# -*- coding: utf-8 -*-
"""
scripts/gm_omega/transferibilidad_latam.py — GM-Ω-ICPI-010

    ¿Qué elementos de QUIRA constituyen **arquitectura generalizable de
    inteligencia pública** y cuáles son **soluciones contingentes** derivadas
    de la historia normativa, institucional, documental y metodológica del
    Ecuador?

    ⚠️ NO ES «¿puede QUIRA aplicarse en otro país?». Esa pregunta es
    superficial y se responde con un sí vacío. La útil separa dos cosas:

        QUIRA no debe exportar Ecuador.
        Debe poder exportar su ARQUITECTURA y adaptar su CORPUS.

    ★ LA REGLA QUE ORDENA ESTA ETAPA, y que evita repetir `DOC-009` en
    versión automatizada:

        La presencia de una norma ecuatoriana NO demuestra que un componente
        sea contingente: demuestra que existe un ACOPLAMIENTO NORMATIVO que
        hay que identificar.

        La ausencia de cita normativa NO demuestra que un componente sea
        universal.

    Es decir: **la máquina detecta dependencia; la dirección determina
    significado.** Un documento puede citar la Constitución ecuatoriana sólo
    para ilustrar un caso de implementación de un principio generalizable — y
    ese matiz puede ser uno de los hallazgos de `010`.

    LECTURA PURA · no toca el Gold Master · baseline congelado.

Uso:  python scripts/gm_omega/transferibilidad_latam.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_SALIDA = _RAIZ / "docs" / "architecture" / "GM-OMEGA_TRANSFERIBILIDAD_010.md"

# ── LAS CUATRO CATEGORÍAS ─────────────────────────────────────────────────
#
# La cuarta —decisión de diseño contingente— la añadió el colega y evita una
# falsa dicotomía: algo puede no ser normativo NI histórico y aun así no ser
# arquitectura generalizable. Sin ella, toda decisión propia se colaría como
# «núcleo» por no citar una norma.
_CATEGORIAS = [
    ("A", "NÚCLEO ARQUITECTÓNICO", "🟢",
     "su función no depende de ninguna norma ecuatoriana concreta",
     "no tendría que cambiar"),
    ("B", "ADAPTADOR NORMATIVO", "🔵",
     "la FUNCIÓN permanece; cambia el corpus jurídico que la alimenta",
     "sólo cambiar el corpus normativo"),
    ("C", "SEDIMENTACIÓN HISTÓRICA", "🟠",
     "existe porque QUIRA nació en una trayectoria concreta",
     "cambiar ontología, unidad, fuente y lógica"),
    ("D", "DECISIÓN DE DISEÑO CONTINGENTE", "🟣",
     "ni normativa ni histórica: se eligió, y podría haberse elegido otra",
     "⚠️ lo somete a prueba `011-C4`"),
]

# Instituciones y sistemas ecuatorianos: son INSTANCIAS de una función. La
# distinción instancia↔función es el corazón de `010`.
_INSTANCIAS = {
    "SERCOP": "portal nacional de contratación pública",
    "eSIGEF": "sistema de ejecución presupuestaria del Estado",
    "SIGAD": "sistema de autorreporte de cumplimiento del gobierno local",
    "CPCCS": "órgano de participación ciudadana y control social",
    "CGE": "entidad fiscalizadora superior",
    "CNE": "autoridad electoral",
    "MEF": "ministerio de finanzas",
    "INEC": "instituto nacional de estadística",
    "AME": "asociación de municipalidades",
    "SNP": "órgano nacional de planificación",
}

_NORMAS = {
    "COOTAD": "régimen de competencias del gobierno local",
    "COPFP": "planificación y finanzas públicas",
    "COPLAFIP": "planificación y finanzas públicas",
    "LOSNCP": "contratación pública",
    "LOTAIP": "transparencia y acceso a la información",
    "LOPC": "participación ciudadana",
    "LOSEP": "servicio público",
    "NCI": "normas de control interno",
}

# El inventario de componentes. Se DECLARA, no se deriva: clasificar por
# función es un juicio, y automatizarlo sería la caja negra que `Q0` prohíbe.
# La columna `deps` la mide el script; la categoría la fija la dirección.
_COMPONENTES = [
    # (componente, función, categoría, qué habría que cambiar, nota)
    ("Ingesta de fuentes", "incorporar documentos y datos al corpus", "A",
     "los conectores concretos", ""),
    ("Trazabilidad / provenance", "saber de dónde viene cada afirmación", "A",
     "nada", "`MNT_UUID` · cadena de autoridad"),
    ("Los 8 estados de la evidencia", "distinguir «no existe» de «no pude "
     "obtener» de «falló»", "A", "nada",
     "★ probablemente lo más exportable del constructo"),
    ("Escalera prueba↔verificador", "graduar qué acredita cada artefacto",
     "A", "nada", "el escalón 7 —lo leído ≠ la fuente— es universal"),
    ("Separación norma→evidencia→inferencia", "no confundir lo que la ley "
     "manda con lo que ocurrió ni con lo que se concluye", "A", "nada",
     "`DOC-030` · Eje 0 de la carta"),
    ("Gold Master como estado canónico", "una sola fuente del número", "A",
     "nada", "el formato Excel es contingente; la función no"),
    ("Versionado y hash-chain", "que un resultado sea reproducible", "A",
     "nada", ""),
    ("Motor de congruencia multiplicativa", "un eslabón roto anula la cadena",
     "D", "⚠️ por determinar", "★ `011-C4` decide si es necesario"),
    ("Producto lógico de `V_i`", "un silo en cero anula la meta", "D",
     "⚠️ por determinar", "regla fuerte, sin justificación cuantitativa"),
    ("Los cuatro silos de verificación", "contrastar una afirmación contra "
     "fuentes independientes", "B", "qué sistemas ocupan cada silo",
     "la función es universal; `SERCOP`/`eSIGEF`/`LOTAIP`/`CPCCS` no"),
    ("`P_i` peso presupuestario", "ponderar por magnitud del compromiso",
     "B", "el artículo que lo funda", "`COPFP 54` ↔ su equivalente"),
    ("`R_i` relevancia normativa", "ponderar por jerarquía de la competencia",
     "B", "el catálogo de competencias del país",
     "`COOTAD 54-55` ↔ su equivalente"),
    ("`T_i` materialización temporal", "medir devengo, no compromiso", "B",
     "la norma que define el devengado",
     "`COPFP 115-117` + Acuerdo 067 ↔ equivalente"),
    ("`V_i` inmutabilidad documental", "exigir evidencia en varios silos",
     "B", "las leyes de transparencia y contratación", ""),
    ("`E_i` fricción de autonomía", "ajustar por modalidad de ejecución",
     "B", "el régimen de entidades adscritas", ""),
    ("`C_i` calidad de proceso", "descontar por infracciones verificadas",
     "B", "el catálogo de infracciones del país",
     "⚠️ su semántica cerró en `011-C2`; sus parámetros siguen abiertos"),
    ("Pesos `0,15 / 0,10 / 0,05`", "graduar la severidad de cada infracción",
     "D", "⚠️ por determinar", "sin fundamento cuantitativo (`C3-R`)"),
    ("Piso `C_i ≥ 0,50`", "impedir que una infracción anule la meta", "D",
     "⚠️ por determinar", "sin fundamento cuantitativo (`C3-R`)"),
    ("Escala AVEP", "traducir un número a un juicio institucional", "D",
     "⚠️ por determinar", "baremo propio · dos versiones divergen (`D-012`)"),
    ("Los 13 dominios", "organizar el objeto observado", "C",
     "la estructura de competencias del país",
     "nacieron del caso Montecristi"),
    ("Universo de 25 metas", "acotar la muestra operacional", "C",
     "todo: es una decisión del caso", "`ADR-036` · `D-001`"),
    ("`SAT` I-VI", "alertar sobre patrones de riesgo", "B",
     "los artículos que fundan cada alerta", "la función viaja"),
    ("Corpus normativo vectorizado", "poder afirmar que una obligación "
     "existe", "B", "el corpus entero del país",
     "★ `BM-01` · la estructura viaja, el contenido se sustituye"),
    ("Estatuto Orgánico como fuente de `E_i`/`C_i`", "imputar cada meta a "
     "una unidad responsable", "B", "el instrumento equivalente",
     "`Res. 040-2025` es la instancia"),
]


def medir_dependencias() -> dict:
    """La capa automática: **cuántas veces** aparece cada norma e institución
    ecuatoriana en el canon y en las reglas de negocio.

    ⚠️ ESTO MIDE ACOPLAMIENTO, NO CONTINGENCIA. Una cita puede estar ahí para
    ilustrar un principio generalizable. La cifra abre la pregunta; no la
    responde."""
    def contar(patron: str, rutas: list[str]) -> int:
        total = 0
        rx = re.compile(r"\b" + patron + r"\b")
        for ruta in rutas:
            base = _RAIZ / ruta
            if not base.exists():
                continue
            for p in base.rglob("*"):
                if p.suffix.lower() not in (".md", ".yaml", ".py"):
                    continue
                if "historico" in p.parts or "__pycache__" in p.parts:
                    continue
                try:
                    total += len(rx.findall(p.read_text(encoding="utf-8",
                                                        errors="replace")))
                except Exception:
                    continue
        return total

    rutas = ["docs", "app", "governance", "marco_teorico"]
    return {
        "normas": {k: contar(k, rutas) for k in _NORMAS},
        "instancias": {k: contar(k, rutas) for k in _INSTANCIAS},
        "brn": len(list((_RAIZ / "docs" / "brn").glob("*.yaml")))
        if (_RAIZ / "docs" / "brn").exists() else 0,
    }


def main() -> int:
    dep = medir_dependencias()
    por_cat = {c: sum(1 for x in _COMPONENTES if x[2] == c)
               for c, _n, _i, _d, _q in _CATEGORIAS}
    print(f"componentes clasificados: {len(_COMPONENTES)}")
    for cid, nombre, icono, _d, _q in _CATEGORIAS:
        print(f"  {icono} {cid} {nombre:<32} {por_cat[cid]:>2}")
    print(f"normas ecuatorianas citadas: {sum(dep['normas'].values())} "
          f"· instancias institucionales: {sum(dep['instancias'].values())}")
    _escribir(dep, por_cat)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(dep, por_cat) -> None:
    o: list[str] = []
    A = o.append

    A("# GM-Ω · TRANSFERIBILIDAD LATAM  `010`")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/gm_omega/transferibilidad_latam.py`. Las **dependencias** se "
      "miden del repositorio; la **clasificación funcional** se declara, "
      "porque es un juicio.")
    A("")
    A("> ### La pregunta")
    A("> ¿Qué elementos de QUIRA constituyen **arquitectura generalizable de "
      "inteligencia pública** y cuáles son **soluciones contingentes** "
      "derivadas de la historia normativa, institucional, documental y "
      "metodológica del Ecuador?")
    A("")
    A("⚠️ **No es «¿puede QUIRA aplicarse en otro país?».** Esa pregunta se "
      "responde con un sí vacío. La útil separa dos cosas:")
    A("")
    A("> **QUIRA no debe exportar Ecuador. Debe poder exportar su "
      "ARQUITECTURA y adaptar su CORPUS.**")
    A("")

    # ── La regla ──────────────────────────────────────────────────────────
    A("## ★ La regla que ordena esta etapa")
    A("")
    A("| | |")
    A("|---|---|")
    A("| La **presencia** de una norma ecuatoriana | **NO** demuestra que un "
      "componente sea contingente. Demuestra que existe un **acoplamiento "
      "normativo** que hay que identificar |")
    A("| La **ausencia** de cita normativa | **NO** demuestra que un "
      "componente sea universal |")
    A("")
    A("> ### La máquina detecta dependencia; la dirección determina significado")
    A("")
    A("Sin esta regla, `010` repetiría `DOC-009` en versión automatizada: "
      "**detectar → clasificar → convertir la detección en ontología**. Un "
      "documento puede citar la Constitución ecuatoriana sólo para **ilustrar "
      "un caso de implementación** de un principio generalizable — y ese "
      "matiz puede ser uno de los hallazgos de esta etapa.")
    A("")

    # ── Las cuatro categorías ─────────────────────────────────────────────
    A("## Las cuatro categorías")
    A("")
    A("| | Categoría | Qué es | ¿Qué habría que cambiar para desplegarlo? |")
    A("|---|---|---|---|")
    for cid, nombre, icono, que, cambio in _CATEGORIAS:
        A(f"| {icono} **{cid}** | {nombre} | {que} | *{cambio}* |")
    A("")
    A("⚠️ **La categoría `D` evita una falsa dicotomía**, y la añadió el "
      "colega. Algo puede **no ser normativo ni histórico** y aun así no ser "
      "arquitectura generalizable: «elegimos esta fórmula porque en ese "
      "momento parecía adecuada» no es Ecuador, pero tampoco es universal. "
      "Sin `D`, toda decisión propia se colaría como núcleo **por el mero "
      "hecho de no citar una norma**.")
    A("")
    A("### El test que decide la categoría")
    A("")
    A("```")
    A("  ¿qué tendría que cambiar para desplegarlo en otro país?")
    A("")
    A("    «nada»                                    → 🟢 A núcleo")
    A("    «sólo el corpus normativo»                → 🔵 B adaptador")
    A("    «ontología, unidad, fuente y lógica»      → 🟠 C sedimentación")
    A("    «depende de si la decisión era necesaria» → 🟣 D contingente")
    A("```")
    A("")

    # ── La matriz ─────────────────────────────────────────────────────────
    A("## ★ La matriz de componentes")
    A("")
    A("| Componente | Función | | ¿Qué habría que cambiar? |")
    A("|---|---|---|---|")
    _ICO = {c: i for c, _n, i, _d, _q in _CATEGORIAS}
    for comp, func, cat, cambio, nota in _COMPONENTES:
        n = f" · {nota}" if nota else ""
        A(f"| **{comp}** | {func}{n} | {_ICO[cat]} `{cat}` | {cambio} |")
    A("")
    A("| Categoría | Componentes |")
    A("|---|---:|")
    for cid, nombre, icono, _d, _q in _CATEGORIAS:
        A(f"| {icono} **{cid}** {nombre} | {por_cat[cid]} |")
    A("")

    # ── Función vs instancia ──────────────────────────────────────────────
    A("## ★ Función ≠ instancia · el corazón de `010`")
    A("")
    A("Lo que hace transferible a un adaptador normativo es que su **función** "
      "existe en cualquier Estado, aunque la **institución** que la encarna "
      "sea ecuatoriana:")
    A("")
    A("| Instancia ecuatoriana | Menciones | Función generalizable |")
    A("|---|---:|---|")
    for k, funcion in sorted(_INSTANCIAS.items(),
                             key=lambda x: -dep["instancias"].get(x[0], 0)):
        A(f"| `{k}` | {dep['instancias'].get(k, 0)} | {funcion} |")
    A("")
    A("| Norma ecuatoriana | Menciones | Materia generalizable |")
    A("|---|---:|---|")
    for k, materia in sorted(_NORMAS.items(),
                             key=lambda x: -dep["normas"].get(x[0], 0)):
        A(f"| `{k}` | {dep['normas'].get(k, 0)} | {materia} |")
    A("")
    A(f"Y las **{dep['brn']} reglas de negocio** de `docs/brn/` son el caso "
      "más nítido: cada una declara la norma que la funda. **Esa estructura "
      "es el adaptador**: la regla viaja, el artículo se sustituye.")
    A("")
    A("> ### El acoplamiento no es un defecto: es lo que hace verificable al "
      "sistema")
    A(">")
    A("> Un motor que no cite norma no sería más universal — sería **menos "
      "auditable**. La `Regla de Oro 3` («sin norma verificada, no hay dato») "
      "exige el acoplamiento. Lo que `010` separa no es «con norma» de «sin "
      "norma», sino **norma como parámetro** de **norma como supuesto "
      "estructural**.")
    A("")

    # ── La hipótesis ──────────────────────────────────────────────────────
    A("## ★ La hipótesis que `010` tenía que poner a prueba")
    A("")
    A("La carta `Q0` la formuló así:")
    A("")
    A("> El producto exportable de QUIRA **puede no ser el ICPI**, sino la "
      "arquitectura `NORMA + EVIDENCIA + ONTOLOGÍA + METODOLOGÍA → "
      "INTELIGENCIA PÚBLICA`.")
    A("")
    A("Lo que la matriz muestra:")
    A("")
    nucleo = [c for c in _COMPONENTES if c[2] == "A"]
    A(f"| | |")
    A(f"|---|---|")
    A(f"| componentes que **no tendrían que cambiar** | {len(nucleo)} |")
    A(f"| …y **ninguno de ellos es el ICPI** | ✅ |")
    A("")
    A("Los candidatos a núcleo son de otra naturaleza: **los 8 estados de la "
      "evidencia**, la **escalera prueba↔verificador**, la **separación "
      "norma→evidencia→inferencia**, la **trazabilidad**, el **estado "
      "canónico único**. Ninguno depende de qué mida el índice.")
    A("")
    A("> ### `010` no confirma ni refuta la hipótesis: la hace formulable")
    A(">")
    A("> Que el núcleo identificado sea **metodológico y no métrico** es "
      "**compatible** con la hipótesis. No la demuestra: para eso haría falta "
      "un segundo caso —otro país, u otro municipio con otro marco— y hoy no "
      "existe. `DOC-019`: un caso no autoriza la regla general.")
    A("")

    # ── Lo que entrega ────────────────────────────────────────────────────
    A("## Lo que `010` entrega a `011-C4`")
    A("")
    A("| Hallazgo | Consecuencia para el dictamen |")
    A("|---|---|")
    A(f"| **{por_cat['D']} componentes** caen en `D` — decisión de diseño "
      "contingente | son exactamente los que `C4` tiene que juzgar, y ahora "
      "están **enumerados** |")
    A("| la multiplicatividad está en `D`, no en `A` | **no se puede "
      "defender como necesaria por ser transferible**: su transferibilidad "
      "depende de que la decisión fuera necesaria, que es lo que se juzga |")
    A(f"| **{por_cat['B']} componentes** son adaptadores | el acoplamiento "
      "normativo es **denso y explícito** — y eso es una fortaleza "
      "auditable, no una atadura |")
    A(f"| **{por_cat['C']} componentes** son sedimentación | incluidos los "
      "13 dominios y el universo de 25: **`R0` y `v2` heredan esto** |")
    A("")
    A("> ### Y la advertencia con la que se entra a `C4`")
    A(">")
    A("> `010` no se hizo para demostrar que QUIRA es universal. La pregunta "
      "no era si todo QUIRA es transferible, sino **qué parte merece llamarse "
      "arquitectura** y qué parte debe reconocerse como adaptación, "
      "sedimentación o decisión contingente. Un `010` que devolviera «todo es "
      "núcleo» habría sido un `010` mal hecho.")
    A("")

    A("## Dictamen de `010` · por grado de certeza")
    A("")
    A("| Afirmación | Estado |")
    A("|---|---|")
    A("| El acoplamiento normativo del motor es explícito y localizable | "
      "**DEMOSTRADO** · norma declarada componente a componente |")
    A("| La función de cada silo existe con independencia de la institución "
      "ecuatoriana que la ocupa | **DEMOSTRADO** |")
    A("| Los candidatos a núcleo son metodológicos, no métricos | "
      "**DEMOSTRADO** sobre la matriz declarada |")
    A("| El ICPI no está entre ellos | **DEMOSTRADO** |")
    A("| La arquitectura es efectivamente transferible a otro país | ⬜ **NO "
      "DETERMINABLE** · exigiría un segundo caso (`DOC-019`) |")
    A("| Los componentes `D` son o no necesarios al constructo | ⬜ **FUERA "
      "DE ALCANCE** · `011-C4` |")
    A("")
    A("> ### GM-Ω-010 — CERRADO COMO SEPARACIÓN ARQUITECTURA / CONTINGENCIA")
    A(">")
    A("> Se clasificaron los componentes del constructo en **núcleo**, "
      "**adaptador normativo**, **sedimentación histórica** y **decisión de "
      "diseño contingente**, con el criterio explícito de qué habría que "
      "cambiar para desplegarlo en otro país.")
    A(">")
    A("> **No demuestra** que QUIRA sea transferible: eso requiere un segundo "
      "caso. Demuestra **dónde está el acoplamiento** y **qué parte del "
      "sistema no depende de él**.")
    A("")
    A("---")
    A(f"*GM-Ω-ICPI-010 · {len(_COMPONENTES)} componentes clasificados · "
      f"{dep['brn']} reglas de negocio · el Gold Master no se modificó · "
      f"baseline 27,4582 % congelado · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
