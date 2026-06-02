# ADR-019 — Dominios de Legitimación Democrática: Hipótesis Arquitectónica

**Estado**: SUPPORTED  
**Fecha de apertura**: 2026-06-02  
**Fecha de actualización**: 2026-06-02  
**Fecha de cierre**: PENDIENTE — ver Criterios de Confirmación  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Participantes**: Equipo Dylus Lab · Colega Asesor Externo  

> **SUPPORTED**: La evidencia observacional es positiva y consistente en todas las métricas disponibles. No existe ninguna métrica que contradiga la hipótesis. Falta evidencia discriminante formal (betweenness GDS, community detection) para pasar a CONFIRMED. Ver §Evidencia Acumulada.

## Evidencia Acumulada — 2026-06-02

### Degree Centrality (grafo con LOPC Dom08-Core + Dom09 seed)

| Nodo | Tipo | Degree | Posición |
|---|---|---|---|
| Dom08 | Dominio | 21 | 1° — único |
| Dom09 | Dominio | 11 | 2° (incompleto) |
| Dom07 | Dominio | 10 | 3° |
| Dom04 | Dominio | 7 | 4° |
| C01 | Circuito | 6 | 5° |
| CE_1 | ACK constituyente | 4 | — |
| CE_95 | NRC | 4 | — |
| CE_226 | NRC | 4 | — |

### Betweenness Proxy (NRC→Dominio paths, longitud 1..5)

| Nodo | Tipo | Proxy | Ratio vs Dom07 |
|---|---|---|---|
| Dom08 | Dominio | 328 | 1.58x |
| Dom07 | Dominio | 207 | 1.00x (base) |
| **CE_95** | **NRC** | **145** | **0.70x — ACK supera a Dom04** |
| Dom04 | Dominio | 128 | 0.62x |
| Dom09 | Dominio | 99 | 0.48x (incompleto) |
| CE_226 | NRC | 82 | 0.40x |
| **CE_1** | **NRC constituyente** | **82** | **0.40x — empatado con CE_226** |
| CE_18 | NRC | 76 | 0.37x |

### ACKs instrumentando dominios

| Dominio | ACKs | Normas |
|---|---|---|
| Dom08 | 13 | COOTAD + LOPC |
| Dom09 | 7 | LOPC + RES-CPCCS (incompleto) |
| Dom07 | 5 | LOTAIP + LOPC |
| Dom04 | 3 | LOPC (pendiente COOTAD 295+) |

### Díada Dom08+Dom09

- Proxy combinado: **427** vs Dom07: **207** (ratio 2.06x)
- Ciclo: Dom08 ─GENERA─► Dom09 ─RETROALIMENTA─► Dom08 ✅
- Norma raíz compartida: CE_95 ─FUNDA─► Dom08 y Dom09 ✅
- CE_1 ─CONSTITUYE─► CE_95 ─FUNDA─► [Dom08, Dom09] ✅

### Hallazgos que no estaban en la hipótesis inicial

1. **CE_95 > Dom04** en proxy: un NRC supera en centralidad a un dominio operacional completo
2. **CE_1 = CE_226** en proxy: la capa de soberanía popular ya es visible computacionalmente
3. **LOPC toca 6 dominios** con solo 15 artículos: evidencia de ley de arquitectura, no temática
4. **Dom08 degree = 2× Dom07**: diferencia no marginal, no atribuible a artefacto de carga



---

## Contexto

Durante la construcción del DCO Dom08 (Participación Ciudadana) emergió una observación arquitectónica no prevista:

Dom08 no se comporta como los demás dominios operacionales del sistema.

Dom03 (Contratación) existe para adquirir bienes y servicios.  
Dom10 (Agua) existe para prestar servicios a la ciudadanía.  
Dom02 (Presupuesto) existe para asignar recursos públicos.

Dom08 responde una pregunta diferente:

```
¿Quién autorizó esto?
¿Quién participó?
¿Quién controló?
¿Quién validó?
```

Dom08 no administra recursos ni servicios. **Administra legitimidad democrática.**

Esta observación, desarrollada en diálogo con el colega asesor (2026-06-02), generó la hipótesis que este ADR propone formalizar — pero no antes de ser falsificada empíricamente en el grafo.

---

## Distinción Conceptual Fundante

### Dom07 vs Dom08 no son equivalentes ni simétricas

**Dom07 (Transparencia)**  
Lógica: `Estado → publica información → ciudadanía observa`  
Es una lógica de **acceso**.  
Norma raíz: `CE_18` — derecho a buscar, recibir y acceder a información.  
El sujeto principal es el Estado (quien publica).

**Dom08 (Participación)**  
Lógica: `Ciudadanía → incide → decide → controla → evalúa → corrige`  
Es una lógica de **ejercicio de poder**.  
Norma raíz: `CE_95` + `CE_1` — participación protagónica / soberanía popular.  
El sujeto principal es la ciudadanía organizada (quien ejerce mandato).

### La relación correcta entre Dom07 y Dom08 es bidireccional

```
Dom07 ──INFORMA──►  Dom08   (transparencia entrega insumo para participar)
Dom08 ──DEMANDA──►  Dom07   (participación genera mandante que exige transparencia)
```

`LOTAIP_7 INSTRUMENTA Dom08` es incorrecto: la participación no nace de la transparencia jurídicamente.  
`CE_18` y `CE_95` son **raíces independientes** que se cruzan operacionalmente pero no se fundan mutuamente.

---

## La Hipótesis

### H1 — Categoría "Dominios de Legitimación Democrática"

Existe una categoría arquitectónica distinta de los dominios operacionales que incluye como mínimo:

```
Dom08 — Participación Ciudadana & Control Democrático
Dom09 — Rendición de Cuentas        [pendiente DCO]
```

Estos dominios no producen bienes ni servicios. Producen **legitimidad, control y mandato**.  
Su función es ser la **capa de traducción** entre el constituyente (el pueblo soberano) y la administración pública cotidiana.

### H2 — Dom08 como Mecanismo de Traducción Constitucional

Dom08 convierte:

```
CE_1 (soberanía abstracta del pueblo)
        ↓
Acción pública verificable y legitimada
```

Sin Dom08, CE_1 permanece como declaración constitucional sin traducción institucional.  
Con Dom08 activo, la soberanía popular se materializa en: cabildos, silla vacía, veedurías, presupuesto participativo, rendición de cuentas.

### H3 — CE_1 como Nodo Constituyente (Apex)

Los 4 NRCs funcionales actuales (CE_226, CE_18, CE_95, CE_264) describen condiciones de funcionamiento del Estado.  
CE_1 describe **quién es el titular del poder** — es ontológicamente anterior a todos ellos.

```
CE_1 ──CONSTITUYE──► CE_226  (la soberanía popular es la fuente de la legalidad)
CE_1 ──CONSTITUYE──► CE_95   (participación es el mecanismo de ejercicio de CE_1)
CE_1 ──CONSTITUYE──► CE_18   (información es prerrequisito para soberanía informada)
CE_1 ──CONSTITUYE──► CE_264  (competencias GAD son una delegación del soberano)
```

Por esto CE_1 usa la relación `CONSTITUYE` (no `HABILITA`):  
`HABILITA` = condición funcional que permite otra acción.  
`CONSTITUYE` = fuente ontológica de la que deriva la validez.

---

## Los Tres Escenarios Falsificables

Una vez que Dom08 y Dom09 estén completos en Neo4j y con LOPC ingresada, ejecutar:

```cypher
// Grado de cada nodo (proxy rápido de centralidad)
MATCH (n)
RETURN labels(n)[0] AS tipo, n.ack_id AS id,
       size((n)--()) AS degree
ORDER BY degree DESC
LIMIT 20
```

```cypher
// Betweenness centrality (requiere GDS plugin o cálculo manual)
CALL gds.betweenness.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).ack_id AS id, score
ORDER BY score DESC
LIMIT 10
```

### Escenario A — ADR-018 confirmado

Los NRCs funcionales (CE_226, CE_18, CE_95, CE_264) siguen dominando la centralidad.  
**Consecuencia**: la categoría "Legitimación Democrática" no tiene soporte empírico.  
ADR-019 pasa a estado RECHAZADO. ADR-018 permanece como doctrina canónica.

### Escenario B — Dom08 emerge como hub

Dom08 aparece con centralidad extraordinaria — mayor que cualquier ACK sectorial y comparable a los NRCs.  
**Consecuencia**: la hipótesis H1 gana fuerza empírica.  
ADR-019 pasa a estado ACTIVO. Se formaliza la categoría y se revisa la arquitectura de los 12 dominios.

### Escenario C — CE_1 conecta todo

CE_1 muestra mayor betweenness centrality que CE_226 tras cargar Dom09.  
**Consecuencia**: QUIRA no es solo una arquitectura administrativa — es una arquitectura de soberanía.  
La frase canónica del sistema requiere revisión: "el grafo revela que la constitución es un grafo de poder, no solo de legalidad."  
ADR-019 pasa a estado ACTIVO con alcance ampliado.

---

## LOPC como Evidencia Anticipatoria

La Ley Orgánica de Participación Ciudadana (~102 artículos) no regula un servicio público.  
Regula la **forma en que la ciudadanía interactúa con todo el aparato público**:

| Capítulo LOPC | Dominio(s) afectados |
|---|---|
| Principios participación (1-10) | Dom08, Dom01 |
| Democracia directa (11-40) | Dom08 |
| Participación en gestión pública (41-65) | Dom08, Dom02, Dom04 |
| **Participación en GADs (64-80)** | **Dom08 core** |
| Silla vacía (77) | Dom08, Dom03 |
| Control social (81-97) | Dom08, Dom07, Dom09 |
| **Rendición de cuentas (88-97)** | **Dom09** |
| Consejos consultivos (98-102) | Dom08, Dom12 |

Si una sola ley toca 8 de 12 dominios, eso ya es evidencia anticipatoria de que Dom08 es un nodo hub. El grafo lo confirmará o refutará con precisión.

---

## Criterios de Activación (Gate para pasar de PROPUESTO → ACTIVO)

```
1. Dom09 DCO creado (docs/adr/DCO_Dom09_*.md)
2. Dom09 cargado en Neo4j (chs_rol = DESTINO en C01, más relaciones propias)
3. LOPC completa ingresada en normativa_corpus (F0.2 crítico)
4. COOTAD Arts. 305-309 (resto de la sección participación) como ACKs
5. Centralidad medida (consulta degree + betweenness)
6. Resultado: Escenario B o C observado empíricamente
```

Si los 6 criterios se cumplen y el grafo no muestra Escenario B ni C:  
→ ADR-019 pasa a RECHAZADO  
→ Dom08 permanece como dominio sectorial con alta conectividad, sin categoría especial

---

## Decisión Provisional (en vigor hasta criterios de activación)

Mientras ADR-019 está en estado PROPUESTO:

1. **Dom08 y Dom09 se mantienen como dominios separados** en la arquitectura de 12 dominios
2. **CE_1 se registra como nrc_rango=constituyente** en el ACK Registry (distinción de los NRCs funcionales)
3. **La relación CONSTITUYE existe en Neo4j** pero con metadata `adr: 'ADR-019'` para marcar su origen hipotético
4. **LOPC ingesta = F0.2 crítico** (no ampliado — es prerrequisito del gate de activación)
5. **No renombrar Dom08 ni Dom09** — los nombres canónicos permanecen hasta que el grafo hable

---

## Ruta hacia ADR-019 Activo

```
[HOY]
  CE_1 → ACK Registry v0.4 + Neo4j (nrc_rango=constituyente, CONSTITUYE)
  ADR-019 → PROPUESTO

[Sprint Dom09]
  DCO Dom09 — Rendición de Cuentas
  Neo4j Dom09 extension

[Sprint LOPC]
  F0.2 crítico — LOPC completa /qlep
  COOTAD 305-309 ACKs

[Medición]
  Centralidad: degree + betweenness
  Observar escenario A/B/C

[Decisión]
  ADR-019 → ACTIVO o RECHAZADO
```

---

## Relacionado

- ADR-016: DCO — Estructura del Dominio Constitucional Operacionalizable
- ADR-017: Circuitos Constitucionales (C01, Triángulo P-02)
- ADR-018: Nodos Raíz Constitucionales — criterio betweenness
- DCO Dom07: docs/adr/DCO_Dom07_Transparencia_Activa.md
- DCO Dom08: docs/adr/DCO_Dom08_Participacion_Ciudadana.md

---

*ADR-019 PROPUESTO · QUIRA Gov · Dylus Lab · 2026-06-02*  
*Estado: hipótesis falsificable — no congelar hasta que el grafo hable*
