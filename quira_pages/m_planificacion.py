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


def _ley_row(plan: dict, stage: str, gloss: str) -> str:
    """Fila de fundamento legal — artículo VERIFICADO del corpus (sha256 · Regla 3). '' si no hay."""
    art = ((plan.get("base_normativa") or {}).get("por_eslabon") or {}).get(stage)
    if not art:
        return ""
    nom = _LEY_NOMBRE.get(art["norma"], art["norma"])
    return (f'<div class="pl-lawrow">⚖ <b>Fundamento legal:</b> '
            f'<span class="pl-law">{nom} · Art. {art["articulo"]}</span> {gloss}</div>')


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
    stages = [("PDOT", f'{plan.get("metas_total", 25)} metas', "el plan"),
              ("POA", f'{plan.get("metas_total", 25)} programadas', "la operación"),
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


def _cobertura_band(pct) -> str:
    """Cobertura de metas con dotación POA — encuadre correcto (no es brecha · Javo 2026-07-01)."""
    if pct is None:
        return ""
    return (
        f'<div class="pl-cov">'
        f'<div class="pl-cov-row"><span class="pl-cov-val">{pct:.0f}%</span>'
        f'<span class="pl-cov-lbl">de las metas del PDOT cuentan con presupuesto operativo (POA) del municipio '
        f'<b>— 24 de 25</b></span></div>'
        f'<div class="pl-cov-note">La meta restante corresponde a los grupos de atención prioritaria, que ejecuta '
        f'el <b>Patronato</b> —entidad adscrita— en su propio ámbito de acción (COOTAD · Art. 249). No es una brecha '
        f'del plan: es competencia de otra unidad de la red municipal.</div>'
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
/* cierre */
.pl-cierre{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.09);border-radius:14px;
  padding:16px 20px;margin-top:22px}
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
        "El <b>Plan de Desarrollo y Ordenamiento Territorial (PDOT)</b> es la hoja de ruta que cada municipio del "
        "Ecuador está <b>obligado por ley</b> a definir. Fija, para el período <b>2023-2027</b>, las metas de "
        "desarrollo del territorio —qué se quiere lograr en agua, vialidad, salud, ambiente, desechos— y quién "
        "responde por cada una. No es un documento decorativo: es el <b>compromiso formal</b> contra el que se "
        "mide toda la gestión municipal. Cada fila de la tabla es una meta, con cuatro datos que conviene leer "
        "juntos:<br>• su <b>sistema</b> (el área a la que pertenece),<br>• la <b>meta plurianual</b>, con su "
        "valor de partida y su valor de llegada al 2027,<br>• el <b>tipo de competencia</b> —qué obliga la ley "
        "al municipio en exclusiva y qué comparte con otros niveles de gobierno—,<br>• y la <b>dirección "
        "municipal</b> responsable de cumplirla."
        + _ley_row(plan, "pdot", "— la planificación del desarrollo es obligatoria para todos los gobiernos "
                   "autónomos descentralizados.")), unsafe_allow_html=True)
    st.markdown(_tabla_metas(metas), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.15], gap="large")
    with c1:
        _show(_donut(comp), 250)
    with c2:
        st.markdown(_narr(
            f"De las <b>{len(metas)} metas</b>, <b>{criticas} son de competencia crítica</b>: las materias donde "
            f"la ley no da opción y el municipio <b>debe</b> actuar en primera persona —agua potable, vialidad, "
            f"alcantarillado, manejo de desechos—. La gráfica reparte las metas por tipo de competencia: en "
            f"<b>azul intenso</b>, lo que el GAD ejecuta en exclusiva; en <b>tonos grises</b>, lo que comparte o "
            f"coordina con el gobierno central y las juntas parroquiales. Ver este peso importa porque la ley "
            f"exige <b>priorizar y financiar primero</b> las competencias exclusivas críticas: son la vara con "
            f"la que se juzga si el plan está bien enfocado."),
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
        f"cuánto</b> hacerlo este año. Aterriza las metas en <b>{len(proys)} proyectos y actividades</b> "
        f"concretos —una ampliación de alcantarillado, la compra de un vehículo hidrosuccionador, la "
        f"construcción de un pozo— y a cada uno le asigna tres cosas: la <b>dirección</b> responsable, la "
        f"<b>partida presupuestaria</b> (el código contable que identifica el tipo de gasto) y el <b>monto</b> "
        f"previsto para 2026. En conjunto movilizan <b>${tpoa:,.0f}</b>. Es el <b>puente</b> entre la promesa "
        f"del plan y el dinero que la vuelve realidad."
        + _ley_row(plan, "poa", "— cada dirección municipal prepara su Plan Operativo Anual antes del cierre "
                   "del ejercicio, articulado al presupuesto.")), unsafe_allow_html=True)
    st.markdown(_tabla_proyectos(proys), unsafe_allow_html=True)
    if poa:
        c1, c2 = st.columns([1.3, 1], gap="large")
        with c1:
            _show(_cronograma(poa), 220)
        with c2:
            st.markdown(_narr(
                "La curva muestra el <b>ritmo planificado mes a mes</b>: cuánto de la operación está previsto "
                "ejecutar en cada mes, según lo que el propio municipio programó en el POA. <b>Ojo: es el plan, "
                "no lo ya ejecutado.</b> La línea punteada marca el <b>corte actual</b> —la ejecución real "
                "ingerida llega hasta abril—; a la derecha de esa línea (zona sombreada) es programación a "
                "futuro. Leerla permite anticipar los <b>meses de mayor exigencia</b> y ver si la carga se "
                "concentra o se reparte a lo largo del año."),
                unsafe_allow_html=True)


def _sec_pac(plan: dict) -> None:
    _pac_total = plan.get("pac", {}).get("total_usd", 0)
    pub = plan.get("publicado", {}) or {}
    st.markdown(_head("3", "PAC — LA CONTRATACIÓN", f"qué contrata el municipio · total oficial ${_pac_total:,.0f}"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        f"El <b>Plan Anual de Contratación (PAC)</b> es la lista oficial de todo lo que el municipio va a comprar "
        f"o contratar en el año —obras, bienes y servicios— con su costo estimado. Asciende a "
        f"<b>${_pac_total:,.0f}</b> y cubre el <b>98.6% del presupuesto de inversión</b>: es decir, casi todo lo "
        f"que se planea invertir ya tiene previsto un proceso de contratación. Eso es buena señal de coherencia "
        f"entre el plan y el gasto. El siguiente paso —el que QUIRA verifica <b>en vivo</b>— es contrastar ese "
        f"plan con lo que el municipio <b>ya publicó realmente en el SERCOP</b> (el Servicio Nacional de "
        f"Contratación Pública), traído en tiempo real desde los datos abiertos del Estado."
        + _ley_row(plan, "pac", "— toda entidad pública debe elaborar y publicar su Plan Anual de Contratación, "
                   "en concordancia con su plan y su presupuesto.")), unsafe_allow_html=True)
    if pub.get("procesos"):
        st.markdown(_publicado_band(pub), unsafe_allow_html=True)
        st.markdown(_intro(
            f"<b>Lo publicado en el SERCOP al corte {pub.get('corte', '')}:</b> {pub.get('n_procesos', 0)} procesos "
            f"por <b>${pub.get('total_usd', 0):,.0f}</b> (valor referencial de planificación). El detalle, proceso "
            f"por proceso y directo de la fuente oficial:"), unsafe_allow_html=True)
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
                f"PAC todavía está en preparación, porque el gasto público arranca lento y se acelera en el "
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
        "El <b>presupuesto de inversión</b> es el dinero con el que efectivamente se construye y se compra: "
        "bienes y obras. La tabla separa dos cifras que suelen confundirse:<br>• lo <b>codificado</b> —lo "
        "asignado y disponible para gastar—,<br>• y lo <b>devengado</b> —lo que ya se ejecutó al corte—.<br>"
        "Importante: <b>no es el presupuesto municipal total</b> (que incluye sueldos y gasto corriente), sino "
        "específicamente la <b>inversión</b>, que es la parte con la que se relacionan las metas del plan y la "
        "contratación. Por ley, cómo se prioriza este gasto se decide con <b>participación ciudadana</b> "
        "<span class='pl-law'>COOTAD · Art. 238</span>."
        + _ley_row(plan, "presupuesto", "— el presupuesto de los GAD se ajusta obligatoriamente al plan de "
                   "desarrollo y de ordenamiento territorial.")), unsafe_allow_html=True)
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
            f"porque el gasto público es de <b>carga tardía</b> (las obras grandes arrancan a mitad de año). El "
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
                f"están efectivamente moviéndose al corte —y cuáles todavía no arrancan."),
                unsafe_allow_html=True)


def _sec_coherencia(plan: dict) -> None:
    sat = plan.get("sat0", {}) or {}
    sat_temp = sat.get("global_temp", "alerta")
    st.markdown(_head("6", "LA COHERENCIA", "del plan al gasto, proceso por proceso · la señal preventiva"),
                unsafe_allow_html=True)
    st.markdown(_stepper(sat_temp), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.15], gap="large")
    with c1:
        st.markdown(_pills(sat.get("componentes", [])), unsafe_allow_html=True)
    with c2:
        st.markdown(_narr(
            "Esta es la lectura preventiva —el valor propio de QUIRA—. El sistema contrasta lo <b>planificado</b> "
            "(POA) con lo <b>contratado</b> (PAC), <b>proceso por proceso</b>, y revisa cuatro señales: que no se "
            "abra una brecha entre plan y contratación, que no se fragmenten montos, que cada proceso supere el "
            "mínimo de análisis y que la evidencia llegue a tiempo. Los procesos ya vinculados a una meta marcan "
            "<b>coherencia</b>; la señal preventiva se concentra donde ese vínculo aún no está cerrado. <b>No es "
            "una falta ni una sanción</b>: es señalar <b>dónde cerrar la coherencia antes</b> de ejecutar, para "
            "que el plan no se erosione en el camino del papel al gasto real."),
            unsafe_allow_html=True)


def _cierre(plan: dict) -> None:
    pres = plan.get("presupuesto", {}) or {}
    corte = pres.get("corte", "Q1-2026")
    st.markdown(
        f'<div class="pl-cierre">'
        f'<div class="pl-cierre-lbl">En síntesis</div>'
        f'<div class="pl-cierre-txt">El plan <b>sostiene su diseño</b>: las metas del PDOT se traducen en '
        f'operación (POA), contratación (PAC) y presupuesto coherentes entre sí. El foco preventivo está en que '
        f'<b>la contratación y la ejecución alcancen al presupuesto</b> conforme avanza el año fiscal, para que la '
        f'correspondencia del plan no se erosione en el camino al gasto.</div>'
        f'<div class="pl-src">Fuente: PDOT · POA · PAC (SERCOP) · presupuesto eSIGEF · corte {corte}.</div>'
        f'</div>',
        unsafe_allow_html=True)


def render() -> None:
    """QINV-001 · Planificación Estratégica — lectura documental continua (sin pestañas)."""
    d = _cargar()
    plan = d.get("plan") or {}
    st.markdown(_css(), unsafe_allow_html=True)
    st.markdown('<div class="pl-wrap">', unsafe_allow_html=True)

    if not plan:
        st.markdown('<div style="font-size:15px;color:#7E8BA3;padding:20px 0">'
                    '— evidencia del plan pendiente de carga —</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    pres = plan.get("presupuesto", {}) or {}
    corte = pres.get("corte", "Q1-2026")

    # título limpio (sin encabezado forense · sin pregunta · sin estado)
    st.markdown(
        f'<div class="pl-title-band"><div class="pl-title">Planificación Estratégica</div>'
        f'<div class="pl-sub">La columna vertebral del municipio, leída de principio a fin: del plan de '
        f'desarrollo a la ejecución del gasto — <b>PDOT → POA → contratación → presupuesto</b>, al corte '
        f'{corte}.</div></div>',
        unsafe_allow_html=True)

    # cobertura de metas (encuadre correcto · no es brecha)
    st.markdown(_cobertura_band(plan.get("cobertura_metas_poa")), unsafe_allow_html=True)

    # resumen de la columna vertebral
    st.markdown(_cruce(plan), unsafe_allow_html=True)

    # los eslabones, uno tras otro (tabla + gráfica + texto)
    _sec_pdot(plan)
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_poa(plan)
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_pac(plan)
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_presupuesto(plan)
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_ipe(plan)
    st.markdown(_div(), unsafe_allow_html=True)
    _sec_coherencia(plan)

    # cierre factual corto (sin IA, sin veredicto %)
    _cierre(plan)
    st.markdown('</div>', unsafe_allow_html=True)
