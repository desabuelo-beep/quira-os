"""
sentinel/budget_record_loader.py
RC-7.4 Data Bridge — QUIRA OS
Convierte series_longitudinal del gm_snapshot.json → BudgetRecord objects
para alimentar el pipeline RC-7.2/7.3 en producción.

Estructura esperada en gm_snapshot.json:
  "series_longitudinal": {
    "gad_inversion_g7178": [ { periodo, orden, codificado, devengado, ... }, ... ],
    "ep_aseo_g7178":        [ ... ],
    "bomberos_g7178":       [ ... ],
    "patronato_g7178":      [ ... ],
    "h90_holding_2026q1":   [ ... ],   # sección transversal, no longitudinal por entidad
  }

Uso típico (wiring en render_sentinel):
  from sentinel.budget_record_loader import load_budget_records, get_primary_series
  records = get_primary_series()      # GAD G71-78 — serie primaria D3
  st.session_state["rc72_budget_records"] = records

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# Series con múltiples puntos (análisis longitudinal real)
_LONGITUDINAL_SERIES = [
    "gad_inversion_g7178",
    "ep_aseo_g7178",
    "bomberos_g7178",
    "patronato_g7178",
]

# Sección transversal: todos los entes en un único período → NO es longitudinal
_CROSSSECTION_SERIES = ["h90_holding_2026q1"]


def _record_from_dict(d: dict):
    """
    Convierte un dict del snapshot → BudgetRecord.
    Import tardío de longitudinal_engine para evitar import circular.
    """
    from sentinel.longitudinal_engine import BudgetRecord

    return BudgetRecord(
        periodo     = str(d.get("periodo", "?")),
        orden       = int(d.get("orden", 0)),
        codificado  = float(d.get("codificado", 0)),
        devengado   = float(d.get("devengado", 0)),
        reformas    = float(d.get("reformas", 0)),
        grupo_gasto = str(d.get("grupo_gasto", "")),
        entidad     = str(d.get("entidad", "GAD")),
    )


def load_budget_records(
    snapshot:    Optional[dict] = None,
    series_keys: Optional[List[str]] = None,
) -> Dict[str, list]:
    """
    Carga series longitudinales del gm_snapshot → dict de BudgetRecord lists.

    Args:
        snapshot:    dict del gm_snapshot (si None, carga desde gm_loader.load())
        series_keys: lista de series a cargar (si None, carga todas las longitudinales)

    Returns:
        Dict[serie_key → list[BudgetRecord]] — ordenado por record.orden
        Retorna {} si no hay series disponibles (nunca lanza excepción).
    """
    try:
        if snapshot is None:
            from sentinel.gm_loader import load as _gm_load
            snapshot = _gm_load()

        series_data = snapshot.get("series_longitudinal", {})
        if not series_data:
            logger.warning("RC-7.4: gm_snapshot sin bloque series_longitudinal")
            return {}

        keys_to_load = series_keys if series_keys is not None else _LONGITUDINAL_SERIES
        result: Dict[str, list] = {}

        for key in keys_to_load:
            raw = series_data.get(key)
            if not raw or not isinstance(raw, list):
                continue
            try:
                records = [_record_from_dict(r) for r in raw]
                records.sort(key=lambda r: r.orden)
                result[key] = records
                logger.debug(
                    "RC-7.4: cargada serie '%s' — %d puntos (%s)",
                    key,
                    len(records),
                    ", ".join(r.periodo for r in records),
                )
            except Exception as exc:
                logger.warning("RC-7.4: error cargando serie '%s': %s", key, exc)

        return result

    except Exception as exc:
        logger.error("RC-7.4: load_budget_records falló: %s", exc)
        return {}


def get_primary_series(snapshot: Optional[dict] = None) -> list:
    """
    Devuelve la serie primaria de análisis: GAD inversión G71-78.

    Esta es la base del D3 canonical (H07b_Ti_INVERSIÓN) y la serie
    más completa y verificada del snapshot. Es la que se inyecta en
    st.session_state["rc72_budget_records"] para activar RC-7.2/7.3.

    Returns:
        list[BudgetRecord] — vacío si no disponible (nunca lanza excepción).
    """
    all_series = load_budget_records(
        snapshot=snapshot,
        series_keys=["gad_inversion_g7178"],
    )
    return all_series.get("gad_inversion_g7178", [])


def get_holding_series(snapshot: Optional[dict] = None) -> Dict[str, list]:
    """
    Devuelve series de todos los entes del Holding Municipal con datos disponibles.
    Útil para análisis multi-entidad (analyze_multi_entity).

    Returns:
        Dict[entidad → list[BudgetRecord]] — solo series con al menos 1 punto.
    """
    all_series = load_budget_records(
        snapshot=snapshot,
        series_keys=_LONGITUDINAL_SERIES,
    )
    return {k: v for k, v in all_series.items() if v}


def get_crosssection_h90(snapshot: Optional[dict] = None) -> list:
    """
    Devuelve la sección transversal H90 Q1-2026 (todos los grupos, todos los entes).

    NOTA: Esta no es una serie longitudinal — es un corte en un único período.
    No apta para analyze_series(). Útil para comparación inter-entidad puntual.

    Returns:
        list[BudgetRecord] — 4 registros (GAD, PATRONATO, EP_ASEO, BOMBEROS).
    """
    try:
        if snapshot is None:
            from sentinel.gm_loader import load as _gm_load
            snapshot = _gm_load()
        series_data = snapshot.get("series_longitudinal", {})
        raw = series_data.get("h90_holding_2026q1", [])
        return [_record_from_dict(r) for r in raw]
    except Exception as exc:
        logger.warning("RC-7.4: get_crosssection_h90 falló: %s", exc)
        return []


def summarize_available_series(snapshot: Optional[dict] = None) -> str:
    """
    Resumen textual de series disponibles — para diagnóstico, debug panel y logs.

    Returns:
        str multiline con estado de cada serie.
    """
    all_series = load_budget_records(snapshot=snapshot)
    if not all_series:
        return "RC-7.4: No hay series longitudinales disponibles en gm_snapshot.json"

    lines = [f"RC-7.4 Series disponibles: {len(all_series)} serie(s)"]
    for key, records in all_series.items():
        if not records:
            continue
        periodos = " · ".join(r.periodo for r in records)
        entidad  = records[0].entidad
        lines.append(
            f"  · {key} [{entidad}] — {len(records)} punto(s): {periodos}"
        )
    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 60)
    print("RC-7.4 Data Bridge — diagnóstico")
    print("=" * 60)

    # 1. Resumen de series disponibles
    print(summarize_available_series())
    print()

    # 2. Pipeline completo con la serie primaria
    primary = get_primary_series()
    if not primary:
        print("ERROR: serie primaria GAD G71-78 no disponible")
        sys.exit(1)

    print(f"Serie primaria: {len(primary)} puntos")
    for r in primary:
        ti_calc = (r.devengado / r.codificado * 100) if r.codificado > 0 else 0
        print(f"  [{r.orden}] {r.periodo:10s}  cod={r.codificado:>12,.0f}  "
              f"dev={r.devengado:>12,.0f}  Ti_calc={ti_calc:5.2f}%")
    print()

    # 3. Pipeline RC-7.2 + RC-7.3
    try:
        from sentinel.calibration_layer import run_full_pipeline, describe_calibrated
        result, ps, ic, binding, cr = run_full_pipeline(primary)

        print(f"Clase RC-7.2 : {ic.clase}  (confianza={ic.confianza:.2f})")
        print(f"Clase RC-7.3 : {cr.calibrated_class}  (calibrada={cr.calibrated_confidence:.2f})")
        print(f"SATs activos : {cr.sat_codes_calibrated}")
        print(f"AVEP score   : {cr.avep_score:.1f}  riesgo={cr.avep_riesgo}")
        print()
        print("Narrativa RC-7.3:")
        print(describe_calibrated(cr))
    except Exception as exc:
        print(f"ERROR pipeline: {exc}")
