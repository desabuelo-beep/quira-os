"""
app/agents/d07/reportes.py — Report Generator (etapa agéntica final)
=========================================================================
Genuinamente IA (colega, 2026-07-22): convertir un score + evidencia en
narrativa explicable (Regla de Oro 2 — lenguaje de administración pública,
nunca acusatorio) es juicio, no plantilla de texto. Distinto de
`persistencia.construir_resultado`, que solo estructura datos.

FASE 5 — NO IMPLEMENTADO. Requiere presupuesto de API.
"""
from __future__ import annotations

from .scoring import ScoreCD


def redactar_observacion(score: ScoreCD) -> str:
    raise NotImplementedError("Fase 5 — redacción narrativa pendiente de presupuesto de API.")
