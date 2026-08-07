"""
QUIRA Intelligence — Entry Point · 2026-05-27
Infraestructura de monitoreo institucional preventivo para GADs del Ecuador.
Dylus Lab © 2026

ARQUITECTURA 4 AMBIENTES (regla canónica permanente — ver docs/NOMENCLATURA_CANONICA.md):
  🏛 GOV    — Observatorio · Ejecutivo + Técnico · ACTIVO
  🌎 Civic  — QUIRA Ciudadano · acceso público · Fase 3
  📑 Coop   — QUIRA Cooperación · bilaterales y multilaterales · Fase 2
  ⚙  OPS   — Operaciones · Operador + Administrador · ACTIVO

ROLES (CONGELADOS — no cambiar sin revisión doctrinal):
  ejecutivo    → GOV (vista ejecutiva: alcalde, concejales)
  tecnico      → GOV (vista técnica: planificación)
  operador     → OPS (infraestructura: equipo Dylus Lab)
  administrador→ OPS + GOV verificación (admin total)

ROUTING POST-LOGIN:
  ejecutivo / tecnico    → GOV
  operador / administrador → OPS
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
[data-testid="stHeader"] { display: none !important; }
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
from quira_pages.env_coop   import render as _render_coop
from quira_pages.env_obs    import render as _render_obs
from quira_pages.env_ops    import render as _render_ops


# ── CATÁLOGO DE AMBIENTES ─────────────────────────────────────────────────────
# Ambiente primero, rol después.
# GOV / Civic / Impact: todos los roles autenticados.
# Ops: solo Operator / Admin.

# Etiquetas y colores al sistema v1.1 (2026-08-06). Las anteriores publicaban
# «QUIRA Institucional» —el nombre retirado de la portada— y la paleta previa.
from utils.css_tokens import C as _C

ENVIRONMENTS = {
    "gov": {
        "label":       "Centro",
        "icon":        "🏛",
        "render":      _render_gov,
        "roles":       ["Observatorio", "Ejecutivo", "Directivo", "Administrador"],
        "desc":        "Centro de Inteligencia Territorial",
        "badge_color": _C.ACENTO,
        "ops_only":    False,
    },
    "civic": {
        "label":       "Ciudadana",
        "icon":        "🌎",
        "render":      _render_civic,
        "roles":       ["Observatorio", "Ejecutivo", "Directivo", "Operador", "Administrador"],
        "desc":        "QUIRA Ciudadana · control social",
        "badge_color": _C.V_TX3,
        "ops_only":    False,
    },
    # La clave era `impact` y el nombre público «Cooperación» (Javo · 2026-08-07):
    # el canon trató ambos productos como uno solo y quedaron cruzados. Son
    # distintos —Cooperación responde «¿qué puede financiarse y con qué
    # instrumento?»; Impact, «¿qué pueden investigar y reproducir terceros?»— y
    # el contenido de este ambiente es cooperación, no investigación. La clave
    # pasa a `coop` y `impact` queda LIBRE para cuando ese producto exista.
    "coop": {
        "label":       "Cooperación",
        "icon":        "📑",
        "render":      _render_coop,
        "roles":       ["Observatorio", "Ejecutivo", "Directivo", "Operador", "Administrador"],
        "desc":        "Cooperación bilateral y multilateral · Fase 2",
        "badge_color": _C.V_TX3,
        "ops_only":    False,
    },
    # EL OBSERVATORIO — producto principal (ADR-041 §5.1), ambiente propio.
    # Va SEPARADO de Operaciones (Javo · 2026-08-06, corrigiendo al director, que
    # los había fusionado). No son el mismo concepto con dos nombres:
    #   · Observatorio → instrumento de administración pública y desarrollo. Sus
    #     interlocutores son el sector público, los multilaterales y la
    #     cooperación. Lo que se ve aquí se enseña.
    #   · Operaciones  → mantenimiento técnico, para cuando algo se rompe.
    # Fusionarlos degradaba el producto principal a herramienta de soporte.
    "obs": {
        "label":       "Observatorio",
        "icon":        "◷",
        "render":      _render_obs,
        "roles":       ["Observatorio", "Ejecutivo", "Directivo", "Administrador"],
        "desc":        "Observatorio de Integridad Territorial",
        "badge_color": _C.ACENTO,
        "ops_only":    False,
    },
    "ops": {
        "label":       "Operaciones",
        "icon":        "⚙",
        "render":      _render_ops,
        "roles":       ["Observatorio", "Operador", "Administrador"],
        "desc":        "Mantenimiento técnico · equipo Dylus Lab",
        "badge_color": _C.V_TX3,
        "ops_only":    True,
    },
}

_ENV_ORDER = ["gov", "obs", "civic", "coop", "ops"]

# Mapa legacy: cualquier ruta del Sprint 1-2 → su ambiente correcto
_LEGACY: dict[str, str] = {
    # Clave renombrada (2026-08-07): una sesión abierta en `impact` no debe
    # quedar sin destino. El nombre queda reservado para el producto Impact.
    "impact":       "coop",
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
    """Ambientes que el rol activo puede abrir.

    La comparación es sin distinguir mayúsculas a propósito: la sesión guarda el
    nombre VISIBLE del rol («Observatorio») mientras que el resto del sistema
    —y las pruebas— usan la clave en minúsculas. Con la comparación literal,
    `observatorio` no coincidía con ninguna entrada y el router caía siempre en
    su rama de emergencia, de modo que el camino real nunca se ejercitaba."""
    rol = str(st.session_state.get("rol", "")).strip().lower()
    return {k for k, v in ENVIRONMENTS.items()
            if any(rol == str(r).lower() for r in v.get("roles", []))}


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    rol       = st.session_state.get("rol", "")
    rol_emoji = st.session_state.get("rol_emoji", "")

    # ── Identidad ────────────────────────────────────────────────────────────
    # La MARCA, no un glifo: decía «⬡ QUIRA Intelligence» con un hexágono
    # tipográfico. Y bajo él, «GOV · CIVIC · IMPACT · OPS» —nombres internos de
    # los ambientes— que la frontera de lenguaje no admite en pantalla.
    from utils.marca import logo as _logo_marca
    st.markdown(f"""
<div style="padding:14px 0 12px">
    <div style="display:flex;align-items:center;gap:10px">
      <span style="line-height:0">{_logo_marca("marfil", 26)}</span>
      <span style="font:600 16px/1 Archivo,Inter,sans-serif;letter-spacing:.19em;
                   color:{_C.V_TX}">QUIRA</span>
    </div>
    <div style="font-size:9px;color:{_C.V_TX3};letter-spacing:.05em;margin-top:7px">
        {APP_VERSION} · {GAD_NOMBRE}</div>
</div>
<div style="background:{_C.VOLCAN_UP};border:1px solid {_C.V_BD};
            border-radius:10px;padding:10px 12px;margin-bottom:16px">
    <div style="font-size:10px;color:{_C.V_TX3};margin-bottom:3px">SESIÓN ACTIVA</div>
    <div style="font-size:12px;font-weight:700;color:{_C.V_TX}">{rol_emoji} {rol}</div>
    <div style="font-size:9px;color:{_C.V_TX3};margin-top:1px">{GAD_NOMBRE}</div>
</div>
    """, unsafe_allow_html=True)

    current = st.session_state.get("page", "gov")
    acc     = _accessible()

    # ── Navegación interna GOV (aparece solo cuando GOV está activo) ──────────
    if current == "gov":
        try:
            from quira_pages.env_gov import render_sidebar_nav
            render_sidebar_nav()
        except Exception:
            pass

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


# ── ROUTER PRINCIPAL ──────────────────────────────────────────────────────────
page_key = st.session_state.get("page", "gov")

# Resolver legacy
if page_key in _LEGACY:
    page_key = _LEGACY[page_key]
    st.session_state["page"] = page_key

# Resolver acceso — ante un destino inválido, el Centro; si tampoco, el primero
# accesible. Antes el fallback era `"ops" if is_ops_user() else "gov"`, y desde
# que el rol único alcanza ambos ambientes eso habría mandado al panel de
# operación a quien pidiera cualquier ruta rota. El Centro es el destino natural.
acc = _accessible()
if page_key not in acc or page_key not in ENVIRONMENTS:
    page_key = "gov" if "gov" in acc else next(iter(sorted(acc)), "gov")
    st.session_state["page"] = page_key

log_page(page_key)
ENVIRONMENTS[page_key]["render"]()
