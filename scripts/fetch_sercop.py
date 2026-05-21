#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fetch_sercop.py — QUIRA OS
Obtiene el estado de los procesos de contratación pública (SERCOP)
para un municipio dado por RUC.

IMPORTANTE: No se descarga solo el PAC. Se analiza el ESTADO VIVO de los
procesos mes a mes: adjudicados, cancelados, desiertos, en publicación,
contratos suscritos y liquidados. Esto permite medir la ejecución legal real.

Fuente: Portal de Compras Públicas (SERCOP)
  - SOCE API: https://soce.gob.ec/soce/
  - Portal:   https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/

Uso:
  python scripts/fetch_sercop.py --ruc 1360000980001 --year 2026
  python scripts/fetch_sercop.py --ruc 1360000980001 --year 2026 --out data/scouting/

Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from scripts.rc_scout import api_get
except ImportError:
    # Fallback si rc_scout no está disponible
    import urllib.request
    import urllib.error

    def api_get(url: str, timeout: int = 20) -> Any:
        """Minimal fallback HTTP GET."""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "QUIRA-Scout/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"[WW] GET {url} → {e}")
            return None

OUT_DIR = Path(__file__).parent.parent / "data" / "scouting"

# ── URLs SERCOP ───────────────────────────────────────────────────────────────
# API de datos abiertos OCDS (Open Contracting Data Standard)
SERCOP_OCDS_BASE = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/v1"
# Portal principal
SERCOP_PORTAL   = "https://www.compraspublicas.gob.ec"

# Estados canonicos SERCOP
ESTADOS_PROCESO = {
    "ADJUDICADO":           "adjudicados",
    "EN_PUBLICACION":       "en_publicacion",
    "CANCELADO":            "cancelados",
    "DESIERTO":             "desiertos",
    "CONTRATO_SUSCRITO":    "contratos_suscritos",
    "CONTRATO_LIQUIDADO":   "contratos_liquidados",
}

# Alertas automáticas
UMBRAL_CANCELADOS_PCT = 15.0   # > 15% cancelados → alerta
UMBRAL_PARÁLISIS_DIAS = 90     # proceso sin resolución > 90 días → alerta
UMBRAL_EMERGENCIA_PCT = 10.0   # > 10% PAC en emergencias → alerta


# ══════════════════════════════════════════════════════════════════════════════
# OBTENCIÓN DE DATOS
# ══════════════════════════════════════════════════════════════════════════════

def fetch_pac(ruc: str, year: int) -> dict | None:
    """
    Descarga el Plan Anual de Contratación (PAC) de la entidad.
    Intenta primero la API OCDS; si falla, informa la URL de descarga manual.
    """
    # Intento API OCDS
    url = (
        f"{SERCOP_OCDS_BASE}/plannedprocurement"
        f"?buyer.identifier.id={ruc}&year={year}&page=1&limit=1"
    )
    resp = api_get(url)
    if resp and isinstance(resp, dict):
        total = resp.get("count", 0)
        return {
            "via": "ocds_api",
            "total_procesos_planificados": total,
            "pac_url": url,
        }

    # Fallback: URL de descarga manual
    portal_url = (
        f"{SERCOP_PORTAL}/ProcesoContratacion/compras/busqueda/buscarPAC"
        f"?ruc={ruc}&anio={year}"
    )
    print(f"[WW] API OCDS no disponible. Descarga PAC manualmente desde:")
    print(f"     {portal_url}")
    return None


def fetch_procesos(ruc: str, year: int, delay: float = 0.5) -> dict:
    """
    Obtiene el estado de todos los procesos de contratación activos.
    Devuelve conteos por estado y datos de alertas.
    """
    conteos: dict[str, int] = {v: 0 for v in ESTADOS_PROCESO.values()}
    procesos_raw: list[dict] = []
    alertas: list[str] = []

    page = 1
    total_fetched = 0

    print(f"[>>] Consultando procesos SERCOP para RUC {ruc}, año {year}...")

    while True:
        url = (
            f"{SERCOP_OCDS_BASE}/contracts"
            f"?buyer.identifier.id={ruc}&year={year}&page={page}&limit=100"
        )
        resp = api_get(url)

        if not resp or not isinstance(resp, dict):
            if page == 1:
                print("[WW] API SERCOP no respondió — generando estructura vacía con URL manual")
                portal_url = (
                    f"{SERCOP_PORTAL}/ProcesoContratacion/compras/busqueda"
                    f"?ruc={ruc}&tipoBusqueda=expediente&busquedaText=&year={year}"
                )
                return {
                    "via": "manual_required",
                    "portal_url": portal_url,
                    "conteos": conteos,
                    "total_procesos": 0,
                    "alertas": ["api_no_disponible"],
                    "nota": f"Verificar manualmente en: {portal_url}",
                }
            break

        items = resp.get("results", resp.get("items", []))
        if not items:
            break

        for item in items:
            estado_raw = (item.get("status") or "").upper()
            estado_tipo = (item.get("tender", {}).get("procurementMethod") or "").upper()
            fecha_inicio_str = item.get("tender", {}).get("tenderPeriod", {}).get("startDate", "")

            # Conteo por estado
            for estado_canon, key in ESTADOS_PROCESO.items():
                if estado_canon in estado_raw:
                    conteos[key] += 1

            # Detección de procesos sin resolución > 90 días
            if "EN_PUBLICACION" in estado_raw and fecha_inicio_str:
                try:
                    fecha_inicio = datetime.fromisoformat(fecha_inicio_str[:10]).date()
                    dias = (date.today() - fecha_inicio).days
                    if dias > UMBRAL_PARÁLISIS_DIAS:
                        alertas.append(f"proceso_paralizado_>90d")
                except Exception:
                    pass

            # Detección de emergencias
            if "EMERGENCIA" in estado_tipo or "EMERGENCIA" in estado_raw:
                conteos.setdefault("emergencias", 0)
                conteos["emergencias"] = conteos.get("emergencias", 0) + 1

            procesos_raw.append(item)

        total_fetched += len(items)
        total_api = resp.get("count", 0)

        if total_fetched >= total_api:
            break

        page += 1
        time.sleep(delay)

    # ── Calcular alertas ──────────────────────────────────────────────────────
    total = sum(conteos.values())
    if total > 0:
        pct_cancelados = conteos["cancelados"] / total * 100
        if pct_cancelados > UMBRAL_CANCELADOS_PCT:
            alertas.append(f"cancelados_excesivos_{pct_cancelados:.1f}pct")

        n_emergencias = conteos.get("emergencias", 0)
        if n_emergencias > 0 and (n_emergencias / total * 100) > UMBRAL_EMERGENCIA_PCT:
            alertas.append("emergencias_excesivas")

    # Deduplicar alertas de parálisis
    if "proceso_paralizado_>90d" in alertas:
        count_paralisis = alertas.count("proceso_paralizado_>90d")
        alertas = [a for a in alertas if a != "proceso_paralizado_>90d"]
        alertas.append(f"paralisis_{count_paralisis}_procesos_>90d")

    return {
        "via": "ocds_api",
        "conteos": conteos,
        "total_procesos": total_fetched,
        "alertas": list(set(alertas)),
    }


# ══════════════════════════════════════════════════════════════════════════════
# CONSTRUCCIÓN DEL BLOQUE CONTRATACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def build_contratacion_block(ruc: str, year: int) -> dict:
    """
    Construye el bloque 'contratacion' para el snapshot.
    Integra PAC + estado de procesos activos.
    """
    pac = fetch_pac(ruc, year)
    procesos = fetch_procesos(ruc, year)

    conteos = procesos.get("conteos", {})
    total   = procesos.get("total_procesos", 0)

    pct_adjudicados = (
        conteos.get("adjudicados", 0) / total * 100 if total > 0 else 0.0
    )
    pct_cancelados = (
        conteos.get("cancelados", 0) / total * 100 if total > 0 else 0.0
    )

    n_pac_planificados = (
        pac.get("total_procesos_planificados", 0) if pac else 0
    )

    block = {
        "pac_year":                year,
        "pac_publicado":           pac is not None,
        "fecha_pac":               None,           # completar manual
        "total_planificado_usd":   0.0,            # completar desde PAC CSV
        "n_procesos_planificados": n_pac_planificados,
        "estado_al_corte": {
            "adjudicados":          conteos.get("adjudicados", 0),
            "en_publicacion":       conteos.get("en_publicacion", 0),
            "cancelados":           conteos.get("cancelados", 0),
            "desiertos":            conteos.get("desiertos", 0),
            "contratos_suscritos":  conteos.get("contratos_suscritos", 0),
            "contratos_liquidados": conteos.get("contratos_liquidados", 0),
        },
        "pct_adjudicados":   round(pct_adjudicados, 2),
        "pct_cancelados":    round(pct_cancelados, 2),
        "alertas":           procesos.get("alertas", []),
        "fuente":            f"SERCOP · RUC {ruc} · {year}",
        "fecha_corte":       date.today().isoformat(),
        "via_api":           procesos.get("via", "desconocido"),
    }

    if procesos.get("nota"):
        block["nota"] = procesos["nota"]
    if procesos.get("portal_url"):
        block["portal_url_manual"] = procesos["portal_url"]

    return block


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Obtiene estado de procesos SERCOP para un municipio | QUIRA OS",
    )
    parser.add_argument("--ruc",  required=True, help="RUC de la entidad (13 dígitos)")
    parser.add_argument("--year", type=int, default=date.today().year, help="Año a analizar")
    parser.add_argument("--out",  type=str, default=None, help="Ruta de salida del JSON")
    parser.add_argument("--enrich", type=str, default=None,
                        help="Snapshot existente a enriquecer con bloque contratacion")
    args = parser.parse_args()

    print(f"[>>] Consultando SERCOP para RUC {args.ruc}, año {args.year}...")

    block = build_contratacion_block(args.ruc, args.year)

    # Mostrar resumen
    estado = block["estado_al_corte"]
    print(f"[OK] Procesos encontrados: {block['estado_al_corte']}")
    print(f"     Adjudicados:   {estado['adjudicados']} ({block['pct_adjudicados']:.1f}%)")
    print(f"     En publicación:{estado['en_publicacion']}")
    print(f"     Cancelados:    {estado['cancelados']} ({block['pct_cancelados']:.1f}%)")
    print(f"     Desiertos:     {estado['desiertos']}")
    print(f"     C. Suscritos:  {estado['contratos_suscritos']}")
    print(f"     C. Liquidados: {estado['contratos_liquidados']}")

    if block["alertas"]:
        print(f"[!!] Alertas: {', '.join(block['alertas'])}")
    else:
        print("[OK] Sin alertas de contratación")

    # Si se pasa un snapshot existente, enriquecerlo
    if args.enrich:
        snap_path = Path(args.enrich)
        if snap_path.exists():
            with open(snap_path, "r", encoding="utf-8") as f:
                snap = json.load(f)
            snap["contratacion"] = block
            with open(snap_path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2)
            print(f"[OK] Snapshot enriquecido: {snap_path}")
        else:
            print(f"[XX] No se encontró el snapshot: {snap_path}")
        return

    # Guardar bloque independiente
    out_path = (
        Path(args.out) if args.out
        else OUT_DIR / f"sercop_{args.ruc}_{args.year}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"ruc": args.ruc, "year": args.year, "contratacion": block},
                  f, ensure_ascii=False, indent=2)
    print(f"[OK] Bloque SERCOP guardado: {out_path}")
    print()
    print("Para enriquecer un snapshot existente:")
    print(f"  python scripts/fetch_sercop.py --ruc {args.ruc} --year {args.year} "
          f"--enrich data/scouting/gm_snapshot_{{municipio}}.json")


if __name__ == "__main__":
    main()
