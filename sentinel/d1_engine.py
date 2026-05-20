"""
sentinel/d1_engine.py
RC-D1 Legalidad — Motor Orquestador
Dylus Lab © 2026-05-20

FUNCIÓN:
  Orquesta RC-D1.1 (Competency Graph) y RC-D1.2 (Procedural Integrity) para producir
  un análisis de coherencia normativa institucional completo a partir de los resultados
  D3 (temporal) y D4 (territorial).

PIPELINE RC-D1:
  1. Extraer estado ejecutivo de los dicts D3 / D4
  2. Mapear patrones D3 → acciones D1 (contratación, reforma, liquidación, etc.)
  3. Mapear patrones D4 → acciones D1 territoriales (PP, distribución parroquial, etc.)
  4. Para cada acción activada: correr check_competency() (RC-D1.1)
  5. Para cada acción con time_window: correr check_procedural() (RC-D1.2)
  6. Combinar en D1Result con status consolidado, narrativa unificada y SAT activos
  7. Registrar nodo de provenance en el DAG
  8. Evaluar necesidad de human review

OUTPUT:
  D1Result — contiene lista de checks individuales + status_global + prompt block

DOCTRINA INMUTABLE:
  D1 informa — la autoridad pública decide.
  No se emiten juicios de culpabilidad ni veredictos. Solo hipótesis de coherencia.
  Tier máximo si observational_only: "potencial".
  Tier máximo si art. no verificado: "moderada".

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from sentinel.d1_competency import (
    D1Status,
    CompetencyContext,
    D1CompetencyResult,
    D3_TO_D1_ACTION,
    D4_TO_D1_ACTION,
    check_competency,
    get_d1_competency_block,
)
from sentinel.d1_procedural import check_procedural, D1ProceduralResult


# ── ESTADO GLOBAL D1 ──────────────────────────────────────────────────────────

_STATUS_SEVERITY: Dict[D1Status, int] = {
    D1Status.LEGAL:                0,
    D1Status.OBSERVADO:            1,
    D1Status.RIESGO_EVIDENCIA:     2,
    D1Status.RIESGO_PROCEDIMIENTO: 3,
    D1Status.RIESGO_COMPETENCIA:   4,
    D1Status.REQUIERE_REVIEW:      5,
}


# ── DATACLASSES ───────────────────────────────────────────────────────────────

@dataclass
class D1Result:
    """
    Resultado consolidado del motor RC-D1 Legalidad.

    status_global   — el status más severo entre todos los checks individuales
    checks          — lista de D1CompetencyResult (uno por acción activada)
    procedural      — lista de D1ProceduralResult (uno por acción con ventana temporal)
    observational   — True si cross_confidence < 0.25 (cap: solo hipótesis potenciales)
    needs_review    — True si algún check requiere escalación institucional
    d3_pattern      — patrón D3 que activó el análisis (puede ser vacío)
    d4_pattern      — patrón D4 territorial que activó el análisis
    entity_id       — entidad analizada
    narrative       — texto consolidado para inyección en prompt (≤500 chars)
    sat_codes       — SAT codes activos (de D1)
    prompt_block    — bloque compacto (<150 tokens) para Claude Haiku
    confidence      — confianza propagada (mín de D3/D4 cross-confidence)
    timestamp       — fecha de análisis (2026-05-20)
    """
    entity_id:      str
    status_global:  D1Status
    checks:         List[D1CompetencyResult]
    procedural:     List[D1ProceduralResult]
    observational:  bool
    needs_review:   bool
    d3_pattern:     str
    d4_pattern:     str
    narrative:      str
    sat_codes:      List[str]
    prompt_block:   str
    confidence:     float
    timestamp:      str = field(default_factory=lambda: datetime.date.today().isoformat())


# ── ORQUESTADOR PRINCIPAL ─────────────────────────────────────────────────────

def analyze_d1(
    d3_dict:      Dict[str, Any],
    d4_dict:      Dict[str, Any],
    entity_id:    str,
    cross_conf:   float = 0.0,
    has_cedula:   bool  = False,
    current_month: int  = 5,
    current_year:  int  = 2026,
) -> D1Result:
    """
    Motor principal RC-D1 Legalidad.

    Parámetros:
      d3_dict       — output de summarize_calibrated() (RC-7.3)
      d4_dict       — output de summarize_d4_calibrated() (RC-D4)
      entity_id     — "GAD" | "EMAI-EP" | "BOMBEROS" | "PATRONATO"
      cross_conf    — confianza cruzada D3×D4 (de summarize_cross)
      has_cedula    — True si hay cédula presupuestaria disponible
      current_month — mes actual para verificación temporal (1-12)
      current_year  — año actual
    """
    # ── Extraer estado ejecutivo D3 ───────────────────────────────────────────
    d3_pattern  = d3_dict.get("calibrated_class", "SIN_PATRON_CLARO")
    d3_conf     = d3_dict.get("calibrated_confidence", 0.10)
    d3_avep     = d3_dict.get("avep_score", 50.0)

    # ── Extraer estado ejecutivo D4 ───────────────────────────────────────────
    d4_pattern  = d4_dict.get("principal_pattern", "SIN_PATRON")
    d4_conf     = d4_dict.get("calibrated_confidence", 0.50)
    d4_irs      = d4_dict.get("irs", 50.0)
    n_parroquias_pp = d4_dict.get("n_critical_underfunded", 0)

    # Confianza propagada para D1 (mín D3/D4, nunca baja de 0.05)
    effective_conf = cross_conf if cross_conf > 0.0 else min(d3_conf, d4_conf)
    effective_conf = round(max(0.05, min(0.95, effective_conf)), 4)
    observational  = effective_conf < 0.25

    # ── Activar checks desde D3 ───────────────────────────────────────────────
    checks: List[D1CompetencyResult]   = []
    procedural: List[D1ProceduralResult] = []

    d3_action_info = D3_TO_D1_ACTION.get(d3_pattern, (None, "Sin patron D3"))
    d3_action, d3_reason = d3_action_info

    if d3_action:
        reforma_pct = d3_dict.get("reform_pct", 0.0)
        ctx = CompetencyContext(
            entity_id          = entity_id,
            action_type        = d3_action,
            reforma_pct        = reforma_pct,
            d3_pattern         = d3_pattern,
            d4_pattern         = d4_pattern,
            has_cedula_data    = has_cedula,
            evidence_confirmed = [],
            trigger_reason     = d3_reason,
        )
        check = check_competency(ctx, d3_confidence=d3_conf, d4_confidence=d4_conf)
        checks.append(check)

        # Procedural: solo si la acción tiene ventana temporal
        proc = check_procedural(
            entity_id      = entity_id,
            action_type    = d3_action,
            current_month  = current_month,
            current_year   = current_year,
            has_cedula_data = has_cedula,
        )
        if proc is not None:
            procedural.append(proc)

    # ── Activar checks desde D4 (territorial) ────────────────────────────────
    d4_action_info = D4_TO_D1_ACTION.get(d4_pattern, (None, "Sin patron D4"))
    d4_action, d4_reason = d4_action_info

    if d4_action and d4_action != d3_action:  # evitar duplicar el mismo check
        ctx_d4 = CompetencyContext(
            entity_id          = entity_id,
            action_type        = d4_action,
            d3_pattern         = d3_pattern,
            d4_pattern         = d4_pattern,
            n_parroquias_pp    = n_parroquias_pp,
            n_parroquias_total = 7,
            has_cedula_data    = has_cedula,
            evidence_confirmed = [],
            trigger_reason     = d4_reason,
        )
        check_d4 = check_competency(ctx_d4, d3_confidence=d3_conf, d4_confidence=d4_conf)
        checks.append(check_d4)

    # ── Status global: el más severo ──────────────────────────────────────────
    if checks:
        status_global = max(
            [c.status for c in checks],
            key=lambda s: _STATUS_SEVERITY.get(s, 0),
        )
    else:
        status_global = D1Status.OBSERVADO

    # Cap observacional: si observational_only → nunca más severo que OBSERVADO
    if observational and status_global not in (D1Status.LEGAL, D1Status.OBSERVADO):
        status_global = D1Status.OBSERVADO

    # SAT codes D1 activos (de checks con status ≥ RIESGO_EVIDENCIA)
    sat_codes = list({
        c.sat_code for c in checks
        if c.sat_code and _STATUS_SEVERITY.get(c.status, 0) >= 2
    })

    # ── Human Review ─────────────────────────────────────────────────────────
    needs_review = (
        not observational
        and _STATUS_SEVERITY.get(status_global, 0) >= _STATUS_SEVERITY[D1Status.RIESGO_PROCEDIMIENTO]
    )

    # ── Narrativa consolidada ─────────────────────────────────────────────────
    narrative = _build_d1_narrative(
        entity_id, status_global, checks, procedural, effective_conf, observational
    )

    # ── Prompt block compacto (<150 tokens) ──────────────────────────────────
    prompt_block = _build_d1_prompt_block(
        entity_id, status_global, checks, procedural, effective_conf, observational
    )

    return D1Result(
        entity_id      = entity_id,
        status_global  = status_global,
        checks         = checks,
        procedural     = procedural,
        observational  = observational,
        needs_review   = needs_review,
        d3_pattern     = d3_pattern,
        d4_pattern     = d4_pattern,
        narrative      = narrative,
        sat_codes      = sat_codes,
        prompt_block   = prompt_block,
        confidence     = effective_conf,
    )


# ── NARRATIVA Y PROMPT BLOCK ──────────────────────────────────────────────────

def _build_d1_narrative(
    entity_id:    str,
    status:       D1Status,
    checks:       List[D1CompetencyResult],
    procedural:   List[D1ProceduralResult],
    conf:         float,
    obs:          bool,
) -> str:
    """Narrativa consolidada RC-D1 para inyección en prompt (≤500 chars)."""
    obs_tag = " [OBSERVACIONAL]" if obs else ""
    n_risks = sum(
        1 for c in checks
        if _STATUS_SEVERITY.get(c.status, 0) >= 2
    )
    proc_alerts = sum(1 for p in procedural if p.is_overdue)

    base = (
        f"[RC-D1{obs_tag}] {entity_id} — {status.value} (conf={conf:.0%}). "
        f"{n_risks} riesgo(s) de competencia/procedimiento detectado(s). "
    )
    if proc_alerts:
        base += f"{proc_alerts} alerta(s) de ventana temporal vencida. "

    if checks:
        top = max(checks, key=lambda c: _STATUS_SEVERITY.get(c.status, 0))
        base += f"Principal: {top.action_type} → {top.status.value} ({top.approver_required})."

    return base[:500]


def _build_d1_prompt_block(
    entity_id:  str,
    status:     D1Status,
    checks:     List[D1CompetencyResult],
    procedural: List[D1ProceduralResult],
    conf:       float,
    obs:        bool,
) -> str:
    """Bloque compacto (<150 tokens) para Claude Haiku."""
    obs_tag  = "[OBS] " if obs else ""
    lines    = [f"[D1:{entity_id}] {obs_tag}{status.value} conf={conf:.0%}"]

    for c in checks[:3]:
        if _STATUS_SEVERITY.get(c.status, 0) >= 1:
            lines.append(
                f"  {c.action_type}: {c.status.value} | aprobador={c.approver_required[:30]}"
                + (f" | SAT={c.sat_code}" if c.sat_code else "")
            )
    for p in procedural[:2]:
        if p.is_overdue:
            lines.append(f"  PROC-ALERT: {p.action_type} — plazo vencido ({p.deadline_label})")

    return "\n".join(lines)


# ── CONTEXTO PARA QUERY ───────────────────────────────────────────────────────

def get_d1_context_for_query(
    query:      str,
    d3_dict:    Dict[str, Any],
    d4_dict:    Dict[str, Any],
    entity_id:  str,
    cross_conf: float = 0.0,
    has_cedula: bool  = False,
) -> str:
    """
    Genera bloque de contexto D1 para inyectar en el prompt de Claude Haiku.
    Incluye competency map + result summary.
    """
    result = analyze_d1(d3_dict, d4_dict, entity_id, cross_conf, has_cedula)
    comp_block = get_d1_competency_block(entity_id)

    return (
        f"{comp_block}\n\n"
        f"{result.prompt_block}\n\n"
        f"D1-NARRATIVE: {result.narrative}"
    )


# ── SUMMARIZE PARA SESSION STATE ─────────────────────────────────────────────

def summarize_d1(result: D1Result) -> Dict[str, Any]:
    """
    Dict compacto para session_state["d1_result"].
    Solo campos serializables — no dataclasses anidadas.
    """
    top_check = max(result.checks, key=lambda c: _STATUS_SEVERITY.get(c.status, 0)) if result.checks else None
    proc_overdue = [p.action_type for p in result.procedural if p.is_overdue]

    return {
        "entity_id":        result.entity_id,
        "status_global":    result.status_global.value,
        "confidence":       result.confidence,
        "observational":    result.observational,
        "needs_review":     result.needs_review,
        "d3_pattern":       result.d3_pattern,
        "d4_pattern":       result.d4_pattern,
        "sat_codes":        result.sat_codes,
        "n_checks":         len(result.checks),
        "n_risks":          sum(
            1 for c in result.checks if _STATUS_SEVERITY.get(c.status, 0) >= 2
        ),
        "proc_overdue":     proc_overdue,
        "narrative":        result.narrative,
        "prompt_block":     result.prompt_block,
        "top_action":       top_check.action_type if top_check else "",
        "top_approver":     top_check.approver_required if top_check else "",
        "top_sat_code":     top_check.sat_code if top_check else "",
        "top_counterfactual": top_check.counterfactual if top_check else "",
        "top_norm_refs":    top_check.norm_refs if top_check else [],
        "top_evidence_gaps": top_check.evidence_gaps if top_check else [],
        "timestamp":        result.timestamp,
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D1 Legalidad Engine — QUIRA OS")
    print("=" * 65)

    # Simular salida RC-7.3 (D3 temporal) y RC-D4 (territorial)
    d3_mock = {
        "calibrated_class":      "MANIPULACION_TEMPORAL",
        "calibrated_confidence": 0.65,
        "avep_score":            28.0,
        "avep_riesgo":           "Ejecucion Critica",
        "reform_pct":            0.0,
    }
    d4_mock = {
        "principal_pattern":       "CONCENTRACION_TERRITORIAL",
        "calibrated_confidence":   0.72,
        "irs":                     78.3,
        "avep_d4_score":           22.0,
        "avep_d4_riesgo":          "Inequidad Estructural",
        "n_critical_underfunded":  3,
    }

    print("\n── Test 1: GAD — MANIPULACION_TEMPORAL × CONCENTRACION_TERRITORIAL ──")
    r1 = analyze_d1(d3_mock, d4_mock, "GAD", cross_conf=0.48, has_cedula=True)
    print(f"  Status global : {r1.status_global.value}")
    print(f"  Confidence    : {r1.confidence:.0%}")
    print(f"  Observational : {r1.observational}")
    print(f"  Needs review  : {r1.needs_review}")
    print(f"  N checks      : {len(r1.checks)}")
    print(f"  SAT codes D1  : {r1.sat_codes}")
    print(f"  Narrative     : {r1.narrative[:120]}...")
    print(f"  Prompt block  :\n{r1.prompt_block}")

    print("\n── Test 2: EMAI-EP — PARALISIS_ESTRUCTURAL × REZAGO_PERSISTENTE ──")
    d3_ep = {**d3_mock, "calibrated_class": "PARALISIS_ESTRUCTURAL", "calibrated_confidence": 0.55}
    d4_ep = {**d4_mock, "principal_pattern": "REZAGO_PERSISTENTE", "n_critical_underfunded": 4}
    r2 = analyze_d1(d3_ep, d4_ep, "EMAI-EP", cross_conf=0.40, has_cedula=True)
    print(f"  Status global : {r2.status_global.value}")
    print(f"  Needs review  : {r2.needs_review}")
    print(f"  Checks        : {[(c.action_type, c.status.value) for c in r2.checks]}")

    print("\n── Test 3: Observacional (low cross-conf) ──")
    r3 = analyze_d1(d3_mock, d4_mock, "GAD", cross_conf=0.18, has_cedula=False)
    print(f"  Status global : {r3.status_global.value}  (debe ser OBSERVADO por cap)")
    print(f"  Observational : {r3.observational}")

    print("\n── summarize_d1 ──")
    s = summarize_d1(r1)
    for k, v in list(s.items())[:10]:
        print(f"  {k}: {v}")
