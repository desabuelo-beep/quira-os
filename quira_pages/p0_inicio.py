"""
QUIRA OS — P-00 Inicio
Pantalla de entrada consolidada · Sprint 2

Muestra el estado real del municipio según el último snapshot Q1:
  · ICPI global (53.56% → Ruptura Sistémica)
  · Alertas SAT activas (SAT-III / SAT-IV / SAT-V)
  · Nivel de riesgo ponderado (ALTO)
  · Accesos directos por rol

Carga datos desde municipality_snapshots (Supabase).
Si no hay snapshot activo muestra aviso de ingesta pendiente.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from utils.session import get_rol, is_tecnico, navigate_to

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
    """Carga el snapshot activo de Montecristi desde Supabase o JSON estático."""
    try:
        from utils.snapshot_io import load_snapshot
        return load_snapshot(municipio_code="130801")
    except Exception:
        return None, None


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

    # ── Header ─────────────────────────────────────────────────────────────
    st.markdown("""
<div style="margin-bottom:24px">
    <div style="font-size:1.1rem;font-weight:900;color:#E2E8F0;letter-spacing:-0.02em">
        Estado del Municipio
    </div>
    <div style="font-size:12px;color:rgba(255,255,255,0.35);margin-top:2px">
        Montecristi · Q1 2026 · Corte enero–marzo
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Sin snapshot ─────────────────────────────────────────────────────
    if not snap:
        st.warning(
            "⚠️ No hay snapshot activo para Montecristi. "
            "Ejecuta el pipeline desde **Centro de Control → Panel de Carga** para generar el primer diagnóstico."
        )
        if is_tecnico():
            if st.button("→ Ir al Panel de Carga", type="primary"):
                navigate_to("carga")
        return

    # ── Extraer datos del snapshot ────────────────────────────────────────
    icpi_data   = snap.get("icpi", {})
    sat_data    = snap.get("sat",  {})
    tgi_data    = snap.get("tgi",  {})
    meta_snap   = snap.get("_meta", {})

    icpi_pct    = icpi_data.get("global_pct") or icpi_data.get("global")
    icpi_clasif = icpi_data.get("clasificacion", "—")

    riesgo_pond = sat_data.get("riesgo_ponderado", 0.0)
    clasif_sat  = sat_data.get("clasif_riesgo", "—").upper()
    alertas_act = sat_data.get("alertas_activas", [])
    n_activas   = sat_data.get("total_activas", len(alertas_act))
    tgi_score   = tgi_data.get("score")

    fecha_corte = meta_snap.get("fecha_corte", "")
    source_lbl  = (meta or {}).get("source", "supabase")
    source_note = "Supabase" if source_lbl == "supabase" else "archivo local"

    icpi_str    = f"{icpi_pct:.1f}%" if icpi_pct is not None else "—"
    tgi_str     = f"{tgi_score:.1f}" if tgi_score is not None else "—"
    riesgo_str  = f"{riesgo_pond * 100:.1f}%" if riesgo_pond else "—"

    icpi_color  = _ICPI_COLOR.get(icpi_clasif, "#F59E0B")
    riesgo_col  = _RIESGO_COLOR.get(clasif_sat, "#F97316")

    # ── Métricas principales ──────────────────────────────────────────────
    m_icpi  = _card_metric("ICPI Global", icpi_str,    icpi_clasif,     icpi_color)
    m_riesg = _card_metric("Riesgo SAT",  clasif_sat,  f"{n_activas} alertas activas", riesgo_col)
    m_tgi   = _card_metric("TGI Score",   tgi_str,     "Índice TGI D1-D5", "#64748B" if tgi_str == "—" else "#00D4FF")

    st.markdown(f"""
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px">
    {m_icpi}{m_riesg}{m_tgi}
</div>
""", unsafe_allow_html=True)

    # ── Alertas SAT activas ───────────────────────────────────────────────
    if alertas_act:
        st.markdown(f"""
<div style="margin-bottom:8px">
    <span style="font-size:12px;font-weight:700;color:rgba(255,255,255,0.6);
                 letter-spacing:0.07em;text-transform:uppercase">
        🚨 Alertas SAT Activas ({n_activas})
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
    else:
        st.success("✅ Sin alertas SAT activas en el período.")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Accesos rápidos por rol ───────────────────────────────────────────
    st.markdown("""
<div style="font-size:12px;font-weight:700;color:rgba(255,255,255,0.6);
             letter-spacing:0.07em;text-transform:uppercase;margin-bottom:10px">
    Accesos Rápidos
</div>
""", unsafe_allow_html=True)

    if rol == "Alcalde":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("📊 Tablero Ejecutivo", use_container_width=True):
                navigate_to("ejecutivo")
        with c2:
            if st.button("📉 Causas de la Brecha", use_container_width=True):
                navigate_to("brecha")
        with c3:
            if st.button("🏛️ Grupo Municipal", use_container_width=True):
                navigate_to("holding")
        with c4:
            if st.button("🧮 Proyector", use_container_width=True):
                navigate_to("simulador")

    elif rol == "Concejal":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🚨 Alertas SAT", use_container_width=True):
                navigate_to("sat")
        with c2:
            if st.button("🎯 Metas del Plan", use_container_width=True):
                navigate_to("metas")
        with c3:
            if st.button("📉 Causas de la Brecha", use_container_width=True):
                navigate_to("brecha")
        with c4:
            if st.button("🔍 Transparencia", use_container_width=True):
                navigate_to("transparencia")

    else:  # Técnico
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("⬡ Centro de Control", use_container_width=True):
                navigate_to("sentinel_hub")
        with c2:
            if st.button("🚨 Alertas SAT", use_container_width=True):
                navigate_to("sat")
        with c3:
            if st.button("⬆️ Panel de Carga", use_container_width=True):
                navigate_to("carga")
        with c4:
            if st.button("📊 Tablero Técnico", use_container_width=True):
                navigate_to("dashboard")

    # ── Metadatos del snapshot ────────────────────────────────────────────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
<div style="font-size:9px;color:rgba(255,255,255,0.2);border-top:1px solid rgba(255,255,255,0.05);
            padding-top:10px">
    Fuente: {source_note} · Corte {fecha_corte} · Pipeline Q1 QUIRA OS Sprint 2
</div>
""", unsafe_allow_html=True)
