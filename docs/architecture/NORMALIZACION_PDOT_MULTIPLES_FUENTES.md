# Normalización — Entidad Documental Canónica y Manifestaciones (PDOT Montecristi)

> Hallazgo de Javo (2026-07-21): *"ningún municipio del país tiene dos PDOT o dos planes de
> desarrollo, es un único documento."* Confirmado y **certificado directamente por Javo** también
> para una tercera fuente (el KB Excel). El colega precisó el modelo: el problema no era "archivo
> distinto" sino confundir **entidad documental** con **manifestación documental**.

## El modelo correcto (colega, 2026-07-21)
```
DOCUMENTO CANÓNICO                      (nivel semántico — el instrumento institucional)
  PDOT-MONTECRISTI-2023-2027
        │
        ├── Manifestación DOCX  (PDOT-MONTECRISTI)      ← CANÓNICA
        ├── Manifestación PDF   (PLAN-BICENTENARIO-MCR) ← réplica
        └── Manifestación KB    (PDOT-KB-EXCEL)         ← réplica
```
**La autoridad no es propiedad de un indicador — es propiedad de la manifestación** de la que ese
indicador fue extraído. Un booleano suelto en `pdot_indicadores` no escala si mañana aparece una
manifestación HTML o XML del mismo documento; una capa de Entidad Documental Canónica sí.

## Las tres manifestaciones, con evidencia
| Manifestación | `norma_sigla` | Tipo | Pipeline | ¿Canónica? |
|---|---|---|---|---|
| `.docx` completo | `PDOT-MONTECRISTI` | docx | `qlep-corpus-v1.0` | **sí** — mejor parser (Strategy pattern), mejor chunking (headings de Word), fuente del Corpus v1.0 |
| PDF comprimido | `PLAN-BICENTENARIO-MCR` | pdf | `holding-v1.0` | no — réplica; 157 indicadores exactos duplicados con la canónica (piso — el solapamiento semántico real es mayor, ver nota) |
| Knowledge Base Excel | `PDOT-KB-EXCEL` | kb_excel | `v1-kb-parser` | no — **certificado por Javo**: construido antes de QUIRA para maximizar cobertura de indicadores del PDOT, con énfasis en PUGS (confirmado: su categoría PUGS existe con 24 registros) |

**Nota sobre "157 duplicados" (precisión del colega):** ese número es una comparación de
**igualdad literal** (`indicador` + `valor_texto` + `territorio` idénticos carácter a carácter).
Es un **piso conservador**, no el solapamiento real: Haiku puede redactar el mismo dato territorial
como *"Área urbana consolidada"* en una extracción y *"Superficie urbana consolidada"* en otra —
semánticamente idénticos, textualmente distintos, y esa comparación NO los detecta. El
solapamiento semántico real entre las tres manifestaciones es mayor a 157/3317. No se ha
cuantificado con precisión — requeriría comparación semántica (embeddings), no literal.

## Esquema implementado
```sql
documento_canonico (id, nombre, descripcion, canton_id)
manifestacion_documental (
    id, documento_canonico_id → documento_canonico,
    norma_sigla UNIQUE,               -- la sigla que ya usan normativa_corpus / pdot_indicadores
    tipo_manifestacion,               -- 'docx' | 'pdf' | 'kb_excel' | ...
    archivo_origen, pipeline_origen,
    es_canonica boolean,              -- SOLO una por documento_canonico_id
    replica_de → manifestacion_documental.norma_sigla,   -- de cuál es réplica, si aplica
    notas
)
```
`pdot_indicadores.fuente_autoritativa` se mantiene como columna de conveniencia (evita un JOIN en
cada consulta) pero **ahora se sincroniza desde `manifestacion_documental.es_canonica`** — la tabla
de manifestaciones es la fuente de verdad; el booleano es una proyección, no el diseño.

También se registró `PAI-PLURIANUAL-GAD` como su propio `documento_canonico` (documento distinto,
no comparte este problema) — así el modelo cubre las tres siglas del extractor de forma uniforme,
sin casos especiales.

## Qué NO se hizo (deliberadamente)
- **No se borró nada** de `normativa_corpus` ni `pdot_indicadores`. Las réplicas quedan consultables
  con su relación explícita (`replica_de`) hacia la manifestación canónica.
- **No se sacó `PLAN-BICENTENARIO-MCR` "sin dejar rastro"** del extractor: el modelo ahora permite
  que un futuro `pdot_extractor.py` v2 CONSULTE `manifestacion_documental` antes de procesar un
  documento — si encuentra que la sigla es `es_canonica=false`, la salta automáticamente y registra
  por qué (en vez de que quede simplemente ausente de una lista hardcodeada, como quedó hoy de forma
  provisional en `SIGLAS_PDOT`).

## Pendiente
- Cuantificar el solapamiento semántico real (no solo literal) entre las tres manifestaciones —
  candidato a v1.1, usando los embeddings ya generados de `normativa_corpus` (no de
  `pdot_indicadores`, que no tiene embedding propio).
- Migrar `pdot_extractor.py` para que consulte `manifestacion_documental` en vez de la lista estática
  `SIGLAS_PDOT` — hoy es provisional (se retiró `PLAN-BICENTENARIO-MCR` a mano de esa lista).

---
*Normalización PDOT · Dylus Lab © 2026 · "La autoridad documental vive en la manifestación, no en cada dato extraído de ella — ese es el nivel correcto para modelar la trazabilidad."*
