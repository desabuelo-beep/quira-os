"""
app/agents/d02/motor.py — Lectura del motor (NO recálculo)
=========================================================================
Responsabilidad única: LEER las 4 capacidades + 3 señales SAT de d02 del
Gold Master. Envuelve `scripts/enrich_presupuesto.py` — el enricher YA
existe, YA está en producción, YA corrige el bug histórico del PCD-D02
(ISP leído de la columna correcta). Este módulo NO reimplementa esa
lógica — la importa (Regla 7: no duplicar lo que ya existe).

REGLA 1/4 (inviolables): ISP, Ti, fondos externos y las 3 señales SAT las
calcula el Gold Master. Este módulo nunca recalcula — solo lee.
"""
from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

_ENRICHER_PATH = pathlib.Path("scripts/enrich_presupuesto.py")


def _cargar_enricher():
    spec = importlib.util.spec_from_file_location("enrich_presupuesto", _ENRICHER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sha(path: pathlib.Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def _procedencia_de_lectura() -> dict[str, Any]:
    """De quién es esta lectura. **Sin reloj** (ADR-053 §5.2)."""
    try:
        from app.agents import procedencia as P, sujeto as S
        return P.de_generacion("d02.motor",
                               f"{S.POR_DEFECTO} {S.nombre_corto()}", S.huella())
    except Exception:                                    # noqa: BLE001
        return {"etapa": "d02.motor", "estado": "sujeto_no_acreditado_por_la_cadena"}


def leer_metricas() -> dict[str, Any]:
    """Lee (no calcula) las 4 capacidades + 3 señales SAT vía el enricher real.

    MIGRADO A AGENTE DE DOMINIO (2026-08-26 · ADR-053, tras el piloto d01).

    ⚠️ LO QUE d02 AÑADE AL MOLDE, y d01 no necesitaba: **este motor DELEGA**, y
    por eso su evidencia tiene dos partes que no son la misma cosa.

        evidencia_sha256   el Gold Master · QUÉ DATOS se leyeron
        motor_sha256       el enricher    · QUÉ LÓGICA los leyó

    Con el mismo Excel, un enricher distinto puede producir otro resultado —el
    propio `enrich_presupuesto.py` corrigió en su día el bug del ISP leído de la
    columna equivocada (PCD-D02)—. Registrar sólo el Gold Master dejaría esa
    diferencia invisible: dos afirmaciones con la misma evidencia declarada y
    distinto número.

    Es la misma lección de siempre, un escalón más arriba: **la identidad de
    quien lee es parte de la procedencia de lo leído.**"""
    mod = _cargar_enricher()
    bloque = mod.build_block()
    return {
        "status": "ok",
        "fuente": "scripts/enrich_presupuesto.py (leído, NO recalculado — Regla 1/4)",
        "naturaleza": "INMUTABLE",
        "evidencia_sha256": _sha(pathlib.Path(mod.EXCEL))[:16],
        "motor_sha256": _sha(_ENRICHER_PATH)[:16],
        "procedencia": _procedencia_de_lectura(),
        "sostenibilidad_isp_pct": bloque["isp"]["global_pct"],
        "absorcion_ti_pct": bloque["ejecucion"]["ti_pct"],
        "movilizacion_usd": bloque["captacion"]["total_externo"],
        "movilizacion_n_convenios": bloque["captacion"]["n_convenios"],
        "elegibilidad_pnd_pct": bloque["elegibilidad"]["alineacion_pnd_pct"],
        "elegibilidad_icods_pct": bloque["ods"]["icods_pct"],
        "sat_senales": bloque["sat_presupuestario"]["senales"],
        "sat_n_activas": bloque["sat_presupuestario"]["n_activas"],
    }


def sostener_isp():
    """El ISP **como afirmación con su cadena**, no como porcentaje suelto.

    Mismo contrato que `d01.motor.sostener_ipe` — es lo que hace del molde un
    molde y no una implementación repetida."""
    import datetime as _dt

    from app.agents import procedencia as P, sujeto as S

    try:
        m = leer_metricas()
    except Exception as exc:                             # noqa: BLE001
        # Que el motor no se pueda leer NO dice nada del sujeto: dice algo del
        # instrumento (ADR-042 §6 · «no existe» ≠ «no pude obtener»).
        return P.sostener(
            f"no fue posible leer el ISP del motor: {type(exc).__name__}",
            P.Procedencia(fuente="Gold Master vía enrich_presupuesto.py",
                          sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}"),
            P.HALLAZGO_DE_VERIFICABILIDAD)

    return P.sostener(
        f"la sostenibilidad presupuestaria (ISP) es {m['sostenibilidad_isp_pct']}",
        P.Procedencia(
            fuente=f"Gold Master vía `enrich_presupuesto.py` "
                   f"(motor {m['motor_sha256']})",
            captura=_dt.date.today().isoformat(),
            estado_adquisicion="leido_del_motor",
            evidencia=m["evidencia_sha256"],
            # ESCALÓN 4: el Gold Master que el enricher abrió, no el que se suponga.
            artefacto=str(pathlib.Path(_cargar_enricher().EXCEL)),
            verificador="d02.motor.leer_metricas",
            prueba_del_verificador="test_d02_lee_las_capacidades_sin_recalcularlas",
            sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}",
        ))
