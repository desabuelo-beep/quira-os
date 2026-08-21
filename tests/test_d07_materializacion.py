# -*- coding: utf-8 -*-
"""
tests/test_d07_materializacion.py — obligación ↔ evidencia
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-20). Javo corrigió la ontología del dominio:

> *«El universo de información de transparencia activa del GAD no debe
> interpretarse como una colección arbitraria de archivos, sino como una
> materialización documental de obligaciones normativas y procedimentales.»*

Estas pruebas defienden esa estructura y, sobre todo, la regla que impide
convertir una ausencia en una acusación.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents.d07 import materializacion as M              # noqa: E402


def test_la_ausencia_de_artefacto_no_es_incumplimiento():
    """LA REGLA CENTRAL (colega, 2026-08-20):

    > *«La ausencia de un artefacto no constituye por sí misma incumplimiento;
    > constituye una ausencia de evidencia respecto de una obligación cuya
    > materialización esperada debe haber sido previamente determinada por el
    > corpus normativo y procedimental aplicable.»*

    Ningún estado de esta matriz puede afirmar incumplimiento: eso es
    calificación jurídica y corresponde al motor normativo, no al instrumento
    que observa. Es el mismo error que el dominio acaba de corregir con los
    enlaces —«no lo encontré» convertido en «no existe»— aplicado ahora a los
    documentos."""
    prohibidos = {"incumple", "incumplimiento", "infringe", "viola", "ilegal",
                  "no_cumple", "sancion"}
    estados = {M.MATERIALIZADA, M.PARCIAL, M.SIN_EVIDENCIA, M.NO_DETERMINABLE}
    for e in estados:
        assert not (set(e.lower().split("_")) & prohibidos), (
            f"el estado «{e}» califica jurídicamente y no debería")
    # Y el estado de ausencia debe nombrarse por lo que es: falta de evidencia.
    assert M.SIN_EVIDENCIA == "sin_evidencia_hallada"


def test_la_unidad_es_la_relacion_no_el_archivo_ni_el_numeral():
    """La matriz se construye desde la obligación, con la evidencia entrando
    como materialización — no al revés. Cada relación debe poder responder qué
    exige la norma, con qué procedencia normativa, y qué se encontró."""
    obligaciones = M.cargar_obligaciones()
    assert len(obligaciones) >= 25, "faltan obligaciones de la vara"
    # El art. 24 —donde la norma pide las actas del Concejo— no es un numeral
    # del art. 19 y vive aparte en la vara: omitirlo dejaba 48 artefactos sin
    # obligación identificada teniendo la suya, y de las más importantes.
    assert any(o.numeral == "Art.24" for o in obligaciones)
    for o in obligaciones:
        assert o.texto, f"la obligación {o.numeral} llegó sin su texto normativo"


def test_el_numeral_5_22_es_un_solo_conjunto_en_el_portal():
    """FALSO HALLAZGO EVITADO (2026-08-20). El mapeo devolvía `5` para los
    numerales 5 y 22, pero el portal los publica juntos bajo `Numeral 5-22`. La
    primera corrida declaró «numeral 5 sin evidencia hallada» habiendo **30
    artefactos publicados**: un hallazgo falso producido por el instrumento."""
    assert M._clave("5") == "5-22"
    assert M._clave("22") == "5-22"
    assert M._clave("Art.24") == "Art."
    assert M._clave("6") == "6", "los demás numerales no se remapean"


def test_lo_que_no_se_asocia_a_una_obligacion_no_se_interpreta():
    """Un artefacto sin obligación identificada puede significar cuatro cosas
    distintas —que no hallamos la relación normativa, que hay una obligación
    transversal, que es materialización complementaria, o que no es exigido— y
    **sólo la cuarta** sería «el GAD publica lo que nadie le pide».

    Presentar esa lectura como la única sería inventar un hallazgo. El módulo
    declara la limitación del análisis y se detiene ahí."""
    fuente = (RAIZ / "app" / "agents" / "d07" /
              "materializacion.py").read_text(encoding="utf-8")
    i = fuente.index("def artefactos_sin_obligacion")
    bloque = fuente[i:i + 1400]
    assert "limitación del análisis" in bloque
    assert "no se presume" in bloque or "se determina, no" in bloque


def test_una_obligacion_sin_periodicidad_declarada_no_la_inventa():
    """La Guía no declara periodicidad para todos los numerales. Donde no la
    declara, exigirla sería fabricar la obligación — y el dominio ya cometió ese
    error una vez, aplicando «12 meses» a conjuntos trimestrales."""
    obligaciones = M.cargar_obligaciones()
    sin_declarar = [o for o in obligaciones if not o.periodicidad_declarada]
    assert sin_declarar, (
        "la vara declara periodicidad para TODOS los numerales; verificar, "
        "porque la Guía no lo hace")
    for o in sin_declarar:
        assert o.periodicidad.get("estado") in (None, "no_sustentado")


def test_el_numeral_22_existe_como_obligacion_propia():
    """LO QUE JAVO ENCONTRÓ (2026-08-20), y era un defecto del extractor.

    > *«El 5-22 son dos cosas que se piden: por un lado el formulario para
    > acceso a la información pública y por otro la evidencia de los servicios
    > brindados. Y así cada literal tiene su propia forma, reglamentada.»*

    La vara **no tenía el numeral 22**. El extractor fusionaba el bloque porque
    la guía lo desarrolla junto al 5, con un solo conjunto de datos — y un
    comentario mío afirmaba que separarlos «inventaría dos exigencias donde la
    norma pone una». La norma pone dos, y la guía las transcribe por separado:

        [293] Números 5 y 22                          ← encabezado plural
        [296] «Los servicios que brinda la entidad…»   (ibidem, número 5)
        [297] «Formularios y formatos de solicitudes…» (ibidem, número 22)

    Fusionar la publicación NO fusiona la obligación. Mientras estuvieron
    fundidas era **imposible** sostener el hallazgo que la norma permite:
    «publica los servicios pero no los formularios»."""
    obligaciones = {o.numeral: o for o in M.cargar_obligaciones()}
    assert "22" in obligaciones, "el numeral 22 desapareció de la vara otra vez"
    o22 = obligaciones["22"]
    assert "ormulario" in o22.texto, (
        "el numeral 22 debe traer su obligación literal, no la del 5")
    assert "ervicio" in obligaciones["5"].texto
    assert o22.texto != obligaciones["5"].texto, "son dos obligaciones distintas"


def test_los_campos_del_bloque_compartido_no_se_reparten_por_nuestra_cuenta():
    """La guía asigna SEIS campos al bloque 5-22 y **no dice cuáles
    corresponden a cada numeral**. Repartirlos por criterio propio sería
    completar la norma — precisamente lo que la vara existe para no hacer.

    Se declara el estado y se deja el reparto como lo que es: un silencio del
    corpus, no una decisión de QUIRA."""
    obligaciones = {o.numeral: o for o in M.cargar_obligaciones()}
    for num in ("5", "22"):
        d = obligaciones[num]
        assert d.campos_exigidos, f"el numeral {num} llegó sin campos"
    # Ambos heredan los mismos campos del bloque, y eso se declara.
    assert (obligaciones["5"].campos_exigidos ==
            obligaciones["22"].campos_exigidos)


# ══════════════════════════════════════════════════════════════════════════════
# CAPA 2 · el caso 317 como test obligatorio del clasificador
# ══════════════════════════════════════════════════════════════════════════════

def test_una_facultad_accesoria_no_degrada_una_obligacion_explicita():
    """TEST OBLIGATORIO DEL CLASIFICADOR (colega, 2026-08-20).

    El párrafo 317 de la Guía contiene **`deberán` y `podrá` a la vez**:

        «los sujetos obligados DEBERÁN generar un documento en el que se
        especifique: descripción del servicio; […] tiempo estimado de respuesta.
        Esta información PODRÁ reportarse en cualquier formato»

    El clasificador lo leyó como facultad no exigible y convirtió una obligación
    con ocho requisitos dentro en una recomendación. El «podrá» gobierna sólo el
    formato; la obligación de generar el documento y sus ocho contenidos queda
    intacta.

    Este caso queda fijado porque es el único de los 105 que mezcla ambos modos
    verbales, y porque su fallo no era técnico sino jurídico: habría eximido al
    sujeto observado de una obligación real."""
    import importlib.util
    ruta = RAIZ / "scripts" / "normativa" / "extraer_condiciones_exigibilidad.py"
    spec = importlib.util.spec_from_file_location("ce", ruta)
    ce = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ce)

    caso_317 = (
        "En cuanto al enlace para acceder al reporte del servicio, los sujetos "
        "obligados deberán generar un documento en el que se especifique "
        "información relacionada con: la descripción del servicio; a quién está "
        "dirigido; requisitos para acceder al servicio. Esta información podrá "
        "reportarse en cualquier formato que considere la entidad.")
    tipo, _ = ce.clasificar(caso_317)
    assert tipo != ce.ORIENTACION, (
        "una facultad sobre el FORMATO no puede degradar la obligación sobre el "
        "CONTENIDO — eximiría al sujeto de una obligación real")

    # Y la facultad pura sí debe reconocerse como tal.
    facultad = "las entidades podrán establecer acciones para difundir sus servicios"
    assert ce.clasificar(facultad)[0] == ce.ORIENTACION


def test_los_pilotos_de_capa2_estan_validados_y_trazables():
    """Cada condición de los pilotos debe declarar quién la validó y poder
    remontarse a su párrafo de origen. Sin eso, una clasificación jurídica sería
    indistinguible de una inferencia del algoritmo (ADR-042 §6-ter)."""
    import yaml
    ruta = RAIZ / "docs" / "brn" / "CAPA2_pilotos_6_y_5-22.yaml"
    if not ruta.exists():
        pytest.skip("sin pilotos de Capa 2 en este entorno")
    d = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    cs = d["numeral_6"]["condiciones"] + d["numerales_5_y_22"]["condiciones"]
    assert len(cs) == 7
    for c in cs:
        assert c["tipo_validado"], f"{c['id']} sin validar"
        assert c["exigible_validado"] in ("si", "no"), f"{c['id']} sin exigibilidad"
        assert c.get("validado_por"), f"{c['id']} no dice quién lo validó"
        assert c["parrafo"], f"{c['id']} sin trazabilidad al texto de origen"
    # La bifurcación condicionada debe declarar su antecedente.
    f01 = next(c for c in cs if c["id"] == "C522-F01")
    assert f01.get("condicion_de_activacion"), (
        "una condición procedimental sin antecedente declarado se leería como "
        "opción discrecional de la entidad")


def test_la_relacion_segmento_condicion_es_de_muchos_a_muchos():
    """ADR-042 §6-sexies · las TRES invariantes del contrato (colega, 2026-08-20).

    No basta con comprobar que `segmento_origen` exista. Hay que demostrar la
    transformación, porque es donde se pierden o se inflan las cuentas:

        1 · todo segmento citado existe en la fuente madre
        2 · un mismo segmento puede originar VARIAS condiciones
        3 · una condición puede citar VARIOS segmentos

    El caso 317 es el fixture canónico de las tres a la vez:

        CSV     C5-B07  ─┐
                          ├── un solo texto (párrafo 317)
                C22-B07 ─┘
        YAML    C522-B02 ─┐
                          ├── dos condiciones tras atomizar
                C522-G01 ─┘

    Y los identificadores NO se reconcilian: `C6-C01` (condición) y `C6-C02`
    (segmento) viven en espacios de nombres distintos a propósito."""
    import csv
    import yaml
    ruta = RAIZ / "docs" / "brn" / "CAPA2_pilotos_6_y_5-22.yaml"
    csv_ruta = RAIZ / "data" / "lotaip" / "VALIDACION_JURIDICA_condiciones.csv"
    if not (ruta.exists() and csv_ruta.exists()):
        pytest.skip("faltan artefactos de Capa 2 en este entorno")

    d = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    cs = d["numeral_6"]["condiciones"] + d["numerales_5_y_22"]["condiciones"]
    with csv_ruta.open(encoding="utf-8-sig") as f:
        segmentos = {r["id"] for r in csv.DictReader(f, delimiter=";")}

    # ── invariante 1 · todo segmento citado existe en la fuente madre ──────────
    for c in cs:
        origen = c.get("segmento_origen")
        assert origen, f"{c['id']} no declara de qué segmento proviene"
        for s in origen:
            assert s in segmentos, (
                f"{c['id']} cita el segmento «{s}», que no está en el CSV")

    # ── invariante 2 · un segmento origina VARIAS condiciones ──────────────────
    por_segmento = {}
    for c in cs:
        for s in c["segmento_origen"]:
            por_segmento.setdefault(s, []).append(c["id"])
    multiples = {s: v for s, v in por_segmento.items() if len(v) > 1}
    assert multiples, (
        "ninguna condición comparte segmento: la atomización no está "
        "representada y el modelo no demuestra su razón de ser")
    assert set(multiples.get("C5-B07", [])) == {"C522-B02", "C522-G01"}

    # ── invariante 3 · una condición cita VARIOS segmentos ─────────────────────
    compartidas = [c for c in cs if len(c["segmento_origen"]) > 1]
    assert compartidas, (
        "ninguna condición cita más de un segmento: el bloque compartido 5-22 "
        "no está representado")

    # ── y los namespaces NO se reconcilian ─────────────────────────────────────
    c6 = next(c for c in cs if c["id"] == "C6-C01")
    assert c6["segmento_origen"] == ["C6-C02"], (
        "el id de condición y el de segmento son distintos A PROPÓSITO: "
        "igualarlos mezclaría la unidad textual con la analítica")

    # El fixture canónico, completo.
    del_317 = [c for c in cs if c["parrafo"] == 317]
    assert len(del_317) == 2
    assert {c["exigible_validado"] for c in del_317} == {"si", "no"}
