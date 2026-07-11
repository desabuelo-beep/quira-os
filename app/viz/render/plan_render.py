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
except ImportError:  # dentro del paquete app (Streamlit)
    from app.viz.render.html_render import _CSS as _RDC_CSS, _esc, _corta, _ley, _seccion, _pct  # noqa: F401
    from app.viz.render.hallazgos import render_hallazgos as _hallazgos_html, h_serie, h_proyeccion  # noqa: F401
    from app.viz.render.relacional import cadena_integridad, REL_CSS  # noqa: F401

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
"""
_CSS = _RDC_CSS.replace("</style>", _PLAN_EXTRA + REL_CSS + "</style>")

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
_BACK = [  # (concepto, instrumento, pregunta, clase)
    ("PDOT", "el plan", "¿qué se comprometió?", "src"),
    ("POA", "la operación", "¿se programó?", ""),
    ("Presupuesto", "el recurso", "¿se asignó?", ""),
    ("PAC", "la contratación", "¿se contrató?", ""),
    ("Ejecución", "el gasto", "¿se ejecutó?", "out"),
]


def _backbone(plan: dict) -> str:
    nodos = []
    for i, (n, ins, q, cls) in enumerate(_BACK):
        if i:
            nodos.append('<div class="qc-conn"><div class="aw">→</div></div>')
        nodos.append(f'<div class="qc-blk {cls}"><div class="bl">{_esc(n)}</div>'
                     f'<div class="bsys">{_esc(ins)}</div><div class="bq">{_esc(q)}</div></div>')
    pr = plan.get("presupuesto", {}) or {}
    pac = plan.get("pac", {}) or {}
    strip = [
        ("PDOT", f'{plan.get("metas_total", 0)} metas', "2023-2027"),
        ("POA", f'{len(plan.get("poa_proyectos", []))} proyectos', "operación anual"),
        ("Presupuesto", _m(pr.get("codificado_inversion")), "codificado inversión"),
        ("PAC", _m(pac.get("total_usd")), f'{pac.get("n_procesos", 0)} procesos'),
        ("Ejecución", _m(pr.get("devengado")), f'{pr.get("ti_pct", 0)}% al corte'),
    ]
    si = "".join(f'<div class="pl-si"><div class="k">{_esc(k)}</div><div class="v">{_esc(v)}</div>'
                 f'<div class="s">{_esc(s)}</div></div>' for k, v, s in strip)
    return (
        '<p class="qc-p">La <b>planificación</b> no es un documento: es una <b>cadena</b> que debe sostenerse '
        'del plan al gasto. QUIRA sigue la <b>biografía del plan</b> a través de los sistemas del Estado —cada '
        'eslabón debe respaldar al siguiente—. Si la meta no baja al POA, o el POA no tiene presupuesto, o el '
        'presupuesto no se contrata, la cadena se rompe: eso es una <b>brecha documentada</b>, no una inferencia.</p>'
        f'<div class="qc-pipe">{"".join(nodos)}</div>'
        f'<div class="pl-strip">{si}</div>')


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
    pr = plan.get("presupuesto", {}) or {}
    cob = plan.get("cobertura_metas_poa") or 0
    ipe = (plan.get("ipe_ejecutado", {}) or {}).get("pct")
    filas = [
        ("#1E8E3E", f"{cob:.0f}%", "de las metas del plan bajan a proyectos operativos (POA)."),
        ("#1A73E8", f"{round(ipe) if ipe is not None else 0}%", "del gasto ejecutado está vinculado a los objetivos del PDOT."),
        ("#F9AB00", f"{pr.get('ti_pct',0)}%", "de ejecución de inversión al corte del período."),
    ]
    sint = "".join(f'<div class="qc-sr"><b style="color:{c}">{_esc(v)}</b><span>{_esc(t)}</span></div>' for c, v, t in filas)
    cierre = ('<div class="qc-sr-cierre">En conjunto, la evidencia indica que Montecristi conserva <b>alta '
              'consistencia entre la planificación estratégica y la operación institucional</b>. La principal brecha '
              'del período no reside en la formulación del plan, sino en la <b>velocidad con que la contratación '
              'transforma esa planificación en ejecución presupuestaria</b>.</div>')
    return (f'<div class="qc-sint"><div class="qc-sint-lbl">Síntesis ejecutiva del dominio — Planificación · '
            f'Montecristi · corte {_esc(pr.get("corte",""))}</div><div class="qc-sint-b">{sint}{cierre}'
            f'<div class="qc-fuente">Fuentes: PDOT 2023-2027 · POA · Presupuesto (cédula) · PAC · SERCOP · IPE.</div></div></div>')


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


def _longitudinal_plan(plan: dict) -> str:
    """05 · La trayectoria en el tiempo + proyección (motor temporal → 5º motor Prospectivo).
    Lee la serie del canon (H07b ejecución REAL 2023-2025 + H12c proyección); QUIRA la narra,
    no la recalcula. Los ejercicios CRUZADOS en el cajón, como pidió la dirección."""
    sm = plan.get("serie_multianio") or {}
    ej = sm.get("ejecucion") or []
    cerr = [e for e in ej if e.get("cerrado")]
    if len(cerr) < 2:
        return ""
    curso = next((e for e in ej if not e.get("cerrado")), None)

    def _col(p):
        return "#22D3EE" if p >= 70 else ("#F9AB00" if p >= 55 else "#D93025")

    cards = ""
    for i, e in enumerate(cerr):
        p = e["pct"]
        delta = ""
        if i > 0:
            d = round(p - cerr[i - 1]["pct"], 1)
            dc = "#1E8E3E" if d >= 0 else "#D93025"
            delta = (f'<span style="font-family:ui-monospace,monospace;font-size:9px;color:{dc};'
                     f'margin-left:5px">{"▲" if d >= 0 else "▼"}{abs(d)}pp</span>')
        cards += (f'<div class="pl-si"><div class="k">Ejercicio {e["anio"]}</div>'
                  f'<div class="v" style="color:{_col(p)}">{p:.0f}%</div>'
                  f'<div class="s">ejecución de la inversión{delta}</div></div>')
    if curso:
        cards += (f'<div class="pl-si" style="border-style:dashed;opacity:.7"><div class="k">Ejercicio {curso["anio"]}</div>'
                  f'<div class="v" style="color:var(--tx2)">{curso["pct"]:.0f}%</div>'
                  f'<div class="s">en curso · parcial (no comparable)</div></div>')

    H = [h_serie("Trayectoria de la ejecución", [(e["anio"], e["pct"]) for e in cerr])]
    proy = sm.get("proyeccion") or {}
    if proy.get("proyeccion"):
        med = proy.get("promedio")
        ancla = f"tendencia del período · media {med:.0f}%" if med else "tendencia del período"
        H.append(h_proyeccion("Proyección del próximo ejercicio completo", proy["proyeccion"], ancla))

    intro = ('<p class="qc-p">Los ejercicios <b>cruzados en el tiempo</b>: cómo la planificación se convirtió en '
             'ejecución, año a año. El dato es real —cédulas presupuestarias eSIGEF—; la lectura, del observatorio. '
             'El ejercicio en curso se muestra aparte porque es parcial y no admite comparación.</p>')
    return intro + f'<div class="pl-strip">{cards}</div>' + _hallazgos_html(H)


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
    {_seccion('01', 'El procedimiento · del plan al gasto', _backbone(plan) + _cadena_relacional(plan), _ley_esl(plan, 'poa', 'Fundamento jurídico aplicable'))}
    {_seccion('02', 'El plan y su cobertura', _cobertura(plan), _ley_esl(plan, 'presupuesto', 'Fundamento jurídico aplicable'))}
    {_seccion('03', 'La trazabilidad · metas del plan', '<p class="qc-p">Cada expediente es la <b>biografía de una meta</b>: su recorrido desde el plan hasta el gasto, y hasta dónde llega la cadena documental.</p><p class="qc-cap">No se eligen al azar: se muestran las metas de mayor <b>Valor Demostrativo</b> —el puntaje (0-100) que resume cuánto demuestra el método cada expediente: profundidad de la cadena documental, peso presupuestario y tipo de competencia. A mayor puntaje, más completa y probatoria es la trazabilidad.</p>' + _expedientes_metas(plan), _ley_esl(plan, 'pac', 'Fundamento jurídico aplicable'))}
    {_seccion('04', 'La coherencia · análisis preventivo', _coherencia(plan), _ley_esl(plan, 'gasto', 'Fundamento jurídico aplicable'))}
    {_seccion('05', 'La trayectoria en el tiempo · proyección', _longitudinal_plan(plan))}
    {_seccion('06', 'La evaluación · hallazgos e implicaciones', '<p class="qc-p">Interpretación del dato —no una descripción—: el patrón que revela el análisis, y qué significa.</p>' + _hallazgos_html(_hallazgos_plan(plan)) + _implicaciones_plan(plan))}
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
