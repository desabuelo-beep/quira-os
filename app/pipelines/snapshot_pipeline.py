"""
app/pipelines/snapshot_pipeline.py — QUIRA OS · Sprint 1
Orquestador Snapshot Pipeline Territorial

Este es el corazón operacional de QUIRA en Fase 1.

Funciones:
  1. fetch_dpe()            → datos presupuestarios DPE API
  2. fetch_sercop()         → contratación viva SERCOP OCDS
  3. fetch_rdc()            → rendición de cuentas CPCCS
  4. fetch_social()         → evidencia pública (placeholder)
  5. normalize_sources()    → merge y normalización
  6. build_snapshot()       → ensamble snapshot canónico
  7. validate_snapshot()    → validación doctrinaria
  8. save_snapshot()        → persistencia Supabase/JSON
  9. emit_provenance()      → trazabilidad auditable

Flujo doctrinal: OBSERVAR → ENTENDER → VALIDAR → MEMORIZAR
Territorio canónico: Montecristi (código 130801)
Municipio de prueba multi-GAD: Manta (130901), Jipijapa (130601)

Marco: TGI Territorial — D1-D5 — SAT — ICPI
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Agregar raíz al PYTHONPATH ────────────────────────────────────────────────
_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_ROOT))

import config as cfg

logger = logging.getLogger(__name__)
logging.basicConfig(level=cfg.LOG_LEVEL if hasattr(cfg, "LOG_LEVEL") else "INFO",
                    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


# ══════════════════════════════════════════════════════════════════════════════
# SNAPSHOT PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

class SnapshotPipeline:
    """Orquestador del pipeline territorial de snapshots QUIRA.

    Uso:
        pipeline = SnapshotPipeline(ruc="1360000980001", municipio_code="130901")
        result = pipeline.run()                      # ejecución completa
        result = pipeline.run(dry_run=True)          # sin persistir
    """

    def __init__(
        self,
        ruc: str | None = None,
        municipio_code: str | None = None,
        municipio_name: str | None = None,
        dpe_establishment_id: int | None = None,
        year: int | None = None,
    ) -> None:
        from scripts.registry import get_by_ruc, get_by_code

        # ── Resolver municipio desde registry ─────────────────────────────────
        m: dict | None = None
        if ruc:
            m = get_by_ruc(ruc)
        elif municipio_code:
            m = get_by_code(municipio_code)

        if m:
            self.ruc                  = m["ruc"]
            self.municipio_code       = m["municipio_code"]
            self.municipio_name       = m.get("municipio_name") or municipio_name or m["canton"]
            self.nombre_oficial       = m.get("nombre_oficial", "")
            self.dpe_establishment_id = m.get("dpe_establishment_id") or dpe_establishment_id
        else:
            # Fallback canónico — Montecristi
            self.ruc                  = ruc or cfg.CANONICAL_RUC
            self.municipio_code       = municipio_code or cfg.CANONICAL_MUNICIPIO_CODE
            self.municipio_name       = municipio_name or cfg.CANONICAL_MUNICIPIO_NAME
            self.nombre_oficial       = ""
            self.dpe_establishment_id = dpe_establishment_id

        from datetime import date
        self.year      = year or date.today().year
        self.timestamp = datetime.now(timezone.utc)
        self._results: dict[str, Any] = {}

    # ── API pública ────────────────────────────────────────────────────────────

    def run(self, dry_run: bool = False) -> dict:
        """Ejecuta el pipeline completo de 9 pasos.

        Args:
            dry_run: Si True, ejecuta todo pero NO persiste en Supabase/disco.

        Returns:
            dict con snapshot completo + provenance.
        """
        logger.info(f"{'[DRY-RUN] ' if dry_run else ''}Pipeline → {self.municipio_name} "
                    f"({self.municipio_code}) | año {self.year}")

        # ── PASO 1–4: Adquisición ─────────────────────────────────────────────
        dpe_result     = self._step_fetch_dpe()
        sercop_result  = self._step_fetch_sercop()
        rdc_result     = self._step_fetch_rdc()
        social_result  = self._step_fetch_social()

        # ── PASO 5: Normalización ─────────────────────────────────────────────
        sources = self._step_normalize_sources(dpe_result, sercop_result, rdc_result, social_result)

        # ── PASO 6: Ensamble snapshot ─────────────────────────────────────────
        snapshot = self._step_build_snapshot(sources)

        # ── PASO 7: Validación ────────────────────────────────────────────────
        validation = self._step_validate_snapshot(snapshot)
        snapshot["_pipeline"]["validation"] = validation

        # ── PASO 8: Persistencia ──────────────────────────────────────────────
        if not dry_run:
            save_result = self._step_save_snapshot(snapshot)
            snapshot["_pipeline"]["save_result"] = save_result
        else:
            snapshot["_pipeline"]["save_result"] = {"status": "skipped", "reason": "dry_run"}

        # ── PASO 9: Provenance ────────────────────────────────────────────────
        provenance = self._step_emit_provenance(snapshot, dry_run)
        snapshot["_pipeline"]["provenance_path"] = str(provenance) if provenance else None

        self._log_summary(snapshot)
        return snapshot

    # ── PASOS INTERNOS ─────────────────────────────────────────────────────────

    def _step_fetch_dpe(self) -> dict:
        logger.info("PASO 1 → fetch_dpe()")
        if not cfg.ENABLE_DPE:
            return {"status": "disabled", "source_id": "dpe", "reliability": 0.0, "data": {}}
        try:
            from app.connectors.dpe import fetch_dpe_data
            result = fetch_dpe_data(
                ruc=self.ruc,
                establishment_id=self.dpe_establishment_id,
                year=self.year,
            )
        except Exception as exc:
            logger.error(f"  fetch_dpe error: {exc}")
            result = {"status": "failed", "source_id": "dpe", "reliability": 0.0,
                      "data": {}, "error": str(exc)}
        self._results["dpe"] = result
        logger.info(f"  DPE → {result['status']} | reliability={result['reliability']}")
        return result

    def _step_fetch_sercop(self) -> dict:
        logger.info("PASO 2 → fetch_sercop()")
        if not cfg.ENABLE_SERCOP:
            return {"status": "disabled", "source_id": "sercop", "reliability": 0.0, "data": {}}
        try:
            from app.connectors.sercop import fetch_sercop_data
            result = fetch_sercop_data(ruc=self.ruc, year=self.year)
        except Exception as exc:
            logger.error(f"  fetch_sercop error: {exc}")
            result = {"status": "failed", "source_id": "sercop", "reliability": 0.0,
                      "data": {}, "error": str(exc)}
        self._results["sercop"] = result
        logger.info(f"  SERCOP → {result['status']} | reliability={result['reliability']}")
        return result

    def _step_fetch_rdc(self) -> dict:
        logger.info("PASO 3 → fetch_rdc()")
        if not cfg.ENABLE_CPCCS:
            return {"status": "disabled", "source_id": "cpccs", "reliability": 0.0, "data": {}}
        try:
            from app.connectors.cpccs import fetch_rdc_cpccs
            result = fetch_rdc_cpccs(
                ruc=self.ruc,
                year=self.year - 1,    # RdC es del año anterior
                nombre_municipio=self.nombre_oficial or self.municipio_name,
            )
        except Exception as exc:
            logger.error(f"  fetch_rdc error: {exc}")
            result = {"status": "failed", "source_id": "cpccs", "reliability": 0.0,
                      "data": {}, "error": str(exc)}
        self._results["cpccs"] = result
        logger.info(f"  CPCCS → {result['status']} | reliability={result['reliability']}")
        return result

    def _step_fetch_social(self) -> dict:
        """Placeholder — Fase 2. YouTube/Facebook require manual verification."""
        logger.info("PASO 4 → fetch_social() [placeholder]")
        result = {
            "status":      "placeholder",
            "source_id":   "social",
            "reliability": 0.0,
            "data": {
                "nota": "Verificación manual requerida — YouTube/Facebook oficial GAD",
                "youtube_url": None,
                "facebook_url": None,
            },
        }
        self._results["social"] = result
        return result

    def _step_normalize_sources(self, dpe, sercop, rdc, social) -> dict:
        """Normaliza y merges los resultados de los 4 conectores."""
        logger.info("PASO 5 → normalize_sources()")
        return {
            "dpe":    dpe,
            "sercop": sercop,
            "cpccs":  rdc,
            "social": social,
        }

    def _step_build_snapshot(self, sources: dict) -> dict:
        """Ensambla el snapshot canónico con namespace doctrinal."""
        logger.info("PASO 6 → build_snapshot()")

        traceability = self._calculate_traceability(sources)
        coverage     = self._calculate_coverage(sources)
        missing_dims = self._calculate_missing_dimensions(sources)

        # ── Namespace doctrinal (AJUSTE 2 del Sprint 1) ───────────────────────
        snapshot = {
            "_meta": {
                "schema_version": cfg.SNAPSHOT_SCHEMA if hasattr(cfg, "SNAPSHOT_SCHEMA") else "1.0",
                "pipeline_version": cfg.PIPELINE_VERSION if hasattr(cfg, "PIPELINE_VERSION") else "1.0",
                "generated_at": self.timestamp.isoformat(),
                "year": self.year,
                "fecha_corte": self.timestamp.date().isoformat(),
                "version_excel": "pipeline-generated",
            },
            "gad": {
                "codigo": self.municipio_code,
                "nombre": self.municipio_name,
                "ruc":    self.ruc,
            },
            "doctrine": cfg.DOCTRINE if hasattr(cfg, "DOCTRINE") else {
                "framework":   "TGI Territorial",
                "dimensions":  ["D1", "D2", "D3", "D4", "D5"],
                "sat_enabled": True,
            },
            "tgi": {
                "score": None,   # calculado desde Gold Master Excel
                "nota":  "TGI requiere Gold Master Excel — este snapshot es Q1-Observación",
            },
            "financiero": {
                "nota": "Datos financieros cargados desde Gold Master Excel o DPE CSV",
            },
            "series_longitudinal": {},
            "territorial": {},
            "contratacion": sources["sercop"].get("data", {}),
            "accountability": {
                "rdc": sources["cpccs"].get("data", {}),
            },
            "sources": {k: {
                "status":      v.get("status"),
                "reliability": v.get("reliability"),
                "error":       v.get("error"),
            } for k, v in sources.items()},
            "traceability_score":  traceability,
            "coverage_score":      coverage,
            "source_confidence":   round(
                sum(v.get("reliability", 0) * cfg.PIPELINE_WEIGHTS.get(v.get("source_id", ""), 0)
                    for v in [sources["dpe"], sources["sercop"], sources["cpccs"]]), 3
            ) if hasattr(cfg, "PIPELINE_WEIGHTS") else 0.0,
            "missing_dimensions":  missing_dims,
            "_pipeline": {
                "run_id":    f"{self.municipio_code}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}",
                "dry_run":   False,
            },
        }
        return snapshot

    def _step_validate_snapshot(self, snapshot: dict) -> dict:
        """Valida el snapshot contra el esquema canónico."""
        logger.info("PASO 7 → validate_snapshot()")
        try:
            from utils.snapshot_io import validate_snapshot
            ok, errors = validate_snapshot(snapshot)
            status = "ok" if ok else "warnings"
            logger.info(f"  Validación → {status} | errores: {errors}")
            return {"status": status, "errors": errors}
        except Exception as exc:
            logger.warning(f"  Validación no ejecutada: {exc}")
            return {"status": "skipped", "errors": [str(exc)]}

    def _step_save_snapshot(self, snapshot: dict) -> dict:
        """Persiste el snapshot en data/snapshots/ + Supabase."""
        logger.info("PASO 8 → save_snapshot()")
        saved_files = []

        # ── Guardar JSON local en data/snapshots/ ─────────────────────────────
        try:
            snap_dir = cfg.SNAPSHOTS_DIR / self.municipio_code
            snap_dir.mkdir(parents=True, exist_ok=True)
            filename  = f"{self.municipio_code}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}.json"
            snap_path = snap_dir / filename
            with open(snap_path, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, ensure_ascii=False, indent=2)
            saved_files.append(str(snap_path))
            logger.info(f"  Guardado JSON: {snap_path}")
        except Exception as exc:
            logger.error(f"  Error guardando JSON: {exc}")

        # ── Intentar Supabase ─────────────────────────────────────────────────
        supabase_result = {"status": "skipped", "reason": "no connection configured"}
        try:
            from sentinel.db_config import get_connection
            conn = get_connection()
            from utils.snapshot_io import save_snapshot
            ok, msg = save_snapshot(conn, snapshot, uploaded_by="pipeline", notas="auto-pipeline")
            conn.close()
            supabase_result = {"status": "ok" if ok else "error", "message": msg}
            logger.info(f"  Supabase → {supabase_result['status']}: {msg}")
        except Exception as exc:
            supabase_result = {"status": "skipped", "reason": str(exc)}
            logger.debug(f"  Supabase no disponible: {exc}")

        return {
            "status":        "ok" if saved_files else "failed",
            "saved_files":   saved_files,
            "supabase":      supabase_result,
        }

    def _step_emit_provenance(self, snapshot: dict, dry_run: bool) -> Path | None:
        """Emite JSON de provenance para auditoría y trazabilidad."""
        logger.info("PASO 9 → emit_provenance()")
        try:
            provenance = {
                "run_id":         snapshot["_pipeline"]["run_id"],
                "generated_at":   self.timestamp.isoformat(),
                "municipio_code": self.municipio_code,
                "municipio_name": self.municipio_name,
                "ruc":            self.ruc,
                "year":           self.year,
                "dry_run":        dry_run,
                "doctrine":       snapshot.get("doctrine", {}),
                "sources": {k: {
                    "status":      v.get("status"),
                    "reliability": v.get("reliability"),
                    "error":       v.get("error"),
                } for k, v in self._results.items()},
                "scores": {
                    "traceability_score": snapshot.get("traceability_score"),
                    "coverage_score":     snapshot.get("coverage_score"),
                    "source_confidence":  snapshot.get("source_confidence"),
                },
                "missing_dimensions": snapshot.get("missing_dimensions", []),
                "validation":         snapshot["_pipeline"].get("validation", {}),
            }

            prov_dir = cfg.SNAPSHOTS_DIR / self.municipio_code / "provenance"
            prov_dir.mkdir(parents=True, exist_ok=True)
            prov_path = prov_dir / f"provenance_{snapshot['_pipeline']['run_id']}.json"
            with open(prov_path, "w", encoding="utf-8") as f:
                json.dump(provenance, f, ensure_ascii=False, indent=2)
            logger.info(f"  Provenance → {prov_path}")
            return prov_path
        except Exception as exc:
            logger.error(f"  Error emitiendo provenance: {exc}")
            return None

    # ── CÁLCULOS INTERNOS ──────────────────────────────────────────────────────

    def _calculate_traceability(self, sources: dict) -> float:
        """TRACEABILITY_SCORE = Σ(reliability_i × weight_i) × 100."""
        weights  = getattr(cfg, "PIPELINE_WEIGHTS", {"dpe": 0.40, "sercop": 0.35, "cpccs": 0.25})
        score    = 0.0
        for source_id, weight in weights.items():
            rel = sources.get(source_id, {}).get("reliability", 0.0) or 0.0
            score += rel * weight
        return round(score * 100, 2)

    def _calculate_coverage(self, sources: dict) -> float:
        """Coverage = proporción de fuentes con status 'ok'."""
        active = [v for k, v in sources.items() if k != "social"]
        ok     = sum(1 for v in active if v.get("status") == "ok")
        return round(ok / len(active), 2) if active else 0.0

    def _calculate_missing_dimensions(self, sources: dict) -> list[str]:
        """Detecta dimensiones TGI sin cobertura de datos."""
        missing = []
        dpe_ok  = sources.get("dpe", {}).get("status") in ("ok", "partial")
        serc_ok = sources.get("sercop", {}).get("status") in ("ok", "partial")
        cpccs_ok = sources.get("cpccs", {}).get("status") in ("ok", "partial")

        if not dpe_ok:
            missing.extend(["D3-financiero", "D5-presupuesto"])
        if not serc_ok:
            missing.append("D1-contratacion")
        if not cpccs_ok:
            missing.append("D5-rdc")
        if not dpe_ok and not serc_ok:
            missing.append("D2-planificacion")
        if not sources.get("social", {}).get("data", {}).get("youtube_url"):
            missing.append("D5-evidencia-publica")
        return sorted(set(missing))

    def _log_summary(self, snapshot: dict) -> None:
        logger.info("─" * 60)
        logger.info(f"  QUIRA Snapshot — {self.municipio_name} ({self.municipio_code})")
        logger.info(f"  Año: {self.year} | Generado: {self.timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
        logger.info(f"  TRACEABILITY SCORE : {snapshot.get('traceability_score', 0):.1f}/100")
        logger.info(f"  COVERAGE SCORE     : {snapshot.get('coverage_score', 0):.0%}")
        logger.info(f"  SOURCE CONFIDENCE  : {snapshot.get('source_confidence', 0):.3f}")
        logger.info(f"  MISSING DIMENSIONS : {snapshot.get('missing_dimensions', [])}")
        logger.info(f"  VALIDATION         : {snapshot['_pipeline'].get('validation', {}).get('status', '?')}")
        logger.info("─" * 60)
