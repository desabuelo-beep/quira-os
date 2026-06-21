"""
QUIRA OS — QINV-006 · Salud Institucional (Investigación)
═══════════════════════════════════════════════════════════════════════════════
Primera INSTANCIA del kernel InvestigacionQUIRA (UMI). El corte vigente es el
expediente QEXP-006-2026-Q1. NO es un dashboard: es un expediente de inteligencia.

  · Evidencia  → cosecha del motor (cumplimiento real + las 3 vistas-cantera)
  · Peritaje   → dictamen sobre la capacidad institucional
  · Veredicto  → el cumplimiento institucional vivo, para decidir en segundos

La pregunta forense es PERMANENTE (vive en QINV-006); cada corte la congela en un
expediente fechado. Doctrina: Excel = Estado (Regla 1 · el número se lee, no se
recalcula) · sin dato verificado no hay afirmación (Regla 3). Firewall: ningún
código interno en la vista pública.

NOTA: este archivo era el contenedor de 3 pestañas (Vista Ejecutiva · Pulso ·
Brecha). Ese contenido se conserva íntegro como "evidencia ampliada" — nada se
pierde; se reencuadra como prueba del expediente.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from quira_pages.umi import InvestigacionQUIRA

# Pregunta forense PERMANENTE (canon · Diccionario d06 · campo 6)
_PREGUNTA = "¿Tiene esta institución capacidad para sostener el gobierno?"


def _cargar() -> dict:
    """Lee el cumplimiento institucional real del motor (Gold Master · Regla 1)."""
    try:
        from quira_pages.p_command_center import _load_data
        return _load_data() or {}
    except Exception:
        return {}


def _evidencia_panel(icpi_str: str, clasif: str) -> None:
    """La prueba: el cumplimiento real y sus parámetros de seguimiento (corte Q1-2026)."""
    filas = [
        ("Cumplimiento institucional", icpi_str, "el índice agregado de la salud del aparato público"),
        ("Clasificación del corte", clasif or "—", "lectura del motor para este período"),
        ("Métricas en seguimiento", "41", "el diagnóstico no es un dato suelto"),
        ("Corte del expediente", "Q1-2026", "foto fechada · la investigación es permanente"),
    ]
    bloques = "".join(
        f'<div style="padding:10px 0;border-bottom:1px solid rgba(255,255,255,.06)">'
        f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px">'
        f'<span style="font-size:12px;color:#A8B4C8">{lbl}</span>'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:15px;'
        f'font-weight:800;color:#E8EDF4">{val}</span></div>'
        f'<div style="font-size:10px;color:#5A6B7E;margin-top:2px">{sub}</div></div>'
        for lbl, val, sub in filas
    )
    st.markdown(
        f'<div style="background:rgba(255,255,255,.015);border:1px solid rgba(255,255,255,.07);'
        f'border-radius:12px;padding:4px 16px 8px">{bloques}</div>',
        unsafe_allow_html=True,
    )


def _cantera() -> None:
    """Evidencia ampliada: las 3 vistas-cantera del motor (datos reales · ancho completo)."""
    st.markdown('<div style="margin-top:16px"></div>', unsafe_allow_html=True)
    with st.expander("▸ Evidencia ampliada — diagnóstico, pulso y causas de la brecha", expanded=False):
        t1, t2, t3 = st.tabs(["🏛 Diagnóstico", "⚡ Pulso", "📉 Causas de la Brecha"])
        with t1:
            try:
                from quira_pages.p_ejecutivo import render as _r
                _r()
            except Exception as e:
                st.caption(f"Diagnóstico no disponible: {e}")
        with t2:
            try:
                from quira_pages.p6_pulso import render as _r
                _r()
            except Exception as e:
                st.caption(f"Pulso no disponible: {e}")
        with t3:
            try:
                from quira_pages.p7_brecha import render as _r
                _r()
            except Exception as e:
                st.caption(f"Causas de la brecha no disponibles: {e}")


def render() -> None:
    """QINV-006 · Salud Institucional — el primer expediente sobre el kernel UMI."""
    d = _cargar()
    icpi = d.get("icpi_pct")
    clasif = d.get("icpi_clasif", "—")
    tiene = isinstance(icpi, (int, float))
    icpi_str = f"{icpi:.1f}%" if tiene else "—"

    if not tiene:
        estado, temp, vpct = "SIN DATOS DEL CORTE", "dim", None
        headline = "Sin evidencia cargada para este corte."
        peritaje = [
            "El expediente no puede dictaminar sin evidencia del motor (Regla 3): "
            "cargue el corte para emitir el peritaje.",
        ]
    else:
        if icpi < 65:
            estado, temp = "BAJO UMBRAL", "critico"
        elif icpi < 80:
            estado, temp = "OBSERVADO", "alerta"
        else:
            estado, temp = "EN RANGO", "verde"
        vpct = int(round(icpi))
        headline = ("El deterioro es estructural, no coyuntural." if icpi < 65
                    else "El cumplimiento se sostiene, bajo vigilancia.")
        peritaje = [
            f"El índice de cumplimiento institucional se sitúa hoy en {icpi_str}.",
            "El diagnóstico integra 41 métricas en seguimiento (corte Q1-2026): "
            "no es un dato aislado, es un patrón sostenido.",
            ("La institución sostiene el gobierno, pero sin margen: cualquier choque "
             "la empuja bajo el piso operativo." if icpi < 65 else
             "La institución opera con holgura, pero la vigilancia no se suspende."),
        ]

    inv = InvestigacionQUIRA(
        id="QINV-006", dominio="d06", nombre="Salud Institucional", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=icpi_str, temp=temp,
        hipotesis="La capacidad institucional se sostiene cerca del umbral de gobernabilidad.",
        evidencia=lambda: _evidencia_panel(icpi_str, clasif),
        peritaje_headline=headline,
        peritaje=peritaje,
        veredicto_label="Capacidad institucional",
        veredicto_pct=vpct,
        divergencias="41 métricas en seguimiento",
        prioridad="Prioridad 1 · capacidad institucional",
        prioridad_temp=temp if temp != "dim" else "alerta",
        conclusion=(
            "La institución sostiene el gobierno hoy, pero su capacidad de cumplimiento "
            "está bajo el umbral: la prioridad no es cosmética, es estructural."
            if tiene and icpi < 65 else
            "Lea el peritaje y la evidencia ampliada para el dictamen del corte."
        ),
    )
    inv.to_streamlit()
    _cantera()
