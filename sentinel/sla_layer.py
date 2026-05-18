"""
SENTINEL RAG · sla_layer.py
Sprint 2.3 — Institutional SLA Layer.

Cada caso de gobernanza tiene un SLA con owner y deadline.
Sin SLA, la gobernanza se convierte en burocracia digital.

Estados automáticos por tiempo transcurrido:
    0–24h   → NORMAL   🟢
    24–48h  → SEGUIMIENTO 🟡
    48–72h  → CRITICO  🟠
    >72h    → VENCIDO  🔴

Prioridad institucional:
    alta    → max_resolution_hours = 24
    media   → max_resolution_hours = 48
    baja    → max_resolution_hours = 72

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Optional

from sentinel.rag_config import LOGS_DIR, SENTINEL_VERSION

# ── RUTA ──────────────────────────────────────────────────────────────────────
SLA_LOG = LOGS_DIR / "governance_sla.jsonl"
SLA_LOG.parent.mkdir(parents=True, exist_ok=True)

# ── DEFAULTS ──────────────────────────────────────────────────────────────────
SLA_HOURS_BY_PRIORITY = {
    "alta":  24,
    "media": 48,
    "baja":  72,
}
SLA_DEFAULT_OWNER    = "coordinador_planificacion"
SLA_DEFAULT_PRIORITY = "media"


# ── ENUMS ─────────────────────────────────────────────────────────────────────
class SlaStatus(str, Enum):
    NORMAL      = "NORMAL"
    SEGUIMIENTO = "SEGUIMIENTO"
    CRITICO     = "CRITICO"
    VENCIDO     = "VENCIDO"
    CUMPLIDO    = "CUMPLIDO"  # caso cerrado dentro del SLA


class Priority(str, Enum):
    ALTA  = "alta"
    MEDIA = "media"
    BAJA  = "baja"


# ── DATACLASS ─────────────────────────────────────────────────────────────────
@dataclass
class CaseSLA:
    """
    SLA institucional de un caso de gobernanza.

    Campos:
        case_id              — ID del caso (misma clave que GovernanceCase)
        decision_ts          — Timestamp de la decisión original
        pregunta             — Pregunta (para trazabilidad)
        owner                — Responsable institucional del SLA
        priority             — alta | media | baja
        max_resolution_hours — Horas máximas para resolución
        opened_at            — Timestamp ISO de apertura del SLA
        deadline             — Timestamp ISO de vencimiento
        closed_at            — Timestamp ISO de cierre (si aplica)
        status               — Estado SLA calculado dinámicamente
        sentinel_version     — Versión de Sentinel al crear el SLA
    """
    case_id:              str
    decision_ts:          str
    pregunta:             str
    owner:                str
    priority:             str
    max_resolution_hours: int
    opened_at:            str
    deadline:             str
    closed_at:            str = ""
    status:               str = SlaStatus.NORMAL.value
    sentinel_version:     str = SENTINEL_VERSION


# ── CÁLCULO DE ESTADO ─────────────────────────────────────────────────────────
def _compute_sla_status(sla: CaseSLA) -> SlaStatus:
    """Calcula el estado SLA en función del tiempo transcurrido."""
    if sla.closed_at:
        return SlaStatus.CUMPLIDO

    import datetime

    try:
        opened = datetime.datetime.fromisoformat(sla.opened_at)
        now    = datetime.datetime.now()
        elapsed_h = (now - opened).total_seconds() / 3600
        max_h     = sla.max_resolution_hours
    except Exception:
        return SlaStatus.NORMAL

    if elapsed_h >= max_h:
        return SlaStatus.VENCIDO
    elif elapsed_h >= max_h * 0.667:   # >66%  del tiempo → CRITICO
        return SlaStatus.CRITICO
    elif elapsed_h >= max_h * 0.333:   # >33%  del tiempo → SEGUIMIENTO
        return SlaStatus.SEGUIMIENTO
    else:
        return SlaStatus.NORMAL


def _hours_remaining(sla: CaseSLA) -> float:
    """Horas restantes para el vencimiento del SLA."""
    if sla.closed_at:
        return 0.0
    import datetime
    try:
        opened    = datetime.datetime.fromisoformat(sla.opened_at)
        now       = datetime.datetime.now()
        elapsed_h = (now - opened).total_seconds() / 3600
        return max(0.0, sla.max_resolution_hours - elapsed_h)
    except Exception:
        return float(sla.max_resolution_hours)


def _deadline_from(opened_at: str, max_hours: int) -> str:
    """Calcula el deadline ISO a partir de opened_at y max_hours."""
    import datetime
    try:
        opened = datetime.datetime.fromisoformat(opened_at)
        dl     = opened + datetime.timedelta(hours=max_hours)
        return dl.strftime("%Y-%m-%dT%H:%M:%S")
    except Exception:
        return ""


# ── PERSISTENCIA ──────────────────────────────────────────────────────────────
def _append_sla(sla: CaseSLA) -> None:
    entry = asdict(sla)
    with SLA_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _load_all_sla() -> dict[str, dict]:
    """Carga todos los SLA del log (latest-wins por case_id)."""
    if not SLA_LOG.exists():
        return {}
    slas: dict[str, dict] = {}
    with SLA_LOG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                slas[entry["case_id"]] = entry
            except (json.JSONDecodeError, KeyError):
                continue
    return slas


# ── API PRINCIPAL ─────────────────────────────────────────────────────────────
def create_sla(
    case_id:    str,
    decision_ts: str,
    pregunta:   str,
    owner:      str       = SLA_DEFAULT_OWNER,
    priority:   str       = SLA_DEFAULT_PRIORITY,
) -> CaseSLA:
    """
    Crea un SLA para un caso de gobernanza.

    Args:
        case_id     — ID del caso de gobernanza
        decision_ts — Timestamp de la decisión original
        pregunta    — Pregunta para trazabilidad
        owner       — Responsable institucional del SLA
        priority    — alta (24h) | media (48h) | baja (72h)

    Returns:
        CaseSLA persistido.
    """
    if isinstance(priority, Priority):
        priority = priority.value

    priority       = priority.lower()
    max_hours      = SLA_HOURS_BY_PRIORITY.get(priority, 48)
    opened_at      = time.strftime("%Y-%m-%dT%H:%M:%S")
    deadline       = _deadline_from(opened_at, max_hours)

    sla = CaseSLA(
        case_id              = case_id,
        decision_ts          = decision_ts,
        pregunta             = pregunta,
        owner                = owner,
        priority             = priority,
        max_resolution_hours = max_hours,
        opened_at            = opened_at,
        deadline             = deadline,
        status               = SlaStatus.NORMAL.value,
    )
    _append_sla(sla)
    return sla


def close_sla(case_id: str) -> Optional[CaseSLA]:
    """
    Marca el SLA de un caso como CUMPLIDO (cierre dentro del deadline).
    """
    slas = _load_all_sla()
    if case_id not in slas:
        return None

    raw  = slas[case_id]
    sla  = CaseSLA(**{k: raw.get(k, "") for k in CaseSLA.__dataclass_fields__})
    sla.closed_at = time.strftime("%Y-%m-%dT%H:%M:%S")
    sla.status    = SlaStatus.CUMPLIDO.value
    _append_sla(sla)
    return sla


def get_sla(case_id: str) -> Optional[dict]:
    """Retorna el SLA de un caso, con estado calculado en tiempo real."""
    slas = _load_all_sla()
    if case_id not in slas:
        return None

    raw = slas[case_id]
    sla = CaseSLA(**{k: raw.get(k, "") for k in CaseSLA.__dataclass_fields__})

    # Recalcular estado en tiempo real
    sla.status = _compute_sla_status(sla).value

    result = asdict(sla)
    result["horas_restantes"] = round(_hours_remaining(sla), 1)
    result["status_icon"] = {
        "NORMAL":      "🟢",
        "SEGUIMIENTO": "🟡",
        "CRITICO":     "🟠",
        "VENCIDO":     "🔴",
        "CUMPLIDO":    "✅",
    }.get(sla.status, "•")
    return result


def get_all_slas(include_closed: bool = False) -> list[dict]:
    """
    Retorna todos los SLA con estado calculado en tiempo real.
    Ordenados: VENCIDO → CRITICO → SEGUIMIENTO → NORMAL → CUMPLIDO.
    """
    slas = _load_all_sla()
    result = []

    for raw in slas.values():
        sla = CaseSLA(**{k: raw.get(k, "") for k in CaseSLA.__dataclass_fields__})
        status = _compute_sla_status(sla)

        if not include_closed and status == SlaStatus.CUMPLIDO:
            continue

        entry = asdict(sla)
        entry["status"]          = status.value
        entry["horas_restantes"] = round(_hours_remaining(sla), 1)
        entry["status_icon"]     = {
            "NORMAL":      "🟢",
            "SEGUIMIENTO": "🟡",
            "CRITICO":     "🟠",
            "VENCIDO":     "🔴",
            "CUMPLIDO":    "✅",
        }.get(status.value, "•")
        result.append(entry)

    # Ordenar por urgencia
    order = {"VENCIDO": 0, "CRITICO": 1, "SEGUIMIENTO": 2, "NORMAL": 3, "CUMPLIDO": 4}
    result.sort(key=lambda s: order.get(s["status"], 9))
    return result


def get_sla_summary() -> dict:
    """
    Resumen estadístico de todos los SLA activos.
    Útil para el bloque D del HOME (Estado Sentinel).
    """
    all_slas = get_all_slas(include_closed=True)
    total    = len(all_slas)
    vencidos = sum(1 for s in all_slas if s["status"] == "VENCIDO")
    criticos = sum(1 for s in all_slas if s["status"] == "CRITICO")
    seguimiento = sum(1 for s in all_slas if s["status"] == "SEGUIMIENTO")
    normales = sum(1 for s in all_slas if s["status"] == "NORMAL")
    cumplidos = sum(1 for s in all_slas if s["status"] == "CUMPLIDO")

    alerta = vencidos > 0 or criticos > 0

    return {
        "total":       total,
        "vencidos":    vencidos,
        "criticos":    criticos,
        "seguimiento": seguimiento,
        "normales":    normales,
        "cumplidos":   cumplidos,
        "alerta":      alerta,
        "alerta_icon": "🔴" if vencidos > 0 else ("🟠" if criticos > 0 else "🟢"),
    }


def update_sla_owner(case_id: str, new_owner: str) -> Optional[dict]:
    """Actualiza el owner de un SLA (para reasignación institucional)."""
    slas = _load_all_sla()
    if case_id not in slas:
        return None

    raw = slas[case_id]
    sla = CaseSLA(**{k: raw.get(k, "") for k in CaseSLA.__dataclass_fields__})
    sla.owner  = new_owner
    sla.status = _compute_sla_status(sla).value
    _append_sla(sla)
    return get_sla(case_id)


# ── FORMATO CONSOLA ───────────────────────────────────────────────────────────
def format_sla(sla_dict: dict) -> str:
    """Formato legible de un SLA para consola."""
    icon = sla_dict.get("status_icon", "•")
    lines = [
        "-" * 58,
        f"  SLA {sla_dict.get('case_id', '?')}  {icon} {sla_dict.get('status', '?')}",
        "-" * 58,
        f"  Owner    : {sla_dict.get('owner', '?')}",
        f"  Prioridad: {sla_dict.get('priority', '?')} ({sla_dict.get('max_resolution_hours', '?')}h)",
        f"  Abierto  : {sla_dict.get('opened_at', '?')}",
        f"  Deadline : {sla_dict.get('deadline', '?')}",
        f"  Restantes: {sla_dict.get('horas_restantes', '?')}h",
        f"  Pregunta : {sla_dict.get('pregunta', '')[:65]}",
        "-" * 58,
    ]
    return "\n".join(lines)


def format_sla_summary(summary: dict) -> str:
    """Formato del resumen SLA para consola."""
    lines = [
        "=" * 58,
        "  SENTINEL · SLA Summary",
        "=" * 58,
        f"  Total SLA    : {summary['total']}",
        f"  Vencidos     : {summary['vencidos']}  🔴",
        f"  Criticos     : {summary['criticos']}  🟠",
        f"  Seguimiento  : {summary['seguimiento']}  🟡",
        f"  Normales     : {summary['normales']}  🟢",
        f"  Cumplidos    : {summary['cumplidos']}  ok",
        f"  ALERTA       : {'SI' if summary['alerta'] else 'no'}  {summary['alerta_icon']}",
        "=" * 58,
    ]
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if "--summary" in args:
        print(format_sla_summary(get_sla_summary()))
        sys.exit(0)

    if "--list" in args:
        slas = get_all_slas()
        if not slas:
            print("No hay SLAs activos.")
        else:
            for s in slas:
                print(format_sla(s))
        sys.exit(0)

    if "--demo" in args:
        print("\n-- Demo: create_sla --\n")
        sla = create_sla(
            case_id     = "6227ebe9",
            decision_ts = "2026-05-17T10:00:00",
            pregunta    = "Por que D3 esta en rojo?",
            owner       = "coordinador_planificacion",
            priority    = "alta",
        )
        s = get_sla(sla.case_id)
        print(format_sla(s))
        print(format_sla_summary(get_sla_summary()))
        sys.exit(0)

    print("""
SENTINEL · SLA Layer CLI
Uso:
  python -m sentinel.sla_layer --summary   # Resumen de SLAs
  python -m sentinel.sla_layer --list      # Todos los SLAs activos
  python -m sentinel.sla_layer --demo      # Demo con un SLA de prueba
""")
