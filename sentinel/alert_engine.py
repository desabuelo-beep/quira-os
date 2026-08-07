"""
sentinel/alert_engine.py
Motor de Alertas de Cumplimiento — Sprint 2.6

Genera alertas automáticas a partir de los datos operativos del sistema:
  1. Ejecución       — Ti inversión vs umbrales y trayectoria mensual
  2. Cobertura       — Entidades sin upload en el período más reciente

Diseño institucional: el usuario ve severidad (Crítica / Advertencia),
entidad, período y acción sugerida. Nunca terminilogía técnica de BD.

Escalado futuro (Sprint 3.0): Contratación (PAC vs SERCOP), Gobernanza (SLA).

Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import logging
from datetime import datetime
from typing import Optional

from sentinel.db_config import get_connection

_log = logging.getLogger(__name__)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
EXPECTED_ENTITIES = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]

UMBRAL_VERDE    = 35.0   # % Ti — zona verde
UMBRAL_AMARILLO = 15.0   # % Ti — zona amarillo
UMBRAL_ROJO     = 0.0    # % Ti — crítico absoluto (sin ejecución)

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo",  6: "Junio",   7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

ENTITY_LABELS = {
    "GAD":       "GAD Municipal de Montecristi",
    "BOMBEROS":  "Cuerpo de Bomberos de Montecristi",
    "EMAI-EP":   "Empresa Municipal de Aseo Integral",
    "PATRONATO": "Patronato Municipal de Amparo Social",
}

OK          = "ok"
WARNING     = "warning"
ERROR       = "error"

# Estados institucionales de alerta
ESTADO_ABIERTA     = "pendiente"
ESTADO_EN_REVISION = "en_revision"
ESTADO_RESUELTA    = "resuelta"


def _alert_hash(entidad: str, tipo: str, period_year: int,
                period_month: int, severidad: str) -> str:
    """SHA256 del cuarteto institucional. Si cambia severidad → nuevo hash."""
    raw = f"{entidad}|{tipo}|{period_year}|{period_month}|{severidad}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


# ── HELPERS ───────────────────────────────────────────────────────────────────
def _periodo_label(year: int, month: int) -> str:
    return f"{MESES_ES.get(month, str(month))} {year}"


def _prev_period(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def _make_alert(
    tipo: str,
    status: str,
    entidad: str,
    titulo: str,
    detalle: str,
    periodo: str,
    valor: Optional[float] = None,
    accion: str = "",
    umbral: Optional[float] = None,
    fuente_datos: str = "",
) -> dict:
    severidad = "Crítica" if status == ERROR else "Advertencia"
    return {
        "id":            f"{tipo}_{entidad}_{periodo.replace(' ', '_')}",
        "tipo":          tipo,
        "status":        status,
        "severidad":     severidad,
        "entidad":       entidad,
        "entidad_label": ENTITY_LABELS.get(entidad, entidad),
        "titulo":        titulo,
        "detalle":       detalle,
        "valor":         valor,
        "periodo":       periodo,
        "accion":        accion,
        "umbral":        umbral,
        "fuente_datos":  fuente_datos or ("monthly_kpis" if tipo == "ejecucion" else "document_uploads"),
        "ts":            datetime.now().isoformat(),
    }


# ── ALERTAS DE EJECUCIÓN ──────────────────────────────────────────────────────
def _check_ejecucion() -> list[dict]:
    """
    Genera alertas de Ti inversión para el período más reciente.
    Compara con umbral institucional y trayectoria vs mes anterior.
    """
    alerts = []
    try:
        conn = get_connection()
        c    = conn.cursor()

        # Período más reciente con datos
        last = c.execute(
            "SELECT period_year as y, period_month as m "
            "FROM monthly_kpis ORDER BY period_year DESC, period_month DESC LIMIT 1"
        ).fetchone()
        if not last:
            conn.close()
            return []

        year, month = last["y"], last["m"]
        py, pm      = _prev_period(year, month)
        periodo_lbl = _periodo_label(year, month)

        # Ti del período actual por entidad
        rows_cur = c.execute(
            "SELECT entidad, AVG(ti_mensual_pct) as ti "
            "FROM monthly_kpis WHERE period_year=? AND period_month=? "
            "GROUP BY entidad",
            (year, month),
        ).fetchall()
        ti_cur = {r["entidad"]: r["ti"] for r in rows_cur}

        # Ti del período anterior por entidad
        rows_prev = c.execute(
            "SELECT entidad, AVG(ti_mensual_pct) as ti "
            "FROM monthly_kpis WHERE period_year=? AND period_month=? "
            "GROUP BY entidad",
            (py, pm),
        ).fetchall()
        ti_prev = {r["entidad"]: r["ti"] for r in rows_prev}

        conn.close()

        for ent in EXPECTED_ENTITIES:
            ti = ti_cur.get(ent)
            if ti is None:
                continue  # entidad sin datos → cobertura la captura
            ti_ant = ti_prev.get(ent)

            lbl = ENTITY_LABELS.get(ent, ent)

            # Alerta por umbral
            if ti <= UMBRAL_ROJO:
                alerts.append(_make_alert(
                    tipo         = "ejecucion",
                    status       = ERROR,
                    entidad      = ent,
                    titulo       = f"Sin ejecución de inversión — {lbl}",
                    detalle      = f"Ti inversión = 0.00% en {periodo_lbl}. "
                                   f"Los grupos 84.xx (Bienes de Larga Duración) "
                                   f"no registran devengado en el período.",
                    periodo      = periodo_lbl,
                    valor        = ti,
                    accion       = "Verificar partidas de inversión y compromisos pendientes de legalización.",
                    umbral       = UMBRAL_AMARILLO,
                    fuente_datos = "monthly_kpis",
                ))
            elif ti < UMBRAL_AMARILLO:
                alerts.append(_make_alert(
                    tipo         = "ejecucion",
                    status       = ERROR,
                    entidad      = ent,
                    titulo       = f"Ejecución de inversión crítica — {lbl}",
                    detalle      = f"Ti inversión = {ti:.2f}% en {periodo_lbl}. "
                                   f"Por debajo del umbral mínimo de {UMBRAL_AMARILLO:.0f}%. "
                                   f"Riesgo de incumplimiento presupuestario.",
                    periodo      = periodo_lbl,
                    valor        = ti,
                    accion       = "Priorizar ejecución de partidas de inversión. Revisar con dirección financiera.",
                    umbral       = UMBRAL_AMARILLO,
                    fuente_datos = "monthly_kpis",
                ))
            elif ti < UMBRAL_VERDE:
                alerts.append(_make_alert(
                    tipo         = "ejecucion",
                    status       = WARNING,
                    entidad      = ent,
                    titulo       = f"Ejecución de inversión bajo umbral verde — {lbl}",
                    detalle      = f"Ti inversión = {ti:.2f}% en {periodo_lbl}. "
                                   f"Dentro de zona amarilla (15–35%). "
                                   f"Requiere aceleración para alcanzar el umbral institucional.",
                    periodo      = periodo_lbl,
                    valor        = ti,
                    accion       = f"Acelerar ejecución de inversión para superar {UMBRAL_VERDE:.0f}% antes de fin de trimestre.",
                    umbral       = UMBRAL_VERDE,
                    fuente_datos = "monthly_kpis",
                ))

            # Alerta adicional por tendencia decreciente (solo si no hay ya error)
            if (
                ti_ant is not None
                and ti > UMBRAL_ROJO  # ya no es cero
                and ti < ti_ant - 0.5  # retrocedió más de 0.5 pp
                and not any(a["entidad"] == ent and a["status"] == ERROR for a in alerts)
            ):
                alerts.append(_make_alert(
                    tipo     = "ejecucion",
                    status   = WARNING,
                    entidad  = ent,
                    titulo   = f"Retroceso en trayectoria de inversión — {lbl}",
                    detalle  = (
                        f"Ti {_periodo_label(py, pm)}: {ti_ant:.2f}% → "
                        f"{periodo_lbl}: {ti:.2f}% "
                        f"(variación: {ti - ti_ant:+.2f} pp). "
                        f"La trayectoria es decreciente."
                    ),
                    periodo  = periodo_lbl,
                    valor    = ti - ti_ant,
                    accion   = "Identificar causa del retroceso y activar medidas correctivas.",
                ))

    except Exception as e:
        alerts.append(_make_alert(
            tipo    = "ejecucion",
            status  = ERROR,
            entidad = "SISTEMA",
            titulo  = "Error al verificar ejecución",
            detalle = f"No se pudo consultar la base de datos: {str(e)[:120]}",
            periodo = "–",
            accion  = "Verificar conectividad con la base de datos.",
        ))
    return alerts


# ── ALERTAS DE COBERTURA DOCUMENTAL ──────────────────────────────────────────
def _check_cobertura() -> list[dict]:
    """
    Detecta entidades sin upload en el período operativo más reciente.
    Compara las 4 entidades esperadas vs las que tienen registro.
    """
    alerts = []
    try:
        conn = get_connection()
        c    = conn.cursor()

        # Período más reciente en document_uploads
        last = c.execute(
            "SELECT period_year as y, period_month as m "
            "FROM document_uploads WHERE period_month IS NOT NULL "
            "ORDER BY period_year DESC, period_month DESC LIMIT 1"
        ).fetchone()
        if not last:
            conn.close()
            return []

        year, month = last["y"], last["m"]
        periodo_lbl = _periodo_label(year, month)

        # Entidades con upload en ese período
        rows = c.execute(
            "SELECT DISTINCT entidad FROM document_uploads "
            "WHERE period_year=? AND period_month=?",
            (year, month),
        ).fetchall()
        entidades_con_doc = {r["entidad"] for r in rows}
        conn.close()

        faltantes = [e for e in EXPECTED_ENTITIES if e not in entidades_con_doc]

        for ent in faltantes:
            lbl = ENTITY_LABELS.get(ent, ent)
            alerts.append(_make_alert(
                tipo    = "cobertura",
                status  = WARNING,
                entidad = ent,
                titulo  = f"Evidencia mensual pendiente — {lbl}",
                detalle = (
                    f"No se encontró cédula presupuestaria cargada para "
                    f"{lbl} en {periodo_lbl}. "
                    f"El período está operativo en otras entidades del holding."
                ),
                periodo = periodo_lbl,
                accion  = f"Cargar la cédula eSIGEF de {lbl} para {periodo_lbl} en el Centro de Ingesta.",
            ))

    except Exception as e:
        alerts.append(_make_alert(
            tipo    = "cobertura",
            status  = ERROR,
            entidad = "SISTEMA",
            titulo  = "Error al verificar cobertura documental",
            detalle = f"No se pudo consultar registros de documentos: {str(e)[:120]}",
            periodo = "–",
            accion  = "Verificar conectividad con la base de datos.",
        ))
    return alerts


# ── PERSISTENCIA ─────────────────────────────────────────────────────────────
def _parse_periodo(periodo: str) -> tuple[int, int]:
    """Convierte 'Marzo 2026' → (2026, 3). Retorna (0, 0) si no parsea."""
    _MES_NUM = {v: k for k, v in MESES_ES.items()}
    parts = periodo.split()
    if len(parts) == 2:
        mes = _MES_NUM.get(parts[0])
        try:
            year = int(parts[1])
            if mes:
                return year, mes
        except ValueError:
            pass
    return 0, 0


def save_alerts(alerts: list[dict]) -> int:
    """
    Persiste alertas con lógica hash-aware:
      - Si el hash existe y estado != resuelta → actualiza detected_at (alerta viva)
      - Si el hash no existe → INSERT nueva alerta
      - Si cambia la severidad → nuevo hash → nueva alerta (la anterior queda histórica)
    Retorna el número de filas nuevas insertadas.

    Un fallo aquí NO se silencia (2026-08-06). Antes, un `except: pass` envolvía
    la inserción entera y también el `close()`: si algo fallaba a mitad, las
    alertas no se guardaban, nadie se enteraba y la conexión quedaba abierta.
    Una alerta que no se persiste y no avisa es peor que ninguna alerta — el
    sistema queda creyendo que vigiló.
    """
    inserted = 0
    conn = None
    try:
        conn = get_connection()
        c    = conn.cursor()
        now  = datetime.now().isoformat()

        for a in alerts:
            if a["entidad"] == "SISTEMA":
                continue
            year, month = _parse_periodo(a["periodo"])
            if year == 0:
                continue

            h = _alert_hash(a["entidad"], a["tipo"], year, month, a["severidad"])

            # ¿Existe ya una alerta con este hash?
            existing = c.execute(
                "SELECT id, estado FROM alerts_history WHERE hash_alerta=?", (h,)
            ).fetchone()

            if existing:
                if (existing["estado"] or "pendiente") != ESTADO_RESUELTA:
                    # Sigue activa — actualizar timestamp para que aparezca como reciente
                    c.execute(
                        "UPDATE alerts_history SET detected_at=? WHERE hash_alerta=?",
                        (now, h),
                    )
            else:
                # Nueva alerta
                if conn.mode == "supabase":
                    sql = """
                        INSERT INTO alerts_history
                            (detected_at, period_year, period_month, entidad, tipo,
                             status, severidad, titulo, detalle, accion, valor,
                             umbral, fuente_datos, hash_alerta, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendiente')
                        ON CONFLICT (period_year, period_month, entidad, tipo) DO NOTHING
                    """
                else:
                    sql = """
                        INSERT OR IGNORE INTO alerts_history
                            (detected_at, period_year, period_month, entidad, tipo,
                             status, severidad, titulo, detalle, accion, valor,
                             umbral, fuente_datos, hash_alerta, estado)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pendiente')
                    """
                c.execute(sql, (
                    now, year, month,
                    a["entidad"], a["tipo"], a["status"], a["severidad"],
                    a["titulo"], a.get("detalle", ""), a.get("accion", ""),
                    a.get("valor"), a.get("umbral"), a.get("fuente_datos", ""), h,
                ))
                if c.rowcount > 0:
                    inserted += 1
                    # RC-2A: Poblar campos SLA en la alerta recién insertada
                    try:
                        from sentinel.sla_db import update_alert_sla
                        new_row = c.execute(
                            "SELECT id, detected_at, severidad, entidad, estado, escalada "
                            "FROM alerts_history WHERE hash_alerta=?", (h,)
                        ).fetchone()
                        if new_row:
                            update_alert_sla(conn, new_row)
                    except Exception as _e:  # noqa: BLE001
                        # Sin plazo asignado la señal existe pero queda fuera
                        # del seguimiento de vencimientos: nadie la reclama.
                        _log.warning("señal guardada sin plazo de atención "
                                     "(%s: %s)", type(_e).__name__, _e)
                else:
                    # UNIQUE conflict con registro antiguo sin hash → backfill
                    c.execute(
                        "UPDATE alerts_history SET hash_alerta=?, umbral=?, fuente_datos=?, detected_at=? "
                        "WHERE period_year=? AND period_month=? AND entidad=? AND tipo=? "
                        "AND (hash_alerta IS NULL OR hash_alerta='')",
                        (h, a.get("umbral"), a.get("fuente_datos", ""), now,
                         year, month, a["entidad"], a["tipo"]),
                    )

        conn.commit()
    except Exception as e:  # noqa: BLE001
        _log.error("no se pudieron persistir %d alerta(s): %s: %s — "
                   "la vigilancia de este ciclo NO quedó registrada",
                   len(alerts), type(e).__name__, e)
    finally:
        # El cierre estaba dentro del `try`: un fallo previo dejaba la conexión
        # abierta y, con el pooler, esas conexiones se acumulan.
        if conn is not None:
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                _log.warning("no se pudo cerrar la conexión tras guardar alertas")
    return inserted


def auto_resolve_alerts(entidad: str, year: int, month: int,
                        tipo: str, ref: str = "auto") -> int:
    """
    Marca como resuelta la alerta de (entidad, year, month, tipo) si está pendiente.
    Retorna el número de alertas resueltas.
    """
    try:
        conn = get_connection()
        c    = conn.cursor()
        now  = datetime.now().isoformat()
        c.execute(
            "UPDATE alerts_history SET estado=?, resuelta_en=?, resuelta_ref=? "
            "WHERE period_year=? AND period_month=? AND entidad=? AND tipo=? "
            "AND estado IN (?, ?)",
            (ESTADO_RESUELTA, now, ref, year, month, entidad, tipo,
             ESTADO_ABIERTA, ESTADO_EN_REVISION),
        )
        resolved = c.rowcount
        conn.commit()
        conn.close()
        return resolved
    except Exception:
        return 0


def mark_en_revision(alert_id: int) -> bool:
    """Marca una alerta como 'en revisión'. Retorna True si actualizó."""
    try:
        conn = get_connection()
        c    = conn.cursor()
        c.execute(
            "UPDATE alerts_history SET estado=? WHERE id=? AND estado=?",
            (ESTADO_EN_REVISION, alert_id, ESTADO_ABIERTA),
        )
        ok = c.rowcount > 0
        conn.commit()
        conn.close()
        return ok
    except Exception:
        return False


def resolve_alert_with_comment(
    alert_id: int,
    resolucion: str,
    suggestion_used: bool = False,
    suggestion_category: str | None = None,
    suggestion_confidence: float | None = None,
    edited_before_submit: bool = False,
) -> bool:
    """
    Cierra una alerta con comentario humano institucional.
    Persiste trazabilidad de sugerencia (Sprint 2.8C) cuando se usa borrador.
    """
    try:
        conn = get_connection()
        c    = conn.cursor()
        now  = datetime.now().isoformat()
        try:
            c.execute(
                """UPDATE alerts_history
                   SET estado=?, resuelta_en=?, resolucion=?,
                       suggestion_used=?, suggestion_category=?,
                       suggestion_confidence=?, edited_before_submit=?
                   WHERE id=? AND estado != ?""",
                (
                    ESTADO_RESUELTA, now, resolucion.strip(),
                    1 if suggestion_used else 0,
                    suggestion_category,
                    suggestion_confidence,
                    1 if edited_before_submit else 0,
                    alert_id, ESTADO_RESUELTA,
                ),
            )
        except Exception:
            c.execute(
                "UPDATE alerts_history SET estado=?, resuelta_en=?, resolucion=? "
                "WHERE id=? AND estado != ?",
                (ESTADO_RESUELTA, now, resolucion.strip(), alert_id, ESTADO_RESUELTA),
            )
        ok = c.rowcount > 0
        conn.commit()
        conn.close()
        return ok
    except Exception:
        return False


def get_alerts_history(
    limit: int = 60,
    entidad: str = "",
    tipo: str = "",
    estado: str = "",
) -> list[dict]:
    """
    Retorna alertas del historial con filtros opcionales.
    """
    try:
        conn   = get_connection()
        c      = conn.cursor()
        where  = []
        params: list = []
        if entidad:
            where.append("entidad=?");  params.append(entidad)
        if tipo:
            where.append("tipo=?");     params.append(tipo)
        if estado:
            where.append("estado=?");   params.append(estado)
        clause = ("WHERE " + " AND ".join(where)) if where else ""
        rows   = c.execute(
            f"SELECT * FROM alerts_history {clause} ORDER BY detected_at DESC LIMIT ?",
            params + [limit],
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def get_alert_kpis() -> dict:
    """
    KPIs de resumen para el encabezado de /alertas:
      - criticas_activas, advertencias_activas, resueltas_este_mes, dias_abierta_max
    """
    try:
        from datetime import date
        conn   = get_connection()
        c      = conn.cursor()
        now_m  = date.today().strftime("%Y-%m")

        criticas   = c.execute(
            "SELECT COUNT(*) as n FROM alerts_history WHERE status='error' AND estado!=?",
            (ESTADO_RESUELTA,)
        ).fetchone()["n"]

        advertencias = c.execute(
            "SELECT COUNT(*) as n FROM alerts_history WHERE status='warning' AND estado!=?",
            (ESTADO_RESUELTA,)
        ).fetchone()["n"]

        resueltas_mes = c.execute(
            "SELECT COUNT(*) as n FROM alerts_history WHERE estado=? AND resuelta_en LIKE ?",
            (ESTADO_RESUELTA, f"{now_m}%")
        ).fetchone()["n"]

        # Alerta más antigua sin resolver
        oldest = c.execute(
            "SELECT MIN(detected_at) as ts FROM alerts_history WHERE estado!=?",
            (ESTADO_RESUELTA,)
        ).fetchone()["ts"]
        dias_max = 0
        if oldest:
            try:
                dias_max = (datetime.now() - datetime.fromisoformat(oldest[:19])).days
            except Exception:
                pass

        conn.close()
        return {
            "criticas_activas":    criticas,
            "advertencias_activas": advertencias,
            "resueltas_este_mes":  resueltas_mes,
            "dias_abierta_max":    dias_max,
        }
    except Exception:
        return {"criticas_activas": 0, "advertencias_activas": 0,
                "resueltas_este_mes": 0, "dias_abierta_max": 0}


def get_tendencias() -> list[dict]:
    """
    Analiza meses consecutivos en rojo por entidad.
    Retorna una lista de tendencias relevantes para mostrar en UI.
    """
    tendencias = []
    conn = None
    try:
        conn = get_connection()
        c    = conn.cursor()

        for ent in EXPECTED_ENTITIES:
            rows = c.execute(
                "SELECT period_year, period_month, status, severidad "
                "FROM alerts_history WHERE entidad=? AND tipo='ejecucion' "
                "ORDER BY period_year DESC, period_month DESC LIMIT 6",
                (ent,),
            ).fetchall()
            if not rows:
                continue

            # Meses consecutivos en crítico
            consecutivos_rojo = 0
            for r in rows:
                if r["status"] == "error":
                    consecutivos_rojo += 1
                else:
                    break

            # Tendencia de valor (último vs primero de la serie)
            vals = c.execute(
                "SELECT valor FROM alerts_history WHERE entidad=? AND tipo='ejecucion' "
                "AND valor IS NOT NULL ORDER BY period_year ASC, period_month ASC LIMIT 3",
                (ent,),
            ).fetchall()

            if consecutivos_rojo >= 2:
                tendencias.append({
                    "entidad":       ent,
                    "entidad_label": ENTITY_LABELS.get(ent, ent),
                    "tipo":          "consecutivo_rojo",
                    "meses":         consecutivos_rojo,
                    "mensaje":       f"{consecutivos_rojo} meses consecutivos en zona crítica",
                    "status":        "error",
                })
            elif len(vals) >= 2:
                v_ini = vals[0]["valor"]
                v_fin = vals[-1]["valor"]
                if v_ini is not None and v_fin is not None and v_fin > v_ini + 1.0:
                    delta = v_fin - v_ini
                    tendencias.append({
                        "entidad":       ent,
                        "entidad_label": ENTITY_LABELS.get(ent, ent),
                        "tipo":          "mejora",
                        "delta":         delta,
                        "mensaje":       f"Mejora sostenida +{delta:.1f} pp en la serie histórica",
                        "status":        "warning",
                    })

    except Exception as e:  # noqa: BLE001
        _log.warning("no se pudo calcular la tendencia institucional: %s: %s — "
                     "se devuelve lo obtenido hasta el fallo, no una serie "
                     "completa", type(e).__name__, e)
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:  # noqa: BLE001
                pass
    return tendencias


# ── SPRINT 2.6.2 — ANALYTICS DE SEGUIMIENTO INSTITUCIONAL ────────────────────

def get_aging_report() -> dict:
    """
    Métricas de aging del backlog activo y del historial resuelto.
    Útil para: alcalde, dirección financiera, auditoría, Contraloría.
    """
    today = datetime.now()
    try:
        conn = get_connection()
        c    = conn.cursor()
        rows = c.execute(
            "SELECT entidad, estado, detected_at, resuelta_en, status "
            "FROM alerts_history"
        ).fetchall()
        conn.close()

        active: list   = []
        resolved: list = []
        for r in rows:
            d   = dict(r)
            det = (d.get("detected_at") or "")[:19]
            if d["estado"] in (ESTADO_ABIERTA, ESTADO_EN_REVISION):
                try:
                    dias = max(0, (today - datetime.fromisoformat(det)).days)
                    d["dias_abierta"] = dias
                    active.append(d)
                except Exception:
                    pass
            elif d["estado"] == ESTADO_RESUELTA:
                res = (d.get("resuelta_en") or "")[:19]
                try:
                    d_res = max(0, (
                        datetime.fromisoformat(res) - datetime.fromisoformat(det)
                    ).days)
                    d["dias_resolucion"] = d_res
                    resolved.append(d)
                except Exception:
                    pass

        backlog  = len(active)
        dias_max = max((a["dias_abierta"] for a in active), default=0)
        dias_avg = round(sum(a["dias_abierta"] for a in active) / backlog, 1) if backlog else 0
        res_avg  = (
            round(sum(r["dias_resolucion"] for r in resolved) / len(resolved), 1)
            if resolved else 0
        )

        ent_data: dict = {}
        for a in active:
            ent = a["entidad"]
            if ent not in ent_data:
                ent_data[ent] = {"n": 0, "dias": [], "n_criticas": 0}
            ent_data[ent]["n"] += 1
            ent_data[ent]["dias"].append(a["dias_abierta"])
            if a.get("status") == ERROR:
                ent_data[ent]["n_criticas"] += 1

        por_entidad = sorted([
            {
                "entidad":       ent,
                "n_abiertas":    ed["n"],
                "n_criticas":    ed["n_criticas"],
                "dias_max":      max(ed["dias"], default=0),
                "dias_promedio": round(sum(ed["dias"]) / len(ed["dias"]), 1) if ed["dias"] else 0,
            }
            for ent, ed in ent_data.items()
        ], key=lambda x: (-x["dias_max"], -x["n_criticas"]))

        return {
            "backlog_total":       backlog,
            "dias_max":            dias_max,
            "dias_promedio":       dias_avg,
            "resolucion_promedio": res_avg,
            "total_resueltas":     len(resolved),
            "por_entidad":         por_entidad,
        }
    except Exception:
        return {
            "backlog_total": 0, "dias_max": 0, "dias_promedio": 0,
            "resolucion_promedio": 0, "total_resueltas": 0, "por_entidad": [],
        }


def get_reincidencia(min_meses: int = 2) -> list[dict]:
    """
    Detecta entidades con alertas del mismo tipo en múltiples períodos.
    min_meses=2 → incidencia repetida; ≥3 → patrón estructural.
    """
    try:
        conn = get_connection()
        c    = conn.cursor()
        rows = c.execute(
            "SELECT entidad, tipo, period_year, period_month, status "
            "FROM alerts_history ORDER BY entidad, tipo, period_year, period_month"
        ).fetchall()
        conn.close()

        from collections import defaultdict
        groups: dict = defaultdict(list)
        for r in rows:
            d = dict(r)
            groups[(d["entidad"], d["tipo"])].append(
                (d["period_year"], d["period_month"], d.get("status", ""))
            )

        result = []
        for (ent, tipo), periods in groups.items():
            seen: set = set()
            unique: list = []
            for p in periods:
                k = (p[0], p[1])
                if k not in seen:
                    seen.add(k)
                    unique.append(p)
            if len(unique) < min_meses:
                continue

            unique.sort(key=lambda x: (x[0], x[1]))
            n_criticas = sum(1 for p in unique if p[2] == ERROR)
            primera = f"{unique[0][1]:02d}/{unique[0][0]}"
            ultima  = f"{unique[-1][1]:02d}/{unique[-1][0]}"

            result.append({
                "entidad":       ent,
                "entidad_label": ENTITY_LABELS.get(ent, ent),
                "tipo":          tipo,
                "n_periodos":    len(unique),
                "n_criticas":    n_criticas,
                "primera_vez":   primera,
                "ultima_vez":    ultima,
                "es_patron":     len(unique) >= 3,
                "status":        ERROR if n_criticas >= max(1, len(unique) // 2) else WARNING,
            })

        result.sort(key=lambda x: (-x["n_periodos"], -x["n_criticas"]))
        return result
    except Exception:
        return []


def get_ranking_riesgo() -> list[dict]:
    """
    Score compuesto de riesgo institucional por entidad.
    Formula: (criticas×3) + (advertencias×1) + (dias_max//15) + (reincidencias×2)
    Nivel: ERROR ≥6, WARNING ≥2, OK <2.
    """
    try:
        aging_data   = get_aging_report()
        reincidencias = get_reincidencia(min_meses=1)

        ent_score: dict = {e: {
            "score": 0, "n_criticas": 0, "n_advertencias": 0,
            "dias_max": 0, "meses_reincidencia": 0,
        } for e in EXPECTED_ENTITIES}

        for ed in aging_data["por_entidad"]:
            ent = ed["entidad"]
            if ent in ent_score:
                nc = ed["n_criticas"]
                na = ed["n_abiertas"] - nc
                dm = ed["dias_max"]
                ent_score[ent]["n_criticas"]    += nc
                ent_score[ent]["n_advertencias"] += na
                ent_score[ent]["dias_max"]        = max(ent_score[ent]["dias_max"], dm)
                ent_score[ent]["score"]           += nc * 3 + na * 1 + dm // 15

        for r in reincidencias:
            ent = r["entidad"]
            if ent in ent_score:
                ent_score[ent]["meses_reincidencia"] = max(
                    ent_score[ent]["meses_reincidencia"], r["n_periodos"]
                )
                ent_score[ent]["score"] += r["n_periodos"] * 2

        ranking = []
        for ent, s in sorted(ent_score.items(), key=lambda x: -x[1]["score"]):
            nivel = ERROR if s["score"] >= 6 else (WARNING if s["score"] >= 2 else OK)
            ranking.append({
                "entidad":            ent,
                "entidad_label":      ENTITY_LABELS.get(ent, ent),
                "score":              s["score"],
                "n_criticas":         s["n_criticas"],
                "n_advertencias":     s["n_advertencias"],
                "dias_max":           s["dias_max"],
                "meses_reincidencia": s["meses_reincidencia"],
                "nivel":              nivel,
            })
        return ranking
    except Exception:
        return []


def get_alertas_sin_resolver(umbral_dias: int = 45) -> list[dict]:
    """
    Alertas activas abiertas por más de umbral_dias días.
    Señal de abandono institucional, cuello de botella o simulación de cumplimiento.
    """
    today = datetime.now()
    try:
        conn = get_connection()
        c    = conn.cursor()
        rows = c.execute(
            "SELECT id, entidad, tipo, titulo, severidad, status, detected_at, estado "
            "FROM alerts_history WHERE estado IN (?, ?) ORDER BY detected_at ASC",
            (ESTADO_ABIERTA, ESTADO_EN_REVISION),
        ).fetchall()
        conn.close()

        result = []
        for r in rows:
            d = dict(r)
            try:
                det  = (d.get("detected_at") or "")[:19]
                dias = (today - datetime.fromisoformat(det)).days
                if dias >= umbral_dias:
                    d["dias_abierta"] = dias
                    result.append(d)
            except Exception:
                pass
        return result
    except Exception:
        return []


# ── PUNTO DE ENTRADA ─────────────────────────────────────────────────────────
def run_alert_check() -> dict:
    """
    Ejecuta todos los checks de alerta, persiste en alerts_history y retorna
    resultado agregado.
    """
    alerts: list[dict] = []
    alerts.extend(_check_ejecucion())
    alerts.extend(_check_cobertura())

    # Ordenar: críticas primero, luego por entidad
    _order = {ERROR: 0, WARNING: 1, OK: 2}
    alerts.sort(key=lambda a: (_order.get(a["status"], 9), a["entidad"]))

    # Persistir (idempotente — duplicados ignorados)
    save_alerts(alerts)

    n_error   = sum(1 for a in alerts if a["status"] == ERROR)
    n_warning = sum(1 for a in alerts if a["status"] == WARNING)
    n_total   = len(alerts)

    if n_error > 0:
        status, label, emoji = ERROR, "Alertas Críticas Activas", "🔴"
    elif n_warning > 0:
        status, label, emoji = WARNING, "Advertencias Activas", "🟡"
    else:
        status, label, emoji = OK, "Sin Alertas Activas", "🟢"

    return {
        "alerts":     alerts,
        "n_error":    n_error,
        "n_warning":  n_warning,
        "n_total":    n_total,
        "status":     status,
        "label":      label,
        "emoji":      emoji,
        "ts_display": datetime.now().strftime("%d %b %Y, %H:%M"),
    }
