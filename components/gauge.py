"""
QUIRA OS v0.1 — Gauge semicircular ICGI-T
Plotly indicator adaptado para Streamlit dark theme
Dylus Lab © 2026
"""
import plotly.graph_objects as go
from typing import Optional


def render_gauge(
    score: float,
    label: str = "ICGI-T",
    avep_label: str = "",
    color: str = "#D69E2E",
    meta: float = 70.0,
    height: int = 280,
) -> go.Figure:
    """
    Genera un gauge semicircular para el score ICGI-T.

    Args:
        score: Valor 0-100
        label: Etiqueta central
        avep_label: Texto bajo el score (nivel AVEP)
        color: Color del arco según banda AVEP
        meta: Línea de meta (por defecto 70 = Gestión por Mandato)
        height: Alto del gráfico en px
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "suffix": "",
            "font": {"size": 48, "color": "#FFFFFF", "family": "Inter, sans-serif"},
            "valueformat": ".2f",
        },
        title={
            "text": f"<b>{label}</b><br><span style='font-size:13px;color:#A0AEC0'>{avep_label}</span>",
            "font": {"size": 15, "color": "#E2E8F0"},
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(255,255,255,0.2)",
                "tickvals": [0, 20, 40, 70, 90, 100],
                "ticktext": ["0", "20", "40", "70", "90", "100"],
                "tickfont": {"size": 10, "color": "rgba(255,255,255,0.4)"},
            },
            "bar": {"color": color, "thickness": 0.22},
            "bgcolor":  "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                # Bandas AVEP coloreadas (fondo)
                {"range": [0, 20],   "color": "rgba(229,62,62,0.15)"},
                {"range": [20, 40],  "color": "rgba(230,126,34,0.12)"},
                {"range": [40, 70],  "color": "rgba(214,158,46,0.12)"},
                {"range": [70, 90],  "color": "rgba(56,161,105,0.12)"},
                {"range": [90, 100], "color": "rgba(49,130,206,0.12)"},
            ],
            "threshold": {
                "line": {"color": "#00D4FF", "width": 3},
                "thickness": 0.85,
                "value": meta,
            },
        },
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#E2E8F0", "family": "Inter, sans-serif"},
        height=height,
        margin={"t": 60, "b": 10, "l": 30, "r": 30},
    )

    # Anotación de meta
    fig.add_annotation(
        x=0.5, y=-0.06,
        xref="paper", yref="paper",
        text=f"── Meta Mandato: {meta:.0f}%",
        showarrow=False,
        font={"size": 10, "color": "#00D4FF"},
        align="center",
    )

    return fig


def render_mini_gauge(
    score: float,
    color: str = "#D69E2E",
    height: int = 140,
) -> go.Figure:
    """Gauge compacto para entidades del holding (P-02)."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "font": {"size": 28, "color": "#FFFFFF", "family": "Inter, sans-serif"},
            "valueformat": ".1f",
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "visible": False,
            },
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 20],   "color": "rgba(229,62,62,0.12)"},
                {"range": [20, 40],  "color": "rgba(230,126,34,0.10)"},
                {"range": [40, 70],  "color": "rgba(214,158,46,0.10)"},
                {"range": [70, 90],  "color": "rgba(56,161,105,0.10)"},
                {"range": [90, 100], "color": "rgba(49,130,206,0.10)"},
            ],
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin={"t": 20, "b": 0, "l": 10, "r": 10},
    )
    return fig
