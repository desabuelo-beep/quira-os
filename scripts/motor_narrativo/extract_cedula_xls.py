# -*- coding: utf-8 -*-
"""
Motor Narrativo — lector de la CÉDULA PRESUPUESTARIA DE GASTOS (documento oficial).
Dylus Lab © 2026 · doctrina PCD-MN01 §18 (capa R4 · cifras financieras).

Verifica DOCUMENTALMENTE las afirmaciones de ejecución presupuestaria del discurso
contra la cédula oficial de gastos. NO recalcula ninguna métrica del Gold Master:
el canon NO produce la ejecución presupuestaria GENERAL (su `PSG_EJECUCION` es otra
sub-métrica). La ejecución general vive en el documento fuente (la cédula), y de ahí
se lee — no se inventa (Regla 1/3/4). Solo lectura, cifras públicas de presupuesto.

Estructura de la cédula: filas jerárquicas (Programa/Subprograma/Proyecto/Actividad/
Partida). La fila 'Programa' del código 01 = total del GAD. Columnas: Codigo ·
Estructura · Asignacion Inicial · Reformas · Codificado · Compromiso... · Devengado.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

_BASE = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi"
             r"\Cedulas Presupuestarias 2023-2026")
_ARCH = {
    "2023": r"Presupuestos 2023\GAD Montecristi_Diciembre_Cedula_Presupuestaria_de_Gastos_ 2023.xls",
    "2024": r"Presupuestos 2024\GAD Montecristi_Cedula_Presupuestaria_de_Gastos_ 2024.xls",
}


def _num(v) -> float | None:
    try:
        return float(str(v).replace(",", "").replace("$", "").strip())
    except (ValueError, AttributeError):
        return None


@lru_cache(maxsize=8)
def ejecucion_gastos(año: str) -> dict | None:
    """Total de gastos del año desde la cédula oficial: codificado, devengado, ratio.
    None si no existe el archivo. El ratio = devengado/codificado = ejecución de egresos."""
    rel = _ARCH.get(año)
    if not rel or not (_BASE / rel).exists():
        return None
    df = pd.read_excel(_BASE / rel, header=None, dtype=str)
    # localizar la fila de encabezado (contiene 'Codificado' y 'Devengado')
    hdr = None
    for i in range(min(15, len(df))):
        fila = " ".join(str(x) for x in df.iloc[i].tolist())
        if "Codificado" in fila and "Devengado" in fila:
            hdr = i
            break
    if hdr is None:
        return None
    cols = [str(x).strip() for x in df.iloc[hdr].tolist()]
    ci_cod = next((j for j, c in enumerate(cols) if c.lower().startswith("codificado")), None)
    ci_dev = next((j for j, c in enumerate(cols) if c.lower().startswith("devengado")), None)
    ci_est = next((j for j, c in enumerate(cols) if "estructura" in c.lower()), 1)
    if ci_cod is None or ci_dev is None:
        return None
    # fila total = primera 'Programa'
    for i in range(hdr + 1, len(df)):
        if str(df.iat[i, ci_est]).strip().lower() == "programa":
            cod, dev = _num(df.iat[i, ci_cod]), _num(df.iat[i, ci_dev])
            if cod and dev and cod > 0:
                return {"codificado": cod, "devengado": dev, "ratio": dev / cod, "año": año}
    return None


if __name__ == "__main__":
    import sys
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    e = ejecucion_gastos(año)
    if e:
        print(f"CÉDULA GASTOS {año}: codificado ${e['codificado']:,.2f} · "
              f"devengado ${e['devengado']:,.2f} · ejecución {e['ratio'] * 100:.2f}%")
    else:
        print(f"CÉDULA GASTOS {año}: no disponible")
