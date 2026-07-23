"""
app/agents/d09/fuentes.py — Agente de extracción (Fase 4, IA — pieza mínima)
=========================================================================
RO-IX-001 exige verificación DOCUMENTAL de 3 criterios obligatorios
(informe_presentado, contenido_minimo, deliberacion_publica) más 1 opcional
(fidelidad_narrativa). motor.py ya lee los hechos crudos (serie, cpccs,
fidelidad 2024); lo que falta es el JUICIO que contrasta esos hechos contra
el contenido mínimo oficial (Reglamento Art.10) y, para 2025, el NLP sobre
el video de la rendición (el diferenciador — pendiente honesto de PCD-D09).
Mismo molde Portal Navigator + Evidence Interpreter que d01/d02/d03/d07.

FASE 4 — NO IMPLEMENTADO. Requiere presupuesto de API.
"""
from __future__ import annotations

from typing import Any


def verificar_contenido_minimo(informe_n: str, n_componentes: int) -> Any:
    raise NotImplementedError(
        f"Fase 4 — contraste del informe N°{informe_n} ({n_componentes} componentes) "
        "contra el contenido mínimo oficial (Reglamento CPCCS Art.10). "
        "Pendiente de presupuesto de API."
    )


def extraer_fidelidad_narrativa_video(anio: int) -> Any:
    raise NotImplementedError(
        f"Fase 4 — NLP sobre el video de la rendición {anio} (afirmación por afirmación, "
        "el diferenciador RDC). Pendiente de presupuesto de API — PCD-D09 §Pendientes honestos."
    )
