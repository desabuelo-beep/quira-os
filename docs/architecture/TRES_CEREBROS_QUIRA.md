# QUIRA — Arquitectura de los Tres Cerebros

**Versión:** 1.0  
**Fecha:** 2026-06-01  
**Estado:** CONGELADO — aprobado Dylus Lab  
**Origen:** Sprint 4 (Corpus Normativo) · Análisis posterior a F0.1 + F0.2  
**Autores:** Dylus Lab (Javo + Claude)

---

## El descubrimiento

Antes de Sprint 4, QUIRA tenía dos cerebros implícitos: razonamiento causal (Neo4j/QTMP) y documentación humana (Obsidian). Con el corpus normativo operacional, emerge un tercer cerebro completamente distinto. Esta arquitectura formaliza los tres y sus interfaces.

---

## La Ley Cero — El Excel Canónico (no es un cerebro)

> **"El Excel Canónico es el Estado."**

El Excel Canónico no es un cerebro. Es el **legislador del sistema**. Los tres cerebros son operacionales — procesan, navegan, razonan. El Excel es constitucional — define qué es verdad. Ningún cerebro puede contradecirlo.

```
Excel Canónico (SIAP-ICPI_GOLD_MASTER_v5.5_TGI)
│
│  "Ley Cero" — establece indicadores, fórmulas, dominios, metodología
│
├──→ Cerebro 1 — Memoria Normativa
├──→ Cerebro 2 — Razonamiento Institucional
└──→ Cerebro 3 — Navegación Cognitiva Humana
```

**Regla:** Si un cerebro contradice al Excel, el cerebro está mal.

---

## Los Tres Cerebros

### CEREBRO 1 — Memoria Normativa
**Infraestructura:** Supabase + pgvector  
**Modelo:** paraphrase-multilingual-MiniLM-L12-v2 (384 dim)  
**Tabla:** normativa_corpus  

**Responde:**
- ¿Qué dice la norma sobre X?
- ¿Dónde está ese concepto en el ordenamiento jurídico?
- ¿Qué documento lo contiene?
- ¿Qué artículos se parecen semánticamente a esta pregunta?

**Lo que NO hace:**
- No sabe cuál norma *gobierna* (solo sabe cuál se *parece*)
- No razona sobre causalidad
- No establece jerarquía doctrinal

**Escala:** 41 documentos → ~5,000-6,000 chunks · F0.1-F0.8

---

### CEREBRO 2 — Razonamiento Institucional
**Infraestructura:** Neo4j + QTMP + Circuitos Constitucionales  
**Modelo:** QTMP (Quadrum Territorial Meta-Pattern) + ADR-013/ADR-016/ADR-017  
**Tabla:** qtmp_ECU-13-MONTECRISTI_*.yaml  

**Responde:**
- ¿Quién debe hacer qué, cuándo y con qué evidencia?
- ¿Qué depende de qué? (causalidad institucional)
- ¿Qué circuito está roto?
- ¿Qué consecuencia activa el incumplimiento?

**Lo que NO hace:**
- No busca texto normativo (usa ACK IDs como anclas)
- No explica a humanos (genera datos estructurados para algoritmos)
- No navega — razona

---

### CEREBRO 3 — Navegación Cognitiva Humana
**Infraestructura:** Obsidian (QUIRA_KB_Montecristi)  
**Modelo:** Wikilinks [[X]] + Graph View + Jerarquía 4 niveles  
**Estructura:** ver Sección "Jerarquía Obsidian"  

**Responde:**
- ¿Cómo entiendo este dominio completo?
- ¿Cómo se relacionan CE_18, LOTAIP_7 y Dom07?
- ¿Qué circuito involucra este dominio?
- ¿Cómo aprende el sistema un experto humano nuevo?

**Lo que NO hace:**
- No almacena chunks (eso es Cerebro 1)
- No razona en grafos (eso es Cerebro 2)
- No calcula indicadores (eso es el Excel)
- No replica vectores

**Valor único:** Convierte la topología legal-institucional en algo navegable para humanos. El Graph View de Obsidian es el único lugar donde la arquitectura completa de QUIRA es visible de un vistazo.

---

## El hallazgo epistemológico central (F0.1)

Durante la validación de F0.1 se consultó:

```
"¿Qué artículo fundamenta la transparencia activa?"
→ Cerebro 1 devuelve: Art.19 (score 0.572)
→ Doctrina canónica: Art.18
```

Esto reveló una distinción fundamental que ningún sistema RAG clásico puede resolver solo:

```
Cerebro 1 (corpus)   = similitud semántica   ≠   norma rectora
Cerebro 2 (QTMP)     = causalidad formal     ≠   texto normativo  
Cerebro 3 (Obsidian) = inteligibilidad humana ≠   razonamiento algorítmico
```

La norma rectora (Art.18) es una **decisión curatorial humana** que vive en el DCO (ADR-016), no en el embedding. El corpus encuentra proximidad. El DCO decide qué norma *gobierna*.

**Esto es el patrón QNKC recurrente:**
```
Corpus ≠ Doctrina
Modelo ≠ Validación
Publicación ≠ Transparencia efectiva
```

---

## Interfaces entre cerebros

Los cerebros no son silos. Tienen tres interfaces formales:

### Interface C1 → C3 (query canónica)
Cada nota dominio en Obsidian (Cerebro 3) tiene una `query_canonica` — la búsqueda semántica pre-diseñada que devuelve los chunks más relevantes del Cerebro 1.

```yaml
# En Dom07_Transparencia.md (Obsidian)
query_canonica_A: "¿Qué norma obliga al GAD a publicar información pública activamente?"
query_canonica_B: "¿Qué norma sustenta la participación ciudadana en decisiones del GAD?"
```

Esto resuelve el problema Art.18 vs Art.19: el Cerebro 3 sabe cuál es la pregunta correcta. El Cerebro 1 sabe buscar.

### Interface C2 → C3 (circuitos)
Cada circuito en Neo4j (Cerebro 2) tiene su nota correspondiente en Obsidian (Cerebro 3). El nombre del nodo Neo4j es el anchor del wikilink Obsidian.

```
Neo4j: CIRCUIT_TRANSPARENCIA_PARTICIPACION
Obsidian: [[C01_Transparencia_Participacion_Planificacion]]
```

### Interface C1 → C2 (ACK IDs)
Cada ACK en el Cerebro 2 tiene un `chunk_ref` que apunta a un sha256 del Cerebro 1. Cuando el razonamiento QTMP necesita citar la norma, puede recuperar el texto exacto del corpus.

```yaml
# En ACK CE_18
chunk_ref_sha256: "abc123..."  # sha256 del chunk correspondiente en normativa_corpus
```

---

## Jerarquía Obsidian — 4 Niveles

El error del modelo "1 nota = 1 artículo" es que invierte la jerarquía de consulta humana. Las personas piensan en dominios y circuitos, no en artículos. Los artículos son átomos.

```
Nivel 0 — CIRCUITO         ← punto de entrada operacional
  C01_Transparencia_Participacion_Planificacion.md
  → "¿Qué pasa si este circuito se rompe?"

Nivel 1 — DOMINIO (DCO)    ← punto de entrada analítico  
  Dom07_Transparencia.md
  → "¿Cómo funciona este dominio?"
  → consume [[CE_18]] [[LOTAIP_7]] [[Dom07A]] [[C01]]

Nivel 2 — INSTRUMENTO      ← síntesis por ley
  LOTAIP_Transparencia_GAD.md      ← YA EXISTE en vault backup
  CE_Principios_Estado_GAD.md      ← YA EXISTE en vault backup
  → "¿Qué hace esta ley?"
  → consume [[CE_18]] [[CE_226]] [[LOTAIP_34]]

Nivel 3 — ACK (átomo)      ← backing, no navegación primaria
  CE_18.md
  CE_226.md
  LOTAIP_7.md
  → "¿Qué dice exactamente este artículo?"
  → generado por /qlep
```

**Regla de navegación:** Un humano entra por Nivel 0 o 1. Llega a Nivel 3 solo cuando necesita el texto exacto. Un algoritmo consulta directamente Nivel 3 o el Cerebro 1.

**Los niveles 2 (Instrumentos) ya existen en el vault backup.** Se enriquecen con wikilinks hacia ACKs, no se reescriben.

---

## Anti-patrones formales

| Anti-patrón | Por qué falla |
|---|---|
| Obsidian como base vectorial | Duplica Cerebro 1, sin la ventaja de búsqueda semántica |
| Obsidian como Neo4j | Duplica Cerebro 2, sin la ventaja del razonamiento causal |
| "1 nota = 1 artículo" como navegación principal | 3,000+ notas hacen el vault innavegable; Art.18 solo importa en contexto de Dom07 |
| Usar corpus para decidir qué norma gobierna | Cerebro 1 mide similitud, no autoridad jurídica |
| Crear notas Dominio antes de tener ACKs | La síntesis prematura produce documentación sin sustancia |
| Confundir circuito con dominio | Un circuito atraviesa múltiples dominios; un dominio puede participar en múltiples circuitos |

---

## La topología completa de QUIRA

```
                    ┌─────────────────────┐
                    │    Excel Canónico    │
                    │  (Ley Cero — define) │
                    └─────────┬───────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐  ┌────────────────┐  ┌───────────────────┐
│   CEREBRO 1     │  │   CEREBRO 2    │  │    CEREBRO 3      │
│  Supabase +     │◄─┤  Neo4j + QTMP  │  │  Obsidian         │
│  pgvector       │  │  + Circuitos   │◄─┤  QUIRA_KB_        │
│                 │  │                │  │  Montecristi      │
│  ¿Qué dice?    │  │  ¿Quién debe?  │  │  ¿Cómo entiendo?  │
│  ¿Dónde está?  │  │  ¿Qué depende? │  │  ¿Cómo se conecta?│
└────────┬────────┘  └───────┬────────┘  └─────────┬─────────┘
         │                   │                     │
         └─────── Interface: ACK IDs + sha256 ─────┘
                             │
                    ┌────────▼───────┐
                    │    QUIRA UI    │
                    │  Streamlit +   │
                    │  Sentinel      │
                    └────────────────┘
```

---

## Consecuencias de esta arquitectura

1. **Cada pregunta tiene un cerebro dueño.** Antes de responder, QUIRA debe clasificar la pregunta. La clasificación es parte del diseño de Sentinel.

2. **ADR-016 (DCO) es el artefacto de integración.** El DCO es el único artefacto que habla los tres idiomas: lista las normas fundantes (para Cerebro 1), los circuitos (para Cerebro 2), y tiene la nota Obsidian (para Cerebro 3).

3. **Obsidian no se construye directamente — emerge del QLEP.** Cada `/qlep` execution produce un ACK que incluye su formato Obsidian. La bóveda crece con los ACKs.

4. **El vault backup existente (Nivel 2) es válido y permanece.** Las 39+ notas actuales no se modifican. Solo se añaden niveles 0, 1 y 3.

---

*QUIRA Gov · Dylus Lab © 2026*  
*Siguiente: ADR-016 (DCO) — Dom07 como caso de referencia*
