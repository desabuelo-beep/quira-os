"""
QUIRA — Ambiente OBSERVATORIO  ·  `quira_pages/env_obs.py`

El Observatorio de Integridad Territorial: el instrumento con el que se observa
la gestión pública de forma progresiva y verificable. Es el PRODUCTO PRINCIPAL
(ADR-041 §5.1), no una herramienta interna.

────────────────────────────────────────────────────────────────────────────────
NO ES OPERACIONES — la distinción es de Javo (2026-08-06) y corrige al director
────────────────────────────────────────────────────────────────────────────────
El director había alojado este panel dentro del ambiente de Operaciones
razonando que evitaba duplicar (Regla 7). Estaba mal: no son el mismo concepto
con dos nombres, son dos cosas distintas.

  · OPERACIONES (`env_ops.py`) → mantenimiento TÉCNICO del sistema. Lo hace
    Dylus Lab cuando algo se rompe: cargas, conectores, cache, versiones.
  · OBSERVATORIO (este archivo) → instrumento de ADMINISTRACIÓN PÚBLICA y
    desarrollo. Sus interlocutores son entidades del sector público, organismos
    multilaterales y agencias de cooperación. Lo que se ve aquí se enseña.

Alojar el segundo dentro del primero lo degradaba de producto a herramienta de
soporte, y contradecía al propio ADR-041, que lo nombra el producto principal.

────────────────────────────────────────────────────────────────────────────────
LA VÍA — portal de transparencia de la Defensoría del Pueblo
────────────────────────────────────────────────────────────────────────────────
Bajo LOTAIP la obligación de publicar es del GAD y la Defensoría registra el
cumplimiento mes a mes. El Observatorio lee ese registro: no requiere que ningún
municipio entregue nada ni que medie acuerdo. De ahí sale la cobertura
progresiva de los 222 sin tener toda su información — y el identificador que
devuelve el portal es la llave para cruzar después con los demás sistemas.

La secuencia es progresiva por diseño (Javo): se valida el cantón piloto —2025
completo y lo que va de 2026— antes de ampliar el barrido.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from utils.css_tokens import C
from utils.marca import logo


def _tab_estado() -> None:
    """Estado de la operación — el panel."""
    try:
        from quira_pages.p_panel_observatorio import render as _panel
        _panel()
    except Exception as e:  # noqa: BLE001
        st.error(f"Panel del Observatorio no disponible: {e}")


def _tab_monitoreo() -> None:
    """Monitoreo mensual de transparencia — el trabajo sustantivo del dominio.

    Todavía no tiene interfaz propia: la primera práctica se ve completa en el
    estado de la operación, y el desarrollo de la verificación conjunto por
    conjunto es el frente abierto. Se declara en vez de simularse."""
    st.markdown(
        f'<div style="border:1px dashed {C.V_BD_FUERTE};border-radius:10px;'
        f'padding:16px 18px;font-size:12px;color:{C.V_TX2};line-height:1.7">'
        f'<b style="color:{C.V_TX}">Verificación conjunto por conjunto — en '
        f'preparación.</b><br>'
        f'La metodología está escrita y el catálogo tiene los <b>24 conjuntos '
        f'de datos</b> que la Guía Metodológica de la Defensoría exige, cada uno '
        f'trazado a su numeral de ley. La Guía está en el corpus verificada con '
        f'su huella digital.<br><br>'
        f'Falta ingerir el <b>Instructivo de Monitoreo</b>, que es la norma que '
        f'define <i>cómo</i> se evalúa —escala y criterios—. Sin él, una '
        f'calificación citaría una fuente que el sistema no tiene verificada, '
        f'que es exactamente el defecto que esta metodología vino a corregir.'
        f'<br><br>Mientras tanto, el <b>estado de la operación</b> muestra el '
        f'cumplimiento mes a mes que el portal ya acredita.</div>',
        unsafe_allow_html=True)


def render() -> None:
    """Ambiente Observatorio."""
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
    <span style="line-height:0">{logo("marfil", 26)}</span>
    <div>
      <div style="font-size:14px;font-weight:800;color:{C.V_TX}">
        Observatorio de Integridad Territorial</div>
      <div style="font-size:10px;color:{C.V_TX2}">Monitoreo progresivo de la
        gestión pública territorial · evidencia verificable</div>
    </div>
</div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["◷ Estado de la operación",
                      "🗓 Monitoreo mensual de transparencia"])
    with t1:
        _tab_estado()
    with t2:
        _tab_monitoreo()
