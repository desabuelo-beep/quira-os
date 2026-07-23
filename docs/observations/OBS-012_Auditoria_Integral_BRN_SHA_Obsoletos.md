# OBS-012 — Auditoría Integral: BRN con SHA256 obsoletos + Art.241 CE perdido

**Estado**: RESUELTO — corregido el mismo día · 2026-07-23
**Origen**: Auditoría integral solicitada por Javo ("destripe todo súper rudo") antes de migrar d02/d03/d09, disparada por el patrón de bugs encontrados el 22-23 jul.
**Ancla**: `docs/brn/CNO-I-001.yaml` · `CNO-III-001.yaml` · `CNO-IV-001.yaml` · `CNO-IX-001.yaml` · Corpus v1.0.

---

## Hallazgo A — Los 4 CNO de la BRN tenían SHA256 obsoletos (sistémico)

Las 4 CNO (BRN v2.1, dominios d01/d02/d03/d09) se ratificaron entre el **18 y 20 de julio**.
El Corpus Normativo se **reemplazó completo el 21 de julio** (`reingesta_replace.py`, nuevo
parser). El rechunking cambió el contenido exacto de cada chunk → cambió su SHA256, aunque el
**texto legal en sí no cambió**. Resultado: **26 de 34 eslabones (76%)** de la BRN citaban un
SHA256 que ya no existe en el corpus vigente — técnicamente, ninguna CNO estaba verificada
(Regla de Oro 3) desde el 21 de julio, sin que nadie lo detectara.

**Corrección:** recalculados los 26 SHA256 contra el corpus vigente, verificando primero que
cada chunk contiene el texto correcto (no solo el hash). Un caso (`COOTAD Art.60`, CNO-III) era
ambiguo (3 candidatos por ruido de chunking de otro documento) — resuelto por coincidencia
textual con la sumilla del YAML. Backup de los 4 archivos originales:
`data/backups/brn_pre_correccion_sha_20260723/`.

## Hallazgo B — CE Art.241 genuinamente perdido del corpus (no solo mal indexado)

El **fundamento_constitucional #1 de CNO-I-001** (d01) — *"la planificación garantizará el
ordenamiento territorial y será obligatoria en todos los GAD"* — no existía en el corpus: ni
indexado por `articulo_num`, ni mencionado en el texto de ningún chunk. Verificado contra el
DOCX original: el artículo **sí existe** en la fuente (`Constitución del Ecuador.docx`), es de
una sola oración, ubicado justo antes de "Capítulo segundo". El chunker lo perdió durante el
rechunking del 21-jul. Es el **único hueco** en los 444 artículos de la Constitución (no es un
patrón masivo) — pero cayó exactamente en el artículo que necesitábamos esta semana.

**Corrección:** re-extraído del DOCX, insertado como chunk aditivo (`id=22931`,
`sha256=c4565a2...`), embedding generado con el modelo local (`sentence-transformers`, no
consume presupuesto de Haiku). Corpus pasa de v1.0 a **v1.0.1** (hash maestro recalculado,
`docs/architecture/CORPUS_v1.0_MAESTRO.json`).

## Hallazgo C (menor) — COOTAD-2026 §198.1-198.6 y Disposición Transitoria: contenido íntegro, mal indexado

No es pérdida: es el mismo "límite conocido v1.1" ya documentado en `CORPUS_v1.0_CIERRE.md`. El
chunker etiquetó el bloque de reforma ("Artículo 4.- Agréguese...") bajo el número del artículo
reformatorio, no del artículo insertado. Contenido verificado íntegro; SHA256 recalculados
apuntando a los chunks reales (`id=15913` a `15919`).

## Lección de auditoría

Ninguno de estos tres hallazgos habría aparecido en una revisión superficial — todos requirieron
verificar **contra la fuente primaria** (el corpus real, el DOCX original), no contra la memoria
de lo que "debería" decir un documento ya ratificado. Confirma el principio que ya gobierna esta
fase del proyecto: verificar antes de escalar (migrar d02/d03/d09) es más barato que corregir
después de replicar el mismo patrón cinco veces.

## Propagación de la corrección

- `docs/brn/CNO-I/III/IV/IX-001.yaml` — 34/34 SHA256 verificados.
- `data/d01/catalogo_d01_v1.0.0.yaml` — sincronizado.
- Neo4j (grafo d01, nodos `:Articulo`) — sincronizado.
- `docs/architecture/CORPUS_v1.0_MAESTRO.json` — v1.0.1, hash maestro recalculado.

---
*OBS-012 · QUIRA Gov · Dylus Lab © 2026*
