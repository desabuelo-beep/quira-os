"""
SENTINEL · ui_router.py
Orquestador de Generative UI — Sentinel v2 / Sprint 2.
Después del chart principal, determina qué componentes contextuales activar:
Alert · Nav · Evidence · KPI Mini · Scenario.
Regla: contexto accionable, no decorativo — cada componente debe impulsar una decisión.
Dylus Lab © 2026
"""
from __future__ import annotations
import unicodedata
from sentinel.ui_components import (
    alert_card, nav_card, evidence_card, kpi_mini, scenario_card,
)


# ── HELPERS ────────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _has(q: str, *terms: str) -> bool:
    return any(t in q for t in terms)


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def route(query: str) -> None:
    """
    Detecta el contexto de la query y renderiza los componentes UI apropiados.
    Llamado inmediatamente después del chart determinístico.
    """
    from data.loader import load_all
    data = load_all()
    q    = _norm(query)
    qh   = hash(query) & 0xFFFF   # hash corto para claves únicas de botones

    if _has(q, "nbi", "necesidades basicas", "insatisfechas", "inequidad territorial"):
        _route_nbi(data, qh)
    elif _has(q, "inversion per capita", "per capita", "capita", "inversion"):
        _route_inversion(data, qh)
    elif _has(q, "agua", "cobertura agua"):
        _route_agua(data, qh)
    elif _has(q, "indices", "indice", "complementarios",
               "ife", "ied", "igp", "psg", "isp", "itam", "ioc", "iet"):
        _route_indices(data, qh)
    elif _has(q, "icgi", "evolucion", "historico"):
        _route_icgit(data, qh)
    elif _has(q, "tps", "tasa pobreza"):
        _route_tps(data, qh)
    elif _has(q, "parroquia"):
        _route_nbi(data, qh)    # default territorial


# ── ROUTES ESPECÍFICAS ─────────────────────────────────────────────────────────

def _route_nbi(data: dict, qh: int) -> None:
    parroquias = data.get("parroquias", [])
    criticas   = [p for p in parroquias if p["nbi"] >= 50]
    max_p      = max(parroquias, key=lambda p: p["nbi"], default={})
    min_p      = min(parroquias, key=lambda p: p["nbi"], default={})
    brecha     = max_p.get("nbi", 0) - min_p.get("nbi", 0)

    alert_card(
        severity="critical" if brecha > 20 else "high",
        title="Brecha Territorial · NBI",
        message=(
            f"{len(criticas)} parroquia{'s' if len(criticas) != 1 else ''} supera{'n' if len(criticas) != 1 else ''} "
            f"el umbral crítico del 50%. "
            f"<b>{max_p.get('nombre','')}</b> ({max_p.get('nbi',0):.1f}%) vs "
            f"<b>{min_p.get('nombre','')}</b> ({min_p.get('nbi',0):.1f}%)."
        ),
        metric=f"Brecha máxima: {brecha:.1f} puntos porcentuales",
        legal="COOTAD Art.238 · PDOT meta AH-I-X-03 · Agenda 2030 ODS-1",
    )

    nav_card(
        title="Explorar en QUIRA OS",
        buttons=[
            {"label": "GeoTwin",          "page_key": "geotwin",   "icon": "🗺️"},
            {"label": "Inversión Cápita",  "page_key": "inversion", "icon": "💰"},
            {"label": "Causas Brecha",     "page_key": "brecha",    "icon": "📉"},
            {"label": "Simulador",         "page_key": "simulador", "icon": "🧮"},
        ],
        query_hash=qh,
    )

    evidence_card(
        sources=[
            "H99_ENGINE_CORE · 7 parroquias verificadas",
            "INEC/PDOT Diagnóstico Social · diagnóstico oficial",
            "SIAP-ICPI Gold Master v4.1 · sellado Q1-2026",
        ],
        confidence="Alta",
        note="NBI derivado de encuesta INEC + diagnóstico PDOT 2023-2027.",
    )


def _route_inversion(data: dict, qh: int) -> None:
    parroquias = data.get("parroquias", [])
    min_p      = min(parroquias, key=lambda p: p["per_capita"], default={})
    max_p      = max(parroquias, key=lambda p: p["per_capita"], default={})
    ratio      = max_p.get("per_capita", 1) / max(min_p.get("per_capita", 1), 1)
    iet        = data.get("indices", {}).get("IET", {}).get("valor", 44.80)

    alert_card(
        severity="critical" if ratio > 2.5 else "high",
        title="Inequidad de Inversión Territorial · IET",
        message=(
            f"<b>{max_p.get('nombre','')}</b> recibe <b>${max_p.get('per_capita',0)}/hab</b> — "
            f"{ratio:.1f}x más que <b>{min_p.get('nombre','')}</b> "
            f"(${min_p.get('per_capita',0)}/hab). "
            f"Índice de Equidad Territorial: <b>IET={iet:.2f}</b> → Transición Crítica."
        ),
        metric=f"Ratio máximo de inequidad: {ratio:.1f}x entre parroquias",
        legal="COOTAD Art.272 · Equidad en distribución de recursos",
    )

    scenario_card(
        description=(
            "Si la inversión en parroquias rurales aumenta 15%, el IET escala ~5 puntos "
            "y el ICGI-T proyectado cierre 2026 mejoraría de 65.77 a ≈ 67.2."
        ),
        baseline=65.77,
        projected=67.2,
        query_hash=qh,
    )

    nav_card(
        title="Explorar en QUIRA OS",
        buttons=[
            {"label": "GeoTwin",      "page_key": "geotwin",   "icon": "🗺️"},
            {"label": "ODS Tracker",  "page_key": "ods",       "icon": "🌐"},
            {"label": "Simulador",    "page_key": "simulador", "icon": "🧮"},
        ],
        query_hash=qh,
    )

    evidence_card(
        sources=[
            "POA-PAC GAD Montecristi · inversión por parroquia",
            "INEC proyecciones poblacionales · habitantes por parroquia",
            "IET=44.80 · SIAP-ICPI Q1-2026 · SAT-III activa",
        ],
        confidence="Alta",
    )


def _route_agua(data: dict, qh: int) -> None:
    parroquias = data.get("parroquias", [])
    critica    = min(parroquias, key=lambda p: p["agua"], default={})

    alert_card(
        severity="critical",
        title="Servicio Crítico · Agua Potable",
        message=(
            f"<b>{critica.get('nombre','')}</b> tiene cobertura de solo "
            f"<b>{critica.get('agua',0):.2f}%</b> — prácticamente sin acceso a agua potable. "
            f"Meta PDOT 2027: llevar cobertura cantonal del 39.25% al <b>42.38%</b>. "
            f"Sin intervención urgente, la meta PDOT es inalcanzable."
        ),
        metric=f"Cobertura mínima: {critica.get('agua',0):.2f}% · SAT-I activa",
        legal="COOTAD Art.55 lit.d · Agua y alcantarillado · ODS-6",
    )

    alert_card(
        severity="high",
        title="Acciones Requeridas",
        message=(
            "① Revisar priorización POA para agua rural en Isabel Muentes. "
            "② Cruzar inversión histórica AH con cobertura actual. "
            "③ Simular impacto de inversión adicional $500K en Q2-2026. "
            "④ Activar mesa técnica intersectorial agua-saneamiento."
        ),
    )

    nav_card(
        title="Explorar en QUIRA OS",
        buttons=[
            {"label": "Metas PDOT",     "page_key": "metas",     "icon": "🎯"},
            {"label": "Cadena POA·PAC", "page_key": "cadena",    "icon": "🔗"},
            {"label": "Simulador",      "page_key": "simulador", "icon": "🧮"},
            {"label": "ODS Tracker",    "page_key": "ods",       "icon": "🌐"},
        ],
        query_hash=qh,
    )

    evidence_card(
        sources=[
            "H99_ENGINE_CORE · cobertura agua por parroquia",
            "PDOT 2023-2027 · meta SC-I-N-01 agua potable 39.25%→42.38%",
            "SAT-I activa · SIAP-ICPI Q1-2026",
        ],
        confidence="Alta",
        legal="COOTAD Art.55 lit.d",
    )


def _route_indices(data: dict, qh: int) -> None:
    indices = data.get("indices", {})
    ruptura = [(k, v) for k, v in indices.items()
               if v.get("valor") is not None and v["valor"] < 30]
    mandato = [(k, v) for k, v in indices.items()
               if v.get("valor") is not None and v["valor"] >= 70]

    if ruptura:
        nombres_ruptura = " · ".join(
            f"{k}={v['valor']:.1f}" for k, v in ruptura
        )
        alert_card(
            severity="critical",
            title=f"{len(ruptura)} Índice{'s' if len(ruptura)>1 else ''} en Ruptura Sistémica",
            message=(
                f"<b>{nombres_ruptura}</b> — por debajo del umbral de Ocurrencia (30). "
                f"Cada punto de Ruptura descuenta directamente del ICGI-T global."
            ),
            metric="Impacto estimado: -8.2 pts ICGI-T (ISP) · -3.1 pts (PSG)",
        )

    kpi_mini(
        title="Índices clave · Q1-2026",
        items=[
            {"label": k, "value": f"{v['valor']:.1f}", "delta": v.get("avep", "")[:12]}
            for k, v in list(indices.items())[:5]
            if v.get("valor") is not None
        ],
    )

    nav_card(
        title="Explorar en QUIRA OS",
        buttons=[
            {"label": "Eficiencia Dirs.", "page_key": "eficiencia",   "icon": "📋"},
            {"label": "Transparencia",    "page_key": "transparencia", "icon": "🔍"},
            {"label": "Género Equidad",   "page_key": "genero",        "icon": "💜"},
            {"label": "Simulador",        "page_key": "simulador",     "icon": "🧮"},
        ],
        query_hash=qh,
    )

    evidence_card(
        sources=[
            "H73_OUTPUT_API · 50 métricas verificadas",
            "SIAP-ICPI Gold Master v4.1 · Q1-2026",
            "Escala AVEP: Excelencia≥90 · Mandato≥70 · Transición≥50 · Ocurrencia≥30",
        ],
        confidence="Alta",
        note="IFE-E y algunos sub-índices en calibración Q2-2026.",
    )


def _route_icgit(data: dict, qh: int) -> None:
    icgit = data.get("icgit", {})
    score = icgit.get("score", 53.56)
    proj  = icgit.get("proyeccion", 65.77)
    meta  = icgit.get("meta_mandato", 70.0)
    hist  = icgit.get("historico", {})

    kpi_mini(
        title="ICGI-T · Serie histórica verificada",
        items=[
            {"label": "2023",    "value": f"{hist.get('2023',57.36):.2f}"},
            {"label": "2024",    "value": f"{hist.get('2024',67.12):.2f}"},
            {"label": "2025",    "value": f"{hist.get('2025',69.93):.2f}"},
            {"label": "Q1-2026", "value": f"{score:.2f}", "delta": "solo marzo"},
            {"label": "Proj 2026","value": f"{proj:.2f}", "delta": f"meta {meta:.0f}"},
        ],
    )

    gap = meta - proj
    alert_card(
        severity="medium" if gap <= 5 else "high",
        title="Brecha vs Meta Mandato 2026",
        message=(
            f"Proyección cierre 2026: <b>{proj:.2f}</b> · Meta Mandato: <b>{meta:.2f}</b>. "
            f"Brecha de <b>{gap:.2f} puntos</b> a cerrar en Q2-Q4. "
            f"Se requiere acelerar ejecución presupuestaria y cerrar SATs activas."
        ),
        metric=f"Presupuesto ejecutado Q1: 23.75% de $26.7M",
    )

    scenario_card(
        description=(
            f"Si la ejecución se normaliza al 25% por trimestre (ritmo Q2-Q4), "
            f"el ICGI-T proyectado al cierre 2026 podría escalar a ≈ {proj:.2f}. "
            f"Simula escenarios de recuperación en el Módulo Simulador."
        ),
        baseline=score,
        projected=proj,
        query_hash=qh,
    )

    nav_card(
        title="Explorar en QUIRA OS",
        buttons=[
            {"label": "Simulador",    "page_key": "simulador", "icon": "🧮"},
            {"label": "Pulso",        "page_key": "pulso",     "icon": "⚡"},
            {"label": "Alertas SAT",  "page_key": "sat",       "icon": "🚨"},
            {"label": "Brecha",       "page_key": "brecha",    "icon": "📉"},
        ],
        query_hash=qh,
    )

    evidence_card(
        sources=[
            "H12_MOTOR_ICPI_CANÓNICO · fórmula inmutable",
            "H07_FINANCIERO_eSIGEF · devengado Q1-2026",
            "H12c_ICPI_HISTÓRICO_ANUAL · 2023-2025 verificado",
        ],
        confidence="Alta",
        note="Q1-2026 es corte de solo marzo — ritmo 23.75% normal para primer trimestre.",
    )


def _route_tps(data: dict, qh: int) -> None:
    parroquias = data.get("parroquias", [])
    critica    = max(parroquias, key=lambda p: p["tps"], default={})
    criticas   = [p for p in parroquias if p["tps"] >= 60]

    alert_card(
        severity="critical",
        title="Pobreza por Servicios · TPS",
        message=(
            f"<b>{critica.get('nombre','')}</b> con TPS de <b>{critica.get('tps',0):.1f}%</b> — "
            f"la más alta del cantón. "
            f"{len(criticas)} parroquia{'s' if len(criticas)>1 else ''} supera{'n' if len(criticas)>1 else ''} "
            f"el 60%, indicador de pobreza severa por acceso a servicios."
        ),
        metric=f"Brecha TPS cantonal: {critica.get('tps',0) - min(p['tps'] for p in parroquias):.1f} pts",
        legal="ODS-1 · ODS-10 · PDOT meta AH-I-X-03",
    )

    nav_card(
        title="Explorar en QUIRA OS",
        buttons=[
            {"label": "GeoTwin",     "page_key": "geotwin",   "icon": "🗺️"},
            {"label": "Inversión",   "page_key": "inversion", "icon": "💰"},
            {"label": "ODS Tracker", "page_key": "ods",       "icon": "🌐"},
        ],
        query_hash=qh,
    )

    evidence_card(
        sources=[
            "INEC · Tasa de Pobreza por Servicios · encuesta oficial",
            "PDOT 2023-2027 · diagnóstico social territorial",
            "SIAP-ICPI Gold Master v4.1 · Q1-2026",
        ],
        confidence="Media",
        note="TPS: fuente INEC/PDOT diagnóstico oficial (no extraída por quira_extract.py).",
    )
