#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/_generate_snapshot_dpe.py — QUIRA OS
Generador de gm_snapshot.json para municipios desde la API del portal DPE.

Fuente: API pública del Portal Nacional de Transparencia (DPE)
Uso: python scripts/_generate_snapshot_dpe.py --id 936
     python scripts/_generate_snapshot_dpe.py --ruc 1360000980001

Municipios conocidos (resultado de RC-SCOUT):
  Manta     → --id 936  (RUC: 1360000980001)
  Jipijapa  → --id 934  (RUC: 1360000630001)

El snapshot generado es un ESQUELETO validable por Panel de Carga.
Campos financieros (TGI, Ti, devengado) requieren datos del Gold Master Excel.
Flujo completo:
  1. Correr este script → genera gm_snapshot_{municipio}.json
  2. Abrir quiraintelligence.streamlit.app → Panel de Carga → Subir Snapshot
  3. (Opcional) Enriquecer con datos LOTAIP una vez descargados los CSV

Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Importar helpers de RC-SCOUT ─────────────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.rc_scout import (
    api_get, api_post,
    DPE_ADMIN_API, DPE_PUBLIC_API, DPE_TRANSP_API,
)

OUT_DIR = Path(__file__).parent.parent / "data" / "scouting"


# ══════════════════════════════════════════════════════════════════════════════
# COLECCIÓN DE DATOS DPE
# ══════════════════════════════════════════════════════════════════════════════

def fetch_entity(establishment_id: int | None = None, ruc: str | None = None) -> dict | None:
    """Obtiene datos de la entidad desde la API DPE."""
    if establishment_id:
        data = api_get(f"{DPE_ADMIN_API}/establishment/{establishment_id}")
        if data and isinstance(data, dict):
            return data

    if ruc:
        # Buscar por RUC en la lista
        resp = api_get(f"{DPE_ADMIN_API}/establishment/list?function=7")
        if resp:
            for group in resp.get("results", []):
                for item in group.get("data", []):
                    if item.get("identification") == ruc:
                        eid = item.get("id")
                        return api_get(f"{DPE_ADMIN_API}/establishment/{eid}")
    return None


def fetch_presupuesto_coverage(ruc: str, max_month_2026: int = 5) -> dict:
    """Obtiene la cobertura de meses publicados por año."""
    coverage: dict[str, list[int]] = {}
    for year in [2024, 2025, 2026]:
        max_m = max_month_2026 if year == 2026 else 12
        months = []
        for m in range(1, max_m + 1):
            resp = api_post(
                f"{DPE_PUBLIC_API}/presupuesto",
                {"ruc": ruc, "year": year, "month": m},
            )
            if resp:
                months.append(m)
        coverage[str(year)] = months
    return coverage


def fetch_annual_report(establishment_id: int) -> dict | None:
    """Obtiene info del reporte anual si existe."""
    resp = api_get(
        f"{DPE_TRANSP_API}/anual-report/establishment?establishment_id={establishment_id}"
    )
    if resp and isinstance(resp, dict):
        records = resp.get("list", [])
        if records:
            r = records[0]
            return {
                "year": r.get("year"),
                "file_path": r.get("file"),
                "created_at": (r.get("created_at") or "")[:10],
            }
    return None


# ══════════════════════════════════════════════════════════════════════════════
# GENERACIÓN DEL SNAPSHOT
# ══════════════════════════════════════════════════════════════════════════════

def build_snapshot(entity: dict, coverage: dict, annual: dict | None) -> dict:
    """
    Construye el gm_snapshot.json validable por Panel de Carga.
    Los campos financieros son placeholders marcados como 'pendiente_gold_master'.
    """
    eid    = entity.get("id", 0)
    ruc    = entity.get("identification", "000000000001")
    nombre = entity.get("name", entity.get("alias", "GAD Municipal"))
    # Codigo GAD: primeros 6 digitos del RUC
    codigo = ruc[:6] if ruc and len(ruc) >= 6 else "000000"

    months_2025  = coverage.get("2025", [])
    months_2026  = coverage.get("2026", [])
    fecha_corte  = f"2026-{max(months_2026):02d}-30" if months_2026 else "2026-04-30"

    today_iso = date.today().isoformat()

    snapshot = {
        "_meta": {
            "municipio":              nombre,
            "codigo_gad":             codigo,
            "ruc":                    ruc,
            "establishment_id_dpe":   eid,
            "fecha_corte":            fecha_corte,
            "version_excel":          f"DPE-API-{today_iso}",
            "sincronizado":           datetime.now(timezone.utc).isoformat(),
            "fuente_primaria":        "Portal DPE (api.transparencia.dpe.gob.ec)",
            "fuente_secundaria":      "Pendiente — Gold Master Excel no disponible",
            "meses_disponibles_2025": months_2025,
            "meses_disponibles_2026": months_2026,
            "cobertura_completa_2025": len(months_2025) == 12,
            "annual_report":          annual,
            "estado_datos":           "esqueleto_dpe_api",
            "nota": (
                "Snapshot generado automaticamente desde API DPE. "
                "Los campos financieros (TGI, Ti, devengado) son placeholder "
                "y deben actualizarse con datos del Gold Master Excel una vez disponibles."
            ),
        },
        "gad": {
            "codigo":          codigo,
            "nombre":          nombre,
            "nombre_corto":    entity.get("alias", nombre)[:50],
            "tipo":            "GAD Municipal",
            "ruc":             ruc,
            "autoridad":       f"{entity.get('first_name_authority','')} {entity.get('last_name_authority','')}".strip(),
            "cargo_autoridad": entity.get("job_authority", "Alcalde/sa"),
            "email_autoridad": entity.get("email_authority", ""),
            "direccion":       entity.get("address", ""),
            "establishment_id": eid,
        },
        "tgi": {
            "score":           0.0,
            "clasificacion":   "Pendiente",
            "nota":            "Requiere datos PDOT y Gold Master Excel",
            "indicadores": {
                "ICPI": {"valor": 0, "fuente": "pendiente"},
                "ICM":  {"valor": 0, "fuente": "pendiente"},
                "PSG":  {"valor": 0, "fuente": "pendiente"},
                "IET":  {"valor": 0, "fuente": "pendiente"},
                "IGP":  {"valor": 0, "fuente": "pendiente"},
                "IED":  {"valor": 0, "fuente": "pendiente"},
                "IFE":  {"valor": 0, "fuente": "pendiente"},
            },
        },
        "financiero": {
            "ti_2025_pct":         0.0,
            "devengado_q1_2026":   0.0,
            "codificado_anual":    0.0,
            "devengado_acum":      0.0,
            "pct_ejecucion":       0.0,
            "meses_con_datos_dpe": len(months_2025),
            "fuente":              "Pendiente — CSV LOTAIP Numeral 6 no descargado aun",
            "nota_descarga": (
                "Los CSV presupuestarios existen en DPE pero tienen un bug en la URL de descarga "
                "(path incorrecto en la API). Descargar manualmente desde "
                f"https://transparencia.dpe.gob.ec/entidades/{eid}"
            ),
        },
        "series_longitudinal": {
            "presupuesto_mensual_2025": [
                {"mes": m, "devengado": 0, "codificado": 0, "fuente": "pendiente_csv"}
                for m in months_2025
            ],
            "presupuesto_mensual_2026": [
                {"mes": m, "devengado": 0, "codificado": 0, "fuente": "pendiente_csv"}
                for m in months_2026
            ],
        },
        "territorial": {
            "parroquias_total":        0,
            "parroquias_rurales":      0,
            "parroquias_urbanas":      0,
            "poblacion_census_2022":   0,
            "superficie_km2":          0.0,
            "fuente":                  "Pendiente — INEC / PDOT",
        },
        # ── Contratación Pública (SERCOP) ─────────────────────────────────────
        # Fuente: compraspublicas.gob.ec — PAC + estado de procesos activos
        # Script: scripts/fetch_sercop.py (pendiente de construcción)
        # IMPORTANTE: no se descarga solo el PAC — se analiza el estado vivo de
        # los procesos de contratación mes a mes (adjudicados, cancelados,
        # desiertos, en publicación, contratos suscritos y liquidados).
        "contratacion": {
            "pac_year":                 date.today().year,
            "pac_publicado":            None,
            "fecha_pac":                None,
            "total_planificado_usd":    0.0,
            "n_procesos_planificados":  0,
            "estado_al_corte": {
                "adjudicados":          0,
                "en_publicacion":       0,
                "cancelados":           0,
                "desiertos":            0,
                "contratos_suscritos":  0,
                "contratos_liquidados": 0,
            },
            "pct_adjudicados":          0.0,
            "pct_cancelados":           0.0,
            "alertas":                  [],
            "fuente":                   "Pendiente — SERCOP SOCE / compraspublicas.gob.ec",
            "nota": (
                "Verificar en compraspublicas.gob.ec → Búsqueda avanzada → RUC. "
                "Descargar PAC vigente y revisar estado de procesos activos. "
                "Script fetch_sercop.py en construcción."
            ),
        },
        # ── Rendición de Cuentas (CPCCS) ──────────────────────────────────────
        # Fuente A (informe técnico): rendiciondecuentas.cpccs.gob.ec
        # Fuente B (evento público): YouTube / Facebook oficial del GAD
        # Marco legal: LOPC Arts. 88-95 · COOTAD Art. 302 · Res. CPCCS-004-2026
        # Las dos partes son independientes y se verifican por separado.
        "accountability": {
            "rdc": {
                "year":          date.today().year - 1,   # año rendido (anterior)
                # Componente A: informe técnico en plataforma CPCCS (verificable)
                "componente_a": {
                    "n_informe_cpccs":       None,
                    "fecha_ingreso":         None,
                    "en_periodo_cpccs":      None,
                    "asistentes":            None,
                    "lugar":                 None,
                    "zona_rural":            None,
                    "plan_trabajo_publicado": None,
                    "publicado_lotaip":      None,
                    "score":                 0,
                    "fuente":               "Pendiente — rendiciondecuentas.cpccs.gob.ec",
                },
                # Componente B: evento público grabado en redes sociales
                # (evidencia independiente de que el acto se realizó realmente)
                "componente_b": {
                    "video_url":    None,
                    "fecha_video":  None,
                    "plataforma":   None,   # "YouTube" | "Facebook" | "Otro"
                    "duracion_min": None,
                    "vistas":       None,
                    "score":        0,
                    "fuente":      (
                        f"Pendiente — buscar en YouTube/Facebook: "
                        f"'{nombre} rendicion de cuentas {date.today().year - 1}'"
                    ),
                },
                "score_total":  0,
                "clasificacion": "Pendiente",
                "nota": (
                    "RdC tiene DOS componentes verificables independientemente: "
                    "(A) informe técnico en portal CPCCS — auto-declarativo; "
                    "(B) video del evento público en redes oficiales del GAD — "
                    "evidencia independiente. Ambos deben verificarse."
                ),
            }
        },
    }

    return snapshot


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generador de gm_snapshot.json desde API DPE | QUIRA OS",
    )
    parser.add_argument("--id",  type=int, default=None, help="Establishment ID del portal DPE (ej: 936)")
    parser.add_argument("--ruc", type=str, default=None, help="RUC de la entidad (ej: 1360000980001)")
    parser.add_argument("--out", type=str, default=None, help="Ruta de salida (default: data/scouting/)")
    args = parser.parse_args()

    if not args.id and not args.ruc:
        parser.print_help()
        print("\nEjemplos:")
        print("  python scripts/_generate_snapshot_dpe.py --id 936    # Manta")
        print("  python scripts/_generate_snapshot_dpe.py --id 934    # Jipijapa")
        print("  python scripts/_generate_snapshot_dpe.py --ruc 1360000980001")
        sys.exit(0)

    print(f"[>>] Consultando API DPE para {'id=' + str(args.id) if args.id else 'ruc=' + args.ruc}...")

    entity = fetch_entity(establishment_id=args.id, ruc=args.ruc)
    if not entity:
        print("[XX] No se encontro la entidad en la API DPE")
        sys.exit(1)

    ruc  = entity.get("identification", "")
    eid  = entity.get("id", args.id)
    name = entity.get("name", entity.get("alias", ""))
    print(f"[OK] Entidad encontrada: {name}")
    print(f"     RUC: {ruc} | ID: {eid}")

    print("[>>] Consultando cobertura presupuestaria...")
    coverage = fetch_presupuesto_coverage(ruc)
    for year, months in coverage.items():
        print(f"     {year}: {len(months):2d} meses disponibles {months}")

    print("[>>] Consultando reporte anual...")
    annual = fetch_annual_report(eid)
    if annual:
        print(f"     Reporte anual {annual['year']} disponible")
    else:
        print("     Sin reporte anual")

    print("[>>] Generando snapshot...")
    snapshot = build_snapshot(entity, coverage, annual)

    # Determinar ruta de salida
    canton = name.replace("GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DEL CANTÓN ", "").replace(
        "GOBIERNO AUTONOMO DESCENTRALIZADO MUNICIPAL DEL CANTON ", "").replace(
        "GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DE EL ", "").strip()
    slug = canton.lower().replace(" ", "_").replace("/", "-")[:20]
    out_path = Path(args.out) if args.out else (OUT_DIR / f"gm_snapshot_{slug}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    print(f"[OK] Snapshot guardado: {out_path}")
    print()
    print("Siguiente paso:")
    print("  1. Revisa el snapshot y completa los datos financieros si tienes los CSV")
    print("  2. Sube via Panel de Carga en https://quiraintelligence.streamlit.app/")
    print("     → Rol Tecnico → Panel de Carga → Subir Snapshot")
    print()
    print("Para datos financieros reales (una vez disponibles los CSV):")
    print(f"  Descarga los CSV desde: https://transparencia.dpe.gob.ec/entidades/{eid}")
    print("  → Transparencia Activa → año 2025 → cada mes → Descargar")


if __name__ == "__main__":
    main()
