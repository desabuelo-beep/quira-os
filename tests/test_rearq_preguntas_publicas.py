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
    # ⚠️ Y la corrección que Javo obligó a hacer: `FONDO`/`FORMA` significaba
    # DOS COSAS distintas —arquitectura de producto y ontología de la gestión—
    # y ambas eran correctas. No se descarta ninguna: se SEPARAN, porque dos
    # ideas con el mismo nombre es lo que `DOC-033` prohíbe.
    txt = _DOC.read_text(encoding="utf-8")
    assert "DOS EJES, no dos versiones del mismo" in txt, (
        "los dos ejes volvieron a colapsarse en uno. Ambos valen; lo que no "
        "vale es que compartan nombre")
    assert "`SECTORIAL`" in txt and "`TRANSVERSAL`" in txt, (
        "el eje ontológico perdió su vocabulario propio y vuelve a colisionar "
        "con el arquitectónico")
    assert "ORTOGONALES" in txt, (
        "se perdió que los ejes se cruzan en vez de competir — que es lo que "
        "permite preguntar si un fenómeno transversal tiene FORMA")
    assert "No se dice «el ICPI es FONDO»" in txt, (
        "desapareció la regla de precisión que impide mezclar niveles")
    assert "sigue sin validarla" in txt, (
        "se perdió el límite del hallazgo. Que los macroejes admitan esa "
        "lectura no demuestra que sea mejor que la actual")


def test_un_indicador_sin_pregunta_no_se_evalua_como_malo():
    """★ REGLA PROTEGIDA: **falta el otro lado del cruce.**

    11 de 13 dominios no son cruzables hoy. Y la razón importa: **no es que
    su indicador sea malo** — es que no hay pregunta declarada contra la cual
    evaluarlo.

    ⚠️ Sin esta distinción, `Q-M2` leería «no cruzable» como «no responde», y
    once indicadores quedarían marcados por un vacío que no es suyo. Es la
    categoría `B` de `Q-M0`: problema de arquitectura, no del instrumento."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no puede responder bien ni mal: no se puede evaluar" in txt, (
        "desapareció la consecuencia lógica: sin pregunta no hay evaluación "
        "posible, ni positiva ni negativa")
    assert "Eso no lo convierte en malo" in txt, (
        "se perdió por qué un dominio no cruzable no imputa nada al "
        "indicador. Sin esa línea, un hueco de la ontología se le achaca")
    # ⚠️ Y `Q-M2` no queda bloqueada: queda ACOTADA al subconjunto maduro.
    # Decir «bloqueada» era demasiado fuerte y detenía trabajo que sí puede
    # hacerse.
    assert "`Q-M2` NO está bloqueada · está ACOTADA" in txt, (
        "Q-M2 volvió a declararse bloqueada. Puede trabajar sobre los "
        "dominios cuya curación ya permite establecer una pregunta")
    assert "subconjunto maduro" in txt


def test_el_mapa_de_madurez_distingue_no_trabajado_de_inexistente():
    """★ REGLA PROTEGIDA: **«todavía no trabajado» ≠ «no existe»**, ahora a
    nivel de dominio.

    La `v1` publicó «11 de 13 dominios no tienen pregunta rectora» como si
    fuera una carencia de la ontología. Javo lo corrigió: *«los dominios no
    están completos todos, hemos estado trabajando uno por uno»*.

    Es el mismo error del `71 %` → `62 %`, y por eso hacen falta **cinco
    estados y no dos**:

        DECLARADO · INCOMPLETO · NO INICIADO · NO DECLARADO · NO DETERMINABLE

    ⚠️ `NO INICIADO` y `NO DECLARADO` parecen lo mismo y son opuestos: el
    primero es un dominio que nadie ha curado; el segundo, uno que se curó y
    **aun así** no produjo pregunta. Sólo el segundo sería un hallazgo."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "MAPA DE MADUREZ, no un inventario de carencias" in txt, (
        "el mapa volvió a leerse como inventario de carencias")
    for estado in ("DECLARADO", "INCOMPLETO", "NO INICIADO", "NO DECLARADO",
                   "NO DETERMINABLE"):
        assert estado in txt, f"falta el estado `{estado}`"
    assert "no pueden clasificarse como carentes de pregunta" in txt, (
        "desapareció la formulación correcta del resultado")
    assert "lo que todavía no vimos → vacío → defecto" in txt, (
        "se perdió la cadena que NO debe seguirse")


def test_las_discrepancias_se_registran_y_no_se_resuelven():
    """★ REGLA PROTEGIDA: **una discrepancia entre el canon y la memoria del
    autor no la resuelve un script.**

    Aparecieron tres, y ninguna se decidió aquí:

        1. ¿12 o 13 dominios? Javo dice que `d04` (SAT) se eliminó; la
           Constitución Ontológica lo mantiene en cuatro lugares
        2. `d08` — Javo lo señala trabajado; `BOOT` dice ENTRABLE y no hay PCD
        3. `d06` tiene PCD cerrado y no figura entre los que Javo enumera

    ⚠️ Y una cuarta, que `DOC-033` obliga a no dar por hecha: que «Rendición
    de Cuentas y Transparencia» corresponda uno a uno con `d09` y `d07`. **El
    nombre no lo demuestra.**"""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Se registran; no se resuelven aquí" in txt, (
        "el expediente empezó a resolver discrepancias por su cuenta")
    assert "es propagarlo al canon" in txt, (
        "desapareció el caso `d04`. Y su lectura correcta no es «¿12 o 13?» "
        "sino: decisión aprobada + implementación efectivizada + canon no "
        "propagado")
    assert "CINCO dimensiones" in txt, (
        "un solo estado volvió a colapsar trabajo, curación, documentación, "
        "decisión e implementación — que es lo que producía las falsas "
        "discrepancias")
    assert "no autoriza" in txt and "clasificarlo como no trabajado" in txt, (
        "se perdió que la ausencia de PCD mide la FORMALIZACIÓN, no el "
        "trabajo realizado")
    assert "El nombre no lo demuestra" in txt, (
        "se perdió la aplicación de DOC-033 a la correspondencia de dominios "
        "por nombre")


def test_estar_curado_no_significa_quedar_congelado():
    """★ REGLA PROTEGIDA: **un dominio curado entra al refactor con más
    autoridad, no con menos.**

    Javo pidió unificar `d01` y `d02` en un solo dominio. Y tiene sentido que
    lo pidan los curados: son los únicos con evidencia suficiente para decidir
    si deben unificarse, dividirse o trasladarse.

    ⚠️ Pero la unificación concreta **es plausible y no está demostrada**:
    `IPE` —el indicador más maduro— vive en `d01` y mide precisamente la
    articulación plan↔presupuesto, lo que es evidencia a favor; y `d02` no
    tiene pregunta rectora declarada, así que **falta un lado de la
    comparación**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Estar curado no significa quedar congelado" in txt, (
        "se perdió que la curación habilita el refactor en vez de blindarlo")
    assert "plausible y no está demostrada" in txt, (
        "la unificación d01+d02 se dio por buena. Es evidencia a favor, no "
        "una decisión tomada")
    assert "falta un lado de la comparación" in txt


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
