"""
sentinel/synthesis_prioritizer.py
RC-SYNTHESIS — Priorización de Señales y Tensión Dominante
Dylus Lab © 2026-05-20

FUNCIÓN:
  Recibe los resultados de todos los motores RC y produce:
  1. Lista priorizada de señales (máximo 3 — regla doctrinal)
  2. Tensión dominante semántica (no un score, sino un tipo institucional)
  3. Dimensiones suprimidas (engines que no llegaron al top-3)

REGLA DOCTRINAL CLAVE:
  La dimensión con mayor evidencia (confidence) domina.
  No se suman tensiones linealmente.
  Un motor con conf=0.07 no puede dominar sobre uno con conf=0.90,
  aunque su severidad nominal sea mayor.

  ranking_score = severity × confidence × obs_penalty × engine_weight

  obs_penalty = 0.4 si observational (señal debilitada epistémicamente)
  engine_weight = peso relativo del motor (D3×D4 > D4 > D1.3 > D3 > D1)

DOCTRINA:
  "El sistema informa — la autoridad pública decide."
  Máximo 3 señales. Siempre. No hay excepciones.

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ── PESOS DE MOTOR (calibrados para Montecristi GAD Holding) ─────────────────
# D3×D4 es el cruce más informativo; D4 territorial tiene alta densidad.
# D3 longitudinal puede tener baja conf por períodos cortos.
# D1/D1.3 legales son más deterministas pero requieren cédula confirmada.
_ENGINE_WEIGHTS: Dict[str, float] = {
    "D3xD4":       1.20,   # cruce es más que suma de partes
    "D4":          1.10,   # territorial — alta densidad datos
    "D1.3":        1.05,   # estratégico — vault-verified PDOT
    "D3":          1.00,   # temporal — puede tener pocos períodos
    "D1":          0.90,   # legal — requiere cédula; más conservador
    "HUMAN_REVIEW": 0.80,  # escalación — siempre observacional hasta confirmación humana
}

# ── SEVERIDAD CARDINAL POR MOTOR Y ESTADO ─────────────────────────────────────
_D3_SEVERITY: Dict[str, int] = {
    "INFRAEJECUCION_CRONICA":  5,
    "MANIPULACION_TEMPORAL":   5,
    "PARALISIS_ESTRUCTURAL":   4,
    "DETERIORO_PROGRESIVO":    4,
    "CIERRE_TARDIO":           3,
    "EXPANSION_TARDIA":        2,
    "SHOCK_EXTERNO":           2,
    "RECUPERACION_VERIFICADA": 1,
    "REFORMA_LEGITIMA":        1,
    "SIN_PATRON_CLARO":        0,
}

_D4_SEVERITY: Dict[str, int] = {
    "CONCENTRACION_TERRITORIAL": 5,
    "CAPTURA_CAPITAL":           5,
    "REZAGO_PERSISTENTE":        4,
    "INEQUIDAD_HIDRICA":         4,
    "SESGO_DISTRIBUTIVO":        3,
    "SIN_PATRON":                0,
}

_D3D4_SEVERITY: Dict[str, int] = {
    "CRISIS_DOBLE":             5,
    "EXCLUSION_PERIFERICA":     5,
    "VULNERABILIDAD_HIDRICA":   5,
    "EXPANSION_CONCENTRADA":    4,
    "REDISTRIBUCION_REGRESIVA": 4,
    "MAQUILLAJE_TERRITORIAL":   3,
    "EXPANSION_CON_EXCLUSION":  3,
    "CONVERGENCIA_CRITICA":     2,
    "SIN_CRUCE_CONFIRMADO":     0,
}

_D1_SEVERITY: Dict[str, int] = {
    "REQUIERE_REVIEW":         5,
    "RIESGO_DE_COMPETENCIA":   4,
    "RIESGO_DE_PROCEDIMIENTO": 3,
    "RIESGO_DE_EVIDENCIA":     2,
    "OBSERVADO":               1,
    "LEGAL":                   0,
}

_D13_SEVERITY: Dict[str, int] = {
    "CONTRADICCION_CRITICA":  5,
    "DESVIACION_ESTRATEGICA": 4,
    "DESVIACION_MENOR":       2,
    "EVIDENCIA_INSUFICIENTE": 0,
    "ALINEADO":               0,
}


# ── SIGNAL ────────────────────────────────────────────────────────────────────

@dataclass
class Signal:
    """
    Señal de un motor RC — unidad atómica de la síntesis.

    source        — "D3" | "D4" | "D3xD4" | "D1" | "D1.3" | "HUMAN_REVIEW"
    label         — estado/patrón del motor (p.e. "PARALISIS_ESTRUCTURAL")
    status        — mismo que label (para compatibilidad)
    confidence    — confianza calibrada del motor (0-1)
    severity      — severidad cardinal (0-5)
    observational — True si confidence < 0.25 (señal epistémicamente debilitada)
    sat_codes     — SAT codes del motor
    description   — texto descriptivo corto
    ranking_score — calculado: severity × confidence × obs_penalty × engine_weight
    """
    source:        str
    label:         str
    status:        str
    confidence:    float
    severity:      int
    observational: bool
    sat_codes:     List[str]
    description:   str
    ranking_score: float = field(init=False)

    def __post_init__(self):
        obs_penalty = 0.40 if self.observational else 1.00
        w = _ENGINE_WEIGHTS.get(self.source, 1.0)
        self.ranking_score = round(
            (self.severity / 5.0) * self.confidence * obs_penalty * w,
            4
        )


# ── TENSIONES DOMINANTES SEMÁNTICAS ──────────────────────────────────────────
# No son scores — son tipos institucionales emergentes de combinaciones de señales.

DOMINANT_TENSIONS = {
    "EXPANSION_REGRESIVA":         "Expansion presupuestaria sin correccion distributiva territorial",
    "BLOQUEO_INSTITUCIONAL":       "Paralisis ejecutiva con concentracion territorial persistente",
    "DESACOPLE_ESTRATEGICO":       "Divergencia entre compromiso PDOT declarado y comportamiento material",
    "CRISIS_TERRITORIAL_CRITICA":  "Subejecucion y concentracion territorial simultaneas — señal de alta complejidad",
    "VULNERABILIDAD_HIDRICA_SISTEMICA": "Inequidad hidrica rural sin correccion — competencia municipal exclusiva",
    "MAQUILLAJE_INSTITUCIONAL":    "Concentracion Q4 terminal sin redistribucion territorial real",
    "FRICCION_PROCEDIMENTAL":      "Riesgo en canal aprobatorio o competencia formal del acto presupuestario",
    "TENSION_COMPUESTA":           "Combinacion de tensiones institucionales sin patron dominante unico",
    "SIN_TENSION_DOMINANTE":       "Sin señales de magnitud suficiente para señalizacion prioritaria",
    "COHERENCIA_POSITIVA":         "Indicadores muestran alineamiento entre ejecucion y compromisos institucionales",
}


def determine_dominant_tension(top_signals: List[Signal]) -> str:
    """
    Determina la tensión dominante semántica a partir de las señales priorizadas.

    NO suma tensiones linealmente.
    La combinación específica de señales produce una hipótesis semántica emergente.
    """
    if not top_signals:
        return "SIN_TENSION_DOMINANTE"

    top = top_signals[0]   # señal mejor rankeada (evidencia × severidad)
    statuses = {s.status for s in top_signals}
    sources  = {s.source for s in top_signals}

    # Todos en verde → coherencia positiva
    all_benign = all(s.severity <= 1 for s in top_signals)
    if all_benign:
        return "COHERENCIA_POSITIVA"

    # ── D3×D4 como señal dominante ────────────────────────────────────────────
    if top.source == "D3xD4":
        if "CRISIS_DOBLE" in statuses:
            return "CRISIS_TERRITORIAL_CRITICA"
        if "EXCLUSION_PERIFERICA" in statuses:
            return "CRISIS_TERRITORIAL_CRITICA"
        if "VULNERABILIDAD_HIDRICA" in statuses:
            return "VULNERABILIDAD_HIDRICA_SISTEMICA"
        if "EXPANSION_CONCENTRADA" in statuses:
            # Verificar si hay también D1.3 CONTRADICCION → desacople PDOT
            if any(s.source == "D1.3" and s.severity >= 4 for s in top_signals):
                return "DESACOPLE_ESTRATEGICO"
            return "EXPANSION_REGRESIVA"
        if "REDISTRIBUCION_REGRESIVA" in statuses:
            return "EXPANSION_REGRESIVA"
        if "MAQUILLAJE_TERRITORIAL" in statuses:
            return "MAQUILLAJE_INSTITUCIONAL"

    # ── D1.3 como señal dominante (coherencia estratégica PDOT) ──────────────
    if top.source == "D1.3" and top.severity >= 4:
        # Con D4 concentración: desacople estratégico territorial
        if any(s.source in ("D4", "D3xD4") and s.severity >= 3 for s in top_signals):
            return "DESACOPLE_ESTRATEGICO"
        return "DESACOPLE_ESTRATEGICO"

    # ── D4 como señal dominante ───────────────────────────────────────────────
    if top.source == "D4":
        if top.status == "INEQUIDAD_HIDRICA":
            return "VULNERABILIDAD_HIDRICA_SISTEMICA"
        if top.status in ("CONCENTRACION_TERRITORIAL", "CAPTURA_CAPITAL"):
            # Con D3 paralisis/deterioro → bloqueo institucional
            d3_sig = next((s for s in top_signals if s.source == "D3"), None)
            if d3_sig and d3_sig.status in ("PARALISIS_ESTRUCTURAL", "INFRAEJECUCION_CRONICA", "DETERIORO_PROGRESIVO"):
                return "BLOQUEO_INSTITUCIONAL"
            # Con D3 expansión → expansión regresiva
            if d3_sig and d3_sig.status in ("EXPANSION_TARDIA", "RECUPERACION_VERIFICADA"):
                return "EXPANSION_REGRESIVA"

    # ── D3 como señal dominante (sin D4 fuerte) ───────────────────────────────
    if top.source == "D3":
        if top.status in ("PARALISIS_ESTRUCTURAL", "INFRAEJECUCION_CRONICA"):
            return "BLOQUEO_INSTITUCIONAL"

    # ── D1 riesgo procedimental ───────────────────────────────────────────────
    if top.source == "D1" and top.status in ("RIESGO_DE_PROCEDIMIENTO", "RIESGO_DE_COMPETENCIA"):
        return "FRICCION_PROCEDIMENTAL"

    # ── Default: tensión compuesta ────────────────────────────────────────────
    return "TENSION_COMPUESTA"


# ── MOTOR DE PRIORIZACIÓN ─────────────────────────────────────────────────────

def build_signals(data: Dict[str, Any]) -> List[Signal]:
    """
    Construye señales desde los dicts de sesión de todos los motores RC.

    Solo incluye señales con severity > 0 (ignorar ALINEADO/LEGAL/SIN_PATRON).
    """
    signals: List[Signal] = []

    # ── D3 (RC-7.3 Calibration Layer) ────────────────────────────────────────
    d3 = data.get("rc73_calibrated") or {}
    if d3:
        d3_cls  = d3.get("calibrated_class", "SIN_PATRON_CLARO")
        d3_conf = float(d3.get("calibrated_confidence", 0.10))
        d3_sev  = _D3_SEVERITY.get(d3_cls, 0)
        if d3_sev > 0:
            signals.append(Signal(
                source        = "D3",
                label         = d3_cls,
                status        = d3_cls,
                confidence    = d3_conf,
                severity      = d3_sev,
                observational = d3_conf < 0.25,
                sat_codes     = d3.get("sat_codes_calibrated", []),
                description   = f"Patron temporal: {d3_cls} (avep={d3.get('avep_score', 50):.0f})",
            ))

    # ── D4 (RC-D4 Territorial) ───────────────────────────────────────────────
    d4 = data.get("d4_calibrated") or {}
    if d4:
        d4_pat  = d4.get("principal_pattern", "SIN_PATRON")
        d4_conf = float(d4.get("calibrated_confidence", 0.50))
        d4_sev  = _D4_SEVERITY.get(d4_pat, 0)
        if d4_sev > 0:
            signals.append(Signal(
                source        = "D4",
                label         = d4_pat,
                status        = d4_pat,
                confidence    = d4_conf,
                severity      = d4_sev,
                observational = d4_conf < 0.25,
                sat_codes     = d4.get("sat_codes", []),
                description   = f"Patron territorial: {d4_pat} (IRS={d4.get('irs', 0):.1f})",
            ))

    # ── D3×D4 (Cross-inference) ───────────────────────────────────────────────
    cross = data.get("d3d4_cross") or {}
    if cross:
        c_pat   = cross.get("cross_pattern", "SIN_CRUCE_CONFIRMADO")
        c_conf  = float(cross.get("cross_confidence", 0.0))
        c_sev   = _D3D4_SEVERITY.get(c_pat, 0)
        c_obs   = bool(cross.get("observational_only", True))
        if c_sev > 0:
            signals.append(Signal(
                source        = "D3xD4",
                label         = c_pat,
                status        = c_pat,
                confidence    = c_conf,
                severity      = c_sev,
                observational = c_obs or c_conf < 0.25,
                sat_codes     = cross.get("sat_codes", []),
                description   = f"Cruce temporal×territorial: {c_pat} (EED={cross.get('eed_score', 0):+.1f})",
            ))

    # ── D1 (Competency + Procedural) ─────────────────────────────────────────
    d1 = data.get("d1_result") or {}
    if d1:
        d1_st   = d1.get("status_global", "OBSERVADO")
        d1_conf = float(d1.get("confidence", 0.10))
        d1_sev  = _D1_SEVERITY.get(d1_st, 0)
        if d1_sev >= 2:   # solo señalar si hay riesgo real (no solo OBSERVADO)
            signals.append(Signal(
                source        = "D1",
                label         = d1_st,
                status        = d1_st,
                confidence    = d1_conf,
                severity      = d1_sev,
                observational = d1_conf < 0.25 or bool(d1.get("observational", True)),
                sat_codes     = d1.get("sat_codes", []),
                description   = f"Coherencia juridica: {d1_st} ({d1.get('top_action', '')})",
            ))

    # ── D1.3 (Strategic Coherence PDOT) ──────────────────────────────────────
    d13 = data.get("d13_result") or {}
    if d13:
        d13_st   = d13.get("status", "EVIDENCIA_INSUFICIENTE")
        d13_conf = float(d13.get("confidence", 0.10))
        d13_sev  = _D13_SEVERITY.get(d13_st, 0)
        if d13_sev >= 2:   # solo si hay desviación real
            signals.append(Signal(
                source        = "D1.3",
                label         = d13_st,
                status        = d13_st,
                confidence    = d13_conf,
                severity      = d13_sev,
                observational = d13_conf < 0.25 or bool(d13.get("observational", True)),
                sat_codes     = [d13["sat_code"]] if d13.get("sat_code") else [],
                description   = (
                    f"Coherencia PDOT: {d13_st} "
                    f"(IRS={d13.get('irs_actual', 0):.1f} vs meta<={d13.get('irs_meta', 45):.0f}, "
                    f"delta={d13.get('irs_delta', 0):+.1f})"
                ),
            ))

    # ── HUMAN_REVIEW flag ─────────────────────────────────────────────────────
    hr = data.get("inference_review_flag") or {}
    if hr and not hr.get("acknowledged", True):
        hr_conf = float(hr.get("cross_conf", 0.30))
        signals.append(Signal(
            source        = "HUMAN_REVIEW",
            label         = "REVISION_INSTITUCIONAL_REQUERIDA",
            status        = "REVISION_INSTITUCIONAL_REQUERIDA",
            confidence    = hr_conf,
            severity      = 4,   # siempre alto cuando activo y no ack
            observational = bool(hr.get("observational", False)),
            sat_codes     = [],
            description   = f"Escalacion institucional activa: {hr.get('cross_pattern', '')}",
        ))

    return signals


def prioritize_signals(
    data:        Dict[str, Any],
    max_signals: int = 3,
) -> Tuple[List[Signal], List[str]]:
    """
    Prioriza señales de todos los motores RC y retorna top-N + dimensiones suprimidas.

    Reglas:
      1. ranking_score = severity × confidence × obs_penalty × engine_weight
      2. La dimensión con mayor evidencia domina (conf es primaria)
      3. Máximo max_signals (doctrina: 3)
      4. Señales con severity=0 siempre suprimidas

    Returns: (top_signals, suppressed_dimensions)
    """
    all_signals = build_signals(data)

    if not all_signals:
        return [], []

    # Ordenar por ranking_score desc, desempate por confidence desc
    ranked = sorted(all_signals, key=lambda s: (s.ranking_score, s.confidence), reverse=True)

    top      = ranked[:max_signals]
    rest     = ranked[max_signals:]
    suppressed = [f"{s.source}:{s.label}" for s in rest if s.severity > 0]

    return top, suppressed
