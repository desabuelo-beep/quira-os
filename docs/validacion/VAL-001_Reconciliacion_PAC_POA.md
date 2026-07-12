# VAL-001 · Validación Empírica — Reconciliación PAC↔POA (Motor de Biografía)

**Estado:** revisión de precisión hecha (~99% tras excluir ambiguas) · revisión ciega independiente pendiente · 2026-07-11
**Origen:** recomendación del colega (asesor) — *"FASE V · Validación Empírica"*: el 92% de cobertura
no es un resultado científico hasta medir **precisión** con revisión humana de una muestra. Correcto,
y adoptado. Antes de Fase 2 (Neo4j), se mide la calidad de lo ya reconciliado.
**Relacionado:** ADR-032 (Motor de Biografía) · `scripts/enrich_poa_multianio.py` (`_contratos_2025_por_meta`).

---

## Qué se mide

La atribución de contratos por meta se hace por **reconciliación intersistémica PAC↔POA por descripción**
(`SequenceMatcher`, restringida a la misma partida económica). El "92%" era **cobertura** (procesos con
match ≥0.55), NO **precisión** (¿el match es correcto?). Aquí se separan.

## Métricas automáticas (2025 · 100 reconciliaciones)

| Confianza (similitud) | n | % |
|---|---|---|
| ≥ 0.90 (casi idéntico) | 62 | 62% |
| 0.80 – 0.90 (fuerte) | 21 | 21% |
| 0.70 – 0.80 (buena) | 9 | 9% |
| < 0.70 (marginal) | 8 | 8% |
| **ALTA confianza (≥0.80)** | **83** | **83%** |
| **AMBIGUAS** (2ª meta candidata a <0.08) | **2** | **2%** |

**Hallazgo de la validación:** los marginales (<0.70) resultaron ser mayormente **correctos** que bajaban
por acentos/mayúsculas (*"PÓLIZA"* vs *"POLIZA"*) — un **falso negativo del normalizador**, ya corregido
(transliteración de acentos). Los residuales genuinamente dudosos son servicios transversales (pólizas de
seguro) que pueden pertenecer a varias metas — el caso límite a revisar.

## Revisión de precisión (director + Javo · 2026-07-11)

Revisados los 100 matches con **contexto completo** (PAC ↔ POA ↔ meta), cruzando con las marcas de Javo:
- **Precisión estimada ~97-98%** a nivel de meta. La gran mayoría son descripciones casi idénticas del
  mismo trabajo real (combustible→vehículos, parque La Huella→IVU, estudio de suelo→equipamiento…).
- **Los errores se concentraban en las `ambigua: true` (2%)** — 2º candidato con meta distinta a score
  cercano. Ej: PAC *"control hidráulico y mitigación de riesgos"* mal atribuido a *"embellecimiento urbano"*
  (obras distintas). Javo detectó uno adicional (materiales de construcción → meta "puntos digitales").
- **Acción tomada:** el extractor ahora **EXCLUYE las ambiguas** (no atribuye cuando la meta no es decidible
  con certeza) → contratos **100 → 98**, precisión estimada **~99%**. Es exactamente donde vivían los errores.
- Nota: varios items administrativos caen bajo la meta *"instalaciones e infraestructuras"* (catch-all del
  propio POA) — correcto por fuente, aunque semánticamente laxo.

### Pendiente (para rigor pleno · tesis/CAF/GAD)
- Revisión **ciega e independiente** (no del constructor) de una muestra → precisión formal.
- **Recall** (procesos que debieron reconciliarse y no se reconciliaron) + matriz de confusión.

Con la exclusión de ambiguas, la entrada a Neo4j tiene ya **autoridad metodológica** razonable; la revisión
ciega la elevaría a estándar de publicación.

## Regla que deja esta validación

La reconciliación se **mide antes de propagarse al grafo**. Neo4j **expresa relaciones ya validadas**,
no las valida. Confianza automática ⇒ candidata; precisión humana ⇒ canónica.

---
*VAL-001 · Dylus Lab © 2026 · "Un buen resultado no es el que suena bien: es el que sobrevive a que lo midan."*
