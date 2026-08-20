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
import logging
import os

import streamlit as st

_LOG_DIR  = "logs"
_LOG_FILE = os.path.join(_LOG_DIR, "audit.log")

_log = logging.getLogger(__name__)


def _ts() -> str:
    return datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _session_user() -> str:
    return st.session_state.get("usuario", "—")


def _session_rol() -> str:
    return st.session_state.get("rol", "—")


#: Fallos de escritura acumulados en esta sesión. Este registro es la traza de
#: ACCESOS —entradas, intentos fallidos, bloqueos—: si deja de escribirse sin
#: que nadie lo note, un acceso no autorizado no dejaría huella, que es
#: precisamente lo que se necesitaría para detectarlo.
_fallos_escritura = 0


def fallos_de_escritura() -> int:
    """Cuántas veces no se pudo escribir la bitácora en esta sesión."""
    return _fallos_escritura


def _write(entry: dict) -> None:
    try:
        os.makedirs(_LOG_DIR, exist_ok=True)
        entry["sid"] = st.session_state.get("session_id", "—")
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as e:
        # Se mantiene el criterio de no romper el flujo por un fallo de
        # bitácora, pero NO el silencio. Se avisa por el canal de registro del
        # sistema —nunca a este mismo archivo, que es el que está fallando— y
        # se cuenta, para que la pérdida de traza sea visible.
        global _fallos_escritura
        _fallos_escritura += 1
        _log.error("no se pudo escribir la bitácora de accesos (%s): %s — "
                   "van %d fallo(s); el evento «%s» NO quedó registrado",
                   type(e).__name__, e, _fallos_escritura,
                   entry.get("event", "?"))


# ── Llegada al portal · antes de autenticarse ─────────────────────────────────
# POR QUÉ (2026-08-18). Javo, tras publicar el landing: *«están ingresando a QUIRA
# y no sé quiénes ni cómo»*. La bitácora sólo empezaba en el LOGIN, de modo que
# todo el tráfico que llega a la puerta y no entra era invisible — y es
# justamente el que interesa cuando se acaba de publicar en una red.
#
# SE REGISTRA LA PROCEDENCIA, NO A LA PERSONA. Ni IP, ni huella de navegador, ni
# identificador persistente: sólo de dónde viene el enlace (UTM) y qué sesión
# anónima abrió. Un sistema que audita transparencia pública no puede rastrear a
# quien lo visita — y menos con herramientas de terceros. La analítica externa se
# descartó por eso y porque enviaría el dato fuera del control de Dylus Lab.

def log_landing(utm: dict | None = None) -> None:
    """Una llegada al portal público. Se llama UNA vez por sesión."""
    if st.session_state.get("_landing_registrado"):
        return
    st.session_state["_landing_registrado"] = True
    u = {k: v for k, v in (utm or {}).items() if v}
    _write({"ts": _ts(), "event": "LANDING",
            "origen": u.get("utm_source", "directo"),
            "campana": u.get("utm_campaign", "—"),
            "medio": u.get("utm_medium", "—")})


def leer_utm(params) -> dict:
    """Extrae los parámetros de campaña del enlace (`?utm_source=linkedin`).

    Sólo lee las cinco claves estándar y descarta el resto: un parámetro
    arbitrario en la URL no debe acabar en la bitácora."""
    permitidas = ("utm_source", "utm_medium", "utm_campaign",
                  "utm_content", "utm_term")
    try:
        return {k: str(params.get(k, ""))[:40] for k in permitidas
                if params.get(k)}
    except Exception:                                    # noqa: BLE001
        return {}


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
