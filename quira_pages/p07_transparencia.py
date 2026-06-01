"""
QUIRA Intelligence — Dom07 Transparencia  (Layer 2 · Sprint 4)
Módulo ejecutivo para el Dominio 7 — Transparencia e Información Pública.

ADR-013 (2026-05-31) + ADR-014 (2026-06-01) — QTMP circuit TRANSPARENCIA → Dom07.
QNKC-P01 Dualidad Epistémica: C4 (Cumplimiento Formal) × C5 (Verificabilidad Efectiva).
OBS-QNKC-01: verificabilidad_efectiva = C5a (Existencia) × C5b (Actualidad) × C5c (Inteligibilidad).

Bloomberg Model:
  ✗ NUNCA exponer: TRANSPARENCIA, IND_TRANS_01_MCR, H41_IOC, circuit_id, fuente_neo4j
  ✓ SOLO exponer: narrativa, fuente, valor_principal, indicador_label, semaforo, fecha_corte

Estructura Layer 2 canónica — Dom07:
  1. Semáforo y KPI principal (cumplimiento integral publicación institucional)
  2. Narrativa causal (CE Art. 18 — derecho a la información)
  3. Dualidad Epistémica QNKC-P01:
       C4  — Cumplimiento Formal   (¿el municipio publicó?)
       C5  — Verificabilidad Efectiva = C5a × C5b × C5c
  4. Fórmula C8 = C4 × (C5a × C5b × C5c)
  5. Fuentes de observabilidad: portal LOTAIP · SIGEF · SERCOP
  6. Tasa de respuesta SAIP (si dato disponible)
  7. Pie de página con fuente pública

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
_AZUL    = "#3B82F6"   # C5 — perspectiva externa (ciudadana)
_TEAL    = "#14B8A6"   # C4 — perspectiva interna (institucional)


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTES CANÓNICOS
# ══════════════════════════════════════════════════════════════════════════════

def _render_return_band() -> None:
    """Banda superior de retorno al Centro de Mando — solo para Ejecutivo."""
    if is_ejecutivo():
        col1, _col2 = st.columns([1, 7])
        with col1:
            if st.button("← Centro de Mando", key="back_to_cc_d07"):
                st.session_state["gov_module"] = "inicio"
                st.rerun()


def _semaforo_color(semaforo: str) -> str:
    return {
        "VERDE":    _VERDE,
        "AMARILLO": _ALERTA,
        "ROJO":     _CRITICO,
        "PENDIENTE":_MUTED,
    }.get(semaforo, _MUTED)


def _semaforo_label(semaforo: str) -> str:
    return {
        "VERDE":    "TRANSPARENCIA EFECTIVA",
        "AMARILLO": "CUMPLIMIENTO PARCIAL",
        "ROJO":     "OPACIDAD CRÍTICA",
        "PENDIENTE":"VERIFICACIÓN PENDIENTE",
    }.get(semaforo, semaforo)


# ══════════════════════════════════════════════════════════════════════════════
# LAYER 2 CANÓNICO — Dom07 Transparencia
# QNKC-P01: C4 × C5 — el artefacto documental es uno, el ángulo epistémico es doble
# ══════════════════════════════════════════════════════════════════════════════

def _render_dom07_ejecutivo(chain: dict) -> None:
    """
    Layer 2 canónico — Dom07 Transparencia e Información Pública.
    Implementa QNKC-P01 (Dualidad Epistémica) y OBS-QNKC-01 (C5 tres dimensiones).
    Solo lenguaje de gobernanza pública. Sin nomenclatura interna.
    """
    # ── Extraer campos públicos del chain ─────────────────────────────────────
    sem             = chain.get("semaforo", "PENDIENTE")
    color           = _semaforo_color(sem)
    label           = _semaforo_label(sem)
    valor           = chain.get("valor_principal")          # puede ser None
    ind_label       = chain.get(
        "indicador_label",
        "Cumplimiento integral de publicación institucional"
    )
    fuente          = chain.get("fuente", "Portal LOTAIP GADMCM")
    corte           = chain.get("fecha_corte", "pendiente")
    narrativa       = chain.get("narrativa", "")
    estado          = chain.get("estado_dato", "pendiente_validacion")
    numerales       = chain.get("numerales_publicados")     # puede ser None
    numerales_total = chain.get("numerales_total", 21)
    tasa_saip       = chain.get("tasa_respuesta_saip")      # puede ser None
    umbral          = chain.get("umbral_verde", 80.0)
    fuente_neo4j    = chain.get("fuente_neo4j", False)      # INTERNO — no exponer en UI

    es_pendiente = (valor is None or sem == "PENDIENTE")

    # ── Cabecera de dominio ───────────────────────────────────────────────────
    st.markdown(
        f"<div style='font-size:11px;color:{_MUTED};letter-spacing:2px;"
        f"text-transform:uppercase;margin-bottom:4px'>D07 · TRANSPARENCIA</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div style='font-size:20px;font-weight:700;color:white;margin-bottom:16px'>"
        "Transparencia e Información Pública</div>",
        unsafe_allow_html=True,
    )

    # ── Sección 1: Semáforo y KPI principal ──────────────────────────────────
    if es_pendiente:
        st.markdown(
            f"""<div style="background:{color}18;border:1px solid {color}44;
                         border-left:4px solid {color};border-radius:10px;
                         padding:16px 20px;margin-bottom:16px">
  <div style="font-size:1.5rem;font-weight:900;color:{color};
              font-family:monospace;line-height:1">— / 100</div>
  <div style="font-size:0.75rem;font-weight:700;color:{color};
              letter-spacing:1px;margin-top:6px">{label}</div>
  <div style="font-size:0.8rem;color:rgba(255,255,255,0.7);margin-top:6px">
    {ind_label} · Se activa al completar la verificación del portal LOTAIP
  </div>
</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div style="background:{color}18;border:1px solid {color}44;
                         border-left:4px solid {color};border-radius:10px;
                         padding:16px 20px;margin-bottom:16px">
  <div style="font-size:2.8rem;font-weight:900;color:{color};
              font-family:monospace;line-height:1">{valor:.0f} / 100</div>
  <div style="font-size:0.75rem;font-weight:700;color:{color};
              letter-spacing:1px;margin-top:6px">{label}</div>
  <div style="font-size:0.8rem;color:rgba(255,255,255,0.7);margin-top:6px">
    {ind_label}
  </div>
</div>""",
            unsafe_allow_html=True,
        )

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

    # ── Sección 3: Dualidad Epistémica QNKC-P01 ─────────────────────────────
    # El mismo artefacto (portal LOTAIP) tiene dos ángulos epistémicos:
    #   C4: perspectiva interna — ¿el municipio cumplió su obligación de publicar?
    #   C5: perspectiva externa — ¿un ciudadano puede confirmarlo de forma independiente?
    st.markdown(
        f"<div style='font-size:0.75rem;color:{_MUTED};margin-bottom:8px;"
        f"font-weight:600;letter-spacing:1px'>"
        f"PROCESO Y EVIDENCIA — DOS ÁNGULOS DEL MISMO ARTEFACTO</div>",
        unsafe_allow_html=True,
    )

    col_c4, col_c5 = st.columns(2)

    # ── C4: Cumplimiento Formal (perspectiva institucional interna) ───────────
    with col_c4:
        if numerales is not None:
            c4_val   = f"{numerales} / {numerales_total}"
            c4_pct   = (numerales / numerales_total) * 100
            c4_color = (
                _VERDE   if c4_pct >= 80 else
                _ALERTA  if c4_pct >= 50 else
                _CRITICO
            )
            c4_barra = (
                f"<div style='margin:8px 0 4px'>"
                f"<div style='height:6px;background:rgba(255,255,255,0.1);"
                f"border-radius:4px;overflow:hidden'>"
                f"<div style='height:100%;width:{c4_pct:.0f}%;background:{c4_color};"
                f"border-radius:4px'></div></div>"
                f"<div style='font-size:0.6rem;color:{_MUTED};margin-top:3px'>"
                f"{c4_pct:.0f}% de cobertura</div></div>"
            )
        else:
            c4_val   = "— / 21"
            c4_color = _MUTED
            c4_barra = ""

        st.markdown(
            f"""<div style="background:{c4_color}10;border:1px solid {c4_color}28;
                         border-top:3px solid {_TEAL};border-radius:8px;
                         padding:14px;min-height:180px">
  <div style="font-size:0.62rem;color:{_TEAL};font-weight:700;
              letter-spacing:1.5px;margin-bottom:8px">C4 · CUMPLIMIENTO FORMAL</div>
  <div style="font-size:0.78rem;color:rgba(255,255,255,0.85);font-weight:600;
              margin-bottom:8px">¿El municipio publicó?</div>
  <div style="font-size:1.6rem;font-weight:900;color:{c4_color};
              font-family:monospace;margin-bottom:0">{c4_val}</div>
  {c4_barra}
  <div style="font-size:0.67rem;color:{_MUTED};line-height:1.5;margin-top:4px">
    Numerales LOTAIP Art. 19<br>con contenido activo en portal<br>
    <span style="color:{_TEAL}">Perspectiva institucional</span>
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    # ── C5: Verificabilidad Efectiva (perspectiva ciudadana externa) ──────────
    with col_c5:
        st.markdown(
            f"""<div style="background:{_AZUL}08;border:1px solid {_AZUL}22;
                         border-top:3px solid {_AZUL};border-radius:8px;
                         padding:14px;min-height:180px">
  <div style="font-size:0.62rem;color:{_AZUL};font-weight:700;
              letter-spacing:1.5px;margin-bottom:8px">C5 · VERIFICABILIDAD EFECTIVA</div>
  <div style="font-size:0.78rem;color:rgba(255,255,255,0.85);font-weight:600;
              margin-bottom:10px">¿Un ciudadano puede confirmarlo?</div>
  <div style="display:flex;flex-direction:column;gap:5px">
    <div style="font-size:0.67rem;color:rgba(255,255,255,0.8);
                background:rgba(59,130,246,0.08);border-radius:5px;
                padding:6px 10px;border-left:2px solid {_AZUL}">
      <span style="color:{_AZUL};font-weight:700">C5a · Existencia</span><br>
      ¿El enlace responde HTTP 200?
    </div>
    <div style="font-size:0.67rem;color:rgba(255,255,255,0.8);
                background:rgba(59,130,246,0.08);border-radius:5px;
                padding:6px 10px;border-left:2px solid {_AZUL}">
      <span style="color:{_AZUL};font-weight:700">C5b · Actualidad</span><br>
      ¿El contenido es del período vigente?
    </div>
    <div style="font-size:0.67rem;color:rgba(255,255,255,0.8);
                background:rgba(59,130,246,0.08);border-radius:5px;
                padding:6px 10px;border-left:2px solid {_AZUL}">
      <span style="color:{_AZUL};font-weight:700">C5c · Inteligibilidad</span><br>
      ¿Un ciudadano puede entenderlo?
    </div>
  </div>
  <div style="font-size:0.62rem;color:{_AZUL};margin-top:8px">
    Perspectiva ciudadana externa
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Sección 4: Fórmula C8 ────────────────────────────────────────────────
    # C8 = cumplimiento_formal × verificabilidad_efectiva
    #    = C4 × (C5a × C5b × C5c)
    # Multiplicativa: un cero en cualquier dimensión colapsa el resultado a cero.
    st.markdown(
        f"""<div style="background:rgba(255,255,255,0.03);
                     border:1px solid rgba(255,255,255,0.08);
                     border-radius:8px;padding:14px 18px;margin-bottom:16px">
  <div style="font-size:0.65rem;color:{_MUTED};font-weight:700;
              letter-spacing:1.5px;margin-bottom:10px">INDICADOR INTEGRAL DE TRANSPARENCIA</div>
  <div style="font-family:monospace;font-size:0.9rem;color:white;
              display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:10px">
    <span style="color:{_VERDE};font-weight:900">C8</span>
    <span style="color:{_MUTED}">=</span>
    <span style="background:{_TEAL}18;color:{_TEAL};font-weight:700;
                padding:2px 8px;border-radius:4px">C4</span>
    <span style="color:{_MUTED}">×</span>
    <span style="color:{_MUTED}">(</span>
    <span style="background:{_AZUL}18;color:{_AZUL};font-weight:700;
                padding:2px 8px;border-radius:4px">C5a</span>
    <span style="color:{_MUTED}">×</span>
    <span style="background:{_AZUL}18;color:{_AZUL};font-weight:700;
                padding:2px 8px;border-radius:4px">C5b</span>
    <span style="color:{_MUTED}">×</span>
    <span style="background:{_AZUL}18;color:{_AZUL};font-weight:700;
                padding:2px 8px;border-radius:4px">C5c</span>
    <span style="color:{_MUTED}">)</span>
  </div>
  <div style="display:flex;gap:16px;flex-wrap:wrap">
    <div style="font-size:0.68rem;color:{_MUTED};line-height:1.5;flex:1;min-width:200px">
      <span style="color:{_VERDE};font-weight:700">Verde</span> ≥ {umbral:.0f} &nbsp;|&nbsp;
      <span style="color:{_ALERTA};font-weight:700">Amarillo</span> ≥ 50 &nbsp;|&nbsp;
      <span style="color:{_CRITICO};font-weight:700">Rojo</span> &lt; 50
    </div>
    <div style="font-size:0.68rem;color:{_MUTED};line-height:1.5;flex:2;min-width:240px">
      Un GAD que publica 21/21 artículos con enlaces rotos tiene C5a ≈ 0
      y por tanto C8 ≈ 0. La transparencia simulada no es transparencia.
    </div>
  </div>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Sección 5: Fuentes de observabilidad ─────────────────────────────────
    st.markdown(
        f"<div style='font-size:0.75rem;color:{_MUTED};margin-bottom:8px;"
        f"font-weight:600;letter-spacing:1px'>"
        f"FUENTES DE OBSERVABILIDAD — VERIFICABLES POR CUALQUIER CIUDADANO SIN CREDENCIALES</div>",
        unsafe_allow_html=True,
    )

    # OBS-QNKC-02: portal DPE es la fuente canónica de C5a/C5b bajo LOTAIP 2.0
    obs_sources = [
        (
            "Portal DPE · LOTAIP 2.0",
            "transparencia.dpe.gob.ec",
            "Fuente canónica C5 · Numerales Art. 19 · todos los GADs del Ecuador",
            "DPE — Ley LOTAIP 2.0 (fuente regulatoria oficial)",
        ),
        (
            "SIGEF",
            "finanzas.gob.ec",
            "Ejecución presupuestaria en tiempo real · por partidas",
            "COOTAD Art. 215",
        ),
        (
            "SERCOP",
            "compraspublicas.gob.ec",
            "PAC + contratos adjudicados + montos + contratistas",
            "LOSNCP Art. 21",
        ),
    ]

    cols = st.columns(3)
    for i, (nombre, url, desc, norma_txt) in enumerate(obs_sources):
        with cols[i]:
            st.markdown(
                f"""<div style="background:rgba(255,255,255,0.04);
                             border:1px solid rgba(255,255,255,0.08);
                             border-radius:8px;padding:12px;text-align:center;
                             height:100%">
  <div style="font-size:0.75rem;font-weight:700;color:white;margin-bottom:4px">{nombre}</div>
  <div style="font-size:0.62rem;color:{_AZUL};margin-bottom:6px">{url}</div>
  <div style="font-size:0.63rem;color:{_MUTED};line-height:1.5;margin-bottom:4px">{desc}</div>
  <div style="font-size:0.58rem;color:rgba(255,255,255,0.3)">{norma_txt}</div>
</div>""",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Sección 6: Tasa SAIP — solo si el dato existe ─────────────────────────
    if tasa_saip is not None:
        color_saip = (
            _VERDE   if tasa_saip >= 95 else
            _ALERTA  if tasa_saip >= 70 else
            _CRITICO
        )
        st.markdown(
            f"""<div style="background:{color_saip}12;border:1px solid {color_saip}30;
                         border-radius:8px;padding:12px 16px;margin-bottom:16px;
                         display:flex;align-items:center;gap:16px">
  <div style="font-size:1.6rem;font-weight:900;color:{color_saip};
              font-family:monospace;min-width:60px">{tasa_saip:.0f}%</div>
  <div>
    <div style="font-size:0.75rem;font-weight:700;color:white">
      Tasa de respuesta a solicitudes de información
    </div>
    <div style="font-size:0.68rem;color:{_MUTED};margin-top:3px">
      % de solicitudes ciudadanas respondidas dentro de los 10 días hábiles · LOTAIP Art. 34
    </div>
  </div>
</div>""",
            unsafe_allow_html=True,
        )

    # ── Sección 7: Pie de página ──────────────────────────────────────────────
    fuente_badge = "🔴 Datos en vivo · Neo4j" if fuente_neo4j else "📋 Datos consolidados"
    st.caption(f"{fuente_badge} · Fuente: {fuente} · Corte: {corte}")

    if es_pendiente:
        st.info(
            "**Verificación pendiente.** Para activar este dominio, el equipo QUIRA Operaciones "
            "debe auditar directamente el portal montecristi.gob.ec: "
            "contar los 21 numerales activos (C5a), verificar fechas de actualización (C5b) "
            "y evaluar comprensibilidad para el ciudadano (C5c). "
            "El indicador C8 se calculará automáticamente al cargar los datos en el sistema.",
            icon="🔍",
        )


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT — llamado desde env_gov.py · _render_transparencia()
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Layer 2 — Transparencia e Información Pública
    Dominio D07 · Sprint 4 BETA-CORE · ADR-013 + ADR-014
    QNKC-P01 Dualidad Epistémica · OBS-QNKC-01 C5 tres dimensiones

    Todos los roles → vista canónica QTMP TRANSPARENCIA.
    """
    from app.connectors.neo4j_qtmp import get_qtmp_chain
    _render_return_band()

    chain = get_qtmp_chain("TRANSPARENCIA")
    if chain:
        _render_dom07_ejecutivo(chain)
    else:
        st.error("Datos del dominio no disponibles. Intente nuevamente.")
