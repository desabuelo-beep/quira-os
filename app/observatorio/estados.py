"""
QUIRA — Semántica de estados de captura  ·  `app/observatorio/estados.py`

Implementa ADR-042 §6. Es el único lugar donde vive la regla más importante del
Observatorio:

    «no existe evidencia» ≠ «no pude obtener evidencia» ≠ «el capturador falló»

Si un portal cambia su HTML y el conector deja de funcionar, QUIRA **no puede
convertir ese fallo técnico en una afirmación sobre la gestión pública**. Sería
exactamente el tipo de aseveración que este sistema existe para no hacer.

────────────────────────────────────────────────────────────────────────────────
POR QUÉ ESTO ES CÓDIGO Y NO UNA CONVENCIÓN
────────────────────────────────────────────────────────────────────────────────
La distinción es fácil de enunciar y fácil de perder. Un capturador que devuelve
una lista vacía «parece» que encontró que no hay nada publicado. Sin una guarda
explícita, ese vacío viaja hasta un informe y se lee como incumplimiento del
municipio. Por eso cada estado declara, en su definición, si afirma algo sobre
el sujeto observado y si puede publicarse — y `exigir_publicable()` corta el
paso antes de que un estado que no lo permite llegue a un producto.

Fundamento: Principio Rector de la Constitución Ontológica — *la ausencia de
evidencia es un RESULTADO de auditoría, nunca autorización para inferir hechos*.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Estado(str, Enum):
    """Los ocho estados de ADR-042 §6. Hereda de `str` para que persista y se
    compare como texto sin conversiones."""

    # ── Del proceso de captura ───────────────────────────────────────────────
    CAPTURADA = "capturada"
    PROCESADA = "procesada"
    PENDIENTE_VALIDACION = "pendiente_validacion"
    VALIDADA = "validada"

    # ── Hallazgo sobre el sujeto observado ───────────────────────────────────
    EVIDENCIA_AUSENTE = "evidencia_ausente"

    # ── Sobre la fuente o sobre nosotros — NUNCA sobre el sujeto ─────────────
    FUENTE_NO_DISPONIBLE = "fuente_no_disponible"
    CAPTURADOR_DEGRADADO = "capturador_degradado"
    ERROR_TECNICO = "error_tecnico"


@dataclass(frozen=True)
class Semantica:
    """Qué significa un estado, y qué se puede hacer con él."""

    etiqueta: str
    #: ¿Afirma algo sobre la gestión del sujeto observado?
    afirma_sobre_sujeto: bool
    #: ¿Puede llegar a un producto que se publica?
    publicable: bool
    #: De qué habla realmente, cuando no habla del sujeto.
    habla_de: str
    explicacion: str


_SEMANTICA: dict[Estado, Semantica] = {
    Estado.CAPTURADA: Semantica(
        etiqueta="Capturada",
        afirma_sobre_sujeto=False,
        publicable=False,
        habla_de="el proceso",
        explicacion="El artefacto se obtuvo de la fuente. Todavía no se ha "
                    "leído ni interpretado.",
    ),
    Estado.PROCESADA: Semantica(
        etiqueta="Procesada",
        afirma_sobre_sujeto=False,
        publicable=False,
        habla_de="el proceso",
        explicacion="Se extrajo y estructuró su contenido. Lo que diga todavía "
                    "es una propuesta de la máquina.",
    ),
    Estado.PENDIENTE_VALIDACION: Semantica(
        etiqueta="Pendiente de validación",
        afirma_sobre_sujeto=False,
        publicable=False,
        habla_de="el proceso",
        explicacion="La máquina propuso un hallazgo y falta que una persona lo "
                    "acredite contra la fuente. Nada se publica en este estado "
                    "(ADR-035: la IA propone, el humano valida).",
    ),
    Estado.VALIDADA: Semantica(
        etiqueta="Validada",
        afirma_sobre_sujeto=True,
        publicable=True,
        habla_de="el sujeto observado",
        explicacion="Una persona la acreditó contra la fuente. Es el único "
                    "estado en que un hallazgo positivo puede publicarse.",
    ),
    Estado.EVIDENCIA_AUSENTE: Semantica(
        etiqueta="Sin evidencia localizada",
        afirma_sobre_sujeto=True,
        publicable=True,
        habla_de="el sujeto observado",
        explicacion="La fuente respondió correctamente y no hay nada publicado. "
                    "Es un hallazgo verificable — y se enuncia como ausencia de "
                    "publicación registrada, NUNCA como incumplimiento: "
                    "calificar jurídicamente no le corresponde a QUIRA.",
    ),
    Estado.FUENTE_NO_DISPONIBLE: Semantica(
        etiqueta="Fuente no disponible",
        afirma_sobre_sujeto=False,
        publicable=False,
        habla_de="la fuente",
        explicacion="La fuente no respondió. Habla del portal, no del "
                    "municipio: un servidor caído no dice nada sobre si la "
                    "entidad publicó o no.",
    ),
    Estado.CAPTURADOR_DEGRADADO: Semantica(
        etiqueta="Capturador degradado",
        afirma_sobre_sujeto=False,
        publicable=False,
        habla_de="nuestro instrumento",
        explicacion="La fuente respondió pero su formato cambió y el capturador "
                    "ya no lo entiende. Habla de NUESTRO instrumento. Confundir "
                    "esto con ausencia de evidencia produciría una acusación a "
                    "partir de un selector roto.",
    ),
    Estado.ERROR_TECNICO: Semantica(
        etiqueta="Error técnico",
        afirma_sobre_sujeto=False,
        publicable=False,
        habla_de="nosotros",
        explicacion="Falló algo de nuestro lado. No dice nada de nadie más.",
    ),
}

#: Estados que cierran el ciclo de una corrida.
TERMINALES = frozenset({
    Estado.VALIDADA, Estado.EVIDENCIA_AUSENTE,
    Estado.FUENTE_NO_DISPONIBLE, Estado.CAPTURADOR_DEGRADADO,
    Estado.ERROR_TECNICO,
})

#: Los tres que se confunden entre sí, y que este módulo existe para separar.
NO_ES_HALLAZGO = frozenset({
    Estado.FUENTE_NO_DISPONIBLE, Estado.CAPTURADOR_DEGRADADO,
    Estado.ERROR_TECNICO,
})


class EstadoNoPublicable(Exception):
    """Se intentó llevar a un producto un estado que no lo admite."""


def semantica(estado: Estado | str) -> Semantica:
    """Semántica de un estado. Un valor desconocido es un error técnico: ante la
    duda NO se afirma nada sobre el sujeto observado."""
    try:
        return _SEMANTICA[Estado(estado)]
    except (ValueError, KeyError):
        return _SEMANTICA[Estado.ERROR_TECNICO]


def afirma_sobre_sujeto(estado: Estado | str) -> bool:
    """¿Este estado dice algo sobre la gestión observada?"""
    return semantica(estado).afirma_sobre_sujeto


def es_publicable(estado: Estado | str) -> bool:
    """¿Puede este estado llegar a un producto que se publica?"""
    return semantica(estado).publicable


def exigir_publicable(estado: Estado | str, contexto: str = "") -> None:
    """Corta el paso antes de publicar. Llamar en la frontera de cada producto.

    Es la guarda que impide que un capturador roto se convierta en un hallazgo
    sobre un municipio. Levanta en vez de devolver `False` a propósito: un
    booleano ignorado sigue publicando; una excepción, no."""
    s = semantica(estado)
    if not s.publicable:
        donde = f" ({contexto})" if contexto else ""
        raise EstadoNoPublicable(
            f"«{s.etiqueta}» no puede publicarse{donde}: habla de "
            f"{s.habla_de}, no del sujeto observado. {s.explicacion}")


def clasificar(*, fuente_respondio: bool, formato_reconocido: bool,
               hay_contenido: bool, fallo_interno: bool = False) -> Estado:
    """Traduce lo que ocurrió durante una captura al estado que corresponde.

    Existe para que la decisión NO quede en manos de cada capturador. El error
    típico es devolver «no hay evidencia» cuando en realidad la fuente no
    respondió o el formato cambió — y ese error produce una afirmación falsa
    sobre un municipio.

    El orden de las preguntas importa y es deliberado:
      1 · ¿falló algo nuestro?        → error técnico
      2 · ¿respondió la fuente?       → si no, la fuente no está disponible
      3 · ¿entendemos el formato?     → si no, nuestro capturador está degradado
      4 · ¿hay contenido?             → recién aquí se puede hablar del sujeto

    Solo se llega al paso 4 cuando los tres anteriores están descartados. Es lo
    que hace que `EVIDENCIA_AUSENTE` sea un hallazgo y no una suposición."""
    if fallo_interno:
        return Estado.ERROR_TECNICO
    if not fuente_respondio:
        return Estado.FUENTE_NO_DISPONIBLE
    if not formato_reconocido:
        return Estado.CAPTURADOR_DEGRADADO
    if not hay_contenido:
        return Estado.EVIDENCIA_AUSENTE
    return Estado.CAPTURADA


def color(estado: Estado | str) -> str:
    """Color del sistema visual para un estado.

    Sigue la doctrina del sistema: lo que habla del instrumento es instrumental
    —no alarma—, y la ausencia se muestra como ausencia. Solo lo que requiere
    atención lleva el ocre; nada lleva verde, porque no hay color de «bien»."""
    from utils.css_tokens import C
    e = Estado(estado) if not isinstance(estado, Estado) else estado
    if e is Estado.VALIDADA:
        return C.ACENTO
    if e is Estado.EVIDENCIA_AUSENTE:
        return C.OCRE
    if e in NO_ES_HALLAZGO:
        return C.V_TX3          # habla de nosotros o de la fuente: instrumental
    return C.V_TX2              # en curso


def resumen() -> list[tuple[str, Semantica]]:
    """Los ocho estados en orden canónico — para leyendas y documentación."""
    return [(e.value, _SEMANTICA[e]) for e in Estado]
