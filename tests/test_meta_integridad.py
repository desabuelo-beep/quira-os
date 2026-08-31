# -*- coding: utf-8 -*-
"""
tests/test_meta_integridad.py — CAPA 0 · la capacidad de QUIRA de auditarse
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-31). El colega la puso antes que todas las demás capas:

> *«Antes de auditar QUIRA, auditamos la capacidad de QUIRA para auditarse a sí
> mismo. […] Esta capa es crítica: porque si falla, todo lo demás queda
> contaminado.»*

Y falla. En un solo día salieron tres diagnósticos falsos —«7 de 8 enrichers»,
«d08 tiene 3/3 SHA», «d02 no carga su RO»— y los tres eran el mismo error:

    afirmar sobre un universo que no se declaró.

De ahí salió la regla. Pero la regla **no se había aplicado a los inventarios
que la produjeron**: sólo `canon.py` declaraba universo, y aun él lo hacía por
fila y no sobre sí mismo. Un mecanismo de meta-integridad que se exceptúa a sí
mismo no es una regla, es una costumbre.

LO QUE ESTA CAPA FIJA:

    Ningún inventario puede afirmar sin declarar su universo,
    cómo lo descubrió, y qué queda fuera de su alcance.

Y se comprueba sobre la lista DERIVADA de inventarios — no sobre una escrita a
mano, que tendría exactamente el defecto que persigue.

Dylus Lab © 2026
"""
from __future__ import annotations

import importlib
import inspect
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_CAMPOS = ("que", "donde", "como", "hallados", "fuera_de_alcance")


def inventarios() -> list[tuple[str, object]]:
    """Los inventarios del sistema, DERIVADOS por introspección.

    Un inventario es una función pública de `app/agents/*.py` cuyo nombre
    empieza por `cobertura` y que no exige argumentos. Escribir la lista a mano
    haría que este mismo módulo afirmara sobre un universo no declarado — el
    defecto que existe para impedir."""
    salida = []
    for f in sorted((RAIZ / "app" / "agents").glob("*.py")):
        if f.name.startswith("_"):
            continue
        mod = importlib.import_module(f"app.agents.{f.stem}")
        for nombre, fn in vars(mod).items():
            if not nombre.startswith("cobertura") or not callable(fn):
                continue
            firma = inspect.signature(fn)
            if all(p.default is not inspect.Parameter.empty
                   for p in firma.parameters.values()):
                salida.append((f"{f.stem}.{nombre}", fn))
    return salida


def test_hay_inventarios_que_auditar():
    """Si la introspección deja de encontrarlos, las demás pruebas pasarían en
    vacío — el peor modo de fallo de una suite: verde por no mirar nada."""
    assert len(inventarios()) >= 3, (
        f"se esperaban al menos apropiacion, ejecucion y canon: {inventarios()}")


@pytest.mark.parametrize("nombre", [n for n, _ in inventarios()])
def test_todo_inventario_declara_su_universo(nombre):
    """LA REGLA DE LA CAPA 0, aplicada a todos por igual.

    No basta con decir qué encontró: hay que decir **dónde buscó, cómo, y qué
    no puede ver**. Sin eso, un resultado no es comprobable — nadie sabe sobre
    qué se hizo la afirmación, que es exactamente lo que pasó tres veces."""
    fn = dict(inventarios())[nombre]
    u = fn().get("universo")
    assert u, f"{nombre} afirma sin declarar sobre qué universo lo hace"
    for campo in _CAMPOS:
        assert campo in u, f"{nombre}: al universo le falta «{campo}»"
    assert u["fuera_de_alcance"], (
        f"{nombre} declara no tener límites. Ningún inventario de este sistema "
        f"lo consiguió todavía; declarar cero es no haberlos buscado")


@pytest.mark.parametrize("nombre", [n for n, _ in inventarios()])
def test_el_universo_declarado_coincide_con_lo_hallado(nombre):
    """El universo no puede ser prosa decorativa: `hallados` debe cuadrar con lo
    que el inventario efectivamente devuelve. Un universo que nadie contrasta se
    vuelve un adorno que envejece."""
    fn = dict(inventarios())[nombre]
    d = fn()
    u = d["universo"]
    assert isinstance(u["hallados"], int) and u["hallados"] >= 0
    filas = d.get("dominios")
    if filas is not None:
        assert u["hallados"] == len(filas), (
            f"{nombre}: declara {u['hallados']} y devuelve {len(filas)} filas")


def test_ningun_inventario_confunde_no_hallado_con_inexistente():
    """El error de fondo, buscado en la prosa de los propios inventarios.

    Cada uno debe distinguir explícitamente «no lo encontré» de «no existe» —
    el Principio Rector aplicado hacia adentro. `canon` lo hace con
    `no_comprobable`; `ejecucion` con `None` frente a `False`; `apropiacion` con
    `no_integrado` frente a `no_protegido`."""
    for nombre, fn in inventarios():
        mod = nombre.split(".")[0]
        fuente = (RAIZ / "app" / "agents" / f"{mod}.py").read_text(encoding="utf-8")
        assert "fuera_de_alcance" in fuente, f"{mod} no declara sus límites"
        assert any(marca in fuente for marca in
                   ("no_comprobable", "no_integrado", "incomprobable",
                    "no significa", "no_significa", "no es evidencia")), (
            f"{mod} no distingue en ninguna parte «no hallado» de «inexistente»")


def test_la_regla_alcanza_a_los_inventarios_futuros():
    """El trinquete de la capa. Un inventario nuevo queda sujeto a la regla por
    el solo hecho de llamarse `cobertura*` en `app/agents/` — nadie tiene que
    acordarse de añadirlo a una lista. Es la diferencia entre una regla y una
    costumbre, y es lo que faltaba: la regla nació de tres errores y no se había
    aplicado a los inventarios que la produjeron."""
    nombres = [n for n, _ in inventarios()]
    assert {"apropiacion.cobertura_de_la_plataforma",
            "ejecucion.cobertura",
            "canon.cobertura_canonica"} <= set(nombres), (
        f"la introspección dejó de alcanzar a alguno de los tres: {nombres}")
