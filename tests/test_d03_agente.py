# -*- coding: utf-8 -*-
"""
tests/test_d03_agente.py — d03 como agente de dominio gobernado
════════════════════════════════════════════════════════════════════════════════
Tercer dominio migrado (ADR-053 §6). Los criterios del §5 son los mismos, y aquí
se comprueba algo distinto de lo que comprobaron d01 y d02:

    d01   estrenó el molde
    d02   le añadió `motor_sha256` — un motor que delega declara qué lógica leyó
    d03   **no descubre nada nuevo**

Que el tercero no añada nada al patrón es el resultado que hacía falta: el molde
dejó de cambiar con cada dominio. Y entra con el escalón 4 ya cerrado, cosa que
d01 y d02 recibieron después de migrar.

Este archivo mezcla criterios y ataques a propósito: con el patrón estable, no
hace falta separarlos como en el piloto.

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
from app.agents.d03 import motor as M                     # noqa: E402


def _hay_motor() -> bool:
    return M._ENRICHER_PATH.exists()


# ── CRITERIO 3 · el verificador tiene quien lo respalde ───────────────────────
def test_d03_lee_el_mandato_sin_recalcularlo(gold_master):
    """Acredita a `d03.motor.leer_metricas`. La propiedad: d03 **lee** lo que el
    enricher produce (Reglas de Oro 1 y 4), no lo deriva."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    m = M.leer_metricas()
    assert m["status"] == "ok"
    assert m["naturaleza"] == "INMUTABLE"
    assert "NO recalculado" in m["fuente"]
    for clave in ("incorporacion_pct", "calidad_ife_pct",
                  "auditoria_canon_coherente", "autoridades_total"):
        assert clave in m, f"falta «{clave}»"


# ── CRITERIOS 1, 2 y 4 (escalón) ──────────────────────────────────────────────
def test_d03_declara_sujeto_artefacto_y_no_lleva_reloj(gold_master):
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    pr = M.leer_metricas()["procedencia"]
    assert pr["sujeto_huella"] == S.huella()
    for reloj in ("sellado", "generado", "fecha", "timestamp"):
        assert reloj not in pr

    s = M.sostener_incorporacion()
    assert s.peso == P.HECHO_VERIFICABLE, f"faltan: {s.faltan}"
    assert s.procedencia.artefacto, "d03 no declara con qué comprobar su evidencia"
    assert P.evidencia_corresponde(s.procedencia) is True


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_identidad_alterar_el_sujeto_cambia_lo_afirmado(gold_master):
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    perfil = S._SUJETOS / f"{S.POR_DEFECTO}.json"
    respaldo = perfil.read_bytes()
    antes = M.leer_metricas()["procedencia"]["sujeto_huella"]
    try:
        d = json.loads(respaldo.decode("utf-8"))
        d["identidad_en_fuentes"]["dominio_web"] = "otro-gad.gob.ec"
        perfil.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        S.cargar.cache_clear()
        despues = M.leer_metricas()["procedencia"]["sujeto_huella"]
    finally:
        perfil.write_bytes(respaldo)
        S.cargar.cache_clear()
    assert antes != despues


def test_ataque_evidencia_un_hash_ajeno_degrada(gold_master):
    """El escalón 4, que d03 recibe cerrado de fábrica."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    import dataclasses

    s = M.sostener_incorporacion()
    falseada = dataclasses.replace(s.procedencia, evidencia="0000000000000000")
    assert P.evidencia_corresponde(falseada) is False
    assert P.sostener("x", falseada).peso == P.HALLAZGO_DE_VERIFICABILIDAD


def test_ataque_equivalencia_d03_no_transforma_lo_que_el_enricher_produce(gold_master):
    """Lo devuelto debe ser idénticamente lo que `build_block()` produjo. Un solo
    redondeo de más sería recalcular."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")

    bloque = M._cargar_enricher().build_block()
    m = M.leer_metricas()
    for devuelto, original in (
            (m["incorporacion_pct"], bloque["incorporacion"]["pct"]),
            (m["calidad_ife_pct"], bloque["calidad"]["pct"]),
            (m["autoridades_total"], bloque["autoridades"]["total"])):
        assert devuelto == original, (
            f"d03 devolvió {devuelto} donde el enricher produjo {original}")


def test_ataque_grado_no_sube_sin_evidencia():
    vacia = P.Procedencia(fuente="Gold Master vía enricher",
                          sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}")
    for pretendido in (P.HECHO_VERIFICABLE, P.HALLAZGO_DE_VERIFICABILIDAD):
        assert P.sostener("x", vacia, pretendido).peso == P.NO_DETERMINABLE


# ── LO QUE d03 CONFIRMA DEL EJE ───────────────────────────────────────────────
def test_los_tres_dominios_migrados_leen_el_mismo_gold_master():
    """d03 se suma al eje que d01 y d02 abrieron. **Y aquí importa más**: el
    `META_CATALOGO` decía que d03 no comparte fuente con nadie salvo la plantilla
    del orquestador —fue la razón de ponerlo tercero y no segundo (ADR-053 §6)—.

    Lee el mismo Excel, pero eso **no lo convierte en interlocutor**: comparten
    el artefacto, no la pregunta. d01↔d02 se consultan por la cédula
    presupuestaria; d03 no tiene qué preguntarles todavía."""
    if not _hay_motor():
        pytest.skip("enricher no accesible")
    from app.agents.d01 import motor as D1
    from app.agents.d02 import motor as D2

    if not D1._GM_DEFAULT.exists():
        pytest.skip("Gold Master no accesible")

    shas = {d: m["evidencia_sha256"] for d, m in
            (("d01", D1.leer_metricas()), ("d02", D2.leer_metricas()),
             ("d03", M.leer_metricas()))}
    assert len(set(shas.values())) == 1, (
        f"los dominios migrados declaran evidencias distintas del mismo Gold "
        f"Master: {shas}")
