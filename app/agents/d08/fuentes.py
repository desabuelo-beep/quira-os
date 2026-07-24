"""
app/agents/d08/fuentes.py — Agente de extracción documental (Fase 4, IA parcial)
=========================================================================
La participación tiene su evidencia diseminada en las actas de las instancias y
mecanismos (PP, Consejo, Cabildo, Audiencias). d08 tiene DOS extracciones:

  · Determinística (sin IA, hoy): presencia y formalización — ¿el documento existe?
    ¿consta la RESOLUCIÓN (audiencia/consejo)? Es texto plano sobre los procesables.
  · Agéntica (Fase 4, requiere API): interpretar los APORTES ciudadanos emanados de
    cada acta y contrastarlos contra la ejecución (POA/PAC/presupuesto) — dimensión
    efectividad (RO-VIII-003). Motor propio de d08, NO enrich_aportes.py (que es de d09).

Además, 16 actas de audiencia están ESCANEADAS → OCR certificado (Javo las extrae).

FASE 4 (interpretación de aportes) — NO IMPLEMENTADO. Requiere presupuesto de API.
"""
from __future__ import annotations

import pathlib
import re
from typing import Any

_CARPETA = pathlib.Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi\Participación Ciudadana")
_RE_RESOLUCION = re.compile(r"\bresoluci[oó]n\b", re.IGNORECASE)


def verificar_formalizacion(texto: str) -> bool:
    """Determinístico (hoy): ¿el acta menciona una RESOLUCIÓN? (LOPC 75 / COPLAFIP 29).
    Señal débil de formalización — la verificación plena es Fase 4 (interpretar el acto)."""
    return bool(_RE_RESOLUCION.search(texto or ""))


def extraer_aportes_de_acta(ruta_acta: str, mecanismo: str) -> Any:
    raise NotImplementedError(
        f"Fase 4 — interpretar los aportes ciudadanos del acta '{ruta_acta}' (mecanismo {mecanismo}) "
        "y contrastarlos contra la ejecución (POA/PAC/presupuesto). Motor propio de d08. "
        "Pendiente de presupuesto de API."
    )
