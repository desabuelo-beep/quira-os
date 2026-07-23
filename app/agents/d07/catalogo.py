"""
app/agents/d07/catalogo.py — Resolver de Catálogo (etapa 1 del pipeline)
=========================================================================
Responsabilidad única: cargar CATALOGO_CANONICO_CD_D07_v1.0.0.yaml.

Refactor 2026-07-23 (Javo — retroactivo, no "mejora futura"): delgado sobre
`_template.catalogo` — antes duplicaba el mismo código. El template es
ahora la fuente de la lógica genérica; d07 solo fija SU path y SU clave.

NO es un "Agente" (no hay IA ni decisión): es un módulo determinístico.
Neo4j (grafo d07) es un ÍNDICE DERIVADO de este mismo YAML para navegación
y consulta — nunca una segunda fuente de verdad. Si algo cambia, cambia
aquí primero y se regenera scripts/cypher/002_d07_transparencia.cypher.
"""
from __future__ import annotations

import pathlib
from typing import Any

from .._template import catalogo as _base

_DEFAULT = pathlib.Path("data/d07/catalogo_cd_d07_v1.0.0.yaml")
_CLAVE_LISTA = "conjuntos_datos"


def cargar(path: str | pathlib.Path = _DEFAULT) -> dict[str, Any]:
    return _base.cargar(path)


def indexar_por_id(catalogo: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return _base.indexar_por_id(catalogo, _CLAVE_LISTA)
