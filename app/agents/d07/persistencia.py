"""
app/agents/d07/persistencia.py — Guardar resultado (etapa 4 del pipeline)
=========================================================================
Responsabilidad única: construir y (cuando se cablee Fase 5) persistir el
contrato de salida mensual. Determinístico, sin IA.

Refactor 2026-07-23 (Javo — retroactivo): antes NO generaba `evaluation_id`
por CD, violando el contrato definido en CATALOGO_CANONICO_CD_D07.md
("Contrato de la Evaluación mensual" — EvaluationID = Municipio+Dominio+
CD+Periodo). Corregido: cada fila de `detalle` ahora trae su propio
evaluation_id, usando `_template.persistencia` (fuente única de la clave).
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

from .._template import persistencia as _base
from .scoring import ScoreCD


def construir_resultado(dominio: str, municipio: str, anio: int, mes: int,
                         catalogo_version: str, scores: list[ScoreCD],
                         sita: dict[str, float]) -> dict[str, Any]:
    return {
        "dominio": dominio, "municipio": municipio, "periodo": f"{anio}-{mes:02d}",
        "catalogo_version": catalogo_version,
        "sita": sita,
        "detalle": [{
            "evaluation_id": _base.construir_evaluation_id(municipio, dominio, s.cd_id, anio, mes),
            "cd": s.cd_id, "sita_cd": s.sita, "cta": s.cta, "eta": s.eta,
            "rp": s.rp, "ci": s.ci, "obs": s.observaciones,
        } for s in scores],
        "generado_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def guardar(resultado: dict[str, Any]) -> None:
    """Esqueleto — persistencia real (Supabase + nodo :Evaluacion en Neo4j)
    se cablea junto con la evidencia real en Fase 5."""
    raise NotImplementedError("Persistencia real pendiente de Fase 5.")
