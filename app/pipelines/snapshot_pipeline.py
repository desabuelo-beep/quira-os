"""
app/pipelines/snapshot_pipeline.py — QUIRA OS · Sprint 2
Orquestador Snapshot Pipeline Territorial

Este es el corazón operacional de QUIRA en Fase 1-2.

Funciones:
  1. fetch_dpe()            → datos presupuestarios DPE API
  2. fetch_sercop()         → contratación viva SERCOP OCDS
  3. fetch_rdc()            → rendición de cuentas CPCCS
  4. fetch_social()         → evidencia pública (placeholder)
  5. fetch_gold_master()    → métricas canónicas Gold Master (fallback + TGI)
  6. normalize_sources()    → merge y normalización
  7. build_snapshot()       → ensamble snapshot canónico
  8. eval_sat()             → evaluación SAT (triple ancla legal+operativa+doctrinal)
  9. validate_snapshot()    → validación doctrinaria
  10. save_snapshot()        → persistencia Supabase/JSON
  11. emit_provenance()      → trazabilidad auditable

Flujo doctrinal: OBSERVAR → ENTENDER → VALIDAR → MEMORIZAR
Territorio canónico: Montecristi (código 130801)
Municipio de prueba multi-GAD: Manta (130901), Jipijapa (130601)

Marco: TGI Territorial — D1-D5 — SAT — ICPI
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ── Agregar raíz al PYTHONPATH ────────────────────────────────────────────────
_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_ROOT))

import config as cfg
from utils.logger import get_logger, configure_root

configure_root()  # silenciar librerías externas (httpx, urllib3…)
logger = get_logger(__name__, level=getattr(cfg, "LOG_LEVEL", "INFO"))


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

        # ── PASO 5: Gold Master (métricas canónicas + TGI fallback) ──────────
        gm_result = self._step_fetch_gold_master()

        # ── PASO 6: Normalización ─────────────────────────────────────────────
        sources = self._step_normalize_sources(
            dpe_result, sercop_result, rdc_result, social_result, gm_result
        )

        # ── PASO 7: Ensamble snapshot ─────────────────────────────────────────
        snapshot = self._step_build_snapshot(sources)

        # ── PASO 8: Evaluación SAT ────────────────────────────────────────────
        sat_result = self._step_eval_sat(snapshot)
        snapshot["sat"] = sat_result

        # ── PASO 9: Validación ────────────────────────────────────────────────
        validation = self._step_validate_snapshot(snapshot)
        snapshot["_pipeline"]["validation"] = validation

        # ── PASO 10: Persistencia ─────────────────────────────────────────────
        if not dry_run:
            save_result = self._step_save_snapshot(snapshot)
            snapshot["_pipeline"]["save_result"] = save_result
        else:
            snapshot["_pipeline"]["save_result"] = {"status": "skipped", "reason": "dry_run"}

        # ── PASO 11: Provenance ───────────────────────────────────────────────
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

    def _step_fetch_gold_master(self) -> dict:
        """PASO 5 — Lee métricas canónicas del Gold Master (H73_OUTPUT_API).

        Actúa como fuente de verdad TGI cuando las APIs institucionales
        no están disponibles, y siempre provee el score TGI certificado.
        """
        logger.info("PASO 5 → fetch_gold_master()")
        try:
            from app.connectors.gold_master import fetch_gold_master_data
            gm_path = getattr(cfg, "GOLD_MASTER_PATH", None)
            result = fetch_gold_master_data(gold_master_path=gm_path)
        except Exception as exc:
            logger.error(f"  fetch_gold_master error: {exc}")
            result = {
                "status": "failed", "source_id": "gold_master",
                "reliability": 0.0, "data": {}, "error": str(exc),
            }
        self._results["gold_master"] = result
        logger.info(
            f"  GoldMaster → {result['status']} | rows={result.get('sheet_rows', 0)} | "
            f"reliability={result.get('reliability', 0)}"
        )
        return result

    def _step_eval_sat(self, snapshot: dict) -> dict:
        """PASO 8 — Evalúa el catálogo SAT completo contra el snapshot.

        Produce alertas con triple ancla: Base Legal + Operativa + Doctrinal QUIRA.
        Clasificación: BAJO / MEDIO / ALTO / CRÍTICO
        """
        logger.info("PASO 8 → eval_sat()")
        try:
            from app.services.sat_evaluator import evaluate_sat
            result = evaluate_sat(snapshot)
            logger.info(
                f"  SAT → activas: {result['total_activas']}/{result['total_evaluadas']} | "
                f"riesgo: {result['riesgo_ponderado']:.3f} → {result['clasif_riesgo']} | "
                f"sin datos: {len(result['datos_insuficientes'])}"
            )
        except Exception as exc:
            logger.error(f"  eval_sat error: {exc}")
            result = {
                "alertas": [], "activas": [], "riesgo_ponderado": 0.0,
                "clasif_riesgo": "SIN_DATOS", "sat_score": 0.0,
                "datos_insuficientes": [], "total_evaluadas": 0, "total_activas": 0,
                "error": str(exc),
            }
        return result

    def _step_normalize_sources(self, dpe, sercop, rdc, social, gold_master=None) -> dict:
        """Normaliza y merges los resultados de los conectores."""
        logger.info("PASO 6 → normalize_sources()")
        return {
            "dpe":         dpe,
            "sercop":      sercop,
            "cpccs":       rdc,
            "social":      social,
            "gold_master": gold_master or {},
        }

    def _step_build_snapshot(self, sources: dict) -> dict:
        """Ensambla el snapshot canónico con namespace doctrinal."""
        logger.info("PASO 7 → build_snapshot()")

        traceability = self._calculate_traceability(sources)
        coverage     = self._calculate_coverage(sources)
        missing_dims = self._calculate_missing_dimensions(sources)

        # ── Gold Master data (métricas canónicas certificadas) ─────────────────
        gm_data = sources.get("gold_master", {}).get("data", {}) or {}
        gm_icpi = gm_data.get("icpi", {})
        gm_tgi  = gm_data.get("tgi", {})
        gm_fin  = gm_data.get("financiero", {})
        gm_cont = gm_data.get("contratacion", {})
        gm_acc  = gm_data.get("accountability", {})
        gm_sat  = gm_data.get("sat_engine", {})

        # ── TGI: desde Gold Master si disponible ───────────────────────────────
        tgi_score = gm_tgi.get("score")
        tgi_block = {
            "score":  tgi_score,
            "d1":     gm_tgi.get("d1"),
            "d2":     gm_tgi.get("d2"),
            "d3":     gm_tgi.get("d3"),
            "d4":     gm_tgi.get("d4"),
            "d5":     gm_tgi.get("d5"),
            "nota":   ("Calculado desde Gold Master H73_OUTPUT_API"
                       if tgi_score is not None
                       else "TGI requiere Gold Master Excel — este snapshot es Q1-Observación"),
            "fuente": "gold_master_h73" if tgi_score is not None else "pendiente",
        }

        # ── ICPI: desde Gold Master ────────────────────────────────────────────
        icpi_block = {
            "global":        gm_icpi.get("global"),
            "global_pct":    gm_icpi.get("global_pct"),
            "clasificacion": gm_icpi.get("clasificacion"),
            "historico":     gm_icpi.get("historico", {}),
            "acumulado_q1":  gm_icpi.get("acumulado_q1"),
            "fuente":        "gold_master_h73" if gm_icpi.get("global") is not None else "pendiente",
        }

        # ── Financiero: pipeline API primero, Gold Master como fallback ────────
        api_fin = sources.get("dpe", {}).get("data", {}) or {}
        financiero_block = {
            **gm_fin,           # base desde Gold Master
            **api_fin,          # sobreescribir con datos API si disponibles
            "fuente_primaria": "dpe_api" if api_fin else "gold_master_h73",
        }

        # ── Namespace doctrinal ────────────────────────────────────────────────
        snapshot = {
            "_meta": {
                "schema_version":  getattr(cfg, "SNAPSHOT_SCHEMA", "1.0"),
                "pipeline_version": getattr(cfg, "PIPELINE_VERSION", "1.0.0-sprint2"),
                "generated_at":    self.timestamp.isoformat(),
                "year":            self.year,
                "fecha_corte":     self.timestamp.date().isoformat(),
                "version_excel":   "SIAP-ICPI_GOLD_MASTER_v5.5_TGI",
                "gold_master_ok":  sources.get("gold_master", {}).get("status") == "ok",
            },
            "gad": {
                "codigo": self.municipio_code,
                "nombre": self.municipio_name,
                "ruc":    self.ruc,
            },
            "doctrine": getattr(cfg, "DOCTRINE", {
                "framework":   "TGI Territorial",
                "dimensions":  ["D1", "D2", "D3", "D4", "D5"],
                "sat_enabled": True,
            }),
            "tgi":      tgi_block,
            "icpi":     icpi_block,
            "financiero":      financiero_block,
            "series_longitudinal": {},
            "territorial":    {},
            "contratacion":   {**gm_cont, **(sources["sercop"].get("data", {}) or {})},
            "accountability": {
                "rdc":  sources["cpccs"].get("data", {}),
                "gold_master": gm_acc,
            },
            "gold_master_data": gm_data,   # preservado para SAT evaluator
            "sources": {k: {
                "status":      v.get("status") if isinstance(v, dict) else None,
                "reliability": v.get("reliability") if isinstance(v, dict) else None,
                "error":       v.get("error") if isinstance(v, dict) else None,
            } for k, v in sources.items()},
            "traceability_score": traceability,
            "coverage_score":     coverage,
            "source_confidence":  round(
                sum(
                    sources.get(sid, {}).get("reliability", 0)
                    * getattr(cfg, "PIPELINE_WEIGHTS", {"dpe": 0.40, "sercop": 0.35, "cpccs": 0.25}).get(sid, 0)
                    for sid in ("dpe", "sercop", "cpccs")
                ), 3
            ),
            "missing_dimensions": missing_dims,
            "_pipeline": {
                "run_id":  f"{self.municipio_code}_{self.timestamp.strftime('%Y%m%d_%H%M%S')}",
                "dry_run": False,
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
            from sentinel.db_config import get_connection  # noqa: QUIRA-DEPR — migrar a utils.db_config en v7.0
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
        """Emite el JSON de procedencia de la corrida.

        UN ENSAYO NO SE GUARDA DONDE SE GUARDA LA OBSERVACIÓN (2026-08-25).
        Hasta hoy, seco y real escribían **en el mismo directorio y con el mismo
        patrón de nombre**; la diferencia vivía sólo dentro del archivo, en un
        campo. El recuento del día lo puso en números:

            85 corridas en seco · 4 reales

        Es decir: el 95 % de la carpeta de procedencia del sujeto observado no
        observó nada. Quien la barriera con un glob obtenía 89 registros que
        *parecen* procedencia de 130801 — y ninguna herramienta se lo habría
        advertido, porque el nombre del archivo prometía lo que el contenido no
        cumplía.

        Es el mismo error que este dominio persigue afuera —«el nombre del
        enlace no es evidencia», tres veces contra el GAD— cometido aquí contra
        nosotros mismos. Un `dry_run` no dice nada del sujeto: dice que
        ejercitamos el instrumento.

        La distinción ya estaba **declarada** en el dato (`dry_run`); lo que
        faltaba era que la **estructura la respetara**. Nada nace en Python
        (Regla 9): esto sólo obliga al disco a decir lo que el campo ya decía.
        """
        logger.info("PASO 11 → emit_provenance()")   # era «PASO 9»: etiqueta falsa
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
            if dry_run:                       # el ensayo no se mezcla con la observación
                prov_dir = prov_dir / "ensayos"
            prov_dir.mkdir(parents=True, exist_ok=True)
            prefijo = "ensayo" if dry_run else "provenance"
            prov_path = prov_dir / f"{prefijo}_{snapshot['_pipeline']['run_id']}.json"
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
        sat  = snapshot.get("sat", {})
        icpi = snapshot.get("icpi", {})
        tgi  = snapshot.get("tgi", {})
        logger.info("─" * 60)
        logger.info(f"  QUIRA Snapshot — {self.municipio_name} ({self.municipio_code})")
        logger.info(f"  Año: {self.year} | Generado: {self.timestamp.strftime('%Y-%m-%d %H:%M UTC')}")
        logger.info(f"  TRACEABILITY SCORE : {snapshot.get('traceability_score', 0):.1f}/100")
        logger.info(f"  COVERAGE SCORE     : {snapshot.get('coverage_score', 0):.0%}")
        logger.info(f"  SOURCE CONFIDENCE  : {snapshot.get('source_confidence', 0):.3f}")
        # TGI / ICPI desde Gold Master
        if icpi.get("global_pct") is not None:
            logger.info(f"  ICPI GLOBAL        : {icpi['global_pct']:.2f}% → {icpi.get('clasificacion', '?')}")
        if tgi.get("score") is not None:
            logger.info(f"  TGI SCORE          : {tgi['score']:.4f}")
        # SAT
        if sat.get("total_evaluadas", 0) > 0:
            logger.info(
                f"  SAT RIESGO         : {sat.get('riesgo_ponderado', 0):.3f} → "
                f"{sat.get('clasif_riesgo', '?')} | "
                f"Activas: {sat.get('total_activas', 0)}/{sat.get('total_evaluadas', 0)}"
            )
            if sat.get("activas"):
                logger.warning(f"  SAT ALERTAS        : {sat['activas']}")
        logger.info(f"  MISSING DIMENSIONS : {snapshot.get('missing_dimensions', [])}")
        logger.info(f"  VALIDATION         : {snapshot['_pipeline'].get('validation', {}).get('status', '?')}")
        logger.info("─" * 60)
