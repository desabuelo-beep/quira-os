# -*- coding: utf-8 -*-
"""
tests/test_frontera_de_efectos.py — el guard también se ataca
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-25 · deuda 4-ter). Javo puso la vara donde había que
ponerla:

> *«La prueba buena no sería "hoy no salió a la red". Sería: si el código
> intenta salir a la red durante un test, el test lo detecta y falla. Hay que
> inyectarle la regresión y comprobar que la captura.»*

Es la lección de `test_11b` aplicada al propio mecanismo de defensa: **una
prueba que simplemente pasa no demuestra que esté protegiendo nada.** Aquí se
intenta cruzar la frontera a propósito, en las cuatro direcciones en que se
puede cruzar, y se comprueba que muerde.

LO QUE DEFIENDE, en una línea: el observador no puede alterar en silencio
aquello cuya integridad pretende demostrar.

Dylus Lab © 2026
"""
from __future__ import annotations


import socket
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from tests.conftest import MARCADOR, EfectoRealNoDeclarado     # noqa: E402


# ── LA FRONTERA MUERDE ────────────────────────────────────────────────────────
def test_una_prueba_no_declarada_no_puede_lanzar_un_subproceso():
    """`subprocess` es el único punto por el que sale el trabajo real del
    dominio: los generadores corren como procesos hijos. Cerrarlo cierra la
    descarga, la regeneración y —dentro de esos hijos— la red."""
    for fn in ("run", "Popen", "call", "check_call", "check_output"):
        with pytest.raises(EfectoRealNoDeclarado):
            getattr(subprocess, fn)([sys.executable, "-c", "pass"])


def test_una_prueba_no_declarada_no_puede_abrir_la_red():
    """Defensa en profundidad. Hoy ninguna prueba llama a la red en-proceso;
    esto existe para que mañana no pueda empezar a hacerlo en silencio."""
    with pytest.raises(EfectoRealNoDeclarado):
        socket.create_connection(("example.invalid", 80), timeout=1)
    with pytest.raises(EfectoRealNoDeclarado):
        socket.socket().connect(("example.invalid", 80))


def test_la_ruta_QUE_NOS_COLGO_queda_cortada_en_seco():
    """LA PRUEBA QUE REPRODUCE EL INCIDENTE.

    El 2026-08-25, `test_08b` —que sólo quería comprobar un gate— acabó
    lanzando el orquestador, que vio la evidencia desalineada y se puso a
    reanalizar 936 archivos e intentar salida de red. La suite se colgó.

        test → orquestador.ejecutar() → preparar_evidencia()
             → ejecutar_etapa() → subprocess → script → curl

    Aquí se recorre esa misma ruta a propósito. Debe detenerse en el `spawn`,
    con una causa legible, en milisegundos — no en veinticinco minutos.

    ⚠️ Se comprueba además que la excepción **se propaga**: `ejecutar_etapa`
    captura `TimeoutExpired`, y si algún día ampliara ese `except` a `Exception`
    el guard quedaría convertido en un simple «etapa fallida» y la prueba
    seguiría verde creyéndose protegida."""
    from app.agents.d07 import etapas as E

    import ast

    etapa = next(e for e in E.ETAPAS if e["id"] == "contenido")
    with pytest.raises(EfectoRealNoDeclarado) as exc:
        E.ejecutar_etapa(etapa, forzar=True)      # forzar = ir al trabajo real
    assert "subproceso" in str(exc.value)

    # Y que nadie pueda anular el guard **sin tocarlo**: basta con que
    # `ejecutar_etapa` ensanche su `except` para que la excepción se convierta
    # en un plácido «etapa fallida». Sería la forma más silenciosa de perder la
    # defensa: nada se pondría rojo.
    arbol = ast.parse((RAIZ / "app/agents/d07/etapas.py").read_text(
        encoding="utf-8"))
    fn = next(n for n in ast.walk(arbol)
              if isinstance(n, ast.FunctionDef) and n.name == "ejecutar_etapa")
    capturas = [h.type for n in ast.walk(fn) if isinstance(n, ast.Try)
                for h in n.handlers]
    anchas = [ast.unparse(c) if c is not None else "except: (todo)"
              for c in capturas
              if c is None or ast.unparse(c) in ("Exception", "BaseException")]
    assert not anchas, (
        f"`ejecutar_etapa` captura {anchas}: eso se tragaría la frontera de "
        f"efectos y la convertiría en un resultado «fallida» que nadie mira. "
        f"El guard seguiría existiendo y ya no defendería nada.")


# ── …Y NO ES UN MURO: EL PERMISO FUNCIONA ─────────────────────────────────────
@pytest.mark.efecto_real("comprueba que el propio marcador abre la frontera; "
                         "sin esto el permiso sería decorativo y nadie lo notaría")
def test_el_marcador_realmente_abre_la_frontera():
    """El contrapeso. Un guard que no se pudiera levantar convertiría el
    marcador en adorno, y la primera prueba legítima que lo necesitara sería
    'arreglada' quitando el guard entero."""
    r = subprocess.run([sys.executable, "-c", "print('permitido')"],
                       capture_output=True, timeout=30)
    assert r.returncode == 0
    assert b"permitido" in r.stdout


# ── EL PERMISO ES EXCEPCIONAL, Y ESTÁ CONTADO ─────────────────────────────────
def test_el_permiso_de_efecto_real_es_excepcional():
    """TRINQUETE: puede bajar, nunca subir.

    Declarar el efecto ya es mejor que heredarlo, pero un permiso que se
    reparte deja de ser una excepción y vuelve a ser la regla —sin que nadie
    tome la decisión de volver atrás—. Aquí se cuenta.

    La regla al añadir uno: **si el efecto se puede eliminar, se elimina; sólo
    se declara el que es inherente a lo que la prueba demuestra.** Lanzar un
    script puro para leer su código de salida se elimina (se importa); borrar un
    derivado para ver si la cadena lo reconstruye, no.

    ⚠️ SE CUENTA CON AST, NO CON `grep`, y la primera versión enseñó por qué:
    contaba 3 donde hay 2, porque sumaba una **línea de ejemplo dentro de un
    docstring** como si fuera un decorador. Un tope que cuenta prosa no protege
    nada, y «arreglarlo» subiendo el número habría legitimado un declarante
    inexistente — *etiqueta incorrecta = número falso* (§6-sexies), esta vez
    contra el propio guard."""
    import ast

    DECLARANTES_TOLERADOS = 2
    declarantes = []
    for f in sorted(RAIZ.glob("tests/**/*.py")):
        arbol = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        for nodo in ast.walk(arbol):
            if not isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for dec in nodo.decorator_list:
                objetivo = dec.func if isinstance(dec, ast.Call) else dec
                if (isinstance(objetivo, ast.Attribute)
                        and objetivo.attr == MARCADOR):
                    declarantes.append(f"{f.name}::{nodo.name}")
    assert len(declarantes) <= DECLARANTES_TOLERADOS, (
        f"más pruebas se dieron permiso para actuar sobre el mundo: "
        f"{declarantes}. Antes de subir el tope, comprueba si el efecto se "
        f"puede eliminar en vez de declararse.")


def test_la_frontera_se_aplica_a_todas_sin_que_nadie_la_active():
    """`autouse` a propósito: una defensa que hay que recordar activar es
    exactamente la que falla el día que importa. Se comprueba en el código, no
    en la costumbre."""
    fuente = (RAIZ / "tests" / "conftest.py").read_text(encoding="utf-8")
    assert "@pytest.fixture(autouse=True)" in fuente, (
        "la frontera dejó de aplicarse sola: pasó a depender de que cada "
        "prueba se acuerde de pedirla")
