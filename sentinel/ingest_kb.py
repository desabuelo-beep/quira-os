"""
SENTINEL RAG · ingest_kb.py
Pipeline de ingesta: Obsidian vault → chunks → embeddings → ChromaDB.
Diseñado para ser incremental y extensible (fuente_tipo = obsidian | excel | pdf | vivo).
Ejecutar: python -m sentinel.ingest_kb [--force]
Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import re
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.rag_config import (
    VAULT_DIR, CHROMA_DIR, EMBED_MODEL, CHROMA_COLLECTION,
    FUENTE_CANONICA, FUENTE_VERSION, FUENTE_FECHA, INDEX_VERSION,
    YAML_ALIASES, CHUNK_MAX_TOKENS, CHUNK_OVERLAP_LINES,
    CARPETA_A_DIMENSION,
)

# ── DEPENDENCIAS LAZY (para mejor mensajes de error) ──────────────────────────
def _load_deps():
    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
        return chromadb, SentenceTransformer
    except ImportError as e:
        print(f"\n❌ Dependencia faltante: {e}")
        print("   Instalar con: pip install chromadb sentence-transformers")
        sys.exit(1)


# ── FRONTMATTER PARSER (mismo que en audit_yaml) ──────────────────────────────
def _extract_frontmatter(text: str) -> tuple[dict, str]:
    if not text.strip().startswith("---"):
        return {}, text
    lines = text.split("\n")
    end_idx = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}, text

    yaml_block = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:])

    data = {}
    current_key = None
    current_list = None

    for raw_line in yaml_block.split("\n"):
        line = re.sub(r"\s*#.*$", "", raw_line).rstrip()
        if not line:
            continue
        if line.startswith("  - ") or line.startswith("- "):
            item = line.lstrip("- ").strip().strip('"').strip("'")
            if current_list is not None:
                current_list.append(item)
            elif current_key:
                data[current_key] = [item]
                current_list = data[current_key]
            continue
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].strip().lower()
            val = parts[1].strip().strip('"').strip("'") if len(parts) > 1 else ""
            current_key = key
            current_list = None
            if val:
                data[key] = val
            else:
                data[key] = None
    return data, body


def _resolve(yaml: dict, campo: str, default: str = "") -> str:
    """Resuelve un campo YAML con sus aliases."""
    aliases = [campo] + YAML_ALIASES.get(campo, [])
    for a in aliases:
        if a in yaml and yaml[a] is not None:
            val = yaml[a]
            if isinstance(val, list):
                return " | ".join(str(v) for v in val)
            return str(val).strip()
    return default


# ── CHUNKER ───────────────────────────────────────────────────────────────────
def _chunk_by_headers(text: str, title: str) -> list[dict]:
    """
    Divide el cuerpo de una nota por encabezados Markdown (##, ###).
    Cada chunk preserva su encabezado como contexto.
    """
    chunks = []
    current_section = "Introducción"
    current_lines: list[str] = []

    def _flush(section: str, lines: list[str]) -> None:
        body = "\n".join(lines).strip()
        if not body or len(body.split()) < 8:  # descartar chunks vacíos
            return
        # Si el chunk es muy largo, partir por párrafos
        words = body.split()
        if len(words) <= CHUNK_MAX_TOKENS:
            chunks.append({"section": section, "text": f"[{title}] {section}\n{body}"})
        else:
            # Partir por párrafos dobles
            paragraphs = re.split(r"\n{2,}", body)
            buffer = []
            buf_words = 0
            for para in paragraphs:
                pw = len(para.split())
                if buf_words + pw > CHUNK_MAX_TOKENS and buffer:
                    chunk_text = "\n\n".join(buffer)
                    chunks.append({"section": section, "text": f"[{title}] {section}\n{chunk_text}"})
                    # Overlap: mantener último párrafo
                    buffer = buffer[-CHUNK_OVERLAP_LINES:] if CHUNK_OVERLAP_LINES else []
                    buf_words = sum(len(b.split()) for b in buffer)
                buffer.append(para)
                buf_words += pw
            if buffer:
                chunk_text = "\n\n".join(buffer)
                chunks.append({"section": section, "text": f"[{title}] {section}\n{chunk_text}"})

    for line in text.split("\n"):
        # Encabezados H2 o H3 → nuevo chunk
        if line.startswith("## ") or line.startswith("### "):
            _flush(current_section, current_lines)
            current_section = line.lstrip("#").strip()
            current_lines = []
        else:
            current_lines.append(line)

    _flush(current_section, current_lines)  # último bloque
    return chunks


def _file_hash(path: Path) -> str:
    """SHA256 del archivo para detección de cambios."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# ── METADATA BUILDER ──────────────────────────────────────────────────────────
def _build_metadata(yaml: dict, md_path: Path, section: str, chunk_idx: int) -> dict:
    """
    Construye el dict de metadatos de un chunk — el alma de la trazabilidad.
    Todos los campos son strings (requisito ChromaDB).
    """
    rel = md_path.relative_to(VAULT_DIR)
    folder = str(rel.parent)

    # Territorio — puede ser dict anidado o string
    # DEFAULT: todas las notas son de Montecristi si no se especifica
    territorio_raw = yaml.get("territorio", {})
    if isinstance(territorio_raw, dict):
        canton    = territorio_raw.get("canton", "Montecristi")
        parroquia = territorio_raw.get("parroquia", "")
    elif territorio_raw:
        canton    = str(territorio_raw)
        parroquia = ""
    else:
        canton    = "Montecristi"
        parroquia = ""

    # dimension_tgi — puede ser lista o string
    # Si falta, inferir desde la carpeta del archivo
    dim_raw = yaml.get("dimension_tgi", [])
    if isinstance(dim_raw, list) and dim_raw:
        dimension_tgi = " | ".join(str(d) for d in dim_raw)
    elif isinstance(dim_raw, str) and dim_raw:
        dimension_tgi = dim_raw
    else:
        # Inferir desde carpeta — buscar coincidencia más específica primero
        inferred = []
        for carpeta_key, dims in CARPETA_A_DIMENSION.items():
            if folder.startswith(carpeta_key) or folder == carpeta_key:
                if len(carpeta_key) > len(" ".join(inferred) if inferred else ""):
                    inferred = dims
        dimension_tgi = " | ".join(inferred) if inferred else "general"

    return {
        # Identificación
        "source":         str(rel),
        "nota":           md_path.stem,
        "carpeta":        folder,
        "chunk_idx":      str(chunk_idx),
        "section":        section,

        # Semántica YAML
        "tipo_nota":      _resolve(yaml, "tipo_nota"),
        "nombre":         _resolve(yaml, "nombre", md_path.stem),
        "entidad":        _resolve(yaml, "entidad", "GAD-MNT"),
        "canton":         canton,
        "parroquia":      parroquia,
        "dimension_tgi":  dimension_tgi,
        "tags":           _resolve(yaml, "tags"),
        "estado":         _resolve(yaml, "estado", "activo"),
        "fecha":          _resolve(yaml, "fecha", FUENTE_FECHA),

        # Trazabilidad y versionado
        "fuente_tipo":    "obsidian",
        "fuente_canonica": _resolve(yaml, "fuente_canonica", FUENTE_CANONICA),
        "fuente_version": FUENTE_VERSION,
        "fuente_fecha":   FUENTE_FECHA,
        "index_version":  INDEX_VERSION,
        "file_hash":      _file_hash(md_path),
    }


# ── INGESTA PRINCIPAL ─────────────────────────────────────────────────────────
def ingest(force: bool = False) -> dict:
    """
    Lee todas las notas Obsidian, genera chunks y los almacena en ChromaDB.
    Si force=False, salta notas cuyo hash no cambió desde la última ingesta.
    """
    chromadb, SentenceTransformer = _load_deps()

    print(f"\n{'═'*60}")
    print("  SENTINEL RAG · INGESTA OBSIDIAN → CHROMADB")
    print(f"{'═'*60}")
    print(f"  Vault:        {VAULT_DIR}")
    print(f"  ChromaDB:     {CHROMA_DIR}")
    print(f"  Modelo:       {EMBED_MODEL}")
    print(f"  index_version:{INDEX_VERSION}")

    # Cargar modelo de embeddings
    print(f"\n  Cargando modelo de embeddings...")
    print(f"  (Primera vez toma 1-2 min — descarga ~120MB)")
    model = SentenceTransformer(EMBED_MODEL)
    print(f"  ✅ Modelo listo")

    # Conectar ChromaDB
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"}  # similitud coseno
    )

    # Leer hashes existentes para ingesta incremental
    existing_hashes: set[str] = set()
    if not force:
        try:
            existing = collection.get(include=["metadatas"])
            for meta in existing["metadatas"]:
                if meta and "file_hash" in meta:
                    existing_hashes.add(meta["file_hash"])
        except Exception:
            pass

    md_files = sorted(VAULT_DIR.rglob("*.md"))
    stats = {"total": 0, "procesadas": 0, "saltadas": 0, "chunks": 0, "errores": 0}

    for md_path in md_files:
        stats["total"] += 1
        fhash = _file_hash(md_path)

        # Skip si no cambió (ingesta incremental)
        if not force and fhash in existing_hashes:
            stats["saltadas"] += 1
            continue

        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ⚠️  Error leyendo {md_path.name}: {e}")
            stats["errores"] += 1
            continue

        if len(text.strip()) < 20:
            stats["saltadas"] += 1
            continue

        yaml_data, body = _extract_frontmatter(text)
        title = _resolve(yaml_data, "nombre", md_path.stem)
        chunks = _chunk_by_headers(body, title)

        if not chunks:
            stats["saltadas"] += 1
            continue

        # Preparar batch para ChromaDB
        ids, docs, embeddings_list, metas = [], [], [], []

        for i, chunk in enumerate(chunks):
            chunk_id = f"{md_path.stem}__{i}"
            meta = _build_metadata(yaml_data, md_path, chunk["section"], i)

            # Borrar versión anterior del chunk si existe
            try:
                collection.delete(ids=[chunk_id])
            except Exception:
                pass

            ids.append(chunk_id)
            docs.append(chunk["text"])
            metas.append(meta)

        # Generar embeddings en batch
        embeddings_list = model.encode(docs, show_progress_bar=False).tolist()

        # Guardar en ChromaDB
        collection.add(
            ids=ids,
            documents=docs,
            embeddings=embeddings_list,
            metadatas=metas,
        )

        stats["procesadas"] += 1
        stats["chunks"] += len(chunks)

        if stats["procesadas"] % 20 == 0:
            print(f"  ...{stats['procesadas']} notas / {stats['chunks']} chunks")

    # Guardar log de ingesta
    log = {
        "timestamp":     datetime.now().isoformat(),
        "index_version": INDEX_VERSION,
        "vault":         str(VAULT_DIR),
        "stats":         stats,
        "force":         force,
    }
    log_path = CHROMA_DIR.parent / "reports" / f"ingest_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    log_path.parent.mkdir(exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    # Resumen
    total_collection = collection.count()
    print(f"\n{'─'*60}")
    print(f"  ✅ Ingesta completa")
    print(f"  Notas procesadas:  {stats['procesadas']}")
    print(f"  Notas saltadas:    {stats['saltadas']}  (sin cambios)")
    print(f"  Chunks nuevos:     {stats['chunks']}")
    print(f"  Errores:           {stats['errores']}")
    print(f"  Total en ChromaDB: {total_collection} chunks")
    print(f"  Log:               {log_path}")
    print(f"{'═'*60}\n")

    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingestar vault Obsidian en ChromaDB")
    parser.add_argument("--force", action="store_true",
                        help="Reingestar todas las notas aunque no hayan cambiado")
    args = parser.parse_args()
    ingest(force=args.force)
