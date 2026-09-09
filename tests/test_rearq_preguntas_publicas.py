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
    assert "No inventa las preguntas que todavía no están disponibles" in txt, (
        "Q-M1 dejó de declarar explícitamente qué no hace")
    # ⚠️ Y la corrección del colega sobre CÓMO se nombra ese vacío: decir
    # «faltan once preguntas» imputa una carencia a la ontología. El estado
    # real es que todavía no están disponibles para los dominios no curados.
    assert "aún no" in txt and "formalmente disponibles" in txt, (
        "volvió la formulación que convierte trabajo pendiente en carencia")


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

    ⚠️ Y la `v2` lo decía en prosa mientras **calculaba un solo estado**. Las
    cinco dimensiones son ahora estructura del script, no redacción: cada una
    viaja con su propia prueba y **ninguna se infiere de otra**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "MAPA DE MADUREZ, no un inventario de carencias" in txt, (
        "el mapa volvió a leerse como inventario de carencias")
    for dim in ("trabajo", "curación", "documental", "decisión",
                "implementación"):
        assert dim in txt, f"falta la dimensión `{dim}`"
    assert "no pueden clasificarse como carentes de pregunta" in txt, (
        "desapareció la formulación correcta del resultado")
    assert "lo que todavía no vimos → vacío → defecto" in txt, (
        "se perdió la cadena que NO debe seguirse")


def test_un_PCD_cerrado_no_acredita_que_el_dominio_este_completo():
    """★ REGLA PROTEGIDA: **conformidad ≠ suficiencia.**

    Es el hallazgo que `PCD-D06` obligó a escribir, y el que la `v2` violaba en
    código: derivaba el estado del dominio de «¿existe el `PCD`?».

    `PCD-D06` está **CERRADO** y su dominio no tiene silo de entrada, no
    calcula `ICM` y su alerta sigue apagada (`sat_evaluator.py:297`, verificado
    un mes después del cierre).

    ⚠️ El `PCD` hace con el dominio **lo mismo que QUIRA hace con el GAD**: no
    certifica que esté bien, certifica que lo que hay es trazable y que lo que
    falta está declarado. Sin esta regla, seis archivos en `docs/pcd/` se leen
    como seis dominios terminados."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "estado_dimensional" in fuente, (
        "volvió el estado único por dominio. Cada dimensión debe calcularse "
        "por separado y con su propia evidencia")
    assert "estado_curacion" not in fuente, (
        "reapareció la función que colapsaba las cinco dimensiones en una")
    txt = _DOC.read_text(encoding="utf-8")
    assert "CONFORMIDAD de lo que existe" in txt and "SUFICIENCIA" in txt, (
        "desapareció la regla que impide leer un PCD cerrado como un dominio "
        "completo")
    # ⚠️ La dimensión `trabajo` se prueba con evidencia MATERIAL —código en
    # disco—, no con la declaración de nadie. Fue lo que resolvió `d08`.
    assert "app/agents/" in fuente, (
        "el script dejó de leer los agentes en disco. Sin esa lectura, "
        "`trabajo` vuelve a depender de lo que alguien recuerde")


def test_PENDIENTE_no_es_un_destino_REARQ():
    """★ REGLA PROTEGIDA: **un estado de la decisión no es un destino.**

    Se listaba `PENDIENTE` como noveno destino junto a `CONSERVAR`,
    `TRASLADAR` o `DEPRECAR`. No pertenece a esa familia: los ocho responden
    *«¿qué hacemos con este dominio?»* y `PENDIENTE` responde *«¿ya podemos
    decidirlo?»*.

    ⚠️ Mezclarlos permitiría cerrar un dominio con destino `PENDIENTE` y dar
    el análisis por terminado. Un dominio con la decisión pendiente **no tiene
    destino asignado todavía**, que es justo lo que hay que poder decir."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "`PENDIENTE` no es un destino" in txt, (
        "PENDIENTE volvió a listarse como destino REARQ")
    assert "Ocho destinos" in txt, (
        "el conteo de destinos volvió a incluir el estado de la decisión")
    assert "estado de la\ndecisión" in txt or "estado de la decisión" in txt


def test_el_cruce_es_evidencia_y_no_dictamen():
    """★ REGLA PROTEGIDA: **el cruce `A/B/C/D` no determina el destino.**

    Es evidencia para evaluarlo. Un indicador puede «responder bien» y aun así
    deber trasladarse; puede «no responder» porque la pregunta está mal
    planteada.

    ⚠️ Leer `D → RECONSTRUIR` automáticamente sustituiría el juicio
    arquitectónico por una tabla — que es la versión sofisticada del mismo
    error que `Q-M0` cometió al derivar estado de la existencia de un
    archivo."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no determina por sí solo el destino" in txt, (
        "el cruce volvió a leerse como dictamen automático de destino")
    assert "evidencia para evaluarlo" in txt


def test_la_lectura_SECTORIAL_TRANSVERSAL_se_marca_como_hipotesis():
    """★ REGLA PROTEGIDA: **lo que el canon admite ≠ lo que el canon dice.**

    El reparto `1,2,3 → TRANSVERSAL` y `4 → SECTORIAL` es una lectura que la
    Constitución **admite**, no una clasificación que **haga**.

    ⚠️ Publicarlo sin marca lo convertiría en propiedad del canon por el solo
    hecho de aparecer en un documento derivado — exactamente la promoción
    indebida que `Q-M0` tuvo que corregir."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "HIPÓTESIS DE LECTURA ONTOLÓGICA" in txt, (
        "la lectura sectorial/transversal se publicó como hecho del canon")
    assert "no está declarado en la Constitución" in _plano(txt), (
        "desapareció el límite explícito de la hipótesis")


def _plano(t: str) -> str:
    """Une los saltos de línea del markdown para que una aserción no dependa
    de dónde cayó el ajuste de línea."""
    return " ".join(t.split())


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
