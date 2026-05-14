"""
QUIRA OS v0.1 — Pantalla de login
Dylus Lab © 2026
"""
import streamlit as st
from config import USERS, APP_NAME, GAD_NOMBRE, CORTE
from utils.session import set_user


def render_login() -> None:
    """Renderiza la pantalla de autenticación QUIRA OS."""
    # CSS mínimo para login
    st.markdown("""<style>
    [data-testid="stAppViewContainer"] {
        background: #0A1628;
    }
    [data-testid="stHeader"] { background: transparent; }
    .login-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 16px;
        padding: 2.5rem;
        max-width: 420px;
        margin: auto;
    }
    .login-logo {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: -1px;
        color: #00D4FF;
        text-align: center;
        margin-bottom: 4px;
    }
    .login-sub {
        font-size: 0.78rem;
        color: rgba(255,255,255,0.45);
        text-align: center;
        margin-bottom: 1.8rem;
        letter-spacing: 0.04em;
    }
    .login-gad {
        font-size: 0.85rem;
        color: rgba(255,255,255,0.7);
        text-align: center;
        margin-bottom: 1.4rem;
        border-top: 1px solid rgba(255,255,255,0.08);
        padding-top: 1rem;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        color: rgba(255,255,255,0.6) !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF, #7C5CFC) !important;
        color: #0A1628 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100%;
        padding: 0.6rem !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.04em !important;
    }
    .stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px);
    }
    .login-error {
        background: rgba(229,62,62,0.12);
        border: 1px solid rgba(229,62,62,0.35);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        color: #FC8181;
        font-size: 0.82rem;
        margin-top: 0.6rem;
    }
    .login-badge {
        display: inline-block;
        background: rgba(0,212,255,0.1);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.7rem;
        color: #00D4FF;
        margin: 0 auto 1.2rem;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Centrar contenido
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown(f"""
<div class="login-card">
    <div class="login-logo">⬡ {APP_NAME}</div>
    <div class="login-sub">SISTEMA INTEGRAL DE GOBERNANZA</div>
    <div style="text-align:center;margin-bottom:1.2rem">
        <span class="login-badge">🔒 PMV · Acceso Restringido · {CORTE}</span>
    </div>
    <div class="login-gad">🏛️ {GAD_NOMBRE}</div>
</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            rol_options = {
                "🏛️ Alcalde":  "alcalde",
                "⚖️ Concejal": "concejal",
                "⚙️ Técnico":  "tecnico",
            }
            rol_display = st.selectbox(
                "ROL DE ACCESO",
                options=list(rol_options.keys()),
            )
            password = st.text_input(
                "CONTRASEÑA",
                type="password",
                placeholder="••••••••",
            )
            submitted = st.form_submit_button("ACCEDER →")

        if submitted:
            usuario_key = rol_options[rol_display]
            user_cfg    = USERS.get(usuario_key, {})

            if password == user_cfg.get("password", ""):
                set_user(
                    usuario=usuario_key,
                    rol=user_cfg["rol"],
                    emoji=user_cfg["emoji"],
                )
                st.rerun()
            else:
                st.error("⚠️ Contraseña incorrecta. Intente nuevamente.")

        # Nota PMV
        st.markdown("""
<div style="text-align:center;margin-top:1.6rem;font-size:0.68rem;
            color:rgba(255,255,255,0.22);line-height:1.5">
    QUIRA OS v0.1 · Dylus Lab © 2026<br>
    Datos sellados Q1-2026 · SIAP-ICPI v1.0222<br>
    <span style="color:rgba(255,180,0,0.5)">⚠ Entorno de demostración — no producción</span>
</div>
        """, unsafe_allow_html=True)
