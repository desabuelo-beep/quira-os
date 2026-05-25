"""
QUIRA OS v0.1 — Entry Point · Arquitectura Modular Sprint 3
Sistema de Gobernanza Municipal · GAD Montecristi · Dylus Lab © 2026

REGLA ARQUITECTURAL PERMANENTE:
  El sidebar tiene MÁXIMO 7 items por rol.
  Nuevas vistas = tabs dentro del módulo correspondiente.
  Nunca crear un nuevo item de sidebar para una sub-feature.

Módulos:
  M0 · Inicio         → Estado del Municipio (snapshot Q1)
  M1 · Situación      → Vista Ejecutiva | Pulso | Brecha
  M2 · Alertas        → SAT activas | Longitudinal (Sprint 3)
  M3 · Municipal      → Grupo | Participación | Transparencia | Inversión
  M4 · Análisis       → Tablero | Eficiencia | Metas | [Cadena | Op. Tec.]
  M5 · Control        → Pipeline + 9 herramientas operativas (solo Técnico)
  M6 · Proyector      → Simulador (todos los roles)
"""
import streamlit as st
from config import APP_NAME, APP_VERSION, GAD_NOMBRE, GAD_PERIODO, ALCALDE, CORTE
from utils.session import (
    init_session, check_session_expiry, is_authenticated,
    logout, navigate_to, is_tecnico, get_rol,
)
from utils.audit_log import log_page
from auth.login import render_login


# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} · {GAD_NOMBRE}",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── ESTILOS GLOBALES ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0A1628 !important;
    font-family: 'Inter', -apple-system, sans-serif;
    color: #E2E8F0;
}

/* ── LAYOUT ── */
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

iframe {
    width: 100% !important;
    border: none !important;
    display: block !important;
}

[data-testid="stAppViewBlockContainer"],
.appview-container .main section { padding-top: 0.5rem !important; }

[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0 !important;
}

/* ── CHROME ── */
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
    z-index: 100 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdown"] p {
    color: rgba(255,255,255,0.65);
    font-size: 12px;
}

/* ── TABS — módulos internos ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.07);
    gap: 4px;
    padding: 4px;
    flex-wrap: wrap;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    color: rgba(255,255,255,0.5);
    font-size: 12px;
    font-weight: 600;
    border-radius: 7px;
    padding: 6px 14px;
    white-space: nowrap;
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

/* ── Z-INDEX ── */
section.main, [data-testid="stMain"] { z-index: 10 !important; }
[data-baseweb="popover"],
[data-baseweb="tooltip"],
[data-testid="stPopover"] { z-index: 99999 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 10px; }

/* ── DESKTOP: sidebar siempre visible ── */
@media (min-width: 769px) {
    [data-testid="stSidebar"] {
        transform: translateX(0) !important;
        min-width: 244px !important;
        width: 244px !important;
        display: flex !important;
        visibility: visible !important;
    }
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    .main .block-container,
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
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
    [data-testid="stTabs"] [data-baseweb="tab"] {
        font-size: 10px !important;
        padding: 5px 8px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ── INIT + SEGURIDAD ──────────────────────────────────────────────────────────
init_session()
check_session_expiry()

if not is_authenticated():
    render_login()
    st.stop()

# ── SCHEDULER SILENCIOSO ──────────────────────────────────────────────────────
try:
    from sentinel.scheduler import tick as _scheduler_tick
    from sentinel.db_config import get_connection as _get_db
    _sched_conn = _get_db()
    _scheduler_tick(_sched_conn)
    _sched_conn.close()
except Exception:
    pass

# ── MÓDULOS — imports lazy (solo los 6 módulos + inicio) ─────────────────────
from quira_pages.p0_inicio    import render as m0_inicio
from quira_pages.m1_situacion import render as m1_situacion
from quira_pages.m2_alertas   import render as m2_alertas
from quira_pages.m3_municipal import render as m3_municipal
from quira_pages.m4_analisis  import render as m4_analisis
from quira_pages.m5_control   import render as m5_control
from quira_pages.p13_simulador import render as m6_proyector


# ── CATÁLOGO DE MÓDULOS ───────────────────────────────────────────────────────
# Max 7 items en sidebar. roles=[...] controla visibilidad.
# ¡NO añadir aquí sin quitar algo o convertirlo en tab de un módulo existente!
MODULES = {
    "inicio": {
        "label":  "Estado del Municipio",
        "icon":   "⬡",
        "render": m0_inicio,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
        "desc":   "ICPI · SAT activas · Alertas Q1",
    },
    "situacion": {
        "label":  "Situación",
        "icon":   "🏛",
        "render": m1_situacion,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
        "desc":   "Vista Ejecutiva · Pulso · Brecha",
    },
    "alertas": {
        "label":  "Alertas",
        "icon":   "🚨",
        "render": m2_alertas,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
        "desc":   "SAT activas · Evolución longitudinal",
    },
    "municipal": {
        "label":  "Municipal",
        "icon":   "🏛️",
        "render": m3_municipal,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
        "desc":   "Grupo · Participación · Transparencia · Inversión",
    },
    "analisis": {
        "label":  "Análisis",
        "icon":   "📊",
        "render": m4_analisis,
        "roles":  ["Concejal", "Técnico"],
        "desc":   "Tablero · Eficiencia · Metas · Cadena",
    },
    "control": {
        "label":  "Control",
        "icon":   "⚙️",
        "render": m5_control,
        "roles":  ["Técnico"],
        "desc":   "Pipeline · Carga · Ingesta · Sentinel IA",
    },
    "proyector": {
        "label":  "Proyector ✨",
        "icon":   "🧮",
        "render": m6_proyector,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
        "desc":   "Simulador de escenarios",
    },
}

# Orden de aparición en sidebar
_NAV_ORDER = ["inicio", "situacion", "alertas", "municipal", "analisis", "control", "proyector"]

# Mapa de claves legacy → módulo nuevo (para no romper bookmarks)
_LEGACY: dict[str, str] = {
    # páginas planas anteriores → módulo que las contiene ahora
    "ejecutivo":    "situacion",
    "pulso":        "situacion",
    "brecha":       "situacion",
    "dashboard":    "analisis",
    "sat":          "alertas",
    "metas":        "analisis",
    "eficiencia":   "analisis",
    "cadena":       "analisis",
    "operacion":    "analisis",
    "holding":      "municipal",
    "gobernanza":   "municipal",
    "transparencia":"municipal",
    "inversion":    "municipal",
    "sentinel_hub": "control",
    "carga":        "control",
    "ingesta":      "control",
    "historico":    "control",
    "alertas_sys":  "control",
    "seguimiento":  "control",
    "reportes":     "control",
    "gestion":      "control",
    "sentinel":     "control",
    "simulador":    "proyector",
    # legacy Sprint 1
    "confianza":    "municipal",
    "rdc":          "municipal",
    "congruencia":  "alertas",
    "congruencias": "alertas",
    "aprendizaje":  "control",
}


def _accessible() -> set[str]:
    rol = st.session_state.get("rol", "")
    return {k for k, v in MODULES.items() if rol in v.get("roles", [])}


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    rol       = st.session_state.get("rol", "")
    rol_emoji = st.session_state.get("rol_emoji", "")

    # ── Identidad QUIRA GOV ───────────────────────────────────────────────────
    st.markdown(f"""
<div style="padding:16px 0 12px">
    <div style="font-size:1.4rem;font-weight:900;color:#00D4FF;letter-spacing:-0.03em;
                margin-bottom:1px">⬡ {APP_NAME}</div>
    <div style="display:flex;align-items:center;gap:6px;margin-top:3px">
        <span style="font-size:9px;font-weight:700;color:#00D4FF;background:rgba(0,212,255,0.12);
                     border:1px solid rgba(0,212,255,0.25);border-radius:4px;
                     padding:1px 6px;letter-spacing:.06em">GOV</span>
        <span style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:.05em">
            {APP_VERSION} · Gobernanza Municipal</span>
    </div>
</div>
<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:10px;padding:10px 12px;margin-bottom:16px">
    <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:3px">SESIÓN ACTIVA</div>
    <div style="font-size:12px;font-weight:700;color:#E2E8F0">{rol_emoji} {rol}</div>
    <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:1px">{GAD_NOMBRE}</div>
</div>
    """, unsafe_allow_html=True)

    # ── Navegación — máx 7 módulos visibles ──────────────────────────────────
    current = st.session_state.get("page", "inicio")
    acc     = _accessible()

    for key in _NAV_ORDER:
        if key not in acc:
            continue
        mod = MODULES[key]
        is_active = (key == current)
        if st.button(
            f"{mod['icon']}  {mod['label']}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            help=mod["desc"],
        ):
            st.session_state["page"] = key
            st.rerun()

    st.markdown("---")

    # ── Info GAD ──────────────────────────────────────────────────────────────
    st.markdown(f"""
<div style="font-size:9px;color:rgba(255,255,255,0.25);line-height:1.8">
    🏛️ {GAD_NOMBRE}<br>
    📅 Período {GAD_PERIODO}<br>
    👤 {ALCALDE}<br>
    📊 Corte {CORTE}
</div>
    """, unsafe_allow_html=True)

    if st.button("← Cerrar Sesión", use_container_width=True):
        logout()
        st.rerun()

    # SAT badge rápido
    try:
        from data.loader import load_all, get_sat_counts
        _sat = get_sat_counts(load_all())
        if _sat.get("criticos", 0) > 0:
            n = _sat["criticos"]
            st.error(f"🔴 {n} señal{'es' if n > 1 else ''} crítica{'s' if n > 1 else ''}")
    except Exception:
        pass


# ── ROUTER PRINCIPAL ──────────────────────────────────────────────────────────
page_key = st.session_state.get("page", "inicio")

# Resolver legacy
if page_key in _LEGACY:
    page_key = _LEGACY[page_key]
    st.session_state["page"] = page_key

# Guard de acceso
acc = _accessible()
if page_key not in acc or page_key not in MODULES:
    page_key = "inicio"
    st.session_state["page"] = page_key

log_page(page_key)
MODULES[page_key]["render"]()

st.caption(
    "QUIRA OS · Gobernanza Municipal · Dylus Lab © 2026 · "
    "Corte enero–marzo 2026 · Sprint 2"
)
