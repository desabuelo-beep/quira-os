"""
QUIRA Intelligence — Vista Ejecutiva · Sprint C.3
Jerarquía de Atención + Observabilidad Viva · p_vista_ejecutiva.py

Doctrina: "QUIRA no muestra todo al mismo nivel.
           QUIRA organiza la atención institucional según criticidad sistémica."

━━━ ARQUITECTURA · JERARQUÍA DE ATENCIÓN (3 capas) ━━━━━━━━━━━━━━━━━━━━━
  HEADER        — Identidad institucional: GAD · TGI · SAT · Alcalde
  BRIEFING STRIP — Brief ejecutivo 2 líneas (8-15s) — situación + acción
  ─────────────────────────────────────────────────────── CAPA 1 (DOMINANTE)
  Zona 1        — Pulso + SEÑAL CRÍTICA: TOP GAD RUPTURA → TGI → D1-D5
  Zona 2        — Lo Urgente: SAT sistémicas (causa + acción + ley)
  ─────────────────────────────────────────────────────── CAPA 2 (CONTEXTO)
  Zona 3+4      — Compromisos compactos · Territorio compacto (sub-grid)
  ─────────────────────────────────────────────────────── CAPA 3 (SOPORTE)
  Zona 5        — Ecosistema Municipal: 4 entidades · TOP · contraste
  Zona 6        — QUIRA IA + Oportunidades (lectura profunda, 15-30s)

  Grid: Z1 span-2-rows (dominante) | Z2 · Z34 (sub-grid compacto)
  Lectura 3s: TOP RUPTURA rojo → TGI contexto → SAT urgente → acción
  TOP: utils/top.py · W_Q calibrado eSIGEF Ecuador · NOMENCLATURA 7.2

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from config import GAD_NOMBRE, ALCALDE, CORTE
from utils.top import top_entidad, narrativa_ia


# ══════════════════════════════════════════════════════════════════════════════
# DATOS — Gold Master snapshot (fallback local)
# ══════════════════════════════════════════════════════════════════════════════

_FALLBACK: dict = {
    "tgi": {
        "score": 68.82, "clasificacion": "Transición con Riesgos",
        "color_hex": "#FFB800",
        "d1": {"valor": 83.5},  "d2": {"valor": 69.93},
        "d3": {"valor": 14.58}, "d4": {"valor": 66.85},
        "d5": {"valor": 100.0},
        "irs": {"valor": 79.7, "clasificacion": "Muy Regresivo"},
        "ied_global": {"valor": 31.14},
        "brecha_rural_usd": 1791935,
    },
    "icpi": {"global_pct": 53.56, "clasificacion": "Ruptura Sistémica"},
    "sat_gm": {
        "clasif_riesgo": "ALTO", "activas_count": 3,
        "sat_activas_detalle": {
            "SAT-III": {"peso": 0.20, "descripcion": "Sub-ejecución D3"},
            "SAT-IV":  {"peso": 0.10, "descripcion": "Brecha territorial crítica"},
            "SAT-V":   {"peso": 0.05, "descripcion": "Trazabilidad insuficiente"},
        },
    },
    "financiero": {
        "ti_2026_raw_pct": 1.05,
        "presupuesto_codificado_grupos78_2026": 22595464,
        "devengado_q1_2026": 238066,
        "fondos_bloqueados_est": 3660000,
        "fondos_bloqueados_detalle": "BDE $3.5M + Gender Bond $95K + ONU Mujeres $65K",
        "h90_consolidado": {
            "gad_ti_q1_pct": 11.20,
            "patronato_codificado": 4341242.62,
            "patronato_devengado_q1": 849061.75,
            "patronato_ti_q1_pct": 19.56,
            "ep_aseo_codificado": 2438254.45,
            "ep_aseo_devengado_q1": 442929.52,
            "ep_aseo_ti_q1_pct": 18.17,
            "bomberos_codificado": 1485033.40,
            "bomberos_devengado_q1": 288599.28,
            "bomberos_ti_q1_pct": 19.43,
            "holding_ti_q1_pct": 12.40,
            "holding_total_codificado": 54242424.28,
            "holding_total_devengado_q1": 6727849.41,
        },
    },
    "psg": {"psg_fidelidad_pct": 69.93},
    "gad": {"promesas_cne": 66, "metas_pdot": 25},
    "territorial": {
        "parroquias": [
            {"nombre": "Montecristi",         "tipo": "Urbana", "nbi_pct": 38.4,
             "iet_local_pct": 193.75, "inv_percapita_q1": 217},
            {"nombre": "Aníbal San Andrés",    "tipo": "Rural",  "nbi_pct": 52.1,
             "iet_local_pct": 51.79,  "inv_percapita_q1": 58},
            {"nombre": "Colorado",             "tipo": "Rural",  "nbi_pct": 58.7,
             "iet_local_pct": 28.57,  "inv_percapita_q1": 32},
            {"nombre": "Leónidas Proaño",      "tipo": "Rural",  "nbi_pct": 54.3,
             "iet_local_pct": 42.86,  "inv_percapita_q1": 48},
            {"nombre": "Gral. Alfaro",         "tipo": "Rural",  "nbi_pct": 49.8,
             "iet_local_pct": 63.39,  "inv_percapita_q1": 71},
            {"nombre": "Isabel Muentes",       "tipo": "Rural",  "nbi_pct": 61.2,
             "iet_local_pct": 35.71,  "inv_percapita_q1": 40,
             "alerta": "Agua 1.02%"},
            {"nombre": "La Pila",              "tipo": "Rural",  "nbi_pct": 55.9,
             "iet_local_pct": 46.43,  "inv_percapita_q1": 52},
        ],
        "nbi_rural_promedio": 55.7,
    },
}


@st.cache_data(ttl=300, show_spinner=False)
def _load() -> dict:
    try:
        from utils.cache_quira import cargar_gm_snapshot
        data = cargar_gm_snapshot()
        if data and "tgi" in data:
            return data
    except Exception:
        pass
    return _FALLBACK


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTACIONES — TOP del Ecosistema Municipal
# ══════════════════════════════════════════════════════════════════════════════

def _compute_ecosistema(data: dict) -> list[dict]:
    """
    Calcula TOP para las 4 entidades del Ecosistema Municipal.
    Fuente: financiero.h90_consolidado — Gold Master v5.5.

    GAD usa Ti de inversión estricta (G71-78 / D3) para señal crítica.
    Patronato · EP Aseo · Bomberos usan Ti H90 (todos los grupos).
    """
    h90 = data.get("financiero", {}).get("h90_consolidado", {})
    fin = data.get("financiero", {})

    specs = [
        {
            "nombre":    "GAD Municipal",
            "emoji":     "🏛",
            "nota_ti":   "inversión G71-78 · D3",
            "ti_pct":    fin.get("ti_2026_raw_pct", 1.05),
            "codificado": fin.get("presupuesto_codificado_grupos78_2026", 22595464),
            "devengado":  fin.get("devengado_q1_2026", 238066),
        },
        {
            "nombre":    "Patronato Municipal",
            "emoji":     "💚",
            "nota_ti":   "todos grupos · H90",
            "ti_pct":    h90.get("patronato_ti_q1_pct", 19.56),
            "codificado": h90.get("patronato_codificado", 4341242.62),
            "devengado":  h90.get("patronato_devengado_q1", 849061.75),
        },
        {
            "nombre":    "EP Aseo",
            "emoji":     "♻",
            "nota_ti":   "todos grupos · H90",
            "ti_pct":    h90.get("ep_aseo_ti_q1_pct", 18.17),
            "codificado": h90.get("ep_aseo_codificado", 2438254.45),
            "devengado":  h90.get("ep_aseo_devengado_q1", 442929.52),
        },
        {
            "nombre":    "Cuerpo de Bomberos",
            "emoji":     "🚒",
            "nota_ti":   "todos grupos · H90",
            "ti_pct":    h90.get("bomberos_ti_q1_pct", 19.43),
            "codificado": h90.get("bomberos_codificado", 1485033.40),
            "devengado":  h90.get("bomberos_devengado_q1", 288599.28),
        },
    ]

    result = []
    for s in specs:
        td = top_entidad(s["ti_pct"], CORTE, s["nombre"])
        td.update({k: s[k] for k in ("emoji", "nota_ti", "codificado", "devengado")})
        # Alias: top_entidad retorna "entidad"; código HTML usa "nombre"
        td["nombre"] = td.get("entidad", s["nombre"])
        result.append(td)
    return result


def _compose_quira_ia(data: dict, eco: list[dict]) -> str:
    """
    Brief ejecutivo institucional para QUIRA IA.
    Usa narrativa_ia() de utils/top.py para cada entidad.
    Lenguaje: autoritario, preciso. No es chatbot.
    """
    gad_e       = eco[0]   # GAD siempre índice 0
    otros       = eco[1:]  # Patronato, EP Aseo, Bomberos

    # Brief del GAD (ruptura)
    gad_brief   = narrativa_ia(gad_e)

    # Sobre-ritmo de las entidades del ecosistema
    sobre_ritmo = [e["nombre"] for e in otros if e.get("categoria") == "sostenible"]
    atencion    = [e["nombre"] for e in otros if e.get("categoria") != "sostenible"]

    fin          = data.get("financiero", {})
    fondos       = fin.get("fondos_bloqueados_est", 3660000)
    fondos_m     = fondos / 1_000_000

    partes = [gad_brief]

    if sobre_ritmo:
        lista = (
            ", ".join(sobre_ritmo[:-1]) + " y " + sobre_ritmo[-1]
            if len(sobre_ritmo) > 1 else sobre_ritmo[0]
        )
        partes.append(
            f"En contraste, {lista} mantienen trayectoria sobre el ritmo histórico "
            f"esperado para {CORTE}. El ecosistema municipal opera de forma saludable "
            "fuera del núcleo de inversión del GAD."
        )

    if atencion:
        partes.append(
            f"Entidades con atención requerida: {', '.join(atencion)}. "
            "Monitorear Q siguiente."
        )

    partes.append(
        f"La palanca de mayor impacto disponible ahora mismo es el desembolso BDE "
        f"(${fondos_m:.1f}M en fondos bloqueados). Su activación antes de mediados de "
        "junio determina si Q2 cierra dentro o fuera del umbral COPFP Art. 113."
    )

    return " ".join(partes)


def _briefing_sentence(narrative: str) -> str:
    """
    Extrae las 2 primeras oraciones del narrative para el Briefing Strip.
    Máximo 280 caracteres — lectura de 8-15s.
    """
    import re
    partes = re.split(r'(?<=\.)\s+', narrative.strip())
    texto  = " ".join(partes[:2])
    return texto if len(texto) <= 280 else texto[:277] + "…"


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS HTML — puras, deterministas, sin imports de Streamlit
# ══════════════════════════════════════════════════════════════════════════════

def _sem(valor: float) -> str:
    """Color semafórico estándar para métricas 0-100."""
    if valor >= 70: return "#22C55E"
    if valor >= 50: return "#FFB700"
    if valor >= 30: return "#F97316"
    return "#EF4444"


def _zt(icon: str, titulo: str, sub: str, color: str = "rgba(255,255,255,.28)") -> str:
    """Zone title — label + subtítulo."""
    return (
        f'<div style="margin-bottom:14px">'
        f'<div style="font:700 9px/1 Inter,sans-serif;color:{color};'
        f'text-transform:uppercase;letter-spacing:.1em">{icon} {titulo}</div>'
        f'<div style="font:400 10px/1 Inter,sans-serif;color:rgba(255,255,255,.18);'
        f'margin-top:3px">{sub}</div>'
        f'</div>'
    )


def _mini_bar(label: str, sub: str, valor: float) -> str:
    c = _sem(valor)
    w = max(0.0, min(100.0, valor))
    return (
        f'<div style="margin-bottom:9px">'
        f'<div style="display:flex;justify-content:space-between;margin-bottom:2px">'
        f'<div>'
        f'<div style="font:700 9px/1 Inter,sans-serif;color:rgba(255,255,255,.48)">{label}</div>'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.22);margin-top:1px">{sub}</div>'
        f'</div>'
        f'<span style="font:700 11px/1 Inter,sans-serif;color:{c};margin-top:1px">{valor:.0f}%</span>'
        f'</div>'
        f'<div style="height:3px;background:rgba(255,255,255,.07);border-radius:2px">'
        f'<div style="height:3px;width:{w}%;background:{c};border-radius:2px"></div>'
        f'</div>'
        f'</div>'
    )


def _compromiso_row(icon: str, titulo: str, valor: str, vc: str,
                    desc: str, urg: str = "", uc: str = "#F59E0B") -> str:
    urg_html = (
        f'<div style="font:600 9px/1 Inter,sans-serif;color:{uc};margin-top:3px">⏱ {urg}</div>'
    ) if urg else ""
    return (
        f'<div style="display:flex;gap:10px;padding:9px 0;'
        f'border-bottom:1px solid rgba(255,255,255,.05)">'
        f'<span style="font-size:14px;flex-shrink:0;margin-top:1px">{icon}</span>'
        f'<div style="flex:1;min-width:0">'
        f'<div style="font:700 11px/1.2 Inter,sans-serif;color:#E2E8F0">'
        f'{titulo} <span style="color:{vc}">{valor}</span></div>'
        f'<div style="font:400 9px/1.4 Inter,sans-serif;color:rgba(255,255,255,.36);'
        f'margin-top:2px">{desc}</div>'
        f'{urg_html}'
        f'</div></div>'
    )


def _parroquia_row(p: dict) -> str:
    iet   = p.get("iet_local_pct", 0)
    nbi   = p.get("nbi_pct", 0)
    inv   = p.get("inv_percapita_q1", 0)
    alerta = p.get("alerta", "")
    tipo  = p.get("tipo", "Rural")

    # Color por IET: ≥100 verde (sobre-inversión o paridad), 50-99 amarillo, <50 rojo
    if iet >= 100:
        c_iet = "#22C55E"
        ico   = "◉"
    elif iet >= 50:
        c_iet = "#F59E0B"
        ico   = "◎"
    else:
        c_iet = "#EF4444"
        ico   = "○"

    alerta_html = (
        f'<span style="font:700 8px/1 Inter,sans-serif;color:#EF4444;'
        f'background:rgba(239,68,68,.1);border-radius:3px;padding:1px 5px;'
        f'margin-left:5px">⚡ {alerta}</span>'
    ) if alerta else ""

    tipo_badge = (
        f'<span style="font:400 8px/1 Inter,sans-serif;color:rgba(0,212,255,.5);'
        f'margin-left:4px">URB</span>'
        if tipo == "Urbana" else ""
    )

    return (
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'padding:5px 0;border-bottom:1px solid rgba(255,255,255,.04)">'
        f'<div style="display:flex;align-items:center;gap:6px">'
        f'<span style="color:{c_iet};font-size:9px">{ico}</span>'
        f'<span style="font:400 10px/1 Inter,sans-serif;color:#D1D5DB">'
        f'{p["nombre"]}{tipo_badge}</span>'
        f'{alerta_html}'
        f'</div>'
        f'<div style="display:flex;gap:10px;align-items:center">'
        f'<span style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.3)">'
        f'NBI {nbi:.0f}%</span>'
        f'<span style="font:700 9px/1 Inter,sans-serif;color:{c_iet}">'
        f'IET {iet:.0f}%</span>'
        f'<span style="font:400 9px/1 JetBrains Mono,monospace;color:rgba(255,255,255,.2)">'
        f'${inv}/hab</span>'
        f'</div>'
        f'</div>'
    )


def _entity_card(e: dict) -> str:
    """Card de entidad del Ecosistema con TOP semafórico."""
    nombre  = e.get("nombre", "—")
    emoji   = e.get("emoji", "")
    ti      = e.get("ti_pct", 0.0)
    nota_ti = e.get("nota_ti", "")
    cod     = e.get("codificado", 0)
    dev     = e.get("devengado", 0)
    color   = e.get("color", "#EF4444")
    icono   = e.get("icono", "🔴")
    label   = e.get("label", "—")
    top_d   = e.get("top_display")       # None si sobre ritmo
    cat     = e.get("categoria", "ruptura")

    # TOP display: si None (sobre ritmo), usar label; si tiene valor, mostrarlo
    top_line = (
        f'<div style="font:700 14px/1 Inter,sans-serif;color:{color}">{top_d}</div>'
        if top_d else
        f'<div style="font:700 11px/1.2 Inter,sans-serif;color:{color};'
        f'text-align:center">Sobre ritmo esperado</div>'
    )

    # Borde del card según categoría
    border_intensity = "2px" if cat == "ruptura" else "1px"

    return (
        f'<div style="background:rgba(255,255,255,.025);'
        f'border:{border_intensity} solid {color}33;'
        f'border-top:3px solid {color};'
        f'border-radius:12px;padding:14px 12px;'
        f'display:flex;flex-direction:column;gap:6px">'

        # Entity name
        f'<div style="font:700 11px/1.2 Inter,sans-serif;color:#E2E8F0">'
        f'{emoji} {nombre}</div>'

        # Ti
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.35)">'
        f'Ti {CORTE}: <span style="font-weight:700;color:rgba(255,255,255,.65)">'
        f'{ti:.2f}%</span>'
        f' <span style="color:rgba(255,255,255,.2)">({nota_ti})</span></div>'

        # TOP badge
        f'<div style="background:{color}12;border:1px solid {color}2A;'
        f'border-radius:8px;padding:8px;text-align:center;margin:2px 0">'
        f'<div style="font:700 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
        f'letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px">'
        f'{icono} TOP · Trayectoria Proyectada</div>'
        f'{top_line}'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'margin-top:4px">{label}</div>'
        f'</div>'

        # Cod / Dev
        f'<div style="display:flex;justify-content:space-between;'
        f'padding-top:6px;border-top:1px solid rgba(255,255,255,.05)">'
        f'<div style="text-align:center">'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25)">Codificado</div>'
        f'<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.55);margin-top:2px">'
        f'${cod/1_000:.0f}K</div>'
        f'</div>'
        f'<div style="text-align:center">'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25)">Devengado Q1</div>'
        f'<div style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.55);margin-top:2px">'
        f'${dev/1_000:.0f}K</div>'
        f'</div>'
        f'</div>'

        f'</div>'
    )


def _alerta_card(codigo: str, sat_info: dict, ti_raw: float) -> str:
    """Card ejecutivo de alerta SAT. ti_raw inyectado para SAT-III dinámico."""
    _MAP = {
        "SAT-III": {
            "titulo":  "Ejecución de inversión en alerta",
            "causa":   f"Solo el {ti_raw:.2f}% del presupuesto de inversión (G71-78) ejecutado en Q1. "
                       "Ritmo proyectado: 8% anual — umbral mínimo legal: 60%.",
            "tiempo":  "Cierre Q2 en ~45 días",
            "accion":  "Activar desembolso BDE $3.5M. Convocar Director de Obras.",
            "ley":     "COPFP Art. 113",
            "color":   "#EF4444",
        },
        "SAT-IV": {
            "titulo":  "Inequidad territorial crítica",
            "causa":   "IRS 79.7 (Muy Regresivo): la inversión no llega donde más se necesita. "
                       "Isabel Muentes: 1.02% cobertura de agua.",
            "tiempo":  "Acumulativo desde inicio de mandato",
            "accion":  "Revisar distribución geográfica del POA. Priorizar NBI alto.",
            "ley":     "COOTAD Art. 192",
            "color":   "#F97316",
        },
        "SAT-V": {
            "titulo":  "Evidencia institucional insuficiente",
            "causa":   "Densidad de trazabilidad por debajo del umbral requerido. "
                       "Rendición de Cuentas CPCCS se aproxima.",
            "tiempo":  "Próximo plazo legal CPCCS",
            "accion":  "Solicitar reportes con evidencia firmada a todos los directores.",
            "ley":     "COOTAD Art. 302",
            "color":   "#F59E0B",
        },
    }
    info = _MAP.get(codigo, {})
    if not info:
        return ""
    c = info["color"]
    return (
        f'<div style="border:1px solid {c}22;border-left:3px solid {c};'
        f'border-radius:10px;padding:11px 13px;margin-bottom:8px;background:{c}07">'

        f'<div style="display:flex;align-items:center;gap:7px;margin-bottom:4px">'
        f'<span style="font:800 8px/1 Inter,sans-serif;color:{c};background:{c}22;'
        f'padding:2px 7px;border-radius:4px;letter-spacing:.06em">{codigo}</span>'
        f'<span style="font:700 11px/1.2 Inter,sans-serif;color:#E2E8F0">{info["titulo"]}</span>'
        f'</div>'

        f'<div style="font:400 10px/1.55 Inter,sans-serif;color:rgba(255,255,255,.48);'
        f'margin-bottom:5px">{info["causa"]}</div>'

        f'<div style="display:flex;justify-content:space-between;flex-wrap:wrap;'
        f'gap:4px;margin-bottom:5px">'
        f'<span style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.3)">⏱ {info["tiempo"]}</span>'
        f'<span style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.2)">{info["ley"]}</span>'
        f'</div>'

        f'<div style="padding-top:5px;border-top:1px solid rgba(255,255,255,.05)">'
        f'<span style="font:600 10px/1.3 Inter,sans-serif;color:{c}">→ {info["accion"]}</span>'
        f'</div>'
        f'</div>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# CONSTRUCTORES DE ZONA — HTML puro, sin st.*
# ══════════════════════════════════════════════════════════════════════════════

def _html_header(data: dict, ts: str = "") -> str:
    """
    Header institucional. Sprint C.3: indicador SISTEMA VIVO con timestamp.
    ts — timestamp de render (HH:MM · DD/MM) inyectado desde render().
    """
    tgi       = data.get("tgi", {})
    score     = tgi.get("score", 0.0)
    color_tgi = tgi.get("color_hex", "#FFB700")
    sat       = data.get("sat_gm", {})
    n_act     = sat.get("activas_count", 0)
    clasif    = sat.get("clasif_riesgo", "—")
    apellido  = ALCALDE.split()[-1] if ALCALDE else "—"

    sc = {"BAJO": "#22C55E", "MEDIO": "#F59E0B",
          "ALTO": "#F97316", "CRÍTICO": "#EF4444"}.get(clasif, "#F97316")

    # Sprint C.3 — SISTEMA VIVO: pulsing dot + timestamp
    ts_line = (
        f'<div style="font:400 7px/1 JetBrains Mono,monospace;'
        f'color:rgba(255,255,255,.18);margin-top:2px">{ts}</div>'
    ) if ts else ""

    vivo_chip = (
        f'<div style="display:flex;align-items:center;gap:6px;'
        f'padding:5px 10px;background:rgba(34,197,94,.06);'
        f'border:1px solid rgba(34,197,94,.18);border-radius:8px">'
        f'<div class="ve-live-dot"></div>'
        f'<div>'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(34,197,94,.75);'
        f'letter-spacing:.08em;text-transform:uppercase;white-space:nowrap">SISTEMA VIVO</div>'
        f'{ts_line}'
        f'</div></div>'
    )

    return (
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'padding:11px 18px;background:rgba(255,255,255,.02);'
        f'border:1px solid rgba(255,255,255,.07);border-radius:12px;margin-bottom:16px">'

        # Left: GAD
        f'<div style="display:flex;align-items:center;gap:10px">'
        f'<span style="font-size:18px">🏛</span>'
        f'<div>'
        f'<div style="font:900 14px/1 Inter,sans-serif;color:#E2E8F0;letter-spacing:-.02em">'
        f'{GAD_NOMBRE}</div>'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'margin-top:2px">QUIRA Institucional · Vista Ejecutiva · Corte {CORTE}</div>'
        f'</div></div>'

        # Right: KPI chips + VIVO
        f'<div style="display:flex;align-items:center;gap:8px">'

        # TGI
        f'<div style="text-align:center;padding:5px 12px;'
        f'background:{color_tgi}12;border:1px solid {color_tgi}30;border-radius:8px">'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
        f'letter-spacing:.07em;text-transform:uppercase">TGI Global</div>'
        f'<div style="font:900 1.5rem/1.1 Inter,sans-serif;color:{color_tgi}">'
        f'{score:.1f}</div>'
        f'</div>'

        # SAT
        f'<div style="text-align:center;padding:5px 12px;'
        f'background:{sc}12;border:1px solid {sc}30;border-radius:8px">'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
        f'letter-spacing:.07em;text-transform:uppercase">Alertas SAT</div>'
        f'<div style="font:900 1.5rem/1.1 Inter,sans-serif;color:{sc}">'
        f'{n_act}</div>'
        f'</div>'

        # Alcalde
        f'<div style="text-align:center;padding:5px 12px;'
        f'background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.18);border-radius:8px">'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(0,212,255,.4);'
        f'letter-spacing:.07em;text-transform:uppercase">Ejecutivo</div>'
        f'<div style="font:700 12px/1.3 Inter,sans-serif;color:#00D4FF;margin-top:2px">'
        f'{apellido}</div>'
        f'</div>'

        # SISTEMA VIVO — Sprint C.3
        + vivo_chip

        + f'</div></div>'
    )


def _html_z1_pulso(data: dict, gad_top: dict | None = None) -> str:
    """
    Sprint C.1 — Jerarquía de Atención.
    Señal crítica TOP GAD primero (dominante), TGI como contexto, barras como soporte.
    El alcalde ve el problema en 0-3 segundos antes de leer cualquier texto.
    """
    tgi       = data.get("tgi", {})
    score     = tgi.get("score", 0.0)
    clasif    = tgi.get("clasificacion", "—")
    color_tgi = tgi.get("color_hex", "#FFB700")
    icpi      = data.get("icpi", {})
    icpi_pct  = icpi.get("global_pct", 0.0)
    icpi_cl   = icpi.get("clasificacion", "—")

    d1 = tgi.get("d1", {}).get("valor", 0.0)
    d2 = tgi.get("d2", {}).get("valor", 0.0)
    d3 = tgi.get("d3", {}).get("valor", 0.0)
    d4 = tgi.get("d4", {}).get("valor", 0.0)
    d5 = tgi.get("d5", {}).get("valor", 0.0)

    bars = (
        _mini_bar("D1 — Legalidad",          "Marco normativo · COOTAD · PAC publicado", d1) +
        _mini_bar("D2 — Planificación",       "Fidelidad PDOT · metas en trayectoria", d2) +
        _mini_bar("D3 — Ejecución",           "Ti inversión Q1-2026 · activación pendiente", d3) +
        _mini_bar("D4 — Equidad Territorial", "IRS 79.7 — inversión concentrada urbana", d4) +
        _mini_bar("D5 — Capacidad",           "SIGAD · SNP certificados al 100%", d5)
    )

    # ── Señal crítica TOP (capa dominante — 0-3s) ────────────────────────────
    if gad_top:
        g_color = gad_top.get("color", "#EF4444")
        g_cat   = gad_top.get("categoria", "ruptura").upper()
        g_top   = gad_top.get("top", 8.1)
        g_diag  = gad_top.get("diagnostico", "Intervención urgente requerida.")
        g_icono = gad_top.get("icono", "🔴")

        # Sprint C.3: animar el bloque ruptura (solo si aplica)
        pulse_class = ' ve-ruptura-pulse' if g_cat == "RUPTURA" else ''

        top_signal = (
            f'<div class="ve-zone{pulse_class}" style="background:{g_color}10;border:1.5px solid {g_color}40;'
            f'border-left:4px solid {g_color};'
            f'border-radius:10px;padding:14px 15px;margin-bottom:16px">'

            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'margin-bottom:8px">'
            f'<div style="font:800 8px/1 Inter,sans-serif;color:{g_color};'
            f'letter-spacing:.1em;text-transform:uppercase">'
            f'⚡ Inversión GAD · Señal Crítica</div>'
            f'<span style="font:800 8px/1 Inter,sans-serif;color:{g_color};'
            f'background:{g_color}20;padding:2px 9px;border-radius:4px;'
            f'letter-spacing:.08em">{g_icono} {g_cat}</span>'
            f'</div>'

            # TOP value — dominante visual
            f'<div style="font:900 3rem/1 Inter,sans-serif;color:{g_color};'
            f'letter-spacing:-.04em;margin-bottom:4px">{g_top:.1f}<span style="font-size:1.4rem">%</span></div>'

            f'<div style="font:600 10px/1 Inter,sans-serif;color:rgba(255,255,255,.4);'
            f'margin-bottom:3px">TOP · Trayectoria Operativa Proyectada · {CORTE}</div>'
            f'<div style="font:400 9px/1.4 Inter,sans-serif;color:rgba(255,255,255,.28)">'
            f'{g_diag}</div>'
            f'</div>'
        )
    else:
        top_signal = ""

    return (
        _zt("◉", "Pulso del Municipio",
            "Señal Crítica → TGI · D1–D5 · Motor Predictivo") +

        # Señal crítica TOP — PRIMERO (dominante cognitivo)
        top_signal +

        # TGI como contexto (segundo) — más compacto que Sprint B
        f'<div style="display:flex;align-items:baseline;gap:8px;margin-bottom:2px">'
        f'<div style="font:900 2.8rem/1 Inter,sans-serif;color:{color_tgi};'
        f'letter-spacing:-.05em">{score:.1f}</div>'
        f'<div>'
        f'<div style="font:700 11px/1 Inter,sans-serif;color:{color_tgi}">{clasif}</div>'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.22)">'
        f'TGI · Gobernanza Integral · 0–100</div>'
        f'</div></div>'

        f'<div style="font:600 9px/1 Inter,sans-serif;color:#22C55E;'
        f'margin-bottom:14px;margin-top:4px">↗ Tendencia positiva 2023–2025</div>'

        + bars +

        f'<div style="margin-top:10px;padding-top:8px;'
        f'border-top:1px solid rgba(255,255,255,.05)">'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.2)">'
        f'ICPI (velocidad de ejecución) — '
        f'<span style="color:rgba(255,255,255,.45)">{icpi_pct:.1f}%</span> · {icpi_cl}'
        f'</div></div>'
    )


def _html_briefing_strip(eco: list[dict], narrative: str) -> str:
    """
    Sprint C.1 — Briefing Ejecutivo Diario (capa 8-15s).
    Sprint C.3 — borde animado cuando GAD en ruptura.
    Situación de sala de mando: 2 oraciones, sin chatbot, sin adornos.
    Aparece ANTES del grid, full-width, siempre visible.
    """
    gad    = eco[0]
    color  = gad.get("color", "#EF4444")
    brief  = _briefing_sentence(narrative)
    cat    = gad.get("categoria", "ruptura")

    # Sprint C.3: animar borde en ruptura
    live_class = " ve-briefing-live" if cat == "ruptura" else ""

    return (
        f'<div class="ve-root{live_class}" style="display:flex;align-items:center;gap:14px;'
        f'padding:12px 18px;margin-bottom:14px;'
        f'background:rgba(0,0,0,.22);'
        f'border:1px solid rgba(255,255,255,.07);'
        f'border-left:3px solid {color};border-radius:12px">'

        # Label
        f'<div style="flex-shrink:0;white-space:nowrap">'
        f'<div style="font:800 7px/1 Inter,sans-serif;color:{color};'
        f'letter-spacing:.1em;text-transform:uppercase;margin-bottom:2px">'
        f'◆ BRIEFING EJECUTIVO</div>'
        f'<div style="font:400 7px/1 JetBrains Mono,monospace;'
        f'color:rgba(255,255,255,.2)">QUIRA IA · {CORTE}</div>'
        f'</div>'

        # Separador
        f'<div style="width:1px;height:28px;background:rgba(255,255,255,.08);flex-shrink:0"></div>'

        # Brief text
        f'<div style="font:400 11px/1.6 Inter,sans-serif;'
        f'color:rgba(255,255,255,.62);flex:1">{brief}</div>'

        f'</div>'
    )


def _html_decisiones_strip(data: dict) -> str:
    """
    Sprint E.3 — CAPA 1: franja de decisiones urgentes.
    Transforma QUIRA de sistema de monitoreo a sistema de decisión.
    Solo aparece cuando hay ≥1 decisión. No es decorativa — es operativa.
    """
    fin        = data.get("financiero", {})
    tgi        = data.get("tgi", {})
    sat        = data.get("sat_gm", {})
    psg        = data.get("psg", {})

    ti         = fin.get("ti_2026_raw_pct", 1.05)
    bloqueados = fin.get("fondos_bloqueados_est", 0)
    n_sat      = sat.get("activas_count", 0)
    d2_val     = tgi.get("d2", {}).get("valor", 69.93)
    pac_pub    = psg.get("pac_publicado", True)

    decisiones: list[tuple[str, str, str]] = []  # (icon, texto, color)

    if ti < 15:
        decisiones.append((
            "💰",
            f"Ti Q1-2026: {ti:.2f}% · Plan de aceleración presupuestaria antes del 30 Jun",
            "#EF4444",
        ))
    if bloqueados > 500_000:
        m = bloqueados / 1_000_000
        decisiones.append((
            "🔒",
            f"${m:.2f}M fondos bloqueados · BDE + ONU Mujeres · gestión urgente",
            "#F97316",
        ))
    if n_sat > 0:
        decisiones.append((
            "⚠",
            f"{n_sat} alertas SAT activas · informe ejecutivo requerido",
            "#F59E0B",
        ))
    if d2_val < 70:
        decisiones.append((
            "🎯",
            f"D2 Planificación: {d2_val:.1f}% · revisar metas PDOT rezagadas",
            "#F59E0B",
        ))

    n = len(decisiones)
    if n == 0:
        return ""

    items_html = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:5px;padding:0 12px;'
        f'border-left:2px solid {c};flex-shrink:0;max-width:260px">'
        f'<span style="font-size:9px;margin-top:1px">{icon}</span>'
        f'<span style="font:400 9px/1.4 Inter,sans-serif;color:rgba(255,255,255,.52)">{text}</span>'
        f'</div>'
        for icon, text, c in decisiones
    )

    return (
        f'<div style="display:flex;align-items:center;padding:10px 16px;'
        f'background:rgba(239,68,68,.035);'
        f'border:1px solid rgba(239,68,68,.14);'
        f'border-radius:10px;margin-bottom:10px;overflow-x:hidden;gap:0">'
        f'<div style="flex-shrink:0;min-width:110px;margin-right:12px">'
        f'<div style="font:800 8px/1 Inter,sans-serif;color:#EF4444;'
        f'letter-spacing:.1em;text-transform:uppercase">⚡ {n} DECISIONES</div>'
        f'<div style="font:400 7px/1 JetBrains Mono,monospace;'
        f'color:rgba(255,255,255,.2);margin-top:3px">Requieren acción ejecutiva</div>'
        f'</div>'
        f'<div style="width:1px;height:32px;background:rgba(255,255,255,.07);'
        f'flex-shrink:0;margin-right:12px"></div>'
        f'<div style="display:flex;gap:0;flex:1;flex-wrap:wrap;gap:6px">{items_html}</div>'
        f'</div>'
    )


def _html_z2_urgente(data: dict) -> str:
    sat     = data.get("sat_gm", {})
    clasif  = sat.get("clasif_riesgo", "ALTO")
    n_act   = sat.get("activas_count", 0)
    activas = sat.get("sat_activas_detalle", {})
    ti_raw  = data.get("financiero", {}).get("ti_2026_raw_pct", 1.05)

    sc = {"BAJO": "#22C55E", "MEDIO": "#F59E0B",
          "ALTO": "#F97316", "CRÍTICO": "#EF4444"}.get(clasif, "#F97316")

    cards = "".join(
        _alerta_card(cod, activas.get(cod, {}), ti_raw)
        for cod in activas
    )

    return (
        _zt("⚠", "Lo Urgente",
            "Alertas SAT activas · Acción del Ejecutivo requerida", "#F97316") +

        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">'
        f'<div style="font:900 2.8rem/1 Inter,sans-serif;color:{sc};'
        f'letter-spacing:-.04em">{n_act}</div>'
        f'<div>'
        f'<div style="font:700 13px/1 Inter,sans-serif;color:{sc}">alertas activas</div>'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.28);'
        f'margin-top:2px">Riesgo institucional: {clasif}</div>'
        f'</div></div>'

        + cards
    )


def _html_z3_compromisos(data: dict) -> str:
    psg          = data.get("psg", {})
    gad          = data.get("gad", {})
    fidelidad    = psg.get("psg_fidelidad_pct", 69.93)
    promesas_cne = gad.get("promesas_cne", 66)
    metas_pdot   = gad.get("metas_pdot", 25)
    fc           = _sem(fidelidad)

    return (
        _zt("📅", "Compromisos",
            "Próximos 60 días · Plazos institucionales críticos") +

        _compromiso_row(
            "📋", "Rendición de Cuentas CPCCS",
            "Pendiente", "#F59E0B",
            "Validación del informe anual ante la ciudadanía",
            "Plazo legal próximo · Prioridad alta", "#EF4444"
        ) +
        _compromiso_row(
            "🎯", f"Metas PDOT — {metas_pdot} metas",
            f"{fidelidad:.1f}%", fc,
            f"Fidelidad de planificación (D2) · Plan de Desarrollo Ordenamiento Territorial"
        ) +
        _compromiso_row(
            "📜", f"Plan de Gobierno CNE — {promesas_cne} compromisos",
            "Módulo en construcción", "rgba(255,255,255,.3)",
            f"{promesas_cne} compromisos CNE identificados — sin datos de avance disponibles. "
            "IFE en desarrollo."
        ) +
        _compromiso_row(
            "💰", "Cierre presupuestario Q2",
            "30 Jun", "#F97316",
            "Inversión G71-78 · Ti actual 1.05% · Activar desembolso BDE antes de Q2",
            "~45 días · Riesgo COPFP Art. 113 si no se activa", "#EF4444"
        )
    )


def _html_z4_territorio(data: dict) -> str:
    tgi        = data.get("tgi", {})
    irs        = tgi.get("irs", {})
    irs_val    = irs.get("valor", 79.7)
    irs_cl     = irs.get("clasificacion", "Muy Regresivo")
    d4_val     = tgi.get("d4", {}).get("valor", 66.85)
    brecha_usd = tgi.get("brecha_rural_usd", 1791935)
    d4c        = _sem(d4_val)

    parroquias = data.get("territorial", {}).get("parroquias", _FALLBACK["territorial"]["parroquias"])
    filas = "".join(_parroquia_row(p) for p in parroquias)

    return (
        _zt("🗺", "Territorio",
            f"Equidad territorial · {len(parroquias)} parroquias · Cantón Montecristi") +

        f'<div style="display:flex;gap:8px;margin-bottom:12px">'

        # IRS
        f'<div style="flex:1;background:rgba(239,68,68,.07);'
        f'border:1px solid rgba(239,68,68,.2);border-radius:8px;'
        f'padding:8px;text-align:center">'
        f'<div style="font:900 1.5rem/1 Inter,sans-serif;color:#EF4444">{irs_val:.0f}</div>'
        f'<div style="font:400 8px/1.3 Inter,sans-serif;color:rgba(255,255,255,.35);'
        f'margin-top:2px">IRS · {irs_cl}</div>'
        f'</div>'

        # D4
        f'<div style="flex:1;background:{d4c}0F;border:1px solid {d4c}25;'
        f'border-radius:8px;padding:8px;text-align:center">'
        f'<div style="font:900 1.5rem/1 Inter,sans-serif;color:{d4c}">{d4_val:.0f}%</div>'
        f'<div style="font:400 8px/1.3 Inter,sans-serif;color:rgba(255,255,255,.35);'
        f'margin-top:2px">D4 · Equidad</div>'
        f'</div>'

        # Brecha
        f'<div style="flex:1;background:rgba(249,115,22,.07);'
        f'border:1px solid rgba(249,115,22,.2);border-radius:8px;'
        f'padding:8px;text-align:center">'
        f'<div style="font:900 1rem/1 Inter,sans-serif;color:#F97316">'
        f'${brecha_usd/1_000_000:.2f}M</div>'
        f'<div style="font:400 8px/1.3 Inter,sans-serif;color:rgba(255,255,255,.35);'
        f'margin-top:2px">Brecha rural</div>'
        f'</div>'

        f'</div>'

        # Parroquias
        f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(255,255,255,.2);'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:5px">'
        f'IET: Índice de Equidad Territorial (100% = paridad)</div>'

        + filas
    )


def _html_z3_poa_pac(data: dict) -> str:
    """
    Sprint E.3 — CAPA 2: POA / Metas PDOT + Estado PAC.
    D2=Fidelidad Planificación · pac_publicado · metas sin PAC.
    """
    tgi     = data.get("tgi", {})
    psg     = data.get("psg", {})
    fin     = data.get("financiero", {})

    d2_val  = tgi.get("d2", {}).get("valor", 69.93)
    d2_col  = _sem(d2_val)

    pac_pub      = psg.get("pac_publicado", True)
    pac_col      = "#22C55E" if pac_pub else "#EF4444"
    pac_lbl      = "Publicado" if pac_pub else "Pendiente"

    metas_sin_pac = 4           # dato canónico p12_cadena — CHK-08
    mp_col        = "#F97316" if metas_sin_pac > 0 else "#22C55E"

    # Fechas críticas
    ti_raw = fin.get("ti_2026_raw_pct", 1.05)

    return (
        f'<div style="font:800 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">'
        f'🎯 POA · Metas PDOT</div>'

        # D2 metric principal
        f'<div style="background:{d2_col}10;border:1px solid {d2_col}22;'
        f'border-radius:8px;padding:8px 10px;margin-bottom:7px;'
        f'display:flex;justify-content:space-between;align-items:center">'
        f'<div>'
        f'<div style="font:900 1.4rem/1 Inter,sans-serif;color:{d2_col}">{d2_val:.0f}%</div>'
        f'<div style="font:400 7px/1 Inter,sans-serif;color:rgba(255,255,255,.3);margin-top:3px">'
        f'D2 · Fidelidad Planificación</div>'
        f'</div>'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:{d2_col};'
        f'padding:2px 6px;border:1px solid {d2_col}44;border-radius:4px;text-transform:uppercase">'
        f'{"OK" if d2_val >= 70 else "ALERTA"}</div>'
        f'</div>'

        # PAC + Metas sin PAC
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:7px">'
        f'<div style="padding:6px 7px;background:rgba(255,255,255,.025);'
        f'border:1px solid rgba(255,255,255,.06);border-radius:7px;text-align:center">'
        f'<div style="font:700 9px/1 Inter,sans-serif;color:{pac_col}">{pac_lbl} ✓</div>'
        f'<div style="font:400 7px/1 Inter,sans-serif;color:rgba(255,255,255,.2);margin-top:2px">'
        f'PAC 2026</div>'
        f'</div>'
        f'<div style="padding:6px 7px;background:rgba(255,255,255,.025);'
        f'border:1px solid {mp_col}22;border-radius:7px;text-align:center">'
        f'<div style="font:700 9px/1 Inter,sans-serif;color:{mp_col}">{metas_sin_pac} sin PAC</div>'
        f'<div style="font:400 7px/1 Inter,sans-serif;color:rgba(255,255,255,.2);margin-top:2px">'
        f'Metas bloqueadas</div>'
        f'</div>'
        f'</div>'

        # Q2 deadline
        f'<div style="display:flex;align-items:center;gap:6px;padding:5px 7px;'
        f'background:rgba(239,68,68,.04);border:1px solid rgba(239,68,68,.12);border-radius:6px">'
        f'<div style="width:5px;height:5px;border-radius:50%;background:#EF4444;flex-shrink:0"></div>'
        f'<div style="font:400 8px/1.3 Inter,sans-serif;color:rgba(255,255,255,.4)">'
        f'Ti: <span style="color:#EF4444;font-weight:700">{ti_raw:.2f}%</span> '
        f'· Cierre Q2 <span style="color:#F97316">30 Jun</span> · COPFP Art. 113</div>'
        f'</div>'
    )


def _html_z4_inst(data: dict) -> str:
    """
    Sprint E.3 — CAPA 2: Transparencia institucional.
    LOTAIP · RdC CPCCS · D5 Capacidad Institucional.
    Conservative: LOTAIP sin dato en snapshot → ALERTA hasta confirmar.
    """
    tgi     = data.get("tgi", {})
    d5_val  = tgi.get("d5", {}).get("valor", 100.0)
    d5_col  = _sem(d5_val)

    items = [
        ("#F59E0B", "LOTAIP",        "Actualización mensual · verificar cumplimiento"),
        ("#F59E0B", "RdC CPCCS",     "Validación ciudadana · plazo legal próximo"),
        ("#22C55E", "SNP / SIGAD",   f"D5 {d5_val:.0f}% · Capacidad Institucional OK"),
    ]

    rows = "".join(
        f'<div style="display:flex;align-items:flex-start;gap:7px;padding:5px 0;'
        f'border-bottom:1px solid rgba(255,255,255,.035)">'
        f'<div style="width:5px;height:5px;border-radius:50%;background:{c};'
        f'flex-shrink:0;margin-top:3px"></div>'
        f'<div>'
        f'<div style="font:700 8px/1 Inter,sans-serif;color:{c}">{lbl}</div>'
        f'<div style="font:400 7px/1.3 Inter,sans-serif;color:rgba(255,255,255,.32);margin-top:1px">{det}</div>'
        f'</div>'
        f'</div>'
        for c, lbl, det in items
    )

    return (
        f'<div style="font:800 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">'
        f'🏛 Transparencia</div>'

        # D5 headline
        f'<div style="background:{d5_col}10;border:1px solid {d5_col}22;'
        f'border-radius:8px;padding:8px 10px;margin-bottom:7px;'
        f'display:flex;justify-content:space-between;align-items:center">'
        f'<div>'
        f'<div style="font:900 1.4rem/1 Inter,sans-serif;color:{d5_col}">{d5_val:.0f}%</div>'
        f'<div style="font:400 7px/1 Inter,sans-serif;color:rgba(255,255,255,.3);margin-top:3px">'
        f'D5 · Capacidad Institucional</div>'
        f'</div>'
        f'<div style="font:700 7px/1 Inter,sans-serif;color:{d5_col};'
        f'padding:2px 6px;border:1px solid {d5_col}44;border-radius:4px;text-transform:uppercase">'
        f'SNP OK</div>'
        f'</div>'

        + rows
    )


def _html_z4_territorio(data: dict) -> str:
    """
    Sprint E.3 — CAPA 2: Territorio · Equidad.
    Extraído de _html_z3z4_compact para modularidad.
    """
    tgi        = data.get("tgi", {})
    irs_val    = tgi.get("irs", {}).get("valor", 79.7)
    irs_cl     = tgi.get("irs", {}).get("clasificacion", "Muy Regresivo")
    d4_val     = tgi.get("d4", {}).get("valor", 66.85)
    brecha_usd = tgi.get("brecha_rural_usd", 1791935)
    d4c        = _sem(d4_val)

    parroquias = data.get("territorial", {}).get("parroquias", _FALLBACK["territorial"]["parroquias"])
    criticas   = [p for p in parroquias if p.get("iet_local_pct", 100) < 50][:3]
    z4_rows    = "".join(_parroquia_row(p) for p in criticas) if criticas else ""

    return (
        f'<div style="font:800 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">'
        f'🗺 Territorio</div>'

        # KPIs
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:8px">'
        f'<div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.18);'
        f'border-radius:7px;padding:7px;text-align:center">'
        f'<div style="font:900 1.2rem/1 Inter,sans-serif;color:#EF4444">{irs_val:.0f}</div>'
        f'<div style="font:400 7px/1.3 Inter,sans-serif;color:rgba(255,255,255,.3);margin-top:2px">'
        f'IRS · {irs_cl}</div>'
        f'</div>'
        f'<div style="background:{d4c}0D;border:1px solid {d4c}20;'
        f'border-radius:7px;padding:7px;text-align:center">'
        f'<div style="font:900 1rem/1 Inter,sans-serif;color:{d4c}">${brecha_usd/1_000_000:.2f}M</div>'
        f'<div style="font:400 7px/1.3 Inter,sans-serif;color:rgba(255,255,255,.3);margin-top:2px">'
        f'Brecha rural</div>'
        f'</div>'
        f'</div>'

        + (
            f'<div style="font:700 7px/1 Inter,sans-serif;color:rgba(255,255,255,.18);'
            f'text-transform:uppercase;letter-spacing:.07em;margin-bottom:4px">'
            f'Parroquias bajo IET 50%</div>'
            + z4_rows
            if criticas else
            f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.2)">'
            f'Sin parroquias críticas en este corte.</div>'
        )
    )


def _html_z3z4_compact(data: dict) -> str:
    """
    Sprint E.3 — CAPA 2: Control Estratégico.
    3 columnas: POA/Metas · Transparencia · Territorio.
    Cada columna es una zona clickeable que lleva a su módulo técnico.
    """
    return (
        f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;height:100%">'
        f'<div>{_html_z3_poa_pac(data)}</div>'
        f'<div>{_html_z4_inst(data)}</div>'
        f'<div>{_html_z4_territorio(data)}</div>'
        f'</div>'
    )


def _html_z5_ecosistema(eco: list[dict]) -> str:
    h90_total_cod = sum(e.get("codificado", 0) for e in eco)
    h90_total_dev = sum(e.get("devengado", 0) for e in eco)
    ti_holding    = (h90_total_dev / h90_total_cod * 100) if h90_total_cod else 0

    cards = "".join(_entity_card(e) for e in eco)

    return (
        _zt("🏢", "Ecosistema Municipal",
            "4 entidades · TOP semafórico · Trayectoria Operativa Proyectada · Corte Q1-2026",
            "#00D4FF") +

        # 4-col grid interno
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;'
        f'margin-bottom:10px">'
        + cards +
        f'</div>'

        # Holding total
        f'<div style="padding:8px 12px;background:rgba(255,255,255,.02);'
        f'border:1px solid rgba(255,255,255,.06);border-radius:8px;'
        f'display:flex;justify-content:space-between;align-items:center">'
        f'<span style="font:700 9px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
        f'text-transform:uppercase;letter-spacing:.06em">Holding Municipal · Q1-2026</span>'
        f'<div style="display:flex;gap:14px">'
        f'<span style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.3)">'
        f'Codificado: <span style="color:rgba(255,255,255,.55)">'
        f'${h90_total_cod/1_000_000:.2f}M</span></span>'
        f'<span style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.3)">'
        f'Devengado: <span style="color:rgba(255,255,255,.55)">'
        f'${h90_total_dev/1_000_000:.2f}M</span></span>'
        f'<span style="font:700 9px/1 Inter,sans-serif;color:#F59E0B">'
        f'Ti Holding: {ti_holding:.1f}%</span>'
        f'</div></div>'

        f'<div style="font:400 8px/1.5 Inter,sans-serif;color:rgba(255,255,255,.15);'
        f'margin-top:6px">Fuente: H90_PRESUPUESTO_CONSOLIDADO · Gold Master v5.5_TGI · '
        f'NOMENCLATURA_CANONICA Sección 7.2</div>'
    )


def _html_z6_ia(data: dict, eco: list[dict], narrative: str) -> str:
    fin     = data.get("financiero", {})
    fondos  = fin.get("fondos_bloqueados_est", 3660000)
    fondos_det = fin.get("fondos_bloqueados_detalle", "BDE $3.5M + Gender Bond $95K + ONU Mujeres $65K")
    tgi     = data.get("tgi", {})
    ied     = tgi.get("ied_global", {}).get("valor", 31.14)
    ied_c   = _sem(ied)

    return (
        f'<div style="display:grid;grid-template-columns:1.3fr 1fr;gap:14px">'

        # --- Oportunidades ---
        f'<div>'
        + _zt("✦", "Oportunidades", "Fondos disponibles · Cooperación · Capacidad") +

        f'<div style="background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.2);'
        f'border-radius:10px;padding:12px 14px;margin-bottom:10px">'
        f'<div style="font:700 8px/1 Inter,sans-serif;color:#9B79FF;letter-spacing:.07em;'
        f'text-transform:uppercase;margin-bottom:5px">Fondos Bloqueados</div>'
        f'<div style="font:900 2rem/1 Inter,sans-serif;color:#7C5CFC;'
        f'letter-spacing:-.03em">${fondos/1_000_000:.2f}M</div>'
        f'<div style="font:400 10px/1.55 Inter,sans-serif;color:rgba(255,255,255,.38);'
        f'margin-top:4px">{fondos_det}</div>'
        f'<div style="font:600 10px/1 Inter,sans-serif;color:#9B79FF;margin-top:8px">'
        f'→ Gestionar desembolso BDE · Activar contratos pendientes</div>'
        f'</div>'

        f'<div style="display:flex;gap:8px">'

        # Cooperación
        f'<div style="flex:1;background:rgba(34,197,94,.06);'
        f'border:1px solid rgba(34,197,94,.18);border-radius:8px;padding:10px">'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
        f'margin-bottom:3px">Cooperación internacional</div>'
        f'<div style="font:700 12px/1 Inter,sans-serif;color:#22C55E">CAF · BID · PNUD</div>'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'margin-top:2px">Ventanas abiertas Q2-2026</div>'
        f'</div>'

        # IED
        f'<div style="flex:1;background:{ied_c}0D;border:1px solid {ied_c}22;'
        f'border-radius:8px;padding:10px">'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
        f'margin-bottom:3px">Eficiencia Directiva · IED</div>'
        f'<div style="font:900 1.2rem/1 Inter,sans-serif;color:{ied_c}">{ied:.1f}%</div>'
        f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'margin-top:2px">Espacio de mejora disponible</div>'
        f'</div>'

        f'</div></div>'  # end oportunidades

        # --- QUIRA IA ---
        f'<div>'
        + _zt("◆", "QUIRA IA",
              "Análisis Preventivo Institucional · Lenguaje ejecutivo",
              "#00D4FF") +

        f'<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.15);'
        f'border-radius:10px;padding:14px;height:calc(100% - 48px);box-sizing:border-box">'

        f'<div style="font:400 11px/1.7 Inter,sans-serif;color:rgba(255,255,255,.58)">'
        f'{narrative}'
        f'</div>'

        f'<div style="margin-top:10px;padding-top:8px;'
        f'border-top:1px solid rgba(255,255,255,.06);'
        f'font:400 8px/1.5 Inter,sans-serif;color:rgba(255,255,255,.18)">'
        f'Base legal: COPFP Art. 113 · Metodología TOP QUIRA_DOCTRINE_v1.3 · '
        f'Gold Master v5.5_TGI · Corte {CORTE}'
        f'</div>'
        f'</div>'
        f'</div>'  # end QUIRA IA

        f'</div>'  # end 2-col grid
    )


# ══════════════════════════════════════════════════════════════════════════════
# CSS — scoped bajo .ve-root para evitar conflictos con Streamlit
# ══════════════════════════════════════════════════════════════════════════════

_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400&display=swap');

.ve-root * { box-sizing: border-box; font-family: 'Inter', sans-serif; }

/* ── Sprint C.1 — Jerarquía de Atención ────────────────────────────────────
   Grid asimétrico: Z1 domina (span 2 filas, col ancha).
   Peso visual: Z1 🔴 Máximo → Z2 🔴 Alto → Z34 🟡 Medio → Z5/Z6 🟢 Soporte
   ───────────────────────────────────────────────────────────────────────── */

.ve-grid {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    grid-template-rows: auto auto;
    gap: 14px;
    margin-bottom: 10px;
}

/* Z1 — DOMINANTE: ocupa columna izquierda, ambas filas */
.ve-z1 {
    grid-column: 1;
    grid-row: 1 / 3;
}

/* Z2 — ALTO: columna derecha, fila 1 */
.ve-z2 {
    grid-column: 2;
    grid-row: 1;
}

/* Z34 — MEDIO: columna derecha, fila 2 (sub-grid interno 2-col) */
.ve-z34 {
    grid-column: 2;
    grid-row: 2;
}

/* Z5 — SOPORTE: full width */
.ve-z5 { grid-column: 1 / -1; }

/* Z6 — SOPORTE: full width */
.ve-z6 { grid-column: 1 / -1; }

/* Zone card base */
.ve-zone {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 20px;
}

/* Z1 — borde sutil diferenciado: dominante institucional */
.ve-z1 {
    border-color: rgba(255,255,255,.09);
}

/* Z34 — padding reducido: zona compacta */
.ve-z34 {
    padding: 14px 16px;
}

/* Z5 ecosistema — identidad holding */
.ve-z5 {
    background: rgba(0,212,255,.02);
    border-color: rgba(0,212,255,.12);
}

/* Z6 IA — fondo neutro */
.ve-z6 {
    background: rgba(255,255,255,.02);
    border-color: rgba(255,255,255,.06);
}

/* ── Sprint C.3 — Observabilidad Viva ──────────────────────────────────────
   El sistema respira. Pulsos mínimos — señal, no ruido.
   ───────────────────────────────────────────────────────────────────────── */

/* Ruptura badge glow — 2.8s · solo cuando categoría RUPTURA */
@keyframes ve-ruptura-glow {
    0%, 100% { box-shadow: 0 0 0 0 transparent; }
    50%       { box-shadow: 0 0 0 5px rgba(239,68,68,.14),
                            0 0 22px rgba(239,68,68,.22); }
}

/* Heartbeat del sistema vivo — live dot en header */
@keyframes ve-live-beat {
    0%, 100% { opacity: 1;  transform: scale(1.0); }
    50%       { opacity: .28; transform: scale(.58); }
}

/* Briefing strip border pulse — solo en ruptura GAD */
@keyframes ve-briefing-glow {
    0%, 100% { border-left-color: rgba(239,68,68,.60); }
    50%       { border-left-color: rgba(239,68,68,1.00); }
}

/* Utility classes */
.ve-ruptura-pulse {
    animation: ve-ruptura-glow 2.8s ease-in-out infinite;
}

.ve-live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22C55E;
    display: inline-block;
    flex-shrink: 0;
    animation: ve-live-beat 1.8s ease-in-out infinite;
}

.ve-briefing-live {
    animation: ve-briefing-glow 3.2s ease-in-out infinite;
}

/* Responsive: mobile stack */
@media (max-width: 900px) {
    .ve-grid {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
    }
    .ve-z1, .ve-z2, .ve-z34, .ve-z5, .ve-z6 {
        grid-column: 1;
        grid-row: auto;
    }
    .eco-grid { grid-template-columns: repeat(2, 1fr) !important; }
}
@media (max-width: 480px) {
    .eco-grid { grid-template-columns: 1fr !important; }
}
</style>"""


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Vista Ejecutiva · Sprint C.3 Observabilidad Viva.
    Llamado desde env_gov.py cuando el rol activo es 'ejecutivo'.

    Estructura de atención (3 capas):
      CAPA 1 → Header VIVO + Briefing strip animado (identidad + situación)
      CAPA 2 → Z1 ruptura pulsante (dominante) + Z2 (alto) + Z34 (compacto)
      CAPA 3 → Z5 (ecosistema) + Z6 (IA + oportunidades)

    Sprint C.3: CSS @keyframes · ve-ruptura-pulse · ve-live-dot · ve-briefing-live
    """
    from datetime import datetime
    data      = _load()
    ts_render = datetime.now().strftime("%H:%M · %d/%m")

    # ── Computaciones Python (puras, deterministas) ───────────────────────────
    eco       = _compute_ecosistema(data)
    gad_top   = eco[0]                        # GAD siempre índice 0
    narrative = _compose_quira_ia(data, eco)

    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Header institucional + SISTEMA VIVO ──────────────────────────────────
    st.markdown(
        f'<div class="ve-root">{_html_header(data, ts=ts_render)}</div>',
        unsafe_allow_html=True,
    )

    # ── Briefing strip + Grid principal ──────────────────────────────────────
    # IMPORTANTE: sin líneas en blanco dentro del string HTML —
    # el parser Markdown de Streamlit termina bloques HTML en blank lines.
    # Usar concatenación de f-strings sin triple-quote con saltos vacíos.
    grid_html = (
        f'<div class="ve-root">'
        f'{_html_briefing_strip(eco, narrative)}'
        f'{_html_decisiones_strip(data)}'
        f'<div class="ve-grid">'
        f'<div class="ve-zone ve-z1">{_html_z1_pulso(data, gad_top)}</div>'
        f'<div class="ve-zone ve-z2">{_html_z2_urgente(data)}</div>'
        f'<div class="ve-zone ve-z34">{_html_z3z4_compact(data)}</div>'
        f'<div class="ve-zone ve-z5">{_html_z5_ecosistema(eco)}</div>'
        f'<div class="ve-zone ve-z6">{_html_z6_ia(data, eco, narrative)}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(grid_html, unsafe_allow_html=True)

    # ── Drill-down — Navegación Rápida (Sprint E.1) ───────────────────────────
    # Botones nativos Streamlit → no dependen de HTML clickeable.
    # Para el Ejecutivo abren vistas expandidas inline.
    # Para el Técnico navegan al módulo técnico correspondiente.
    from utils.session import is_tecnico as _is_tec
    drill = st.session_state.get("ve_drill", None)

    st.markdown(
        '<div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,.06)">'
        '<div style="font:700 8px/1 Inter,sans-serif;color:rgba(255,255,255,.18);'
        'letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px">VER EN DETALLE →</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    nav_cols = st.columns(6)
    _drill_map = [
        ("🎯 Metas · POA",      "poa",         "analisis"       if _is_tec() else None),
        ("📊 TGI Completo",     "tgi",         "cadena"         if _is_tec() else None),
        ("🚨 SAT · Alertas",    "sat",         "alertas"        if _is_tec() else None),
        ("🏛 Transparencia",    "lotaip",      "transparencia"  if _is_tec() else None),
        ("🏢 Ecosistema",       "ecosistema",  "municipal"      if _is_tec() else None),
        ("🤖 QUIRA IA",         "ia",          "analisis"       if _is_tec() else None),
    ]

    for i, (label, drill_key, mod_key) in enumerate(_drill_map):
        with nav_cols[i]:
            is_active = (drill == drill_key)
            if st.button(
                label,
                key=f"ve_nav_{drill_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                if is_active:
                    # Toggle off
                    st.session_state["ve_drill"] = None
                elif mod_key and _is_tec():
                    # Técnico → navega al módulo dedicado
                    st.session_state["gov_module"] = mod_key
                    st.session_state["ve_drill"] = None
                else:
                    # Ejecutivo → expansión inline
                    st.session_state["ve_drill"] = drill_key
                st.rerun()

    # ── Expansión inline (Ejecutivo sin acceso a módulos técnicos) ────────────
    drill = st.session_state.get("ve_drill", None)
    if drill:
        st.markdown(
            f'<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.12);'
            f'border-radius:12px;padding:16px 18px;margin-top:8px">'
            f'<div style="font:800 9px/1 Inter,sans-serif;color:rgba(0,212,255,.7);'
            f'letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px">'
            f'🔍 Detalle: {drill.upper()}</div></div>',
            unsafe_allow_html=True,
        )
        if drill == "tgi":
            # D1-D5 expandido
            tgi = data.get("tgi", {})
            dims = [("D1","Legalidad","Marco normativo"),
                    ("D2","Planificación","PDOT · PSG"),
                    ("D3","Inversión","eSIGEF · ejecución"),
                    ("D4","Equidad","Territorio · NBI"),
                    ("D5","Institucional","Capacidad interna")]
            for k, nombre, desc in dims:
                val = tgi.get(k, {}).get("valor", 0)
                col = "#22C55E" if val >= 70 else "#F59E0B" if val >= 50 else "#EF4444"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:8px 12px;background:rgba(255,255,255,.02);border-radius:8px;'
                    f'margin-bottom:4px"><div><span style="font:700 10px/1 Inter,sans-serif;'
                    f'color:rgba(255,255,255,.7)">{k} — {nombre}</span>'
                    f'<span style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
                    f'margin-left:8px">{desc}</span></div>'
                    f'<span style="font:900 14px/1 Inter,sans-serif;color:{col}">{val:.1f}%</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        elif drill == "sat":
            sat = data.get("sat_gm", {})
            activas = sat.get("sat_activas_detalle", {})
            for cod, info in activas.items():
                st.markdown(
                    f'<div style="padding:10px 14px;background:rgba(239,68,68,.06);'
                    f'border:1px solid rgba(239,68,68,.2);border-radius:8px;margin-bottom:6px">'
                    f'<div style="font:800 9px/1 Inter,sans-serif;color:#EF4444">{cod}</div>'
                    f'<div style="font:400 9px/1.4 Inter,sans-serif;color:rgba(255,255,255,.55);'
                    f'margin-top:3px">{info.get("descripcion","")}</div>'
                    f'<div style="font:700 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
                    f'margin-top:4px">Peso: {info.get("peso",0)*100:.0f}%</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        elif drill == "poa":
            # Metas POA / PDOT expandido
            tgi = data.get("tgi", {})
            psg = data.get("psg", {})
            fin = data.get("financiero", {})
            dims_poa = [
                ("D1", "Legalidad y Coherencia", tgi.get("d1", {}).get("valor", 83.5)),
                ("D2", "Fidelidad Planificación", tgi.get("d2", {}).get("valor", 69.93)),
                ("D3", "Ejecución Presupuestaria", tgi.get("d3", {}).get("valor", 14.58)),
            ]
            for cod, nombre, val in dims_poa:
                col = "#22C55E" if val >= 70 else "#F59E0B" if val >= 50 else "#EF4444"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:8px 12px;background:rgba(255,255,255,.02);border-radius:8px;margin-bottom:4px">'
                    f'<div><span style="font:700 10px/1 Inter,sans-serif;color:rgba(255,255,255,.7)">'
                    f'{cod} — {nombre}</span></div>'
                    f'<span style="font:900 14px/1 Inter,sans-serif;color:{col}">{val:.1f}%</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            pac_pub = psg.get("pac_publicado", True)
            ti_raw  = fin.get("ti_2026_raw_pct", 1.05)
            st.markdown(
                f'<div style="padding:10px 14px;background:rgba(245,158,11,.04);'
                f'border:1px solid rgba(245,158,11,.16);border-radius:8px;margin-top:6px">'
                f'<div style="font:700 9px/1.4 Inter,sans-serif;color:rgba(255,255,255,.6)">'
                f'PAC 2026: <span style="color:{"#22C55E" if pac_pub else "#EF4444"}">'
                f'{"Publicado" if pac_pub else "Pendiente"}</span> · '
                f'4 metas sin PAC (bloqueadas) · Ti Q1: <span style="color:#EF4444">{ti_raw:.2f}%</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        elif drill == "lotaip":
            # Transparencia + RdC expandido
            tgi   = data.get("tgi", {})
            d5_v  = tgi.get("d5", {}).get("valor", 100.0)
            items_lotaip = [
                ("#F59E0B", "LOTAIP",    "Actualización mensual · verificar cumplimiento en portal MAAP"),
                ("#F59E0B", "RdC CPCCS", "Rendición de cuentas ciudadana · plazo legal próximo"),
                ("#22C55E", "D5 Capacidad Institucional", f"{d5_v:.0f}% · SNP · SIGAD al día"),
                ("#22C55E", "PAC Publicado", "Plan Anual de Contratación publicado en SERCOP"),
            ]
            for col, lbl, det in items_lotaip:
                st.markdown(
                    f'<div style="display:flex;align-items:flex-start;gap:8px;padding:8px 12px;'
                    f'background:rgba(255,255,255,.02);border-radius:8px;margin-bottom:4px">'
                    f'<div style="width:7px;height:7px;border-radius:50%;background:{col};'
                    f'flex-shrink:0;margin-top:3px"></div>'
                    f'<div><div style="font:700 9px/1 Inter,sans-serif;color:{col}">{lbl}</div>'
                    f'<div style="font:400 8px/1.4 Inter,sans-serif;color:rgba(255,255,255,.4);margin-top:2px">'
                    f'{det}</div></div></div>',
                    unsafe_allow_html=True,
                )
        elif drill == "ecosistema":
            for ent in eco:
                col = ent.get("color", "#F97316")
                ti  = ent.get("ti_pct", 0)
                top = ent.get("top", 0)
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:10px 14px;background:rgba(255,255,255,.02);border-radius:8px;'
                    f'margin-bottom:4px">'
                    f'<div style="font:600 10px/1 Inter,sans-serif;color:rgba(255,255,255,.7)">'
                    f'{ent.get("emoji","")} {ent.get("nombre","")}</div>'
                    f'<div style="display:flex;gap:16px;align-items:center">'
                    f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.35)">'
                    f'Ti: {ti:.2f}%</div>'
                    f'<div style="font:900 13px/1 Inter,sans-serif;color:{col}">'
                    f'TOP {top:.1f}%</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
        elif drill == "ia":
            st.markdown(
                f'<div style="font:400 11px/1.6 Inter,sans-serif;'
                f'color:rgba(255,255,255,.6);padding:4px 0">{narrative}</div>',
                unsafe_allow_html=True,
            )
        elif drill == "territorio":
            parroquias = data.get("territorial", {}).get("parroquias", [])
            for p in parroquias:
                nbi = p.get("nbi_pct", 0)
                col = "#EF4444" if nbi > 55 else "#F59E0B" if nbi > 40 else "#22C55E"
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;'
                    f'padding:8px 12px;background:rgba(255,255,255,.02);border-radius:8px;'
                    f'margin-bottom:4px">'
                    f'<div style="font:600 10px/1 Inter,sans-serif;color:rgba(255,255,255,.7)">'
                    f'{"🏙" if p.get("tipo")=="Urbana" else "🌿"} {p.get("nombre","")}'
                    f'<span style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.3);'
                    f'margin-left:6px">{p.get("tipo","")}</span></div>'
                    f'<div style="display:flex;gap:14px">'
                    f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.35)">'
                    f'NBI: <span style="color:{col};font-weight:700">{nbi:.1f}%</span></div>'
                    f'<div style="font:400 8px/1 Inter,sans-serif;color:rgba(255,255,255,.35)">'
                    f'${p.get("inv_percapita_q1",0)}/hab</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )

        if st.button("✕ Cerrar detalle", key="ve_close_drill", type="secondary"):
            st.session_state["ve_drill"] = None
            st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        f'<div style="margin-top:10px;font:400 8px/1 JetBrains Mono,monospace;'
        f'color:rgba(255,255,255,.1);text-align:right;display:flex;'
        f'justify-content:space-between;align-items:center">'
        f'<span style="color:rgba(255,255,255,.07)">Cache datos: 5 min · TTL activo</span>'
        f'<span>QUIRA Intelligence · Sprint E.3 · '
        f'Gold Master v5.5_TGI · Corte Q1-2026 · Dylus Lab © 2026</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
