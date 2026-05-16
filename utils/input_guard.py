"""
QUIRA OS — Input Guard (Día 5 Sprint Security)
Sanitización y validación de todos los inputs de usuario antes de procesar.
Protege contra:
  - prompt injection al LLM
  - inputs gigantes que explotan context window
  - caracteres de control y patrones de evasión
Dylus Lab © 2026
"""
from __future__ import annotations
import re
import time
import unicodedata

import streamlit as st

_MAX_QUERY_LEN   = 800   # caracteres máximos para consultas a Sentinel
_MAX_FIELD_LEN   = 120   # campos cortos
_QPM_LIMIT       = 10    # consultas por minuto por usuario
_QPM_WINDOW      = 60    # ventana de medición en segundos

# Patrones de prompt injection — inglés y español
_INJECTION_PATTERNS = [
    # ── Inglés clásico ──────────────────────────────────────────────────────────
    r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions?",
    r"forget\s+(?:all\s+)?(?:previous|prior|above)",
    r"you\s+are\s+now\s+(?:a\s+)?(?:different|new|another)",
    r"act\s+as\s+(?:an?\s+)?(?:unrestricted|jailbroken|evil|dan|dán)",
    r"system\s*prompt\s*:",
    r"\[system\]",
    r"<\s*system\s*>",
    # ### override/reset — segunda palabra ahora opcional
    r"###\s*(?:new|reset|override|ignore)(?:\s+\w+)*",
    # ── Extracción de conocimiento interno ──────────────────────────────────────
    r"(?:muestra|revela|dime|dame|show|reveal)\s+(?:tus?|your|los?)\s*(?:pesos?|coeficientes?|f[oó]rmulas?|weights?|params?|internos?)",
    r"(?:pesos?|coeficientes?)\s+internos?\s+del\s+(?:modelo|icgi|irs|cbst)",
    # ── Español — ignora + objeto con palabras intermedias ──────────────────────
    r"ignora[r]?\b[\w\s]{0,30}\b(?:instrucciones?|restricciones?|pol[ií]ticas?|anteriores?)",
    # ── Español — actúa / responde como + rol no autorizado ────────────────────
    r"act[uú]a[r]?\s+como\s+(?:\w+\s+){0,3}(?:admin|asesor|jefe|director|consultor|sin\s+restricciones?)",
    r"responde\s+como\s+(?:asesor|consultor|experto|agente|pol[ií]tico|externo)",
    # ── Español — revelar / ignorar ─────────────────────────────────────────────
    r"revelar?\s+(?:instrucciones?|prompt|sistema|secretos?|configuraci[oó]n|pesos?)",
    r"nuevo\s+rol\s*:",
    r"eres?\s+(?:ahora\s+)?(?:un|una)\s+(?:asistente\s+)?(?:sin\s+restricciones?|malicioso|hacke)",
]
_INJECTION_RE = re.compile(
    "|".join(_INJECTION_PATTERNS),
    flags=re.IGNORECASE | re.UNICODE,
)


def sanitize_query(text: str) -> str:
    """
    Limpia y valida una consulta de usuario para el LLM.
    Raises ValueError si detecta intent de inyección.
    Retorna el texto limpio y truncado.
    """
    if not isinstance(text, str):
        return ""

    # 1. Normalizar unicode (NFKC colapsa homoglifos)
    text = unicodedata.normalize("NFKC", text)

    # 2. Eliminar caracteres de control (excluye \n \t que son legítimos)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # 3. Detectar prompt injection
    if _INJECTION_RE.search(text):
        raise ValueError("Input bloqueado: contiene patrones de instrucción no autorizados.")

    # 4. Truncar a límite seguro
    if len(text) > _MAX_QUERY_LEN:
        text = text[:_MAX_QUERY_LEN]

    return text.strip()


def sanitize_field(text: str) -> str:
    """Para campos cortos (passwords ya van por hash, esto es para otros inputs)."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    return text[:_MAX_FIELD_LEN].strip()


def is_safe_query(text: str) -> tuple[bool, str]:
    """
    Versión no-raising para usar en condicionales.
    Retorna (True, texto_limpio) o (False, motivo_del_bloqueo).
    """
    try:
        clean = sanitize_query(text)
        return True, clean
    except ValueError as e:
        return False, str(e)


def check_rate_limit() -> tuple[bool, str]:
    """
    Rate limiting por usuario: máximo _QPM_LIMIT consultas en _QPM_WINDOW segundos.
    Usa session_state para no necesitar backend — funciona en Streamlit Cloud.
    Retorna (permitido, mensaje_de_error).
    """
    now  = time.time()
    key  = "_sentinel_query_times"
    times: list[float] = st.session_state.get(key, [])

    # Descartar timestamps fuera de la ventana
    times = [t for t in times if now - t < _QPM_WINDOW]

    if len(times) >= _QPM_LIMIT:
        espera = int(_QPM_WINDOW - (now - times[0])) + 1
        return False, f"Máximo {_QPM_LIMIT} consultas por minuto. Intenta en {espera}s."

    times.append(now)
    st.session_state[key] = times
    return True, ""
