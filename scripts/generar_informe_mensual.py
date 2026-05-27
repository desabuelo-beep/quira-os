#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/generar_informe_mensual.py — QUIRA Intelligence · Sprint 3 Semana 4
Generador del Informe Longitudinal Institucional.

Produce el primer documento de memoria institucional operacional:
  · Resumen ejecutivo: ICPI · TGI · SAT · diagnóstico global
  · Tabla RC-M canónica (Período | ICPI | D3 Ti | SAT-IV | Riesgo)
  · Dimensiones TGI D1-D5 con scores y fuentes
  · Alertas SAT activas con base legal y detalle
  · Datos financieros (presupuesto · devengado · Ti)
  · Trazabilidad y confiabilidad de fuentes
  · Metadatos del ciclo

Salidas:
  · data/informes/INFORME_YYYYMM_CODIGO.json   — estructura canónica
  · data/informes/INFORME_YYYYMM_CODIGO.md     — documento institucional

Uso:
  python scripts/generar_informe_mensual.py
  python scripts/generar_informe_mensual.py --municipio 130901
  python scripts/generar_informe_mensual.py --año 2026 --mes 5

Doctrina: ver docs/MONTHLY_CYCLE.md · docs/ARQUITECTURA_CANONICA.md
Dylus Lab © 2026 — QUIRA Intelligence
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# ── Raíz del proyecto en sys.path ─────────────────────────────────────────────
_RAIZ = Path(__file__).parent.parent
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from utils.logger import get_logger

logger = get_logger("informe_mensual")

# ── Constantes ─────────────────────────────────────────────────────────────────
MUNICIPIO_CANONICO  = "130801"
MUNICIPIO_NOMBRE    = "GAD Municipal de Montecristi"
RUTA_INFORMES       = _RAIZ / "data" / "informes"
RUTA_GM_SNAPSHOT    = _RAIZ / "data" / "gm_snapshot.json"
RUTA_SNAPSHOTS      = _RAIZ / "data" / "snapshots"

_SAT_DESCRIPTORES: dict[str, dict] = {
    "SAT-0":    {"nombre": "Coherencia POA-PAC",              "ley": "LOSNCP Art. 22"},
    "SAT-I":    {"nombre": "Fragmentación Selectiva",          "ley": "COPFP Art. 54"},
    "SAT-II":   {"nombre": "Reforma Significativa Tardía",     "ley": "COPFP Art. 115"},
    "SAT-III":  {"nombre": "Parálisis Presupuestaria",         "ley": "COPFP Art. 113"},
    "SAT-IV":   {"nombre": "Alerta Fiscal COOTAD",             "ley": "COOTAD Art. 192"},
    "SAT-V":    {"nombre": "Brecha Compromiso CPCCS",          "ley": "COOTAD Art. 302"},
    "SAT-VI":   {"nombre": "Desvío Presupuesto Participativo", "ley": "COOTAD Art. 238"},
    "SAT-VII":  {"nombre": "Pulso Sináptico",                  "ley": "Doctrinal"},
    "SAT-VIII": {"nombre": "Equidad Territorial",              "ley": "COOTAD Art. 238/247"},
}

_ICPI_CLASIFICACION = {
    "Excelente":         (80, 100),
    "Saludable":         (65, 79.99),
    "En Construcción":   (50, 64.99),
    "Ruptura Sistémica": (0,  49.99),
}

_RIESGO_LABEL = {
    "BAJO":    "Riesgo Bajo — sistema estable",
    "MEDIO":   "Riesgo Medio — vigilancia activa recomendada",
    "ALTO":    "Riesgo Alto — intervención institucional requerida",
    "CRÍTICO": "Riesgo Crítico — acción inmediata mandatoria",
}


# ══════════════════════════════════════════════════════════════════════════════
# Carga de datos
# ══════════════════════════════════════════════════════════════════════════════

def _cargar_gm_snapshot() -> dict:
    """Carga el snapshot JSON del Gold Master (fuente canónica de TGI y financiero)."""
    if RUTA_GM_SNAPSHOT.exists():
        return json.loads(RUTA_GM_SNAPSHOT.read_text(encoding="utf-8"))
    logger.warning("  gm_snapshot.json no encontrado — datos TGI/financiero omitidos")
    return {}


def _cargar_ultimo_snapshot_local(municipio_code: str) -> dict:
    """Carga el snapshot local más reciente para el municipio dado."""
    snap_dir = RUTA_SNAPSHOTS / municipio_code
    if not snap_dir.exists():
        return {}
    candidatos = sorted(
        [p for p in snap_dir.glob("*.json") if "provenance" not in p.name],
        reverse=True,
    )
    if not candidatos:
        return {}
    ruta = candidatos[0]
    logger.info(f"  Snapshot local: {ruta.name}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def _cargar_historial_longitudinal(municipio_code: str) -> dict:
    """Carga el resumen longitudinal RC-M vía longitudinal_engine."""
    try:
        from app.services.longitudinal_engine import get_longitudinal_summary
        return get_longitudinal_summary(municipio_code)
    except Exception as exc:
        logger.warning(f"  longitudinal_engine no disponible: {exc}")
        return {"error": str(exc), "n_periodos": 0, "rcm_table": []}


# ══════════════════════════════════════════════════════════════════════════════
# Construcción del informe
# ══════════════════════════════════════════════════════════════════════════════

def _seccion_resumen_ejecutivo(snap: dict, gm: dict, longitud: dict) -> dict:
    """Bloque de resumen ejecutivo.

    TGI = índice titular (gobernanza institucional integral, D1-D5).
    ICPI = lente complementario (progreso de ejecución, más conservador).
    Fuente canónica: Gold Master v5.5 H73_OUTPUT_API (ambos índices).
    """
    icpi_data = snap.get("icpi", {})
    icpi_pct  = icpi_data.get("global_pct") or gm.get("icpi", {}).get("global_pct")
    # Clasificación: Gold Master (gm_snapshot.json) es la fuente canónica de clasificaciones —
    # el snapshot local puede tener variantes sin tilde (pipeline v5.5).
    icpi_cls  = (
        gm.get("icpi", {}).get("clasificacion", "")
        or icpi_data.get("clasificacion", "")
    )

    if not icpi_cls and icpi_pct is not None:
        for cls, (lo, hi) in _ICPI_CLASIFICACION.items():
            if lo <= icpi_pct <= hi:
                icpi_cls = cls
                break

    # TGI: índice titular — leer del snapshot primero, fallback a gm_snapshot.json
    tgi_snap  = snap.get("tgi", {})
    tgi_data  = gm.get("tgi", {})
    tgi_score = tgi_snap.get("score") or tgi_data.get("score")

    sat_data  = snap.get("sat", {})
    riesgo    = sat_data.get("clasif_riesgo", "—").upper()
    n_activas = sat_data.get("total_activas", 0)

    return {
        "icpi_global_pct":   icpi_pct,
        "icpi_clasificacion": icpi_cls,
        "tgi_score":          tgi_score,
        "sat_riesgo":         riesgo,
        "sat_label":          _RIESGO_LABEL.get(riesgo, riesgo),
        "sat_activas":        n_activas,
        "n_periodos_rcm":     longitud.get("n_periodos", 0),
        "icpi_trend":         longitud.get("icpi_trend", "INSUFICIENTE_DATOS"),
        "diagnostico_global": _diagnostico_global(icpi_pct, icpi_cls, riesgo, n_activas),
    }


def _diagnostico_global(icpi_pct: float | None, icpi_cls: str, riesgo: str, n_activas: int) -> str:
    """Diagnóstico textual canónico del estado institucional.

    Usa la clasificación ICPI almacenada en el snapshot (fuente Gold Master),
    no recomputa rangos para evitar divergencia con la doctrina Excel.
    """
    if icpi_pct is None:
        return "Diagnóstico pendiente — ICPI no calculado en este período."

    _DIAGNOSTICO_POR_CLASIFICACION = {
        "Ruptura Sistémica": "El municipio opera por debajo del umbral mínimo de coherencia institucional. Se requiere intervención estructural urgente.",
        "En Construcción":   "El municipio muestra avances parciales pero requiere fortalecimiento estructural sostenido.",
        "Saludable":         "Gestión institucional dentro de parámetros aceptables. Mantener trayectoria.",
        "Excelente":         "Alto estándar de gestión institucional. Referente territorial.",
    }
    cls_display = icpi_cls or "—"
    descripcion = _DIAGNOSTICO_POR_CLASIFICACION.get(cls_display, "Clasificación no estándar — revisar Gold Master.")
    base = f"ICPI={icpi_pct:.2f}% ({cls_display}). {descripcion}"

    if n_activas > 0:
        base += f" {n_activas} alerta(s) SAT activa(s) requieren atención — Riesgo {riesgo}."
    else:
        base += " Sin alertas SAT activas en el período."
    return base


def _seccion_dimensiones_tgi(gm: dict) -> list[dict]:
    """Dimensiones TGI D1-D5 desde el Gold Master."""
    tgi = gm.get("tgi", {})
    dimensiones = []
    for key in ("d1", "d2", "d3", "d4", "d5"):
        dim = tgi.get(key)
        if not isinstance(dim, dict):
            continue
        dimensiones.append({
            "codigo":  dim.get("codigo", key.upper()),
            "nombre":  dim.get("nombre", "—"),
            "valor":   dim.get("valor"),
            "peso":    dim.get("peso"),
            "fuente":  dim.get("fuente", "Gold Master"),
        })
    return dimensiones


def _seccion_alertas_sat(snap: dict) -> list[dict]:
    """Lista de alertas SAT activas con base legal y detalle."""
    alertas_raw = snap.get("sat", {}).get("alertas", [])
    resultado   = []
    for a in alertas_raw:
        if not a.get("activa"):
            continue
        codigo = a.get("codigo", "")
        descriptor = _SAT_DESCRIPTORES.get(codigo, {})
        resultado.append({
            "codigo":       codigo,
            "nombre":       a.get("nombre") or descriptor.get("nombre", "—"),
            "tipo":         a.get("tipo", "—"),
            "base_legal":   a.get("base_legal_art") or descriptor.get("ley", "—"),
            "dimension":    a.get("dimension", "—"),
            "valor_obs":    a.get("valor_observado"),
            "umbral":       a.get("umbral"),
            "detalle":      a.get("detalle", "—"),
        })
    return resultado


def _seccion_financiero(snap: dict, gm: dict) -> dict:
    """Datos financieros: presupuesto, devengado, Ti."""
    fin_snap = snap.get("financiero", {})
    fin_gm   = gm.get("financiero", {})

    return {
        "presupuesto_total_2026":        fin_gm.get("presupuesto_total_gad_2026"),
        "presupuesto_codificado_inv":    fin_gm.get("presupuesto_codificado_grupos78_2026"),
        "devengado_q1_2026":             fin_gm.get("devengado_q1_2026"),
        "ti_2025_pct":                   fin_gm.get("ti_2025_pct"),
        "ti_2026_raw_pct":               fin_gm.get("ti_2026_raw_pct"),
        "ti_2026_normalizada_pct":       fin_gm.get("ti_2026_normalizada_pct"),
        "corte_datos":                   fin_gm.get("corte_datos"),
        "fondos_bloqueados_est":         fin_gm.get("fondos_bloqueados_est"),
        "fuente":                        fin_gm.get("fuente", "Gold Master v6.0"),
    }


def _seccion_trazabilidad(snap: dict) -> dict:
    """Trazabilidad y confiabilidad de fuentes."""
    sources = snap.get("sources", {})
    return {
        "traceability_score": snap.get("traceability_score"),
        "coverage_score":     snap.get("coverage_score"),
        "source_confidence":  snap.get("source_confidence"),
        "fuentes": {
            src: {
                "estado":      info.get("status", "—"),
                "reliability": info.get("reliability"),
            }
            for src, info in sources.items()
            if isinstance(info, dict)
        },
    }


# ══════════════════════════════════════════════════════════════════════════════
# Generación del Markdown institucional
# ══════════════════════════════════════════════════════════════════════════════

def _formatear_pct(valor: float | str | None, decimales: int = 2) -> str:
    if valor is None:
        return "—"
    if isinstance(valor, str):
        return valor  # ya viene formateado (p.ej. "60%")
    return f"{valor:.{decimales}f}%"


def _formatear_usd(valor: float | None) -> str:
    if valor is None:
        return "—"
    return f"${valor:,.2f}"


def _generar_markdown(
    municipio_code: str,
    año: int,
    mes: int,
    informe: dict,
) -> str:
    """Genera el documento Markdown institucional del informe."""
    ahora    = datetime.now()
    mes_es   = [
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ][mes]
    res      = informe["resumen_ejecutivo"]
    tgi_dims = informe["dimensiones_tgi"]
    alertas  = informe["alertas_sat_activas"]
    fin      = informe["financiero"]
    traz     = informe["trazabilidad"]
    rcm      = informe.get("rc_m", [])

    lineas = [
        f"# Informe Longitudinal Institucional",
        f"## GAD Municipal de Montecristi · {mes_es.capitalize()} {año}",
        f"",
        f"> **Emitido por:** QUIRA Intelligence — Dylus Lab  ",
        f"> **Fecha de emisión:** {ahora.strftime('%Y-%m-%d %H:%M')}  ",
        f"> **Código municipio:** {municipio_code}  ",
        f"> **Versión sistema:** QUIRA Intelligence v6.0  ",
        f"> **Fuente canónica:** Gold Master v5.5 (SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx)  ",
        f"> **Doctrina:** TGI Territorial · COPFP · COOTAD · LOSNCP",
        f"",
        f"---",
        f"",
        f"## 1. Resumen Ejecutivo",
        f"",
        f"| Indicador | Valor | Clasificación | Fuente |",
        f"|-----------|-------|---------------|--------|",
        f"| **TGI** — Gobernanza Institucional | **{_formatear_pct(res['tgi_score'], 2)}** | Índice D1-D5 ponderado | G4.2 · H73 v5.5 |",
        f"| Riesgo SAT | {res['sat_riesgo']} | {res['sat_label']} | H75/H73 v5.5 |",
        f"| ICPI — Progreso de Ejecución | {_formatear_pct(res['icpi_global_pct'])} | {res['icpi_clasificacion']} | G4.1 · H73 v5.5 |",
        f"| Alertas SAT activas | {res['sat_activas']} / 9 | — | H75 v5.5 |",
        f"| Períodos RC-M disponibles | {res['n_periodos_rcm']} | {res['icpi_trend']} | Longitudinal |",
        f"",
        f"> **TGI** = índice canónico de gobernanza institucional (D1-D5, largo plazo).  ",
        f"> **ICPI** = lente de progreso ejecutivo (velocidad de ejecución, más exigente).  ",
        f"> Ambos son complementarios — TGI es el indicador titular de QUIRA (Gold Master v5.5 canónico).",
        f"",
        f"**Diagnóstico doctrinal:**  ",
        f"{res['diagnostico_global']}",
        f"",
        f"---",
        f"",
        f"## 2. Tabla RC-M — Evolución Longitudinal",
        f"",
        f"| Período | ICPI | D3 Ti | SAT-IV | Riesgo |",
        f"|---------|------|-------|--------|--------|",
    ]

    if rcm:
        for fila in rcm:
            lineas.append(
                f"| {fila.get('periodo','—')} "
                f"| {_formatear_pct(fila.get('icpi_pct'))} "
                f"| {_formatear_pct(fila.get('d3_ti_pct'))} "
                f"| {fila.get('sat_iv','—')} "
                f"| {fila.get('riesgo','—')} |"
            )
    else:
        lineas.append("| *(sin datos históricos suficientes)* | — | — | — | — |")

    lineas += [
        f"",
        f"> Tabla RC-M: registro canónico de evolución institucional. "
        f"Mínimo 3 períodos requeridos para análisis de tendencia.",
        f"",
        f"---",
        f"",
        f"## 3. Dimensiones TGI — Desglose D1-D5",
        f"",
        f"| Dimensión | Nombre | Score | Peso | Fuente |",
        f"|-----------|--------|-------|------|--------|",
    ]

    for d in tgi_dims:
        lineas.append(
            f"| {d['codigo']} "
            f"| {d['nombre']} "
            f"| {_formatear_pct(d.get('valor'))} "
            f"| {d.get('peso', 0)*100:.0f}% "
            f"| {d['fuente'][:40]}{'…' if len(d['fuente'])>40 else ''} |"
        )

    if not tgi_dims:
        lineas.append("| *(TGI no disponible en este ciclo)* | — | — | — | — |")

    lineas += [
        f"",
        f"---",
        f"",
        f"## 4. Alertas SAT Activas",
        f"",
    ]

    if alertas:
        for a in alertas:
            lineas += [
                f"### {a['codigo']} — {a['nombre']}",
                f"",
                f"- **Tipo:** {a['tipo']}",
                f"- **Dimensión:** {a['dimension']}",
                f"- **Base legal:** {a['base_legal']}",
                f"- **Valor observado:** {_formatear_pct(a.get('valor_obs'))}",
                f"- **Umbral canónico:** {_formatear_pct(a.get('umbral'))}",
                f"- **Detalle:** {a['detalle']}",
                f"",
            ]
    else:
        lineas += [
            f"✅ **Sin alertas SAT activas en el período.**",
            f"",
            f"El municipio opera dentro de los parámetros canónicos del TGI.",
            f"",
        ]

    lineas += [
        f"---",
        f"",
        f"## 5. Datos Financieros",
        f"",
        f"| Concepto | Valor |",
        f"|----------|-------|",
        f"| Presupuesto total GAD 2026 | {_formatear_usd(fin.get('presupuesto_total_2026'))} |",
        f"| Presupuesto codificado inversión (Grupos 7+8) | {_formatear_usd(fin.get('presupuesto_codificado_inv'))} |",
        f"| Devengado Q1-2026 | {_formatear_usd(fin.get('devengado_q1_2026'))} |",
        f"| Ti 2025 (histórico) | {_formatear_pct(fin.get('ti_2025_pct'))} |",
        f"| Ti 2026 — tasa bruta | {_formatear_pct(fin.get('ti_2026_raw_pct'))} |",
        f"| Ti 2026 — normalizada | {_formatear_pct(fin.get('ti_2026_normalizada_pct'))} |",
        f"| Fondos bloqueados estimados | {_formatear_usd(fin.get('fondos_bloqueados_est'))} |",
        f"| Corte de datos | {fin.get('corte_datos','—')} |",
        f"",
        f"**Fuente:** {fin.get('fuente','—')}",
        f"",
        f"---",
        f"",
        f"## 6. Trazabilidad y Confiabilidad",
        f"",
        f"| Métrica | Valor |",
        f"|---------|-------|",
        f"| Traceability Score | {traz.get('traceability_score','—')}/100 |",
        f"| Coverage Score | {traz.get('coverage_score','—')}% |",
        f"| Source Confidence | {traz.get('source_confidence','—')} |",
        f"",
        f"**Fuentes del pipeline:**",
        f"",
        f"| Fuente | Estado | Reliability |",
        f"|--------|--------|-------------|",
    ]

    for fuente, info in (traz.get("fuentes") or {}).items():
        lineas.append(
            f"| {fuente} | {info.get('estado','—')} | {info.get('reliability','—')} |"
        )

    lineas += [
        f"",
        f"---",
        f"",
        f"## 7. Metadatos del Ciclo",
        f"",
        f"| Campo | Valor |",
        f"|-------|-------|",
        f"| Generado en | {ahora.isoformat()} |",
        f"| Municipio | {municipio_code} — GAD Municipal de Montecristi |",
        f"| Período | {año}-{mes:02d} |",
        f"| Sistema | QUIRA Intelligence v6.0 |",
        f"| Gold Master | SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx (canónico activo) |",
        f"| Script | scripts/generar_informe_mensual.py |",
        f"| Doctrina | TGI Territorial · COPFP · COOTAD · LOSNCP |",
        f"",
        f"---",
        f"",
        f"*Este informe es generado automáticamente por QUIRA Intelligence.*  ",
        f"*Dylus Lab © 2026 — Todos los derechos reservados.*  ",
        f"*El Gold Master Excel es propiedad exclusiva de Dylus Lab y no se distribuye públicamente.*",
    ]

    return "\n".join(lineas)


# ══════════════════════════════════════════════════════════════════════════════
# Función principal
# ══════════════════════════════════════════════════════════════════════════════

def generar_informe(municipio_code: str, año: int, mes: int) -> dict:
    """Genera el informe mensual completo para el municipio y período dados."""
    logger.info(f"Generando informe: {municipio_code} · {año}-{mes:02d}...")

    # ── Carga de datos ─────────────────────────────────────────────────────────
    logger.info("  Cargando datos...")
    gm       = _cargar_gm_snapshot()
    snap     = _cargar_ultimo_snapshot_local(municipio_code)
    longitud = _cargar_historial_longitudinal(municipio_code)

    # ── Secciones del informe ──────────────────────────────────────────────────
    informe = {
        "_meta": {
            "generado_en":    datetime.now().isoformat(),
            "municipio_code": municipio_code,
            "municipio_nombre": MUNICIPIO_NOMBRE if municipio_code == MUNICIPIO_CANONICO
                                else snap.get("gad", {}).get("nombre", municipio_code),
            "periodo":        f"{año}-{mes:02d}",
            "quira_version":  "v6.0",
            "script":         "scripts/generar_informe_mensual.py",
            "gold_master_version": gm.get("_meta", {}).get("version_excel", "—"),
        },
        "resumen_ejecutivo":  _seccion_resumen_ejecutivo(snap, gm, longitud),
        "rc_m":               longitud.get("rcm_table", []),
        "dimensiones_tgi":    _seccion_dimensiones_tgi(gm),
        "alertas_sat_activas": _seccion_alertas_sat(snap),
        "financiero":         _seccion_financiero(snap, gm),
        "trazabilidad":       _seccion_trazabilidad(snap),
        "longitudinal_summary": {
            k: v for k, v in longitud.items()
            if k not in ("rcm_table", "error")
        },
    }

    # ── Salidas ────────────────────────────────────────────────────────────────
    RUTA_INFORMES.mkdir(parents=True, exist_ok=True)
    nombre_base = f"INFORME_{año}{mes:02d}_{municipio_code}"

    ruta_json = RUTA_INFORMES / f"{nombre_base}.json"
    ruta_md   = RUTA_INFORMES / f"{nombre_base}.md"

    ruta_json.write_text(
        json.dumps(informe, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info(f"  JSON: {ruta_json}")

    md_contenido = _generar_markdown(municipio_code, año, mes, informe)
    ruta_md.write_text(md_contenido, encoding="utf-8")
    logger.info(f"  Markdown: {ruta_md}")

    return {
        "estado":    "ok",
        "ruta_json": str(ruta_json),
        "ruta_md":   str(ruta_md),
        "informe":   informe,
    }


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="QUIRA Intelligence — Generador del Informe Longitudinal Institucional",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/generar_informe_mensual.py
  python scripts/generar_informe_mensual.py --municipio 130901 --año 2026 --mes 4
        """,
    )
    parser.add_argument(
        "--municipio", default=MUNICIPIO_CANONICO,
        help=f"Código del municipio (por defecto: {MUNICIPIO_CANONICO} — Montecristi)",
    )
    parser.add_argument(
        "--año", type=int, default=datetime.now().year,
        help="Año del informe (por defecto: año actual)",
    )
    parser.add_argument(
        "--mes", type=int, default=datetime.now().month,
        help="Mes del informe (por defecto: mes actual)",
    )
    return parser


def main() -> int:
    parser = construir_parser()
    args   = parser.parse_args()

    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info("QUIRA Intelligence — Informe Longitudinal Institucional")
    logger.info(f"Municipio: {args.municipio} · Período: {args.año}-{args.mes:02d}")
    logger.info("=" * 60)

    resultado = generar_informe(
        municipio_code=args.municipio,
        año=args.año,
        mes=args.mes,
    )

    duracion = (datetime.now() - inicio).total_seconds()
    logger.info("=" * 60)
    logger.info(f"Informe generado en {duracion:.1f}s — Estado: {resultado['estado']}")
    logger.info(f"JSON: {resultado['ruta_json']}")
    logger.info(f"MD:   {resultado['ruta_md']}")
    logger.info("=" * 60)

    # ── Resumen a consola ──────────────────────────────────────────────────────
    res = resultado["informe"]["resumen_ejecutivo"]
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  QUIRA Intelligence — Resumen del Informe                ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  ICPI Global : {str(res.get('icpi_global_pct','—'))+'%':<15}  {res.get('icpi_clasificacion',''):<25}  ║")
    print(f"║  TGI Score   : {str(res.get('tgi_score','—')):<40}  ║")
    print(f"║  SAT Riesgo  : {res.get('sat_riesgo','—'):<15}  {res.get('sat_activas',0)} alerta(s) activa(s)          ║")
    print(f"║  RC-M        : {res.get('n_periodos_rcm',0)} período(s) · Tendencia: {res.get('icpi_trend','—'):<20}  ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    return 0 if resultado["estado"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
