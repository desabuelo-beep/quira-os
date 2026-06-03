# OBS-004 — Calidad del Corpus de Evidencia Observacional

**Estado**: CONFIRMED
**Fecha**: 2026-06-03
**Origen**: Gate 6.5A · Semantic Mining sobre RC+PP
**Tipo**: Observacion de calidad de datos

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

### P1 — Repeticion acumulativa de cabecera (RC-GAD)
Los chunks de RC-GAD-2023/2024 acumulan el header del informe en cada chunk
por efecto del overlap del chunker. Resultado: mucho contexto redundante.
**Impacto**: reduccion de densidad semantica util por chunk.
**Mitigacion**: ajustar CHUNK_OVERLAP en chunker_holding.py de 50 a 10 palabras
para documentos DOCX muy estructurados.

### P2 — Texto scrambled en PDFs escaneados (RC-ASEO final pages)
Las ultimas paginas de RC-ASEO-2023 contienen texto con letras separadas por espacios
(artefacto de extraccion de PDF escaneado). Ejemplo: "o r s e c l a e r q g u o i p..."
**Impacto**: chunks inutilizables semanticamente.
**Mitigacion**: filtro GIBBERISH_RE activo en mine_evidence.py excluye estos chunks.
**Accion futura**: aplicar OCR (pymupdf) en PDFs escaneados antes de ingestar.

### P3 — Chunks de texto nominal (< 30 palabras)
Algunos chunks son solo titulos de seccion sin contenido sustancial.
**Mitigacion**: filtro MIN_PALABRAS=30 activo.

## Impacto en la Analitica

Los problemas afectan ~15-20% del corpus de evidencia.
El 80-85% restante es utilizable para mineria semantica.
Los PP-GAD (246 chunks de alta densidad) son el activo mas limpio del corpus.

---

*OBS-004 · QUIRA Gov · Dylus Lab · 2026-06-03*
