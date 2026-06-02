# DCO Dom09 — Rendición de Cuentas & Control Social

**ADR referencia**: ADR-016 (template DCO canónico)  
**dominio_id**: Dom09  
**nombre_canonico**: "Rendición de Cuentas & Control Social"  
**Estado**: ACTIVO  
**Fecha**: 2026-06-02  
**Proyecto**: QUIRA Gov · Dylus Lab  

---

## Componente 1 — Identidad del Dominio

```yaml
dominio_id:       Dom09
nombre_canonico:  "Rendición de Cuentas & Control Social"
chs_rol_c01:      DESTINO
chs_peso_c01:     0.7
dco_activo:       true
```

### Por qué existe este dominio

Dom09 es la **respuesta institucional obligatoria al mandato democrático** que Dom08 activa.

La ciudadanía participa (Dom08) porque tiene el derecho constitucional de incidir en la gestión pública. Para que esa participación tenga sentido real, el mandatario (el Alcalde, la institución) debe responder ante el mandante (la ciudadanía) sobre lo que hizo con el mandato recibido.

Sin rendición de cuentas, Dom08 queda como participación vacía — la ciudadanía decide pero nunca sabe si sus decisiones se cumplieron.

Sin participación, Dom09 queda como rendición vacía — hay un informe, pero nadie lo exigió, nadie lo esperaba, nadie lo usa para nada.

Son la misma moneda.

### El ciclo operacional concreto en los GADs

```
Dom08-B (Presupuesto Participativo):
  Ciudadanía decide "queremos agua en el barrio X"
  → PP planifica el gasto
  → GAD ejecuta (o no ejecuta)

Dom09 (Rendición de Cuentas):
  Ciudadanía pregunta "¿llegó el agua al barrio X?"
  → RC evalúa si se cumplió lo participado
  → Ciudadanía califica la gestión
  → Retroalimenta el siguiente PP
```

Este ciclo PP→RC **no es metafórico** — es la arquitectura operacional que los GADs municipales implementan (o deben implementar) conforme LOPC + COOTAD + RES-CPCCS-RC-2026.

Las actas del PP son **evidencia L0 de Dom08**. El informe de RC es **evidencia L0 de Dom09**. La comparación PP-planificado vs RC-ejecutado es la **métrica que cierra el ciclo**.

---

## Componente 2 — Norma Fundante

**Norma fundante primaria**: CE Art. 95 — Participación ciudadana protagónica

Esta elección no es casual ni arbitraria. Es la misma norma fundante que Dom08.

CE_95 dice en un solo artículo: *"participarán de manera protagónica en la toma de decisiones, planificación y gestión de los asuntos públicos, **y en el control popular de las instituciones del Estado y la sociedad, y de sus representantes**"*

El "control popular" no es un derecho separado — es la segunda mitad del mismo derecho. Dom08 materializa la primera mitad (participar y decidir). Dom09 materializa la segunda (controlar y evaluar).

Por esto Dom08 y Dom09 comparten raíz constitucional. La LOPC los regula en el mismo cuerpo legal. El CPCCS los administra como parte de la misma arquitectura institucional.

**Norma fundante secundaria**: CE Art. 100 — Instancias de participación en todos los niveles de gobierno  
→ "elaborarán planes y políticas, mejorarán la calidad de la inversión pública, **y elaborarán presupuestos participativos**"  
→ La rendición de cuentas es implícita: quien elabora el presupuesto participativamente debe rendir cuentas de él.

---

## Componente 3 — Subdominios

### Dom09-A: Rendición de Cuentas Anual Obligatoria

**Obligación fundante**: LOPC Art. 90 + Art. 95  
**Actor obligado**: Alcalde (autoridad electa), Directivos, Representantes de empresas públicas  
**Periodicidad**: UNA VEZ POR AÑO + AL FINAL DE LA GESTIÓN  
**Metodología vigente**: RES-CPCCS-RC-2026  

El Alcalde debe rendir cuentas ante la ciudadanía sobre:
- Plan de trabajo / plan estratégico de gobierno
- POA (plan operativo anual) y su ejecución
- Presupuesto general y presupuesto participativo
- Propuestas y acciones de gestión

El proceso es habilitado por el CPCCS, que proporciona la metodología, el espacio digital de reporte, y certifica la calificación ciudadana.

**Indicador canónico**: RC realizada / RC esperada (0/1 binario por año)  
**Indicador de calidad**: Calificación ciudadana obtenida (escala CPCCS)

### Dom09-B: Evaluación del Ciclo Presupuesto Participativo → Ejecución

**Obligación fundante**: LOPC Art. 71 (en lectura RC) + LOPC Art. 91  
**Actor obligado**: Alcalde, Director Financiero  
**Pregunta central**: ¿Se ejecutó lo que la ciudadanía decidió en el PP?

Este subdominio cierra el ciclo con Dom08-B (Presupuesto Participativo). La RC no solo evalúa "cuánto se gastó" — evalúa "si lo que se gastó corresponde a lo que la ciudadanía priorizó en el PP del año anterior."

Sin Dom09-B, el presupuesto participativo es una consulta decorativa. Con Dom09-B, es un mandato con verificación.

**Evidencia específica**:
- Comparativo PP planificado vs. ejecutado (obra x obra, proyecto x proyecto)
- Informe de ejecución presupuestaria (POA-PAC)
- Actas de asamblea de evaluación ciudadana

---

## Componente 4 — Cadena Normativa

### C1 — Nivel Constitucional (fundamento del dominio)

| ACK | Tipo | Rol en Dom09 |
|---|---|---|
| CE_95 | principio/derecho | Norma raíz — "control popular de las instituciones" |
| CE_100 | obligacion | Instancias de participación incluyen evaluación de la gestión |
| CE_226 | principio | Marco general de legalidad — RC como obligación del servidor |

**Nota**: CE_1 (soberanía popular) es el apex ontológico. La RC es la forma en que los mandatarios responden ante el mandante constitucional (el pueblo). LOPC Art. 91 lo dice explícitamente: *"garantizar a los mandantes el acceso a la información"* — LA CIUDADANÍA ES EL MANDANTE.

### C2 — Nivel Orgánico (obligaciones operativas)

| ACK | Tipo | Contenido |
|---|---|---|
| LOPC_89 | definicion | "Proceso sistemático, deliberado, interactivo y universal" |
| LOPC_90 | obligacion | Sujetos obligados: Alcalde + funcionarios + empresas públicas |
| LOPC_91 | obligacion | Objetivos: acceso mandantes, control popular, prevenir corrupción |
| LOPC_93 | procedimiento | Nivel programático y operativo — funcionarios y directivos |
| LOPC_95 | plazo | Periodicidad anual + al final de gestión |

### C4 — Nivel Metodológico (procedimiento vigente)

| ACK | Tipo | Contenido |
|---|---|---|
| RES-CPCCS-RC-2026 | procedimiento | Reglamento vigente CPCCS 2026 — metodología, plataforma, calificación |

**Nota arquitectónica**: La posición de RES-CPCCS-RC-2026 en C4 (no C2) replica el patrón de LOTAIP en Dom07. La norma orgánica (LOPC) crea la obligación. El reglamento operacional (RES-CPCCS) define el procedimiento específico. C4 es la "ventana de observación" del dominio.

---

## Componente 5 — Evidencia Canónica

### Evidencia L0 (Excel Canónico / registros locales GAD)

| Tipo | Fuente | Verifica |
|---|---|---|
| Informe de RC publicado | Portal LOTAIP + sistema CPCCS | Dom09-A: RC realizada |
| Calificación ciudadana | Sistema CPCCS | Dom09-A: calidad RC |
| Actas asamblea de evaluación | Secretaría Municipal | Dom09-A: proceso deliberativo |
| Comparativo PP vs. ejecución | POA-PAC + actas PP | Dom09-B: cumplimiento del mandato participativo |
| Informe ejecución presupuestaria | SIGEF / sistema financiero GAD | Dom09-B: cuánto se ejecutó de lo participado |

### Evidencia L4 (compliance normativo)

- Informe CPCCS de cumplimiento de RC (¿el GAD cumplió el proceso metodológico?)
- Pronunciamientos CGE si RC revela irregularidades

---

## Componente 6 — Variables e Indicadores

### Variables principales

| Variable | Tipo | Rango | Fuente |
|---|---|---|---|
| RC_REALIZADA | binaria | 0/1 | Sistema CPCCS |
| RC_CALIFICACION | continua | 0-100 | Calificación ciudadana CPCCS |
| PP_VS_EJECUCION_PCT | continua | 0-100% | POA-PAC vs actas PP |
| RC_DIAS_PLAZO | entera | días de demora | Fecha convocatoria vs fecha legal |

### Indicador de cierre de ciclo

```
CICLO_DEMOCRATICO_SCORE = 
    (Dom08_PP_PARTICIPACION * 0.5) + (Dom09_RC_CALIFICACION * 0.5)
```

Si este score es alto, el ciclo PP→RC funciona. Si hay asimetría (PP alto, RC bajo o viceversa), el ciclo está roto.

---

## Componente 7 — Circuitos

### C01 — Transparencia → Participación → Planificación

```
Dom07 (ORIGEN) → Dom08 (INTERMEDIARIO) → Dom04 (DESTINO)
                                   ↓
                              Dom09 (DESTINO alternativo)
```

Dom09 es **DESTINO** en C01 porque la cadena de transparencia activa la participación, que genera la exigencia de rendición de cuentas. Sin Dom07 funcionando, la ciudadanía no tiene información para exigir una RC de calidad.

**Peso CHS**: 0.7 (mismo que Dom04 en C01 — ambos son "destinos" del circuito)

### C04 — Ciclo Democrático PP → RC (PENDIENTE ADR-017 extensión)

```
Dom08 ──GENERA──────► Dom09
Dom09 ──RETROALIMENTA──► Dom08
```

Este circuito formaliza el ciclo PP-RC como estructura constitucional computable. C04 está pendiente de formalización en ADR-017 extensión, pero las relaciones ya existen en el grafo.

---

## Componente 8 — Relación con Dom08 (par constitucional)

Dom09 y Dom08 forman un **par constitucional** — dos nodos con acoplamiento constitucional fuerte que operan como unidad funcional:

| Aspecto | Dom08 | Dom09 |
|---|---|---|
| Norma raíz | CE_95 | CE_95 (misma) |
| Ley operativa | LOPC (participación) | LOPC (rendición) |
| Órgano habilitador | Alcalde convoca | CPCCS habilita |
| Mecanismo PP | PP planifica gasto | — |
| Mecanismo RC | — | RC evalúa ejecución |
| Evidencia L0 | Actas PP, convocatorias | Informe RC, calificación |
| Dirección causal | Dom08 GENERA Dom09 | Dom09 RETROALIMENTA Dom08 |

**El acoplamiento empírico se verificará con betweenness centrality** cuando se ejecute la prueba ADR-019. Si Dom08+Dom09 forman una díada con alta centralidad conjunta → Escenario C ADR-019.

---

## Queries Canónicas

```cypher
// Q_Dom09_1: ¿CE_95 funda Dom09 como funda Dom08?
MATCH (ce95:ACK {ack_id:'CE_95'})-[:FUNDA]->(d09:Dominio {id:'Dom09'})
RETURN ce95.ack_id, d09.id, d09.nombre

// Q_Dom09_2: Ciclo democrático completo
MATCH (d08:Dominio {id:'Dom08'})-[r1:GENERA]->(d09:Dominio {id:'Dom09'})
MATCH (d09)-[r2:RETROALIMENTA]->(d08)
RETURN d08.id, type(r1), d09.id, type(r2), d08.id

// Q_Dom09_3: ¿Qué LOPC ACKs instrumentan Dom09?
MATCH (a:ACK {norma_sigla:'LOPC'})-[:INSTRUMENTA]->(d09:Dominio {id:'Dom09'})
RETURN a.ack_id, a.tipo, a.nombre ORDER BY a.articulo

// Q_Dom09_4: Degree Dom08 vs Dom09 (primer dato para ADR-019)
MATCH (d:Dominio) WHERE d.id IN ['Dom08','Dom09']
OPTIONAL MATCH (n)-[r]-(d)
RETURN d.id, COUNT(r) AS degree ORDER BY degree DESC

// Q_Dom09_5: CE_1 → CE_95 → Dom08+Dom09 (díada soberanía)
MATCH (ce1:ACK {ack_id:'CE_1'})-[:CONSTITUYE]->(ce95:ACK {ack_id:'CE_95'})
MATCH (ce95)-[:FUNDA]->(d:Dominio) WHERE d.id IN ['Dom08','Dom09']
RETURN ce1.ack_id AS apex, ce95.ack_id AS nrc, COLLECT(d.id) AS diada
```

---

## Nota sobre Validación de ADR-019

Una vez que Dom09 esté completo en Neo4j y CE_95 establezca relación FUNDA con Dom09:

```cypher
// Betweenness proxy (grado) — verificación preliminar
MATCH (d:Dominio)
OPTIONAL MATCH (n)-[r]-(d)
RETURN d.id, COUNT(r) AS degree
ORDER BY degree DESC
```

Si Dom08 + Dom09 tienen los dos primeros degrees del sistema → Escenario B+C de ADR-019 observable.

Community detection formal (requiere GDS o cálculo externo):
```cypher
// Cuando GDS esté disponible en AuraDB:
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).id AS nodo, communityId
ORDER BY communityId, nodo
```

Si Dom08 y Dom09 quedan en la misma comunidad → díada constitucional confirmada empíricamente.

---

*DCO Dom09 · QUIRA Gov · Dylus Lab · 2026-06-02*  
*Basado en: ADR-016 (template) · ADR-017 (circuitos) · ADR-018 (NRC) · ADR-019 (hipótesis díada)*
