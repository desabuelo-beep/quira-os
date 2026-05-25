"""
QUIRA OS — Módulo M2: Alertas
Consolida Señales SAT · (Sprint 3: Longitudinal SAT · Diff Engine).

Las nuevas vistas de alertas van aquí como tabs.

Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st


def render() -> None:
    # Sprint 2: SAT activo
    # Sprint 3 añadirá: "📈 SAT Longitudinal", "🔍 Comparación de Períodos"
    tab_sat, tab_long = st.tabs([
        "🚨 Señales SAT Activas",
        "📈 Evolución Longitudinal",
    ])

    with tab_sat:
        try:
            from quira_pages.p9_sat import render as _r
            _r()
        except Exception as e:
            st.error(f"SAT no disponible: {e}")

    with tab_long:
        # Placeholder — Sprint 3: Longitudinal Engine
        st.markdown("""
<div style="padding:40px 0;text-align:center;color:rgba(255,255,255,0.3)">
    <div style="font-size:2rem;margin-bottom:12px">📈</div>
    <div style="font-size:14px;font-weight:600">Evolución Longitudinal — Sprint 3</div>
    <div style="font-size:11px;margin-top:6px">
        Visualizará la trayectoria ICPI · SAT · D3 entre períodos<br>
        <code>compare_snapshots(mayo, junio)</code>
    </div>
</div>
        """, unsafe_allow_html=True)
