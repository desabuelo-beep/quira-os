# -*- coding: utf-8 -*-
"""
scripts/rearq/preguntas_publicas.py — REARQ · Q-M1 · LAS PREGUNTAS

    ¿Qué preguntas sobre la gestión pública necesita poder responder QUIRA?

    ★ LA PRUEBA MENTAL QUE ORDENA ESTA ETAPA:

        Si mañana borráramos mentalmente los doce índices históricos de
        QUIRA, ¿qué preguntas fundamentales seguiríamos necesitando
        responder?

    No significa borrarlos: significa **suspender su autoridad
    epistemológica durante el diseño**. Después se hace el cruce, y ahí los
    índices **se ganan su residencia** en vez de que `Q-M1` tenga que
    justificar por qué siguen existiendo.

    ⚠️ Y LAS PREGUNTAS NO SE INVENTAN. El colega fue explícito: se derivan
    **del corpus, la doctrina, la arquitectura y el propósito declarado de
    QUIRA**, no de la memoria ni de la intuición del momento. Por eso esta
    etapa empieza leyendo la Constitución Ontológica —4 macroejes, 13
    dominios, cada uno con su **capacidad del Estado** declarada— y no una
    lista escrita aquí.

    ⚠️ `FONDO`/`FORMA` sigue siendo **hipótesis arquitectónica** hasta que se
    demuestre que organiza las preguntas mejor que la ontología actual. Se
    contrasta; no se asume.

    LO QUE `Q-M1` NO HACE: no dice «este índice sirve y este no». Recorre la
    cadena y registra correspondencias.

Uso:  python scripts/rearq/preguntas_publicas.py
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

_SALIDA = _RAIZ / "docs" / "architecture" / "REARQ_Q-M1_PREGUNTAS_PUBLICAS.md"
_CONTRATO = _RAIZ / "docs" / "architecture" / "GM-OMEGA_CONTRATO_INDICE_DOMINIO.md"

_PD = "⬜ POR DECLARAR"

# Los cuatro macroejes de la Constitución Ontológica (§CAPA 0). NO son una
# lista escrita aquí: son la agrupación que el canon ya declara para los 13
# dominios, y la columna «capacidad del Estado» de cada uno es lo que hace
# de ellos familias de preguntas y no rótulos.
_MACROEJES = {
    "1": ("DIRECCIÓN", "¿hacia dónde va la administración y con qué mandato?"),
    "2": ("CAPACIDAD", "¿con qué puede la administración sostener lo que se "
                       "propone?"),
    "3": ("DEMOCRACIA", "¿ante quién responde y con qué verificabilidad?"),
    "4": ("TERRITORIO", "¿qué ocurre en el territorio y con quiénes?"),
}

# Las cuatro respuestas posibles del cruce pregunta ↔ indicador existente.
_CRUCE = [
    ("A", "✅", "responde bien"),
    ("B", "🟡", "responde parcialmente"),
    ("C", "🔵", "responde una pregunta DISTINTA de la que su dominio plantea"),
    ("D", "🔴", "no hay indicador para esta pregunta"),
]


def leer_dominios() -> list[dict]:
    """Los 13 dominios con su macroeje, capacidad y pregunta rectora — del
    contrato ya construido.

    ⚠️ Se lee; no se reescribe. Y donde el contrato dice `POR_DECLARAR`, aquí
    también: **inventar la pregunta de un dominio sería escribir el canon
    desde un script**, que es exactamente lo contrario de cómo QUIRA
    construye."""
    if not _CONTRATO.exists():
        return []
    out = []
    for linea in _CONTRATO.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*`(d\d\d)`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|"
                     r"([^|]*)\|([^|]*)\|", linea)
        if not m:
            continue
        cap = m.group(3).strip()
        eje = re.search(r"·\s*(\d)\s", cap)
        out.append({
            "id": m.group(1),
            "nombre": m.group(2).strip(),
            "capacidad": cap.split("·")[0].strip(),
            "macroeje": eje.group(1) if eje else "?",
            "indicador": m.group(4).strip(),
            "construccion": m.group(5).strip(),
            "pregunta": m.group(6).strip(),
        })
    return out


def clasificar(dominios: list[dict]) -> dict:
    """Cuántas preguntas están declaradas, y dónde. El recuento es el primer
    resultado de `Q-M1`: **no se puede diseñar desde preguntas que nadie ha
    escrito**."""
    con = [d for d in dominios if "POR_DECLARAR" not in d["pregunta"]
           and d["pregunta"]]
    sin = [d for d in dominios if d not in con]
    por_eje: dict[str, list] = {}
    for d in dominios:
        por_eje.setdefault(d["macroeje"], []).append(d)
    return {"con": con, "sin": sin, "por_eje": por_eje}


def main() -> int:
    dominios = leer_dominios()
    if not dominios:
        print("[no determinable] no se pudo leer el contrato índice→dominio.")
        return 2
    c = clasificar(dominios)

    print(f"dominios leídos del canon: {len(dominios)}")
    print(f"con pregunta rectora declarada: {len(c['con'])} "
          f"({', '.join(d['id'] for d in c['con'])})")
    print(f"SIN pregunta declarada: {len(c['sin'])}")
    for eje, ds in sorted(c["por_eje"].items()):
        n, _p = _MACROEJES.get(eje, ("?", ""))
        print(f"  macroeje {eje} {n:<12} {len(ds)} dominios")

    _escribir(dominios, c)
    print(f"→ {_SALIDA.relative_to(_RAIZ).as_posix()}")
    return 0


def _escribir(dominios, c) -> None:
    o: list[str] = []
    A = o.append

    A("# REARQ · `Q-M1` — LAS PREGUNTAS PÚBLICAS")
    A("")
    A("**DERIVADO — no editar a mano.** Lo regenera "
      "`scripts/rearq/preguntas_publicas.py` leyendo el contrato "
      "índice→dominio, que a su vez deriva de la Constitución Ontológica.")
    A("")
    A("> ### La prueba mental que ordena esta etapa")
    A("> **Si mañana borráramos mentalmente los doce índices históricos de "
      "QUIRA, ¿qué preguntas fundamentales sobre la gestión pública "
      "seguiríamos necesitando responder?**")
    A("")
    A("No significa borrarlos: significa **suspender su autoridad "
      "epistemológica durante el diseño**. Después se hace el cruce — y ahí "
      "los índices **se ganan su residencia**, en vez de que `Q-M1` tenga que "
      "justificar por qué siguen existiendo.")
    A("")
    A("⚠️ **Las preguntas no se inventan aquí.** Se derivan del corpus, la "
      "doctrina y la arquitectura declarada. Escribir en un script las "
      "preguntas que el canon no tiene sería **escribir el canon desde un "
      "script** — lo contrario de cómo QUIRA construye.")
    A("")

    # ── El primer resultado ───────────────────────────────────────────────
    A("## ★ El primer resultado · no se puede diseñar desde preguntas que "
      "nadie escribió")
    A("")
    A("| | |")
    A("|---|---:|")
    A(f"| dominios en el canon | {len(dominios)} |")
    A(f"| **con pregunta rectora declarada** | **{len(c['con'])}** |")
    A(f"| **sin pregunta declarada** | **{len(c['sin'])}** |")
    A("")
    A("Los dos que la tienen —" +
      " y ".join(f"`{d['id']}`" for d in c["con"]) +
      "— son precisamente **los que tienen `PCD` cerrado**. La pregunta no "
      "aparece por escribirla: aparece al curar el dominio.")
    A("")
    A("> ### Y eso reordena `Q-M1` antes de empezar")
    A(">")
    A("> `Q-M1` no puede **derivar** las once preguntas que faltan: sólo "
      "puede **mostrar el hueco y la forma que tendría llenarlo**. "
      "Derivarlas desde un script sería inventarlas.")
    A("")

    # ── Las familias ──────────────────────────────────────────────────────
    A("## Las cuatro familias de preguntas · macroejes de la Constitución")
    A("")
    A("⚠️ **No son una lista escrita aquí.** Son la agrupación que el canon "
      "ya declara para los 13 dominios, y la columna «capacidad del Estado» "
      "de cada uno es lo que los convierte en **familias de preguntas** y no "
      "en rótulos.")
    A("")
    for eje in sorted(c["por_eje"]):
        nombre, pregunta = _MACROEJES.get(eje, ("?", _PD))
        ds = c["por_eje"][eje]
        A(f"### Macroeje {eje} · **{nombre}**")
        A("")
        A(f"> {pregunta}")
        A("")
        A("| Dominio | Capacidad del Estado | Pregunta rectora | Indicador |")
        A("|---|---|---|---|")
        for d in ds:
            p = (d["pregunta"] if "POR_DECLARAR" not in d["pregunta"]
                 else "⬜ **por declarar**")
            A(f"| `{d['id']}` {d['nombre']} | {d['capacidad']} | {p} | "
              f"{d['indicador']} |")
        A("")

    # ── FONDO / FORMA como hipótesis ──────────────────────────────────────
    A("## ★ `FONDO` / `FORMA` · contrastada contra los macroejes, no asumida")
    A("")
    A("La hipótesis de `010` decía que QUIRA necesita dos ejes: **qué** "
      "gestiona la administración y **cómo** la gestiona. Puesta contra los "
      "macroejes que el canon ya tiene:")
    A("")
    A("| Macroeje | Capacidades que agrupa | ¿FONDO o FORMA? |")
    A("|---|---|---|")
    for eje in sorted(c["por_eje"]):
        nombre, _p = _MACROEJES.get(eje, ("?", ""))
        caps = " · ".join(d["capacidad"] for d in c["por_eje"][eje])
        lectura = ("**FONDO** — son sectores y poblaciones" if eje == "4"
                   else "**FORMA** — son modos de administrar")
        A(f"| {eje} {nombre} | {caps} | {lectura} |")
    A("")
    A("> ### El hallazgo: la Constitución **ya contiene** el eje FONDO/FORMA, "
      "sin nombrarlo")
    A(">")
    A("> Los macroejes `1`, `2` y `3` agrupan **modos de administrar** "
      "—dirigir, sostener, responder—; el `4` agrupa **materias y "
      "poblaciones**. La distinción que `010` propuso como novedad estaba "
      "**implícita en la ontología desde el principio**.")
    A("")
    A("⚠️ **Y eso no la valida todavía.** Que los macroejes se dejen leer así "
      "es **compatible** con la hipótesis; no demuestra que `FONDO`/`FORMA` "
      "organice las preguntas **mejor** que la agrupación actual. Para eso "
      "haría falta comparar ambas contra un conjunto de preguntas "
      "declaradas — y **once de trece no existen**.")
    A("")
    A("Es la misma disciplina que se aplicó a `IED`: evidencia que respalda "
      "una hipótesis no es la hipótesis demostrada.")
    A("")

    # ── El cruce ──────────────────────────────────────────────────────────
    A("## El cruce · las cuatro respuestas posibles")
    A("")
    A("Cuando exista la pregunta, el cruce con el indicador histórico da una "
      "de cuatro:")
    A("")
    A("| | | Significa |")
    A("|---|---|---|")
    for cid, ico, txt in _CRUCE:
        A(f"| **{cid}** | {ico} | el indicador existente {txt} |")
    A("")
    A("Y **sólo `D` obliga a crear algo nuevo**. `A` conserva, `B` amplía, "
      "`C` **traslada** — que es el caso más interesante y el que ya "
      "sospechamos en el ICPI: reside en `d06` pero puede estar respondiendo "
      "una pregunta de otro eje.")
    A("")
    A("### Lo que hoy puede cruzarse")
    A("")
    A("| Dominio | Pregunta | Indicador | Cruce |")
    A("|---|---|---|---|")
    for d in c["con"]:
        A(f"| `{d['id']}` | {d['pregunta'][:74]}… | {d['indicador'][:38]} | "
          f"⬜ **por evaluar en `Q-M2`** |")
    for d in c["sin"][:4]:
        A(f"| `{d['id']}` | ⬜ sin pregunta | {d['indicador'][:38]} | 🔴 **no "
          f"cruzable**: no hay pregunta contra la cual evaluar |")
    A("")
    A(f"⚠️ **{len(c['sin'])} de {len(dominios)} dominios no son cruzables "
      f"hoy.** No porque su indicador sea malo, sino porque **falta el otro "
      f"lado del cruce**. Un indicador sin pregunta declarada no puede "
      f"responder bien ni mal: no se puede evaluar.")
    A("")

    # ── Lo que Q-M1 entrega ───────────────────────────────────────────────
    A("## Lo que `Q-M1` entrega, y lo que no")
    A("")
    A("| ✅ Establecido | ⬜ Abierto |")
    A("|---|---|")
    A("| las cuatro familias existen en el canon y agrupan los 13 dominios | "
      "las once preguntas rectoras que faltan |")
    A("| los macroejes se dejan leer como `FONDO`/`FORMA` | si esa lectura "
      "organiza **mejor** que la actual |")
    A("| la pregunta aparece al **curar** el dominio, no al escribirla | qué "
      "indicador responde a qué pregunta (`Q-M2`) |")
    A("")
    A("> ### La consecuencia operativa, y no es la que se esperaba")
    A(">")
    A("> `Q-M1` iba a reconstruir las preguntas necesarias. Lo que encuentra "
      "es que **el canon ya declaró las familias** y que **once de trece "
      "preguntas no existen todavía** — y que el camino para que existan **ya "
      "está definido**: es el `PCD`, la curación de dominio (`Regla de Oro "
      "8`).")
    A(">")
    A("> No hace falta un método nuevo. Hace falta **aplicar el que hay a "
      "once dominios**.")
    A("")
    A("⚠️ Y eso **no** significa «curar los once antes de seguir». Significa "
      "que la Rearquitectura tiene ahora una **dependencia declarada**: "
      "cualquier decisión sobre residencia de indicadores se apoya en "
      "preguntas que, en once casos, todavía no están escritas.")
    A("")
    A("## Lo que `Q-M1` NO hace")
    A("")
    A("- **No inventa las once preguntas que faltan.**")
    A("- **No dice «este índice sirve y este no».**")
    A("- **No valida `FONDO`/`FORMA`**: la contrasta y declara qué falta para "
      "poder decidirlo.")
    A("- **No toca el motor.** Gold Master intacto · baseline **27,4582 %** "
      "congelado.")
    A("")
    A("---")
    A(f"*REARQ · `Q-M1` · {len(dominios)} dominios · {len(c['con'])} con "
      f"pregunta declarada · 4 familias derivadas del canon · el Gold Master "
      f"no se modificó · Dylus Lab © 2026*")

    _SALIDA.write_text("\n".join(o) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
