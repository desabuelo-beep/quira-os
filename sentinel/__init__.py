"""
SENTINEL Agent Package · QUIRA OS v0.1
Fase: Reader · Lee H73/H99, explica, sugiere pantallas, detecta anomalías.
NO ejecuta acciones autónomas — La autoridad pública decide.
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
from sentinel.ui_components import d4_card

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
    "d4_card",
]
