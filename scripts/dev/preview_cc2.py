# -*- coding: utf-8 -*-
"""
preview_cc2.py — Harness de verificación visual del Centro de Mando v2
=======================================================================
SOLO DESARROLLO LOCAL. Renderiza p_command_center_v2 con sesión simulada
(rol ejecutivo) SIN tocar el sistema de auth — permite al director ver el
render real con Playwright en localhost y detectar errores de runtime que
el AST/import no capturan. Lección 2026-06-11: verificación con ojos.

Uso:  streamlit run scripts/dev/preview_cc2.py --server.port 8599
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import streamlit as st

st.set_page_config(page_title="DEV · CC v2 preview", layout="wide")

# Sesión simulada (lo que session.py esperaría post-login)
st.session_state.setdefault("autenticado", True)
st.session_state.setdefault("rol", "ejecutivo")
st.session_state.setdefault("login_time", 9e12)

st.markdown(
    '<div style="background:#7C5CFC22;border:1px solid #7C5CFC;padding:4px 10px;'
    'border-radius:8px;font-size:11px;color:#B9A8FF">🔧 PREVIEW DEV — Centro de '
    'Mando v2 · sesión simulada · sin auth real</div>',
    unsafe_allow_html=True,
)

try:
    from quira_pages.p_command_center_v2 import render
    render()
    nav = st.session_state.get("gov_module")
    if nav:
        st.success(f"✅ NAVEGACIÓN DISPARADA → gov_module = '{nav}' (el botón funciona)")
except Exception as e:
    import traceback
    st.error(f"💥 v2 CRASHEÓ: {e}")
    st.code(traceback.format_exc())
