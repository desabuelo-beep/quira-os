# -*- coding: utf-8 -*-
"""
tests/test_escalon4_evidencia.py — la evidencia debe ser la que se leyó
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-30). El mismo hueco apareció TRES veces —d07, d01 y la
frontera d01↔d02— y ahí dejó de ser una imperfección local. El colega:

> *«Ya no es una imperfección localizada de un dominio. Es una propiedad del
> contrato de evidencia. […] No necesitamos que QUIRA sepa que una evidencia
> existe. Necesitamos que pueda demostrar que es la evidencia que realmente
> leyó.»*

    declarado → existente → corresponde → CORRESPONDE AL ARTEFACTO → exitoso
                └── ya estaba ──┘         └──── esto se cierra aquí ────┘

LA PROPOSICIÓN QUE SE CIERRA:

> Una evidencia sólo puede sostener una afirmación si el hash declarado
> corresponde al artefacto que efectivamente fue leído por el verificador.

⚠️ Y SE CIERRA CON UN RESIDUO DECLARADO, que estas pruebas miden: la
verificación sólo actúa cuando la procedencia **declara el artefacto**. Quien no
lo declare sigue acreditando por existencia, como antes. Exigirlo a todos habría
roto toda `Procedencia` viva del sistema; el residuo queda medido y con
trinquete, no escondido.

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
from app.agents import sujeto as S                        # noqa: E402
from app.agents.d01 import motor as D1                    # noqa: E402

_BASE = dict(fuente="Gold Master", captura="2026-08-30",
             estado_adquisicion="leido_del_motor",
             verificador="d01.motor.leer_metricas",
             prueba_del_verificador="test_d01_lee_el_ipe_sin_recalcularlo")


def _base():
    return {**_BASE, "sujeto": f"{S.POR_DEFECTO} {S.nombre_corto()}"}


def _hay_gm() -> bool:
    return D1._GM_DEFAULT.exists()


def test_el_hash_correcto_del_artefacto_leido_sostiene():
    """`artefacto A → hash A → lectura A → evidencia A` ✅"""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")
    real = D1.leer_metricas()["evidencia_sha256"]
    p = P.Procedencia(**_base(), evidencia=real, artefacto=str(D1._GM_DEFAULT))
    assert P.evidencia_corresponde(p) is True
    assert P.sostener("el IPE es X", p).peso == P.HECHO_VERIFICABLE


def test_un_hash_que_no_es_del_artefacto_DEGRADA():
    """`artefacto A → hash B` ⛔ — **ésta es la aserción que antes estaba
    invertida** en `test_d01_adversarial::test_ataque_2b` y en el ataque de la
    frontera, documentando el hueco. Ahora defiende la regla."""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")
    p = P.Procedencia(**_base(), evidencia="0000000000000000",
                      artefacto=str(D1._GM_DEFAULT))
    assert P.evidencia_corresponde(p) is False
    s = P.sostener("el IPE es X", p)
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD, (
        "un hash que no corresponde al artefacto no puede acreditar la lectura")
    assert "evidencia" in s.faltan


def test_un_artefacto_que_ya_no_esta_DEGRADA():
    """Si el artefacto desapareció o se movió, la afirmación **ya no puede
    verificarse contra lo que hay**. Puede ser que el hash fuera falso o que el
    archivo cambiara; QUIRA reporta que no puede sostenerla, no cuál de las dos
    cosas ocurrió — afirmar la causa sería inferir."""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")
    real = D1.leer_metricas()["evidencia_sha256"]
    p = P.Procedencia(**_base(), evidencia=real,
                      artefacto="/ruta/que/ya/no/existe.xlsx")
    assert P.evidencia_corresponde(p) is False
    assert P.sostener("x", p).peso == P.HALLAZGO_DE_VERIFICABILIDAD


def test_sin_artefacto_no_se_afirma_ni_se_niega_la_correspondencia():
    """EL RESIDUO, medido y no escondido.

    `None` —no `False`— porque no declarar el artefacto **no prueba que el hash
    sea falso**: lo hace incomprobable. Decir `False` acusaría de falsa una
    evidencia que sólo es no verificable, que es exactamente el error que este
    dominio persigue afuera: *«no lo encontré» ≠ «no existe»*."""
    p = P.Procedencia(**_base(), evidencia="0000000000000000")
    assert P.evidencia_corresponde(p) is None
    assert P.sostener("x", p).peso == P.HECHO_VERIFICABLE, (
        "sin artefacto declarado se acredita por existencia, como antes: el "
        "residuo es conocido y está bajo trinquete")


def test_los_dominios_migrados_declaran_su_artefacto():
    """TRINQUETE: puede subir, nunca bajar.

    Los dominios que pasaron por ADR-053 §5 deben poder demostrar su evidencia,
    no sólo declararla. Si uno dejara de hacerlo, volvería al hueco sin que
    nadie lo notara."""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")
    from app.agents.d02 import motor as D2

    for nombre, sostenida in (("d01", D1.sostener_ipe()),
                              ("d02", D2.sostener_isp())):
        assert sostenida.procedencia.artefacto, (
            f"{nombre} dejó de declarar el artefacto: su evidencia vuelve a ser "
            f"incomprobable")
        assert P.evidencia_corresponde(sostenida.procedencia) is True, (
            f"{nombre} declara una evidencia que no corresponde a su artefacto")


def test_el_artefacto_no_es_una_octava_capa():
    """Las siete capas de ADR-042 §6-bis no cambian. `artefacto` es el respaldo
    de la cuarta, no una capa más — si entrara en el conteo, toda procedencia
    existente pasaría a tener una capa «sin responder» que nadie le exigió."""
    p = P.Procedencia(**_base(), evidencia="abc", artefacto="/x")
    assert "artefacto" not in p.capas_respondidas()
    assert "artefacto" not in p.capas_sin_responder()
    assert len(p.capas_respondidas()) + len(p.capas_sin_responder()) == 7
