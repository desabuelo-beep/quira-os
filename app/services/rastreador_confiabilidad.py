# -*- coding: utf-8 -*-
"""
app/services/rastreador_confiabilidad.py — QUIRA Intelligence
Alias semántico español de reliability_tracker.py

Transición gradual al español (Sprint 3 Semana 4).
Los módulos nuevos importan desde aquí; el original se mantiene
como fuente canónica hasta que todos los imports migren.

Doctrina: docs/ARQUITECTURA_CANONICA.md — Sección 6 (Deprecaciones y Renombramientos)
Dylus Lab © 2026 — QUIRA Intelligence
"""
from app.services.reliability_tracker import (  # noqa: F401 — reexportación semántica
    get_reliability_dashboard,
    get_reliability_history,
    get_traceability_trend,
    get_source_health,
    build_reliability_report,
)

__all__ = [
    "get_reliability_dashboard",
    "get_reliability_history",
    "get_traceability_trend",
    "get_source_health",
    "build_reliability_report",
]
