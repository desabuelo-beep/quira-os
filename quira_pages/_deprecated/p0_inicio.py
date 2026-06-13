"""
QUIRA OS — P-00 Inicio · Sprint A
Ficha cantonal de identidad institucional — Montecristi v1.0

Muestra quién es el municipio (alcalde, período, presupuesto, parroquias)
antes de entrar a los 12 dominios de análisis.
Bloomberg Firewall: ningún índice metodológico (ICPI/TGI/Ti) visible aquí.
Índices van en Sprint C (dashboards por dominio).

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from utils.session import get_rol, is_tecnico, navigate_to
from quira_pages.components.canton_card import render_canton_header

# ── SAT descriptores (fijo — triple anclaje doctrinal) ────────────────────────
_SAT_INFO: dict[str, dict] = {
    "SAT-0":   {"nombre": "Coherencia POA-PAC",           "ley": "LOSNCP Art. 22",        "tipo": "preventiva", "color": "#F59E0B"},
    "SAT-I":   {"nombre": "Fragmentación Selectiva",       "ley": "COPFP Art. 54",          "tipo": "crítica",    "color": "#EF4444"},
    "SAT-II":  {"nombre": "Reforma Significativa Tardía",  "ley": "COPFP Art. 115",         "tipo": "alerta",     "color": "#F97316"},
    "SAT-III": {"nombre": "Parálisis Presupuestaria",      "ley": "COPFP Art. 113",         "tipo": "crítica",    "color": "#EF4444"},
    "SAT-IV":  {"nombre": "Alerta Fiscal COOTAD",          "ley": "COOTAD Art. 192",        "tipo": "legal",      "color": "#DC2626"},
    "SAT-V":   {"nombre": "Brecha Compromiso CPCCS",       "ley": "COOTAD Art. 302",        "tipo": "alerta",     "color": "#F97316"},
    "SAT-VI":  {"nombre": "Desvío Presupuesto Participativo","ley": "COOTAD Art. 238",      "tipo": "alerta",     "color": "#F97316"},
    "SAT-VII": {"nombre": "Pulso Sináptico",               "ley": "—",                      "tipo": "informacional","color": "#64748B"},
    "SAT-VIII":{"nombre": "Equidad Territorial",           "ley": "COOTAD Art. 238 / 247",  "tipo": "informacional","color": "#64748B"},
}

_RIESGO_COLOR: dict[str, str] = {
    "BAJO":    "#22C55E",
    "MEDIO":   "#F59E0B",
    "ALTO":    "#F97316",
    "CRÍTICO": "#EF4444",
}

_ICPI_COLOR: dict[str, str] = {
    "Excelente":          "#22C55E",
    "Saludable":          "#84CC16",
    "En Construcción":    "#F59E0B",
    "Ruptura Sistémica":  "#EF4444",
}


# ─────────────────────────────────────────────────────────────────────────────
def _load_snapshot() -> tuple[dict | None, dict | None]:
    """Carga el snapshot activo de Montecristi con cache de 5 minutos."""
    from utils.cache_quira import cargar_snapshot
    return cargar_snapshot(municipio_code="130801")


def _badge(text: str, color: str, bg: str = "") -> str:
    bg_css = f"background:{bg};" if bg else f"background:{color}22;"
    return (
        f'<span style="display:inline-block;padding:3px 10px;border-radius:6px;'
        f'font-size:11px;font-weight:700;color:{color};'
        f'{bg_css}border:1px solid {color}44;letter-spacing:0.04em">{text}</span>'
    )


def _card_metric(label: str, value: str, sub: str, color: str) -> str:
    return f"""
<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.09);
            border-radius:14px;padding:20px 22px;flex:1;min-width:160px">
    <div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:0.07em;
                text-transform:uppercase;margin-bottom:6px">{label}</div>
    <div style="font-size:2rem;font-weight:900;color:{color};letter-spacing:-0.03em;
                line-height:1">{value}</div>
    <div style="font-size:11px;color:rgba(255,255,255,0.45);margin-top:6px">{sub}</div>
</div>
"""


def _sat_row(codigo: str, info: dict) -> str:
    tipo_label = info["tipo"].upper()
    return f"""
<div style="display:flex;align-items:center;gap:12px;padding:10px 14px;
            background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
            border-left:3px solid {info['color']};border-radius:10px;margin-bottom:6px">
    <span style="font-weight:800;color:{info['color']};font-size:12px;
                 min-width:60px">{codigo}</span>
    <span style="flex:1;font-size:12px;color:#E2E8F0;font-weight:600">{info['nombre']}</span>
    <span style="font-size:10px;color:rgba(255,255,255,0.4)">{info['ley']}</span>
    <span style="font-size:9px;font-weight:700;color:{info['color']};
                 background:{info['color']}22;padding:2px 7px;border-radius:4px;
                 letter-spacing:0.05em">{tipo_label}</span>
</div>
"""


# ─────────────────────────────────────────────────────────────────────────────
def render() -> None:
    rol = get_rol()

    # ── Cargar snapshot ────────────────────────────────────────────────────
    snap, meta = _load_snapshot()

    # ── Extraer alertas SAT del snapshot (si existe) ─────────────────────
    sat_data    = (snap or {}).get("sat",  {})
    alertas_act = sat_data.get("alertas_activas", [])
    n_activas   = sat_data.get("total_activas", len(alertas_act))
    meta_snap   = (snap or {}).get("_meta", {})
    fecha_corte = meta_snap.get("fecha_corte", "")
    source_lbl  = (meta or {}).get("source", "supabase")
    source_note = "Supabase" if source_lbl == "supabase" else "archivo local"

    # ── Ficha cantonal de identidad (Sprint A) ────────────────────────────
    render_canton_header(sat_count=n_activas)

    # ── Sin snapshot: aviso al técnico ───────────────────────────────────
    if not snap:
        st.info(
            "📋 Aún no hay diagnóstico activo para Montecristi. "
            "Ingresá los datos desde **Panel de Carga** para activar el análisis."
        )
        if is_tecnico():
            if st.button("→ Ir al Panel de Carga", type="primary"):
                navigate_to("carga")


    # ── Alertas SAT activas (detalle) ────────────────────────────────────
    if snap and alertas_act:
        st.markdown(f"""
<div style="margin-bottom:8px">
    <span style="font-size:11px;font-weight:700;color:rgba(255,255,255,0.5);
                 letter-spacing:0.07em;text-transform:uppercase">
        Señales de gestión activas ({n_activas})
    </span>
</div>
""", unsafe_allow_html=True)
        rows_html = ""
        for codigo in alertas_act:
            info = _SAT_INFO.get(codigo)
            if info:
                rows_html += _sat_row(codigo, info)
        if rows_html:
            st.markdown(rows_html, unsafe_allow_html=True)

    # ── CTA principal: acceder a los 12 dominios ─────────────────────────
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    col_cta, col_sec = st.columns([2, 3])
    with col_cta:
        if st.button("Explorar 12 dominios de gobernanza →",
                     type="primary", use_container_width=True):
            navigate_to("command_center")

    # ── Accesos secundarios por rol ───────────────────────────────────────
    with col_sec:
        if rol == "Alcalde":
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("📉 Brecha", use_container_width=True):
                    navigate_to("brecha")
            with c2:
                if st.button("🏛️ Grupo Municipal", use_container_width=True):
                    navigate_to("holding")
            with c3:
                if st.button("🧮 Proyector", use_container_width=True):
                    navigate_to("simulador")
        elif rol == "Concejal":
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🚨 Alertas", use_container_width=True):
                    navigate_to("sat")
            with c2:
                if st.button("🎯 Metas PDyOT", use_container_width=True):
                    navigate_to("metas")
            with c3:
                if st.button("🔍 Transparencia", use_container_width=True):
                    navigate_to("transparencia")
        else:  # Técnico
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("⬡ Control", use_container_width=True):
                    navigate_to("sentinel_hub")
            with c2:
                if st.button("⬆️ Carga", use_container_width=True):
                    navigate_to("carga")
            with c3:
                if st.button("🚨 Alertas", use_container_width=True):
                    navigate_to("sat")

    # ── Metadatos ─────────────────────────────────────────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    _corte_lbl = fecha_corte or "Q1-2026"
    st.markdown(f"""
<div style="font-size:9px;color:rgba(255,255,255,0.18);
            border-top:1px solid rgba(255,255,255,0.05);padding-top:10px">
    Fuente: {source_note} · Corte {_corte_lbl} · QUIRA OS Sprint A
</div>
""", unsafe_allow_html=True)
