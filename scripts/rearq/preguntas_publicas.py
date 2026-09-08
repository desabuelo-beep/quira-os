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


# ── ESTADO DE CURACIÓN ────────────────────────────────────────────────────
#
# ⚠️ LA CORRECCIÓN QUE JAVO IMPUSO. La v1 de `Q-M1` publicó «11 de 13 dominios
# no tienen pregunta rectora» como si fuera una carencia de la ontología. No lo
# es: **esos dominios todavía no se han curado**. Es una fotografía del estado
# de MADURACIÓN del trabajo, no del canon.
#
# Y es el mismo error del 71 %→62 %, ahora a nivel de dominio: confundir
# «todavía no trabajado» con «no existe». Por eso hacen falta cinco estados y
# no dos.
_ESTADOS = [
    ("DECLARADO", "✅", "curado, y la pregunta rectora tiene respaldo "
                        "documental en su `PCD`"),
    ("INCOMPLETO", "🟡", "la curación empezó y no terminó"),
    ("NO INICIADO", "⬜", "el dominio **todavía no ha pasado** por curación — "
                         "⚠️ no es lo mismo que carecer de pregunta"),
    ("NO DECLARADO", "🔴", "se curó y **aun así** no hay pregunta explícita"),
    ("NO DETERMINABLE", "❓", "evidencia parcial o conflictiva que impide "
                             "establecer el estado"),
]


def estado_curacion() -> dict[str, tuple[str, str]]:
    """El estado real de cada dominio, derivado de los `PCD` que existen en
    disco y de lo que `BOOT` declara — no de lo que se recuerde.

    ⚠️ Y donde la evidencia discrepa se dice `NO DETERMINABLE`, no se elige la
    versión más cómoda."""
    pcd = {p.stem.split("_")[0].replace("PCD-D", "d").lower()
           for p in (_RAIZ / "docs" / "pcd").glob("PCD-D*.md")}
    pcd = {f"d{int(x[1:]):02d}" for x in pcd if x[1:].isdigit()}

    boot = ""
    b = _RAIZ / "governance" / "BOOT.md"
    if b.exists():
        boot = b.read_text(encoding="utf-8")

    out: dict[str, tuple[str, str]] = {}
    for i in range(1, 14):
        d = f"d{i:02d}"
        if re.search(rf"{d} en curaci[óo]n", boot, re.I):
            out[d] = ("INCOMPLETO", "`BOOT` lo declara en curación")
        elif d in pcd:
            out[d] = ("DECLARADO", f"`PCD-D{i:02d}` existe en `docs/pcd/`")
        elif re.search(rf"{d} ENTRABLE", boot):
            out[d] = ("NO DETERMINABLE",
                      "`BOOT` lo declara ENTRABLE y **no hay `PCD`**, pero "
                      "Javo lo señala como trabajado — evidencia conflictiva")
        else:
            out[d] = ("NO INICIADO", "sin `PCD` y sin mención de curación")
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
    cur = estado_curacion()
    for d in dominios:
        d["estado"], d["prueba"] = cur.get(d["id"], ("NO DETERMINABLE", "—"))
    c = clasificar(dominios)
    c["por_estado"] = {}
    for d in dominios:
        c["por_estado"].setdefault(d["estado"], []).append(d)

    print(f"dominios leídos del canon: {len(dominios)}")
    for e, ds in c["por_estado"].items():
        print(f"  {e:<17} {len(ds):>2} · {', '.join(x['id'] for x in ds)}")
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
    A("## ★ El primer resultado · un MAPA DE MADUREZ, no un inventario de "
      "carencias")
    A("")
    A("### 📜 CORRECCIÓN · la `v1` confundió «no trabajado» con «no existe»")
    A("")
    A("La primera versión publicó **«11 de 13 dominios no tienen pregunta "
      "rectora»** como si fuera una carencia de la ontología. Javo lo "
      "corrigió:")
    A("")
    A("> *«Los dominios no están completos todos, hemos estado trabajando uno "
      "por uno […] Los demás no se ha empezado su trabajo.»*")
    A("")
    A("⚠️ **Es el mismo error del `71 %` → `62 %`, ahora a nivel de dominio.** "
      "La formulación correcta:")
    A("")
    A("> En el estado actual de curación del corpus, sólo se dispone de "
      "preguntas rectoras formalmente declaradas para los dominios que han "
      "alcanzado el nivel de curación correspondiente. **Los dominios aún no "
      "trabajados no pueden clasificarse como carentes de pregunta.**")
    A("")
    A("### Los cinco estados, y por qué no bastan dos")
    A("")
    A("| | Estado | Significa |")
    A("|---|---|---|")
    for nombre, icono, desc in _ESTADOS:
        A(f"| {icono} | **{nombre}** | {desc} |")
    A("")
    A("### El mapa, derivado de los `PCD` en disco y de `BOOT`")
    A("")
    A("| Estado | Dominios | Prueba |")
    A("|---|---|---|")
    _ICO = {n: i for n, i, _d in _ESTADOS}
    for estado in ("DECLARADO", "INCOMPLETO", "NO DETERMINABLE",
                   "NO INICIADO"):
        ds = c["por_estado"].get(estado, [])
        if not ds:
            continue
        ids = " · ".join(f"`{d['id']}`" for d in ds)
        A(f"| {_ICO.get(estado, '')} **{estado}** ({len(ds)}) | {ids} | "
          f"{ds[0]['prueba']} |")
    A("")
    A("> ### Lo que esto cambia")
    A(">")
    A("> No es «`2/13` con pregunta y `11/13` sin ella». Es **un estado de "
      "curación heterogéneo sobre un universo ontológico todavía "
      "parcialmente observado** — y eso es esperable: la Rearquitectura se "
      "hace **mientras se termina de construir el conocimiento del "
      "sistema**.")
    A("")
    A("⚠️ **No es una debilidad: es lo que permite hacer `REARQ` bien.** La "
      "cadena correcta es `lo trabajado → evidencia disponible → lo no "
      "trabajado → incertidumbre explícita → siguiente dominio`. Nunca `lo "
      "que todavía no vimos → vacío → defecto`.")
    A("")

    # ── Las discrepancias ─────────────────────────────────────────────────
    A("## ★ Tres discrepancias entre el canon y lo que la dirección declara")
    A("")
    A("⚠️ **Se registran; no se resuelven aquí.** Resolver una discrepancia "
      "entre el canon y la memoria del autor exige la fuente, no el criterio "
      "de un script.")
    A("")
    A("### ★ Un solo estado no alcanza · hacen falta CINCO dimensiones")
    A("")
    A("Las discrepancias no eran contradicciones: eran **dimensiones "
      "distintas colapsadas en una sola columna**.")
    A("")
    A("| Dimensión | Qué mide |")
    A("|---|---|")
    A("| **trabajo** | qué se ha hecho realmente |")
    A("| **curación** | qué nivel formal alcanzó (`PCD`) |")
    A("| **documental** | qué está formalmente registrado en el canon |")
    A("| **decisión** | qué ha sido aprobado |")
    A("| **implementación** | qué está efectivizado en el producto |")
    A("")
    A("> **Usar la existencia de un `PCD` como sustituto de la realidad del "
      "proceso** fue el error de la versión anterior. Trabajo realizado ≠ "
      "`PCD` cerrado ≠ implementado.")
    A("")
    A("### Los tres casos, resueltos por dimensión")
    A("")
    A("| | `d04` Alertas | `d06` Salud Inst. | `d08` Participación |")
    A("|---|---|---|---|")
    A("| **trabajo** | — | 🔴 **no iniciado** (Javo) | ✅ **trabajado** (Javo) |")
    A("| **curación** | — | ⚠️ existe `PCD-D06` en disco | ❌ sin `PCD-D08` |")
    A("| **documental** | 🔴 **sigue en la Constitución** (4 lugares) | "
      "`PCD` presente | `BOOT`: `ENTRABLE` |")
    A("| **decisión** | ✅ **aprobada** — eliminarlo | — | — |")
    A("| **implementación** | ✅ **efectivizada** — fuera del frontend | — | "
      "— |")
    A("")
    A("Y así los tres dejan de ser «discrepancias» y pasan a ser **estados "
      "precisos**:")
    A("")
    A("| # | Caso | Lectura correcta |")
    A("|---|---|---|")
    A("| 1 | **¿12 o 13 dominios?** | **No es binario.** El **producto** "
      "tiene hoy **12 dominios visibles**; el **canon** conserva **13**. "
      "`d04` fue eliminado por decisión aprobada y efectivizada — lo "
      "pendiente **no es decidirlo, es propagarlo al canon** |")
    A("| 2 | **`d08` Participación** | ✅ **trabajado**. La ausencia de `PCD` "
      "cerrado **no autoriza** a clasificarlo como no trabajado: mide la "
      "**formalización**, no el trabajo |")
    A("| 3 | **`d06` Salud Institucional** | 🔴 **no iniciado**, según Javo — "
      "⚠️ y existe un `PCD-D06` en disco. **Discrepancia real que queda "
      "abierta**: habrá que determinar qué documenta ese `PCD` |")
    A("")
    A("⚠️ Y una cuarta que `DOC-033` obliga a no dar por hecha: que "
      "*«Rendición de Cuentas y Transparencia»* —mencionado como un trabajo— "
      "corresponda **uno a uno** con `d09` y `d07` tal como están definidos "
      "hoy. **El nombre no lo demuestra**; lo demostraría la correspondencia "
      "documental.")
    A("")
    A("### Lo que `d04` enseña como patrón")
    A("")
    A("> **decisión aprobada ✅ + implementación efectivizada ✅ + canon no "
      "propagado 🔴**")
    A(">")
    A("> No es un dominio en disputa: es una **deuda de propagación "
      "documental**. Y conviene verificar además que la decisión tenga su "
      "anclaje canónico —si existe, la deuda es sólo de propagación; si no, "
      "hay que reconstruir esa autoridad.")
    A("")
    A("Su motivo, además, es arquitectónicamente interesante: los `SAT` "
      "dejaron de ser un dominio propio **para volverse alertas dentro de "
      "cada dominio**. Eso es exactamente una decisión de `FORMA` con "
      "consecuencias en `FONDO`.")
    A("")

    # ── d06 y el ICPI ─────────────────────────────────────────────────────
    A("### `d06` y el ICPI · la hipótesis que NO se decide aquí")
    A("")
    A("Javo:")
    A("")
    A("> *«Ahí estaba pensado meter el ICPI; pero éste posiblemente sea "
      "transversal y debe estar fuera, y el dominio de Salud Institucional "
      "iría con el índice de eficiencia directiva — o todo lo que implique, "
      "visualizo yo, pero no sé si sea lo más adecuado.»*")
    A("")
    A("⚠️ **Decidir ahora `d06 → IED` sería exactamente lo que `Q-M1` acaba "
      "de prohibir**: meter un indicador existente en un dominio porque "
      "encaja de tamaño. El orden obligado es:")
    A("")
    A("```")
    A("  1. ¿qué fenómeno es «Salud Institucional»?")
    A("  2. ¿qué pregunta pública necesita responder?")
    A("  3. ¿qué evidencia lo observa?")
    A("  4. ¿qué indicador —si alguno— responde esa pregunta?")
    A("  5. …y sólo entonces: ¿debe existir un dominio visible con ese nombre?")
    A("```")
    A("")
    A("Seis salidas siguen abiertas, y ninguna está descartada:")
    A("")
    A("| | Salida |")
    A("|---|---|")
    A("| A | `d06` es realmente necesario |")
    A("| B | `d06` queda absorbido por otro dominio |")
    A("| C | «salud institucional» es un **fenómeno transversal**, no un "
      "dominio |")
    A("| D | `IED` es un **componente** de ese fenómeno, no su indicador |")
    A("| E | `ICPI` e `IED` son dos medidas de **una misma dimensión "
      "transversal** |")
    A("| F | ninguno de los indicadores históricos lo representa y hay que "
      "**reconstruir** |")
    A("")
    A("La intuición de Javo —el ICPI fuera de `d06` por transversal— **es "
      "coherente con lo que `010` y `Q-M0` ya midieron**. Eso la hace "
      "plausible; no la convierte en decisión.")
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
    A("## ★★ DOS EJES, no dos versiones del mismo · y ambos valen")
    A("")
    A("### 📜 CORRECCIÓN · `FONDO`/`FORMA` significaba dos cosas distintas")
    A("")
    A("`Q-M1` leyó los macroejes como `FONDO`/`FORMA` en sentido **ontológico** "
      "—qué gestiona la administración frente a cómo la gestiona—. Javo usa "
      "los mismos términos en sentido **arquitectónico**:")
    A("")
    A("> *«Cuando me refiero a FONDO es lo estructural —código, "
      "documentación, metodología—; FORMA, a lo que vemos en el frontend de "
      "los dominios.»*")
    A("")
    A("⚠️ **Dos cosas distintas con el mismo nombre es exactamente lo que "
      "`DOC-033` prohíbe**, y esta vez el nombre lo compartían dos ideas "
      "**ambas correctas**. Javo pidió conservar las dos. Así que no se "
      "descarta ninguna: **se separan**.")
    A("")
    A("| | Eje | Pregunta | Vocabulario |")
    A("|---|---|---|---|")
    A("| **1** | **ARQUITECTÓNICO** — de producto | ¿dónde y cómo existe el "
      "conocimiento **dentro de QUIRA**? | **`FONDO`** / **`FORMA`** |")
    A("| **2** | **ONTOLÓGICO** — de la gestión pública | ¿qué realidad "
      "estamos intentando conocer? | **`SECTORIAL`** / **`TRANSVERSAL`** |")
    A("")
    A("Renombrar el segundo eje **no le quita valor**: le quita la colisión. "
      "«Transversal» ya se usa en el proyecto, así que no inflama el canon "
      "(`Regla de Oro 7`).")
    A("")
    A("### Eje 1 · `FONDO` / `FORMA` — arquitectura de QUIRA")
    A("")
    A("| | Qué contiene |")
    A("|---|---|")
    A("| **`FONDO`** | código · Gold Master · datos · conectores · "
      "metodología · fórmulas · reglas · evidencia · documentación · "
      "ontología · trazabilidad · pruebas · gobernanza |")
    A("| **`FORMA`** | frontend · dominios visibles · navegación · "
      "indicadores presentados · mapas · narrativa · semáforos · "
      "comparaciones · experiencia |")
    A("")
    A("> ### Y de aquí sale una regla de precisión")
    A(">")
    A("> **No se dice «el ICPI es FONDO».** Se dice: el constructo pertenece "
      "al conocimiento metodológico de QUIRA; **su cálculo reside en `FONDO` "
      "y su representación en `FORMA`**. Decir lo primero mezcla niveles.")
    A("")
    A("### Eje 2 · `SECTORIAL` / `TRANSVERSAL` — la realidad observada")
    A("")
    A("| Macroeje | Capacidades que agrupa | Lectura |")
    A("|---|---|---|")
    for eje in sorted(c["por_eje"]):
        nombre, _p = _MACROEJES.get(eje, ("?", ""))
        caps = " · ".join(d["capacidad"] for d in c["por_eje"][eje])
        lectura = ("**SECTORIAL** — materias y poblaciones" if eje == "4"
                   else "**TRANSVERSAL** — modos de administrar")
        A(f"| {eje} {nombre} | {caps} | {lectura} |")
    A("")
    A("> La distinción **ya estaba implícita en la Constitución**: los "
      "macroejes `1`, `2` y `3` agrupan modos de administrar; el `4`, "
      "materias y poblaciones.")
    A("")
    A("⚠️ **Y eso sigue sin validarla.** Que los macroejes admitan esa "
      "lectura es **compatible** con la hipótesis; no demuestra que organice "
      "las preguntas **mejor** que la agrupación actual. Compararlo exigiría "
      "las preguntas, y **la mayoría de los dominios aún no está curada**. Es "
      "la misma disciplina que se aplicó a `IED`.")
    A("")
    A("> ### Los dos ejes son ORTOGONALES, y por eso ambos sirven")
    A(">")
    A("> Un indicador **transversal** puede residir en `FONDO` y mostrarse en "
      "`FORMA`. Un dominio **sectorial** también. Cruzar los dos ejes es lo "
      "que permite preguntar, por ejemplo, si un fenómeno transversal tiene "
      "hoy una `FORMA` que lo represente — y el caso `IED` sugiere que **no "
      "la tiene**.")
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
    A("### ⚠️ `Q-M2` NO está bloqueada · está ACOTADA")
    A("")
    A("La `v1` decía que `Q-M2` quedaba bloqueada porque faltaban once "
      "preguntas. Es demasiado fuerte. La formulación correcta:")
    A("")
    A("> **`Q-M2` puede comenzar únicamente sobre los dominios cuya curación "
      "ya permite establecer una pregunta rectora.** Para los dominios no "
      "iniciados o incompletos, cualquier evaluación indicador↔pregunta debe "
      "permanecer pendiente hasta completar su curación.")
    A("")
    n_maduros = len(c["por_estado"].get("DECLARADO", []))
    A(f"Y eso significa que **`Q-M2` puede trabajar hoy sobre el subconjunto "
      f"maduro de {n_maduros} dominios** — no sobre ninguno, como decía la "
      f"versión anterior.")
    A("")
    A("Un indicador sin pregunta declarada **no puede responder bien ni mal: "
      "no se puede evaluar**. Eso no lo convierte en malo — es la categoría "
      "`B` de `Q-M0`, problema de arquitectura y no del instrumento.")
    A("")

    # ── La unificación ────────────────────────────────────────────────────
    A("## ★ Lo que el refactor debe hacer con los dominios ya curados")
    A("")
    A("Javo:")
    A("")
    A("> *«Los curados deben entrar en el refactor. Por ejemplo unificar "
      "planificación y presupuesto —`d01` y `d02`— para trabajar toda esa "
      "sección en un solo dominio, no dos. Y así todos los cambios en cada "
      "dominio que mejoren sustancialmente a QUIRA.»*")
    A("")
    A("> ### Estar curado no significa quedar congelado")
    A(">")
    A("> Un dominio curado entra al refactor **con más autoridad, no con "
      "menos**: es el único que tiene evidencia suficiente para decidir si "
      "debe unificarse, dividirse o trasladarse. Los no curados no pueden "
      "ni siquiera plantearse esa pregunta.")
    A("")
    A("### ★ La misión, dicha por Javo")
    A("")
    A("> *«Los dominios deben subsanarse, mejorarse, elevarse a lo que "
      "realmente necesitamos para QUIRA — ésa es la misiva de este refactor, "
      "no dejarlos como están. Todos deben revisarse íntegramente para "
      "potenciar y elevar cada dominio, con base en el Excel y la normativa. "
      "Todo debe crecer.»*")
    A("")
    A("Eso cambia la naturaleza de `REARQ`. **No es una auditoría de "
      "conservación.** No pregunta «¿está bien el dominio actual?», sino:")
    A("")
    A("> **¿Qué debería ser este dominio para que QUIRA cumpla adecuadamente "
      "su propósito?**")
    A("")
    A("Con una regla que no cambia: **primero entendemos qué existe; después "
      "decidimos qué debe existir.** El método es `CLASIFICAR → COMPRENDER → "
      "EVALUAR → REDISEÑAR → IMPLEMENTAR`, nunca `CLASIFICAR → CONSERVAR`.")
    A("")
    A("### Nueve destinos posibles, no seis")
    A("")
    A("«Refactorizar» se quedaba corto: sugería arreglar defectos, y la "
      "misión es **elevar**.")
    A("")
    A("| | Destino | Cuándo |")
    A("|---|---|---|")
    A("| **CONSERVAR** | funciona y satisface la necesidad |")
    A("| **MEJORAR** | necesita elevarse |")
    A("| **REESTRUCTURAR** | requiere cambio interno importante |")
    A("| **UNIFICAR** | combinar con otro dominio |")
    A("| **DESCOMPONER** | separar fenómenos mezclados |")
    A("| **TRASLADAR** | cambiar residencia |")
    A("| **RECONSTRUIR** | lo existente no representa lo que QUIRA necesita "
      "conocer |")
    A("| **DEPRECAR** | dejarlo fuera |")
    A("| **PENDIENTE** | evidencia insuficiente para decidir |")
    A("")
    A("> ### Y la regla central de `Q-M1`, reformulada")
    A(">")
    A("> **Los dominios históricos no conservan automáticamente su "
      "residencia, nombre, estructura ni indicador.** Cada uno será evaluado "
      "frente a las preguntas que QUIRA necesita responder, y podrá "
      "conservarse, mejorarse, reestructurarse, unificarse, descomponerse, "
      "trasladarse, reconstruirse o deprecarse.")
    A("")
    A("Es una vuelta más que «los indicadores se ganan su residencia»: **los "
      "dominios también**.")
    A("")
    A("### El caso `d01` + `d02` — lo que habría que verificar antes")
    A("")
    A("| Criterio | Por qué importa |")
    A("|---|---|")
    A("| ¿responden **la misma pregunta rectora** o dos distintas? | `d01` la "
      "tiene declarada; `d02` **no** — y sin ella no se puede comparar |")
    A("| ¿comparten **unidad de análisis**? | unificar dominios con unidades "
      "distintas produce un dominio que mide dos cosas |")
    A("| ¿comparten **evidencia primaria**? | `IPE` cruza gasto ejecutado con "
      "metas del PDOT: **ya opera sobre ambos** |")
    A("| ¿qué pasa con sus indicadores y sus `PCD` cerrados? | `DOC-028`: "
      "continuidad histórica ≠ continuidad metodológica |")
    A("")
    A("⚠️ **La unificación es plausible y no está demostrada.** `IPE` —el "
      "indicador más maduro— vive en `d01` y mide precisamente la "
      "articulación plan↔presupuesto: eso es **evidencia a favor**. Pero "
      "`d02` no tiene pregunta declarada, así que **hoy falta un lado de la "
      "comparación**. Es `Q-M2` sobre el subconjunto maduro.")
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
