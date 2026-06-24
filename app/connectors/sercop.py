"""
app/connectors/sercop.py — QUIRA OS · Sprint 1
Conector institucional: SERCOP — Sistema de Contratación Pública

Puente entre el pipeline y scripts/fetch_sercop.py.
Expone la interfaz canónica que consume snapshot_pipeline.py.

Doctrina: SERCOP OCDS API expone el tiempo institucional — procesos en tránsito,
cuellos de botella, parálisis, simulación de gestión.

Fuente: datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/v1/
Standard: OCDS (Open Contracting Data Standard)
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

SOURCE_ID   = "sercop"
RELIABILITY = 0.95


def fetch_sercop_data(
    ruc: str,
    year: int | None = None,
    search: str = "",
    buyer: str = "",
) -> dict:
    """Obtiene el estado vivo de contratación pública desde SERCOP OCDS API.

    Args:
        ruc:  RUC de 13 dígitos del municipio.
        year: Año de consulta (default: año actual).

    Returns:
        dict con claves:
            status:       "ok" | "partial" | "failed"
            source_id:    "sercop"
            reliability:  float (0-1)
            data:         dict con contratacion block completo
            error:        str | None
    """
    year = year or date.today().year

    result: dict[str, Any] = {
        "status":      "pending",
        "source_id":   SOURCE_ID,
        "reliability": RELIABILITY,
        "data":        {},
        "error":       None,
    }

    try:
        from scripts.fetch_sercop import build_contratacion_block

        # API actual: search por palabra clave + filtro por comprador (no por RUC)
        contratacion = build_contratacion_block(year, search or "", buyer or "")

        result["data"]   = contratacion
        result["status"] = "ok" if contratacion.get("n_procesos") else "partial"

        # Ajustar reliability si la API no respondió
        if result["status"] == "partial":
            result["reliability"] = round(RELIABILITY * 0.5, 3)

        alertas = contratacion.get("alertas", [])
        if alertas:
            logger.warning(f"[SERCOP] RUC {ruc} — {len(alertas)} alertas: {alertas}")
        else:
            logger.info(f"[SERCOP] RUC {ruc} — status: {result['status']}")

    except Exception as exc:
        logger.error(f"[SERCOP] Error fetching RUC {ruc}: {exc}")
        result["status"]      = "failed"
        result["error"]       = str(exc)
        result["reliability"] = 0.0

    return result
