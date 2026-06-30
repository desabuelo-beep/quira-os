# -*- coding: utf-8 -*-
"""
scripts/recalc_com.py — QUIRA OS · Recálculo del Canon en Windows (win32com)
═══════════════════════════════════════════════════════════════════════════
openpyxl escribe inputs pero DESTRUYE el cache de fórmulas (data_only=True → None).
Excel debe recalcular para restaurar el cache ANTES de leer derivados o promover.

Usa DispatchEx (instancia DEDICADA · NO se engancha al Excel abierto de Javo).
NO toca fórmulas — solo fuerza CalculateFullRebuild + Save sobre la COPIA WORK.
La fórmula canónica (H12!B33 ICPI) es INMUTABLE: este script jamás la modifica,
solo pide a Excel que la recompute con los inputs nuevos.

Uso:  python scripts/recalc_com.py "<ruta xlsx>"
Dylus Lab © 2026
"""
import sys
from pathlib import Path

XL_AUTOMATIC = -4105  # xlCalculationAutomatic


def recalc(path: str) -> int:
    p = Path(path)
    if not p.exists():
        print(f"[ERR] no existe: {p}")
        return 1

    import win32com.client as win32  # pywin32

    app = win32.DispatchEx("Excel.Application")  # instancia nueva y aislada
    app.Visible = False
    app.DisplayAlerts = False
    try:
        wb = app.Workbooks.Open(str(p.absolute()))
        app.Calculation = XL_AUTOMATIC
        try:
            app.CalculateFullRebuild()
        except Exception:
            app.CalculateFull()
        wb.Save()
        wb.Close(SaveChanges=True)
        print(f"[OK] recalculado y guardado: {p.name}")
        return 0
    finally:
        app.Quit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/recalc_com.py \"<ruta xlsx>\"")
        raise SystemExit(1)
    raise SystemExit(recalc(sys.argv[1]))
