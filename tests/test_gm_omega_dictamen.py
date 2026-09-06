# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_dictamen.py — GM-Ω-ICPI-011-C4 · el dictamen
════════════════════════════════════════════════════════════════════════════════
La cadena entera desemboca aquí, y cada etapa preguntó otra cosa:

    C3    ¿de dónde vino la decisión?
    010   ¿pertenece al núcleo o al contexto?
    C4    ¿merece permanecer?

★ EL HALLAZGO MEDIDO QUE REFORMULA `D1`

Ningún `E_i`, `T_i` ni `C_i` vale cero. Las 6 metas anuladas de 25 lo están
**exclusivamente por `V_i`**, y arrastran el 12,8 % del peso. Así que en el
estado actual `D1` y `D2` son **la misma pregunta en la práctica**, aunque
sigan siendo distintas en teoría.

★ Y EL CONTRAFACTUAL QUE SEPARA LAS TRES PROPOSICIONES DE `D2`

    vigente · anula, la meta sigue en el denominador     27,4582 %
    «no acreditado» · la meta sale del universo          31,4883 %   +4,03 pp

Tratar la falta de evidencia como «no acreditado» en vez de «no cumplido»
**mueve el índice cuatro puntos**. No es un matiz interpretativo: es una
decisión con efecto material sobre el resultado publicado.

⚠️ Y LO QUE EL DICTAMEN NO DICE: que el ICPI esté mal. Ninguna decisión
resultó incorrecta. `D` era incertidumbre, no condena.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_DICTAMEN_011C4.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "dictamen_c4.py"


def test_el_dictamen_no_interviene_el_motor():
    """`C4` juzga; no corrige. Y sus cifras son contrafactuales: ninguna
    puede citarse fuera del expediente (`DOC-010`)."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "C4 intenta escribir en el Gold Master"
    txt = _DOC.read_text(encoding="utf-8")
    for etiqueta in ("MATEMÁTICAMENTE REPRODUCIBLE",
                     "METODOLÓGICAMENTE CONTRAFACTUAL",
                     "NO AUTORIZADA PARA PUBLICACIÓN"):
        assert etiqueta in txt, f"desapareció la etiqueta «{etiqueta}»"
    assert "No recalibra" in txt


def test_las_siete_secciones_van_en_orden():
    """No se puede juzgar el álgebra antes de saber qué fenómeno se mide, ni
    la escala antes de saber qué clasifica. El orden **es** el método."""
    txt = _DOC.read_text(encoding="utf-8")
    pos = [txt.find(f"`C4-{i}` ·") for i in range(1, 8)]
    assert all(p > 0 for p in pos), "falta alguna de las siete secciones"
    assert pos == sorted(pos), (
        "las secciones se desordenaron. El orden no es cosmético: juzgar la "
        "escala antes de declarar su objeto es lo que DOC-012 prohíbe")


def test_toda_la_anulacion_viene_hoy_de_Vi():
    """★ El hallazgo que reformula `D1`.

    Ningún `E_i`, `T_i` ni `C_i` vale cero. Las metas anuladas lo están
    **sólo por falta de evidencia documental**.

    ⚠️ Consecuencia: discutir la multiplicatividad «en abstracto» es discutir
    otra cosa. Hoy `D1` se manifiesta **enteramente** a través de `D2`, y un
    dictamen que las tratara por separado sin decirlo estaría describiendo un
    motor que no es el que existe."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "opera hoy por **un solo factor**: `V_i`" in txt, (
        "desapareció el hallazgo que ancla D1 a la realidad del motor")
    assert "son la misma pregunta en la práctica" in txt, (
        "se perdió que D1 y D2 coinciden en el estado actual, aunque sean "
        "distintas en teoría")


def test_las_tres_proposiciones_de_D2_no_se_confunden():
    """★★ La sección decisiva del dictamen.

        1. «el fenómeno NO OCURRIÓ»            → afirmación sobre el mundo
        2. «no hay evidencia suficiente»       → sobre el conocimiento
        3. «la unidad no puede contribuir»     → regla metodológica

    La 3 puede ser perfectamente defendible. Lo que **no** puede es
    presentarse como consecuencia lógica de la 2 — y ése es el punto que `C4`
    tenía que resolver.

    ⚠️ Si esto se pierde, el índice vuelve a restar por no poder acreditar
    **sin declarar que eso es lo que hace**, y entonces la ausencia de
    evidencia se convierte en una inferencia sobre el mundo. Es exactamente lo
    que el principio rector prohíbe."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Las tres proposiciones que no pueden confundirse" in txt
    assert "no ocurrió" in txt and "no hay evidencia suficiente" in txt.lower()
    assert "presentarse como **consecuencia lógica** de la 2" in txt, (
        "desapareció la distinción central de D2: una regla metodológica "
        "legítima no es una deducción del estado del conocimiento")
    assert "puede LIMITAR lo que el sistema puede afirmar" in txt, (
        "se perdió la segunda regla del dictamen, la que gobierna C4-4")


def test_el_contrafactual_de_V0_esta_medido_y_acotado():
    """La diferencia entre «no acreditado» y «no cumplido» **tiene precio**, y
    el dictamen lo mide en vez de discutirlo.

    ⚠️ Y la tercera fila —presumir cumplimiento— NO es una alternativa
    defendible: contradice el principio rector. Se mide sólo para acotar el
    rango, y eso debe decirse, o alguien la citará como opción."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no es una alternativa defendible" in txt, (
        "desapareció la salvedad sobre presumir cumplimiento sin evidencia. "
        "Sin ella, una fila medida para acotar el rango se lee como propuesta")
    assert "decisión con efecto material medible" in txt, (
        "se perdió que el tratamiento de V=0 no es un matiz interpretativo")
    assert "31.4883" in txt or "31,4883" in txt, (
        "desapareció la cifra del contrafactual de exclusión")


def test_ninguna_decision_se_declara_incorrecta():
    """★ El límite del dictamen, y lo que impide que `D` se lea como condena.

    Ninguna de las cinco decisiones resultó incorrecta. `C4` no autoriza a
    eliminar nada: `D` significaba «no puede recibir presunción de necesidad»,
    no «está mal».

    ⚠️ Y el veredicto de `D1` tiene que decir las dos cosas: **ni necesaria ni
    incorrecta**. Perder cualquiera de las dos mitades convierte un dictamen
    en una sentencia."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "No dice que el ICPI esté mal" in txt, (
        "el dictamen dejó de declarar su límite. Sin esa línea, cinco "
        "veredictos se leen como cinco defectos")
    assert "No autoriza a eliminar nada" in txt
    assert "es **necesaria** al constructo | 🔴 **NO DEMOSTRADO**" in txt and \
           "es **incorrecta** | 🔴 **NO DEMOSTRADO**" in txt, (
        "el veredicto de D1 perdió una de sus dos mitades. Debe decir que no "
        "se demuestra necesaria NI incorrecta")
    assert "decisiones sometidas a prueba, no como cargos" in txt, (
        "se perdió cómo llegan las decisiones D desde 010")


def test_la_conclusion_es_declarar_no_corregir():
    """★ La conclusión de toda la investigación, y la única acción que el
    dictamen autoriza — que no toca una sola fórmula.

        El constructo funciona y es internamente coherente. Lo que le falta
        no son correcciones: es DECLARAR SUS PROPIAS ELECCIONES COMO
        ELECCIONES.

    Cinco decisiones sostienen el índice y ninguna está declarada como
    decisión: se presentan como si fueran propiedades del fenómeno. Esa es la
    diferencia entre un motor que se puede auditar y uno que sólo se puede
    creer."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "declarar sus propias elecciones como elecciones" in txt.lower(), (
        "desapareció la conclusión del dictamen. Sin ella, C4 termina en "
        "cinco veredictos sueltos y ninguna acción")
    assert "no toca una sola fórmula" in txt, (
        "se perdió que la acción autorizada NO es intervenir el motor")
    assert "un `ADR` por decisión" in txt, (
        "desapareció la forma concreta de la acción: declarar el estatuto de "
        "cada decisión D con sus alternativas")


def test_C4_2_declara_lo_que_no_puede_cerrar():
    """La honestidad sobre la unidad de análisis.

    Mientras `011-A2` no declare la unidad en el canon y `011-B` no establezca
    la correspondencia, **el ICPI se calcula sobre una unidad que el sistema
    no define formalmente**. El motor funciona; la definición vive en la
    práctica.

    ⚠️ Eso NO invalida el índice: lo **acota**. Es válido sobre su universo
    operacional declarado — lo que no puede hacerse es presentarlo como si
    midiera el PDOT completo."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no define formalmente" in txt, (
        "C4-2 dejó de declarar que la unidad no está en el canon")
    assert "no invalida el índice" in txt and "lo acota" in txt.lower(), (
        "se perdió el matiz: una unidad no declarada limita el alcance de las "
        "afirmaciones, no la validez del cálculo")
