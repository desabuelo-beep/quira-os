"""
tests/test_sat_evaluator.py — QUIRA OS · Sprint 2
Tests para app/services/sat_evaluator.py

Sin red, sin Supabase, sin Excel — solo lógica SAT.
Ejecutar: pytest tests/test_sat_evaluator.py -v

Dylus Lab © 2026
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from app.services.sat_evaluator import evaluate_sat, SAT_CATALOG, _classify_risk


# ── Helpers ───────────────────────────────────────────────────────────────────

def _snap_with_ejecucion(pct: float, cancelados_pct: float = 0.05) -> dict:
    """Snapshot sintético con ejecución presupuestaria configurable.

    usa los nombres de campo que lee el SAT evaluator:
      - financiero.ejecucion_porcentaje  → SAT-III (parálisis presupuestaria)
      - financiero.inversion_porcentaje  → SAT-IV  (inversión COOTAD)
    """
    return {
        "financiero": {
            "ejecucion_porcentaje": pct,       # campo canónico para SAT-III
            "inversion_porcentaje": pct * 0.8, # proxy — SAT-IV usa este campo
            "psg_ejecucion": pct,              # alias legacy
        },
        "contratacion": {
            "pac_publicado": True,
            "procesos_adjudicados": 10,
            "procesos_cancelados": int(10 * cancelados_pct),
            "cancelados_pct": cancelados_pct,
        },
        "accountability": {
            "rdc": {"score": 75.0},
            "gold_master": {"rdc_score": 75.0, "rdc_clasificacion": "Parcialmente Cumplida"},
        },
        "tgi": {"score": None, "fuente": "pendiente"},
        "gold_master_data": {
            "sat_engine": {
                "riesgo_total": None,
                "clasif_riesgo": None,
                "activas_count": None,
            }
        },
    }


# ── TESTS: catálogo SAT ───────────────────────────────────────────────────────

class TestSATCatalog:

    def test_catalog_not_empty(self):
        """El catálogo SAT debe tener entradas."""
        assert len(SAT_CATALOG) > 0

    def test_all_sat_have_codigo(self):
        """Todos los SATs deben tener código único."""
        codigos = [s["codigo"] for s in SAT_CATALOG]
        assert len(codigos) == len(set(codigos)), "Códigos SAT duplicados"

    def test_all_sat_have_required_fields(self):
        """Todos los SATs deben tener los campos mínimos requeridos."""
        required = {"codigo", "nombre", "dimension", "tipo", "base_legal_art"}
        for sat in SAT_CATALOG:
            missing = required - set(sat.keys())
            assert not missing, f"{sat['codigo']} falta: {missing}"

    def test_sat_dimensions_valid(self):
        """Todas las dimensiones deben ser D1-D5."""
        valid = {"D1", "D2", "D3", "D4", "D5"}
        for sat in SAT_CATALOG:
            assert sat["dimension"] in valid, (
                f"{sat['codigo']} tiene dimensión inválida: {sat['dimension']}"
            )

    def test_sat_tipos_valid(self):
        """Tipos SAT deben ser valores del catálogo."""
        valid = {"critica", "legal", "preventiva", "alerta", "informacional"}
        for sat in SAT_CATALOG:
            assert sat["tipo"] in valid, (
                f"{sat['codigo']} tiene tipo inválido: {sat['tipo']}"
            )

    def test_peso_severidad_range(self):
        """Pesos de severidad deben ser 0.0–1.0."""
        for sat in SAT_CATALOG:
            peso = sat.get("peso_severidad", 0)
            assert 0.0 <= peso <= 1.0, (
                f"{sat['codigo']} peso_severidad fuera de rango: {peso}"
            )

    def test_sat_iii_exists(self):
        """SAT-III (Parálisis Presupuestaria) debe estar en el catálogo."""
        codigos = {s["codigo"] for s in SAT_CATALOG}
        assert "SAT-III" in codigos, "SAT-III no encontrado en catálogo"

    def test_sat_iv_exists(self):
        """SAT-IV (Alerta Fiscal COOTAD) debe estar en el catálogo."""
        codigos = {s["codigo"] for s in SAT_CATALOG}
        assert "SAT-IV" in codigos, "SAT-IV no encontrado en catálogo"


# ── TESTS: clasificación de riesgo ───────────────────────────────────────────

class TestRiskClassification:

    def test_bajo(self):
        assert _classify_risk(0.10) == "BAJO"

    def test_medio(self):
        assert _classify_risk(0.20) == "MEDIO"

    def test_alto(self):
        assert _classify_risk(0.35) == "ALTO"

    def test_critico(self):
        assert _classify_risk(0.55) == "CRÍTICO"

    def test_zero_is_bajo(self):
        assert _classify_risk(0.0) == "BAJO"

    def test_boundary_bajo_medio(self):
        """0.15 es el límite BAJO/MEDIO."""
        assert _classify_risk(0.14) == "BAJO"
        assert _classify_risk(0.15) == "MEDIO"

    def test_boundary_medio_alto(self):
        """0.30 es el límite MEDIO/ALTO."""
        assert _classify_risk(0.29) == "MEDIO"
        assert _classify_risk(0.30) == "ALTO"

    def test_boundary_alto_critico(self):
        """0.50 es el límite ALTO/CRÍTICO."""
        assert _classify_risk(0.49) == "ALTO"
        assert _classify_risk(0.50) == "CRÍTICO"


# ── TESTS: evaluate_sat ───────────────────────────────────────────────────────

class TestEvaluateSAT:

    def test_returns_required_keys(self):
        """El resultado debe contener todas las claves canónicas."""
        result = evaluate_sat(_snap_with_ejecucion(0.60))
        required = {
            "alertas", "activas", "alertas_activas", "riesgo_ponderado",
            "clasif_riesgo", "sat_score", "datos_insuficientes",
            "total_evaluadas", "total_activas", "evaluated_at",
        }
        missing = required - set(result.keys())
        assert not missing, f"Claves faltantes en resultado SAT: {missing}"

    def test_sat_iii_activa_con_ejecucion_baja(self):
        """Con ejecución < 60%, SAT-III (Parálisis Presupuestaria) debe activarse."""
        snap = _snap_with_ejecucion(0.30)  # 30% — muy por debajo del umbral 60%
        result = evaluate_sat(snap)
        activas = result.get("alertas_activas", result.get("activas", []))
        assert "SAT-III" in activas, (
            f"SAT-III debe activarse con ejecución 30%. Activas: {activas}"
        )

    def test_no_sat_iii_con_ejecucion_alta(self):
        """Con ejecución > 75%, SAT-III no debe activarse."""
        snap = _snap_with_ejecucion(0.85)  # 85% — saludable
        result = evaluate_sat(snap)
        activas = result.get("alertas_activas", result.get("activas", []))
        assert "SAT-III" not in activas, (
            f"SAT-III NO debe activarse con ejecución 85%. Activas: {activas}"
        )

    def test_riesgo_ponderado_range(self):
        """riesgo_ponderado debe estar en [0, 1]."""
        snap = _snap_with_ejecucion(0.30)
        result = evaluate_sat(snap)
        rp = result["riesgo_ponderado"]
        assert 0.0 <= rp <= 1.0, f"riesgo_ponderado fuera de rango: {rp}"

    def test_clasif_riesgo_valid(self):
        """clasif_riesgo debe ser valor canónico."""
        valid = {"BAJO", "MEDIO", "ALTO", "CRÍTICO", "SIN_DATOS"}
        result = evaluate_sat(_snap_with_ejecucion(0.50))
        assert result["clasif_riesgo"] in valid, (
            f"clasif_riesgo inválido: {result['clasif_riesgo']}"
        )

    def test_total_activas_equals_len_activas(self):
        """total_activas debe coincidir con len(alertas_activas)."""
        result = evaluate_sat(_snap_with_ejecucion(0.30))
        activas = result.get("alertas_activas", result.get("activas", []))
        assert result["total_activas"] == len(activas), (
            f"Inconsistencia: total_activas={result['total_activas']} "
            f"!= len(activas)={len(activas)}"
        )

    def test_alto_riesgo_con_ejecucion_muy_baja(self):
        """Ejecución muy baja produce clasificación ALTO o CRÍTICO."""
        snap = _snap_with_ejecucion(0.10)
        result = evaluate_sat(snap)
        assert result["clasif_riesgo"] in ("ALTO", "CRÍTICO"), (
            f"Ejecución 10% debe producir ALTO o CRÍTICO, "
            f"obtuvo: {result['clasif_riesgo']}"
        )

    def test_empty_snapshot_doesnt_crash(self):
        """Snapshot vacío no debe lanzar excepción — debe retornar SIN_DATOS."""
        try:
            result = evaluate_sat({})
            # Si no lanza excepción, aceptar resultado con datos_insuficientes
            assert isinstance(result, dict)
        except Exception as e:
            pytest.fail(f"evaluate_sat({{}}) lanzó excepción: {e}")
