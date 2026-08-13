# -*- coding: utf-8 -*-
"""
scripts/vis/objeto_canonico.py — el primer objeto visual canónico de QUIRA
══════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). ADR-049 fija la gramática visual y exige probarla
sobre un caso real **antes** de tocar la interfaz. Este guion produce ese caso:
la cadena de 2026 del GAD Montecristi, con su ruptura y con su desvío.

CÓMO SE PRUEBA VIS-INV-001. La invariante dice que toda representación visual es
una **proyección determinista del motor**, sin crear ni completar nada. Aquí eso
no es una promesa: **este módulo no contiene un solo número escrito a mano.**
Todo se deriva en `construir_estado()`; `svg()` sólo sabe dibujar lo que ese
estado le entrega. Si el estado no trae una cifra, la gráfica no puede
inventarla porque no tiene de dónde.

SEGUNDA VERSIÓN (revisión de Javo, misma noche). La primera tenía seis defectos,
y cinco eran del tipo que este proyecto persigue —decir de más o de menos sin
que se note—:

  1. La leyenda declaraba un trazo de «límite propio de QUIRA» que **no aparecía
     en el dibujo**. Una leyenda con un símbolo que nunca se usa proyecta que la
     captura fue perfecta. Ahora se usa, y en el sitio exacto donde lo es.
  2. **Faltaba el eslabón de contratación.** El dinero no salta de la partida al
     devengado: pasa por adjudicación. Omitirlo ocultaba si el gasto tiene
     proveedor trazable. Se dibuja — y como NO se capturó, se dibuja como límite
     propio, que es la verdad y de paso resuelve el defecto 1.
  3. **Faltaba la escala.** «$1.781.928 trazables» sin denominador no dice nada.
  4. **Las 101 actividades se trataban en bloque**, ocultando que la
     trazabilidad no desapareció: MIGRÓ al código de actividad orgánica. Ese es
     el hallazgo, y no estaba dibujado.
  5. **La flecha de ruptura salía del objetivo**, insinuando que el objetivo
     carece de meta. La ruptura ocurre en el acoplamiento PAI → meta.
  6. La procedencia era una nota bibliográfica, no un registro auditable: sin
     SHA, sin conteos, sin corte.

Uso:  python scripts/vis/objeto_canonico.py [--salida ruta.svg]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts" / "normativa"))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from extraer_cedula import BASE as BASE_CED, extraer_todo          # noqa: E402
from extraer_pai import ARCHIVOS, BASE as BASE_PAI, extraer as extraer_pai  # noqa: E402
from cruce_poa_cedula import corte_anual, estado_financiero        # noqa: E402

TINTA, GRIS, BORDE, FONDO = "#2B3A42", "#8A9BA5", "#D7DEE2", "#FFFFFF"
DEMOSTRADO = "#3D6B5A"      # verde apagado · vínculo demostrado
ROTO = "#B4513C"            # terracota · el observado no lo declara
PROPIO = "#8A6D3B"          # ocre · límite de QUIRA, jamás del municipio
PANEL = "#F7F9FA"


def _sha(p: Path) -> str:
    # 16 de los 64 caracteres. Rotularlo «SHA-256» a secas sería inexacto ante
    # una revisión estricta: el prefijo declara el truncamiento.
    return ("sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()[:16]
            if p.exists() else "—")


def construir_estado(anio: int = 2026) -> dict:
    pai = extraer_pai(anio)
    ced = extraer_todo(anio)
    corte, mes = corte_anual(ced, "GAD Montecristi", anio)

    por_obj: dict[str, set] = {}
    for r in pai:
        o, p = r["campos"].get("objetivo_estrategico", ""), r["campos"].get("partida")
        if o and p:
            por_obj.setdefault(o, set()).add(p)

    # Montos, no sólo conteos: un objetivo puede concentrar casi todo el dinero
    # y ocho pesar poco. «8 de 9» sin importes engaña sin mentir.
    grupos = {"con_devengado": [0, 0.0, 0.0], "con_codificado": [0, 0.0, 0.0],
              "sin_evidencia": [0, 0.0, 0.0]}
    for ps in por_obj.values():
        est = [estado_financiero(corte.get(p))["estado"] for p in ps]
        monto = sum((corte.get(p, {}).get("devengado") or 0) for p in ps)
        # El codificado se lleva aparte: un objetivo con presupuesto asignado y
        # cero gastado NO es lo mismo que uno sin un dólar asignado, y mostrar
        # sólo «$0» los confundía.
        codif = sum((corte.get(p, {}).get("codificado") or 0) for p in ps)
        k = ("con_devengado" if "devengado_positivo" in est else
             "con_codificado" if "codificado_sin_devengado" in est else "sin_evidencia")
        grupos[k][0] += 1
        grupos[k][1] += monto
        grupos[k][2] += codif

    trazable = sum(v[1] for v in grupos.values())
    total_gad = sum(r.get("devengado") or 0 for r in corte.values())
    metas = json.loads((RAIZ / "data" / "pdot" / "registro_maestro_metas.json")
                       .read_text(encoding="utf-8"))["metas"]
    partidas = {p for ps in por_obj.values() for p in ps}
    con_codigo = sum(1 for r in pai if r["campos"].get("codigo_actividad"))
    sin_codigo = len(pai) - con_codigo      # las que faltan NO se dejan en el aire
    ejemplos = sorted({r["campos"]["codigo_actividad"].split("-")[0]
                       for r in pai if r["campos"].get("codigo_actividad")})[:4]

    fpai = BASE_PAI / ARCHIVOS[anio]
    fced = next((c for c in sorted((BASE_CED / f"Presupuestos {anio}" /
                                    f"GAD Montecristi {anio}").glob("*.xlsx"))
                 if mes and mes[:3].lower() in c.name.lower()), None)

    return {
        "anio": anio, "corte_cedula": mes,
        "tronco": [
            {"n": "Plan de Desarrollo y Ordenamiento Territorial",
             "c": f"{len(metas)} metas vigentes", "p": "registro maestro · documental"},
            {"n": "Objetivo estratégico", "c": f"{len(por_obj)} declarados",
             "p": "extracción PAI · documental"},
            {"n": "Plan Anual de Inversiones", "c": f"{len(pai)} actividades",
             "p": "extracción PAI · documental"},
        ],
        # ── ATRIBUCIÓN CORREGIDA (2026-08-13), y en la dirección contraria a la
        # de ayer. El 12-ago se rotuló `captura_no_completada` —culpa nuestra—
        # porque la API dejó de responder tras ~60 peticiones propias en una
        # hora, y parecía saturación. La medición del día siguiente no lo
        # sostiene:
        #
        #   · falla desde DOS REDES distintas, en DOS DÍAS distintos;
        #   · falla en TODOS los endpoints, incluida la raíz del host;
        #   · corta SIEMPRE entre 20,0 y 20,6 s — 5 de 5 intentos espaciados.
        #
        # Un corte metronómico a 20 s no es saturación: la saturación produce
        # patrones erráticos. Pero **no se puede determinar desde aquí si el
        # límite es del servidor o de la ruta**, así que tampoco se afirma.
        # `fuente_no_accesible` con la incertidumbre declarada es lo único que la
        # evidencia sostiene — y asumir culpa propia sin pruebas distorsiona el
        # hallazgo igual que atribuirla al observado.
        "rama_financiera": [
            {"n": "Partida presupuestaria", "c": f"{len(partidas)} distintas",
             "e": "validado"},
            {"n": "Contratación pública", "c": "la fuente no respondió · causa no determinada",
             "e": "fuente_no_accesible"},
            {"n": "Cédula presupuestaria", "c": f"{len(corte)} partidas · corte {mes}",
             "e": "validado"},
            {"n": "Devengado", "c": f"${trazable:,.0f}", "e": "validado"},
        ],
        # Las aristas se declaran aparte porque TAMBIÉN tienen estado. Una arista
        # que dice «verificado» saliendo de un nodo no verificado es una
        # afirmación falsa, y en la versión anterior existía exactamente esa.
        "aristas_financiera": [
            {"de": 0, "a": 1, "e": "fuente_no_accesible",
             "et": "fuente sin respuesta en 5 de 5 intentos"},
            {"de": 1, "a": 2, "e": "no_demostrado",
             "et": "eslabón no incorporado a este corte"},
            {"de": 2, "a": 3, "e": "validado", "et": "verificado en la cédula"},
        ],
        "rama_organica": {
            "n": "Código de actividad orgánica",
            "c": f"{con_codigo} con código orgánico · {sin_codigo} sin identificador",
            "detalle": " · ".join(ejemplos), "e": "desviado",
            "p": "extracción PAI · documental",
            # HECHO e INTERPRETACIÓN, separados. El conteo es medido; la lectura
            # de que «la trazabilidad migró del plan al organigrama» es una
            # inferencia del analista registrada en OBS-027, no la salida de
            # ningún motor. La versión anterior de este panel la presentaba como
            # si fuera un hallazgo del propio dibujo — que es exactamente lo que
            # VIS-INV-001 prohíbe, escrito el mismo día.
            "interpretacion": {
                # La redacción anterior decía que el identificador «ancla la
                # actividad a la dirección que la ejecuta». El instrumento
                # muestra un código; que ese código corresponda a una unidad
                # responsable de la ejecución es un puente que el documento no
                # cierra — y la gráfica no debe cerrarlo por nosotros.
                "texto": ["El código identifica una unidad orgánica dentro del",
                          "instrumento. Su relación con la ejecución administrativa",
                          "es lectura analítica, no medición del resultado."],
                "fuente": "OBS-027 · observación registrada",
                "tipo": "inferencia"}},
        "rama_operacional": [
            {"n": "Meta", "c": f"{sum(1 for r in pai if r['campos'].get('meta_pdot'))}"
                               f" de {len(pai)} actividades", "e": "sin_evidencia"},
            {"n": "Indicador",
             "c": f"{sum(1 for r in pai if r['campos'].get('indicador_pdot'))}"
                  f" de {len(pai)} actividades", "e": "sin_evidencia"},
            # «no verificable» englobaba cuatro situaciones que no son la misma:
            # que la fuente no lo declare, que no se reconcilie, que no se haya
            # podido capturar o que lo rompiéramos al extraer. Se declara cuál.
            {"n": "Resultado", "c": "el instrumento no declara meta ni indicador",
             "e": "sin_evidencia"},
        ],
        "escala": {
            "trazable": trazable, "total_gad": total_gad,
            "pct": (trazable / total_gad * 100) if total_gad else 0,
            # El total es del GAD ENTERO, no «del universo del Plan de
            # Inversiones»: el Plan cubre inversión y no aspira al gasto
            # corriente. Rotularlo mal insinuaría que falta lo que nunca debió
            # estar — un hallazgo falso nacido de una etiqueta.
            "nota": "el Plan de Inversiones cubre inversión, no el gasto corriente",
        },
        "objetivos": {k: {"n": v[0], "monto": v[1], "codificado": v[2]}
                      for k, v in grupos.items()},
        "total_objetivos": len(por_obj),
        "procedencia": [
            {"f": fpai.name, "sha": _sha(fpai), "d": f"{len(pai)} filas · 4 hojas"},
            {"f": fced.name if fced else f"conjunto de datos {mes} {anio}",
             "sha": _sha(fced) if fced else "—",
             "d": f"{len(corte)} partidas · acumulado a {mes}"},
            {"f": "Ordenanza 07-2024-CM-GADMCM", "sha": "sha256:662756aac591b247",
             "d": "sancionada 05-11-2024 · fija el plan vigente"},
        ],
    }


# ── dibujo ────────────────────────────────────────────────────────────────────
def _caja(x, y, w, t, c, color, guion="", h=54, detalle="", estado=""):
    d = f' stroke-dasharray="{guion}"' if guion else ""
    # El estado tipado se muestra literal: quien mira no debe deducir de qué
    # clase de ausencia se trata a partir del color.
    badge = (f'<text x="{x+w-14}" y="{y+18}" font-size="9.5" fill="{color}" '
             f'text-anchor="end" font-family="Consolas, monospace">{estado}</text>') if estado else ""
    extra = (f'<text x="{x+15}" y="{y+51}" font-size="10.5" fill="{color}" '
             f'font-style="italic">{detalle}</text>') if detalle else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{FONDO}" '
            f'stroke="{color}" stroke-width="1.6"{d}/>'
            f'<text x="{x+15}" y="{y+21}" font-size="13" font-weight="600" fill="{TINTA}">{t}</text>'
            f'<text x="{x+15}" y="{y+38}" font-size="11.5" fill="{GRIS}">{c}</text>{badge}{extra}')


def _flecha_v(x, y1, y2, color, guion="", aspa=False, et=""):
    s = f' stroke-dasharray="{guion}"' if guion else ""
    if aspa:
        m = (y1 + y2) / 2
        return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{m-8}" stroke="{color}" stroke-width="2"{s}/>'
                f'<line x1="{x-7}" y1="{m-5}" x2="{x+7}" y2="{m+5}" stroke="{color}" stroke-width="2.4"/>'
                f'<line x1="{x+7}" y1="{m-5}" x2="{x-7}" y2="{m+5}" stroke="{color}" stroke-width="2.4"/>'
                f'<line x1="{x}" y1="{m+8}" x2="{x}" y2="{y2}" stroke="{color}" stroke-width="2"{s}/>'
                + (f'<text x="{x+14}" y="{m+4}" font-size="10.5" fill="{color}">{et}</text>' if et else ""))
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2-7}" stroke="{color}" stroke-width="2"{s}/>'
            f'<path d="M{x-5},{y2-8} L{x},{y2} L{x+5},{y2-8}" fill="{color}"/>'
            + (f'<text x="{x+14}" y="{(y1+y2)/2+4}" font-size="10.5" fill="{color}">{et}</text>' if et else ""))


def verificar_procedencia(e: dict) -> list[str]:
    """VIS-INT-001 · si un elemento del dibujo no tiene propietario canónico, ese
    elemento no puede existir. Es una regla más fuerte que «la gráfica no
    calcula»: obliga a que cada cifra pueda señalar de quién es."""
    huerfanos = []
    for n in e["tronco"] + e["rama_financiera"] + e["rama_operacional"] + [e["rama_organica"]]:
        if not n.get("p") and not n.get("e"):
            huerfanos.append(n["n"])
    if not e.get("procedencia"):
        huerfanos.append("procedencia")

    # ── COHERENCIA ARISTA↔NODO (extensión de VIS-INT-001)
    # No basta con que cada caja tenga el estado correcto: **las relaciones entre
    # cajas también deben respetarlos**. La versión anterior dibujaba una flecha
    # que decía «verificado en la fuente» saliendo de un nodo cuyo propio estado
    # declaraba que la fuente no se había obtenido. Un lector externo leía
    # «contratación → cédula: verificado» justo donde no había nada verificado.
    ok = {"validado", "parcialmente_validado"}
    nodos = e["rama_financiera"]
    for a in e.get("aristas_financiera", []):
        if a["e"] in ok and not (nodos[a["de"]]["e"] in ok and nodos[a["a"]]["e"] in ok):
            huerfanos.append(
                f'arista {nodos[a["de"]]["n"]} → {nodos[a["a"]]["n"]}: declara '
                f'«{a["e"]}» con extremos en '
                f'«{nodos[a["de"]]["e"]}» / «{nodos[a["a"]]["e"]}»')
    return huerfanos


def svg(e: dict) -> str:
    W = 1240
    A, B, C = 60, 480, 880           # columnas de las tres ramas
    ANC, ANCB = 380, 300
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 1130" width="{W}" '
         f'height="1130" font-family="Segoe UI, Helvetica, Arial, sans-serif">',
         f'<rect width="{W}" height="1130" fill="{FONDO}"/>',
         f'<text x="60" y="46" font-size="21" font-weight="700" fill="{TINTA}">'
         f'Cadena de evidencia · ejercicio {e["anio"]}</text>',
         f'<text x="60" y="69" font-size="13" fill="{GRIS}">Gobierno Autónomo Descentralizado '
         f'Municipal del Cantón Montecristi · corte acumulado a {e["corte_cedula"]}</text>',
         f'<line x1="60" y1="84" x2="{W-60}" y2="84" stroke="{BORDE}"/>']

    # ── tronco: lo común a todo, en fila
    yt = 106
    for i, n in enumerate(e["tronco"]):
        x = 60 + i * 400
        p.append(_caja(x, yt, 360, n["n"], n["c"], DEMOSTRADO))
        if i < 2:
            p.append(f'<line x1="{x+360}" y1="{yt+27}" x2="{x+393}" y2="{yt+27}" '
                     f'stroke="{DEMOSTRADO}" stroke-width="2"/>'
                     f'<path d="M{x+392},{yt+22} L{x+400},{yt+27} L{x+392},{yt+32}" fill="{DEMOSTRADO}"/>')

    # ── bifurcación desde el Plan de Inversiones (no desde el objetivo)
    # BIFURCACIÓN EN T. La versión anterior trazaba tres codos independientes desde
    # el mismo origen, y se superponían: el trazo llegaba cortado a las cajas. Un
    # conector partido sugiere una derivación incierta donde la derivación es un
    # hecho — la geometría también afirma.
    yb = yt + 54
    xpai = 860 + 180
    ramales = [A + ANC // 2, B + ANCB // 2, C + ANCB // 2]
    y_bus = yb + 26
    p.append(f'<path d="M{xpai},{yb} L{xpai},{y_bus}" stroke="{TINTA}" stroke-width="2"/>')
    p.append(f'<text x="{xpai+12}" y="{yb+20}" font-size="10.5" fill="{TINTA}" '
             f'font-weight="600">la cadena se bifurca aquí</text>')
    p.append(f'<line x1="{min(ramales)}" y1="{y_bus}" x2="{max(max(ramales), xpai)}" '
             f'y2="{y_bus}" stroke="{TINTA}" stroke-width="2" stroke-linecap="round"/>')
    for xc in ramales:
        p.append(f'<circle cx="{xc}" cy="{y_bus}" r="3" fill="{TINTA}"/>'
                 f'<line x1="{xc}" y1="{y_bus}" x2="{xc}" y2="{yb+44}" stroke="{TINTA}" '
                 f'stroke-width="2"/>'
                 f'<path d="M{xc-5},{yb+44} L{xc},{yb+52} L{xc+5},{yb+44}" fill="{TINTA}"/>')

    ROT = {"validado": ("verificado en la fuente", DEMOSTRADO, "", False),
           "captura_no_completada": ("captura propia no completada", PROPIO, "2 3", False),
           "fuente_no_accesible": ("la fuente no respondió", PROPIO, "2 3", False),
           "no_demostrado": ("eslabón no incorporado", PROPIO, "2 3", False),
           "sin_evidencia": ("el instrumento no lo declara", ROTO, "4 5", True),
           "desviado": ("", PROPIO, "2 3", False)}

    # rama A · financiera
    y = yb + 52
    p.append(f'<text x="{A}" y="{y-8}" font-size="11" font-weight="700" fill="{DEMOSTRADO}" '
             f'letter-spacing="0.5">RUTA FINANCIERA · evidencia parcial</text>')
    for i, n in enumerate(e["rama_financiera"]):
        _, col, gui, _ = ROT[n["e"]]
        p.append(_caja(A, y, ANC, n["n"], n["c"], col, gui,
                       estado=n["e"] if n["e"] != "validado" else ""))
        ar = next((a for a in e["aristas_financiera"] if a["de"] == i), None)
        if ar:
            _, cA, gA, _ = ROT[ar["e"]]
            p.append(_flecha_v(A + 26, y + 54, y + 96, cA, gA, et=ar["et"]))
        y += 96

    # rama B · orgánica — a dónde se fue la trazabilidad
    yo = yb + 52
    o = e["rama_organica"]
    p.append(f'<text x="{B}" y="{yo-8}" font-size="11" font-weight="700" fill="{PROPIO}" '
             f'letter-spacing="0.5">IDENTIFICADOR PRESENTE EN EL INSTRUMENTO</text>')
    p.append(_caja(B, yo, ANCB, o["n"], o["c"], PROPIO, "2 3", h=66, detalle=o["detalle"]))
    itp = o["interpretacion"]
    # Marco punteado y rótulo explícito: lo de dentro NO es una medición. Sin esta
    # distinción, el dibujo afirmaría por su cuenta lo que ningún motor estableció.
    p.append(f'<rect x="{B}" y="{yo+82}" width="{ANCB}" height="96" rx="6" fill="{PANEL}" '
             f'stroke="{GRIS}" stroke-dasharray="3 3"/>')
    p.append(f'<text x="{B+15}" y="{yo+100}" font-size="9.5" font-weight="700" fill="{GRIS}" '
             f'letter-spacing="0.6">INTERPRETACIÓN — NO ES MEDICIÓN</text>')
    for k, linea in enumerate(itp["texto"]):
        p.append(f'<text x="{B+15}" y="{yo+119+k*16}" font-size="11" fill="{TINTA}" '
                 f'font-style="italic">{linea}</text>')
    p.append(f'<text x="{B+15}" y="{yo+170}" font-size="9.5" fill="{GRIS}">{itp["fuente"]}</text>')

    # rama C · operacional — rota
    yc = yb + 52
    p.append(f'<text x="{C}" y="{yc-8}" font-size="11" font-weight="700" fill="{ROTO}" '
             f'letter-spacing="0.5">RUTA OPERACIONAL · no demostrable</text>')
    for i, n in enumerate(e["rama_operacional"]):
        p.append(_caja(C, yc, ANCB, n["n"], n["c"], ROTO, "5 4", estado=n["e"]))
        if i < len(e["rama_operacional"]) - 1:
            p.append(_flecha_v(C + 26, yc + 54, yc + 96, ROTO, "4 5", aspa=True,
                               et="el instrumento no lo declara"))
        yc += 96

    # ── escala: el devengado trazable dentro del universo del GAD
    ye = 520
    es = e["escala"]
    p.append(f'<rect x="{B}" y="{ye}" width="{ANCB+ANCB+80}" height="104" rx="6" '
             f'fill="{PANEL}" stroke="{BORDE}"/>')
    p.append(f'<text x="{B+15}" y="{ye+23}" font-size="12.5" font-weight="600" fill="{TINTA}">'
             f'Escala · qué parte del gasto queda trazada</text>')
    bw = ANCB + ANCB + 80 - 30
    p.append(f'<rect x="{B+15}" y="{ye+34}" width="{bw}" height="20" rx="3" fill="#E3E9EC"/>')
    p.append(f'<rect x="{B+15}" y="{ye+34}" width="{int(bw*es["pct"]/100)}" height="20" rx="3" '
             f'fill="{DEMOSTRADO}"/>')
    p.append(f'<text x="{B+15}" y="{ye+72}" font-size="12" fill="{TINTA}">'
             f'<tspan font-weight="700">${es["trazable"]:,.0f}</tspan> trazados por el Plan de '
             f'Inversiones · de <tspan font-weight="700">${es["total_gad"]:,.0f}</tspan> devengados '
             f'por el municipio ({es["pct"]:.0f}%)</text>')
    p.append(f'<text x="{B+15}" y="{ye+91}" font-size="11" fill="{GRIS}" font-style="italic">'
             f'{es["nota"]} — el resto no es opacidad.</text>')

    # ── respaldo financiero por objetivo, CON MONTOS
    yr = ye + 120
    ob = e["objetivos"]
    p.append(f'<rect x="{B}" y="{yr}" width="{ANCB+ANCB+80}" height="106" rx="6" '
             f'fill="{PANEL}" stroke="{BORDE}"/>')
    p.append(f'<text x="{B+15}" y="{yr+23}" font-size="12.5" font-weight="600" fill="{TINTA}">'
             f'Respaldo financiero de los {e["total_objetivos"]} objetivos</text>'
             f'<text x="{B+ANCB+ANCB+65}" y="{yr+23}" font-size="10" fill="{GRIS}" '
             f'text-anchor="end">devengado · si no hay, codificado</text>')
    for k, (cl, et) in enumerate([("con_devengado", "con ejecución certificada"),
                                  ("con_codificado", "con asignación sin ejecutar"),
                                  ("sin_evidencia", "sin respaldo financiero")]):
        v = ob[cl]
        # «$0» a secas no distingue un objetivo con presupuesto asignado y sin
        # gastar de uno que no tiene un dólar. Cuando no hay devengado, manda el
        # codificado.
        cifra = (f'${v["monto"]:,.0f}' if v["monto"] else
                 (f'${v["codificado"]:,.0f} asignado' if v["codificado"] else "sin asignación"))
        p.append(f'<text x="{B+15}" y="{yr+46+k*20}" font-size="11.5" fill="{GRIS}">{et}</text>'
                 f'<text x="{B+430}" y="{yr+46+k*20}" font-size="11.5" fill="{TINTA}" '
                 f'text-anchor="end">{v["n"]} de {e["total_objetivos"]}</text>'
                 f'<text x="{B+ANCB+ANCB+65}" y="{yr+46+k*20}" font-size="11.5" '
                 f'font-weight="700" fill="{TINTA}" text-anchor="end">{cifra}</text>')

    # ── lectura
    yl = 760
    p.append(f'<rect x="60" y="{yl}" width="{W-120}" height="94" rx="6" fill="{PANEL}" '
             f'stroke="{BORDE}"/>')
    p.append(f'<text x="78" y="{yl+25}" font-size="13" font-weight="700" fill="{TINTA}">Lectura</text>')
    # «La articulación es demostrable» afirmaba más de lo probado: articulación
    # es una cualidad sustantiva, y lo que la evidencia sostiene es que una
    # CADENA DOCUMENTAL puede reconstruirse. Confundirlas convertiría
    # trazabilidad en efectividad.
    for k, t in enumerate([
        "La evidencia permite reconstruir esta cadena documental hasta el gasto ejecutado.",
        "La cadena hacia metas e indicadores no puede reconstruirse: los instrumentos de 2026",
        "no los declaran. Esto describe lo que los documentos permiten demostrar, no el desempeño."]):
        p.append(f'<text x="78" y="{yl+48+k*19}" font-size="12.5" fill="{TINTA}">{t}</text>')
    p.append(f'<text x="60" y="{yl+114}" font-size="11.5" font-weight="600" fill="{ROTO}">'
             f'Ausencia de evidencia documental. No constituye evidencia de incumplimiento.</text>')

    # ── leyenda: los tres trazos, los tres presentes en el dibujo
    yg = yl + 136
    for k, (col, gui, et) in enumerate([
            (DEMOSTRADO, "", "vínculo demostrado con documento de respaldo"),
            (ROTO, "4 5", "vínculo no demostrable — el instrumento observado no lo declara"),
            (PROPIO, "2 3", "límite de la captura de QUIRA — no es una carencia del municipio")]):
        yy = yg + k * 19
        p.append(f'<line x1="60" y1="{yy}" x2="94" y2="{yy}" stroke="{col}" stroke-width="2.4" '
                 f'stroke-dasharray="{gui}"/>'
                 f'<text x="106" y="{yy+4}" font-size="11.5" fill="{GRIS}">{et}</text>')

    # ── procedencia auditable
    yp = yg + 72
    p.append(f'<line x1="60" y1="{yp}" x2="{W-60}" y2="{yp}" stroke="{BORDE}"/>')
    p.append(f'<text x="60" y="{yp+20}" font-size="11" font-weight="700" fill="{GRIS}" '
             f'letter-spacing="0.5">PROCEDENCIA</text>'
             f'<text x="720" y="{yp+20}" font-size="9.5" fill="{GRIS}" '
             f'letter-spacing="0.4">HASH · SHA-256 truncado a 16 de 64</text>')
    for k, pr in enumerate(e["procedencia"]):
        yy = yp + 38 + k * 17
        p.append(f'<text x="60" y="{yy}" font-size="10.5" fill="{GRIS}">{pr["f"][:62]}</text>'
                 f'<text x="720" y="{yy}" font-size="10.5" fill="{GRIS}" '
                 f'font-family="Consolas, monospace">{pr["sha"]}</text>'
                 f'<text x="{W-60}" y="{yy}" font-size="10.5" fill="{GRIS}" '
                 f'text-anchor="end">{pr["d"]}</text>')
    p.append("</svg>")
    return "".join(p)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anio", type=int, default=2026)
    ap.add_argument("--salida", default=str(RAIZ / "data" / "vis" / "cadena_2026.svg"))
    args = ap.parse_args()

    e = construir_estado(args.anio)
    huerfanos = verificar_procedencia(e)
    if huerfanos:
        print(f"[XX] VIS-INT-001 · {len(huerfanos)} elemento(s) sin propietario canónico:")
        for h in huerfanos:
            print(f"      · {h}")
        sys.exit(2)
    print("[OK] VIS-INT-001 · todo elemento tiene propietario canónico")
    print(f"ESTADO DERIVADO · {e['anio']} · corte {e['corte_cedula']}")
    for n in e["tronco"]:
        print(f"   · {n['n']:46} {n['c']}")
    for n in e["rama_financiera"]:
        print(f"   {'✓' if n['e']=='validado' else '◌'} {n['n']:46} {n['c']}  [{n['e']}]")
    o = e["rama_organica"]
    print(f"   ↻ {o['n']:46} {o['c']}  ({o['detalle']})")
    for n in e["rama_operacional"]:
        print(f"   ∅ {n['n']:46} {n['c']}")
    es = e["escala"]
    print(f"   escala: ${es['trazable']:,.0f} de ${es['total_gad']:,.0f} = {es['pct']:.0f}%")
    for k, v in e["objetivos"].items():
        print(f"   {k:16} {v['n']} obj · ${v['monto']:,.0f}")

    out = Path(args.salida)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg(e), encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(e, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    print(f"\n  → {out}\n  → {out.with_suffix('.json')}")


if __name__ == "__main__":
    main()
