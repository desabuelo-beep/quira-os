# -*- coding: utf-8 -*-
"""
tests/test_acoplamiento_observable.py — CAPA 2 · P6 y P7
════════════════════════════════════════════════════════════════════════════════
El colega fijó la precisión antes de empezar:

> *«No construyamos un "grafo de imports". Construyamos un grafo de acoplamiento
> observable. Los imports pueden ser una de sus fuentes, pero no la definición
> del grafo.»*

Y la regla que gobierna la lectura del resultado:

> *«No detectar una lectura no significa que no exista una lectura.»*

EL HALLAZGO DE ESTE ATAQUE, y es el sexto del mismo patrón en la sesión:
`check_portabilidad.py` declara `AMBITOS = ("scripts", "app", "quira_pages",
"utils")` y lleva meses reportando **0 rutas fijas · objetivo cumplido**.
`sentinel/` —73 archivos `.py`— no está en esa lista, y contiene tres rutas
absolutas al disco de una persona.

Dylus Lab © 2026
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import acoplamiento as K                  # noqa: E402


# ── CRITERIOS ─────────────────────────────────────────────────────────────────
def test_el_grafo_se_deriva_del_AST_no_del_texto():
    """Un nombre de función en un comentario no es una llamada. Toda la sesión
    demostró que el análisis textual produce falsos positivos; aquí se exige que
    el módulo use `ast` de verdad."""
    fuente = (RAIZ / "app" / "agents" / "acoplamiento.py").read_text(encoding="utf-8")
    assert "import ast" in fuente and "ast.walk" in fuente
    assert K.grafo(), "el grafo quedó vacío: eso sería verde por no mirar nada"


def test_las_rutas_compuestas_se_resuelven():
    """`RAIZ / "docs" / "brn"` es la forma dominante en QUIRA, porque el sistema
    tiene trinquete en **0 rutas fijas**. Un analizador que sólo entiende
    literales mide bien un sistema mal construido y mal uno bien construido: sin
    resolver composiciones veía 7 artefactos de 52."""
    encontrados = {a["hacia"] for a in K.grafo() if a["resuelto"]}
    assert len(encontrados) >= 40, (
        f"la resolución de rutas compuestas se rompió: {len(encontrados)} artefactos")
    assert any(x.startswith("data/") for x in encontrados)


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_un_modo_de_apertura_no_es_un_artefacto():
    """REGRESIÓN de un defecto real de este módulo.

    La primera versión tomaba «el primer argumento string» como ruta, y el grafo
    registró como artefactos del sistema los modos `"a"`, `"r"`, `"rb"`, `"w"`,
    el encoding `cp850` y hasta el contenido XML de un archivo. `open(ruta,
    "rb")` y `ruta.open("rb")` son la misma operación con la ruta en sitios
    opuestos — cada operación debe declarar DÓNDE la lleva."""
    basura = {"a", "r", "rb", "w", "wb", "utf-8", "utf-8-sig", "cp850"}
    hallados = {a["hacia"] for a in K.grafo() if a["resuelto"]}
    intersec = basura & hallados
    assert not intersec, f"volvieron a colarse modos/encodings como artefactos: {intersec}"


def test_ataque_lo_no_resoluble_no_desaparece_del_grafo():
    """LA REGLA DEL COLEGA, fijada como prueba. Si el analizador no puede
    resolver una ruta, el acoplamiento debe seguir en el grafo marcado como no
    determinable. Un acoplamiento invisible es peor que uno no declarado: el
    segundo se ve."""
    c = K.cobertura_de_acoplamiento()
    assert c["no_determinables"] > 0
    assert c["no_determinables"] + len([a for a in K.grafo() if a["resuelto"]]) == c["aristas"], (
        "hay aristas que no están ni resueltas ni contadas como no determinables")
    assert c["modulos_con_ruta_no_resoluble"], (
        "no se dice QUÉ módulos tienen rutas irresolubles: sin eso el límite no "
        "es accionable")


def test_ataque_el_modulo_no_se_cuenta_a_si_mismo():
    """`acoplamiento.py` nombra en su tabla todas las operaciones que busca. Si
    se analizara, aparecería acoplado a todo lo que mide."""
    assert not any(a["desde"].endswith("agents/acoplamiento.py") for a in K.grafo())


def test_ataque_el_grafo_no_decide_si_lo_no_declarado_esta_mal():
    """Un acoplamiento no declarado puede ser deuda, dependencia legítima
    omitida, arquitectura antigua o falso positivo. El módulo observa; la
    decisión exige gobernanza."""
    c = K.cobertura_de_acoplamiento()
    assert "incorrecto" not in c and "infraccion" not in c
    assert "No se afirma que lo no declarado esté mal" in c["afirmacion_sostenible"]


# ── EL HALLAZGO · P7 ──────────────────────────────────────────────────────────
def test_el_gate_de_portabilidad_no_cubre_sentinel():
    """SEXTA VEZ EL MISMO PATRÓN: una lista escrita a mano que pretende ser el
    universo.

    `check_portabilidad.py` declara `AMBITOS = ("scripts", "app",
    "quira_pages", "utils")` y reporta **0 rutas fijas · objetivo cumplido**.
    `sentinel/` tiene 73 archivos `.py`, no está en la lista, y contiene tres
    lecturas con ruta absoluta al disco de una persona —halladas por el grafo de
    acoplamiento, no por el gate—.

    ⚠️ Esta prueba **fija el hallazgo, no lo repara**: ampliar `AMBITOS` movería
    el trinquete de 0 a 3 y eso es una decisión de gobernanza. Cuando se decida,
    esta prueba debe invertirse — y que haya que tocarla es justamente la señal
    de que algo cambió."""
    gate = (RAIZ / "scripts" / "ci" / "check_portabilidad.py").read_text(encoding="utf-8")
    assert 'AMBITOS = ("scripts", "app", "quira_pages", "utils")' in gate, (
        "cambió el universo del gate: revisar si el hallazgo sigue vigente")
    assert (RAIZ / "sentinel").is_dir()
    assert "sentinel" not in gate, "sentinel entró al gate: actualizar el hallazgo"

    absolutas = [a for a in K.grafo()
                 if a["resuelto"] and (a["hacia"][1:3] == ":\\" or a["hacia"][1:3] == ":/")]
    assert absolutas, "dejaron de verse las rutas absolutas"
    assert all(a["desde"].startswith("sentinel/") for a in absolutas), (
        f"aparecieron rutas absolutas fuera de sentinel/: "
        f"{[a['desde'] for a in absolutas if not a['desde'].startswith('sentinel/')]}")
