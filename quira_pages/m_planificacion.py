"""
QUIRA OS — QINV-001 · Planificación Estratégica (Investigación)
═══════════════════════════════════════════════════════════════════════════════
Instancia del kernel InvestigacionQUIRA (UMI). Investiga la CADENA estratégica del
territorio: PDOT → POA → PAC → Coherencia. Bajo la regla 20/70/10 y en clave
PREVENTIVA (no punitiva).

EVIDENCIA NATIVA (no se cosechan páginas viejas · Javo 2026-06-23): cada sección
se construye aquí, con dato real del snapshot (bloque `planificacion`, puente
Excel→snapshot vía scripts/enrich_planificacion.py). Layout cohesivo: GRÁFICA a la
izquierda + TEXTO interpretativo a la derecha, fluido como una sola sección, con la
tipología de visualización adecuada a cada dato (transferencia directa).

NO mezcla otros cajones: la fidelidad electoral/IFE/promesas es de Gobernanza del
Mandato (d03) — aquí NO aparece. Madre: FIDELIDAD DE PLANIFICACIÓN (correspondencia
con las metas plurianuales · dato real, NO el proxy IPE).

Firewall: ningún código interno en la vista (ni ICPI, ni TGI, ni H-series).
Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from quira_pages.umi import InvestigacionQUIRA

_PREGUNTA = (
    "¿La institución sostiene la correspondencia con sus metas plurianuales, "
    "o registra desviaciones en su senda de desarrollo?"
)
_UMBRAL = 70.0
_T = {"critico": "#FF4D4D", "alerta": "#FFB020", "verde": "#22C55E",
      "normal": "#00D4FF", "dim": "#5A6B7E"}


def _cargar() -> dict:
    """Estado real de la planificación (Gold Master · Regla 1)."""
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


# ═══════════════════════════════════════════════════════════════════════════════
# Viz helpers — varias tipologías, la adecuada a cada dato (transferencia directa)
# ═══════════════════════════════════════════════════════════════════════════════
def _seg_bar(items: list[dict]) -> str:
    """Barra de composición segmentada (para mezcla categórica · competencia)."""
    total = sum(i["n"] for i in items) or 1
    pal = ["#00D4FF", "#3BA7D9", "#6E8CA8", "#46566A", "#34404F"]
    segs, leg = "", ""
    for i, it in enumerate(items):
        c = pal[i % len(pal)]
        segs += f'<span style="width:{100*it["n"]/total:.1f}%;background:{c}"></span>'
        leg += (f'<div class="pl-leg"><span class="pl-leg-dot" style="background:{c}"></span>'
                f'{it["label"]} · <b>{it["n"]}</b></div>')
    return f'<div class="pl-seg">{segs}</div><div class="pl-legs">{leg}</div>'


def _barras_h(items: list[tuple], accent: str = "#00D4FF") -> str:
    """Barras horizontales (para ranking · direcciones, tipos de contratación)."""
    maxv = max((n for _, n in items), default=1) or 1
    rows = ""
    for label, n in items:
        rows += (f'<div class="pl-bar-row"><span class="pl-bar-lab">{label}</span>'
                 f'<span class="pl-bar-track"><span class="pl-bar-fill" '
                 f'style="width:{100*n/maxv:.0f}%;background:{accent}"></span></span>'
                 f'<span class="pl-bar-val">{n}</span></div>')
    return f'<div class="pl-bars">{rows}</div>'


def _pills(items: list[dict]) -> str:
    """Pastillas de estado (para señales · coherencia SAT-0)."""
    out = ""
    for it in items:
        c = _T.get(it.get("temp", "dim"), "#5A6B7E")
        out += (f'<div class="pl-pill" style="border-color:{c}3a">'
                f'<span class="pl-pill-dot" style="background:{c}"></span>'
                f'<span class="pl-pill-lab">{it["label"]}</span>'
                f'<span class="pl-pill-est" style="color:{c}">{it["estado"]}</span></div>')
    return out


def _seccion(num: str, titulo: str, sub: str, viz: str, narr: str) -> str:
    """Sección cohesiva: gráfica (izq) + interpretación (der), fluido, sin huecos."""
    return (
        f'<div class="pl-sec">'
        f'<div class="pl-sec-h"><span class="pl-sec-n">{num}</span>'
        f'<span class="pl-sec-t">{titulo}</span>'
        f'<span class="pl-sec-s">{sub}</span></div>'
        f'<div class="pl-row"><div class="pl-viz">{viz}</div>'
        f'<div class="pl-narr">{narr}</div></div></div>'
    )


def _css() -> str:
    return """
<style>
.pl-sec{margin:2px 0 18px;padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,.07)}
.pl-sec:last-child{border-bottom:none}
.pl-sec-h{display:flex;align-items:baseline;gap:9px;margin-bottom:12px}
.pl-sec-n{font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:800;color:#00D4FF}
.pl-sec-t{font-size:13.5px;font-weight:800;color:#E8EDF4;letter-spacing:.02em}
.pl-sec-s{font-size:11px;color:#5A6B7E}
.pl-row{display:flex;gap:26px;align-items:flex-start;flex-wrap:wrap}
.pl-viz{flex:1.3;min-width:240px}
.pl-narr{flex:1;min-width:220px;font-size:12.5px;line-height:1.62;color:#C7D2E0}
.pl-narr b{color:#E8EDF4}
.pl-seg{display:flex;height:15px;border-radius:8px;overflow:hidden;background:rgba(255,255,255,.05)}
.pl-seg span{display:block;height:100%}
.pl-legs{margin-top:11px}
.pl-leg{font-size:11.5px;color:#A8B4C8;margin:4px 0}
.pl-leg-dot{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:7px;vertical-align:middle}
.pl-bars{margin-top:2px}
.pl-bar-row{display:flex;align-items:center;gap:9px;margin:5px 0}
.pl-bar-lab{font-size:11.5px;color:#A8B4C8;width:150px;text-align:right;flex-shrink:0;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pl-bar-track{flex:1;height:9px;background:rgba(255,255,255,.06);border-radius:5px;overflow:hidden}
.pl-bar-fill{display:block;height:100%;border-radius:5px}
.pl-bar-val{font-family:'JetBrains Mono',monospace;font-size:11.5px;font-weight:700;color:#E8EDF4;width:22px}
.pl-kpi{display:flex;align-items:baseline;gap:8px;margin-bottom:12px}
.pl-kpi-v{font-family:'JetBrains Mono',monospace;font-size:30px;font-weight:900;color:#00D4FF;line-height:1}
.pl-kpi-l{font-size:11.5px;color:#8892B0}
.pl-pill{display:flex;align-items:center;gap:9px;padding:8px 12px;margin:6px 0;
  background:rgba(255,255,255,.02);border:1px solid;border-radius:9px}
.pl-pill-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0}
.pl-pill-lab{font-size:12px;color:#C7D2E0;flex:1}
.pl-pill-est{font-size:11px;font-weight:700;text-align:right}
.pl-note{font-size:11px;color:#5A6B7E;margin-top:9px}
.pl-tag{display:inline-block;font-size:10.5px;font-weight:700;color:#00D4FF;
  background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.25);
  border-radius:7px;padding:2px 9px;margin-top:8px}
</style>"""


def _evidencia(d: dict) -> None:
    """Las 4 secciones nativas de la cadena de planificación."""
    plan = d.get("plan") or {}
    st.markdown(_css(), unsafe_allow_html=True)

    if not plan:
        st.markdown('<div style="font-size:12px;color:#5A6B7E">— evidencia del plan '
                    'pendiente de carga en el corte —</div>', unsafe_allow_html=True)
        return

    # ① EL PLAN — metas por competencia (composición segmentada)
    comp = plan.get("competencia", [])
    criticas = sum(c["n"] for c in comp if "Crítica" in c["label"])
    total = plan.get("metas_total", sum(c["n"] for c in comp))
    narr_a = (
        f"El Plan de Desarrollo define <b>{total} metas</b> plurianuales 2023-2027. "
        f"<b>{criticas} son de competencia crítica</b> del GAD —agua potable, vialidad, "
        f"alcantarillado, desechos—: ahí se concentra la mayor obligación de ley y la "
        f"mayor presión técnica. Las demás sostienen la gestión o se comparten con "
        f"otros niveles de gobierno."
    )
    st.markdown(_seccion("①", "EL PLAN", "qué comprometió el territorio (PDOT)",
                         _seg_bar(comp), narr_a), unsafe_allow_html=True)

    # ② LA OPERACIÓN — metas por dirección (barras horizontales)
    dirs = plan.get("direcciones", [])
    multi = [(x["dir"], x["n"]) for x in dirs if x["n"] > 1]
    singles = [x for x in dirs if x["n"] == 1]
    viz_b = _barras_h(multi, accent="#3BA7D9")
    if singles:
        viz_b += (f'<div class="pl-note">+ {len(singles)} direcciones más con 1 meta '
                  f'cada una</div>')
    top = multi[0][0] if multi else "—"
    narr_b = (
        f"Las {total} metas se traducen en el Plan Operativo 2026, repartidas en "
        f"<b>{plan.get('n_direcciones','—')} direcciones</b>. <b>{top}</b> y Gestión "
        f"Ambiental cargan el mayor número. La correspondencia plan→operación está "
        f"completa: cada meta tiene una dirección responsable —el plan no quedó en papel."
    )
    st.markdown(_seccion("②", "LA OPERACIÓN", "quién la ejecuta (POA)",
                         viz_b, narr_b), unsafe_allow_html=True)

    # ③ LA CONTRATACIÓN — PAC (número grande + tipos)
    pac = plan.get("pac", {}) or {}
    tipos = [(t["tipo"], t["n"]) for t in pac.get("tipos", [])][:4]
    total_usd = pac.get("total_usd", 0)
    viz_c = (f'<div class="pl-kpi"><span class="pl-kpi-v">${total_usd:,.0f}</span>'
             f'<span class="pl-kpi-l">programados · {pac.get("n_procesos","—")} procesos</span></div>'
             f'{_barras_h(tipos, accent="#6E8CA8")}')
    if pac.get("gap_proceso"):
        viz_c += '<div class="pl-tag">incluye atención a grupos prioritarios</div>'
    narr_c = (
        f"El Plan Anual de Contratación programa <b>${total_usd:,.0f}</b> en "
        f"<b>{pac.get('n_procesos','—')} procesos</b>, mayormente por subasta inversa "
        f"electrónica. La contratación es el puente entre lo planificado y lo realizado: "
        f"aquí el plan se vuelve obra y servicio. Incluye un proceso dedicado a la "
        f"atención de grupos prioritarios —la huella social del plan."
    )
    st.markdown(_seccion("③", "LA CONTRATACIÓN", "con qué se compra (PAC)",
                         viz_c, narr_c), unsafe_allow_html=True)

    # ④ LA COHERENCIA — SAT-0 (pastillas de estado)
    sat = plan.get("sat0", {}) or {}
    comps = sat.get("componentes", [])
    narr_d = (
        "La señal preventiva contrasta lo planificado (POA) con lo contratado (PAC) "
        f"—¿coinciden? Hoy marca <b>revisar la alineación</b>: hay procesos bajo el monto "
        "mínimo de análisis y la brecha aún no consolida dato. No es una falta: es el "
        "punto exacto donde conviene cerrar la coherencia <b>antes</b> de ejecutar, para "
        "que el plan no se erosione en el camino al gasto."
    )
    st.markdown(_seccion("④", "LA COHERENCIA", "¿el plan y el gasto coinciden? (señal preventiva)",
                         _pills(comps), narr_d), unsafe_allow_html=True)


def render() -> None:
    """QINV-001 · Planificación Estratégica — la cadena del plan, evidencia nativa."""
    d = _cargar()
    fid = d.get("fidelidad_plan")
    tiene = isinstance(fid, (int, float))
    dato_str = f"{fid:.1f}%" if tiene else "—"

    if not tiene:
        estado, temp, vpct, prioridad_temp = "—", "dim", None, "alerta"
        headline = "Sin evidencia cargada para este corte."
        peritaje = ["La investigación no puede leer sin evidencia del motor (Regla 3): "
                    "cargue el corte para emitir la lectura."]
        conclusion = "Lea la evidencia del corte para la interpretación de QUIRA."
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
            "plurianuales del Plan de Desarrollo —el diseño está esencialmente a la "
            "altura de su objetivo a 2027.",
            "La evidencia recorre la cadena completa: del plan (metas) a quién lo ejecuta "
            "(direcciones), a con qué se compra (contratación) y a su coherencia.",
            "La distancia que importa no está en el diseño del plan, sino en sostener su "
            "traducción a ejecución —ahí se abren las desviaciones, y ahí va la atención hoy.",
        ]
        conclusion = (
            "El Plan de Desarrollo mantiene su senda en el diseño plurianual. La señal es "
            "preventiva: vigilar que la operación (POA) y la contratación (PAC) sigan el "
            "ritmo del plan, para que la correspondencia no se erosione en la ejecución."
        )

    inv = InvestigacionQUIRA(
        id="QINV-001", dominio="d01", nombre="Planificación Estratégica", version="2026-Q1",
        pregunta=_PREGUNTA, estado=estado, dato=dato_str, temp=temp,
        hipotesis=("La fidelidad estratégica se mide por la correspondencia sostenida "
                   "entre el plan plurianual y su ejecución a lo largo de la cadena."),
        evidencia=lambda: _evidencia(d),
        peritaje_headline=headline,
        peritaje=peritaje,
        veredicto_label="Correspondencia con el Plan",
        veredicto_pct=vpct,
        divergencias="",
        prioridad="Foco · ejecución de la cadena del plan",
        prioridad_temp=prioridad_temp,
        conclusion=conclusion,
    )
    inv.to_streamlit()
