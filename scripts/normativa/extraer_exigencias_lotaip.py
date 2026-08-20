# -*- coding: utf-8 -*-
"""
scripts/normativa/extraer_exigencias_lotaip.py — qué exige la norma, numeral por numeral
═════════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Javo detuvo una medición que contaba archivos por mes:

> *«Mal tu contador Director: en solo 3 de 12 meses del 2025 el GAD Montecristi sube su
> Presupuesto, numeral 6 […] la lógica está en lo que piden los documentos legales del
> corpus normativo. Esos documentos mandan todo el procedimiento a llevar (y lo que
> menciona se puede sumar como filtro).»*

Tenía razón, y el reparo es de fondo. **La periodicidad de cada numeral la fija la norma,
no el contador.** Este documento no declara una cadencia uniforme: declara al menos seis
distintas —mensual, trimestral, semestral, anual, «semestral o anual según varíen los
contenidos», y «conforme los eventos electorales»—. Exigirle doce meses a un numeral de
contenido trimestral **fabrica un incumplimiento que la norma no sostiene**.

LO QUE ESTE MÓDULO EXTRAE, y no es de QUIRA: es del órgano rector.

  · `Guía metodológica para el cumplimiento de las obligaciones de transparencia`
    Defensoría del Pueblo · Capítulo II (obligación, campos y periodicidad) y
    Capítulo IX (anexo de estándares de datos abiertos)

REGLA DE EXTRACCIÓN (formulación del colega, adoptada):

    **No se completa esta matriz con conocimiento general sobre LOTAIP.**
    Si el corpus lo dice, se reproduce; si no lo dice, se marca `no_sustentado`
    y se sigue investigando dentro del corpus.

Por eso ningún campo de la salida se escribe a mano: todo lleva `_procedencia` con el
párrafo del que salió, y la periodicidad conserva **el texto literal** junto a su lectura
normalizada — para que quien discuta la medición pueda discutir la fuente, no la lectura.

QUÉ NO HACE: no evalúa a nadie, no puntúa, no cuenta archivos. Produce la vara. La
confrontación contra los 936 archivos capturados es un paso posterior y separado.

Uso:  python scripts/normativa/extraer_exigencias_lotaip.py [--json data/lotaip/exigencias_por_numeral.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes                    # noqa: E402

FUENTE = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Normativa_Word"
              r"\LOTAIP - guia-metodologica-mecanismos.docx")

# Los tres sub-bloques del numeral 1. La guía los desarrolla por separado porque el
# numeral 1 del art. 19 manda tres cosas distintas en una sola frase, y la Defensoría
# los publica separados (`Numeral 1.2`, `Numeral 1.3` en el portal). Tratarlos como uno
# solo mezclaría tres periodicidades que la guía declara por separado.
SUBNUMERALES_1 = {
    "Estructura orgánica funcional": "1.1",
    "Base legal que la rige": "1.2",
    "Metas y objetivos de las unidades administrativas": "1.3",
}

# Un numeral puede compartir conjunto de datos con otro: la guía desarrolla el 5
# (servicios) y el 22 (formularios) en un mismo bloque, con una sola lista de campos y
# una sola periodicidad. Separarlos inventaría dos exigencias donde la norma pone una.
COMPARTIDOS = {"5": ["5", "22"]}


def _txt(s) -> str:
    """Normaliza a forma compuesta y colapsa espacios. La guía trae combinaciones
    Unicode descompuestas y espacios de ancho cero dentro de las viñetas."""
    s = unicodedata.normalize("NFC", str(s or "")).replace("\u200b", " ")
    return " ".join(s.replace("\t", " ").replace("\n", " ").split())


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").lower()
    return " ".join(s.split())


# ── periodicidad ────────────────────────────────────────────────────────────────────
# Se leen las cadencias EN EL ORDEN EN QUE LA NORMA LAS ESCRIBE, y se conserva el
# literal. «semestral o anual» es una sola declaración con dos opciones, no dos
# obligaciones: colapsarla a «anual» relajaría la vara, y a «semestral» la endurecería.
_CADENCIAS = ["mensual", "bimensual", "trimestral", "cuatrimestral",
              "semestral", "anual"]


def _cadencias(frase: str) -> list[str]:
    n = _norm(frase)
    hall = [(n.find(c), c) for c in _CADENCIAS if c in n]
    return [c for _, c in sorted(hall)]


def _periodicidad(frase: str) -> dict:
    """Parte la declaración en sus dos mitades: metadatos y contenidos.

    La guía las escribe siempre en la misma frase y **casi siempre distintas**:
    los metadatos se actualizan mensualmente aunque el contenido sea anual. Medir
    el contenido con la cadencia de los metadatos fue exactamente el error que
    produjo el «3/12» del numeral 6."""
    lit = _txt(frase)
    n = _norm(lit)
    # El pivote es la palabra que separa ambas mitades en el texto del órgano rector.
    corte = -1
    for marca in ("periodicidad de generacion", "periodicidad de la publicacion",
                  "periodicidad de generacion de sus contenidos"):
        p = n.find(marca)
        if p != -1:
            corte = p
            break
    if corte == -1:
        # Una sola cadencia para ambos: «los metadatos … y la periodicidad … será mensual».
        c = _cadencias(lit)
        return {"literal": lit,
                "metadatos": c[0] if c else None,
                "contenidos": c if c else [],
                "estado": "declarada" if c else "no_interpretable"}

    meta = _cadencias(lit[:corte])
    cont = _cadencias(lit[corte:])
    if not cont and meta:
        cont = meta
    if not meta and cont:
        # «…los metadatos de este conjunto de datos **y** la periodicidad de generación
        # de sus contenidos será mensual»: una sola cadencia enunciada al final rige las
        # dos mitades. Leerla sólo como contenido dejaba 17 numerales sin metadatos
        # declarados cuando la norma sí los declara.
        meta = cont[:1]
    return {
        "literal": lit,
        "metadatos": meta[0] if meta else None,
        "contenidos": cont,
        # `condicionada` = la norma admite dos cadencias («semestral o anual, según
        # varíen los contenidos»). No es ambigüedad del lector: es la regla escrita.
        "estado": ("condicionada" if len(cont) > 1 else
                   "declarada" if cont else "no_interpretable"),
        "condicion": ("según varía" if "segun" in _norm(lit[corte:]) else None),
    }


# ── extracción ──────────────────────────────────────────────────────────────────────
def _bloques_cap2(ps: list[tuple[str, str]]) -> list[dict]:
    """Recorre el Capítulo II y corta un bloque por numeral.

    El ancla primaria es la línea `Número N`. No basta: el numeral 12 (mecanismos de
    rendición de cuentas) **no la tiene** en el original, y el 22 va dentro del bloque
    del 5. Por eso el ancla secundaria es la transcripción entrecomillada del artículo,
    que la guía cierra con `(ibidem, número N)` — el propio documento se autonumera."""
    ini = fin = None
    for i, (t, s) in enumerate(ps):
        if s == "Heading 1" and t.startswith("Parámetros técnicos para garantizar"):
            if "artículo 19" in t and ini is None:
                ini = i
            elif "del 20 al 30" in t and ini is not None:
                fin = i
                break
    if ini is None:
        return []
    fin = fin or len(ps)

    marcas: list[tuple[int, str]] = []
    for i in range(ini, fin):
        t, s = ps[i]
        if not t:
            continue
        if re.fullmatch(r"N[uú]mero\s+\d+", t):
            marcas.append((i, t.split()[-1]))
            continue
        if s == "Heading 1":
            for pref, sub in SUBNUMERALES_1.items():
                if t[1:].strip().startswith(pref) or t.startswith(pref):
                    marcas.append((i, sub))
                    break
            continue
        # Ancla secundaria: transcripción del artículo con su número declarado.
        m = re.search(r"[“\"].{20,}?[”\"]\s*\(.*?n[uú]mero\s+(\d+)\)", t)
        if m and not any(n == m.group(1) for _, n in marcas):
            marcas.append((i, m.group(1)))
            continue
        # El numeral 12 sólo se reconoce por su enunciado: la guía omitió su ancla.
        if t.startswith("“Mecanismos de rendición de cuentas"):
            if not any(n == "12" for _, n in marcas):
                marcas.append((i, "12"))

    marcas.sort()
    # La guía desarrolla el 5 (servicios) y el 22 (formularios) en UN solo bloque: una
    # lista de campos y una periodicidad para ambos. Cortarlos por su ancla dejaba al 5
    # con cero campos y sin periodicidad —y esa carencia era del lector, no de la norma.
    fusionadas = [m for k, m in enumerate(marcas)
                  if not (m[1] == "22" and k and marcas[k - 1][1] == "5")]

    out = []
    for k, (p0, num) in enumerate(fusionadas):
        p1 = fusionadas[k + 1][0] if k + 1 < len(fusionadas) else fin
        out.append({"numeral": num, "desde": p0, "hasta": p1})
    return out


def _leer_bloque(ps, b: dict) -> dict:
    """De un bloque saca lo que la norma exige: enunciado, campos y periodicidad."""
    p0, p1 = b["desde"], b["hasta"]
    enunciado, campos, periodo, en_campos = None, [], None, False
    p_campos = p_periodo = None

    for i in range(p0, p1):
        t, s = ps[i]
        if not t:
            continue
        if enunciado is None and t.startswith(("“", '"')):
            # La transcripción puede abarcar VARIOS párrafos: los numerales 8
            # (contratación) y 17 (audiencias) abren comilla y la cierran dos o tres
            # párrafos después. Exigir el cierre en el mismo párrafo dejaba sin
            # enunciado a los dos numerales de mayor peso del artículo.
            trozos, cerro = [], False
            for j in range(i, min(i + 8, p1)):
                tj = ps[j][0]
                if not tj:
                    continue
                trozos.append(tj)
                if "”" in tj[1:] or (j > i and '"' in tj):
                    cerro = True
                    break
            crudo = _txt(" ".join(trozos))
            m = re.match(r'^[“"](.+?)[”"]', crudo)
            enunciado = _txt(m.group(1)) if m else (crudo.lstrip('“"') if not cerro else None)
            if enunciado:
                continue
        if s == "Heading 2" and _norm(t).startswith("conjunto de datos"):
            en_campos, p_campos = True, i
            continue
        if en_campos:
            if s == "List Paragraph":
                v = _txt(t)
                if v:
                    campos.append(v)
                continue
            # Un párrafo corrido cierra la lista de campos.
            if campos:
                en_campos = False
        # Subcadena, NO prefijo. En el numeral 24 la frase arranca a mitad de párrafo
        # («…información en la periodicidad establece en los compromisos asumidos por la
        # institución. La actualización de los metadatos…») y exigir prefijo la perdía;
        # lo mismo en los numerales 11 y 20. Tres periodicidades declaradas se habrían
        # registrado como silencio de la norma siendo defecto del lector.
        if periodo is None and (j := t.find("La actualización de los metadatos")) != -1:
            periodo, p_periodo = _periodicidad(t[j:]), i

    d = {
        "numeral": b["numeral"],
        # El enunciado LITERAL del artículo tal como la guía lo transcribe. Si falta,
        # se declara: no se sustituye por una paráfrasis ni por memoria de la ley.
        "obligacion": enunciado or None,
        "obligacion_estado": "transcrita" if enunciado else "no_sustentado",
        "campos_exigidos": campos,
        "campos_estado": "declarados" if campos else "no_sustentado",
        "periodicidad": periodo or {"estado": "no_sustentado",
                                    "literal": None, "contenidos": []},
        "_procedencia": {"capitulo": "II", "parrafo_inicio": p0, "parrafo_fin": p1,
                         "parrafo_campos": p_campos, "parrafo_periodicidad": p_periodo},
    }
    if b["numeral"] in COMPARTIDOS:
        d["comparte_conjunto_con"] = COMPARTIDOS[b["numeral"]]
    return d


def _anexo(ps: list[tuple[str, str]]) -> dict:
    """Capítulo IX. **No contiene los campos: remite a hojas externas.**

    Es un hallazgo, no un defecto del lector: la estructura formal del conjunto de
    datos, sus metadatos y su diccionario viven en Google Sheets fuera del documento
    normativo. QUIRA registra la remisión y su URL; **no reconstruye los campos que
    el corpus no contiene.**"""
    ini = None
    for i, (t, s) in enumerate(ps):
        if s == "Heading 1" and _norm(t) == "estructura de datos":
            ini = i
            break
    if ini is None:
        return {}
    out, actual = {}, None
    for i in range(ini, len(ps)):
        t, s = ps[i]
        if not t:
            continue
        m = re.fullmatch(r"N[uú]mero\s+(\d+)", t)
        if m:
            actual = m.group(1)
            out.setdefault(actual, {"remisiones": [], "_parrafo": i})
            continue
        if actual and "http" in t:
            u = re.search(r"(https?://\S+)", t.replace(" ", ""))
            eti = _norm(t.split("http")[0]).strip(" :·")
            if u:
                out[actual]["remisiones"].append({"que": eti or "sin etiqueta",
                                                  "url": u.group(1)})
    return out


def extraer() -> dict:
    import docx
    doc = docx.Document(str(FUENTE))
    ps = [(p.text.strip(), p.style.name) for p in doc.paragraphs]

    bloques = _bloques_cap2(ps)
    numerales = [_leer_bloque(ps, b) for b in bloques]

    # El bloque `1` sólo transcribe el enunciado del artículo; el desarrollo vive en
    # 1.1/1.2/1.3. Se propaga la transcripción a los tres y el bloque suelto se retira:
    # dejarlo habría publicado un numeral 1 con cero campos y sin periodicidad —una
    # ausencia inventada— junto a los tres sub-numerales que sí los tienen.
    n1 = next((n for n in numerales if n["numeral"] == "1"), None)
    if n1 and n1["obligacion"]:
        for n in numerales:
            if n["numeral"].startswith("1.") and not n["obligacion"]:
                n["obligacion"] = n1["obligacion"]
                n["obligacion_estado"] = "transcrita_en_el_numeral_matriz"
                n["_procedencia"]["parrafo_obligacion"] = n1["_procedencia"]["parrafo_inicio"]
    if n1 and any(n["numeral"].startswith("1.") for n in numerales):
        numerales = [n for n in numerales if n["numeral"] != "1"]

    anexo = _anexo(ps)

    for n in numerales:
        base = n["numeral"].split(".")[0]
        r = anexo.get(base, {}).get("remisiones", [])
        n["estructura_formal"] = {
            "estado": "remitida_a_recurso_externo" if r else "no_declarada",
            "remisiones": r,
            "nota": ("el anexo del capítulo IX no publica los campos: enlaza hojas de "
                     "cálculo externas. Fuera del corpus, no verificables por SHA."),
        }
    return {"numerales": numerales, "n_anexo": len(anexo),
            "regla_de_ausencia": _regla_ausencia(ps),
            "articulo_24_gad": _articulo_24(ps)}


def _articulo_24(ps) -> dict:
    """Art. 24 · obligación **específica** de los GAD, y por eso va aparte.

    No se mezcla con la matriz del art. 19: son artículos distintos con conjuntos de
    datos distintos, y agregarlos contaminaría el indicador del 19 con obligaciones
    que no le pertenecen (colega, 2026-08-17). El portal de la DPE también los publica
    separados, bajo la etiqueta `Art. 24 Gobiernos Autónomos Descentralizados`.

    Nótese lo que manda su sección 1: los GAD deben publicar aquí **el PDOT**. La misma
    fuente que el resto de QUIRA usa para la cadena meta→partida→devengado es, además,
    una obligación de transparencia con periodicidad propia."""
    ini = None
    for i, (t, s) in enumerate(ps):
        if t.strip() == "Artículo 24":
            ini = i
            break
    if ini is None:
        return {"estado": "no_sustentado"}
    # El artículo siguiente NO siempre lleva encabezado `Artículo 25`: abre con su
    # sujeto obligado entrecomillado —«Banco Central del Ecuador. - El Banco Central…»—.
    # Cortar sólo por el encabezado numerado arrastraba al bloque del GAD los campos
    # del Banco Central y de la Asamblea Nacional: 70 campos ajenos atribuidos al GAD.
    _OTRO_ART = re.compile(r'^[“"][A-ZÁÉÍÓÚÑ][^”"]{4,70}\.\s*[-–]')
    fin = ini + 80
    for i in range(ini + 2, min(len(ps), ini + 200)):
        t = ps[i][0].strip()
        if re.fullmatch(r"Art[íi]culo\s+\d+", t) or _OTRO_ART.match(t):
            fin = i
            break

    enunciado, secciones, actual, periodo = None, [], None, None
    for i in range(ini, fin):
        t, s = ps[i]
        if not t:
            continue
        if enunciado is None and t.startswith("“"):
            m = re.match(r'^[“"](.+?)[”"]', _txt(t))
            enunciado = _txt(m.group(1)) if m else _txt(t).lstrip('“"')
            continue
        if s == "Heading 1" and re.match(r"^\d\s", t):
            actual = {"seccion": t[0], "titulo": _txt(t[1:]), "campos": [],
                      "_parrafo": i}
            secciones.append(actual)
            continue
        if actual is not None and s == "List Paragraph":
            v = _txt(t)
            if v:
                actual["campos"].append(v)
            continue
        if (j := t.find("La actualización de los metadatos")) != -1 and periodo is None:
            periodo = _periodicidad(t[j:])
        # La guía manda expresamente incluir el PDOT en la sección 1. Se registra como
        # exigencia declarada, no como interpretación nuestra.
        if actual is not None and "Planes de Desarrollo y Ordenamiento Territorial" in t:
            actual["incluye_expresamente"] = _txt(t)

    return {
        "articulo": "24",
        "sujeto_obligado": "Gobiernos Autónomos Descentralizados",
        "obligacion": enunciado,
        "secciones": secciones,
        "periodicidad": periodo or {"estado": "no_sustentado", "contenidos": []},
        "_procedencia": {"capitulo": "II", "parrafo_inicio": ini, "parrafo_fin": fin},
        "nota": "obligación específica: NO se agrega a la matriz del art. 19",
    }


def _regla_ausencia(ps) -> dict:
    """La norma prevé que un campo no tenga información, y **fija la forma exacta**.

    Importa porque separa dos cosas que se parecen y no son iguales: un conjunto de
    datos que calla, y uno que declara la ausencia. Sólo el segundo cumple —y sólo si
    usa la fórmula literal. `no disponible` no es `INFORMACIÓN NO DISPONIBLE`: el
    Instructivo manda «verificar que en éste se encuentre colocado los textos», que es
    una comprobación de forma, no de intención."""
    for i, (t, _) in enumerate(ps):
        c = _txt(t)
        if re.search(r"se escribir[áa].{0,40}(NO APLICA|INFORMACIÓN NO DISPONIBLE)", c):
            return {
                "literal": c,
                "formulas_admitidas": ["NO APLICA", "INFORMACIÓN NO DISPONIBLE"],
                "sin_comillas": True,
                "exige_ademas": "nota aclaratoria en el archivo diccionario de datos "
                                "(Instructivo de monitoreo · cap. VI de la guía)",
                "_procedencia": {"capitulo": "VI", "parrafo": i},
            }
    return {"estado": "no_sustentado"}


# ── informe ─────────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", help="ruta donde volcar la matriz")
    args = ap.parse_args()

    if not FUENTE.exists():
        print(f"[XX] no se halló la guía: {FUENTE.name}")
        sys.exit(2)

    print("EXIGENCIAS LOTAIP POR NUMERAL · Guía metodológica · Defensoría del Pueblo\n")
    d = extraer()
    ns = d["numerales"]

    print(f"  {'num':5} {'campos':>6}  {'metadatos':10} {'contenidos':24} obligación")
    print("  " + "─" * 96)
    for n in ns:
        p = n["periodicidad"]
        cont = " o ".join(p.get("contenidos") or []) or "—"
        if p.get("estado") == "condicionada":
            cont += " *"
        ob = (n["obligacion"] or "«no transcrita en la guía»")[:40]
        print(f"  {n['numeral']:5} {len(n['campos_exigidos']):6}  "
              f"{str(p.get('metadatos') or '—'):10} {cont:24} {ob}")
    print("  " + "─" * 96)
    print("  * la norma admite dos cadencias según varíe el contenido — no es ambigüedad del lector")

    from collections import Counter
    cad = Counter(" o ".join(n["periodicidad"].get("contenidos") or []) or "sin declarar"
                  for n in ns)
    print(f"\n  CADENCIAS DE CONTENIDO declaradas por la norma:")
    for k, v in cad.most_common():
        print(f"     {k:28} {v:3} numerales")

    faltan = [n["numeral"] for n in ns if n["periodicidad"].get("estado") == "no_sustentado"]
    if faltan:
        print(f"\n  ⚠ sin periodicidad hallada en el corpus: {', '.join(faltan)}")
        print("    → NO se les asigna una por defecto. Se miden aparte o no se miden.")

    inv = Invariantes("exigencias LOTAIP por numeral")
    inv.cardinalidad("numerales", len(ns), minimo=20)
    inv.cardinalidad("con campos declarados",
                     sum(1 for n in ns if n["campos_exigidos"]), minimo=18)
    inv.texto_legible([c for n in ns for c in n["campos_exigidos"]])
    print()
    inv.informe()

    if args.json:
        sha = hashlib.sha256(FUENTE.read_bytes()).hexdigest()
        salida = {"_meta": {
            "fuente": FUENTE.name, "sha256": sha,
            "norma": "Guía metodológica para el cumplimiento de las obligaciones de "
                     "transparencia · Defensoría del Pueblo del Ecuador",
            "alcance": "art. 19 LOTAIP — obligaciones generales de transparencia activa",
            "regla": "lo que el corpus dice se reproduce; lo que no dice se marca "
                     "no_sustentado. QUIRA no completa la vara con conocimiento general.",
            "advertencia": "esta matriz NO puntúa a nadie. Es la exigencia normativa "
                           "contra la cual se confronta la evidencia observada.",
        }, **d}
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → {p}")
        print(f"  sha256 de la fuente: {sha[:32]}…")


if __name__ == "__main__":
    main()
