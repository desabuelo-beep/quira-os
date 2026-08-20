# -*- coding: utf-8 -*-
"""
scripts/normativa/extraer_matriz_calificacion.py — qué se califica en cada numeral
══════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-20). Javo, tras corregir la ontología del dominio:

> *«Aquí no nos inventamos nada, todo está listo en los documentos técnicos de la
> DPE. Este DOM debe quedar impoluto e inexpugnable como base para los demás.»*

La auditoría de `scoring.py` contra el Instructivo le dio la razón en el
parámetro más delicado. Tres de los cuatro coincidían con la norma; el cuarto no:

    CTA  1,0 completa y actualizada · 0,5 incompleta O desactualizada · 0,0 sin
         información                                              ✅ coincidía
    ETA  1 tres estrellas · 0 sin información                      ✅ coincidía
    RP   1 dentro del plazo · 0 fuera                              ✅ coincidía
    CI   ⛔ el motor exigía los TRES parámetros cualitativos a TODOS los
         numerales. **El Instructivo los asigna uno por uno.**

El Anexo 1 del Instructivo trae la matriz de calificación: para cada numeral,
qué parámetros se evalúan. `Vigencia de la información` sólo aplica a los
numerales 16 y 18; `Validez de la información` sólo a 3 y 6; `Estado de
verificables` a 24 de 26 —no al 2 ni al 4—. Exigirlos todos a todos penalizaba
al sujeto observado por criterios que la norma no le aplica.

Es un dato adicional: **el Anexo 1 lista los numerales 5 y 22 como filas
separadas**, lo que confirma por vía independiente la corrección que Javo hizo
sobre la vara ese mismo día.

QUÉ HACE. Lee el Anexo 1 y produce la matriz de calificación por numeral. No
interpreta, no completa y no reparte: lo que la tabla marca, se registra; lo que
deja en blanco, se declara como no aplicable.

Uso:  python scripts/normativa/extraer_matriz_calificacion.py [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import config                                              # noqa: E402

_FUENTE = (config.DATOS_DIR / "Normativa_Word" /
           "LOTAIP - Instructivo-monitoreo-transparencia-activa-2024.docx")
_SALIDA = RAIZ / "data" / "lotaip" / "matriz_calificacion.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Las columnas del Anexo 1, en el orden en que el Instructivo las dispone. Los
# tres primeros son los parámetros CUANTITATIVOS —se califican siempre— y los
# tres últimos los CUALITATIVOS, que se marcan «SI» sólo donde aplican.
CUANTITATIVOS = ("informacion_completa_y_actualizada", "datos_abiertos",
                 "registro_dentro_del_plazo")
CUALITATIVOS = ("estado_de_verificables", "vigencia_de_la_informacion",
                "validez_de_la_informacion")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def extraer() -> dict:
    from docx import Document
    doc = Document(str(_FUENTE))

    filas: list[list[str]] = []
    for t in doc.tables:
        cab = [c.text.strip() for c in t.rows[0].cells]
        # La tabla del Anexo 1 se reconoce por su estructura, no por su posición:
        # el documento la parte en varias tablas consecutivas.
        if not cab or "Numeral" not in cab[0] or len(cab) < 9:
            continue
        for r in t.rows[1:]:
            v = [c.text.strip() for c in r.cells]
            if v[0] and v[0][0].isdigit():
                filas.append(v)

    numerales = []
    for v in filas:
        num = v[0].split()[0].strip(".")
        aplica = {}
        for k, col in enumerate(CUALITATIVOS, start=6):
            valor = (v[k] if k < len(v) else "").strip().upper()
            aplica[col] = valor == "SI"
        numerales.append({
            "numeral": num,
            "formato_para_difusion": v[2][:180],
            # Los cuantitativos se califican SIEMPRE: la tabla les pone 1 en
            # todas las filas porque es el valor máximo alcanzable, no una marca
            # de aplicabilidad.
            "parametros_cuantitativos": list(CUANTITATIVOS),
            "parametros_cualitativos_aplicables": [k for k, v_ in aplica.items() if v_],
            "no_aplicables": [k for k, v_ in aplica.items() if not v_],
        })

    # Un numeral puede aparecer varias veces (el 1 tiene tres formatos de
    # difusión). Se consolidan sus parámetros: si alguno de sus formatos exige un
    # parámetro, el numeral lo exige.
    consolidado: dict[str, dict] = {}
    for n in numerales:
        d = consolidado.setdefault(n["numeral"], {
            "numeral": n["numeral"], "formatos": [],
            "parametros_cuantitativos": list(CUANTITATIVOS),
            "parametros_cualitativos_aplicables": [],
        })
        d["formatos"].append(n["formato_para_difusion"])
        for p in n["parametros_cualitativos_aplicables"]:
            if p not in d["parametros_cualitativos_aplicables"]:
                d["parametros_cualitativos_aplicables"].append(p)

    return {
        "_meta": {
            "fuente": _FUENTE.name,
            "sha256": _sha(_FUENTE),
            "norma": "Instructivo para evaluar el nivel de cumplimiento de los "
                     "parámetros técnicos de la transparencia activa · Defensoría "
                     "del Pueblo, 2024",
            "seccion": "Anexo No. 1 · Formatos de evaluación",
            "regla": "lo que la tabla marca se registra; lo que deja en blanco se "
                     "declara NO APLICABLE. QUIRA no reparte ni completa.",
            "por_que": "el motor exigía los tres parámetros cualitativos a todos "
                       "los numerales; el Instructivo los asigna uno por uno",
            "generado": _dt.date.today().isoformat(),
            "numerales": len(consolidado),
            "filas_del_anexo": len(filas),
        },
        "numerales": sorted(consolidado.values(),
                            key=lambda d: (len(d["numeral"]), d["numeral"])),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", help="ruta donde volcar la matriz")
    args = ap.parse_args()

    if not _FUENTE.exists():
        print(f"⛔ no se halla el Instructivo en {_FUENTE}")
        sys.exit(2)

    m = extraer()
    print("MATRIZ DE CALIFICACIÓN · Anexo 1 del Instructivo DPE 2024")
    print(f"qué parámetros se evalúan en cada numeral · {m['_meta']['numerales']} numerales\n")

    from collections import Counter
    cuenta = Counter()
    for n in m["numerales"]:
        for p in n["parametros_cualitativos_aplicables"]:
            cuenta[p] += 1
    print("  PARÁMETROS CUALITATIVOS · a cuántos numerales aplica cada uno")
    for p in CUALITATIVOS:
        quienes = [n["numeral"] for n in m["numerales"]
                   if p in n["parametros_cualitativos_aplicables"]]
        detalle = ("todos menos " +
                   ", ".join(n["numeral"] for n in m["numerales"]
                             if p not in n["parametros_cualitativos_aplicables"])
                   ) if len(quienes) > len(m["numerales"]) / 2 else ", ".join(quienes)
        print(f"     {p:32} {cuenta[p]:3}   {detalle[:44]}")

    print(f"\n  ⚠ el motor exigía los TRES a los {m['_meta']['numerales']} numerales")

    if args.json:
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  → {p.relative_to(RAIZ) if p.is_absolute() else p}")
        print(f"  sha256 de la fuente: {m['_meta']['sha256'][:32]}…")


if __name__ == "__main__":
    main()
