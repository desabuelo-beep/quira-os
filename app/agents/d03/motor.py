"""
app/agents/d03/motor.py — Lectura del motor (NO recálculo)
=========================================================================
Responsabilidad única: LEER incorporación + calidad (IFE) + señal SAT-III
de d03 del Gold Master. Envuelve `scripts/enrich_mandato.py` — el
enricher YA existe, YA está en producción, YA absorbió la curación del
canon (PCD-D03: rótulo corregido, estado de verificación como dato,
Clasificación_IFE como fórmula viva). Este módulo NO reimplementa esa
lógica — la importa (Regla 7).

REGLA 1/4: el IFE, el conteo de incorporación y el centinela los calcula
el Gold Master / el enricher curado. Este módulo nunca recalcula.
"""
from __future__ import annotations

import importlib.util
import pathlib
from typing import Any

_ENRICHER_PATH = pathlib.Path("scripts/enrich_mandato.py")


def _cargar_enricher():
    spec = importlib.util.spec_from_file_location("enrich_mandato", _ENRICHER_PATH)
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
        return P.de_generacion("d03.motor",
                               f"{S.POR_DEFECTO} {S.nombre_corto()}", S.huella())
    except Exception:                                    # noqa: BLE001
        return {"etapa": "d03.motor", "estado": "sujeto_no_acreditado_por_la_cadena"}


def leer_metricas() -> dict[str, Any]:
    """Lee (no calcula) incorporación + calidad + auditoría del canon.

    MIGRADO A AGENTE DE DOMINIO (2026-08-30 · ADR-053, tercer dominio). El molde
    llega ya certificado: d01 lo estrenó, d02 le añadió `motor_sha256` —porque
    un motor que delega debe declarar qué lógica leyó— y el escalón 4 cerró la
    correspondencia evidencia↔artefacto antes de que d03 entrara.

    **d03 es el primero que no descubre nada nuevo del molde**, y eso también es
    un resultado: significa que el patrón dejó de cambiar con cada dominio."""
    mod = _cargar_enricher()
    bloque = mod.build_block()
    return {
        "status": "ok",
        "fuente": "scripts/enrich_mandato.py (leído, NO recalculado — Regla 1/4)",
        "naturaleza": "INMUTABLE",
        "evidencia_sha256": _sha(pathlib.Path(mod.EXCEL))[:16],
        "motor_sha256": _sha(_ENRICHER_PATH)[:16],
        "artefacto": str(pathlib.Path(mod.EXCEL)),
        "procedencia": _procedencia_de_lectura(),
        "incorporacion_pct": bloque["incorporacion"]["pct"],
        "incorporacion_total": bloque["incorporacion"]["total"],
        "incorporacion_con_meta": bloque["incorporacion"]["con_meta"],
        "incorporacion_pct_verificado": bloque["incorporacion"]["pct_verificado"],
        "calidad_ife_pct": bloque["calidad"]["pct"],
        "calidad_clasificacion": bloque["calidad"]["clasificacion"],
        "auditoria_canon_coherente": bloque["auditoria_canon"]["coherente"],
        "autoridades_sin_verificar": bloque["autoridades"]["sin_verificar"],
        "autoridades_total": bloque["autoridades"]["total"],
    }


def sostener_incorporacion():
    """La incorporación del mandato **como afirmación con su cadena**.

    Mismo contrato que `d01.sostener_ipe` y `d02.sostener_isp`, con el escalón 4
    incluido desde el primer día: declara el artefacto, no sólo su hash."""
    import datetime as _dt

    from app.agents import procedencia as P, sujeto as S

    try:
        m = leer_metricas()
    except Exception as exc:                             # noqa: BLE001
        return P.sostener(
            f"no fue posible leer la incorporación del mandato: {type(exc).__name__}",
            P.Procedencia(fuente="Gold Master vía enrich_mandato.py",
                          sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}"),
            P.HALLAZGO_DE_VERIFICABILIDAD)

    return P.sostener(
        f"la incorporación del mandato al POA es {m['incorporacion_pct']}",
        P.Procedencia(
            fuente=f"Gold Master vía `enrich_mandato.py` (motor {m['motor_sha256']})",
            captura=_dt.date.today().isoformat(),
            estado_adquisicion="leido_del_motor",
            evidencia=m["evidencia_sha256"],
            artefacto=m["artefacto"],
            verificador="d03.motor.leer_metricas",
            prueba_del_verificador="test_d03_lee_el_mandato_sin_recalcularlo",
            sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}",
        ))
