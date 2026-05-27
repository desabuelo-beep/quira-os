"""
QUIRA Intelligence — Entry Point · 2026-05-26
Infraestructura de monitoreo institucional preventivo para GADs del Ecuador.
Dylus Lab © 2026

ARQUITECTURA 4 AMBIENTES (regla canónica permanente — no negociable):
  🏛 GOV    — Monitoreo institucional · el producto hoy · ACTIVO
  🌎 Civic  — Ciudadanía · acceso público sin login · EN CONSTRUCCIÓN
  📑 Impact — Cooperación internacional · roadmap futuro
  ⚙  Ops   — Infraestructura interna · solo equipo QUIRA

REGLAS ARQUITECTURALES PERMANENTES:
  · Un solo dominio: quiraholding.streamlit.app
  · Nada vive fuera de estos 4 ambientes. Sin subdominios separados.
  · GOV recibe vistas nuevas como tabs — nunca un quinto ambiente.
  · Civic: acceso público sin autenticación (ciudadanos).
  · Impact: placeholder hasta que haya 6 meses de datos longitudinales.
  · Roles institucionales: Viewer / Analyst / Operator / Admin.
  · Civic no requiere credenciales institucionales.
"""
import streamlit as st
from config import APP_NAME, APP_VERSION, GAD_NOMBRE, GAD_PERIODO, ALCALDE, CORTE
from utils.session import (
    init_session, check_session_expiry, is_authenticated,
    logout, is_operator, get_rol,
)
from utils.audit_log import log_page
from auth.login import render_login


# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"QUIRA Intelligence · {GAD_NOMBRE}",
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

# ── IMPORTS LAZY — 4 ambientes ────────────────────────────────────────────────
from quira_pages.env_gov    import render as _render_gov
from quira_pages.env_civic  import render as _render_civic
from quira_pages.env_impact import render as _render_impact
from quira_pages.env_ops    import render as _render_ops


# ── CATÁLOGO DE AMBIENTES ─────────────────────────────────────────────────────
# Ambiente primero, rol después.
# GOV / Civic / Impact: todos los roles autenticados.
# Ops: solo Operator / Admin.

ENVIRONMENTS = {
    "gov": {
        "label":       "GOV",
        "icon":        "🏛",
        "render":      _render_gov,
        "roles":       ["Viewer", "Analyst", "Operator", "Admin"],
        "desc":        "Monitoreo Institucional",
        "badge_color": "#00D4FF",
        "ops_only":    False,
    },
    "civic": {
        "label":       "Civic",
        "icon":        "🌎",
        "render":      _render_civic,
        "roles":       ["Viewer", "Analyst", "Operator", "Admin"],
        "desc":        "Ciudadanía · Próximamente",
        "badge_color": "#22C55E",
        "ops_only":    False,
    },
    "impact": {
        "label":       "Impact",
        "icon":        "📑",
        "render":      _render_impact,
        "roles":       ["Viewer", "Analyst", "Operator", "Admin"],
        "desc":        "Cooperación · Próximamente",
        "badge_color": "#A855F7",
        "ops_only":    False,
    },
    "ops": {
        "label":       "Ops",
        "icon":        "⚙",
        "render":      _render_ops,
        "roles":       ["Operator", "Admin"],
        "desc":        "Infraestructura Interna",
        "badge_color": "#F97316",
        "ops_only":    True,
    },
}

_ENV_ORDER = ["gov", "civic", "impact", "ops"]

# Mapa legacy: cualquier ruta del Sprint 1-2 → su ambiente correcto
_LEGACY: dict[str, str] = {
    # Módulos Sprint 2 → GOV
    "inicio":       "gov",
    "situacion":    "gov",
    "alertas":      "gov",
    "municipal":    "gov",
    "analisis":     "gov",
    "proyector":    "gov",
    # Páginas planas → GOV
    "ejecutivo":    "gov",
    "pulso":        "gov",
    "brecha":       "gov",
    "dashboard":    "gov",
    "sat":          "gov",
    "metas":        "gov",
    "eficiencia":   "gov",
    "cadena":       "gov",
    "operacion":    "gov",
    "holding":      "gov",
    "gobernanza":   "gov",
    "transparencia":"gov",
    "inversion":    "gov",
    "confianza":    "gov",
    "rdc":          "gov",
    "congruencia":  "gov",
    "congruencias": "gov",
    "simulador":    "gov",
    # Control → Ops
    "control":      "ops",
    "sentinel_hub": "ops",
    "carga":        "ops",
    "ingesta":      "ops",
    "historico":    "ops",
    "alertas_sys":  "ops",
    "seguimiento":  "ops",
    "reportes":     "ops",
    "gestion":      "ops",
    "sentinel":     "ops",
    "aprendizaje":  "ops",
}


def _accessible() -> set[str]:
    rol = st.session_state.get("rol", "")
    return {k for k, v in ENVIRONMENTS.items() if rol in v.get("roles", [])}


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    rol       = st.session_state.get("rol", "")
    rol_emoji = st.session_state.get("rol_emoji", "")

    # ── Identidad QUIRA Intelligence ─────────────────────────────────────────
    st.markdown(f"""
<div style="padding:16px 0 12px">
    <div style="font-size:1.4rem;font-weight:900;color:#00D4FF;letter-spacing:-0.03em;
                margin-bottom:1px">⬡ QUIRA Intelligence</div>
    <div style="font-size:9px;color:rgba(255,255,255,.25);letter-spacing:.04em;margin-top:1px">
        GOV · CIVIC · IMPACT · OPS</div>
    <div style="display:flex;align-items:center;gap:6px;margin-top:3px">
        <span style="font-size:9px;font-weight:700;color:#00D4FF;background:rgba(0,212,255,0.12);
                     border:1px solid rgba(0,212,255,0.25);border-radius:4px;
                     padding:1px 6px;letter-spacing:.06em">INTELLIGENCE</span>
        <span style="font-size:9px;color:rgba(255,255,255,0.3);letter-spacing:.05em">
            {APP_VERSION} · {GAD_NOMBRE}</span>
    </div>
</div>
<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
            border-radius:10px;padding:10px 12px;margin-bottom:16px">
    <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-bottom:3px">SESIÓN ACTIVA</div>
    <div style="font-size:12px;font-weight:700;color:#E2E8F0">{rol_emoji} {rol}</div>
    <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:1px">{GAD_NOMBRE}</div>
</div>
    """, unsafe_allow_html=True)

    # ── Selector de Ambientes ─────────────────────────────────────────────────
    st.markdown(
        '<div style="font-size:9px;color:rgba(255,255,255,.35);letter-spacing:.08em;'
        'text-transform:uppercase;margin-bottom:6px">AMBIENTES</div>',
        unsafe_allow_html=True,
    )

    current = st.session_state.get("page", "gov")
    acc     = _accessible()

    for env_key in _ENV_ORDER:
        if env_key not in acc:
            continue
        env = ENVIRONMENTS[env_key]
        is_active = (env_key == current)
        badge_color = env["badge_color"]

        # Badge de ambiente
        badge_html = (
            f'<span style="font-size:8px;font-weight:700;color:{badge_color};'
            f'background:{badge_color}18;border:1px solid {badge_color}33;'
            f'border-radius:3px;padding:1px 5px;margin-left:4px;letter-spacing:.04em">'
            f'{env["label"]}</span>'
        )

        # Nota "próximamente" para Civic e Impact
        coming_soon = env_key in ("civic", "impact")
        label_text = f"{env['icon']}  {env['label']}"
        if coming_soon:
            label_text += "  ·  Próx."

        if st.button(
            label_text,
            key=f"nav_env_{env_key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            help=env["desc"],
        ):
            st.session_state["page"] = env_key
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

    # SAT badge rápido — solo en GOV
    if current == "gov":
        try:
            from data.loader import load_all, get_sat_counts
            _sat = get_sat_counts(load_all())
            if _sat.get("criticos", 0) > 0:
                n = _sat["criticos"]
                st.error(f"🔴 {n} señal{'es' if n > 1 else ''} crítica{'s' if n > 1 else ''}")
        except Exception:
            pass


# ── ROUTER PRINCIPAL ──────────────────────────────────────────────────────────
page_key = st.session_state.get("page", "gov")

# Resolver legacy
if page_key in _LEGACY:
    page_key = _LEGACY[page_key]
    st.session_state["page"] = page_key

# Resolver acceso — fallback a GOV
acc = _accessible()
if page_key not in acc or page_key not in ENVIRONMENTS:
    page_key = "gov"
    st.session_state["page"] = page_key

log_page(page_key)
ENVIRONMENTS[page_key]["render"]()

st.caption(
    f"QUIRA Intelligence · {GAD_NOMBRE} · Dylus Lab © 2026 · "
    f"Gold Master v5.5_TGI · Corte {CORTE}"
)
