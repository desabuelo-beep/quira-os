# -*- coding: utf-8 -*-
"""
scripts/d08/preparar_validacion.py — Instrumento de validación experta (d08 · Fase 2b)
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: MARCO-TEORICO-001
  constitution_articles: [1, 3, 9]
  type: TECNICA

Javo no puede revisar 223 correspondencias a mano. Este instrumento las PRIORIZA y
las prepara para validación humana eficiente — y, sobre todo, **convierte cada
decisión suya en calibración del motor**: no es revisar por revisar, es enseñarle
al sistema dónde está el umbral real.

CÓMO FUNCIONA (construido para decidir rápido)
  1. Prioriza: primero las VINCULANTES (COOTAD 238, incorporación exigible) y las
     que están en la banda de decisión (0.52-0.62), donde el juicio humano vale más.
  2. Muestrea por estratos: no se validan 223 — se validan ~30 bien elegidas, y de
     ahí sale la tasa real de aciertos por tramo de score.
  3. Produce un CSV editable: Javo escribe `si` / `no` / `duda` en una columna.
  4. Al reimportarlo (`--aplicar`), calcula precisión por tramo y RECOMIENDA los
     umbrales reales — la calibración deja de ser una suposición.

ESTO ES AUTOMATIZAR CONSTRUYENDO JUNTOS: el humano no valida para siempre; valida
una muestra, el sistema aprende dónde cortar, y el resto se automatiza con umbral
fundado en evidencia — no en un número copiado de otro dominio.

Uso:
  python scripts/d08/preparar_validacion.py            → genera la muestra a validar
  python scripts/d08/preparar_validacion.py --aplicar  → lee el CSV validado y calibra
Dylus Lab © 2026
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
TRAZA = REPO / "data" / "d08" / "trazabilidad_demandas.json"
CSV_VAL = REPO / "data" / "d08" / "validacion_experta.csv"

# Tramos de score: se muestrea en TODOS para medir precisión en cada uno.
TRAMOS = [(0.70, 1.01, "alto"), (0.62, 0.70, "fuerte"),
          (0.56, 0.62, "banda_alta"), (0.52, 0.56, "banda_baja"),
          (0.40, 0.52, "bajo")]
POR_TRAMO = 6          # muestras por tramo → ~30 decisiones, no 223


def tramo_de(score: float) -> str:
    for lo, hi, nombre in TRAMOS:
        if lo <= score < hi:
            return nombre
    return "muy_bajo"


def generar() -> int:
    t = json.loads(TRAZA.read_text(encoding="utf-8"))["trazabilidad"]
    # prioriza vinculantes (COOTAD 238): su incorporación es EXIGIBLE
    por_tramo: dict[str, list] = defaultdict(list)
    for r in sorted(t, key=lambda x: (x["naturaleza_juridica"] != "vinculante", -x["similitud"])):
        por_tramo[tramo_de(r["similitud"])].append(r)

    muestra = []
    for _, _, nombre in TRAMOS:
        muestra += por_tramo[nombre][:POR_TRAMO]

    with open(CSV_VAL, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["#", "TRAMO", "SCORE", "VINCULANTE", "DEMANDA CIUDADANA",
                    "PROYECTO POA MÁS PRÓXIMO", "¿CORRESPONDE? (si/no/duda)", "NOTA DE JAVO"])
        for i, r in enumerate(muestra, 1):
            w.writerow([i, tramo_de(r["similitud"]), r["similitud"],
                        "SÍ" if r["naturaleza_juridica"] == "vinculante" else "no",
                        r["demanda"][:160],
                        r["proyecto_poa_mas_proximo"][:160] or "(sin proyecto próximo)",
                        "", ""])

    print(f"=== INSTRUMENTO DE VALIDACIÓN EXPERTA ===\n")
    print(f"  Generado: {CSV_VAL.relative_to(REPO)}")
    print(f"  {len(muestra)} correspondencias a validar (de {len(t)} totales)\n")
    print("  Muestreo por tramo de score — para medir precisión en CADA tramo:")
    for _, _, nombre in TRAMOS:
        print(f"    {nombre:12} {min(len(por_tramo[nombre]), POR_TRAMO)} muestras "
              f"(de {len(por_tramo[nombre])} disponibles)")
    print("\n  INSTRUCCIONES PARA JAVO:")
    print("    1. Abrir el CSV en Excel (separador ';').")
    print("    2. En '¿CORRESPONDE?' escribir: si · no · duda")
    print("       → ¿el proyecto del POA responde REALMENTE a esa demanda ciudadana?")
    print("    3. Guardar y ejecutar:  python scripts/d08/preparar_validacion.py --aplicar")
    print("\n  Con ~30 decisiones suyas el sistema calcula el umbral REAL y automatiza el resto.")
    return 0


def aplicar() -> int:
    if not CSV_VAL.exists():
        print("ERROR: no existe el CSV. Ejecutar primero sin --aplicar.")
        return 1
    filas = list(csv.DictReader(open(CSV_VAL, encoding="utf-8-sig"), delimiter=";"))
    col = "¿CORRESPONDE? (si/no/duda)"
    validadas = [f for f in filas if (f.get(col) or "").strip().lower() in ("si", "sí", "no", "duda")]
    if not validadas:
        print("Aún no hay validaciones. Complete la columna '¿CORRESPONDE?' y vuelva a ejecutar.")
        return 0

    por_tramo: dict[str, dict] = defaultdict(lambda: {"si": 0, "no": 0, "duda": 0})
    for f in validadas:
        v = (f[col] or "").strip().lower().replace("sí", "si")
        por_tramo[f["TRAMO"]][v] += 1

    print(f"=== CALIBRACIÓN CON {len(validadas)} DECISIONES DE JAVO ===\n")
    print(f"  {'TRAMO':13} {'✓ SÍ':>6} {'✗ NO':>6} {'? DUDA':>7}   PRECISIÓN")
    umbral_recomendado = None
    for _, _, nombre in TRAMOS:
        d = por_tramo.get(nombre)
        if not d or not (d["si"] + d["no"]):
            continue
        prec = d["si"] / (d["si"] + d["no"])
        print(f"  {nombre:13} {d['si']:>6} {d['no']:>6} {d['duda']:>7}   {prec:.0%}")
        if prec >= 0.80 and umbral_recomendado is None:
            umbral_recomendado = nombre

    print("\n  RECOMENDACIÓN (fundada en evidencia, no en suposición):")
    if umbral_recomendado:
        lo = next(l for l, h, n in TRAMOS if n == umbral_recomendado)
        print(f"    Umbral de auto-aceptación: score >= {lo}  (precisión >= 80% en '{umbral_recomendado}')")
        print(f"    Por debajo → mantener validación humana.")
    else:
        print("    Ningún tramo alcanza 80% de precisión: el cruce necesita mejor señal")
        print("    (limpiar OCR de las demandas o enriquecer el texto del POA) antes de automatizar.")
    print("\n  Las decisiones quedan en el CSV como registro trazable de la validación experta.")
    return 0


if __name__ == "__main__":
    raise SystemExit(aplicar() if "--aplicar" in sys.argv else generar())
