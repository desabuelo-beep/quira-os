# -*- coding: utf-8 -*-
"""
backup_corpus.py — Backup completo de normativa_corpus antes de tocar Supabase
QUIRA Gov · Dylus Lab © 2026

Exporta TODA la tabla (incluidos embeddings) a un .jsonl local, con streaming por lotes para
no cargar los 13k+ registros en memoria de golpe. No hay pg_dump disponible en este entorno,
así que este es el mecanismo de reversibilidad antes de cualquier DELETE/reingesta (colega
2026-07-21: "backup completo del corpus normativo" — paso 7 del plan).

Uso:
  python scripts/normativa/backup_corpus.py            # backup completo
  python scripts/normativa/backup_corpus.py --restore data/backups/normativa_corpus_YYYYMMDD.jsonl
"""
from __future__ import annotations

import json
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent.parent
SECRETS = REPO / ".streamlit" / "secrets.toml"
BACKUP_DIR = REPO / "data" / "backups"
COLUMNAS = ["id", "norma_sigla", "norma_nombre", "jerarquia", "milestone_qlep", "tipo_documento",
            "articulo_num", "articulo_raw", "chunk_seq", "contenido", "palabras", "dominios_quira",
            "sha256", "embedding", "archivo_nombre", "archivo_sha256", "ingestado_at",
            "ingestado_por", "document_id", "document_class", "authority_level", "source_entity",
            "canton_id", "circuit_refs", "evidence_type", "metadata_json"]


def _uri() -> str:
    return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]


def backup() -> Path:
    import psycopg2
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = BACKUP_DIR / f"normativa_corpus_{ts}.jsonl"

    conn = psycopg2.connect(_uri(), connect_timeout=30)
    cur = conn.cursor(name="backup_cursor")  # server-side cursor: no carga todo en memoria
    cur.itersize = 500
    cols_sql = ", ".join(COLUMNAS)
    cur.execute(f"SELECT {cols_sql} FROM public.normativa_corpus ORDER BY id")

    n = 0
    with open(out, "w", encoding="utf-8") as f:
        for row in cur:
            rec = dict(zip(COLUMNAS, row))
            # embedding viene como string "[0.1,0.2,...]" o Vector — normalizar a str para JSON
            if rec.get("embedding") is not None:
                rec["embedding"] = str(rec["embedding"])
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
            n += 1
            if n % 2000 == 0:
                print(f"  ... {n} filas exportadas")
    conn.close()
    print(f"OK — backup completo: {n} filas → {out.relative_to(REPO)}")
    return out


def restore(path: str) -> None:
    """Restaura el backup completo: TRUNCATE + reinsertar todas las filas. Solo para emergencia
    (si la reingesta en modo REPLACE deja el corpus en un estado peor que el original)."""
    import psycopg2
    p = Path(path)
    if not p.exists():
        print(f"[ERR] no existe el backup: {p}"); return
    conn = psycopg2.connect(_uri(), connect_timeout=30)
    cur = conn.cursor()
    print(f"RESTAURANDO desde {p.name} — esto reemplaza TODA la tabla actual.")
    cur.execute("TRUNCATE public.normativa_corpus RESTART IDENTITY")
    cols_sql = ", ".join(COLUMNAS)
    idx_emb = COLUMNAS.index("embedding")
    placeholders = ", ".join("%s::vector" if i == idx_emb else "%s" for i in range(len(COLUMNAS)))
    n = 0
    with open(p, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            vals = [rec.get(c) for c in COLUMNAS]
            cur.execute(
                f"INSERT INTO public.normativa_corpus ({cols_sql}) VALUES ({placeholders})",
                vals,
            )
            n += 1
            if n % 2000 == 0:
                conn.commit()
                print(f"  ... {n} filas restauradas")
    conn.commit()
    conn.close()
    print(f"OK — restauradas {n} filas desde el backup.")


if __name__ == "__main__":
    if "--restore" in sys.argv:
        idx = sys.argv.index("--restore")
        restore(sys.argv[idx + 1])
    else:
        backup()
