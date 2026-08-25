"""
app/agents/d01/motor.py — Lectura del motor (NO recálculo)
=========================================================================
Responsabilidad única: LEER las métricas de d01 del Gold Master.

REGLA 1 y 4 (inviolables): el IPE y la cobertura los calcula el Gold Master
(fórmula nativa H16b, que deriva de H12!B33 INMUTABLE). Este módulo NUNCA
recalcula — solo lee. Determinístico, sin IA.

HALLAZGO de la migración (2026-07-22): d01 calcula su IPE en H16b pero NO lo
expone en el contrato de salida H73 (fetch_gold_master_data solo trae 7
claves, ninguna de d01). Por eso aquí se lee H16b directamente. Exponer el
IPE en H73 sería una cirugía del Gold Master — se deja anotado como deuda,
NO se ejecuta en esta migración (Javo: "sin tocar el ICPI").
"""
from __future__ import annotations

import pathlib
from typing import Any

try:
    from config import DATOS_DIR as _DATOS
except Exception:                                        # noqa: BLE001
    import os as _os
    from pathlib import Path as _P
    _DATOS = _P(_os.environ.get("QUIRA_DATOS", "."))

_GM_DEFAULT = pathlib.Path(
    str(_DATOS / "SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx")
)
_HOJA = "H16b_IPE"
# Celdas verificadas 2026-07-22 (PCD-D01: el IPE real curado vive en B15, no en
# el proxy B6=0.84 que quedó como nota metodológica).
_CELDA_IPE = "B15"            # IPE_Ejecutado_2026_Real
_CELDA_COBERTURA = "B12"      # Cobertura_Metas_POA_2026
_CELDA_INV_VINCULADA = "B16"  # Inversion_Vinculada_Real_USD


def leer_metricas(gold_master_path: str | pathlib.Path | None = None) -> dict[str, Any]:
    """Lee (no calcula) IPE, cobertura e inversión vinculada de H16b."""
    path = pathlib.Path(gold_master_path) if gold_master_path else _GM_DEFAULT
    if not path.exists():
        return {"status": "failed", "error": f"Gold Master no encontrado: {path}"}

    import openpyxl
    wb = openpyxl.load_workbook(str(path), data_only=True, read_only=True)
    if _HOJA not in wb.sheetnames:
        return {"status": "failed", "error": f"Hoja {_HOJA} no existe"}
    ws = wb[_HOJA]
    return {
        "status": "ok",
        "fuente": f"{_HOJA} (leído, NO recalculado — Regla 1/4)",
        "naturaleza": "INMUTABLE",
        "ipe_ejecutado": ws[_CELDA_IPE].value,
        "cobertura_metas_poa": ws[_CELDA_COBERTURA].value,
        "inversion_vinculada_usd": ws[_CELDA_INV_VINCULADA].value,
    }
