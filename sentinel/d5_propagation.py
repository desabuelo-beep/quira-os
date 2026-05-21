"""
sentinel/d5_propagation.py
RC-D5 — Motor de Propagacion de Tensiones Institucionales
Dylus Lab © 2026-05-20

FUNCION:
  Analiza como las tensiones detectadas en los motores D3/D4/D3xD4/D1/D1.3
  se propagan y amplifican entre dimensiones del sistema de gobernanza.

  No es un detector de anomalias adicionales.
  Es un analizador de dinamica sistemica: detecta cuales tensiones ya
  confirmadas se refuerzan mutuamente a traves del grafo institucional.

TAXONOMIA DE CASCADAS:
  NINGUNA           — sin propagacion activa
  LINEAL            — 1 camino activo (A -> B)
  CASCADA_DOBLE     — cadena de 3 dimensiones (A -> B -> C)
  RETROALIMENTACION — ciclo detectado (A -> B -> A)
  CASCADA_TOTAL     — 4+ dimensiones en red de propagacion

SEVERIDAD D5:
  5 — CASCADA_TOTAL con amplificacion >= 0.70
  4 — CASCADA_TOTAL (amp < 0.70) O RETROALIMENTACION O CASCADA_DOBLE
  3 — LINEAL con intensidad >= 0.50
  2 — LINEAL con intensidad < 0.50 (no observacional)
  1 — propagacion observacional debil
  0 — ninguna

SAT CODES D5:
  SAT-D5-A — propagacion lineal confirmada (1+ camino activo)
  SAT-D5-B — cascada doble (cadena de 3 dimensiones)
  SAT-D5-C — retroalimentacion detectada (ciclo A->B->A)
  SAT-D5-D — cascada total (4+ dimensiones en red)

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from sentinel.d5_graph import (
    PropagationEdge, PROPAGATION_EDGES, EDGES_BY_SOURCE,
    get_edges_from,
)


# ── EXTRACCION DE ESTADOS ACTIVOS ─────────────────────────────────────────────

def _extract_active_states(
    data: Dict[str, Any],
) -> Dict[str, Tuple[str, float, bool]]:
    """
    Extrae el estado activo de cada dimension con su confianza y flag observacional.
    Retorna {dim: (state, confidence, observational)}.
    """
    active: Dict[str, Tuple[str, float, bool]] = {}

    # D3 — RC-7.3 Calibration Layer
    d3 = data.get("rc73_calibrated") or {}
    d3_cls  = d3.get("calibrated_class", "SIN_PATRON_CLARO")
    d3_conf = float(d3.get("calibrated_confidence", 0.0))
    if d3_cls not in ("SIN_PATRON_CLARO", "") and d3_conf > 0.05:
        active["D3"] = (d3_cls, d3_conf, d3_conf < 0.25)

    # D4 — RC-D4 Territorial
    d4 = data.get("d4_calibrated") or {}
    d4_pat  = d4.get("principal_pattern", "SIN_PATRON")
    d4_conf = float(d4.get("calibrated_confidence", 0.0))
    if d4_pat not in ("SIN_PATRON", "") and d4_conf > 0.05:
        active["D4"] = (d4_pat, d4_conf, d4_conf < 0.35)

    # D3xD4 — Cross-inference
    cross = data.get("d3d4_cross") or {}
    c_pat  = cross.get("cross_pattern", "")
    c_conf = float(cross.get("cross_confidence", 0.0))
    c_obs  = bool(cross.get("observational_only", True))
    if c_pat and c_pat not in ("SIN_CRUCE_CONFIRMADO", "") and c_conf > 0.05:
        active["D3xD4"] = (c_pat, c_conf, c_obs or c_conf < 0.25)

    # D1 — RC-D1 Legalidad
    d1 = data.get("d1_result") or {}
    d1_st   = d1.get("status_global", "")
    d1_conf = float(d1.get("confidence", 0.0))
    d1_obs  = bool(d1.get("observational", True))
    if d1_st and d1_st not in ("LEGAL", "") and d1_conf > 0.05:
        active["D1"] = (d1_st, d1_conf, d1_obs or d1_conf < 0.25)

    # D1.3 — RC-D1.3 Normative Coherence
    d13 = data.get("d13_result") or {}
    d13_st   = d13.get("status", "")
    d13_conf = float(d13.get("confidence", 0.0))
    d13_obs  = bool(d13.get("observational", True))
    if d13_st and d13_st not in ("ALINEADO", "EVIDENCIA_INSUFICIENTE", "") and d13_conf > 0.05:
        active["D1.3"] = (d13_st, d13_conf, d13_obs or d13_conf < 0.25)

    return active


# ── CAMINO ACTIVO ─────────────────────────────────────────────────────────────

@dataclass
class ActivePath:
    """Un camino de propagacion activo en el sistema institucional."""
    source_dim:    str
    source_state:  str
    target_dim:    str
    target_state:  str
    edge_weight:   float
    source_conf:   float
    intensity:     float     # edge_weight x source_conf
    observational: bool
    rationale:     str
    norm_context:  str  = ""
    feedback:      bool = False
    chain_depth:   int  = 1  # profundidad dentro de una cadena


# ── RESULTADO D5 ──────────────────────────────────────────────────────────────

@dataclass
class D5PropagationResult:
    """
    Resultado del motor RC-D5 Tension Propagation Engine.

    entity_id            — entidad analizada
    active_paths         — caminos de propagacion activos (ordenados por intensidad)
    cascade_type         — "NINGUNA"|"LINEAL"|"CASCADA_DOBLE"|"RETROALIMENTACION"|"CASCADA_TOTAL"
    cascade_depth        — longitud del camino mas largo detectado
    dims_involved        — dimensiones involucradas en la red de propagacion
    amplification_factor — intensidad maxima de propagacion
    emergent_risk        — riesgo sistemico no visible en ninguna dimension aislada
    observational        — True si todos los caminos son observacionales
    confidence           — amplificacion maxima (proxy de confianza del motor)
    severity             — 0-5 (escala D5)
    sat_codes            — codigos SAT activos
    prompt_block         — bloque para Claude Haiku (<150 tokens)
    timestamp            — fecha del analisis
    """
    entity_id:            str
    active_paths:         List[ActivePath]
    cascade_type:         str
    cascade_depth:        int
    dims_involved:        List[str]
    amplification_factor: float
    emergent_risk:        str
    observational:        bool
    confidence:           float
    severity:             int
    sat_codes:            List[str]
    prompt_block:         str
    timestamp:            str = field(
        default_factory=lambda: datetime.date.today().isoformat()
    )


# ── DETECCION DE CAMINOS ACTIVOS ──────────────────────────────────────────────

def _find_active_paths(
    active_states: Dict[str, Tuple[str, float, bool]],
) -> List[ActivePath]:
    """
    Identifica los caminos de propagacion activos dado el estado de cada dimension.

    Un camino se activa si:
      1. La dimension fuente tiene estado activo
      2. El estado activo coincide con el estado fuente de la arista
      3. La confianza de la fuente supera el minimo de la arista
    """
    paths: List[ActivePath] = []

    for edge in PROPAGATION_EDGES:
        src = active_states.get(edge.source_dim)
        if src is None:
            continue
        src_state, src_conf, src_obs = src
        if src_state != edge.source_state:
            continue
        if src_conf < edge.min_source_conf:
            continue

        intensity = round(edge.weight * src_conf, 4)
        paths.append(ActivePath(
            source_dim   = edge.source_dim,
            source_state = edge.source_state,
            target_dim   = edge.target_dim,
            target_state = edge.target_state,
            edge_weight  = edge.weight,
            source_conf  = src_conf,
            intensity    = intensity,
            observational = src_obs,
            rationale    = edge.rationale,
            norm_context = edge.norm_context,
            feedback     = edge.feedback,
        ))

    # Ordenar por intensidad descendente
    paths.sort(key=lambda p: (p.intensity, p.edge_weight), reverse=True)
    return paths


# ── DETECCION DE CASCADAS ─────────────────────────────────────────────────────

def _detect_cascade(
    paths:         List[ActivePath],
    active_states: Dict[str, Tuple[str, float, bool]],
) -> Tuple[str, int, List[str]]:
    """
    Clasifica el tipo de cascada y calcula la profundidad maxima.

    Retorna (cascade_type, cascade_depth, dims_involved).
    """
    if not paths:
        return "NINGUNA", 0, []

    # Dimensiones involucradas como fuente o destino
    dims: Set[str] = set()
    for p in paths:
        dims.add(p.source_dim)
        dims.add(p.target_dim)
    dims_list = sorted(dims)

    # Detectar retroalimentacion: caminos A->B y B->A simultaneos
    feedback = False
    for p in paths:
        if any(
            q.source_dim == p.target_dim and q.target_dim == p.source_dim
            for q in paths
        ):
            feedback = True
            break

    # Detectar cadenas de longitud 3+ (A->B->C)
    max_chain = 1
    for p in paths:
        # Segundo salto desde target_dim
        second = [q for q in paths if q.source_dim == p.target_dim]
        for q in second:
            chain_len = 2
            # Tercer salto
            third = [r for r in paths if r.source_dim == q.target_dim and r.target_dim != p.source_dim]
            if third:
                chain_len = 3
            max_chain = max(max_chain, chain_len)

    # Clasificar en orden de prioridad
    n_dims = len(dims_list)
    if n_dims >= 4 or max_chain >= 3:
        return "CASCADA_TOTAL", max_chain, dims_list
    if feedback:
        return "RETROALIMENTACION", 2, dims_list
    if max_chain >= 2:
        return "CASCADA_DOBLE", 2, dims_list
    return "LINEAL", 1, dims_list


# ── SEVERIDAD D5 ──────────────────────────────────────────────────────────────

def _compute_severity(
    cascade_type:   str,
    amplification:  float,
    paths:          List[ActivePath],
) -> int:
    if cascade_type == "NINGUNA":
        return 0
    if cascade_type == "CASCADA_TOTAL" and amplification >= 0.70:
        return 5
    if cascade_type in ("CASCADA_TOTAL", "RETROALIMENTACION", "CASCADA_DOBLE"):
        return 4
    # LINEAL
    if all(p.observational for p in paths):
        return 1
    if amplification >= 0.50:
        return 3
    return 2


# ── SAT CODES ─────────────────────────────────────────────────────────────────

def _compute_sat(cascade_type: str, severity: int) -> List[str]:
    codes: List[str] = []
    if cascade_type == "NINGUNA":
        return codes
    if cascade_type == "CASCADA_TOTAL":
        codes.append("SAT-D5-D")
    if cascade_type == "RETROALIMENTACION":
        codes.append("SAT-D5-C")
    if cascade_type in ("CASCADA_DOBLE",) or (severity >= 4 and "SAT-D5-C" not in codes and "SAT-D5-D" not in codes):
        codes.append("SAT-D5-B")
    # SAT-D5-A siempre cuando hay algun camino
    codes.append("SAT-D5-A")
    return list(dict.fromkeys(codes))   # deduplicate preservando orden


# ── RIESGO EMERGENTE ──────────────────────────────────────────────────────────

_EMERGENT_TEMPLATES: Dict[str, str] = {
    "CASCADA_TOTAL": (
        "La red de propagacion conecta {n_dims} dimensiones simultaneamente. "
        "El riesgo sistemico emergente supera lo observable en cualquier dimension aislada: "
        "la disfuncion opera como ciclo auto-reforzante. "
        "Camino dominante: {top_path}."
    ),
    "RETROALIMENTACION": (
        "Ciclo de retroalimentacion detectado entre dimensiones. "
        "La tension inicial se amplifica al recorrer el ciclo institucional: "
        "sin intervencion, la senal crece en intensidad con cada periodo. "
        "Camino dominante: {top_path}."
    ),
    "CASCADA_DOBLE": (
        "La propagacion atraviesa tres dimensiones en cadena. "
        "El riesgo emergente no es visible en ninguna dimension aislada: "
        "emerge de la dinamica de transmision entre ellas. "
        "Camino dominante: {top_path}."
    ),
    "LINEAL": (
        "La tension en {source} amplifica activamente {target}. "
        "El riesgo combinado supera la suma de las senales individuales. "
        "Intensidad de propagacion: {amp:.0%}."
    ),
    "NINGUNA": "",
}


def _build_emergent_risk(
    cascade_type: str,
    paths:        List[ActivePath],
    entity_id:    str,
) -> str:
    if cascade_type == "NINGUNA" or not paths:
        return ""

    top = paths[0]
    top_path = f"{top.source_dim}:{top.source_state}->{top.target_dim}:{top.target_state}"

    # Dimensiones involucradas
    dims: Set[str] = set()
    for p in paths:
        dims.add(p.source_dim)
        dims.add(p.target_dim)

    template = _EMERGENT_TEMPLATES.get(cascade_type, "")
    try:
        risk = template.format(
            n_dims   = len(dims),
            top_path = top_path,
            source   = top.source_dim,
            target   = top.target_dim,
            amp      = top.intensity,
        )
    except KeyError:
        risk = template

    return risk[:480]


# ── PROMPT BLOCK ──────────────────────────────────────────────────────────────

def _build_prompt_block(
    entity_id:     str,
    cascade_type:  str,
    severity:      int,
    confidence:    float,
    paths:         List[ActivePath],
    dims_involved: List[str],
    emergent_risk: str,
) -> str:
    """Bloque compacto para Claude Haiku (<150 tokens)."""
    if cascade_type == "NINGUNA":
        return f"[D5-PROPAGACION:{entity_id}] sin_cascada_activa"

    obs_tag  = "[OBS] " if all(p.observational for p in paths) else ""
    lines = [
        f"[D5-PROPAGACION:{entity_id}] {obs_tag}{cascade_type} sev={severity}/5",
        f"  dims: {', '.join(dims_involved)}  |  n_caminos: {len(paths)}",
        f"  amplificacion_max: {confidence:.0%}",
    ]
    if paths:
        top = paths[0]
        lines.append(
            f"  camino_dominante: {top.source_dim}:{top.source_state}"
            f"->{top.target_dim}:{top.target_state} ({top.intensity:.0%})"
        )
    if emergent_risk:
        lines.append(f"  riesgo_emergente: {emergent_risk[:130]}...")
    return "\n".join(lines)


# ── MOTOR PRINCIPAL ───────────────────────────────────────────────────────────

def analyze_propagation(
    data:      Dict[str, Any],
    entity_id: str = "GAD",
) -> D5PropagationResult:
    """
    RC-D5 — Motor principal de propagacion de tensiones.

    Parametros:
      data      — dict con todos los resultados de sesion
                  (misma estructura que para synthesize())
      entity_id — entidad activa

    Retorna D5PropagationResult con cascada detectada y riesgo emergente.
    Solo procesa entidades GAD (entidades holding sin PDOT retornan empty).
    """
    # D5 solo aplica a GAD (que tiene PDOT y D4 territorial propio)
    if entity_id not in ("GAD",):
        return _empty_result(entity_id, reason="no_pdot")

    # 1. Extraer estados activos
    active_states = _extract_active_states(data)
    if not active_states:
        return _empty_result(entity_id)

    # 2. Encontrar caminos activos
    paths = _find_active_paths(active_states)
    if not paths:
        return _empty_result(entity_id)

    # 3. Clasificar cascada
    cascade_type, cascade_depth, dims_involved = _detect_cascade(paths, active_states)

    # 4. Amplificacion = intensidad del camino dominante
    amplification = round(paths[0].intensity, 4)

    # 5. Observacional: solo si TODOS los caminos son observacionales
    observational = all(p.observational for p in paths)

    # 6. Severidad
    severity = _compute_severity(cascade_type, amplification, paths)

    # 7. SAT codes
    sat_codes = _compute_sat(cascade_type, severity)

    # 8. Riesgo emergente
    emergent_risk = _build_emergent_risk(cascade_type, paths, entity_id)

    # 9. Prompt block
    prompt_block = _build_prompt_block(
        entity_id, cascade_type, severity, amplification,
        paths, dims_involved, emergent_risk,
    )

    return D5PropagationResult(
        entity_id            = entity_id,
        active_paths         = paths,
        cascade_type         = cascade_type,
        cascade_depth        = cascade_depth,
        dims_involved        = dims_involved,
        amplification_factor = amplification,
        emergent_risk        = emergent_risk,
        observational        = observational,
        confidence           = round(amplification, 4),
        severity             = severity,
        sat_codes            = sat_codes,
        prompt_block         = prompt_block,
    )


def _empty_result(entity_id: str, reason: str = "") -> D5PropagationResult:
    label = "no_propagacion_activa" if not reason else f"no_aplica:{reason}"
    return D5PropagationResult(
        entity_id            = entity_id,
        active_paths         = [],
        cascade_type         = "NINGUNA",
        cascade_depth        = 0,
        dims_involved        = [],
        amplification_factor = 0.0,
        emergent_risk        = "",
        observational        = True,
        confidence           = 0.0,
        severity             = 0,
        sat_codes            = [],
        prompt_block         = f"[D5-PROPAGACION:{entity_id}] {label}",
    )


# ── SUMMARIZE ─────────────────────────────────────────────────────────────────

def summarize_propagation(result: D5PropagationResult) -> Dict[str, Any]:
    """Dict compacto para session_state['d5_propagation']."""
    return {
        "entity_id":            result.entity_id,
        "cascade_type":         result.cascade_type,
        "cascade_depth":        result.cascade_depth,
        "dims_involved":        result.dims_involved,
        "amplification_factor": result.amplification_factor,
        "emergent_risk":        result.emergent_risk,
        "observational":        result.observational,
        "confidence":           result.confidence,
        "severity":             result.severity,
        "sat_codes":            result.sat_codes,
        "n_paths":              len(result.active_paths),
        "prompt_block":         result.prompt_block,
        "active_paths": [
            {
                "source_dim":    p.source_dim,
                "source_state":  p.source_state,
                "target_dim":    p.target_dim,
                "target_state":  p.target_state,
                "intensity":     p.intensity,
                "edge_weight":   p.edge_weight,
                "source_conf":   p.source_conf,
                "observational": p.observational,
                "feedback":      p.feedback,
                "rationale":     p.rationale[:100],
                "norm_context":  p.norm_context,
            }
            for p in result.active_paths[:6]   # max 6 en el dict
        ],
        "timestamp": result.timestamp,
    }


def get_propagation_prompt_block(result: D5PropagationResult) -> str:
    """Bloque listo para inyectar en system prompt."""
    return result.prompt_block


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D5 Motor de Propagacion de Tensiones — QUIRA OS")
    print("=" * 65)

    # Test 1 — GAD con señales multiples (CRISIS_DOBLE escenario)
    mock_full = {
        "rc73_calibrated": {
            "calibrated_class":      "PARALISIS_ESTRUCTURAL",
            "calibrated_confidence": 0.65,
        },
        "d4_calibrated": {
            "principal_pattern":     "CONCENTRACION_TERRITORIAL",
            "calibrated_confidence": 0.78,
            "irs": 78.3,
        },
        "d3d4_cross": {
            "cross_pattern":     "CRISIS_DOBLE",
            "cross_confidence":  0.50,
            "observational_only": False,
        },
        "d1_result": {
            "status_global": "RIESGO_DE_PROCEDIMIENTO",
            "confidence":    0.45,
            "observational": False,
        },
        "d13_result": {
            "status":        "CONTRADICCION_CRITICA",
            "confidence":    0.48,
            "observational": False,
        },
        "inference_review_flag": None,
    }

    print("\n-- Test 1: GAD escenario CRISIS_DOBLE + multiples señales --")
    r1 = analyze_propagation(mock_full, "GAD")
    print(f"  cascade_type     : {r1.cascade_type}")
    print(f"  cascade_depth    : {r1.cascade_depth}")
    print(f"  dims_involved    : {r1.dims_involved}")
    print(f"  amplification    : {r1.amplification_factor:.0%}")
    print(f"  severity         : {r1.severity}/5")
    print(f"  observational    : {r1.observational}")
    print(f"  sat_codes        : {r1.sat_codes}")
    print(f"  n_active_paths   : {len(r1.active_paths)}")
    print(f"  emergent_risk[:120]: {r1.emergent_risk[:120]}")
    print(f"\n  Prompt block:\n{r1.prompt_block}")

    print("\n-- Test 2: GAD solo D3 con baja confianza --")
    mock_low = {
        "rc73_calibrated": {
            "calibrated_class":      "PARALISIS_ESTRUCTURAL",
            "calibrated_confidence": 0.20,   # bajo el min_source_conf=0.35
        },
        "d4_calibrated": {"principal_pattern": "SIN_PATRON", "calibrated_confidence": 0.50},
        "d3d4_cross": None,
        "d1_result": None,
        "d13_result": None,
        "inference_review_flag": None,
    }
    r2 = analyze_propagation(mock_low, "GAD")
    print(f"  cascade_type : {r2.cascade_type}  (debe ser NINGUNA — conf insuficiente)")

    print("\n-- Test 3: EMAI-EP (no tiene PDOT — debe retornar NINGUNA) --")
    r3 = analyze_propagation(mock_full, "EMAI-EP")
    print(f"  cascade_type : {r3.cascade_type}  (debe ser NINGUNA)")
    print(f"  prompt_block : {r3.prompt_block}")

    print("\n-- Test 4: Solo D4 alta conf --")
    mock_d4only = {
        "rc73_calibrated": None,
        "d4_calibrated": {
            "principal_pattern":     "CONCENTRACION_TERRITORIAL",
            "calibrated_confidence": 0.85,
        },
        "d3d4_cross": None,
        "d1_result": None,
        "d13_result": None,
        "inference_review_flag": None,
    }
    r4 = analyze_propagation(mock_d4only, "GAD")
    print(f"  cascade_type : {r4.cascade_type}")
    print(f"  dims         : {r4.dims_involved}")
    print(f"  n_paths      : {len(r4.active_paths)}")
    for p in r4.active_paths[:3]:
        print(f"    {p.source_dim}:{p.source_state} -> {p.target_dim}:{p.target_state} ({p.intensity:.0%})")

    print("\n-- summarize_propagation (Test 1) --")
    s = summarize_propagation(r1)
    for k, v in list(s.items())[:8]:
        if not isinstance(v, list):
            print(f"  {k}: {v}")
        else:
            print(f"  {k}: [{len(v)} items]")
