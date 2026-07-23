"""
app/agents/d09/catalogo.py — Resolver de Catálogo (etapa 1 del pipeline)
=========================================================================
Delgado sobre `_template.catalogo`, igual que d07/d01/d02/d03. Fuente:
data/d09/catalogo_d09_v1.0.0.yaml (dominio más heterogéneo migrado: 1 índice
+ 3 hechos documentales — ver docs/pcd/PCD-D09_Rendicion_Cuentas.md).
"""
from __future__ import annotations

import pathlib
from typing import Any

from .._template import catalogo as _base

_DEFAULT = pathlib.Path("data/d09/catalogo_d09_v1.0.0.yaml")


def cargar(path: str | pathlib.Path = _DEFAULT) -> dict[str, Any]:
    return _base.cargar(path)


def indexar_metricas(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, "metricas")


def indexar_eslabones(catalogo: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {e["orden"]: e for e in catalogo["eslabones"]}
