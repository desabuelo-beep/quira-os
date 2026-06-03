#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
001_apply_schema_v2.py — Ejecutar Migration 001: Schema v2.0
QUIRA Gov · Dylus Lab © 2026

Uso:
  python scripts/migrations/001_apply_schema_v2.py            # aplica migración
  python scripts/migrations/001_apply_schema_v2.py --verify   # solo verifica estado
  python scripts/migrations/001_apply_schema_v2.py --rollback # revierte (CUIDADO)

Diseño:
  Star Schema — documents (dimension) + normativa_corpus (fact, denormalized)
  Referencia: ADR-021 · CANONICAL_CHUNK_SCHEMA.md v1.1
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent   # quira-os/
sys.path.insert(0, str(ROOT))

import toml
import streamlit as st
_secrets_path = ROOT / ".streamlit" / "secrets.toml"
_raw = toml.load(str(_secrets_path))
class _F:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k):  return _raw[k]
st.secrets = _F()

from sentinel.db_config import get_connection

# ── Mapping de documentos existentes → nuevas columnas ────────────────────────
# Fuente de verdad: CANONICAL_CHUNK_SCHEMA.md §4.2
# Formato: "sigla": (document_class, authority_level, source_entity, canton_id, circuit_refs_doc)
DOCUMENT_MAPPING: dict[str, tuple] = {
    # Capa A — NORMA
    "CE":               ("NORMA", 100, "CONST_EC",       None,      ["C01","C02","C03"]),
    "LOTAIP":           ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C01"]),
    "RLOTAIP":          ("NORMA",  80, "EJ_EJECUTIVO",   None,      ["C01"]),
    "LOPC":             ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C01","C02"]),
    "COD":              ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C01"]),
    "RCOD":             ("NORMA",  80, "CNE",            None,      ["C01"]),
    "COOTAD":           ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C01","C02","C03"]),
    "COOTAD-2026":      ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C01","C02"]),
    "COPLAFIP":         ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C02","C03"]),
    "RCOPLAFIP":        ("NORMA",  80, "EJ_EJECUTIVO",   None,      ["C02","C03"]),
    "LOTUGS":           ("NORMA",  95, "ASAMBLEA_NAC",   None,      []),
    "LOC-CGE":          ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C01","C03"]),
    "NCI-CGE":          ("NORMA",  80, "CGE",            None,      ["C01","C03"]),
    "CONA":             ("NORMA",  92, "ASAMBLEA_NAC",   None,      []),
    "LODISC":           ("NORMA",  92, "ASAMBLEA_NAC",   None,      []),
    "LOPAM":            ("NORMA",  92, "ASAMBLEA_NAC",   None,      []),
    "LMH":              ("NORMA",  92, "ASAMBLEA_NAC",   None,      []),
    "LPEVM":            ("NORMA",  92, "ASAMBLEA_NAC",   None,      []),
    "CEDAW":            ("NORMA",  70, "ONU",            None,      []),
    "CADH":             ("NORMA",  70, "OEA",            None,      []),
    "CDN":              ("NORMA",  70, "ONU",            None,      []),
    "PIDESC":           ("NORMA",  70, "ONU",            None,      []),
    "LOSNCP":           ("NORMA",  95, "ASAMBLEA_NAC",   None,      ["C03"]),
    "RLOSNCP":          ("NORMA",  80, "EJ_EJECUTIVO",   None,      ["C03"]),
    "LOSEP":            ("NORMA",  95, "ASAMBLEA_NAC",   None,      []),
    "RLOSEP":           ("NORMA",  80, "EJ_EJECUTIVO",   None,      []),
    "COA":              ("NORMA",  95, "ASAMBLEA_NAC",   None,      []),
    "COA-AMB":          ("NORMA",  95, "ASAMBLEA_NAC",   None,      []),
    "RCOA-AMB":         ("NORMA",  80, "EJ_EJECUTIVO",   None,      []),
    "LOTD":             ("NORMA",  95, "ASAMBLEA_NAC",   None,      []),
    "CLASP-2026":       ("NORMA",  65, "MEF",            None,      ["C02","C03"]),
    "RES-ORG-GADMCM-2025": ("NORMA", 75, "GAD_MCR",    "MCR",      []),
    "RES-CPCCS-RC-2026":("NORMA",  75, "CPCCS",         None,      ["C01"]),
    "LOIEME":           ("NORMA",  92, "ASAMBLEA_NAC",   None,      []),

    # Capa B — METODOLOGIA
    "GUIA-LOTAIP-MEC":  ("METODOLOGIA", 55, "SNP",       None,      ["C01"]),
    "GUIA-LOTAIP-ENT":  ("METODOLOGIA", 55, "SNP",       None,      ["C01"]),
    "ACUERDO-PDOT-2023":("METODOLOGIA", 65, "SNP",       None,      []),
    "LINEAMIENTOS-PDOT-2023": ("METODOLOGIA", 65, "SNP", None,      []),
    "LINEAMIENTOS-PFI": ("METODOLOGIA", 60, "SNP",       None,      []),
    "PND-2025":         ("METODOLOGIA", 50, "SNP",       None,      []),
    "PAGCC-2024":       ("METODOLOGIA", 50, "EJ_EJECUTIVO", None,   ["C01","C02"]),

    # Capa C — INSTRUMENTO_TERRITORIAL
    "PDOT-MONTECRISTI": ("INSTRUMENTO_TERRITORIAL", 48, "GAD_MCR", "MCR", ["C01","C02","C03"]),
    "PLAN-GOB-MCR":     ("INSTRUMENTO_TERRITORIAL", 15, "GAD_MCR", "MCR", ["C01","C02"]),
}


# ── PRE-CHECK ─────────────────────────────────────────────────────────────────
def check_state(conn) -> dict:
    """Verifica el estado actual del schema."""
    result = {}
    c = conn.cursor()

    def _bool(row) -> bool:
        """Extrae bool de fila — soporta dict y tuple."""
        if isinstance(row, dict):
            return list(row.values())[0]
        return row[0]

    def _int(row) -> int:
        if isinstance(row, dict):
            return list(row.values())[0]
        return row[0]

    # ¿Tabla documents existe?
    c.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'documents'
        )
    """)
    result["documents_exists"] = _bool(c.fetchone())

    # ¿normativa_corpus tiene document_class?
    c.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.columns
            WHERE table_name = 'normativa_corpus'
            AND column_name = 'document_class'
        )
    """)
    result["corpus_has_document_class"] = _bool(c.fetchone())

    # ¿Tabla holding_structured_data existe?
    c.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'holding_structured_data'
        )
    """)
    result["holding_exists"] = _bool(c.fetchone())

    # Conteo actual
    c.execute("SELECT COUNT(*) FROM normativa_corpus")
    result["chunks_total"] = _int(c.fetchone())

    # Chunks con document_class ya poblado (si la columna existe)
    if result["corpus_has_document_class"]:
        c.execute("SELECT COUNT(*) FROM normativa_corpus WHERE document_class IS NOT NULL")
        result["chunks_classified"] = _int(c.fetchone())
    else:
        result["chunks_classified"] = 0

    return result


def print_state(state: dict, title: str = "Estado Schema") -> None:
    ok  = "[OK]"
    nok = "[--]"
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")
    print(f"  Tabla documents:          {ok if state['documents_exists'] else nok}")
    print(f"  Tabla holding_structured: {ok if state['holding_exists'] else nok}")
    print(f"  corpus.document_class:    {ok if state['corpus_has_document_class'] else nok}")
    print(f"  Chunks total:             {state['chunks_total']:,}")
    print(f"  Chunks clasificados:      {state['chunks_classified']:,}")
    print(f"{'='*55}\n")


# ── DDL MIGRATION ─────────────────────────────────────────────────────────────
def apply_ddl(conn) -> None:
    """Aplica el DDL de Migration 001 (CREATE TABLE + ALTER TABLE + índices)."""
    ddl_path = Path(__file__).parent / "001_ddl_schema_v2.sql"
    sql = ddl_path.read_text(encoding="utf-8")

    print("  Aplicando DDL (CREATE TABLE documents + ALTER normativa_corpus)...")
    try:
        conn.execute(sql)
        conn.commit()
        print("  [OK] DDL aplicado correctamente.")
    except Exception as e:
        print(f"  [FAIL] Error en DDL: {e}")
        raise


# ── DATA MIGRATION ────────────────────────────────────────────────────────────
def populate_documents_table(conn) -> int:
    """
    Paso 1 de Gate 6.2:
    Inserta los 43 documentos existentes en la tabla documents,
    usando el DOCUMENT_MAPPING como fuente de verdad.
    """
    c = conn.cursor()
    inserted = 0
    skipped  = 0

    print(f"\n  Poblando tabla documents ({len(DOCUMENT_MAPPING)} entradas)...")

    for sigla, (doc_class, auth_level, source_ent, canton, _) in DOCUMENT_MAPPING.items():
        # Verificar si la sigla existe en normativa_corpus
        c.execute("SELECT DISTINCT norma_nombre, jerarquia, milestone_qlep, tipo_documento, archivo_nombre "
                  "FROM normativa_corpus WHERE norma_sigla = %s LIMIT 1", (sigla,))
        row = c.fetchone()
        if not row:
            print(f"    [WARN]  {sigla} no encontrada en corpus — saltando")
            skipped += 1
            continue

        try:
            # row es dict: {"norma_nombre": ..., "jerarquia": ..., etc.}
            conn.execute("""
                INSERT INTO documents
                    (norma_sigla, norma_nombre, document_class, authority_level,
                     source_entity, canton_id, jerarquia, milestone_qlep,
                     tipo_documento, archivo_nombre, vigente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                ON CONFLICT (norma_sigla) DO UPDATE SET
                    document_class  = EXCLUDED.document_class,
                    authority_level = EXCLUDED.authority_level,
                    source_entity   = EXCLUDED.source_entity,
                    canton_id       = EXCLUDED.canton_id,
                    updated_at      = NOW()
            """, (
                sigla,
                row.get("norma_nombre") if isinstance(row, dict) else row[0],
                doc_class, auth_level, source_ent, canton,
                row.get("jerarquia")     if isinstance(row, dict) else row[1],
                row.get("milestone_qlep") if isinstance(row, dict) else row[2],
                row.get("tipo_documento") if isinstance(row, dict) else row[3],
                row.get("archivo_nombre") if isinstance(row, dict) else row[4],
            ))
            inserted += 1
            print(f"    [v] {sigla:30s} -> {doc_class} / auth={auth_level}")
        except Exception as e:
            print(f"    [FAIL] {sigla}: {e}")

    conn.commit()
    print(f"\n  Resultado: {inserted} insertados / {skipped} saltados")
    return inserted


def update_corpus_columns(conn) -> int:
    """
    Paso 2 de Gate 6.2:
    Actualiza las columnas denormalizadas en normativa_corpus
    usando los valores recién insertados en documents.
    """
    print("\n  Actualizando columnas denormalizadas en normativa_corpus...")
    try:
        conn.execute("""
            UPDATE normativa_corpus nc
            SET
                document_id     = d.document_id,
                document_class  = d.document_class,
                authority_level = d.authority_level,
                source_entity   = d.source_entity,
                canton_id       = d.canton_id
            FROM documents d
            WHERE nc.norma_sigla = d.norma_sigla
              AND (nc.document_class IS NULL OR nc.document_id IS NULL)
        """)
        conn.commit()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM normativa_corpus WHERE document_class IS NOT NULL")
        row = c.fetchone()
        updated = list(row.values())[0] if isinstance(row, dict) else row[0]
        print(f"  [OK] {updated:,} chunks actualizados con nuevas columnas")
        return updated
    except Exception as e:
        print(f"  [FAIL] Error actualizando corpus: {e}")
        raise


# ── ROLLBACK ──────────────────────────────────────────────────────────────────
def apply_rollback(conn) -> None:
    """Revierte Migration 001. USAR CON CUIDADO."""
    rollback_path = Path(__file__).parent / "001_rollback.sql"
    sql = rollback_path.read_text(encoding="utf-8")
    print("  [WARN]  APLICANDO ROLLBACK — esto destruye la tabla documents y los nuevos índices...")
    conn.execute(sql)
    conn.commit()
    print("  [OK] Rollback aplicado.")


# ── MAIN ──────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migration 001 — Schema v2.0 QUIRA Corpus"
    )
    parser.add_argument("--verify",   action="store_true",
                        help="Solo verificar estado actual, no modificar nada")
    parser.add_argument("--rollback", action="store_true",
                        help="Revertir Migration 001 (DESTRUCTIVO)")
    parser.add_argument("--populate", action="store_true",
                        help="Solo poblar datos (Gate 6.2) — requiere DDL ya aplicado")
    args = parser.parse_args()

    conn = get_connection()
    state_before = check_state(conn)

    if args.verify:
        print_state(state_before, "Estado Actual Schema")
        conn.close()
        return

    if args.rollback:
        print_state(state_before, "Estado PRE-ROLLBACK")
        apply_rollback(conn)
        print_state(check_state(conn), "Estado POST-ROLLBACK")
        conn.close()
        return

    print_state(state_before, "Estado PRE-MIGRACIÓN (Gate 6.1b)")

    if not state_before["documents_exists"]:
        # Gate 6.1b: DDL
        print("\n  [Gate 6.1b] Aplicando DDL...")
        apply_ddl(conn)
    else:
        print("\n  [Gate 6.1b] DDL ya aplicado — saltando.")

    if args.populate or not state_before["corpus_has_document_class"] or state_before["chunks_classified"] == 0:
        # Gate 6.2: Data migration
        print("\n  [Gate 6.2] Poblando tabla documents y actualizando corpus...")
        inserted = populate_documents_table(conn)
        if inserted > 0:
            update_corpus_columns(conn)
    else:
        classified = state_before["chunks_classified"]
        total      = state_before["chunks_total"]
        print(f"\n  [Gate 6.2] {classified}/{total} chunks ya clasificados — saltando.")

    state_after = check_state(conn)
    print_state(state_after, "Estado POST-MIGRACIÓN")

    # Verificación de integridad
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM normativa_corpus WHERE document_class IS NULL")
    row = c.fetchone()
    unclassified = list(row.values())[0] if isinstance(row, dict) else row[0]
    if unclassified > 0:
        print(f"  [WARN]  ATENCIÓN: {unclassified} chunks sin clasificar (norma_sigla no en DOCUMENT_MAPPING)")
        c.execute("SELECT DISTINCT norma_sigla FROM normativa_corpus WHERE document_class IS NULL")
        missing = [list(r.values())[0] if isinstance(r, dict) else r[0] for r in c.fetchall()]
        print(f"     Siglas faltantes: {missing}")
    else:
        print("  [OK] Todos los chunks clasificados correctamente.")

    conn.close()
    print("\n  [OK] Migration 001 completada.\n")


if __name__ == "__main__":
    main()
