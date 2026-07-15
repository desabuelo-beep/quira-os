# -*- coding: utf-8 -*-
"""
m_presupuesto — página del DOM d02 · Presupuesto & Financiamiento (Dylus Lab © 2026).

Cajón de DOMINIO (capacidad financiera territorial · réplica del molde de d01/d09).
HTML autocontenido (Regla 1: la app NO recalcula; lee el snapshot del Gold Master).
"""
from __future__ import annotations

import json
import os

import streamlit as st

_SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")


def render() -> None:
    """QINV-002 · Presupuesto & Financiamiento — la capacidad financiera territorial del municipio."""
    try:
        d = (json.load(open(_SNAP, encoding="utf-8")) or {}).get("presupuesto_dom") or {}
    except Exception:  # noqa: BLE001
        d = {}
    if not d:
        st.markdown('<div style="font-size:15px;color:#7E8BA3;padding:20px 0">'
                    '— evidencia financiera pendiente de carga —</div>', unsafe_allow_html=True)
        return
    try:
        from app.viz.render.presupuesto_render import cajon_presupuesto_streamlit
    except Exception as e:  # noqa: BLE001
        st.error(f"Cajón de Presupuesto & Financiamiento no disponible: {e}")
        return
    st.markdown(cajon_presupuesto_streamlit(d), unsafe_allow_html=True)
