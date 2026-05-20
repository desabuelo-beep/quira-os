# -*- coding: utf-8 -*-
"""
sentinel/sla_db.py
RC-2A — SLA Institucional (Supabase-backed)

Gestión de SLA de alertas contra la tabla alerts_history de Supabase.
Complementa (no reemplaza) sla_layer.py que opera sobre casos de gobernanza
IA; este módulo opera sobre el holding municipal de inversión.

Estados SLA (congelados RC-2A):
    EN_TIEMPO       — dentro del plazo institucional
    PROXIMO_VENCER  — menos del 20% del tiempo restante
    VENCIDO         — plazo vencido, sin resolución
    ESCALADO        — plazo vencido + sistema escaló automáticamente
    PAUSADO         — suspendido por decisión institucional
    EXENTO          — exento formalmente de SLA

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional


# ── CONSTANTES ────────────────────────────────────────────────────────────────
_SLA_DEFAULT_CRITICA    = 48    # horas
_SLA_DEFAULT_ADVERTENCIA = 120  # horas
_SLA_THRESHOLD_PROXIMO  = 0.20  # <20% tiempo restante → PROXIMO_VENCER

# Estados que implican resolución (no cuentan como vencidos)
_ESTADOS_CERRADOS = {"archivada", "validada"}

# Etiquetas institucionales por estado SLA
SLA_LABELS = {
    "EN_TIEMPO":      "En tiempo",
    "PROXIMO_VENCER": "Próximo a vencer",
    "VENCIDO":        "Vencido",
    "ESCALADO":       "Escalado",
    "PAUSADO":        "Pausado",
    "EXENTO":         "Exento",
}

SLA_ICONS = {
    "EN_TIEMPO":      "🟢",
    "PROXIMO_VENCER": "🟡",
    "VENCIDO":        "🔴",
    "ESCALADO":       "🔺",
    "PAUSADO":        "⏸",
    "EXENTO":         "✅",
}

SLA_COLORS = {
    "EN_TIEMPO":      "#00E096",
    "PROXIMO_VENCER": "#FFB800",
    "VENCIDO":        "#FF4D6D",
    "ESCALADO":       "#FF4D6D",
    "PAUSADO":        "#8892A4",
    "EXENTO":         "#00E096",
}


# ── CONFIG ────────────────────────────────────────────────────────────────────
def _normalize_severidad(severidad: str) -> str:
    """
    Normaliza severidad a 'CRITICA' o 'ADVERTENCIA' sin importar acentos ni case.
    Maneja: 'Crítica', 'CRITICA', 'Crítico', 'CRITICO', 'Advertencia', etc.
    """
    import unicodedata
    s = (severidad or "").upper()
    s_nfd = "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )  # elimina diacríticos
    return "CRITICA" if "CRIT" in s_nfd else "ADVERTENCIA"


def get_sla_target_hours(conn, severidad: str) -> int:
    """
    Busca target_hours en sla_config (entidad='*', severidad normalizada).
    Fallback: 48h para CRITICA, 120h para todo lo demás.
    """
    sev_key = _normalize_severidad(severidad)
    try:
        c = conn.cursor()
        row = c.execute(
            "SELECT target_hours FROM sla_config "
            "WHERE entidad='*' AND severidad=? AND activo=TRUE "
            "ORDER BY id DESC LIMIT 1",
            (sev_key,),
        ).fetchone()
        if row:
            return int(row["target_hours"])
    except Exception:
        pass
    return _SLA_DEFAULT_CRITICA if sev_key == "CRITICA" else _SLA_DEFAULT_ADVERTENCIA


# ── CÓMPUTO ───────────────────────────────────────────────────────────────────
def compute_sla_due_at(detected_at_str: str, target_hours: int) -> str:
    """Devuelve ISO timestamp del vencimiento SLA."""
    try:
        detected = _parse_dt(detected_at_str)
        due      = detected + timedelta(hours=target_hours)
        return due.strftime("%Y-%m-%dT%H:%M:%S")
    except Exception:
        return ""


def compute_sla_status(
    detected_at_str: str,
    target_hours: int,
    estado: str,
    escalada: int = 0,
) -> tuple[str, Optional[float]]:
    """
    Calcula (sla_status, horas_restantes).
    horas_restantes < 0  → vencido hace N horas.
    Retorna ('EN_TIEMPO', None) si no hay datos suficientes.
    """
    if not detected_at_str or not target_hours:
        return "EN_TIEMPO", None

    # Alertas ya cerradas → cumplido dentro del SLA (simplificado RC-2A)
    if (estado or "").lower() in _ESTADOS_CERRADOS:
        return "EN_TIEMPO", 0.0

    try:
        detected = _parse_dt(detected_at_str)
        due      = detected + timedelta(hours=target_hours)
        now      = datetime.now()
        remaining_h = (due - now).total_seconds() / 3600.0

        if remaining_h < 0:
            # Vencido — ¿escalado?
            return ("ESCALADO" if escalada else "VENCIDO"), round(remaining_h, 1)

        pct_remaining = remaining_h / target_hours
        if pct_remaining < _SLA_THRESHOLD_PROXIMO:
            return "PROXIMO_VENCER", round(remaining_h, 1)

        return "EN_TIEMPO", round(remaining_h, 1)

    except Exception:
        return "EN_TIEMPO", None


# ── PERSISTENCIA ──────────────────────────────────────────────────────────────
def update_alert_sla(conn, alert: dict) -> None:
    """
    Calcula y escribe los 4 campos SLA de una alerta.
    `alert` debe contener: id, detected_at, severidad, entidad, estado, escalada.
    """
    target_h = get_sla_target_hours(conn, alert.get("severidad", ""))
    due_at   = compute_sla_due_at(alert.get("detected_at", ""), target_h)
    status, _ = compute_sla_status(
        alert.get("detected_at", ""),
        target_h,
        alert.get("estado", ""),
        int(alert.get("escalada") or 0),
    )
    try:
        c = conn.cursor()
        c.execute(
            """UPDATE alerts_history
               SET sla_target_hours=?, sla_due_at=?, sla_status=?
               WHERE id=?""",
            (target_h, due_at, status, alert["id"]),
        )
        conn.commit()
    except Exception:
        pass


def backfill_sla(conn) -> int:
    """
    Rellena los campos SLA de todas las alertas existentes.
    Idempotente — sobreescribe siempre (recalcula en tiempo real).
    Devuelve el número de alertas actualizadas.
    """
    try:
        c = conn.cursor()
        alerts = c.execute(
            "SELECT id, detected_at, severidad, entidad, estado, escalada "
            "FROM alerts_history"
        ).fetchall()
        updated = 0
        for a in alerts:
            update_alert_sla(conn, a)
            updated += 1
        return updated
    except Exception:
        return 0


def refresh_sla_statuses(conn) -> int:
    """
    Actualiza sla_status para todas las alertas NO cerradas.
    Llamar periódicamente (watchdog o cada carga de página).
    """
    try:
        c = conn.cursor()
        rows = c.execute(
            "SELECT id, detected_at, sla_target_hours, estado, escalada "
            "FROM alerts_history "
            "WHERE estado NOT IN ('archivada','validada') "
            "AND sla_target_hours IS NOT NULL"
        ).fetchall()
        updated = 0
        for r in rows:
            status, _ = compute_sla_status(
                r.get("detected_at", ""),
                int(r.get("sla_target_hours") or 48),
                r.get("estado", ""),
                int(r.get("escalada") or 0),
            )
            c.execute(
                "UPDATE alerts_history SET sla_status=? WHERE id=?",
                (status, r["id"]),
            )
            updated += 1
        conn.commit()
        return updated
    except Exception:
        return 0


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
def get_sla_summary(conn) -> dict:
    """
    Resumen de cumplimiento SLA para Vista Ejecutiva y Centro de Control.

    Retorna:
        total_activas, en_tiempo, proximo_vencer, vencidas, escaladas,
        pct_cumplimiento (%), alerta_global (bool)
    """
    defaults = {
        "total_activas": 0, "en_tiempo": 0, "proximo_vencer": 0,
        "vencidas": 0, "escaladas": 0, "pct_cumplimiento": 100.0,
        "alerta_global": False,
    }
    try:
        c = conn.cursor()
        rows = c.execute(
            "SELECT sla_status FROM alerts_history "
            "WHERE estado NOT IN ('archivada','validada')"
        ).fetchall()
        if not rows:
            return defaults

        counts = {"EN_TIEMPO": 0, "PROXIMO_VENCER": 0, "VENCIDO": 0, "ESCALADO": 0}
        for r in rows:
            st = (r.get("sla_status") or "EN_TIEMPO").upper()
            if st in counts:
                counts[st] += 1
            else:
                counts["EN_TIEMPO"] += 1  # PAUSADO/EXENTO count as compliant

        total     = len(rows)
        vencidas  = counts["VENCIDO"] + counts["ESCALADO"]
        cumplidas = counts["EN_TIEMPO"] + counts["PROXIMO_VENCER"]
        pct       = round(cumplidas / total * 100, 1) if total else 100.0

        return {
            "total_activas":    total,
            "en_tiempo":        counts["EN_TIEMPO"],
            "proximo_vencer":   counts["PROXIMO_VENCER"],
            "vencidas":         counts["VENCIDO"],
            "escaladas":        counts["ESCALADO"],
            "pct_cumplimiento": pct,
            "alerta_global":    vencidas > 0,
        }
    except Exception:
        return defaults


# ── HTML HELPERS ──────────────────────────────────────────────────────────────
def sla_badge_html(sla_status: str, hours_remaining: Optional[float]) -> str:
    """
    Genera HTML compacto del badge SLA para insertar en alert cards.
    Compatible con el design system QUIRA OS (variables CSS custom).
    """
    status = (sla_status or "EN_TIEMPO").upper()
    icon   = SLA_ICONS.get(status, "•")
    label  = SLA_LABELS.get(status, status)
    color  = SLA_COLORS.get(status, "#8892A4")
    bg     = f"{color}18"
    border = f"{color}35"

    # Texto de tiempo
    time_txt = ""
    if hours_remaining is not None:
        if hours_remaining < 0:
            h = abs(hours_remaining)
            if h >= 24:
                d = int(h // 24)
                time_txt = f" · Vencida hace {d}d"
            else:
                time_txt = f" · Vencida hace {int(h)}h"
        elif hours_remaining > 0 and status in ("EN_TIEMPO", "PROXIMO_VENCER"):
            if hours_remaining >= 24:
                d = int(hours_remaining // 24)
                time_txt = f" · {d}d restantes"
            else:
                time_txt = f" · {int(hours_remaining)}h restantes"

    return (
        f'<span style="display:inline-flex;align-items:center;gap:4px;'
        f'font-size:9px;font-weight:700;letter-spacing:.04em;'
        f'padding:2px 8px;border-radius:8px;white-space:nowrap;'
        f'background:{bg};color:{color};border:1px solid {border}">'
        f'{icon} SLA {label}{time_txt}</span>'
    )


# ── UTIL ──────────────────────────────────────────────────────────────────────
def _parse_dt(s: str) -> datetime:
    """Parsea ISO timestamp flexible."""
    s = (s or "").strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # Último intento con fromisoformat
    return datetime.fromisoformat(s)
