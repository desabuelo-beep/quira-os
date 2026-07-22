# Normalización — Entidad Documental Canónica y Manifestaciones (PDOT Montecristi)

> Hallazgo de Javo (2026-07-21): *"ningún municipio del país tiene dos PDOT... es un único
> documento."* Certificado también para el KB Excel y el PAI. El colega cerró el modelo con una
> corrección metodológica de fondo (ver §Lección).

## El modelo final
```
DOCUMENTO CANÓNICO — PDOT-MONTECRISTI-2023-2027    (nivel semántico: el instrumento institucional)
        │
        ├── DOCX  (PDOT-MONTECRISTI)       formato=docx     completitud=copia_íntegra   ← CANÓNICA
        ├── PDF   (PLAN-BICENTENARIO-MCR)  formato=pdf      completitud=copia_íntegra
        ├── KB    (PDOT-KB-EXCEL)          formato=kb_excel completitud=knowledge_base
        └── PAI   (PAI-PLURIANUAL-GAD)     formato=docx     completitud=extracto
```
**Completitud ≠ formato** (precisión del colega): una manifestación no es necesariamente una copia
completa. El KB Excel es un **derivado estructurado** con énfasis en PUGS; el PAI es un **extracto**
(solo la matriz plurianual). Tratarlas todas como "réplica/no-réplica" homogeneizaba de más — el
campo `completitud` distingue `copia_íntegra | extracto | derivado | índice | knowledge_base`.

## Esquema final (Supabase)
```sql
documento_canonico (id, nombre, descripcion, canton_id)

manifestacion_documental (
    id SERIAL PK,
    documento_canonico_id → documento_canonico,
    norma_sigla UNIQUE,             -- puente con normativa_corpus / pdot_indicadores
    tipo_manifestacion,             -- formato: docx | pdf | kb_excel
    completitud,                    -- naturaleza: copia_integra | extracto | derivado | knowledge_base
    archivo_origen, pipeline_origen,
    es_canonica boolean,            -- SOLO una por documento_canonico_id
    replica_de → manifestacion_documental.norma_sigla,
    notas
)

pdot_indicadores.id_manifestacion → manifestacion_documental.id     -- FK REAL, fuente de verdad
```
`pdot_indicadores.fuente_autoritativa` queda **DEPRECADA** (comentario SQL en la columna, sin
`DROP` sobre datos de producción): sobraba en cuanto existió el FK real. Cualquier consumidor nuevo
debe usar `id_manifestacion → manifestacion_documental.es_canonica`, no el booleano.

## Las cuatro manifestaciones, con evidencia
| Manifestación | `norma_sigla` | Formato | Completitud | ¿Canónica? |
|---|---|---|---|---|
| `.docx` completo | `PDOT-MONTECRISTI` | docx | copia_íntegra | **sí** — mejor parser, mejor chunking, en el manifest de los 43 |
| PDF comprimido | `PLAN-BICENTENARIO-MCR` | pdf | copia_íntegra | no — 157 indicadores exactos duplicados (piso conservador, ver nota) |
| Knowledge Base Excel | `PDOT-KB-EXCEL` | kb_excel | knowledge_base | no — certificado por Javo: derivado con énfasis en PUGS (24 registros confirmados) |
| Plan Plurianual de Inversiones | `PAI-PLURIANUAL-GAD` | docx | extracto | no — solo la matriz plurianual; nombre de archivo `...GAD Montecristi PDOT.docx` |

**Nota sobre "157 duplicados":** comparación de igualdad **literal**, piso conservador. Haiku
redacta el mismo dato con fraseo distinto entre extracciones ("Área urbana consolidada" vs.
"Superficie urbana consolidada") — el solapamiento semántico real es mayor. No cuantificado aún
(candidato v1.1, requiere comparación por embeddings).

## Lección metodológica (colega, 2026-07-21) — la más importante de esta fase
La secuencia real de esta sesión fue:
```
"No son el mismo documento" → "Sí son el mismo" → "hay tres manifestaciones" → "hay cuatro"
```
Eso revela el error de fondo: **se modeló a partir de los nombres de las siglas, no de la identidad
documental.** La regla correcta en ingeniería documental es la inversa:
> Primero se identifica el activo documental canónico. Después se identifican todas sus
> manifestaciones. Nunca al revés.
Cada corrección en cascada (documentos→mismo documento→3→4 manifestaciones) fue evitable si el
primer paso hubiera sido preguntar *"¿cuántos PDOT tiene Montecristi?"* en vez de *"¿estas dos
siglas apuntan a archivos distintos?"*. Se registra explícitamente para no repetirlo: ante una
nueva sigla que toque el mismo dominio territorial/institucional, el primer paso es identificar el
documento canónico, no comparar metadatos de ingesta.

## Qué NO se hizo (deliberadamente)
- **No se borró nada.** Las cuatro manifestaciones quedan consultables, con su completitud y su
  relación explícita hacia la canónica.
- **No se hizo `DROP COLUMN fuente_autoritativa`** sobre una tabla de producción sin verificar antes
  qué código externo la consulta — se deprecó con comentario SQL, candidata a eliminar en v1.1.

## Pendiente
- Cuantificar el solapamiento semántico real (embeddings) entre las cuatro manifestaciones.
- Migrar `pdot_extractor.py` para que consulte `manifestacion_documental` (filtrando
  `es_canonica=true`) en vez de la lista estática `SIGLAS_PDOT`.
- Revisar si algún consumidor existente (dashboards, GeoTwin, QTMP) lee `fuente_autoritativa`
  directamente — si es así, migrarlo al JOIN antes de considerar el `DROP COLUMN` definitivo.

---
*Normalización PDOT · Dylus Lab © 2026 · "Primero el documento canónico, después sus manifestaciones — nunca al revés."*
