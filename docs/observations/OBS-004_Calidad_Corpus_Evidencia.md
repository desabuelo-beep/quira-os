# OBS-004 — Calidad del Corpus de Evidencia Observacional

**Estado**: CONFIRMED — FIX APLICADO  
**Fecha**: 2026-06-02  
**Actualizado**: 2026-06-03 (chunker fix ejecutado)  
**Origen**: Gate 6.5A · Semantic Mining sobre RC+PP  
**Tipo**: Observacion de calidad de datos + accion correctiva

---

## Hallazgo

Al ejecutar Gate 6.5 Fase 1 se ingresaron 392 chunks del Holding Municipal Montecristi.
El analisis de calidad revela patrones de extraccion que afectan la utilidad analitica
de algunos chunks.

## Estadisticas del Corpus (392 chunks)

| Documento | Chunks | Palabras | Avg pal/chunk |
|---|---|---|---|
| PP-GAD-2024 | 22 | 7,991 | 363.2 |
| PP-GAD-2025 | 110 | 43,702 | 397.3 |
| PP-GAD-2026 | 114 | 45,259 | 397.0 |
| RC-ASEO-2023 | 21 | 8,248 | 392.8 |
| RC-ASEO-2024 | 43 | 17,197 | 399.9 |
| RC-BOMBEROS-2023 | 13 | 4,780 | 367.7 |
| RC-BOMBEROS-2024 | 15 | 5,708 | 380.5 |
| RC-GAD-2023 | 12 | 1,436 | 119.7 |
| RC-GAD-2024 | 13 | 1,691 | 130.1 |
| RC-PATRONATO-2023 | 19 | 988 | 52.0 |
| RC-PATRONATO-2024 | 10 | 425 | 42.5 |

**Total**: 392 chunks · 137,425 palabras
**RC**: 146 chunks · **PP**: 246 chunks

## Problemas de Calidad Detectados

### P1 — Repeticion acumulativa de cabecera (RC-GAD) — FIX APLICADO

Los chunks de RC-GAD-2023/2024 acumulaban el header del informe en cada chunk
por efecto del overlap (50 palabras en DOCX). Adicionalmente, el template CPCCS
de RC usa una estructura de "path acumulativo" donde cada párrafo incluye la
jerarquía del documento completa.

**Fix ejecutado** (commit siguiente a este):
- `CHUNK_OVERLAP_DOCX = 10` (era 50) — evita arrastre de cabeceras de sección
- `_dedupe_common_prefix()` — función nueva que stripea prefijos comunes entre
  chunks consecutivos (threshold: 15 palabras idénticas iniciales)
- Overlap adaptativo: DOCX=10, PDF=50

**Chunks RC-GAD post-fix**: deduplicacion activa, menor repeticion de contexto.

**Issue residual conocido**: el template CPCCS genera párrafos muy cortos (9-19 palabras)
que son solo campos/etiquetas del formulario. Esto no es un bug del chunker — es
la estructura del documento. Los filtros MIN_PALABRAS=30 en mine_evidence.py los
excluyen correctamente de la minería.

**Para Fases 2-3 (POA, PAC)**: documentos con estructura diferente — el fix
de CHUNK_OVERLAP_DOCX=10 los beneficiará directamente.

### P2 — Texto scrambled en PDFs escaneados (RC-ASEO final pages)

Las últimas páginas de RC-ASEO-2023 contienen texto con letras separadas por
espacios (artefacto de extracción de PDF escaneado por pdfplumber).
Ejemplo: "o r s e c l a e r q g u o i p..."

**Estado**: ACEPTADO con filtro activo.
**Mitigación actual**: filtro GIBBERISH_RE en mine_evidence.py excluye estos chunks.
**Acción futura**: para Fase 5 (XLSX) y si se reingestar PDFs escaneados, usar
pymupdf con OCR antes de chunking.

### P3 — Chunks de texto nominal (< 30 palabras)

Algunos chunks son solo títulos de sección sin contenido sustancial.
**Mitigación activa**: filtro MIN_PALABRAS=30 en mine_evidence.py.

## Impacto en la Analitica

Los problemas afectan ~15-20% del corpus de evidencia.
El 80-85% restante es utilizable para mineria semantica.
Los PP-GAD (246 chunks de alta densidad) son el activo mas limpio del corpus.

---

*OBS-004 · QUIRA Gov · Dylus Lab · 2026-06-03*
