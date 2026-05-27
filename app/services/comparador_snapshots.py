# -*- coding: utf-8 -*-
"""
app/services/comparador_snapshots.py — QUIRA Intelligence
Alias semántico español de snapshot_diff.py

Transición gradual al español (Sprint 3 Semana 4).
Los módulos nuevos importan desde aquí; el original se mantiene
como fuente canónica hasta que todos los imports migren.

Doctrina: docs/ARQUITECTURA_CANONICA.md — Sección 6 (Deprecaciones y Renombramientos)
Dylus Lab © 2026 — QUIRA Intelligence
"""
from app.services.snapshot_diff import (  # noqa: F401 — reexportación semántica
    compare_snapshots,
    DiffResult,
    detect_reincidence_from_history,
)

__all__ = [
    "compare_snapshots",
    "DiffResult",
    "detect_reincidence_from_history",
]
