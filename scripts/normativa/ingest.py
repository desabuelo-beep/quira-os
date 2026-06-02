# -*- coding: utf-8 -*-
"""
ingest.py — Pipeline completo: DOCX → chunks → embeddings → Supabase
QUIRA Gov · Corpus Normativo Ecuatoriano · Dylus Lab © 2026

Uso:
  python scripts/normativa/ingest.py                    # todos los documentos
  python scripts/normativa/ingest.py --milestone F0.1   # solo Constitución
  python scripts/normativa/ingest.py --sigla LOTAIP     # solo LOTAIP
  python scripts/normativa/ingest.py --status           # estadísticas actuales

Idempotente: SHA256 UNIQUE en DB — duplicados omitidos silenciosamente.
Token-eficiente: Python corre localmente, los documentos nunca entran a Claude.

Requerimientos:
  pip install python-docx sentence-transformers toml psycopg2-binary
"""

from __future__ import annotations

import argparse
import hashlib
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

# ── Parchear st.secrets para ejecutar fuera de Streamlit ─────────────────────
import toml
_secrets_path = ROOT / ".streamlit" / "secrets.toml"
_raw_secrets  = toml.load(str(_secrets_path))

import streamlit as st
class _FakeSecrets:
    def get(self, k, d=None):  return _raw_secrets.get(k, d)
    def __getitem__(self, k):  return _raw_secrets[k]
st.secrets = _FakeSecrets()

# ── QUIRA OS imports ──────────────────────────────────────────────────────────
from sentinel.db_config import get_connection

# ── Script-local imports ───────────────────────────────────────────────────────
_THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(_THIS_DIR))
from manifest import MANIFEST, NORMATIVA_BASE
from chunker  import chunk_docx_with_meta

# ── CONSTANTES ────────────────────────────────────────────────────────────────
EMBED_MODEL     = "paraphrase-multilingual-MiniLM-L12-v2"
EMBED_DIM       = 384
BATCH_SIZE      = 32       # chunks por batch de embedding
VERSION_SKILL   = "1.0"
NOW             = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ── HELPERS ───────────────────────────────────────────────────────────────────
def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def _load_existing_hashes(conn) -> set[str]:
    """Carga todos los SHA256 ya en normativa_corpus."""
    try:
        c = conn.cursor()
        c.execute("SELECT sha256 FROM normativa_corpus")
        return {row["sha256"] for row in c.fetchall()}
    except Exception:
        return set()


def _get_model():
    """Carga el modelo de embeddings (primera vez: descarga ~120 MB)."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBED_MODEL)


def _embed_batch(model, texts: list[str]) -> list[list[float]]:
    """Genera embeddings para un batch de textos."""
    vecs = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return [v.tolist() for v in vecs]


def _insert_chunk(conn, row: dict, embedding: list[float]) -> bool:
    """
    Inserta un chunk con su embedding en normativa_corpus.
    Retorna True si insertado, False si ya existía (UNIQUE constraint).
    """
    mode = conn.mode
    try:
        if mode == "supabase":
            # pgvector acepta el array como string "[0.1,0.2,...]"
            emb_str = "[" + ",".join(f"{v:.6f}" for v in embedding) + "]"
            conn.execute("""
                INSERT INTO normativa_corpus
                    (norma_sigla, norma_nombre, jerarquia, milestone_qlep,
                     tipo_documento, articulo_num, articulo_raw, chunk_seq,
                     contenido, palabras, dominios_quira, sha256,
                     embedding, archivo_nombre, archivo_sha256,
                     ingestado_at, ingestado_por)
                VALUES
                    (%s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,
                     %s::vector,%s,%s, %s,%s)
                ON CONFLICT (sha256) DO NOTHING
            """, (
                row["norma_sigla"], row["norma_nombre"], row["jerarquia"],
                row["milestone_qlep"], row["tipo_documento"],
                row.get("articulo_num"), row.get("articulo_raw"),
                row["chunk_seq"],
                row["contenido"], row["palabras"], row["dominios_quira"],
                row["sha256"],
                emb_str, row["archivo_nombre"], row.get("archivo_sha256", ""),
                NOW, f"qlep-corpus-v{VERSION_SKILL}",
            ))
        else:
            # SQLite: embedding como JSON
            emb_json = json.dumps(embedding)
            conn.execute("""
                INSERT OR IGNORE INTO normativa_corpus
                    (norma_sigla, norma_nombre, jerarquia, milestone_qlep,
                     tipo_documento, articulo_num, articulo_raw, chunk_seq,
                     contenido, palabras, dominios_quira, sha256,
                     embedding, archivo_nombre, archivo_sha256,
                     ingestado_at, ingestado_por)
                VALUES
                    (?,?,?,?, ?,?,?,?, ?,?,?,?, ?,?,?, ?,?)
            """, (
                row["norma_sigla"], row["norma_nombre"], row["jerarquia"],
                row["milestone_qlep"], row["tipo_documento"],
                row.get("articulo_num"), row.get("articulo_raw"),
                row["chunk_seq"],
                row["contenido"], row["palabras"], row["dominios_quira"],
                row["sha256"],
                emb_json, row["archivo_nombre"], row.get("archivo_sha256", ""),
                NOW, f"qlep-corpus-v{VERSION_SKILL}",
            ))
        conn.commit()
        return True
    except Exception as exc:
        err = str(exc).lower()
        if "unique" in err or "duplicate" in err:
            return False   # ya existía
        print(f"    [DB ERR] {exc}")
        return False


# ── STATUS ────────────────────────────────────────────────────────────────────
def cmd_status() -> None:
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT norma_sigla, milestone_qlep,
                   COUNT(*) AS chunks,
                   SUM(palabras) AS palabras_total,
                   SUM(CASE WHEN embedding IS NOT NULL THEN 1 ELSE 0 END) AS con_embedding
            FROM normativa_corpus
            GROUP BY norma_sigla, milestone_qlep
            ORDER BY milestone_qlep, norma_sigla
        """)
        rows = c.fetchall()
        if not rows:
            print("normativa_corpus está vacía — ejecutar ingest.py primero.")
            conn.close()
            return

        total_chunks = sum(r["chunks"] for r in rows)
        total_emb    = sum(r["con_embedding"] for r in rows)

        print(f"\n{'Sigla':25s} {'Milestone':8s} {'Chunks':>7s} {'Palabras':>10s} {'Emb':>5s}")
        print("-" * 62)
        for r in rows:
            emb_ok = "✓" if r["con_embedding"] == r["chunks"] else f"{r['con_embedding']}/{r['chunks']}"
            print(f"  {r['norma_sigla']:23s} {r['milestone_qlep']:8s} "
                  f"{r['chunks']:7d} {r['palabras_total']:10,d} {emb_ok:>5s}")
        print("-" * 62)
        print(f"  {'TOTAL':23s} {'':8s} {total_chunks:7d}  {'':9s} "
              f"{'✓' if total_emb == total_chunks else str(total_emb)+'/'+ str(total_chunks):>5s}")

    except Exception as exc:
        print(f"Error consultando estado: {exc}")
    conn.close()


# ── INGESTA ───────────────────────────────────────────────────────────────────
def ingest(milestone: Optional[str] = None,
           sigla: Optional[str] = None,
           dry_run: bool = False) -> None:

    # Filtrar manifiesto
    entries = MANIFEST
    if milestone:
        entries = [e for e in entries if e["milestone"] == milestone]
    if sigla:
        entries = [e for e in entries if e["sigla"] == sigla]

    if not entries:
        print("No se encontraron documentos con los filtros indicados.")
        return

    print("=" * 65)
    print("  QUIRA — Corpus Normativo Ecuatoriano · Ingesta v" + VERSION_SKILL)
    print(f"  Documentos a procesar: {len(entries)}")
    print("=" * 65)

    # [1] Hashes existentes
    print("\n[1/4] Cargando hashes existentes...")
    conn = get_connection()
    existing = _load_existing_hashes(conn)
    conn.close()
    print(f"      {len(existing)} chunks ya registrados en DB.")

    # [2] Modelo de embeddings
    print("\n[2/4] Cargando modelo de embeddings...")
    model = _get_model()
    print(f"      {EMBED_MODEL} listo ({EMBED_DIM} dim)")

    # [3] Procesar documentos
    print("\n[3/4] Procesando documentos...\n")

    results = []
    ok_total   = 0
    skip_total = 0
    err_total  = 0

    for entry in entries:
        filepath  = os.path.join(NORMATIVA_BASE, entry["archivo"])
        sigla_lbl = entry["sigla"]
        ms        = entry["milestone"]
        tag       = f"{sigla_lbl:25s} {ms}"

        if not os.path.exists(filepath):
            print(f"  [MISSING] {tag}  — {entry['archivo'][:50]}")
            results.append((tag, "MISSING", 0, 0))
            err_total += 1
            continue

        # Chunking
        t0 = time.time()
        try:
            file_sha = _file_sha256(filepath)
            rows = chunk_docx_with_meta(filepath, entry)
        except Exception as exc:
            print(f"  [ERR-PARSE] {tag}  — {exc}")
            results.append((tag, "ERR-PARSE", 0, 0))
            err_total += 1
            continue

        # Separar chunks nuevos de duplicados
        new_rows  = [r for r in rows if r["sha256"] not in existing]
        skip_rows = [r for r in rows if r["sha256"] in existing]

        if not new_rows:
            elapsed = time.time() - t0
            print(f"  [SKIP-DUP] {tag}  ({len(skip_rows)} chunks ya en DB)")
            results.append((tag, "DUP", len(skip_rows), 0))
            skip_total += len(skip_rows)
            continue

        if dry_run:
            print(f"  [DRY-RUN]  {tag}  → {len(new_rows)} chunks nuevos "
                  f"({len(skip_rows)} ya en DB)")
            results.append((tag, "DRY-RUN", len(new_rows), 0))
            continue

        # Añadir archivo_sha256
        for r in new_rows:
            r["archivo_sha256"] = file_sha

        # Embedding en batches
        texts = [r["contenido"] for r in new_rows]
        all_embeddings: list[list[float]] = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            embs  = _embed_batch(model, batch)
            all_embeddings.extend(embs)

        # Insertar
        conn_ins = get_connection()
        ok_doc   = 0
        for r, emb in zip(new_rows, all_embeddings):
            inserted = _insert_chunk(conn_ins, r, emb)
            if inserted:
                ok_doc += 1
                existing.add(r["sha256"])  # evitar duplicados en mismo batch
        conn_ins.close()

        elapsed = time.time() - t0
        print(f"  [OK]       {tag}  "
              f"{ok_doc:4d} chunks · {len(skip_rows):3d} dup · {elapsed:.1f}s")
        results.append((tag, "OK", ok_doc, len(skip_rows)))
        ok_total   += ok_doc
        skip_total += len(skip_rows)

    # [4] Resumen
    print("\n[4/4] Resumen:")
    print(f"  Chunks insertados:   {ok_total:,}")
    print(f"  Chunks duplicados:   {skip_total:,}")
    print(f"  Documentos con error:{err_total}")
    print(f"  Documentos OK:       {sum(1 for _, e, _, _ in results if e == 'OK')}")
    print()

    # Tabla final
    print("  Detalle por documento:")
    print("  " + "-" * 60)
    print(f"  {'Sigla-Milestone':30s}  {'Estado':10s}  {'Chunks':>6s}  {'Dup':>5s}")
    print("  " + "-" * 60)
    for tag, estado, chunks, dups in results:
        print(f"  {tag:30s}  {estado:10s}  {chunks:6d}  {dups:5d}")
    print("  " + "-" * 60)
    print()
    print("=" * 65)
    print("  Ingesta completada. Datos disponibles en Supabase.")
    print("=" * 65)


# ── CLI ───────────────────────────────────────────────────────────────────────
def _parse_args():
    p = argparse.ArgumentParser(
        description="QUIRA — Ingesta del Corpus Normativo Ecuatoriano"
    )
    p.add_argument("--milestone", type=str, default=None,
                   help="Filtrar por milestone QLEP (F0.1..F0.8)")
    p.add_argument("--sigla", type=str, default=None,
                   help="Filtrar por sigla de norma (CE, LOTAIP, COOTAD...)")
    p.add_argument("--status", action="store_true",
                   help="Mostrar estadísticas actuales y salir")
    p.add_argument("--dry-run", action="store_true",
                   help="Mostrar qué se ingestionaría sin escribir en DB")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    if args.status:
        print("\n[STATUS] normativa_corpus —")
        cmd_status()
        sys.exit(0)

    ingest(
        milestone=args.milestone,
        sigla=args.sigla,
        dry_run=args.dry_run,
    )
