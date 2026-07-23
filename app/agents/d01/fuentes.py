"""
app/agents/d01/fuentes.py — Agentes de extracción de fuentes (Fase 4, IA)
=========================================================================
La cadena de articulación de d01 se arma de fuentes que viven en sitios
distintos — cada una necesita un agente con juicio propio:

    PDOT Agent    → web del GAD (documento largo, formato variable por GAD)
    POA Agent     → web del GAD (programación operativa anual)
    PAC Agent     → portal SERCOP / web del GAD (plan anual de contratación)
    SERCOP Agent  → portal de compras públicas (contratación REAL ejecutada;
                    navegación + lectura de procesos, no un simple fetch)
    Budget Agent  → cédula presupuestaria del portal de transparencia DPE
                    = MISMA fuente que d07 CD-06 (reuso, no re-extraer:
                    el grafo relaciona Fuente 'Presupuesto' -MISMA_FUENTE_QUE-> CD-06)

Reusa extractores ya existentes donde los hay:
    scripts/motor_narrativo/extract_cedula_xls.py  (cédula)
    scripts/motor_narrativo/extract_pac_docx.py    (PAC)

FASE 4 — NO IMPLEMENTADO. Requiere presupuesto de API (Haiku) + navegador.
"""
from __future__ import annotations

from typing import Any


def extraer_fuente(fuente_id: str, municipio: str, anio: int) -> dict[str, Any]:
    raise NotImplementedError(
        f"Fase 4 — extracción de '{fuente_id}' pendiente de presupuesto de API. "
        "Budget/Presupuesto NO se re-extrae: se reusa la evidencia de d07 CD-06."
    )
