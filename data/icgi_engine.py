"""
QUIRA OS v0.1 — Motor ICGI-T
Proyecciones, deltas históricos, cálculo de impacto SAT
Dylus Lab © 2026
"""
from typing import Optional
from data.demo_data import ICGIT_Q1_2026
from data.loader import classify_avep


# ── HISTÓRICO & PROYECCIÓN ─────────────────────────────────────────────────────
def historico_series(icgit: dict) -> tuple[list[str], list[float]]:
    """
    Devuelve (labels, valores) para el gráfico histórico ICGI-T.
    Incluye 2023, 2024, 2025, Q1-2026 real y proyección 2026.
    """
    h = icgit.get("historico", {})
    labels = ["2023", "2024", "2025", "Q1-2026", "2026 proj."]
    values = [
        h.get("2023", 57.36),
        h.get("2024", 67.11),
        h.get("2025", 69.93),
        h.get("2026_q1", icgit["score"]),
        h.get("2026_proj", icgit.get("proyeccion", 65.77)),
    ]
    return labels, values


def delta_yoy(icgit: dict) -> float:
    """Delta ICGI-T Q1-2026 vs. 2025 anual."""
    h = icgit.get("historico", {})
    return round(icgit["score"] - h.get("2025", 69.93), 2)


def ritmo_ejecucion(icgit: dict) -> dict:
    """
    Analiza el ritmo de ejecución presupuestal.
    Distingue ti_raw (% real) de ti_norm (% normalizado para la fecha).
    """
    ti_raw  = icgit.get("ti_raw", 0)
    ti_norm = icgit.get("ti_norm", 0)
    meta    = icgit.get("meta_mandato", 70.0)

    brecha_raw  = round(meta - ti_raw, 2)
    brecha_norm = round(meta - ti_norm, 2)

    return {
        "ti_raw":      ti_raw,
        "ti_norm":     ti_norm,
        "brecha_raw":  brecha_raw,
        "brecha_norm": brecha_norm,
        "ok_ritmo":    ti_norm >= meta,
        "semaforo":    "🟢" if ti_norm >= meta else ("🟡" if ti_norm >= 50 else "🔴"),
    }


def proyeccion_cierre(icgit: dict) -> dict:
    """Proyección de cierre 2026 con contexto AVEP."""
    proj  = icgit.get("proyeccion", 65.77)
    meta  = icgit.get("meta_mandato", 70.0)
    band  = classify_avep(proj)
    delta = round(proj - meta, 2)
    return {
        "proyeccion": proj,
        "meta":       meta,
        "delta":      delta,
        "on_track":   proj >= meta,
        "avep":       band["label"],
        "color":      band["color"],
        "emoji":      band["emoji"],
    }


# ── IMPACTO SAT ────────────────────────────────────────────────────────────────
def sat_impact_total(sat_list: list[dict]) -> float:
    """
    Calcula impacto total de SATs activas sobre ICGI-T.
    Extrae el valor numérico de campos tipo '−8.2 pts ICGI-T'.
    """
    total = 0.0
    for sat in sat_list:
        if sat.get("estado") == "ACTIVA":
            impacto = sat.get("impacto", "")
            # Extrae primer número negativo del string
            import re
            match = re.search(r"[−\-]([\d.]+)\s*pts", impacto)
            if match:
                total -= float(match.group(1))
    return round(total, 2)


def sat_priority_sort(sat_list: list[dict]) -> list[dict]:
    """Ordena SATs: CRÍTICO primero, luego ALERTA."""
    order = {"CRÍTICO": 0, "ALERTA": 1}
    return sorted(sat_list, key=lambda s: order.get(s.get("nivel", "ALERTA"), 2))


# ── SCORECARD EJECUTIVO ────────────────────────────────────────────────────────
def build_scorecard(data: dict) -> dict:
    """
    Consolida los KPIs clave para el dashboard ejecutivo (P-01).
    """
    icgit  = data["icgit"]
    indices = data["indices"]
    sat    = data["sat"]
    sat_counts = {
        "criticos":    sum(1 for s in sat if s["nivel"] == "CRÍTICO"),
        "alertas":     sum(1 for s in sat if s["nivel"] == "ALERTA"),
    }

    ritmo = ritmo_ejecucion(icgit)
    proj  = proyeccion_cierre(icgit)

    # Índices críticos (🔴)
    criticos_indices = [
        (k, v) for k, v in indices.items()
        if v.get("valor") is not None and v["valor"] < 20
    ]

    return {
        "icgit_score":     icgit["score"],
        "icgit_avep":      icgit["avep"],
        "icgit_emoji":     icgit.get("avep_emoji", "🟡"),
        "icgit_color":     icgit.get("color", "#D69E2E"),
        "delta_yoy":       delta_yoy(icgit),
        "ritmo":           ritmo,
        "proyeccion":      proj,
        "sat_criticos":    sat_counts["criticos"],
        "sat_alertas":     sat_counts["alertas"],
        "sat_impact":      sat_impact_total(sat),
        "criticos_indices": criticos_indices,
        "presupuesto":     icgit.get("presupuesto_total", 0),
        "ejecutado":       icgit.get("inversion_ejecutada", 0),
        "pct_ejecutado":   round(
            icgit.get("inversion_ejecutada", 0) /
            max(icgit.get("presupuesto_total", 1), 1) * 100, 2
        ),
    }


# ── HOLDING ANALYTICS ─────────────────────────────────────────────────────────
def holding_stats(holding: dict) -> dict:
    """Estadísticas del holding municipal (HPT-M)."""
    entidades = holding.get("entidades", [])
    scores    = [e["score"] for e in entidades]
    avg       = round(sum(scores) / len(scores), 2) if scores else 0
    band      = classify_avep(avg)
    alerts    = [e for e in entidades if e.get("alerta")]

    return {
        "promedio":     avg,
        "avep":         band["label"],
        "color":        band["color"],
        "emoji":        band["emoji"],
        "total":        len(entidades),
        "en_alerta":    len(alerts),
        "max_score":    max(scores) if scores else 0,
        "min_score":    min(scores) if scores else 0,
        "icgit_global": holding.get("icgit_global", 53.56),
    }


# ── GEOTWIN ANALYTICS ─────────────────────────────────────────────────────────
def geotwin_stats(parroquias: list[dict]) -> dict:
    """Estadísticas territoriales GeoTwin para P-04."""
    total_inv  = sum(p.get("inversion", 0) for p in parroquias)
    total_hab  = sum(p.get("habitantes", 0) for p in parroquias)
    per_capitas = [p.get("per_capita", 0) for p in parroquias]
    sin_voz    = [p for p in parroquias if p.get("participacion", {}).get("estado") == "Sin voz"]
    emergencia = [p for p in parroquias if p.get("estado") == "EMERGENCIA"]

    max_pc = max(per_capitas) if per_capitas else 0
    min_pc = min(per_capitas) if per_capitas else 0
    brecha_pc = round(max_pc / max_pc * 100, 1) if max_pc else 0  # relative to max

    return {
        "total_inversion":    total_inv,
        "total_habitantes":   total_hab,
        "per_capita_max":     max_pc,
        "per_capita_min":     min_pc,
        "brecha_territorial": round(max_pc - min_pc, 0),
        "ratio_cabecera":     round(max_pc / max(min_pc, 1), 1),
        "parroquias_sin_voz": len(sin_voz),
        "parroquias_emergencia": len(emergencia),
        "n_total":            len(parroquias),
    }


# ── DELTA FORMATTER ───────────────────────────────────────────────────────────
def fmt_delta(value: float, reverse: bool = False) -> tuple[str, str]:
    """
    Formatea un delta numérico.
    reverse=True invierte el color (útil para brechas donde mayor es peor).
    Returns (texto, color_hex)
    """
    if value > 0:
        color = "#E53E3E" if reverse else "#38A169"
        return f"+{value:.2f}", color
    elif value < 0:
        color = "#38A169" if reverse else "#E53E3E"
        return f"{value:.2f}", color
    else:
        return "0.00", "#718096"
