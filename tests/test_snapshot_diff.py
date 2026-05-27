"""
tests/test_snapshot_diff.py — QUIRA OS · Sprint 3 P2
Snapshot Diff Engine — suite completa de tests

Cobertura:
  - compare_snapshots()         — clasificacion canonica (6 paths)
  - _clasificar()               — logica de clasificacion y prioridades
  - _detectar_sat_iii()         — reincidencia D3 con y sin historial
  - _sat_activas()              — extraccion de codigos SAT (2 formatos)
  - _diff_campos()              — generacion de FieldDiff
  - _field_diff()               — direccion de cada campo
  - _pct()                      — conversion ratio → porcentaje
  - _get()                      — acceso anidado seguro
  - _generar_notas()            — notas doctrinales contextuales
  - detect_reincidence_from_history() — API longitudinal de alto nivel

Todos los tests son offline — sin Supabase, sin Excel, sin filesystem.
Dylus Lab (c) 2026
"""
from __future__ import annotations

import pytest

from app.services.snapshot_diff import (
    DiffResult,
    FieldDiff,
    compare_snapshots,
    detect_reincidence_from_history,
    _get,
    _pct,
    _sat_activas,
    _field_diff,
    _clasificar,
    _detectar_sat_iii,
    _diff_campos,
    _generar_notas,
)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers de fixtures
# ══════════════════════════════════════════════════════════════════════════════

def _snap(
    *,
    fecha_corte: str = "2026-05-25",
    icpi_score: float | None = 0.5356,      # ratio 0-1  (53.56 %)
    d3: float | None = 0.1458,              # ratio 0-1  (14.58 %)
    tgi_score: float | None = 66.85,
    d1: float | None = 0.75,
    d2: float | None = 0.6993,
    d4: float | None = 0.45,
    d5: float | None = 0.83,
    sat_activas: list | None = None,
    sat_alertas: list | None = None,
    riesgo_ponderado: str | None = "ALTO",
    clasif_riesgo: str | None = "ALTO",
    total_activas: int = 3,
    ejecucion_pct: float | None = 0.58,
) -> dict:
    """Snapshot minimal valido para tests del Diff Engine.

    icpi_score y las dimensiones se expresan como ratio (0-1) para simular
    el formato real del pipeline. _pct() los convierte internamente.
    """
    if sat_activas is None:
        sat_activas = ["SAT-III", "SAT-IV", "SAT-V"]
    if sat_alertas is None:
        sat_alertas = []
    return {
        "_meta": {
            "schema_version": "1.0",
            "fecha_corte": fecha_corte,
            "pipeline_version": "1.0.0-test",
        },
        "icpi": {
            "score": icpi_score,
            "clasificacion": "Test",
        },
        "tgi": {
            "score": tgi_score,
            "dimensiones": {
                "d1": d1,
                "d2": d2,
                "d3": d3,
                "d4": d4,
                "d5": d5,
            },
        },
        "sat": {
            "activas": sat_activas,
            "alertas": sat_alertas,
            "riesgo_ponderado": riesgo_ponderado,
            "clasif_riesgo": clasif_riesgo,
            "total_activas": total_activas,
        },
        "financiero": {
            "ejecucion_pct": ejecucion_pct,
        },
    }


def _snap_pct(
    *,
    fecha_corte: str = "2026-05-25",
    icpi_score: float | None = 53.56,       # ya en % (> 1.5)
    d3: float | None = 14.58,
    **kwargs,
) -> dict:
    """Variante donde las metricas ya vienen expresadas en porcentaje."""
    return _snap(fecha_corte=fecha_corte, icpi_score=icpi_score, d3=d3, **kwargs)


# ══════════════════════════════════════════════════════════════════════════════
# 1. Helpers internos: _get y _pct
# ══════════════════════════════════════════════════════════════════════════════

class TestGetHelper:
    def test_top_level_key(self):
        assert _get({"a": 1}, "a") == 1

    def test_nested_two_levels(self):
        assert _get({"a": {"b": 42}}, "a.b") == 42

    def test_nested_three_levels(self):
        assert _get({"x": {"y": {"z": "deep"}}}, "x.y.z") == "deep"

    def test_missing_key_returns_default(self):
        assert _get({"a": 1}, "b") is None

    def test_missing_nested_returns_default(self):
        assert _get({"a": {}}, "a.b", "fallback") == "fallback"

    def test_none_parent_returns_default(self):
        assert _get({"a": None}, "a.b") is None

    def test_empty_dict(self):
        assert _get({}, "a.b.c") is None

    def test_value_none_returns_default(self):
        assert _get({"a": None}, "a") is None


class TestPctHelper:
    def test_ratio_to_pct(self):
        assert _pct(0.5356) == pytest.approx(53.56, rel=1e-4)

    def test_already_pct_passthrough(self):
        # Valores > 1.5 se consideran ya en %
        assert _pct(53.56) == pytest.approx(53.56, rel=1e-4)

    def test_zero_ratio(self):
        assert _pct(0.0) == pytest.approx(0.0)

    def test_one_ratio(self):
        assert _pct(1.0) == pytest.approx(100.0)

    def test_none_returns_none(self):
        assert _pct(None) is None

    def test_negative_ratio(self):
        # Ratios negativos se mantienen proporcionales
        result = _pct(-0.5)
        assert result == pytest.approx(-50.0)


# ══════════════════════════════════════════════════════════════════════════════
# 2. Extraccion de SAT activas — _sat_activas
# ══════════════════════════════════════════════════════════════════════════════

class TestSatActivas:
    def test_formato_lista_strings(self):
        snap = {"sat": {"activas": ["SAT-III", "SAT-IV"]}}
        result = _sat_activas(snap)
        assert result == {"SAT-III", "SAT-IV"}

    def test_formato_lista_dicts_con_codigo(self):
        snap = {
            "sat": {
                "activas": [
                    {"codigo": "SAT-V", "estado": "ACTIVA"},
                    {"code": "SAT-I"},
                ]
            }
        }
        result = _sat_activas(snap)
        assert "SAT-V" in result
        assert "SAT-I" in result

    def test_formato_alertas_solo_activas(self):
        snap = {
            "sat": {
                "activas": [],
                "alertas": [
                    {"codigo": "SAT-II", "estado": "ACTIVA"},
                    {"codigo": "SAT-VI", "estado": "INACTIVA"},
                ],
            }
        }
        result = _sat_activas(snap)
        assert result == {"SAT-II"}

    def test_sin_sat_devuelve_vacio(self):
        assert _sat_activas({}) == set()

    def test_normaliza_a_mayusculas(self):
        snap = {"sat": {"activas": ["sat-iii", "Sat-IV"]}}
        result = _sat_activas(snap)
        assert "SAT-III" in result
        assert "SAT-IV" in result


# ══════════════════════════════════════════════════════════════════════════════
# 3. _field_diff — diferencia de campo individual
# ══════════════════════════════════════════════════════════════════════════════

class TestFieldDiff:
    def test_valores_iguales_devuelve_none(self):
        assert _field_diff("campo", 42.0, 42.0) is None

    def test_mejora_numerica(self):
        fd = _field_diff("icpi.score", 0.50, 0.55)
        assert fd is not None
        assert fd.direccion == "MEJORA"
        assert fd.delta == pytest.approx(0.05)

    def test_deterioro_numerica(self):
        fd = _field_diff("icpi.score", 0.60, 0.50)
        assert fd is not None
        assert fd.direccion == "DETERIORO"
        assert fd.delta == pytest.approx(-0.10)

    def test_cambio_insignificante_devuelve_none(self):
        # delta < 0.001 se ignora
        assert _field_diff("x", 1.0000, 1.0001) is None

    def test_none_a_valor(self):
        fd = _field_diff("campo", None, 42.0)
        assert fd is not None
        assert fd.direccion == "NUEVO"

    def test_valor_a_none(self):
        fd = _field_diff("campo", 42.0, None)
        assert fd is not None
        assert fd.direccion == "PERDIDO"

    def test_cambio_string(self):
        fd = _field_diff("riesgo", "ALTO", "MEDIO")
        assert fd is not None
        assert fd.direccion == "CAMBIADO"
        assert fd.delta is None


# ══════════════════════════════════════════════════════════════════════════════
# 4. _clasificar — logica de clasificacion canonica
# ══════════════════════════════════════════════════════════════════════════════

class TestClasificar:
    def test_sin_delta_insuficiente_datos(self):
        assert _clasificar(None, None, None) == "INSUFICIENTE_DATOS"

    def test_ruptura_delta_exactamente_menos_10(self):
        assert _clasificar(70.0, 60.0, -10.0) == "RUPTURA"

    def test_ruptura_delta_mayor_a_10(self):
        assert _clasificar(80.0, 65.0, -15.0) == "RUPTURA"

    def test_recuperacion_condicion_exacta(self):
        # icpi_a < 60, icpi_b >= 65 y delta > 0
        assert _clasificar(58.0, 66.0, 8.0) == "RECUPERACION"

    def test_recuperacion_no_activa_si_icpi_a_sobre_60(self):
        # icpi_a >= 60 → no es recuperacion
        result = _clasificar(61.0, 68.0, 7.0)
        assert result == "MEJORA"

    def test_recuperacion_no_activa_si_icpi_b_bajo_65(self):
        # icpi_b < 65 → no supera umbral de recuperacion
        result = _clasificar(55.0, 64.0, 9.0)
        assert result == "MEJORA"

    def test_mejora_delta_exactamente_1pp(self):
        assert _clasificar(50.0, 51.0, 1.0) == "MEJORA"

    def test_mejora_delta_mayor_1pp(self):
        assert _clasificar(50.0, 53.0, 3.0) == "MEJORA"

    def test_deterioro_delta_exactamente_menos_1pp(self):
        assert _clasificar(55.0, 54.0, -1.0) == "DETERIORO"

    def test_deterioro_delta_mayor_a_1pp(self):
        assert _clasificar(55.0, 52.0, -3.0) == "DETERIORO"

    def test_estable_delta_menor_1pp_positivo(self):
        assert _clasificar(50.0, 50.5, 0.5) == "ESTABLE"

    def test_estable_delta_menor_1pp_negativo(self):
        assert _clasificar(50.0, 49.5, -0.5) == "ESTABLE"

    def test_estable_delta_cero(self):
        assert _clasificar(50.0, 50.0, 0.0) == "ESTABLE"

    def test_ruptura_tiene_prioridad_sobre_deterioro(self):
        # Una caida de -12pp es RUPTURA, no DETERIORO
        assert _clasificar(80.0, 68.0, -12.0) == "RUPTURA"


# ══════════════════════════════════════════════════════════════════════════════
# 5. _detectar_sat_iii — reincidencia D3
# ══════════════════════════════════════════════════════════════════════════════

class TestDetectarSatIII:
    def test_con_historial_3_periodos_bajo_60(self):
        # _detectar_sat_iii agrega SOLO d3_b al historial (no d3_a).
        # Para 3 periodos: historial debe tener 2 valores + d3_b = 3 total.
        historial = [50.0, 45.0]   # + d3_b = 30.0 → [50, 45, 30], todos < 60
        assert _detectar_sat_iii(45.0, 30.0, historial) is True

    def test_con_historial_solo_2_periodos_bajo_60(self):
        # historial tiene 1 valor + d3_b = 2 total → insuficiente para SAT-III
        historial = [50.0]         # + d3_b = 40.0 → [50, 40] = 2 periodos
        assert _detectar_sat_iii(50.0, 40.0, historial) is False

    def test_con_historial_no_consecutivos(self):
        # Los ultimos 3 incluyen 70.0 >= 60 → racha rota
        historial = [70.0, 50.0]   # + d3_b = 40.0 → [70, 50, 40] → 70 rompe racha
        assert _detectar_sat_iii(50.0, 40.0, historial) is False

    def test_con_historial_exactamente_60_no_activa(self):
        # La condicion es ESTRICTAMENTE menor que 60; 60.0 no cuenta
        historial = [60.0, 59.9]   # + d3_b = 59.0 → [60.0, 59.9, 59.0] → 60 no < 60
        assert _detectar_sat_iii(60.0, 59.0, historial) is False

    def test_sin_historial_no_activa(self):
        # Sin historial nunca puede haber SAT-III (necesita 3 periodos)
        assert _detectar_sat_iii(40.0, 30.0, None) is False

    def test_historial_vacio_no_activa(self):
        assert _detectar_sat_iii(40.0, 30.0, []) is False

    def test_historial_insuficiente_largo(self):
        historial = [45.0, 50.0]
        # historial + d3_b = [45, 50, 65]  — ultimo sobre umbral
        assert _detectar_sat_iii(50.0, 65.0, historial) is False

    def test_historial_largo_solo_ultimos_3_cuentan(self):
        # Primeros valores sobre umbral no rompen la racha si los 3 ultimos < 60
        historial = [75.0, 70.0, 55.0, 45.0]   # + d3_b = 30.0 → [55,45,30] < 60
        assert _detectar_sat_iii(45.0, 30.0, historial) is True


# ══════════════════════════════════════════════════════════════════════════════
# 6. compare_snapshots — clasificaciones canonicas (tests de integracion)
# ══════════════════════════════════════════════════════════════════════════════

class TestCompareSnapshotsClasificacion:

    def test_insuficiente_datos_sin_icpi(self):
        snap_a = _snap(icpi_score=None)
        snap_b = _snap(icpi_score=None)
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "INSUFICIENTE_DATOS"
        assert result.icpi_delta_pp is None

    def test_insuficiente_datos_solo_snap_b_sin_icpi(self):
        snap_a = _snap(icpi_score=0.55)
        snap_b = _snap(icpi_score=None)
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "INSUFICIENTE_DATOS"

    def test_ruptura_caida_10pp(self):
        snap_a = _snap(icpi_score=0.70)    # 70%
        snap_b = _snap(icpi_score=0.60)    # 60% → delta = -10pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "RUPTURA"
        assert result.icpi_delta_pp == pytest.approx(-10.0, abs=0.01)

    def test_ruptura_caida_mayor_10pp(self):
        snap_a = _snap(icpi_score=0.80)    # 80%
        snap_b = _snap(icpi_score=0.65)    # 65% → delta = -15pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "RUPTURA"

    def test_recuperacion_desde_zona_critica(self):
        snap_a = _snap(icpi_score=0.55)    # 55% < 60 (crisis)
        snap_b = _snap(icpi_score=0.68)    # 68% >= 65 (recuperado)
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "RECUPERACION"

    def test_mejora_delta_exacto_1pp(self):
        snap_a = _snap(icpi_score=0.5000)
        snap_b = _snap(icpi_score=0.5100)  # +1pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "MEJORA"
        assert result.icpi_delta_pp == pytest.approx(1.0, abs=0.01)

    def test_mejora_delta_mayor_1pp(self):
        snap_a = _snap(icpi_score=0.50)
        snap_b = _snap(icpi_score=0.55)    # +5pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "MEJORA"

    def test_deterioro_delta_exacto_menos_1pp(self):
        snap_a = _snap(icpi_score=0.6000)
        snap_b = _snap(icpi_score=0.5900)  # -1pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "DETERIORO"

    def test_deterioro_entre_1_y_10pp(self):
        snap_a = _snap(icpi_score=0.65)
        snap_b = _snap(icpi_score=0.58)    # -7pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "DETERIORO"

    def test_estable_variacion_menor_1pp(self):
        snap_a = _snap(icpi_score=0.5356)
        snap_b = _snap(icpi_score=0.5400)  # +0.44pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "ESTABLE"

    def test_estable_sin_variacion(self):
        snap = _snap(icpi_score=0.5356)
        result = compare_snapshots(snap, snap)
        assert result.clasificacion == "ESTABLE"

    def test_icpi_como_porcentaje_directo(self):
        # Snapshots donde icpi.score ya viene en %, no ratio
        snap_a = _snap_pct(icpi_score=53.56)
        snap_b = _snap_pct(icpi_score=56.00)   # +2.44pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.clasificacion == "MEJORA"


# ══════════════════════════════════════════════════════════════════════════════
# 7. compare_snapshots — metadatos y campos
# ══════════════════════════════════════════════════════════════════════════════

class TestCompareSnapshotsMetadatos:

    def test_periodo_a_y_b_correctos(self):
        snap_a = _snap(fecha_corte="2026-03-25")
        snap_b = _snap(fecha_corte="2026-05-25")
        result = compare_snapshots(snap_a, snap_b)
        assert result.periodo_a == "2026-03-25"
        assert result.periodo_b == "2026-05-25"

    def test_riesgo_a_y_b(self):
        snap_a = _snap(riesgo_ponderado="ALTO")
        snap_b = _snap(riesgo_ponderado="MEDIO")
        result = compare_snapshots(snap_a, snap_b)
        assert result.riesgo_a == "ALTO"
        assert result.riesgo_b == "MEDIO"

    def test_d3_ti_delta_calculado(self):
        snap_a = _snap(d3=0.50)    # 50%
        snap_b = _snap(d3=0.60)    # 60% → +10pp
        result = compare_snapshots(snap_a, snap_b)
        assert result.d3_ti_delta_pp == pytest.approx(10.0, abs=0.01)

    def test_d3_delta_none_si_sin_datos(self):
        snap_a = _snap(d3=None)
        snap_b = _snap(d3=None)
        result = compare_snapshots(snap_a, snap_b)
        assert result.d3_ti_delta_pp is None

    def test_campos_cambiados_incluye_icpi(self):
        snap_a = _snap(icpi_score=0.50)
        snap_b = _snap(icpi_score=0.55)
        result = compare_snapshots(snap_a, snap_b)
        campos = {fd.campo for fd in result.campos_cambiados}
        assert "icpi.score" in campos

    def test_campos_cambiados_vacio_si_mismo_snapshot(self):
        snap = _snap()
        result = compare_snapshots(snap, snap)
        assert result.campos_cambiados == []

    def test_diff_result_es_instancia_correcta(self):
        result = compare_snapshots(_snap(), _snap())
        assert isinstance(result, DiffResult)


# ══════════════════════════════════════════════════════════════════════════════
# 8. compare_snapshots — alertas SAT
# ══════════════════════════════════════════════════════════════════════════════

class TestCompareSnapshotsAlertas:

    def test_alertas_nuevas_detectadas(self):
        snap_a = _snap(sat_activas=["SAT-III"])
        snap_b = _snap(sat_activas=["SAT-III", "SAT-IV"])
        result = compare_snapshots(snap_a, snap_b)
        assert "SAT-IV" in result.alertas_nuevas
        assert result.alertas_mitigadas == []

    def test_alertas_mitigadas_detectadas(self):
        snap_a = _snap(sat_activas=["SAT-III", "SAT-V"])
        snap_b = _snap(sat_activas=["SAT-III"])
        result = compare_snapshots(snap_a, snap_b)
        assert "SAT-V" in result.alertas_mitigadas
        assert result.alertas_nuevas == []

    def test_sin_cambios_alertas_ambas_listas_vacias(self):
        snap_a = _snap(sat_activas=["SAT-III"])
        snap_b = _snap(sat_activas=["SAT-III"])
        result = compare_snapshots(snap_a, snap_b)
        assert result.alertas_nuevas == []
        assert result.alertas_mitigadas == []

    def test_todas_alertas_mitigadas(self):
        snap_a = _snap(sat_activas=["SAT-II", "SAT-IV"])
        snap_b = _snap(sat_activas=[])
        result = compare_snapshots(snap_a, snap_b)
        assert set(result.alertas_mitigadas) == {"SAT-II", "SAT-IV"}

    def test_formato_dicts_sat_alertas(self):
        snap_a = _snap(
            sat_activas=[],
            sat_alertas=[{"codigo": "SAT-I", "estado": "ACTIVA"}],
        )
        snap_b = _snap(
            sat_activas=[],
            sat_alertas=[
                {"codigo": "SAT-I", "estado": "ACTIVA"},
                {"codigo": "SAT-II", "estado": "ACTIVA"},
            ],
        )
        result = compare_snapshots(snap_a, snap_b)
        assert "SAT-II" in result.alertas_nuevas


# ══════════════════════════════════════════════════════════════════════════════
# 9. compare_snapshots — SAT-III reincidencia
# ══════════════════════════════════════════════════════════════════════════════

class TestCompareSnapshotsSatIII:

    def test_sat_iii_activa_con_historial_3_periodos(self):
        # compare_snapshots pasa d3_b (no d3_a) a _detectar_sat_iii.
        # historial debe tener 2 valores para que [h1, h2, d3_b] = 3 periodos.
        snap_a = _snap(d3=0.45)         # 45%
        snap_b = _snap(d3=0.30)         # 30%
        historial = [50.0, 45.0]        # + 30% → [50, 45, 30], todos < 60
        result = compare_snapshots(snap_a, snap_b, historial_d3=historial)
        assert result.sat_iii_reincidente is True

    def test_sat_iii_no_activa_sin_historial(self):
        snap_a = _snap(d3=0.40)
        snap_b = _snap(d3=0.35)
        result = compare_snapshots(snap_a, snap_b, historial_d3=None)
        assert result.sat_iii_reincidente is False

    def test_sat_iii_no_activa_historial_insuficiente(self):
        # Solo 2 periodos en historial total → no alcanza para SAT-III
        snap_a = _snap(d3=0.40)
        snap_b = _snap(d3=0.35)
        result = compare_snapshots(snap_a, snap_b, historial_d3=[45.0])
        # historial = [45, 35] → solo 2 periodos < 60
        assert result.sat_iii_reincidente is False

    def test_sat_iii_no_activa_d3_sobre_umbral(self):
        # d3_a NO se incluye en el historial interno; el historial externo debe
        # contener el valor >= 60 para romper la racha.
        snap_a = _snap(d3=0.45)
        snap_b = _snap(d3=0.40)
        historial = [75.0, 50.0]   # + 40% → [75, 50, 40] → 75 >= 60 → False
        result = compare_snapshots(snap_a, snap_b, historial_d3=historial)
        assert result.sat_iii_reincidente is False


# ══════════════════════════════════════════════════════════════════════════════
# 10. compare_snapshots — notas doctrinales
# ══════════════════════════════════════════════════════════════════════════════

class TestCompareSnapshotsNotas:

    def test_ruptura_genera_nota_protocolo(self):
        snap_a = _snap(icpi_score=0.80)
        snap_b = _snap(icpi_score=0.65)   # -15pp → RUPTURA
        result = compare_snapshots(snap_a, snap_b)
        assert any("RUPTURA" in nota for nota in result.notas)
        assert any("SAT-VI" in nota for nota in result.notas)

    def test_recuperacion_genera_nota(self):
        snap_a = _snap(icpi_score=0.55)
        snap_b = _snap(icpi_score=0.68)   # RECUPERACION
        result = compare_snapshots(snap_a, snap_b)
        assert any("RECUPERACION" in nota for nota in result.notas)

    def test_mejora_genera_nota(self):
        snap_a = _snap(icpi_score=0.50)
        snap_b = _snap(icpi_score=0.55)
        result = compare_snapshots(snap_a, snap_b)
        assert any("MEJORA" in nota for nota in result.notas)

    def test_deterioro_genera_nota(self):
        snap_a = _snap(icpi_score=0.60)
        snap_b = _snap(icpi_score=0.55)
        result = compare_snapshots(snap_a, snap_b)
        assert any("DETERIORO" in nota for nota in result.notas)

    def test_sat_iii_genera_nota_legal(self):
        # Necesita 2 valores en historial para que [h1, h2, d3_b] = 3 periodos
        snap_a = _snap(d3=0.45)
        snap_b = _snap(d3=0.30)
        historial = [50.0, 45.0]    # + 30% → [50, 45, 30], todos < 60 → SAT-III activa
        result = compare_snapshots(snap_a, snap_b, historial_d3=historial)
        assert any("SAT-III" in nota for nota in result.notas)
        assert any("COPFP" in nota for nota in result.notas)

    def test_d3_critico_severo_genera_nota(self):
        # D3 < 40% activa nota adicional
        snap_a = _snap(d3=0.45, icpi_score=0.55)
        snap_b = _snap(d3=0.38, icpi_score=0.53)   # 38% < 40%
        result = compare_snapshots(snap_a, snap_b)
        assert any("40%" in nota or "critica" in nota.lower() for nota in result.notas)

    def test_icpi_bajo_50_genera_nota_ruptura_sistemica(self):
        snap_a = _snap(icpi_score=0.55)
        snap_b = _snap(icpi_score=0.48)   # 48% < 50%
        result = compare_snapshots(snap_a, snap_b)
        assert any("50%" in nota or "Ruptura" in nota for nota in result.notas)

    def test_alertas_nuevas_en_notas(self):
        snap_a = _snap(sat_activas=[])
        snap_b = _snap(sat_activas=["SAT-IV"], icpi_score=0.51)
        result = compare_snapshots(snap_a, snap_b)
        assert any("SAT-IV" in nota for nota in result.notas)

    def test_estable_sin_alertas_puede_no_generar_notas(self):
        snap_a = _snap(icpi_score=0.5356, sat_activas=[])
        snap_b = _snap(icpi_score=0.5356, sat_activas=[])
        result = compare_snapshots(snap_a, snap_b)
        # Estable sin alertas → notas minimas o vacias
        # (no debe fallar — puede o no tener notas)
        assert isinstance(result.notas, list)


# ══════════════════════════════════════════════════════════════════════════════
# 11. detect_reincidence_from_history — API longitudinal
# ══════════════════════════════════════════════════════════════════════════════

class TestDetectReincidenceFromHistory:

    def test_lista_vacia_devuelve_estado_limpio(self):
        result = detect_reincidence_from_history([])
        assert result["sat_iii_activa"] is False
        assert result["periodos_d3_bajo"] == 0
        assert result["valores_d3"] == []
        assert result["clasificacion_seq"] == []

    def test_un_solo_snapshot_no_activa_sat_iii(self):
        snap = _snap(d3=0.40)
        result = detect_reincidence_from_history([snap])
        assert result["sat_iii_activa"] is False
        assert result["periodos_d3_bajo"] == 1
        assert result["clasificacion_seq"] == []   # 1 snapshot = 0 pares

    def test_tres_snapshots_d3_bajo_activa_sat_iii(self):
        snaps = [
            _snap(d3=0.50, icpi_score=0.55, fecha_corte="2026-01-25"),
            _snap(d3=0.45, icpi_score=0.54, fecha_corte="2026-03-25"),
            _snap(d3=0.40, icpi_score=0.53, fecha_corte="2026-05-25"),
        ]
        result = detect_reincidence_from_history(snaps)
        assert result["sat_iii_activa"] is True
        assert result["periodos_d3_bajo"] == 3

    def test_tres_snapshots_d3_sobre_60_no_activa(self):
        snaps = [
            _snap(d3=0.65, icpi_score=0.60),
            _snap(d3=0.70, icpi_score=0.61),
            _snap(d3=0.72, icpi_score=0.62),
        ]
        result = detect_reincidence_from_history(snaps)
        assert result["sat_iii_activa"] is False
        assert result["periodos_d3_bajo"] == 0

    def test_racha_rota_en_medio_no_activa(self):
        snaps = [
            _snap(d3=0.45, icpi_score=0.55),    # < 60 — racha 1
            _snap(d3=0.65, icpi_score=0.57),    # > 60 — rompe racha
            _snap(d3=0.40, icpi_score=0.56),    # < 60 — nuevo inicio
            _snap(d3=0.35, icpi_score=0.55),    # < 60 — solo 2 consecutivos
        ]
        result = detect_reincidence_from_history(snaps)
        assert result["sat_iii_activa"] is False
        assert result["periodos_d3_bajo"] == 2

    def test_clasificacion_seq_longitud_correcta(self):
        snaps = [_snap() for _ in range(5)]
        result = detect_reincidence_from_history(snaps)
        assert len(result["clasificacion_seq"]) == 4    # N-1 pares

    def test_valores_d3_extraidos_correctamente(self):
        snaps = [
            _snap(d3=0.50),
            _snap(d3=0.45),
            _snap(d3=0.40),
        ]
        result = detect_reincidence_from_history(snaps)
        # 0.50 → 50%, 0.45 → 45%, 0.40 → 40%
        assert len(result["valores_d3"]) == 3
        assert all(v < 60 for v in result["valores_d3"])

    def test_clasificacion_seq_correcta_mejora_deterioro(self):
        snaps = [
            _snap(icpi_score=0.50, fecha_corte="2026-01-25"),
            _snap(icpi_score=0.55, fecha_corte="2026-03-25"),   # MEJORA +5pp
            _snap(icpi_score=0.53, fecha_corte="2026-05-25"),   # DETERIORO -2pp
        ]
        result = detect_reincidence_from_history(snaps)
        assert result["clasificacion_seq"][0] == "MEJORA"
        assert result["clasificacion_seq"][1] == "DETERIORO"

    def test_snapshot_d3_none_excluido_de_valores_d3(self):
        snaps = [
            _snap(d3=None),
            _snap(d3=0.45),
        ]
        result = detect_reincidence_from_history(snaps)
        # Los None se filtran en valores_d3
        assert None not in result["valores_d3"]
        assert len(result["valores_d3"]) == 1


# ══════════════════════════════════════════════════════════════════════════════
# 12. _generar_notas — cobertura directa
# ══════════════════════════════════════════════════════════════════════════════

class TestGenerarNotas:

    def test_clasificacion_estable_sin_extras_devuelve_lista(self):
        notas = _generar_notas("ESTABLE", 0.5, 70.0, 55.0, False, [], [])
        assert isinstance(notas, list)

    def test_ruptura_produce_nota_con_delta(self):
        notas = _generar_notas("RUPTURA", -12.0, 55.0, 55.0, False, [], [])
        assert any("12.0pp" in n or "12" in n for n in notas)

    def test_sat_iii_produce_nota_copfp(self):
        notas = _generar_notas("DETERIORO", -3.0, 50.0, 55.0, True, [], [])
        assert any("COPFP" in n for n in notas)

    def test_alertas_nuevas_en_nota(self):
        notas = _generar_notas("ESTABLE", 0.0, 65.0, 60.0, False, ["SAT-II", "SAT-IV"], [])
        assert any("SAT-II" in n or "SAT-IV" in n for n in notas)

    def test_alertas_mitigadas_en_nota(self):
        notas = _generar_notas("ESTABLE", 0.0, 65.0, 60.0, False, [], ["SAT-V"])
        assert any("SAT-V" in n for n in notas)

    def test_d3_severo_menos_40_nota(self):
        notas = _generar_notas("DETERIORO", -5.0, 38.0, 55.0, False, [], [])
        assert any("40" in n for n in notas)

    def test_icpi_menos_50_nota_ruptura_sistemica(self):
        notas = _generar_notas("DETERIORO", -5.0, 55.0, 48.0, False, [], [])
        assert any("50%" in n or "Ruptura" in n for n in notas)


# ══════════════════════════════════════════════════════════════════════════════
# 13. Casos borde adicionales
# ══════════════════════════════════════════════════════════════════════════════

class TestCasosBorde:

    def test_snap_a_vacio_no_falla(self):
        result = compare_snapshots({}, _snap())
        assert result.clasificacion == "INSUFICIENTE_DATOS"

    def test_snap_b_vacio_no_falla(self):
        result = compare_snapshots(_snap(), {})
        assert result.clasificacion == "INSUFICIENTE_DATOS"

    def test_ambos_snapshots_vacios(self):
        result = compare_snapshots({}, {})
        assert result.clasificacion == "INSUFICIENTE_DATOS"

    def test_historial_d3_lista_vacia_no_activa_sat_iii(self):
        snap_a = _snap(d3=0.40)
        snap_b = _snap(d3=0.35)
        result = compare_snapshots(snap_a, snap_b, historial_d3=[])
        assert result.sat_iii_reincidente is False

    def test_clasif_riesgo_fallback_si_riesgo_ponderado_none(self):
        snap_a = _snap(riesgo_ponderado=None, clasif_riesgo="MEDIO")
        snap_b = _snap(riesgo_ponderado=None, clasif_riesgo="ALTO")
        result = compare_snapshots(snap_a, snap_b)
        assert result.riesgo_a == "MEDIO"
        assert result.riesgo_b == "ALTO"

    def test_campos_cambiados_campo_nombre(self):
        snap_a = _snap(icpi_score=0.50, tgi_score=60.0)
        snap_b = _snap(icpi_score=0.55, tgi_score=65.0)
        result = compare_snapshots(snap_a, snap_b)
        campos_nombres = {fd.campo for fd in result.campos_cambiados}
        assert "icpi.score" in campos_nombres
        assert "tgi.score" in campos_nombres

    def test_field_diff_direccion_mejora_positivo(self):
        snap_a = _snap(icpi_score=0.50)
        snap_b = _snap(icpi_score=0.56)
        result = compare_snapshots(snap_a, snap_b)
        icpi_diff = next((fd for fd in result.campos_cambiados if fd.campo == "icpi.score"), None)
        assert icpi_diff is not None
        assert icpi_diff.direccion == "MEJORA"

    def test_sat_activas_vacias_en_ambos_no_falla(self):
        snap_a = _snap(sat_activas=[])
        snap_b = _snap(sat_activas=[])
        result = compare_snapshots(snap_a, snap_b)
        assert result.alertas_nuevas == []
        assert result.alertas_mitigadas == []
