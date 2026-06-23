"""
QUIRA OS — QINV-001 · Planificación Estratégica (Investigación) · vista BI
═══════════════════════════════════════════════════════════════════════════════
Instancia del kernel InvestigacionQUIRA (UMI). Investiga la CADENA estratégica del
territorio: PDOT → POA → PAC → Coherencia. Regla 20/70/10, clave PREVENTIVA.

EVIDENCIA NATIVA, nivel BI (Plotly · Javo 2026-06-23): cada sección se construye
aquí con dato real del snapshot (bloque `planificacion`, puente Excel→snapshot vía
scripts/enrich_planificacion.py). Layout cohesivo gráfica + texto. Visualización
adecuada a cada dato: dona (composición) · barras (ranking) · tabla (detalle) ·
diagrama de cruce (cadena) · medidor (veredicto). "Se ve más el Excel" sin exponer
lo canónico.

NO mezcla otros cajones: la fidelidad electoral/IFE es de Gobernanza (d03), aquí NO.
Madre: FIDELIDAD DE PLANIFICACIÓN (correspondencia con las metas · dato real, NO IPE).
Firewall: ningún código interno en la vista (ni ICPI, ni TGI, ni H-series).
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
        font=dict(family="Inter, sans-serif", color="#A8B4C8", size=11),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _donut(comp: list[dict]) -> go.Figure:
    labels = [c["label"] for c in comp]
    vals = [c["n"] for c in comp]
    fig = go.Figure(go.Pie(
        labels=labels, values=vals, hole=0.64, sort=False, direction="clockwise",
        marker=dict(colors=[_COMP.get(l, "#5A6B7E") for l in labels],
                    line=dict(color="#0A0F19", width=2)),
        textinfo="value", textfont=dict(family="JetBrains Mono", color="#E8EDF4", size=13),
        hoverinfo="skip"))
    fig.add_annotation(text=f"<b>{sum(vals)}</b>", showarrow=False, y=0.52,
                       font=dict(family="JetBrains Mono", color="#E8EDF4", size=24))
    fig.add_annotation(text="metas", showarrow=False, y=0.30,
                       font=dict(color="#5A6B7E", size=10))
    return fig


def _bar(items: list[tuple], accent: str = "#3BA7D9") -> go.Figure:
    items = items[::-1]
    labels = [(l[:24] + "…") if len(l) > 25 else l for l, _ in items]
    fig = go.Figure(go.Bar(
        x=[n for _, n in items], y=labels, orientation="h",
        marker=dict(color=accent), text=[n for _, n in items], textposition="outside",
        textfont=dict(family="JetBrains Mono", color="#E8EDF4", size=11),
        hoverinfo="skip", cliponaxis=False))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(tickfont=dict(color="#A8B4C8", size=11), ticksuffix="   ")
    return fig


def _gauge(pct: float, color: str) -> go.Figure:
    return go.Figure(go.Indicator(
        mode="gauge+number", value=pct,
        number=dict(suffix="%", font=dict(family="JetBrains Mono", color=color, size=24)),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#46566A", tickfont=dict(color="#5A6B7E", size=9)),
            bar=dict(color=color, thickness=0.72),
            bgcolor="rgba(255,255,255,0.03)", borderwidth=0,
            threshold=dict(line=dict(color="#E8EDF4", width=2), thickness=0.85, value=70))))


# ═══════════════════════ HTML premium ═══════════════════════
def _head(num: str, tit: str, sub: str) -> str:
    return (f'<div class="pl-h"><span class="pl-n">{num}</span>'
            f'<span class="pl-t">{tit}</span><span class="pl-s">{sub}</span></div>')


def _narr(txt: str) -> str:
    return f'<div class="pl-narr">{txt}</div>'


def _div() -> str:
    return '<hr class="pl-div">'


def _tabla_metas(metas: list[dict]) -> str:
    rows = ""
    for m in metas:
        c = _COMP.get(m["competencia"], "#5A6B7E")
        rows += (f'<tr><td class="mt-id">{m["id"]}</td><td class="mt-sis">{m["sistema"]}</td>'
                 f'<td class="mt-meta">{m["meta"]}</td>'
                 f'<td><span class="mt-comp" style="color:{c};border-color:{c}44">{m["competencia"]}</span></td>'
                 f'<td class="mt-dir">{m["direccion"]}</td></tr>')
    return (f'<div class="mt-wrap"><table class="mt"><thead><tr><th>ID</th><th>Sistema</th>'
            f'<th>Meta plurianual 2023-2027</th><th>Competencia</th><th>Dirección responsable</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>')


def _pills(comps: list[dict]) -> str:
    out = ""
    for it in comps:
        c = _T.get(it.get("temp", "dim"), "#5A6B7E")
        out += (f'<div class="pl-pill" style="border-color:{c}3a"><span class="pl-pd" '
                f'style="background:{c}"></span><span class="pl-pl">{it["label"]}</span>'
                f'<span class="pl-pe" style="color:{c}">{it["estado"]}</span></div>')
    return out


def _cruce(plan: dict) -> str:
    pac = plan.get("pac", {}) or {}
    stages = [("PDOT", f'{plan.get("metas_total", 25)} metas', "el plan"),
              ("POA", f'{plan.get("n_direcciones", 13)} direcciones', "la operación"),
              ("PAC", f'{pac.get("n_procesos", "—")} procesos', "la compra"),
              ("PRESUPUESTO", f'${pac.get("total_usd", 0):,.0f}', "el recurso")]
    arrows = ["#22C55E", "#22C55E", "#FFB020"]
    html = '<div class="cr">'
    for i, (code, val, lab) in enumerate(stages):
        html += (f'<div class="cr-card"><div class="cr-c">{code}</div>'
                 f'<div class="cr-v">{val}</div><div class="cr-l">{lab}</div></div>')
        if i < len(arrows):
            html += f'<div class="cr-a" style="color:{arrows[i]}">→</div>'
    return html + '</div>'


def _stepper(sat_temp: str) -> str:
    links = [("Plan", "verde"), ("Operación", "verde"),
             ("Contratación", "normal"), ("Coherencia", sat_temp or "alerta")]
    out = ""
    for i, (lab, t) in enumerate(links):
        c = _T.get(t, "#5A6B7E")
        out += (f'<div class="sp-l"><span class="sp-d" style="background:{c};'
                f'box-shadow:0 0 9px {c}99"></span><span class="sp-t">{lab}</span></div>')
        if i < len(links) - 1:
            out += '<span class="sp-ln"></span>'
    return f'<div class="sp">{out}</div>'


def _css() -> str:
    return """
<style>
.pl-h{display:flex;align-items:baseline;gap:9px;margin:6px 0 11px}
.pl-n{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:800;color:#00D4FF}
.pl-t{font-size:13.5px;font-weight:800;color:#E8EDF4;letter-spacing:.02em}
.pl-s{font-size:11px;color:#5A6B7E}
.pl-narr{font-size:12.5px;line-height:1.62;color:#C7D2E0;padding-top:6px}
.pl-narr b{color:#E8EDF4}
hr.pl-div{border:none;border-top:1px solid rgba(255,255,255,.07);margin:16px 0}
.mt-wrap{max-height:250px;overflow-y:auto;border:1px solid rgba(255,255,255,.07);
  border-radius:10px;margin-bottom:6px}
.mt{width:100%;border-collapse:collapse;font-size:11px}
.mt thead th{position:sticky;top:0;background:#0E1623;color:#8892B0;font-weight:700;
  text-align:left;padding:8px 10px;letter-spacing:.03em;border-bottom:1px solid rgba(255,255,255,.08);
  font-size:10px;text-transform:uppercase}
.mt td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,.04);color:#C7D2E0;vertical-align:top}
.mt tbody tr:hover{background:rgba(0,212,255,.03)}
.mt-id{font-family:'JetBrains Mono',monospace;color:#5A6B7E;white-space:nowrap}
.mt-sis{color:#A8B4C8;white-space:nowrap}
.mt-meta{color:#E8EDF4;min-width:240px}
.mt-comp{font-size:9.5px;font-weight:700;border:1px solid;border-radius:6px;padding:2px 7px;white-space:nowrap}
.mt-dir{color:#8892B0;white-space:nowrap}
.pl-pill{display:flex;align-items:center;gap:9px;padding:8px 12px;margin:6px 0;
  background:rgba(255,255,255,.02);border:1px solid;border-radius:9px}
.pl-pd{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.pl-pl{font-size:12px;color:#C7D2E0;flex:1}
.pl-pe{font-size:10.5px;font-weight:700;text-align:right}
.cr{display:flex;align-items:stretch;gap:6px;margin:4px 0 14px;flex-wrap:nowrap}
.cr-card{flex:1;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.08);
  border-radius:11px;padding:12px 10px;text-align:center;min-width:0}
.cr-c{font-family:'JetBrains Mono',monospace;font-size:9.5px;font-weight:800;color:#00D4FF;
  letter-spacing:.08em}
.cr-v{font-size:15px;font-weight:800;color:#E8EDF4;margin:5px 0 2px;white-space:nowrap;
  overflow:hidden;text-overflow:ellipsis}
.cr-l{font-size:10px;color:#5A6B7E}
.cr-a{display:flex;align-items:center;font-size:20px;font-weight:800;flex-shrink:0}
.sp{display:flex;align-items:center;padding:8px 2px}
.sp-l{display:flex;flex-direction:column;align-items:center;gap:6px}
.sp-d{width:13px;height:13px;border-radius:50%}
.sp-t{font-size:10px;color:#A8B4C8;font-weight:600;white-space:nowrap}
.sp-ln{flex:1;height:2px;background:rgba(255,255,255,.12);margin:0 4px;margin-bottom:18px}
</style>"""


def _evidencia(d: dict) -> None:
    plan = d.get("plan") or {}
    st.markdown(_css(), unsafe_allow_html=True)
    if not plan:
        st.markdown('<div style="font-size:12px;color:#5A6B7E">— evidencia del plan '
                    'pendiente de carga —</div>', unsafe_allow_html=True)
        return

    comp = plan.get("competencia", [])
    metas = plan.get("metas_detalle", [])
    total = plan.get("metas_total", 25)
    criticas = sum(c["n"] for c in comp if "Crítica" in c["label"])

    # ① EL PLAN — tabla (Excel) + dona + texto
    st.markdown(_head("①", "EL PLAN", f"qué comprometió el territorio · {total} metas plurianuales (PDOT)"),
                unsafe_allow_html=True)
    st.markdown(_tabla_metas(metas), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.1], gap="medium")
    with c1:
        _show(_donut(comp), 210)
    with c2:
        st.markdown(_narr(
            f"De las <b>{total} metas</b> del Plan de Desarrollo, <b>{criticas} son de "
            f"competencia crítica</b> del GAD —agua, vialidad, alcantarillado, desechos—: "
            f"ahí se concentra la mayor obligación de ley. La tabla de arriba es el plan "
            f"completo, tal como vive en el motor; la dona muestra su peso por tipo de "
            f"competencia."), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    # ② LA OPERACIÓN — barras direcciones + texto
    dirs = plan.get("direcciones", [])
    multi = [(x["dir"], x["n"]) for x in dirs if x["n"] > 1]
    st.markdown(_head("②", "LA OPERACIÓN", "quién la ejecuta · del plan al POA 2026"),
                unsafe_allow_html=True)
    c1, c2 = st.columns([1.15, 1], gap="medium")
    with c1:
        _show(_bar(multi, "#3BA7D9"), 220)
    with c2:
        top = multi[0][0] if multi else "—"
        st.markdown(_narr(
            f"Las {total} metas se traducen en el Plan Operativo 2026, repartidas en "
            f"<b>{plan.get('n_direcciones', '—')} direcciones</b>. <b>{top}</b> y Gestión "
            f"Ambiental cargan el mayor número. Cada meta tiene una dirección responsable: "
            f"el plan no quedó en papel, aterrizó en la institución."), unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    # ③ LA CONTRATACIÓN — barras tipos + texto
    pac = plan.get("pac", {}) or {}
    tipos = [(t["tipo"], t["n"]) for t in pac.get("tipos", [])][:5]
    st.markdown(_head("③", "LA CONTRATACIÓN", f"con qué se compra · PAC ${pac.get('total_usd', 0):,.0f}"),
                unsafe_allow_html=True)
    c1, c2 = st.columns([1.15, 1], gap="medium")
    with c1:
        _show(_bar(tipos, "#6E8CA8"), 200)
    with c2:
        st.markdown(_narr(
            f"El Plan Anual de Contratación programa <b>${pac.get('total_usd', 0):,.0f}</b> "
            f"en <b>{pac.get('n_procesos', '—')} procesos</b>, mayormente por subasta inversa "
            f"electrónica. Aquí el plan se vuelve obra y servicio. Incluye un proceso dedicado "
            f"a la atención de grupos prioritarios —la huella social del plan."),
            unsafe_allow_html=True)
    st.markdown(_div(), unsafe_allow_html=True)

    # ④ LA COHERENCIA — diagrama de cruce + señales + texto
    sat = plan.get("sat0", {}) or {}
    st.markdown(_head("④", "LA COHERENCIA", "el cruce de los productos · ¿el plan y el gasto coinciden?"),
                unsafe_allow_html=True)
    st.markdown(_cruce(plan), unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.1], gap="medium")
    with c1:
        st.markdown(_pills(sat.get("componentes", [])), unsafe_allow_html=True)
    with c2:
        st.markdown(_narr(
            "El diagrama recorre el cruce de la cadena: del plan al recurso. La señal "
            "preventiva marca hoy <b>revisar la alineación POA-PAC</b> —hay procesos bajo el "
            "monto mínimo y la brecha aún no consolida dato. No es una falta: es el punto "
            "exacto para cerrar la coherencia <b>antes</b> de ejecutar."), unsafe_allow_html=True)


def _peritaje_viz(sat_temp: str) -> None:
    st.markdown(_css(), unsafe_allow_html=True)
    st.markdown(_stepper(sat_temp), unsafe_allow_html=True)
    st.markdown('<div style="font-size:10.5px;color:#5A6B7E;margin-top:2px">'
                'La cadena es sólida hasta la operación; el foco preventivo está en la '
                'coherencia hacia la ejecución.</div>', unsafe_allow_html=True)


def _conclusion_viz(pct: int, color: str) -> None:
    _show(_gauge(pct, color), 175)


def render() -> None:
    """QINV-001 · Planificación Estratégica — vista BI, evidencia nativa."""
    d = _cargar()
    fid = d.get("fidelidad_plan")
    plan = d.get("plan") or {}
    sat_temp = (plan.get("sat0", {}) or {}).get("global_temp", "alerta")
    tiene = isinstance(fid, (int, float))
    dato_str = f"{fid:.1f}%" if tiene else "—"

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
        headline = ("El plan conserva la correspondencia con su senda; el foco "
                    "preventivo está en sostenerla en la ejecución.")
        peritaje = [
            f"La planificación mantiene una correspondencia del {dato_str} con las metas "
            "plurianuales —el diseño del plan está esencialmente a la altura de su objetivo a 2027.",
            "La evidencia recorre la cadena completa: del plan a quién lo ejecuta, a con qué "
            "se compra, y a la coherencia entre todo.",
            "La distancia que importa no está en el diseño, sino en sostener la traducción a "
            "ejecución —ahí se abren las desviaciones, y ahí va la atención hoy.",
        ]
        conclusion = (
            "El Plan de Desarrollo mantiene su senda en el diseño plurianual. La señal es "
            "preventiva: vigilar que la operación (POA) y la contratación (PAC) sigan el ritmo "
            "del plan, para que la correspondencia no se erosione en la ejecución."
        )
        per_viz = lambda: _peritaje_viz(sat_temp)
        con_viz = lambda: _conclusion_viz(vpct, _T.get(temp, "#00D4FF"))

    inv = InvestigacionQUIRA(
        id="QINV-001", dominio="d01", nombre="Planificación Estratégica", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=dato_str, temp=temp,
        hipotesis=("La fidelidad estratégica se mide por la correspondencia sostenida entre "
                   "el plan plurianual y su ejecución a lo largo de la cadena."),
        evidencia=lambda: _evidencia(d),
        peritaje_headline=headline,
        peritaje=peritaje,
        peritaje_viz=per_viz,
        veredicto_label="Correspondencia con el Plan",
        veredicto_pct=vpct,
        divergencias="",
        prioridad="Foco · ejecución de la cadena del plan",
        prioridad_temp=prioridad_temp,
        conclusion=conclusion,
        conclusion_viz=con_viz,
    )
    inv.to_streamlit()
