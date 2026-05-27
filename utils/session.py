"""
QUIRA Intelligence — Gestión de sesión segura (v3 · Nomenclatura canónica 2026-05-27)
  · Roles congelados en español: ejecutivo / tecnico / operador / administrador
  · Helpers de rol actualizados — elimina chequeos en inglés
  · check_session_expiry() llamado al inicio de cada request
  · Expiración de sesión: logout automático a los 60 minutos
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
    "page":          "gov",       # default landing tras login
    "gov_module":    "inicio",    # módulo activo dentro de GOV
    "data_loaded":   False,
    "login_time":    0,
    "session_id":    None,
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
    """
    Registra la sesión autenticada y determina la página de entrada.
    Ejecutivo / Técnico → GOV
    Operador / Administrador → OPS
    """
    from models.auth import ROLE_TECNICO, ROLE_OPERADOR, ROLE_ADMINISTRADOR

    # Determinar página de entrada según rol
    rol_lower = rol.lower()
    if rol_lower in (ROLE_OPERADOR, ROLE_ADMINISTRADOR):
        default_page = "ops"
    else:
        default_page = "gov"

    st.session_state["authenticated"] = True
    st.session_state["usuario"]       = usuario
    st.session_state["rol"]           = rol
    st.session_state["rol_emoji"]     = emoji
    st.session_state["page"]          = default_page
    st.session_state["gov_module"]    = "inicio"
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


# ── Helpers de rol (nomenclatura canónica v3) ────────────────────────────────

def _rol() -> str:
    """Devuelve el rol actual en minúsculas para comparación robusta."""
    return st.session_state.get("rol", "").lower()


def is_ejecutivo() -> bool:
    """True solo para Ejecutivo — alcalde, concejales. (COOTAD: el alcalde es el Ejecutivo.)"""
    return _rol() == "ejecutivo"


def is_tecnico() -> bool:
    """True para Técnico y roles de mayor privilegio (incluye OPS)."""
    return _rol() in ("tecnico", "operador", "administrador")


def is_operador() -> bool:
    """True para Operador o Administrador — acceso OPS."""
    return _rol() in ("operador", "administrador")


def is_admin() -> bool:
    """True solo para Administrador — acceso total."""
    return _rol() == "administrador"


def is_gov_user() -> bool:
    """True para roles con acceso a GOV: Directivo, Técnico, Administrador."""
    return _rol() in ("ejecutivo", "tecnico", "administrador")


def is_ops_user() -> bool:
    """True para roles con acceso a OPS: Operador, Administrador."""
    return _rol() in ("operador", "administrador")


def is_viewer() -> bool:
    """True para cualquier rol autenticado (mínimo privilegio)."""
    return _rol() in ("ejecutivo", "tecnico", "operador", "administrador")


def is_analyst() -> bool:
    """True para Técnico y roles de mayor privilegio — análisis avanzado."""
    return _rol() in ("tecnico", "operador", "administrador")


# ── Aliases deprecated — solo para compatibilidad con módulos legacy ─────────
# Eliminar progresivamente en Sprint B

def is_operator() -> bool:
    """DEPRECATED → usar is_operador()"""
    return is_operador()


def is_alcalde() -> bool:
    """DEPRECATED → usar is_ejecutivo()"""
    return is_ejecutivo()
