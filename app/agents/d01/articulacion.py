"""
app/agents/d01/articulacion.py — Alignment Agent (Fase 4, IA — corazón de d01)
=========================================================================
La pieza cognitiva central de d01. No extrae ni calcula: CRUZA e INTERPRETA
la cadena de articulación para evaluar las dos Reglas Operativas de la BRN:

    RO-I-001 (Pct_Metas_Con_Programacion):
        ¿cada meta del PDOT tiene línea en el POA? (criterios: meta_con_proyecto,
        dotacion_asignada, responsable_definido)
    RO-I-002 (Pct_Coherencia_Programacion_Contratacion):
        ¿cada línea del POA con contratación consta en el PAC/SERCOP, con
        partida coincidente? (criterios: linea_en_pac, partida_coincidente,
        publicacion_portal)

Es IA genuina porque el cruce PDOT↔POA↔PAC no es join exacto: los textos de
meta/objetivo/partida no coinciden literalmente entre instrumentos (el mismo
problema del "61% artefacto" del PCD-D01 — el POA agrega partidas a 2 dígitos,
el eSIGEF ejecuta a 6). Requiere juicio semántico, no igualdad de strings.

Distinto del IPE: el IPE (cuánto $ ejecutado se vincula a metas) YA lo calcula
el Gold Master (motor.py, determinístico). La articulación evalúa la CADENA
COMPLETA plan→programación→contratación, que el Gold Master no cubre entera.

FASE 4 — NO IMPLEMENTADO. Requiere presupuesto de API.
"""
from __future__ import annotations

from typing import Any


def evaluar_articulacion(pdot: Any, poa: Any, pac: Any) -> dict[str, Any]:
    raise NotImplementedError(
        "Fase 4 — cruce semántico PDOT↔POA↔PAC (RO-I-001, RO-I-002) pendiente "
        "de presupuesto de API. El IPE, en cambio, se lee ya (motor.leer_metricas)."
    )
