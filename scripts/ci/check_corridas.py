"""
QUIRA — Gate del registro de corridas  ·  `scripts/ci/check_corridas.py`

Verifica ADR-042 §4 (preguntas 2, 3, 5 y 6) y §5-bis: que toda corrida quede
registrada con lo necesario para repetirla, y que **lo calibrado no se publique**.

LAS DOS REGLAS QUE ESTE GATE PROTEGE

 1 · Una corrida cuyo costo no se conoce no se puede repetir a escala. Escalar
     de un municipio a 222 multiplica ese número, y conviene saberlo ANTES de
     comprometerlo. Un método que no se puede repetir no es un método.

 2 · La primera corrida de 2025 es de CALIBRACIÓN: su fin es medir si el
     procedimiento funciona, no producir cifras. Publicar sus resultados sería
     dar por bueno un método que todavía se estaba probando.

Uso:  python scripts/ci/check_corridas.py
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

from app.observatorio.corrida import Corrida, TARIFAS          # noqa: E402
from app.observatorio.estados import Estado                    # noqa: E402

fallas: list[str] = []


def _check(ok: bool, desc: str, detalle: str = "") -> None:
    print(f"   {'OK  ' if ok else '>>  '} {desc}")
    if not ok:
        fallas.append(detalle or desc)


print("\n[1/4] Una corrida registra lo necesario para repetirla")
c = Corrida(municipio="130801", fuente="transparencia", periodo="2025",
            procedimiento="captura_dpe_mensual", version_procedimiento="v1",
            modelo="claude-haiku-4-5-20251001", tipo="calibracion")
r = c.resumen()
for campo in ("municipio", "fuente", "periodo", "procedimiento",
              "version_procedimiento", "modelo", "inicio", "id"):
    _check(bool(r.get(campo)), f"registra «{campo}»")


print("\n[2/4] El costo se calcula y se conserva la tarifa usada")
c.tokens_entrada, c.tokens_salida = 1_000_000, 200_000
esperado = round(1.00 + 0.2 * 5.00, 6)          # 1M entrada + 200k salida
_check(abs(c.costo_usd() - esperado) < 1e-9,
       f"costo de 1M+200k con Haiku = ${c.costo_usd()}",
       f"dio {c.costo_usd()} y debía dar {esperado}")

c.cerrar(Estado.CAPTURADA, documentos=12)
_check(c.tarifa_usada == TARIFAS["claude-haiku-4-5-20251001"],
       "guarda la tarifa vigente al cerrar",
       "sin la tarifa guardada, un cambio de precio reescribiría el costo "
       "histórico de todas las corridas anteriores")
_check(c.duracion_s() is not None, "registra la duración")

local = Corrida(municipio="130801", fuente="transparencia", periodo="2025",
                procedimiento="p", version_procedimiento="v1",
                modelo="local-gguf")
local.tokens_entrada = 5_000_000
_check(local.costo_usd() == 0.0, "la inferencia local no cuesta nada")


print("\n[3/4] Lo calibrado NO se publica, aunque su estado lo permita")
cal = Corrida(municipio="130801", fuente="transparencia", periodo="2025",
              procedimiento="p", version_procedimiento="v1", tipo="calibracion",
              estado=Estado.VALIDADA.value)
_check(not cal.es_publicable(),
       "corrida de calibración con estado «validada» → NO publicable",
       "una corrida de calibración se estaría publicando: sus cifras saldrían "
       "de un procedimiento que todavía se estaba probando (ADR-042 §5-bis)")

prod = Corrida(municipio="130801", fuente="transparencia", periodo="2025",
               procedimiento="p", version_procedimiento="v1", tipo="produccion",
               estado=Estado.VALIDADA.value)
_check(prod.es_publicable(), "corrida de producción validada → publicable")

for e in (Estado.CAPTURADOR_DEGRADADO, Estado.FUENTE_NO_DISPONIBLE,
          Estado.PENDIENTE_VALIDACION):
    p = Corrida(municipio="1", fuente="f", periodo="2025", procedimiento="p",
                version_procedimiento="v1", tipo="produccion", estado=e.value)
    _check(not p.es_publicable(),
           f"producción con «{e.value}» → NO publicable")


print("\n[4/4] El gasto del mes se puede consultar")
from app.observatorio.corrida import gasto_del_mes                # noqa: E402
from datetime import datetime, timezone                           # noqa: E402
hoy = datetime.now(timezone.utc)
g = gasto_del_mes(hoy.year, hoy.month)
_check("total_usd" in g and "por_modelo" in g and "corridas" in g,
       f"gasto del mes: {g['corridas']} corrida(s) · ${g['total_usd']}")
_check(g["corridas"] >= 1, "la corrida de prueba quedó registrada",
       "una corrida cerrada no aparece en la bitácora: el registro no está "
       "escribiendo, y el costo real sería invisible")


print("\n" + "=" * 68)
if fallas:
    print(f"  {len(fallas)} FALLA(S) — la trazabilidad de corridas no se sostiene")
    for f in fallas:
        print(f"     - {f}")
    print("=" * 68)
    sys.exit(1)
print("  TODO OK — toda corrida es repetible y lo calibrado no se publica")
print("=" * 68)
