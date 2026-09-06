# GM-Ω · ICPI — SERIE TEMPORAL DEL MOTOR  `011-C3R`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/serie_temporal_motor.py`.

> ### Qué es esto, dicho con precisión
> `011-C3` se ejecutó sobre el corpus documental **disponible**, y posteriormente se identificó un **corpus histórico externo relevante que no formó parte de su universo de revisión**. Esto es una **verificación de sensibilidad documental**: determina si ese corpus contiene evidencia capaz de modificar alguna conclusión de `C3`.

⚠️ **No prejuzga el resultado.** Puede terminar **sin cambio**, **parcialmente modificado** o **reabierto**. Y no dice que `C3` estuviera incompleto: dice que su universo de evidencia creció después.

⚠️ **El límite que no se cruza.** La serie puede demostrar **cuándo** y **qué** cambió. **No demuestra por qué.** Convertir una secuencia en una causa sería `DOC-009`. El resultado más fuerte posible es:

> **SECUENCIA DE CAMBIO DEMOSTRADA · JUSTIFICACIÓN AÚN NO DETERMINADA**

Que ya es mucho más rico que un `NO DETERMINABLE` seco.

## El universo examinado

| | |
|---|---:|
| archivos candidatos | 82 |
| **artefactos históricos únicos por contenido** (SHA-256) | **71** |
| legibles | 71 |
| **con evidencia estructural suficiente del motor** para las preguntas examinadas | **68** |
| con hoja `H01` de parámetros | 68 |

⚠️ **La terminología es deliberada.** «Artefactos únicos por contenido» **no** significa «estados históricos del motor». Un hash distinto puede deberse a un cambio en el motor, en los datos, en otra hoja, o a algo puramente cosmético. Llamarlos «versiones metodológicas» confundiría *archivo distinto* con *diseño distinto* — por eso el análisis trabaja con **transiciones de las variables relevantes**, no con diferencias binarias del libro.

⚠️ **11 archivos son copias exactas** de otra versión —mismo contenido, distinto nombre—. Deduplicar por hash antes de analizar evita leer el mismo libro varias veces y, sobre todo, evita contar una copia como una transición.

## La serie, ordenada por fecha

| Fecha | Archivo | Hojas | Factores | `C_i` mecanismo | Piso `0,50` | `Ci_Manual` |
|---|---|---:|---:|---|---|---|
| 2026-02-27 | `Instrumento SIAP-ICPI TESIS.xlsx` | 27 | — | — | — | — |
| 2026-03-06 | `SIAP-ICPI_VERSION_CON_METODOLOGIA.xlsx` | 43 | — | — | — | — |
| 2026-04-10 | `TERRA — Sistema de Integridad Algorítmic` | 37 | 6 | — | — | — |
| 2026-04-24 | `TERRA — Sistema de Integridad Algorítmic` | 56 | 6 | — | — | — |
| 2026-04-25 | `TERRA — Sistema de Integridad Algorítmic` | 58 | 6 | — | — | — |
| 2026-04-29 | `TERRA — Sistema de Integridad Algorítmic` | 72 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-29 | `TERRA — Sistema de Integridad Algorítmic` | 72 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 73 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 73 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 72 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 73 | 0 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 73 | 0 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 74 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 72 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 74 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — (SIAP-ICPI v1.0).xlsx` | 74 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 74 | 6 | calidad proceso | ✅ | ✅ |
| 2026-04-30 | `TERRA — Sistema de Integridad Algorítmic` | 74 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-01 | `TERRA — Sistema de Integridad Algorítmic` | 74 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-01 | `TERRA — Sistema de Integridad Algorítmic` | 78 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-01 | `TERRA — Sistema de Integridad Algorítmic` | 88 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-03 | `ECIAP_BACKUP_20260503_010318.xlsx` | 90 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-03 | `ECIAP-EGG-7.8 (v1.0) by Gnomika Lab erro` | 94 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-03 | `ECIAP-EGG-7.8 (v1.0) by Gnomika Lab.xlsx` | 95 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-05 | `ECIAP-EGG-7.8 (v1.0) by Gnomika Lab.xlsx` | 96 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-06 | `ECIAP-EGG-7.8 (v1.0) by Gnomika Lab Insu` | 99 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-06 | `ECIAP-EGG-7.8 (v1.0) by Gnomika Lab.xlsx` | 99 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-08 | `ECIAP_GOLD_MASTER_v1.1_Q1_2026_BACKUP_pr` | 99 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-08 | `TERRA — Sistema de Integridad Algorítmic` | 90 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-08 | `TERRA — Sistema de Integridad Algorítmic` | 90 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-08 | `TERRA — Ecosistema de Integridad Algorít` | 94 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-10 | `ECIAP_GOLD_MASTER_v1.1_Q1_2026.xlsx` | 100 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-10 | `Dylus Lab - Sistema de Integridad Algorí` | 113 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-10 | `ECIAP_GOLD_MASTER_v1.1_Q1_2026.xlsx` | 99 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-11 | `Dylus Lab - Sistema de Integridad Algorí` | 113 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-11 | `Dylus Lab - Sistema de Integridad Algorí` | 113 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-14 | `SIAP-ICPI_GOLD_MASTER_v3.0_QUIRA_2026051` | 113 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-14 | `SIAP-ICPI_GOLD_MASTER_v4.0_QUIRA_2026051` | 114 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-14 | `SIAP-ICPI_GOLD_MASTER_v4.1_QUIRA_2026051` | 115 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v4.1_QUIRA_2026051` | 115 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v5.0_TGI_20260516.` | 116 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v5.1_TGI_20260516.` | 116 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v5.2_TGI_20260516.` | 116 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v5.3_TGI_20260516.` | 119 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v5.4_TGI_20260516_` | 119 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-16 | `SIAP-ICPI_GOLD_MASTER_v5.4_TGI_20260516_` | 119 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-17 | `SIAP-ICPI_GOLD_MASTER_v5.4_TGI_20260516.` | 120 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-17 | `SIAP-ICPI_GOLD_MASTER_v5.4_TGI_20260517.` | 120 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-18 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518_` | 121 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-20 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518_` | 121 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-25 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-25 | `TGI_GOLD_MASTER_v6.0_20260525.xlsx` | 34 | — | — | — | — |
| 2026-05-26 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518_` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-26 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518_` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-26 | `SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_202605` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-05-30 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-06-15 | `SIAP-ICPI_GOLD_MASTER_v5.5_WORK_20260615` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-06-23 | `SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_202606` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-06-24 | `SIAP-ICPI_GOLD_MASTER_v5.5_WORK_20260623` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-06-29 | `SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_202607` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-06-30 | `SIAP-ICPI_GOLD_MASTER_v5.5_WORK_20260624` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-01 | `SIAP-ICPI_GOLD_MASTER_v6.0_FREEZE_202606` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-01 | `SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_202607` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-01 | `SIAP-ICPI_GOLD_MASTER_v5.5_FREEZE_202607` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-02 | `SIAP-ICPI_GOLD_MASTER_v5.5_WORK_20260702` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-15 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-23 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-29 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-07-29 | `SIAP-ICPI_GOLD_MASTER_v5.6_FREEZE_202608` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-08-11 | `SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx` | 123 | 6 | calidad proceso | ✅ | ✅ |
| 2026-09-04 | `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.` | 122 | 6 | calidad proceso | ✅ | ✅ |

## ★ Las transiciones · sólo donde algo cambia

Ésta es la mitad que hace viable el método: de la serie completa sólo interesan sus **discontinuidades**. Lo demás no se lee.

⚠️ **Se descarta el ruido de lectura.** Algunos libros se guardaron con valores en vez de fórmulas, y entonces `n_factores` lee `0` sin que el motor haya cambiado. Una transición que va y vuelve el mismo día, con todas las demás propiedades intactas, **es un artefacto de lectura, no un cambio de diseño** — y llamarla transición sería fabricar genealogía.

### número de factores del numerador

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `6` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-30 | `0` | `6` | `TERRA — Sistema de Integridad Algorítmica Pr` |

### `C_i` = calidad de proceso

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `False` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `False` | `True` | `TERRA — Sistema de Integridad Algorítmica Pr` |

### piso `MÁX(0,50; …)`

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `False` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `False` | `True` | `TERRA — Sistema de Integridad Algorítmica Pr` |

### `Ci_Manual_2025`

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `False` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `False` | `True` | `TERRA — Sistema de Integridad Algorítmica Pr` |

### pesos de deducción

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `` | `05·10·15` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `05·10·15` | `` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-30 | `` | `05·10·15` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-30 | `05·10·15` | `` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-30 | `` | `05·10·15` | `TERRA — Sistema de Integridad Algorítmica Pr` |

### `H01` Sección L

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `False` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `False` | `True` | `TERRA — Sistema de Integridad Algorítmica Pr` |

### `H01` Sección M

| Fecha | De | A | Archivo |
|---|---|---|---|
| 2026-04-10 | — | `False` | `TERRA — Sistema de Integridad Algorítmica Pr` |
| 2026-04-29 | `False` | `True` | `TERRA — Sistema de Integridad Algorítmica Pr` |

## ★ El corte · dónde ocurre el cambio

| | Fecha |
|---|---|
| última versión **sin** el mecanismo determinista | **2026-04-25** |
| primera versión **con** el mecanismo determinista | **2026-04-29** |
| declarado en `H01!A94` («Ci DETERMINISTA v1.0») | **2026-04-27** |

> ### La ventana del cambio queda acotada a días, y la declaración del autor **se corrobora con evidencia independiente**
>
> `H01!A94` declara el **27-abr-2026**. La última versión sin el mecanismo es del **2026-04-25**; la primera con él, del **2026-04-29**. La fecha declarada **cae dentro de la ventana**.

### ★ Y lo que la serie demuestra y `C3` no podía saber

Las transformaciones **no fueron graduales**. En la misma versión aparecen a la vez:

| Elemento | ¿Aparece en la misma versión? |
|---|---|
| el piso `MÁX(0,50; …)` | ✅ **sí** |
| el fallback `Ci_Manual_2025` | ✅ **sí** |
| la Sección L (matriz de deducciones) | ✅ **sí** |
| la Sección M (registro de infracciones) | ✅ **sí** |

> ### `C_i` no derivó: fue REFACTORIZADO en un solo acto de diseño
>
> Mecanismo, pesos, piso, fallback y las dos secciones de `H01` entran **juntos** en la primera versión identificada con el nuevo mecanismo.

⚠️ **Y aquí la formulación exacta importa.** Decir que esto «descarta la calibración iterativa» sería más fuerte de lo que la serie permite: pudo haber ajustes fuera de los artefactos preservados, o una calibración desarrollada antes y materializada de golpe. Lo defendible es:

> **La serie preservada no evidencia una calibración iterativa ni un ajuste gradual de estos parámetros.** Por tanto, la hipótesis de una calibración iterativa **observable en la serie** queda **sin soporte documental**.

Y una magnitud acompaña al cambio: entre esas dos versiones el libro pasa de **58 a 72 hojas** — catorce nuevas. Eso es **consistente con una modificación estructural sustantiva del instrumento**; por sí solo no la demuestra.

## ★ FASE 3 · sensibilidad documental acotada

**213 documentos** `.md` y `.txt` del corpus histórico, revisados para responder **una sola pregunta**:

> ¿Existe en el corpus tardíamente incorporado evidencia documental que **explique la decisión** materializada entre el 25 y el 29 de abril de 2026?

No se leyeron completos. Se buscaron los términos de `C_i` y, de ésos, **sólo los que además traen lenguaje de decisión** —«DECISIÓN», «REEMPLAZAR», «DETECTAR», «razón», «criterio»—. ⚠️ Que un artefacto **nombre** a `C_i` no prueba que lo **justifique**: es la distinción que ya falló una vez al intentar derivar la doctrina por términos.

**12 documentos** contienen lenguaje de decisión.

| Fecha | Documento |
|---|---|
| 2026-04-20 | `metodologia_beta_Dctos/INSUMOS METODOLOGIA.md` |
| 2026-04-27 | `_historico/Prompt/GOLDMASTER_REFACTOR_MASTER_v2.0.md` |
| 2026-04-28 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-04-29 | `_historico/TERRA_ECIAP/Refactorizacion_TERRA/varios/construccion de refactor` |
| 2026-05-19 | `_historico/ETL_scripts_legacy/quira_insumos_legacy/scripts/gold_master_previ` |

### ★ Y la respuesta a `P5` aparece

`GOLDMASTER_REFACTOR_MASTER_v2.0.md` no menciona `C_i`: **lo corrige**. Lo cataloga como error crítico y prescribe el reemplazo —

```
  E-CRIT-04: Variable Ci mal definida o sin Motor Determinista

  DETECTAR: «imputabilidad», «status legal», «personería
            jurídica», «legalidad de la entidad» en la
            definición de Ci
  DETECTAR: Ci_mínimo = 0  (debe ser 0.50)
  DETECTAR: INF-04 como deducción acumulable (debe ser FIJA)
  DETECTAR: H01 sin Sección L o sin Sección M

  REEMPLAZAR — Ci = Motor de Verificación Normativa v1.0
  «Motor Ci Determinista v1.0 (DECISIÓN 27-Abr-2026)»
```

Y la razón, escrita:

> **«`Ci` evalúa la CALIDAD DEL EXPEDIENTE ADMINISTRATIVO vía infracciones normativas verificadas — nunca el estatus jurídico de ninguna entidad.»**

### Qué explica y qué no

| Pregunta | Estado tras la Fase 3 |
|---|---|
| ¿por qué se **sustituyó el constructo**? | ✅ **DECLARADO** · para que `C_i` no evalúe el **estatus jurídico de una entidad**. La definición anterior —imputabilidad, personería, legalidad— se catalogó como **error crítico** |
| ¿por qué **esos pesos** `0,15 · 0,10 · 0,05`? | ⬜ **NO DETERMINABLE** · el documento los enuncia, no los justifica |
| ¿por qué el **piso `0,50`**? | ⬜ **NO DETERMINABLE** · dice «NUNCA 0», no dice por qué `0,50` |

> ### La razón declarada encaja con el canon, y eso la hace más creíble sin volverla demostrada
>
> Evaluar «el estatus jurídico de una entidad» sería exactamente lo que la `Regla de Oro 2` prohíbe —lenguaje acusatorio— y lo que el principio rector niega: **QUIRA certifica verificabilidad, no verdad**. La corrección de `C_i` es coherente con la doctrina que el sistema ya tenía.

⚠️ **Grado exacto: `DECLARADO`, no `DEMOSTRADO`.** Es una razón escrita por el autor en un artefacto de trabajo fechado y corroborada por la implementación resultante. No es una demostración de la intención — `DOC-024` sigue aplicando. En concreto: **no hay evidencia independiente suficiente para afirmar que ésa fuera la ÚNICA motivación del rediseño**.

### Y una precisión sobre qué le pasó a la definición anterior

Decir «no se abandonó, se catalogó como error crítico» sería impreciso: **sí fue abandonada como mecanismo operativo**. Lo correcto:

> La definición anterior fue **conservada como antecedente histórico**, pero su **mecanismo operativo fue declarado un defecto crítico y sustituido** por el Motor `C_i` Determinista v1.0.

Que es exactamente la categoría `📜 SUPERADO METODOLÓGICAMENTE` de la carta de rearquitectura, y encaja con `BM-05` y `DOC-031`.

### La cadena reconstruida

```
  C_i original         imputabilidad orgánica · responsabilidad
        ↓
  problema detectado   riesgo de evaluar atributos JURÍDICOS de
                       la entidad
        ↓
  E-CRIT-04            esa definición = defecto crítico
        ↓
  27-abr-2026          DECISIÓN: sustituir el mecanismo
        ↓
  nuevo C_i            calidad del expediente vía infracciones
                       normativas verificadas
        ↓
  regla de protección  nunca el estatus jurídico de la entidad
        ↓
  29-abr-2026          implementación: L + M + pesos + piso +
                       fallback
```

> Esto ya no es arqueología: es **la traza documental de una decisión de diseño**.

⚠️ Y la frontera se mantiene: hay evidencia de **lo que el documento prescribe y declara como razón**. No la hay de que ésa fuera la única motivación.

## ★ Dictamen de `C3-R` · las seis preguntas

| # | Pregunta | Respuesta | Estado |
|---|---|---|---|
| **P1** | ¿cuándo cambia `C_i` de mecanismo? | entre **2026-04-25** y **2026-04-29** | ✅ **DEMOSTRADO** |
| **P2** | ¿cuándo cambian sus pesos? | **en el mismo acto** · `0,05 · 0,10 · 0,15` entran con el mecanismo | ✅ **DEMOSTRADO** |
| **P3** | ¿cuándo aparece el piso `0,50`? | **en el mismo acto** | ✅ **DEMOSTRADO** |
| **P4** | ¿cuándo aparece `Ci_Manual_2025`? | **en el mismo acto** | ✅ **DEMOSTRADO** |
| **P5a** | ¿por qué se **sustituyó el constructo**? | para que `C_i` no evalúe el **estatus jurídico de una entidad** · `E-CRIT-04` | ✅ **DECLARADO** (Fase 3) |
| **P5b** | ¿por qué **esos pesos**? | el documento los enuncia, no los justifica | ⬜ **NO DETERMINABLE** |
| **P5c** | ¿por qué el **piso `0,50`**? | «NUNCA 0», sin decir por qué `0,50` | ⬜ **NO DETERMINABLE** |
| **P6** | ¿se reconcilia el versionado? | pendiente · tres esquemas sin correspondencia | 🔄 abierto |

⚠️ **`P5` y `P6` son problemas distintos y no deben mezclarse.** `P5` es **causalidad histórica** —por qué se sustituyó—; `P6` es **identidad y versionado** —cómo se corresponden las nomenclaturas—. `P6` podría resolverse por completo mañana y `P5b`/`P5c` seguir abiertas. No sería una contradicción.

## ★ Los tres grados · qué se demostró y qué no

La distinción que impide que este expediente se lea como más concluyente de lo que es:

### ✅ DEMOSTRADO

- existe una versión anterior **sin** el mecanismo determinista;
- existe una posterior **con** él;
- la transición queda acotada al **25-29 de abril de 2026**;
- `H01!A94` declara el **27 de abril**, y esa fecha cae dentro;
- el mecanismo aparece junto con pesos, piso, fallback y las Secciones `L` y `M`;
- la estructura del libro aumenta sustancialmente en el mismo salto;
- existe un documento que **prescribe** el reemplazo y declara su razón.

### 🟡 INFERENCIA RAZONABLE

- que se tratara de un **acto de refactorización deliberado y unitario**. La evidencia estructural lo hace altamente plausible.

### 🔴 NO DEMOSTRADO

- **por qué esos pesos y ese piso concretos**;
- que la razón declarada fuera la **única** motivación.

> ### «Entraron juntos» ≠ «sabemos por qué entraron juntos»
>
> `DOC-009` aplica entero: la simultaneidad **sugiere** una decisión única; no la prueba. Y una razón declarada por el autor es `DECLARADO`, no `DEMOSTRADO` (`DOC-024`).

> ### El estado de `C3` cambia — pero no en la dirección que se temía
>
> `011-C3` decía `NO DETERMINABLE` a secas sobre la sustitución del mecanismo, los pesos y el piso. Ahora dice:
>
> **SECUENCIA DE CAMBIO DEMOSTRADA · RAZÓN DEL CONSTRUCTO DECLARADA · JUSTIFICACIÓN DE LOS PARÁMETROS AÚN NO DETERMINADA.**

Sus conclusiones **no se invalidan**: se **precisan**. Y una parte —el porqué de la sustitución— pasa de `NO DETERMINABLE` a `DECLARADO`, que es exactamente para lo que sirve una reapertura por evidencia tardía (`DOC-031`).

## ★ Cinco preguntas distintas, cinco calidades de respuesta

La arquitectura epistemológica que `C3-R` deja montada, y que evita que se hable de «la razón del cambio» como si fuera una sola cosa:

| | Pregunta | Estado |
|---|---|---|
| **Historia** | ¿qué mecanismo existía? | ✅ **DEMOSTRADO** |
| **Evolución** | ¿cuándo fue sustituido? | ✅ **DEMOSTRADO** |
| **Decisión** | ¿qué razón declaró el diseñador? | 🟡 **DECLARADO** |
| **Justificación metodológica** | ¿por qué esa solución es válida? | ⬜ **fuera de alcance** · `011-C4` |
| **Parámetros** | ¿por qué `0,15 / 0,10 / 0,05` y `0,50`? | 🔴 **NO DETERMINABLE** |

> Son cinco cosas diferentes, y hoy tenemos respuestas de **calidad distinta** para cada una. Tratarlas como una sola fue lo que hizo que `011-C3` cerrara con un `NO DETERMINABLE` demasiado grueso.

> ### `C3-R` — CERRADO
>
> **SECUENCIA DE CAMBIO DEMOSTRADA · RAZÓN DEL CAMBIO DE MECANISMO DECLARADA · JUSTIFICACIÓN DE LOS PARÁMETROS AÚN NO DETERMINADA · RECONCILIACIÓN DE VERSIONADO PENDIENTE.**

### ⚠️ Qué significa «cerrado» aquí — y qué no

> Cerrar `C3-R` **no implica que la genealogía histórica completa de QUIRA esté agotada**. Implica que la evidencia adicional examinada es **suficiente para actualizar las conclusiones específicas de `C3`** sin necesidad de ampliar indefinidamente la búsqueda para las preguntas hoy abiertas.

Esa distinción **protege a `BM-05` de convertirse en un pozo sin fondo**. No se seguirá excavando hasta encontrar una frase que diga «elegimos 0,15 porque…». Si aparece, se incorpora; perseguirla indefinidamente no es método.

Y la ausencia **permanece como hallazgo, no como pendiente**:

> Los parámetros fueron **establecidos documentalmente**, pero su **fundamento cuantitativo no ha sido determinado**.

Para `011-C4` eso vale más que conocer la historia completa: un parámetro sin fundamento cuantitativo es una **decisión de diseño abierta** (`DOC-027`), y hay tres.

### Lo que esto le entrega a `011-C4`

| Antes de `C3-R` | Después |
|---|---|
| «`C_i` cambió en algún momento, sin razón conocida» | «`C_i` fue sustituido en un acto fechado, con **razón declarada** y dentro de un proceso de refactorización documentado» |
| la pregunta era: ¿por qué se fue acumulando? | la pregunta es: **¿es válida la solución que se adoptó, y sus parámetros?** |

⚠️ **Sobre la palabra «refactorización».** Se usa porque existe un documento que se declara a sí mismo proceso de refactorización del Gold Master y prescribe los cambios. **La fuente de esa clasificación es ese documento, no el incremento de hojas** — el salto de 58 a 72 es sólo consistente con ella.

### `P6` merece expediente propio, y no cabe en `010`

`P6` es una cuestión de **identidad de artefactos**, no de transferibilidad LATAM. Meterla en `010` mezclaría dos problemas sin relación. Si se cierra, se cierra construyendo un **grafo de correspondencia de versiones**:

```
  archivo → hash → fecha → versión declarada → estructura →
            fórmula → sucesor / progenitor probable
```

con estados `1:1 DEMOSTRADO` · `CORRESPONDENCIA PROBABLE` · `RAMIFICACIÓN` · `DUPLICADO POR CONTENIDO` · `NO DETERMINABLE` — la misma taxonomía de `011-B`, que aparece por tercera vez.

**No bloquea a `C4`** mientras no afecte a una conclusión metodológica.

---
*GM-Ω-ICPI-011-C3R · 71 versiones únicas de 82 archivos · lectura pura · el Gold Master vigente no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
