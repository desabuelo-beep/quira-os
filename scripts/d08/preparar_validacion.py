# -*- coding: utf-8 -*-
"""
scripts/d08/preparar_validacion.py — Validación experta del MRSPP (d08 · Fase 2b)
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: MARCO-TEORICO-001
  constitution_articles: [1, 3, 9]
  type: TECNICA

Javo no puede revisar 223 correspondencias a mano. Este instrumento las PRIORIZA y
convierte cada decisión suya en calibración del motor.

★ v2 (2026-07-29) — CAMBIA LA PREGUNTA. Antes se muestreaba por tramo de score y se
preguntaba "¿corresponde?", porque lo que se calibraba era un umbral. Con el MRSPP v3
lo que decide ya no es el score sino el TIPO DE SATISFACCIÓN, así que se muestrea por
NIVEL y la pregunta pasa a ser:

    "¿corresponde CON ESTE TIPO de satisfacción?"

Eso permite medir la precisión de CADA nivel por separado y ver cuál está mal
calibrado — un umbral global ya no diría nada útil.

Uso:
  python scripts/d08/preparar_validacion.py            → genera la muestra a validar
  python scripts/d08/preparar_validacion.py --aplicar  → lee el CSV validado y calibra
Dylus Lab © 2026
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
TRAZA = REPO / "data" / "d08" / "trazabilidad_demandas.json"
CSV_VAL = REPO / "data" / "d08" / "validacion_experta.csv"

# Niveles del MRSPP que se validan (nula no se muestrea: es la ausencia)
TIPOS = ["directa", "funcional", "complementaria", "instrumental"]
POR_TIPO = 8           # ~30 decisiones, no 223

COL = "¿CORRECTO? (si/no/otro-tipo)"


def tipo_de(r: dict) -> str:
    """Tipo MRSPP declarado en el expediente ('directa: ...' → 'directa')."""
    return (r.get("filtro_ontologico") or "nula").split(":")[0].strip()


def generar() -> int:
    t = json.loads(TRAZA.read_text(encoding="utf-8"))["trazabilidad"]
    con_correlato = [r for r in t if r["estado_epistemico"] != "sin_correlato"]

    # prioriza vinculantes (COOTAD 238): su incorporación es EXIGIBLE
    por_tipo: dict[str, list] = defaultdict(list)
    for r in sorted(con_correlato,
                    key=lambda x: (x["naturaleza_juridica"] != "vinculante", -x["similitud"])):
        por_tipo[tipo_de(r)].append(r)

    muestra = []
    for tp in TIPOS:
        muestra += por_tipo[tp][:POR_TIPO]

    with open(CSV_VAL, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["#", "TIPO MRSPP", "SCORE", "VINCULANTE", "DEMANDA CIUDADANA",
                    "PROYECTO DEL POA", "POR QUÉ EL MOTOR LO CLASIFICÓ ASÍ",
                    COL, "NOTA DE JAVO"])
        for i, r in enumerate(muestra, 1):
            w.writerow([i, tipo_de(r).upper(), r["similitud"],
                        "SÍ" if r["naturaleza_juridica"] == "vinculante" else "no",
                        r["demanda"][:170],
                        (r["proyecto_poa_mas_proximo"] or "(ninguno)")[:170],
                        r["filtro_ontologico"][:130], "", ""])

    print("=== VALIDACIÓN EXPERTA · MRSPP v3 ===")
    print()
    print(f"  Generado: {CSV_VAL.relative_to(REPO)}")
    print(f"  {len(muestra)} correspondencias a validar (de {len(con_correlato)} con correlato)")
    print()
    print("  Muestreo por TIPO DE SATISFACCIÓN — se mide si cada NIVEL clasifica bien:")
    for tp in TIPOS:
        disp = len(por_tipo[tp])
        print(f"    {tp:16} {min(disp, POR_TIPO):>2} muestras   (de {disp} disponibles)")
    print()
    print("  CÓMO SE VALIDA (Javo):")
    print("    1. Abrir el CSV en Excel (separador ';').")
    print("    2. En '¿CORRECTO?' escribir:")
    print("         si   -> el tipo asignado es el correcto")
    print("         no   -> no hay relación alguna (debió ser NULA)")
    print("         directa | funcional | instrumental | complementaria")
    print("              -> sí hay relación, pero es de OTRO tipo")
    print("    3. Guardar y ejecutar:  python scripts/d08/preparar_validacion.py --aplicar")
    print()
    print("  Con ~30 decisiones se mide la precisión de CADA nivel del MRSPP,")
    print("  no un umbral global. Ahí se ve qué nivel está mal calibrado.")
    return 0


def aplicar() -> int:
    if not CSV_VAL.exists():
        print("ERROR: no existe el CSV. Ejecutar primero sin --aplicar.")
        return 1
    filas = list(csv.DictReader(open(CSV_VAL, encoding="utf-8-sig"), delimiter=";"))
    validas = ("si", "sí", "no") + tuple(TIPOS)
    validadas = [f for f in filas if (f.get(COL) or "").strip().lower() in validas]
    if not validadas:
        print("Aún no hay validaciones. Complete la columna '¿CORRECTO?' y vuelva a ejecutar.")
        return 0

    # ok = el tipo era correcto · nula = no había relación · confusion = era otro tipo
    res: dict[str, dict] = defaultdict(lambda: {"ok": 0, "nula": 0, "confusion": 0})
    confusiones: Counter = Counter()
    for f in validadas:
        v = (f[COL] or "").strip().lower().replace("sí", "si")
        tp = (f["TIPO MRSPP"] or "").strip().lower()
        if v == "si":
            res[tp]["ok"] += 1
        elif v == "no":
            res[tp]["nula"] += 1
        else:
            res[tp]["confusion"] += 1
            confusiones[f"{tp} -> {v}"] += 1

    print(f"=== CALIBRACIÓN DEL MRSPP · {len(validadas)} decisiones de Javo ===")
    print()
    print(f"  {'NIVEL':16} {'OK':>5} {'NULA':>7} {'OTRO':>7}   PRECISIÓN")
    debiles = []
    for tp in TIPOS:
        d = res.get(tp)
        n = d and (d["ok"] + d["nula"] + d["confusion"])
        if not n:
            continue
        prec = d["ok"] / n
        print(f"  {tp:16} {d['ok']:>5} {d['nula']:>7} {d['confusion']:>7}   {prec:.0%}")
        if prec < 0.80:
            debiles.append((tp, prec, d))

    if confusiones:
        print()
        print("  CONFUSIONES ENTRE NIVELES (hay relación, el motor erró el tipo):")
        for k, n in confusiones.most_common():
            print(f"    {k:38} {n}")

    print()
    print("  DIAGNÓSTICO:")
    if not debiles:
        print("    Todos los niveles >=80%. El MRSPP está calibrado: se puede automatizar")
        print("    el resto con validación por muestreo.")
    else:
        for tp, prec, d in debiles:
            if d["nula"] >= d["confusion"]:
                print(f"    · '{tp}' {prec:.0%} — FALSOS POSITIVOS ({d['nula']} sin relación real):")
                print("      endurecer su regla en filtro_ontologico.py + añadir el caso al test.")
            else:
                print(f"    · '{tp}' {prec:.0%} — CONFUSIÓN DE NIVEL ({d['confusion']} casos):")
                print("      la relación existe; falta precisión en el criterio que separa niveles.")
        print()
        print("    NO se automatiza un nivel por debajo de 80%: se corrige la regla primero.")

    print()
    print("  Las decisiones quedan en el CSV como registro trazable (Constitución Art. 3).")
    return 0


if __name__ == "__main__":
    raise SystemExit(aplicar() if "--aplicar" in sys.argv else generar())
