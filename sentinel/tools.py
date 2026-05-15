"""
SENTINEL · tools.py
Typed data getters que Sentinel invoca internamente.
Fuente única: data.loader → demo_data.py → Gold Master v4.1 (H73 + H99)
Dylus Lab © 2026
"""
from __future__ import annotations
from data.loader import load_all


# ── get_indicator ──────────────────────────────────────────────────────────────
def get_indicator(name: str) -> dict | None:
    """
    Retorna el dict completo de un índice por su clave (H73_OUTPUT_API).

    Args:
        name: Clave del índice, p.ej. "PSG", "IGP", "IET", "ISP", "IOC"

    Returns:
        dict con keys: nombre, valor, avep, descripcion (si disponible) | None
    """
    data = load_all()
    ind  = data["indices"].get(name.upper())
    if ind is None:
        # Intentar búsqueda parcial
        for k, v in data["indices"].items():
            if name.upper() in k or name.upper() in v.get("nombre", "").upper():
                return {"_key": k, **v}
    return ind


# ── get_parroquia ──────────────────────────────────────────────────────────────
def get_parroquia(name: str) -> dict | None:
    """
    Retorna los datos de una parroquia por nombre (H99_ENGINE_CORE).

    Args:
        name: Nombre o fragmento del nombre de la parroquia.

    Returns:
        dict con keys: nombre, tps, nbi, agua, inversion, habitantes,
                       per_capita, estado, participacion | None
    """
    data = load_all()
    name_lo = name.lower()
    # Búsqueda exacta primero
    for p in data["parroquias"]:
        if p["nombre"].lower() == name_lo:
            return p
    # Búsqueda parcial
    for p in data["parroquias"]:
        if name_lo in p["nombre"].lower():
            return p
    return None


# ── get_sat_alerts ─────────────────────────────────────────────────────────────
def get_sat_alerts(nivel: str | None = None) -> list[dict]:
    """
    Retorna las alertas SAT activas, opcionalmente filtradas por nivel.

    Args:
        nivel: "CRÍTICO", "ALTO", "MEDIO" o None para todas.

    Returns:
        Lista de dicts con keys: id, nombre, nivel, descripcion, direccion
    """
    data = load_all()
    sat  = data.get("sat", [])
    if nivel:
        sat = [s for s in sat if s.get("nivel", "").upper() == nivel.upper()]
    return sat


# ── get_budget_gap ─────────────────────────────────────────────────────────────
def get_budget_gap() -> dict:
    """
    Retorna análisis de brecha presupuestaria y regresividad territorial.
    Fuente: H73_OUTPUT_API + H99_ENGINE_CORE (Gold Master v4.1)

    Returns:
        dict con:
          - brecha_fondos_bloqueados: $ bloqueados por mal PSG/ISP
          - irs_global: Índice de Regresividad Social (0-100)
          - irs_clasificacion: etiqueta AVEP del IRS
          - psg: Presupuesto Sensible al Género (%)
          - isp: Inversión en Salud (%)
          - parroquia_peor: parroquia con mayor vulnerabilidad
          - per_capita_min: menor inversión per cápita ($/hab)
          - per_capita_max: mayor inversión per cápita ($/hab)
    """
    from data.demo_data import (
        BRECHA_FONDOS_BLOQ, IRS_GLOBAL, IRS_CLASIFICACION
    )
    data = load_all()
    indices    = data["indices"]
    parroquias = data["parroquias"]

    psg_val = indices.get("PSG", {}).get("valor")
    isp_val = indices.get("ISP", {}).get("valor")

    parr_sorted = sorted(parroquias, key=lambda p: p["tps"], reverse=True)
    peor        = parr_sorted[0] if parr_sorted else {}

    per_capitas = [p["per_capita"] for p in parroquias if p.get("per_capita", 0) > 0]

    return {
        "brecha_fondos_bloqueados": BRECHA_FONDOS_BLOQ,
        "irs_global":              IRS_GLOBAL,
        "irs_clasificacion":       IRS_CLASIFICACION,
        "psg":                     psg_val,
        "isp":                     isp_val,
        "parroquia_peor":          peor.get("nombre"),
        "tps_peor":                peor.get("tps"),
        "per_capita_min":          min(per_capitas) if per_capitas else None,
        "per_capita_max":          max(per_capitas) if per_capitas else None,
        "n_sat_criticas":          len(get_sat_alerts("CRÍTICO")),
    }


# ── get_all_context ────────────────────────────────────────────────────────────
def get_all_context() -> dict:
    """
    Snapshot completo del sistema para el system prompt de Sentinel.
    Une H73 (indices), H99 (parroquias), SAT y ICGI-T en un solo dict.
    """
    data = load_all()
    return {
        "icgit":      data["icgit"],
        "indices":    data["indices"],
        "sat":        data["sat"],
        "parroquias": data["parroquias"],
        "budget_gap": get_budget_gap(),
    }
