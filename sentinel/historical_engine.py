"""
sentinel/historical_engine.py
Motor de inteligencia histórica — Sprint 2.5B

Análisis del Holding Municipal de Montecristi:
    GAD · BOMBEROS · EMAI-EP · PATRONATO

Funciones principales:
    get_resumen_holding()     → KPIs consolidados por mes
    get_tendencia_entidad()   → Serie temporal Ti por entidad
    get_ranking_categorias()  → Top partidas por devengado
    detect_alertas()          → Semáforo 🔴🟡🟢 automático
    get_holding_totales()     → Acumulados anuales del holding

Dylus Lab © 2026
"""
from __future__ import annotations

from typing import Optional

from sentinel.db_config import get_connection

ENTIDADES = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]

ALERTAS_UMBRALES = {
    "rojo":    15.0,   # Ti < 15% → alerta crítica
    "amarillo": 35.0,  # Ti < 35% → precaución
}


# ── RESUMEN HOLDING ───────────────────────────────────────────────────────────
def get_resumen_holding(year: int) -> list[dict]:
    """
    KPIs consolidados por mes para todo el holding.
    Retorna lista ordenada por mes con totales de las 4 entidades.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            k.period_month,
            SUM(k.codificado_total)  AS codificado_total,
            SUM(k.devengado_total)   AS devengado_total,
            SUM(k.codificado_inv)    AS codificado_inv,
            SUM(k.devengado_inv)     AS devengado_inv,
            COUNT(DISTINCT k.entidad) AS entidades_count
        FROM monthly_kpis k
        WHERE k.period_year = ?
        GROUP BY k.period_month
        ORDER BY k.period_month
    """, (year,)).fetchall()
    conn.close()

    result = []
    for r in rows:
        cod_inv = r["codificado_inv"] or 0.0
        dev_inv = r["devengado_inv"]  or 0.0
        ti = round(dev_inv / cod_inv * 100, 2) if cod_inv > 0 else 0.0
        result.append({
            "month":           r["period_month"],
            "codificado_total": round(r["codificado_total"] or 0, 2),
            "devengado_total":  round(r["devengado_total"]  or 0, 2),
            "codificado_inv":   round(cod_inv, 2),
            "devengado_inv":    round(dev_inv, 2),
            "ti_holding":       ti,
            "entidades_count":  r["entidades_count"],
        })
    return result


# ── TENDENCIA POR ENTIDAD ─────────────────────────────────────────────────────
def get_tendencia_entidad(year: int) -> dict[str, list[dict]]:
    """
    Serie temporal de Ti mensual por entidad.
    Retorna dict: entidad → [{"month": int, "ti": float, ...}, ...]
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            k.entidad,
            k.period_month,
            k.ti_mensual_pct,
            k.ti_acumulado_pct,
            k.codificado_total,
            k.devengado_total,
            k.codificado_inv,
            k.devengado_inv
        FROM monthly_kpis k
        WHERE k.period_year = ?
        ORDER BY k.entidad, k.period_month
    """, (year,)).fetchall()
    conn.close()

    result: dict[str, list] = {e: [] for e in ENTIDADES}
    for r in rows:
        entidad = r["entidad"]
        if entidad not in result:
            result[entidad] = []
        result[entidad].append({
            "month":           r["period_month"],
            "ti":              r["ti_mensual_pct"]  or 0.0,
            "ti_acumulado":    r["ti_acumulado_pct"] or 0.0,
            "codificado_total": r["codificado_total"] or 0.0,
            "devengado_total":  r["devengado_total"]  or 0.0,
            "codificado_inv":   r["codificado_inv"]   or 0.0,
            "devengado_inv":    r["devengado_inv"]    or 0.0,
        })
    return result


# ── RANKING POR ENTIDAD ───────────────────────────────────────────────────────
def get_ranking_entidades(year: int) -> list[dict]:
    """
    Ranking de entidades por Ti acumulado del año.
    Incluye totales de ejecución para contexto.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            k.entidad,
            MAX(k.period_month)   AS ultimo_mes,
            MAX(k.ti_acumulado_pct) AS ti_acumulado,
            SUM(k.codificado_inv)  AS codificado_inv_total,
            SUM(k.devengado_inv)   AS devengado_inv_total,
            SUM(k.codificado_total) AS codificado_total,
            SUM(k.devengado_total)  AS devengado_total
        FROM monthly_kpis k
        WHERE k.period_year = ?
        GROUP BY k.entidad
        ORDER BY ti_acumulado DESC
    """, (year,)).fetchall()
    conn.close()

    result = []
    for i, r in enumerate(rows, 1):
        cod_inv = r["codificado_inv_total"] or 0.0
        dev_inv = r["devengado_inv_total"]  or 0.0
        ti_real = round(dev_inv / cod_inv * 100, 2) if cod_inv > 0 else 0.0
        result.append({
            "rank":            i,
            "entidad":         r["entidad"],
            "ultimo_mes":      r["ultimo_mes"],
            "ti_acumulado":    r["ti_acumulado"]  or 0.0,
            "ti_real":         ti_real,
            "codificado_inv":  round(cod_inv, 2),
            "devengado_inv":   round(dev_inv, 2),
            "codificado_total": round(r["codificado_total"] or 0, 2),
            "devengado_total":  round(r["devengado_total"]  or 0, 2),
        })
    return result


# ── ALERTAS AUTOMÁTICAS ───────────────────────────────────────────────────────
def detect_alertas(year: int, month: Optional[int] = None) -> list[dict]:
    """
    Semáforo automático por entidad.
    Si month=None, usa el último mes disponible por entidad.

    Returns:
        Lista de dicts con: entidad, ti, semaforo (rojo/amarillo/verde), mensaje
    """
    conn = get_connection()
    if month:
        rows = conn.execute("""
            SELECT entidad,
                   AVG(ti_mensual_pct)  AS ti_mensual_pct,
                   AVG(ti_acumulado_pct) AS ti_acumulado_pct,
                   period_month
            FROM monthly_kpis
            WHERE period_year=? AND period_month=?
            GROUP BY entidad, period_month
            ORDER BY entidad
        """, (year, month)).fetchall()
    else:
        rows = conn.execute("""
            SELECT entidad,
                   AVG(ti_mensual_pct)  AS ti_mensual_pct,
                   AVG(ti_acumulado_pct) AS ti_acumulado_pct,
                   MAX(period_month)     AS period_month
            FROM monthly_kpis
            WHERE period_year=?
              AND period_month = (
                  SELECT MAX(m2.period_month) FROM monthly_kpis m2
                  WHERE m2.period_year=? AND m2.entidad=monthly_kpis.entidad
              )
            GROUP BY entidad
            ORDER BY entidad
        """, (year, year)).fetchall()
    conn.close()

    alertas = []
    for r in rows:
        ti  = r["ti_mensual_pct"] or 0.0
        mes = r["period_month"]

        if ti < ALERTAS_UMBRALES["rojo"]:
            semaforo = "rojo"
            msg = f"Ejecución crítica: Ti={ti:.1f}% — requiere acción inmediata"
        elif ti < ALERTAS_UMBRALES["amarillo"]:
            semaforo = "amarillo"
            msg = f"Ejecución baja: Ti={ti:.1f}% — monitoreo recomendado"
        else:
            semaforo = "verde"
            msg = f"Ejecución normal: Ti={ti:.1f}%"

        alertas.append({
            "entidad":   r["entidad"],
            "mes":       mes,
            "ti":        round(ti, 2),
            "semaforo":  semaforo,
            "mensaje":   msg,
        })
    return alertas


# ── TOTALES ANUALES DEL HOLDING ───────────────────────────────────────────────
def get_holding_totales(year: int) -> dict:
    """
    Acumulados consolidados del año para el holding completo.
    Usa el último mes disponible de cada entidad.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            SUM(k.codificado_total) AS codificado_total,
            SUM(k.devengado_total)  AS devengado_total,
            SUM(k.codificado_inv)   AS codificado_inv,
            SUM(k.devengado_inv)    AS devengado_inv,
            COUNT(DISTINCT k.entidad) AS num_entidades,
            MAX(k.period_month)     AS ultimo_mes
        FROM monthly_kpis k
        WHERE k.period_year = ?
          AND (k.entidad, k.period_month) IN (
              SELECT entidad, MAX(period_month)
              FROM monthly_kpis
              WHERE period_year=?
              GROUP BY entidad
          )
    """, (year, year)).fetchone()
    conn.close()

    if not rows:
        return {}

    cod_inv = rows["codificado_inv"] or 0.0
    dev_inv = rows["devengado_inv"]  or 0.0
    cod_tot = rows["codificado_total"] or 0.0
    dev_tot = rows["devengado_total"]  or 0.0

    return {
        "year":             year,
        "ultimo_mes":       rows["ultimo_mes"],
        "num_entidades":    rows["num_entidades"],
        "codificado_total": round(cod_tot, 2),
        "devengado_total":  round(dev_tot, 2),
        "codificado_inv":   round(cod_inv, 2),
        "devengado_inv":    round(dev_inv, 2),
        "ti_holding":       round(dev_inv / cod_inv * 100, 2) if cod_inv > 0 else 0.0,
        "ejec_total":       round(dev_tot / cod_tot * 100, 2) if cod_tot > 0 else 0.0,
    }


# ── DISPONIBILIDAD POR ENTIDAD ────────────────────────────────────────────────
def get_meses_disponibles(year: int) -> dict[str, list[int]]:
    """
    Retorna los meses disponibles por entidad para el año dado.
    Útil para saber qué cédulas faltan.
    """
    conn = get_connection()
    rows = conn.execute("""
        SELECT DISTINCT entidad, period_month
        FROM monthly_kpis
        WHERE period_year = ?
        ORDER BY entidad, period_month
    """, (year,)).fetchall()
    conn.close()

    result: dict[str, list] = {e: [] for e in ENTIDADES}
    for r in rows:
        entidad = r["entidad"]
        if entidad not in result:
            result[entidad] = []
        result[entidad].append(r["period_month"])
    return result
