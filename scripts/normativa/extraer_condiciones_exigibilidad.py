# -*- coding: utf-8 -*-
"""
scripts/normativa/extraer_condiciones_exigibilidad.py — la anatomía, no la epidermis
════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-20). Javo, leyendo la Guía sobre el numeral 6:

> *«Si estamos considerando que para cada numeral existen condiciones de
> exigibilidad que establece la Guía, ¿en el monitoreo que estamos construyendo
> para los 636? Eso también me preocupa.»*

Tenía razón, y la medición lo confirmó: la vara capturaba **el enunciado del
artículo, los bullets del conjunto de datos y la periodicidad**. Todo lo demás
—la prosa donde la Guía pone las condiciones de exigibilidad— quedaba fuera:
**105 párrafos en los 26 numerales.**

Y no es prosa decorativa. Dos ejemplos que lo prueban:

    numeral 6, párr. 351   «tomarán los montos del codificado de INGRESOS y para
                            los gastos la información del devengado»
                            ← la regla que sostiene el hallazgo de que el GAD
                              sólo reporta egresos. Estaba en el documento y no
                              en nuestra vara.

    numeral 5-22, párr 317 «el enlace al reporte deberá especificar: descripción
                            del servicio; a quién está dirigido; requisitos;
                            procedimiento; costo; oficinas; horarios; tiempo
                            estimado de respuesta»
                            ← OCHO requisitos DENTRO de un solo campo. El motor
                              comprobaba que la columna existiera.

    campo presente ≠ requisito satisfecho

CÓMO SE CLASIFICA, y por qué así. La taxonomía la fijó el colega (A-G). La
asignación **no la decide el lector**: se deriva del modo verbal con que la Guía
enuncia cada condición. «Deberá» obliga; «podrá» faculta; «se tomará» fija un
método. Clasificar por criterio propio convertiría una recomendación en
obligación, que es el error inverso al que este dominio viene corrigiendo.

Toda clasificación sale marcada con el indicio que la produjo, para que pueda
revisarse una a una sin reconstruir el razonamiento.

Uso:  python scripts/normativa/extraer_condiciones_exigibilidad.py [--numeral 6] [--json s.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import config                                              # noqa: E402

_FUENTE = (config.DATOS_DIR / "Normativa_Word" /
           "LOTAIP - guia-metodologica-mecanismos.docx")
_VARA = RAIZ / "data" / "lotaip" / "exigencias_por_numeral.json"
_SALIDA = RAIZ / "data" / "lotaip" / "condiciones_exigibilidad.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Taxonomía · formulada por el colega, 2026-08-20 ─────────────────────────────
ESTRUCTURAL = "A_exigencia_estructural"      # qué debe contener el conjunto de datos
MATERIAL = "B_exigencia_material"            # qué información debe existir
CALCULO = "C_regla_de_calculo"               # cómo se obtiene o contrasta un valor
FUENTE = "D_fuente_documental_exigida"       # de dónde debe provenir
PERIODICIDAD = "E_periodicidad"              # cada cuánto
PROCEDIMENTAL = "F_condicion_procedimental"  # qué hacer cuando ocurre X
ORIENTACION = "G_orientacion_no_exigible"    # posibilidad, recomendación, facultad

TAXONOMIA = {
    ESTRUCTURAL: "qué debe contener el conjunto de datos",
    MATERIAL: ("condición que exige que determinada información sustantiva "
               "exista, se publique, sea accesible o pueda constatarse en la "
               "materialización esperada, con independencia de la denominación "
               "formal del campo que la transporte"),
    CALCULO: "cómo debe obtenerse o contrastarse un valor",
    FUENTE: "de dónde debe provenir la información",
    PERIODICIDAD: "cada cuánto debe generarse o actualizarse",
    PROCEDIMENTAL: "qué debe hacer la entidad ante determinada situación",
    ORIENTACION: "posibilidad, recomendación o mecanismo facultativo · NO exigible",
}

# Los indicios son LINGÜÍSTICOS y verificables en el texto. El orden importa: se
# evalúa de más específico a más general, porque un párrafo puede llevar varios.
_INDICIOS = [
    # G · lo facultativo se reconoce primero: si la Guía dice «podrán», ninguna
    # otra lectura puede convertirlo en obligación.
    (ORIENTACION, r"\bpodr[áa]n?\b|\bde preferencia\b|\bes importante que\b"
                  r"|\bcontribuir[áa]\b|\bpodr[íi]an?\b"),
    # F · condición con antecedente: «si … deberá»
    (PROCEDIMENTAL, r"^\s*si\b.{0,200}?\bdeber[áa]\b"),
    # C · método de cálculo o contraste
    (CALCULO, r"\bpara obtener\b|\bse tomar[áa]\b|\btomar[áa]n\b|\bporcentaje de\b"
              r"|\bsumatoria\b|\btotalizar\b"),
    # D · origen de los datos
    (FUENTE, r"\bse consideran los datos\b|\bproveniente[s]? de\b"
             r"|\bc[ée]dula presupuestaria\b|\bcon base en\b"),
    # E · cadencia
    (PERIODICIDAD, r"\bactualizaci[óo]n de los metadatos\b|\bperiodicidad\b"),
    # A · estructura del conjunto de datos
    (ESTRUCTURAL, r"\ben el conjunto de datos\b|\bse registrar[áa] el siguiente\b"
                  r"|\bformato del conjunto de datos\b"),
    # B · el resto de lo obligatorio
    (MATERIAL, r"\bdeber[áa]n?\b|\bse debe\b|\bdebe[nr]?\b|\bse detallar[áa]\b"
               r"|\bse incluir[áa]\b"),
]

# Una condición puede enumerar sub-requisitos con punto y coma tras dos puntos.
# El caso insignia: los OCHO contenidos del reporte de servicio (numeral 5-22).
_ENUMERACION = re.compile(r":\s*(.+?[;,].+)$")


def _txt(s: str) -> str:
    s = unicodedata.normalize("NFC", str(s or "")).replace("​", " ")
    return " ".join(s.replace("\t", " ").replace("\n", " ").split())


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").lower()
    return " ".join(s.split())


# Una obligación explícita en el párrafo. Si está, ninguna facultad accesoria
# puede degradar la condición a «no exigible».
# El patron se escribe SIN TILDES a proposito: `_norm` las elimina antes de
# comparar, y un patron acentuado quedo a merced de la codificacion del
# archivo — fallo en silencio y dejo pasar el error que debia impedir.
_OBLIGA = re.compile(r"\bdeberan?\b|\bse debe\b|\bdeben\b|\bes obligatorio\b")


def clasificar(texto: str) -> tuple[str, str]:
    """Tipo de condición e indicio que lo produjo. Nunca sin su fundamento.

    ⚠️ LA PRECEDENCIA DE «G» SE CORRIGIÓ EN EL PRIMER CASO DE PRUEBA (2026-08-20),
    y el error fue exactamente el que esta taxonomía existe para impedir.

    El párrafo 317 del numeral 5-22 dice: *«los sujetos obligados **deberán**
    generar un documento en el que se especifique: descripción del servicio; a
    quién está dirigido; […] tiempo estimado de respuesta. Esta información
    **podrá** reportarse en cualquier formato»*.

    El «podrá» gobierna sólo la última frase —el formato—, no la obligación. Al
    buscar primero los indicios facultativos, el clasificador convirtió **una
    obligación con ocho requisitos dentro en una recomendación**. Regla que lo
    cierra: *una facultad accesoria no degrada una obligación explícita.*"""
    n = _norm(texto)
    obliga = bool(_OBLIGA.search(n))
    for tipo, patron in _INDICIOS:
        if tipo == ORIENTACION and obliga:
            continue            # hay «deberá»: la facultad es accesoria
        m = re.search(patron, n, re.I)
        if m:
            return tipo, m.group(0)
    return MATERIAL, "(sin indicio verbal · revisar a mano)"


def subrequisitos(texto: str) -> list[str]:
    """Los requisitos que una condición enumera dentro de sí.

    «deberán generar un documento en el que se especifique: la descripción del
    servicio; a quién está dirigido; requisitos; …» → ocho requisitos que hoy
    viajaban dentro de un solo campo, invisibles para el motor."""
    m = _ENUMERACION.search(texto)
    if not m:
        return []
    crudo = m.group(1)
    if crudo.count(";") < 2:            # dos o más `;` para no partir prosa normal
        return []
    partes = []
    for bruto in crudo.split(";"):
        # El último requisito arrastra la frase siguiente («…tiempo estimado de
        # respuesta. Esta información podrá reportarse…»). El punto la corta.
        limpio = bruto.strip(" .;").split(". ")[0].strip(" .;")
        if 3 < len(limpio) < 160:
            partes.append(limpio)
    return partes


def extraer(numeral_filtro: str | None = None) -> dict:
    from docx import Document
    doc = Document(str(_FUENTE))
    ps = [(_txt(p.text), p.style.name) for p in doc.paragraphs]
    vara = json.loads(_VARA.read_text(encoding="utf-8"))

    fuera = []
    for n in vara["numerales"]:
        num = str(n["numeral"])
        if numeral_filtro and num != numeral_filtro:
            continue
        pr = n["_procedencia"]
        p0, p1 = pr["parrafo_inicio"], pr["parrafo_fin"]
        p_per = pr.get("parrafo_periodicidad")

        condiciones = []
        for i in range(p0, min(p1, len(ps))):
            t, s = ps[i]
            # Fuera: los bullets (son los campos), el enunciado del artículo
            # (ya está en la vara) y el párrafo de periodicidad (idem).
            if not t or len(t) < 45 or s == "List Paragraph":
                continue
            if t.startswith(("“", '"')) or (p_per and i == p_per):
                continue
            # Un párrafo que empieza en minúscula es la CONTINUACIÓN del
            # anterior, partido por el maquetado del documento. Clasificarlo
            # como condición autónoma inventaría exigencias donde hay una sola.
            continuacion = t[:1].islower()
            tipo, indicio = clasificar(t)
            sub = subrequisitos(t)
            _ = tipo
            condiciones.append({
                # Identificador estable: numeral · tipo · orden. Permite revisar
                # una a una y remontarse al segmento normativo de origen sin
                # reconstruir el razonamiento (colega, 2026-08-20).
                "id": f"C{num.replace('.', '')}-{tipo[0]}{len(condiciones) + 1:02d}",
                "parrafo": i,
                "texto": t,
                "tipo": tipo,
                "indicio": indicio,
                "exigible": tipo != ORIENTACION,
                "subrequisitos": sub,
                "n_subrequisitos": len(sub),
                "fragmento_de_continuacion": continuacion,
            })
        fuera.append({
            "numeral": num,
            "condiciones": condiciones,
            "n_condiciones": len(condiciones),
            "n_exigibles": sum(1 for c in condiciones
                               if c["exigible"] and not c["fragmento_de_continuacion"]),
            "n_fragmentos": sum(1 for c in condiciones
                                if c["fragmento_de_continuacion"]),
            "n_subrequisitos": sum(c["n_subrequisitos"] for c in condiciones),
        })

    return {
        "_meta": {
            "fuente": _FUENTE.name,
            "sha256": hashlib.sha256(_FUENTE.read_bytes()).hexdigest(),
            "norma": "Guía metodológica integral · Defensoría del Pueblo",
            "que_es": "las condiciones de exigibilidad que la Guía establece en "
                      "prosa, fuera de la lista de campos del conjunto de datos",
            "por_que": "la vara capturaba enunciado + campos + periodicidad. Las "
                       "condiciones quedaban fuera: 105 párrafos, entre ellos la "
                       "regla del codificado de ingresos (numeral 6) y los ocho "
                       "contenidos del reporte de servicio (numeral 5-22)",
            "taxonomia": TAXONOMIA,
            "regla_de_clasificacion":
                "se deriva del MODO VERBAL con que la Guía enuncia la condición, "
                "no del criterio del lector. «deberá» obliga; «podrá» faculta. "
                "Cada clasificación trae el indicio que la produjo.",
            "limite": "clasificación PROPUESTA y revisable · el criterio jurídico "
                      "final no lo fija este script",
            "generado": _dt.date.today().isoformat(),
        },
        "numerales": fuera,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--numeral", help="analizar sólo este numeral")
    ap.add_argument("--json", help="ruta donde volcar el resultado")
    ap.add_argument("--detalle", action="store_true")
    args = ap.parse_args()

    if not _FUENTE.exists():
        print(f"⛔ no se halla la Guía en {_FUENTE}")
        sys.exit(2)

    d = extraer(args.numeral)
    tot = sum(n["n_condiciones"] for n in d["numerales"])
    exi = sum(n["n_exigibles"] for n in d["numerales"])
    sub = sum(n["n_subrequisitos"] for n in d["numerales"])

    print("CONDICIONES NORMATIVAS CANDIDATAS A EXIGIBILIDAD · Guía DPE")
    print("lo que la vara NO capturaba: la anatomía, no la epidermis\n")
    # ⚠️ TRES POBLACIONES, NO DOS (colega, 2026-08-20). La salida anterior decía
    # «89 exigibles / 16 orientaciones» y las categorías sumaban 98 + 7. El
    # colega lo cazó por aritmética: *«o faltan 9 condiciones o el clasificador
    # está contando otra población»*. Era lo segundo — 9 fragmentos de
    # continuación iban sumados a las orientaciones por una etiqueta mal puesta.
    # Un número correcto con el rótulo equivocado es un número falso.
    frag = sum(1 for n in d["numerales"] for c in n["condiciones"]
               if c["fragmento_de_continuacion"])
    orient = sum(1 for n in d["numerales"] for c in n["condiciones"]
                 if c["tipo"] == ORIENTACION)
    print(f"   segmentos hallados            {tot:5}")
    print(f"     · candidatas exigibles      {exi:5}")
    print(f"     · orientaciones (G)         {orient:5}   no exigibles")
    print(f"     · fragmentos de continuación{frag:5}   párrafo partido · no son condición")
    print(f"   cuadre: {exi} + {orient} + {frag} = {exi + orient + frag}"
          f"{'  ✓' if exi + orient + frag == tot else '  ⛔ NO CUADRA'}")
    print(f"   subrequisitos dentro de ellas {sub:5}")

    tipos = Counter(c["tipo"] for n in d["numerales"] for c in n["condiciones"])
    print("\n   POR TIPO")
    for t, desc in TAXONOMIA.items():
        print(f"      {t:32} {tipos.get(t, 0):4}   {desc[:40]}")

    if args.detalle or args.numeral:
        for n in d["numerales"]:
            if not n["condiciones"]:
                continue
            print(f"\n   ══ NUMERAL {n['numeral']} · {n['n_condiciones']} condiciones ══")
            for c in n["condiciones"]:
                marca = ("… " if c["fragmento_de_continuacion"]
                         else "  " if c["exigible"] else "○ ")
                print(f"   {marca}[{c['parrafo']}] {c['tipo'][:24]:26} «{c['indicio'][:22]}»")
                print(f"        {c['texto'][:150]}")
                for s in c["subrequisitos"]:
                    print(f"           · {s[:100]}")

    if args.json:
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n   → {p.relative_to(RAIZ) if p.is_absolute() else p}")
        print(f"   sha256 de la fuente: {d['_meta']['sha256'][:32]}…")


if __name__ == "__main__":
    main()
