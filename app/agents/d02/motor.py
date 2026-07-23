"""
app/agents/d02/motor.py — Lectura del motor (NO recálculo)
=========================================================================
Responsabilidad única: LEER las 4 capacidades + 3 señales SAT de d02 del
Gold Master. Envuelve `scripts/enrich_presupuesto.py` — el enricher YA
existe, YA está en producción, YA corrige el bug histórico del PCD-D02
(ISP leído de la columna correcta). Este módulo NO reimplementa esa
lógica — la importa (Regla 7: no duplicar lo que ya existe).

REGLA 1/4 (inviolables): ISP, Ti, fondos externos y las 3 señales SAT las
calcula el Gold Master. Este módulo nunca recalcula — solo lee.
"""
from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

_ENRICHER_PATH = pathlib.Path("scripts/enrich_presupuesto.py")


def _cargar_enricher():
    spec = importlib.util.spec_from_file_location("enrich_presupuesto", _ENRICHER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def leer_metricas() -> dict[str, Any]:
    """Lee (no calcula) las 4 capacidades + 3 señales SAT vía el enricher real."""
    mod = _cargar_enricher()
    bloque = mod.build_block()
    return {
        "status": "ok",
        "fuente": "scripts/enrich_presupuesto.py (leído, NO recalculado — Regla 1/4)",
        "naturaleza": "INMUTABLE",
        "sostenibilidad_isp_pct": bloque["isp"]["global_pct"],
        "absorcion_ti_pct": bloque["ejecucion"]["ti_pct"],
        "movilizacion_usd": bloque["captacion"]["total_externo"],
        "movilizacion_n_convenios": bloque["captacion"]["n_convenios"],
        "elegibilidad_pnd_pct": bloque["elegibilidad"]["alineacion_pnd_pct"],
        "elegibilidad_icods_pct": bloque["ods"]["icods_pct"],
        "sat_senales": bloque["sat_presupuestario"]["senales"],
        "sat_n_activas": bloque["sat_presupuestario"]["n_activas"],
    }
