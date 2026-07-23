"""
app/agents/_template/fuentes.py — Agentes de extracción (GENÉRICO, stub)
=========================================================================
Portal Navigator + Evidence Collector + Evidence Interpreter (colega,
2026-07-22): localizar, descargar, juzgar. Genéricos en FORMA — el DOM
específico define QUÉ portal, QUÉ formato, QUÉ criterios de juicio (eso
vive en el catalogo.py del DOM, no aquí).

FASE 4 de cada DOM — NO IMPLEMENTADO hasta que exista presupuesto de API.
Ver `app/agents/d07/evidencia.py` para la instancia ya razonada de este
mismo molde.
"""
from __future__ import annotations

from typing import Any


def extraer_evidencia(unidad_id: str, municipio: str, anio: int, mes: int) -> Any:
    raise NotImplementedError(
        f"Fase 4 — extracción de '{unidad_id}' pendiente de presupuesto de API."
    )
