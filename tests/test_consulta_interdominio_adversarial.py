# -*- coding: utf-8 -*-
"""
tests/test_consulta_interdominio_adversarial.py — atacar la frontera, no el caso feliz
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-30 · ADR-053 §6-bis). El colega, al llegar aquí:

> *«Después de construir el mínimo contrato, atacaría la frontera interdominio,
> no el contrato feliz. Eso sería mucho más valioso que simplemente demostrar
> que dos agentes pueden llamarse.»*

Los cuatro ataques son suyos, y cada uno intenta romper una garantía distinta:

    A → B                 hacer que la respuesta trate de otro sujeto
    GM-123 → GM-456       hacer que declare una evidencia que no es la suya
    G → G+1               hacer que el grado suba al cruzar
    Sostenida → verdad    hacer que d02 la convierta en verdad propia

LA GARANTÍA QUE TODOS DEFIENDEN, y es la razón de que el contrato exista:

> **Un dominio comparte evidencia gobernada, nunca verdades.** Cruzar la
> frontera no añade evidencia, y por tanto no puede añadir peso.

Dylus Lab © 2026
"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import procedencia as P                   # noqa: E402
from app.agents import sujeto as S                        # noqa: E402
from app.agents.consulta import (Consulta, GradoElevadoAlCruzar,   # noqa: E402
                                 Respuesta, SujetoDistintoAlCruzar, consumir)
from app.agents.d01 import motor as D01                   # noqa: E402


def _sujeto() -> str:
    return f"{S.POR_DEFECTO} {S.nombre_corto()}"


def _consulta_real() -> Consulta:
    return Consulta(
        solicitante="d02", consultado="d01", sujeto=_sujeto(),
        pregunta="¿qué evidencia sostiene la vinculación de inversión a metas?")


def _hay_gm() -> bool:
    return D01._GM_DEFAULT.exists()


# ── EL CASO REAL, primero: si esto no pasa, los ataques no significan nada ────
def test_00_d02_puede_preguntar_a_d01_y_recibir_evidencia():
    """La primera consulta inter-dominio de QUIRA. d02 evalúa sostenibilidad y
    necesita saber qué inversión está vinculada a metas — dato que d01 sostiene
    y que d02 tendría que re-derivar del mismo Gold Master."""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")

    r = D01.atender(_consulta_real())
    assert r.grado == P.HECHO_VERIFICABLE, f"faltan: {r.faltantes}"
    assert r.evidencia_sha256, "la respuesta no dice de qué evidencia sale"
    assert consumir(r).procedencia.sujeto == _sujeto()

    # Y lo que la respuesta SIGNIFICA está dicho, no queda a interpretación.
    assert "tiene evidencia para sostener" in r.dice_la_verdad_de()
    assert "es verdad" not in r.dice_la_verdad_de().lower()


# ── ATAQUE 1 · A → B · el sujeto ──────────────────────────────────────────────
def test_ataque_A_a_B_una_respuesta_de_otro_sujeto_no_se_consume():
    """Dos dominios podrían estar hablando de municipios distintos sin notarlo.
    Con 222 GAD produciendo las mismas métricas, es el error más silencioso
    posible: los números encajan y son de otro."""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")

    r = D01.atender(_consulta_real())
    # Se pregunta por otro municipio y se intenta colar la respuesta de éste.
    falsa = dataclasses.replace(
        r, consulta=dataclasses.replace(r.consulta, sujeto="130150 Manta"))
    with pytest.raises(SujetoDistintoAlCruzar):
        consumir(falsa)


# ── ATAQUE 2 · GM-123 → GM-456 · la evidencia ─────────────────────────────────
def test_ataque_GM_la_evidencia_viaja_con_la_respuesta_y_no_se_sustituye():
    """La evidencia declarada tiene que ser la del artefacto que produjo el
    número. Sustituirla dejaría una afirmación cuyo respaldo no existe.

    ✅ ESCALÓN 4 CERRADO el 2026-08-30. La respuesta que cruza la frontera ya
    no sólo declara un hash: declara **con qué artefacto se comprueba**, y la
    cadena lo verifica. Sustituir el hash degrada la afirmación en origen."""
    if not _hay_gm():
        pytest.skip("Gold Master no accesible")

    r = D01.atender(_consulta_real())
    real = r.evidencia_sha256
    assert real != "0000000000000000"

    # La afirmación que viaja declara su artefacto y corresponde.
    assert r.sostenida.procedencia.artefacto, (
        "la respuesta cruza la frontera sin decir con qué comprobar su evidencia")
    assert P.evidencia_corresponde(r.sostenida.procedencia) is True

    # ASERCIÓN INVERTIDA: un hash ajeno sobre el mismo artefacto ya no acredita.
    falseada = dataclasses.replace(r.sostenida.procedencia,
                                   evidencia="0000000000000000")
    assert P.evidencia_corresponde(falseada) is False
    assert P.sostener("x", falseada).peso == P.HALLAZGO_DE_VERIFICABILIDAD, (
        "una evidencia sustituida debe degradar la afirmación antes de cruzar")


# ── ATAQUE 3 · G → G+1 · el grado ─────────────────────────────────────────────
def test_ataque_G_mas_1_cruzar_la_frontera_no_eleva_el_grado():
    """EL ATAQUE CENTRAL. Si d01 sólo sostiene un hallazgo y d02 lo consume como
    hecho verificable, el grado subió **sin evidencia nueva** — y cruzar el
    límite entre dominios se habría convertido en la forma de saltarse
    `test_ninguna_transformacion_puede_subir_el_grado`.

    Nótese que **lanza en vez de degradar**: consumir mal una afirmación ajena
    no es un caso de uso que haya que tolerar, es un error de programa."""
    pobre = P.sostener(
        "no fue posible leer el IPE",
        P.Procedencia(fuente="Gold Master", sujeto=_sujeto()),
        P.HALLAZGO_DE_VERIFICABILIDAD)
    r = Respuesta(consulta=_consulta_real(), sostenida=pobre)

    assert r.grado != P.HECHO_VERIFICABLE
    with pytest.raises(GradoElevadoAlCruzar):
        consumir(r, como=P.HECHO_VERIFICABLE)

    # Consumirlo por lo que vale sí se permite, y conserva el grado original.
    assert consumir(r, como=r.grado).peso == pobre.peso


# ── ATAQUE 4 · Sostenida → verdad ─────────────────────────────────────────────
def test_ataque_verdad_la_respuesta_nunca_afirma_que_algo_sea_cierto():
    """El atajo epistemológico que el contrato existe para impedir.

    `dice_la_verdad_de()` genera la frase con el grado REAL, así que no hay
    forma de obtener de la respuesta una afirmación de verdad — ni cuando la
    cadena está completa, ni cuando falta todo."""
    pobre = P.sostener("x", P.Procedencia(fuente="GM", sujeto=_sujeto()))
    r = Respuesta(consulta=_consulta_real(), sostenida=pobre)
    frase = r.dice_la_verdad_de()

    assert "NO puede sostener" in frase, (
        "una cadena incompleta no puede producir una frase afirmativa")
    for prohibido in ("es verdad", "es cierto", "se comprueba que",
                      "demuestra que", "confirma que"):
        assert prohibido not in frase.lower(), (
            f"la respuesta afirma verdad con «{prohibido}»: QUIRA certifica "
            f"verificabilidad, nunca verdad (ADR-043 §3)")

    # Y el consumidor no recibe un valor: recibe la afirmación con su peso.
    s = consumir(r, como=r.grado)
    assert isinstance(s, P.Sostenida)
    assert s.habla_del_sujeto is False, (
        "una cadena incompleta no puede terminar hablando del sujeto tras cruzar")
