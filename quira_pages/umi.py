"""
QUIRA OS — UMI · Unidad Metodológica de Investigación
═══════════════════════════════════════════════════════════════════════════════
El MOLDE UNIVERSAL del expediente de inteligencia institucional. Las 13
investigaciones (los dominios) heredan EXACTAMENTE esta anatomía de 4 momentos:

  1. PREGUNTA FORENSE      — el encabezado soberano (reemplaza el título del widget)
  2. EVIDENCIA (50% izq)   — la prueba física e incontestable del motor (cosecha)
  3. PERITAJE QUIRA (50% der) — el dictamen vinculante del perito (causa, no síntoma)
  4. CONCLUSIÓN EJECUTIVA  — el veredicto que el alcalde necesita para actuar en segundos

NO es gobernanza, NO es un documento, NO es un ADR: es el componente de render
reutilizable (forma · ADR-030 · regla 50/50). El contenido lo provee cada dominio
desde el canon (Diccionario · motor). Aquí solo vive la ESTRUCTURA.

"QUIRA no visualiza datos: construye expedientes de inteligencia institucional
para la toma de decisiones." — la mesa, 2026-06-21.

Dylus Lab © 2026
"""
from __future__ import annotations

from typing import Callable, Sequence

import streamlit as st

# Paleta soberana — consistente con el Centro de Mando v2 (firewall: sin códigos internos)
_TEMP: dict[str, str] = {
    "critico": "#FF4D4D",
    "alerta": "#FFB020",
    "normal": "#00D4FF",
    "verde": "#22C55E",
    "dim": "#5A6B7E",
}
_IA = "#00D4FF"  # el color del perito (QUIRA)


def _css(color: str) -> str:
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
.umi-wrap, .umi-wrap * {{ font-family:'Inter',system-ui,sans-serif; }}

/* 1 · Pregunta forense */
.umi-badge {{ font-family:'JetBrains Mono',monospace; font-size:10.5px; font-weight:700;
  letter-spacing:.14em; color:{color}; text-transform:uppercase; }}
.umi-pregunta {{ font-size:27px; font-weight:800; color:#E8EDF4; line-height:1.18;
  margin:4px 0 2px; max-width:62ch; }}
.umi-dato {{ font-family:'JetBrains Mono',monospace; font-size:30px; font-weight:900;
  color:{color}; line-height:1; text-align:right; }}
.umi-estado {{ font-size:9.5px; font-weight:800; letter-spacing:.06em; color:{color};
  border:1px solid {color}55; border-radius:11px; padding:3px 11px; }}

/* secciones evidencia / peritaje */
.umi-sec {{ font-family:'JetBrains Mono',monospace; font-size:10.5px; font-weight:700;
  letter-spacing:.1em; margin:2px 0 8px; }}
.umi-sec-ev {{ color:#8892B0; }}
.umi-sec-ia {{ color:{_IA}; }}

/* peritaje — el dictamen */
.umi-perito {{ background:rgba(0,212,255,.04); border:1px solid rgba(0,212,255,.22);
  border-left:3px solid {_IA}; border-radius:12px; padding:14px 16px; }}
.umi-perito-head {{ font-size:12px; font-weight:800; color:{_IA}; margin-bottom:9px; }}
.umi-dic {{ display:flex; gap:9px; align-items:flex-start; margin-bottom:9px;
  font-size:12.5px; color:#C7D2E0; line-height:1.5; }}
.umi-dic b {{ color:#E8EDF4; }}
.umi-dic-mk {{ color:{_IA}; font-weight:800; flex-shrink:0; }}

/* 4 · conclusión ejecutiva */
.umi-concl {{ background:rgba(255,255,255,.02); border:1px solid rgba(255,255,255,.09);
  border-radius:14px; padding:16px 18px; margin-top:6px; }}
.umi-concl-lbl {{ font-size:10.5px; font-weight:800; letter-spacing:.1em; color:#8892B0;
  text-transform:uppercase; }}
.umi-bar {{ height:13px; background:rgba(255,255,255,.07); border-radius:8px;
  overflow:hidden; margin:7px 0 4px; }}
.umi-bar-fill {{ height:100%; background:{color}; border-radius:8px; }}
.umi-bigpct {{ font-family:'JetBrains Mono',monospace; font-size:34px; font-weight:900;
  color:{color}; line-height:1; }}
.umi-chip {{ display:inline-block; font-size:11px; font-weight:700; border-radius:9px;
  padding:4px 11px; }}
.umi-concl-txt {{ font-size:13px; color:#C7D2E0; line-height:1.55; margin-top:6px; }}
hr.umi-div {{ border:none; border-top:1px solid rgba(255,255,255,.08); margin:10px 0; }}
</style>"""


def _peritaje_html(headline: str, dictamenes: Sequence[str]) -> str:
    head = f'<div class="umi-perito-head">◎ QUIRA dictamina</div>'
    lead = f'<div class="umi-dic"><b>{headline}</b></div>' if headline else ""
    cuerpo = "".join(
        f'<div class="umi-dic"><span class="umi-dic-mk">▸</span><span>{d}</span></div>'
        for d in dictamenes
    )
    return f'<div class="umi-perito">{head}{lead}{cuerpo}</div>'


def render_investigacion(
    *,
    pregunta: str,
    badge: str = "",
    estado: str = "",
    dato: str = "",
    temp: str = "normal",
    evidencia: Callable[[], None] | None = None,
    peritaje_headline: str = "",
    peritaje: Sequence[str] = (),
    veredicto_label: str = "",
    veredicto_pct: int | None = None,
    divergencias: str = "",
    prioridad: str = "",
    prioridad_temp: str = "critico",
    conclusion: str = "",
    on_volver: Callable[[], None] | None = None,
) -> None:
    """Renderiza UNA investigación en el molde universal (4 momentos).

    Cada dominio la invoca con su contenido del canon. Ej. d06:

        render_investigacion(
            pregunta="¿Tiene esta institución capacidad para sostener el gobierno?",
            badge="06 · Salud Institucional · Investigación",
            estado="BAJO UMBRAL", dato="58.6%", temp="critico",
            evidencia=_evidencia_d06,          # cosecha del motor (prueba real)
            peritaje_headline="El deterioro es estructural, no coyuntural.",
            peritaje=["El cumplimiento está 11.4 pts bajo el umbral…", "…"],
            veredicto_label="Capacidad institucional",
            veredicto_pct=59, divergencias="4 dimensiones en rojo",
            prioridad="Prioridad 1 · sostenibilidad financiera",
            conclusion="La institución sostiene el gobierno, pero…",
        )
    """
    color = _TEMP.get(temp, _IA)
    st.markdown(_css(color), unsafe_allow_html=True)

    # ── 0 · Volver al Centro de Mando ────────────────────────────────────────
    if on_volver is not None:
        if st.button("← Volver al Centro de Mando", key="umi_volver"):
            on_volver()

    st.markdown('<div class="umi-wrap">', unsafe_allow_html=True)

    # ── 1 · PREGUNTA FORENSE (encabezado soberano) ───────────────────────────
    hcol, dcol = st.columns([4.6, 1.4])
    with hcol:
        st.markdown(
            f'<div class="umi-badge">{badge}</div>'
            f'<div class="umi-pregunta">{pregunta}</div>',
            unsafe_allow_html=True,
        )
    with dcol:
        st.markdown(
            f'<div style="text-align:right;padding-top:4px">'
            f'<div class="umi-dato">{dato}</div>'
            f'<div style="margin-top:7px"><span class="umi-estado">● {estado}</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="umi-div">', unsafe_allow_html=True)

    # ── 2 | 3 · EVIDENCIA (izq) | PERITAJE QUIRA (der) ───────────────────────
    col_e, col_p = st.columns(2, gap="large")
    with col_e:
        st.markdown(
            '<div class="umi-sec umi-sec-ev">▎ EVIDENCIA — la prueba del motor</div>',
            unsafe_allow_html=True,
        )
        if evidencia is not None:
            evidencia()
        else:
            st.markdown(
                '<div style="font-size:11px;color:#5A6B7E">— evidencia pendiente de cosecha —</div>',
                unsafe_allow_html=True,
            )
    with col_p:
        st.markdown(
            '<div class="umi-sec umi-sec-ia">▎ PERITAJE QUIRA — dictamen vinculante</div>',
            unsafe_allow_html=True,
        )
        if peritaje or peritaje_headline:
            st.markdown(_peritaje_html(peritaje_headline, peritaje), unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="font-size:11px;color:#5A6B7E">— peritaje en cómputo —</div>',
                unsafe_allow_html=True,
            )

    # ── 4 · CONCLUSIÓN EJECUTIVA (el veredicto para actuar) ───────────────────
    pct = max(0, min(100, int(veredicto_pct))) if veredicto_pct is not None else None
    barra = (
        f'<div class="umi-bar"><div class="umi-bar-fill" style="width:{pct}%"></div></div>'
        if pct is not None else ""
    )
    bigpct = f'<span class="umi-bigpct">{pct}%</span>' if pct is not None else ""
    pcolor = _TEMP.get(prioridad_temp, "#FF4D4D")
    div_html = (
        f'<span class="umi-concl-lbl">Divergencias</span><br>'
        f'<span style="font-size:15px;font-weight:800;color:#E8EDF4">{divergencias}</span>'
        if divergencias else ""
    )
    prio_html = (
        f'<span class="umi-chip" style="background:{pcolor}1f;color:{pcolor};'
        f'border:1px solid {pcolor}55">⚑ {prioridad}</span>'
        if prioridad else ""
    )
    concl_txt = f'<div class="umi-concl-txt">{conclusion}</div>' if conclusion else ""

    st.markdown(
        f'<div class="umi-concl">'
        f'<div class="umi-concl-lbl">Conclusión ejecutiva — {veredicto_label}</div>'
        f'<div style="display:flex;align-items:flex-end;gap:18px;margin-top:4px">'
        f'<div style="flex:1">{barra}</div>{bigpct}</div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'gap:14px;margin-top:10px;flex-wrap:wrap">'
        f'<div>{div_html}</div><div>{prio_html}</div></div>'
        f'{concl_txt}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('</div>', unsafe_allow_html=True)
