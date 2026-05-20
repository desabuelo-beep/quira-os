"""
QUIRA OS · p_historico.py
Inteligencia Histórica del Holding Municipal — Sprint 2.5B

Visualiza la evolución de Ti por entidad (GAD · BOMBEROS · EMAI-EP · PATRONATO),
ranking de ejecución de inversión y semáforo de alertas automático.

Sprint 2.5B · Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

from quira_pages.html_engine import DEMO_CSS, page_frame
from sentinel.historical_engine import (
    get_resumen_holding,
    get_tendencia_entidad,
    get_ranking_entidades,
    detect_alertas,
    get_holding_totales,
    get_meses_disponibles,
    ENTIDADES,
)

# ── PALETA POR ENTIDAD ────────────────────────────────────────────────────────
COLORES = {
    "GAD":       "#00D4FF",   # cyan
    "BOMBEROS":  "#FF4D6D",   # rojo
    "EMAI-EP":   "#00E096",   # verde
    "PATRONATO": "#FFB800",   # ámbar
}

MESES_CORTOS = ["", "Ene", "Feb", "Mar", "Abr", "May", "Jun",
                 "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

EXTRA_CSS = """
.sec-label {
  font-size: 9px; font-weight: 700; letter-spacing: 1.2px;
  text-transform: uppercase; color: var(--cyan);
  border-left: 3px solid var(--cyan); padding-left: 9px;
  margin-bottom: 12px;
}
.kpi-box {
  background: var(--navy-light); border: 1px solid var(--divider);
  border-radius: 10px; padding: 14px 16px; text-align: center;
}
.kpi-num  { font-family: var(--mono); font-size: 24px; font-weight: 800; color: var(--cyan); }
.kpi-lbl  { font-size: 10px; color: var(--muted); margin-top: 4px; }
.rank-row {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid var(--divider);
  font-size: 13px;
}
.rank-row:last-child { border-bottom: none; }
.rank-num  { font-family: var(--mono); font-size: 20px; font-weight: 800; color: var(--muted); width: 28px; }
.rank-name { font-weight: 700; color: var(--white); flex: 1; }
.rank-ti   { font-family: var(--mono); font-size: 14px; font-weight: 800; }
.rank-bar-wrap { flex: 2; background: rgba(255,255,255,0.06); border-radius: 4px; height: 6px; }
.rank-bar      { height: 6px; border-radius: 4px; }
.sem-card {
  display: flex; align-items: flex-start; gap: 14px;
  background: var(--navy-light); border: 1px solid var(--divider);
  border-radius: 10px; padding: 14px 16px; margin-bottom: 8px;
}
.sem-dot  { width: 12px; height: 12px; border-radius: 50%; margin-top: 3px; flex-shrink: 0; }
.dot-rojo    { background: #FF4D6D; box-shadow: 0 0 8px #FF4D6D88; }
.dot-amarillo{ background: #FFB800; box-shadow: 0 0 8px #FFB80088; }
.dot-verde   { background: #00E096; box-shadow: 0 0 8px #00E09688; }
.sem-entidad { font-weight: 700; color: var(--white); font-size: 13px; }
.sem-msg     { font-size: 12px; color: var(--muted); margin-top: 3px; }
.avail-dot   { display:inline-block; width:10px; height:10px; border-radius:50%;
               margin-right:4px; vertical-align:middle; }
"""


# ── HELPERS ───────────────────────────────────────────────────────────────────
def _fmt_m(v: float) -> str:
    if v >= 1_000_000:
        return f"${v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"${v/1_000:.0f}K"
    return f"${v:,.0f}"


def _sem_color_css(semaforo: str) -> str:
    return {"rojo": "#FF4D6D", "amarillo": "#FFB800", "verde": "#00E096"}.get(semaforo, "#888")


# ── PANEL: TOTALES DEL HOLDING ────────────────────────────────────────────────
def _panel_totales(totales: dict) -> str:
    if not totales:
        return '<div class="card"><p style="color:var(--muted)">Sin datos disponibles.</p></div>'

    ti = totales.get("ti_holding", 0)
    color = "#00E096" if ti >= 35 else "#FFB800" if ti >= 15 else "#FF4D6D"
    mes_label = MESES_CORTOS[totales.get("ultimo_mes", 0)] if totales.get("ultimo_mes") else "–"

    return f"""
<div class="card">
  <div class="sec-label">Holding Municipal · Consolidado {totales['year']} (al {mes_label})</div>
  <div class="grid-4">
    <div class="kpi-box">
      <div class="kpi-num" style="color:{color}">{ti:.1f}%</div>
      <div class="kpi-lbl">Ti Holding (inversión)</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{_fmt_m(totales.get('devengado_inv',0))}</div>
      <div class="kpi-lbl">Devengado inversión</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{_fmt_m(totales.get('codificado_inv',0))}</div>
      <div class="kpi-lbl">Codificado inversión</div>
    </div>
    <div class="kpi-box">
      <div class="kpi-num">{totales.get('num_entidades',0)}</div>
      <div class="kpi-lbl">Entidades con datos</div>
    </div>
  </div>
</div>
"""


# ── PANEL: RANKING ────────────────────────────────────────────────────────────
def _panel_ranking(ranking: list[dict]) -> str:
    if not ranking:
        return ""
    max_ti = max((r["ti_real"] for r in ranking), default=100) or 100
    rows = ""
    for r in ranking:
        color  = COLORES.get(r["entidad"], "#888")
        ti     = r["ti_real"]
        bar_w  = min(100, round(ti / max_ti * 100))
        rows += f"""
<div class="rank-row">
  <div class="rank-num">#{r['rank']}</div>
  <div class="rank-name" style="color:{color}">{r['entidad']}</div>
  <div class="rank-bar-wrap">
    <div class="rank-bar" style="width:{bar_w}%;background:{color}"></div>
  </div>
  <div class="rank-ti" style="color:{color}">{ti:.1f}%</div>
  <div style="font-size:11px;color:var(--muted);width:90px;text-align:right">
    {_fmt_m(r['devengado_inv'])} / {_fmt_m(r['codificado_inv'])}
  </div>
</div>"""

    return f"""
<div class="card">
  <div class="sec-label">Ranking Ti inversión — Holding 2026</div>
  {rows}
</div>
"""


# ── PANEL: ALERTAS ────────────────────────────────────────────────────────────
def _panel_alertas(alertas: list[dict]) -> str:
    if not alertas:
        return ""
    items = ""
    for a in alertas:
        color  = _sem_color_css(a["semaforo"])
        dot_cls = f"dot-{a['semaforo']}"
        mes_s   = MESES_CORTOS[a.get("mes", 0)] if a.get("mes") else "–"
        items += f"""
<div class="sem-card">
  <div class="sem-dot {dot_cls}"></div>
  <div>
    <div class="sem-entidad" style="color:{color}">{a['entidad']}
      <span style="font-size:10px;color:var(--muted);font-weight:400;margin-left:6px">{mes_s} 2026</span>
    </div>
    <div class="sem-msg">{a['mensaje']}</div>
  </div>
</div>"""

    return f"""
<div class="card">
  <div class="sec-label">Semáforo de ejecución — último período disponible</div>
  {items}
</div>
"""


# ── PANEL: DISPONIBILIDAD ─────────────────────────────────────────────────────
def _panel_disponibilidad(meses_disp: dict[str, list]) -> str:
    meses_target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    rows = ""
    for entidad in ENTIDADES:
        disponibles = meses_disp.get(entidad, [])
        dots = ""
        for m in meses_target:
            if m <= 3:  # Solo mostramos Jan-Mar (los que tenemos)
                ok = m in disponibles
                color = COLORES.get(entidad, "#888") if ok else "rgba(255,255,255,0.12)"
                dots += f'<span class="avail-dot" style="background:{color}" title="{MESES_CORTOS[m]}"></span>'
        entidad_color = COLORES.get(entidad, "#888")
        rows += f"""
<div style="display:flex;align-items:center;gap:10px;padding:6px 0;
            border-bottom:1px solid var(--divider)">
  <div style="color:{entidad_color};font-weight:700;font-size:12px;width:90px">{entidad}</div>
  <div>{dots}</div>
  <div style="font-size:11px;color:var(--muted)">{len(disponibles)} mes(es)</div>
</div>"""

    return f"""
<div class="card">
  <div class="sec-label">Disponibilidad de cédulas (Ene–Mar 2026)</div>
  {rows}
</div>
"""


# ── GRÁFICA: TENDENCIA Ti POR ENTIDAD ─────────────────────────────────────────
def _chart_tendencia(tendencia: dict[str, list]) -> go.Figure:
    fig = go.Figure()

    for entidad, series in tendencia.items():
        if not series:
            continue
        xs = [MESES_CORTOS[p["month"]] for p in series]
        ys = [p["ti"] for p in series]
        color = COLORES.get(entidad, "#888")

        fig.add_trace(go.Scatter(
            x=xs, y=ys,
            name=entidad,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=8, color=color, line=dict(color="#0A0F1E", width=1.5)),
            hovertemplate=f"<b>{entidad}</b><br>%{{x}}: Ti=%{{y:.1f}}%<extra></extra>",
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,15,30,0.4)",
        font=dict(color="#94A3B8", size=11),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#94A3B8"),
            linecolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            ticksuffix="%",
            tickfont=dict(color="#94A3B8"),
        ),
        margin=dict(t=10, b=10, l=0, r=0),
        height=300,
        hovermode="x unified",
    )
    return fig


# ── GRÁFICA: BARRAS COMPARATIVAS ─────────────────────────────────────────────
def _chart_barras_comparativas(ranking: list[dict]) -> go.Figure:
    entidades = [r["entidad"] for r in ranking]
    colores   = [COLORES.get(e, "#888") for e in entidades]
    cod_vals  = [r["codificado_inv"] / 1_000_000 for r in ranking]
    dev_vals  = [r["devengado_inv"]  / 1_000_000 for r in ranking]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Codificado Inv.",
        x=entidades, y=cod_vals,
        marker_color=[c + "44" for c in colores],
        marker_line=dict(color=colores, width=1.5),
        hovertemplate="<b>%{x}</b><br>Codificado: $%{y:.2f}M<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Devengado Inv.",
        x=entidades, y=dev_vals,
        marker_color=colores,
        hovertemplate="<b>%{x}</b><br>Devengado: $%{y:.2f}M<extra></extra>",
    ))

    fig.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,15,30,0.4)",
        font=dict(color="#94A3B8", size=11),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(showgrid=False, tickfont=dict(color="#94A3B8")),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.06)",
            tickprefix="$", ticksuffix="M",
            tickfont=dict(color="#94A3B8"),
        ),
        margin=dict(t=10, b=10, l=0, r=0),
        height=280,
    )
    return fig


# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────
def render() -> None:
    st.markdown("""
<div style="padding:12px 0 8px">
  <div style="font-size:18px;font-weight:800;color:#00D4FF;letter-spacing:-.02em">
    Inteligencia Histórica · Holding Municipal
  </div>
  <div style="font-size:12px;color:rgba(255,255,255,0.45);margin-top:2px">
    GAD · Bomberos · EMAI-EP · Patronato — Ejecución Jan–Mar 2026
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Selector de año ───────────────────────────────────────────────────────
    col_year, _ = st.columns([1, 5])
    with col_year:
        year = st.number_input("Año", min_value=2024, max_value=2030,
                               value=2026, step=1, label_visibility="visible")

    year = int(year)

    # ── Carga de datos ────────────────────────────────────────────────────────
    totales   = get_holding_totales(year)
    tendencia = get_tendencia_entidad(year)
    ranking   = get_ranking_entidades(year)
    alertas   = detect_alertas(year)
    meses_d   = get_meses_disponibles(year)

    if not totales:
        st.warning(f"No hay datos disponibles para el año {year}. "
                   "Ingresa cédulas desde el Centro de Ingesta.")
        return

    # ── Panel totales consolidados ────────────────────────────────────────────
    totales_html = page_frame(DEMO_CSS + EXTRA_CSS, _panel_totales(totales))
    components.html(totales_html, height=170, scrolling=False)

    # ── Gráficas ──────────────────────────────────────────────────────────────
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown(
            '<div style="font-size:10px;font-weight:700;color:#00D4FF;'
            'text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">'
            'Tendencia Ti mensual por entidad</div>',
            unsafe_allow_html=True,
        )
        fig_tend = _chart_tendencia(tendencia)
        st.plotly_chart(fig_tend, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown(
            '<div style="font-size:10px;font-weight:700;color:#00D4FF;'
            'text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">'
            'Codificado vs Devengado inversión ($M)</div>',
            unsafe_allow_html=True,
        )
        if ranking:
            fig_bar = _chart_barras_comparativas(ranking)
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # ── Ranking + Alertas ─────────────────────────────────────────────────────
    col_r, col_s = st.columns([2, 1])

    with col_r:
        rank_html = page_frame(DEMO_CSS + EXTRA_CSS, _panel_ranking(ranking))
        components.html(rank_html, height=300, scrolling=False)

    with col_s:
        alertas_html = page_frame(
            DEMO_CSS + EXTRA_CSS,
            _panel_alertas(alertas) + _panel_disponibilidad(meses_d),
        )
        components.html(alertas_html, height=500, scrolling=True)
