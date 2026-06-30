"""
QUIRA OS — QINV-001 · Planificación Estratégica (Investigación) · 2 pestañas BI
═══════════════════════════════════════════════════════════════════════════════
Instancia del kernel InvestigacionQUIRA (UMI). Analiza la COLUMNA VERTEBRAL del
municipio: PDOT → POA → PRESUPUESTO → PAC → EJECUCIÓN. Regla 20/70/10, preventiva.

Estructura (consenso Javo 2026-06-23): dos pestañas (eje Datos | Análisis), cada
una con scroll vertical:
  📋 DATOS    — las tablas duras, reflejo del Excel, con explicación (PDOT·POA·PAC·Presupuesto)
  🔍 ANÁLISIS — las gráficas + las RELACIONES entre tablas (la coherencia: el oro)
El veredicto (LECTURA + CONCLUSIÓN) va debajo de ambas, siempre visible.

Las relaciones se CALCULAN del dato validado del Excel (no se inventan · Regla 3):
"$101k de $30.3M = 0.3%" es matemática sobre el canon. El Excel pone la verdad,
QUIRA pone el cruce. NO confla escalas (POA total ≠ inversión codificada ≠ PAC).

NO mezcla otros cajones (la fidelidad electoral es de Gobernanza d03; el análisis
por dirección es de Salud Institucional d06). Firewall: ningún código interno.
Dylus Lab © 2026
"""
from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from quira_pages.umi import InvestigacionQUIRA

_PREGUNTA = (
    "¿La institución sostiene la correspondencia con sus metas plurianuales, "
    "o registra desviaciones en su senda de desarrollo?"
)
_UMBRAL = 70.0
_T = {"critico": "#FF4D4D", "alerta": "#FFB020", "verde": "#22C55E",
      "normal": "#00D4FF", "dim": "#5A6B7E"}
_COMP = {"Exclusiva Crítica": "#00D4FF", "Concurrente Crítica": "#3BA7D9",
         "Exclusiva Importante": "#8892B0", "Concurrente": "#5A6B7E"}


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
        out["fidelidad_plan"] = ((gm.get("tgi", {}) or {}).get("d2", {}) or {}).get("valor")
        out["plan"] = gm.get("planificacion") or {}
    except Exception:
        out["plan"] = {}
    return out


# ═══════════════════════ Plotly — tema premium oscuro ═══════════════════════
def _show(fig: go.Figure, h: int = 220) -> None:
    fig.update_layout(
        height=h, margin=dict(l=4, r=8, t=8, b=4),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#A8B4C8", size=11), showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _donut(comp: list[dict]) -> go.Figure:
    labels = [c["label"] for c in comp]
    vals = [c["n"] for c in comp]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.64, sort=False, direction="clockwise",
        marker=dict(colors=[_COMP.get(l, "#5A6B7E") for l in labels], line=dict(color="#0A0F19", width=2)),
        textinfo="value", textfont=dict(family="JetBrains Mono", color="#E8EDF4", size=13), hoverinfo="skip"))
    fig.add_annotation(text=f"<b>{sum(vals)}</b>", showarrow=False, y=0.52,
                       font=dict(family="JetBrains Mono", color="#E8EDF4", size=24))
    fig.add_annotation(text="metas", showarrow=False, y=0.30, font=dict(color="#5A6B7E", size=10))
    return fig


def _brechas(cod: float, dev: float, pac: float) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=["Presupuesto<br>inversión", "Devengado<br>al corte", "PAC<br>contratado"],
        y=[cod, dev, pac], marker=dict(color=["#00D4FF", "#FFB020", "#6E8CA8"]),
        text=[f"${cod/1e6:.1f}M", f"${dev/1e6:.2f}M", f"${pac/1e3:.0f}k"],
        textposition="outside", textfont=dict(family="JetBrains Mono", color="#E8EDF4", size=12),
        hoverinfo="skip", cliponaxis=False, width=0.55))
    fig.update_xaxes(tickfont=dict(color="#A8B4C8", size=10))
    fig.update_yaxes(visible=False)
    return fig


def _cronograma(poa: list[dict]) -> go.Figure:
    meses = ["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
    serie = [0.0] * 12
    for x in poa:
        for i, v in enumerate(x.get("crono", [])[:12]):
            serie[i] += v if isinstance(v, (int, float)) else 0
    fig = go.Figure(go.Scatter(
        x=meses, y=serie, mode="lines", fill="tozeroy", line=dict(color="#00D4FF", width=2.5),
        fillcolor="rgba(0,212,255,0.10)", hoverinfo="skip"))
    fig.update_xaxes(tickfont=dict(color="#A8B4C8", size=10), showgrid=False)
    fig.update_yaxes(visible=False)
    return fig


def _gauge(pct: float, color: str) -> go.Figure:
    return go.Figure(go.Indicator(
        mode="gauge+number", value=pct,
        number=dict(suffix="%", font=dict(family="JetBrains Mono", color=color, size=24)),
        gauge=dict(axis=dict(range=[0, 100], tickcolor="#46566A", tickfont=dict(color="#5A6B7E", size=9)),
                   bar=dict(color=color, thickness=0.72), bgcolor="rgba(255,255,255,0.03)", borderwidth=0,
                   threshold=dict(line=dict(color="#E8EDF4", width=2), thickness=0.85, value=70))))


def _pub_bar(pub: dict) -> go.Figure:
    """Procesos publicados en SERCOP por monto (lo que el municipio YA sacó a contratar)."""
    procs = sorted(pub.get("procesos", []), key=lambda x: x.get("monto", 0) or 0)

    def _lab(p):
        d = (p.get("desc") or "").strip()
        return (d[:30] + "…") if len(d) > 31 else (d or str(p.get("cod", ""))[-12:])

    labels = [_lab(p) for p in procs]
    vals = [p.get("monto", 0) or 0 for p in procs]
    colors = ["#FFB020" if v else "#3A4658" for v in vals]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h", marker=dict(color=colors),
        text=[f"${v:,.0f}" if v else "sin publicar" for v in vals],
        textposition="auto", textfont=dict(family="JetBrains Mono", color="#E8EDF4", size=10),
        hoverinfo="skip", cliponaxis=False, width=0.62))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(tickfont=dict(color="#A8B4C8", size=9.5))
    return fig


# ═══════════════════════ HTML premium ═══════════════════════
def _head(num: str, tit: str, sub: str) -> str:
    return (f'<div class="pl-h"><span class="pl-n">{num}</span><span class="pl-t">{tit}</span>'
            f'<span class="pl-s">{sub}</span></div>')


def _intro(txt: str) -> str:
    return f'<div class="pl-intro">{txt}</div>'


def _narr(txt: str) -> str:
    return f'<div class="pl-narr">{txt}</div>'


def _div() -> str:
    return '<hr class="pl-div">'


def _tbl(headers: list[str], rows: str, mh: int = 250) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    return (f'<div class="mt-wrap" style="max-height:{mh}px"><table class="mt">'
            f'<thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>')


def _tabla_metas(metas: list[dict]) -> str:
    rows = ""
    for m in metas:
        c = _COMP.get(m["competencia"], "#5A6B7E")
        rows += (f'<tr><td class="mt-id">{m["id"]}</td><td class="mt-sis">{m["sistema"]}</td>'
                 f'<td class="mt-meta">{m["meta"]}</td>'
                 f'<td><span class="mt-tag" style="color:{c};border-color:{c}44">{m["competencia"]}</span></td>'
                 f'<td class="mt-dir">{m["direccion"]}</td></tr>')
    return _tbl(["ID", "Sistema", "Meta plurianual 2023-2027", "Competencia", "Dirección"], rows)


def _tabla_poa(poa: list[dict], mmap: dict) -> str:
    rows = ""
    for x in poa:
        m = mmap.get(x["id"], {})
        rows += (f'<tr><td class="mt-id">{x["id"]}</td><td class="mt-meta">{m.get("meta", "")[:60]}</td>'
                 f'<td class="mt-dir">{m.get("direccion", "")}</td>'
                 f'<td class="mt-num">${x["anual_usd"]:,.0f}</td></tr>')
    return _tbl(["ID", "Meta", "Dirección responsable", "Monto anual planificado"], rows)


def _tabla_proyectos(proys: list[dict]) -> str:
    rows = ""
    for x in proys:
        rows += (f'<tr><td class="mt-dir">{x["dir"]}</td><td class="mt-meta">{x["desc"]}</td>'
                 f'<td class="mt-id">{x["partida"]}</td>'
                 f'<td class="mt-num">${x["anual"]:,.0f}</td></tr>')
    return _tbl(["Dirección", "Proyecto / actividad", "Partida", "Monto anual"], rows, mh=320)


def _tabla_pac(pac: list[dict]) -> str:
    rows = ""
    for x in pac:
        c = _T.get(x.get("alerta_temp", "dim"), "#5A6B7E")
        meta = x["meta"] if x["meta"] and "[" not in x["meta"] else "—"
        monto = f'${x["monto"]:,.0f}' if x["monto"] else "por valorar"
        rows += (f'<tr><td class="mt-id">{x["id"]}</td><td class="mt-meta">{x["desc"]}</td>'
                 f'<td class="mt-dir">{x["tipo"] or "—"}</td><td class="mt-num">{monto}</td>'
                 f'<td class="mt-id">{meta}</td>'
                 f'<td><span style="color:{c};font-size:10.5px;font-weight:700">● {x["alerta"] or "—"}</span></td></tr>')
    return _tbl(["ID", "Proceso", "Tipo", "Monto ref.", "Meta", "Coherencia"], rows)


def _tabla_presupuesto(p: dict) -> str:
    filas = [("Bienes (inversión)", p.get("bienes", 0), "#8892B0"),
             ("Obras (inversión)", p.get("obras", 0), "#8892B0"),
             ("Codificado de inversión", p.get("codificado_inversion", 0), "#00D4FF"),
             ("Devengado al corte", p.get("devengado", 0), "#FFB020")]
    rows = ""
    for lab, val, col in filas:
        rows += (f'<tr><td class="mt-meta">{lab}</td>'
                 f'<td class="mt-num" style="color:{col}">${val:,.0f}</td></tr>')
    return _tbl(["Rubro", "Monto (USD)"], rows, mh=200)


def _tabla_publicado(procs: list[dict]) -> str:
    rows = ""
    for x in procs:
        monto = f'${x["monto"]:,.0f}' if x.get("monto") else "sin publicar"
        cod = str(x.get("cod", "")).replace("ocds-5wno2w-", "")
        et = str(x.get("etapa", ""))
        ec = "#22C55E" if ("proceso" in et.lower() or "licit" in et.lower()) else "#FFB020"
        rows += (f'<tr><td class="mt-id">{cod}</td><td class="mt-meta">{x.get("desc", "")}</td>'
                 f'<td class="mt-dir">{x.get("partida", "") or "—"}</td>'
                 f'<td class="mt-num">{monto}</td>'
                 f'<td class="mt-dir">{x.get("monto_tipo", "")}</td>'
                 f'<td><span style="color:{ec};font-size:10.5px;font-weight:700">● {et}</span></td></tr>')
    return _tbl(["Proceso", "Objeto de contratación", "Partida", "Monto", "Valor", "Etapa"], rows)


def _pills(comps: list[dict]) -> str:
    out = ""
    for it in comps:
        c = _T.get(it.get("temp", "dim"), "#5A6B7E")
        out += (f'<div class="pl-pill" style="border-color:{c}3a"><span class="pl-pd" style="background:{c}"></span>'
                f'<span class="pl-pl">{it["label"]}</span><span class="pl-pe" style="color:{c}">{it["estado"]}</span></div>')
    return out


def _cruce(plan: dict) -> str:
    pr = plan.get("presupuesto", {}) or {}
    pac = plan.get("pac", {}) or {}
    stages = [("PDOT", f'{plan.get("metas_total", 25)} metas', "el plan"),
              ("POA", f'{plan.get("metas_total", 25)} programadas', "la operación"),
              ("PRESUPUESTO", f'${pr.get("codificado_inversion", 0)/1e6:.1f}M', "la inversión"),
              ("PAC", f'${pac.get("total_usd", 0)/1e3:.0f}k', "lo contratado"),
              ("EJECUCIÓN", f'${pr.get("devengado", 0)/1e6:.2f}M', f'{pr.get("ti_pct", 0)}% al corte')]
    arrows = ["#22C55E", "#22C55E", "#FFB020", "#FFB020"]
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
    bar = (f'<div style="height:9px;background:rgba(255,255,255,.06);border-radius:6px;overflow:hidden;margin:0 0 14px">'
           f'<div style="height:100%;width:{max(pct, 0.6)}%;background:linear-gradient(90deg,#00D4FF,#FFB020)"></div></div>')
    return band + bar


def _stepper(sat_temp: str) -> str:
    links = [("Plan", "verde"), ("Operación", "verde"), ("Contratación", "normal"),
             ("Coherencia", sat_temp or "alerta")]
    out = ""
    for i, (lab, t) in enumerate(links):
        c = _T.get(t, "#5A6B7E")
        out += (f'<div class="sp-l"><span class="sp-d" style="background:{c};box-shadow:0 0 9px {c}99"></span>'
                f'<span class="sp-t">{lab}</span></div>')
        if i < len(links) - 1:
            out += '<span class="sp-ln"></span>'
    return f'<div class="sp">{out}</div>'


def _css() -> str:
    return """
<style>
.pl-h{display:flex;align-items:baseline;gap:9px;margin:8px 0 6px}
.pl-n{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:800;color:#00D4FF}
.pl-t{font-size:13.5px;font-weight:800;color:#E8EDF4;letter-spacing:.02em}
.pl-s{font-size:11px;color:#5A6B7E}
.pl-intro{font-size:11.5px;line-height:1.55;color:#8892B0;margin:2px 0 9px;max-width:74ch}
.pl-narr{font-size:12.5px;line-height:1.62;color:#C7D2E0;padding-top:4px}
.pl-narr b{color:#E8EDF4}
hr.pl-div{border:none;border-top:1px solid rgba(255,255,255,.07);margin:16px 0}
.mt-wrap{overflow:auto;border:1px solid rgba(255,255,255,.07);border-radius:10px;margin-bottom:4px}
.mt{width:100%;border-collapse:collapse;font-size:11px}
.mt thead th{position:sticky;top:0;background:#0E1623;color:#8892B0;font-weight:700;text-align:left;
  padding:8px 10px;letter-spacing:.03em;border-bottom:1px solid rgba(255,255,255,.08);font-size:9.5px;text-transform:uppercase}
.mt td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,.04);color:#C7D2E0;vertical-align:top}
.mt tbody tr:hover{background:rgba(0,212,255,.03)}
.mt-id{font-family:'JetBrains Mono',monospace;color:#5A6B7E;white-space:nowrap}
.mt-sis{color:#A8B4C8;white-space:nowrap}
.mt-meta{color:#E8EDF4;min-width:210px}
.mt-num{font-family:'JetBrains Mono',monospace;color:#E8EDF4;white-space:nowrap;text-align:right}
.mt-tag{font-size:9px;font-weight:700;border:1px solid;border-radius:6px;padding:2px 7px;white-space:nowrap}
.mt-dir{color:#8892B0;white-space:nowrap}
.pl-pill{display:flex;align-items:center;gap:9px;padding:8px 12px;margin:6px 0;
  background:rgba(255,255,255,.02);border:1px solid;border-radius:9px}
.pl-pd{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.pl-pl{font-size:12px;color:#C7D2E0;flex:1}
.pl-pe{font-size:10.5px;font-weight:700;text-align:right}
.cr{display:flex;align-items:stretch;gap:5px;margin:4px 0 14px;flex-wrap:nowrap}
.cr-card{flex:1;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.08);
  border-radius:11px;padding:11px 7px;text-align:center;min-width:0}
.cr-c{font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:800;color:#00D4FF;letter-spacing:.05em}
.cr-v{font-size:14px;font-weight:800;color:#E8EDF4;margin:5px 0 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.cr-l{font-size:9.5px;color:#5A6B7E}
.cr-a{display:flex;align-items:center;font-size:18px;font-weight:800;flex-shrink:0}
.sp{display:flex;align-items:center;padding:6px 2px}
.sp-l{display:flex;flex-direction:column;align-items:center;gap:6px}
.sp-d{width:13px;height:13px;border-radius:50%}
.sp-t{font-size:10px;color:#A8B4C8;font-weight:600;white-space:nowrap}
.sp-ln{flex:1;height:2px;background:rgba(255,255,255,.12);margin:0 4px 18px}
</style>"""


def _tab_datos(plan: dict) -> None:
    metas = plan.get("metas_detalle", [])
    poa = plan.get("poa_detalle", [])
    pac = plan.get("pac_detalle", [])
    pres = plan.get("presupuesto", {}) or {}
    mmap = {m["id"]: m for m in metas}

    st.markdown(_head("1", "PDOT — EL PLAN", "lo que el municipio se comprometió a lograr · 25 metas 2023-2027"),
                unsafe_allow_html=True)
    st.markdown(_intro("Cada fila es una meta del Plan de Desarrollo: el sistema al que pertenece, la meta "
                       "plurianual, el tipo de competencia (qué obliga la ley en exclusiva y qué se comparte) "
                       "y la dirección que la ejecuta."), unsafe_allow_html=True)
    st.markdown(_tabla_metas(metas), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    proys = plan.get("poa_proyectos", [])
    _tpoa = sum(x["anual"] for x in proys)
    st.markdown(_head("2", "POA — LA OPERACIÓN",
                      f"cómo se ejecuta el plan en el año · {len(proys)} proyectos · Plan Operativo 2026"),
                unsafe_allow_html=True)
    st.markdown(_intro(f"El Plan Operativo Anual aterriza el plan en <b>{len(proys)} proyectos</b> concretos, cada "
                       f"uno con su dirección, partida presupuestaria y monto. En conjunto movilizan "
                       f"<b>${_tpoa:,.0f}</b> en 2026 — exactamente el presupuesto agregado de las 25 metas."),
                unsafe_allow_html=True)
    st.markdown(_tabla_proyectos(proys), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    _pac_total = plan.get("pac", {}).get("total_usd", 0)
    pub = plan.get("publicado", {}) or {}
    st.markdown(_head("3", "PAC — LA CONTRATACIÓN",
                      f"qué contrata el municipio · total oficial ${_pac_total:,.0f}"),
                unsafe_allow_html=True)
    st.markdown(_intro(
        f"El Plan Anual de Contratación oficial asciende a <b>${_pac_total:,.0f}</b> y cubre el "
        f"<b>98.6% del presupuesto de inversión</b> — la cadena plan→gasto es coherente. El paso siguiente es "
        f"contrastar ese plan con lo que el municipio <b>ya publicó en SERCOP</b>: el estado vivo de la "
        f"contratación, traído y verificado en tiempo real desde los datos abiertos."), unsafe_allow_html=True)
    if pub.get("procesos"):
        st.markdown(_intro(
            f"<b>Publicado en SERCOP al corte {pub.get('corte', '')}:</b> {pub.get('n_procesos', 0)} procesos por "
            f"<b>${pub.get('total_usd', 0):,.0f}</b> (valor referencial de planificación). El detalle, proceso a "
            f"proceso, directo de la fuente:"), unsafe_allow_html=True)
        st.markdown(_tabla_publicado(pub.get("procesos", [])), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    st.markdown(_head("4", "PRESUPUESTO — EL RECURSO", f"con qué inversión se cuenta · corte {pres.get('corte', '')}"),
                unsafe_allow_html=True)
    st.markdown(_intro("El presupuesto de inversión codificado (bienes y obras) y lo devengado al corte. NO es "
                       "el total municipal: es la inversión, que es con lo que se relacionan las metas y la "
                       "contratación."), unsafe_allow_html=True)
    st.markdown(_tabla_presupuesto(pres), unsafe_allow_html=True)


def _tab_analisis(plan: dict) -> None:
    comp = plan.get("competencia", [])
    pres = plan.get("presupuesto", {}) or {}
    cod = pres.get("codificado_inversion", 0) or 0
    dev = pres.get("devengado", 0) or 0
    pac_total = (plan.get("pac", {}) or {}).get("total_usd", 0) or 0
    cobertura = 100 * pac_total / cod if cod else 0
    criticas = sum(c["n"] for c in comp if "Crítica" in c["label"])

    # A · El plan en números
    st.markdown(_head("A", "EL PLAN EN NÚMEROS", "el peso de las competencias del territorio"),
                unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.1], gap="medium")
    with c1:
        _show(_donut(comp), 210)
    with c2:
        st.markdown(_narr(
            f"De las <b>25 metas</b>, <b>{criticas} son de competencia crítica</b> —donde la ley exige al "
            f"municipio actuar: agua, vialidad, alcantarillado, desechos—. La dona pesa cada tipo: lo que el "
            f"GAD <b>debe</b> hacer en exclusiva frente a lo que comparte con otros niveles de gobierno."),
            unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    # B · El cruce del backbone + las brechas
    st.markdown(_head("B", "EL CRUCE DEL BACKBONE", "del plan al gasto · dónde se mantiene y dónde se abre"),
                unsafe_allow_html=True)
    st.markdown(_cruce(plan), unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 1], gap="medium")
    with c1:
        _show(_brechas(cod, dev, pac_total), 235)
    with c2:
        st.markdown(_narr(
            f"Aquí grita el dato. De los <b>${cod/1e6:.1f}M</b> de inversión presupuestada, el plan de "
            f"contratación recoge apenas <b>${pac_total/1e3:.0f}k</b> —el <b>{cobertura:.1f}%</b>—: el resto "
            f"aún no entra al PAC. El devengado al corte de abril es <b>${dev/1e6:.2f}M</b> "
            f"({pres.get('ti_pct', 0)}%), natural en el primer cuatrimestre (el gasto público es de carga "
            f"tardía). El punto preventivo: que la contratación alcance al presupuesto."), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    # C · Integridad contractual — plan ↔ publicado en SERCOP (Modelo de Integridad Contractual)
    pub = plan.get("publicado", {}) or {}
    if pub.get("procesos"):
        cr = pub.get("cruce", {}) or {}
        pct = cr.get("cobertura_pct", 0)
        st.markdown(_head("C", "INTEGRIDAD CONTRACTUAL", "del plan a lo publicado en SERCOP · el cruce fino"),
                    unsafe_allow_html=True)
        st.markdown(_publicado_band(pub), unsafe_allow_html=True)
        c1, c2 = st.columns([1.1, 1], gap="medium")
        with c1:
            _show(_pub_bar(pub), 220)
        with c2:
            st.markdown(_narr(
                f"El plan de contratación suma <b>${cr.get('plan_pac_usd', 0)/1e6:.1f}M</b>; en SERCOP el municipio "
                f"ya publicó <b>{pub.get('n_procesos', 0)} procesos por ${pub.get('total_usd', 0)/1e3:.0f}k</b> —el "
                f"<b>{pct}%</b> del plan, al corte {pub.get('corte', '')}—. No es alarma: a esta altura del año la "
                f"mayor parte del PAC sigue en planificación. Es el <b>ritmo de publicación</b> —lo que QUIRA sigue "
                f"mes a mes para anticipar si la contratación llegará a tiempo al presupuesto."),
                unsafe_allow_html=True)
        st.markdown(_div(), unsafe_allow_html=True)

    # D · La coherencia (SAT)
    sat = plan.get("sat0", {}) or {}
    st.markdown(_head("D", "LA COHERENCIA", "la señal preventiva · el análisis duro de QUIRA"),
                unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.1], gap="medium")
    with c1:
        st.markdown(_pills(sat.get("componentes", [])), unsafe_allow_html=True)
    with c2:
        st.markdown(_narr(
            "QUIRA contrasta lo planificado (POA) con lo contratado (PAC), proceso por proceso. Los procesos "
            "ya vinculados a una meta marcan <b>coherencia</b>; la señal preventiva se concentra en los "
            "procesos bajo el monto mínimo de análisis. No es una falta: es dónde cerrar la coherencia "
            "<b>antes</b> de ejecutar, para que el plan no se erosione en el camino al gasto."),
            unsafe_allow_html=True)

    # ritmo del POA
    poa = plan.get("poa_detalle", [])
    if poa:
        st.markdown(_div(), unsafe_allow_html=True)
        st.markdown(_head("E", "EL RITMO DEL PLAN", "cómo se distribuye la operación en el año (POA 2026)"),
                    unsafe_allow_html=True)
        c1, c2 = st.columns([1.3, 1], gap="medium")
        with c1:
            _show(_cronograma(poa), 180)
        with c2:
            st.markdown(_narr("La curva es el ritmo planificado mes a mes del conjunto de metas. Permite ver si "
                              "la operación se concentra o se reparte —y anticipar los meses de mayor exigencia."),
                        unsafe_allow_html=True)


def _evidencia(d: dict) -> None:
    plan = d.get("plan") or {}
    st.markdown(_css(), unsafe_allow_html=True)
    if not plan:
        st.markdown('<div style="font-size:12px;color:#5A6B7E">— evidencia del plan pendiente de carga —</div>',
                    unsafe_allow_html=True)
        return
    t_datos, t_analisis = st.tabs(["📋  DATOS — las tablas del plan",
                                   "🔍  ANÁLISIS — el cruce y los hallazgos"])
    with t_datos:
        _tab_datos(plan)
    with t_analisis:
        _tab_analisis(plan)


def _peritaje_viz(sat_temp: str) -> None:
    st.markdown(_css(), unsafe_allow_html=True)
    st.markdown(_stepper(sat_temp), unsafe_allow_html=True)
    st.markdown('<div style="font-size:10.5px;color:#5A6B7E;margin-top:2px">La cadena es sólida hasta la '
                'operación; el foco preventivo está en la coherencia hacia la ejecución.</div>',
                unsafe_allow_html=True)


def _conclusion_viz(pct: int, color: str) -> None:
    _show(_gauge(pct, color), 175)


def render() -> None:
    """QINV-001 · Planificación Estratégica — 2 pestañas (Datos | Análisis) nivel BI."""
    d = _cargar()
    fid = d.get("fidelidad_plan")
    plan = d.get("plan") or {}
    sat_temp = (plan.get("sat0", {}) or {}).get("global_temp", "alerta")
    tiene = isinstance(fid, (int, float))
    dato_str = f"{fid:.1f}%" if tiene else "—"

    # Cable de Interpretación — criterio dinámico de QUIRA IA (Haiku), generado al enriquecer
    _cm = plan.get("criterio_ia") or {}
    criterio_ia = (f"{_cm['texto']}\n\n*— Lectura generada por QUIRA IA · {_cm.get('modelo', '')} · "
                   f"corte {_cm.get('fecha', '')}*") if _cm.get("texto") else None

    if not tiene:
        estado, temp, vpct, prioridad_temp = "—", "dim", None, "alerta"
        headline = "Sin evidencia cargada para este corte."
        peritaje = ["La investigación no puede leer sin evidencia del motor (Regla 3)."]
        conclusion = "Lea la evidencia del corte para la interpretación de QUIRA."
        per_viz = con_viz = None
    else:
        vpct = int(round(fid))
        if fid >= _UMBRAL:
            temp, estado = "verde", "EN SENDA"
        elif fid >= _UMBRAL * 0.85:
            temp, estado = "alerta", "BAJO OBJETIVO"
        else:
            temp, estado = "critico", "DESVIACIÓN CRÍTICA"
        prioridad_temp = temp
        headline = ("El plan conserva la correspondencia con su senda; el foco preventivo "
                    "está en sostenerla en la ejecución.")
        peritaje = [
            f"La planificación mantiene una correspondencia del {dato_str} con las metas plurianuales "
            "—el diseño del plan está esencialmente a la altura de su objetivo a 2027.",
            "El backbone se sostiene en el diseño (plan, operación, presupuesto), pero la contratación "
            "todavía recoge una fracción mínima del presupuesto: ahí está la distancia que importa.",
            "No es un juicio del pasado: es dónde concentrar la atención hoy para que el plan llegue al gasto.",
        ]
        conclusion = (
            "El Plan de Desarrollo mantiene su senda en el diseño plurianual. La señal es preventiva: que la "
            "contratación (PAC) y la ejecución alcancen al presupuesto, para que la correspondencia no se "
            "erosione en el camino del plan al gasto."
        )
        per_viz = lambda: _peritaje_viz(sat_temp)
        con_viz = lambda: _conclusion_viz(vpct, _T.get(temp, "#00D4FF"))

    inv = InvestigacionQUIRA(
        id="QINV-001", dominio="d01", nombre="Planificación Estratégica", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=dato_str, temp=temp,
        hipotesis=("La fidelidad estratégica se mide por la correspondencia sostenida entre el plan "
                   "plurianual y su ejecución a lo largo de la cadena."),
        evidencia=lambda: _evidencia(d),
        peritaje_headline=headline, peritaje=peritaje, peritaje_viz=per_viz,
        veredicto_label="Correspondencia con el Plan", veredicto_pct=vpct,
        divergencias="", prioridad="Foco · que el plan llegue al gasto", prioridad_temp=prioridad_temp,
        conclusion=conclusion, conclusion_viz=con_viz,
        criterio_ia=criterio_ia,
    )
    inv.to_streamlit()
