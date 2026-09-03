# -*- coding: utf-8 -*-
"""
Cajón del DOM d08 · Participación Ciudadana — QUIRA (Dylus Lab © 2026).

Rótulo público: "Participación Ciudadana" (canon · no se renombra).
ALCANCE (catálogo d08 v1.0.0 · Javo · 2026-07-23): la participación NO se mide por la
existencia del mecanismo. Se mide en TRES dimensiones, y la tercera es la que decide:

  1. INTEGRIDAD NORMATIVA   (RO-VIII-001) — ¿existe / se instaló / se documentó?
  2. VITALIDAD DEMOCRÁTICA  (RO-VIII-002) — ¿cuántos participaron, con qué diversidad?  [DISEÑO]
  3. EFECTIVIDAD/INCIDENCIA (RO-VIII-003) — ¿lo pedido se volvió POA / presupuesto / obra?

DOCTRINA QUE GOBIERNA ESTE CAJÓN (la que evita el lenguaje acusatorio · Regla 2):
una demanda sin correspondencia NO prueba desatención — prueba que el expediente no la
acredita. Por eso el resultado se presenta SIEMPRE partido en sus dos causas:
  (a) inverificable por el instrumento — la demanda nombra un lugar y el plan operativo
      declara territorio en el 1,1% de sus filas (OBS-020): la vía de verificación está
      cerrada por el propio instrumento, no por la gestión.
  (b) sin correspondencia temática acreditada — ningún proyecto con objeto compatible.

FRONTERA d08/d09 (corrección de naturaleza · Javo): los aportes de este dominio emanan
de las INSTANCIAS de participación (actas de presupuesto participativo, audiencias,
cabildos). Los aportes al informe de rendición son control social — viven en su dominio.

POR QUÉ NO SE PINTA EL ÍNDICE MADRE: el snapshot trae el vector del motor y el
cajón lo deja fuera a propósito. Publicar un porcentaje cuya composición no se puede
explicar al lector sería un número sin fundamento verificable (Regla 3). Queda en el
bloque para cuando su composición se documente; la radiografía de este dominio son las
tres dimensiones, no una cifra única.

Regla 1: consume el SNAPSHOT (bloque `participacion_dom`), no el motor.

DEUDA TÉCNICA REGISTRADA (CSS · medida, no estimada · 2026-08-05): de las 60 reglas
`.d8-*`, **17 son copia literal de las `.d2-*`** de Presupuesto — dos familias completas:
la cadena `norma → regla → indicador → señal` (`.d8-cad*`) y la cadena de valor público
(`.d8-fl*`). Ya se repiten en DOS dominios, así que corresponde promoverlas a `_CSS` base.
NO se hace ahora, y la razón importa: `_CSS` lo consumen los cuatro cajones en producción,
y tocarlo justo antes de publicar el acumulado convertiría un refactor cosmético en un
riesgo de regresión sobre dominios ya cerrados (Regla 8). Se hace después del despliegue,
con los cuatro cajones verificados. Las otras 43 reglas son propias del dominio: el patrón
de la casa es un prefijo por dominio, y disolverlo acoplaría los cajones entre sí.
"""
from __future__ import annotations

try:
    from html_render import _CSS as _BASE_CSS, _esc, _seccion  # noqa: F401
    from provenance import prov, prov_leyenda, PROV_CSS  # noqa: F401
except ImportError:  # dentro del paquete app (Streamlit)
    from app.viz.render.html_render import _CSS as _BASE_CSS, _esc, _seccion  # noqa: F401
    from app.viz.render.provenance import prov, prov_leyenda, PROV_CSS  # noqa: F401

_COL = "#2BB3A3"   # color propio del dominio (teal · lo cívico)

_D08_CSS = (
    ".qc.d8{--ind:" + _COL + "}"
    # ── las tres dimensiones ──
    ".d8-dims{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:10px 0 4px}"
    ".d8-dim{border:1px solid var(--bd);border-top-width:3px;border-radius:8px;padding:11px 13px;background:var(--sf)}"
    ".d8-dim .n{font-family:ui-monospace,monospace;font-size:8.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2)}"
    ".d8-dim .t{font-family:Georgia,serif;font-size:14.5px;font-weight:700;color:var(--tx);margin:3px 0 4px}"
    ".d8-dim .q{font-size:11px;color:var(--tx2);line-height:1.45;font-style:italic}"
    ".d8-dim .e{font-family:ui-monospace,monospace;font-size:8.5px;font-weight:800;letter-spacing:.05em;margin-top:7px;display:inline-block}"
    # ── instancias (integridad) ──
    ".d8-ins{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin:9px 0 2px}"
    ".d8-in{border:1px solid var(--bd);border-left-width:3px;border-radius:7px;padding:9px 12px;background:var(--sf)}"
    ".d8-in-h{display:flex;align-items:baseline;justify-content:space-between;gap:8px}"
    ".d8-in-t{font-family:Georgia,serif;font-size:13.5px;font-weight:700;color:var(--tx)}"
    ".d8-in-s{font-family:ui-monospace,monospace;font-size:8.5px;font-weight:800;white-space:nowrap}"
    ".d8-in-n{font-family:ui-monospace,monospace;font-size:9px;color:var(--law);margin-top:3px;letter-spacing:.02em}"
    ".d8-in-x{font-size:10.5px;color:var(--tx2);line-height:1.4;margin-top:4px}"
    ".d8-in-nat{font-size:8.5px;color:var(--tx2);border:1px solid var(--bd);border-radius:9px;padding:1px 7px;margin-left:6px;white-space:nowrap;font-family:ui-monospace,monospace;letter-spacing:.03em}"
    # ── barra de dos causas ──
    ".d8-cau{border:1px solid var(--bd);border-radius:8px;padding:13px 15px;background:var(--sf);margin:10px 0}"
    ".d8-cau-b{display:flex;height:34px;border-radius:5px;overflow:hidden;gap:2px;margin:9px 0 10px}"
    ".d8-cau-s{display:flex;align-items:center;justify-content:center;font-family:ui-monospace,monospace;font-size:12px;font-weight:800;color:#0E1420;min-width:34px}"
    ".d8-cau-l{display:flex;flex-direction:column;gap:8px}"
    ".d8-cau-i{display:flex;gap:10px;align-items:flex-start;font-size:11.5px;color:var(--tx2);line-height:1.5}"
    ".d8-cau-i b{color:var(--tx)}"
    ".d8-cau-d{width:11px;height:11px;border-radius:3px;flex:none;margin-top:3px}"
    # ── hero del resultado · el CONTEXTO antes que la cifra de síntesis ──
    ".d8-hero{border:1px solid var(--bd);border-left:3px solid " + _COL + ";border-radius:8px;padding:15px 18px;background:var(--sf);margin:4px 0 12px}"
    ".d8-vol{display:flex;flex-wrap:wrap;gap:26px;margin-bottom:11px}"
    ".d8-vol-i{display:flex;flex-direction:column;gap:1px}"
    ".d8-vol-i .n{font-family:Georgia,serif;font-size:31px;font-weight:700;line-height:1;color:var(--tx)}"
    ".d8-vol-i .l{font-size:10.5px;color:var(--tx2);line-height:1.35;max-width:190px}"
    ".d8-hero-x{font-size:12.5px;color:var(--tx2);line-height:1.55}.d8-hero-x b{color:var(--tx)}"
    ".d8-sint-l{display:flex;align-items:baseline;gap:9px;margin-top:12px;padding-top:11px;border-top:1px solid var(--bd)}"
    ".d8-sint-l .v{font-family:ui-monospace,monospace;font-size:17px;font-weight:800}"
    ".d8-sint-l .t{font-size:11.5px;color:var(--tx2)}"
    # ── tabla de trazabilidad ──
    ".d8-tw{max-height:400px;overflow-y:auto;border:1px solid var(--bd);border-radius:7px;margin-top:8px}"
    ".d8-t{width:100%;border-collapse:collapse;font-size:11.5px}"
    ".d8-t th{position:sticky;top:0;background:#141b28;text-align:left;font-family:ui-monospace,monospace;font-size:8.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);font-weight:700;padding:7px 10px;border-bottom:1px solid var(--bd);z-index:1}"
    ".d8-t td{padding:8px 10px;border-bottom:1px solid rgba(255,255,255,.05);color:var(--tx2);vertical-align:top}"
    ".d8-t td:first-child{color:var(--tx)}"
    ".d8-t .sub{font-size:9.5px;color:var(--tx2);margin-top:2px}"
    ".d8-t .est{font-family:ui-monospace,monospace;font-size:9px;font-weight:800;white-space:nowrap}"
    ".d8-vb{font-size:8.5px;font-family:ui-monospace,monospace;border:1px solid var(--bd);border-radius:9px;padding:1px 6px;white-space:nowrap}"
    # ── vitalidad en diseño ──
    ".d8-vit{border:1px dashed var(--bd);border-radius:8px;padding:13px 16px;background:rgba(255,255,255,.015)}"
    ".d8-vc{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:9px 0 4px}"
    ".d8-vc-i{border:1px solid var(--bd);border-radius:6px;padding:8px 11px}"
    ".d8-vc-i .k{font-size:12px;color:var(--tx);font-weight:600}"
    ".d8-vc-i .d{font-size:10.5px;color:var(--tx2);margin-top:2px;line-height:1.4}"
    ".d8-vc-i .l{font-family:ui-monospace,monospace;font-size:8.5px;color:var(--law);margin-top:4px}"
    ".d8-asis{display:flex;gap:20px;align-items:flex-end;justify-content:center;padding:8px 0 2px;margin-top:8px}"
    ".d8-as{display:flex;flex-direction:column;align-items:center;gap:4px}"
    ".d8-as-b{width:46px;border-radius:3px 3px 0 0;background:linear-gradient(180deg," + _COL + ",#1B7A70)}"
    ".d8-as-n{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--tx)}"
    ".d8-as-y{font-family:ui-monospace,monospace;font-size:9.5px;color:var(--tx2)}"
    # ── señal preventiva ──
    ".d8-sen{border:1px solid var(--bd);border-left-width:3px;border-radius:8px;padding:12px 15px;background:var(--sf)}"
    ".d8-sen-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px}"
    ".d8-sen-t{font-family:Georgia,serif;font-size:14.5px;font-weight:700;color:var(--tx)}"
    ".d8-sen-e{font-family:ui-monospace,monospace;font-size:9px;font-weight:800;letter-spacing:.05em;white-space:nowrap}"
    ".d8-cad{display:flex;flex-wrap:nowrap;align-items:stretch;gap:0;margin-top:10px;width:100%;overflow-x:auto;padding-bottom:2px}"
    ".d8-cad-n{flex:1 1 0;min-width:106px;border:1px solid var(--bd);border-radius:6px;padding:6px 10px;background:var(--sf);font-size:11px;color:var(--tx);line-height:1.3}"
    ".d8-cad-n .k{display:block;font-family:ui-monospace,monospace;font-size:7.5px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--tx2);margin-bottom:2px}"
    ".d8-cad-n.law{border-color:var(--law);border-left-width:3px}.d8-cad-n.est{font-weight:700}"
    ".d8-cad-a{flex:0 0 auto;display:flex;align-items:center;padding:0 7px;color:var(--tx2);font-size:12px}"
    # ── cadena de valor (ubica el dominio) ──
    ".d8-fl{display:flex;flex-wrap:nowrap;align-items:stretch;gap:0;margin:6px 0;width:100%;overflow-x:auto;padding-bottom:2px}"
    ".d8-fl-n{flex:1 1 0;min-width:82px;border:1px solid var(--bd);border-radius:7px;padding:8px 10px;background:var(--sf);text-align:center}"
    ".d8-fl-n .t{display:block;font-family:Georgia,serif;font-size:13px;font-weight:700;color:var(--tx)}"
    ".d8-fl-n .s{display:block;font-size:9px;color:var(--tx2);margin-top:2px}"
    ".d8-fl-a{flex:0 0 auto;display:flex;align-items:center;padding:0 5px;color:var(--tx2);font-size:12px}"
    ".d8-span{position:relative;margin:5px 0 2px;height:24px}"
    ".d8-span .b{position:absolute;left:0;right:0;top:5px;height:3px;border-radius:2px;background:linear-gradient(90deg," + _COL + "22," + _COL + "," + _COL + "22)}"
    ".d8-span .l{position:absolute;left:50%;transform:translateX(-50%);top:10px;background:#0E1420;padding:0 12px;font-family:ui-monospace,monospace;font-size:8.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:" + _COL + "}"
    # ── chips de reparto ──
    ".d8-chip{display:inline-block;font-size:10.5px;color:var(--tx2);border:1px solid var(--bd);border-radius:12px;padding:2px 10px;margin:6px 6px 0 0}.d8-chip b{color:var(--tx)}"
    "@media(max-width:720px){.d8-dims,.d8-ins,.d8-vc{grid-template-columns:1fr}}"
)
_CSS = _BASE_CSS.replace("</style>", PROV_CSS + _D08_CSS + "</style>")

_SEM = {"ok": ("#1E8E3E", "&#10003;"), "wn": ("#F9AB00", "!"), "no": ("#D93025", "&#10007;")}
_NAT = {"estructural": "estructural · la Ley la define",
        "operativa": "operativa · se prueba con actas",
        "mixta": "mixta · norma y operación"}


# ══════════════════════════ 01 · comprender ══════════════════════════
def _cabecera(d: dict) -> str:
    return (
        '<p class="qc-p">Este dominio no pregunta si el municipio <b>tiene</b> mecanismos de participación: '
        'casi todos los tienen, porque la ley los obliga. Pregunta algo más exigente — <b>si esos mecanismos '
        'ejercen incidencia real</b> sobre lo que el municipio termina planificando, presupuestando y '
        'construyendo. La diferencia entre una participación que decide y una que solo se reúne.</p>'
        '<p class="qc-p">Se evalúa en <b>tres dimensiones</b>, en orden de exigencia creciente: que la instancia '
        '<b>exista y esté documentada</b>, que la democracia <b>esté viva</b> (cuánta gente y con qué diversidad) '
        'y —la decisiva— que <b>lo pedido llegue a la ejecución</b>.</p>'
        + prov_leyenda())


def _dimensiones(d: dict) -> str:
    ef = d.get("efectividad") or {}
    integ = d.get("integridad") or {}
    n_ok, n_tot = integ.get("n_documentadas", 0), integ.get("n_total", 0)
    vinc = ef.get("vinculantes") or 0
    sin_c = (ef.get("vinculantes_por_estado") or {}).get("sin_correlato", 0)
    pct_inc = round(100 * (vinc - sin_c) / vinc) if vinc else 0
    dims = [
        ("01", "Integridad normativa", "¿la instancia existe, se instaló y quedó documentada?",
         f"{n_ok} de {n_tot} instancias documentadas", "#1E8E3E"),
        ("02", "Vitalidad democrática", "¿cuánta gente participa y con qué diversidad territorial y social?",
         "dimensión en diseño", "#F9AB00"),
        ("03", "Efectividad e incidencia", "¿lo que la ciudadanía pidió se convirtió en plan, presupuesto y obra?",
         f"{pct_inc}% con correspondencia acreditada", "#D93025" if pct_inc < 40 else "#F9AB00"),
    ]
    tar = "".join(
        f'<div class="d8-dim" style="border-top-color:{c}"><div class="n">Dimensión {n}</div>'
        f'<div class="t">{_esc(t)}</div><div class="q">{_esc(q)}</div>'
        f'<div class="e" style="color:{c}">{_esc(e)}</div></div>' for n, t, q, e, c in dims)
    return f'<div class="d8-dims">{tar}</div>'


def _cadena_estado() -> str:
    fases = [("Promesa", "plan de gobierno"), ("Plan", "PDOT · metas"),
             ("Presupuesto", "asignación de recursos"), ("Ejecución", "contratación · obra"),
             ("Resultado", "bienes y servicios"), ("Territorio", "impacto en la gente")]
    nodos = '<span class="d8-fl-a">&rarr;</span>'.join(
        f'<span class="d8-fl-n"><span class="t">{_esc(t)}</span>'
        f'<span class="s">{_esc(s)}</span></span>' for t, s in fases)
    return (
        '<p class="qc-cap" style="margin-top:12px">La participación ciudadana no ocupa un eslabón de la cadena de '
        'valor público: la <b>atraviesa entera</b>. Es la única dimensión que entra por el principio —cuando la '
        'ciudadanía prioriza— y debe poder rastrearse hasta el final, cuando la obra existe en el territorio. Por '
        'eso se mide a lo largo de toda la cadena, no en un punto:</p>'
        f'<div class="d8-fl">{nodos}</div>'
        '<div class="d8-span"><span class="b"></span><span class="l">la demanda ciudadana debe poder rastrearse '
        'de extremo a extremo</span></div>'
        '<p class="qc-cap">Su prueba es <b>longitudinal</b>: una demanda planteada en una asamblea debe poder '
        'seguirse hasta el plan operativo, el presupuesto y la obra. Donde la trazabilidad se corta, se registra '
        '<b>dónde</b> se cortó — ese es el hallazgo.</p>')


# ══════════════════════════ 02 · integridad ══════════════════════════
def _instancias(d: dict) -> str:
    integ = d.get("integridad") or {}
    ins = integ.get("instancias") or []
    if not ins:
        return ""
    tarjetas = ""
    for i in ins:
        col, mk = _SEM.get(i.get("semaforo", "wn"), _SEM["wn"])
        cob = f'<div class="d8-in-x">{_esc(i["cobertura"])}</div>' if i.get("cobertura") else ""
        tarjetas += (
            f'<div class="d8-in" style="border-left-color:{col}">'
            f'<div class="d8-in-h"><span class="d8-in-t">{_esc(i["nombre"])}</span>'
            f'<span class="d8-in-s" style="color:{col}">{mk} {_esc(i["estado"])}</span></div>'
            f'<div class="d8-in-n">{_esc(i["norma"])}'
            f'<span class="d8-in-nat">{_esc(_NAT.get(i.get("naturaleza"), ""))}</span></div>{cob}</div>')
    return (
        '<p class="qc-p">Las <b>siete instancias y mecanismos</b> que la ley manda, con el estado de su evidencia. '
        'La distinción de la derecha importa: una instancia <b>estructural</b> existe porque la ley la crea —no se '
        'le exige "prueba de existencia"—; una <b>operativa</b> solo se acredita con las actas de sus actos.</p>'
        f'<div class="d8-ins">{tarjetas}</div>'
        '<p class="qc-cap" style="margin-top:11px">La <b>Asamblea Ciudadana</b> aparece con evidencia indirecta por '
        'una razón de fondo, no por un vacío: es una <b>organización ciudadana autónoma</b>, no una dependencia '
        'municipal. Sus archivos no son exigibles al municipio; lo que sí se verifica es que el municipio la '
        '<b>reconozca y articule</b>, y eso consta en las actas de los mecanismos que ella avala.</p>')


def _hallazgo_audiencias(d: dict) -> str:
    h = (d.get("integridad") or {}).get("hallazgo_audiencias") or {}
    n, cita, res = h.get("n", 0), h.get("citan_norma", 0), h.get("con_resolucion", 0)
    if not n:
        return ""
    return (
        f'<div class="d8-cau" style="border-left:3px solid #F9AB00">'
        f'<div style="font-family:Georgia,serif;font-size:14.5px;font-weight:700;color:var(--tx);margin-bottom:5px">'
        f'La audiencia se realiza; su resolución no consta</div>'
        f'<div style="font-size:12px;color:var(--tx2);line-height:1.55">Las <b style="color:var(--tx)">{n} actas</b> '
        f'de audiencia pública del período (2023-2025) invocan expresamente los artículos que las regulan '
        f'—<b style="color:var(--tx)">{cita} de {n}</b>—. Pero la <b style="color:var(--tx)">resolución formal</b> '
        f'que la norma exige como cierre del acto aparece en <b style="color:var(--tx)">{res} de {n}</b>. '
        f'La autoridad estuvo presente en las {n}, de modo que no se trata de delegación.<br><br>'
        f'Es una <b style="color:var(--tx)">brecha entre el cumplimiento narrado y el documental</b>, sostenida '
        f'durante tres años: el acto ocurre y se relata, pero el instrumento que lo vuelve exigible no se emite. '
        f'No es una acusación —es lo que el expediente permite verificar—.</div></div>'
        f'<p class="qc-cap">Fundamento: <b>Ley Orgánica de Participación Ciudadana, artículos 73 a 75</b> '
        f'(la audiencia pública y su resolución).</p>')


# ══════════════════════════ 03 · vitalidad ══════════════════════════
def _vitalidad(d: dict) -> str:
    v = d.get("vitalidad") or {}
    comp = v.get("componentes") or []
    # ⚠️ AQUÍ SE PINTABA LA ASISTENCIA A LAS JORNADAS DE RENDICIÓN (Javo,
    # 2026-09-03). El mismo gráfico —201 · 261 · 322— salía en el cajón de
    # rendición y en éste, y un lector veía «participación creciente» en dos
    # dominios distintos con un dato que sólo pertenece a uno. El acta de
    # rendición es primigenia de d09; aquí no es ni siquiera evidencia del
    # mecanismo que esta dimensión mide.
    #
    # Y el pie afirmaba «el único registro de asistencia disponible». Es falso:
    # 31 actas de mecanismos PROPIOS declaran registro anexo. Lo que falta es su
    # digitalización, no el registro — y decir «no hay» donde hay «hay,
    # escaneado» convierte un límite del instrumento en una ausencia del sujeto.
    expediente = v.get("expediente_propio") or []
    cards = "".join(f'<div class="d8-vc-i"><div class="k">{_esc(k)}</div><div class="d">{_esc(x)}</div>'
                    f'<div class="l">{_esc(l)}</div></div>' for k, x, l in comp)
    serie = ""
    if expediente:
        # ⚠️ SIN F-STRING ANIDADA. La primera versión llevaba comillas simples
        # dentro de una f-string delimitada por comillas simples: legal desde
        # PEP 701 (Python 3.12), y esta máquina corre 3.13 — pero el runner usa
        # 3.11 y no compila. Es el MISMO defecto que ya tumbó un CI el 02-sep,
        # cometido otra vez por el mismo motivo: lo que aquí pasa, allí no.
        # `check_health` lo cazó porque compila contra la versión que el
        # workflow declara; la simulación local no, porque sólo corría pytest.
        def _docs(e):
            n = e.get("n_documentos")
            return f' · {n} documento(s) en expediente' if n else ''

        filas = "".join(
            f'<div class="d8-cau-i"><span class="d8-cau-d" style="background:var(--ind)"></span>'
            f'<div><b>{_esc(e["mecanismo"])}</b> — {_esc(str(e.get("cobertura") or "sin cobertura declarada"))}'
            f'{_docs(e)}</div></div>'
            for e in expediente)
        serie = (f'<p class="qc-cap" style="margin-top:13px">Lo que este dominio SÍ tiene de suyo: el expediente '
                 f'documental de sus propios mecanismos. La asistencia a las jornadas de rendición '
                 f'<b>no se muestra aquí</b> —pertenece al cajón de rendición de cuentas—: presentarla en esta '
                 f'dimensión haría pasar un dato ajeno por una medición propia.</p>'
                 f'<div class="d8-cau-l" style="margin-top:9px">{filas}</div>')
    return (
        '<p class="qc-p">Un mecanismo puede cumplirse en la forma y estar <b>vacío</b>. En un cantón de cerca de '
        'cien mil habitantes, unas decenas de participantes es una señal democrática distinta a la que sugiere el '
        'acta. Esta dimensión mide eso: <b>si la democracia local está viva</b>.</p>'
        f'<div class="d8-vit"><div style="font-family:ui-monospace,monospace;font-size:9px;letter-spacing:.12em;'
        f'text-transform:uppercase;color:#F9AB00;font-weight:700">Dimensión declarada y reservada — '
        f'qué medirá al operacionalizarse</div>'
        f'<div class="d8-vc">{cards}</div>'
        f'<div style="font-size:11.5px;color:var(--tx2);line-height:1.55;margin-top:8px;border-top:1px solid '
        f'var(--bd);padding-top:10px">Esta dimensión <b style="color:var(--tx)">no está vacía: está reservada</b>. '
        f'Sus cuatro dimensiones de medida y su fundamento legal ya están definidos; lo que falta es el índice, y ese '
        f'<b style="color:var(--tx)">se sella en el motor del canon, no en esta pantalla</b> — anticiparlo aquí '
        f'sería inventar una medición. Hay además un obstáculo material declarado: '
        f'<b style="color:var(--tx)">{_esc(v.get("bloqueo", ""))}</b> Mostrar el hueco es parte del método: un '
        f'dominio que oculta lo que aún no mide no es auditable.</div>{serie}</div>'
        '<p class="qc-cap" style="margin-top:11px">Fundamento del mandato de diversidad: <b>Ley Orgánica de '
        'Participación Ciudadana, artículo 57</b> —la composición debe garantizar las diversas identidades '
        'territoriales y la equidad de género y generacional—.</p>')


# ══════════════════════════ 04 · efectividad ══════════════════════════
def _hero_incidencia(d: dict) -> str:
    """El volumen y la naturaleza PRIMERO; el porcentaje al cierre, como síntesis.
    Un número de una cifra abriendo el bloque se lee como veredicto antes de que el lector
    sepa sobre qué universo se calcula — y aquí el universo es justamente lo que hay que
    entender (observación del colega · 2026-08-05)."""
    ef = d.get("efectividad") or {}
    tot = ef.get("total_demandas") or 0
    vinc = ef.get("vinculantes") or 0
    ve = ef.get("vinculantes_por_estado") or {}
    sin_c = ve.get("sin_correlato", 0)
    con = vinc - sin_c
    pct = round(100 * con / vinc) if vinc else 0
    col = "#D93025" if pct < 25 else ("#F9AB00" if pct < 60 else "#1E8E3E")
    vol = [
        (tot, "demandas recogidas en las instancias de participación (2023-2026)"),
        (vinc, "de ellas son <b>jurídicamente exigibles</b> (presupuesto participativo)"),
        (sin_c, "sin correspondencia acreditada <b>en el expediente</b>"),
    ]
    cifras = "".join(f'<div class="d8-vol-i"><span class="n">{n}</span><span class="l">{t}</span></div>'
                     for n, t in vol)
    return (
        f'<div class="d8-hero"><div class="d8-vol">{cifras}</div>'
        f'<div class="d8-hero-x">Esa última cifra debe leerse con precisión, porque de ella depende todo lo '
        f'demás: <b>no dice que esas demandas no se atendieron</b>. Dice que, con los documentos públicos '
        f'disponibles, la correspondencia <b>no puede verificarse</b>. Son dos afirmaciones distintas, y '
        f'confundirlas convertiría una lectura documental en una acusación. El bloque siguiente separa las '
        f'<b>dos causas</b> que producen esa cifra — y solo una de ellas señala a la gestión.</div>'
        f'<div class="d8-sint-l"><span class="v" style="color:{col}">{pct}%</span>'
        f'<span class="t">de correspondencia acreditada sobre lo exigible (<b>{con}</b> de {vinc}) — '
        f'la síntesis, una vez entendido de dónde sale</span></div></div>')


def _dos_causas(d: dict) -> str:
    ef = d.get("efectividad") or {}
    c = ef.get("causas") or {}
    inv, tem = c.get("inverificable_instrumento", 0), c.get("sin_correspondencia_tematica", 0)
    tot = inv + tem
    if not tot:
        return ""
    poa = c.get("poa_localiza_pct", 0)
    p_inv = round(100 * inv / tot)
    segs = (f'<div class="d8-cau-s" style="width:{p_inv}%;background:#5AA9E6">{inv}</div>'
            f'<div class="d8-cau-s" style="width:{100 - p_inv}%;background:#C9782E">{tem}</div>')
    return (
        '<p class="qc-p">Aquí está la distinción que separa explicar una brecha de imputarla. Las '
        f'<b>{tot} demandas</b> sin correspondencia acreditada <b>no son un solo fenómeno</b>: son dos, y tienen '
        'consecuencias opuestas para el municipio.</p>'
        f'<div class="d8-cau"><div class="d8-cau-b">{segs}</div><div class="d8-cau-l">'
        f'<div class="d8-cau-i"><span class="d8-cau-d" style="background:#5AA9E6"></span><span>'
        f'<b>{inv} · inverificables por el instrumento.</b> La demanda nombra un lugar concreto del cantón '
        f'("el sector X", "el barrio Y"), de modo que solo puede darse por atendida si el proyecto declara '
        f'<b>dónde</b> se ejecuta. Pero el plan operativo declara territorio en el <b>{poa}%</b> de sus filas. '
        f'La vía de verificación está cerrada por el propio instrumento de planificación — <b>no por la '
        f'gestión</b>. Aquí el hallazgo no es sobre lo que el municipio hizo: es sobre <b>cómo registra lo que '
        f'hace</b>, y se corrige añadiendo la localización al formato.</span></div>'
        f'<div class="d8-cau-i"><span class="d8-cau-d" style="background:#C9782E"></span><span>'
        f'<b>{tem} · sin correspondencia temática acreditada.</b> Ningún proyecto del plan operativo tiene un '
        f'objeto compatible con lo pedido. Es la señal más cercana a una brecha de atención real, pero <b>tampoco '
        f'la prueba</b>: la demanda pudo atenderse por una vía que el plan no describe —una obra registrada con '
        f'otro nombre, un servicio de operación corriente—.</span></div></div></div>'
        '<p class="qc-cap">La consecuencia práctica de separarlas: la primera se resuelve con una <b>decisión '
        'administrativa</b> —localizar el gasto en el plan operativo— y devolvería verificabilidad a cientos de '
        'demandas de inmediato. La segunda exige revisar la <b>priorización</b>. Confundirlas llevaría a corregir '
        'lo que no está roto.</p>')


def _reparto(d: dict) -> str:
    ef = d.get("efectividad") or {}
    mec, anio = ef.get("por_mecanismo") or {}, ef.get("por_anio") or {}
    tot = ef.get("total_demandas") or 1
    cm = "".join(f'<span class="d8-chip">{_esc(k)}: <b>{v}</b></span>' for k, v in mec.items())
    ca = "".join(f'<span class="d8-chip">{_esc(k)}: <b>{v}</b></span>' for k, v in anio.items())
    return (
        f'<p class="qc-cap" style="margin-top:12px"><b>De dónde salen las {tot} demandas</b> — por mecanismo y por '
        f'año. Solo las del presupuesto participativo son <b>jurídicamente exigibles</b>; las de audiencias y '
        f'cabildos orientan la gestión, y su acogida revela voluntad política, no incumplimiento:</p>'
        f'<div>{cm}</div><div style="margin-top:4px">{ca}</div>')


_EST_LBL = {"hipotesis": ("Correspondencia propuesta", "#5AA9E6"),
            "pendiente_validacion": ("En revisión experta", "#F9AB00"),
            "sin_correlato": ("Sin correspondencia acreditada", "#9AA0A6")}


def _tabla(d: dict) -> str:
    ef = d.get("efectividad") or {}
    filas = ef.get("muestra") or []
    if not filas:
        return ""
    rows = ""
    for f in filas:
        lbl, col = _EST_LBL.get(f["estado"], ("—", "#9AA0A6"))
        vb = ('<span class="d8-vb" style="color:#2BB3A3;border-color:#2BB3A366">exigible</span>'
              if f.get("vinculante") else '<span class="d8-vb">orienta</span>')
        proy = _esc(f["proyecto"]) if f["proyecto"] else (
            '<i style="color:#7E8BA3">— ningún proyecto con objeto compatible en el plan operativo —</i>'
            if not f.get("con_lugar") else
            '<i style="color:#7E8BA3">— la demanda nombra un lugar; el plan no declara territorio —</i>')
        src = f'<div class="sub">{_esc(f["fuente_poa"])}</div>' if f["fuente_poa"] else ""
        rows += (f'<tr><td style="min-width:200px">{_esc(f["demanda"])}'
                 f'<div class="sub">{_esc(f["mecanismo"])} · {_esc(f["anio"])} &nbsp;{vb}</div></td>'
                 f'<td style="min-width:250px">{proy}{src}</td>'
                 f'<td style="text-align:center"><span class="est" style="color:{col}">{_esc(lbl)}</span></td></tr>')
    return (
        '<p class="qc-p">La trazabilidad, demanda por demanda: lo que la ciudadanía pidió en la instancia, junto al '
        'proyecto del plan operativo que le correspondería. Nótese el estado del centro —<b>en revisión '
        'experta</b>—: la máquina <b>propone</b> la correspondencia; un analista la <b>confirma</b>. Ninguna '
        'correspondencia se da por cierta sin ese paso.</p>'
        f'<div class="d8-tw"><table class="d8-t"><thead><tr><th>Demanda ciudadana (instancia de participación)</th>'
        f'<th>Proyecto del plan operativo que le correspondería</th><th style="text-align:center">Estado</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>'
        f'<p class="qc-cap">Muestra representativa de los tres estados, ordenada por proximidad. El expediente '
        f'completo contiene las {ef.get("total_demandas", 0)} demandas contrastadas contra '
        f'{ef.get("registros_poa_contrastados", 0)} registros del plan operativo.</p>')


# ══════════════════════════ 05 · señal ══════════════════════════
def _senal(d: dict) -> str:
    s = d.get("senal") or {}
    if not s.get("denominador"):
        return ""

    # D-006 · SIN UMBRAL ACREDITADO NO HAY VEREDICTO, y eso se DICE.
    # La medición es de d08 y se sostiene sola; el umbral viene de RO-VIII-003,
    # que está en «propuesta». Encender la señal exigiría una autoridad que la
    # regla todavía no tiene. Ocultar el bloque habría convertido «no puedo
    # decidir» en «no hay nada que ver» — el error que este dominio existe para
    # no cometer.
    if s.get("estado_umbral") == "no_consumible" or s.get("umbral") is None:
        return (
            '<p class="qc-p">Esta señal vigila que lo priorizado por la ciudadanía en el '
            'presupuesto participativo se incorpore a la planificación operativa, como manda '
            'la ley. <b>Hoy la medición existe y el umbral que la activaría no está '
            'acreditado</b>, de modo que se publica lo medido y no el veredicto.</p>'
            f'<div class="d8-sen" style="border-left-color:var(--tx3)">'
            f'<div class="d8-sen-h"><span class="d8-sen-t">{_esc(s.get("nombre", ""))}</span>'
            f'<span class="d8-sen-e" style="color:var(--tx3)">&#9679; SIN UMBRAL ACREDITADO</span></div>'
            f'<div style="font-size:11.5px;color:var(--tx2);line-height:1.45;margin:4px 0 2px">'
            f'Medición: <b>{s["numerador"]} de {s["denominador"]}</b> '
            f'({s.get("valor", 0) * 100:.1f}%) sin correspondencia verificable.</div>'
            f'<div style="font-size:11px;color:var(--tx3);line-height:1.45;margin-top:6px">'
            f'{_esc(s.get("por_que", ""))}</div></div>'
            f'<p class="qc-cap" style="margin-top:10px">{_esc(s.get("frontera", ""))}</p>')

    val, umb = s.get("valor", 0), s.get("umbral", 0)
    activa = val >= umb
    col = "#F9AB00" if activa else "#1E8E3E"
    chip = "&#9888; SEÑAL ACTIVA" if activa else "&#9679; SIN SEÑAL"
    cad = [("norma", "COOTAD Art. 238", "law"),
           ("regla", f"{_esc(s['regla'])}", ""),
           ("indicador · hoy", f"{s['numerador']} de {s['denominador']} ({val * 100:.1f}%)", ""),
           ("señal", "activa" if activa else "sin señal", "est")]
    nodos = '<span class="d8-cad-a">&rarr;</span>'.join(
        f'<span class="d8-cad-n {c}"' + (f' style="color:{col}"' if c == "est" else "")
        + f'><span class="k">{k}</span>{v}</span>' for k, v, c in cad)
    return (
        '<p class="qc-p">Un expediente no solo describe: <b>anticipa</b>. Esta señal se enciende cuando más de la '
        'mitad de lo que la ley vuelve exigible no puede verificarse documentalmente. El umbral es deliberadamente '
        '<b>conservador</b>, porque la señal no afirma desatención — afirma <b>no verificabilidad</b>.</p>'
        f'<div class="d8-sen" style="border-left-color:{col}">'
        f'<div class="d8-sen-h"><span class="d8-sen-t">{_esc(s["nombre"])}</span>'
        f'<span class="d8-sen-e" style="color:{col}">{chip}</span></div>'
        f'<div style="font-size:11.5px;color:var(--tx2);line-height:1.45;margin:4px 0 2px">'
        f'Vigila que lo priorizado por la ciudadanía en el presupuesto participativo se incorpore a la '
        f'planificación operativa, como manda la ley.</div>'
        f'<div class="d8-cad">{nodos}</div></div>'
        f'<p class="qc-cap" style="margin-top:10px"><b>Cómo debe leerse esta señal encendida:</b> '
        f'{_esc(s.get("frontera", ""))} Una señal activa no es un dictamen: es una <b>alerta temprana</b> que pide '
        f'revisión — y en este caso la revisión apunta primero al <b>formato del instrumento</b>, no a la '
        f'gestión.</p>')


# ══════════════════════════ síntesis ══════════════════════════
def _sintesis(d: dict) -> str:
    ef = d.get("efectividad") or {}
    integ = d.get("integridad") or {}
    c = ef.get("causas") or {}
    vinc = ef.get("vinculantes") or 0
    sin_c = (ef.get("vinculantes_por_estado") or {}).get("sin_correlato", 0)
    inv, tem = c.get("inverificable_instrumento", 0), c.get("sin_correspondencia_tematica", 0)
    h = integ.get("hallazgo_audiencias") or {}
    dictamen = (
        f'<div class="qc-sr-cierre">El análisis documental muestra un sistema de participación '
        f'<b>formalmente completo</b>: {integ.get("n_documentadas", 0)} de {integ.get("n_total", 0)} instancias '
        f'están instaladas y documentadas, con cobertura de los tres años del período. La distancia aparece al '
        f'pasar de la forma al efecto: de <b>{vinc} demandas ciudadanas exigibles</b>, <b>{sin_c}</b> no tienen '
        f'correspondencia acreditada en la planificación operativa.<br><br>'
        f'Esa cifra, sin embargo, <b>no es un juicio sobre la gestión</b>, y el desglose lo sostiene: '
        f'<b>{inv}</b> de esas demandas son <b>inverificables por el instrumento</b> —nombran un lugar del cantón '
        f'que el plan operativo no registra, porque localiza apenas el {c.get("poa_localiza_pct", 0)}% de su '
        f'gasto—, y solo <b>{tem}</b> carecen además de un proyecto temáticamente compatible. El mismo patrón '
        f'reaparece en las audiencias públicas: {h.get("citan_norma", 0)} de {h.get("n", 0)} actas invocan la '
        f'norma que las regula y {h.get("con_resolucion", 0)} contienen la resolución que esa norma exige.<br><br>'
        f'En conjunto, la lectura es consistente y tiene una consecuencia accionable: <b>la participación de '
        f'Montecristi no falla por ausencia de mecanismos, sino por ausencia de trazabilidad</b>. El municipio '
        f'convoca, delibera y recoge demandas; lo que sus instrumentos no permiten es <b>demostrar qué ocurrió '
        f'después</b>. Y eso —a diferencia de un problema de voluntad— se corrige con una decisión '
        f'administrativa: localizar el gasto en el plan operativo y emitir la resolución que cierra cada '
        f'audiencia.</div>')
    return (f'<div class="qc-sint"><div class="qc-sint-lbl">Síntesis ejecutiva del dominio — Participación '
            f'Ciudadana · Montecristi · corte {_esc(d.get("corte", ""))}</div>'
            f'<div class="qc-sint-b">{dictamen}'
            f'<div class="qc-fuente">Fuentes: informes de presupuesto participativo 2024-2026 · actas de audiencia '
            f'pública 2023-2025 · acta de cabildo popular 2025 · resoluciones del Consejo de Planificación '
            f'2023-2025 · plan operativo anual (archivo oficial) · plan de desarrollo y ordenamiento territorial.'
            f'</div></div></div>')


# ══════════════════════════ ensamblado ══════════════════════════
def cajon_participacion(d: dict) -> str:
    if not d:
        return ""
    return f"""{_CSS}
<section class="qc d8">
  <div class="qc-hd">
    <div class="qc-ey">QUIRA · Observatorio de Integridad Territorial · Municipio 001</div>
    <div class="qc-idea">Participación Ciudadana</div>
    <div class="qc-q">¿Los canales de articulación social ejercen incidencia real en la política institucional, o son un proceso meramente formal?</div>
  </div>
  <div class="qc-body">
    {_seccion('01', 'Comprender este dominio · de la forma al efecto', _cabecera(d) + _dimensiones(d) + _cadena_estado())}
    {_seccion('02', 'Integridad normativa · las instancias que la ley manda', _instancias(d) + _hallazgo_audiencias(d), prov=prov('doc'))}
    {_seccion('03', 'Vitalidad democrática · ¿está viva la participación?', _vitalidad(d), prov=prov('doc'))}
    {_seccion('04', 'Efectividad e incidencia · de lo pedido a lo ejecutado', _hero_incidencia(d) + _dos_causas(d) + _reparto(d) + _tabla(d), prov=prov('ana'))}
    {_seccion('05', 'Señal preventiva · la brecha que se anticipa', _senal(d), prov=prov('ana'))}
    {_sintesis(d)}
  </div>
  <div class="qc-placa"><div class="qc-placa-q">QUIRA no certifica que la demanda ciudadana fue atendida.<br>Certifica si el expediente público permite demostrarlo.</div>
    <div class="qc-placa-s">La ausencia de correspondencia es un resultado del análisis documental, nunca una acusación.</div>
    <div style="margin-top:15px;padding-top:12px;border-top:1px solid var(--bd);font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx2)">&#11041; QUIRA · <b style="color:var(--tx)">by Dylus&nbsp;Lab</b></div>
  </div>
</section>"""


def cajon_participacion_streamlit(d: dict) -> str:
    """HTML del dominio d08 listo para st.markdown (sin sangría ni líneas en blanco)."""
    h = cajon_participacion(d)
    return "\n".join(ln.lstrip() for ln in h.splitlines() if ln.strip())
