# QUIRA_STATE.md — Estado Vivo del Proyecto

> **Documento de arranque obligatorio.** El `CLAUDE.md` exige leer este archivo como paso 2 de toda sesión.
> Single source of truth de: qué está abierto, qué está cerrado, en qué sprint, dónde vive cada cosa.
> **Actualizar este archivo al final de cada sesión que cambie el estado.**

**Última actualización**: 2026-06-02 (sesión 2 — sincronización post Gates 3-4)
**Sprint activo**: Sprint Constitucional — Gate 6 Semantic Mining
**Fase**: Transición Cerebro 2 consolidado → Semantic Mining del corpus completo

---

## 0. ORIENTACIÓN RÁPIDA (leer en 60 segundos)

QUIRA es un **Knowledge Operating System** para gestión pública preventiva. No es dashboard ni BI.
Laboratorio: GAD Municipal de Montecristi (Ecuador). Destino: 221 municipios.

**Los 3 Cerebros:**
1. **Cerebro 1 — Memoria Normativa** (Supabase pgvector): 41 docs, 7,740 chunks. ✅ COMPLETO
2. **Cerebro 2 — Grafo Causal** (Neo4j AuraDB): 37 nodos, 55 aristas. 🔨 EN CONSTRUCCIÓN ACTIVA
3. **Cerebro 3 — Razonamiento** (Claude API + corpus + grafo): futuro

**Lo que se construyó en sesiones 2026-06-02:**
El grafo constitucional dejó de ser hipótesis y empezó a **revelar estructura**. Dom08+Dom09 forman
el par constitucional más central. CE_1 es nodo apex computacional. COOTAD_266 cerró el ciclo
PP→RC→nuevo_PP normativamente (OBS-003 CONFIRMED). Corpus completo: 43 docs / 8,351 chunks.
Gates 3 y 4 completados. ADR-019 STRONGLY_SUPPORTED (no CONFIRMED — rigor epistemológico activo).

---

## 1. QUÉ ESTÁ CERRADO (CONGELADO — no re-litigar)

| Artefacto | Estado | Doc |
|---|---|---|
| Doctrina canónica "El Excel es el Estado" | CONGELADO 2026-05-26 | `docs/QUIRA_DOCTRINE_v1.md` |
| Arquitectura 4 capas + 12 dominios v2 | CONGELADO 2026-05-29 | `docs/ARQUITECTURA_CANONICA.md` |
| Constitución de Lenguaje (palabras prohibidas) | CONGELADO 2026-05-29 | `docs/GLOSARIO_INSTITUCIONAL.md` |
| ADR-016 — Template DCO (8 componentes) | CONGELADO | `docs/adr/ADR-016_*.md` |
| ADR-017 — Circuitos Constitucionales (C01 live) | ACTIVO | `docs/adr/ADR-017_*.md` |
| ADR-018 — NRC + O-02 (NRCs = comunidad detectable) | CONGELADO v1.0 | `docs/adr/ADR-018_*.md` |
| Corpus Normativo (Cerebro 1) | COMPLETO 2026-06-01 | `project_corpus_normativo` (memoria) |
| Gold Master v5.5_TGI | Canónico activo | `docs/GOLD_MASTER_v6_SCHEMA.md` |

---

## 2. QUÉ ESTÁ ABIERTO (en progreso o pendiente)

### Gates completados (actualización post sesión 2)
- **Gate 3 ✅** — COOTAD_266 cargado en Neo4j · OBS-003 creada · commit d66c2d3
- **Gate 4 ✅** — Re-run analítico (38n/58a) · COOTAD_266 → Comunidad 4 · commit 6c8a213
- **OBS-003 ✅ CONFIRMED** — COOTAD_266 es puente RC↔presupuesto/planificación (no Dom09 exclusivo)
- **Corpus ✅** — 41→43 docs, 7,740→8,351 chunks · commit 86f0c08

### Gate 6 — Motor de Trazabilidad Pública (EN PROGRESO)
  Gate 6.1a COMPLETADO: CANONICAL_CHUNK_SCHEMA.md v1.1 (Star Schema)
  Gate 6.1b COMPLETADO: DDL Supabase (documents + holding_structured_data + 8 cols corpus)
  Gate 6.2  COMPLETADO: 43 docs → tabla documents · 8,351 chunks clasificados
  Gate 6.3  PENDIENTE: manifest.py nuevos campos
  Gate 6.4  PENDIENTE: Normativa_Word delta
  Gate 6.5  PENDIENTE: Holding MCR (POA · PAC · RC · PP)
  Gate 6.6  PENDIENTE: Semantic Mining
  Gate 6.7  PENDIENTE: Re-evaluar ADR-019

### ADR-019 — Dominios de Legitimación Democrática → **STRONGLY_SUPPORTED**
Hipótesis: Dom08 + Dom09 forman una categoría arquitectónica distinta de los dominios operacionales.
No producen bienes/servicios — producen **legitimidad, control y mandato**.

**Evidencia a favor (computacional, en `data/centrality_results.json`):**
- C1 PASS: Dom08 betweenness=0.0644 = 4.6× Dom07 (umbral 1.3×)
- C2 PASS: Dom09 en top-4 betweenness (posición 2°)
- C4b PASS: CE_1 Cascade Score=39 > CE_226=34
- C3 reformulado: Dom08 (comunidad C2) y Dom09 (comunidad C3) son clusters DISTINTOS pero adyacentes, unidos por GENERA+RETROALIMENTA

**Por qué NO está CONFIRMED todavía** (rigor epistemológico, commit 3c98583):
Falta Dom09 completo + re-run con métricas estándar sobre snapshot estable. No se congela teoría
antes de que el grafo maduro hable. **NO cambiar a CONFIRMED sin completar Dom09.**

### ADR-020 — Analítica Constitucional → ACTIVO
6 métricas: degree, betweenness, closeness, eigenvector, community (Louvain), cascade score (M6).
Script: `scripts/analytics/compute_centrality.py` (NetworkX 3.6.1). Corre contra AuraDB.

### Dom09 — Rendición de Cuentas → DCO inicial, falta completar
Tiene 7 ACKs. Le faltan: COOTAD 266-270 (RC específica GAD) + LOPC 88,92,96 + RES-CPCCS completo.
Cuando se complete, re-evaluar C3 y considerar ADR-019 → CONFIRMED.

---

## 3. ESTADO DE LOS 3 TRACKS

### Track A — Corpus Supabase (Cerebro 1) ✅ COMPLETO
- **43 docs · 8,351 chunks** · pgvector 384dim · tabla `normativa_corpus`
- Incluye: PDOT Montecristi (594 chunks) + Plan GOB MCR (18 chunks) — commit 86f0c08
- Modelo: `paraphrase-multilingual-MiniLM-L12-v2`

### Track B — ACK Registry v0.6 ✅ Gap cerrado
- `data/ack_registry.json` — **35 ACKs** · 4 NRCs funcionales + 1 NRC constituyente (CE_1)
- Nuevo: COOTAD_266 (sha256 0f71df42) — ancla fiscal ciclo democrático — commit d66c2d3
- chunk_refs SHA256 verificados (excepto gaps documentados: LOTAIP_47, LOPC_72)

### Track C — Neo4j Grafo (Cerebro 2) 🔨 ACTIVO
- **AuraDB Free · Instancia `6c134c35`** · **38 nodos · 58 aristas** · 10 tipos de relación
- **CRÍTICO**: AuraDB Free usa el instance ID como username Y database name (no "neo4j")
- **CRÍTICO**: usar patrón `MATCH + MERGE` para relaciones (nunca `MERGE (anon)-[r]->(var)` — crea duplicados)
- Scripts:
  - `scripts/normativa/load_c01_neo4j.py` — 14 pasos C01 base + 10 queries validación
  - `scripts/normativa/extend_lopc_neo4j.py` — 15 LOPC ACKs + 7 dominios + 28 relaciones
  - `scripts/analytics/compute_centrality.py` — 6 métricas + veredicto ADR-019

**Relaciones canónicas (10 tipos):**
`CONSTITUYE` (CE_1→NRCs) · `HABILITA` (CE_226→NRCs) · `FUNDA` (NRC→Dominio) ·
`INSTRUMENTA` (ACK sectorial→Dominio) · `ALIMENTA` (Dominio→Circuito) · `INCLUYE` (Circuito→Dominio) ·
`INFORMA` (Dom07→Dom08) · `DEMANDA` (Dom08→Dom07) · `GENERA` (Dom08→Dom09) · `RETROALIMENTA` (Dom09→Dom08)

**Cadenas verificadas:**
```
CE_226 → CE_18 → Dom07 → C01      (cadena transparencia)
CE_226 → CE_95 → Dom08 → C01      (cadena participación)
CE_1 → CE_95 → Dom08 → 6 dominios (cadena soberanía)
Dom08 ⇄ Dom09                     (ciclo democrático: GENERA + RETROALIMENTA)
```

---

## 4. DCOs (Dominios Constitucionales Operacionalizables)

| Dominio | norma_fundante | chs_rol | Estado | Archivo |
|---|---|---|---|---|
| Dom07 Transparencia | CE_18 | ORIGEN | ACTIVO | (referencia ADR-016) |
| Dom08 Participación | CE_95 | INTERMEDIARIO | ACTIVO | `docs/adr/DCO_Dom08_*.md` |
| Dom09 Rendición Cuentas | CE_95 (misma raíz) | DESTINO | inicial — completar | `docs/adr/DCO_Dom09_*.md` |

**Hallazgo clave**: Dom08 y Dom09 comparten norma raíz (CE_95). Son "par constitucional" — el ciclo
operacional real en los GAD es: **PP (Presupuesto Participativo, Dom08-B) → Gestión → RC (Rendición, Dom09) → nuevo PP**.

---

## 5. EVIDENCIA DIGITAL VERIFICABLE (EDV)

Concepto canónico nuevo (2026-06-02): el video de un evento público es evidencia L0-digital, mandatada
por LOPC_101 (democracia electrónica). El nodo NO es "VIDEO" sino "Evidencia Digital Verificable".

`data/evidencia_digital_verificable.json`:

| Entidad | RC 2024 (gestión 2024, evento 2025) | RC 2025 (gestión 2025, evento 2026) |
|---|---|---|
| GAD Montecristi | youtube.com/watch?v=mqDT5jKXHW8 ✅ Gold Master | youtube.com/watch?v=Qexwg7EKmUo ⏳ pendiente Gold Master |

**Pendiente**: metadatos RC 2025 (fecha exacta evento, URL informe CPCCS, calificación ciudadana) + RC de los 3 entes del Holding.

---

## 6. PRÓXIMOS PASOS (actualizado post Gates 3-4 · colega asesor 2026-06-02)

**Gate 6 — Motor de Trazabilidad Pública (SIGUIENTE · ver ADR-021)**

ADR-021 ACTIVO — `docs/adr/ADR-021_Ontologia_Corpus_Motor_Trazabilidad.md`
Define: 4 Capas (A=Norma/B=Metodología/C=Instrumento/D=Evidencia) + authority_level + canton_id

Fuentes:
  Normativa_Word: `C:\...\ProyecT\Normativa_Word` (43 docs · Capas A+B)
  Holding MCR:    `C:\...\ProyecT\Holding_Municipal_Montecristi` (~90 docs · Capas C+D)

Secuencia Gates:
  Gate 6.1 ⏳ Schema Supabase: ADD COLUMN document_class + authority_level + canton_id
  Gate 6.2 ⏳ Migración corpus existente (43 docs → clasificar retroactivamente)
  Gate 6.3 ⏳ Delta Normativa_Word: ingestar lo que falta (skill /qlep-corpus)
  Gate 6.4 ⏳ Ingesta Holding MCR (Capas C+D) — evidencia de ejecución territorial
  Gate 6.5 ⏳ Datos estructurados LOTAIP → tabla holding_structured_data
  Gate 6.6 ⏳ Semantic Mining: densidad por dominio, circuitos emergentes
  Gate 6.7 ⏳ Re-evaluar ADR-019 con corpus completo

**Gate 5 — ADR-019 CONFIRMED** (después de Gate 6.7)
- NO antes. Dom09 necesita cobertura real del corpus completo
- Métricas estándar deben sostenerlo — no solo Cascade Score M6

**Pendiente paralelo (no bloquea Gate 6)**
- RC 2025 metadatos CPCCS → Gold Master (esperando plazos legales CPCCS)

---

## 7. MAPA DE DOCUMENTOS (dónde vive qué)

```
docs/QUIRA_DOCTRINE_v1.md       → doctrina operativa (fase pre-constitucional)
docs/ARQUITECTURA_CANONICA.md   → 4 capas + 12 dominios
docs/NORTH.md                   → visión / norte estratégico
docs/GLOSARIO_INSTITUCIONAL.md  → constitución de lenguaje (palabras prohibidas)
docs/architecture/TRES_CEREBROS_QUIRA.md   → arquitectura 3 cerebros
docs/architecture/FOUNDATION_LAYER_V1.md   → 5 pilares + modelo madurez L0-L5

docs/adr/ADR-016..020 + DCO_Dom08/09   → FASE CONSTITUCIONAL (lo nuevo, grafo)
governance/decisions/ADR-013..015      → fase operativa antigua (QTMP, BETA-CORE)
governance/QUIRA_STATE.md              → ESTE ARCHIVO (estado vivo)

data/ack_registry.json                 → 34 ACKs (Track B)
data/evidencia_digital_verificable.json → EDV registry
data/centrality_results.json           → última corrida analítica
docs/snapshots/snapshot_2026_06_02.md  → snapshot del grafo

Memoria Claude (~/.claude/.../memory/): índice en MEMORY.md
Skill /quira-orient → orientación rápida invocable
```

---

## 8. REGLAS CRÍTICAS (romper = dañar el proyecto)

1. **Excel primero, nunca PMV en aislamiento.** El Gold Master es la fuente de verdad. Nunca actualizar el PMV sin pasar por el Excel.
2. **Lo canónico no se nombra en UI pública.** Prohibido en pantallas/API/repo público: ICPI, TGI, Ti, QTMP, H-series (H01-H99), QNKC, PSG, IOC, IGP, IET. También node IDs internos (Dom07, C01, CE_226).
3. **Bloomberg Model.** Los IDs internos viven en código/governance/docs internos, JAMÁS en UI ciudadana.
4. **Prohibición absoluta de alucinación.** Nunca inventar números de artículo ni datos sin fuente verificada (corpus Supabase con SHA256).
5. **Sin norma, no hay indicador.** QUIRA solo observa como obligación lo que una norma ecuatoriana efectivamente manda.
6. **No congelar teoría antes de que el grafo hable.** ADR-019 sigue SUPPORTED a propósito.
7. **No commitear secretos.** `.streamlit/secrets.toml` está en .gitignore. Credenciales Neo4j/Supabase/Anthropic nunca al repo.
8. **Repo es PRIVADO.** github.com/desabuelo-beep/quira-os — mantener privado.

---

## 9. INFRAESTRUCTURA (sin secretos — credenciales en .streamlit/secrets.toml local)

| Servicio | Detalle | Notas |
|---|---|---|
| Neo4j AuraDB Free | Instancia `6c134c35` | user=DB=instance ID. Archivo creds: `C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Neo4j-6c134c35-Created-2026-06-02.txt` |
| Supabase | `normativa_corpus` pgvector | URI en secrets.toml [database] |
| Anthropic | Claude Haiku (Sentinel) | key en secrets.toml |
| GitHub | desabuelo-beep/quira-os (PRIVADO) | main branch, push directo |
| Streamlit Cloud | deploy automático desde main | secrets pegados en Settings |

---

*QUIRA_STATE.md · Mantener vivo · Actualizar al cierre de cada sesión que cambie el estado*
