# -*- coding: utf-8 -*-
"""
sentinel/scheduler.py
RC-2B — Scheduler Institucional QUIRA OS

Patrón "opportunistic tick":
  - Almacena timestamps de última ejecución en scheduler_log (Supabase).
  - tick() se llama en cada carga de página (app.py), después del gate de auth.
  - Si una tarea está vencida, la ejecuta sincrónicamente y registra resultado.
  - Seguro en multi-sesión: el timestamp actúa como mutex débil.
    (Lo peor que puede pasar: dos sesiones corren la misma tarea casi
     simultáneamente. No produce datos corruptos, solo duplica trabajo.)

Tareas registradas (RC-2B):
  ┌─────────────────────────┬──────────────┬───────────────────────────────────┐
  │ Tarea                   │ Intervalo    │ Función                           │
  ├─────────────────────────┼──────────────┼───────────────────────────────────┤
  │ sla_refresh             │ 30 min       │ refresh_sla_statuses(conn)        │
  │ watchdog_silencio       │ 4 h          │ watchdog.run_watchdog_silencio()  │
  │ watchdog_escalamiento   │ 1 h          │ watchdog.run_watchdog_escalamiento│
  └─────────────────────────┴──────────────┴───────────────────────────────────┘

Principio: tick() completa en < 500 ms en condiciones normales.
           Si una tarea falla, se registra el error y el scheduler continúa.

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentinel.db_config import DbConn

# ── CONFIGURACIÓN DE TAREAS ───────────────────────────────────────────────────
_TASKS: dict[str, int] = {
    "sla_refresh":           30,   # minutos
    "watchdog_silencio":     240,  # minutos (4 h)
    "watchdog_escalamiento": 60,   # minutos (1 h)
}


# ── RUNNERS INTERNOS ──────────────────────────────────────────────────────────
def _run_sla_refresh(conn: "DbConn") -> str:
    from sentinel.sla_db import refresh_sla_statuses
    n = refresh_sla_statuses(conn)
    return f"{n} alertas actualizadas"


def _run_watchdog_silencio(conn: "DbConn") -> str:
    from sentinel.watchdog import run_watchdog_silencio
    n = run_watchdog_silencio(conn)
    return f"{n} alertas silencio creadas/actualizadas"


def _run_watchdog_escalamiento(conn: "DbConn") -> str:
    from sentinel.watchdog import run_watchdog_escalamiento
    n = run_watchdog_escalamiento(conn)
    return f"{n} alertas escaladas automáticamente"


_RUNNERS = {
    "sla_refresh":           _run_sla_refresh,
    "watchdog_silencio":     _run_watchdog_silencio,
    "watchdog_escalamiento": _run_watchdog_escalamiento,
}


# ── SCHEDULER_LOG HELPERS ─────────────────────────────────────────────────────
def _get_last_run(conn: "DbConn", task_name: str) -> datetime | None:
    """Retorna el datetime de la última ejecución, o None si nunca corrió."""
    try:
        c = conn.cursor()
        row = c.execute(
            "SELECT last_run FROM scheduler_log WHERE task_name=?", (task_name,)
        ).fetchone()
        if not row or not row.get("last_run"):
            return None
        s = str(row["last_run"])
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _mark_ran(conn: "DbConn", task_name: str, status: str, result_msg: str) -> None:
    """Registra o actualiza la fila de scheduler_log para la tarea."""
    now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    try:
        c = conn.cursor()
        if conn.mode == "supabase":
            c.execute(
                """INSERT INTO scheduler_log (task_name, last_run, status, result_msg, runs_total)
                   VALUES (%s, %s, %s, %s, 1)
                   ON CONFLICT (task_name) DO UPDATE
                       SET last_run=%s, status=%s, result_msg=%s,
                           runs_total = scheduler_log.runs_total + 1""",
                (task_name, now_iso, status, result_msg,
                 now_iso, status, result_msg),
            )
        else:
            c.execute(
                """INSERT INTO scheduler_log (task_name, last_run, status, result_msg, runs_total)
                   VALUES (?, ?, ?, ?, 1)
                   ON CONFLICT (task_name) DO UPDATE
                       SET last_run=excluded.last_run, status=excluded.status,
                           result_msg=excluded.result_msg,
                           runs_total = runs_total + 1""",
                (task_name, now_iso, status, result_msg),
            )
        conn.commit()
    except Exception:
        pass


# ── TICK PRINCIPAL ────────────────────────────────────────────────────────────
def tick(conn: "DbConn") -> dict[str, str]:
    """
    Punto de entrada del scheduler. Llamar en cada carga de página (app.py).

    Para cada tarea registrada:
      1. Lee last_run de scheduler_log.
      2. Si elapsed >= intervalo → ejecuta y registra resultado.
      3. Si la tarea falla → registra ERROR y continúa.

    Retorna dict {task_name: resultado_str} solo de las tareas que corrieron.
    """
    now     = datetime.now()
    results: dict[str, str] = {}

    for task_name, interval_min in _TASKS.items():
        runner = _RUNNERS.get(task_name)
        if runner is None:
            continue

        last_run = _get_last_run(conn, task_name)
        if last_run is None:
            # Primera vez — ejecutar inmediatamente
            elapsed_min = interval_min + 1
        else:
            elapsed_min = (now - last_run).total_seconds() / 60.0

        if elapsed_min >= interval_min:
            try:
                msg = runner(conn)
                _mark_ran(conn, task_name, "OK", msg)
                results[task_name] = msg
            except Exception as e:
                err = str(e)[:200]
                _mark_ran(conn, task_name, "ERROR", err)
                results[task_name] = f"ERROR: {err}"

    return results


# ── DIAGNÓSTICO ───────────────────────────────────────────────────────────────
def get_scheduler_status(conn: "DbConn") -> list[dict]:
    """
    Retorna el estado actual de todas las tareas del scheduler.
    Usado por el Centro de Control para mostrar estado operativo.
    """
    try:
        c = conn.cursor()
        rows = c.execute(
            "SELECT task_name, last_run, status, result_msg, runs_total "
            "FROM scheduler_log ORDER BY task_name"
        ).fetchall()
        now = datetime.now()
        result = []
        for r in rows:
            last_run = _get_last_run(conn, r["task_name"])
            interval = _TASKS.get(r["task_name"], 0)
            if last_run:
                elapsed = int((now - last_run).total_seconds() / 60)
                proxima = max(0, interval - elapsed)
            else:
                elapsed, proxima = None, 0
            result.append({
                "task_name":   r["task_name"],
                "last_run":    r.get("last_run"),
                "status":      r.get("status", "–"),
                "result_msg":  r.get("result_msg", ""),
                "runs_total":  r.get("runs_total", 0),
                "interval_min": interval,
                "elapsed_min": elapsed,
                "proxima_min": proxima,
            })
        # Tareas que nunca corrieron
        registered = {r["task_name"] for r in rows}
        for task_name, interval in _TASKS.items():
            if task_name not in registered:
                result.append({
                    "task_name":   task_name,
                    "last_run":    None,
                    "status":      "PENDING",
                    "result_msg":  "Nunca ejecutada",
                    "runs_total":  0,
                    "interval_min": interval,
                    "elapsed_min": None,
                    "proxima_min": 0,
                })
        return result
    except Exception:
        return []
