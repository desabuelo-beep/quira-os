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
# 13 DOMINIOS — CONCEPTO (campo-4 ADN) + número duro + PREGUNTA (campo-6 ADN)
# ══════════════════════════════════════════════════════════════════════════════
_DOMAINS_V2: list[dict[str, Any]] = [
    {
        "id": "d01", "num": "01", "nombre": "Planificación Estratégica",
        "concepto": "Instrumento rector que verifica la consistencia entre la planificación "
                    "territorial, la programación operativa, la asignación presupuestaria y la "
                    "ejecución pública.",
        "estado": "EN RUTA", "metric": "96%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicios 2025 y 2026",
        "radiografia_macro": [("METAS", "25"), ("COBERTURA", "96%"), ("ALINEACIÓN PND", "83%")],
        "gancho": "¿El cantón mantiene el rumbo hacia sus metas plurianuales, o se desvió en el camino?",
        "temp": "verde", "mod": "ods",
    },
    {
        "id": "d02", "num": "02", "nombre": "Presupuesto & Financiamiento",
        "concepto": "La capacidad del cantón de captar, mover y ejecutar recursos a "
                    "tiempo — y de apalancar capital externo sin caer en subejecución.",
        "estado": "CONDICIONADO", "metric": "58%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicio 2026 · corte Abril",
        "radiografia_macro": [("CAPTADO", "$1.87M"), ("EJECUCIÓN", "6.4%"), ("SALUD PRESUP.", "58%")],
        "gancho": "¿Con qué eficiencia y oportunidad se ejecutan los recursos frente al riesgo de subejecución?",
        "temp": "funds", "mod": "cooperacion",
    },
    {
        "id": "d03", "num": "03", "nombre": "Gobernanza del Mandato Electoral",
        "concepto": "La correspondencia entre lo que se prometió en campaña y lo que "
                    "el plan de gobierno realmente ejecuta — la palabra empeñada, medida.",
        "estado": "EN RUTA", "metric": "79.3%",
        "folio_estado": "EN LÍNEA", "periodo": "Período 2023 – 2027",
        "radiografia_macro": [("PROMESAS", "76"), ("VINCULADAS", "75"), ("FIDELIDAD", "79.3%")],
        "gancho": "¿La gestión mantiene la correspondencia con los compromisos que la ciudadanía validó en las urnas?",
        "temp": "alerta", "mod": "metas",
    },
    {
        "id": "d04", "num": "04", "nombre": "Alertas Institucionales",
        "concepto": "La vigilancia preventiva del cantón: las desviaciones y riesgos "
                    "detectados antes de que se vuelvan crisis.",
        "metric_key": "n_alertas", "metric_suffix": " activas",
        "gancho": "¿Qué riesgos están activos hoy y cuáles exigen intervención antes de volverse crisis?",
        "temp": "critico", "mod": "alertas", "dynamic_d04": True,
    },
    {
        "id": "d05", "num": "05", "nombre": "Holding e Integración Municipal",
        "concepto": "El desempeño coordinado de las entidades adscritas del municipio "
                    "(empresas públicas, Bomberos, Patronato) — quién articula y quién "
                    "arrastra al conjunto.",
        "estado": "BAJO OBJETIVO", "metric_key": "hold_avg", "metric_suffix": "%",
        "gancho": "¿Las entidades operan articuladas, o hay piezas que arrastran al conjunto?",
        "temp": "alerta", "mod": "municipal",
    },
    {
        "id": "d06", "num": "06", "nombre": "Salud Institucional",
        "concepto": "El estado de fondo del aparato público: su capacidad de sostener "
                    "el cumplimiento de sus funciones en el tiempo, no solo cumplir hoy.",
        "estado": "BAJO UMBRAL", "metric_key": "icpi_pct", "metric_suffix": "%",
        "gancho": "¿El gobierno cumple sus funciones de forma sostenible, o hay un deterioro estructural?",
        "temp": "critico", "mod": "situacion",
    },
    {
        "id": "d07", "num": "07", "nombre": "Transparencia",
        "concepto": "La relación entre la obligación legal de publicar y la capacidad "
                    "real de sostener una gestión auditable por la ciudadanía.",
        "estado": "OBSERVADO", "metric": "21/21",
        "gancho": "¿La información pública es verificable, o hay opacidad que impide auditar la gestión?",
        "temp": "normal", "mod": "transparencia",
    },
    {
        "id": "d08", "num": "08", "nombre": "Participación Ciudadana",
        "concepto": "La incidencia real de la ciudadanía en las decisiones públicas — "
                    "no cuántos talleres hubo, sino cuánto cambiaron lo que se decidió.",
        "estado": "BAJO OBJETIVO", "metric_key": "igp_pct", "metric_suffix": "%",
        "gancho": "¿La ciudadanía incide de verdad en las decisiones, o la participación es solo formal?",
        "temp": "alerta", "mod": "confianza",
    },
    {
        "id": "d09", "num": "09", "nombre": "Rendición de Cuentas",
        "concepto": "Espacio de fiscalización y control social que contrasta la asignación de "
                    "recursos aprobada contra la ejecución real devengada en territorio, "
                    "garantizando el cumplimiento normativo de la rendición.",
        "estado": "CONSOLIDADO", "metric": "72.7%",
        "folio_estado": "EN LÍNEA", "periodo": "Ejercicios 2023 - 2025",
        "radiografia_macro": [("VERIFICABLE", "55%"), ("SIN RESPALDO", "16%"), ("EFICACIA", "72.7%")],
        "gancho": "¿Qué parte del discurso se comprueba con registros independientes y qué queda sin respaldo público?",
        "temp": "normal", "mod": "rdc",
    },
    {
        "id": "d10", "num": "10", "nombre": "Cobertura de Servicios e Infraestructura",
        "concepto": "El acceso real a los servicios básicos visto desde el territorio: "
                    "dónde llegan las redes y dónde está el déficit estructural.",
        "estado": "BRECHA CRÍTICA", "metric": "34.9%",
        "gancho": "¿Dónde está el déficit real de servicios y a quién golpea la brecha urbano-rural?",
        "temp": "critico", "mod": "territorio",
    },
    {
        "id": "d11", "num": "11", "nombre": "Desarrollo Económico Territorial",
        "concepto": "La vitalidad económica del territorio: su capacidad de sostener "
                    "producción, empleo y cadenas de valor.",
        "estado": "EN CONSTRUCCIÓN", "metric": "—",
        "gancho": "Módulo en estructuración — empleo, industria y turismo.",
        "temp": "dim", "mod": None, "disabled": True,
    },
    {
        "id": "d12", "num": "12", "nombre": "Inclusión, Equidad y Género",
        "concepto": "La capacidad del municipio de cerrar las brechas de los grupos de "
                    "atención prioritaria, sobre todo donde la vulnerabilidad se "
                    "concentra en el territorio.",
        "estado": "CRÍTICO", "metric_key": "psg_pct", "metric_suffix": "%",
        "gancho": "¿El presupuesto de equidad es real, y dónde se concentra la brecha territorial?",
        "temp": "critico", "mod": "genero",
    },
    {
        "id": "d13", "num": "13", "nombre": "Sostenibilidad y Resiliencia Ambiental",
        "concepto": "La integridad ecológica del territorio: el equilibrio entre las "
                    "presiones sobre el ambiente y la capacidad del municipio de "
                    "conservar sus recursos y adaptarse al riesgo climático.",
        "estado": "EN CONSTRUCCIÓN", "metric": "—",
        "gancho": "¿Qué tan efectiva es la gestión pública para mitigar la "
                  "vulnerabilidad ambiental y conservar los recursos vitales del territorio?",
        "temp": "dim", "mod": None, "disabled": True,
    },
]

# Solo los DOM CURADOS son entrables; el resto queda BLOQUEADO (Javo 2026-07-14).
# d03 REABIERTO (2026-07-16): el canon fue curado y promovido — 76 promesas reales del Plan
# CNE, cero contaminación (antes: 66 con 3 de otros cantones). Las vinculaciones están
# validadas por Javo y corroboradas contra las 25 metas del universo operacional (ADR-036).
_ENTRABLES = {"d01", "d02", "d03", "d09"}
for _dm in _DOMAINS_V2:
    _dm["disabled"] = _dm["id"] not in _ENTRABLES

# Las 4 DIMENSIONES del sistema (lentes · NO contenido · NUNCA duplican los 13).
# Ciclo: ¿Qué? (Gobierno) · ¿Dónde? (Territorio) · ¿Por qué? (Inteligencia) · ¿Con quién? (Convergencia).
# La ACCIÓN (¿y ahora qué?) la cierra el GOBIERNO, FUERA de QUIRA: QUIRA informa y
# conecta, no actúa (frontera · Javo 2026-06-21). El 4to = match entre QUIRAs.
# Frame universal a las 6 QUIRAs; el contenido es propio de cada una.
_DIMS = [
    {"key": "dim_gob",    "icon": "🏛", "nombre": "Gobierno",
     "desc": "¿Qué? · la institución y sus 13 investigaciones", "dest": None, "activo": True},
    {"key": "dim_terr",   "icon": "🗺", "nombre": "Territorio",
     "desc": "¿Dónde? · el cantón en el mapa", "dest": "geotwin"},
    {"key": "dim_intel",  "icon": "◎", "nombre": "Inteligencia",
     "desc": "¿Por qué? · QUIRA lee y anticipa", "dest": "control"},
    {"key": "dim_conv", "icon": "🔗", "nombre": "Convergencia",
     "desc": "¿Con quién? · el encuentro entre las QUIRAs", "dest": None, "proximamente": True},
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
    hold = d.get("hold_avg", 0.0)
    d["icpi_str"]    = f"{icpi:.1f}%" if icpi is not None else "—"
    _parcial = any(t in str(d.get("icpi_clasif", "")).lower() for t in ("parcial", "preliminar"))
    d["icpi_color"]  = "#F59E0B" if _parcial else (C.sem(icpi) if icpi is not None else "#EF4444")
    d["icpi_sub"]    = d.get('icpi_clasif', '—')
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
            f'border-left:3px solid {t["c"]}!important; border-radius:12px!important; '
            f'min-height:220px!important; transition:border-color .12s ease; {op} }}'
        )
        if True:  # ícono-entrada estilizado para las 13 (todas son investigaciones)
            # ÍCONO-entrada (Javo · 2026-06-21): el ícono alusivo ES el disparador
            # nativo de entrada — reemplaza la numeración y el botón-caja. Robusto
            # (no overlay, no enlace). Hover = el cajón se ilumina e invita a entrar.
            per_card.append(
                f'.st-key-card_{dom["id"]}:hover > div[data-testid="stVerticalBlockBorderWrapper"] '
                f'{{ border-color:{t["c"]}!important; }}'
                f'.st-key-nav_{dom["id"]} button {{ background:{t["c"]}1c!important; '
                f'border:1px solid {t["c"]}45!important; border-radius:9px!important; '
                f'font-size:17px!important; line-height:1!important; padding:0!important; '
                f'min-height:38px!important; height:38px!important; width:100%!important; '
                f'box-shadow:none!important; }}'
                f'.st-key-nav_{dom["id"]} button:hover {{ background:{t["c"]}33!important; '
                f'border-color:{t["c"]}!important; transform:translateY(-1px); }}'
            )
    for k in _DIMS:
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
            '<div style="font-size:14px;font-weight:800;color:#E8EDF4">Centro de Inteligencia Territorial</div>'
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

    # ── Banda de 4 DIMENSIONES (lentes del sistema · no duplican los 13) ──────
    dcols = st.columns(4, gap="small")
    for col, dim in zip(dcols, _DIMS):
        with col:
            with st.container(border=True, key=dim["key"]):
                st.markdown(
                    f'<div style="padding:4px 6px 2px">'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="font-size:18px">{dim["icon"]}</span>'
                    f'<span style="font-size:15px;font-weight:800;color:#E8EDF4">'
                    f'{dim["nombre"]}</span></div>'
                    f'<div style="font-size:10px;color:#8892B0;margin-top:4px;'
                    f'line-height:1.35">{dim["desc"]}</div></div>',
                    unsafe_allow_html=True,
                )
                if dim.get("activo"):
                    st.markdown(
                        '<div style="font-size:9.5px;color:#22C55E;text-align:center;'
                        'padding:4px 0 2px;font-weight:700">● estás aquí</div>',
                        unsafe_allow_html=True,
                    )
                elif dim.get("proximamente"):
                    st.markdown(
                        '<div style="font-size:9.5px;color:#5A6B7E;text-align:center;'
                        'padding:4px 0 2px">— próximamente —</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    if st.button("entrar →", key=f"go_{dim['key']}", use_container_width=True):
                        _nav(dim["dest"])

    st.markdown(
        '<div style="display:flex;justify-content:space-between;margin:4px 2px 0">'
        '<span style="font-size:10.5px;font-weight:800;letter-spacing:.1em;'
        'color:#00D4FF">▎ÁREAS DE GESTIÓN</span>'
        '<span style="font-size:9.5px;color:#5A6B7E;font-family:\'JetBrains Mono\','
        'monospace">Montecristi · clic en el ícono para entrar</span></div>',
        unsafe_allow_html=True,
    )

    # ── Grid · 13 cajones · dimensiones iguales · ÍCONO = entrada ─────────────
    n_alertas = int(d.get("n_alertas", 0) or 0)
    # Ícono alusivo por cajón (reemplaza la numeración · ningún cajón manda sobre otro)
    _ICON = {
        "d01": "🧭", "d02": "💰", "d03": "📜", "d04": "🚨", "d05": "🏢",
        "d06": "🩺", "d07": "🔍", "d08": "🗳", "d09": "📣", "d10": "🗺",
        "d11": "📈", "d12": "🤝", "d13": "🌿",
    }
    # Color propio por dominio (Javo 2026-07-14 · diferenciación visual por colores)
    _DOM_COL = {
        "d01": "#22D3EE", "d02": "#A78BFA", "d03": "#F9AB00", "d04": "#EF5350",
        "d05": "#26A69A", "d06": "#EC407A", "d07": "#42A5F5", "d08": "#66BB6A",
        "d09": "#FFA726", "d10": "#8D6E63", "d11": "#FFEE58", "d12": "#AB47BC",
        "d13": "#9CCC65",
    }
    for fila in range(0, len(_DOMAINS_V2), 3):
        cols = st.columns(3, gap="small")
        for col, dom in zip(cols, _DOMAINS_V2[fila:fila + 3]):
            with col:
                with st.container(border=True, key=f"card_{dom['id']}"):
                    t = _TEMP[dom["temp"]]
                    color = _DOM_COL.get(dom["id"], "#5AA9E6")
                    # d04 dinámico: verde sin alertas
                    estado = dom.get("estado", "")
                    if dom.get("dynamic_d04"):
                        estado = "SIN ALERTAS" if n_alertas == 0 else f"{n_alertas} ACTIVAS"
                        t = _TEMP["verde"] if n_alertas == 0 else _TEMP["critico"]
                    metric = _metric_of(dom, d)
                    icono = _ICON.get(dom["id"], "◉")
                    # título: ÍCONO-entrada (disparador) + nombre
                    ic, nm = st.columns([0.17, 0.83], gap="small")
                    with ic:
                        # Las 13 abren su investigación sobre el kernel (qinv · UMI)
                        if dom.get("disabled"):
                            st.markdown('<div style="font-size:18px;text-align:center;opacity:.4;'
                                        'padding-top:6px" title="En preparación">🔒</div>',
                                        unsafe_allow_html=True)
                        elif st.button(icono, key=f"nav_{dom['id']}",
                                       help=f"Entrar · {dom['nombre']}"):
                            _nav(f"qinv_{dom['id']}")
                    with nm:
                        st.markdown(
                            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:7.5px;'
                            f'font-weight:800;letter-spacing:.14em;color:{color};padding-top:6px">DOMINIO</div>'
                            f'<div style="font-size:13px;font-weight:800;color:#E8EDF4;'
                            f'line-height:1.15;margin-top:1px">{dom["nombre"]}</div>',
                            unsafe_allow_html=True,
                        )
                    # cuerpo: concepto (izq) | métrica + estado (der)
                    # cuerpo tipo FOLIO / MEMORANDO — documento sellado (Javo 2026-07-14): alcance + estado
                    # + radiografía de 3 indicadores macro. El detalle se descubre AL ENTRAR (no es un índice).
                    rm = dom.get("radiografia_macro", [])
                    est = dom.get("folio_estado", "")
                    per = dom.get("periodo", "")
                    mono = "font-family:'JetBrains Mono',monospace"
                    box = ""
                    if rm:
                        sep = f'<span style="color:{color};opacity:.55;margin:0 6px">→</span>'
                        cells = sep.join(
                            f'<span style="white-space:nowrap"><span style="font-size:7.5px;font-weight:800;'
                            f'letter-spacing:.05em;color:#7E8BA3">{lab}</span> '
                            f'<span style="{mono};font-size:13px;font-weight:900;color:{color}">{val}</span></span>'
                            for lab, val in rm)
                        box = (f'<div style="{mono};font-size:7.5px;font-weight:800;letter-spacing:.1em;'
                               f'text-transform:uppercase;color:#7E8BA3;margin-top:11px;margin-bottom:5px">'
                               f'Radiografía documental · métricas de consistencia</div>'
                               f'<div style="border:1px solid {color}45;border-radius:6px;padding:9px 8px;'
                               f'text-align:center;background:{color}0d">{cells}</div>')
                    estado_html = ""
                    if est or per:
                        _p = f' · {per}' if per else ""
                        estado_html = (f'<div style="{mono};font-size:8.5px;color:#8494A8;margin-top:10px;'
                                       f'letter-spacing:.02em"><span style="color:{color};font-weight:800">'
                                       f'ESTADO:</span> <b style="color:#C4D0E0">{est}</b>{_p}</div>')
                    # Rejilla de 3 filas fijas (Javo · 2026-07-16): el ALCANCE fluía libre y su
                    # largo variable empujaba ESTADO y RADIOGRAFÍA a alturas distintas en cada
                    # tarjeta. Con alto fijo en el alcance y la radiografía anclada al fondo,
                    # las tres franjas caen SIEMPRE en la misma línea, sea cual sea el texto.
                    st.markdown(
                        f'<div style="padding:2px 2px 0;display:flex;flex-direction:column;'
                        f'min-height:196px">'
                        f'<div style="height:3px;background:{color};border-radius:2px;opacity:.7;margin-bottom:10px"></div>'
                        f'<div style="{mono};font-size:8px;font-weight:800;letter-spacing:.08em;color:{color};'
                        f'margin-bottom:3px">[ ALCANCE ]</div>'
                        f'<div style="font-size:11px;color:#A8B4C8;line-height:1.5;height:66px;'
                        f'overflow:hidden">{dom["concepto"]}</div>'
                        f'<div style="margin-top:auto">{estado_html}{box}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    if dom.get("disabled"):
                        st.markdown(
                            '<div style="font-size:9.5px;color:#5A6B7E;text-align:center;'
                            'padding:2px 0">— en construcción —</div>',
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
