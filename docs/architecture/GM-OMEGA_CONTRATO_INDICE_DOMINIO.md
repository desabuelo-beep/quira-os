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

## Estado: **30 de 48 celdas** por declarar (62 %)

| Índice | Dominio | Rol | Pregunta que responde | Capa | Autoridad |
|---|---|---|---|---|---|
| `ICPI` | **POR_DECLARAR** | **POR_DECLARAR** | **POR_DECLARAR** | INSTITUCIONAL | ⚠️ el indicador nuclear del Gold Master no tiene dominio declarado — y es posible que la respuesta correcta sea que es TRANSVERSAL, no de un dominio |
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

**El indicador nuclear del Gold Master no tiene dominio declarado.** Y antes de asignarle uno conviene considerar que la respuesta correcta quizá sea que **no pertenece a ninguno**: si el ICPI mide la congruencia de la cadena completa —planificación, presupuesto, contratación, ejecución, transparencia, rendición— entonces es **transversal**, y meterlo en un dominio lo empequeñecería.

Eso conecta con la corrección de `T1-T2`: el ICPI es **indicador nuclear del Gold Master**, no «el centro de QUIRA». Puede ser nuclear y transversal a la vez — pero hay que **declararlo**, no dejarlo implícito.

## Lo que este contrato NO hace

- **No renombra `ICPI`.** La migración del nombre, si `011` la decide, no cuesta trazabilidad: el **identificador** (`ICPI`) permanece estable y es lo que usan el código, el Gold Master y toda referencia previa; el **nombre desarrollado** puede evolucionar con su versión, su vigencia y su nombre histórico conservado (`DOC-015`). Pero el orden no se invierte: **primero se decide qué mide el constructo, después cómo se llama.**
- **No asigna dominios por inferencia.** Diez de doce índices esperan una decisión de arquitectura o de curación.
- **No toca el Gold Master, ni el frontend, ni AVEP.**

---
*GM-Ω · Contrato T3-T5 · 30/48 celdas por declarar · ningún código de producto modificado · Dylus Lab © 2026*
