"""
app/agents/d03/fuentes.py — Agente de extracción (Fase 4, IA — pieza mínima)
=========================================================================
Igual que d02, la mayor parte de d03 ya vive resuelta y curada en el
Gold Master (motor.py la lee). La pieza agéntica real identificada en el
PCD-D03: contrastar promesas pendientes de verificación contra el
documento oficial del CNE (trazabilidad documental — RO-III-001 lo exige
como criterio obligatorio), y mantener actualizado el registro de
autoridades electas (SCHEMA_CNE). Mismo molde Portal Navigator +
Evidence Interpreter que d01/d02/d07 — no un agente nuevo.

FASE 4 — NO IMPLEMENTADO. Requiere presupuesto de API.
"""
from __future__ import annotations

from typing import Any


def contrastar_promesa_documento(promesa_id: str, plan_cne_path: str) -> Any:
    raise NotImplementedError(
        f"Fase 4 — contraste documental de '{promesa_id}' contra el Plan CNE original. "
        "Pendiente de presupuesto de API."
    )
