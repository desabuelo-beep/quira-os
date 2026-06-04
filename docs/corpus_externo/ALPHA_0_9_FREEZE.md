# ALPHA_0_9_FREEZE — Congelamiento Formal de Alpha 0.9
## Registro de Estado Verificable al Cierre de Fase

**Estado**: CONGELADO  
**Fecha de cierre**: 2026-05-31  
**Versión de congelamiento**: Alpha 0.9  
**Custodio**: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO

> Este documento sigue la práctica de congelamiento formal de Palantir:
> registra qué EXISTE verificablemente, qué fue EXCLUIDO deliberadamente,
> y cuáles son las condiciones de entrada a Alpha 1.0.
> No es un resumen. Es un contrato.

---

## I. QUÉ EXISTE — VERIFICABLE

### Capa 1 — Gobernanza documental

| Artefacto | Ruta | Versión | Verificable |
|---|---|---|---|
| Data Governance | `governance\QUIRA_DATA_GOVERNANCE_v1.0.md` | 1.0 | ✅ existe |
| Territorial Semantics | `governance\QUIRA_TERRITORIAL_SEMANTICS_v1.0.md` | 1.0 | ✅ existe |
| Causal Model + C10 + Adenda | `governance\QUIRA_CAUSAL_MODEL_v1.0.md` | 1.0+adenda | ✅ existe |
| Beta Backlog | `governance\QUIRA_BETA_BACKLOG.md` | vivo | ✅ existe |
| QUIRA_STATE | `governance\QUIRA_STATE.md` | 1.0 | ✅ existe |
| MAPA Ecosistema | `MAPA_ECOSISTEMA_QUIRA.md` | 2.0 | ✅ existe |
| ALPHA_0_9_FREEZE (este) | `governance\ALPHA_0_9_FREEZE.md` | 1.0 | ✅ existe |
| ADRs (9 decisiones) | `governance\decisions\ADR-001 a ADR-009` | 1.0 | ✅ existen |

### Capa 2 — Datos y Gold Master

| Artefacto | Ruta | Estado |
|---|---|---|
| Gold Master canónico | `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | ✅ activo |
| Gold Master freeze | `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_20260526.xlsx` | ✅ snapshot 2026-05-26 |
| H73 métricas calculadas | Gold Master tab H73 | ✅ 58/63 = 92.1% |
| Provenance engine | Gold Master + Supabase | ✅ CHK-08 completado |
| MMP_AVANCE_PCT | Gold Master fórmula viva | ✅ CHK-12 completado |
| Snapshot longitudinal #1 | Supabase | ✅ ICPI=17.45%, TGI=66.79%, 2026-05-26 |

### Capa 3 — QTMP Schema v1.1

| Elemento | Archivo | Estado |
|---|---|---|
| Schema v1.1 (5 campos nuevos) | `quira-os\data\qtmp\qtmp_schema.yaml` | ✅ congelado |
| Canton registry | `quira-os\data\qtmp\qtmp_canton_registry.yaml` | ✅ existe |
| Circuito GAP_10PCT | `quira-os\data\qtmp\qtmp_ECU-13-MONTECRISTI_GAP_10PCT.yaml` | ✅ con datos P2 |
| Circuito AGUA_POTABLE | `quira-os\data\qtmp\qtmp_ECU-13-MONTECRISTI_AGUA_POTABLE.yaml` | ✅ cargado |
| Circuito EQUIDAD | `quira-os\data\qtmp\qtmp_ECU-13-MONTECRISTI_EQUIDAD.yaml` | ✅ cargado |

**Los 3 circuitos están en estado `listo_neo4j`.**

### Capa 4 — Hallazgo causal de Alpha

```
HALLAZGO FUNDACIONAL — Alpha 0.9:

COOTAD_249 cumplido (20.84% cod, 10% piso)
         ↓
Ti_Patronato_2025 = 50% (ROJO)
         ↓
PARADOJA: cumplir la ley no garantiza el impacto.

Este es el primer hallazgo causal verificable de QUIRA.
```

### Capa 5 — Epistemología operativa

| Concepto | Dónde vive | Estado |
|---|---|---|
| Tipos de dato: observado / calculado / derivado / proxy | QTMP schema v1.1 campo `naturaleza_valor` | ✅ operativo |
| `pendiente_microdato` | QTMP schema v1.1 campo `estado_dato` | ✅ operativo |
| `proxy_de` block | QTMP schema v1.1 | ✅ operativo |
| C10 — Reflexión Institucional | Causal Model Adenda Sec. XIV | ✅ formalizado |
| Principio 6 — Autocuración Metodológica | Causal Model Adenda Sec. XVI | ✅ formalizado |

---

## II. QUÉ FUE EXCLUIDO DELIBERADAMENTE

| Exclusión | Razón | Cuándo |
|---|---|---|
| Índices complementarios Piso 2 (Dom12) | No afecta Alpha. Fuente identificada. | Beta — `BETA-DOM12-001` |
| Desagregación Ti G71 vs G73 | Hallazgo C10 sin impacto en Alpha | Beta — `BETA-DOM12-002` |
| Efecto COOTAD reforma clasificación | Requiere validación académica | Beta — `BETA-DOM12-003` |
| PDOT Montecristi atomizado (QLEP) | Sprint dedicado en Beta | Beta — `BETA-DOM04-001` |
| Microdatos INEC DPA 2022 | Requiere alianza Red Académica | Beta — `BETA-TERRITORIO-001` |
| Calibración H1-H8 académica | Hipótesis marcadas, validación externa | Beta — `BETA-METODO-001` |
| Neo4j carga inicial | Decisión arquitectónica: grafo nace sobre base congelada | Sprint 2 Alpha 1.0 |
| Cédula Patronato dic-2025 | Dato externo SIGEF pendiente | Pendiente GADMCM |

**Principio de exclusión**: Ningún ítem excluido invalida Alpha 0.9. Son profundizaciones, no correcciones.

---

## III. QUÉ SE CONSIDERA TERMINADO

### Terminado = Verificable + No requiere revisión en Alpha

| Item | Criterio de completitud |
|---|---|
| Cadena causal QNKC-002 (C1-C10) | Documentada, hipótesis H1-H8 registradas como `hipotesis` |
| Los 12 dominios canónicos | Definidos con criterios ontológico/operativo/causal (ADR-010) |
| QTMP schema v1.1 | Congelado, 3 circuitos en estado `listo_neo4j` |
| Gold Master v5.5 con H73 = 92.1% | 58/63 métricas confirmadas |
| Snapshot longitudinal #1 | Punto de referencia temporal establecido |
| ProyecT como workspace | Reorganización ejecutada y documentada |
| 4 capas epistemológicas | Ontología → Gobernanza → Causalidad → Metacausalidad |

### Terminado con asterisco (pendiente validación externa)

| Item | Condición pendiente |
|---|---|
| Ratio_COOTAD_249 = 20.84% | Falta cédula Patronato dic-2025 → `pendiente_validacion` |
| H1-H8 hipótesis causales | Válidas como hipótesis; `validado_academico` requiere Red Académica |

---

## IV. CONDICIONES DE ENTRADA A ALPHA 1.0

Alpha 1.0 se declara cuando QUIRA cumple TODO lo siguiente:

```
CONDICIÓN 1 — Neo4j cargado
  ✓ Los 3 QTMPs ingestados como nodos y relaciones
  ✓ Hipótesis H1-H8 como edges tipados

CONDICIÓN 2 — Primera consulta causal ejecutada
  ✓ Query: ¿Por qué Montecristi tiene brechas Dom12 si cumple COOTAD_249?
  ✓ Respuesta: cadena causal completa (COOTAD_249 → Ti_Patronato → G73)
  ✓ Cada nodo trazable a fuente documental

CONDICIÓN 3 — Resultado verificable
  ✓ La cadena causal es reproducible
  ✓ Cualquier observador externo puede verificar cada paso

NO ES CONDICIÓN para Alpha 1.0:
  ✗ Cédula Patronato dic-2025 (puede estar pendiente)
  ✗ Validación Red Académica H1-H8 (es Beta)
  ✗ Nuevos circuitos o dominios (es Beta)
```

---

## V. DECLARACIÓN DE CIERRE

> Alpha 0.9 cierra habiendo construido lo que ningún sistema municipal ecuatoriano
> tiene hoy: una infraestructura epistemológica que no solo mide el territorio —
> sino que formaliza cómo sabe lo que sabe y reconoce explícitamente lo que aún
> no puede explicar.
>
> Eso no es un dashboard. Es una base de razonamiento territorial.
>
> Alpha 1.0 comenzará cuando el grafo responda su primera pregunta real.

---

*ALPHA_0_9_FREEZE v1.0 — Congelado 2026-05-31*  
*Este documento no se modifica. Solo Alpha 1.0 FREEZE lo sucede.*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
