# -*- coding: utf-8 -*-
"""
gm_2025_curve.py — curva de PACING real de Montecristi desde monthly_kpis 2025.
pacing(M) = devengado_inv_acumulado(M) / devengado_inv_anual.  SOLO LECTURA.
Construye el FactorTemporal basado en evidencia (no hipótesis nacional).
Dylus Lab © 2026
"""
from __future__ import annotations
import sys, os
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, REPO)
import toml
_raw = toml.load(os.path.join(REPO, ".streamlit", "secrets.toml"))
import streamlit as st
class _F:
    def get(self,k,d=None): return _raw.get(k,d)
    def __getitem__(self,k): return _raw[k]
st.secrets = _F()
from sentinel.db_config import get_connection

ENTS = ["BOMBEROS", "EMAI-EP", "PATRONATO"]   # GAD excluido: solo Q4 2025

def main() -> int:
    conn = get_connection(); c = conn.cursor()
    rows = c.execute(
        "SELECT entidad, period_month, MAX(devengado_inv) AS dev FROM monthly_kpis "
        "WHERE period_year=2025 AND devengado_inv IS NOT NULL GROUP BY entidad, period_month "
        "ORDER BY entidad, period_month", ()
    ).fetchall()
    conn.close()

    # dev acumulado por entidad/mes (dedup por MAX)
    series = {e: {} for e in ENTS}
    for r in rows:
        e = r["entidad"]
        if e in series:
            series[e][r["period_month"]] = float(r["dev"] or 0)

    # forzar monotonía (acumulado nunca baja) y normalizar por anual (mes 12 o máx)
    pacing = {}   # entidad -> {mes: fraccion}
    annual = {}
    for e in ENTS:
        s = series[e]
        meses = sorted(s.keys())
        run = 0.0; mono = {}
        for m in range(1, 13):
            if m in s: run = max(run, s[m])     # acumulado monótono
            mono[m] = run
        ann = mono[12] if mono[12] > 0 else max(mono.values())
        annual[e] = ann
        pacing[e] = {m: (mono[m] / ann if ann else 0.0) for m in range(1, 13)}

    print("PACING(M) = % del anual ejecutado al mes M (inversión, dev acumulado/anual)")
    print(f"{'mes':>3} | {'BOMBEROS':>9} {'EMAI-EP':>9} {'PATRON.':>9} | {'simple':>7} {'pond.':>7} | {'LINEAL':>7}")
    print("-"*72)
    for m in range(1, 13):
        vals = [pacing[e][m] for e in ENTS]
        simple = sum(vals)/len(vals)
        wtot = sum(annual[e] for e in ENTS)
        wavg = sum(pacing[e][m]*annual[e] for e in ENTS)/wtot if wtot else 0
        lineal = m/12
        star = "  <-- ABRIL (corte vivo 2026)" if m == 4 else ""
        print(f"{m:>3} | {pacing['BOMBEROS'][m]*100:>8.1f}% {pacing['EMAI-EP'][m]*100:>8.1f}% "
              f"{pacing['PATRONATO'][m]*100:>8.1f}% | {simple*100:>6.1f}% {wavg*100:>6.1f}% | {lineal*100:>6.1f}%{star}")

    # FactorTemporal en Abril (mes 4) + impacto en GAD Ti
    m = 4
    vals = [pacing[e][m] for e in ENTS]
    simple4 = sum(vals)/len(vals)
    wtot = sum(annual[e] for e in ENTS)
    wavg4 = sum(pacing[e][m]*annual[e] for e in ENTS)/wtot
    gad_raw = 0.0643   # GAD Ti_raw inversión abril 2026 (H07_S5!B20)
    print("\n=== FACTOR TEMPORAL ABRIL (mes 4) ===")
    print(f"  LINEAL (actual)      = {4/12:.4f}  -> GAD Ti_norm = {min(1,gad_raw/(4/12))*100:.2f}%")
    print(f"  pacing simple (3 adscritas) = {simple4:.4f}  -> GAD Ti_norm = {min(1,gad_raw/simple4)*100:.2f}%")
    print(f"  pacing ponderado            = {wavg4:.4f}  -> GAD Ti_norm = {min(1,gad_raw/wavg4)*100:.2f}%")
    print(f"  anual dev_inv: BOM={annual['BOMBEROS']:,.0f} EMAI={annual['EMAI-EP']:,.0f} PAT={annual['PATRONATO']:,.0f}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
