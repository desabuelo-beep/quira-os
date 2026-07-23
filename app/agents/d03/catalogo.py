"""
app/agents/d03/catalogo.py — Resolver de Catálogo (etapa 1 del pipeline)
=========================================================================
Delgado sobre `_template.catalogo`, igual que d07/d01/d02. Fuente:
data/d03/catalogo_d03_v1.0.0.yaml (dos métricas: incorporación=hecho,
calidad=índice — ver docs/pcd/PCD-D03_Gobernanza_Mandato.md).
"""
from __future__ import annotations

import pathlib
from typing import Any

from .._template import catalogo as _base

_DEFAULT = pathlib.Path("data/d03/catalogo_d03_v1.0.0.yaml")


def cargar(path: str | pathlib.Path = _DEFAULT) -> dict[str, Any]:
    return _base.cargar(path)


def indexar_metricas(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, "metricas")


def indexar_eslabones(catalogo: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {e["orden"]: e for e in catalogo["eslabones"]}
