"""
app/agents/d01/persistencia.py — Guardar resultado (etapa 4 del pipeline)
=========================================================================
Faltaba (Javo, 2026-07-23 — corrección retroactiva, no "mejora futura"):
d01 tenía motor/fuentes/articulacion pero ningún módulo de persistencia,
a diferencia de d07. Se corrige ahora, alineado al mismo contrato
(EvaluationID = Municipio+Dominio+Unidad+Periodo, `_template.persistencia`).

Unidad de d01 = **RO** (RO-I-001, RO-I-002), no CD-XX (eso es de d07) — la
BRN define la cadena por Reglas Operativas, no por conjuntos de datos.
La métrica del motor (IPE) es un caso aparte: no es mensual como las RO
(se lee del Gold Master, anual/vigente), se persiste sin `evaluation_id`
de periodo mensual.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .._template import persistencia as _base


def construir_resultado_ro(municipio: str, anio: int, mes: int,
                            hallazgos_ro: list[dict[str, Any]]) -> dict[str, Any]:
    """hallazgos_ro: salida de articulacion.evaluar_articulacion (Fase 4) —
    cada item con al menos {'ro_id': 'RO-I-001', 'pct': float, 'obs': [...]}."""
    detalle = [{
        "evaluation_id": _base.construir_evaluation_id(municipio, "d01", h["ro_id"], anio, mes),
        **h,
    } for h in hallazgos_ro]
    return _base.construir_resultado("d01", municipio, anio, mes,
                                      catalogo_version="CNO-I-001 v1.0",
                                      detalle=detalle, agregado={})


def construir_resultado_metrica(municipio: str, metricas: dict[str, Any]) -> dict[str, Any]:
    """Para motor.leer_metricas() — NO es mensual (Gold Master vigente), sin
    evaluation_id de periodo; se marca con la fecha de lectura."""
    return {
        "dominio": "d01", "municipio": municipio,
        "naturaleza": "INMUTABLE — leído del Gold Master, no recalculado (Regla 1/4)",
        "metricas": metricas,
        "leido_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def guardar(resultado: dict[str, Any]) -> None:
    raise NotImplementedError("Persistencia real pendiente de Fase 5 de d01.")
