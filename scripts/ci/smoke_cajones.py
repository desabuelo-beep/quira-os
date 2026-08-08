# -*- coding: utf-8 -*-
"""
smoke_cajones — ¿la APP monta y entra a cada cajón sin reventar? (Dylus Lab © 2026)

Por qué existe: verificar que un renderizador produce HTML correcto NO prueba que la
aplicación arranque y llegue hasta él. Entre uno y otro hay imports, sesión, router y
`st.*` — y ahí es donde fallan los despliegues. Este chequeo cubre ese tramo.

Cómo, sin navegador ni credenciales: `streamlit.testing.v1.AppTest` monta `app.py` de
verdad (mismos imports, mismo router, mismo session_state) y lo ejecuta headless. Las
contraseñas del entorno están hasheadas y no se tocan: se inyecta la sesión ya
autenticada, que es exactamente lo que el login produce tras validar el hash.

Uso:  python scripts/ci/smoke_cajones.py            (todos)
      python scripts/ci/smoke_cajones.py qinv_d08   (uno)
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_RAIZ))

# Cada destino declara una HUELLA: un fragmento que solo aparece si ese cajón se
# renderizó de verdad. Sin ella el chequeo daba falsos OK — "no lanzó excepción" es
# compatible con "el router devolvió al inicio en silencio", que es exactamente el
# bug que este archivo destapó el 2026-08-05. Un test que no distingue no sirve.
#
# Un 4º campo opcional declara CON QUÉ ROLES se prueba el destino. Sin él se
# usan los dos de `ROLES`. Los ambientes propios lo necesitan porque el rol
# legacy `tecnico` no tiene acceso a ellos: probarlos con ese rol no comprobaba
# nada — el router lo desviaba al Centro y el fallo era del test, no del código.
DESTINOS: list[tuple] = [
    ("inicio", "Panorama general", "QUIRA Observatorio"),
    ("qinv_d01", "d01 · Planificación Estratégica", "Planificación"),
    ("qinv_d02", "d02 · Presupuesto & Financiamiento", "capacidad financiera"),
    ("qinv_d03", "d03 · Gobernanza del Mandato", "mandato"),
    ("qinv_d08", "d08 · Participación Ciudadana", "inverificables por el instrumento"),
    ("qinv_d09", "d09 · Rendición de Cuentas", "rendición"),
    ("transparencia", "d07 · Transparencia", "ransparencia"),
    ("territorio", "d10 · Territorio & Cobertura", "erritorio"),
    # El Observatorio es un AMBIENTE, no un módulo del Centro. La huella es una
    # etiqueta que solo se emite si las cifras se contaron contra el registro: si
    # el panel se pintara sin datos, el título saldría igual pero la sección
    # caería en «sin dato».
    ("env:obs", "Observatorio · panel", "Consultables en el portal", ("observatorio",)),
    ("env:ops", "Operaciones · mantenimiento", "Mantenimiento técnico", ("observatorio",)),
]

# `observatorio` es el rol vigente (ADR-041): único con credencial y con acceso pleno.
# Se conserva `tecnico` —legacy, ya sin credencial— porque recorre el OTRO camino del
# router: el de sidebar, donde vivía el bug de navegación que este archivo destapó. Probar
# solo el camino del canvas dejaría ese tramo sin cubrir otra vez.
ROLES = ("observatorio", "tecnico")


def _correr(modulo: str, rol: str = "tecnico", timeout: int = 120):
    """Monta la app con la sesión ya autenticada y navega al destino.

    Un destino con prefijo `env:` cambia de AMBIENTE en vez de módulo — el
    Observatorio no cuelga del Centro, así que probarlo exige entrar por su
    propia puerta."""
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(_RAIZ / "app.py"), default_timeout=timeout)
    at.session_state["authenticated"] = True
    at.session_state["usuario"] = "smoke_ci"
    at.session_state["rol"] = rol
    at.session_state["login_time"] = time.time()
    at.session_state["session_id"] = "sess_smoke"
    if modulo.startswith("env:"):
        at.session_state["page"] = modulo.split(":", 1)[1]
    else:
        at.session_state["page"] = "gov"
        at.session_state["gov_module"] = modulo
    return at.run()


def _verificar(modulo: str, huella: str, rol: str) -> tuple[bool, str]:
    """(pasa, detalle). Tres condiciones: sin excepción, sin `st.error` —así reporta el
    router un módulo caído sin tumbar la app— y con la huella del cajón en el HTML.

    El margen especial que necesitaba Operaciones se retiró: montaba doce
    páginas completas para mostrar una y tardaba casi cuatro minutos. Con carga
    perezosa entra en seis segundos, como cualquier otro destino."""
    at = _correr(modulo, rol=rol)
    if at.exception:
        return False, f"EXCEPCIÓN: {str(at.exception[0].message)[:80]}"
    errores = [e.value for e in at.error]
    if errores:
        return False, f"st.error: {errores[0][:80]}"
    texto = " ".join(m.value for m in at.markdown if isinstance(m.value, str))
    if huella.lower() not in texto.lower():
        return False, f"montó pero NO renderizó el cajón (falta «{huella[:40]}»)"
    return True, f"{len(texto):,} car."


def main(argv: list[str]) -> int:
    destinos = [d for d in DESTINOS if not argv or d[0] in argv]
    print("=" * 72)
    print("  SMOKE · la app monta, entra al cajón y lo RENDERIZA · roles: " + " · ".join(ROLES))
    print("=" * 72)
    fallos = 0
    for destino in destinos:
        modulo, nombre, huella = destino[0], destino[1], destino[2]
        for rol in (destino[3] if len(destino) > 3 else ROLES):
            t0 = time.time()
            try:
                ok, detalle = _verificar(modulo, huella, rol)
            except Exception as e:  # noqa: BLE001
                ok, detalle = False, f"{type(e).__name__}: {str(e)[:70]}"
            marca = "OK    " if ok else "FALLA "
            print(f"  {marca} {nombre:34s} [{rol:9s}] {detalle} · {time.time() - t0:.0f}s")
            fallos += 0 if ok else 1
    total = len(destinos) * len(ROLES)
    print("=" * 72)
    if fallos:
        print(f"  FALLO — {fallos} de {total} comprobaciones no pasan")
        return 1
    print(f"  TODO OK — {total} comprobaciones ({len(destinos)} destinos × {len(ROLES)} roles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
