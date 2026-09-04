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

## Estado: **29 de 48 celdas** por declarar (60 %)

| Índice | Dominio | Rol | Pregunta que responde | Capa | Autoridad |
|---|---|---|---|---|---|
| `ICPI` | d06 | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | PCD-D06 §Diccionario campo 6 · «Ancla en ICPI» — ⚠️ y d06 está cerrado como SINTETIZADOR, lo que hace compatible la hipótesis transversal |
| `IPE` | d01 | PRIMARIO | ¿Qué proporción del gasto ejecutado está vinculada a metas del PDOT? | INSTITUCIONAL | PCD-D01 · cerrado · fórmula nativa en H16b |
| `IGP` | d08 | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | D-010 · curación de d08 · ⚠️ alcance en disputa: mide 2 de 7 mecanismos |
| `ITAM` | d07 | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | PCD-D07 · asignación por confirmar |
| `IED` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | 06_IED_DIRECTIVO.md |
| `IFE` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | H16 |
| `ICODS` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | H20 |
| `IEF` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | H20c |
| `PSG` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | H16c |
| `IBSC` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | TÉCNICO | H12b |
| `TGI` | **POR_DECLARAR** | COMPUESTO | **POR_DECLARAR** | INTERNO | 01_TGI_FRAMEWORK.md · 5 dimensiones · probablemente transversal |
| `MMP` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INTERNO | 08_MMP_MENSUAL.md |

## Los dominios y su pregunta

Javo lo señaló: **los dominios también responden a algo propio.** `m_rdc.py` lo dice en un comentario —«su dueño por la pregunta que responde»— pero **ningún campo la declara**. Es la misma forma que el mapeo índice→dominio: existe en el diseño, no como artefacto.

| Dominio | Nombre | Curación | Pregunta que responde |
|---|---|---|---|
| `d01` | Planificación | PCD-D01 ✅ | ¿Lo planificado se formula en concordancia con el mandato, y el gasto aterriza donde el plan manda? |
| `d02` | Presupuesto y Financiamiento | PCD-D02 | **POR_DECLARAR** |
| `d03` | Gobernanza y Mandato | PCD-D03 | **POR_DECLARAR** |
| `d04` | — | sin construir | **POR_DECLARAR** |
| `d05` | — | sin construir | **POR_DECLARAR** |
| `d06` | Salud Institucional | PCD-D06 ✅ | **POR_DECLARAR** |
| `d07` | Transparencia | PCD-D07 | **POR_DECLARAR** |
| `d08` | Participación Ciudadana | d08 entrable | **POR_DECLARAR** |
| `d09` | Rendición de Cuentas | PCD-D09 ✅ | ¿Lo que el GAD rindió ante el CPCCS se corresponde con lo que hizo, y la ciudadanía pudo incidir? |
| `d10` | — | sin construir | **POR_DECLARAR** |
| `d11` | — | sin construir | **POR_DECLARAR** |
| `d12` | — | sin construir | **POR_DECLARAR** |
| `d13` | Mutabilidad | Constitución §Mutabilidad | **POR_DECLARAR** |

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

## ⚠️ Ningún dominio está cerrado hasta pasar este refactor

Regla de Javo, y tiene consecuencia inmediata sobre este contrato: `d01`, `d06` y `d09` figuran como **cerrados**, pero se cerraron bajo un canon **anterior** al Terminology Freeze — antes de que existieran `DOC-013` (higiene ontológica), `DOC-014` (capas de presentación) y este contrato. Su cierre es válido **para lo que entonces se auditó**, y no acredita lo que entonces no se preguntaba.

Es el mismo principio que gobierna todo GM-Ω: **un mecanismo de cobertura no es autoridad sobre su propia cobertura**. Un PCD cerrado acredita las siete capas que revisó, no las preguntas que aún no se hacían. Por eso el estado correcto de esos tres no es «cerrado» ni «abierto», sino **cerrado bajo canon anterior** — y su reapertura es barata: sólo necesitan declarar su pregunta rectora y la residencia de sus índices, que es lo que este contrato pide.

## Lo que este contrato NO hace

- **No renombra `ICPI`.** La migración del nombre, si `011` la decide, no cuesta trazabilidad: el **identificador** (`ICPI`) permanece estable y es lo que usan el código, el Gold Master y toda referencia previa; el **nombre desarrollado** puede evolucionar con su versión, su vigencia y su nombre histórico conservado (`DOC-015`). Pero el orden no se invierte: **primero se decide qué mide el constructo, después cómo se llama.**
- **No asigna dominios por inferencia.** Diez de doce índices esperan una decisión de arquitectura o de curación.
- **No toca el Gold Master, ni el frontend, ni AVEP.**

---
*GM-Ω · Contrato T3-T5 · 29/48 celdas por declarar · ningún código de producto modificado · Dylus Lab © 2026*
