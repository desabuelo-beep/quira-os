"""
sentinel/d4_loader.py
RC-D4 Data Loader — QUIRA OS
Carga datos parroquiales desde gm_snapshot.json → ejecuta pipeline D4 completo.

API principal:
  run_d4_pipeline(snapshot=None) → CalibratedD4Result | None
  get_d4_context_for_query(query, cr=None) → str   (inyección en Claude Haiku)

Doctrina: el loader no modifica datos — traduce el snapshot al lenguaje del motor.
Fuente canónica: gm_snapshot.territorial.parroquias (salidas Gold Master v5.5).

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from sentinel.d4_engine      import ParishRecord, analyze_territory
from sentinel.d4_patterns    import detect_d4_patterns
from sentinel.d4_calibration import CalibratedD4Result, calibrate_d4, describe_d4_calibrated

# ── RUTA SNAPSHOT ──────────────────────────────────────────────────────────────
_SNAPSHOT_PATH = Path(__file__).parent.parent / "data" / "gm_snapshot.json"

# Cache de sesión simple — None = aún no corrido, False = pipeline falló
_CACHED_D4: Optional[CalibratedD4Result] = None
_PIPELINE_RAN = False


# ── CARGA SNAPSHOT ─────────────────────────────────────────────────────────────

def _load_snapshot(snapshot: Optional[dict] = None) -> dict:
    if snapshot is not None:
        return snapshot
    with open(_SNAPSHOT_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_parish_records(snapshot: Optional[dict] = None) -> List[ParishRecord]:
    """
    Convierte gm_snapshot.territorial.parroquias → list[ParishRecord].
    Usa inv_percapita_q1 como proxy de inversión per cápita (H99_ENGINE_CORE).
    Silencia silenciosamente filas con datos faltantes o corruptos.
    """
    data      = _load_snapshot(snapshot)
    parroquias = data.get("territorial", {}).get("parroquias", [])

    records: List[ParishRecord] = []
    for p in parroquias:
        try:
            r = ParishRecord(
                id                 = str(p["id"]),
                nombre             = str(p["nombre"]),
                tipo               = str(p["tipo"]),               # "Urbana" | "Rural"
                poblacion          = int(p["poblacion_2022"]),
                nbi_pct            = float(p["nbi_pct"]),
                cobertura_agua_pct = float(p["cobertura_agua_pct"]),
                inv_percapita      = float(p["inv_percapita_q1"]),
                iet_local_pct      = float(p.get("iet_local_pct", 0.0)),
            )
            records.append(r)
        except (KeyError, ValueError, TypeError):
            continue   # dato corrupto — no bloquear pipeline

    return records


# ── PIPELINE COMPLETO D4 ───────────────────────────────────────────────────────

def run_d4_pipeline(snapshot: Optional[dict] = None) -> Optional[CalibratedD4Result]:
    """
    Ejecuta el pipeline D4 completo:
      gm_snapshot → ParishRecord[] → D4Result → D4PatternSet → CalibratedD4Result

    Cachea el resultado para la sesión (snapshot=None re-usa caché).
    Retorna None si no hay parroquias cargables — NUNCA lanza excepción.
    """
    global _CACHED_D4, _PIPELINE_RAN

    if snapshot is None and _PIPELINE_RAN:
        return _CACHED_D4   # puede ser None si el pipeline falló antes

    try:
        parishes = load_parish_records(snapshot)
        if not parishes:
            _PIPELINE_RAN = True
            return None

        d4_result   = analyze_territory(parishes)
        d4_patterns = detect_d4_patterns(d4_result)
        d4_calib    = calibrate_d4(d4_result, d4_patterns)

        if snapshot is None:
            _CACHED_D4   = d4_calib
            _PIPELINE_RAN = True

        return d4_calib

    except Exception:
        if snapshot is None:
            _PIPELINE_RAN = True
        return None


def invalidate_d4_cache() -> None:
    """Invalida caché para forzar recomputo (tests, refresh de snapshot)."""
    global _CACHED_D4, _PIPELINE_RAN
    _CACHED_D4    = None
    _PIPELINE_RAN = False


# ── CONTEXTO PARA CLAUDE HAIKU ─────────────────────────────────────────────────

_D4_KEYWORDS = {
    "territorio", "parroquia", "rural", "urbana", "equidad", "equity",
    "inversion", "inversión", "distribución", "distribucion", "brecha",
    "nbi", "necesidades", "agua", "cobertura", "rezago", "concentracion",
    "concentración", "montecristi", "isabel muentes", "colorado", "alfaro",
    "pila", "leonidas", "anibal", "d4", "sat-d4", "iet", "irs",
    "gini", "per capita", "percapita", "inequidad", "territorial",
}


def _query_is_d4_relevant(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in _D4_KEYWORDS)


def get_d4_context_for_query(
    query: str,
    cr: Optional[CalibratedD4Result] = None,
) -> str:
    """
    Retorna bloque de contexto D4 para inyectar en el system prompt de Claude Haiku.
    Vacío ('') si la query no es territorialmente relevante.
    Máx ~800 chars — preserva tokens del contexto activo.
    """
    if not _query_is_d4_relevant(query):
        return ""

    result = cr if cr is not None else run_d4_pipeline()
    if result is None:
        return ""

    return describe_d4_calibrated(result)


# ── RESUMEN PARA LOGS / DEBUG ──────────────────────────────────────────────────

def summarize_d4_pipeline(snapshot: Optional[dict] = None) -> str:
    """Resumen textual del pipeline D4 para logs y debug."""
    cr = run_d4_pipeline(snapshot)
    if cr is None:
        return "D4 Pipeline: sin datos parroquiales"

    sats = ", ".join(cr.sat_codes_calibrated) if cr.sat_codes_calibrated else "ninguno"
    lines = [
        f"D4 Pipeline — {cr.avep_d4_riesgo} (AVEP {cr.avep_d4_score:.1f} pts)",
        f"IRS={cr.irs:.1f}  CR1={cr.cr1:.0%}  CapRatio={cr.capital_ratio:.1f}x",
        f"Patron principal: {cr.principal_pattern}",
        f"Patrones calibrados: {len(cr.patterns_summary)}  SATs: {sats}",
        f"Sub-financiadas criticas: {cr.n_critical_underfunded} "
        f"({', '.join(cr.most_underfunded[:3])})",
        f"Ajustes aplicados: {len(cr.adjustments_applied)}",
    ]
    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import io

    # Wrap stdout with UTF-8 for Windows cp1252 consoles
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D4 Pipeline Completo — QUIRA OS")
    print("=" * 65)

    # 1. Carga de parroquias
    parishes = load_parish_records()
    print(f"\nParroquias cargadas: {len(parishes)}")
    for p in parishes:
        print(
            f"  {p.id} {p.nombre:22s} [{p.tipo:6s}]  "
            f"pob={p.poblacion:,d}  NBI={p.nbi_pct:.1f}%  "
            f"agua={p.cobertura_agua_pct:.1f}%  "
            f"inv=${p.inv_percapita:.0f}/hab"
        )

    # 2. Pipeline completo
    cr = run_d4_pipeline()
    if cr is None:
        print("\nERROR: pipeline retorno None — revisar gm_snapshot.json")
        sys.exit(1)

    print("\n" + "=" * 65)
    print("RESULTADO CALIBRADO")
    print("=" * 65)
    print(f"  AVEP riesgo : {cr.avep_d4_riesgo}")
    print(f"  AVEP score  : {cr.avep_d4_score:.1f}")
    print(f"  IRS         : {cr.irs:.1f}")
    print(f"  CR1         : {cr.cr1:.1%}")
    print(f"  Capital r.  : {cr.capital_ratio:.2f}x")
    print(f"  Sub-crits   : {cr.n_critical_underfunded} parroquias")
    print(f"  Mas rezago  : {', '.join(cr.most_underfunded)}")

    print(f"\nPatrones calibrados ({len(cr.patterns_summary)}):")
    for p in cr.patterns_summary:
        print(f"  [{p['risk']:7s}] {p['nombre']:30s}  "
              f"conf={p['confianza']:.0%}  {p['sat_hint']}")

    sats = ", ".join(cr.sat_codes_calibrated) if cr.sat_codes_calibrated else "ninguno"
    print(f"\nSATs activos: {sats}")
    print(f"\nNarrativa: {cr.narrative}")

    print("\nAjustes de calibracion aplicados:")
    for adj in cr.adjustments_applied:
        print(f"  - {adj[:100]}")

    # 3. Contexto Haiku — query territorial
    print("\n" + "=" * 65)
    print("CONTEXTO HAIKU — query territorial")
    print("=" * 65)
    ctx = get_d4_context_for_query(
        "Cual es la distribucion territorial de inversion en Montecristi?"
    )
    print(ctx if ctx else "(vacio)")

    # 4. Contexto Haiku — query no territorial
    print("\n--- Query NO territorial ---")
    ctx2 = get_d4_context_for_query("Cual es el presupuesto codificado 2025?")
    print(f"Contexto: {repr(ctx2)}")   # debe ser ''

    print("\n" + "=" * 65)
    print("D4 Pipeline OK")
    print("=" * 65)
