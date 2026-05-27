"""
Tests — reliability_tracker.py (Sprint 3 · P3)

Cubre:
  · FUENTES_CATALOG estructura y completitud
  · get_reliability_dashboard() — con y sin snapshot
  · get_reliability_history() — historial longitudinal
  · get_traceability_trend() — serie temporal
  · get_source_health() — diagnóstico de salud
  · build_reliability_report() — informe completo
  · Helpers internos: _effective_reliability, _reliability_label

Tests: 42 · Todos sin llamadas reales a Supabase ni DPE.
Dylus Lab © 2026
"""
from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock

from app.services.reliability_tracker import (
    FUENTES_CATALOG,
    _effective_reliability,
    _reliability_label,
    _get_source_data,
    get_reliability_dashboard,
    get_reliability_history,
    get_traceability_trend,
    get_source_health,
    build_reliability_report,
)


# ══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ══════════════════════════════════════════════════════════════════════════════

def _snap(*, fecha_corte="2026-05-01", traz=0.89, src_conf=0.93,
          dpe_rel=0.95, sercop_rel=0.92, cpccs_rel=0.78, gm_rel=0.99,
          dpe_status="ok", sercop_status="ok", cpccs_status="ok", gm_status="ok",
          dpe_error=None) -> dict:
    """Snapshot mínimo válido para pruebas."""
    return {
        "_meta": {"fecha_corte": fecha_corte, "generated_at": f"{fecha_corte}T10:00:00"},
        "traceability_score": traz,
        "source_confidence":  src_conf,
        "sources": {
            "gold_master": {"status": gm_status,     "reliability": gm_rel,     "error": None},
            "dpe":         {"status": dpe_status,    "reliability": dpe_rel,    "error": dpe_error},
            "sercop":      {"status": sercop_status, "reliability": sercop_rel, "error": None},
            "cpccs":       {"status": cpccs_status,  "reliability": cpccs_rel,  "error": None},
        },
    }


def _history_2() -> list[dict]:
    """Dos snapshots de meses distintos para pruebas longitudinales."""
    return [
        _snap(fecha_corte="2026-04-01", traz=0.82, dpe_rel=0.90, cpccs_rel=0.75),
        _snap(fecha_corte="2026-05-01", traz=0.89, dpe_rel=0.95, cpccs_rel=0.78),
    ]


# ══════════════════════════════════════════════════════════════════════════════
# TestFuentesCatalog
# ══════════════════════════════════════════════════════════════════════════════

class TestFuentesCatalog:
    def test_has_four_sources(self):
        assert len(FUENTES_CATALOG) == 4

    def test_required_keys_present(self):
        required = {"key", "nombre", "categoria", "icono", "reliability_base", "descripcion"}
        for f in FUENTES_CATALOG:
            assert required.issubset(f.keys()), f"Fuente {f.get('key')} falta keys"

    def test_known_keys(self):
        keys = {f["key"] for f in FUENTES_CATALOG}
        assert keys == {"gold_master", "dpe", "sercop", "cpccs"}

    def test_gold_master_highest_reliability(self):
        gm = next(f for f in FUENTES_CATALOG if f["key"] == "gold_master")
        others = [f["reliability_base"] for f in FUENTES_CATALOG if f["key"] != "gold_master"]
        assert gm["reliability_base"] >= max(others)

    def test_reliability_base_range(self):
        for f in FUENTES_CATALOG:
            assert 0.0 <= f["reliability_base"] <= 1.0, f"Fuera de rango: {f['key']}"

    def test_cpccs_lower_than_dpe_and_sercop(self):
        rel = {f["key"]: f["reliability_base"] for f in FUENTES_CATALOG}
        assert rel["cpccs"] < rel["dpe"]
        assert rel["cpccs"] < rel["sercop"]


# ══════════════════════════════════════════════════════════════════════════════
# TestHelpers
# ══════════════════════════════════════════════════════════════════════════════

class TestEffectiveReliability:
    def test_uses_snap_value_when_valid(self):
        assert _effective_reliability(0.88, 0.95) == 0.88

    def test_uses_base_when_snap_none(self):
        assert _effective_reliability(None, 0.95) == 0.95

    def test_uses_base_when_snap_out_of_range_high(self):
        assert _effective_reliability(1.5, 0.95) == 0.95

    def test_uses_base_when_snap_out_of_range_low(self):
        assert _effective_reliability(-0.1, 0.90) == 0.90

    def test_zero_is_valid(self):
        assert _effective_reliability(0.0, 0.95) == 0.0

    def test_one_is_valid(self):
        assert _effective_reliability(1.0, 0.95) == 1.0

    def test_rounds_to_4_decimals(self):
        result = _effective_reliability(0.123456789, 0.5)
        assert len(str(result).split(".")[-1]) <= 4

    def test_handles_string_number(self):
        # reliability puede venir como string en algunos snapshots legacy
        assert _effective_reliability("0.88", 0.95) == 0.88  # type: ignore


class TestReliabilityLabel:
    def test_excelente(self):
        assert _reliability_label(0.99) == "Excelente"
        assert _reliability_label(0.95) == "Excelente"

    def test_muy_bueno(self):
        assert _reliability_label(0.90) == "Muy bueno"
        assert _reliability_label(0.85) == "Muy bueno"

    def test_funcional(self):
        assert _reliability_label(0.80) == "Funcional"
        assert _reliability_label(0.70) == "Funcional"

    def test_limitado(self):
        assert _reliability_label(0.65) == "Limitado"
        assert _reliability_label(0.50) == "Limitado"

    def test_critico(self):
        assert _reliability_label(0.49) == "Crítico"
        assert _reliability_label(0.0)  == "Crítico"


class TestGetSourceData:
    def test_extracts_known_source(self):
        snap = _snap(dpe_rel=0.92, dpe_status="ok")
        result = _get_source_data(snap, "dpe")
        assert result["reliability"] == 0.92
        assert result["status"] == "ok"
        assert result["error"] is None

    def test_unknown_source_returns_defaults(self):
        snap = _snap()
        result = _get_source_data(snap, "nonexistent_source")
        assert result["status"] == "unknown"
        assert result["reliability"] is None

    def test_extracts_error_field(self):
        snap = _snap(dpe_error="Timeout 503", dpe_status="error")
        result = _get_source_data(snap, "dpe")
        assert result["error"] == "Timeout 503"

    def test_empty_snap_returns_defaults(self):
        result = _get_source_data({}, "dpe")
        assert result["status"] == "unknown"


# ══════════════════════════════════════════════════════════════════════════════
# TestGetReliabilityDashboard
# ══════════════════════════════════════════════════════════════════════════════

class TestGetReliabilityDashboard:
    def _mock_load(self, snap):
        return patch("app.services.reliability_tracker.load_snapshot",
                     return_value=(snap, {}))

    def test_returns_four_entries(self):
        with patch("utils.snapshot_io.load_snapshot", return_value=(_snap(), {})):
            result = get_reliability_dashboard()
        assert len(result) == 4

    def test_required_keys_in_each_entry(self):
        required = {"key", "nombre", "categoria", "icono", "reliability",
                    "label", "status", "error", "descripcion"}
        with patch("utils.snapshot_io.load_snapshot", return_value=(_snap(), {})):
            result = get_reliability_dashboard()
        for item in result:
            assert required.issubset(item.keys())

    def test_gold_master_highest_reliability(self):
        with patch("utils.snapshot_io.load_snapshot", return_value=(_snap(), {})):
            result = get_reliability_dashboard()
        rels = {item["key"]: item["reliability"] for item in result}
        assert rels["gold_master"] >= rels["dpe"]
        assert rels["gold_master"] >= rels["sercop"]
        assert rels["gold_master"] >= rels["cpccs"]

    def test_uses_snapshot_reliability_over_base(self):
        snap = _snap(dpe_rel=0.88)
        with patch("utils.snapshot_io.load_snapshot", return_value=(snap, {})):
            result = get_reliability_dashboard()
        dpe = next(i for i in result if i["key"] == "dpe")
        assert dpe["reliability"] == 0.88

    def test_no_snapshot_uses_base_reliability(self):
        with patch("utils.snapshot_io.load_snapshot", return_value=(None, None)):
            result = get_reliability_dashboard()
        assert len(result) == 4
        for item in result:
            catalog_entry = next(f for f in FUENTES_CATALOG if f["key"] == item["key"])
            assert item["reliability"] == catalog_entry["reliability_base"]

    def test_status_propagated(self):
        snap = _snap(dpe_status="error", dpe_error="API down")
        with patch("utils.snapshot_io.load_snapshot", return_value=(snap, {})):
            result = get_reliability_dashboard()
        dpe = next(i for i in result if i["key"] == "dpe")
        assert dpe["status"] == "error"
        assert dpe["error"] == "API down"

    def test_label_assigned(self):
        with patch("utils.snapshot_io.load_snapshot", return_value=(_snap(), {})):
            result = get_reliability_dashboard()
        for item in result:
            assert item["label"] in ("Excelente", "Muy bueno", "Funcional", "Limitado", "Crítico")

    def test_handles_load_exception_gracefully(self):
        with patch("utils.snapshot_io.load_snapshot", side_effect=Exception("DB down")):
            result = get_reliability_dashboard()
        # Should still return catalog entries with base reliability
        assert len(result) == 4


# ══════════════════════════════════════════════════════════════════════════════
# TestGetReliabilityHistory
# ══════════════════════════════════════════════════════════════════════════════

class TestGetReliabilityHistory:
    def _mock_history(self, snaps):
        # get_snapshot_history se importa lazy dentro de la función → patchear en la fuente
        return patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=snaps,
        )

    def test_returns_list(self):
        with self._mock_history(_history_2()):
            result = get_reliability_history()
        assert isinstance(result, list)

    def test_correct_length(self):
        with self._mock_history(_history_2()):
            result = get_reliability_history()
        assert len(result) == 2

    def test_required_keys(self):
        required = {"periodo", "fecha_corte", "traceability", "source_conf", "fuentes"}
        with self._mock_history(_history_2()):
            result = get_reliability_history()
        for row in result:
            assert required.issubset(row.keys())

    def test_fuentes_has_all_sources(self):
        with self._mock_history(_history_2()):
            result = get_reliability_history()
        for row in result:
            assert set(row["fuentes"].keys()) == {"gold_master", "dpe", "sercop", "cpccs"}

    def test_traceability_score_propagated(self):
        snaps = [_snap(fecha_corte="2026-04-01", traz=0.82)]
        with self._mock_history(snaps):
            result = get_reliability_history()
        assert result[0]["traceability"] == 0.82

    def test_empty_history_returns_empty_list(self):
        with self._mock_history([]):
            result = get_reliability_history()
        assert result == []

    def test_oldest_first_order_preserved(self):
        """El tracker no reordena — preserva el orden del longitudinal_engine."""
        snaps = _history_2()  # oldest-first
        with self._mock_history(snaps):
            result = get_reliability_history()
        assert result[0]["fecha_corte"] < result[1]["fecha_corte"]

    def test_source_reliability_in_fuentes(self):
        snap = _snap(fecha_corte="2026-05-01", cpccs_rel=0.75)
        with self._mock_history([snap]):
            result = get_reliability_history()
        assert result[0]["fuentes"]["cpccs"]["reliability"] == 0.75


# ══════════════════════════════════════════════════════════════════════════════
# TestGetTraceabilityTrend
# ══════════════════════════════════════════════════════════════════════════════

class TestGetTraceabilityTrend:
    def _mock_history(self, snaps):
        return patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=snaps,
        )

    def test_returns_list_of_tuples(self):
        with self._mock_history(_history_2()):
            result = get_traceability_trend()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_correct_length(self):
        with self._mock_history(_history_2()):
            result = get_traceability_trend()
        assert len(result) == 2

    def test_scores_match_snapshots(self):
        snaps = [
            _snap(fecha_corte="2026-04-01", traz=0.82),
            _snap(fecha_corte="2026-05-01", traz=0.89),
        ]
        with self._mock_history(snaps):
            result = get_traceability_trend()
        scores = [v for _, v in result]
        assert scores[0] == 0.82
        assert scores[1] == 0.89

    def test_empty_history_returns_empty_list(self):
        with self._mock_history([]):
            result = get_traceability_trend()
        assert result == []

    def test_none_traz_propagated(self):
        snap = _snap(fecha_corte="2026-05-01")
        snap["traceability_score"] = None
        with self._mock_history([snap]):
            result = get_traceability_trend()
        assert result[0][1] is None


# ══════════════════════════════════════════════════════════════════════════════
# TestGetSourceHealth
# ══════════════════════════════════════════════════════════════════════════════

class TestGetSourceHealth:
    def test_returns_dict_with_four_keys(self):
        with patch("utils.snapshot_io.load_snapshot", return_value=(_snap(), {})):
            result = get_source_health()
        assert set(result.keys()) == {"gold_master", "dpe", "sercop", "cpccs"}

    def test_ok_high_reliability_is_ok(self):
        snap = _snap(dpe_rel=0.95, dpe_status="ok")
        with patch("utils.snapshot_io.load_snapshot", return_value=(snap, {})):
            result = get_source_health()
        assert result["dpe"] == "OK"

    def test_ok_low_reliability_is_degraded(self):
        snap = _snap(cpccs_rel=0.65, cpccs_status="ok")
        with patch("utils.snapshot_io.load_snapshot", return_value=(snap, {})):
            result = get_source_health()
        assert result["cpccs"] == "DEGRADED"

    def test_error_status_is_error(self):
        snap = _snap(dpe_status="error", dpe_error="503 Service Unavailable")
        with patch("utils.snapshot_io.load_snapshot", return_value=(snap, {})):
            result = get_source_health()
        assert result["dpe"] == "ERROR"

    def test_unknown_status_is_unknown(self):
        with patch("utils.snapshot_io.load_snapshot", return_value=(None, None)):
            result = get_source_health()
        for v in result.values():
            assert v == "UNKNOWN"

    def test_all_values_are_valid_states(self):
        valid = {"OK", "DEGRADED", "ERROR", "UNKNOWN"}
        with patch("utils.snapshot_io.load_snapshot", return_value=(_snap(), {})):
            result = get_source_health()
        for v in result.values():
            assert v in valid


# ══════════════════════════════════════════════════════════════════════════════
# TestBuildReliabilityReport
# ══════════════════════════════════════════════════════════════════════════════

class TestBuildReliabilityReport:
    def _mock_all(self, snap, history):
        load_patch = patch("utils.snapshot_io.load_snapshot",
                           return_value=(snap, {}))
        hist_patch = patch(
            "app.services.longitudinal_engine.get_snapshot_history",
            return_value=history,
        )
        return load_patch, hist_patch

    def test_returns_required_keys(self):
        required = {
            "dashboard", "history", "traceability_series",
            "source_health", "avg_reliability", "n_ok", "n_errors", "error",
        }
        lp, hp = self._mock_all(_snap(), _history_2())
        with lp, hp:
            result = build_reliability_report()
        assert required.issubset(result.keys())

    def test_error_is_none_on_success(self):
        lp, hp = self._mock_all(_snap(), _history_2())
        with lp, hp:
            result = build_reliability_report()
        assert result["error"] is None

    def test_avg_reliability_is_float(self):
        lp, hp = self._mock_all(_snap(), _history_2())
        with lp, hp:
            result = build_reliability_report()
        assert isinstance(result["avg_reliability"], float)
        assert 0.0 <= result["avg_reliability"] <= 1.0

    def test_n_ok_counts_ok_sources(self):
        snap = _snap(dpe_status="ok", sercop_status="ok",
                     cpccs_status="error", gm_status="ok")
        lp, hp = self._mock_all(snap, [snap])
        with lp, hp:
            result = build_reliability_report()
        assert result["n_ok"] == 3

    def test_n_errors_counts_error_sources(self):
        snap = _snap(dpe_error="Timeout", cpccs_status="error")
        lp, hp = self._mock_all(snap, [snap])
        with lp, hp:
            result = build_reliability_report()
        assert result["n_errors"] >= 1

    def test_dashboard_length(self):
        lp, hp = self._mock_all(_snap(), _history_2())
        with lp, hp:
            result = build_reliability_report()
        assert len(result["dashboard"]) == 4

    def test_history_length(self):
        lp, hp = self._mock_all(_snap(), _history_2())
        with lp, hp:
            result = build_reliability_report()
        assert len(result["history"]) == 2

    def test_error_returned_on_exception(self):
        # Patchear get_reliability_dashboard directamente para forzar excepción no capturada
        with patch(
            "app.services.reliability_tracker.get_reliability_dashboard",
            side_effect=RuntimeError("Fallo total"),
        ):
            result = build_reliability_report()
        assert result["error"] is not None
        assert "Fallo total" in result["error"]
        assert result["dashboard"] == []
