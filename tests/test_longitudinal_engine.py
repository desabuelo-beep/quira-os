"""
Tests para app/services/longitudinal_engine.py
Sprint 3 — Prioridad 1

Cobertura:
  - _get_nested          (utilidad interna)
  - _period_label        (etiqueta de período)
  - _snap_timestamp      (parseo de timestamp)
  - _dedup_snapshots     (deduplicación por fecha_corte)
  - get_snapshot_history (carga local con mocks)
  - build_rcm_table      (tabla RC-M canónica)
  - build_metric_trend   (serie temporal)
  - detect_trend         (clasificación de trayectoria)
  - get_longitudinal_summary (integración)

Todos los tests son offline (sin Supabase, sin filesystem real).
"""
from __future__ import annotations

import json
import tempfile
import os
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# ── Helpers para fixtures ──────────────────────────────────────────────────────

def _make_snap(
    *,
    fecha_corte: str = "2026-05-25",
    generated_at: str | None = None,
    icpi_pct: float = 53.56,
    isp_salud_presup: float = 0.1458,
    sat_activas: list | None = None,
    clasif_riesgo: str = "ALTO",
    riesgo_ponderado: float = 0.35,
    sat_alertas: list | None = None,
) -> dict:
    """Snapshot mínimo válido para tests longitudinales."""
    if generated_at is None:
        generated_at = f"{fecha_corte}T10:00:00+00:00"
    if sat_activas is None:
        sat_activas = ["SAT-III", "SAT-IV", "SAT-V"]
    if sat_alertas is None:
        sat_alertas = [
            {
                "codigo": "SAT-IV",
                "estado": "ACTIVA" if "SAT-IV" in sat_activas else "SIN_DATOS",
                "activa": "SAT-IV" in sat_activas,
            }
        ]
    return {
        "_meta": {
            "schema_version": "1.0",
            "pipeline_version": "1.0.0-test",
            "generated_at": generated_at,
            "fecha_corte": fecha_corte,
            "version_excel": "GOLD_MASTER_TEST",
            "gold_master_ok": True,
        },
        "gad": {"codigo": "130801", "nombre": "GAD Municipal de Montecristi"},
        "tgi": {"score": None, "fuente": "pendiente"},
        "icpi": {
            "global": icpi_pct / 100,
            "global_pct": icpi_pct,
            "clasificacion": "Test",
        },
        "financiero": {
            "isp_salud_presup": isp_salud_presup,
            "psg_ejecucion": 0.13,
        },
        "series_longitudinal": {},
        "territorial": {},
        "sat": {
            "alertas": sat_alertas,
            "activas": sat_activas,
            "riesgo_ponderado": riesgo_ponderado,
            "clasif_riesgo": clasif_riesgo,
            "total_activas": len(sat_activas),
        },
        "traceability_score": 41.62,
    }


def _history_of(snapshots: list[dict]) -> list[dict]:
    """Pasa directamente la lista como si fuera el resultado de get_snapshot_history."""
    return snapshots


# ══════════════════════════════════════════════════════════════════════════════
# Importaciones bajo test
# ══════════════════════════════════════════════════════════════════════════════

from app.services.longitudinal_engine import (
    _get_nested,
    _period_label,
    _snap_timestamp,
    _dedup_snapshots,
    build_rcm_table,
    build_metric_trend,
    detect_trend,
    get_longitudinal_summary,
    get_snapshot_history,
)


# ══════════════════════════════════════════════════════════════════════════════
# 1. _get_nested
# ══════════════════════════════════════════════════════════════════════════════

class TestGetNested:
    def test_simple_key(self):
        assert _get_nested({"a": 1}, "a") == 1

    def test_nested_two_levels(self):
        assert _get_nested({"a": {"b": 42}}, "a.b") == 42

    def test_nested_three_levels(self):
        assert _get_nested({"x": {"y": {"z": "ok"}}}, "x.y.z") == "ok"

    def test_missing_key_returns_default(self):
        assert _get_nested({"a": 1}, "b", "fallback") == "fallback"

    def test_missing_nested_key_returns_none(self):
        assert _get_nested({"a": {}}, "a.b") is None

    def test_non_dict_at_path_returns_default(self):
        assert _get_nested({"a": "string"}, "a.b", -1) == -1


# ══════════════════════════════════════════════════════════════════════════════
# 2. _period_label
# ══════════════════════════════════════════════════════════════════════════════

class TestPeriodLabel:
    def test_mayo_2026(self):
        snap = _make_snap(fecha_corte="2026-05-25")
        assert _period_label(snap) == "May 2026"

    def test_enero_2025(self):
        snap = _make_snap(fecha_corte="2025-01-15")
        assert _period_label(snap) == "Ene 2025"

    def test_diciembre(self):
        snap = _make_snap(fecha_corte="2025-12-01")
        assert _period_label(snap) == "Dic 2025"

    def test_invalid_date_returns_raw(self):
        snap = {"_meta": {"fecha_corte": "INVALIDO"}}
        result = _period_label(snap)
        assert result == "INVALIDO"

    def test_missing_fecha_returns_desconocido(self):
        result = _period_label({})
        assert result == "Desconocido"


# ══════════════════════════════════════════════════════════════════════════════
# 3. _snap_timestamp
# ══════════════════════════════════════════════════════════════════════════════

class TestSnapTimestamp:
    def test_parses_iso_with_offset(self):
        snap = _make_snap(generated_at="2026-05-25T20:15:09.514671+00:00")
        ts = _snap_timestamp(snap)
        assert ts.year == 2026
        assert ts.month == 5
        assert ts.day == 25

    def test_fallback_to_fecha_corte(self):
        snap = {"_meta": {"fecha_corte": "2026-06-15"}}
        ts = _snap_timestamp(snap)
        assert ts.year == 2026
        assert ts.month == 6

    def test_invalid_returns_datetime_min(self):
        snap = {"_meta": {}}
        ts = _snap_timestamp(snap)
        assert ts == datetime.min


# ══════════════════════════════════════════════════════════════════════════════
# 4. _dedup_snapshots
# ══════════════════════════════════════════════════════════════════════════════

class TestDedupSnapshots:
    def test_same_fecha_keeps_latest(self):
        snap_old = _make_snap(
            fecha_corte="2026-05-25",
            generated_at="2026-05-25T10:00:00+00:00",
            icpi_pct=50.0,
        )
        snap_new = _make_snap(
            fecha_corte="2026-05-25",
            generated_at="2026-05-25T20:00:00+00:00",
            icpi_pct=53.56,
        )
        result = _dedup_snapshots([snap_old, snap_new], limit=10)
        assert len(result) == 1
        assert result[0]["icpi"]["global_pct"] == 53.56

    def test_different_dates_both_kept(self):
        snap1 = _make_snap(fecha_corte="2026-05-25")
        snap2 = _make_snap(fecha_corte="2026-06-25")
        result = _dedup_snapshots([snap1, snap2], limit=10)
        assert len(result) == 2

    def test_oldest_first_ordering(self):
        snap_may = _make_snap(fecha_corte="2026-05-01")
        snap_jun = _make_snap(fecha_corte="2026-06-01")
        snap_jul = _make_snap(fecha_corte="2026-07-01")
        result = _dedup_snapshots([snap_jul, snap_may, snap_jun], limit=10)
        periodos = [r["_meta"]["fecha_corte"] for r in result]
        assert periodos == ["2026-05-01", "2026-06-01", "2026-07-01"]

    def test_limit_is_respected(self):
        snaps = [_make_snap(fecha_corte=f"2026-0{i}-01") for i in range(1, 8)]
        result = _dedup_snapshots(snaps, limit=3)
        assert len(result) == 3


# ══════════════════════════════════════════════════════════════════════════════
# 5. build_rcm_table
# ══════════════════════════════════════════════════════════════════════════════

class TestBuildRCMTable:
    def test_single_snapshot_returns_one_row(self):
        snap = _make_snap(
            fecha_corte="2026-05-25",
            icpi_pct=53.56,
            isp_salud_presup=0.1458,
            sat_activas=["SAT-III", "SAT-IV", "SAT-V"],
            clasif_riesgo="ALTO",
        )
        rows = build_rcm_table([snap])
        assert len(rows) == 1
        row = rows[0]
        assert row["periodo"] == "May 2026"
        assert row["icpi_pct"] == 53.56
        assert row["d3_ti_pct"] == pytest.approx(14.58, abs=0.01)
        assert row["sat_iv"] == "ACTIVA"
        assert row["riesgo"] == "ALTO"
        assert row["fecha_corte"] == "2026-05-25"

    def test_sat_iv_mitigated_when_not_in_activas(self):
        snap = _make_snap(
            sat_activas=["SAT-III"],  # SAT-IV no está activa
            sat_alertas=[
                {"codigo": "SAT-IV", "estado": "INACTIVA", "activa": False}
            ],
        )
        rows = build_rcm_table([snap])
        assert rows[0]["sat_iv"] == "mitigada"

    def test_sat_iv_sin_datos_when_not_evaluated(self):
        snap = _make_snap(
            sat_activas=[],
            sat_alertas=[
                {"codigo": "SAT-IV", "estado": "SIN_DATOS", "activa": False}
            ],
        )
        rows = build_rcm_table([snap])
        assert rows[0]["sat_iv"] == "SIN DATOS"

    def test_multiple_snapshots_correct_order(self):
        snap1 = _make_snap(fecha_corte="2026-05-01", icpi_pct=53.0)
        snap2 = _make_snap(fecha_corte="2026-06-01", icpi_pct=58.0)
        snap3 = _make_snap(fecha_corte="2026-07-01", icpi_pct=64.0)
        rows = build_rcm_table([snap1, snap2, snap3])
        assert len(rows) == 3
        assert rows[0]["icpi_pct"] == 53.0
        assert rows[1]["icpi_pct"] == 58.0
        assert rows[2]["icpi_pct"] == 64.0

    def test_none_icpi_handled(self):
        snap = _make_snap()
        snap["icpi"]["global_pct"] = None
        rows = build_rcm_table([snap])
        assert rows[0]["icpi_pct"] is None

    def test_d3_ti_converts_ratio_to_pct(self):
        snap = _make_snap(isp_salud_presup=0.60)
        rows = build_rcm_table([snap])
        assert rows[0]["d3_ti_pct"] == pytest.approx(60.0, abs=0.01)

    def test_empty_history_returns_empty_table(self):
        assert build_rcm_table([]) == []


# ══════════════════════════════════════════════════════════════════════════════
# 6. build_metric_trend
# ══════════════════════════════════════════════════════════════════════════════

class TestBuildMetricTrend:
    def test_icpi_series(self):
        snaps = [
            _make_snap(fecha_corte="2026-05-01", icpi_pct=53.0),
            _make_snap(fecha_corte="2026-06-01", icpi_pct=58.0),
            _make_snap(fecha_corte="2026-07-01", icpi_pct=64.0),
        ]
        series = build_metric_trend(snaps, "icpi.global_pct")
        assert len(series) == 3
        assert series[0] == ("May 2026", 53.0)
        assert series[1] == ("Jun 2026", 58.0)
        assert series[2] == ("Jul 2026", 64.0)

    def test_missing_metric_returns_none(self):
        snap = _make_snap()
        series = build_metric_trend([snap], "sat.nonexistent_field")
        assert series[0][1] is None

    def test_nested_metric_riesgo_ponderado(self):
        snap = _make_snap(riesgo_ponderado=0.35)
        series = build_metric_trend([snap], "sat.riesgo_ponderado")
        assert series[0][1] == pytest.approx(0.35, abs=0.001)

    def test_empty_history_returns_empty(self):
        assert build_metric_trend([], "icpi.global_pct") == []


# ══════════════════════════════════════════════════════════════════════════════
# 7. detect_trend
# ══════════════════════════════════════════════════════════════════════════════

class TestDetectTrend:
    def test_mejora_when_delta_ge_1(self):
        assert detect_trend([50.0, 55.0, 60.0]) == "MEJORA"

    def test_deterioro_when_delta_le_minus_1(self):
        assert detect_trend([60.0, 55.0, 50.0]) == "DETERIORO"

    def test_estable_when_within_threshold(self):
        assert detect_trend([50.0, 50.5, 50.8]) == "ESTABLE"

    def test_insufficient_data_with_one_value(self):
        assert detect_trend([50.0]) == "INSUFICIENTE_DATOS"

    def test_insufficient_data_with_empty_list(self):
        assert detect_trend([]) == "INSUFICIENTE_DATOS"

    def test_nones_are_ignored(self):
        assert detect_trend([None, 50.0, None, 55.0]) == "MEJORA"

    def test_all_nones_returns_insufficient(self):
        assert detect_trend([None, None, None]) == "INSUFICIENTE_DATOS"

    def test_exact_threshold_is_mejora(self):
        # delta exacto de 1.0 pp = MEJORA
        assert detect_trend([50.0, 51.0]) == "MEJORA"

    def test_just_below_threshold_is_estable(self):
        # delta de 0.9 pp = ESTABLE
        assert detect_trend([50.0, 50.9]) == "ESTABLE"

    def test_two_values_sufficient(self):
        assert detect_trend([50.0, 52.0]) == "MEJORA"


# ══════════════════════════════════════════════════════════════════════════════
# 8. get_snapshot_history (con archivos locales mock)
# ══════════════════════════════════════════════════════════════════════════════

class TestGetSnapshotHistory:
    def test_loads_local_files_when_supabase_fails(self, tmp_path):
        """Verifica que el fallback a JSON local funciona correctamente."""
        municipio_code = "130801"
        snap_dir = tmp_path / municipio_code
        snap_dir.mkdir()

        snap1 = _make_snap(
            fecha_corte="2026-05-01",
            generated_at="2026-05-01T10:00:00+00:00",
            icpi_pct=53.0,
        )
        snap2 = _make_snap(
            fecha_corte="2026-06-01",
            generated_at="2026-06-01T10:00:00+00:00",
            icpi_pct=58.0,
        )

        (snap_dir / "130801_20260501_100000.json").write_text(
            json.dumps(snap1), encoding="utf-8"
        )
        (snap_dir / "130801_20260601_100000.json").write_text(
            json.dumps(snap2), encoding="utf-8"
        )

        with patch("app.services.longitudinal_engine.cfg.SNAPSHOTS_DIR", tmp_path):
            with patch(
                "app.services.longitudinal_engine._load_supabase_snapshots",
                return_value=[],
            ):
                history = get_snapshot_history(municipio_code, limit=12)

        assert len(history) == 2
        # Oldest-first
        assert history[0]["_meta"]["fecha_corte"] == "2026-05-01"
        assert history[1]["_meta"]["fecha_corte"] == "2026-06-01"

    def test_deduplication_applied(self, tmp_path):
        """Mismo fecha_corte con dos archivos → solo el más reciente."""
        municipio_code = "130801"
        snap_dir = tmp_path / municipio_code
        snap_dir.mkdir()

        snap_old = _make_snap(
            fecha_corte="2026-05-25",
            generated_at="2026-05-25T10:00:00+00:00",
            icpi_pct=50.0,
        )
        snap_new = _make_snap(
            fecha_corte="2026-05-25",
            generated_at="2026-05-25T20:00:00+00:00",
            icpi_pct=53.56,
        )

        (snap_dir / "130801_20260525_100000.json").write_text(
            json.dumps(snap_old), encoding="utf-8"
        )
        (snap_dir / "130801_20260525_200000.json").write_text(
            json.dumps(snap_new), encoding="utf-8"
        )

        with patch("app.services.longitudinal_engine.cfg.SNAPSHOTS_DIR", tmp_path):
            with patch(
                "app.services.longitudinal_engine._load_supabase_snapshots",
                return_value=[],
            ):
                history = get_snapshot_history(municipio_code, limit=12)

        assert len(history) == 1
        assert history[0]["icpi"]["global_pct"] == 53.56

    def test_empty_dir_returns_empty_list(self, tmp_path):
        municipio_code = "130801"
        (tmp_path / municipio_code).mkdir()

        with patch("app.services.longitudinal_engine.cfg.SNAPSHOTS_DIR", tmp_path):
            with patch(
                "app.services.longitudinal_engine._load_supabase_snapshots",
                return_value=[],
            ):
                history = get_snapshot_history(municipio_code, limit=12)

        assert history == []


# ══════════════════════════════════════════════════════════════════════════════
# 9. get_longitudinal_summary (integración)
# ══════════════════════════════════════════════════════════════════════════════

class TestGetLongitudinalSummary:
    def _make_history(self) -> list[dict]:
        return [
            _make_snap(
                fecha_corte="2026-05-01",
                generated_at="2026-05-01T10:00:00+00:00",
                icpi_pct=53.0,
                clasif_riesgo="ALTO",
                riesgo_ponderado=0.40,
            ),
            _make_snap(
                fecha_corte="2026-06-01",
                generated_at="2026-06-01T10:00:00+00:00",
                icpi_pct=58.0,
                clasif_riesgo="MEDIO",
                riesgo_ponderado=0.25,
            ),
        ]

    def test_returns_correct_n_periodos(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["n_periodos"] == 2

    def test_icpi_trend_mejora(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["icpi_trend"] == "MEJORA"

    def test_last_period_label(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["last_period"] == "Jun 2026"

    def test_last_icpi_pct(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["last_icpi_pct"] == 58.0

    def test_last_riesgo(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["last_riesgo"] == "MEDIO"

    def test_last_sat_activas_count(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        # Ambos snapshots tienen 3 alertas activas
        assert summary["last_sat_activas"] == 3

    def test_rcm_table_populated(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert len(summary["rcm_table"]) == 2
        assert summary["rcm_table"][0]["periodo"] == "May 2026"
        assert summary["rcm_table"][1]["periodo"] == "Jun 2026"

    def test_icpi_series_populated(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert len(summary["icpi_series"]) == 2
        assert summary["icpi_series"][0][1] == 53.0
        assert summary["icpi_series"][1][1] == 58.0

    def test_no_snapshots_returns_error(self):
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=[],
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["n_periodos"] == 0
        assert summary["error"] is not None
        assert "No hay snapshots" in summary["error"]

    def test_error_on_exception_returns_safe_dict(self):
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            side_effect=RuntimeError("Simulated failure"),
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["error"] is not None
        assert "Simulated failure" in summary["error"]
        assert summary["n_periodos"] == 0

    def test_no_error_key_when_ok(self):
        history = self._make_history()
        with patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        ):
            summary = get_longitudinal_summary("130801")
        assert summary["error"] is None
