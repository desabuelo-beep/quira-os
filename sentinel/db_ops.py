"""
sentinel/db_ops.py
Operaciones de base de datos — Sprint 2.5A+

Compatible con SQLite (local) y Supabase PostgreSQL.
El modo se configura en .streamlit/secrets.toml — ver db_config.py.

Operaciones disponibles:
    ingest_cedula()         → pipeline completo (upload + lines + kpis)
    save_cedula_upload()    → registra documento en document_uploads
    save_execution_lines()  → inserta líneas de cédula (bulk)
    save_monthly_kpis()     → calcula y guarda indicadores del mes
    get_existing_hashes()   → SHA256 existentes (guardrail G4)
    get_existing_periods()  → períodos existentes (guardrail G5)
    get_upload_history()    → historial de cédulas subidas
    get_kpi_history()       → serie temporal de Ti para gráficas
    get_last_kpi()          → último KPI disponible
    get_cedulas_count()     → conteo total de cédulas

Dylus Lab © 2026
"""
from __future__ import annotations

import time
from typing import Optional

import pandas as pd

from sentinel.db_config import get_connection, SCHEMA_VERSION
from sentinel.cedula_parser import CedulaParseResult

SENTINEL_VERSION = "2.5.0"


# ── ESCRITURA ─────────────────────────────────────────────────────────────────
def save_cedula_upload(
    result:      CedulaParseResult,
    year:        int,
    month:       int,
    file_name:   str,
    uploaded_by: str = "analista",
    notes:       str = "",
    entidad:     str = "GAD",
) -> int:
    """
    Registra la cédula en document_uploads.
    Usa RETURNING id — compatible con SQLite 3.35+ y PostgreSQL.

    Returns:
        upload_id — ID del registro creado
    """
    conn = get_connection()
    c    = conn.cursor()

    # Versión: ¿cuántas cédulas previas de este período?
    row = c.execute(
        "SELECT MAX(version) as max_v FROM document_uploads "
        "WHERE document_type='CEDULA' AND period_year=? AND period_month=? AND entidad=?",
        (year, month, entidad),
    ).fetchone()
    version = ((row["max_v"] or 0) + 1) if row else 1

    status = "OK" if result.ok else "ERROR"
    ts     = time.strftime("%Y-%m-%dT%H:%M:%S")

    row_id = c.execute("""
        INSERT INTO document_uploads
            (document_type, period_year, period_month, version,
             file_name, sha256, size_bytes, uploaded_by, uploaded_at,
             validation_status, validation_notes, notes, entidad, sentinel_version)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        RETURNING id
    """, (
        "CEDULA", year, month, version,
        file_name, result.sha256, result.size_bytes,
        uploaded_by, ts,
        status, result.error or "",
        notes, entidad, SENTINEL_VERSION,
    )).fetchone()

    upload_id = row_id["id"]
    conn.commit()
    conn.close()
    return upload_id


def save_execution_lines(
    upload_id: int,
    result:    CedulaParseResult,
    year:      int,
    month:     int,
) -> int:
    """
    Inserta líneas de ejecución presupuestaria (bulk).

    Returns:
        Número de filas insertadas.
    """
    if result.df is None or result.df.empty:
        return 0

    conn = get_connection()
    c    = conn.cursor()
    col  = result.col_map
    df   = result.df
    ts   = time.strftime("%Y-%m-%dT%H:%M:%S")

    def _s(col_name: str, row) -> str:
        real = col.get(col_name)
        if real and real in df.columns:
            v = row[real]
            return "" if pd.isna(v) else str(v).strip()
        return ""

    def _f(internal: str, row) -> float:
        key = f"_{internal}"
        if key in df.columns:
            v = row[key]
            return 0.0 if pd.isna(v) else float(v)
        return 0.0

    rows_to_insert = []
    for _, row in df.iterrows():
        rows_to_insert.append((
            upload_id, year, month,
            _s("unidad", row),
            _s("unidad", row),
            _s("programa", row),
            "",
            _s("proyecto", row),
            _s("partida", row),
            _s("descripcion", row),
            _f("codificado", row),
            0.0,
            _f("codificado", row),   # vigente = codificado (fallback)
            0.0,
            _f("devengado", row),
            _f("pagado", row),
            0.0,
            0.0,
            row.get("_grupo", ""),
            1 if row.get("_es_inversion", False) else 0,
            ts,
        ))

    c.executemany("""
        INSERT INTO budget_execution_lines
            (upload_id, period_year, period_month,
             unidad_codigo, unidad_nombre, programa, subprograma, proyecto,
             partida, descripcion,
             codificado, reformas, vigente, comprometido, devengado, pagado,
             saldo, pct_ejecucion,
             grupo_gasto, es_inversion, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, rows_to_insert)

    conn.commit()
    conn.close()
    return len(rows_to_insert)


def save_monthly_kpis(
    upload_id: int,
    result:    CedulaParseResult,
    year:      int,
    month:     int,
    entidad:   str = "GAD",
) -> None:
    """
    Calcula y guarda KPIs del mes.
    Ti acumulado = promedio de todos los meses del año hasta este período.
    """
    conn = get_connection()
    c    = conn.cursor()
    ts   = time.strftime("%Y-%m-%dT%H:%M:%S")

    rows_year = c.execute(
        "SELECT ti_mensual_pct FROM monthly_kpis "
        "WHERE period_year=? AND entidad=? AND ti_mensual_pct IS NOT NULL",
        (year, entidad),
    ).fetchall()
    valores = [r["ti_mensual_pct"] for r in rows_year] + [result.ti_mensual_pct]
    ti_acumulado = round(sum(valores) / len(valores), 2)

    c.execute("""
        INSERT INTO monthly_kpis
            (upload_id, period_year, period_month, entidad,
             d3_ejecucion, d3_source,
             irs_valor,
             codificado_total, devengado_total,
             devengado_inv, codificado_inv,
             ti_mensual_pct, ti_acumulado_pct,
             calculated_at, sentinel_version)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        upload_id, year, month, entidad,
        result.ti_mensual_pct, "cedula_mensual",
        None,
        result.codificado_total, result.devengado_total,
        result.devengado_inv, result.codificado_inv,
        result.ti_mensual_pct, ti_acumulado,
        ts, SENTINEL_VERSION,
    ))

    conn.commit()
    conn.close()


# ── CONSULTAS ─────────────────────────────────────────────────────────────────
def get_existing_hashes() -> list[str]:
    """SHA256 ya registrados — para guardrail G4."""
    conn = get_connection()
    rows = conn.execute("SELECT sha256 FROM document_uploads").fetchall()
    conn.close()
    return [r["sha256"] for r in rows]


def get_existing_periods() -> list[tuple]:
    """Pares (year, month) ya registrados — para guardrail G5."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT period_year, period_month FROM document_uploads "
        "WHERE document_type='CEDULA'"
    ).fetchall()
    conn.close()
    return [(r["period_year"], r["period_month"]) for r in rows]


def get_upload_history(limit: int = 20) -> list[dict]:
    """Historial de documentos subidos, más recientes primero."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, document_type, period_year, period_month, version,
               file_name, sha256, size_bytes, uploaded_by, uploaded_at,
               validation_status, notes, entidad
        FROM document_uploads
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows   # ya son list[dict] por el wrapper


def get_kpi_history(year: int | None = None) -> list[dict]:
    """Serie temporal de KPIs. Si year se provee, filtra por ese año."""
    conn = get_connection()
    if year:
        rows = conn.execute("""
            SELECT k.period_year, k.period_month,
                   k.ti_mensual_pct, k.ti_acumulado_pct,
                   k.codificado_total, k.devengado_total,
                   k.devengado_inv, k.codificado_inv,
                   k.calculated_at,
                   u.file_name, u.version
            FROM monthly_kpis k
            JOIN document_uploads u ON k.upload_id = u.id
            WHERE k.period_year=?
            ORDER BY k.period_year, k.period_month
        """, (year,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT k.period_year, k.period_month,
                   k.ti_mensual_pct, k.ti_acumulado_pct,
                   k.codificado_total, k.devengado_total,
                   k.devengado_inv, k.codificado_inv,
                   k.calculated_at,
                   u.file_name, u.version
            FROM monthly_kpis k
            JOIN document_uploads u ON k.upload_id = u.id
            ORDER BY k.period_year, k.period_month
        """).fetchall()
    conn.close()
    return rows


def get_last_kpi() -> Optional[dict]:
    """Último KPI disponible — para D3 en tiempo real en Centro de Control."""
    conn = get_connection()
    row  = conn.execute("""
        SELECT k.period_year, k.period_month,
               k.ti_mensual_pct, k.ti_acumulado_pct,
               k.codificado_total, k.devengado_total,
               k.devengado_inv, k.codificado_inv,
               k.calculated_at,
               u.file_name, u.version
        FROM monthly_kpis k
        JOIN document_uploads u ON k.upload_id = u.id
        ORDER BY k.period_year DESC, k.period_month DESC
        LIMIT 1
    """).fetchone()
    conn.close()
    return row   # dict o None


def get_cedulas_count() -> int:
    """Número total de cédulas registradas."""
    conn = get_connection()
    row  = conn.execute(
        "SELECT COUNT(*) as n FROM document_uploads WHERE document_type='CEDULA'"
    ).fetchone()
    conn.close()
    return row["n"] if row else 0


# ── PIPELINE COMPLETO ─────────────────────────────────────────────────────────
def ingest_cedula(
    result:      CedulaParseResult,
    year:        int,
    month:       int,
    file_name:   str,
    uploaded_by: str = "analista",
    notes:       str = "",
    entidad:     str = "GAD",
) -> dict:
    """
    Pipeline completo de ingesta en un solo paso:
      1. Registra en document_uploads
      2. Inserta líneas de ejecución (bulk)
      3. Calcula y guarda KPIs del mes

    Returns:
        dict con ok, upload_id, lines_inserted, ti_mensual_pct
    """
    if not result.ok:
        return {
            "ok":             False,
            "error":          result.error,
            "upload_id":      None,
            "lines_inserted": 0,
            "ti_mensual_pct": 0.0,
        }

    upload_id      = save_cedula_upload(result, year, month, file_name, uploaded_by, notes, entidad)
    lines_inserted = save_execution_lines(upload_id, result, year, month)
    save_monthly_kpis(upload_id, result, year, month, entidad)

    return {
        "ok":             True,
        "upload_id":      upload_id,
        "lines_inserted": lines_inserted,
        "ti_mensual_pct": result.ti_mensual_pct,
        "sha256":         result.sha256,
    }
