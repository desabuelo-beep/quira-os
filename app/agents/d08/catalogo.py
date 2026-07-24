"""
app/agents/d08/catalogo.py — Resolver de Catálogo (etapa 1 del pipeline)
=========================================================================
Delgado sobre `_template.catalogo`, igual que d07/d01/d02/d03/d09. Fuente:
data/d08/catalogo_d08_v1.0.0.yaml (dominio más rico institucionalmente:
familia CNO-VIII de 8 CNO jerárquicas + 3 dimensiones — ver docs/brn/CNO-VIII-*).
"""
from __future__ import annotations

import pathlib
from typing import Any

from .._template import catalogo as _base

_DEFAULT = pathlib.Path("data/d08/catalogo_d08_v1.0.0.yaml")


def cargar(path: str | pathlib.Path = _DEFAULT) -> dict[str, Any]:
    return _base.cargar(path)


def indexar_instancias(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Indexa las instancias/mecanismos por su id de CNO (CNO-VIII-001..007)."""
    return {i["cno"]: i for i in catalogo["instancias"]}


def indexar_por_mecanismo(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {i["mecanismo"]: i for i in catalogo["instancias"]}
