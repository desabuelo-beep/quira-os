"""
app/agents/d01/catalogo.py — Resolver de Catálogo (etapa 1 del pipeline)
=========================================================================
Faltaba (Javo, 2026-07-23 — corrección retroactiva): el grafo de d01
(scripts/cypher/003_d01_planificacion.cypher) se generó desde un script
Python con datos inline, sin YAML intermedio — rompía el principio "Neo4j
deriva del catálogo, nunca al revés" que sí se respetó en d07. Corregido:
ahora existe `data/d01/catalogo_d01_v1.0.0.yaml` como fuente única; este
módulo la carga, igual que d07/catalogo.py, delgado sobre `_template`.
"""
from __future__ import annotations

import pathlib
from typing import Any

from .._template import catalogo as _base

_DEFAULT = pathlib.Path("data/d01/catalogo_d01_v1.0.0.yaml")


def cargar(path: str | pathlib.Path = _DEFAULT) -> dict[str, Any]:
    return _base.cargar(path)


def indexar_eslabones(catalogo: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {e["orden"]: e for e in catalogo["eslabones"]}


def indexar_ro(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, "reglas_operativas")


def indexar_fuentes(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, "fuentes")
