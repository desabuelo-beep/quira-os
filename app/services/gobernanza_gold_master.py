# -*- coding: utf-8 -*-
"""
app/services/gobernanza_gold_master.py — QUIRA Intelligence
Alias semántico español de gold_master_governance.py

Transición gradual al español (Sprint 3 Semana 4).
Los módulos nuevos importan desde aquí; el original se mantiene
como fuente canónica hasta que todos los imports migren.

Doctrina: docs/ARQUITECTURA_CANONICA.md — Sección 6 (Deprecaciones y Renombramientos)
Dylus Lab © 2026 — QUIRA Intelligence
"""
from app.services.gold_master_governance import (  # noqa: F401 — reexportación semántica
    validar_gold_master,
    obtener_changelog_gm,
    respaldar_gold_master,
    obtener_estado_gm,
)

__all__ = [
    "validar_gold_master",
    "obtener_changelog_gm",
    "respaldar_gold_master",
    "obtener_estado_gm",
]
