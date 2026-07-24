"""
app/agents/d08/persistencia.py — Guardar resultado (etapa 4 del pipeline)
=========================================================================
Mismo contrato que d01/d02/d03/d07/d09: EvaluationID = Municipio+Dominio+Unidad+Periodo.
d08 es anual (RO-VIII-*, frecuencia: anual). La Unidad es el mecanismo/instancia
(hay varios en el dominio), por eso el resultado se estructura por instancia.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .._template import persistencia as _base


def construir_resultado(municipio: str, anio: int, integridad: dict[str, Any], igp: dict[str, Any]) -> dict[str, Any]:
    eval_id = _base.construir_evaluation_id(municipio, "d08", "SISTEMA_PARTICIPACION", anio, 1)  # anual → mes fijo
    return {
        "evaluation_id": eval_id,
        "dominio": "d08", "municipio": municipio, "periodo": f"{anio} (anual)",
        "naturaleza": "verificabilidad documental (integridad) + IGP leído en diagnóstico (Regla 1/4)",
        "integridad_normativa": integridad["senales"],
        "igp_diagnostico": {
            "global": igp.get("igp_global"),
            "naturaleza": igp.get("naturaleza"),
            "hallazgos": igp.get("hallazgos_obs"),
        },
        "dimensiones_pendientes": {
            "vitalidad_democratica": "RO-VIII-002 · índice a sellar en el Gold Master",
            "efectividad_incidencia": "RO-VIII-003 · motor de extracción de aportes de participación pendiente",
        },
        "leido_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def guardar(resultado: dict[str, Any]) -> None:
    raise NotImplementedError("Persistencia real pendiente de cierre de d08.")
