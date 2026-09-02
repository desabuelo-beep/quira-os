# -*- coding: utf-8 -*-
"""
tests/test_d02_cruza_el_puente.py — el primer consumidor real del puente BRN
════════════════════════════════════════════════════════════════════════════════
D-005 era: `65` escrito en `enrich_presupuesto.py` mientras `RO-IV-001` declara
65 hasta 2026-12-31 y **70 desde 2027-01-01**. Hoy coincidían; el 1 de enero de
2027 dejarían de hacerlo y nada avisaría.

    detectar la copia caduca   →  el remedio
    hacerla imposible          →  la cura

El colega marcó la trampa que había que evitar: *«no cerraría D-005 simplemente
sustituyendo `UMBRAL = 65` por `lector.obtener(...)`. Eso sólo sería una
refactorización»*. El cierre exige que el consumidor **respete el estado**, no
sólo que cambie de dónde lee.

Y la frontera que este cruce no rompe (ADR-047): el lector dice *qué regla hay,
con qué estado y qué procedencia*; **la lógica de dominio sigue siendo de d02**.

⚠️ Y SI NO ES CONSUMIBLE, NO SE INVENTA UN NÚMERO. Volver al literal como
respaldo reintroduciría la deuda que este cambio cierra: d02 devuelve `None` con
el motivo, y quien lea el bloque sabrá que el umbral no está acreditado.

Dylus Lab © 2026
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import brn_lector as L                    # noqa: E402


def _d02():
    spec = importlib.util.spec_from_file_location(
        "_enrich_presupuesto", RAIZ / "scripts" / "enrich_presupuesto.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── EL CRUCE ──────────────────────────────────────────────────────────────────
def test_d02_recibe_el_umbral_con_su_procedencia_no_un_numero_suelto():
    """El primer consumidor real del puente. No recibe `65`: recibe la regla con
    su identidad, su vigencia temporal, la CNO de la que cuelga y el sello que
    la acredita."""
    u = _d02()._umbral_de_la_regla()
    assert u["estado"] == "consumible"
    assert u["valor"] == 65
    assert u["regla"] == "RO-IV-001" and u["deriva_de"] == "CNO-IV-001"
    assert len(u["vigencia_operativa"]) == 2, (
        "d02 debe ver los dos tramos, no sólo el vigente hoy")
    assert "Javo" in u["procedencia"]


def test_el_literal_ya_no_es_fuente_de_autoridad():
    """PASO 6 del colega: atacar el antiguo punto de copia. El `65` desapareció
    del bloque publicado; si vuelve, la deuda vuelve con él."""
    fuente = (RAIZ / "scripts" / "enrich_presupuesto.py").read_text(encoding="utf-8")
    assert '"umbral_cootad": 65' not in fuente, (
        "el literal volvió: D-005 se reabrió")
    assert '"umbral_cootad": _umbral_de_la_regla()' in fuente


# ── ATAQUES · el consumidor debe RESPETAR el estado, no sólo leerlo ───────────
def test_ataque_una_RO_propuesta_no_entra(monkeypatch):
    """PASO 9. Si la pieza pasara a `propuesta`, d02 **deja de consumirla** — no
    se entera por un test de deuda seis meses después."""
    real = L.regla

    def degradada(rid):
        import dataclasses
        r = real(rid)
        return dataclasses.replace(r, estado_pieza="propuesta") if r else None

    monkeypatch.setattr(L, "regla", degradada)
    u = _d02()._umbral_de_la_regla()
    assert u["valor"] is None and u["estado"] == "no_consumible"
    assert "propuesta" in u["por_que"]


def test_ataque_un_catalogo_desactualizado_bloquea_el_consumo(monkeypatch):
    """PASO 10. Si el canon cambia y nadie recompila, d02 no consume: el
    catálogo describe otro canon y su sello ya no aplica."""
    monkeypatch.setattr(L, "canon_sha_actual", lambda: "ffffffffffffffff")
    u = _d02()._umbral_de_la_regla()
    assert u["valor"] is None and u["estado"] == "no_consumible"
    assert "catálogo al día: False" in u["por_que"]


def test_ataque_sin_sello_no_hay_umbral(monkeypatch):
    """El sello es una de las tres condiciones y ninguna suple a otra: un
    catálogo íntegro y al día **sin validación humana** tampoco alimenta a d02."""
    monkeypatch.setattr(L, "_SELLO", RAIZ / "docs" / "registry" / "no_existe.json")
    u = _d02()._umbral_de_la_regla()
    assert u["valor"] is None and u["estado"] == "no_consumible"
    assert "sello acredita: False" in u["por_que"]


def test_ataque_lo_no_consumible_no_cae_al_literal():
    """LA TRAMPA QUE HABÍA QUE EVITAR. Un respaldo al `65` copiado dejaría el
    cambio en cosmética: el valor seguiría viniendo de la copia siempre que el
    puente fallara — y fallar es justo cuando más importa no inventar."""
    fuente = (RAIZ / "scripts" / "enrich_presupuesto.py").read_text(encoding="utf-8")
    cuerpo = fuente.split("def _umbral_de_la_regla")[1].split("\ndef ")[0]
    for caida in ("return 65", "return 0.65", "or 65", "valor\": 65"):
        assert caida not in cuerpo, (
            f"el consumidor cae al literal cuando el puente falla: «{caida}»")
    assert cuerpo.count('"valor": None') >= 3, (
        "los tres caminos de fallo deben devolver None con su motivo")


def test_el_lector_no_se_convirtio_en_un_segundo_motor():
    """La advertencia del colega, fijada: *«el lector no debe calcular el umbral,
    reinterpretar Derecho ni decidir qué significa RO-IV-001»*. Su trabajo es
    certificar la condición de consumo y exponer la regla **sin aumentar su
    grado**; la lógica sigue en d02 (ADR-047)."""
    # ⚠️ SE MIDE LA PROPIEDAD, NO LA PALABRA. El primer intento buscaba `sum(`
    # en el texto y falló contra `sum(1 for c in cnos if c.get(...))`, que es
    # **contar para verificar** —justo lo que el ataque 6 exige— y no calcular
    # una métrica. La palabra no es el uso, otra vez.
    #
    # La propiedad real: el lector entrega el valor de la regla **tal cual está
    # en el catálogo**, sin derivarlo ni transformarlo.
    import json

    brn = json.loads((RAIZ / "data" / "gm_snapshot.json").read_text(
        encoding="utf-8"))["brn_cno"]
    del_catalogo = {r["id"]: r.get("umbral_vigente")
                    for c in brn["cno"] for r in c.get("deriva_ro", [])}
    for rid, valor in L.leer().reglas.items():
        assert valor.umbral_vigente == del_catalogo[rid], (
            f"el lector transformó el valor de {rid}: entrega "
            f"{valor.umbral_vigente} y el catálogo dice {del_catalogo[rid]}")
        assert valor.vigencia_operativa == (
            next(r.get("vigencia_operativa") or []
                 for c in brn["cno"] for r in c.get("deriva_ro", [])
                 if r["id"] == rid)), f"el lector reinterpretó la vigencia de {rid}"
