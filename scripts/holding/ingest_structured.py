# -*- coding: utf-8 -*-
"""
ingest_structured.py — XLSX/XLS del Holding MCR → holding_structured_data
QUIRA Gov · Gate 6.5 Fase 4 (Cédulas Presupuestarias) · Dylus Lab © 2026

Ingesta datos tabulares (cédulas, presupuestos, POA-Excel) a Supabase.
No genera embeddings vectoriales — los datos quedan como JSONB para
queries de trazabilidad financiera (Q09-Q12).

Preguntas que habilita:
  Q09 — ¿Cuánto de lo planificado (POA) llegó a ejecutarse (devengado)?
  Q10 — ¿Cuántos procesos PAC terminaron como gasto efectivo?
  Q11 — ¿La ejecución se concentra en diciembre? (patología administrativa)
  Q12 — Gap A≠D cuantificable: Norma→Plan→Ejecución→RC

Idempotente: UNIQUE en archivo_sha256 — duplicados ignorados.

Uso:
  python scripts/holding/ingest_structured.py           # todos los XLSX/XLS
  python scripts/holding/ingest_structured.py --sigla STRUCT-GAD-CEDULA-GASTOS-2024
  python scripts/holding/ingest_structured.py --status
  python scripts/holding/ingest_structured.py --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

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

_THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(_THIS_DIR))
from manifest_holding import HOLDING_BASE, MANIFEST_HOLDING

VERSION = "struct-v1.0"
NOW     = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    """Lee XLSX/XLS y retorna lista de filas como dicts (header = primera fila)."""
    import openpyxl

    suffix = path.suffix.lower()
    if suffix == ".xls":
        import xlrd
        wb = xlrd.open_workbook(str(path))
        ws = wb.sheet_by_index(0)
        if ws.nrows == 0:
            return []
        headers = [str(ws.cell_value(0, c)).strip() for c in range(ws.ncols)]
        rows = []
        for r in range(1, ws.nrows):
            row = {}
            for c, h in enumerate(headers):
                val = ws.cell_value(r, c)
                if val != "":
                    row[h or f"col_{c}"] = str(val) if not isinstance(val, (int, float)) else val
            if any(row.values()):
                rows.append(row)
        return rows
    else:
        wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
        ws = wb.active
        all_rows = list(ws.iter_rows(values_only=True))
        wb.close()
        if not all_rows:
            return []
        # Primera fila no vacía = headers
        headers = [str(h).strip() if h is not None else f"col_{i}"
                   for i, h in enumerate(all_rows[0])]
        rows = []
        for raw_row in all_rows[1:]:
            row = {}
            for h, val in zip(headers, raw_row):
                if val is not None and str(val).strip():
                    row[h] = val if isinstance(val, (int, float)) else str(val)
            if any(row.values()):
                rows.append(row)
        return rows


def _ingest_entry(conn, entry: dict, existing_sha256s: set[str],
                  dry_run: bool = False) -> str:
    """Procesa una entrada structured. Retorna 'OK' | 'SKIP' | 'MISSING' | 'ERR'."""
    path = Path(HOLDING_BASE) / entry["archivo"]
    sigla = entry["sigla"]

    if not path.exists():
        return "MISSING"

    suffix = path.suffix.lower()
    if suffix not in (".xlsx", ".xls"):
        return f"SKIP_FORMAT({suffix})"

    sha = _sha256_file(path)
    if sha in existing_sha256s:
        return "SKIP_DUP"

    rows = _read_excel(path)
    if not rows:
        return "EMPTY"

    # Extraer periodo desde el año del entry o del nombre del archivo
    year = entry.get("year")
    periodo = str(year) if year else path.stem

    datos = {
        "sigla":   sigla,
        "archivo": entry["archivo"],
        "rows":    rows,
        "total_rows": len(rows),
    }

    if dry_run:
        return f"DRY({len(rows)} filas)"

    # document_class: solo INSTRUMENTO_TERRITORIAL | EVIDENCIA_OBSERVACIONAL (constraint DB)
    doc_class = entry.get("document_class", "INSTRUMENTO_TERRITORIAL")
    if doc_class not in ("INSTRUMENTO_TERRITORIAL", "EVIDENCIA_OBSERVACIONAL"):
        doc_class = "INSTRUMENTO_TERRITORIAL"

    # evidence_type: solo RC_INFORME | PP_INFORME | EDV | SIGAD_ICM | LOTAIP_DATOS | NULL
    ev_type = entry.get("evidence_type")
    if ev_type not in (None, "RC_INFORME", "PP_INFORME", "EDV", "SIGAD_ICM", "LOTAIP_DATOS"):
        ev_type = "LOTAIP_DATOS"  # datos de transparencia activa

    try:
        conn.execute("""
            INSERT INTO holding_structured_data
                (source_entity, canton_id, document_class, authority_level,
                 evidence_type, periodo, archivo_nombre, archivo_sha256,
                 datos_json, ingestado_at, ingestado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s)
            ON CONFLICT (archivo_sha256) DO NOTHING
        """, (
            entry.get("source_entity", "UNKNOWN"),
            entry.get("canton_id", "MCR"),
            doc_class,
            entry.get("authority_level"),
            ev_type,
            periodo,
            str(entry["archivo"]),
            sha,
            json.dumps(datos, ensure_ascii=False, default=str),
            NOW,
            VERSION,
        ))
        conn.commit()
        existing_sha256s.add(sha)
        return f"OK({len(rows)} filas)"
    except Exception as exc:
        try:
            conn._conn.rollback()  # limpiar transacción abortada
        except Exception:
            pass
        return f"ERR: {exc}"


# ── COMANDOS ──────────────────────────────────────────────────────────────────

def cmd_status(conn) -> None:
    c = conn.cursor()
    c.execute("""
        SELECT source_entity, document_class, COUNT(*) AS docs,
               SUM((datos_json->'total_rows')::int) AS total_filas
        FROM holding_structured_data
        WHERE canton_id = 'MCR'
        GROUP BY source_entity, document_class
        ORDER BY source_entity, document_class
    """)
    rows = c.fetchall()
    if not rows:
        print("holding_structured_data vacío.")
        return
    print(f"\n{'Entidad':20s} {'Clase':30s} {'Docs':>5} {'Filas':>8}")
    print("-" * 70)
    total_docs = total_filas = 0
    for r in rows:
        d = r["docs"]; f = r["total_filas"] or 0
        print(f"{r['source_entity']:20s} {r['document_class']:30s} {d:>5} {f:>8}")
        total_docs += d; total_filas += (f or 0)
    print("-" * 70)
    print(f"{'TOTAL':20s} {'':30s} {total_docs:>5} {total_filas:>8}")


def cmd_ingest(entries: list[dict], dry_run: bool = False) -> None:
    conn = get_connection()
    existing = _load_existing_sha256s(conn)

    inserted = skipped = errors = missing = 0
    print(f"\nIngestando {len(entries)} entradas structured del Holding MCR\n")

    for entry in entries:
        sigla = entry.get("sigla", "?")
        result = _ingest_entry(conn, entry, existing, dry_run=dry_run)

        if result.startswith("OK"):
            print(f"  [OK]      {sigla:50s} {result}")
            inserted += 1
        elif result.startswith("SKIP_DUP"):
            print(f"  [SKIP]    {sigla:50s} ya existe")
            skipped += 1
        elif result == "MISSING":
            print(f"  [MISSING] {sigla:50s} archivo no encontrado")
            missing += 1
        elif result == "EMPTY":
            print(f"  [EMPTY]   {sigla:50s} sin filas")
        elif result.startswith("SKIP_FORMAT"):
            print(f"  [SKIP]    {sigla:50s} {result} — solo XLSX/XLS")
            skipped += 1
        elif result.startswith("DRY"):
            print(f"  [DRY-RUN] {sigla:50s} {result}")
        else:
            print(f"  [ERR]     {sigla:50s} {result}")
            errors += 1

    conn.close()
    print(f"\n{'='*55}")
    print(f"  Ingesta structured completada")
    print(f"  Insertados: {inserted}  |  Ya existian: {skipped}  |  Faltantes: {missing}  |  Errores: {errors}")
    print(f"{'='*55}\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Ingesta structured Holding MCR")
    parser.add_argument("--sigla",   help="Procesar solo esta sigla")
    parser.add_argument("--status",  action="store_true")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    args = parser.parse_args()

    struct_entries = [e for e in MANIFEST_HOLDING if e.get("ingest_mode") == "structured"]

    if args.status:
        conn = get_connection()
        cmd_status(conn)
        conn.close()
        return

    if args.sigla:
        entries = [e for e in struct_entries if e.get("sigla") == args.sigla]
        if not entries:
            print(f"Sigla no encontrada: {args.sigla}")
            sys.exit(1)
    else:
        entries = struct_entries

    cmd_ingest(entries, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
