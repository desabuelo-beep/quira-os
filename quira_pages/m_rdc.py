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


def _ley_bloque(arts: list[str], gloss: str = "") -> str:
    """Marco legal como bloque SEPARADO debajo del párrafo (patrón de Planificación
    · _ley_row): las citas no van dentro del texto, sino en chips + glosa aparte."""
    chips = " ".join(f'<span class="pl-law">{a}</span>' for a in arts)
    g = f'<div style="margin-top:7px;color:#8493A8;font-style:italic">{gloss}</div>' if gloss else ""
    return f'<div class="pl-lawrow">⚖ <b>Marco legal vigente:</b><br>{chips}{g}</div>'


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
        "La rendición de cuentas es un <b>ejercicio anual y obligatorio</b> ante la ciudadanía y el Consejo de "
        "Participación Ciudadana y Control Social. Aquí, los tres informes oficiales del período, con su evolución "
        "verificable —número de informe, fecha, lugar y asistencia ciudadana:"), unsafe_allow_html=True)
    st.markdown(_ley_bloque(["Constitución · Art. 204", "LOPC · Art. 88"],
                            "Toda autoridad electa rinde cuentas una vez al año ante la ciudadanía y el CPCCS; el "
                            "proceso es público, obligatorio y verificable."), unsafe_allow_html=True)
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
        "El marco lo exige: la rendición de cuentas es <b>obligatoria y verificable</b>. A continuación, cada "
        "afirmación pública del video de rendición, contrastada con su evidencia:"),
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
        f"Ciudadana y Control Social (CPCCS): informe estructurado, compromisos y su seguimiento. El indicador "
        f"clave es la <b>brecha de compromisos</b> —cuánto de lo prometido en la rendición anterior se cumplió—: "
        f"<b>{brecha}</b>. Es la memoria que impide que la rendición sea un acto de un solo día."),
        unsafe_allow_html=True)
    st.markdown(_ley_bloque(["LOPC · Art. 88", "Constitución · Art. 204"],
                            "El CPCCS recibe y da seguimiento a los compromisos que la autoridad adquiere en la "
                            "rendición; el ciclo no se agota en el evento anual."), unsafe_allow_html=True)


# ═══════════════════════ APORTES CIUDADANOS (demanda → ejecución) ═══════════════
_AP_ESTADO = {"atendido": ("Atendido", "#2DD46F"),
              "por_validar": ("En seguimiento", "#FFB020"),
              "sin_correlato": ("Sin correlato", "#7E8BA3")}
_AP_TIEMPO = {"a_tiempo": "A tiempo", "tarde": "Con demora", "olvidado": "Sin correlato"}
_MINI_H = ('<div style="font-size:11.5px;font-weight:700;color:#B8C4D6;text-transform:uppercase;'
           'letter-spacing:.04em;margin:0 0 6px 2px">{}</div>')


def _aportes_tiempo_bar(pt: dict) -> go.Figure:
    orden = [("a_tiempo", "#2DD46F"), ("tarde", "#FFB020"), ("olvidado", "#7E8BA3")]
    labels = [_AP_TIEMPO[k] for k, _ in orden]
    vals = [pt.get(k, 0) for k, _ in orden]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h", marker=dict(color=[c for _, c in orden]),
        text=[str(v) for v in vals], textposition="auto",
        textfont=dict(family="JetBrains Mono", color="#0A0F19", size=13),
        hoverinfo="skip", cliponaxis=False, width=0.62))
    fig.update_xaxes(visible=False, range=[0, (max(vals) * 1.22) if any(vals) else 1])
    fig.update_yaxes(tickfont=dict(color="#DCE4F0", size=12.5), autorange="reversed")
    return fig


def _aportes_eje_bar(pe: dict) -> go.Figure:
    ejes = [e for e in sorted(pe, key=lambda k: -pe[k]["total"]) if e != "—"]
    tot = [pe[e]["total"] for e in ejes]
    at = [pe[e]["atendidos"] for e in ejes]
    fig = go.Figure()
    fig.add_bar(x=tot, y=ejes, orientation="h", marker=dict(color="rgba(126,139,163,.26)"),
                text=[str(v) for v in tot], textposition="outside",
                textfont=dict(color="#7E8BA3", size=11), hoverinfo="skip", width=0.62)
    fig.add_bar(x=at, y=ejes, orientation="h", marker=dict(color="#22D3EE"),
                hoverinfo="skip", width=0.62)
    fig.update_layout(barmode="overlay", showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
    fig.update_xaxes(visible=False, range=[0, (max(tot) * 1.2) if tot else 1])
    fig.update_yaxes(tickfont=dict(color="#B8C4D6", size=10.5))
    return fig


def _tabla_aportes(detalle: list[dict]) -> str:
    # muestra representativa de los TRES estados (transparencia de ambos lados)
    def _by(estado):
        return sorted([d for d in detalle if d["estado"] == estado], key=lambda d: -d["score"])
    sel = _by("atendido")[:10] + _by("por_validar")[:6] + _by("sin_correlato")[:6]
    rows = ""
    for d in sel:
        label, col = _AP_ESTADO.get(d["estado"], ("—", "#7E8BA3"))
        ev = d["evidencia"] or "— sin obra o servicio correlativo en el período —"
        yr = f' · {d["anio_ejecucion"]}' if d.get("anio_ejecucion") else ""
        rows += (f'<tr><td class="mt-meta" style="min-width:200px">{d["demanda"]}'
                 f'<div style="color:#7E8BA3;font-size:10.5px;margin-top:2px">{d["eje"]} · pedido {d["anio_aporte"]}</div></td>'
                 f'<td style="min-width:230px;color:#AEB9CC;padding:9px 12px;'
                 f'border-bottom:1px solid rgba(255,255,255,.05)">{ev}</td>'
                 f'<td style="text-align:center;white-space:nowrap;padding:9px 12px;'
                 f'border-bottom:1px solid rgba(255,255,255,.05)">'
                 f'<div style="color:{col};font-weight:800;font-size:12.5px">{label}{yr}</div></td></tr>')
    return _tbl(["Demanda ciudadana (rendición)", "Obra o servicio que la atiende (ejecución)", "Estado"],
                rows, mh=460)


def _sec_aportes(ap: dict) -> None:
    det = ap.get("detalle", [])
    if not det:
        return
    total = ap.get("total", len(det))
    est = ap.get("por_estado", {})
    n_at = est.get("atendido", 0)
    n_sin = est.get("sin_correlato", 0)
    pct = round(100 * n_at / total) if total else 0
    st.markdown(_head("5", "LA VOZ CIUDADANA",
                      "de lo que se pidió a lo que se ejecutó · trazabilidad del aporte ciudadano"),
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="pl-cov" style="border-color:rgba(45,212,111,.28);border-left-color:#2DD46F;'
        f'background:linear-gradient(90deg,rgba(45,212,111,.10),rgba(45,212,111,.02))">'
        f'<div class="pl-cov-row"><span class="pl-cov-val" style="color:#2DD46F">{pct}%</span>'
        f'<span class="pl-cov-lbl">de los <b>{total} aportes ciudadanos</b> del período tienen '
        f'<b>correspondencia verificada</b> con una obra o servicio del gobierno (<b>{n_at}</b> atendidos); '
        f'<b>{n_sin}</b> quedan sin correlato en la ejecución</span></div>'
        f'<div class="pl-cov-note">En la rendición, la ciudadanía plantea <b>demandas y aportes</b> —consultivos: '
        f'orientan la gestión—. QUIRA rastrea cada aporte hasta la <b>ejecución real</b> (el POA, la contratación, '
        f'el presupuesto) a lo largo de <b>todo el período de gobierno</b>, no solo del año siguiente. Así distingue '
        f'lo atendido <b>a tiempo</b>, lo atendido <b>con demora</b> y lo que <b>quedó sin correlato</b>. Cada '
        f'correspondencia se propone por análisis y se <b>confirma afirmación por afirmación</b>.</div>'
        f'</div>', unsafe_allow_html=True)
    st.markdown(_ley_bloque(["LOPC · Art. 89", "COOTAD · Art. 238"],
                            "Los aportes ciudadanos en la rendición son consultivos (orientan la gestión); se "
                            "distinguen del presupuesto participativo, que sí es vinculante."), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.15], gap="large")
    with c1:
        st.markdown(_MINI_H.format("Tiempo de respuesta del gobierno"), unsafe_allow_html=True)
        _show(_aportes_tiempo_bar(ap.get("por_tiempo", {})), 210)
    with c2:
        st.markdown(_MINI_H.format("Aportes por eje del PDOT · con correspondencia"), unsafe_allow_html=True)
        _show(_aportes_eje_bar(ap.get("por_eje", {})), 210)
    st.markdown(_intro(
        "La trazabilidad, aporte por aporte: la demanda que la ciudadanía planteó en la rendición, junto a la "
        "<b>obra o servicio</b> del gobierno que la atiende y el <b>año</b> en que se ejecutó. La evidencia al "
        "lado —no es opinión, es correspondencia verificable:"), unsafe_allow_html=True)
    st.markdown(_tabla_aportes(det), unsafe_allow_html=True)


def _cierre_rdc(r: dict) -> None:
    fid = r.get("fidelidad", {})
    g = fid.get("global_pct") or 0
    n_alta, n_baja = fid.get("n_alta", 0), fid.get("n_baja", 0)
    n = fid.get("n_afirmaciones", 0)
    serie = r.get("serie", [])
    ap = r.get("aportes", {})
    ap_tot = ap.get("total", 0)
    _ae = ap.get("por_estado", {})
    ap_pct = round(100 * (_ae.get("atendido", 0) + _ae.get("por_validar", 0)) / ap_tot) if ap_tot else 0
    ap_row = ("" if not ap_tot else
              f'<div class="pl-syn-row"><span class="pl-syn-c">Voz ciudadana · aporte→obra</span>'
              f'<span class="pl-syn-t">De <b>{ap_tot} aportes</b> ciudadanos del período, <b>{ap_pct}%</b> tienen '
              f'correspondencia con la ejecución —lo pedido se rastrea hasta la obra, a lo largo de todo el período '
              f'de gobierno, no solo el año siguiente.</span></div>')
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
        f'{ap_row}'
        f'<div class="pl-cierre-txt" style="margin-top:15px">En conjunto, la rendición de cuentas de Montecristi '
        f'<b>resiste el contraste con la evidencia</b>: la mayoría de las afirmaciones se sostienen en la prueba '
        f'documental. El valor de esta lectura es que ese contraste <b>ya no depende de la confianza</b> —está '
        f'documentado y es verificable, afirmación por afirmación, con la evidencia a la vista.</div>'
        f'<div class="pl-src">Fuente: informe de rendición oficial · eSIGEF · PAC · actas CPCCS · corte 2024.</div>'
        f'</div>', unsafe_allow_html=True)


def _sec_verificabilidad(rdc_serie=None, aportes=None) -> None:
    """Cajón de VERIFICABILIDAD PÚBLICA DEL DISCURSO del DOMINIO (Motor Narrativo): explicación
    compartida + LA RENDICIÓN EN EL TIEMPO (intro) + análisis por año + evaluación + síntesis, SIN
    duplicar lo explicativo (Javo · 2026-07-10). Snapshot → HTML (Regla 1: la app NO corre el motor)."""
    import json
    from pathlib import Path
    base = Path(__file__).resolve().parents[1] / "data" / "motor_narrativo" / "snapshots"

    def _load(a):
        p = base / f"verificabilidad_{a}.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    serie = [s for s in (_load("2024"), _load("2025")) if s]
    if not serie:
        return
    try:
        from app.viz.render.html_render import cajon_dominio_streamlit
    except Exception:
        return
    st.markdown(cajon_dominio_streamlit(serie, rdc_serie, aportes), unsafe_allow_html=True)


def render() -> None:
    """QINV-009 · Rendición de Cuentas — cajón de DOMINIO (Motor Narrativo): explicación + serie +
    análisis por año + evaluación + síntesis, en una sola pieza (Javo · 2026-07-10)."""
    r = _cargar()
    st.markdown(_css(), unsafe_allow_html=True)
    _sec_verificabilidad(r.get("serie") if r else None,   # cajón del DOMINIO — serie + aportes integrados
                         r.get("aportes") if r else None)
