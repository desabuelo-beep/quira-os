"""
app/agents/apropiacion.py — qué capacidades son de QUIRA, y hasta qué punto
===========================================================================
POR QUÉ ES TRANSVERSAL (2026-08-19 · ADR-051 §2d). El colega, al ver la escalera
nacer dentro de d07:

> *«La separación capacidad ≠ ejecución ≠ validación es exactamente la que
> necesitábamos. Y yo la convertiría en una pieza transversal del modelo de
> QUIRA, no solamente en una peculiaridad de d07.»*

Tiene razón por una consecuencia práctica: si cada dominio define su propia idea
de «está listo», el sistema no puede responder **una sola pregunta** —¿qué sabe
hacer QUIRA hoy?— sin que alguien recorra siete implementaciones distintas y las
concilie a mano. Que es exactamente el trabajo que este módulo existe para que
nadie tenga que volver a hacer.

CINCO DIMENSIONES, NO UNA ESCALERA DE TRES (colega, 2026-08-19):

    CAPACIDAD    ¿puede hacerlo?                 el código existe y está declarado
    SUJETO       ¿sobre quién puede afirmarlo?   ámbito de validez — NO es madurez
    EJECUCIÓN    ¿lo hizo realmente?             sello de una corrida propia
    EVIDENCIA    ¿qué conserva de haberlo hecho? insumos y salidas con SHA
    VALIDACIÓN   ¿puede reproducirse?            una prueba nombrada que existe

**El grado de apropiación es una FUNCIÓN DERIVADA de esas dimensiones, no una
dimensión más.** La distinción no es académica: mientras el grado fue un dato
independiente, el sistema pudo perder el sujeto al construir la etiqueta —y lo
hizo, el mismo día en que se añadió—. Ahora el sujeto viaja dentro de la
afirmación y **no puede desprenderse de ella**:

    contenido → reproducible → sujeto 130801 → evidencia sellada → prueba E

es una afirmación mucho más fuerte que `contenido → validado`, porque la segunda
admite inflación silenciosa: suena nacional y es de un municipio.

**Los grados se derivan; no se declaran.** Es la Regla de Oro 3 aplicada al
propio sistema: sin evidencia, no hay dato — tampoco cuando el dato trata de
nosotros. Una capacidad que se dice «validada» sin prueba que la ejercite es el
mismo tipo de afirmación que este observatorio existe para no hacer.

LO QUE ESTO PERMITE DECIR, y es lo importante: **«esto todavía no lo sé hacer».**
Para un sistema de inteligencia pública, declarar el propio límite vale tanto
como producir un resultado — y es lo que separa un mapa de capacidades de una
lista de intenciones.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

CAPACIDAD = "capacidad"
EJECUCION = "ejecucion"
VALIDADO = "validado"
AUSENTE = "ausente"

# El orden importa: se usa para comparar y para agregar. No es alfabético.
ESCALERA = [AUSENTE, CAPACIDAD, EJECUCION, VALIDADO]

ETIQUETA_PUBLICA = {
    # Lenguaje de administración pública — esto puede llegar a una pantalla.
    VALIDADO: "Reproducible",
    EJECUCION: "El sistema la ejecuta",
    CAPACIDAD: "Sin ejecución registrada",
    AUSENTE: "No disponible",
}


# ══════════════════════════════════════════════════════════════════════════════
# TRES CLASES QUE NO SON LA MISMA COSA · ADR-051 §2c y §10
# ══════════════════════════════════════════════════════════════════════════════
# El colega, sobre los 636 artefactos (2026-08-19):
#
# > *«Yo incluso evitaría llamarlos simplemente "datos" en determinados
# > contextos, porque puede producir una confusión semántica. […] Y eso debería
# > estar codificado en metadatos, no únicamente en ADR-051.»*
#
# Un ADR que nadie lee cuando abre un JSON no protege nada. Estas constantes se
# escriben DENTRO de cada artefacto producido, para que su naturaleza viaje con
# él y no dependa de que quien lo consuma recuerde de dónde salió.
MATERIAL_DE_INGENIERIA = "material_de_ingenieria"
EVIDENCIA_DE_OBSERVACION = "evidencia_de_observacion"
RESULTADO_OFICIAL = "resultado_oficial"

CLASES = {
    MATERIAL_DE_INGENIERIA: (
        "Producido durante I+D para construir, probar o calibrar el sistema. "
        "Puede ser exacto y aun así NO sostiene una afirmación sobre el sujeto "
        "observado: sirve como fixture, caso límite o regresión."),
    EVIDENCIA_DE_OBSERVACION: (
        "Adquirido por QUIRA con procedencia sellada, sobre un sujeto "
        "declarado. Puede sostener hallazgos; no los constituye."),
    RESULTADO_OFICIAL: (
        "Hallazgo acreditado que recorrió la cadena completa y fue validado "
        "conforme al canon. Es lo único publicable como observación."),
}


def clasificar_artefacto(clase: str, motivo: str = "") -> dict:
    """El bloque que todo artefacto debe llevar en su `_meta`.

    Sin esto, un JSON con 636 artefactos correctos es indistinguible de una
    observación oficial — y esa confusión es exactamente la que separa una
    plataforma de inteligencia pública de una colección de datos."""
    if clase not in CLASES:
        raise ValueError(f"clase epistemológica desconocida: {clase}")
    d = {"clase_epistemologica": clase, "significa": CLASES[clase]}
    if motivo:
        d["por_que"] = motivo
    return d


class AfirmacionSinSujeto(ValueError):
    """Se intentó afirmar una capacidad ejecutada o reproducible sin declarar su
    ámbito. No es un aviso: la afirmación no llega a existir."""


@dataclass(frozen=True)
class Afirmacion:
    """LA UNIDAD DEL SISTEMA · lo que QUIRA puede decir, con todo lo que hace
    falta para poder decirlo.

    ⚠️ SE LLAMABA `Grado`, y el nombre inducía el error (colega, 2026-08-19):

    > *«La unidad correcta de QUIRA no es el grado, sino la afirmación. Grado no
    > es una sexta dimensión: es una función derivada de las cinco.»*

    Mientras el objeto se llamó `Grado`, lo natural era tratarlo como un dato
    —una etiqueta que se pasa, se copia y se reconstruye— y así fue como el
    sujeto se perdió al reconstruirlo. Un objeto llamado `Afirmacion` invita a
    preguntarse *«¿afirmación de qué, sobre quién?»*, que es exactamente la
    pregunta correcta. Renombrar aquí no es cosmética: elimina la ambigüedad que
    produjo el defecto (Regla de Oro 7).

    Un grado sin su fundamento es una afirmación, no una medición.

    ⚠️ Y SIN SUJETO, MIENTE POR OMISIÓN (colega, 2026-08-19):

    > *«La escalera responde "¿qué sabe hacer QUIRA?" pero no "¿sobre quién
    > puede hacerlo?". Hoy tenían: QUIRA sabe hacer X + X está configurado para
    > Montecristi. Eso produce una ilusión peligrosa.»*

    «Sé descargar los conjuntos de datos» y «sé descargarlos del portal de
    Montecristi» son afirmaciones distintas, y sólo la segunda es verdadera. La
    afirmación completa que este sistema puede sostener es:

        capacidad + sujeto + ejecución + evidencia + validación
    """
    capacidad: str
    grado: str
    fundamento: str
    dominio: str = ""
    sujeto: str = ""             # ámbito de validez · NO es un nivel de madurez

    def __post_init__(self):
        # INVARIANTE ESTRUCTURAL, no una prueba. Una capacidad que se afirma
        # ejecutada o reproducible **sin decir sobre quién** es precisamente la
        # inflación silenciosa que este módulo existe para impedir; hacerla
        # imposible de construir es más fuerte que detectarla después.
        if self.grado in (EJECUCION, VALIDADO) and not self.sujeto:
            raise AfirmacionSinSujeto(
                f"«{self.capacidad}» se declara {self.grado} sin sujeto: una "
                f"ejecución ocurrió necesariamente sobre alguien")

    @property
    def es_operativa(self) -> bool:
        return self.grado == VALIDADO

    def afirmacion(self) -> str:
        """Lo que se puede decir de esta capacidad, con su alcance a la vista."""
        if self.grado != VALIDADO:
            return f"{self.capacidad}: {ETIQUETA_PUBLICA[self.grado].lower()}"
        alcance = f" sobre {self.sujeto}" if self.sujeto else " — sujeto sin acreditar"
        return f"{self.capacidad}: reproducible{alcance}"


# El nombre anterior sigue disponible: hay código y pruebas que lo usan, y
# romperlos para ganar un nombre no sería una mejora. Pero el nombre que enseña
# el modelo es `Afirmacion`.
Grado = Afirmacion


def existe_prueba(nombre: str) -> bool:
    """¿Existe de verdad la prueba que se invoca como acreditación?

    Una referencia a una prueba inexistente acreditaría reproducibilidad sin
    nada que la sostenga — el equivalente exacto de citar un artículo de ley que
    no existe (Regla de Oro 3)."""
    for f in (RAIZ / "tests").glob("test_*.py"):
        if f"def {nombre}(" in f.read_text(encoding="utf-8", errors="replace"):
            return True
    return False


def derivar(capacidad: str, *, hay_codigo: bool, ejecutada_por_el_agente: bool,
            prueba: str | None, dominio: str = "", sujeto: str = "") -> "Afirmacion":
    """La escalera, aplicada a una capacidad cualquiera.

    Cada dominio aporta los tres hechos que sí conoce —si tiene el código, si
    hay registro de una corrida propia, y qué prueba la acredita—; el grado sale
    de aquí, igual para todos."""
    if not hay_codigo:
        return Afirmacion(capacidad, AUSENTE, "no existe el código operativo", dominio, sujeto)
    if not ejecutada_por_el_agente:
        return Afirmacion(capacidad, CAPACIDAD,
                     "el código existe, pero no hay registro de que QUIRA lo "
                     "haya ejecutado", dominio, "")
    if not sujeto:
        # Hay sello de ejecución pero no dice sobre quién. La afirmación NO se
        # eleva: se degrada al grado que la evidencia sostiene. Es la misma
        # regla que se aplica al sujeto observado —sin procedencia, no hay
        # dato— aplicada al propio sistema.
        return Afirmacion(capacidad, CAPACIDAD,
                     "hay registro de ejecución pero SIN sujeto declarado · la "
                     "afirmación se degrada en vez de suponer el ámbito",
                     dominio, "")
    if not prueba:
        return Afirmacion(capacidad, EJECUCION,
                     "QUIRA la ejecutó · sin prueba de reproducibilidad declarada",
                     dominio, sujeto)
    if not existe_prueba(prueba):
        return Afirmacion(capacidad, EJECUCION,
                     f"QUIRA la ejecutó · la prueba «{prueba}» está declarada "
                     f"pero NO existe", dominio, sujeto)
    return Afirmacion(capacidad, VALIDADO,
                 f"QUIRA la ejecutó y «{prueba}» la reproduce desde cero",
                 dominio, sujeto)


def resumir(grados: list[Afirmacion]) -> dict:
    """El estado agregado, para responder «¿qué sabe hacer QUIRA hoy?».

    Devuelve también `operativas`, que es la única cifra publicable: las demás
    describen trabajo en curso, no capacidad acreditada."""
    conteo = {g: 0 for g in ESCALERA}
    for x in grados:
        conteo[x.grado] = conteo.get(x.grado, 0) + 1
    total = len(grados) or 1
    sujetos = sorted({x.sujeto for x in grados if x.sujeto})
    return {
        "total": len(grados),
        "por_grado": conteo,
        "operativas": conteo[VALIDADO],
        "proporcion_operativa": round(conteo[VALIDADO] / total, 3),
        "limite_declarado": [x.capacidad for x in grados if x.grado != VALIDADO],
        # Sobre quién se acreditó lo acreditado. Una capacidad demostrada sobre
        # un solo sujeto NO es una capacidad nacional, y la cifra lo dice sola.
        "sujetos_acreditados": sujetos,
        "alcance": ("ningún sujeto acreditado" if not sujetos else
                    f"acreditado sobre {len(sujetos)} sujeto(s): {', '.join(sujetos)}"),
    }


def lo_que_todavia_no_sabe_hacer(grados: list[Afirmacion]) -> list[str]:
    """La frase que un sistema de inteligencia pública tiene que poder decir.

    No es una lista de pendientes de proyecto: es el **límite declarado** del
    instrumento en este momento, en los mismos términos en que se declara la
    ausencia de evidencia del sujeto observado."""
    return [f"{x.capacidad}: {x.fundamento}" for x in grados if x.grado != VALIDADO]


# ══════════════════════════════════════════════════════════════════════════════
# AUTOCONOCIMIENTO · lo que QUIRA puede decir de sí misma, con evidencia
# ══════════════════════════════════════════════════════════════════════════════
# El colega, cerrando la iteración del 2026-08-19:
#
# > *«La pregunta que QUIRA debería poder contestar no es "¿qué hicimos hoy?"
# > sino: ¿qué sé hacer, qué ejecuté, qué puedo demostrar que reproduzco, sobre
# > qué sujetos puedo hacerlo y qué todavía no sé hacer? Y además: ¿qué parte de
# > esa afirmación proviene de QUIRA y qué parte de I+D asistida? Si QUIRA puede
# > generar esa respuesta por sí misma, a partir de evidencia sellada, la
# > escalera dejó de ser documentación: se convirtió en una propiedad del
# > sistema.»*
#
# Eso es lo que hace esta función. Ni una línea de su salida es una declaración:
# todo sale de los sellos de ejecución y de la existencia real de las pruebas.

def autoconocimiento(grados: list[Afirmacion]) -> dict:
    """Las cinco preguntas, respondidas desde evidencia.

    La sexta —qué proviene de I+D asistida— se responde por diferencia: **todo
    lo que no está en `demuestro_que_reproduzco`**. Si una capacidad produjo
    resultados durante el desarrollo pero el sistema no puede reproducirlos, esos
    resultados son material de ingeniería y no observación (ADR-051 §2c)."""
    r = resumir(grados)
    return {
        "que_se_hacer": [g.capacidad for g in grados if g.grado != AUSENTE],
        "que_ejecute": [g.capacidad for g in grados
                        if g.grado in (EJECUCION, VALIDADO)],
        "demuestro_que_reproduzco": [g.capacidad for g in grados
                                     if g.grado == VALIDADO],
        "sobre_que_sujetos": r["sujetos_acreditados"],
        "que_todavia_no_se_hacer": lo_que_todavia_no_sabe_hacer(grados),
        "atribuible_a_id_asistida": [
            g.capacidad for g in grados if g.grado != VALIDADO],
        "advertencia": (
            "Las capacidades que no figuran como reproducibles pueden haber "
            "producido resultados correctos durante el desarrollo. Esos "
            "resultados son material de ingeniería: no constituyen observación "
            "atribuible al sistema (ADR-051 §2c)."),
    }


def informe(grados: list[Afirmacion]) -> str:
    """El autoconocimiento en texto plano, para consola y para el expediente."""
    a = autoconocimiento(grados)
    r = resumir(grados)
    L = ["QUÉ SÉ HACER, QUÉ PUEDO DEMOSTRAR Y QUÉ NO",
         "=" * 72,
         f"  capacidades con código      {len(a['que_se_hacer']):3}",
         f"  ejecutadas por el sistema   {len(a['que_ejecute']):3}",
         f"  reproducibles (demostradas) {len(a['demuestro_que_reproduzco']):3}",
         f"  alcance                     {r['alcance']}",
         "",
         "  LO QUE PUEDO AFIRMAR:"]
    L += [f"     · {g.afirmacion()}" for g in grados if g.grado == VALIDADO] or \
         ["     · nada todavía"]
    L += ["", "  LO QUE TODAVÍA NO SÉ HACER:"]
    L += [f"     · {x}" for x in a["que_todavia_no_se_hacer"]] or ["     · —"]
    L += ["", "  " + a["advertencia"]]
    return "\n".join(L)

# ── El autoconocimiento como ARTEFACTO, no como pantalla ───────────────────────
# El colega, cerrando (2026-08-19):
#
# > *«El autoconocimiento de QUIRA no debería ser solamente un reporte bonito en
# > la consola. Debería convertirse en un artefacto derivado y sellado.»*
#
# La diferencia es sustantiva. Un texto en pantalla se lee y se olvida; un
# artefacto con SHA, fecha de derivación y fuentes declaradas **se puede citar,
# comparar entre corridas y auditar**. Y sobre todo: se le aplica la misma
# exigencia que QUIRA le pide al sujeto observado —procedencia verificable— en
# lugar de eximirse a sí misma de ella.

_ARTEFACTO = RAIZ / "data" / "quira" / "autoconocimiento.json"


def sellar_autoconocimiento(grados: list[Afirmacion],
                            fuentes: list[str] | None = None) -> dict:
    """Deriva el autoconocimiento, lo sella y lo persiste.

    El SHA se calcula sobre el contenido **sin** la fecha ni el propio sello:
    así dos derivaciones del mismo estado dan el mismo hash y se puede saber si
    el sistema cambió, no sólo si el reloj avanzó."""
    import datetime as _dt
    import hashlib
    import json

    cuerpo = autoconocimiento(grados)
    cuerpo["resumen"] = resumir(grados)
    cuerpo["afirmaciones"] = [
        {"capacidad": g.capacidad, "dominio": g.dominio, "grado": g.grado,
         "sujeto": g.sujeto, "fundamento": g.fundamento}
        for g in grados]

    sha = hashlib.sha256(
        json.dumps(cuerpo, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()

    doc = {
        "_meta": {
            "que_es": "perímetro de lo que QUIRA sabe hacer, derivado de su "
                      "propia evidencia",
            "derivado": _dt.datetime.now().isoformat(timespec="seconds"),
            "sha256_estado": sha,
            "fuentes": fuentes or [
                "sellos de ejecución de cada dominio (cadena_estado.json)",
                "perfiles de sujeto (data/sujetos/)",
                "existencia real de las pruebas nombradas (tests/)",
            ],
            "advertencia_de_lectura":
                "NO DECLARADO MANUALMENTE · DERIVADO POR QUIRA. Ninguna línea de "
                "este documento es una afirmación de sus autores: todas salen de "
                "artefactos sellados. Si una capacidad no figura como "
                "reproducible, los resultados que haya producido son material de "
                "ingeniería y no observación atribuible (ADR-051 §2c).",
        },
        **cuerpo,
    }
    _ARTEFACTO.parent.mkdir(parents=True, exist_ok=True)
    _ARTEFACTO.write_text(json.dumps(doc, ensure_ascii=False, indent=1),
                          encoding="utf-8")
    return doc


def leer_autoconocimiento() -> dict | None:
    """El último perímetro sellado, si existe."""
    import json
    if not _ARTEFACTO.exists():
        return None
    try:
        return json.loads(_ARTEFACTO.read_text(encoding="utf-8"))
    except Exception:                                    # noqa: BLE001
        return None

# ══════════════════════════════════════════════════════════════════════════════
# COBERTURA DE DEFENSA · «sin atacar» no es «seguro»
# ══════════════════════════════════════════════════════════════════════════════
# El colega, cerrando la jornada de ataques (2026-08-19):
#
# > *«"Sin atacar" no puede convertirse en "seguro" por defecto. Eso debería
# > entrar directamente en el autoconocimiento de QUIRA.»*
#
# Es el mismo error que el sistema acaba de descubrir a nivel de sujeto, ahora a
# nivel de plataforma: **confundir ausencia de contradicción con evidencia de
# validez.** d07 tiene sello, gate de sujeto, huella y once ataques ejecutados
# contra él; d01, d02, d03, d08 y d09 no tienen ninguna de esas defensas — no
# porque hayan resistido, sino porque nadie las ha puesto ni probado.
#
# El estado se DERIVA de la evidencia disponible, como todo lo demás aquí: se
# mira qué defensas existen en el código del dominio y qué pruebas adversariales
# lo nombran. Nadie declara «protegido».
PROTEGIDO_Y_ATACADO = "protegido_y_atacado"
PROTEGIDO_SIN_ATACAR = "protegido_sin_atacar"
NO_PROTEGIDO = "no_protegido"
SIN_DETERMINAR = "no_determinable"

_DEFENSAS = ("_SELLO_CADENA", "sujeto_huella", "gate SUJETO", "_sujeto_actual")


def cobertura_de_defensa(dominio: str) -> dict:
    """Qué defensas tiene este dominio y cuáles se han ejercitado contra él.

    Devuelve un estado y su fundamento. `no_protegido` no es una acusación: es
    la lectura honesta de que ese dominio todavía no tiene el mecanismo, y por
    tanto un ataque equivalente no encontraría defensa que romper."""
    carpeta = RAIZ / "app" / "agents" / dominio
    if not carpeta.exists():
        return {"dominio": dominio, "estado": SIN_DETERMINAR,
                "fundamento": "no existe el paquete del dominio"}

    fuente = "\n".join(f.read_text(encoding="utf-8", errors="replace")
                       for f in carpeta.glob("*.py"))
    tiene = [d for d in _DEFENSAS if d in fuente]

    ataques = []
    for f in (RAIZ / "tests").glob("test_*adversarial*.py"):
        txt = f.read_text(encoding="utf-8", errors="replace")
        if f".{dominio}" in txt or f"/{dominio}" in txt:
            ataques = [ln.split("(")[0].replace("def ", "").strip()
                       for ln in txt.splitlines() if ln.startswith("def test_")]

    if not tiene:
        return {"dominio": dominio, "estado": NO_PROTEGIDO, "defensas": [],
                "ataques_ejecutados": len(ataques),
                "fundamento": "no se halló ninguna de las defensas de identidad "
                              "de sujeto en el código del dominio"}
    if not ataques:
        return {"dominio": dominio, "estado": PROTEGIDO_SIN_ATACAR,
                "defensas": tiene, "ataques_ejecutados": 0,
                "fundamento": "tiene las defensas, pero ninguna prueba "
                              "adversarial las ha ejercitado — resistir no está "
                              "demostrado, sólo no refutado"}
    return {"dominio": dominio, "estado": PROTEGIDO_Y_ATACADO,
            "defensas": tiene, "ataques_ejecutados": len(ataques),
            "fundamento": f"{len(ataques)} ataques ejecutados contra sus defensas"}


def cobertura_de_la_plataforma(dominios: list[str] | None = None) -> dict:
    """El perímetro de defensa de todos los dominios, en una sola lectura.

    Impide la afirmación que el colega marcó en rojo: *«QUIRA ya tiene un
    mecanismo transversal de integridad de sujeto»*. Lo que se puede decir es
    cuál lo tiene demostrado y cuáles no."""
    dominios = dominios or sorted(
        d.name for d in (RAIZ / "app" / "agents").iterdir()
        if d.is_dir() and d.name.startswith("d"))
    filas = [cobertura_de_defensa(d) for d in dominios]
    por_estado = {}
    for f in filas:
        por_estado.setdefault(f["estado"], []).append(f["dominio"])
    return {
        "dominios": filas,
        "por_estado": por_estado,
        "afirmacion_sostenible": (
            "QUIRA ha demostrado un mecanismo de integridad de sujeto en " +
            ", ".join(por_estado.get(PROTEGIDO_Y_ATACADO, ["ninguno"])) +
            "; los demás dominios permanecen sin evidencia de haber pasado por "
            "ese mecanismo."),
    }
