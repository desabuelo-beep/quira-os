# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_gaming.py — GM-Ω-ICPI-009 · el incentivo cambia de signo
════════════════════════════════════════════════════════════════════════════════
009 preguntó si el ICPI puede mejorarse sin mejorar la realidad. La primera
respuesta —«no: ejecutar rinde 6,6 veces más que documentar»— era del corte de
abril, y la simulación de cierre de año la desmintió con los propios datos del
informe.

    abril   (T=0,30)   DOC  +7,84   MAT +52,10   → MATERIAL
            (T=0,75)   DOC +13,74   MAT +18,95   → MATERIAL
    cierre  (T=0,90)   DOC +15,72   MAT  +7,61   → DOCUMENTAL

⚠️ El hallazgo no es un sí ni un no: **la ventana de gaming tiene fecha**.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_GAMING_009.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "gaming_icpi.py"


def test_el_analisis_no_toca_el_gold_master():
    """009 mide un incentivo; no recalcula ni corrige nada. Y sus cifras son
    contrafactuales: ninguna puede citarse fuera de la auditoría (`DOC-010`)."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "009 intenta escribir en el Excel"
    txt = _DOC.read_text(encoding="utf-8")
    for etiqueta in ("MATEMÁTICAMENTE REPRODUCIBLE",
                     "METODOLÓGICAMENTE CONTRAFACTUAL",
                     "NO AUTORIZADA PARA PUBLICACIÓN"):
        assert etiqueta in txt, f"desapareció la etiqueta «{etiqueta}»"


def test_la_inversion_del_incentivo_no_se_pierde():
    """★ El hallazgo de 009, y el que esta dirección estuvo a punto de no ver.

    La primera conclusión fue «el incentivo está alineado: ejecutar rinde 6,6×
    más». Era cierta **para abril**. Al simular el cierre del ejercicio el signo
    se invierte: con `T` alto el margen material se agota, mientras las metas con
    `V=0` siguen valiendo mucho —porque `V=0` anula la meta entera—.

    ⚠️ Si esto se pierde, vuelve un veredicto binario y falso: «el ICPI no es
    gameable». Lo correcto es que **es gameable en una ventana temporal
    concreta**, y eso sí se puede vigilar."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "EL INCENTIVO SE INVIERTE" in txt, (
        "desapareció el hallazgo central. Sin él, 009 se lee como un aprobado "
        "general del motor, y el corte de abril no autoriza esa conclusión")
    assert "La ventana de gaming tiene fecha" in txt, (
        "se perdió la formulación accionable: no es gameable o no, es gameable "
        "en un tramo del año")
    assert "propiedad estructural" in txt, (
        "la inversión dejó de declararse estructural. Si se lee como un efecto "
        "de los datos de este año, nadie la vigilará el año que viene")


def test_009_no_convierte_un_incentivo_en_una_acusacion():
    """La línea que separa medir de acusar.

    009 mide un incentivo estructural, **no una conducta**. Y documentar no es
    ilegítimo: aportar evidencia a LOTAIP o al CPCCS es una obligación legal, y
    que el índice la premie es correcto."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "No demuestra que nadie haya hecho esto" in txt, (
        "desapareció la salvedad. Un incentivo medido leído como conducta "
        "probada es una acusación sin evidencia, y el canon lo prohíbe")
    assert "es una obligación legal" in txt, (
        "se perdió que documentar es legítimo y obligatorio. Sin eso, 009 "
        "parecería sugerir que aportar evidencia es hacer trampa")


def test_009_entrega_a_011C4_sin_dictaminar():
    """009 alimenta el dictamen; no lo emite. Entrega a `011-C4` un argumento
    de doble filo —a favor de conservar la multiplicatividad durante la ventana
    operativa, a vigilar por su inversión— y una pregunta abierta que no
    responde: si el índice debería tener un incentivo constante."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "011-C4" in txt
    assert "¿debería el índice tener un incentivo constante?" in txt, (
        "desapareció la pregunta que 009 deja abierta. Cerrarla aquí sería "
        "que un análisis de sensibilidad dictamine sobre el constructo")
