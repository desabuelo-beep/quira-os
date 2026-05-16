"""
QUIRA OS — Audit Logger
Registro institucional de accesos, consultas y actividad crítica.
Formato: NDJSON (una entrada JSON por línea) → fácil de ingerir en cualquier SIEM.

NUNCA subir logs/ a Git. El .gitignore ya protege ese directorio.
Dylus Lab © 2026
"""
from __future__ import annotations
import datetime
import json
import os

import streamlit as st

_LOG_DIR  = "logs"
_LOG_FILE = os.path.join(_LOG_DIR, "audit.log")


def _ts() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _session_user() -> str:
    return st.session_state.get("usuario", "—")


def _session_rol() -> str:
    return st.session_state.get("rol", "—")


def _write(entry: dict) -> None:
    try:
        os.makedirs(_LOG_DIR, exist_ok=True)
        entry["sid"] = st.session_state.get("session_id", "—")
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError:
        pass  # nunca romper el flujo de la app por un fallo de log


# ── Eventos de autenticación ──────────────────────────────────────────────────

def log_login_ok(usuario: str) -> None:
    _write({"ts": _ts(), "event": "LOGIN_OK",     "usuario": usuario})


def log_login_fail(usuario: str, motivo: str = "") -> None:
    _write({"ts": _ts(), "event": "LOGIN_FAIL",   "usuario": usuario, "motivo": motivo})


def log_lockout(usuario: str) -> None:
    _write({"ts": _ts(), "event": "LOCKOUT",      "usuario": usuario})


def log_logout(usuario: str, motivo: str = "manual") -> None:
    _write({"ts": _ts(), "event": "LOGOUT",       "usuario": usuario, "motivo": motivo})


# ── Navegación ────────────────────────────────────────────────────────────────

def log_page(page: str) -> None:
    _write({
        "ts":      _ts(),
        "event":   "PAGE_VIEW",
        "usuario": _session_user(),
        "rol":     _session_rol(),
        "page":    page,
    })


# ── Sentinel ──────────────────────────────────────────────────────────────────

def log_sentinel_query(module: str, query_len: int, score: str = "") -> None:
    """Loguea la consulta sin almacenar el texto completo (privacidad)."""
    _write({
        "ts":        _ts(),
        "event":     "SENTINEL_QUERY",
        "usuario":   _session_user(),
        "rol":       _session_rol(),
        "module":    module,
        "query_len": query_len,
        "score":     score,
    })


def log_escalamiento(module: str, action: str) -> None:
    _write({
        "ts":      _ts(),
        "event":   "ESCALAMIENTO",
        "usuario": _session_user(),
        "rol":     _session_rol(),
        "module":  module,
        "action":  action,
    })
