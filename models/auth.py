"""
QUIRA Intelligence — Model: Auth  (Seguridad v3 · Nomenclatura canónica 2026-05-27)
Capa de autenticación segura:
  · Contraseñas hasheadas PBKDF2-SHA256 — nunca texto plano
  · Credenciales en st.secrets (producción) o variables de entorno (dev)
  · Rate limiting: bloqueo tras 3 intentos fallidos por 5 minutos
  · Expiración de sesión: logout automático a los 60 minutos

Roles CONGELADOS (ver docs/NOMENCLATURA_CANONICA.md):
  ejecutivo    — Alcalde, concejales, director ejecutivo → GOV (vista ejecutiva)
  tecnico      — Directivo de planificación → GOV (vista técnica)
  operador     — Equipo Dylus Lab (operación) → OPS
  administrador— Equipo Dylus Lab (admin total) → OPS + GOV verificación

ELIMINADOS DEFINITIVAMENTE: viewer / analyst / operator / admin (inglés v1-v2)
No usar. No recuperar. No reintroducir.

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

# Salt fijo de la aplicación
_APP_SALT = b"QUIRA_OS_v1_Dylus_Lab_2026"

# ── Constantes de roles (usar estas, nunca strings literales en código) ───────
ROLE_EJECUTIVO     = "ejecutivo"
ROLE_TECNICO       = "tecnico"
ROLE_OPERADOR      = "operador"
ROLE_ADMINISTRADOR = "administrador"


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
# En Streamlit Cloud → Settings → Secrets → TOML:
#   [auth]
#   ejecutivo_hash     = "<resultado de _hash('tu_password')>"
#   tecnico_hash       = "<resultado de _hash('tu_password')>"
#   operador_hash      = "<resultado de _hash('tu_password')>"
#   administrador_hash = "<resultado de _hash('tu_password')>"

# ⛔ FALLBACK ELIMINADO — 2026-08-05, tras reporte de acceso no autorizado (Javo).
#
# Aquí vivía `_FALLBACK_HASHES`, con el hash de una contraseña ESCRITA EN TEXTO PLANO en
# este mismo archivo, idéntica para los cuatro roles. Y `_stored_hash` caía en ella con un
# `except Exception` amplio: bastaba que la lectura de secrets fallara por cualquier motivo
# —sección ausente, error de red, typo en el panel— para que la aplicación aceptara una
# contraseña que cualquiera con acceso al repositorio podía leer. Diseño FAIL-OPEN.
#
# Ahora es FAIL-CLOSED: sin secretos configurados no se autentica a nadie. Un despliegue
# mal configurado queda inaccesible, que es el comportamiento correcto — nunca abierto.
# Para desarrollo local, configurar `.streamlit/secrets.toml` (no se rastrea en git).

_USER_META: dict[str, dict] = {
    ROLE_EJECUTIVO:     {"rol": "Ejecutivo",     "emoji": "🏛"},
    ROLE_TECNICO:       {"rol": "Directivo",       "emoji": "📐"},
    ROLE_OPERADOR:      {"rol": "Operador",       "emoji": "⚙️"},
    ROLE_ADMINISTRADOR: {"rol": "Administrador",  "emoji": "🔑"},
}


def _stored_hash(rol_key: str) -> str:
    """Hash almacenado para el rol, o cadena vacía si no hay credencial configurada.

    Devolver "" hace que `validate` rechace SIEMPRE (ver `if not stored`): sin secretos,
    nadie entra. Es deliberado — la versión anterior devolvía aquí un hash de respaldo con
    contraseña conocida, y ese era el agujero."""
    try:
        return st.secrets["auth"][f"{rol_key}_hash"] or ""
    except Exception:
        return ""


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
    """True si la sesión superó los 60 minutos."""
    login_time = st.session_state.get("login_time", 0)
    return login_time > 0 and (time.time() - login_time) > _SESSION_SECS


def rol_options() -> dict[str, str]:
    """Opciones para el dropdown de login. Display → key interno."""
    return {
        "🏛 Ejecutivo":      ROLE_EJECUTIVO,
        "📐 Directivo":     ROLE_TECNICO,
        "⚙️ Operador":      ROLE_OPERADOR,
        "🔑 Administrador": ROLE_ADMINISTRADOR,
    }


def validate_any(password: str) -> AuthUser:
    """
    Valida la contraseña contra todos los roles — el sistema detecta el rol.
    Orden de prueba: ejecutivo → tecnico → operador → administrador.
    En producción, cada rol tiene un hash único; el primero que coincida es el rol.

    Desde 2026-08-05 cada rol tiene credencial PROPIA y no hay hash de respaldo:
    si un rol no está configurado en secrets, simplemente nunca coincide.

    Lanza LockedError si está bloqueado, AuthError si ningún rol coincide.
    """
    locked, secs = is_locked()
    if locked:
        raise LockedError(secs)

    pw_hash = _hash(password)
    for rol_key in (ROLE_EJECUTIVO, ROLE_TECNICO, ROLE_OPERADOR, ROLE_ADMINISTRADOR):
        stored = _stored_hash(rol_key)
        if stored and _safe_eq(pw_hash, stored):
            # Login exitoso — resetear contadores
            st.session_state[_tries_key()] = 0
            st.session_state[_lock_key()]  = 0
            meta = _USER_META.get(rol_key, {})
            return AuthUser(
                key=rol_key,
                rol=meta.get("rol", rol_key),
                emoji=meta.get("emoji", ""),
            )

    # Contraseña no coincide con ningún rol
    tries = st.session_state.get(_tries_key(), 0) + 1
    st.session_state[_tries_key()] = tries
    if tries >= _MAX_ATTEMPTS:
        st.session_state[_lock_key()]  = time.time() + _LOCKOUT_SECS
        st.session_state[_tries_key()] = 0
        raise LockedError(_LOCKOUT_SECS)
    raise AuthError(f"Contraseña incorrecta ({tries}/{_MAX_ATTEMPTS} intentos)")
