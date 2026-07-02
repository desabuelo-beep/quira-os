"""
QUIRA OS — QINV-009 · Rendición de Cuentas · lectura documental (réplica del molde)
═══════════════════════════════════════════════════════════════════════════════
Réplica del patrón de Planificación (ADR-031), reusando el lenguaje visual del molde.
Backbone de RDC = la TRIANGULACIÓN: narrativa oficial (discurso) ↔ evidencia física/
financiera ↔ informe CPCCS. Dos pilares:
  1. FIDELIDAD NARRATIVA (H34b) — lo dicho ↔ lo probado · el diferenciador
  2. REPORTE CPCCS (H31) — marco y compromisos (LOPC Art. 88)
El Presupuesto Participativo (H10b) NO va aquí: es de Participación Ciudadana (d08),
su dueño por la pregunta que responde (incidencia ciudadana). Ruteo · Javo 2026-07-02.

Datos del canon vía snapshot (Regla 1). Firewall: lenguaje de gobernanza, sin códigos.
Dylus Lab © 2026
"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from quira_pages.m_planificacion import _css, _head, _intro, _narr, _div, _tbl, _show

_T = {"critico": "#FF5A5A", "alerta": "#FFB020", "verde": "#2DD46F", "normal": "#22D3EE", "dim": "#7E8BA3"}


def _cargar() -> dict:
    try:
        from utils.cache_quira import cargar_gm_snapshot
        return (cargar_gm_snapshot() or {}).get("rendicion") or {}
    except Exception:
        return {}


# ═══════════════════════ gráficos ═══════════════════════
def _fid_bar(claims: list[dict]) -> go.Figure:
    top = list(reversed(claims))
    labels = [(c["meta"][:30] + "…") if len(c["meta"]) > 31 else c["meta"] for c in top]
    vals = [c["if_n"] * 100 for c in top]
    colors = [_T.get(c["temp"], "#7E8BA3") for c in top]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h", marker=dict(color=colors),
        text=[f"{v:.0f}%" for v in vals], textposition="auto",
        textfont=dict(family="JetBrains Mono", color="#0A0F19", size=12),
        hoverinfo="skip", cliponaxis=False, width=0.7))
    fig.add_vline(x=85, line=dict(color="#2DD46F", width=1, dash="dot"))
    fig.update_xaxes(visible=False, range=[0, 108])
    fig.update_yaxes(tickfont=dict(color="#B8C4D6", size=10.5))
    return fig


# ═══════════════════════ tablas ═══════════════════════
def _tabla_claims(claims: list[dict]) -> str:
    rows = ""
    for c in claims:
        col = _T.get(c["temp"], "#7E8BA3")
        rows += (f'<tr><td class="mt-meta" style="min-width:140px">{c["entidad"]}'
                 f'<div style="color:#7E8BA3;font-size:10.5px;margin-top:2px">{c["timestamp"]} · {c["categoria"]}</div></td>'
                 f'<td style="min-width:230px;color:#DCE4F0;font-style:italic;padding:9px 12px;'
                 f'border-bottom:1px solid rgba(255,255,255,.05)">“{c["discurso"]}”</td>'
                 f'<td style="min-width:230px;color:#AEB9CC;padding:9px 12px;'
                 f'border-bottom:1px solid rgba(255,255,255,.05)">{c["evidencia"]}</td>'
                 f'<td style="text-align:center;white-space:nowrap;padding:9px 12px;'
                 f'border-bottom:1px solid rgba(255,255,255,.05)">'
                 f'<div style="color:{col};font-weight:900;font-size:15px">{c["if_n"]*100:.0f}%</div>'
                 f'<div style="color:{col};font-size:10px;font-weight:700">{c["clasificacion"]}</div></td></tr>')
    return _tbl(["Ente · momento del video", "Lo que se DIJO (rendición oficial)",
                 "Lo que muestra la EVIDENCIA", "Fidelidad"], rows, mh=480)


# ═══════════════════════ serie 3 años ═══════════════════════
def _serie_bar(serie: list[dict]) -> go.Figure:
    xs = [s["periodo"] for s in serie]
    ys = [s.get("asistentes") or 0 for s in serie]
    fig = go.Figure(go.Bar(
        x=xs, y=ys, marker=dict(color="#22D3EE"), text=[str(v) for v in ys], textposition="outside",
        textfont=dict(family="JetBrains Mono", color="#F0F4FA", size=15), hoverinfo="skip", width=0.5))
    fig.update_xaxes(tickfont=dict(color="#B8C4D6", size=13))
    fig.update_yaxes(visible=False, range=[0, (max(ys) * 1.28) if ys else 1])
    return fig


def _tabla_serie_rdc(serie: list[dict]) -> str:
    rows = ""
    for s in serie:
        rows += (f'<tr><td class="mt-meta">RDC {s["periodo"]}</td><td class="mt-id">N° {s["informe_n"]}</td>'
                 f'<td class="mt-dir">{s["fecha_rdc"]}</td><td class="mt-dir">{s["lugar"]}</td>'
                 f'<td class="mt-num">{s.get("asistentes") or "—"}</td>'
                 f'<td class="mt-num">{s.get("n_componentes", 0)}</td></tr>')
    return _tbl(["Período", "Informe", "Fecha RDC", "Lugar", "Asistentes", "Componentes"], rows, mh=200)


def _tabla_cumplimiento(comps: list[dict]) -> str:
    rows = ""
    for c in comps:
        rows += (f'<tr><td class="mt-meta" style="min-width:210px">{c["componente"]}</td>'
                 f'<td style="color:#AEB9CC;padding:9px 12px;border-bottom:1px solid rgba(255,255,255,.05)">'
                 f'{c.get("resultado") or "—"}</td></tr>')
    return _tbl(["Componente del plan de trabajo", "Resultado reportado (informe oficial)"], rows, mh=380)


# ═══════════════════════ secciones ═══════════════════════
def _sec_serie(serie: list[dict]) -> None:
    if not serie:
        return
    st.markdown(_head("1", "LA RENDICIÓN EN EL TIEMPO",
                      "tres ciclos de rendición ante la ciudadanía · 2023-2025"), unsafe_allow_html=True)
    st.markdown(_intro(
        "La rendición de cuentas es un <b>ejercicio anual y obligatorio</b> ante la ciudadanía y el CPCCS "
        "<span class='pl-law'>Constitución · Art. 204</span> <span class='pl-law'>LOPC · Art. 88</span>. Aquí, "
        "los tres informes oficiales del período, con su evolución verificable —número de informe, fecha, lugar "
        "y asistencia ciudadana:"), unsafe_allow_html=True)
    st.markdown(_tabla_serie_rdc(serie), unsafe_allow_html=True)
    if any(s.get("asistentes") for s in serie):
        c1, c2 = st.columns([1.15, 1], gap="large")
        with c1:
            _show(_serie_bar(serie), 250)
        with c2:
            a0 = serie[0].get("asistentes") or 0
            aN = serie[-1].get("asistentes") or 0
            delta = f"+{100 * (aN - a0) / a0:.0f}%" if a0 else "—"
            st.markdown(_narr(
                f"La <b>asistencia ciudadana</b> a la rendición creció de <b>{a0}</b> ({serie[0]['periodo']}) a "
                f"<b>{aN}</b> ({serie[-1]['periodo']}) —<b>{delta}</b>—: el control social no se debilita, se "
                f"fortalece. Y el informe se hace más detallado año a año ({serie[0].get('n_componentes', 0)} → "
                f"{serie[-1].get('n_componentes', 0)} componentes), señal de una rendición que profundiza en vez "
                f"de simplificar."), unsafe_allow_html=True)


def _sec_cumplimiento(cumpl: dict) -> None:
    comps = (cumpl or {}).get("componentes", [])
    if not comps:
        return
    per = (cumpl or {}).get("periodo", "")
    st.markdown(_head("2", "EL CUMPLIMIENTO REPORTADO",
                      f"lo que la autoridad declara haber ejecutado · informe {per}"), unsafe_allow_html=True)
    st.markdown(_intro(
        f"El cuerpo de la rendición: <b>{len(comps)} componentes del plan de trabajo</b> y el resultado que la "
        f"autoridad reporta haber logrado en cada uno (informe oficial {per}). Es la <b>narrativa del "
        f"cumplimiento</b> —lo que se afirma—; el paso siguiente es contrastarla con la evidencia (la fidelidad "
        f"narrativa, más abajo):"), unsafe_allow_html=True)
    st.markdown(_tabla_cumplimiento(comps), unsafe_allow_html=True)


def _sec_fidelidad(fid: dict) -> None:
    claims = fid.get("claims", [])
    g = fid.get("global_pct") or 0
    n_alta = fid.get("n_alta", 0)
    n_baja = fid.get("n_baja", 0)
    st.markdown(_head("3", "LA FIDELIDAD NARRATIVA",
                      "lo que se dijo ↔ lo que muestra la evidencia · el corazón de la rendición"),
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="pl-cov" style="border-color:rgba(34,211,238,.28);border-left-color:#22D3EE;'
        f'background:linear-gradient(90deg,rgba(34,211,238,.10),rgba(34,211,238,.02))">'
        f'<div class="pl-cov-row"><span class="pl-cov-val" style="color:#22D3EE">{g:.0f}%</span>'
        f'<span class="pl-cov-lbl">de <b>fidelidad narrativa</b>: de {len(claims)} afirmaciones del informe oficial '
        f'de rendición, <b>{n_alta} coinciden</b> con la evidencia verificada y <b>{n_baja} registran brecha</b> '
        f'entre lo dicho y lo probado</span></div>'
        f'<div class="pl-cov-note">La rendición de cuentas no es un discurso: es la <b>correspondencia '
        f'verificable</b> entre lo que la autoridad afirma ante la ciudadanía y lo que la evidencia documental '
        f'demuestra. Se triangula <b>afirmación por afirmación</b> el discurso del video oficial con la prueba '
        f'física y financiera (eSIGEF, PAC, actas, oficios). Cada una recibe un <b>índice de fidelidad</b>: 100% = '
        f'lo dicho coincide con lo probado; bajo = brecha. Es el control ciudadano hecho evidencia, no opinión.</div>'
        f'</div>', unsafe_allow_html=True)
    st.markdown(_intro(
        "El marco lo exige: la rendición de cuentas es obligatoria y verificable "
        "<span class='pl-law'>Constitución · Art. 204</span> <span class='pl-law'>LOPC · Art. 88</span>. "
        "A continuación, cada afirmación pública del video de rendición, contrastada con su evidencia:"),
        unsafe_allow_html=True)
    st.markdown(_tabla_claims(claims), unsafe_allow_html=True)
    if claims:
        baja = [c for c in claims if c["temp"] == "critico"]
        c1, c2 = st.columns([1.15, 1], gap="large")
        with c1:
            _show(_fid_bar(claims), 330)
        with c2:
            _extra = ""
            if baja:
                b = baja[0]
                _extra = (f" La afirmación con mayor brecha es la de <b>{b['entidad']}</b> "
                          f"(“{b['discurso'][:60]}…”), donde la evidencia difiere del dato declarado.")
            st.markdown(_narr(
                f"Cada barra es una afirmación, medida por su fidelidad a la evidencia; la línea marca el umbral de "
                f"<b>fidelidad alta (85%)</b>. <b>{n_alta} de {len(claims)}</b> superan el umbral —la palabra "
                f"oficial se sostiene en el hecho—.{_extra} No es acusación: es señalar dónde la narrativa y la "
                f"evidencia deben reconciliarse, con la prueba a la vista."), unsafe_allow_html=True)


def _sec_cpccs(cp: dict) -> None:
    st.markdown(_head("4", "EL CIRCUITO CPCCS",
                      "la rendición formal ante el órgano de control social"),
                unsafe_allow_html=True)
    brecha = cp.get("brecha_compromisos") or "—"
    st.markdown(_intro(
        f"Más allá del discurso, la rendición tiene un <b>circuito formal</b> ante el Consejo de Participación "
        f"Ciudadana y Control Social (CPCCS): informe estructurado, compromisos y su seguimiento "
        f"<span class='pl-law'>LOPC · Art. 88</span> <span class='pl-law'>Constitución · Art. 204</span>. El "
        f"indicador clave es la <b>brecha de compromisos</b> —cuánto de lo prometido en la rendición anterior se "
        f"cumplió—: <b>{brecha}</b>. Es la memoria que impide que la rendición sea un acto de un solo día."),
        unsafe_allow_html=True)


def _cierre_rdc(r: dict) -> None:
    fid = r.get("fidelidad", {})
    g = fid.get("global_pct") or 0
    n_alta, n_baja = fid.get("n_alta", 0), fid.get("n_baja", 0)
    n = fid.get("n_afirmaciones", 0)
    serie = r.get("serie", [])
    st.markdown(
        f'<div class="pl-cierre">'
        f'<div class="pl-cierre-lbl">Síntesis ejecutiva — la rendición, verificada</div>'
        f'<div class="pl-syn-row"><span class="pl-syn-c">Ejercicio · sostenido</span>'
        f'<span class="pl-syn-t">Rendición cumplida los <b>{len(serie)} años</b> (2023-2025) con asistencia '
        f'ciudadana <b>creciente</b> —el control social se consolida, no se debilita.</span></div>'
        f'<div class="pl-syn-row"><span class="pl-syn-c">Fidelidad · discurso ↔ hecho</span>'
        f'<span class="pl-syn-t"><b>{g:.0f}%</b> de fidelidad narrativa: de {n} afirmaciones públicas, {n_alta} se '
        f'sostienen en la evidencia y {n_baja} registra brecha a reconciliar. La palabra oficial, contrastada con '
        f'la prueba documental.</span></div>'
        f'<div class="pl-syn-row"><span class="pl-syn-c">Control · circuito CPCCS</span>'
        f'<span class="pl-syn-t">La rendición formal ante el Consejo de Participación Ciudadana y Control Social '
        f'cierra el círculo: lo prometido se sigue año a año, no se diluye en un acto de un solo día.</span></div>'
        f'<div class="pl-cierre-txt" style="margin-top:15px">En conjunto, la rendición de cuentas de Montecristi '
        f'<b>resiste el contraste con la evidencia</b>: la mayoría de las afirmaciones se sostienen en la prueba '
        f'documental. El valor de esta lectura es que ese contraste <b>ya no depende de la confianza</b> —está '
        f'documentado y es verificable, afirmación por afirmación, con la evidencia a la vista.</div>'
        f'<div class="pl-src">Fuente: informe de rendición oficial · eSIGEF · PAC · actas CPCCS · corte 2024.</div>'
        f'</div>', unsafe_allow_html=True)


def render() -> None:
    """QINV-009 · Rendición de Cuentas — lectura documental continua (réplica del molde)."""
    r = _cargar()
    st.markdown(_css(), unsafe_allow_html=True)
    st.markdown('<div class="pl-wrap">', unsafe_allow_html=True)
    if not r or not r.get("fidelidad"):
        st.markdown('<div style="font-size:15px;color:#7E8BA3;padding:20px 0">'
                    '— evidencia de rendición pendiente de carga —</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown(
        '<div class="pl-title-band"><div class="pl-title">Rendición de Cuentas</div>'
        '<div class="pl-sub"><b>La palabra pública, contrastada con la evidencia.</b> Triangula lo que la '
        'autoridad afirma en su rendición con la prueba física y financiera verificable, y con el circuito formal '
        'de control social. Donde el discurso y el hecho coinciden, hay integridad; donde difieren, la brecha '
        'queda a la vista. <b>Serie 2023-2025 · fidelidad narrativa del ejercicio 2024.</b></div></div>',
        unsafe_allow_html=True)

    _sec_serie(r.get("serie", []))
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_cumplimiento(r.get("cumplimiento_actual", {}))
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_fidelidad(r.get("fidelidad", {}))
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_cpccs(r.get("cpccs", {}))
    _cierre_rdc(r)
    st.markdown('</div>', unsafe_allow_html=True)
