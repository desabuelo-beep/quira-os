# -*- coding: utf-8 -*-
"""
tests/test_mapa_maestro.py — el mapa de frentes no se queda atrás
════════════════════════════════════════════════════════════════════════════════
Javo lo pidió con una razón concreta: *«para que no nos pase nuevamente volver a
hacer refactor porque no recordamos»*. No había un artefacto que dijera qué
frentes hay, en qué orden y qué depende de qué — vivía en la cabeza del director
y disperso en cinco documentos.

⚠️ Y UN MAPA DE ESTADO ESCRITO A MANO ES EL PROBLEMA QUE VIENE A RESOLVER. Se
desactualiza en dos semanas, se sigue citando, y quien lo lea creerá que sabe
dónde está el proyecto. Es el patrón del «48,33 %» aplicado a la hoja de ruta,
y sería el peor sitio donde cometerlo.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_MAPA = RAIZ / "docs" / "architecture" / "GM-OMEGA_MAPA_MAESTRO.md"
_SCRIPT = RAIZ / "scripts" / "gm_omega" / "mapa_maestro.py"
_BOOT = RAIZ / "governance" / "BOOT.md"


def test_el_mapa_se_deriva_y_lo_declara():
    """Sin esta declaración, el primero que quiera actualizar un estado lo
    editará a mano — y a partir de ahí el mapa dirá lo que alguien recordaba,
    no lo que el repositorio contiene."""
    assert _SCRIPT.exists(), "desapareció el generador del mapa maestro"
    txt = _MAPA.read_text(encoding="utf-8")
    assert "DERIVADO — no editar a mano" in txt
    assert "mapa_maestro.py" in txt, (
        "el mapa no dice quién lo genera: sin eso nadie sabe cómo rehacerlo")


def test_el_estado_sale_de_las_fuentes_vivas_no_del_script():
    """La mitad que hace fiable al mapa: las deudas, la doctrina y las pruebas
    NO se cuentan a mano en el script — se leen de `deuda.py`, `doctrina.py` y
    `tests/`. Lo único declarado es la SECUENCIA, que es un juicio."""
    fuente = _SCRIPT.read_text(encoding="utf-8")
    for viva in ("from app.agents.deuda import deudas",
                 "from app.agents.doctrina import doctrina"):
        assert viva in fuente, (
            f"el mapa dejó de leer una fuente viva (`{viva}`). Si el estado "
            f"pasa a estar escrito en el script, el mapa deja de reflejar el "
            f"repositorio y empieza a reflejar la memoria de quien lo editó")
    assert 'rglob("test_*.py")' in fuente, (
        "el recuento de pruebas dejó de derivarse del directorio de tests")


def test_las_dependencias_declaran_que_bloquea_a_que():
    """Un mapa que sólo lista tareas no evita repetir trabajo: lo que lo evita
    es saber qué se puede hacer HOY y qué espera a qué.

    ⚠️ Y la corrección que costó una vuelta: `R0` y `R1` NO dependen de `011`.
    Esta dirección lo tuvo mal —«011 antes que R2» era demasiado grueso—; son
    diagnóstico y lo ALIMENTAN. Sólo `R2` espera."""
    txt = _MAPA.read_text(encoding="utf-8")
    assert "AHORA, en paralelo" in txt, (
        "desapareció el bloque de lo que puede avanzar sin bloqueo. Sin él, un "
        "frente bloqueado se confunde con un frente parado")
    assert "`R0` y `R1` NO dependen de `011`" in txt, (
        "se perdió la corrección de la secuencia: R0 y R1 son diagnóstico y "
        "alimentan a 011; sólo R2 espera al dictamen")
    for etapa in ("008", "009", "010", "011", "R0", "R1", "R2", "T6"):
        assert etapa in txt, f"la etapa `{etapa}` desapareció del mapa"


def test_boot_lleva_al_mapa():
    """`BOOT.md` es la única fuente viva de arranque. Un mapa maestro que no se
    alcanza desde ahí es un documento que nadie abrirá en la sesión siguiente —
    y entonces no resuelve el problema que motivó escribirlo."""
    boot = _BOOT.read_text(encoding="utf-8")
    assert "GM-OMEGA_MAPA_MAESTRO.md" in boot, (
        "BOOT dejó de apuntar al mapa maestro. Sin esa ruta, el próximo "
        "arranque vuelve a reconstruir el estado de memoria, que es justo lo "
        "que Javo pidió evitar")


def test_ninguna_etapa_se_declara_cerrada_sin_custodio():
    """Regla 1 del mapa. Una etapa `✅` sin prueba que la fije acredita cero por
    no existir — es el defecto que `D-004` documentó en el propio CI, donde un
    gate verde certificaba un corpus que nunca había mirado.

    ⚠️ SE VERIFICA LA PROPIEDAD MEDIBLE: que cada frente con etapas cerradas
    tenga al menos un archivo de pruebas asociado. No demuestra que el custodio
    cubra la etapa concreta — eso exige leerlo — y por eso la regla queda además
    escrita en el documento, para quien venga después."""
    from scripts.gm_omega.mapa_maestro import _ETAPAS, _HECHO

    cerradas = {f for f, _e, _t, est, _n in _ETAPAS if est == _HECHO}
    assert cerradas, "ninguna etapa figura como cerrada: revisar el mapa"

    tests = " ".join(p.name for p in (RAIZ / "tests").rglob("test_*.py"))
    for frente, marca in (("GM-Ω", "gm_omega"), ("TF", "terminologia")):
        if frente in cerradas:
            assert marca in tests, (
                f"el frente {frente} tiene etapas cerradas y no hay pruebas "
                f"que las fijen. Una etapa cerrada sin custodio acredita cero "
                f"por no existir")

    txt = _MAPA.read_text(encoding="utf-8")
    assert "Ningún frente se cierra sin custodio" in txt
