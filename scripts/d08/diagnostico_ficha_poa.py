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

# ★ EL SUJETO (ampliación 2026-08-05 · Javo). Saber DÓNDE no basta: sin sujeto
# declarado, la intervención tampoco puede seguirse hasta el RESULTADO. Se mide en dos
# niveles porque no es lo mismo nombrar al destinatario que dimensionarlo.
RE_SUJETO = re.compile(
    r"\b(familias?|habitantes?|beneficiari|moradores?|pobladores?|usuarios?|estudiantes?"
    r"|ninos?|niñas?|adultos? mayores?|personas con discapacidad|grupos? de atencion prioritaria"
    r"|mujeres|jovenes|jóvenes|productores?|artesanos?)\b", re.I)
RE_SUJETO_CUANT = re.compile(
    r"\b\d{2,6}\s*(familias|habitantes|beneficiarios|personas|usuarios|moradores)\b", re.I)

# ★ LA CAUSA. Marca de intervención con financiador externo: es el contraste que explica
# por qué unas filas localizan y otras no (el requisito del tercero existe; el propio, no).
RE_FINANCIADOR = re.compile(r"\b(BDE|cr[ée]dito|contraparte|banco de desarrollo)\b", re.I)


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

    # ── AMPLIACIÓN 2026-08-05 · el SUJETO y la CAUSA (observación de Javo) ──────
    # Javo: "falta otra pregunta que pormenorice el territorio y el actor". Tenía razón:
    # medir solo el LUGAR deja fuera la mitad de la cadena. Una intervención sin sujeto
    # declarado tampoco puede seguirse hasta el RESULTADO, aunque se sepa dónde ocurre.
    con_sujeto = sum(1 for f in poa if RE_SUJETO.search(f["texto"]))
    con_sujeto_cuant = sum(1 for f in poa if RE_SUJETO_CUANT.search(f["texto"]))
    con_ambos = sum(1 for f in poa
                    if fo._territorios(f["texto"]) and RE_SUJETO.search(f["texto"]))

    # ── LA CAUSA · lo que eleva el hallazgo de descriptivo a explicativo ────────
    # Constitución CAPA 0: QUIRA no DETECTA la incoherencia (eso es QUADRUM), EXPLICA
    # su causalidad. La pregunta no es "¿cuántas filas localizan?" sino "¿QUÉ hace que
    # unas localicen y otras no?". Con financiador externo el requisito existe; con el
    # formato propio, no. El GAD sabe localizar — lo demuestra cuando se lo exigen.
    ext = [f for f in poa if RE_FINANCIADOR.search(f["texto"])]
    ext_loc = [f for f in ext if fo._territorios(f["texto"])]
    prop = [f for f in poa if not RE_FINANCIADOR.search(f["texto"])]
    prop_loc = [f for f in prop if fo._territorios(f["texto"])]

    def pct(x: int) -> str:
        return f"{x:>5}  ({x / n:>5.1%})"

    print(f"\n=== DIAGNÓSTICO DE LA FICHA POA · {n} filas · GAD Montecristi ===")
    print("    (consolidado de CUATRO planes operativos ANUALES: 2023 · 2024 · 2025 · 2026)\n")
    print("  ¿El instrumento permite seguir la intervención hasta el territorio?\n")
    print(f"  ¿QUÉ se hace?  · objeto sustantivo ......... {pct(con_objeto)}")
    print(f"  ¿DÓNDE se ejecuta? · unidad territorial .... {pct(con_territorio)}   ← decisiva")
    print(f"     ↳ corroboración independiente ........... {pct(con_marcador)}   (marcador de lugar)")
    print(f"  ¿SOBRE QUIÉN recae? · sujeto declarado ..... {pct(con_sujeto)}")
    print(f"     ↳ con la población CUANTIFICADA ......... {pct(con_sujeto_cuant)}")
    print(f"  AMBAS a la vez (dónde + sobre quién) ....... {pct(con_ambos)}   ← la cadena completa")
    print(f"  Solo clasificación presupuestaria .......... {pct(solo_clasificacion)}")
    # Se conserva por continuidad de OBS-020, con su nombre real: son componentes
    # OPERATIVOS de la intervención (residuos, seguridad, salud, vialidad), NO los
    # componentes del PDOT (biofísico, sociocultural…), cuya vinculación es ~100%.
    # Confundirlos fue un error de nomenclatura corregido hoy (Javo + asesoría).
    print(f"  [ref. OBS-020] rubro operativo reconocible . {pct(con_componente)}")

    print("\n  LA CAUSA — qué distingue a las filas que SÍ localizan:")
    r_ext = 100 * len(ext_loc) / len(ext) if ext else 0
    r_prop = 100 * len(prop_loc) / len(prop) if prop else 0
    print(f"    · con financiador externo (BDE/crédito/contraparte): "
          f"{len(ext_loc)} de {len(ext)}  ({r_ext:.1f}%)")
    print(f"    · solo con formato propio ........................: "
          f"{len(prop_loc)} de {len(prop)}  ({r_prop:.2f}%)")
    if r_prop:
        print(f"    → razón {r_ext / r_prop:.0f} a 1. El GAD SÍ sabe localizar el gasto: lo hace")
        print("      cuando un tercero lo exige. Lo que falta no es capacidad — es el")
        print("      requisito en su propio formato. (n=%d en el grupo externo: patrón" % len(ext))
        print("      fuertemente sugerido, no ley; se propone, el humano valida.)")

    print("\n  LECTURA (frontera Carta Art. 4.5 — no se afirma incumplimiento):")
    print(f"    · {1 - con_territorio / n:.0%} de las filas no permite saber DÓNDE se ejecuta el gasto,")
    print(f"      y {1 - con_ambos / n:.0%} no permite saber dónde Y sobre quién a la vez.")
    print("      La cadena PLAN→…→TERRITORIO no se puede recorrer POR CONSTRUCCIÓN del")
    print("      documento, no por falta de algoritmo.")
    print("\n  QUIRA no dictamina incumplimiento: localiza DÓNDE se rompe la cadena, explica")
    print("  POR QUÉ, y devuelve una decisión accionable — aquí, un campo en la ficha.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
