"""
QUIRA OS v0.1 — P-04 GeoTwin · Análisis Territorial
7 parroquias · IGP · Paradoja democrática · Equidad territorial
Dylus Lab © 2026
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data.loader import load_all, get_zonas_sin_voz
from data.icgi_engine import geotwin_stats
from components.kpi_card import section_header, info_box
from utils.session import is_tecnico


# Colores de estado
_ESTADO_COLOR = {
    "EMERGENCIA": "#E53E3E",
    "PRIORIDAD":  "#7C5CFC",
    "ALERTA":     "#E67E22",
    "NORMAL":     "#D69E2E",
    "OK":         "#38A169",
}


def render() -> None:
    data       = load_all()
    parroquias = data["parroquias"]
    stats      = geotwin_stats(parroquias)
    sin_voz    = get_zonas_sin_voz(data)
    show_tech  = is_tecnico()

    # ── HEADER ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:20px">
        <h1 style="font-size:1.4rem;font-weight:900;color:#E2E8F0;margin:0">
            GeoTwin · Análisis Territorial
        </h1>
        <div style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:4px">
            7 parroquias · SIAP-ICPI + PDOT_KB · Gobernanza Participativa · Q1-2026
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ───────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _stat("INVERSIÓN TOTAL", f"${stats['total_inversion']:,.0f}", "#00D4FF")
    with c2:
        _stat("BRECHA TERRITORIAL",
              f"${stats['brecha_territorial']:,.0f}/hab",
              "#E53E3E",
              note=f"Cabecera ${stats['per_capita_max']}/hab · Peor ${stats['per_capita_min']}/hab")
    with c3:
        _stat("PARROQUIAS SIN VOZ",
              str(stats["parroquias_sin_voz"]),
              "#E53E3E" if stats["parroquias_sin_voz"] > 0 else "#38A169",
              note="IGP · participación = 0")
    with c4:
        _stat("EN EMERGENCIA", str(stats["parroquias_emergencia"]), "#E53E3E",
              note=f"de {stats['n_total']} parroquias")

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── GRÁFICOS ───────────────────────────────────────────────────────────────
    col_bar, col_bubble = st.columns([1, 1], gap="medium")

    with col_bar:
        section_header("Inversión Per Cápita", "$/habitante · Q1-2026", "💰")
        _render_per_capita_chart(parroquias)

    with col_bubble:
        section_header("Brecha NBI vs Inversión", "Necesidad vs. respuesta institucional", "📍")
        _render_bubble(parroquias)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── TABLA PARROQUIAS ───────────────────────────────────────────────────────
    section_header("Detalle por Parroquia", "TPS · NBI · Agua · Inversión · Participación IGP", "📋")
    _render_table(parroquias, show_tech)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── IGP GOBERNANZA PARTICIPATIVA ───────────────────────────────────────────
    section_header("Gobernanza Participativa · IGP", "Obligación institucional CPCCS / LOPC", "🗳️")

    col_igp, col_paradox = st.columns([1, 1], gap="medium")

    with col_igp:
        igp = data["indices"].get("IGP", {})
        st.markdown(f"""
        <div style="background:rgba(124,92,252,0.06);border:1px solid rgba(124,92,252,0.2);
                    border-radius:12px;padding:16px">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                    <div style="font-size:12px;font-weight:700;color:#E2E8F0">IGP · {igp.get('nombre','Gobernanza Participativa')}</div>
                    <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:2px">{igp.get('estado','Referencia 2025')}</div>
                    {'<div style="font-size:9px;color:rgba(255,255,255,0.25);margin-top:1px">↳ IGP · H20b · CPCCS</div>' if show_tech else ''}
                </div>
                <div style="font-size:1.8rem;font-weight:900;color:#7C5CFC">{igp.get('valor',27.98):.2f}</div>
            </div>
            <div style="height:4px;background:rgba(255,255,255,0.07);border-radius:2px;margin:10px 0">
                <div style="width:{igp.get('valor',27.98):.1f}%;height:100%;background:#7C5CFC;border-radius:2px"></div>
            </div>
            <div style="font-size:10px;color:rgba(255,255,255,0.5);line-height:1.5">{igp.get('nota','')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # Tabla participación resumida
        st.markdown("""
        <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.5);
                    letter-spacing:0.06em;margin-bottom:8px">PARTICIPACIÓN 2025 POR PARROQUIA</div>
        """, unsafe_allow_html=True)

        for p in parroquias:
            part  = p.get("participacion", {})
            color = "#E53E3E" if part.get("estado") == "Sin voz" else \
                    "#E67E22" if part.get("estado") == "Bajo" else \
                    "#D69E2E" if part.get("estado") == "Parcial" else "#38A169"
            mesas = part.get("mesas", 0)
            pres  = part.get("presupuesto", 0)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04)">
                <div style="font-size:10px;color:rgba(255,255,255,0.7)">{p['nombre']}</div>
                <div style="display:flex;gap:8px;align-items:center">
                    <span style="font-size:9px;color:rgba(255,255,255,0.4)">{mesas} mesas · ${pres:,.0f}</span>
                    <span style="font-size:9px;font-weight:700;color:{color}">{part.get('estado','—')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_paradox:
        # Paradoja democrática
        st.markdown(f"""
        <div style="background:rgba(229,62,62,0.06);border:2px solid rgba(229,62,62,0.25);
                    border-radius:12px;padding:18px;margin-bottom:12px">
            <div style="font-size:12px;font-weight:800;color:#FC8181;margin-bottom:10px">
                ⚠ Paradoja Democrática Detectada
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.7);line-height:1.6;margin-bottom:12px">
                Las parroquias con mayor necesidad (NBI alto, TPS crítico) son las que
                <strong style="color:#FC8181">menos participación tienen</strong> en decisiones
                de presupuesto y planificación territorial.
            </div>
            <div style="background:rgba(255,255,255,0.04);border-radius:8px;padding:12px">
                <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.4);
                            letter-spacing:0.06em;margin-bottom:8px">ZONAS SIN VOZ PARTICIPATIVA</div>
        """, unsafe_allow_html=True)

        for p in sin_voz:
            st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                            margin-bottom:6px;padding:8px 10px;
                            background:rgba(229,62,62,0.08);border-radius:6px;
                            border-left:3px solid #E53E3E">
                    <div>
                        <div style="font-size:11px;font-weight:700;color:#FC8181">
                            🚨 {p['nombre']}
                        </div>
                        <div style="font-size:9px;color:rgba(255,255,255,0.4);margin-top:2px">
                            NBI {p['nbi']}% · TPS {p['tps']:.0f}% · ${p['per_capita']}/hab
                        </div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:9px;color:#FC8181;font-weight:700">0 mesas</div>
                        <div style="font-size:9px;color:rgba(255,255,255,0.3)">$0 part.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

        info_box(
            "🎯 Acción SAT-V: Convocar asambleas en Isabel Muentes y Aníbal San Andrés. "
            "El silencio participativo amplifica la brecha territorial.",
            level="danger",
        )

    if show_tech:
        st.markdown("---")
        st.markdown("""
        <div style="font-size:9px;color:rgba(255,255,255,0.2)">
        🔧 GeoTwin · Fuente: SIAP-ICPI + PDOT_KB · H20b (IGP) · H04 (TPS) ·
        CPCCS V=0 en RDC 2026 · 50 UT activas vs meta 75
        </div>
        """, unsafe_allow_html=True)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def _stat(label: str, value: str, color: str, note: str = "") -> None:
    note_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:4px">{note}</div>' if note else ""
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                border-top:2px solid {color};border-radius:12px;padding:14px 16px">
        <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.4);
                    letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px">{label}</div>
        <div style="font-size:1.5rem;font-weight:900;color:{color};line-height:1">{value}</div>
        {note_html}
    </div>
    """, unsafe_allow_html=True)


def _render_per_capita_chart(parroquias: list[dict]) -> None:
    nombres = [p["nombre"].replace(" (cabecera)", "") for p in parroquias]
    vals    = [p["per_capita"] for p in parroquias]
    colors  = [_ESTADO_COLOR.get(p["estado"], "#D69E2E") for p in parroquias]

    fig = go.Figure(go.Bar(
        x=vals,
        y=nombres,
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"${v}/hab" for v in vals],
        textposition="outside",
        textfont={"size": 9, "color": "#E2E8F0"},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E2E8F0", "size": 10},
        height=270,
        margin={"t": 10, "b": 10, "l": 10, "r": 60},
        xaxis={"gridcolor": "rgba(255,255,255,0.05)", "range": [0, 140]},
        yaxis={"tickfont": {"size": 9}},
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_bubble(parroquias: list[dict]) -> None:
    df = pd.DataFrame([{
        "Parroquia": p["nombre"].replace(" (cabecera)", ""),
        "NBI (%)":   p["nbi"],
        "Inversión ($)": p["inversion"],
        "Habitantes": p["habitantes"],
        "Estado": p["estado"],
        "Color": _ESTADO_COLOR.get(p["estado"], "#D69E2E"),
    } for p in parroquias])

    fig = go.Figure()
    for _, row in df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["NBI (%)"]],
            y=[row["Inversión ($)"]],
            mode="markers+text",
            marker={
                "size": max(row["Habitantes"] / 500, 8),
                "color": row["Color"],
                "opacity": 0.8,
                "line": {"width": 1, "color": "rgba(255,255,255,0.3)"},
            },
            text=[row["Parroquia"]],
            textposition="top center",
            textfont={"size": 8, "color": "rgba(255,255,255,0.6)"},
            name=row["Parroquia"],
            hovertemplate=(
                f"<b>{row['Parroquia']}</b><br>"
                f"NBI: {row['NBI (%)']:.1f}%<br>"
                f"Inversión: ${row['Inversión ($)']:,.0f}<br>"
                f"Habitantes: {row['Habitantes']:,}<extra></extra>"
            ),
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E2E8F0", "size": 10},
        height=270,
        margin={"t": 10, "b": 10, "l": 10, "r": 10},
        xaxis={
            "title": "NBI (%)", "gridcolor": "rgba(255,255,255,0.05)",
            "titlefont": {"size": 9},
        },
        yaxis={
            "title": "Inversión ($)", "gridcolor": "rgba(255,255,255,0.05)",
            "titlefont": {"size": 9},
        },
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_table(parroquias: list[dict], show_tech: bool) -> None:
    rows_html = ""
    for p in parroquias:
        part   = p.get("participacion", {})
        estado_color = _ESTADO_COLOR.get(p["estado"], "#D69E2E")
        part_color   = {
            "Sin voz": "#E53E3E",
            "Bajo":    "#E67E22",
            "Parcial": "#D69E2E",
            "Activo":  "#38A169",
        }.get(part.get("estado", ""), "#D69E2E")

        rows_html += f"""
        <tr style="border-bottom:1px solid rgba(255,255,255,0.05)">
            <td style="padding:8px 10px;font-size:11px;color:rgba(255,255,255,0.8);font-weight:600">
                {p['emoji']} {p['nombre']}
            </td>
            <td style="padding:8px 10px;text-align:center;font-size:11px">
                <span style="color:{estado_color};font-weight:700">{p['estado']}</span>
            </td>
            <td style="padding:8px 10px;text-align:right;font-size:11px;color:rgba(255,255,255,0.7)">
                {p['tps']:.1f}%
            </td>
            <td style="padding:8px 10px;text-align:right;font-size:11px;color:rgba(255,255,255,0.7)">
                {p['nbi']:.1f}%
            </td>
            <td style="padding:8px 10px;text-align:right;font-size:11px;color:rgba(255,255,255,0.7)">
                {p['agua']:.1f}%
            </td>
            <td style="padding:8px 10px;text-align:right;font-size:11px;color:#00D4FF;font-weight:700">
                ${p['per_capita']}/hab
            </td>
            <td style="padding:8px 10px;text-align:center;font-size:10px">
                <span style="color:{part_color};font-weight:700">{part.get('estado','—')}</span><br>
                <span style="color:rgba(255,255,255,0.3);font-size:9px">
                    {part.get('mesas',0)} mesas · ${part.get('presupuesto',0):,.0f}
                </span>
            </td>
        </tr>
        """

    st.markdown(f"""
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-family:Inter,sans-serif">
        <thead>
            <tr style="border-bottom:2px solid rgba(255,255,255,0.12)">
                <th style="padding:8px 10px;text-align:left;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    PARROQUIA
                </th>
                <th style="padding:8px 10px;text-align:center;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    ESTADO
                </th>
                <th style="padding:8px 10px;text-align:right;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    TPS
                </th>
                <th style="padding:8px 10px;text-align:right;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    NBI
                </th>
                <th style="padding:8px 10px;text-align:right;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    AGUA
                </th>
                <th style="padding:8px 10px;text-align:right;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    INV/HAB
                </th>
                <th style="padding:8px 10px;text-align:center;font-size:9px;font-weight:700;
                           color:rgba(255,255,255,0.4);letter-spacing:0.06em;text-transform:uppercase">
                    IGP · PARTICIPACIÓN
                </th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)
