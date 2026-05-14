"""
QUIRA OS v0.1 — Gestión de sesión Streamlit
Patrón SESSION_DEFAULTS heredado de TERRA_DEPLOY_v1.0
Dylus Lab © 2026
"""
import streamlit as st

SESSION_DEFAULTS: dict = {
    "authenticated": False,
    "usuario":       None,
    "rol":           None,
    "rol_emoji":     None,
    "page":          "dashboard",
    "data_loaded":   False,
    "show_tech":     False,   # modo técnico: muestra tech-labels backstage
}


def init_session() -> None:
    """Inicializa el estado de sesión con los valores por defecto."""
    for key, value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


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


def logout() -> None:
    for key in SESSION_DEFAULTS:
        st.session_state[key] = SESSION_DEFAULTS[key]
    # Limpiar cache de datos
    if hasattr(st, "cache_data"):
        st.cache_data.clear()


def navigate_to(page: str) -> None:
    st.session_state["page"] = page
    st.rerun()


def is_tecnico() -> bool:
    return st.session_state.get("rol") == "Técnico"


def is_alcalde() -> bool:
    return st.session_state.get("rol") == "Alcalde"
