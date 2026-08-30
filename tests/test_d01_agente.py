# -*- coding: utf-8 -*-
"""
tests/test_d01_agente.py — d01 como agente de dominio gobernado
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-26 · ADR-053, piloto). Javo selló el ADR-053 y ordenó
empezar por d01. Estas pruebas son los **criterios de entrada del §5**, aplicados
al primer dominio que migra.

Ninguno es un invento de esta migración: los cinco salieron de defectos reales
encontrados en d07 durante agosto, y por eso se le exigen a todo dominio que
entre después.

    1 · identidad huellada          ← el RUC no lo estaba (deuda 2-ter)
    2 · procedencia sin reloj       ← estamparla luego re-ejecutaba (deuda #2)
    3 · verificador con prueba      ← `evaluar` no tenía ninguna (deuda #1)
    4 · frontera de efectos         ← una prueba lanzó una corrida (deuda 4-ter)
    5 · equivalencia demostrada     ← antes de retirar nada

LO QUE d01 DEMUESTRA, y es el punto del piloto: que un dominio puede pasar de
**devolver números** a **sostener afirmaciones** sin tocar una sola fórmula. El
IPE sigue saliendo de `H16b`; lo que se añadió es la cadena que permite
responder «¿en qué se basa QUIRA para decir esto?».

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import procedencia as P                   # noqa: E402
from app.agents.d01 import motor as M                     # noqa: E402


def _hay_gold_master() -> bool:
    return M._GM_DEFAULT.exists()


# ── CRITERIO 3 · el verificador tiene quien lo respalde ───────────────────────
def test_d01_lee_el_ipe_sin_recalcularlo():
    """LA PRUEBA QUE ACREDITA A `d01.motor.leer_metricas`.

    `sostener_ipe()` declara este nombre en `prueba_del_verificador`, y desde
    que se cerró la deuda #1 eso ya no basta con declararlo: `respalda()`
    comprueba por AST que **esta función nombre al verificador**. Por eso llama
    a `leer_metricas` de verdad — si sólo lo mencionara en un comentario, la
    afirmación degradaría.

    Y la propiedad que verifica es la que importa (Regla de Oro 1 y 4): que el
    módulo **lee** H16b y **no recalcula** nada."""
    if not _hay_gold_master():
        pytest.skip("Gold Master no accesible en este entorno")

    m = M.leer_metricas()
    assert m["status"] == "ok", m.get("error")

    # Lee las tres celdas declaradas, y nada más.
    assert m["ipe_ejecutado"] is not None
    assert 0 <= float(m["ipe_ejecutado"]) <= 1, (
        "el IPE es una proporción: si sale de rango, no se está leyendo H16b!B15")
    assert m["naturaleza"] == "INMUTABLE"
    assert "NO recalculado" in m["fuente"], (
        "la salida debe declarar que se leyó, no que se calculó")

    # Y el valor NO se deriva aquí: dos lecturas dan lo mismo porque la fuente
    # es la misma, no porque haya una fórmula estable en este módulo.
    assert M.leer_metricas()["ipe_ejecutado"] == m["ipe_ejecutado"]


# ── CRITERIO 1 · identidad huellada ───────────────────────────────────────────
def test_d01_declara_sobre_quien_lee():
    """Un número sin sujeto no es una observación: con 222 GAD produciendo
    `ipe_ejecutado`, la ambigüedad deja de ser teórica (deuda #2)."""
    if not _hay_gold_master():
        pytest.skip("Gold Master no accesible en este entorno")
    from app.agents import sujeto as S

    proc = M.leer_metricas()["procedencia"]
    assert proc.get("sujeto"), "la lectura no dice de quién es"
    assert proc["sujeto_huella"] == S.huella(), (
        "la huella estampada no es la del perfil vigente")


# ── CRITERIO 2 · procedencia sin reloj ────────────────────────────────────────
def test_la_procedencia_de_d01_es_reproducible():
    """Sin marca de tiempo dentro del artefacto. Un reloj ahí lo volvería
    irreproducible para siempre: cada lectura daría algo distinto sin que nada
    hubiera cambiado. El *cuándo* pertenece a la cadena de la afirmación, no al
    artefacto (ADR-053 §5.2)."""
    if not _hay_gold_master():
        pytest.skip("Gold Master no accesible en este entorno")

    a = M.leer_metricas()["procedencia"]
    b = M.leer_metricas()["procedencia"]
    assert a == b, "dos lecturas idénticas dieron procedencias distintas"
    for reloj in ("sellado", "generado", "fecha", "timestamp", "leido_at"):
        assert reloj not in a, f"la procedencia guarda un reloj: «{reloj}»"


# ── EL PUNTO DEL PILOTO · de devolver números a sostener afirmaciones ─────────
def test_d01_sostiene_el_ipe_con_su_cadena_completa():
    """Lo que separa un agente gobernado de un lector de Excel.

    No se comprueba que el IPE «sea correcto» —eso lo calcula el Gold Master y
    aquí no se recalcula—, sino que **la afirmación sobre él pueda responder las
    siete capas** de ADR-042 §6-bis. Si alguna falta, degrada."""
    if not _hay_gold_master():
        pytest.skip("Gold Master no accesible en este entorno")

    s = M.sostener_ipe()
    assert s.peso == P.HECHO_VERIFICABLE, (
        f"la cadena de d01 no sostiene una afirmación sobre el sujeto; "
        f"faltan: {s.faltan}")
    assert s.habla_del_sujeto is True
    assert not s.faltan


def test_si_no_hay_motor_d01_no_afirma_sobre_el_sujeto():
    """EL CASO QUE MÁS IMPORTA, y el que este dominio comparte con d07: cuando
    el instrumento falla, **eso no es un hallazgo sobre el GAD**.

    Sin Gold Master no se puede decir «el IPE es bajo»: sólo «no fue posible
    leerlo». Es `ADR-042 §6` —«no existe» ≠ «no pude obtener»— aplicado al motor
    en vez de a un enlace."""
    s = M.sostener_ipe("/ruta/que/no/existe/gm.xlsx")
    assert s.peso != P.HECHO_VERIFICABLE, (
        "sin poder leer el motor, QUIRA no puede afirmar nada del sujeto")
    assert s.habla_del_sujeto is False


# ── CRITERIO 5 · equivalencia · no se retira nada sin demostrarla ─────────────
def test_la_migracion_no_cambio_un_solo_numero():
    """La migración añadió cadena, **no aritmética**. Se comprueba contra las
    celdas declaradas en el propio módulo: si alguien moviera la lectura a otra
    celda «mientras migra», esto lo detiene."""
    if not _hay_gold_master():
        pytest.skip("Gold Master no accesible en este entorno")
    import openpyxl

    wb = openpyxl.load_workbook(str(M._GM_DEFAULT), data_only=True, read_only=True)
    ws = wb[M._HOJA]
    m = M.leer_metricas()
    for celda, clave in ((M._CELDA_IPE, "ipe_ejecutado"),
                         (M._CELDA_COBERTURA, "cobertura_metas_poa"),
                         (M._CELDA_INV_VINCULADA, "inversion_vinculada_usd")):
        assert m[clave] == ws[celda].value, (
            f"«{clave}» ya no corresponde a {M._HOJA}!{celda}: la migración "
            f"cambió un número, y sólo debía añadir cadena")
