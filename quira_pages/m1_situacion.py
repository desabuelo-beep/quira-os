"""
QUIRA OS — Módulo M1: Situación
Consolida Vista Ejecutiva · Pulso · Causas de la Brecha en tabs.

Regla de módulos: las nuevas vistas de situación van aquí como tabs,
NO como items nuevos en el sidebar.

Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st


def render() -> None:
    tab_exec, tab_pulso, tab_brecha = st.tabs([
        "🏛 Vista Ejecutiva",
        "⚡ Pulso del Municipio",
        "📉 Causas de la Brecha",
    ])

    with tab_exec:
        try:
            from quira_pages.p_ejecutivo import render as _r
            _r()
        except Exception as e:
            st.error(f"Vista Ejecutiva no disponible: {e}")

    with tab_pulso:
        try:
            from quira_pages.p6_pulso import render as _r
            _r()
        except Exception as e:
            st.error(f"Pulso no disponible: {e}")

    with tab_brecha:
        try:
            from quira_pages.p7_brecha import render as _r
            _r()
        except Exception as e:
            st.error(f"Brecha no disponible: {e}")
