"""
QUIRA OS — Módulo M5: Control (solo Técnico)
Consolida Centro de Control · Panel de Carga · Ingesta · Historial ·
Monitor de Alertas · Seguimiento · Reportes · Gestión · Sentinel IA.

Regla: todas las herramientas operativas del Técnico viven aquí.
Las nuevas herramientas operativas van como tabs adicionales, no como
nuevos items en el sidebar.

Sprint 3 añadirá: "🔄 Snapshot Diff", "📦 Gold Master Governance"

Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st


def render() -> None:
    tabs = st.tabs([
        "⬡ Centro de Control",
        "⬆️ Panel de Carga",
        "📥 Ingesta Mensual",
        "📈 Historial",
        "🔔 Monitor de Alertas",
        "📊 Seguimiento",
        "📄 Reportes",
        "🗓 Gestión",
        "🔮 Sentinel IA",
    ])

    with tabs[0]:
        try:
            from quira_pages.p_sentinel_hub import render as _r
            _r()
        except Exception as e:
            st.error(f"Centro de Control no disponible: {e}")

    with tabs[1]:
        try:
            from quira_pages.p_carga import render as _r
            _r()
        except Exception as e:
            st.error(f"Panel de Carga no disponible: {e}")

    with tabs[2]:
        try:
            from quira_pages.p_ingesta import render as _r
            _r()
        except Exception as e:
            st.error(f"Ingesta no disponible: {e}")

    with tabs[3]:
        try:
            from quira_pages.p_historico import render as _r
            _r()
        except Exception as e:
            st.error(f"Historial no disponible: {e}")

    with tabs[4]:
        try:
            from quira_pages.p_alertas import render as _r
            _r()
        except Exception as e:
            st.error(f"Monitor de Alertas no disponible: {e}")

    with tabs[5]:
        try:
            from quira_pages.p_seguimiento import render as _r
            _r()
        except Exception as e:
            st.error(f"Seguimiento no disponible: {e}")

    with tabs[6]:
        try:
            from quira_pages.p_reportes import render as _r
            _r()
        except Exception as e:
            st.error(f"Reportes no disponible: {e}")

    with tabs[7]:
        try:
            from quira_pages.p_gestion import render as _r
            _r()
        except Exception as e:
            st.error(f"Gestión no disponible: {e}")

    with tabs[8]:
        try:
            from components.sentinel import render_sentinel
            render_sentinel()
        except Exception as e:
            st.error(f"Sentinel IA no disponible: {e}")
