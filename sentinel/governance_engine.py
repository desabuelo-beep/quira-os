"""
sentinel/governance_engine.py
Motor de Gobernanza Institucional — Sprint 2.9A

Ruta de Atención: estados formales, ownership, escalamiento, bitácora inmutable.

Principios:
  - Humano al centro — sin transiciones automáticas
  - Bitácora inmutable — append-only alert_timeline
  - Lenguaje institucional — sin terminología técnica
  - Auditabilidad total — cada evento tiene actor + nota

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sentinel.db_config import get_connection

# ── ESTADOS INSTITUCIONALES ────────────────────────────────────────────────────
ESTADOS: dict[str, dict] = {
    "pendiente":   {"label": "Abierta",      "color": "#FF4D6D", "icon": "🔴"},
    "en_revision": {"label": "En Revisión",  "color": "#FFB800", "icon": "🟡"},
    "derivada":    {"label": "Derivada",     "color": "#7C6AF7", "icon": "🔵"},
    "resuelta":    {"label": "Resuelta",     "color": "#00D4FF", "icon": "🔷"},
    "observada":   {"label": "Observada",    "color": "#FF6B35", "icon": "🟠"},
    "validada":    {"label": "Validada",     "color": "#4DB8FF", "icon": "🔹"},
    "archivada":   {"label": "Archivada",    "color": "#00E096", "icon": "🟢"},
}

# ── MÁQUINA DE ESTADOS ────────────────────────────────────────────────────────
TRANSITIONS: dict[str, list[str]] = {
    "pendiente":   ["en_revision", "derivada"],
    "en_revision": ["resuelta", "derivada", "observada"],
    "derivada":    ["en_revision"],
    "resuelta":    ["validada", "observada"],
    "observada":   ["en_revision"],
    "validada":    ["archivada"],
    "archivada":   [],  # estado terminal
}

# ── NIVELES DE ESCALAMIENTO ───────────────────────────────────────────────────
NIVELES: dict[str, str] = {
    "analista":   "Analista Institucional",
    "director":   "Dirección de Área",
    "financiero": "Dirección Financiera",
    "alcalde":    "Despacho del Alcalde",
}

_EVENTO_LABEL: dict[str, str] = {
    "pendiente":   "Alerta detectada",
    "en_revision": "Tomada en revisión",
    "derivada":    "Derivada a otra dirección",
    "resuelta":    "Resolución registrada",
    "observada":   "Resolución observada — requiere corrección",
    "validada":    "Resolución validada",
    "archivada":   "Archivada — cierre institucional",
}


# ── HELPERS ───────────────────────────────────────────────────────────────────
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_timeline_event(
    conn,
    alert_id: int,
    actor: str,
    evento: str,
    estado_desde: Optional[str],
    estado_hasta: Optional[str],
    nota: Optional[str],
    nivel: str = "analista",
) -> None:
    conn.cursor().execute(
        """INSERT INTO alert_timeline
           (alert_id, timestamp, actor, evento, estado_desde, estado_hasta, nota, nivel)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (alert_id, _now(), actor, evento, estado_desde, estado_hasta, nota, nivel),
    )


# ── TRANSICIÓN DE ESTADO ──────────────────────────────────────────────────────
def transition_alert(
    alert_id: int,
    new_estado: str,
    actor: str = "sistema",
    nota: Optional[str] = None,
    nivel: str = "analista",
) -> bool:
    """
    Cambia el estado de una alerta validando la transición permitida.
    Escribe evento en alert_timeline. Retorna True si fue exitoso.
    """
    if new_estado not in ESTADOS:
        return False

    conn = get_connection()
    c    = conn.cursor()

    row = c.execute(
        "SELECT estado FROM alerts_history WHERE id=?", (alert_id,)
    ).fetchone()
    if not row:
        conn.close()
        return False

    current = row["estado"]
    if new_estado not in TRANSITIONS.get(current, []):
        conn.close()
        return False

    now = _now()
    c.execute(
        "UPDATE alerts_history SET estado=? WHERE id=?",
        (new_estado, alert_id),
    )

    if new_estado == "archivada":
        # Marcar fecha de resolución final si no estaba
        c.execute(
            "UPDATE alerts_history SET resuelta_en=? WHERE id=? AND resuelta_en IS NULL",
            (now, alert_id),
        )

    evento = _EVENTO_LABEL.get(new_estado, f"Estado: {ESTADOS[new_estado]['label']}")
    _write_timeline_event(conn, alert_id, actor, evento, current, new_estado, nota, nivel)

    conn.commit()
    conn.close()
    return True


# ── ASIGNACIÓN DE RESPONSABLE ─────────────────────────────────────────────────
def assign_alert(
    alert_id: int,
    owner: str,
    nivel: str = "analista",
    actor: str = "sistema",
    nota: Optional[str] = None,
) -> bool:
    """
    Asigna ownership de una alerta. Persiste owner_anterior para trazabilidad.
    Registra evento en timeline.
    """
    conn = get_connection()
    c    = conn.cursor()

    row = c.execute(
        "SELECT owner_actual FROM alerts_history WHERE id=?", (alert_id,)
    ).fetchone()
    if not row:
        conn.close()
        return False

    owner_ant = row.get("owner_actual") or ""
    now       = _now()

    try:
        c.execute(
            """UPDATE alerts_history
               SET owner_actual=?, owner_anterior=?, fecha_asignacion=?, nivel_escalamiento=?
               WHERE id=?""",
            (owner, owner_ant, now, nivel, alert_id),
        )
    except Exception:
        conn.close()
        return False

    nivel_label = NIVELES.get(nivel, nivel)
    evento      = f"Asignada a {nivel_label}"
    _write_timeline_event(
        conn, alert_id, actor, evento, None, None,
        nota or f"Responsable: {owner}",
        nivel,
    )

    conn.commit()
    conn.close()
    return True


# ── ESCALAMIENTO ──────────────────────────────────────────────────────────────
def escalar_alert(
    alert_id: int,
    nivel_destino: str,
    actor: str = "analista",
    nota: Optional[str] = None,
) -> bool:
    """Marca la alerta como escalada al nivel indicado. Escribe timeline."""
    conn = get_connection()
    c    = conn.cursor()

    row = c.execute(
        "SELECT estado FROM alerts_history WHERE id=?", (alert_id,)
    ).fetchone()
    if not row:
        conn.close()
        return False

    try:
        c.execute(
            "UPDATE alerts_history SET escalada=1, nivel_escalamiento=? WHERE id=?",
            (nivel_destino, alert_id),
        )
    except Exception:
        conn.close()
        return False

    nivel_label = NIVELES.get(nivel_destino, nivel_destino)
    evento      = f"Escalada a {nivel_label}"
    _write_timeline_event(conn, alert_id, actor, evento, None, None, nota, nivel_destino)

    conn.commit()
    conn.close()
    return True


# ── CONSULTAS ─────────────────────────────────────────────────────────────────
def get_timeline(alert_id: int) -> list[dict]:
    """
    Retorna la bitácora completa de un alert.
    Si no hay eventos formales, sintetiza uno a partir de detected_at.
    """
    conn  = get_connection()
    c     = conn.cursor()
    rows  = c.execute(
        """SELECT timestamp, actor, evento, estado_desde, estado_hasta, nota, nivel
           FROM   alert_timeline
           WHERE  alert_id = ?
           ORDER  BY timestamp ASC""",
        (alert_id,),
    ).fetchall()

    if not rows:
        ah = c.execute(
            "SELECT detected_at, titulo FROM alerts_history WHERE id=?",
            (alert_id,),
        ).fetchone()
        conn.close()
        if ah:
            return [{
                "timestamp":    (ah.get("detected_at") or "")[:19],
                "actor":        "sistema",
                "evento":       "Alerta detectada automáticamente",
                "estado_desde": None,
                "estado_hasta": "pendiente",
                "nota":         ah.get("titulo", ""),
                "nivel":        "sistema",
            }]
        return []

    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["timestamp"] = (d.get("timestamp") or "")[:19].replace("T", " ")
        result.append(d)
    return result


def get_gestion_kpis() -> dict:
    """Conteos por estado + escalaciones + alertas sin responsable."""
    conn = get_connection()
    c    = conn.cursor()

    counts: dict[str, int] = {}
    for estado in ESTADOS:
        n = (c.execute(
            "SELECT COUNT(*) as n FROM alerts_history WHERE estado=?", (estado,)
        ).fetchone() or {}).get("n", 0)
        counts[estado] = n

    escaladas = (c.execute(
        "SELECT COUNT(*) as n FROM alerts_history WHERE escalada=1"
    ).fetchone() or {}).get("n", 0)

    sin_owner = (c.execute(
        """SELECT COUNT(*) as n FROM alerts_history
           WHERE (owner_actual IS NULL OR owner_actual = '')
             AND estado NOT IN ('archivada')""",
    ).fetchone() or {}).get("n", 0)

    conn.close()

    activos = [counts.get(e, 0) for e in ("pendiente","en_revision","derivada","observada")]
    return {
        "por_estado":    counts,
        "escaladas":     escaladas,
        "sin_owner":     sin_owner,
        "total_activas": sum(activos),
        "en_validacion": counts.get("validada", 0),
        "archivadas":    counts.get("archivada", 0),
    }


def get_alerts_for_gestion(excluir_archivadas: bool = True) -> list[dict]:
    """
    Alertas con info de ownership y transiciones disponibles.
    Ordenadas por prioridad: observadas → pendientes → en_revision → otras.
    """
    conn  = get_connection()
    where = "WHERE estado != 'archivada'" if excluir_archivadas else ""
    rows  = conn.cursor().execute(f"""
        SELECT id, titulo, entidad, tipo, severidad, estado,
               period_year, period_month, detected_at,
               owner_actual, nivel_escalamiento, escalada,
               fecha_asignacion, resolucion
        FROM   alerts_history
        {where}
        ORDER  BY
            CASE estado
                WHEN 'observada'   THEN 1
                WHEN 'pendiente'   THEN 2
                WHEN 'en_revision' THEN 3
                WHEN 'derivada'    THEN 4
                WHEN 'resuelta'    THEN 5
                WHEN 'validada'    THEN 6
                ELSE 7
            END,
            detected_at DESC
        LIMIT 60
    """).fetchall()
    conn.close()

    result = []
    for r in rows:
        d = dict(r)
        d["estado_meta"]  = ESTADOS.get(d["estado"], {})
        d["transiciones"] = [
            {"id": t, **ESTADOS.get(t, {})}
            for t in TRANSITIONS.get(d["estado"], [])
        ]
        d["nivel_label"]  = NIVELES.get(d.get("nivel_escalamiento") or "", "–")
        d["periodo"]      = f"{d.get('period_month') or '–'}/{d.get('period_year') or '–'}"
        d["dias_abierta"] = _days_since(d.get("detected_at", ""))
        result.append(d)
    return result


def get_alerts_summary_for_timeline() -> list[dict]:
    """Lista reducida de alertas para selector de timeline."""
    conn  = get_connection()
    rows  = conn.cursor().execute("""
        SELECT id, titulo, entidad, estado, period_year, period_month
        FROM   alerts_history
        ORDER  BY detected_at DESC
        LIMIT  100
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _days_since(iso_str: str) -> int:
    try:
        ts  = datetime.fromisoformat(iso_str)
        now = datetime.now(timezone.utc) if ts.tzinfo else datetime.now()
        return max(0, (now - ts).days)
    except Exception:
        return 0
