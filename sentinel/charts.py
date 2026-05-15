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
)


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def get_template_text(query: str) -> str | None:
    """
    Devuelve texto contextual pre-escrito para queries de visualización o simulación.
    Si retorna un string → sentinel.py OMITE la llamada al LLM.
    Si retorna None → no hay intent reconocido, el LLM gestiona la respuesta.
    """
    q = _norm(query)

    # Sprint 4: Simulación paramétrica — bypass LLM, renderizar resultado directo
    from sentinel.simulate_policy import detect_simulation_intent, POLICY_LABELS
    sim_intent = detect_simulation_intent(query)
    if sim_intent:
        pol   = POLICY_LABELS.get(sim_intent["policy_type"], sim_intent["policy_type"])
        delta = sim_intent["delta"] * 100
        ter   = sim_intent["territorio"].replace("_", " ").title()
        return (
            f"**Simulación · {pol} · +{delta:.0f}% en {ter}**\n\n"
            f"Ejecutando CBST v0.1 (Coeficientes Beta de Simulación Territorial) "
            f"para modelar el impacto de un incremento del {delta:.0f}% en inversión "
            f"de {pol.lower()} en {ter}. "
            f"Los resultados muestran proyecciones sobre agua, NBI, TPS e ICGI-T cantonal. "
            f"Calibración: PDOT 2023-2027 + INEC 2022 + H99 Q1-2026. "
            f"El gráfico de impacto se genera automáticamente abajo.\n\n"
            f"_Modelo Beta · sujeto a calibración con datos eSIGEF Q2-Q4 2026_"
        )

    if _has(q, "nbi", "necesidades basicas", "insatisfechas"):
        return (
            "**NBI por Parroquia — Distribución de Necesidades Básicas Insatisfechas**\n\n"
            "Las 3 parroquias más críticas superan el umbral del 50%: **Aníbal San Andrés** (61.7%), "
            "**Isabel Muentes** (61.2%) y **Colorado** (58.4%). Más de la mitad de su población "
            "carece de acceso adecuado a servicios básicos. La brecha entre la parroquia más vulnerable "
            "y la cabecera cantonal (38.2%) es de **23.5 puntos porcentuales**. "
            "Acción prioritaria: inversión AH (agua/saneamiento) en zona rural.\n\n"
            "_Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026_"
        )

    if _has(q, "inversion per capita", "per capita", "inversion por habitante", "capita"):
        return (
            "**Inversión per Cápita — Brecha de Equidad Territorial**\n\n"
            "**Isabel Muentes** recibe **$40/hab** — la inversión más baja del cantón. "
            "**Montecristi (cabecera)** recibe **$113/hab**. La brecha es de **2.83x**: "
            "por cada dólar que llega a Isabel Muentes, la cabecera recibe $2.83. "
            "El IET (Equidad Territorial) registra 44.80 — Transición Crítica. SAT-III activa. "
            "La línea del gráfico indica el promedio cantonal.\n\n"
            "_Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026_"
        )

    if _has(q, "indices", "indice", "complementarios",
             "ife", "ied", "igp", "psg", "itam", "ioc", "iet", "icods", "isp"):
        return (
            "**Índices Complementarios QUIRA OS — Corte Q1-2026**\n\n"
            "En **Ruptura Sistémica** (< 30): ISP=14.58 🔴 y PSG=12.83 🔴 — el PSG bloquea "
            "el acceso al Gender Bond de ONU Mujeres. En **Gestión por Mandato** (≥70): "
            "ICODS=87.50 🟢 y IFE-A=72.73 🟢. IGP=27.98 🟠 — solo 50 Unidades Territoriales "
            "activas vs meta de 75. Las líneas de referencia muestran los umbrales AVEP.\n\n"
            "_Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026_"
        )

    if _has(q, "icgi", "evolucion", "historico", "historia") and _has(q, *_VIZ_TRIGGER):
        return (
            "**Evolución ICGI-T 2023 → Q1-2026 → Proyección 2026**\n\n"
            "Tendencia positiva: **57.36** (2023) → **67.12** (2024) → **69.93** (2025). "
            "**Q1-2026 marca 53.56** — corte de solo marzo, con ejecución del 23.75% del presupuesto "
            "($6.3M de $26.7M), ritmo normal para el primer trimestre. "
            "Proyección cierre 2026: **65.77** — aún por debajo de la meta Mandato (70.0). "
            "Se requiere acelerar ejecución en Q2-Q3.\n\n"
            "_Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026_"
        )

    if _has(q, "tps", "tasa pobreza", "pobreza por servicios"):
        return (
            "**TPS por Parroquia — Tasa de Pobreza por Servicios**\n\n"
            "**Isabel Muentes** lidera con **77.94%** 🔴 — casi 8 de cada 10 personas en "
            "situación de pobreza por servicios. **Aníbal San Andrés** (62.34%) y "
            "**Colorado** (58.67%) también en zona crítica. La cabecera **Montecristi** "
            "registra 22.45% 🟢. La brecha TPS cantonal es de **55.5 puntos porcentuales**.\n\n"
            "_Fuente: INEC/PDOT diagnóstico oficial · Q1-2026_"
        )

    if _has(q, "agua", "cobertura agua", "acceso agua") and _has(q, *_VIZ_TRIGGER):
        return (
            "**Cobertura de Agua Potable por Parroquia**\n\n"
            "**Isabel Muentes** tiene cobertura de apenas **1.02%** 🔴 — prácticamente sin "
            "acceso a agua potable. **Aníbal San Andrés** (28.9%) y **Colorado** (34.7%) "
            "también están en situación crítica. La meta PDOT 2027 es llevar la cobertura "
            "cantonal del 39.25% al **42.38%**. Sin intervención urgente en Isabel Muentes, "
            "la meta es inalcanzable.\n\n"
            "_Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026_"
        )

    if _has(q, "parroquia") and _has(q, *_VIZ_TRIGGER):
        return (
            "**Análisis Territorial por Parroquia**\n\n"
            "Las 4 parroquias rurales más vulnerables superan el 50% de NBI. "
            "Isabel Muentes (61.2%) y Aníbal San Andrés (61.7%) son las más críticas. "
            "La cabecera cantonal (38.2%) concentra la mayor inversión per cápita ($113/hab) "
            "mientras Isabel Muentes recibe solo $40/hab.\n\n"
            "_Fuente: SIAP-ICPI Gold Master v4.1 · Q1-2026_"
        )

    return None


def detect_and_render(query: str) -> bool:
    """
    Detecta intención de visualización o simulación, renderiza componentes
    y activa UI contextual via ui_router. Returns True si renderizó algo.
    """
    from data.loader import load_all
    from sentinel import ui_router
    data = load_all()
    q    = _norm(query)
    hit  = False

    # ── Sprint 4: Simulación paramétrica (tiene prioridad sobre charts) ────────
    from sentinel.simulate_policy  import detect_simulation_intent, simulate_policy
    from sentinel.ui_components    import simulation_card, evidence_card, nav_card
    from sentinel.legal_router     import find_legal_refs
    from sentinel.coherencia_engine import evaluate as _coh_eval
    from sentinel.ui_components    import coherencia_card
    sim_intent = detect_simulation_intent(query)
    if sim_intent:
        result = simulate_policy(**sim_intent)
        if result:
            simulation_card(result, query_hash=hash(query) & 0xFFFF)

            # Fase 3 — Coherencia Institucional automática tras proyección
            _legal_refs = find_legal_refs(query)
            _territory  = result.get("territorio")
            _coh_result = _coh_eval(
                query      = query,
                data       = data,
                sim_result = result,
                legal_refs = _legal_refs,
                territory  = _territory,
            )
            coherencia_card(_coh_result)

            evidence_card(
                sources=[
                    f"CBST {result['cbst_version']} · {result['model_status']}",
                    result["calibration_basis"],
                    f"H99_ENGINE_CORE · {result['territorio']} Q1-2026",
                ],
                confidence=result["confidence_label"],
                note=result["nota"],
            )
            from sentinel import state_memory
            state_memory.update_state(query)
            return True

    # NBI por parroquia
    if _has(q, "nbi", "necesidades basicas", "insatisfechas"):
        _chart_nbi(data); hit = True

    # Inversión per cápita
    elif _has(q, "inversion per capita", "per capita", "inversion por habitante",
              "inversion/hab", "capita"):
        _chart_inversion(data); hit = True

    # Cobertura de agua
    elif _has(q, "agua", "cobertura agua", "acceso agua") and _has(q, *_VIZ_TRIGGER):
        _chart_agua(data); hit = True

    # TPS
    elif _has(q, "tps", "tasa pobreza", "pobreza por servicios"):
        _chart_tps(data); hit = True

    # Índices complementarios
    elif _has(q, "indices", "indice", "complementarios",
              "ife", "ied", "igp", "psg", "itam", "ioc", "iet", "icods", "isp"):
        _chart_indices(data); hit = True

    # Evolución ICGI-T
    elif _has(q, "icgi", "evolucion", "historico", "historia") and _has(q, *_VIZ_TRIGGER):
        _chart_icgit_trend(data); hit = True

    # Genérico parroquias
    elif _has(q, "parroquia") and _has(q, *_VIZ_TRIGGER):
        _chart_nbi(data); hit = True

    if hit:
        from sentinel import state_memory
        state_memory.update_state(query)   # Sprint 3: persiste contexto
        ui_router.route(query)             # Generative UI contextual (Opción C)

    return hit


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
        **_DARK, height=310,
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
        **_DARK, height=310,
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
        **_DARK, height=310,
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
        **_DARK, height=310,
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
        **_DARK, height=310,
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
