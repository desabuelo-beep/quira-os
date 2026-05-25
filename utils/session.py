"""
QUIRA OS — Gestión de sesión segura
  · Registro de login_time para expiración
  · check_session_expiry() llamado al inicio de cada request
Dylus Lab © 2026
"""
import secrets
import time
import streamlit as st
from utils.audit_log import log_logout

SESSION_DEFAULTS: dict = {
    "authenticated": False,
    "usuario":       None,
    "rol":           None,
    "rol_emoji":     None,
    "page":          "inicio",
    "data_loaded":   False,
    "show_tech":     False,
    "login_time":    0,        # timestamp de login — para expiración
    "session_id":    None,     # correlation ID para trazabilidad forense
}

_SESSION_TTL = 3600  # 60 minutos


def init_session() -> None:
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def check_session_expiry() -> None:
    """Si la sesión expiró, hace logout silencioso y fuerza el login."""
    if not is_authenticated():
        return
    login_time = st.session_state.get("login_time", 0)
    if login_time and (time.time() - login_time) > _SESSION_TTL:
        logout(motivo="session_expired")
        st.warning("⏱️ Sesión expirada. Por seguridad, vuelve a iniciar sesión.")
        st.rerun()


def is_authenticated() -> bool:
    return st.session_state.get("authenticated", False)


def get_rol() -> str:
    return st.session_state.get("rol", "")


def get_usuario() -> str:
    return st.session_state.get("usuario", "")


def set_user(usuario: str, rol: str, emoji: str) -> None:
    st.session_state["authenticated"] = True
    st.session_state["usuario"]       = usuario
    st.session_state["rol"]           = rol
    st.session_state["rol_emoji"]     = emoji
    st.session_state["show_tech"]     = (rol == "Técnico")
    st.session_state["login_time"]    = time.time()
    st.session_state["session_id"]    = "sess_" + secrets.token_hex(8)


def logout(motivo: str = "manual") -> None:
    usuario = get_usuario()
    if usuario:
        log_logout(usuario, motivo=motivo)
    for key, val in SESSION_DEFAULTS.items():
        st.session_state[key] = val
    if hasattr(st, "cache_data"):
        st.cache_data.clear()


def navigate_to(page: str) -> None:
    st.session_state["page"] = page
    st.rerun()


def is_tecnico() -> bool:
    return st.session_state.get("rol") == "Técnico"


def is_alcalde() -> bool:
    return st.session_state.get("rol") == "Alcalde"
