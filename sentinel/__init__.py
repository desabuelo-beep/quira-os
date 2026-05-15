"""
SENTINEL Agent Package · QUIRA OS v0.1
Fase: Reader · Lee H73/H99, explica, sugiere pantallas, detecta anomalías.
NO ejecuta acciones autónomas — La autoridad pública decide.
Dylus Lab © 2026
"""
from sentinel.tools   import get_indicator, get_parroquia, get_sat_alerts, get_budget_gap
from sentinel.policies import PUEDE, NO_PUEDE, evaluar_seguridad
from sentinel.audit   import log_interaction, read_audit_log

__all__ = [
    "get_indicator", "get_parroquia", "get_sat_alerts", "get_budget_gap",
    "PUEDE", "NO_PUEDE", "evaluar_seguridad",
    "log_interaction", "read_audit_log",
]
