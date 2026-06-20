"""
QUIRA Intelligence — Dom10 Territorio & Cobertura  (Layer 2 · Sprint 3)
Módulo ejecutivo para el Dominio 10 — Agua Potable y Cobertura Territorial.

ADR-013 (2026-05-31) — QTMP circuit AGUA_POTABLE → Dom10.
Lenguaje de gobernanza pública. Sin nomenclatura interna.

Bloomberg Model:
  ✗ NUNCA exponer: AGUA_POTABLE, IND_AGPT_01_MCR, RES_AGPT_01_MCR, fuente_neo4j, circuit_id
  ✓ SOLO exponer: narrativa, fuente, valor_principal, indicador_label, semaforo, fecha_corte

Estructura Layer 2 canónica:
  1. Semáforo y KPI principal (cobertura de agua potable por red pública)
  2. Narrativa causal (CE Art. 264 — competencia exclusiva municipal)
  3. Indicadores clave: cobertura · continuidad 24/7 · meta PDOT 2027
  4. Visualización: barra de progreso + barras comparativas
  5. Pie de página con fuente pública

Dylus Lab © 2026 — DOCUMENTO INTERNO · QUIRA Operaciones
"""
from __future__ import annotations

import streamlit as st
from utils.session import is_ejecutivo

# ── Paleta de semáforo canónica ──────────────────────────────────────────────
_VERDE   = "#22C55E"
_ALERTA  = "#F97316"
_CRITICO = "#EF4444"
_MUTED   = "rgba(255,255,255,0.45)"


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTES CANÓNICOS — reutilizables en todos los Layer 2
# ══════════════════════════════════════════════════════════════════════════════

def _render_return_band() -> None:
    """Banda superior de retorno al Centro de Mando — solo para Ejecutivo."""
    if is_ejecutivo():
        col1, _col2 = st.columns([1, 7])
        with col1:
            if st.button("← Centro de Mando", key="back_to_cc_d10"):
                st.session_state["gov_module"] = "inicio"
                st.rerun()


def _semaforo_color(semaforo: str) -> str:
    m = {"VERDE": _VERDE, "AMARILLO": _ALERTA, "ROJO": _CRITICO}
    return m.get(semaforo, _MUTED)


def _semaforo_label(semaforo: str) -> str:
    m = {
        "VERDE":    "EN RUTA",
        "AMARILLO": "BAJO OBJETIVO",
        "ROJO":     "BRECHA CRÍTICA",
        "PENDIENTE":"EN MODELADO",
    }
    return m.get(semaforo, semaforo)


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2 CANÓNICO — Dom10 Territorio & Cobertura
# ══════════════════════════════════════════════════════════════════════════════

def _render_dom10_ejecutivo(chain: dict) -> None:
    """
    Layer 2 canónico — Dom10 Territorio & Cobertura.
    Solo lenguaje de gobernanza pública. Sin nomenclatura interna.

    Estructura:
      1. Semáforo y KPI principal (cobertura de agua potable)
      2. Narrativa causal (CE 264 — competencia exclusiva)
      3. Indicadores clave: cobertura · continuidad · meta PDOT 2027
      4. Visualización: barra de progreso + barras comparativas
      5. Pie de página con fuente pública
    """
    # ── Extraer campos públicos del chain ─────────────────────────────────────
    sem            = chain.get("semaforo", "ROJO")
    color          = _semaforo_color(sem)
    label          = _semaforo_label(sem)
    valor          = chain.get("valor_principal", 34.9)
    ind_label      = chain.get("indicador_label", "Cobertura de agua potable por red pública")
    fuente         = chain.get("fuente", "INEC Censo de Población y Vivienda 2022")
    corte          = chain.get("fecha_corte", "2022")
    narrativa      = chain.get("narrativa", "")
    estado         = chain.get("estado_dato", "confirmado")
    continuidad    = chain.get("continuidad_pct", 0.0)
    sem_cont       = chain.get("continuidad_semaforo", "ROJO")
    meta_pdot      = chain.get("meta_pdot_2027", 42.38)
    linea_base     = chain.get("linea_base_pdot", 39.25)
    umbral         = chain.get("umbral_verde", 90.0)
    fuente_neo4j   = chain.get("fuente_neo4j", False)   # INTERNO — no exponer en UI text

    # ── Cabecera de dominio ───────────────────────────────────────────────────
    st.markdown(
        f"<div style='font-size:11px;color:{_MUTED};letter-spacing:2px;"
        f"text-transform:uppercase;margin-bottom:4px'>D10 · TERRITORIO & COBERTURA</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:20px;font-weight:700;color:white;margin-bottom:16px'>"
        "Territorio &amp; Cobertura de Servicios Públicos</div>",
        unsafe_allow_html=True,
    )

    # ── Sección 1: Semáforo y KPI principal ──────────────────────────────────
    badge_asterisco = " *" if estado != "confirmado" else ""
    st.markdown(
        f"""<div style="background:{color}18;border:1px solid {color}44;
                     border-left:4px solid {color};border-radius:10px;
                     padding:16px 20px;margin-bottom:16px">
  <div style="font-size:2.8rem;font-weight:900;color:{color};
              font-family:monospace;line-height:1">{valor:.1f}%{badge_asterisco}</div>
  <div style="font-size:0.75rem;font-weight:700;color:{color};
              letter-spacing:1px;margin-top:6px">{label}</div>
  <div style="font-size:0.8rem;color:rgba(255,255,255,0.7);margin-top:6px">
    {ind_label}
  </div>
</div>""",
        unsafe_allow_html=True,
    )

    if estado != "confirmado":
        st.caption(f"* Pendiente confirmación oficial · {fuente}")

    # ── Sección 2: Narrativa causal ───────────────────────────────────────────
    if narrativa:
        st.markdown(
            f"""<div style="background:rgba(255,255,255,0.04);border-radius:10px;
                         padding:14px 18px;margin-bottom:16px;
                         border:1px solid rgba(255,255,255,0.08);
                         font-size:0.88rem;color:rgba(255,255,255,0.82);
                         line-height:1.7">{narrativa}</div>""",
            unsafe_allow_html=True,
        )

    # ── Sección 3: Indicadores clave ─────────────────────────────────────────
    col_a, col_b, col_c = st.columns(3)

    color_cobertura = _semaforo_color(sem)
    color_cont      = _semaforo_color(sem_cont)
    # Meta PDOT es informativa — color neutral (entre línea base y umbral)
    color_meta      = _semaforo_color("AMARILLO")

    with col_a:
        st.markdown(
            f"""<div style="background:{color_cobertura}15;border:1px solid {color_cobertura}33;
                         border-radius:8px;padding:14px;text-align:center">
  <div style="font-size:1.8rem;font-weight:900;color:{color_cobertura};
              font-family:monospace">{valor:.1f}%</div>
  <div style="font-size:0.68rem;color:{color_cobertura};font-weight:700;margin-top:4px">
    BRECHA CRÍTICA
  </div>
  <div style="font-size:0.65rem;color:{_MUTED};margin-top:3px;line-height:1.4">
    Cobertura red pública<br>agua potable · Censo 2022
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""<div style="background:{color_cont}15;border:1px solid {color_cont}33;
                         border-radius:8px;padding:14px;text-align:center">
  <div style="font-size:1.8rem;font-weight:900;color:{color_cont};
              font-family:monospace">{continuidad:.0f}%</div>
  <div style="font-size:0.68rem;color:{color_cont};font-weight:700;margin-top:4px">
    SIN CONTINUIDAD
  </div>
  <div style="font-size:0.65rem;color:{_MUTED};margin-top:3px;line-height:1.4">
    Servicio continuo 24/7<br>en ninguna parroquia
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            f"""<div style="background:{color_meta}15;border:1px solid {color_meta}33;
                         border-radius:8px;padding:14px;text-align:center">
  <div style="font-size:1.8rem;font-weight:900;color:{color_meta};
              font-family:monospace">{meta_pdot:.1f}%</div>
  <div style="font-size:0.68rem;color:{color_meta};font-weight:700;margin-top:4px">
    META PDOT 2027
  </div>
  <div style="font-size:0.65rem;color:{_MUTED};margin-top:3px;line-height:1.4">
    Objetivo plan territorial<br>Bicentenario 2023-2027
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Sección 4: Visualización ──────────────────────────────────────────────

    # Barra de progreso — cobertura actual vs umbral de referencia
    st.markdown(
        f"""<div style="margin-bottom:16px">
  <div style="font-size:0.75rem;color:{_MUTED};margin-bottom:6px;
              font-weight:600;letter-spacing:1px">COBERTURA ACTUAL VS UMBRAL DE REFERENCIA</div>
  <div style="position:relative;height:10px;background:rgba(255,255,255,0.1);
              border-radius:6px;overflow:hidden;margin-bottom:4px">
    <div style="position:absolute;height:100%;width:{valor:.1f}%;
                background:{color};border-radius:6px;
                transition:width 0.5s ease"></div>
    <div style="position:absolute;height:100%;left:{umbral:.0f}%;
                width:2px;background:{_VERDE};opacity:0.7"></div>
  </div>
  <div style="display:flex;justify-content:space-between;font-size:0.7rem;
              color:{_MUTED}">
    <span>0%</span>
    <span style="color:{_VERDE}">▲ Umbral {umbral:.0f}%</span>
    <span>100%</span>
  </div>
</div>""",
        unsafe_allow_html=True,
    )

    # Barras comparativas — línea base / cobertura actual / meta PDOT
    puntos = [
        (linea_base, "Línea Base\n2023",  _CRITICO),
        (valor,       "Cobertura\nActual", _CRITICO),
        (meta_pdot,   "Meta PDOT\n2027",  _ALERTA),
        (umbral,      "Umbral\nReferencia",_VERDE),
    ]
    max_v = max(v for v, _, _ in puntos)
    bars  = ""
    for v, etiqueta, c in puntos:
        h = (v / max_v) * 60
        etiqueta_html = etiqueta.replace("\n", "<br>")
        bars += (
            f"<div style='display:flex;flex-direction:column;align-items:center;gap:4px'>"
            f"<div style='font-size:0.75rem;color:{c};font-weight:700'>{v:.1f}%</div>"
            f"<div style='width:44px;height:{h:.0f}px;background:{c};border-radius:4px 4px 0 0'></div>"
            f"<div style='font-size:0.62rem;color:{_MUTED};text-align:center;line-height:1.3'>"
            f"{etiqueta_html}</div>"
            f"</div>"
        )

    st.markdown(
        f"""<div style="margin-bottom:20px">
  <div style="font-size:0.75rem;color:{_MUTED};margin-bottom:10px;
              font-weight:600;letter-spacing:1px">ESCENARIOS DE COBERTURA</div>
  <div style="display:flex;gap:28px;align-items:flex-end;height:90px">{bars}</div>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Sección 5: Pie de página ──────────────────────────────────────────────
    fuente_badge = "🔴 Datos en vivo" if fuente_neo4j else "📋 Datos consolidados"
    st.caption(f"{fuente_badge} · Fuente: {fuente} · Corte: {corte}")


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT — llamado desde env_gov.py · _render_territorio()
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Layer 2 — Territorio & Cobertura de Servicios Públicos
    Dominio D10 · Sprint 3 Panel Estratégico · ADR-013

    Todos los roles → vista canónica QTMP (cobertura agua potable).
    El GeoTwin con mapa Folium (p4_geotwin.py) sigue siendo Técnico.
    """
    from app.connectors.neo4j_qtmp import get_qtmp_chain
    _render_return_band()

    chain = get_qtmp_chain("AGUA_POTABLE")
    if chain:
        _render_dom10_ejecutivo(chain)
    else:
        st.error("Datos del dominio no disponibles. Intente nuevamente.")
