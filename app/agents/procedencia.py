"""
app/agents/procedencia.py — la cadena que sostiene una afirmación sobre el sujeto
=================================================================================
POR QUÉ EXISTE (2026-08-19 · ADR-042 §6-bis). El colega convirtió la regla de
atribución en una cadena de preguntas, y luego pidió lo que faltaba:

> *«No basta con que exista evidencia; debe existir evidencia que responda la
> cadena pertinente. Si una capa no puede responderse, no se inventa la
> respuesta: se degrada la afirmación.»*

Mientras esa cadena vivió sólo en un documento, se cumplía cuando alguien se
acordaba. Aquí se ejecuta.

LAS SIETE CAPAS. Cuando QUIRA afirma **«el GAD no publicó X»**, debe poder
responder, en orden:

    1 fuente                 ¿de qué fuente institucional se habla?
    2 captura                ¿se intentó traerla, y cuándo?
    3 estado_adquisicion     ¿en qué estado terminó? (ADR-042 §6)
    4 evidencia              ¿qué artefacto quedó, con qué SHA?
    5 verificador            ¿qué componente la interpretó?
    6 prueba_del_verificador ¿qué prueba respalda esa interpretación?
    7 sujeto                 ¿sobre quién se afirma?

EL PRINCIPIO QUE GOBIERNA ESTE MÓDULO, y es el que emergió de toda la sesión:

    **Cuando la cadena no puede sostener una afirmación, QUIRA degrada la
    afirmación; nunca rellena el vacío.**

Degradar no es fallar. Es la conducta correcta: la ausencia de procedencia no
autoriza a inferir solidez, del mismo modo que la ausencia de evidencia no
autoriza a inferir hechos sobre el sujeto (Principio Rector · CAPA 0).

QUÉ NO HACE. No juzga si la afirmación es cierta —eso lo dice la evidencia
contra la Regla Operativa—; dice **cuánto peso puede soportar**.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field, fields
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# Los tres pesos que una afirmación puede soportar, de menor a mayor. Coinciden
# a propósito con los niveles semánticos de ADR-051 §4: este módulo no inventa
# una escala nueva, decide en cuál de las existentes cae cada afirmación.
NO_DETERMINABLE = "no_determinable"          # falta procedencia · no se afirma nada
HALLAZGO_DE_VERIFICABILIDAD = "hallazgo_de_verificabilidad"   # se afirma sobre el ACTO de verificar
HECHO_VERIFICABLE = "hecho_verificable"      # se afirma sobre el sujeto

# Qué capas hacen falta para cada peso. La progresión no es arbitraria: para
# decir algo del sujeto hay que poder recorrer la cadena entera; para decir que
# NO se pudo verificar basta con demostrar que se intentó y en qué terminó.
EXIGE = {
    HECHO_VERIFICABLE: ("fuente", "captura", "estado_adquisicion", "evidencia",
                        "verificador", "prueba_del_verificador", "sujeto"),
    HALLAZGO_DE_VERIFICABILIDAD: ("fuente", "captura", "estado_adquisicion",
                                  "sujeto"),
    NO_DETERMINABLE: (),
}

PREGUNTA = {
    "fuente": "¿de qué fuente institucional se habla?",
    "captura": "¿se intentó traerla, y cuándo?",
    "estado_adquisicion": "¿en qué estado terminó la adquisición?",
    "evidencia": "¿qué artefacto quedó, con qué identidad?",
    "verificador": "¿qué componente la interpretó?",
    "prueba_del_verificador": "¿qué prueba respalda esa interpretación?",
    "sujeto": "¿sobre quién se afirma?",
}


@dataclass(frozen=True)
class Procedencia:
    """Las respuestas que QUIRA tiene para una afirmación concreta.

    Un campo vacío no es un defecto que ocultar: es una capa sin responder, y su
    consecuencia está declarada de antemano."""
    fuente: str = ""
    captura: str = ""
    estado_adquisicion: str = ""
    evidencia: str = ""
    verificador: str = ""
    prueba_del_verificador: str = ""
    sujeto: str = ""

    def capas_respondidas(self) -> list[str]:
        return [f.name for f in fields(self) if getattr(self, f.name)]

    def capas_sin_responder(self) -> list[str]:
        return [f.name for f in fields(self) if not getattr(self, f.name)]


@dataclass
class Sostenida:
    """Una afirmación con el peso que su cadena permite, y por qué ése."""
    enunciado: str
    peso: str
    procedencia: Procedencia
    faltan: list[str] = field(default_factory=list)
    degradada_desde: str = ""

    @property
    def habla_del_sujeto(self) -> bool:
        """Sólo el peso máximo dice algo del sujeto observado. Los otros dos
        hablan de nuestra capacidad de verificar, que es otra cosa."""
        return self.peso == HECHO_VERIFICABLE


def _responde(p: Procedencia, capa: str) -> bool:
    """¿La capa está respondida DE VERDAD?

    ⚠️ `prueba_del_verificador` no basta con declararla: se comprueba que la
    prueba exista. Citar una prueba inexistente acreditaría una interpretación
    sin nada que la respalde — el mismo defecto que ya se cerró en la escalera
    de apropiación, que aquí habría vuelto a entrar por otra puerta."""
    valor = getattr(p, capa)
    if not valor:
        return False
    if capa == "prueba_del_verificador":
        # 2026-08-26 · deuda #1. Antes bastaba con que la prueba EXISTIERA, y eso
        # dejaba que cualquier prueba real acreditara cualquier verificador. Ahora
        # se exige además que la prueba **nombre al verificador que dice
        # respaldar**: la correspondencia se deriva del AST de la función, no se
        # declara. Sin verificador declarado no hay nada que corresponder, y la
        # capa se responde sólo si la prueba existe.
        from app.agents.apropiacion import existe_prueba, respalda
        if not existe_prueba(valor):
            return False
        return respalda(valor, p.verificador) if p.verificador else True
    return True


def peso_sostenible(p: Procedencia) -> tuple[str, list[str]]:
    """Qué puede afirmarse con esta procedencia, y qué capas lo impiden."""
    for peso in (HECHO_VERIFICABLE, HALLAZGO_DE_VERIFICABILIDAD):
        faltan = [c for c in EXIGE[peso] if not _responde(p, c)]
        if not faltan:
            return peso, []
    return NO_DETERMINABLE, [c for c in EXIGE[HALLAZGO_DE_VERIFICABILIDAD]
                             if not _responde(p, c)]


def sostener(enunciado: str, p: Procedencia,
             pretendido: str = HECHO_VERIFICABLE) -> Sostenida:
    """Devuelve la afirmación con el peso que su cadena permite.

    Si se pretendía más de lo que la procedencia sostiene, **se degrada y se
    dice desde dónde**. Callar la degradación sería peor que no tenerla: dejaría
    la afirmación con su apariencia original y sin su fundamento."""
    peso, faltan = peso_sostenible(p)
    orden = [NO_DETERMINABLE, HALLAZGO_DE_VERIFICABILIDAD, HECHO_VERIFICABLE]
    degradada = pretendido if orden.index(peso) < orden.index(pretendido) else ""
    if degradada:
        # Qué capas impidieron el peso PRETENDIDO, no el alcanzado. Decir «se
        # degradó» sin decir por qué es media respuesta, y la mitad que falta es
        # justamente la accionable.
        faltan = [c for c in EXIGE[pretendido] if not _responde(p, c)]
    return Sostenida(enunciado, peso, p, faltan, degradada)


def explicar(s: Sostenida) -> str:
    """Por qué esta afirmación pesa lo que pesa. En lenguaje de administración
    pública: esto puede llegar a una pantalla o a un expediente."""
    if s.peso == HECHO_VERIFICABLE:
        return (f"Verificado sobre {s.procedencia.sujeto}: la información "
                f"proviene de {s.procedencia.fuente}, se conserva el documento "
                f"obtenido y el criterio aplicado está respaldado por una prueba.")
    if s.peso == HALLAZGO_DE_VERIFICABILIDAD:
        base = (f"No fue posible acreditar el contenido: {s.procedencia.fuente} "
                f"respondió con estado «{s.procedencia.estado_adquisicion}». Se "
                f"registra la limitación, no una conclusión sobre "
                f"{s.procedencia.sujeto or 'el sujeto'}.")
        if s.faltan:
            base += (" Falta responder: " +
                     " ".join(PREGUNTA[c] for c in s.faltan))
        return base
    faltan = " ".join(PREGUNTA[c] for c in s.faltan)
    return (f"No determinable: la cadena de procedencia no responde — {faltan} "
            f"Se degrada la afirmación en lugar de completarla por inferencia.")


# ══════════════════════════════════════════════════════════════════════════════
# NATURALEZA DE VERIFICABILIDAD DEL OBJETO · ADR-052
# ══════════════════════════════════════════════════════════════════════════════
# Javo, 2026-08-20, mirando veinte años adelante:
#
# > *«Sin esa categoría, tu propio sistema empuja al municipio a dejar de hacer
# > lo que no puede documentar. Con ella, distingues el vacío que acusa del
# > vacío que no acusa.»*
#
# NO ES UN SEXTO ESTADO DE LA EVIDENCIA. Es una dimensión ANTERIOR que decide si
# la evidencia siquiera es evaluable. La secuencia sólo se recorre en un sentido:
#
#     naturaleza → evidencia → resultado
#
# y nunca al revés: QUIRA no puede observar un resultado y deducir desde allí la
# naturaleza del objeto. Esa sería la autoexoneración perfecta.
#
# LA INVARIANTE (colega, 2026-08-20):
#
#     **La ausencia de evidencia sólo puede evaluarse cuando existe una
#     expectativa normativa previa de materialización documental.**
#
# Y las tres proposiciones que NO se colapsan:
#
#     no encontré evidencia            ← habla del proceso de búsqueda
#     ≠ no existe evidencia esperable  ← habla del sujeto observado
#     ≠ el objeto no admite verificación documental bajo este instrumento
#                                      ← habla de la relación objeto/instrumento

VERIFICABLE_DOCUMENTALMENTE = "verificable_documentalmente"
NO_DOCUMENTAL = "no_documental"

# Quién puede declarar la naturaleza. La lista tiene UN elemento a propósito.
_AUTORIZADO_A_DECLARAR = ("corpus_normativo",)

# Resultado cuando el objeto no admite verificación documental. NO es un estado
# de la evidencia: es la constancia de que no había evidencia que esperar.
SIN_MATERIALIZACION_EXIGIBLE = "sin_materializacion_documental_exigible"


class NaturalezaUsurpada(RuntimeError):
    """Alguien que no es el corpus normativo intentó declarar un objeto como no
    verificable documentalmente. Si el motor pudiera hacerlo, se autoexoneraría
    de todo lo que no sabe medir; si pudiera el sujeto observado, sería la
    puerta trasera. La excepción existe para que el intento no pase callado."""


@dataclass(frozen=True)
class Naturaleza:
    """Si el objeto admite verificación documental bajo ESTE instrumento.

    `fundamento` no es decorativo: es lo que permite auditar la clasificación
    hasta el corpus. Sin él no se construye."""
    clase: str
    declarada_por: str
    fundamento: str

    def __post_init__(self):
        if self.clase == NO_DOCUMENTAL:
            if self.declarada_por not in _AUTORIZADO_A_DECLARAR:
                raise NaturalezaUsurpada(
                    f"«{self.declarada_por}» no puede declarar un objeto "
                    f"no_documental · sólo {_AUTORIZADO_A_DECLARAR[0]}")
            if not self.fundamento:
                raise NaturalezaUsurpada(
                    "no_documental sin fundamento en el corpus: sería una "
                    "exoneración sin causa declarada")

    @property
    def admite_evidencia(self) -> bool:
        return self.clase == VERIFICABLE_DOCUMENTALMENTE


def naturaleza_del_objeto(materializacion_esperada: str | None,
                          declarada_por: str = "corpus_normativo",
                          fundamento: str = "") -> Naturaleza:
    """La naturaleza se DERIVA de si el corpus declara materialización esperada.

    No es una etiqueta que alguien elija: si la norma declara qué debería
    existir, el objeto es verificable documentalmente. Si no la declara —y sólo
    el corpus puede no declararla— el objeto no tiene evidencia que esperar."""
    if materializacion_esperada:
        return Naturaleza(VERIFICABLE_DOCUMENTALMENTE, "corpus_normativo",
                          f"el corpus declara materialización esperada: "
                          f"{materializacion_esperada[:120]}")
    return Naturaleza(NO_DOCUMENTAL, declarada_por, fundamento)


def evaluar_ausencia(n: Naturaleza, hay_evidencia: bool) -> str:
    """Qué resultado produce la ausencia de evidencia, según la naturaleza.

    ⚠️ AQUÍ VIVE LA DEFENSA. Un motor que sólo mira `hay_evidencia` produce
    `sin_evidencia` en los dos casos, y con eso convierte una propiedad del
    objeto en una imputación al sujeto. La pregunta correcta va antes:
    **¿había una evidencia documental normativamente esperable?**"""
    if not n.admite_evidencia:
        # No se dice «buscamos y no encontramos». Se dice algo anterior.
        return SIN_MATERIALIZACION_EXIGIBLE
    return "con_evidencia" if hay_evidencia else "sin_evidencia"


# ── LA PROCEDENCIA VIAJA CON EL ARTEFACTO ─────────────────────────────────────
# 2026-08-25 · deuda #2 del registro d07. Formulación del colega:
#
#   *«La procedencia debe viajar con el artefacto hasta el límite en que el
#   artefacto pueda ser consumido independientemente de la cadena que lo
#   produjo.»*
#
# Hasta hoy, cuatro artefactos derivados de d07 no decían de quién eran. La
# cadena los protegía **indirectamente** —alterar la identidad invalida el sello
# y el gate SUJETO detiene la corrida—, pero un archivo copiado, adjuntado o
# ingerido por otro dominio sale de la cadena y pierde esa protección. Con 222
# GAD produciendo `inventario_documental.json`, la ambigüedad deja de ser
# teórica.
#
# ⚠️ LO QUE ESTE MECANISMO NO HACE: escribir el sujeto que el operador sabe. Lee
# el que la CADENA acreditó al producir esa etapa. Si la cadena no lo acreditó,
# **lo dice**; no lo rellena. Rellenarlo convertiría un artefacto sin
# procedencia en uno que aparenta tenerla — el error exacto que el módulo entero
# existe para impedir.
SUJETO_NO_ACREDITADO = "sujeto_no_acreditado_por_la_cadena"
ETAPA_NO_SELLADA = "etapa_no_sellada"


def de_generacion(etapa: str, sujeto: str, huella: str) -> dict:
    """Lo que un artefacto puede decir de su propio sujeto. **Determinista.**

    ⚠️ SIN MARCA DE TIEMPO, y es deliberado. Un derivado tiene que poder
    reconstruirse byte a byte desde su evidencia —`test_quira_reconstruye_sus_
    derivados_sin_ayuda` lo exige—, y un reloj dentro del archivo lo haría
    irreproducible para siempre. El **cuándo** pertenece al sello de la cadena;
    el **de quién**, al artefacto. Meter el reloj aquí costó un fallo real.

    Si no hay sujeto que acreditar, se dice; no se rellena. Escribir el sujeto
    que el operador recuerda convertiría un artefacto sin procedencia en uno
    que aparenta tenerla — el error exacto que este módulo existe para impedir."""
    if not sujeto or not huella:
        return {
            "etapa": etapa,
            "estado": SUJETO_NO_ACREDITADO,
            "por_que": "la etapa se produjo sin declarar sujeto",
            "no_significa": "que el artefacto no sea del sujeto observado; "
                            "significa que su cadena no lo acreditó, y eso no "
                            "se suple con lo que el operador recuerde",
        }
    return {"etapa": etapa, "sujeto": sujeto, "sujeto_huella": huella,
            "acreditada_por": "la cadena que produjo la etapa"}


SUJETO_DERIVADO_DE_LA_EVIDENCIA = "sujeto_derivado_de_la_evidencia"


def por_derivacion(etapa: str, sujeto: str, huella: str, fundamento: str,
                   comprobacion: str) -> dict:
    """Tercera vía de acreditación: **ni el sello lo declaró, ni el operador lo
    escribe — la evidencia misma lo contiene** (2026-08-26).

    Nació de un caso concreto: `descargas_indice.json` se produjo antes de que
    la cadena exigiera sujeto, así que su sello dice `None`. Quedaban tres
    salidas, y dos eran malas:

        re-ejecutar la etapa   → sustituye evidencia histórica por evidencia
                                 nueva para conseguir el estado que queremos ver
        escribir «130801»      → fabricar procedencia con lo que el operador sabe
        DERIVARLO              → leer lo que la evidencia ya contiene

    La diferencia con `de_generacion` está en quién responde: allí responde la
    cadena que lo produjo; aquí responde **el propio contenido del artefacto**, y
    por eso `comprobacion` es obligatoria y debe ser reproducible por un tercero.
    Sin ella esto sería declarar con otro nombre.

    ⚠️ NO sustituye al sello. Un artefacto derivado dice de quién es; no dice que
    su cadena lo acreditara. Son afirmaciones distintas y el campo las separa."""
    if not (fundamento and comprobacion):
        raise NaturalezaUsurpada(
            "derivar el sujeto sin fundamento ni comprobación reproducible es "
            "declararlo — que es exactamente lo que este módulo impide")
    return {"etapa": etapa, "sujeto": sujeto, "sujeto_huella": huella,
            "estado": SUJETO_DERIVADO_DE_LA_EVIDENCIA,
            "acreditada_por": "el contenido del propio artefacto",
            "fundamento": fundamento,
            "comprobacion": comprobacion,
            "no_significa": "que la cadena que lo produjo acreditara el sujeto; "
                            "su sello sigue diciendo que no lo hizo"}


def procedencia_del_artefacto(etapa: str, sello: dict) -> dict:
    """La misma declaración, cuando el sujeto se lee del sello en vez de
    recibirse. Para artefactos ya producidos, cuya cadena ya está sellada."""
    e = (sello or {}).get(etapa)
    if not isinstance(e, dict):
        return {"etapa": etapa, "estado": ETAPA_NO_SELLADA,
                "no_significa": "que el artefacto carezca de sujeto; significa "
                                "que ninguna cadena registró haberlo producido"}
    return de_generacion(etapa, e.get("sujeto"), e.get("sujeto_huella"))
