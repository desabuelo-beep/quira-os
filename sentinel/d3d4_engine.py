"""
sentinel/d3d4_engine.py
RC-D3D4 — Motor de Inferencia Cruzada Temporal-Territorial
QUIRA OS · Dylus Lab © 2026-05-20

Cruza el diagnostico temporal (D3: ejecucion presupuestaria) con el diagnostico
territorial (D4: equidad interparroquial) para detectar patrones institucionales
compuestos.

Doctrina epistemica:
  - El cruce produce hipotesis institucionales, NO veredictos.
  - observational_only=True cuando la evidencia D3 es insuficiente
    (cross_confidence < 0.25 o d3_conf < 0.15): el sistema senala
    direccion, no confirma patron.
  - cross_confidence = sqrt(d3_conf * d4_conf) con penalizacion x0.5 si D3<0.30
  - EED Score (Execution-Equity Divergence) = d3_avep - d4_avep:
      > +15 → expansion_concentrada (ejecucion bien, equidad mal)
      < -15 → rezago_distributivo  (equidad peor que ejecucion)
      ~ 0   → alineado

Patrones cruzados D3xD4 (8 patrones canonicos):
  EXPANSION_CONCENTRADA     — ejecucion crece, inequidad territorial persiste
  EXPANSION_CON_EXCLUSION   — ejecucion crece, parroquias rezagadas excluidas
  CRISIS_DOBLE              — ejecucion baja + inequidad alta = doble vulnerabilidad
  EXCLUSION_PERIFERICA      — contraccion + rezago = parroquias pobres al margen
  VULNERABILIDAD_HIDRICA    — contraccion + inequidad hidrica = riesgo servicios basicos
  MAQUILLAJE_TERRITORIAL    — concentracion Q4 + concentracion territorial = cosmetica
  REDISTRIBUCION_REGRESIVA  — reforma presupuestaria mantiene/profundiza inequidad
  CONVERGENCIA_CRITICA      — D4 critico sin patron D3 claro
  SIN_CRUCE_CONFIRMADO      — evidencia insuficiente (solo observacional)

API principal: analyze_cross(d3_dict, d4_dict) -> D3D4CrossResult
Entradas:
  d3_dict: output de summarize_calibrated()  (sentinel.calibration_layer)
  d4_dict: output de summarize_d4_calibrated() (sentinel.d4_calibration)

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


# ── TIPOS ──────────────────────────────────────────────────────────────────────

@dataclass
class D3State:
    """Estado ejecutivo D3 extraido del dict de summarize_calibrated()."""
    avep_class:   str        # calibrated_class del RC-7.3
    avep_score:   float      # avep_score del RC-7.3
    avep_riesgo:  str        # avep_riesgo del RC-7.3
    confidence:   float      # calibrated_confidence
    evidence_wt:  float      # evidence_weight (proxy de n_periodos)
    sat_codes:    List[str]  # sat_codes_calibrated
    has_data:     bool       # True si el dict fue cargado correctamente


@dataclass
class D4State:
    """Estado ejecutivo D4 extraido del dict de summarize_d4_calibrated()."""
    principal_pattern: str        # principal_pattern del RC-D4
    irs:               float      # IRS territorial (0-100, mayor = mas inequidad)
    avep_d4_score:     float      # avep_d4_score (mayor = mas equidad)
    avep_d4_riesgo:    str        # avep_d4_riesgo
    confidence:        float      # calibrated_confidence del D4
    sat_codes:         List[str]  # sat_codes_calibrated del D4
    n_critical:        int        # n_critical_underfunded
    patterns:          List[str]  # nombres de patterns_summary (en orden)


@dataclass
class D3D4CrossResult:
    """
    Resultado del cruce D3xD4.

    Garantias:
      - Nunca acusatorio — hipotesis institucionales, no veredictos
      - observational_only=True cuando cross_confidence < 0.25
      - EED score siempre calculado (incluso si observacional)
      - cross_confidence siempre derivado matematicamente de ambas fuentes
    """
    cross_pattern:      str        # patron cruzado canonico
    severity:           str        # "CRITICO"|"ALTO"|"MEDIO"|"OBSERVACIONAL"
    sat_codes:          List[str]  # SAT codes D3D4 activos
    d3_confidence:      float
    d4_confidence:      float
    cross_confidence:   float      # sqrt(d3 * d4) con penalizacion
    observational_only: bool       # True si D3 insuficiente
    d3_state:           D3State
    d4_state:           D4State
    narrative:          str        # bloque para Claude Haiku (<=500 chars)
    evidence:           List[str]  # evidencias auditables para Contraloria
    eed_score:          float      # D3_avep - D4_avep
    eed_class:          str        # "expansion_concentrada"|"rezago_distributivo"|"alineado"


# ── MAPEOS ────────────────────────────────────────────────────────────────────

# Grupo funcional D3 (calibrated_class -> grupo para la matriz de cruce)
_D3_GROUPS: dict[str, str] = {
    "EXPANSION_TARDIA":        "expansion",
    "RECUPERACION_VERIFICADA": "expansion",
    "REFORMA_LEGITIMA":        "reforma",
    "MANIPULACION_TEMPORAL":   "q4_terminal",
    "CIERRE_TARDIO":           "q4_terminal",
    "DETERIORO_PROGRESIVO":    "contraccion",
    "PARALISIS_ESTRUCTURAL":   "contraccion",
    "INFRAEJECUCION_CRONICA":  "contraccion",
    "SHOCK_EXTERNO":           "reforma",
    "SIN_PATRON_CLARO":        "neutral",
}

# Grupo funcional D4 (principal_pattern -> grupo para la matriz de cruce)
_D4_GROUPS: dict[str, str] = {
    "CONCENTRACION_TERRITORIAL": "concentracion",
    "CAPTURA_CAPITAL":           "captura",
    "REZAGO_PERSISTENTE":        "rezago",
    "INEQUIDAD_HIDRICA":         "hidrica",
    "SESGO_DISTRIBUTIVO":        "sesgo",
    "SIN_PATRON":                "sin_patron",
}

# Matriz de cruce canonica: (d3_group, d4_group) -> (patron, severidad, SAT-code)
_CROSS_MATRIX: dict[tuple, tuple] = {
    # EXPANSION + cualquier inequidad territorial
    ("expansion",   "concentracion"): ("EXPANSION_CONCENTRADA",    "CRITICO",      "SAT-D3D4-A"),
    ("expansion",   "captura"):       ("EXPANSION_CONCENTRADA",    "CRITICO",      "SAT-D3D4-A"),
    ("expansion",   "sesgo"):         ("EXPANSION_CONCENTRADA",    "ALTO",         "SAT-D3D4-A"),
    ("expansion",   "rezago"):        ("EXPANSION_CON_EXCLUSION",  "ALTO",         "SAT-D3D4-B"),
    ("expansion",   "hidrica"):       ("EXPANSION_CON_EXCLUSION",  "ALTO",         "SAT-D3D4-B"),
    # CONTRACCION + inequidad territorial
    ("contraccion", "concentracion"): ("CRISIS_DOBLE",             "CRITICO",      "SAT-D3D4-A"),
    ("contraccion", "captura"):       ("CRISIS_DOBLE",             "CRITICO",      "SAT-D3D4-A"),
    ("contraccion", "rezago"):        ("EXCLUSION_PERIFERICA",     "CRITICO",      "SAT-D3D4-A"),
    ("contraccion", "hidrica"):       ("VULNERABILIDAD_HIDRICA",   "CRITICO",      "SAT-D3D4-A"),
    ("contraccion", "sesgo"):         ("EXCLUSION_PERIFERICA",     "ALTO",         "SAT-D3D4-B"),
    # Q4_TERMINAL + inequidad territorial (concentracion al final del ejercicio)
    ("q4_terminal", "concentracion"): ("MAQUILLAJE_TERRITORIAL",   "ALTO",         "SAT-D3D4-C"),
    ("q4_terminal", "captura"):       ("MAQUILLAJE_TERRITORIAL",   "ALTO",         "SAT-D3D4-C"),
    ("q4_terminal", "rezago"):        ("MAQUILLAJE_TERRITORIAL",   "MEDIO",        "SAT-D3D4-C"),
    ("q4_terminal", "sesgo"):         ("MAQUILLAJE_TERRITORIAL",   "MEDIO",        "SAT-D3D4-C"),
    # REFORMA (incluye shock externo) + inequidad territorial
    ("reforma",     "concentracion"): ("REDISTRIBUCION_REGRESIVA", "ALTO",         "SAT-D3D4-D"),
    ("reforma",     "captura"):       ("REDISTRIBUCION_REGRESIVA", "ALTO",         "SAT-D3D4-D"),
    ("reforma",     "rezago"):        ("REDISTRIBUCION_REGRESIVA", "MEDIO",        "SAT-D3D4-D"),
    ("reforma",     "sesgo"):         ("REDISTRIBUCION_REGRESIVA", "MEDIO",        "SAT-D3D4-D"),
    # NEUTRAL (SIN_PATRON_CLARO) + inequidad territorial
    ("neutral",     "concentracion"): ("CONVERGENCIA_CRITICA",     "MEDIO",        "SAT-D3D4-E"),
    ("neutral",     "captura"):       ("CONVERGENCIA_CRITICA",     "MEDIO",        "SAT-D3D4-E"),
    ("neutral",     "rezago"):        ("CONVERGENCIA_CRITICA",     "MEDIO",        "SAT-D3D4-E"),
    ("neutral",     "hidrica"):       ("CONVERGENCIA_CRITICA",     "MEDIO",        "SAT-D3D4-E"),
    ("neutral",     "sesgo"):         ("CONVERGENCIA_CRITICA",     "MEDIO",        "SAT-D3D4-E"),
}

# Narrativas por patron cruzado (variables: {d3_class}, {irs}, {n_crit}, {eed}, {d3_conf}, {d4_pattern})
_CROSS_NARRATIVES: dict[str, str] = {
    "EXPANSION_CONCENTRADA": (
        "La expansion presupuestaria observada ({d3_class}) coexiste con inequidad territorial "
        "estructural (IRS={irs:.1f}). El crecimiento de recursos ejecutados favorece "
        "desproporcionadamente areas con menor necesidad relativa. "
        "EED={eed:+.1f} pts — la brecha temporal-territorial es positiva y significativa."
    ),
    "EXPANSION_CON_EXCLUSION": (
        "Expansion temporal ({d3_class}) con {n_crit} parroquias en rezago critico "
        "sistematicamente excluidas del crecimiento. IRS={irs:.1f}. "
        "El incremento de ejecucion no alcanza los territorios de mayor necesidad. "
        "EED={eed:+.1f} pts."
    ),
    "CRISIS_DOBLE": (
        "Doble vulnerabilidad institucional: contraccion de ejecucion ({d3_class}) coincide "
        "con alta inequidad territorial (IRS={irs:.1f}). Las parroquias mas necesitadas "
        "enfrentan simultaneamente menor ejecucion y mayor concentracion de recursos en la capital. "
        "EED={eed:+.1f} pts."
    ),
    "EXCLUSION_PERIFERICA": (
        "Exclusion periferica critica: contraccion de ejecucion ({d3_class}) combinada con "
        "rezago territorial persistente (IRS={irs:.1f}). {n_crit} parroquias con sub-financiamiento "
        "severo y tendencia de ejecucion negativa. EED={eed:+.1f} pts."
    ),
    "VULNERABILIDAD_HIDRICA": (
        "Riesgo hidrico territorial agravado por contraccion de ejecucion ({d3_class}). "
        "IRS={irs:.1f} con inequidad en cobertura de servicios basicos. La reduccion de recursos "
        "ejecutados impacta desproporcionadamente parroquias rurales. EED={eed:+.1f} pts."
    ),
    "MAQUILLAJE_TERRITORIAL": (
        "Patron de concentracion temporal ({d3_class}) coincidente con concentracion "
        "territorial estructural (IRS={irs:.1f}). La acumulacion de gasto en periodo terminal "
        "puede encubrir una distribucion territorial regresiva. EED={eed:+.1f} pts."
    ),
    "REDISTRIBUCION_REGRESIVA": (
        "Reforma presupuestaria ({d3_class}) no corrige — y posiblemente profundiza — "
        "la inequidad territorial observada (IRS={irs:.1f}). "
        "La restructuracion presupuestaria amerita revision de su impacto distributivo territorial. "
        "EED={eed:+.1f} pts."
    ),
    "CONVERGENCIA_CRITICA": (
        "Inequidad territorial estructural (IRS={irs:.1f}) sin patron temporal D3 claro. "
        "{n_crit} parroquias en rezago critico. La distribucion interparroquial de inversion "
        "muestra patrones sistematicos independientes del ciclo de ejecucion. "
        "EED={eed:+.1f} pts."
    ),
    "SIN_CRUCE_CONFIRMADO": (
        "Evidencia D3 insuficiente para cruce confirmado (conf D3={d3_conf:.0%}). "
        "Dirección observable: D4={d4_pattern} territorial (IRS={irs:.1f}). "
        "Se requieren >= 3 periodos comparables para inferencia D3xD4 confirmada. "
        "EED indicativo={eed:+.1f} pts."
    ),
}


# ── MECANISMOS INTERNOS ────────────────────────────────────────────────────────

def _extract_d3_state(d3_dict: dict) -> D3State:
    """Extrae D3State desde el dict de summarize_calibrated()."""
    return D3State(
        avep_class  = d3_dict.get("calibrated_class", "SIN_PATRON_CLARO"),
        avep_score  = float(d3_dict.get("avep_score",            52.0)),
        avep_riesgo = d3_dict.get("avep_riesgo", "Transicion Critica"),
        confidence  = float(d3_dict.get("calibrated_confidence", 0.0)),
        evidence_wt = float(d3_dict.get("evidence_weight",       0.0)),
        sat_codes   = list(d3_dict.get("sat_codes_calibrated",   [])),
        has_data    = bool(d3_dict),
    )


def _extract_d4_state(d4_dict: dict) -> D4State:
    """Extrae D4State desde el dict de summarize_d4_calibrated()."""
    patterns_raw = d4_dict.get("patterns_summary", [])
    pattern_names = [p.get("nombre", "") for p in patterns_raw if p.get("nombre")]
    return D4State(
        principal_pattern = d4_dict.get("principal_pattern",      "SIN_PATRON"),
        irs               = float(d4_dict.get("irs",               0.0)),
        avep_d4_score     = float(d4_dict.get("avep_d4_score",    100.0)),
        avep_d4_riesgo    = d4_dict.get("avep_d4_riesgo", "Equidad Territorial"),
        confidence        = float(d4_dict.get("calibrated_confidence", 0.0)),
        sat_codes         = list(d4_dict.get("sat_codes_calibrated",   [])),
        n_critical        = int(d4_dict.get("n_critical_underfunded",   0)),
        patterns          = pattern_names,
    )


def _compute_cross_confidence(d3_conf: float, d4_conf: float) -> float:
    """
    cross_confidence = sqrt(d3_conf * d4_conf)
    Penalizacion x0.5 si d3_conf < 0.30 (evidencia temporal muy debil).
    """
    base = math.sqrt(max(0.0, d3_conf) * max(0.0, d4_conf))
    if d3_conf < 0.30:
        base *= 0.5
    return round(base, 4)


def _compute_eed(d3_avep: float, d4_avep: float) -> tuple[float, str]:
    """
    EED (Execution-Equity Divergence) = D3_avep - D4_avep.
      > +15 → expansion_concentrada (ejecucion bien, equidad territorial mal)
      < -15 → rezago_distributivo (inequidad peor que lo que sugiere ejecucion)
      entre  → alineado (ambos diagnosticos coherentes)
    """
    eed = round(d3_avep - d4_avep, 1)
    if eed > 15:
        eed_class = "expansion_concentrada"
    elif eed < -15:
        eed_class = "rezago_distributivo"
    else:
        eed_class = "alineado"
    return eed, eed_class


def _resolve_cross_pattern(
    d3_group:    str,
    d4:          D4State,
) -> tuple[str, str, list[str]]:
    """
    Resuelve el patron cruzado mirando primero el patron principal D4,
    luego iterando sobre patrones secundarios si no hay match directo.

    Returns: (cross_pattern, severity, sat_codes)
    """
    d4_group = _D4_GROUPS.get(d4.principal_pattern, "sin_patron")

    if d4_group == "sin_patron":
        return "SIN_CRUCE_CONFIRMADO", "OBSERVACIONAL", []

    entry = _CROSS_MATRIX.get((d3_group, d4_group))
    if entry:
        cp, sev, sat = entry
        return cp, sev, [sat]

    # Fallback: intentar con patrones secundarios D4
    for alt_p in d4.patterns[1:3]:
        alt_g = _D4_GROUPS.get(alt_p, "sin_patron")
        if alt_g == "sin_patron":
            continue
        entry = _CROSS_MATRIX.get((d3_group, alt_g))
        if entry:
            cp, sev, sat = entry
            return cp, sev, [sat]

    return "SIN_CRUCE_CONFIRMADO", "OBSERVACIONAL", []


def _build_cross_narrative(
    cross_pattern: str,
    d3:            D3State,
    d4:            D4State,
    eed:           float,
    observational: bool,
) -> str:
    """Genera narrativa institucional para el patron cruzado (<=500 chars)."""
    template = _CROSS_NARRATIVES.get(cross_pattern, "")
    try:
        text = template.format(
            d3_class   = d3.avep_class,
            irs        = d4.irs,
            n_crit     = d4.n_critical,
            eed        = eed,
            d3_conf    = d3.confidence,
            d4_pattern = d4.principal_pattern,
        )
    except (KeyError, ValueError):
        text = (
            f"Cruce D3xD4: {cross_pattern}. "
            f"D3={d3.avep_class} (conf={d3.confidence:.0%}), "
            f"D4={d4.principal_pattern} IRS={d4.irs:.1f}. "
            f"EED={eed:+.1f} pts."
        )

    prefix = "[OBSERVACIONAL — evidencia D3 insuficiente] " if observational else ""
    return (prefix + text)[:500]


def _build_evidence(
    d3:            D3State,
    d4:            D4State,
    cross_conf:    float,
    eed:           float,
    observational: bool,
) -> List[str]:
    """Construye lista de evidencias auditables para Contraloria."""
    penalty_note = " x0.5 (D3<0.30)" if d3.confidence < 0.30 else ""
    ev = [
        f"D3: {d3.avep_class} | conf={d3.confidence:.0%} | ew={d3.evidence_wt:.0%} | "
        f"AVEP-D3={d3.avep_score:.1f} ({d3.avep_riesgo})",
        f"D4: {d4.principal_pattern} | IRS={d4.irs:.1f} | conf={d4.confidence:.0%} | "
        f"AVEP-D4={d4.avep_d4_score:.1f} ({d4.avep_d4_riesgo})",
        f"EED = AVEP-D3({d3.avep_score:.1f}) - AVEP-D4({d4.avep_d4_score:.1f}) = {eed:+.1f}",
        f"cross_conf = sqrt({d3.confidence:.3f} * {d4.confidence:.3f})"
        f"{penalty_note} = {cross_conf:.3f}",
    ]
    if observational:
        ev.append(
            f"observational_only: cross_conf={cross_conf:.3f} < 0.25 — "
            f"requiere >=3 periodos D3 para inferencia confirmada"
        )
    if d4.n_critical > 0:
        ev.append(f"D4: {d4.n_critical} parroquias en rezago critico")
    if d3.sat_codes:
        ev.append(f"D3 SATs: {', '.join(d3.sat_codes)}")
    if d4.sat_codes:
        ev.append(f"D4 SATs: {', '.join(d4.sat_codes)}")
    return ev


def _build_cross_prompt_block(result: "D3D4CrossResult") -> str:
    """Bloque compacto para inyeccion en system prompt de Claude Haiku (<= 600 chars)."""
    if result.cross_pattern == "SIN_CRUCE_CONFIRMADO" and result.d4_state.irs < 20:
        return ""

    obs_prefix = "[OBSERVACIONAL] " if result.observational_only else ""
    sats_str   = " · ".join(result.sat_codes) if result.sat_codes else "--"
    lines = [
        f"DIAGNOSTICO D3xD4 — {obs_prefix}{result.cross_pattern} [{result.severity}]",
        f"  EED={result.eed_score:+.1f} pts ({result.eed_class})",
        f"  D3: {result.d3_state.avep_class} (conf={result.d3_confidence:.0%}) | "
        f"D4: IRS={result.d4_state.irs:.1f} (conf={result.d4_confidence:.0%})",
        f"  SATs: {sats_str}",
        f"  {result.narrative[:220]}",
        "INSTRUCCION: El cruce D3xD4 produce hipotesis institucionales — no veredictos. "
        "Usar lenguaje observacional ('la evidencia sugiere...', 'se observa direccionalmente...').",
    ]
    return "\n".join(lines)[:650]


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def analyze_cross(
    d3_dict: Optional[dict],
    d4_dict: Optional[dict],
) -> D3D4CrossResult:
    """
    API principal: combina d3_dict y d4_dict para producir D3D4CrossResult.

    Args:
        d3_dict: output de summarize_calibrated()    — sentinel.calibration_layer
        d4_dict: output de summarize_d4_calibrated() — sentinel.d4_calibration

    Returns:
        D3D4CrossResult con patron cruzado, EED score y narrativa institucional.
        Si alguno de los dicts es None/vacio, produce resultado observacional minimo.

    Doctrina: hipotesis institucionales, no veredictos.
    """
    # ── Extraer estados desde dicts de sesion ────────────────────────────────
    d3 = _extract_d3_state(d3_dict or {})
    d4 = _extract_d4_state(d4_dict or {})

    # ── Calcular metricas epistemicas ─────────────────────────────────────────
    eed, eed_class   = _compute_eed(d3.avep_score, d4.avep_d4_score)
    cross_conf       = _compute_cross_confidence(d3.confidence, d4.confidence)
    observational    = (
        cross_conf < 0.25
        or not d3.has_data
        or d3_dict is None
        or d3.confidence < 0.15
    )

    # ── Resolver patron cruzado desde la matriz ────────────────────────────────
    if d4_dict is None or d4.principal_pattern == "SIN_PATRON":
        cross_pattern = "SIN_CRUCE_CONFIRMADO"
        severity      = "OBSERVACIONAL"
        sat_codes     = []
    else:
        d3_group = _D3_GROUPS.get(d3.avep_class, "neutral")
        cross_pattern, severity, sat_codes = _resolve_cross_pattern(d3_group, d4)

    # ── Degradar severidad si evidencia insuficiente ───────────────────────────
    if observational and severity in ("CRITICO", "ALTO", "MEDIO"):
        severity = "OBSERVACIONAL"

    # ── Construir narrativa y evidencias ──────────────────────────────────────
    narrative = _build_cross_narrative(cross_pattern, d3, d4, eed, observational)
    evidence  = _build_evidence(d3, d4, cross_conf, eed, observational)

    return D3D4CrossResult(
        cross_pattern      = cross_pattern,
        severity           = severity,
        sat_codes          = sat_codes,
        d3_confidence      = d3.confidence,
        d4_confidence      = d4.confidence,
        cross_confidence   = cross_conf,
        observational_only = observational,
        d3_state           = d3,
        d4_state           = d4,
        narrative          = narrative,
        evidence           = evidence,
        eed_score          = eed,
        eed_class          = eed_class,
    )


def get_cross_context_for_query(
    query:   str,
    d3_dict: Optional[dict] = None,
    d4_dict: Optional[dict] = None,
) -> str:
    """
    Retorna bloque D3xD4 para inyectar en system prompt de Claude Haiku.
    Vacio si d4_dict es None o la query no es institucionalmente relevante.
    """
    if d4_dict is None:
        return ""

    _CROSS_KEYWORDS = {
        "presupuesto", "ejecucion", "inversion", "parroquia", "rural",
        "inequidad", "equidad", "territorio", "concentracion", "d3", "d4",
        "avep", "irs", "distribucion", "gasto", "holding", "brecha",
        "temporal", "espacial", "cruce", "historico",
    }
    q_low = query.lower()
    # Activar si la query menciona alguna keyword
    if not any(kw in q_low for kw in _CROSS_KEYWORDS):
        return ""

    result = analyze_cross(d3_dict, d4_dict)
    return _build_cross_prompt_block(result)


def summarize_cross(result: D3D4CrossResult) -> dict:
    """Serializa D3D4CrossResult a dict para session_state y debug."""
    return {
        "cross_pattern":      result.cross_pattern,
        "severity":           result.severity,
        "sat_codes":          result.sat_codes,
        "d3_confidence":      result.d3_confidence,
        "d4_confidence":      result.d4_confidence,
        "cross_confidence":   result.cross_confidence,
        "observational_only": result.observational_only,
        "eed_score":          result.eed_score,
        "eed_class":          result.eed_class,
        "narrative":          result.narrative,
        "evidence":           result.evidence,
        "d3_state": {
            "avep_class":   result.d3_state.avep_class,
            "avep_score":   result.d3_state.avep_score,
            "avep_riesgo":  result.d3_state.avep_riesgo,
            "confidence":   result.d3_state.confidence,
            "evidence_wt":  result.d3_state.evidence_wt,
            "sat_codes":    result.d3_state.sat_codes,
        },
        "d4_state": {
            "principal_pattern": result.d4_state.principal_pattern,
            "irs":               result.d4_state.irs,
            "avep_d4_score":     result.d4_state.avep_d4_score,
            "avep_d4_riesgo":    result.d4_state.avep_d4_riesgo,
            "confidence":        result.d4_state.confidence,
            "n_critical":        result.d4_state.n_critical,
            "patterns":          result.d4_state.patterns,
        },
    }


# ── CLI TEST ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import io

    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D3D4 Cross-Inference Engine — QUIRA OS")
    print("=" * 65)

    # Simular estado Montecristi real:
    # D3: SIN_PATRON_CLARO (solo 2-3 periodos) conf=0.07, ew=0.14, avep=52.0
    # D4: CONCENTRACION_TERRITORIAL IRS=93.1, conf=0.90, avep_d4=33.1
    _d3_mock = {
        "calibrated_class":      "SIN_PATRON_CLARO",
        "avep_score":            52.0,
        "avep_riesgo":           "Transicion Critica",
        "calibrated_confidence": 0.07,
        "evidence_weight":       0.14,
        "sat_codes_calibrated":  [],
    }
    _d4_mock = {
        "principal_pattern":      "CONCENTRACION_TERRITORIAL",
        "irs":                    93.1,
        "avep_d4_score":          33.1,
        "avep_d4_riesgo":         "Inequidad Estructural",
        "calibrated_confidence":  0.90,
        "sat_codes_calibrated":   ["SAT-D4-A", "SAT-D4-B", "SAT-D4-C"],
        "n_critical_underfunded": 4,
        "patterns_summary": [
            {"nombre": "CONCENTRACION_TERRITORIAL", "confianza": 0.90, "risk": "CRITICO"},
            {"nombre": "REZAGO_PERSISTENTE",         "confianza": 0.88, "risk": "CRITICO"},
            {"nombre": "CAPTURA_CAPITAL",            "confianza": 0.82, "risk": "CRITICO"},
            {"nombre": "INEQUIDAD_HIDRICA",          "confianza": 0.65, "risk": "ALTO"},
        ],
    }

    result = analyze_cross(_d3_mock, _d4_mock)

    print(f"\nPatron cruzado : {result.cross_pattern}")
    print(f"Severidad       : {result.severity}")
    print(f"Observacional   : {result.observational_only}")
    print(f"EED score       : {result.eed_score:+.1f} pts ({result.eed_class})")
    print(f"cross_conf      : {result.cross_confidence:.4f}")
    print(f"D3 conf         : {result.d3_confidence:.0%}")
    print(f"D4 conf         : {result.d4_confidence:.0%}")
    print(f"SATs activos    : {', '.join(result.sat_codes) or '--'}")

    print("\n--- Narrativa ---")
    print(result.narrative)

    print("\n--- Evidencias ---")
    for ev in result.evidence:
        print(f"  · {ev}")

    print("\n--- Prompt block ---")
    print(_build_cross_prompt_block(result))
