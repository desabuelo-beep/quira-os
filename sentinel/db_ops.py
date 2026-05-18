"""
sentinel/db_ops.py
Operaciones de base de datos — Sprint 2.5A

Capa de acceso a datos para el pipeline de ingesta mensual.
Separa la lógica SQL del parser y de la UI.

Operaciones disponibles:
    save_cedula_upload()    → registra el documento en document_uploads
    save_execution_lines()  → inserta las líneas de la cédula (bulk)
    save_monthly_kpis()     → calcula y guarda indicadores del mes
    get_existing_hashes()   → para guardrail G4 (duplicados)
    get_existing_periods()  → para guardrail G5 (versionado)
    get_upload_history()    → historial de cédulas subidas
    get_kpi_history()       → serie temporal de Ti para gráficas
    get_last_kpi()          → último KPI disponible (para Centro de Control)

Dylus Lab © 2026
"""
from __future__ import annotations

import time
from typing import Optional

import pandas as pd

from sentinel.db_config import get_connection, SCHEMA_VERSION
from sentinel.cedula_parser import CedulaParseResult

# Versión del agente Sentinel que genera los registros
SENTINEL_VERSION = "2.5.0"


# ── ESCRITURA ─────────────────────────────────────────────────────────────────
def save_cedula_upload(
    result:      CedulaParseResult,
    year:        int,
    month:       int,
    file_name:   str,
    uploaded_by: str = "analista",
    notes:       str = "",
) -> int:
    """
    Registra la cédula en document_uploads.

    Returns:
        upload_id — ID del registro creado (FK para las demás tablas)
    """
    conn = get_connection()
    c    = conn.cursor()

    # Calcular versión (¿cuántas cédulas previas de este período?)
    row = c.execute(
        "SELECT MAX(version) FROM document_uploads "
        "WHERE document_type='CEDULA' AND period_year=? AND period_month=?",
        (year, month),
    ).fetchone()
    version = (row[0] or 0) + 1

    status = "OK" if result.ok else "ERROR"
    ts     = time.strftime("%Y-%m-%dT%H:%M:%S")

    c.execute("""
        INSERT INTO document_uploads
            (document_type, period_year, period_month, version,
             file_name, sha256, size_bytes, uploaded_by, uploaded_at,
             validation_status, validation_notes, notes, sentinel_version)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        "CEDULA", year, month, version,
        file_name, result.sha256, result.size_bytes,
        uploaded_by, ts,
        status, result.error or "",
        notes, SENTINEL_VERSION,
    ))

    upload_id = c.lastrowid
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
    Inserta las líneas de ejecución presupuestaria en budget_execution_lines.

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
        """Extrae valor como string, safe."""
        real = col.get(col_name)
        if real and real in df.columns:
            v = row[real]
            return "" if pd.isna(v) else str(v).strip()
        return ""

    def _f(col_name: str, row) -> float:
        """Extrae valor del campo canonico calculado (prefijo _)."""
        col_calc = f"_{col_name}"
        if col_calc in df.columns:
            v = row[col_calc]
            return 0.0 if pd.isna(v) else float(v)
        return 0.0

    rows_to_insert = []
    for _, row in df.iterrows():
        rows_to_insert.append((
            upload_id, year, month,
            _s("unidad", row),      # unidad_codigo — placeholder
            _s("unidad", row),      # unidad_nombre
            _s("programa", row),
            "",                     # subprograma — no siempre presente
            _s("proyecto", row),
            _s("partida", row),
            _s("descripcion", row),
            _f("codificado", row),
            0.0,                    # reformas — no siempre presente
            _f("codificado", row),  # vigente = codificado si no hay columna vigente
            0.0,                    # comprometido
            _f("devengado", row),
            _f("pagado", row),
            0.0,                    # saldo — calculable pero no siempre viene
            0.0,                    # pct_ejecucion — calculable
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
    n = c.rowcount
    conn.close()
    return len(rows_to_insert)


def save_monthly_kpis(
    upload_id: int,
    result:    CedulaParseResult,
    year:      int,
    month:     int,
) -> None:
    """
    Calcula y guarda los KPIs del mes en monthly_kpis.
    Incluye Ti acumulado (promedio de meses del año hasta el período).
    """
    conn = get_connection()
    c    = conn.cursor()
    ts   = time.strftime("%Y-%m-%dT%H:%M:%S")

    # Ti acumulado: promedio de ti_mensual_pct de todos los meses del año
    rows_year = c.execute(
        "SELECT ti_mensual_pct FROM monthly_kpis WHERE period_year=? AND ti_mensual_pct IS NOT NULL",
        (year,),
    ).fetchall()
    valores_previos = [r[0] for r in rows_year if r[0] is not None]
    valores_previos.append(result.ti_mensual_pct)
    ti_acumulado = round(sum(valores_previos) / len(valores_previos), 2)

    c.execute("""
        INSERT INTO monthly_kpis
            (upload_id, period_year, period_month,
             d3_ejecucion, d3_source,
             irs_valor,
             codificado_total, devengado_total,
             devengado_inv, codificado_inv,
             ti_mensual_pct, ti_acumulado_pct,
             calculated_at, sentinel_version)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        upload_id, year, month,
        result.ti_mensual_pct, "cedula_mensual",
        None,   # IRS se calcula aparte con todas las dimensiones
        result.codificado_total, result.devengado_total,
        result.devengado_inv, result.codificado_inv,
        result.ti_mensual_pct, ti_acumulado,
        ts, SENTINEL_VERSION,
    ))

    conn.commit()
    conn.close()


# ── CONSULTAS ─────────────────────────────────────────────────────────────────
def get_existing_hashes() -> list[str]:
    """Retorna todos los SHA256 ya registrados (para G4)."""
    conn = get_connection()
    rows = conn.execute("SELECT sha256 FROM document_uploads").fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_existing_periods() -> list[tuple]:
    """Retorna pares (year, month) ya registrados para CEDULA (para G5)."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT period_year, period_month FROM document_uploads "
        "WHERE document_type='CEDULA'"
    ).fetchall()
    conn.close()
    return [(r[0], r[1]) for r in rows]


def get_upload_history(limit: int = 20) -> list[dict]:
    """Historial de documentos subidos, más recientes primero."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, document_type, period_year, period_month, version,
               file_name, sha256, size_bytes, uploaded_by, uploaded_at,
               validation_status, notes
        FROM document_uploads
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_kpi_history(year: int | None = None) -> list[dict]:
    """
    Serie temporal de KPIs mensuales.
    Si year se provee, filtra por ese año.
    """
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
    return [dict(r) for r in rows]


def get_last_kpi() -> Optional[dict]:
    """Último KPI disponible — usado por Centro de Control para D3 en tiempo real."""
    conn = get_connection()
    row = conn.execute("""
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
    return dict(row) if row else None


def get_cedulas_count() -> int:
    """Número total de cédulas registradas."""
    conn = get_connection()
    n = conn.execute(
        "SELECT COUNT(*) FROM document_uploads WHERE document_type='CEDULA'"
    ).fetchone()[0]
    conn.close()
    return n


# ── PIPELINE COMPLETO ─────────────────────────────────────────────────────────
def ingest_cedula(
    result:      CedulaParseResult,
    year:        int,
    month:       int,
    file_name:   str,
    uploaded_by: str = "analista",
    notes:       str = "",
) -> dict:
    """
    Pipeline completo de ingesta:
      1. Registra en document_uploads
      2. Inserta líneas de ejecución
      3. Calcula y guarda KPIs del mes

    Returns:
        dict con upload_id, lines_inserted, ti_mensual_pct, ok
    """
    if not result.ok:
        return {
            "ok":           False,
            "error":        result.error,
            "upload_id":    None,
            "lines_inserted": 0,
            "ti_mensual_pct": 0.0,
        }

    upload_id     = save_cedula_upload(result, year, month, file_name, uploaded_by, notes)
    lines_inserted = save_execution_lines(upload_id, result, year, month)
    save_monthly_kpis(upload_id, result, year, month)

    return {
        "ok":             True,
        "upload_id":      upload_id,
        "lines_inserted": lines_inserted,
        "ti_mensual_pct": result.ti_mensual_pct,
        "sha256":         result.sha256,
    }
