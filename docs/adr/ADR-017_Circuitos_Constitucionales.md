# ADR-017 — Circuitos Constitucionales QUIRA
## Arquitectura Formal de Cadenas Causales Multi-Dominio

**Versión:** 1.0  
**Fecha:** 2026-06-01  
**Estado:** CONGELADO v1.0  
**Autores:** Dylus Lab · Colega asesor  
**Relacionado:** ADR-013 · ADR-016 (DCO) · ACK_REGISTRY · TRES_CEREBROS_QUIRA

---

## El problema que resuelve

ADR-013 mapea circuitos QTMP a dominios individuales:

```
TRANSPARENCIA → Dom07
GAP_10PCT     → Dom12
AGUA_POTABLE  → Dom10
EQUIDAD       → Dom06
```

Ese mapeo es correcto pero incompleto. Un circuito QTMP es un **punto de entrada** a un dominio. Un Circuito Constitucional es algo diferente: **una cadena causal que cruza múltiples dominios**.

Sin ADR-017, QUIRA puede responder:
```
"¿Cumple Dom07?"  → ✅ / ❌
"¿Cumple Dom08?"  → ✅ / ❌
```

Con ADR-017, QUIRA puede responder:
```
"¿El municipio puede gobernar el ciclo Transparencia→Participación→Planificación?"
→ "Dom07 degradado (portal desactualizado 112 días). Esto inhibe la participación
   informada requerida por CE Art.95. Sin participación, el PDOT se planifica
   sin insumo ciudadano — violando CE Art.264.1. DIAGNÓSTICO SISTÉMICO:
   Ruptura de ciclo democrático cantonal."
```

La diferencia es la **causalidad constitucional**. No es una correlación estadística — es una cadena normativa verificable artículo por artículo.

---

## Diferencia entre ADR-013 y ADR-017

| Concepto | ADR-013 | ADR-017 |
|---|---|---|
| **Unidad** | Circuito QTMP → 1 dominio | Circuito Constitucional → N dominios |
| **Lógica** | Mapeo (machine-readable) | Causalidad (governance logic) |
| **Output** | Estado de 1 indicador | Diagnóstico sistémico |
| **Activación** | Por alerta QTMP | Por degradación de nodo |
| **Raíz normativa** | 1 norma clave | Cadena de ACKs interconectados |
| **Modelo** | Árbol plano | Grafo dirigido (DAG) |

**Regla canónica:**  
> ADR-013 es el punto de entrada. ADR-017 es la cadena de consecuencias.

---

## Conceptos fundamentales

### Nodo
Un Dominio (DCO) participando en un circuito. Tiene un rol y una condición de activación.

**Roles posibles:**
- `ORIGEN` — Nodo donde el fallo se origina. Su degradación propaga al siguiente.
- `INTERMEDIARIO` — Nodo de transmisión. Amplifica o atenúa la propagación.
- `DESTINO` — Nodo donde el impacto sistémico se materializa.

Un mismo dominio puede ser DESTINO en C01 y ORIGEN en C03.

### Arista
Una relación causal constitucional entre dos nodos. Tipos:
- `HABILITA` — El nodo A debe funcionar para que B pueda funcionar
- `INFORMA` — El nodo A provee insumos que B requiere para sus decisiones
- `CONTROLA` — El nodo A ejerce supervisión legal sobre B
- `FINANCIA` — El nodo A asigna recursos que B ejecuta

### Diagnóstico sistémico
El output del circuito cuando uno o más nodos están degradados. No es un indicador — es un **juicio de gobernanza** que cita las normas violadas y la cadena causal.

### Circuit Health Score (CHS) — Aporte QUIRA
Métrica agregada para el Centro de Mando. Fórmula:

```
CHS_Cn = Σ(NodeOK_i × peso_rol_i) / Σ(peso_rol_i)

donde:
  peso_rol_i:  ORIGEN=1.5 · INTERMEDIARIO=1.0 · DESTINO=0.7
  NodeOK_i:    1.0 si nodo en cumplimiento · 0.0 si degradado

Regla de colapso: Si cualquier nodo ORIGEN falla → CHS = 0.0 (independiente del resto)

Escala semáforo:
  CHS ≥ 0.80  → 🟢 ALINEADO
  CHS 0.50-0.79 → 🟡 RIESGO
  CHS < 0.50  → 🔴 RUPTURA
```

El CHS no reemplaza al diagnóstico textual — es la cara del circuito en el dashboard. El diagnóstico textual es la fundamentación jurídica.

---

## Schema de Circuito Constitucional

```yaml
circuit_id: C01                   # formato: C + número secuencial
nombre_corto: "Transparencia → Participación → Planificación"
descripcion: >
  Circuito democrático fundamental: el derecho ciudadano a la información
  (Dom07) habilita la participación informada (Dom08), que a su vez legitima
  y nutre la planificación territorial (Dom04).
triangulo_gobernanza: P-02        # si aplica — principio QUIRA relacionado

nodos:
  - dominio_id: Dom07
    rol: ORIGEN
    norma_fundante_ack: CE_18
    condicion_activacion:
      descripcion: "Portal LOTAIP sin actualización o con más del 30% de ítems vacíos"
      umbral: "90 días sin actualización o >30% ítems LOTAIP vacíos"
      fuente_medicion: "Auditoría portal Dom07 (QTMP TRANSPARENCIA)"

  - dominio_id: Dom08
    rol: INTERMEDIARIO
    norma_fundante_ack: CE_95        # revisado_por_experto: false — pendiente jurista
    condicion_activacion:
      descripcion: "Sin cabildos ni asambleas participativas en el período"
      umbral: "0 eventos participativos en 6 meses"
      fuente_medicion: "Registro Dom08 (pendiente Layer 2)"

  - dominio_id: Dom04
    rol: DESTINO
    norma_fundante_ack: CE_264_1     # revisado_por_experto: false — pendiente jurista
    condicion_activacion:
      descripcion: "PDOT sin actualización dentro del plazo legal o sin aprobación"
      umbral: "PDOT vencido o sin resolución del Concejo en período de planificación"
      fuente_medicion: "Registro PDOT Dom04 (pendiente Layer 2)"

aristas:
  - origen: Dom07
    destino: Dom08
    tipo: INFORMA
    mecanismo: >
      Sin información pública actualizada, la participación ciudadana carece de
      insumo. CE Art.18 garantiza el derecho a recibir información veraz y oportuna.
      Sin ese insumo, las asambleas se realizan sobre datos desconocidos o
      desactualizados — vacían el contenido del derecho de participación (CE Art.95).
    acks_relevantes: [CE_18, LOTAIP_7, LOTAIP_34]

  - origen: Dom08
    destino: Dom04
    tipo: HABILITA
    mecanismo: >
      La participación ciudadana es un insumo constitucional de la planificación
      territorial. CE Art.264.1 obliga al GAD a formular el PDOT "de manera articulada
      con la planificación nacional... y parroquial". Sin procesos participativos
      formales, el PDOT no tiene legitimidad democrática constitucional — no solo
      procedimental.
    acks_relevantes: [CE_95, CE_264_1, COOTAD_302]

diagnostico:
  escenarios:
    - estado: "ALINEADO"
      condicion: "Dom07 ✅ + Dom08 ✅ + Dom04 ✅"
      output: "Ciclo democrático cantonal activo. El municipio informa, participa y planifica con legitimidad constitucional."
      chs: "≥ 0.80"

    - estado: "RIESGO_ORIGEN"
      condicion: "Dom07 ❌ + Dom08 ✅ + Dom04 ✅"
      output: >
        ⚠️ RIESGO CIRCUITO C01 — ORIGEN DEGRADADO
        Dom07 sin cumplimiento: portal LOTAIP desactualizado.
        Riesgo inmediato: la participación ciudadana pierde su insumo informacional.
        Si Dom07 no se normaliza en 30 días, Dom08 comenzará a degradarse.
        Norma violada: CE Art.18 — Derecho de acceso a información pública.
      chs: "0.0 (regla colapso ORIGEN)"

    - estado: "RUPTURA_PARCIAL"
      condicion: "Dom07 ❌ + Dom08 ❌ + Dom04 ✅"
      output: >
        🚨 RUPTURA CIRCUITO C01 — CADENA ROTA
        Dom07 sin cumplimiento + Dom08 sin cumplimiento.
        La participación no está ocurriendo o está ocurriendo sin insumo real.
        Dom04 está en riesgo de planificación sin mandato democrático.
        Normas violadas: CE Art.18 + CE Art.95.
        Acción requerida: auditoría urgente portal LOTAIP + verificación registros participativos.
      chs: "0.0"

    - estado: "COLAPSO_SISTEMICO"
      condicion: "Dom07 ❌ + Dom08 ❌ + Dom04 ❌"
      output: >
        🔴 COLAPSO SISTÉMICO C01 — CICLO DEMOCRÁTICO ROTO
        El municipio no informa, no participa y no planifica con legitimidad constitucional.
        Esta es la falla de gobernanza más grave del circuito C01.
        Normas violadas: CE Art.18 + CE Art.95 + CE Art.264.1.
        Posibles consecuencias: glosa CGE por planificación sin proceso participativo
        documentado; observación DPE por violación derecho información.
        Acción inmediata: Alcaldía debe convocar Consejo de Planificación Cantonal.
      chs: "0.0"

neo4j_cypher: |
  MERGE (c:Circuit {id: 'C01'})
  SET c.nombre = 'Transparencia → Participación → Planificación',
      c.estado = 'ACTIVO', c.version = '1.0'

  MERGE (d07:Domain {id: 'Dom07'})
  MERGE (d08:Domain {id: 'Dom08'})
  MERGE (d04:Domain {id: 'Dom04'})

  MERGE (c)-[:INCLUYE {rol: 'ORIGEN',        peso: 1.5}]->(d07)
  MERGE (c)-[:INCLUYE {rol: 'INTERMEDIARIO', peso: 1.0}]->(d08)
  MERGE (c)-[:INCLUYE {rol: 'DESTINO',       peso: 0.7}]->(d04)

  MERGE (d07)-[:INFORMA  {circuito: 'C01', mecanismo: 'CE_18→CE_95'}]->(d08)
  MERGE (d08)-[:HABILITA {circuito: 'C01', mecanismo: 'CE_95→CE_264_1'}]->(d04)
```

---

## C02 — Presupuesto → Contratación → Transparencia *(spec parcial)*

```yaml
circuit_id: C02
nombre_corto: "Presupuesto → Contratación → Transparencia"
descripcion: >
  El ciclo de integridad financiera: la planificación presupuestaria (Dom02)
  determina qué se contrata (Dom03), y la transparencia de ese proceso (Dom07)
  cierra el ciclo de rendición de cuentas.
estado: PARCIAL                   # pendiente mapeo completo de aristas

nodos:
  - dominio_id: Dom02
    rol: ORIGEN
    norma_fundante_ack: COOTAD_215    # presupuesto participativo
    condicion_activacion: "Presupuesto no aprobado o no publicado en plazo legal"

  - dominio_id: Dom03
    rol: INTERMEDIARIO
    norma_fundante_ack: LOSNCP_22     # pendiente — plan anual de contratación
    condicion_activacion: "PAC no publicado o con más del 40% de procesos sin adjudicación"

  - dominio_id: Dom07
    rol: DESTINO
    norma_fundante_ack: CE_18
    condicion_activacion: "Procesos de contratación sin publicación en SERCOP o LOTAIP"

aristas:
  - origen: Dom02
    destino: Dom03
    tipo: FINANCIA
    mecanismo: "Sin presupuesto aprobado, el PAC no puede ejecutarse (LOSNCP Art.22 requiere fondos disponibles)"

  - origen: Dom03
    destino: Dom07
    tipo: INFORMA
    mecanismo: "Los procesos de contratación son sujetos obligatorios de publicación LOTAIP (art.7 literal l)"

pendiente:
  - Confirmar ACK IDs exactos para Dom03 (LOSNCP → qlep pendiente)
  - Validar condiciones de activación con experto SERCOP
  - Construir Layer 2 Dom02 + Dom03
```

---

## C03 — Planificación → Inversión → Servicios *(spec parcial)*

```yaml
circuit_id: C03
nombre_corto: "Planificación → Inversión → Servicios"
descripcion: >
  El circuito de desarrollo territorial: el PDOT (Dom04) orienta la inversión
  pública (Dom02), que se ejecuta en servicios territoriales concretos (Dom10).
  Este circuito conecta la planificación estratégica con la cobertura real.
estado: PARCIAL

nodos:
  - dominio_id: Dom04
    rol: ORIGEN
    norma_fundante_ack: CE_264_1
    condicion_activacion: "PDOT desactualizado o sin metas anualizables"

  - dominio_id: Dom02
    rol: INTERMEDIARIO
    norma_fundante_ack: COOTAD_215
    condicion_activacion: "Inversión no alineada con metas PDOT (>30% desalineación)"

  - dominio_id: Dom10
    rol: DESTINO
    norma_fundante_ack: CE_264_4      # agua potable y alcantarillado (pendiente verificación)
    condicion_activacion: "Cobertura de servicios básicos por debajo de meta PDOT"

aristas:
  - origen: Dom04
    destino: Dom02
    tipo: INFORMA
    mecanismo: "El PDOT define las prioridades de inversión. Sin PDOT actualizado, la inversión es discrecional y no territorial"

  - origen: Dom02
    destino: Dom10
    tipo: FINANCIA
    mecanismo: "Los proyectos de servicios básicos (agua, saneamiento) se financian del presupuesto de inversión GADMCM"

pendiente:
  - Construir Layer 2 Dom04
  - Confirmar ACK CE_264_4 (competencia agua potable)
  - Cruzar con datos INEC 2022 cobertura agua Dom10 (ya disponibles)
```

---

## Intersecciones entre circuitos

```
C01: Dom07 → Dom08 → Dom04
C02: Dom02 → Dom03 → Dom07
C03: Dom04 → Dom02 → Dom10
```

**Observación crítica (superación sobre diseño original):**

Los tres circuitos forman un grafo coherente donde:
- **Dom07 es nodo compartido** C01(ORIGEN) + C02(DESTINO)
- **Dom02 es nodo compartido** C02(ORIGEN) + C03(INTERMEDIARIO)
- **Dom04 es nodo compartido** C01(DESTINO) + C03(ORIGEN)

Esto significa que la degradación de Dom07 no solo rompe C01 — también bloquea el cierre de C02 (que necesita Dom07 como destino de transparencia). **Un fallo en Dom07 es un fallo en dos circuitos simultáneamente.**

Esta propiedad se llama **Nodo de Alta Centralidad** y es información que QUIRA debe exponer en el Centro de Mando:

```
ALERTA MULTI-CIRCUITO: Dom07 degradado afecta C01 + C02
CHS_C01 = 0.0 · CHS_C02 = 0.0
```

---

## Relación con ADR-013 (mapeo QTMP)

Los cuatro circuitos QTMP de ADR-013 son **puntos de entrada** a dominios individuales.  
Los circuitos constitucionales (C01, C02, C03...) son **cadenas causales** que cruzan dominios.

No son redundantes — son dos capas distintas:

```
ADR-013 TRANSPARENCIA → Dom07 (entry)
             ↓
ADR-017 C01: Dom07 → Dom08 → Dom04 (chain)
             ↓
ADR-017 C02: Dom02 → Dom03 → Dom07 (chain, Dom07 como destino)
```

Cuando el circuito QTMP TRANSPARENCIA se activa, QUIRA debe ejecutar C01 **y** C02 para el diagnóstico sistémico completo.

---

## Estado de implementación

| Circuito | Diseño | Layer 2 | Neo4j | Estado |
|---|---|---|---|---|
| C01 | ✅ COMPLETO | Dom07 parcial · Dom08/Dom04 pendiente | Cypher listo | **LISTO PARA IMPLEMENTACIÓN** |
| C02 | ⚠️ PARCIAL | Dom02/Dom03 pendiente | Pendiente | DISEÑO PENDIENTE |
| C03 | ⚠️ PARCIAL | Dom04/Dom10 pendiente | Pendiente | DISEÑO PENDIENTE |

**Próximo paso canónico:**
```
1. Cargar C01 en Neo4j (Cypher arriba)
2. Construir Layer 2 Dom08 (p08_participacion.py) — alimenta nodo INTERMEDIARIO C01
3. Completar C02 tras QLEP Dom03 (LOSNCP ACKs)
4. Completar C03 tras Layer 2 Dom04
```

---

## Por qué ADR-017 es el paso que habilita el diagnóstico sistémico

Sin circuitos formalizados:
```
QUIRA produce 12 indicadores de 12 dominios
→ El usuario recibe 12 semáforos
→ Interpreta la relación entre ellos por intuición
```

Con circuitos formalizados:
```
QUIRA evalúa 3 circuitos
→ Produce diagnósticos sistémicos causales
→ "La razón por la que la planificación falla es que no hay información (Dom07)"
→ No 12 semáforos — 1 diagnóstico con cadena normativa
```

**Esta es la capacidad que diferencia QUIRA de un dashboard de indicadores.**  
Un dashboard mide. QUIRA razona.

---

*ADR-017 v1.0 · QUIRA Gov · Dylus Lab © 2026*  
*Siguiente: C01 → Neo4j · Layer 2 Dom08 · C02 spec completa (QLEP Dom03)*
