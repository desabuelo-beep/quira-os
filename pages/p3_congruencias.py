"""
QUIRA OS v0.1 — P-03 Congruencias + IFE-A/E + 10 Índices
Cuatro congruencias · fidelidad de mandato · trazabilidad
Dylus Lab © 2026
"""
import streamlit as st
import plotly.graph_objects as go
from data.loader import load_all
from components.kpi_card import section_header, info_box, progress_bar_card
from components.avep_badge import avep_badge_html, render_index_card
from utils.session import is_tecnico


_CONGRUENCIA_META = {
    "politica":    {
        "pregunta":  "¿Estamos gobernando lo que prometimos?",
        "fuente":    "IFE-A · 48/66 promesas CNE vinculadas al PDOT",
        "icon":      "🗳️",
    },
    "operativa":   {
        "pregunta":  "¿Lo planificado se está ejecutando?",
        "fuente":    "POA→PAC→SERCOP→eSIGEF · 4 cortes detectados",
        "icon":      "⚙️",
    },
    "territorial": {
        "pregunta":  "¿La inversión llega donde más se necesita?",
        "fuente":    "GeoTwin · 7 parroquias · PDOT_KB",
        "icon":      "🗺️",
    },
    "ecosistemica":{
        "pregunta":  "¿Todo el holding municipal está alineado?",
        "fuente":    "HPT-M · 4 entidades · Bomberos/Patronato/EP Aseo",
        "icon":      "🔗",
    },
}


def render() -> None:
    data      = load_all()
    show_tech = is_tecnico()

    # ── HEADER ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:20px">
        <h1 style="font-size:1.4rem;font-weight:900;color:#E2E8F0;margin:0">
            Congruencias de Gobernanza
        </h1>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:4px">
            Promesa → Planificación → Ejecución → Territorio · Q1-2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 4 CONGRUENCIAS ─────────────────────────────────────────────────────────
    section_header("Las Cuatro Congruencias", "Dimensiones de coherencia institucional", "🎯")
    cols = st.columns(2, gap="medium")
    congruencias = data["congruencias"]

    for i, (key, c) in enumerate(congruencias.items()):
        meta = _CONGRUENCIA_META.get(key, {})
        with cols[i % 2]:
            _congruencia_card(c, meta, show_tech)

    # ── RADAR ──────────────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    col_radar, col_ife = st.columns([1, 1], gap="medium")

    with col_radar:
        section_header("Radar de Congruencias", "", "📡")
        _render_radar(congruencias)

    with col_ife:
        section_header("Fidelidad de Mandato · IFE", "IFE-A auditado + IFE-E en construcción", "🗳️")
        _render_ife(data["indices"], show_tech)

    # ── 10 ÍNDICES COMPLEMENTARIOS ─────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    section_header("Índices Complementarios ICGI-T", "10 dimensiones de gobernanza · Q1-2026", "📋")

    indices = data["indices"]
    c1, c2 = st.columns(2, gap="medium")
    for i, (key, idx) in enumerate(indices.items()):
        with (c1 if i % 2 == 0 else c2):
            render_index_card(
                key       = key,
                nombre    = idx["nombre"],
                valor     = idx["valor"],
                avep      = idx["avep"],
                emoji     = idx["emoji"],
                color     = idx["color"],
                estado    = idx["estado"],
                nota      = idx["nota"],
                show_tech = show_tech,
            )

    if show_tech:
        st.markdown("---")
        st.markdown("""
        <div style="font-size:9px;color:rgba(255,255,255,0.2)">
        🔧 Fuente: SIAP-ICPI H16 (IFE-A) + IFE-E · H15 · H19 · H20b · H28 ·
        Fidelidad de Mandato · Corte Q1-2026
        </div>
        """, unsafe_allow_html=True)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def _congruencia_card(c: dict, meta: dict, show_tech: bool) -> None:
    score  = c["score"]
    color  = c.get("color_avep", c.get("color", "#D69E2E"))
    pct    = min(score, 100)
    icon   = meta.get("icon", "")
    fuente = meta.get("fuente", c.get("fuente", ""))
    pregunta = meta.get("pregunta", c.get("pregunta", ""))

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.07);
                border-top:3px solid {color};
                border-radius:12px;padding:16px 18px;margin-bottom:12px">

        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
            <div>
                <div style="font-size:13px;font-weight:800;color:#E2E8F0">
                    {icon} {c['nombre']}
                </div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:3px;
                            font-style:italic">{pregunta}</div>
            </div>
            <div style="text-align:right">
                <div style="font-size:1.8rem;font-weight:900;color:{color};line-height:1">
                    {score:.2f}
                </div>
                <div style="font-size:9px;color:{color};opacity:0.8">{c['emoji']} {c['avep']}</div>
            </div>
        </div>

        <div style="height:5px;background:rgba(255,255,255,0.07);border-radius:3px;margin-bottom:8px">
            <div style="width:{pct:.1f}%;height:100%;background:{color};border-radius:3px"></div>
        </div>

        <div style="font-size:9px;color:rgba(255,255,255,0.35)">{fuente}</div>
    </div>
    """, unsafe_allow_html=True)


def _render_radar(congruencias: dict) -> None:
    labels = [c["nombre"] for c in congruencias.values()]
    values = [c["score"] for c in congruencias.values()]
    # Cerrar el polígono
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill="toself",
        fillcolor="rgba(0,212,255,0.1)",
        line={"color": "#00D4FF", "width": 2},
        marker={"size": 6, "color": "#00D4FF"},
        hovertemplate="%{theta}: %{r:.2f}<extra></extra>",
    ))

    # Meta 70
    fig.add_trace(go.Scatterpolar(
        r=[70, 70, 70, 70, 70],
        theta=labels_closed,
        mode="lines",
        line={"color": "rgba(56,161,105,0.5)", "width": 1.5, "dash": "dash"},
        showlegend=True,
        name="Meta 70%",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar={
            "bgcolor": "rgba(0,0,0,0)",
            "radialaxis": {
                "range": [0, 100],
                "tickfont": {"size": 9, "color": "rgba(255,255,255,0.35)"},
                "gridcolor": "rgba(255,255,255,0.07)",
                "linecolor": "rgba(255,255,255,0.1)",
            },
            "angularaxis": {
                "tickfont": {"size": 9, "color": "rgba(255,255,255,0.6)"},
                "linecolor": "rgba(255,255,255,0.1)",
            },
        },
        font={"color": "#E2E8F0"},
        height=260,
        margin={"t": 20, "b": 20, "l": 20, "r": 20},
        legend={"font": {"size": 9}},
        showlegend=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_ife(indices: dict, show_tech: bool) -> None:
    # IFE-A
    ife_a = indices.get("IFE-A", {})
    st.markdown(f"""
    <div style="background:rgba(56,161,105,0.06);border:1px solid rgba(56,161,105,0.2);
                border-left:4px solid #38A169;border-radius:10px;padding:14px 16px;margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <div style="font-size:12px;font-weight:700;color:#E2E8F0">
                    🟢 IFE-A · Fidelidad Electoral
                </div>
                <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:2px">
                    {ife_a.get('estado', 'REAL auditado')}
                </div>
                {'<div style="font-size:9px;color:rgba(255,255,255,0.25);margin-top:1px">↳ IFE-A · H16</div>' if show_tech else ''}
            </div>
            <div style="font-size:1.6rem;font-weight:900;color:#38A169">{ife_a.get('valor', 72.73):.2f}</div>
        </div>
        <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:8px;line-height:1.5">
            {ife_a.get('nota', '48 de 66 promesas vinculadas al PDOT')}
        </div>
        <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:2px;margin-top:8px">
            <div style="width:{ife_a.get('valor',72.73):.1f}%;height:100%;background:#38A169;border-radius:2px"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # IFE-E (en construcción)
    ife_e = indices.get("IFE-E", {})
    st.markdown(f"""
    <div style="background:rgba(124,92,252,0.06);border:1px solid rgba(124,92,252,0.2);
                border-left:4px solid #7C5CFC;border-radius:10px;padding:14px 16px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <div style="font-size:12px;font-weight:700;color:#E2E8F0">
                    ⏳ IFE-E · Fidelidad de Ejecución
                </div>
                <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:2px">
                    En construcción · Activo {ife_e.get('estado', 'Q2-2026')}
                </div>
                {'<div style="font-size:9px;color:rgba(255,255,255,0.25);margin-top:1px">↳ IFE-E · v1.2</div>' if show_tech else ''}
            </div>
            <div style="font-size:1rem;font-weight:700;color:#7C5CFC">—</div>
        </div>
        <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:8px;line-height:1.5">
            {ife_e.get('nota', 'Mide trazabilidad POA→PAC→eSIGEF')}
        </div>
        <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:2px;margin-top:8px;
                    background:repeating-linear-gradient(45deg,rgba(124,92,252,.18),rgba(124,92,252,.18) 3px,
                    transparent 3px,transparent 7px);border:1px dashed rgba(124,92,252,.3)"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    info_box(
        "📋 IFE-A mide la coherencia entre promesas electorales (CNE) y el PDOT. "
        "IFE-E medirá la trazabilidad de ejecución POA→PAC→SERCOP→eSIGEF — disponible Q2-2026.",
        level="info",
    )
