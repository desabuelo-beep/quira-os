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

| Nombre | Categoría | Autoridad que lo define | Archivos | En producto |
|---|---|---|---:|---:|
| `LOTAIP` | FUENTE | LOTAIP Art. 7 | 249 | 19 |
| `CPCCS` | FUENTE | LOPC Art. 88 | 215 | 18 |
| `SERCOP` | FUENTE | LOSNCP | 206 | 10 |
| `eSIGEF` | FUENTE | COPFP · MEF | 199 | 17 |
| `SIGAD` | FUENTE | SENPLADES | 94 | 1 |
| `PDOT` | EVIDENCIA | COOTAD · COPFP Art. 41 | 415 | 26 |
| `R_i` | VARIABLE | tesis · H14!F | 15 | — |
| `P_i` | VARIABLE | tesis · H14!G | 13 | — |
| `V_i` | VARIABLE | tesis · H13!F | 13 | — |
| `E_i` | VARIABLE | ⚠️ NOT_DETERMINABLE (007-B0) | 12 | — |
| `T_i` | VARIABLE | H07b!fila 20 | 10 | — |
| `C_i` | VARIABLE | H01 TBL_CALIBRACION_Ci | 10 | — |
| `ICPI` | INDICADOR | tesis (abril 2026) · H12!B33 | 355 | 12 |
| `TGI` | INDICADOR | 01_TGI_FRAMEWORK.md | 341 | 6 |
| `IGP` | INDICADOR | H20b | 75 | 6 |
| `IED` | INDICADOR | 06_IED_DIRECTIVO.md | 68 | 4 |
| `MMP` | INDICADOR | 08_MMP_MENSUAL.md | 33 | 1 |
| `NOT_DETERMINABLE` | ESTADO | Constitución CAPA 0 | 8 | — |
| `TEMPORAL_SEMANTIC_GAP` | ESTADO | GM-Ω taxonomía | 7 | — |
| `UNTRACEABLE` | ESTADO | GM-Ω taxonomía | 5 | — |
| `QUIRA Institucional` | PRODUCTO | ADR-041 §4 | 31 | 2 |
| `QUIRA Cooperación` | PRODUCTO | ADR-041 §4 | 25 | 2 |
| `QUIRA Impact` | PRODUCTO | ADR-041 §4 | 19 | 1 |
| `QUIRA Economic` | PRODUCTO | ADR-041 §4 | 11 | 1 |
| `SAT` | CAPA | H21-H24 · SAT_Catalogo | 265 | 13 |
| `GeoTwin` | CAPA | QTMP | 80 | 7 |
| `QUIRA IA` | CAPA | ADR-035/037 | 55 | 2 |
| `Motor` | FUNCIÓN | H12_MOTOR_ICPI_CANÓNICO · ADR-023 | 226 | 12 |
| `Ciudadana` | FUNCIÓN | ADR-041 §4 | 158 | 16 |
| `Observatorio` | FUNCIÓN | ADR-041 §4 | 53 | 8 |
| `Consola` | FUNCIÓN | ADR-042 | 15 | 1 |
| `QUIRA` | ARTEFACTO | identity/CONSTITUCION_INSTITUCIONAL.md | 823 | 59 |
| `Dylus Lab` | ARTEFACTO | identity/ | 792 | 60 |
| `Gold Master` | ARTEFACTO | ADR-023 · METODOLOGIA_GOLD_MASTER.md | 390 | 18 |
| `AVEP` ⚠️ | SIN_CATEGORÍA | ⚠️ ninguna autoridad vigente lo define | 69 | 3 |

**«En producto»** cuenta archivos de `quira_pages/`, `components/` y `views/`. Un nombre interno con presencia ahí es candidato a revisión por Bloomberg Firewall — pero **no automáticamente una infracción**: puede aparecer en un comentario o en una clave de datos que nunca se pinta.

## T5 · ⚠️ Nombres que no responden a la pregunta

> *¿Qué tipo de objeto QUIRA soy?*

### `AVEP`

no es indicador, ni fuente, ni variable, ni estado, ni producto, ni capa. Nació como nombre de un eje conceptual, derivó a fórmula copiada en 11 hojas, y hoy existen DOS versiones incompatibles (D-012)

Vive en **69 archivos**, de los cuales **3 son superficies del producto** (`components/avep_badge.py`, `components/gauge.py`, `components/sentinel.py`).

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
| `PROGAPSA` | 3 |
| `BDE` | 3 |
| `ACTIVA` | 3 |
| `CORREL` | 3 |
| `ALTO` | 3 |
| `NORTH` | 3 |
| `CPFP` | 3 |
| `DPE` | 2 |
| `BOOT` | 2 |
| `PRIVADO` | 2 |
| `VER` | 2 |
| `RIPS` | 2 |
| `UNESCO` | 2 |
| `CRE` | 2 |
| `PLAZO` | 2 |
| `RIESGO` | 2 |
| `OUTPUTS` | 2 |
| `SOBRE` | 2 |
| `DATOS` | 2 |

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
*GM-Ω · Terminology Freeze T1-T2 · 35 nombres clasificados · ningún código modificado · Dylus Lab © 2026*
