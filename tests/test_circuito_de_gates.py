# -*- coding: utf-8 -*-
"""
tests/test_circuito_de_gates.py — la pertenencia al CI se DECLARA, no se infiere del nombre
════════════════════════════════════════════════════════════════════════════════
★ POR QUÉ EXISTE (P5-03 · ratificado 2026-09-14)

El workflow ejecuta `scripts/ci/check_*.py` en bucle. Es decir: **lo que decide si
un verificador es obligatorio es el prefijo de su nombre de archivo.** Hoy coincide
con la función, pero por costumbre — y la costumbre ya falló una vez: en el barrido
`P2/P3` se contó `registrar_ejecucion.py` como gate por residir en `scripts/ci/`, y
es un productor (falsación 16 · residencia leída como función).

EL CRITERIO, ratificado (reformulación del colega):

    Un verificador pertenece al circuito obligatorio cuando su ausencia o fallo
    puede permitir que QUIRA produzca, publique, compile o trate como válido un
    estado que contradiga una invariante canónica de integridad, procedencia,
    normativa o reproducibilidad.

⚠️ El tercer estado (`exit 2`) NO es el criterio: es una propiedad de diseño del
verificador. Un gate puede ser obligatorio aunque todavía no la tenga.

Cada archivo de `scripts/ci/` declara en su docstring una línea

    CIRCUITO: OBLIGATORIO | BAJO_DEMANDA | NO_GATE — y por qué

y esta prueba obliga a que la declaración y el workflow digan lo mismo.

Dylus Lab © 2026
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
_CI = RAIZ / "scripts" / "ci"
_WORKFLOW = RAIZ / ".github" / "workflows" / "quira-health.yml"
_CLASES = ("OBLIGATORIO", "BAJO_DEMANDA", "NO_GATE")
_DECL = re.compile(rf"^CIRCUITO:\s*({'|'.join(_CLASES)})\b\s*[—-]\s*(.+)$", re.M)


def _declaraciones() -> dict[str, list[tuple[str, str]]]:
    """La declaración vive en el DOCSTRING del módulo, y se lee con `ast`.

    Buscarla con una expresión sobre todo el archivo aceptaría un `CIRCUITO:` escrito
    en un comentario o en un ejemplo — hallar el término no prueba la declaración
    (corolario de presencia de `DOC-035`)."""
    out = {}
    for p in sorted(_CI.glob("*.py")):
        doc = ast.get_docstring(ast.parse(p.read_text(encoding="utf-8"))) or ""
        out[p.name] = _DECL.findall(doc)
    return out


def _ejecutados_por_ci() -> set[str]:
    """Lo que el workflow corre DE VERDAD, leído del workflow — no copiado aquí:
    las llamadas explícitas y lo que cubre su bucle."""
    wf = _WORKFLOW.read_text(encoding="utf-8")
    explicitos = set(re.findall(r"python\s+scripts/ci/([\w]+\.py)", wf))
    en_bucle = set()
    for patron in re.findall(r"for\s+\w+\s+in\s+(scripts/ci/[\w*]+\.py)", wf):
        en_bucle |= {p.name for p in RAIZ.glob(patron)}
    return explicitos | en_bucle


def test_todo_archivo_de_ci_declara_su_circuito_una_sola_vez():
    sin, repetidos = [], []
    for nombre, decl in _declaraciones().items():
        if not decl:
            sin.append(nombre)
        elif len(decl) > 1:
            repetidos.append(nombre)
    assert not sin, (
        f"archivos de scripts/ci sin declaración CIRCUITO: {sin}. Declarar "
        "OBLIGATORIO, BAJO_DEMANDA o NO_GATE en el docstring, con el porqué")
    assert not repetidos, f"archivos con más de una declaración: {repetidos}"


def test_toda_declaracion_dice_que_protege_o_por_que_no_es_gate():
    """Una clase sin razón es una etiqueta. La razón es lo que permite revisar la
    clasificación cuando cambie la invariante."""
    vacias = [n for n, d in _declaraciones().items()
              if d and len(d[0][1].strip()) < 25]
    assert not vacias, f"declaraciones sin justificación: {vacias}"


def test_lo_obligatorio_es_exactamente_lo_que_el_ci_ejecuta():
    """El núcleo de P5-03. En las dos direcciones:

    - un verificador declarado OBLIGATORIO que el CI no ejecuta es una protección
      que se cree activa y no lo está;
    - un archivo que el CI ejecuta sin declararse OBLIGATORIO está en el circuito
      por su nombre, no por su función — la falsación 16 esperando repetirse."""
    obligatorios = {n for n, d in _declaraciones().items()
                    if d and d[0][0] == "OBLIGATORIO"}
    ejecutados = _ejecutados_por_ci()

    no_ejecutados = obligatorios - ejecutados
    sin_declarar = ejecutados - obligatorios

    assert not no_ejecutados, (
        f"declarados OBLIGATORIOS que el CI NO ejecuta: {sorted(no_ejecutados)}. "
        "O entran al workflow, o su declaración miente")
    assert not sin_declarar, (
        f"el CI ejecuta sin que se declaren OBLIGATORIOS: {sorted(sin_declarar)}. "
        "Están en el circuito por su nombre de archivo, no por lo que protegen")


def test_un_productor_no_se_ejecuta_como_gate():
    ejecutados = _ejecutados_por_ci()
    productores = {n for n, d in _declaraciones().items() if d and d[0][0] == "NO_GATE"}
    assert not (productores & ejecutados), (
        f"el CI trata como gate a un productor: {sorted(productores & ejecutados)}")
