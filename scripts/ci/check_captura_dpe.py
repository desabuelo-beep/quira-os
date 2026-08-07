"""
QUIRA — Gate del capturador DPE  ·  `scripts/ci/check_captura_dpe.py`

Comprueba que el capturador de la vía principal NO convierta un fallo técnico
en una afirmación sobre un municipio. Es ADR-042 §6 llevado al pipeline: sin
esto, la semántica de estados vive en un módulo y no en el trabajo real.

EL DEFECTO QUE ESTE GATE VIGILA (encontrado 2026-08-07). El conector hacía:

    resp = api_post(...)
    if resp:
        months.append(m)

`api_post` devolvía `None` para todo — 404, timeout, error de servidor y JSON
corrupto—, así que un mes con fallo de red quedaba fuera de la lista exactamente
igual que un mes no publicado. Ese vacío viajaba a un informe y se leía como
incumplimiento.

Las respuestas se simulan: el gate no toca la red ni gasta nada.

Uso:  python scripts/ci/check_captura_dpe.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.observatorio import Estado                              # noqa: E402
import scripts.rc_scout as scout                                 # noqa: E402

fallas: list[str] = []


def _check(ok: bool, descripcion: str, detalle: str = "") -> None:
    print(f"   {'OK  ' if ok else '>>  '} {descripcion}")
    if not ok:
        fallas.append(detalle or descripcion)


class _Respuesta(BytesIO):
    """Sustituto mínimo de lo que devuelve `urlopen`."""
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _simular(comportamiento):
    """Reemplaza `urlopen` en el módulo del scout."""
    scout.urlopen = comportamiento


print("\n[1/2] Cada situación produce el estado que le corresponde")

CASOS = [
    ("la fuente devuelve datos",
     lambda *a, **k: _Respuesta(json.dumps({"total": 1}).encode()),
     Estado.CAPTURADA),
    ("la fuente responde vacío",
     lambda *a, **k: _Respuesta(b"{}"),
     Estado.EVIDENCIA_AUSENTE),
    ("404 — no hay dato para el período",
     lambda *a, **k: (_ for _ in ()).throw(
         HTTPError("u", 404, "not found", {}, None)),
     Estado.EVIDENCIA_AUSENTE),
    ("500 — el servidor falla",
     lambda *a, **k: (_ for _ in ()).throw(
         HTTPError("u", 500, "server error", {}, None)),
     Estado.FUENTE_NO_DISPONIBLE),
    ("la fuente no responde",
     lambda *a, **k: (_ for _ in ()).throw(URLError("timeout")),
     Estado.FUENTE_NO_DISPONIBLE),
    ("responde algo que no sabemos leer",
     lambda *a, **k: _Respuesta(b"<html>mantenimiento</html>"),
     Estado.CAPTURADOR_DEGRADADO),
]

_urlopen_real = scout.urlopen
try:
    for nombre, comportamiento, esperado in CASOS:
        _simular(comportamiento)
        _, estado = scout.api_post_con_estado("http://x", {})
        _check(estado is esperado, f"{nombre} → {estado.value}",
               f"«{nombre}» dio {estado.value} y debía dar {esperado.value}")

    print("\n[2/2] Las distinciones que sostienen la tesis")

    # 1 · Un servidor caído NO puede parecer un municipio que no publica.
    _simular(lambda *a, **k: (_ for _ in ()).throw(URLError("caído")))
    _, e_caido = scout.api_post_con_estado("http://x", {})
    _simular(lambda *a, **k: _Respuesta(b"{}"))
    _, e_vacio = scout.api_post_con_estado("http://x", {})
    _check(e_caido is not e_vacio,
           "«fuente caída» y «sin publicación» son estados distintos",
           "un fallo de red y una ausencia real dan el MISMO estado: el "
           "capturador volvería a convertir un problema técnico en un hallazgo")

    # 2 · Ninguno de los estados técnicos puede publicarse.
    from app.observatorio import es_publicable
    for e in (Estado.FUENTE_NO_DISPONIBLE, Estado.CAPTURADOR_DEGRADADO,
              Estado.ERROR_TECNICO):
        _check(not es_publicable(e), f"«{e.value}» no es publicable")

    # 3 · El capturador expone la variante con estado — si desaparece, algún
    #     llamador volvería a interpretar un None como «no hay datos».
    _check(hasattr(scout, "api_post_con_estado") and
           hasattr(scout, "api_get_con_estado"),
           "el capturador expone las consultas con estado")
finally:
    scout.urlopen = _urlopen_real

print("\n" + "=" * 68)
if fallas:
    print(f"  {len(fallas)} FALLA(S) — el capturador puede afirmar de más")
    for f in fallas:
        print(f"     - {f}")
    print("=" * 68)
    sys.exit(1)
print("  TODO OK — un fallo de la fuente no se registra como incumplimiento")
print("=" * 68)
