"""
SENTINEL · state_memory.py
Memoria conversacional de sesión — Sprint 3.
Recuerda: última parroquia · último indicador · último modo de análisis.
Doctrina: continuidad institucional — Sentinel no olvida entre preguntas.
Dylus Lab © 2026
"""
from __future__ import annotations
import unicodedata
import streamlit as st

# ── CATÁLOGOS ──────────────────────────────────────────────────────────────────

_PARROQUIAS_NORM = [
    "montecristi",
    "andres de vera",
    "tabuga",
    "la pila",
    "leonidas plaza",
    "pile",
    "isabel muentes",
]

_PARROQUIA_DISPLAY: dict[str, str] = {
    "montecristi":    "Montecristi",
    "andres de vera": "Andrés de Vera",
    "tabuga":         "Tabuga",
    "la pila":        "La Pila",
    "leonidas plaza": "Leónidas Plaza",
    "pile":           "Pile",
    "isabel muentes": "Isabel Muentes",
}

_INDICADORES: dict[str, list[str]] = {
    "NBI":       ["nbi", "necesidades basicas", "insatisfechas"],
    "inversion": ["inversion per capita", "per capita", "capita", "inversion"],
    "agua":      ["agua", "cobertura agua", "acceso agua"],
    "TPS":       ["tps", "tasa pobreza", "pobreza por servicios"],
    "indices":   ["indices", "indice", "complementarios",
                  "ife", "ied", "igp", "psg", "isp", "itam", "ioc", "iet"],
    "ICGI-T":    ["icgi", "evolucion icgi", "historico icgi"],
}

_MODOS: dict[str, list[str]] = {
    "prospectivo": ["simular", "proyectar", "escenario", "2026", "2027",
                    "meta", "proyeccion", "si subimos", "si aumentamos"],
    "financiero":  ["inversion", "presupuesto", "poa", "pac",
                    "devengado", "ejecucion", "per capita"],
    "territorial": ["parroquia", "nbi", "agua", "tps",
                    "territorio", "cantonal", "rural"],
}

_KEY = "sentinel_memory"


# ── HELPERS ────────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _init() -> None:
    if _KEY not in st.session_state:
        st.session_state[_KEY] = {
            "ultima_parroquia":  None,   # key normalizada
            "ultimo_indicador":  None,   # "NBI" | "inversion" | "agua" | ...
            "ultimo_modo":       None,   # "territorial" | "financiero" | "prospectivo"
            "ultima_query":      "",
            "turno":             0,
        }


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def update_state(query: str) -> None:
    """
    Extrae contexto de la query y actualiza la memoria de sesión.
    Se llama después de procesar cada pregunta (viz o texto).
    """
    _init()
    mem = st.session_state[_KEY]
    q   = _norm(query)

    # Parroquia — mayor especificidad primero (frases antes que palabras sueltas)
    for par in _PARROQUIAS_NORM:
        if par in q:
            mem["ultima_parroquia"] = par
            break

    # Indicador — orden importa: frases compuestas antes de términos simples
    for ind, terms in _INDICADORES.items():
        if any(t in q for t in terms):
            mem["ultimo_indicador"] = ind
            break

    # Modo — prospectivo tiene prioridad si se detecta simulación
    for modo, terms in _MODOS.items():
        if any(t in q for t in terms):
            mem["ultimo_modo"] = modo
            break

    mem["ultima_query"] = query
    mem["turno"] += 1


def get_context() -> dict:
    """Retorna copia del estado actual de memoria."""
    _init()
    return dict(st.session_state[_KEY])


def has_context() -> bool:
    """True si hay al menos una parroquia o indicador en memoria."""
    _init()
    mem = st.session_state[_KEY]
    return bool(mem["ultima_parroquia"] or mem["ultimo_indicador"])


def get_parroquia_key() -> str | None:
    _init()
    return st.session_state[_KEY]["ultima_parroquia"]


def get_parroquia_display() -> str | None:
    key = get_parroquia_key()
    return _PARROQUIA_DISPLAY.get(key) if key else None


def build_context_prompt() -> str:
    """
    Genera un bloque corto para inyectar al system prompt de Groq.
    Provee continuidad institucional entre preguntas de seguimiento.
    """
    _init()
    if not has_context():
        return ""

    mem = st.session_state[_KEY]
    lines = ["CONTEXTO CONVERSACIÓN ACTIVA (mantener si la query es ambigua):"]

    if mem["ultima_parroquia"]:
        display = _PARROQUIA_DISPLAY.get(mem["ultima_parroquia"],
                                         mem["ultima_parroquia"].title())
        lines.append(f"  Última parroquia analizada: {display}")

    if mem["ultimo_indicador"]:
        lines.append(f"  Último indicador consultado: {mem['ultimo_indicador']}")

    if mem["ultimo_modo"]:
        lines.append(f"  Modo activo: {mem['ultimo_modo']}")

    lines.append(
        "  Si el usuario hace una pregunta de seguimiento sin mencionar territorio "
        "o indicador, responde en el contexto de los valores anteriores. "
        "No empieces desde cero."
    )
    return "\n".join(lines)


def reset() -> None:
    """Limpia toda la memoria de sesión. Llamar al limpiar la conversación."""
    if _KEY in st.session_state:
        del st.session_state[_KEY]
