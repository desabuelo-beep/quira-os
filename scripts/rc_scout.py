#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/rc_scout.py — QUIRA OS · RC-SCOUT v2.0
Motor de Exploración Municipal — API REST + LOTAIP

Fuente primaria: API pública del Portal Nacional de Transparencia (DPE)
  https://transparencia.dpe.gob.ec/backend/v1/public/

Endpoints descubiertos por ingeniería inversa del portal:
  • GET  /admin/public/establishment/list?function=7     → lista todos los GADs
  • GET  /admin/public/establishment/{id}               → detalle de entidad
  • POST /public/public/presupuesto {ruc, year, month}  → presupuesto mensual
  • GET  /transparency/transparency/months?establishment_id={id}&year={y}&type=A
  • GET  /transparency/anual-report/establishment?establishment_id={id}

Fuente secundaria SERCOP (PAC):
  https://www.compraspublicas.gob.ec

Modos de uso:
    # Fase 1: Listar todos los GAD Municipales del Ecuador via API
    python scripts/rc_scout.py --list [--province manabi]

    # Fase 2: Escanear completitud presupuestaria (Manabí por defecto)
    python scripts/rc_scout.py --scan [--province manabi] [--all]

    # Fase 3: Ver reporte generado
    python scripts/rc_scout.py --report

    # Descargar archivos de un municipio via Playwright (requiere browser)
    python scripts/rc_scout.py --download --id 936

Salidas:
    data/scouting/gad_municipales_all.json   — lista completa (394 GADs)
    data/scouting/scouting_report.json       — ranking de candidatos
    data/scouting/{id}/                      — archivos por municipio

Dylus Lab © 2026 · Datos públicos LOTAIP — Ecuador
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# ── UTF-8 stdout (evita UnicodeEncodeError en Windows CP1252) ─────────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACION
# ══════════════════════════════════════════════════════════════════════════════

OUT_DIR = Path(__file__).parent.parent / "data" / "scouting"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DPE_BASE       = "https://transparencia.dpe.gob.ec"
DPE_ADMIN_API  = f"{DPE_BASE}/backend/v1/admin/public"
DPE_PUBLIC_API = f"{DPE_BASE}/backend/v1/public/public"
DPE_TRANSP_API = f"{DPE_BASE}/backend/v1/transparency"

# function=7 → "Gobiernos Autónomos Descentralizados" en el form-fields del portal
GAD_FUNCTION_ID = 7

# Provincias prioritarias (comparabilidad con Montecristi / Manabí)
PRIORITY_PROVINCES = [14, 8, 24, 12]  # Manabí, Esmeraldas, Santa Elena, Los Ríos

# IDs numéricos de provincias
PROVINCE_NAMES = {
    1: "Azuay", 2: "Bolivar", 3: "Canar", 4: "Carchi", 5: "Chimborazo",
    6: "Cotopaxi", 7: "El Oro", 8: "Esmeraldas", 9: "Galapagos",
    10: "Guayas", 11: "Imbabura", 12: "Loja", 13: "Los Rios", 14: "Manabi",
    15: "Morona Santiago", 16: "Napo", 17: "Orellana", 18: "Pastaza",
    19: "Pichincha", 20: "Santa Elena", 21: "Santo Domingo", 22: "Sucumbios",
    23: "Tungurahua", 24: "Zamora Chinchipe",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) QUIRA-Scout/2.0",
    "Accept": "application/json",
    "Referer": "https://transparencia.dpe.gob.ec/",
}

MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


# ══════════════════════════════════════════════════════════════════════════════
# UTILIDADES HTTP
# ══════════════════════════════════════════════════════════════════════════════

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": ".", "OK": "OK", "WARN": "!!", "ERR": "XX", "STEP": ">>"}.get(level, ".")
    print(f"[{ts}] {prefix} {msg}", flush=True)


# ══════════════════════════════════════════════════════════════════════════════
# ACCESO A LA API — con estado explícito (ADR-042 §6)
# ══════════════════════════════════════════════════════════════════════════════
# Las funciones `api_get`/`api_post` devolvían `None` para TODO: un 404, un
# timeout, un error del servidor y un JSON corrupto eran indistinguibles entre
# sí. Quien las llamaba solo podía interpretar el `None` como «no hay datos» —
# y así un fallo de red terminaba registrado como que un municipio no publicó.
#
# Las variantes `_con_estado` devuelven además QUÉ pasó, para que el llamador
# no tenga que adivinar. Las originales se conservan sobre ellas: siguen
# devolviendo solo los datos, así que ningún llamador existente se rompe.

def _pedir(url: str, timeout: int, payload: dict | None = None):
    """(datos, estado). Traduce lo que ocurrió al vocabulario de ADR-042 §6."""
    from app.observatorio import Estado
    try:
        if payload is None:
            req = Request(url, headers=HEADERS)
        else:
            req = Request(url, data=json.dumps(payload).encode("utf-8"),
                          headers={**HEADERS, "Content-Type": "application/json"})
        with urlopen(req, timeout=timeout) as r:
            crudo = r.read()
        try:
            datos = json.loads(crudo)
        except json.JSONDecodeError:
            # La fuente respondió, pero lo que devolvió no es lo que sabemos
            # leer. Habla de NUESTRO instrumento, no del municipio.
            log(f"respuesta no interpretable → {url[:60]}", "WARN")
            return None, Estado.CAPTURADOR_DEGRADADO
        # Una respuesta vacía es una respuesta: la fuente contestó y no hay nada.
        if datos in (None, [], {}):
            return None, Estado.EVIDENCIA_AUSENTE
        return datos, Estado.CAPTURADA
    except HTTPError as e:
        # 404/400 en estos endpoints significan «no hay dato para ese período»:
        # la fuente respondió y la respuesta es la ausencia. Cualquier otro
        # código habla del servidor, no del sujeto observado.
        if e.code in (400, 404):
            return None, Estado.EVIDENCIA_AUSENTE
        log(f"HTTP {e.code} → {url[:60]}", "WARN")
        return None, Estado.FUENTE_NO_DISPONIBLE
    except (URLError, TimeoutError, OSError) as e:
        log(f"sin respuesta de la fuente ({type(e).__name__}) → {url[:60]}", "WARN")
        return None, Estado.FUENTE_NO_DISPONIBLE
    except Exception as e:  # noqa: BLE001
        log(f"fallo interno en la consulta: {type(e).__name__}: {e}", "WARN")
        return None, Estado.ERROR_TECNICO


def api_get_con_estado(url: str, timeout: int = 15):
    """(datos, estado) de una consulta GET."""
    return _pedir(url, timeout)


def api_post_con_estado(url: str, payload: dict, timeout: int = 12):
    """(datos, estado) de una consulta POST."""
    return _pedir(url, timeout, payload)


def api_get(url: str, timeout: int = 15) -> dict | list | None:
    """Solo los datos. Para saber POR QUÉ no hay, usar `api_get_con_estado`."""
    return _pedir(url, timeout)[0]


def api_post(url: str, payload: dict, timeout: int = 12) -> dict | list | None:
    """Solo los datos. Para saber POR QUÉ no hay, usar `api_post_con_estado`."""
    return _pedir(url, timeout, payload)[0]


def save_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════════════════
# FASE 1: ENUMERACION DE GAD MUNICIPALES VIA API
# ══════════════════════════════════════════════════════════════════════════════

def list_gad_municipales(province_filter: list[int] | None = None) -> list[dict]:
    """
    Lista todos los GAD Municipales del Ecuador via la API del portal DPE.
    Filtra por función=7 (Gobiernos Autónomos Descentralizados) y
    keywords MUNICIPAL/MUNICIPIO en el nombre.

    Args:
        province_filter: lista de IDs de provincia (None = todas)

    Returns:
        Lista de dicts con id, nombre, ruc, provincia, slug
    """
    log("Consultando API de entidades DPE...", "STEP")
    resp = api_get(f"{DPE_ADMIN_API}/establishment/list?function={GAD_FUNCTION_ID}")
    if not resp:
        log("API no respondio — verifica conectividad", "ERR")
        return []

    results: list[dict] = []
    for letter_group in resp.get("results", []):
        for item in letter_group.get("data", []):
            name = item.get("name", "").upper()
            # Solo GAD Municipales (excluir Provincial, Parroquial, Empresa Publica)
            if not (("MUNICIPAL" in name or "MUNICIPIO" in name) and
                    "PROVINCIAL" not in name and
                    "PARROQUIAL" not in name and
                    "EMPRESA" not in name and
                    "PATRONATO" not in name and
                    "REGISTRO" not in name):
                continue

            provinces = item.get("province", [])
            if province_filter and not any(p in province_filter for p in provinces):
                continue

            province_id = provinces[0] if provinces else 0
            results.append({
                "id":           item.get("id"),
                "nombre":       item.get("name"),
                "alias":        item.get("alias", ""),
                "ruc":          item.get("identification", ""),
                "provincia_id": province_id,
                "provincia":    PROVINCE_NAMES.get(province_id, "Desconocida"),
                "parroquia":    (item.get("parroquia") or [""])[0],
                "autoridad":    f"{item.get('first_name_authority','')} {item.get('last_name_authority','')}".strip(),
                "cargo":        item.get("job_authority", ""),
                "email":        item.get("email_authority", ""),
                "activo":       item.get("is_active", True),
            })

    log(f"GAD Municipales encontrados: {len(results)}", "OK")
    return results


# ══════════════════════════════════════════════════════════════════════════════
# FASE 2: ANALISIS DE COMPLETITUD PRESUPUESTARIA
# ══════════════════════════════════════════════════════════════════════════════

def check_presupuesto_coverage(
    ruc: str,
    years: list[int] | None = None,
    max_month_2026: int = 5,
) -> dict:
    """
    Consulta la API de presupuesto para cada mes de cada año objetivo.

    Args:
        ruc:           RUC de la institución (13 dígitos)
        years:         Años a consultar (default: [2025, 2026])
        max_month_2026: Mes máximo a consultar en 2026 (ajustar al mes actual)

    Returns:
        dict con meses disponibles por año y score de completitud
    """
    if years is None:
        years = [2025, 2026]

    coverage: dict[str, list[int]] = {}
    for year in years:
        max_m = max_month_2026 if year == 2026 else 12
        avail = []
        for month in range(1, max_m + 1):
            resp = api_post(
                f"{DPE_PUBLIC_API}/presupuesto",
                {"ruc": ruc, "year": year, "month": month},
            )
            if resp:  # respuesta no vacia = datos publicados
                avail.append(month)
        coverage[str(year)] = avail
        time.sleep(0.1)  # rate limiting suave

    # Score: 5pts/mes-2025, 8pts/mes-2026
    score = len(coverage.get("2025", [])) * 5 + len(coverage.get("2026", [])) * 8
    return {"cobertura_por_anio": coverage, "score": score}


def check_annual_report(establishment_id: int) -> dict | None:
    """Verifica si hay reporte anual disponible para la entidad."""
    resp = api_get(
        f"{DPE_TRANSP_API}/anual-report/establishment?establishment_id={establishment_id}"
    )
    if resp and isinstance(resp, dict):
        records = resp.get("list", [])
        if records:
            latest = records[0]
            return {
                "year":         latest.get("year"),
                "file_path":    latest.get("file"),
                "created_at":   latest.get("created_at", "")[:10],
            }
    return None


def analyze_municipality(muni: dict, max_month_2026: int = 5) -> dict:
    """
    Análisis completo de un GAD Municipal.

    Returns:
        dict con coverage, score, viabilidad y metadatos
    """
    ruc = muni["ruc"]
    eid = muni["id"]

    # 1. Cobertura presupuestaria
    coverage = check_presupuesto_coverage(ruc, max_month_2026=max_month_2026)

    # 2. Reporte anual (solo si tiene datos 2025)
    annual = None
    if coverage["cobertura_por_anio"].get("2025"):
        annual = check_annual_report(eid)

    # 3. Viabilidad: score >= 60 (al menos 6 meses 2025 + algo 2026)
    viable = coverage["score"] >= 60

    return {
        **muni,
        "cobertura":    coverage["cobertura_por_anio"],
        "score":        coverage["score"],
        "viable":       viable,
        "reporte_anual": annual,
        "meses_2025":   len(coverage["cobertura_por_anio"].get("2025", [])),
        "meses_2026":   len(coverage["cobertura_por_anio"].get("2026", [])),
    }


# ══════════════════════════════════════════════════════════════════════════════
# FASE 3: RANKING Y REPORTE
# ══════════════════════════════════════════════════════════════════════════════

def build_ranking(results: list[dict]) -> dict:
    """Construye el reporte final con ranking de candidatos."""
    viable    = sorted(
        [r for r in results if r.get("viable")],
        key=lambda r: (-r.get("score", 0), r["nombre"]),
    )
    no_viable = [r for r in results if not r.get("viable")]

    # Prioridad: Manabí primero (misma provincia que Montecristi)
    priority = [r for r in viable if r.get("provincia_id") in PRIORITY_PROVINCES]
    others   = [r for r in viable if r not in priority]
    ranked   = priority + others

    report = {
        "_meta": {
            "generado_en":       datetime.now().isoformat(),
            "script":            "rc_scout.py v2.0",
            "portal":            DPE_BASE,
            "total_escaneados":  len(results),
            "total_viable":      len(viable),
        },
        "recomendacion":        ranked[:3],
        "todos_viables":        ranked,
        "no_viable":            no_viable[:20],
    }

    report_path = OUT_DIR / "scouting_report.json"
    save_json(report_path, report)
    log(f"Reporte guardado -> {report_path}", "OK")

    # Resumen consola
    print("\n" + "=" * 65)
    print("  RC-SCOUT v2.0 -- TOP CANDIDATOS PARA EXPANSION QUIRA")
    print("=" * 65)
    for i, r in enumerate(ranked[:5], 1):
        poa = "[POA-SI]" if r.get("reporte_anual") else "[POA-?]"
        print(f"  {i}. {r['nombre'][:55]}")
        print(f"     {r['provincia']:15s} | Score:{r['score']:3d}pts | "
              f"2025:{r['meses_2025']:2d}/12 | 2026:{r['meses_2026']:2d}/4 | {poa}")
    print("=" * 65)

    return report


# ══════════════════════════════════════════════════════════════════════════════
# DESCARGA DE ARCHIVOS VIA PLAYWRIGHT (OPCIONAL)
# ══════════════════════════════════════════════════════════════════════════════

def download_municipality_files(
    establishment_id: int,
    ruc: str,
    years: list[int] | None = None,
    headless: bool = True,
) -> list[str]:
    """
    Descarga los archivos presupuestarios de un municipio via Playwright.
    Usa el portal DPE directamente (maneja cookies y auth automáticamente).

    Nota: El campo url_download de la API tiene paths incorrectos (bug DPE).
    Por eso se usa Playwright para descarga real.

    Returns:
        Lista de rutas de archivos descargados.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("Playwright no instalado. Instalar con: pip install playwright && playwright install chromium", "ERR")
        return []

    if years is None:
        years = [2025, 2026]

    muni_dir = OUT_DIR / str(establishment_id)
    muni_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[str] = []

    # Obtener lista de archivos via API
    file_records: list[dict] = []
    for year in years:
        max_m = 5 if year == 2026 else 12
        for month in range(1, max_m + 1):
            resp = api_post(
                f"{DPE_PUBLIC_API}/presupuesto",
                {"ruc": ruc, "year": year, "month": month},
            )
            if resp:
                for record in resp:
                    for f in record.get("files", []):
                        file_records.append({
                            "year": year,
                            "month": month,
                            "name": f.get("name", ""),
                            "description": f.get("description", ""),
                            "file_id": f.get("id"),
                            "url_hint": f.get("url_download", ""),
                        })

    if not file_records:
        log("No se encontraron archivos via API", "WARN")
        return []

    log(f"Archivos a descargar: {len(file_records)}", "STEP")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless, slow_mo=300)
        ctx = browser.new_context(
            accept_downloads=True,
            locale="es-EC",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120.0.0.0"
            ),
        )
        page = ctx.new_page()
        page.set_default_timeout(30_000)

        try:
            # Navegar a la pagina de la entidad para obtener cookies
            entity_url = f"{DPE_BASE}/entidades/{establishment_id}"
            log(f"Cargando pagina de entidad: {entity_url}", "STEP")
            page.goto(entity_url, wait_until="networkidle", timeout=30_000)
            time.sleep(2)

            # Intentar descargar cada archivo
            for fr in file_records[:20]:  # max 20 archivos
                try:
                    fname = f"{fr['year']:04d}_{fr['month']:02d}_{fr['name'].replace('/', '-').replace(' ', '_')}"
                    dest  = muni_dir / fname

                    # Intentar descarga via URL directa desde la pagina con cookies
                    hint_url = f"{DPE_BASE}{fr['url_hint']}" if fr.get("url_hint") else None
                    if hint_url:
                        try:
                            with page.expect_download(timeout=15_000) as dl:
                                page.goto(hint_url, wait_until="commit", timeout=15_000)
                            dl.value.save_as(str(dest))
                            size = dest.stat().st_size
                            log(f"[DL] {fname} ({size:,}b)", "OK")
                            downloaded.append(str(dest))
                            continue
                        except Exception:
                            pass  # Fallback: intentar click en el enlace de la pagina

                except Exception as e:
                    log(f"Descarga fallida para {fr.get('name','?')}: {e}", "WARN")

        finally:
            ctx.close()
            browser.close()

    return downloaded


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="RC-SCOUT v2.0 — Exploracion municipal LOTAIP via REST API | QUIRA OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/rc_scout.py --list --province manabi
  python scripts/rc_scout.py --scan --province manabi
  python scripts/rc_scout.py --scan --all
  python scripts/rc_scout.py --report
  python scripts/rc_scout.py --download --id 936
""",
    )
    parser.add_argument("--list",     action="store_true", help="Listar GAD Municipales via API")
    parser.add_argument("--scan",     action="store_true", help="Escanear completitud presupuestaria")
    parser.add_argument("--report",   action="store_true", help="Mostrar reporte existente")
    parser.add_argument("--download", action="store_true", help="Descargar archivos de un municipio")
    parser.add_argument("--id",       type=int,  default=None, help="ID del municipio para --download")
    parser.add_argument("--ruc",      type=str,  default=None, help="RUC alternativo para --download")
    parser.add_argument("--province", type=str,  default=None, help="Filtrar por provincia (ej: manabi)")
    parser.add_argument("--all",      action="store_true",     help="Escanear todas las provincias (lento)")
    parser.add_argument("--visible",  action="store_true",     help="Mostrar ventana browser en --download")
    args = parser.parse_args()

    # Mapeo nombre → ID de provincia
    province_name_map = {v.lower().replace(" ", ""): k for k, v in PROVINCE_NAMES.items()}
    province_filter = None
    if args.province and not args.all:
        pkey = args.province.lower().replace(" ", "").replace("í", "i").replace("á", "a")
        pid  = province_name_map.get(pkey)
        if pid:
            province_filter = [pid]
            log(f"Provincia filtrada: {PROVINCE_NAMES[pid]} (id={pid})", "OK")
        else:
            # Buscar parcial
            matches = [(k, v) for k, v in PROVINCE_NAMES.items() if args.province.lower() in v.lower()]
            if matches:
                province_filter = [matches[0][0]]
                log(f"Provincia filtrada: {matches[0][1]} (id={matches[0][0]})", "OK")
            else:
                log(f"Provincia no reconocida: {args.province!r}", "WARN")

    # ── --list ─────────────────────────────────────────────────────────────────
    if args.list:
        gads = list_gad_municipales(province_filter=province_filter)
        save_json(OUT_DIR / "gad_municipales_all.json", gads)
        print(f"\n{'ID':>6} | {'RUC':>15} | {'Provincia':15} | Nombre")
        print("-" * 80)
        for g in gads[:50]:
            print(f"{g['id']:>6} | {g['ruc']:>15} | {g['provincia']:15} | {g['nombre'][:45]}")
        if len(gads) > 50:
            print(f"  ... y {len(gads)-50} más")

    # ── --scan ─────────────────────────────────────────────────────────────────
    elif args.scan:
        # Cargar lista (o descargar)
        list_path = OUT_DIR / "gad_municipales_all.json"
        if list_path.exists():
            with open(list_path, encoding="utf-8") as f:
                all_gads = json.load(f)
        else:
            all_gads = list_gad_municipales()
            save_json(list_path, all_gads)

        # Filtrar
        if province_filter:
            gads_to_scan = [g for g in all_gads if g.get("provincia_id") in province_filter]
        else:
            gads_to_scan = all_gads

        log(f"Escaneando {len(gads_to_scan)} municipios...", "STEP")

        results: list[dict] = []
        for i, gad in enumerate(gads_to_scan, 1):
            name_short = gad["nombre"].replace(
                "GOBIERNO AUTONOMO DESCENTRALIZADO MUNICIPAL DEL CANTON ", ""
            ).replace(
                "GOBIERNO AUTÓNOMO DESCENTRALIZADO MUNICIPAL DEL CANTÓN ", ""
            )[:30]
            log(f"[{i:02d}/{len(gads_to_scan)}] {name_short}", "STEP")
            result = analyze_municipality(gad)
            results.append(result)

            # Guardar progreso incremental
            save_json(OUT_DIR / "scan_progress.json", results)
            time.sleep(0.3)

        build_ranking(results)

    # ── --report ───────────────────────────────────────────────────────────────
    elif args.report:
        report_path = OUT_DIR / "scouting_report.json"
        if not report_path.exists():
            log("No hay reporte. Ejecuta --scan primero.", "ERR")
            return
        with open(report_path, encoding="utf-8") as f:
            report = json.load(f)

        meta = report.get("_meta", {})
        print(f"\nReporte generado: {meta.get('generado_en','?')[:19]}")
        print(f"Total escaneados: {meta.get('total_escaneados','?')}")
        print(f"Total viables:    {meta.get('total_viable','?')}")
        print()
        print("=== RECOMENDACION QUIRA ===")
        for r in report.get("recomendacion", []):
            print(f"  [{r['id']}] {r['nombre'][:55]}")
            print(f"       RUC: {r['ruc']} | {r['provincia']} | Score: {r.get('score',0)}")
            print(f"       2025: {r.get('meses_2025',0)}/12 meses | 2026: {r.get('meses_2026',0)}/4 meses")
            print()

    # ── --download ─────────────────────────────────────────────────────────────
    elif args.download:
        if not args.id:
            # Default: usar los candidatos del reporte
            report_path = OUT_DIR / "scouting_report.json"
            if report_path.exists():
                with open(report_path, encoding="utf-8") as f:
                    rpt = json.load(f)
                for cand in rpt.get("recomendacion", [])[:2]:
                    log(f"Descargando: {cand['nombre'][:50]}", "STEP")
                    download_municipality_files(
                        cand["id"], cand["ruc"], headless=not args.visible
                    )
            else:
                log("Usa --id para especificar el ID del municipio o ejecuta --scan primero", "ERR")
        else:
            # Obtener RUC del ID
            ruc = args.ruc
            if not ruc:
                entity = api_get(f"{DPE_ADMIN_API}/establishment/{args.id}")
                if entity:
                    ruc = entity.get("identification", "")
                    name = entity.get("name", str(args.id))
                    log(f"Entidad: {name}", "OK")
                    log(f"RUC: {ruc}", "OK")
            if ruc:
                download_municipality_files(args.id, ruc, headless=not args.visible)
            else:
                log(f"No se encontro el municipio con ID {args.id}", "ERR")

    else:
        parser.print_help()
        print("\nInicio rapido:")
        print("  python scripts/rc_scout.py --list --province manabi")
        print("  python scripts/rc_scout.py --scan --province manabi")
        print("  python scripts/rc_scout.py --report")


if __name__ == "__main__":
    main()
