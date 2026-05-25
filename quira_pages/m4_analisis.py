"""
QUIRA OS — Módulo M4: Análisis (Concejal + Técnico)
Consolida Tablero Técnico · Eficiencia · Metas · Cadena · Operación.

Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st
from utils.session import is_tecnico


def render() -> None:
    tabs_base = ["📊 Tablero Técnico", "📋 Eficiencia", "🎯 Metas del Plan"]
    tabs_tec  = ["🔗 Cadena de Planificación", "⚙️ Operación Técnica"]

    labels = tabs_base + (tabs_tec if is_tecnico() else [])
    tabs   = st.tabs(labels)

    with tabs[0]:
        try:
            from quira_pages.p1_dashboard import render as _r
            _r()
        except Exception as e:
            st.error(f"Tablero no disponible: {e}")

    with tabs[1]:
        try:
            from quira_pages.p14_eficiencia import render as _r
            _r()
        except Exception as e:
            st.error(f"Eficiencia no disponible: {e}")

    with tabs[2]:
        try:
            from quira_pages.p8_metas import render as _r
            _r()
        except Exception as e:
            st.error(f"Metas no disponible: {e}")

    if is_tecnico():
        with tabs[3]:
            try:
                from quira_pages.p12_cadena import render as _r
                _r()
            except Exception as e:
                st.error(f"Cadena no disponible: {e}")

        with tabs[4]:
            try:
                from quira_pages.p5_operacion import render as _r
                _r()
            except Exception as e:
                st.error(f"Operación no disponible: {e}")
