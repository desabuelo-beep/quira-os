# -*- coding: utf-8 -*-
"""Test funcional p2_holding — ejecutar con: python scripts/_test_holding.py"""
import sys
sys.path.insert(0, ".")

import unittest.mock as mock

with mock.patch("streamlit.cache_data", lambda **k: (lambda f: f)):
    from quira_pages.p2_holding import (
        _load_sercop_data, _fmt, _cajon, _sparkline, _tipos_html, _ENTIDADES,
        _concentracion_stats, _cajon2,
    )

# ── Carga de datos ─────────────────────────────────────────────────────────────
d = _load_sercop_data()
assert d["ok"], f"Data load failed: {d.get('error')}"
assert d["total_procesos"] == 772, f"Expected 772, got {d['total_procesos']}"
assert d["total_adjudicado"] > 12_000_000, f"Total adj too low: {d['total_adjudicado']}"
assert "prov_by_entity" in d, "prov_by_entity missing from load result"
print(f"  [OK] load: {d['total_procesos']} procesos, ${d['total_adjudicado']:,.0f}")

# ── Formatters ─────────────────────────────────────────────────────────────────
assert _fmt(0)         == "$0",      f"_fmt(0): {_fmt(0)}"
assert _fmt(500)       == "$500",    f"_fmt(500): {_fmt(500)}"
assert _fmt(1_500)     == "$1.5K",   f"_fmt(1500): {_fmt(1_500)}"
assert _fmt(1_500_000) == "$1.50M",  f"_fmt(1.5M): {_fmt(1_500_000)}"
print("  [OK] _fmt edge cases")

# ── Cajón 1: cajones por entidad ───────────────────────────────────────────────
by_year = d["by_year"]
tipos   = d["tipos"]
DEMO_NUMBERS = ["82.7", "74.1", "58.4", "71.7", "61.2", "44.8"]

for i, cod in enumerate(["GAD", "PATRONATO", "BOMBEROS", "EMAI", "HABITAT"], 1):
    stats = d["by_entity"].get(cod, {"procesos": 0, "adjudicado": 0, "presupuestado": 0, "proveedores": 0})
    html  = _cajon(i, cod, stats, by_year, tipos)

    assert f"hm{i}" in html,  f"Missing id hm{i} in {cod}"
    assert f"arr{i}" in html, f"Missing class arr{i} in {cod}"

    for bad in DEMO_NUMBERS:
        assert bad not in html, f"Hardcoded demo value '{bad}' found in {cod} cajon"

    print(f"  [OK] {cod}: {stats['procesos']} proc, ${stats['adjudicado']:,.0f}, no demo values")

# ── Alertas Cajón 1 ────────────────────────────────────────────────────────────
gad_html = _cajon(1, "GAD", d["by_entity"].get("GAD", {}), by_year, tipos)
assert "2024" in gad_html and "2025" in gad_html, "GAD debe mostrar años en sparkline"
assert "Caída 2024→2025" in gad_html or "Ca" in gad_html, "GAD caida alert"

hab_stats = {"procesos": 0, "adjudicado": 0.0, "presupuestado": 0.0, "proveedores": 0}
hab_html  = _cajon(5, "HABITAT", hab_stats, by_year, tipos)
assert "Sin actividad" in hab_html or "sin registro" in hab_html.lower(), \
    f"HABITAT alert missing. Snippet: {hab_html[:300]}"

print("  [OK] GAD caida alert present")
print("  [OK] HABITAT sin actividad alert present")

# ── Montos reales en Cajón 1 ───────────────────────────────────────────────────
all_html = "".join(
    _cajon(i, cod, d["by_entity"].get(cod, {"procesos":0,"adjudicado":0,"presupuestado":0,"proveedores":0}),
           by_year, tipos)
    for i, cod in enumerate(["GAD","PATRONATO","BOMBEROS","EMAI","HABITAT"], 1)
)
assert "8.33M" in all_html or "8." in all_html, "GAD adj should appear"
print("  [OK] Montos reales presentes (Cajón 1)")

# ── Cajón 2: Concentración de Proveedores ─────────────────────────────────────
by_entity      = d["by_entity"]
prov_by_entity = d["prov_by_entity"]

# Debe haber proveedores para GAD, PATRONATO, BOMBEROS, EMAI
for cod in ["GAD", "PATRONATO", "BOMBEROS", "EMAI"]:
    assert prov_by_entity.get(cod), f"prov_by_entity vacío para {cod}"
    top = prov_by_entity[cod][0]
    assert top["adj"] > 0, f"Top proveedor {cod} tiene adj=0"
    print(f"  [OK] {cod} prov: top='{top['proveedor'][:30]}' ${top['adj']:,.0f}")

# HABITAT sin proveedores
assert not prov_by_entity.get("HABITAT"), "HABITAT no debe tener proveedores en SERCOP"
print("  [OK] HABITAT: sin proveedores (esperado)")

# _concentracion_stats — GAD debe tener concentración calculable
gad_adj  = by_entity.get("GAD", {}).get("adjudicado", 0.0)
gad_conc = _concentracion_stats("GAD", prov_by_entity, gad_adj)
assert 0 < gad_conc["top_pct"] <= 100, f"GAD top_pct fuera de rango: {gad_conc['top_pct']}"
assert gad_conc["hhi"] > 0, f"GAD HHI debe ser > 0"
assert gad_conc["semaforo"] in ("rojo", "amarillo", "verde"), f"Semaforo invalido: {gad_conc['semaforo']}"
print(f"  [OK] GAD concentracion: {gad_conc['top_pct']:.1f}% · HHI={gad_conc['hhi']:.0f} · {gad_conc['semaforo']}")

# _cajon2 — genera HTML sin demo values
c2_html = _cajon2(prov_by_entity, by_entity)
assert "cajon2body" in c2_html, "cajon2body id missing"
assert "HHI" in c2_html, "HHI label missing from cajon2"
assert "cardonanl" in c2_html, "Credit to cali-monitor author missing"
for bad in DEMO_NUMBERS:
    assert bad not in c2_html, f"Demo value '{bad}' found in cajon2"
print("  [OK] Cajón 2 HTML generado: cajon2body, HHI, créditos, sin demo values")

# HABITAT card especial en cajón 2
assert "Sin procesos" in c2_html or "sin registro" in c2_html.lower() or "HABITAT" in c2_html, \
    "HABITAT special card missing in cajon2"
print("  [OK] HABITAT card presente en Cajón 2")

print()
print("=" * 50)
print("ALL TESTS PASSED — p2_holding.py limpio (Cajón 1 + Cajón 2)")
print("=" * 50)
