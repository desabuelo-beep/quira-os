"""
app/connectors/cpccs.py — QUIRA OS · Sprint 1
Conector institucional: CPCCS — Rendición de Cuentas

Puente entre el pipeline y scripts/fetch_rdc_cpccs.py.
Expone la interfaz canónica que consume snapshot_pipeline.py.

Doctrina dual:
  Componente A (CPCCS portal)  — declaración institucional verificable
  Componente B (redes sociales) — evidencia performativa independiente
  CPCCS ≠ Rendición de cuentas real: A + B = señal útil

Fuente A: rendiciondecuentas.cpccs.gob.ec
Fuente B: YouTube/Facebook oficial GAD (verificación manual o YouTube API v3)
Dylus Lab © 2026
"""
from __future__ import annotations

import logging
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

SOURCE_ID   = "cpccs"
RELIABILITY = 0.80   # auto-declarativo — menor que DPE/SERCOP


def fetch_rdc_cpccs(
    ruc: str,
    year: int | None = None,
    nombre_municipio: str = "",
) -> dict:
    """Obtiene el bloque de Rendición de Cuentas (RdC) desde CPCCS + redes.

    Args:
        ruc:               RUC de 13 dígitos del municipio.
        year:              Año rendido (default: año anterior al actual).
        nombre_municipio:  Nombre oficial para instrucciones Componente B.

    Returns:
        dict con claves:
            status:       "ok" | "partial" | "failed"
            source_id:    "cpccs"
            reliability:  float (0-1) — 0.80 si A disponible, ajustado si pendiente
            data:         dict accountability.rdc completo
            error:        str | None
    """
    year = year or (date.today().year - 1)

    result: dict[str, Any] = {
        "status":      "pending",
        "source_id":   SOURCE_ID,
        "reliability": RELIABILITY,
        "data":        {},
        "error":       None,
    }

    try:
        from scripts.fetch_rdc_cpccs import build_accountability_block

        block = build_accountability_block(ruc, year, nombre_municipio)
        rdc   = block.get("accountability", {}).get("rdc", {})

        result["data"] = rdc

        comp_a = rdc.get("componente_a", {})
        if comp_a.get("n_informe_cpccs"):
            result["status"]      = "ok"
            result["reliability"] = round(RELIABILITY, 3)
        elif comp_a.get("portal_url_manual"):
            # API CPCCS no respondió — requiere verificación manual
            result["status"]      = "partial"
            result["reliability"] = round(RELIABILITY * 0.3, 3)
        else:
            result["status"]      = "partial"
            result["reliability"] = round(RELIABILITY * 0.2, 3)

        score_total = rdc.get("score_total", 0)
        logger.info(f"[CPCCS] RUC {ruc} año {year} — score RdC: {score_total}/100 — status: {result['status']}")

    except Exception as exc:
        logger.error(f"[CPCCS] Error fetching RUC {ruc}: {exc}")
        result["status"]      = "failed"
        result["error"]       = str(exc)
        result["reliability"] = 0.0

    return result
