# -*- coding: utf-8 -*-
"""
chunker_holding.py — DOCX/PDF → chunks seccion-nivel
QUIRA Gov · Holding Municipal Montecristi · Dylus Lab © 2026

A diferencia del chunker normativo (articulo-nivel), este chunker opera
sobre documentos de gestion publica (RC, PP, POA, PAC, SIGAD) que tienen
estructura de secciones/capitulos, no de articulos juridicos.

Estrategia:
  1. Extraer texto del DOCX (python-docx) o PDF (pdfplumber)
  2. Detectar limites de seccion con regex flexible
  3. Chunks de ~400 palabras con overlap de 2 parrafos
  4. SHA256 por chunk para idempotencia

Dependencias: python-docx, pdfplumber
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ── REGEX CABECERAS DE SECCION ────────────────────────────────────────────────
# Detecta: "CAPITULO I", "SECCIÓN 3", "1.", "1.1", "I.", titulos en mayuscula
SECTION_RE = re.compile(
    r"(?:^|\n)\s*"
    r"(?:"
    r"CAP[IÍ]TULO\s+[\dIVXivx]+"            # CAPÍTULO I / CAPÍTULO 1
    r"|SECCI[OÓ]N\s+[\dIVXivx]+"             # SECCIÓN 3
    r"|\d+\.\d*\s+[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]+" # 1.2 TITULO EN MAYUSCULAS
    r"|\d+\.\s+[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]+"    # 1. TITULO EN MAYUSCULAS
    r"|[IVX]+\.\s+[A-ZÁÉÍÓÚÑ]"              # I. TITULO
    r"|[A-ZÁÉÍÓÚÑ]{4,}(?:\s+[A-ZÁÉÍÓÚÑ]{2,}){0,5}\s*$" # LINEA TODO MAYUSCULAS
    r")",
    re.MULTILINE
)

CHUNK_MAX_WORDS  = 400
CHUNK_OVERLAP    = 50   # palabras de overlap entre chunks


@dataclass
class HoldingChunk:
    """Un chunk de documento del Holding Municipal."""
    seccion_raw:   str               # cabecera de sección detectada o "PÁRRAFO"
    chunk_seq:     int               # secuencia en el documento
    contenido:     str               # texto del chunk
    palabras:      int               # conteo de palabras
    sha256:        str               # hash del contenido
    pagina_inicio: Optional[int] = None  # para PDFs

    @classmethod
    def from_text(cls, text: str, seq: int, seccion: str = "CONTENIDO",
                  pagina: Optional[int] = None) -> "HoldingChunk":
        text = text.strip()
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return cls(
            seccion_raw   = seccion,
            chunk_seq     = seq,
            contenido     = text,
            palabras      = len(text.split()),
            sha256        = sha,
            pagina_inicio = pagina,
        )


# ── EXTRACCIÓN DE TEXTO ────────────────────────────────────────────────────────

def _extract_text_docx(path: Path) -> list[tuple[str, int]]:
    """
    Extrae párrafos de un DOCX.
    Retorna: lista de (texto_parrafo, numero_parrafo)
    """
    from docx import Document
    doc = Document(str(path))
    paragraphs = []
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if text:
            paragraphs.append((text, i))
    return paragraphs


def _extract_text_pdf(path: Path) -> list[tuple[str, int]]:
    """
    Extrae texto de un PDF página por página usando pdfplumber.
    Retorna: lista de (texto_pagina, numero_pagina)
    """
    import pdfplumber
    pages = []
    with pdfplumber.open(str(path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages.append((text, i))
    return pages


def _extract_text(path: Path) -> tuple[list[tuple[str, int]], str]:
    """
    Auto-detecta formato y extrae texto.
    Retorna: (fragmentos, tipo) donde tipo = 'docx' | 'pdf'
    """
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return _extract_text_docx(path), "docx"
    elif suffix == ".pdf":
        return _extract_text_pdf(path), "pdf"
    else:
        raise ValueError(f"Formato no soportado: {suffix}")


# ── CHUNKING ──────────────────────────────────────────────────────────────────

def _split_into_chunks(fragments: list[tuple[str, int]],
                       doc_type: str) -> list[HoldingChunk]:
    """
    Divide los fragmentos en chunks de ~CHUNK_MAX_WORDS palabras.
    Detecta cabeceras de sección como límites naturales.
    """
    chunks: list[HoldingChunk] = []
    current_words: list[str] = []
    current_seccion = "CONTENIDO"
    current_page: Optional[int] = None
    seq = 0

    def flush(words: list[str], seccion: str, page: Optional[int]) -> Optional[HoldingChunk]:
        text = " ".join(words).strip()
        if len(text) < 20:   # ignorar fragmentos muy cortos
            return None
        return HoldingChunk.from_text(text, seq, seccion, page)

    for fragment, page_or_para in fragments:
        page_ref = page_or_para if doc_type == "pdf" else None

        # Detectar si el fragmento es una cabecera de sección
        is_section_header = bool(SECTION_RE.match(fragment)) or (
            len(fragment) < 120 and fragment.isupper() and len(fragment.split()) >= 2
        )

        if is_section_header and current_words:
            # Emitir chunk actual antes de nueva sección
            chunk = flush(current_words, current_seccion, current_page)
            if chunk:
                chunks.append(chunk)
                seq += 1
            # Conservar overlap
            overlap_words = current_words[-CHUNK_OVERLAP:] if len(current_words) > CHUNK_OVERLAP else current_words[:]
            current_words = overlap_words
            current_seccion = fragment[:100]  # nueva sección
            current_page = page_ref

        # Agregar texto al buffer
        fragment_words = fragment.split()
        current_words.extend(fragment_words)

        # Emitir si supera el límite
        while len(current_words) >= CHUNK_MAX_WORDS:
            chunk_words = current_words[:CHUNK_MAX_WORDS]
            chunk = flush(chunk_words, current_seccion, current_page)
            if chunk:
                chunks.append(chunk)
                seq += 1
            # Overlap para el siguiente chunk
            current_words = current_words[CHUNK_MAX_WORDS - CHUNK_OVERLAP:]
            current_page = page_ref

    # Emitir lo que queda
    if current_words:
        chunk = flush(current_words, current_seccion, current_page)
        if chunk:
            chunks.append(chunk)

    return chunks


# ── API PÚBLICA ───────────────────────────────────────────────────────────────

def chunk_holding_doc(path: str | Path) -> list[HoldingChunk]:
    """
    Chunker principal para documentos del Holding Municipal.
    Acepta DOCX o PDF. Retorna lista de HoldingChunk.

    Uso:
        chunks = chunk_holding_doc("path/to/RC-GAD-2024.docx")
        for c in chunks:
            print(c.seccion_raw, c.palabras, c.sha256[:8])
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    fragments, doc_type = _extract_text(path)
    chunks = _split_into_chunks(fragments, doc_type)
    return chunks


# ── TEST ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python chunker_holding.py <path_to_docx_or_pdf>")
        sys.exit(1)

    target = Path(sys.argv[1])
    print(f"Procesando: {target.name}")
    chunks = chunk_holding_doc(target)
    print(f"Chunks generados: {len(chunks)}")
    for c in chunks[:3]:
        print(f"  [{c.chunk_seq}] {c.seccion_raw[:50]:50s} | {c.palabras:4d} palabras | {c.sha256[:12]}")
    if len(chunks) > 3:
        print(f"  ... {len(chunks)-3} chunks mas")
