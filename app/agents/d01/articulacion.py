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

────────────────────────────────────────────────────────────────────────────
OBSERVACIÓN DE JAVO (2026-08-26) · LA PREGUNTA QUE ESTAS RO NO HACEN
────────────────────────────────────────────────────────────────────────────
> *«Cuando esa cadena se rompe o se invierte —**cuando el pliego precede a la
> necesidad**— tienes una señal que ningún portal de transparencia captura hoy.»*

Se comprobó contra `RO-I-001` y `RO-I-002`: **ninguna pregunta por el orden.**
Preguntan CORRESPONDENCIA —¿existe la meta en el POA? ¿existe la línea en el
PAC?— y no PRECEDENCIA. Los dos «antes de» que aparecen en las RO son otra
cosa: el plazo del COOTAD Art. 233 y el momento en que se emite la señal.

    RO-I-001/002   ¿está?          ← correspondencia
    la observación ¿qué vino antes? ← precedencia

**Por qué no se implementa aquí y ahora**, aunque el hueco sea real:

  · La precedencia sólo tiene sentido sobre pares YA emparejados: para decir
    «este pliego precede a esta necesidad» hay que saber primero que ambos se
    refieren a lo mismo — y ese emparejamiento es justo el cruce semántico que
    esta Fase 4 tiene bloqueado por presupuesto de API.
  · Hay una versión DÉBIL que sí sería determinística —un instrumento posterior
    sin instrumento previo que lo sostenga— pero no está medida y no debe
    construirse dentro del piloto de d01 (ADR-053: el piloto demuestra el
    molde, no crece).

**Y el límite epistemológico, que es lo que hace utilizable la señal:** lo
verificable es *«no encuentro evidencia que conecte esta especificación con una
necesidad previamente declarada»*. NO *«hubo captura del pliego»*. La primera es
una afirmación sobre la cadena; la segunda infiere intención, y QUIRA certifica
verificabilidad, no verdad (`ADR-043 §4`).
"""
from __future__ import annotations

from typing import Any


def evaluar_articulacion(pdot: Any, poa: Any, pac: Any) -> dict[str, Any]:
    raise NotImplementedError(
        "Fase 4 — cruce semántico PDOT↔POA↔PAC (RO-I-001, RO-I-002) pendiente "
        "de presupuesto de API. El IPE, en cambio, se lee ya (motor.leer_metricas)."
    )
