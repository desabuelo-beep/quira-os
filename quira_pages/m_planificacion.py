"""
QUIRA OS — QINV-001 · Planificación Estratégica · lectura documental (flujo único)
═══════════════════════════════════════════════════════════════════════════════
Reescritura 2026-07-01 (Javo): el cajón deja de ser un "expediente forense" y pasa
a ser una LECTURA DOCUMENTAL continua — sin pestañas, sin encabezado de investigación,
sin capa de IA (la IA es conversacional, en otra pantalla), sin memoria de diseño.
La gente REVISA todo aquí; si tiene dudas, consulta a QUIRA IA conversando (otra capa).

Estructura (un solo scroll, por eslabón de la columna vertebral):
  cobertura → resumen backbone → PDOT (tabla+gráfica+texto) → POA → PAC → PRESUPUESTO
  → COHERENCIA → cierre factual corto.

Ley INLINE por eslabón: un artículo VERIFICADO del corpus (sha256 · Regla 3 — no se
inventan). CE 241 (PDOT) · COOTAD 233 (POA) · LOSNCP 22 (PAC) · COOTAD 215/238
(presupuesto/priorización). Explicaciones en cards de color, ampliadas para no-expertos.
Cronograma con marcador de corte (plan ≠ ejecución). Firewall: ningún código interno.
Dylus Lab © 2026
"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

_UMBRAL = 70.0
_T = {"critico": "#FF5A5A", "alerta": "#FFB020", "verde": "#2DD46F",
      "normal": "#22D3EE", "dim": "#7E8BA3"}
_COMP = {"Exclusiva Crítica": "#22D3EE", "Concurrente Crítica": "#3BA7D9",
         "Exclusiva Importante": "#9AA6BE", "Concurrente": "#7E8BA3"}


def _cargar() -> dict:
    out: dict = {}
    try:
        from quira_pages.p_command_center import _load_data
        out.update(_load_data() or {})
    except Exception:
        pass
    try:
        from utils.cache_quira import cargar_gm_snapshot
        gm = cargar_gm_snapshot() or {}
        out["plan"] = gm.get("planificacion") or {}
    except Exception:
        out["plan"] = {}
    return out


# ═══════════════════════ Plotly — tema premium oscuro (fuentes ↑) ══════════════
def _show(fig: go.Figure, h: int = 260) -> None:
    fig.update_layout(
        height=h, margin=dict(l=4, r=8, t=8, b=4),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#B8C4D6", size=13), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _donut(comp: list[dict]) -> go.Figure:
    labels = [c["label"] for c in comp]
    vals = [c["n"] for c in comp]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.62, sort=False, direction="clockwise",
        marker=dict(colors=[_COMP.get(l, "#7E8BA3") for l in labels], line=dict(color="#0A0F19", width=2)),
        textinfo="value", textfont=dict(family="JetBrains Mono", color="#F0F4FA", size=16), hoverinfo="skip"))
    fig.add_annotation(text=f"<b>{sum(vals)}</b>", showarrow=False, y=0.52,
                       font=dict(family="JetBrains Mono", color="#F0F4FA", size=30))
    fig.add_annotation(text="metas", showarrow=False, y=0.28, font=dict(color="#7E8BA3", size=13))
    return fig


def _competencia_bar(comp: list[dict], metas: list[dict], poa_detalle: list[dict]) -> go.Figure:
    """Metas por tipo de competencia — número y presupuesto POA (más analítico que la dona)."""
    mcomp = {m["id"]: m.get("competencia", "") for m in metas}
    bud: dict = {}
    for x in poa_detalle:
        c = mcomp.get(x.get("id"), "")
        bud[c] = bud.get(c, 0) + (x.get("anual_usd", 0) or 0)
    order = ["Exclusiva Crítica", "Concurrente Crítica", "Exclusiva Importante", "Concurrente"]
    items = sorted(comp, key=lambda c: order.index(c["label"]) if c["label"] in order else 99, reverse=True)
    labels = [c["label"] for c in items]
    counts = [c["n"] for c in items]
    buds = [bud.get(c["label"], 0) for c in items]
    colors = [_COMP.get(l, "#7E8BA3") for l in labels]
    fig = go.Figure(go.Bar(
        x=counts, y=labels, orientation="h", marker=dict(color=colors),
        text=[f"  {n} metas · ${b/1e6:.1f}M" for n, b in zip(counts, buds)],
        textposition="outside", textfont=dict(family="Inter", color="#D2DBEA", size=12.5),
        hoverinfo="skip", cliponaxis=False, width=0.6))
    fig.update_xaxes(visible=False, range=[0, (max(counts) * 1.6) if counts else 1])
    fig.update_yaxes(tickfont=dict(color="#E8EDF4", size=12.5))
    return fig


def _brechas(cod: float, dev: float, pac: float) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=["Presupuesto<br>inversión", "Devengado<br>al corte", "PAC<br>contratado"],
        y=[cod, dev, pac], marker=dict(color=["#22D3EE", "#FFB020", "#6E8CA8"]),
        text=[f"${cod/1e6:.1f}M", f"${dev/1e6:.2f}M", f"${pac/1e3:.0f}k"],
        textposition="outside", textfont=dict(family="JetBrains Mono", color="#F0F4FA", size=15),
        hoverinfo="skip", cliponaxis=False, width=0.55))
    fig.update_xaxes(tickfont=dict(color="#B8C4D6", size=13))
    fig.update_yaxes(visible=False)
    return fig


def _cronograma(poa: list[dict], corte_idx: int = 4) -> go.Figure:
    """Ritmo PLANIFICADO mes a mes (100% plan del POA). `corte_idx` = meses con ejecución
    ingerida (Ene-Abr = 4) → marcador que separa el tramo ya transcurrido del plan futuro."""
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    serie = [0.0] * 12
    for x in poa:
        for i, v in enumerate(x.get("crono", [])[:12]):
            serie[i] += v if isinstance(v, (int, float)) else 0
    fig = go.Figure(go.Scatter(
        x=meses, y=serie, mode="lines", fill="tozeroy", line=dict(color="#22D3EE", width=3),
        fillcolor="rgba(34,211,238,0.12)", hoverinfo="skip"))
    # sombreado del tramo aún NO transcurrido (plan a futuro) + línea de corte
    _ymax = max(serie) * 1.15 if any(serie) else 1
    fig.add_vrect(x0=corte_idx - 0.5, x1=11.5, fillcolor="rgba(255,176,32,0.05)", line_width=0)
    fig.add_vline(x=corte_idx - 0.5, line=dict(color="#FFB020", width=1.5, dash="dot"))
    fig.add_annotation(x=corte_idx - 0.5, y=_ymax, text="corte · abril", showarrow=False,
                       font=dict(color="#FFB020", size=11), xanchor="left", xshift=4)
    fig.update_xaxes(tickfont=dict(color="#B8C4D6", size=12), showgrid=False)
    fig.update_yaxes(visible=False, range=[0, _ymax])
    return fig


def _pub_bar(pub: dict) -> go.Figure:
    """Procesos publicados en SERCOP por monto (lo que el municipio YA sacó a contratar)."""
    procs = sorted(pub.get("procesos", []), key=lambda x: x.get("monto", 0) or 0)

    def _lab(p):
        d = (p.get("desc") or "").strip()
        return (d[:32] + "…") if len(d) > 33 else (d or str(p.get("cod", ""))[-12:])

    labels = [_lab(p) for p in procs]
    vals = [p.get("monto", 0) or 0 for p in procs]
    colors = ["#FFB020" if v else "#3A4658" for v in vals]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h", marker=dict(color=colors),
        text=[f"${v:,.0f}" if v else "sin publicar" for v in vals],
        textposition="auto", textfont=dict(family="JetBrains Mono", color="#F0F4FA", size=12),
        hoverinfo="skip", cliponaxis=False, width=0.64))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(tickfont=dict(color="#B8C4D6", size=12))
    return fig


def _ipe_bar(por_obj: list[dict]) -> go.Figure:
    """Devengado de inversión vinculado, por objetivo del plan (barras horizontales)."""
    top = list(reversed(por_obj[:8]))            # mayor arriba
    labels = [(o["objetivo"][:36] + "…") if len(o["objetivo"]) > 37 else o["objetivo"] for o in top]
    vals = [o["dev"] for o in top]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h", marker=dict(color="#2DD46F"),
        text=[f"${v/1e3:.0f}k" for v in vals], textposition="auto",
        textfont=dict(family="JetBrains Mono", color="#F0F4FA", size=12),
        hoverinfo="skip", cliponaxis=False, width=0.66))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(tickfont=dict(color="#B8C4D6", size=11.5))
    return fig


# ═══════════════════════ HTML premium (fuentes ↑) ═══════════════════════
def _head(num: str, tit: str, sub: str) -> str:
    return (f'<div class="pl-h"><span class="pl-n">{num}</span><span class="pl-t">{tit}</span>'
            f'<span class="pl-s">{sub}</span></div>')


def _intro(txt: str) -> str:
    return f'<div class="pl-intro">{txt}</div>'


def _narr(txt: str) -> str:
    return f'<div class="pl-narr">{txt}</div>'


_LEY_NOMBRE = {"CE": "Constitución", "COOTAD": "COOTAD", "LOSNCP": "LOSNCP",
               "RLOSNCP": "Reglamento LOSNCP", "COPLAFIP": "COPLAFIP", "PND-2025": "Plan Nacional"}


def _ley_row(plan: dict, stage: str, gloss: str = "") -> str:
    """Marco legal vigente — artículos VERIFICADOS del corpus (sha256 · Regla 3). '' si no hay."""
    art = ((plan.get("base_normativa") or {}).get("por_eslabon") or {}).get(stage)
    if not art:
        return ""
    marco = art.get("marco")
    if marco:
        chips = " ".join(f'<span class="pl-law">{s}</span>' for s in marco)
        g = f'<div style="margin-top:7px;color:#8493A8;font-style:italic">{gloss}</div>' if gloss else ""
        return f'<div class="pl-lawrow">⚖ <b>Marco legal vigente:</b><br>{chips}{g}</div>'
    nom = _LEY_NOMBRE.get(art.get("norma"), art.get("norma", ""))
    return (f'<div class="pl-lawrow">⚖ <b>Fundamento legal:</b> '
            f'<span class="pl-law">{nom} · Art. {art.get("articulo", "")}</span> {gloss}</div>')


def _div() -> str:
    return '<hr class="pl-div">'


def _tbl(headers: list[str], rows: str, mh: int = 300) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    return (f'<div class="mt-wrap" style="max-height:{mh}px"><table class="mt">'
            f'<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')


def _tabla_metas(metas: list[dict]) -> str:
    rows = ""
    for m in metas:
        c = _COMP.get(m["competencia"], "#7E8BA3")
        rows += (f'<tr><td class="mt-id">{m["id"]}</td><td class="mt-sis">{m["sistema"]}</td>'
                 f'<td class="mt-meta">{m["meta"]}</td>'
                 f'<td><span class="mt-tag" style="color:{c};border-color:{c}55">{m["competencia"]}</span></td>'
                 f'<td class="mt-dir">{m["direccion"]}</td></tr>')
    return _tbl(["ID", "Sistema", "Meta plurianual 2023-2027", "Competencia", "Dirección"], rows)


def _tabla_proyectos(proys: list[dict]) -> str:
    rows = ""
    for x in proys:
        rows += (f'<tr><td class="mt-dir">{x["dir"]}</td><td class="mt-meta">{x["desc"]}</td>'
                 f'<td class="mt-id">{x["partida"]}</td>'
                 f'<td class="mt-num">${x["anual"]:,.0f}</td></tr>')
    return _tbl(["Dirección", "Proyecto / actividad", "Partida", "Monto anual"], rows, mh=360)


def _tabla_presupuesto(p: dict) -> str:
    filas = [("Bienes (inversión)", p.get("bienes", 0), "#9AA6BE"),
             ("Obras (inversión)", p.get("obras", 0), "#9AA6BE"),
             ("Codificado de inversión", p.get("codificado_inversion", 0), "#22D3EE"),
             ("Devengado al corte", p.get("devengado", 0), "#FFB020")]
    rows = ""
    for lab, val, col in filas:
        rows += (f'<tr><td class="mt-meta">{lab}</td>'
                 f'<td class="mt-num" style="color:{col}">${val:,.0f}</td></tr>')
    return _tbl(["Rubro", "Monto (USD)"], rows, mh=240)


def _tabla_publicado(procs: list[dict]) -> str:
    rows = ""
    for x in procs:
        monto = f'${x["monto"]:,.0f}' if x.get("monto") else "sin publicar"
        cod = str(x.get("cod", "")).replace("ocds-5wno2w-", "")
        et = str(x.get("etapa", ""))
        ec = "#2DD46F" if ("proceso" in et.lower() or "licit" in et.lower()) else "#FFB020"
        rows += (f'<tr><td class="mt-id">{cod}</td><td class="mt-meta">{x.get("desc", "")}</td>'
                 f'<td class="mt-dir">{x.get("partida", "") or "—"}</td>'
                 f'<td class="mt-num">{monto}</td>'
                 f'<td class="mt-dir">{x.get("monto_tipo", "")}</td>'
                 f'<td><span style="color:{ec};font-size:12px;font-weight:700">● {et}</span></td></tr>')
    return _tbl(["Proceso", "Objeto de contratación", "Partida", "Monto", "Valor", "Etapa"], rows)


def _tabla_pac(pac: list[dict]) -> str:
    """El PAC completo — cada proceso planificado, con su vínculo a meta y su coherencia."""
    rows = ""
    for x in pac:
        c = _T.get(x.get("alerta_temp", "dim"), "#7E8BA3")
        meta = x["meta"] if x.get("meta") and "[" not in x.get("meta", "") else "—"
        monto = f'${x["monto"]:,.0f}' if x.get("monto") else "por valorar"
        rows += (f'<tr><td class="mt-id">{x.get("id", "")}</td><td class="mt-meta">{x.get("desc", "")}</td>'
                 f'<td class="mt-dir">{x.get("tipo") or "—"}</td><td class="mt-num">{monto}</td>'
                 f'<td class="mt-id">{meta}</td>'
                 f'<td><span style="color:{c};font-size:12px;font-weight:700">● {x.get("alerta") or "—"}</span></td></tr>')
    return _tbl(["ID", "Proceso", "Tipo de procedimiento", "Monto ref.", "Meta", "Coherencia"], rows, mh=340)


def _pills(comps: list[dict]) -> str:
    out = ""
    for it in comps:
        c = _T.get(it.get("temp", "dim"), "#7E8BA3")
        out += (f'<div class="pl-pill" style="border-color:{c}3a"><span class="pl-pd" style="background:{c}"></span>'
                f'<span class="pl-pl">{it["label"]}</span><span class="pl-pe" style="color:{c}">{it["estado"]}</span></div>')
    return out


def _cruce(plan: dict) -> str:
    pr = plan.get("presupuesto", {}) or {}
    pac = plan.get("pac", {}) or {}
    _mt = plan.get("metas_total", 25)
    _np = len(plan.get("poa_proyectos", []))
    stages = [("PDOT", f'{_mt} metas', "el plan"),
              ("POA", f'{_np} proyectos', f'operan {_mt} metas'),
              ("PRESUPUESTO", f'${pr.get("codificado_inversion", 0)/1e6:.1f}M', "la inversión"),
              ("PAC", f'${pac.get("total_usd", 0)/1e6:.1f}M', "lo contratado"),
              ("EJECUCIÓN", f'${pr.get("devengado", 0)/1e6:.2f}M', f'{pr.get("ti_pct", 0)}% al corte')]
    arrows = ["#2DD46F", "#2DD46F", "#FFB020", "#FFB020"]
    html = '<div class="cr">'
    for i, (code, val, lab) in enumerate(stages):
        html += (f'<div class="cr-card"><div class="cr-c">{code}</div><div class="cr-v">{val}</div>'
                 f'<div class="cr-l">{lab}</div></div>')
        if i < len(arrows):
            html += f'<div class="cr-a" style="color:{arrows[i]}">→</div>'
    return html + '</div>'


def _publicado_band(pub: dict) -> str:
    cr = pub.get("cruce", {}) or {}
    plan = cr.get("plan_pac_usd", 0) or 0
    publ = cr.get("publicado_usd", 0) or 0
    pct = cr.get("cobertura_pct", 0) or 0
    n = pub.get("n_procesos", 0)
    corte = pub.get("corte", "")
    band = (f'<div class="cr">'
            f'<div class="cr-card"><div class="cr-c">PLAN PAC 2026</div><div class="cr-v">${plan/1e6:.2f}M</div>'
            f'<div class="cr-l">planificado oficial</div></div>'
            f'<div class="cr-a" style="color:#FFB020">→</div>'
            f'<div class="cr-card"><div class="cr-c">PUBLICADO SERCOP</div><div class="cr-v">${publ/1e3:.0f}k</div>'
            f'<div class="cr-l">{n} procesos · corte {corte}</div></div>'
            f'<div class="cr-a" style="color:#FFB020">→</div>'
            f'<div class="cr-card"><div class="cr-c">COBERTURA</div>'
            f'<div class="cr-v" style="color:#FFB020">{pct}%</div>'
            f'<div class="cr-l">del plan ya en SERCOP</div></div></div>')
    bar = (f'<div style="height:11px;background:rgba(255,255,255,.06);border-radius:6px;overflow:hidden;margin:0 0 16px">'
           f'<div style="height:100%;width:{max(pct, 0.6)}%;background:linear-gradient(90deg,#22D3EE,#FFB020)"></div></div>')
    return band + bar


def _stepper(sat_temp: str) -> str:
    links = [("Plan", "verde"), ("Operación", "verde"), ("Contratación", "normal"),
             ("Coherencia", sat_temp or "alerta")]
    out = ""
    for i, (lab, t) in enumerate(links):
        c = _T.get(t, "#7E8BA3")
        out += (f'<div class="sp-l"><span class="sp-d" style="background:{c};box-shadow:0 0 9px {c}99"></span>'
                f'<span class="sp-t">{lab}</span></div>')
        if i < len(links) - 1:
            out += '<span class="sp-ln"></span>'
    return f'<div class="sp">{out}</div>'


def _cobertura_band(pct, metas_total: int = 25) -> str:
    """Cobertura de metas del PDOT en el POA — primer eslabón (POA ≠ Presupuesto · Javo 2026-07-02)."""
    if pct is None:
        return ""
    n_con = round(pct / 100 * metas_total)
    return (
        f'<div class="pl-cov">'
        f'<div class="pl-cov-row"><span class="pl-cov-val">{pct:.0f}%</span>'
        f'<span class="pl-cov-lbl">de las metas del PDOT (<b>{n_con} de {metas_total}</b>) están '
        f'<b>operativizadas en el Plan Operativo Anual (POA)</b> de 2026</span></div>'
        f'<div class="pl-cov-note">Este es el <b>primer eslabón de la trazabilidad</b>: mide cuánto del plan '
        f'<b>plurianual</b> de desarrollo (PDOT 2023-2027) se traduce en <b>programación operativa concreta</b> '
        f'este año —con actividades, responsables y recursos asignados en el POA—. Un porcentaje alto indica que '
        f'la planificación de largo plazo <b>se traduce efectivamente</b> en la operación anual, y no permanece en el plano declarativo.'
        f'<b>Precisión conceptual:</b> el <b>POA</b> es el instrumento de <i>programación operativa</i> anual; '
        f'es distinto del <b>Presupuesto Municipal</b>, que es el instrumento <i>financiero</i> que asigna los '
        f'fondos —ambos se leen en detalle más abajo—. La meta que aún no figura en el POA del GAD central se '
        f'gestiona por otra unidad de la red municipal, en su propio instrumento.</div>'
        f'</div>')


def _css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
.pl-wrap, .pl-wrap *{font-family:'Inter',system-ui,sans-serif}
/* título limpio (no forense) */
.pl-title{font-size:30px;font-weight:900;color:#F0F4FA;letter-spacing:-.01em;line-height:1.1;margin:2px 0 6px}
.pl-sub{font-size:15.5px;line-height:1.6;color:#AEB9CC;max-width:88ch;margin-bottom:10px}
.pl-title-band{border-bottom:1px solid rgba(255,255,255,.09);padding-bottom:14px;margin-bottom:16px}
/* cobertura */
.pl-cov{background:linear-gradient(90deg,rgba(45,212,111,.10),rgba(45,212,111,.02));
  border:1px solid rgba(45,212,111,.28);border-left:4px solid #2DD46F;border-radius:12px;padding:14px 18px;margin:4px 0 20px}
.pl-cov-row{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.pl-cov-val{font-family:'JetBrains Mono',monospace;font-size:34px;font-weight:900;color:#2DD46F;line-height:1}
.pl-cov-lbl{font-size:15px;color:#DCE4F0;font-weight:500}
.pl-cov-note{font-size:13.5px;line-height:1.6;color:#9AA6BE;margin-top:9px}
.pl-cov-note b{color:#C7D2E0}
/* secciones */
.pl-h{display:flex;align-items:baseline;gap:11px;margin:20px 0 8px;flex-wrap:wrap}
.pl-n{font-family:'JetBrains Mono',monospace;font-size:16px;font-weight:800;color:#22D3EE}
.pl-t{font-size:19px;font-weight:800;color:#F0F4FA;letter-spacing:.01em}
.pl-s{font-size:13px;color:#7E8BA3}
.pl-intro{font-size:14.5px;line-height:1.72;color:#C2CDDE;margin:4px 0 14px;
  background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.07);
  border-left:3px solid #3BA7D9;border-radius:11px;padding:14px 18px}
.pl-intro b{color:#EAF0F8}
.pl-narr{font-size:14.5px;line-height:1.74;color:#D2DBEA;
  background:rgba(34,211,238,.045);border:1px solid rgba(34,211,238,.16);
  border-left:3px solid #22D3EE;border-radius:12px;padding:15px 18px}
.pl-narr b{color:#F0F4FA}
.pl-law{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:700;
  color:#22D3EE;background:rgba(34,211,238,.10);border:1px solid rgba(34,211,238,.26);
  border-radius:6px;padding:1px 8px;margin:0 2px;white-space:nowrap}
.pl-lawrow{margin-top:11px;padding-top:9px;border-top:1px dashed rgba(255,255,255,.12);
  font-size:12.5px;color:#9AA6BE;line-height:1.55}
.pl-lawrow b{color:#C7D2E0}
hr.pl-div{border:none;border-top:1px solid rgba(255,255,255,.08);margin:22px 0}
/* tablas — fuentes ↑ */
.mt-wrap{overflow:auto;border:1px solid rgba(255,255,255,.09);border-radius:12px;margin-bottom:6px}
.mt{width:100%;border-collapse:collapse;font-size:13px}
.mt thead th{position:sticky;top:0;background:#0E1623;color:#AEB9CC;font-weight:700;text-align:left;
  padding:10px 12px;letter-spacing:.03em;border-bottom:1px solid rgba(255,255,255,.10);font-size:11px;text-transform:uppercase}
.mt td{padding:9px 12px;border-bottom:1px solid rgba(255,255,255,.05);color:#D2DBEA;vertical-align:top}
.mt tbody tr:hover{background:rgba(34,211,238,.04)}
.mt-id{font-family:'JetBrains Mono',monospace;color:#7E8BA3;white-space:nowrap}
.mt-sis{color:#B8C4D6;white-space:nowrap}
.mt-meta{color:#F0F4FA;min-width:240px}
.mt-num{font-family:'JetBrains Mono',monospace;color:#F0F4FA;white-space:nowrap;text-align:right}
.mt-tag{font-size:10.5px;font-weight:700;border:1px solid;border-radius:6px;padding:2px 8px;white-space:nowrap}
.mt-dir{color:#9AA6BE;white-space:nowrap}
/* pills */
.pl-pill{display:flex;align-items:center;gap:10px;padding:10px 14px;margin:7px 0;
  background:rgba(255,255,255,.025);border:1px solid;border-radius:10px}
.pl-pd{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.pl-pl{font-size:14px;color:#D2DBEA;flex:1}
.pl-pe{font-size:12px;font-weight:700;text-align:right}
/* cruce backbone */
.cr{display:flex;align-items:stretch;gap:6px;margin:6px 0 16px;flex-wrap:nowrap}
.cr-card{flex:1;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.09);
  border-radius:12px;padding:13px 8px;text-align:center;min-width:0}
.cr-c{font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:800;color:#22D3EE;letter-spacing:.05em}
.cr-v{font-size:17px;font-weight:800;color:#F0F4FA;margin:6px 0 3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cr-l{font-size:11px;color:#7E8BA3}
.cr-a{display:flex;align-items:center;font-size:20px;font-weight:800;flex-shrink:0}
/* stepper */
.sp{display:flex;align-items:center;padding:8px 2px 4px}
.sp-l{display:flex;flex-direction:column;align-items:center;gap:7px}
.sp-d{width:15px;height:15px;border-radius:50%}
.sp-t{font-size:12px;color:#B8C4D6;font-weight:600;white-space:nowrap}
.sp-ln{flex:1;height:2px;background:rgba(255,255,255,.13);margin:0 5px 19px}
/* nota al pie de tabla */
.pl-note{font-size:12.5px;line-height:1.6;color:#8493A8;background:rgba(255,255,255,.02);
  border:1px dashed rgba(255,255,255,.12);border-radius:9px;padding:10px 14px;margin:2px 0 4px}
.pl-note b{color:#B8C4D6}
/* síntesis por eslabón */
.pl-syn-row{display:flex;gap:14px;align-items:baseline;padding:9px 0;border-bottom:1px solid rgba(255,255,255,.06)}
.pl-syn-c{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:800;color:#22D3EE;
  letter-spacing:.04em;min-width:190px;flex-shrink:0;text-transform:uppercase}
.pl-syn-t{font-size:14.5px;line-height:1.62;color:#D2DBEA}
.pl-syn-t b{color:#F0F4FA}
/* motores SAT */
.pl-sat-h{display:flex;align-items:center;gap:11px;margin:16px 0 10px;flex-wrap:wrap}
.pl-sat-n{font-family:'JetBrains Mono',monospace;font-size:10.5px;font-weight:800;color:#7E8BA3;
  letter-spacing:.08em;text-transform:uppercase}
.pl-sat-t{font-size:16.5px;font-weight:800;color:#F0F4FA}
.pl-sat-e{font-size:11px;font-weight:700;border:1px solid;border-radius:9px;padding:2px 10px}
.ev-chain{display:flex;align-items:center;padding:8px 2px 14px}
.ev-node{display:flex;flex-direction:column;align-items:center;gap:8px;min-width:0}
.ev-n{font-family:'JetBrains Mono',monospace;font-size:17px;font-weight:900;width:46px;height:46px;
  display:flex;align-items:center;justify-content:center;border:2px solid;border-radius:50%;
  background:rgba(255,255,255,.02)}
.ev-l{font-size:11.5px;color:#B8C4D6;font-weight:600;text-align:center;max-width:96px}
.ev-link{flex:1;height:3px;border-radius:2px;margin:0 6px 24px}
.pl-clean{display:flex;gap:14px;align-items:flex-start;background:rgba(45,212,111,.06);
  border:1px solid rgba(45,212,111,.22);border-left:3px solid #2DD46F;border-radius:12px;padding:15px 18px}
.pl-clean-ic{font-size:22px;color:#2DD46F;font-weight:900;flex-shrink:0;line-height:1.2}
.pl-clean-t{font-size:15px;font-weight:800;color:#F0F4FA;margin-bottom:5px}
.pl-clean-d{font-size:14px;line-height:1.65;color:#C2CDDE}
.pl-clean-d b{color:#EAF0F8}
/* cierre */
.pl-cierre{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.09);border-radius:14px;
  padding:18px 22px;margin-top:22px}
.pl-cierre-lbl{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:800;letter-spacing:.1em;
  color:#7E8BA3;text-transform:uppercase;margin-bottom:7px}
.pl-cierre-txt{font-size:15.5px;line-height:1.7;color:#D2DBEA}
.pl-cierre-txt b{color:#F0F4FA}
.pl-src{font-size:12.5px;color:#7E8BA3;margin-top:10px}
</style>"""


# ═══════════════════════ los eslabones (tabla + gráfica + texto) ══════════════
def _sec_pdot(plan: dict) -> None:
    metas = plan.get("metas_detalle", [])
    comp = plan.get("competencia", [])
    criticas = sum(c["n"] for c in comp if "Crítica" in c["label"])
    st.markdown(_head("1", "PDOT — EL PLAN", f"lo que el municipio se comprometió a lograr · {len(metas)} metas 2023-2027"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        "El <b>Plan de Desarrollo y Ordenamiento Territorial (PDOT)</b> es el <b>instrumento rector</b> de la "
        "planificación cantonal: define, con carácter <b>obligatorio y vinculante</b>, el modelo de desarrollo "
        "del territorio para el período <b>2023-2027</b> y articula al municipio con el Sistema Nacional "
        "Descentralizado de Planificación Participativa. Lo aprueba el Concejo Municipal, y el POA y el "
        "presupuesto anual se <b>formulan en concordancia con él</b> —nunca a la inversa—. No es un instrumento "
        "declarativo: es el <b>compromiso formal</b> contra el que se mide toda la gestión. Cada fila de la tabla "
        "es una meta, con "
        "cuatro datos que conviene leer juntos:<br>• su <b>sistema</b> (el área a la que pertenece),<br>• la "
        "<b>meta plurianual</b>, con su valor de partida y su valor de llegada al 2027,<br>• el <b>tipo de "
        "competencia</b> —qué obliga la ley al municipio en exclusiva y qué comparte con otros niveles de "
        "gobierno—,<br>• y la <b>dirección municipal</b> responsable de cumplirla."
        + _ley_row(plan, "pdot", "La planificación del desarrollo es obligatoria en todos los niveles de gobierno "
                   "y se articula al Plan Nacional de Desarrollo.")), unsafe_allow_html=True)
    st.markdown(_tabla_metas(metas), unsafe_allow_html=True)
    cm = {c["label"]: c["n"] for c in comp}
    ec, cc = cm.get("Exclusiva Crítica", 0), cm.get("Concurrente Crítica", 0)
    ei, co = cm.get("Exclusiva Importante", 0), cm.get("Concurrente", 0)
    c1, c2 = st.columns([1.05, 1.2], gap="large")
    with c1:
        _show(_competencia_bar(comp, metas, plan.get("poa_detalle", [])), 260)
    with c2:
        st.markdown(_narr(
            f"La gráfica clasifica las <b>{len(metas)} metas</b> según el <b>tipo de competencia</b> que la ley "
            f"asigna al municipio —el criterio que define qué está <i>obligado</i> a hacer y con qué prioridad—. "
            f"Cada barra muestra su número de metas y el presupuesto operativo que concentran:"
            f"<br>• <b>Exclusiva Crítica — {ec}:</b> competencias propias e indelegables en servicios esenciales "
            f"(agua potable, alcantarillado, desechos, vialidad). Máxima prioridad legal y presupuestaria."
            f"<br>• <b>Concurrente Crítica — {cc}:</b> servicios esenciales que el GAD ejerce <i>compartiendo</i> "
            f"la competencia con otro nivel de gobierno."
            f"<br>• <b>Exclusiva Importante — {ei}:</b> competencias propias del municipio en materias no "
            f"clasificadas como críticas —son la mayoría de las metas—."
            f"<br>• <b>Concurrente — {co}:</b> competencias de gestión compartida, de alcance general."
            f"<br>En conjunto, <b>{criticas} metas son de competencia crítica</b> ({ec} + {cc}): son las que la "
            f"ley obliga a <b>priorizar y financiar primero</b>. Leer este reparto revela si el plan está "
            f"realmente enfocado donde la norma lo exige, o disperso en lo secundario."),
            unsafe_allow_html=True)


def _sec_poa(plan: dict) -> None:
    proys = plan.get("poa_proyectos", [])
    poa = plan.get("poa_detalle", [])
    tpoa = sum(x["anual"] for x in proys)
    st.markdown(_head("2", "POA — LA OPERACIÓN",
                      f"cómo se ejecuta el plan en el año · {len(proys)} proyectos · Plan Operativo 2026"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        f"Si el PDOT dice <b>qué</b> lograr, el <b>Plan Operativo Anual (POA)</b> dice <b>cómo</b> y <b>con "
        f"cuánto</b> hacerlo este año. En términos legales es la <b>desagregación anualizada del plan estratégico "
        f"plurianual</b>: convierte cada meta del PDOT en <b>metas físicas anuales</b>, con sus <b>indicadores de "
        f"gestión</b>, <b>responsables internos</b>, <b>cronograma de desembolsos</b> y la <b>asignación exacta "
        f"de partidas</b> del gasto (permanente y no permanente). En la práctica, concreta el plan en"
        f"<b>{len(proys)} proyectos y actividades</b> concretos —una ampliación de alcantarillado, la compra de "
        f"un hidrosuccionador, la construcción de un pozo—, cada uno con su <b>dirección</b> responsable, su "
        f"<b>partida presupuestaria</b> (el código contable del gasto) y su <b>monto</b> 2026. En conjunto "
        f"movilizan <b>${tpoa:,.0f}</b>: es el <b>vínculo</b> entre los objetivos del plan y la asignación de "
        f"recursos que los hace ejecutables."
        + _ley_row(plan, "poa", "El POA es la desagregación operativa anual del plan plurianual, articulada al "
                   "presupuesto.")), unsafe_allow_html=True)
    st.markdown(_tabla_proyectos(proys), unsafe_allow_html=True)
    if poa:
        c1, c2 = st.columns([1.3, 1], gap="large")
        with c1:
            _show(_cronograma(poa), 220)
        with c2:
            st.markdown(_narr(
                "La curva muestra el <b>ritmo planificado mes a mes</b>: cuánto de la operación está previsto "
                "ejecutar en cada mes, según lo que el propio municipio programó en el POA. <b>Precisión: es el plan,"
                "no lo ya ejecutado.</b> La línea punteada marca el <b>corte actual</b> —la ejecución real "
                "ingerida llega hasta abril—; a la derecha de esa línea (zona sombreada) es programación a "
                "futuro. Leerla permite anticipar los <b>meses de mayor exigencia</b> y ver si la carga se "
                "concentra o se reparte a lo largo del año."),
                unsafe_allow_html=True)


def _sec_pac(plan: dict) -> None:
    _pac_total = plan.get("pac", {}).get("total_usd", 0)
    pac_det = plan.get("pac_detalle", []) or []
    pub = plan.get("publicado", {}) or {}
    st.markdown(_head("3", "PAC — LA CONTRATACIÓN", f"qué contrata el municipio · total oficial ${_pac_total:,.0f}"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        f"El <b>Plan Anual de Contratación (PAC)</b> es la lista oficial de todo lo que el municipio va a comprar "
        f"o contratar en el año —obras, bienes y servicios— con su costo estimado y el <b>procedimiento</b> "
        f"previsto (subasta inversa, licitación, menor cuantía, etc.). Asciende a <b>${_pac_total:,.0f}</b> y "
        f"cubre el <b>98.6% del presupuesto de inversión</b>: casi todo lo que se planea invertir ya tiene "
        f"asignado un proceso de contratación —señal de coherencia entre plan y gasto—. Importante: el PAC "
        f"<b>no es un documento estático</b>; puede <b>reformarse</b> durante el año por necesidades "
        f"institucionales justificadas, mediante resolución de la máxima autoridad o su delegado, publicándose "
        f"de inmediato en el portal oficial."
        + _ley_row(plan, "pac", "El PAC es obligatorio, debe concordar con el plan y el presupuesto, y sus "
                   "reformas se publican de inmediato en el portal de compras públicas.")), unsafe_allow_html=True)
    # El PAC completo (Javo 2026-07-02: mostrar todo el PAC, no solo lo publicado)
    if pac_det:
        st.markdown(_intro(
            f"<b>El PAC completo — {len(pac_det)} procesos planificados.</b> Cada proceso, su procedimiento, su "
            f"monto referencial y su vínculo a una meta del plan (cuando el dato ya lo permite); la columna "
            f"<b>Coherencia</b> marca la señal preventiva del cruce plan↔contratación:"), unsafe_allow_html=True)
        st.markdown(_tabla_pac(pac_det), unsafe_allow_html=True)
        st.markdown(
            '<div class="pl-note"><b>Nota:</b> varios procesos figuran con monto <b>"por valorar"</b> — su '
            'cuantía se define al concretarse el estudio de mercado y publicarse en el portal de compras públicas. '
            'El <b>vínculo fino proceso↔meta</b> y el cruce con lo efectivamente publicado se completan y actualizan '
            'en vivo conforme avanza el ejercicio; a esta altura del año varias celdas están en formación.</div>',
            unsafe_allow_html=True)
    # Lo YA publicado en el SERCOP — estado vivo verificado
    if pub.get("procesos"):
        st.markdown(_intro(
            "Hasta aquí, <b>el plan</b>. Ahora el <b>estado vivo</b>: qué de ese plan el municipio "
            "<b>ya publicó realmente en el SERCOP</b> (Servicio Nacional de Contratación Pública), traído y "
            "verificado en tiempo real desde los datos abiertos del Estado."), unsafe_allow_html=True)
        st.markdown(_publicado_band(pub), unsafe_allow_html=True)
        st.markdown(_intro(
            f"<b>Publicado en el SERCOP al corte {pub.get('corte', '')}:</b> {pub.get('n_procesos', 0)} procesos "
            f"por <b>${pub.get('total_usd', 0):,.0f}</b> (valor referencial). El detalle, proceso por proceso y "
            f"directo de la fuente oficial:"), unsafe_allow_html=True)
        st.markdown(_tabla_publicado(pub.get("procesos", [])), unsafe_allow_html=True)
        cr = pub.get("cruce", {}) or {}
        c1, c2 = st.columns([1.1, 1], gap="large")
        with c1:
            _show(_pub_bar(pub), 230)
        with c2:
            st.markdown(_narr(
                f"El plan de contratación suma <b>${cr.get('plan_pac_usd', 0)/1e6:.1f}M</b>; en el SERCOP el "
                f"municipio ya publicó <b>{pub.get('n_procesos', 0)} procesos por "
                f"${pub.get('total_usd', 0)/1e3:.0f}k</b> —el <b>{cr.get('cobertura_pct', 0)}%</b> del plan, al "
                f"corte {pub.get('corte', '')}—. <b>No es una alarma</b>: a esta altura del año la mayor parte del "
                f"PAC todavía está en preparación, porque la ejecución del gasto público se concentra en el "
                f"segundo semestre. Lo que conviene seguir es el <b>ritmo de publicación</b> mes a mes: es la "
                f"señal temprana de si la contratación llegará a tiempo a cubrir lo presupuestado."),
                unsafe_allow_html=True)


def _sec_presupuesto(plan: dict) -> None:
    pres = plan.get("presupuesto", {}) or {}
    cod = pres.get("codificado_inversion", 0) or 0
    dev = pres.get("devengado", 0) or 0
    pac_total = (plan.get("pac", {}) or {}).get("total_usd", 0) or 0
    cobertura = 100 * pac_total / cod if cod else 0
    st.markdown(_head("4", "PRESUPUESTO — EL RECURSO", f"con qué inversión se cuenta · corte {pres.get('corte', '')}"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        "El <b>Presupuesto Municipal</b> es el instrumento <b>financiero</b> anual que asigna los recursos a cada "
        "programa y partida. Por mandato constitucional y legal <b>se formula en concordancia con el plan</b> —se "
        "subordina al PDOT y al POA, no a la inversa— y su priorización se define con <b>participación ciudadana</b>. "
        "Aquí se muestra específicamente la <b>inversión</b> (bienes y obras), separando dos cifras que suelen "
        "confundirse:<br>• lo <b>codificado</b> —lo asignado y disponible para gastar—,<br>• y lo <b>devengado</b> "
        "—lo que ya se ejecutó al corte—.<br>No es el presupuesto municipal <i>total</i> (que incluye sueldos y "
        "gasto corriente), sino la parte de <b>inversión</b>, que es con la que se relacionan las metas del plan "
        "y la contratación."
        + _ley_row(plan, "presupuesto", "El presupuesto de los GAD se ajusta obligatoriamente al plan; su ciclo "
                   "—formulación, aprobación, ejecución y clausura— está reglado en el COOTAD y el COPLAFIP.")),
        unsafe_allow_html=True)
    st.markdown(_tabla_presupuesto(pres), unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 1], gap="large")
    with c1:
        _show(_brechas(cod, dev, pac_total), 250)
    with c2:
        st.markdown(_narr(
            f"Aquí se lee la tensión clave del año. De los <b>${cod/1e6:.1f}M</b> de inversión presupuestada, el "
            f"plan de contratación recoge <b>${pac_total/1e6:.1f}M</b> —el <b>{cobertura:.1f}%</b>—: plan y "
            f"presupuesto están alineados. Pero lo <b>devengado</b> —lo realmente ejecutado— es apenas "
            f"<b>${dev/1e6:.2f}M</b> ({pres.get('ti_pct', 0)}%), algo <b>natural en el primer cuatrimestre</b> "
            f"porque el gasto público es de <b>carga tardía</b> (las obras de mayor cuantía inician en el segundo semestre). El "
            f"punto preventivo no es el nivel bajo de hoy, sino <b>vigilar que la ejecución acelere</b> para "
            f"alcanzar al presupuesto antes del cierre del ejercicio."),
            unsafe_allow_html=True)


def _sec_ipe(plan: dict) -> None:
    """El gasto ejecutado vinculado a una meta del plan (IPE-ejecutado · lenguaje gobernanza)."""
    ie = plan.get("ipe_ejecutado") or {}
    if not ie or not ie.get("total"):
        return
    por = plan.get("ipe_por_objetivo") or []
    pct = ie.get("pct", 0)
    total = ie.get("total", 0) or 1
    vinc = ie.get("vinculado", 0)
    nop = ie.get("no_pdot", 0)
    st.markdown(_head("5", "EL GASTO VINCULADO AL PLAN",
                      "cuánto del gasto de inversión ejecutado responde a una meta del PDOT"),
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="pl-cov" style="border-color:rgba(34,211,238,.28);border-left-color:#22D3EE;'
        f'background:linear-gradient(90deg,rgba(34,211,238,.10),rgba(34,211,238,.02))">'
        f'<div class="pl-cov-row"><span class="pl-cov-val" style="color:#22D3EE">{pct:.1f}%</span>'
        f'<span class="pl-cov-lbl">de la inversión ejecutada al corte (<b>${total/1e6:.2f}M</b>) está vinculada '
        f'a una meta del PDOT vía su partida presupuestaria</span></div>'
        f'<div class="pl-cov-note">Solo <b>${nop/1e3:.0f}k</b> ({100*nop/total:.1f}%) es gasto de inversión sin '
        f'vínculo al plan (obras puntuales, seguros). El vínculo se traza cruzando cada partida ejecutada con el '
        f'proyecto operativo que la imputa a un objetivo del plan —lo que antes no se leía de un vistazo.</div>'
        f'</div>', unsafe_allow_html=True)
    if por:
        c1, c2 = st.columns([1.25, 1], gap="large")
        with c1:
            _show(_ipe_bar(por), 270)
        with c2:
            top = por[0]
            st.markdown(_narr(
                f"Este es un indicador de <b>calidad del gasto</b>: no basta con ejecutar dinero, importa que ese "
                f"dinero responda a una meta del plan y no a decisiones improvisadas. El desglose reparte los "
                f"<b>${vinc/1e6:.2f}M</b> vinculados por objetivo del plan: el de mayor ejecución es "
                f"<b>{top['objetivo'].lower()}</b> (${top['dev']/1e3:.0f}k), seguido de las coberturas de "
                f"servicios y la movilidad. Así se ve, en <b>dinero ya ejecutado</b>, qué prioridades del plan "
                f"están en ejecución efectiva al corte —y cuáles aún no inician."),
                unsafe_allow_html=True)


# ═══════════════════════ Motores SAT — instrumentos preventivos (honestos) ══════
def _sat_h(num: str, titulo: str, comp: dict) -> str:
    estado = comp.get("estado", "—") or "—"
    c = _T.get(comp.get("temp", "dim"), "#7E8BA3")
    return (f'<div class="pl-sat-h"><span class="pl-sat-n">Motor {num}</span>'
            f'<span class="pl-sat-t">{titulo}</span>'
            f'<span class="pl-sat-e" style="color:{c};border-color:{c}55;background:{c}14">● {estado}</span></div>')


def _brecha_bipartito(plan: dict) -> go.Figure:
    """Grafo bipartito POA(partidas) ↔ SERCOP(procesos). Honesto: verde=con proceso · gris=en programación."""
    from collections import defaultdict
    poa: dict = defaultdict(float)
    for x in plan.get("poa_proyectos", []):
        k = str(x.get("partida", "")).strip()
        if k:
            poa[k] += x.get("anual", 0) or 0
    serc = {str(x.get("partida", "")).strip() for x in plan.get("publicado", {}).get("procesos", [])
            if str(x.get("partida", "")).strip()}
    top = sorted(poa.items(), key=lambda kv: -kv[1])[:7]
    n = len(top) or 1
    ys = list(range(n, 0, -1))
    fig = go.Figure()
    for (k, v), y in zip(top, ys):
        if k in serc:
            fig.add_trace(go.Scatter(x=[0.2, 0.8], y=[y, y], mode="lines",
                          line=dict(color="#2DD46F", width=2.5), hoverinfo="skip"))
    for (k, v), y in zip(top, ys):
        col = "#2DD46F" if k in serc else "#5A6B7E"
        fig.add_trace(go.Scatter(x=[0.2], y=[y], mode="markers+text",
                      marker=dict(size=15, color=col, line=dict(color="#0A0F19", width=1.5)),
                      text=[f"{k} · ${v/1e6:.1f}M  "], textposition="middle left",
                      textfont=dict(color="#B8C4D6", size=10.5), hoverinfo="skip"))
        if k in serc:
            fig.add_trace(go.Scatter(x=[0.8], y=[y], mode="markers",
                          marker=dict(size=13, color="#FFB020", line=dict(color="#0A0F19", width=1.5)),
                          hoverinfo="skip"))
    fig.add_annotation(x=0.2, y=n + 0.7, text="<b>POA</b> · líneas del plan", showarrow=False,
                       font=dict(color="#22D3EE", size=11), xanchor="left")
    fig.add_annotation(x=0.8, y=n + 0.7, text="<b>publicado</b>", showarrow=False,
                       font=dict(color="#FFB020", size=11), xanchor="left")
    fig.update_xaxes(visible=False, range=[-0.05, 1.2])
    fig.update_yaxes(visible=False, range=[0, n + 1.4])
    return fig


def _monto_scatter(plan: dict) -> go.Figure:
    """Dispersión de montos — los de menor cuantía concentran la señal preventiva."""
    pts = []
    for x in plan.get("publicado", {}).get("procesos", []):
        m = x.get("monto") or 0
        if m:
            pts.append(float(m))
    for x in plan.get("pac_detalle", []):
        m = x.get("monto") or 0
        if m:
            pts.append(float(m))
    pts.sort()
    xs = list(range(1, len(pts) + 1))
    fig = go.Figure(go.Scatter(
        x=xs, y=pts, mode="markers",
        marker=dict(size=14, color=pts or [0], colorscale=[[0, "#FFB020"], [1, "#22D3EE"]],
                    line=dict(color="#0A0F19", width=1)), hoverinfo="skip"))
    fig.update_xaxes(title_text="procesos (ordenados por monto)", tickfont=dict(color="#B8C4D6", size=10),
                     title_font=dict(color="#7E8BA3", size=11), showgrid=False)
    fig.update_yaxes(title_text="monto (USD)", tickfont=dict(color="#B8C4D6", size=10),
                     title_font=dict(color="#7E8BA3", size=11), gridcolor="rgba(255,255,255,.06)")
    return fig


def _evidencia_chain(plan: dict) -> str:
    pub = plan.get("publicado", {}) or {}
    et = {e["etapa"]: e["n"] for e in pub.get("por_etapa", [])}
    fases = [("Planificado", et.get("Planificado", 0)),
             ("Publicado / en proceso", et.get("En proceso", 0)),
             ("Adjudicado", et.get("Adjudicado", 0)),
             ("Contrato", et.get("Contrato", 0) + et.get("Contratado", 0))]
    out = ""
    for i, (lab, c) in enumerate(fases):
        col = "#2DD46F" if c else "#46566A"
        out += (f'<div class="ev-node"><span class="ev-n" style="color:{col};border-color:{col}66">{c}</span>'
                f'<span class="ev-l">{lab}</span></div>')
        if i < 3:
            out += f'<span class="ev-link" style="background:{"#2DD46F" if c else "#2A3444"}"></span>'
    return f'<div class="ev-chain">{out}</div>'


def _downcoding_card(plan: dict) -> str:
    return (
        '<div class="pl-clean"><span class="pl-clean-ic">✓</span>'
        '<div><div class="pl-clean-t">Sin señal de fraccionamiento</div>'
        '<div class="pl-clean-d">No se detecta el patrón de <b>dividir un mismo objeto de gasto</b> en múltiples '
        'procesos pequeños para evadir los umbrales de control (el fraccionamiento clásico). Este motor se '
        '<b>enciende</b> si aparece una concentración anómala de procesos de ínfima cuantía sobre un mismo objeto '
        'o proveedor; al corte, la contratación está limpia en este frente.</div></div></div>')


def _sec_coherencia(plan: dict) -> None:
    sat = plan.get("sat0", {}) or {}
    sat_temp = sat.get("global_temp", "alerta")
    comps = {c.get("label"): c for c in sat.get("componentes", [])}
    st.markdown(_head("6", "LA COHERENCIA", "cuatro motores de análisis preventivo sobre la contratación"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        "Aquí vive el <b>análisis de mayor valor</b> del sistema. Ya no mira si el plan existe —eso se vio arriba— "
        "sino si la <b>ejecución es coherente</b> con él, cruzando la contratación <b>proceso por proceso</b> a "
        "través de cuatro <b>motores preventivos</b>. Cada uno vigila una forma distinta de erosión del gasto "
        "público y habla en <b>lenguaje preventivo</b>: no acusa ni sanciona —señala dónde cerrar la coherencia "
        "<b>antes</b> de ejecutar—. Varios están <b>en formación</b>: se encienden con toda su fuerza conforme la "
        "contratación del año llena sus datos."), unsafe_allow_html=True)
    st.markdown(_stepper(sat_temp), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    st.markdown(_sat_h("1", "Brecha plan ↔ contratación", comps.get("Brecha POA-PAC", {})), unsafe_allow_html=True)
    c1, c2 = st.columns([1.15, 1], gap="large")
    with c1:
        _show(_brecha_bipartito(plan), 300)
    with c2:
        st.markdown(_narr(
            "El motor conecta cada <b>línea del plan operativo</b> (izquierda) con el <b>proceso de contratación</b> "
            "que la ejecuta (derecha). Una línea del plan <b>sin conexión</b> es presupuesto que aún no llegó a "
            "contratarse. <b>Al corte de abril</b>, la mayoría está <b>en programación</b> —aún sin publicar en el "
            "SERCOP, natural en el primer cuatrimestre—; en <b>verde</b>, las que ya tienen proceso. El poder del "
            "grafo se revela hacia mitad de año: si una línea de <b>mucho presupuesto</b> sigue huérfana cuando el "
            "año avanza, el hueco se vuelve visible al instante."), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    st.markdown(_sat_h("2", "Dispersión de montos", comps.get("Monto mínimo", {})), unsafe_allow_html=True)
    c1, c2 = st.columns([1.15, 1], gap="large")
    with c1:
        _show(_monto_scatter(plan), 300)
    with c2:
        st.markdown(_narr(
            "Cada punto es un proceso, ubicado por su <b>monto</b>. Los de <b>menor cuantía</b> (abajo, en ámbar) "
            "son los más difíciles de fiscalizar y los más propensos al fraccionamiento —por eso concentran la "
            "señal preventiva—. El motor vigila la <b>frecuencia</b>: un proceso pequeño es rutina; muchos "
            "seguidos bajo el umbral son un <b>patrón</b> a revisar. Con la contratación de Q1 aún rala, muestra "
            "los pocos procesos ya valorados; se densifica con el año."), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    st.markdown(_sat_h("3", "Reloj de evidencia", comps.get("Reloj de evidencia", {})), unsafe_allow_html=True)
    st.markdown(_evidencia_chain(plan), unsafe_allow_html=True)
    st.markdown(_narr(
        "Cada contratación deja una <b>cadena de evidencia</b> en sus etapas legales: planificación → publicación "
        "→ adjudicación → contrato. Una cadena <b>completa y en plazo</b> es señal de proceso sano; una etapa que "
        "<b>no llega a tiempo</b> rompe la cadena y enciende la alerta. Al corte, los procesos publicados están en "
        "sus <b>primeras etapas</b> —lo esperado a esta altura—; el reloj vigila que ninguno se estanque."),
        unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    st.markdown(_sat_h("4", "Fraccionamiento contractual", comps.get("Downcoding contractual", {})),
                unsafe_allow_html=True)
    st.markdown(_downcoding_card(plan), unsafe_allow_html=True)


def _cierre(plan: dict) -> None:
    metas = plan.get("metas_detalle", [])
    comp = plan.get("competencia", [])
    criticas = sum(c["n"] for c in comp if "Crítica" in c["label"])
    cob = plan.get("cobertura_metas_poa") or 0
    proys = plan.get("poa_proyectos", [])
    tpoa = sum(x.get("anual", 0) for x in proys)
    pac_total = (plan.get("pac", {}) or {}).get("total_usd", 0) or 0
    pub = plan.get("publicado", {}) or {}
    pub_pct = (pub.get("cruce", {}) or {}).get("cobertura_pct", 0)
    pres = plan.get("presupuesto", {}) or {}
    cod = pres.get("codificado_inversion", 0) or 0
    dev = pres.get("devengado", 0) or 0
    ti = pres.get("ti_pct", 0)
    ipe = (plan.get("ipe_ejecutado") or {}).get("pct", 0)
    corte = pres.get("corte", "enero–abril 2026")

    def _r(code, txt):
        return f'<div class="pl-syn-row"><span class="pl-syn-c">{code}</span><span class="pl-syn-t">{txt}</span></div>'

    filas = (
        _r("Plan · PDOT",
           f"<b>{len(metas)} metas</b> plurianuales de desarrollo, <b>{criticas} de competencia crítica</b> "
           f"(donde la ley obliga a actuar). El <b>{cob:.0f}%</b> ya se incorporó a la operación anual: la "
           f"planificación de largo plazo se tradujo en gestión concreta.")
        + _r("Operación · POA",
             f"<b>{len(proys)} proyectos</b> movilizan <b>${tpoa/1e6:.1f}M</b> en 2026, cada uno con dirección, "
             f"partida y cronograma —el plan traducido en actividades concretas y responsables.")
        + _r("Contratación · PAC",
             f"<b>${pac_total/1e6:.1f}M</b> planificados (el <b>98.6%</b> del presupuesto de inversión). "
             f"<b>{pub_pct}%</b> ya publicado en el SERCOP —bajo, pero <b>natural en el primer cuatrimestre</b>; "
             f"la ejecución del gasto se concentra en el segundo semestre.")
        + _r("Recurso · Presupuesto",
             f"<b>${cod/1e6:.1f}M</b> de inversión codificada; <b>${dev/1e6:.2f}M</b> devengados "
             f"(<b>{ti}%</b>) —ejecución inicial, de carga tardía típica del gasto de inversión.")
        + _r("Calidad · Gasto vinculado",
             f"<b>{ipe:.1f}%</b> del gasto de inversión ya ejecutado corresponde a una meta del plan: se asigna "
             f"<b>según lo planificado</b>, no por decisiones discrecionales.")
        + _r("Prevención · Coherencia",
             "señal preventiva activa en la alineación plan↔contratación —el foco es <b>cerrar el vínculo antes</b> "
             "de ejecutar, no sancionar después.")
    )
    st.markdown(
        f'<div class="pl-cierre">'
        f'<div class="pl-cierre-lbl">Síntesis ejecutiva — la cadena de extremo a extremo</div>'
        f'{filas}'
        f'<div class="pl-cierre-txt" style="margin-top:15px">En conjunto, <b>el plan sostiene su diseño</b>: la '
        f'correspondencia entre lo planificado, lo presupuestado y lo contratado es sólida, y el gasto ya ejecutado '
        f'es de <b>alta calidad</b> (vinculado a metas). La <b>atención es preventiva, no correctiva</b>: pasa por '
        f'que la <b>contratación y la ejecución aceleren</b> en el segundo semestre para alcanzar al presupuesto '
        f'antes del cierre del ejercicio, de modo que los compromisos del PDOT no se erosionen en el tránsito de la '
        f'planificación a la ejecución. Ese seguimiento mes a mes es, precisamente, el valor de observar la planificación de extremo a extremo, de la meta al gasto.</div>'
        f'<div class="pl-src">Fuente: PDOT · POA · PAC (SERCOP) · presupuesto eSIGEF · corte {corte}.</div>'
        f'</div>',
        unsafe_allow_html=True)


def render() -> None:
    """QINV-001 · Planificación Estratégica — cajón de DOMINIO (patrón RDC · Javo 2026-07-10):
    principio → procedimiento (backbone) → cobertura → trazabilidad → coherencia → evaluación → síntesis.
    HTML autocontenido (Regla 1: la app NO recalcula; lee el snapshot del Gold Master)."""
    plan = (_cargar() or {}).get("plan") or {}
    if not plan:
        st.markdown('<div style="font-size:15px;color:#7E8BA3;padding:20px 0">'
                    '— evidencia del plan pendiente de carga —</div>', unsafe_allow_html=True)
        return
    try:
        from app.viz.render.plan_render import cajon_plan_streamlit
    except Exception as e:  # noqa: BLE001
        st.error(f"Cajón de Planificación no disponible: {e}")
        return
    st.markdown(cajon_plan_streamlit(plan), unsafe_allow_html=True)
    # La síntesis ejecutiva (6 eslabones) ahora vive DENTRO del cajón (_sintesis_plan) — ya no
    # se renderiza aparte: el antiguo _cierre() quedaba fuera del cajón y sin CSS (flotaba).
