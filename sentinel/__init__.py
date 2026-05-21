"""
SENTINEL Agent Package · QUIRA OS v0.1
Fase: Reader · Lee H73/H99, explica, sugiere pantallas, detecta anomalias.
NO ejecuta acciones autonomas — La autoridad publica decide.
Dylus Lab © 2026
"""
from sentinel.tools   import get_indicator, get_parroquia, get_sat_alerts, get_budget_gap
from sentinel.policies import PUEDE, NO_PUEDE, evaluar_seguridad
from sentinel.audit   import log_interaction, read_audit_log

# RC-7.2 Longitudinal Engine — 4 sub-motores
from sentinel.longitudinal_engine     import (
    BudgetRecord, LongitudinalResult, analyze_series, analyze_multi_entity, summarize_result,
)
from sentinel.administrative_patterns import (
    Pattern, PatternSet, detect_patterns, summarize_pattern_set,
)
from sentinel.institutional_classifier import (
    InstitutionalClass, classify, describe_for_sentinel, summarize_class,
)
from sentinel.normative_binding import (
    NormativeBinding, bind, run_rc72_pipeline, build_rc72_prompt_block,
    get_rc72_context_for_query, summarize_binding,
)
# RC-7.3 Calibration Layer
from sentinel.calibration_layer import (
    CalibratedResult, calibrate, describe_calibrated, summarize_calibrated,
    run_full_pipeline,
)
# RC-7.4 Data Bridge
from sentinel.budget_record_loader import (
    load_budget_records, get_primary_series, get_holding_series,
    get_crosssection_h90, summarize_available_series,
)
# RC-D4 Territorial Equity Engine
from sentinel.d4_engine import (
    ParishRecord, ParishAnalysis, D4Result, analyze_territory, summarize_d4,
)
from sentinel.d4_patterns import (
    D4Pattern, D4PatternSet, detect_d4_patterns, summarize_pattern_set_d4,
)
from sentinel.d4_calibration import (
    CalibratedD4Result, calibrate_d4, describe_d4_calibrated, summarize_d4_calibrated,
)
from sentinel.d4_loader import (
    load_parish_records, run_d4_pipeline, get_d4_context_for_query,
    summarize_d4_pipeline, invalidate_d4_cache,
)
# RC-D4 Visual
from sentinel.ui_components import d4_card, d3d4_card, inference_review_card
# RC-D4 Normative
from sentinel.d4_normative import (
    D4NormRef, D4NormativeBinding,
    bind_d4_from_dict, get_d4_normative_context,
    summarize_d4_normative,
)
# RC-D3D4 Cross-Inference Engine
from sentinel.d3d4_engine import (
    D3State, D4State, D3D4CrossResult,
    analyze_cross, get_cross_context_for_query, summarize_cross,
)
# RC-D3D4-Normative Cross Layer
from sentinel.d3d4_normative import (
    D3D4NormRef, D3D4NormativeBinding,
    bind_cross_from_dict, get_cross_normative_context, summarize_d3d4_normative,
)
# RC-CORE Registry Layer
from sentinel.rc_registry import (
    RC,
    get_threshold, overwhelm_active, needs_tier_cap, get_tier_cap,
    get_tier_language, is_prohibited_language,
    get_pdot_meta, get_eed_class, get_cross_conf, is_observational,
    needs_human_review, audit_registry_consistency,
)
# Provenance Graph
from sentinel.provenance_graph import (
    ProvenanceNode, ProvenanceEdge, ProvenanceGraph,
    get_graph, reset_graph,
    add_source_node, add_transform_node, add_inference_node,
    add_normative_node, add_governed_by,
    get_ancestry, get_confidence_chain, summarize_graph,
    get_provenance_block, export_graph_json,
    register_d3_result, register_d4_result,
    register_cross_result, register_cross_normative,
)
# Human Review — RC-CORE Layer
from sentinel.human_review import (
    InferenceReviewFlag,
    needs_institutional_review, flag_inference,
    get_active_flags, acknowledge_flag,
)
# RC-D1 Legalidad — Competency Graph
from sentinel.d1_competency import (
    D1Status, CompetencyContext, D1CompetencyResult,
    D3_TO_D1_ACTION, D4_TO_D1_ACTION,
    check_competency,
    get_entity_competencies, get_approver, get_norm_refs,
    get_evidence_required, get_d1_competency_block,
)
# RC-D1.2 Procedural Integrity
from sentinel.d1_procedural import (
    D1ProceduralResult, check_procedural,
    get_time_windows, list_entities_with_windows,
)
# RC-D1 Engine (Orchestrator)
from sentinel.d1_engine import (
    D1Result, analyze_d1, summarize_d1,
    get_d1_context_for_query,
)
# RC-D1.3 Normative Coherence
from sentinel.d1_coherence import (
    D13Status, StrategicCommitment, AlignmentGaps, D13CoherenceResult,
    analyze_coherence, summarize_coherence,
    get_coherence_prompt_block, get_all_commitments, get_irs_meta,
)
# RC-D1 Visual
from sentinel.ui_components import d1_card, d1_coherence_card
# RC-SYNTHESIS Meta-Orquestador Epistemologico
from sentinel.synthesis_prioritizer import (
    Signal,
    build_signals, prioritize_signals, determine_dominant_tension,
    DOMINANT_TENSIONS,
)
from sentinel.synthesis_templates import build_hypothesis, build_action_route
from sentinel.synthesis_engine import (
    SynthesisResult,
    synthesize, summarize_synthesis, get_synthesis_prompt_block,
)
from sentinel.ui_components import synthesis_card

__all__ = [
    # Core tools
    "get_indicator", "get_parroquia", "get_sat_alerts", "get_budget_gap",
    "PUEDE", "NO_PUEDE", "evaluar_seguridad",
    "log_interaction", "read_audit_log",
    # RC-7.2 sub-motor 1
    "BudgetRecord", "LongitudinalResult", "analyze_series", "analyze_multi_entity", "summarize_result",
    # RC-7.2 sub-motor 2
    "Pattern", "PatternSet", "detect_patterns", "summarize_pattern_set",
    # RC-7.2 sub-motor 3
    "InstitutionalClass", "classify", "describe_for_sentinel", "summarize_class",
    # RC-7.2 sub-motor 4
    "NormativeBinding", "bind", "run_rc72_pipeline", "build_rc72_prompt_block",
    "get_rc72_context_for_query", "summarize_binding",
    # RC-7.3 Calibration Layer
    "CalibratedResult", "calibrate", "describe_calibrated", "summarize_calibrated",
    "run_full_pipeline",
    # RC-7.4 Data Bridge
    "load_budget_records", "get_primary_series", "get_holding_series",
    "get_crosssection_h90", "summarize_available_series",
    # RC-D4 Territorial Equity Engine
    "ParishRecord", "ParishAnalysis", "D4Result", "analyze_territory", "summarize_d4",
    "D4Pattern", "D4PatternSet", "detect_d4_patterns", "summarize_pattern_set_d4",
    "CalibratedD4Result", "calibrate_d4", "describe_d4_calibrated", "summarize_d4_calibrated",
    "load_parish_records", "run_d4_pipeline", "get_d4_context_for_query",
    "summarize_d4_pipeline", "invalidate_d4_cache",
    # RC-D4 Visual
    "d4_card", "d3d4_card", "inference_review_card",
    # RC-D4 Normative
    "D4NormRef", "D4NormativeBinding",
    "bind_d4_from_dict", "get_d4_normative_context", "summarize_d4_normative",
    # RC-D3D4 Cross-Inference Engine
    "D3State", "D4State", "D3D4CrossResult",
    "analyze_cross", "get_cross_context_for_query", "summarize_cross",
    # RC-D3D4-Normative Cross Layer
    "D3D4NormRef", "D3D4NormativeBinding",
    "bind_cross_from_dict", "get_cross_normative_context", "summarize_d3d4_normative",
    # RC-CORE Registry Layer
    "RC",
    "get_threshold", "overwhelm_active", "needs_tier_cap", "get_tier_cap",
    "get_tier_language", "is_prohibited_language",
    "get_pdot_meta", "get_eed_class", "get_cross_conf", "is_observational",
    "needs_human_review", "audit_registry_consistency",
    # Provenance Graph
    "ProvenanceNode", "ProvenanceEdge", "ProvenanceGraph",
    "get_graph", "reset_graph",
    "add_source_node", "add_transform_node", "add_inference_node",
    "add_normative_node", "add_governed_by",
    "get_ancestry", "get_confidence_chain", "summarize_graph",
    "get_provenance_block", "export_graph_json",
    "register_d3_result", "register_d4_result",
    "register_cross_result", "register_cross_normative",
    # Human Review RC-CORE Layer
    "InferenceReviewFlag",
    "needs_institutional_review", "flag_inference",
    "get_active_flags", "acknowledge_flag",
    # RC-D1 Legalidad — Competency Graph
    "D1Status", "CompetencyContext", "D1CompetencyResult",
    "D3_TO_D1_ACTION", "D4_TO_D1_ACTION",
    "check_competency",
    "get_entity_competencies", "get_approver", "get_norm_refs",
    "get_evidence_required", "get_d1_competency_block",
    # RC-D1.2 Procedural Integrity
    "D1ProceduralResult", "check_procedural",
    "get_time_windows", "list_entities_with_windows",
    # RC-D1 Engine
    "D1Result", "analyze_d1", "summarize_d1",
    "get_d1_context_for_query",
    # RC-D1.3 Normative Coherence
    "D13Status", "StrategicCommitment", "AlignmentGaps", "D13CoherenceResult",
    "analyze_coherence", "summarize_coherence",
    "get_coherence_prompt_block", "get_all_commitments", "get_irs_meta",
    # RC-D1 Visual
    "d1_card", "d1_coherence_card",
    # RC-SYNTHESIS Meta-Orquestador Epistemologico
    "Signal",
    "build_signals", "prioritize_signals", "determine_dominant_tension",
    "DOMINANT_TENSIONS",
    # RC-SYNTHESIS Templates
    "build_hypothesis", "build_action_route",
    # RC-SYNTHESIS Engine
    "SynthesisResult",
    "synthesize", "summarize_synthesis", "get_synthesis_prompt_block",
    # RC-SYNTHESIS Visual
    "synthesis_card",
]
