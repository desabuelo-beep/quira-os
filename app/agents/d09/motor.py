"""
app/agents/d09/motor.py — Lectura del Gold Master (etapa 3 del pipeline)
=========================================================================
d09 es el primer dominio con DOS fuentes de lectura distintas (Regla 1/4:
nunca recalcular, solo leer):

  · fidelidad_narrativa + cpccs_brecha → EN VIVO desde el Excel, envolviendo
    `scripts/enrich_rdc.py::build_block()` (mismo patrón que d01/d02/d03).
  · serie_rendiciones + cumplimiento_actual + aportes → NO viven en el
    Excel (aportes sí parte de H10c, pero el cruce es embeddings, no
    fórmula); se extraen por `scripts/enrich_rdc_docx.py` y
    `scripts/enrich_aportes.py`, que hacen I/O de archivo y MERGE directo
    al snapshot (no exponen una función pura de lectura). Se leen del
    snapshot ya persistido (`data/gm_snapshot.json['rendicion']`) —
    aceptado explícitamente así en PCD-D09 ("deriva de informes
    verificados; estampar en el Gold Master es mejora futura").

BUG ENCONTRADO Y CORREGIDO (2026-07-23, migración d09): `enrich_rdc.py`
sobrescribía TODO `snap["rendicion"]` (`snap["rendicion"] = block`), lo que
borraba `aportes`/`serie`/`cumplimiento_actual` si se re-ejecutaba solo.
Corregido a merge (`rend.update(block)`). Ver EVIDENCIA_d09_2026-07-23.md.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
from typing import Any

_ENRICHER_PATH = pathlib.Path("scripts/enrich_rdc.py")
_SNAPSHOT_PATH = pathlib.Path("data/gm_snapshot.json")


def _cargar_enricher():
    spec = importlib.util.spec_from_file_location("enrich_rdc", _ENRICHER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def leer_metricas() -> dict[str, Any]:
    mod = _cargar_enricher()
    bloque_vivo = mod.build_block()  # fidelidad (H34b) + cpccs (H31), fresco del Excel

    snap = json.loads(_SNAPSHOT_PATH.read_text(encoding="utf-8"))
    persistido = snap.get("rendicion", {})

    fid = bloque_vivo["fidelidad"]
    return {
        "status": "ok",
        "fuente_viva": "scripts/enrich_rdc.py (leído, NO recalculado — Regla 1/4)",
        "fuente_persistida": "data/gm_snapshot.json['rendicion'] (extracción DOCX, ver PCD-D09)",
        "fidelidad_naturaleza": "ÍNDICE — evaluación experta trazable, no cómputo automático",
        "fidelidad_global_pct": fid["global_pct"],
        "fidelidad_n_afirmaciones": fid["n_afirmaciones"],
        "fidelidad_n_alta": fid["n_alta"],
        "fidelidad_n_baja": fid["n_baja"],
        "fidelidad_cobertura": "ejercicio 2024 (2025 pendiente de NLP sobre video — PCD-D09)",
        "cpccs_marco_legal": bloque_vivo["cpccs"]["marco_legal"],
        "cpccs_brecha_compromisos": bloque_vivo["cpccs"]["brecha_compromisos"] or "sin dato",
        "serie_rendiciones": persistido.get("serie", []),
        "cumplimiento_actual": persistido.get("cumplimiento_actual", {}),
        "aportes_naturaleza": "HECHO — cruce semiautomático H10c×POA, evaluación experta trazable (metodología v0.3 pendiente de aval formal)",
        "aportes_total": persistido.get("aportes", {}).get("total"),
        "aportes_validados": persistido.get("aportes", {}).get("n_validados"),
        "aportes_por_estado": persistido.get("aportes", {}).get("por_estado", {}),
    }
