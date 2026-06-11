"""
QUIRA Intelligence — Centro de Mando v2 NATIVO  (Sprint C · 2026-06-11)
Teatro Operacional · GAD Montecristi · Holding Municipal

POR QUÉ v2 (lección registrada en BOOT):
  El v1 renderizaba los cajones dentro de components.html (iframe) y
  navegaba con un puente postMessage → click de botones ocultos del parent.
  En Streamlit Cloud el iframe corre SANDBOX cross-origin: el puente jamás
  puede tocar la ventana principal → los cajones NUNCA navegaron en deploy.
  v2 = TODO nativo: st.container + st.button reales. Cero iframes para
  navegación. Lo que se ve es el DOM de Streamlit — no puede fallar.

SPECS DE CONTENIDO (Javo · 2026-06-11):
  Cada cajón = (a) CONCEPTO: qué ES este dominio en lenguaje humano,
  (b) número duro representativo, (c) GANCHO que invita a entrar.
  "Su info no me dice nada, es solo un número frío" → resuelto aquí.

Navegación: st.session_state["gov_module"] = mod → env_gov rutea.
Dylus Lab © 2026
"""
from __future__ import annotations

from typing import Any

import streamlit as st

from utils.session import get_rol, logout

UI_VERSION = "UI v2.0-nativo · 2026-06-11"

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE TEMPERATURA (idéntica doctrina v1)
# ══════════════════════════════════════════════════════════════════════════════
_TEMP: dict[str, dict[str, str]] = {
    "critico": {"bg": "rgba(239,68,68,.10)",  "bd": "rgba(239,68,68,.45)",  "c": "#EF4444"},
    "alerta":  {"bg": "rgba(249,115,22,.09)", "bd": "rgba(249,115,22,.40)", "c": "#F97316"},
    "normal":  {"bg": "rgba(0,212,255,.05)",  "bd": "rgba(0,212,255,.25)",  "c": "#00D4FF"},
    "verde":   {"bg": "rgba(34,197,94,.07)",  "bd": "rgba(34,197,94,.32)",  "c": "#22C55E"},
    "funds":   {"bg": "rgba(124,92,252,.10)", "bd": "rgba(124,92,252,.42)", "c": "#7C5CFC"},
    "dim":     {"bg": "rgba(255,255,255,.02)","bd": "rgba(255,255,255,.08)","c": "#5A6B7E"},
}

# ══════════════════════════════════════════════════════════════════════════════
# 12 DOMINIOS — CONCEPTO (qué es) + número duro + GANCHO (por qué entrar)
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS_V2: list[dict[str, Any]] = [
    {
        "id": "d01", "num": "01", "nombre": "Planificación Estratégica",
        "concepto": "El plan de desarrollo del cantón: los compromisos que "
                    "Montecristi se fijó hasta 2027 y su grado de ejecución real.",
        "estado": "EN RUTA", "metric": "56/56",
        "gancho": "¿Qué prometió el cantón y cuánto se cumple? Los 4 ejes, meta por meta.",
        "temp": "verde", "mod": "ods",
    },
    {
        "id": "d02", "num": "02", "nombre": "Presupuesto & Financiamiento",
        "concepto": "El dinero del cantón: de dónde viene, en qué se invierte y "
                    "qué fondos internacionales están en juego.",
        "estado": "CONDICIONADO", "metric": "$3.66M",
        "gancho": "Tres fondos activos dependen de hitos de este trimestre — cuáles y qué los condiciona.",
        "temp": "funds", "mod": "cooperacion",
    },
    {
        "id": "d03", "num": "03", "nombre": "Metas PDOT · Mandato",
        "concepto": "La palabra empeñada: las promesas registradas ante el CNE "
                    "convertidas (o no) en metas formales del plan.",
        "estado": "EN RUTA", "metric": "94.6%",
        "gancho": "53 de 56 metas en cronograma — y 3 en rezago. Mira cuáles son.",
        "temp": "alerta", "mod": "metas",
    },
    {
        "id": "d04", "num": "04", "nombre": "Alertas Institucionales",
        "concepto": "El sistema de alerta temprana: señales que anticipan riesgos "
                    "institucionales antes de que se vuelvan crisis.",
        "metric_key": "n_alertas", "metric_suffix": " activas",
        "gancho": "7 tipos de señal bajo monitoreo continuo — el semáforo del cantón.",
        "temp": "critico", "mod": "alertas", "dynamic_d04": True,
    },
    {
        "id": "d05", "num": "05", "nombre": "Holding Municipal",
        "concepto": "Las 4 entidades del holding (GAD, EP Aseo, Bomberos, "
                    "Patronato) medidas con la misma vara.",
        "estado": "BAJO OBJETIVO", "metric_key": "hold_avg", "metric_suffix": "%",
        "gancho": "EP Aseo lidera con 82% y el GAD está en rezago — compara las cuatro.",
        "temp": "alerta", "mod": "municipal",
    },
    {
        "id": "d06", "num": "06", "nombre": "Salud Institucional",
        "concepto": "El estado general del municipio como institución: 41 métricas "
                    "integradas en un solo diagnóstico.",
        "estado": "BAJO UMBRAL", "metric_key": "icpi_pct", "metric_suffix": "%",
        "gancho": "11.4 puntos bajo el umbral — entra a ver dónde se concentra la brecha.",
        "temp": "critico", "mod": "situacion",
    },
    {
        "id": "d07", "num": "07", "nombre": "Transparencia",
        "concepto": "La información que la ley obliga a publicar (LOTAIP) y su "
                    "estado real de publicación y verificación.",
        "estado": "OBSERVADO", "metric": "21/21",
        "gancho": "21 de 21 artículos publicados, sin sanciones — verifica la evidencia.",
        "temp": "normal", "mod": "transparencia",
    },
    {
        "id": "d08", "num": "08", "nombre": "Participación Ciudadana",
        "concepto": "Los mecanismos por los que la ciudadanía decide: presupuesto "
                    "participativo, cabildos, consultas, veedurías.",
        "estado": "BAJO OBJETIVO", "metric": "27.98%",
        "gancho": "6 mecanismos activos pero la participación no llega al objetivo de 40% — ¿por qué?",
        "temp": "alerta", "mod": "confianza",
    },
    {
        "id": "d09", "num": "09", "nombre": "Rendición de Cuentas",
        "concepto": "El examen anual del municipio ante el CPCCS y la ciudadanía: "
                    "el circuito que valida (o bloquea) la gestión del año.",
        "estado": "EN PREPARACIÓN", "metric_key": "dias_rdc", "metric_suffix": " días",
        "gancho": "Cuenta regresiva a la presentación de agosto — el circuito tiene condiciones en rojo.",
        "temp": "alerta", "mod": "rdc",
    },
    {
        "id": "d10", "num": "10", "nombre": "Territorio & Cobertura",
        "concepto": "Los servicios básicos vistos desde el territorio: quién tiene "
                    "agua, saneamiento y recolección — y quién no.",
        "estado": "BRECHA CRÍTICA", "metric": "34.9%",
        "gancho": "Una parroquia concentra todas las brechas. El mapa lo explica en 30 segundos.",
        "temp": "critico", "mod": "territorio",
    },
    {
        "id": "d11", "num": "11", "nombre": "Ecosistema Productivo Territorial",
        "concepto": "La economía del territorio: empleo, industria, turismo y la "
                    "zona especial de desarrollo.",
        "estado": "EN CONSTRUCCIÓN", "metric": "—",
        "gancho": "Módulo en estructuración — empleo, industria y turismo.",
        "temp": "dim", "mod": None, "disabled": True,
    },
    {
        "id": "d12", "num": "12", "nombre": "Protección Social & Grupos Prioritarios",
        "concepto": "Los grupos que la Constitución manda atender primero: "
                    "inversión social, género y prioridad territorial.",
        "estado": "CRÍTICO", "metric": "12.83%",
        "gancho": "La inversión social está 17.2 puntos bajo el mandato constitucional — $2.1M de brecha.",
        "temp": "critico", "mod": "genero",
    },
]

_KPIS = [
    {"key": "kpi_situacion",   "label": "CUMPLIMIENTO INSTITUCIONAL", "dest": "situacion",
     "val_key": "icpi_str",    "color_key": "icpi_color", "sub_key": "icpi_sub"},
    {"key": "kpi_cooperacion", "label": "FONDOS EN RIESGO", "dest": "cooperacion",
     "val": "$3.66M", "color": "#7C5CFC", "sub": "BID · CAF · PNUD · desembolso condicionado"},
    {"key": "kpi_alertas",     "label": "ALERTAS ACTIVAS", "dest": "alertas",
     "val_key": "alert_str", "color_key": "alert_color", "sub_key": "riesgo_str"},
    {"key": "kpi_municipal",   "label": "HOLDING MUNICIPAL", "dest": "municipal",
     "val_key": "hold_str", "color_key": "hold_color", "sub": "Promedio 4 entidades · EP Aseo líder"},
]


# ══════════════════════════════════════════════════════════════════════════════
# DATOS — reusa la carga del v1 (misma fuente, misma doctrina)
# ══════════════════════════════════════════════════════════════════════════════

def _data() -> dict[str, Any]:
    from quira_pages.p_command_center import _load_data
    d = _load_data()
    from utils.css_tokens import C
    icpi = d.get("icpi_pct")
    n_al = int(d.get("n_alertas", 0) or 0)
    hold = d.get("hold_avg", 68.7)
    d["icpi_str"]    = f"{icpi:.1f}%" if icpi is not None else "—"
    d["icpi_color"]  = C.sem(icpi) if icpi is not None else "#EF4444"
    d["icpi_sub"]    = f"{d.get('icpi_clasif', '—')} · umbral 65%"
    d["alert_str"]   = str(n_al)
    d["alert_color"] = "#EF4444" if n_al > 0 else "#22C55E"
    d["riesgo_str"]  = (d.get("riesgo_clasif") or "Sin alertas críticas")
    if d["riesgo_str"] in ("—", ""):
        d["riesgo_str"] = "Sin alertas críticas"
    d["hold_str"]    = f"{hold:.1f}%"
    d["hold_color"]  = C.sem(hold)
    return d


def _metric_of(dom: dict, d: dict) -> str:
    k = dom.get("metric_key")
    if k:
        v = d.get(k)
        if v is not None:
            suf = dom.get("metric_suffix", "")
            return f"{v:.1f}{suf}" if isinstance(v, float) else f"{v}{suf}"
    return dom.get("metric", "—")


def _nav(mod: str) -> None:
    st.session_state["gov_module"] = mod
    st.session_state["ejecutivo_modo"] = "vista"
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# CSS GLOBAL — estética sobre componentes NATIVOS (st-key-* targeting)
# ══════════════════════════════════════════════════════════════════════════════

def _css() -> str:
    per_card = []
    for dom in _DOMAINS_V2:
        t = _TEMP[dom["temp"]]
        op = "opacity:.45;" if dom.get("disabled") else ""
        per_card.append(
            f'.st-key-card_{dom["id"]} > div[data-testid="stVerticalBlockBorderWrapper"] '
            f'{{ background:{t["bg"]}!important; border:1px solid {t["bd"]}!important; '
            f'border-left:3px solid {t["c"]}!important; border-radius:12px!important; {op} }}'
        )
        per_card.append(
            f'.st-key-nav_{dom["id"]} button {{ background:transparent!important; '
            f'border:1px solid {t["bd"]}!important; color:{t["c"]}!important; '
            f'font-size:11px!important; font-weight:700!important; '
            f'border-radius:8px!important; padding:2px 10px!important; min-height:30px!important; }}'
            f'.st-key-nav_{dom["id"]} button:hover {{ background:{t["c"]}22!important; '
            f'border-color:{t["c"]}!important; }}'
        )
    for k in _KPIS:
        per_card.append(
            f'.st-key-{k["key"]} > div[data-testid="stVerticalBlockBorderWrapper"] '
            f'{{ background:rgba(255,255,255,.015)!important; '
            f'border:1px solid rgba(255,255,255,.07)!important; '
            f'border-radius:12px!important; }}'
            f'.st-key-go_{k["key"]} button {{ background:transparent!important; '
            f'border:none!important; color:#8892B0!important; font-size:11px!important; '
            f'min-height:26px!important; padding:0 6px!important; }}'
            f'.st-key-go_{k["key"]} button:hover {{ color:#E8EDF4!important; }}'
        )
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* Sidebar fuera + main full-width + fondo */
[data-testid="stSidebar"], [data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {{
  display:none!important; width:0!important; min-width:0!important;
}}
.stApp {{ background:#080D18!important; }}
.main .block-container, [data-testid="stMainBlockContainer"], div.block-container {{
  max-width:100%!important; padding:0.6rem 1.1rem 0.8rem!important;
}}
html, body, .stApp, .stApp * {{ font-family:'Inter',system-ui,sans-serif; }}

/* Header buttons */
.st-key-btn_quira_ia button {{
  background:rgba(0,212,255,.08)!important; border:1px solid rgba(0,212,255,.4)!important;
  color:#00D4FF!important; font-weight:700!important; font-size:12px!important;
  border-radius:9px!important;
}}
.st-key-btn_quira_ia button:hover {{ background:rgba(0,212,255,.18)!important; }}
.st-key-btn_salir button {{
  background:transparent!important; border:1px solid rgba(255,255,255,.14)!important;
  color:#8892B0!important; font-size:12px!important; border-radius:9px!important;
}}
.st-key-btn_salir button:hover {{ color:#E8EDF4!important; border-color:rgba(255,255,255,.3)!important; }}

/* Compactar gaps verticales */
div[data-testid="stVerticalBlock"] {{ gap:.45rem!important; }}

{''.join(per_card)}
</style>"""


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Centro de Mando v2 — nativo, sin iframes de navegación."""
    st.markdown(_css(), unsafe_allow_html=True)
    d = _data()
    rol = get_rol() or "ejecutivo"

    # ── Header ────────────────────────────────────────────────────────────────
    h1, h2, h3, h4 = st.columns([5.2, 1.1, 1.5, 0.9])
    with h1:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:14px">'
            '<span style="font-size:21px;font-weight:900;color:#00D4FF;'
            'letter-spacing:.04em">⬡ QUIRA</span>'
            '<div style="border-left:1px solid rgba(255,255,255,.12);padding-left:14px">'
            '<div style="font-size:15px;font-weight:800;color:#E8EDF4">Centro de Mando</div>'
            '<div style="font-size:10.5px;color:#8892B0">GAD Municipal de Montecristi · '
            'Corte Q1-2026</div></div></div>',
            unsafe_allow_html=True,
        )
    with h2:
        st.markdown(
            f'<div style="text-align:right;padding-top:8px">'
            f'<span style="font-size:10px;font-weight:700;color:#22C55E;'
            f'border:1px solid rgba(34,197,94,.35);border-radius:12px;'
            f'padding:3px 10px">● EN LÍNEA</span> '
            f'<span style="font-size:10px;font-weight:700;color:#00D4FF;'
            f'border:1px solid rgba(0,212,255,.35);border-radius:12px;'
            f'padding:3px 10px;text-transform:capitalize">{rol}</span></div>',
            unsafe_allow_html=True,
        )
    with h3:
        if st.button("◎ Preguntar a QUIRA", key="btn_quira_ia", use_container_width=True):
            _nav("control")
    with h4:
        if st.button("⎋ Salir", key="btn_salir", use_container_width=True):
            logout()
            st.rerun()

    # ── KPI band (4 tiles clicables) ─────────────────────────────────────────
    kcols = st.columns(4, gap="small")
    for col, k in zip(kcols, _KPIS):
        with col:
            with st.container(border=True, key=k["key"]):
                val   = k.get("val")   or d.get(k.get("val_key", ""), "—")
                color = k.get("color") or d.get(k.get("color_key", ""), "#00D4FF")
                sub   = k.get("sub")   or d.get(k.get("sub_key", ""), "")
                st.markdown(
                    f'<div style="padding:2px 4px 0">'
                    f'<div style="font-size:9.5px;font-weight:700;letter-spacing:.08em;'
                    f'color:#8892B0">{k["label"]}</div>'
                    f'<div style="font-size:30px;font-weight:900;'
                    f"font-family:'JetBrains Mono',monospace;"
                    f'color:{color};line-height:1.15">{val}</div>'
                    f'<div style="font-size:10px;color:#8892B0">{sub}</div></div>',
                    unsafe_allow_html=True,
                )
                if st.button("abrir →", key=f"go_{k['key']}", use_container_width=True):
                    _nav(k["dest"])

    st.markdown(
        '<div style="display:flex;justify-content:space-between;margin:4px 2px 0">'
        '<span style="font-size:10.5px;font-weight:800;letter-spacing:.1em;'
        'color:#00D4FF">▎DOMINIOS OPERACIONALES</span>'
        '<span style="font-size:9.5px;color:#5A6B7E;font-family:\'JetBrains Mono\','
        'monospace">Holding Municipal · Montecristi · 12 dominios · clic en ABRIR</span></div>',
        unsafe_allow_html=True,
    )

    # ── Grid 4 × 3 — cards nativas ───────────────────────────────────────────
    n_alertas = int(d.get("n_alertas", 0) or 0)
    for fila in range(0, 12, 3):
        cols = st.columns(3, gap="small")
        for col, dom in zip(cols, _DOMAINS_V2[fila:fila + 3]):
            with col:
                with st.container(border=True, key=f"card_{dom['id']}"):
                    t = _TEMP[dom["temp"]]
                    # d04 dinámico: verde sin alertas
                    estado = dom.get("estado", "")
                    if dom.get("dynamic_d04"):
                        estado = "SIN ALERTAS" if n_alertas == 0 else f"{n_alertas} ACTIVAS"
                        t = _TEMP["verde"] if n_alertas == 0 else _TEMP["critico"]
                    metric = _metric_of(dom, d)
                    st.markdown(
                        f'<div style="padding:2px 4px 0">'
                        # fila título
                        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px">'
                        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;'
                        f'font-weight:700;color:{t["c"]};background:{t["c"]}1c;'
                        f'border:1px solid {t["c"]}38;border-radius:6px;padding:1px 7px">'
                        f'{dom["num"]}</span>'
                        f'<span style="font-size:13.5px;font-weight:800;color:#E8EDF4">'
                        f'{dom["nombre"]}</span></div>'
                        # CONCEPTO (spec Javo: qué ES el dominio)
                        f'<div style="font-size:11px;color:#A8B4C8;line-height:1.45;'
                        f'margin-bottom:7px">{dom["concepto"]}</div>'
                        # estado + número duro
                        f'<div style="display:flex;align-items:baseline;gap:10px;margin-bottom:6px">'
                        f'<span style="font-size:9px;font-weight:800;letter-spacing:.06em;'
                        f'color:{t["c"]};border:1px solid {t["c"]}45;border-radius:10px;'
                        f'padding:2px 9px">● {estado}</span>'
                        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:24px;'
                        f'font-weight:900;color:{t["c"]}">{metric}</span></div>'
                        # GANCHO (spec Javo: invitación a entrar)
                        f'<div style="font-size:10.5px;color:#7E8BA3;font-style:italic;'
                        f'line-height:1.4">{dom["gancho"]}</div></div>',
                        unsafe_allow_html=True,
                    )
                    if dom.get("mod") and not dom.get("disabled"):
                        if st.button("ABRIR →", key=f"nav_{dom['id']}",
                                     use_container_width=True):
                            _nav(dom["mod"])
                    else:
                        st.markdown(
                            '<div style="font-size:9.5px;color:#5A6B7E;text-align:center;'
                            'padding:4px 0 2px">— en construcción —</div>',
                            unsafe_allow_html=True,
                        )

    # ── Footer + stamp de versión ─────────────────────────────────────────────
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;margin-top:6px;'
        f'padding-top:8px;border-top:1px solid rgba(255,255,255,.06)">'
        f'<span style="font-size:9.5px;color:#5A6B7E">● Sistema operativo · '
        f'GAD Municipal de Montecristi · Corte Q1-2026</span>'
        f'<span style="font-size:9.5px;color:#5A6B7E">Dylus Lab © 2026 · '
        f'QUIRA Intelligence · <span style="font-family:\'JetBrains Mono\',monospace;'
        f'opacity:.75">{UI_VERSION}</span></span></div>',
        unsafe_allow_html=True,
    )
