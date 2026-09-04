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
    for nombre, cat, autoridad, _vis, _ in _INVENTARIO:
        assert cat in _CATEGORIAS, (
            f"`{nombre}` tiene la categoría «{cat}», que no está en la "
            f"taxonomía. Inventar una categoría para acomodar un nombre es "
            f"exactamente la inflación que DOC-013 prohíbe")
        assert autoridad, (
            f"`{nombre}` no declara qué autoridad lo define. Un nombre sin "
            f"autoridad es un nombre que nadie puede cambiar ni retirar")

    sin_cat = [n for n, c, *_r in _INVENTARIO if c == "SIN_CATEGORÍA"]
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


def test_todo_indicador_publicable_declara_su_capa_de_lectura():
    """DOC-014 · nombre técnico ≠ nombre de presentación.

    Javo corrigió el supuesto del que partía la discusión: **los índices están
    construidos para aparecer en el dominio que los representa**. La decisión no
    es cuáles publicar —eso ya lo resolvió la arquitectura de dominios— sino en
    qué **capa de lectura** aparece cada nombre:

        PÚBLICO         la pregunta que responde, y el valor
        INSTITUCIONAL   la sigla, el período, las fuentes, la metodología
        TÉCNICO         el nombre completo y la cadena hasta la evidencia

    ⚠️ SE VERIFICA QUE CADA NOMBRE DECLARE SU CAPA, no que la capa sea la
    acertada — eso se afina en `T3-T5` y se ejecuta en `T6`."""
    from scripts.gm_omega.terminologia_quira import _INVENTARIO, _CAPA_PRESENTACION

    for nombre, _cat, _aut, vis, _nota in _INVENTARIO:
        assert vis in _CAPA_PRESENTACION, (
            f"`{nombre}` declara la visibilidad «{vis}», que no está entre las "
            f"capas de lectura. Inventar una capa para acomodar un nombre es la "
            f"misma inflación que DOC-013 prohíbe, un piso más arriba")

    # Ningún indicador puede vivir sólo en la capa pública: si se publica, tiene
    # que poder abrirse hasta su metodología. Es la mitad de QUIRA que no se
    # negocia — toda afirmación regresa a su evidencia.
    solo_publico = [n for n, c, _a, v, _ in _INVENTARIO
                    if c == "INDICADOR" and v == "PÚBLICO"]
    assert not solo_publico, (
        f"{solo_publico} son indicadores marcados sólo como PÚBLICO. Un "
        f"indicador publicado sin capa metodológica es un número sin "
        f"trazabilidad, que es exactamente lo que QUIRA existe para no hacer")


def test_el_mapeo_indice_dominio_se_declara_ausente_no_se_inventa():
    """El hallazgo real del intento de verificación, y el más incómodo.

    Javo afirma —y la arquitectura lo aplica— que cada índice aparece en el
    dominio que lo representa. Al intentar comprobarlo apareció que **no existe
    un artefacto que declare ese mapeo**: vive en el diseño, no en algo
    verificable. `PROTOCOLO_CURACION_DOMINIO` registra el estado de curación de
    cada dominio, no qué índice le corresponde.

    Es la misma forma que `E_i` —una regla que opera sin estar escrita— y que
    `AVEP` —un vocabulario que se propaga sin autoridad—.

    ⚠️ Y la tabla que el documento imprime NO demuestra lo contrario: se apoya en
    una lista de superficies escrita a mano en el propio script. Medir contra una
    lista propia y presentar el resultado como hallazgo sería `DOC-009` otra vez.
    Esta prueba vigila que esa salvedad no desaparezca."""
    txt = _DOC.read_text(encoding="utf-8")
    assert "No existe un artefacto que declare qué índice pertenece a qué" in txt, (
        "desapareció el hallazgo: sin él, la tabla de índices por dominio se "
        "leería como una verificación, y no lo es")
    assert "escrita a mano" in txt, (
        "desapareció la salvedad sobre la lista de superficies. Sin ella, un "
        "índice ausente de la tabla parecería ausente del producto")


def test_el_contrato_no_rellena_celdas_por_inferencia():
    """`T3-T5` · el contrato ÍNDICE → DOMINIO → ROL → PREGUNTA → CAPA.

    Existe porque el mapeo vive en el diseño y no en un artefacto verificable.
    Su valor depende enteramente de una disciplina: **sólo se declara lo que
    tiene autoridad documental**. Un contrato completo por suposición sería
    `DOC-009` a escala de arquitectura — y peor que no tenerlo, porque parecería
    verificado.

    ⚠️ SE VERIFICA QUE LAS CELDAS SIN AUTORIDAD SIGAN MARCADAS, no que estén
    llenas. Que falte el 62 % es hoy el estado real y honesto del canon."""
    from scripts.gm_omega.contrato_indice_dominio import (_CONTRATO, _DOMINIOS,
                                                          _PENDIENTE, _ROLES)
    assert _CONTRATO, "el contrato quedó vacío"

    for idx, _dom, rol, _preg, autoridad in _CONTRATO:
        assert autoridad, (
            f"`{idx}` no dice de dónde sale su asignación. Una celda sin "
            f"autoridad es una suposición con formato de tabla")
        assert rol in _ROLES, (
            f"`{idx}` declara el rol «{rol}», que no está en la taxonomía de "
            f"roles")

    pendientes = sum(1 for _i, d, r, p, _a in _CONTRATO
                     for v in (d, r, p) if v == _PENDIENTE)
    assert pendientes > 0, (
        "el contrato ya no tiene celdas POR_DECLARAR. Si de verdad se "
        "completó, cada asignación nueva debe citar el PCD, ADR o decisión que "
        "la sostiene — y esta prueba debe pasar a verificar ESO, no la ausencia")

    sin_pregunta = [c for c, (_n, _e, q) in _DOMINIOS.items() if q == _PENDIENTE]
    assert sin_pregunta, (
        "todos los dominios declaran ya su pregunta. Excelente — pero entonces "
        "hay que comprobar que cada una sale de su PCD, no del script")


def test_el_identificador_es_estable_y_el_nombre_puede_migrar():
    """DOC-015 · el mecanismo que hace segura la migración que Javo plantea.

        identificador    ICPI                     ← nunca cambia
        nombre canónico  Índice de Congruencia…   ← puede evolucionar
        nombre histórico (conservado con su período)

    Es el basónimo de la nomenclatura científica: la especie se renombra, el
    nombre original queda registrado, ninguna cita anterior se rompe. Sin esta
    separación, «renombrar» y «conservar la genealogía» parecen excluyentes.

    ⚠️ Y NO AUTORIZA A RENOMBRAR. El orden no se invierte: primero `011` decide
    qué mide el constructo, después cómo se llama. Cambiar el nombre para que
    encaje con el álgebra sería poner etiqueta nueva a contenido no auditado."""
    from scripts.gm_omega.contrato_indice_dominio import _CONTRATO
    from scripts.gm_omega.terminologia_quira import _INVENTARIO

    ids_contrato = {c[0] for c in _CONTRATO}
    ids_inventario = {n for n, cat, *_r in _INVENTARIO if cat == "INDICADOR"}
    assert ids_contrato == ids_inventario, (
        f"el identificador de un indicador difiere entre el inventario y el "
        f"contrato: {ids_contrato ^ ids_inventario}. El identificador es "
        f"justamente lo que NO puede variar entre artefactos — si varía, deja "
        f"de servir para lo único que existe: sostener las referencias")

    contrato_doc = (RAIZ / "docs" / "architecture" /
                    "GM-OMEGA_CONTRATO_INDICE_DOMINIO.md").read_text(encoding="utf-8")
    assert "primero se decide qué mide el constructo, después cómo se llama" in (
        contrato_doc.lower()), (
        "desapareció el orden. Sin él, DOC-015 se leería como permiso para "
        "renombrar, cuando es sólo el mecanismo que lo hará posible sin pérdida")


def test_la_ontologia_gobierna_a_la_implementacion_no_al_reves():
    """DOC-016 · el principio rector de `T3-T6`.

        No se cambia la ontología de un indicador para hacerla coincidir con su
        implementación; se corrige la implementación para hacerla coincidir con
        la ontología validada.

    Protege de un error muy fácil de cometer: descubrir que la fórmula hace A y
    rebautizar A como si siempre hubiera sido el propósito.

    ⚠️ Y esta auditoría estuvo a punto de cometerlo. Llegó a plantear una
    disyuntiva —«congruencia → quitar la multiplicatividad; integridad → el
    nombre se queda corto»— que el título de la tesis disuelve: *«Sistema de
    INTEGRIDAD Algorítmica Preventiva: Modelo de CONGRUENCIA Intersistémica»*
    contiene ambas palabras como **dos niveles**, no como alternativas. La
    constancia de esa corrección debe sobrevivir en el artefacto."""
    doc = (RAIZ / "docs" / "architecture" /
           "GM-OMEGA_CONTRATO_INDICE_DOMINIO.md").read_text(encoding="utf-8")
    assert "falso dilema" in doc.lower(), (
        "desapareció la corrección del planteamiento anterior. Sin ella, la "
        "disyuntiva congruencia/integridad volvería a leerse como si fuera real")
    assert "SIAP" in doc and "dos niveles" in doc.lower(), (
        "se perdió la arquitectura de dos niveles del título fundacional: el "
        "SISTEMA persigue integridad, el MODELO mide congruencia")
    assert "semántica de la multiplicación" in doc.lower(), (
        "011 volvió a plantearse como una elección de palabra. Lo que debe "
        "juzgar es qué significa que un factor sea cero, no qué nombre encaja")


def test_ningun_dominio_se_declara_cerrado_sin_pasar_el_refactor():
    """Regla de Javo, con consecuencia inmediata: `d01`, `d06` y `d09` figuran
    como cerrados, pero se cerraron bajo un canon ANTERIOR a `DOC-013`,
    `DOC-014` y al contrato índice→dominio.

    Es el principio que gobierna todo GM-Ω —**un mecanismo de cobertura no es
    autoridad sobre su propia cobertura**— aplicado a los expedientes de
    curación: un PCD cerrado acredita las siete capas que revisó, no las
    preguntas que aún no se hacían.

    ⚠️ NO invalida esos cierres. Los reclasifica: «cerrado bajo canon anterior»
    es un tercer estado, y su reapertura es barata."""
    doc = (RAIZ / "docs" / "architecture" /
           "GM-OMEGA_CONTRATO_INDICE_DOMINIO.md").read_text(encoding="utf-8")
    assert "cerrado bajo canon anterior" in doc.lower(), (
        "desapareció el tercer estado de los dominios curados. Sin él, un PCD "
        "cerrado antes del Terminology Freeze parecería acreditar preguntas "
        "que nadie le hizo")


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
    _, cat, autoridad, vis, nota = icpi[0]
    assert vis == "INSTITUCIONAL", (
        f"`ICPI` pasó a visibilidad «{vis}». La sigla pertenece a la ficha "
        f"metodológica: en la capa pública va la pregunta que responde, no el "
        f"acrónimo (DOC-014)")
    assert cat == "INDICADOR", (
        f"`ICPI` pasó a categoría «{cat}». No es el centro de QUIRA: es un "
        f"indicador nuclear del Gold Master, y confundirlo con el eje "
        f"ontológico del sistema es el error que ya cometimos con AVEP")
    assert "tesis" in autoridad.lower(), (
        "`ICPI` dejó de citar la tesis como autoridad. Es su único anclaje "
        "documental anterior a cualquier Gold Master conservado")
    assert "Congruencia Programática e Intersistémica" in nota
