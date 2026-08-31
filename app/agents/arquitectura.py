"""
app/agents/arquitectura.py — CAPA 2 · qué arquitectura puede QUIRA demostrar
================================================================================
POR QUÉ EXISTE (2026-08-31). La Capa 0 fijó que ningún inventario afirma sin
declarar su universo. La Capa 1 mostró que el canon está bien y que lo roto son
los **vínculos**. La Capa 2 pregunta lo mismo un nivel arriba:

> *«¿Qué arquitectura existe realmente en el código y la documentación, y cuánto
> coincide con la que hemos decidido que QUIRA debe tener?»*

LO QUE ESTE MÓDULO NO HACE, y es su regla más importante: **no dice
`vigente = true`.** El colega lo prohibió expresamente cuando el director
propuso mapear `RATIFICADO → vigente`:

> *«Una equivalencia no es una propiedad porque históricamente la conozcamos; es
> una propiedad cuando QUIRA puede señalar el artefacto que la establece.»*

Los ADR usan cuatro nombres de estado de tres épocas —`ACEPTADO`, `ACTIVO`,
`RATIFICADO`, `APROBADO — sellado`— y **ningún artefacto declara que sean
equivalentes**. Puede que lo sean; no está demostrado. Así que este módulo separa
lo que el artefacto dice de lo que QUIRA puede derivar:

    estado_declarado      lo que el ADR escribe, literal y sin normalizar
    validacion_humana     lo ÚNICO derivable: ¿consta que un humano validó?
    ...............       y `no_determinable` cuando no consta

LA PROPIEDAD DERIVABLE ES OTRA, y la da la propia autoridad. `ADR-035 §5` no
define nombres de estado: define la **transición**.

    Ley → Extracción → PROPUESTA → VALIDACIÓN HUMANA → BRN → Gold Master → SAT
    JAMÁS: Ley → IA → SAT.  La IA propone; el humano valida.

Por eso la pregunta computable no es *«¿qué significa RATIFICADO?»* sino
**«¿consta validación humana?»**. Esa sí se responde con evidencia.

⚠️ Y `no_determinable` NO es una acusación. Once ADR son anteriores a ADR-035
—la norma que introdujo el registro del validador— y su silencio documental se
produjo **antes de que existiera la obligación de registrar**. Convertir eso en
un defecto sería una imputación retroactiva, que es exactamente lo que este
observatorio le prohíbe hacerle al sujeto observado.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# ⚠️ DOS DIRECTORIOS, Y DESCUBRIRLO COSTÓ UN FALSO POSITIVO. La primera versión
# miraba sólo `docs/adr/` y reportó cinco «citas rotas»; al verificarlas antes de
# reportarlas, cuatro apuntaban a ADR que **sí existen** en `docs/corpus_externo/`
# —entre ellos `ADR-007_Gold_Master_unica_fuente_calculo`, que es fundacional— y
# la quinta era una mención hipotética. Cero citas rotas, universo incompleto en
# un 23%: 41 ADR de 53.
#
# Por qué doce decisiones viven en un directorio llamado «corpus externo» es una
# pregunta abierta —¿archivo histórico deliberado, o quedaron fuera al migrar?—
# y este módulo NO la responde: los cuenta a todos y declara la partición.
ADR_DIRS = (RAIZ / "docs" / "adr", RAIZ / "docs" / "corpus_externo")

# ── DESCUBRIMIENTO POR ROL, NO POR TERRITORIO ────────────────────────────────
# El colega, tras el hallazgo de los doce: *«¿cómo descubre QUIRA un ADR,
# independientemente de dónde esté almacenado? […] `docs/adr/` no puede volver a
# ser tratado como sinónimo de universo ADR»*.
#
# Por eso el universo NO es una lista de carpetas: es el repositorio entero,
# menos exclusiones **declaradas una por una**. Así, un ADR guardado mañana en un
# tercer territorio aparece solo; y si algo se excluye, se sabe por qué.
_EXCLUIDOS = (
    (".claude/worktrees", "copias de trabajo de otras ramas: duplican el original"),
    ("skills/", "plantillas de herramientas de terceros — `ADR-FORMAT.md` explica "
                "cómo escribir un ADR; no es una decisión de QUIRA"),
    ("node_modules", "dependencias externas"),
)


def territorios() -> dict:
    """Dónde vive de hecho cada ADR, y qué se excluyó a propósito.

    Que la arquitectura documental tenga **más de un territorio físico** es en
    sí una propiedad arquitectónica, y hasta hoy no estaba registrada en ningún
    sitio: se descubrió porque un inventario acusó en falso."""
    encontrados: dict[str, list[str]] = {}
    excluidos: list[dict] = []
    for f in sorted(RAIZ.rglob("ADR-*.md")):
        rel = f.relative_to(RAIZ).as_posix()
        motivo = next((m for pat, m in _EXCLUIDOS if pat in rel), "")
        if motivo:
            excluidos.append({"archivo": rel, "motivo": motivo})
            continue
        encontrados.setdefault(str(f.parent.relative_to(RAIZ).as_posix()), []).append(rel)
    return {"territorios": {k: len(v) for k, v in sorted(encontrados.items())},
            "excluidos": excluidos,
            "declarados_en_el_modulo": [d.relative_to(RAIZ).as_posix() for d in ADR_DIRS]}


# ── TIPOS DE RELACIÓN ────────────────────────────────────────────────────────
# *«mención ≠ referencia ≠ dependencia ≠ consumo ≠ autoridad»*. Un simple
# `referenciado=True` es lo que produjo cuatro falsos positivos hoy: la mención
# hipotética de `ADR-054`, la RO citada en un docstring, el puente compilado que
# existe sin que nadie lo cruce.
MENCION = "mencion"                    # el id aparece, sin más
AUTORIDAD = "autoridad_invocada"       # se cita como fundamento de algo
EN_CODIGO = "referenciado_en_codigo"   # vive en un .py
EN_CANON = "referenciado_en_canon"     # vive en un CNO/RO
EN_COMPILADO = "referenciado_en_artefacto_compilado"

_PATRON_AUTORIDAD = (r"(?:conforme a|seg[uú]n|por mandato de|en aplicaci[oó]n de|"
                     r"fundamento|autoridad|deriva de|exigid[oa] por)\s*[«\"'`(]?\s*ADR-{n}"
                     r"|ADR-{n}\s*§")

# La norma que introdujo la exigencia de validación humana registrada. Todo lo
# anterior a ella se lee sin retroactividad (ver docstring).
AUTORIDAD_VALIDACION = "ADR-035"

SI = "si"
NO = "no"
NO_DETERMINABLE = "no_determinable"
NO_ES_DECISION = "no_es_decision"   # calificación de evidencia, no acto de gobierno

# Estados que NO son decisiones de gobernanza sino calificaciones de evidencia.
# ADR-019 es `STRONGLY_SUPPORTED` **a propósito** — Regla de Oro 10: «no congelar
# teoría antes que el grafo hable». Tratarlo como un ADR sin validar sería acusar
# al canon de cumplir su propia regla.
_EVIDENCIA = ("supported", "strongly_supported")
_REVERTIDO = ("revertido",)


@lru_cache(maxsize=1)
def _crudos() -> list[tuple[str, str, str]]:
    """(nombre, cabecera, texto) de cada ADR. Sin interpretar."""
    salida = []
    for d in ADR_DIRS:
        if not d.is_dir():
            continue
        for f in sorted(d.glob("ADR-*.md")):
            t = f.read_text(encoding="utf-8", errors="replace")
            salida.append((f.name, t[:1400], t))
    return sorted(salida)


def _linea_estado(cabecera: str) -> str:
    m = re.search(r"(?im)^\s*[-*|]?\s*(?:\*\*)?(?:estado|status)(?:\*\*)?\s*[:|]\s*(.{0,140})",
                  cabecera)
    return m.group(1).strip() if m else ""


def _numero(nombre: str) -> str:
    m = re.match(r"ADR-(\d{3})", nombre)
    return m.group(1) if m else ""


def adr(nombre: str) -> dict:
    """Todo lo que se puede decir de UN ADR, separando declarado de derivado."""
    cab, texto = next(((c, t) for n, c, t in _crudos() if n == nombre), ("", ""))
    linea = _linea_estado(cab)
    plano = re.sub(r"[^a-záéíóúñ_ ]", " ", linea.lower())

    # DERIVADO: ¿consta validación humana? Es lo único que ADR-035 §5 exige.
    if any(e in plano.split() or e in plano for e in _EVIDENCIA):
        validacion = NO_ES_DECISION
    elif any(r in plano for r in _REVERTIDO):
        validacion = NO_ES_DECISION
    elif re.search(r"\bpendiente\b", plano):
        validacion = NO            # lo dice él mismo: aún no validado
    elif re.search(r"\bjavo\b", plano):
        validacion = SI
    else:
        validacion = NO_DETERMINABLE

    fecha = re.search(r"20\d\d-\d\d-\d\d", linea)
    citados = sorted({f"ADR-{n}" for n in re.findall(r"ADR-(\d{3})", texto)}
                     - {f"ADR-{_numero(nombre)}"})
    return {
        "id": f"ADR-{_numero(nombre)}",
        "archivo": nombre,
        # DECLARADO · literal, sin normalizar. Normalizarlo sería fabricar la
        # taxonomía que ningún artefacto establece.
        "estado_declarado": linea,
        "fecha_declarada": fecha.group(0) if fecha else "",
        "validador_registrado": "Javo" if re.search(r"\bjavo\b", plano) else "",
        # DERIVADO · lo único que la autoridad permite computar.
        "validacion_humana": validacion,
        "autoridad_invocada": AUTORIDAD_VALIDACION + " §5" if "035" in texto else "",
        "cita_a": citados,
        "anterior_a_la_autoridad": _numero(nombre) < "035",
    }


def todos() -> list[dict]:
    return [adr(n) for n, _, _ in _crudos()]


def referencias_no_resueltas() -> list[dict]:
    """Referencias a un ADR que no aparece en ningún directorio conocido.

    Es una de las ocho propiedades que el colega pidió atacar: *«relaciones
    declaradas que ningún artefacto puede demostrar»*. Pero se llama **no
    resuelta**, no «rota», y se devuelve con su contexto — porque las cinco
    primeras que este módulo encontró eran todas falsas:

        ADR-005·011·012   existían, en el otro directorio  → universo incompleto
        ADR-054           «obligaría a abrir un ADR-054»   → mención hipotética

    Una referencia sin resolver es una ·SEÑAL con su línea, para que alguien la
    lea; llamarla rota sería un ⛔ERROR, y decidirlo exige leer la frase."""
    existentes = {a["id"] for a in todos()}
    fuera = []
    for nombre, _, texto in _crudos():
        yo = f"ADR-{_numero(nombre)}"
        for n in sorted(set(re.findall(r"ADR-(\d{3})", texto))):
            cid = f"ADR-{n}"
            if cid == yo or cid in existentes:
                continue
            m = re.search(rf".{{0,70}}{cid}.{{0,50}}", texto)
            fuera.append({"desde": yo, "referencia": cid,
                          "contexto": (m.group(0).strip() if m else "")[:118]})
    return fuera


@lru_cache(maxsize=1)
def _corpus_referente() -> list[tuple[str, str]]:
    """Todo lo que puede referirse a un ADR: canon, código, artefactos compilados.

    El universo de referentes se declara aquí y se barre entero — no se pregunta
    «¿lo cita el código?» sino «¿quién lo cita, y de qué manera?»."""
    piezas = []
    # ⚠️ `*.md` DE LA RAÍZ INCLUIDO, y faltaba. La primera versión barría docs/,
    # app/, scripts/, governance/ e identity/ — y dejaba fuera `CLAUDE.md`, que
    # es donde viven las Reglas de Oro. Se notó porque el patrón «ningún script
    # lo recalcula» dio 0 artefactos siendo una de las reglas más citadas del
    # sistema: el universo del corpus referente estaba tan incompleto como el de
    # los ADR, y por la misma razón — se listaron carpetas en vez de derivarlas.
    for patron in ("*.md", "docs/**/*.md", "docs/brn/*.yaml", "app/**/*.py",
                   "scripts/**/*.py", "governance/*.md", "identity/*.md",
                   "data/brn_manifest.json", "data/brn_config.json"):
        for f in RAIZ.glob(patron):
            rel = f.relative_to(RAIZ).as_posix()
            # El inventario no se cuenta a sí mismo: este módulo nombra ADR en
            # sus comentarios y se colaría como «referente», inflando la
            # centralidad de lo que él mismo está midiendo. Mismo principio que
            # `arbol_limpio` en el registrador — un dato que se incluye a sí
            # mismo deja de informar.
            if any(p in rel for p in ("__pycache__", "worktrees", "node_modules",
                                      "app/agents/arquitectura.py")):
                continue
            try:
                piezas.append((rel, f.read_text(encoding="utf-8", errors="replace")))
            except OSError:
                continue
    return piezas


def rol_observable(adr_id: str) -> dict:
    """Qué lugar ocupa REALMENTE un ADR en la red, sin declarar si gobierna.

    El colega lo pidió así tras el hallazgo de `ADR-007`: *«No "gobierna porque
    Javo dice que gobierna", sino: ¿qué artefactos lo tratan como autoridad?
    ¿qué artefactos dependen de él?»*. Si resulta citado por el canon, por el
    compilador y por otros ADR, hay **evidencia de centralidad** aunque nadie le
    ponga todavía la etiqueta política de vigente.

    ⚠️ Centralidad no es vigencia. Un ADR muy citado puede estar derogado, y uno
    poco citado puede ser fundacional. Esto mide presencia en la red, nada más —
    y decirlo es parte de no afirmar de más."""
    n = adr_id.split("-")[-1]
    aut = re.compile(_PATRON_AUTORIDAD.format(n=n), re.I)
    rel: dict[str, list[str]] = {}
    for ruta, texto in _corpus_referente():
        if adr_id not in texto:
            continue
        if ruta.endswith((f"{adr_id}.md",)) or f"/{adr_id}_" in f"/{ruta}":
            continue                                   # no se cita a sí mismo
        tipos = [MENCION]
        if aut.search(texto):
            tipos.append(AUTORIDAD)
        if ruta.endswith(".py"):
            tipos.append(EN_CODIGO)
        elif "/brn/" in ruta and ruta.endswith(".yaml"):
            tipos.append(EN_CANON)
        elif ruta.startswith("data/"):
            tipos.append(EN_COMPILADO)
        for t in tipos:
            rel.setdefault(t, []).append(ruta)
    return {
        "id": adr_id,
        "relaciones": {k: sorted(set(v)) for k, v in rel.items()},
        "artefactos_que_lo_refieren": len({r for v in rel.values() for r in v}),
        "lo_invocan_como_autoridad": len(rel.get(AUTORIDAD, [])),
    }


def centralidad() -> list[dict]:
    """Los ADR ordenados por presencia observable en la red. NO por importancia."""
    filas = [rol_observable(a["id"]) for a in todos()]
    return sorted(filas, key=lambda r: (-r["lo_invocan_como_autoridad"],
                                        -r["artefactos_que_lo_refieren"], r["id"]))


def cobertura_arquitectonica() -> dict:
    """La vista de Capa 2, con su universo declarado (Capa 0 lo exige)."""
    filas = todos()
    por_validacion: dict[str, list[str]] = {}
    for a in filas:
        por_validacion.setdefault(a["validacion_humana"], []).append(a["id"])

    sin_constancia = [a["id"] for a in filas
                      if a["validacion_humana"] == NO_DETERMINABLE]
    posteriores = [a["id"] for a in filas
                   if a["validacion_humana"] == NO_DETERMINABLE
                   and not a["anterior_a_la_autoridad"]]
    return {
        "adr": filas,
        "universo": {
            "que": "decisiones de arquitectura registradas como ADR",
            "donde": "docs/adr/ADR-*.md",
            "como": "cabecera de cada archivo; el estado se lee LITERAL y no se "
                    "normaliza, porque ningún artefacto declara la equivalencia "
                    "entre los nombres de las tres épocas",
            "hallados": len(filas),
            "fuera_de_alcance": [
                "decisiones de arquitectura que no se registraron como ADR: no "
                "existen para este inventario",
                "si dos estados distintos significan lo mismo — requiere una "
                "decisión de gobernanza, no una inferencia",
                "si un ADR gobierna HOY: este módulo no computa vigencia",
                "por qué doce ADR viven en `corpus_externo/` y no en `adr/`: la "
                "partición se cuenta, su razón no consta en ningún artefacto",
            ],
        },
        "por_validacion_humana": por_validacion,
        "sin_constancia_de_validacion": sorted(sin_constancia),
        "sin_constancia_y_posteriores_a_la_autoridad": sorted(posteriores),
        "referencias_no_resueltas": referencias_no_resueltas(),
        "afirmacion_sostenible": _afirmar(filas, sin_constancia, posteriores),
    }


def _afirmar(filas: list[dict], sin_constancia: list[str],
             posteriores: list[str]) -> str:
    con = sum(1 for a in filas if a["validacion_humana"] == SI)
    base = (f"De {len(filas)} decisiones de arquitectura registradas, {con} "
            f"acreditan validación humana en su propio estado. **No se afirma "
            f"cuáles gobiernan hoy**: ningún artefacto declara la equivalencia "
            f"entre los nombres de estado de las tres épocas.")
    if sin_constancia:
        base += (f" Sin constancia de validación: {len(sin_constancia)} — y en "
                 f"{len(sin_constancia) - len(posteriores)} de ellas el silencio "
                 f"es anterior a {AUTORIDAD_VALIDACION}, la norma que introdujo "
                 f"la obligación de registrarla: no consta ≠ no se validó.")
    if posteriores:
        base += (f" ⚠️ Posteriores a la autoridad y aun así sin constancia: "
                 f"{', '.join(posteriores)} — ahí la exigencia ya regía.")
    return base
