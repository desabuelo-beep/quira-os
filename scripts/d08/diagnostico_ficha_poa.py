# -*- coding: utf-8 -*-
"""
scripts/d08/diagnostico_ficha_poa.py — ¿La ficha POA permite monitorear el desarrollo?
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 4]
  type: TECNICA

HALLAZGO DE JAVO (2026-07-29), 15 años en gestión pública de GAD:

  "El problema real es la forma metodológica de construcción de la ficha de POA.
   Es una cuestión muy general que no aterriza las necesidades para un monitoreo
   y evaluación real e integral de la planificación del desarrollo cantonal."

Este script CONVIERTE ESA AFIRMACIÓN EN MEDIDA. No audita al GAD por incumplir —
audita si el instrumento de planificación **es apto para lo que la ley le pide**.

POR QUÉ IMPORTA
El cruce demanda↔POA se rompió tres veces seguidas, y las tres por la misma causa:
la fila del POA mezcla **clasificación presupuestaria** con **contenido sustantivo**
sin separarlos:

    partida · PROGRAMA · actividad · unidad responsable · monto

Cada capa de metadato que se filtra (REGLA 0 · homógrafos · programa) destapa la
siguiente. Eso deja de ser un defecto del algoritmo y pasa a ser una propiedad del
documento. NO se afirma por qué se construyó así — eso atribuiría intención institucional
y no está demostrado. Se afirma lo observable: la ficha no contiene información suficiente
para reconstruir territorialmente la ejecución mediante evidencia documental verificable.

LO QUE SE MIDE (por fila del POA, sin juicio de valor)
  1. ¿Declara OBJETO?     — hay una descripción sustantiva de qué se hace
  2. ¿Declara TERRITORIO? — se puede saber DÓNDE se ejecuta
  3. ¿Declara COMPONENTES operativos? — permite satisfacción instrumental
  4. ¿Solo clasificación presupuestaria? — partida + programa, sin objeto

La #2 es la decisiva: **sin ancla territorial no se puede verificar si una demanda
de un barrio fue atendida**. La trazabilidad territorial no falla por falta de
algoritmo: falla porque el dato no está en el documento.

FRONTERA (Carta Art. 4.5 · Principio de No-Inferencia)
No se afirma "el GAD incumple". Se certifica: **"el instrumento de planificación no
permite verificar la correspondencia entre demanda ciudadana y ejecución"**. Eso es
ausencia de habilitación documental — una de las tres categorías que QUIRA sí certifica.

Uso:  python scripts/d08/diagnostico_ficha_poa.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import filtro_ontologico as fo          # noqa: E402
from cruzar_demandas import cargar_poa  # noqa: E402

# Programas presupuestarios: clasificación, NO objeto de la intervención.
PROGRAMAS = ("urbanizacion y embellecimiento", "administracion general",
             "servicios sociales", "servicios comunales", "otros servicios",
             "servicios generales", "gestion ambiental", "desarrollo comunitario")

RE_MONTO = re.compile(r"\b\d{1,3}(?:[.,]\d{3})*[.,]\d{2}\b")

# ★ CORROBORACIÓN INDEPENDIENTE del ancla territorial.
# El conteo por registro de topónimos podría subestimar si el registro está incompleto.
# Este segundo método no depende de conocer NINGÚN nombre de lugar: si el POA localizara
# el gasto, usaría alguno de estos marcadores. Que ambos métodos converjan en ~1% es lo
# que convierte el hallazgo en afirmable (dos caminos, misma medida).
RE_MARCADOR_LUGAR = re.compile(
    r"\b(barrio|sector|comunidad|comuna|parroquia|sitio|recinto|ciudadela|km )\s+\w+", re.I)


def main() -> int:
    poa = cargar_poa(("2023", "2024", "2025", "2026"))
    if not poa:
        print("ERROR: sin POA")
        return 1

    n = len(poa)
    con_territorio = con_componente = solo_clasificacion = con_objeto = 0
    con_marcador = sum(1 for f in poa if RE_MARCADOR_LUGAR.search(f["texto"]))
    for fila in poa:
        t = fo._norm(fila["texto"])
        # se retira todo lo que es metadato para ver qué queda de sustantivo
        limpio = fo._sin_unidad_ejecutora(t)
        for pr in PROGRAMAS:
            limpio = limpio.replace(pr, " ")
        limpio = fo.RE_PARTIDA.sub(" ", limpio)
        limpio = RE_MONTO.sub(" ", limpio)
        resto = " ".join(limpio.split())

        if fo._territorios(fila["texto"]):
            con_territorio += 1
        if any(c in t for fam in fo.COMPONENTES_OPERATIVOS.values() for c in fam):
            con_componente += 1
        if len(resto) < 25:
            solo_clasificacion += 1
        else:
            con_objeto += 1

    def pct(x: int) -> str:
        return f"{x:>5}  ({x / n:>5.1%})"

    print(f"\n=== DIAGNÓSTICO DE LA FICHA POA · {n} filas · GAD Montecristi 2023-2026 ===\n")
    print("  ¿El instrumento permite monitorear la planificación del desarrollo?\n")
    print(f"  Declara OBJETO sustantivo .................. {pct(con_objeto)}")
    print(f"  Declara TERRITORIO de ejecución ............ {pct(con_territorio)}   ← decisiva")
    print(f"     ↳ corroboración independiente ........... {pct(con_marcador)}   (marcador de lugar)")
    print(f"  Declara COMPONENTES operativos ............. {pct(con_componente)}")
    print(f"  Solo clasificación presupuestaria .......... {pct(solo_clasificacion)}")

    print("\n  LECTURA (frontera Carta Art. 4.5 — no se afirma incumplimiento):")
    print(f"    · {1 - con_territorio / n:.0%} de las filas NO permite saber DÓNDE se ejecuta el gasto.")
    print("      Sin ancla territorial, verificar si la demanda de un barrio fue atendida")
    print("      es imposible POR CONSTRUCCIÓN del documento, no por falta de algoritmo.")
    print(f"    · {1 - con_componente / n:.0%} no declara componentes operativos → la satisfacción")
    print("      INSTRUMENTAL es inverificable (por eso el cruce arroja instrumental = 0:")
    print("      no es que no exista, es que el expediente no la declara).")
    print("\n  QUIRA certifica: AUSENCIA DE HABILITACIÓN DOCUMENTAL del instrumento de")
    print("  planificación para el monitoreo y evaluación que la ley le exige.")
    print("  NO certifica: que el GAD haya incumplido. Eso lo determina el órgano de control.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
