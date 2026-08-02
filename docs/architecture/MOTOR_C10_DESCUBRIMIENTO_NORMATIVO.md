---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 9, 13]
  type: ARQUITECTONICA
---

# MOTOR C10 · Descubrimiento Normativo Asistido

**2026-07-30 · propuesta de Javo, precisada por la asesoría · instrumentación de un concepto existente**

> **Pregunta de Javo:** *"¿puede QUIRA reconocer cuándo posiblemente se configure una SAT? Creo que
> las reglas dicen por algún lado que no más motores, pero creo esta propuesta es potente."*

---

## 0 · Las dos verificaciones que había que hacer antes

### ¿Viola la prohibición de "no más motores"?

**No.** `CLAUDE.md` prohíbe algo más preciso:

> *"construir un **motor de cálculo paralelo** al Gold Master"*

El Motor C10 **no calcula**: detecta patrones y ensambla expedientes. No produce métricas, no toca
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

**Por eso NO se llama MDN, MDCN ni SDNA. Se llama Motor C10** — *deriva, no redefinas* (Regla 6).

## 1 · Qué hace, en una frase

> **Detecta hechos que la arquitectura normativa vigente no explica, y ensambla un expediente
> candidato completo — `Corpus → CNO → RO → SAT` — en estado NO VIGENTE, para decisión humana.**

**La IA no decreta. La IA propone un expediente.** Esa distinción es toda la arquitectura.

## 2 · Flujo

```
        DATOS (silos S1..S9 · corpus · calendario CNE)
                        │
                        ▼
              ¿patrón no habitual?
                        │
            ┌───────────┴───────────┐
           NO                      SÍ
            │                       │
        flujo normal        ¿lo explica alguna
                            combinación CNO+RO
                            ya existente?
                                    │
                        ┌───────────┴───────────┐
                       SÍ                      NO
                        │                       │
                  no hace nada          expediente candidato
                                       (Corpus·CNO·RO·SAT)
                                                │
                                                ▼
                                      estado: NO VIGENTE
                                                │
                                                ▼
                                       REVISIÓN HUMANA (Javo)
                                                │
                                                ▼
                                     sella en el Gold Master
```

**Las dos preguntas son una sola cadena, no dos motores.** La asesoría propuso separar `MDN` (detectar)
de `MDCN` (construir expediente). **Se rechaza como componentes distintos**: son dos etapas del mismo
proceso, y duplicar el componente es inflación (Regla 7). Un motor, dos etapas.

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
detectó preguntando *"¿por las SAT no debería pasar la BRN?"*. Con el Motor C10 el flujo habría sido:

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

`check_sat_brn.py` hoy reporta la deuda una vez. El Motor C10 la vigila de forma continua:

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

## 7 · Estado y condición de arranque

**No se construye todavía.** Queda declarado en el canon y **bloqueado por R-E**: el esfuerzo
disponible está comprometido en cerrar Montecristi. Construirlo antes sería abrir un frente nuevo
con el molde a medio hacer.

| Precondición | Estado |
|---|---|
| d08 Participación cerrado con PCD | ⏳ |
| Deuda SAT↔BRN estructural saldada | ⏳ 60% |
| d06 SIGAD construido (Fase A) | ⏳ |

**Cuando esas tres se cumplan**, el Motor C10 tiene fundamento, datos y reglas para operar. Antes,
no: detectaría "vacíos" que en realidad son deudas nuestras, no del marco normativo.

---
*Motor C10 · Dylus Lab © 2026 · instrumenta el concepto 7 del Inventario, declarado en mayo-2026.*
