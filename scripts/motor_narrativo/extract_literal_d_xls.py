# -*- coding: utf-8 -*-
"""
Motor Narrativo — lector del LITERAL D (servicios institucionales · LOTAIP Numeral 5-22).
Dylus Lab © 2026 · doctrina PCD-MN01 §20 (capa R6 · coberturas de servicio).

Registro oficial de transparencia del patronato: por mes, cada servicio con su
"Número de personas que acceden". Verifica las coberturas del discurso (atenciones,
beneficiarios) contra el dato publicado. NO está en el canon ni en Supabase — se lee
directo del documento oficial (Regla 1/3/4 · solo lectura).

VENTANA HONESTA (aval Javo): 2024 solo sep–dic (4 meses) → cobertura `parcial`, NO se
extrapola al año. 2025 completo. La métrica del registro es "personas que acceden";
el discurso suele decir "atenciones" — se reporta el dato real, sin igualar métricas.
"""
from __future__ import annotations

import glob
import os
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd

_BASE = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi"
             r"\Literal D servicios institucionales\Patronato")


def _num(v) -> float | None:
    try:
        return float(re.sub(r"[^\d.]", "", str(v).replace(",", "")))
    except (ValueError, AttributeError):
        return None


@lru_cache(maxsize=8)
def servicios_patronato(año: str) -> dict | None:
    """Servicios del patronato del año con su cobertura sumada sobre los meses
    DISPONIBLES. Devuelve {servicios:{nombre:personas}, total, meses, año}. None si no hay."""
    folder = _BASE / año
    if not folder.exists():
        return None
    servicios: dict[str, float] = {}
    meses = 0
    for f in sorted(glob.glob(str(folder / "*.xlsx"))):
        try:
            df = pd.read_excel(f, header=0, dtype=str)
        except Exception:
            continue
        if df.empty:
            continue
        cols = list(df.columns)
        svc_col = cols[0]
        num_col = next((c for c in cols if re.search(r"personas que acceden|n[uú]mero de personas", str(c), re.I)), None)
        if num_col is None:
            continue
        meses += 1
        for _, row in df.iterrows():
            # sanea el nombre: quita el carácter de reemplazo (mojibake U+FFFD) y normaliza espacios
            svc = re.sub(r"\s+", " ", str(row[svc_col]).replace("�", "")).strip()
            n = _num(row[num_col])
            if svc and svc.lower() not in ("nan", "") and n:
                servicios[svc] = servicios.get(svc, 0.0) + n
    if not servicios:
        return None
    return {"servicios": servicios, "total": sum(servicios.values()), "meses": meses, "año": año}


if __name__ == "__main__":
    import sys
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    d = servicios_patronato(año)
    if d:
        print(f"LITERAL D patronato {año}: {len(d['servicios'])} servicios · {d['meses']} meses · "
              f"total {d['total']:,.0f} personas")
        top = sorted(d["servicios"].items(), key=lambda x: -x[1])[:8]
        for svc, n in top:
            print(f"  {n:>10,.0f}  {svc[:70]}")
    else:
        print(f"LITERAL D patronato {año}: no disponible")
