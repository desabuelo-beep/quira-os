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
]
