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


def test_el_hallazgo_de_agregacion_no_se_pierde():
    """★ Lo que 008-R descubrió, y que reformula todo lo dicho sobre cobertura.

        El Gold Master no seleccionó 25 metas de 66: AGREGÓ las 66 en 25.

    `SC-I-N-01` —«Agua potable: cobertura 39.25%→42.38%; calidad 100%;
    infraestructura BUENA 22.74%→41.64%»— contiene TRES metas del PDOT, y sus
    cifras lo prueban: viajan intactas del documento a la celda del motor.

    ⚠️ Si esto se pierde, vuelve la aritmética falsa: `66−25=41 excluidas`,
    «cobertura del 37,88 %», «las 41 metas fuera». Ninguna de esas frases
    describe nada — no hay partición que hacer."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "AGREGA, no selecciona" in txt, (
        "desapareció el hallazgo central de 008-R. Sin él vuelve la lectura de "
        "subconjunto, que es falsa")
    assert "la resta no describe nada" in txt, (
        "se perdió la consecuencia: `66 − 25 = 41` no identifica metas "
        "excluidas, porque la relación es N:1 y no una partición")
    assert "39.25" in txt, (
        "desapareció el caso que lo demuestra. El hallazgo sin su evidencia "
        "vuelve a ser una afirmación que hay que creer")


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
