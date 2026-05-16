"""
Backward-compat shim — la View real vive en views/html_engine.py
Las páginas existentes siguen importando desde aquí sin cambios.
"""
from views.html_engine import (  # noqa: F401
    DEMO_CSS,
    page_frame,
    render_page,
    page_header,
    prog_bar,
    sentinel_cta,
)
