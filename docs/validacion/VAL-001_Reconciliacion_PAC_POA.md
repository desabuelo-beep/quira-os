# VAL-001 · Validación Empírica — Reconciliación PAC↔POA (Motor de Biografía)

**Estado:** ABIERTO (automático hecho · revisión humana PENDIENTE) · 2026-07-11
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

## Lo que FALTA (por qué el estado es ABIERTO)

Lo anterior es **confianza automática, no precisión verificada por humano.** Pendiente:
- **Revisión humana** de la muestra `data/validacion_reconciliacion_2025.json` (100 matches, campo
  `revision_humana` = OK/ERROR) → **precisión real** (aciertos/total).
- **Matriz de confusión** + **recall** (procesos que debieron reconciliarse y no).
- Documentar los **casos límite** (servicios transversales).

Con ese informe, la entrada a Neo4j tiene **autoridad metodológica** (colega) — apto para tesis/CAF/GAD.

## Regla que deja esta validación

La reconciliación se **mide antes de propagarse al grafo**. Neo4j **expresa relaciones ya validadas**,
no las valida. Confianza automática ⇒ candidata; precisión humana ⇒ canónica.

---
*VAL-001 · Dylus Lab © 2026 · "Un buen resultado no es el que suena bien: es el que sobrevive a que lo midan."*
