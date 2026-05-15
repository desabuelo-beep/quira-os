"""
SENTINEL · audit.py
Registro de cada interacción: pregunta, herramienta usada, fuente, confianza.
Formato: JSONL — una línea por interacción.
Ruta: logs/sentinel_audit.jsonl
Dylus Lab © 2026
"""
from __future__ import annotations
import json
import os
import datetime

_AUDIT_DIR  = os.path.join(os.path.dirname(__file__), "..", "logs")
_AUDIT_FILE = os.path.join(_AUDIT_DIR, "sentinel_audit.jsonl")


def log_interaction(
    pregunta:  str,
    respuesta: str,
    tool_usado:  str | None  = None,
    confianza:   str          = "media",
    fuente:      str          = "H73_OUTPUT_API / H99_ENGINE_CORE",
    modo_seguro: bool         = False,
    pagina_origen: str | None = None,
) -> None:
    """
    Registra una interacción en el log de auditoría.

    Args:
        pregunta:      Texto de la pregunta del usuario (max 500 chars logged)
        respuesta:     Texto de la respuesta (max 300 chars logged)
        tool_usado:    Nombre de la herramienta invocada (get_indicator, etc.)
        confianza:     "alta" | "media" | "baja" | "modo_seguro"
        fuente:        Identificador del conjunto de datos fuente
        modo_seguro:   True si Sentinel activó modo cauteloso
        pagina_origen: page_key desde donde se originó la pregunta
    """
    try:
        os.makedirs(_AUDIT_DIR, exist_ok=True)
        entry = {
            "ts":            datetime.datetime.now().isoformat(),
            "pregunta":      pregunta[:500],
            "respuesta_ok":  bool(respuesta and "error" not in respuesta.lower()[:50]),
            "respuesta_len": len(respuesta),
            "tool_usado":    tool_usado,
            "confianza":     "modo_seguro" if modo_seguro else confianza,
            "fuente":        fuente,
            "pagina_origen": pagina_origen,
        }
        with open(_AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # Audit failures must never crash the main flow


def read_audit_log(last_n: int = 20) -> list[dict]:
    """
    Lee las últimas N entradas del audit log.

    Args:
        last_n: Número de entradas más recientes a retornar.

    Returns:
        Lista de dicts (última entrada = último elemento)
    """
    try:
        if not os.path.exists(_AUDIT_FILE):
            return []
        with open(_AUDIT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        entries = []
        for line in lines[-last_n:]:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                pass
        return entries
    except Exception:
        return []


def get_audit_stats() -> dict:
    """
    Estadísticas básicas del audit log (para el panel técnico).
    """
    entries = read_audit_log(last_n=500)
    if not entries:
        return {"total": 0, "con_tool": 0, "modo_seguro": 0, "ok_pct": 0.0}

    con_tool    = sum(1 for e in entries if e.get("tool_usado"))
    modo_seguro = sum(1 for e in entries if e.get("confianza") == "modo_seguro")
    ok          = sum(1 for e in entries if e.get("respuesta_ok", False))

    return {
        "total":       len(entries),
        "con_tool":    con_tool,
        "modo_seguro": modo_seguro,
        "ok_pct":      round(ok / len(entries) * 100, 1),
        "ultima_ts":   entries[-1].get("ts", "—"),
    }
