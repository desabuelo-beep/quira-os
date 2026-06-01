# QNKC — Índice de Principios Arquitectónicos del Framework

**Estado:** Vivo — se actualiza al congelar cada nuevo principio  
**Versión:** 1.2  
**Fecha creación:** 2026-06-01 · Última actualización:** 2026-06-01  
**Clasificación en la jerarquía de gobernanza:** Primer nivel — al mismo nivel que ADRs del núcleo y QLEP Canónico  
**Clasif.:** Interno · QUIRA Operaciones

> **"QUIRA no verifica documentos. QUIRA verifica cadenas causales."**

---

## Posición en la arquitectura de gobernanza

Este documento no es documentación auxiliar. Es una pieza fundacional de la filosofía operativa de QUIRA.

| Artefacto | Qué congela |
|-----------|-------------|
| QLEP Canónico | La base normativa — qué obliga el ordenamiento jurídico |
| ADRs | Las decisiones de implementación — cómo se construye el sistema |
| **QNKC Principios** | **La epistemología — cómo QUIRA sabe lo que sabe y qué errores de razonamiento evita** |

Los ADRs dicen qué se decidió. Los principios QNKC dicen por qué el sistema razona como razona. Sin los principios, cada sprint puede reinventar los mismos errores de categoría.

---

## Hipótesis Arquitectónica H-QNKC-01 (congelada 2026-06-01)

> **Todos los principios QNKC emergen cuando existe riesgo de confundir un artefacto administrativo con el efecto institucional que dicho artefacto pretende representar.**
>
> El objetivo del framework no es verificar la existencia de documentos, sino reconstruir la cadena causal entre obligación pública, ejecución institucional y transformación verificable de la realidad.
>
> Por tanto, todo nuevo principio QNKC deberá formularse como una ruptura explícita de un falso equivalente institucional.

Esta hipótesis es la que unifica P00, P01, P02, P03 y P04 en una familia — no en una lista.

---

## Hipótesis Arquitectónica H-QNKC-02 (registrada 2026-06-01)

> **Las capacidades institucionales observables en QUIRA se modelan como cadenas multiplicativas de condiciones necesarias.**
>
> Una dimensión ausente invalida la capacidad completa, aunque todas las demás existan.
>
> Esto no es una convención matemática — es un axioma epistemológico: en gobernanza pública, las condiciones para que un proceso produzca resultado no son aditivas ni compensables. No se puede "promediar" transparencia real.

**Cómo emerge H-QNKC-02:** cuando P01 descompone `verificabilidad_efectiva = C5a × C5b × C5c`, y el mismo patrón reaparece en C8, P02, P03 y P04, el framework revela que la multiplicación no es una característica de Dom07 — es la gramática matemática del sistema completo.

**Diferencia con H-QNKC-01 — dos ejes ortogonales:**

| Hipótesis | Eje | Pregunta que responde |
|-----------|-----|----------------------|
| H-QNKC-01 | Categorial — qué confusión destruye el principio | ¿Este patrón confunde un proceso con su resultado? |
| H-QNKC-02 | Matemático — cómo modela QUIRA la capacidad institucional | ¿Cómo se agregan las condiciones necesarias en el indicador? |

Son ortogonales: H-QNKC-01 determina el contenido de un principio, H-QNKC-02 determina su forma matemática. Todo principio válido del framework satisface ambas hipótesis simultáneamente.

**La diferencia que H-QNKC-02 captura:**

Los sistemas GovTech convencionales agregan atributos como suma:
```
Transparencia = (Publicado + Actualizado + Comprensible) / 3
             = (100 + 100 + 0) / 3 = 66.7 → "transparencia aceptable"
```

QUIRA encadena condiciones necesarias como producto:
```
Transparencia = Publicado × Actualizado × Comprensible
             = 1 × 1 × 0 = 0 → "transparencia fallida"
```

La comprensión no es un extra — es condición necesaria. No hay transparencia sin ella. Si cualquier eslabón es cero, la cadena completa colapsa.

**Test QNKC — Criterio formal de admisión al árbol de principios:**

Para que un candidato sea aceptado como Principio o Scheduled Principle, debe satisfacer ambas hipótesis simultáneamente:

| Test | Pregunta | Si falla |
|------|---------|---------|
| H-QNKC-01 | ¿Destruye un falso equivalente institucional (proceso ≠ resultado)? | No es principio |
| H-QNKC-02 | ¿La capacidad resultante colapsa si falta alguna condición necesaria? | No es principio |

Dos casos de fallo instructivos:

**Caso A — Cumple H-QNKC-01, falla H-QNKC-02:**  
Ejemplo: "Verificabilidad ≠ Comprensión." Destruye un falso equivalente (✔ H-QNKC-01), pero es una refinación de C5 dentro de P01, no una cadena multiplicativa independiente. No genera nuevo nivel causal. → OBS-QNKC.

**Caso B — Cumple H-QNKC-02, falla H-QNKC-01:**  
Ejemplo: "Disponibilidad = Servidor × Base de datos × API." La multiplicación es real (✔ H-QNKC-02), pero no destruye una confusión proceso/resultado — es un requisito de infraestructura. → Regla técnica de implementación.

Solo cuando ambas condiciones se satisfacen simultáneamente el candidato entra al árbol.

**Estructura multiplicativa pre-formal de los Scheduled Principles:**

H-QNKC-02 predice la forma interna de P02–P04 antes de que estén formalizados. Cuando su sprint llegue, estas estructuras son la hipótesis de partida, no el resultado final:

| Principio | Cadena multiplicativa anticipada | Si = 0 |
|-----------|----------------------------------|--------|
| P02 | `participación_efectiva = Convocatoria × Deliberación × Incidencia_real` | 500 asistentes sin incidencia = participación nula |
| P03 | `seguimiento_efectivo = Medición × Alerta × Corrección_aplicada` | Dashboard perfecto sin corrección = seguimiento nulo |
| P04 | `rendición_efectiva = Informe × Verificación × Corrección_posterior` | Audiencia pública sin corrección = rendición nula |
| P05 | `impacto = C9a_output × Continuidad_temporal × C9b_outcome` | Mejora anual sin variación censal = output, no impacto |

**Implicación para la tagline canónica:**

> *"QUIRA no verifica documentos. QUIRA verifica cadenas causales."*

La precisión técnica que H-QNKC-02 añade:

> *"QUIRA verifica cadenas causales compuestas por condiciones necesarias."*

La primera frase describe la topología del sistema (cadenas, no atributos aislados). La segunda describe el álgebra (multiplicativa, no aditiva). Ambas son verdad — la segunda es la especificación técnica de la primera.

---

## Hipótesis Arquitectónica H-QNKC-03 (anticipada — QUIRA Impact)

> **La verificación de una cadena causal no equivale a la atribución de su resultado.**
>
> Demostrar que la cadena de condiciones necesarias estuvo intacta (H-QNKC-02) no demuestra que esa cadena fue la causa del cambio observado. El cambio pudo haber ocurrido por factores externos no capturados en el modelo.

**Por qué no es extensión de H-QNKC-02:**

| Hipótesis | Pregunta | Modelo matemático |
|-----------|---------|-------------------|
| H-QNKC-02 | ¿La cadena de condiciones necesarias estuvo intacta? | Producto: C = c₁ × c₂ × c₃ |
| H-QNKC-03 | ¿El cambio observado fue causado por esa cadena y no por otro factor? | Contrafactual: E[outcome\|intervención] − E[outcome\|sin intervención] |

Son preguntas epistemológicamente distintas. P00–P05 verifican cadenas. P06 atribuye cambios. Esa distinción requiere un tercer axioma porque la multiplicación no puede resolver la identificación causal contrafactual.

**Cuándo se necesitará:**  
Cuando P06 (Impacto ≠ Transformación sistémica) se formalice. En ese momento, la pregunta ya no será "¿la cobertura de agua mejoró?" sino "¿mejoró porque la inversión municipal lo causó, o mejoró por factores demográficos / transferencias nacionales / ciclo climático?" QUIRA Impact necesitará un modelo de atribución (diferencias en diferencias, control sintético, o similar) que la cadena multiplicativa no puede proveer.

**Estado:** Anticipada — no necesaria para BETA-CORE. Activación cuando QUIRA Impact entre en diseño.

---

## Estructura Axiomática del Framework

**La transición de catálogo a sistema axiomático (2026-06-01):**  
Hasta la formalización de H-QNKC-02, el framework era una colección de principios organizados bajo un meta-principio. Con la aparición de dos hipótesis ortogonales que validan formalmente cada principio, el framework adquirió estructura axiomática. Los principios dejaron de ser intuiciones registradas — pasaron a ser derivaciones demostrables.

El sistema completo tiene cuatro niveles con responsabilidades distintas:

| Nivel | Tipo | Función lógica | Ejemplos |
|-------|------|---------------|---------|
| 1 — Raíz | Hipótesis Arquitectónica (H-QNKC-NN) | Axiomas — definen la gramática desde la que se derivan los principios | H-QNKC-01, H-QNKC-02 |
| 2 — Derivaciones | Principios (Pxx) | Teoremas — destruyen falsos equivalentes satisfaciendo ambas hipótesis | P00, P01 |
| 3 — Refinaciones | Observaciones (OBS-QNKC-NN) | Corolarios — patrones que refinan un principio existente sin ser independientes | OBS-QNKC-01 |
| 4 — Expresiones | Implementaciones | Instanciaciones del sistema en artefactos concretos | QTMP, QLEP, GeoTwin, Constitución de Lenguaje |

**Por qué cuatro niveles y no tres:**  
Sin el nivel de Observaciones, el árbol inflaría sus principios con refinamientos locales. P07, P08, P09 aparecerían para cosas que son especificaciones de C5, C8 o C9 dentro de principios ya congelados. OBS-QNKC absorbe esos patrones sin elevarlos artificialmente.

**La consecuencia de gobernanza:**  
Cuando aparece un candidato, la pregunta ya no es "¿es importante?" sino "¿a qué nivel pertenece?":

```
¿Satisface H-QNKC-01 Y H-QNKC-02?   → Principio o Scheduled
¿Satisface H-QNKC-01 pero no H-QNKC-02? → OBS-QNKC
¿Satisface H-QNKC-02 pero no H-QNKC-01? → Regla técnica (no entra al árbol)
¿No satisface ninguna?                   → Contexto de implementación (no entra al árbol)
```

Eso es más estable que el criterio anterior: no depende de juicio. Depende de verificación contra axiomas.

---

## Unificación — Una Sola Teoría de Causalidad Institucional

La consecuencia más profunda del sistema axiomático:

> **QUIRA no tiene una teoría de transparencia, una teoría de participación y una teoría de rendición.**  
> **Tiene una sola teoría de causalidad institucional.**  
> **Todos los principios son proyecciones de esa teoría sobre distintos dominios.**

| Principio | Dominio de proyección | Falso equivalente en el dominio |
|-----------|----------------------|--------------------------------|
| P00 | Capa normativa (C1–C2) | La norma no implica cumplimiento |
| P01 | Capa documental (C4–C5) | El documento no implica evidencia |
| P02 | Dom08 Participación Ciudadana | El acto participativo no implica influencia |
| P03 | Dom03 Seguimiento de Metas | La medición no implica corrección |
| P04 | Dom09 Rendición de Cuentas | El informe no implica cambio |
| P05 | Dimensión temporal / longitudinal | El output anual no implica impacto censal |
| P06 | Escala sistémica | El impacto puntual no implica transformación |

En cada fila, la estructura subyacente es idéntica:
- H-QNKC-01 identifica la confusión proceso/resultado específica al dominio
- H-QNKC-02 describe la cadena multiplicativa de condiciones necesarias en ese dominio

**Consecuencia sobre los Scheduled Principles:**  
Las estructuras pre-formales de P02–P04 registradas en H-QNKC-02 no son hipótesis sobre lo que el sprint puede descubrir. Son derivaciones de la teoría. El Sprint de Dom08 no inventará la estructura de P02 — la calibrará: definirá qué cuenta como "Incidencia real" en el contexto concreto de Montecristi. La forma ya está determinada por los axiomas. Solo los coeficientes son empíricos.

**Consecuencia sobre el crecimiento del framework:**  
Si QUIRA incorpora un nuevo dominio institucional, la teoría ya predice la forma de su principio antes de que exista:
1. ¿Qué confusión proceso/resultado es institucionalmente peligrosa en ese dominio? → H-QNKC-01 aplicado
2. ¿Cuáles son las condiciones necesarias cuya ausencia colapsa la capacidad en ese dominio? → H-QNKC-02 aplicado

El framework no necesita inventar para crecer. Necesita proyectar.

**La consecuencia metodológica para los sprints:**

Bajo el modelo axiomático, cada sprint tiene dos tipos de trabajo que no pueden mezclarse:

| Tipo | Qué determina | Quién lo determina | Ejemplo Sprint 4 |
|------|--------------|-------------------|-----------------|
| Estructura causal | La forma del indicador — qué factores, en qué relación multiplicativa | Los axiomas — derivación formal | `C8 = C4 × C5a × C5b × C5c` para Dom07 |
| Parámetros empíricos | Los valores, pesos y fuentes de cada factor | El sprint — observación del territorio en Montecristi | ¿Qué fuente provee C5c? ¿Qué umbral define "comprensible"? |

Sprint 4 no diseña la teoría de Dom07. La implementa.  
La forma ya está fijada por P01: C4 → C5a → C5b → C5c → C8.  
El sprint descubre los parámetros: qué datasource alimenta cada dimensión, qué umbrales activan el semáforo, qué peso relativo recibe cada C5 en el indicador.

Lo mismo aplica a todos los sprints subsecuentes:

- **Sprint Dom08** no inventa la estructura de P02 — calibra qué cuenta como `Incidencia_real` en el contexto concreto de Montecristi
- **Sprint Dom03** no inventa la estructura de P03 — calibra qué constituye `Corrección_aplicada` verificable en el ciclo de seguimiento del GAD
- **Sprint Obs. Longitudinal** no inventa la distinción C9a/C9b — la aplica: debe separar outputs anuales de outcomes censales *antes* de construir la serie temporal, o el instrumento leerá NBI inmóvil como impacto = 0, cuando en realidad significa resolución temporal insuficiente

**El cambio de pregunta que los axiomas producen:**

```
Antes: ¿Cómo debería verse este dominio?

Ahora: ¿Qué variables, fuentes y pesos calibran
        la estructura que P0N ya determinó?
```

La primera pregunta es abierta — cualquier sprint puede responderla de forma diferente. La segunda es cerrada en su forma y abierta solo en sus coeficientes. Eso es lo que hace que el sistema sea acumulable sin perder coherencia.

---

## Meta-principio raíz

> **Existencia documental ≠ Cumplimiento institucional**

Esta formulación es correcta pero incompleta. La raíz más profunda es:

> **Proceso ≠ Resultado**

Cada falso equivalente que los principios QNKC destruyen es una confusión entre el proceso de hacer algo y el resultado de haberlo hecho. El artefacto documental siempre registra el proceso. QUIRA siempre mide el resultado.

**Regla generativa de nuevos principios QNKC:**

> ¿Estamos midiendo el proceso de X o el resultado de X?  
> Si la distinción colapsa en algún punto del sistema → hay un principio QNKC esperando ser formalizado.

---

## Tabla de Falsos Equivalentes — El Framework como Teoría

QUIRA puede leerse como un sistema que destruye sistemáticamente los falsos equivalentes de la gobernanza pública:

| Nivel | Principio | Falso equivalente destruido | Consecuencia de diseño |
|-------|-----------|---------------------------|------------------------|
| Jurídico | P00 | Norma ≠ Cumplimiento | LOTAIP en C4, no en C2 |
| Documental | P01 | Documento ≠ Evidencia | C8 = cumplimiento × verificabilidad |
| Participativo | P02 | Participación ≠ Influencia | Dom08 C9 requiere trazar decisión modificada |
| Operacional | P03 | Medición ≠ Acción | Dom03 C9 requiere trazar corrección aplicada |
| Institucional | P04 | Rendición ≠ Cambio | Dom09 C9 requiere trazar corrección posterior al informe |

La mayoría de sistemas GovTech miden:
```
Existe documento = Sí → compliance = cumplido
```

QUIRA reconstruye la cadena completa de causalidad:
```
Existencia     → ¿El artefacto existe?              (P00)
Verificación   → ¿Es verificable por terceros?       (P01)
Incidencia     → ¿Cambió una decisión?              (P02)
Corrección     → ¿Disparó una acción?               (P03, P04)
Impacto        → ¿Produjo variación territorial?    (P05)
Transformación → ¿Cambió el sistema?                (P06)
```

Cada eslabón es un principio QNKC. Cada salto entre eslabones es donde los sistemas GovTech convencionales se detienen.

**Mapa de la progresión al roadmap de productos QUIRA:**

| Profundidad causal | Principios | Producto QUIRA | Hito |
|-------------------|-----------|---------------|------|
| Existencia + Verificación | P00, P01 | QUIRA Gov — Dom07 | Sprint 4 |
| Incidencia + Corrección | P02, P03, P04 | QUIRA Gov — BETA-CORE | MILESTONE_002 |
| Impacto | P05 | QUIRA Longitudinal | Sprint Obs. Longitudinal |
| Transformación | P06 | QUIRA Impact | Sin fecha |

La serie QNKC no es solo filosofía — es el mapa de madurez del sistema.

---

## Evolución del Framework — Las Tres Fases

**Fase 1 — La pregunta era de posición normativa:**
> ¿Dónde vive LOTAIP en la cadena causal?

Producto: P00 — OBLIGACIÓN SUSTANTIVA ≠ VENTANA DE OBSERVACIÓN  
Eje: posición de la norma en C1-C9

**Fase 2 — La pregunta pasó a ser de lectura epistémica:**
> ¿Qué significa realmente que un documento exista?

Producto: P01 — DUALIDAD EPISTÉMICA  
Eje: quién lee el artefacto y con qué propósito (C4 vs C5)

**Fase 3 — La pregunta ahora es de consecuencia institucional:**
> ¿Cómo sabe QUIRA que un acto institucional produjo una consecuencia real?

Productos pendientes: P02 (participación), P03 (seguimiento), P04 (rendición)  
Eje: longitud de la cadena entre C5 y C9

Las tres fases no se reemplazan. Se acumulan. Sprint 4 necesita las tres.

---

## GeoTwin Vista B — La Manifestación Territorial

GeoTwin Vista B (post-MILESTONE_002) no es una funcionalidad. Es la manifestación territorial del mismo meta-principio.

Los principios QNKC recorren la pregunta desde la epistemología:
```
Documento → Evidencia → Verificación → Impacto
```

GeoTwin Vista B recorre la misma pregunta desde el territorio:
```
Competencia → Obligación → Proceso → Resultado → Territorio
```

Son dos recorridos hacia la misma pregunta fundamental:
> ¿La obligación pública produjo una transformación observable en la realidad?

Uno llega desde el cómo-sabemos. El otro llega desde el dónde-ocurrió.  
GeoTwin Vista B es la evidencia espacial de que la cadena causal QNKC cerró.

---

## Principios Congelados

### P00 — OBLIGACIÓN SUSTANTIVA ≠ VENTANA DE OBSERVACIÓN

**Estado:** Congelado (origen: decisión Dom07 / TRANSPARENCIA QTMP, 2026-06-01)  
**Falso equivalente destruido:** Norma ≠ Cumplimiento  
**Enunciado:** Una norma que crea un mecanismo de publicación o verificación no crea la obligación de prestar el servicio — solo crea la ventana desde la cual se puede observar si el servicio fue prestado.  
**Consecuencia:** LOTAIP en C4, no en C2. Dom07 no absorbe los dominios operativos.  
**Documentado en:** `QLEP_CANONICO_MONTECRISTI_v1.0.md` · `qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` · `app/connectors/neo4j_qtmp.py`

---

### P01 — DUALIDAD EPISTÉMICA EN DOMINIOS OBSERVACIONALES

**Estado:** Congelado v1.1 (2026-06-01)  
**Falso equivalente destruido:** Documento ≠ Evidencia  
**Enunciado:** El mismo artefacto documental cumple simultáneamente función operativa (C4) y función probatoria (C5) según quién lo lee. No son dos documentos — son dos lecturas del mismo documento.  
**Consecuencia:** `C8 = cumplimiento_formal × verificabilidad_efectiva`. Multiplicación, no promedio — si la verificabilidad es cero, C8 es cero aunque el cumplimiento formal sea 100%.  
**Dominios:** Dom07 (ALTO), Dom09 (MEDIO), Dom08 (MEDIO)  
**Documentado en:** `governance/framework/QNKC_P01_Dominios_Observacionales.md`

---

## Principios Pendientes de Formalizar

Dos categorías: **scheduled** (vinculados a un sprint o hito conocido) y **anticipated** (sin fecha, requieren condiciones que no existen aún).

### Scheduled — Vinculados a sprints del roadmap BETA-CORE y post-M002

| Código | Momento de formalización | Falso equivalente | Pregunta que lo dispara |
|--------|-------------------------|------------------|------------------------|
| P02 | Sprint 6 (Dom08) | Participación ≠ Influencia | ¿El acta demuestra que la participación cambió una decisión concreta de inversión? |
| P03 | Sprint 10 (Dom03) | Medición ≠ Acción | ¿El semáforo rojo de seguimiento disparó una corrección de gestión verificable? |
| P04 | Sprint 11 (Dom09) | Rendición ≠ Cambio | ¿El informe de rendición generó correcciones institucionales observables y trazables? |
| **P05** | **Sprint Observabilidad Longitudinal (post-MILESTONE_002)** | **Resultado ≠ Impacto** | **¿El dato de C9 mide lo que la institución entregó, o lo que cambió en el territorio como consecuencia?** |

Cada uno se formaliza cuando su sprint detecta el punto donde el sistema podría confundir un proceso con su resultado — o en el caso de P05, un output con un outcome.

**Nota sobre P05 — no es opcional y tiene una consecuencia de frecuencia:**

C9 en QUIRA actualmente mezcla sin distinción dos fenómenos con **velocidades causales incompatibles**:

| Subcapa | Tipo | Ejemplo | Frecuencia de cambio observable |
|---------|------|---------|--------------------------------|
| C9a | Output — lo que la institución entregó | "Cobertura agua 34.9% → 42%" | Anual — medible desde SIGEF + EP |
| C9b | Outcome — lo que cambió en el territorio | "Brecha NBI sin cambio" | Censal — INEC produce estimaciones cada 5-10 años |

Un municipio puede mejorar C9a año a año sin que C9b se mueva. Eso no es falla del sistema — es la diferencia entre resultado e impacto. QUIRA debe poder representar ambos hechos simultáneamente sin confundirlos.

**La consecuencia arquitectónica crítica:** si el Sprint Observabilidad Longitudinal no distingue C9a de C9b antes de construir la serie temporal, los snapshots T0, T1, T2 van a parecer que "NBI no cambia" — no porque el impacto no ocurra, sino porque el instrumento de medición tiene resolución insuficiente para detectarlo en el plazo anual institucional. La serie temporal va a malinterpretar ausencia de dato como ausencia de impacto.

El Sprint Observabilidad Longitudinal ya está planificado (Punto #1 establecido 2026-05-26). P05 debe formalizarse antes de que ese sprint defina qué mide C9.

### Anticipated — Sin fecha, requieren condiciones que no existen aún

| Código | Falso equivalente | Condición de activación |
|--------|------------------|------------------------|
| P06 | Impacto ≠ Transformación sistémica | Requiere series longitudinales multi-año + datos causales que demuestren que la política sostenida (no solo un ciclo) produjo cambio estructural. No existen aún en el sistema. Aparecerá cuando QUIRA Impact se desarrolle. |

**P06 no se formaliza sin datos.** La distinción entre "mejoró 3pp en 2026" (impacto puntual) y "Montecristi redujo su brecha NBI en X años de política continua" (transformación sistémica) requiere una dimensión temporal y un modelo causal que BETA-CORE no construye. El colega tiene razón: P06 aparecerá solo cuando el sistema lo necesite.

---

## Observaciones Arquitectónicas Registradas

Patrones identificados que **no son principios aún** — no tienen sprint que los requiera — pero que reaparecerán con alta probabilidad y merecen registro para no perderlos.

### OBS-QNKC-01 — Verificabilidad ≠ Comprensión

**Estado:** Observación registrada (2026-06-01) — sin formalizar como principio  
**Falso equivalente insinuado:** Evidencia ≠ Inteligibilidad  
**Enunciado:** Un documento puede ser perfectamente verificable (existe, es descargable, tiene contenido del período vigente) y seguir siendo opaco para el ciudadano común. La verificabilidad confirma la existencia del documento; la comprensión confirma su utilidad democrática.

```
Presupuesto publicado        ✔
PDF descargable              ✔
Legible para auditor experto ✔
Comprensible para ciudadano  ✗  ← OBS-QNKC-01
```

**Por qué no es P02:** Es una refinación de C5 dentro de P01, no un nivel nuevo de la cadena causal. P01 dice "el mismo artefacto tiene dos lecturas." OBS-QNKC-01 dice "hay tres niveles de lectura C5, no uno."

| Nivel C5 | Verificación | Pregunta |
|----------|-------------|---------|
| C5 básica | C5a · Existencia | ¿El documento existe y es accesible? |
| C5 media | C5b · Actualidad | ¿El contenido es del período vigente y está completo? |
| C5 avanzada | C5c · Inteligibilidad | ¿Un ciudadano común puede entenderlo y usarlo? |

**Fórmula operativa de los tres niveles:**

```
verificabilidad_efectiva = C5a × C5b × C5c
```

Coherencia estructural con C8: la multiplicación es la misma lógica. Si C5c (inteligibilidad) es cero — el documento existe y está actualizado pero nadie puede entenderlo — la verificabilidad es cero aunque C5a y C5b sean perfectos. El sistema no puede premiar transparencia inaccesible. Exactamente el mismo mecanismo que en `C8 = cumplimiento_formal × verificabilidad_efectiva`.

**Ya implementado parcialmente en el sistema:**
- Estado `INCOMPRENSIBLE` en `qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` — uno de los 5 estados posibles de publicación LOTAIP
- Constitución de Lenguaje QUIRA v1 (congelada 2026-05-29) — 5 audiencias discursivas + reglas de plain language para C10 narrativas

OBS-QNKC-01 es el puente epistemológico que une QNKC (cómo el sistema sabe lo que sabe) con la Constitución de Lenguaje (cómo el sistema comunica lo que sabe). No eran dos artefactos independientes — ambos protegen contra el mismo falso equivalente.

**Cuándo formalizarlo:** cuando GeoTwin Vista B entre en diseño (requiere que la vista constitucional sea comprensible para la ciudadanía, no solo para el auditor) o cuando las narrativas C10 necesiten un criterio explícito para decidir qué lenguaje es suficientemente claro. Probablemente post-MILESTONE_002.

---

### OBS-QNKC-02 — Portal Regulatorio ≠ Portal Institucional como Fuente de C5

**Estado:** Observación registrada (2026-06-01) — activa Sprint 4  
**Falso equivalente insinuado:** Portal GAD = Fuente autoritativa de cumplimiento LOTAIP  
**Principio padre:** P01 — Documento ≠ Evidencia (Dualidad Epistémica QNKC-P01)  
**Descubierta durante:** Calibración Sprint 4 — Dom07 Transparencia  
**Norma asociada:** Ley Orgánica de Transparencia y Acceso a la Información Pública (LOTAIP 2.0 — reforma vigente)

**Enunciado:**

En dominios observacionales cuya obligación C4 incluye publicación conforme LOTAIP, la fuente canónica de C5 (verificabilidad externa) no es el portal institucional del propio GAD — es el portal regulatorio de la Defensoría del Pueblo del Ecuador: **transparencia.dpe.gob.ec**.

**La dualidad aplicada a nivel de infraestructura:**

| Fuente | Capa QNKC | Perspectiva | Autoridad |
|--------|-----------|-------------|-----------|
| Portal GAD (montecristi.gob.ec) | C4 | El GAD declara que publicó | Autodeclaración — puede divergir de la fuente oficial |
| Portal DPE (transparencia.dpe.gob.ec) | C5 | La DPE confirma qué publicó el GAD | Autoridad regulatoria — fuente oficial de cumplimiento LOTAIP |

El portal GAD es C4 (el proceso de publicación). El portal DPE es C5 (la verificación externa de ese proceso). Esto es exactamente la Dualidad Epistémica de P01 — el mismo artefacto documental leído desde dos perspectivas — aplicada ahora al nivel de la infraestructura digital regulatoria.

**Consecuencia operativa para C5a/C5b:**

- **C5a (Existencia):** ¿El numeral aparece registrado en `transparencia.dpe.gob.ec` para el GAD Montecristi?
- **C5b (Actualidad):** ¿La fecha de carga en el portal DPE corresponde al período obligatorio?

C5c (Inteligibilidad) es una evaluación cualitativa del contenido del documento — aplica independientemente del portal donde se consulte. OBS-QNKC-01 y OBS-QNKC-02 son ortogonales:

```
OBS-QNKC-01 → QUÉ mide C5     (tres dimensiones: C5a · C5b · C5c)
OBS-QNKC-02 → DÓNDE se verifica C5a/C5b  (portal regulatorio, no institucional)
```

**Consecuencia para la replicación a 221 GADs — implicación arquitectónica mayor:**

| Escenario | Fuente C5a/C5b | Costo de calibración |
|-----------|----------------|----------------------|
| Sin LOTAIP 2.0: portal GAD por institución | 221 portales distintos, scraping heterogéneo | Alto — estructura diferente por cantón |
| Con LOTAIP 2.0: portal DPE centralizado | 1 portal con estructura uniforme | Bajo — consulta única, dato estandarizado |

**Complejidad observacional — Transformación O(n) → O(1):**

La consecuencia arquitectónica de OBS-QNKC-02 es una reducción en la complejidad de verificación de C5a/C5b:

Esquema pre-OBS-QNKC-02 — 221 fuentes heterogéneas:
```
221 portales municipales
       ↓
221 conectores específicos
       ↓
221 modelos de scraping
```

Esquema post-OBS-QNKC-02 — fuente regulatoria unificada:
```
Portal DPE (transparencia.dpe.gob.ec)
      ↓
Fuente observacional unificada y estandarizada
      ↓
221 GADs
```

La complejidad de verificación C5a/C5b cambia de O(n) — un conector por cada GAD — a O(1) — una sola consulta a fuente canónica. Esto no es solo una mejora operacional. Cambia el modelo de escalabilidad de QUIRA: el costo de cubrir un nuevo GAD en Dom07 deja de ser proporcional al número de GADs y pasa a ser el costo fijo de un único conector DPE. Para BETA-CORE (Montecristi) es una mejora en robustez de datos. Para la visión de 221 GADs, es la diferencia entre un proyecto inescalable y uno que escala por definición.

**Consecuencia epistemológica — cambio de pregunta bautismal N2 Dom07:**

OBS-QNKC-02 produce una consecuencia directa y verificable sobre la pregunta fundacional de Dom07. La distinción no es operacional — es epistemológica: el objeto de evaluación cambia de sujeto:

| Versión | Pregunta implícita | Fuente de observación | Perspectiva |
|---------|-------------------|----------------------|-------------|
| N2 v1.0 | ¿Qué afirma haber publicado el municipio? | Portal GAD — autodeclaración | C4 (proceso) |
| N2 v1.0.1 | ¿Qué verifica un tercero institucional como publicado? | Portal DPE — regulador externo | C5 (evidencia) |

```
QUIRA deja de evaluar:
  lo que el GAD afirma haber publicado

QUIRA pasa a evaluar:
  lo que un tercero institucional puede verificar como publicado
```

Esta es exactamente la Dualidad Epistémica de P01 aplicada al nivel de infraestructura digital: el portal GAD es C4 (el proceso de publicación, autodeclarado), el portal DPE es C5 (la verificación externa de ese proceso). OBS-QNKC-02 hace explícito el punto de lectura correcto para el lado C5 de la dualidad.

La N2 actualizada (v1.0.1) está documentada en `QLEP_CANONICO_MONTECRISTI_v1.0.md` — enmienda LOTAIP 2.0 como evento normativo calificante.

**Relación con OBS-QNKC-01:**

OBS-QNKC-01 resuelve "¿cuántos niveles tiene C5?" (respuesta: tres — C5a · C5b · C5c).  
OBS-QNKC-02 resuelve "¿dónde se verifica C5a y C5b?" (respuesta: en el portal regulatorio DPE, no en el portal institucional del GAD).

Ambas refinan P01 desde ángulos complementarios y ambas son necesarias para calibrar Dom07 correctamente.

**Pendiente de verificación (calibración Sprint 4):**
- Confirmar que LOTAIP 2.0 establece obligación (no recomendación) de carga en portal DPE
- Verificar si transparencia.dpe.gob.ec tiene API de consulta programática
- Identificar el path/entidad exacta para Montecristi en el portal DPE
- Verificar si LOTAIP 2.0 modificó el número de numerales obligatorios (el colega observó hasta 24 en la navegación — pendiente contrastar con texto legal)

**El desplazamiento epistemológico completo — de autodeclaración a observación externa:**

OBS-QNKC-02 no solo cambia la fuente de un dato. Cambia el sujeto de evaluación de QUIRA en Dom07:

```
Modelo anterior:
  ¿Qué afirma haber publicado el GAD? (autodeclaración — C4)

Modelo OBS-QNKC-02:
  ¿Qué verifica un tercero institucional como publicado? (observación externa — C5)
```

Dom07 dejó de ser un dominio de autodeclaración y pasó a ser un dominio de observación externa. Este es el núcleo epistemológico de P01 (Dualidad Epistémica) aplicado no a los documentos sino a la infraestructura digital que los contiene: el portal GAD es C4 (el proceso de publicación), el portal DPE es C5 (la verificación de ese proceso por un tercero con autoridad regulatoria).

**Patrón generalizador — Verificadores Externos por Dominio:**

OBS-QNKC-02 probablemente no es específica de Dom07 (LOTAIP). Si el patrón se mantiene, otros dominios tienen su equivalente de verificador externo:

| Dominio | Fuente primaria actual (C4) | Posible fuente observacional externa (C5) | Institución verificadora |
|---------|----------------------------|------------------------------------------|--------------------------|
| Dom07 Transparencia | Portal GAD · autodeclaración | `transparencia.dpe.gob.ec` | DPE |
| Dom08 Participación | Actas municipales · proceso | Evidencia de incidencia en PDOT/POA firmado | Consejo Planificación / CPCCS |
| Dom09 Rendición | Informe municipal · autodeclaración | Evaluación externa / observatorio rendición | CPCCS |
| Dom03 Seguimiento | Reporte interno de metas | SIGEF (ejecución financiera) / CGE (auditoría) | MEF / CGE |

La pauta subyacente es directamente derivada de P01: QUIRA prioriza el verificador externo cuando existe con autoridad normativa y estructura consultable sobre el dominio evaluado.

**Cuándo formalizarlo como P07:** Si Dom07 (DPE) valida y Dom08 (CPCCS) + Dom09 (CPCCS/DPE) confirman el mismo patrón en sus respectivos sprints, el candidato es:

> **P07 — Autodeclaración ≠ Verificación Externa (en C5)**  
> *"Para evaluar la verificabilidad C5 de una capacidad institucional, QUIRA prioriza fuentes regulatorias externas sobre autodeclaraciones del propio GAD."*

P07 satisfaría H-QNKC-01 (destruye el falso equivalente "declaración de cumplimiento = cumplimiento verificable por tercero") y H-QNKC-02 (la verificabilidad colapsa si no existe verificador externo con cobertura positiva). El test formal se aplica cuando Dom08 y Dom09 tengan sus sprints — no antes.

**Validación en curso — ADR-015:**

La auditoría N4 de Dom07 responde dos preguntas simultáneas:
- **Pregunta operativa:** ¿Cuál es el C8 de Montecristi? (Dom07 específico)
- **Pregunta arquitectónica:** ¿Puede DPE actuar como fuente canónica para 221 GADs? (escala nacional)

La segunda tiene alcance mayor. Si valida, la complejidad de observabilidad Dom07 para 221 GADs es O(1). Si no valida, la complejidad sigue siendo O(n). Resultado documentado en `ADR-015_Validacion_OBS-QNKC-02.md` — pendiente de cierre post-N4.

**Estado tras auditoría N4:** OBS-QNKC-02 pasará de "Registrada" a "Validada", "Parcialmente validada" o "No confirmada" — actualizando este índice y cerrando ADR-015.

---

## Corolarios Metodológicos Registrados

Consecuencias del sistema axiomático sobre el proceso de desarrollo — no sobre lo que QUIRA mide, sino sobre cómo los sprints trabajan bajo el marco axiomático.

### COR-QNKC-01 — Los sprints posteriores al congelamiento de un principio no diseñan estructura; calibran observables

**Estado:** Registrado (2026-06-01)  
**Derivado de:** H-QNKC-02 — las condiciones necesarias se modelan multiplicativamente  
**Enunciado:** Una vez que un principio Pxx está congelado, la estructura causal de su Layer 2 está determinada. Los sprints posteriores descubren los parámetros empíricos — variables observables, fuentes de datos, pesos, umbrales — pero no la forma.

**La distinción crítica:**

| Tipo de trabajo | Quién lo determina | Ejemplo Sprint 4 — Dom07 |
|----------------|-------------------|--------------------------|
| Estructura causal | Los axiomas (H-QNKC-01 + H-QNKC-02) → derivación de P01 | `C8 = C4 × C5a × C5b × C5c` — ya congelado |
| Parámetros empíricos | El sprint — observación en Montecristi | ¿Qué mide C5c? ¿Qué umbral activa ROJO? |

**Dom07 como primera prueba empírica del sistema axiomático:**  
Sprint 4 es la primera Layer 2 completa construida como derivación directa de los axiomas. Si la cadena C4 → C5a → C5b → C5c → C8 valida P01 en Dom07, el mismo patrón se proyecta sobre todos los sprints subsecuentes sin rediseñar la epistemología:

```
P01 → Dom07   (Sprint 4 — calibra C5a/C5b/C5c para LOTAIP)
P02 → Dom08   (Sprint 6 — calibra Incidencia_real para Participación)
P03 → Dom03   (Sprint 10 — calibra Corrección_aplicada para Seguimiento)
P04 → Dom09   (Sprint 11 — calibra Corrección_posterior para Rendición)
P05 → Obs.Long (post-M002 — calibra C9a/C9b antes de la serie temporal)
```

**Por qué COR-QNKC-01 no es un principio Pxx:**  
No destruye un falso equivalente institucional (H-QNKC-01). No modela una capacidad como condición necesaria (H-QNKC-02). Es una consecuencia procedimental del sistema axiomático — una regla sobre cómo los sprints trabajan bajo ese sistema, no sobre qué mide QUIRA.

---

### COR-QNKC-02 — El criterio real de cierre de un sprint es la obtención de un Dominio Epistemológicamente Cerrado

**Estado:** Registrado (2026-06-01)  
**Derivado de:** H-QNKC-01 + H-QNKC-02 + ADR-012 — la combinación de los axiomas con el protocolo N1→N5 define cuándo un sprint está verdaderamente cerrado  
**Enunciado:** Un sprint está concluido cuando su dominio alcanza estado **DEC (Dominio Epistemológicamente Cerrado)** — no cuando sus tareas técnicas se completan.

**Definición formal de DEC:**

Un dominio alcanza estado DEC cuando la cadena:

```
Norma → Pregunta → Observación → Verificación → Resultado
```

puede recorrerse de extremo a extremo sin huecos con datos reales — y cuando ese recorrido valida o falsea empíricamente los principios QNKC que gobiernan el dominio.

**Condiciones necesarias para DEC (todas deben satisfacerse simultáneamente):**

| Condición | Qué requiere | Lo que NO es suficiente |
|-----------|-------------|------------------------|
| 1. ADR-012 N1–N5 completos | Todos los pasos con datos reales — sin fallback | N1–N4 con proxies o estimados |
| 2. Principio P0N testado empíricamente | El principio gobernante del dominio tiene al menos un resultado observable que confirma o refuta su forma multiplicativa | El principio existe en governance pero no en datos |
| 3. OBS-QNKC aplicable testada | Si existe una OBS-QNKC activa en el dominio, tiene resultado: validada / parcialmente validada / no confirmada | La OBS existe registrada pero sin cierre empírico |
| 4. C10 calculado con dato real | La narrativa del Alcalde refleja un dato territorial verificable | C10 producido con datos de fallback o "pendiente" |

**Condiciones que NO son suficientes para DEC:**

```
El commit existe               → necesaria, no suficiente
La pantalla funciona           → necesaria, no suficiente
Neo4j load ejecutado           → necesaria, no suficiente
N5 (C10) producido             → necesaria pero no suficiente si usa fallback
Layer 2 desplegado             → necesaria, no suficiente
```

**La distinción crítica — lo que COR-QNKC-02 hace explícito:**

Un dominio puede ser técnicamente completo (pantalla funciona, Neo4j cargado, connector operativo) y epistemológicamente abierto: el indicador se calcula con datos proxy, el C8 usa fallback, el C10 dice "PENDIENTE". Ese dominio no es DEC.

DEC no es más exigente en lo técnico — es exigente en lo empírico: requiere que el dato real pase por la cadena completa y que los principios que gobiernan el dominio hayan sido confrontados con evidencia, no solo con estructura.

**Dom07 como primera prueba de COR-QNKC-02:**

Sprint 4 no cierra cuando `p07_transparencia.py` funciona. Sprint 4 cierra cuando:

1. N4 completo: auditoría real en `transparencia.dpe.gob.ec` para Montecristi — datos [Numeral × C5a × C5b × C5c] registrados
2. N5 completo: C10 calculado con `C8 = C4 × C5a × C5b × C5c` usando datos reales (no PENDIENTE)
3. ADR-015 cerrado: OBS-QNKC-02 declarada validada / parcialmente validada / no confirmada con evidencia
4. Tres hipótesis testadas simultáneamente:
   - **H-A:** P01 funciona operativamente — `C8 = C4 × C5a × C5b × C5c` calculable con datos reales
   - **H-B:** OBS-QNKC-01 es observable — ¿existen numerales donde C5a=1, C5b=1, C5c=0?
   - **H-C:** OBS-QNKC-02 escala nacionalmente — ¿puede DPE actuar como observador canónico?

Dom07 DEC = Dom07 técnico + Dom07 empírico + principios testados.

**Consecuencia sobre los sprints subsecuentes:**

Dom08, Dom09, Dom03 no son experimentos epistemológicos. Son **replicaciones del patrón DEC**. La forma es idéntica (ADR-012 N1→N5 + test de principios gobernantes). Solo los coeficientes empíricos varían. COR-QNKC-02 formaliza por qué Dom07 como primer DEC importa: establece el estándar de cierre para todos los sprints subsecuentes. Cuando Dom07 esté DEC, el framework habrá demostrado que H-QNKC-01 + H-QNKC-02 + P01 + OBS-QNKC-01 + OBS-QNKC-02 pueden producir conjuntamente un dominio operativo completo y verificado. Dom08–Dom12 heredan ese estándar.

**Por qué COR-QNKC-02 no es un principio Pxx:**  
No destruye un falso equivalente institucional (H-QNKC-01). No modela una capacidad institucional como condición necesaria (H-QNKC-02). Es una consecuencia del sistema axiomático sobre cómo los sprints se evalúan — una regla de proceso derivada de los axiomas, como COR-QNKC-01, no sobre lo que QUIRA mide.

---

## Tipos de Conocimiento QNKC

El framework produce cuatro tipos de conocimiento con ciclos de vida distintos:

| Tipo | Código | Función | Ciclo de vida | Ejemplo |
|------|--------|---------|--------------|---------|
| **Hipótesis Arquitectónica** | H-QNKC-NN | Axioma que determina la forma o el alcance del framework. No destruye un falso equivalente — establece la gramática desde la que los principios se derivan | Permanente — no se deroga; toda nueva hipótesis se añade a las existentes | H-QNKC-01, H-QNKC-02 |
| **Principio** | Pxx | Destruye un falso equivalente institucional demostrado con evidencia de sprint. Debe satisfacer simultáneamente H-QNKC-01 y H-QNKC-02 | Permanente — congelado cuando se formaliza. No se modifica; se enmienda con nuevo documento | P00, P01 |
| **Scheduled Principle** | Pxx (sprint asignado) | Falso equivalente identificado con sprint conocido que lo requiere. Existe como entrada en este índice, no como documento propio | Temporal — se convierte en Principio cuando su sprint lo materializa | P02, P03, P04, P05 |
| **Observación Arquitectónica** | OBS-QNKC-NN | Patrón recurrente que no requiere principio independiente — es refinación de un principio existente o requiere condiciones que aún no existen | Abierto — puede evolucionar a Principio Scheduled, cerrarse como implementado, o seguir registrado indefinidamente | OBS-QNKC-01 |
| **Corolario Metodológico** | COR-QNKC-NN | Consecuencia del sistema axiomático sobre cómo el framework crece y cómo se construyen sus implementaciones. No destruye un falso equivalente — formaliza una regla de proceso derivada de los axiomas | Permanente — se registra cuando la práctica de sprint confirma la regla derivada | COR-QNKC-01 (calibración) · COR-QNKC-02 (cierre DEC) |

**La diferencia crítica entre Scheduled y OBS-QNKC:** un Scheduled Principle tiene sprint asignado donde será necesario. Una OBS-QNKC no tiene sprint — aparece cuando el sistema la necesita, o cuando un sprint posterior revela que el patrón es más profundo de lo que parecía.

**Lo que no entra al framework:** intuiciones sin evidencia de sprint, analogías externas no demostradas en datos del sistema, principios que no destruyen un falso equivalente concreto. La prueba de H-QNKC-01 se aplica antes de registrar cualquier candidato: ¿existe riesgo observado — no abstracto — de confundir un proceso con su resultado?

---

## Convención de Nombrado

- `H-QNKC-NN`: Hipótesis arquitectónicas fundacionales — establecen la gramática del framework, no destruyen falsos equivalentes
- `P00`: Principios sobre la posición de una norma en la cadena C1-C9 (eje de capas)
- `P01+`: Principios sobre la lectura o consecuencia de artefactos (eje epistémico y causal)
- `OBS-QNKC-NN`: Observaciones arquitectónicas registradas — refinaciones epistemológicas dentro de principios existentes
- `COR-QNKC-NN`: Corolarios metodológicos — consecuencias del sistema axiomático sobre el proceso de desarrollo; no sobre el dominio observacional
- Numeración secuencial en orden de descubrimiento — no de importancia jerárquica
- Cada principio congelado tiene documento propio en `governance/framework/`
- Este índice es el registro canónico — los documentos propios son las especificaciones

**Prueba para cualquier candidato a principio:**  
Antes de crear P0N, responder: ¿qué proceso está siendo confundido con su resultado — o qué resultado está siendo confundido con su impacto? Si no hay una respuesta clara con evidencia de un sprint concreto, el patrón no es aún un principio — es una observación.

**Árbol estructural del framework:**

```
HIPÓTESIS FUNDACIONALES
├── H-QNKC-01  Proceso ≠ Resultado              (Congelada — eje categorial)
├── H-QNKC-02  Condiciones necesarias × (no +)  (Congelada — eje matemático)
└── H-QNKC-03  Verificación ≠ Atribución        (Anticipada — QUIRA Impact / P06)

PRINCIPIOS  (cada uno satisface H-QNKC-01 + H-QNKC-02 simultáneamente)
├── P00  Norma ≠ Cumplimiento              (Congelado — 2026-06-01)
├── P01  Documento ≠ Evidencia             (Congelado — 2026-06-01)
├── P02  Participación ≠ Influencia        (Scheduled — Sprint Dom08)
├── P03  Medición ≠ Acción                 (Scheduled — Sprint Dom03)
├── P04  Rendición ≠ Cambio                (Scheduled — Sprint Dom09)
├── P05  Resultado ≠ Impacto               (Scheduled — Sprint Obs. Longitudinal)
└── P06  Impacto ≠ Transformación sist.    (Anticipated — QUIRA Impact, sin fecha)

OBS-QNKC  (refinaciones epistemológicas — dentro de principios existentes)
├── OBS-01  Verificabilidad ≠ Comprensión           (Registrada — refinación de C5 dentro de P01)
└── OBS-02  Portal Regulatorio ≠ Portal Institucional como C5  (Registrada · ADR-015 abierto — validación N4 pendiente · O(n)→O(1) · N2 Dom07 v1.0.1)

COR-QNKC  (corolarios metodológicos — consecuencias de los axiomas sobre el proceso de desarrollo)
├── COR-01  Sprints posteriores calibran observables, no diseñan estructura  (Registrado — derivación de H-QNKC-02)
└── COR-02  Criterio de cierre de sprint = DEC (Dominio Epistemológicamente Cerrado)  (Registrado — N4 Dom07 es test simultáneo de P01 + OBS-01 + OBS-02)
```

Las dos hipótesis son la raíz. Cada Pxx es un nodo que implementa simultáneamente H-QNKC-01 (el falso equivalente que destruye) y H-QNKC-02 (la cadena multiplicativa que lo expresa). Un candidato que solo satisface una de las dos hipótesis no es un principio del framework — es un caso de uso o una regla de diseño.

---

## Estado Epistemológico para BETA-CORE

> **La arquitectura epistemológica de QUIRA está cerrada en el nivel de fundamentos para el ciclo BETA-CORE.**

**Qué significa "cerrada en el nivel de fundamentos":**  
Las dos hipótesis que generan todos los principios del framework están formalizadas:
- H-QNKC-01 (eje categorial): todo principio futuro deberá destruir una confusión proceso/resultado
- H-QNKC-02 (eje matemático): todo principio futuro deberá expresarse como cadena multiplicativa de condiciones necesarias

No significa que no aparecerán nuevos principios. Significa algo más fuerte: todo principio futuro deberá poder derivarse simultáneamente de H-QNKC-01 (falso equivalente que destruye) y H-QNKC-02 (cadena multiplicativa que lo expresa). Si no puede derivarse de ambas, no es un principio del framework — es una OBS-QNKC o una regla de implementación. Ese es el verdadero cierre.

**Estado de los principios para BETA-CORE:**  
P00 y P01 están formalizados. P02–P05 están programados con sprint conocido y con su estructura multiplicativa pre-formal derivada de H-QNKC-02. OBS-QNKC-01 está implementada en el sistema (estado `INCOMPRENSIBLE` en QTMP + Constitución de Lenguaje) antes de requerir formalización explícita. OBS-QNKC-02 registrada durante calibración Sprint 4 — Dom07: el portal regulatorio DPE (transparencia.dpe.gob.ec) es la fuente canónica de C5a/C5b para dominios LOTAIP; cambia dónde QUIRA verifica, no qué verifica ni con qué fórmula. Consecuencia para 221 GADs: verificación C5a/C5b centralizada en una sola fuente estructurada. No se requieren principios adicionales para cerrar MILESTONE_002.

El próximo principio que QUIRA va a necesitar es P02 — en el Sprint de Dom08 (Participación Ciudadana). Aparecerá exactamente cuando el sistema tenga que decidir qué cuenta como C9: si el acta de participación es suficiente, o si se requiere trazar que la participación modificó una decisión concreta de inversión. La estructura multiplicativa pre-formal ya está registrada: `participación_efectiva = Convocatoria × Deliberación × Incidencia_real`.

**Tagline — topología y álgebra:**

> *"QUIRA no verifica documentos. QUIRA verifica cadenas causales."*

Describe la topología: cadenas, no atributos aislados.

> *"QUIRA verifica cadenas causales compuestas por condiciones necesarias."*

Describe el álgebra: multiplicativa, no aditiva. La segunda es la especificación técnica de la primera. Para uso interno e institucional; la primera sigue siendo la frase canónica pública.

**Condición de reapertura:** si durante la construcción de algún dominio Tier A–C el sistema detecta una confusión proceso/resultado no cubierta por P00–P04, se registra como OBS-QNKC y se evalúa si cumple simultáneamente H-QNKC-01 (falso equivalente) y H-QNKC-02 (cadena multiplicativa). Si cumple ambas, se escala a Scheduled. Si solo cumple una, queda como OBS-QNKC.

**Horizonte post-BETA-CORE — H-QNKC-03:**  
H-QNKC-03 está registrada como anticipada. No se activa durante BETA-CORE porque ningún dominio de Montecristi requiere aún atribución causal contrafactual — solo verificación de cadenas. H-QNKC-03 se activará cuando P06 (Impacto ≠ Transformación sistémica) entre en formalización, lo que ocurrirá en QUIRA Impact. Ese momento marcará el paso del framework de un sistema de verificación causal a un sistema de atribución causal. Son epistemológicamente distintos y requieren axiomas distintos.

**Madurez epistemológica al cierre de Sprint 3:**

```
Nivel 0 — Catálogo         12 dominios listados
Nivel 1 — Framework        Capas C1–C9 causal
Nivel 2 — Teoría           P00–P06 como principios derivados
Nivel 3 — Sistema axiomático   H-QNKC-01 + H-QNKC-02 como raíces
                               Principios como derivaciones verificables
```

QNKC opera en Nivel 3. Los sprints que siguen no construyen la teoría — la instancian en Montecristi.

---

## Relación con otros documentos de gobernanza

| Documento | Relación |
|-----------|----------|
| `QLEP_CANONICO_MONTECRISTI_v1.0.md` | P00 está implícito en el Estado QLEP de Dom07 · base normativa de la que emergen los principios |
| `ADR-014_BETA_CORE_Roadmap.md` | La secuencia de sprints donde P02-P04 se materializarán |
| `COMPETENCIAS_QUIRA_MAP.md` | El marco constitucional que los principios protegen de confusión |
| `QNKC_P01_Dominios_Observacionales.md` | Especificación completa de P01 |
| `qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` | Primera implementación de P00 + P01 + OBS-QNKC-01 (estado INCOMPRENSIBLE) en YAML canónico |
| `constitucion_lenguaje_v1.md` | Implementación comunicacional de OBS-QNKC-01 — el plain language como respuesta al falso equivalente Verificabilidad ≠ Comprensión |

---

*Dylus Lab © 2026 · QUIRA Operaciones*  
*"QUIRA no verifica documentos. QUIRA verifica cadenas causales."*
