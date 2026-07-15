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
    "@media(max-width:640px){.d2-sem{flex-direction:column}}"
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


def _biografia_capital(d: dict) -> str:
    """La cadena del capital: por cada convenio, ODS→PND→PDOT·Meta→Convenio→$. Impacto = ausencia declarada."""
    fondos = (d.get("captacion") or {}).get("detalle") or []
    if not fondos:
        return ""
    bloques = ""
    for f in fondos:
        ods = f.get("ods", "") or "ODS por precisar"
        eje = (f.get("pnd_eje", "") or "Plan Nacional").split("—")[0].strip()
        nodos = [("ODS", ods), ("Plan Nacional", eje), ("PDOT · meta", f.get("meta", "")),
                 ("Convenio", _esc(f.get("nombre", ""))[:34]), ("Capital", f'{_m(f.get("monto"))} · {f.get("modalidad","")}')]
        chain = ('<div class="d2-ba">&#9656;</div>').join(
            f'<div class="d2-bn"><div class="s">{_esc(s)}</div><div class="l">{_esc(l)}</div></div>' for s, l in nodos)
        bloques += f'<div class="d2-bio">{chain}</div>'
    return (
        '<p class="qc-p">Lo que un cooperante realmente financia no es "el presupuesto": es una <b>cadena</b> que '
        'va del compromiso global al dólar ejecutado en el territorio. Esta es la <b>biografía del capital</b> de '
        'cada convenio —del ODS que lo justifica al recurso comprometido—:</p>'
        + bloques
        + '<p class="qc-cap">El último eslabón —el <b>impacto territorial medido</b> y el <b>ODS efectivamente '
        'alcanzado</b>— es hoy una <b>ausencia declarada</b>: el municipio aún no publica medición de resultados. '
        'Es hacia dónde se cierra el ciclo, no lo que hoy se demuestra. QUIRA lo señala, no lo inventa.</p>')


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


def cajon_presupuesto(d: dict) -> str:
    if not d:
        return ""
    return f"""{_CSS}
<section class="qc">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio 001</div>
    <div class="qc-idea">Presupuesto &amp; Financiamiento</div>
    <div class="qc-q">¿El municipio moviliza, administra y transforma sus recursos para cumplir los objetivos del territorio?</div>
  </div>
  <div class="qc-body">
    {_seccion('01', 'Comprender este dominio · la capacidad financiera territorial', _cabecera(d))}
    {_seccion('02', 'La radiografía · las cuatro capacidades', _radiografia(d) + _elegibilidad(d) + _movilizacion(d) + _absorcion(d) + _sostenibilidad(d), prov=prov('ana'))}
    {_seccion('03', 'La biografía del capital público · del ODS al dólar ejecutado', _biografia_capital(d), prov=prov('doc'))}
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
