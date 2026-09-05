# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_justificacion.py — GM-Ω-ICPI-011-C3 · reconstrucción causal
════════════════════════════════════════════════════════════════════════════════
`C2` preguntó **qué dice** `C_i`. `C3` pregunta **por qué el sistema terminó
usando esa regla, esos pesos, ese piso y ese fallback** — y cuánto de esa cadena
puede demostrarse.

★ EL HALLAZGO QUE REORDENÓ LA ETAPA

`metodologia.docx`, creado el **25-mar-2026** —anterior al 27-abr—, define las
**seis** variables con definición conceptual, fundamento normativo y tabla de
escala. Eso obligó a corregir dos cosas que se daban por sabidas:

    007-B0 decía  «C_i entró el 27-abr-2026»
    y consta      el CONCEPTO es anterior; esa fecha data «Ci DETERMINISTA
                  v1.0», una versión nueva de un factor preexistente

    011-C2 decía  «nada en el instrumento explica la divergencia E_i ↔ C_i»
    y consta      cierto DEL INSTRUMENTO, falso DEL CORPUS: son dos ejes del
                  mismo Estatuto —quién EJECUTA vs. quién RESPONDE— con escala
                  ordinal común, y la metodología trae hasta un caso ilustrado

⚠️ LA CADENA SE CORTA EN LA RAZÓN, y eso es el resultado, no un fallo del
peritaje: por qué se sustituyó el constructo de `C_i`, por qué esos pesos y por
qué ese piso **no constan en ninguna fuente**. `DOC-022` lo explica —la
evolución fue conversacional— y `DOC-011` prohíbe inventar la causa.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_JUSTIFICACION_011C3.md"
_C2 = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_SEMANTICA_011C2.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "justificacion_transformaciones.py"


def test_C3_no_interviene_el_motor():
    """El encargo era un peritaje, no un rediseño. `C3` no toca `C_i`, `E_i`,
    `T_i`, la fórmula, las calibraciones, `Ci_Manual_2025` ni `Ci_Adaptativo`.

    ⚠️ Y ES LA TENTACIÓN REAL DE ESTA ETAPA: al encontrar cuatro reglas
    discrepantes, lo natural es querer elegir una. Elegirla sería sustituir un
    peritaje por una decisión de diseño sobre un motor congelado."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "011-C3 intenta escribir en el Gold Master"
    txt = _DOC.read_text(encoding="utf-8")
    assert "No se tocó nada" in txt, (
        "desapareció la declaración de no intervención. Sin ella, un "
        "expediente que documenta cuatro reglas discrepantes se lee como el "
        "preámbulo de una corrección")
    assert "27,4582 % sigue congelado" in txt or "27,4582 %" in txt, (
        "se perdió la constancia del baseline congelado")


def test_la_fecha_de_Ci_se_corrige_sin_borrar_el_error():
    """★ La corrección a `007-B0`, y por qué el error era reconocible.

    `H01!A94` dice «★ Ci DETERMINISTA v1.0 … 27-Abr-2026». Se leyó como la
    fecha de nacimiento del factor. Pero la celda data **una versión**, y una
    metodología del 25-mar ya contiene `C_i`.

    ⚠️ ES EL ESCALÓN 7 DE LA ESCALERA —**lo leído ≠ la fuente**— aplicado a una
    genealogía: se tomó la fecha del artefacto que DOCUMENTA un cambio como si
    fuera la fecha del CONCEPTO. Si esta constancia se pierde, el próximo que
    lea `A94` volverá a datar el factor en abril."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "hay que corregir `007-B0`" in txt, (
        "desapareció la corrección de la fecha de C_i. Sin ella sigue "
        "circulando que el factor nació el 27-abr")
    assert "esa fecha data su **versión determinista**" in txt, (
        "se perdió la lectura correcta de H01!A94: data una VERSIÓN, no la "
        "creación del factor")
    assert "lo leído ≠ la fuente" in txt, (
        "desapareció el diagnóstico del error. Nombrarlo es lo que impide "
        "repetirlo, y esta auditoría ya lo cometió antes")


def test_la_sustitucion_de_constructo_queda_documentada():
    """★ El hallazgo central de `C3`.

    Lo del 27-abr no fue una incorporación: fue **una sustitución de mecanismo
    bajo el mismo nombre**.

        ANTES   C_i = IMPUTABILIDAD ORGÁNICA      Constitución 233 · NCI 401-01
                claridad de la asignación         escala {1,00 · 0,90 · 0,75}
        DESPUÉS C_i = CALIDAD DE PROCESO          LOSNCP · CGE · COPFP · CPCCS
                descuento por infracciones        MAX(0,50 · 1 − Σ deducciones)

    Y ninguna capa se retiró: la Sección I sigue implementando el constructo
    original, las Secciones L/M el nuevo, y `Ci_Manual_2025` conserva los
    valores del primero como fallback. **Las cuatro divergencias de `C2` son un
    solo fenómeno: dos generaciones del factor conviviendo.**"""
    txt = _DOC.read_text(encoding="utf-8")
    assert "sustitución de mecanismo bajo el mismo nombre" in txt, (
        "desapareció el hallazgo central. Sin él, las divergencias de C2 "
        "vuelven a parecer cuatro anomalías sueltas en vez de un solo cambio "
        "no propagado")
    assert "Dos generaciones del mismo factor conviven" in txt, (
        "se perdió la explicación unificada de las divergencias")
    assert "el instrumento no declara cuál gobierna" in txt, (
        "desapareció el límite: C3 documenta que conviven, no cuál rige. "
        "Elegir una sería una decisión de diseño sobre un motor congelado")
    assert "La **razón** de la sustitución | ⬜ **NO DETERMINABLE**" in txt, (
        "la razón del cambio dejó de declararse NO DETERMINABLE. Es el "
        "resultado honesto: DOC-022 explica por qué no está —la evolución fue "
        "conversacional— y DOC-011 prohíbe inventarla")


def test_la_superposicion_EiCi_resulta_estar_justificada():
    """★ La corrección que `C3` le debe a `C2`, y que va en dirección contraria
    a lo que se esperaba.

    `C2` escribió que «nada en el instrumento explica la diferencia». Era
    cierto **del instrumento** y falso **del corpus**: la metodología define
    dos ejes distintos sobre el mismo Estatuto Orgánico —

        E_i   quién EJECUTA    directa 1,00 · convenio 0,90 · delegada 0,75
        C_i   quién RESPONDE   único 1,00 · compartida 0,90 · difusa 0,75

    — y hasta trae un caso: `M3` (Salud), ejecución directa (`E=1,00`) con
    responsabilidad compartida entre Planificación y Obras Públicas (`C=0,90`).

    ⚠️ ASÍ QUE LA SUPERPOSICIÓN NO ES UN DEFECTO: es deliberada y razonada. Lo
    que sigue sin explicación son las 12 asignaciones divergentes concretas."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "quién EJECUTA" in txt and "quién RESPONDE" in txt, (
        "desapareció la distinción entre los dos ejes. Sin ella, la escala "
        "común de E_i y C_i vuelve a leerse como redundancia")
    assert "es deliberada y está justificada en la metodología" in txt, (
        "se perdió que la superposición está justificada documentalmente")
    c2 = _C2.read_text(encoding="utf-8")
    assert "CORRECCIÓN POSTERIOR — aportada por `011-C3`" in c2, (
        "011-C2 no recibió la corrección. Un expediente que no propaga lo que "
        "una etapa posterior matiza sigue afirmando algo incompleto")
    assert "cierta del instrumento y falsa del corpus" in c2, (
        "desapareció el diagnóstico preciso del error de C2: buscar sólo en el "
        "Gold Master cuando la razón vivía en la metodología")


def test_la_entrega_material_se_reubica_en_Ti_con_su_limite():
    """★ La corrección que rescata la intuición de Javo, reubicándola.

    `C2` concluyó que ninguna variable contempla la entrega material. La
    metodología obliga a matizarlo: `T_i` se define sobre el **devengado y no
    el compromiso**, y el devengado exige acta de entrega-recepción (Acuerdo
    067 MEF). La metodología lo justifica como anti-gaming con esas palabras.

    Javo señalaba un mecanismo real; se equivocó de variable.

    ⚠️ PERO EL LÍMITE HAY QUE DECIRLO IGUAL DE CLARO: el motor lee la columna
    «Devengado» de eSIGEF, **no comprueba que el acta exista**. La protección
    es normativa, no verificada. Perder ese matiz convertiría una delegación de
    confianza en una capacidad del motor — y eso es justo lo que QUIRA existe
    para no hacer."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "pero en `T_i`, no en `C_i`" in txt, (
        "desapareció la reubicación. Sin ella, C2 deja dicho que el constructo "
        "ignora la entrega material, y la metodología demuestra que no")
    assert "normativa, no verificada por el motor" in txt, (
        "se perdió el límite. Una protección normativa presentada como "
        "verificación es exactamente la clase de afirmación que QUIRA audita "
        "en otros")
    assert "Acuerdo 067" in txt or "Acuerdo Ministerial 067" in txt, (
        "desapareció la fuente normativa que sostiene el matiz")


def test_C3_declara_donde_se_corta_la_cadena():
    """El resultado incómodo, y el que no debe suavizarse.

    De las nueve preguntas, tres quedan `NO DETERMINABLE`: por qué se sustituyó
    el mecanismo, por qué esos pesos y por qué ese piso. No es que el peritaje
    fallara — es que **la razón nunca se escribió** (`DOC-022`).

    ⚠️ Y HAY UN PRECEDENTE DECLARADO QUE NO ALCANZA: `H95` `L-07` dice que los
    pesos del TGI son «criterio experto (Dylus Lab), no PCA ni regresión». Eso
    documenta una PRÁCTICA, no justifica LOS PESOS DE `C_i` — y confundir una
    cosa con otra sería tomar un precedente por una prueba."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "se corta en la razón" in txt, (
        "desapareció la declaración de dónde termina lo demostrable")
    assert "nunca se escribió" in txt, (
        "se perdió la explicación del corte. Sin ella, tres NO DETERMINABLE "
        "parecen un peritaje incompleto en vez de un hallazgo")
    assert "criterio experto" in txt, (
        "desapareció el único precedente declarado sobre los pesos. Es débil "
        "y por eso mismo hay que mostrarlo: documenta una práctica, no "
        "justifica los pesos de C_i")
    assert "**NO DETERMINABLE**" in txt


def test_el_registro_de_versiones_no_cubre_el_cambio_de_Ci():
    """`H80_MODEL_REGISTRY` versiona el motor con fecha, operador y predecesor
    — y el cambio más consecuente cae en un salto sin entrada propia:

        v1.0.2  31-mar-2026        ARCHIVADO
             ⬅ 27-abr · Ci DETERMINISTA v1.0
        v2.1    01-may-2026        ACTIVO

    ⚠️ NO ES UNA ACUSACIÓN DE MAL VERSIONADO. El registro existe, es coherente
    y `P-05` del protocolo de gobernanza algorítmica lo exige. Lo que falta es
    GRANULARIDAD: sustituir el constructo de un factor se registra igual que
    cualquier otro cambio."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no tiene entrada propia en el registro" in txt, (
        "desapareció la observación sobre el versionado")
    assert "no es una acusación de mal versionado" in txt.lower(), (
        "se perdió la salvedad. El registro cumple lo que el protocolo exige; "
        "lo que falta es granularidad, y la diferencia importa")
