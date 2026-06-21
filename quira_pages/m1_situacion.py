"""
QUIRA OS — QINV-006 · Salud Institucional (Investigación)
═══════════════════════════════════════════════════════════════════════════════
Primera INSTANCIA del kernel InvestigacionQUIRA (UMI). Corte vigente:
QEXP-006-2026-Q1. NO es un dashboard ni una tablita: es un EXPEDIENTE de
inteligencia bajo la regla soberana 20/70/10.

  20% · Contexto  → la pregunta forense permanente + el estado general (banda UMI)
  70% · EVIDENCIA → el universo de pruebas del motor: los 3 cuerpos de evidencia
                    (Diagnóstico · Pulso · Brecha) ABIERTOS y a ancho completo.
                    La riqueza del laboratorio de Montecristi NO se minimiza.
  10% · Dictamen  → el peritaje QUIRA, DESPUÉS de toda la evidencia, jamás antes.

Doctrina: Excel = Estado (Regla 1 · el número se lee, no se recalcula) · sin dato
verificado no hay afirmación (Regla 3). QUIRA resume el método; no lo reemplaza.
Firewall: ningún código interno en la vista pública.

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
    """El universo de evidencia de Salud Institucional — los 3 cuerpos del motor,
    abiertos y en secuencia. Es el 70%: la prueba pesa más que el dictamen."""
    _div = ('<hr style="border:none;border-top:1px solid rgba(255,255,255,.08);'
            'margin:16px 0">')
    _bloque("① DIAGNÓSTICO INSTITUCIONAL", "las 41 métricas integradas del motor", "p_ejecutivo")
    st.markdown(_div, unsafe_allow_html=True)
    _bloque("② PULSO OPERATIVO", "el estado vivo del municipio", "p6_pulso")
    st.markdown(_div, unsafe_allow_html=True)
    _bloque("③ CAUSAS DE LA BRECHA", "dónde y por qué se abre la distancia al umbral", "p7_brecha")


def render() -> None:
    """QINV-006 · Salud Institucional — el primer expediente sobre el kernel UMI."""
    d = _cargar()
    icpi = d.get("icpi_pct")
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
            f"Tras integrar los tres cuerpos de evidencia, el cumplimiento "
            f"institucional se sitúa en {icpi_str}.",
            "El diagnóstico no descansa en un dato suelto: son 41 métricas en "
            "seguimiento las que sostienen el patrón.",
            ("La institución sostiene el gobierno, pero sin margen: cualquier choque "
             "la empuja bajo el piso operativo." if icpi < 65 else
             "La institución opera con holgura, pero la vigilancia no se suspende."),
        ]

    inv = InvestigacionQUIRA(
        id="QINV-006", dominio="d06", nombre="Salud Institucional", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=icpi_str, temp=temp,
        hipotesis="La capacidad institucional se sostiene cerca del umbral de gobernabilidad.",
        evidencia=_evidencia,
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
            "Lea el peritaje sobre la evidencia desplegada para el dictamen del corte."
        ),
    )
    inv.to_streamlit()
