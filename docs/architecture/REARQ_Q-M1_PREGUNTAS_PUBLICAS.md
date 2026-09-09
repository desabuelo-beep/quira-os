# REARQ · `Q-M1` — LAS PREGUNTAS PÚBLICAS

**DERIVADO — no editar a mano.** Lo regenera `scripts/rearq/preguntas_publicas.py` leyendo el contrato índice→dominio, que a su vez deriva de la Constitución Ontológica.

> ### La prueba mental que ordena esta etapa
> **Si mañana borráramos mentalmente los doce índices históricos de QUIRA, ¿qué preguntas fundamentales sobre la gestión pública seguiríamos necesitando responder?**

No significa borrarlos: significa **suspender su autoridad epistemológica durante el diseño**. Después se hace el cruce — y ahí los índices **se ganan su residencia**, en vez de que `Q-M1` tenga que justificar por qué siguen existiendo.

⚠️ **Las preguntas no se inventan aquí.** Se derivan del corpus, la doctrina y la arquitectura declarada. Escribir en un script las preguntas que el canon no tiene sería **escribir el canon desde un script** — lo contrario de cómo QUIRA construye.

## ★ El primer resultado · un MAPA DE MADUREZ, no un inventario de carencias

### 📜 CORRECCIÓN · la `v1` confundió «no trabajado» con «no existe»

La primera versión publicó **«11 de 13 dominios no tienen pregunta rectora»** como si fuera una carencia de la ontología. Javo lo corrigió:

> *«Los dominios no están completos todos, hemos estado trabajando uno por uno […] Los demás no se ha empezado su trabajo.»*

⚠️ **Es el mismo error del `71 %` → `62 %`, ahora a nivel de dominio.** La formulación correcta:

> En el estado actual de curación del corpus, sólo se dispone de preguntas rectoras formalmente declaradas para los dominios que han alcanzado el nivel de curación correspondiente. **Los dominios aún no trabajados no pueden clasificarse como carentes de pregunta.**

### Las cinco dimensiones, y por qué no basta una

| Dimensión | Qué mide |
|---|---|
| **trabajo** | qué se ha hecho realmente |
| **curacion** | qué nivel formal alcanzó el proceso |
| **documental** | qué está registrado en el canon |
| **decision** | qué ha sido aprobado |
| **implementacion** | qué está efectivizado en el producto |

> ### 📜 La regla que `PCD-D06` obligó a escribir
>
> `PCD-D06` está **CERRADO** y su dominio no tiene silo de entrada, no calcula `ICM` y su alerta sigue apagada un mes después (`sat_evaluator.py:297`). Luego:
>
> **Un `PCD` cerrado certifica CONFORMIDAD de lo que existe, no SUFICIENCIA de lo que debería existir.**
>
> Es lo mismo que QUIRA hace con un municipio: no dice que esté bien, dice que lo que hay es trazable y que **lo que falta está declarado**. Por eso `PCD` presente **no** puede traducirse a «dominio curado», y por eso cada dimensión se calcula por separado.

### El mapa dimensional, derivado del disco

⚠️ Cada celda trae **su propia prueba**. Ninguna dimensión se infiere de otra, y donde no hay evidencia se dice `NO DETERMINABLE` — que es el tercer estado, no un relleno.

| Dominio | trabajo | curación | documental | decisión | implementación |
|---|---|---|---|---|---|
| `d01` Planificación Estratég | DEMOSTRADO | NO DETERMINABLE | PCD PRESENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d02` Presupuesto y Financia | DEMOSTRADO | NO DETERMINABLE | PCD PRESENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d03` Gobernanza del Mandato | DEMOSTRADO | NO DETERMINABLE | PCD PRESENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d04` Alertas Institucionale | NO DETERMINABLE | NO COMPLETADA | PCD AUSENTE | APROBADA · declarada | EFECTIVIZADA · declarada |
| `d05` Holding e Integración  | NO DETERMINABLE | NO COMPLETADA | PCD AUSENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d06` Salud Institucional | NO INICIADO · declarado | CERRADO con hueco declarado — silo S6 abierto | PCD PRESENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d07` Transparencia | DEMOSTRADO | EN CURACIÓN | PCD PRESENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d08` Participación Ciudadan | DEMOSTRADO | NO COMPLETADA | PCD AUSENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d09` Rendición de Cuentas | DEMOSTRADO | NO DETERMINABLE | PCD PRESENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d10` Cobertura de Servicios | NO DETERMINABLE | NO COMPLETADA | PCD AUSENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d11` Desarrollo Económico T | NO DETERMINABLE | NO COMPLETADA | PCD AUSENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d12` Inclusión, Equidad y G | NO DETERMINABLE | NO COMPLETADA | PCD AUSENTE | NO DETERMINABLE | NO DETERMINABLE |
| `d13` Sostenibilidad y Resil | NO DETERMINABLE | NO COMPLETADA | PCD AUSENTE | NO DETERMINABLE | NO DETERMINABLE |

**Pruebas de las celdas que no son `NO DETERMINABLE`:**

| Dominio | Dimensión | Estado | Prueba |
|---|---|---|---|
| `d01` | trabajo | DEMOSTRADO | existe `app/agents/d01/` — código escrito |
| `d01` | documental | PCD PRESENTE | `PCD-D01_Planificacion.md` · `type: NORMATIVA` |
| `d02` | trabajo | DEMOSTRADO | existe `app/agents/d02/` — código escrito |
| `d02` | documental | PCD PRESENTE | `PCD-D02_Presupuesto_Financiamiento.md` · `type: NORMATIVA` |
| `d03` | trabajo | DEMOSTRADO | existe `app/agents/d03/` — código escrito |
| `d03` | documental | PCD PRESENTE | `PCD-D03_Gobernanza_Mandato.md` · `type: NORMATIVA` |
| `d04` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d04` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |
| `d04` | decision | APROBADA · declarada | la dirección declara aprobada la baja del dominio SAT |
| `d04` | implementacion | EFECTIVIZADA · declarada | la dirección declara que salió del frontend |
| `d05` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d05` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |
| `d06` | trabajo | NO INICIADO · declarado | la dirección lo señala no iniciado — ⚠️ y existe un `PCD-D06` **cerrado** en disco |
| `d06` | curacion | CERRADO con hueco declarado — silo S6 abierto | declarado por `PCD-D06_Salud_Institucional.md` |
| `d06` | documental | PCD PRESENTE | `PCD-D06_Salud_Institucional.md` · `type: EXPEDIENTE` |
| `d07` | trabajo | DEMOSTRADO | existe `app/agents/d07/` — código escrito |
| `d07` | curacion | EN CURACIÓN | `BOOT` lo declara en curación |
| `d07` | documental | PCD PRESENTE | `PCD-D07_Transparencia.md` · `type: NORMATIVA` |
| `d08` | trabajo | DEMOSTRADO | existe `app/agents/d08/` — código escrito |
| `d08` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d08` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |
| `d09` | trabajo | DEMOSTRADO | existe `app/agents/d09/` — código escrito |
| `d09` | documental | PCD PRESENTE | `PCD-D09_Rendicion_Cuentas.md` · `type: NORMATIVA` |
| `d10` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d10` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |
| `d11` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d11` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |
| `d12` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d12` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |
| `d13` | curacion | NO COMPLETADA | no hay `PCD` que acredite el cierre formal — ⚠️ no equivale a «no trabajado» |
| `d13` | documental | PCD AUSENTE | no hay expediente en `docs/pcd/` |

> ### Lo que esto cambia
>
> No es «`2/13` con pregunta y `11/13` sin ella». Es **un estado de curación heterogéneo sobre un universo ontológico todavía parcialmente observado** — y eso es esperable: la Rearquitectura se hace **mientras se termina de construir el conocimiento del sistema**.

⚠️ **No es una debilidad: es lo que permite hacer `REARQ` bien.** La cadena correcta es `lo trabajado → evidencia disponible → lo no trabajado → incertidumbre explícita → siguiente dominio`. Nunca `lo que todavía no vimos → vacío → defecto`.

## ★ Tres discrepancias entre el canon y lo que la dirección declara

⚠️ **Se registran; no se resuelven aquí.** Resolver una discrepancia entre el canon y la memoria del autor exige la fuente, no el criterio de un script.

### ★ Un solo estado no alcanza · hacen falta CINCO dimensiones

Las discrepancias no eran contradicciones: eran **dimensiones distintas colapsadas en una sola columna**.

| Dimensión | Qué mide |
|---|---|
| **trabajo** | qué se ha hecho realmente |
| **curación** | qué nivel formal alcanzó (`PCD`) |
| **documental** | qué está formalmente registrado en el canon |
| **decisión** | qué ha sido aprobado |
| **implementación** | qué está efectivizado en el producto |

> **Usar la existencia de un `PCD` como sustituto de la realidad del proceso** fue el error de la versión anterior. Trabajo realizado ≠ `PCD` cerrado ≠ implementado.

### Los tres casos, resueltos por dimensión

| | `d04` Alertas | `d06` Salud Inst. | `d08` Participación |
|---|---|---|---|
| **trabajo** | — | 🔴 no iniciado · **declarado** | ✅ **DEMOSTRADO** — existe `app/agents/d08/` |
| **curación** | — | `CERRADO con hueco declarado — silo S6 abierto` | ❌ sin `PCD-D08` |
| **documental** | 🔴 **sigue en la Constitución** (4 lugares) | `PCD` presente · `type: EXPEDIENTE` | `BOOT`: `ENTRABLE` |
| **decisión** | ✅ aprobada · **declarada** — eliminarlo | — | — |
| **implementación** | ✅ efectivizada · **declarada** | 🟡 parcial — `SAT-I` apagada | — |

> ⚠️ `d08` **dejó de ser `NO DETERMINABLE`.** La existencia de `app/agents/d08/` es evidencia **material** de trabajo: código que alguien escribió. Lo que `BOOT` dice —`ENTRABLE`— mide otra cosa, y en este punto está **desactualizado**. La discrepancia se resolvió por evidencia, no por criterio.

Y así los tres dejan de ser «discrepancias» y pasan a ser **estados precisos**:

| # | Caso | Lectura correcta |
|---|---|---|
| 1 | **¿12 o 13 dominios?** | **No es binario.** El **producto** tiene hoy **12 dominios visibles**; el **canon** conserva **13**. `d04` fue eliminado por decisión aprobada y efectivizada — lo pendiente **no es decidirlo, es propagarlo al canon** |
| 2 | **`d08` Participación** | ✅ **trabajado**. La ausencia de `PCD` cerrado **no autoriza** a clasificarlo como no trabajado: mide la **formalización**, no el trabajo |
| 3 | **`d06` Salud Institucional** | ✅ **resuelto por lectura del expediente.** No era contradicción: `PCD-D06` documenta una **auditoría de 7 capas**, no la construcción del dominio. Cerró `CERRADO con hueco declarado — silo S6 abierto`, y el hueco sigue abierto |

⚠️ Y una cuarta que `DOC-033` obliga a no dar por hecha: que *«Rendición de Cuentas y Transparencia»* —mencionado como un trabajo— corresponda **uno a uno** con `d09` y `d07` tal como están definidos hoy. **El nombre no lo demuestra**; lo demostraría la correspondencia documental.

### Lo que `d06` resolvió, y lo que abrió

La lectura de `PCD-D06` disolvió la discrepancia: **ambas lecturas eran ciertas en dimensiones distintas.** «No iniciado» es exacto en `FONDO` —no hay `app/agents/d06`, ni silo `S6`, ni `ICM`—; «funcionalmente vivo» es exacto en `FORMA` —la superficie lee del snapshot, sin `demo_data`, contrastada contra el motor—.

> **`d06` es la prueba de que una sola dimensión no bastaba**, y apareció justo después de separarlas.

Lo que abrió está registrado en `REARQ_ARQUEO_CAPACIDAD_DOCUMENTAL`: la capacidad documental de Transparencia **existe, está preservada y no se reconstruye**. Su destino `REARQ` sigue sin decidirse.

### Lo que `d04` enseña como patrón

> **decisión aprobada ✅ + implementación efectivizada ✅ + canon no propagado 🔴**
>
> No es un dominio en disputa: es una **deuda de propagación documental**. Y conviene verificar además que la decisión tenga su anclaje canónico —si existe, la deuda es sólo de propagación; si no, hay que reconstruir esa autoridad.

Su motivo es arquitectónicamente interesante: los `SAT` dejaron de ser un dominio propio **para volverse alertas dentro de cada dominio**.

⚠️ Y conviene decirlo con precisión: **no es «una decisión de `FORMA`».** Se **manifiesta** en `FORMA` —el dominio desaparece del frontend— pero constituye una **decisión arquitectónica con consecuencias en ambos ejes**: cambia dónde reside la alerta, quién la calcula y a qué dominio pertenece su evidencia. Eso es `FONDO`.

### `d06` y el ICPI · la hipótesis que NO se decide aquí

Javo:

> *«Ahí estaba pensado meter el ICPI; pero éste posiblemente sea transversal y debe estar fuera, y el dominio de Salud Institucional iría con el índice de eficiencia directiva — o todo lo que implique, visualizo yo, pero no sé si sea lo más adecuado.»*

⚠️ **Decidir ahora `d06 → IED` sería exactamente lo que `Q-M1` acaba de prohibir**: meter un indicador existente en un dominio porque encaja de tamaño. El orden obligado es:

```
  1. ¿qué fenómeno es «Salud Institucional»?
  2. ¿qué pregunta pública necesita responder?
  3. ¿qué evidencia lo observa?
  4. ¿qué indicador —si alguno— responde esa pregunta?
  5. …y sólo entonces: ¿debe existir un dominio visible con ese nombre?
```

Seis salidas siguen abiertas, y ninguna está descartada:

| | Salida |
|---|---|
| A | `d06` es realmente necesario |
| B | `d06` queda absorbido por otro dominio |
| C | «salud institucional» es un **fenómeno transversal**, no un dominio |
| D | `IED` es un **componente** de ese fenómeno, no su indicador |
| E | `ICPI` e `IED` son dos medidas de **una misma dimensión transversal** |
| F | ninguno de los indicadores históricos lo representa y hay que **reconstruir** |

La intuición de Javo —el ICPI fuera de `d06` por transversal— **es coherente con lo que `010` y `Q-M0` ya midieron**. Eso la hace plausible; no la convierte en decisión.

## Las cuatro familias de preguntas · macroejes de la Constitución

⚠️ **No son una lista escrita aquí.** Son la agrupación que el canon ya declara para los 13 dominios, y la columna «capacidad del Estado» de cada uno es lo que los convierte en **familias de preguntas** y no en rótulos.

### Macroeje 1 · **DIRECCIÓN**

> ¿hacia dónde va la administración y con qué mandato?

| Dominio | Capacidad del Estado | Pregunta rectora | Indicador |
|---|---|---|---|
| `d01` Planificación Estratégica | trayectoria | ¿Lo planificado se formula en concordancia con el mandato, y el gasto aterriza donde el plan manda? | Avance físico metas PDOT |
| `d02` Presupuesto y Financiamiento | movilización | ⬜ **por declarar** | Elegibilidad / fondos en riesgo |
| `d03` Gobernanza del Mandato | fidelidad democrática | ⬜ **por declarar** | Consistencia IFE-A |

### Macroeje 2 · **CAPACIDAD**

> ¿con qué puede la administración sostener lo que se propone?

| Dominio | Capacidad del Estado | Pregunta rectora | Indicador |
|---|---|---|---|
| `d04` Alertas Institucionales | anticipación | ⬜ **por declarar** | Cola del SAT |
| `d05` Holding e Integración Municipal | articulación | ⬜ **por declarar** | Promedio de entidades |
| `d06` Salud Institucional | sostenibilidad interna | ⬜ **por declarar** | ⚠️ «Cumplimiento Institucional (ICPI)» |

### Macroeje 3 · **DEMOCRACIA**

> ¿ante quién responde y con qué verificabilidad?

| Dominio | Capacidad del Estado | Pregunta rectora | Indicador |
|---|---|---|---|
| `d07` Transparencia | verificabilidad | ⬜ **por declarar** | LOTAIP 21/21 |
| `d08` Participación Ciudadana | inteligencia colectiva | ⬜ **por declarar** | Gobernanza participativa (IGP) |
| `d09` Rendición de Cuentas | responsabilidad pública | ¿Lo que el GAD rindió ante el CPCCS se corresponde con lo que hizo, y la ciudadanía pudo incidir? | Estado del circuito de rendición |

### Macroeje 4 · **TERRITORIO**

> ¿qué ocurre en el territorio y con quiénes?

| Dominio | Capacidad del Estado | Pregunta rectora | Indicador |
|---|---|---|---|
| `d10` Cobertura de Servicios e Infraestructura | acceso colectivo | ⬜ **por declarar** | Cobertura agua/saneamiento · NBI |
| `d11` Desarrollo Económico Territorial | dinamización | ⬜ **por declarar** | PEA / cadenas de valor |
| `d12` Inclusión, Equidad y Género | inclusión y equidad | ⬜ **por declarar** | Presupuesto con enfoque de género (PSG) |
| `d13` Sostenibilidad y Resiliencia Ambiental | resiliencia | ⬜ **por declarar** | ICODS · biofísico/riesgo |

## ★★ DOS EJES, no dos versiones del mismo · y ambos valen

### 📜 CORRECCIÓN · `FONDO`/`FORMA` significaba dos cosas distintas

`Q-M1` leyó los macroejes como `FONDO`/`FORMA` en sentido **ontológico** —qué gestiona la administración frente a cómo la gestiona—. Javo usa los mismos términos en sentido **arquitectónico**:

> *«Cuando me refiero a FONDO es lo estructural —código, documentación, metodología—; FORMA, a lo que vemos en el frontend de los dominios.»*

⚠️ **Dos cosas distintas con el mismo nombre es exactamente lo que `DOC-033` prohíbe**, y esta vez el nombre lo compartían dos ideas **ambas correctas**. Javo pidió conservar las dos. Así que no se descarta ninguna: **se separan**.

| | Eje | Pregunta | Vocabulario |
|---|---|---|---|
| **1** | **ARQUITECTÓNICO** — de producto | ¿dónde y cómo existe el conocimiento **dentro de QUIRA**? | **`FONDO`** / **`FORMA`** |
| **2** | **ONTOLÓGICO** — de la gestión pública | ¿qué realidad estamos intentando conocer? | **`SECTORIAL`** / **`TRANSVERSAL`** |

Renombrar el segundo eje **no le quita valor**: le quita la colisión. «Transversal» ya se usa en el proyecto, así que no inflama el canon (`Regla de Oro 7`).

### Eje 1 · `FONDO` / `FORMA` — arquitectura de QUIRA

| | Qué contiene |
|---|---|
| **`FONDO`** | código · Gold Master · datos · conectores · metodología · fórmulas · reglas · evidencia · documentación · ontología · trazabilidad · pruebas · gobernanza |
| **`FORMA`** | frontend · dominios visibles · navegación · indicadores presentados · mapas · narrativa · semáforos · comparaciones · experiencia |

> ### Y de aquí sale una regla de precisión
>
> **No se dice «el ICPI es FONDO».** Se dice: el constructo pertenece al conocimiento metodológico de QUIRA; **su cálculo reside en `FONDO` y su representación en `FORMA`**. Decir lo primero mezcla niveles.

### Eje 2 · `SECTORIAL` / `TRANSVERSAL` — la realidad observada

| Macroeje | Capacidades que agrupa | Lectura |
|---|---|---|
| 1 DIRECCIÓN | trayectoria · movilización · fidelidad democrática | **TRANSVERSAL** — modos de administrar |
| 2 CAPACIDAD | anticipación · articulación · sostenibilidad interna | **TRANSVERSAL** — modos de administrar |
| 3 DEMOCRACIA | verificabilidad · inteligencia colectiva · responsabilidad pública | **TRANSVERSAL** — modos de administrar |
| 4 TERRITORIO | acceso colectivo · dinamización · inclusión y equidad · resiliencia | **SECTORIAL** — materias y poblaciones |

> ### ⚠️ Esa columna es una HIPÓTESIS DE LECTURA ONTOLÓGICA
>
> El reparto `1,2,3 → TRANSVERSAL` y `4 → SECTORIAL` **no está declarado en la Constitución**: es una lectura que el canon *admite*, no una clasificación que el canon *hace*. Se marca como hipótesis y se publica como tal.
>
> Confundir «el canon admite esta lectura» con «el canon lo dice» es la misma promoción indebida que `Q-M0` tuvo que corregir. La lectura es **útil para pensar** y no es todavía una propiedad del canon.

⚠️ **Y eso sigue sin validarla.** Que los macroejes admitan esa lectura es **compatible** con la hipótesis; no demuestra que organice las preguntas **mejor** que la agrupación actual. Compararlo exigiría las preguntas, y **la mayoría de los dominios aún no está curada**. Es la misma disciplina que se aplicó a `IED`.

> ### Los dos ejes son ORTOGONALES, y por eso ambos sirven
>
> Un indicador **transversal** puede residir en `FONDO` y mostrarse en `FORMA`. Un dominio **sectorial** también. Cruzar los dos ejes es lo que permite preguntar, por ejemplo, si un fenómeno transversal tiene hoy una `FORMA` que lo represente — y el caso `IED` sugiere que **no la tiene**.

## El cruce · las cuatro respuestas posibles

Cuando exista la pregunta, el cruce con el indicador histórico da una de cuatro:

| | | Significa |
|---|---|---|
| **A** | ✅ | el indicador existente responde bien |
| **B** | 🟡 | el indicador existente responde parcialmente |
| **C** | 🔵 | el indicador existente responde una pregunta DISTINTA de la que su dominio plantea |
| **D** | 🔴 | el indicador existente no hay indicador para esta pregunta |

⚠️ **El cruce no determina por sí solo el destino `REARQ`.** Es **evidencia para evaluarlo**, no la decisión. Un indicador puede «responder bien» y aun así deber trasladarse, o «no responder» porque la pregunta está mal planteada. Leer `D → RECONSTRUIR` de forma automática sería sustituir el juicio arquitectónico por una tabla.

Con esa cautela: `A` es evidencia a favor de conservar, `B` de ampliar, `C` de trasladar —el caso más interesante, y el que ya se sospecha en el ICPI: reside en `d06` y puede estar respondiendo una pregunta de otro eje— y `D` es el único que **puede** obligar a crear algo nuevo.

### Lo que hoy puede cruzarse

| Dominio | Pregunta | Indicador | Cruce |
|---|---|---|---|
| `d01` | ¿Lo planificado se formula en concordancia con el mandato, y el gasto ater… | Avance físico metas PDOT | ⬜ **por evaluar en `Q-M2`** |
| `d09` | ¿Lo que el GAD rindió ante el CPCCS se corresponde con lo que hizo, y la c… | Estado del circuito de rendición | ⬜ **por evaluar en `Q-M2`** |
| `d02` | ⬜ sin pregunta | Elegibilidad / fondos en riesgo | 🔴 **no cruzable**: no hay pregunta contra la cual evaluar |
| `d03` | ⬜ sin pregunta | Consistencia IFE-A | 🔴 **no cruzable**: no hay pregunta contra la cual evaluar |
| `d04` | ⬜ sin pregunta | Cola del SAT | 🔴 **no cruzable**: no hay pregunta contra la cual evaluar |
| `d05` | ⬜ sin pregunta | Promedio de entidades | 🔴 **no cruzable**: no hay pregunta contra la cual evaluar |

### ⚠️ `Q-M2` NO está bloqueada · está ACOTADA

La `v1` decía que `Q-M2` quedaba bloqueada porque faltaban once preguntas. Es demasiado fuerte. La formulación correcta:

> **`Q-M2` puede comenzar únicamente sobre los dominios cuya curación ya permite establecer una pregunta rectora.** Para los dominios no iniciados o incompletos, cualquier evaluación indicador↔pregunta debe permanecer pendiente hasta completar su curación.

Y eso significa que **`Q-M2` puede trabajar hoy sobre el subconjunto maduro de 2 dominios** — los que tienen pregunta rectora declarada, no sobre ninguno como decía la versión anterior.

Un indicador sin pregunta declarada **no puede responder bien ni mal: no se puede evaluar**. Eso no lo convierte en malo.

⚠️ Y tampoco autoriza a clasificarlo: **su estado en `Q-M0` permanece pendiente de clasificación**. Decir «es la categoría `B`, problema de arquitectura» sería adjudicar una causa antes de tener el lado de la comparación que falta.

## ★ Lo que el refactor debe hacer con los dominios ya curados

Javo:

> *«Los curados deben entrar en el refactor. Por ejemplo unificar planificación y presupuesto —`d01` y `d02`— para trabajar toda esa sección en un solo dominio, no dos. Y así todos los cambios en cada dominio que mejoren sustancialmente a QUIRA.»*

> ### Estar curado no significa quedar congelado
>
> Un dominio curado entra al refactor **con más autoridad, no con menos**: es el único que tiene evidencia suficiente para decidir si debe unificarse, dividirse o trasladarse. Los no curados no pueden ni siquiera plantearse esa pregunta.

### ★ La misión, dicha por Javo

> *«Los dominios deben subsanarse, mejorarse, elevarse a lo que realmente necesitamos para QUIRA — ésa es la misiva de este refactor, no dejarlos como están. Todos deben revisarse íntegramente para potenciar y elevar cada dominio, con base en el Excel y la normativa. Todo debe crecer.»*

Eso cambia la naturaleza de `REARQ`. **No es una auditoría de conservación.** No pregunta «¿está bien el dominio actual?», sino:

> **¿Qué debería ser este dominio para que QUIRA cumpla adecuadamente su propósito?**

Con una regla que no cambia: **primero entendemos qué existe; después decidimos qué debe existir.** El método es `CLASIFICAR → COMPRENDER → EVALUAR → REDISEÑAR → IMPLEMENTAR`, nunca `CLASIFICAR → CONSERVAR`.

### Ocho destinos posibles, no seis

«Refactorizar» se quedaba corto: sugería arreglar defectos, y la misión es **elevar**.

| Destino | Cuándo |
|---|---|
| **CONSERVAR** | funciona y satisface la necesidad |
| **MEJORAR** | necesita elevarse |
| **REESTRUCTURAR** | requiere cambio interno importante |
| **UNIFICAR** | combinar con otro dominio |
| **DESCOMPONER** | separar fenómenos mezclados |
| **TRASLADAR** | cambiar residencia |
| **RECONSTRUIR** | lo existente no representa lo que QUIRA necesita conocer |
| **DEPRECAR** | dejarlo fuera |

> ### ⚠️ `PENDIENTE` no es un destino
>
> Se listaba como noveno y **no pertenece a la misma familia**. Los ocho de arriba responden *«¿qué hacemos con este dominio?»*; `PENDIENTE` responde *«¿ya podemos decidirlo?»*. Es un **estado de la decisión**, no un destino.
>
> Mezclarlos permitiría cerrar un dominio con destino `PENDIENTE` y dar por hecho el análisis. Un dominio con la decisión pendiente **no tiene destino asignado todavía** — que es justamente lo que hay que poder decir.

> ### Y la regla central de `Q-M1`, reformulada
>
> **Los dominios históricos no conservan automáticamente su residencia, nombre, estructura ni indicador.** Cada uno será evaluado frente a las preguntas que QUIRA necesita responder, y podrá conservarse, mejorarse, reestructurarse, unificarse, descomponerse, trasladarse, reconstruirse o deprecarse.

Es una vuelta más que «los indicadores se ganan su residencia»: **los dominios también**.

### El caso `d01` + `d02` — lo que habría que verificar antes

| Criterio | Por qué importa |
|---|---|
| ¿responden **la misma pregunta rectora** o dos distintas? | `d01` la tiene declarada; `d02` **no** — y sin ella no se puede comparar |
| ¿comparten **unidad de análisis**? | unificar dominios con unidades distintas produce un dominio que mide dos cosas |
| ¿comparten **evidencia primaria**? | `IPE` cruza gasto ejecutado con metas del PDOT: **ya opera sobre ambos** |
| ¿qué pasa con sus indicadores y sus `PCD` cerrados? | `DOC-028`: continuidad histórica ≠ continuidad metodológica |

⚠️ **La unificación es plausible y no está demostrada.** `IPE` —el indicador más maduro— vive en `d01` y mide precisamente la articulación plan↔presupuesto: eso es **evidencia a favor**. Pero `d02` no tiene pregunta declarada, así que **hoy falta un lado de la comparación**. Es `Q-M2` sobre el subconjunto maduro.

## Lo que `Q-M1` entrega, y lo que no

| ✅ Establecido | ⬜ Abierto |
|---|---|
| las cuatro familias existen en el canon y agrupan los 13 dominios | las preguntas rectoras **aún no formalmente disponibles** (11) |
| los macroejes se dejan leer como `FONDO`/`FORMA` | si esa lectura organiza **mejor** que la actual |
| la pregunta aparece al **curar** el dominio, no al escribirla | qué indicador responde a qué pregunta (`Q-M2`) |

> ### La consecuencia operativa, y no es la que se esperaba
>
> `Q-M1` iba a reconstruir las preguntas necesarias. Lo que encuentra es que **el canon ya declaró las familias** y que el camino para que las preguntas existan **ya está definido**: es el `PCD`, la curación de dominio (`Regla de Oro 8`).
>
> No hace falta un método nuevo. Hace falta **aplicar el que hay**.

⚠️ **Formulación cuidada:** no se dice «faltan 11 preguntas», porque eso imputaría una carencia. Se dice que **las preguntas rectoras todavía no están formalmente disponibles para los dominios no curados** — que es una fotografía del avance del trabajo, no un defecto de la ontología.

Y eso **no** significa «curar todos antes de seguir». Significa que la Rearquitectura tiene una **dependencia declarada**: cualquier decisión sobre residencia de indicadores se apoya en preguntas que, en varios casos, todavía no están escritas.

## Lo que `Q-M1` NO hace

- **No inventa las preguntas que todavía no están disponibles.**
- **No dice «este índice sirve y este no».**
- **No valida `FONDO`/`FORMA`**: la contrasta y declara qué falta para poder decidirlo.
- **No toca el motor.** Gold Master intacto · baseline **27,4582 %** congelado.

---
*REARQ · `Q-M1` · 13 dominios · 2 con pregunta declarada · 4 familias derivadas del canon · el Gold Master no se modificó · Dylus Lab © 2026*
