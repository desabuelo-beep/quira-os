---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 9, 13]
  type: ARQUITECTONICA
---

# DESCUBRIMIENTO NORMATIVO · uso del Motor de Descubrimiento (ADR-031) para vacíos normativos

**2026-07-30 · propuesta de Javo, precisada por la asesoría · instrumentación de un concepto existente**

> **Pregunta de Javo:** *"¿puede QUIRA reconocer cuándo posiblemente se configure una SAT? Creo que
> las reglas dicen por algún lado que no más motores, pero creo esta propuesta es potente."*

---

## ⛔ 0 · CORRECCIÓN MAYOR (Javo · 2026-07-30): NO es un motor nuevo

> **Javo:** *"debes revisar la documentación, ya que no creo que tenemos más de un motor —claro, el
> Gold Master es del cálculo, pero existen creo 5 en total. Si estoy alucinando corríjame."*

**No alucinaba. Yo estaba incompleto.** `ADR-031 §3` define **MCIP — los 5 motores TIPADOS**, y el
cuarto es exactamente lo que este documento proponía crear:

| Motor | Lee de | Responde | Naturaleza |
|---|---|---|---|
| **Matemático** | Gold Master (MCM) | los NÚMEROS — la verdad | runtime · **supremo** |
| **Grafos** | Neo4j | las RELACIONES | runtime |
| **Causal** | econometría | ¿qué CAUSÓ este resultado? | lab |
| **★ Descubrimiento** | K-Means · HDBSCAN · UMAP | **PATRONES ocultos / anomalías** | **laboratorio, NO runtime** |
| **Prospectivo** | simulación | ¿qué pasa SI…? | lab → runtime |

**No se crea nada. Se declara un uso del Motor de Descubrimiento ya existente.** Este documento pasa
de *"motor nuevo"* a **extensión de ADR-031** — que es lo que la Regla 7 exige.

### ADR-031 ya había zanjado el debate de hoy

Literal, en el mismo ADR:

> *"**Corrección al asesor: el SAT no nace en un 'motor analítico' de QUIRA; nace en el Excel.**"*
> *"El mapeo SAT→dominio YA existe (`SAT_Catalogo`) — QUIRA **lee y rutea, nunca los genera** (Regla 1)."*

Toda la discusión de esta sesión sobre *"¿puede la IA crear SAT?"* **ya estaba resuelta en el canon**.
Las tres reglas inquebrantables que la asesoría propuso hoy no son nuevas: son la reformulación de algo
decidido en ADR-031.

### Dos restricciones de ADR-031 que este documento NO tenía

| Restricción | Qué implica |
|---|---|
| **"laboratorio, NO runtime"** | el Motor de Descubrimiento **no corre en producción**. Sus hallazgos *vuelven al MCD*; no viven en el sistema |
| **Secuencia obligatoria** | *"entra **cuando el grafo ya genera la pregunta** — no antes. Primero el grafo; de él emergen las preguntas naturales, no al revés"* |

**La segunda es la que faltaba y es decisiva.** El flujo que propuse arrancaba en los datos crudos.
ADR-031 exige que arranque **en el grafo**: primero Neo4j revela la relación, y de ahí emerge la
pregunta que el clustering responde. Detectar patrones sin pregunta previa es *data-dredging*, y
produciría exactamente los "falsos descubrimientos" que R-H acaba de prohibir.

### Qué sobrevive de esta propuesta

| Aporte | Estado |
|---|---|
| Aplicar el Motor de Descubrimiento a **vacíos normativos** (no solo a clusters de datos) | ✅ **es la contribución real de Javo** |
| El expediente candidato `C10-{año}-{n}` con `Corpus→CNO→RO→SAT` | ✅ formaliza el retorno al MCD que ADR-031 pide |
| Las tres reglas inquebrantables | ✅ ya implícitas en ADR-031 · quedan explícitas |
| *"Motor C10"* como componente nuevo | ❌ **es el Motor de Descubrimiento** |

> **Séptima vez en esta sesión que el canon ya tenía la respuesta.** Y el error fue de método: consulté
> el Inventario de Conceptos (que llevó a C10) pero **no ADR-031**, que estaba citado en la primera línea
> del BOOT que yo mismo estaba editando.
>
> **Regla que se extiende (2026-07-30):** *antes de declarar un componente, se consulta el Inventario de
> Conceptos **y los ADR**.* El Inventario cubre **conceptos**; los ADR cubren **arquitectura**. Buscar solo
> en uno deja el otro ciego — que es exactamente lo que pasó aquí.

---

## 1 · Las dos verificaciones originales *(se conservan — siguen siendo válidas)*

### ¿Viola la prohibición de "no más motores"?

**No.** `CLAUDE.md` prohíbe algo más preciso:

> *"construir un **motor de cálculo paralelo** al Gold Master"*

El Motor de Descubrimiento **no calcula**: detecta patrones y ensambla expedientes. No produce métricas, no toca
`H12!B33`, no compite con el Gold Master. Y existe **precedente aprobado**: `PCD-MN01_Motor_Narrativo`
declara ser *"capacidad TRANSVERSAL de QUIRA —no un dominio, no dispara el Protocolo de Expansión
Ontológica—"*. Ya hay un motor no-de-cálculo cerrado con PCD.

### ¿Es un concepto nuevo? — **NO. Ya existe desde mayo-2026**

`QUIRA_CAUSAL_MODEL_v1.0.md` §XIV, **C10 · Reflexión Institucional**:

```
Trigger: hallazgo que revela una limitación del modelo (no del territorio)
Input:   C9 confirmado + paradoja o anomalía metodológica documentada
Output:  nueva hipótesis sobre una variable no medida
         O nueva capa en la cadena causal existente
         O corrección de un supuesto previo
Destino: Beta backlog (si requiere construcción)
```

**Eso es literalmente lo que los asesores proponen.** Trigger = detección · Output = conocimiento
candidato · Destino = backlog, nunca auto-aprobación.

> **Sexta vez en esta sesión que el canon contenía la respuesta.** El concepto 7 del Inventario
> (**C10 · Metacognición institucional**) lleva en estado `parcial` desde mayo. Lo que falta no es
> inventar un motor: es **instrumentarlo**.

**Por eso NO se llama MDN, MDCN ni SDNA: es el Motor de Descubrimiento** (ADR-031 §3), operando el
concepto **C10** (Inventario 7) — *deriva, no redefinas* (regla propia de `INVENTARIO-CONCEPTOS-001`; se citaba «Regla 6», hoy renumerada — corregido 2026-08-26).

## 2 · Qué hace, en una frase

> **Detecta hechos que la arquitectura normativa vigente no explica, y ensambla un expediente
> candidato completo — `Corpus → CNO → RO → SAT` — en estado NO VIGENTE, para decisión humana.**

**La IA no decreta. La IA propone un expediente.** Esa distinción es toda la arquitectura.

## 2 · Flujo

> ⚠️ **Flujo CORREGIDO por ADR-031.** La primera versión arrancaba en los datos crudos. El ADR exige
> arrancar **en el grafo**: *"primero el grafo; de él emergen las preguntas naturales, no al revés"*.
> Detectar patrones sin pregunta previa es *data-dredging* — produciría los "falsos descubrimientos"
> que R-H prohíbe.

```
     NEO4J (Motor de Grafos · runtime)
                 │
                 ▼
     el grafo revela una RELACIÓN inesperada
                 │
                 ▼
        ¿emerge una pregunta natural?          ← condición de entrada (ADR-031)
                 │
        ┌────────┴────────┐
       NO                SÍ
        │                 │
   no se activa    MOTOR DE DESCUBRIMIENTO
                   (K-Means · HDBSCAN · UMAP)
                   ⚠️ LABORATORIO, no runtime
                          │
                          ▼
              ¿lo explica alguna CNO+RO
                    ya existente?
                          │
              ┌───────────┴───────────┐
             SÍ                      NO
              │                       │
        no hace nada          expediente candidato
                             C10-{año}-{n} · NO VIGENTE
                                      │
                                      ▼
                          el hallazgo VUELVE AL MCD
                            (ADR-031: no vive en el
                             sistema, retorna al modelo)
                                      │
                                      ▼
                             REVISIÓN HUMANA (Javo)
                                      │
                                      ▼
                            sella en el Gold Master
```

**Un solo motor, ya existente.** La asesoría propuso separar `MDN` (detectar) de `MDCN` (construir
expediente): son dos etapas del mismo proceso, y **ambas caen dentro del Motor de Descubrimiento de
ADR-031**. Duplicar componentes es inflación (Regla 7).

## 3 · Las tres reglas inquebrantables

| # | Regla | Fundamento |
|---|---|---|
| **1** | **El Gold Master nunca auto-crea una SAT.** Un registro entra solo por aprobación humana explícita. | Regla 1 · el Excel es el estado |
| **2** | **La Configuración Normativa es la unidad primaria, no la SAT.** Antes de proponer una SAT se evalúa si el patrón se explica con una `CNO`+`RO` existentes. | Regla 7 · evita SAT innecesarias |
| **3** | **Un candidato en `NO VIGENTE` no altera el ICPI.** No suma ni resta hasta ser sellado. | `H12!B33` inmutable |

> **Por qué la regla 1 es innegociable:** si una IA pudiera crear SAT automáticamente, el sistema
> dejaría de ser auditable. Sería *"permitir que un compilador modifique el estándar del lenguaje
> mientras compila"* (asesoría). La autoridad normativa permanece bajo control humano.

## 4 · El expediente candidato

**Identificador: `C10-{año}-{secuencia}`** — no `SAT-X`, porque **todavía no se sabe si será una SAT**.
Puede terminar siendo una CNO nueva, una modificación de RO, una excepción metodológica, una nota
interpretativa **o** una SAT.

```yaml
id: C10-2027-001
estado: NO_VIGENTE
patron_observado: "Presupuesto prorrogado en año electoral"
hechos:
  - "S1 CNE: calendario electoral activo para febrero 2027"
  - "S5 eSIGEF: Presupuesto_Inicial_2027 == Codificado_2026"
  - "S7 LOTAIP: no consta ordenanza de presupuesto 2027"
cobertura_silos: [S1, S2, S5]
corpus_relacionado: "COPFP Art. 107 (presupuesto prorrogado)"   # ← SHA verificado, Regla 3
cno_candidata: null          # ¿existe ya? el motor consulta la BRN antes de proponer
ro_candidata: "RO-II-004 (límite de compromisos plurianuales)"
sat_candidata: "¿necesaria? — evaluar primero si RO existente basta"
razonamiento: "..."
requiere: [validacion_humana]
```

### ⛔ Lo que el expediente NO lleva

La asesoría incluyó un campo **`confianza: 0.97`**. **Se rechaza.** Ese número no tiene origen
verificable — sería inventar precisión, exactamente el error que este sistema combate (OBS-021 ·
OBS-023). Si algún día hay un score, deberá derivarse de una medición declarada, no de una intuición
del modelo.

## 5 · Por qué esto vale — dos usos inmediatos

### a) Habría evitado el error de SAT-IX

Hoy se creó `SAT-IX` **escribiéndola directamente en el Excel**, saltándose `CNO → RO`. Javo lo
detectó preguntando *"¿por las SAT no debería pasar la BRN?"*. Con este flujo habría sido:

```
162 demandas vinculantes sin correlato
        ↓
¿lo explica alguna CNO+RO existente? → CNO-VIII-005 sí existe (COOTAD 238)
        ↓
expediente C10-2026-001 con RO-VIII-003 como productora
        ↓
revisión → sello
```

**El error no habría ocurrido.** Es el mismo principio del test de regresión: convertir el hallazgo
en verificación permanente.

### b) Convierte la deuda SAT↔BRN en capacidad permanente

`check_sat_brn.py` hoy reporta la deuda una vez. El Motor de Descubrimiento la vigila de forma continua:

| SAT | Corpus | CNO | RO | Evidencia | Estado |
|---|:---:|:---:|:---:|:---:|---|
| SAT-0 | ✓ | ✓ | ✓ | ✓ | completa |
| **SAT-I** | ✓ | ✓ | ✗ | **✗** | deuda **estructural + epistemológica** |
| SAT-IX | ✓ | ✓ | ✓ | ✓ | completa |

## 6 · Lo que se descarta de la propuesta

| Propuesta | Veredicto |
|---|---|
| *"Motor de SAT Emergentes"* | ❌ el producto no son SAT: es **conocimiento candidato** |
| `MDN` + `MDCN` como dos componentes | ❌ dos etapas de un proceso — duplicar es inflación (R.7) |
| Nombres `MDCN` · `SDNA` · `CNC` · `OBS-NORM` | ❌ **seis siglas para una cosa.** El concepto ya se llama **C10** |
| Campo `confianza: 0.97` | ❌ precisión inventada, sin origen verificable |
| *"INSERT en tabla H24_SAT"* | ❌ `H24` es la hoja de **SAT-IV**; el catálogo es `SAT_Catalogo` |

> **La proliferación de siglas es el riesgo real de esta propuesta.** El Mapa de Gobernanza
> Metodológica nació hace dos días justamente para evitarla. Un concepto declarado en mayo no
> necesita cuatro nombres nuevos en julio.

## 6-bis · Revisión final de la asesoría (2026-07-31) — converge, sin desvarío

El colega llegó **por su cuenta** a las mismas conclusiones que la verificación contra el canon:

| Su conclusión | Estado |
|---|---|
| *"No debe implementarse como un nuevo motor — ADR-031 ya define el Motor de Descubrimiento"* | ✅ coincide |
| *"Lo correcto sería especializar el motor existente"* | ✅ coincide |
| *"No hacía falta inventar un Motor C10; C10 ya existía, faltaba operacionalizarlo"* | ✅ coincide |
| *"Lo nuevo no es el motor: es el TIPO DE PREGUNTA que puede responder"* | ✅ **la formulación más precisa de todas** |
| Su diagrama arranca en **Motor Grafos** antes del Descubrimiento | ✅ respeta la secuencia de ADR-031 |

> **Su mejor frase, y vale conservarla:** *"No cambia el motor. **Cambia el tipo de pregunta que el
> motor puede responder.**"* Y la consecuencia: QUIRA pasa de responder *"¿se incumplió una regla
> existente?"* a *"**¿existe un fenómeno recurrente para el cual todavía no existe una regla?**"* —
> aprendizaje de gobernanza, no aprendizaje automático.

### La única propuesta nueva — y por qué NO entra

Propone llamar **`CNC` · Configuración Normativa Candidata** al expediente, en vez de *"SAT candidata"*,
porque puede terminar siendo SAT, CNO, RO o nota metodológica.

**El razonamiento es correcto y ya está incorporado** (§4): el identificador es `C10-{año}-{n}`
precisamente porque *"todavía no se sabe si será una SAT"*. **La sigla nueva no añade capacidad, no
elimina ambigüedad y no reduce complejidad** — falla las tres condiciones de la Regla 7.

Y hay una razón adicional: ayer se descartaron **seis nombres** para esta misma cosa (`MDCN`, `MDN`,
`SDNA`, `CNC`, `OBS-NORM`, *"Motor de SAT Emergentes"*). `C10-{año}-{n}` ya comunica lo mismo **sin
sigla nueva**, y deriva de un concepto que existe desde mayo.

## 7 · Estado y condición de arranque

**No se construye todavía.** El motor ya está declarado en ADR-031; lo que queda pendiente es *este uso*,
**bloqueado por R-E**: el esfuerzo
disponible está comprometido en cerrar Montecristi. Construirlo antes sería abrir un frente nuevo
con el molde a medio hacer.

| Precondición | Estado |
|---|---|
| d08 Participación cerrado con PCD | ⏳ |
| Deuda SAT↔BRN estructural saldada | ⏳ 60% |
| d06 SIGAD construido (Fase A) | ⏳ |

**Cuando esas tres se cumplan**, este uso tiene fundamento, datos y reglas para operar. Antes,
no: detectaría "vacíos" que en realidad son deudas nuestras, no del marco normativo.

---
*Dylus Lab © 2026 · NO es un motor nuevo: extiende el **Motor de Descubrimiento** (ADR-031 §3, 4º de los 5 del MCIP)
y opera el concepto 7 del Inventario (C10), declarado en mayo-2026.*
