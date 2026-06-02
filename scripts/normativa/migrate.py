# -*- coding: utf-8 -*-
"""
migrate.py — Crear tabla normativa_corpus en Supabase (pgvector)
QUIRA Gov · Corpus Normativo Ecuatoriano · Dylus Lab © 2026

Idempotente: se puede re-ejecutar sin efectos secundarios.
Requiere: extensión pgvector habilitada en Supabase (está por defecto).
"""

import sys
import os

# ── Path setup ────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

# ── Parchear st.secrets para ejecutar fuera de Streamlit ─────────────────────
import toml
_secrets_path = os.path.join(
    os.path.dirname(__file__), "..", "..", ".streamlit", "secrets.toml"
)
_raw_secrets = toml.load(_secrets_path)

import streamlit as st
class _FakeSecrets:
    def get(self, k, d=None):  return _raw_secrets.get(k, d)
    def __getitem__(self, k):  return _raw_secrets[k]
st.secrets = _FakeSecrets()

# ── QUIRA OS imports ──────────────────────────────────────────────────────────
from sentinel.db_config import get_connection


# ── ESQUEMA normativa_corpus ──────────────────────────────────────────────────
# PostgreSQL / Supabase (pgvector).
# Para SQLite local: embedding guardado como TEXT (JSON array).

_SQL_SUPABASE = """
-- Extensión pgvector (idempotente)
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal
CREATE TABLE IF NOT EXISTS normativa_corpus (
    id              SERIAL PRIMARY KEY,

    -- Identidad del documento
    norma_sigla     TEXT    NOT NULL,
    norma_nombre    TEXT    NOT NULL,
    jerarquia       INTEGER NOT NULL,
    milestone_qlep  TEXT    NOT NULL,
    tipo_documento  TEXT    NOT NULL,

    -- Identidad del chunk
    articulo_num    INTEGER,
    articulo_raw    TEXT,
    chunk_seq       INTEGER NOT NULL DEFAULT 0,

    -- Contenido
    contenido       TEXT    NOT NULL,
    palabras        INTEGER NOT NULL DEFAULT 0,

    -- Dominios QUIRA (JSON array como TEXT)
    dominios_quira  TEXT    NOT NULL DEFAULT '[]',

    -- Deduplicación
    sha256          TEXT    NOT NULL UNIQUE,

    -- Embedding vectorial (384 dimensiones — MiniLM L12 v2)
    embedding       vector(384),

    -- Archivo fuente
    archivo_nombre  TEXT    NOT NULL,
    archivo_sha256  TEXT    NOT NULL DEFAULT '',

    -- Auditoría
    ingestado_at    TEXT    NOT NULL,
    ingestado_por   TEXT    NOT NULL DEFAULT 'qlep-corpus-v1.0'
);

-- Índice semántico (búsqueda aproximada por coseno)
-- lists=50 es apropiado para <100k filas
CREATE INDEX IF NOT EXISTS idx_normativa_embedding
    ON normativa_corpus
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);

-- Índices de filtrado
CREATE INDEX IF NOT EXISTS idx_normativa_sigla
    ON normativa_corpus (norma_sigla);

CREATE INDEX IF NOT EXISTS idx_normativa_milestone
    ON normativa_corpus (milestone_qlep);

CREATE INDEX IF NOT EXISTS idx_normativa_jerarquia
    ON normativa_corpus (jerarquia);
"""

# SQLite fallback (sin pgvector — embedding como TEXT JSON)
_SQL_SQLITE = """
CREATE TABLE IF NOT EXISTS normativa_corpus (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    norma_sigla     TEXT    NOT NULL,
    norma_nombre    TEXT    NOT NULL,
    jerarquia       INTEGER NOT NULL,
    milestone_qlep  TEXT    NOT NULL,
    tipo_documento  TEXT    NOT NULL,
    articulo_num    INTEGER,
    articulo_raw    TEXT,
    chunk_seq       INTEGER NOT NULL DEFAULT 0,
    contenido       TEXT    NOT NULL,
    palabras        INTEGER NOT NULL DEFAULT 0,
    dominios_quira  TEXT    NOT NULL DEFAULT '[]',
    sha256          TEXT    NOT NULL UNIQUE,
    embedding       TEXT,
    archivo_nombre  TEXT    NOT NULL,
    archivo_sha256  TEXT    NOT NULL DEFAULT '',
    ingestado_at    TEXT    NOT NULL,
    ingestado_por   TEXT    NOT NULL DEFAULT 'qlep-corpus-v1.0'
);
CREATE INDEX IF NOT EXISTS idx_normativa_sigla     ON normativa_corpus (norma_sigla);
CREATE INDEX IF NOT EXISTS idx_normativa_milestone ON normativa_corpus (milestone_qlep);
"""


def run_migration() -> None:
    conn = get_connection()
    mode = conn.mode
    print(f"Modo de base de datos: {mode}")

    if mode == "supabase":
        # PostgreSQL: ejecutar sentencias separadas
        stmts = [s.strip() for s in _SQL_SUPABASE.split(";") if s.strip()]
        c = conn.cursor()
        for stmt in stmts:
            try:
                c.execute(stmt)
                conn.commit()
            except Exception as exc:
                # Errores de "ya existe" son normales (idempotente)
                err = str(exc).lower()
                if any(x in err for x in ["already exists", "duplicate"]):
                    conn.commit()  # limpiar estado de error
                    print(f"  [SKIP] Ya existía: {stmt[:60]}...")
                else:
                    print(f"  [ERR]  {exc}")
                    conn.commit()
    else:
        # SQLite: ejecutar todo junto
        for stmt in _SQL_SQLITE.split(";"):
            stmt = stmt.strip()
            if stmt:
                try:
                    conn.execute(stmt)
                    conn.commit()
                except Exception as exc:
                    print(f"  [ERR] {exc}")

    conn.close()

    print("\nMigración completada.")
    print("  Tabla:   normativa_corpus")
    if mode == "supabase":
        print("  Índice:  idx_normativa_embedding (ivfflat coseno, lists=50)")
    print("  Ready para ingesta.")


# ── VERIFICACIÓN ──────────────────────────────────────────────────────────────
def verify() -> None:
    conn = get_connection()
    c    = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) AS n FROM normativa_corpus")
        row = c.fetchone()
        n   = row["n"] if row else 0
        print(f"\nVerificación OK — normativa_corpus existe · {n} filas actuales")
    except Exception as exc:
        print(f"\nVerificación FALLIDA: {exc}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  QUIRA — Migración normativa_corpus")
    print("=" * 60)
    run_migration()
    verify()
    print("=" * 60)
