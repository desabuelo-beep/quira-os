# -*- coding: utf-8 -*-
"""
scripts/gm_omega/carta_rearquitectura.py — QUIRA-NEXT · CARTA DE REARQUITECTURA

    El refactor es INTEGRAL, de fondo y forma, sobre todo el ecosistema —
    desde el Excel hacia adelante. Y por eso mismo necesita plan antes que
    ejecución.

    POR QUÉ EXISTE. Javo, 2026-09-05:

        «Lo histórico no es la verdad absoluta o una camisa de fuerza que se
         deba continuar […] esto merece una planificación integral para
         hacerlo bien, sin dañar lo que es válido.»

    ⚠️ Y LA PRUEBA DE QUE HACÍA FALTA la dio esta dirección en el acto: ante
    el ejemplo «quitar la palabra auditoría de la documentación», empezó a
    ejecutarlo. Medido después: **609 ocurrencias en 233 archivos**, y no son
    la misma palabra —`auditoría CGE` es norma citada, `auditoría` como nombre
    de GM-Ω sí cambia, `auditable` es una propiedad que se conserva—. Un
    reemplazo sin clasificar previa habría borrado artículos de ley.

    ESTA CARTA NO EJECUTA NADA. Ordena: qué existe, en qué categoría cae cada
    pieza, qué se puede decidir hoy y qué espera al dictamen `011-C4`.

    ⚠️ EL GOLD MASTER SIGUE CONGELADO. Planificar el refactor no adelanta el
    momento de intervenir el motor.

Uso:  python scripts/gm_omega/carta_rearquitectura.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "QUIRA-NEXT_CARTA_REARQUITECTURA.md"

# ── LAS CINCO CATEGORÍAS ──────────────────────────────────────────────────
#
# El núcleo de la carta, y la regla que impide «dañar lo que es válido»:
# ninguna pieza del ecosistema se toca antes de clasificarla. Las propuso el
# colega y son la corrección a una formulación anterior demasiado gruesa
# —«donde no hay razón documentada, no hay nada que respetar»—, que empujaba
# al extremo contrario del sesgo conservador que venía a corregir.
_CATEGORIAS = [
    ("HISTÓRICO", "🏛️",
     "existió y ya no opera",
     "se PRESERVA como trazabilidad — nunca se borra",
     "el nombre `SIAP`, `QUADRUM`, `TERRA`; `ICPI_v1`; las versiones "
     "superadas de los expedientes"),
    ("NORMATIVO VIGENTE", "⚖️",
     "lo fija una norma en vigor",
     "se ACATA mientras siga vigente — no es decisión de diseño",
     "`R_i`↔COOTAD 54-55 · `V_i`↔LOTAIP 7 · `T_i`↔COPFP 115-117 + Acuerdo "
     "067 MEF · `P_i`↔COPFP 54 · las cuatro infracciones de `C_i`"),
    ("EMPÍRICAMENTE ÚTIL", "🔬",
     "funciona y hay evidencia de que funciona",
     "se CONSERVA si supera validación — y hay que poder mostrar cuál",
     "el producto lógico de `V_i` (un silo en cero anula la meta); la "
     "jerarquía de fuentes de `T_i`; los cuatro silos"),
    ("DECISIÓN DE DISEÑO ANTIGUA", "🔧",
     "se eligió, no se dedujo; y nadie escribió por qué",
     "queda ABIERTA a rediseño — ni válida ni inválida por antigüedad",
     "los pesos `0,10/0,15/0,05/0,50`; el piso `0,50`; la residencia de "
     "cada índice en su dominio; la escala AVEP"),
    ("SUPERADO METODOLÓGICAMENTE", "📜",
     "fue correcto en su momento y el conocimiento actual lo desplazó",
     "se conserva como ANTECEDENTE, no como regla",
     "`C_i` = imputabilidad orgánica frente a `C_i` = calidad de proceso; "
     "«Cumplimiento Institucional» como nombre del ICPI"),
]

# ── LOS DIEZ EJES ─────────────────────────────────────────────────────────
#
# Del colega. Se auditan SIMULTÁNEAMENTE porque un refactor que arregle la
# ontología sin tocar el frontend produce un sistema que dice una cosa y
# muestra otra — que es el defecto que GM-Ω lleva toda la investigación
# documentando en el propio instrumento.
_EJES = [
    ("A", "Ontología", "¿qué cosas existen en QUIRA?",
     "Constitución §CAPA 0 · `T1`/`T2` cerrados"),
    ("B", "Taxonomía", "¿cómo se llaman y cómo se agrupan?",
     "`T1`-`T6` · 43 nombres clasificados · `T6` espera al dictamen"),
    ("C", "Metodología", "¿qué significa cada indicador?",
     "`011-C2` ✅ para los 6 factores · falta para los otros 11 índices"),
    ("D", "Datos", "¿qué fuente alimenta cada dato?",
     "`004` matriz de procedencia · 150 celdas"),
    ("E", "Gold Master", "¿cómo se representa canónicamente?",
     "⚠️ CONGELADO hasta `011-C4`"),
    ("F", "Código", "¿la implementación coincide con la ontología?",
     "`DOC-016`: la ontología gobierna a la implementación"),
    ("G", "Dominios", "¿cada indicador vive donde corresponde?",
     "`R0`/`R1`/`R2` · 23 de 48 celdas `POR_DECLARAR`"),
    ("H", "Frontend", "¿la interfaz representa la arquitectura?",
     "sin frente · Bloomberg Firewall vigente"),
    ("I", "Narrativa", "¿QUIRA explica bien lo que mide?",
     "sin frente · es el salto de dashboard a inteligencia pública"),
    ("J", "Escalabilidad LATAM", "¿qué es Ecuador y qué es generalizable?",
     "`010` · siguiente en la ruta"),
]


def inventario() -> list[tuple[str, str, int, bool]]:
    """Sobre cuántos artefactos actúa el refactor. Se cuenta, no se estima:
    un plan que no sabe su tamaño no es un plan.

    ⚠️ EL ÚLTIMO CAMPO DICE SI LA FILA SUMA AL TOTAL. `ADR` y `PCD` viven
    DENTRO de `docs/`, así que sumarlos los contaría dos veces. La primera
    versión de esta carta publicó 1371 en vez de 936 por exactamente eso — un
    dato inflado, en un documento cuyo objeto es no falsear datos."""
    def n(patron: str, raiz: str = ".") -> int:
        base = _RAIZ / raiz
        if not base.exists():
            return 0
        return sum(1 for p in base.rglob(patron)
                   if "historico" not in p.parts and ".git" not in p.parts)

    return [
        ("CANON", "documentos `docs/**/*.md`", n("*.md", "docs"), True),
        ("CANON", "  ↳ de los cuales, `ADR`", n("*.md", "docs/adr"), False),
        ("CANON", "  ↳ de los cuales, `PCD` de dominio",
         n("*.md", "docs/pcd"), False),
        ("CANON", "reglas de negocio `brn/*.yaml`", n("*.yaml", "docs/brn"),
         True),
        ("CANON", "gobernanza", n("*.md", "governance"), True),
        ("CANON", "marco teórico", n("*.md", "marco_teorico"), True),
        ("CÓDIGO", "módulos de aplicación", n("*.py", "app"), True),
        ("CÓDIGO", "páginas de interfaz", n("*.py", "quira_pages"), True),
        ("CÓDIGO", "scripts", n("*.py", "scripts"), True),
        ("CÓDIGO", "pruebas `tests/test_*.py`", n("test_*.py", "tests"), True),
        ("DATOS", "snapshots", n("*.json", "data"), True),
    ]


def main() -> int:
    inv = inventario()
    total = sum(c for _g, _d, c, suma in inv if suma)
    print(f"{total} artefactos · más 123 hojas del Gold Master · 13 dominios "
          f"· 12 índices")
    for grupo, desc, cuenta, suma in inv:
        print(f"  {grupo:<8} {desc:<38} {cuenta:>5}{'' if suma else '  (no suma)'}")
    _escribir(inv, total)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(inv, total) -> None:
    o: list[str] = []
    A = o.append

    A("# QUIRA-NEXT · CARTA DE REARQUITECTURA")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/carta_rearquitectura.py`. El **inventario** se cuenta "
      "del repositorio; las **categorías y los ejes** se declaran, porque son "
      "un juicio de dirección.")
    A("")
    A("> ### Qué es esto")
    A("> El plan del **refactor integral de fondo y forma de todo el "
      "ecosistema** — desde el Excel hacia adelante. **No ejecuta nada.** "
      "Ordena qué existe, en qué categoría cae cada pieza, y qué se puede "
      "decidir hoy.")
    A("")
    A("⚠️ **El Gold Master sigue congelado hasta `011-C4`.** Planificar el "
      "refactor **no adelanta** el momento de intervenir el motor. Y el "
      "baseline **27,4582 %** no se mueve.")
    A("")

    A("## Por qué existe esta carta")
    A("")
    A("Javo, 2026-09-05:")
    A("")
    A("> *«Lo histórico no es la verdad absoluta o una camisa de fuerza que se "
      "deba continuar […] esto merece una planificación integral para hacerlo "
      "bien, sin dañar lo que es válido.»*")
    A("")
    A("### ⚠️ Y la prueba de que hacía falta la dio esta dirección en el acto")
    A("")
    A("Ante el ejemplo *«quitar la palabra auditoría de la documentación»*, "
      "esta dirección **empezó a ejecutarlo** en vez de leerlo como lo que "
      "era: una muestra del NIVEL del refactor. Javo lo detuvo.")
    A("")
    A("Lo medido antes de parar:")
    A("")
    A("```")
    A("  «auditoría» →  609 ocurrencias  ·  233 archivos")
    A("```")
    A("")
    A("Y **no son la misma palabra**:")
    A("")
    A("| Uso | Ejemplo | Tratamiento |")
    A("|---|---|---|")
    A("| **auditoría CGE / Contraloría** | «observación formal de auditoría "
      "CGE», `NCI 406-01` | ⚖️ **norma citada — intocable** |")
    A("| **QUIRA descrita como auditoría** | «QUIRA audita la gobernanza» | "
      "🔧 **sí cambia** — `BOOT` ya dice ⛔ «NO es auditoría ni "
      "observatorio» |")
    A("| **GM-Ω descrita como auditoría** | «esta auditoría cometió…» | 🔧 "
      "**sí cambia** — es un peritaje |")
    A("| **`auditable` / `auditabilidad`** | «cadena auditable» | 🔬 "
      "**se conserva** — es la propiedad que QUIRA certifica |")
    A("")
    A("> Un reemplazo sin clasificación previa **habría borrado artículos de "
      "ley**. Eso es exactamente «dañar lo que es válido», y ocurrió en el "
      "primer minuto del primer ejemplo.")
    A("")
    A("Y hay algo peor, que conviene decir: **`governance/BOOT.md` ya declara "
      "desde el 2026-08-05 que QUIRA «⛔ NO es auditoría ni observatorio»**. "
      "La regla existía; el vocabulario del repositorio no la siguió. Es el "
      "mismo patrón que `DOC-013` —el canon dice una cosa y la práctica "
      "deriva— y es la razón de fondo por la que este refactor es necesario.")
    A("")

    # ── Las cinco categorías ──────────────────────────────────────────────
    A("## ★ 1 · Las cinco categorías · la regla que impide dañar lo válido")
    A("")
    A("**Ninguna pieza del ecosistema se toca antes de clasificarla.** Y la "
      "clasificación no es opinable: cada categoría tiene una prueba distinta.")
    A("")
    A("| | Categoría | Qué es | Qué se hace con ella |")
    A("|---|---|---|---|")
    for nombre, icono, que_es, tratamiento, _ej in _CATEGORIAS:
        A(f"| {icono} | **{nombre}** | {que_es} | {tratamiento} |")
    A("")
    A("### Ejemplos ya identificados por `GM-Ω`")
    A("")
    for nombre, icono, _q, _t, ejemplos in _CATEGORIAS:
        A(f"**{icono} {nombre}** — {ejemplos}")
        A("")
    A("### La corrección que esta tabla incorpora")
    A("")
    A("Una versión anterior de `DOC-027` decía:")
    A("")
    A("> ~~«Donde no hay razón documentada, no hay nada que respetar.»~~")
    A("")
    A("El colega la corrigió, y con razón: **empujaba al extremo contrario** "
      "del sesgo conservador que venía a corregir. La formulación rigurosa es:")
    A("")
    A("> Donde no existe justificación documental de una decisión de diseño, "
      "esa decisión **no adquiere autoridad metodológica por antigüedad**; su "
      "permanencia debe **evaluarse nuevamente** frente al fenómeno, la "
      "teoría, la evidencia, la norma y la arquitectura actual.")
    A("")
    A("La diferencia es toda: una decisión antigua sin justificación **no es "
      "automáticamente incorrecta**. Tampoco automáticamente correcta. Queda "
      "**abierta**, que es un estado distinto de ambos.")
    A("")

    # ── El inventario ─────────────────────────────────────────────────────
    A("## 2 · Sobre qué actúa · el tamaño real")
    A("")
    A("Un plan que no sabe su tamaño no es un plan. Contado del repositorio:")
    A("")
    A("| Grupo | Artefactos | Cuenta |")
    A("|---|---|---:|")
    for grupo, desc, cuenta, suma in inv:
        marca = f"**{cuenta}**" if suma else f"*{cuenta}*"
        A(f"| {grupo} | {desc} | {marca} |")
    A(f"| | **TOTAL en el repositorio** | **{total}** |")
    A("")
    A("⚠️ Las filas en *cursiva* **no suman**: están contenidas en la línea "
      "de arriba. La primera versión de esta carta las sumaba —contando "
      "`ADR` y `PCD` dos veces, y dejando fuera las pruebas por el error "
      "opuesto— y publicó un total inflado. Se deja dicho porque es "
      "exactamente el defecto que este refactor viene a corregir, cometido en "
      "el documento que lo planifica.")
    A("")
    A("Más, fuera del repositorio o no contable por archivo:")
    A("")
    A("| | Cuenta |")
    A("|---|---:|")
    A("| hojas del Gold Master | 123 |")
    A("| dominios | 13 |")
    A("| índices | 12 |")
    A("| factores del ICPI | 6 |")
    A("")
    A("> ### Esto no se refactoriza pieza por pieza a mano")
    A(">")
    A("> A un artefacto por sesión, el refactor tarda años. Lo que hace "
      "viable un cambio de esta escala es que **la clasificación sea "
      "derivable**: cada pieza declara su categoría y un gate lo verifica — "
      "el mismo patrón de `deuda.py` y `doctrina.py`.")
    A("")

    # ── Fondo y forma ─────────────────────────────────────────────────────
    A("## ★ 3 · La arquitectura propuesta · FONDO y FORMA")
    A("")
    A("La expresión es de Javo —*«los dominios fondo y forma»*— y el colega la "
      "formalizó. Es el cambio conceptual más grande de la carta:")
    A("")
    A("```")
    A("                        QUIRA")
    A("                          │")
    A("              ┌───────────┴───────────┐")
    A("            FONDO                   FORMA")
    A("     ¿QUÉ gestiona el GAD?    ¿CÓMO lo gestiona?")
    A("              │                       │")
    A("     dominios sectoriales    capacidades transversales")
    A("              │                       │")
    A("   salud · agua · vialidad    planificación · ejecución")
    A("   ambiente · riesgos ·       eficiencia · contratación")
    A("   desarrollo económico       transparencia · trazabilidad")
    A("                              coordinación · responsabilidad")
    A("              └───────────┬───────────┘")
    A("                          │")
    A("                    INTELIGENCIA")
    A("             gráfica → analítica → narrativa")
    A("                          │")
    A("                      EVIDENCIA")
    A("```")
    A("")
    A("> **La misma gestión se observa a la vez desde el fondo y desde la "
      "forma.** Eso es lo que hoy no se puede hacer, y es la razón por la que "
      "indicadores transversales viven dentro de dominios sectoriales.")
    A("")
    A("### El caso que lo ilustra · `IED`")
    A("")
    A("Javo propuso *«establecer eficiencia directiva»*. **Ya existe**: el "
      "`IED` —Índice de Eficiencia por Dirección— desglosa metas del PDOT por "
      "dirección del Estatuto Orgánico (`H17`, `H30_IED_POR_DIRECCIÓN`). Lo "
      "que no tiene es sitio: su dominio, su rol y su pregunta están los tres "
      "`POR_DECLARAR`.")
    A("")
    A("Y en el esquema FONDO/FORMA se ve por qué: **`IED` no pertenece a "
      "ningún dominio sectorial**. La pregunta «¿qué tan eficientemente "
      "funciona la dirección responsable?» aplica a Salud, a Obras Públicas y "
      "a Financiera por igual. Es **forma**, y hoy no hay dónde ponerla.")
    A("")
    A("### Los tres niveles que esto habilita")
    A("")
    A("| Nivel | Unidad | Pregunta |")
    A("|---|---|---|")
    A("| **sectorial** | una competencia | ¿qué resultados está gestionando? |")
    A("| **organizacional** | una dirección | ¿cómo funciona esa unidad? |")
    A("| **transversal** | el gobierno municipal | ¿es coherente, eficiente, "
      "trazable y coordinado el sistema completo? |")
    A("")

    # ── El ICPI ───────────────────────────────────────────────────────────
    A("## ★ 4 · El ICPI · cuatro destinos posibles, ninguno decidido")
    A("")
    A("⚠️ **No se decide aquí.** `011-C4` lo hace. Pero conviene tener los "
      "cuatro sobre la mesa para que el dictamen no se lea como binario:")
    A("")
    A("| | Destino | Qué significaría |")
    A("|---|---|---|")
    A("| **A** | se **conserva** | la construcción supera `C4` y la teoría "
      "justifica sus dimensiones |")
    A("| **B** | se **refactoriza** | mismo fenómeno, otros factores, otra "
      "semántica, otra agregación, otra escala, otra residencia |")
    A("| **C** | se **descompone** | en vez de un número: congruencia "
      "programática · ejecución financiera · trazabilidad · responsabilidad "
      "institucional · eficiencia directiva · desempeño operativo. Y un "
      "**panel multidimensional** en lugar de un índice único |")
    A("| **D** | se **depreca** | `ICPI_v1` queda disponible para "
      "trazabilidad y deja de ser el indicador operativo principal |")
    A("")
    A("**Ninguno de los cuatro es un fracaso.** `D` tampoco: sería evolución "
      "metodológica, y el `ICPI` histórico seguiría explicando de dónde "
      "vino el sistema.")
    A("")
    A("### ⚠️ Y por qué el nombre va al final")
    A("")
    A("Javo planteó renombrar el `ICPI`. La secuencia correcta **no empieza "
      "por el nombre**:")
    A("")
    A("```")
    A("  1. ¿qué fenómeno sobrevive a C4?")
    A("  2. ¿cuál es su unidad?")
    A("  3. ¿cuál es su arquitectura?")
    A("  4. ¿cuál es su residencia?")
    A("  5. …y recién entonces: ¿cómo se llama?")
    A("```")
    A("")
    A("> Empezar por el nombre sería hacer **branding de un concepto que "
      "todavía se está rediseñando**.")
    A("")

    # ── Los diez ejes ─────────────────────────────────────────────────────
    A("## 5 · Los diez ejes · se auditan simultáneamente")
    A("")
    A("Un refactor que arregle la ontología sin tocar el frontend produce un "
      "sistema que **dice una cosa y muestra otra** — el defecto que `GM-Ω` "
      "lleva toda la investigación documentando dentro del propio "
      "instrumento.")
    A("")
    A("| | Eje | Pregunta | Estado hoy |")
    A("|---|---|---|---|")
    for letra, nombre, pregunta, estado in _EJES:
        A(f"| **{letra}** | {nombre} | {pregunta} | {estado} |")
    A("")

    # ── Qué se puede hacer ya ─────────────────────────────────────────────
    A("## ★ 6 · Qué se puede hacer HOY y qué espera al dictamen")
    A("")
    A("La dependencia con `011` es **más chica de lo que parece**. Sólo "
      "espera lo que presupone saber qué sobrevive:")
    A("")
    A("```")
    A("  AHORA · no toca el motor, y alimenta al dictamen")
    A("  ├── 010        transferibilidad LATAM        ← siguiente en la ruta")
    A("  ├── R0         diagnóstico de los 13 dominios")
    A("  ├── R1         modelos A · B · C de arquitectura")
    A("  ├── EJE H/I    dashboards y narrativa por dominio")
    A("  ├── LIMPIEZA   clasificar los 411 documentos de canon")
    A("  └── 011-A2     declarar la unidad `i` en el canon")
    A("")
    A("           ↓")
    A("")
    A("  011-C4   DICTAMEN · ¿qué sobrevive del constructo?")
    A("")
    A("           ↓ y sólo entonces")
    A("")
    A("  ├── T6         renombrar / deprecar / eliminar")
    A("  ├── R2         residencia y ámbito de los índices")
    A("  ├── EJE E      intervenir el Gold Master")
    A("  └── v2         universo completo del PDOT (66)")
    A("```")
    A("")
    A("| Frente | ¿Espera a `C4`? | Por qué |")
    A("|---|---|---|")
    A("| `010` LATAM | 🟢 no | separar lo ecuatoriano de lo generalizable "
      "**alimenta** el dictamen |")
    A("| `R0` · `R1` | 🟢 no | son diagnóstico |")
    A("| Dashboards · narrativa | 🟢 no | dependen de `R0`, no de `C4` |")
    A("| Limpieza documental | 🟢 no | clasificar no es cambiar |")
    A("| Renombrado (`T6`) | 🔴 **sí** | el nombre depende de qué resulte que "
      "mide |")
    A("| Residencia (`R2`) | 🔴 **sí** | mover un índice cuyo constructo está "
      "en dictamen es reorganizar la casa antes de saber qué se guarda |")
    A("| Gold Master | 🔴 **sí** | `Regla de Oro 1` |")
    A("")

    # ── Reglas de migración ───────────────────────────────────────────────
    A("## 7 · Las reglas de la migración")
    A("")
    A("| # | Regla | De dónde sale |")
    A("|---|---|---|")
    A("| 1 | **Clasificar antes de tocar.** Ninguna pieza se modifica sin "
      "declarar en cuál de las cinco categorías cae | esta carta · §1 |")
    A("| 2 | **El basónimo no cambia.** El identificador estable sobrevive al "
      "renombrado, o se rompe la trazabilidad | `DOC-015` |")
    A("| 3 | **Nombre técnico ≠ nombre de presentación.** Tres capas, y la "
      "jerga no cruza al producto | `DOC-014` · `Regla de Oro 2` |")
    A("| 4 | **Anti-inflación.** Si un concepto sólo renombra, no entra: debe "
      "añadir capacidad, eliminar ambigüedad o reducir complejidad | `Regla "
      "de Oro 7` |")
    A("| 5 | **Ningún cambio nace en Python.** Nace en el canon; el código "
      "implementa | `Regla de Oro 9` · `DOC-016` |")
    A("| 6 | **Lo que se retira no se borra:** pasa a `HISTÓRICO` con su "
      "linaje | `DOC-013` |")
    A("| 7 | **Continuidad histórica ≠ continuidad metodológica.** Conservar "
      "`ICPI_v1` no obliga a que `ICPI_v2 = ICPI_v1`; conservar `d06` "
      "histórico no obliga a que `d06` futuro sea igual | el colega, "
      "2026-09-05 |")
    A("| 8 | **Cada dominio cierra con su `PCD`.** El protocolo de curación no "
      "se salta | `Regla de Oro 8` |")
    A("")

    A("## Lo que esta carta NO hace")
    A("")
    A("- **No decide el destino del ICPI.** Cuatro opciones sobre la mesa, "
      "`011-C4` elige.")
    A("- **No renombra nada.** El nombre es el último paso, no el primero.")
    A("- **No toca el Gold Master.** Congelado hasta el dictamen.")
    A("- **No clasifica todavía** los 411 documentos ni las 123 hojas: "
      "establece **cómo** se clasifican. El barrido es trabajo de ejecución.")
    A("")
    A("> ### El propósito, dicho en una línea")
    A(">")
    A("> `GM-Ω` no existe para legitimar el pasado ni para destruirlo, sino "
      "para **ponerlo en su lugar**: el pasado como **linaje**, la norma como "
      "**restricción**, la evidencia como **fundamento**, la teoría como "
      "**justificación** — y el diseño como **decisión presente**.")
    A("")
    A("Lo que eso habilita es lo que hasta ahora no se podía hacer con "
      "seguridad: **diseñar el QUIRA que se necesita, no preservar el QUIRA "
      "que se construyó.**")
    A("")
    A("---")
    A(f"*QUIRA-NEXT · Carta de Rearquitectura · {total} artefactos "
      f"inventariados · el Gold Master no se modificó · baseline 27,4582 % "
      f"congelado · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
