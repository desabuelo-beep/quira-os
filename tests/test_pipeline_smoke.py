"""
tests/test_pipeline_smoke.py — QUIRA OS · Sprint 2
Smoke test del pipeline completo en modo dry_run.

Mock de los conectores externos (DPE/SERCOP/CPCCS/GoldMaster)
para ejecutar sin red, sin Excel, sin Supabase.

Ejecutar: pytest tests/test_pipeline_smoke.py -v

Dylus Lab © 2026
"""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


# ── Fixtures de conectores mock ───────────────────────────────────────────────

_DPE_MOCK = {
    "status":      "ok",
    "source_id":   "dpe",
    "reliability": 0.95,
    "data": {
        "psg_ejecucion": 0.2985,   # 29.85% — activa SAT-III
        "psg_fidelidad": 0.92,
        "ife_inversion": 3_200_000,
        "ife_meta":      8_000_000,
    },
    "error": None,
}

_SERCOP_MOCK = {
    "status":      "ok",
    "source_id":   "sercop",
    "reliability": 0.90,
    "data": {
        "pac_publicado":        True,
        "procesos_adjudicados": 24,
        "procesos_cancelados":  4,
        "cancelados_pct":       0.167,
    },
    "error": None,
}

_CPCCS_MOCK = {
    "status":      "ok",
    "source_id":   "cpccs",
    "reliability": 0.80,
    "data": {
        "score": 42.0,
        "clasificacion": "Parcialmente Cumplida",
        "tipo_rdc": "Virtual",
    },
    "error": None,
}

_GOLD_MASTER_MOCK = {
    "status":      "ok",
    "source_id":   "gold_master",
    "reliability": 0.99,
    "sheet_rows":  51,
    "data": {
        "icpi": {
            "global":        0.5356,
            "global_pct":    53.56,
            "clasificacion": "Ruptura Sistémica",
            "historico":     {"2023": 52.1, "2024": 53.0, "2025": 53.56},
            "acumulado_q1":  None,
        },
        "tgi": {
            "score": None,   # H73 no expone TGI_SCORE — normal
            "d1": None, "d2": None, "d3": None, "d4": None, "d5": None,
        },
        "financiero": {
            # Valores reales del Gold Master Montecristi Q1-2026
            # SAT-III fallback: isp_salud_presup < 60% → activa
            "isp_salud_presup": 0.1458,   # 14.58% — activa SAT-III vía fallback
            "isp_meta":         0.65,
            "isp_brecha_pp":   -0.5042,
            "psg_ejecucion":    0.2985,   # 29.85% — ejecución total
            "psg_fidelidad":    0.92,
            # SAT-IV: inversión pública — también bajo umbral
            "ife_inversion":    0.0895,   # 8.95% < 10% umbral → activa SAT-IV
            "ife_meta":         0.10,
        },
        "contratacion":  {},
        "accountability": {},
        "sat_engine": {
            "riesgo_total":  None,
            "clasif_riesgo": None,
            "activas_count": None,
        },
        "_raw_h73": {},
    },
    "error": None,
}


# ── Smoke test ────────────────────────────────────────────────────────────────

class TestPipelineSmoke:

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_dry_run_completes(self, mock_gm, mock_cpccs, mock_serc, mock_dpe):
        """Pipeline dry_run debe completarse sin excepción."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        pipeline = SnapshotPipeline(municipio_code="130801")
        result = pipeline.run(dry_run=True)
        assert result is not None, "Pipeline dry_run devolvió None"

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_snapshot_has_required_top_keys(self, *mocks):
        """El snapshot resultante tiene las claves canónicas de primer nivel."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)

        required = {"_meta", "gad", "tgi", "icpi", "financiero",
                    "series_longitudinal", "territorial", "sat", "_pipeline"}
        missing = required - set(result.keys())
        assert not missing, f"Claves faltantes en snapshot: {missing}"

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_icpi_loaded_from_gold_master(self, *mocks):
        """ICPI global debe cargarse desde el Gold Master mock."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)
        icpi = result.get("icpi", {})
        assert icpi.get("global_pct") == pytest.approx(53.56), (
            f"ICPI esperado 53.56, obtenido: {icpi.get('global_pct')}"
        )

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_sat_evaluates_and_activates(self, *mocks):
        """Con ejecución 29.85%, SAT-III debe activarse."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)
        sat = result.get("sat", {})
        activas = sat.get("alertas_activas", sat.get("activas", []))
        assert "SAT-III" in activas, (
            f"SAT-III debe activarse con ejecución 29.85%. Activas: {activas}"
        )

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_gad_codigo_montecristi(self, *mocks):
        """El snapshot debe identificar Montecristi como municipio canónico."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)
        assert result["gad"]["codigo"] == "130801"

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_validation_passes(self, *mocks):
        """El snapshot generado debe pasar la validación canónica."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)
        validation = result["_pipeline"].get("validation", {})
        assert validation.get("status") in ("ok", "warnings"), (
            f"Validación esperaba 'ok'/'warnings', obtuvo: {validation}"
        )

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_dry_run_skips_save(self, *mocks):
        """En dry_run, save_result debe indicar 'skipped'."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)
        save = result["_pipeline"].get("save_result", {})
        assert save.get("status") == "skipped", (
            f"dry_run debe tener save_result.status='skipped': {save}"
        )

    @patch("app.connectors.dpe.fetch_dpe_data",         return_value=_DPE_MOCK)
    @patch("app.connectors.sercop.fetch_sercop_data",   return_value=_SERCOP_MOCK)
    @patch("app.connectors.cpccs.fetch_rdc_cpccs",      return_value=_CPCCS_MOCK)
    @patch("app.connectors.gold_master.fetch_gold_master_data", return_value=_GOLD_MASTER_MOCK)
    def test_traceability_score_positive(self, *mocks):
        """Con las 3 fuentes OK, traceability_score debe ser > 0."""
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        result = SnapshotPipeline(municipio_code="130801").run(dry_run=True)
        ts = result.get("traceability_score", 0)
        assert ts > 0, f"Traceability score debe ser > 0 con fuentes OK. Obtuvo: {ts}"


# ── Test de logger ────────────────────────────────────────────────────────────

class TestLogger:

    def test_get_logger_returns_logger(self):
        """get_logger debe retornar un logging.Logger."""
        import logging
        from utils.logger import get_logger
        logger = get_logger("test.quira")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_idempotent(self):
        """Dos llamadas al mismo nombre retornan el mismo logger."""
        from utils.logger import get_logger
        l1 = get_logger("test.quira.idempotent")
        l2 = get_logger("test.quira.idempotent")
        assert l1 is l2

    def test_logger_does_not_propagate(self):
        """Logger QUIRA no debe propagar al logger raíz."""
        from utils.logger import get_logger
        logger = get_logger("test.quira.noprop")
        assert not logger.propagate
