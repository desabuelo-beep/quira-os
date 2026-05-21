"""
sentinel/synthesis_engine.py
RC-SYNTHESIS — Meta-Orquestador Epistemológico
Dylus Lab © 2026-05-20

FUNCIÓN:
  Toma los resultados de todos los motores RC (D3/D4/D3×D4/D1/D1.3/Provenance/HumanReview)
  y produce UNA síntesis priorizada con máximo 3 señales accionables.

  Es el filtro entre la complejidad del stack y el decisor institucional.

  No es un "summary". No suma tensiones linealmente.
  Es un meta-orquestador epistemológico que:
    * Identifica qué tensión domina el sistema
    * Preserva cuál dimensión tiene mayor evidencia
    * Suprime señales observacionales que no merecen atención inmediata
    * Produce una hipótesis institucional emergente de la combinación
    * Comprime la evidencia a 1-3 señales accionables

DOCTRINA INMUTABLE (las 3 reglas del colega):
  1. Nunca sumar tensiones linealmente → tipos institucionales emergentes
  2. La dimensión con mayor evidencia domina → conf es primaria en ranking
  3. Máximo 3 señales → siempre; sin excepciones

SEVERIDAD DE SYNTHESIS:
  CRITICA  — señal con severity≥5 Y conf≥0.40 Y no observacional
  ALTA     — señal con severity≥4 Y conf≥0.35
  MEDIA    — señal con severity≥3 O (2 señales severity≥2)
  BAJA     — todas severity≤2
  NINGUNA  — sin señales activas

OUTPUT:
  SynthesisResult — tipo único que entra al prompt de Claude Haiku
  summarize_synthesis() — dict para session_state["synthesis"]
  get_synthesis_prompt_block() — bloque compacto (<200 tokens)

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from sentinel.synthesis_prioritizer import (
    Signal, prioritize_signals, determine_dominant_tension,
    DOMINANT_TENSIONS,
)
from sentinel.synthesis_templates import build_hypothesis, build_action_route


# ── SEVERIDAD GLOBAL ──────────────────────────────────────────────────────────

def _compute_severity(top_signals: List[Signal]) -> str:
    """
    Severidad global de la síntesis.
    Primaria: confianza × severidad cardinal. No alarma por señales débiles.
    """
    if not top_signals:
        return "NINGUNA"

    top = top_signals[0]

    if top.severity >= 5 and top.confidence >= 0.40 and not top.observational:
        return "CRITICA"
    if top.severity >= 4 and top.confidence >= 0.35:
        return "ALTA"
    n_medium = sum(1 for s in top_signals if s.severity >= 3)
    n_minor  = sum(1 for s in top_signals if s.severity >= 2)
    if n_medium >= 1 or n_minor >= 2:
        return "MEDIA"
    return "BAJA"


# ── COMPRESIÓN DE EVIDENCIA ───────────────────────────────────────────────────

def _compress_evidence(top_signals: List[Signal]) -> str:
    """
    Cadena compacta de evidencia para el prompt block (~80 tokens).
    """
    if not top_signals:
        return "Sin evidencia suficiente para síntesis."
    parts = []
    for s in top_signals:
        obs_tag = "[OBS] " if s.observational else ""
        parts.append(
            f"{s.source}:{obs_tag}{s.label} (conf={s.confidence:.0%}, sev={s.severity})"
        )
    return " | ".join(parts)


# ── DATACLASS RESULTADO ───────────────────────────────────────────────────────

@dataclass
class SynthesisResult:
    """
    Resultado del meta-orquestador epistemológico RC-SYNTHESIS.

    dominant_tension      — tipo institucional emergente (semántico, no un score)
    severity              — "CRITICA" | "ALTA" | "MEDIA" | "BAJA" | "NINGUNA"
    confidence            — del motor con mayor evidencia en top_signals
    observational         — True si el motor dominante es observacional
    top_signals           — máximo 3 señales priorizadas
    suppressed_dimensions — engines con señales que no alcanzaron el top-3
    institutional_hypothesis — hipótesis interpretable (~300 chars)
    action_route          — 2-3 pasos concretos para la autoridad
    evidence_summary      — cadena compacta de evidencia (~80 tokens)
    needs_human_review    — True si human_review flag está activo
    entity_id             — entidad analizada
    prompt_block          — bloque compacto para Claude Haiku (<200 tokens)
    timestamp             — fecha del análisis
    """
    entity_id:               str
    dominant_tension:        str
    severity:                str
    confidence:              float
    observational:           bool
    top_signals:             List[Signal]
    suppressed_dimensions:   List[str]
    institutional_hypothesis: str
    action_route:            List[str]
    evidence_summary:        str
    needs_human_review:      bool
    prompt_block:            str
    timestamp:               str = field(default_factory=lambda: datetime.date.today().isoformat())


# ── MOTOR PRINCIPAL ───────────────────────────────────────────────────────────

def synthesize(
    data:      Dict[str, Any],
    entity_id: str = "GAD",
) -> SynthesisResult:
    """
    RC-SYNTHESIS — Motor principal.

    Parámetros:
      data      — dict con todos los resultados de sesión:
                  rc73_calibrated, d4_calibrated, d3d4_cross, d1_result,
                  d13_result, inference_review_flag
      entity_id — entidad activa

    Retorna SynthesisResult con síntesis priorizada (máximo 3 señales).
    """
    # ── Priorización ──────────────────────────────────────────────────────────
    top_signals, suppressed = prioritize_signals(data, max_signals=3)

    # ── Tensión dominante (semántica, no score) ───────────────────────────────
    dominant_tension = determine_dominant_tension(top_signals)

    # ── Severidad global ──────────────────────────────────────────────────────
    severity = _compute_severity(top_signals)

    # ── Confianza del motor dominante ─────────────────────────────────────────
    conf = top_signals[0].confidence if top_signals else 0.0
    obs  = top_signals[0].observational if top_signals else True

    # ── Human review ─────────────────────────────────────────────────────────
    hr_flag       = data.get("inference_review_flag") or {}
    needs_review  = bool(hr_flag) and not hr_flag.get("acknowledged", True)

    # ── Contexto para templates ───────────────────────────────────────────────
    d4  = data.get("d4_calibrated")  or {}
    d13 = data.get("d13_result")     or {}
    d1  = data.get("d1_result")      or {}
    ctx = {
        "irs_actual":   float(d4.get("irs",          50.0)),
        "irs_meta":     float(d13.get("irs_meta",     45.0)),
        "n_critical":   int(d4.get("n_critical_underfunded", 0)),
        "top_action":   d1.get("top_action", ""),
        "entity_id":    entity_id,
    }

    # ── Hipótesis institucional ───────────────────────────────────────────────
    hypothesis = build_hypothesis(dominant_tension, top_signals, entity_id, ctx)

    # ── Ruta de acción ────────────────────────────────────────────────────────
    action_route = build_action_route(dominant_tension, top_signals, entity_id)

    # ── Compresión de evidencia ───────────────────────────────────────────────
    evidence_summary = _compress_evidence(top_signals)

    # ── Prompt block (<200 tokens) ───────────────────────────────────────────
    prompt_block = _build_prompt_block(
        entity_id, dominant_tension, severity, conf, obs,
        top_signals, hypothesis, needs_review
    )

    return SynthesisResult(
        entity_id               = entity_id,
        dominant_tension        = dominant_tension,
        severity                = severity,
        confidence              = round(conf, 4),
        observational           = obs,
        top_signals             = top_signals,
        suppressed_dimensions   = suppressed,
        institutional_hypothesis = hypothesis,
        action_route            = action_route,
        evidence_summary        = evidence_summary,
        needs_human_review      = needs_review,
        prompt_block            = prompt_block,
    )


def _build_prompt_block(
    entity_id:        str,
    dominant_tension: str,
    severity:         str,
    conf:             float,
    obs:              bool,
    top_signals:      List[Signal],
    hypothesis:       str,
    needs_review:     bool,
) -> str:
    """Bloque compacto para Claude Haiku (<200 tokens)."""
    obs_tag  = "[OBS] " if obs else ""
    rev_tag  = " | REVISION_REQUERIDA" if needs_review else ""
    tension_desc = DOMINANT_TENSIONS.get(dominant_tension, dominant_tension)

    lines = [
        f"[SENTINEL-SYNTHESIS:{entity_id}] {obs_tag}{severity}{rev_tag}",
        f"  tension_dominante: {dominant_tension}",
        f"  descripcion: {tension_desc[:60]}",
        f"  conf_dominante: {conf:.0%}",
    ]
    for i, s in enumerate(top_signals[:3], 1):
        obs_s = "[OBS] " if s.observational else ""
        lines.append(f"  señal_{i}: {s.source}:{obs_s}{s.label} (conf={s.confidence:.0%}, sev={s.severity})")
    lines.append(f"  hipotesis: {hypothesis[:180]}...")
    return "\n".join(lines)


# ── SUMMARIZE ─────────────────────────────────────────────────────────────────

def summarize_synthesis(result: SynthesisResult) -> Dict[str, Any]:
    """Dict compacto para session_state['synthesis']."""
    return {
        "entity_id":               result.entity_id,
        "dominant_tension":        result.dominant_tension,
        "severity":                result.severity,
        "confidence":              result.confidence,
        "observational":           result.observational,
        "needs_human_review":      result.needs_human_review,
        "n_signals":               len(result.top_signals),
        "suppressed_dimensions":   result.suppressed_dimensions,
        "institutional_hypothesis": result.institutional_hypothesis,
        "action_route":            result.action_route,
        "evidence_summary":        result.evidence_summary,
        "prompt_block":            result.prompt_block,
        "top_signals": [
            {
                "source":        s.source,
                "label":         s.label,
                "confidence":    s.confidence,
                "severity":      s.severity,
                "observational": s.observational,
                "sat_codes":     s.sat_codes,
                "description":   s.description,
            }
            for s in result.top_signals
        ],
        "timestamp": result.timestamp,
    }


def get_synthesis_prompt_block(result: SynthesisResult) -> str:
    """Bloque listo para inyectar en system prompt."""
    return result.prompt_block


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-SYNTHESIS Meta-Orquestador Epistemologico — QUIRA OS")
    print("=" * 65)

    # Simular session_state completo con señales múltiples
    mock_data = {
        "rc73_calibrated": {
            "calibrated_class":      "PARALISIS_ESTRUCTURAL",
            "calibrated_confidence": 0.65,
            "avep_score":            72.0,
            "sat_codes_calibrated":  ["SAT-X-C"],
            "n_periodos": 3,
        },
        "d4_calibrated": {
            "principal_pattern":       "CONCENTRACION_TERRITORIAL",
            "calibrated_confidence":   0.78,
            "irs":                     78.3,
            "avep_d4_score":           22.0,
            "sat_codes":               ["SAT-D4-A"],
            "n_critical_underfunded":  4,
        },
        "d3d4_cross": {
            "cross_pattern":    "CRISIS_DOBLE",
            "cross_confidence": 0.50,
            "observational_only": False,
            "eed_score":         50.0,
            "sat_codes":        ["SAT-D3D4-A"],
            "d3_confidence":    0.65,
            "d4_confidence":    0.78,
        },
        "d1_result": {
            "status_global": "RIESGO_DE_PROCEDIMIENTO",
            "confidence":    0.45,
            "observational": False,
            "needs_review":  True,
            "sat_codes":     ["SAT-D1-A"],
            "top_action":    "reforma_presupuestaria",
        },
        "d13_result": {
            "status":      "CONTRADICCION_CRITICA",
            "confidence":  0.48,
            "observational": False,
            "irs_actual":  78.3,
            "irs_meta":    45.0,
            "irs_delta":   33.3,
            "composite_gap": 0.64,
            "sat_code":    "SAT-D1-D",
        },
        "inference_review_flag": None,
    }

    print("\n── Test 1: GAD con señales múltiples (CRISIS_DOBLE + CONTRADICCION_CRITICA) ──")
    r1 = synthesize(mock_data, "GAD")
    print(f"  dominant_tension : {r1.dominant_tension}")
    print(f"  severity         : {r1.severity}")
    print(f"  confidence       : {r1.confidence:.0%}")
    print(f"  observational    : {r1.observational}")
    print(f"  n_signals        : {len(r1.top_signals)}")
    print(f"  suppressed       : {r1.suppressed_dimensions}")
    print(f"  hypothesis       : {r1.institutional_hypothesis[:140]}...")
    print(f"  action_route:")
    for i, a in enumerate(r1.action_route, 1):
        print(f"    {i}. {a[:80]}")
    print(f"\n  Prompt block:\n{r1.prompt_block}")

    print("\n── Test 2: Solo D3 observacional (baja conf) ──")
    mock_low = {
        "rc73_calibrated": {
            "calibrated_class": "SIN_PATRON_CLARO",
            "calibrated_confidence": 0.07,
            "avep_score": 50.0,
            "sat_codes_calibrated": [],
        },
        "d4_calibrated": {"principal_pattern": "SIN_PATRON", "calibrated_confidence": 0.50, "irs": 42.0, "n_critical_underfunded": 0, "sat_codes": []},
        "d3d4_cross": None,
        "d1_result": None,
        "d13_result": None,
        "inference_review_flag": None,
    }
    r2 = synthesize(mock_low, "GAD")
    print(f"  dominant_tension : {r2.dominant_tension}")
    print(f"  severity         : {r2.severity}")
    print(f"  n_signals        : {len(r2.top_signals)}")

    print("\n── Test 3: D4 dominante con conf alta, D3 conf baja ──")
    mock_d4dom = {**mock_data,
        "rc73_calibrated": {**mock_data["rc73_calibrated"], "calibrated_confidence": 0.07},
        "d3d4_cross": None,
        "d1_result": None,
        "d13_result": None,
    }
    r3 = synthesize(mock_d4dom, "GAD")
    print(f"  dominant_tension : {r3.dominant_tension}  (D4 con conf=0.78 debe dominar)")
    print(f"  confidence       : {r3.confidence:.0%}  (debe reflejar D4)")

    print("\n── summarize_synthesis (primeras 10 claves) ──")
    s = summarize_synthesis(r1)
    for k, v in list(s.items())[:10]:
        if not isinstance(v, list):
            print(f"  {k}: {v}")
        else:
            print(f"  {k}: [{len(v)} items]")
