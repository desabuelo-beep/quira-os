# -*- coding: utf-8 -*-
"""
chunker.py — DOCX → chunks artículo-nivel
QUIRA Gov · Corpus Normativo Ecuatoriano · Dylus Lab © 2026

Lee un archivo DOCX y lo segmenta en chunks artículo-nivel usando patrones
regex adaptados a la estructura del derecho ecuatoriano.

Algoritmo:
  1. Extraer texto plano del DOCX (párrafos concatenados)
  2. Detectar límites de artículo con regex canónico
  3. Para artículos >450 palabras → dividir en sub-chunks con overlap
  4. El preámbulo (antes del Art. 1) → chunk especial tipo PREÁMBULO

Dependencias: python-docx
"""

from __future__ import annotations

import re
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ── REGEX CANÓNICO — LÍMITES DE ARTÍCULO ─────────────────────────────────────
# Soporta:
#   Art. 226.-    Art. 226.    Art. 226 —
#   Artículo 226.-   ARTÍCULO 226.-
#   Art. 226A.-   Art. 226.1.-   (artículos innumerados o con sufijo)
#   Art. único.-  Art. innumerado.-
#
ARTICLE_RE = re.compile(
    r"(?:^|\n)\s*"
    r"(?:"
    r"Art(?:í|i|Í|I)cul(?:o|a|os|as)?s?\.\s*"
    r"|ARTÍCULO\s+"
    r"|Art\.\s*"
    r")"
    r"("
    r"\d+(?:\.\d+)?(?:\s*[A-Za-záéíóúÁÉÍÓÚ]+)?"  # 226 / 226.1 / 226A
    r"|único|innumerado|\w+"                          # único / innumerado
    r")\s*[\.\-–—·]?",
    re.IGNORECASE | re.MULTILINE,
)

# Límite de palabras por chunk (alineado con CHUNK_MAX_TOKENS del RAG config)
CHUNK_MAX_WORDS = 450

# Overlap entre sub-chunks (en líneas)
CHUNK_OVERLAP_LINES = 2


@dataclass
class ArticleChunk:
    """Un chunk = un artículo (o sub-artículo si supera CHUNK_MAX_WORDS)."""
    articulo_num:   Optional[int]   # None para preámbulo
    articulo_raw:   str             # "Art. 226" tal como aparece en texto
    chunk_seq:      int             # 0=único/primero, 1,2...=continuación
    contenido:      str             # texto del chunk
    palabras:       int             # conteo de palabras
    sha256:         str             # hash SHA256 del contenido


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _word_count(text: str) -> int:
    return len(text.split())


def _split_long_chunk(articulo_raw: str,
                      articulo_num: Optional[int],
                      text: str) -> list[ArticleChunk]:
    """
    Divide un artículo largo en sub-chunks de ≤CHUNK_MAX_WORDS palabras.
    Mantiene CHUNK_OVERLAP_LINES líneas de solapamiento entre chunks.
    """
    lines = text.splitlines(keepends=True)
    chunks: list[ArticleChunk] = []
    current_lines: list[str] = []
    current_words = 0
    seq = 0

    for line in lines:
        line_words = _word_count(line)
        if current_words + line_words > CHUNK_MAX_WORDS and current_lines:
            # Emitir chunk actual
            chunk_text = "".join(current_lines).strip()
            if chunk_text:
                chunks.append(ArticleChunk(
                    articulo_num=articulo_num,
                    articulo_raw=articulo_raw,
                    chunk_seq=seq,
                    contenido=chunk_text,
                    palabras=_word_count(chunk_text),
                    sha256=_sha256(chunk_text),
                ))
                seq += 1
            # Retener overlap
            overlap = current_lines[-CHUNK_OVERLAP_LINES:] if CHUNK_OVERLAP_LINES > 0 else []
            current_lines = overlap
            current_words = sum(_word_count(l) for l in overlap)

        current_lines.append(line)
        current_words += line_words

    # Emitir chunk final
    if current_lines:
        chunk_text = "".join(current_lines).strip()
        if chunk_text:
            chunks.append(ArticleChunk(
                articulo_num=articulo_num,
                articulo_raw=articulo_raw,
                chunk_seq=seq,
                contenido=chunk_text,
                palabras=_word_count(chunk_text),
                sha256=_sha256(chunk_text),
            ))

    return chunks


def _make_chunk(articulo_raw: str,
                articulo_num: Optional[int],
                text: str) -> list[ArticleChunk]:
    """Crea 1 o más chunks a partir de un artículo."""
    text = text.strip()
    if not text:
        return []
    if _word_count(text) <= CHUNK_MAX_WORDS:
        return [ArticleChunk(
            articulo_num=articulo_num,
            articulo_raw=articulo_raw,
            chunk_seq=0,
            contenido=text,
            palabras=_word_count(text),
            sha256=_sha256(text),
        )]
    return _split_long_chunk(articulo_raw, articulo_num, text)


def _parse_art_num(raw: str) -> Optional[int]:
    """Extrae el número entero del artículo a partir del match del raw."""
    try:
        # Tomar solo la parte numérica inicial
        digits = re.match(r"(\d+)", raw.strip())
        return int(digits.group(1)) if digits else None
    except (ValueError, AttributeError):
        return None


def chunk_docx(filepath: str | Path) -> list[ArticleChunk]:
    """
    Carga un DOCX y lo segmenta en chunks artículo-nivel.

    Returns:
        Lista de ArticleChunk ordenados: PREÁMBULO (si existe) + Art. 1, 2, ...
    """
    from docx import Document  # python-docx

    doc = Document(str(filepath))

    # Extraer texto completo del DOCX (párrafos, tablas)
    parts: list[str] = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            parts.append(text)

    # Incluir texto de tablas (NCI, clasificadores tienen tablas con contenido)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text = cell.text.strip()
                if text and text not in parts:
                    parts.append(text)

    full_text = "\n".join(parts)

    # ── Segmentar por artículo ────────────────────────────────────────────────
    matches = list(ARTICLE_RE.finditer(full_text))

    if not matches:
        # Documento sin artículos detectables → todo como chunk único PREÁMBULO
        return _make_chunk("DOCUMENTO", None, full_text)

    chunks: list[ArticleChunk] = []

    # Preámbulo (texto antes del primer artículo)
    preamble_text = full_text[:matches[0].start()].strip()
    if preamble_text and _word_count(preamble_text) >= 20:
        chunks.extend(_make_chunk("PREÁMBULO", None, preamble_text))

    # Artículos
    for i, match in enumerate(matches):
        art_raw_num = match.group(1).strip()  # ej: "226", "único", "226.1"
        art_num     = _parse_art_num(art_raw_num)
        art_raw     = f"Art. {art_raw_num}"

        # Texto del artículo: desde el match hasta el siguiente (o fin)
        start = match.start()
        end   = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
        art_text = full_text[start:end].strip()

        chunks.extend(_make_chunk(art_raw, art_num, art_text))

    return chunks


def chunk_docx_with_meta(filepath: str | Path,
                         meta: dict) -> list[dict]:
    """
    Wrapper que retorna dicts listos para INSERT en normativa_corpus.

    meta: entrada del MANIFEST (sigla, nombre, jerarquia, milestone, tipo, dominios)
    """
    import json
    chunks = chunk_docx(filepath)
    rows   = []
    for c in chunks:
        rows.append({
            "norma_sigla":    meta["sigla"],
            "norma_nombre":   meta["nombre"],
            "jerarquia":      meta["jerarquia"],
            "milestone_qlep": meta["milestone"],
            "tipo_documento": meta["tipo"],
            "articulo_num":   c.articulo_num,
            "articulo_raw":   c.articulo_raw,
            "chunk_seq":      c.chunk_seq,
            "contenido":      c.contenido,
            "palabras":       c.palabras,
            "dominios_quira": json.dumps(meta["dominios"], ensure_ascii=False),
            "sha256":         c.sha256,
            "archivo_nombre": Path(filepath).name,
        })
    return rows


# ── TEST RÁPIDO ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, os
    if len(sys.argv) < 2:
        print("Uso: python chunker.py <ruta_archivo.docx>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"ERROR: archivo no encontrado: {path}")
        sys.exit(1)

    chunks = chunk_docx(path)
    print(f"\nArchivo: {os.path.basename(path)}")
    print(f"Chunks detectados: {len(chunks)}\n")
    for i, c in enumerate(chunks[:20]):   # primeros 20
        print(f"  [{i+1:3d}] {c.articulo_raw:15s} seq={c.chunk_seq}  "
              f"palabras={c.palabras:4d}  "
              f"sha256={c.sha256[:12]}...")
    if len(chunks) > 20:
        print(f"  ... ({len(chunks) - 20} chunks más)")
    print()

    total_palabras = sum(c.palabras for c in chunks)
    print(f"Total palabras: {total_palabras:,}")
    print(f"Promedio por chunk: {total_palabras // max(len(chunks), 1)}")
