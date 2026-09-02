# -*- coding: utf-8 -*-
"""
tests/test_d09_agente.py — d09 y el escalón 7: lo leído no siempre es la fuente
════════════════════════════════════════════════════════════════════════════════
Cuarto dominio migrado (ADR-053 §6). d03 fue el primero que **no descubrió nada
nuevo** del molde; d09 rompe esa racha, y era su papel: es el dominio heterogéneo
—dos fuentes, una de ellas un derivado persistido—, y por eso se dejó tarde.

LO QUE d09 OBLIGÓ A RESOLVER:

 1 · **La procedencia es por AFIRMACIÓN, no por dominio.** d01..d03 lo
     escondieron porque cada uno tiene una fuente y una métrica. d09 afirma
     sobre la fidelidad (Gold Master, en vivo) y sobre la serie de rendiciones
     (tres informes DOCX vía snapshot). Un solo `sostener_X()` con un solo
     artefacto habría acreditado la serie con el hash del Excel — un artefacto
     que **no contiene el dato**.

 2 · **El escalón 7.** Acreditar el snapshot demuestra que se leyó bien el
     snapshot; no demuestra que venga de los informes que dice.

         DOCX 2023/24/25 → enrich_rdc_docx → gm_snapshot.json → d09.motor
         └──── tramo 1: escalón 7 ──────┘   └─ tramo 2: escalón 4 ─┘

 3 · **Un enricher que no encuentra su fuente destruía la evidencia.** No es
     teórico: costó los tres años de la serie en una corrida real de esta misma
     sesión, y se recuperaron del control de versiones.

Dylus Lab © 2026
"""
from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.agents import procedencia as P                   # noqa: E402
from app.agents import sujeto as S                        # noqa: E402
from app.agents.d09 import motor as M                     # noqa: E402


def _hay_motor() -> bool:
    return M._ENRICHER_PATH.exists() and M._SNAPSHOT_PATH.exists()


# ── CRITERIO 3 · el verificador tiene quien lo respalde ───────────────────────
def test_d09_lee_la_fidelidad_sin_recalcularla(gold_master):
    """Acredita `d09.motor.leer_metricas` para la mitad VIVA: se lee del Gold
    Master vía enricher, no se deriva (Reglas de Oro 1 y 4)."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    m = M.leer_metricas()
    assert m["status"] == "ok"
    assert "NO recalculado" in m["fuente_viva"]
    for clave in ("fidelidad_global_pct", "fidelidad_n_afirmaciones",
                  "evidencia_sha256", "motor_sha256"):
        assert clave in m, f"falta «{clave}»"


def test_d09_lee_la_serie_sin_recalcularla(gold_master):
    """Acredita el mismo verificador para la mitad PERSISTIDA, que es otra cosa:
    tres informes documentales que d09 no vuelve a extraer."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    m = M.leer_metricas()
    serie = m["serie_rendiciones"]
    assert serie, "la serie está vacía: o no se extrajo, o algo la sobrescribió"
    for fila in serie:
        for clave in ("periodo", "informe_n", "asistentes", "n_componentes"):
            assert clave in fila, f"la serie no declara «{clave}»"


# ── LA PROPIEDAD NUEVA · una procedencia por afirmación ───────────────────────
def test_las_dos_afirmaciones_no_comparten_procedencia(gold_master):
    """EL HALLAZGO DE d09. Dos afirmaciones del mismo dominio, con evidencias
    distintas, comprobadas contra artefactos distintos. Si compartieran
    procedencia, la más débil quedaría vestida con la credencial de la más
    fuerte — la operación que este sistema le prohíbe al sujeto observado."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    fid = M.sostener_fidelidad().procedencia
    ser = M.sostener_serie("2023").procedencia
    assert fid.artefacto != ser.artefacto, (
        "la fidelidad y la serie se acreditan con el mismo artefacto: una de las "
        "dos está usando un archivo que no contiene su dato")
    assert P.evidencia_corresponde(fid) is True
    assert P.evidencia_corresponde(ser) is True


def test_la_serie_se_declara_derivada_y_la_fidelidad_de_primera_mano(gold_master):
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    assert P.de_primera_mano(M.sostener_fidelidad().procedencia) is True
    assert P.de_primera_mano(M.sostener_serie("2023").procedencia) is False


def test_el_escalon_7_comprueba_el_informe_de_origen():
    """La serie señala el DOCX del que deriva, y ese DOCX se comprueba."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    pr = M.sostener_serie("2023").procedencia
    if not pr.deriva_de:
        pytest.skip("el snapshot no declara origen: correr enrich_rdc_docx.py")
    assert P.origen_corresponde(pr) is True
    assert Path(pr.deriva_de).suffix == ".docx"


# ── ATAQUES ───────────────────────────────────────────────────────────────────
def test_ataque_identidad_alterar_el_sujeto_cambia_lo_afirmado(gold_master):
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")
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


def test_ataque_escalon7_un_origen_que_ya_no_esta_degrada_SOLO_la_serie():
    """EL ATAQUE QUE SEPARA LOS DOS TRAMOS, y la razón de que el escalón 7 no
    sea decorativo. Si el informe de origen desaparece, la serie deja de poder
    decir de dónde viene **aunque el snapshot siga íntegro** — y la fidelidad,
    que no deriva de nada, no se ve afectada en absoluto."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    ser = M.sostener_serie("2023").procedencia
    if not ser.deriva_de:
        pytest.skip("el snapshot no declara origen")

    huerfana = dataclasses.replace(ser, deriva_de="/informe/que/ya/no/existe.docx")
    assert P.origen_corresponde(huerfana) is False
    assert P.evidencia_corresponde(huerfana) is True, (
        "el snapshot sigue íntegro: lo que se perdió es el vínculo con su origen")
    assert P.sostener("x", huerfana).peso == P.HALLAZGO_DE_VERIFICABILIDAD

    # La fidelidad no deriva de nada, así que nada de esto la toca.
    assert P.sostener("x", M.sostener_fidelidad().procedencia).peso == P.HECHO_VERIFICABLE


def test_ataque_escalon7_un_origen_falseado_degrada():
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")
    ser = M.sostener_serie("2023").procedencia
    if not ser.deriva_de:
        pytest.skip("el snapshot no declara origen")
    falseada = dataclasses.replace(ser, origen_sha="0000000000000000")
    assert P.origen_corresponde(falseada) is False
    assert P.sostener("x", falseada).peso == P.HALLAZGO_DE_VERIFICABILIDAD


def test_ataque_inflacion_la_serie_no_puede_acreditarse_con_el_excel(gold_master):
    """El ataque directo a la propiedad nueva: vestir la afirmación derivada con
    el artefacto de la de primera mano. El hash del snapshot no corresponde al
    Gold Master, así que la sustitución se detecta."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    m = M.leer_metricas()
    ser = M.sostener_serie("2023").procedencia
    inflada = dataclasses.replace(ser, artefacto=m["artefacto"])
    assert P.evidencia_corresponde(inflada) is False
    assert P.sostener("x", inflada).peso == P.HALLAZGO_DE_VERIFICABILIDAD


def test_ataque_evidencia_un_hash_ajeno_degrada(gold_master):
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")
    s = M.sostener_fidelidad()
    falseada = dataclasses.replace(s.procedencia, evidencia="0000000000000000")
    assert P.evidencia_corresponde(falseada) is False


def test_ataque_grado_no_sube_sin_evidencia():
    vacia = P.Procedencia(fuente="informes CPCCS",
                          sujeto=f"{S.POR_DEFECTO} {S.nombre_corto()}")
    for pretendido in (P.HECHO_VERIFICABLE, P.HALLAZGO_DE_VERIFICABILIDAD):
        assert P.sostener("x", vacia, pretendido).peso == P.NO_DETERMINABLE


def test_ataque_equivalencia_d09_no_transforma_lo_que_lee(gold_master):
    """Ni del enricher vivo ni del snapshot. Un redondeo de más sería recalcular."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    bloque = M._cargar_enricher().build_block()
    snap = json.loads(M._SNAPSHOT_PATH.read_text(encoding="utf-8"))["rendicion"]
    m = M.leer_metricas()
    assert m["fidelidad_global_pct"] == bloque["fidelidad"]["global_pct"]
    assert m["serie_rendiciones"] == snap["serie"]
    assert m["aportes_total"] == snap["aportes"]["total"]


def test_un_periodo_ausente_no_se_afirma_como_falta_de_rendicion(gold_master):
    """La distinción que da sentido al dominio entero, aplicada a sí mismo: que
    un periodo no esté en lo leído **no dice que el GAD no rindiera cuentas**."""
    if not _hay_motor():
        pytest.skip("fuentes de d09 no accesibles")

    s = M.sostener_serie("1998")
    assert "no consta" in s.enunciado
    assert s.peso == P.HALLAZGO_DE_VERIFICABILIDAD
    assert not s.habla_del_sujeto, (
        "una afirmación sobre lo que no encontramos no puede hablar del sujeto")
    for prohibido in ("no rindió", "incumpl", "omitió", "no realizó"):
        assert prohibido not in s.enunciado.lower()


# ── REGRESIÓN DEL DEFECTO DE INTEGRIDAD ───────────────────────────────────────
def test_el_cable_documental_no_escribe_si_no_accede_a_los_informes():
    """REGRESIÓN de un borrado REAL ocurrido en esta sesión.

    `enrich_rdc_docx.py` saltaba los informes que no encontraba y guardaba
    igualmente: tres años de serie desaparecieron sustituidos por listas vacías,
    sin un solo error. Es el colapso que QUIRA persigue afuera —«no lo
    encontré» ≠ «no existe»— cometido adentro y contra los propios datos.

    Se comprueba **estáticamente**, leyendo el guard: ejecutar el cable para
    verificarlo cruzaría la frontera de efectos y, peor, volvería a arriesgar el
    snapshot — que es exactamente como se descubrió."""
    fuente = (RAIZ / "scripts" / "enrich_rdc_docx.py").read_text(encoding="utf-8")
    cuerpo = fuente.split("def main(")[1]
    guard = cuerpo.find("SystemExit")
    escritura = cuerpo.find('open(SNAP, "w"')
    assert guard != -1, "el cable ya no aborta cuando le faltan informes"
    assert 0 < guard < escritura, (
        "el guard quedó DESPUÉS de la escritura: no protege nada")


def test_el_cable_no_asume_el_directorio_actual_como_raiz_de_datos():
    """La causa raíz del borrado. Ejecutado como script, `config` no es
    importable y el respaldo caía a `"."`: toda fuente parecía ausente. Asumir
    una raíz equivocada convierte una falla de importación en un hallazgo falso
    sobre el sujeto."""
    fuente = (RAIZ / "scripts" / "enrich_rdc_docx.py").read_text(encoding="utf-8")
    cabecera = fuente.split("def _txt")[0]
    assert 'QUIRA_DATOS", "."' not in cabecera, (
        "vuelve a asumir el directorio actual como raíz de datos")
    assert "SystemExit" in cabecera, "no aborta cuando se queda sin raíz de datos"
