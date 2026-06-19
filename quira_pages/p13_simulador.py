"""
QUIRA OS v0.1 — P-13 Simulador de Escenarios
¿Qué ICGI-T logramos si mejoramos X? · Motor de escenarios interactivo
Tab 2: Sensibilidad IRS · Composite_Need v2.1 · Análisis del tester
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico

# ── MODELO SIMPLIFICADO ICGI-T ────────────────────────────────────────────────
_VECTORES = [
    {
        "key":     "isp",
        "codigo":  "Presupuesto",
        "nombre":  "Salud Presupuestaria",
        "actual":  14.58,
        "meta":    65.0,
        "peso":    0.22,
        "impacto": -8.2,
        "color":   "🔴",
        "accion":  "Activar coactivas + catastro predial",
    },
    {
        "key":     "ied",
        "codigo":  "Eficiencia",
        "nombre":  "Eficiencia Direcciones",
        "actual":  33.99,
        "meta":    70.0,
        "peso":    0.18,
        "impacto": -6.8,
        "color":   "🔴",
        "accion":  "Publicar evidencias PAC · cerrar señales de alerta",
    },
    {
        "key":     "igp",
        "codigo":  "Participación",
        "nombre":  "Gobernanza Participativa",
        "actual":  27.98,
        "meta":    60.0,
        "peso":    0.14,
        "impacto": -4.1,
        "color":   "🟠",
        "accion":  "Convocar asambleas parroquiales · 75 UT activas",
    },
    {
        "key":     "ioc",
        "codigo":  "Transparencia",
        "nombre":  "Transparencia (invertido)",
        "actual":  17.71,
        "meta":    40.0,
        "peso":    0.12,
        "impacto": -3.1,
        "color":   "🟠",
        "accion":  "Actualizar LOTAIP · publicar POA/PAC en portal",
    },
    {
        "key":     "iet",
        "codigo":  "Equidad",
        "nombre":  "Equidad Territorial",
        "actual":  44.80,
        "meta":    70.0,
        "peso":    0.10,
        "impacto": -2.8,
        "color":   "🟡",
        "accion":  "Redirigir inversión Q2 · $80/hab parroquias rurales",
    },
    {
        "key":     "psg",
        "codigo":  "Género",
        "nombre":  "Presupuesto de Género",
        "actual":  12.83,
        "meta":    30.0,
        "peso":    0.08,
        "impacto": -2.4,
        "color":   "🟡",
        "accion":  "Reclasificar programas género en POA-Q2",
    },
]

_SCORE_BASE   = 53.56
_META_MANDATO = 70.0

# ── IRS SENSITIVITY DATA (Tester v2.1 · Composite_Need analysis) ──────────────
# Columns: label, w_agua_gap(%), w_nbi(%), w_pop(%), irs_global
_IRS_ESCENARIOS = [
    {"label": "Base Anterior",       "w_agua": 45, "w_nbi": 30, "w_pop": 25, "irs": 78.4, "rec": False},
    {"label": "Alto énfasis NBI",    "w_agua": 35, "w_nbi": 50, "w_pop": 15, "irs": 82.1, "rec": False},
    {"label": "Alto énfasis Agua",   "w_agua": 60, "w_nbi": 25, "w_pop": 15, "irs": 76.9, "rec": False},
    {"label": "★ Recomendado v2.1",  "w_agua": 50, "w_nbi": 30, "w_pop": 20, "irs": 79.7, "rec": True},
    {"label": "Bajo énfasis NBI",    "w_agua": 50, "w_nbi": 20, "w_pop": 30, "irs": 74.3, "rec": False},
    {"label": "Muy bajo NBI",        "w_agua": 55, "w_nbi": 15, "w_pop": 30, "irs": 71.8, "rec": False},
]


def _calcular_icgit(mejoras: dict) -> float:
    score = _SCORE_BASE
    for v in _VECTORES:
        nuevo = mejoras.get(v["key"], v["actual"])
        delta = nuevo - v["actual"]
        rango = v["meta"] - v["actual"]
        if rango > 0 and delta > 0:
            fraccion = min(delta / rango, 1.0)
            score += fraccion * abs(v["impacto"])
    return min(score, 100.0)


def _avep_label(s: float) -> tuple[str, str]:
    if s >= 85: return "Excelencia Institucional", "green"
    if s >= 70: return "Gestión por Mandato",      "green"
    if s >= 50: return "Transición Crítica",        "amber"
    if s >= 30: return "Gestión por Ocurrencia",    "red"
    return "Ruptura Sistémica", "red"


def _avep_irs(v: float) -> tuple[str, str]:
    if v >= 70: return "Muy Regresivo", "red"
    if v >= 50: return "Regresivo",     "amber"
    if v >= 30: return "Moderado",      "amber"
    return "Equitativo", "green"


def _gauge_bar(score: float, label: str, col: str) -> str:
    pct = min(score, 100)
    return f"""
<div style="margin-bottom:6px">
  <div style="display:flex;justify-content:space-between;
              font-size:10px;color:rgba(255,255,255,.5);margin-bottom:4px">
    <span>{label}</span><span>{score:.2f}%</span>
  </div>
  <div style="height:10px;background:rgba(255,255,255,.07);
              border-radius:5px;overflow:hidden">
    <div style="height:10px;width:{pct:.1f}%;
                background:var(--{col});border-radius:5px;
                transition:width .3s ease"></div>
  </div>
</div>"""


def _irs_interpolado(w_nbi: float) -> float:
    """Interpolación lineal a trozos desde los puntos validados por el tester."""
    # Sorted by w_nbi, averaging duplicates (w_nbi=30 aparece dos veces: 78.4 y 79.7)
    pts = [(15, 71.8), (20, 74.3), (25, 76.9), (30, 79.05), (50, 82.1)]
    if w_nbi <= pts[0][0]:
        return pts[0][1]
    if w_nbi >= pts[-1][0]:
        return round(pts[-1][1] + (w_nbi - pts[-1][0]) * 0.06, 1)
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        if x0 <= w_nbi <= x1:
            return round(y0 + (y1 - y0) * (w_nbi - x0) / (x1 - x0), 1)
    return 79.7


def render() -> None:
    load_all()
    is_tecnico()

    st.markdown("""
<style>
.sim-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}
.sim-score {
    font-size: 72px;
    font-weight: 900;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    line-height: 1;
    text-align: center;
}
.sim-avep {
    font-size: 14px;
    font-weight: 700;
    text-align: center;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: .08em;
}
.sim-label {
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="margin-bottom:16px">
  <div style="font-size:11px;font-weight:700;color:#00D4FF;
              text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px">
    ⑨ PROYECTOR DE ESCENARIOS
  </div>
  <div style="font-size:22px;font-weight:900;color:#F0F4FF;margin-bottom:4px">
    Motor de Escenarios QUIRA OS
  </div>
  <div style="font-size:11px;color:rgba(255,255,255,0.45)">
    Tab 1: Calificación de gestión — vectores de mejora · Tab 2: Regresividad de la inversión — análisis de sensibilidad
  </div>
</div>
""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Calificación · Vectores de Mejora", "🔴 Regresividad de la Inversión · Sensibilidad"])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — ICGI-T SIMULATOR (existing content)
    # ══════════════════════════════════════════════════════════════════════════
    with tab1:
        col_sliders, col_resultado = st.columns([3, 2], gap="large")
        mejoras = {}

        with col_sliders:
            st.markdown('<div class="sim-label">VECTORES DE MEJORA · MUEVE LOS SLIDERS</div>',
                        unsafe_allow_html=True)
            for v in _VECTORES:
                st.markdown(
                    f'<div style="font-size:11px;font-weight:700;color:#E2E8F0;margin-bottom:2px">'
                    f'{v["color"]} {v["nombre"]}</div>'
                    f'<div style="font-size:9px;color:rgba(255,255,255,.4);margin-bottom:4px">'
                    f'Actual: {v["actual"]:.1f}% · Meta: {v["meta"]:.0f}% · '
                    f'Prioridad: {"🔴 Alta" if abs(v["impacto"]) >= 6 else "🟠 Media" if abs(v["impacto"]) >= 3 else "🟡 Normal"}</div>',
                    unsafe_allow_html=True,
                )
                nuevo_val = st.slider(
                    label=v["codigo"],
                    min_value=float(v["actual"]),
                    max_value=float(v["meta"]),
                    value=float(v["actual"]),
                    step=0.5,
                    format="%.1f%%",
                    label_visibility="collapsed",
                    key=f"sim_{v['key']}",
                )
                mejoras[v["key"]] = nuevo_val
                ganancia = nuevo_val - v["actual"]
                if ganancia > 0.1:
                    st.markdown(
                        f'<div style="font-size:9px;color:#00E096;margin-bottom:12px">'
                        f'▲ +{ganancia:.1f} pts en {v["codigo"]} → mejora la calificación</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown('<div style="margin-bottom:12px"></div>', unsafe_allow_html=True)

        with col_resultado:
            score_proj = _calcular_icgit(mejoras)
            avep_label, avep_col = _avep_label(score_proj)
            delta_vs_base = score_proj - _SCORE_BASE
            delta_vs_meta = score_proj - _META_MANDATO
            col_score_hex = {"green": "#00E096", "amber": "#FFB800", "red": "#FF4D6D"}[avep_col]

            st.markdown(f"""
<div class="sim-card" style="border-top:3px solid {col_score_hex}">
  <div class="sim-label">CALIFICACIÓN PROYECTADA</div>
  <div class="sim-score" style="color:{col_score_hex}">{score_proj:.2f}<span style="font-size:28px">%</span></div>
  <div class="sim-avep" style="color:{col_score_hex}">{avep_label}</div>
</div>
""", unsafe_allow_html=True)

            st.markdown('<div class="sim-label" style="margin-top:8px">COMPARATIVAS</div>',
                        unsafe_allow_html=True)
            st.markdown(
                _gauge_bar(_SCORE_BASE, "ene–mar 2026 (base)", "red")
                + _gauge_bar(score_proj, f"Proyectado ({avep_label[:10]})", avep_col)
                + _gauge_bar(69.93, "2025 (pico)", "amber")
                + _gauge_bar(70.0, "Meta mandato", "green"),
                unsafe_allow_html=True,
            )

            st.markdown(f"""
<div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap">
  <div style="background:rgba(0,224,150,.08);border:1px solid rgba(0,224,150,.25);
              border-radius:9px;padding:10px 14px;flex:1;text-align:center">
    <div style="font-size:20px;font-weight:900;color:var(--{'green' if delta_vs_base>=0 else 'red'})">
      {'+' if delta_vs_base>=0 else ''}{delta_vs_base:.2f} pts
    </div>
    <div style="font-size:9px;color:rgba(255,255,255,.4);margin-top:2px">vs ene–mar 2026</div>
  </div>
  <div style="background:rgba(255,184,0,.07);border:1px solid rgba(255,184,0,.25);
              border-radius:9px;padding:10px 14px;flex:1;text-align:center">
    <div style="font-size:20px;font-weight:900;color:var(--{'green' if delta_vs_meta>=0 else 'amber'})">
      {'+' if delta_vs_meta>=0 else ''}{delta_vs_meta:.2f} pts
    </div>
    <div style="font-size:9px;color:rgba(255,255,255,.4);margin-top:2px">vs meta 70%</div>
  </div>
</div>
""", unsafe_allow_html=True)

            if score_proj >= 70:
                st.success("🎯 ¡Gestión por Mandato alcanzada! Con estas mejoras el GAD supera la meta al cierre 2026.")
            elif score_proj >= 65:
                st.warning(f"🟡 Cerca de la meta. Quedan {_META_MANDATO - score_proj:.2f} pts para Gestión por Mandato.")
            elif score_proj > _SCORE_BASE:
                st.info("📈 Mejora real vs ene–mar 2026. Continúa ajustando los vectores de mayor impacto para maximizar el avance.")
            else:
                st.error("⚠️ Sin cambios. Mueve los sliders para simular mejoras.")

        # Escenarios predefinidos
        st.markdown("---")
        st.markdown('<div class="sim-label">⚡ ESCENARIOS RÁPIDOS</div>', unsafe_allow_html=True)
        sc1, sc2, sc3, sc4 = st.columns(4)
        escenarios = [
            ("🔴 Solo Presupuesto", {"isp": 65.0},                              "Resuelves deuda tributaria"),
            ("⚡ Presup. + Eficiencia", {"isp": 65.0, "ied": 60.0},             "Mejora presupuesto y cadena PAC"),
            ("🎯 Meta Q3-2026", {"isp": 45.0, "ied": 55.0, "igp": 45.0, "psg": 22.0}, "Escenario realista Q3"),
            ("✨ Todos al 80%", {v["key"]: min(v["meta"], v["actual"]+(v["meta"]-v["actual"])*0.8)
                                  for v in _VECTORES},                            "Mejora ambiciosa"),
        ]
        for col, (label, vals, desc) in zip([sc1, sc2, sc3, sc4], escenarios):
            proj = _calcular_icgit({**{v["key"]: v["actual"] for v in _VECTORES}, **vals})
            avep_l, avep_c = _avep_label(proj)
            col_hex = {"green": "#00E096", "amber": "#FFB800", "red": "#FF4D6D"}[avep_c]
            with col:
                st.markdown(f"""
<div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
            border-radius:10px;padding:14px;text-align:center;height:130px;
            display:flex;flex-direction:column;justify-content:space-between">
  <div style="font-size:11px;font-weight:700;color:#E2E8F0">{label}</div>
  <div style="font-size:28px;font-weight:900;color:{col_hex};font-family:monospace">{proj:.1f}%</div>
  <div style="font-size:9px;color:rgba(255,255,255,.4)">{desc}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        mejoras_txt = ", ".join(
            f"{v['codigo']} {mejoras.get(v['key'], v['actual']):.1f}%"
            for v in _VECTORES if mejoras.get(v['key'], v['actual']) > v['actual'] + 0.1
        ) or "ninguna mejora aún"
        with c1:
            if st.button("🔮 Sentinel · Validar este escenario",
                         use_container_width=True, type="primary"):
                st.session_state["page"] = "sentinel"
                st.session_state["sentinel_pregunta_auto"] = (
                    f"Estoy simulando un escenario donde el GAD de Montecristi mejora: {mejoras_txt}. "
                    f"El modelo proyecta una calificación de gestión de {score_proj:.2f}% ({avep_label}). "
                    f"¿Es este escenario realista en el plazo Q2-Q3 2026? "
                    f"¿Qué obstáculos concretos debo anticipar para alcanzarlo?"
                )
                st.rerun()
        with c2:
            if st.button("📉 Ver Causas de la Brecha", use_container_width=True):
                st.session_state["page"] = "brecha"
                st.rerun()
        with c3:
            if st.button("🚨 Ver Señales de Alerta", use_container_width=True):
                st.session_state["page"] = "sat"
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — IRS SENSITIVITY ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown("""
<div style="margin-bottom:20px">
  <div style="font-size:11px;font-weight:700;color:#FF4D6D;
              text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px">
    🔴 REGRESIVIDAD DE LA INVERSIÓN · ANÁLISIS DE SENSIBILIDAD
  </div>
  <div style="font-size:20px;font-weight:900;color:#F0F4FF;margin-bottom:6px">
    ¿Cómo cambia la regresividad de la inversión al variar los pesos?
  </div>
  <div style="font-size:11px;color:rgba(255,255,255,0.45)">
    La regresividad mide si la inversión pública llega a donde más se necesita,
    ponderando <strong style="color:#FF4D6D">acceso a agua</strong>,
    <strong style="color:#FF4D6D">necesidades básicas insatisfechas</strong> y
    <strong style="color:#FF4D6D">población</strong> · A mayor regresividad,
    mayor inequidad territorial en el reparto del presupuesto.
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Tabla de escenarios + chart ───────────────────────────────────────
        col_t, col_c = st.columns([3, 2], gap="large")

        with col_t:
            st.markdown('<div class="sim-label">TABLA DE SENSIBILIDAD · 6 ESCENARIOS VALIDADOS</div>',
                        unsafe_allow_html=True)
            rows_html = ""
            for s in _IRS_ESCENARIOS:
                irs_col = "#00E096" if s["irs"] < 75 else ("#FFB800" if s["irs"] < 80 else "#FF4D6D")
                rec_badge = ('<span style="font-size:8px;background:rgba(0,212,255,.15);'
                             'color:#00D4FF;border-radius:4px;padding:1px 5px;margin-left:4px">'
                             'OFICIAL</span>') if s["rec"] else ""
                bg = "rgba(0,212,255,.06)" if s["rec"] else "rgba(255,255,255,.02)"
                border = "1px solid rgba(0,212,255,.3)" if s["rec"] else "1px solid rgba(255,255,255,.07)"
                rows_html += f"""
<div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1.2fr;
            gap:8px;padding:8px 10px;background:{bg};border:{border};
            border-radius:7px;margin-bottom:4px;align-items:center">
  <div style="font-size:10px;font-weight:700;color:#E2E8F0">
    {s["label"]}{rec_badge}
  </div>
  <div style="font-size:10px;color:rgba(255,255,255,.5);text-align:center">
    <div style="font-size:8px;color:rgba(255,255,255,.3)">Agua</div>
    {s["w_agua"]}%
  </div>
  <div style="font-size:10px;color:rgba(255,255,255,.5);text-align:center">
    <div style="font-size:8px;color:rgba(255,255,255,.3)">NBI</div>
    {s["w_nbi"]}%
  </div>
  <div style="font-size:10px;color:rgba(255,255,255,.5);text-align:center">
    <div style="font-size:8px;color:rgba(255,255,255,.3)">Pob</div>
    {s["w_pop"]}%
  </div>
  <div style="font-size:14px;font-weight:900;color:{irs_col};text-align:right;
              font-family:monospace">
    {s["irs"]}
  </div>
</div>"""
            st.markdown(rows_html, unsafe_allow_html=True)
            st.markdown("""
<div style="margin-top:8px;padding:8px 10px;background:rgba(255,77,109,.05);
            border:1px solid rgba(255,77,109,.2);border-radius:7px;
            font-size:9px;color:rgba(255,255,255,.4);line-height:1.7">
  Fuente: Análisis de sensibilidad territorial · 7 parroquias Montecristi
  · En todos los escenarios la regresividad es ≥71.8% → zona <strong style="color:#FF4D6D">Muy Regresivo</strong>
  · La inversión pública NO llega proporcionalmente a donde más se necesita
</div>
""", unsafe_allow_html=True)

        with col_c:
            try:
                import plotly.graph_objects as go
                nbi_pesos  = [s["w_nbi"] for s in _IRS_ESCENARIOS]
                irs_vals   = [s["irs"]   for s in _IRS_ESCENARIOS]
                rec_colors = ["#00D4FF" if s["rec"] else "#FF4D6D" for s in _IRS_ESCENARIOS]
                rec_sizes  = [14 if s["rec"] else 8 for s in _IRS_ESCENARIOS]

                # Smooth curve (interpolated)
                nbi_range = list(range(10, 61))
                irs_curve = [_irs_interpolado(n) for n in nbi_range]

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=nbi_range, y=irs_curve,
                    mode="lines",
                    line=dict(color="rgba(255,77,109,0.4)", width=2, dash="dot"),
                    showlegend=False, name="Interpolado",
                ))
                fig.add_trace(go.Scatter(
                    x=nbi_pesos, y=irs_vals,
                    mode="markers+text",
                    marker=dict(size=rec_sizes, color=rec_colors,
                                line=dict(width=1, color="#1A2942")),
                    text=[f"{v:.1f}" for v in irs_vals],
                    textposition="top center",
                    textfont=dict(size=9, color="#E2E8F0"),
                    showlegend=False, name="Escenarios",
                ))
                fig.add_annotation(
                    x=30, y=79.7,
                    text="★ Escenario<br>Recomendado",
                    showarrow=True,
                    arrowhead=2, arrowcolor="#00D4FF", arrowwidth=1.5,
                    font=dict(size=9, color="#00D4FF"),
                    ax=40, ay=-30,
                )
                fig.update_layout(
                    title=dict(text="Regresividad vs Peso NBI (%)", font=dict(size=11, color="#9BA3B2"), x=0),
                    xaxis=dict(title="Peso NBI (%)", color="#9BA3B2",
                               gridcolor="rgba(255,255,255,0.05)", range=[8, 58]),
                    yaxis=dict(title="Regresividad", color="#9BA3B2",
                               gridcolor="rgba(255,255,255,0.05)", range=[68, 86]),
                    plot_bgcolor="#0D1B2F",
                    paper_bgcolor="#0D1B2F",
                    margin=dict(l=40, r=20, t=40, b=40),
                    height=280,
                    font=dict(color="#9BA3B2"),
                )
                fig.add_hrect(y0=70, y1=86, fillcolor="rgba(255,77,109,0.06)",
                              line_width=0, annotation_text="Muy Regresivo",
                              annotation_font=dict(size=8, color="rgba(255,77,109,0.5)"),
                              annotation_position="top left")
                st.plotly_chart(fig, use_container_width=True)
            except ImportError:
                st.info("Instalar plotly para ver el gráfico: `pip install plotly`")

        # ── 6 Escenarios validados — Gold Master trazabilidad ─────────────────
        st.markdown("---")
        st.markdown("""
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
  <div>
    <div style="font-size:11px;font-weight:700;color:#FF4D6D;
                text-transform:uppercase;letter-spacing:.1em">
      📋 ANÁLISIS DE SENSIBILIDAD · 6 ESCENARIOS VALIDADOS
    </div>
    <div style="font-size:9px;color:rgba(255,255,255,0.35);margin-top:3px">
      Fuente: Análisis de necesidades territoriales · Trazabilidad verificada
    </div>
  </div>
  <div style="background:rgba(0,212,255,0.08);border:1px solid rgba(0,212,255,0.3);
              border-radius:8px;padding:8px 14px;text-align:center">
    <div style="font-size:9px;color:rgba(0,212,255,0.7);font-weight:700">REGRESIVIDAD OFICIAL</div>
    <div style="font-size:28px;font-weight:900;color:#FF4D6D;font-family:monospace;line-height:1.1">79.7</div>
    <div style="font-size:8px;color:rgba(255,255,255,0.4)">★ Escenario recomendado</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Grid de 6 escenarios en 3 columnas
        cols_esc = st.columns(3)
        _COL_HEX = {"red": "#FF4D6D", "amber": "#FFB800", "green": "#00E096"}
        for i, esc in enumerate(_IRS_ESCENARIOS):
            irs_label, irs_col = _avep_irs(esc["irs"])
            hex_color = _COL_HEX[irs_col]
            is_rec    = esc["rec"]
            border    = "rgba(0,212,255,0.50)" if is_rec else "rgba(255,255,255,0.07)"
            bg        = "rgba(0,212,255,0.07)" if is_rec else "rgba(255,255,255,0.02)"
            badge     = '<div style="font-size:8px;font-weight:700;color:#00D4FF;margin-bottom:4px">✦ OFICIAL · USE EN REPORTES</div>' if is_rec else ""
            with cols_esc[i % 3]:
                st.markdown(f"""
<div style="border:1px solid {border};background:{bg};border-radius:10px;
            padding:12px 10px;margin-bottom:8px;text-align:center">
  {badge}
  <div style="font-size:10px;font-weight:700;color:rgba(255,255,255,0.8);margin-bottom:6px">{esc['label']}</div>
  <div style="font-size:32px;font-weight:900;color:{hex_color};font-family:monospace;line-height:1">{esc['irs']}</div>
  <div style="font-size:9px;font-weight:700;color:{hex_color};margin:4px 0">{irs_label}</div>
  <div style="font-size:8px;color:rgba(255,255,255,0.3);margin-top:6px">
    Agua {esc['w_agua']}% · NBI {esc['w_nbi']}% · Pob {esc['w_pop']}%
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown("""
<div style="background:rgba(0,212,255,.05);border:1px solid rgba(0,212,255,.12);
            border-radius:8px;padding:8px 12px;font-size:9px;color:rgba(255,255,255,.4);margin-top:4px">
  🔒 Los pesos de ponderación son parámetros validados del modelo territorial QUIRA.
  El índice de regresividad oficial para reportes externos, solicitudes PNUD/BID/GEF y evidencia institucional es
  <strong style="color:#00D4FF">79.7 pts · Escenario recomendado</strong>.
</div>
""", unsafe_allow_html=True)

        # ── Conclusiones del análisis de sensibilidad ─────────────────────────
        st.markdown("""
<div style="background:rgba(255,77,109,.05);border:1px solid rgba(255,77,109,.2);
            border-radius:12px;padding:14px 16px;margin-top:12px">
  <div style="font-size:11px;font-weight:700;color:#FF4D6D;margin-bottom:8px">
    📋 CONCLUSIONES DEL ANÁLISIS DE SENSIBILIDAD
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px">
    <div style="font-size:10px;color:rgba(255,255,255,.7);line-height:1.6;
                padding:8px;background:rgba(255,255,255,.02);border-radius:6px">
      <strong style="color:#FF4D6D">NBI es el indicador más duro.</strong>
      A mayor peso NBI → mayor regresividad → más inequidad detectada.
      Rango realista: 71.8–82.1 pts.
    </div>
    <div style="font-size:10px;color:rgba(255,255,255,.7);line-height:1.6;
                padding:8px;background:rgba(255,255,255,.02);border-radius:6px">
      <strong style="color:#00D4FF">En todos los escenarios</strong>
      el GAD está en zona <strong>Muy Regresivo</strong> (regresividad > 70).
      Argumento institucional para PNUD, BID, GEF.
    </div>
    <div style="font-size:10px;color:rgba(255,255,255,.7);line-height:1.6;
                padding:8px;background:rgba(255,255,255,.02);border-radius:6px">
      <strong style="color:#FFB800">Peso recomendado (50/30/20)</strong>
      es el más equilibrado y defendible ante Contraloría.
      Certificado de validación territorial QUIRA.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔮 Sentinel · Estrategia de equidad de inversión + cooperantes",
                         use_container_width=True, type="primary", key="sent_irs"):
                st.session_state["page"] = "sentinel"
                st.session_state["sentinel_pregunta_auto"] = (
                    "El índice de regresividad de la inversión de Montecristi es 79.7% (Muy Regresivo) "
                    "con ponderación Agua=50%, NBI=30%, Población=20%. Esto significa que la inversión pública "
                    "NO llega proporcionalmente a donde más se necesita. "
                    "¿Cómo presento este indicador ante PNUD, BID Lab y GEF para fortalecer "
                    "la solicitud de fondos? ¿Qué acciones concretas en Q2-Q3 2026 reducen la regresividad "
                    "de 79.7% a menos de 65%?"
                )
                st.rerun()
        with c2:
            if st.button("🗺️ Ver Territorio Digital", use_container_width=True, key="geo_irs"):
                st.session_state["page"] = "geotwin"
                st.rerun()
        with c3:
            if st.button("💜 Ver Género y Equidad", use_container_width=True, key="gen_irs"):
                st.session_state["page"] = "genero"
                st.rerun()
