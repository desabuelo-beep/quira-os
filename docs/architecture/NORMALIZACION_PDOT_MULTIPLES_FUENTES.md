# Normalización — Múltiples Manifestaciones del PDOT de Montecristi

> Hallazgo de Javo (2026-07-21): *"ningún municipio del país tiene dos PDOT o dos planes de
> desarrollo, es un único documento."* Correcto — y esta normalización corrige un framing mío
> insuficiente ("documentos distintos") que confundía **archivo fuente** con **instrumento de
> planificación**.

## El hallazgo, con evidencia
`PDOT-MONTECRISTI` y `PLAN-BICENTENARIO-MCR` son el **mismo Plan de Desarrollo y Ordenamiento
Territorial de Montecristi 2023-2027** ("Plan Bicentenario"), verificado por coincidencia textual
literal de portada e índice:
- `PDOT-MONTECRISTI` → `PDOT MOntecristi 2023-2027 Bicentenario.docx` · pipeline `qlep-corpus` ·
  **en el manifest de los 43 documentos normativos** · Corpus v1.0 oficial.
- `PLAN-BICENTENARIO-MCR` → `Oficiales\Plan Bicentenario1-comprimido.pdf` · pipeline
  `holding-v1.0` · ingesta anterior, **fuera del manifest**.

Confirmado en `pdot_indicadores`: **157 coincidencias exactas** (mismo indicador + valor +
territorio) entre ambas fuentes — piso del solapamiento real, ya que Haiku redacta cada indicador
con fraseo distinto según el chunking de origen (PDF vs. DOCX), así que el solapamiento semántico
verdadero es mayor a ese 4.7% medido literal.

## Decisión (Javo + colega, 2026-07-21)
**No se elimina nada. Se declara autoridad, se conserva historia.**

| | `PDOT-MONTECRISTI` | `PLAN-BICENTENARIO-MCR` |
|---|---|---|
| Rol | **Fuente única autoritativa** | Fuente histórica / deprecada |
| Motivo | Mejor parser (Strategy pattern), mejor chunking (headings de Word), mejor trazabilidad, es la fuente del Corpus v1.0 oficial | Ingesta anterior del mismo plan, chunking peor granulado, fuera del manifest |
| `pdot_indicadores.fuente_autoritativa` | `true` (3,317 filas) | `false` (3,430 filas, marcadas — no borradas) |
| `pdot_extractor.py` → `SIGLAS_PDOT` | incluida | **retirada** — no se vuelve a extraer de ahí |
| 224 chunks pendientes de extracción | — | **no se completan**: extraer más de una fuente redundante no aporta valor |

## Qué cambió en código/datos
1. **Migración de dato** (sin romper nada): `ALTER TABLE pdot_indicadores ADD COLUMN
   fuente_autoritativa boolean NOT NULL DEFAULT true` + `UPDATE ... SET fuente_autoritativa = false
   WHERE norma_sigla = 'PLAN-BICENTENARIO-MCR'`. Cualquier consumidor futuro del Banco de
   Indicadores (dashboards, GeoTwin, QTMP) debe filtrar `WHERE fuente_autoritativa = true` para
   evitar contar el mismo dato territorial dos veces.
2. **`pdot_extractor.py`**: `SIGLAS_PDOT` ya no incluye `PLAN-BICENTENARIO-MCR` — no se reanuda su
   extracción por accidente en una corrida futura.
3. **Nada se borró** de `normativa_corpus` ni de `pdot_indicadores` — la trazabilidad histórica de
   `PLAN-BICENTENARIO-MCR` permanece consultable.

## Pendiente para v1.1
- Hay una **cuarta fuente**, `PDOT-KB-EXCEL` (1,660 indicadores en `pdot_indicadores`), no
  investigada en esta sesión — queda como `fuente_autoritativa = true` (default) hasta verificar si
  es complementaria (un Knowledge Base estructurado distinto) o si también solapa con el `.docx`.
- Considerar si los 3,430 indicadores de `PLAN-BICENTENARIO-MCR` deben excluirse por completo de
  las vistas/consultas del Banco de Indicadores, o si basta con el filtro por
  `fuente_autoritativa`.

---
*Normalización PDOT · Dylus Lab © 2026 · "Un plan, un documento canónico — la trazabilidad no exige mantener dos identidades activas para el mismo instrumento."*
