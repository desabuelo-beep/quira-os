# -*- coding: utf-8 -*-
"""
tests/test_registro_de_autoridad.py — el registro que certifica la cadena de autoridad
════════════════════════════════════════════════════════════════════════════════
★ POR QUÉ EXISTE (P5 · 2026-09-14)

`check_health [5/5]` imprimía «100 % · 111 aristas · 0 rotas» en cada CI. Al
regenerar sus derivados apareció lo que esa línea escondía:

    registro …… generado el 2026-08-12 · 29 activos fuera, entre ellos
                toda la familia normativa de Transparencia
    grafo ……… generado el 2026-07-27 · siete semanas
    cadena …… 5 aristas rotas, invisibles

Tres defectos distintos lo producían, y cada prueba de aquí ataca uno:

  1 · el paso «¿el Registry está al día con el disco?» sólo comprobaba que la
      Constitución EXISTIERA — el rótulo prometía frescura, el mecanismo
      verificaba existencia
  2 · sin `id:` declarado, el identificador se FABRICABA desde el nombre de
      archivo: `ADR-023` quedaba como `CANON_ADR-ADR-023_Arquitectura_Tres_Nivele`,
      y todo hijo con `parent: ADR-023` apuntaba a nada (`DOC-015`)
  3 · un padre que existe fuera del catálogo se informaba como «inexistente»

Y un cuarto, latente: los extractores leían `id:` y `status:` en cualquier parte
del texto, sin distinguir la cabecera de un ejemplo citado. Es el corolario de
presencia de `DOC-035`.

⚠️ Estas pruebas protegen REGLAS, no el estado actual: siguen siendo válidas
aunque mañana cambien todos los activos.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for sub in ("", "scripts/governance", "scripts/ci", "scripts/rearq"):
    ruta = str(RAIZ / sub) if sub else str(RAIZ)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

import build_authority_graph  # noqa: E402
import build_registry  # noqa: E402
import check_health  # noqa: E402

_REGISTRO = RAIZ / "registry" / "registry.yaml"
_GRAFO = RAIZ / "registry" / "authority_graph.json"
_FENCE = "`" * 3


def test_un_registro_desactualizado_no_pasa_el_gate():
    """El defecto 1. Se quita un activo del registro EN MEMORIA —el disco sigue
    teniéndolo— y el gate debe decir que el registro no refleja el disco.

    Si esta prueba pasa con un registro mutilado, el paso 3 de `check_registry`
    volvió a ser lo que era: un rótulo sin mecanismo."""
    txt = _REGISTRO.read_text(encoding="utf-8")
    bloques = txt.split("\n  - id: ")
    assert len(bloques) > 2, "el registro no tiene el formato esperado"
    mutilado = "\n  - id: ".join([bloques[0]] + bloques[2:])

    errores = check_health._registro_al_dia(mutilado, _GRAFO)

    assert any("no refleja el disco" in e for e in errores), (
        "se retiró un activo del registro y el gate no lo detectó: el paso "
        f"«¿el registro está al día?» no está verificando nada. Errores: {errores}")


def test_el_identificador_es_el_que_el_documento_declara():
    """El defecto 2 (`DOC-015` · identificador estable ≠ nombre).

    `ADR-023` es el padre que cuatro aristas no encontraban. Su identificador no
    se fabrica: lo declara su título y lo confirma su archivo."""
    adr23 = next((RAIZ / "docs" / "adr").glob("ADR-023_*.md"))
    assert build_registry.identificador(adr23, None, "canon_adr") == "ADR-023"


def test_el_prefijo_del_archivo_solo_no_acredita_el_identificador(tmp_path):
    """La otra cara del defecto 2, para no caer en el opuesto: el nombre de archivo
    por sí solo NO basta. Hacen falta dos representaciones que coincidan —título y
    archivo—; una sola sería inferir el identificador del nombre (`DOC-033`)."""
    doc = tmp_path / "ADR-999_Documento_de_prueba.md"
    doc.write_text("---\nauthority:\n  parent: GOVERNANCE-001\n---\n\n"
                   "# Un título que no declara identificador\n", encoding="utf-8")

    ident = build_registry.identificador(doc, None, "canon_adr")

    assert ident != "ADR-999", (
        "se tomó el identificador del nombre de archivo sin que el documento lo "
        "declarara: eso es inferir por nombre, no leer una declaración")


def test_hallar_un_termino_no_prueba_la_declaracion(tmp_path):
    """El corolario de presencia de `DOC-035`, atacado sobre los DOS extractores
    de QUIRA que leen declaraciones de un documento.

    El caso es la falsación 15 del barrido: un `estado: NO_VIGENTE` escrito dentro
    de un ejemplo se leyó como el estado del documento. Aquí el término está
    presente —`id:`, `status:`— y lo que no está es la declaración."""
    doc = tmp_path / "ejemplo.md"
    doc.write_text(
        "# Un documento sin cabecera\n\n"
        "Así se vería una ficha:\n\n"
        f"{_FENCE}yaml\nid: FALSO-001\nstatus: NO_VIGENTE\nparent: NADIE\n{_FENCE}\n",
        encoding="utf-8")

    ident, padre, _ = build_registry.analizar(doc)
    assert ident is None and padre is None, (
        f"el registro tomó id={ident!r} parent={padre!r} de un bloque de ejemplo: "
        "hallar el término no prueba la declaración")

    import preguntas_publicas
    assert preguntas_publicas._cabecera(doc.read_text(encoding="utf-8")) == "", (
        "el extractor de estado de los PCD aceptó un documento sin cabecera como "
        "si declarara algo")


def test_un_padre_fuera_de_catalogo_no_es_un_padre_inexistente():
    """El defecto 3. `PROTOCOLO_CURACION_DOMINIO` existe en disco, en el hueco de
    alcance que el registro declara a propósito. Llamarlo «inexistente» era decir
    que falta lo que sólo no se inspeccionó — `DOC-035` sobre el propio gate."""
    assert build_authority_graph.fuera_de_catalogo("PROTOCOLO_CURACION_DOMINIO")
    assert not build_authority_graph.fuera_de_catalogo("NO_EXISTE_EN_NINGUN_SITIO")


def test_ningun_identificador_nombra_a_dos_activos():
    """Un id que nombra a dos activos no resuelve a ninguno.

    Pasó: los seis `app/agents/d*/__init__.py` compartían `DOMAIN_PIPELINE-__init__`
    — seis pipelines fundidos en un nodo del grafo."""
    activos, _ = build_registry.escanear()
    vistos: dict[str, str] = {}
    duplicados = []
    for a in activos:
        if a["id"] in vistos:
            duplicados.append((a["id"], vistos[a["id"]], a["path"]))
        vistos[a["id"]] = a["path"]
    assert not duplicados, f"identificadores compartidos: {duplicados}"
