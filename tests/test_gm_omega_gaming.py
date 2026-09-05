# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_gaming.py — GM-Ω-ICPI-009 · el incentivo cambia de signo
════════════════════════════════════════════════════════════════════════════════
009 preguntó si el ICPI puede mejorarse sin mejorar la realidad. La primera
respuesta —«no: ejecutar rinde 6,6 veces más que documentar»— era del corte de
abril, y la simulación con la ejecución alta la desmintió con los propios datos.

    T = 0,30   DOC  +5,81   MAT +52,10   → material ≈ 9,0×
    T = 0,75   DOC +10,92   MAT +18,95   → material ≈ 1,7×
    T = 0,90   DOC +12,64   MAT  +7,61   → SE INVIERTE, documental ≈ 1,7×

⚠️ EL EJE ES `T`, NO EL CALENDARIO. 009 movió `T` de golpe para todas las metas;
eso no es cómo avanza un ejercicio presupuestario. Rotular el eje con meses
—«enero-abril», «cierre»— le atribuye a la simulación una escala temporal que
no tiene, y esta dirección lo hizo dos veces antes de retirarlo.

⚠️ Y 009 NO RESUELVE QUÉ ES `C_i`. Lo clasificó primero como DOCUMENTAL (error
propio) y luego como MATERIAL (hipótesis de Javo, plausible pero no demostrada).
El estado correcto es PENDIENTE: `011-C2/C3` existe precisamente para reconstruir
la semántica de cada factor. Si un análisis de incentivos la fija, habrá resuelto
la pregunta ontológica que debía auditarlo a él.

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
    más». Era cierta **para un valor de `T`**. Al simular la ejecución alta el
    signo se invierte: con `T` cerca de 1 el margen material se agota, mientras
    las metas con `V=0` siguen valiendo mucho —porque `V=0` anula la meta
    entera—.

    ⚠️ Si esto se pierde, vuelve un veredicto binario y falso: «el ICPI no es
    gameable»."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "SUPERFICIE DE INCENTIVO ES DINÁMICA" in txt, (
        "desapareció el hallazgo central. Sin él, 009 se lee como un aprobado "
        "general del motor, y el corte de abril no autoriza esa conclusión")
    # ⚠️ La formulación se corrigió: «la ventana de gaming tiene fecha» era
    # retóricamente potente y epistemológicamente excesiva —009 no identificó el
    # momento real de inversión, sólo la diferencia entre escenarios discretos—.
    assert "puede invertirse hacia el cierre" in txt, (
        "se perdió la formulación exacta: la ventaja relativa DEPENDE DEL ESTADO "
        "temporal y PUEDE invertirse. Ni «es gameable» ni «tiene fecha»")
    assert "epistemológicamente demasiado fuerte" in txt, (
        "desapareció la constancia de que la formulación anterior era excesiva. "
        "Sin ella, alguien la reintroduce por parecer más contundente")


def test_el_eje_de_la_simulacion_es_T_y_no_el_calendario():
    """La corrección que esta dirección tuvo que hacer dos veces.

    El diagrama rotulaba sus tres escalones «ENERO-ABRIL / MITAD DE AÑO /
    CIERRE». Pero lo que 009 varió fue `T`, de golpe y para todas las metas a la
    vez. Un ejercicio presupuestario real no se comporta así, y ponerle meses al
    eje convierte una simulación paramétrica en un calendario que nadie midió.

    ⚠️ Es el mismo defecto que el «48,33 %»: un derivado narrativo que dice algo
    más preciso de lo que su fuente puede sostener."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "El eje es `T`, **no el calendario**" in txt, (
        "desapareció la advertencia. Sin ella el diagrama vuelve a leerse como "
        "una línea de tiempo, y 009 no midió ningún mes")
    for mes in ("ENERO-ABRIL", "MITAD DE AÑO"):
        assert mes not in txt, (
            f"volvió el rótulo temporal «{mes}» al diagrama: le atribuye a la "
            f"simulación una escala de calendario que no tiene")


def test_la_semantica_de_Ci_queda_abierta_para_011():
    """★ La corrección más importante de este cierre, y la que 009 no podía
    verse a sí mismo.

    `C_i` pasó por tres estados:

        DOCUMENTAL   error de esta dirección — inflaba el techo documental,
                     que es justamente el resultado que 009 mide
        MATERIAL     hipótesis de Javo: acta de entrega-recepción e impacto
                     verificado. Plausible, institucionalmente coherente…
                     y **no demostrada**
        PENDIENTE    ✅ el estado correcto

    ⚠️ EL RIESGO ES ESTRUCTURAL, no de redacción. `011-C2/C3` existe para
    reconstruir qué significa históricamente cada factor. Si `009` fija la
    semántica de `C_i`, entonces un análisis de comportamiento habrá resuelto
    por adelantado la pregunta ontológica sobre la variable que lo audita — y
    `011` heredará como premisa lo que tenía que juzgar."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert '"C": ("PENDIENTE"' in fuente, (
        "`C_i` volvió a clasificarse en una vía. No puede: mientras 011-C2/C3 "
        "no cierre su semántica, sumarlo a DOCUMENTAL o a MATERIAL altera el "
        "resultado de 009 con una hipótesis no demostrada")

    txt = _DOC.read_text(encoding="utf-8")
    assert "**REFUTADO** por el propio autor" in txt, (
        "se perdió la constancia de que la clasificación documental de C_i fue "
        "un error corregido por Javo. Sin ella, el error puede repetirse")
    assert "ni resuelve la semántica de `C_i`" in txt, (
        "el cierre de 009 dejó de declarar que no resuelve C_i. Ése es "
        "exactamente el límite de alcance que protege a 011")
    # `011-C2` resolvió la semántica y REFUTÓ la hipótesis. Lo que 009 sigue sin
    # poder fijar es la naturaleza del ESFUERZO, que depende de qué regla rija.
    assert "🔴 **REFUTADO** por `011-C2`" in txt, (
        "desapareció el resultado del contraste. La hipótesis de la entrega "
        "material no quedó pendiente: quedó refutada contra el instrumento, y "
        "el expediente debe decirlo")
    assert "esperar tuvo premio" in txt.lower(), (
        "se perdió la constancia de por qué la cautela importó: si 009 hubiera "
        "dado por buena la hipótesis, habría publicado como respuesta del motor "
        "una defensa que el motor no implementa")


def test_009_no_absuelve_ni_condena_la_arquitectura():
    """★ La frase que hubo que retirar, y por qué.

        ~~«La inversión al cierre no describe un motor mal diseñado.»~~

    Suena a matiz prudente y es **una absolución**. `009` mide una superficie de
    incentivo; no tiene competencia para dictaminar sobre la validez del diseño
    —ni en contra ni a favor—. Que la inversión simulada sea *compatible* con la
    dinámica real de la gestión pública ecuatoriana no determina que la
    arquitectura sea adecuada. Eso lo juzga `011-C4`.

    ⚠️ Un análisis que absuelve es tan inutilizable como uno que acusa: en ambos
    casos el dictamen ya está escrito antes de que empiece el peritaje."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no describe un motor mal diseñado" not in txt.replace(
        "~~«La inversión del incentivo al cierre **no describe un motor mal "
        "diseñado**: describe el momento del año en que la realidad "
        "institucional ecuatoriana concentra su presión.»~~", ""), (
        "volvió la absolución fuera de su tachado. 009 no puede declarar que "
        "el motor está bien diseñado")
    assert "no determina por sí misma que la arquitectura sea adecuada ni " \
           "inadecuada" in txt, (
        "desapareció la formulación forense. Sin ella, la compatibilidad con "
        "el fenómeno institucional se lee como validación del diseño")
    assert "FUERA DEL ALCANCE de 009" in txt, (
        "el dictamen dejó de declarar que la valoración de la arquitectura no "
        "le corresponde")


def test_la_ventaja_material_se_declara_acotada_al_escenario():
    """`+52,10` frente a `+5,81` es un hecho del corte de abril, no una
    propiedad del índice.

    La diferencia entre «en este escenario el techo material es ~9× el
    documental» y «el índice incentiva 9 veces más la ejecución» es toda la
    diferencia entre una medición y una teoría del comportamiento — y 009 sólo
    tiene la primera. No midió el coste de ninguna de las dos vías."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "En el escenario de abril analizado" in txt, (
        "se perdió el acotamiento al escenario. La cifra sola invita a leerse "
        "como propiedad atemporal de la fórmula, y no lo es")
    assert "Y sólo en ese escenario" in txt
    assert "un techo contrafactual no dice nada sobre qué es más barato" in txt, (
        "desapareció la salvedad de coste. Sin ella, «mayor techo» se convierte "
        "en «más rentable», que es una afirmación económica sin medición")


def test_009_no_convierte_un_incentivo_en_una_acusacion():
    """La línea que separa medir de acusar.

    009 mide un incentivo estructural, **no una conducta**. Y documentar no es
    ilegítimo: aportar evidencia a LOTAIP o al CPCCS es una obligación legal, y
    que el índice la premie es coherente con un constructo de congruencia."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "No demuestra que nadie haya hecho esto" in txt, (
        "desapareció la salvedad. Un incentivo medido leído como conducta "
        "probada es una acusación sin evidencia, y el canon lo prohíbe")
    assert "es una obligación legal" in txt, (
        "se perdió que documentar es legítimo y obligatorio. Sin eso, 009 "
        "parecería sugerir que aportar evidencia es hacer trampa")


def test_009_entrega_a_011C4_sin_dictaminar():
    """009 alimenta el dictamen; no lo emite. Entrega a `011-C4` dos entradas de
    signo opuesto y una pregunta que no responde — si el índice debería tener un
    incentivo constante— más la que formuló el colega y es más fina que «¿hay
    gaming?»: si el ICPI evalúa el **estado** de una meta en un momento del
    ciclo o la **integridad retrospectiva** de su materialización."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "011-C4" in txt
    assert "¿debería el índice tener un incentivo constante?" in txt, (
        "desapareció la pregunta que 009 deja abierta. Cerrarla aquí sería "
        "que un análisis de sensibilidad dictamine sobre el constructo")
    assert "integridad de todo su proceso de materialización" in txt, (
        "se perdió la pregunta que reencuadra 011-C4. Sin ella el dictamen "
        "vuelve a ser «¿hay gaming?», que es la pregunta pequeña")
