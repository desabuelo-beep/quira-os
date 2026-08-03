# -*- coding: utf-8 -*-
"""
m_participacion — página del DOM d08 · Participación Ciudadana (Dylus Lab © 2026).

Cajón de DOMINIO (tres dimensiones: integridad · vitalidad · efectividad — catálogo d08
v1.0.0 · RO-VIII-001/002/003). Réplica del molde de d01/d02/d09.
HTML autocontenido (Regla 1: la app NO recalcula; lee el snapshot del Gold Master).

El bloque `participacion_dom` lo produce scripts/enrich_participacion.py.
"""
from __future__ import annotations

import json
import os

import streamlit as st

_SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")


def render() -> None:
    """QINV-008 · Participación Ciudadana — ¿la voz ciudadana llega a la ejecución?"""
    try:
        d = (json.load(open(_SNAP, encoding="utf-8")) or {}).get("participacion_dom") or {}
    except Exception:  # noqa: BLE001
        d = {}
    if not d:
        st.markdown('<div style="font-size:15px;color:#7E8BA3;padding:20px 0">'
                    '— evidencia de participación pendiente de carga —</div>', unsafe_allow_html=True)
        return
    try:
        from app.viz.render.participacion_render import cajon_participacion_streamlit
    except Exception as e:  # noqa: BLE001
        st.error(f"Cajón de Participación Ciudadana no disponible: {e}")
        return
    st.markdown(cajon_participacion_streamlit(d), unsafe_allow_html=True)
