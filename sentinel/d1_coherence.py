"""
sentinel/d1_coherence.py
RC-D1.3 — Normative Coherence (Coherencia Estratégica Institucional)
Dylus Lab © 2026-05-20

FUNCIÓN:
  Motor de coherencia estratégica institucional.
  Responde a la pregunta que D3/D4/D1.1 no responden:

  "¿El municipio está ejecutando aquello que dijo que era prioritario
   para el territorio?"

  No es un motor jurídico clásico.
  No verifica procedimiento (D1.1) ni distribución temporal (D3).
  Verifica si el COMPORTAMIENTO MATERIAL del aparato público
  es coherente con los COMPROMISOS ESTRATÉGICOS DECLARADOS.

ARQUITECTURA (4 capas):
  1. Strategic Commitment Map    — compromisos vault-verified del PDOT
  2. Execution Alignment Engine  — gaps: alineamiento / ejecución / territorial / persistencia
  3. Contradiction Classifier    — 5 estados (incluye EVIDENCIA_INSUFICIENTE)
  4. Narrative Synthesizer       — hipótesis institucional auditada (~400 chars)

ESTADOS D1.3 (5 niveles):
  ALINEADO               — ejecución coherente con compromiso declarado
  DESVIACION_MENOR       — gap marginal; no bloquea; requiere seguimiento
  DESVIACION_ESTRATEGICA — contradicción sostenida entre planificación y ejecución
  CONTRADICCION_CRITICA  — divergencia estructural PDOT ↔ comportamiento material
  EVIDENCIA_INSUFICIENTE — densidad insuficiente para valoración prudente

FUENTES VAULT-VERIFIED:
  PDOT Montecristi 2023-2027 — IRS ≤ 45.0 (meta D4 equidad, data/d4_normative.json)
  CRE Art. 238               — equidad interterritorial (verificado)
  CRE Art. 264(4)            — competencia agua potable (verificado)
  COOTAD Art. 238            — presupuesto participativo (verificado D1.1)
  COOTAD Art. 272            — distribución parroquial cantonal (verificado D1.1)

DOCTRINA INMUTABLE:
  D1.3 detecta contradicciones institucionales difusas.
  No acusa. No sanciona. Produce hipótesis de coherencia estratégica.
  "El sistema informa — la autoridad pública decide."
  Nunca: "incumplió el compromiso X." Siempre: "genera indicadores de desacople."

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ── ESTADO D1.3 (5 niveles, incluye EVIDENCIA_INSUFICIENTE) ──────────────────

class D13Status(str, Enum):
    """
    Estados de coherencia estratégica institucional.

    ALINEADO               — ejecución coherente con PDOT
    DESVIACION_MENOR       — gap marginal (<15% del objetivo)
    DESVIACION_ESTRATEGICA — contradicción sostenida (gap ≥ 15%, persistente)
    CONTRADICCION_CRITICA  — divergencia estructural (gap ≥ 40%, cross-confirmada)
    EVIDENCIA_INSUFICIENTE — densidad insuficiente para valoración (prudencia RC-CORE)
    """
    ALINEADO               = "ALINEADO"
    DESVIACION_MENOR       = "DESVIACION_MENOR"
    DESVIACION_ESTRATEGICA = "DESVIACION_ESTRATEGICA"
    CONTRADICCION_CRITICA  = "CONTRADICCION_CRITICA"
    EVIDENCIA_INSUFICIENTE = "EVIDENCIA_INSUFICIENTE"


# Severidad ordinal para comparaciones
_STATUS_SEVERITY: Dict[D13Status, int] = {
    D13Status.ALINEADO:               0,
    D13Status.EVIDENCIA_INSUFICIENTE: 1,
    D13Status.DESVIACION_MENOR:       2,
    D13Status.DESVIACION_ESTRATEGICA: 3,
    D13Status.CONTRADICCION_CRITICA:  4,
}


# ── CAPA 1: STRATEGIC COMMITMENT MAP (solo vault-verified) ───────────────────

@dataclass
class StrategicCommitment:
    """
    Compromiso estratégico del PDOT Montecristi 2023-2027.

    Solo se incluyen compromisos con fuente vault-verified.
    target_value es el valor objetivo al año deadline.
    priority_weight refleja urgencia territorial relativa (0-1).
    """
    objective_id:    str
    sector:          str       # "equidad_territorial" | "agua" | "pp" | "distribucion"
    territory:       str       # "CANTONAL" | "RURAL" | parroquia específica
    target_metric:   str       # qué se mide
    target_value:    float     # valor objetivo
    target_direction: str      # "lte" (≤) | "gte" (≥)
    deadline:        str       # "2027"
    priority_weight: float     # 0.0 – 1.0
    norm_source:     str       # fuente vault-verified
    verified:        bool      # siempre True en este mapa
    note:            str = ""


# Mapa canónico de compromisos PDOT Montecristi 2023-2027
# SOLO compromisos vault-verified — no inventar targets sin fuente
_COMMITMENT_MAP: List[StrategicCommitment] = [

    StrategicCommitment(
        objective_id    = "PDOT-EQUIDAD-01",
        sector          = "equidad_territorial",
        territory       = "CANTONAL",
        target_metric   = "IRS",
        target_value    = 45.0,
        target_direction= "lte",         # IRS debe ser ≤ 45
        deadline        = "2027",
        priority_weight = 0.90,
        norm_source     = "PDOT Montecristi 2023-2027 — Meta D4 Equidad (data/d4_normative.json)",
        verified        = True,
        note            = (
            "Autocompromiso del GAD. El municipio se fijó IRS ≤ 45 como meta de equidad. "
            "Analíticamente más fuerte que norma externa: es su propio compromiso declarado."
        ),
    ),

    StrategicCommitment(
        objective_id    = "PDOT-AGUA-01",
        sector          = "agua",
        territory       = "RURAL",
        target_metric   = "cobertura_agua_rural",
        target_value    = 0.0,   # sin target numérico vault-verified; se usa gap relativo
        target_direction= "gte",
        deadline        = "2027",
        priority_weight = 0.82,
        norm_source     = "CRE Art. 264(4) — competencia municipal agua potable; D4 patrón INEQUIDAD_HIDRICA",
        verified        = True,
        note            = (
            "No hay target numérico vault-confirmed para cobertura específica. "
            "Se activa cuando D4 detecta INEQUIDAD_HIDRICA como patrón principal. "
            "El compromiso de competencia exclusiva (CRE 264(4)) implica obligación de cobertura territorial."
        ),
    ),

    StrategicCommitment(
        objective_id    = "PDOT-PP-01",
        sector          = "pp",
        territory       = "CANTONAL",
        target_metric   = "parroquias_pp_cubiertas",
        target_value    = 7.0,   # 7 parroquias Montecristi (COOTAD Art. 238 — verificado)
        target_direction= "gte",
        deadline        = "ANUAL",
        priority_weight = 0.75,
        norm_source     = "COOTAD Art. 238 — presupuesto participativo obligatorio",
        verified        = True,
        note            = (
            "Montecristi tiene 7 parroquias. El PP debe cubrir todas. "
            "Si D4 muestra concentración + D1.1 detecta PP incompleto → señal de desacople estratégico."
        ),
    ),

    StrategicCommitment(
        objective_id    = "PDOT-DIST-01",
        sector          = "distribucion",
        territory       = "PARROQUIAS_RURALES",
        target_metric   = "equidad_distribucion_cantonal",
        target_value    = 0.0,   # sin target numérico vault-verified; gap relativo
        target_direction= "gte",
        deadline        = "ANUAL",
        priority_weight = 0.70,
        norm_source     = "COOTAD Art. 272 + CRE Art. 238 — equidad interterritorial",
        verified        = True,
        note            = (
            "Sin target porcentual vault-verified. Se activa cuando D4 detecta CAPTURA_CAPITAL "
            "o CONCENTRACION_TERRITORIAL. La equidad distributiva es obligación normativa, "
            "no meta voluntaria."
        ),
    ),
]

# Índice por sector para lookup rápido
_COMMITMENTS_BY_SECTOR: Dict[str, List[StrategicCommitment]] = {}
for _c in _COMMITMENT_MAP:
    _COMMITMENTS_BY_SECTOR.setdefault(_c.sector, []).append(_c)


# ── CAPA 2: EXECUTION ALIGNMENT ENGINE ───────────────────────────────────────

@dataclass
class AlignmentGaps:
    """
    Brechas de alineamiento entre compromisos PDOT y comportamiento material.

    alignment_gap   — PDOT compromiso vs asignación real (presupuestal)
    execution_gap   — asignación vs ejecución real (Ti)
    territorial_gap — urbano vs rural (IRS actual vs IRS meta PDOT)
    persistence_gap — ¿la brecha es sostenida o puntual? (0-1)
    """
    alignment_gap:   float     # 0-1: qué tan lejos del objetivo de planificación
    execution_gap:   float     # 0-1: qué tan lejos de la ejecución esperada
    territorial_gap: float     # abs(IRS_actual - IRS_meta) / IRS_meta
    persistence_gap: float     # 0=puntual, 1=totalmente persistente
    composite_gap:   float     # media ponderada de los 4 gaps
    n_gaps_active:   int       # cuántos gaps son material (> 0.15)


def compute_alignment_gaps(
    irs_actual:  float,
    irs_meta:    float,
    avep_d3:     float,          # 0-100 (mayor = más riesgo de ejecución)
    d3_pattern:  str,
    d4_pattern:  str,
    cross_conf:  float,
    n_periods:   int = 1,
) -> AlignmentGaps:
    """
    Calcula las 4 brechas de alineamiento a partir de los outputs D3/D4.

    Inputs son observados (no inventados):
      irs_actual  — IRS calculado por RC-D4
      irs_meta    — 45.0 (PDOT vault-verified)
      avep_d3     — AVEP score de RC-7.3 (alta = mala ejecución)
      d3_pattern  — patrón longitudinal
      d4_pattern  — patrón territorial
      cross_conf  — confianza cruzada D3×D4
      n_periods   — períodos disponibles (calibración epistemológica)
    """
    # ── territorial_gap: qué tan lejos del IRS meta PDOT ─────────────────────
    if irs_meta > 0:
        t_gap = max(0.0, (irs_actual - irs_meta) / irs_meta)   # > 0 si IRS > meta
    else:
        t_gap = 0.0
    t_gap = min(1.0, t_gap)

    # ── execution_gap: inferido de AVEP score D3 (alta = mala ejecución) ─────
    # AVEP D3: 100=crítico, 0=excelente ejecución
    e_gap = min(1.0, avep_d3 / 100.0)

    # ── alignment_gap: proximidad entre patrón D3 y patrón D4 ─────────────────
    # Si D3 muestra expansión pero D4 muestra concentración → desacople estratégico
    _misaligned_pairs = {
        ("expansion",    "concentracion"),
        ("expansion",    "captura"),
        ("q4_terminal",  "concentracion"),
        ("q4_terminal",  "captura"),
        ("reforma",      "concentracion"),
        ("reforma",      "captura"),
    }
    _D3_GROUP = {
        "EXPANSION_TARDIA":        "expansion",
        "RECUPERACION_VERIFICADA": "expansion",
        "MANIPULACION_TEMPORAL":   "q4_terminal",
        "CIERRE_TARDIO":           "q4_terminal",
        "REFORMA_LEGITIMA":        "reforma",
        "SHOCK_EXTERNO":           "reforma",
        "DETERIORO_PROGRESIVO":    "contraccion",
        "PARALISIS_ESTRUCTURAL":   "contraccion",
        "INFRAEJECUCION_CRONICA":  "contraccion",
        "SIN_PATRON_CLARO":        "neutral",
    }
    _D4_GROUP = {
        "CONCENTRACION_TERRITORIAL": "concentracion",
        "CAPTURA_CAPITAL":           "captura",
        "REZAGO_PERSISTENTE":        "rezago",
        "INEQUIDAD_HIDRICA":         "hidrica",
        "SESGO_DISTRIBUTIVO":        "sesgo",
        "SIN_PATRON":                "sin_patron",
    }
    d3g = _D3_GROUP.get(d3_pattern, "neutral")
    d4g = _D4_GROUP.get(d4_pattern, "sin_patron")
    a_gap = 0.65 if (d3g, d4g) in _misaligned_pairs else (0.35 if d3g == "contraccion" else 0.10)

    # ── persistence_gap: ¿el patrón es crónico o puntual? ────────────────────
    _PERSISTENT_PATTERNS = {
        "INFRAEJECUCION_CRONICA",
        "DETERIORO_PROGRESIVO",
        "PARALISIS_ESTRUCTURAL",
        "CONCENTRACION_TERRITORIAL",
        "REZAGO_PERSISTENTE",
        "CAPTURA_CAPITAL",
    }
    base_persistence = 0.75 if d3_pattern in _PERSISTENT_PATTERNS or d4_pattern in _PERSISTENT_PATTERNS else 0.25
    # Escalar por n_períodos (más períodos → más certeza sobre persistencia)
    period_factor = min(1.0, n_periods / 4.0)
    p_gap = round(base_persistence * period_factor, 4)

    # ── composite gap (ponderado) ─────────────────────────────────────────────
    # territorial > execution > alignment > persistence
    composite = round(
        0.35 * t_gap
        + 0.30 * e_gap
        + 0.20 * a_gap
        + 0.15 * p_gap,
        4
    )

    n_active = sum(1 for g in [t_gap, e_gap, a_gap, p_gap] if g > 0.15)

    return AlignmentGaps(
        alignment_gap   = round(a_gap, 4),
        execution_gap   = round(e_gap, 4),
        territorial_gap = round(t_gap, 4),
        persistence_gap = p_gap,
        composite_gap   = composite,
        n_gaps_active   = n_active,
    )


# ── CAPA 3: CONTRADICTION CLASSIFIER ─────────────────────────────────────────

def classify_contradiction(
    gaps:       AlignmentGaps,
    confidence: float,
    obs:        bool,
    has_data:   bool,
    n_periods:  int,
) -> D13Status:
    """
    Clasifica el nivel de contradicción estratégica en 5 estados.

    Hereda prudencia inferencial de RC-CORE:
      - obs=True → máximo DESVIACION_MENOR
      - has_data=False → EVIDENCIA_INSUFICIENTE
      - n_periods < 2 → baja al nivel inferior (excepto ALINEADO)
    """
    # Sin datos suficientes → siempre EVIDENCIA_INSUFICIENTE
    if not has_data or confidence < 0.10:
        return D13Status.EVIDENCIA_INSUFICIENTE

    # Observacional (cross_conf < 0.25) → nunca más severo que DESVIACION_MENOR
    if obs:
        if gaps.composite_gap < 0.15:
            return D13Status.ALINEADO
        return D13Status.DESVIACION_MENOR

    # n_períodos insuficiente para afirmar persistencia
    if n_periods < 2 and gaps.persistence_gap > 0.5:
        return D13Status.EVIDENCIA_INSUFICIENTE

    g = gaps.composite_gap
    t = gaps.territorial_gap

    # ── Contradicción crítica ─────────────────────────────────────────────────
    # Ruta A: composite ≥ 0.60 Y territorial_gap ≥ 0.40 Y al menos 3 gaps activos
    if g >= 0.60 and t >= 0.40 and gaps.n_gaps_active >= 3 and confidence >= 0.40:
        return D13Status.CONTRADICCION_CRITICA
    # Ruta B: brecha territorial extrema (≥ 0.60) con al menos 2 gaps activos
    # — un IRS 60%+ por encima del objetivo PDOT siempre es crítico, aunque
    #   la composite no alcance el umbral por ponderación
    if t >= 0.60 and gaps.n_gaps_active >= 2 and confidence >= 0.40:
        return D13Status.CONTRADICCION_CRITICA

    # ── Desviación estratégica ────────────────────────────────────────────────
    # composite ≥ 0.40 Y territorial_gap ≥ 0.20 Y persistence > 0.5
    if g >= 0.40 and t >= 0.20 and gaps.persistence_gap >= 0.50:
        return D13Status.DESVIACION_ESTRATEGICA

    # Variante: sin persistencia alta pero brecha territorial severa
    if g >= 0.50 and t >= 0.35:
        return D13Status.DESVIACION_ESTRATEGICA

    # ── Desviación menor ──────────────────────────────────────────────────────
    if g >= 0.15:
        return D13Status.DESVIACION_MENOR

    # ── Alineado ──────────────────────────────────────────────────────────────
    return D13Status.ALINEADO


# ── CAPA 4: NARRATIVE SYNTHESIZER ────────────────────────────────────────────

def build_coherence_narrative(
    entity_id:   str,
    status:      D13Status,
    gaps:        AlignmentGaps,
    d3_pattern:  str,
    d4_pattern:  str,
    irs_actual:  float,
    irs_meta:    float,
    confidence:  float,
    obs:         bool,
) -> Tuple[str, str]:
    """
    Produce (narrative, hypothesis) — hipótesis institucional auditada.
    Máximo ~400 chars cada una. Nunca acusatoria.

    Returns: (narrative, hypothesis)
      narrative — descripción técnica del estado
      hypothesis — lectura institucional interpretable (la clave de D1.3)
    """
    obs_tag   = " [OBSERVACIONAL]" if obs else ""
    irs_delta = irs_actual - irs_meta
    gap_pct   = f"{gaps.composite_gap:.0%}"

    _STATUS_PHRASES = {
        D13Status.ALINEADO: (
            "muestra coherencia entre compromisos PDOT y comportamiento material",
            f"La ejecución territorial de {entity_id} presenta indicadores de alineamiento "
            f"con el PDOT 2023-2027. IRS actual ({irs_actual:.1f}) dentro del rango esperado "
            f"hacia la meta 2027 (≤ {irs_meta:.0f})."
        ),
        D13Status.EVIDENCIA_INSUFICIENTE: (
            "no tiene densidad suficiente para valoración estratégica prudente",
            f"La densidad de evidencia disponible para {entity_id} no permite una valoración "
            f"estratégica confiable. Se requieren al menos 2 períodos comparables con "
            f"cédulas presupuestarias confirmadas."
        ),
        D13Status.DESVIACION_MENOR: (
            "presenta desviación marginal respecto al compromiso PDOT",
            f"Se detecta un gap de alineamiento menor ({gap_pct}) entre el comportamiento "
            f"presupuestario observado y los objetivos PDOT de {entity_id}. "
            f"IRS actual: {irs_actual:.1f} (meta: ≤ {irs_meta:.0f}, delta: +{irs_delta:.1f}). "
            f"No configura contradicción estratégica en este momento."
        ),
        D13Status.DESVIACION_ESTRATEGICA: (
            "genera indicadores de desacople estratégico sostenido",
            f"El PDOT 2023-2027 de {entity_id} prioriza equidad territorial (IRS ≤ {irs_meta:.0f} "
            f"para 2027); sin embargo, el IRS actual ({irs_actual:.1f}) y el patrón detectado "
            f"({d3_pattern} × {d4_pattern}) sugieren desacople entre planificación estratégica "
            f"y ejecución territorial real. Gap compuesto: {gap_pct}."
        ),
        D13Status.CONTRADICCION_CRITICA: (
            "presenta divergencia estructural entre compromiso declarado y comportamiento material",
            f"Existe una divergencia estructural entre el compromiso PDOT de {entity_id} "
            f"(IRS ≤ {irs_meta:.0f} para 2027) y el comportamiento material observado "
            f"(IRS={irs_actual:.1f}, delta={irs_delta:+.1f}). "
            f"Patrón {d3_pattern} × {d4_pattern} con {gaps.n_gaps_active} brechas activas. "
            f"La divergencia acumulada sugiere desacople estructural entre planificación "
            f"estratégica y ejecución territorial."
        ),
    }

    phrase, hypothesis = _STATUS_PHRASES.get(status, ("", ""))

    narrative = (
        f"[D1.3{obs_tag}] {entity_id} — {status.value}: "
        f"{entity_id} {phrase} (conf={confidence:.0%}, gap={gap_pct}). "
        f"IRS actual={irs_actual:.1f}, meta PDOT 2027=≤{irs_meta:.0f}. "
        f"D3={d3_pattern} · D4={d4_pattern}."
    )[:450]

    return narrative, hypothesis[:400]


# ── DATACLASSES RESULTADO ─────────────────────────────────────────────────────

@dataclass
class D13CoherenceResult:
    """
    Resultado de la verificación RC-D1.3 Normative Coherence.

    status            — D13Status (5 estados)
    confidence        — confianza propagada desde D3×D4
    observational     — True si cross_conf < 0.25 (cap: max DESVIACION_MENOR)
    gaps              — AlignmentGaps (4 brechas calculadas)
    commitments       — compromisos PDOT activados para este chequeo
    narrative         — texto técnico (<450 chars)
    hypothesis        — hipótesis institucional interpretable (<400 chars)
    counterfactual    — ruta positiva de alineamiento
    sat_code          — SAT D1.3 activo (vacío si ALINEADO/EVIDENCIA_INSUFICIENTE)
    irs_actual        — IRS territorial observado
    irs_meta          — IRS objetivo PDOT 2027
    irs_delta         — diferencia (>0 = por encima del objetivo)
    """
    entity_id:    str
    status:       D13Status
    confidence:   float
    observational: bool
    gaps:         AlignmentGaps
    commitments:  List[StrategicCommitment]
    narrative:    str
    hypothesis:   str
    counterfactual: str
    sat_code:     str
    severity:     str   # "alto" | "medio" | "bajo" | "sin_datos"
    d3_pattern:   str
    d4_pattern:   str
    irs_actual:   float
    irs_meta:     float
    irs_delta:    float


# ── SAT Y SEVERIDAD ───────────────────────────────────────────────────────────

_SAT_MAP = {
    D13Status.CONTRADICCION_CRITICA:  ("SAT-D1-D", "alto"),
    D13Status.DESVIACION_ESTRATEGICA: ("SAT-D1-D", "medio"),
    D13Status.DESVIACION_MENOR:       ("",          "bajo"),
    D13Status.ALINEADO:               ("",          "bajo"),
    D13Status.EVIDENCIA_INSUFICIENTE: ("",          "sin_datos"),
}


# ── MOTOR PRINCIPAL ───────────────────────────────────────────────────────────

def analyze_coherence(
    entity_id:  str,
    d3_dict:    Dict[str, Any],
    d4_dict:    Dict[str, Any],
    cross_conf: float = 0.0,
    n_periods:  int   = 1,
    has_data:   bool  = True,
) -> D13CoherenceResult:
    """
    RC-D1.3 — Motor principal de coherencia estratégica.

    Parámetros:
      entity_id  — "GAD" | "EMAI-EP" | "BOMBEROS" | "PATRONATO"
      d3_dict    — output de summarize_calibrated() (RC-7.3)
      d4_dict    — output de summarize_d4_calibrated() (RC-D4)
      cross_conf — confianza cruzada D3×D4
      n_periods  — períodos con datos disponibles
      has_data   — False si no hay cédula presupuestaria

    Solo entidades con compromisos PDOT territoriales tienen chequeo completo.
    EMAI-EP/BOMBEROS/PATRONATO → always EVIDENCIA_INSUFICIENTE (sin PDOT propio).
    """
    # Entidades sin PDOT propio: solo el GAD tiene compromisos PDOT directos
    if entity_id != "GAD":
        return _make_no_pdot_result(entity_id, d3_dict, d4_dict, cross_conf)

    # Extraer estado ejecutivo
    d3_pattern  = d3_dict.get("calibrated_class", "SIN_PATRON_CLARO")
    d3_conf     = float(d3_dict.get("calibrated_confidence", 0.10))
    avep_d3     = float(d3_dict.get("avep_score", 50.0))

    d4_pattern  = d4_dict.get("principal_pattern", "SIN_PATRON")
    d4_conf     = float(d4_dict.get("calibrated_confidence", 0.50))
    irs_actual  = float(d4_dict.get("irs", 50.0))

    # Confianza propagada (mín D3/D4, cap 0.25 = observacional)
    effective_conf = cross_conf if cross_conf > 0 else min(d3_conf, d4_conf)
    effective_conf = round(max(0.05, min(0.95, effective_conf)), 4)
    obs = effective_conf < 0.25

    # Meta PDOT vault-verified
    irs_meta = 45.0   # PDOT Montecristi 2023-2027 — data/d4_normative.json

    # Gaps de alineamiento
    gaps = compute_alignment_gaps(
        irs_actual  = irs_actual,
        irs_meta    = irs_meta,
        avep_d3     = avep_d3,
        d3_pattern  = d3_pattern,
        d4_pattern  = d4_pattern,
        cross_conf  = effective_conf,
        n_periods   = n_periods,
    )

    # Compromisos activados
    activated = _get_activated_commitments(d3_pattern, d4_pattern, irs_actual, irs_meta)

    # Clasificación
    status = classify_contradiction(
        gaps      = gaps,
        confidence= effective_conf,
        obs       = obs,
        has_data  = has_data,
        n_periods = n_periods,
    )

    # Narrativa e hipótesis institucional
    narrative, hypothesis = build_coherence_narrative(
        entity_id  = entity_id,
        status     = status,
        gaps       = gaps,
        d3_pattern = d3_pattern,
        d4_pattern = d4_pattern,
        irs_actual = irs_actual,
        irs_meta   = irs_meta,
        confidence = effective_conf,
        obs        = obs,
    )

    # Counterfactual: ruta de alineamiento positivo
    counterfactual = _build_coherence_counterfactual(status, irs_actual, irs_meta, gaps)

    sat_code, severity = _SAT_MAP.get(status, ("", "bajo"))

    return D13CoherenceResult(
        entity_id     = entity_id,
        status        = status,
        confidence    = effective_conf,
        observational = obs,
        gaps          = gaps,
        commitments   = activated,
        narrative     = narrative,
        hypothesis    = hypothesis,
        counterfactual= counterfactual,
        sat_code      = sat_code,
        severity      = severity,
        d3_pattern    = d3_pattern,
        d4_pattern    = d4_pattern,
        irs_actual    = irs_actual,
        irs_meta      = irs_meta,
        irs_delta     = round(irs_actual - irs_meta, 2),
    )


def _get_activated_commitments(
    d3_pattern: str,
    d4_pattern: str,
    irs_actual: float,
    irs_meta:   float,
) -> List[StrategicCommitment]:
    """Retorna los compromisos PDOT relevantes para la combinación de patrones."""
    activated = []

    # PDOT-EQUIDAD-01: siempre activo (es el compromiso central IRS)
    if irs_actual > irs_meta * 0.80:  # 80% del margen → empieza a activarse
        activated.append(_COMMITMENT_MAP[0])

    # PDOT-AGUA-01: activo si D4 detecta inequidad hídrica
    if d4_pattern == "INEQUIDAD_HIDRICA":
        activated.append(_COMMITMENT_MAP[1])

    # PDOT-PP-01: activo si D4 detecta concentración (PP potencialmente incompleto)
    if d4_pattern in ("CONCENTRACION_TERRITORIAL", "REZAGO_PERSISTENTE", "CAPTURA_CAPITAL"):
        activated.append(_COMMITMENT_MAP[2])

    # PDOT-DIST-01: activo si hay captura capital o sesgo distributivo
    if d4_pattern in ("CAPTURA_CAPITAL", "SESGO_DISTRIBUTIVO", "CONCENTRACION_TERRITORIAL"):
        activated.append(_COMMITMENT_MAP[3])

    return activated or [_COMMITMENT_MAP[0]]  # mínimo siempre el compromiso de equidad


def _build_coherence_counterfactual(
    status:    D13Status,
    irs_actual: float,
    irs_meta:  float,
    gaps:      AlignmentGaps,
) -> str:
    """Ruta positiva de alineamiento hacia el PDOT. Solo si hay desviación."""
    if status == D13Status.ALINEADO:
        return (
            f"La ejecución actual ({irs_actual:.1f} IRS) muestra trayectoria "
            f"compatible con la meta PDOT 2027 (≤ {irs_meta:.0f})."
        )
    if status == D13Status.EVIDENCIA_INSUFICIENTE:
        return (
            "Para activar D1.3 se requiere: (1) cédula presupuestaria cerrada, "
            "(2) datos de distribución parroquial real, (3) al menos 2 períodos comparables."
        )
    delta_needed = irs_actual - irs_meta
    return (
        f"Para alcanzar coherencia PDOT 2027 se requiere reducir el IRS desde "
        f"{irs_actual:.1f} hasta ≤ {irs_meta:.0f} (delta={delta_needed:+.1f}). "
        f"Eso implica redistribución de inversión hacia parroquias con déficit "
        f"territorial (brecha territorial actual: {gaps.territorial_gap:.0%}). "
        f"El mecanismo habilitador es PP completo + ordenanza de distribución cantonal."
    )[:350]


def _make_no_pdot_result(
    entity_id: str,
    d3_dict:   Dict[str, Any],
    d4_dict:   Dict[str, Any],
    cross_conf: float,
) -> D13CoherenceResult:
    """
    Para EMAI-EP/BOMBEROS/PATRONATO: no tienen PDOT propio.
    Su coherencia estratégica se evalúa via el GAD consolidado (Holding).
    D1.3 devuelve EVIDENCIA_INSUFICIENTE con nota explicativa.
    """
    irs = float(d4_dict.get("irs", 0.0))
    d3_pattern = d3_dict.get("calibrated_class", "SIN_PATRON_CLARO")
    d4_pattern = d4_dict.get("principal_pattern", "SIN_PATRON")
    conf = round(max(0.05, min(0.95, cross_conf or 0.10)), 4)

    note = (
        f"{entity_id} no tiene PDOT propio — los compromisos estratégicos territoriales "
        f"son responsabilidad del GAD Municipal. D1.3 para {entity_id} solo es pertinente "
        f"en análisis consolidado del Holding Municipal."
    )
    gaps = AlignmentGaps(0.0, 0.0, 0.0, 0.0, 0.0, 0)

    return D13CoherenceResult(
        entity_id     = entity_id,
        status        = D13Status.EVIDENCIA_INSUFICIENTE,
        confidence    = conf,
        observational = True,
        gaps          = gaps,
        commitments   = [],
        narrative     = f"[D1.3] {entity_id}: {note}",
        hypothesis    = note,
        counterfactual= f"Para analizar coherencia estratégica de {entity_id} usar análisis Holding consolidado.",
        sat_code      = "",
        severity      = "sin_datos",
        d3_pattern    = d3_pattern,
        d4_pattern    = d4_pattern,
        irs_actual    = irs,
        irs_meta      = 45.0,
        irs_delta     = round(irs - 45.0, 2),
    )


# ── SUMMARIZE ─────────────────────────────────────────────────────────────────

def summarize_coherence(result: D13CoherenceResult) -> Dict[str, Any]:
    """Dict compacto para session_state["d13_result"]."""
    return {
        "entity_id":        result.entity_id,
        "status":           result.status.value,
        "confidence":       result.confidence,
        "observational":    result.observational,
        "irs_actual":       result.irs_actual,
        "irs_meta":         result.irs_meta,
        "irs_delta":        result.irs_delta,
        "alignment_gap":    result.gaps.alignment_gap,
        "execution_gap":    result.gaps.execution_gap,
        "territorial_gap":  result.gaps.territorial_gap,
        "persistence_gap":  result.gaps.persistence_gap,
        "composite_gap":    result.gaps.composite_gap,
        "n_gaps_active":    result.gaps.n_gaps_active,
        "n_commitments":    len(result.commitments),
        "sat_code":         result.sat_code,
        "severity":         result.severity,
        "d3_pattern":       result.d3_pattern,
        "d4_pattern":       result.d4_pattern,
        "narrative":        result.narrative,
        "hypothesis":       result.hypothesis,
        "counterfactual":   result.counterfactual,
    }


def get_coherence_prompt_block(result: D13CoherenceResult) -> str:
    """Bloque compacto (<120 tokens) para inyectar en prompt Claude Haiku."""
    obs_tag = "[OBS] " if result.observational else ""
    return (
        f"[D1.3:{result.entity_id}] {obs_tag}{result.status.value} "
        f"conf={result.confidence:.0%} | IRS={result.irs_actual:.1f} meta<={result.irs_meta:.0f} "
        f"delta={result.irs_delta:+.1f} | gap_compuesto={result.gaps.composite_gap:.0%}\n"
        f"  hypothesis: {result.hypothesis[:150]}..."
        if result.status not in (D13Status.ALINEADO, D13Status.EVIDENCIA_INSUFICIENTE)
        else f"[D1.3:{result.entity_id}] {obs_tag}{result.status.value} conf={result.confidence:.0%}"
    )


# ── CONSULTA DIRECTA ──────────────────────────────────────────────────────────

def get_all_commitments() -> List[StrategicCommitment]:
    """Lista de todos los compromisos PDOT vault-verified."""
    return list(_COMMITMENT_MAP)


def get_irs_meta() -> float:
    """Meta PDOT vault-verified para IRS 2027."""
    return 45.0


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D1.3 Normative Coherence — QUIRA OS")
    print("=" * 65)

    print("\n── Compromisos PDOT vault-verified ──")
    for c in get_all_commitments():
        print(f"  [{c.objective_id}] {c.sector} | {c.territory}")
        print(f"    metric={c.target_metric} target={c.target_value} deadline={c.deadline}")
        print(f"    fuente: {c.norm_source[:70]}")

    print("\n── Test 1: GAD — CONTRADICCION_CRITICA (IRS=78, CONCENTRACION×PARALISIS) ──")
    d3_a = {"calibrated_class": "PARALISIS_ESTRUCTURAL", "calibrated_confidence": 0.65, "avep_score": 75.0}
    d4_a = {"principal_pattern": "CONCENTRACION_TERRITORIAL", "calibrated_confidence": 0.70, "irs": 78.3}
    r1 = analyze_coherence("GAD", d3_a, d4_a, cross_conf=0.48, n_periods=3, has_data=True)
    print(f"  Status      : {r1.status.value}")
    print(f"  Confidence  : {r1.confidence:.0%}")
    print(f"  IRS delta   : {r1.irs_delta:+.1f} (meta ≤ {r1.irs_meta:.0f})")
    print(f"  Gaps        : territorial={r1.gaps.territorial_gap:.0%} exec={r1.gaps.execution_gap:.0%} composite={r1.gaps.composite_gap:.0%}")
    print(f"  SAT         : {r1.sat_code}")
    print(f"  Commitments : {len(r1.commitments)}")
    print(f"  Hypothesis  : {r1.hypothesis[:120]}...")

    print("\n── Test 2: GAD — ALINEADO (IRS=42, buen patrón) ──")
    d3_b = {"calibrated_class": "RECUPERACION_VERIFICADA", "calibrated_confidence": 0.75, "avep_score": 20.0}
    d4_b = {"principal_pattern": "SIN_PATRON", "calibrated_confidence": 0.70, "irs": 42.0}
    r2 = analyze_coherence("GAD", d3_b, d4_b, cross_conf=0.55, n_periods=4, has_data=True)
    print(f"  Status      : {r2.status.value}")
    print(f"  IRS delta   : {r2.irs_delta:+.1f}")
    print(f"  Counterfactual: {r2.counterfactual[:80]}...")

    print("\n── Test 3: GAD — Observacional (cross_conf=0.18) ──")
    r3 = analyze_coherence("GAD", d3_a, d4_a, cross_conf=0.18, n_periods=1, has_data=True)
    print(f"  Status      : {r3.status.value}  (debe ser max DESVIACION_MENOR)")
    print(f"  Observational: {r3.observational}")

    print("\n── Test 4: EMAI-EP — sin PDOT propio ──")
    r4 = analyze_coherence("EMAI-EP", d3_a, d4_a, cross_conf=0.45, has_data=True)
    print(f"  Status      : {r4.status.value}  (debe ser EVIDENCIA_INSUFICIENTE)")
    print(f"  Hypothesis  : {r4.hypothesis[:80]}...")

    print("\n── summarize_coherence ──")
    s = summarize_coherence(r1)
    for k, v in list(s.items())[:12]:
        print(f"  {k}: {v}")

    print("\n── Prompt block ──")
    print(get_coherence_prompt_block(r1))
