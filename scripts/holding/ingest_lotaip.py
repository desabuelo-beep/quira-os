# -*- coding: utf-8 -*-
"""
ingest_lotaip.py — Cédulas Mensuales LOTAIP → holding_structured_data
QUIRA Gov · Gate 6.5 Fase 4b · Dylus Lab © 2026

Auto-descubre archivos XLSX de ejecución mensual (LOTAIP Numeral 6-6)
desde Presupuestos 2025/ y Presupuestos 2026/ del Holding MCR.
No requiere manifest estático — detecta entidad/mes/año desde estructura
de carpetas y nombres de archivo.

Habilita:
  Q09 — POA vs Devengado (ejecución vs planificación)
  Q10 — PAC vs Devengado (contratado vs gastado)
  Q11 — Concentración diciembre (patología administrativa)
  Q12 — Gap A≠D cuantificable

Cobertura descubierta (2025-06-03):
  Bomberos  2025: 12/12 meses ✅
  EP Aseo   2025: 12/12 meses ✅
  Patronato 2025:  9/12 meses (falta: Ene, Mar faltante parcial)
  GAD       2025:  3/12 meses (Oct-Dic — meses anteriores no subidos por GAD)
  Todas     2026:  Ene-Mar/Abr ✅

Uso:
  python scripts/holding/ingest_lotaip.py           # ingesta completa
  python scripts/holding/ingest_lotaip.py --status  # resumen por entidad/mes
  python scripts/holding/ingest_lotaip.py --dry-run # sin escribir a DB
  python scripts/holding/ingest_lotaip.py --year 2025
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from config import DATOS_DIR as _DATOS
except Exception:                                        # noqa: BLE001
    import os as _os
    _DATOS = Path(_os.environ.get("QUIRA_DATOS", "."))

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

import toml
import streamlit as st
_secrets_path = ROOT / ".streamlit" / "secrets.toml"
_raw = toml.load(str(_secrets_path))
class _F:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k): return _raw[k]
st.secrets = _F()

from sentinel.db_config import get_connection

HOLDING_BASE = _DATOS / "Holding_Municipal_Montecristi"
PRESUP_BASE  = HOLDING_BASE / "Presupuestos 2023-2026"
VERSION      = "lotaip-v1.0"
NOW          = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ── MAPEOS ────────────────────────────────────────────────────────────────────

ENTITY_MAP = {
    "bomberos":   "BOMBEROS_MCR",
    "aseo":       "EP_ASEO_MCR",
    "gad":        "GAD_MCR",
    "patronato":  "PATRONATO_MCR",
}

MES_MAP = {
    "enero":      ("01", "ENE"),
    "febrero":    ("02", "FEB"),
    "marzo":      ("03", "MAR"),
    "abril":      ("04", "ABR"),
    "mayo":       ("05", "MAY"),
    "junio":      ("06", "JUN"),
    "julio":      ("07", "JUL"),
    "agosto":     ("08", "AGO"),
    "septiembre": ("09", "SEP"),
    "octubre":    ("10", "OCT"),
    "noviembre":  ("11", "NOV"),
    "diciembre":  ("12", "DIC"),
}

def _detect_entity(folder_name: str) -> str | None:
    f = folder_name.lower()
    for key, entity in ENTITY_MAP.items():
        if key in f:
            return entity
    return None

def _detect_month_year(filename: str) -> tuple[str, str, str] | None:
    """Retorna (year, month_num, month_code) o None."""
    name = filename.lower()
    year_m = re.search(r"20(2[3-9])", name)
    if not year_m:
        return None
    year = "20" + year_m.group(1)
    for mes_str, (num, code) in MES_MAP.items():
        if mes_str in name:
            return year, num, code
    return None


# ── DESCUBRIMIENTO ────────────────────────────────────────────────────────────

def discover_files() -> list[dict]:
    """Descubre todos los XLSX/XLS de ejecución mensual LOTAIP."""
    files = []

    # Estructura 2025: Presupuestos 2025/{Entidad}/archivo.xlsx
    presup_2025 = PRESUP_BASE / "Presupuestos 2025"
    if presup_2025.exists():
        for entity_dir in presup_2025.iterdir():
            if not entity_dir.is_dir():
                continue
            entity = _detect_entity(entity_dir.name)
            if not entity:
                continue
            for f in entity_dir.glob("*.xlsx"):
                result = _detect_month_year(f.name)
                if result:
                    year, month_num, month_code = result
                    files.append({
                        "path":       f,
                        "source_entity": entity,
                        "year":       int(year),
                        "month_num":  month_num,
                        "month_code": month_code,
                        "periodo":    f"{year}-{month_num}",
                        "sigla":      f"LOTAIP-{entity.replace('_MCR','')}-{year}-{month_code}",
                    })

    # Estructura 2026: Presupuestos 2026/Cedulas Mensuales {Entidad} 2026/archivo.xlsx
    presup_2026 = PRESUP_BASE / "Presupuestos 2026"
    if presup_2026.exists():
        for sub in presup_2026.iterdir():
            if not sub.is_dir():
                continue
            entity = _detect_entity(sub.name)
            if not entity:
                continue
            for f in sub.glob("*.xlsx"):
                result = _detect_month_year(f.name)
                if result:
                    year, month_num, month_code = result
                    files.append({
                        "path":       f,
                        "source_entity": entity,
                        "year":       int(year),
                        "month_num":  month_num,
                        "month_code": month_code,
                        "periodo":    f"{year}-{month_num}",
                        "sigla":      f"LOTAIP-{entity.replace('_MCR','')}-{year}-{month_code}",
                    })

    return sorted(files, key=lambda x: (x["source_entity"], x["year"], x["month_num"]))


# ── HELPERS ────────────────────────────────────────────────────────────────────

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_existing_sha256s(conn) -> set[str]:
    try:
        c = conn.cursor()
        c.execute("SELECT archivo_sha256 FROM holding_structured_data WHERE archivo_sha256 IS NOT NULL")
        return {row["archivo_sha256"] for row in c.fetchall()}
    except Exception:
        return set()


def _read_excel(path: Path) -> list[dict]:
    import openpyxl
    wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    ws = wb.active
    all_rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if not all_rows:
        return []
    headers = [str(h).strip() if h is not None else f"col_{i}"
               for i, h in enumerate(all_rows[0])]
    rows = []
    for raw_row in all_rows[1:]:
        row = {h: (v if isinstance(v, (int, float)) else str(v))
               for h, v in zip(headers, raw_row)
               if v is not None and str(v).strip()}
        if row:
            rows.append(row)
    return rows


# ── INGESTIÓN ─────────────────────────────────────────────────────────────────

def _ingest_one(conn, entry: dict, existing: set[str], dry_run: bool) -> str:
    sha = _sha256_file(entry["path"])
    if sha in existing:
        return "SKIP"

    rows = _read_excel(entry["path"])
    if not rows:
        return "EMPTY"

    if dry_run:
        return f"DRY({len(rows)}f)"

    datos = {
        "sigla":      entry["sigla"],
        "archivo":    str(entry["path"].relative_to(HOLDING_BASE)),
        "rows":       rows,
        "total_rows": len(rows),
    }

    try:
        conn.execute("""
            INSERT INTO holding_structured_data
                (source_entity, canton_id, document_class, authority_level,
                 evidence_type, periodo, archivo_nombre, archivo_sha256,
                 datos_json, ingestado_at, ingestado_por)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s,%s)
            ON CONFLICT (archivo_sha256) DO NOTHING
        """, (
            entry["source_entity"],
            "MCR",
            "INSTRUMENTO_TERRITORIAL",
            22,                     # authority_level cedula = 22 (igual que SIGAD_ICM)
            "LOTAIP_DATOS",
            entry["periodo"],
            entry["path"].name,
            sha,
            json.dumps(datos, ensure_ascii=False, default=str),
            NOW,
            VERSION,
        ))
        conn.commit()
        existing.add(sha)
        return f"OK({len(rows)}f)"
    except Exception as exc:
        try:
            conn._conn.rollback()
        except Exception:
            pass
        return f"ERR:{exc}"


# ── STATUS ────────────────────────────────────────────────────────────────────

def cmd_status() -> None:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT source_entity, periodo,
               (datos_json->>'total_rows')::int AS filas
        FROM holding_structured_data
        WHERE evidence_type = 'LOTAIP_DATOS' AND canton_id = 'MCR'
        ORDER BY source_entity, periodo
    """)
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No hay datos LOTAIP en holding_structured_data.")
        return

    print(f"\n{'Entidad':20s} {'Período':10s} {'Filas':>6}")
    print("-" * 40)
    by_entity: dict[str, list] = {}
    for r in rows:
        e = r["source_entity"]; p = r["periodo"]; f = r["filas"] or 0
        by_entity.setdefault(e, []).append((p, f))
        print(f"{e:20s} {p:10s} {f:>6}")

    print("\n--- Cobertura mensual ---")
    all_months = sorted({p for e in by_entity.values() for p, _ in e})
    print(f"{'Entidad':20s}", end="")
    for m in all_months:
        print(f" {m[5:]:>3}", end="")
    print()
    for ent, meses in sorted(by_entity.items()):
        meses_set = {p for p, _ in meses}
        print(f"{ent:20s}", end="")
        for m in all_months:
            print(f" {'✓' if m in meses_set else '·':>3}", end="")
        print()


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta LOTAIP mensual Holding MCR")
    parser.add_argument("--status",  action="store_true")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    parser.add_argument("--year",    type=int, help="Solo este año (2025 o 2026)")
    args = parser.parse_args()

    if args.status:
        cmd_status()
        return

    files = discover_files()
    if args.year:
        files = [f for f in files if f["year"] == args.year]

    print(f"\nDescubiertos: {len(files)} archivos LOTAIP mensuales")

    # Resumen de cobertura ANTES de ingestar
    from collections import defaultdict
    coverage: dict[str, set] = defaultdict(set)
    for f in files:
        coverage[f["source_entity"]].add(f["periodo"])
    print("\nCobertura descubierta:")
    for ent in sorted(coverage):
        meses = sorted(coverage[ent])
        print(f"  {ent:20s} {len(meses):2d} meses: {', '.join(m[5:] for m in meses)}")

    conn = get_connection()
    existing = _load_existing_sha256s(conn)

    inserted = skipped = errors = 0
    print()
    for entry in files:
        result = _ingest_one(conn, entry, existing, dry_run=args.dry_run)
        entity_short = entry["source_entity"].replace("_MCR","")
        label = f"{entity_short:12s} {entry['periodo']}"
        if result.startswith("OK"):
            print(f"  [OK]    {label}  {result}")
            inserted += 1
        elif result == "SKIP":
            skipped += 1
        elif result.startswith("DRY"):
            print(f"  [DRY]   {label}  {result}")
        elif result == "EMPTY":
            print(f"  [EMPTY] {label}")
        else:
            print(f"  [ERR]   {label}  {result}")
            errors += 1

    conn.close()
    print(f"\n{'='*50}")
    print(f"  LOTAIP: Insertados={inserted}  Existían={skipped}  Errores={errors}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
