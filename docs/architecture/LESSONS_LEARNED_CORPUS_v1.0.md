# Lecciones Aprendidas — Corpus Normativo v1.0

> Documento pedido por el colega (2026-07-21): captura el conocimiento técnico que la auditoría del
> corpus dejó, para que no se pierda ni se repita.

## 1. Dos activos distintos que se confundieron durante el proceso
- **Corpus Normativo** — los 43 documentos del `manifest.py` (QLEP-CORPUS). **v1.0 congelado, 100%
  completo.**
- **Banco Semántico de Indicadores** — `pdot_indicadores` + `pdot_extract_log`, poblado por
  `pdot_extractor.py`. **Solo `PDOT-MONTECRISTI` es parte del Corpus Normativo** (está en el
  manifest, `.docx`, pipeline `qlep-corpus`).

  **Corrección tras el hallazgo de Javo (mismo día):** mi primera redacción llamó a
  `PLAN-BICENTENARIO-MCR` "documento distinto" del PDOT — impreciso. Es el **mismo Plan de
  Desarrollo y Ordenamiento Territorial** (confirmado por coincidencia textual literal de portada),
  ingerido dos veces: `.docx` (oficial, pipeline `qlep-corpus`) y un PDF comprimido (pipeline
  `holding-v1.0`, anterior). Se verificaron **157 coincidencias exactas** de indicadores entre
  ambas — piso del solapamiento real. Normalización aplicada (ver
  `NORMALIZACION_PDOT_MULTIPLES_FUENTES.md`): `PDOT-MONTECRISTI` queda como fuente única
  autoritativa (`pdot_indicadores.fuente_autoritativa = true`); `PLAN-BICENTENARIO-MCR` se marca
  `false` (no se borra, no se vuelve a extraer). Lección: "documentos distintos" es una afirmación
  que exige verificar CONTENIDO, no solo metadatos de sigla/pipeline — dos siglas distintas pueden
  ser el mismo instrumento territorial. La tercera sigla del extractor, `PAI-PLURIANUAL-GAD`, sí es
  un documento distinto (Plan Anual de Inversión) — no comparte este problema. Confundir el Corpus
  con el Banco de Indicadores llevó a decir "extracción completa" cuando solo el Corpus lo estaba.

## 2. El límite real era del extractor, no del parser
Tras reemplazar el PDOT con el parser nuevo, una racha de "JSON inválido" parecía apuntar a un
problema de chunking. No lo era: **`max_tokens=2048`** se quedaba corto en tablas densas (áreas
verdes/equipamiento por núcleo urbano, decenas de filas numéricas) — Haiku generaba un array JSON
tan largo que se truncaba antes de cerrar. Prueba definitiva: el chunk 22832 pasó de `0 indicadores
/ JSON inválido` a **16 indicadores correctos** solo con `max_tokens=4096`. Lección: cuando un
parser nuevo "falla" justo después de un cambio grande, verificar primero el eslabón que consume su
salida antes de sospechar del parser.

## 3. La política de reintentos era demasiado conservadora
El extractor abortaba tras **5 fallos consecutivos**, asumiendo créditos agotados. Pero un JSON
truncado por tabla difícil y una excepción real de conexión/créditos son cosas distintas — mezclarlas
detenía toda la corrida por una sola sección complicada. Corregido: `extraer_chunk` ahora distingue
`parse_error` (JSON malformado tras 3 reintentos — sigue la corrida, se registra como error) de
`api_error` (excepción real de conexión/rate-limit/créditos — sigue contando para el aborto real).
Un corpus de miles de chunks no debe detenerse por una tabla rara.

## 4. Ingesta incremental por `chunk_id`, no reemplazo
`ingest.py` es aditivo (`ON CONFLICT (sha256) DO NOTHING`) — nunca borra. Cuando el chunking cambia,
el contenido (y el SHA) de cada chunk cambia, así que una "reingesta" simple no reemplaza: duplica.
Se resolvió con `reingesta_replace.py`: transaccional **documento por documento**
(`BEGIN→DELETE sigla→INSERT→COMMIT`), nunca `DELETE` de toda la tabla — si un documento falla, los
ya procesados quedan intactos (lo confirmó el caso PDOT: 42/43 exitosos, 1 rollback aislado).

## 5. Dependencias por `chunk_id` bloquean el reemplazo — hay que resolverlas antes, no forzar
`pdot_indicadores`/`pdot_extract_log` referencian `normativa_corpus.id` por FK. Reemplazar chunks
cambia los IDs y rompe esa relación. Opciones evaluadas: (A) migrar la FK a `chunk_sha256` — descartada,
porque el SHA también cambia si el chunking cambia, no resuelve nada por sí sola; (B) borrar las
filas dependientes (con backup) y re-extraer desde cero sobre los chunks nuevos — la elegida, porque
la nueva segmentación (headings de Word) da mejor contexto al extractor (3,317 indicadores vs 2,004).

## 6. Un regex de segmentación tiene un techo de complejidad manejable
Tres ajustes sucesivos al regex de artículos (ancla de título, límite de caracteres, exclusión de
mayúsculas) cada uno arreglaba un caso y rompía otro (LOPC, COOTAD-2026, CONA). Señal de que el
enfoque solo-regex llegó a su límite para referencias cruzadas densas. Se revirtió al regex ya
validado en vez de seguir iterando sobre producción sin batería de regresión más amplia — documentado
como limitación conocida (COOTAD-2026, CONA, COA-AMB, RCOA-AMB: contenido íntegro, solo mal numerado)
para un milestone **v1.1** con parser de mayor contexto (estructura DOCX / análisis sintáctico).

## Roadmap de versiones (recomendación del colega)
```
Corpus v1.0 (cerrado) → Indicadores v1.0 (finalización: PLAN-BICENTENARIO-MCR, 224 chunks
  pendientes, cuando haya crédito) → Parser v1.1 (referencias cruzadas) → Corpus v1.1
```

---
*Lecciones Aprendidas · Corpus v1.0 · Dylus Lab © 2026*
