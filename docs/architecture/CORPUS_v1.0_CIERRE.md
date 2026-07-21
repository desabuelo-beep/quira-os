# Corpus Normativo v1.0 — Cierre y Línea Base Congelada

> **Estado:** ❄️ CONGELADO · 2026-07-21 · hash maestro `8d3220d6…c39dd527`
> **Parser:** `parser-v1.0` (tag) · **Documentos:** 43 · **Chunks normativos:** 9,158

Cierre de la fase de estabilización del corpus normativo, iniciada por el hallazgo de Javo (el
Art. 88 de la LOPC citado como "inexistente" cuando en realidad **faltaba en la ingesta**, no en el
Derecho). Lo que empezó como un bug puntual se convirtió en una auditoría completa de la materia
prima sobre la que se apoya toda la BRN.

## Principio que guio la fase
> *«Si la base normativa no está completa, todo lo que se construya encima es alucinación probable.»*
> Una plataforma de integridad no puede basarse en integridad asumida: debe **demostrarla**.

## Qué se hizo (plan del colega, ejecutado en orden)
1. **Auditoría completa** de los 43 documentos (no un caso aislado): `auditar_corpus.py` con 6 modos
   — cobertura docx-vs-corpus, `--estructural`, `--cobertura-perfil`, `--calidad`, `--fixtures`,
   `--integridad`.
2. **Parser corregido** — 3 bugs de segmentación hallados y arreglados:
   - regex tragaba el título del artículo + falsos matches (`\w+`);
   - ancla exigía inicio de línea → perdía artículos maquetados como `"...título Art. N\n"` (LOPC 77/103);
   - **Disposiciones** (Transitorias/Finales/Derogatorias) absorbidas en el artículo previo — ahí vive
     el 65% de COOTAD-2026.
3. **Parser multi-perfil** (Strategy pattern) para documentos NO articulados — nada es "segunda fase":
   PND (Objetivo/Política), NCI-CGE/PDOT/guías (encabezados de Word), convenios (Art. real).
   Reproducibilidad completa verificada (43/43 · mismo nº de chunks, orden, SHA y metadata).
4. **Backup completo** (13,106 filas con embeddings) → `data/backups/`.
5. **Reingesta REPLACE transaccional** documento por documento (BEGIN→DELETE→INSERT→COMMIT; nunca
   DELETE de toda la tabla). 42/43 en la primera pasada; el diseño transaccional aisló el único fallo.
6. **PDOT-MONTECRISTI — Opción B** (decisión de Javo): sus chunks tenían 2,004 indicadores
   territoriales dependientes por FK (`pdot_indicadores`). Se respaldó, se reemplazó el PDOT
   (594→825 chunks) y se **re-extrajeron los indicadores con Haiku** sobre la nueva segmentación →
   **3,317 indicadores** (más ricos, cada chunk trae su encabezado de sección). Integridad FK: 0 huérfanos.
7. **Limpieza del duplicado** `RES-ORG-GAD-2025` (mismo documento que `RES-ORG-GADMCM-2025`, ingerido
   dos veces por pipelines distintos) — con backup, manifiesto de trazabilidad y verificación de 0
   dependencias antes de borrar.
8. **Congelación** — este documento + hash maestro.

## Estado final
- **Integridad referencial: GRAFO CERRADO** — 0 SHA duplicados, 0 chunks sin contenido, 0 siglas
  fuera del manifest, 0 del manifest sin ingestar.
- **35 normas articuladas:** 21 al 100%, 7 con ruido de conteo (referencias cruzadas contadas como
  faltantes, sin pérdida real), **4 con el límite conocido del regex** (abajo).
- **8 no articuladas** segmentadas por su unidad estructural propia.
- **PDOT** reconstruido con integridad FK perfecta.

## Límite conocido → milestone v1.1 (NO bloquea v1.0)
En leyes con **referencias cruzadas densas** (`"Artículo 5.- Agréguese... del artículo 198.4..."`),
el regex asigna mal el número de artículo a un puñado de chunks: **COOTAD-2026** (Art. 5/6/7),
**CONA** (6), **COA-AMB** (6), **RCOA-AMB** (15). **El contenido está íntegro en el corpus** — solo
la etiqueta numérica es incorrecta. Se intentaron 3 ajustes al regex; cada uno rompía otro documento.
Conclusión (compartida con el colega): el enfoque de solo-regex llegó a su límite. **v1.1** debe usar
un parser con más contexto (estructura DOCX / análisis sintáctico), en un milestone dedicado, sin
mezclarlo con el cierre de esta línea base estable.

## Deuda menor conocida
- `PLAN-BICENTENARIO-MCR`: 224 chunks sin extraer indicadores (corte por créditos de API, no por el
  parser). Reanudable con `pdot_extractor.py` cuando haya crédito. No es de los 43 normativos.

## Reproducibilidad
El hash maestro (`SHA256` de todos los `sha256` de chunks normativos, ordenados) permite verificar en
cualquier momento que el corpus sigue siendo el mismo. Regenerar con el mismo parser sobre los mismos
43 `.docx` debe producir el mismo hash. Snapshot completo en `CORPUS_v1.0_MAESTRO.json`.

---
*Corpus Normativo v1.0 · Dylus Lab © 2026 · «La base sobre la que operarán los 222 cantones ya no se asume completa: se demostró que lo es.»*
