"""
tests/test_snapshot_validation.py — QUIRA OS · Sprint 2
Tests para utils/snapshot_io.validate_snapshot()

Sin red, sin Supabase, sin Excel — solo lógica de validación.
Ejecutar: pytest tests/test_snapshot_validation.py -v

Dylus Lab © 2026
"""
import sys
from pathlib import Path

# Agregar raíz al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from utils.snapshot_io import validate_snapshot


# ── Fixture base — snapshot mínimo válido ─────────────────────────────────────
def _minimal_snapshot(overrides: dict = None) -> dict:
    """Snapshot mínimo que pasa la validación completa."""
    snap = {
        "_meta": {
            "fecha_corte": "2026-03-31",
            "version_excel": "SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518",
        },
        "gad": {
            "codigo": "130801",
            "nombre": "GAD Municipal de Montecristi",
        },
        "tgi": {
            "score":  None,
            "fuente": "pendiente",   # Q1 — TGI pendiente es válido
        },
        "financiero":          {},
        "series_longitudinal": {},
        "territorial":         {},
    }
    if overrides:
        for k, v in overrides.items():
            if isinstance(v, dict) and k in snap and isinstance(snap[k], dict):
                snap[k].update(v)
            else:
                snap[k] = v
    return snap


# ── TESTS: snapshot válido ────────────────────────────────────────────────────

class TestValidSnapshot:

    def test_minimal_valid(self):
        """El snapshot mínimo con fuente=pendiente debe ser válido."""
        ok, errors = validate_snapshot(_minimal_snapshot())
        assert ok, f"Snapshot mínimo debe ser válido. Errores: {errors}"
        assert errors == []

    def test_with_tgi_score(self):
        """TGI score numérico dentro de rango debe pasar."""
        snap = _minimal_snapshot({"tgi": {"score": 58.5, "fuente": "gold_master_h73"}})
        ok, errors = validate_snapshot(snap)
        assert ok, f"Score 58.5 debe ser válido. Errores: {errors}"

    def test_tgi_score_boundaries(self):
        """TGI 0.0 y 100.0 son valores límite válidos."""
        for score in (0.0, 100.0, 50.0, 99.99):
            snap = _minimal_snapshot({"tgi": {"score": score, "fuente": "gold_master_h73"}})
            ok, errors = validate_snapshot(snap)
            assert ok, f"Score {score} debe ser válido. Errores: {errors}"

    def test_gold_master_fuente_allows_null_score(self):
        """fuente=gold_master_h73 con score=None es válido (datos en proceso)."""
        snap = _minimal_snapshot({"tgi": {"score": None, "fuente": "gold_master_h73"}})
        ok, errors = validate_snapshot(snap)
        assert ok, f"Gold Master con score=None debe ser válido. Errores: {errors}"

    def test_codigo_6_digits(self):
        """Código de municipio de 6 dígitos numéricos."""
        for code in ("130801", "130901", "130601"):
            snap = _minimal_snapshot({"gad": {"codigo": code, "nombre": "Test"}})
            ok, errors = validate_snapshot(snap)
            assert ok, f"Código {code} debe ser válido. Errores: {errors}"


# ── TESTS: snapshot inválido ──────────────────────────────────────────────────

class TestInvalidSnapshot:

    def test_missing_top_keys(self):
        """Snapshot sin claves de primer nivel debe fallar."""
        ok, errors = validate_snapshot({})
        assert not ok
        assert len(errors) > 0

    def test_missing_fecha_corte(self):
        """_meta sin fecha_corte debe reportar error."""
        snap = _minimal_snapshot()
        snap["_meta"]["fecha_corte"] = ""
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("fecha_corte" in e for e in errors)

    def test_missing_version_excel(self):
        """_meta sin version_excel debe reportar error."""
        snap = _minimal_snapshot()
        snap["_meta"]["version_excel"] = ""
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("version_excel" in e for e in errors)

    def test_gad_codigo_too_short(self):
        """Código GAD de menos de 6 dígitos debe fallar."""
        snap = _minimal_snapshot({"gad": {"codigo": "1308", "nombre": "Test"}})
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("codigo" in e for e in errors)

    def test_gad_codigo_non_numeric(self):
        """Código GAD no numérico debe fallar."""
        snap = _minimal_snapshot({"gad": {"codigo": "ABCDEF", "nombre": "Test"}})
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("codigo" in e for e in errors)

    def test_tgi_score_above_100(self):
        """TGI score > 100 debe fallar."""
        snap = _minimal_snapshot({"tgi": {"score": 150.0, "fuente": "gold_master_h73"}})
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("tgi.score" in e for e in errors)

    def test_tgi_score_negative(self):
        """TGI score negativo debe fallar."""
        snap = _minimal_snapshot({"tgi": {"score": -5.0, "fuente": "gold_master_h73"}})
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("tgi.score" in e for e in errors)

    def test_tgi_null_without_fuente(self):
        """TGI score=None sin fuente válida debe fallar."""
        snap = _minimal_snapshot({"tgi": {"score": None, "fuente": "desconocido"}})
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("tgi.score" in e for e in errors)

    def test_missing_gad_nombre(self):
        """GAD sin nombre debe reportar error."""
        snap = _minimal_snapshot()
        snap["gad"]["nombre"] = ""
        ok, errors = validate_snapshot(snap)
        assert not ok
        assert any("gad.nombre" in e for e in errors)
