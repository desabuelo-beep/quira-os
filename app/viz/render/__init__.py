# -*- coding: utf-8 -*-
"""
Sistema de Visualización Canónico — capa RENDER (el contrato).
Dylus Lab © 2026 · doctrina: docs/architecture/SISTEMA_VISUALIZACION_CANONICO.md.

Cada renderer consume `list[NarrativeEvidence]` y produce una salida (figura · SVG · PDF).
El motor NUNCA se importa aquí — solo el objeto canónico. canon → datos → presentación.

Implementaciones (siguiente paso, cajón "Verificabilidad Pública del Discurso"):
  matplotlib_render.py  → PDF / informes oficiales  (⭐ control total, reproducible, Firewall)
  svg_render.py         → dashboard web
  plotly_render.py      → interactivo (futuro)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Protocol

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence import NarrativeEvidence


class Renderer(Protocol):
    """Todo renderer implementa esto. Recibe el objeto canónico, decide cómo dibujar."""

    def render(self, evidencias: list[NarrativeEvidence], **opts):
        ...
