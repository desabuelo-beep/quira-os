"""
utils — QUIRA OS v0.1
Módulos auxiliares de soporte transversal.
Dylus Lab © 2026
"""
from utils.display_names import tech_to_admin, source_label, indicator_label, INDICATOR_LABELS
from utils.snapshot_io   import validate_snapshot, save_snapshot, load_snapshot, list_snapshots
from utils.page_guards   import (
    sget, sget_nested, require_data, safe_dict_get,
    empty_notice, data_stale_notice, auth_required_notice, guard_suggestion,
)
from utils.session       import init_session, check_session_expiry, is_authenticated, get_rol, get_usuario
from utils.input_guard   import *  # noqa: F401,F403 — re-export existing guards
