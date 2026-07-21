# Manifiesto de Limpieza del Corpus — Duplicados Detectados

> Documento de trazabilidad previo a cualquier borrado (pedido del colega, 2026-07-21): antes de
> eliminar un registro de Supabase se deja evidencia reproducible de qué es, de dónde vino y por
> qué se propone la acción. **Nada se ha borrado.** Este documento solo describe el hallazgo.

## Limitación conocida — `COOTAD-2026` Art. 5/6/7 (registrada, no resuelta)

Durante la reingesta (2026-07-21) se detectó que el chunker fusiona los Art. 5, 6 y 7 de la ley
reformatoria bajo el rótulo `Art. 198` cuando su texto contiene, cerca, una referencia cruzada del
tipo `"Artículo 5 .- Agréguese... del artículo 198.4..."`. Se intentaron 3 ajustes sucesivos al
regex (`ARTICLE_RE`); cada uno resolvía ese caso pero introducía una regresión distinta en otro
documento (LOPC Art. 9, o el título completo de la ley fusionado con Art. 1). Se decidió **revertir
al regex ya validado y usado en la reingesta real** (el que generó los 42 documentos reemplazados
exitosamente) en vez de seguir iterando sobre datos de producción sin una batería de regresión más
amplia. **El contenido de los Art. 5/6/7 SÍ está íntegro en el corpus** (nada se pierde) — solo el
número de artículo asignado a esos 3 chunks es incorrecto. Pendiente: un ajuste acotado y muy
probado (o corrección manual de esos 3 registros) en una sesión dedicada, no un parche apresurado.

## Hallazgo 1 — `RES-ORG-GAD-2025` duplica a `RES-ORG-GADMCM-2025`

| Campo | `RES-ORG-GAD-2025` (candidato a limpieza) | `RES-ORG-GADMCM-2025` (correcto, en manifest) |
|---|---|---|
| Documento fuente | Resolución Administrativa No. 040-2025-ALC-LJTL-GADMCM — Orgánico Estructural | El mismo documento |
| Chunks | 97 | 92 |
| `articulo_num` poblado | 0 de 97 (ninguno) | 86 de 92 |
| Pipeline (`ingestado_por`) | `holding-v1.0` | `qlep-corpus-v1.0` |
| Fecha de ingesta | 2026-06-03T12:57:56Z | 2026-06-02T01:32:39Z (1 día antes) |
| SHA de muestra (chunk 1) | `b5e4085449cb...` | `d436c332bf83...` (distinto — texto trozado distinto, mismo documento) |
| ¿En `manifest.py`? | **No** | Sí — sigla oficial del corpus normativo |

**Diagnóstico:** el mismo documento fue ingerido dos veces por **dos pipelines distintos**: primero por QLEP-CORPUS (el flujo normativo, con artículos numerados — correcto), y un día después por el pipeline del Holding (evidencia observacional municipal, texto plano sin artículo). No es corrupción de datos: son dos sistemas que no se coordinaron sobre el mismo documento fuente.

**Acción propuesta:** eliminar los 97 chunks de `RES-ORG-GAD-2025` (sigla fuera del manifest, sin estructura articulada, entrada `holding-v1.0`). Mantener `RES-ORG-GADMCM-2025` (sigla oficial, articulada, `qlep-corpus-v1.0`). **Pendiente de autorización de Javo.**

## Documentos revisados y descartados como falso positivo

Durante el check de integridad referencial (`--integridad`) aparecieron otras siglas fuera del manifest (`RC-ASEO-*`, `RC-GAD-*`, `RC-PATRONATO-*`, `RC-BOMBEROS-*`, `SIGAD-GAD-*-DOC`, `PRESUP-PATRONATO-2024-DOC`, `PLAN-BICENTENARIO-MCR`). Se verificó su `tipo_documento` en Supabase: son `EVIDENCIA_OBSERVACIONAL` / `informe_rendicion` / `INSTRUMENTO_TERRITORIAL` — pertenecen al **pipeline del Holding Municipal** (evidencia real de rendición de cuentas, presupuesto, SIGAD), una colección distinta y legítima dentro de la misma tabla compartida `normativa_corpus`. **No son duplicados de corpus normativo** y no se tocan.

## Procedimiento de verificación (reproducible)
```sql
-- Confirmar que ambas siglas describen el mismo documento
SELECT norma_sigla, count(*), count(articulo_num), ingestado_por, min(ingestado_at)
FROM normativa_corpus WHERE norma_sigla IN ('RES-ORG-GAD-2025','RES-ORG-GADMCM-2025')
GROUP BY norma_sigla, ingestado_por;
```

---
*Manifiesto de Limpieza · Dylus Lab © 2026 · generado antes de tocar Supabase, no después.*
