"""
app/agents/sujeto.py — quién está siendo observado
==================================================
POR QUÉ EXISTE (2026-08-19 · OBS-032). El colega fijó el criterio rector:

> *«No debemos construir d07 para Montecristi. Debemos utilizar Montecristi para
> construir el patrón que permita ejecutar d07 sobre 222 GAD.»*

La medición mostró lo contrario: la identidad del sujeto —su código en la API de
la Defensoría, su dominio web, su nombre— estaba escrita a mano en **once puntos
de código**, repartidos por siete archivos. Aplicar la cadena al GAD 002 exigía
editarlos todos y acordarse de los once. Multiplicado por 222, eso no es un
pipeline: es un procedimiento manual con apariencia de software.

    instrumento que contiene al sujeto   →  una medición
    instrumento que recibe al sujeto     →  un instrumento

ES TRANSVERSAL, NO DE d07. Vive en `app/agents/` y no en `app/agents/d07/`
porque todo dominio observa al mismo sujeto: d01 mira su PDOT, d02 su
presupuesto, d07 su portal de transparencia. Una identidad por dominio sería el
mismo error, repetido siete veces.

QUÉ NO HACE. No decide qué observar ni cómo: sólo dice **a quién**. Los criterios
siguen viniendo de la RO, y la evidencia de la fuente.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
_SUJETOS = RAIZ / "data" / "sujetos"

# Mientras sólo haya un sujeto declarado, éste es el que asume la cadena. No es
# un valor por defecto escondido: está aquí, en un solo sitio, y se ve.
POR_DEFECTO = "130801"


class SujetoNoDeclarado(RuntimeError):
    """Pedir un sujeto que no tiene perfil es un error, no un vacío que se
    rellena. Inventar la identidad de un GAD sería exactamente lo que la Regla
    de Oro 3 prohíbe con los datos: afirmar sin fuente."""


@lru_cache(maxsize=None)
def cargar(codigo: str | None = None) -> dict:
    """El perfil del sujeto observado. Única puerta de lectura."""
    codigo = str(codigo or POR_DEFECTO)
    p = _SUJETOS / f"{codigo}.json"
    if not p.exists():
        declarados = sorted(f.stem for f in _SUJETOS.glob("*.json"))
        raise SujetoNoDeclarado(
            f"no hay perfil para «{codigo}» · declarados: {declarados or 'ninguno'}")
    return json.loads(p.read_text(encoding="utf-8"))


def entidad_dpe(codigo: str | None = None) -> int:
    """Identificador del sujeto en la API de la Defensoría del Pueblo.

    Estaba escrito dos veces a mano y con tipos distintos —`{937: ...}` en un
    script, `["937"]` en otro—, que es la forma en que una identidad duplicada
    empieza a divergir."""
    return int(cargar(codigo)["identidad_en_fuentes"]["dpe_entidad_id"])


def dominio_web(codigo: str | None = None) -> str:
    """Dominio institucional del sujeto."""
    return cargar(codigo)["identidad_en_fuentes"]["dominio_web"]


def dominios(codigo: str | None = None) -> list[str]:
    """Dominio principal y sus servicios asociados.

    Se devuelven juntos porque el enlace que el GAD publica puede apuntar al
    portal o a su Nextcloud, y ambos son publicación del mismo sujeto: tratar
    uno como ajeno convertiría contenido propio en ausencia."""
    ident = cargar(codigo)["identidad_en_fuentes"]
    return [ident["dominio_web"], *ident.get("dominios_asociados", [])]


def nombre(codigo: str | None = None) -> str:
    return cargar(codigo)["nombre"]


def nombre_corto(codigo: str | None = None) -> str:
    return cargar(codigo)["nombre_corto"]


def huella(codigo: str | None = None) -> str:
    """Huella criptográfica de la IDENTIDAD del sujeto, no de su nombre.

    ⚠️ POR QUÉ EXISTE (2026-08-19 · ataque end-to-end). El gate `SUJETO`
    comparaba una etiqueta legible —«130801 Montecristi»—, y eso dejaba una
    puerta abierta: cambiar `dpe_entidad_id` de 937 a 999 **no alteraba la
    etiqueta**. El sistema seguía midiendo con evidencia de la entidad 937
    mientras el perfil declaraba observar la 999, con todos los gates en verde y
    la corrida COMPLETED.

    Una etiqueta identifica para leer; una huella identifica para verificar. Se
    huella todo aquello con lo que se va a la fuente: si cambia cualquier parte
    de la identidad, la evidencia anterior deja de corresponder."""
    import hashlib
    import json as _json
    d = cargar(codigo)
    identidad = {"codigo": str(codigo or POR_DEFECTO),
                 **d["identidad_en_fuentes"]}
    crudo = _json.dumps(identidad, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(crudo.encode()).hexdigest()


def declarados() -> list[str]:
    """Los sujetos que QUIRA sabe observar hoy. Con 222 GAD, esta lista es el
    inventario real de alcance — no una aspiración del roadmap."""
    return sorted(f.stem for f in _SUJETOS.glob("*.json"))
