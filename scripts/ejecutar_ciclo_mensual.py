#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/ejecutar_ciclo_mensual.py — QUIRA Intelligence · Sprint 3 Semana 4
Orquestador del Ciclo Mensual Automatizado.

Ejecuta la secuencia completa del ciclo operacional QUIRA:
  1. Validar Gold Master (integridad canónica)
  2. Respaldar Gold Master con firma SHA-256
  3. Ejecutar pipeline de snapshot (11 pasos)
  4. Verificar resultado del snapshot
  5. Emitir reporte de ciclo en JSON

Uso:
  # Ciclo completo — municipio canónico Montecristi
  python scripts/ejecutar_ciclo_mensual.py

  # Municipio específico
  python scripts/ejecutar_ciclo_mensual.py --municipio 130901

  # Año/mes específico
  python scripts/ejecutar_ciclo_mensual.py --municipio 130801 --año 2026 --mes 5

  # Solo validar Gold Master (sin ejecutar pipeline)
  python scripts/ejecutar_ciclo_mensual.py --solo-validar-gm

  # Solo respaldar Gold Master
  python scripts/ejecutar_ciclo_mensual.py --solo-respaldar-gm

  # Modo prueba (no persiste en Supabase)
  python scripts/ejecutar_ciclo_mensual.py --dry-run

Ciclo mensual completo: ver docs/MONTHLY_CYCLE.md
Arquitectura: ver docs/ARQUITECTURA_CANONICA.md

Dylus Lab © 2026 — QUIRA Intelligence
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# ── Raíz del proyecto en sys.path ─────────────────────────────────────────────
_RAIZ = Path(__file__).parent.parent
sys.path.insert(0, str(_RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from utils.logger import get_logger

logger = get_logger("ciclo_mensual")

# ── Constantes ─────────────────────────────────────────────────────────────────
MUNICIPIO_CANONICO = "130801"  # Montecristi
RUTA_REPORTES      = _RAIZ / "data" / "reportes_ciclo"


# ══════════════════════════════════════════════════════════════════════════════
# Pasos del ciclo
# ══════════════════════════════════════════════════════════════════════════════

def paso_validar_gold_master() -> dict:
    """Paso 1: Valida integridad canónica del Gold Master v6.0."""
    logger.info("PASO 1 — Validando Gold Master...")
    try:
        from app.services.gold_master_governance import validar_gold_master
        resultados = validar_gold_master()
        errores  = [r for r in resultados if r.es_error()]
        alertas  = [r for r in resultados if r.es_alerta()]
        estado   = "ERROR" if errores else ("ALERTA" if alertas else "OK")
        resumen  = {
            "estado":        estado,
            "total_reglas":  len(resultados),
            "errores":       len(errores),
            "alertas":       len(alertas),
            "detalle_errores": [f"{r.regla}: {r.detalle}" for r in errores],
            "detalle_alertas": [f"{r.regla}: {r.detalle}" for r in alertas],
        }
        if errores:
            logger.error(f"  Gold Master con {len(errores)} ERROR(es) críticos:")
            for r in errores:
                logger.error(f"    ✗ [{r.categoria}] {r.regla}: {r.detalle}")
        elif alertas:
            logger.warning(f"  Gold Master OK con {len(alertas)} alerta(s)")
        else:
            logger.info(f"  Gold Master validado: {len(resultados)} reglas — 0 errores, 0 alertas ✓")
        return resumen
    except Exception as exc:
        logger.error(f"  Error validando Gold Master: {exc}")
        return {"estado": "ERROR", "error": str(exc)}


def paso_respaldar_gold_master() -> dict:
    """Paso 2: Crea respaldo firmado SHA-256 del Gold Master."""
    logger.info("PASO 2 — Respaldando Gold Master (SHA-256)...")
    try:
        from app.services.gold_master_governance import respaldar_gold_master
        resultado = respaldar_gold_master(destino=str(_RAIZ / "data" / "backups"))
        if resultado["estado"] == "ok":
            logger.info(
                f"  Respaldo creado: {Path(resultado['ruta_respaldo']).name} "
                f"({resultado['tamano_bytes']:,} bytes) — SHA256: {resultado['sha256'][:16]}..."
            )
        else:
            logger.warning(f"  Respaldo no completado: {resultado.get('error')}")
        return resultado
    except Exception as exc:
        logger.error(f"  Error al respaldar: {exc}")
        return {"estado": "error", "error": str(exc)}


def paso_ejecutar_pipeline(municipio_code: str, año: int, mes: int, dry_run: bool) -> dict:
    """Paso 3: Ejecuta el Snapshot Pipeline completo (11 pasos)."""
    logger.info(f"PASO 3 — Ejecutando pipeline: {municipio_code} · {año}-{mes:02d} (dry_run={dry_run})...")
    try:
        from app.pipelines.snapshot_pipeline import SnapshotPipeline
        pipeline = SnapshotPipeline(
            municipio_code=municipio_code,
            year=año,
            # El pipeline calcula internamente el mes activo
        )
        resultado = pipeline.run(dry_run=dry_run)
        # pipeline.run() devuelve el snapshot directamente (no tiene "status" de nivel superior)
        estado_snap = "ok" if resultado.get("_pipeline") else resultado.get("status", "error")
        icpi        = resultado.get("icpi", {}).get("global_pct", "—")
        sat_activas = resultado.get("sat", {}).get("total_activas", "—")
        logger.info(f"  Pipeline completado → estado={estado_snap} · ICPI={icpi}% · SAT activas={sat_activas}")
        return resultado
    except Exception as exc:
        logger.error(f"  Error en pipeline: {exc}")
        return {"status": "error", "error": str(exc)}


def paso_verificar_snapshot(resultado_pipeline: dict) -> dict:
    """Paso 4: Verifica que el snapshot producido cumple criterios de calidad mínimos.

    Nota: pipeline.run() devuelve el snapshot dict directamente (no anidado bajo 'snapshot').
    Los metadatos del pipeline viven en resultado_pipeline.get("_pipeline", {}).
    """
    logger.info("PASO 4 — Verificando snapshot...")
    # pipeline.run() devuelve el snapshot directamente — no usar .get("snapshot", {})
    snapshot = resultado_pipeline
    verificaciones = []
    aprobado = True

    def verificar(nombre: str, condicion: bool, detalle: str):
        nonlocal aprobado
        estado = "OK" if condicion else "FALLA"
        if not condicion:
            aprobado = False
        verificaciones.append({"nombre": nombre, "estado": estado, "detalle": detalle})
        nivel = logger.info if condicion else logger.warning
        simbolo = "✓" if condicion else "✗"
        nivel(f"  {simbolo} {nombre}: {detalle}")

    # Verificaciones canónicas
    icpi = snapshot.get("icpi", {}).get("global_pct", 0)
    verificar("icpi_presente", icpi > 0, f"ICPI={icpi}%")
    verificar("icpi_en_rango", 0 <= icpi <= 100, f"ICPI={icpi}% — debe estar en [0,100]")

    tgi = snapshot.get("tgi", {}).get("score", 0)
    verificar("tgi_presente", tgi > 0, f"TGI={tgi}%")

    # El snapshot usa "gad.codigo" para el municipio
    municipio = snapshot.get("gad", {}).get("codigo", "")
    verificar("municipio_code_presente", bool(municipio), f"código={municipio}")

    # El período vive en _meta.fecha_corte (YYYY-MM-DD) o _meta.year como fallback
    meta_snap = snapshot.get("_meta", {})
    periodo   = meta_snap.get("fecha_corte", "") or str(meta_snap.get("year", ""))
    verificar("periodo_presente", bool(periodo), f"período={periodo}")

    # El resultado de guardado vive en _pipeline.save_result (dry_run → "skipped")
    pipeline_meta  = resultado_pipeline.get("_pipeline", {})
    save_result    = pipeline_meta.get("save_result", {})
    estado_guardado = save_result.get("status", "no_ejecutado")
    verificar(
        "persistencia",
        estado_guardado in ("ok", "skipped"),
        f"guardado={estado_guardado}",
    )

    return {
        "aprobado":       aprobado,
        "verificaciones": verificaciones,
        "total_ok":       sum(1 for v in verificaciones if v["estado"] == "OK"),
        "total_falla":    sum(1 for v in verificaciones if v["estado"] == "FALLA"),
    }


def emitir_reporte_ciclo(
    municipio_code: str,
    año: int,
    mes: int,
    resultados: dict,
) -> Path:
    """Paso 5: Emite reporte JSON del ciclo completo."""
    logger.info("PASO 5 — Emitiendo reporte de ciclo...")
    RUTA_REPORTES.mkdir(parents=True, exist_ok=True)

    nombre = f"CICLO_{año}{mes:02d}_{municipio_code}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    ruta   = RUTA_REPORTES / nombre

    reporte = {
        "_meta": {
            "generado_en":    datetime.now().isoformat(),
            "municipio_code": municipio_code,
            "periodo":        f"{año}-{mes:02d}",
            "script":         "scripts/ejecutar_ciclo_mensual.py",
            "quira_version":  "v6.0",
        },
        "pasos": resultados,
        "estado_global": _calcular_estado_global(resultados),
    }

    ruta.write_text(json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  Reporte guardado: {ruta}")
    return ruta


def _calcular_estado_global(resultados: dict) -> str:
    """Determina el estado global del ciclo a partir de los resultados de cada paso."""
    errores = []

    gm_val = resultados.get("validacion_gm", {})
    if gm_val.get("estado") == "ERROR":
        errores.append("Gold Master con errores críticos")

    gm_res = resultados.get("respaldo_gm", {})
    if gm_res.get("estado") == "error":
        errores.append("Respaldo Gold Master fallido")

    pip = resultados.get("pipeline", {})
    # pipeline.run() devuelve el snapshot directamente (sin "status" de nivel superior).
    # Un pipeline exitoso tiene "_pipeline" con run_id.
    # Un pipeline fallido por excepción devuelve {"status": "error", "error": "..."}.
    pipeline_completo = pip.get("_pipeline") is not None and pip.get("status") != "error"
    if not pipeline_completo:
        errores.append(f"Pipeline no completó (status={pip.get('status', 'sin respuesta')})")

    snap_verif = resultados.get("verificacion_snapshot", {})
    if not snap_verif.get("aprobado", False):
        errores.append(f"Snapshot no aprueba verificación ({snap_verif.get('total_falla')} fallas)")

    if errores:
        logger.warning(f"  Estado global: ALERTA — {'; '.join(errores)}")
        return f"ALERTA: {'; '.join(errores)}"

    logger.info("  Estado global: OK — Ciclo completado exitosamente ✓")
    return "OK"


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="QUIRA Intelligence — Ejecutor del Ciclo Mensual Automatizado",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/ejecutar_ciclo_mensual.py
  python scripts/ejecutar_ciclo_mensual.py --municipio 130901 --año 2026 --mes 5
  python scripts/ejecutar_ciclo_mensual.py --solo-validar-gm
  python scripts/ejecutar_ciclo_mensual.py --dry-run
        """,
    )
    parser.add_argument(
        "--municipio", default=MUNICIPIO_CANONICO,
        help=f"Código del municipio (por defecto: {MUNICIPIO_CANONICO} — Montecristi)",
    )
    parser.add_argument(
        "--año", type=int, default=datetime.now().year,
        help="Año del ciclo (por defecto: año actual)",
    )
    parser.add_argument(
        "--mes", type=int, default=datetime.now().month,
        help="Mes del ciclo (por defecto: mes actual)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Ejecuta el pipeline sin persistir datos en Supabase",
    )
    parser.add_argument(
        "--solo-validar-gm", action="store_true",
        help="Solo valida el Gold Master (no ejecuta el pipeline completo)",
    )
    parser.add_argument(
        "--solo-respaldar-gm", action="store_true",
        help="Solo respalda el Gold Master con SHA-256 (no ejecuta el pipeline)",
    )
    return parser


def main() -> int:
    parser = construir_parser()
    args   = parser.parse_args()

    inicio = datetime.now()
    logger.info("=" * 60)
    logger.info("QUIRA Intelligence — Ciclo Mensual Automatizado")
    logger.info(f"Municipio: {args.municipio} · Período: {args.año}-{args.mes:02d}")
    logger.info(f"Inicio: {inicio.isoformat()}")
    logger.info("=" * 60)

    resultados: dict = {}

    # ── Modo: solo validar Gold Master ────────────────────────────────────────
    if args.solo_validar_gm:
        resultados["validacion_gm"] = paso_validar_gold_master()
        estado = resultados["validacion_gm"]["estado"]
        logger.info(f"\nValidación completada → {estado}")
        return 0 if estado != "ERROR" else 1

    # ── Modo: solo respaldar Gold Master ─────────────────────────────────────
    if args.solo_respaldar_gm:
        resultados["respaldo_gm"] = paso_respaldar_gold_master()
        estado = resultados["respaldo_gm"]["estado"]
        logger.info(f"\nRespaldo completado → {estado}")
        return 0 if estado == "ok" else 1

    # ── Ciclo completo ────────────────────────────────────────────────────────
    resultados["validacion_gm"] = paso_validar_gold_master()

    # Si el Gold Master tiene errores críticos, detener el ciclo
    if resultados["validacion_gm"].get("estado") == "ERROR":
        logger.error("\n⚠ CICLO DETENIDO — Gold Master con errores críticos.")
        logger.error("  Corregir el Gold Master antes de ejecutar el pipeline.")
        return 1

    resultados["respaldo_gm"] = paso_respaldar_gold_master()

    resultados["pipeline"] = paso_ejecutar_pipeline(
        municipio_code=args.municipio,
        año=args.año,
        mes=args.mes,
        dry_run=args.dry_run,
    )

    resultados["verificacion_snapshot"] = paso_verificar_snapshot(resultados["pipeline"])

    ruta_reporte = emitir_reporte_ciclo(
        municipio_code=args.municipio,
        año=args.año,
        mes=args.mes,
        resultados=resultados,
    )

    fin = datetime.now()
    duracion = (fin - inicio).total_seconds()
    estado_global = _calcular_estado_global(resultados)

    logger.info("=" * 60)
    logger.info(f"Ciclo finalizado en {duracion:.1f}s — Estado: {estado_global}")
    logger.info(f"Reporte: {ruta_reporte}")
    logger.info("=" * 60)

    return 0 if estado_global == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
