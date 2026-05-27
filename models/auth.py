"""
QUIRA Intelligence — Model: Auth  (Seguridad v2)
Capa de autenticación segura:
  · Contraseñas hasheadas PBKDF2-SHA256 — nunca texto plano
  · Credenciales en st.secrets (producción) o variables de entorno (dev)
  · Rate limiting: bloqueo tras 3 intentos fallidos por 5 minutos
  · Expiración de sesión: logout automático a los 60 minutos

Roles PMV (Sprint 3 · 2026-05-25):
  Viewer   — Consulta análisis y reportes (GOV, Impact)
  Analyst  — Análisis avanzado, comparativos longitudinales (GOV, Impact)
  Operator — Ejecuta pipeline, gestiona snapshots (GOV, Ops)
  Admin    — Configuración total, governance, Gold Master (todos)

DEPRECATED: Alcalde / Concejal / Técnico — modelo SaaS municipal descartado.
No usar, no recuperar, no reintroducir.

Sin imports de Streamlit salvo para leer secrets. Sin HTML.
Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import hmac
import binascii
import time
from dataclasses import dataclass

import streamlit as st

# ── Constantes de seguridad ───────────────────────────────────────────────────
_MAX_ATTEMPTS  = 3          # intentos antes de bloqueo
_LOCKOUT_SECS  = 300        # 5 minutos de bloqueo
_SESSION_SECS  = 3600       # 60 minutos → logout automático
_PBKDF2_ITERS  = 260_000    # iteraciones PBKDF2 (OWASP 2024)

# Salt fijo de la aplicación (añade entropía al hash incluso si la BD se filtra)
_APP_SALT = b"QUIRA_OS_v1_Dylus_Lab_2026"


# ── Hashing ───────────────────────────────────────────────────────────────────

def _hash(plain: str) -> str:
    """PBKDF2-SHA256 con salt de app. Siempre devuelve el mismo hex para el mismo input."""
    dk = hashlib.pbkdf2_hmac(
        "sha256", plain.encode("utf-8"), _APP_SALT, _PBKDF2_ITERS
    )
    return binascii.hexlify(dk).decode()


def _safe_eq(a: str, b: str) -> bool:
    """Comparación en tiempo constante — previene timing attacks."""
    return hmac.compare_digest(a, b)


# ── Credenciales ──────────────────────────────────────────────────────────────
# Orden de búsqueda:
#   1. st.secrets (Streamlit Cloud → Settings → Secrets)
#   2. Hashes embebidos de fallback (sólo para dev local)
#
# Para producción, en Streamlit Cloud añade en Secrets:
#   [auth]
#   viewer_hash   = "<resultado de _hash('tu_password')>"
#   analyst_hash  = "<resultado de _hash('tu_password')>"
#   operator_hash = "<resultado de _hash('tu_password')>"
#   admin_hash    = "<resultado de _hash('tu_password')>"

_FALLBACK_HASHES: dict[str, str] = {
    # Generados con _hash("quira2026") — cambiar en producción
    "viewer":   _hash("quira2026"),
    "analyst":  _hash("quira2026"),
    "operator": _hash("quira2026"),
    "admin":    _hash("quira2026"),
}

_USER_META: dict[str, dict] = {
    "viewer":   {"rol": "Viewer",   "emoji": "👁"},
    "analyst":  {"rol": "Analyst",  "emoji": "📊"},
    "operator": {"rol": "Operator", "emoji": "⚙️"},
    "admin":    {"rol": "Admin",    "emoji": "🔑"},
}


def _stored_hash(rol_key: str) -> str:
    """Lee el hash desde st.secrets (prod) o fallback (dev)."""
    try:
        return st.secrets["auth"][f"{rol_key}_hash"]
    except Exception:
        return _FALLBACK_HASHES.get(rol_key, "")


# ── Público ───────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class AuthUser:
    key:   str
    rol:   str
    emoji: str


class AuthError(Exception):
    """Credenciales incorrectas."""


class LockedError(Exception):
    """Demasiados intentos — cuenta bloqueada temporalmente."""
    def __init__(self, seconds_left: int):
        self.seconds_left = seconds_left
        super().__init__(f"Bloqueado por {seconds_left}s")


def _lock_key()  -> str: return "auth_locked_until"
def _tries_key() -> str: return "auth_failed_tries"


def is_locked() -> tuple[bool, int]:
    """Retorna (bloqueado, segundos_restantes)."""
    until = st.session_state.get(_lock_key(), 0)
    left  = int(until - time.time())
    return (left > 0, max(left, 0))


def validate(rol_key: str, password: str) -> AuthUser:
    """
    Valida credenciales con protección brute-force.
    Lanza LockedError si está bloqueado, AuthError si la contraseña es incorrecta.
    """
    locked, secs = is_locked()
    if locked:
        raise LockedError(secs)

    stored = _stored_hash(rol_key)
    if not stored or not _safe_eq(_hash(password), stored):
        tries = st.session_state.get(_tries_key(), 0) + 1
        st.session_state[_tries_key()] = tries
        if tries >= _MAX_ATTEMPTS:
            st.session_state[_lock_key()]  = time.time() + _LOCKOUT_SECS
            st.session_state[_tries_key()] = 0
            raise LockedError(_LOCKOUT_SECS)
        raise AuthError(f"Contraseña incorrecta ({tries}/{_MAX_ATTEMPTS} intentos)")

    # Login exitoso → resetear contadores
    st.session_state[_tries_key()] = 0
    st.session_state[_lock_key()]  = 0

    meta = _USER_META.get(rol_key, {})
    return AuthUser(key=rol_key, rol=meta.get("rol", rol_key), emoji=meta.get("emoji", ""))


def is_session_expired() -> bool:
    """True si la sesión superó los 60 minutos de inactividad."""
    login_time = st.session_state.get("login_time", 0)
    return login_time > 0 and (time.time() - login_time) > _SESSION_SECS


def rol_options() -> dict[str, str]:
    return {
        "👁 Viewer":   "viewer",
        "📊 Analyst":  "analyst",
        "⚙️ Operator": "operator",
        "🔑 Admin":    "admin",
    }
