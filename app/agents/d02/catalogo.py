"""
app/agents/d02/catalogo.py — Resolver de Catálogo (etapa 1 del pipeline)
=========================================================================
Delgado sobre `_template.catalogo`, igual que d07/d01. Fuente:
data/d02/catalogo_d02_v1.0.0.yaml (4 capacidades + 3 señales SAT, ver
docs/pcd/PCD-D02_Presupuesto_Financiamiento.md).
"""
from __future__ import annotations

import pathlib
from typing import Any

from .._template import catalogo as _base

_DEFAULT = pathlib.Path("data/d02/catalogo_d02_v1.0.0.yaml")


def cargar(path: str | pathlib.Path = _DEFAULT) -> dict[str, Any]:
    return _base.cargar(path)


def indexar_capacidades(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, "capacidades")


def indexar_senales(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, "senales_sat")
