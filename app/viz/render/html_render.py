# -*- coding: utf-8 -*-
"""
Sistema de Visualización Canónico — RENDERER HTML del cajón de Verificabilidad.
Dylus Lab © 2026 · implementa CONSTITUCION_VISUAL_QUIRA.md (v1.7) + PCD-MN01 §22-§23.

Consume el SNAPSHOT (no el motor · Regla 1). Gramática de 8 pasos, enriquecida (Javo + asesor
· 2026-07-10): pregunta → principio (📖) → procedimiento [FILTRO ontológico + trazabilidad] →
resultado (el ojo primero) → evidencia (expedientes con mini-cadena) → EVOLUCIÓN longitudinal
(en el mismo cajón · veto de Javo al cajón aparte) → interoperabilidad como RED → síntesis → placa.
Sin "auditoría" (punitivo). Sin códigos internos. Paleta oscura institucional.
"""
from __future__ import annotations

import html as _h

try:  # sintetizador de hallazgos COMPARTIDO (un solo idioma para todos los DOM · asesor 2026-07-11)
    from hallazgos import render_hallazgos as _hallazgos_html  # noqa: F401
    from provenance import prov, prov_leyenda, PROV_CSS  # proveniencia ADR-033 (compartido)  # noqa: F401
except ImportError:  # dentro del paquete app (Streamlit)
    from app.viz.render.hallazgos import render_hallazgos as _hallazgos_html  # noqa: F401
    from app.viz.render.provenance import prov, prov_leyenda, PROV_CSS  # noqa: F401

_COL = {"independiente": "#1E8E3E", "institucional": "#1A73E8", "parcial": "#F9AB00",
        "sin_evidencia_publica": "#9AA0A6", "contradiccion": "#D93025"}  # gramática canónica

# pipeline horizontal · trazabilidad biográfica del dato (más aire · Constitución Visual §5)
_STEPS = [
    ("Origen político", "aseveración de la autoridad", "src", ""),
    ("Planificación · POA", "¿consta la meta?", "", "valida planificación"),
    ("Contratación · SERCOP", "¿se contrató?", "", "valida mercado"),
    ("Presupuesto · cédula", "¿se ejecutó?", "", "valida ejecución"),
    ("Nivel de evidencia", "veredicto documental", "out", "valida transparencia"),
]
# mini-cadena por expediente: hasta qué nodo se corroboró
_CANON = ["Discurso", "POA", "SERCOP", "Presupuesto"]
_UPTO = {"discurso": 0, "poa": 1, "sercop": 2, "cedula": 3}


def _esc(s) -> str:
    return _h.escape(str(s or ""))


def _corta(s, n: int) -> str:
    s = str(s or "").strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(",;:.· ") + "…"


def _ley(marco: dict, clave: str, titulo: str = "Fundamento jurídico aplicable") -> str:
    arts = marco.get(clave) or []
    if not arts:
        return ""
    chips = "".join(f'<span class="qc-lawc">{_esc(a)}</span>' for a in arts)
    return f'<details class="qc-law"><summary>📖 {_esc(titulo)}</summary>{chips}</details>'


def _pct(part: int, whole: int) -> int:
    return round(100 * part / whole) if whole else 0


def _seccion(n: str, titulo: str, cuerpo: str, ley: str = "", cls: str = "", prov: str = "") -> str:
    return (f'<div class="qc-sec {cls}"><div class="qc-h"><span class="qc-hn">{_esc(n)}</span>'
            f'<span class="qc-ht">{_esc(titulo)}</span>{prov}</div>{cuerpo}{ley}</div>')


# ── HALLAZGOS · inferencias CALCULADAS del dato (paso 7 · produce conocimiento, no texto libre) ──
_EJE_INFRA = {"agua", "vías", "vias", "ambiente"}                       # obra física
_EJE_SOCIAL = {"salud", "cultura", "seguridad", "social", "educación", "educacion"}  # política pública
def _hallazgos(snap: dict, serie: list) -> list:
    """Inferencias sobre el dato del snapshot (y la serie): patrones, no descripción."""
    pe = snap.get("por_eje", {})
    emb = snap.get("embudo", {})
    H = []
    # eje con trazabilidad ALTA y ROBUSTA: n≥3 y ≥60% independiente; se elige por prueba absoluta
    cand = {k: v for k, v in pe.items() if v["n"] >= 3 and k != "otro" and v["independiente"] / v["n"] >= 0.6}
    if cand:
        top = max(cand, key=lambda k: cand[k]["independiente"])
        p = _pct(cand[top]["independiente"], cand[top]["n"])
        H.append(("up", f"Mayor trazabilidad en {top.capitalize()}",
                  f"Es el eje con más evidencia independiente robusta: {cand[top]['independiente']} de {cand[top]['n']} afirmaciones ({p}%) tienen registro externo del Estado."))
    if serie and len(serie) >= 2:
        a0, a1 = serie[0], serie[-1]
        y0, y1 = a0["meta"]["año"], a1["meta"]["año"]
        i0, i1 = _metric(a0, "institucional"), _metric(a1, "institucional")
        if i1 - i0 >= 5:
            H.append(("warn", "Incremento de la autocertificación",
                      f"Las afirmaciones sostenidas solo en el informe propio pasan del {i0}% ({y0}) al {i1}% ({y1}): el discurso se apoya más en el reporte institucional que en registros externos."))
        s0, s1 = _metric(a0, "sin"), _metric(a1, "sin")
        if s0 - s1 >= 3:
            H.append(("up", "Retrocede el vacío documental",
                      f"El discurso sin respaldo público baja del {s0}% ({y0}) al {s1}% ({y1}): más afirmaciones alcanzan una fuente verificable."))

    def _avg(ks):
        tot = sum(pe[k]["n"] for k in ks)
        return _pct(sum(pe[k]["independiente"] for k in ks), tot) if tot else 0
    infra = [k for k in pe if k in _EJE_INFRA and pe[k]["n"] >= 2]
    soc = [k for k in pe if k in _EJE_SOCIAL and pe[k]["n"] >= 2]
    if infra and soc:
        pi, ps = _avg(infra), _avg(soc)
        if pi - ps >= 15:
            H.append(("info", "La evidencia se concentra en la inversión",
                      f"Los ejes de infraestructura muestran más trazabilidad ({pi}%) que los de política social ({ps}%): el discurso documenta mejor la obra que su resultado social."))
    pros = next((n["n"] for n in emb.get("niveles", []) if n.get("nivel") == "E"), 0)
    if pros:
        H.append(("prosp", "Compromisos abiertos a seguimiento",
                  f"{pros} afirmaciones son promesas a futuro: no se verifican hoy, pero quedan registradas para contrastar su cumplimiento en la próxima rendición."))
    return H[:4]


# _hallazgos_html: importado del sintetizador compartido hallazgos.render_hallazgos (ver top del módulo)


# ─────────────────────────── 01 · EL PROCEDIMIENTO ───────────────────────────
def _embudo(emb: dict, breve: bool = False) -> str:
    niveles = emb.get("niveles", [])
    total = emb.get("con_gestion", 1) or 1
    seg = "".join(
        f'<div class="qc-fseg" style="flex:{max(n["n"],0.001)};background:{n["color"]}" '
        f'title="{_esc(n["label"])}: {n["n"]}"></div>' for n in niveles if n["n"])
    chips = ""
    for n in niveles:
        grupo = ("analiza" if n["analiza"] else ("segui" if n.get("nivel") == "E" else "arch"))
        chips += (f'<div class="qc-fchip {grupo}"><span class="d" style="background:{n["color"]}"></span>'
                  f'<b>{n["n"]}</b> {_esc(n["label"])} <small>{_esc(n["sub"])}</small></div>')
    intro = ('' if breve else
             '<p class="qc-p">De todo lo dicho, QUIRA analiza solo lo que tiene <b>valor público verificable</b>: '
             'no elimina nada, clasifica y explica por qué algo queda fuera (relevancia ontológica).</p>')
    return (
        intro
        + f'<div class="qc-embudo"><div class="qc-fhead"><span><b>{emb.get("extraidas",0)}</b> afirmaciones '
        f'extraídas</span><span class="ar">→</span><span><b>{emb.get("analizadas",0)}</b> con valor público '
        f'<b>entran al análisis</b></span></div>'
        f'<div class="qc-fbar">{seg}</div><div class="qc-fchips">{chips}</div>'
        f'<div class="qc-fnote">Las <b>prospectivas</b> (compromisos a futuro) y las <b>protocolarias</b> '
        f'(ceremoniales) no se eliminan: se <b>archivan</b> —las primeras para <b>seguimiento</b>— y no entran '
        f'al cálculo de verificabilidad.</div></div>')


def _pipeline() -> str:
    pasos = []
    for i, (lbl, q, cls, vlbl) in enumerate(_STEPS):
        if i:
            pasos.append(f'<div class="qc-conn"><div class="vl">{_esc(vlbl)}</div><div class="aw">→</div></div>')
        pasos.append(f'<div class="qc-blk {cls}"><div class="bl">{_esc(lbl)}</div><div class="bq">{_esc(q)}</div></div>')
    return (f'<p class="qc-p" style="margin-top:18px">Cada afirmación admitida se somete a un <b>escrutinio de '
            f'trazabilidad</b> sobre los ecosistemas de información del Estado. Si el rastro se interrumpe, la '
            f'evidencia pública es nula:</p><div class="qc-pipe">{"".join(pasos)}</div>')


# ── cadena FUSIONADA (Javo · 2026-07-10): pipeline + biografía en UNA cadena · concepto·sistema·pregunta ──
_CAD = [
    ("El discurso", "origen", "lo que afirma la autoridad", "src"),
    ("Planificación", "POA", "¿consta la meta?", ""),
    ("Contratación", "SERCOP", "¿se contrató?", ""),
    ("Presupuesto", "cédula", "¿se ejecutó?", ""),
    ("Integridad", "veredicto", "nivel de evidencia pública", "out"),
]


def _cadena() -> str:
    nodos = []
    for i, (n, sistema, q, cls) in enumerate(_CAD):
        if i:
            nodos.append('<div class="qc-conn"><div class="aw">→</div></div>')
        nodos.append(f'<div class="qc-blk {cls}"><div class="bl">{_esc(n)}</div>'
                     f'<div class="bsys">{_esc(sistema)}</div><div class="bq">{_esc(q)}</div></div>')
    return f'<div class="qc-pipe">{"".join(nodos)}</div>'


def _procedimiento(marco: dict) -> str:
    """01 · La explicación COMPARTIDA del método (una vez, no por año). Fusiona la cadena de
    trazabilidad y la biografía del dato en UNA sola (Javo · 2026-07-10). Prepara al lector."""
    return (
        '<p class="qc-p">La <b>rendición de cuentas</b> es el acto anual y obligatorio en que la autoridad informa '
        'a la ciudadanía qué hizo con lo público. QUIRA toma cada <b>afirmación</b> de ese discurso y sigue su '
        '<b>biografía documental</b> a través de los sistemas del Estado —planificación, contratación, '
        'presupuesto— que históricamente operan en <b>silos</b>. Si el rastro se sostiene de extremo a extremo, '
        'hay evidencia pública; si se interrumpe, la evidencia es nula. Nada se infiere: la ausencia de rastro es, '
        'en sí misma, un resultado. El mismo método es <b>escalable a los 221 gobiernos locales</b>.</p>'
        + _cadena()
        + '<p class="qc-p" style="margin-top:13px">Cada afirmación termina con un <b>nivel de evidencia pública</b> '
        '—no un juicio de verdad—: verificable con <b>registro independiente</b>, declarada solo en el <b>informe '
        'propio</b>, o <b>sin respaldo público</b>. Eso es lo que se lee, año por año, a continuación.</p>'
        + _ley(marco, '01_triangulacion') + _ley(marco, '02_suficiencia_probatoria', 'Suficiencia probatoria'))


def _leyenda_niveles() -> str:
    """El SEMÁFORO de la evidencia — qué dice cada color (cómo leer los resultados de RDC · Javo 2026-07-14).
    Reusa el contenedor de leyenda de la proveniencia (qc-provl), con un cuadro de color por nivel."""
    niveles = [
        ("#1E8E3E", "Prueba independiente", "verificable con un registro público que la autoridad NO controla"),
        ("#1A73E8", "Autocertificación", "declarado solo en el informe propio del GAD, sin un tercero que lo confirme"),
        ("#F9AB00", "Prueba parcial", "hay rastro, pero la cadena documental no se sostiene completa"),
        ("#9AA0A6", "Sin respaldo público", "no existe registro público que lo compruebe — ausencia declarada"),
        ("#D93025", "Prueba en contrario", "el registro público contradice lo afirmado"),
    ]
    filas = "".join(
        f'<div class="qc-provl-i"><span style="width:11px;height:11px;border-radius:3px;background:{c};'
        f'display:inline-block;flex:none"></span><span><b style="color:var(--tx)">{lbl}</b> — {desc}</span></div>'
        for c, lbl, desc in niveles)
    return ('<div class="qc-provl" style="margin-top:12px"><div class="qc-provl-t">El semáforo de la evidencia · '
            f'qué dice cada color</div>{filas}</div>')


# ─────────────────────────── 02 · EL RESULTADO ───────────────────────────
def _resultado(snap: dict, m: dict) -> str:
    r = snap["resumen"]
    ind, sinp = r.get("pct_independiente", 0), r.get("pct_sin_evidencia", 0)
    hero = (
        f'<div class="qc-hero">'
        f'<div class="qc-hbar"><div class="qc-hfill g" style="width:{max(ind,10)}%">'
        f'<span class="qc-hnum">{ind}%</span></div>'
        f'<div class="qc-hlbl">verificable con <b>registros públicos independientes</b></div></div>'
        f'<div class="qc-hbar"><div class="qc-hfill s" style="width:{max(sinp,10)}%">'
        f'<span class="qc-hnum d">{sinp}%</span></div>'
        f'<div class="qc-hlbl"><b>sin respaldo público</b> verificable</div></div>'
        f'</div>')
    filas = ""
    for e in snap["espectro"]:
        sub = f' <small>· {_esc(e["sub"])}</small>' if e["sub"] else ""
        filas += (f'<div class="qc-row"><div class="qc-lbl">{_esc(e["label"])}{sub}</div>'
                  f'<div class="qc-track"><div class="qc-bar" style="width:{max(e["pct"],1)}%;background:{e["color"]}"></div></div>'
                  f'<div class="qc-num"><b>{e["n"]}</b> · {e["pct"]}%</div></div>')
    return (
        f'<p class="qc-p">De las <b>{r.get("sustantivas",0)} afirmaciones con valor público</b> del ejercicio, '
        f'contrastadas por toda la cadena documental:</p>'
        f'{hero}<div class="qc-esp-h">Desglose por nivel de evidencia</div>{filas}')


# ─────────────────────────── 03 · EXPEDIENTES ───────────────────────────
def _minichain(cadena: str) -> str:
    # cada tipo de evidencia tiene su propia biografía documental (Javo · 2026-07-10)
    if cadena == "registro":        # cobertura del patronato vía transparencia (LOTAIP)
        pares = [("Discurso", True), ("Patronato", True), ("Transparencia Activa", True), ("Literal D", True)]
    elif cadena == "informe":       # autocertificación (informe anual al CPCCS)
        pares = [("Discurso", True), ("Informe Anual", True), ("CPCCS", True)]
    else:                           # cadena de silos del Estado: POA → SERCOP → Presupuesto
        upto = _UPTO.get(cadena, 0)
        pares = [(s, i <= upto) for i, s in enumerate(_CANON)]
    nodos = []
    for j, (s, on) in enumerate(pares):
        if j:
            nodos.append(f'<span class="mc-a {"on" if on else ""}">→</span>')
        nodos.append(f'<span class="mc-n {"on" if on else "off"}">{_esc(s)}</span>')
    return f'<div class="qc-mc"><span class="mc-t">Cadena documental encontrada</span><div class="mc-row">{"".join(nodos)}</div></div>'


def _expedientes(snap: dict) -> str:
    out = ""
    for e in snap["expedientes"]:
        badges = "".join(f'<span class="qc-bdg">{_esc(b)}</span>' for b in e.get("badges", []))
        out += (f'<div class="qc-exp"><div class="qc-exp-top">'
                f'<span class="qc-exp-id">EXPEDIENTE · afirmación estratégica · {_esc(e["id"])}</span>'
                f'<span class="qc-stamp" style="color:{e["color"]};border-color:{e["color"]}">{_esc(e["estado"])}</span></div>'
                f'<div class="qc-vd"><span class="qc-vd-s">Valor demostrativo <b>{e.get("vd", 0)}</b></span>{badges}</div>'
                f'<div class="qc-exp-b">'
                f'<div class="qc-kv"><span class="k">Aseveración</span><span class="v">"{_esc(_corta(e["aseveracion"],104))}"</span></div>'
                f'<div class="qc-kv"><span class="k">Fuente</span><span class="v">{_esc(e["fuente"])}</span></div>'
                f'<div class="qc-kv"><span class="k">Resultado</span><span class="v"><b>{_esc(_corta(e["resultado"],128))}</b></span></div>'
                f'{_minichain(e.get("cadena","discurso"))}</div></div>')
    return f'<div class="qc-exps">{out}</div>'


# ─────────────────────────── 04 · EVOLUCIÓN (longitudinal) ───────────────────────────
def _metric(snap: dict, clave: str) -> int:
    r = snap["resumen"]
    n = r.get("sustantivas", 0) or 1
    if clave == "independiente":
        return r.get("pct_independiente", 0)
    if clave == "sin":
        return r.get("pct_sin_evidencia", 0)
    return _pct(r.get("institucional", 0), n)   # autocertificación


def _evolucion(serie: list, marco: dict) -> str:
    if not serie or len(serie) < 2:
        base = serie[-1] if serie else {}
        a = base.get("meta", {}).get("año", "—")
        return (f'<p class="qc-p"><b>Ejercicio {_esc(a)} — línea base.</b> Es el primer período medido con esta '
                f'metodología; al incorporar el siguiente año, esta sección trazará la <b>evolución</b> de la '
                f'verificabilidad y el <b>seguimiento de los compromisos a futuro</b>.</p>')
    a0, a1 = serie[0], serie[-1]
    y0, y1 = a0["meta"]["año"], a1["meta"]["año"]
    met = [("independiente", "Prueba independiente", "#1E8E3E"),
           ("institucional", "Autocertificación", "#1A73E8"),
           ("sin", "Sin respaldo público", "#9AA0A6")]
    cards = ""
    for clave, lbl, col in met:
        v0, v1 = _metric(a0, clave), _metric(a1, clave)
        d = v1 - v0
        signo = "▲" if d > 0 else ("▼" if d < 0 else "■")
        if d == 0 or clave == "institucional":       # autocertificación: cambio contextual → neutro
            dcol = "#9AA0A6"
        else:                                         # independiente: subir es mejor · sin: bajar es mejor
            dcol = "#1E8E3E" if ((d > 0) == (clave == "independiente")) else "#D93025"
        cards += (f'<div class="qc-ev"><div class="ev-l" style="color:{col}">{_esc(lbl)}</div>'
                  f'<div class="ev-r"><div class="ev-yr"><span class="ev-y">{y0}</span><b>{v0}%</b></div>'
                  f'<span class="ev-ar">→</span>'
                  f'<div class="ev-yr"><span class="ev-y">{y1}</span><b style="color:{col}">{v1}%</b></div>'
                  f'<span class="ev-d" style="color:{dcol};border-color:{dcol}">{signo} {abs(d)}</span></div></div>')
    # PERFIL EVOLUTIVO por eje: no solo el %, el COMPORTAMIENTO (barra + cambio vs año anterior)
    e0, e1 = a0.get("por_eje", {}), a1.get("por_eje", {})
    ejes = sorted(set(e0) & set(e1), key=lambda k: -(e1[k]["n"]))
    perfil = ""
    for ej in ejes[:6]:
        p0 = _pct(e0[ej]["independiente"], e0[ej]["n"])
        p1 = _pct(e1[ej]["independiente"], e1[ej]["n"])
        d = p1 - p0
        ar, dc = ("▲", "#1E8E3E") if d > 0 else (("▼", "#D93025") if d < 0 else ("■", "#9AA0A6"))
        perfil += (f'<div class="qc-pf"><div class="pf-l">{_esc(ej.capitalize())}</div>'
                   f'<div class="pf-track"><div class="pf-bar" style="width:{max(p1,2)}%"></div></div>'
                   f'<div class="pf-v">{p1}%</div><div class="pf-d" style="color:{dc}">{ar} {abs(d)}</div></div>')
    perfil_html = (f'<div class="qc-ev-h">Perfil por eje temático · {y1}</div>'
                   f'<p class="qc-cap">Cada barra es un <b>tema del cantón</b> (agua, salud, vías…): su largo es el '
                   f'<b>porcentaje del discurso de ese tema que tiene prueba independiente</b> en {y1}; a la derecha, '
                   f'cuánto cambió frente a {y0} (▲ mejoró · ▼ retrocedió · en puntos porcentuales).</p>'
                   f'<div class="qc-pfs">{perfil}</div>') if perfil else ""
    return (
        f'<p class="qc-p">La rendición no es un acto de un solo año: la ley exige <b>seguimiento plurianual</b> '
        f'de los compromisos. Al cruzar los ejercicios <b>{y0} ↔ {y1}</b> aparece el <b>comportamiento del '
        f'discurso</b> —qué mejora, qué depende del informe propio, qué sigue sin respaldo—:</p>'
        f'<p class="qc-cap">Cada tarjeta es un <b>indicador de verificabilidad</b>: muestra su valor en {y0} y en '
        f'{y1}, y la <b>flecha</b> marca el cambio (<b>▲</b> subió · <b>▼</b> bajó · <b>■</b> estable).</p>'
        f'<div class="qc-evs">{cards}</div>{perfil_html}')


# ─────────────────────────── 05 · INTEROPERABILIDAD (red) ───────────────────────────
# biografía del dato — la TESIS (concepto + término concreto que ya usábamos + glosa · Javo 2026-07-10)
_BIO = [("Dato", "discurso", "lo que se dijo"), ("Documento", "POA", "dónde consta"),
        ("Sistema", "SERCOP", "qué entidad lo registra"), ("Evidencia", "cédula", "nivel de respaldo"),
        ("Integridad", "veredicto", "¿la cadena se sostiene?")]


def _red() -> str:
    nodos = []
    for i, (n, c, s) in enumerate(_BIO):
        if i:
            nodos.append('<div class="bio-a">→</div>')
        last = " last" if i == len(_BIO) - 1 else ""
        nodos.append(f'<div class="bio-n{last}"><div class="bn">{_esc(n)}</div>'
                     f'<div class="bc">{_esc(c)}</div><div class="bs">{_esc(s)}</div></div>')
    return (f'<p class="qc-p">La innovación no es conectar sistemas: es <b>seguir la biografía del dato</b> a través de '
            f'ellos. Cada aseveración recorre una <b>vida documental</b> —de lo dicho a la integridad verificable— '
            f'cruzando entidades que operan en silos, de forma <b>escalable a los 221 gobiernos locales</b>:</p>'
            f'<div class="qc-bio">{"".join(nodos)}</div>')


# ─────────────────────────── síntesis ───────────────────────────
def _implicaciones(snap: dict, serie: list) -> str:
    """El SO-WHAT: qué SIGNIFICA el resultado (implicaciones, no conclusiones · asesor 2026-07-10).
    Convierte el cajón en un artículo científico visual: no dice 55%, dice qué significa ese 55%."""
    r = snap["resumen"]
    ind, sinp = r.get("pct_independiente", 0), r.get("pct_sin_evidencia", 0)
    if serie and len(serie) >= 2:
        a0, a1 = serie[0], serie[-1]
        s0, s1 = _metric(a0, "sin"), _metric(a1, "sin")
        i0, i1 = _metric(a0, "institucional"), _metric(a1, "institucional")
        partes = []
        if s1 < s0:
            partes.append("el municipio incrementó la publicación de información verificable")
        elif s1 > s0:
            partes.append("creció la proporción de afirmaciones sin respaldo público")
        if i1 > i0:
            partes.append("también aumentó la dependencia del informe institucional propio")
        elif i1 < i0:
            partes.append("se apoyó menos en su propio informe")
        cuerpo = ", pero ".join(partes) if partes else "el nivel de verificabilidad se mantiene estable"
        if s1 < s0 and i1 > i0:
            cierre = ("Sugiere una mejora parcial en la transparencia documental, aunque persisten áreas con "
                      "limitada trazabilidad independiente.")
        elif s1 < s0:
            cierre = "Sugiere una mejora en la transparencia documental del período."
        else:
            cierre = "Sugiere una consolidación del proceso, con margen de mejora en la evidencia independiente."
        txt = f"Este análisis evidencia que {cuerpo}. {cierre}"
    else:
        txt = (f"Este primer ejercicio medido fija la línea base: {ind}% del discurso admite verificación "
               f"independiente y {sinp}% carece de respaldo público consultable. Es el punto de partida del "
               f"seguimiento plurianual de la integridad del discurso.")
    return f'<div class="qc-impl"><div class="qc-impl-t">Implicaciones</div><div class="qc-impl-b">{_esc(txt)}</div></div>'


# ── LOS APORTES CIUDADANOS — 3ª dimensión del RDC: el documento CPCCS (Javo · 2026-07-10) ──
# la demanda ciudadana recorre los MISMOS silos del Estado que el discurso (fusión · Javo 2026-07-10)
_CAD_AP = ["Demanda ciudadana", "POA", "SERCOP", "Ejecución"]
_AP_EST = {"atendido": ("Atendido", "#1E8E3E"), "por_validar": ("En seguimiento", "#F9AB00"),
           "sin_correlato": ("Sin correlato", "#9AA0A6")}


def _minichain_aporte(estado: str) -> str:
    upto = {"atendido": 3, "por_validar": 1, "sin_correlato": 0}.get(estado, 0)
    nodos = []
    for j, s in enumerate(_CAD_AP):
        if j:
            nodos.append(f'<span class="mc-a {"on" if j <= upto else ""}">→</span>')
        nodos.append(f'<span class="mc-n {"on" if j <= upto else "off"}">{_esc(s)}</span>')
    return f'<div class="qc-mc"><span class="mc-t">Trazabilidad del aporte</span><div class="mc-row">{"".join(nodos)}</div></div>'


def _aporte_vd(d: dict) -> tuple:
    vd = {"atendido": 86, "por_validar": 56, "sin_correlato": 30}.get(d.get("estado"), 30)
    if d.get("estado") == "atendido" and d.get("tiempo") == "a_tiempo":
        vd += 10
    badges = [_AP_EST.get(d.get("estado"), ("—", ""))[0]]
    t = {"a_tiempo": "A tiempo", "tarde": "Con demora"}.get(d.get("tiempo"))
    if t and d.get("estado") != "sin_correlato":
        badges.append(t)
    try:
        mo = float(d.get("monto", 0) or 0)
        if mo > 0:
            badges.append(f"${mo:,.0f}")
    except (TypeError, ValueError):
        pass
    return min(vd, 100), badges[:3]


def _aportes(ap: dict) -> str:
    det = (ap or {}).get("detalle") or []
    if not det:
        return ""
    total = ap.get("total", len(det)) or 1
    est = ap.get("por_estado", {}) or {}
    pat, psin = _pct(est.get("atendido", 0), total), _pct(est.get("sin_correlato", 0), total)
    hero = (f'<div class="qc-hero"><div class="qc-hbar"><div class="qc-hfill g" style="width:{max(pat,10)}%">'
            f'<span class="qc-hnum">{pat}%</span></div><div class="qc-hlbl">de los aportes tienen '
            f'<b>correspondencia verificada</b> con una obra o servicio</div></div>'
            f'<div class="qc-hbar"><div class="qc-hfill s" style="width:{max(psin,10)}%">'
            f'<span class="qc-hnum d">{psin}%</span></div><div class="qc-hlbl"><b>sin correlato</b> en la ejecución</div></div></div>')
    ti = ap.get("por_tiempo", {}) or {}
    filas_t = [("A tiempo", ti.get("a_tiempo", 0), "#1E8E3E"), ("Con demora", ti.get("tarde", 0), "#F9AB00"),
               ("Sin respuesta", ti.get("olvidado", 0), "#9AA0A6")]
    filas = "".join(f'<div class="qc-row"><div class="qc-lbl">{_esc(lbl)}</div>'
                    f'<div class="qc-track"><div class="qc-bar" style="width:{max(_pct(nn,total),1)}%;background:{cc}"></div></div>'
                    f'<div class="qc-num"><b>{nn}</b> · {_pct(nn,total)}%</div></div>' for lbl, nn, cc in filas_t)

    def _by(e):
        return sorted([d for d in det if d.get("estado") == e], key=lambda d: -_aporte_vd(d)[0])
    sel = (_by("atendido")[:2] + _by("por_validar")[:1] + _by("sin_correlato")[:2])[:4]
    exps = ""
    for d in sel:
        vd, badges = _aporte_vd(d)
        lbl, col = _AP_EST.get(d.get("estado"), ("—", "#9AA0A6"))
        bch = "".join(f'<span class="qc-bdg">{_esc(b)}</span>' for b in badges)
        res = (f'{_corta(d.get("evidencia",""), 110)} ({d.get("anio_ejecucion","")})'
               if d.get("estado") != "sin_correlato" and d.get("evidencia")
               else "No se localizó obra o servicio correlativo en la ejecución del período.")
        exps += (f'<div class="qc-exp"><div class="qc-exp-top">'
                 f'<span class="qc-exp-id">APORTE CIUDADANO · {_esc(d.get("eje",""))} · pedido {_esc(d.get("anio_aporte",""))}</span>'
                 f'<span class="qc-stamp" style="color:{col};border-color:{col}">{_esc(lbl)}</span></div>'
                 f'<div class="qc-vd"><span class="qc-vd-s">Valor demostrativo <b>{vd}</b></span>{bch}</div>'
                 f'<div class="qc-exp-b">'
                 f'<div class="qc-kv"><span class="k">Demanda</span><span class="v">"{_esc(_corta(d.get("demanda",""),104))}"</span></div>'
                 f'<div class="qc-kv"><span class="k">Sector</span><span class="v">{_esc(d.get("sector","—"))}</span></div>'
                 f'<div class="qc-kv"><span class="k">Resultado</span><span class="v"><b>{_esc(res)}</b></span></div>'
                 f'{_minichain_aporte(d.get("estado"))}</div></div>')
    return (
        '<p class="qc-p">El informe de rendición registra los <b>aportes ciudadanos</b> recibidos en el proceso. '
        'No son vinculantes —orientan la gestión—, pero QUIRA rastrea cada <b>demanda</b> hasta la <b>obra o '
        'servicio</b> que la atiende, a lo largo de todo el período de gobierno (no solo el año siguiente):</p>'
        f'{hero}<div class="qc-esp-h">Tiempo de respuesta del gobierno</div>{filas}'
        '<div class="qc-subh">Los aportes, rastreados</div>'
        f'<div class="qc-exps">{exps}</div>')


def _conclusion(snap: dict, m: dict, serie: list | None = None) -> str:
    """Síntesis ejecutiva del DOMINIO (no de un año · Javo 2026-07-10): rotula el período completo."""
    sint = ""
    for nivel, val, txt in snap["sintesis"]["hallazgos"]:
        col = _COL.get(nivel, _COL["independiente"])
        sint += f'<div class="qc-sr"><b style="color:{col}">{_esc(val)}</b><span>{_esc(txt)}</span></div>'
    fuentes = " · ".join(_esc(f) for f in snap["sintesis"]["fuentes"])
    años = [s["meta"]["año"] for s in serie if s] if serie else [m.get("año")]
    periodo = f'{años[0]}–{años[-1]}' if len(años) > 1 else str(años[0])
    return (f'<div class="qc-sint"><div class="qc-sint-lbl">Síntesis ejecutiva del dominio — Rendición de '
            f'Cuentas · {_esc(m.get("canton"))} · período {_esc(periodo)}</div><div class="qc-sint-b">{sint}'
            f'<div class="qc-fuente">Fuentes: {fuentes}.</div></div></div>')


_FOLD_CSS = (
    ".qc-fold{margin:11px 0 2px;border:1px solid var(--bd);border-radius:8px;overflow:hidden}"
    ".qc-fold>summary{cursor:pointer;padding:9px 13px;font-family:ui-monospace,monospace;font-size:10px;"
    "font-weight:700;letter-spacing:.03em;color:var(--tx2);background:var(--sf);list-style:none}"
    ".qc-fold>summary::-webkit-details-marker{display:none}"
    ".qc-fold>summary::before{content:'\\25B8  '}.qc-fold[open]>summary::before{content:'\\25BE  '}"
    ".qc-foldw{overflow-x:auto}.qc-foldt{width:100%;border-collapse:collapse;font-size:11px}"
    ".qc-foldt th{text-align:left;padding:7px 13px;color:var(--tx2);font-family:ui-monospace,monospace;"
    "font-size:8px;text-transform:uppercase;letter-spacing:.05em;border-top:1px solid var(--bd);white-space:nowrap}"
    ".qc-foldt td{padding:7px 13px;color:var(--tx2);border-top:1px solid var(--bd)}"
    ".qc-foldt td:first-child{color:var(--tx)}"
    ".qc-foldt td.n{text-align:right;font-family:ui-monospace,monospace;font-weight:700;color:var(--tx)}"
)


def _tabla_fold(summary: str, headers: list, filas: list) -> str:
    """Tabla como EVIDENCIA bajo demanda (Primacía Narrativa · patrón desplegable). Cada fila es una
    lista de celdas (texto, clase). No es protagonista: se abre con clic."""
    if not filas:
        return ""
    th = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    cuerpo = "".join("<tr>" + "".join(f'<td class="{c}">{_esc(v)}</td>' for v, c in fila) + "</tr>" for fila in filas)
    return (f'<details class="qc-fold"><summary>{_esc(summary)}</summary>'
            f'<div class="qc-foldw"><table class="qc-foldt"><thead><tr>{th}</tr></thead>'
            f'<tbody>{cuerpo}</tbody></table></div></details>')


def _evidencia_por_eje(snap: dict) -> str:
    """Tabla de evidencia (Javo · como Planificación): distribución de las afirmaciones por área de
    gestión y cuántas tienen prueba independiente. Dato del snapshot; no se protagoniza."""
    pe = snap.get("por_eje", {}) or {}
    if not pe:
        return ""
    filas = []
    for eje, v in sorted(pe.items(), key=lambda kv: -((kv[1] or {}).get("n", 0) or 0)):
        v = v or {}
        n = v.get("n", 0) or 0
        ind = v.get("independiente", 0) or 0
        pct = round(100 * ind / n) if n else 0
        filas.append([(eje.replace("_", " ").capitalize(), ""), (str(n), "n"), (str(ind), "n"), (f"{pct}%", "n")])
    tabla = _tabla_fold("Ver el detalle por área de gestión",
                        ["Área de gestión", "Afirmaciones", "Con prueba independiente", "Verificable"], filas)
    return '<div class="qc-subh">La evidencia por área de gestión</div>' + tabla


# ─────────────────────────── ensamblaje ───────────────────────────
def _analisis_anio(snap: dict, n: int) -> str:
    """Bloque de análisis de UN ejercicio (embudo + resultado + expedientes) — se repite por año.
    Lo EXPLICATIVO no va aquí (está una sola vez en 01 El procedimiento · Javo 2026-07-10)."""
    m = snap["meta"]
    cuerpo = ('<div class="qc-subh">Qué entró al análisis</div>'
              + _embudo(snap.get("embudo", {}), breve=True)
              + '<div class="qc-subh">Qué pudo verificarse</div>' + _resultado(snap, m)
              + '<div class="qc-subh">Los expedientes</div>' + _expedientes(snap)
              + _evidencia_por_eje(snap))
    return _seccion(f'0{n}', f'Ejercicio Fiscal {m.get("año")} · {m.get("autoridad")}', cuerpo, cls="qc-anio", prov=prov('doc'))


def _evaluacion(serie: list, marco: dict) -> str:
    """La evaluación COMPARTIDA (una vez): evolución + perfil + hallazgos + prospectiva + implicaciones."""
    return (_evolucion(serie, marco)
            + '<div class="qc-subh">Hallazgos del análisis</div>'
            + '<p class="qc-p">Interpretación del dato —no una descripción—: el patrón que revela, y qué significa.</p>'
            + _hallazgos_html(_hallazgos(serie[-1], serie))
            + _implicaciones(serie[-1], serie))


def _rendicion_en_tiempo(serie: list) -> str:
    """02 · LA RENDICIÓN EN EL TIEMPO — introductoria (Javo · 2026-07-10): los ejercicios del período
    (informe, fecha, lugar, asistencia). Integra la serie en el formato del cajón."""
    serie = [s for s in (serie or []) if s]
    if not serie:
        return ""
    filas = ""
    maxa = max((s.get("asistentes") or 0) for s in serie) or 1
    for s in serie:
        a = s.get("asistentes")
        filas += (f'<tr><td>RDC {_esc(s.get("periodo"))}</td><td>N° {_esc(s.get("informe_n","—"))}</td>'
                  f'<td>{_esc(s.get("fecha_rdc","—"))}</td><td>{_esc(s.get("lugar","—"))}</td>'
                  f'<td class="num">{a if a else "—"}</td><td class="num">{s.get("n_componentes",0)}</td></tr>')
    barras = "".join(
        f'<div class="qc-att"><div class="qc-att-n">{(s.get("asistentes") or "—")}</div>'
        f'<div class="qc-att-bar" style="height:{max(round(58*(s.get("asistentes") or 0)/maxa),3)}px"></div>'
        f'<div class="qc-att-y">{_esc(s.get("periodo"))}</div></div>' for s in serie)
    a0 = serie[0].get("asistentes") or 0
    aN = serie[-1].get("asistentes") or 0
    delta = f"+{round(100 * (aN - a0) / a0)}%" if a0 else "—"
    return (
        '<p class="qc-p">La rendición de cuentas es un <b>acto anual y obligatorio</b> ante la ciudadanía y el '
        'Consejo de Participación Ciudadana y Control Social. Estos son los <b>ejercicios del período</b>, con su '
        'evolución verificable —informe, fecha, lugar y asistencia ciudadana—; es el punto de partida de todo lo '
        'que sigue:</p>'
        f'<table class="qc-serie"><tr><th>Período</th><th>Informe</th><th>Fecha</th><th>Lugar</th>'
        f'<th class="num">Asistentes</th><th class="num">Componentes</th></tr>{filas}</table>'
        f'<div class="qc-att-h">Asistencia ciudadana a la rendición</div><div class="qc-atts">{barras}</div>'
        f'<p class="qc-p" style="margin-top:12px">La <b>asistencia</b> creció de <b>{a0}</b> a <b>{aN}</b> '
        f'(<b>{delta}</b>): el control social se fortalece. Es aún una participación <b>reducida</b> frente al tamaño '
        f'del cantón —un margen de ampliación, no una falla del proceso—.</p>')


def cajon_dominio_rdc(serie: list, rdc_serie: list | None = None, doc: dict | None = None) -> str:
    """Cajón RDC del DOMINIO completo (3 dimensiones · Javo 2026-07-10): el DISCURSO (procedimiento +
    análisis por año + evaluación), los EJERCICIOS en el tiempo (serie), y el DOCUMENTO CPCCS (aportes
    ciudadanos + cumplimiento del plan de trabajo). `serie` = snapshots del motor (ascendente); `rdc_serie`
    = ejercicios de rendición; `doc` = dict de rendición del GM (aportes, cumplimiento_actual, …)."""
    serie = [s for s in serie if s]
    if not serie:
        return ""
    ref = serie[-1]
    m, marco = ref["meta"], ref.get("marco_legal", {})
    bloques, n = [], 1
    bloques.append(_seccion(f'0{n}', 'Cómo leer este dominio · el procedimiento', prov_leyenda() + _procedimiento(marco) + _leyenda_niveles())); n += 1
    serie_html = _rendicion_en_tiempo(rdc_serie or [])
    if serie_html:                                            # LA RENDICIÓN EN EL TIEMPO como introducción (Javo)
        bloques.append(_seccion(f'0{n}', 'La rendición en el tiempo · los ejercicios del período', serie_html)); n += 1
    for s in serie:
        bloques.append(_analisis_anio(s, n)); n += 1          # 0X · Ejercicio 20XX (por año · el discurso)
    doc = doc or {}                                           # 3ª dimensión · el DOCUMENTO CPCCS (aportes · Javo)
    ap_html = _aportes(doc.get("aportes") or {})
    if ap_html:
        bloques.append(_seccion(f'0{n}', 'Los aportes ciudadanos · la voz que se rastrea', ap_html,
                                _ley(marco, 'dominio_lead', 'Fundamento (aportes ciudadanos · LOPC)'))); n += 1
    bloques.append(_seccion(f'0{n}', 'La evaluación · comparación, patrones y prospectiva',
                            _evaluacion(serie, marco), _ley(marco, '04_analisis_sistemico')))
    cuerpo = "".join(bloques) + _conclusion(ref, m, serie)    # síntesis ejecutiva del DOMINIO al cierre (Javo)
    return f"""{_CSS}
<section class="qc">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio {_esc(m.get('municipio'))}</div>
    <div class="qc-idea">{_esc(ref['dominio'])}</div>
    <div class="qc-q">¿Qué parte del discurso de la autoridad admite verificación con fuentes públicas oficiales?</div>
  </div>
  <div class="qc-princ"><span class="t">Principio metodológico</span>
    QUIRA <b>no certifica la veracidad</b> de lo que dice la autoridad: reconstruye la <b>trazabilidad biográfica
    del dato público</b> —la historia documental de cada afirmación—. Cada logro declarado debe poder demostrarse a
    lo largo de su <b>ciclo de vida documental</b>: planificación → contratación → ejecución. Lo que no deja rastro
    público no se infiere: se registra como <b>ausencia de evidencia</b> —un resultado, nunca una acusación—.
    {_ley(marco, 'dominio_lead', 'Fundamento del dominio (Rendición de Cuentas)')}
  </div>
  <div class="qc-body">{cuerpo}</div>
  <div class="qc-placa"><div class="qc-placa-q">QUIRA no certifica la verdad. Certifica el nivel de<br>verificabilidad pública de cada afirmación.</div>
    <div class="qc-placa-s">La ausencia de evidencia es un resultado del análisis documental, nunca una acusación.</div>
    <div style="margin-top:15px;padding-top:12px;border-top:1px solid var(--bd);font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx2)">⬡ QUIRA · <b style="color:var(--tx)">by Dylus&nbsp;Lab</b></div>
  </div>
</section>"""


def cajon_dominio_streamlit(serie: list, rdc_serie: list | None = None, doc: dict | None = None) -> str:
    """HTML del dominio RDC listo para st.markdown (sin sangría ni líneas en blanco)."""
    h = cajon_dominio_rdc(serie, rdc_serie, doc)
    return "\n".join(ln.lstrip() for ln in h.splitlines() if ln.strip())


def cajon_verificabilidad(snap: dict, serie: list | None = None) -> str:
    """(Legado · un año) Snapshot + serie opcional → HTML del cajón. Reemplazado por cajon_dominio_rdc."""
    m = snap["meta"]
    marco = snap.get("marco_legal", {})

    def sec(n, titulo, cuerpo, ley=""):
        return (f'<div class="qc-sec"><div class="qc-h"><span class="qc-hn">{n}</span>'
                f'<span class="qc-ht">{_esc(titulo)}</span></div>{cuerpo}{ley}</div>')

    proc = _embudo(snap.get("embudo", {})) + _pipeline()
    return f"""{_CSS}
<section class="qc">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio {_esc(m.get('municipio'))}</div>
    <div class="qc-idea">{_esc(snap['dominio'])}</div>
    <div class="qc-q">¿Qué parte del discurso de la autoridad admite verificación con fuentes públicas oficiales?</div>
  </div>
  <div class="qc-princ"><span class="t">Principio metodológico</span>
    QUIRA <b>no certifica la veracidad</b>: reconstruye la <b>trazabilidad biográfica del dato público</b>.
    Exige que cada logro declarado demuestre su <b>ciclo de vida documental</b> —planificación → contratación → ejecución—.
    {_ley(marco, 'dominio_lead', 'Fundamento del dominio (Rendición de Cuentas)')}
  </div>
  <div class="qc-body">
    {sec('01', 'El procedimiento · qué se analiza y cómo se rastrea', proc, _ley(marco, '01_triangulacion'))}
    {sec('02', 'El resultado', _resultado(snap, m), _ley(marco, '02_suficiencia_probatoria'))}
    {sec('03', 'La evidencia · expedientes', '<p class="qc-p">Cada expediente es la <b>trazabilidad biográfica</b> de una afirmación estratégica: su historia desde el discurso hasta su corroboración en los sistemas del Estado. Nunca discurso ceremonial.</p>' + _expedientes(snap), _ley(marco, '03_fichas_contraste'))}
    {sec('04', 'La evolución · seguimiento plurianual', _evolucion(serie or [snap], marco), _ley(marco, 'dominio_lead', 'Fundamento del seguimiento (rendición plurianual)'))}
    {sec('05', 'Interoperabilidad · la innovación', _red(), _ley(marco, '04_analisis_sistemico'))}
    {sec('06', 'Los hallazgos · lo que revela el análisis', '<p class="qc-p">Interpretación del dato —no una descripción—: el patrón que revela el análisis, y qué significa.</p>' + _hallazgos_html(_hallazgos(snap, serie or [snap])) + _implicaciones(snap, serie or [snap]))}
    {_conclusion(snap, m)}
  </div>
  <div class="qc-placa"><div class="qc-placa-q">QUIRA no certifica la verdad. Certifica el nivel de<br>verificabilidad pública de cada afirmación.</div>
    <div class="qc-placa-s">La ausencia de evidencia es un resultado del análisis documental, nunca una acusación.</div>
    <div style="margin-top:15px;padding-top:12px;border-top:1px solid var(--bd);font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx2)">⬡ QUIRA · <b style="color:var(--tx)">by Dylus&nbsp;Lab</b></div>
  </div>
</section>"""


def cajon_streamlit(snap: dict, serie: list | None = None) -> str:
    """HTML listo para st.markdown(unsafe_allow_html=True): sin indentación ni líneas en blanco
    (evita que el parser de Streamlit lo interprete como bloques de código/párrafos)."""
    h = cajon_verificabilidad(snap, serie)
    return "\n".join(ln.lstrip() for ln in h.splitlines() if ln.strip())


_CSS = """<style>
.qc{--ind:#1E8E3E;--inst:#1A73E8;--parc:#F9AB00;--sin:#9AA0A6;--prosp:#8B7BD8;--law:#6BA6C9;
 --tx:#E7ECF3;--tx2:#97A3B8;--sf:rgba(255,255,255,.03);--bd:rgba(255,255,255,.14);
 font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--tx);max-width:1080px;margin:0 auto;
 font-size:14px;line-height:1.55;border:1px solid var(--bd);border-top:3px solid var(--ind);border-radius:5px;
 background:#0E1420;overflow:hidden}
.qc *{box-sizing:border-box}
.qc-hd{padding:22px 26px 18px;border-bottom:1px solid var(--bd)}
.qc-ey{font-family:ui-monospace,monospace;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--tx2)}
.qc-idea{font-family:Georgia,serif;font-size:26px;font-weight:600;margin:8px 0 11px}
.qc-q{font-family:Georgia,serif;font-size:16px;font-style:italic;line-height:1.4;border-left:3px solid var(--ind);padding-left:14px}
.qc-princ{margin:20px 26px 0;padding:13px 16px;background:rgba(30,142,62,.08);border:1px solid rgba(30,142,62,.3);border-radius:7px;font-size:13px;color:var(--tx2)}
.qc-princ .t{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ind);font-weight:700;display:block;margin-bottom:4px}
.qc-princ b{color:var(--tx)}
.qc-law{margin-top:11px;font-size:11.5px}
details.qc-law summary{cursor:pointer;list-style:none;color:var(--law);font-family:ui-monospace,monospace;font-size:11px;font-weight:600;padding:5px 9px;border:1px solid var(--law);border-radius:4px;display:inline-block}
details.qc-law summary::-webkit-details-marker{display:none}
details.qc-law[open] summary{margin-bottom:7px}
.qc-lawc{display:inline-block;font-family:ui-monospace,monospace;font-size:10px;color:var(--tx2);border:1px solid var(--bd);border-radius:3px;padding:1px 6px;margin:3px 4px 0 0;white-space:nowrap}
.qc-body{padding:8px 26px 22px}.qc-sec{margin-top:30px}
.qc-subh{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx2);font-weight:700;margin:22px 0 11px}
.qc-anio{border:1px solid var(--bd);border-radius:9px;padding:2px 18px 18px;margin-top:24px;background:rgba(255,255,255,.015)}
.qc-anio>.qc-h{margin-top:16px}.qc-anio>.qc-h .qc-ht{font-size:17px;font-family:Georgia,serif}
.qc-h{display:flex;align-items:baseline;gap:10px;margin:0 0 12px}
.qc-hn{font-family:ui-monospace,monospace;font-size:12px;color:var(--ind);font-weight:700}
.qc-ht{font-size:15px;font-weight:600}
.qc-p{font-size:12.5px;color:var(--tx2);margin:0 0 13px}.qc-p b{color:var(--tx);font-weight:600}
/* embudo */
.qc-embudo{border:1px solid var(--bd);border-radius:8px;padding:14px 16px;background:var(--sf)}
.qc-fhead{display:flex;align-items:center;gap:12px;font-size:13px;color:var(--tx2);margin-bottom:10px}
.qc-fhead b{color:var(--tx);font-size:15px}.qc-fhead .ar{color:var(--law);font-size:16px}
.qc-fbar{display:flex;height:16px;border-radius:3px;overflow:hidden;gap:2px}
.qc-fseg{min-width:5px}
.qc-fchips{display:flex;flex-wrap:wrap;gap:6px 16px;margin-top:11px}
.qc-fchip{font-size:11.5px;color:var(--tx2);display:flex;align-items:center;gap:6px}
.qc-fchip b{color:var(--tx)}.qc-fchip small{opacity:.7}
.qc-fchip .d{width:9px;height:9px;border-radius:2px;flex:none}
.qc-fchip.arch{opacity:.65}
/* pipeline (respira) */
.qc-pipe{display:flex;flex-wrap:nowrap;align-items:stretch;justify-content:center;gap:0;margin-top:4px;overflow-x:auto;padding-bottom:5px}
.qc-blk{width:150px;flex:0 0 auto;border:1px solid var(--bd);border-radius:6px;padding:11px 9px;text-align:center;background:var(--sf);display:flex;flex-direction:column;justify-content:center}
.qc-blk .bl{font-family:ui-monospace,monospace;font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--tx2);font-weight:700}
.qc-blk .bq{font-size:10.5px;margin-top:5px;color:var(--tx2)}
.qc-blk.src{border-color:var(--inst)}.qc-blk.src .bl{color:var(--inst)}
.qc-blk.out{border-color:var(--ind);background:rgba(30,142,62,.1)}.qc-blk.out .bl{color:var(--ind)}
.qc-conn{width:46px;flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center}
.qc-conn .vl{font-size:7.5px;color:var(--tx2);text-align:center;line-height:1.15;margin-bottom:3px;font-style:italic}
.qc-conn .aw{color:var(--law);font-size:17px}
.qc-blk .bsys{font-family:ui-monospace,monospace;font-size:8.5px;color:var(--law);margin-top:3px;letter-spacing:.02em}
/* resultado — el ojo primero */
.qc-hero{margin:4px 0 18px;display:flex;flex-direction:column;gap:11px}
.qc-hbar{display:flex;align-items:center;gap:14px}
.qc-hfill{height:42px;border-radius:6px;display:flex;align-items:center;padding:0 16px;min-width:96px;flex:0 0 auto}
.qc-hfill.g{background:var(--ind)}.qc-hfill.s{background:var(--sin)}
.qc-hnum{font-family:Georgia,serif;font-weight:700;font-size:25px;color:#fff;white-space:nowrap}
.qc-hnum.d{color:#0E1420}
.qc-hlbl{font-size:13px;color:var(--tx);flex:1}.qc-hlbl b{font-weight:700}
.qc-esp-h{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--tx2);margin:6px 0 9px}
.qc-row{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.qc-lbl{width:220px;text-align:right;font-size:12px;flex:none;color:var(--tx)}.qc-lbl small{color:var(--tx2)}
.qc-track{flex:1;height:13px}.qc-bar{height:13px;border-radius:2px;min-width:2px}
.qc-num{width:66px;font-family:ui-monospace,monospace;font-size:11.5px;color:var(--tx2);flex:none}.qc-num b{color:var(--tx);font-size:13px}
/* expedientes + mini-cadena */
.qc-exps{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.qc-exp{border:1px solid var(--bd);border-radius:4px;overflow:hidden;background:var(--sf)}
.qc-exp-top{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:6px 11px;background:rgba(255,255,255,.05);border-bottom:1px solid var(--bd)}
.qc-exp-id{font-family:ui-monospace,monospace;font-size:8.5px;letter-spacing:.03em;font-weight:700;color:var(--tx2)}
.qc-stamp{font-family:ui-monospace,monospace;font-size:8.5px;font-weight:700;padding:2px 6px;border:1.5px solid;border-radius:3px;text-transform:uppercase;white-space:nowrap}
.qc-exp-b{padding:9px 11px}
.qc-kv{font-size:11.5px;margin:3px 0;display:flex;gap:8px}
.qc-kv .k{font-family:ui-monospace,monospace;font-size:8.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--tx2);flex:none;width:66px;padding-top:2px}
.qc-kv .v{flex:1;color:var(--tx2)}.qc-kv .v b{color:var(--tx)}
.qc-mc{margin-top:9px;padding-top:8px;border-top:1px dashed var(--bd)}
.qc-mc .mc-t{font-family:ui-monospace,monospace;font-size:8px;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);display:block;margin-bottom:5px}
.qc-mc .mc-row{display:flex;flex-wrap:wrap;align-items:center;gap:4px}
.mc-n{font-size:9.5px;padding:3px 8px;border-radius:3px;border:1px solid var(--bd)}
.mc-n.on{color:#fff;background:rgba(30,142,62,.34);border-color:var(--ind);font-weight:600}
.mc-n.off{color:#AEB8C6;border-color:rgba(255,255,255,.22);background:rgba(255,255,255,.03)}
.mc-a{color:#8894A6;font-size:12px}.mc-a.on{color:var(--ind);font-weight:700}
/* evolución */
.qc-evs{display:grid;grid-template-columns:repeat(auto-fit,minmax(252px,1fr));gap:12px;margin-bottom:14px}
.qc-ev{border:1px solid var(--bd);border-radius:8px;padding:15px 16px;background:var(--sf)}
.qc-ev .ev-l{font-size:12.5px;font-weight:700;margin-bottom:13px;overflow-wrap:normal;word-break:keep-all}
.qc-cap{font-size:11px;color:var(--tx2);line-height:1.5;margin:0 0 12px;font-style:italic}.qc-cap b{color:var(--tx);font-style:normal}
.qc-ev .ev-r{display:flex;align-items:center;gap:10px}
.qc-ev .ev-yr{display:flex;flex-direction:column;gap:1px}
.qc-ev .ev-yr .ev-y{font-family:ui-monospace,monospace;font-size:9px;color:var(--tx2);letter-spacing:.05em}
.qc-ev .ev-yr b{font-family:Georgia,serif;font-size:25px;line-height:1}
.qc-ev .ev-ar{color:var(--law);font-size:17px}
.qc-ev .ev-d{margin-left:auto;font-family:ui-monospace,monospace;font-size:12px;font-weight:700;border:1px solid;border-radius:12px;padding:2px 9px;white-space:nowrap}
@media(max-width:720px){.qc-evs{grid-template-columns:1fr}}
.qc-ev-h{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--tx2);margin:2px 0 8px}
.qc-evt{width:100%;border-collapse:collapse;font-size:11.5px}
.qc-evt th{text-align:left;font-family:ui-monospace,monospace;font-size:9px;letter-spacing:.05em;text-transform:uppercase;color:var(--tx2);font-weight:700;padding:4px 8px;border-bottom:1px solid var(--bd)}
.qc-evt td{padding:5px 8px;border-bottom:1px solid rgba(255,255,255,.05);color:var(--tx2)}
.qc-evt td:first-child{color:var(--tx)}.qc-evt td:nth-child(4){font-family:ui-monospace,monospace;font-weight:700}
/* embudo · nota */
.qc-fnote{margin-top:11px;padding-top:10px;border-top:1px solid var(--bd);font-size:11px;color:var(--tx2);line-height:1.5}
.qc-fnote b{color:var(--tx)}
/* biografía del dato (interoperabilidad · la tesis · UNA sola línea) */
.qc-bio{display:flex;flex-wrap:nowrap;align-items:stretch;justify-content:center;gap:2px 0;margin:4px 0;overflow-x:auto;padding-bottom:3px}
.bio-n{min-width:110px;flex:1 0 auto;max-width:158px;text-align:center;padding:11px 6px;border:1px solid var(--bd);border-radius:7px;background:var(--sf)}
.bio-n .bn{font-family:Georgia,serif;font-size:14px;font-weight:600;color:var(--tx)}
.bio-n .bc{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--law);margin-top:2px;letter-spacing:.02em}
.bio-n .bs{font-size:9px;color:var(--tx2);margin-top:3px;line-height:1.25}
.bio-n.last{border-color:var(--ind);background:rgba(30,142,62,.1)}.bio-n.last .bn{color:var(--ind)}
.bio-a{display:flex;align-items:center;color:var(--law);font-size:14px;padding:0 3px;flex:none}
/* hallazgos calculados */
.qc-hzs{display:flex;flex-direction:column;gap:9px}
.qc-hz{display:flex;gap:12px;align-items:flex-start;padding:11px 13px;border:1px solid var(--bd);border-left-width:3px;border-radius:6px;background:var(--sf)}
.qc-hz .hz-n{font-family:Georgia,serif;font-size:15px;font-weight:700;border:1.5px solid;border-radius:5px;width:34px;height:34px;display:flex;align-items:center;justify-content:center;flex:none}
.qc-hz .hz-t{font-size:13px;font-weight:700;color:var(--tx);margin-bottom:2px}
.qc-hz .hz-d{font-size:11.5px;color:var(--tx2);line-height:1.5}
/* valor demostrativo (expedientes) */
.qc-vd{display:flex;flex-wrap:wrap;align-items:center;gap:6px;padding:6px 11px;background:rgba(255,255,255,.02);border-bottom:1px solid var(--bd)}
.qc-vd-s{font-family:ui-monospace,monospace;font-size:9px;letter-spacing:.03em;text-transform:uppercase;color:var(--tx2)}
.qc-vd-s b{font-family:Georgia,serif;font-size:15px;color:var(--tx);margin-left:3px}
.qc-bdg{font-size:8.5px;color:var(--tx2);border:1px solid var(--bd);border-radius:10px;padding:1px 7px;white-space:nowrap}
/* perfil evolutivo */
.qc-pfs{display:flex;flex-direction:column;gap:6px}
.qc-pf{display:flex;align-items:center;gap:10px}
.qc-pf .pf-l{width:100px;text-align:right;font-size:11.5px;color:var(--tx);flex:none}
.qc-pf .pf-track{flex:1;height:11px;background:rgba(255,255,255,.04);border-radius:2px}
.qc-pf .pf-bar{height:11px;border-radius:2px;background:var(--ind);min-width:2px}
.qc-pf .pf-v{width:36px;font-family:ui-monospace,monospace;font-size:11px;color:var(--tx);flex:none}
.qc-pf .pf-d{width:46px;font-family:ui-monospace,monospace;font-size:10.5px;font-weight:700;flex:none}
/* la rendición en el tiempo (intro) */
.qc-serie{width:100%;border-collapse:collapse;font-size:12px;margin:4px 0 6px}
.qc-serie th{text-align:left;font-family:ui-monospace,monospace;font-size:9px;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);font-weight:700;padding:6px 10px;border-bottom:1px solid var(--bd)}
.qc-serie td{padding:7px 10px;border-bottom:1px solid rgba(255,255,255,.05);color:var(--tx2)}
.qc-serie td:first-child{color:var(--tx);font-weight:600}
.qc-serie .num{text-align:right;font-family:ui-monospace,monospace}
.qc-att-h{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--tx2);margin:16px 0 8px}
.qc-atts{display:flex;align-items:flex-end;gap:24px;justify-content:center;padding:6px 0 2px}
.qc-att{display:flex;flex-direction:column;align-items:center;gap:5px;min-width:60px}
.qc-att-bar{width:50px;background:linear-gradient(180deg,#3AA6D6,#1A73E8);border-radius:3px 3px 0 0}
.qc-att-n{font-family:Georgia,serif;font-size:16px;font-weight:700;color:var(--tx)}
.qc-att-y{font-family:ui-monospace,monospace;font-size:10px;color:var(--tx2)}
.qc-tbl-wrap{max-height:340px;overflow-y:auto;border:1px solid var(--bd);border-radius:7px;margin-top:4px}
.qc-tbl-wrap .qc-serie{margin:0}
.qc-tbl-wrap .qc-serie th{position:sticky;top:0;background:#141b28;z-index:1}
.qc-tbl-wrap .qc-serie td:nth-child(2){color:var(--tx2)}
/* implicaciones */
.qc-impl{margin-top:16px;padding:14px 16px;border:1px solid var(--bd);border-left:3px solid var(--law);border-radius:7px;background:var(--sf)}
.qc-impl-t{font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--law);font-weight:700;margin-bottom:6px}
.qc-impl-b{font-family:Georgia,serif;font-size:14px;line-height:1.55;color:var(--tx)}
/* síntesis + placa */
.qc-sint{margin:30px 0 0;border:1.5px solid var(--ind);border-radius:7px;overflow:hidden}
.qc-sint-lbl{font-family:Georgia,serif;font-size:16px;font-weight:700;background:rgba(30,142,62,.14);color:var(--ind);padding:12px 18px;border-bottom:1px solid rgba(30,142,62,.35)}
.qc-sint-b{padding:16px 18px}
.qc-sr{display:flex;gap:12px;margin-bottom:8px;font-size:13px}.qc-sr b{flex:none;width:70px;font-weight:700}.qc-sr span{color:var(--tx2)}
.qc-fuente{font-family:ui-monospace,monospace;font-size:10px;color:var(--tx2);margin-top:12px;line-height:1.6}
.qc-placa{margin:20px 26px 24px;padding:20px;border:1px solid var(--bd);border-radius:5px;text-align:center;background:var(--sf)}
.qc-placa-q{font-family:Georgia,serif;font-size:18px;font-weight:600;line-height:1.4;color:var(--tx)}
.qc-placa-s{font-size:12px;color:var(--tx2);margin-top:9px}
@media(max-width:640px){.qc-exps,.qc-evs{grid-template-columns:1fr}.qc-lbl{width:150px}}
</style>"""
_CSS = _CSS.replace("</style>", PROV_CSS + _FOLD_CSS + "</style>")   # proveniencia + tabla plegable (compartido)


if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path
    snapdir = Path(__file__).resolve().parents[3] / "data" / "motor_narrativo" / "snapshots"
    año = sys.argv[1] if len(sys.argv) > 1 else "2025"

    def _load(a):
        p = snapdir / f"verificabilidad_{a}.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    snap = _load(año)
    serie = [s for s in (_load("2024"), _load("2025")) if s]
    serie = [s for s in serie if int(s["meta"]["año"]) <= int(año)]  # no “ver el futuro”
    out = snapdir / f"cajon_{año}.html"
    out.write_text(cajon_verificabilidad(snap, serie), encoding="utf-8")
    print(f"HTML del cajón {año} → {out} ({out.stat().st_size} bytes)")
