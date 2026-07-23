"""
app/agents/d03/persistencia.py — Guardar resultado (etapa 4 del pipeline)
=========================================================================
Mismo contrato que d01/d02/d07: EvaluationID = Municipio+Dominio+Unidad+Periodo.
d03 es anual (RO-III-001, frecuencia: anual — el mandato se evalúa por
período, no mensualmente), a diferencia de d07 (mensual).
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .._template import persistencia as _base


def construir_resultado(municipio: str, anio: int, metricas: dict[str, Any]) -> dict[str, Any]:
    eval_id = _base.construir_evaluation_id(municipio, "d03", "IFE", anio, 1)  # anual → mes fijo
    return {
        "evaluation_id": eval_id,
        "dominio": "d03", "municipio": municipio, "periodo": f"{anio} (anual)",
        "naturaleza": "INMUTABLE — leído del Gold Master, no recalculado (Regla 1/4)",
        "incorporacion_pct": metricas["incorporacion_pct"],
        "calidad_ife_pct": metricas["calidad_ife_pct"],
        "clasificacion": metricas["calidad_clasificacion"],
        "leido_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def guardar(resultado: dict[str, Any]) -> None:
    raise NotImplementedError("Persistencia real pendiente de Fase 5 de d03.")
