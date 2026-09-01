# -*- coding: utf-8 -*-
"""
tests/test_brn_lector.py — los once ataques al lector verificable
════════════════════════════════════════════════════════════════════════════════
El colega listó lo que había que atacar antes de dar D-003 por cerrada, y esta
batería los recorre. La regla que gobierna todo el módulo:

> *«El lector no gobierna nada: verifica antes de entregar.»*

⚠️ UN ATAQUE NO SE PUEDE DEFENDER, Y SE DECLARA. El nº3 —«sello modificado para
apuntar al canon actual»— **no es detectable por este lector**: sin firma
criptográfica del artefacto de gobernanza, quien pueda escribir el sello puede
escribirlo coherente. Es la misma honestidad del escalón 5: *esto no es
infalsificable; impide la falsificación barata y silenciosa*. Se prueba que el
límite está declarado, no que se defiende.

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

from app.agents import brn_lector as L                    # noqa: E402


def _snapshot_con(tmp_path, mutar):
    """Copia el snapshot, le aplica una mutación y apunta el lector ahí.
    Nunca se toca el artefacto real."""
    d = json.loads(L._SNAP.read_text(encoding="utf-8"))
    mutar(d["brn_cno"])
    p = tmp_path / "snap.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


# ── ESTADO BASE ───────────────────────────────────────────────────────────────
def test_el_catalogo_esta_al_dia_y_sellado():
    c = L.leer()
    assert c.estado == L.AL_DIA and c.canon_coincide
    assert c.sello.estado == L.VALIDADO and c.sello.validado_por == "Javo"
    assert c.integridad_cno == (16, 16) and len(c.reglas) == 13


# ── 1 · CANON ALTERADO DESPUÉS DEL SELLO ──────────────────────────────────────
def test_ataque_1_canon_alterado_invalida_el_sello(monkeypatch):
    """Si el canon cambia tras el sello, el catálogo queda desactualizado y el
    sello anterior **no aplica**: acredita otra compilación."""
    monkeypatch.setattr(L, "canon_sha_actual", lambda: "ffffffffffffffff")
    c = L.leer()
    assert c.estado == L.DESACTUALIZADO
    assert not c.canon_coincide
    assert "el actual es" in c.por_que
    for r in c.reglas.values():
        assert not r.catalogo_al_dia
        assert not r.es_consumible_como_vigente, (
            "una regla de un catálogo desactualizado no puede consumirse")


# ── 2 · HASH FALSIFICADO EN EL SNAPSHOT ───────────────────────────────────────
def test_ataque_2_un_hash_falsificado_no_se_acredita_a_si_mismo(tmp_path, monkeypatch):
    """El lector **recalcula** el canon; no cree al artefacto. Si confiara en el
    `canon_sha256` declarado, un catálogo alterado se acreditaría solo."""
    p = _snapshot_con(tmp_path, lambda b: b.update({"canon_sha256": "dead0000dead0000"}))
    monkeypatch.setattr(L, "_SNAP", p)
    c = L.leer()
    assert c.estado == L.DESACTUALIZADO
    assert c.canon_sha256_actual == L.canon_sha_actual()
    assert c.sello.estado == L.NO_APLICA, (
        "el sello acreditó un catálogo cuyo hash no validó")


# ── 3 · EL ATAQUE QUE NO SE PUEDE DEFENDER, DECLARADO ─────────────────────────
def test_ataque_3_el_limite_del_lector_esta_declarado():
    """Quien pueda escribir el sello puede escribirlo apuntando al canon actual,
    y este lector lo aceptaría. **No es detectable sin firma criptográfica del
    artefacto de gobernanza.**

    Se declara en vez de fingirse: vender esto como infalsificable sería el tipo
    de afirmación que este observatorio existe para no hacer."""
    doc = (RAIZ / "app" / "agents" / "brn_lector.py").read_text(encoding="utf-8")
    assert "sólo el acto de gobernanza" in doc or "acto de gobernanza" in doc
    sello = json.loads(L._SELLO.read_text(encoding="utf-8"))
    assert "_caduca" in sello, "el sello dejó de declarar su propio mecanismo"


# ── 4 · SELLO ELIMINADO ───────────────────────────────────────────────────────
def test_ataque_4_sin_sello_es_no_consta_no_un_error(monkeypatch):
    """Ausencia de sello no es fallo del lector ni invalidez del catálogo: es
    `no_consta`. El catálogo sigue siendo técnicamente íntegro."""
    monkeypatch.setattr(L, "_SELLO", RAIZ / "docs" / "registry" / "no_existe.json")
    c = L.leer()
    assert c.sello.estado == L.NO_CONSTA and not c.sello.acredita
    assert c.integridad_cno == (16, 16), "la integridad no depende del sello"
    assert c.estado == L.AL_DIA, "sin sello el catálogo sigue al día"


# ── 5 · EL SELLO NO PROMOCIONA PIEZAS ─────────────────────────────────────────
def test_ataque_5_una_pieza_propuesta_sigue_propuesta():
    """EL SEGUNDO CANDADO. El sello significa «Javo validó este catálogo contra
    este canon», no «Javo validó cada decisión contenida en cada pieza»."""
    c = L.leer()
    assert c.sello.acredita, "esta prueba necesita el catálogo sellado"
    propuestas = [r for r in c.reglas.values() if r.estado_pieza == "propuesta"]
    assert propuestas, "no hay piezas en propuesta: el ataque no es medible"
    for r in propuestas:
        assert not r.es_consumible_como_vigente, (
            f"{r.id} se volvió consumible porque el catálogo está sellado")


# ── 6 y 7 · INTEGRIDAD RECALCULADA ────────────────────────────────────────────
def test_ataque_6_integridad_cno_alterada_no_engaña(tmp_path, monkeypatch):
    """El campo `integridad_compilacion` es una afirmación del compilador. El
    lector la **recalcula** sobre el contenido: alterarla no cambia el conteo."""
    def romper(b):
        b["integridad_compilacion"] = {"piezas_cno": "99/99", "piezas_ro": "99/99"}
        b["cno"][0]["cadena_integra"] = False
    p = _snapshot_con(tmp_path, romper)
    monkeypatch.setattr(L, "_SNAP", p)
    c = L.leer()
    assert c.integridad_cno == (15, 16), (
        f"el lector creyó al campo en vez de contar: {c.integridad_cno}")


def test_ataque_7_integridad_ro_alterada_no_engaña(tmp_path, monkeypatch):
    def romper(b):
        b["total_ro"] = 999
    p = _snapshot_con(tmp_path, romper)
    monkeypatch.setattr(L, "_SNAP", p)
    c = L.leer()
    assert c.integridad_ro == (13, 13), "el lector usó `total_ro` en vez de contar"


# ── 8 · CATÁLOGO INEXISTENTE O CORRUPTO ───────────────────────────────────────
def test_ataque_8_un_catalogo_ilegible_falla_explicitamente(tmp_path, monkeypatch):
    """Un lector que ante un archivo roto devolviera «cero reglas» convertiría un
    fallo de lectura en una afirmación sobre el canon. Se levanta excepción."""
    roto = tmp_path / "roto.json"
    roto.write_text("{ esto no es json", encoding="utf-8")
    monkeypatch.setattr(L, "_SNAP", roto)
    with pytest.raises(L.CatalogoNoVerificable):
        L.leer()

    monkeypatch.setattr(L, "_SNAP", tmp_path / "no_existe.json")
    with pytest.raises(L.CatalogoNoVerificable):
        L.leer()

    vacio = tmp_path / "vacio.json"
    vacio.write_text('{"otra_cosa": 1}', encoding="utf-8")
    monkeypatch.setattr(L, "_SNAP", vacio)
    with pytest.raises(L.CatalogoNoVerificable):
        L.leer()


# ── 9 · EL COMPILADOR NO FIRMA SU SELLO ───────────────────────────────────────
def test_ataque_9_el_lector_tampoco_escribe_el_sello():
    """Ni el compilador ni el lector pueden tocar el artefacto de gobernanza. Si
    el lector pudiera escribirlo, bastaría con leer para quedar validado."""
    doc = (RAIZ / "app" / "agents" / "brn_lector.py").read_text(encoding="utf-8")
    for linea in doc.splitlines():
        if "_SELLO" in linea and ("write_text" in linea or "json.dump" in linea):
            raise AssertionError(f"el lector escribe el sello: {linea.strip()}")


# ── 10 · EL CONSUMIDOR NO PUEDE ELEVAR EL GRADO ───────────────────────────────
def test_ataque_10_el_grado_no_sube_al_cruzar_la_frontera():
    """La misma regla de la consulta inter-dominio, aplicada al puente
    compilado: quien recibe una regla recibe **su** estado, y no hay ninguna vía
    para construir una `ReglaLeida` consumible a partir de una que no lo es —
    los objetos son inmutables."""
    import dataclasses

    c = L.leer()
    propuesta = next(r for r in c.reglas.values() if r.estado_pieza == "propuesta")
    with pytest.raises(dataclasses.FrozenInstanceError):
        propuesta.estado_pieza = "vigente"                      # type: ignore[misc]
    # Y si alguien fabrica una copia elevada, deja de corresponder al catálogo.
    falsa = dataclasses.replace(propuesta, estado_pieza="vigente")
    assert falsa.id in c.reglas
    assert c.reglas[falsa.id].estado_pieza == "propuesta", (
        "la copia elevada contaminó el catálogo leído")


# ── 11 · ÍNTEGRO ≠ VALIDADO ───────────────────────────────────────────────────
def test_ataque_11_integro_no_es_lo_mismo_que_validado(monkeypatch):
    """El ataque que el colega marcó como especialmente importante: que
    `integridad = 16/16` no se lea nunca como `validación humana = sí`.

    Sin sello, el lector debe poder decir **«técnicamente íntegro y no validado
    humanamente»** — dos afirmaciones distintas que no se implican."""
    monkeypatch.setattr(L, "_SELLO", RAIZ / "docs" / "registry" / "no_existe.json")
    c = L.leer()
    assert c.integridad_cno == (16, 16) and c.canon_coincide, "íntegro"
    assert not c.sello.acredita, "y a la vez NO validado"
    for r in c.reglas.values():
        assert not r.es_consumible_como_vigente, (
            "la integridad técnica bastó para consumir: el colapso que este "
            "ataque existe para impedir")
