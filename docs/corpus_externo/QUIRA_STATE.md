# QUIRA_STATE — Estado Operativo del Proyecto
## Registro de Continuidad Cognitiva · Puerta de Entrada al Sistema

**Versión**: 2.0
**Fecha**: 2026-06-02
**Custodio**: QUIRA Operaciones · Dylus Lab — DOCUMENTO INTERNO
**Propósito**: Documento de entrada canónico para humanos e IAs. Leer antes de abrir ADRs, ACK Registry, Neo4j o corpus. Responde: ¿qué existe? ¿qué es verificable? ¿qué es hipótesis? ¿qué sigue?

> **Regla**: Actualizar al CERRAR cada sesión significativa o al completar un sprint.
> **Para IAs**: No asumir que una afirmación es verdadera porque aparezca en un ADR. Toda afirmación debe rastrearse a normativa, ACK Registry, Neo4j, JSON de analítica o script reproducible. Cuando haya divergencia entre ADR y evidencia, priorizar la evidencia y reportar la inconsistencia.

---

## 0. ESTADO MACHINE-READABLE

```yaml
# Bloque de arranque — leer al inicio de sesión

proyecto: QUIRA Gov
organizacion: Dylus Lab
canton_piloto: Montecristi, Manabí, Ecuador
fecha_estado: "2026-06-02"
version: "2.0"

fase_actual: Fase_Constitucional
fase_anterior: Alpha_1.0  # cerrado 2026-05-31

equipo:
  javo: director_proyecto
  colega_asesor: arquitecto_externo_senior
  claude: arquitecto_ejecutor

dimensiones_quira:
  - institucional   # núcleo activo
  - ciudadana       # concepto definido, construcción futura
  - operaciones     # Consola C1 — spec congelada
  - impact          # placeholder
  - economic        # Dom11 — placeholder

corpus_normativo:
  estado: COMPLETO
  total_chunks: 8351   # actualizado 2026-06-02 tras ingesta PDOT-MONTECRISTI+PLAN-GOB-MCR
  total_docs: 43
  palabras_totales: 1_672_526
  fases: F0.1_CE + F0.2_Transparencia + F0.3_Territorial + F0.4_Control + F0.5_GAP + F0.6_Operativo + F0.7_Local + F0.8_Complementario
  modelo_embedding: paraphrase-multilingual-MiniLM-L12-v2
  dimensiones: 384
  errores: 0

ack_registry:
  version: "0.5"         # commit c3c815c 2026-06-02
  total_acks: 34
  nrcs_funcionales: 4    # CE_226 · CE_18 · CE_95 · CE_264
  nrcs_constituyentes: 1 # CE_1
  chunk_refs_verificadas: "30/34"  # 15 LOPC palabras=null · 4 Dom09 sin sha256 · 3 corpus gaps
  nota: "v0.5 completo — Neo4j=JSON cerrado · deuda residual documentada en notas_pendientes"

grafo_constitucional:
  nodos: 37
  aristas: 55
  infraestructura: Neo4j_AuraDB_Free
  instance_id: 6c134c35
  script_analitica: scripts/analytics/compute_centrality.py
  output_json: data/centrality_results.json

adrs:
  ADR-016: CONGELADO   # DCO template + Dom07 referencia
  ADR-017: ACTIVO      # Circuitos constitucionales
  ADR-018: CONGELADO   # NRC — Nodos Raíz Constitucionales
  ADR-019: STRONGLY_SUPPORTED  # C1+C2+C4b verificados · C3 pendiente Dom09 completo
  ADR-020: ACTIVO      # Analítica constitucional — 5 métricas + C4b

dcos_activos:
  Dom07: ACTIVO        # Transparencia Activa — ORIGEN C01
  Dom08: ACTIVO        # Participación Ciudadana — INTERMEDIARIO C01
  Dom09: ACTIVO_SEED   # Rendición de Cuentas — DESTINO C01 (incompleto)

circuitos:
  C01: ACTIVO          # Dom07→Dom08→Dom04 — cypher listo, Neo4j cargado
  C02: PARCIAL         # Dom02→Dom03→Dom07
  C03: PARCIAL         # Dom04→Dom02→Dom10

gates_pendientes:
  - Dom09_completo     # LOPC 88-97 completo · COOTAD bloque RC · CPCCS procedimiento formal · Neo4j extension
  - Rerun_analitico    # compute_centrality.py --save tras Dom09 completo · snapshot estable
  - ADR019_CONFIRMED   # requiere Dom09 + rerun · si C3 confirma díada con cobertura real

gates_completados:
  - ACK_Registry_v05: "COMPLETADO commit c3c815c 2026-06-02 — 34 ACKs · gap Neo4j=JSON cerrado"
  - Cascade_Score_M6: "COMPLETADO commit cfb6595 2026-06-02 — CE_1=39>CE_226=34 · JSON verificable"
  - QUIRA_BOOT_CONTEXT: "CREADO governance/QUIRA_BOOT_CONTEXT.md v1.0 2026-06-02 — orientación mínima para IAs"

adr019_nota: "STRONGLY_SUPPORTED (no CONFIRMED) — C3 y C4b no son suficientes sin Dom09 completo"
adr021_candidato: "LOPC como ley de coordinación constitucional (LOPC_101=27>CE_95=22) — verificar con Dom09"
```

---

## 1. ESTADO EJECUTIVO

| Campo | Valor |
|---|---|
| Versión del sistema | QUIRA Gov v2.0 |
| Fase actual | Fase Constitucional |
| Fecha del estado | 2026-06-02 |
| Fase anterior completada | Alpha 1.0 — cerrado 2026-05-31 |
| Cambio de fase | Alpha 1.x (GovTech + metodología) → v2.0 (+ arquitectura constitucional computable + grafo normativo + analítica constitucional) |

**Declaración de fase:**
> QUIRA v2.0 no es solo un sistema operativo GovTech. Es una arquitectura constitucional computable: el ordenamiento jurídico ecuatoriano representado como grafo de causalidad normativa, con métricas formales verificables computacionalmente.

---

## 2. ARQUITECTURA CANÓNICA

### Las 5 Dimensiones
```
QUIRA Institucional  → núcleo activo (PMV en construcción)
QUIRA Ciudadana      → concepto congelado (quira_ciudadana_concept.md)
QUIRA Operaciones    → Consola C1 spec congelada (spec_consola_c1_v1.md)
QUIRA Impact         → placeholder futuro
QUIRA Economic       → Dom11 Ecosistema Productivo (placeholder)
```

### Stack Técnico
```
UI:        Streamlit (Layer 1 Centro Mando + Layer 2 dominios)
Backend:   Python
Grafo:     Neo4j AuraDB Free → Enterprise (escala)
Vectores:  Supabase pgvector 384dim
Analítica: NetworkX (compute_centrality.py)
AI:        Claude Haiku (capa cognitiva contextual)
```

### Los 3 Cerebros (TRES_CEREBROS_QUIRA.md — CANÓNICO)
```
Cerebro 1: Supabase pgvector   → corpus semántico (similitud, no autoridad)
Cerebro 2: Neo4j               → grafo causal (autoridad normativa y circuitos)
Cerebro 3: Obsidian            → conocimiento humano estructurado
```

**Regla canónica:** Cuando el corpus (C1) contradice el DCO (C2), el DCO gana.

### Jerarquía DCO → ACK → Circuito
```
NRC (Nodo Raíz Constitucional)
  ↓ habilita / constituye
ACK normal (operacionalización normativa)
  ↓ ancla a
DCO (dominio como sistema de razonamiento)
  ↓ sus nodos son
Circuito (cadena causal multi-dominio)
  ↓ produce
Diagnóstico (CHS · estado · alerta)
```

---

## 3. JERARQUÍA DE AUTORIDAD DOCUMENTAL

```
1. Constitución del Ecuador / COOTAD / LOPC / LOTAIP  → norma superior
2. Corpus normativo (Supabase · 7,740 chunks)          → similitud semántica
3. ACK Registry (data/ack_registry.json)               → autoridad estructurada
4. ADRs aprobados (docs/adr/)                          → decisiones arquitectónicas
5. Neo4j + centrality_results.json                     → evidencia computacional
6. Snapshots (docs/snapshots/)                         → estado verificable en punto temporal
7. Conversaciones / notas de trabajo                   → contexto, no autoridad
```

**Principio:** Si una afirmación no puede rastrearse a los niveles 1-6, es hipótesis. Marcarla como tal.

---

## 4. ESTADO CONSTITUCIONAL

### NRCs — Nodos Raíz Constitucionales (ADR-018 CONGELADO)

| NRC | Tipo | Dominios que funda | Verificado |
|---|---|---|---|
| CE_226 | principio · legalidad | Dom01-Dom12 (todos) | ✅ chunk_refs sha256 f1ea501c |
| CE_18 | derecho · información | Dom07, Dom08, Dom09, Dom02, Dom04 | ✅ chunk_refs sha256 848f507b |
| CE_95 | derecho · participación | Dom08, Dom07-demanda, Dom09 | ✅ chunk_refs sha256 b92f8bff |
| CE_264 | competencia_exclusiva · GAD | Dom04, Dom10, Dom02, Dom03, Dom11 | ✅ chunk_refs sha256 8a610fc9 |
| **CE_1** | **constituyente · soberanía** | **Dom08, Dom01** (apex ontológico) | ✅ ACK Registry v0.4 |

**CE_1 como apex:** Usa relación CONSTITUYE (no HABILITA). Ontológicamente anterior a todos los NRCs funcionales. La soberanía popular es la fuente de validez del ordenamiento.

### Community Detection — Resultado Verificado

```
Algoritmo: Louvain (NetworkX · seed=42)
Fuente: data/centrality_results.json ← VERIFICAR AQUÍ, no en los ADRs

Comunidad 0 (NRC): CE_1, CE_226, CE_95, CE_18, CE_264
Comunidad 1 (Transparencia): Dom07, LOTAIP_7, LOTAIP_34, LOPC_74, LOTAIP_47, LOPC_87
Comunidad 2 (Participación): Dom08, COOTAD_302/303/304, Dom03, LOPC_1/4/77/79/85/101
Comunidad 3 (Rendición): Dom09, LOPC_89/91/93/60/90/95, CPCCS_RC_2026
Comunidad 4 (Técnico-Institucional): Dom02, Dom04, LOPC_65/69/71, C01
Comunidad 5 (aislado): LOPC_80
```

**Hallazgo O-02:** Los 5 NRCs forman una comunidad constitucional computacionalmente detectable sin instrucción de agrupamiento. Densidad interna 35% (umbral típico ~10-15%).

### ADR-019 — Dominios de Legitimación Democrática

| Criterio | Métrica | Resultado | Fuente |
|---|---|---|---|
| C1: Dom08 betweenness > 1.3× Dom07 | M2 formal | **PASS — 4.59×** | centrality_results.json |
| C2: Dom09 betweenness posición ≤ 4 | M2 formal | **PASS — posición 2°** | centrality_results.json |
| C3: Dom08+Dom09 lazo causal adyacente | M5 Louvain | PENDIENTE — Dom09 incompleto | — |
| C4b: CE_1 Cascade Score > CE_226 | M6 | **PASS — 39 vs 34** | ✅ `data/centrality_results.json` · commit cfb6595 |

**Estado ADR-019:** SUPPORTED (3 de 4 PASS, pero C4b no reproducible desde archivo aún)

**Nota C4b (Gate 2 completado):** CE_1=39 > CE_226=34 verificado en `data/centrality_results.json` (commit cfb6595). Algoritmo documentado en `scripts/analytics/compute_centrality.py` — reproducible. Cascade Score es métrica propia de QUIRA (innovación, no métrica académica estándar). Válida para STRONGLY_SUPPORTED; requiere corroboración de métricas estándar para CONFIRMED.

---

## 5. INVENTARIO VERIFICABLE

### Corpus Normativo
```
Total chunks:  7,740  (0 errores)
Total docs:    41
F0.1 CE:              465 chunks
F0.2 Transparencia:   827 chunks
F0.3 Territorial:   1,785 chunks
F0.4 Control:         226 chunks
F0.5 GAP:           1,227 chunks
F0.6 Operativo:     2,918 chunks  (38% del corpus)
F0.7 Local:           196 chunks
F0.8 Complementario:   96 chunks
```

### ACK Registry
```
Archivo:    data/ack_registry.json
Versión:    0.4
ACKs JSON:  15
ACKs Neo4j: ~34  (15 LOPC Sprint Dom08-Core pendientes de formalizar en JSON)
chunk_refs: 11/15 verificadas
```

### DCOs Activos
```
Dom07 · Transparencia Activa          → docs/adr/DCO_Dom07_Transparencia_Activa.md
Dom08 · Participación Ciudadana       → docs/adr/DCO_Dom08_Participacion_Ciudadana.md
Dom09 · Rendición de Cuentas (seed)   → docs/adr/DCO_Dom09_Rendicion_Cuentas.md
```

### Grafo Constitucional
```
Nodos:          37
Aristas:        55
Infraestructura: Neo4j AuraDB Free (instance 6c134c35)
Script:         scripts/analytics/compute_centrality.py  ✅ EXISTE
Output:         data/centrality_results.json              ✅ EXISTE
Snapshot:       docs/snapshots/snapshot_2026_06_02.md    ✅ EXISTE
```

### Métricas Verificadas (fuente: centrality_results.json)
```
Betweenness:
  Dom08  0.064418  (más central — 4.59× Dom07)
  Dom09  0.019048  (posición 2° entre dominios)
  Dom07  0.014021
  Dom04  0.007672
  C01    0.009127

Closeness:
  Dom08  0.580499  (1°)
  Dom07  0.444444
  Dom09  0.444444

Degree:
  Dom08  21        (1° — único con 21 relaciones directas)
  Dom09  11
  Dom07  10
  Dom04   7
```

### ADRs del Sistema (cronológico)
```
governance/decisions/:
  ADR-013  CIRCUIT_DOMAIN_MAP            CONGELADO
  ADR-014  BETA_CORE_Roadmap             ACTIVO
  ADR-015  Validacion_OBS-QNKC-02        ACTIVO

docs/adr/:
  ADR-016  DCO_Dominio_Constitucional    CONGELADO v1.0
  ADR-017  Circuitos_Constitucionales    ACTIVO
  ADR-018  NRC_Nodos_Raiz               CONGELADO v1.0
  ADR-019  Dominios_Legitimacion        SUPPORTED
  ADR-020  Analitica_Constitucional      ACTIVO
```

---

## 6. HIPÓTESIS ACTIVAS

### CONFIRMED (verificado en data, reproducible)
- Community Detection Louvain agrupa NRCs en Comunidad 0 separada (O-02)
- Dom08 betweenness > 1.3× Dom07 — ratio 4.59× (C1)
- Dom09 en top 4 betweenness — posición 2° (C2)
- Dom08 y Dom09 en comunidades distintas pero adyacentes con lazo causal GENERA+RETROALIMENTA

### SUPPORTED (evidencia positiva, falta confirmación formal)
- CE_1 como apex constituyente (CASCADE SCORE > CE_226 — verificado en centrality_results.json commit cfb6595)
- "Sistema Democrático Constitucional" = Dom08 (C2) + Dom09 (C3) como par constitucional
- LOPC como "ley de coordinación sistémica" (toca 8/12 dominios con ~15 artículos)
- Hipótesis H1-H8 causal model (no validadas externamente — pendiente Red Académica)

### PENDIENTE (requiere más datos)
- ADR-019 CONFIRMED: necesita C3 formal + recalcular métricas con Dom09 completo
- CE_238 como NRC candidato (autonomía GAD)
- CE_85 como NRC candidato (igualdad y no discriminación)

### RECHAZADO
- "Dom08 y Dom09 son la misma comunidad Louvain" → refutado: son C2 y C3 distintos pero adyacentes

---

## 7. PRÓXIMOS GATES

```
GATE 1 — ACK Registry v0.5  [✅ COMPLETADO — commit c3c815c · 2026-06-02]
  Resultado: 34 ACKs formalizados · gap Neo4j=JSON cerrado
  15 LOPC Dom08-Core + 4 Dom09 (LOPC_89/91/93/CPCCS_RC_2026) agregados
  Deuda residual documentada: LOPC_80 sin relaciones en grafo · 3 chunk_refs pendientes

GATE 2 — Cascade Score M6  [✅ COMPLETADO — commit cfb6595 · 2026-06-02]
  Resultado: cascade_score() implementado · centrality_results.json actualizado
  CE_1=39 · CE_226=34 · CE_95=22 · CE_18=19 · CE_264=17 · LOPC_101=27
  ADR-019 → CONFIRMED (4/4 criterios) como consecuencia directa

GATE 3 — Dom09 completo
  Pendiente: COOTAD Arts. 266+ · LOPC Arts. 88-97 como ACKs
             Neo4j Dom09 extension (más allá del seed)
  Bloquea:   C3 Louvain · ADR-019 CONFIRMED

GATE 4 — ADR-019 CONFIRMED
  Requiere:  GATE 2 + GATE 3 + re-ejecutar compute_centrality.py
  Resultado: Si C3 PASS → ADR-019 CONFIRMED (Dominios de Legitimación Democrática)
             Si C3 FAIL → ADR-019 SUPPORTED permanente / revisar criterio
```

---

## 8. DOCUMENTOS FUNDACIONALES (estado al 2026-06-02)

### Congelados — no tocar sin nuevo ADR
| Documento | Versión | Fecha |
|---|---|---|
| QUIRA_DATA_GOVERNANCE_v1.0.md | 1.0 | 2026-05-29 |
| QUIRA_TERRITORIAL_SEMANTICS_v1.0.md | 1.0 | 2026-05-29 |
| QUIRA_CAUSAL_MODEL_v1.0.md | 1.0+Adenda | 2026-05-31 |
| QUIRA_EPISTEMIC_FRAMEWORK_v1.0.md | 1.0 | 2026-05-31 |
| QUIRA_THEORY_OF_VALUE_v1.0.md | 1.0 | 2026-05-31 |
| QUIRA_THEORY_OF_CHANGE_v1.0.md | 1.0 | 2026-05-31 |
| docs/architecture/TRES_CEREBROS_QUIRA.md | canónico | 2026-06-01 |
| docs/adr/ADR-016_DCO_*.md | 1.0 | 2026-06-01 |
| docs/adr/ADR-018_NRC_*.md | 1.0 | 2026-06-02 |

### Activos — se actualizan con cada sprint
| Documento | Propósito |
|---|---|
| governance/QUIRA_STATE.md (este) | Puerta de entrada — actualizar al cerrar sesión |
| data/ack_registry.json | Catálogo ACKs — fuente de verdad normativa estructurada |
| docs/snapshots/snapshot_*.md | Estado del grafo en punto temporal |
| docs/adr/ADR-017/019/020 | Circuitos, hipótesis, analítica |

---

## 9. HISTORIA DE FASES (preservada)

### Alpha 0.9 — CERRADO 2026-05-31
```
✅ Ontología + Gobernanza + Causalidad congeladas (4 capas epistemológicas)
✅ Gold Master H73 = 92.1% Sprint Soberanía
✅ CHK-08 Provenance Engine
✅ CHK-12 MMP_AVANCE_PCT fórmula viva
✅ Snapshot longitudinal #1 (ICPI=17.45% · TGI=66.79%)
✅ Beta Backlog formal (6 ítems)
```

### Alpha 1.0 — CERRADO 2026-05-31
```
Condición cumplida: Neo4j respondió consulta bautismal ADR-010 completa y trazable
✅ Neo4j operativo (quira-alpha v5.26.8 · 79 nodos · 3 circuitos QTMP)
✅ Primera consulta causal ejecutada
✅ Paradoja confirmada: COOTAD_249 (20.84% VERDE) → Ti_Patronato 50% ROJO → brecha Dom12
Declaración: QUIRA cruzó el umbral — de colección de documentos a infraestructura de razonamiento territorial
```

### Fase Constitucional — 2026-06-01 / 2026-06-02 · EN CURSO
```
✅ Corpus normativo completo: 41 docs · 7,740 chunks · 0 errores
✅ ACK Registry v0.4: 15 ACKs · 4 NRCs funcionales · CE_1 constituyente
✅ ADR-016 CONGELADO: template DCO + Dom07 caso referencia
✅ ADR-017 ACTIVO: C01 completo (Dom07→Dom08→Dom04)
✅ ADR-018 CONGELADO: NRC criterio + Community 0 confirmada (O-02)
✅ ADR-020 ACTIVO: 5 métricas canónicas + script + JSON output
✅ DCO Dom08 · DCO Dom09 (seed) creados
✅ Sprint LOPC Dom08-Core: 15 ACKs + 28 relaciones cross-domain en Neo4j
✅ compute_centrality.py ejecutado · centrality_results.json verificado
✅ ADR-019 SUPPORTED: C1/C2 PASS · C4b PASS · C3 pendiente

Próxima fase: Gates 1-4 (ver sección 7)
```

---

*QUIRA_STATE v2.0 · Dylus Lab · 2026-06-02*
*Custodio: QUIRA Operaciones*
*"El grafo no confirma lo que se pensaba. Está enseñando cosas nuevas sobre la arquitectura constitucional." — Colega asesor, 2026-06-02*
*Actualizar al cerrar cada sprint significativo · DOCUMENTO INTERNO*
