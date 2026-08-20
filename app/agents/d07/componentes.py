"""
app/agents/d07/componentes.py — Cobertura material (etapa 6 del pipeline d07)
=========================================================================
POR QUÉ EXISTE (2026-08-17). Javo desarmó una medición que daba el presupuesto
por cumplido:

> *«En el mismo presupuesto la norma establece ingreso y egresos. El GAD solo
> reporta egresos. […] Sería algarete si Quira deja ese análisis tan básico.»*

Tenía razón, y la comprobación lo confirmó: los ocho períodos publicados del
numeral 6 traen **cero filas de ingreso**. El análisis anterior lo daba por
bueno porque contaba columnas —14 exigidas, 14 publicadas— sin mirar qué había
dentro. Existencia y estructura correctas, dimensión ausente.

QUÉ HACE. Comprueba que la evidencia cubra los `componentes` que el catálogo
canónico declara para cada conjunto. No inventa la lista: `CD-06` ya la traía
desde julio —Ingresos, Gastos, Financiamiento, Resultados_operativos,
Liquidacion— y nadie la había medido nunca.

CÓMO COMPRUEBA, y por qué esto no es conocimiento externo. La obligación del
numeral 6 dice, literalmente:

    «…especificando ingresos, gastos, financiamiento y resultados operativos
     **de conformidad con los clasificadores presupuestales**…»

Es la propia norma la que remite al clasificador. Por eso leer el primer dígito
del código de cuenta —1 y 2 ingresos, 3 y 9 financiamiento, 5 a 8 gastos— no es
traer un criterio de fuera: es aplicar el instrumento que la obligación manda
usar. Donde la norma NO remite a un instrumento, la comprobación se hace por
aparición literal del término, y si tampoco es concluyente el resultado queda
`no_determinable` — nunca `ausente`.

LOS TRES ESTADOS, y la razón de que sean tres:

    cubierto        la evidencia contiene la dimensión
    no_hallado      la evidencia NO la contiene — hallazgo de cobertura material
    no_determinable no hay forma verificable de decidirlo con esta evidencia

`no_determinable` existe para no convertir un límite del método en un cargo
contra el sujeto obligado. Un componente que no sabemos comprobar no es un
componente incumplido.

Y ESTO NO ES UN INCUMPLIMIENTO (colega, 2026-08-17): un componente `no_hallado`
es un **hallazgo de cobertura material verificable**. Escalarlo a incumplimiento
exige que la obligación esté asociada al campo, que sea inequívoca, que no haya
excepción aplicable ni recurso oficial alternativo. Eso lo decide el motor
normativo, no este módulo — que por eso no puntúa ni entra en SITA.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from . import reglas as R
from .evidencia import (RAIZ, _catalogo, _clave_numeral, _datos, _leer_tabla,
                        _norm, _tipo_archivo)

# ⚠️ EL CLASIFICADOR YA NO VIVE AQUÍ (2026-08-18 · ADR-051). Los grupos del
# Clasificador Presupuestario y la condición que habilita su uso los declara
# `RO-VII-002` y se consumen por `reglas.py`. Antes eran una constante de módulo:
# un criterio normativo escondido en el código, sin cadena ni fundamento citable.
# Si mañana el órgano rector reagrupa el clasificador, cambia la RO — no este
# archivo.

# Sinónimos admitidos SOLO para la comprobación literal. No traducen ni
# reinterpretan la norma: recogen cómo el mismo concepto aparece escrito en los
# encabezados publicados. `Gastos` y `EGRESOS` son la misma dimensión del
# clasificador, y exigir la palabra exacta habría marcado como ausente una
# dimensión que la evidencia sí trae.
_SINONIMOS = {
    "Ingresos": ("ingreso", "ingresos"),
    "Gastos": ("gasto", "gastos", "egreso", "egresos"),
    "Financiamiento": ("financiamiento", "financiero"),
    "Resultados_operativos": ("resultado operativo", "resultados operativos"),
    "Liquidacion": ("liquidacion", "liquidación"),
}


@dataclass
class Cobertura:
    cd_id: str
    anio: int
    mes: int
    por_componente: dict[str, dict] = field(default_factory=dict)

    @property
    def cubiertos(self) -> int:
        return sum(1 for v in self.por_componente.values()
                   if v["estado"] == "cubierto")

    @property
    def no_hallados(self) -> list[str]:
        return [k for k, v in self.por_componente.items()
                if v["estado"] == "no_hallado"]

    @property
    def medibles(self) -> int:
        return sum(1 for v in self.por_componente.values()
                   if v["estado"] != "no_determinable")


def _codigos_por_grupo(filas: list[list[str]]) -> dict[str, int]:
    """Cuenta filas por grupo del clasificador, leyendo el primer dígito del
    código de cuenta. Se toma la primera columna cuyo contenido sea mayoritariamente
    numérico de 3+ dígitos: es el código, aunque la cabecera lo llame `Cuenta`,
    `Código` o `Partida`."""
    if len(filas) < 2:
        return {}
    datos = filas[1:]
    mejor_col, mejor_n = None, 0
    for j in range(len(filas[0])):
        n = sum(1 for f in datos
                if len(f) > j and re.fullmatch(r"\d{3,}", (f[j] or "").strip()))
        if n > mejor_n:
            mejor_col, mejor_n = j, n
    if mejor_col is None or mejor_n < max(3, len(datos) // 4):
        return {}
    fuera: dict[str, int] = {}
    for f in datos:
        if len(f) > mejor_col:
            c = (f[mejor_col] or "").strip()
            if c[:1].isdigit():
                fuera[c[0]] = fuera.get(c[0], 0) + 1
    return fuera


def _aparece(termino: str, filas: list[list[str]]) -> bool:
    """Busca la dimensión en la cabecera y en los valores de texto."""
    claves = _SINONIMOS.get(termino, (termino.replace("_", " ").lower(),))
    for f in filas[:400]:
        for c in f:
            t = _norm(c)
            if t and any(k in t for k in claves):
                return True
    return False


def verificar_cobertura(cd_id: str, anio: int, mes: int) -> Cobertura:
    """Comprueba los componentes declarados por el canon contra la evidencia."""
    cat = _catalogo()["por_clave"].get(cd_id) or {}
    cob = Cobertura(cd_id=cd_id, anio=anio, mes=mes)

    # Las dimensiones las declara la REGLA OPERATIVA, no el módulo ni el catálogo.
    # Si la RO no enumera ninguna para este conjunto, no hay cobertura material que
    # medir — y eso NO es un incumplimiento: es que la obligación no desagrega.
    comps = R.dimensiones(cd_id)
    if not comps:
        return cob
    # CD-01 lista `1.1, 1.2, 1.3` como componentes en el catálogo, pero eso NO son
    # dimensiones materiales: son sub-numerales con periodicidad y campos propios.
    if all(re.fullmatch(r"\d+(\.\d+)?", c) for c in comps):
        return cob

    num = str(cat.get("numeral_ley") or "")
    clave = "Art.24" if num.startswith("Art") else num.replace("5+22", "5")
    d = _datos()
    conjuntos = [r for r in d["indice"]
                 if r.get("anio") == str(anio) and r.get("mes") == mes
                 and _clave_numeral(r.get("numeral", "")) == clave
                 and _tipo_archivo(r["archivo"]) == "conjunto_de_datos"
                 and r.get("ruta")]
    if not conjuntos:
        for c in comps:
            cob.por_componente[c] = {
                "estado": "no_determinable",
                "razon": "no se halló conjunto de datos publicado en el período",
            }
        return cob

    filas: list[list[str]] = []
    for r in conjuntos:
        filas.extend(_leer_tabla(RAIZ / r["ruta"]))

    # La vía del clasificador se habilita SÓLO si la obligación lo invoca, y quien
    # decide esa condición es la RO — no una comprobación improvisada aquí.
    obliga_clasificador = (
        R.instrumento_de_verificacion(cd_id) == "clasificador_presupuestario"
        and R.clasificador_habilitado(cat.get("obligacion_literal")))
    grupos_ro = R.grupos_clasificador()
    grupos = _codigos_por_grupo(filas) if obliga_clasificador else {}

    for c in comps:
        if obliga_clasificador and c in grupos_ro and grupos:
            esperados = grupos_ro[c]
            n = sum(grupos.get(g, 0) for g in esperados)
            cob.por_componente[c] = {
                "estado": "cubierto" if n else "no_hallado",
                "filas": n,
                "prueba": f"códigos del clasificador que empiezan en {'/'.join(esperados)}",
                "observado": dict(sorted(grupos.items())),
                "fundamento": "la obligación remite a los clasificadores presupuestales",
            }
            continue

        # ASIMETRÍA DELIBERADA. Hallar el término prueba que la dimensión está;
        # NO hallarlo **no prueba que falte**, porque la evidencia puede nombrarla
        # de otro modo. En el numeral 8 la búsqueda literal marcó como ausentes los
        # cinco componentes, y estaban todos: «Objetivos» se publica como `OBJETO
        # DEL PROCESO`, «Montos» como `MONTO DE LA ADJUDICACIÓN`, «Proveedores»
        # como `IDENTIFICACIÓN DEL CONTRATISTA`. Cinco hallazgos falsos de golpe.
        #
        # Por eso la ausencia sólo se declara cuando existe una regla objetiva —hoy,
        # el clasificador presupuestario que la propia obligación invoca—. Sin ella,
        # el resultado es `no_determinable`: un límite del método, no un cargo.
        if _aparece(c, filas):
            cob.por_componente[c] = {
                "estado": "cubierto",
                "prueba": "el término aparece en la cabecera o en los valores",
            }
        else:
            cob.por_componente[c] = {
                "estado": "no_determinable",
                "razon": ("la obligación no remite a un instrumento que permita "
                          "comprobarlo, y la evidencia puede nombrar la dimensión "
                          "de otro modo — no se declara ausencia sin regla objetiva"),
            }
    return cob
