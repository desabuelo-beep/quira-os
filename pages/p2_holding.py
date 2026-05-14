"""
QUIRA OS v0.1 — P-02 Holding Municipal (HPT-M)
4 entidades · scores · cascada ICGI-T
Dylus Lab © 2026
"""
import streamlit as st
import plotly.graph_objects as go
from data.loader import load_all
from data.icgi_engine import holding_stats
from components.gauge import render_mini_gauge
from components.kpi_card import section_header, info_box
from utils.session import is_tecnico


def render() -> None:
    data     = load_all()
    holding  = data["holding"]
    stats    = holding_stats(holding)
    show_tech = is_tecnico()

    # ── HEADER ─────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-bottom:20px">
        <h1 style="font-size:1.4rem;font-weight:900;color:#E2E8F0;margin:0">
            Holding Municipal · HPT-M
        </h1>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:4px">
            Gobernanza integrada · 4 entidades municipales · Q1-2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MÉTRICAS RESUMEN ───────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _stat_card("ICGI-T GLOBAL", f"{stats['icgit_global']:.2f}", "#D69E2E", "🟡 Transición Crítica")
    with c2:
        _stat_card("PROMEDIO HPT-M", f"{stats['promedio']:.2f}", stats["color"], f"{stats['emoji']} {stats['avep']}")
    with c3:
        _stat_card("ENTIDADES TOTALES", str(stats["total"]), "#00D4FF", "holding municipal")
    with c4:
        alert_color = "#E53E3E" if stats["en_alerta"] > 0 else "#38A169"
        _stat_card("EN ALERTA", str(stats["en_alerta"]), alert_color,
                   "requieren intervención" if stats["en_alerta"] > 0 else "sin alertas activas")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── RADAR / COMPARATIVA ────────────────────────────────────────────────────
    col_chart, col_list = st.columns([1, 1], gap="medium")

    with col_chart:
        section_header("Comparativa de Scores", "HPT-M · 4 entidades", "📊")
        _render_bar_chart(holding["entidades"])

    with col_list:
        section_header("Cascada de Gobernanza", "ICGI-T → Nodo 1 → Nodo 2", "🔗")
        _render_cascade(holding["entidades"], stats["icgit_global"])

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── TARJETAS ENTIDADES ─────────────────────────────────────────────────────
    section_header("Detalle de Entidades", "", "🏛️")
    cols = st.columns(2, gap="medium")
    for i, entity in enumerate(holding["entidades"]):
        with cols[i % 2]:
            _entity_card(entity, show_tech)

    # ── NOTA TÉCNICA ───────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    info_box(
        "🔗 El score HPT-M es el promedio ponderado de las 4 entidades del holding. "
        "EP Aseo Municipal está en alerta por ISP inferior al umbral COOTAD. "
        "El Cuerpo de Bomberos lidera el ranking con 82.70.",
        level="info",
    )

    if show_tech:
        st.markdown("---")
        st.markdown("""
        <div style="font-size:9px;color:rgba(255,255,255,0.2)">
        🔧 Fuente: SIAP-ICPI H71 · H71b · HPT-M canónico · Corte Q1-2026
        </div>
        """, unsafe_allow_html=True)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def _stat_card(label: str, value: str, color: str, note: str = "") -> None:
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                border-top:2px solid {color};border-radius:12px;padding:14px 16px">
        <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.4);
                    letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px">{label}</div>
        <div style="font-size:1.8rem;font-weight:900;color:{color};line-height:1">{value}</div>
        <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:4px">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def _render_bar_chart(entidades: list[dict]) -> None:
    nombres = [e["nombre"].replace("Cuerpo de ", "").replace(" Municipal", "") for e in entidades]
    scores  = [e["score"] for e in entidades]
    colors  = [e.get("color", "#D69E2E") for e in entidades]

    fig = go.Figure(go.Bar(
        x=nombres,
        y=scores,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{s:.1f}" for s in scores],
        textposition="outside",
        textfont={"size": 12, "color": "#E2E8F0"},
    ))

    # Meta line
    fig.add_hline(
        y=70, line_dash="dash", line_color="#38A169", line_width=1.5,
        annotation_text="Meta 70%", annotation_font={"size": 9, "color": "#38A169"},
        annotation_position="top right",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E2E8F0", "size": 11},
        height=260,
        margin={"t": 30, "b": 10, "l": 10, "r": 10},
        yaxis={"range": [0, 100], "gridcolor": "rgba(255,255,255,0.05)"},
        xaxis={"tickfont": {"size": 9}},
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_cascade(entidades: list[dict], icgit_global: float) -> None:
    """Diagrama de cascada: ICGI-T → GAD (Nodo 1) → adscritas (Nodo 2)."""
    nodo1 = [e for e in entidades if e.get("nodo") == "Nodo 1"]
    nodo2 = [e for e in entidades if e.get("nodo") == "Nodo 2"]

    # ICGI-T global
    st.markdown(f"""
    <div style="text-align:center;margin-bottom:12px">
        <div style="display:inline-block;background:rgba(0,212,255,0.1);
                    border:2px solid rgba(0,212,255,0.3);border-radius:12px;
                    padding:10px 24px">
            <div style="font-size:9px;color:#00D4FF;font-weight:700;letter-spacing:0.06em">
                ICGI-T GLOBAL
            </div>
            <div style="font-size:1.6rem;font-weight:900;color:#00D4FF">{icgit_global:.2f}</div>
        </div>
    </div>
    <div style="text-align:center;color:rgba(255,255,255,0.3);font-size:18px;margin-bottom:8px">↓</div>
    """, unsafe_allow_html=True)

    # Nodo 1
    for e in nodo1:
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:8px">
            <div style="display:inline-block;background:rgba({_rgb(e['color'])},0.1);
                        border:1px solid rgba({_rgb(e['color'])},0.3);border-radius:10px;
                        padding:8px 20px">
                <div style="font-size:9px;color:rgba(255,255,255,0.4);font-weight:700">NODO 1</div>
                <div style="font-size:12px;font-weight:700;color:{e['color']}">{e['nombre']}</div>
                <div style="font-size:1.2rem;font-weight:900;color:{e['color']}">{e['score']:.2f}</div>
            </div>
        </div>
        <div style="text-align:center;color:rgba(255,255,255,0.3);font-size:14px;margin-bottom:8px">↓</div>
        """, unsafe_allow_html=True)

    # Nodo 2 (horizontal)
    n2_cols = st.columns(len(nodo2))
    for col, e in zip(n2_cols, nodo2):
        with col:
            alert_border = "2px solid #E53E3E" if e.get("alerta") else f"1px solid rgba({_rgb(e['color'])},0.3)"
            st.markdown(f"""
            <div style="background:rgba({_rgb(e['color'])},0.08);
                        border:{alert_border};border-radius:10px;
                        padding:10px;text-align:center">
                <div style="font-size:8px;color:rgba(255,255,255,0.4);font-weight:700">NODO 2</div>
                <div style="font-size:10px;font-weight:700;color:{e['color']};margin-top:3px">
                    {e['nombre'].replace(' Municipal','').replace('Cuerpo de ','').replace(' Aseo','⚠ Aseo')}
                </div>
                <div style="font-size:1.1rem;font-weight:900;color:{e['color']}">{e['score']:.1f}</div>
                {'<div style="font-size:8px;color:#FC8181;margin-top:2px">⚠ ALERTA</div>' if e.get("alerta") else ''}
            </div>
            """, unsafe_allow_html=True)


def _entity_card(entity: dict, show_tech: bool) -> None:
    alert_html = ""
    if entity.get("alerta"):
        alert_html = """
        <div style="background:rgba(229,62,62,0.1);border:1px solid rgba(229,62,62,0.3);
                    border-radius:6px;padding:5px 10px;font-size:9px;color:#FC8181;margin-top:8px">
            ⚠ Entidad en alerta — requiere plan de acción inmediato
        </div>
        """

    tech_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.25);margin-top:2px">↳ {entity["id"]} · {entity["nodo"]}</div>' if show_tech else ""

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);
                border:1px solid rgba({_rgb(entity['color'])},0.2);
                border-left:4px solid {entity['color']};
                border-radius:12px;padding:16px 18px;margin-bottom:10px">

        <div style="display:flex;justify-content:space-between;align-items:flex-start">
            <div>
                <div style="font-size:13px;font-weight:800;color:#E2E8F0">{entity['emoji']} {entity['nombre']}</div>
                <div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:3px">{entity['tipo']}</div>
                {tech_html}
            </div>
            <div style="text-align:right">
                <div style="font-size:2rem;font-weight:900;color:{entity['color']};line-height:1">
                    {entity['score']:.2f}
                </div>
                <div style="font-size:9px;color:{entity['color']};opacity:0.8">{entity['avep']}</div>
            </div>
        </div>

        <div style="margin-top:10px;height:5px;background:rgba(255,255,255,0.06);border-radius:3px">
            <div style="width:{min(entity['score'],100):.1f}%;height:100%;
                        background:{entity['color']};border-radius:3px"></div>
        </div>
        {alert_html}
    </div>
    """, unsafe_allow_html=True)


def _rgb(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    if len(h) == 6:
        return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"
    return "255,255,255"
