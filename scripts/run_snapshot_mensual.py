#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/run_snapshot_mensual.py — QUIRA Intelligence
Lanzador automático del ciclo mensual.

Calcula automáticamente el mes de corte (mes anterior al actual)
y ejecuta ejecutar_ciclo_mensual.py con los parámetros correctos.

Uso:
  # Ejecución normal (scheduled task — día 26 de cada mes)
  python scripts/run_snapshot_mensual.py

  # Dry-run para testing
  python scripts/run_snapshot_mensual.py --dry-run

  # Override manual
  python scripts/run_snapshot_mensual.py --mes 4 --año 2026

Convención: correr el día 26 del mes siguiente al período a capturar.
  Ejemplo: 26 Junio → captura datos de Mayo (mes 5)

Dylus Lab © 2026 — Sprint Observabilidad Longitudinal
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

_RAIZ = Path(__file__).parent.parent
MUNICIPIO = "130801"


def calcular_periodo_corte(año_override=None, mes_override=None):
    """Calcula el período de corte: mes anterior al actual."""
    hoy = datetime.now()
    if año_override and mes_override:
        return año_override, mes_override
    # Mes anterior
    if hoy.month == 1:
        return hoy.year - 1, 12
    return hoy.year, hoy.month - 1


def main():
    parser = argparse.ArgumentParser(
        description="Lanzador automático del ciclo mensual QUIRA"
    )
    parser.add_argument("--año",     type=int, default=None, help="Año override")
    parser.add_argument("--mes",     type=int, default=None, help="Mes override")
    parser.add_argument("--dry-run", action="store_true",    help="No persistir en Supabase")
    args = parser.parse_args()

    año, mes = calcular_periodo_corte(args.año, args.mes)
    print(f"[run_snapshot_mensual] Período de corte: {año}-{mes:02d}")
    print(f"[run_snapshot_mensual] Municipio: {MUNICIPIO}")
    print(f"[run_snapshot_mensual] Dry-run: {args.dry_run}")
    print(f"[run_snapshot_mensual] Iniciando ciclo...")

    cmd = [
        sys.executable,
        str(_RAIZ / "scripts" / "ejecutar_ciclo_mensual.py"),
        "--municipio", MUNICIPIO,
        "--año",       str(año),
        "--mes",       str(mes),
    ]
    if args.dry_run:
        cmd.append("--dry-run")

    result = subprocess.run(cmd, cwd=str(_RAIZ))
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
