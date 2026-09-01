# -*- coding: utf-8 -*-
"""
tests/test_puente_compilado.py — D-003 · por qué nadie cruza el puente
════════════════════════════════════════════════════════════════════════════════
D-003 decía: *«las 13 RO están compiladas en `snapshot['brn_cno']` — el puente
existe, firmado y al día, y ningún motor lo cruza»*. Iba a construir el lector
para que lo cruzaran. **La medición previa lo impidió**, y el colega la había
exigido antes de escribir código:

> *«No modificar. No recalcular. No reparar todavía. Primero medir.»*

Y antes fijó la frontera que este módulo NO debe romper:

> *«el puente no debe hacer que el Gold Master consulte la BRN para decidir sus
> valores. La BRN explica y traza la dependencia; no gobierna el motor.»*

LO QUE LA MEDICIÓN ENCONTRÓ — tres cosas, y ninguna era la esperada:

 1 · **El catálogo se declara `propuesta` por un LITERAL.** `brn_cno.py:165`
     escribe `"estado_catalogo": "propuesta · pendiente de validación humana"`
     fijo, mientras la línea 147 sí deriva el estado de cada CNO. Aunque Javo
     selle todo el canon, el compilado seguirá diciendo pendiente: **un campo
     que nunca puede ser verdadero no informa** — el mismo defecto que tuvo
     `arbol_limpio` al contarse a sí mismo.

 2 · **El compilado está desactualizado.** Su fecha es 2026-08-19 y las 9 piezas
     de d07 —`CNO-VII-001..004` y `RO-VII-001..005`— se promovieron a `vigente`
     el 26-ago. El compilado las tiene como `propuesta`. Nueve de nueve,
     coincidencia exacta con un evento conocido.

 3 · Por tanto **cruzar el puente hoy sería consumir un catálogo obsoleto que
     además se auto-declara no validado.** No cruzarlo no era negligencia.

EL ORDEN CORRECTO, que la medición reveló: recompilar → resolver el literal del
estado → *sólo entonces* el lector. Construir el lector primero habría acoplado
nueve motores a un artefacto caducado.

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

_SNAP = RAIZ / "data" / "gm_snapshot.json"


def _brn():
    if not _SNAP.exists():
        return None
    d = json.loads(_SNAP.read_text(encoding="utf-8"))
    return d.get("brn_cno")


def test_el_puente_lleva_la_cadena_normativa_completa():
    """LO QUE EL PUENTE SÍ TIENE, y es más de lo que D-003 suponía: cada CNO
    viaja con su cadena de eslabones —`rol`, `norma`, `articulo`, `sumilla`— y
    con `cadena_integra`. La trazabilidad norma→regla está compilada."""
    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    c0 = brn["cno"][0]
    assert c0.get("cadena"), "la cadena normativa dejó de viajar compilada"
    esl = c0["cadena"][0]
    assert {"rol", "norma", "articulo"} <= set(esl), f"eslabón incompleto: {esl}"
    assert brn["cadenas_integras"] == brn["total_cno"]


def test_el_estado_del_catalogo_es_un_literal_que_nadie_puede_cambiar():
    """HALLAZGO 1 de D-003, con trinquete invertido.

    `scripts/brn_cno.py` escribe el estado del catálogo como texto fijo. Ninguna
    validación humana puede moverlo: el campo nunca podrá decir otra cosa. El
    día que se derive, esta prueba fallará — y ése será el arreglo."""
    fuente = (RAIZ / "scripts" / "brn_cno.py").read_text(encoding="utf-8")
    assert '"estado_catalogo": "propuesta' in fuente, (
        "el estado del catálogo ya no es un literal: actualizar D-003")
    # Y el contraste: el estado de cada CNO SÍ se deriva del YAML de origen.
    assert 'cno.get("estado"' in fuente, (
        "el compilador dejó de respetar el estado declarado por cada pieza")


def test_el_compilado_esta_desactualizado_respecto_del_canon():
    """HALLAZGO 2 de D-003, y explica por qué nadie debería cruzar todavía.

    Las 9 piezas de d07 se promovieron a `vigente` el 26-ago; el compilado es
    del 19-ago y las tiene como `propuesta`. Un motor que leyera este puente hoy
    recibiría el estado anterior a una promoción que Javo ya validó.

    El día que se recompile, esta prueba fallará."""
    import glob

    import yaml

    brn = _brn()
    if brn is None:
        pytest.skip("no está el snapshot")
    compilado = {c["id"]: c.get("estado") for c in brn["cno"]}
    compilado.update({r["id"]: r.get("estado")
                      for c in brn["cno"] for r in c.get("deriva_ro", [])})
    difieren = []
    for f in glob.glob(str(RAIZ / "docs" / "brn" / "*.yaml")):
        d = yaml.safe_load(Path(f).read_text(encoding="utf-8"))
        if not isinstance(d, dict) or not d.get("id"):
            continue
        if d["id"] in compilado and compilado[d["id"]] != d.get("estado"):
            difieren.append(d["id"])
    assert difieren, (
        "el compilado ya coincide con el canon en disco: se recompiló y D-003 "
        "avanzó — actualizar el hallazgo")
    assert all(x.endswith(tuple(f"-VII-00{n}" for n in range(1, 6)))
               for x in difieren), (
        f"divergen piezas fuera de d07, que no se explican por la promoción del "
        f"26-ago: {difieren}")


def test_ningun_motor_cruza_el_puente_todavia():
    """HALLAZGO 3. Y no cruzarlo **no era negligencia**: hacerlo hoy sería
    consumir un catálogo caducado que además se declara no validado.

    Los únicos que tocan `brn_cno` son su productor y los inventarios de
    auditoría — que lo leen para medirlo, no para calcular con él."""
    # ⚠️ SE LEE CON `pathlib`, NO CON `grep` POR SUBPROCESO. El primer intento
    # llamó a `subprocess.run(["grep"...])` y la frontera de efectos lo detuvo
    # —el mecanismo de la deuda 4-ter funcionando contra quien lo escribió—. La
    # salida correcta no era declarar `efecto_real`: era no necesitarlo.
    motores = [f for d in ("d01", "d02", "d03", "d07", "d08", "d09")
               for f in (RAIZ / "app" / "agents" / d).rglob("*.py")
               if "__pycache__" not in f.parts]
    consumidores = [f.relative_to(RAIZ).as_posix() for f in motores
                    if "brn_cno" in f.read_text(encoding="utf-8", errors="replace")]
    assert not consumidores, (
        f"un motor empezó a consumir el compilado: {consumidores} — comprobar "
        f"antes que el catálogo esté recompilado y validado")


def test_la_frontera_de_la_BRN_sigue_declarada():
    """LA REGLA QUE EL PUENTE NO PUEDE ROMPER, y que el colega fijó antes de
    dejar construir nada: la BRN **explica y traza**; no gobierna al motor. El
    flujo canónico sigue siendo `Excel → Python`, y el Gold Master permanece
    autónomo (Reglas de Oro 1 y 4)."""
    doctrina = _brn()
    if doctrina is None:
        pytest.skip("no está el snapshot")
    assert "REGLA" in doctrina["_doctrina"] and "ADR-035" in doctrina["_doctrina"]
    assert "MDN" in doctrina["_modelo"], (
        "el modelo de dependencias normativas dejó de declararse")
