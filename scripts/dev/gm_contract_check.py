# -*- coding: utf-8 -*-
"""
gm_contract_check.py — verifica que el CONTRATO (H73_OUTPUT_API) del vivo corregido
entregue el ICPI 27.46% al pipeline. SOLO LECTURA · Sprint D.1 Paso 1 (pie de plomo).
Dylus Lab © 2026
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

from app.connectors.gold_master import fetch_gold_master_data

r = fetch_gold_master_data()
print(f"status={r['status']} · reliability={r['reliability']} · claves_leidas={r['sheet_rows']}")
if r.get("error"): print("error:", r["error"])
d = r.get("data", {})
print(f"\nCONTRATO H73 — {len(d)} claves REALES (lo que fluye a QUIRA):")
for k in sorted(d.keys()):
    v = d[k]
    flag = "  <== ICPI" if "ICPI" in k.upper() or "27.4" in str(v) or "0.274" in str(v) else ""
    print(f"  {k:30s} = {v}{flag}")
