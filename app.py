"""
QUIRA OS v0.1 — Entry Point
Sistema Integral de Gobernanza · GAD Municipal de Montecristi
Dylus Lab © 2026
"""
import streamlit as st
from config import APP_NAME, APP_VERSION, GAD_NOMBRE, GAD_PERIODO, ALCALDE, CORTE
from utils.session import init_session, is_authenticated, logout, navigate_to, is_tecnico
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
</style>
""", unsafe_allow_html=True)

# ── INIT SESSION ───────────────────────────────────────────────────────────────
init_session()

# ── GATE: LOGIN ────────────────────────────────────────────────────────────────
if not is_authenticated():
    render_login()
    st.stop()

# ── CARGA LAZY DE PÁGINAS ──────────────────────────────────────────────────────
from pages.p1_dashboard    import render as p1
from pages.p2_holding      import render as p2
from pages.p3_congruencias import render as p3
from pages.p4_geotwin      import render as p4
from pages.p5_operacion    import render as p5
from components.sentinel   import render_sentinel

def _p6_sentinel():
    render_sentinel()

PAGES = {
    "dashboard":    {"label": "Tablero Ejecutivo",     "icon": "📊", "render": p1},
    "holding":      {"label": "Holding Municipal",     "icon": "🏛️", "render": p2},
    "congruencias": {"label": "Congruencias",          "icon": "🎯", "render": p3},
    "geotwin":      {"label": "GeoTwin · Territorio",  "icon": "🗺️", "render": p4},
    "operacion":    {"label": "Operación Técnica",     "icon": "⚙️", "render": p5},
    "sentinel":     {"label": "Sentinel · IA",         "icon": "🔮", "render": _p6_sentinel},
}

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

    # Navegación
    st.markdown("""
    <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);
                letter-spacing:0.08em;text-transform:uppercase;margin-bottom:8px">
        MÓDULOS QUIRA OS
    </div>
    """, unsafe_allow_html=True)

    current_page = st.session_state.get("page", "dashboard")
    for key, page in PAGES.items():
        # Etiqueta con notas especiales
        disabled_note = " 🔒" if key == "operacion" and not is_tecnico() else ""
        sentinel_note = " ✨" if key == "sentinel" else ""

        if st.button(
            f"{page['icon']} {page['label']}{disabled_note}{sentinel_note}",
            key=f"nav_{key}",
            use_container_width=True,
        ):
            st.session_state["page"] = key
            st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Info GAD
    st.markdown(f"""
    <div style="border-top:1px solid rgba(255,255,255,0.06);padding-top:14px">
        <div style="font-size:9px;color:rgba(255,255,255,0.25);line-height:1.6">
            🏛️ {GAD_NOMBRE}<br>
            📅 Período {GAD_PERIODO}<br>
            👤 {ALCALDE}<br>
            📊 Corte {CORTE}<br>
            <br>
            <span style="color:rgba(255,180,0,0.5)">⚠ Entorno PMV · no producción</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

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
            st.markdown(f"""
            <div style="margin-top:12px;background:rgba(229,62,62,0.1);
                        border:1px solid rgba(229,62,62,0.25);border-radius:8px;
                        padding:8px 10px;text-align:center">
                <div style="font-size:10px;font-weight:700;color:#FC8181">
                    🔴 {_sat['criticos']} SAT Crítica{'s' if _sat['criticos']>1 else ''} Activa{'s' if _sat['criticos']>1 else ''}
                </div>
                <div style="font-size:9px;color:rgba(255,255,255,0.35);margin-top:2px">
                    Ver Tablero Ejecutivo
                </div>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        pass

# ── MAIN CONTENT ───────────────────────────────────────────────────────────────
page_key = st.session_state.get("page", "dashboard")
page_cfg  = PAGES.get(page_key, PAGES["dashboard"])
page_cfg["render"]()

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:40px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.05);
            text-align:center">
    <div style="font-size:9px;color:rgba(255,255,255,0.18)">
        QUIRA OS v0.1 · Dylus Lab © 2026 · SIAP-ICPI v1.0222 · Datos sellados Q1-2026
    </div>
</div>
""", unsafe_allow_html=True)
