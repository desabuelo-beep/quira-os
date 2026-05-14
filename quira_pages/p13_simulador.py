"""
QUIRA OS v0.1 — P-13 Simulador de Escenarios
¿Qué ICGI-T logramos si mejoramos X? · Motor de escenarios interactivo
Dylus Lab © 2026
"""
import streamlit as st
from data.loader import load_all
from utils.session import is_tecnico

# ── MODELO SIMPLIFICADO ICGI-T ────────────────────────────────────────────────
# Pesos derivados del SIAP-ICPI v1.0222 (suma ≈ 1.0)
_VECTORES = [
    {
        "key":     "isp",
        "codigo":  "ISP",
        "nombre":  "Salud Presupuestaria",
        "actual":  14.58,
        "meta":    65.0,
        "peso":    0.22,     # peso en el ICGI-T
        "impacto": -8.2,     # pts ICGI-T perdidos Q1-2026
        "color":   "🔴",
        "accion":  "Activar coactivas + catastro predial",
    },
    {
        "key":     "ied",
        "codigo":  "IED",
        "nombre":  "Eficiencia Direcciones",
        "actual":  33.99,
        "meta":    70.0,
        "peso":    0.18,
        "impacto": -6.8,
        "color":   "🔴",
        "accion":  "Publicar evidencias PAC · regularizar SAT-0",
    },
    {
        "key":     "igp",
        "codigo":  "IGP",
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
        "codigo":  "IOC",
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
        "codigo":  "IET",
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
        "codigo":  "PSG",
        "nombre":  "Presupuesto de Género",
        "actual":  12.83,
        "meta":    30.0,
        "peso":    0.08,
        "impacto": -2.4,
        "color":   "🟡",
        "accion":  "Reclasificar programas género en POA-Q2",
    },
]

_SCORE_BASE  = 53.56   # ICGI-T Q1-2026
_SCORE_2025  = 69.93   # pico 2025
_META_MANDATO = 70.0


def _calcular_icgit(mejoras: dict) -> float:
    """
    Calcula el ICGI-T proyectado dado un dict {key: nuevo_valor}.
    Modelo lineal: cada punto de mejora en el vector genera
    (mejora_pts / rango_vector) * peso * 100 puntos de ICGI-T.
    """
    score = _SCORE_BASE
    for v in _VECTORES:
        nuevo = mejoras.get(v["key"], v["actual"])
        delta = nuevo - v["actual"]   # cuánto mejora el vector
        rango = v["meta"] - v["actual"]
        if rango > 0 and delta > 0:
            fraccion = min(delta / rango, 1.0)
            score += fraccion * abs(v["impacto"])
    return min(score, 100.0)


def _avep_label(s: float) -> tuple[str, str]:
    if s >= 85:
        return "Excelencia Institucional", "green"
    if s >= 70:
        return "Gestión por Mandato", "green"
    if s >= 50:
        return "Transición Crítica", "amber"
    if s >= 30:
        return "Gestión por Ocurrencia", "red"
    return "Ruptura Sistémica", "red"


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


def render() -> None:
    load_all()   # caché warm-up
    is_tecnico()

    # ── HEADER NATIVO ─────────────────────────────────────────────────────────
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
<div style="margin-bottom:20px">
  <div style="font-size:11px;font-weight:700;color:#00D4FF;
              text-transform:uppercase;letter-spacing:.12em;margin-bottom:4px">
    ⑨ SIMULADOR DE ESCENARIOS
  </div>
  <div style="font-size:22px;font-weight:900;color:#F0F4FF;margin-bottom:6px">
    ¿Qué ICGI-T logramos si mejoramos X?
  </div>
  <div style="font-size:11px;color:rgba(255,255,255,0.45)">
    Mueve los sliders para simular el impacto de cada vector sobre el ICGI-T proyectado
    · Modelo SIAP-ICPI v1.0222 · Base Q1-2026
  </div>
</div>
""", unsafe_allow_html=True)

    # ── LAYOUT: sliders izquierda · resultado derecha ─────────────────────────
    col_sliders, col_resultado = st.columns([3, 2], gap="large")

    mejoras = {}

    with col_sliders:
        st.markdown('<div class="sim-label">VECTORES DE MEJORA · MUEVE LOS SLIDERS</div>',
                    unsafe_allow_html=True)

        for v in _VECTORES:
            st.markdown(
                f'<div style="font-size:11px;font-weight:700;color:#E2E8F0;margin-bottom:2px">'
                f'{v["color"]} {v["codigo"]} · {v["nombre"]}</div>'
                f'<div style="font-size:9px;color:rgba(255,255,255,.4);margin-bottom:4px">'
                f'Actual: {v["actual"]:.1f}% · Meta: {v["meta"]:.0f}% · '
                f'Impacto base: {v["impacto"]:.1f} pts</div>',
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
                    f'▲ +{ganancia:.1f} pts en {v["codigo"]} '
                    f'→ contribuye al ICGI-T</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown('<div style="margin-bottom:12px"></div>',
                            unsafe_allow_html=True)

    with col_resultado:
        score_proj = _calcular_icgit(mejoras)
        avep_label, avep_col = _avep_label(score_proj)
        delta_vs_base = score_proj - _SCORE_BASE
        delta_vs_meta = score_proj - _META_MANDATO

        col_score_hex = {
            "green": "#00E096",
            "amber": "#FFB800",
            "red":   "#FF4D6D",
        }[avep_col]

        st.markdown(f"""
<div class="sim-card" style="border-top:3px solid {col_score_hex}">
  <div class="sim-label">ICGI-T PROYECTADO</div>
  <div class="sim-score" style="color:{col_score_hex}">{score_proj:.2f}<span style="font-size:28px">%</span></div>
  <div class="sim-avep" style="color:{col_score_hex}">{avep_label}</div>
</div>
""", unsafe_allow_html=True)

        # Comparativas
        st.markdown('<div class="sim-label" style="margin-top:8px">COMPARATIVAS</div>',
                    unsafe_allow_html=True)
        st.markdown(
            _gauge_bar(_SCORE_BASE, "Q1-2026 (base)", "red")
            + _gauge_bar(score_proj,  f"Proyectado ({avep_label[:10]})", avep_col)
            + _gauge_bar(69.93,       "2025 (pico)",  "amber")
            + _gauge_bar(70.0,        "Meta mandato", "green"),
            unsafe_allow_html=True,
        )

        # Delta badge
        delta_col = "green" if delta_vs_base >= 0 else "red"
        st.markdown(f"""
<div style="margin-top:14px;display:flex;gap:10px;flex-wrap:wrap">
  <div style="background:rgba(0,224,150,.08);border:1px solid rgba(0,224,150,.25);
              border-radius:9px;padding:10px 14px;flex:1;text-align:center">
    <div style="font-size:20px;font-weight:900;color:var(--{'green' if delta_vs_base>=0 else 'red'})">
      {'+' if delta_vs_base>=0 else ''}{delta_vs_base:.2f} pts
    </div>
    <div style="font-size:9px;color:rgba(255,255,255,.4);margin-top:2px">vs Q1-2026</div>
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

        # Mensaje contextual
        if score_proj >= 70:
            st.success(f"🎯 ¡Gestión por Mandato alcanzada! Con estas mejoras el GAD supera la meta al cierre 2026.")
        elif score_proj >= 65:
            st.warning(f"🟡 Cerca de la meta. Quedan {_META_MANDATO - score_proj:.2f} pts para Gestión por Mandato.")
        elif score_proj > _SCORE_BASE:
            st.info(f"📈 Mejora real vs Q1-2026. Continúa ajustando los vectores de mayor peso (ISP, IED).")
        else:
            st.error("⚠️ Sin cambios. Mueve los sliders para simular mejoras.")

    # ── ESCENARIOS PREDEFINIDOS ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="sim-label">⚡ ESCENARIOS RÁPIDOS</div>',
                unsafe_allow_html=True)

    sc1, sc2, sc3, sc4 = st.columns(4)

    escenarios = [
        ("🔴 Solo ISP",         {"isp": 65.0}, "Resuelves deuda tributaria · ISP al 65%"),
        ("⚡ ISP + IED",        {"isp": 65.0, "ied": 60.0}, "ISP + regularizas cadena PAC"),
        ("🎯 Meta Q3-2026",     {"isp": 45.0, "ied": 55.0, "igp": 45.0, "psg": 22.0},
         "Escenario realista Q3-2026"),
        ("✨ Todos al 80%",     {v["key"]: min(v["meta"], v["actual"] + (v["meta"]-v["actual"])*0.8)
                                 for v in _VECTORES}, "Mejora ambiciosa todos los vectores"),
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
  <div style="font-size:28px;font-weight:900;color:{col_hex};
              font-family:monospace">{proj:.1f}%</div>
  <div style="font-size:9px;color:rgba(255,255,255,.4)">{desc}</div>
</div>
""", unsafe_allow_html=True)

    # ── CTA SENTINEL ──────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2, c3 = st.columns(3)

    # Construir contexto dinámico con los valores actuales de los sliders
    mejoras_txt = ", ".join(
        f"{v['codigo']} {mejoras.get(v['key'], v['actual']):.1f}%"
        for v in _VECTORES
        if mejoras.get(v['key'], v['actual']) > v['actual'] + 0.1
    ) or "ninguna mejora aún"

    with c1:
        if st.button("🔮 Sentinel · Validar este escenario",
                     use_container_width=True, type="primary"):
            st.session_state["page"] = "sentinel"
            st.session_state["sentinel_pregunta_auto"] = (
                f"Estoy simulando un escenario donde el GAD de Montecristi mejora: {mejoras_txt}. "
                f"El modelo proyecta un ICGI-T de {score_proj:.2f}% ({avep_label}). "
                f"¿Es este escenario realista en el plazo Q2-Q3 2026? "
                f"¿Qué obstáculos concretos debo anticipar para alcanzarlo?"
            )
            st.rerun()
    with c2:
        if st.button("📉 Ver Causas de la Brecha", use_container_width=True):
            st.session_state["page"] = "brecha"
            st.rerun()
    with c3:
        if st.button("🚨 Ver Alertas SAT", use_container_width=True):
            st.session_state["page"] = "sat"
            st.rerun()
