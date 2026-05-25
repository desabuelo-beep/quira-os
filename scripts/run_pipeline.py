#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/run_pipeline.py — QUIRA OS · Sprint 1
Entry-point CLI para ejecutar el Snapshot Pipeline Territorial.

Uso:
  # Municipio canónico (Montecristi)
  python scripts/run_pipeline.py

  # Por RUC
  python scripts/run_pipeline.py --ruc 1360000980001

  # Por código
  python scripts/run_pipeline.py --code 130901

  # Modo dry-run (sin persistir)
  python scripts/run_pipeline.py --ruc 1360000980001 --dry-run

  # Año específico
  python scripts/run_pipeline.py --ruc 1360000430001 --year 2025

Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="QUIRA OS — Snapshot Pipeline Territorial",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/run_pipeline.py                              # Montecristi
  python scripts/run_pipeline.py --ruc 1360000980001         # Manta
  python scripts/run_pipeline.py --code 130601 --dry-run     # Jipijapa (dry)
        """,
    )
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--ruc",  type=str, help="RUC del municipio (13 dígitos)")
    grp.add_argument("--code", type=str, help="municipio_code (6 dígitos)")

    parser.add_argument("--year",    type=int, default=None, help="Año de análisis")
    parser.add_argument("--dry-run", action="store_true",    help="Ejecutar sin persistir")
    parser.add_argument("--json",    action="store_true",    help="Imprimir snapshot JSON al final")
    parser.add_argument("--verbose", action="store_true",    help="Logging DEBUG")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    from app.pipelines.snapshot_pipeline import SnapshotPipeline

    pipeline = SnapshotPipeline(
        ruc=args.ruc,
        municipio_code=args.code,
        year=args.year,
    )

    result = pipeline.run(dry_run=args.dry_run)

    if args.json:
        # Imprimir snapshot completo (excluir _pipeline interno)
        output = {k: v for k, v in result.items() if k != "_pipeline"}
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\nPipeline completado — TRACEABILITY SCORE: {result.get('traceability_score', 0):.1f}/100")
        if result.get("missing_dimensions"):
            print(f"Dimensiones sin cobertura: {result['missing_dimensions']}")
        save = result.get("_pipeline", {}).get("save_result", {})
        if save.get("saved_files"):
            print(f"Snapshot guardado: {save['saved_files'][0]}")


if __name__ == "__main__":
    main()
