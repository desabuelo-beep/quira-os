"""
app/agents/brn_lector.py — la frontera verificable entre el catálogo y quien lo use
================================================================================
D-003 · último tramo. El colega fijó qué NO debe ser esto:

> *«No debe ser un simple `json.load()`. Debe ser un lector verificable […] El
> lector no gobierna nada: verifica antes de entregar.»*

Y la frontera que no puede romperse, declarada antes de dejar escribir código:

> *«el puente no debe hacer que el Gold Master consulte la BRN para decidir sus
> valores. La BRN explica y traza la dependencia; no gobierna el motor.»*

    CANON → COMPILADOR → gm_snapshot.json → **LECTOR** → CONSUMIDOR

TRES PREGUNTAS DISTINTAS, que este módulo se niega a colapsar:

    ¿qué dicen las piezas?                    derivado del catálogo
    ¿el compilado corresponde al canon de hoy? verificable por `canon_sha256`
    ¿Javo validó este compilado?               verificable por el sello externo

EL CANDADO. Un sello no vale para un catálogo que no validó, y un catálogo no
vale para un canon que ya cambió:

    canon actual == canon_sha256 del catálogo ?
      NO  → catálogo DESACTUALIZADO · el sello anterior NO aplica
      SÍ  → ¿hay sello?
              no          → no_consta
              sí, otro hash → NO aplica (valida otra compilación)
              sí, mismo hash → validado · quién · cuándo

Así **una recompilación no renueva el sello**: el compilador produce el
artefacto, y sólo el acto de gobernanza que ya existe puede acreditarlo.

Y EL SEGUNDO CANDADO, igual de importante: **el sello no promociona nada**. Una
CNO en `propuesta` sigue en `propuesta` aunque el catálogo esté validado. El
sello significa *«Javo validó este catálogo compilado contra este canon»*, no
*«Javo validó cada decisión contenida en cada pieza»*.

Dylus Lab © 2026
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
_SNAP = RAIZ / "data" / "gm_snapshot.json"
_SELLO = RAIZ / "docs" / "registry" / "sello_catalogo_brn.json"
_BRN_DIR = RAIZ / "docs" / "brn"

# Estados del catálogo respecto del canon.
AL_DIA = "al_dia"
DESACTUALIZADO = "desactualizado"
NO_DETERMINABLE = "no_determinable"

# Estados del sello.
VALIDADO = "validado"
NO_CONSTA = "no_consta"
NO_APLICA = "no_aplica_a_este_catalogo"


class CatalogoNoVerificable(RuntimeError):
    """El catálogo no está o no puede leerse. **Se levanta en vez de devolver un
    catálogo vacío**: un lector que ante un archivo roto entrega «cero reglas»
    convierte un fallo de lectura en una afirmación sobre el canon."""


@dataclass(frozen=True)
class Sello:
    """El acto de gobierno, y si aplica a lo que se está leyendo."""
    estado: str
    validado_por: str = ""
    fecha: str = ""
    canon_sha256_validado: str = ""
    por_que: str = ""

    @property
    def acredita(self) -> bool:
        return self.estado == VALIDADO


@dataclass(frozen=True)
class ReglaLeida:
    """Una RO con **su estado y su procedencia**, no un valor suelto.

    El consumidor recibe el grado que la pieza tiene y no puede elevarlo: es la
    misma regla de la consulta inter-dominio —*el grado no sube al cruzar la
    frontera*— aplicada al puente compilado."""
    id: str
    variable: str
    umbral_vigente: object
    vigencia_operativa: list = field(default_factory=list)
    opera_en: str = ""
    estado_pieza: str = ""          # vigente | propuesta — NUNCA lo altera el sello
    deriva_de: str = ""             # la CNO de la que cuelga
    cadena_normativa: list = field(default_factory=list)
    catalogo_al_dia: bool = False
    sello: Sello | None = None

    @property
    def es_consumible_como_vigente(self) -> bool:
        """Sólo si la pieza está vigente, el catálogo al día y el sello acredita.
        Las tres condiciones, y ninguna suple a otra."""
        return (self.estado_pieza == "vigente" and self.catalogo_al_dia
                and self.sello is not None and self.sello.acredita)


@dataclass(frozen=True)
class CatalogoBRN:
    estado: str
    canon_sha256_declarado: str
    canon_sha256_actual: str
    integridad_cno: tuple
    integridad_ro: tuple
    sello: Sello
    reglas: dict
    por_que: str = ""

    @property
    def canon_coincide(self) -> bool:
        return self.canon_sha256_declarado == self.canon_sha256_actual


def canon_sha_actual() -> str:
    """La huella del canon de HOY, recalculada — nunca leída del artefacto.

    Si se confiara en el `canon_sha256` que el propio catálogo declara, un
    catálogo alterado se acreditaría a sí mismo. El lector rehace la cuenta.

    ⚠️ NORMALIZA LOS FINALES DE LÍNEA, igual que el compilador y por la misma
    razón: `read_bytes()` crudo hacía que la huella dependiera del sistema de
    archivos —CRLF en Windows, LF en el runner—, y el mismo canon daba dos
    resultados. Lo destapó el primer CI real: allí el catálogo se declaraba
    desactualizado y d02 dejaba de consumir su umbral.

    Las dos cuentas TIENEN que hacerse igual. Si el compilador normaliza y el
    lector no, nunca coinciden y el catálogo queda desactualizado para siempre
    — que es exactamente lo que pasó entre el arreglo del compilador y éste."""
    h = hashlib.sha256()
    for f in sorted(_BRN_DIR.glob("*.yaml")):
        h.update(f.name.encode())
        h.update(f.read_bytes().replace(b"\r\n", b"\n"))
    return h.hexdigest()[:16]


def _leer_sello(canon_del_catalogo: str) -> Sello:
    """El sello externo, y si aplica a ESTE catálogo."""
    if not _SELLO.exists():
        return Sello(NO_CONSTA, por_que="no hay artefacto de sello")
    try:
        s = json.loads(_SELLO.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return Sello(NO_CONSTA, por_que="el sello no es legible")
    firmado = str(s.get("canon_sha256_validado", ""))
    if firmado != canon_del_catalogo:
        return Sello(NO_APLICA, validado_por=s.get("validado_por", ""),
                     fecha=s.get("fecha_validacion", ""),
                     canon_sha256_validado=firmado,
                     por_que=f"el sello valida el canon {firmado} y este catálogo "
                             f"declara {canon_del_catalogo}: acredita otra compilación")
    return Sello(s.get("estado", NO_CONSTA), s.get("validado_por", ""),
                 s.get("fecha_validacion", ""), firmado)


def leer() -> CatalogoBRN:
    """Carga, verifica y entrega. En ese orden — nunca entrega sin verificar."""
    if not _SNAP.exists():
        raise CatalogoNoVerificable(f"no está el snapshot: {_SNAP}")
    try:
        brn = json.loads(_SNAP.read_text(encoding="utf-8")).get("brn_cno")
    except (json.JSONDecodeError, OSError) as e:
        raise CatalogoNoVerificable(f"snapshot ilegible: {type(e).__name__}") from e
    if not isinstance(brn, dict) or "cno" not in brn:
        raise CatalogoNoVerificable("el snapshot no contiene un catálogo BRN")

    declarado = str(brn.get("canon_sha256", ""))
    actual = canon_sha_actual()
    sello = _leer_sello(declarado)

    # INTEGRIDAD RECALCULADA, no leída. El campo `integridad_compilacion` es una
    # afirmación del compilador; el lector la comprueba contra el contenido.
    cnos = brn["cno"]
    integras = sum(1 for c in cnos if c.get("cadena_integra"))
    ros = [r for c in cnos for r in c.get("deriva_ro", [])]

    reglas = {}
    for c in cnos:
        for r in c.get("deriva_ro", []):
            reglas[r["id"]] = ReglaLeida(
                id=r["id"], variable=r.get("variable", ""),
                umbral_vigente=r.get("umbral_vigente"),
                vigencia_operativa=r.get("vigencia_operativa") or [],
                opera_en=r.get("opera_en", ""),
                # ⚠️ EL ESTADO DE LA PIEZA VIENE DE LA PIEZA. El sello del
                # catálogo no lo toca: validar el acto de compilar no valida
                # cada decisión compilada.
                estado_pieza=r.get("estado", ""),
                deriva_de=c.get("id", ""),
                cadena_normativa=c.get("cadena") or [],
                catalogo_al_dia=(declarado == actual),
                sello=sello)

    estado = (NO_DETERMINABLE if not declarado
              else AL_DIA if declarado == actual else DESACTUALIZADO)
    por_que = ("" if estado == AL_DIA else
               "el catálogo no declara su canon de entrada" if estado == NO_DETERMINABLE
               else f"compilado sobre el canon {declarado}; el actual es {actual}")
    return CatalogoBRN(estado, declarado, actual, (integras, len(cnos)),
                       (len(ros), len(ros)), sello, reglas, por_que)


def regla(ro_id: str) -> ReglaLeida | None:
    """Una RO concreta, con su estado y su procedencia. `None` si no está —
    y `None` significa «no está en este catálogo», no «no existe»."""
    return leer().reglas.get(ro_id)
