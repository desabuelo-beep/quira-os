"""
QUIRA OS v0.1 — P-01 Dashboard Ejecutivo
ICGI-T · KPIs · Tendencia · SAT feed · Brechas estructurales
Dylus Lab © 2026
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data.loader import load_all, get_sat_counts
from data.icgi_engine import (
    historico_series, delta_yoy, ritmo_ejecucion,
    proyeccion_cierre, build_scorecard, sat_priority_sort, fmt_delta,
)
from components.gauge import render_gauge
from components.kpi_card import section_header, info_box, progress_bar_card
from components.sat_card import sat_card, sat_feed_header
from utils.session import is_tecnico


def render() -> None:
    data = load_all()
    scorecard = build_scorecard(data)
    show_tech = is_tecnico()

    # ── HEADER ─────────────────────────────────────────────────────────────────
    st.html(f"""
    <div style="display:flex;justify-content:space-between;align-items:flex-start;
                margin-bottom:20px">
        <div>
            <h1 style="font-size:1.4rem;font-weight:900;color:#E2E8F0;margin:0;letter-spacing:-0.02em">
                Tablero Ejecutivo · ICGI-T
            </h1>
            <div style="font-size:0.75rem;color:rgba(255,255,255,0.4);margin-top:4px">
                Corte Q1-2026 · Marzo 2026 · SIAP-ICPI v1.0222
            </div>
        </div>
        <div style="text-align:right">
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.3)">Excel SIAP-ICPI</div>
            <div style="font-size:0.8rem;color:{'#38A169' if data['excel_ok'] else '#E53E3E'}">
                {'✓ Conectado' if data['excel_ok'] else '⚠ Usando datos demo'}
            </div>
        </div>
    </div>
    """)

    # ── FILA 1: Gauge + KPIs ───────────────────────────────────────────────────
    col_gauge, col_kpis = st.columns([1, 2], gap="medium")

    with col_gauge:
        icgit = data["icgit"]
        fig = render_gauge(
            score      = icgit["score"],
            label      = "ICGI-T",
            avep_label = icgit["avep"],
            color      = icgit.get("color", "#D69E2E"),
            meta       = icgit.get("meta_mandato", 70.0),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # AVEP label debajo del gauge
        st.html(f"""
        <div style="text-align:center;margin-top:-10px">
            <span style="display:inline-block;background:rgba(214,158,46,0.12);
                         border:1px solid rgba(214,158,46,0.3);border-radius:20px;
                         padding:5px 18px;font-size:11px;font-weight:700;
                         color:{icgit.get('color','#D69E2E')}">
                {icgit.get('avep_emoji','🟡')} {icgit['avep']}
            </span>
        </div>
        """)

    with col_kpis:
        # Row A: inversión + SAT críticos
        delta_txt, delta_col = fmt_delta(scorecard["delta_yoy"])
        ritmo = scorecard["ritmo"]

        c1, c2 = st.columns(2)
        with c1:
            _kpi(
                "INVERSIÓN EJECUTADA",
                f"${scorecard['ejecutado']:,.0f}",
                f"{scorecard['pct_ejecutado']:.1f}% del presupuesto",
                "🟡" if scorecard['pct_ejecutado'] < 70 else "🟢",
                "#FFB700",
                note=f"Presupuesto total: ${scorecard['presupuesto']:,.0f}",
            )
        with c2:
            _kpi(
                "DELTA vs 2025",
                delta_txt,
                "ICGI-T Q1-2026 vs año anterior",
                "🔴" if scorecard["delta_yoy"] < 0 else "🟢",
                delta_col,
            )

        st.html("<div style='height:10px'></div>")

        c3, c4 = st.columns(2)
        with c3:
            _kpi(
                "RITMO TI NORMALIZADO",
                f"{ritmo['ti_norm']:.1f}%",
                f"{'✓ OK para Q1' if ritmo['ok_ritmo'] else '⚠ Bajo ritmo esperado'}",
                ritmo["semaforo"],
                "#38A169" if ritmo["ok_ritmo"] else "#E53E3E",
                note=f"TI real: {ritmo['ti_raw']:.1f}% · Meta mandato: 70%",
            )
        with c4:
            n_crit = scorecard["sat_criticos"]
            _kpi(
                "SAT CRÍTICAS ACTIVAS",
                str(n_crit),
                f"Impacto total: {scorecard['sat_impact']:.1f} pts ICGI-T",
                "🔴" if n_crit > 0 else "🟢",
                "#E53E3E" if n_crit > 0 else "#38A169",
                note=f"{scorecard['sat_alertas']} en nivel ALERTA",
            )

    # ── FILA 2: Tendencia + Proyección ─────────────────────────────────────────
    st.html("<div style='height:12px'></div>")
    col_trend, col_proj = st.columns([2, 1], gap="medium")

    with col_trend:
        section_header("Tendencia Histórica ICGI-T", "2023 → 2026", "📈")
        _render_trend_chart(data["icgit"])

    with col_proj:
        proj = scorecard["proyeccion"]
        section_header("Proyección Cierre 2026", "", "🎯")
        st.html(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px;padding:18px;text-align:center">
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.4);margin-bottom:8px">
                ESTIMACIÓN CIERRE 2026
            </div>
            <div style="font-size:2.8rem;font-weight:900;color:{proj['color']};line-height:1">
                {proj['proyeccion']:.2f}
            </div>
            <div style="font-size:11px;color:{proj['color']};margin-top:6px">
                {proj['emoji']} {proj['avep']}
            </div>
            <div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:12px;
                        border-top:1px solid rgba(255,255,255,0.06);padding-top:10px">
                Meta Gestión por Mandato: 70.0<br>
                Brecha: <span style="color:{'#E53E3E' if proj['delta']<0 else '#38A169'};font-weight:700">
                    {proj['delta']:+.2f} pts
                </span>
            </div>
        </div>
        """)

        if not proj["on_track"]:
            st.html("<div style='height:10px'></div>")
            info_box(
                "⚠ Al ritmo actual, el cierre 2026 no alcanzaría la meta de Gestión por Mandato. "
                "Se requiere acelerar ejecución en Q2-Q3.",
                level="warning",
            )

    # ── FILA 3: Brechas Estructurales + SAT feed ───────────────────────────────
    st.html("<div style='height:12px'></div>")
    col_brechas, col_sat = st.columns([1, 1], gap="medium")

    with col_brechas:
        section_header("Brechas Estructurales", "Índices críticos que arrastran el ICGI-T", "⚠️")
        indices = data["indices"]

        progress_bar_card(
            label     = "Salud Presupuestaria",
            value     = indices["ISP"]["valor"],
            color     = indices["ISP"]["color"],
            avep      = indices["ISP"]["avep"],
            emoji     = indices["ISP"]["emoji"],
            note      = indices["ISP"]["nota"],
            show_tech = show_tech,
            tech_label= "ISP · H19",
        )
        progress_bar_card(
            label     = "Presupuesto Género",
            value     = indices["PSG"]["valor"],
            color     = indices["PSG"]["color"],
            avep      = indices["PSG"]["avep"],
            emoji     = indices["PSG"]["emoji"],
            note      = indices["PSG"]["nota"],
            show_tech = show_tech,
            tech_label= "PSG · LOTAIP · ONU Mujeres",
        )
        progress_bar_card(
            label     = "Opacidad Crítica",
            value     = indices["IOC"]["valor"],
            color     = indices["IOC"]["color"],
            avep      = indices["IOC"]["avep"],
            emoji     = indices["IOC"]["emoji"],
            note      = "Índice invertido — mayor es peor · " + indices["IOC"]["nota"],
            show_tech = show_tech,
            tech_label= "IOC · LOTAIP",
        )
        # IGP — en construcción
        progress_bar_card(
            label     = "Gobernanza Participativa",
            value     = None,
            color     = "#7C5CFC",
            avep      = "En calibración",
            emoji     = "⏳",
            note      = "Componente ICGI-T en validación · activo Q2-2026",
            dashed    = True,
            show_tech = show_tech,
            tech_label= "IGP · CPCCS / LOPC",
        )

    with col_sat:
        sat_counts = get_sat_counts(data)
        sat_feed_header(sat_counts["criticos"], sat_counts["alertas"])
        sats = sat_priority_sort(data["sat"])
        for s in sats:
            sat_card(
                sat_id      = s["id"],
                nombre      = s["nombre"],
                estado      = s["estado"],
                nivel       = s["nivel"],
                color       = s["color"],
                emoji       = s["emoji"],
                descripcion = s["descripcion"],
                impacto     = s["impacto"],
                accion      = s["accion"],
                compact     = True,
            )

    # ── FOOTER TÉCNICO ─────────────────────────────────────────────────────────
    if show_tech:
        st.markdown("---")
        st.html("""
        <div style="font-size:9px;color:rgba(255,255,255,0.2);line-height:1.6">
        🔧 MODO TÉCNICO · Fuente: SIAP-ICPI H12 · H15 · H19 · H20b · H28 ·
        Corte Q1-2026 · Verificado Dylus Lab
        </div>
        """)


# ── HELPERS ────────────────────────────────────────────────────────────────────
def _kpi(label: str, value: str, subtitle: str, emoji: str, color: str, note: str = "") -> None:
    note_html = f'<div style="font-size:9px;color:rgba(255,255,255,0.3);margin-top:5px">{note}</div>' if note else ""
    st.html(f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                border-top:2px solid {color};border-radius:12px;padding:14px 16px">
        <div style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.45);
                    letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px">
            {label}
        </div>
        <div style="font-size:1.6rem;font-weight:900;color:#FFFFFF;line-height:1">{value}</div>
        <div style="font-size:10px;color:rgba(255,255,255,0.5);margin-top:4px">
            {emoji} {subtitle}
        </div>
        {note_html}
    </div>
    """)


def _render_trend_chart(icgit: dict) -> None:
    labels, values = historico_series(icgit)

    # Colores: reales vs proyección
    colors = ["#00D4FF", "#00D4FF", "#00D4FF", "#FFB700", "#7C5CFC"]
    line_dash = ["solid", "solid", "solid", "solid", "dot"]

    fig = go.Figure()

    # Área de relleno debajo de la línea
    fig.add_trace(go.Scatter(
        x=labels, y=values,
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.06)",
        line={"color": "rgba(0,0,0,0)"},
        showlegend=False,
        hoverinfo="skip",
    ))

    # Línea principal (reales)
    fig.add_trace(go.Scatter(
        x=labels[:4], y=values[:4],
        mode="lines+markers",
        line={"color": "#00D4FF", "width": 2.5},
        marker={"size": 7, "color": colors[:4], "line": {"width": 2, "color": "#0A1628"}},
        name="ICGI-T Real",
        hovertemplate="%{x}: %{y:.2f}<extra></extra>",
    ))

    # Proyección (punteada)
    fig.add_trace(go.Scatter(
        x=[labels[3], labels[4]], y=[values[3], values[4]],
        mode="lines+markers",
        line={"color": "#7C5CFC", "width": 2, "dash": "dot"},
        marker={"size": 7, "color": "#7C5CFC", "symbol": "diamond"},
        name="Proyección 2026",
        hovertemplate="%{x}: %{y:.2f}<extra></extra>",
    ))

    # Línea de meta
    fig.add_hline(
        y=70, line_dash="dash", line_color="#38A169", line_width=1.5,
        annotation_text="Meta Mandato 70%",
        annotation_font={"size": 9, "color": "#38A169"},
        annotation_position="bottom right",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E2E8F0", "family": "Inter, sans-serif", "size": 11},
        height=200,
        margin={"t": 10, "b": 10, "l": 10, "r": 10},
        xaxis={
            "gridcolor": "rgba(255,255,255,0.05)",
            "tickfont": {"size": 10},
        },
        yaxis={
            "gridcolor": "rgba(255,255,255,0.05)",
            "range": [40, 85],
            "tickfont": {"size": 10},
        },
        legend={
            "font": {"size": 9},
            "orientation": "h",
            "y": -0.25,
        },
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
