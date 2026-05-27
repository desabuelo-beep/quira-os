"""
QUIRA OS — Longitudinal Engine (RC-M)
Sprint 3 · Prioridad 1

Convierte el sistema de "foto instantánea" en "trayectoria institucional".
Implementa el motor RC-M canónico: Período | ICPI | D3 Ti | SAT-IV | Riesgo.

Funciones:
  get_snapshot_history()      → lista de snapshots ordenados (oldest-first)
  build_rcm_table()           → tabla RC-M canónica para UI
  build_metric_trend()        → serie temporal de cualquier métrica (dot-notation)
  detect_trend()              → MEJORA / DETERIORO / ESTABLE / INSUFICIENTE_DATOS
  get_longitudinal_summary()  → resumen de alto nivel para dashboard

Doctrina: Q4-Memoria opera sobre snapshots Q1 guardados en data/snapshots/.
Stack (local JSON + Supabase) es reemplazable. Las firmas de función son permanentes.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import config as cfg
from utils.logger import get_logger

logger = get_logger(__name__)

# ── Constantes ─────────────────────────────────────────────────────────────────
_MESES_ES = {
    1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic",
}

# Delta mínimo (en pp) para clasificar como MEJORA o DETERIORO
_TREND_THRESHOLD_PP = 1.0


# ══════════════════════════════════════════════════════════════════════════════
# Helpers internos
# ══════════════════════════════════════════════════════════════════════════════

def _get_nested(d: dict, path: str, default: Any = None) -> Any:
    """Resuelve dot-notation en dict anidado. E.g. 'icpi.global_pct'."""
    node = d
    for key in path.split("."):
        if not isinstance(node, dict):
            return default
        node = node.get(key)
        if node is None:
            return default
    return node


def _period_label(snap: dict) -> str:
    """Etiqueta legible del período a partir de fecha_corte (YYYY-MM-DD → 'May 2026')."""
    raw = _get_nested(snap, "_meta.fecha_corte", "")
    try:
        dt = datetime.strptime(str(raw), "%Y-%m-%d")
        return f"{_MESES_ES[dt.month]} {dt.year}"
    except Exception:
        return str(raw) or "Desconocido"


def _snap_timestamp(snap: dict) -> datetime:
    """Parsea generated_at para ordenamiento cronológico."""
    raw = _get_nested(snap, "_meta.generated_at", "")
    try:
        # fromisoformat acepta +00:00 desde Python 3.7
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except Exception:
        # Fallback: intentar parsear fecha_corte
        raw2 = _get_nested(snap, "_meta.fecha_corte", "")
        try:
            return datetime.strptime(str(raw2), "%Y-%m-%d")
        except Exception:
            return datetime.min


def _dedup_snapshots(snaps: list[dict], limit: int) -> list[dict]:
    """
    Deduplica por fecha_corte (mismo período), conservando el generated_at más reciente.
    Retorna lista ordenada oldest-first, máximo `limit` elementos.
    """
    best: dict[str, dict] = {}
    for snap in snaps:
        key = _get_nested(snap, "_meta.fecha_corte", "unknown")
        if key == "unknown":
            key = _snap_timestamp(snap).strftime("%Y-%m-%d")
        existing = best.get(key)
        if existing is None or _snap_timestamp(snap) > _snap_timestamp(existing):
            best[key] = snap
    ordered = sorted(best.values(), key=_snap_timestamp)
    return ordered[-limit:]


# ══════════════════════════════════════════════════════════════════════════════
# 1. Carga de snapshots
# ══════════════════════════════════════════════════════════════════════════════

def _load_local_snapshots(municipio_code: str, limit: int) -> list[dict]:
    """Carga snapshots desde archivos JSON locales en data/snapshots/<codigo>/."""
    snap_dir = Path(cfg.SNAPSHOTS_DIR) / municipio_code
    if not snap_dir.exists():
        logger.warning("Directorio de snapshots no encontrado: %s", snap_dir)
        return []

    # Tomar los N más recientes por nombre de archivo (contiene timestamp)
    files = sorted(snap_dir.glob(f"{municipio_code}_*.json"), reverse=True)[: limit * 2]
    snaps: list[dict] = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                snaps.append(json.load(fh))
        except Exception as exc:
            logger.warning("Error al cargar snapshot %s: %s", f.name, exc)
    return snaps


def _load_supabase_snapshots(municipio_code: str, limit: int) -> list[dict]:
    """
    Carga snapshots históricos desde Supabase (tabla municipality_snapshots).
    Retorna lista vacía si Supabase no está disponible o falla.
    """
    try:
        from sentinel.db_config import get_connection  # noqa: QUIRA-DEPR — migrar a utils.db_config en v7.0
        conn = get_connection()
        c = conn.cursor()
        c.execute(
            """SELECT snapshot_json, fecha_corte
               FROM municipality_snapshots
               WHERE municipio_code = ?
               ORDER BY fecha_corte ASC
               LIMIT ?""",
            (municipio_code, limit),
        )
        rows = c.fetchall()
        conn.close()
        snaps: list[dict] = []
        for row in rows:
            try:
                raw = row["snapshot_json"] if isinstance(row, dict) else row[0]
                snap = json.loads(raw) if isinstance(raw, str) else raw
                snaps.append(snap)
            except Exception as exc:
                logger.warning("Error al parsear snapshot de Supabase: %s", exc)
        logger.info(
            "Supabase: %d snapshots cargados para %s", len(snaps), municipio_code
        )
        return snaps
    except Exception as exc:
        logger.debug("Supabase no disponible para historial longitudinal: %s", exc)
        return []


def get_snapshot_history(
    municipio_code: str = "130801",
    limit: int = 12,
    prefer_local: bool = False,
) -> list[dict]:
    """
    Carga el historial de snapshots de un municipio, oldest-first.

    Estrategia de carga:
    1. Supabase (canónico, de-duplicado por fecha_corte) — salvo prefer_local=True
    2. Archivos JSON locales (data/snapshots/<codigo>/)
    3. Deduplicación final por fecha_corte (mismo período = conservar más reciente)

    Args:
        municipio_code: Código de 6 dígitos del municipio.
        limit:          Máximo de períodos únicos a retornar.
        prefer_local:   Si True, omite la búsqueda en Supabase.

    Returns:
        Lista de dicts snapshot, oldest-first, máximo `limit` elementos.
    """
    raw_snaps: list[dict] = []

    if not prefer_local:
        raw_snaps = _load_supabase_snapshots(municipio_code, limit * 2)

    if not raw_snaps:
        raw_snaps = _load_local_snapshots(municipio_code, limit * 2)

    if not raw_snaps:
        logger.warning("No hay snapshots disponibles para %s", municipio_code)
        return []

    return _dedup_snapshots(raw_snaps, limit)


# ══════════════════════════════════════════════════════════════════════════════
# 2. Tabla RC-M canónica
# ══════════════════════════════════════════════════════════════════════════════

def _sat_iv_status(snap: dict) -> str:
    """
    Determina el estado de SAT-IV en el snapshot.

    Jerarquía:
    1. sat.activas / sat.alertas_activas (lista de códigos activos)
    2. sat.alertas → buscar SAT-IV por campo 'estado'
    3. 'SIN DATOS' si no hay información evaluada
    """
    activas: list[str] = (
        _get_nested(snap, "sat.activas", [])
        or _get_nested(snap, "sat.alertas_activas", [])
        or []
    )
    if "SAT-IV" in activas:
        return "ACTIVA"

    # Buscar en el catálogo completo de alertas evaluadas
    alertas: list[dict] = _get_nested(snap, "sat.alertas", []) or []
    for alerta in alertas:
        if alerta.get("codigo") == "SAT-IV":
            estado = alerta.get("estado", "SIN_DATOS")
            if estado == "ACTIVA":
                return "ACTIVA"
            if estado == "SIN_DATOS":
                return "SIN DATOS"
            # INACTIVA, MITIGADA, etc.
            return "mitigada"

    return "SIN DATOS"


def build_rcm_table(history: list[dict]) -> list[dict]:
    """
    Construye la tabla RC-M canónica de SPRINT3.md.

    Columnas por fila:
        periodo     str          Etiqueta legible: "May 2026"
        icpi_pct    float|None   ICPI global en porcentaje (0-100)
        d3_ti_pct   float|None   Ti ejecución presupuestaria en % (isp_salud_presup × 100)
        sat_iv      str          "ACTIVA" | "mitigada" | "SIN DATOS"
        riesgo      str          "ALTO" | "MEDIO" | "BAJO" | "CRÍTICO" | "—"
        fecha_corte str          ISO date (YYYY-MM-DD) para tooltip / ordenamiento

    Args:
        history: Lista de snapshots oldest-first (de get_snapshot_history).

    Returns:
        Lista de dicts con las columnas RC-M, mismo orden que history.
    """
    rows: list[dict] = []
    for snap in history:
        # ICPI
        icpi_raw = _get_nested(snap, "icpi.global_pct")
        icpi_pct = round(float(icpi_raw), 2) if icpi_raw is not None else None

        # D3 Ti — isp_salud_presup está en ratio (0.1458 → 14.58%)
        d3_raw = _get_nested(snap, "financiero.isp_salud_presup")
        d3_ti_pct = round(float(d3_raw) * 100, 2) if d3_raw is not None else None

        # SAT-IV
        sat_iv = _sat_iv_status(snap)

        # Riesgo SAT ponderado
        riesgo = _get_nested(snap, "sat.clasif_riesgo") or "—"

        rows.append(
            {
                "periodo": _period_label(snap),
                "icpi_pct": icpi_pct,
                "d3_ti_pct": d3_ti_pct,
                "sat_iv": sat_iv,
                "riesgo": riesgo,
                "fecha_corte": _get_nested(snap, "_meta.fecha_corte", ""),
            }
        )
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# 3. Serie temporal de cualquier métrica
# ══════════════════════════════════════════════════════════════════════════════

def build_metric_trend(
    history: list[dict],
    metric_path: str,
) -> list[tuple[str, float | None]]:
    """
    Serie temporal de una métrica usando dot-notation.

    Args:
        history:     Lista de snapshots oldest-first.
        metric_path: Ruta dot-notation. E.g. 'icpi.global_pct',
                     'sat.riesgo_ponderado', 'traceability_score'.

    Returns:
        Lista de tuplas (periodo_label, valor_float | None), oldest-first.
    """
    result: list[tuple[str, float | None]] = []
    for snap in history:
        label = _period_label(snap)
        raw = _get_nested(snap, metric_path)
        val: float | None = None
        if raw is not None:
            try:
                val = float(raw)
            except (TypeError, ValueError):
                val = None
        result.append((label, val))
    return result


# ══════════════════════════════════════════════════════════════════════════════
# 4. Clasificación de tendencia
# ══════════════════════════════════════════════════════════════════════════════

def detect_trend(values: list[float | None]) -> str:
    """
    Clasifica la trayectoria de una serie de valores.

    Reglas (requiere ≥ 2 valores no-None):
    - MEJORA:              último > primero por ≥ _TREND_THRESHOLD_PP
    - DETERIORO:           último < primero por ≥ _TREND_THRESHOLD_PP
    - ESTABLE:             diferencia dentro de ±_TREND_THRESHOLD_PP
    - INSUFICIENTE_DATOS:  menos de 2 valores válidos

    Args:
        values: Lista de floats (puede contener None). Oldest-first.

    Returns:
        Una de las 4 categorías canónicas.
    """
    clean = [v for v in values if v is not None]
    if len(clean) < 2:
        return "INSUFICIENTE_DATOS"
    delta = clean[-1] - clean[0]
    if delta >= _TREND_THRESHOLD_PP:
        return "MEJORA"
    if delta <= -_TREND_THRESHOLD_PP:
        return "DETERIORO"
    return "ESTABLE"


# ══════════════════════════════════════════════════════════════════════════════
# 5. Resumen de alto nivel
# ══════════════════════════════════════════════════════════════════════════════

def get_longitudinal_summary(
    municipio_code: str = "130801",
    prefer_local: bool = False,
) -> dict:
    """
    Resumen longitudinal de alto nivel para widgets de dashboard.

    Keys en el dict retornado:
        n_periodos       int    Número de períodos únicos en el historial
        icpi_trend       str    MEJORA | DETERIORO | ESTABLE | INSUFICIENTE_DATOS
        riesgo_trend     str    Idem, basado en sat.riesgo_ponderado
        last_period      str    Etiqueta del último período ("May 2026")
        last_icpi_pct    float|None
        last_riesgo      str    Clasificación SAT del último período
        last_sat_activas int    Número de alertas SAT activas en el último período
        rcm_table        list[dict]  Tabla RC-M completa (build_rcm_table)
        icpi_series      list[tuple] Serie temporal ICPI (build_metric_trend)
        error            str|None    Mensaje de error si ocurrió, None si ok

    Args:
        municipio_code: Código de 6 dígitos del municipio.
        prefer_local:   Si True, omite Supabase y usa solo archivos locales.

    Returns:
        Dict con las keys descritas arriba.
    """
    _empty = {
        "n_periodos": 0,
        "icpi_trend": "INSUFICIENTE_DATOS",
        "riesgo_trend": "INSUFICIENTE_DATOS",
        "last_period": "—",
        "last_icpi_pct": None,
        "last_riesgo": "—",
        "last_sat_activas": 0,
        "rcm_table": [],
        "icpi_series": [],
        "error": None,
    }

    try:
        history = get_snapshot_history(
            municipio_code, prefer_local=prefer_local
        )
        if not history:
            return {**_empty, "error": "No hay snapshots disponibles para este municipio"}

        rcm_table = build_rcm_table(history)
        icpi_series = build_metric_trend(history, "icpi.global_pct")
        riesgo_series = build_metric_trend(history, "sat.riesgo_ponderado")

        icpi_vals = [v for _, v in icpi_series]
        riesgo_vals = [v for _, v in riesgo_series]

        last = history[-1]
        activas: list[str] = (
            _get_nested(last, "sat.activas", [])
            or _get_nested(last, "sat.alertas_activas", [])
            or []
        )

        return {
            "n_periodos": len(history),
            "icpi_trend": detect_trend(icpi_vals),
            "riesgo_trend": detect_trend(riesgo_vals),
            "last_period": _period_label(last),
            "last_icpi_pct": _get_nested(last, "icpi.global_pct"),
            "last_riesgo": _get_nested(last, "sat.clasif_riesgo", "—") or "—",
            "last_sat_activas": len(activas),
            "rcm_table": rcm_table,
            "icpi_series": icpi_series,
            "error": None,
        }

    except Exception as exc:
        logger.error(
            "Error en get_longitudinal_summary para %s: %s",
            municipio_code, exc, exc_info=True,
        )
        return {**_empty, "error": str(exc)}
