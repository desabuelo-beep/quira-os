"""
QUIRA — Gate de la semántica de captura  ·  `scripts/ci/check_estados_captura.py`

Verifica que se sostenga la regla de ADR-042 §6:

    «no existe evidencia» ≠ «no pude obtener evidencia» ≠ «el capturador falló»

Es la regla que impide que un selector roto se convierta en una acusación contra
un municipio. Se comprueba sola porque es fácil de enunciar y fácil de perder.

Uso:  python scripts/ci/check_estados_captura.py
Dylus Lab © 2026
"""
from __future__ import annotations

import sys
# La consola de Windows abre en cp1252 y este gate imprime flechas y viñetas.
# Sin esto revienta con UnicodeEncodeError DESPUÉS de calcular sus resultados:
# un gate que muere al informar es un gate que no informa.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.observatorio import (                                    # noqa: E402
    Estado, EstadoNoPublicable, afirma_sobre_sujeto, clasificar,
    es_publicable, exigir_publicable, resumen, semantica, NO_ES_HALLAZGO)

fallas: list[str] = []


def _check(condicion: bool, descripcion: str, detalle: str = "") -> None:
    print(f"   {'OK  ' if condicion else '>>  '} {descripcion}")
    if not condicion:
        fallas.append(detalle or descripcion)


print("\n[1/5] Los ocho estados existen y están completos")
_check(len(Estado) == 8, f"ocho estados definidos (hay {len(Estado)})")
for clave, s in resumen():
    print(f"        {clave:<22} habla de {s.habla_de:<22} "
          f"{'PUBLICABLE' if s.publicable else 'no publicable'}")


print("\n[2/5] Solo dos estados afirman sobre el sujeto observado")
# Un hallazgo positivo acreditado, y la ausencia verificada. Nada más puede
# decir algo sobre la gestión de un municipio.
esperado = {Estado.VALIDADA, Estado.EVIDENCIA_AUSENTE}
real = {e for e in Estado if afirma_sobre_sujeto(e)}
_check(real == esperado,
       f"afirman sobre el sujeto: {sorted(e.value for e in real)}",
       f"deberían ser {sorted(e.value for e in esperado)} y son "
       f"{sorted(e.value for e in real)}")

# Lo publicable y lo que afirma deben coincidir: publicar algo que no afirma
# nada sobre el sujeto sería publicar ruido con apariencia de hallazgo.
_check({e for e in Estado if es_publicable(e)} == esperado,
       "publicable ⇔ afirma sobre el sujeto")


print("\n[3/5] Los tres que se confunden NO hablan del sujeto")
for e in NO_ES_HALLAZGO:
    s = semantica(e)
    _check(not s.afirma_sobre_sujeto and not s.publicable,
           f"«{s.etiqueta}» habla de {s.habla_de}, no del sujeto",
           f"{e.value} afirma sobre el sujeto o es publicable, y no debe")


print("\n[4/5] La guarda corta el paso antes de publicar")
for e in (Estado.CAPTURADOR_DEGRADADO, Estado.FUENTE_NO_DISPONIBLE,
          Estado.ERROR_TECNICO, Estado.PENDIENTE_VALIDACION):
    try:
        exigir_publicable(e, "prueba")
        _check(False, f"«{e.value}» debería bloquearse y no lo hizo")
    except EstadoNoPublicable:
        _check(True, f"«{e.value}» bloqueado antes de publicar")

for e in (Estado.VALIDADA, Estado.EVIDENCIA_AUSENTE):
    try:
        exigir_publicable(e)
        _check(True, f"«{e.value}» pasa la guarda")
    except EstadoNoPublicable:
        _check(False, f"«{e.value}» fue bloqueado y debería pasar")

# Un estado desconocido no puede publicarse: ante la duda no se afirma nada.
_check(not es_publicable("cualquier_cosa"),
       "un estado desconocido no es publicable")


print("\n[5/5] La clasificación distingue los cuatro casos")
casos = [
    ("fuente caída",
     dict(fuente_respondio=False, formato_reconocido=True, hay_contenido=True),
     Estado.FUENTE_NO_DISPONIBLE),
    ("el portal cambió de formato",
     dict(fuente_respondio=True, formato_reconocido=False, hay_contenido=True),
     Estado.CAPTURADOR_DEGRADADO),
    ("respondió bien y no hay nada publicado",
     dict(fuente_respondio=True, formato_reconocido=True, hay_contenido=False),
     Estado.EVIDENCIA_AUSENTE),
    ("respondió bien y hay contenido",
     dict(fuente_respondio=True, formato_reconocido=True, hay_contenido=True),
     Estado.CAPTURADA),
    ("falla nuestra",
     dict(fuente_respondio=True, formato_reconocido=True, hay_contenido=True,
          fallo_interno=True),
     Estado.ERROR_TECNICO),
]
for nombre, kwargs, esperado_e in casos:
    obtenido = clasificar(**kwargs)
    _check(obtenido is esperado_e,
           f"{nombre} → {obtenido.value}",
           f"«{nombre}» dio {obtenido.value} y debía dar {esperado_e.value}")

# EL CASO QUE JUSTIFICA TODO ESTE ARCHIVO: una fuente que responde con un
# formato que ya no entendemos NO puede leerse como ausencia de evidencia.
_check(clasificar(fuente_respondio=True, formato_reconocido=False,
                  hay_contenido=False) is Estado.CAPTURADOR_DEGRADADO,
       "formato roto + sin contenido → capturador degradado, NO ausencia",
       "un capturador roto se estaría reportando como falta de publicación "
       "del municipio — la afirmación falsa que este sistema existe para evitar")


print("\n" + "=" * 66)
if fallas:
    print(f"  {len(fallas)} FALLA(S) — la semántica de captura no se sostiene")
    for f in fallas:
        print(f"     - {f}")
    print("=" * 66)
    sys.exit(1)
print("  TODO OK — un fallo técnico no puede volverse una acusación")
print("=" * 66)
