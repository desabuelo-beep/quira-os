# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_matriz.py — GM-Ω-ICPI-004/005 · la matriz no se escribe
════════════════════════════════════════════════════════════════════════════════
El colega exigió la trazabilidad celda a celda:

> *«El patrón por variable no sustituye la trazabilidad de las 150 celdas. […]
> Eso nos permitirá contestar, para cualquier meta: ¿por qué esta meta tiene
> exactamente este número? Y reconstruirlo sin mirar el ICPI final.»*

Tenía razón. La primera pasada comprimió las 150 celdas en 6 patrones —legítimo
mientras el patrón fuera idéntico, pero deja sin respuesta la pregunta concreta.

⚠️ Y LA MATRIZ NO SE ESCRIBIÓ A MANO, que es la otra mitad. Una tabla copiada
del Excel se queda atrás el día que el Excel cambia: es el patrón del «48,33 %»,
cometido dentro de la auditoría que lo persigue. Se DERIVA cada vez.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_MATRIZ = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_MATRIZ_004.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "matriz_procedencia_icpi.py"


def test_la_matriz_es_derivada_y_lo_declara():
    """Un artefacto derivado que no dice serlo invita a editarlo a mano, y el
    día que alguien lo haga dejará de reflejar el motor sin que nada avise."""
    assert _SCRIPT.exists(), "desapareció el generador de la matriz"
    txt = _MATRIZ.read_text(encoding="utf-8")
    assert "DERIVADO — no editar a mano" in txt
    assert "matriz_procedencia_icpi.py" in txt, (
        "la matriz no dice quién la genera: sin eso, nadie sabe cómo rehacerla")


def test_las_150_celdas_estan_una_por_una():
    """La exigencia del colega, fijada. 25 metas × 6 variables, cada una con su
    celda del Gold Master y su origen — no un patrón que las resuma."""
    txt = _MATRIZ.read_text(encoding="utf-8")
    celdas = txt.count("| `H12!")
    assert celdas == 150, (
        f"la matriz tiene {celdas} celdas y deben ser 150 (25 metas × 6 "
        f"variables). Si el motor cambió de tamaño, regenerar y actualizar esto")
    for var in ("P_i", "R_i", "V_i", "E_i", "T_i", "C_i"):
        assert txt.count(f"| `{var}` | `H12!") == 25, (
            f"{var} no aparece en las 25 metas")


def test_el_generador_no_escribe_en_el_gold_master():
    """Regla de Oro 1 y 4. La auditoría observa el motor; no lo toca. Se mide la
    PROPIEDAD —que sólo abra en lectura— y no la palabra: `read_only=True` en
    cada apertura, y ninguna llamada a `save`."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert fuente.count("load_workbook") == fuente.count("read_only=True"), (
        "hay una apertura del Gold Master que no es de sólo lectura")
    assert ".save(" not in fuente, "el generador intenta escribir en el Excel"


def test_sin_gold_master_la_matriz_no_se_inventa():
    """El tercer estado, aplicado al propio generador: si el motor no se
    resolvió, devuelve 2 —no determinable— en vez de producir una matriz vacía
    que parecería una matriz sin hallazgos.

    Es la misma distinción que `check_extraccion` tuvo que aprender el 02-sep:
    «no pude mirar» no es «miré y no había nada»."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "GOLD_MASTER_RESUELTO" in fuente, (
        "el generador dejó de comprobar si el motor se resolvió")
    assert "return 2" in fuente, (
        "desapareció el código de salida «no determinable»: sin él, no poder "
        "mirar se confundiría con no encontrar nada")


def test_el_hallazgo_de_E_i_lo_encuentra_el_propio_generador():
    """`E_i` es el único componente sin biografía: 25 literales sin fórmula ni
    fuente en el libro. Y no es una afirmación de la ficha — la produce el
    generador al leer el motor, así que se cae sola el día que `E_i` reciba una
    fórmula.

    ⚠️ Que se caiga sería la señal de que la deuda de trazabilidad se cerró."""
    txt = _MATRIZ.read_text(encoding="utf-8")
    literales = txt.count("LITERAL (sin origen declarado)")
    assert literales == 25, (
        f"hay {literales} celdas sin origen declarado y eran 25 (todas `E_i`). "
        f"Si BAJÓ, alguien le dio biografía a E_i y hay que actualizar la ficha; "
        f"si SUBIÓ, otra variable perdió la suya")
    # ⚠️ E_i estuvo clasificado como UNTRACEABLE y era afirmar más de lo medido.
    # Agotada la búsqueda —no deriva de `Competencia_GAD` ni de la entidad, pero
    # la TESIS sí define su regla (COOTAD 54 · NCI 200-04)— el estado correcto es
    # PARCIALMENTE_VERIFICADO: la regla existe; lo que falta en el libro es la
    # MODALIDAD de ejecución de cada meta. «Sin fuente declarada aquí» no es
    # «sin fuente».
    assert "PARCIALMENTE_VERIFICADO" in txt, (
        "el estado provisional de E_i dejó de declararse")
    assert "UNTRACEABLE" not in txt.split("## Las 150 celdas")[0].replace(
        "UNTRACEABLE             hay valor", ""), (
        "volvió a clasificarse E_i como UNTRACEABLE sin agotar la búsqueda")


def test_la_incoherencia_de_E_i_se_señala_sin_declararla_defecto():
    """La comprobación cruzada que pidió el colega: contrastar el valor asignado
    contra la regla de la tesis, dada la entidad que ejecuta la meta.

    Resultado: **5 de 6 metas ejecutadas por entidades adscritas** tienen `E_i`
    distinto del 0,75 que la regla pide para la delegación.

    ⚠️ Y NO SE DECLARA DEFECTO, que es la mitad importante. La entidad se infiere
    de la columna de `T_i` —el mejor proxy del libro— y la MODALIDAD real
    (directa · convenio · delegación) no consta en ninguna celda. Señalar dónde
    la regla documentada y el valor no concuerdan es medir; llamarlo error sería
    afirmar sobre lo que no se midió."""
    txt = _MATRIZ.read_text(encoding="utf-8")
    alertas = txt.count("adscrita) y la regla de la tesis pide")
    assert alertas == 5, (
        f"las metas con E_i incoherente pasaron de 5 a {alertas}. Si BAJÓ, "
        f"alguien alineó E_i con la regla o declaró la modalidad; si SUBIÓ, "
        f"apareció otra")
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "NO demuestra un defecto" in fuente or "NO es un defecto demostrado" in fuente, (
        "el generador dejó de declarar que la incoherencia no es un defecto "
        "probado: sin esa salvedad, una inferencia se leería como veredicto")


def test_ser_entidad_adscrita_no_determina_E_i():
    """DOC-008 · el principio que emergió de la corrección de Javo:

        QUIRA no debe penalizar la arquitectura administrativa legítima; debe
        penalizar la pérdida verificable de integridad, control o trazabilidad.

    Javo lo planteó primero —«castigar al GAD por derivar una obra a EP Aseo no
    es viable: es la misma institucionalidad»— y el colega lo formalizó. Una EP
    municipal puede ejecutar una obra MEJOR trazada que una dirección interna:

        adscrita  ≠  menor integridad
        delegada  ≠  menor desempeño

    Y armoniza `E_i` con el resto: si delegar debilitara la trazabilidad, `V_i`
    ya lo mediría —verifica el rastro REAL en los cuatro silos—. Penalizar por
    el organigrama sería meter **estructura institucional como proxy de
    desempeño**, e imputar por presunción donde el sistema exige evidencia.

    ⚠️ SE VERIFICA LA PROPIEDAD, no un valor concreto: que pertenecer a una
    entidad adscrita NO determine `E_i`. Basta con que alguna meta de adscrita
    tenga autonomía plena para demostrar que el motor no las castiga por serlo.

    Y esto NO afirma que la regla vigente sea correcta —su criterio está
    `NOT_DETERMINABLE` (§7-ter)—: afirma que la regla histórica, la que
    penalizaba el organigrama, ya no se aplica."""
    import re
    txt = _MATRIZ.read_text(encoding="utf-8")

    # Metas cuya línea de E_i menciona una entidad adscrita, con su valor.
    adscritas = []
    for m in re.finditer(r"\| `E_i` \| `H12![A-Z]+\d+` \| ([\d.]+) \| [^|]+\| ([^|]+)\|", txt):
        valor, ent = float(m.group(1)), m.group(2)
        if any(x in ent for x in ("Patronato", "Bomberos", "EP Aseo")):
            adscritas.append(valor)

    assert adscritas, (
        "no se localizó ninguna meta de entidad adscrita: cambió el formato de "
        "la matriz y esta prueba dejó de mirar lo que dice mirar")
    assert max(adscritas) == 1.0, (
        f"ninguna meta de entidad adscrita alcanza E_i = 1,0 (máximo {max(adscritas)}). "
        f"El motor volvió a penalizar el organigrama en vez de la pérdida "
        f"verificable de trazabilidad — y esa la mide `V_i`, no `E_i`")
    assert len(set(adscritas)) > 1, (
        "todas las metas de adscritas tienen el mismo E_i: ser adscrita volvió "
        "a determinar el valor")
