# -*- coding: utf-8 -*-
"""
scripts/brn_ro_adapter.py — BRN v2 · ROAdapter (contrato estable RO → modelo interno)
═══════════════════════════════════════════════════════════════════════════════════
El adaptador formal que pidió el colega (2026-07-18). Es el ÚNICO componente que conoce la
estructura YAML de una RO. Todo lo demás (compilador, catálogo) consume el MODELO INTERNO
estable (ROModel), nunca el diccionario crudo.

    RO YAML  →  [ ROAdapter ]  →  ROModel (estable)  →  compilador · catálogo

Si en BRN v3 cambian las claves (`metrica.nombre` → `metric.name`), **solo cambia este archivo**;
el compilador y el catálogo permanecen intactos. Ese es el criterio de generalidad real (matiz del
colega): la lógica aguas abajo no se toca al evolucionar el formato ni al añadir dominios.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field

# VERSIÓN DEL CONTRATO INTERNO (colega · 2026-07-20) — independiente del formato YAML externo y del
# artifact_schema. Un YAML de RO v3 puede seguir traduciéndose a ROModel 2.0 sin tocar el compilador:
# esa es la fuerza de la frontera. Solo sube si cambia la FORMA del modelo interno (romper aguas abajo).
CONTRATO_VERSION = "2.0"


@dataclass(frozen=True)
class Tramo:
    """Un tramo de vigencia operativa (§4b). Un umbral plano es un tramo sin fechas."""
    desde: str | None
    hasta: str | None
    umbral: float | None


@dataclass(frozen=True)
class ROModel:
    """Modelo interno ESTABLE de una Regla Operativa. Contrato aguas abajo — no cambia aunque
    cambie el YAML. Los tramos unifican `vigencia_operativa` y el `umbral` plano en una sola forma."""
    id: str
    version: str | None
    cno_id: str                     # normalizado desde `deriva_de` ("CNO-IV-001 v1.0" → "CNO-IV-001")
    metrica: str | None             # qué se mide
    unidad: str | None
    frecuencia: str | None
    tramos: tuple[Tramo, ...]       # SIEMPRE ≥1; el runtime elige por fecha
    metodo: dict | None             # algoritmo conceptual (no ejecución)
    consume: tuple[str, ...]        # a quién alimenta (nunca el motor)
    opera_en: str | None
    estado: str


def adaptar(ro: dict) -> ROModel:
    """Traduce una RO cruda (YAML→dict) al modelo interno estable. ÚNICO punto que conoce las
    claves del YAML de la RO."""
    m = ro.get("metrica") or {}
    p = ro.get("parametros") or {}
    vo = p.get("vigencia_operativa")
    if vo:
        tramos = tuple(Tramo(t.get("desde"), t.get("hasta"), t.get("umbral")) for t in vo)
    else:
        tramos = (Tramo(None, None, p.get("umbral")),)   # umbral plano = un tramo sin fechas
    return ROModel(
        id=ro.get("id"),
        version=ro.get("version"),
        cno_id=str(ro.get("deriva_de", "")).split()[0] if ro.get("deriva_de") else "",
        metrica=m.get("nombre"),
        unidad=m.get("unidad"),
        frecuencia=p.get("frecuencia"),
        tramos=tramos,
        metodo=ro.get("metodo"),
        consume=tuple(ro.get("consume") or []),
        opera_en=ro.get("opera_en"),
        estado=ro.get("estado", "propuesta"),
    )


def umbral_en(model: ROModel, fecha: str) -> float | None:
    """Resuelve el umbral del tramo vigente a una fecha (esto lo hace el RUNTIME, no el compilador).
    Si hay solape, gana el último tramo cuyo rango contiene la fecha (orden cronológico)."""
    vig = None
    for t in model.tramos:
        d = t.desde or "0000-00-00"
        h = t.hasta or "9999-12-31"
        if d <= fecha <= h:
            vig = t.umbral
    return vig if vig is not None else (model.tramos[0].umbral if model.tramos else None)
