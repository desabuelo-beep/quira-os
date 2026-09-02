# -*- coding: utf-8 -*-
"""
tests/test_d02_agente.py — d02 como agente de dominio gobernado
════════════════════════════════════════════════════════════════════════════════
Segundo dominio migrado (ADR-053 §6), con el molde ya certificado en d01. Los
criterios del §5 son los mismos; lo que cambia es lo que d02 añade al molde.

LO QUE d02 APORTA, y d01 no necesitaba: **su motor DELEGA** en
`scripts/enrich_presupuesto.py` en vez de abrir el Excel. Eso parte la evidencia
en dos cosas que no son la misma:

    evidencia_sha256   el Gold Master · QUÉ DATOS se leyeron
    motor_sha256       el enricher    · QUÉ LÓGICA los leyó

Con el mismo Excel, un enricher distinto puede dar otro número — el propio
`enrich_presupuesto.py` corrigió en su día el ISP leído de la columna equivocada
(PCD-D02). Registrar sólo el Gold Master dejaría esa diferencia invisible.

Y AQUÍ APARECE EL EJE DEL §6-bis: d01 y d02 leen **el mismo Gold Master**. Es la
base de la consulta inter-dominio, y por primera vez es observable.

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
from app.agents.d02 import motor as M                     # noqa: E402


def _hay_motor() -> bool:
    return M._ENRICHER_PATH.exists()


# ── CRITERIO 3 · el verificador tiene quien lo respalde ───────────────────────
def test_d02_lee_las_capacidades_sin_recalcularlas(gold_master):
    """LA PRUEBA QUE ACREDITA A `d02.motor.leer_metricas`.

    `sostener_isp()` declara este nombre, y `respalda()` comprueba por AST que
    esta función **nombre al verificador**. Por eso lo llama de verdad.

    La propiedad: d02 **lee** lo que el enricher produce y no lo recalcula
    (Reglas de Oro 1 y 4). Su ISP es el del Gold Master, no uno derivado aquí."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    m = M.leer_metricas()
    assert m["status"] == "ok"
    assert m["naturaleza"] == "INMUTABLE"
    assert "NO recalculado" in m["fuente"]

    # Las cuatro capacidades y las señales SAT vienen del bloque, no de aquí.
    for clave in ("sostenibilidad_isp_pct", "absorcion_ti_pct",
                  "movilizacion_usd", "elegibilidad_pnd_pct"):
        assert clave in m, f"falta la capacidad «{clave}»"
    assert isinstance(m["sat_senales"], (list, dict))


# ── CRITERIOS 1 y 2 · identidad y procedencia ─────────────────────────────────
def test_d02_declara_sobre_quien_lee_y_sin_reloj(gold_master):
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    from app.agents import sujeto as S

    a = M.leer_metricas()["procedencia"]
    assert a.get("sujeto"), "la lectura no dice de quién es"
    assert a["sujeto_huella"] == S.huella()
    for reloj in ("sellado", "generado", "fecha", "timestamp"):
        assert reloj not in a, f"la procedencia guarda un reloj: «{reloj}»"


# ── LO QUE d02 AÑADE AL MOLDE ─────────────────────────────────────────────────
def test_la_evidencia_de_un_motor_que_delega_incluye_al_delegado(gold_master):
    """Si sólo se registrara el Gold Master, dos afirmaciones producidas por
    enrichers distintos —una con el bug del ISP y otra sin él— declararían la
    misma evidencia y darían números distintos. **La identidad de quien lee es
    parte de la procedencia de lo leído.**"""
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    m = M.leer_metricas()
    assert m["evidencia_sha256"], "falta la evidencia (qué datos)"
    assert m["motor_sha256"], "falta la identidad del motor (qué lógica)"
    assert m["evidencia_sha256"] != m["motor_sha256"], (
        "el Gold Master y el enricher no pueden tener la misma huella: son "
        "artefactos distintos y responden preguntas distintas")
    # Y la cadena de la afirmación nombra al motor, no sólo a la fuente.
    s = M.sostener_isp()
    assert m["motor_sha256"] in s.procedencia.fuente


def test_d02_sostiene_el_isp_con_su_cadena_completa(gold_master):
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    s = M.sostener_isp()
    assert s.peso == P.HECHO_VERIFICABLE, f"faltan: {s.faltan}"
    assert s.habla_del_sujeto is True


# ── EL EJE DEL §6-bis, POR PRIMERA VEZ OBSERVABLE ─────────────────────────────
def test_d01_y_d02_leen_el_mismo_gold_master():
    """LA BASE DE LA CONSULTA INTER-DOMINIO (ADR-053 §6-bis).

    El ADR sostenía —citando el `META_CATALOGO_AGENTES`— que d01, d02, d07 y d09
    miran la misma cédula presupuestaria, y que por eso cada uno derivando su
    propia lectura es la puerta a varias verdades sobre el mismo documento.

    **Aquí deja de ser una cita y pasa a ser una comprobación**: los dos primeros
    dominios migrados producen la MISMA evidencia. Ése es el hecho que hace
    posible que d02 pregunte a d07 en vez de re-derivar — y el que hará
    verificable el contrato cuando se diseñe."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    from app.agents.d01 import motor as M1

    if not M1._GM_DEFAULT.exists():
        pytest.skip("Gold Master no accesible")

    assert M.leer_metricas()["evidencia_sha256"] == \
        M1.leer_metricas()["evidencia_sha256"], (
        "d01 y d02 declaran evidencias distintas leyendo el mismo Gold Master: "
        "la consulta inter-dominio no podría apoyarse en evidencia común")
