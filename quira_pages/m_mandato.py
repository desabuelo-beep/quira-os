# -*- coding: utf-8 -*-
"""
m_mandato — página del DOM d03 · Gobernanza del Mandato (Dylus Lab © 2026).

Cajón de DOMINIO (la palabra empeñada · réplica del molde de d01/d02/d09).
HTML autocontenido (Regla 1: la app NO recalcula; lee el snapshot del Gold Master).
"""
from __future__ import annotations

import json
import os

import streamlit as st

_SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")


def render() -> None:
    """QINV-003 · Gobernanza del Mandato — qué pasó con la palabra empeñada ante el electorado."""
    try:
        d = (json.load(open(_SNAP, encoding="utf-8")) or {}).get("mandato_dom") or {}
    except Exception:  # noqa: BLE001
        d = {}
    if not d:
        st.markdown('<div style="font-size:15px;color:#7E8BA3;padding:20px 0">'
                    '— evidencia del mandato pendiente de carga —</div>', unsafe_allow_html=True)
        return
    try:
        from app.viz.render.mandato_render import cajon_mandato_streamlit
    except Exception as e:  # noqa: BLE001
        st.error(f"Cajón de Gobernanza del Mandato no disponible: {e}")
        return
    st.markdown(cajon_mandato_streamlit(d), unsafe_allow_html=True)
