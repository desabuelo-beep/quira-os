# ADR-011 — Tres productos · Motor IA · Arquitectura integrada QUIRA

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones · Director de Arquitectura  

---

## Contexto

Alpha 1.0 demostró que el núcleo causal existe y funciona. El siguiente paso no es
construir más infraestructura — es abrir ese núcleo a tres audiencias distintas
con tres interfaces distintas, y elevar la capa de inteligencia artificial al
máximo nivel técnicamente alcanzable con la infraestructura actual.

Se agregan dos vectores estratégicos:
1. **Universidades de Ecuador (UEB y red)** requieren al menos 5 municipios monitoreados.
2. **Elecciones 2026** abren una ventana única de validación social con ciudadanía,
   academia y candidatos como testers simultáneos.

---

## Decisión

### Producto 1 — QUIRA Gov (Institucional)

**Audiencia**: GAD, alcaldía, dirección técnica, académicos.  
**Núcleo**: Neo4j + Gold Master + Streamlit PMV.  
**AI**: Motor IA Claude (claude-3-5-sonnet) para consultas en lenguaje natural.  
**Estado**: Operativo (Alpha 1.0). Beta = Panel Estratégico + roles.

### Producto 2 — QUIRA Ciudadana

**Audiencia**: Ciudadanos, periodistas, candidatos, academia.  
**Núcleo**: Grafo compartido con Gov. Interfaz pública simplificada.  
**Capacidades**:
- Ingesta documental: subida directa (PDOT, POA, PAC, presupuestos, rendición de cuentas)
  o scraping automático desde portales LOTAIP / sitios web institucionales.
- Si el documento no existe: SAIP automático (LOTAIP Art. 34).
- Día 16: email con documento de proceso judicial y guía de acción.
- NLP "versus": contrasta discurso público (rendición de cuentas, actos políticos)
  con hallazgos del grafo. Expone la verdad con evidencia.
- Formación para la acción: qué puede hacer el ciudadano, paso a paso.

**Estado**: Diseño. Sprint dedicado posterior a Beta-1.

### Producto 3 — QUIRA Operaciones

**Audiencia**: Equipo QUIRA Operaciones · Dylus Lab.  
**Núcleo**: Centro de Mando interno. Observabilidad longitudinal. Alertas automáticas.  
**Estado**: Parcial (Centro de Mando en construcción).

---

## Arquitectura de grafo — Compartida, interfaces separadas

```
Neo4j (grafo único)
    ↓ interfaz Gov         → Panel Estratégico + consultas técnicas
    ↓ interfaz Ciudadana   → preguntas simplificadas + SAIP + versus NLP
    ↓ interfaz Operaciones → alertas + observabilidad + snapshot longitudinal
```

El grafo es la fuente de verdad única. Las interfaces son vistas con distinto
vocabulario y nivel de acceso. No se duplican datos. No se duplican bases.

---

## Motor IA — Claude como capa de razonamiento

### Componente 1 — QUIRA Intelligence Engine

- Acepta preguntas en lenguaje natural (español ecuatoriano)
- Genera Cypher usando Claude + contexto del schema
- Ejecuta contra Neo4j
- Genera respuesta en lenguaje natural con fuentes y semáforos
- Modelo: claude-3-5-sonnet-20241022 (análisis) / claude-3-haiku-20240307 (velocidad)

### Componente 2 — QUIRA Versus NLP

- Input: texto de discurso (rendición de cuentas, acto político, comunicado)
- Proceso: Claude extrae afirmaciones sobre indicadores de gestión
- Proceso: mapea afirmaciones a nodos del grafo
- Proceso: consulta el grafo para obtener datos reales
- Output: reporte "versus" — lo que se dijo vs. lo que los datos muestran

### Componente 3 — QUIRA SAIP Engine

- Genera automáticamente solicitudes LOTAIP (Art. 34)
- Registra fecha de envío → calcula día 16
- Día 16: genera email con documento de proceso judicial (acción constitucional)
- Tracking de estado: pendiente → recibido → cumplido → escalado_judicial

---

## Expansión territorial — 5 municipios (UEB)

- El QTMP schema v1.1 es multi-cantón por diseño.
- Ruta de expansión: 1 circuito universal (GAP_10PCT, COOTAD_249 aplica a todos)
- Datos: UEB aporta cédulas SIGEF de sus municipios de estudio.
- Roadmap: Montecristi completo → luego 4 municipios provincia Manabí.

---

## Congelamiento durante construcción

Los siguientes componentes permanecen CONGELADOS durante la construcción de
QUIRA Ciudadana y el motor IA:

```
✗ Schema QTMP (solo extender, no modificar)
✗ ADRs 001-010 (este es el 011)
✗ Cadena bautismal (es el contrato de referencia)
✗ Corpus normativo ACK (solo agregar, no modificar)
```

---

## Consecuencias

- Cualquier nuevo producto requiere este ADR como base.
- El grafo compartido significa que una mejora en los datos beneficia a los 3 productos.
- QUIRA Ciudadana NO es una versión simplificada de Gov — es un producto distinto
  con lógica de empoderamiento ciudadano, no de gestión institucional.
- MILESTONE_002 = primer usuario externo que obtiene una respuesta correcta sin
  intervención del equipo. Target: durante campaña electoral 2026.

---

## Ver también

ADR-010, ADR-005, ADR-009, SPEC_CIUDADANA_001.md, ALPHA_1_0_FREEZE.md

---

*ADR-011 — Registrado 2026-05-31*  
*DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones*
