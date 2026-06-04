# QUIRA — Arquitectura de Producto
## Versión 1.0

**Estado**: CONGELADO  
**Fecha**: 2026-05-31  
**Custodio**: QUIRA Operaciones · Dylus Lab  
**Deriva de**: QUIRA_EPISTEMIC_FRAMEWORK_v1.0 (Secciones VII y VIII) + ADR-011  
**Audiencia**: Dylus Lab · QUIRA Operaciones · Equipos de construcción

> El grafo es uno. Los productos son cinco. Los verbos son distintos.
> La fuente de verdad es la misma para todos.

**Fuente canónica de productos**: `QUIRA_ECOSYSTEM_2026_2030.md` — ese documento define los 5 productos completos.
Este documento especifica la arquitectura técnica compartida. No reemplaza al Ecosystem doc.

**Los cinco productos del ecosistema QUIRA:**
```
1. QUIRA Institucional  → verbo: GESTIONAR   → GADs, alcaldía, direcciones técnicas
2. QUIRA Ciudadana      → verbo: EXIGIR      → ciudadanos, periodistas, candidatos
3. QUIRA Operaciones    → verbo: OBSERVAR     → Dylus Lab, QUIRA Operaciones (interno)
4. QUIRA Impact         → verbo: TRAZAR       → CAF, BID, BM, PNUD, UE, GIZ, JICA
5. QUIRA Economy        → verbo: EVALUAR      → empresas, bancos, fondos ESG (futuro)
```

---

## I. PRINCIPIO ARQUITECTÓNICO CENTRAL

```
Neo4j (grafo causal único — fuente de verdad territorial)
    │
    ├── interfaz QUIRA Gov          → GADs, alcaldía, academia, dirección técnica
    ├── interfaz QUIRA Ciudadana    → ciudadanos, periodistas, candidatos
    └── interfaz QUIRA Operaciones  → Dylus Lab, QUIRA Operaciones
```

**Regla cardinal**: Los datos NO se duplican. Las bases NO se multiplican.
Una mejora en el grafo beneficia a los tres productos simultáneamente.
Una brecha detectada en cualquier interfaz retroalimenta el grafo central.

---

## II. STACK TÉCNICO CANÓNICO

| Capa | Tecnología | Función |
|---|---|---|
| Grafo causal | Neo4j (quira-alpha v5.26.8) | Cerebro — razonamiento territorial |
| Vector / memoria rápida | Supabase pgvector | Embeddings + snapshots longitudinales |
| Espacial | PostGIS (en desarrollo) | GeoTwin — mapas territoriales |
| Interfaz Gov | Streamlit | Panel Estratégico · PMV operativo |
| Interfaz Ciudadana | Por definir (Sprint Ciudadana) | UX pública simplificada |
| Motor IA | Claude (claude-3-5-sonnet + claude-3-haiku) | Consultas NL → Cypher → respuesta |
| SAIP Engine | Claude + tracking BD | Generación LOTAIP + escalamiento judicial |
| Versus NLP | Claude + Whisper | Discurso oficial vs. datos del grafo |
| Observabilidad | Centro de Mando (en construcción) | Alertas + snapshot longitudinal |
| Dominio | quiraintelligence.com | Cara pública del sistema |
| Repositorio | quira-os (GitHub) | Código y scripts |

**Decisiones arquitectónicas congeladas** (no reabrir sin ADR):
- Grafo = Neo4j (no vector store, no relacional puro)
- Vector = Supabase pgvector (no Pinecone, no Weaviate)
- UI = Streamlit (no React, no Next.js para el Gov MVP)
- Stack multi-cantón por diseño desde QTMP v1.1

---

## III. PRODUCTO 1 — QUIRA GOV (Institucional)

**Verbo**: GESTIONAR  
**Audiencia**: GAD, alcaldía, dirección técnica, académicos  
**Estado**: Alpha 1.0 operativo → Beta en construcción

### Núcleo

El grafo Neo4j responde preguntas causales sobre el territorio en lenguaje natural.
El Motor IA (Claude) traduce pregunta → Cypher → respuesta verificable.

### Componentes confirmados

| Componente | Estado | Descripción |
|---|---|---|
| Panel Estratégico | Beta pendiente | 12 dominios causalmente cerrados con semáforos |
| Sistema de roles | Pendiente | Ejecutivo (alcalde), Directivo (técnico), Operaciones |
| Motor IA (Haiku) | Pendiente → Sprint 3 | Reemplaza Groq actual |
| GeoTwin | Beta | Mapa territorial con PDOT atómizado |
| Circuitos QTMP | En desarrollo | 12 circuitos (1 por dominio — 11 restantes) |

### Beta roadmap

```
Beta-1: Panel Estratégico + roles + Claude Haiku
Beta-2: Dom02 (Agua Potable) causalmente cerrado — segunda cadena
Beta-3: Dom01 + Dom04 — norma + territorio
...hasta Dom12 completo
```

### Estado de dominios

| Dominio | Datos | QTMP | Causal |
|---|---|---|---|
| Dom12 — Protección Social (GAP_10PCT) | Confirmado | Cargado | ✅ CERRADO |
| Dom_AGUA — Agua Potable | Confirmado | Cargado | ✅ Cerrado (circuito) |
| Dom_EQUIDAD — Equidad Territorial | Confirmado (parcial) | Cargado | Parcial |
| Dom01 a Dom11 | PDOT + Gold Master | Pendiente QTMP | ❌ Pendiente |

> **Regla QTMP**: Cada dominio necesita su propio circuito QTMP con la norma raíz (ACK).
> No es agregar nodos — es definir la cadena normativa completa de ese dominio.

---

## IV. PRODUCTO 2 — QUIRA CIUDADANA

**Verbo**: EXIGIR  
**Audiencia**: Ciudadanos, periodistas, candidatos, academia  
**Estado**: Diseño. Sprint dedicado posterior a Beta-1 de Gov.

> QUIRA Ciudadana NO es una versión simplificada de Gov.
> Es un producto distinto con lógica de empoderamiento ciudadano,
> no de gestión institucional. La audiencia decide qué hace
> con la información — QUIRA solo la provee.

### Módulos del Sprint Ciudadana

#### Módulo 1 — Ingesta Documental
- Subida directa: PDOT, POA, PAC, presupuestos, rendiciones de cuentas
- Scraping automático desde portales LOTAIP / sitios web institucionales
- Extracción de texto + clasificación automática con Claude

#### Módulo 2 — SAIP Engine (LOTAIP Art. 34)
- Si el documento requerido no existe en LOTAIP → genera SAIP automático
- Registro de fecha de envío → calcula día 16
- Día 16: Claude genera email con documento de proceso judicial + guía de acción
- Tracking de estado: `pendiente` → `recibido` → `cumplido` → `escalado_judicial`
- IOC (H41): Índice de Opacidad Cantonal — actualizado dinámicamente con cada SAIP

```
IOC_actual: 17.71% (Montecristi 2025 — "Opacidad Moderada")
Escala: <10% Verde · 10-20% Amarillo · 20-40% Rojo · >40% Crítico
Meta 2027: IOC < 10%
Fuente: H41 del Gold Master (fuente canónica — nunca calcular desde defaults)
```

#### Módulo 3 — Versus NLP
- Input: texto o URL de discurso (rendición de cuentas, acto político, comunicado)
- Claude extrae afirmaciones sobre indicadores de gestión
- Claude mapea afirmaciones a nodos del grafo
- Claude consulta el grafo → obtiene dato real
- Output: reporte "versus" — lo que se dijo vs. lo que los datos muestran
- Corpus inicial: videos de rendición de cuentas del alcalde en redes sociales

```
Ejemplo versus:
  Discurso: "Montecristi invierte más del 10% en grupos prioritarios"
  Dato grafo: "COOTAD_249 cumplido (20.84%) PERO Ti_Patronato=50% → Dom12 ROJO año 3"
  Versus: ✓ Cumple el porcentaje formal · ✗ No llega al territorio
```

#### Módulo 4 — Formación para la acción
- ¿Qué puede hacer el ciudadano ante este dato?
- Pasos específicos: SAIP → audiencia pública → acción de protección → denuncia CGE
- Marco normativo citado (CE Art. 18, LOTAIP Art. 34, COOTAD Art. 60-61)
- Lenguaje ciudadano — sin jerga técnica ni nomenclatura interna

### Diseño UX — Principios

- El ciudadano es el centro, no el sistema
- Una pregunta → una respuesta → una acción posible
- Sin acrónimos internos en la interfaz pública
- Sin mencionar Gold Master, QTMP, IDs de nodos, schema
- Accesible en baja conectividad (mobile-first)
- En español ecuatoriano, no en lenguaje técnico-legal

### Ventana de validación

Elecciones 2026 = primer escenario de validación social con:
- Ciudadanos verificando promesas de campaña
- Periodistas contrastando discurso con datos
- Candidatos encontrando brechas para sus propuestas
- Academia observando el comportamiento de uso

---

## V. PRODUCTO 3 — QUIRA OPERACIONES

**Verbo**: OBSERVAR  
**Audiencia**: Dylus Lab · QUIRA Operaciones  
**Estado**: Parcial (Centro de Mando en construcción)

### Función

Observabilidad interna del sistema QUIRA.
No observa el territorio — observa cómo QUIRA observa el territorio.

### Componentes

| Componente | Estado |
|---|---|
| Centro de Mando (Streamlit) | En construcción |
| Snapshot longitudinal | Operativo (Supabase — snapshot #1: 2026-05-26) |
| Alertas automáticas sobre anomalías del grafo | Pendiente |
| Dashboard de salud del grafo (nodos, circuitos, estado) | Pendiente |

### Datos de snapshot

```
Snapshot #1 — 2026-05-26:
  ICPI = 17.45%
  TGI = 66.79%
  Supabase: OK
```

---

## VI. MOTOR IA — Componentes compartidos entre productos

El Motor IA es una capa transversal que sirve a los tres productos.
No es un chatbot. No es RAG clásico. Es razonamiento sobre el grafo.

### Componente 1 — QUIRA Intelligence Engine (Gov + Ciudadana)

```
Input:   Pregunta en lenguaje natural (español ecuatoriano)
Proceso: Claude + contexto del schema → genera Cypher
         Ejecuta Cypher contra Neo4j
Output:  Respuesta en lenguaje natural con fuentes y semáforos
Modelos: claude-3-5-sonnet-20241022 (análisis profundo)
         claude-3-haiku-20240307 (velocidad, consultas simples)
```

### Componente 2 — QUIRA Versus NLP (Ciudadana)

```
Input:   Texto de discurso (rendición de cuentas, acto político, comunicado)
Proceso: Claude extrae afirmaciones sobre indicadores de gestión
         Claude mapea afirmaciones a nodos del grafo
         Claude consulta el grafo para obtener datos reales
Output:  Reporte "versus" — lo que se dijo vs. lo que los datos muestran
```

### Componente 3 — QUIRA SAIP Engine (Ciudadana)

```
Input:   Tipo de información + institución + fecha de solicitud
Proceso: Claude genera solicitud LOTAIP (Art. 34) personalizada
         Registra fecha envío → calcula día 16
Output:  Día 0: solicitud formal generada
         Día 16: email con documento de proceso judicial + guía
Tracking: pendiente → recibido → cumplido → escalado_judicial
```

---

## VII. EXPANSIÓN TERRITORIAL — 5 Municipios (UEB)

El QTMP schema v1.1 es multi-cantón por diseño.
Un circuito como GAP_10PCT aplica a cualquier municipio porque COOTAD_249 aplica a todos.

**Ruta de expansión**:

```
1. Montecristi completo (12 dominios causalmente cerrados)
2. UEB aporta datos SIGEF de 4 municipios de la provincia Manabí
3. Se instancian los mismos circuitos QTMP con el ID de cantón correspondiente
4. El grafo Neo4j crece — mismo schema, nuevos IDs
5. Resultado: comparación longitudinal inter-cantonal (longitudinalidad territorial)
```

**Bottleneck**: La expansión no depende del software — depende de los datos.
Cada municipio necesita sus propias cédulas SIGEF, POA, PDOT.
UEB es el puente de obtención de esos datos.

---

## VIII. MODELO DE NEGOCIOS — Capa de sostenibilidad

### Independencia institucional como principio

Dylus Lab opera sin contratos con los municipios que analiza.
La razón: si el cliente es el alcalde, el sistema no puede decir
que el alcalde ejecutó el 50% de su presupuesto de inversión.
La independencia epistemológica requiere independencia financiera.

### Fuentes de ingreso compatibles con independencia

| Fuente | Modelo | Condición |
|---|---|---|
| B2G — SaaS a otros GADs que quieren usar QUIRA | Licencia de uso — no de metodología | GAD que paga no es el GAD analizado |
| DaaS — Datos procesados para academia y think tanks | Venta de análisis territorial | No expone metodología interna |
| Cooperación internacional | BID Lab, GIZ, CAF, PNUD, USAID | Alineado con ODS 16 — transparencia e instituciones |
| Consultoría Gov Tech | QUIRA como referente para otros municipios | Basado en reputación metodológica |

**La metodología (Gold Master, QTMP, ICPI) no se vende. Es el activo que produce el valor.**
Lo que se vende es el resultado: la cadena causal, el panel, la explicación.
El método permanece en Dylus Lab.

---

## IX. CONGELAMIENTO — Qué no cambia durante la construcción

```
✗ Schema QTMP v1.1 (solo extender, no modificar)
✗ ADRs 001-011 (base arquitectónica)
✗ Cadena bautismal (contrato de referencia Alpha 1.0)
✗ Corpus normativo ACK (solo agregar, no modificar)
✗ Ontología QNKC-002 (12 dominios, 10 capas causales)
✗ Stack técnico canónico (Neo4j + Supabase + Streamlit + Claude)
```

---

## Ver también

ADR-011, QUIRA_EPISTEMIC_FRAMEWORK_v1.0, QUIRA_THEORY_OF_CHANGE_v1.0,
QUIRA_CAUSAL_MODEL_v1.0, QUIRA_STATE v1.3, ALPHA_1_0_FREEZE

---

*QUIRA_PRODUCT_ARCHITECTURE v1.0 — Registrado 2026-05-31*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
