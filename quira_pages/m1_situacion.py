"""
QUIRA OS — QINV-006 · Salud Institucional (Investigación)
═══════════════════════════════════════════════════════════════════════════════
Primera INSTANCIA del kernel InvestigacionQUIRA (UMI). Investigación de
inteligencia PREVENTIVA bajo la regla soberana 20/70/10. NO es punitiva: QUIRA
anticipa y orienta el foco; no acusa ni emite veredictos sobre el pasado.

  20% · Contexto  → la pregunta estratégica permanente + el estado del corte
  70% · EVIDENCIA → todo lo que observa el motor: los 3 cuerpos de evidencia
                    (Diagnóstico · Pulso · Brecha) ABIERTOS y a ancho completo.
                    La riqueza del método validado en Montecristi NO se minimiza.
  10% · Lectura   → la interpretación de QUIRA, DESPUÉS de toda la evidencia.

Doctrina: Excel = Estado (Regla 1 · el número se lee, no se recalcula) · sin dato
verificado no hay afirmación (Regla 3 · NO se inventan métricas que el motor no
sostiene). Firewall: ningún código interno en la vista pública.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from quira_pages.umi import InvestigacionQUIRA

# Pregunta estratégica PERMANENTE (canon · Diccionario d06 · campo 6)
_PREGUNTA = "¿Tiene esta institución capacidad para sostener el gobierno?"


def _cargar() -> tuple[dict, str]:
    """Lee el cumplimiento institucional real del motor (Gold Master · Regla 1).

    Devuelve `(datos, motivo)`. El `except` devolvía `{}` a secas, y entonces un
    FALLO TÉCNICO era indistinguible de un corte sin datos: las dos cosas
    pintaban la misma pantalla vacía. Son distintas —una se arregla, la otra se
    consigue— y ADR-046 §2.4 obliga a decir cuál es (2026-08-10)."""
    try:
        from quira_pages.p_command_center import _load_data
        d = _load_data() or {}
        return d, ("" if d else "sin_datos")
    except Exception as e:
        return {}, f"error_tecnico: {type(e).__name__}"


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
    abiertos y en secuencia. Es el 70%: la evidencia pesa más que la lectura."""
    _div = ('<hr style="border:none;border-top:1px solid rgba(255,255,255,.08);'
            'margin:16px 0">')
    _bloque("① DIAGNÓSTICO INSTITUCIONAL", "los indicadores integrados del motor", "p_ejecutivo")
    st.markdown(_div, unsafe_allow_html=True)
    _bloque("② PULSO OPERATIVO", "el estado vivo del municipio", "p6_pulso")
    st.markdown(_div, unsafe_allow_html=True)
    _bloque("③ CAUSAS DE LA BRECHA", "dónde y por qué se abre la distancia", "p7_brecha")


def render() -> None:
    """QINV-006 · Salud Institucional — primera investigación sobre el kernel UMI."""
    d, motivo = _cargar()
    icpi = d.get("icpi_pct")
    clasif = (d.get("icpi_clasif") or "").strip()
    tiene = isinstance(icpi, (int, float))
    icpi_str = f"{icpi:.1f}%" if tiene else "—"

    if not tiene:
        # ADR-046 §2.4 · la ausencia se muestra ACCIONABLE. Decía «cargue el
        # corte», que es una instrucción de operador dirigida a quien no está
        # mirando la pantalla. Ahora dice QUÉ falta, POR QUÉ falta y CÓMO se
        # consigue — y distingue el fallo técnico de la evidencia inexistente,
        # que son problemas distintos con soluciones distintas.
        estado, temp, vpct = "Sin evidencia", "dim", None
        if motivo.startswith("error_tecnico"):
            headline = "La evidencia existe, pero el sistema no pudo leerla."
            peritaje = [
                "Esto no es una ausencia de evidencia: es un fallo de lectura del "
                f"sistema ({motivo.split(': ')[-1]}). El dato del motor no está en duda.",
                "Se registra como incidencia técnica y no altera lo publicado sobre "
                "este municipio. Nada se infiere mientras tanto.",
            ]
            conclusion = ("Fallo técnico de lectura, no ausencia documental. "
                          "Corresponde a mantenimiento, no al municipio.")
        else:
            headline = "Este municipio todavía no puede leerse."
            peritaje = [
                "No hay evidencia suficiente para calcular el cumplimiento "
                "institucional de este corte. **La ausencia es el resultado**, no un "
                "error de la pantalla ni un juicio sobre la entidad.",
                "Falta la cédula presupuestaria del período y los reportes de "
                "ejecución. Si el municipio no los publicó, pueden pedirse por "
                "solicitud de acceso a la información pública — o aportarse, si "
                "alguien ya los tiene.",
                "Que la evidencia llegue por esa vía **enciende la lectura de este "
                "territorio**, y deja constancia igualmente de que no estaba publicada.",
            ]
            conclusion = ("Sin evidencia no hay afirmación (Regla 3). Lo que falta está "
                          "identificado y puede conseguirse.")
    else:
        vpct = int(round(icpi))
        # Color = semáforo VISUAL; el estado = la clasificación REAL del motor (no inventada).
        temp = "critico" if icpi < 50 else ("alerta" if icpi < 75 else "verde")
        estado = clasif if clasif else "—"
        headline = "El cumplimiento institucional necesita atención sostenida."
        peritaje = [
            f"Tras integrar los tres cuerpos de evidencia, el cumplimiento "
            f"institucional del corte se sitúa en {icpi_str}.",
            "La lectura no descansa en un dato suelto: integra el conjunto de "
            "indicadores que el motor mide para este corte.",
            "La evidencia desplegada arriba muestra dónde se concentra la distancia "
            "— ahí está el foco preventivo, antes de que escale.",
        ]
        conclusion = (
            "El cumplimiento institucional está por debajo del nivel deseado para el "
            "corte. La señal es preventiva: marca dónde concentrar la atención hoy, "
            "no un juicio sobre el pasado."
        )

    inv = InvestigacionQUIRA(
        id="QINV-006", dominio="d06", nombre="Salud Institucional", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=icpi_str, temp=temp,
        hipotesis="La capacidad institucional se mide por el cumplimiento sostenible de funciones.",
        evidencia=_evidencia,
        peritaje_headline=headline,
        peritaje=peritaje,
        veredicto_label="Cumplimiento institucional",
        veredicto_pct=vpct,
        divergencias="",
        prioridad="Foco · cumplimiento institucional",
        prioridad_temp=temp if temp != "dim" else "alerta",
        conclusion=conclusion,
    )
    inv.to_streamlit()
