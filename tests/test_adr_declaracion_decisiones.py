# -*- coding: utf-8 -*-
"""
tests/test_adr_declaracion_decisiones.py — los cinco ADR de `011-C4`
════════════════════════════════════════════════════════════════════════════════
`011-C4` concluyó que **cinco decisiones sostienen el ICPI y ninguna está
declarada como decisión** — se presentan como si fueran propiedades del
fenómeno. Estos cinco `ADR` las declaran.

    ADR-054 · D1  multiplicatividad
    ADR-055 · D2  V_i multiplicativo · el más importante
    ADR-056 · D3  pesos de deducción
    ADR-057 · D4  piso 0,50
    ADR-058 · D5  objeto de AVEP

★ SON CINCO, NO CUATRO. Las decisiones no tienen el mismo tipo epistemológico:
agruparlas haría que una justifique a otra.

⚠️ Y CADA UNO LLEVA LOS DIEZ CAMPOS OBLIGATORIOS. Sin ellos —en particular sin
«qué es inferencia», «qué permanece NO DETERMINABLE» y «condición objetiva para
revisarla»— un ADR se convierte en una **justificación retrospectiva**: un texto
que explica por qué lo que ya se hizo estaba bien.

⚠️ NINGUNO CAMBIA EL MOTOR. Declarar no es corregir, y `DOC-029` fija el orden:
observar → clasificar → justificar → diseñar la migración → ejecutar.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_ADR = RAIZ / "docs" / "adr"
_LOS_CINCO = {
    "D1": "ADR-054_D1_Arquitectura_Multiplicativa_del_ICPI.md",
    "D2": "ADR-055_D2_Semantica_de_la_Ausencia_de_Evidencia.md",
    "D3": "ADR-056_D3_Pesos_de_Deduccion_de_Ci.md",
    "D4": "ADR-057_D4_Piso_Minimo_de_Ci.md",
    "D5": "ADR-058_D5_Objeto_del_Baremo_AVEP.md",
}

# Los diez campos que impiden que un ADR sea una justificación retrospectiva.
_CAMPOS = [
    "1 · Decisión vigente",
    "2 · Fenómeno que pretende representar",
    "3 · Unidad afectada",
    "4 · Evidencia que la sostiene",
    "5 · Alternativas consideradas",
    "6 · Qué está DEMOSTRADO",
    "7 · Qué es INFERENCIA",
    "8 · Qué permanece NO DETERMINABLE",
    "9 · Consecuencias de mantenerla",
    "10 · Condición objetiva para revisarla",
]


def test_existen_los_cinco():
    """Cinco decisiones, cinco declaraciones. Agrupar dos decisiones de
    distinto tipo epistemológico en un solo ADR haría que una justifique a la
    otra por contigüidad."""
    for d, nombre in _LOS_CINCO.items():
        assert (_ADR / nombre).exists(), (
            f"falta el ADR de `{d}`. C4 identificó cinco decisiones sin "
            f"declarar; con cuatro ADR, una queda sin declarar")


def test_cada_ADR_lleva_los_diez_campos():
    """★ Los diez campos son la diferencia entre declarar y justificar.

    Los tres que más cuesta escribir son los que más importan:

        7 · qué es INFERENCIA
        8 · qué permanece NO DETERMINABLE
        10 · condición objetiva para revisarla

    Sin el 7 y el 8, el ADR presenta como demostrado lo que se supone. Sin el
    10, la decisión queda declarada **y congelada** — que es el sesgo
    conservador que `DOC-027` corrige."""
    for d, nombre in _LOS_CINCO.items():
        txt = (_ADR / nombre).read_text(encoding="utf-8")
        for campo in _CAMPOS:
            assert campo in txt, (
                f"al ADR de `{d}` le falta el campo «{campo}». Sin los diez, "
                f"un ADR se convierte en una justificación retrospectiva")


def test_ninguno_se_declara_aprobado_por_la_maquina():
    """`ADR-035 §5`: la IA propone, el humano valida.

    Un ADR que naciera `APROBADO` sin sello de Javo sería exactamente la caja
    negra que la carta de rearquitectura prohíbe: la máquina ratificando sus
    propias propuestas."""
    for d, nombre in _LOS_CINCO.items():
        txt = (_ADR / nombre).read_text(encoding="utf-8")
        m = re.search(r"^status:\s*(.+)$", txt, re.M)
        assert m, f"el ADR de `{d}` no declara `status`"
        assert "PROPUESTO" in m.group(1), (
            f"el ADR de `{d}` nace con status «{m.group(1).strip()}». Debe "
            f"nacer PROPUESTO: la IA propone, el humano valida")
        assert "La IA propone; el humano valida" in txt


def test_ninguno_cambia_el_motor():
    """Declarar no es corregir. `DOC-029` fija el orden y estos ADR están en
    la fase de **justificar**, no en la de ejecutar."""
    for d, nombre in _LOS_CINCO.items():
        txt = (_ADR / nombre).read_text(encoding="utf-8")
        assert "no cambia el motor" in txt.lower(), (
            f"el ADR de `{d}` dejó de declarar que no interviene el motor. "
            f"Un ADR de declaración que además cambia algo es una migración "
            f"sin diseño")


def test_D1_dice_las_dos_mitades():
    """El veredicto de `D1` tiene que decir **ni necesaria ni incorrecta**.

    Perder cualquiera de las dos mitades convierte un dictamen en sentencia:
    con sólo la primera parece una condena; con sólo la segunda, un aval."""
    txt = (_ADR / _LOS_CINCO["D1"]).read_text(encoding="utf-8")
    assert "No se demuestra necesaria **ni incorrecta**" in txt, (
        "D1 perdió una de sus dos mitades")
    assert "elección metodológica" in txt and "no una propiedad derivada" in txt


def test_D2_conserva_las_tres_proposiciones():
    """★ El ADR más importante de los cinco: es el único que toca el principio
    rector del sistema.

        1. «el fenómeno NO OCURRIÓ»        → sobre el mundo
        2. «no hay evidencia suficiente»   → sobre el conocimiento
        3. «la unidad no puede contribuir» → regla metodológica

    La 3 es legítima; **no es consecuencia lógica de la 2**. Y `V_i = 0` no
    significa que el fenómeno no ocurriera: significa que la unidad no puede
    aportar congruencia **acreditada**."""
    txt = (_ADR / _LOS_CINCO["D2"]).read_text(encoding="utf-8")
    assert "No es consecuencia lógica de la `2`" in txt, (
        "D2 perdió la distinción central: una regla metodológica legítima no "
        "se deduce del estado del conocimiento")
    assert "congruencia **acreditada**" in txt
    assert "31,4883" in txt or "31.4883" in txt, (
        "desapareció la elasticidad medida: la semántica de la ausencia de "
        "evidencia mueve el índice +4,03 pp")
    assert "no defendible" in txt, (
        "se perdió que presumir cumplimiento sin evidencia contradice el "
        "principio rector — se midió sólo para acotar el rango")


def test_D3_y_D4_declaran_su_condicion_de_activacion():
    """Ambas son **latentes**: hoy no mueven el índice porque no hay
    infracciones registradas.

    ⚠️ Y por eso mismo la condición de revisión es la que es: **antes de
    registrar la primera infracción**. Aplazarla sería dejar la decisión para
    el momento en que ya no pueda tomarse con calma."""
    for d in ("D3", "D4"):
        txt = (_ADR / _LOS_CINCO[d]).read_text(encoding="utf-8")
        assert "Efecto hoy: ninguno" in txt, (
            f"el ADR de `{d}` dejó de declarar que hoy no mueve el índice")
        assert "primera infracción" in txt, (
            f"el ADR de `{d}` perdió su condición objetiva de revisión")
        assert "D-013" in txt, (
            f"el ADR de `{d}` dejó de apuntar a la divergencia latente que "
            f"hay que resolver antes de la revisión")


def test_D4_enuncia_su_tesis_sustantiva():
    """`D4` parece el más pequeño de los cinco —un número— y es el que más
    afirma:

        incluso acumulando infracciones existe un mínimo de contribución
        institucional que debe preservarse

    Puede ser correcto. Pero es una **tesis**, y hasta este ADR nadie la había
    enunciado como tal — así que no podía discutirse."""
    txt = (_ADR / _LOS_CINCO["D4"]).read_text(encoding="utf-8")
    assert "tesis sustantiva" in txt
    assert "no es un parámetro técnico" in txt.lower(), (
        "D4 volvió a presentarse como un ajuste de valor")
    assert "acota cuánto puede penalizar el sistema" in txt, (
        "desapareció la consecuencia no declarada: un GAD con desacato firme "
        "conserva la mitad de su C_i")


def test_D5_no_propone_escala_antes_de_declarar_objeto():
    """`DOC-012` · un porcentaje no tiene significado semántico por sí mismo.

    Este ADR **no propone umbrales**: abre la pregunta de qué fenómeno
    clasifica `AVEP`. Elegir umbrales antes de elegir objeto es elegir al
    azar — y elegirlos desde el resultado que producen es `DOC-009`."""
    txt = (_ADR / _LOS_CINCO["D5"]).read_text(encoding="utf-8")
    assert "no se puede validar una escala antes de declarar el fenómeno" \
           in txt.lower(), (
        "D5 perdió la regla que lo ordena")
    assert "NO DECLARADO" in txt, (
        "el campo del fenómeno dejó de declararse vacío, que es el hallazgo")
    assert "no se elige umbral desde el resultado que produce" in txt, (
        "desapareció la prohibición de DOC-009 aplicada a los umbrales")
    assert "D-012" in txt, "D5 dejó de vincularse con la deuda que desbloquea"
