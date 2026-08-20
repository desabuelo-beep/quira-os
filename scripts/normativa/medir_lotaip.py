# -*- coding: utf-8 -*-
"""
scripts/normativa/medir_lotaip.py — la evidencia observada contra la exigencia normativa
═════════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Una medición anterior reportó «12/12 meses» contando meses
con *alguna* publicación. Javo la desarmó con un caso:

> *«Mal tu contador Director: en solo 3 de 12 meses del 2025 el GAD Montecristi sube su
> Presupuesto, numeral 6.»*

Tenía razón, y el defecto no era aritmético sino de método: **se agregaba por entidad lo
que la norma exige por numeral**, y se contaba con una cadencia uniforme que la norma no
establece. Este módulo hace lo contrario y en el orden que fija el corpus:

    corpus normativo → obligación → periodicidad → evidencia exigida → prueba → resultado

LAS TRES COSAS QUE AQUÍ NO SE CONFUNDEN (formulación del colega, adoptada):

    filtro exploratorio  ≠  criterio normativo  ≠  resultado de cumplimiento

El conteo de archivos por mes es **filtro**: sirve para detectar dónde mirar, jamás para
concluir. El criterio lo pone la Guía Metodológica de la Defensoría (`exigencias_por_
numeral.json`), y sólo del cruce de ambos sale un resultado.

LO QUE ESTE MÓDULO **NO** HACE, y es deliberado:

  · No mide un numeral cuya periodicidad la guía no declara (1.1, 3 y 12). Se marcan
    `no_determinable`. **Asignarles una cadencia por defecto sería inventar la vara** —
    justo el error que produjo el «3/12» presentado como si aplicara a todos.
  · No juzga el contenido de los archivos: la tríada puede estar publicada y vacía. Eso
    exige abrir el CSV y es una prueba distinta, posterior a ésta.
  · No convierte el resultado en puntaje ni en ICPI. La obligación determina qué puede
    medir el indicador, nunca al revés.

Uso:  python scripts/normativa/medir_lotaip.py [--anio 2025] [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes                    # noqa: E402

EXIGENCIAS = RAIZ / "data" / "lotaip" / "exigencias_por_numeral.json"
EVIDENCIA = RAIZ / "data" / "lotaip" / "dpe_montecristi.json"

# Cuántos períodos genera cada cadencia en un ejercicio, y a qué período pertenece un
# mes. Esto NO es criterio de QUIRA: es la lectura aritmética de la cadencia que la
# guía declara. Un numeral trimestral tiene cuatro oportunidades de cumplir, no doce.
CADENCIA = {
    "mensual":      (12, lambda m: m),
    "bimensual":    (6,  lambda m: (m - 1) // 2 + 1),
    "trimestral":   (4,  lambda m: (m - 1) // 3 + 1),
    "cuatrimestral":(3,  lambda m: (m - 1) // 4 + 1),
    "semestral":    (2,  lambda m: (m - 1) // 6 + 1),
    "anual":        (1,  lambda m: 1),
}

# El portal de la Defensoría etiqueta los conjuntos igual que la guía los desarrolla
# —`Numeral 5-22` para el bloque compartido, `1.1/1.2/1.3` para el numeral matriz—, de
# modo que la correspondencia es directa y no hay que inventarla. Lo único que se
# normaliza es el prefijo.
def _clave(etiqueta: str) -> str | None:
    e = etiqueta.strip()
    if not e.lower().startswith("numeral"):
        return None                      # Art. 24 GAD: otra obligación, otro artículo
    n = e.split(None, 1)[1].strip() if " " in e else ""
    return "5" if n == "5-22" else n or None


def _cadencia_aplicable(per: dict) -> tuple[str | None, str]:
    """Elige la cadencia con la que se mide, y dice por qué.

    Cuando la norma admite dos («semestral o anual, según varíen los contenidos») se
    mide con **la menos exigente**. No es indulgencia: es que la norma condiciona la
    cadencia a un hecho —que el contenido varíe— que QUIRA no observa. Medir con la
    más exigente atribuiría un incumplimiento que la norma no sostiene."""
    cont = per.get("contenidos") or []
    if not cont:
        return None, "la guía no declara periodicidad de contenidos para este numeral"
    if len(cont) == 1:
        return cont[0], "cadencia única declarada por la guía"
    menos = max(cont, key=lambda c: CADENCIA.get(c, (99, None))[0] * -1)
    return menos, (f"la guía admite «{' o '.join(cont)}» según varíe el contenido; se "
                   f"mide con la menos exigente porque QUIRA no observa esa variación")


def medir(anio: str, tope: int | None = None) -> dict:
    ex = json.loads(EXIGENCIAS.read_text(encoding="utf-8"))
    ev = json.loads(EVIDENCIA.read_text(encoding="utf-8"))
    exig = {n["numeral"]: n for n in ex["numerales"]}

    ent = ev["entidades"]["937"]
    blq = ent["anios"][anio]
    meses_eval = tope or blq["meses_evaluados"]

    # FILTRO EXPLORATORIO: dónde hay algo publicado. No concluye nada por sí solo.
    obs: dict[str, set[int]] = defaultdict(set)
    fuera: dict[str, set[int]] = defaultdict(set)
    for r in blq["registros"]:
        k = _clave(r["numeral"])
        (obs if k else fuera)[k or r["numeral"]].add(r["mes"])

    filas = []
    for num, e in exig.items():
        cad, razon = _cadencia_aplicable(e["periodicidad"])
        meses = sorted(obs.get(num, ()))
        if cad is None:
            filas.append({
                "numeral": num, "estado": "no_determinable",
                "razon": razon, "cadencia": None,
                "meses_con_publicacion": meses,
                # Se registra lo observado, pero **no se puntúa**: sin vara no hay
                # medición (Regla de Oro 3 aplicada a este dominio).
                "nota": "observado sin evaluar — falta la exigencia en el corpus",
            })
            continue

        n_per, cual = CADENCIA[cad]
        # Sólo cuentan los períodos ya vencidos dentro del tramo evaluado.
        exigidos = sorted({cual(m) for m in range(1, meses_eval + 1)})
        cubiertos = sorted({cual(m) for m in meses})
        faltan = [p for p in exigidos if p not in cubiertos]
        filas.append({
            "numeral": num, "cadencia": cad, "razon_cadencia": razon,
            "periodos_exigidos": exigidos, "periodos_cubiertos": cubiertos,
            "periodos_faltantes": faltan,
            "meses_con_publicacion": meses,
            "estado": ("cumple_periodicidad" if not faltan else
                       "sin_publicacion_alguna" if not cubiertos else
                       "incumple_periodicidad"),
            "obligacion": (e["obligacion"] or "")[:120],
        })

    orden = {"sin_publicacion_alguna": 0, "incumple_periodicidad": 1,
             "no_determinable": 2, "cumple_periodicidad": 3}
    filas.sort(key=lambda f: (orden[f["estado"]],
                              -len(f.get("periodos_faltantes") or []), f["numeral"]))

    # Art. 24 · obligación **específica** de los GAD. Se mide con su propia vara y se
    # reporta aparte: agregarla al art. 19 contaminaría ese indicador con obligaciones
    # que no le pertenecen (colega, 2026-08-17).
    a24 = ex.get("articulo_24_gad") or {}
    m24 = None
    if a24.get("secciones"):
        cad, razon = _cadencia_aplicable(a24.get("periodicidad") or {})
        meses = sorted(next((v for k, v in fuera.items() if "24" in k), set()))
        if cad:
            _, cual = CADENCIA[cad]
            exigidos = sorted({cual(m) for m in range(1, meses_eval + 1)})
            cubiertos = sorted({cual(m) for m in meses})
            faltan = [p for p in exigidos if p not in cubiertos]
            m24 = {"articulo": "24", "cadencia": cad, "razon_cadencia": razon,
                   "secciones": len(a24["secciones"]),
                   "campos_exigidos": sum(len(s["campos"]) for s in a24["secciones"]),
                   "periodos_exigidos": exigidos, "periodos_cubiertos": cubiertos,
                   "periodos_faltantes": faltan,
                   "meses_con_publicacion": meses,
                   "estado": ("cumple_periodicidad" if not faltan else
                              "sin_publicacion_alguna" if not cubiertos else
                              "incumple_periodicidad")}

    return {"anio": anio, "meses_evaluados": meses_eval, "numerales": filas,
            "articulo_24_gad": m24,
            "fuera_de_la_matriz": {k: sorted(v) for k, v in fuera.items()}}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anio", default="2025")
    ap.add_argument("--tope", type=int, help="último mes evaluable (2026 → 5)")
    ap.add_argument("--json", help="ruta donde volcar el resultado")
    args = ap.parse_args()

    d = medir(args.anio, args.tope)
    print(f"CUMPLIMIENTO LOTAIP · GAD Montecristi · {d['anio']} "
          f"(meses evaluados: {d['meses_evaluados']})")
    print("medido contra la periodicidad que declara la Guía Metodológica de la DPE, "
          "no contra un conteo uniforme\n")

    ico = {"sin_publicacion_alguna": "▓", "incumple_periodicidad": "▒",
           "no_determinable": "·", "cumple_periodicidad": " "}
    print(f"  {'':2}{'num':6}{'cadencia':12}{'exigidos':>9}{'cubiertos':>10}"
          f"{'faltan':>7}  obligación")
    print("  " + "─" * 96)
    for f in d["numerales"]:
        ex_ = len(f.get("periodos_exigidos") or [])
        cu = len(f.get("periodos_cubiertos") or [])
        fa = len(f.get("periodos_faltantes") or [])
        ob = f.get("obligacion") or f.get("razon", "")
        print(f"  {ico[f['estado']]} {f['numeral']:6}{str(f['cadencia'] or '—'):12}"
              f"{ex_ if f['cadencia'] else '—':>9}{cu if f['cadencia'] else '—':>10}"
              f"{fa if f['cadencia'] else '—':>7}  {ob[:44]}")
    print("  " + "─" * 96)
    print("  ▓ ni una sola publicación   ▒ publica, pero no en todos los períodos exigidos")
    print("  · la guía no declara periodicidad → NO se mide, no se puntúa como falta")

    from collections import Counter
    c = Counter(f["estado"] for f in d["numerales"])
    print("\n  RESULTADO")
    for k in ("sin_publicacion_alguna", "incumple_periodicidad",
              "cumple_periodicidad", "no_determinable"):
        if c.get(k):
            print(f"     {k:26} {c[k]:3} numerales")
    medibles = c.get("sin_publicacion_alguna", 0) + c.get("incumple_periodicidad", 0) \
        + c.get("cumple_periodicidad", 0)
    print(f"     {'—' * 26}")
    print(f"     medibles con la vara vigente {medibles} de {len(d['numerales'])}")

    m24 = d.get("articulo_24_gad")
    if m24:
        print(f"\n  ART. 24 · obligación específica de GAD (medida aparte, no se suma al 19)")
        print(f"     {m24['secciones']} secciones · {m24['campos_exigidos']} campos · "
              f"cadencia {m24['cadencia']}")
        print(f"     períodos exigidos {len(m24['periodos_exigidos'])} · "
              f"cubiertos {len(m24['periodos_cubiertos'])} · "
              f"faltan {len(m24['periodos_faltantes'])} → {m24['estado']}")
        if m24["periodos_faltantes"]:
            print(f"     sin publicación en los períodos: {m24['periodos_faltantes']}")

    inv = Invariantes(f"medición LOTAIP {d['anio']}")
    inv.cardinalidad("numerales evaluados", len(d["numerales"]), minimo=20)
    inv.cardinalidad("numerales medibles", medibles, minimo=15)
    print()
    inv.informe()

    if args.json:
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"_meta": {
            "vara": "Guía metodológica DPE · data/lotaip/exigencias_por_numeral.json",
            "evidencia": "portal de transparencia DPE · data/lotaip/dpe_montecristi.json",
            "regla": "filtro exploratorio ≠ criterio normativo ≠ resultado de cumplimiento",
            "limite": "mide publicación por período, NO el contenido del archivo: la "
                      "tríada puede estar publicada y vacía. Prueba distinta y posterior.",
        }, **d}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → {p}")


if __name__ == "__main__":
    main()
