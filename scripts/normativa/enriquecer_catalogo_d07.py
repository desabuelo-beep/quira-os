# -*- coding: utf-8 -*-
"""
scripts/normativa/enriquecer_catalogo_d07.py — cerrar el contrato operativo de d07
══════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Javo pidió que QUIRA ejecute el dominio **sin Claude
supervisando**: *«Quira debe realizar todo esto de manera independiente cuando se la
manda a través de los comandos o botones del sistema»*.

Para eso el agente necesita un contrato ejecutable, y **ya existe**:
`data/d07/catalogo_cd_d07_v1.0.0.yaml`, con `fuente_verdad: true`, sus 24 conjuntos y
—en CD-06— los componentes materiales del presupuesto. Lo que le falta es justo lo que
se extrajo hoy de la Guía Metodológica: **periodicidad, campos exigidos y regla de
ausencia**. Sin eso el agente no puede decidir solo si un numeral está a tiempo, si el
archivo trae lo que debe, ni si una celda vacía es una carencia o una declaración.

QUÉ NO HACE, y es lo importante: **no crea una segunda fuente de verdad.** No hay
matriz paralela ni MVM nueva —eso sólo renombraría C4/C5 y `componentes`, y la Regla de
Oro 7 lo prohíbe—. Enriquece el catálogo existente y conserva intacto lo que ya
declaraba: `normativa`, `operativa`, `empirica`, `componentes`, `guia`.

EL GATE QUE JUSTIFICA EL MÉTODO. Los componentes materiales se derivan **sólo del texto
literal de la obligación** (decisión de Javo): la norma los enumera —«especificando
ingresos, gastos, financiamiento y resultados operativos […] así como liquidación del
presupuesto»—. CD-06 es el único conjunto donde el canon ya los había declarado, así
que sirve de control: **si el derivador no reproduce esos cinco, aborta.** Un extractor
que no puede reproducir la única respuesta conocida no puede proponer las demás.

Uso:  python scripts/normativa/enriquecer_catalogo_d07.py [--escribir]
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

EXIGENCIAS = RAIZ / "data" / "lotaip" / "exigencias_por_numeral.json"
SELLO = RAIZ / "data" / "lotaip" / "VARA_SELLO.json"
ORIGEN = RAIZ / "data" / "d07" / "catalogo_cd_d07_v1.0.0.yaml"
DESTINO = RAIZ / "data" / "d07" / "catalogo_cd_d07_v1.1.0.yaml"

# Control del derivador: lo que el canon ya declaró para CD-06 desde julio.
CONTROL_CD06 = ["Ingresos", "Gastos", "Financiamiento",
                "Resultados_operativos", "Liquidacion"]

# SÓLO `especificando`. Es el único conector con el que la ley abre una enumeración
# cerrada de dimensiones —«especificando ingresos, gastos, financiamiento y resultados
# operativos»—. Se probó también con `incluyendo` y el resultado fue ruido: del numeral
# 3 («incluyendo todo ingreso adicional correspondiente a todo el personal del
# organismo, dependencia y/o persona jurídica») derivaba el componente
# `Dependencia_y/o_persona_juridica`, que es un complemento del sujeto obligado, no una
# dimensión del conjunto de datos. Un componente inventado es peor que uno ausente:
# haría fallar la cobertura material por una exigencia que la norma nunca impuso.
_ENUMERADORES = r"(?:especificando)"
_ADITIVO = r"as[íi] como"


def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _titulo(frase: str) -> str:
    """`resultados operativos` → `Resultados_operativos`, como el canon los escribe."""
    p = _sin_tildes(" ".join(frase.split())).strip(" .,;")
    p = re.sub(r"^(el|la|los|las|un|una|todo|todos)\s+", "", p, flags=re.I)
    if not p:
        return ""
    palabras = p.split()
    return "_".join([palabras[0].capitalize()] + [w.lower() for w in palabras[1:]])


def derivar_componentes(obligacion: str) -> list[str]:
    """Extrae las dimensiones que el enunciado nombra EXPRESAMENTE.

    Nada de conocimiento externo ni de inferencia sobre los datos: si la norma no las
    enumera, este conjunto no tiene componentes derivables y se declara así. Es
    preferible medir menos numerales que medir con dimensiones inventadas."""
    if not obligacion:
        return []
    o = " ".join(obligacion.split())
    fuera: list[str] = []

    for m in re.finditer(_ENUMERADORES + r"\s+(.+?)(?=$|\.|;|,?\s+as[íi] como|\s+de conformidad)",
                         o, re.I):
        bloque = m.group(1)
        # «a, b, c y d» — la coma y la conjunción son el separador que usa la ley.
        for parte in re.split(r",\s*|\s+y\s+", bloque):
            parte = parte.strip()
            # Una «parte» larga ya no es una dimensión: es una oración subordinada.
            if 3 <= len(parte) <= 40:
                t = _titulo(parte)
                if t and t not in fuera:
                    fuera.append(t)

    # `así como X` añade una dimensión más, en singular. Se toma sólo el núcleo
    # nominal —«liquidación del presupuesto» → `Liquidacion`— porque el complemento
    # repite el objeto del numeral y no es una dimensión distinta.
    for m in re.finditer(_ADITIVO + r"\s+((?:\w+\s*){1,3}?)(?:\s+del?\s+|\s*,|\s*\.|$)",
                         o, re.I):
        nucleo = m.group(1).strip()
        if 3 <= len(nucleo) <= 34:
            t = _titulo(nucleo.split()[0] if len(nucleo.split()) > 2 else nucleo)
            if t and t not in fuera:
                fuera.append(t)
    return fuera


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    import yaml
    cat = yaml.safe_load(ORIGEN.read_text(encoding="utf-8"))
    ex = json.loads(EXIGENCIAS.read_text(encoding="utf-8"))
    sello = json.loads(SELLO.read_text(encoding="utf-8"))

    # La vara debe estar sellada y coincidir: el catálogo no se enriquece con una
    # exigencia que cambió a mitad de camino.
    actual = hashlib.sha256(EXIGENCIAS.read_bytes()).hexdigest()
    if actual != sello["sha256"]:
        print("[XX] la vara cambió desde que fue sellada — no se enriquece el catálogo")
        sys.exit(3)

    porn = {n["numeral"]: n for n in ex["numerales"]}
    a24 = ex.get("articulo_24_gad") or {}

    # ── GATE DEL DERIVADOR ────────────────────────────────────────────────────────
    d6 = derivar_componentes(porn["6"]["obligacion"])
    faltan = [c for c in CONTROL_CD06 if c not in d6]
    print("GATE · ¿el derivador reproduce los componentes que el canon ya declaró?")
    print(f"   canon CD-06 : {CONTROL_CD06}")
    print(f"   derivado    : {d6}")
    if faltan:
        print(f"   [XX] no reproduce: {faltan}")
        print("   Un derivador que no recupera la única respuesta conocida no puede")
        print("   proponer las demás. No se enriquece el catálogo.")
        sys.exit(4)
    print("   [ok] reproduce los cinco componentes\n")

    # ── enriquecimiento ───────────────────────────────────────────────────────────
    nuevos = 0
    for cd in cat["conjuntos_datos"]:
        num = str(cd.get("numeral_ley") or "")
        clave = "5" if num == "5+22" else num
        n = porn.get(clave)

        if num.startswith("Art"):
            # CD-A24 se nutre de la matriz específica del art. 24, no del art. 19.
            if a24.get("secciones"):
                cd["periodicidad"] = a24["periodicidad"]
                cd["campos_exigidos"] = [c for s in a24["secciones"] for c in s["campos"]]
                cd["secciones"] = [{"seccion": s["seccion"], "titulo": s["titulo"],
                                    "campos": s["campos"]} for s in a24["secciones"]]
                cd["obligacion_literal"] = a24.get("obligacion")
                nuevos += 1
            continue
        # CD-01 agrupa 1.1/1.2/1.3 y por eso NO existe como entrada «1» en la matriz:
        # la guía desarrolla los tres por separado, con periodicidad y campos propios.
        # Buscarlo por la clave «1» lo dejaba sin campos ni periodicidad —un conjunto
        # canónico vacío—, cuando la exigencia está completa en sus sub-numerales.
        if clave == "1":
            subs = [porn[k] for k in ("1.1", "1.2", "1.3") if k in porn]
            if subs:
                cd["obligacion_literal"] = subs[0]["obligacion"]
                cd["subnumerales"] = [{"numeral": s["numeral"],
                                       "campos_exigidos": s["campos_exigidos"],
                                       "periodicidad": s["periodicidad"]} for s in subs]
                cd["campos_exigidos"] = [c for s in subs for c in s["campos_exigidos"]]
                # La periodicidad NO se agrega: 1.1 no la declara y 1.2/1.3 sí. Una
                # sola cadencia para los tres ocultaría que uno no es medible.
                cd["periodicidad"] = {
                    "estado": "por_subnumeral",
                    "detalle": {s["numeral"]: s["periodicidad"].get("contenidos")
                                for s in subs},
                }
                nuevos += 1
            continue
        if not n:
            cd["exigencia"] = {"estado": "no_hallada_en_la_guia"}
            continue

        cd["obligacion_literal"] = n["obligacion"]
        cd["periodicidad"] = n["periodicidad"]
        cd["campos_exigidos"] = n["campos_exigidos"]

        derivados = derivar_componentes(n["obligacion"] or "")
        if cd.get("componentes"):
            # Lo que el canon ya declaraba MANDA. Los derivados sólo se registran
            # como contraste, para que una divergencia se vea en vez de perderse.
            cd["componentes_derivados_del_literal"] = derivados
        elif derivados:
            cd["componentes"] = derivados
            cd["componentes_origen"] = "derivados del texto literal de la obligación"
        else:
            cd["componentes_origen"] = "la obligación no enumera dimensiones"
        nuevos += 1

    cat["version"] = "1.1.0"
    cat["vara_normativa"] = {
        "fuente": ex["_meta"]["fuente"], "sha256_fuente": ex["_meta"]["sha256"],
        "sha256_matriz": sello["sha256"],
        "emisor": "Defensoría del Pueblo del Ecuador",
        "nota": "periodicidad, campos y regla de ausencia extraídos de la Guía "
                "Metodológica. Lo que la guía no declara queda no_sustentado: "
                "no se completa con conocimiento general sobre LOTAIP.",
    }
    cat["regla_ausencia"] = ex.get("regla_de_ausencia")

    print(f"CATÁLOGO d07 · {len(cat['conjuntos_datos'])} conjuntos · "
          f"{nuevos} enriquecidos\n")
    print(f"  {'id':8}{'periodicidad':16}{'campos':>7}  componentes")
    print("  " + "─" * 92)
    for cd in cat["conjuntos_datos"]:
        p = cd.get("periodicidad") or {}
        cad = " o ".join(p.get("contenidos") or []) or "—"
        comp = cd.get("componentes") or []
        marca = "" if cd.get("componentes_origen", "").startswith("derivados") else " *"
        print(f"  {cd['id']:8}{cad:16}{len(cd.get('campos_exigidos') or []):7}  "
              f"{(', '.join(comp)[:52] or '—')}{marca if comp else ''}")
    print("  " + "─" * 92)
    print("  * componentes ya declarados en el canon (no derivados hoy)")

    sin_per, por_sub = [], []
    for c in cat["conjuntos_datos"]:
        p = c.get("periodicidad") or {}
        if p.get("estado") == "por_subnumeral":
            por_sub.append(c["id"])
        elif not p.get("contenidos"):
            sin_per.append(c["id"])
    if sin_per:
        print(f"\n  sin periodicidad en el corpus: {', '.join(sin_per)}")
        print("  → el agente NO debe medirles temporalidad: estado no_determinable")
    if por_sub:
        # No es lo mismo «no medible» que «medible por partes»: en CD-01 el
        # sub-numeral 1.1 carece de cadencia declarada pero 1.2 y 1.3 la tienen.
        # Tratar el conjunto entero como no medible perdería dos exigencias reales.
        print(f"  periodicidad por sub-numeral: {', '.join(por_sub)}")
        print("  → se mide cada sub-numeral con la suya; el que no la declare, no se mide")

    if args.escribir:
        DESTINO.write_text(
            yaml.safe_dump(cat, allow_unicode=True, sort_keys=False, width=100),
            encoding="utf-8")
        print(f"\n  → {DESTINO.relative_to(RAIZ)}")
        print(f"  sha256: {hashlib.sha256(DESTINO.read_bytes()).hexdigest()[:40]}…")
    else:
        print("\n  (ensayo · use --escribir para generar el catálogo v1.1.0)")


if __name__ == "__main__":
    main()
