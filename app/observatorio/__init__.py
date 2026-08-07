"""
QUIRA — Observatorio · capa de adquisición de evidencia (ADR-042)

El Observatorio es la **función** institucional de vigilancia; este paquete
contiene la lógica que la ejecuta. La Consola de Monitoreo
(`quira_pages/p_monitoreo_fuentes.py`) es su superficie de operación.

Dylus Lab © 2026
"""
from app.observatorio.estados import (            # noqa: F401
    Estado, EstadoNoPublicable, Semantica,
    afirma_sobre_sujeto, clasificar, color, es_publicable,
    exigir_publicable, resumen, semantica,
    NO_ES_HALLAZGO, TERMINALES,
)

__all__ = [
    "Estado", "EstadoNoPublicable", "Semantica",
    "afirma_sobre_sujeto", "clasificar", "color", "es_publicable",
    "exigir_publicable", "resumen", "semantica",
    "NO_ES_HALLAZGO", "TERMINALES",
]
