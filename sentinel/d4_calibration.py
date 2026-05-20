"""
sentinel/d4_calibration.py
RC-D4 Calibración Espacial — QUIRA OS

Capa de prudencia espacial: análoga a RC-7.3 (temporal) pero para equidad territorial.
Previene falsos positivos en patrones D4 causados por:
  1. Efecto capital-cantonal: sede administrativa justifica inversión diferenciada
  2. Alcance competencial: agua/educación/salud son servicios nacionales, no GAD
  3. Corte único: un snapshot puede no reflejar el patrón estructural
  4. Concentración poblacional: el cantón capital tiene 57% de la población
  5. Ruralidad estructural: costos per-capita legítimamente mayores en áreas dispersas

La calibración reduce confianza pero NUNCA oculta patrones evidentes.
Un IRS=93 con 5 parroquias rurales al -84% no puede suprimirse totalmente.
La prudencia espacial ajusta la certeza de la inferencia, no la existencia del dato.

API principal: calibrate_d4(result, ps) → CalibratedD4Result
Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from sentinel.d4_engine import D4Result
from sentinel.d4_patterns import D4Pattern, D4PatternSet

# ── CARGA CONFIGURACIÓN ────────────────────────────────────────────────────────
_CALIB_PATH = Path(__file__).parent.parent / "data" / "d4_calibration.json"

def _load_calib() -> dict:
    try:
        if _CALIB_PATH.exists():
            return json.loads(_CALIB_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

_CALIB = _load_calib()


# ── PARÁMETROS DE CALIBRACIÓN ESPACIAL ────────────────────────────────────────

# Factor de descuento por efecto capital-cantonal.
# El cantón capital legítimamente recibe más por: administración, cortes, salud,
# mercado, infraestructura de tránsito. Descuento aplicado a SAT-D4-C (captura capital).
_CAPITAL_EFFECT_DISCOUNT = _CALIB.get("capital_effect_discount", 0.18)

# Factor de descuento por alcance competencial.
# Agua: SENAGUA/Junta de Aguas/EMAPAM son competentes, no solo el GAD.
# Aplicado a SAT-D4-D (inequidad hídrica).
_COMPETENCE_SCOPE_DISCOUNT = _CALIB.get("competence_scope_discount", 0.12)

# Factor de descuento por corte único (snapshot single-period).
# Un solo corte temporal introduce incertidumbre sobre si el patrón es estructural.
_SINGLE_PERIOD_DISCOUNT = _CALIB.get("single_period_discount", 0.08)

# Factor de descuento por concentración poblacional natural.
# El cantón capital con 57% de población justifica cierta concentración de inversión.
# Aplicado cuando urban_population_share > 50%.
_POPULATION_CONCENTRATION_DISCOUNT = _CALIB.get("population_concentration_discount", 0.10)

# Umbral mínimo de confianza calibrada para emitir SAT D4.
# Más alto que RC-7.3 (0.40) porque los hallazgos D4 son políticamente sensibles.
_SAT_D4_MIN_CONF = _CALIB.get("sat_d4_min_confidence", 0.45)

# Confianza mínima garantizada — un IRS=93 y CR1=85% NUNCA baja de este umbral.
_MIN_FLOOR_CONF = _CALIB.get("min_floor_confidence", 0.35)

# Umbral de IRS para ignorar todos los descuentos (evidencia abrumadora).
_IRS_OVERWHELM_THRESHOLD = _CALIB.get("irs_overwhelm_threshold", 85.0)

# AVEP D4 — mapeo IRS → riesgo institucional
_AVEP_D4 = [
    (80.0, "Ruptura Territorial",      20.0),
    (60.0, "Inequidad Estructural",    40.0),
    (40.0, "Sesgo Distributivo",       60.0),
    (20.0, "Distribución Aceptable",   80.0),
    (0.0,  "Equidad Territorial",     100.0),
]


# ── TIPO RESULTADO CALIBRADO ───────────────────────────────────────────────────

@dataclass
class CalibratedD4Result:
    """Resultado D4 con prudencia espacial aplicada."""

    # ── Diagnóstico ───────────────────────────────────────────────────────────
    principal_pattern:     str          # patrón principal (calibrado)
    sat_codes_calibrated:  List[str]    # SATs que superan umbral mínimo
    raw_confidence:        float        # confianza antes de calibración
    calibrated_confidence: float        # confianza después de ajustes
    adjustments_applied:   List[str]    # descuentos aplicados (auditables)

    # ── Métricas clave para narrative ─────────────────────────────────────────
    irs:                   float
    capital_ratio:         float
    n_critical_underfunded: int
    most_underfunded:      List[str]
    cr1:                   float

    # ── AVEP D4 ───────────────────────────────────────────────────────────────
    avep_d4_score:         float
    avep_d4_riesgo:        str

    # ── Narrativa institucional ────────────────────────────────────────────────
    narrative:             str

    # ── Para serialización ────────────────────────────────────────────────────
    patterns_summary:      List[dict]


# ── MECANISMOS DE CALIBRACIÓN ──────────────────────────────────────────────────

def _apply_capital_effect(
    conf: float, p: D4Pattern, result: D4Result, applied: List[str]
) -> float:
    """Descuento por efecto capital-cantonal (SAT-D4-C)."""
    if p.sat_hint != "SAT-D4-C":
        return conf

    # Si el IRS es abrumadoramente alto, ignorar el descuento
    if result.irs >= _IRS_OVERWHELM_THRESHOLD:
        applied.append(
            f"capital_effect: descuento omitido (IRS={result.irs:.1f} supera umbral "
            f"de evidencia abrumadora {_IRS_OVERWHELM_THRESHOLD})"
        )
        return conf

    applied.append(
        f"capital_effect: -{ _CAPITAL_EFFECT_DISCOUNT:.0%} por efecto sede administrativa "
        f"(cabecera cantonal justifica hasta 30% de prima sobre rural)"
    )
    return max(_MIN_FLOOR_CONF, conf - _CAPITAL_EFFECT_DISCOUNT)


def _apply_competence_scope(
    conf: float, p: D4Pattern, applied: List[str]
) -> float:
    """Descuento por alcance competencial parcial del GAD (SAT-D4-D hídrica)."""
    if p.sat_hint != "SAT-D4-D":
        return conf

    applied.append(
        f"competence_scope: -{_COMPETENCE_SCOPE_DISCOUNT:.0%} "
        f"(cobertura agua parcialmente fuera de competencia GAD: SENAGUA/Juntas de Agua/EMAPAM)"
    )
    return max(_MIN_FLOOR_CONF, conf - _COMPETENCE_SCOPE_DISCOUNT)


def _apply_single_period_discount(
    conf: float, applied: List[str]
) -> float:
    """Descuento uniforme por análisis de un solo corte temporal."""
    applied.append(
        f"single_period: -{_SINGLE_PERIOD_DISCOUNT:.0%} (snapshot Q1-2026 único — "
        f"datos longitudinales parroquiales pendientes para confirmar patrón estructural)"
    )
    return max(_MIN_FLOOR_CONF, conf - _SINGLE_PERIOD_DISCOUNT)


def _apply_population_concentration(
    conf: float, p: D4Pattern, result: D4Result, applied: List[str]
) -> float:
    """
    Descuento cuando la concentración de inversión es parcialmente explicada
    por la concentración poblacional del capital cantonal.
    Solo aplica a SAT-D4-A y SAT-D4-C.
    """
    if p.sat_hint not in ("SAT-D4-A", "SAT-D4-C"):
        return conf

    urban_pop_share = sum(
        a.actual_inv_percapita * a.actual_inv_percapita  # no tenemos pop directo aquí
        for a in result.parish_analyses if a.tipo == "Urbana"
    )
    # Proxy: si CR1 > 80% pero la parroquia urbana tiene >55% de la población,
    # parte de la concentración es estructuralmente esperada
    urban_analyses = [a for a in result.parish_analyses if a.tipo == "Urbana"]
    if not urban_analyses:
        return conf

    # Heurística: si need_share de la capital es > 40%, la concentración tiene base demográfica
    cap_need_share = urban_analyses[0].need_share
    if cap_need_share > 0.40 and result.irs < _IRS_OVERWHELM_THRESHOLD:
        applied.append(
            f"population_concentration: -{_POPULATION_CONCENTRATION_DISCOUNT:.0%} "
            f"(capital con {cap_need_share:.0%} de necesidad cantonal — "
            f"concentración parcialmente justificada demográficamente)"
        )
        return max(_MIN_FLOOR_CONF, conf - _POPULATION_CONCENTRATION_DISCOUNT)

    return conf


def _compute_avep_d4(irs: float) -> tuple[float, str]:
    """Mapea IRS → AVEP D4 score + riesgo."""
    for threshold, riesgo, score in _AVEP_D4:
        if irs >= threshold:
            # Interpolación lineal dentro del rango
            next_idx = _AVEP_D4.index((threshold, riesgo, score))
            if next_idx < len(_AVEP_D4) - 1:
                next_th, _, next_score = _AVEP_D4[next_idx + 1]
                if threshold > next_th:
                    t = (irs - threshold) / (threshold - next_th) if threshold != next_th else 0
                    score = score + t * (next_score - score)
            return round(score, 1), riesgo
    return 100.0, "Equidad Territorial"


def _build_d4_narrative(result: D4Result, ps: D4PatternSet, conf: float) -> str:
    """
    Genera narrativa institucional para el diagnóstico D4 calibrado.
    Máx ~400 chars para el system prompt de Claude Haiku.
    """
    if not ps.patterns:
        return (
            f"Distribución territorial de inversión sin patrones críticos detectados. "
            f"IRS={result.irs:.1f}, CR1={result.cr1:.0%}."
        )

    principal = ps.patterns[0]
    underfunded_str = " · ".join(result.most_underfunded[:3])

    # Construir texto específico por patrón principal
    if principal.nombre == "CONCENTRACION_TERRITORIAL":
        base = (
            f"Inequidad territorial sistémica: IRS={result.irs:.1f} confirma que parroquias "
            f"con mayor NBI reciben sistemáticamente menos inversión. "
            f"Capital ratio {result.capital_ratio:.1f}x. "
            f"Más sub-financiadas: {underfunded_str}."
        )
    elif principal.nombre == "REZAGO_PERSISTENTE":
        base = (
            f"{result.n_critical_underfunded} parroquias rurales con brecha >50% bajo baseline equitativo. "
            f"Sub-financiadas: {underfunded_str}. "
            f"IRS={result.irs:.1f} confirma patrón regresivo."
        )
    elif principal.nombre == "CAPTURA_CAPITAL":
        base = (
            f"Cabecera cantonal capta {result.capital_ratio:.1f}x la inversión per cápita rural. "
            f"CR1={result.cr1:.0%} de la inversión cantonal en 1 parroquia. "
            f"Rezago: {underfunded_str}."
        )
    else:
        base = principal.descripcion[:250]

    return f"{base} [Confianza calibrada: {conf:.0%}]"


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def calibrate_d4(result: D4Result, ps: D4PatternSet) -> CalibratedD4Result:
    """
    Aplica la capa de prudencia espacial al análisis D4.

    Mecanismos:
      1. Capital effect discount (SAT-D4-C)
      2. Competence scope discount (SAT-D4-D)
      3. Single-period discount (todos)
      4. Population concentration discount (SAT-D4-A, SAT-D4-C)
      5. Overwhelm bypass (IRS ≥ 85 → ignora descuentos de credibilidad)

    Args:
        result: D4Result del motor espacial
        ps:     D4PatternSet de los detectores

    Returns:
        CalibratedD4Result con prudencia espacial aplicada
    """
    if not ps.patterns:
        avep_score, avep_riesgo = _compute_avep_d4(result.irs)
        return CalibratedD4Result(
            principal_pattern      = "SIN_PATRON",
            sat_codes_calibrated   = [],
            raw_confidence         = 0.0,
            calibrated_confidence  = 0.0,
            adjustments_applied    = [],
            irs                    = result.irs,
            capital_ratio          = result.capital_ratio,
            n_critical_underfunded = result.n_critical_underfunded,
            most_underfunded       = result.most_underfunded,
            cr1                    = result.cr1,
            avep_d4_score          = avep_score,
            avep_d4_riesgo         = avep_riesgo,
            narrative              = "Sin patrones D4 detectados.",
            patterns_summary       = [],
        )

    # Trabajar con el patrón principal para la confianza global
    principal = ps.patterns[0]
    raw_conf  = principal.confianza
    applied: List[str] = []
    sat_calibrated: List[str] = []

    # Bypass de evidencia abrumadora — si IRS ≥ 85, no se aplican descuentos de credibilidad
    overwhelm = result.irs >= _IRS_OVERWHELM_THRESHOLD

    # Procesar todos los patrones
    for p in ps.patterns:
        p_conf = p.confianza
        p_applied: List[str] = []

        if not overwhelm:
            p_conf = _apply_single_period_discount(p_conf, p_applied)
            p_conf = _apply_capital_effect(p_conf, p, result, p_applied)
            p_conf = _apply_competence_scope(p_conf, p, p_applied)
            p_conf = _apply_population_concentration(p_conf, p, result, p_applied)
        else:
            p_applied.append(
                f"overwhelm_bypass: IRS={result.irs:.1f} >= {_IRS_OVERWHELM_THRESHOLD} "
                f"-- descuentos omitidos por evidencia abrumadora"
            )

        if p_conf >= _SAT_D4_MIN_CONF:
            sat_calibrated.append(p.sat_hint)

        if p == principal:
            # Recoger los applied del patrón principal
            applied.extend(p_applied)

    # Confianza calibrada global (del patrón principal)
    p_conf_main = principal.confianza
    if not overwhelm:
        p_applied_main: List[str] = []
        p_conf_main = _apply_single_period_discount(p_conf_main, p_applied_main)
        p_conf_main = _apply_capital_effect(p_conf_main, principal, result, p_applied_main)
        p_conf_main = _apply_competence_scope(p_conf_main, principal, p_applied_main)
        p_conf_main = _apply_population_concentration(p_conf_main, principal, result, p_applied_main)
        # Ya se registró en applied arriba — no duplicar
    else:
        p_conf_main = min(0.95, principal.confianza)

    cal_conf = max(_MIN_FLOOR_CONF, p_conf_main)
    avep_score, avep_riesgo = _compute_avep_d4(result.irs)

    narrative = _build_d4_narrative(result, ps, cal_conf)

    patterns_summary = [
        {
            "nombre":    p.nombre,
            "sat_hint":  p.sat_hint,
            "confianza": round(p.confianza, 3),
            "risk":      p.risk_level,
        }
        for p in ps.patterns
    ]

    return CalibratedD4Result(
        principal_pattern      = principal.nombre,
        sat_codes_calibrated   = list(dict.fromkeys(sat_calibrated)),
        raw_confidence         = raw_conf,
        calibrated_confidence  = round(cal_conf, 3),
        adjustments_applied    = applied,
        irs                    = result.irs,
        capital_ratio          = result.capital_ratio,
        n_critical_underfunded = result.n_critical_underfunded,
        most_underfunded       = result.most_underfunded,
        cr1                    = result.cr1,
        avep_d4_score          = avep_score,
        avep_d4_riesgo         = avep_riesgo,
        narrative              = narrative,
        patterns_summary       = patterns_summary,
    )


def describe_d4_calibrated(cr: CalibratedD4Result) -> str:
    """
    Bloque compacto para el system prompt de Claude Haiku.
    Máx ~600 chars.
    """
    sats = ", ".join(cr.sat_codes_calibrated) if cr.sat_codes_calibrated else "ninguno"
    lines = [
        f"DIAGNÓSTICO D4 CALIBRADO ({cr.principal_pattern} | {cr.avep_d4_riesgo}):",
        f"  {cr.narrative[:300]}",
        f"  IRS={cr.irs:.1f} · Capital ratio={cr.capital_ratio:.1f}x · "
        f"CR1={cr.cr1:.0%} · Rezago crítico: {cr.n_critical_underfunded} parroquias",
        f"  Sub-financiadas: {', '.join(cr.most_underfunded[:3])}",
        f"  Confianza: {cr.raw_confidence:.0%} → {cr.calibrated_confidence:.0%}",
        f"  SATs D4 activos: {sats}",
    ]
    return "\n".join(lines)[:800]


def summarize_d4_calibrated(cr: CalibratedD4Result) -> dict:
    """Serializa CalibratedD4Result a dict para logs y session_state."""
    return {
        "principal_pattern":      cr.principal_pattern,
        "sat_codes_calibrated":   cr.sat_codes_calibrated,
        "raw_confidence":         cr.raw_confidence,
        "calibrated_confidence":  cr.calibrated_confidence,
        "adjustments_applied":    cr.adjustments_applied,
        "irs":                    cr.irs,
        "capital_ratio":          cr.capital_ratio,
        "n_critical_underfunded": cr.n_critical_underfunded,
        "most_underfunded":       cr.most_underfunded,
        "cr1":                    cr.cr1,
        "avep_d4_score":          cr.avep_d4_score,
        "avep_d4_riesgo":         cr.avep_d4_riesgo,
        "narrative":              cr.narrative,
        "patterns_summary":       cr.patterns_summary,
    }
