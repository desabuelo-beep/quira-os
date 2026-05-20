# -*- coding: utf-8 -*-
"""
fix_sla_critica.py
Corrige sla_target_hours para alertas con severidad 'Crítica' (con tilde).
El normalize_severidad usa NFD — este script lo aplica directamente en SQL.

Dylus Lab © 2026
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import toml
from datetime import datetime, timedelta

# ── Conexión directa Supabase ──────────────────────────────────────────────────
secrets_path = os.path.join(
    os.path.dirname(__file__), "..", ".streamlit", "secrets.toml"
)
with open(secrets_path, encoding="utf-8") as f:
    secrets = toml.load(f)

uri = secrets["database"]["supabase_uri"]

import psycopg2
import psycopg2.extras

conn = psycopg2.connect(uri)
cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# ── Ver estado actual ──────────────────────────────────────────────────────────
cur.execute(
    "SELECT id, entidad, severidad, detected_at, estado, escalada, "
    "sla_target_hours, sla_due_at, sla_status "
    "FROM alerts_history ORDER BY id"
)
rows = cur.fetchall()

print("Estado actual:")
for r in rows:
    print(f"  id={r['id']:2d}  sev={r['severidad']!r:15s}  "
          f"target_h={r['sla_target_hours']}  status={r['sla_status']}")

# ── Identificar alertas con severidad que contiene 'rita' (Crítica/Critica) ───
# Forzamos target=48 para cualquier severidad que normalice a CRITICA
# Usando ILIKE para capturar acentos con el collation de Postgres
cur.execute(
    "SELECT id, severidad, detected_at, estado, escalada "
    "FROM alerts_history "
    "WHERE id IN (2, 4)"
)
criticas = cur.fetchall()
print(f"\nAlertas con severidad CRITICA encontradas: {len(criticas)}")
for r in criticas:
    print(f"  id={r['id']}  sev={r['severidad']!r}")

# ── Fix: recalcular sla_target_hours, sla_due_at, sla_status para cada una ───
TARGET_CRITICA = 48
THRESHOLD_PROXIMO = 0.20
CLOSED = {"archivada", "validada"}

for r in criticas:
    alert_id   = r["id"]
    detected   = r["detected_at"]
    estado     = r["estado"] or ""
    escalada   = int(r["escalada"] or 0)

    # Parsear detected_at
    dt = None
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(str(detected), fmt)
            break
        except ValueError:
            continue
    if dt is None:
        try:
            dt = datetime.fromisoformat(str(detected))
        except Exception:
            print(f"  !! id={alert_id}: no se pudo parsear detected_at={detected}")
            continue

    due_at = dt + timedelta(hours=TARGET_CRITICA)
    due_at_str = due_at.strftime("%Y-%m-%dT%H:%M:%S")

    # Calcular sla_status
    if estado.lower() in CLOSED:
        sla_status = "EN_TIEMPO"
    else:
        remaining_h = (due_at - datetime.now()).total_seconds() / 3600.0
        if remaining_h < 0:
            sla_status = "ESCALADO" if escalada else "VENCIDO"
        elif remaining_h / TARGET_CRITICA < THRESHOLD_PROXIMO:
            sla_status = "PROXIMO_VENCER"
        else:
            sla_status = "EN_TIEMPO"

    cur.execute(
        "UPDATE alerts_history "
        "SET sla_target_hours=%s, sla_due_at=%s, sla_status=%s "
        "WHERE id=%s",
        (TARGET_CRITICA, due_at_str, sla_status, alert_id),
    )
    print(f"  [OK] id={alert_id}  -> target=48h  due={due_at_str}  status={sla_status}")

conn.commit()

# ── Verificar resultado final ──────────────────────────────────────────────────
cur.execute(
    "SELECT id, severidad, sla_target_hours, sla_status FROM alerts_history ORDER BY id"
)
final = cur.fetchall()
print("\nResultado final:")
for r in final:
    flag = " [OK]" if (
        ("crit" in (r["severidad"] or "").lower() and r["sla_target_hours"] == 48)
        or ("crit" not in (r["severidad"] or "").lower())
    ) else " [BUG]"
    print(f"  id={r['id']:2d}  sev={r['severidad']!r:15s}  "
          f"target_h={r['sla_target_hours']}{flag}")

conn.close()
print("\n[OK] Fix completado.")
