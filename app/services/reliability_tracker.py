"""
QUIRA Intelligence — Reliability Tracker (Sprint 3 · P3)

Trazabilidad longitudinal de confiabilidad por fuente institucional.
La "densidad de trazabilidad pública" es un indicador institucional en sí mismo.

Funciones públicas:
  get_reliability_dashboard()      → tabla actual de confiabilidad por fuente
  get_reliability_history()        → evolución histórica de confiabilidad mensual
  get_traceability_trend()         → serie temporal del traceability_score
  get_source_health()              → diagnóstico de salud por fuente (última lectura)
  build_reliability_report()       → informe completo de confiabilidad

Doctrina: cada snapshot registra la confiabilidad real observada de sus fuentes.
El tracker agrega esa información longitudinalmente.

Stack (reemplazable): longitudinal_engine para carga de snapshots.
Firmas de función: permanentes.

Dylus Lab © 2026
"""
from __future__ import annotations

from typing import Any

from utils.logger import get_logger

logger = get_logger(__name__)

# ── Catálogo canónico de fuentes ───────────────────────────────────────────────
FUENTES_CATALOG: list[dict] = [
    {
        "key":        "gold_master",
        "nombre":     "Gold Master Excel",
        "categoria":  "Canónico",
        "icono":      "📋",
        "reliability_base": 0.99,
        "descripcion": "Motor metodológico TGI/ICPI/D1-D5 · Dylus Lab",
    },
    {
        "key":        "dpe",
        "nombre":     "DPE API",
        "categoria":  "Operativo",
        "icono":      "📊",
        "reliability_base": 0.95,
        "descripcion": "eSIGEF · presupuesto y ejecución institucional",
    },
    {
        "key":        "sercop",
        "nombre":     "SERCOP OCDS",
        "categoria":  "Operativo",
        "icono":      "📝",
        "reliability_base": 0.95,
        "descripcion": "Portal contratación pública · estándar OCDS",
    },
    {
        "key":        "cpccs",
        "nombre":     "CPCCS RdC",
        "categoria":  "Funcional",
        "icono":      "🏛",
        "reliability_base": 0.80,
        "descripcion": "Rendición de cuentas ciudadana · portal CPCCS",
    },
]

_MUNICIPIO_DEFAULT = "130801"


# ══════════════════════════════════════════════════════════════════════════════
# Helpers internos
# ══════════════════════════════════════════════════════════════════════════════

def _get_source_data(snap: dict, key: str) -> dict:
    """Extrae datos de una fuente desde el snapshot. Tolerante a múltiples formatos."""
    sources: dict = snap.get("sources") or {}
    src = sources.get(key) or {}
    return {
        "status":      src.get("status", "unknown"),
        "reliability": src.get("reliability"),
        "error":       src.get("error"),
    }


def _snap_period(snap: dict) -> str:
    """Etiqueta legible del período del snapshot."""
    try:
        from app.services.longitudinal_engine import _period_label  # type: ignore
        return _period_label(snap)
    except Exception:
        raw = (snap.get("_meta") or {}).get("fecha_corte", "")
        return str(raw) or "—"


def _snap_fecha(snap: dict) -> str:
    """fecha_corte ISO del snapshot."""
    return (snap.get("_meta") or {}).get("fecha_corte", "")


def _effective_reliability(snap_reliability: float | None, base: float) -> float:
    """
    Confiabilidad efectiva del snapshot.
    Si el snapshot registró una fiabilidad medida, usarla; si no, usar la base del catálogo.
    """
    if snap_reliability is not None:
        try:
            v = float(snap_reliability)
            if 0.0 <= v <= 1.0:
                return round(v, 4)
        except (TypeError, ValueError):
            pass
    return base


def _reliability_label(rel: float) -> str:
    if rel >= 0.95:
        return "Excelente"
    if rel >= 0.85:
        return "Muy bueno"
    if rel >= 0.70:
        return "Funcional"
    if rel >= 0.50:
        return "Limitado"
    return "Crítico"


# ══════════════════════════════════════════════════════════════════════════════
# 1. Dashboard de confiabilidad actual
# ══════════════════════════════════════════════════════════════════════════════

def get_reliability_dashboard(
    municipio_code: str = _MUNICIPIO_DEFAULT,
) -> list[dict]:
    """
    Tabla de confiabilidad actual por fuente, basada en el snapshot activo.

    Cada dict en la lista contiene:
        key          str    Clave interna de la fuente
        nombre       str    Nombre legible
        categoria    str    "Canónico" | "Operativo" | "Funcional" | "Manual"
        icono        str    Emoji representativo
        reliability  float  Confiabilidad efectiva (0.0–1.0)
        label        str    "Excelente" | "Muy bueno" | "Funcional" | ...
        status       str    "ok" | "error" | "unknown"
        error        str|None  Mensaje de error si status != "ok"
        descripcion  str    Descripción de la fuente

    Returns:
        Lista con una entrada por fuente del catálogo.
    """
    snap: dict | None = None
    try:
        from utils.snapshot_io import load_snapshot
        snap, _ = load_snapshot(municipio_code=municipio_code)
    except Exception as exc:
        logger.warning("reliability_dashboard: no se pudo cargar snapshot: %s", exc)

    result: list[dict] = []
    for fuente in FUENTES_CATALOG:
        base = fuente["reliability_base"]
        if snap:
            sd = _get_source_data(snap, fuente["key"])
            eff = _effective_reliability(sd.get("reliability"), base)
            status = sd.get("status", "unknown")
            error  = sd.get("error")
        else:
            eff    = base
            status = "unknown"
            error  = None

        result.append({
            "key":         fuente["key"],
            "nombre":      fuente["nombre"],
            "categoria":   fuente["categoria"],
            "icono":       fuente["icono"],
            "reliability": eff,
            "label":       _reliability_label(eff),
            "status":      status,
            "error":       error,
            "descripcion": fuente["descripcion"],
        })

    return result


# ══════════════════════════════════════════════════════════════════════════════
# 2. Historial de confiabilidad longitudinal
# ══════════════════════════════════════════════════════════════════════════════

def get_reliability_history(
    municipio_code: str = _MUNICIPIO_DEFAULT,
    limit: int = 12,
) -> list[dict]:
    """
    Evolución histórica de confiabilidad por fuente, oldest-first.

    Cada dict contiene:
        periodo        str    Etiqueta legible: "May 2026"
        fecha_corte    str    ISO date
        traceability   float|None  traceability_score global del snapshot
        source_conf    float|None  source_confidence ponderada
        fuentes        dict   {key: {"reliability": float, "status": str}}

    Args:
        municipio_code: Código de 6 dígitos del municipio.
        limit:          Máximo de períodos a retornar.

    Returns:
        Lista de dicts con historial de confiabilidad, oldest-first.
    """
    try:
        from app.services.longitudinal_engine import get_snapshot_history
        history = get_snapshot_history(municipio_code, limit=limit)
    except Exception as exc:
        logger.warning("reliability_history: error cargando historial: %s", exc)
        return []

    if not history:
        return []

    rows: list[dict] = []
    for snap in history:
        fuentes_snap: dict[str, Any] = {}
        for fuente in FUENTES_CATALOG:
            key  = fuente["key"]
            base = fuente["reliability_base"]
            sd   = _get_source_data(snap, key)
            fuentes_snap[key] = {
                "reliability": _effective_reliability(sd.get("reliability"), base),
                "status":      sd.get("status", "unknown"),
            }

        rows.append({
            "periodo":      _snap_period(snap),
            "fecha_corte":  _snap_fecha(snap),
            "traceability": snap.get("traceability_score"),
            "source_conf":  snap.get("source_confidence"),
            "fuentes":      fuentes_snap,
        })

    return rows


# ══════════════════════════════════════════════════════════════════════════════
# 3. Serie temporal de trazabilidad
# ══════════════════════════════════════════════════════════════════════════════

def get_traceability_trend(
    municipio_code: str = _MUNICIPIO_DEFAULT,
    limit: int = 12,
) -> list[tuple[str, float | None]]:
    """
    Serie temporal del traceability_score global (0.0–1.0), oldest-first.

    Returns:
        Lista de tuplas (periodo_label, traceability_score | None).
    """
    history = get_reliability_history(municipio_code=municipio_code, limit=limit)
    return [(row["periodo"], row.get("traceability")) for row in history]


# ══════════════════════════════════════════════════════════════════════════════
# 4. Diagnóstico de salud por fuente
# ══════════════════════════════════════════════════════════════════════════════

def get_source_health(
    municipio_code: str = _MUNICIPIO_DEFAULT,
) -> dict[str, str]:
    """
    Diagnóstico simple de salud actual para cada fuente.

    Returns:
        Dict {key: "OK" | "DEGRADED" | "ERROR" | "UNKNOWN"}.
    """
    dashboard = get_reliability_dashboard(municipio_code=municipio_code)
    result: dict[str, str] = {}
    for item in dashboard:
        status = item.get("status", "unknown")
        rel    = item.get("reliability", 0.0)
        if status == "ok" and rel >= 0.85:
            health = "OK"
        elif status == "ok" and rel >= 0.60:
            health = "DEGRADED"
        elif status == "error" or item.get("error"):
            health = "ERROR"
        else:
            health = "UNKNOWN"
        result[item["key"]] = health
    return result


# ══════════════════════════════════════════════════════════════════════════════
# 5. Informe completo de confiabilidad
# ══════════════════════════════════════════════════════════════════════════════

def build_reliability_report(
    municipio_code: str = _MUNICIPIO_DEFAULT,
    limit: int = 12,
) -> dict:
    """
    Informe completo de confiabilidad del sistema de fuentes.

    Keys del dict retornado:
        dashboard        list[dict]   Estado actual por fuente
        history          list[dict]   Historial longitudinal
        traceability_series list[tuple] Serie temporal traceability_score
        source_health    dict[str,str] Diagnóstico rápido por fuente
        avg_reliability  float|None   Promedio ponderado de confiabilidad actual
        n_ok             int          Número de fuentes con status="ok"
        n_errors         int          Número de fuentes con error
        error            str|None     Mensaje global si hubo fallo

    Args:
        municipio_code: Código de 6 dígitos del municipio.
        limit:          Períodos máximos en el historial.

    Returns:
        Dict con el informe completo.
    """
    _empty: dict = {
        "dashboard":          [],
        "history":            [],
        "traceability_series": [],
        "source_health":      {},
        "avg_reliability":    None,
        "n_ok":               0,
        "n_errors":           0,
        "error":              None,
    }

    try:
        dashboard  = get_reliability_dashboard(municipio_code)
        history    = get_reliability_history(municipio_code, limit=limit)
        traz_series = get_traceability_trend(municipio_code, limit=limit)
        health     = get_source_health(municipio_code)

        # Promedio ponderado de confiabilidad actual
        rels   = [item["reliability"] for item in dashboard if item.get("reliability") is not None]
        avg    = round(sum(rels) / len(rels), 4) if rels else None
        n_ok   = sum(1 for item in dashboard if item.get("status") == "ok")
        n_err  = sum(1 for item in dashboard if item.get("error"))

        return {
            "dashboard":           dashboard,
            "history":             history,
            "traceability_series": traz_series,
            "source_health":       health,
            "avg_reliability":     avg,
            "n_ok":                n_ok,
            "n_errors":            n_err,
            "error":               None,
        }

    except Exception as exc:
        logger.error("build_reliability_report: %s", exc)
        return {**_empty, "error": str(exc)}
