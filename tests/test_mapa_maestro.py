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

import pytest
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
    assert "EN PARALELO" in txt, (
        "desapareció el bloque de lo que puede avanzar sin bloqueo. Sin él, un "
        "frente bloqueado se confunde con un frente parado")
    assert "`R0` y `R1` NO dependen de `011`" in txt, (
        "se perdió la corrección de la secuencia: R0 y R1 son diagnóstico y "
        "alimentan a 011; sólo R2 espera al dictamen")
    for etapa in ("008", "009", "010", "011", "R0", "R1", "R2", "T6"):
        assert etapa in txt, f"la etapa `{etapa}` desapareció del mapa"


def test_la_genealogia_habilita_a_decidir_no_obliga_a_repetir():
    """★ DOC-027 · el encuadre que Javo corrigió el 2026-09-05.

        «Lo histórico no es la verdad absoluta o una camisa de fuerza
         que se deba continuar.»

    Tenía razón, y lo incómodo es que **el canon ya lo decía**: `DOC-013`
    establece que QUIRA no conserva conceptos por herencia. Lo que pasó es que
    `GM-Ω` reconstruyó tanta genealogía que produjo un sesgo conservador **de
    hecho**, aunque **de derecho** dijera lo contrario.

    La regla que lo corrige: un `NO DETERMINABLE` genealógico es un **grado de
    libertad**, no una laguna. Donde no hay razón documentada no hay nada que
    respetar.

    ⚠️ Y LA DISTINCIÓN QUE IMPIDE QUE ESTO SE VUELVA LO CONTRARIO —borrón y
    cuenta nueva—: hay una parte que no es herencia sino **anclaje normativo**.
    `R_i`↔COOTAD, `V_i`↔LOTAIP, `T_i`↔COPFP/Acuerdo 067 no se revisan por
    criterio propio: cambian si cambia la ley. Confundir las dos categorías
    falla en ambas direcciones — congelar por costumbre lo mejorable, o
    rediseñar por gusto lo que la norma fija."""
    txt = _MAPA.read_text(encoding="utf-8")
    assert "GRADO DE LIBERTAD, no una laguna" in txt, (
        "desapareció DOC-027. Sin él, cada NO DETERMINABLE de la genealogía "
        "vuelve a leerse como un hueco que hay que respetar, cuando es "
        "exactamente lo contrario: nada que respetar")
    assert "Herencia histórica ≠ anclaje normativo" in txt, (
        "se perdió la distinción que impide que «lo histórico no obliga» se "
        "convierta en borrón y cuenta nueva. Lo anclado a norma vigente no es "
        "herencia revisable")
    assert "no adelanta el momento de intervenir" in txt, (
        "desapareció el límite. Ampliar QUÉ se puede decidir no adelanta "
        "CUÁNDO se toca el motor: el Gold Master sigue congelado hasta C4")
    assert "no autoriza a **inventar** la razón" in txt, (
        "se perdió la salvaguarda de DOC-011. Un NO DETERMINABLE habilita a "
        "decidir, no a rellenar el hueco con una razón fabricada")


def test_la_ruta_al_dictamen_no_pierde_lo_que_pospone():
    """La secuencia acordada el 2026-09-05 —`C2 → C3 → 010 → C4`— pospone dos
    etapas que `C4` sigue necesitando: `011-A2` (declarar la unidad `i` en el
    canon) y `011-B` (la correspondencia documental ↔ operacional).

    ⚠️ POSPONER NO ES CERRAR, y ésa es justo la confusión que este mapa existe
    para evitar. Una etapa que desaparece del camino porque otra se adelantó es
    exactamente el «volver a hacer refactor porque no recordamos» que Javo pidió
    impedir.

    También vigila la razón del orden: `010` va DESPUÉS de `C3` porque analizar
    transferibilidad sobre variables cuya ontología se está reconstruyendo es
    construir sobre premisas que el propio análisis puede desmentir — y `011-C2`
    lo demostró en el acto, refutando la semántica que se daba por buena."""
    txt = _MAPA.read_text(encoding="utf-8")
    assert "LA RUTA AL DICTAMEN" in txt, (
        "desapareció la secuencia acordada hacia el dictamen")
    assert "`011-A2` y `011-B` siguen abiertas" in txt, (
        "el mapa dejó de declarar que la ruta acordada POSPONE dos etapas que "
        "011-C4 sigue necesitando. Sin esa constancia, una etapa pospuesta se "
        "lee como una etapa resuelta")
    assert "Por qué `010` va DESPUÉS de `C3`" in txt, (
        "se perdió la razón del orden. Una secuencia sin su porqué se "
        "reordena en la siguiente sesión por conveniencia")


def test_boot_lleva_al_mapa():
    """`BOOT.md` es la única fuente viva de arranque. Un mapa maestro que no se
    alcanza desde ahí es un documento que nadie abrirá en la sesión siguiente —
    y entonces no resuelve el problema que motivó escribirlo."""
    boot = _BOOT.read_text(encoding="utf-8")
    assert "GM-OMEGA_MAPA_MAESTRO.md" in boot, (
        "BOOT dejó de apuntar al mapa maestro. Sin esa ruta, el próximo "
        "arranque vuelve a reconstruir el estado de memoria, que es justo lo "
        "que Javo pidió evitar")


def test_el_refactor_separa_lo_que_restaura_de_lo_que_crea():
    """DOC-021 · antes de decidir: ¿esto lo resuelve la tesis?

    Javo lo planteó —*«tenemos la tesis, y todo el constructo metodológico allí
    claro; eso es lo que estamos corrigiendo»*— y es cierto en lo esencial. Pero
    no todo lo que el refactor toca estaba ahí:

        RESTAURAR  la tesis tenía la respuesta y la implementación la perdió
                   (`P_i`, `E_i`, AVEP como baremo, «muestra estratégica»…)
        CREAR      la tesis no la tiene y hay que decidirla
                   (criterio de las 25, qué es `i`, umbrales AVEP, LATAM…)

    ⚠️ LA DISTINCIÓN ES OPERATIVA. Esta auditoría cometió los dos errores en
    direcciones opuestas: dudó de `P_i`, que la tesis explicaba, y declaró
    `UNTRACEABLE` a `E_i`, cuya regla la tesis define. Buscar en la tesis una
    respuesta que no está lleva a inventarla; decidir por cuenta propia algo que
    la tesis ya resolvió rompe la genealogía."""
    txt = _MAPA.read_text(encoding="utf-8")
    assert "RESTAURAR" in txt and "CREAR" in txt, (
        "desapareció la separación entre lo que el refactor restaura de la "
        "tesis y lo que decide por primera vez. Sin ella, una decisión nueva "
        "puede presentarse como si viniera del documento fundacional")
    assert "¿esto lo resuelve la tesis?" in txt, (
        "se perdió la pregunta que ordena cada decisión del refactor")
    assert "se declara que es una decisión nueva" in txt, (
        "desapareció la obligación de declarar lo que se crea. Una decisión "
        "nueva presentada como hallazgo falsea la genealogía — que es "
        "precisamente lo que GM-Ω reconstruyó")


def test_un_cambio_de_unidad_con_las_tres_condiciones_no_es_deriva():
    """DOC-023 · la unidad `i` cambió, y eso no es un defecto.

        i = PROMESA del Plan CNE  →  i = META del PDOT

    Se cumplen las tres condiciones: razón metodológica declarada por Javo
    —anclar la evaluación en el instrumento que OPERACIONALIZA el mandato—,
    definición operacional vigente, y genealogía reconstruida (`ANEXO M` de
    febrero + calculadora QUADRUM).

    ⚠️ Y AQUÍ ESTA AUDITORÍA COMETIÓ UN ERROR JURÍDICO GRAVE: escribió que «el
    plan de campaña no obliga jurídicamente». Es falso, y contradice a `d03
    Gobernanza del Mandato Electoral`, que existe precisamente porque el Plan
    CNE **sí** es vinculante. Ambos instrumentos obligan; el PDOT es donde el
    mandato se vuelve medible. La constancia del error se conserva."""
    doc = (RAIZ / "docs" / "architecture" /
           "GM-OMEGA_GENEALOGIA_DOCUMENTAL.md")
    if not doc.exists():
        pytest.skip("aún no se generó el expediente genealógico")
    txt = doc.read_text(encoding="utf-8")
    assert "CORRECCIÓN JURÍDICA" in txt, (
        "desapareció la corrección del error jurídico. Sin ella queda "
        "circulando en el expediente que el Plan CNE no obliga — falso, y "
        "contrario al canon de d03")
    assert "OPERACIONALIZA el mandato" in txt, (
        "se perdió la formulación correcta del cambio de unidad: es "
        "metodológica, no jurídica. Ambos instrumentos son vinculantes")
    assert "constituye evidencia de identidad" in txt, (
        "desapareció el blindaje de los tres universos: 77/76 CNE ≠ 66 PDOT ≠ "
        "25 GM. La coincidencia numérica del 66 ya engañó una vez")


def test_las_decisiones_conversacionales_se_declaran_deuda():
    """DOC-022 · lo que sostiene el motor y vive sólo en una conversación.

    Javo lo aclaró y resolvió el hueco que 13 documentos no llenaron: la fórmula
    del ICPI evolucionó **en diálogo desde enero**. La entrada de `C_i`, el paso
    de cinco a seis factores y la renormalización de `P_i`/`R_i` no están
    documentados porque **nunca hubo documento**.

    ⚠️ NO ES UN REPROCHE AL MÉTODO. Iterar potenció la fórmula y el motor
    resultante funciona. La deuda es otra: **lo que el sistema ejecuta debe
    poder explicarse desde el sistema**, no desde la memoria de quien lo
    construyó. Sin eso, `011` vuelve a decidir lo ya decidido.

    Esta prueba vigila que la constancia no se pierda — porque el día que se
    pierda, el hueco parecerá negligencia documental en vez de lo que fue."""
    doc = (RAIZ / "docs" / "architecture" /
           "GM-OMEGA_GENEALOGIA_DOCUMENTAL.md")
    if not doc.exists():
        pytest.skip("aún no se generó el expediente genealógico")
    txt = doc.read_text(encoding="utf-8")
    assert "la evolución fue conversacional" in txt, (
        "desapareció la explicación del hueco. Sin ella, la ausencia de "
        "documentos se lee como descuido y no como el modo real en que se "
        "construyó el motor")
    assert "nunca hubo uno" in txt, (
        "se perdió la distinción entre «falta un documento» y «nunca existió». "
        "Buscar indefinidamente algo que no se escribió es trabajo perdido")
    assert "el hueco empieza en ENERO" in txt, (
        "la auditoría situaba el hueco en abril→mayo y empieza antes: abril es "
        "sólo donde aparece el primer artefacto conservado")


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
