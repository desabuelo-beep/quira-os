# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_serie_motor.py — GM-Ω-ICPI-011-C3R · serie temporal
════════════════════════════════════════════════════════════════════════════════
`011-C3` declaró `NO DETERMINABLE` la razón de tres transformaciones de `C_i`.
Después Javo señaló —como paréntesis, dudando si era necesario— una carpeta con
la historia del proyecto. Al medirla aparecieron **83 versiones fechadas del
Gold Master** que `C3` no había examinado.

★ LO QUE LA SERIE DEMOSTRÓ

    25-abr-2026   última versión SIN el mecanismo determinista   58 hojas
    27-abr-2026   fecha declarada en H01!A94
    29-abr-2026   primera versión CON el mecanismo               72 hojas

    Y entran JUNTOS: mecanismo · pesos 0,05/0,10/0,15 · piso 0,50 ·
    fallback Ci_Manual_2025 · Sección L · Sección M

`C_i` **no derivó: fue refactorizado en un solo acto de diseño**, y la fecha que
el autor declaró cae dentro de la ventana — corroborada por evidencia
independiente.

⚠️ Y EL LÍMITE QUE NO SE CRUZA. La serie demuestra CUÁNDO y QUÉ. No demuestra
POR QUÉ. Que cuatro cosas entren juntas hace **plausible** una decisión
deliberada; plausible no es demostrado, y confundirlos sería `DOC-009`.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_ICPI_SERIE_MOTOR_011C3R.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "serie_temporal_motor.py"


def test_la_serie_es_lectura_pura():
    """Ochenta y dos libros abiertos, ninguno modificado. Y no se toca el Gold
    Master vigente: la serie son copias históricas en disco."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert ".save(" not in fuente, "C3R intenta escribir en un libro"
    assert "data_only=False, read_only=True" in fuente, (
        "los libros dejaron de abrirse en modo lectura")
    txt = _DOC.read_text(encoding="utf-8")
    assert "27,4582 %" in txt, "se perdió la constancia del baseline congelado"


def test_la_reapertura_no_invalida_ni_confirma_por_defecto():
    """★ `DOC-031` · la formulación que evita los dos extremos.

    Decir «`C3` no usó la serie, luego `C3` está incompleto» sería demasiado
    fuerte y prejuzgaría. La formulación forense es que `C3` se ejecutó sobre
    el corpus **disponible**, y después apareció un corpus externo relevante
    que no formó parte de su universo de revisión — así que se abre una
    **verificación de sensibilidad documental**.

    ⚠️ EL RESULTADO PODÍA SER CUALQUIERA: sin cambio, parcial o reabierto. Fue
    el intermedio, y eso hay que decirlo tal cual: `C3` **no se invalidó, se
    precisó**."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "verificación de sensibilidad documental" in txt, (
        "desapareció la formulación forense de la reapertura. Sin ella, "
        "revisar una conclusión cerrada se lee como desautorizarla")
    assert "No prejuzga el resultado" in txt, (
        "se perdió que la verificación podía terminar sin cambio. Una "
        "reapertura que da por hecho que encontrará algo no es una "
        "verificación: es una búsqueda de confirmación")
    assert "no se invalidan" in txt and "se **precisan**" in txt, (
        "el expediente dejó de declarar qué le pasó a C3. Ni invalidado ni "
        "confirmado: precisado, que es el tercer resultado")


def test_el_corte_queda_fechado_y_corrobora_la_declaracion():
    """★ El hallazgo. La ventana del cambio se acota a cuatro días, y la fecha
    que el autor declaró en `H01!A94` **cae dentro**.

    Eso convierte una declaración del autor en un hecho corroborado por
    evidencia independiente — que es exactamente lo que `DOC-024` pedía y que
    en `011-C2` no se pudo hacer."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "última versión **sin** el mecanismo determinista" in txt
    assert "primera versión **con** el mecanismo determinista" in txt
    assert "cae dentro de la ventana" in txt, (
        "se perdió la corroboración. Es lo que eleva `H01!A94` de declaración "
        "del autor a hecho verificado contra una fuente independiente")
    assert "2026-04-27" in txt, (
        "desapareció la fecha declarada contra la que se contrasta")


def test_el_cambio_fue_un_acto_unico_y_eso_no_prueba_su_causa():
    """★ Lo que la serie demuestra, y lo que sigue sin demostrar.

    Mecanismo, pesos, piso, fallback y las dos secciones de `H01` entran en la
    **misma versión**. No hay pesos intermedios que se ajustaran después, ni un
    piso añadido más tarde: **descarta la calibración iterativa**. Y el libro
    pasa de 58 a 72 hojas — una refactorización mayor, no un ajuste.

    ⚠️ PERO LA CAUSA SIGUE SIN CONSTAR. Que cuatro cosas entren juntas hace
    plausible una decisión deliberada y única. Plausible no es demostrado. El
    resultado exacto es:

        SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA

    Si esa segunda mitad se pierde, la serie se leerá como si explicara el
    porqué — y eso es inferir la intención desde el resultado, `DOC-009`."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "no derivó: fue REFACTORIZADO en un solo acto de diseño" in txt, (
        "desapareció el hallazgo central de C3R")
    assert "descarta la hipótesis de calibración iterativa" in txt, (
        "se perdió lo que la simultaneidad permite descartar")
    assert "SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA" \
           in txt, (
        "desapareció el estado exacto del resultado. Sin esa fórmula, «sabemos "
        "cuándo» se desliza hacia «sabemos por qué»")
    assert "plausibilidad **no es una demostración**" in txt, (
        "se perdió la salvedad de DOC-009. La simultaneidad sugiere una "
        "decisión deliberada; no la prueba")


def test_el_ruido_de_lectura_no_se_cuenta_como_transicion():
    """La disciplina que hace fiable la serie.

    Algunos libros se guardaron con valores en vez de fórmulas, y entonces el
    conteo de factores lee `0` sin que el motor haya cambiado. Una transición
    que va y vuelve el mismo día, con todas las demás propiedades intactas,
    **es un artefacto de lectura**.

    ⚠️ Contarla sería FABRICAR GENEALOGÍA — inventar un cambio de diseño que
    nunca ocurrió, en un expediente cuyo objeto es reconstruir cambios
    reales."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "ruido de lectura" in txt, (
        "desapareció el filtro de artefactos de lectura")
    assert "fabricar genealogía" in txt, (
        "se perdió por qué importa: un falso positivo aquí no es un error de "
        "conteo, es un cambio de diseño inventado")


def test_las_copias_se_deduplican_por_contenido():
    """82 archivos, 71 versiones únicas. Deduplicar por SHA-256 evita leer el
    mismo libro varias veces y —lo que importa— **evita contar una copia como
    una transición**: el mismo contenido con otro nombre y otra fecha de
    archivo parecería un cambio y no lo es."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    assert "sha256" in fuente.lower(), (
        "la deduplicación por contenido desapareció")
    txt = _DOC.read_text(encoding="utf-8")
    assert "únicos por contenido" in txt
    assert "copias exactas" in txt, (
        "se perdió la constancia de cuántos archivos eran duplicados")
