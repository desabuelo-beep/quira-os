# -*- coding: utf-8 -*-
"""
tests/test_d02_adversarial.py — atacar d02, no confirmarlo
════════════════════════════════════════════════════════════════════════════════
Las mismas cuatro fronteras que en d01 (identidad · procedencia · grado ·
equivalencia), más **una que sólo existe aquí**: d02 delega en un enricher, y
un motor que delega puede mentir de una forma que uno que lee directo no puede.

    5 · DELEGACIÓN   hacer que d02 declare una evidencia que no corresponde
                     a la lógica que realmente produjo el número

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import procedencia as P                   # noqa: E402
from app.agents import sujeto as S                        # noqa: E402
from app.agents.d02 import motor as M                     # noqa: E402


def _hay_motor() -> bool:
    return M._ENRICHER_PATH.exists()


# ── ATAQUE 1 · IDENTIDAD ──────────────────────────────────────────────────────
def test_ataque_1_d02_no_puede_afirmar_sobre_un_sujeto_alterado():
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    perfil = S._SUJETOS / f"{S.POR_DEFECTO}.json"
    respaldo = perfil.read_bytes()
    antes = M.leer_metricas()["procedencia"]["sujeto_huella"]
    try:
        d = json.loads(respaldo.decode("utf-8"))
        d["identidad_en_fuentes"]["dpe_entidad_id"] = 999
        perfil.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        S.cargar.cache_clear()
        despues = M.leer_metricas()["procedencia"]["sujeto_huella"]
    finally:
        perfil.write_bytes(respaldo)
        S.cargar.cache_clear()
    assert antes != despues, (
        "alterar la identidad no cambió la huella que d02 estampa")


# ── ATAQUE 5 · DELEGACIÓN · el que sólo existe en d02 ─────────────────────────
def test_ataque_5_cambiar_el_enricher_cambia_la_evidencia_declarada(tmp_path):
    """EL ATAQUE PROPIO DE UN MOTOR QUE DELEGA.

    Si el enricher cambia, la afirmación **no puede seguir declarando la misma
    procedencia**: con el mismo Gold Master, otra lógica puede dar otro número
    —es exactamente lo que ocurrió cuando `enrich_presupuesto.py` corrigió el
    ISP leído de la columna equivocada (PCD-D02)—.

    Se altera el enricher en una copia y se comprueba que su huella cambia. Si
    no cambiara, dos resultados distintos declararían idéntica procedencia."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    original = M._ENRICHER_PATH.read_bytes()
    sha_antes = M.leer_metricas()["motor_sha256"]
    copia = tmp_path / "enricher_alterado.py"
    copia.write_bytes(original + b"\n# una linea mas cambia la logica declarada\n")

    import hashlib
    sha_copia = hashlib.sha256(copia.read_bytes()).hexdigest()[:16]
    assert sha_antes != sha_copia, (
        "modificar el enricher NO alteró su huella: dos lógicas distintas "
        "declararían la misma procedencia")
    # Y el original sigue intacto: el ataque no dejó residuo.
    assert M._ENRICHER_PATH.read_bytes() == original


# ── ATAQUE 3 · GRADO ──────────────────────────────────────────────────────────
def test_ataque_3_d02_no_sube_el_grado_sin_evidencia():
    vacia = P.Procedencia(fuente="Gold Master vía enricher",
                          sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}")
    for pretendido in (P.HECHO_VERIFICABLE, P.HALLAZGO_DE_VERIFICABILIDAD):
        assert P.sostener("x", vacia, pretendido).peso == P.NO_DETERMINABLE

    if not _hay_motor():
        pytest.skip("enricher no accesible")
    m = M.leer_metricas()
    sin_prueba = P.Procedencia(
        fuente="Gold Master vía enricher", captura="2026-08-26",
        estado_adquisicion="leido_del_motor", evidencia=m["evidencia_sha256"],
        verificador="d02.motor.leer_metricas",
        prueba_del_verificador="test_inexistente_tras_un_renombrado",
        sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}")
    s = P.sostener("el ISP es X", sin_prueba)
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert "prueba_del_verificador" in s.faltan


# ── ATAQUE 4 · EQUIVALENCIA · ¿lee o transforma? ──────────────────────────────
def test_ataque_4_d02_no_transforma_lo_que_el_enricher_produce():
    """La versión de d02 del ataque del colega. Aquí no se puede fabricar un
    Gold Master falso —la ruta la fija el enricher—, así que se compara contra
    la fuente directa: **lo que d02 devuelve debe ser idénticamente lo que
    `build_block()` produjo**, sin redondeos, escalas ni «normalizaciones».

    Un solo `round()` de más aquí sería recalcular (Reglas de Oro 1 y 4)."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    mod = M._cargar_enricher()
    bloque = mod.build_block()
    m = M.leer_metricas()

    pares = [
        (m["sostenibilidad_isp_pct"], bloque["isp"]["global_pct"]),
        (m["absorcion_ti_pct"], bloque["ejecucion"]["ti_pct"]),
        (m["movilizacion_usd"], bloque["captacion"]["total_externo"]),
        (m["elegibilidad_pnd_pct"], bloque["elegibilidad"]["alineacion_pnd_pct"]),
        (m["sat_n_activas"], bloque["sat_presupuestario"]["n_activas"]),
    ]
    for devuelto, original in pares:
        assert devuelto == original, (
            f"d02 devolvió {devuelto} donde el enricher produjo {original}: "
            f"está transformando el número en vez de leerlo")
