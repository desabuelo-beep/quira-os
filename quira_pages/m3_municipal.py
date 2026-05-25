"""
QUIRA OS — Módulo M3: Municipal
Consolida Grupo Municipal · Participación Ciudadana · Transparencia · Inversión.

Sprint 3 añadirá: Metas del Plan (cuando haya datos longitudinales).

Dylus Lab © 2026
"""
from __future__ import annotations
import streamlit as st


def render() -> None:
    tab_hold, tab_gov, tab_trans, tab_inv = st.tabs([
        "🏛️ Grupo Municipal",
        "🗳️ Participación Ciudadana",
        "🔍 Transparencia Pública",
        "💰 Inversión por Habitante",
    ])

    with tab_hold:
        try:
            from quira_pages.p2_holding import render as _r
            _r()
        except Exception as e:
            st.error(f"Grupo Municipal no disponible: {e}")

    with tab_gov:
        try:
            from quira_pages.p16_gobernanza import render as _r
            _r()
        except Exception as e:
            st.error(f"Participación no disponible: {e}")

    with tab_trans:
        try:
            from quira_pages.p15_transparencia import render as _r
            _r()
        except Exception as e:
            st.error(f"Transparencia no disponible: {e}")

    with tab_inv:
        try:
            from quira_pages.p10_inversion import render as _r
            _r()
        except Exception as e:
            st.error(f"Inversión no disponible: {e}")
