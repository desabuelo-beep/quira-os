# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_semantica.py — GM-Ω-ICPI-011-C2 · genealogía semántica
════════════════════════════════════════════════════════════════════════════════
`011-C1` reconstruyó el álgebra del ICPI. `011-C2` reconstruye el SIGNIFICADO:
qué declara medir cada factor, y si su mecanismo mide eso.

La etapa se adelantó a `010` por una razón concreta: `009` clasificó `C_i` dos
veces y las dos se equivocó. Mientras no se sepa qué significan `E_i` y `C_i`,
todo análisis de comportamiento se hace sobre variables cuya ontología seguimos
reconstruyendo.

★ LOS CUATRO HALLAZGOS QUE ESTAS PRUEBAS PROTEGEN

    1. `C_i` mide LEGALIDAD del proceso, no entrega material     → refuta 009
    2. `E_i` y `C_i` comparten escala, vocabulario y fuente…
       …pero divergen en 12 de 25 metas: NO son la misma variable
    3. El glosario y la Sección L discrepan sobre `INF-03`,
       sobre `INF-04` y sobre el piso de `C_i`
    4. Las Secciones L y M se contradicen: «abandona la heurística»
       frente a «`Ci_Manual_2025` es el fallback vigente»

⚠️ NINGUNO CAMBIA HOY EL ICPI. Sin infracciones registradas, las reglas
discrepantes no se ejecutan. Eso los hace **latentes**, no inofensivos: se
activan el día que se registre la primera infracción, que es exactamente el día
en que el motor tiene que estar bien.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_SEMANTICA_011C2.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "semantica_factores.py"


def test_el_expediente_se_deriva_del_instrumento_no_de_la_memoria():
    """La regla que hace utilizable a `011-C2`: **se lee del Gold Master**.

    Una genealogía semántica escrita de memoria es exactamente el defecto que
    GM-Ω viene documentando —el derivado narrativo desacoplado de su fuente—.
    Si estas lecturas desaparecen, el expediente pasa a decir lo que alguien
    recordaba de las variables, no lo que el instrumento declara."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    for hoja in ("H02_GLOSARIO_QUIRA", "H01_PARÁMETROS",
                 "H12_MOTOR_ICPI_CANÓNICO"):
        assert hoja in fuente, (
            f"`011-C2` dejó de leer `{hoja}`. Sin esa hoja, la semántica se "
            f"reconstruye de memoria y el expediente deja de ser auditable")
    assert ".save(" not in fuente, "011-C2 intenta escribir en el Gold Master"


def test_Ci_mide_legalidad_del_proceso_y_no_entrega_material():
    """★ El hallazgo que refuta a `009` y salva su cierre.

    La hipótesis era: «`C_i` exige acta de entrega-recepción e impacto
    verificado; `T=1` con `C→0` anula el maquillaje contable de noviembre».

    El instrumento dice otra cosa. `C_i` es **«Calidad de Proceso Orgánico»**:
    nace en 1,00 por presunción de legalidad y sólo baja ante **infracciones
    normativas verificadas** —LOSNCP, CGE/NCI, COPFP, CPCCS—. Ninguna de las
    cuatro mide entrega.

    ⚠️ LA MITAD DE ATRIBUCIÓN SÍ SE SOSTIENE: la Sección I imputa cada meta a
    una unidad orgánica con su base legal. Perder ese matiz convertiría una
    refutación parcial en una descalificación, y no lo es."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "mide legalidad del proceso, no entrega del producto" in txt, (
        "desapareció el hallazgo central de 011-C2. Sin él vuelve a circular "
        "que el motor tiene una defensa contra el maquillaje contable de fin "
        "de ejercicio, y no la tiene")
    assert "presunción de legalidad" in txt, (
        "se perdió el mecanismo: C_i NACE en 1,00 y se DEDUCE. Sin eso, un "
        "C_i alto se lee como logro verificado y es una presunción")
    assert "**Atribución**" in txt and "✅ **SÍ**" in txt, (
        "desapareció la mitad de la hipótesis que SÍ se sostiene. Una "
        "refutación que se lleva por delante lo correcto es imprecisa")


def test_la_entrega_material_no_la_mide_ninguna_variable():
    """La consecuencia, y la que no debe suavizarse.

    Si `C_i` no verifica entrega y ninguna otra variable lo hace, entonces la
    disociación financiero ↔ físico —anticipo en noviembre, obra sin empezar—
    **no la captura el motor hoy**. `009` afirmaba lo contrario."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no está implementada en ninguna variable del ICPI" in txt, (
        "se perdió la consecuencia. Sin ella, 011-C2 queda como una precisión "
        "terminológica cuando es un hueco de cobertura del motor")
    gaming = (RAIZ / "docs" / "architecture" /
              "GM-OMEGA_ICPI_GAMING_009.md").read_text(encoding="utf-8")
    assert "CORRECCIÓN POSTERIOR — aportada por `011-C2`" in gaming, (
        "009 dejó de registrar su corrección. Un expediente que no propaga lo "
        "que una etapa posterior desmiente sigue afirmando algo falso")
    assert "NINGUNA VARIABLE LO MIDE" in gaming, (
        "el diagrama de 009 volvió a atribuir la verificación de entrega a "
        "`C_i`. La rama está vacía y debe verse vacía")


def test_Ei_y_Ci_comparten_escala_pero_no_son_la_misma_variable():
    """★ El solapamiento, y la precisión que impide exagerarlo.

        `E_i`  autonomía orgánica       1,0 autónomo / 0,9 compartido / 0,75 difuso
        `C_i`  calidad proceso orgánico 1,0 / 0,9 / 0,75 · «exclusivo/compartido/difuso»

    Misma escala, mismo vocabulario, misma fuente declarada (Res. 040-2025).
    La conclusión fácil sería «están duplicadas» — y es **falsa**: divergen en
    12 de 25 metas. Si fueran la misma variable coincidirían en todas.

    ⚠️ EL HALLAZGO REAL ES PEOR DE DIAGNOSTICAR Y MEJOR DE CORREGIR: están
    parcialmente solapadas y **nada en el instrumento explica dónde divergen**.
    Una divergencia puede ser legítima (competencia autónoma con proceso
    difuso) o un error de asignación, y `011-C2` no puede distinguirlas."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "🔴 **REFUTADO** · divergen en" in txt, (
        "se perdió la refutación de la duplicación. Afirmar que E_i y C_i son "
        "la misma variable sería un hallazgo espectacular y falso")
    assert "ambigüedad ontológica" in txt, (
        "desapareció lo que sí está demostrado: dos dimensiones distintas de "
        "la fórmula usan el mismo vocabulario y la misma escala sobre la "
        "misma fuente")
    assert "nada en el instrumento explica la diferencia" in txt, (
        "se perdió el límite del hallazgo. Sin él, 011-C2 parecería estar "
        "juzgando las asignaciones, y eso es 011-C3")


def test_las_reglas_discrepantes_de_Ci_quedan_registradas():
    """★ El patrón del «48,33 %» dentro del propio instrumento.

    El glosario y la Sección L definen ambos cuánto deduce cada infracción, y
    **no dicen lo mismo**:

        INF-03   0,05 en la matriz normativa · 0,20 en el glosario   (×4)
        INF-04   FIJA `Ci=0,50` · o resta 0,50 — son operaciones distintas
        piso     `MÁX(0,50; …)` · o `MAX(…, 0)`

    Y hay una cuarta, la más consecuente: la Sección L declara que el motor
    «abandona la valoración heurística» mientras la M declara que
    `Ci_Manual_2025` es el fallback vigente.

    ⚠️ HOY NINGUNA CAMBIA UN NÚMERO, porque no hay infracciones registradas.
    Son divergencias LATENTES. Perder su registro significa que se descubran
    el día que se active la primera infracción."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "El mismo factor, tres reglas distintas" in txt, (
        "desapareció el hallazgo de las reglas discrepantes")
    assert "otra operación" in txt, (
        "se perdió que INF-04 FIJA en vez de restar. Tratarlo como diferencia "
        "de formato oculta que el resultado es distinto")
    assert "nunca puede anular una meta" in txt, (
        "desapareció la consecuencia del piso 0,50: con él, C_i no puede "
        "llevar una meta a cero, y eso cambia qué es capaz de penalizar")
    assert "La divergencia es **latente**" in txt, (
        "se perdió que las reglas no se ejecutan hoy. Sin ese matiz, 011-C2 "
        "parecería estar denunciando un error activo en el ICPI publicado")


def test_una_definicion_de_glosario_no_es_participacion_en_el_calculo():
    """`Ci_Adaptativo` está definido —con su premio ×1,15 por
    `FONDO_CONCURSABLE`— y **no entra al numerador**.

    La única autoridad sobre qué participa del índice es la fórmula del
    numerador, no el glosario. Una capacidad declarada sin efecto no es lo
    mismo que una capacidad inexistente, y la diferencia importa: alguien
    podría citar el premio a fondos concursables como característica del
    motor."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Qué entra REALMENTE al índice" in txt
    assert "el numerador no lo referencia" in txt, (
        "se perdió que Ci_Adaptativo no participa del cálculo. Sin esa "
        "constancia, una definición de glosario se cita como comportamiento "
        "del motor")


def test_011C2_reconstruye_y_no_dictamina():
    """El límite de alcance, y el que `009` aprendió a la fuerza.

    Que una semántica resulte confusa, solapada o calibrada al revés es un
    HECHO que `011-C2` registra. Si eso invalida el constructo lo juzga
    `011-C4`. Un expediente que reconstruye y de paso absuelve o condena deja
    al dictamen sin nada que decidir."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "Reconstruir el significado no es aprobarlo ni condenarlo" in txt, (
        "011-C2 dejó de declarar su límite de alcance")
    assert "**No se afirma cuál de las tres es la correcta.**" in txt, (
        "se perdió la abstención sobre qué regla es la vigente. Elegir una "
        "aquí sería que la reconstrucción resuelva lo que 011-C3 debe "
        "justificar documentalmente")
    for destino in ("`011-C3`", "`011-C4`"):
        assert destino in txt, (
            f"desapareció la entrega a {destino}. Una cuestión abierta sin "
            f"dueño se convierte en una cuestión olvidada")
