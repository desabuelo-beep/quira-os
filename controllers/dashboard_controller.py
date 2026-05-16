"""
QUIRA OS — Controller: Dashboard
Responsabilidad única: orquestar Model + View y manejar eventos de Streamlit.
Dylus Lab © 2026
"""
import streamlit as st
from utils.session import is_tecnico
from models.dashboard import load
from views.dashboard_view import build_html
from views.html_engine import render_page


def run() -> None:
    d         = load()
    show_tech = is_tecnico()

    render_page(build_html(d, show_tech), show_tech=show_tech, height=1000)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔮 Preguntar a Sentinel sobre el ICGI-T",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                f"¿Por qué el ICGI-T bajó de {d.h2025:.2f} en 2025 a {d.h2026:.2f} en Q1-2026 "
                "y qué debe hacer el GAD para alcanzar la meta de 70 al cierre 2026?"
            )
            st.rerun()
    with c2:
        if st.button("📊 Ver Congruencias de Gobernanza", use_container_width=True):
            st.session_state["page"] = "congruencias"
            st.rerun()
