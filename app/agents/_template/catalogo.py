"""
app/agents/_template/catalogo.py — Resolver de Catálogo (GENÉRICO)
=========================================================================
Idéntico en forma a `app/agents/d07/catalogo.py` — comparado con
`app/agents/d01/` para confirmar qué es realmente genérico (colega,
2026-07-23): d01 no tiene un CATALOGO_CD como d07 porque su unidad no es
CD-XX, es la cadena BRN (CNO-I-001). Por eso este resolver acepta CUALQUIER
YAML/estructura de catálogo — el DOM decide su propia forma; esto solo
la carga y la indexa.

NO es un "Agente" (sin IA). Neo4j es un índice derivado de este YAML —
nunca una segunda fuente de verdad (mismo principio que d07).
"""
from __future__ import annotations

import pathlib
from typing import Any

import yaml


def cargar(path: str | pathlib.Path) -> dict[str, Any]:
    p = pathlib.Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Catálogo no encontrado: {p}")
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def indexar_por_id(catalogo: dict[str, Any], clave_lista: str, clave_id: str = "id") -> dict[str, dict[str, Any]]:
    """clave_lista = nombre de la lista en el YAML (ej. 'conjuntos_datos' en d07,
    'eslabones' en un DOM tipo cadena). El DOM define su propia clave."""
    return {item[clave_id]: item for item in catalogo[clave_lista]}
