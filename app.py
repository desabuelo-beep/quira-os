"""
QUIRA OS v0.1 — Entry Point
Sistema Integral de Gobernanza · GAD Municipal de Montecristi
Dylus Lab © 2026
"""
import streamlit as st
from config import APP_NAME, APP_VERSION, GAD_NOMBRE, GAD_PERIODO, ALCALDE, CORTE
from utils.session import init_session, check_session_expiry, is_authenticated, logout, navigate_to, is_tecnico
from utils.audit_log import log_page
from auth.login import render_login


# ── CONFIGURACIÓN STREAMLIT ────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} · {GAD_NOMBRE}",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── ESTILOS GLOBALES ───────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── RESET & BASE ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0A1628 !important;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #E2E8F0;
}

/* ── LAYOUT ANCHO TOTAL — Streamlit 1.35+ selectors ── */
/* Cubre tanto la clase legacy como los data-testid modernos */
.main .block-container,
[data-testid="stMainBlockContainer"],
div.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
}

/* Iframes de components.html() — sin borde, ancho total */
iframe {
    width: 100% !important;
    border: none !important;
    display: block !important;
}

/* Streamlit añade padding-top extra al primer bloque */
[data-testid="stAppViewBlockContainer"],
.appview-container .main section {
    padding-top: 0.5rem !important;
}

/* Eliminar gap entre secciones de st.container() */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0 !important;
}

/* Header */
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] p {
    color: rgba(255,255,255,0.65);
    font-size: 12px;
}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.07);
    gap: 4px;
    padding: 4px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: rgba(255,255,255,0.5);
    font-size: 12px;
    font-weight: 600;
    border-radius: 7px;
    padding: 6px 14px;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(0,212,255,0.12) !important;
    color: #00D4FF !important;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: rgba(0,212,255,0.1) !important;
    border-color: rgba(0,212,255,0.3) !important;
    color: #00D4FF !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 10px; }

/* ── HIDE Streamlit branding ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ── SCROLLBAR DUPLICADO — eliminado desde html_engine.py (scrolling=False) ── */
/* NO tocar overflow/height del root — rompe el scroll nativo en mobile */

/* ── Z-INDEX STACK — evita que el sidebar se monte sobre modales/tooltips ── */
[data-testid="stSidebar"] {
    z-index: 100 !important;
}
section.main, [data-testid="stMain"] {
    z-index: 10 !important;
}
/* Tooltips y popovers de Streamlit siempre encima */
[data-baseweb="popover"],
[data-baseweb="tooltip"],
[data-testid="stPopover"] {
    z-index: 99999 !important;
}

/* ── DESKTOP: sidebar siempre visible — neutraliza caché de collapsed ── */
@media (min-width: 769px) {
    [data-testid="stSidebar"] {
        transform: translateX(0) !important;
        min-width: 244px !important;
        width: 244px !important;
        display: flex !important;
        visibility: visible !important;
    }
}

/* ── QUICKNAV: forzar horizontal en pantallas pequeñas ── */
@media (max-width: 768px) {
    [data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: 0 !important;
        flex: 1 1 0% !important;
        overflow: hidden !important;
    }
    [data-testid="stHorizontalBlock"] .stButton > button {
        font-size: 9px !important;
        padding: 4px 2px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        min-height: 36px !important;
    }
}

/* ── MOBILE: sidebar colapsado por defecto, toggle visible ── */
@media (max-width: 768px) {
    /* Main sin padding extra cuando sidebar está oculto */
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    /* Botón de expandir/colapsar sidebar — siempre visible y con color cyan */
    [data-testid="collapsedControl"],
    button[data-testid="collapsedControl"] {
        position: fixed !important;
        top: 8px !important;
        left: 0 !important;
        background: rgba(0,212,255,0.22) !important;
        border: 1px solid rgba(0,212,255,0.4) !important;
        border-left: none !important;
        border-radius: 0 8px 8px 0 !important;
        color: #00D4FF !important;
        width: 28px !important;
        height: 44px !important;
        z-index: 99999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* Sidebar abierto: drawer flotante */
    [data-testid="stSidebar"][aria-expanded="true"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        height: 100dvh !important;
        width: 82vw !important;
        max-width: 310px !important;
        overflow-y: auto !important;
        z-index: 9998 !important;
        box-shadow: 6px 0 32px rgba(0,0,0,0.7) !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ── INIT SESSION + SEGURIDAD ──────────────────────────────────────────────────
init_session()
check_session_expiry()   # logout automático si la sesión expiró (60 min)

# ── GATE: LOGIN ────────────────────────────────────────────────────────────────
if not is_authenticated():
    render_login()
    st.stop()

# ── CARGA LAZY DE PÁGINAS ──────────────────────────────────────────────────────
from quira_pages.p1_dashboard    import render as p1
from quira_pages.p2_holding      import render as p2
from quira_pages.p3_congruencias import render as p3
from quira_pages.p4_geotwin      import render as p4
from quira_pages.p5_operacion    import render as p5
from quira_pages.p6_pulso        import render as p6
from quira_pages.p7_brecha       import render as p7
from quira_pages.p8_metas        import render as p8
from quira_pages.p9_sat          import render as p9
from quira_pages.p10_inversion   import render as p10
from quira_pages.p11_ods         import render as p11
from quira_pages.p12_cadena      import render as p12
from quira_pages.p13_simulador   import render as p13
from quira_pages.p14_eficiencia  import render as p14
from quira_pages.p15_transparencia import render as p15
from quira_pages.p16_gobernanza  import render as p16_gobernanza
from quira_pages.p18_cooperacion import render as p18
from quira_pages.p19_genero      import render as p19
from components.sentinel   import render_sentinel

def _p_sentinel():
    render_sentinel()

PAGES = {
    # ── EJECUTIVO ─────────────────────────────────────────────────────────────
    "dashboard":    {"label": "Tablero Ejecutivo",     "icon": "📊", "render": p1},
    "pulso":        {"label": "Pulso Ejecutivo",       "icon": "⚡", "render": p6},
    "brecha":       {"label": "Causas de la Brecha",   "icon": "📉", "render": p7},
    "simulador":    {"label": "Proyector ✨",            "icon": "🧮", "render": p13},
    # ── PLANIFICACIÓN ─────────────────────────────────────────────────────────
    "metas":        {"label": "Metas PDOT",            "icon": "🎯", "render": p8},
    "cadena":       {"label": "Cadena POA·PAC",        "icon": "🔗", "render": p12},
    "congruencias": {"label": "Congruencias HPT-M",    "icon": "🔗", "render": p3},
    # ── OPERATIVO ─────────────────────────────────────────────────────────────
    "sat":          {"label": "Alertas SAT",           "icon": "🚨", "render": p9},
    "eficiencia":   {"label": "Eficiencia Dirs.",      "icon": "📋", "render": p14},
    "operacion":    {"label": "Operación Técnica",     "icon": "⚙️", "render": p5},
    # ── TERRITORIAL ───────────────────────────────────────────────────────────
    "geotwin":      {"label": "GeoTwin · Territorio",  "icon": "🗺️", "render": p4},
    "inversion":    {"label": "Inversión per Cápita",  "icon": "💰", "render": p10},
    "holding":      {"label": "Holding Municipal",     "icon": "🏛️", "render": p2},
    # ── CIUDADANÍA ────────────────────────────────────────────────────────────
    "gobernanza":   {"label": "Gobernanza Participativa", "icon": "🗳️", "render": p16_gobernanza},
    "transparencia":{"label": "Transparencia LOTAIP",  "icon": "🔍", "render": p15},
    # ── ESTRATÉGICO ───────────────────────────────────────────────────────────
    "ods":          {"label": "ODS Tracker",           "icon": "🌐", "render": p11},
    "cooperacion":  {"label": "Cooperación Intern.",   "icon": "💸", "render": p18},
    "genero":       {"label": "Género y Ambiente",      "icon": "💜", "render": p19},
    # ── IA ────────────────────────────────────────────────────────────────────
    "sentinel":     {"label": "Sentinel · IA",         "icon": "🔮", "render": _p_sentinel},
}

# ── DOCTRINA QUIRA — AGRUPACIÓN POR ESTADO COGNITIVO ──────────────────────────
SECTIONS = [
    ("ENTENDER",  "Ver la verdad",          ["dashboard", "pulso", "brecha", "geotwin", "inversion"]),
    ("GOBERNAR",  "Corregir el sistema",    ["metas", "cadena", "congruencias", "sat", "eficiencia", "operacion", "holding", "ods", "cooperacion", "genero"]),
    ("SIMULAR",   "Proyectar escenarios",   ["simulador"]),
    ("CONFIAR",   "Defender decisiones",    ["gobernanza", "transparencia"]),
    ("APRENDER",  "El sistema mejora",      ["sentinel"]),
]

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / identidad
    rol        = st.session_state.get("rol", "")
    rol_emoji  = st.session_state.get("rol_emoji", "")
    usuario    = st.session_state.get("usuario", "")

    st.markdown(f"""
<div style="padding:16px 0 20px">
    <div style="font-size:1.4rem;font-weight:900;color:#00D4FF;letter-spacing:-0.03em;
                margin-bottom:2px">⬡ {APP_NAME}</div>
    <div style="font-size:0.65rem;color:rgba(255,255,255,0.35);letter-spacing:0.05em;
                text-transform:uppercase">{APP_VERSION} · Sistema de Gobernanza</div>
</div>
<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:10px;padding:10px 12px;margin-bottom:20px">
    <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:4px">SESIÓN ACTIVA</div>
    <div style="font-size:12px;font-weight:700;color:#E2E8F0">{rol_emoji} {rol}</div>
    <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px">{GAD_NOMBRE}</div>
</div>
    """, unsafe_allow_html=True)

    # Navegación — Doctrina QUIRA
    current_page = st.session_state.get("page", "dashboard")
    for section_id, section_label, page_keys in SECTIONS:
        st.markdown(f"""
<div style="font-size:9px;font-weight:700;color:rgba(0,212,255,0.55);
            letter-spacing:0.09em;text-transform:uppercase;
            padding:10px 2px 3px;border-top:1px solid rgba(255,255,255,0.05);
            margin-top:2px">{section_id} <span style="color:rgba(255,255,255,0.2);font-weight:400">· {section_label}</span></div>
        """, unsafe_allow_html=True)
        for key in page_keys:
            page = PAGES[key]
            disabled_note = " 🔒" if key == "operacion" and not is_tecnico() else ""
            sentinel_note = " ✨" if key == "sentinel" else ""
            if st.button(
                f"{page['icon']} {page['label']}{disabled_note}{sentinel_note}",
                key=f"nav_{key}",
                use_container_width=True,
            ):
                st.session_state["page"] = key
                st.rerun()

    st.markdown("---")

    # Info GAD
    st.markdown(f"""
<div style="font-size:9px;color:rgba(255,255,255,0.25);line-height:1.8">
    🏛️ {GAD_NOMBRE}<br>
    📅 Período {GAD_PERIODO}<br>
    👤 {ALCALDE}<br>
    📊 Corte {CORTE}<br>
    <br>
    <span style="color:rgba(255,180,0,0.5)">⚠ Entorno PMV · no producción</span>
</div>
    """, unsafe_allow_html=True)

    # Logout
    if st.button("← Cerrar Sesión", use_container_width=True):
        logout()
        st.rerun()

    # SAT badge rápido
    from data.loader import load_all, get_sat_counts
    try:
        _data = load_all()
        _sat  = get_sat_counts(_data)
        if _sat["criticos"] > 0:
            st.error(
                f"🔴 {_sat['criticos']} SAT Crítica{'s' if _sat['criticos']>1 else ''} "
                f"Activa{'s' if _sat['criticos']>1 else ''} · Ver Tablero"
            )
    except Exception:
        pass

# ── MAIN CONTENT ───────────────────────────────────────────────────────────────
page_key = st.session_state.get("page", "dashboard")
# Redirect legacy keys → merged screen
if page_key in ("confianza", "rdc"):
    page_key = "gobernanza"
    st.session_state["page"] = "gobernanza"
page_cfg  = PAGES.get(page_key, PAGES["dashboard"])

# ── Quick-nav bar — fallback cuando sidebar está colapsado (mobile-first) ──────
# 5 accesos directos siempre visibles: Tablero · Brecha · Proyector · SAT · Sentinel
_quicknav_pages = ["dashboard", "brecha", "geotwin", "simulador", "sentinel"]
with st.container():
    _qn_cols = st.columns(len(_quicknav_pages), gap="small")
    for _col, _k in zip(_qn_cols, _quicknav_pages):
        with _col:
            _is_active = (_k == page_key)
            if st.button(
                f"{PAGES[_k]['icon']} {PAGES[_k]['label'].split(' ')[0]}",
                key=f"topnav_{_k}",
                use_container_width=True,
                type="primary" if _is_active else "secondary",
            ):
                st.session_state["page"] = _k
                st.rerun()
st.markdown(
    "<div style='height:1px;background:rgba(255,255,255,0.05);margin:0 0 14px'></div>",
    unsafe_allow_html=True,
)

log_page(page_key)
page_cfg["render"]()

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.caption("QUIRA OS v0.1 · Dylus Lab © 2026 · SIAP-ICPI v1.0222 · Datos sellados Q1-2026")
