# GM-Ω · TERMINOLOGY FREEZE — INVENTARIO Y CLASIFICACIÓN  `T1-T2`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/terminologia_quira.py`.

> ### ⚠️ ESTA ETAPA NO TOCA CÓDIGO
> `T1` inventario · `T2` clasificación · `T3` autoridad · `T4` uso · `T5` necesidad. La acción —`T6`: CONSERVAR / RENOMBRAR / DEPRECAR / ELIMINAR / HISTÓRICO— se ejecuta **después**, y sólo con las decisiones tomadas. **Primero se estabiliza el vocabulario; después se cambia lo mínimo.** Cambiar código ahora sería la misma prisa que produjo el problema que este documento inventaria.

> ### La regla que lo gobierna · `DOC-013`
> **QUIRA no conserva conceptos por herencia; conserva únicamente conceptos que cumplen una función verificable en su arquitectura.**
>
> Es la regla de Javo —*«si no aporta a QUIRA, sólo infla»*— elevada de criterio de canon a **higiene ontológica de toda la arquitectura**. Y tiene una salvaguarda que la separa de la destrucción de evidencia: **un concepto puede morir como componente activo sin desaparecer de la historia de QUIRA.**

## Qué se mide y qué se declara

| | |
|---|---|
| **USO** — en cuántos archivos vive, si cruza al producto | **derivado** |
| **CATEGORÍA** — qué tipo de objeto es | **declarado**: es un juicio ontológico con autoridad, no una inferencia desde el patrón de uso (`DOC-009`) |

## La taxonomía

| Categoría | Qué es |
|---|---|
| **FUENTE** | origina evidencia — institución o sistema externo |
| **EVIDENCIA** | registro o documento verificable capturado |
| **VARIABLE** | dato operacionalizado que entra en un cálculo |
| **INDICADOR** | medida derivada de variables |
| **ESTADO** | condición epistemológica u operativa del dato |
| **PRODUCTO** | entrega funcional a un usuario |
| **CAPA** | capacidad transversal, no un producto |
| **FUNCIÓN** | actividad de la arquitectura — extensión declarada en T2 |
| **ARTEFACTO** | objeto canónico del sistema — extensión declarada en T2 |
| **SIN_CATEGORÍA** | ⚠️ no responde a «¿qué tipo de objeto QUIRA soy?» |

⚠️ **La propuesta original tenía seis categorías más una transversal, y no bastaron.** El Observatorio no es fuente ni producto; el Gold Master no es evidencia ni indicador. Se extendió a `FUNCIÓN` y `ARTEFACTO` **declarando la extensión** — y que hicieran falta es en sí un resultado de `T2`: la arquitectura real de QUIRA tiene más tipos de objeto de los que el primer corte suponía.

## T1-T4 · Inventario clasificado

| Nombre | Categoría | Capa | Autoridad que lo define | Archivos | En producto |
|---|---|---|---|---:|---:|
| `LOTAIP` | FUENTE | PÚBLICO | LOTAIP Art. 7 | 249 | 19 |
| `CPCCS` | FUENTE | PÚBLICO | LOPC Art. 88 | 217 | 18 |
| `SERCOP` | FUENTE | PÚBLICO | LOSNCP | 206 | 10 |
| `eSIGEF` | FUENTE | PÚBLICO | COPFP · MEF | 199 | 17 |
| `SIGAD` | FUENTE | PÚBLICO | SENPLADES | 94 | 1 |
| `PDOT` | EVIDENCIA | PÚBLICO | COOTAD · COPFP Art. 41 | 417 | 26 |
| `R_i` | VARIABLE | TÉCNICO | tesis · H14!F | 15 | — |
| `P_i` | VARIABLE | TÉCNICO | tesis · H14!G | 13 | — |
| `V_i` | VARIABLE | TÉCNICO | tesis · H13!F | 13 | — |
| `E_i` | VARIABLE | TÉCNICO | ⚠️ NOT_DETERMINABLE (007-B0) | 13 | — |
| `T_i` | VARIABLE | TÉCNICO | H07b!fila 20 | 10 | — |
| `C_i` | VARIABLE | TÉCNICO | H01 TBL_CALIBRACION_Ci | 10 | — |
| `ICPI` | INDICADOR | INSTITUCIONAL | tesis (abril 2026) · H12!B33 | 357 | 12 |
| `TGI` | INDICADOR | INTERNO | 01_TGI_FRAMEWORK.md | 343 | 6 |
| `IGP` | INDICADOR | INSTITUCIONAL | H20b | 77 | 6 |
| `IFE` | INDICADOR | INSTITUCIONAL | H16 | 74 | 6 |
| `PSG` | INDICADOR | INSTITUCIONAL | H16c | 73 | 6 |
| `IED` | INDICADOR | INSTITUCIONAL | 06_IED_DIRECTIVO.md | 70 | 4 |
| `ITAM` | INDICADOR | INSTITUCIONAL | H18 | 51 | 1 |
| `IPE` | INDICADOR | INSTITUCIONAL | H16b · PCD-D01 | 40 | 1 |
| `MMP` | INDICADOR | INTERNO | 08_MMP_MENSUAL.md | 35 | 1 |
| `ICODS` | INDICADOR | INSTITUCIONAL | H20 | 33 | 2 |
| `IEF` | INDICADOR | INSTITUCIONAL | H20c | 20 | — |
| `IBSC` | INDICADOR | TÉCNICO | H12b_MOTOR_IBSC | 14 | 1 |
| `NOT_DETERMINABLE` | ESTADO | INSTITUCIONAL | Constitución CAPA 0 | 8 | — |
| `TEMPORAL_SEMANTIC_GAP` | ESTADO | TÉCNICO | GM-Ω taxonomía | 7 | — |
| `UNTRACEABLE` | ESTADO | TÉCNICO | GM-Ω taxonomía | 5 | — |
| `QUIRA Institucional` | PRODUCTO | PÚBLICO | ADR-041 §4 | 31 | 2 |
| `QUIRA Cooperación` | PRODUCTO | PÚBLICO | ADR-041 §4 | 25 | 2 |
| `QUIRA Impact` | PRODUCTO | PÚBLICO | ADR-041 §4 | 19 | 1 |
| `QUIRA Economic` | PRODUCTO | PÚBLICO | ADR-041 §4 | 11 | 1 |
| `SAT` | CAPA | INTERNO | H21-H24 · SAT_Catalogo | 265 | 13 |
| `GeoTwin` | CAPA | PÚBLICO | QTMP | 80 | 7 |
| `QUIRA IA` | CAPA | PÚBLICO | ADR-035/037 | 55 | 2 |
| `Motor` | FUNCIÓN | TÉCNICO | H12_MOTOR_ICPI_CANÓNICO · ADR-023 | 226 | 12 |
| `Ciudadana` | FUNCIÓN | PÚBLICO | ADR-041 §4 | 160 | 16 |
| `Observatorio` | FUNCIÓN | PÚBLICO | ADR-041 §4 | 53 | 8 |
| `Consola` | FUNCIÓN | INTERNO | ADR-042 | 15 | 1 |
| `QUIRA` | ARTEFACTO | PÚBLICO | identity/CONSTITUCION_INSTITUCIONAL.md | 825 | 59 |
| `Dylus Lab` | ARTEFACTO | PÚBLICO | identity/ | 794 | 60 |
| `Gold Master` | ARTEFACTO | TÉCNICO | ADR-023 · METODOLOGIA_GOLD_MASTER.md | 392 | 18 |
| `AVEP` ⚠️ | SIN_CATEGORÍA | HISTÓRICO | ⚠️ ninguna autoridad vigente lo define | 71 | 3 |

## La segunda dimensión · capa de presentación

| Capa | Qué significa |
|---|---|
| **PÚBLICO** | lenguaje de administración pública · primera capa de lectura |
| **INSTITUCIONAL** | ficha metodológica · segunda capa, al abrir el indicador |
| **TÉCNICO** | trazabilidad forense · tercera capa, usuario institucional |
| **INTERNO** | no cruza al producto (Regla de Oro 2) |
| **HISTÓRICO** | conservado por genealogía · fuera del runtime |

⚠️ **No es un filtro de publicación**, y el matiz decide todo lo demás. Los índices **están construidos para aparecer en el dominio que los representa**: esa decisión ya la tomó la arquitectura de dominios y no se relitiga aquí. Lo que la visibilidad decide es **en qué capa de lectura** aparece cada nombre dentro de su dominio.

La consecuencia práctica es la separación **nombre técnico ≠ nombre de presentación** (`DOC-014`):

```
   PÚBLICO         ¿El mandato ofrecido puede seguirse hasta
                   su materialización?          27,46 %
        ↓ abrir
   INSTITUCIONAL   ICPI · corte abril 2026 · qué mide, período,
                   universo, fuentes, metodología
        ↓ abrir
   TÉCNICO         Índice de Congruencia Programática e Intersistémica
                   → Gold Master → P·R·V·E·T·C → fuentes → evidencia
```

Así **no se oculta el indicador: se hace inteligible**. Y evita el riesgo opuesto —una portada de siglas y porcentajes flotantes— que induciría a leerlos como notas comparables entre sí. `DOC-012` ya dice por qué eso sería falso: **un porcentaje no significa nada por sí mismo**.

### Verificación · ¿cada índice aparece en su dominio?

De **12 indicadores** inventariados, **4** aparecen en alguna superficie de dominio:

| Indicador | Superficies de dominio donde se le encontró |
|---|---|
| `ICPI` | `p16_gobernanza` |
| `TGI` | — |
| `IED` | — |
| `IGP` | `p16_gobernanza` |
| `MMP` | — |
| `IPE` | `m_planificacion` |
| `IFE` | `p16_gobernanza` |
| `ITAM` | — |
| `ICODS` | — |
| `IEF` | — |
| `PSG` | — |
| `IBSC` | — |

### ⚠️ Y aquí el resultado que importa NO es esa tabla

**Esa tabla no demuestra nada, y hay que decirlo antes de que alguien la cite.** Se apoya en una lista de superficies de dominio **escrita a mano** en este mismo script (`_PAGS_DOMINIO`, 8 de las 55 páginas del producto). Un índice que no aparece puede vivir perfectamente en una superficie que la lista no incluye. Medir contra una lista propia y presentar el resultado como hallazgo sería exactamente lo que `DOC-009` prohíbe.

**Lo que sí quedó demostrado, al intentar la verificación:**

> **No existe un artefacto que declare qué índice pertenece a qué dominio.**

El mapeo existe —Javo lo tiene claro y la arquitectura lo aplica: *«todos los índices están construidos para aparecer en los dominios que los representan»*— pero **vive en el diseño, no en un artefacto verificable**. `PROTOCOLO_CURACION_DOMINIO` registra el estado de curación de cada dominio, no qué índice le corresponde.

Y sin esa tabla, **ninguna verificación automática es posible**: ni ésta, ni una que compruebe que un índice no se publica fuera de su dominio, ni una que detecte un dominio que perdió su indicador. Es la misma forma del problema de `E_i` —una regla que opera sin estar escrita— y del de `AVEP` —un vocabulario que se propaga sin autoridad que lo defina—.

**Producir ese mapeo es el primer entregable de `T3`.** No se improvisa aquí: exige leer dominio por dominio, y eso es curación, no inventario.

**«En producto»** cuenta archivos de `quira_pages/`, `components/` y `views/`. Un nombre interno con presencia ahí es candidato a revisión por Bloomberg Firewall — pero **no automáticamente una infracción**: puede aparecer en un comentario o en una clave de datos que nunca se pinta.

## T5 · ⚠️ Nombres que no responden a la pregunta

> *¿Qué tipo de objeto QUIRA soy?*

### `AVEP`

no es indicador, ni fuente, ni variable, ni estado, ni producto, ni capa. Nació como nombre de un eje conceptual, derivó a fórmula copiada en 11 hojas, y hoy existen DOS versiones incompatibles (D-012)

Vive en **71 archivos**, de los cuales **3 son superficies del producto** (`components/avep_badge.py`, `components/gauge.py`, `components/sentinel.py`).

**Que se haya propagado no demuestra que deba existir: demuestra que se propagó.** Y ésa es exactamente la distinción que `DOC-013` introduce.

## T1 · Siglas propias en uso que nadie clasificó

Detectadas en canon, `config.py` y `BOOT.md`, excluidas las normas e instituciones externas. **No son necesariamente deuda** —muchas serán hojas del Gold Master o nombres legítimos aún sin ficha—, pero cada una debería poder responder a qué tipo de objeto pertenece.

| Sigla | Archivos de canon donde aparece |
|---|---:|
| `IET` | 24 |
| `SIAP` | 23 |
| `IRS` | 17 |
| `ICM` | 6 |
| `PMV` | 4 |
| `EJECUTA` | 3 |
| `BDE` | 3 |
| `PROGAPSA` | 3 |
| `ACTIVA` | 3 |
| `CORREL` | 3 |
| `NORTH` | 3 |
| `ALTO` | 3 |
| `CPFP` | 3 |
| `BOOT` | 2 |
| `DPE` | 2 |
| `PRIVADO` | 2 |
| `VER` | 2 |
| `UNESCO` | 2 |
| `RIPS` | 2 |
| `CRE` | 2 |
| `PLAZO` | 2 |
| `RIESGO` | 2 |
| `OUTPUTS` | 2 |
| `DATOS` | 2 |
| `SOBRE` | 2 |

## ⚠️ Hallazgo de propina · siglas normativas mal formadas

La **Regla de Oro 3** prohíbe citar normas sin verificar. Una sigla a un solo carácter de la correcta es una cita que **no resuelve**, y ninguna revisión de contenido la ve: «parece» un código legal.

| Sigla en uso | Probablemente | Archivos |
|---|---|---:|
| `CPFP` | `COPFP` | 3 |

Lo detectó el inventario terminológico, no una revisión normativa — que es precisamente el argumento a favor de hacer este ejercicio. **Verificar dónde vive cada una antes de corregir**: una aparición en un backup del vault no es lo mismo que una en el canon vivo o en una cita publicada.

## Lo que este documento NO decide

- **No renombra nada.** `ICPI` sigue siendo *Índice de Congruencia Programática e Intersistémica*: es el nombre de la tesis, el documento con fecha anterior a todo Gold Master conservado, y **el único anclaje documental verificable que tiene el constructo**. Renombrarlo destruiría la genealogía que `001-007` reconstruyó.
- **No elimina AVEP.** Propone su categoría y mide su uso. La decisión —deprecar del runtime conservando la genealogía histórica— es de `T6`, y sólo después de que `011` dictamine si QUIRA necesita interpretar porcentajes mediante categorías para entregar su producto.
- **No construye el baremo parametrizable.** La arquitectura `país · institución · versión · constructo · umbrales · etiquetas · fundamento · vigencia` es un **patrón metodológico disponible**, no un componente obligatorio. Construirlo antes de saber si hace falta sería infringir `DOC-013` en el mismo documento que lo declara.

---
*GM-Ω · Terminology Freeze T1-T2 · 42 nombres clasificados · ningún código modificado · Dylus Lab © 2026*
