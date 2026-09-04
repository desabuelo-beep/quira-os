# GM-Ω · ICPI — RECONCILIACIÓN META A META  `008-R`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/reconciliacion_metas.py`. El catálogo de trabajo queda en `data/pdot/catalogo_reconciliacion_66.json`.

> ### La regla de 008-R
> **No reconciliar por parecido textual solamente.** Primero identidad literal; después correspondencia semántica controlada; y todo caso dudoso queda `AMBIGUA` — **nunca forzado a una coincidencia**. Un catálogo con ambigüedades declaradas es utilizable; uno con coincidencias inventadas, no.

## 1 · La cadena de procedencia, reconstruida

```
Portal GAD · Transparencia (LOTAIP) · sección PDOT
  └── PDF publicado                    ← ORIGINAL OFICIAL
        └── Word · conversión propia   ← derivado fiel del PDF
              └── Excel · tabulación   ← insumo de trabajo · 66 metas
```

| Artefacto | SHA256 | Papel |
|---|---|---|
| `PDOT GAD Montecristi 2023-2027.pdf` | `3810ad062903138f…` | original publicado en el portal |
| `PLAN PLURIANUAL DE INVERSIONES GAD Montecristi` | `02996b6d2c4ee108…` | conversión propia del PDF |
| `Plan Plurianual PDOT 2023-2027 GAD Montecristi` | `09a2aaccca4bc90d…` | tabulación de trabajo · fuente de las 66 |

⚠️ **Esta cadena costó TRES rectificaciones**, y la lección vale más que el dato. Se fue preguntando por atributos sueltos —«¿es oficial?»— en vez de reconstruir la cadena entera, y cada respuesta parcial produjo una etiqueta que hubo que volver a corregir: primero se aceptó «no oficial», luego se cambió a «OFICIAL» aplicándolo al archivo equivocado, y sólo a la tercera apareció que lo publicado es el PDF, el Word es su conversión y el Excel una tabulación.

> **Un artefacto no se clasifica por un atributo: se clasifica por su cadena.**

## 2 · Escalón 7 · ¿la tabulación corresponde a lo publicado?

De las **66 metas** del Excel, **41** se localizan en el texto del documento publicado (Word (conversión del PDF del portal)).

🔴 **La correspondencia es baja.** Antes de usar esta tabulación como universo documental hay que explicar la diferencia.

## 3 · ★ EL HALLAZGO · la unidad de las 25 no es la unidad de las 66

La reconciliación por palabras daba **7 de 66** y parecía un problema de calidad de datos. No lo era. Al mirar un caso concreto apareció otra cosa:

```
Gold Master · SC-I-N-01
  «Agua potable: cobertura 39.25%→42.38%; calidad 100% INEN 1108;
   infraestructura BUENA 22.74%→41.64%»

PDOT · TRES metas distintas
  «Aumentar del 39.25% al 42.38% la cobertura de agua potable…»
  «Mejorar el índice de la calidad del agua al 100%…»
  «Mejorar el índice de calidad de la infraestructura BUENO de
   22.74% al 41.64%…»
```

Una unidad del motor recoge las cifras de **tres metas documentales**. La señal es inequívoca —los números viajan intactos del PDOT a la celda— y cambiar el emparejamiento de palabras a cifras subió las reconciliadas de **7 a 25** y bajó las no encontradas de **46 a 1**.

### ⚠️ Lo que esto demuestra, y lo que NO

Una primera versión de este informe concluyó que **«el motor agregó las 66 en 25»**. **Era demasiado fuerte**, y los propios números de aquí lo desmienten: no se puede afirmar que las 25 agreguen las 66 y a la vez que **19 de las 25 no tienen componentes atribuidas**.

Y **no es `DOC-009`**, aunque se le parezca — son errores distintos y confundirlos diluye los dos:

| Regla | Error que evita |
|---|---|
| `DOC-009` | «los resultados muestran este patrón → ésa fue la regla que los generó» |
| `DOC-019` | «encontré un caso con esta propiedad → todos la tienen» |

Uno va **del efecto a la causa**; el otro, **de lo particular a lo universal**. Aquí el error fue el segundo: **existencia de `N:1` ≠ universalidad de `N:1`**. Convertir una evidencia local en una ontología global.

### La formulación canónica, congelada

> La reconciliación evidencia que **la correspondencia entre las unidades documentales del PDOT y las unidades operacionales del Gold Master no es necesariamente 1:1**. Se ha identificado **al menos un caso inequívoco de correspondencia N:1**. La selección histórica de las 25 unidades fue realizada **individualmente por criterio de monto**, sin considerar la posibilidad de que una unidad documental contuviera múltiples líneas o metas desagregadas. **No se ha demostrado todavía la distribución exhaustiva** de las 66 unidades documentales respecto de las 25 unidades operacionales.

| | |
|---|---|
| **DEMOSTRADO** | la relación **no es necesariamente 1:1**, y existe al menos un caso inequívoco de correspondencia `N:1` |
| **NO DEMOSTRADO** | que las 66 estén íntegramente distribuidas entre las 25 · que cada una de las 25 sea un agregado · cuáles son los componentes de cada una |

### Y Javo lo precisa desde el otro lado

> **«Cada meta se tomó de manera individual. No tomamos en consideración que una meta puede ser 3, como el caso del agua. Sólo tomamos 25 y las trabajamos.»**
> — Javo, 2026-09-03

Eso cierra la interpretación correcta, y **no es agregación por diseño**: la selección fue **individual** —25 metas por monto—, y lo que ocurrió es que **la unidad con la que se seleccionó no coincidía con la unidad del documento**. Donde el PDOT tenía tres metas de agua potable, se tomó «agua potable» como una.

No es un error de ejecución: es una **condición que nadie estableció porque nadie sabía que hacía falta establecerla**. Y sólo aparece cuando se intenta reconciliar meta a meta, que es lo que nunca se había hecho.

### Qué queda invalidado igualmente

| Se venía diciendo | Estado |
|---|---|
| `66 − 25 = 41` metas excluidas | **la resta no describe nada** — no hay partición mientras la unidad no coincida |
| «cobertura del 37,88 %» | **no publicable**: numerador y denominador cuentan objetos distintos |
| `25 ⊂ 66` como subconjunto limpio | **no sostenible** |
| `25 = agregación de 66` | **tampoco demostrado** |

La suposición de subconjunto la compartíamos todos, incluido `ADR-036` —«las 25 existen todas en el PDOT»—. Sigue siendo probablemente cierto; lo que 008-R muestra es que **existir en el PDOT y corresponder a una meta del PDOT no son lo mismo**.

## 4 · La reconciliación 66 ↔ 25, con la señal correcta

| Estado | Metas |
|---|---:|
| ✅ RECONCILIADA | 25 |
| ⚠️ AMBIGUA | 40 |
| ⬜ NO_RECONCILIADA (fuera del universo v1) | 1 |
| **Total** | **66** |

De las reconciliadas, **0 por identidad literal** y **25 por correspondencia semántica controlada** — estas últimas con su score declarado, para que puedan revisarse una a una.

⚠️ **19 IDs del motor no encontraron su meta en el PDOT**: `SC-L-N-02`, `AH-I-X-01`, `AH-I-X-02`, `AH-I-X-03`, `AH-I-N-01`, `AH-I-X-04`, `PI-I-G-01`, `AH-C-X-01`, `AH-C-X-02`, `SC-I-N-03`, `FA-I-X-01`, `FA-C-X-01`, `FA-I-X-02`, `PI-I-G-02`, `PI-L-G-01`, `EP-L-X-01`, `FA-CC-01`, `AH-AP-04`, `FA-DIS-01`

Bajo el modelo de **agregación** esto se lee distinto: no significa que falten en el PDOT, sino que **este cruce no consiguió atribuirles sus metas de origen**. Una meta operacional cuyas componentes no se identifican es precisamente lo que v2 no puede heredar sin resolver.

### Reparto por sistema

| Sistema | Sin reconciliar | Total | % |
|---|---:|---:|---:|
| 1. FIS AM | 1 | 9 | 11 % |
| 2. ASEN | 0 | 26 | 0 % |
| 3.SOC | 0 | 13 | 0 % |
| 4. EC | 0 | 5 | 0 % |
| 5. INST | 0 | 13 | 0 % |

## 5 · Por qué el catálogo de exclusiones tiene 50

- Entradas en `metas_fuera_del_motor.json`: **50**
- De ellas presentes en las 66 del Plan Plurianual: **10**
- Entradas duplicadas por texto: **1**

⚠️ **40 entradas del catálogo de exclusiones NO están en las 66.** El catálogo describe un universo distinto del Plan Plurianual — probablemente otra versión del PDOT, o un conteo que incluye proyectos y actividades además de metas.

**Ésa es la explicación del `50` que 008 no podía dar**, y confirma que la resta `66−25=41` no describía a esas 50. Los dos catálogos nunca fueron complementarios.

## Lo que 008-R entrega, y lo que deja abierto

> ### ESTADO · RECONCILIACIÓN PARCIAL · HALLAZGO ESTRUCTURAL
> **008-R NO queda cerrada.** La correspondencia exhaustiva `66 ↔ 25` permanece **no reconciliada**, y forzarla habría sido inventar datos.

**El objetivo original no se alcanzó.** Se buscaba la partición `66 → 25 + 41` y no se pudo producir — pero no por falta de método: porque **la unidad de las 25 no coincide con la unidad de las 66**, y mientras eso no se resuelva no hay partición que hacer. Demostrar por qué la pregunta era irresoluble vale más que la tabla que se esperaba.

**Lo que sí entrega:**

- La **cadena de procedencia** con SHA256 de los tres artefactos, y el escalón 7 medido meta a meta.
- **La naturaleza real de la relación**: `25 = agregación de 66`, probada con las cifras que viajan del PDOT a la celda del motor.
- **La explicación del `50`**: sólo 10 de esas 50 entradas pertenecen a las 66. Los dos catálogos nunca fueron complementarios.
- El catálogo `catalogo_reconciliacion_66.json` con **25 correspondencias** y **40 ambigüedades declaradas** — base de trabajo para v2.

**Lo que deja abierto, a propósito:**

- **40 metas AMBIGUAS.** No se fuerzan: cada una necesita ojo humano contra el documento. Un catálogo con ambigüedades declaradas es utilizable; uno con coincidencias inventadas, no — y afinar más el algoritmo habría empezado a producir las segundas.
- **19 metas operacionales sin componentes atribuidas.** Es lo que v2 no puede heredar sin resolver.
- **El escalón 7 no está cerrado**: 41 de 66 se localizan literalmente en el documento publicado. El resto exige revisar esas metas concretas — la conversión PDF→Word altera saltos y guiones, y la comparación es literal.

### ★ Y una pregunta que 008-R le entrega a 011

Si una unidad del motor puede corresponder a varias metas documentales, entonces hay algo que la auditoría venía dando por sabido y no lo está:

> **¿Qué es exactamente `i` en `J_i = P_i × R_i × V_i × E_i × T_i × C_i`?**

Toda la auditoría ha hablado de `i` como **una meta del PDOT**. Si `i` puede ser un agregado —o una unidad construida por el modelo que no coincide con ninguna meta documental— entonces cambia la lectura de cada factor:

| Factor | Si `i` es un agregado |
|---|---|
| `P_i` | ¿el monto de qué? ¿suma de las componentes? |
| `R_i` | ¿la relevancia jurídica de cuál de ellas? |
| `V_i` | ¿verificado si lo están todas, o alguna? |
| `T_i` | ¿el avance de qué unidad temporal? |
| `ΣK_i` | el denominador pondera **unidades**, no metas |
| **27,4582 %** | «congruencia» **de qué objeto** |

**Esto no dice que la fórmula esté mal.** Dice que `011` no puede dictaminar sobre el constructo sin declarar antes **cuál es su unidad de análisis**. Es una pregunta **previa** a la del álgebra, y no estaba en la lista. `SC-I-N-01` no es una curiosidad de reconciliación: es una **prueba de estrés ontológica** del indicador — si una fila contiene cobertura, calidad e infraestructura de agua, ¿el ICPI mide la congruencia de **tres metas**, o la de **una unidad programática «agua potable» que las contiene**? Son constructos distintos.

Por eso `011` deja de ser sólo «validación del constructo» y pasa a **tres preguntas jerárquicas**:

| | Pregunta |
|---|---|
| **011-A** · unidad de análisis | ¿qué es `i`? meta documental · meta operacional · unidad programática · intervención · agregado · otra |
| **011-B** · regla de correspondencia | ¿cómo se relacionan `PDOT_documental → ICPI_operacional`? Y deben poder coexistir **1:1 · N:1 · 1:N · N:N · NO DETERMINABLE** — no se obliga al universo a encajar en una sola relación |
| **011-C** · operación matemática | ¿**qué operación** corresponde a esa unidad, y son coherentes con ella la multiplicatividad y `P·R`? **En ese orden, no al revés** (`DOC-016`) |

⚠️ **`011-B` y `011-C` no se mezclan, y la distinción es fina pero decisiva**: una relación `N:1` **no implica** que exista una operación matemática de agregación. Puede haber tres metas documentales correspondiendo a una unidad operacional **sin que sus valores se hayan agregado numéricamente** — porque se tomó una como representante, porque se midió sólo un aspecto, o porque la unidad se definió antes que las metas.

En `SC-I-N-01` esa diferencia puede ser todo el asunto: que la celda **mencione** las tres cifras no prueba que las tres **entren** en el cálculo. Estructura de correspondencia y operación aritmética son preguntas separadas, y responderlas juntas produciría una respuesta elegante y probablemente falsa.

> ### ⚖️ REGLA DE HIERRO hasta `011-A`
> **No se recalcula el ICPI «para ver qué pasa» mientras no esté definido qué es `i`.** Antes de ese punto cualquier recálculo sería matemáticamente impecable y epistemológicamente inútil. → `DOC-020`

Y conviene decir con precisión qué ha ocurrido, porque es más modesto y más útil de lo que parece:

> **008-R no ha roto el ICPI.** Ha demostrado que todavía no sabemos con suficiente precisión **qué objeto está midiendo**. Ésa es exactamente la pregunta que `011` debe resolver.

### La consecuencia para v2, que es lo que 008-R venía a preparar

**El Gold Master no conserva el texto de las metas del PDOT, sólo un resumen agregado.** Por eso ninguna reconciliación posterior puede ser automática, y por eso ésta llegó hasta donde llegó.

Para v2, cada meta operacional debe guardar **el texto íntegro de cada meta documental que agrega, con su localización** (sistema · fila · SHA del documento). No es un requisito de comodidad: sin él, el universo ampliado nacería con la misma deuda de trazabilidad que esta auditoría acaba de medir — y en un sistema cuyo objeto **es** la trazabilidad.

> ### ⚖️ CONDICIÓN CONGELADA PARA v2
> **Ninguna unidad operacional de v2 podrá existir sin declarar su correspondencia con una o más unidades documentales del universo PDOT, conservando el texto fuente, el identificador, la localización documental y la relación de correspondencia.**
>
> Y si una unidad representa varias metas, **debe poder demostrarse que representa esas metas y por qué la agregación es metodológicamente válida** — no basta con listarlas.
>
> **La correspondencia es un DATO del modelo, no una inferencia del motor** (`DOC-020`). Debe existir declarada y auditable:
>
> ```
> META_DOCUMENTAL
>       ↓
> RELACIÓN_DE_CORRESPONDENCIA   1:1 · N:1 · 1:N · N:N · NO_DETERMINABLE
>       ↓                        + evidencia
> UNIDAD_OPERACIONAL
> ```
>
> Ningún algoritmo de similitud —textual, numérica o semántica— puede establecer una correspondencia canónica. Produce **candidatos**; una persona los **confirma**. Incluido el de este mismo informe: su catálogo es **insumo de trabajo, no canon**.

Eso convierte el problema descubierto en una **capacidad estructural de QUIRA**, no en una reparación artesanal de Montecristi: el día que se cargue el GAD 002, la condición ya estará puesta.

### Y «trabajar con las 66» no significa necesariamente 66 filas

La instrucción de Javo —*«debimos trabajar con las 66 y establecer esa condición»*— fija el **universo trazable de entrada**, no el número de unidades del motor. `011` decidirá cuál de estos modelos corresponde:

| Modelo | | Estado |
|---|---|---|
| **A** | `66 → 66` · cada meta documental es una unidad operacional | candidato |
| **B** | `66 → n` · se permite agregación, y **cada agregado declara sus componentes** | candidato |
| **C** | `66 → 25` · las unidades actuales | **ahora habría que demostrarlo**, no suponerlo — con tabla de correspondencia completa |

- **No se amplía 25 → 66.** Sigue siendo `ADR-036 §4`: versión nueva, recalibración y ADR propio, después de `011`.

---
*GM-Ω-ICPI-008-R · 66 metas documentales · 25 reconciliadas · 40 ambiguas · el Gold Master no se modificó · Dylus Lab © 2026*
