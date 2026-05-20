# -*- coding: utf-8 -*-
"""
sentinel/watchdog.py
RC-2B — Watchdog de Silencio Operativo y Escalamiento SLA

Ejecuta dos vigilancias autónomas que se activan sin intervención humana:

  1. Silencio Operativo
     Detecta entidades del Holding que no han cargado evidencia mensual
     en los últimos N días. Genera alerta tipo 'silencio' en alerts_history.
     Umbral por defecto: 7 días. Ajustable vía watchdog_config.

  2. Escalamiento SLA
     Identifica alertas con sla_status='VENCIDO' que llevan más de
     DIAS_ESCALAR días sin ser resueltas ni escaladas.
     Las marca escalada=1, sla_status='ESCALADO' y registra evento en
     alert_timeline (trazabilidad inmutable).

Principio RC-2B: automatización administrativa, nunca decisional.
  - Cambia estados y escala.
  - Nunca cierra, nunca resuelve, nunca interpreta causas.

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentinel.db_config import DbConn

# ── CONSTANTES ────────────────────────────────────────────────────────────────
WATCHDOG_SILENCIO_DIAS    = 7   # días sin upload → alerta silencio
WATCHDOG_ESCALAMIENTO_DIAS = 7  # días vencido sin resolución → auto-escalamiento

EXPECTED_ENTITIES = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]
ENTITY_LABELS = {
    "GAD":       "GAD Municipal de Montecristi",
    "BOMBEROS":  "Cuerpo de Bomberos de Montecristi",
    "EMAI-EP":   "Empresa Municipal de Aseo Integral",
    "PATRONATO": "Patronato Municipal de Amparo Social",
}

_CLOSED_STATES = {"archivada", "validada", "resuelta"}


# ── WATCHDOG 1: SILENCIO OPERATIVO ───────────────────────────────────────────

def check_silencio(conn: "DbConn", threshold_days: int = WATCHDOG_SILENCIO_DIAS) -> list[dict]:
    """
    Detecta entidades sin uploads en los últimos threshold_days días.
    Retorna lista de dicts con: entidad, entidad_label, dias_sin_carga,
                                ultimo_upload (ISO str o None).
    """
    try:
        c = conn.cursor()
        now = datetime.now()
        cutoff = (now - timedelta(days=threshold_days)).strftime("%Y-%m-%dT%H:%M:%S")

        silentes = []
        for ent in EXPECTED_ENTITIES:
            row = c.execute(
                "SELECT MAX(uploaded_at) as ultimo "
                "FROM document_uploads WHERE entidad=?",
                (ent,),
            ).fetchone()
            ultimo = row["ultimo"] if row else None

            if ultimo is None:
                # Nunca ha cargado
                dias = threshold_days + 1
                silentes.append({
                    "entidad":        ent,
                    "entidad_label":  ENTITY_LABELS.get(ent, ent),
                    "dias_sin_carga": dias,
                    "ultimo_upload":  None,
                })
            else:
                # Parsear y comparar
                try:
                    dt_ultimo = None
                    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
                        try:
                            dt_ultimo = datetime.strptime(str(ultimo), fmt)
                            break
                        except ValueError:
                            continue
                    if dt_ultimo is None:
                        dt_ultimo = datetime.fromisoformat(str(ultimo))
                    dias = (now - dt_ultimo).days
                    if dias >= threshold_days:
                        silentes.append({
                            "entidad":        ent,
                            "entidad_label":  ENTITY_LABELS.get(ent, ent),
                            "dias_sin_carga": dias,
                            "ultimo_upload":  str(ultimo),
                        })
                except Exception:
                    pass
        return silentes
    except Exception:
        try:
            conn._raw.rollback()  # reset aborted transaction state
        except Exception:
            pass
        return []


def run_watchdog_silencio(conn: "DbConn",
                          threshold_days: int = WATCHDOG_SILENCIO_DIAS) -> int:
    """
    Ejecuta el watchdog de silencio y persiste alertas en alerts_history.
    Idempotente — usa UNIQUE(period_year, period_month, entidad, tipo).
    Retorna número de alertas nuevas creadas.
    """
    silentes = check_silencio(conn, threshold_days)
    if not silentes:
        return 0

    from sentinel.sla_db import update_alert_sla

    now = datetime.now()
    year, month = now.year, now.month
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%S")
    inserted = 0
    c = conn.cursor()

    for s in silentes:
        ent  = s["entidad"]
        lbl  = s["entidad_label"]
        dias = s["dias_sin_carga"]
        ultimo = s["ultimo_upload"]

        if ultimo:
            detalle = (
                f"No se han registrado cargas de evidencia para {lbl} en {dias} días. "
                f"El último documento fue cargado el {ultimo[:10]}. "
                f"Se requiere cédula eSIGEF del período vigente."
            )
        else:
            detalle = (
                f"No existe registro de cargas de evidencia para {lbl} en el sistema. "
                f"La entidad no tiene documentos registrados en Supabase. "
                f"Se requiere cédula eSIGEF del período vigente."
            )

        accion = (
            f"Solicitar urgentemente a {lbl} la carga de cédula eSIGEF en el "
            f"Centro de Ingesta. Plazo: 48 horas. Alerta generada automáticamente "
            f"por el Watchdog Silencio Operativo."
        )

        try:
            if conn.mode == "supabase":
                sql = """
                    INSERT INTO alerts_history
                        (detected_at, period_year, period_month, entidad, tipo,
                         status, severidad, titulo, detalle, accion,
                         fuente_datos, estado)
                    VALUES (%s, %s, %s, %s, 'silencio',
                            'warning', 'Advertencia', %s, %s, %s,
                            'watchdog_silencio', 'pendiente')
                    ON CONFLICT (period_year, period_month, entidad, tipo) DO UPDATE
                        SET detected_at=%s, detalle=%s
                """
                c.execute(sql, (
                    now_iso, year, month, ent,
                    f"Silencio operativo — {lbl} ({dias}d sin carga)",
                    detalle, accion,
                    now_iso, detalle,  # ON CONFLICT update values
                ))
            else:
                sql = """
                    INSERT OR REPLACE INTO alerts_history
                        (detected_at, period_year, period_month, entidad, tipo,
                         status, severidad, titulo, detalle, accion,
                         fuente_datos, estado)
                    VALUES (?, ?, ?, ?, 'silencio',
                            'warning', 'Advertencia', ?, ?, ?,
                            'watchdog_silencio', 'pendiente')
                """
                c.execute(sql, (
                    now_iso, year, month, ent,
                    f"Silencio operativo — {lbl} ({dias}d sin carga)",
                    detalle, accion,
                ))
            if c.rowcount > 0:
                inserted += 1
        except Exception:
            pass

    try:
        conn.commit()
    except Exception:
        pass

    # Backfill SLA para las alertas recién creadas
    try:
        for s in silentes:
            row = c.execute(
                "SELECT id, detected_at, severidad, entidad, estado, escalada "
                "FROM alerts_history "
                "WHERE period_year=? AND period_month=? AND entidad=? AND tipo='silencio'",
                (year, month, s["entidad"]),
            ).fetchone()
            if row:
                update_alert_sla(conn, row)
    except Exception:
        pass

    return inserted


# ── WATCHDOG 2: ESCALAMIENTO SLA ─────────────────────────────────────────────

def run_watchdog_escalamiento(
    conn: "DbConn",
    dias_vencido: int = WATCHDOG_ESCALAMIENTO_DIAS,
) -> int:
    """
    Auto-escala alertas que llevan más de `dias_vencido` días en VENCIDO
    sin ser resueltas ni escaladas previamente.

    Acción:
      - escalada = 1
      - sla_status = 'ESCALADO'
      - Registra evento en alert_timeline (inmutable)

    NO cierra, NO resuelve, NO interpreta causas.
    Retorna el número de alertas escaladas.
    """
    try:
        c = conn.cursor()
        now = datetime.now()
        cutoff_iso = (now - timedelta(days=dias_vencido)).strftime("%Y-%m-%dT%H:%M:%S")

        # Alertas vencidas, no escaladas, no cerradas, más antiguas que el umbral
        rows = c.execute(
            "SELECT id, detected_at, entidad, severidad, titulo "
            "FROM alerts_history "
            "WHERE sla_status='VENCIDO' "
            "  AND (escalada IS NULL OR escalada=0) "
            "  AND estado NOT IN ('archivada','validada','resuelta') "
            "  AND detected_at < ?",
            (cutoff_iso,),
        ).fetchall()

        if not rows:
            return 0

        escalados = 0
        now_iso = now.strftime("%Y-%m-%dT%H:%M:%S")

        for r in rows:
            alert_id = r["id"]
            try:
                # Actualizar alerta
                c.execute(
                    "UPDATE alerts_history "
                    "SET escalada=1, sla_status='ESCALADO', nivel_escalamiento='director' "
                    "WHERE id=?",
                    (alert_id,),
                )
                # Registrar en timeline (bitácora inmutable)
                nota = (
                    f"Escalamiento automático por Watchdog RC-2B. "
                    f"Alerta en estado VENCIDO por más de {dias_vencido} días sin resolución. "
                    f"Se requiere intervención de Dirección de Área."
                )
                c.execute(
                    """INSERT INTO alert_timeline
                       (alert_id, timestamp, actor, evento, estado_desde,
                        estado_hasta, nota, nivel)
                       VALUES (?, ?, 'sistema', 'escalamiento_automatico',
                               'VENCIDO', 'ESCALADO', ?, 'director')""",
                    (alert_id, now_iso, nota),
                )
                escalados += 1
            except Exception:
                pass

        conn.commit()
        return escalados

    except Exception:
        try:
            conn._raw.rollback()
        except Exception:
            pass
        return 0


# ── PUNTO DE ENTRADA ÚNICO ────────────────────────────────────────────────────

def run_all(conn: "DbConn") -> dict:
    """
    Ejecuta todos los watchdogs. Retorna dict con resultados.
    Llamado por scheduler.tick() en cada ciclo programado.
    """
    silencio_nuevas    = run_watchdog_silencio(conn)
    escalaciones_auto  = run_watchdog_escalamiento(conn)
    return {
        "silencio_alertas_nuevas":  silencio_nuevas,
        "escalaciones_automaticas": escalaciones_auto,
    }
