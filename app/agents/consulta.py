"""
app/agents/consulta.py — un dominio pregunta a otro por evidencia, no por verdad
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-30 · ADR-053 §6-bis). La idea es de Javo:

> *«Cuando el Agente de Rendición de Cuentas o el de Presupuesto necesite
> verificar un dato de Transparencia, no tiene que llamar a 5 scripts: le hace
> una consulta directa al Agente d07.»*

Y la condición que la hace viable, del colega:

> *«d02 → d01 puede significar «d01 tiene evidencia para sostener X respecto de
> este sujeto». **No debería significar «d01 dice que X es verdadero, por tanto
> d02 puede asumirlo»**. La primera conserva la genealogía; la segunda crea el
> atajo epistemológico que QUIRA existe para impedir.»*

CUÁNDO SE CONSTRUYÓ, y no antes: el ADR fijó que este contrato **no se diseña
hasta que haya dos dominios migrados con evidencia común**. Ese día llegó — d01
y d02 leen el mismo Gold Master y hay una prueba que lo fija
(`test_d01_y_d02_leen_el_mismo_gold_master`). Diseñarlo antes habría sido una
interfaz sin interlocutor.

ES DELIBERADAMENTE MÍNIMO. No hay clase base de agente, ni bus, ni router, ni
registro de capacidades. Sólo lo que el primer caso real necesita. Generalizar
antes de que el contrato sobreviva a su primer ataque sería construir alrededor
de algo no demostrado — el error que esta sesión midió cinco veces.

LO QUE VIAJA, Y LO QUE NO:

    ✅  la afirmación completa: sujeto · evidencia · motor · grado · faltantes
    ⛔  un booleano, un número, o «X es verdad»

**La unidad transferible no puede ser un valor.** Con el mismo Gold Master, dos
motores distintos pueden producir lecturas distintas —lo demostró `motor_sha256`
en d02—, así que un número desnudo no dice de dónde salió ni cuánto peso
soporta. Sólo una afirmación sustentada es transferible sin pérdida.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.agents.procedencia import (HECHO_VERIFICABLE, NO_DETERMINABLE,
                                    Sostenida)

# El orden de menor a mayor peso. Se usa para comprobar que cruzar la frontera
# no eleva lo afirmado; no es alfabético y no debe reordenarse.
_ORDEN = [NO_DETERMINABLE, "hallazgo_de_verificabilidad", HECHO_VERIFICABLE]


class GradoElevadoAlCruzar(RuntimeError):
    """Un dominio intentó consumir una afirmación ajena con más peso del que
    tenía. Cruzar la frontera no puede ser la forma de saltarse
    `test_ninguna_transformacion_puede_subir_el_grado`."""


class SujetoDistintoAlCruzar(RuntimeError):
    """La respuesta trata de un sujeto distinto al preguntado. Con 222 GAD, dos
    dominios podrían estar hablando de municipios distintos sin notarlo."""


@dataclass(frozen=True)
class Consulta:
    """Lo que un dominio le pregunta a otro.

    ⚠️ `pregunta` describe **qué evidencia se busca**, no una proposición a
    validar. «¿tienes evidencia sobre la cobertura de metas del POA?» es una
    consulta; «¿es cierto que el GAD cumplió?» no lo es."""
    solicitante: str
    consultado: str
    sujeto: str
    pregunta: str


@dataclass(frozen=True)
class Respuesta:
    """Lo que el dominio consultado devuelve. **Nunca un valor suelto.**

    Contiene la afirmación tal como el consultado puede sostenerla, con su
    identidad de motor —porque con la misma fuente, otra lógica puede leer
    distinto (hallazgo de d02)— y la constancia de qué se preguntó."""
    consulta: Consulta
    sostenida: Sostenida
    evidencia_sha256: str = ""
    motor_sha256: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    @property
    def grado(self) -> str:
        return self.sostenida.peso

    @property
    def faltantes(self) -> list[str]:
        return list(self.sostenida.faltan)

    def dice_la_verdad_de(self) -> str:
        """La formulación exacta de lo que esta respuesta significa.

        Existe para que nadie tenga que recordarla: la frase se genera con el
        grado real, y en ningún caso afirma que el enunciado sea cierto."""
        if self.grado == HECHO_VERIFICABLE:
            return (f"{self.consulta.consultado} tiene evidencia para sostener "
                    f"«{self.sostenida.enunciado}» respecto de "
                    f"{self.consulta.sujeto}")
        return (f"{self.consulta.consultado} NO puede sostener eso sobre "
                f"{self.consulta.sujeto}: falta {self.faltantes or 'evidencia'}")


def consumir(respuesta: Respuesta, como: str = HECHO_VERIFICABLE) -> Sostenida:
    """Lo que el dominio solicitante puede hacer con la respuesta.

    **Aquí vive la defensa de la frontera**, y por eso el cruce no es una simple
    llamada a función: se comprueba que el consumo no eleve el grado ni cambie
    el sujeto. Si lo intenta, no devuelve algo degradado — **lanza**: consumir
    mal una afirmación ajena no es un caso de uso, es un error de programa.

    Devuelve la MISMA afirmación del consultado, no una copia reinterpretada:
    d02 no obtiene una verdad propia, obtiene la de d01 con su genealogía."""
    if _ORDEN.index(como) > _ORDEN.index(respuesta.grado):
        raise GradoElevadoAlCruzar(
            f"{respuesta.consulta.solicitante} intenta consumir como «{como}» "
            f"lo que {respuesta.consulta.consultado} sólo sostiene como "
            f"«{respuesta.grado}». Cruzar la frontera no añade evidencia.")
    if respuesta.sostenida.procedencia.sujeto != respuesta.consulta.sujeto:
        raise SujetoDistintoAlCruzar(
            f"se preguntó por «{respuesta.consulta.sujeto}» y la afirmación es "
            f"sobre «{respuesta.sostenida.procedencia.sujeto}»")
    return respuesta.sostenida
