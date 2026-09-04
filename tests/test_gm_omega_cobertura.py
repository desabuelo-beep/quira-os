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


def test_el_criterio_de_seleccion_se_declara_con_su_autoridad():
    """DOC-018 · la justificación del universo no justifica su selección.

    Durante meses `ADR-036` pareció cerrar la cuestión: ratificaba usar 25 metas
    como universo operacional v1. Pero justificar **usar un subconjunto** no es
    justificar **que ese subconjunto sea representativo**, y el criterio sólo se
    supo cuando Javo lo declaró: **mayor monto económico, para fines de tesis**.

    ⚠️ Y LA FORMA IMPORTA TANTO COMO EL CONTENIDO: no se dedujo mirando las 25
    —eso habría sido `DOC-009`— sino que lo declaró **quien lo aplicó**. Es lo
    que a `E_i` le sigue faltando: una fuente con autoridad sobre la regla, no
    una explicación que encaje con los datos.

    Esta prueba vigila que el criterio siga declarado CON SU FUENTE. Un criterio
    sin autoría vuelve a ser una explicación plausible, que es lo contrario."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "monto económico más amplio" in txt, (
        "desapareció el criterio de selección de las 25 metas. Sin él, 008 "
        "vuelve a no poder decir qué representa el 27,4582 %")
    assert "Javo, 2026-09-03" in txt, (
        "el criterio perdió su autoría. Sin fuente con autoridad deja de ser "
        "una regla declarada y vuelve a ser una explicación que encaja — que es "
        "exactamente lo que DOC-009 prohíbe tratar como hallazgo")
    assert "del gasto sí · del mandato no" in txt, (
        "se perdió la consecuencia del criterio: la muestra representa el gasto, "
        "no el PDOT como mandato. Es lo que acota qué puede afirmar el ICPI v1")


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


def test_la_procedencia_separa_los_tres_atributos_que_no_son_lo_mismo():
    """⚠️ ESTA PRUEBA NACIÓ MAL Y SE CORRIGIÓ. Su primera versión exigía que el
    catálogo dijera `OFICIAL`, porque esta auditoría había aplicado al `.xlsx`
    una aclaración de Javo que se refería al documento del portal. Eran archivos
    distintos.

    La cadena real, reconstruida a la tercera:

        Portal GAD · Transparencia (LOTAIP) · sección PDOT
          └── PDF publicado                    ← ORIGINAL OFICIAL
                └── Word · conversión propia
                      └── Excel · tabulación   ← este catálogo

    Y de ahí la propiedad que sí hay que vigilar: **tres atributos que no deben
    colapsarse en la palabra «oficial»** —

        PUBLICADO en el portal   ·   VÁLIDO como insumo   ·   FUENTE CANÓNICA

    El `.xlsx` es válido (SHA verificado), no publicado, y no es la fuente
    canónica de metas. Las tres cosas a la vez, sin contradicción."""
    if not _PDOT.exists():
        pytest.skip("no está el catálogo del PDOT")
    proc = json.loads(_PDOT.read_text(encoding="utf-8")).get("_procedencia", {})

    assert proc.get("publicado_en_portal") is False, (
        "el catálogo dejó de declarar que el .xlsx NO está publicado. Sin ese "
        "campo se vuelve a confundir con el PDF del portal, que sí lo está")
    assert proc.get("documento_publicado"), (
        "no se declara CUÁL es el documento publicado. Decir que éste no lo es "
        "sin nombrar el que sí, deja la cadena a medias")
    assert "fuente_canonica_de_metas" in proc, (
        "desapareció la distinción entre el insumo tabulado y la fuente "
        "canónica de metas (el PDOT aprobado)")
    for historico in ("_caracter_anterior", "_caracter_v2_erroneo"):
        assert historico in proc, (
            f"se perdió `{historico}`. Una procedencia corregida conserva lo "
            f"que decía antes —incluidas las correcciones equivocadas— o nadie "
            f"puede auditar cómo se llegó a la etiqueta actual (DOC-015)")
    assert "TRES atributos" in proc.get("verificabilidad", ""), (
        "la verificabilidad dejó de explicar por qué es parcial. La razón no es "
        "la oficialidad: es que lo leído no es la fuente canónica (escalón 7)")
