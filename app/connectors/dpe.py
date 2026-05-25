"""
app/connectors/dpe.py — QUIRA OS · Sprint 1
Conector institucional: Portal Nacional de Transparencia (DPE)

Puente entre el pipeline y scripts/_generate_snapshot_dpe.py.
La lógica de adquisición vive en scripts/; este módulo expone la interfaz
canónica que consume snapshot_pipeline.py.

Doctrina: DPE es API pública parcialmente expuesta. Playwright = fallback, no núcleo.

Fuente: api.transparencia.dpe.gob.ec/backend/v1/
Dylus Lab © 2026
"""
from __future__ import annotations

import logging
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ── Agregar raíz al path ──────────────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

# Source reliability weight (config.py)
SOURCE_ID = "dpe"
RELIABILITY = 0.95


def fetch_dpe_data(
    ruc: str,
    establishment_id: int | None = None,
    year: int | None = None,
) -> dict:
    """Obtiene datos presupuestarios y de cobertura desde la API DPE.

    Args:
        ruc:              RUC de 13 dígitos del municipio.
        establishment_id: ID de establecimiento DPE (opcional — si None, busca por RUC).
        year:             Año de consulta (default: año actual).

    Returns:
        dict con claves:
            status:       "ok" | "partial" | "failed"
            source_id:    "dpe"
            reliability:  float (0-1)
            data:         dict con presupuesto, cobertura, entidad
            coverage:     dict {year: [meses]}
            error:        str | None
    """
    year = year or date.today().year

    result: dict[str, Any] = {
        "status":      "pending",
        "source_id":   SOURCE_ID,
        "reliability": RELIABILITY,
        "data":        {},
        "coverage":    {},
        "error":       None,
    }

    try:
        from scripts.rc_scout import api_get, api_post, DPE_ADMIN_API, DPE_PUBLIC_API

        # ── 1. Obtener entidad ────────────────────────────────────────────────
        entity = None
        if establishment_id:
            entity = api_get(f"{DPE_ADMIN_API}/establishment/{establishment_id}")
        if not entity:
            # Buscar por RUC en lista de GADs municipales
            resp = api_get(f"{DPE_ADMIN_API}/establishment/list?function=7")
            if resp:
                for group in resp.get("results", []):
                    for item in group.get("data", []):
                        if item.get("identification") == ruc:
                            eid = item.get("id")
                            entity = api_get(f"{DPE_ADMIN_API}/establishment/{eid}")
                            break
                    if entity:
                        break

        if entity:
            result["data"]["entidad"] = {
                "id":     entity.get("id"),
                "nombre": entity.get("name") or entity.get("nombre"),
                "ruc":    entity.get("identification") or ruc,
            }

        # ── 2. Cobertura de meses publicados ─────────────────────────────────
        coverage: dict[str, list[int]] = {}
        max_month = date.today().month + 1

        for y in [year - 1, year]:
            max_m = max_month if y == year else 12
            months = []
            for m in range(1, max_m + 1):
                resp = api_post(
                    f"{DPE_PUBLIC_API}/presupuesto",
                    {"ruc": ruc, "year": y, "month": m},
                )
                if resp:
                    months.append(m)
            if months:
                coverage[str(y)] = months

        result["coverage"]          = coverage
        result["data"]["cobertura"] = coverage

        # ── 3. Calcular score de cobertura ────────────────────────────────────
        meses_actuales = len(coverage.get(str(year), []))
        meses_anteriores = len(coverage.get(str(year - 1), []))

        result["data"]["meses_publicados_actual"]   = meses_actuales
        result["data"]["meses_publicados_anterior"] = meses_anteriores
        result["data"]["cobertura_pct"]             = round(meses_actuales / 12, 2) if meses_actuales else 0.0

        # reliability ajustado por cobertura
        cov_factor = min(1.0, meses_anteriores / 12) if meses_anteriores else 0.5
        result["reliability"] = round(RELIABILITY * cov_factor, 3)

        result["status"] = "ok" if (entity or coverage) else "partial"
        logger.info(f"[DPE] RUC {ruc} — cobertura {coverage} — status: {result['status']}")

    except Exception as exc:
        logger.error(f"[DPE] Error fetching RUC {ruc}: {exc}")
        result["status"] = "failed"
        result["error"]  = str(exc)
        result["reliability"] = 0.0

    return result
