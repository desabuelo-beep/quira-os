# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_reconciliacion.py — GM-Ω-ICPI-008-R
════════════════════════════════════════════════════════════════════════════════
008-R salió a producir la partición `66 → 25 + 41` y descubrió que esa partición
no existe: **el motor agrega, no selecciona.** El objetivo no se alcanzó, y el
por qué vale más que la tabla que se esperaba.

Estas pruebas fijan las dos cosas que no pueden perderse: el hallazgo, y la
disciplina que lo hizo posible —no forzar coincidencias—.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_RECONCILIACION_008R.md"
_CAT = RAIZ / "data" / "pdot" / "catalogo_reconciliacion_66.json"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "reconciliacion_metas.py"


def test_el_hallazgo_N1_no_se_generaliza_a_regla():
    """DOC-019 · un caso demostrado no autoriza la regla general.

    008-R encontró un caso inequívoco: `SC-I-N-01` —«Agua potable: cobertura
    39.25%→42.38%; calidad 100%; infraestructura 22.74%→41.64%»— lleva las
    cifras de TRES metas del PDOT.

    ⚠️ Y ESTA DIRECCIÓN CONCLUYÓ «el motor agregó las 66 en 25». Era demasiado
    fuerte, y los propios números del informe lo desmentían: 19 de las 25 no
    tienen componentes atribuidas. No se puede afirmar las dos cosas.

    Es `DOC-009` en su forma más difícil de ver, porque la señal era fuerte y la
    conclusión, elegante. Esta prueba vigila las dos mitades: que el hallazgo
    siga —con su evidencia— y que la generalización NO vuelva."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "39.25" in txt, (
        "desapareció el caso que demuestra la correspondencia N:1. Un hallazgo "
        "sin su evidencia vuelve a ser una afirmación que hay que creer")
    assert "DEMOSTRADO" in txt and "NO DEMOSTRADO" in txt, (
        "se perdió la separación entre lo demostrado —existe un caso N:1— y lo "
        "no demostrado —que las 66 estén distribuidas entre las 25—")
    assert "`25 = agregación de 66` | **tampoco demostrado**" in txt, (
        "volvió la generalización: afirmar que las 25 agregan las 66 contradice "
        "que 19 de ellas no tengan componentes atribuidas. Un caso no es la "
        "regla (DOC-019)")
    assert "RECONCILIACIÓN PARCIAL" in txt, (
        "008-R se declaró cerrada. La correspondencia exhaustiva 66↔25 sigue "
        "sin reconciliar, y darla por cerrada dejaría un hueco creyendo que no "
        "lo hay")


def test_el_catalogo_de_correspondencias_es_insumo_no_canon():
    """DOC-020 · la correspondencia es un DATO del modelo, no una inferencia.

    008-R escribió un algoritmo que empareja por cifras y acertó en un caso
    comprobable. **El riesgo es justamente ése**: que un método que funciona a
    veces se convierta en autoridad. Si el motor puede «descubrir» que dos metas
    corresponden, la trazabilidad deja de ser un dato y pasa a ser una hipótesis
    con formato de tabla.

    ⚠️ Se vigila el propio artefacto de esta auditoría: su catálogo produce
    CANDIDATOS, y ninguno es canónico hasta que una persona lo confirme contra
    el documento — las reconciliadas incluidas."""
    if not _CAT.exists():
        pytest.skip("aún no se generó el catálogo")
    meta = json.loads(_CAT.read_text(encoding="utf-8")).get("_meta", {})
    assert meta.get("estatus", "").startswith("INSUMO DE TRABAJO"), (
        "el catálogo dejó de declararse insumo. Un archivo de correspondencias "
        "sin ese sello acaba citándose como canon, y entonces una inferencia "
        "algorítmica se vuelve trazabilidad oficial")
    assert "doc_020" in meta, (
        "desapareció la advertencia de DOC-020 del propio catálogo")
    txt = _DOC.read_text(encoding="utf-8")
    assert "RELACIÓN_DE_CORRESPONDENCIA" in txt, (
        "se perdió el contrato: la correspondencia debe existir como dato "
        "declarado con su tipo de relación y su evidencia")
    assert "No se recalcula el ICPI" in txt, (
        "desapareció la regla de hierro. Recalcular antes de saber qué es `i` "
        "daría un número impecable y epistemológicamente inútil")


def test_correspondencia_y_operacion_no_se_mezclan():
    """La distinción fina del asesor, y puede ser todo el asunto en SC-I-N-01:

        una relación N:1 NO implica que exista una operación matemática de
        agregación.

    Tres metas documentales pueden corresponder a una unidad operacional **sin
    que sus valores se hayan agregado numéricamente** — porque se tomó una como
    representante, porque se midió un solo aspecto, o porque la unidad se
    definió antes que las metas.

    ⚠️ Que la celda MENCIONE tres cifras no prueba que las tres ENTREN en el
    cálculo. Responder ambas preguntas juntas daría una respuesta elegante y
    probablemente falsa."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no implica** que exista una operación" in txt, (
        "se perdió la separación entre correspondencia (011-B) y operación "
        "matemática (011-C). Mezclarlas convierte una relación estructural en "
        "una afirmación sobre el cálculo, que es otra cosa")
    assert "011-B" in txt and "011-C" in txt


def test_la_unidad_de_analisis_queda_planteada_a_011():
    """Lo que 008-R le entrega a `011`, y que no estaba en su lista.

    Si una unidad del motor puede corresponder a varias metas documentales,
    entonces hay algo que toda la auditoría venía dando por sabido:

        ¿qué es exactamente `i` en `J_i = P_i × R_i × V_i × E_i × T_i × C_i`?

    Se ha hablado de `i` como «una meta del PDOT». Si puede ser un agregado,
    cambia la lectura de cada factor y del denominador — y por tanto de qué
    objeto afirma congruencia el 27,4582 %.

    ⚠️ No dice que la fórmula esté mal. Dice que **la unidad de análisis es una
    pregunta previa a la del álgebra**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "¿Qué es exactamente `i`" in txt, (
        "desapareció la pregunta de la unidad de análisis. Sin ella, 011 "
        "dictaminaría sobre el constructo sin saber sobre qué objeto se calcula")
    assert "unidad de análisis" in txt


def test_la_reconciliacion_no_fuerza_coincidencias():
    """La regla de 008-R, medida sobre el artefacto.

    Un catálogo con ambigüedades declaradas es utilizable; uno con
    coincidencias inventadas, no. Afinar más el algoritmo habría empezado a
    producir las segundas — y por eso se paró donde se paró.

    ⚠️ SE VERIFICA QUE LAS AMBIGUAS SIGAN EXISTIENDO. Un catálogo que un día
    aparezca sin ninguna no será mejor: será sospechoso, salvo que alguien las
    haya resuelto **a mano contra el documento** y lo haya declarado."""
    if not _CAT.exists():
        pytest.skip("aún no se generó el catálogo de reconciliación")
    cat = json.loads(_CAT.read_text(encoding="utf-8"))
    filas = cat.get("filas", [])
    assert filas, "el catálogo de reconciliación quedó vacío"

    amb = [f for f in filas if f["estado"] == "AMBIGUA"]
    assert amb, (
        "el catálogo ya no tiene ambigüedades. Si se resolvieron a mano contra "
        "el documento, hay que declararlo en `_meta` y esta prueba debe pasar a "
        "verificar ESO; si las resolvió el algoritmo, se están forzando "
        "coincidencias y el catálogo dejó de ser confiable")
    for f in filas:
        assert f["estado"] in ("RECONCILIADA", "AMBIGUA", "NO_RECONCILIADA"), (
            f"estado desconocido en {f.get('meta', '')[:40]}")
        if f["estado"] == "RECONCILIADA":
            assert f["id_icpi"] and f["tipo"] in ("literal", "cifras", "semántica"), (
                "una fila reconciliada sin ID o sin tipo de señal: no se puede "
                "auditar cómo se estableció esa correspondencia")


def test_la_cadena_de_procedencia_esta_completa_y_con_sha():
    """Un artefacto no se clasifica por un atributo: se clasifica por su cadena.

    Costó TRES rectificaciones llegar aquí —«no oficial» → «OFICIAL» aplicado al
    archivo equivocado → la cadena real—, porque se preguntaba por atributos
    sueltos en vez de reconstruir el recorrido entero:

        PDF del portal → Word (conversión propia) → Excel (tabulación)

    ⚠️ Los tres SHA son lo que convierte esa cadena en verificable en vez de
    recordada."""
    if not _CAT.exists():
        pytest.skip("aún no se generó el catálogo")
    cad = json.loads(_CAT.read_text(encoding="utf-8")).get("cadena_procedencia", {})
    for eslabon in ("pdf_portal", "word_conversion", "xlsx_tabulacion"):
        assert eslabon in cad, f"falta el eslabón `{eslabon}` de la cadena"
        assert cad[eslabon].get("sha256"), (
            f"`{eslabon}` no trae SHA256: sin él la cadena se afirma, no se "
            f"verifica")
    txt = _DOC.read_text(encoding="utf-8")
    assert "se clasifica por su cadena" in txt, (
        "desapareció la lección de las tres rectificaciones, que es lo que "
        "evita repetirlas")


def test_v2_hereda_el_requisito_de_conservar_el_texto_de_las_metas():
    """La consecuencia práctica que 008-R venía a preparar.

    El Gold Master guarda un resumen agregado, no el texto de las metas del
    PDOT. Por eso ninguna reconciliación posterior puede ser automática — y por
    eso ésta llegó hasta donde llegó.

    Si v2 se construye sin arreglar eso, el universo ampliado nacerá con la
    misma deuda de trazabilidad que esta auditoría acaba de medir, en un sistema
    cuyo objeto **es** la trazabilidad."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "texto íntegro de cada meta documental" in txt, (
        "se perdió el requisito para v2: cada meta operacional debe conservar "
        "el texto y la localización de las metas que agrega")
    assert "no conserva el texto de las metas" in txt
