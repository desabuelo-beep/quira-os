# -*- coding: utf-8 -*-
"""
tests/test_naturaleza_verificabilidad.py — la prueba de estrés de ADR-052
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-20). El colega, al cerrar el debate del sexto estado:

> *«Si ADR-052 pasa esas cuatro pruebas, entonces tenemos algo mucho más sólido
> que una buena idea: tenemos una **invariante arquitectónica demostrada**. Y
> recién después tendría sentido decidir si se promociona algún día a CAPA 0.»*

Los cuatro casos son suyos. El cuarto es el que decide si la categoría sirve o
se convierte en la puerta trasera perfecta.

LA INVARIANTE QUE TODAS DEFIENDEN:

    **La ausencia de evidencia sólo puede evaluarse cuando existe una
    expectativa normativa previa de materialización documental.**

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import procedencia as P                    # noqa: E402


# ── CASO 1 · objeto inequívocamente documental ─────────────────────────────────
def test_caso1_un_objeto_documental_sigue_comportandose_como_antes():
    """Lo primero que hay que probar de una categoría nueva es que **no rompe
    lo que ya funcionaba**. El numeral 6 exige un conjunto de datos con catorce
    campos: su naturaleza es documental y su evidencia se evalúa igual que
    siempre."""
    n = P.naturaleza_del_objeto(
        "conjunto de datos del presupuesto, 14 campos, periodicidad mensual")
    assert n.clase == P.VERIFICABLE_DOCUMENTALMENTE
    assert n.admite_evidencia is True
    assert P.evaluar_ausencia(n, hay_evidencia=True) == "con_evidencia"
    assert P.evaluar_ausencia(n, hay_evidencia=False) == "sin_evidencia"
    # Y la clasificación se puede auditar hasta su causa.
    assert "el corpus declara materialización esperada" in n.fundamento


# ── CASO 2 · evidencia indirecta o parcial ─────────────────────────────────────
def test_caso2_la_evidencia_dificil_no_convierte_el_objeto_en_no_documental():
    """El riesgo inverso al que la categoría previene: que `no_documental` se
    use como salida cuando la evidencia es difícil, indirecta o incompleta.

    Un objeto cuya materialización esperada existe **sigue siendo documental**
    aunque la evidencia sea trabajosa de hallar. La dificultad de la búsqueda no
    es una propiedad del objeto."""
    n = P.naturaleza_del_objeto(
        "documento de reporte del servicio con ocho contenidos exigidos")
    assert n.clase == P.VERIFICABLE_DOCUMENTALMENTE
    # Aunque no se halle nada, el objeto NO cambia de naturaleza.
    assert P.evaluar_ausencia(n, hay_evidencia=False) == "sin_evidencia"
    assert n.admite_evidencia is True


# ── CASO 3 · objeto genuinamente no susceptible ────────────────────────────────
def test_caso3_un_objeto_sin_materializacion_esperada_no_produce_hallazgo():
    """El caso que justifica ADR-052. Cuando el corpus **no declara** una
    materialización esperada, la ausencia de documento no es un hallazgo: no
    había nada que esperar.

    El resultado NO es «sin evidencia» —eso acusaría al sujeto por un límite del
    instrumento— sino la constancia de que no existía materialización exigible."""
    n = P.naturaleza_del_objeto(
        None, declarada_por="corpus_normativo",
        fundamento="el instrumento no establece materialización documental "
                   "para el criterio interno de priorización")
    assert n.clase == P.NO_DOCUMENTAL
    assert n.admite_evidencia is False
    r = P.evaluar_ausencia(n, hay_evidencia=False)
    assert r == P.SIN_MATERIALIZACION_EXIGIBLE
    assert r != "sin_evidencia", (
        "convertir la naturaleza del objeto en ausencia de evidencia acusaría "
        "al sujeto por una propiedad del instrumento")


# ── CASO 4 · EL QUE DECIDE SI LA CATEGORÍA SIRVE ───────────────────────────────
def test_caso4_no_publicar_lo_debido_termina_en_sin_evidencia_jamas_en_no_documental():
    """LA PRUEBA MÁS IMPORTANTE DE LAS CUATRO (colega, 2026-08-20).

    Un sujeto que simplemente **no publicó lo que debía publicar** tiene que
    terminar en `sin_evidencia`. Si pudiera terminar en `no_documental`, la
    categoría dejaría de proteger al observado y pasaría a exonerarlo: sería la
    puerta trasera perfecta para todo incumplimiento.

    La defensa no está en la buena voluntad de quien clasifica. Está en el
    orden: la naturaleza se deriva de si el CORPUS declara materialización
    esperada, **antes** de mirar si hay evidencia. Que no haya documento no
    puede entrar en esa decisión."""
    # El numeral 10 exige planes y programas en ejecución: materialización
    # esperada declarada. El GAD no publicó nada en 2025.
    n = P.naturaleza_del_objeto("planes y programas de la entidad en ejecución")
    assert n.clase == P.VERIFICABLE_DOCUMENTALMENTE, (
        "la falta de publicación NO puede alterar la naturaleza del objeto")
    assert P.evaluar_ausencia(n, hay_evidencia=False) == "sin_evidencia"


# ── LA BARRERA · quién puede declarar ──────────────────────────────────────────
def test_ni_el_motor_ni_el_sujeto_pueden_declarar_no_documental():
    """Si el motor pudiera hacerlo, se autoexoneraría de todo lo que no sabe
    medir. Si pudiera el sujeto observado, sería la puerta trasera. Sólo el
    corpus normativo, y con fundamento."""
    for quien in ("motor_de_verificacion", "sujeto_observado", "operador",
                  "quira", "d07"):
        with pytest.raises(P.NaturalezaUsurpada):
            P.Naturaleza(P.NO_DOCUMENTAL, quien, "porque no lo encontramos")

    # Y ni siquiera el corpus puede declararlo sin decir por qué.
    with pytest.raises(P.NaturalezaUsurpada):
        P.Naturaleza(P.NO_DOCUMENTAL, "corpus_normativo", "")


def test_la_secuencia_solo_se_recorre_en_un_sentido():
    """ADR-052: `naturaleza → evidencia → resultado`, nunca al revés. El
    resultado no puede realimentar la naturaleza — eso permitiría reclasificar
    un objeto **después** de fallar la búsqueda, que es exactamente el error 2
    del ADR (exonerar al sujeto por un límite propio).

    Se prueba estructuralmente: `evaluar_ausencia` recibe la naturaleza ya
    construida y no puede modificarla, porque es `frozen`."""
    import dataclasses
    n = P.naturaleza_del_objeto("acta de sesión del Concejo")
    with pytest.raises(dataclasses.FrozenInstanceError):
        n.clase = P.NO_DOCUMENTAL          # type: ignore[misc]


def test_el_estado_del_objeto_y_el_de_la_evidencia_no_comparten_vocabulario():
    """ADR-052 §1. Si `no_documental` apareciera entre los estados de evidencia,
    volveríamos a la lista heterogénea que el ADR existe para separar. Los dos
    vocabularios deben ser disjuntos."""
    naturaleza = {P.VERIFICABLE_DOCUMENTALMENTE, P.NO_DOCUMENTAL}
    evidencia = {P.HECHO_VERIFICABLE, P.HALLAZGO_DE_VERIFICABILIDAD,
                 P.NO_DETERMINABLE}
    assert not (naturaleza & evidencia), (
        "la naturaleza del objeto y el estado de la evidencia no pueden "
        "compartir términos: son dimensiones distintas")
