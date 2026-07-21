# -*- coding: utf-8 -*-
"""
reingesta_replace.py — Reingesta en modo REPLACE, documento por documento
QUIRA Gov · Dylus Lab © 2026

Por qué existe (hallazgo 2026-07-21, confirmado por el colega): `ingest.py` es puramente
ADITIVO (`ON CONFLICT (sha256) DO NOTHING`). Como el parser cambió (captura disposiciones,
corrige la ancla LOPC, filtra referencias cruzadas), el contenido — y por tanto el SHA — de
cada chunk es distinto al que ya está en Supabase. Una "reingesta" simple NO reemplazaría los
chunks viejos: los DUPLICARÍA semánticamente (mismo artículo, dos veces, con distinto corte).

Plan del colega (2026-07-21):
  1. Manifiesto de reemplazo ANTES de tocar nada (trazabilidad: chunks actuales/nuevos,
     SHA antiguos/nuevos, fecha, versión parser, versión corpus).
  2. Modo --replace TRANSACCIONAL POR DOCUMENTO (BEGIN → DELETE sigla → INSERT nuevos →
     COMMIT). NUNCA `DELETE` de toda la tabla. Si un documento falla, ROLLBACK de ESE
     documento — los anteriores ya quedaron consistentes.

Uso:
  python scripts/normativa/reingesta_replace.py --manifiesto     # dry-run, no toca Supabase
  python scripts/normativa/reingesta_replace.py --replace        # ejecuta transaccional
  python scripts/normativa/reingesta_replace.py --replace --sigla LOPC   # solo una sigla
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent.parent
SECRETS = REPO / ".streamlit" / "secrets.toml"
WORD_DIR = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Normativa_Word")
MANIFIESTO_PATH = REPO / "docs" / "architecture" / "MANIFIESTO_REEMPLAZO_CORPUS.json"

sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).parent))
from manifest import MANIFEST                       # noqa: E402
from chunker import chunk_docx_with_meta             # noqa: E402


def _uri() -> str:
    return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]


def _parser_version() -> str:
    try:
        r = subprocess.run(["git", "describe", "--tags", "--exact-match"],
                          cwd=REPO, capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return r.stdout.strip()
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                          cwd=REPO, capture_output=True, text=True, timeout=10)
        return f"HEAD@{r.stdout.strip()}"
    except Exception:
        return "desconocida"


def generar_manifiesto() -> dict:
    """Manifiesto de reemplazo (dry-run): compara para CADA documento del manifiesto lo que YA
    hay en Supabase contra lo que el parser congelado generaría. NO toca la base de datos."""
    import psycopg2
    cur = psycopg2.connect(_uri(), connect_timeout=30).cursor()
    entradas = []
    for m in MANIFEST:
        sigla = m["sigla"]
        f = WORD_DIR / m["archivo"]
        cur.execute("SELECT sha256 FROM public.normativa_corpus WHERE norma_sigla=%s ORDER BY id", (sigla,))
        sha_actuales = [r[0] for r in cur.fetchall()]
        if not f.exists():
            entradas.append({"sigla": sigla, "estado": "ARCHIVO_FALTANTE",
                             "chunks_actuales": len(sha_actuales), "chunks_nuevos": None})
            continue
        try:
            rows_nuevos = chunk_docx_with_meta(str(f), m)
        except Exception as e:
            entradas.append({"sigla": sigla, "estado": f"ERROR_PARSER: {str(e)[:80]}",
                             "chunks_actuales": len(sha_actuales), "chunks_nuevos": None})
            continue
        sha_nuevos = [r["sha256"] for r in rows_nuevos]
        idénticos = set(sha_actuales) == set(sha_nuevos)
        entradas.append({
            "sigla": sigla,
            "estado": "SIN_CAMBIOS" if idénticos else "REEMPLAZO_NECESARIO",
            "chunks_actuales": len(sha_actuales),
            "chunks_nuevos": len(rows_nuevos),
            "sha_actuales_no_en_nuevos": len(set(sha_actuales) - set(sha_nuevos)),
            "sha_nuevos_no_en_actuales": len(set(sha_nuevos) - set(sha_actuales)),
        })
        print(f"  {'=' if idénticos else '≠'} {sigla:22} actuales={len(sha_actuales):4} "
              f"nuevos={len(rows_nuevos):4} {'(sin cambios)' if idénticos else '(REEMPLAZAR)'}")
    manifiesto = {
        "generado": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "version_parser": _parser_version(),
        "version_corpus_previa": "pre-v1.0 (sin congelar)",
        "total_documentos": len(entradas),
        "requieren_reemplazo": sum(1 for e in entradas if e["estado"] == "REEMPLAZO_NECESARIO"),
        "documentos": entradas,
    }
    MANIFIESTO_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFIESTO_PATH.write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nManifiesto escrito: {MANIFIESTO_PATH.relative_to(REPO)}")
    print(f"{manifiesto['requieren_reemplazo']} de {manifiesto['total_documentos']} documentos "
          f"requieren reemplazo (parser {manifiesto['version_parser']})")
    return manifiesto


def replace_documento(sigla: str, entry: dict, model) -> tuple[bool, str]:
    """BEGIN → DELETE WHERE norma_sigla=X → INSERT nuevos (con embedding) → COMMIT.
    Si algo falla: ROLLBACK de ESTE documento únicamente — los ya procesados quedan intactos."""
    import psycopg2
    f = WORD_DIR / entry["archivo"]
    if not f.exists():
        return False, "archivo faltante"
    try:
        rows = chunk_docx_with_meta(str(f), entry)
    except Exception as e:
        return False, f"error de parseo: {str(e)[:80]}"
    if not rows:
        return False, "el parser no generó chunks"

    texts = [r["contenido"] for r in rows]
    embeddings = []
    for i in range(0, len(texts), 32):
        embeddings.extend(v.tolist() for v in model.encode(texts[i:i + 32], convert_to_numpy=True, show_progress_bar=False))

    conn = psycopg2.connect(_uri(), connect_timeout=30)
    conn.autocommit = False
    cur = conn.cursor()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        cur.execute("DELETE FROM public.normativa_corpus WHERE norma_sigla=%s", (sigla,))
        borrados = cur.rowcount
        for r, emb in zip(rows, embeddings):
            emb_str = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
            cur.execute("""
                INSERT INTO public.normativa_corpus
                    (norma_sigla, norma_nombre, jerarquia, milestone_qlep, tipo_documento,
                     articulo_num, articulo_raw, chunk_seq, contenido, palabras, dominios_quira,
                     sha256, embedding, archivo_nombre, archivo_sha256, ingestado_at, ingestado_por)
                VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, %s,%s::vector,%s,%s, %s,%s)
                ON CONFLICT (sha256) DO NOTHING
            """, (r["norma_sigla"], r["norma_nombre"], r["jerarquia"], r["milestone_qlep"],
                  r["tipo_documento"], r.get("articulo_num"), r.get("articulo_raw"),
                  r["chunk_seq"], r["contenido"], r["palabras"], r["dominios_quira"],
                  r["sha256"], emb_str, r["archivo_nombre"], "", now, "reingesta-replace-v1.0"))
        conn.commit()
        return True, f"{borrados} borrados → {len(rows)} insertados"
    except Exception as e:
        conn.rollback()
        return False, f"ROLLBACK: {str(e)[:100]}"
    finally:
        conn.close()


def ejecutar_replace(solo_sigla: str | None = None) -> None:
    from sentence_transformers import SentenceTransformer
    print("Cargando modelo de embeddings...")
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    entries = [m for m in MANIFEST if not solo_sigla or m["sigla"] == solo_sigla]
    print(f"REEMPLAZO TRANSACCIONAL — {len(entries)} documento(s), uno a la vez\n")
    ok, fallos = 0, []
    for m in entries:
        exito, detalle = replace_documento(m["sigla"], m, model)
        print(f"  {'✅' if exito else '❌'} {m['sigla']:22} {detalle}")
        if exito:
            ok += 1
        else:
            fallos.append(m["sigla"])
    print(f"\n{ok}/{len(entries)} documentos reemplazados. "
          f"{'Fallaron: ' + str(fallos) if fallos else 'Sin fallos.'}")


if __name__ == "__main__":
    if "--manifiesto" in sys.argv:
        generar_manifiesto()
    elif "--replace" in sys.argv:
        sigla = None
        if "--sigla" in sys.argv:
            sigla = sys.argv[sys.argv.index("--sigla") + 1]
        ejecutar_replace(sigla)
    else:
        print("Uso: --manifiesto (dry-run) | --replace [--sigla SIGLA]")
