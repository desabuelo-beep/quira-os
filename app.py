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

/* ── LAYOUT ANCHO TOTAL ── */
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
.appview-container .main section {
    padding-top: 0.5rem !important;
}

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

/* ── NAV BUTTONS — estado activo ── */
.nav-active > button {
    background: rgba(0,212,255,0.12) !important;
    border-color: rgba(0,212,255,0.3) !important;
    color: #00D4FF !important;
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

/* ── Z-INDEX ── */
[data-testid="stSidebar"] { z-index: 100 !important; }
section.main, [data-testid="stMain"] { z-index: 10 !important; }
[data-baseweb="popover"],
[data-baseweb="tooltip"],
[data-testid="stPopover"] { z-index: 99999 !important; }

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
}
</style>
""", unsafe_allow_html=True)

# ── INIT SESSION + SEGURIDAD ──────────────────────────────────────────────────
init_session()
check_session_expiry()

# ── GATE: LOGIN ────────────────────────────────────────────────────────────────
if not is_authenticated():
    render_login()
    st.stop()

# ── RC-2B: SCHEDULER INSTITUCIONAL (silencioso) ───────────────────────────────
try:
    from sentinel.scheduler import tick as _scheduler_tick
    from sentinel.db_config import get_connection as _get_db
    _sched_conn = _get_db()
    _scheduler_tick(_sched_conn)
    _sched_conn.close()
except Exception:
    pass

# ── CARGA DE PÁGINAS ───────────────────────────────────────────────────────────
# Fase 1 — Inicio (nuevo, Sprint 2)
from quira_pages.p0_inicio       import render as p0

# Técnico / Operativo
from quira_pages.p_sentinel_hub  import render as p_hub
from quira_pages.p_carga         import render as p_carga
from quira_pages.p_ingesta       import render as p_ingesta
from quira_pages.p_historico     import render as p_historico
from quira_pages.p_alertas       import render as p_alertas
from quira_pages.p_seguimiento   import render as p_seguimiento
from quira_pages.p_reportes      import render as p_reportes
from quira_pages.p_gestion       import render as p_gestion

# Ejecutivo / Directivo
from quira_pages.p_ejecutivo     import render as p_ejecutivo
from quira_pages.p1_dashboard    import render as p1
from quira_pages.p6_pulso        import render as p6
from quira_pages.p7_brecha       import render as p7

# Análisis institucional
from quira_pages.p2_holding      import render as p2
from quira_pages.p8_metas        import render as p8
from quira_pages.p9_sat          import render as p9
from quira_pages.p10_inversion   import render as p10
from quira_pages.p12_cadena      import render as p12
from quira_pages.p14_eficiencia  import render as p14
from quira_pages.p5_operacion    import render as p5

# Ciudadanía / Respaldo
from quira_pages.p15_transparencia import render as p15
from quira_pages.p16_gobernanza  import render as p16_gobernanza

# Proyección
from quira_pages.p13_simulador   import render as p13

# IA
from components.sentinel         import render_sentinel

# Fase 2+ (importar pero NO registrar en PAGES — se activarán en Sprint 3)
# from quira_pages.p4_geotwin    import render as p4   # Fase 2 — GeoTwin
# from quira_pages.p11_ods       import render as p11  # Fase 2 — ODS
# from quira_pages.p18_cooperacion import render as p18  # Fase 2
# from quira_pages.p19_genero    import render as p19  # Fase 2

def _p_sentinel():
    render_sentinel()


# ── CATÁLOGO DE PÁGINAS CON CONTROL DE ACCESO ─────────────────────────────────
# roles: lista de roles que pueden ver esta página.
# Roles disponibles: "Alcalde", "Concejal", "Técnico"
PAGES = {
    # ── INICIO (todos los roles) ───────────────────────────────────────────
    "inicio": {
        "label":  "Estado del Municipio",
        "icon":   "⬡",
        "render": p0,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },

    # ── VISIÓN EJECUTIVA ───────────────────────────────────────────────────
    "ejecutivo": {
        "label":  "Vista Ejecutiva",
        "icon":   "🏛",
        "render": p_ejecutivo,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },
    "pulso": {
        "label":  "Pulso del Municipio",
        "icon":   "⚡",
        "render": p6,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },
    "brecha": {
        "label":  "Causas de la Brecha",
        "icon":   "📉",
        "render": p7,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },

    # ── ALERTAS ───────────────────────────────────────────────────────────
    "sat": {
        "label":  "Señales de Alerta SAT",
        "icon":   "🚨",
        "render": p9,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },
    "metas": {
        "label":  "Metas del Plan Cantonal",
        "icon":   "🎯",
        "render": p8,
        "roles":  ["Concejal", "Técnico"],
    },

    # ── MUNICIPAL ─────────────────────────────────────────────────────────
    "holding": {
        "label":  "Grupo Municipal",
        "icon":   "🏛️",
        "render": p2,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },
    "inversion": {
        "label":  "Inversión por Habitante",
        "icon":   "💰",
        "render": p10,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },
    "gobernanza": {
        "label":  "Participación Ciudadana",
        "icon":   "🗳️",
        "render": p16_gobernanza,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },
    "transparencia": {
        "label":  "Transparencia Pública",
        "icon":   "🔍",
        "render": p15,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },

    # ── PROYECCIÓN ────────────────────────────────────────────────────────
    "simulador": {
        "label":  "Proyector ✨",
        "icon":   "🧮",
        "render": p13,
        "roles":  ["Alcalde", "Concejal", "Técnico"],
    },

    # ── OPERATIVO (Técnico + Concejal) ────────────────────────────────────
    "dashboard": {
        "label":  "Tablero Técnico",
        "icon":   "📊",
        "render": p1,
        "roles":  ["Concejal", "Técnico"],
    },
    "eficiencia": {
        "label":  "Eficiencia por Dirección",
        "icon":   "📋",
        "render": p14,
        "roles":  ["Concejal", "Técnico"],
    },
    "cadena": {
        "label":  "Cadena de Planificación",
        "icon":   "🔗",
        "render": p12,
        "roles":  ["Técnico"],
    },
    "operacion": {
        "label":  "Operación Técnica",
        "icon":   "⚙️",
        "render": p5,
        "roles":  ["Técnico"],
    },

    # ── CONTROL (solo Técnico) ────────────────────────────────────────────
    "sentinel_hub": {
        "label":  "Centro de Control",
        "icon":   "⬡",
        "render": p_hub,
        "roles":  ["Técnico"],
    },
    "carga": {
        "label":  "Panel de Carga",
        "icon":   "⬆️",
        "render": p_carga,
        "roles":  ["Técnico"],
    },
    "ingesta": {
        "label":  "Ingesta Mensual",
        "icon":   "📥",
        "render": p_ingesta,
        "roles":  ["Técnico"],
    },
    "historico": {
        "label":  "Historial de Snapshots",
        "icon":   "📈",
        "render": p_historico,
        "roles":  ["Técnico"],
    },
    "alertas": {
        "label":  "Monitor de Alertas",
        "icon":   "🔔",
        "render": p_alertas,
        "roles":  ["Técnico"],
    },
    "seguimiento": {
        "label":  "Seguimiento",
        "icon":   "📊",
        "render": p_seguimiento,
        "roles":  ["Técnico"],
    },
    "reportes": {
        "label":  "Reportes",
        "icon":   "📄",
        "render": p_reportes,
        "roles":  ["Técnico"],
    },
    "gestion": {
        "label":  "Gestión de Tareas",
        "icon":   "🗓",
        "render": p_gestion,
        "roles":  ["Técnico"],
    },

    # ── IA (solo Técnico) ─────────────────────────────────────────────────
    "sentinel": {
        "label":  "Sentinel · IA",
        "icon":   "🔮",
        "render": _p_sentinel,
        "roles":  ["Técnico"],
    },
}

# ── SECCIONES POR ROL ──────────────────────────────────────────────────────────
# Cada sección define qué páginas agrupa. El sidebar filtra automáticamente
# por rol antes de renderizar — si la sección queda vacía, no se muestra.
SECTIONS = [
    ("SITUACIÓN",   "Estado y prioridades",   ["inicio", "ejecutivo", "pulso", "brecha"]),
    ("ALERTAS",     "Señales activas",         ["sat", "metas", "inversion"]),
    ("MUNICIPAL",   "Organización del GAD",    ["holding", "gobernanza", "transparencia"]),
    ("PROYECCIÓN",  "Escenarios",              ["simulador"]),
    ("ANÁLISIS",    "Datos y métricas",        ["dashboard", "eficiencia", "cadena", "operacion"]),
    ("CONTROL",     "Operación interna",       ["sentinel_hub", "carga", "ingesta", "historico", "alertas", "seguimiento", "reportes", "gestion"]),
    ("IA",          "Inteligencia artificial", ["sentinel"]),
]


# ── HELPER: páginas accesibles para el rol actual ─────────────────────────────
def _accessible_pages() -> set[str]:
    rol = st.session_state.get("rol", "")
    return {k for k, v in PAGES.items() if rol in v.get("roles", [])}


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    rol       = st.session_state.get("rol", "")
    rol_emoji = st.session_state.get("rol_emoji", "")

    # Logo + identidad
    st.markdown(f"""
<div style="padding:16px 0 20px">
    <div style="font-size:1.4rem;font-weight:900;color:#00D4FF;letter-spacing:-0.03em;
                margin-bottom:2px">⬡ {APP_NAME}</div>
    <div style="font-size:0.65rem;color:rgba(255,255,255,0.35);letter-spacing:0.05em;
                text-transform:uppercase">{APP_VERSION} · Gobernanza Municipal</div>
</div>
<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:10px;padding:10px 12px;margin-bottom:20px">
    <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:4px">SESIÓN ACTIVA</div>
    <div style="font-size:12px;font-weight:700;color:#E2E8F0">{rol_emoji} {rol}</div>
    <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:2px">{GAD_NOMBRE}</div>
</div>
    """, unsafe_allow_html=True)

    # Navegación filtrada por rol
    current_page = st.session_state.get("page", "inicio")
    accessible   = _accessible_pages()

    for section_id, section_label, page_keys in SECTIONS:
        # Solo mostrar páginas accesibles para este rol
        visible = [k for k in page_keys if k in accessible and k in PAGES]
        if not visible:
            continue  # sección no visible para este rol

        st.markdown(f"""
<div style="font-size:9px;font-weight:700;color:rgba(0,212,255,0.55);
            letter-spacing:0.09em;text-transform:uppercase;
            padding:10px 2px 3px;border-top:1px solid rgba(255,255,255,0.05);
            margin-top:2px">{section_id}
    <span style="color:rgba(255,255,255,0.2);font-weight:400"> · {section_label}</span>
</div>
        """, unsafe_allow_html=True)

        for key in visible:
            page = PAGES[key]
            is_active = (key == current_page)
            btn_style = "primary" if is_active else "secondary"
            if st.button(
                f"{page['icon']} {page['label']}",
                key=f"nav_{key}",
                use_container_width=True,
                type=btn_style,
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
    <span style="color:rgba(255,180,0,0.5)">⚠ Entorno PMV · Sprint 2</span>
</div>
    """, unsafe_allow_html=True)

    # Logout
    if st.button("← Cerrar Sesión", use_container_width=True):
        logout()
        st.rerun()

    # SAT badge rápido (solo si hay alertas críticas)
    from data.loader import load_all, get_sat_counts
    try:
        _data = load_all()
        _sat  = get_sat_counts(_data)
        if _sat["criticos"] > 0:
            n = _sat["criticos"]
            st.error(
                f"🔴 {n} señal{'es' if n > 1 else ''} crítica{'s' if n > 1 else ''} activa{'s' if n > 1 else ''}"
            )
    except Exception:
        pass


# ── MAIN CONTENT ───────────────────────────────────────────────────────────────
# Resolver claves legacy → página correcta
_LEGACY_KEYS: dict[str, str] = {
    "confianza":    "gobernanza",
    "rdc":          "gobernanza",
    "sentinel_hub": "sentinel_hub",  # mantener si el usuario navega directo
    "aprendizaje":  "sentinel",
    "congruencia":  "sat",
    "congruencias": "sat",
    "dashboard":    "dashboard",
    "ejecutivo":    "ejecutivo",
}

page_key = st.session_state.get("page", "inicio")

# Aplicar mapa legacy
if page_key in _LEGACY_KEYS and page_key not in PAGES:
    page_key = _LEGACY_KEYS[page_key]
    st.session_state["page"] = page_key

# Si la página no es accesible para el rol, redirigir a inicio
accessible = _accessible_pages()
if page_key not in accessible or page_key not in PAGES:
    page_key = "inicio"
    st.session_state["page"] = page_key

page_cfg = PAGES[page_key]

log_page(page_key)
page_cfg["render"]()

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.caption(
    "QUIRA OS · Gobernanza Municipal · Dylus Lab © 2026 · "
    "Datos verificados corte enero–marzo 2026 · Sprint 2"
)
