# -*- coding: utf-8 -*-
"""
mandato_render — cajón del DOM d03 · Gobernanza del Mandato (Dylus Lab © 2026).

LA PALABRA EMPEÑADA. Qué proporción de lo que el candidato prometió ante el CNE se
convirtió en meta del plan de desarrollo — y con qué nivel de prueba documental.

DOS CAPAS (acuerdo Javo + colega · 2026-07-15):
  CAPA 1 · el ÍNDICE oficial del dominio → lo calcula el MOTOR; aquí solo se lee y se explica.
  CAPA 2 · la BIOGRAFÍA del mandato → muestra el recorrido completo (promesa→plan→POA→
           presupuesto→ejecución→resultado) REFERENCIANDO cada eslabón al dominio donde se
           mide. NO recalcula: eso sería el motor paralelo prohibido (Regla 4).

PRINCIPIO RECTOR: tener meta asignada ≠ estar verificada. Los tres niveles se declaran.
Firewall: jamás "IFE"/"Score_IFE"/"silo"/H-codes hacia afuera.
"""
from __future__ import annotations

try:
    from app.viz.render.html_render import _CSS as _BASE_CSS, _esc, _seccion
    from app.viz.render.provenance import prov, prov_leyenda, PROV_CSS
except ImportError:  # ejecución directa
    from html_render import _CSS as _BASE_CSS, _esc, _seccion       # type: ignore
    from provenance import prov, prov_leyenda, PROV_CSS             # type: ignore

_COL = "#F9AB00"   # color propio del dominio (ámbar · el mandato)

_D03_CSS = (
    ".qc.d3{--ind:" + _COL + "}"  # identidad ámbar: tiñe los acentos ESTRUCTURALES (nº de sección,
    # borde de la pregunta). Los semáforos ✓/✗ usan color hardcoded → conservan su significado.
    ".d3-hero{border:1px solid var(--bd);border-left:3px solid " + _COL + ";border-radius:9px;padding:15px 17px;margin:10px 0;background:var(--sf)}"
    ".d3-hero-h{display:flex;align-items:baseline;justify-content:space-between;gap:12px;flex-wrap:wrap}"
    ".d3-hero-t{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--tx)}"
    ".d3-hero-v{font-family:ui-monospace,monospace;font-size:30px;font-weight:900;color:" + _COL + ";line-height:1}"
    ".d3-hero-c{font-size:11px;color:var(--tx2);margin-top:2px}"
    ".d3-bar{position:relative;height:10px;border-radius:5px;background:var(--bd);margin:11px 0 3px;overflow:visible}"
    ".d3-bar .f{display:block;height:100%;border-radius:5px;background:" + _COL + "}"
    ".d3-bar .u{position:absolute;top:-3px;bottom:-3px;width:2px;background:var(--tx);opacity:.8;border-radius:1px}"
    ".d3-esc{display:flex;justify-content:space-between;font-family:ui-monospace,monospace;font-size:8px;color:var(--tx2)}"
    # niveles de verificabilidad
    ".d3-niv{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin:10px 0 4px}"
    ".d3-nivc{border:1px solid var(--bd);border-left-width:3px;border-radius:7px;padding:10px 12px;background:var(--sf)}"
    ".d3-nivc .n{font-family:ui-monospace,monospace;font-size:22px;font-weight:900;line-height:1}"
    ".d3-nivc .k{font-family:ui-monospace,monospace;font-size:8px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--tx2);margin-top:3px}"
    ".d3-nivc .x{font-size:10.5px;color:var(--tx2);line-height:1.4;margin-top:5px}"
    # registro de promesas
    ".d3-tab{width:100%;border-collapse:collapse;font-size:11px;margin-top:8px}"
    ".d3-tab th{font-family:ui-monospace,monospace;font-size:8px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);text-align:left;padding:5px 7px;border-bottom:1px solid var(--bd)}"
    ".d3-tab td{padding:5px 7px;border-bottom:1px solid rgba(255,255,255,.04);color:var(--tx);vertical-align:top}"
    ".d3-tab tr:hover td{background:rgba(249,171,0,.05)}"
    ".d3-pill{display:inline-block;font-family:ui-monospace,monospace;font-size:8px;font-weight:800;padding:1px 6px;border-radius:9px;white-space:nowrap}"
    ".d3-eje{display:inline-block;font-size:9.5px;color:var(--tx2);border:1px solid var(--bd);border-radius:9px;padding:1px 7px;margin:0 5px 4px 0}"
    # biografía del mandato
    ".d3-bio{display:flex;flex-wrap:nowrap;align-items:stretch;gap:0;border:1px solid var(--bd);border-radius:8px;padding:11px;margin:9px 0;background:var(--sf);width:100%;overflow-x:auto}"
    ".d3-bn{flex:1 1 0;min-width:104px;border-radius:6px;padding:8px 9px;text-align:center;background:rgba(249,171,0,.09)}"
    ".d3-bn.ref{background:rgba(255,255,255,.03)}.d3-bn.no{background:rgba(217,48,37,.1)}"
    ".d3-bn .s{font-family:ui-monospace,monospace;font-size:7.5px;font-weight:800;letter-spacing:.05em;color:var(--tx2);text-transform:uppercase}"
    ".d3-bn .l{font-size:11px;color:var(--tx);margin-top:3px;line-height:1.25;font-weight:600}"
    ".d3-bn .d{font-size:8.5px;color:var(--tx2);margin-top:2px}"
    ".d3-ba{flex:0 0 auto;display:flex;align-items:center;justify-content:center;color:" + _COL + ";min-width:20px;font-size:13px}"
    "@media(max-width:640px){.d3-niv{grid-template-columns:1fr}}"
)

_CSS = _BASE_CSS.replace("</style>", PROV_CSS + _D03_CSS + "</style>")

_VERDE, _AMBAR, _ROJO = "#1E8E3E", "#F9AB00", "#D93025"


def _ley_esl(d: dict, esl: str, titulo: str) -> str:
    """Marco legal del eslabón desde base_normativa.por_eslabon[esl].marco — MOLDE de d01.
    Los artículos vienen del CORPUS VERIFICADO (sha256) vía `scripts/normativa_mandato.py`;
    aquí solo se leen (Regla 1). Nunca se hardcodean en el render (Regla 9 · Regla 3)."""
    b = ((d.get("base_normativa", {}) or {}).get("por_eslabon", {}) or {}).get(esl) or {}
    arts = b.get("marco") or []
    if not arts:
        return ""
    chips = "".join(f'<span class="qc-lawc">{_esc(a)}</span>' for a in arts)
    return f'<details class="qc-law"><summary>&#128214; {_esc(titulo)}</summary>{chips}</details>'


def _cabecera(d: dict) -> str:
    el = d.get("eleccion") or {}
    sha = el.get("sha256", "")
    return (
        '<p class="qc-p">Toda autoridad llega al cargo con una <b>palabra empeñada</b>: el plan de trabajo que '
        'inscribió ante el <b>Consejo Nacional Electoral</b> para pedir el voto. Ese documento es un '
        '<b>compromiso público verificable</b>, no una pieza de campaña que caduca el día de la elección.</p>'
        '<p class="qc-p">Este dominio hace una sola pregunta, y la hace en serio: <b>¿qué pasó con esa palabra '
        'después de ganar?</b> No mide si la obra se construyó —eso se mide aguas abajo—: mide si el compromiso '
        '<b>encontró correspondencia</b> en la planificación institucional. Una promesa que no llegó al plan '
        'quedó, por ahora, en el discurso.</p>'
        # CORRECCIÓN (colega · 2026-07-16): la versión previa decía "una meta que nadie prometió carece de
        # mandato". Es inconstitucional: una meta nacida del diagnóstico técnico tiene mandato —el del
        # Art. 264— aunque no tenga mandato ELECTORAL. Javo ya había corregido esta doctrina; la frase
        # había sobrevivido en el texto. La medición es unidireccional: promesa → ¿llegó al plan?
        '<p class="qc-p">La lectura inversa <b>no aplica</b>: que una meta no provenga de una promesa electoral '
        '<b>no es una irregularidad</b>. Muchas nacen legítimamente del <b>diagnóstico técnico</b> del plan y del '
        'deber constitucional de planificar el desarrollo cantonal.</p>'
        f'<p class="qc-cap">Documento fuente: <b>{_esc(el.get("documento", ""))}</b> · elección '
        f'<b>{el.get("anio", "")}</b> · período <b>{_esc(el.get("periodo", ""))}</b> · huella de integridad '
        f'<code>{_esc(sha)}</code> — el archivo auditado es exactamente este, y cualquier alteración lo delata.</p>')


def _indice(d: dict) -> str:
    """CAPA 1 · el índice oficial. Lo calcula el MOTOR; aquí se lee y se explica (Regla 1/4)."""
    cal = d.get("calidad") or {}
    pct = cal.get("pct") or 0
    clasif = _esc(cal.get("clasificacion", ""))
    escala = cal.get("escala") or []
    esc_txt = " · ".join(f'{_esc(e.get("umbral",""))} {_esc(e.get("nivel",""))}' for e in escala[:3])
    return (
        '<p class="qc-p">La <b>fidelidad del mandato</b> no cuenta promesas: las <b>pondera</b>. Una promesa puede '
        'entrar al plan de forma <b>directa</b>, <b>con matices</b> o solo <b>parcial</b>, y no es honesto que las '
        'tres pesen igual. El índice mide, con esa ponderación, cuánto del mandato sobrevivió al pasar al plan:</p>'
        f'<div class="d3-hero"><div class="d3-hero-h"><div>'
        f'<div class="d3-hero-t">Fidelidad del mandato electoral</div>'
        f'<div class="d3-hero-c">{clasif}</div></div>'
        f'<div class="d3-hero-v">{pct:.1f}%</div></div>'
        f'<div class="d3-bar"><span class="f" style="width:{min(max(pct,0),100):.0f}%"></span>'
        f'<span class="u" style="left:85%"></span></div>'
        f'<div class="d3-esc"><span>0%</span><span>umbral de fidelidad alta: 85%</span><span>100%</span></div>'
        f'</div>'
        f'<p class="qc-cap">Escala oficial: {esc_txt}. El valor lo calcula el motor del modelo; este expediente '
        f'lo <b>lee y lo explica</b> — no lo recalcula.</p>')
    # NOTA INTERNA (Javo · 2026-07-16 · Regla 2): aquí NO se narra la cocina. La no-comparabilidad
    # con la serie anterior y el porqué (registro depurado) son historia de CONSTRUCCIÓN nuestra:
    # viven en OBS-010 y ADR-036, no en el producto. El DOM publica el resultado curado, no el
    # diario de obra. Contarlo aquí solo sembraría dudas sobre QUIRA sin aportar nada sobre el GAD.


def _niveles(d: dict) -> str:
    """La joya del dominio: el nivel de PRUEBA de cada afirmación (Principio Rector)."""
    inc = d.get("incorporacion") or {}
    ver, pend, sin = inc.get("verificadas", 0), inc.get("pendientes", 0), inc.get("sin_meta", 0)
    tot = inc.get("total", 0)
    # Rótulos prudentes (colega · 2026-07-16): "sin correspondencia" a secas suena definitivo;
    # lo exacto es que no se identificó dentro del universo auditado.
    filas = [
        (ver, "Correspondencia verificada", _VERDE,
         "contrastada contra el documento electoral: hay prueba documental de que el compromiso "
         "encontró su meta en la planificación"),
        (pend, "Pendiente de contraste", _AMBAR,
         "el registro le asigna una meta, pero ese vínculo aún no se contrastó contra el documento"),
        (sin, "Sin correspondencia identificada", _ROJO,
         "no se identificó ninguna meta que la recoja <b>dentro del universo auditado</b>"),
    ]
    cel = "".join(f'<div class="d3-nivc" style="border-left-color:{c}">'
                  f'<div class="n" style="color:{c}">{n}</div><div class="k">{_esc(k)}</div>'
                  f'<div class="x">{x}</div></div>' for n, k, c, x in filas)
    # NOTA (colega · Regla 2): se retiró "aquí este expediente se aplica a sí mismo el estándar…".
    # Hablaba de QUIRA; el lector vino a evaluar al municipio, no al observatorio. Eso es interno.
    return (
        '<p class="qc-p"><b>Tener una meta asignada no es lo mismo que tener la correspondencia probada.</b> '
        f'De las <b>{tot} promesas</b>, este es el nivel de prueba de cada afirmación:</p>'
        f'<div class="d3-niv">{cel}</div>')


def _registro(d: dict) -> str:
    """La EVIDENCIA del mandato, bajo demanda (molde de d01 · Primacía Narrativa · patrón qc-ev).
    Una tabla por eje: el lector abre la que le interesa y ve la relación completa —promesa
    literal, meta que la recoge, grado de correspondencia y nivel de prueba—."""
    pr = d.get("promesas") or []
    if not pr:
        return ""
    inc = d.get("incorporacion") or {}
    # agrupar por eje, en el orden del plan de trabajo
    orden, grupos = [], {}
    for p in pr:
        e = p.get("eje", "—")
        if e not in grupos:
            grupos[e] = []
            orden.append(e)
        grupos[e].append(p)

    bloques = ""
    for eje in orden:
        ps = grupos[eje]
        con = sum(1 for p in ps if p.get("meta"))
        filas = ""
        for p in ps:
            tiene = bool(p.get("meta"))
            col = _VERDE if tiene else _AMBAR
            # Rótulos precisos (colega · 2026-07-16): "sin correspondencia" a secas suena definitivo;
            # lo cierto es que no se identificó DENTRO del universo auditado.
            grado = _esc(p.get("tipo", "")) or "—"
            filas += (f'<tr><td class="cod">{_esc(p.get("id",""))}</td>'
                      f'<td>{_esc(p.get("promesa",""))}</td>'
                      f'<td class="cod">{_esc(p.get("meta","")) or "—"}</td>'
                      f'<td style="color:{col}">{grado}</td></tr>')
        bloques += (f'<details class="qc-ev"><summary>{_esc(eje)} · <b>{len(ps)} promesas</b> — '
                    f'{con} con correspondencia documental</summary>'
                    '<div class="qc-evw scroll"><table class="qc-evt"><thead><tr>'
                    '<th>Código</th><th>Promesa literal del plan de trabajo</th>'
                    '<th>Meta que la recoge</th><th>Grado de correspondencia</th></tr></thead>'
                    f'<tbody>{filas}</tbody></table></div></details>')
    return (
        '<p class="qc-p">Cada promesa se contrasta, una a una, contra las metas de la planificación. La tabla de '
        'cada área abre la <b>relación completa</b>: el texto literal comprometido ante el electorado, la meta que '
        'lo recoge y con qué <b>grado</b> lo hace —directo, con matices o parcial—. Ese grado es lo que pondera el '
        'índice: no es lo mismo asumir un compromiso que rozarlo.</p>'
        f'<p class="qc-cap"><b>{len(pr)} promesas</b> · <b>{inc.get("con_meta", 0)}</b> con correspondencia '
        f'documental identificada. Abra el área que le interese:</p>' + bloques)


def _biografia(d: dict) -> str:
    """CAPA 2 · la biografía del mandato. MUESTRA el recorrido; cada eslabón aguas abajo se
    REFERENCIA al dominio que lo mide (ADR-032) — jamás se recalcula aquí (Regla 4)."""
    inc = d.get("incorporacion") or {}
    tot, con = inc.get("total", 0), inc.get("con_meta", 0)
    nodos = [
        ("Promesa", f"{tot} registradas", "documento del CNE · verificado", "ok"),
        # Rótulo preciso (colega): "75 con meta" hacía leer que el plan tiene 75 metas. Lo que
        # decimos es que 75 PROMESAS encontraron correspondencia.
        ("Plan de desarrollo", f"{con} con correspondencia", "medido aquí", "ok"),
        ("Programación", "se mide en Planificación", "otro dominio", "ref"),
        ("Presupuesto", "se mide en Presupuesto", "otro dominio", "ref"),
        ("Ejecución", "se mide en Presupuesto", "otro dominio", "ref"),
        ("Resultado", "sin medición publicada", "ausencia declarada", "no"),
    ]
    chain = '<div class="d3-ba">&#9656;</div>'.join(
        f'<div class="d3-bn {c if c != "ok" else ""}"><div class="s">{_esc(s)}</div>'
        f'<div class="l">{_esc(l)}</div><div class="d">{_esc(dd)}</div></div>'
        for s, l, dd, c in nodos)
    return (
        '<p class="qc-p">Un mandato no se evalúa con un número: se <b>audita siguiendo su recorrido</b>. La promesa '
        'viaja del voto al territorio, y en cada estación puede perderse. Esta es la <b>vida completa del mandato</b> '
        '—y este dominio solo mide las dos primeras estaciones—:</p>'
        f'<div class="d3-bio">{chain}</div>'
        '<p class="qc-cap">Los eslabones intermedios <b>ya se miden en sus propios dominios</b>: este expediente los '
        '<b>referencia</b>, no los recalcula —un número solo puede nacer una vez, o deja de ser confiable—. El último '
        'nodo está en <b>rojo</b>: el municipio no publica medición de resultados, así que <b>la cadena del mandato '
        'no cierra</b>. Se ve; no se rellena.</p>')


def _sintesis(d: dict) -> str:
    cal = d.get("calidad") or {}
    inc = d.get("incorporacion") or {}
    aut = d.get("autoridades") or {}
    pct = cal.get("pct") or 0
    ver, tot = inc.get("verificadas", 0), inc.get("total", 0)
    sin = inc.get("sin_meta", 0)
    # MOLDE de d01 (Javo · 2026-07-16): la síntesis NO es una sección más — es el dictamen, con su
    # estructura propia (qc-sint / qc-sint-lbl / qc-sr-cierre / qc-fuente). Y DICTAMINA: cita lo ya
    # demostrado y emite juicio; no vuelve a explicar lo que el expediente ya probó.
    dictamen = (
        '<div class="qc-sr-cierre">El análisis documental evidencia que <b>el mandato electoral sí se tradujo '
        f'en planificación</b>: <b>{tot - sin}</b> de las <b>{tot} promesas</b> inscritas ante el Consejo Nacional '
        f'Electoral encontraron correspondencia en las metas del plan de desarrollo, y el grado con que lo '
        f'hicieron —ponderado— sitúa la fidelidad en <b>{pct:.1f}%</b>: <b>{_esc(cal.get("clasificacion",""))}</b>, '
        'por debajo del 85% que marca fidelidad alta. <b>El compromiso no se diluyó al pasar del discurso al '
        'documento</b>, que es precisamente lo que exige el deber de planificación del desarrollo y lo que este '
        'dominio verifica. '
        f'La distancia con ese umbral no proviene de promesas olvidadas —solo <b>{sin}</b> no halló correspondencia '
        'identificada— sino del <b>grado</b> con que muchas se incorporaron: recogidas con matices o solo en '
        'parte. <b>La atención del período es preventiva, no correctiva</b>: el mandato está en el plan; lo que '
        'queda por demostrar es su viaje aguas abajo. Dos ausencias acotan el dictamen y ninguna se disimula: '
        f'<b>{aut.get("sin_verificar", 0)} de {aut.get("total", 0)} autoridades electas</b> permanecen sin datos '
        'verificados, y <b>la última etapa de la cadena —el resultado territorial— no puede auditarse</b>: no '
        'existe información pública suficiente para reconstruir documentalmente los resultados obtenidos.</div>')
    # ALCANCE al pie (colega): primero qué mide y el resultado; el alcance al final, como nota
    # metodológica. Antes abría el dominio y hacía pensar "¿entonces no miden todo?".
    nota = ('<p class="qc-cap" style="margin-top:9px"><b>Nota metodológica · alcance.</b> El PDOT vigente '
            'contiene <b>67 metas</b>; la correspondencia se evalúa contra un <b>muestreo estratégico</b> de '
            'ellas —el conjunto que el modelo representa para <b>validación empírica</b> del método—, no contra '
            'el plan de desarrollo en su totalidad. Una promesa cuya meta exista fuera de ese conjunto se '
            'declara <b>fuera de alcance</b> y <b>no se computa como incumplimiento</b> del municipio.</p>')
    return (f'<div class="qc-sint"><div class="qc-sint-lbl">Síntesis ejecutiva del dominio — Gobernanza del '
            f'Mandato Electoral · Montecristi · período 2023–2027</div><div class="qc-sint-b">{dictamen}{nota}'
            f'<div class="qc-fuente">Fuentes: Plan de Trabajo inscrito ante el CNE 2023 (verificado por huella '
            f'documental) · metas del plan de desarrollo · Código de la Democracia Art. 97 · COPLAFIP Art. 41 y '
            f'42.</div></div></div>')


def cajon_mandato(d: dict) -> str:
    return f"""{_CSS}
<section class="qc d3">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio 001</div>
    <div class="qc-idea">Gobernanza del Mandato Electoral</div>
    <div class="qc-q">¿Qué ocurrió con la palabra empeñada ante el electorado una vez ganada la elección?</div>
  </div>
  <div class="qc-body">
    {prov_leyenda()}
    {_seccion('01', 'Comprender este dominio · la palabra empeñada', _cabecera(d), _ley_esl(d, 'compromiso', 'Fundamento del dominio (Mandato Electoral)'))}
    {_seccion('02', 'La fidelidad del mandato · el índice y su nivel de prueba', _indice(d) + _niveles(d), _ley_esl(d, 'traduccion', 'Fundamento jurídico aplicable'), prov=prov('ana'))}
    {_seccion('03', 'El registro del mandato · promesa por promesa, con su evidencia', _registro(d), _ley_esl(d, 'investidura', 'Fundamento jurídico aplicable'), prov=prov('doc'))}
    {_seccion('04', 'La biografía del mandato · del voto al territorio', _biografia(d), _ley_esl(d, 'consecuencia', 'Fundamento jurídico aplicable'), prov=prov('doc'))}
    {_sintesis(d)}
  </div>
  <div class="qc-plate">&#11041; QUIRA &middot; by Dylus Lab</div>
</section>"""


def cajon_mandato_streamlit(d: dict) -> str:
    return cajon_mandato(d)
