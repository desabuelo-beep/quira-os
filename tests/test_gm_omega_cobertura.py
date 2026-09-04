# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_cobertura.py — GM-Ω-ICPI-008 · la cobertura
════════════════════════════════════════════════════════════════════════════════
008 preguntó qué universo mide el ICPI, y lo primero que encontró fue que
`ADR-036` ya lo había decidido y ratificado. Es la tercera vez en esta auditoría
que se empieza a investigar algo ya resuelto —`E_i`, el mapa índice→dominio, la
cobertura—, así que la regla deja de ser una lección y pasa a tener custodio.

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

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_COBERTURA_008.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "cobertura_icpi.py"
_ADR = RAIZ / "docs" / "adr" / "ADR-036_Universo_Operacional_Metas.md"
_PDOT = RAIZ / "data" / "pdot" / "metas_plurianual_extraccion.json"


def test_el_analisis_no_toca_el_gold_master_ni_la_cifra_madre():
    """008 observa. La cifra madre sigue congelada por la regla `GM-Ω-ICPI-000`
    durante todo el diagnóstico, y ampliar de 25 a 66 sería una versión
    metodológica nueva (`ADR-036 §2/§4`), no una cura."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert fuente.count("load_workbook") == fuente.count("read_only=True"), (
        "hay una apertura del Gold Master que no es de sólo lectura")
    assert ".save(" not in fuente, "el análisis intenta escribir en el Excel"
    txt = _DOC.read_text(encoding="utf-8")
    assert "27,4582 % sigue congelada" in txt or "27,4582" in txt


def test_el_alcance_del_ICPI_se_declara_donde_el_ADR_lo_exige():
    """⚠️ DOC-017 · la consecuencia práctica de un ADR necesita custodio.

    `ADR-036 §1`: «Toda publicación de d01/d03 debe declararlo: *se mide contra
    las 25 metas estratégicas del modelo*». Nadie había verificado nunca si eso
    se cumple, y no se cumple: **0 superficies visibles**.

    ⚠️ FIJA EL ESTADO, NO LO APRUEBA. Mientras la obligación siga incumplida
    esta prueba verifica que el hallazgo está donde decimos; el día que alguien
    publique el alcance, saltará — y entonces se invierte para vigilar que no
    desaparezca."""
    from scripts.gm_omega.cobertura_icpi import declaracion_de_alcance
    a = declaracion_de_alcance()
    assert not a["visible"], (
        f"el alcance ya se declara en {a['visible']}. Si se curó, hay que "
        f"INVERTIR esta prueba —que exija su presencia— y actualizar D-001. Una "
        f"obligación cumplida sin custodio vuelve a perderse en la siguiente "
        f"refactorización")
    assert _ADR.exists(), "desapareció el ADR que fija la obligación"
    assert "debe declararlo" in _ADR.read_text(encoding="utf-8"), (
        "el ADR-036 dejó de exigir la declaración de alcance: si la obligación "
        "se retiró, esta prueba y D-001 tienen que reflejarlo")


def test_el_criterio_de_seleccion_de_las_25_sigue_sin_documentarse():
    """El hueco que `ADR-036` no cierra y que 008 aísla.

    El ADR verifica que las 25 **existen** en el PDOT —«ninguna inventada»— y
    eso responde «son legítimas». **No responde «por qué éstas».** Y de eso
    depende si la muestra es representativa: mayor presupuesto, competencia
    crítica, o disponibilidad de evidencia producen el mismo conjunto y
    significados completamente distintos del 27,4582 %.

    ⚠️ Es la misma forma que `E_i`: valores conocidos, regla generadora no
    reconstruible. Y por eso 008 NO declara sesgo — sin criterio, leer la
    composición como sesgo sería `DOC-009`."""
    from scripts.gm_omega.cobertura_icpi import criterio_declarado
    hallados = criterio_declarado()
    assert not hallados, (
        f"aparecieron documentos que declaran el criterio de selección de las "
        f"25 metas: {hallados}. Si es real, 008 puede pronunciarse sobre el "
        f"sesgo y hay que rehacer su §4; verificar primero que hablan de las "
        f"METAS y no de otra selección —GATE-007 ya produjo ese falso positivo")
    txt = _DOC.read_text(encoding="utf-8")
    assert "NO declara sesgo" in txt or "no se puede afirmar que la muestra sea" in txt


def test_ocho_reconoce_que_el_ADR_ya_habia_decidido():
    """La constancia que más vale de 008, y que no es un hallazgo técnico.

    Este frente empezó a investigar algo que el canon ya había resuelto. Es la
    tercera vez —`E_i`, el mapa índice→dominio, la cobertura— y por eso la
    lección deja de ser una anécdota y pasa a tener custodio: **buscar donde
    debía estar, antes de declarar nada**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "ya estaba respondido" in txt.lower(), (
        "desapareció la constancia de que ADR-036 había decidido esto antes. "
        "Sin ella, 008 se lee como si hubiera descubierto el universo "
        "operacional, y lo que hizo fue medirlo")
    assert "ADR-036" in txt and "RATIFICADO" in txt


def test_el_denominador_declara_que_es_oficial_y_por_que():
    """La corrección de Javo, fijada: **«no remitido formalmente» ≠ «no
    oficial»**.

    El PDOT se obtuvo del portal del GAD. `LOTAIP Art. 7` obliga a publicarlo y
    el canon sostiene que el portal es materialización de una obligación —
    degradar lo publicado a «no oficial» anularía toda la transparencia activa,
    incluida `V_LOTAIP`, que puntúa 1,0 por «documento en URL pública».

    ⚠️ Y la reserva se conserva por OTRA razón: lo leído es el Plan Plurianual
    `.xlsx` y la fuente canónica de metas es el PDOT aprobado. Escalón 7: **lo
    leído ≠ la fuente**. Oficial y provisional a la vez, sin contradicción."""
    if not _PDOT.exists():
        pytest.skip("no está el catálogo del PDOT")
    proc = json.loads(_PDOT.read_text(encoding="utf-8")).get("_procedencia", {})
    assert proc.get("caracter", "").startswith("OFICIAL"), (
        "el catálogo volvió a clasificar como «no oficial» un documento "
        "obtenido del portal del GAD. Esa etiqueta confunde el CANAL con el "
        "CARÁCTER del documento, y aplicada en serie anularía la transparencia "
        "activa que el propio modelo puntúa")
    assert "_caracter_anterior" in proc, (
        "se perdió la etiqueta anterior. La corrección de una procedencia "
        "conserva lo que decía antes (DOC-015): sin eso, nadie puede auditar "
        "que la clasificación cambió ni por qué")
    assert "escalón 7" in proc.get("verificabilidad", "").lower(), (
        "la reserva sobre el denominador dejó de decir su razón real: no es la "
        "oficialidad, es que lo leído fue el Plan Plurianual y no el PDOT "
        "aprobado")
