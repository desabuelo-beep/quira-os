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
        from scripts.rc_scout import (api_get, api_post_con_estado,
                                      DPE_ADMIN_API, DPE_PUBLIC_API)

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

        # Cada mes se consulta CON SU ESTADO (ADR-042 §6). Antes se hacía
        # `if resp: months.append(m)`, de modo que un timeout o un error del
        # servidor dejaba el mes fuera de la lista — exactamente igual que si el
        # municipio no hubiera publicado. Ese vacío viajaba después a un informe
        # y se leía como incumplimiento: una afirmación sobre la gestión pública
        # construida sobre un fallo de red.
        #
        # Ahora se separan tres cosas: meses publicados, meses en que la fuente
        # respondió que no hay nada, y meses que NO SE PUDIERON COMPROBAR. Los
        # últimos no son ausencia de evidencia: son ausencia de medición.
        from app.observatorio import Estado
        no_comprobados: dict[str, list[int]] = {}

        for y in [year - 1, year]:
            max_m = max_month if y == year else 12
            months: list[int] = []
            sin_medir: list[int] = []
            for m in range(1, max_m + 1):
                resp, estado = api_post_con_estado(
                    f"{DPE_PUBLIC_API}/presupuesto",
                    {"ruc": ruc, "year": y, "month": m},
                )
                if estado is Estado.CAPTURADA and resp:
                    months.append(m)
                elif estado is not Estado.EVIDENCIA_AUSENTE:
                    # Ni publicado ni verificablemente ausente: no se sabe.
                    sin_medir.append(m)
            if months:
                coverage[str(y)] = months
            if sin_medir:
                no_comprobados[str(y)] = sin_medir

        result["coverage"]               = coverage
        result["data"]["cobertura"]      = coverage
        result["no_comprobados"]         = no_comprobados
        result["data"]["no_comprobados"] = no_comprobados

        # ── 3. Calcular score de cobertura ────────────────────────────────────
        meses_actuales = len(coverage.get(str(year), []))
        meses_anteriores = len(coverage.get(str(year - 1), []))

        result["data"]["meses_publicados_actual"]   = meses_actuales
        result["data"]["meses_publicados_anterior"] = meses_anteriores

        # El porcentaje se calcula sobre los meses EFECTIVAMENTE COMPROBADOS,
        # no sobre doce. Dividir entre doce cuando tres meses no se pudieron
        # consultar produce una cifra que parece medida y no lo está — y esa
        # cifra es la que después viaja a un informe.
        sin_medir_actual = len(no_comprobados.get(str(year), []))
        comprobados = max(0, max_month - sin_medir_actual)
        result["data"]["meses_no_comprobados"] = sin_medir_actual
        result["data"]["base_de_calculo"]      = comprobados
        result["data"]["cobertura_pct"] = (
            round(meses_actuales / comprobados, 2) if comprobados else None
        )

        # La confianza baja cuando hay meses sin medir: no es lo mismo una
        # cobertura verificada de punta a punta que una con huecos.
        cov_factor = min(1.0, meses_anteriores / 12) if meses_anteriores else 0.5
        total_sin_medir = sum(len(v) for v in no_comprobados.values())
        if total_sin_medir:
            cov_factor *= max(0.3, 1 - total_sin_medir / 24)
        result["reliability"] = round(RELIABILITY * cov_factor, 3)

        # `partial` deja de significar dos cosas distintas: ahora dice
        # explícitamente que la medición quedó incompleta.
        if total_sin_medir:
            result["status"] = "partial"
            result["error"] = (f"{total_sin_medir} mes(es) no se pudieron "
                               f"comprobar: la fuente no respondió o su formato "
                               f"cambió. NO son ausencia de publicación.")
            logger.warning("[DPE] RUC %s — %d mes(es) sin comprobar: %s",
                           ruc, total_sin_medir, no_comprobados)
        else:
            result["status"] = "ok" if (entity or coverage) else "partial"
        logger.info(f"[DPE] RUC {ruc} — cobertura {coverage} — status: {result['status']}")

    except Exception as exc:
        logger.error(f"[DPE] Error fetching RUC {ruc}: {exc}")
        result["status"] = "failed"
        result["error"]  = str(exc)
        result["reliability"] = 0.0

    return result
