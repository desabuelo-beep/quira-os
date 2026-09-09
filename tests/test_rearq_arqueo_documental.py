# -*- coding: utf-8 -*-
"""
tests/test_rearq_arqueo_documental.py — REARQ · Arqueo `001`
════════════════════════════════════════════════════════════════════════════════
★ POR QUÉ EXISTE ESTE ARCHIVO

La Rearquitectura estuvo a punto de tratar como vacío una capacidad que llevaba
semanas construida: la captura, verificación y evaluación documental de la
Transparencia Activa. Existía —con corpus, normativa, reglas, trazabilidad,
código y expediente— y un informe la declaró ausente.

    Un documento que dice «esto está protegido» no protege nada.
    Una prueba que falla cuando el artefacto desaparece, sí.

Por eso este custodio comprueba **los artefactos en disco**, no las frases sobre
ellos. Es la diferencia entre declarar la preservación y ejercerla.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

_DOC = RAIZ / "docs" / "architecture" / "REARQ_ARQUEO_CAPACIDAD_DOCUMENTAL.md"

# Los artefactos que el arqueo declara protegidos. Si alguno desaparece o se
# vacía, esta lista lo delata antes de que nadie lo eche de menos.
_PROTEGIDOS = [
    "docs/pcd/PCD-D07_Transparencia.md",
    "docs/architecture/gm_dumps/H09_S7_TRANSPARENCIA_LOTAIP.md",
    "docs/architecture/gm_dumps/H70_BITACORA_LOTAIP_OPACIDAD.md",
    "docs/architecture/gm_dumps/H41_IOC_OPACIDAD_CRITICA.md",
    "scripts/holding/ingest_lotaip.py",
    "quira_pages/p07_transparencia.py",
    "docs/observations/OBS-009_Divergencia_SIGAD_LOTAIP_GAD_MCR.md",
]


def _plano(t: str) -> str:
    """Une los saltos de línea del markdown para que una aserción no dependa
    de dónde cayó el ajuste de línea.

    ⚠️ Y neutraliza los `>` de continuación de blockquote: sin eso, una frase
    partida dentro de una cita queda con un `>` incrustado en medio y la
    aserción falla por formato, no por contenido."""
    limpio = "\n".join(ln.lstrip("> ").rstrip() for ln in t.splitlines())
    return " ".join(limpio.split())


def test_los_artefactos_protegidos_siguen_en_disco():
    """★ REGLA PROTEGIDA: **la preservación se ejerce, no se declara.**

    Cada uno de estos artefactos costó semanas. El arqueo los declara
    intocables hasta completar `RECONCILIACIÓN`, y esta prueba es lo que
    convierte esa declaración en un gate real.

    ⚠️ Si una de estas rutas falla, **no se corrige la lista**: se recupera el
    artefacto. La lista es el inventario, no el problema."""
    faltan = []
    for rel in _PROTEGIDOS:
        p = RAIZ / rel
        if not p.is_file() or p.stat().st_size == 0:
            faltan.append(rel)
    assert not faltan, (
        "desaparecieron artefactos bajo preservación activa: "
        + " · ".join(faltan)
        + " — recupérelos; NO edite esta lista para que la prueba pase")


def test_el_corpus_capturado_del_portal_sigue_completo():
    """★ REGLA PROTEGIDA: **la evidencia capturada es irreemplazable.**

    Son 1.748 archivos descargados del portal LOTAIP, organizados por año, mes
    y numeral. No se pueden regenerar: el portal cambia, y lo que se publicó en
    febrero de 2026 puede no estar mañana.

    ⚠️ Por eso una captura no es un caché. Es **el estado del sujeto observado
    en una fecha**, y borrarla destruye la única prueba de lo que había."""
    base = RAIZ / "data" / "lotaip"
    desc = base / "descargas"
    assert desc.is_dir(), (
        "desapareció `data/lotaip/descargas/` — es la evidencia capturada del "
        "portal, y no se puede volver a obtener")
    n_desc = sum(1 for p in desc.rglob("*") if p.is_file())
    n_tot = sum(1 for p in base.rglob("*") if p.is_file())
    # ⚠️ Dos cifras, no una. Confundirlas fue el error que este mismo arqueo
    # tuvo que corregir: 1.748 es `data/lotaip/` entero; 936 son las descargas
    # —y 936 es la cifra de evidencia con SHA que `PCD-D07` declara—.
    assert n_desc >= 900, (
        f"las descargas del portal bajaron a {n_desc}. El arqueo registró "
        "936; una caída así indica borrado, no depuración")
    assert n_tot >= 1700, (
        f"el corpus LOTAIP bajó a {n_tot} archivos. El arqueo registró 1.748")


def test_la_secuencia_no_se_invierte():
    """★ REGLA PROTEGIDA: **no se alinea lo histórico con un diseño que aún no
    existe.**

    `ARQUEO → PRESERVACIÓN → RECONCILIACIÓN → DISEÑO REARQ → MIGRACIÓN`.

    ⚠️ Invertirla es exactamente cómo se destruye conocimiento histórico: se
    «limpia» un artefacto para que encaje en un diseño provisional, y cuando el
    diseño cambia ya no queda el original contra el cual comparar."""
    txt = _plano(_DOC.read_text(encoding="utf-8"))
    for etapa in ("ARQUEO", "PRESERVACIÓN", "RECONCILIACIÓN", "DISEÑO REARQ",
                  "MIGRACIÓN"):
        assert etapa in txt, f"desapareció la etapa `{etapa}` de la secuencia"
    assert "Nunca al revés" in txt, (
        "se perdió la prohibición de invertir la secuencia")


def test_RECONSTRUIR_queda_descartado_por_evidencia():
    """★ REGLA PROTEGIDA: **madurez incompleta ≠ capacidad inexistente.**

    Que hoy existan 10 artefactos con OCR manual no significa que la
    arquitectura documental esté ausente: significa que su automatización y su
    escalabilidad están incompletas.

    ⚠️ La distinción decide el destino `REARQ`. «No existe» autoriza a
    reconstruir desde cero; «existe y no escala» obliga a preservar y mejorar.
    Confundirlas cuesta las semanas que ya se invirtieron."""
    txt = _plano(_DOC.read_text(encoding="utf-8"))
    assert "No es `RECONSTRUIR`" in txt, (
        "volvió a abrirse la puerta a reconstruir desde cero una capacidad "
        "cuya existencia está demostrada")
    assert "automatización y escalabilidad" in txt or \
           "automatización** y **escalabilidad**" in txt, (
        "se perdió la lectura correcta del OCR manual: es grado de madurez, "
        "no ausencia de arquitectura")


def test_la_pregunta_abierta_no_se_resuelve_en_el_arqueo():
    """★ REGLA PROTEGIDA: **un arqueo inventaría; no decide.**

    Queda abierto si la capacidad documental es un componente de su dominio o
    infraestructura transversal reutilizable.

    ⚠️ Y la formulación importa: que hoy estén implementadas juntas **no
    demuestra que deban seguir juntas, ni que deban separarse**. Ambas
    conclusiones serían inferencias desde el estado actual — el error que
    `ADR-026` cometió al convertir en definición la arqueología de un dominio
    inacabado."""
    txt = _plano(_DOC.read_text(encoding="utf-8"))
    assert "no demuestra que deban permanecer juntas" in txt, (
        "el arqueo empezó a decidir la residencia arquitectónica")
    assert "Tampoco demuestra que deban separarse" in txt, (
        "se perdió la mitad simétrica de la cautela — sin ella, la frase "
        "empuja hacia conservar")


def test_DOC_035_el_alcance_de_la_busqueda_es_parte_del_resultado():
    """★ REGLA PROTEGIDA: **una búsqueda acotada no autoriza a declarar
    ausencia.**

    El falso vacío se produjo por excluir rutas (`worktrees`) y buscar por el
    número del dominio en vez de por el nombre del trabajo — sin declarar
    ninguna de las dos cosas al reportar.

    ⚠️ Es `DOC-034` aplicado al observador. `d07` declara
    `cortado_por_tope_de_tamano` en lugar de afirmar que el archivo no existe;
    quien informa un vacío debe declarar su alcance con el mismo rigor."""
    txt = _plano(_DOC.read_text(encoding="utf-8"))
    assert "DOC-035" in txt, "desapareció la regla que el error dejó"
    assert "no haber mirado bien no es haber mirado" in txt, (
        "se perdió la formulación de la regla")
    assert "excluyó rutas" in txt and "número del dominio" in txt, (
        "el arqueo dejó de registrar la causa concreta del falso vacío, que "
        "es lo que impide repetirlo")
