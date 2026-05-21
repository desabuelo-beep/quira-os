#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/rc_scout.py — QUIRA OS · RC-SCOUT v1.0
Motor de Exploración Municipal — Playwright + LOTAIP

Fuentes públicas oficiales:
  • Portal Nacional de Transparencia (DPE):
      https://transparencia.dpe.gob.ec
      → Literal 6 / Numeral 6: Presupuesto mensual (Excel/CSV)
      → Literal 9 / Numeral 9: POA (PDF)
  • SERCOP:
      https://www.compraspublicas.gob.ec
      → PAC (Plan Anual de Contrataciones) (PDF)

Modos de uso:
    # Fase 1: Explorar estructura del portal (toma screenshots, mapea DOM)
    python scripts/rc_scout.py --discover

    # Fase 2: Escanear todos los GAD Municipales y puntuar completitud
    python scripts/rc_scout.py --scan [--province manabi]

    # Fase 3: Descargar documentos de un municipio específico
    python scripts/rc_scout.py --download --code 130801

    # Flujo completo: scan + auto-descargar top candidatos
    python scripts/rc_scout.py --scan --auto-download --top 5

Salida:
    data/scouting/scouting_report.json   — ranking de municipios candidatos
    data/scouting/{code}/               — archivos descargados por municipio

Dylus Lab © 2026 · Datos públicos LOTAIP — Ecuador
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Dependencias externas ─────────────────────────────────────────────────────
try:
    from playwright.sync_api import sync_playwright, Page, Browser, TimeoutError as PWTimeout
except ImportError:
    print("ERROR: Playwright no instalado.")
    print("  pip install playwright && playwright install chromium")
    sys.exit(1)


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════════════

OUT_DIR  = Path(__file__).parent.parent / "data" / "scouting"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Portales
PORTAL_DPE   = "https://transparencia.dpe.gob.ec"
PORTAL_SERCOP = "https://www.compraspublicas.gob.ec"

# Períodos objetivo
TARGET_YEAR_PRIMARY   = 2025
TARGET_YEAR_SECONDARY = 2026
MIN_MONTHS_2025 = 10   # al menos 10 meses de 2025 para calificar

# Años en que las metas PDOT coinciden con el horizonte de Montecristi (2023-2027)
PDOT_COMPATIBLE_YEARS = [2023, 2024, 2025, 2026, 2027]

# Provincias prioritarias para comparabilidad con Montecristi (Manabí)
PRIORITY_PROVINCES = ["Manabí", "Esmeraldas", "Santa Elena", "Los Ríos"]

# Literales LOTAIP relevantes
LITERAL_PRESUPUESTO = "6"   # Numeral/Literal 6 — Presupuesto institucional
LITERAL_POA         = "9"   # Numeral/Literal 9 — POA

MESES = {
    1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
    5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto",
    9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre",
}


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def log(msg: str, level: str = "INFO") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    prefix = {"INFO": "·", "OK": "✓", "WARN": "⚠", "ERR": "✗", "STEP": "▶"}.get(level, "·")
    print(f"[{ts}] {prefix} {msg}", flush=True)


def safe_mkdir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def screenshot(page: Page, name: str) -> None:
    """Guarda screenshot en data/scouting/screenshots/"""
    ss_dir = safe_mkdir(OUT_DIR / "screenshots")
    path   = ss_dir / f"{name}_{datetime.now().strftime('%H%M%S')}.png"
    try:
        page.screenshot(path=str(path))
        log(f"Screenshot → {path.name}", "OK")
    except Exception as e:
        log(f"Screenshot fallido: {e}", "WARN")


def wait_for_content(page: Page, timeout_ms: int = 15_000) -> None:
    """Espera a que el portal JS cargue contenido real."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout_ms)
    except PWTimeout:
        pass
    time.sleep(1.5)   # margen adicional para renders lentos


# ══════════════════════════════════════════════════════════════════════════════
# FASE 0: DESCUBRIMIENTO — mapear estructura del portal
# ══════════════════════════════════════════════════════════════════════════════

def phase_discover(page: Page) -> dict:
    """
    Navega el portal DPE y mapea su estructura.
    Objetivo: identificar:
      - Cómo filtrar por tipo de institución (GAD Municipal)
      - Cómo acceder a cada institución
      - Cómo navegar a los literales de presupuesto y POA
      - Patrones de URL / selectores CSS

    Devuelve un dict con los hallazgos para que el analista ajuste SELECTORS.
    """
    log("Iniciando fase de descubrimiento", "STEP")
    findings: dict = {"portals": {}, "selectors": {}, "url_patterns": [], "notes": []}

    # ── Portal DPE ────────────────────────────────────────────────────────────
    log(f"Navegando {PORTAL_DPE}", "STEP")
    page.goto(PORTAL_DPE, wait_until="domcontentloaded", timeout=30_000)
    wait_for_content(page)
    screenshot(page, "00_dpe_home")

    title = page.title()
    log(f"Título: {title}", "OK")
    findings["portals"]["dpe"] = {"url": PORTAL_DPE, "title": title}

    # Extraer todos los links visibles
    links = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('a[href]'))
            .map(a => ({text: a.innerText.trim().slice(0,80), href: a.href}))
            .filter(l => l.text.length > 2)
            .slice(0, 50)
    }""")
    log(f"Links encontrados: {len(links)}", "OK")
    findings["portals"]["dpe"]["sample_links"] = links[:20]

    # Buscar inputs de búsqueda
    inputs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('input, select, button'))
            .map(el => ({tag: el.tagName, type: el.type||'', id: el.id||'',
                         name: el.name||'', placeholder: el.placeholder||'',
                         class: el.className.slice(0,60), text: el.innerText?.slice(0,40)||''}))
            .slice(0, 30)
    }""")
    findings["portals"]["dpe"]["form_elements"] = inputs

    # Intentar buscar "GAD Municipal" en el portal
    search_terms = ["GAD Municipal", "municipal", "gobierno autónomo", "municipio"]
    for term in search_terms:
        try:
            # Intentar campo de búsqueda con selector genérico
            search_box = page.query_selector("input[type='search'], input[placeholder*='buscar' i], input[placeholder*='search' i], input[type='text']")
            if search_box:
                search_box.fill(term)
                search_box.press("Enter")
                wait_for_content(page)
                screenshot(page, f"01_search_{term.replace(' ','_')}")
                results_text = page.inner_text("body")[:2000]
                findings["portals"]["dpe"][f"search_{term}"] = results_text[:500]
                log(f"Búsqueda '{term}': OK", "OK")
                break
        except Exception as e:
            log(f"Búsqueda fallida para '{term}': {e}", "WARN")

    # ── Intentar URL directa de instituciones ────────────────────────────────
    institution_urls = [
        f"{PORTAL_DPE}/index.php/instituciones",
        f"{PORTAL_DPE}/index.php/component/transparencia/",
        f"{PORTAL_DPE}/instituciones",
        f"{PORTAL_DPE}/entidades",
    ]
    for url in institution_urls:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15_000)
            wait_for_content(page)
            if page.url != PORTAL_DPE and "404" not in page.title().lower():
                screenshot(page, f"02_instituciones_{url.split('/')[-1]}")
                findings["url_patterns"].append({"url": url, "title": page.title(), "final_url": page.url})
                log(f"URL instituciones válida: {page.url}", "OK")
                break
        except Exception:
            pass

    # Texto completo del home para análisis
    try:
        body_text = page.inner_text("body")
        findings["portals"]["dpe"]["body_sample"] = body_text[:1000]
    except Exception:
        pass

    log("Descubrimiento completado", "OK")
    return findings


# ══════════════════════════════════════════════════════════════════════════════
# SELECTORES — ajustar después de fase de descubrimiento
# ══════════════════════════════════════════════════════════════════════════════
# Estos selectores son candidatos basados en patrones LOTAIP conocidos.
# Si el descubrimiento muestra selectores diferentes, actualizar aquí.

SELECTORS = {
    # Campo de búsqueda de institución
    "search_input": "input[type='search'], input[placeholder*='buscar' i], input[type='text']:first-of-type",
    # Tipo de institución (dropdown)
    "tipo_institucion": "select[name*='tipo' i], select[id*='tipo' i], select[class*='tipo' i]",
    # Valor GAD Municipal en el dropdown de tipo
    "valor_gad_municipal": "GAD Municipal",
    # Lista de resultados de instituciones
    "institution_items": "tr[class*='institution'], .institution-item, .entity-row, table tbody tr",
    # Nombre de la institución dentro del item
    "institution_name": "td:first-child, .name, [class*='nombre']",
    # Link a página de institución
    "institution_link": "a[href*='institucion'], a[href*='entity'], a[href*='lotaip']",
    # Sección de literales LOTAIP
    "literal_section": "a[href*='literal'], button[class*='literal'], [class*='numeral']",
    # Archivos descargables
    "download_links": "a[href$='.xlsx'], a[href$='.xls'], a[href$='.csv'], a[href$='.pdf']",
}


# ══════════════════════════════════════════════════════════════════════════════
# FASE 1: ENUMERACIÓN DE GAD MUNICIPALES
# ══════════════════════════════════════════════════════════════════════════════

def get_gad_list(page: Page, province_filter: str | None = None) -> list[dict]:
    """
    Obtiene la lista de GAD Municipales del portal.
    Retorna lista de dicts: {code, name, province, url}
    """
    log("Enumerando GAD Municipales", "STEP")
    gads: list[dict] = []

    page.goto(PORTAL_DPE, wait_until="domcontentloaded", timeout=30_000)
    wait_for_content(page)

    # Intentar filtrar por tipo GAD Municipal
    try:
        tipo_select = page.query_selector(SELECTORS["tipo_institucion"])
        if tipo_select:
            tipo_select.select_option(label=SELECTORS["valor_gad_municipal"])
            wait_for_content(page)
            screenshot(page, "10_gad_filter")
            log("Filtro GAD Municipal aplicado", "OK")
    except Exception as e:
        log(f"Filtro de tipo fallido: {e} — continuando sin filtro", "WARN")

    # Extraer lista
    rows = page.query_selector_all(SELECTORS["institution_items"])
    log(f"Filas encontradas: {len(rows)}", "OK")

    for row in rows:
        try:
            name_el = row.query_selector(SELECTORS["institution_name"])
            link_el = row.query_selector("a[href]")
            name  = name_el.inner_text().strip() if name_el else row.inner_text().strip()[:80]
            url   = link_el.get_attribute("href") if link_el else ""

            # Filtrar solo GAD Municipales (si el portal mezcla tipos)
            if not any(kw in name.upper() for kw in ["GAD", "GOBIERNO AUTÓNOMO", "MUNICIPAL", "MUNICIPIO"]):
                continue
            if province_filter and province_filter.upper() not in name.upper():
                continue

            # Extraer código del URL (patrón típico: ?id=130801 o /130801/)
            code_match = re.search(r'(\d{6})', url or "")
            code = code_match.group(1) if code_match else f"unknown_{len(gads):03d}"

            gads.append({"code": code, "name": name, "province": _extract_province(name), "url": url})
        except Exception:
            continue

    log(f"GAD Municipales encontrados: {len(gads)}", "OK")
    return gads


def _extract_province(name: str) -> str:
    """Intenta extraer la provincia del nombre de la institución."""
    known_provinces = [
        "Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo", "Cotopaxi",
        "El Oro", "Esmeraldas", "Galápagos", "Guayas", "Imbabura", "Loja",
        "Los Ríos", "Manabí", "Morona Santiago", "Napo", "Orellana",
        "Pastaza", "Pichincha", "Santa Elena", "Santo Domingo", "Sucumbíos",
        "Tungurahua", "Zamora Chinchipe",
    ]
    name_upper = name.upper()
    for prov in known_provinces:
        if prov.upper() in name_upper:
            return prov
    return "Desconocida"


# ══════════════════════════════════════════════════════════════════════════════
# FASE 2: ANÁLISIS DE COMPLETITUD POR MUNICIPIO
# ══════════════════════════════════════════════════════════════════════════════

def analyze_municipality(page: Page, gad: dict) -> dict:
    """
    Para un GAD dado, analiza la completitud de datos en DPE:
      - Presupuesto mensual 2025 (cuántos meses disponibles)
      - Presupuesto 2026 (disponible?)
      - POA 2025 (disponible?)
    Retorna un dict de análisis.
    """
    result = {
        "code":           gad["code"],
        "name":           gad["name"],
        "province":       gad["province"],
        "portal_url":     gad.get("url", ""),
        "presupuesto_2025_months": [],
        "presupuesto_2026_months": [],
        "poa_2025":               False,
        "poa_2026":               False,
        "pac_sercop":             None,
        "score_completitud":      0,
        "viable":                 False,
        "download_urls":          {"presupuesto": [], "poa": [], "pac": []},
        "errors":                 [],
    }

    url = gad.get("url", "")
    if not url:
        result["errors"].append("URL de institución no disponible")
        return result

    # Navegar a la página de la institución
    try:
        full_url = url if url.startswith("http") else f"{PORTAL_DPE}{url}"
        page.goto(full_url, wait_until="domcontentloaded", timeout=20_000)
        wait_for_content(page)
    except Exception as e:
        result["errors"].append(f"Navegación fallida: {e}")
        return result

    # Buscar literal de presupuesto (literal 6)
    _find_presupuesto(page, result)

    # Buscar literal de POA (literal 9)
    _find_poa(page, result)

    # Calcular score
    n2025 = len(result["presupuesto_2025_months"])
    n2026 = len(result["presupuesto_2026_months"])
    score = n2025 * 5   # 5 pts por mes 2025
    score += n2026 * 8  # 8 pts por mes 2026 (más reciente = más valioso)
    score += 10 if result["poa_2025"] else 0
    score += 15 if result["poa_2026"] else 0
    result["score_completitud"] = score

    # Viable si tiene >= MIN_MONTHS_2025 meses de 2025
    result["viable"] = n2025 >= MIN_MONTHS_2025

    return result


def _find_presupuesto(page: Page, result: dict) -> None:
    """Encuentra y registra los meses disponibles de presupuesto."""
    try:
        # Buscar links o secciones relacionadas con "presupuesto" / "literal 6" / "numeral 6"
        budget_links = page.evaluate("""(literal) => {
            const all = Array.from(document.querySelectorAll('a, button, td, li'));
            return all
                .filter(el => {
                    const txt = (el.innerText || el.textContent || '').toLowerCase();
                    return txt.includes('presupuesto') || txt.includes('numeral 6') ||
                           txt.includes('literal 6') || txt.includes('numeral e');
                })
                .map(el => ({
                    text: (el.innerText || el.textContent || '').trim().slice(0, 80),
                    href: el.tagName === 'A' ? el.href : (el.querySelector('a')?.href || ''),
                    tag:  el.tagName
                }))
                .slice(0, 20);
        }""", LITERAL_PRESUPUESTO)

        for link in budget_links:
            href = link.get("href", "")
            text = link.get("text", "")
            # Detectar año y mes
            year_match  = re.search(r'20(25|26)', text + href)
            month_match = re.search(
                r'(enero|febrero|marzo|abril|mayo|junio|julio|agosto|'
                r'septiembre|octubre|noviembre|diciembre)', text.lower()
            )
            if year_match:
                year = int("20" + year_match.group(1))
                if href and any(href.endswith(ext) for ext in [".xlsx", ".xls", ".csv", ".pdf"]):
                    month = _month_name_to_num(month_match.group(1) if month_match else "")
                    target = result[f"presupuesto_{year}_months"]
                    if month and month not in target:
                        target.append(month)
                    if href not in result["download_urls"]["presupuesto"]:
                        result["download_urls"]["presupuesto"].append(href)

    except Exception as e:
        result["errors"].append(f"Error buscando presupuesto: {e}")


def _find_poa(page: Page, result: dict) -> None:
    """Encuentra y registra la disponibilidad del POA."""
    try:
        poa_links = page.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('a, button, td, li'));
            return all
                .filter(el => {
                    const txt = (el.innerText || el.textContent || '').toLowerCase();
                    return txt.includes('poa') || txt.includes('plan operativo') ||
                           txt.includes('numeral 9') || txt.includes('literal 9');
                })
                .map(el => ({
                    text: (el.innerText || el.textContent || '').trim().slice(0, 80),
                    href: el.tagName === 'A' ? el.href : (el.querySelector('a')?.href || '')
                }))
                .slice(0, 10);
        }""")

        for link in poa_links:
            href = link.get("href", "")
            text = link.get("text", "")
            if "2025" in text + href:
                result["poa_2025"] = True
                if href and href not in result["download_urls"]["poa"]:
                    result["download_urls"]["poa"].append(href)
            if "2026" in text + href:
                result["poa_2026"] = True
                if href and href not in result["download_urls"]["poa"]:
                    result["download_urls"]["poa"].append(href)

    except Exception as e:
        result["errors"].append(f"Error buscando POA: {e}")


def _month_name_to_num(name: str) -> int | None:
    map_ = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    }
    return map_.get(name.lower().strip())


# ══════════════════════════════════════════════════════════════════════════════
# FASE 3: SERCOP — PAC por municipio
# ══════════════════════════════════════════════════════════════════════════════

def check_sercop_pac(page: Page, municipio_name: str) -> dict:
    """
    Busca el PAC del municipio en SERCOP.
    Retorna {found: bool, year: int, url: str, pac_items: int}
    """
    result = {"found": False, "year": None, "url": None, "pac_items": 0}
    try:
        search_url = (
            f"{PORTAL_SERCOP}/ProcesoContratacion/compras/PC/buscarProceso.cpe"
            f"?tipoBusqueda=simple&busqueda={municipio_name.replace(' ','+')}+PAC"
        )
        page.goto(search_url, wait_until="domcontentloaded", timeout=20_000)
        wait_for_content(page)

        # Contar resultados
        rows = page.query_selector_all("table tbody tr")
        result["pac_items"] = len(rows)
        result["found"]     = len(rows) > 0
        result["url"]       = page.url

        log(f"SERCOP {municipio_name}: {len(rows)} procesos encontrados", "OK")
    except Exception as e:
        log(f"SERCOP lookup fallido para {municipio_name}: {e}", "WARN")
    return result


# ══════════════════════════════════════════════════════════════════════════════
# FASE 4: DESCARGA DE ARCHIVOS
# ══════════════════════════════════════════════════════════════════════════════

def download_files(page: Page, result: dict) -> list[str]:
    """
    Descarga los archivos identificados para un municipio.
    Retorna lista de rutas descargadas.
    """
    muni_dir  = safe_mkdir(OUT_DIR / result["code"])
    downloaded: list[str] = []

    all_urls = (
        result["download_urls"]["presupuesto"] +
        result["download_urls"]["poa"] +
        result["download_urls"]["pac"]
    )

    for url in all_urls[:20]:   # máximo 20 archivos por municipio
        if not url or not url.startswith("http"):
            continue
        try:
            # Extraer nombre del archivo
            fname = url.split("/")[-1].split("?")[0]
            if not fname:
                fname = f"archivo_{len(downloaded):02d}.pdf"
            dest = muni_dir / fname

            # Descargar con Playwright (maneja cookies de sesión)
            with page.expect_download() as dl_info:
                page.goto(url, wait_until="domcontentloaded", timeout=15_000)
            download = dl_info.value
            download.save_as(str(dest))
            downloaded.append(str(dest))
            log(f"↓ {fname}", "OK")
        except Exception as e:
            log(f"Descarga fallida {url}: {e}", "WARN")

    return downloaded


# ══════════════════════════════════════════════════════════════════════════════
# FASE 5: REPORTE FINAL
# ══════════════════════════════════════════════════════════════════════════════

def build_report(results: list[dict], discovery: dict | None = None) -> dict:
    """Construye el reporte final de scouting."""
    viable     = [r for r in results if r.get("viable")]
    no_viable  = [r for r in results if not r.get("viable")]

    # Ordenar por score
    viable.sort(key=lambda r: r.get("score_completitud", 0), reverse=True)

    # Prioridad provincial (Manabí primero)
    priority = [r for r in viable if r.get("province") in PRIORITY_PROVINCES]
    other    = [r for r in viable if r not in priority]
    ranked   = priority + other

    report = {
        "_meta": {
            "generado_en":      datetime.now().isoformat(),
            "script":           "rc_scout.py v1.0",
            "target_year":      TARGET_YEAR_PRIMARY,
            "min_months_2025":  MIN_MONTHS_2025,
            "total_scanned":    len(results),
            "total_viable":     len(viable),
        },
        "top_candidatos":  ranked[:10],
        "recomendacion":   ranked[:2] if len(ranked) >= 2 else ranked,
        "no_viable":       no_viable[:20],
        "discovery":       discovery or {},
    }

    # Salvar
    report_path = OUT_DIR / "scouting_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    log(f"Reporte guardado → {report_path}", "OK")

    # Resumen en consola
    print("\n" + "═" * 60)
    print("  RC-SCOUT — TOP CANDIDATOS PARA EXPANSIÓN QUIRA")
    print("═" * 60)
    for i, r in enumerate(ranked[:5], 1):
        months_2025 = len(r.get("presupuesto_2025_months", []))
        months_2026 = len(r.get("presupuesto_2026_months", []))
        poa_flag    = "✓ POA" if r.get("poa_2025") else "✗ POA"
        print(f"  {i}. {r['name']}")
        print(f"     {r['province']} · Score: {r['score_completitud']}pts")
        print(f"     2025: {months_2025}/12 meses · 2026: {months_2026} meses · {poa_flag}")
    print("═" * 60)

    return report


# ══════════════════════════════════════════════════════════════════════════════
# ORQUESTADOR PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def run(
    mode: str         = "scan",
    province: str     | None = None,
    target_code: str  | None = None,
    auto_download: bool = False,
    top_n: int          = 5,
    headless: bool      = True,
) -> dict:
    """
    Orquestador RC-SCOUT.

    Args:
        mode:          "discover" | "scan" | "download"
        province:      Filtrar por provincia (opcional)
        target_code:   Código de municipio específico para "download"
        auto_download: Descargar automáticamente top candidatos
        top_n:         Cuántos candidatos descargar en auto-download
        headless:      Ocultar ventana del browser (False = visible)
    """
    log(f"RC-SCOUT iniciando — modo: {mode}", "STEP")
    report: dict = {}

    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=headless, slow_mo=200)
        context = browser.new_context(
            accept_downloads=True,
            locale="es-EC",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page: Page = context.new_page()
        page.set_default_timeout(20_000)

        try:
            if mode == "discover":
                discovery = phase_discover(page)
                report    = {"discovery": discovery}
                disc_path = OUT_DIR / "discovery.json"
                with open(disc_path, "w", encoding="utf-8") as f:
                    json.dump(discovery, f, ensure_ascii=False, indent=2)
                log(f"Discovery guardado → {disc_path}", "OK")

            elif mode == "scan":
                discovery = None
                gads      = get_gad_list(page, province_filter=province)
                if not gads:
                    log("No se encontraron GAD — ejecuta --discover primero para ajustar selectores", "WARN")
                    # Modo demo: retornar estructura vacía para que el analista ajuste
                    report = build_report([])
                else:
                    results: list[dict] = []
                    for i, gad in enumerate(gads):
                        log(f"[{i+1}/{len(gads)}] {gad['name']}", "STEP")
                        analysis = analyze_municipality(page, gad)
                        # SERCOP check (solo si tiene datos en DPE)
                        if analysis["viable"]:
                            pac = check_sercop_pac(page, gad["name"])
                            analysis["pac_sercop"] = pac
                        results.append(analysis)

                        # Guardar progreso incremental
                        prog_path = OUT_DIR / "scan_progress.json"
                        with open(prog_path, "w", encoding="utf-8") as f:
                            json.dump(results, f, ensure_ascii=False, indent=2)

                    report = build_report(results, discovery)

                    # Auto-download top candidatos
                    if auto_download and report.get("top_candidatos"):
                        for cand in report["top_candidatos"][:top_n]:
                            log(f"Descargando archivos: {cand['name']}", "STEP")
                            downloaded = download_files(page, cand)
                            cand["downloaded_files"] = downloaded

            elif mode == "download":
                if not target_code:
                    log("--download requiere --code XXXXXX", "ERR")
                else:
                    # Cargar resultado previo del scan
                    prog_path = OUT_DIR / "scouting_report.json"
                    if prog_path.exists():
                        with open(prog_path, encoding="utf-8") as f:
                            prev = json.load(f)
                        all_results = prev.get("top_candidatos", []) + prev.get("no_viable", [])
                        target = next((r for r in all_results if r["code"] == target_code), None)
                        if target:
                            downloaded = download_files(page, target)
                            log(f"Archivos descargados: {len(downloaded)}", "OK")
                            report = {"downloaded": downloaded}
                        else:
                            log(f"Código {target_code} no encontrado en reporte previo", "ERR")
                    else:
                        log("Ejecuta --scan primero para generar el reporte", "ERR")

        except Exception as e:
            log(f"Error crítico: {e}", "ERR")
            import traceback
            traceback.print_exc()
        finally:
            context.close()
            browser.close()

    return report


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="RC-SCOUT — Exploración municipal LOTAIP · QUIRA OS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--discover",      action="store_true",  help="Mapear estructura del portal")
    parser.add_argument("--scan",          action="store_true",  help="Escanear todos los GAD Municipales")
    parser.add_argument("--download",      action="store_true",  help="Descargar archivos de un municipio")
    parser.add_argument("--province",      type=str, default=None, help="Filtrar por provincia (ej: 'Manabí')")
    parser.add_argument("--code",          type=str, default=None, help="Código GAD para --download")
    parser.add_argument("--auto-download", action="store_true",  help="Descargar top candidatos automáticamente")
    parser.add_argument("--top",           type=int, default=3,   help="Cuántos candidatos en auto-download")
    parser.add_argument("--visible",       action="store_true",  help="Mostrar ventana del browser (debug)")
    args = parser.parse_args()

    if args.discover:
        mode = "discover"
    elif args.scan:
        mode = "scan"
    elif args.download:
        mode = "download"
    else:
        parser.print_help()
        print("\nEjemplo de inicio rápido:")
        print("  python scripts/rc_scout.py --discover")
        print("  python scripts/rc_scout.py --scan --province Manabí")
        sys.exit(0)

    run(
        mode=mode,
        province=args.province,
        target_code=args.code,
        auto_download=args.auto_download,
        top_n=args.top,
        headless=not args.visible,
    )


if __name__ == "__main__":
    main()
