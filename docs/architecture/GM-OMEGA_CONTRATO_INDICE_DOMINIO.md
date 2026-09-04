# GM-Ω · CONTRATO ÍNDICE → DOMINIO  `T3-T5`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/contrato_indice_dominio.py`. Para declarar una celda, se edita `_CONTRATO` en el script **citando la autoridad**, no aquí.

> ### Qué es esto
> El artefacto que le falta a QUIRA para poder decir, de forma **verificable**:
>
> **«Este indicador pertenece aquí, responde esta pregunta y se presenta de esta manera.»**
>
> Cuando exista completo, el frontend deja de ser una discusión estética y pasa a ser una **proyección de la arquitectura canónica**.

> ### ⚠️ Las celdas NO se rellenan por inferencia
> Sólo se declara lo que tiene **autoridad documental**: un PCD cerrado, un ADR, una decisión registrada. Que un índice aparezca en una página no prueba que ése sea su dominio canónico. Todo lo demás queda `POR_DECLARAR` **y se cuenta**.
>
> Un contrato a medio llenar que dice cuánto le falta es más útil que uno completo por suposición — eso sería `DOC-009` a escala de arquitectura.

## Estado: **23 de 48 celdas** por declarar (48 %)

| Índice | Dominio | Rol | Pregunta que responde | Capa | Autoridad |
|---|---|---|---|---|---|
| `ICPI` | d06 | PRIMARIO | **POR_DECLARAR** | INSTITUCIONAL | Constitución §CAPA 0.5 (d06 → «Cumplimiento Institucional (ICPI)») + PCD-D06 «Ancla en ICPI» — ⚠️ residencia canónica EN REVISIÓN, ver §T3-R |
| `IPE` | d01 | PRIMARIO | ¿Qué proporción del gasto ejecutado está vinculada a metas del PDOT? | INSTITUCIONAL | PCD-D01 · cerrado · fórmula nativa en H16b |
| `IGP` | d08 | PRIMARIO | **POR_DECLARAR** | INSTITUCIONAL | Constitución §CAPA 0.5 (d08 → «Gobernanza participativa (IGP)») · ⚠️ alcance en disputa: mide 2 de 7 mecanismos (D-010) |
| `ITAM` | d07 | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | PCD-D07 · asignación por confirmar |
| `IED` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | 06_IED_DIRECTIVO.md |
| `IFE` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | H16 |
| `ICODS` | d13 | PRIMARIO | **POR_DECLARAR** | INSTITUCIONAL | Constitución §CAPA 0.5 (d13 → «ICODS · biofísico/riesgo») |
| `IEF` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | H20c |
| `PSG` | d12 | PRIMARIO | **POR_DECLARAR** | INSTITUCIONAL | Constitución §CAPA 0.5 (d12 → «Presupuesto con enfoque de género (PSG)») |
| `IBSC` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | TÉCNICO | H12b |
| `TGI` | **POR_DECLARAR** | COMPUESTO | **POR_DECLARAR** | INTERNO | 01_TGI_FRAMEWORK.md · 5 dimensiones · probablemente transversal |
| `MMP` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INTERNO | 08_MMP_MENSUAL.md |

## Los dominios y su pregunta

Javo lo señaló: **los dominios también responden a algo propio.** `m_rdc.py` lo dice en un comentario —«su dueño por la pregunta que responde»— pero **ningún campo la declara**. Es la misma forma que el mapeo índice→dominio: existe en el diseño, no como artefacto.

| Dom | Nombre | Capacidad del Estado · macroeje | Indicador (Constitución) | Construcción | Pregunta rectora |
|---|---|---|---|---|---|
| `d01` | Planificación Estratégica | trayectoria · 1 Dirección | Avance físico metas PDOT | CONSTRUIDO · PCD-D01 | ¿Lo planificado se formula en concordancia con el mandato, y el gasto aterriza donde el plan manda? |
| `d02` | Presupuesto y Financiamiento | movilización · 1 Dirección | Elegibilidad / fondos en riesgo | PCD-D02 | **POR_DECLARAR** |
| `d03` | Gobernanza del Mandato | fidelidad democrática · 1 Dirección | Consistencia IFE-A | PCD-D03 | **POR_DECLARAR** |
| `d04` | Alertas Institucionales | anticipación · 2 Capacidad | Cola del SAT | SELLADO · sin construir | **POR_DECLARAR** |
| `d05` | Holding e Integración Municipal | articulación · 2 Capacidad | Promedio de entidades | SELLADO · sin construir | **POR_DECLARAR** |
| `d06` | Salud Institucional | sostenibilidad interna · 2 Capacidad | ⚠️ «Cumplimiento Institucional (ICPI)» | PCD-D06 · sintetizador | **POR_DECLARAR** |
| `d07` | Transparencia | verificabilidad · 3 Democracia | LOTAIP 21/21 | EN CURACIÓN | **POR_DECLARAR** |
| `d08` | Participación Ciudadana | inteligencia colectiva · 3 Democracia | Gobernanza participativa (IGP) | ENTRABLE | **POR_DECLARAR** |
| `d09` | Rendición de Cuentas | responsabilidad pública · 3 Democracia | Estado del circuito de rendición | CONSTRUIDO · PCD-D09 | ¿Lo que el GAD rindió ante el CPCCS se corresponde con lo que hizo, y la ciudadanía pudo incidir? |
| `d10` | Cobertura de Servicios e Infraestructura | acceso colectivo · 4 Territorio | Cobertura agua/saneamiento · NBI | SELLADO · sin construir | **POR_DECLARAR** |
| `d11` | Desarrollo Económico Territorial | dinamización · 4 Territorio | PEA / cadenas de valor | SELLADO · sin construir | **POR_DECLARAR** |
| `d12` | Inclusión, Equidad y Género | inclusión y equidad · 4 Territorio | Presupuesto con enfoque de género (PSG) | SELLADO · sin construir | **POR_DECLARAR** |
| `d13` | Sostenibilidad y Resiliencia Ambiental | resiliencia · 4 Territorio | ICODS · biofísico/riesgo | SELLADO · primer ejercicio de mutabilidad | **POR_DECLARAR** |

**11 de 13 dominios** no tienen pregunta declarada. Sólo se escribieron las de `d01` y `d09`, que tienen PCD cerrado y de cuyo expediente se pueden sostener. **Inventar las demás sería escribir el canon desde un script**, que es exactamente lo contrario de cómo QUIRA construye.

## Los roles (`T4`)

| Rol | Qué significa |
|---|---|
| **PRIMARIO** | responde la pregunta central de su dominio |
| **COMPUESTO** | agrega otros indicadores |
| **AUXILIAR** | alimenta a otro indicador, no se lee solo |
| **DIAGNÓSTICO** | sirve al análisis interno, no a la lectura pública |
| **POR_DECLARAR** | ⚠️ la arquitectura no lo ha declarado |

## ⚠️ El caso `ICPI` merece párrafo propio

**Sí tenía dominio declarado, y estaba donde Javo recordaba**: `PCD-D06 Salud Institucional` lo fija como su ancla —*«Ancla en ICPI — cumplimiento sostenible de gobierno»*—. Lo que faltaba no era la decisión: era el **artefacto que la hiciera legible sin abrir el expediente de un dominio**. Eso es exactamente lo que este contrato es.

Y el hallazgo interesante es que **la asignación no cierra la pregunta**, la afina: `d06` está cerrado **como sintetizador** —un dominio que agrega lo que otros producen—, así que alojar allí un indicador **transversal** no es una contradicción sino la forma natural de hacerlo. Las dos cosas pueden ser ciertas a la vez:

> `ICPI` = **indicador nuclear transversal del Gold Master**, con residencia canónica en `d06` por ser el dominio sintetizador.

⚠️ Se deja como **denominación provisional**, no como decisión. Para declararlo transversal hace falta responder algo que todavía no está escrito: **¿la pregunta que responde el ICPI pertenece a un dominio, o evalúa la relación ENTRE dominios?** Consumir datos de varios silos no basta —un indicador puede leer de todas partes y aun así responder una pregunta local—. La celda `pregunta` sigue `POR_DECLARAR` a propósito.

## ★ El título de la tesis disuelve el falso dilema

Javo aportó el título completo del documento fundacional:

> **Arquitectura del Sistema de Integridad Algorítmica Preventiva (SIAP): Modelo de Congruencia Intersistémica** para la Trazabilidad y Alineación POA-PDOT en los GAD del Ecuador.

Ese título **contiene las dos palabras**, y no como sinónimos: como **dos niveles de una misma arquitectura**.

```
   SIAP   Sistema de INTEGRIDAD Algorítmica Preventiva   ← el propósito
     └── ICPI   Modelo de CONGRUENCIA Intersistémica     ← lo que mide
```

Esto **corrige un planteamiento anterior de esta auditoría**. Se había formulado como disyuntiva —«si el constructo es congruencia hay que quitar la multiplicatividad; si es integridad conjunta, el nombre se queda corto»— y era demasiado rápido. La multiplicatividad puede ser **perfectamente coherente con un constructo de congruencia** si la teoría establece que la congruencia efectiva **exige simultáneamente** determinadas condiciones. Integridad y congruencia no compiten por el nombre: una es el sistema, la otra es el modelo.

Lo que `011` debe juzgar, entonces, **no es qué palabra encaja mejor**, sino la **semántica de la multiplicación**:

> ¿Qué relación teórica existe entre `P`, `R`, `V`, `E`, `T` y `C`, y qué significa que uno de ellos sea cero? Si `V=0` —«no pude verificar documentalmente»— anula toda la contribución de una meta, el índice no está diciendo «esta meta no es congruente»: está diciendo «la congruencia **certificable** de esta unidad es nula porque falta una condición necesaria». Puede ser defendible. Hay que demostrarlo.

Y `SIAP` resultó tener **dos expansiones** en las tesis —«Sistema de Integridad Algorítmica Preventiva» y «Sistema Integral de Auditoría y Planificación»—: la misma deriva semántica de `AVEP`, en la sigla que da nombre al propio Gold Master.

## ★ T3-R · La transversalidad del ICPI es una DECISIÓN NUEVA

Javo lo precisó y corrige cómo se venía contando: **nunca se concibió el ICPI como transversal.** Tenía su dominio —`d06`— igual que los demás índices. Lo que ahora se plantea es **incorporar** esa transversalidad.

La diferencia no es de matiz. Presentarlo como si «siempre hubiera sido transversal y no nos habíamos dado cuenta» sería reescribir la historia para que encaje con una idea nueva — el mismo pecado que `DOC-016` prohíbe, aplicado a la arquitectura en vez de al nombre. **Es una evolución del canon, y como tal se registra.**

### El canon YA autoriza este refactor

No hace falta forzar nada: la Constitución lo previó.

> **DECLARACIÓN DE MUTABILIDAD** — «Los 12 cajones constituyen la organización operativa VIGENTE […] La estructura de dominios es modular […] **Lo permanente es la Capa 0; los dominios son variables.**»

Y `CAPA 0.5` da el criterio que decide: cada dominio es la manifestación de **una capacidad del Estado**. Ahí está el argumento, y no es una opinión:

| | |
|---|---|
| `d06` es la capacidad de | **sostenibilidad interna** — «cumplir funciones consistentemente» |
| El ICPI mide | **congruencia entre el mandato y su materialización a través de los silos** |

**No son lo mismo.** Y el propio canon lo delata: la Constitución nombra el indicador de `d06` como «**Cumplimiento** Institucional (ICPI)», cuando `GM-Ω-ICPI-001` reconstruyó que el ICPI **no mide cumplimiento** —mide congruencia— y la Regla de Oro lo prohíbe expresamente.

> La residencia del ICPI en `d06` se apoya en una denominación que el propio canon ya retiró.

Eso **no invalida `d06`**: cuando se selló, «Cumplimiento Institucional» era la lectura vigente. Es una divergencia **entre dos documentos del canon**, y resolverla es justamente lo que GM-Ω existe para hacer.

### Pero la transversalidad todavía no está probada

⚠️ **Que el ICPI consuma datos de varios silos NO prueba que sea transversal.** Un indicador puede leer de todas partes y responder una pregunta local; inferir la arquitectura del patrón de consumo sería `DOC-009` otra vez. La prueba tiene que venir del **constructo**:

> Si para responder su pregunta es **necesario relacionar sistemáticamente dimensiones que pertenecen a distintos dominios**, entonces la transversalidad es una propiedad del constructo y no una conveniencia de diseño.

Y el canon ya tiene el instrumento para juzgarlo: **la prueba de exportabilidad** (Constitución §CAPA 0.5) —*«¿sobreviven las capacidades si desaparecen los dominios?»*—. Aplicada al ICPI: ¿sobrevive el ICPI si desaparece `d06`? Si la respuesta es sí, no era su dominio.

### Residencia ≠ ámbito, y ahí está la salida

El contrato actual sólo sabe decir `índice → dominio`, y esa relación es demasiado pobre. Hacen falta dos campos donde hay uno:

```
   RESIDENCIA CANÓNICA   dónde se gestiona y quién responde por él
   ÁMBITO DE COBERTURA   qué dominios atraviesa
```

Con esa distinción, **sacar el ICPI de `d06` deja de ser un dilema**. No es «o pertenece a `d06` o desaparece de `d06`»: `d06` puede conservarlo como **indicador relacionado** —lo necesita para explicar la salud institucional— sin ser su propietario exclusivo. Nada se esconde; cambia quién responde por él.

### Secuencia propuesta — y no empieza moviendo nada

| | | |
|---|---|---|
| **R0** | Diagnóstico | qué dominios hay, cuáles construidos, qué pregunta rectora, qué índices residen, cuáles se solapan |
| **R1** | Modelos | `A` todo índice dentro de un dominio · `B` dominios + transversales · `C` dominios + capa transversal + Centro |
| **R2** | Decisión | ¿sale el ICPI de `d06`? ¿qué otros son transversales? ¿`d06` conserva referencia? |

⚠️ **`T3-R` es diagnóstico, no ejecución.** No mueve el ICPI, no toca el Gold Master, no desmonta dominios. Primero se demuestra **qué arquitectura hace falta**; sólo entonces se cambia. Y `011` sigue por delante: mover un indicador cuyo constructo aún está en dictamen sería reorganizar la casa antes de saber qué se guarda.

## ⚠️ Ningún dominio está cerrado hasta pasar este refactor

**Primero, una distinción que esta auditoría tenía al revés.** Javo la precisó: **sellado ≠ terminado, y sellado ≠ construido.**

| Estado | Qué significa |
|---|---|
| **SELLADO** | su concepción quedó fijada bajo el canon de entonces · **no está construido** |
| **ABIERTO / CONSTRUIDO** | es sobre el que se ha trabajado y tiene producto |
| **CERRADO (PCD)** | su expediente de curación se completó — cosa distinta de las dos anteriores |

Se venía leyendo «cerrado» como «terminado e intocable», y eso llevó a recomendar no tocar `d01`, `d06` y `d09`. **Era demasiado fuerte.**

Regla de Javo, entonces, con su consecuencia: esos tres tienen PCD cerrado bajo un canon **anterior** al Terminology Freeze — antes de que existieran `DOC-013`, `DOC-014` y este contrato. Su cierre es válido **para lo que entonces se auditó**, y no acredita lo que entonces no se preguntaba.

Es el mismo principio que gobierna todo GM-Ω: **un mecanismo de cobertura no es autoridad sobre su propia cobertura**. Un PCD cerrado acredita las siete capas que revisó, no las preguntas que aún no se hacían. Por eso el estado correcto de esos tres no es «cerrado» ni «abierto», sino **cerrado bajo canon anterior** — y su reapertura es barata: sólo necesitan declarar su pregunta rectora y la residencia de sus índices, que es lo que este contrato pide.

## Lo que este contrato NO hace

- **No renombra `ICPI`.** La migración del nombre, si `011` la decide, no cuesta trazabilidad: el **identificador** (`ICPI`) permanece estable y es lo que usan el código, el Gold Master y toda referencia previa; el **nombre desarrollado** puede evolucionar con su versión, su vigencia y su nombre histórico conservado (`DOC-015`). Pero el orden no se invierte: **primero se decide qué mide el constructo, después cómo se llama.**
- **No asigna dominios por inferencia.** Diez de doce índices esperan una decisión de arquitectura o de curación.
- **No toca el Gold Master, ni el frontend, ni AVEP.**

---
*GM-Ω · Contrato T3-T5 · 23/48 celdas por declarar · ningún código de producto modificado · Dylus Lab © 2026*
