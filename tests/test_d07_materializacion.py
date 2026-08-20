# -*- coding: utf-8 -*-
"""
tests/test_d07_materializacion.py — obligación ↔ evidencia
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-20). Javo corrigió la ontología del dominio:

> *«El universo de información de transparencia activa del GAD no debe
> interpretarse como una colección arbitraria de archivos, sino como una
> materialización documental de obligaciones normativas y procedimentales.»*

Estas pruebas defienden esa estructura y, sobre todo, la regla que impide
convertir una ausencia en una acusación.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents.d07 import materializacion as M              # noqa: E402


def test_la_ausencia_de_artefacto_no_es_incumplimiento():
    """LA REGLA CENTRAL (colega, 2026-08-20):

    > *«La ausencia de un artefacto no constituye por sí misma incumplimiento;
    > constituye una ausencia de evidencia respecto de una obligación cuya
    > materialización esperada debe haber sido previamente determinada por el
    > corpus normativo y procedimental aplicable.»*

    Ningún estado de esta matriz puede afirmar incumplimiento: eso es
    calificación jurídica y corresponde al motor normativo, no al instrumento
    que observa. Es el mismo error que el dominio acaba de corregir con los
    enlaces —«no lo encontré» convertido en «no existe»— aplicado ahora a los
    documentos."""
    prohibidos = {"incumple", "incumplimiento", "infringe", "viola", "ilegal",
                  "no_cumple", "sancion"}
    estados = {M.MATERIALIZADA, M.PARCIAL, M.SIN_EVIDENCIA, M.NO_DETERMINABLE}
    for e in estados:
        assert not (set(e.lower().split("_")) & prohibidos), (
            f"el estado «{e}» califica jurídicamente y no debería")
    # Y el estado de ausencia debe nombrarse por lo que es: falta de evidencia.
    assert M.SIN_EVIDENCIA == "sin_evidencia_hallada"


def test_la_unidad_es_la_relacion_no_el_archivo_ni_el_numeral():
    """La matriz se construye desde la obligación, con la evidencia entrando
    como materialización — no al revés. Cada relación debe poder responder qué
    exige la norma, con qué procedencia normativa, y qué se encontró."""
    obligaciones = M.cargar_obligaciones()
    assert len(obligaciones) >= 25, "faltan obligaciones de la vara"
    # El art. 24 —donde la norma pide las actas del Concejo— no es un numeral
    # del art. 19 y vive aparte en la vara: omitirlo dejaba 48 artefactos sin
    # obligación identificada teniendo la suya, y de las más importantes.
    assert any(o.numeral == "Art.24" for o in obligaciones)
    for o in obligaciones:
        assert o.texto, f"la obligación {o.numeral} llegó sin su texto normativo"


def test_el_numeral_5_22_es_un_solo_conjunto_en_el_portal():
    """FALSO HALLAZGO EVITADO (2026-08-20). El mapeo devolvía `5` para los
    numerales 5 y 22, pero el portal los publica juntos bajo `Numeral 5-22`. La
    primera corrida declaró «numeral 5 sin evidencia hallada» habiendo **30
    artefactos publicados**: un hallazgo falso producido por el instrumento."""
    assert M._clave("5") == "5-22"
    assert M._clave("22") == "5-22"
    assert M._clave("Art.24") == "Art."
    assert M._clave("6") == "6", "los demás numerales no se remapean"


def test_lo_que_no_se_asocia_a_una_obligacion_no_se_interpreta():
    """Un artefacto sin obligación identificada puede significar cuatro cosas
    distintas —que no hallamos la relación normativa, que hay una obligación
    transversal, que es materialización complementaria, o que no es exigido— y
    **sólo la cuarta** sería «el GAD publica lo que nadie le pide».

    Presentar esa lectura como la única sería inventar un hallazgo. El módulo
    declara la limitación del análisis y se detiene ahí."""
    fuente = (RAIZ / "app" / "agents" / "d07" /
              "materializacion.py").read_text(encoding="utf-8")
    i = fuente.index("def artefactos_sin_obligacion")
    bloque = fuente[i:i + 1400]
    assert "limitación del análisis" in bloque
    assert "no se presume" in bloque or "se determina, no" in bloque


def test_una_obligacion_sin_periodicidad_declarada_no_la_inventa():
    """La Guía no declara periodicidad para todos los numerales. Donde no la
    declara, exigirla sería fabricar la obligación — y el dominio ya cometió ese
    error una vez, aplicando «12 meses» a conjuntos trimestrales."""
    obligaciones = M.cargar_obligaciones()
    sin_declarar = [o for o in obligaciones if not o.periodicidad_declarada]
    assert sin_declarar, (
        "la vara declara periodicidad para TODOS los numerales; verificar, "
        "porque la Guía no lo hace")
    for o in sin_declarar:
        assert o.periodicidad.get("estado") in (None, "no_sustentado")


def test_el_numeral_22_existe_como_obligacion_propia():
    """LO QUE JAVO ENCONTRÓ (2026-08-20), y era un defecto del extractor.

    > *«El 5-22 son dos cosas que se piden: por un lado el formulario para
    > acceso a la información pública y por otro la evidencia de los servicios
    > brindados. Y así cada literal tiene su propia forma, reglamentada.»*

    La vara **no tenía el numeral 22**. El extractor fusionaba el bloque porque
    la guía lo desarrolla junto al 5, con un solo conjunto de datos — y un
    comentario mío afirmaba que separarlos «inventaría dos exigencias donde la
    norma pone una». La norma pone dos, y la guía las transcribe por separado:

        [293] Números 5 y 22                          ← encabezado plural
        [296] «Los servicios que brinda la entidad…»   (ibidem, número 5)
        [297] «Formularios y formatos de solicitudes…» (ibidem, número 22)

    Fusionar la publicación NO fusiona la obligación. Mientras estuvieron
    fundidas era **imposible** sostener el hallazgo que la norma permite:
    «publica los servicios pero no los formularios»."""
    obligaciones = {o.numeral: o for o in M.cargar_obligaciones()}
    assert "22" in obligaciones, "el numeral 22 desapareció de la vara otra vez"
    o22 = obligaciones["22"]
    assert "ormulario" in o22.texto, (
        "el numeral 22 debe traer su obligación literal, no la del 5")
    assert "ervicio" in obligaciones["5"].texto
    assert o22.texto != obligaciones["5"].texto, "son dos obligaciones distintas"


def test_los_campos_del_bloque_compartido_no_se_reparten_por_nuestra_cuenta():
    """La guía asigna SEIS campos al bloque 5-22 y **no dice cuáles
    corresponden a cada numeral**. Repartirlos por criterio propio sería
    completar la norma — precisamente lo que la vara existe para no hacer.

    Se declara el estado y se deja el reparto como lo que es: un silencio del
    corpus, no una decisión de QUIRA."""
    obligaciones = {o.numeral: o for o in M.cargar_obligaciones()}
    for num in ("5", "22"):
        d = obligaciones[num]
        assert d.campos_exigidos, f"el numeral {num} llegó sin campos"
    # Ambos heredan los mismos campos del bloque, y eso se declara.
    assert (obligaciones["5"].campos_exigidos ==
            obligaciones["22"].campos_exigidos)
