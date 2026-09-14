---
id: PANORAMA-DOCUMENTAL-001
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: REGISTRO
estado: ABIERTO — insumo para decisión, no decisión
fecha: 2026-09-10
---

# Panorama documental de QUIRA — barrido total

> **Por qué existe.** Javo, 2026-09-10: *«el barrido debe ser de todo, para tener la visión
> completa. Si la idea no es una auditoría, sino **elevar este ecosistema**, hasta para
> reclasificar documentación que no sirva y que implican reglas. Con ella ya tendríamos el
> panorama completo de cómo vamos a potenciar, mejorar y elevar el nivel de QUIRA en cada
> ámbito.»*
>
> ⛔ **Esto NO decide nada.** Es el insumo para que la decisión de gobernanza tenga sobre qué
> decidirse — igual que `AUTORIDAD_PROPOSICIONES_BOOT` hizo con `BOOT`.

**Universo:** `docs/` (12 subdirectorios) · `governance/` · `marco_teorico/` · `identity/`.
**Formatos:** `.md` y `.yaml`. **Exclusiones:** `worktrees`, `historico/`, `node_modules`, `.git`.
**Método:** extracción de frontmatter, título, estado, fecha y señales léxicas. **No se leyó el
contenido completo de los 275**: se leyeron sus metadatos y se midieron señales.

## 1 · El panorama

| directorio | docs | sin autoridad | señales obsol. | reglas | MB |
|---|---:|---:|---:|---:|---:|
| `docs/` (raíz) | 20 | **20** | 13 | 59 | 0,28 |
| `docs/adr` | 49 | **3** | 10 | 96 | 0,51 |
| `docs/architecture` | **70** | **65** | **39** | **135** | 0,99 |
| `docs/brn` | 31 | 31 | 14 | 1 | 0,17 |
| `docs/corpus_externo` | 31 | 31 | 7 | 33 | 0,25 |
| `docs/observations` | 33 | 3 | 6 | 28 | 0,19 |
| `docs/pcd` | 7 | **0** | 4 | 19 | 0,08 |
| `docs/registry` | 4 | 1 | 4 | 7 | 0,07 |
| `docs/sprint-b` | 10 | 10 | 1 | 43 | 0,07 |
| `docs/sprint-c` | 7 | 6 | 4 | 31 | 0,10 |
| `docs/sprint-d` | 1 | 1 | 0 | 8 | 0,01 |
| `governance` | 7 | **0** | 3 | 2 | 0,06 |
| `marco_teorico` · `identity` | 4 | 0 | 3 | 9 | 0,05 |
| **TOTAL** | **275** | **171** | **108** | **472** | **2,83** |

## 2 · ★ El hallazgo de gobernanza

> **472 reglas declaradas en 124 documentos. Sólo 96 viven en `docs/adr`, el único cuerpo con
> autoridad declarada casi universal (46 de 49). Las otras 376 están repartidas en documentos que
> no declaran de quién derivan.**

Y el caso concreto que lo vuelve serio:

| documento | reglas | ¿lo designa rector el `MASTER_INDEX`? | ¿declara autoridad? |
|---|---:|---|---|
| `sprint-c/DICCIONARIO_CONCEPTUAL_QUIRA` | 13 | **SÍ** — rector del ADN de los 13 dominios | ⛔ **no** |
| `architecture/QUIRA_OS_DEPENDENCY_ATLAS_v1` | 8 | **SÍ** — rector del cableado del código | ⛔ **no** |
| `architecture/PROTOCOLO_CURACION_DOMINIO` | 7 | **SÍ** — `Regla de Oro 8` | ⛔ **no** |
| `architecture/BRN_CICLO_VIDA_Y_MOLDE` | 8 | **SÍ** — el molde de la BRN | ⛔ **no** |
| `architecture/CONSTITUCION_VISUAL_QUIRA` | **15** | — | ⛔ **no** |
| `UX_CONTRACT` | 14 | — | ⛔ **no** |

> **El `MASTER_INDEX` les da autoridad; ellos no la declaran.** Y `check_health` sólo verifica los
> **129 activos registrados**: los 171 sin frontmatter **quedan fuera del gate**. Por eso el gate
> dice «100 % declaran autoridad» y a la vez el 62 % del corpus no la declara — **ambas cifras son
> ciertas y miden universos distintos**.

## 3 · Los tres cuerpos, por su comportamiento

| cuerpo | qué lo caracteriza | directorios |
|---|---|---|
| **CANON FORMAL** | declara autoridad · frontmatter · trazable | `adr` (46/49) · `pcd` (7/7) · `governance` (7/7) · `observations` (30/33) |
| **CANON DE HECHO** | el índice o el uso les da autoridad, **pero no la declaran** | buena parte de `architecture` · los rectores de `sprint-c` |
| **SEDIMENTO** | material de trabajo de una época, sin rector y sin uso verificado | `sprint-b` · `sprint-d` · `corpus_externo` · parte de `docs/` raíz |

⚠️ **`docs/brn` (31 archivos, 0 con frontmatter) no pertenece a ninguno de los tres**: son `YAML`
de CNO/RO con **su propio esquema de estado** (`vigente` · `propuesta` · `no_determinable`). No
les falta autoridad: la declaran de otra forma. **No se reclasifican con el mismo criterio.**

## 4 · ⚠️ Límite del método, declarado

La columna «señales obsol.» es **léxica, no semántica**: cuenta apariciones de *deprecado ·
superado · histórico · legacy…* en el texto. Un documento **vivo** que **habla** de deprecar otros
puntúa alto sin estar obsoleto — es el caso de `CARTA_REARQUITECTURA` (23) y del propio
`REARQ_ARQUEO` (7).

> **La señal indica dónde mirar, no qué concluir.** `DOC-035` aplicado a esta misma métrica:
> hallar el término prueba presencia del término, no obsolescencia del documento.

## 4-bis · `P0` · CLASIFICACIÓN POR AUTORIDAD × USO EFECTIVO

*(Encargo del asesor: clasificar cada documento, no cada palabra.)*

**Método:** para cada documento se buscan sus referencias entrantes en **todo el repositorio**
—`.md` · `.py` · `.yaml` · `.json`— usando **su identificador real** (`ADR-042`, `DOC-035`,
`CNO-VII-001`…) y no sólo el nombre del archivo. Se distingue **autoridad declarada** (frontmatter
`parent`) de **uso efectivo** (citado por ≥3 documentos, o por código, o por pruebas, o listado en
el índice).

| cuadrante | qué significa | docs | reglas |
|---|---|---:|---:|
| **A · CANON VIVO** | declara autoridad **y** se usa | **101** | 24 |
| **B · CANON INERTE** | declara autoridad y **nadie lo invoca** | **14** | 3 |
| **C · RECTOR DE FACTO** | **no declara** autoridad y **sí se usa** | **100** | **40** |
| **D · SEDIMENTO** | no declara y no se usa | **61** | 20 |
| *de los cuales* **huérfanos absolutos** | 0 citas · 0 código · 0 pruebas · fuera del índice | **24** | — |

### `P0.1` · CALIBRACIÓN — lo que estos cuadrantes NO autorizan a decir

**1 · El universo, congelado y reconciliado.**

```
P0 inicial      275 documentos
P0 corregido    276 documentos
Δ = +1          este mismo PANORAMA_DOCUMENTAL_QUIRA.md, creado entre ambos barridos
```

Queda registrado para que dentro de tres días nadie audite el instrumento en lugar del objeto.
**`U-P0 = 276`**, con los quince directorios declarados en la cabecera.

**2 · «Rector de facto» es una interpretación demasiado fuerte para los 100.**

Lo demostrado es más modesto y más defendible:

> **Existe un conjunto de documentos cuyo papel operativo o arquitectónico NO queda explicado por
> el esquema formal de autoridad que usa el gate.**

Un documento citado por código puede ser cuatro cosas distintas, y el conteo no las separa:

| | |
|---|---|
| **rector efectivo no declarado** | gobierna una decisión o regla |
| **derivado correctamente usado** | deriva de otro que sí declara |
| **artefacto operativo** | catálogo, configuración, plantilla, dato — **consumido, no normativo** |
| **referencia incidental** | mención histórica o de contexto |

> ⛔ **Uso en código ≠ autoridad normativa.** `RO-VIII-003.yaml` tiene 9 usos en código y **no es
> un rector**: es una regla operativa que el compilador consume. La etiqueta «rector de facto»
> se reserva para `P2`, cuando exista evidencia de que el documento **gobierna** algo.

**3 · El conteo de referencias no distingue el TIPO de vínculo.** Hoy suma por igual `cita ·
deriva_de · gobernado_por · implementa · verifica · sustituye · mención incidental`. Mientras no
se separen, **100 es una señal, no una conclusión**.

**4 · Y la regla que gobierna todo lo que sigue:**

> **Ningún documento se depreca, fusiona, eleva o elimina como consecuencia exclusiva de una
> métrica automática.** La máquina descubre · la evidencia contextualiza · **la gobernanza decide**.

### El cuadrante `C` · los de mayor peso

Documentos que el sistema **invoca** sin que declaren de dónde deriva su autoridad:

| reglas | código | pruebas | documento |
|---:|---:|---:|---|
| 3 | **8** | 0 | `NOMENCLATURA_CANONICA.md` |
| 2 | **7** | 1 | `ARQUITECTURA_CANONICA.md` — rector del Nivel 2 del stack |
| 4 | 2 | 0 | `architecture/CONSTITUCION_VISUAL_QUIRA.md` |
| 0 | **9** | 1 | `brn/RO-VIII-003.yaml` |
| 3 | 1 | 0 | `corpus_externo/QUIRA_STATE.md` |
| 1 | 3 | 1 | `QUIRA_DOCTRINE_v1.md` — la doctrina fundacional |
| 2 | 1 | 0 | `architecture/BRN_CICLO_VIDA_Y_MOLDE.md` |

⚠️ Las `RO-*.yaml` aparecen aquí por el mismo motivo del §3: **declaran autoridad con otro
esquema**. No son deuda: son un tipo distinto de artefacto y no deben contarse con este criterio.

### `B` · Los 14 inertes — y qué son realmente

`DEUDA_TECNICA_D07` (30K) · `ADR-048` · `DESCUBRIMIENTO_NORMATIVO_ADR031` · `OBS-025` · `OBS-019`
· `ADR-034` · `GENEALOGIA_QUIRA` · dos prompts de arranque · **`CNO-VIII-004..007`** · y este
mismo panorama, recién creado.

> **Inerte ≠ inválido.** Los `CNO-VIII-*` están en `propuesta` —es coherente que nada los invoque
> todavía—; los dos prompts son operativos de sesión; `OBS-019`/`OBS-025` son observaciones
> cerradas. El cuadrante mide **invocación**, no validez.

## 4-ter · ⛔ LA LECCIÓN · la métrica produjo el hallazgo, tres veces

La primera versión de esta clasificación buscaba referencias **por nombre de archivo**. Como los
ADR se citan por su número, el resultado fue catastrofista y **falso**:

| | métrica defectuosa | identificadores reales |
|---|---:|---:|
| canon inerte | 73 | **14** |
| canon vivo | 42 | **101** |
| huérfanos absolutos | 81 | **24** |

Y produjo una conclusión que llegué a escribir: *«`ADR-042`, el rector de la capa de adquisición,
es canon inerte»*. **Falso**: ningún ADR tiene cero citas. Sólo 6 de 46 tienen tres o menos.

> **Tercera vez en la misma sesión que una métrica mal construida genera el hallazgo:**
>
> | # | métrica | falso hallazgo |
> |---|---|---|
> | 1 | umbral `documentos < 258` | «el filtro de ruido dejó de funcionar» — el corpus había crecido |
> | 2 | señal léxica de obsolescencia | documentos vivos que **hablan** de deprecar puntúan alto |
> | 3 | referencias por nombre de archivo | «73 documentos de canon inerte» |
>
> **Regla que esto deja:** antes de publicar una cifra derivada de una métrica propia, **falsarla
> contra un caso conocido**. `ADR-042` se citaba en decenas de sitios y la métrica decía cero: un
> solo contraste lo habría revelado antes de escribir la conclusión.
>
> Es `ADR-042 §6-bis` —*«falsar el mecanismo antes de culpar al objeto»*— aplicado al instrumento
> de esta auditoría.

## 5 · Lo que este panorama habilita

No una poda. Cuatro preguntas que antes no se podían formular con evidencia — y **ninguna se
responde aquí**:

| # | pregunta | magnitud verificada |
|---|---|---|
| 1 | ¿los **100 rectores de facto** declaran su autoridad, se subordinan, se derivan o pierden esa función? | 100 docs · 40 reglas |
| 2 | de las **472 detecciones de regla**, ¿cuántas son reglas sustantivas **distintas**? ¿cuántas duplican, contradicen o derivan de otra? | requiere `P1` |
| 3 | los **24 huérfanos absolutos** — ¿histórico con valor genealógico, contenido absorbido, o retiro? | 24 docs |
| 4 | **¿por qué el gate de gobernanza tiene un universo distinto del universo documental real?** ¿qué significa «activo» y quién lo determina? | 129 activos vs 276 documentos |

⚠️ La pregunta 2 **no puede responderse con el conteo actual**: `472` son **detecciones léxicas**,
no reglas normalizadas. La unidad de análisis correcta —`P1`— no es el documento sino **la regla
normalizada**, y ahí aplica `DOC-025`: *la misma regla definida dos veces es divergencia latente*.

## 5-bis · Neo4j y Supabase · respuesta a la dirección

> Javo, 2026-09-10: *«recuerde, tenemos Supabase y también Neo4j, que se creó para QUIRA IA como
> última capa conversacional tipo LLM de gestión pública. Si no es viable o si no sirve, me
> avisa.»*

**Sí es viable y sí sirve** — con la precisión que separa lo demostrado de lo supuesto:

> **Neo4j y Supabase no son hipótesis arquitectónicas: su integración y su función prevista están
> demostradas en el sistema. Su estado operativo, contenido y cobertura actuales permanecen
> `NO DETERMINABLES` mientras no exista consulta verificable a las instancias remotas.**

| | **DEMOSTRADO** | **NO DETERMINABLE** |
|---|---|---|
| **Neo4j** | integración en código · múltiples consumidores · loaders Cypher · conectores con fallback · `MISMA_FUENTE_QUE` · artefactos derivados de ejecuciones anteriores · papel arquitectónico para grafo/`MDN` | que la instancia responda hoy · que contenga los nodos y relaciones esperados · que los loaders se hayan ejecutado recientemente · que el grafo corresponda al estado actual del Gold Master · que `QUIRA IA` pueda consultarlo en producción |
| **Supabase** | integración en código · referencias a `normativa_corpus`, `corpus`, `municipality_snapshots` y otras · rutas preparadas para consumirlas · arquitectura que lo contempla como persistencia/origen | contenido actual · cobertura · número de registros · **correspondencia entre `normativa_corpus` y el corpus normativo declarado** · frescura · disponibilidad |

⚠️ `centrality_results.json` (2026-06-02) **demuestra que hubo una ejecución**, no que Neo4j esté
operativo hoy. Y los *114 chunks RDC* conocidos de sesiones anteriores **no entran como evidencia
de este barrido**: no se halló en él el artefacto que los acredita.

⛔ Dos precisiones que quedan blindadas:

- **«Neo4j significa» no implica que Neo4j sea dueño de toda la semántica de QUIRA.**
- **Supabase como repositorio no equivale a autoridad epistemológica ni jurídica.** La autoridad
  jurídica viene del ordenamiento y de la fuente oficial; Supabase es la infraestructura donde
  QUIRA conserva y procesa esa representación.



| | evidencia verificada |
|---|---|
| **Neo4j** | usado por **14+ módulos**: catálogos de `d01`/`d07`/`_template` · `persistencia` · `doctrina.py` · `fondos_matcher` · dos conectores (`neo4j_crdc`, `neo4j_qtmp`) **con fallback declarado** · 7 cypher loaders · `MISMA_FUENTE_QUE` · `compute_centrality` |
| **Supabase** | usado por **14+ módulos** · **7 tablas**: `normativa_corpus` (126 menciones en código) · `corpus` · `municipality_snapshots` · `pdot_indicadores` · `holding_structured_data` · `fondos_convocatorias` · `documents` |

Y el reparto de papeles ya está fijado por el `DEPENDENCY_ATLAS`:

> **«Graphify produce · Gephi explica · Neo4j SIGNIFICA.»** Neo4j es el que porta el significado
> —causalidad, circuitos, dependencias normativas—, y `ADR-038 §9` recomienda montar sobre él el
> **MDN**, el grafo de dependencias normativas de la BRN.

### Lo que NO está construido, y está declarado así en el canon

> `ADR-033:56` — **«QUIRA IA es OTRA capa — la CONVERSACIONAL (arquitectónica · aún por
> construir)»**: el usuario conversa sobre todo lo que hay en QUIRA, **anclado a evidencia e
> índices, sin alucinar**.

    Neo4j + Supabase   →  EXISTEN, integrados, con consumidores
    QUIRA IA           →  la capa que los coronaría · declarada PENDIENTE

No es un olvido ni un abandono: es una capa **decidida y no construida**, igual que la superficie
de QUIRA Ciudadana. La infraestructura que necesitaría **ya está puesta**.

### ⚠️ Y lo que NO se puede afirmar desde aquí

**Estado operativo en vivo: `NO DETERMINABLE`.** No se consultó ninguna de las dos bases —son
remotas y requieren credenciales que no se manipulan—. Lo verificado es **integración en código**,
no que las bases respondan hoy ni qué volumen contienen. La única señal de ejecución hallada es
`data/centrality_results.json`, del **2026-06-02**: análisis de grafo ejecutado hace tres meses.

> Verificar que responden, con qué datos y con qué cobertura, **exige conexión** y queda
> explícitamente fuera de este registro.

## 5-ter · `P1` · NO SE EJECUTÓ COMO SE PLANEÓ — y el motivo es el hallazgo

`P1` debía normalizar «472 reglas». **Dos cosas lo impidieron, y ambas son resultado.**

### 1 · El conteo de 472 era del instrumento, no del corpus

| medición | qué contaba | resultado |
|---|---|---|
| primera | `**Regla…**` **+ listas numeradas en negrita** | 472 |
| segunda | sólo declaraciones explícitas de regla | **89** |

Las listas numeradas en negrita **no son declaraciones de regla**. Es el **cuarto fallo de
instrumento** de esta auditoría, y confirma la advertencia del asesor: *472 detecciones ≠ 472
reglas*.

### 2 · El detector falló la validación · 3 de 5 casos conocidos

Aplicando la regla —*validar contra casos conocidos antes de publicar el agregado*— **no se
publica agregado**:

| caso conocido | forma real en que vive | ¿capturado? |
|---|---|---|
| `Regla de Oro 1` · Excel = Estado | lista numerada en `CLAUDE.md` | ⛔ no |
| `ADR-042 §6-quinquies` | **encabezado de sección** | ⛔ no |
| `DOC-035` | entrada en **`doctrina.py`** (fuera del universo documental) | ⛔ no |
| `BRN` invariantes `I1-I8` | tabla | ✅ sí |
| «Regla de oro del plano» BRN | negrita | ✅ sí |

> **Las reglas de QUIRA no tienen forma sintáctica única.** Viven como listas numeradas,
> encabezados, tablas, blockquotes, entradas de Python y texto con `⛔`. **Ninguna detección
> léxica puede inventariarlas**, y forzar una sería repetir el error que `DOC-035` prohíbe.

### ★★ Y entonces apareció lo que hacía innecesaria la pregunta

> **`app/agents/doctrina.py` ES el registro canónico de reglas: 37 entradas (`DOC-001`…`DOC-037`),
> las 37 con verificador declarado.**

Y `BOOT` fija el **criterio de admisión**, que ya existía:

> *«doctrina → `doctrina.py` · **con verificador cambia de custodio; sin él, se queda aquí**.»*

    regla CON verificador   →  migra a doctrina.py · custodia GATE
    regla SIN verificador   →  permanece donde está

Luego la pregunta de `P1` estaba mal planteada. No es *«¿cómo normalizo las detecciones?»* sino:

> **¿Qué formulaciones dispersas merecen un verificador y, por tanto, la migración al registro
> que ya existe para ellas?**

Eso **no es un problema de script: es una decisión de gobernanza**, una por una, y el criterio
—tener prueba que la vigile— ya está escrito.

### Lo que `P1` sí deja

| | |
|---|---|
| **capa A · evidencia bruta** | 89 ocurrencias con documento, línea, fragmento y marcas de contexto (histórica · negación · condicional · referencial · ejemplo) — **preservada, nada destruido** |
| **capa B · normalización** | ⛔ **no producida.** El instrumento no supera la validación y el corpus no tiene forma canónica |
| **el registro que sí existe** | `doctrina.py` · 37 reglas · 37 verificadores · custodia `GATE` |

⚠️ De las 89 ocurrencias: **16 con marca histórica** · **26 con negación** · **25 condicionales**
· **23 referenciales**. Ninguna de esas categorías equivale a «regla vigente», y por eso ni
siquiera las 89 son un inventario: son **candidatas a examen**.

## 5-quater · `P1.1` · EL RÉGIMEN DE CUSTODIA DE REGLAS

> ⛔ **Corrección de partida:** `doctrina.py` es el registro canónico de **reglas verificadas**.
> Que `BOOT` diga *«con verificador cambia de custodio»* es un **criterio de migración**, no una
> demostración de que toda regla vigente ya esté allí. Lo que sigue reconcilia cuatro universos
> **sin migrar, sin elevar y sin tocar código**.

### `U1` · `doctrina.py` — 37 reglas

| | |
|---|---|
| entradas | **37** (`DOC-001`…`DOC-037`) |
| con verificador declarado | **37** |
| **verificadores que NO existen en `tests/`** | **0** ✅ |

> **El eje de verificación está sano: ninguna regla de `doctrina.py` promete una prueba que no
> exista.**

⚠️ Pero su **procedencia** revela otra cosa:

> **31 de las 37 declaran fuente CONVERSACIONAL, no documental** — *«Javo, 2026-09-06»*, *«el
> colega, 2026-09-05»*… Sólo 6 citan un rector (`ADR`, `PCD`, `.md`, Constitución, `CLAUDE`,
> `BOOT`).

Eso **no es un defecto**: `ADR-035 §5` establece que la IA propone y **el humano valida**, y la
decisión del fundador es fuente legítima de autoridad. Pero fija la función real del artefacto:

> **`doctrina.py` es el mecanismo que convierte decisión conversacional en regla verificada.** Es
> lo que impide que la evolución hablada se pierda — el mismo problema que
> `GM-OMEGA_GENEALOGIA_DOCUMENTAL` registró como *«no hay documento: la evolución fue
> conversacional»*.

### `U4` · Gates — 14 reglas ejecutables

| gate | autoridad citada |
|---|---|
| `check_captura_dpe` · `check_corridas` · `check_errores_silenciosos` · `check_estados_captura` | `ADR-042` |
| `check_consistencia` | `ADR-041` · `ADR-042` · `D-004` · `D-007` · `PCD-D07` |
| `check_extraccion` | `ADR-042` · `D-004` · `D-007` · `OBS-027` |
| `check_sat_brn` | `ADR-038` · `OBS-022` · `RO-VIII-003` |
| `check_portabilidad` | `D-004` · `OBS-032` |
| `check_health` | `D-015` |
| `smoke_cajones` | `ADR-041` |
| **`check_credenciales` · `check_epistemico` · `check_sistema_visual` · `registrar_ejecucion`** | ⛔ **ninguna** |

★ **`ADR-042` gobierna 6 de los 14 gates.** Es el rector operativo real de la capa de adquisición
— el mismo que una métrica defectuosa de este arqueo clasificó como «canon inerte» horas antes.

⚠️ Los **4 sin ID citado no son reglas huérfanas**: declaran su origen **en prosa** dentro de su
propio docstring —un incidente real de credenciales el 2026-08-06, el cierre epistemológico de
`d01`, el mínimo WCAG de contraste, la división productor/lector—. Lo que les falta no es
fundamento: es **identificador citable**.

### Las relaciones entre universos

| relación | estado |
|---|---|
| `U1 ∩ U4` | **1 verificada** — `check_health` cita `D-015`; el resto de gates cita ADR/OBS/PCD, no `DOC-*` |
| `U1 − U2` | **31 de 37** — reglas verificadas cuya autoridad es conversacional, no documental |
| `U2 − U1` | ⬜ **no medible con este instrumento** — las reglas del canon no tienen forma sintáctica única (`P1`) |
| `U3 − U1` | ⬜ **no concluible** — las 89 son candidatas textuales, no reglas |
| `U4 − U1 − U2` | **4 gates** con fundamento en prosa y sin identificador |

### ★ Lo que `P1.1` deja demostrado

> **QUIRA tiene al menos TRES regímenes de custodia de reglas, y son distintos por naturaleza,
> no por descuido:**
>
> | régimen | dónde | cómo acredita | verificación |
> |---|---|---|---|
> | **doctrinal** | `doctrina.py` | 37 entradas con fuente y `por_que_ahi` | **prueba por regla** |
> | **normativo** | `CNO`/`RO` en `docs/brn` | SHA al corpus jurídico · estado propio | invariantes `I1-I8` |
> | **ejecutable** | `scripts/ci/check_*` | cita `ADR`/`OBS`/`D` o funda en prosa | el propio gate |
>
> **No deben forzarse a un mismo esquema de `frontmatter`.** La pregunta correcta no es *«¿tiene
> frontmatter?»* sino: **¿cada clase de artefacto tiene un contrato de autoridad explícito y
> verificable adecuado a su naturaleza?** Para estos tres, la respuesta es **sí**.

### Y la regla que esta fase congela

> **Un detector puede descubrir candidatos; sólo la cadena de autoridad, contexto, evidencia y
> verificación convierte un candidato en regla gobernante.**

## 5-quinquies · `P2/P3` · AUTORIDAD, CUSTODIA, VERIFICACIÓN Y EJECUCIÓN

> ⛔ **Corrección de partida, y es sobre lo que este mismo registro afirmó.** `P1.1` cerró
> diciendo: *«¿cada clase de artefacto tiene un contrato de autoridad explícito y verificable
> adecuado a su naturaleza? Para estos tres, la respuesta es sí.»* **Esa frase generalizaba un
> subconjunto inspeccionado.** Se restringe a: *«para el subconjunto inspeccionado se demostró la
> existencia de contratos diferenciados; su cobertura sobre el universo completo no estaba
> medida.»* `P2/P3` la mide.

### La distinción que hace posible medir — cuatro preguntas, no una

«Autoridad» no es una propiedad: son **cuatro preguntas independientes**, y confundirlas es lo que
produjo los hallazgos falsos de `P0` y `P1`.

| Pregunta | Qué determina | Puede estar sana mientras otra falla |
|---|---|---|
| **¿Quién autoriza?** | autoridad | ✅ |
| **¿Dónde reside?** | custodia | ✅ |
| **¿Cómo se verifica?** | mecanismo de verificación | ✅ |
| **¿Dónde se ejecuta?** | implementación efectiva | ✅ |

Una regla puede tener **autoridad** en una decisión humana validada, **custodia** en `doctrina.py`,
**verificación** en un `verificador`, y **ejecución** en un gate — sin que ninguna de las cuatro
tenga por qué compartir forma documental con las otras. *(Formulación del colega · 2026-09-12.)*

### La matriz de reconciliación · los tres regímenes contra las cuatro preguntas

| | **doctrinal** | **normativo** | **ejecutable** |
|---|---|---|---|
| **¿Quién autoriza?** | decisión humana validada · `ADR-035 §5` — **31/37 fuente conversacional**, 6/37 cita un rector | corpus jurídico vía `CNO` — **107 eslabones con SHA** | `ADR`/`OBS`/`D` citado en **10/14**; fundamento en prosa en **4/14** |
| **¿Dónde reside?** | `doctrina.py` · **37** entradas | `docs/brn/*.yaml` · **16 CNO + 13 RO** | `scripts/ci/` · **14** archivos |
| **¿Cómo se verifica?** | verificador por regla · **37/37 existen**, 0 inexistentes | `I5` **13/13** ✅ · `Regla 3` **16/16** ✅ | el propio gate, con **tres estados** |
| **¿Dónde se ejecuta?** | `pytest tests/` en CI ✅ | `test_brn_lector` + gate `check_sat_brn` en CI ✅ | CI en bucle · **12/14** |
| **Forma del contrato** | entrada Python con `fuente` y `por_que_ahi` | **YAML nativo** con `authority:` | docstring + `exit code` |

### ★ El hallazgo que corrige `P1.1` — y lo hace por la vía contraria a la esperada

**No apareció un régimen roto. Apareció que el instrumento con que se miden los regímenes
pertenece a uno solo de ellos.**

Al medir «documentos sin frontmatter» el detector reportó **31 archivos de `docs/brn` sin
autoridad declarada**. Es falso: **29 de los 30 YAML de la BRN declaran `authority:`** — como
**YAML nativo**, sin los delimitadores `---` del frontmatter markdown. El detector exigía
`startswith("---")`.

> **Aplicar el instrumento del régimen documental al régimen normativo fabrica un hueco que no
> existe.** Es la demostración empírica de por qué no deben forzarse a un mismo esquema: no es una
> preferencia de estilo, es que **la medición cruzada produce falsos positivos**.

Cifra corregida: **133 artefactos declaran autoridad** (104 por frontmatter + 29 por YAML), no 104.

### `A` · Autoridad DECLARADA — el árbol está bien formado

| | |
|---|---|
| `authority.parent` distintos | **13** |
| **que resuelven a un artefacto real** | **13 / 13** ✅ — cero huérfanos |
| raíz del árbol | `identity/CONSTITUCION_INSTITUCIONAL.md` · `parent: null` **declarado**, no omitido |
| concentración | **76 de 104** cuelgan de `GOVERNANCE-001` → `governance/GOVERNANCE_CHARTER.md` |

⚠️ Matiz: 4 de los 13 padres resuelven **por nombre de archivo**, no por `id:` declarado
(`ADR-023`, `ADR-051`, `PROTOCOLO_CURACION_DOMINIO`, `REARQUITECTURA_QUIRA`). El eslabón se
sostiene por convención de nombre, que es más débil que un identificador declarado.

### `B` · Autoridad EFECTIVA — quién gobierna de hecho

| entrantes | documento | ¿nombrado en el Index? |
|---:|---|---|
| **52** | `ADR-035` · Biblioteca de Reglas Normativas (BRN) | ⛔ **no** |
| 31 | `ADR-023` · Arquitectura de tres niveles | ⛔ no |
| 20 | `ADR-024` · Radar Nacional | ✅ sí |
| 20 | `ADR-042` · Consola de Monitoreo | ⛔ no |
| 17 | `ADR-038` · Cadenas Normativas Operativas | ⛔ no |

> **`ADR-035` es el documento más citado de todo QUIRA — 52 referencias entrantes — y no aparece
> nominalmente en la tabla de autoridad.**

⚠️ **Límite declarado:** 2 stems colisionan (`QUIRA_STATE`, `README`) y su conteo **no es
atribuible**. Verificado que **no son duplicados**: `governance/QUIRA_STATE.md` 637 b ·
`docs/corpus_externo/QUIRA_STATE.md` 17.204 b, SHA distintos. Son 4 documentos afectados de 276.

### `C` · Autoridad REGISTRADA — `MASTER_INDEX` contra la realidad

**Lo que está sano:**

```
rutas citadas por el Index que resuelven en disco …… 28 / 28   ✅
```

Ninguna ruta rota. *(Tres se dieron por ausentes en la primera pasada: estaban citadas por
nombre corto heredando la ruta del vecino. Existen las tres.)*

**Los dos defectos, y son distintos:**

| defecto | naturaleza |
|---|---|
| 3 citas por nombre sin ruta | el Index **no es auditable por máquina** hoy |
| **cero filas para la BRN** | hueco de **registro de autoridad** |

`BRN` aparece 5 veces en el Index — **siempre como atributo de un dominio** (*«cadena BRN»*,
*«familia BRN CNO-VIII»*), **nunca como rector**. No existe la fila que responda *«¿dónde vive la
verdad normativa?»*.

> ★ **Y entonces los dos huecos son el mismo hueco.** `ADR-035` no está en el Index porque **la
> BRN entera no está en el Index**: ni el plano maestro, ni los 16 `CNO`, ni las 13 `RO`, ni los
> invariantes `I1-I8`.

### ★★ Pero la BRN sí está registrada — en el OTRO registro

Antes de llamar a eso un vacío de gobernanza, se verificó `registry/registry.yaml`. **La BRN está
ahí**: `canon_cno` **12** · `canon_ro` **8** — 20 activos normativos, y el gate `check_health`
los verifica:

```
[5/5] Cadena de autoridad (Carta de Gobernanza Art. 1)
      activos registrados : 129
      declaran autoridad  : 129 (100.0%)
      cadena reconstruible: 111 aristas, 0 rotas          ✅
```

> **QUIRA tiene DOS registros de autoridad, con propósitos distintos, y ninguno declara al otro:**
>
> | | `registry/registry.yaml` | `governance/QUIRA_MASTER_INDEX.md` |
> |---|---|---|
> | **qué es** | registro de **activos y cadena de autoridad** | tabla de **routeo humano** |
> | **responde** | *«¿de qué cuelga este artefacto?»* | *«¿dónde vive la verdad de X?»* |
> | **lector** | máquina · gate `check_health [5/5]` | persona, al empezar a trabajar |
> | **cobertura** | 129 activos · 111 aristas · 0 rotas | 33 documentos nombrados |
> | **¿verificado?** | ✅ por gate, en cada CI | ⛔ por nadie |

Esto responde la pregunta que el colega dejó abierta —*«¿el `MASTER_INDEX` ya es la capa que
resuelve esa autoridad?»*— y la respuesta es **más limpia de lo esperado: no, porque esa capa ya
existe y es otra.** El `MASTER_INDEX` nunca fue el registro de autoridad: es el **DNS**, y lo dice
en su primera línea (*«NO explica, NO define, NO interpreta — ROUTEA»*).

**El hueco real, entonces, no es que falte autoridad. Es que el routeo humano no cubre el régimen
normativo**, mientras el registro de máquina sí. Quien llega al proyecto y pregunta *«¿dónde vive
la norma?»* no encuentra respuesta en el sitio donde el canon le manda preguntar.

**Y la cobertura del registro de máquina también es parcial**, medida contra disco:

| clase | registrados | en disco | |
|---|---:|---:|---|
| `canon_cno` | 12 | 16 | faltan 4 |
| `canon_ro` | 8 | 13 | faltan 5 |
| `gate` | 1 | 14 | faltan 13 |

⚠️ Que la cadena esté **0 aristas rotas** acredita **lo registrado**, no el universo — es
literalmente la advertencia que el propio CI imprime: *«un mecanismo de cobertura no es autoridad
sobre su propia cobertura»*. **El registro está íntegro; su cobertura es otra pregunta, y esta es
la primera vez que se mide.**

### `D` · Custodia NORMATIVA — medida por primera vez

| invariante | resultado |
|---|---|
| **`I5`** · toda RO deriva de una CNO | **13 / 13** ✅ |
| **`Regla de Oro 3`** · sin SHA no hay eslabón | **16 / 16** CNO · **107 eslabones** ✅ |

Los `sha256` son **hashes truncados a 12 hex**: identificadores de chunk del corpus vectorizado
— la *«ley vectorizada»* de Supabase. **Trazables por diseño, no verificables desde disco.**

**Y aquí el régimen normativo muestra una capacidad que los otros dos no tienen:**

| estado de la RO | n | qué significa |
|---|---|---|
| `vigente` + CNO `vigente` | **7** | compila al motor |
| `propuesta` | 3 | existe, no gobierna aún (familia `VIII`) |
| **`no_determinable`** | 2 | la regla existe; **no puede evaluarse** |
| **`no_observable`** | 1 | requiere otra fuente, **no otro cálculo** |

> **La BRN es el único régimen que puede decir «esta regla existe y no puede evaluarse».** El
> tercer estado de QUIRA, aplicado a la norma. `doctrina.py` y los gates no tienen esa
> expresividad: una regla ahí está o no está.

### `E` · Custodia EJECUTABLE — y el fallo que casi se publica al revés

Se midió *«¿quién invoca cada gate?»* buscando rutas literales y el resultado fue **8 de 14 sin
ejecutor**. Era falso: el workflow los corre **en un bucle sobre `scripts/ci/check_*.py`**, con la
ruta en una variable.

```
CI ejecuta …… check_health explícito + los 12 check_*.py en bucle + pytest completo
fuera del glob …… registrar_ejecucion.py · smoke_cajones.py
```

> ⛔ **Corregido en `§5-octies` (falsación 16):** `registrar_ejecucion.py` **no es un gate, es un
> productor** — se contó como gate por residir en `scripts/ci/`. Universo real: **13 verificadores
> · 12 en CI · 1 productor.**

★ **Y el bucle implementa los tres estados de QUIRA en la propia infraestructura:**

| exit | tratamiento en CI |
|---|---|
| `0` | verificado |
| **`2`** | *«NO DETERMINABLE — este gate no pudo verificar, y por tanto **NO acredita nada**»* |
| otro | hallazgos · falla |

Con la nota explícita: *«un verde acredita lo inspeccionado, nunca el resto»*. **La doctrina del
tercer estado no vive sólo en el canon: está ejecutada en el CI**, y ningún barrido anterior lo
había registrado.

**El único hueco que sobrevive en este eje:** `registry/registry.yaml` registra **1 de 14** gates
(`GATE-check_health`). No es falta de ejecución — es falta de **registro**.

### Los huecos que sobreviven a la falsación

| # | hueco | naturaleza | tipo |
|---|---|---|---|
| **1** | **el routeo humano no cubre el régimen normativo** — ni la BRN ni `ADR-035` (52 entrantes) tienen fila en el `MASTER_INDEX`, aunque **sí estén** en `registry.yaml` | routeo, no autoridad | `NO_RUTEADA` |
| **2** | **cobertura del registro de máquina**: 12/16 `CNO` · 8/13 `RO` · **1/14** gates | cobertura | `PARCIAL` |
| 3 | 2 gates fuera del glob de CI (`registrar_ejecucion`, `smoke_cajones`) | ejecución | `PARCIAL` |
| 4 | 3 citas del Index no resolubles por máquina | auditabilidad | `FORMA` |
| 5 | 4 padres resueltos por nombre, no por `id:` | fuerza del eslabón | `FORMA` |

**Ninguno es una regla gobernando sin autoridad.** Los cinco son de **registro, routeo y forma**,
no de fundamento.

> ⛔ **Y aquí este registro se corrige a sí mismo antes de que la frase cuaje.** Se escribió: *«no
> se solapan. Son tres poblaciones disjuntas»*, apoyado en `U1 ∩ U4 = 1`. **Esa inferencia no se
> sostiene.** `U1 ∩ U4` mide **co-representación por citación** —cuántas reglas aparecen
> simultáneamente bajo dos criterios de búsqueda—, y de ahí **no se sigue independencia
> ontológica**. Dos reglas pueden gobernar el mismo fenómeno sin citarse jamás.
>
> Es `DOC-033` aplicada a los regímenes en lugar de a los indicadores: *«la identidad o semejanza
> nominal no autoriza a inferir identidad, dependencia, complementariedad ni redundancia»* — y su
> simétrica también vale: **la ausencia de co-citación tampoco autoriza a inferir independencia.**
>
> Lo demostrado se restringe a: **`U1 ∩ U4 = 1` · una sola regla está representada bajo ambos
> criterios** (`check_health` ↔ `D-015`). **Si los tres regímenes tienen relación semántica entre
> sí es una pregunta abierta, y es materia de `P4`.**

### La genealogía del método — que no se borra

```
472 detecciones  →  89 candidatos  →  falsaciones y calibraciones  →  37 reglas verificadas
                                                                   →  reconciliación de regímenes
```

Y en `P2/P3`, **nueve falsaciones del propio instrumento**, todas antes de publicar:

| # | lo que el instrumento dijo | lo que era |
|---|---|---|
| 6 | 3 rutas del Index rotas | existían las tres · citadas por nombre corto |
| 7 | 13 RO con CNO inexistente | **13/13 correctas** · comparación invertida |
| 8 | 0/16 CNO con SHA | **16/16** · el SHA es de 12 hex, no 64 |
| 9 | 8 gates sin ejecutor | **12/14 corren en CI** · el bucle usa variable |
| 10 | 31 YAML de BRN sin autoridad | **29/30 la declaran** · en YAML nativo |
| 11 | «la BRN no está registrada» | **`registry.yaml` registra 20 activos normativos** · existe un segundo registro |

> Seis de seis habrían sido **hallazgos graves y falsos**. La `9` habría afirmado lo contrario de
> la verdad; la `11` habría acusado de vacío de gobernanza a un régimen que **tiene su propio
> registro verificado por gate**. **El instrumento de auditoría es, sistemáticamente, la fuente
> de error más probable de esta auditoría** — ya es la conclusión metodológica más repetida del
> barrido, y la única que no ha fallado ninguna vez.
>
> ⛔ Y el patrón tiene una forma constante: **cada falso hallazgo nació de buscar una cosa en la
> forma de otra** — la ruta literal cuando estaba en una variable, el hash de 64 cuando era de 12,
> el frontmatter markdown cuando era YAML nativo, un registro cuando había dos. **No falló la
> búsqueda: falló la suposición sobre la forma.**

### 📌 Criterio transversal que estas once falsaciones producen

> **La ausencia de una forma esperada no demuestra la ausencia de la función.**
>
> Inspeccionar un término, un patrón, un `frontmatter`, un hash de cierta longitud o una llamada
> literal autoriza a concluir ausencia **únicamente respecto de esa representación**. La función
> puede existir bajo otra forma, en otro registro o en otro régimen.

*(Formulación del colega · 2026-09-12. Es el equivalente documental de `DOC-035`, que gobierna el
alcance de búsqueda. **Se registra aquí, NO se eleva a `doctrina.py`:** `P4` observa y clasifica;
`P5` decide. Queda propuesta como candidata doctrinal con verificador pendiente.)*

### Condición de salida hacia `Q-M2-C`

> **No se avanza hasta poder explicar, de cualquier regla: quién la autoriza, dónde reside, cómo
> se verifica y dónde se ejecuta — sin exigir que los tres regímenes adopten la misma forma
> documental.** Con `P2/P3` esa condición se cumple para los tres. Queda pendiente **`P4`**
> (obsolescencia y conflictos semánticos) y **`P5`** (decisiones de gobernanza), donde se resuelve
> el hueco `1`.

## 5-sexies · `P4` · SEMÁNTICA, CONTINUIDAD Y CONFLICTO

> 🔒 **Congelamiento vigente durante toda esta fase** (instrucción del colega · 2026-09-12): **no
> se modifica `doctrina.py`, `registry.yaml`, la BRN, el `MASTER_INDEX`, los gates ni los
> workflows como consecuencia de `P4`. P4 observa y clasifica; `P5` decide.**

### ★★ Y por segunda vez, lo que `P4` iba a construir YA EXISTE

`P1` se detuvo al descubrir que el registro canónico de reglas ya existía. **`P4` se detiene
igual:** la taxonomía semántica está escrita desde antes, en `CARTA_REARQUITECTURA_QUIRA §2`.

| | Categoría | Qué es | Qué se hace |
|---|---|---|---|
| 🏛️ | **HISTÓRICO** | existió y ya no opera | se PRESERVA — nunca se borra |
| ⚖️ | **NORMATIVO VIGENTE** | lo fija una norma en vigor | se ACATA mientras rija |
| 🔬 | **EMPÍRICAMENTE ÚTIL** | funciona y hay evidencia de ello | se CONSERVA si supera validación |
| 🔧 | **DECISIÓN DE DISEÑO ANTIGUA** | se eligió, no se dedujo | queda ABIERTA a rediseño |
| 📜 | **SUPERADO METODOLÓGICAMENTE** | fue correcto y el conocimiento lo desplazó | ANTECEDENTE, no regla |

Con diez reglas de refactor, cada una anclada a doctrina (`DOC-013`, `DOC-014`, `DOC-015`,
`DOC-016`, `DOC-027`, `DOC-028`, Reglas de Oro 2·7·8·9).

### Y la Carta es más fina que la lista propuesta, en el punto decisivo

> ### ⚠️ `NO_DETERMINADO` **no es una sexta categoría. Es un estado de evidencia transversal.**
> *«Una pieza tiene **categoría** y **estado** a la vez.»*

| Pieza | Categoría | Estado de evidencia |
|---|---|---|
| `Constitución Art. 233` | ⚖️ normativo vigente | ✅ fuente primaria localizada |
| peso `C_i = 0,20` | 🔧 decisión de diseño | ❓ justificación no determinada |

**La lista de nueve estados propuesta para `P4` pone `NO_DETERMINABLE` como una etiqueta más, al
lado de `VIGENTE` y `HISTÓRICO`. Eso colapsa dos ejes en uno** — exactamente el error que `P2/P3`
acaba de corregir al separar autoridad · custodia · verificación · ejecución. **La Carta ya lo
había separado**, y además cierra el silogismo que la fusión habilita:

> *«Sin esta separación, el refactor derivaría al silogismo falso: «no está justificado → se puede
> quitar». `DOC-027` lo prohíbe.»*

**Lo que sí falta en la Carta**, y es la contribución real de la propuesta: `TRANSMUTADO`,
`OPERACIONAL`, `EXPLICATIVO`, `CONFLICTIVO`, `VIGENTE DERIVADO`. Y hay un motivo de alcance:
**la Carta clasifica CONSTRUCTOS del modelo analítico** (`C_i`, `V_i`, pesos, escala `AVEP`),
**no artefactos documentales.** Aplicarla a documentos es una extensión, no una lectura.

### `PASO 1` · Lo que cada artefacto declara de sí mismo

```
universo …………… 276          declaran estado …… 147          no declaran …… 129
```

> ⛔ **Cifra corregida en `§5-septies`: son 141 y 135.** Seis de los 147 se leyeron de bloques de
> ejemplo citados dentro del documento, no de su cabecera.

En **cuatro formas distintas** — 73 en línea de negrita · 50 `frontmatter estado` · 23
`frontmatter status` · 1 en tabla. **Y en cuatro vocabularios que corresponden a regímenes
distintos:**

| vocabulario | ejemplos | régimen |
|---|---|---|
| **deliberativo** | `RATIFICADO` · `APROBADO` · `Aceptado` · `CONGELADO` | canon (ADR/PCD) |
| **normativo** | `vigente` · `propuesta` · `no_determinable` · `no_observable` | BRN |
| **epistémico** | `CONFIRMED` · `SUPPORTED` · `STRONGLY_SUPPORTED` | observaciones e hipótesis |
| **operativo** | `ABIERTO` · `CERRADO` · `EJECUTADO` · `PENDIENTE` | expedientes y registros |

> ★ **`P1.1` encontró tres regímenes de custodia de REGLAS. `P4` encuentra cuatro vocabularios de
> ESTADO, y no son los mismos tres.** El **epistémico** —`CONFIRMED`/`SUPPORTED`/
> `STRONGLY_SUPPORTED`— no había aparecido en ningún barrido previo, y no es descuido: la
> **Regla de Oro 10** lo ordena — *«no congelar teoría antes que el grafo hable: `ADR-019` sigue
> `STRONGLY_SUPPORTED` a propósito»*. **Un estado que se conserva deliberadamente incompleto es
> una capacidad, no una deuda.**

### `PRUEBA 1` · Sustitución — y el mecanismo real de QUIRA

Barrido de **14 familias léxicas** sobre 276 `.md` + 30 `.yaml`:

```
850  ocurrencias con señal de sustitución, en 191 documentos
 39  nombran al menos un identificador
  3  nombran dos o más en la misma línea      ← y ninguna de las 3 es una sustitución
```

Con eso se concluyó «cero pares demostrados». **Era falso, y es la falsación 12.** El instrumento
exigía dos identificadores en una línea; **QUIRA no sustituye así.**

> ★ **QUIRA sustituye POR SECCIÓN, y lo declara en AMBOS extremos, con acuse.**

| A · queda superado | → | B · supera | dónde lo declara A | dónde lo declara B |
|---|---|---|---|---|
| `ADR-024 §Capa C` | → | `ADR-044` | `ADR-024:15,19` | `ADR-044:116` ✅ al sellar |
| `ADR-043 §2` fila Adquisición | → | `ADR-045` | `ADR-043:15` | `ADR-045:209` ⏳ al sellar |
| `ADR-045 §10` cláusula del nombre | → | `ADR-046` | — | `ADR-046:105,178` |
| `ARQUITECTURA_CANONICA §SaaS` | → | `ADR-024` + `BOOT §TESIS` | `ARQUITECTURA_CANONICA:48` | — |

**Ningún documento de canon ha sido sustituido entero.** Lo que se supera es **una sección
nombrada**, el resto sigue vigente y el propio documento lo dice arriba: *«el resto de este
documento sigue vigente»*. Y el que supera **lo registra en su tabla de cierre con casilla de
verificación**. Eso es un protocolo, no una costumbre — y ningún barrido lo había descrito.

⚠️ **Las 850 señales restantes hablan del OBJETO, no del canon**: ordenanzas derogadas, normas
reformadas, datos migrados. Es el límite ya declarado en `§4`, ahora **medido**: de 850 señales
léxicas de obsolescencia, **las que tocan al canon son 4**.

### `PRUEBA 3` · Continuidad funcional — el caso `d04`

**Declaración:** `ADR-035:14` y `§3` — *«el **DOM de Alertas Institucionales NO se elimina —
TRANSMUTA en la BRN**»* (Javo · 2026-07-15). No es interpretación: es literal.

**Función que sobrevivió**, verificada por mecanismo y no por nombre:

```
ANTES  tablero de alertas sueltas, generadas por reglas escritas en el sistema
AHORA  SAT derivada de RO derivada de CNO derivada del corpus, con SHA por eslabón
```

`ADR-035:99` lo formula así: *«se cataloga su artículo, se valida su regla, y el SAT aparece»*.
Custodio actual: gate `check_sat_brn`, que cita `ADR-038` · `OBS-022` · `RO-VIII-003`.

> ⛔ **Y aquí este registro se corrige otra vez.** Se escribió *«la función alertar sobre
> incumplimiento normativo sobrevive como SAT»*. **Eso afirma identidad, y sólo se demostró
> continuidad.** Enunciado correcto:
>
> ### **Se demostró continuidad funcional de la detección y señalamiento normativo mediante la cadena `CNO → RO → SAT`. NO se demostró que el mecanismo actual sea semánticamente idéntico al antiguo `d04`.**
>
> **`continuidad funcional ≠ identidad funcional completa`.** El `d04` original pudo tener
> presentación, semáforos, eventos, priorización, interfaz y lógica institucional propias; lo
> verificado es que **una** función nuclear —que la señal derive de norma— vive hoy en la cadena
> BRN. **Qué más tenía `d04` y si algo de eso no tiene sucesor es una pregunta abierta**, y
> responderla exige el inventario del `d04` histórico, que este barrido no hizo.
>
> Por tanto **no se dice «`d04` vive en la BRN»**, sino: **una función demostrable del antiguo
> `d04` transmutó hacia la arquitectura normativa `BRN/SAT`.**

> **En lo demostrado: 📜 SUPERADO METODOLÓGICAMENTE en su forma · ⚖️ NORMATIVO VIGENTE en la
> función que se pudo rastrear.** Ninguna etiqueta sola lo describe — por eso `TRANSMUTADO` hace
> falta; y `TRANSMUTADO` **no significa «equivalente»**, significa «hay continuidad demostrada de
> al menos una función, bajo otra forma».

### ⛔ Y la trampa en la que `P4` iba a caer — el canon ya la había cerrado

`app/agents/canon.py:299`:

> *«El CNO se alcanza por la RO que deriva de él: **el vínculo lo declara el canon, no se infiere
> del numeral romano (`CNO-IV` es `d02`, no `d04`)**.»*

Contar la familia `CNO-IV` como evidencia de que `d04` sigue vivo habría sido exactamente
`DOC-033` —*la semejanza nominal no autoriza a inferir pertenencia ontológica*— cometida sobre
numerales. **El código lo previó y lo dejó escrito en un comentario.** Es la tercera vez en esta
auditoría que la respuesta ya estaba escrita antes de que la pregunta se formulara.

### Casos abiertos que `P4` deja identificados, sin clasificar

| caso | evidencia | por qué no se clasifica aquí |
|---|---|---|
| **`docs/corpus_externo/` · 3 docs `Alpha 0.9 — fundacional pre-Neo4j`** | `QUIRA_CAUSAL_MODEL_v1.0` tiene **13 referencias entrantes**, más que muchos `ADR` vigentes | autodeclaran anterioridad a la arquitectura actual **y** siguen siendo citados: `HISTÓRICO` y `EFECTIVO` a la vez. Requiere la prueba de continuidad, no una etiqueta |
| **`ADR-040` `⛔ REVERTIDO`** | se autodeclara falso; `CNO-VII-001` lo cita como escarmiento que *«bloqueó el Catálogo 26 días»* | un artefacto **revertido como regla** y **vivo como antecedente citado por norma vigente** |
| ~~**`DESCUBRIMIENTO_NORMATIVO_ADR031` `NO_VIGENTE`**~~ | ⛔ **falso — ver `§5-septies`**: el `NO_VIGENTE` estaba en un bloque de ejemplo | el documento **no declara estado**; el caso se disuelve |
| **`ADR-019` `STRONGLY_SUPPORTED` · `ADR-022` `SUPPORTED`** | `Regla de Oro 10` los mantiene así **a propósito** | ⛔ **no son deuda.** Clasificarlos como incompletos sería romper la regla que los protege |
| **`OBS-012` · «BRN con SHA256 obsoletos»** | título declara obsolescencia en la cadena normativa | toca la `Regla de Oro 3`; se examina con la BRN delante, no por su título |
| **129 documentos sin estado declarado** | 59 en `docs/architecture`, mayoría volcados del Gold Master | **son datos, no normas.** Exigirles estado sería el error de forma otra vez |

### Lo que `P4` deja demostrado

1. **La taxonomía existe** (`Carta §2`), y separa **categoría × estado de evidencia** — un eje que la propuesta de nueve etiquetas habría vuelto a colapsar.
2. **Hay un cuarto vocabulario de estado, el epistémico**, y expresa una capacidad deliberada.
3. **La sustitución en QUIRA es por sección, bidireccional y con acuse.** Cuatro casos, todos íntegros.
4. **`d04` TRANSMUTÓ**, con función demostrable y custodio actual — no se infirió del nombre.
5. **De 850 señales léxicas de obsolescencia, 4 tocan al canon.** El resto habla del objeto observado.

### Lo que `P4` NO resolvió, y queda para `P5`

- La **`PRUEBA 2` de conflicto** (fenómeno · unidad · condición · temporalidad · función) **no se ejecutó**: requiere pares candidatos, y ningún instrumento léxico puede proponerlos sin repetir el error de `IFE`/`IEF` que `DOC-033` registra. **Se declara no ejecutada, no vacía.**
- La **extensión de la taxonomía a artefactos documentales** (`TRANSMUTADO`, `OPERACIONAL`, `EXPLICATIVO`, `CONFLICTIVO`, `VIGENTE DERIVADO`) es **decisión de gobernanza**, no medición.
- Los **seis casos abiertos** de arriba.
- El **hueco 1 de `P2/P3`** — la BRN sin fila de routeo.

## 5-septies · `P4` · CIERRE — `PRUEBA 2` ejecutada y los seis casos clasificados

> Instrucción del colega · 2026-09-12: *«Completar `P4` únicamente con la Prueba 2 de conflicto y
> la clasificación de los seis casos abiertos. No modificar ningún artefacto congelado. No crear
> nuevas doctrinas, taxonomías ni registros.»* **Se acata literalmente.**

### ⛔ Primero: el `PASO 1` de `P4` estaba mal medido

Se publicó *«147 de 276 declaran estado»*. **Seis de esos 147 no son estados del artefacto: son
valores dentro de un bloque de ejemplo citado por él.**

| documento | lo que se leyó | lo que declara de verdad |
|---|---|---|
| `ADR-016` | `PROPUESTO \| ACTIVO \| CONGELADO \| REVISANDO` | **`CONGELADO v1.0`** — era la enumeración de valores posibles |
| `ADR-017` | `PARCIAL` | **no declara estado** |
| `DESCUBRIMIENTO_NORMATIVO_ADR031` | `NO_VIGENTE` | **no declara estado** — el `NO_VIGENTE` es de un hallazgo hipotético de 2027 |
| `DCO_Dom08` · `BRN_CICLO_VIDA` · `corpus_externo/QUIRA_STATE` | idem | idem |

Es **`DOC-036 PASO 0`**: confundir el contenido citado con la declaración del artefacto — el mismo
defecto que `P1` cometió al contar listas numeradas como reglas.

```
estados declarados …… 141   (no 147)          no declaran …… 135   (no 129)
```

⚠️ Y el verificador de esa falsación **también falló**: marcó 30 `.yaml` de la BRN como
sospechosos por no tener el `estado:` en los primeros 400 bytes. **No son sospechosos.** Es YAML
nativo, cuyo cuerpo empieza tras el bloque de comentarios. **Tercera vez en esta sola fase que se
aplica el criterio de forma del régimen documental al régimen normativo.**

### `PRUEBA 2` · CONFLICTO SEMÁNTICO — ejecutada, acotada

No se buscó *«documentos que se contradicen»* (trampa `IFE`/`IEF` · `DOC-033`). Se buscó **una
sola clase de candidato objetivo: un mismo indicador publicado con valores distintos**, sobre 13
indicadores de alta consecuencia.

⚠️ **El primer instrumento se descartó entero (falsación 13):** tomaba el primer número tras el
nombre del indicador, y devolvía `SITA → 07` (era `d07`), `ICPI → 12` (era `H12`), `→ 5.5` (era
`v5.5`). **Ningún resultado suyo se usó.** Se rehízo exigiendo **forma de métrica publicada**
—decimal de cuatro cifras—, que no colisiona con identificadores.

**Candidato hallado, y es el de máxima consecuencia del proyecto:** `SITA 2025`, con **dos valores
en artefactos vigentes, cada uno con su prueba**.

| par | ¿mismo fenómeno? | ¿misma unidad? | ¿misma condición? | ¿misma temporalidad? | veredicto |
|---|---|---|---|---|---|
| `0,9719` ↔ `0,4630` | sí | sí | ⛔ **NO — 21 CD vs 24 CD** | sí | **no hay conflicto: dos universos.** Y el alto es inválido: midió *encontrados*, no *exigibles* |
| `0,4646` ↔ `0,4448` | sí | sí | ⛔ **NO MISMA CONDICIÓN DEMOSTRADA** | ⛔ no | **no hay conflicto semántico demostrado**: corresponden a estados/versiones temporales distintos, y el expediente cita el anterior |
| `0,4630` ↔ `0,4646` | sí | sí | ❓ **NO DETERMINABLE** | ❓ | 🔴 **abierto — y ya registrado** |

> ★ **Las cinco preguntas, aplicadas al caso más consecuente de QUIRA, no producen ningún
> conflicto semántico demostrado.** Disuelven dos pares aparentes y dejan uno sin explicar — que
> **`D-015` ya tenía registrado, con su ataque, desde el 2026-09-09**: *«`0,4630` equivale a
> `0,4646` … 🔴 NO DEMOSTRADO»*.

> ### ⛔ Y `P4` NO cierra `D-015`.
>
> **Lo que `P4` puede afirmar:** *no hay conflicto semántico demostrado entre `0,4646` y `0,4448`.*
> **Lo que `P4` NO puede afirmar:** *que la transición `0,4646 → 0,4448` esté reconciliada.*
>
> Lo acreditado es la **modificación del expediente y del criterio**, no la **reproducción
> computacional de ambos estados**. `D-015` sigue abierta exactamente donde estaba: *«tiene corrida
> sellada que lo reproduzca — **PENDIENTE**»*. **Una fase de diagnóstico no puede cerrar una deuda
> de reproducción por el camino de no haber hallado un conflicto.**

**Y `D-015` es más precisa de lo que este barrido habría sido**, porque separa dos propiedades que
un detector habría colapsado: *existe el valor* `DEMOSTRADO` · *tiene procedencia documental*
`DEMOSTRADO (76ca5de)` · *tiene corrida sellada que lo reproduzca* **`PENDIENTE`**.

**El único conflicto interno de estado documentado en QUIRA** —`ADR-041`, frontmatter `APROBADO`
contra pie *«propuesta, sin sellar»*— **fue detectado y corregido el 2026-08-26**, y la corrección
está escrita dentro del propio documento (`ADR-041:263`).

> **Resultado de la `PRUEBA 2`: cero conflictos semánticos nuevos. Uno abierto, ya registrado como
> deuda. Uno cerrado hace tres semanas. `P4` queda completo en este eje.**

### Los seis casos, clasificados por las cuatro preguntas

| caso | ¿gobierna? | ¿sirve hoy? | ¿explica el origen? | ¿se usa de hecho? | clasificación |
|---|---|---|---|---|---|
| **`corpus_externo` · 3 docs `Alpha 0.9`** | ⛔ no — el `Index` rutea la causalidad a Neo4j + Constitución Ontológica | ✅ sí — fuente del concepto `C10` | ✅ sí — corpus fundacional | ⚠️ **bajo**: 11 de 13 citas son internas a su propio cuerpo | 🏛️ **HISTÓRICO · alta utilidad explicativa · sin autoridad actual** |
| **`ADR-040` `⛔ REVERTIDO`** | ⛔ no — revertido por la fuente primaria | ✅ sí | ✅ sí | ✅ **sí — `CNO-VII-001` lo cita como escarmiento** | 🏛️ **HISTÓRICO con función explicativa ACTIVA, citada por norma vigente** |
| **`DESCUBRIMIENTO_NORMATIVO_ADR031`** | — | — | — | — | ⛔ **el caso se DISUELVE.** No es `NO_VIGENTE`; `AUTORIDAD_PROPOSICIONES:292` lo trataba como vigente y **tenía razón**. Instrumentación de `C10`, *bloqueada por `R-E`* |
| **`ADR-019` `STRONGLY_SUPPORTED` · `ADR-022` `SUPPORTED`** | ✅ sí | ✅ sí | — | ✅ sí | ⚖️ **VIGENTE con estado epistémico deliberado.** ⛔ **No es deuda:** `Regla de Oro 10` los mantiene así a propósito |
| **`OBS-012` «SHA256 obsoletos»** | — | — | ✅ sí | — | ✅ **RESUELTO el mismo día (2026-07-23)**, con propagación documentada a 4 artefactos. **El título describe el hallazgo, no un pendiente** — clasificar por título habría sido el error |
| **135 sin estado declarado** *(agregado, no caso individual)* | ❓ | ❓ | ❓ | ❓ | ⛔ **NO CLASIFICABLE con esta evidencia.** Lo demostrado: *no presentan estado en el régimen de metadatos inspeccionado*. **Eso no autoriza a llamarlos datos** — ver recuadro |

> ### ⛔ Y aquí el informe estuvo a punto de cometer el error que acaba de documentar
>
> Se escribió *«135 documentos sin estado = **datos, no normas**»*. **Ese salto es exactamente el
> patrón que `P4` descubrió**: concluir la naturaleza de un artefacto a partir de la ausencia de
> una representación esperada. Un documento sin estado declarado puede ser dato, corpus externo,
> artefacto histórico, material explicativo, instrumento, documentación auxiliar **o una pieza
> normativa cuyo régimen expresa el estado de otra manera** — que es precisamente lo que ocurrió
> con los 30 `.yaml` de la BRN en este mismo apartado.
>
> **Enunciado correcto:** *135 artefactos no presentan estado declarado en el régimen de metadatos
> inspeccionado. Su ausencia de estado no autoriza a clasificarlos.* Clasificarlos exige
> inspeccionar su régimen propio, y eso **no se hizo**.

### ⚠️ Y los «seis casos» no son seis piezas homogéneas

La lista mezcla naturalezas distintas, y conviene decirlo para que el informe sea auditable:

| # | caso | qué es | evidencia | clasificación | cierre |
|---|---|---|---|---|---|
| 1 | `corpus_externo` · 3 docs `Alpha 0.9` | **conjunto** de 3 artefactos | 11 de 13 citas son internas al propio cuerpo | 🏛️ histórico · útil · sin autoridad actual | ✅ clasificado |
| 2 | `ADR-040` | **artefacto** único | autodeclarado revertido · citado por `CNO-VII-001` | 🏛️ histórico con función explicativa activa | ✅ clasificado |
| 3 | `DESCUBRIMIENTO_NORMATIVO_ADR031` | **artefacto** único | el `NO_VIGENTE` es de un bloque de ejemplo | ⛔ **el supuesto no se sostiene** | ✅ disuelto |
| 4 | `ADR-019` · `ADR-022` | **dos artefactos**, no uno | `Regla de Oro 10` los sostiene así | ⚖️ vigentes · estado epistémico deliberado | ✅ clasificado — **no es deuda** |
| 5 | `OBS-012` | **artefacto** único | `RESUELTO 2026-07-23`, propagación a 4 artefactos | ✅ resuelto en origen | ✅ cerrado |
| 6 | 135 sin estado | **agregado del barrido**, no un caso | ausencia en un régimen de metadatos | ⛔ **no clasificable con esta evidencia** | ⚠️ **queda abierto** |

**De los cinco casos documentales (1-5), cuatro no eran lo que parecían**: dos se disuelven
(`3`, `5`), uno es capacidad y no deuda (`4`), y uno invierte su lectura (`1`). **El sexto no es
un caso: es un resultado agregado**, y se devuelve a `P5` sin clasificar.

### ⛔ Y una corrección que alcanza a `P2/P3`

El ranking de **autoridad efectiva** publicado en `§5-quinquies B` cuenta referencias entrantes
**sin distinguir cita externa de cohesión interna**. `QUIRA_CAUSAL_MODEL_v1.0` figura con **13
entrantes** — pero **11 provienen de `docs/corpus_externo/` citándose a sí mismo**. No es
autoridad efectiva: es **un cuerpo congelado con alta densidad interna**.

La métrica se publicó bajo el rótulo **«autoridad efectiva»**. Su nombre correcto es otro:

> ### **densidad de referencias entrantes dentro del universo inspeccionado.**

No es lo mismo, y la diferencia importa porque confirma la separación que esta serie viene
sosteniendo: **`uso ≠ autoridad ≠ gobierno ≠ utilidad ≠ vigencia`** — cinco preguntas, otra vez,
donde se estaba usando una sola cifra.

⚠️ **Qué invalida y qué no.** **No invalida `P2/P3`**: las mediciones siguen siendo correctas —
28/28 rutas, 13/13 padres, `I5` 13/13, 12/14 gates en CI, los dos registros. **Invalida
únicamente la lectura semántica de esa cifra.** Para los `ADR` —citados desde todo el
repositorio— el sesgo es previsiblemente menor, **pero no se midió**. Por tanto el ranking de
`§5-quinquies B` se lee como **orden de citación**, no de autoridad: `ADR-035` sigue siendo el más
citado del corpus, y que sea *el que más gobierna* **no está demostrado por esa cifra**.

### `P4` · CERRADO

| eje | estado |
|---|---|
| taxonomía | ✅ **existe** (`Carta §2`) — no se reinventa |
| continuidad (`d04`) | ✅ **continuidad funcional demostrada**, no identidad |
| sustitución | ✅ **por sección, bidireccional, con acuse** — 4 casos íntegros |
| vocabularios de estado | ✅ **cuatro**, uno de ellos deliberadamente incompleto |
| **conflicto** | ✅ **ejecutado** — cero nuevos demostrados · 1 abierto ya registrado · 1 cerrado en origen |
| **casos** | ✅ **5 documentales clasificados** · ⚠️ **1 agregado devuelto sin clasificar** |

**Nada congelado fue modificado. No se creó doctrina, taxonomía ni registro nuevo.**

### El alcance exacto de este cierre

> **`P4` cierra como cierre de la prueba acotada y de la clasificación documental. NO cierra como
> «se demostró que no existen conflictos semánticos en QUIRA».**
>
> Lo demostrado, en su forma falsable: **en el conjunto de candidatos de alta consecuencia
> inspeccionado mediante la `PRUEBA 2`, no apareció ningún conflicto semántico nuevo demostrado.**

Y la frontera del caso `d04`, que conviene dejar tabulada:

| afirmación | estado |
|---|---|
| una función del antiguo `d04` permanece | ✅ **DEMOSTRADO** |
| esa función pasa hoy por `BRN/SAT` | ✅ **DEMOSTRADO** |
| existe continuidad funcional **parcial** | ✅ **DEMOSTRADO** |
| `d04` completo = BRN | ❌ |
| BRN es el nuevo nombre de `d04` | ❌ |
| todo el significado histórico de `d04` sobrevive | ❌ |

**`continuidad funcional ≠ continuidad ontológica ≠ identidad arquitectónica`.**

### La lección, sin el absoluto

El riesgo principal de QUIRA ya no parece ser que falte documentación: **es interpretar
incorrectamente documentación que ya existe.** Las quince falsaciones lo evidencian.

> ⛔ Pero **no todo lo que apareció era un error de lectura.** La primera redacción decía
> *«ninguna encontró un vacío; todas encontraron una lectura equivocada»*, y eso es demasiado
> absoluto: induciría a creer que **todo** problema aparente se disuelve al releer. **No es así.**
>
> **Las falsaciones de `P4` mostraron que varios aparentes vacíos eran errores de representación o
> de lectura contextual. Los casos que sobrevivieron permanecen como cuestiones abiertas, y no
> fueron convertidos artificialmente en conclusiones.**

Lo que sobrevive, y no es poco:

| | |
|---|---|
| `0,4630 ↔ 0,4646` | reconciliación **abierta** (`D-015`) |
| reproducción de `0,4448` | **pendiente** — corrida sellada |
| uso efectivo externo de varios documentos | **menor** de lo que la métrica sugería |
| autoridad por citación | **no demostrada** como gobierno |
| continuidad completa de `d04` | **no demostrada** — sólo una función |
| 135 artefactos | **sin clasificar** |

> **`P4` no modificó el sistema para que la evidencia encajara. Modificó las conclusiones del
> auditor para que encajaran con la evidencia.**

## 5-octies · `P5` · DECISIÓN — y la corrección de marco que la precede

### ★ La dirección corrige el marco antes de decidir · Javo · 2026-09-14

> *«¿Es mi impresión o el colega confunde esta auditoría con el proceso real de refactorización?
> El trabajo real es construir la nueva y mejor versión de QUIRA, con todo lo que se pueda sumar
> para potenciar y elevar el ecosistema. **Todo lo que se revise y deba acogerse para la
> construcción debería anotarse no como deuda, sino para implementar.**»*

**Verificado contra el canon, la corrección es sustancialmente correcta:**

| lo que dice el canon | dónde |
|---|---|
| esto es *«el plan del **refactor integral de fondo y forma de todo el ecosistema**»* | `CARTA_REARQUITECTURA §Qué es` |
| su término es **`GOLD MASTER vNEXT`** — no un informe | `CARTA §8` |
| el vocabulario de salida son **ocho destinos de construcción**, no categorías de déficit | `REARQ_Q-M1:348` |
| *«la máquina propone, **la dirección ratifica**»* — cada pieza lleva `classification_candidate` y `classification_status` | `CARTA §3` |
| ⛔ **el sesgo ya había sido detectado y escrito**: *«`GM-Ω` reconstruyó tanta genealogía que empezó a producir un **sesgo conservador de HECHO**, aunque el canon dijera lo contrario de DERECHO. Javo lo señaló y tiene razón»* | **`DOC-027`** · 2026-09-05 |

> **Lo que Javo percibe no es una impresión: es la reincidencia del sesgo que `DOC-027` ya
> registró.** Y esta serie de registros lo padeció también: `P0–P4` están redactados casi
> enteramente en clave de **hueco, falsación, pendiente**. Las capacidades que se encontraron —y
> fueron muchas— quedaron escritas como *«no es un hueco»*: **registradas por ausencia de defecto,
> no como herencia para construir.**

**Tres precisiones, que el mismo `DOC-027` exige** —porque su primera redacción *«se fue al extremo
opuesto»* y hubo que corregirla:

1. **El colega no confunde las fases.** Separar observar · clasificar · decidir · ejecutar es
   `DOC-029`, y es correcto. **Lo que estrecha es el PRODUCTO de salida**: reduce `P5` a tres
   decisiones de gobernanza y difiere el resto, y en esa lectura lo que QUIRA ya hace bien no tiene
   dónde anotarse.
2. **La deuda no desaparece: cambia de tamaño.** En QUIRA `deuda` es término técnico —`deuda.py`,
   gravedad *«puede falsear una cifra pública»*—, y eso no es mentalidad de déficit, es protección
   del producto. **`D-015` sigue siendo deuda.** Lo que no es deuda es casi todo lo demás.
3. **Anotar para implementar ≠ implementar ahora.** El Gold Master sigue congelado hasta `011-C4`,
   y `DOC-029` ordena diseñar la migración antes de ejecutarla. Y no todo hallazgo produce algo que
   construir: **las dieciséis falsaciones fueron errores del auditor** — dejan método, no obra.

**Por tanto `P5` tiene tres salidas, no una:**

| salida | qué entra | criterio |
|---|---|---|
| **`P5-C` · CONSTRUCCIÓN** | capacidades a heredar, mejorar, trasladar o conectar en QUIRA vNEXT | destino `REARQ` candidato · la dirección ratifica |
| **`P5-G` · GOBERNANZA** | decisiones que evitan repetir los errores de `P0–P4` | reduce ambigüedad · evita una clase demostrable de error · aumenta capacidad verificable |
| **`P5-D` · DEUDA** | sólo lo que puede falsear una cifra pública | `deuda.py` |

---

### `P5-G.1` · Custodios — fronteras, no un custodio universal

| custodio | gobierna | NO gobierna | lo verifica |
|---|---|---|---|
| **corpus Supabase** | el texto de la ley vigente | su interpretación | SHA por chunk |
| **BRN** (`docs/brn`) | la **operacionalización** de la norma: CNO → RO | el cálculo | `I1–I8` · `check_sat_brn` |
| **Gold Master** | el **número** | la norma · la evidencia | Regla de Oro 1 · congelado |
| **`doctrina.py`** | las reglas **de método** con verificador | la norma jurídica | un test por regla |
| **`deuda.py`** | lo que **puede falsear** una cifra pública | lo que sólo degrada | un ataque por deuda |
| **ADR** | las **decisiones** de arquitectura y su porqué | su ejecución | citas + sustitución por sección |
| **PCD** | el **cierre de curación** de un dominio | su suficiencia (`DOC-035`) | expediente |
| **`registry.yaml`** | la **cadena de autoridad** de los activos registrados | lo no registrado | `check_health [5/5]` |
| **`MASTER_INDEX`** | el **routeo humano**: dónde preguntar | la autoridad | ⛔ nadie |
| **gates** | la **integridad ejecutable** en cada CI | lo que no inspeccionan | exit `0 · 1 · 2` |
| **código** | la **implementación** | ningún cambio conceptual (Regla 9) | la suite |

Leída en columna, la tabla dice algo que ninguna fase había formulado: **cada custodio tiene un
verificador salvo uno — el `MASTER_INDEX`**, que es precisamente el que `DOC-036` manda consultar
primero.

### `P5-G.2` · Representaciones — cuándo dos formas son la misma función

La pregunta que recoge las dieciséis falsaciones. **Criterio propuesto**, derivado de `DOC-013`
(*función verificable*) y `DOC-033` (*lo nominal no autoriza*):

> **Dos representaciones distintas representan la misma función sólo si se cumple al menos una
> de estas dos condiciones:**
> 1. **un mismo mecanismo la ejecuta o la verifica** — gate, test, compilador, lector único; o
> 2. **el canon declara explícitamente la correspondencia** — como `ADR-035:14` para `d04` o `canon.py:299` para `CNO-IV`.
>
> **Y nunca por:** nombre · número · residencia en carpeta · formato · longitud · frecuencia de cita · posición en el archivo.

Cada exclusión de la última línea es **una falsación de esta serie**: residencia (`registrar_ejecucion`
contado como gate), formato (hash de 12), frecuencia de cita (`QUIRA_CAUSAL_MODEL`), posición (el
`estado:` de un ejemplo).

### `P5-G.3` · Las tres decisiones · la dirección ratifica

#### 1 · BRN ↔ `MASTER_INDEX`

**No es una decisión de arquitectura nueva: es aplicar una regla que el Index ya tiene.** Su `§3`:
*«si nace un rector nuevo, regístralo aquí el mismo día — o se pierde»*. La BRN nació el
2026-07-15 con rector claro (`BRN_PLANO_MAESTRO` + `ADR-035/038/039`) y **no se registró**.

Y tiene consecuencia medible: `DOC-036 PASO 0` ordena consultar el Index antes de buscar. **Para la
norma —la base que Javo llama inexpugnable— el protocolo forense envía hoy a un sitio sin
respuesta.**

| | propuesta |
|---|---|
| **qué** | una fila de routeo: *¿dónde vive la verdad normativa?* → `BRN_PLANO_MAESTRO` · `docs/brn` · `ADR-035/038/039` |
| **relación entre registros** | **el Index RUTEA, el registro VERIFICA.** Ninguno sustituye al otro, y el Index debe **nombrar la existencia** de `registry.yaml`, que hoy no menciona |
| **qué NO se hace** | convertir el Index en índice de autoridad. Cambiaría su función, y eso sí sería arquitectura |
| **quién** | `governance/` → **Regla de Oro 5**: sólo con aprobación de Javo |

#### 2 · Cobertura de `registry.yaml`

**El hallazgo no era un problema de criterio.** Las 9 cadenas normativas fuera del registro son:

```
CNO-VII-001 · 002 · 003 · 004    RO-VII-001 · 002 · 003 · 004 · 005
```

**Toda la familia VII — Transparencia — y ninguna otra.** Las `CNO-VIII` en estado `propuesta` sí
están registradas; las `VII` **vigentes** no. No es un criterio de estado: **`d07` nunca se conectó
al registro.**

> ★ Y es exactamente lo que la dirección describió al abrir esta rearquitectura: *«hemos construido
> dominio por dominio, sin conectar totalmente el ecosistema»*. **El dominio que alimentará cada mes
> a todos los demás es el único cuya cadena normativa no está en el registro verificado por
> máquina.** `check_health [5/5]` informa *«100 % · 0 aristas rotas»* — **porque no la mira**.

| | propuesta |
|---|---|
| **criterio** | requiere registro **toda pieza cuya autoridad deriva en cadena** y cuya rotura silenciosa pasaría el CI: `CNO` · `RO` · `ADR` · `PCD` · catálogos de dominio |
| **gates** | ⛔ **no** por defecto: el bucle de CI ya los enumera por glob. Registrarlos sólo añade capacidad si el registro verifica **su autoridad citada** |
| **acción inmediata derivada** | registrar la familia VII → **`P5-C`**, no deuda (la cadena ya está verificada por `I5` y Regla 3; lo que falta es el registro) |

#### 3 · Gates fuera del circuito

**Primero una corrección a `P2/P3` — falsación 16:** se contaron 14 gates. **`registrar_ejecucion.py`
no es un gate: es un PRODUCTOR.** Su propio docstring lo dice —*«este script PRODUCE, el agente
LEE»*—. Se contó como gate **por residir en `scripts/ci/`**: residencia leída como función.

```
verificadores ………… 13        en el circuito de CI …… 12 / 13
productores …………… 1         (registrar_ejecucion)
```

| pieza | qué es | por qué no está en el circuito | propuesta |
|---|---|---|---|
| **`smoke_cajones`** | verificador real: monta `app.py` headless y exige una **huella** por cajón | su nombre no empieza por `check_` · y **no implementa `exit 2`** | **MEJORAR**: implementar el tercer estado y entonces entrar al circuito. Entrar sin él haría que su verde acreditara lo que no pudo montar |
| **`registrar_ejecucion`** | productor del testimonio que lee `procedencia.py` (escalón 6) | nadie lo invoca · **testimonio sin actualizar desde el 2026-09-02** | decidir **cuándo corre**. ⚠️ **No falsea**: `fue_exitosa` sólo acepta testimonio cuyo SHA coincide con el test actual; si no, devuelve `None`. **Degrada en silencio** los verificadores escritos después |

**Criterio propuesto para el circuito obligatorio:**

> Pertenece al circuito de CI todo **verificador** cuya falla pueda hacer que QUIRA publique algo
> falso o roto, **y** que pueda correr sin recursos fuera del repositorio **o** declare `exit 2`
> cuando no pueda. **Un productor no es un gate**, aunque resida con ellos.

### `P5-G.4` · Diferidos — ni deuda ni decisión

| | por qué no entra ahora |
|---|---|
| `MASTER_INDEX` no auditable por máquina | real, pero **no causó ninguna** de las dieciséis falsaciones |
| 4 `authority.parent` resueltos por nombre | ídem |

Pasan a `P5-C` como **MEJORAR · prioridad baja**. No se pierden; no se promueven.

### `P5-G.5` · La regla de la representación — análisis de cobertura

Se leyeron completas `DOC-035` y `DOC-036`. Las dieciséis falsaciones se reparten en **dos
familias**, y el reparto decide la respuesta:

| familia | falsaciones | ¿cubierta? |
|---|---|---|
| **AUSENCIA** — *no lo encontré → no existe* | `6` rutas · `7` RO · `8` SHA · `9` gates · `10` YAML · `11` registro · `12` sustitución | ✅ **CUBIERTA.** `DOC-035` + `DOC-036` pasos `4` variantes terminológicas · `5` variantes de formato · `10` formatos no legibles · `12` falsos positivos. **No faltaba regla: faltó aplicarla** |
| **SIGNIFICADO** — *lo encontré → significa lo que parece* | `13` identificador leído como valor · `14` citación leída como autoridad · `15` ejemplo leído como declaración · `16` residencia leída como función — y las tres que corrigió el colega: continuidad leída como identidad, ausencia de estado leída como «datos», cambio de expediente leído como reconciliación | ⛔ **NO CUBIERTA literalmente** |

**Y el reparto en el tiempo es la evidencia más fuerte:**

```
P2/P3 ……  6 de AUSENCIA  ·  0 de SIGNIFICADO
P4 ………  1 de AUSENCIA  ·  3 numeradas + 3 corregidas de SIGNIFICADO
P5 ………  0 de AUSENCIA  ·  1 de SIGNIFICADO   (la 16)
```

> **Cuando `DOC-035/036` se aplicaron con disciplina, los errores de ausencia casi desaparecieron —
> y los errores se desplazaron a la otra familia, para la que no hay regla.**

**La grieta es precisa.** `DOC-035` hereda de `ADR-042 §6-quinquies`: *«hallar un término prueba
presencia; no hallarlo NO prueba ausencia»*. La segunda mitad está gobernada con rigor. **La primera
se dio por segura, y la falsación 15 la refuta**: hallar `estado: NO_VIGENTE` probó la presencia de
esa cadena — **no que el documento estuviera no vigente.**

**Recomendación · la dirección decide:**

| opción | juicio |
|---|---|
| ya cubierta, no se formaliza | ⛔ **no**: siete errores demostrados en una sola fase |
| **`DOC-038` nueva** | ⛔ **no**: sería inflación — no es un principio nuevo |
| **corolario de `DOC-035`** que complete su mitad no gobernada: *«hallar un término prueba la presencia **del término**; no prueba la función, el régimen ni la declaración que parece nombrar»* — **más** extender `DOC-033` del plano de los indicadores al de los artefactos | ✅ **recomendada**: forma mínima, cierra la grieta exacta, y **pasa el criterio de admisión**: evita una clase demostrable de error |

---

### `P5-C` · CONSTRUCCIÓN — lo que QUIRA vNEXT hereda y eleva

Cada fila entra como **`classification_status: PROPUESTO`** (`CARTA §3`). **La dirección ratifica.**

#### CONSERVAR — capacidades demostradas que la vNEXT hereda tal cual

| # | capacidad | evidencia |
|---|---|---|
| C1 | **los tres estados en la infraestructura**: `0` verificado · `1` hallazgos · `2` no determinable, *«que NO acredita nada»* | `quira-health.yml:141-165` |
| C2 | **sustitución por sección, bidireccional y con acuse** — ningún documento sustituido entero | `ADR-024↔044` · `ADR-043↔045` · `ADR-045↔046` |
| C3 | **estados epistémicos de la norma**: `no_determinable` · `no_observable` · `motivo_sin_sat` | `RO-VII-002/003/004` · `RO-VII-001:206` |
| C4 | **el vínculo se declara, no se infiere del nombre** | `canon.py:299` |
| C5 | **existe · tiene procedencia · se reproduce** como propiedades separadas | `D-015` |
| C6 | **árbol de autoridad con raíz declarada** · 13/13 padres · verificado en cada CI | `check_health [5/5]` |
| C7 | **cadena normativa íntegra**: `I5` 13/13 · 107 eslabones con SHA | `docs/brn` |
| C8 | **estado epistémico deliberadamente incompleto** como capacidad | Regla de Oro 10 · `ADR-019` |
| C9 | **decisión conversacional → regla verificada** · 37/37 con prueba | `doctrina.py` |
| C10 | **candidato ≠ ratificado** | `CARTA §3` |
| C11 | **categoría × estado de evidencia** como ejes separados | `CARTA §2` |
| C12 | **testimonio de corrida anclado por SHA**, que degrada y no falsea | `ejecucion.fue_exitosa` |

#### MEJORAR — capacidades presentes, incompletas o desconectadas

| # | qué | por qué |
|---|---|---|
| M1 | **registrar la familia VII** en `registry.yaml` | el dominio que alimenta a todos está fuera del registro verificado |
| M2 | **fila de routeo normativo** en `MASTER_INDEX` y mención de `registry.yaml` | aplica su propia regla `§3` · repara `DOC-036 PASO 0` para la norma |
| M3 | **`smoke_cajones` con tercer estado**, y dentro del circuito | único verificador fuera de CI |
| M4 | **decidir cuándo corre `registrar_ejecucion`** | escalón 6 de procedencia degradado 12 días |
| M5 | **corolario de `DOC-035`** + extensión de `DOC-033` a artefactos | cierra la familia SIGNIFICADO |
| M6 | **extender la taxonomía `CARTA §2` a artefactos documentales** — con `TRANSMUTADO` sólo si pasa el criterio de admisión | `d04` y `ADR-040` no caben en una sola categoría |
| M7 | `MASTER_INDEX` auditable por máquina · 4 padres por `id:` | robustez · **prioridad baja** |

#### TRASLADAR

| # | qué | por qué |
|---|---|---|
| T1 | **`registrar_ejecucion.py`** fuera de `scripts/ci/` | es productor; su residencia provocó la falsación 16. **Destino: NO DETERMINADO** — no se conoce aún la residencia canónica de los productores |

#### ★ Y la capacidad de mayor alcance, que no es sobre QUIRA sino para QUIRA

**Todo lo que este barrido aprendió leyendo su propio corpus es exactamente lo que QUIRA necesita
para leer el de 222 municipios.** Los documentos de un GAD tienen la misma heterogeneidad:
PDF escaneado, `.docx`, tabla, anexo, portal, acta, sello. Los dieciséis errores del auditor son
**la lista de errores que el lector de QUIRA no puede permitirse** cuando el observado es otro:

| error del auditor sobre sí mismo | el mismo error sobre un GAD |
|---|---|
| leer el `estado:` de un ejemplo como declaración | leer la **ordenanza citada** en un acta como **ordenanza aprobada** |
| leer un identificador como valor | leer un **número de oficio** como **monto** |
| leer citación como autoridad | leer una **mención** del PDOT como **alineación** con el PDOT |
| buscar la forma y no la función | declarar **inexistente** una rendición publicada en otro formato |

`DOC-036` ya lo anticipaba: *«es exactamente el problema que QUIRA resuelve para terceros»*. **`P5`
lo convierte en especificación:**

| # | capacidad de producto | destino |
|---|---|---|
| **PR1** | **reconocer el régimen de representación antes de extraer** — distinguir declaración de cita, valor de identificador, cabecera de ejemplo | **MEJORAR** los extractores de adquisición documental |
| **PR2** | **declarar, junto a cada conclusión, qué formas se inspeccionaron** — no sólo qué fuentes | **MEJORAR** · extiende `DOC-035` al producto |
| **PR3** | **separar presencia del término de presencia de la función** en la evidencia pública | **MEJORAR** · aplica `P5-G.5` al observado |

---

### `P5-D` · DEUDA — lo que puede falsear una cifra pública

| | |
|---|---|
| `D-015` | ⛔ **sigue abierta**, sin cambio — reproducción de `0,4448` y reconciliación `0,4630 ↔ 0,4646` |
| **nuevas** | **ninguna.** La familia VII fuera del registro no falsea: su cadena está verificada por `I5` y Regla 3. El testimonio desactualizado degrada, no falsea |

> **Una deuda frente a veintitrés candidatos de construcción** — 12 capacidades a heredar, 11 a
> mejorar, trasladar o crear. Esa proporción es la respuesta medida a la pregunta de la dirección.

### Lo que `P5` NO hizo

- **No modificó nada.** `doctrina.py` · `registry.yaml` · BRN · `MASTER_INDEX` · gates · workflows: intactos.
- **No ratificó nada.** Todo `P5-C` y `P5-G.3` entra como `PROPUESTO`; `CARTA §3` reserva la ratificación a la dirección.
- **No verificó** que `smoke_cajones` pueda correr en CI sin datos externos — `NO DETERMINADO`.
- **No determinó** la residencia canónica de los productores (`T1`).

## 6 · Y la finalidad, dicha por la dirección

> *«No es una auditoría, sino **elevar este ecosistema**… para potenciar, mejorar y elevar el nivel
> de QUIRA en cada ámbito.»*

⛔ Por eso este registro **no propone conservar por defecto**. La cautela de `REARQ-001` —no
inventar canon duplicado, no destruir procedencia histórica— **no es un mandato de congelación**.
Elevar el ecosistema **incluye crear y elevar capacidades**, y también **retirar lo que ya no
sostiene ninguna**.

---
*Panorama documental · 276 documentos + 30 YAML BRN + 14 gates · 133 con autoridad declarada ·
37 reglas verificadas · 3 regímenes de custodia · Dylus Lab © 2026 · insumo para decisión de
gobernanza, no decisión.*

> El pie anterior decía **«472 reglas»**. Esa cifra fue falsada en `§5-ter` por este mismo
> documento y se corrige aquí: era del instrumento, no del corpus. **Un registro que conserva en
> su pie una cifra que su cuerpo desmintió enseña la cifra, no la corrección.**
