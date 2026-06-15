# -*- coding: utf-8 -*-
"""
gm_2025_probe.py — lee la serie mensual 2025 del holding desde Supabase (monthly_kpis).
SOLO LECTURA (SELECT). Determinista. Para construir la curva de pacing real de Montecristi.
Dylus Lab © 2026
"""
from __future__ import annotations
import sys, os
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)

# Parchear st.secrets para correr fuera de Streamlit (patrón bulk_ingest_2025)
import toml
_secrets_path = os.path.join(REPO, ".streamlit", "secrets.toml")
_raw = toml.load(_secrets_path)
import streamlit as st
class _Fake:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k): return _raw[k]
st.secrets = _Fake()

from sentinel.db_config import get_connection

def main() -> int:
    conn = get_connection()
    print(f"MODE = {conn.mode}")
    c = conn.cursor()

    # años disponibles
    yrs = c.execute("SELECT period_year AS y, COUNT(*) AS n FROM monthly_kpis GROUP BY period_year ORDER BY period_year").fetchall()
    print("AÑOS en monthly_kpis:", [(r["y"], r["n"]) for r in yrs])

    # serie mensual 2025
    rows = c.execute(
        "SELECT entidad, period_month, codificado_inv, devengado_inv, "
        "codificado_total, devengado_total, ti_mensual_pct, ti_acumulado_pct "
        "FROM monthly_kpis WHERE period_year=? ORDER BY entidad, period_month",
        (2025,),
    ).fetchall()

    print(f"\nFILAS 2025 = {len(rows)}")
    print(f"{'entidad':12s} {'mes':>3} {'cod_inv':>14} {'dev_inv':>14} {'ti_mens%':>9} {'ti_acum%':>9}")
    print("-" * 70)
    for r in rows:
        ci = r["codificado_inv"]; di = r["devengado_inv"]
        tm = r["ti_mensual_pct"]; ta = r["ti_acumulado_pct"]
        print(f"{str(r['entidad'])[:12]:12s} {r['period_month']:>3} "
              f"{(ci if ci is not None else 0):>14,.0f} {(di if di is not None else 0):>14,.0f} "
              f"{(tm if tm is not None else 0):>9.2f} {(ta if ta is not None else 0):>9.2f}")

    # también 2026 para comparar
    rows26 = c.execute(
        "SELECT entidad, period_month, devengado_inv, ti_acumulado_pct "
        "FROM monthly_kpis WHERE period_year=? ORDER BY entidad, period_month",
        (2026,),
    ).fetchall()
    print(f"\n2026 (referencia) FILAS = {len(rows26)}")
    for r in rows26:
        print(f"  {str(r['entidad'])[:12]:12s} mes {r['period_month']:>2}  dev_inv={r['devengado_inv']}  ti_acum%={r['ti_acumulado_pct']}")

    conn.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
