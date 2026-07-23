"""
app/agents/d09/persistencia.py — Guardar resultado (etapa 4 del pipeline)
=========================================================================
Mismo contrato que d01/d02/d03/d07: EvaluationID = Municipio+Dominio+Unidad+Periodo.
d09 es anual (RO-IX-001, frecuencia: anual — un ciclo por período fiscal),
igual que d03.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .._template import persistencia as _base


def construir_resultado(municipio: str, anio: int, metricas: dict[str, Any]) -> dict[str, Any]:
    eval_id = _base.construir_evaluation_id(municipio, "d09", "RDC", anio, 1)  # anual → mes fijo
    return {
        "evaluation_id": eval_id,
        "dominio": "d09", "municipio": municipio, "periodo": f"{anio} (anual)",
        "naturaleza": "MIXTA — fidelidad/cpccs leídas del Gold Master; serie/cumplimiento del DOCX persistido (Regla 1/4)",
        "fidelidad_global_pct": metricas["fidelidad_global_pct"],
        "cpccs_brecha_compromisos": metricas["cpccs_brecha_compromisos"],
        "serie_periodos": [s.get("periodo") for s in metricas["serie_rendiciones"]],
        "cumplimiento_n_componentes": len(metricas["cumplimiento_actual"].get("componentes", [])),
        "aportes_total": metricas.get("aportes_total"),
        "aportes_validados": metricas.get("aportes_validados"),
        "leido_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def guardar(resultado: dict[str, Any]) -> None:
    raise NotImplementedError("Persistencia real pendiente de Fase 5 de d09.")
