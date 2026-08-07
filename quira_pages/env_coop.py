"""
QUIRA — Ambiente 📑 Cooperación  ·  `quira_pages/env_coop.py`

QUIRA Cooperación: inteligencia para estructurar, alinear y hacer elegibles
intervenciones ante cooperación bilateral y multilateral, reembolsable y no
reembolsable.

────────────────────────────────────────────────────────────────────────────────
POR QUÉ ESTE ARCHIVO CAMBIÓ DE NOMBRE (Javo · 2026-08-07)
────────────────────────────────────────────────────────────────────────────────
Se llamaba `env_impact.py`, su clave era `impact` y su nombre público
«Cooperación». El canon trató ambos productos como uno solo y quedaron cruzados.
Son distintos, y la diferencia no es de matiz sino de contrato de salida:

  · **Cooperación** responde «¿qué puede financiarse, con qué instrumento y bajo
    qué condiciones de elegibilidad?». Su usuario decide dónde poner recursos.
  · **Impact** responde «¿qué pueden investigar y reproducir terceros?». Su
    usuario produce conocimiento propio, y lo que necesita son datos, series,
    metodología y trazabilidad.

Comparten el mismo conocimiento y el mismo motor; entregan cosas distintas. El
contenido de este ambiente siempre fue cooperación, así que la clave se alinea
con lo que hace y **`impact` queda libre** para cuando ese producto exista.

Estado: Fase 2 (ADR-041 §4). Consume la evidencia que producen las entradas de
Fase 1 —Observatorio y QUIRA Ciudadana—; no genera evidencia propia.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from utils.css_tokens import C
from utils.marca import logo


def render() -> None:
    st.markdown(f"""
<div style="display:flex;flex-direction:column;align-items:center;
            justify-content:center;min-height:60vh;text-align:center;padding:2rem">
    <div style="line-height:0;margin-bottom:18px;opacity:.85">{logo("marfil", 44)}</div>
    <div style="font-size:1.5rem;font-weight:800;color:{C.V_TX};margin-bottom:8px">
        QUIRA Cooperación
    </div>
    <div style="font:400 13px/1.75 Inter,sans-serif;color:{C.V_TX2};max-width:520px;
                margin-bottom:22px">
        Inteligencia para estructurar y hacer elegibles intervenciones ante
        <b style="color:{C.V_TX}">cooperación bilateral y multilateral</b>,
        reembolsable y no reembolsable. Alineación con marcos de financiamiento,
        evidencia de elegibilidad y seguimiento de lo colocado en territorio.
    </div>
    <div style="padding:8px 20px;background:{C.alpha(C.ACENTO,.10)};
                border:1px solid {C.alpha(C.ACENTO,.28)};border-radius:8px;
                font:700 11px/1 'JetBrains Mono',monospace;color:{C.ACENTO};
                letter-spacing:.06em">FASE 2 — EN PREPARACIÓN</div>
    <div style="margin-top:26px;padding:13px 17px;background:{C.VOLCAN_UP};
                border:1px solid {C.V_BD};border-radius:10px;font-size:11.5px;
                color:{C.V_TX2};max-width:500px;line-height:1.7;text-align:left">
        <b style="color:{C.V_TX}">Por qué va después, y no es una preferencia.</b>
        Este producto no genera evidencia: la consume. Su valor para un organismo
        financiador es la <b>cobertura territorial</b>, y esa cobertura la
        producen las dos entradas de Fase 1 — el Observatorio y QUIRA Ciudadana.
        Construirlo antes daría un producto sin nada que ofrecer (ADR-041 §4).
    </div>
</div>
    """, unsafe_allow_html=True)
