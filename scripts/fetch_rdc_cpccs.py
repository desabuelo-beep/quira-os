#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fetch_rdc_cpccs.py — QUIRA OS
Verifica la Rendición de Cuentas (RdC) de un municipio desde fuentes públicas.

La RdC tiene DOS componentes verificables de forma INDEPENDIENTE:

  Componente A — Informe Técnico (portal CPCCS):
    Portal: rendiciondecuentas.cpccs.gob.ec
    Es el informe formal que el GAD sube a la plataforma CPCCS.
    Auto-declarativo pero verificable (número de informe, fecha, asistentes).

  Componente B — Evento Público (redes sociales):
    Fuente: YouTube / Facebook oficial del GAD
    Es evidencia INDEPENDIENTE de que el acto de deliberación pública
    se realizó realmente. Muestra el discurso del alcalde/alcaldesa.
    Si no hay video disponible, el Componente B no puede verificarse.

Marco legal:
  LOPC Arts. 88-95 · COOTAD Art. 302 · Res. CPCCS-004-2026

Uso:
  python scripts/fetch_rdc_cpccs.py --ruc 1360000980001 --year 2024
  python scripts/fetch_rdc_cpccs.py --ruc 1360000980001 --year 2024 --enrich data/scouting/gm_snapshot_manta.json

Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from scripts.rc_scout import api_get
except ImportError:
    import urllib.request

    def api_get(url: str, timeout: int = 20) -> Any:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "QUIRA-Scout/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            print(f"[WW] GET {url} → {e}")
            return None

OUT_DIR = Path(__file__).parent.parent / "data" / "scouting"

# ── URLs ───────────────────────────────────────────────────────────────────────
CPCCS_PORTAL  = "https://rendiciondecuentas.cpccs.gob.ec"
CPCCS_API     = "https://rendiciondecuentas.cpccs.gob.ec/api/v1"


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTE A — INFORME CPCCS
# ══════════════════════════════════════════════════════════════════════════════

def fetch_componente_a(ruc: str, year: int) -> dict:
    """
    Busca el informe de RdC en el portal CPCCS.
    Retorna los campos del Componente A.
    """
    result = {
        "n_informe_cpccs":       None,
        "fecha_ingreso":         None,
        "en_periodo_cpccs":      None,
        "asistentes":            None,
        "lugar":                 None,
        "zona_rural":            None,
        "plan_trabajo_publicado": None,
        "publicado_lotaip":      None,
        "score":                 0,
        "fuente":               f"Pendiente — verificar en {CPCCS_PORTAL}",
    }

    # Intentar API pública CPCCS (si está disponible)
    url = f"{CPCCS_API}/informes?ruc={ruc}&anio={year}"
    resp = api_get(url)

    if resp and isinstance(resp, (dict, list)):
        # Intentar extraer datos si la API responde
        items = resp if isinstance(resp, list) else resp.get("results", [resp])
        if items:
            item = items[0]
            result.update({
                "n_informe_cpccs":       str(item.get("id") or item.get("numero") or ""),
                "fecha_ingreso":         (item.get("fecha_ingreso") or "")[:10],
                "asistentes":            item.get("numero_asistentes") or item.get("asistentes"),
                "lugar":                 item.get("lugar_deliberacion") or item.get("lugar"),
                "plan_trabajo_publicado": item.get("plan_trabajo") is not None,
                "fuente":               f"API CPCCS — {url}",
            })

            # Determinar zona rural por nombre del lugar
            lugar = (result["lugar"] or "").lower()
            palabras_rurales = ["comunidad", "comunidad", "parroquia", "barrio rural",
                                "recinto", "sector", "sitio", "canton"]
            cabeceras = ["casa patrimonial", "auditorio municipal", "teatro municipal",
                         "salon", "concejo", "edificio municipal"]
            if any(p in lugar for p in palabras_rurales):
                result["zona_rural"] = True
            elif any(p in lugar for p in cabeceras):
                result["zona_rural"] = False

            result["score"] = _calcular_score_a(result)
    else:
        # API no disponible — devolver URL para verificación manual
        portal_url = f"{CPCCS_PORTAL}/busqueda?ruc={ruc}&anio={year}"
        result["fuente"] = f"Manual requerido — {portal_url}"
        result["portal_url_manual"] = portal_url
        print(f"[WW] Portal CPCCS no respondió vía API.")
        print(f"     Verificar manualmente: {portal_url}")

    return result


def _calcular_score_a(comp_a: dict) -> int:
    """Calcula el score del Componente A (máximo 65 puntos)."""
    score = 0

    # Informe presentado (30 pts)
    if comp_a.get("n_informe_cpccs"):
        score += 30

    # Asistentes > 100 (10 pts)
    asistentes = comp_a.get("asistentes") or 0
    if isinstance(asistentes, (int, float)) and asistentes > 100:
        score += 10

    # Evento en zona rural (10 pts)
    if comp_a.get("zona_rural") is True:
        score += 10

    # Plan de trabajo con sugerencias publicado (10 pts)
    if comp_a.get("plan_trabajo_publicado"):
        score += 10

    # Publicado en LOTAIP (5 pts)
    if comp_a.get("publicado_lotaip"):
        score += 5

    return score


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTE B — EVENTO PÚBLICO EN REDES SOCIALES
# ══════════════════════════════════════════════════════════════════════════════

def build_componente_b_placeholder(nombre_municipio: str, year: int) -> dict:
    """
    Construye el placeholder del Componente B.
    La verificación de redes sociales es MANUAL (YouTube/Facebook).
    En el futuro se puede automatizar con YouTube Data API v3.
    """
    nombre_corto = (nombre_municipio
                    .replace("GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DEL CANTÓN ", "")
                    .replace("GOBIERNO AUTONOMO DESCENTRALIZADO MUNICIPAL DEL CANTON ", "")
                    .replace("GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DE EL ", "")
                    .replace("GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DE ", "")
                    .strip()
                    .title())

    return {
        "video_url":    None,
        "fecha_video":  None,
        "plataforma":   None,
        "duracion_min": None,
        "vistas":       None,
        "score":        0,
        "fuente":      "Pendiente — verificación manual en redes oficiales",
        "instrucciones_verificacion": (
            f"1. Buscar en YouTube: '{nombre_corto} rendicion de cuentas {year}'\n"
            f"2. Buscar en Facebook: página oficial 'GAD {nombre_corto}' → Videos\n"
            f"3. Verificar que la fecha del video coincida con la fecha en el informe CPCCS\n"
            f"4. Registrar: URL, plataforma, fecha, duración en minutos, vistas\n"
            f"5. El discurso del alcalde/alcaldesa debe estar presente en el video"
        ),
    }


def _calcular_score_b(comp_b: dict) -> int:
    """Calcula el score del Componente B (máximo 35 puntos)."""
    score = 0

    # Video encontrado (15 pts)
    if comp_b.get("video_url"):
        score += 15

    # Fecha coincide (10 pts) — se asume coincidencia si ambas fechas están cargadas
    if comp_b.get("fecha_video") and comp_b.get("video_url"):
        score += 10

    # Duración > 45 minutos (5 pts)
    duracion = comp_b.get("duracion_min") or 0
    if isinstance(duracion, (int, float)) and duracion > 45:
        score += 5

    # Discurso del alcalde verificado (5 pts) — campo explícito
    if comp_b.get("discurso_alcalde_verificado"):
        score += 5

    return score


# ══════════════════════════════════════════════════════════════════════════════
# CONSTRUCCIÓN DEL BLOQUE RdC COMPLETO
# ══════════════════════════════════════════════════════════════════════════════

def build_accountability_block(ruc: str, year: int, nombre: str = "") -> dict:
    """
    Construye el bloque completo 'accountability.rdc' para el snapshot.
    """
    print(f"[>>] Verificando RdC CPCCS · RUC {ruc} · Período {year}...")

    comp_a = fetch_componente_a(ruc, year)
    comp_b = build_componente_b_placeholder(nombre or ruc, year)

    score_a = comp_a.get("score", 0)
    score_b = _calcular_score_b(comp_b)
    score_total = score_a + score_b

    # Clasificación
    if score_total >= 85:
        clasificacion = "Rendición de cuentas excelente"
    elif score_total >= 70:
        clasificacion = "Rendición de cuentas completa"
    elif score_total >= 50:
        clasificacion = "Rendición de cuentas parcial"
    elif comp_a.get("n_informe_cpccs"):
        clasificacion = "Rendición de cuentas deficiente"
    else:
        clasificacion = "Sin rendición de cuentas verificada"

    return {
        "accountability": {
            "rdc": {
                "year":            year,
                "componente_a":    comp_a,
                "componente_b":    comp_b,
                "score_total":     score_total,
                "clasificacion":   clasificacion,
                "nota": (
                    "Componente A (portal CPCCS) = informe formal auto-declarativo. "
                    "Componente B (redes sociales) = evidencia independiente del evento. "
                    "Ambos son necesarios para validar la RdC completa. "
                    "Si A=0 → no presentó informe → score total no representa cumplimiento."
                ),
            }
        }
    }


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verifica Rendición de Cuentas CPCCS + Redes | QUIRA OS",
    )
    parser.add_argument("--ruc",   required=True, help="RUC de la entidad (13 dígitos)")
    parser.add_argument("--year",  type=int, default=date.today().year - 1,
                        help="Año rendido (generalmente el anterior al corriente)")
    parser.add_argument("--nombre", type=str, default="",
                        help="Nombre oficial del municipio (para instrucciones de búsqueda)")
    parser.add_argument("--enrich", type=str, default=None,
                        help="Snapshot existente a enriquecer con bloque accountability")
    parser.add_argument("--out",   type=str, default=None,
                        help="Ruta de salida del JSON")
    args = parser.parse_args()

    block = build_accountability_block(args.ruc, args.year, args.nombre)
    rdc   = block["accountability"]["rdc"]

    # Mostrar resumen
    comp_a = rdc["componente_a"]
    comp_b = rdc["componente_b"]

    print(f"\n{'─'*60}")
    print(f"  RdC {args.year} — Score total: {rdc['score_total']}/100")
    print(f"  Clasificación: {rdc['clasificacion']}")
    print(f"{'─'*60}")
    print(f"  Componente A (CPCCS):  {comp_a['score']}/65")
    if comp_a.get("n_informe_cpccs"):
        print(f"    Informe #:  {comp_a['n_informe_cpccs']}")
        print(f"    Asistentes: {comp_a['asistentes']}")
        print(f"    Lugar:      {comp_a['lugar']}")
        print(f"    Rural:      {comp_a['zona_rural']}")
    else:
        print(f"    → PENDIENTE: {comp_a.get('portal_url_manual','')}")
        print(f"    → Verificar manualmente en el portal CPCCS")
    print(f"  Componente B (Redes):  {comp_b['score']}/35")
    print(f"    → MANUAL REQUERIDO")
    print(f"    Instrucciones:")
    for linea in (comp_b.get("instrucciones_verificacion","")).split("\n"):
        if linea.strip():
            print(f"       {linea}")
    print()

    # Enriquecer snapshot existente
    if args.enrich:
        snap_path = Path(args.enrich)
        if snap_path.exists():
            with open(snap_path, "r", encoding="utf-8") as f:
                snap = json.load(f)
            snap.update(block)
            with open(snap_path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2)
            print(f"[OK] Snapshot enriquecido con bloque RdC: {snap_path}")
        else:
            print(f"[XX] Snapshot no encontrado: {snap_path}")
        return

    # Guardar bloque independiente
    out_path = (
        Path(args.out) if args.out
        else OUT_DIR / f"rdc_{args.ruc}_{args.year}.json"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"ruc": args.ruc, "year": args.year, **block},
                  f, ensure_ascii=False, indent=2)
    print(f"[OK] Bloque RdC guardado: {out_path}")
    print()
    print("Para enriquecer un snapshot:")
    print(f"  python scripts/fetch_rdc_cpccs.py --ruc {args.ruc} --year {args.year} "
          f"--enrich data/scouting/gm_snapshot_{{municipio}}.json")


if __name__ == "__main__":
    main()
