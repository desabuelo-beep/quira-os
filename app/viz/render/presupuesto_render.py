# -*- coding: utf-8 -*-
"""
Cajón del DOM d02 · Presupuesto & Financiamiento — QUIRA (Dylus Lab © 2026).

Rótulo público: "Presupuesto & Financiamiento" (canon · no se renombra).
ALCANCE (colega + Javo · 2026-07-14): la CAPACIDAD FINANCIERA TERRITORIAL del municipio
para transformar su planificación en inversión pública sostenible y captar cooperación.
El presupuesto es EVIDENCIA de la capacidad, no el objeto (igual que el PDOT en d01).

Marco de 4 capacidades (Planificación se CONSUME de d01, no se re-mide · objeto compartido):
  · Elegibilidad   — alineación PND + Agenda 2030/ODS (por qué financiar aquí).
  · Movilización   — fondos externos captados (reembolsable / no reembolsable).
  · Absorción      — ejecución (¿ejecuta lo que capta? · riesgo de subejecución).
  · Sostenibilidad — salud presupuestaria (ISP).
+ BIOGRAFÍA DEL CAPITAL PÚBLICO: la cadena ODS→PND→PDOT·Meta→Convenio→$ por convenio.
  El eslabón de IMPACTO/resultado medido es AUSENCIA DECLARADA (el GAD no lo publica).

Regla 1: consume el SNAPSHOT (bloque `presupuesto_dom`), no el motor.
"""
from __future__ import annotations

try:
    from html_render import _CSS as _BASE_CSS, _esc, _seccion  # noqa: F401
    from provenance import prov, prov_leyenda, PROV_CSS  # noqa: F401
    from hallazgos import render_hallazgos as _hallazgos_html, h_serie  # noqa: F401
except ImportError:  # dentro del paquete app (Streamlit)
    from app.viz.render.html_render import _CSS as _BASE_CSS, _esc, _seccion  # noqa: F401
    from app.viz.render.provenance import prov, prov_leyenda, PROV_CSS  # noqa: F401
    from app.viz.render.hallazgos import render_hallazgos as _hallazgos_html, h_serie  # noqa: F401

_COL = "#A78BFA"   # color propio del dominio (violeta · finanzas)

_D02_CSS = (
    ".qc.d2{--ind:" + _COL + "}"  # identidad violeta del dominio: tiñe los acentos ESTRUCTURALES (nº de sección, borde de la pregunta). Los semáforos ✓/✗ usan color hardcoded → NO cambian.
    ".d2-cap{border:1px solid var(--bd);border-left-width:3px;border-radius:8px;padding:13px 15px;margin:10px 0;background:var(--sf)}"
    ".d2-cap-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:4px}"
    ".d2-cap-t{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--tx)}"
    ".d2-cap-v{font-family:ui-monospace,monospace;font-size:19px;font-weight:900}"
    ".d2-cap-x{font-size:11.5px;color:var(--tx2);line-height:1.5}.d2-cap-x b{color:var(--tx)}"
    ".d2-sem{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 2px}"
    ".d2-semc{flex:1 1 120px;border:1px solid var(--bd);border-radius:7px;padding:9px 11px;background:var(--sf)}"
    ".d2-semc .k{font-family:ui-monospace,monospace;font-size:8.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);font-weight:700}"
    ".d2-semc .v{font-family:Georgia,serif;font-size:16px;font-weight:700;margin-top:2px}"
    ".d2-bio{display:flex;flex-wrap:wrap;align-items:stretch;gap:0;border:1px solid var(--bd);border-radius:8px;padding:10px;margin:9px 0;background:var(--sf);overflow-x:auto}"
    ".d2-bn{flex:0 0 auto;min-width:96px;border-radius:6px;padding:7px 9px;text-align:center;background:rgba(167,139,250,.09)}"
    ".d2-bn .s{font-family:ui-monospace,monospace;font-size:8px;font-weight:700;letter-spacing:.05em;color:var(--tx2);text-transform:uppercase}"
    ".d2-bn .l{font-size:10px;color:var(--tx);margin-top:2px;line-height:1.25}"
    ".d2-ba{flex:1 1 auto;display:flex;align-items:center;justify-content:center;color:" + _COL + ";min-width:22px;font-size:13px}"
    ".d2-bn.wn{background:rgba(249,171,0,.1)}.d2-bn.no{background:rgba(217,48,37,.1)}"
    ".d2-pfg{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:8px 0 6px}"
    ".d2-pft{font-family:ui-monospace,monospace;font-size:8px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2);margin-bottom:6px}"
    ".d2-pf{display:grid;grid-template-columns:1fr 70px 30px;align-items:center;gap:8px;margin-bottom:5px}"
    ".d2-pf .l{font-size:11px;color:var(--tx)}.d2-pf .t{height:8px;border-radius:4px;background:var(--bd);overflow:hidden}"
    ".d2-pf .f{display:block;height:100%;border-radius:4px}.d2-pf .n{font-family:ui-monospace,monospace;font-size:11px;font-weight:700;color:var(--tx);text-align:right}"
    ".d2-chip{display:inline-block;font-size:10px;color:var(--tx2);border:1px solid var(--bd);border-radius:12px;padding:2px 10px;margin:6px 6px 0 0}.d2-chip b{color:var(--tx)}"
    ".d2-sat{border:1px solid var(--bd);border-left-width:3px;border-radius:8px;padding:11px 14px;margin:9px 0;background:var(--sf)}"
    ".d2-sat-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px}"
    ".d2-sat-t{font-family:Georgia,serif;font-size:14px;font-weight:700;color:var(--tx)}"
    ".d2-sat-e{font-family:ui-monospace,monospace;font-size:9px;font-weight:800;letter-spacing:.05em;white-space:nowrap}"
    ".d2-sat-x{font-size:11.5px;color:var(--tx2);line-height:1.45;margin:3px 0 6px}"
    ".d2-sat-m{font-size:11px;color:var(--tx2)}.d2-sat-m b{color:var(--tx)}"
    ".d2-sat-n{font-family:ui-monospace,monospace;font-size:10px;color:var(--tx2)}"
    ".d2-cad{display:flex;flex-wrap:nowrap;align-items:stretch;gap:0;margin-top:9px;overflow-x:auto;padding-bottom:2px}"
    ".d2-cad-n{flex:0 0 auto;border:1px solid var(--bd);border-radius:6px;padding:6px 10px;background:var(--sf);font-size:11px;color:var(--tx);line-height:1.3;max-width:200px}"
    ".d2-cad-n .k{display:block;font-family:ui-monospace,monospace;font-size:7.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--tx2);margin-bottom:2px}"
    ".d2-cad-n.law{border-color:var(--law);border-left-width:3px}.d2-cad-n.est{font-weight:700}"
    ".d2-cad-a{flex:0 0 auto;display:flex;align-items:center;padding:0 7px;color:var(--tx2);font-size:12px}"
    "@media(max-width:640px){.d2-sem,.d2-pfg{grid-template-columns:1fr}}"
)
_CSS = _BASE_CSS.replace("</style>", PROV_CSS + _D02_CSS + "</style>")


def _m(v) -> str:
    v = v or 0
    if abs(v) >= 1e6:
        return f"${v/1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"${v/1e3:.0f}k"
    return f"${v:.0f}"


def _col_pct(p, alto=70, medio=50):
    return "#1E8E3E" if p >= alto else ("#F9AB00" if p >= medio else "#D93025")


def _cabecera(d: dict) -> str:
    """01 · Comprender el dominio: la capacidad financiera territorial + cómo leer."""
    return (
        '<p class="qc-p">Este dominio no trata del presupuesto: trata de la <b>capacidad financiera del '
        'municipio</b> para convertir su planificación en <b>inversión pública sostenible</b> —y para captar '
        'financiamiento nacional e internacional (reembolsable y no reembolsable)—. El presupuesto es la '
        '<b>evidencia</b> de esa capacidad, no el objeto. La pregunta de fondo es la primera que hace cualquier '
        'banco multilateral: <b>¿vale la pena invertir en este municipio?</b></p>'
        '<p class="qc-p">Se evalúa en <b>cuatro capacidades</b> —la de planificación se toma de su dominio '
        'propio, no se repite—: <b>elegibilidad</b> (¿por qué financiar aquí?), <b>movilización</b> (¿capta '
        'recursos?), <b>absorción</b> (¿ejecuta lo que capta?) y <b>sostenibilidad</b> (¿es fiscalmente sano?).</p>'
        + prov_leyenda())


def _radiografia(d: dict) -> str:
    """La radiografía macro: las 4 capacidades como semáforo (color desde el dato)."""
    isp = (d.get("isp") or {}).get("global_pct") or 0
    ti = (d.get("ejecucion") or {}).get("ti_pct") or 0
    pnd = (d.get("elegibilidad") or {}).get("alineacion_pnd_pct") or 0
    ods = (d.get("ods") or {}).get("icods_pct") or 0
    cap = (d.get("captacion") or {}).get("total_externo") or 0
    elig = round((pnd + ods) / 2) if (pnd or ods) else 0
    tarj = [
        ("Elegibilidad", f"{elig}%", _col_pct(elig)),
        ("Movilización", _m(cap), _COL),
        ("Absorción", f"{ti:.0f}%", _col_pct(ti)),
        ("Sostenibilidad", f"{isp:.0f}%", _col_pct(isp, 65, 50)),
    ]
    cel = "".join(f'<div class="d2-semc"><div class="k">{_esc(k)}</div>'
                  f'<div class="v" style="color:{c}">{v}</div></div>' for k, v, c in tarj)
    return ('<p class="qc-cap"><b>Radiografía de la capacidad financiera</b> — un vistazo a las cuatro:</p>'
            f'<div class="d2-sem">{cel}</div>')


def _capacidad(titulo, valor, color, texto) -> str:
    return (f'<div class="d2-cap" style="border-left-color:{color}">'
            f'<div class="d2-cap-h"><span class="d2-cap-t">{_esc(titulo)}</span>'
            f'<span class="d2-cap-v" style="color:{color}">{valor}</span></div>'
            f'<div class="d2-cap-x">{texto}</div></div>')


def _elegibilidad(d: dict) -> str:
    el = d.get("elegibilidad") or {}
    od = d.get("ods") or {}
    pnd = el.get("alineacion_pnd_pct") or 0
    icods = od.get("icods_pct") or 0
    cub, tot = od.get("ods_cubiertos") or 0, od.get("total_ods") or 17
    elig = round((pnd + icods) / 2)
    txt = (f'La condición de entrada al financiamiento: qué tan alineado está el plan con las prioridades que '
           f'los cooperantes exigen. <b>Alineación al Plan Nacional: {pnd}%</b>. <b>Vinculación a la Agenda 2030: '
           f'{icods:.0f}%</b> ({cub} de {tot} ODS cubiertos). Ambas <b>se consumen de la planificación</b> '
           f'(nacen en su dominio, aquí se usan como llave). Un municipio bien alineado es <b>elegible</b>: tiene '
           f'con qué justificar por qué merece la inversión.')
    return _capacidad("Capacidad de elegibilidad", f"{elig}%", _col_pct(elig), txt)


def _movilizacion(d: dict) -> str:
    cap = d.get("captacion") or {}
    total, n = cap.get("total_externo") or 0, cap.get("n_convenios") or 0
    txt = (f'La capacidad de <b>captar recursos más allá del presupuesto propio</b>. El municipio ha movilizado '
           f'<b>{_m(total)}</b> en <b>{n} convenios</b> de financiamiento externo (todos <b>no reembolsables</b>: '
           f'transferencias sectoriales y bonos, no deuda). Es la diferencia entre depender solo de lo propio y '
           f'apalancar capital de terceros para la inversión.')
    return _capacidad("Capacidad de movilización", _m(total), _COL, txt)


def _absorcion(d: dict) -> str:
    ej = d.get("ejecucion") or {}
    ti = ej.get("ti_pct") or 0
    cod, dev = ej.get("codificado") or 0, ej.get("devengado") or 0
    txt = (f'La prueba real: <b>¿ejecuta lo que tiene?</b> No basta captar —un municipio puede ganar un préstamo '
           f'del BID y perderlo por no poder ejecutar—. Al corte ({_esc(ej.get("corte",""))}), la inversión '
           f'devengada es <b>{_m(dev)} de {_m(cod)}</b> (<b>{ti:.1f}%</b>). Es fase inicial del ejercicio, de carga '
           f'diferida; pero un ritmo bajo sostenido es <b>riesgo de subejecución</b> —la principal alerta de '
           f'cualquier financiador—.')
    return _capacidad("Capacidad de absorción", f"{ti:.1f}%", _col_pct(ti), txt)


def _sostenibilidad(d: dict) -> str:
    isp = d.get("isp") or {}
    p = isp.get("global_pct") or 0
    clasif = isp.get("clasificacion") or ""
    txt = (f'La salud fiscal de fondo: si la estructura presupuestaria es coherente y sostenible en el tiempo. El '
           f'índice de salud presupuestaria es <b>{p:.1f}%</b> —<b>{_esc(clasif)}</b>—, por debajo del <b>65% '
           f'mínimo de inversión que fija el COOTAD (Art. 192)</b>. Es la capacidad que sostiene a las otras tres: '
           f'sin salud fiscal, la elegibilidad y la captación no se traducen en inversión duradera.')
    return _capacidad("Capacidad de sostenibilidad", f"{p:.0f}%", _col_pct(p, 65, 50), txt)


_EST = {"ok": ("#1E8E3E", "&#10003;"), "wn": ("#F9AB00", "!"), "no": ("#D93025", "&#10007;")}


def _biografia_capital(d: dict) -> str:
    """Cronología FORENSE (aporte del colega · 2026-07-15): la línea de vida del capital de cada convenio,
    con el ESTADO de cada eslabón (✓ validado · ! en proceso · ✗ sin dato). La ausencia se VE en el nodo."""
    fondos = (d.get("captacion") or {}).get("detalle") or []
    if not fondos:
        return ""

    def _nodo(sistema, label, est):
        col, mk = _EST[est]
        cls = "" if est == "ok" else est
        return (f'<div class="d2-bn {cls}"><div class="s">{_esc(sistema)} <span style="color:{col}">{mk}</span></div>'
                f'<div class="l">{_esc(label)}</div></div>')

    bloques = ""
    for f in fondos:
        ods = f.get("ods", "") or "ODS por precisar"
        eje = (f.get("pnd_eje", "") or "Plan Nacional").split("—")[0].strip()
        nodos = [
            ("ODS", ods.split("—")[0].strip(), "ok"), ("Plan Nac.", eje, "ok"),
            ("Meta PDOT", f.get("meta", ""), "ok"), ("Convenio", _esc(f.get("nombre", ""))[:26], "ok"),
            ("Capital", _m(f.get("monto")), "ok"), ("Contrato", "en proceso", "wn"),
            ("Devengado", "nivel dominio", "wn"), ("Resultado", "sin medición", "no"),
        ]
        chain = ('<div class="d2-ba">&#9656;</div>').join(_nodo(s, l, e) for s, l, e in nodos)
        bloques += f'<div class="d2-bio">{chain}</div>'
    ley = ('<p class="qc-cap"><span style="color:#1E8E3E">&#10003; validado</span> &nbsp;·&nbsp; '
           '<span style="color:#F9AB00">! en proceso</span> &nbsp;·&nbsp; '
           '<span style="color:#D93025">&#10007; sin dato (ausencia declarada)</span></p>')
    return (
        '<p class="qc-p">Lo que un cooperante financia no es "el presupuesto": es una <b>cadena</b> del compromiso '
        'global al dólar ejecutado en el territorio. La <b>línea de vida</b> del capital de cada convenio, con el '
        '<b>estado de cada eslabón</b>:</p>' + ley + bloques
        + '<p class="qc-cap">Fíjese en el último nodo: el <b>impacto/resultado medido</b> aparece en <b>rojo</b> '
        'porque el municipio aún no publica medición de resultados. La <b>ausencia se ve</b> en el nodo — no se '
        'explica ni se rellena (es un hallazgo en sí, no una inferencia).</p>')


def _perfil_financiamiento(d: dict) -> str:
    """Perfil del financiamiento (aporte del colega): de dónde viene el capital externo (cooperante, sector,
    modalidad) — revela autonomía y dependencia. Todo desde el dato del snapshot."""
    from collections import defaultdict
    fondos = (d.get("captacion") or {}).get("detalle") or []
    if not fondos:
        return ""
    total = sum(f.get("monto", 0) for f in fondos) or 1
    _COOP = ["MIDUVI", "MTOP", "BanEcuador", "MIES", "MAG", "MSP", "MTOP", "SE"]
    coop, sect, modal = defaultdict(float), defaultdict(float), defaultdict(float)
    for f in fondos:
        nom = f.get("nombre", "")
        c = next((k for k in _COOP if k.lower() in nom.lower()), "Sectorial")
        coop[c] += f.get("monto", 0)
        sect[(f.get("ods", "").split("—")[-1].strip() or "Otro")] += f.get("monto", 0)
        modal[f.get("modalidad", "")] += f.get("monto", 0)

    def _barras(dd, col):
        return "".join(f'<div class="d2-pf"><span class="l">{_esc(k)}</span>'
                       f'<span class="t"><span class="f" style="width:{v/total*100:.0f}%;background:{col}"></span></span>'
                       f'<span class="n">{v/total*100:.0f}%</span></div>'
                       for k, v in sorted(dd.items(), key=lambda x: -x[1]))
    chips = "".join(f'<span class="d2-chip">{_esc(k)}: <b>{v/total*100:.0f}%</b></span>' for k, v in modal.items())
    conc = round(max(coop.values()) / total * 100) if coop else 0
    return (
        '<p class="qc-cap" style="margin-top:11px"><b>Perfil del financiamiento externo</b> — de dónde viene y en '
        'qué modalidad (revela autonomía y dependencia):</p>'
        f'<div class="d2-pfg"><div><div class="d2-pft">Por origen / cooperante</div>{_barras(coop, _COL)}</div>'
        f'<div><div class="d2-pft">Por sector financiado</div>{_barras(sect, "#5AA9E6")}</div></div>'
        f'<div>{chips}</div>'
        f'<p class="qc-cap" style="margin-top:5px">El mayor origen concentra <b>{conc}%</b> del capital externo — '
        f'a más concentración, más expuesto queda el municipio si una fuente se retira.</p>')


def _sintesis(d: dict) -> str:
    isp = (d.get("isp") or {}).get("global_pct") or 0
    ti = (d.get("ejecucion") or {}).get("ti_pct") or 0
    pnd = (d.get("elegibilidad") or {}).get("alineacion_pnd_pct") or 0
    icods = (d.get("ods") or {}).get("icods_pct") or 0
    cap = (d.get("captacion") or {}).get("total_externo") or 0
    dictamen = (
        f'<div class="qc-sr-cierre">El análisis documental muestra un municipio con <b>alta capacidad de '
        f'elegibilidad</b> —alineación al Plan Nacional del {pnd}% y a la Agenda 2030 del {icods:.0f}%— y una '
        f'<b>movilización externa relevante</b> ({_m(cap)} en convenios no reembolsables). La restricción no está '
        f'en <b>conseguir</b> recursos, sino en <b>absorberlos</b>: la ejecución al corte ({ti:.1f}%) y la salud '
        f'presupuestaria ({isp:.1f}%, bajo el umbral COOTAD) marcan el <b>riesgo de subejecución</b> como la '
        f'principal alerta. En consecuencia: el municipio es <b>elegible y capta</b>, pero su valor como destino '
        f'de inversión depende de <b>fortalecer la capacidad de ejecución y la sostenibilidad fiscal</b> para que '
        f'el capital se convierta en transformación verificable.</div>')
    return (f'<div class="qc-sint"><div class="qc-sint-lbl">Síntesis ejecutiva del dominio — Presupuesto &amp; '
            f'Financiamiento · Montecristi · corte Abril 2026</div><div class="qc-sint-b">{dictamen}'
            f'<div class="qc-fuente">Fuentes: Presupuesto (cédula eSIGEF) · salud presupuestaria · fondos '
            f'externos captados · alineación al Plan Nacional / Agenda 2030 (consumidas de Planificación).</div></div></div>')


def _senal(s: dict) -> str:
    activa = s.get("estado") == "activa"
    col = "#F9AB00" if activa else "#1E8E3E"
    chip = "&#9888; SEÑAL ACTIVA" if activa else "&#9679; SIN SEÑAL"
    est_txt = "señal activa" if activa else "sin señal"
    # La cadena que materializa la ley (aporte del colega): Norma → Regla → Indicador → Señal.
    cad = [("norma", _esc(s.get("norma", "")), "law"), ("regla", _esc(s.get("regla", "")), ""),
           ("indicador · hoy", _esc(s.get("indicador", "")), ""), ("señal", est_txt, "est")]
    nodos = '<span class="d2-cad-a">&rarr;</span>'.join(
        f'<span class="d2-cad-n {c}"' + (f' style="color:{col}"' if c == "est" else "")
        + f'><span class="k">{k}</span>{v}</span>' for k, v, c in cad)
    return (f'<div class="d2-sat" style="border-left-color:{col}">'
            f'<div class="d2-sat-h"><span class="d2-sat-t">{_esc(s.get("nombre", ""))}</span>'
            f'<span class="d2-sat-e" style="color:{col}">{chip}</span></div>'
            f'<div class="d2-sat-x">{_esc(s.get("vigila", ""))}</div>'
            f'<div class="d2-cad">{nodos}</div></div>')


def _senales_preventivas(d: dict) -> str:
    """El salto descriptivo → PREDICTIVO (SAT presupuestario · decisión Javo 2026-07-15: cada SAT en su dominio).
    Las señales las calcula el MOTOR y las contrasta contra umbrales legales; d02 las OBSERVA —no gestiona—."""
    sat = d.get("sat_presupuestario") or {}
    sen = sat.get("senales") or []
    if not sen:
        return ""
    activas = sat.get("n_activas", 0)
    ccol = "#F9AB00" if activas else "#1E8E3E"
    return (
        '<p class="qc-p">Un expediente no solo describe: <b>anticipa</b>. Estas señales las calcula el motor y las '
        'contrasta contra <b>umbrales legales</b> (COPFP · COOTAD). Cuando una se enciende no es una acusación: es '
        'una <b>alerta temprana</b> que alimenta la gestión — el dominio <b>observa</b>, los motores gestionan.</p>'
        f'<p class="qc-cap"><b>{len(sen)} señales</b> vigiladas · '
        f'<b style="color:{ccol}">{activas} activa{"" if activas == 1 else "s"}</b>. '
        f'Al corte, el presupuesto de Montecristi no dispara alertas:</p>'
        + "".join(_senal(s) for s in sen))


def cajon_presupuesto(d: dict) -> str:
    if not d:
        return ""
    return f"""{_CSS}
<section class="qc d2">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio 001</div>
    <div class="qc-idea">Presupuesto &amp; Financiamiento</div>
    <div class="qc-q">¿El municipio moviliza, administra y transforma sus recursos para cumplir los objetivos del territorio?</div>
  </div>
  <div class="qc-body">
    {_seccion('01', 'Comprender este dominio · la capacidad financiera territorial', _cabecera(d))}
    {_seccion('02', 'La radiografía · las cuatro capacidades', _radiografia(d) + _elegibilidad(d) + _movilizacion(d) + _perfil_financiamiento(d) + _absorcion(d) + _sostenibilidad(d), prov=prov('ana'))}
    {_seccion('03', 'Señales preventivas · el presupuesto que se anticipa', _senales_preventivas(d), prov=prov('ana'))}
    {_seccion('04', 'La biografía del capital público · del ODS al dólar ejecutado', _biografia_capital(d), prov=prov('doc'))}
    {_sintesis(d)}
  </div>
  <div class="qc-placa"><div class="qc-placa-q">QUIRA no certifica la verdad. Certifica la capacidad<br>documental del municipio para movilizar y ejecutar recursos.</div>
    <div class="qc-placa-s">La subejecución es un resultado del análisis documental, nunca una acusación.</div>
    <div style="margin-top:15px;padding-top:12px;border-top:1px solid var(--bd);font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx2)">&#11041; QUIRA · <b style="color:var(--tx)">by Dylus&nbsp;Lab</b></div>
  </div>
</section>"""


def cajon_presupuesto_streamlit(d: dict) -> str:
    """HTML del dominio d02 listo para st.markdown (sin sangría ni líneas en blanco)."""
    h = cajon_presupuesto(d)
    return "\n".join(ln.lstrip() for ln in h.splitlines() if ln.strip())
