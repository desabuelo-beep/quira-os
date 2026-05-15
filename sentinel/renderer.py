"""
SENTINEL · renderer.py
Parser + Renderer para respuestas generativas — Sentinel v1.1 (Opción A).
Intercepta bloques ```json con renderType y los convierte en componentes Streamlit.
Doctrina: Sentinel genera intención + estructura / Streamlit renderiza la experiencia.
Dylus Lab © 2026
"""
from __future__ import annotations
import re
import json
import streamlit as st

_JSON_PATTERN = re.compile(r"```json\s*([\s\S]*?)\s*```", re.IGNORECASE)

_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#E2E8F0", size=11),
    margin=dict(t=54, b=44, l=10, r=10),
    height=300,
)


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def parse_response(text: str) -> tuple[str, dict | None]:
    """
    Extrae el primer bloque ```json con renderType de una respuesta Sentinel.
    Devuelve (texto_limpio, datos_visual | None).
    El texto limpio es la respuesta sin el bloque JSON.
    """
    match = _JSON_PATTERN.search(text)
    if not match:
        return text, None
    try:
        data = json.loads(match.group(1))
        if "renderType" in data:
            before = text[: match.start()].rstrip()
            after  = text[match.end() :].lstrip()
            clean  = (before + ("\n" + after if after else "")).strip()
            return clean, data
    except (json.JSONDecodeError, ValueError):
        pass
    return text, None


def render_visual(data: dict) -> None:
    """Despacha el renderType al componente Streamlit correspondiente."""
    rtype = data.get("renderType", "")
    if rtype == "chart":
        _render_chart(data)
    elif rtype == "kpi_grid":
        _render_kpi_grid(data)
    elif rtype == "table":
        _render_table(data)
    elif rtype == "alert":
        _render_alert(data)


# ── RENDERERS ──────────────────────────────────────────────────────────────────

def _render_chart(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.warning("Instala `plotly` en requirements.txt para ver gráficos Sentinel.")
        return

    labels     = data.get("labels", [])
    values     = data.get("values", [])
    title      = data.get("title", "")
    subtitle   = data.get("subtitle", "")
    chart_type = data.get("chartType", "bar")
    unit       = data.get("unit", "")
    threshold  = data.get("color_threshold")
    source     = data.get("source", "SIAP-ICPI")

    if not labels or not values or len(labels) != len(values):
        return

    fig = go.Figure()

    if chart_type == "bar":
        colors = [
            "#E53E3E" if (threshold is not None and float(v) >= threshold) else "#00D4FF"
            for v in values
        ]
        fig.add_trace(go.Bar(
            x=labels, y=values,
            marker_color=colors,
            text=[f"{v}{unit}" for v in values],
            textposition="outside",
            textfont=dict(size=10, color="#E2E8F0"),
        ))
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.07)", zeroline=False)
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.07)")

    elif chart_type == "line":
        fig.add_trace(go.Scatter(
            x=labels, y=values,
            mode="lines+markers+text",
            line=dict(color="#00D4FF", width=2.5),
            marker=dict(size=8, color="#00D4FF"),
            text=[f"{v}{unit}" for v in values],
            textposition="top center",
            textfont=dict(size=10, color="#E2E8F0"),
        ))
        fig.update_yaxes(gridcolor="rgba(255,255,255,0.07)")
        fig.update_xaxes(gridcolor="rgba(255,255,255,0.07)")

    full_title = title + (f"<br><sup style='color:rgba(255,255,255,0.4)'>{subtitle}</sup>" if subtitle else "")
    fig.update_layout(
        **_DARK,
        title=dict(text=full_title, font=dict(size=13, color="#E2E8F0")),
        showlegend=False,
    )
    fig.add_annotation(
        text=f"Fuente: {source} · SIAP-ICPI Q1-2026",
        xref="paper", yref="paper",
        x=1.0, y=-0.20, showarrow=False,
        font=dict(size=9, color="rgba(255,255,255,0.28)"),
        align="right",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_kpi_grid(data: dict) -> None:
    items = data.get("items", [])
    title = data.get("title", "")
    if not items:
        return
    if title:
        st.caption(f"📊 {title.upper()}")
    n = min(len(items), 4)
    cols = st.columns(n)
    for i, item in enumerate(items):
        with cols[i % n]:
            delta = item.get("delta")
            val   = f"{item.get('value', '')}{item.get('unit', '')}"
            st.metric(label=item.get("label", ""), value=val, delta=delta)


def _render_table(data: dict) -> None:
    import pandas as pd
    columns = data.get("columns", [])
    rows    = data.get("rows", [])
    title   = data.get("title", "")
    if not columns or not rows:
        return
    if title:
        st.caption(f"📋 {title.upper()}")
    df = pd.DataFrame(rows, columns=columns)
    st.dataframe(df, use_container_width=True, hide_index=True)


def _render_alert(data: dict) -> None:
    level   = data.get("level", "warning")
    message = data.get("message", "")
    if not message:
        return
    {"error": st.error, "success": st.success, "info": st.info}.get(
        level, st.warning
    )(message)
