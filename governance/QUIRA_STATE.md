# QUIRA_STATE.md — Estado Vivo del Proyecto

> **Documento de arranque obligatorio.** El `CLAUDE.md` exige leer este archivo como paso 2 de toda sesión.
> Single source of truth de: qué está abierto, qué está cerrado, en qué sprint, dónde vive cada cosa.
> **Actualizar este archivo al final de cada sesión que cambie el estado.**

**Última actualización**: 2026-06-02
**Sprint activo**: Sprint Constitucional — Grafo Neo4j + ADRs 016-020
**Fase**: Construcción del Cerebro 2 (Grafo Causal Constitucional)

---

## 0. ORIENTACIÓN RÁPIDA (leer en 60 segundos)

QUIRA es un **Knowledge Operating System** para gestión pública preventiva. No es dashboard ni BI.
Laboratorio: GAD Municipal de Montecristi (Ecuador). Destino: 221 municipios.

**Los 3 Cerebros:**
1. **Cerebro 1 — Memoria Normativa** (Supabase pgvector): 41 docs, 7,740 chunks. ✅ COMPLETO
2. **Cerebro 2 — Grafo Causal** (Neo4j AuraDB): 37 nodos, 55 aristas. 🔨 EN CONSTRUCCIÓN ACTIVA
3. **Cerebro 3 — Razonamiento** (Claude API + corpus + grafo): futuro

**Lo que se construyó en la sesión 2026-06-02 (la grande):**
El grafo constitucional dejó de ser hipótesis y empezó a **revelar estructura**. Se descubrió que la
participación ciudadana (Dom08) + rendición de cuentas (Dom09) forman un **par constitucional** que es
el nodo más central de todo el sistema — más que transparencia. Y que la soberanía popular (CE_1) es
visible computacionalmente como nodo apex.

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
- 41 docs · 7,740 chunks · pgvector 384dim · tabla `normativa_corpus`
- LOPC completa (94 chunks, Arts 1-101) · RES-CPCCS-RC-2026 (104 chunks)
- Modelo: `paraphrase-multilingual-MiniLM-L12-v2`

### Track B — ACK Registry v0.5 ✅ Gap cerrado
- `data/ack_registry.json` — **34 ACKs** · 4 NRCs funcionales + 1 NRC constituyente (CE_1)
- Los 15 LOPC ACKs + CPCCS_RC_2026 ya están sincronizados Neo4j↔JSON
- chunk_refs SHA256 verificados (excepto gaps: LOTAIP_47, LOPC_72)

### Track C — Neo4j Grafo (Cerebro 2) 🔨 ACTIVO
- **AuraDB Free · Instancia `6c134c35`** · 37 nodos · 55 aristas · 10 tipos de relación
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

## 6. PRÓXIMOS PASOS (orden priorizado — colega asesor 2026-06-02)

1. **RC 2025 metadatos completos** → agregar al Gold Master (fecha + CPCCS URL + calificación)
2. **Dom09 completo**: QLEP de COOTAD 266-270 + LOPC 88/92/96 + RES-CPCCS completo → Neo4j
3. **Re-run analítica** con Dom09 maduro → re-evaluar C3 con métricas estándar
4. **ADR-019 → CONFIRMED** SOLO si el grafo maduro lo sostiene (no antes)
5. **LOPC completa**: atomizar los ~80 artículos restantes (núcleo Dom08-Core ya hecho)
6. **Dom10/Dom12 DCOs** + COOTAD 295-310 (cierra capa técnica)

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
