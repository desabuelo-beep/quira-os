"""
QUIRA Intelligence — Vista Ejecutiva · Motor Predictivo Institucional v1
Sprint B · p_vista_ejecutiva.py

6 zonas · CSS Grid · TOP semafórico · Ecosistema Municipal
Doctrina QUIRA_DOCTRINE_v1.3: "El alcalde no navega. El alcalde interpreta."
El alcalde entiende el estado del municipio + ecosistema en 30 segundos.

━━━ ARQUITECTURA ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HEADER       — Barra institucional: GAD · TGI · SAT · Alcalde
  Zona 1       — Pulso Institucional: TGI + D1-D5 + ICPI
  Zona 2       — Lo Urgente: SAT sistémicas (causa + acción + ley)
  Zona 3       — Compromisos: RDC · PDOT · IFE (honesto) · Q2 cierre
  Zona 4       — Territorio: IRS · 7 parroquias · brecha rural
  Zona 5       — Ecosistema Municipal: Patronato · EP Aseo · Bomberos · GAD
  Zona 6       — QUIRA IA: brief ejecutivo + oportunidades

  Layout: CSS Grid 2-col (Z1+Z2 · Z3+Z4) → full-width (Z5 · Z6)
  TOP: utils/top.py — Trayectoria Operativa Proyectada (NOMENCLATURA 7.2)
  Datos: financiero.h90_consolidado del Gold Master v5.5

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

def _html_header(data: dict) -> str:
    tgi       = data.get("tgi", {})
    score     = tgi.get("score", 0.0)
    color_tgi = tgi.get("color_hex", "#FFB700")
    sat       = data.get("sat_gm", {})
    n_act     = sat.get("activas_count", 0)
    clasif    = sat.get("clasif_riesgo", "—")
    apellido  = ALCALDE.split()[-1] if ALCALDE else "—"

    sc = {"BAJO": "#22C55E", "MEDIO": "#F59E0B",
          "ALTO": "#F97316", "CRÍTICO": "#EF4444"}.get(clasif, "#F97316")

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

        # Right: KPI chips
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

        f'</div></div>'
    )


def _html_z1_pulso(data: dict) -> str:
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
        _mini_bar("D1 — Legalidad",         "Marco normativo · COOTAD · PAC publicado", d1) +
        _mini_bar("D2 — Planificación",      "Fidelidad PDOT · metas en trayectoria", d2) +
        _mini_bar("D3 — Ejecución",          "Ti inversión Q1-2026 · activación pendiente", d3) +
        _mini_bar("D4 — Equidad Territorial", "IRS 79.7 — inversión concentrada urbana", d4) +
        _mini_bar("D5 — Capacidad",          "SIGAD · SNP certificados al 100%", d5)
    )

    return (
        _zt("◉", "Pulso del Municipio",
            "Índice de Gobernanza Institucional · 5 dimensiones") +

        f'<div style="font:900 3.4rem/1 Inter,sans-serif;color:{color_tgi};'
        f'letter-spacing:-.05em;margin-bottom:3px">{score:.1f}</div>'
        f'<div style="font:700 12px/1 Inter,sans-serif;color:{color_tgi};'
        f'margin-bottom:2px">{clasif}</div>'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.25);'
        f'margin-bottom:12px">TGI · Gobernanza Integral · Escala 0–100</div>'

        f'<div style="font:600 10px/1 Inter,sans-serif;color:#22C55E;'
        f'margin-bottom:16px">↗ Tendencia positiva 2023–2025 (ICPI: 57→67→70)</div>'

        + bars +

        f'<div style="margin-top:10px;padding-top:8px;'
        f'border-top:1px solid rgba(255,255,255,.05)">'
        f'<div style="font:400 9px/1 Inter,sans-serif;color:rgba(255,255,255,.2)">'
        f'ICPI (velocidad de ejecución) — '
        f'<span style="color:rgba(255,255,255,.45)">{icpi_pct:.1f}%</span> · {icpi_cl}'
        f'</div></div>'
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

/* Main grid: 2-col para Z1-Z4, full-width para Z5 y Z6 */
.ve-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-bottom: 10px;
}
.ve-z5, .ve-z6 { grid-column: 1 / -1; }

/* Zone card base */
.ve-zone {
    background: rgba(255,255,255,.025);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px;
    padding: 20px;
}

/* Zona 5: ecosistema — fondo ligeramente más oscuro */
.ve-z5 {
    background: rgba(0,212,255,.02);
    border-color: rgba(0,212,255,.12);
}

/* Zona 6: IA — fondo neutral */
.ve-z6 {
    background: rgba(255,255,255,.02);
    border-color: rgba(255,255,255,.06);
}

/* Responsive: mobile stack */
@media (max-width: 768px) {
    .ve-grid { grid-template-columns: 1fr; }
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
    Vista Ejecutiva v2 — Motor Predictivo Institucional v1.
    Llamado desde env_gov.py cuando el rol activo es 'ejecutivo'.
    No renderiza header GOV — tiene su propio header institucional.
    """
    data = _load()

    # ── Computaciones Python (puras, deterministas) ───────────────────────────
    eco       = _compute_ecosistema(data)
    narrative = _compose_quira_ia(data, eco)

    # ── CSS ───────────────────────────────────────────────────────────────────
    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="ve-root">{_html_header(data)}</div>',
        unsafe_allow_html=True,
    )

    # ── Grid principal: 6 zonas ───────────────────────────────────────────────
    grid_html = f"""
<div class="ve-root">
<div class="ve-grid">
  <div class="ve-zone ve-z1">{_html_z1_pulso(data)}</div>
  <div class="ve-zone ve-z2">{_html_z2_urgente(data)}</div>
  <div class="ve-zone ve-z3">{_html_z3_compromisos(data)}</div>
  <div class="ve-zone ve-z4">{_html_z4_territorio(data)}</div>
  <div class="ve-zone ve-z5">{_html_z5_ecosistema(eco)}</div>
  <div class="ve-zone ve-z6">{_html_z6_ia(data, eco, narrative)}</div>
</div>
</div>
"""
    st.markdown(grid_html, unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:10px;font:400 8px/1 JetBrains Mono,monospace;'
        'color:rgba(255,255,255,.1);text-align:right">'
        'QUIRA Intelligence · Motor Predictivo Institucional v1 · '
        'Gold Master v5.5_TGI · Corte Q1-2026 · Dylus Lab © 2026'
        '</div>',
        unsafe_allow_html=True,
    )
