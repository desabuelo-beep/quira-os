"""
app/agents/d03/motor.py — Lectura del motor (NO recálculo)
=========================================================================
Responsabilidad única: LEER incorporación + calidad (IFE) + señal SAT-III
de d03 del Gold Master. Envuelve `scripts/enrich_mandato.py` — el
enricher YA existe, YA está en producción, YA absorbió la curación del
canon (PCD-D03: rótulo corregido, estado de verificación como dato,
Clasificación_IFE como fórmula viva). Este módulo NO reimplementa esa
lógica — la importa (Regla 7).

REGLA 1/4: el IFE, el conteo de incorporación y el centinela los calcula
el Gold Master / el enricher curado. Este módulo nunca recalcula.
"""
from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

_ENRICHER_PATH = pathlib.Path("scripts/enrich_mandato.py")


def _cargar_enricher():
    spec = importlib.util.spec_from_file_location("enrich_mandato", _ENRICHER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def leer_metricas() -> dict[str, Any]:
    """Lee (no calcula) incorporación + calidad + auditoría del canon."""
    mod = _cargar_enricher()
    bloque = mod.build_block()
    return {
        "status": "ok",
        "fuente": "scripts/enrich_mandato.py (leído, NO recalculado — Regla 1/4)",
        "naturaleza": "INMUTABLE",
        "incorporacion_pct": bloque["incorporacion"]["pct"],
        "incorporacion_total": bloque["incorporacion"]["total"],
        "incorporacion_con_meta": bloque["incorporacion"]["con_meta"],
        "incorporacion_pct_verificado": bloque["incorporacion"]["pct_verificado"],
        "calidad_ife_pct": bloque["calidad"]["pct"],
        "calidad_clasificacion": bloque["calidad"]["clasificacion"],
        "auditoria_canon_coherente": bloque["auditoria_canon"]["coherente"],
        "autoridades_sin_verificar": bloque["autoridades"]["sin_verificar"],
        "autoridades_total": bloque["autoridades"]["total"],
    }
