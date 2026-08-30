"""
app/agents/d09/motor.py — Lectura del Gold Master (etapa 3 del pipeline)
=========================================================================
d09 es el primer dominio con DOS fuentes de lectura distintas (Regla 1/4:
nunca recalcular, solo leer):

  · fidelidad_narrativa + cpccs_brecha → EN VIVO desde el Excel, envolviendo
    `scripts/enrich_rdc.py::build_block()` (mismo patrón que d01/d02/d03).
  · serie_rendiciones + cumplimiento_actual + aportes → NO viven en el
    Excel (aportes sí parte de H10c, pero el cruce es embeddings, no
    fórmula); se extraen por `scripts/enrich_rdc_docx.py` y
    `scripts/enrich_aportes.py`, que hacen I/O de archivo y MERGE directo
    al snapshot (no exponen una función pura de lectura). Se leen del
    snapshot ya persistido (`data/gm_snapshot.json['rendicion']`) —
    aceptado explícitamente así en PCD-D09 ("deriva de informes
    verificados; estampar en el Gold Master es mejora futura").

BUG ENCONTRADO Y CORREGIDO (2026-07-23, migración d09): `enrich_rdc.py`
sobrescribía TODO `snap["rendicion"]` (`snap["rendicion"] = block`), lo que
borraba `aportes`/`serie`/`cumplimiento_actual` si se re-ejecutaba solo.
Corregido a merge (`rend.update(block)`). Ver EVIDENCIA_d09_2026-07-23.md.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
from typing import Any

_ENRICHER_PATH = pathlib.Path("scripts/enrich_rdc.py")
_SNAPSHOT_PATH = pathlib.Path("data/gm_snapshot.json")


def _cargar_enricher():
    spec = importlib.util.spec_from_file_location("enrich_rdc", _ENRICHER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sha(path: pathlib.Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()[:16]


def _procedencia_de_lectura() -> dict[str, Any]:
    """De quién es esta lectura. **Sin reloj** (ADR-053 §5.2)."""
    try:
        from app.agents import procedencia as P, sujeto as S
        return P.de_generacion("d09.motor",
                               f"{S.POR_DEFECTO} {S.nombre_corto()}", S.huella())
    except Exception:                                    # noqa: BLE001
        return {"etapa": "d09.motor", "estado": "sujeto_no_acreditado_por_la_cadena"}


def _raiz_de_datos() -> pathlib.Path:
    """La única puerta a los datos (gate REGLAS · 0 rutas fijas)."""
    try:
        from config import DATOS_DIR
        return pathlib.Path(DATOS_DIR)
    except Exception:                                    # noqa: BLE001
        import os
        return pathlib.Path(os.environ.get("QUIRA_DATOS", "."))


def leer_metricas() -> dict[str, Any]:
    mod = _cargar_enricher()
    bloque_vivo = mod.build_block()  # fidelidad (H34b) + cpccs (H31), fresco del Excel

    snap = json.loads(_SNAPSHOT_PATH.read_text(encoding="utf-8"))
    persistido = snap.get("rendicion", {})

    fid = bloque_vivo["fidelidad"]
    return {
        "status": "ok",
        # DOS EVIDENCIAS, DECLARADAS POR SEPARADO (2026-08-30 · migración d09).
        # No es un detalle de formato: lo vivo es de primera mano y lo
        # persistido es un derivado de los informes DOCX. Un solo `artefacto`
        # para ambas **inflaría la más débil hasta la más fuerte**, que es
        # exactamente la operación que este sistema le prohíbe al sujeto.
        "evidencia_sha256": _sha(pathlib.Path(mod.EXCEL)),
        "motor_sha256": _sha(_ENRICHER_PATH),
        "artefacto": str(pathlib.Path(mod.EXCEL)),
        "snapshot_sha256": _sha(_SNAPSHOT_PATH),
        "snapshot_artefacto": str(_SNAPSHOT_PATH),
        "origen_serie": persistido.get("_origen_serie", {}),
        "procedencia": _procedencia_de_lectura(),
        "fuente_viva": "scripts/enrich_rdc.py (leído, NO recalculado — Regla 1/4)",
        "fuente_persistida": "data/gm_snapshot.json['rendicion'] (extracción DOCX, ver PCD-D09)",
        "fidelidad_naturaleza": "ÍNDICE — evaluación experta trazable, no cómputo automático",
        "fidelidad_global_pct": fid["global_pct"],
        "fidelidad_n_afirmaciones": fid["n_afirmaciones"],
        "fidelidad_n_alta": fid["n_alta"],
        "fidelidad_n_baja": fid["n_baja"],
        "fidelidad_cobertura": "ejercicio 2024 (2025 pendiente de NLP sobre video — PCD-D09)",
        "cpccs_marco_legal": bloque_vivo["cpccs"]["marco_legal"],
        "cpccs_brecha_compromisos": bloque_vivo["cpccs"]["brecha_compromisos"] or "sin dato",
        "serie_rendiciones": persistido.get("serie", []),
        "cumplimiento_actual": persistido.get("cumplimiento_actual", {}),
        "aportes_naturaleza": "HECHO — cruce semiautomático H10c×POA, evaluación experta trazable (metodología v0.3 pendiente de aval formal)",
        "aportes_total": persistido.get("aportes", {}).get("total"),
        "aportes_validados": persistido.get("aportes", {}).get("n_validados"),
        "aportes_por_estado": persistido.get("aportes", {}).get("por_estado", {}),
    }


# ══════════════════════════════════════════════════════════════════════════════
# UNA PROCEDENCIA POR AFIRMACIÓN · lo que d09 le enseñó al molde (2026-08-30)
# ══════════════════════════════════════════════════════════════════════════════
# d01, d02 y d03 tienen un `sostener_X()` cada uno, y eso bastaba porque cada uno
# tiene UNA fuente y UNA métrica principal. d09 rompe el supuesto: afirma sobre
# la fidelidad —leída en vivo del Gold Master— y sobre la serie de rendiciones
# —derivada de tres informes DOCX vía snapshot—, y esas dos evidencias **no
# valen lo mismo ni se comprueban igual**.
#
# Si hubiera un solo `sostener_rendicion()` con un solo `artefacto`, la serie se
# acreditaría con el hash del Excel: un artefacto que **no contiene el dato**. La
# afirmación más débil quedaría vestida con la procedencia de la más fuerte.
#
#     la procedencia es por AFIRMACIÓN, no por dominio
#
# Y al bajar a la afirmación concreta, la aridad que parecía un problema —tres
# DOCX, ¿cuál es «el» artefacto?— se disuelve: «la rendición de 2023 tuvo 201
# asistentes» deriva de un único archivo.

def sostener_fidelidad():
    """La fidelidad narrativa: evidencia **de primera mano** del Gold Master.

    Mismo contrato que d01/d02/d03 — se lee del motor y se declara el artefacto
    que se leyó (escalón 4). No declara origen porque no deriva de nada."""
    import datetime as _dt

    from app.agents import procedencia as P, sujeto as S

    try:
        m = leer_metricas()
    except Exception as exc:                             # noqa: BLE001
        return P.sostener(
            f"no fue posible leer la fidelidad narrativa: {type(exc).__name__}",
            P.Procedencia(fuente="Gold Master vía enrich_rdc.py",
                          sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}"),
            P.HALLAZGO_DE_VERIFICABILIDAD)

    return P.sostener(
        f"la fidelidad narrativa del informe es {m['fidelidad_global_pct']}",
        P.Procedencia(
            fuente=f"Gold Master vía `enrich_rdc.py` (motor {m['motor_sha256']})",
            captura=_dt.date.today().isoformat(),
            estado_adquisicion="leido_del_motor",
            evidencia=m["evidencia_sha256"],
            artefacto=m["artefacto"],
            verificador="d09.motor.leer_metricas",
            prueba_del_verificador="test_d09_lee_la_fidelidad_sin_recalcularla",
            sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}",
        ))


def sostener_serie(periodo: str):
    """La rendición de UN periodo: evidencia **derivada**, y lo dice.

    Aquí se estrena el escalón 7. El artefacto leído es el snapshot; el origen
    es el informe DOCX de ese año. Acreditar sólo el snapshot demostraría que se
    leyó bien un archivo intermedio — no que ese archivo venga del informe que
    dice. Los dos tramos se declaran, y el que falte se ve.

    ⚠️ La captura fue **manual**: los informes se descargaron a mano del portal
    del CPCCS, no los trajo un adquiridor de QUIRA. Eso no los hace menos
    válidos, pero es una propiedad de la cadena que quien lea la afirmación
    tiene derecho a conocer, y que hasta hoy no constaba en ninguna parte."""
    import datetime as _dt

    from app.agents import procedencia as P, sujeto as S

    sujeto = f"{S.POR_DEFECTO} {S.nombre_corto()}"
    try:
        m = leer_metricas()
        fila = next((f for f in m["serie_rendiciones"]
                     if str(f.get("periodo")) == str(periodo)), None)
    except Exception as exc:                             # noqa: BLE001
        return P.sostener(
            f"no fue posible leer la serie de rendiciones: {type(exc).__name__}",
            P.Procedencia(fuente="informes CPCCS vía snapshot", sujeto=sujeto),
            P.HALLAZGO_DE_VERIFICABILIDAD)

    if fila is None:
        # No se afirma que no hubo rendición: se afirma que no consta en lo
        # leído. La distinción es la razón de ser de todo el dominio.
        return P.sostener(
            f"no consta rendición de cuentas del periodo {periodo} en lo leído",
            P.Procedencia(fuente="informes CPCCS vía snapshot",
                          captura=_dt.date.today().isoformat(),
                          estado_adquisicion="periodo_no_presente_en_la_fuente",
                          sujeto=sujeto),
            P.HALLAZGO_DE_VERIFICABILIDAD)

    org = (m["origen_serie"] or {}).get(str(periodo), {})
    deriva = str(_raiz_de_datos() / org["archivo"]) if org.get("archivo") else ""
    return P.sostener(
        f"la rendición de cuentas del periodo {periodo} registró "
        f"{fila.get('asistentes')} asistentes y {fila.get('n_componentes')} componentes",
        P.Procedencia(
            fuente=f"informe CPCCS N° {fila.get('informe_n')} (descarga manual del portal)",
            captura=_dt.date.today().isoformat(),
            estado_adquisicion="derivado_de_informe_documental",
            evidencia=m["snapshot_sha256"],
            artefacto=m["snapshot_artefacto"],
            deriva_de=deriva,
            origen_sha=org.get("sha256", ""),
            verificador="d09.motor.leer_metricas",
            prueba_del_verificador="test_d09_lee_la_serie_sin_recalcularla",
            sujeto=sujeto,
        ))
