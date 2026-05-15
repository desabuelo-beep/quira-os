"""
SENTINEL · charts.py
Motor de visualización determinístico — Sentinel v1.1.
Detecta intención en la query del usuario y renderiza charts pre-construidos
desde demo_data (sellados Q1-2026). No depende del LLM para los datos.
Dylus Lab © 2026
"""
from __future__ import annotations
import unicodedata
import streamlit as st

# ── HELPERS ────────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    """Normaliza texto: minúsculas + sin tildes para matching robusto."""
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _has(q: str, *terms: str) -> bool:
    return any(t in q for t in terms)


_VIZ_TRIGGER = (
    "grafica", "grafico", "muestra", "muestrame", "visualiza",
    "compara", "comparacion", "barra", "tabla", "chart",
    "distribucion", "tendencia", "evolucion", "linea",
)

_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.02)",
    font=dict(color="#E2E8F0", size=11),
    margin=dict(t=58, b=44, l=10, r=10),
    height=310,
)


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def detect_and_render(query: str) -> bool:
    """
    Detecta intención de visualización y renderiza el chart correspondiente.
    Carga datos desde load_all() (cacheado). Returns True si renderizó algo.
    """
    from data.loader import load_all
    data = load_all()
    q = _norm(query)

    # NBI por parroquia
    if _has(q, "nbi", "necesidades basicas", "insatisfechas"):
        _chart_nbi(data)
        return True

    # Inversión per cápita
    if _has(q, "inversion per capita", "per capita", "inversion por habitante",
             "inversion/hab", "capita"):
        _chart_inversion(data)
        return True

    # Cobertura de agua
    if _has(q, "agua", "cobertura agua", "acceso agua") and _has(q, *_VIZ_TRIGGER):
        _chart_agua(data)
        return True

    # TPS — Tasa de Pobreza por Servicios
    if _has(q, "tps", "tasa pobreza", "pobreza por servicios"):
        _chart_tps(data)
        return True

    # Índices complementarios
    if _has(q, "indices", "indice", "complementarios",
             "ife", "ied", "igp", "psg", "itam", "ioc", "iet", "icods", "isp"):
        _chart_indices(data)
        return True

    # Evolución ICGI-T histórico
    if _has(q, "icgi", "evolucion", "historico", "historia") and _has(q, *_VIZ_TRIGGER):
        _chart_icgit_trend(data)
        return True

    # Petición genérica de parroquias con trigger visual
    if _has(q, "parroquia") and _has(q, *_VIZ_TRIGGER):
        _chart_nbi(data)   # default: NBI es la brecha más crítica
        return True

    return False


# ── CHART BUILDERS ─────────────────────────────────────────────────────────────

def _chart_nbi(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        st.warning("Instala `plotly` en requirements.txt")
        return

    parroquias = sorted(data.get("parroquias", []), key=lambda p: p["nbi"], reverse=True)
    if not parroquias:
        return

    labels = [p["nombre"] for p in parroquias]
    values = [p["nbi"]    for p in parroquias]
    colors = [
        "#E53E3E" if v >= 50 else "#F6AD55" if v >= 38 else "#38A169"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(size=10, color="#E2E8F0"),
    ))
    fig.update_layout(
        **_DARK,
        title=dict(
            text="NBI por Parroquia · Necesidades Básicas Insatisfechas"
                 "<br><sup>🔴 ≥50% crítico · 🟠 ≥38% alerta · 🟢 <38% · Q1-2026</sup>",
            font=dict(size=13, color="#E2E8F0"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, ticksuffix="%"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        showlegend=False,
    )
    _source_annotation(fig)
    st.plotly_chart(fig, use_container_width=True)


def _chart_inversion(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    parroquias = sorted(data.get("parroquias", []), key=lambda p: p["per_capita"])
    if not parroquias:
        return

    labels = [p["nombre"]    for p in parroquias]
    values = [p["per_capita"] for p in parroquias]
    colors = [
        "#E53E3E" if v <= 60 else "#F6AD55" if v <= 90 else "#38A169"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=[f"${v}/hab" for v in values],
        textposition="outside",
        textfont=dict(size=10, color="#E2E8F0"),
    ))

    # Línea de equidad (promedio)
    avg = sum(values) / len(values)
    fig.add_hline(y=avg, line_dash="dash", line_color="rgba(255,255,255,0.35)",
                  annotation_text=f"Promedio ${avg:.0f}/hab",
                  annotation_font_color="rgba(255,255,255,0.5)",
                  annotation_position="top right")

    fig.update_layout(
        **_DARK,
        title=dict(
            text="Inversión per Cápita por Parroquia · $/habitante"
                 "<br><sup>🔴 ≤$60 inequidad crítica · línea = promedio cantonal · Q1-2026</sup>",
            font=dict(size=13, color="#E2E8F0"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, tickprefix="$"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        showlegend=False,
    )
    _source_annotation(fig)
    st.plotly_chart(fig, use_container_width=True)


def _chart_tps(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    parroquias = sorted(data.get("parroquias", []), key=lambda p: p["tps"], reverse=True)
    if not parroquias:
        return

    labels = [p["nombre"] for p in parroquias]
    values = [p["tps"]    for p in parroquias]
    colors = [
        "#E53E3E" if v >= 60 else "#F6AD55" if v >= 35 else "#38A169"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(size=10, color="#E2E8F0"),
    ))
    fig.update_layout(
        **_DARK,
        title=dict(
            text="TPS por Parroquia · Tasa de Pobreza por Servicios"
                 "<br><sup>🔴 ≥60% · 🟠 ≥35% · 🟢 <35% · Fuente INEC/PDOT Q1-2026</sup>",
            font=dict(size=13, color="#E2E8F0"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, ticksuffix="%"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        showlegend=False,
    )
    _source_annotation(fig)
    st.plotly_chart(fig, use_container_width=True)


def _chart_agua(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    parroquias = sorted(data.get("parroquias", []), key=lambda p: p["agua"])
    if not parroquias:
        return

    labels = [p["nombre"] for p in parroquias]
    values = [p["agua"]   for p in parroquias]
    colors = [
        "#E53E3E" if v < 30 else "#F6AD55" if v < 60 else "#38A169"
        for v in values
    ]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(size=10, color="#E2E8F0"),
    ))
    fig.update_layout(
        **_DARK,
        title=dict(
            text="Cobertura de Agua Potable por Parroquia"
                 "<br><sup>🔴 <30% crítico · 🟠 <60% alerta · Meta PDOT 42.38% · Q1-2026</sup>",
            font=dict(size=13, color="#E2E8F0"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, ticksuffix="%"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        showlegend=False,
    )
    _source_annotation(fig)
    st.plotly_chart(fig, use_container_width=True)


def _chart_indices(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    indices = data.get("indices", {})
    items   = [(k, v) for k, v in indices.items() if v.get("valor") is not None]
    items   = sorted(items, key=lambda x: x[1]["valor"], reverse=True)

    if not items:
        return

    labels = [v["nombre"][:22] for _, v in items]
    keys   = [k for k, _ in items]
    values = [v["valor"] for _, v in items]
    colors = [v.get("color", "#00D4FF") for _, v in items]

    fig = go.Figure(go.Bar(
        x=labels, y=values,
        marker_color=colors,
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
        textfont=dict(size=10, color="#E2E8F0"),
        customdata=keys,
    ))

    # Líneas de referencia AVEP
    for y, label, color in [
        (90, "Excelencia 90", "rgba(56,161,105,0.4)"),
        (70, "Mandato 70",   "rgba(0,212,255,0.4)"),
        (50, "Transición 50","rgba(214,158,46,0.4)"),
        (30, "Ocurrencia 30","rgba(229,62,62,0.4)"),
    ]:
        fig.add_hline(y=y, line_dash="dot", line_color=color,
                      annotation_text=label,
                      annotation_font=dict(size=9, color=color),
                      annotation_position="top right")

    fig.update_layout(
        **_DARK,
        height=360,
        title=dict(
            text="Índices Complementarios QUIRA OS · AVEP Q1-2026"
                 "<br><sup>Barras de referencia AVEP: Excelencia·Mandato·Transición·Ocurrencia</sup>",
            font=dict(size=13, color="#E2E8F0"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, range=[0, 105]),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", tickangle=-30),
        showlegend=False,
    )
    _source_annotation(fig)
    st.plotly_chart(fig, use_container_width=True)


def _chart_icgit_trend(data: dict) -> None:
    try:
        import plotly.graph_objects as go
    except ImportError:
        return

    icgit = data.get("icgit", {})
    hist  = icgit.get("historico", {})

    labels = ["2023", "2024", "2025", "Q1-2026", "Proj. 2026"]
    values = [
        hist.get("2023",     57.36),
        hist.get("2024",     67.12),
        hist.get("2025",     69.93),
        hist.get("2026_q1",  53.56),
        hist.get("2026_proj",65.77),
    ]
    colors = ["#00D4FF", "#00D4FF", "#00D4FF", "#F6AD55", "rgba(0,212,255,0.4)"]

    fig = go.Figure()
    # Línea principal
    fig.add_trace(go.Scatter(
        x=labels[:4], y=values[:4],
        mode="lines+markers+text",
        line=dict(color="#00D4FF", width=2.5),
        marker=dict(size=9, color=colors[:4]),
        text=[f"{v:.2f}" for v in values[:4]],
        textposition="top center",
        textfont=dict(size=11, color="#E2E8F0"),
        name="Real",
    ))
    # Proyección punteada
    fig.add_trace(go.Scatter(
        x=["Q1-2026", "Proj. 2026"], y=[values[3], values[4]],
        mode="lines+markers+text",
        line=dict(color="#F6AD55", width=2, dash="dash"),
        marker=dict(size=8, color="#F6AD55"),
        text=["", f"{values[4]:.2f}"],
        textposition="top center",
        textfont=dict(size=11, color="#F6AD55"),
        name="Proyección",
    ))
    # Meta Mandato
    fig.add_hline(y=70, line_dash="dot", line_color="rgba(56,161,105,0.5)",
                  annotation_text="Meta Mandato 70.0",
                  annotation_font=dict(size=9, color="rgba(56,161,105,0.7)"),
                  annotation_position="top left")

    fig.update_layout(
        **_DARK,
        title=dict(
            text="Evolución ICGI-T · 2023 → Q1-2026 → Proyección 2026"
                 "<br><sup>🔵 Real · 🟠 Proyección · --- Meta Mandato 70.0</sup>",
            font=dict(size=13, color="#E2E8F0"),
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False, range=[40, 80]),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        showlegend=False,
    )
    _source_annotation(fig)
    st.plotly_chart(fig, use_container_width=True)


def _source_annotation(fig) -> None:
    fig.add_annotation(
        text="Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026",
        xref="paper", yref="paper",
        x=1.0, y=-0.20, showarrow=False,
        font=dict(size=9, color="rgba(255,255,255,0.28)"),
        align="right",
    )
