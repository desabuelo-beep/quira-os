# -*- coding: utf-8 -*-
"""
tests/test_rearq_preguntas_publicas.py — REARQ · `Q-M1`
════════════════════════════════════════════════════════════════════════════════
Cada prueba de aquí protege **una regla arquitectónica concreta**. Si no hubiera
regla que proteger, todavía estaríamos en diseño conceptual y no correspondería
escribir un custodio.

★ EL RESULTADO INESPERADO DE `Q-M1`

Iba a reconstruir las preguntas necesarias. Lo que encontró es que **el canon ya
declaró las cuatro familias** —los macroejes de la Constitución— y que **11 de
13 dominios no tienen pregunta rectora escrita**. Las dos que existen, `d01` y
`d09`, son exactamente las que tienen `PCD` cerrado.

    La pregunta no aparece por escribirla: aparece al CURAR el dominio.

Y el camino para que existan **ya está definido** — es el `PCD` (`Regla de Oro
8`). No hace falta un método nuevo: hace falta aplicar el que hay a once
dominios.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "REARQ_Q-M1_PREGUNTAS_PUBLICAS.md"
_SCRIPT = RAIZ / "scripts" / "rearq" / "preguntas_publicas.py"


def test_las_preguntas_se_derivan_del_canon_y_no_se_inventan():
    """★ REGLA PROTEGIDA: **no se escribe el canon desde un script.**

    Once dominios no tienen pregunta rectora. La tentación evidente era
    redactarlas aquí — quedarían once celdas llenas y una matriz completa.
    Serían **inventadas**, y con apariencia de canon por venir de un artefacto
    derivado.

    ⚠️ Es la misma disciplina que impidió rellenar `Q-M0` de memoria, y la que
    `DOC-034` fija: no declarar ausencia sin mirar, **y no llenar el vacío con
    lo que uno supone que debería decir**."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "leer_dominios" in fuente, (
        "Q-M1 dejó de leer los dominios del contrato. Sin esa lectura, las "
        "familias y las preguntas pasarían a estar escritas en el script")
    txt = _DOC.read_text(encoding="utf-8")
    assert "escribir el canon desde un script" in txt, (
        "desapareció la regla que impide inventar las preguntas que faltan")
    assert "No inventa las once preguntas que faltan" in txt, (
        "Q-M1 dejó de declarar explícitamente qué no hace")


def test_FONDO_FORMA_sigue_siendo_hipotesis_contrastada():
    """★ REGLA PROTEGIDA: **evidencia que respalda una hipótesis no es la
    hipótesis demostrada.**

    Los macroejes se dejan leer como `FONDO`/`FORMA` —`1`,`2`,`3` son modos de
    administrar; `4` son materias y poblaciones—. Eso es **compatible** con la
    hipótesis de `010`, y es un hallazgo bonito: la distinción estaba
    implícita en la ontología desde el principio.

    ⚠️ Pero no demuestra que organice las preguntas **mejor** que la
    agrupación actual. Para compararlo harían falta las preguntas, y **once de
    trece no existen**. Es la misma cautela que se aplicó a `IED`."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "contrastada contra los macroejes, no asumida" in txt, (
        "FONDO/FORMA volvió a darse por buena. Se contrasta; no se asume")
    assert "no la valida todavía" in txt, (
        "se perdió el límite del hallazgo. Que los macroejes admitan esa "
        "lectura no demuestra que sea mejor que la actual")
    assert "once de trece no existen" in txt, (
        "desapareció la razón por la que la comparación no puede hacerse aún")


def test_un_indicador_sin_pregunta_no_se_evalua_como_malo():
    """★ REGLA PROTEGIDA: **falta el otro lado del cruce.**

    11 de 13 dominios no son cruzables hoy. Y la razón importa: **no es que
    su indicador sea malo** — es que no hay pregunta declarada contra la cual
    evaluarlo.

    ⚠️ Sin esta distinción, `Q-M2` leería «no cruzable» como «no responde», y
    once indicadores quedarían marcados por un vacío que no es suyo. Es la
    categoría `B` de `Q-M0`: problema de arquitectura, no del instrumento."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no son cruzables hoy" in txt
    assert "No porque su indicador sea malo" in txt, (
        "se perdió por qué 11 dominios no se pueden cruzar. Sin esa línea, "
        "un hueco de la ontología se le imputa al indicador")
    assert "no puede responder bien ni mal: no se puede evaluar" in txt, (
        "desapareció la consecuencia lógica: sin pregunta no hay evaluación "
        "posible, ni positiva ni negativa")


def test_la_pregunta_aparece_al_curar_el_dominio():
    """★ REGLA PROTEGIDA: **el método ya existe; no hace falta inventar otro.**

    Los dos dominios con pregunta declarada —`d01` y `d09`— son exactamente
    los que tienen `PCD` cerrado. La correlación no es casual: **la pregunta
    no aparece por escribirla, aparece al curar el dominio** (`Regla de Oro
    8`).

    ⚠️ Y la consecuencia operativa no es «curar los once antes de seguir»,
    sino que la Rearquitectura tiene una **dependencia declarada**: cualquier
    decisión sobre residencia se apoya en preguntas que, en once casos,
    todavía no están escritas."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "aparece al **curar** el dominio" in txt or \
           "aparece al CURAR el dominio" in txt, (
        "se perdió el hallazgo del método: la pregunta es un producto de la "
        "curación, no un requisito previo")
    assert "No hace falta un método nuevo" in txt, (
        "desapareció la conclusión operativa de Q-M1")
    assert "dependencia declarada" in txt, (
        "se perdió que la Rearquitectura queda condicionada, sin quedar "
        "bloqueada. Declarar la dependencia es lo que evita decidir a ciegas")
