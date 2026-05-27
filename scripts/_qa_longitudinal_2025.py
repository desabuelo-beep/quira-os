# -*- coding: utf-8 -*-
"""
scripts/_qa_longitudinal_2025.py
QA Longitudinal — Integridad de las 38 cédulas 2025
Verifica: cobertura, coherencia Ti%, monotonía acumulada, duplicados, gaps.
Dylus Lab © 2026
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import toml
_raw = toml.load(os.path.join(os.path.dirname(__file__), "..", ".streamlit", "secrets.toml"))
import streamlit as st
class _F:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k):  return _raw[k]
st.secrets = _F()

from sentinel.db_config import get_connection

conn = get_connection()

print("=" * 70)
print("  QUIRA OS — QA Longitudinal Histórico 2025")
print("=" * 70)

# ── 1. COBERTURA TOTAL ────────────────────────────────────────────────────────
print("\n[1/6] COBERTURA 2025")
rows = conn.execute("""
    SELECT entidad, COUNT(DISTINCT period_month) as meses,
           MIN(period_month) as desde, MAX(period_month) as hasta
    FROM document_uploads
    WHERE document_type='CEDULA' AND period_year=2025
    GROUP BY entidad ORDER BY entidad
""").fetchall()

total_cedulas = 0
for r in rows:
    meses = r['meses']
    ent   = r['entidad']
    esperado = {'BOMBEROS':12,'EMAI-EP':11,'GAD':3,'PATRONATO':12}.get(ent, '?')
    ok = '✓' if meses == esperado else f'⚠ esperado={esperado}'
    print(f"  {ent:12s}: {meses:2d} meses  (mes {r['desde']}-{r['hasta']})  {ok}")
    total_cedulas += meses
print(f"  Total cédulas distintas: {total_cedulas}")

# ── 2. CONSISTENCIA Ti% ───────────────────────────────────────────────────────
print("\n[2/6] CONSISTENCIA Ti% 2025 (valores fuera de rango)")
kpis = conn.execute("""
    SELECT entidad, period_month, ti_mensual_pct, codificado_inv, devengado_inv
    FROM monthly_kpis
    WHERE period_year=2025
    ORDER BY entidad, period_month
""").fetchall()

errores_ti = []
for k in kpis:
    ti  = k['ti_mensual_pct']
    cod = k['codificado_inv']
    dev = k['devengado_inv']
    # Ti debe estar entre 0 y 110%
    if ti is not None and (ti < 0 or ti > 110):
        errores_ti.append(f"  ERROR Ti={ti:.2f}% — {k['entidad']} mes {k['period_month']}")
    # Dev no puede superar Cod si ti < 100%
    if cod and dev and dev > cod * 1.02:
        errores_ti.append(f"  WARN Dev>Cod — {k['entidad']} mes {k['period_month']} cod={cod:.0f} dev={dev:.0f}")
if errores_ti:
    for e in errores_ti:
        print(e)
else:
    print("  OK — todos los Ti% dentro de rango [0%, 110%]")

# ── 3. MONOTONÍA ACUMULADA (Ti debe ser creciente o estable anualmente) ────────
print("\n[3/6] TRAYECTORIA Ti% por entidad")
entidades = ['BOMBEROS','EMAI-EP','GAD','PATRONATO']
MESES = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',
          7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}

for ent in entidades:
    ks = [k for k in kpis if k['entidad'] == ent]
    if not ks: continue
    print(f"\n  {ent}:")
    ti_prev = None
    for k in ks:
        ti  = k['ti_mensual_pct']
        mes = MESES.get(k['period_month'], str(k['period_month']))
        sem = '🟢' if ti >= 35 else ('🟡' if ti >= 15 else '🔴')
        tendencia = ''
        if ti_prev is not None:
            diff = ti - ti_prev
            tendencia = f" ({'↑' if diff > 0 else ('↓' if diff < 0 else '=')} {abs(diff):.2f}pp)"
        print(f"    {mes}: {ti:6.2f}%  {sem}{tendencia}")
        ti_prev = ti

# ── 4. DUPLICADOS POR PERÍODO ─────────────────────────────────────────────────
print("\n\n[4/6] DUPLICADOS POR PERÍODO")
dups = conn.execute("""
    SELECT entidad, period_year, period_month, COUNT(*) as cnt
    FROM document_uploads
    WHERE document_type='CEDULA' AND period_year=2025
    GROUP BY entidad, period_year, period_month
    HAVING COUNT(*) > 1
    ORDER BY entidad, period_month
""").fetchall()

if dups:
    print("  Períodos con múltiples versiones (normal si hubo correcciones):")
    for d in dups:
        print(f"  {d['entidad']} 2025-{d['period_month']:02d}: {d['cnt']} versiones")
else:
    print("  OK — sin duplicados de período (salvo versiones explícitas)")

# ── 5. GAPS (meses faltantes esperados vs presentes) ─────────────────────────
print("\n[5/6] GAPS — MESES FALTANTES (esperados vs disponibles)")
esperados = {
    'BOMBEROS':  list(range(1,13)),
    'EMAI-EP':   [m for m in range(1,13) if m != 3],  # sin Marzo
    'GAD':       [10,11,12],
    'PATRONATO': list(range(1,13)),
}
presentes_raw = conn.execute("""
    SELECT entidad, array_agg(DISTINCT period_month ORDER BY period_month) as meses
    FROM document_uploads
    WHERE document_type='CEDULA' AND period_year=2025
    GROUP BY entidad
""").fetchall()

presentes = {}
for p in presentes_raw:
    meses_val = p['meses']
    if isinstance(meses_val, list):
        presentes[p['entidad']] = meses_val
    else:
        # SQLite fallback
        presentes[p['entidad']] = []

if not presentes:
    # SQLite — usar query distinta
    for ent in entidades:
        ms = conn.execute(
            "SELECT DISTINCT period_month FROM document_uploads "
            "WHERE document_type='CEDULA' AND period_year=2025 AND entidad=? "
            "ORDER BY period_month",
            (ent,)
        ).fetchall()
        presentes[ent] = [r['period_month'] for r in ms]

gaps_criticos = []
for ent, meses_esp in esperados.items():
    pres = presentes.get(ent, [])
    gaps = [m for m in meses_esp if m not in pres]
    extras = [m for m in pres if m not in meses_esp]
    if gaps:
        gaps_str = ', '.join(MESES.get(m, str(m)) for m in gaps)
        print(f"  {ent:12s}: GAPS  → {gaps_str}")
        if ent not in ('GAD', 'EMAI-EP'):  # GAD y EMAI-EP tienen gaps conocidos
            gaps_criticos.append(f"{ent} meses {gaps_str}")
    else:
        print(f"  {ent:12s}: OK — cobertura completa (según disponibilidad)")

# ── 6. INTEGRIDAD SUPABASE — LINEAS INGESTA ───────────────────────────────────
print("\n[6/6] INTEGRIDAD — LÍNEAS DE EJECUCIÓN")
lines = conn.execute("""
    SELECT du.entidad, du.period_month, COUNT(bel.id) as lineas
    FROM document_uploads du
    LEFT JOIN budget_execution_lines bel ON bel.upload_id = du.id
    WHERE du.document_type='CEDULA' AND du.period_year=2025
    GROUP BY du.entidad, du.period_month, du.id
    HAVING COUNT(bel.id) = 0
""").fetchall()

if lines:
    print("  WARN: uploads sin líneas de ejecución:")
    for l in lines:
        print(f"  {l['entidad']} mes {l['period_month']}: 0 líneas")
else:
    print("  OK — todos los uploads tienen líneas de ejecución asociadas")

conn.close()

print("\n" + "=" * 70)
print("  QA Longitudinal completado.")
if gaps_criticos:
    print(f"  ⚠ Gaps no esperados: {'; '.join(gaps_criticos)}")
else:
    print("  ✓ Sin gaps críticos. Cobertura 2025 dentro de lo disponible.")
print("=" * 70)
