# -*- coding: utf-8 -*-
"""
tests/conftest.py — la frontera entre observar y actuar
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-25 · deuda 4-ter). Javo, tras el episodio de procedencia:

> *«Una prueba no puede tener capacidad accidental de producir efectos
> operativos. Una prueba que puede salir a la red, descargar, regenerar o
> modificar artefactos deja de ser una observación controlada y puede contaminar
> aquello que pretende verificar.»*

Y la frontera que fijó, que es la que este archivo implementa:

> *«Un test que necesite trabajo real no es un test unitario; es una operación
> que debe estar explícitamente separada del ciclo de pruebas.»*

CÓMO LLEGAMOS AQUÍ. Corrigiendo la deuda #2 desalineé la cadena, y `test_08b`
—que sólo quería comprobar un gate— acabó lanzando el orquestador, que decidió
que la evidencia estaba vieja y se puso a **reanalizar 936 archivos y a intentar
salida de red**. La suite se colgó. Nadie escribió eso: fue una capacidad
heredada que nadie había declarado.

    test_08b → orquestador.ejecutar() → preparar_evidencia()
             → ejecutar_etapa() → subprocess → script → curl

LA SIMETRÍA QUE LO HACE IMPORTANTE (Javo). Con la procedencia, el mecanismo de
observación modificó el objeto observado. Aquí, el mecanismo de observación
puede modificar **el mundo que intenta observar**. Son el mismo fallo:

    **el observador no puede alterar en silencio aquello cuya integridad
    pretende demostrar.**

QUÉ DEFIENDE. `subprocess` es el único punto por el que el trabajo real sale
(`app/agents/d07/etapas.py:337`): los generadores corren como procesos hijos, y
la red vive dentro de ellos. Por eso bloquear sólo sockets no serviría de nada
—el hijo tiene su propio proceso— y el estrangulamiento correcto es el `spawn`.
Los sockets se cierran igual, como defensa en profundidad por si algún día algo
llama a la red en-proceso.

QUÉ NO HACE. No prohíbe el trabajo real: lo obliga a **declararse**.

    @pytest.mark.efecto_real("reconstruye el derivado, que es lo que prueba")

Una capacidad declarada es auditable; una heredada, no. Ésa es toda la
diferencia, y es la misma que el dominio le exige al sujeto observado.

Dylus Lab © 2026
"""
from __future__ import annotations

import socket
import subprocess
from pathlib import Path

import pytest

_RAIZ = Path(__file__).resolve().parents[1]
MARCADOR = "efecto_real"


class EfectoRealNoDeclarado(RuntimeError):
    """Una prueba intentó actuar sobre el mundo sin haberlo declarado."""


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        f"{MARCADOR}(razon): la prueba necesita trabajo real —subprocesos, red— "
        f"y lo declara. Sin este marcador, cruzar la frontera detiene la prueba.")


def _prohibir(que: str, como_declarar: bool = True):
    def _bloqueado(*a, **k):
        detalle = ""
        if a:
            detalle = f"\n  intento: {str(a[0])[:120]}"
        extra = (f"\n\n  Si esta prueba NECESITA trabajo real, decláralo:\n"
                 f"    @pytest.mark.{MARCADOR}(\"por qué lo necesita\")\n"
                 f"  Una capacidad declarada es auditable; una heredada, no."
                 ) if como_declarar else ""
        raise EfectoRealNoDeclarado(
            f"una prueba intentó {que} sin declararlo.{detalle}"
            f"\n\n  Las pruebas observan; no actúan sobre el mundo. Esto existe "
            f"porque una\n  prueba llegó a reanalizar 936 archivos y a intentar "
            f"salida de red\n  mientras creía estar comprobando un gate "
            f"(deuda 4-ter).{extra}")
    return _bloqueado


@pytest.fixture(autouse=True)
def frontera_de_efectos(request, monkeypatch):
    """Cierra la frontera para toda prueba que no haya declarado cruzarla.

    `autouse` a propósito: una defensa que hay que recordar activar es
    exactamente la que falla el día que importa. Se aplica a las 494 y son las
    excepciones —no la regla— las que tienen que escribirse."""
    if request.node.get_closest_marker(MARCADOR):
        return                       # declarado: la prueba responde por ello

    # El spawn de procesos: por aquí sale TODO el trabajo real del dominio.
    for nombre in ("run", "Popen", "call", "check_call", "check_output"):
        monkeypatch.setattr(subprocess, nombre,
                            _prohibir(f"lanzar un subproceso "
                                      f"(subprocess.{nombre})"), raising=False)

    # Defensa en profundidad: hoy ninguna prueba llama a la red en-proceso, y
    # esto es para que mañana tampoco pueda empezar a hacerlo en silencio.
    monkeypatch.setattr(socket.socket, "connect",
                        _prohibir("abrir una conexión de red"), raising=False)
    monkeypatch.setattr(socket, "create_connection",
                        _prohibir("abrir una conexión de red"), raising=False)


# ── LA EVIDENCIA QUE EL REPOSITORIO NO CONTIENE ──────────────────────────────
# D-007 · 2026-09-02. Al replicar CI en un clon limpio, tres pruebas fallaron —no
# por un defecto del código, sino porque exigen los 422 artefactos capturados del
# portal, y `.gitignore:114` excluye `data/lotaip/artefactos/` del repositorio
# **por decisión**: son la captura, no el sistema.
#
# El defecto no estaba en el .gitignore ni en el código: estaba en que las
# pruebas **no declaraban esa dependencia**. Dos de ellas ni la mencionaban, y la
# tercera miraba la SALIDA que iba a rehacer en vez de la EVIDENCIA con la que la
# rehace — un guardián apuntando al sitio equivocado.
#
# ⚠️ UN SKIP NO ES UN APROBADO, y por eso este guardián comprueba la AUSENCIA DEL
# DATO, nunca atrapa un fallo. Si la evidencia está y la prueba falla, falla: lo
# que se salta es la comprobación imposible, no la incómoda.
CAPTURA = "data/lotaip/artefactos"


@pytest.fixture
def evidencia_capturada():
    """Salta la prueba si la evidencia local no está, diciendo por qué.

    Se pide como argumento —`def test_x(evidencia_capturada):`— y así la
    dependencia queda **en la firma de la prueba**, visible sin leer el cuerpo.
    Ésa es la mitad del arreglo: la otra era que existiera.

    En la máquina donde vive la captura, estas pruebas corren enteras y son de
    las más exigentes que tiene el sistema. En CI se saltan y **el informe lo
    dice**: un verde de CI acredita lo que CI pudo mirar, no todo (C0 · D-004)."""
    carpeta = _RAIZ / CAPTURA
    if not carpeta.exists() or not any(carpeta.glob("*.bin")):
        pytest.skip(
            f"evidencia capturada ausente ({CAPTURA}): .gitignore la excluye del "
            f"repositorio por decisión, así que esta comprobación no es posible "
            f"aquí. NO es un aprobado — es una verificación no realizada.")
    return carpeta
