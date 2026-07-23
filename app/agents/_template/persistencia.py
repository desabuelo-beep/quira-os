"""
app/agents/_template/persistencia.py — Guardar resultado (GENÉRICO)
=========================================================================
Clave lógica única para TODO QUIRA (colega, 2026-07-22 — mensualización):

    EvaluationID = Municipio + Dominio + Unidad + Periodo(AAAA-MM)

'Unidad' es CD-XX en d07, un eslabón/RO en d01, lo que defina cada DOM —
el contrato exige la clave, no el nombre del campo. Determinístico, sin IA.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any


def construir_evaluation_id(municipio: str, dominio: str, unidad: str, anio: int, mes: int) -> str:
    return f"{municipio}|{dominio}|{unidad}|{anio}-{mes:02d}"


def construir_resultado(dominio: str, municipio: str, anio: int, mes: int,
                         catalogo_version: str, detalle: list[dict[str, Any]],
                         agregado: dict[str, Any]) -> dict[str, Any]:
    return {
        "dominio": dominio, "municipio": municipio, "periodo": f"{anio}-{mes:02d}",
        "catalogo_version": catalogo_version,
        "agregado": agregado,
        "detalle": detalle,
        "generado_at": _dt.datetime.now().isoformat(timespec="seconds"),
    }


def guardar(resultado: dict[str, Any]) -> None:
    """Esqueleto — cada DOM cablea su propio destino (Supabase + nodo
    :Evaluacion en Neo4j) cuando llegue su Fase 5."""
    raise NotImplementedError("Persistencia real pendiente de Fase 5 del DOM correspondiente.")
