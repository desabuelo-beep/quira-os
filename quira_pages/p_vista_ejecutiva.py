"""
QUIRA Intelligence — Vista Ejecutiva Bloomberg-style
Sprint B · p_vista_ejecutiva.py

Pantalla principal para el rol Ejecutivo (alcalde, concejales).
Doctrina: "El alcalde no navega. El alcalde interpreta."

5 zonas · Sin módulos de navegación · QUIRA IA integrado
Lenguaje político-institucional, nunca técnico.
El alcalde entiende el estado del municipio en 30 segundos.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from config import GAD_NOMBRE, ALCALDE, CORTE


# ══════════════════════════════════════════════════════════════════════════════
# DATOS — carga Gold Master snapshot
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
            "SAT-III": {"peso": 0.20},
            "SAT-IV":  {"peso": 0.10},
            "SAT-V":   {"peso": 0.05},
        },
    },
    "financiero": {
        "ti_2026_raw_pct": 1.05,
        "fondos_bloqueados_est": 3660000,
        "fondos_bloqueados_detalle": "BDE $3.5M · Gender Bond $95K · ONU Mujeres $65K",
    },
    "psg": {"psg_fidelidad_pct": 69.93, "psg_ejecucion_2025_pct": 59.85},
    "gad": {"promesas_cne": 66, "metas_pdot": 25},
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
# HELPERS VISUALES
# ══════════════════════════════════════════════════════════════════════════════

def _color(valor: float) -> str:
    """Color semafórico para cualquier métrica 0-100."""
    if valor >= 70: return "#22C55E"
    if valor >= 50: return "#FFB700"
    if valor >= 30: return "#F97316"
    return "#EF4444"


def _mini_bar(label: str, valor: float) -> str:
    c = _color(valor)
    w = max(0, min(100, valor))
    return f"""
<div style="margin-bottom:7px">
  <div style="display:flex;justify-content:space-between;margin-bottom:3px">
    <span style="font-size:9px;color:rgba(255,255,255,.45)">{label}</span>
    <span style="font-size:10px;font-weight:700;color:{c}">{valor:.0f}%</span>
  </div>
  <div style="height:3px;background:rgba(255,255,255,.07);border-radius:2px">
    <div style="height:3px;width:{w}%;background:{c};border-radius:2px"></div>
  </div>
</div>"""


def _zona_title(icon: str, title: str, subtitle: str,
                color: str = "rgba(255,255,255,.3)") -> str:
    return f"""
<div style="margin-bottom:14px">
  <div style="font-size:9px;font-weight:700;color:{color};
              letter-spacing:.1em;text-transform:uppercase">{icon} {title}</div>
  <div style="font-size:10px;color:rgba(255,255,255,.22);margin-top:2px">{subtitle}</div>
</div>"""


def _zona_wrap(content: str, accent: str = "rgba(255,255,255,.08)") -> str:
    return f"""
<div style="background:rgba(255,255,255,.025);
            border:1px solid {accent};
            border-radius:14px;padding:20px;height:100%">
  {content}
</div>"""


# ══════════════════════════════════════════════════════════════════════════════
# HEADER INSTITUCIONAL
# ══════════════════════════════════════════════════════════════════════════════

def _header(data: dict) -> None:
    tgi       = data.get("tgi", {})
    score     = tgi.get("score", 0.0)
    color_tgi = tgi.get("color_hex", "#FFB700")
    sat       = data.get("sat_gm", {})
    n_act     = sat.get("activas_count", 0)
    clasif    = sat.get("clasif_riesgo", "—")
    alcalde_apellido = ALCALDE.split()[-1] if ALCALDE else "—"

    sat_colors = {"BAJO": "#22C55E", "MEDIO": "#F59E0B",
                  "ALTO": "#F97316",  "CRÍTICO": "#EF4444"}
    sat_c = sat_colors.get(clasif, "#F97316")

    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:12px 18px;
            background:rgba(255,255,255,.02);
            border:1px solid rgba(255,255,255,.07);
            border-radius:12px;margin-bottom:18px">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:20px">🏛</span>
    <div>
      <div style="font-size:14px;font-weight:900;color:#E2E8F0;
                  letter-spacing:-.02em">{GAD_NOMBRE}</div>
      <div style="font-size:9px;color:rgba(255,255,255,.28);
                  letter-spacing:.05em;margin-top:1px">
        QUIRA Institucional · Vista Ejecutiva · Corte {CORTE}</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <div style="text-align:center;padding:6px 14px;
                background:{color_tgi}14;
                border:1px solid {color_tgi}33;border-radius:8px">
      <div style="font-size:8px;color:rgba(255,255,255,.35);
                  letter-spacing:.07em;text-transform:uppercase">TGI Global</div>
      <div style="font-size:1.5rem;font-weight:900;color:{color_tgi};
                  line-height:1.1">{score:.1f}</div>
    </div>
    <div style="text-align:center;padding:6px 14px;
                background:{sat_c}14;
                border:1px solid {sat_c}33;border-radius:8px">
      <div style="font-size:8px;color:rgba(255,255,255,.35);
                  letter-spacing:.07em;text-transform:uppercase">Alertas SAT</div>
      <div style="font-size:1.5rem;font-weight:900;color:{sat_c};
                  line-height:1.1">{n_act}</div>
    </div>
    <div style="text-align:center;padding:6px 14px;
                background:rgba(0,212,255,.07);
                border:1px solid rgba(0,212,255,.2);border-radius:8px">
      <div style="font-size:8px;color:rgba(0,212,255,.5);
                  letter-spacing:.07em;text-transform:uppercase">Ejecutivo</div>
      <div style="font-size:12px;font-weight:700;color:#00D4FF;
                  margin-top:2px">{alcalde_apellido}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ZONA 1 — PULSO GLOBAL
# ══════════════════════════════════════════════════════════════════════════════

def _zona1_pulso(data: dict) -> None:
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

    # Tendencia 2023→2025 (ICPI histórico: 57.36→67.12→69.93)
    tendencia_txt   = "↗ Tendencia positiva 2023–2025"
    tendencia_color = "#22C55E"

    bars = (
        _mini_bar("D1 — Legalidad y Coherencia Normativa", d1) +
        _mini_bar("D2 — Fidelidad de Planificación", d2) +
        _mini_bar("D3 — Ejecución Presupuestaria", d3) +
        _mini_bar("D4 — Equidad Territorial", d4) +
        _mini_bar("D5 — Capacidad Institucional", d5)
    )

    content = f"""
{_zona_title("◉", "Pulso del Municipio",
             "Índice de Gobernanza Institucional · 5 dimensiones")}
<div style="font-size:3.4rem;font-weight:900;color:{color_tgi};
            letter-spacing:-.05em;line-height:1;margin-bottom:3px">{score:.1f}</div>
<div style="font-size:12px;font-weight:700;color:{color_tgi};
            margin-bottom:2px">{clasif}</div>
<div style="font-size:9px;color:rgba(255,255,255,.28);
            margin-bottom:10px">TGI · Gobernanza Integral · Escala 0–100</div>
<div style="font-size:10px;color:{tendencia_color};font-weight:600;
            margin-bottom:16px">{tendencia_txt}</div>
{bars}
<div style="margin-top:12px;padding-top:10px;
            border-top:1px solid rgba(255,255,255,.05)">
  <div style="font-size:9px;color:rgba(255,255,255,.22)">
    ICPI (velocidad de ejecución) — {icpi_pct:.1f}% · {icpi_cl}
  </div>
</div>"""

    st.markdown(_zona_wrap(content), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ZONA 2 — LO URGENTE
# ══════════════════════════════════════════════════════════════════════════════

_ALERTAS_EJECUTIVO: dict[str, dict] = {
    "SAT-III": {
        "titulo":  "Ejecución de inversión en alerta",
        "causa":   "Solo el 1.05% del presupuesto de inversión ejecutado en Q1. Meta mínima: 60%.",
        "tiempo":  "Cierre Q2 en ~45 días",
        "accion":  "Convocar al Director de Obras. Activar contratos de obras priorizadas.",
        "ley":     "COPFP Art. 113",
        "color":   "#EF4444",
    },
    "SAT-IV": {
        "titulo":  "Inequidad territorial crítica",
        "causa":   "Índice de Regresión Social 79.7: la inversión no llega donde más se necesita. Brecha rural: $1.79M.",
        "tiempo":  "Acumulativo desde inicio de mandato",
        "accion":  "Revisar distribución geográfica del POA. Priorizar parroquias con mayor NBI.",
        "ley":     "COOTAD Art. 192",
        "color":   "#F97316",
    },
    "SAT-V": {
        "titulo":  "Evidencia institucional insuficiente",
        "causa":   "Las direcciones no están reportando con la calidad y trazabilidad requerida.",
        "tiempo":  "Rendición de Cuentas CPCCS se aproxima",
        "accion":  "Solicitar reportes con evidencia firmada a todos los directores departamentales.",
        "ley":     "COOTAD Art. 302",
        "color":   "#F59E0B",
    },
}


def _alerta_card(codigo: str, info: dict) -> str:
    c = info["color"]
    return f"""
<div style="border:1px solid {c}2A;border-left:3px solid {c};
            border-radius:10px;padding:12px 14px;margin-bottom:8px;
            background:{c}07">
  <div style="display:flex;align-items:center;gap:7px;margin-bottom:5px">
    <span style="font-size:9px;font-weight:800;color:{c};background:{c}22;
                 padding:2px 7px;border-radius:4px;letter-spacing:.06em">{codigo}</span>
    <span style="font-size:11px;font-weight:700;color:#E2E8F0">{info['titulo']}</span>
  </div>
  <div style="font-size:10px;color:rgba(255,255,255,.5);line-height:1.55;
              margin-bottom:6px">{info['causa']}</div>
  <div style="display:flex;justify-content:space-between;align-items:center;
              flex-wrap:wrap;gap:4px;margin-bottom:6px">
    <span style="font-size:9px;color:rgba(255,255,255,.32)">⏱ {info['tiempo']}</span>
    <span style="font-size:8px;color:rgba(255,255,255,.22);">{info['ley']}</span>
  </div>
  <div style="padding-top:6px;border-top:1px solid rgba(255,255,255,.05)">
    <span style="font-size:10px;font-weight:600;color:{c}">→ {info['accion']}</span>
  </div>
</div>"""


def _zona2_urgente(data: dict) -> None:
    sat     = data.get("sat_gm", {})
    clasif  = sat.get("clasif_riesgo", "ALTO")
    n_act   = sat.get("activas_count", 0)
    activas = sat.get("sat_activas_detalle", {})

    sat_colors = {"BAJO": "#22C55E", "MEDIO": "#F59E0B",
                  "ALTO": "#F97316", "CRÍTICO": "#EF4444"}
    c_risk = sat_colors.get(clasif, "#F97316")

    cards_html = "".join(
        _alerta_card(codigo, _ALERTAS_EJECUTIVO[codigo])
        for codigo in activas
        if codigo in _ALERTAS_EJECUTIVO
    )

    content = f"""
{_zona_title("⚠", "Lo Urgente", "Alertas activas · Requieren acción del Ejecutivo",
             color="#F97316")}
<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
  <div style="font-size:2.8rem;font-weight:900;color:{c_risk};
              letter-spacing:-.04em;line-height:1">{n_act}</div>
  <div>
    <div style="font-size:13px;font-weight:700;color:{c_risk}">alertas activas</div>
    <div style="font-size:9px;color:rgba(255,255,255,.3)">Nivel de riesgo institucional: {clasif}</div>
  </div>
</div>
{cards_html}"""

    st.markdown(_zona_wrap(content, f"{c_risk}1A"), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ZONA 3 — COMPROMISOS
# ══════════════════════════════════════════════════════════════════════════════

def _compromiso_row(icon: str, titulo: str, valor: str, val_color: str,
                    desc: str, urgencia: str = "", urg_color: str = "#F59E0B") -> str:
    urg_html = (f'<div style="font-size:9px;font-weight:600;color:{urg_color};'
                f'margin-top:4px">⏱ {urgencia}</div>') if urgencia else ""
    return f"""
<div style="display:flex;align-items:flex-start;gap:10px;
            padding:10px 0;border-bottom:1px solid rgba(255,255,255,.05)">
  <span style="font-size:15px;flex-shrink:0;margin-top:1px">{icon}</span>
  <div style="flex:1;min-width:0">
    <div style="font-size:11px;font-weight:700;color:#E2E8F0">
      {titulo}
      <span style="color:{val_color};margin-left:6px;font-size:12px">{valor}</span>
    </div>
    <div style="font-size:10px;color:rgba(255,255,255,.38);
                margin-top:2px;line-height:1.4">{desc}</div>
    {urg_html}
  </div>
</div>"""


def _zona3_compromisos(data: dict) -> None:
    psg            = data.get("psg", {})
    gad            = data.get("gad", {})
    fidelidad      = psg.get("psg_fidelidad_pct", 69.93)
    promesas_cne   = gad.get("promesas_cne", 66)
    metas_pdot     = gad.get("metas_pdot", 25)
    fidelidad_col  = _color(fidelidad)

    rows = (
        _compromiso_row("📋", "Rendición de Cuentas CPCCS",
                        "Pendiente", "#F59E0B",
                        "Validación del informe anual ante la ciudadanía",
                        "Plazo legal próximo · Prioridad alta", "#EF4444") +
        _compromiso_row("🎯", f"Metas PDOT — {metas_pdot} metas",
                        f"{fidelidad:.1f}%", fidelidad_col,
                        "Fidelidad de planificación (D2) · Plan de Desarrollo") +
        _compromiso_row("📜", f"Plan de Gobierno CNE — {promesas_cne} compromisos",
                        "En monitoreo", "#00D4FF",
                        "Coherencia mandato democrático · IFE en construcción") +
        _compromiso_row("💰", "Cierre presupuestario Q2",
                        "30 Jun", "#F97316",
                        "Ejecución de inversión · Grupos 71-78 · Ti actual: 1.05%",
                        "~45 días · Riesgo COPFP Art. 113 si no se activa", "#EF4444")
    )

    content = f"""
{_zona_title("📅", "Compromisos", "Próximos 60 días · Plazos institucionales críticos")}
{rows}"""

    st.markdown(_zona_wrap(content), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ZONA 4 — TERRITORIO
# ══════════════════════════════════════════════════════════════════════════════

_PARROQUIAS: list[dict] = [
    {"n": "Montecristi (urbano)",         "icono": "◉", "c": "#22C55E", "nota": "núcleo inversión"},
    {"n": "Abdón Calderón",               "icono": "◎", "c": "#F59E0B", "nota": "brecha media"},
    {"n": "Chirijos",                     "icono": "○", "c": "#EF4444", "nota": "brecha crítica"},
    {"n": "La Pila",                      "icono": "◎", "c": "#F59E0B", "nota": "brecha media"},
    {"n": "Leonidas Plaza Gutiérrez",     "icono": "○", "c": "#EF4444", "nota": "brecha crítica"},
    {"n": "San Sebastián",                "icono": "◎", "c": "#F59E0B", "nota": "brecha media"},
]


def _parroquia_row(p: dict) -> str:
    return f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:5px 0;border-bottom:1px solid rgba(255,255,255,.04)">
  <div style="display:flex;align-items:center;gap:8px">
    <span style="color:{p['c']};font-size:10px">{p['icono']}</span>
    <span style="font-size:10px;color:#D1D5DB">{p['n']}</span>
  </div>
  <span style="font-size:9px;color:rgba(255,255,255,.3)">{p['nota']}</span>
</div>"""


def _zona4_territorio(data: dict) -> None:
    tgi          = data.get("tgi", {})
    irs          = tgi.get("irs", {})
    irs_val      = irs.get("valor", 79.7)
    irs_clasif   = irs.get("clasificacion", "Muy Regresivo")
    d4_val       = tgi.get("d4", {}).get("valor", 66.85)
    brecha_usd   = tgi.get("brecha_rural_usd", 1791935)

    d4_color = _color(d4_val)

    parroquias_html = "".join(_parroquia_row(p) for p in _PARROQUIAS)

    content = f"""
{_zona_title("🗺", "Territorio",
             "Equidad territorial · 6 parroquias · Cantón Montecristi")}
<div style="display:flex;gap:10px;margin-bottom:14px">
  <div style="flex:1;background:rgba(239,68,68,.07);
              border:1px solid rgba(239,68,68,.2);
              border-radius:8px;padding:10px 12px;text-align:center">
    <div style="font-size:1.6rem;font-weight:900;color:#EF4444;
                letter-spacing:-.03em">{irs_val:.0f}</div>
    <div style="font-size:8px;color:rgba(255,255,255,.38);margin-top:1px">
      IRS · {irs_clasif}</div>
  </div>
  <div style="flex:1;background:{d4_color}0F;
              border:1px solid {d4_color}2A;
              border-radius:8px;padding:10px 12px;text-align:center">
    <div style="font-size:1.6rem;font-weight:900;color:{d4_color};
                letter-spacing:-.03em">{d4_val:.0f}%</div>
    <div style="font-size:8px;color:rgba(255,255,255,.38);margin-top:1px">
      D4 · Equidad</div>
  </div>
</div>
<div style="font-size:10px;color:rgba(255,255,255,.32);margin-bottom:12px">
  Brecha de inversión rural estimada:
  <span style="color:#F97316;font-weight:700">${brecha_usd:,.0f}</span>
</div>
{parroquias_html}"""

    st.markdown(_zona_wrap(content), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ZONA 5 — OPORTUNIDADES + QUIRA IA
# ══════════════════════════════════════════════════════════════════════════════

def _zona5_oportunidades(data: dict) -> None:
    fin           = data.get("financiero", {})
    fondos        = fin.get("fondos_bloqueados_est", 3660000)
    fondos_det    = fin.get("fondos_bloqueados_detalle",
                             "BDE $3.5M · Gender Bond $95K · ONU Mujeres $65K")
    tgi           = data.get("tgi", {})
    ied           = tgi.get("ied_global", {}).get("valor", 31.14)
    ied_color     = _color(ied)

    st.markdown(f"""
<div style="background:rgba(255,255,255,.025);
            border:1px solid rgba(255,255,255,.07);
            border-radius:14px;padding:20px">
  <div style="display:flex;align-items:flex-start;
              justify-content:space-between;margin-bottom:14px">
    {_zona_title("✦", "Oportunidades",
                 "Fondos disponibles · Cooperación · Capacidad institucional")}
    <div style="background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.2);
                border-radius:7px;padding:5px 12px;flex-shrink:0;align-self:flex-start;
                font-size:10px;font-weight:700;color:#00D4FF;letter-spacing:.04em">
      ● QUIRA IA
    </div>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px">
    <div style="background:rgba(124,92,252,.07);border:1px solid rgba(124,92,252,.2);
                border-radius:10px;padding:14px 16px;flex:2;min-width:240px">
      <div style="font-size:8px;font-weight:700;color:#9B79FF;letter-spacing:.07em;
                  text-transform:uppercase;margin-bottom:6px">Fondos Bloqueados</div>
      <div style="font-size:2.2rem;font-weight:900;color:#7C5CFC;
                  letter-spacing:-.04em;line-height:1">${fondos/1_000_000:.2f}M</div>
      <div style="font-size:10px;color:rgba(255,255,255,.4);
                  margin-top:5px;line-height:1.55">{fondos_det}</div>
      <div style="font-size:10px;font-weight:600;color:#9B79FF;margin-top:8px">
        → Gestionar desembolso BDE · Activar contratos pendientes</div>
    </div>
    <div style="flex:1;min-width:160px;display:flex;flex-direction:column;gap:8px">
      <div style="background:rgba(34,197,94,.06);border:1px solid rgba(34,197,94,.18);
                  border-radius:8px;padding:10px 12px">
        <div style="font-size:9px;color:rgba(255,255,255,.38);margin-bottom:3px">
          Cooperación internacional activa</div>
        <div style="font-size:12px;font-weight:700;color:#22C55E">
          CAF · BID · PNUD</div>
        <div style="font-size:9px;color:rgba(255,255,255,.3);margin-top:2px">
          Ventanas abiertas Q2-2026</div>
      </div>
      <div style="background:{ied_color}0D;border:1px solid {ied_color}25;
                  border-radius:8px;padding:10px 12px">
        <div style="font-size:9px;color:rgba(255,255,255,.38);margin-bottom:3px">
          Eficiencia Directiva — IED</div>
        <div style="font-size:1.3rem;font-weight:900;color:{ied_color};
                    letter-spacing:-.03em">{ied:.1f}%</div>
        <div style="font-size:9px;color:rgba(255,255,255,.3);margin-top:2px">
          Espacio de mejora institucional disponible</div>
      </div>
    </div>
  </div>
  <div style="padding:14px 16px;
              background:rgba(0,212,255,.04);
              border:1px solid rgba(0,212,255,.12);
              border-radius:10px">
    <div style="font-size:9px;font-weight:700;color:#00D4FF;
                letter-spacing:.07em;margin-bottom:7px">
      QUIRA IA — Análisis Preventivo Institucional</div>
    <div style="font-size:11px;color:rgba(255,255,255,.6);line-height:1.65">
      Con D3=14.58% y el cierre de Q2 en aproximadamente 45 días, el municipio enfrenta
      riesgo concreto de cerrar el trimestre por debajo del umbral de ejecución legal.
      El primer punto de no retorno es <strong style="color:#FFB700">mediados de junio</strong>:
      sin activar el desembolso BDE ($3.5M) antes de esa fecha, Q2 cerrará con sub-ejecución
      que activa consecuencias bajo COPFP Art. 113.
      La acción de mayor impacto disponible en este momento es la activación de ese
      crédito, no nuevas reformas presupuestarias.
    </div>
    <div style="font-size:8px;color:rgba(255,255,255,.2);margin-top:8px">
      Base legal: COPFP Art. 113 · Metodología TGI D3 · Gold Master v5.5_TGI · Corte Q1-2026
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Vista Ejecutiva Bloomberg-style.
    Llamado desde env_gov.py cuando el rol activo es 'ejecutivo'.
    No renderiza header GOV — tiene su propio header institucional.
    """
    data = _load()

    _header(data)

    # ── Fila 1: Pulso Global │ Lo Urgente ────────────────────────────────────
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        _zona1_pulso(data)
    with c2:
        _zona2_urgente(data)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Fila 2: Compromisos │ Territorio ─────────────────────────────────────
    c3, c4 = st.columns(2, gap="medium")
    with c3:
        _zona3_compromisos(data)
    with c4:
        _zona4_territorio(data)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Fila 3: Oportunidades + QUIRA IA (ancho completo) ────────────────────
    _zona5_oportunidades(data)

    st.markdown("""
<div style="margin-top:14px;font-size:8px;color:rgba(255,255,255,.12);text-align:right">
  QUIRA Intelligence · Gold Master v5.5_TGI · Corte Q1-2026 · Dylus Lab © 2026
</div>
""", unsafe_allow_html=True)
