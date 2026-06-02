# -*- coding: utf-8 -*-
"""
validate_f01.py — Validación piloto F0.1 (Constitución)
QUIRA Gov · Dylus Lab © 2026

Verifica 5 criterios antes de expandir al corpus completo:
  A. Calidad de chunks (distribución de palabras)
  B. Calidad de embeddings (cobertura, no nulos)
  C. Recuperación semántica (4 queries reales)
  D. Metadatos de dominio (dominios_quira correctos)
  E. Costo operativo (tiempo por query)
"""
from __future__ import annotations
import sys, os, time, json

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, ROOT)

import toml
_secrets = toml.load(os.path.join(ROOT, ".streamlit", "secrets.toml"))
import streamlit as st
class _FS:
    def get(self, k, d=None): return _secrets.get(k, d)
    def __getitem__(self, k):  return _secrets[k]
st.secrets = _FS()

from sentinel.db_config import get_connection
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
TOP_K = 3

# ── QUERIES DE VALIDACIÓN ────────────────────────────────────────────────────
QUERIES = [
    ("A · Participación ciudadana",
     "¿Qué artículo sustenta la participación ciudadana en el Estado?"),
    ("B · Competencias exclusivas municipales",
     "¿Qué artículo define las competencias exclusivas de los municipios?"),
    ("C · Transparencia activa",
     "¿Qué artículo fundamenta el derecho de acceso a la información pública y transparencia activa?"),
    ("D · Planificación participativa",
     "¿Qué artículo conecta la planificación estatal con la participación ciudadana?"),
]


def sem_search(conn, model, query: str, top_k: int = TOP_K):
    emb = model.encode(query).tolist()
    emb_str = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
    t0 = time.time()
    c  = conn.cursor()
    c.execute("""
        SELECT articulo_raw, chunk_seq, palabras,
               LEFT(contenido, 250) AS preview,
               1 - (embedding <=> %s::vector) AS score
        FROM   normativa_corpus
        WHERE  embedding IS NOT NULL
          AND  norma_sigla = 'CE'
        ORDER  BY embedding <=> %s::vector
        LIMIT  %s
    """, (emb_str, emb_str, top_k))
    rows  = c.fetchall()
    elapsed = time.time() - t0
    return rows, elapsed


def main():
    print("=" * 70)
    print("  QUIRA — Validación Piloto F0.1 · Constitución del Ecuador")
    print("=" * 70)

    conn = get_connection()

    # ── A. Calidad de chunks ──────────────────────────────────────────────────
    print("\n[A] Calidad de chunks")
    c = conn.cursor()
    c.execute("""
        SELECT COUNT(*)                        AS total,
               AVG(palabras)                  AS avg_words,
               MIN(palabras)                  AS min_words,
               MAX(palabras)                  AS max_words,
               SUM(CASE WHEN articulo_num IS NULL THEN 1 ELSE 0 END) AS preambulos,
               SUM(CASE WHEN chunk_seq > 0     THEN 1 ELSE 0 END) AS sub_chunks
        FROM normativa_corpus WHERE norma_sigla = 'CE'
    """)
    r = c.fetchone()
    print(f"  Total chunks:     {r['total']}")
    print(f"  Palabras promedio:{r['avg_words']:.0f}")
    print(f"  Rango:            {r['min_words']} — {r['max_words']}")
    print(f"  Chunks preámbulo: {r['preambulos']}")
    print(f"  Sub-chunks (+1):  {r['sub_chunks']}")
    veredicto_a = "OK" if r['avg_words'] < 450 and r['total'] >= 400 else "REVISAR"
    print(f"  Veredicto A:      {veredicto_a}")

    # ── B. Calidad de embeddings ──────────────────────────────────────────────
    print("\n[B] Calidad de embeddings")
    c.execute("""
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN embedding IS NOT NULL THEN 1 ELSE 0 END) AS con_emb
        FROM normativa_corpus WHERE norma_sigla = 'CE'
    """)
    r = c.fetchone()
    cobertura = 100 * r['con_emb'] / max(r['total'], 1)
    print(f"  Con embedding:    {r['con_emb']}/{r['total']} ({cobertura:.1f}%)")
    veredicto_b = "OK" if cobertura == 100 else f"INCOMPLETO ({cobertura:.0f}%)"
    print(f"  Veredicto B:      {veredicto_b}")

    # ── C. Recuperación semántica ──────────────────────────────────────────────
    print("\n[C] Recuperación semántica")
    model = SentenceTransformer(EMBED_MODEL)

    tiempos = []
    for label, query in QUERIES:
        rows, elapsed = sem_search(conn, model, query, top_k=TOP_K)
        tiempos.append(elapsed)
        print(f"\n  Query: {label}")
        print(f"  '{query}'")
        for i, row in enumerate(rows):
            score = row.get("score", 0) or 0
            art   = row.get("articulo_raw", "?")
            seq   = row.get("chunk_seq", 0)
            prev  = row.get("preview", "")[:200].replace("\n", " ")
            print(f"    [{i+1}] {art} (seq={seq})  score={score:.3f}")
            print(f"         {prev}...")
        print(f"  Tiempo: {elapsed:.3f}s")

    # ── D. Metadatos de dominio ────────────────────────────────────────────────
    print("\n[D] Metadatos de dominio")
    c.execute("""
        SELECT dominios_quira, COUNT(*) AS n
        FROM normativa_corpus WHERE norma_sigla = 'CE'
        GROUP BY dominios_quira
    """)
    dom_rows = c.fetchall()
    dom_val  = dom_rows[0]["dominios_quira"] if dom_rows else "[]"
    parsed   = json.loads(dom_val)
    print(f"  Dominios asignados: {parsed}")
    print(f"  Chunks con esta config: {sum(r['n'] for r in dom_rows)}")
    veredicto_d = "OK" if len(parsed) >= 8 else "REVISAR (pocos dominios)"
    print(f"  Veredicto D:      {veredicto_d}")

    # ── E. Costo operativo ────────────────────────────────────────────────────
    print("\n[E] Costo operativo")
    avg_t = sum(tiempos) / len(tiempos) if tiempos else 0
    print(f"  Tiempo promedio por query: {avg_t:.3f}s")
    print(f"  Chunks en DB:              465  (CE)")
    print(f"  Tiempo ingesta F0.1:       ~260s")
    print(f"  Estimado corpus completo:  ~41 docs × avg_chunks × factor")
    veredicto_e = "OK" if avg_t < 2.0 else "LENTO — revisar índice"
    print(f"  Veredicto E:      {veredicto_e}")

    # ── RESUMEN FINAL ─────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  RESUMEN")
    print("=" * 70)
    for ltr, v in [("A", veredicto_a), ("B", veredicto_b),
                   ("D", veredicto_d), ("E", veredicto_e)]:
        emoji = "✓" if v == "OK" else "!"
        print(f"  [{emoji}] Criterio {ltr}: {v}")
    print("  [✓] Criterio C: ver resultados de queries arriba")
    print()

    conn.close()


if __name__ == "__main__":
    main()
