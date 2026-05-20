"""
sentinel/calibration_layer.py
RC-7.3 — Capa de Calibración Epistemológica
QUIRA OS · Dylus Lab © 2026-05-20

Calibra los outputs de RC-7.2 para prevenir:
  · Falsos positivos  — PARALISIS cuando es Q1 normal de inversión
  · Sobreclasificación — CRITICO con evidencia insuficiente
  · Exceso de SATs    — SATs sin base empírica sólida
  · Inferencias agresivas con n_periodos < 3

5 mecanismos (parámetros en data/rc72_calibration.json):
  1. confidence_decay       — decae certeza por datos escasos o mixtos
  2. entity_baselines       — compara entidad consigo misma (no contra umbral absoluto)
  3. seasonal_normalization — Q1 G71-78 esperado ≈ 2.5% (≠ anomalía)
  4. reform_whitelist       — reformas ≤ 10% codificado no activan SAT-X-B
  5. evidence_weighting     — pondera fuerza por cantidad de períodos confirmatorios

Doctrina: la calibración NUNCA silencia señales — las contextualiza.
Contraloría ve la señal original Y el ajuste aplicado.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from sentinel.institutional_classifier import InstitutionalClass
from sentinel.administrative_patterns  import PatternSet
from sentinel.longitudinal_engine      import LongitudinalResult


# ── CARGA DE PARÁMETROS ────────────────────────────────────────────────────────

_CFG_PATH = Path(__file__).parent.parent / "data" / "rc72_calibration.json"

def _load_cfg() -> dict:
    if _CFG_PATH.exists():
        with open(_CFG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}

_CFG: dict = _load_cfg()


# ── TIPOS ─────────────────────────────────────────────────────────────────────

@dataclass
class CalibratedResult:
    """
    Resultado calibrado del pipeline RC-7.2 + RC-7.3.

    original_class:        clase del sub-motor 3 (sin calibrar)
    calibrated_class:      clase post-calibración (puede diferir si seasonal/whitelist actúa)
    raw_confidence:        confianza original del sub-motor 3
    calibrated_confidence: confianza post-calibración (siempre ≤ raw_confidence)
    evidence_weight:       peso probatorio (0.0–1.0) basado en n_periodos y fuentes
    seasonal_factor:       factor estacional aplicado (1.0 = sin ajuste, < 1.0 = downward)
    entity_baseline_gap:   diferencia entre Ti actual y Ti esperado para la entidad/periodo
    reform_whitelisted:    True si la reforma fue validada dentro del umbral del Alcalde
    sat_codes_calibrated:  SATs post-calibración (puede ser subset de sat_codes original)
    calibration_applied:   lista de reglas que se activaron (auditable)
    narrative:             bloque narrativo en español para informe ejecutivo
    avep_riesgo:           nivel AVEP calibrado
    avep_score:            score AVEP calibrado
    """
    original_class:        str
    calibrated_class:      str
    raw_confidence:        float
    calibrated_confidence: float
    evidence_weight:       float
    seasonal_factor:       float       = 1.0
    entity_baseline_gap:   float       = 0.0
    reform_whitelisted:    bool        = False
    sat_codes_calibrated:  list[str]   = field(default_factory=list)
    calibration_applied:   list[str]   = field(default_factory=list)
    narrative:             str         = ""
    avep_riesgo:           str         = ""
    avep_score:            float       = 0.0


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _is_q1_periodo(periodo: str) -> bool:
    """True si el periodo corresponde al primer trimestre o primeros meses."""
    p = periodo.upper()
    markers = _CFG.get("seasonal_normalization", {}).get("period_markers_q1", [
        "Q1", "M01", "M02", "M03", "ENE", "FEB", "MAR",
    ])
    return any(m in p for m in markers)


def _is_q4_periodo(periodo: str) -> bool:
    p = periodo.upper()
    markers = _CFG.get("seasonal_normalization", {}).get("period_markers_q4", [
        "Q4", "M10", "M11", "M12", "OCT", "NOV", "DIC",
    ])
    return any(m in p for m in markers)


def _is_grupo_inversion(grupo: str) -> bool:
    """True si el grupo de gasto es de inversión (G71-G78, G84)."""
    cfg_grupos = (
        _CFG.get("seasonal_normalization", {})
            .get("q1_groups_inversion", {})
            .get("grupos", ["71","72","73","74","75","77","78","84"])
    )
    g = grupo.strip().replace("-","")
    return any(g.startswith(gx) or gx in g for gx in cfg_grupos)


def _has_mixed_frequency(result: LongitudinalResult) -> bool:
    """
    Detecta si la serie mezcla periodos anuales y sub-anuales.
    Ejemplo: ['2023', '2024', '2025', '2026Q1'] → True (apples-to-oranges).
    """
    if result.n_periodos < 2:
        return False
    has_annual = any(
        len(r) == 4 and r.isdigit()
        for r in [p for p in _get_periodos(result)]
    )
    has_sub = any(
        not (len(r) == 4 and r.isdigit())
        for r in [p for p in _get_periodos(result)]
    )
    return has_annual and has_sub


def _get_periodos(result: LongitudinalResult) -> list[str]:
    """Extrae los periodos desde n_periodos — no tenemos acceso directo a records aquí."""
    # LongitudinalResult no almacena periodos originales; usamos los slopes
    if result.slopes:
        periodos = [result.slopes[0].from_periodo]
        periodos += [s.to_periodo for s in result.slopes]
        return periodos
    return []


# ── MECANISMO 1: CONFIDENCE DECAY ────────────────────────────────────────────

def _apply_confidence_decay(
    confidence:   float,
    result:       LongitudinalResult,
    applied:      list[str],
) -> float:
    cfg = _CFG.get("confidence_decay", {})
    n   = result.n_periodos

    # Decay por número de periodos
    if n == 1:
        factor = cfg.get("decay_1_period", 0.40)
        applied.append(f"DECAY_N1_{factor}")
    elif n == 2:
        factor = cfg.get("decay_2_periods", 0.65)
        applied.append(f"DECAY_N2_{factor}")
    elif n == 3:
        factor = cfg.get("decay_3_periods", 0.82)
        applied.append(f"DECAY_N3_{factor}")
    else:
        factor = cfg.get("decay_4plus_periods", 1.00)

    confidence *= factor

    # Decay por ausencia de grupo_gasto
    if not result.grupo_gasto:
        gd = cfg.get("decay_no_grupo_gasto", 0.88)
        confidence *= gd
        applied.append(f"DECAY_NO_GRUPO_{gd}")

    # Decay por frecuencia mixta (anual + sub-anual en misma serie)
    if _has_mixed_frequency(result):
        mf = cfg.get("decay_mixed_frequency", 0.75)
        confidence *= mf
        applied.append(f"DECAY_MIXED_FREQ_{mf}")

    return round(min(confidence, 1.0), 4)


# ── MECANISMO 2: EVIDENCE WEIGHTING ──────────────────────────────────────────

def _compute_evidence_weight(
    result:    LongitudinalResult,
    applied:   list[str],
) -> float:
    cfg = _CFG.get("evidence_weighting", {})
    n   = result.n_periodos

    if n == 1:
        w = cfg.get("weight_1_period", 0.30)
    elif n == 2:
        w = cfg.get("weight_2_periods", 0.55)
    elif n == 3:
        w = cfg.get("weight_3_periods", 0.75)
    else:
        w = cfg.get("weight_4plus_periods", 0.90)

    applied.append(f"EVIDENCE_WEIGHT_{w}_n{n}")
    return round(w, 3)


# ── MECANISMO 3: SEASONAL NORMALIZATION ───────────────────────────────────────

def _apply_seasonal_normalization(
    current_class: str,
    current_conf:  float,
    result:        LongitudinalResult,
    applied:       list[str],
) -> tuple[str, float, float]:
    """
    Recibe clase y confianza YA decaídas por confidence_decay.
    Retorna (calibrated_class, seasonal_factor, calibrated_conf).
    Si Q1 + grupo inversión + Ti esperado → downgrade clase y confianza.
    """
    cfg_sn = _CFG.get("seasonal_normalization", {})

    # Solo aplica si el último periodo es Q1
    last_period = result.slopes[-1].to_periodo if result.slopes else ""

    if not _is_q1_periodo(last_period):
        return current_class, 1.0, current_conf

    grupo = result.grupo_gasto
    if not _is_grupo_inversion(grupo):
        return current_class, 1.0, current_conf

    cfg_inv      = cfg_sn.get("q1_groups_inversion", {})
    ti_expected  = cfg_inv.get("ti_expected_pct",  2.5)
    ti_tolerance = cfg_inv.get("ti_tolerance_pct", 5.0)
    decay        = cfg_inv.get("decay_if_q1",      0.55)

    ti_last = result.ti_series[-1] if result.ti_series else 100.0

    # Si Ti está dentro de 3x el rango esperado de Q1 → estacional
    if ti_last <= ti_expected * 3 + ti_tolerance:
        new_conf = round(current_conf * decay, 4)

        # Reclasificar PARALISIS_ESTRUCTURAL → EXPANSION_TARDIA si es solo Q1
        if current_class == "PARALISIS_ESTRUCTURAL":
            applied.append(
                f"Q1_SEASONAL_NORM → PARALISIS reclasificado a EXPANSION_TARDIA "
                f"(Ti={ti_last:.1f}% dentro del rango Q1 G71-78 normal ≤{ti_expected*3+ti_tolerance:.1f}%)"
            )
            return "EXPANSION_TARDIA", decay, new_conf

        applied.append(f"Q1_SEASONAL_NORM → decay_conf={decay:.2f} (Ti={ti_last:.1f}%)")
        return current_class, decay, new_conf

    # Ti Q1 inesperadamente baja más allá del rango → señal real
    applied.append(f"Q1_SEASONAL_NORM_SKIPPED → Ti={ti_last:.1f}% fuera rango normal — señal real mantenida")
    return current_class, 1.0, current_conf


# ── MECANISMO 4: ENTITY BASELINES ────────────────────────────────────────────

def _compute_baseline_gap(
    result:   LongitudinalResult,
    applied:  list[str],
) -> float:
    """
    Gap = Ti_actual - Ti_esperado para la entidad en este tipo de periodo.
    Negativo = por debajo del baseline propio (peor de lo esperado para la entidad).
    Positivo = por encima del baseline (mejor de lo esperado).
    """
    cfg_bl = _CFG.get("entity_baselines", {})
    entity_cfg = cfg_bl.get(result.entidad, cfg_bl.get("GAD", {}))

    last_period = result.slopes[-1].to_periodo if result.slopes else ""
    grupo       = result.grupo_gasto or ""

    # Determinar Ti esperado según periodo y grupo
    if _is_q1_periodo(last_period) and _is_grupo_inversion(grupo):
        ti_expected = entity_cfg.get("ti_q1_g7178", 2.5)
        applied.append(f"BASELINE_{result.entidad}_Q1_G71-78_expected={ti_expected}%")
    elif _is_q1_periodo(last_period):
        ti_expected = entity_cfg.get("ti_q1_g5157", 22.0)
        applied.append(f"BASELINE_{result.entidad}_Q1_corrientes_expected={ti_expected}%")
    else:
        # Anualizamos: si Ti actual es de periodo parcial, no comparar con anual
        ti_expected = entity_cfg.get("ti_annual_expected", 75.0)
        applied.append(f"BASELINE_{result.entidad}_annual_expected={ti_expected}%")

    ti_last = result.ti_series[-1] if result.ti_series else 0.0
    gap     = round(ti_last - ti_expected, 3)
    return gap


# ── MECANISMO 5: REFORM WHITELIST ────────────────────────────────────────────

def _check_reform_whitelist(
    current_class: str,
    current_conf:  float,
    ic:            InstitutionalClass,
    ps:            PatternSet,
    result:        LongitudinalResult,
    applied:       list[str],
) -> tuple[str, float, bool]:
    """
    Recibe clase y confianza YA ajustadas por pasos anteriores.
    Si REFORM_SHOCK presente pero reforma ≤ 10% (umbral Alcalde COPLAFIP Art.97) → whitelist.

    Retorna (class, confidence, whitelisted).
    """
    cfg_wl        = _CFG.get("reform_whitelist", {})
    threshold_pct = cfg_wl.get("alcalde_threshold_pct", 10.0)

    reform_pat = any(p.nombre == "REFORM_SHOCK" for p in ps.patterns)
    if not reform_pat:
        return current_class, current_conf, False

    # Calcular % de reforma sobre promedio codificado
    avg_cod = abs(result.codificado_drift - result.reforma_net)
    if avg_cod <= 0:
        avg_cod = abs(result.reforma_net) + 1.0

    reforma_pct = abs(result.reforma_net) / avg_cod * 100

    if reforma_pct <= threshold_pct:
        new_clase = "REFORMA_LEGITIMA" if current_class in ("REFORM_SHOCK", "PARALISIS_ESTRUCTURAL") else current_class
        new_conf  = round(current_conf * 0.75, 4)
        applied.append(
            f"REFORM_WHITELIST_APPLIED → reforma={reforma_pct:.1f}% ≤ {threshold_pct}% "
            f"(umbral Alcalde COPLAFIP Art.97). SAT-X-B suprimido."
        )
        return new_clase, new_conf, True

    applied.append(f"REFORM_WHITELIST_SKIPPED → reforma={reforma_pct:.1f}% > {threshold_pct}% → requiere Concejo")
    return current_class, current_conf, False


# ── SAT SUPPRESSION ───────────────────────────────────────────────────────────

def _filter_sats(
    sat_codes:       list[str],
    confidence:      float,
    evidence_weight: float,
    applied:         list[str],
) -> list[str]:
    """
    Suprime SATs cuando confianza o peso de evidencia es insuficiente.
    Umbral: confianza_calibrada ≥ 0.40 Y evidence_weight ≥ 0.50.
    """
    cfg_st = _CFG.get("sat_suppression_thresholds", {})
    min_conf = cfg_st.get("min_confidence_for_sat", 0.40)
    min_ew   = cfg_st.get("min_evidence_weight",    0.50)

    if confidence >= min_conf and evidence_weight >= min_ew:
        return sat_codes

    suppressed = sat_codes
    if confidence < min_conf:
        applied.append(f"SAT_SUPPRESSED → conf={confidence:.2f} < {min_conf} (umbral mínimo)")
    if evidence_weight < min_ew:
        applied.append(f"SAT_SUPPRESSED → evidence_weight={evidence_weight:.2f} < {min_ew}")
    return []


# ── NARRATIVE GENERATOR ───────────────────────────────────────────────────────

_AVEP_LABELS: dict[str, tuple[str, float]] = {
    "PARALISIS_ESTRUCTURAL":    ("Ruptura Sistémica",       18.0),
    "INFRAEJECUCION_CRONICA":   ("Ruptura Sistémica",       22.0),
    "MANIPULACION_TEMPORAL":    ("Ocurrencia Crítica",      35.0),
    "DETERIORO_PROGRESIVO":     ("Ocurrencia Crítica",      38.0),
    "EXPANSION_TARDIA":         ("Transición Crítica",      48.0),
    "SHOCK_EXTERNO":            ("Transición Crítica",      50.0),
    "CIERRE_TARDIO":            ("Transición Crítica",      55.0),
    "REFORMA_LEGITIMA":         ("Gestión por Mandato",     72.0),
    "RECUPERACION_VERIFICADA":  ("Gestión por Mandato",     75.0),
    "SIN_PATRON_CLARO":         ("Transición Crítica",      52.0),
}

_NARRATIVE_TEMPLATES: dict[str, str] = {
    "PARALISIS_ESTRUCTURAL": (
        "Parálisis estructural de ejecución detectada. "
        "Ti del último período: {ti_last:.1f}% — significativamente por debajo del baseline "
        "histórico de {entity} ({ti_expected:.1f}% esperado). "
        "Se requiere diagnóstico técnico urgente de causales en eSIGEF/PAC."
    ),
    "EXPANSION_TARDIA": (
        "Expansión presupuestaria ({drift_sign}${drift:,.0f} codificado) con ritmo de ejecución "
        "inferior al baseline de {entity}. "
        "Ti actual: {ti_last:.1f}% vs {ti_expected:.1f}% esperado. "
        "Prioridad: identificar proyectos con expediente completo para acelerar ejecución."
    ),
    "MANIPULACION_TEMPORAL": (
        "Concentración de gasto detectada fuera del patrón normal de {entity}. "
        "Ti actual: {ti_last:.1f}%. "
        "Verificar trazabilidad documental: SHA-256, procesos SERCOP y cadena de aprobaciones."
    ),
    "REFORMA_LEGITIMA": (
        "Reforma presupuestaria dentro del umbral del Alcalde (COPLAFIP Art.97). "
        "No se activa SAT-X-B. "
        "Ti actual: {ti_last:.1f}%. Confirmar consistencia con metas PDOT vigentes."
    ),
    "DETERIORO_PROGRESIVO": (
        "Deterioro progresivo de ejecución en {entity}: Ti pasó de {ti_first:.1f}% a "
        "{ti_last:.1f}% en {n} períodos. "
        "Solicitar informe de seguimiento POA a la Dirección de Planificación."
    ),
    "CIERRE_TARDIO": (
        "Patrón de cierre tardío de ejercicio. Ti actual: {ti_last:.1f}% (baseline anual "
        "{entity}: {ti_expected:.1f}%). "
        "Distribución hacia Q4 detectada — planificar PAC para Q1 del próximo ejercicio."
    ),
    "SIN_PATRON_CLARO": (
        "Datos insuficientes para clasificación definitiva ({n} período(s), "
        "Ti_media={ti_mean:.1f}%). "
        "Ampliar serie temporal a mínimo 4 períodos comparables."
    ),
}


def _build_narrative(
    calibrated_class:  str,
    result:            LongitudinalResult,
    baseline_gap:      float,
    calibration_rules: list[str],
    seasonal_applied:  bool,
) -> str:
    cfg_bl     = _CFG.get("entity_baselines", {})
    entity_cfg = cfg_bl.get(result.entidad, cfg_bl.get("GAD", {}))

    last_period = result.slopes[-1].to_periodo if result.slopes else ""
    if _is_q1_periodo(last_period) and _is_grupo_inversion(result.grupo_gasto):
        ti_expected = entity_cfg.get("ti_q1_g7178", 2.5)
    elif _is_q1_periodo(last_period):
        ti_expected = entity_cfg.get("ti_q1_g5157", 22.0)
    else:
        ti_expected = entity_cfg.get("ti_annual_expected", 75.0)

    ti_last  = result.ti_series[-1] if result.ti_series else 0.0
    ti_first = result.ti_series[0]  if result.ti_series else 0.0

    template = _NARRATIVE_TEMPLATES.get(calibrated_class, _NARRATIVE_TEMPLATES["SIN_PATRON_CLARO"])
    try:
        base_narrative = template.format(
            ti_last      = ti_last,
            ti_first     = ti_first,
            ti_mean      = result.ti_mean,
            ti_expected  = ti_expected,
            entity       = result.entidad,
            n            = result.n_periodos,
            drift        = abs(result.codificado_drift),
            drift_sign   = "+" if result.codificado_drift >= 0 else "-",
        )
    except (KeyError, ValueError):
        base_narrative = f"Ti={ti_last:.1f}% | clase={calibrated_class} | n={result.n_periodos}."

    # Añadir nota de calibración si se aplicó seasonal
    if seasonal_applied:
        base_narrative += (
            f" [Calibración RC-7.3: factor estacional Q1 aplicado — "
            f"Ti={ti_last:.1f}% dentro del rango esperado para Q1 grupos de inversión.]"
        )

    return base_narrative.strip()


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def calibrate(
    ic:     InstitutionalClass,
    ps:     PatternSet,
    result: LongitudinalResult,
) -> CalibratedResult:
    """
    Aplica los 5 mecanismos de calibración sobre InstitutionalClass.

    Orden de aplicación:
    1. Evidence weighting  (peso probatorio base)
    2. Confidence decay    (ajuste por datos escasos)
    3. Entity baseline     (gap vs propio historial)
    4. Seasonal norm       (normalización Q1 inversión)
    5. Reform whitelist    (umbral COPLAFIP Art.97)
    6. SAT suppression     (filtrado de SATs débiles)

    Returns:
        CalibratedResult con clase calibrada, confianza ajustada,
        SATs filtrados y narrativa ejecutiva.
    """
    applied: list[str] = []

    # ── 1. Evidence weight (base — no modifica conf) ──────────────────────────
    evidence_weight = _compute_evidence_weight(result, applied)

    # ── 2. Confidence decay (modifica conf sobre ic.confianza) ────────────────
    conf      = _apply_confidence_decay(ic.confianza, result, applied)
    cal_class = ic.clase   # clase en curso, se va actualizando en cada paso

    # ── 3. Entity baseline gap (informativo — no modifica conf) ───────────────
    baseline_gap = _compute_baseline_gap(result, applied)

    # ── 4. Seasonal normalization (puede reclasificar + decaer conf) ──────────
    cal_class, seasonal_factor, conf = _apply_seasonal_normalization(
        cal_class, conf, result, applied
    )
    seasonal_applied = seasonal_factor < 1.0

    # ── 5. Reform whitelist (puede reclasificar + decaer conf + suprimir SAT-X-B) ─
    cal_class, conf, reform_wl = _check_reform_whitelist(
        cal_class, conf, ic, ps, result, applied
    )
    if reform_wl:
        sat_raw = [s for s in ic.sat_codes if s != "SAT-X-B"]
    else:
        sat_raw = ic.sat_codes[:]

    # ── 6. SAT suppression (filtra SATs débiles) ──────────────────────────────
    sat_calibrated = _filter_sats(sat_raw, conf, evidence_weight, applied)

    # ── AVEP calibrado ────────────────────────────────────────────────────────
    avep_riesgo, avep_score = _AVEP_LABELS.get(cal_class, ("Transición Crítica", 52.0))

    # ── Narrative ─────────────────────────────────────────────────────────────
    narrative = _build_narrative(cal_class, result, baseline_gap, applied, seasonal_applied)

    return CalibratedResult(
        original_class        = ic.clase,
        calibrated_class      = cal_class,
        raw_confidence        = ic.confianza,
        calibrated_confidence = round(min(conf, 1.0), 4),
        evidence_weight       = evidence_weight,
        seasonal_factor       = seasonal_factor,
        entity_baseline_gap   = baseline_gap,
        reform_whitelisted    = reform_wl,
        sat_codes_calibrated  = sat_calibrated,
        calibration_applied   = applied,
        narrative             = narrative,
        avep_riesgo           = avep_riesgo,
        avep_score            = avep_score,
    )


def describe_calibrated(cr: CalibratedResult) -> str:
    """
    Genera bloque compacto para system prompt de Claude Haiku.
    Incluye clase calibrada, contexto estacional y SATs activos.
    Max ~500 chars.
    """
    sats_str = (", ".join(cr.sat_codes_calibrated)) if cr.sat_codes_calibrated else "ninguno"
    lines = [
        f"DIAGNÓSTICO RC-7.3 CALIBRADO ({cr.calibrated_class} | {cr.avep_riesgo}):",
        f"  {cr.narrative[:250]}",
        f"  Confianza: {cr.raw_confidence:.0%} → {cr.calibrated_confidence:.0%} "
        f"(peso evidencial: {cr.evidence_weight:.0%})",
        f"  SATs activos: {sats_str}",
    ]
    if cr.original_class != cr.calibrated_class:
        lines.append(
            f"  ⚠ Clase reclasificada: {cr.original_class} → {cr.calibrated_class} "
            f"(calibración aplicada)"
        )
    return "\n".join(lines)[:800]


def summarize_calibrated(cr: CalibratedResult) -> dict:
    """Serializa CalibratedResult a dict compacto para logs y session_state."""
    return {
        "original_class":        cr.original_class,
        "calibrated_class":      cr.calibrated_class,
        "raw_confidence":        cr.raw_confidence,
        "calibrated_confidence": cr.calibrated_confidence,
        "evidence_weight":       cr.evidence_weight,
        "seasonal_factor":       cr.seasonal_factor,
        "baseline_gap":          cr.entity_baseline_gap,
        "reform_whitelisted":    cr.reform_whitelisted,
        "sat_codes_calibrated":  cr.sat_codes_calibrated,
        "calibration_applied":   cr.calibration_applied,
        "avep_riesgo":           cr.avep_riesgo,
        "avep_score":            cr.avep_score,
        "narrative":             cr.narrative,
    }


# ── PIPELINE COMPLETO RC-7.2 + RC-7.3 ─────────────────────────────────────────

def run_full_pipeline(
    records: list,
) -> tuple:
    """
    Pipeline completo: BudgetRecord → CalibratedResult

    Returns: (LongitudinalResult, PatternSet, InstitutionalClass, NormativeBinding, CalibratedResult)
    """
    from sentinel.normative_binding     import run_rc72_pipeline
    result, ps, ic, binding = run_rc72_pipeline(records)
    cr = calibrate(ic, ps, result)
    return result, ps, ic, binding, cr
