"""
app/agents/d02/fuentes.py — Agente de extracción (Fase 4, IA — pieza mínima)
=========================================================================
A diferencia de d07/d01, la mayor parte de d02 ya vive resuelta en el
Gold Master (motor.py la lee). La única pieza genuinamente agéntica
identificada en el PCD-D02: el último eslabón de la "biografía del
capital" (ODS→Plan Nacional→Meta PDOT→Convenio→Capital→Contrato→
Devengado→Resultado) — el nodo "Resultado" está en rojo porque el
municipio no publica medición de impacto. Verificar si eso cambió
requiere revisar la web del GAD/transparencia — Portal Navigator +
Evidence Interpreter (mismo molde que d07/d01), no un agente nuevo.

FASE 4 — NO IMPLEMENTADO. Requiere presupuesto de API.
"""
from __future__ import annotations

from typing import Any


def verificar_medicion_resultados(municipio: str, anio: int) -> Any:
    raise NotImplementedError(
        "Fase 4 — verificar si el GAD publicó medición de impacto/resultado "
        "(PCD-D02: ausencia declarada, no rellenada). Pendiente de presupuesto de API."
    )
