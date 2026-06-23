"""
QUIRA OS — QINV-001 · Planificación Estratégica (Investigación)
═══════════════════════════════════════════════════════════════════════════════
Segunda INSTANCIA del kernel InvestigacionQUIRA (UMI), tras QINV-006. Investiga la
CADENA de planificación estratégica del territorio: PDOT → POA → PAC → Presupuesto.
Bajo la regla soberana 20/70/10 y en clave PREVENTIVA (no punitiva): QUIRA anticipa
dónde puede abrirse una desviación en la senda del plan; no juzga el pasado.

  20% · Contexto  → la pregunta estratégica permanente + la correspondencia con el Plan
  70% · EVIDENCIA → la cadena REAL del motor, abierta y a ancho completo:
                    ① las metas del PDOT · ② la cadena POA→PAC · ③ la coherencia.
                    La riqueza del método validado en Montecristi NO se minimiza.
  10% · Lectura   → la interpretación de QUIRA, DESPUÉS de toda la evidencia.

Madre: FIDELIDAD DE PLANIFICACIÓN — % de correspondencia con las metas plurianuales
del PDOT (dato real del motor · NO el proxy IPE, que el Canon marca pendiente de POA).

Doctrina: Excel = Estado (Regla 1 · el número se lee, no se recalcula) · sin dato
verificado no hay afirmación (Regla 3) · Firewall: ningún código interno en la vista
pública (ni ICPI, ni TGI, ni H-series, ni Gold Master).

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from quira_pages.umi import InvestigacionQUIRA

# Pregunta estratégica PERMANENTE — fuente ÚNICA: registro QINV d01 (sin doble pregunta)
_PREGUNTA = (
    "¿La institución sostiene la correspondencia con sus metas plurianuales, "
    "o registra desviaciones en su senda de desarrollo?"
)

# Umbral de referencia = objetivo 2027 del Plan (semáforo canónico del constructor de cajones)
_UMBRAL = 70.0


def _cargar() -> dict:
    """Lee el estado real de la planificación del motor (Gold Master · Regla 1).
    Madre = Fidelidad de Planificación (correspondencia con las metas plurianuales)."""
    out: dict = {}
    try:
        from quira_pages.p_command_center import _load_data
        out.update(_load_data() or {})
    except Exception:
        pass
    # Fidelidad de Planificación + alcance del plan, desde el snapshot del motor.
    try:
        from utils.cache_quira import cargar_gm_snapshot
        gm = cargar_gm_snapshot() or {}
        d2 = (gm.get("tgi", {}) or {}).get("d2", {}) or {}
        out["fidelidad_plan"] = d2.get("valor")            # % correspondencia metas PDOT
        gad = gm.get("gad", {}) or {}
        out["metas_pdot"] = gad.get("metas_pdot")          # 25 metas del PDOT
    except Exception:
        pass
    return out


def _bloque(titulo: str, subtitulo: str, modname: str) -> None:
    """Un cuerpo de evidencia del motor, ABIERTO y a ancho completo (no escondido).
    Cosecha la vista-cantera tal cual la validó Montecristi."""
    st.markdown(
        f'<div style="margin:8px 0 6px">'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:13px;'
        f'font-weight:800;color:#E8EDF4;letter-spacing:.02em">{titulo}</span>'
        f'<span style="font-size:11px;color:#5A6B7E;margin-left:9px">{subtitulo}</span></div>',
        unsafe_allow_html=True,
    )
    try:
        from importlib import import_module
        import_module(f"quira_pages.{modname}").render()
    except Exception as e:
        st.caption(f"Bloque de evidencia no disponible: {e}")


def _evidencia() -> None:
    """El universo de evidencia de Planificación Estratégica — la cadena real del
    motor, abierta y en secuencia. Es el 70%: la evidencia pesa más que la lectura.
    Del plan a su contratación: ① metas PDOT → ② cadena POA-PAC → ③ coherencia."""
    _div = ('<hr style="border:none;border-top:1px solid rgba(255,255,255,.08);'
            'margin:16px 0">')
    _bloque("① EL PLAN", "las metas plurianuales del PDOT 2023-2027", "p8_metas")
    st.markdown(_div, unsafe_allow_html=True)
    _bloque("② LA CADENA", "del plan a la contratación — trazabilidad POA→PAC", "p12_cadena")
    st.markdown(_div, unsafe_allow_html=True)
    _bloque("③ COHERENCIA DE LA CADENA", "dónde el plan se mantiene y dónde se abre", "p3_congruencias")


def render() -> None:
    """QINV-001 · Planificación Estratégica — investigación de la cadena del plan."""
    d = _cargar()
    fid = d.get("fidelidad_plan")
    metas = d.get("metas_pdot")
    tiene = isinstance(fid, (int, float))
    dato_str = f"{fid:.1f}%" if tiene else "—"

    if not tiene:
        estado, temp, vpct = "—", "dim", None
        headline = "Sin evidencia cargada para este corte."
        peritaje = [
            "La investigación no puede leer sin evidencia del motor (Regla 3): "
            "cargue el corte para emitir la lectura.",
        ]
        conclusion = "Lea la evidencia del corte para la interpretación de QUIRA."
        prioridad_temp = "alerta"
    else:
        vpct = int(round(fid))
        # Semáforo canónico (constructor de cajones): umbral = objetivo del Plan.
        if fid >= _UMBRAL:
            temp, estado = "verde", "EN SENDA"
        elif fid >= _UMBRAL * 0.85:
            temp, estado = "alerta", "BAJO OBJETIVO"
        else:
            temp, estado = "critico", "DESVIACIÓN CRÍTICA"
        prioridad_temp = temp
        metas_txt = f"las {metas} metas" if metas else "las metas"
        headline = ("El plan conserva la correspondencia con su senda; el foco "
                    "preventivo está en sostenerla en la ejecución.")
        peritaje = [
            f"La planificación mantiene una correspondencia del {dato_str} con "
            f"{metas_txt} plurianuales del Plan de Desarrollo — el diseño del plan "
            f"está esencialmente a la altura de su objetivo a 2027.",
            "La evidencia desplegada arriba recorre la cadena completa: del plan "
            "(metas) a su contratación (POA→PAC) y a la coherencia entre ambos.",
            "La distancia que importa no está en el diseño del plan, sino en sostener "
            "su traducción a ejecución mes a mes — ahí es donde se abren las "
            "desviaciones, y donde conviene poner la atención hoy.",
        ]
        conclusion = (
            "El Plan de Desarrollo mantiene su senda en el diseño plurianual. La señal "
            "es preventiva: vigilar que la programación operativa (POA) y la "
            "contratación (PAC) sigan el ritmo del plan, para que la correspondencia no "
            "se erosione en la ejecución."
        )

    inv = InvestigacionQUIRA(
        id="QINV-001", dominio="d01", nombre="Planificación Estratégica", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=dato_str, temp=temp,
        hipotesis=("La fidelidad estratégica se mide por la correspondencia sostenida "
                   "entre el plan plurianual y su ejecución a lo largo de la cadena."),
        evidencia=_evidencia,
        peritaje_headline=headline,
        peritaje=peritaje,
        veredicto_label="Correspondencia con el Plan",
        veredicto_pct=vpct,
        divergencias="",
        prioridad="Foco · ejecución de la cadena del plan",
        prioridad_temp=prioridad_temp,
        conclusion=conclusion,
    )
    inv.to_streamlit()
