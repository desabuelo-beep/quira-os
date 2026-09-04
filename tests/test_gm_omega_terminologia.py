# -*- coding: utf-8 -*-
"""
tests/test_gm_omega_terminologia.py — GM-Ω · Terminology Freeze `T1-T2`
════════════════════════════════════════════════════════════════════════════════
El inventario terminológico existe porque un nombre se propagó por 67 archivos
sin que nadie pudiera decir qué tipo de objeto era. Estas pruebas fijan las dos
mitades del ejercicio:

    · que la clasificación siga siendo un JUICIO con autoridad, no una
      inferencia desde el patrón de uso (`DOC-009`);
    · que la etapa NO toque código mientras el vocabulario no esté decidido.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "GM-OMEGA_TERMINOLOGIA_T1-T2.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "terminologia_quira.py"


def test_todo_nombre_propio_declara_su_categoria_ontologica():
    """DOC-013 · la pregunta del colega, vuelta prueba:

        ¿Qué tipo de objeto QUIRA soy?

    Cada nombre del inventario debe responderla. El que no puede queda en
    `SIN_CATEGORÍA` — que **no es un error de la tabla, es el hallazgo**: un
    concepto que se propagó sin cumplir una función verificable.

    ⚠️ SE VERIFICA QUE LA PREGUNTA SIGA HECHA A TODOS, no que las respuestas
    sean correctas. Que `AVEP` esté sin categoría es hoy el estado real; el día
    que `T6` lo deprecie o le encuentre función, esta prueba lo acompañará."""
    from scripts.gm_omega.terminologia_quira import _CATEGORIAS, _INVENTARIO

    assert _INVENTARIO, "el inventario terminológico quedó vacío"
    for nombre, cat, autoridad, _ in _INVENTARIO:
        assert cat in _CATEGORIAS, (
            f"`{nombre}` tiene la categoría «{cat}», que no está en la "
            f"taxonomía. Inventar una categoría para acomodar un nombre es "
            f"exactamente la inflación que DOC-013 prohíbe")
        assert autoridad, (
            f"`{nombre}` no declara qué autoridad lo define. Un nombre sin "
            f"autoridad es un nombre que nadie puede cambiar ni retirar")

    sin_cat = [n for n, c, *_ in _INVENTARIO if c == "SIN_CATEGORÍA"]
    assert "AVEP" in sin_cat, (
        "`AVEP` dejó de estar SIN_CATEGORÍA. Si se le encontró una función "
        "verificable, hay que declarar cuál y con qué autoridad; si se retiró, "
        "hay que sacarlo del inventario vivo y conservarlo en la genealogía "
        "histórica. Ninguna de las dos cosas se hace en silencio")


def test_la_etapa_de_vocabulario_no_toca_codigo():
    """La regla de secuencia: `T1-T5` deciden el vocabulario, `T6` ejecuta.

    Cambiar código mientras el vocabulario está en discusión sería la misma
    prisa que produjo el problema que este inventario documenta — AVEP se
    convirtió en fórmula porque alguien necesitaba aplicarlo ya.

    ⚠️ SE MIDE LA PROPIEDAD: el script sólo lee y escribe SU documento."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    for prohibido in ("os.remove", "shutil.", "unlink(", "rmtree"):
        assert prohibido not in fuente, (
            f"el inventario terminológico usa `{prohibido}`: esta etapa "
            f"INVENTARIA, no ejecuta. T6 es otra cosa y va después")
    assert fuente.count("write_text") == 1, (
        "el script escribe en más de un sitio: sólo debe producir su propio "
        "documento derivado")


def test_el_documento_declara_lo_que_NO_decide():
    """La mitad que suele faltar en un inventario: qué queda pendiente y por qué.

    Sin ella, un lector futuro puede leer la tabla como si fuera la decisión
    tomada — y renombrar `ICPI` o borrar `AVEP` creyendo que ejecuta un acuerdo
    que nadie tomó."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "## Lo que este documento NO decide" in txt
    for pendiente in ("No renombra nada", "No elimina AVEP",
                      "No construye el baremo parametrizable"):
        assert pendiente in txt, f"desapareció la reserva «{pendiente}»"


def test_ICPI_conserva_el_nombre_de_la_tesis():
    """El nombre del constructo no se toca, y la razón es de trazabilidad, no de
    gusto: «Índice de Congruencia Programática e Intersistémica» es el nombre de
    la tesis —el documento con fecha anterior a todo Gold Master conservado— y
    **el único anclaje documental verificable que tiene el ICPI**.

    Renombrarlo destruiría la genealogía que 001-007 reconstruyó, en una
    auditoría cuyo objeto es precisamente la trazabilidad."""
    from scripts.gm_omega.terminologia_quira import _INVENTARIO
    icpi = [f for f in _INVENTARIO if f[0] == "ICPI"]
    assert icpi, "`ICPI` desapareció del inventario"
    _, cat, autoridad, nota = icpi[0]
    assert cat == "INDICADOR", (
        f"`ICPI` pasó a categoría «{cat}». No es el centro de QUIRA: es un "
        f"indicador nuclear del Gold Master, y confundirlo con el eje "
        f"ontológico del sistema es el error que ya cometimos con AVEP")
    assert "tesis" in autoridad.lower(), (
        "`ICPI` dejó de citar la tesis como autoridad. Es su único anclaje "
        "documental anterior a cualquier Gold Master conservado")
    assert "Congruencia Programática e Intersistémica" in nota
