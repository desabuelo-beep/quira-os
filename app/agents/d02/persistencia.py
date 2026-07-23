"""
app/agents/d02/persistencia.py — Guardar resultado (etapa 4 del pipeline)
=========================================================================
Mismo contrato que d01/d07: EvaluationID = Municipio+Dominio+Unidad+Periodo.
Unidad de d02 = capacidad (sostenibilidad/absorcion/movilizacion/elegibilidad)
o señal SAT — no CD-XX (eso es d07) ni RO (eso es d01 puro).
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .._template import persistencia as _base


def construir_resultado_capacidades(municipio: str, metricas: dict[str, Any]) -> dict[str, Any]:
    """Para motor.leer_metricas() — capacidades financieras, no mensuales por CD
    (el Gold Master las trae vigentes al corte, no por mes histórico aún)."""
    return {
        "dominio": "d02", "municipio": municipio,
        "naturaleza": "INMUTABLE — leído del Gold Master, no recalculado (Regla 1/4)",
        "capacidades": {
            "sostenibilidad_isp_pct": metricas["sostenibilidad_isp_pct"],
            "absorcion_ti_pct": metricas["absorcion_ti_pct"],
            "movilizacion_usd": metricas["movilizacion_usd"],
            "elegibilidad_pnd_pct": metricas["elegibilidad_pnd_pct"],
        },
        "leido_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def construir_resultado_sat(municipio: str, anio: int, mes: int, senales: list[dict[str, Any]]) -> dict[str, Any]:
    detalle = [{
        "evaluation_id": _base.construir_evaluation_id(municipio, "d02", s["nombre"].replace(" ", "_"), anio, mes),
        **s,
    } for s in senales]
    return _base.construir_resultado("d02", municipio, anio, mes,
                                      catalogo_version="CATALOGO_D02_PRESUPUESTO_v1.0.0",
                                      detalle=detalle, agregado={})


def guardar(resultado: dict[str, Any]) -> None:
    raise NotImplementedError("Persistencia real pendiente de Fase 5 de d02.")
