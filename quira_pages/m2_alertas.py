"""
QUIRA OS — Módulo M2: Alertas
Consolida SAT activas y Evolución Longitudinal (RC-M).

Sprint 3: Tab "📈 Evolución Longitudinal" conectado al Longitudinal Engine.
Regla: nuevas vistas de alertas = tabs aquí. Nunca un nuevo item de sidebar.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st


# ── Constantes de estilo ───────────────────────────────────────────────────────
_RIESGO_COLOR = {
    "BAJO":    "#00E096",
    "MEDIO":   "#FFB700",
    "ALTO":    "#FF4D6D",
    "CRÍTICO": "#9B1C1C",
    "—":       "#6B7280",
}

_SAT_IV_COLOR = {
    "ACTIVA":    "#FF4D6D",
    "mitigada":  "#00E096",
    "SIN DATOS": "#6B7280",
}

_TREND_EMOJI = {
    "MEJORA":             "📈",
    "DETERIORO":          "📉",
    "ESTABLE":            "➡️",
    "INSUFICIENTE_DATOS": "❓",
}


def render() -> None:
    tab_sat, tab_long = st.tabs([
        "🚨 Señales SAT Activas",
        "📈 Evolución Longitudinal",
    ])

    with tab_sat:
        try:
            from quira_pages.p9_sat import render as _r
            _r()
        except Exception as e:
            st.error(f"SAT no disponible: {e}")

    with tab_long:
        _render_longitudinal()


# ══════════════════════════════════════════════════════════════════════════════
# Tab: Evolución Longitudinal (RC-M)
# ══════════════════════════════════════════════════════════════════════════════

def _render_longitudinal() -> None:
    """Renderiza la tabla RC-M canónica y el gráfico de tendencia ICPI."""
    st.markdown("### 📈 Evolución Longitudinal — Tabla RC-M")
    st.caption(
        "Trayectoria institucional: ICPI · Ejecución Presupuestaria (D3) · SAT-IV · Riesgo ponderado"
    )

    # ── Carga de datos ─────────────────────────────────────────────────────────
    try:
        from app.services.longitudinal_engine import get_longitudinal_summary
        summary = get_longitudinal_summary("130801", prefer_local=True)
    except Exception as exc:
        st.error(f"Error al cargar el motor longitudinal: {exc}")
        return

    if summary.get("error"):
        st.warning(f"⚠️ {summary['error']}")
        _render_no_data_hint()
        return

    # ── Indicadores de tendencia ───────────────────────────────────────────────
    n = summary["n_periodos"]
    icpi_trend = summary["icpi_trend"]
    last_period = summary["last_period"]
    last_riesgo = summary["last_riesgo"]
    last_icpi = summary.get("last_icpi_pct")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Períodos registrados", str(n), help="Snapshots únicos en el historial")
    with col2:
        icpi_str = f"{last_icpi:.1f}%" if last_icpi is not None else "—"
        st.metric("ICPI último período", icpi_str, help=f"Período: {last_period}")
    with col3:
        trend_icon = _TREND_EMOJI.get(icpi_trend, "❓")
        st.metric("Tendencia ICPI", f"{trend_icon} {icpi_trend}")
    with col4:
        risk_color = _RIESGO_COLOR.get(last_riesgo, "#6B7280")
        st.markdown(
            f"<div style='text-align:center'>"
            f"<div style='font-size:0.75rem;color:#9CA3AF;margin-bottom:4px'>Riesgo SAT actual</div>"
            f"<div style='font-size:1.25rem;font-weight:700;color:{risk_color}'>{last_riesgo}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Tabla RC-M ─────────────────────────────────────────────────────────────
    rcm = summary.get("rcm_table", [])
    if not rcm:
        _render_no_data_hint()
        return

    st.markdown("#### Tabla RC-M Canónica")
    _render_rcm_table(rcm)

    st.divider()

    # ── Gráfico de tendencia ICPI ──────────────────────────────────────────────
    icpi_series = summary.get("icpi_series", [])
    if len(icpi_series) >= 2:
        _render_icpi_chart(icpi_series)
    else:
        st.info(
            "📊 El gráfico de tendencia se activará a partir de 2 períodos registrados. "
            "Ejecuta el pipeline la próxima semana para ver la trayectoria.",
            icon="ℹ️",
        )

    # ── Nota doctrinal ─────────────────────────────────────────────────────────
    _render_doctrinal_note()


def _render_rcm_table(rcm: list[dict]) -> None:
    """Renderiza la tabla RC-M con colores semánticos."""
    cols = st.columns([2, 2, 2, 2, 2])
    headers = ["Período", "ICPI (%)", "D3 Ti (%)", "SAT-IV", "Riesgo"]
    for col, h in zip(cols, headers):
        col.markdown(f"**{h}**")

    st.markdown(
        "<hr style='margin:4px 0;border-color:#1F2937'>", unsafe_allow_html=True
    )

    for row in rcm:
        is_last = row == rcm[-1]
        weight = "700" if is_last else "400"
        bg = "#0F172A" if is_last else "transparent"

        icpi_val = row.get("icpi_pct")
        icpi_str = f"{icpi_val:.1f}%" if icpi_val is not None else "—"
        icpi_color = (
            "#FF4D6D" if (icpi_val is not None and icpi_val < 50)
            else "#FFB700" if (icpi_val is not None and icpi_val < 65)
            else "#00E096"
        )

        d3_val = row.get("d3_ti_pct")
        d3_str = f"{d3_val:.1f}%" if d3_val is not None else "—"
        d3_color = (
            "#FF4D6D" if (d3_val is not None and d3_val < 40)
            else "#FFB700" if (d3_val is not None and d3_val < 60)
            else "#00E096"
        )

        sat_iv = row.get("sat_iv", "SIN DATOS")
        sat_iv_color = _SAT_IV_COLOR.get(sat_iv, "#6B7280")

        riesgo = row.get("riesgo", "—")
        riesgo_color = _RIESGO_COLOR.get(riesgo, "#6B7280")

        c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 2])
        cell = f"font-weight:{weight};background:{bg};padding:4px 8px;border-radius:4px"

        c1.markdown(
            f"<div style='{cell}'>{row.get('periodo', '—')}</div>",
            unsafe_allow_html=True,
        )
        c2.markdown(
            f"<div style='{cell};color:{icpi_color}'>{icpi_str}</div>",
            unsafe_allow_html=True,
        )
        c3.markdown(
            f"<div style='{cell};color:{d3_color}'>{d3_str}</div>",
            unsafe_allow_html=True,
        )
        c4.markdown(
            f"<div style='{cell};color:{sat_iv_color}'>{sat_iv}</div>",
            unsafe_allow_html=True,
        )
        c5.markdown(
            f"<div style='{cell};color:{riesgo_color}'>{riesgo}</div>",
            unsafe_allow_html=True,
        )

    if rcm:
        last_fecha = rcm[-1].get("fecha_corte", "")
        st.caption(f"↑ Período más reciente: {last_fecha} · En negrita")


def _render_icpi_chart(icpi_series: list[tuple]) -> None:
    """Gráfico de línea de tendencia ICPI usando Plotly."""
    try:
        import plotly.graph_objects as go

        labels = [s[0] for s in icpi_series]
        values = [s[1] for s in icpi_series]

        fig = go.Figure()

        # Zona de meta (>= 65%)
        fig.add_hrect(
            y0=65,
            y1=100,
            fillcolor="rgba(0, 224, 150, 0.06)",
            line_width=0,
            annotation_text="Meta PDOT ≥ 65%",
            annotation_position="top right",
            annotation_font_color="#00E096",
        )
        # Zona crítica (< 50%)
        fig.add_hrect(
            y0=0,
            y1=50,
            fillcolor="rgba(255, 77, 109, 0.06)",
            line_width=0,
        )
        # Línea de referencia 65%
        fig.add_hline(
            y=65,
            line_dash="dash",
            line_color="#00E096",
            line_width=1,
            annotation_text="65%",
            annotation_position="right",
        )

        # Serie ICPI
        fig.add_trace(
            go.Scatter(
                x=labels,
                y=values,
                mode="lines+markers",
                name="ICPI (%)",
                line=dict(color="#00D4FF", width=2),
                marker=dict(size=8, color="#00D4FF"),
                connectgaps=True,
            )
        )

        fig.update_layout(
            title="Trayectoria ICPI — Períodos registrados",
            yaxis=dict(title="ICPI (%)", range=[0, 100], gridcolor="#1F2937"),
            xaxis=dict(title="Período", gridcolor="#1F2937"),
            plot_bgcolor="#0A1628",
            paper_bgcolor="#0A1628",
            font=dict(color="#E5E7EB"),
            height=340,
            margin=dict(l=40, r=20, t=50, b=40),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)
    except Exception as exc:
        st.warning(f"No se pudo renderizar el gráfico: {exc}")


def _render_doctrinal_note() -> None:
    """Nota doctrinal RC-M al pie."""
    st.markdown(
        """
        <div style='background:#111827;border-left:3px solid #00D4FF;
                    padding:12px 16px;border-radius:4px;margin-top:16px;font-size:0.82rem'>
        <strong style='color:#00D4FF'>Doctrina RC-M</strong><br>
        <span style='color:#9CA3AF'>
        La tabla RC-M convierte observaciones puntuales en trayectoria institucional.
        Ti &lt; 60% por ≥ 3 períodos consecutivos activa SAT-III REINCIDENTE
        (D3-Ejecución · COPFP Art. 113).
        ICPI &lt; 65% sostenido = riesgo de pérdida de elegibilidad a fondos
        (Q5-Proyección contextual).
        </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_no_data_hint() -> None:
    """Muestra instrucción cuando no hay snapshots suficientes."""
    st.markdown(
        """
        <div style='background:#111827;border:1px solid #374151;
                    padding:24px;border-radius:8px;text-align:center;margin:16px 0'>
        <div style='font-size:2rem'>📂</div>
        <div style='font-size:1rem;font-weight:600;color:#E5E7EB;margin:8px 0'>
            Sin historial longitudinal aún
        </div>
        <div style='font-size:0.85rem;color:#9CA3AF;max-width:480px;margin:0 auto'>
            Ejecuta el pipeline una vez por período (semana / mes) desde
            <strong>Control → Panel de Carga</strong>.
            Cada ejecución agrega un punto a la trayectoria RC-M.
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
