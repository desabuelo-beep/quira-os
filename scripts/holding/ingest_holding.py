# -*- coding: utf-8 -*-
"""
ingest_holding.py — Pipeline: Holding MCR → normativa_corpus (Capas C y D)
QUIRA Gov · Dylus Lab © 2026

Uso:
  python scripts/holding/ingest_holding.py                # ingesta completa
  python scripts/holding/ingest_holding.py --fase 1       # solo RC+PP (Fase 1)
  python scripts/holding/ingest_holding.py --sigla RC-GAD-2023
  python scripts/holding/ingest_holding.py --status       # estadisticas
  python scripts/holding/ingest_holding.py --dry-run      # sin escribir a DB

Idempotente: SHA256 UNIQUE en normativa_corpus — duplicados omitidos.
Token-eficiente: Python corre localmente, documentos nunca entran a Claude.

Schema v2.0: inserta document_class, authority_level, source_entity,
canton_id, evidence_type en cada chunk (ADR-021).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

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

# ── Script-local imports ──────────────────────────────────────────────────────
_THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(_THIS_DIR))
from chunker_holding import chunk_holding_doc

EMBED_MODEL   = "paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM     = 384
BATCH_SIZE    = 16
VERSION       = "holding-v1.0"
NOW           = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _load_existing_hashes(conn) -> set[str]:
    try:
        c = conn.cursor()
        c.execute("SELECT sha256 FROM normativa_corpus")
        return {row["sha256"] for row in c.fetchall()}
    except Exception:
        return set()


def _get_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL)


def _embed_batch(model, texts: list[str]) -> list[list[float]]:
    vecs = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return [v.tolist() for v in vecs]


def _load_document_id(conn, sigla: str) -> Optional[int]:
    """Obtiene document_id de la tabla documents para un sigla dado."""
    try:
        c = conn.cursor()
        c.execute("SELECT document_id FROM documents WHERE norma_sigla = %s", (sigla,))
        row = c.fetchone()
        if row:
            val = list(row.values())[0] if isinstance(row, dict) else row[0]
            return val
        return None
    except Exception:
        return None


def _upsert_document(conn, entry: dict) -> int:
    """
    Inserta el documento en la tabla documents si no existe.
    Retorna el document_id.
    """
    conn.execute("""
        INSERT INTO documents
            (norma_sigla, norma_nombre, document_class, authority_level,
             source_entity, canton_id, evidence_type, vigente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
        ON CONFLICT (norma_sigla) DO UPDATE SET
            document_class  = EXCLUDED.document_class,
            authority_level = EXCLUDED.authority_level,
            source_entity   = EXCLUDED.source_entity,
            canton_id       = EXCLUDED.canton_id,
            evidence_type   = EXCLUDED.evidence_type,
            updated_at      = NOW()
    """, (
        entry["sigla"],
        entry["nombre"],
        entry["document_class"],
        entry["authority_level"],
        entry["source_entity"],
        entry["canton_id"],
        entry.get("evidence_type"),
    ))
    conn.commit()

    c = conn.cursor()
    c.execute("SELECT document_id FROM documents WHERE norma_sigla = %s", (entry["sigla"],))
    row = c.fetchone()
    return list(row.values())[0] if isinstance(row, dict) else row[0]


def _insert_chunk(conn, entry: dict, chunk, embedding: list[float],
                  document_id: int, dry_run: bool = False) -> bool:
    """Inserta un chunk en normativa_corpus con campos schema v2.0."""
    if dry_run:
        return True

    try:
        emb_str = "[" + ",".join(f"{v:.6f}" for v in embedding) + "]"
        conn.execute("""
            INSERT INTO normativa_corpus
                (norma_sigla, norma_nombre, jerarquia, milestone_qlep,
                 tipo_documento, articulo_num, articulo_raw, chunk_seq,
                 contenido, palabras, dominios_quira, sha256,
                 embedding, archivo_nombre, archivo_sha256,
                 ingestado_at, ingestado_por,
                 document_id, document_class, authority_level,
                 source_entity, canton_id, evidence_type)
            VALUES
                (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,
                 %s::vector,%s,%s, %s,%s,
                 %s,%s,%s, %s,%s,%s)
            ON CONFLICT (sha256) DO NOTHING
        """, (
            entry["sigla"],
            entry["nombre"],
            0,                              # jerarquia (holding: 0 = no aplica escala normativa)
            "F1.0",                         # milestone holding = F1.x
            entry.get("document_class","INSTRUMENTO_TERRITORIAL"),
            None,                           # articulo_num (no aplica)
            chunk.seccion_raw[:200] if chunk.seccion_raw else None,
            chunk.chunk_seq,
            chunk.contenido,
            chunk.palabras,
            "",                             # dominios_quira (se mapea post-ingesta)
            chunk.sha256,
            emb_str,
            entry["archivo"],
            "",                             # archivo_sha256
            NOW,
            VERSION,
            document_id,
            entry["document_class"],
            entry["authority_level"],
            entry["source_entity"],
            entry["canton_id"],
            entry.get("evidence_type"),
        ))
        conn.commit()
        return True
    except Exception as exc:
        err = str(exc).lower()
        if "unique" in err or "duplicate" in err:
            return False
        print(f"    [DB ERR] {exc}")
        return False


# ── STATUS ────────────────────────────────────────────────────────────────────

def cmd_status(conn) -> None:
    """Muestra estadisticas del corpus del Holding."""
    try:
        c = conn.cursor()
        c.execute("""
            SELECT norma_sigla, document_class, COUNT(*) AS chunks, SUM(palabras) AS palabras
            FROM normativa_corpus
            WHERE canton_id = 'MCR' AND norma_sigla LIKE ANY(ARRAY['RC-%','PP-%','POA-%','PAC-%','PAI-%','SIGAD-%'])
            GROUP BY norma_sigla, document_class
            ORDER BY document_class, norma_sigla
        """)
        rows = c.fetchall()
        if not rows:
            print("No hay datos del Holding en normativa_corpus todavia.")
            return

        print(f"\n{'Sigla':30s} {'Clase':30s} {'Chunks':>7s} {'Palabras':>10s}")
        print("-" * 80)
        total_chunks = 0
        for r in rows:
            sigla  = r["norma_sigla"]   if isinstance(r, dict) else r[0]
            clase  = r["document_class"] if isinstance(r, dict) else r[1]
            chunks = r["chunks"]        if isinstance(r, dict) else r[2]
            pals   = r["palabras"]      if isinstance(r, dict) else r[3]
            total_chunks += chunks
            print(f"  {sigla:28s} {clase:28s} {chunks:7d} {pals:10,d}")
        print("-" * 80)
        print(f"  Total Holding: {total_chunks:,} chunks en normativa_corpus")
    except Exception as e:
        print(f"Error: {e}")


# ── INGESTA ───────────────────────────────────────────────────────────────────

def ingest(fase: Optional[int] = None,
           sigla: Optional[str] = None,
           dry_run: bool = False) -> None:
    """Pipeline principal de ingesta del Holding."""

    # Importar manifesto (puede no existir aun)
    try:
        from manifest_holding import MANIFEST_HOLDING, HOLDING_BASE, get_fase, get_text_docs
    except ImportError:
        print("[ERROR] manifest_holding.py no encontrado. Ejecutar Gate 6.5 setup primero.")
        sys.exit(1)

    # Filtrar entradas a procesar
    candidates = [e for e in MANIFEST_HOLDING if e.get("ingest_mode") == "text"]

    if fase is not None:
        candidates = [e for e in candidates if e.get("fase") == fase]
    if sigla is not None:
        candidates = [e for e in candidates if e.get("sigla") == sigla]

    if not candidates:
        print(f"No hay documentos a procesar con los filtros aplicados.")
        return

    print(f"\nIngestando {len(candidates)} documentos del Holding MCR"
          f"{' (fase '+str(fase)+')' if fase else ''}"
          f"{' (dry-run)' if dry_run else ''}")

    conn = get_connection()
    existing_hashes = _load_existing_hashes(conn)
    model = _get_model() if not dry_run else None

    total_inserted = 0
    total_skipped  = 0
    total_errors   = 0

    for entry in candidates:
        filepath = Path(HOLDING_BASE) / entry["archivo"]

        if not filepath.exists():
            print(f"  [MISSING] {entry['sigla']:30s} {filepath.name}")
            total_errors += 1
            continue

        print(f"  Processing {entry['sigla']:30s} {filepath.suffix.upper()} ...", end=" ", flush=True)

        try:
            chunks = chunk_holding_doc(filepath)
        except Exception as e:
            print(f"[CHUNK ERR] {e}")
            total_errors += 1
            continue

        # Filtrar chunks ya existentes
        new_chunks = [c for c in chunks if c.sha256 not in existing_hashes]
        already    = len(chunks) - len(new_chunks)

        if not new_chunks:
            print(f"[SKIP] {len(chunks)} chunks ya existen")
            total_skipped += len(chunks)
            continue

        # Upsert documento en tabla documents
        if not dry_run:
            document_id = _upsert_document(conn, entry)
        else:
            document_id = -1

        # Embedding en batches
        inserted = 0
        texts = [c.contenido for c in new_chunks]

        for i in range(0, len(texts), BATCH_SIZE):
            batch_chunks  = new_chunks[i : i + BATCH_SIZE]
            batch_texts   = texts[i : i + BATCH_SIZE]
            embeddings    = _embed_batch(model, batch_texts) if not dry_run else [[0.0]*EMBED_DIM]*len(batch_texts)

            for chunk, emb in zip(batch_chunks, embeddings):
                ok = _insert_chunk(conn, entry, chunk, emb, document_id, dry_run)
                if ok:
                    inserted += 1
                    existing_hashes.add(chunk.sha256)

        total_inserted += inserted
        total_skipped  += already
        print(f"[OK] +{inserted} chunks (skip={already})")
        time.sleep(0.05)  # Rate limiting suave

    conn.close()

    print(f"\n{'='*55}")
    print(f"  Ingesta Holding MCR completada")
    print(f"  Insertados: {total_inserted:,}")
    print(f"  Ya existian: {total_skipped:,}")
    print(f"  Errores: {total_errors}")
    print(f"{'='*55}\n")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ingest_holding.py — Pipeline Holding MCR → normativa_corpus"
    )
    parser.add_argument("--fase",    type=int,  help="Fase de ingesta (1=RC+PP, 2=POA, 3=PAC, 4=SIGAD)")
    parser.add_argument("--sigla",   type=str,  help="Sigla especifica a ingestar")
    parser.add_argument("--status",  action="store_true", help="Ver estadisticas actuales")
    parser.add_argument("--dry-run", action="store_true", help="Simular sin escribir a DB")
    args = parser.parse_args()

    if args.status:
        conn = get_connection()
        cmd_status(conn)
        conn.close()
        return

    ingest(
        fase    = args.fase,
        sigla   = args.sigla,
        dry_run = args.dry_run,
    )


if __name__ == "__main__":
    main()
