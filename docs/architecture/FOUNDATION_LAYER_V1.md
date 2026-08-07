# Foundation Layer v1.0 — Núcleo Arquitectónico QUIRA
## Declaración Formal del Núcleo Estable del Sistema

**Versión:** 1.0 (extensión ADR-018 2026-06-02)  
**Fecha:** 2026-06-01  
**Estado:** CONGELADO · Extensión activa via ADR-018  
**Autores:** Dylus Lab · Colega asesor  
**Relacionado:** TRES_CEREBROS_QUIRA · ADR-016 · ACK_REGISTRY · ADR-017 · ADR-018

---

## La tesis de Foundation Layer

Un sistema de conocimiento puede crecer indefinidamente en dos dimensiones:
- **Crecimiento documental:** más leyes, más chunks, más notas
- **Crecimiento estructural:** más ACKs, más DCOs, más circuitos

El crecimiento documental hace el sistema más completo.  
El crecimiento estructural hace el sistema más inteligente.

Foundation Layer v1.0 es la declaración de que QUIRA ya tiene los tres artefactos estructurales mínimos para crecer con coherencia en ambas dimensiones:

```
Sistema con 10,000 normas y 0 circuitos  = buscador sofisticado
Sistema con 500 normas y 50 circuitos    = motor de gobernanza
```

Los tres pilares de Foundation Layer permiten que QUIRA sea lo segundo.

---

## Los tres pilares del núcleo estable

### Pilar I — TRES_CEREBROS_QUIRA.md
**El modelo epistemológico**

Define qué pregunta responde cada capa del sistema:
```
Cerebro 1 (Supabase pgvector): "¿Qué dice la norma?"
Cerebro 2 (Neo4j + QTMP):      "¿Quién debe hacer qué?"
Cerebro 3 (Obsidian):          "¿Cómo lo entiende un humano?"
Ley Cero  (Excel Canónico):    "¿Cuál es la verdad operacional del GAD?"
```

Sin este pilar, las capas compiten en lugar de colaborar. Con él, cada capa tiene una pregunta propia y no puede usurpar la respuesta de otra.

**Principio canónico derivado:**
> "Cuando el corpus contradice el DCO, el DCO gana. El corpus devuelve similitud; el DCO devuelve autoridad."

### Pilar II — ADR-016_DCO_Dominio_Constitucional_Operacionalizable.md
**El formato de inteligencia de dominio**

Define cómo se convierte un dominio de gobernanza en conocimiento operable:
```
Identidad → Norma Fundante → Cadena Normativa (C1-C4) → Subdominios
→ Actores → Variables Operacionales → Circuitos → Corpus + Obsidian
```

Sin este pilar, los dominios son categorías. Con él, cada dominio es un sistema de razonamiento autónomo que puede diagnosticar, alertar y navegar.

**Principio canónico derivado:**
> "LOTAIP está en C4 (observación), no en C2 (obligación). La ventana de observación no es la norma fundante."

### Pilar III — ACK_REGISTRY.md
**El catálogo maestro de conocimiento jurídico**

Define el formato del átomo canónico de conocimiento jurídico (ACK) y establece su catálogo formal:
```
ack_id → tipo → norma{sigla/artículo/jerarquía} → dominios[] → circuitos[]
→ fundante → chunk_refs[] → revisado_por_experto
```

Sin este pilar, el corpus crece en tamaño documental pero los dominios y circuitos no tienen átomos formales que los anclen. Con él, cada afirmación jurídica de QUIRA puede trazarse hasta un artículo específico, verificable, con su SHA256 en el corpus.

**Principio canónico derivado:**
> "Un ACK es la unidad mínima de doctrina. El corpus dice qué existe; el ACK dice qué significa."

---

## La regla de extensión

Todo módulo nuevo de QUIRA debe ser rastreable a al menos uno de los tres pilares.

| Si el módulo nuevo es... | Traza a... |
|---|---|
| Un nuevo cerebro o capa de almacenamiento | Pilar I (TRES_CEREBROS) |
| Un nuevo dominio con DCO | Pilar II (ADR-016) |
| Un nuevo ACK o catálogo de conocimiento | Pilar III (ACK_REGISTRY) |
| Un ACK con alcance multi-dominio universal | Pilar III + ADR-018 (NRC) |
| Un circuito constitucional | Pilar II (nodos) + Pilar III (ACKs que anclan los nodos) |
| Una nueva interfaz de Obsidian | Pilar I (Cerebro 3 definición) |
| Un nuevo indicador en el Excel | Ley Cero (Excel Canónico) — no requiere ADR |

**Si un módulo propuesto no puede rastrear a ningún pilar**, tiene dos caminos:
1. Crear un nuevo ADR que extienda Foundation Layer (decisión arquitectónica formal)
2. Reconocer que está fuera del alcance de QUIRA Gov

Esta regla previene la proliferación de capas ad hoc que fragmentaron arquitecturas anteriores.

---

## Modelo de Madurez QUIRA — 6 Niveles

*(Superación del modelo de 5 niveles del colega asesor — añade L5: Predicción)*

```
L0 ── Excel Canónico ──────────────────── VERDAD OPERACIONAL
│     Fuente: Gold Master v5.5_TGI        "El Estado" · Ley Cero
│     Estado: ✅ ACTIVO
│
L1 ── Corpus + ACK Registry ───────────── MEMORIA JURÍDICA
│     Fuente: normativa_corpus (7,740 chunks) + ack_registry.json
│     Estado: ✅ CORPUS COMPLETO · ACK REGISTRY diseñado (pendiente carga inicial)
│
L2 ── DCO (ADR-016) ────────────────────── INTERPRETACIÓN
│     Fuente: Dom07 completo · Dom08-Dom12 pendientes
│     Estado: ✅ ADR-016 CONGELADO · Dom07 caso referencia
│
L3 ── Circuitos Constitucionales ─────── CAUSALIDAD
│     Fuente: ADR-017 · C01 listo · C02/C03 parciales
│     Estado: ✅ ADR-017 CONGELADO · C01 pendiente carga Neo4j
│
L4 ── Obsidian + Orient ────────────────── NAVEGACIÓN HUMANA
│     Fuente: Cerebro 3 · quira-orient skill
│     Estado: ✅ Dom07 nota Nivel 1 · 39 notas Nivel 2 · /quira-orient v1.0
│
L5 ── GeoTwin + SAT + Sentinel ─────────── PREDICCIÓN TERRITORIAL  ← NUEVO
      Fuente: GeoTwin espacial · SAT alertas · Sentinel IA
      Estado: 🔵 DISEÑADO (SAT activo) · GeoTwin pendiente · Sentinel en desarrollo
```

### Por qué L5 existe (y no era suficiente con 5 niveles)

Los niveles L0-L4 construyen un sistema que **diagnostica y razona** sobre el estado actual de gobernanza. Pero el horizonte final de QUIRA es la **anticipación**: detectar el riesgo antes de que se materialice en un incumplimiento formal.

L5 es la diferencia entre:
- "El municipio incumplió COOTAD 249 en 2025" → L0-L4 (post-hoc)
- "El municipio está en trayectoria de incumplir COOTAD 249 en Q3 2026" → L5 (anticipatorio)

La cadena de predicción:
```
Datos históricos longitudinales (L0+L1)
+ Degradación de nodos en circuitos (L3)
+ SAT activas actuales (L5)
→ Proyección: "C01 entrará en RUPTURA si Dom07 no mejora en 45 días"
→ Alerta proactiva → Acción preventiva → Cumplimiento
```

### Dependencias entre niveles

```
L5 requiere L3 (circuitos para identificar qué predecir)
L4 requiere L2 (DCOs para tener qué navegar)
L3 requiere L2 (DCOs como nodos) + L1 (ACKs que anclan los nodos)
L2 requiere L1 (corpus para validar + ACKs para anclar)
L1 requiere L0 (Excel como fuente de verdad operacional)

Por lo tanto: ningún nivel es saltable.
```

---

## Qué significa "congelado" en Foundation Layer

Foundation Layer v1.0 no es una restricción — es una garantía de estabilidad.

**Congelado NO significa:**
- Que los documentos no puedan evolucionar
- Que no se puedan agregar más DCOs, ACKs o circuitos
- Que la arquitectura está terminada

**Congelado SÍ significa:**
- Los tres pilares definen el vocabulario canónico del sistema
- Cualquier módulo nuevo hereda este vocabulario (no inventa uno nuevo)
- Las reglas canónicas derivadas (Corpus≠Doctrina, LOTAIP en C4, etc.) son inviolables
- Para cambiar un pilar se requiere un ADR de revisión, no una decisión informal

**Analogía:**
> La Constitución de un país no se congela para que no cambie — se congela para que los cambios sean deliberados, justificados y trazables. Foundation Layer v1.0 es la Constitución de QUIRA.

---

## Circuit Health Score como puente L3 → Centro de Mando (L4)

El Centro de Mando actualmente muestra 12 tarjetas de dominio. Con Foundation Layer v1.0 y ADR-017, puede mostrar también Circuit Health Scores:

```
┌─────────────────────────────────────────────────┐
│  CIRCUITOS CONSTITUCIONALES                      │
├─────────────┬──────────┬──────────────────────┤
│ C01         │  0.0     │ 🔴 Dom07 degradado    │
│ Transparencia→Part→Plan │  NODO ORIGEN FALLA   │
├─────────────┼──────────┼──────────────────────┤
│ C02         │  0.82    │ 🟢 Alineado           │
│ Presup→Contr→Transp     │                      │
├─────────────┼──────────┼──────────────────────┤
│ C03         │  0.71    │ 🟡 Riesgo en Dom04    │
│ Plan→Invers→Servicios   │                      │
└─────────────┴──────────┴──────────────────────┘

⚠️ ALERTA MULTI-CIRCUITO: Dom07 comparte C01 y C02
```

Esta vista no reemplaza los 12 dominios — los complementa con la dimensión causal.

---

## La Constitución QUIRA — 5 documentos fundamentales

*(Denominación formal para el conjunto de artefactos arquitectónicos no modificables)*

| # | Documento | Qué congela | Estado |
|---|---|---|---|
| 1 | `TRES_CEREBROS_QUIRA.md` | Modelo epistemológico · 3 preguntas · 3 cerebros · Ley Cero | ✅ CONGELADO |
| 2 | `ADR-016_DCO_*.md` | Formato DCO · 8 componentes · Dom07 caso referencia | ✅ CONGELADO v1.0 |
| 3 | `ACK_REGISTRY.md` | Schema ACK · catálogo maestro · Opción A implementada | ✅ OPERACIONAL v0.2 (11 ACKs · 4 NRCs · traversal ✅) |
| 4 | `ADR-017_Circuitos_*.md` | Arquitectura circuitos · C01 completo · CHS fórmula | ✅ CONGELADO v1.0 |
| 5 | `FOUNDATION_LAYER_V1.md` | Este documento · regla de extensión · 6 niveles madurez | ✅ CONGELADO v1.0 |
| 6 | `ADR-018_NRC_*.md` | Nodos Raíz Constitucionales · es_nrc field · criterio formal | ✅ CONGELADO v1.0 (extiende Pilar III) |

Estos cinco documentos son la Constitución QUIRA. Todo lo demás en el sistema — módulos Python, notas Obsidian, tablas Supabase, grafos Neo4j — implementa, extiende o interpreta esta Constitución. Pero no la gobierna.

---

## Estado del proyecto al 2026-06-01 (post-carga-inicial ACK Registry)

```
Foundation Layer v1.0: ✅ DECLARADA Y CONGELADA
  Pilar I  (3 Cerebros)  : ✅ COMPLETO
  Pilar II (ADR-016 DCO) : ✅ COMPLETO · Dom07 caso referencia
  Pilar III (ACK Registry): ✅ OPERACIONAL v0.2 — 11 ACKs · 4 NRCs · CLI · traversal ✅
  Extensión (ADR-018 NRC) : ✅ CONGELADO — NRC como categoría formal · CE_226 añadido

Madurez actual:
  L0 Excel Canónico   : ✅ ACTIVO (v5.5_TGI · Sprint Soberanía completado)
  L1 Corpus + ACK     : ✅ CORPUS 7,740 chunks · ACK Registry 10 ACKs · 8/10 chunk_refs
  L2 DCO              : ✅ Dom07 completo · Dom08-Dom12 pendientes
  L3 Circuitos        : ✅ ADR-017 congelado · C01 pendiente carga Neo4j
  L4 Obsidian+Orient  : ✅ Dom07 nota · 39 notas · /quira-orient v1.0
  L5 GeoTwin+SAT+Sentinel: 🔵 SAT activo · resto pendiente roadmap O.2+

Primer hito operacional: COMPLETADO
  LOTAIP_7 (sha256: 415a04b6) → Dom07 (DCO ADR-016) → C01/C02 (ADR-017)
  Estado: traversal completo · Neo4j pendiente · CHS calculable (datos pendientes)

Corpus gaps identificados (no bloquean la arquitectura):
  LOTAIP_47 (Art.47): no en corpus F0.x · verificar artículo real + re-ingestar
  LOPC_72 (Art.72):   LOPC no ingresada en corpus F0.2 · ingestar F0.2 ampliado

Próximos pasos — ejecución paralela posible:
  Secuencial obligatorio:
    1. C01 → Neo4j: cargar Cypher ADR-017 (prerequisito para CHS live)
  Paralelo viable:
    2a. Dom08 DCO: Triángulo P-02 Dom07+Dom08+Dom09 · norma fundante CE_95
    2b. Dom07 Layer 2: p07_transparencia.py con corpus F0.2 + ACK Registry activo
  Posterior:
    3. Dom09 DCO: Rendición de Cuentas (cierra Triángulo P-02)
    4. C02 spec completa: requiere QLEP Dom03 (LOSNCP ACKs)
    5. Revisión jurista: CE_61 · CE_95 · CE_100 · LOPC_72 · LOTAIP_34 · LOTAIP_47
  Corpus expansión:
    6. LOPC ingestión F0.2 ampliado (LOPC_72 + otros ACKs Dom08)
    7. LOTAIP versión completa (verificar Art.47 vs Art.20-21 en texto impreso)
```

---

## La Fase Constituyente — Declaración de Cierre (2026-06-01)

### La cadena normativa interna

Foundation Layer v1.0 establece una jerarquía de dependencias entre los cinco documentos constitucionales. Ninguno puede ser ignorado sin romper los que le siguen:

```
Excel Canónico           ← Ley Cero — verdad operacional del GAD
        ↓ define qué es la verdad
TRES_CEREBROS_QUIRA      ← reglas de qué pregunta responde cada capa
        ↓ define qué son los átomos de conocimiento
ACK_REGISTRY             ← catálogo formal de los átomos jurídicos
        ↓ los átomos anclan a los dominios
ADR-016 (DCO)            ← formato de inteligencia de dominio
        ↓ los dominios son nodos de circuitos
ADR-017 (Circuitos)      ← cadenas causales multi-dominio
```

**Nota sobre dependencias mutuas (mejora sobre el modelo lineal):**

La cadena anterior es correcta en dirección general, pero ACK_REGISTRY y ADR-016 son mutuamente dependientes:
- ACK_REGISTRY define los átomos que ADR-016 referencia como anclas (→)
- ADR-017 produce los circuit IDs que ACK_REGISTRY registra en su campo `circuitos[]` (←)

Esto no es una inconsistencia — es el patrón correcto para un grafo de conocimiento: los artefactos se co-determinan. La cadena establece la dirección de autoridad, no la dirección de creación.

### El insight estructural de ADR-017

El cambio más profundo introducido por Foundation Layer no es técnico. Es epistémico:

**Antes de ADR-017:**
```
Portal LOTAIP caído → Problema de Dom07
```

**Después de ADR-017:**
```
Portal LOTAIP caído → Dom07 degradado → Riesgo C01 → Riesgo C02
                                      → "El municipio no puede planificar
                                         porque primero no participa
                                         y primero no informa"
```

El dominio ya no es la unidad de diagnóstico.  
El circuito es la unidad de diagnóstico.  
El dominio es un nodo dentro del diagnóstico.

Esto es lo que hace que QUIRA pase de ser un dashboard a ser un motor de gobernanza.

### Scorecard de madurez QUIRA (2026-06-01 · v2 post-carga-inicial)

*(Evaluación conjunta Dylus Lab + colega asesor — actualizado tras ACK Registry v0.2)*

| Capa | Score | Evidencia |
|---|---|---|
| Corpus normativo | 9/10 | 7,740 chunks · 41 docs · 0 errores · F0.1-F0.8 ✅ |
| Doctrina | 9/10 | Foundation Layer v1.0 · 5 artefactos congelados · Constitución QUIRA |
| Arquitectura | 10/10 | ADR-013/016/017 congelados · 3 Cerebros · Ley Cero definida |
| Circuitos | 6/10 | ADR-017 diseño completo · C01 listo · C02/C03 parciales · Neo4j pendiente |
| Neo4j operativo | 4/10 | Fallback activo (Gold Master) · grafo real no cargado · Cypher C01 listo |
| ACK Knowledge Graph | 6/10 | 10 ACKs cargados · register_ack.py CLI completo · 8/10 chunk_refs · traversal LOTAIP_7→C01 ✅ |
| Diagnóstico sistémico | 3/10 | Traversal operacional · sin CHS calculado live · sin Neo4j real |
| Predicción territorial | 1/10 | SAT activo (3 alertas) · GeoTwin pendiente · Sentinel en desarrollo |
| **Replicabilidad nacional** | **7/10** | Principio Alcance Nacional declarado · canton_id guardrail activo · Kernel+Instancias documentado · 222 municipios destino |

**Lectura del scorecard (v2):**

El salto más significativo de v1→v2 es el ACK Knowledge Graph (1→6): el registry pasó de ser una propuesta a ser un catálogo operacional con CLI, 10 ACKs, 8 SHA256 verificados y traversal completo demostrado.

La nueva dimensión "Replicabilidad nacional" (7/10) refleja que la decisión más estratégica del sprint no fue técnica sino ontológica: **el campo `canton_id` es arquitectónicamente imposible en el ACK Registry**. La normativa es nacional; los datos operacionales son cantonales. Esta separación — Kernel Nacional + Instancias — es lo que hace que QUIRA sea escalable a 222 municipios sin reimplementación.

Las brechas que restan: Neo4j sin datos (4/10), diagnóstico sin CHS live (3/10), predicción incipiente (1/10). Estas son exactamente el roadmap operacional de los próximos sprints.

### La transición: Definir → Demostrar

Hasta Foundation Layer v1.0, QUIRA estaba respondiendo la pregunta:
> **"¿Qué es QUIRA?"**

A partir de Foundation Layer v1.0, QUIRA responde la pregunta:
> **"¿Funciona QUIRA?"**

Esa transición tiene una implicación práctica: el próximo sprint no produce más documentos de arquitectura. Produce código ejecutable que atraviesa la cadena:

```
CE_18 (ACK) → Dom07 (DCO) → C01 (Circuito) → Diagnóstico sistémico
```

Cuando ese recorrido funcione en Neo4j con datos reales, Foundation Layer v1.0 habrá sido demostrado, no solo declarado.

---

*Foundation Layer v1.0 · QUIRA Gov · Dylus Lab © 2026*  
*"La Constitución no limita el crecimiento — garantiza que el crecimiento sea coherente."*  
*Fase constituyente: cerrada 2026-06-01. Fase operacional: iniciada.*
