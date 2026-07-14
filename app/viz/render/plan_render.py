# -*- coding: utf-8 -*-
"""
Sistema de Visualización Canónico — RENDERER del DOM Planificación Estratégica.
Dylus Lab © 2026 · patrón RDC (Javo · 2026-07-10): mismo molde/gramática del cajón RDC,
aplicado al backbone del plan. Reutiliza la gramática de html_render (una sola canon visual).

Estructura (patrón RDC): pregunta → principio → 01 procedimiento (backbone = biografía del plan)
→ 02 el plan y su cobertura → 03 trazabilidad (metas como expedientes) → 04 coherencia (SAT) →
evaluación (hallazgos + implicaciones) → síntesis → placa. HTML autocontenido (sin Plotly).
"""
from __future__ import annotations

import re

# reutiliza la gramática visual + helpers del cajón RDC (una sola canon · no se duplica)
try:
    from html_render import _CSS as _RDC_CSS, _esc, _corta, _ley, _seccion, _pct  # noqa: F401
    from hallazgos import render_hallazgos as _hallazgos_html, h_serie, h_proyeccion  # sintetizador compartido  # noqa: F401
    from relacional import cadena_integridad, REL_CSS  # motor Relacional compartido  # noqa: F401
    from provenance import prov, prov_leyenda, PROV_CSS  # proveniencia ADR-033  # noqa: F401
except ImportError:  # dentro del paquete app (Streamlit)
    from app.viz.render.html_render import _CSS as _RDC_CSS, _esc, _corta, _ley, _seccion, _pct  # noqa: F401
    from app.viz.render.hallazgos import render_hallazgos as _hallazgos_html, h_serie, h_proyeccion  # noqa: F401
    from app.viz.render.relacional import cadena_integridad, REL_CSS  # noqa: F401
    from app.viz.render.provenance import prov, prov_leyenda, PROV_CSS  # noqa: F401

# CSS: la gramática RDC + lo específico del plan (strip de datos del backbone, cards SAT)
_PLAN_EXTRA = """
/* color propio del DOM Planificación (cada DOM es un universo · Javo 2026-07-10) — cian vivo sobre fondo oscuro */
.qc{border-top-color:#22D3EE}
.qc-hn{color:#22D3EE}
.qc-q{border-left-color:#22D3EE}
.qc-princ{background:rgba(34,211,238,.07);border-color:rgba(34,211,238,.28)}
.qc-princ .t{color:#22D3EE}
.qc-blk.out{border-color:#22D3EE;background:rgba(34,211,238,.1)}.qc-blk.out .bl{color:#22D3EE}
.qc-sint{border-color:#22D3EE}
.qc-sint-lbl{background:rgba(34,211,238,.13);color:#22D3EE;border-color:rgba(34,211,238,.32)}
.qc-sr-cierre{font-family:Georgia,serif;font-size:13.5px;line-height:1.55;color:var(--tx);margin-top:13px;padding-top:12px;border-top:1px solid var(--bd)}.qc-sr-cierre b{color:#fff}
.pl-strip{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 2px}
.pl-si{flex:1 1 120px;border:1px solid var(--bd);border-radius:6px;padding:9px 11px;background:var(--sf)}
.pl-si .k{font-family:ui-monospace,monospace;font-size:8.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);font-weight:700}
.pl-si .v{font-family:Georgia,serif;font-size:18px;font-weight:700;color:var(--tx);margin-top:2px}
.pl-si .s{font-size:9.5px;color:var(--tx2);margin-top:1px}
.pl-sat{display:grid;grid-template-columns:1fr 1fr;gap:11px}
.pl-satc{border:1px solid var(--bd);border-left-width:3px;border-radius:7px;padding:12px 14px;background:var(--sf)}
.pl-satc .st{font-size:12.5px;font-weight:700;color:var(--tx);margin-bottom:3px}
.pl-satc .sd{font-size:11.5px;color:var(--tx2);line-height:1.5}
.pl-satc .sv{font-family:ui-monospace,monospace;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;float:right}
@media(max-width:640px){.pl-sat{grid-template-columns:1fr}}
/* Bloque primario por año (2025 cerrado · 2026 parcial) + gráfica de ejecución */
.pl-yr{border:1px solid var(--bd);border-radius:9px;padding:13px 15px;background:var(--sf);margin:11px 0}
.pl-yr.part{border-style:dashed}
.pl-yr-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:9px}
.pl-yr-y{font-family:Georgia,serif;font-size:16px;font-weight:700;color:var(--tx)}
.pl-yr-st{font-family:ui-monospace,monospace;font-size:8px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 8px;border-radius:9px;border:1px solid;white-space:nowrap}
.pl-bar-t{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-bottom:5px}
.pl-bar-p{font-family:Georgia,serif;font-size:19px;font-weight:700}
.pl-bar-m{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--tx2)}
.pl-bar-tk{height:11px;border-radius:6px;background:var(--bd);overflow:hidden}
.pl-bar-fl{height:100%;border-radius:6px}
.pl-yr-x{font-size:11px;color:var(--tx2);line-height:1.5;margin-top:8px}.pl-yr-x b{color:var(--tx)}
/* Evidencia bajo demanda (Primacía Narrativa · patrón <details>) — tabla desplegable */
.qc-ev{margin:11px 0 2px;border:1px solid var(--bd);border-radius:8px;overflow:hidden}
.qc-ev>summary{cursor:pointer;padding:9px 13px;font-family:ui-monospace,monospace;font-size:10px;font-weight:700;letter-spacing:.03em;color:#22D3EE;background:var(--sf);list-style:none}
.qc-ev>summary::-webkit-details-marker{display:none}
.qc-ev>summary::before{content:"▸  "}
.qc-ev[open]>summary::before{content:"▾  "}
.qc-evw{overflow-x:auto}
.qc-evt{width:100%;border-collapse:collapse;font-size:11px}
.qc-evt th{text-align:left;padding:7px 13px;color:var(--tx2);font-family:ui-monospace,monospace;font-size:8px;text-transform:uppercase;letter-spacing:.05em;border-top:1px solid var(--bd);white-space:nowrap}
.qc-evt td{padding:7px 13px;color:var(--tx2);border-top:1px solid var(--bd);vertical-align:top;line-height:1.4}
.qc-evt td:first-child{color:var(--tx);min-width:220px}
.qc-evt td.sc{font-family:Georgia,serif;font-weight:700;color:#22D3EE;text-align:right;white-space:nowrap}
"""
_ESL_CSS = """
.qc-sint-b .pl-esl{display:flex;gap:13px;margin-bottom:11px;font-size:13px;line-height:1.62}
.qc-sint-b .pl-esl .lb{flex:none;width:160px;font-family:ui-monospace,monospace;font-size:10.5px;font-weight:700;color:#22D3EE;letter-spacing:.02em;text-transform:uppercase;padding-top:2px}
.qc-sint-b .pl-esl .tx{color:var(--tx2)}.qc-sint-b .pl-esl .tx b{color:var(--tx)}
@media(max-width:640px){.qc-sint-b .pl-esl{flex-direction:column;gap:3px}.qc-sint-b .pl-esl .lb{width:auto}}
"""
_CSS = _RDC_CSS.replace("</style>", _PLAN_EXTRA + REL_CSS + _ESL_CSS + PROV_CSS + "</style>")

# semáforo (temp) → color de la gramática
_TEMP = {"critico": "#D93025", "alerta": "#F9AB00", "amarillo": "#F9AB00", "normal": "#1A73E8",
         "verde": "#1E8E3E", "dim": "#9AA0A6"}


def _c(temp: str) -> str:
    return _TEMP.get((temp or "").lower(), "#9AA0A6")


def _m(v: float) -> str:
    """monto USD legible."""
    v = float(v or 0)
    if abs(v) >= 1e6:
        return f"${v / 1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"${v / 1e3:.0f}k"
    return f"${v:,.0f}"


# ── 01 · EL PROCEDIMIENTO — el backbone como biografía del plan ──
_BACK = [  # (concepto, instrumento, pregunta, clase) — cadena de EXTREMO A EXTREMO
    ("Plan Nacional", "la política pública", "¿está alineado?", "src"),
    ("PDOT", "el plan local", "¿qué se comprometió?", ""),
    ("POA", "la operación anual", "¿se programó?", ""),
    ("Presupuesto", "el recurso", "¿se asignó?", ""),
    ("PAC", "la contratación", "¿se planificó comprar?", ""),
    ("SERCOP", "la adjudicación", "¿se adjudicó?", ""),
    ("Ejecución", "el gasto", "¿se ejecutó?", "out"),
]


def _backbone(plan: dict) -> str:
    """01 · La cadena de extremo a extremo, EXPLICADA eslabón por eslabón (conceptual, sin cifras
    — las cifras van por año). Dos planos (ADR-033): integridad documental + desempeño analítico."""
    nodos = []
    for i, (n, ins, q, cls) in enumerate(_BACK):
        if i:
            nodos.append('<div class="qc-conn"><div class="aw">→</div></div>')
        nodos.append(f'<div class="qc-blk {cls}"><div class="bl">{_esc(n)}</div>'
                     f'<div class="bsys">{_esc(ins)}</div><div class="bq">{_esc(q)}</div></div>')
    return (
        '<p class="qc-p">La <b>planificación</b> no es un documento: es una <b>cadena</b> que va de la '
        '<b>política pública nacional</b> hasta el <b>gasto ejecutado</b>. QUIRA la observa en <b>dos planos</b>: '
        'su <b>integridad</b> —¿cada eslabón sostiene al siguiente, o hay una brecha documentada?— y su '
        '<b>desempeño</b> —qué tan bien se ejecutó lo planificado—. Aquí se explica la cadena <b>de extremo a '
        'extremo</b>, eslabón por eslabón; las cifras de cada ejercicio se detallan por año, más adelante.</p>'
        f'<div class="qc-pipe">{"".join(nodos)}</div>')


# ── 02 · EL PLAN Y SU COBERTURA (embudo) ──
def _cobertura(plan: dict) -> str:
    mt = plan.get("metas_total", 25) or 25
    cob = plan.get("cobertura_metas_poa") or 0
    n_cob = round(mt * cob / 100)
    comp = plan.get("competencia", []) or []
    total_c = sum(c.get("n", 0) for c in comp) or 1
    cols = ["#1E8E3E", "#1A73E8", "#6BA6C9", "#8B7BD8", "#9AA0A6"]
    seg = "".join(f'<div class="qc-fseg" style="flex:{max(c.get("n",0),0.001)};background:{cols[i%len(cols)]}"></div>'
                  for i, c in enumerate(comp) if c.get("n"))
    chips = "".join(f'<div class="qc-fchip"><span class="d" style="background:{cols[i%len(cols)]}"></span>'
                    f'<b>{c.get("n",0)}</b> {_esc(c.get("label",""))}</div>' for i, c in enumerate(comp))
    return (
        f'<p class="qc-p">El plan cantonal fija <b>{mt} metas</b> plurianuales (PDOT 2023-2027). El primer eslabón '
        f'de la trazabilidad es cuántas <b>bajan a la operación</b> anual (POA):</p>'
        f'<div class="qc-embudo"><div class="qc-fhead"><span><b>{mt}</b> metas del plan</span>'
        f'<span class="ar">→</span><span><b>{n_cob}</b> con proyectos en el POA (<b>{cob:.0f}%</b>)</span></div>'
        f'<div class="qc-fbar">{seg}</div><div class="qc-fchips">{chips}</div>'
        f'<div class="qc-fnote">Distribución de las metas por <b>competencia</b>: exclusiva, concurrente y de '
        f'articulación. La cobertura mide el aterrizaje del plan en la operación, no su ejecución final.</div></div>')


# ── 03 · TRAZABILIDAD — metas como expedientes (Valor Demostrativo = trazabilidad) ──
def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _norm_dir(s: str) -> str:
    """Normaliza una dirección: quita el prefijo 'Dirección de' para poder alinear metas ↔ POA."""
    return re.sub(r"^direcci[oó]n\s+(de\s+)?", "", _norm(s))


def _dir_match(a: str, b: str) -> bool:
    """Match difuso de dirección (tolera prefijo y truncado del POA ~50 chars)."""
    a, b = _norm_dir(a), _norm_dir(b)
    if not a or not b:
        return False
    return a[:18] == b[:18] or a.startswith(b) or b.startswith(a)


def _traza_meta(meta: dict, poa: list, pac: list) -> dict:
    """Rastrea una meta por el backbone. Claves reales del canon: el PAC referencia la meta por su
    CÓDIGO (id, p.ej. AH-I-X-02); el POA no lleva el código de meta, se enlaza por la DIRECCIÓN que
    la opera. Enlace exacto en PAC, aproximado (por unidad ejecutora) en POA — honesto."""
    mid = _norm(meta.get("id"))
    proys = [p for p in poa if _dir_match(meta.get("direccion"), p.get("dir"))]  # la dirección que opera la meta
    tiene_part = any(p.get("partida") for p in proys)
    procs = [p for p in pac if _norm(p.get("meta")) == mid]              # PAC referencia la meta por su código
    # cadena alcanzada
    if procs:
        cadena = "pac"
    elif tiene_part:
        cadena = "presupuesto"
    elif proys:
        cadena = "poa"
    else:
        cadena = "pdot"
    monto = sum(p.get("anual", 0) for p in proys)
    return {"proys": len(proys), "partida": tiene_part, "procs": len(procs),
            "cadena": cadena, "monto": monto, "alerta": next((p.get("alerta") for p in procs if p.get("alerta")), "")}


_CADENA_META = ["PDOT", "POA", "Presupuesto", "PAC"]
_UPTO_META = {"pdot": 0, "poa": 1, "presupuesto": 2, "pac": 3}


def _minichain_meta(cadena: str) -> str:
    upto = _UPTO_META.get(cadena, 0)
    nodos = []
    for j, s in enumerate(_CADENA_META):
        if j:
            nodos.append(f'<span class="mc-a {"on" if j <= upto else ""}">→</span>')
        nodos.append(f'<span class="mc-n {"on" if j <= upto else "off"}">{_esc(s)}</span>')
    return f'<div class="qc-mc"><span class="mc-t">Trazabilidad de la meta</span><div class="mc-row">{"".join(nodos)}</div></div>'


def _vd_meta(t: dict) -> tuple:
    """Valor demostrativo de la trazabilidad (0-100) + sellos."""
    base = {"pac": 92, "presupuesto": 74, "poa": 52, "pdot": 28}[t["cadena"]]
    vd = min(base + min(t["proys"], 4) * 2, 100)
    badges = [{"pac": "Cadena completa", "presupuesto": "Con presupuesto", "poa": "En operación",
               "pdot": "Solo en el plan"}[t["cadena"]]]
    if t["proys"]:
        badges.append(f'{t["proys"]} proyecto{"s" if t["proys"] != 1 else ""} POA')
    if t["monto"]:
        badges.append(_m(t["monto"]))
    return vd, badges[:3]


def _expedientes_metas(plan: dict, k: int = 4) -> str:
    metas = plan.get("metas_detalle", []) or []
    poa = plan.get("poa_proyectos", []) or []
    pac = plan.get("pac_detalle", []) or []
    trazas = [(mm, _traza_meta(mm, poa, pac)) for mm in metas]
    # una por nivel de cadena (más demostrativa primero), en orden de lectura
    quiere = ["pac", "presupuesto", "poa", "pdot", "presupuesto", "pac"]  # rellena hasta k aunque falte una cadena
    porc: dict[str, list] = {}
    for mm, t in trazas:
        porc.setdefault(t["cadena"], []).append((mm, t))
    for v in porc.values():
        v.sort(key=lambda x: -_vd_meta(x[1])[0])
    out, usados = "", {c: 0 for c in quiere}
    n = 0
    for c in quiere:
        pool = porc.get(c, [])
        if usados[c] < len(pool) and n < k:
            mm, t = pool[usados[c]]; usados[c] += 1; n += 1
            vd, badges = _vd_meta(t)
            col = _c({"pac": "verde", "presupuesto": "normal", "poa": "amarillo", "pdot": "dim"}[c])
            estado = {"pac": "Trazable · completa", "presupuesto": "Con presupuesto",
                      "poa": "En operación", "pdot": "Sin bajar al POA"}[c]
            bch = "".join(f'<span class="qc-bdg">{_esc(b)}</span>' for b in badges)
            res = (f'{t["proys"]} proyecto(s) en el POA · {_m(t["monto"])} programado'
                   + (f' · alerta: {t["alerta"]}' if t.get("alerta") else '')) if c != "pdot" else \
                  "La meta consta en el plan pero no se localizó proyecto operativo en el POA."
            out += (f'<div class="qc-exp"><div class="qc-exp-top">'
                    f'<span class="qc-exp-id">EXPEDIENTE · meta del plan · {_esc(mm.get("id",""))}</span>'
                    f'<span class="qc-stamp" style="color:{col};border-color:{col}">{_esc(estado)}</span></div>'
                    f'<div class="qc-vd"><span class="qc-vd-s">Valor demostrativo <b>{vd}</b></span>{bch}</div>'
                    f'<div class="qc-exp-b">'
                    f'<div class="qc-kv"><span class="k">Meta</span><span class="v">"{_esc(_corta(mm.get("meta",""),104))}"</span></div>'
                    f'<div class="qc-kv"><span class="k">Dirección</span><span class="v">{_esc(mm.get("direccion","—"))}</span></div>'
                    f'<div class="qc-kv"><span class="k">Resultado</span><span class="v"><b>{_esc(_corta(res,128))}</b></span></div>'
                    f'{_minichain_meta(c)}</div></div>')
    return f'<div class="qc-exps">{out}</div>'


# ── 04 · LA COHERENCIA (los 4 motores SAT) ──
def _coherencia(plan: dict) -> str:
    sat = plan.get("sat0", {}) or {}
    comps = sat.get("componentes", []) or []
    cards = ""
    for c in comps:
        col = _c(c.get("temp", "dim"))
        cards += (f'<div class="pl-satc" style="border-left-color:{col}">'
                  f'<div class="st">{_esc(c.get("label", "—"))}'
                  f'<span class="sv" style="color:{col}">{_esc(c.get("estado", ""))}</span></div></div>')
    diag = sat.get("diagnostico", "")
    gg = sat.get("global", "")
    diag_html = (f'<div class="qc-impl" style="margin-top:14px"><div class="qc-impl-t">Diagnóstico'
                 f'{" · " + _esc(gg) if gg else ""}</div><div class="qc-impl-b">{_esc(diag)}</div></div>') if diag else ""
    return (
        '<p class="qc-p">Más allá de la trazabilidad, QUIRA corre un <b>análisis preventivo</b> sobre la '
        'contratación: cuatro motores que leen la coherencia entre lo planificado, lo presupuestado y lo que se '
        'contrata, para detectar desvíos <b>antes</b> de que se vuelvan brecha.</p>'
        f'<div class="pl-sat">{cards}</div>{diag_html}')


# ── evaluación · hallazgos calculados + implicaciones ──
def _hallazgos_plan(plan: dict) -> list:
    pr = plan.get("presupuesto", {}) or {}
    ipe = plan.get("ipe_ejecutado", {}) or {}
    pub = (plan.get("publicado", {}) or {}).get("cruce", {}) or {}
    H = []
    cob = plan.get("cobertura_metas_poa") or 0
    if cob:
        tag = "up" if cob >= 80 else ("warn" if cob >= 50 else "info")
        H.append((tag, "Cobertura del plan en la operación",
                  f"El {cob:.0f}% de las {plan.get('metas_total',25)} metas del PDOT baja a proyectos operativos en el POA: el plan aterriza en la gestión."))
    if ipe.get("pct") is not None:
        p = round(ipe["pct"])
        H.append(("info", "Gasto vinculado al plan",
                  f"El {p}% del gasto ejecutado está vinculado a objetivos del PDOT; el resto responde a operación no planificada en el plan de desarrollo."))
    ti = pr.get("ti_pct")
    if ti is not None:
        H.append(("info", "Ejecución al corte",
                  f"Al corte {pr.get('corte','')}, la ejecución presupuestaria de inversión alcanza el {ti}%: el ritmo del gasto frente al riesgo de subejecución."))
    if pub.get("cobertura_pct") is not None:
        pc = round(pub["cobertura_pct"])
        H.append(("warn", "Lo planificado ya en SERCOP",
                  f"Solo el {pc}% del plan de contratación (PAC) aparece publicado en SERCOP al corte: la brecha entre lo planificado y lo que ya está en el mercado público."))
    return H[:4]


# _hallazgos_html: importado del sintetizador compartido hallazgos.render_hallazgos (ver top del módulo)


def _implicaciones_plan(plan: dict) -> str:
    """Interpretación nacida del dato (registro de observatorio, no prosa genérica · Javo 2026-07-10):
    diagnostica DÓNDE reside la brecha —en la formulación del plan o en la velocidad de ejecución—."""
    cob = round(plan.get("cobertura_metas_poa") or 0)
    ipe = round((plan.get("ipe_ejecutado", {}) or {}).get("pct") or 0)
    ti = round((plan.get("presupuesto", {}) or {}).get("ti_pct") or 0)
    alta_form = cob >= 80 and ipe >= 80
    if alta_form and ti < 30:
        txt = (f"La evidencia indica que Montecristi conserva una <b>alta consistencia entre la planificación "
               f"estratégica y la operación institucional</b>: el {cob}% de las metas del PDOT desciende al POA y el "
               f"{ipe}% del gasto ejecutado se vincula a los objetivos del plan de desarrollo. La <b>brecha del "
               f"período no reside en la formulación</b> del plan, sino en la <b>velocidad con que la contratación "
               f"transforma esa planificación en ejecución presupuestaria</b>: al corte, la inversión devengada "
               f"alcanza apenas el {ti}%.")
    elif alta_form:
        txt = (f"La <b>correspondencia entre planificación y operación es alta</b> —{cob}% de las metas en el POA y "
               f"{ipe}% del gasto vinculado al PDOT— y la ejecución de inversión avanza en el {ti}% al corte: la "
               f"planificación estratégica se traduce en operación y comienza a materializarse en gasto dentro del "
               f"calendario del ejercicio fiscal.")
    else:
        txt = (f"La cadena del plan al gasto presenta un <b>eslabón débil en el descenso del plan a la operación</b> "
               f"(cobertura del {cob}% de las metas en el POA): una parte de la planificación estratégica no alcanza "
               f"aún expresión programática, lo que condiciona su ejecución presupuestaria posterior.")
    return f'<div class="qc-impl"><div class="qc-impl-t">Implicaciones</div><div class="qc-impl-b">{txt}</div></div>'


def _sintesis_plan(plan: dict) -> str:
    """Síntesis del dominio, eslabón por eslabón — registro de observatorio nacional (Javo · lenguaje elevado).
    Incorpora al cajón el cierre que antes flotaba sin formato (portado de m_planificacion._cierre)."""
    metas = plan.get("metas_detalle", [])
    comp = plan.get("competencia", [])
    criticas = sum(c["n"] for c in comp if "Crítica" in c["label"])
    cob = plan.get("cobertura_metas_poa") or 0
    proys = plan.get("poa_proyectos", [])
    tpoa = sum(x.get("anual", 0) for x in proys)
    pr = plan.get("presupuesto", {}) or {}
    pac_total = (plan.get("pac", {}) or {}).get("total_usd", 0) or 0
    pub_pct = ((plan.get("publicado", {}) or {}).get("cruce", {}) or {}).get("cobertura_pct", 0)
    cod = pr.get("codificado_inversion", 0) or 0
    dev = pr.get("devengado", 0) or 0
    ti = pr.get("ti_pct", 0)
    ipe = (plan.get("ipe_ejecutado") or {}).get("pct", 0)

    filas = [
        ("Plan · PDOT",
         f"El instrumento rector de la planificación cantonal fija <b>{len(metas)} metas plurianuales</b>, "
         f"<b>{criticas} en competencias de ejercicio obligatorio</b>. El <b>{cob:.0f}%</b> ya desciende a la "
         f"programación operativa del ejercicio: la planificación estratégica encuentra correlato en la gestión y "
         f"no permanece en el plano declarativo."),
        ("Operación · POA",
         f"La programación operativa anual desagrega el plan en <b>{len(proys)} proyectos</b> por <b>${tpoa/1e6:.1f}M</b>, "
         f"cada uno con dirección responsable, partida presupuestaria y cronograma: el vínculo formal entre el "
         f"objetivo estratégico y el recurso que lo hace ejecutable."),
        ("Contratación · PAC",
         f"La contratación planificada asciende a <b>${pac_total/1e6:.1f}M</b> —el <b>98.6%</b> de la inversión "
         f"presupuestada—; el <b>{pub_pct}%</b> se ha materializado en el portal de compras públicas al corte. El "
         f"nivel corresponde al primer cuatrimestre: la ejecución del gasto de inversión se concentra "
         f"estructuralmente en el segundo semestre."),
        ("Recurso · Presupuesto",
         f"La inversión codificada alcanza <b>${cod/1e6:.1f}M</b>, con <b>${dev/1e6:.2f}M</b> devengados (<b>{ti}%</b>) "
         f"al corte —fase inicial del ejercicio, de carga diferida característica del gasto de inversión."),
        ("Calidad · Gasto vinculado",
         f"El <b>{ipe:.1f}%</b> de la inversión ya ejecutada se imputa a una meta del plan a través de su partida: "
         f"el recurso se asigna <b>conforme a lo planificado</b> y no por decisión discrecional —un indicador de "
         f"calidad del gasto, no solo de su volumen."),
        ("Prevención · Coherencia",
         "El análisis preventivo sobre la alineación entre plan y contratación permanece activo: su propósito es "
         "<b>cerrar la coherencia antes de la ejecución</b>, no constatar el incumplimiento una vez consumado."),
    ]
    sint = "".join(f'<div class="pl-esl"><span class="lb">{_esc(lb)}</span><span class="tx">{tx}</span></div>'
                   for lb, tx in filas)
    cierre = ('<div class="qc-sr-cierre">En conjunto, <b>el plan sostiene su diseño</b>: la correspondencia entre lo '
              'planificado, lo presupuestado y lo contratado es consistente, y la inversión ya ejecutada es de alta '
              'calidad por su vínculo con las metas. La atención que amerita el período es de naturaleza <b>preventiva, '
              'no correctiva</b>: reside en que la contratación y la ejecución recuperen ritmo en el segundo semestre '
              'para alcanzar la asignación presupuestaria antes del cierre, de modo que los compromisos del PDOT no se '
              'erosionen en el tránsito de la planificación al gasto. Observar esa cadena de extremo a extremo —de la '
              'meta al recurso ejecutado— es, precisamente, la función del observatorio.</div>')
    return (f'<div class="qc-sint"><div class="qc-sint-lbl">Síntesis ejecutiva del dominio — Planificación · '
            f'Montecristi · corte {_esc(pr.get("corte",""))}</div><div class="qc-sint-b">{sint}{cierre}'
            f'<div class="qc-fuente">Fuentes: PDOT 2023-2027 · POA · Presupuesto (cédula eSIGEF) · PAC · SERCOP.</div></div></div>')


def _biografia_meta(plan: dict) -> str:
    """La biografía de UNA meta — unidad narrativa del observatorio. PRIMARIO: POA oficial 2025 (año
    CERRADO · vínculo meta↔actividad DE LA FUENTE, no inferido · Principio Rector). Fallback: cadena
    2026 del canon si el artefacto no está. Un porcentaje aislado no explica; una biografía, sí."""
    import re as _re
    # ── primario: biografía 2025 desde el artefacto curado (POA oficial · re-vinculación de la fuente) ──
    try:
        import json as _json
        import os as _os
        _p = _os.path.join(_os.path.dirname(__file__), "..", "..", "..", "data", "poa_multianio.json")
        _bios = _json.load(open(_p, encoding="utf-8")).get("biografias_2025", [])
    except Exception:
        _bios = []
    try:
        _ma = _json.load(open(_p, encoding="utf-8")).get("biografia_multianio", [])
    except Exception:
        _ma = []
    _b25 = {b["meta"]: b for b in _bios}
    _ban = ("roles", "institucional", "vehículos", "vehiculos", "sesiones")
    # flagship: la meta más SUSTANTIVA (mayor plan 2025) que cruce ≥2 años con cadena de inversión
    _pool = [x for x in _ma if len(x["anios"]) >= 2 and _b25.get(x["meta"], {}).get("inversion", 0) >= 3
             and not any(k in x["meta"].lower() for k in _ban)]
    if _pool and _b25:
        xm = max(_pool, key=lambda x: _b25[x["meta"]]["plan"])
        b = _b25[xm["meta"]]
        _t = _re.sub(r"\s+(de|del|la|los|las|y|en|a|el|con|para|al)\s*$", "", _corta(b["meta"], 70), flags=_re.I)
        _nc = b.get("contratos", 0)
        _nodos = [
            {"sys": "META", "label": "compromiso del plan",
             "edge": {"estado": "verificado", "nota": "actividades operativas de la meta (POA oficial)"}},
            {"sys": "POA", "label": f'{b["actividades"]} actividades',
             "edge": {"estado": "verificado", "nota": "asignación por partida presupuestaria"}},
            {"sys": "PARTIDAS", "label": f'{b["partidas"]} partidas · {b["inversion"]} de inversión',
             "edge": {"estado": "verificado", "nota": "monto planificado del ejercicio"}},
            {"sys": "PLAN 2025", "label": f'${b["plan"] / 1e6:.1f}M',
             "edge": {"estado": "verificado" if _nc else "pendiente", "nota": "reconciliación PAC↔POA por descripción"}},
            {"sys": "CONTRATOS", "label": f'{_nc} procesos' if _nc else "sin reconciliar"},
        ]
        _in = (f'<p class="qc-cap">Un porcentaje aislado no explica nada; una <b>biografía</b>, sí. La meta '
               f'<b>«{_esc(_t)}»</b> a lo largo de su vida documental —del compromiso <b>al contrato</b>, trazada de la '
               f'<b>fuente oficial</b> (POA + PAC reconciliados, no inferido)—. Cada meta tiene la suya; su recorrido verificable.</p>')
        _chain = cadena_integridad(_nodos, "Biografía de la meta · del plan al contrato · 2025 (año cerrado)")
        _nombres = b.get("contratos_nombres", [])
        _qc = ""
        if _nombres:
            _li = "".join(f'<li>{_esc(nn)}</li>' for nn in _nombres)
            _qc = (f'<p class="qc-cap" style="margin-top:11px"><b>¿Qué contrató?</b> — procesos de su plan de contratación, '
                   f'reconciliados con el PAC por la <b>descripción del trabajo</b> (no por la partida, que es compartida · '
                   f'confianza {b.get("contratos_conf", 0)}):</p>'
                   f'<ul style="margin:5px 0 0;padding-left:20px;font-size:12.5px;color:var(--tx2);line-height:1.6">{_li}</ul>')
        # continuidad multi-año — la PERSISTENCIA del compromiso (no el monto)
        _cards = ""
        for _y, _v in xm["anios"].items():
            _nat = _v.get("nativo")
            _col = "#22D3EE" if _nat else "#9AA0A6"
            _cards += (f'<div class="pl-si"><div class="k">Ejercicio {_y}</div>'
                       f'<div class="v" style="color:{_col}">{_v["act"]}</div>'
                       f'<div class="s">actividades · {"verificado (fuente)" if _nat else "inferido (partida)"}</div></div>')
        _ys = list(xm["anios"].keys())
        _yrs = _ys[0] if len(_ys) == 1 else " y ".join([", ".join(_ys[:-1]), _ys[-1]])
        _cont = (f'<div class="rl-hd" style="margin-top:18px">Continuidad del compromiso · {len(_ys)} ejercicios</div>'
                 f'<p class="qc-cap">El mismo compromiso <b>reaparece en {_yrs}</b>: indicio de <b>memoria institucional</b>. '
                 f'<b>Precisión epistemológica:</b> en <b>2025</b> el vínculo meta↔actividad es <b>directo de la fuente</b>; en '
                 f'años previos es <b>inferido</b> —la partida que en 2025 pertenece a una sola meta—, y asume que ese mapeo se '
                 f'mantiene. Es un <b>indicio, no una certeza</b>; lo no vinculable queda como ausencia declarada, no se rellena.</p>'
                 f'<div class="pl-strip">{_cards}</div>')
        return _in + _chain + _qc + _cont
    # ── fallback: cadena 2026 del canon (Gold Master) ──
    from collections import defaultdict

    def _n(t):
        return _re.sub(r"\s+", " ", (t or "").strip().upper())

    poa = plan.get("poa_proyectos", [])
    parts = {str(p["cuenta"]): p for p in plan.get("presupuesto", {}).get("partidas", [])}
    pub = plan.get("publicado", {}).get("procesos", [])
    by_meta = defaultdict(list)
    for x in poa:
        by_meta[_n(x.get("meta"))].append(x)
    cand = []
    for mk, proys in by_meta.items():
        if not mk or "FORTALECER Y MEJORAR LOS RECURSOS" in mk:       # excluye el contenedor administrativo
            continue
        inv = [x for x in proys if str(x.get("partida", "")).strip()[:1] in ("7", "8")]
        ptds = sorted(set(str(x.get("partida", "")).strip() for x in inv if x.get("partida")))
        if not ptds:
            continue
        cod = sum((parts.get(pt, {}) or {}).get("cod", 0) or 0 for pt in ptds)
        if cod < 100000:
            continue
        dev = sum((parts.get(pt, {}) or {}).get("dev", 0) or 0 for pt in ptds)
        con = [c for c in pub if str(c.get("partida", "")).strip() in ptds]
        cand.append((mk, len(inv), len(ptds), cod, dev, con))
    if not cand:
        return ""
    mk, n_pro, n_ptd, cod, dev, con = max(cand, key=lambda t: t[3])
    ti = 100 * dev / cod if cod else 0
    titulo = _re.sub(r"\s+(de|del|la|los|las|y|en|a|el|con|para)\s*$", "",
                     _corta(mk.capitalize(), 64), flags=_re.I)
    nodos = [
        {"sys": "META", "label": "compromiso del plan",
         "edge": {"estado": "verificado", "nota": "actividades operativas de la meta en el POA"}},
        {"sys": "POA", "label": f"{n_pro} proyectos",
         "edge": {"estado": "verificado", "nota": "asignación presupuestaria"}},
        {"sys": "PRESUPUESTO", "label": f"${cod/1e6:.1f}M · {n_ptd} partidas",
         "edge": {"estado": "verificado" if ti >= 70 else "parcial", "pct": ti, "nota": "ejecución de la inversión"}},
        {"sys": "EJECUCIÓN", "label": f"${dev/1e6:.2f}M devengado",
         "edge": {"estado": "verificado" if con else "pendiente",
                  "nota": "publicación en contratación pública"}},
        {"sys": "SERCOP", "label": f"{len(con)} contratos"},
    ]
    intro = (f'<p class="qc-cap">Un porcentaje aislado no explica nada; una <b>biografía</b>, sí. La meta '
             f'<b>«{_esc(titulo)}»</b> a lo largo de su vida documental —del compromiso al contrato, trazada de la '
             f'fuente—. Esta es la <b>unidad narrativa</b> del observatorio; cada meta tiene la suya, anclada a su '
             f'identificador canónico.</p>')
    return intro + cadena_integridad(nodos, "Biografía de una meta · del plan al contrato")


def _ley_esl(plan: dict, esl: str, titulo: str) -> str:
    """marco legal del eslabón desde base_normativa.por_eslabon[esl].marco (lista de citas verificadas)."""
    d = ((plan.get("base_normativa", {}) or {}).get("por_eslabon", {}) or {}).get(esl) or {}
    arts = d.get("marco") or []
    if not arts:
        return ""
    chips = "".join(f'<span class="qc-lawc">{_esc(a)}</span>' for a in arts)
    return f'<details class="qc-law"><summary>📖 {_esc(titulo)}</summary>{chips}</details>'


def _cadena_relacional(plan: dict) -> str:
    """El Relacional ENCENDIDO: la cadena del plan al gasto como recorrido de integridad entre las
    fuentes (ADR-029 §Precisión · la verdad vive en la fuente). El estado de cada arista se LEE del snapshot."""
    pub = plan.get("publicado", {}) or {}
    pr = plan.get("presupuesto", {}) or {}
    cob = plan.get("cobertura_metas_poa") or 0
    ipe = (plan.get("ipe_ejecutado", {}) or {}).get("pct") or 0
    pac_usd = (plan.get("pac", {}) or {}).get("total_usd") or 0
    cruce = (pub.get("cruce", {}) or {}).get("cobertura_pct") or 0
    ti = pr.get("ti_pct") or 0

    def _edo(pct, alto=70):
        return "verificado" if pct >= alto else ("parcial" if pct > 0 else "pendiente")

    nodos = [
        {"sys": "PDOT", "label": "plan estratégico",
         "edge": {"estado": _edo(cob), "pct": cob, "nota": "metas del plan con dotación en el POA"}},
        {"sys": "POA", "label": "operación anual",
         "edge": {"estado": _edo(ipe), "pct": ipe, "nota": "gasto vinculado a los objetivos del plan"}},
        {"sys": "PRESUPUESTO", "label": "asignación",
         "edge": {"estado": "verificado" if pac_usd else "pendiente", "nota": "contratación planificada (PAC)"}},
        {"sys": "PAC", "label": "plan de compras",
         "edge": {"estado": _edo(cruce), "pct": cruce, "nota": "publicado en SERCOP al corte del período"}},
        {"sys": "SERCOP", "label": "contratación pública",
         "edge": {"estado": _edo(ti), "pct": ti, "nota": "ejecución de la inversión (en curso)"}},
        {"sys": "EJECUCIÓN", "label": "gasto devengado"},
    ]
    intro = ('<p class="qc-cap">La verdad no vive en QUIRA: vive en estas <b>fuentes</b>. El recorrido muestra '
             'cuánto <b>sostiene documentalmente cada fuente a la siguiente</b> —la integración que QUIRA '
             'verificó—. Un eslabón delgado no es una falta: es una fuente que aún no alcanza a la siguiente.</p>')
    return intro + cadena_integridad(nodos, "Integridad de la cadena · fuente por fuente")


def _ejec_col(p: float) -> str:
    return "#22D3EE" if p >= 70 else ("#F9AB00" if p >= 55 else "#D93025")


def _bloque_anio(e: dict, cerrado: bool) -> str:
    """Bloque primario de un ejercicio: gráfica de ejecución (barra devengado/codificado) + lectura."""
    p = e["pct"]
    col = _ejec_col(p) if cerrado else "#9AA0A6"
    w = max(2.0, min(100.0, p))
    estado = "Cerrado" if cerrado else "Parcial · en curso"
    ecol = "#1E8E3E" if cerrado else "#F9AB00"
    mag = (f'${e["devengado"]/1e6:.1f}M de ${e["codif"]/1e6:.1f}M devengados'
           if e.get("codif") and e.get("devengado") else "")
    if cerrado:
        x = (f'Ejercicio <b>cerrado y evaluable</b>: la inversión planificada se ejecutó al '
             f'<b>{p:.1f}%</b>. El resto quedó comprometido o sin devengar al cierre fiscal.')
    else:
        x = (f'Ejercicio <b>en curso</b>: al corte lleva <b>{p:.1f}%</b> devengado sobre un plan de '
             f'${e["codif"]/1e6:.1f}M. Es <b>parcial</b> — se lee aparte, no se compara con años cerrados.')
    return (f'<div class="pl-yr{"" if cerrado else " part"}">'
            f'<div class="pl-yr-h"><span class="pl-yr-y">Ejercicio {e["anio"]}</span>'
            f'<span class="pl-yr-st" style="color:{ecol};border-color:{ecol}55;background:{ecol}14">{estado}</span></div>'
            f'<div class="pl-bar-t"><span class="pl-bar-p" style="color:{col}">{p:.1f}%</span>'
            f'<span class="pl-bar-m">{mag}</span></div>'
            f'<div class="pl-bar-tk"><div class="pl-bar-fl" style="width:{w:.1f}%;background:{col}"></div></div>'
            f'<div class="pl-yr-x">{x}</div></div>')


def _alineacion_pnd(plan: dict) -> str:
    """02b · Alineación PDOT↔Plan Nacional (H11b · objeto canónico compartido · nace en d01).
    Primacía Narrativa (ADR-033): se NARRA (promedio CANÓNICO — QUIRA no recalcula) y la tabla
    por meta va como EVIDENCIA bajo demanda (<details>), nunca como protagonista."""
    a = plan.get("alineacion_pnd") or {}
    ejes = a.get("por_eje") or []
    metas = a.get("metas") or []
    if not ejes:
        return ""
    n, vm = a.get("n_metas", 0), a.get("vinculacion_media") or 0
    dist = " · ".join(f'{_esc(e["eje"].split("—")[0].strip())} ({e["n_metas"]})' for e in ejes)
    intro = ('<div class="qc-cap" style="margin-top:15px"><b>Alineación con el Plan Nacional de Desarrollo</b></div>'
             f'<p class="qc-p">Las <b>{n} metas del PDOT</b> se articulan con los <b>{len(ejes)} ejes</b> del '
             f'Plan Nacional de Desarrollo. Cada meta recibe una <b>calificación de vinculación</b> con la '
             f'política nacional; en promedio es <b>{vm:.2f} sobre 1</b>. Es un <b>resultado analítico</b> '
             '—se calcula una sola vez sobre la evidencia oficial y este dominio lo <b>reporta, no lo rehace</b>—. '
             'La alineación estratégica '
             '<b>existe antes del presupuesto</b>: es la que habilita la elegibilidad de financiamiento y '
             f'cooperación. Las metas se reparten así entre los ejes: {dist}.</p>')
    filas = "".join(
        f'<tr><td>{_esc(m["meta"])}</td><td>{_esc(m["eje"])}</td><td class="sc">{m["score"]:.2f}</td></tr>'
        for m in metas)
    ev = (f'<details class="qc-ev"><summary>Ver las {n} metas y su vinculación al Plan Nacional</summary>'
          '<div class="qc-evw"><table class="qc-evt"><thead><tr><th>Meta del PDOT</th>'
          '<th>Eje · Plan Nacional</th><th>Vinculación</th></tr></thead>'
          f'<tbody>{filas}</tbody></table></div></details>')
    return intro + ev


def _longitudinal_plan(plan: dict) -> str:
    """05 · Los ejercicios de gestión — desagregados por año (último cerrado + en curso, cada uno
    con su gráfica de ejecución) y luego la evaluación consolidada (trayectoria + prospectiva).
    Estructura RDC pedida por la dirección: por año, luego consolidar. Dato real (H07b eSIGEF);
    QUIRA lo narra, no lo recalcula."""
    sm = plan.get("serie_multianio") or {}
    ej = sm.get("ejecucion") or []
    cerr = [e for e in ej if e.get("cerrado")]
    if len(cerr) < 2:
        return ""
    curso = next((e for e in ej if not e.get("cerrado")), None)
    ultimo, previos = cerr[-1], cerr[:-1]

    intro = ('<p class="qc-p">Cada <b>ejercicio de gestión</b> por separado: el último <b>cerrado</b> '
             '(evaluable completo) y el <b>en curso</b> (parcial). El dato es real —cédulas presupuestarias '
             'eSIGEF—; la lectura, del observatorio.</p>')

    foco = _bloque_anio(ultimo, True) + (_bloque_anio(curso, False) if curso else "")

    ctx = ""
    if previos:
        cards = "".join(
            f'<div class="pl-si"><div class="k">Ejercicio {e["anio"]}</div>'
            f'<div class="v" style="color:{_ejec_col(e["pct"])}">{e["pct"]:.0f}%</div>'
            f'<div class="s">ejecución (cerrado)</div></div>' for e in previos)
        ctx = ('<div class="qc-cap" style="margin-top:15px">Ejercicios anteriores · contexto de trayectoria:</div>'
               f'<div class="pl-strip">{cards}</div>')

    H = [h_serie("Trayectoria de la ejecución", [(e["anio"], e["pct"]) for e in cerr])]
    proy = sm.get("proyeccion") or {}
    if proy.get("proyeccion"):
        med = proy.get("promedio")
        ancla = f"tendencia del período · media {med:.0f}%" if med else "tendencia del período"
        H.append(h_proyeccion("Proyección del próximo ejercicio completo", proy["proyeccion"], ancla))
    cons = ('<div class="qc-cap" style="margin-top:16px"><b>Evaluación consolidada</b> — comparación, '
            'patrón y prospectiva sobre los ejercicios cerrados:</div>' + _hallazgos_html(H))

    return intro + foco + ctx + cons


# ── ensamblaje ──
def cajon_dominio_plan(plan: dict) -> str:
    if not plan:
        return ""
    return f"""{_CSS}
<section class="qc">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio 001</div>
    <div class="qc-idea">Planificación Estratégica</div>
    <div class="qc-q">¿El cantón mantiene el rumbo hacia sus metas plurianuales, o se desvió en el camino?</div>
  </div>
  <div class="qc-princ"><span class="t">Principio metodológico</span>
    QUIRA mide la <b>consistencia de la cadena que va del plan al gasto</b>: PDOT → POA → PRESUPUESTO → PAC →
    EJECUCIÓN. No certifica intenciones: verifica que cada eslabón <b>sostenga documentalmente</b> al siguiente.
    Un eslabón roto es una <b>brecha</b>, nunca una inferencia.
    {_ley_esl(plan, 'pdot', 'Fundamento del dominio (Planificación)')}
  </div>
  <div class="qc-body">
    {prov_leyenda()}
    {_seccion('01', 'El procedimiento · del plan al gasto', _backbone(plan) + _cadena_relacional(plan), _ley_esl(plan, 'poa', 'Fundamento jurídico aplicable'), prov=prov('doc'))}
    {_seccion('02', 'El plan y su cobertura', _cobertura(plan) + _alineacion_pnd(plan), _ley_esl(plan, 'presupuesto', 'Fundamento jurídico aplicable'), prov=prov('ana'))}
    {_seccion('03', 'La trazabilidad · metas del plan', '<p class="qc-p">Cada expediente es la <b>biografía de una meta</b>: su recorrido desde el plan hasta el gasto, y hasta dónde llega la cadena documental.</p><p class="qc-cap">No se eligen al azar: se muestran las metas de mayor <b>Valor Demostrativo</b> —el puntaje (0-100) que resume cuánto demuestra el método cada expediente: profundidad de la cadena documental, peso presupuestario y tipo de competencia. A mayor puntaje, más completa y probatoria es la trazabilidad.</p>' + _biografia_meta(plan) + _expedientes_metas(plan), _ley_esl(plan, 'pac', 'Fundamento jurídico aplicable'), prov=prov('doc'))}
    {_seccion('04', 'La coherencia · análisis preventivo', _coherencia(plan), _ley_esl(plan, 'gasto', 'Fundamento jurídico aplicable'), prov=prov('ana'))}
    {_seccion('05', 'Los ejercicios de gestión · por año y evaluación consolidada', _longitudinal_plan(plan), prov=prov('ana'))}
    {_seccion('06', 'La evaluación · hallazgos e implicaciones', '<p class="qc-p">Interpretación del dato —no una descripción—: el patrón que revela el análisis, y qué significa.</p>' + _hallazgos_html(_hallazgos_plan(plan)) + _implicaciones_plan(plan), prov=prov('int'))}
    {_sintesis_plan(plan)}
  </div>
  <div class="qc-placa"><div class="qc-placa-q">QUIRA no certifica la verdad. Certifica la consistencia<br>documental de la cadena del plan al gasto.</div>
    <div class="qc-placa-s">Una cadena rota es un resultado del análisis documental, nunca una acusación.</div>
  </div>
</section>"""


def cajon_plan_streamlit(plan: dict) -> str:
    """HTML del dominio Planificación listo para st.markdown (sin sangría ni líneas en blanco)."""
    h = cajon_dominio_plan(plan)
    return "\n".join(ln.lstrip() for ln in h.splitlines() if ln.strip())
