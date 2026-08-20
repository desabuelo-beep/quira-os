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
        from app.agents.apropiacion import existe_prueba
        return existe_prueba(valor)
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
