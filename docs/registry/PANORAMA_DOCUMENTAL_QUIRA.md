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

> ⛔ **Corregido en `§5-terdecies` (falsación 22).** La tabla de arriba **está mal medida**: la
> expresión tomaba el primer `estado:` del YAML **con cualquier sangría**, y en `RO-VII-002/003/004`
> ese primer `estado:` está **anidado**. Con parser YAML, las tres son **`vigente`** en primer nivel.
> Cifras reales: **10 RO vigentes que compilan · 3 en `propuesta`** —lo confirma
> `brn_compilador --verificar`—.
>
> **La capacidad sobrevive, y es más fina de lo que se escribió.** Los `no_determinable` y
> `no_observable` no son el estado de la regla: son **casos borde que una regla vigente declara como
> dato** —`caso_sin_dimensiones_determinables` · `caso_sin_solicitudes`— para que *«el criterio no
> vuelva al código»*. No es «una regla que no puede evaluarse»: es **una regla vigente que declara
> cuándo su propio resultado no es determinable**.

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

## 5-nonies · `P5` · RATIFICADO E IMPLEMENTADO

### ⛔ La dirección corrige otra premisa · Javo · 2026-09-14

> *«Estamos en auditoría **y** refactorización. Nada está congelado en este gran proceso.»*

`§5-octies` escribió como tercera precisión *«anotar para implementar ≠ implementar ahora»*,
apoyada en un congelamiento. **En este proceso ese congelamiento no existe**, y la precisión se
retira. Lo que se ratifica, se construye.

Y el lenguaje de salida se corrige como pidió el colega, porque «1 deuda y 23 candidatos» vuelve a
leerse en binario: **1 deuda abierta confirmada y 23 capacidades o cambios potenciales de vNEXT,
sujetos a decisión de diseño** — dentro de los cuales hay capacidades que ya existen y sólo se
conservan. **No todos son cambios.**

### Lo ratificado, y lo que ya está hecho

| decisión | ratificación | implementado |
|---|---|---|
| **P5-01** · BRN en `MASTER_INDEX` | ✅ una fila de routeo, sin duplicar semántica | ✅ fila *«Qué NORMA gobierna»* → `BRN_PLANO_MAESTRO` · `docs/brn/` · ADR-035/038/039 · corpus · verificada por `registry.yaml` |
| **P5-02** · familia VII en el registro | ✅ bajo el mismo régimen que las demás | ✅ **por el generador, no a mano** — y resultó no ser un problema de `d07` (ver abajo) |
| **P5-03** · circuito de gates | ✅ reformulado: **criticidad de la invariante**, no «tener tercer estado» | ✅ 14 declaraciones `CIRCUITO:` + prueba que las obliga a coincidir con el workflow |
| **P5-04** · no crear `DOC-038` | ✅ | ✅ |
| **P5-05** · corolario de `DOC-035` | ✅ sujeto a verificar la superficie doctrinal | ✅ verificada y escrita — atacada sobre dos extractores reales |

### ⛔ Falsación 17 — `d07` nunca estuvo desconectado

`§5-octies` afirmó: *«no es un criterio de estado: **`d07` nunca se conectó al registro**»*. **Falso.**
`registry.yaml` declara en su cabecera *«GENERADO · NO editar a mano»* y estaba generado el
**2026-08-12**; las `CNO-VII` nacieron el 2026-08-18. **El generador no se había vuelto a correr.**
Al regenerarlo:

```
registro   2026-08-12 → hoy      129 → 158 activos    (+29: 11 ADR · 5 OBS · 1 PCD · 9 CNO/RO · …)
grafo      2026-07-27 → hoy      111 → 158 nodos
```

No faltaba sólo Transparencia: **faltaba todo lo creado en un mes**. Y el grafo, con el que el
gate imprimía *«111 aristas, 0 rotas»*, **tenía siete semanas**. La capacidad `C6` de `§5-octies`
—*«árbol de autoridad verificado en cada CI»*— se corrige: **el gate verificaba la cadena dentro de
un derivado viejo, no la del repositorio.**

### Y la causa estaba escrita en el propio gate

```python
# 3 · ¿el Registry está al día con el disco? (hash de un centinela)
frozen = ROOT / "identity" / "CONSTITUCION_INSTITUCIONAL.md"
if not frozen.exists(): ...
```

> **El rótulo prometía frescura; el mecanismo verificaba que la Constitución existiera.** Es la
> familia SIGNIFICADO de `§5-octies`, dentro del gate de gobernanza: `declarado ≠ ejecutado`
> (`ADR-042 §6-ter`), en su forma más literal.

**Implementado:** el paso 3 relee el disco con **el mismo escáner** que escribe el registro y
falla si el registro o el grafo no lo reflejan. **Falsado** contra el registro de 2026-08-12:
exit 1, 82 activos nombrados, grafo desactualizado detectado. Con el registro al día, verde.

### ⛔ Y lo que difirimos como «robustez» rompía la cadena

Con los derivados al día aparecieron **5 aristas rotas**. Cuatro eran exactamente los *«padres
resueltos por nombre»* que `§5-octies` y el colega difirieron por no haber *«demostrado impacto
arquitectónico»*. **Se difirieron sobre un grafo de siete semanas.**

La causa, y es `DOC-015` violado a escala: sin `id:` declarado, el generador **fabricaba el
identificador desde el nombre de archivo**.

| | antes | ahora |
|---|---|---|
| `ADR-035` en el registro | `CANON_ADR-ADR-035_Biblioteca_Reglas_Normativ` | **`ADR-035`** |
| activos con id fabricado | **86 de 158** | **30** — 72 declaran `id:` y 56 lo declaran en su título. Los 30 restantes (catálogos, pipelines, cypher, gobernanza, `PCD-MN01`) no tienen prefijo canónico |
| aristas rotas | **5** | **0** |
| ids que nombran a dos activos | **6 pipelines fundidos en `DOMAIN_PIPELINE-__init__`** | **0 · 158 únicos de 158** |

**La corrección no editó 86 archivos.** El generador lee ahora el identificador **donde el documento
lo declara —su título—, y sólo si el archivo dice lo mismo**: dos representaciones que coinciden
(`P5-G.2`), no una inferida de la otra. Una prueba ataca el caso opuesto: un prefijo de archivo
sin título que lo confirme **no** acredita identificador.

La quinta arista —`PCD-D06 → PROTOCOLO_CURACION_DOMINIO`— **no estaba rota**: el padre existe, en
el hueco de alcance que el registro declara a propósito desde el 2026-07-29. El gate lo llamaba
*«padre declarado inexistente»*. Ahora se clasifica **fuera de catálogo** y se informa sin
bloquear: *«el verde NO las cubre»*. ⛔ **No se le estampó autoridad**: la Carta lo prohíbe, y su
derivación sigue pendiente de verificarse.

### `P5-05` · el corolario, y dónde vive realmente

Antes de escribirlo se leyó la superficie completa: `DOC-035`, `DOC-036`, `ADR-042 §6-ter`
(*«la clasificación automática descubre; no interpreta»*), `§6-quater` (*«un número correcto con
una etiqueta incorrecta es un número falso»*), `§6-quinquies`, y `procedencia.py`.

**Resultado:** la familia SIGNIFICADO **ya estaba gobernada para el sujeto observado**. Faltaba su
extensión al **observador** —el mismo movimiento con que nació `DOC-035` para la ausencia—. Se
escribió como corolario dentro de `DOC-035`, no como doctrina nueva.

**Y no era sólo el auditor.** Dos extractores de QUIRA tenían el defecto, latente:

| extractor | leía | con el documento de ataque |
|---|---|---|
| `build_registry.analizar` | `id:` y `parent:` en los primeros 4000 bytes | tomaba `id: FALSO-001` · `parent: NADIE` de un ejemplo |
| `preguntas_publicas._pcds` | `status:` en los primeros 800 bytes | tomaba `status: NO_VIGENTE` de un ejemplo |

Medido: **ningún activo real lo sufría hoy** — es latente, y se declara así. Corregidos para leer
sólo la declaración del documento; `test_hallar_un_termino_no_prueba_la_declaracion` los ataca.

### `P5-03` · el circuito, declarado

| clase | archivos | por qué |
|---|---|---|
| **OBLIGATORIO** | los 12 `check_*` | cada uno protege una invariante de integridad, procedencia, normativa o reproducibilidad — declarada en su docstring |
| **BAJO_DEMANDA** | `smoke_cajones` | su fallo impide **ver** un cajón; no hace que QUIRA afirme algo falso. *(`exit 2` pendiente como propiedad de diseño, no como criterio)* |
| **NO_GATE** | `registrar_ejecucion` | productor — falsación 16 |

La convención de nombre coincidía con la función **por costumbre**. Ahora la pertenencia se
**declara** y `test_lo_obligatorio_es_exactamente_lo_que_el_ci_ejecuta` obliga a que declaración y
workflow coincidan **en las dos direcciones**. Falsado: un `smoke_cajones` declarado obligatorio
y un `check_nuevo.py` sin declarar son detectados.

### ★ El producto arquitectónico principal — y por quinta vez, ya existía

El colega fijó como producto de `P5` *«la separación explícita entre **representación encontrada**
y **afirmación acreditada**»*, con la cadena `REPRESENTACIÓN → CONTEXTO → SIGNIFICADO → EVIDENCIA →
INFERENCIA`.

**Esa separación existe y está ejecutada desde el 2026-08-19: `app/agents/procedencia.py`.**

| cadena propuesta | `procedencia.py` · las siete capas |
|---|---|
| representación | **4** · evidencia — qué artefacto quedó, con qué SHA |
| contexto | **1** fuente · **2** captura · **3** estado de adquisición |
| significado | **5** · verificador — *¿qué componente la interpretó?* · **6** · *¿qué prueba respalda esa interpretación?* |
| — | **7** · sujeto — *¿sobre quién se afirma?* (`ADR-051 §12`: sin sujeto no hay afirmación) |
| inferencia | **el peso**: `no_determinable` · `hallazgo_de_verificabilidad` · `hecho_verificable` (`ADR-051 §4`) |

Y su principio es literalmente el que se pedía: *«cuando la cadena no puede sostener una afirmación,
QUIRA **degrada** la afirmación; nunca rellena el vacío»*. **La capa que la propuesta no tenía, y
`procedencia.py` sí, es el sujeto.**

> **P1 halló el registro de reglas. P4 halló la taxonomía. P5 halla el contrato de interpretación.
> Cinco veces lo que se iba a construir ya estaba construido.** La consecuencia para vNEXT no es
> «construir el contrato»: es **extender el que existe** —al observador (hecho, `DOC-035`), a los
> extractores de gobernanza (hecho, dos) y a los extractores de adquisición de los GAD (`PR1`,
> pendiente)—.

### ⚠️ `anti-falsificación ≠ continuidad de evidencia` — el patrón, medido

La distinción del colega resultó ser **un patrón con tres casos**, no una observación sobre uno:

| derivado de gobernanza | última generación | se protege contra lo viejo | se regenera solo |
|---|---|---|---|
| `registry.yaml` | 2026-08-12 | **ahora sí** — el gate compara con el disco | ⛔ no |
| `authority_graph.json` | 2026-07-27 | **ahora sí** | ⛔ no |
| `registro_de_ejecucion.json` | 2026-09-02 | ✅ sí — SHA por prueba, degrada a `None` | ⛔ no |

**Los tres se protegen —o ya se protegen— contra usar evidencia vieja. Ninguno garantiza que la
nueva se produzca.** Esa es la decisión de diseño de procedencia de ejecución para vNEXT: **quién
regenera un derivado de gobernanza, y cuándo**.

### Lo que queda, sin convertir en deuda

| | destino |
|---|---|
| regeneración gobernada de los tres derivados | **decisión de diseño vNEXT** |
| `smoke_cajones` con `exit 2` | MEJORAR · propiedad de diseño |
| residencia canónica de `registrar_ejecucion` | TRASLADAR · destino no determinado |
| derivación verificada de `PROTOCOLO_CURACION_DOMINIO` y del resto de `docs/architecture` | pendiente · **nunca por estampado** |
| `PCD-MN01` y los 30 ids fabricados restantes | MEJORAR · ninguno es hoy padre de nadie |
| `PR1–PR3` · el corolario llevado a la adquisición de los GAD | **la capacidad de producto de mayor alcance** |
| `D-015` | ⛔ **deuda** — sin cambio |

## 5-decies · `P5-CIERRE` · checkpoint — y la consulta de la dirección sobre una BRN dinámica

### Estado que se registra

> **`P5` — IMPLEMENTADO Y VERIFICADO LOCALMENTE; CIERRE FORMAL PENDIENTE DE CI REMOTO.**
> **`D-015` — única deuda confirmada**
> **`Q-M2-C` — siguiente fase, bloqueada hasta el cierre formal de `P5`**

| | estado |
|---|---|
| implementación local | **DEMOSTRADA** |
| suite local | **DEMOSTRADA** |
| reconstruibilidad desde lo commiteado | **FAVORABLE** — indicios, no prueba |
| CI limpio sobre el estado remoto | **`NO DETERMINABLE`** |

La secuencia de cierre no admite atajo: **push autorizado por la dirección → CI real → si verde, `P5`
formalmente cerrable → `Q-M2-C`**. No se hace push sin esa autorización.

Se corrige la redacción de `§5-nonies`, a pedido del colega: no *«las cinco decisiones están
aplicadas»*, sino **«las cinco decisiones fueron implementadas; el checkpoint verifica que la
implementación corresponde a lo ratificado y declara lo que introdujo»**. ⚠️ El checkpoint lo
ejecuta **quien implementó**: no es la verificación independiente que el colega pidió, y se dice.

### La matriz de correspondencia

| decisión | implementación | evidencia | prueba | estado |
|---|---|---|---|---|
| **P5-01** · BRN → `MASTER_INDEX` | `296c47d` · `governance/QUIRA_MASTER_INDEX.md` · +1 fila | las rutas resuelven —`check_consistencia` no halla rutas obsoletas en el Index—; la fila **sólo rutea y fija fronteras**, no copia contenido de CNO ni RO | sin prueba específica · `check_consistencia` custodia las rutas | ✅ **CERRADA** |
| **P5-02** · registro de autoridad | `296c47d` · `build_registry.py` · `build_authority_graph.py` · `check_health.py` · `registry/*` regenerados | 158 activos · **158 ids únicos** · **0 aristas rotas** · 1 fuera de catálogo · **0 activos sin rastrear en git** · ninguno ignorado · falsado contra el registro de 2026-08-12 | `test_registro_de_autoridad.py` (6) · `check_health [5/5]` | ✅ **CERRADA** · alcance abajo |
| **P5-03** · circuito de gates | `296c47d` · 14 docstrings de `scripts/ci/` | `OBLIGATORIO` **12** · `BAJO_DEMANDA` **1** · `NO_GATE` **1** · el CI ejecuta **12** | `test_circuito_de_gates.py` (4) | ✅ **CERRADA** · alcance abajo |
| **P5-04** · no crear `DOC-038` | — decisión de no crear | `doctrina.py`: **37 entradas**, ninguna `DOC-038` | `test_doctrina_con_custodio` | ✅ **CERRADA** |
| **P5-05** · corolario de `DOC-035` | `296c47d` · `doctrina.py` · `build_registry.analizar` · `preguntas_publicas._cabecera` — **y este checkpoint** · `doctrina._custodia_citada_inexistente` | corolario en la regla · dos extractores corregidos y atacados · la custodia citada en prosa **ahora la verifica el custodio** | `test_hallar_un_termino_no_prueba_la_declaracion` · `test_toda_custodia_citada_en_el_texto_de_una_regla_existe` | ✅ **CERRADA en este checkpoint** |

**Derivados regenerados:** `registry.yaml` · `authority_graph.json` · `institutional_state.json` ·
`INSTITUTIONAL_STATE.md`.
**Fuera de los commits, a propósito:** `data/d07/cadena_estado.json` ·
`data/quira/autoconocimiento.json` · `docs/architecture/REARQ_ARQUEO_CAPACIDAD_DOCUMENTAL.md` —
modificados antes de esta tarea— y `data/snapshots/130801/provenance/ensayos/*`, sin rastrear, que
otro proceso sigue produciendo durante la sesión.
**Pruebas nuevas:** 10 en `296c47d` y 1 en este checkpoint. *(Las «25» que se leyeron eran una
corrida parcial que incluía pruebas vecinas.)*

#### El hueco que el checkpoint encontró en `P5-05`, y se cerró

La prueba del corolario existía, pero **sólo estaba nombrada en la prosa** de `DOC-035`. El custodio
de la doctrina verificaba únicamente el campo `verificador`. Si esa prueba se renombraba, la doctrina
seguiría **afirmando una custodia inexistente**: rótulo ≠ función, el mismo defecto que `P5` halló
en el gate del registro. No se dejó como relación documentada: **el custodio existente ahora exige
que toda prueba citada como custodia exista**. Se ejecutó un **caso negativo** —una referencia a una
prueba inexistente, introducida en memoria durante la verificación y retirada después, sin tocar
ningún archivo— y el custodio detectó la inconsistencia; retirada la referencia, el hallazgo
desaparece.

> ⚠️ **Y lo que ese mecanismo NO acredita, dicho sin ambigüedad.** Verifica **existencia**, nada más:
>
> ```
> prueba citada  ≠  prueba existente  ≠  prueba ejecutada  ≠  prueba adecuada  ≠  doctrina verdadera
> ```
>
> Que la prueba citada exista impide que la doctrina afirme una custodia inexistente. **No demuestra
> que la prueba corra, que ataque lo que dice atacar, ni que la regla sea correcta.** Cada uno de esos
> escalones es otra verificación, y ninguna la hace este custodio.

### Alcance exacto de lo cerrado — lo que NO se afirma

| | se demostró | NO se demostró |
|---|---|---|
| **P5-02** | regeneración · unicidad · resolución de la cadena · 0 aristas rotas · hueco clasificado | **158 activos registrados ≠ 158 activos ontológicamente correctos** |
| **P5-03** | correspondencia entre declaración y ejecución **actual** del CI | que el workflow sea el correcto |
| **todo** | 941 pruebas y `check_health` en verde **en local** | ⛔ **el CI remoto no ha corrido**: `main` va por delante de `origin/main` —38 commits al ejecutar el checkpoint; la cifra crece con cada commit y por eso no se usa como estado—. Indicios: sintaxis compilada contra 3.11, 0 activos sin rastrear, ninguno ignorado. **`NO DETERMINABLE` hasta que corra** |

**Integridad estructural ≠ validez semántica.** Lo que 158/158 demuestra y lo que no:

```
DEMOSTRADO    158 activos → 158 ids únicos → rutas resueltas → 0 aristas rotas
NO ANALIZADO  158 activos → 158 autoridades correctas → 158 semánticas correctas
```

La segunda cadena es otro análisis, y confundirla con la primera sería repetir, en el registro, el
error que `P5` corrigió en el gate.

⚠️ **Y lo que `P5` introdujo, declarado para que no pase como gratuito:** con el paso 3 real,
**agregar, retirar o renombrar un ADR, OBS, PCD, CNO o RO obliga a regenerar registro y grafo antes
del push, o el CI falla**. Es el comportamiento correcto —el gate por fin dice la verdad—, pero
hasta que se decida el régimen de regeneración **la carga recae en quien commitea**. No falsea nada:
es fricción de proceso, y el régimen de la lista `B` es quien debe absorberla.

### `A` · Correcciones a conclusiones anteriores

| se afirmó | lo que era |
|---|---|
| *«`d07` nunca se conectó al registro»* | un derivado sin regenerar desde el 2026-08-12 · **falsación 17** |
| *«árbol de autoridad verificado en cada CI»* (`C6`) | la cadena se verificaba **dentro de un derivado de siete semanas** |
| *«padres por nombre: robustez sin impacto»* | rompían **4 aristas** · se difirieron sobre un grafo viejo |
| *«129 activos · 111 aristas · 0 rotas»* | ⛔ **no sólo viejo: estructuralmente engañoso.** 129 activos con **124 ids distintos** — seis pipelines fundidos en uno. El gate certificaba una representación que **colapsaba objetos distintos** |
| *«¿el registro está al día con el disco?»* | el paso verificaba **que la Constitución existiera** |
| *«las cinco decisiones están aplicadas»* | implementadas · checkpoint ejecutado · CI remoto pendiente |

**La conclusión que `P5` deja, formulada por el colega:**

> **La representación derivada debe ser reconstruible desde el estado actual del universo que
> pretende representar.**

`anti-falsificación ≠ continuidad de evidencia` era insuficiente sin ella: un derivado puede
protegerse contra lo viejo y aun así **colapsar lo que representa**. Y para un gate de CI, **ese
universo es el repositorio commiteado, no el disco de quien generó el derivado** — por eso el
checkpoint verificó que los 158 activos estén rastreados por git. **No se eleva a doctrina**: es la
conclusión de `P5`, y la implementa `check_health._registro_al_dia`.

### `B` · Decisiones fuera de `P5` — y por qué no son residuo

**Criterio:** ninguna es condición para que las cinco decisiones ratificadas se sostengan.

| | naturaleza |
|---|---|
| **régimen de regeneración y custodia de los derivados de gobernanza** — registro, grafo y testimonio de ejecución · la pregunta exacta: **¿quién es el custodio del proceso de regeneración?** Hoy es *«una persona recuerda regenerar»*: funciona, y es frágil. `CANON → REGISTRADOR → DERIVADOS → GATE` debería ser una operación reproducible, no una costumbre | **DECISIÓN DE DISEÑO PENDIENTE, delimitada** · no es deuda en el sentido de `deuda.py`: no falsea una cifra pública · absorbe la fricción que `P5` introdujo |
| `MASTER_INDEX` auditable por máquina | MEJORAR |
| derivación verificada de `PROTOCOLO_CURACION_DOMINIO` y del resto de `docs/architecture` | pendiente · **nunca por estampado** |
| `PCD-MN01` y los 30 ids fabricados | MEJORAR · ninguno es padre de nadie |
| `smoke_cajones` con `exit 2` · residencia de `registrar_ejecucion` | MEJORAR · TRASLADAR |
| `PR1–PR3` · el corolario llevado a los extractores de adquisición de los GAD | capacidad de producto |
| herencia de confianza por `MISMA_FUENTE_QUE` | **es `Q-M2-C`** |
| **BRN dinámica · dominios como subagentes · QUIRA AI coordinador** | **vNEXT** · dirección arquitectónica, no ADR · ver consulta abajo |
| **propagación de cambio aguas abajo** — *si cambia la fuente, ¿qué conocimiento quedó potencialmente afectado?* | **vNEXT** · la mitad **normativa** ya está diseñada: el MDN (`ADR-038 §9` · `BRN_PLANO_MAESTRO §5`) —*«todo texto sabe qué activos dependen de él»*—, sin determinar si opera. La extensión a **evidencia, derivados e inferencias** no está diseñada |
| unificación de dominios | **diferida por la dirección** — no se analiza |

### ★ La consulta de la dirección · ¿BRN dinámica, dominios y QUIRA como agentes?

> *«La BRN no debería ser una cuestión estática con todas sus cadenas […] creo que debe ser
> dinámica, y eso implicaría que fuese un agente o subagente de QUIRA. Y asimismo pensaría cada
> dominio como agente o subagente, y QUIRA el gran agente de IA para la gestión pública — pero sin
> dejar de ser una infraestructura de conocimiento verificable para la gestión pública
> territorial.»* — Javo, 2026-09-14

El colega respondió con la distinción decisiva —**dinámica en su operación, estable en su
autoridad**—. Antes de registrarla se contrastó con el canon, y **por sexta vez lo planteado ya
estaba pensado**:

| lo que plantea la dirección | lo que el canon ya tiene | lo que NO existe |
|---|---|---|
| **BRN dinámica** | `BRN_CICLO_VIDA_Y_MOLDE` Parte I (2026-07-18): estados de CNO y RO, versión inmutable una vez vigente, **vigencia operativa por tramos** —65 % en 2026, 70 % en 2027 sin reformar nada—, `derogada` como *memoria normativa viva*, y la **propagación de una reforma en siete pasos**, con el paso 2 marcado **`[automático]`** y el 3 **`[IA propone]`**. `REFORMA_SIMULADA_CNO-IV-001` ejecutó el ciclo documentalmente | **la operación.** Nadie detecta hoy una reforma, nadie dispara el paso 2: el ciclo existe y **corre a mano** |
| **límite de su autoridad** | `CICLO_VIDA §3b`: *«revisión técnica y aprobación formal son actos distintos»* · sólo Javo promueve a `vigente` · `ADR-035 §5` · `ADR-042 §6-ter` | — |
| **dominios como agentes** | `app/agents/d01…d09` + `_template` · `META_CATALOGO_AGENTES` —*«Organigrama Cognitivo de QUIRA IA»*— · el Budget Agent ya compartido por d01, d02, d07 y d09 | subagentes con vigilancia propia: varios agentes IA siguen en `⬜ Fase 4`. ⚠️ El propio catálogo advierte que debe actualizarse al cerrar cada capacidad; su estado no se da por vigente |
| **criterio para que algo sea agente** | **`ADR-051 §5`**: *«la IA se justifica, no se presupone»* —tres agentes de d07 resultaron deterministas— · `§2`: QUIRA ejecuta sin Claude · `§9`: *«autonomía no es ausencia de decisión humana: una sola orden basta»* | — |
| **QUIRA gran agente, sin dejar de ser infraestructura** | **`DEC-0012`** (vigente) dice literalmente *«infraestructura de conocimiento verificable para la gestión pública territorial»* · `ADR-033`: QUIRA IA como capa conversacional | **QUIRA IA** — *«aún por construir»* |
| **unificación de dominios** | destino `UNIFICAR` y la regla *«los dominios también se ganan su residencia»* (`Q-M1`) | — diferida |

> ★ **La BRN fue diseñada dinámica en julio. Lo estático es su operación.**

Eso afina la secuencia del colega sin alterar su orden. Su paso 2 —*«describir el ciclo de vida
dinámico de la BRN»*— **ya está hecho**; se convierte en **operacionalizar el ciclo que está
descrito**. Y el «BRN Agent» deja de ser una capa por diseñar: es **ejecutar los pasos 1 a 3 de
`CICLO_VIDA §5`** —detectar la reforma, señalar el impacto por el grafo, proponer la versión
siguiente— **y detenerse en el 4**, donde decide una persona.

| | secuencia |
|---|---|
| 1 | cerrar la auditoría y `Q-M2-C` |
| 2 | **operacionalizar** el ciclo de vida que `BRN_CICLO_VIDA_Y_MOLDE` ya describe |
| 3 | el agente normativo como ejecutor de `§5` pasos 1-3 · `§3b` como límite |
| 4 | qué dominios pasan de módulo a subagente — con `ADR-051 §5` como criterio |
| 5 | la coordinación de QUIRA AI |

### `C` · La pregunta de `Q-M2-C`

> **¿Cómo circula una evidencia —y cómo circulan las reglas que permiten interpretarla— entre la
> BRN, el Gold Master, los dominios y los futuros agentes, preservando procedencia, unidad, estado
> epistemológico, autoridad y confianza, sin que el tránsito cree semántica o confianza que no
> existía en el origen?**
>
> *(Formulación del colega, 2026-09-14. Amplía la anterior: no sólo circula la evidencia, también
> las reglas que la vuelven interpretable.)*

*Punto de partida verificado, sin análisis:* `procedencia.py` gobierna el peso de **una** afirmación
en **un** punto; la relación `MISMA_FUENTE_QUE` existe en `scripts/cypher/003`, `004` y `005` — y en
`005` une una `Fuente` con un `Dominio`, no con otra fuente. Si esa relación conserva o transforma la
confianza es lo que `Q-M2-C` tiene que responder.

## 5-undecies · Push, CI reproducido, y apertura de `Q-M2-C`

### Autorización y push · Javo · 2026-09-14

> *«Haga push señor director y abra Q-M2-C.»*

| paso | resultado |
|---|---|
| push de `174c380` a `origin/main` | primer intento rechazado por GitHub (`Internal Server Error`, lado servidor) · **segundo intento aceptado** · local y remoto sincronizados |
| CI remoto | **disparado**, y ⛔ **no legible desde este entorno**: sin `gh` instalado y sin herramienta que lea GitHub Actions. **No se afirma su resultado** |

### El CI reproducido encontró lo que el checkpoint dejó `NO DETERMINABLE`

Se siguió **la receta que el propio workflow documenta**, con sus tres pasos: clon limpio sin lo que
`.gitignore` excluye · `check_health` compilando contra 3.11 · gates y suite con `QUIRA_DATOS`
apuntando a una carpeta vacía.

| commit | `check_health` | gates | suite |
|---|---|---|---|
| `174c380` | ✅ | 10 verificados · 1 no determinable · 0 hallazgos | ⛔ **1 falla** · 877 pasan · 64 omitidas |
| `ffb581e` | ✅ | 10 · 1 · 0 | ✅ **0 fallan** · 877 pasan · 65 omitidas |

**La prueba que fallaba no venía de `P5`:** `test_el_corpus_capturado_del_portal_sigue_completo`,
escrita en el arqueo documental anterior, exigía `data/lotaip/descargas/` en cualquier entorno, y
`.gitignore` la excluye por decisión. **El CI remoto de `174c380` casi con seguridad la muestra
fallando.** Corregida en `ffb581e` con el mecanismo del repositorio —el fixture
`evidencia_capturada`— y verificada en sus tres ramas: pasa en el entorno completo · se salta
diciéndolo en un clon limpio · **falla** si la evidencia está pero `descargas/` desaparece.

**Lo que la reproducción NO cubre:** Linux · el runtime 3.11 (sí la compilación contra 3.11) · una
instalación limpia de dependencias. Por eso:

> **`P5` — IMPLEMENTADO · CI REPRODUCIDO EN CLON LIMPIO: VERDE (`ffb581e`) · CIERRE FORMAL: PENDIENTE
> DE LEER EL CI REMOTO** en GitHub Actions, por quien tenga acceso.

### ⛔ Falsación 18 — divergencia entre artefacto de trabajo y estado canónico

> **Un artefacto de trabajo desactualizado fue inicialmente tomado como posible base del análisis;
> la comparación contra `HEAD` permitió detectar la divergencia antes de extraer conclusiones.**
> *(Redacción del colega, 2026-09-14. La primera versión de este apartado decía «algo restauró una
> versión anterior»: juzgaba un origen que no estaba demostrado.)*

`docs/architecture/REARQ_ARQUEO_CAPACIDAD_DOCUMENTAL.md` **en disco tiene 995 líneas; en `HEAD`,
1.484**. No son finales de línea: faltan en disco `§4-sexies` a `§4-nonies` —la matriz de Web GAD,
el hallazgo de los productores del snapshot, **la síntesis `C` de `Q-M2`**, la capa normativa omitida
y la auditoría del propio arqueo—.

#### Arqueología de la divergencia — sin tocar el archivo

| pregunta del colega | resultado | grado |
|---|---|---|
| **1 · ¿qué difiere?** | la copia en disco es **idéntica, byte a byte sin finales de línea, a la versión del commit `b9f2c32`** (2026-09-09 23:11). Le faltan los cinco commits posteriores: `08618a2` · `a3146d3` · `18346c2` · `8e4980d` · `731c226` | **DEMOSTRADO** · hash `74a13a176fe5a3c8` en ambos |
| **2 · ¿cuándo?** | escrita en disco el **2026-09-12 a las 08:07:33 −05:00**, dos días después del último commit. Es el único archivo del repositorio escrito en esa ventana | **DEMOSTRADO** · fecha de modificación |
| **3 · ¿quién?** | **no fue** una operación de git —el `reflog` sólo registra commits— **ni** una herramienta de esta sesión —su transcript no tiene ninguna ejecución entre 08:06 y 08:09, y su última escritura sobre el archivo es del 2026-09-10 21:59— | **`NO DETERMINABLE`** · universo NO inspeccionado —**no son hipótesis de origen**, sólo lo que no se miró—: otros procesos y programas con acceso a la carpeta. La investigación del origen **se detiene aquí**: el valor probatorio del incidente ya está delimitado |
| **4 · ¿tiene modificaciones locales legítimas?** | **no.** Las «15 inserciones» son líneas de `b9f2c32` que los commits siguientes reescribieron | **DEMOSTRADO** |
| **5 · ¿algún commit la explica?** | no | **DEMOSTRADO** |
| **6 · ¿tiene valor probatorio propio?** | ninguno único: su contenido es recuperable siempre con `git show b9f2c32:<ruta>`. Su valor es **como evidencia del incidente** —hash y fecha—, y ya queda registrado aquí | **DEMOSTRADO** |

**Decisión que corresponde a la dirección**, ahora con evidencia: restaurar el archivo desde `HEAD`
**no pierde nada**, porque todo lo que contiene la copia está en `b9f2c32`. Las opciones siguen
siendo restaurar · conservar · reconciliar — y ninguna se ejecuta sin ratificación.

La orientación de `Q-M2-C` **empezó leyendo esa copia**, y habría partido de un `Q-M2` sin su
síntesis. Es exactamente el aviso con que el colega cerró `P5`: *antes de concluir, preguntar si se
mira la representación equivocada o un derivado envejecido*. **Se leyó de `HEAD`.**

⚠️ **El archivo en disco NO se revirtió** —no es de este trabajo— **ni se incluyó en ningún commit.**
Commitearlo tal como está borraría medio arqueo. **Hasta que la dirección lo reconcilie, `Q-M2-C` lee
el arqueo desde `HEAD`.**

### `Q-M2-C` · APERTURA — sin ejecución probatoria

**La pregunta** (colega · 2026-09-14):

> **¿Cómo circula una evidencia —y cómo circulan las reglas que permiten interpretarla— entre la
> BRN, el Gold Master, los dominios y los futuros agentes, preservando procedencia, unidad, estado
> epistemológico, autoridad y confianza, sin que el tránsito cree semántica o confianza que no
> existía en el origen?**

**El linaje, leído de `HEAD`.** El identificador se conserva; la pregunta crece (`DOC-015`):

| | pregunta | dónde |
|---|---|---|
| `Q-M2` | ¿en qué medida QUIRA transformó la adquisición heterogénea en infraestructura común de evidencia, procedencia y reutilización interdominio? | `REARQ_ARQUEO §4-quater` |
| `C` | ¿puede transformar evidencia de distintos orígenes en un estado canónico común, conservando la procedencia que otros dominios necesitan para reutilizarla sin readquirirla? | `§4-septies` · respuesta **`B`**: arquitectura conceptual común, realización distribuida y desigual |
| omisión | la síntesis recorrió adquisición → transformación → circulación **sin la capa normativa** | `§4-octies` |
| duplicación | `Q-M2` reconstruyó lo que `ADR-033` y `ADR-042` ya decidían | `§4-nonies` |
| **`Q-M2-C`** | reescribir `C` **derivando de lo decidido**, con la capa normativa dentro, y extendida a **la circulación de las reglas y de la confianza** | este registro |

**El punto de partida que `C3` ya dejó demostrado** —y del que no se parte de cero:

| | estado según `§4-septies C3` |
|---|---|
| mecanismo de reutilización | existe · `MISMA_FUENTE_QUE` en `scripts/cypher/` |
| principio | existe · *«la cédula se extrae una vez, no dos»* |
| contrato de consulta interdominio | **decidido y sellado** · `ADR-053 §6-bis` · `app/agents/consulta.py` declara implementarlo —*«POR QUÉ EXISTE (2026-08-30 · ADR-053 §6-bis)»*— |
| **reutilización efectiva** | `C3` dice 🔴 **no demostrada**, citando `ADR-053`: *«consultas dominio → dominio: NINGUNA»* |

> ⚠️ **Y esa cita tiene fecha.** `ADR-053` midió *«NINGUNA»* el **2026-08-26**; `consulta.py` se creó
> el **2026-08-30**; la síntesis `C3` del **2026-09-10** siguió citando la medición anterior como estado.
> Es el patrón de `P5` —un derivado que envejece— en una cita de prosa.
>
> ⛔ **Tampoco se afirma lo contrario:** que el módulo exista no prueba que ningún dominio lo invoque
> (corolario de presencia). **Primera pregunta probatoria de `Q-M2-C`: ¿hay hoy consultas
> dominio → dominio en el código, y quién llama a `consulta.py`?**

**El universo por plano** —verificado sólo en existencia; ningún contenido leído todavía como
prueba—:

| plano | residencia a inspeccionar |
|---|---|
| **BRN** | `BRN_PLANO_MAESTRO` · `BRN_CICLO_VIDA_Y_MOLDE` · `ADR-035/038/039` · `docs/brn/` · `brn_lector.py` · `canon.py` |
| **evidencia** | `ADR-042 §6` · `ADR-045` custodias · `ADR-046` acreditación · `procedencia.py` · `sujeto.py` · `datos.py` |
| **Gold Master** | `ADR-023` · `ADR-029` · `ADR-033` · `ADR-039` compilación · `ADR-047` · `gold_master.py` · `BRIDGE_EXCEL_CORPUS` |
| **dominios** | `ADR-031` · `ADR-053` · `app/agents/d0X/` · `data/d0X/catalogo_*` |
| **indicadores** | `GM-OMEGA_CONTRATO_INDICE_DOMINIO` · matrices de procedencia del ICPI |
| **inferencia** | `ADR-033` capas epistemológicas · `ADR-051 §4` niveles semánticos · `check_epistemico` |
| **interdominio** | `scripts/cypher/001…007` · `consulta.py` · `acoplamiento.py` |
| **agentes** | `META_CATALOGO_AGENTES` · `ADR-051 §2 §5 §9` · `ejecucion.py` · `apropiacion.py` |
| **cambio** | `CICLO_VIDA §5` · MDN `ADR-038 §9` · `REFORMA_SIMULADA_CNO-IV-001` · `DOC-031` |
| **confianza** | pesos de `procedencia.py` · `ADR-033` *«la analítica hereda la confianza de la evidencia»* · `ADR-046` techo por acreditación |

⚠️ **Alcance de este universo, declarado:** la orientación barrió `docs/` y `governance/` **sólo por
título**, y un barrido por título deja fuera lo que no nombra su tema —por ejemplo `ADR-045`—. La
tabla se completó desde el `MASTER_INDEX`, el propio arqueo y lo leído en `P0–P5`. **Antes de concluir
cualquier ausencia se barre por propósito** (`DOC-036 PASO 0-bis`).

**Método:** `DOC-035` · `DOC-036` · `DOC-037` y el corolario de presencia —*hallar una representación
no prueba su función*—. **Fuera de alcance:** la unificación de dominios, diferida por la dirección.

**Ejecución probatoria:** el colega precisó que leer y preparar no espera al CI; lo que espera es
declarar `P5` cerrado.

### `Q-M2-C · P0` — ¿circula hoy conocimiento entre dominios, o sólo existe la arquitectura que lo permitiría?

**La escalera que evita confundir existencia con circulación** (colega, 2026-09-14):

```
contrato documental → módulo existente → caller identificado → ejecución con evidencia → resultado reutilizado
      diseño              potencial          integración              operación              circulación efectiva
```

#### ⛔ Falsación 19 — el grafo de código dijo «nadie lo llama», y era falso

`CodeGraph` devolvió **«No callers found»** para `Consulta`, `consumir` y `atender`. Antes de
registrarlo se contrastó con un caso conocido: la prueba adversarial **los importa**, luego tiene que
llamarlos. La búsqueda literal lo confirmó: **9 invocaciones** que el grafo no resolvió, porque se
hacen como atributo de módulo —`D01.atender(...)`— y con nombres importados.

> **`CodeGraph` no puede utilizarse como prueba exclusiva de ausencia de callers en este universo.**
> *(Precisión del colega: no demuestra que la herramienta sea mala ni que la búsqueda estructural sea
> inútil.)* La regla que emerge: **herramienta estructural → contraste con un caso conocido → sólo
> entonces interpretar una ausencia.** Es `DOC-035`/`DOC-036` en práctica; no pide doctrina nueva.

#### La escalera, recorrida para la consulta interdominio

| escalón | estado | evidencia |
|---|---|---|
| **contrato documental** | ✅ **DEMOSTRADO** | `ADR-053 §6-bis`, sellado 2026-08-26 |
| **módulo existente** | ✅ **DEMOSTRADO** | `app/agents/consulta.py` (2026-08-30) · el lado que responde, sólo en `d01` —`motor.atender`— |
| **defensa de la frontera** | ✅ **DEMOSTRADO por lectura** | `consumir()` **lanza** si el consumo eleva el grado —*«cruzar la frontera no añade evidencia»*— o si cambia el sujeto; devuelve **la misma afirmación**, no una copia reinterpretada; lo que viaja es una afirmación sustentada, **nunca un valor suelto** |
| **caller identificado** | ⚠️ **SÓLO EN PRUEBAS** | las 9 invocaciones están en `tests/test_consulta_interdominio_adversarial.py`. **Ninguna** en `app/` · `quira_pages/` · `scripts/` · `sentinel/` · `utils/` · `views/` · `components/`, tampoco por nombre —*«atender»* y *«consumir»* fuera de esos dos archivos sólo aparecen en prosa ajena— |
| **ejecución con evidencia** | ⚠️ **PARCIAL** | las 3 pruebas corren donde está el Gold Master; **en un clon limpio —y en CI— se omiten**. La defensa de la frontera **no la verifica el CI remoto** |
| **resultado reutilizado** | 🔴 **NO DEMOSTRADO para este canal** | ningún dominio consume una `Respuesta` fuera de las pruebas. ⚠️ **No se generaliza**: `§5-undecies` demuestra circulación efectiva por **otro** canal |

**Universo:** todos los `.py` del repositorio sin worktrees ni caché, más YAML y JSON de las carpetas
de aplicación. **Fuera:** invocaciones desde fuera del repositorio, y lo que la UI pudiera
disparar por mecanismos no textuales.

#### Lo que `P0` deja, y corrige

> **La conclusión de `C3` sobrevive; su evidencia no.** `C3` decía *«reutilización efectiva no
> demostrada»* porque *«no hay consultas dominio → dominio»*, citando la medición del 2026-08-26.
> Hoy el estado es otro, y más preciso: **existe el contrato, existe el módulo, y la defensa de
> frontera está implementada y atacada por pruebas — pero no tiene un solo caller productivo.**
> Integración potencial, sin operación.

> ★ **Y por séptima vez, lo que la pregunta pedía ya existía — en una frontera.** El núcleo de
> `Q-M2-C` —*«sin que el tránsito cree confianza que no existía en el origen»*— **está implementado y
> probado en la frontera de consulta interdominio de evidencia**: `GradoElevadoAlCruzar`. ⛔ Eso NO
> quiere decir que QUIRA garantice globalmente la conservación de la confianza: es una frontera de
> varias, y `§5-undecies` encuentra otra donde la defensa no está.

**Lo que `P0` NO cubre** —los siguientes cortes—:

| plano | pregunta abierta |
|---|---|
| **memoria compartida** | ¿`MISMA_FUENTE_QUE` en Neo4j conserva la confianza al cruzar, o sólo declara identidad de fuente? — y en `005` une una `Fuente` con un `Dominio` |
| **norma → motor** | ¿la compilación `RO → artefacto firmado → Gold Master` (`ADR-039`) conserva procedencia y estado de la regla? |
| **motor → dominio → indicador** | ¿la analítica hereda la confianza de la evidencia (`ADR-033`), y dónde se verifica? |
| **cambio** | propagación normativa **diseñada**, operación **no determinada** · propagación epistemológica **no diseñada** — pregunta abierta, no doctrina |

#### Reconciliación de las cifras de la suite

El colega observó que *«941»* no cuadraba con *«877 + 65 = 942»*. **No hay contradicción, y se mide:**

| entorno | pasan | omitidas | fallan | total |
|---|---:|---:|---:|---:|
| máquina de Javo, con evidencia | 941 | 1 | 0 | **942** |
| clon limpio · `174c380` | 877 | 64 | 1 | **942** |
| clon limpio · `ffb581e` | 877 | 65 | 0 | **942** |

**942 pruebas recolectadas en todos.** *«941»* era el número de las que pasan en el entorno completo,
no el total — y citarlo sin decirlo fue impreciso. **La cifra que gobierna el cierre de `P5` será la
del CI remoto sobre el commit exacto que se cierre**, no una recordada.

**Convención desde aquí:** *«942 pruebas recolectadas; desglose de pass/skip/fail según entorno y
disponibilidad de corpus»*. Una cifra de pasadas sólo se cita con su entorno.

**Gobierno de los commits de `Q-M2-C`:** `c00e574` y los siguientes quedan **locales**. La autorización
de push de `bfec79d` no se extiende por inferencia a commits posteriores: cada push requiere
autorización específica o una autorización general explícita.

## 5-undecies · `Q-M2-C1` · CIRCULACIÓN INTERDOMINIO — y el canal que sí circula

### Orden de los cortes, fijado por el colega

| corte | frontera | pregunta |
|---|---|---|
| **C1** | evidencia entre dominios | ¿caller productivo, ejecución y reutilización? |
| **C2** | `MISMA_FUENTE_QUE` | ¿conserva identidad, procedencia y estado, o sólo declara que debería? |
| **C3** | BRN → compilación → Gold Master | ¿qué atributos de la regla sobreviven a cada transición? · MDN en tres escalones: **¿existe el esquema? → ¿existen nodos y aristas? → ¿se recorre ante un cambio?** |
| **C4** | Gold Master → dominio → indicador → inferencia | ¿conserva la inferencia la trazabilidad y las restricciones de lo que la originó? |

### La lección transversal — por octava vez, ya estaba escrita

El colega propuso, sin elevarla: *«la existencia de una representación, relación, módulo o registro
demuestra capacidad o diseño; sólo la evidencia de ejecución y consumo permite afirmar circulación
efectiva»*, y pidió comprobar antes si el corpus ya la formula. **La formula:**

| | dónde |
|---|---|
| *«capacidad ≠ ejecución ≠ validación»* — y ampliada a **cinco dimensiones** con sujeto y evidencia | `ADR-051 §2d` · ejecutada en `app/agents/apropiacion.py` |
| *«el estado de una etapa no acredita el trabajo de esa etapa»* | `ADR-051 §12-bis` |
| `declarado ≠ existente ≠ ejecutado ≠ exitoso` | `ADR-051 §12-bis` |

**Lo único que añade la formulación del colega es un escalón:** que **otro componente consuma** el
resultado. No hace falta doctrina.

### Por novena vez, el instrumento de `C1` ya existía

`app/agents/acoplamiento.py` construye un *«grafo de acoplamiento observable»* y advierte lo que un
análisis de imports habría omitido: *«los acoplamientos que más importan no son imports: d09 carga su
enricher por ruta, d07 abre YAML del BRN, los motores leen `gm_snapshot.json`»*. Y su guardián
`puede_afirmarse_ausencia()` **se niega** a sostener una ausencia mientras haya rutas sin resolver.

Por eso la búsqueda de **imports entre dominios devolvió cero**, y **cero no significa nada**: no es
el canal.

### ⛔ Falsación 20 — «cero artefactos compartidos» era la zona ciega del instrumento

Ejecutado `acoplamiento.py` sin modificarlo, atribuyendo cada módulo a su dominio con la residencia
que declara el `MASTER_INDEX` —**atribución de este análisis, declarada**—:

```
operaciones de acoplamiento en módulos de dominio ……  54
   ruta resuelta ……………………………………………………………  16
   ruta NO resoluble ……………………………………………………  38   ← 70 %
artefactos leídos por dos o más dominios …………………   0
```

**El instrumento se habría negado a afirmar esa ausencia, y tenía razón.** Resueltas las 38 a mano,
el canal compartido era **`data/gm_snapshot.json`**: cinco enrichers de tres dominios —d02, d03, d09 ×3—
lo leen **y lo reescriben entero**, y el motor de d09 lo lee. El análisis estático no lo veía por dos
formas concretas: `os.path.join(os.path.dirname(__file__), …)` no es literal, y una raíz escrita como
`.parent.parent` no coincide con el patrón `parents` con que se reconoce.

**Compartir archivo no es circular conocimiento.** Cada enricher escribe **su propio bloque**
—`presupuesto_dom` · `mandato_dom` · `rendicion`—. Circular es que uno **consuma el bloque de otro**.

### ★ El canal que circula: d01 → d02

`scripts/enrich_presupuesto.py:196-203`:

```python
# Alineación PND (H11b) + eje PND por meta — objeto compartido que NACE en d01 (se consume).
_al = (_snap.get("planificacion", {}) or {}).get("alineacion_pnd", {}) or {}
alineacion_pnd = round((_al.get("vinculacion_media") or 0) * 100) or None
pnd_metas = {m.get("id"): m.get("eje", "") for m in (_al.get("metas") or [])}
...
except Exception:
    alineacion_pnd, pnd_metas = None, {}
```

| escalón | estado | evidencia |
|---|---|---|
| **contrato documental** | ✅ **DEMOSTRADO** | `data/d02/catalogo_d02_v1.0.0.yaml`: *«H11b (consumido de d01, ADR-032)»* · *«se LEE, no se recalcula (Regla 1)»* |
| **caller productivo** | ✅ **DEMOSTRADO** | `enrich_presupuesto.py` es el *«motor real»* de d02 según el `MASTER_INDEX` |
| **ejecución con evidencia** | ✅ **DEMOSTRADO** | en el snapshot: d01 publica `vinculacion_media = 0.832` con 25 metas con eje · d02 guarda `elegibilidad.alineacion_pnd_pct = 83` |
| **resultado reutilizado** | ✅ **DEMOSTRADO** | **4 fondos** de d02 llevan `pnd_eje` copiado de d01 —*«Eje 3 — Servicios Básicos y Hábitat»*— |

> **La circulación interdominio efectiva está demostrada.** La formulación de `P0` —*«la circulación
> interdominio efectiva permanece no demostrada»*— **vale sólo para el canal de `consulta.py`**, y se
> restringe a él.

### ★★ Y lo que viaja por ese canal, leído contra la frontera que QUIRA ya defendió

| lo que `consulta.py` exige en la frontera | lo que viaja de d01 a d02 |
|---|---|
| *«nunca un valor suelto»*: afirmación con sujeto, evidencia, motor y grado | **un número y cadenas de texto por valor** · la procedencia viaja **sólo como prosa de bloque** —ver falsación 21— · el grado no viaja · el sujeto va **implícito en el archivo**, no en el valor |
| el grado no puede elevarse al cruzar | el grado **no viaja**, así que **no hay con qué comparar**: nada impide que d02 le atribuya luego un peso que d01 no sostenía |
| *«devuelve la misma afirmación, no una copia»* | **copia**: `0.832` pasa a `83`, y el eje se duplica dentro de los fondos. Si d01 cambia, la copia de d02 envejece hasta el próximo enriquecimiento |
| el tercer estado se preserva | `(x or 0) * 100 … or None`: **un cero real y un dato ausente llegan como el mismo `None`** · estructural, **no observado** hoy (el valor es 0,832) |
| un fallo no se lee como ausencia (`ADR-042 §6`) | `except Exception` → *«no pude leer d01»* llega como *«no hay eje PND»*. El gate de errores silenciosos **no lo mira**: sus zonas críticas no incluyen `scripts/` |

> ### **QUIRA presenta al menos dos mecanismos diferenciados de circulación interdominio: `consulta.py`, cuyo contrato incorpora controles explícitos de procedencia y de no elevación del grado, y el canal productivo d01 → d02 mediante `gm_snapshot.json`, cuya circulación efectiva está demostrada pero cuya conservación de procedencia y estado epistemológico durante el tránsito aún debe evaluarse.**
>
> *(Formulación del colega, 2026-09-15. La primera redacción —«el usado, sin defensa»— decía más de lo
> demostrado, y la falsación 21 lo confirmó.)*

#### ⛔ Falsación 21 — «la procedencia no viaja» se verificó buscando tres nombres de clave

La afirmación *«ni procedencia, ni grado, ni sujeto viajan · verificado en el snapshot»* se apoyó en
buscar `procedencia_pnd`, `grado_pnd` y `sostenida`. **El bloque de d02 tiene una clave `_fuente` que
no se miró.** Mirada:

| | lo que dice el snapshot |
|---|---|
| d01 · `planificacion._fuente` | *«PDOT · POA · PAC · coherencia · **corte Q1-2026**»* · y `alineacion_pnd` trae su propia clave `fuente`, **que d02 no lee** |
| d02 · `presupuesto_dom._fuente` | *«Presupuesto (cédula eSIGEF) · ISP · IEF · **alineaciones consumidas** · **corte Abril 2026**»* |
| d02 · `elegibilidad` | `alineacion_pnd_pct: 83` — sin procedencia propia |

**Lo que sí está demostrado, con precisión:** la procedencia viaja **como prosa, a nivel de bloque**:
reconoce que las alineaciones son consumidas, **no nombra a d01 ni a H11b**, y el valor queda bajo el
corte declarado del consumidor —*Abril 2026*— aunque su bloque de origen declara *Q1-2026*. **La
procedencia de bloque no distingue el corte de cada valor.** Si eso importa para la alineación PND
—que puede no depender del corte— es lo que `C4` tiene que evaluar, no esto.

Es la falsación 11 otra vez: **buscar una cosa en la forma de otra**, ahora dentro de `Q-M2-C`.

⚠️ **Lo que esto NO afirma:** que la confianza **se haya inflado** por este canal. No se observó. Se
afirma que **nada en este canal lo impediría ni lo detectaría**, que es exactamente lo que `Q-M2-C`
pregunta. Tampoco es una acusación al diseño, y las fechas lo explican —verificadas con `git log -S`—:

| | commit | fecha |
|---|---|---|
| lectura de `planificacion` desde el enricher de d02 | `6bb5436` | **2026-07-14** |
| nace `consulta.py` | `e6c60f0` · *«primera consulta **d02→d01** · se comparte evidencia, nunca verdad»* | **2026-08-30** |

> **La frontera defendida se construyó para exactamente este par de dominios, y el camino productivo
> siguió usando el canal anterior.** No es un canal olvidado: es la arquitectura previa que sobrevivió
> en código a su propio reemplazo.

**Destino `REARQ` candidato —PROPUESTO, decide la dirección—:** que la circulación d01 → d02 pase por
la frontera defendida, o que el canal por snapshot transporte procedencia, grado y sujeto. Es la
unión de las dos mitades que ya existen.

### Lo que `C1` NO cubrió

| | |
|---|---|
| **d06, el sintetizador** | identificado y **no recorrido**: vive en la capa de páginas (`quira_pages/p6_pulso`, `p7_brecha`, `m1_situacion`…) y `PCD-D06` lo declara *«el dominio que sintetiza evidencia producida por otros»*. Es la circulación interdominio por definición, y pertenece también a `C4` |
| **otras lecturas de bloques ajenos** | el universo de lecturas fue `scripts/enrich_*.py` y el motor de d09, por expresión regular sobre claves literales. **Claves construidas dinámicamente no se ven** |
| **escritura concurrente** | cinco productores reescriben el mismo archivo entero. Si dos corren fuera de orden, uno puede pisar el bloque de otro. **No observado**; se registra como pregunta |
| **el valor en el catálogo** | `catalogo_d02` lleva `alineacion_pnd_pct: 83` escrito: otra copia del mismo número, que envejece igual |

## 5-duodecies · `Q-M2-C2` · `MISMA_FUENTE_QUE` — lo que la relación significa operacionalmente

> **Pregunta, fijada por el colega:** *¿cuando QUIRA reutiliza una misma fuente entre dominios,
> conserva la identidad del artefacto, su procedencia y su estado epistemológico, o solamente
> reutiliza el dato derivado?* — y la advertencia: `C2` **no es una prueba de existencia de
> relaciones**, y no se declara que sea el mismo mecanismo que el canal de `C1`.

**Universo:** `.cypher` · `.py` · `.md` · `.yaml` · `.json` del repositorio sin worktrees ni caché · el
historial de git en todas las ramas · y **el grafo vivo de Neo4j**, consultado en modo lectura por el
conector del propio proyecto, sin exponer credenciales.

### `C2.1` · Existencia — dónde vive la relación

| dónde | resultado |
|---|---|
| **cypher** | **3 relaciones**: `003` `Fuente Presupuesto → CD-06` · `004` `Fuente eSIGEF_d02 → CD-06` · `005` `Fuente PDOT_metas_d03 → Dominio d01` |
| **grafo vivo** | **las mismas 3**, idénticas |
| **código que la escribe** | **ningún cargador localizado** —ni en `.py`, ni en `.sh`/`.ps1`/`.bat`, ni en workflows, ni instrucciones en `docs/architecture`— que ejecute los `.cypher` contra Neo4j. Cómo llegaron al grafo vivo: **`NO DETERMINABLE`** |
| **código que la LEE** | **ninguno**: ninguna consulta en `.py` recorre `MISMA_FUENTE_QUE` · las menciones en `d01/fuentes.py` y `d01/__init__.py` son docstrings |
| **documentos** | `MASTER_INDEX` · `ADR-053` · `META_CATALOGO_AGENTES` · `EVIDENCIA_d03` · `EVIDENCIA_d09` · `_template/README` · `DOC-036` |

### `C2.2` · Identidad — ¿apuntan al mismo artefacto?

| relación | lo que declara el propio nodo | lo que hace el código | ¿mismo artefacto? |
|---|---|---|---|
| `Presupuesto` (d01) → `CD-06` | `origen = 'portal_transparencia_DPE'` | la extracción es **`raise NotImplementedError`** —*«Fase 4 — NO IMPLEMENTADO»*—; el motor de d01 lee el **Gold Master** (`H16b`) | ⛔ **no** — d01 no consume artefactos de `CD-06` |
| `eSIGEF_d02` (d02) → `CD-06` | **`origen = 'Gold Master H07'`** | el enricher lee `sh("H07_S5")` | ⛔ **no** — d02 lee una hoja del Gold Master; d07 descarga el CSV de `CD-06` del portal |
| `PDOT_metas_d03` → `Dominio d01` | `origen = 'H03/PDOT (consumido de d01)'` | — | **otro tipo de relación**: el destino es un **dominio**, no una fuente |

**Prueba por contenido, y no refuta.** `OBS-011` —**CONFIRMED**— demostró que `CD-06` publica **sólo
la cédula de egresos**; la de ingresos está ausente. Si d02 leyera ingresos, no podrían venir de
`CD-06`. **d02 lee sólo egresos de inversión** —`Codificado_Total_Inversión` ·
`Devengado_Total_Inversión` · `Ti`—: el contenido es **compatible** con un mismo origen. Se registra así,
sin forzar el hallazgo.

> **La evidencia es compatible con un origen común en eSIGEF alcanzado mediante canales distintos.**
> *(Precisión del colega: la primera redacción decía «la relación expresa un mismo sistema de origen».
> **La relación no porta esa semántica**: la compatibilidad sale de triangular los nodos, el Gold
> Master, el canon y los artefactos observados, no de la arista.)*
>
> El canon ya separa las dos cosas: `REARQ_ARQUEO §365` `SISTEMA_ORIGEN ≠ CANAL_DE_ADQUISICIÓN`, y
> `§237` registra para eSIGEF tres canales —LOTAIP `CD-06`, transparencia pasiva, carga al Gold Master—
> con d02 *«OPERATIVO por vía indirecta»*. **El nombre de la relación promete más semántica de la que
> su estructura operacional acredita**, y al apuntar a `CD-06` —un conjunto de datos de un canal—
> **no distingue origen de canal**.

⚠️ Y el mismo nombre de relación une **dos tipos ontológicos** —`Fuente → CD` y `Fuente → Dominio`—:
`DOC-033`, lo nominal no autoriza a inferir identidad de naturaleza.

### `C2.3` · Procedencia — ¿qué viaja con el vínculo?

| | grafo vivo |
|---|---|
| **propiedades de las 3 aristas** | **ninguna** — `keys(r) = []` en las tres |
| nodo `Fuente` | `origen` (texto) · `descripcion` · `updated_at` |
| nodo `CD-06` | `guia_sha256` — **el SHA de la guía metodológica, no del artefacto de datos** · `estado_*` · `nota_reuso` · `reuso_cross_dominio` |

**Sin artefacto, SHA del dato, corte, captura, sujeto ni canal en la relación.** Que Neo4j tenga la
arista no demuestra que la procedencia viaje con ella: **no viaja**.

### `C2.4` · Estado epistemológico

**Nada en la arista.** El peso que `procedencia.py` asigna a una afirmación
—`no_determinable` · `hallazgo_de_verificabilidad` · `hecho_verificable`— **no existe en el grafo**.
`CD-06` sólo tiene `estado_empirica = true`, un booleano del conjunto de datos, no el grado de la
evidencia para quien la consume.

### `C2.5` · Efecto observable — ¿evitó una segunda adquisición?

**No.** La cédula entra a QUIRA por al menos dos canales independientes: d07 descarga `CD-06` del
portal por la API de la DPE, y d02 lee `H07_S5`, cargada al Gold Master por otra vía (`§237`). d01 no
extrae. **Ningún código recorre la relación**, así que no pudo evitar nada.

> **`relación existente ≠ reutilización efectiva`** — y en este caso **la reutilización no es
> operación: es intención.** El docstring de d01 lo dice sin ambigüedad: *«Budget/Presupuesto NO se
> re-extrae: se reusa la evidencia de d07 CD-06»* … dentro de una función que **lanza
> `NotImplementedError`**.

### ★ Y lo que el grafo vivo afirma, sin que el repositorio lo produzca

En el Neo4j vivo, `CD-06` tiene dos propiedades que **ningún archivo del repositorio escribe** —ni
`.cypher`, ni `.py`, ni `.md`— **y que no aparecen en el historial de git de ninguna rama**:

```
reuso_cross_dominio = ['d01_Planificacion', 'd02_Presupuesto']
nota_reuso          = "La cedula presupuestaria extraida aqui la consumen d01 y d02 sin re-extraer (colega 2026-07-22)"
```

| la memoria viva afirma | el código demuestra |
|---|---|
| d01 consume la cédula de `CD-06` sin re-extraer | la extracción de d01 **no está implementada**; lee el Gold Master |
| d02 consume la cédula de `CD-06` sin re-extraer | d02 lee **`H07_S5` del Gold Master** — su propio nodo lo declara |

Dos consecuencias, las dos ya nombradas por esta serie:

1. **Viola la conclusión de `P5`**: *la representación derivada debe ser reconstruible desde el estado
   actual del universo que pretende representar*. `d07/__init__.py` declara a Neo4j *«ÍNDICE
   DERIVADO»*, y este índice contiene afirmaciones que **ningún artefacto del repositorio reconstruye**.
   Origen: **`NO DETERMINABLE`** —el texto se atribuye al colega el 2026-07-22; no hay commit que lo
   escriba—.
2. **Es exactamente lo que `Q-M2-C` pregunta**: la memoria que, según `ADR-033`, consumirá QUIRA IA
   contiene **como afirmación** un reuso que la ejecución productiva no muestra. Una respuesta
   conversacional apoyada en ese grafo diría que d01 y d02 reutilizan la cédula. ⚠️ **No se afirma que
   la nota «nació de una decisión y la memoria la convirtió en hecho»**: su origen no está demostrado.
   Lo demostrado es la no correspondencia.

> ### Formulación del hallazgo, fijada por el colega
>
> **El estado derivado vivo contiene al menos una afirmación de reuso cross-dominio cuyo origen y
> mecanismo de generación no son reconstruibles desde el universo documental y de código
> inspeccionado, y cuya afirmación no coincide con los caminos productivos actualmente demostrados.**
>
> No es *«Neo4j está mal»*. Es **pérdida de trazabilidad del estado derivado** — y la regla que se
> sigue para QUIRA IA: **un índice derivado no adquiere autoridad porque contenga una propiedad que
> parece canónica.**

### Lo que `C2` corrige en el canon — sin modificarlo

| afirma | dónde | lo que `C2` demuestra |
|---|---|---|
| *«evidencia reutilizada (`MISMA_FUENTE_QUE`), nunca re-extraída»* | `MASTER_INDEX` · fila *Memoria operacional entre dominios* | declarada, **no operada** |
| *«Hoy hay **reuso de fuente**, no consulta entre agentes»* | `ADR-053 §6-bis` · medición del 2026-08-26 | ni siquiera el reuso de fuente es operación: es **declaración de origen común** |
| el *«contrato de evidencia interdominio»* que *«ya existe»*, con el principio *«la cédula se extrae una vez, no dos»* | `DOC-036 · por_que_ahi` | **existe la relación; el principio no se ejecuta** — la cédula se adquiere por dos canales |

⛔ **Nada de esto se toca aquí.** `ADR-053` está sellado, y el `MASTER_INDEX` y `doctrina.py` son
decisión de la dirección.

### Los patrones de circulación, con `C2` medido

| patrón | qué circula | estado |
|---|---|---|
| `consulta.py` | **afirmación gobernada** —grado, sujeto, motor— | contrato y defensa demostrados · **sin caller productivo** |
| snapshot d01 → d02 | **dato derivado, por copia**, con procedencia de bloque en prosa | **circulación efectiva demostrada** · conservación de procedencia y estado por evaluar |
| **`MISMA_FUENTE_QUE`** | **una declaración de origen común**, sin procedencia ni estado, **que ningún código lee** | **existe en cypher y en el grafo vivo · no opera** · y su nota viva afirma un reuso que el código no hace |
| BRN → Gold Master | regla compilada | **`C3`** |
| Gold Master → dominio → indicador | conocimiento derivado | **`C4`** |

### Destinos `REARQ` candidatos — PROPUESTOS, decide la dirección

| | |
|---|---|
| **retirar del grafo vivo, o marcar como intención**, `nota_reuso` y `reuso_cross_dominio` | afirman como hecho una operación que no ocurre · y **no son reconstruibles** desde el repositorio |
| **separar origen de canal** en la relación —p. ej. `MISMO_SISTEMA_ORIGEN` hacia un nodo de sistema, no hacia un `CD`— | es aplicar `§365`, que ya es canon |
| **dar a la arista la procedencia mínima** —canal, corte, SHA del artefacto— si ha de sostener reutilización | sin eso no puede sostenerla |
| **decidir si Neo4j se regenera sólo desde el repositorio** | es la misma pregunta de `P5-B` —*¿quién custodia la regeneración de los derivados?*— ahora para el grafo |

### El resultado de `C2`, congelado

> **`MISMA_FUENTE_QUE` está materializada en el grafo y su existencia es demostrable, pero su operación
> actual como mecanismo de reutilización de evidencia no está acreditada.** Las relaciones carecen de
> propiedades propias de procedencia y estado epistemológico, no se identificó código productivo que las
> atraviese y los casos examinados muestran adquisiciones por canales distintos. **Por tanto, la relación
> acredita actualmente una declaración de relación u origen, no una reutilización efectiva de evidencia.**
>
> Y: **el grafo vivo contiene al menos una afirmación de reutilización cuya procedencia de generación no
> es reconstruible desde el repositorio inspeccionado y cuya correspondencia con la ejecución productiva
> no fue demostrada.**

*(Formulación del colega, 2026-09-15. Ni «funciona» ni «no funciona». **Diagnóstico antes de cirugía**:
ni la semántica de `MISMA_FUENTE_QUE` ni las propiedades del grafo vivo se tocan hasta cerrar el arqueo.)*

### Lo que `C2` NO cubrió

- Si alguna **página** lee `reuso_cross_dominio` o `nota_reuso` del grafo y lo muestra: no se buscó en `quira_pages/` con consultas dinámicas.
- La **tensión** entre `CD-06 · estado_empirica = true` y la ausencia de ingresos que `OBS-011` confirma: puede ser coherente —publicado, aunque incompleto— y no se evaluó.
- **Las otras relaciones del grafo vivo**: sólo se examinó `MISMA_FUENTE_QUE`.

## 5-terdecies · `Q-M2-C3` · CIRCULACIÓN NORMATIVA — cuando una regla cambia, ¿por qué camino llega?

> **Pregunta, fijada por el colega:** no *«¿se usa el MDN?»*, sino **«cuando una regla normativa
> cambia, ¿por qué camino llega —si llega— el cambio al estado ejecutable?»**. Y la advertencia:
> **no repetir el error de `C1`** —encontrar el nombre de un mecanismo, buscar sólo ese mecanismo y
> concluir sobre toda la circulación—.

**Universo:** `docs/brn` · `ADR-038/039` · `BRN_CICLO_VIDA_Y_MOLDE` · `scripts/brn_*.py` ·
`app/agents/{canon,brn_lector}.py` · los enrichers y renders del caso · `data/brn_{config,manifest}.json` ·
`data/gm_snapshot.json` · la hoja `H24_SAT-IV` del Gold Master vigente, **leída en modo lectura** · y el
Neo4j vivo, **consultado en modo lectura**. Nada se modificó: los artefactos se verificaron intactos por
hash antes y después.

### Lo primero: el canon redefine la pregunta

`ADR-038 §9` fija un **límite duro**:

> *«la BRN traza el motor, NO lo alimenta … el Gold Master **no consulta la BRN** … la BRN **registra
> la relación** `umbral del H24 ← funda en → CNO-IV-001` y **detecta divergencias**; la traza va del
> motor hacia la BRN (para explicar), nunca de la BRN hacia el motor (para dictar).»*

Y `brn_compilador.py`: *«NO escribe el Gold Master vivo — genera artefactos; **aplicarlos al motor es
aparte, sobre COPIA con evidencia**»*.

> **No está demostrado un mecanismo automático y gobernado mediante el cual una modificación normativa
> alcance el derivado ejecutable del Gold Master; el diseño vigente establece que la BRN no alimenta
> directamente al motor en runtime.** La prueba de operación no es *«¿se propagó al Excel?»*: es **¿se
> identifica el impacto y se detecta la divergencia?** Y hay otro estado ejecutable además del Gold
> Master: **los motores Python de dominio**.
>
> *(Precisión del colega: la primera redacción decía «no llega por diseño», y el informe llegó a decir
> «no llega nunca». Mezclaba dos cosas —que la BRN no alimente al motor **en runtime**, y que el motor
> no pueda **recibir reglas compiladas**—. Lo segundo es falso: existe una compilación destinada al
> Gold Master. Lo no demostrado es la cadena `BRN → compilación → derivado → activación` como
> operación automática y gobernada.)*

### Al menos dos artefactos derivados de la BRN, con procesos, destinos y estados distintos

*(Precisión del colega: «dos compilaciones» confunde **proceso** con **artefacto**. Lo demostrado son
dos procesos distintos —dos scripts— que producen dos artefactos derivados.)*

| | proceso `brn_compilador.py` · `ADR-039` | proceso `brn_cno.py` |
|---|---|---|
| **artefacto** | `data/brn_config.json` + `brn_manifest.json` | `gm_snapshot.json["brn_cno"]` |
| **para** | el Gold Master, aplicado a mano sobre copia | los motores Python, vía `brn_lector` |
| **build** | **2026-07-20** | **2026-09-02** |
| **estado hoy** | ⛔ **`--verificar`: DIVERGE — falta recompilar** (exit 1). Contiene 5 RO; el canon de hoy compila **10**. **18 commits** tocaron `docs/brn` después del build, entre ellos `c014e2a` —*«las 9 piezas de d07 pasan a VIGENTE»*— | ✅ **al día**: canon `f9fa18c6f3b8bb9b` declarado = actual · integridad **16/16 CNO · 13/13 RO** · **sello de Javo del 2026-09-02 aplica** |

⚠️ Y el snapshot contiene además un **tercer bloque**, `snap["brn"]`: el **catálogo BRN v1** del
2026-07-18 —17 reglas a nivel de artículo, `COOTAD-192-R01`…, todas en `propuesta`—. **No es el que
lee el puente.** Confundirlo con él fue un error de lectura de este análisis, corregido antes de
registrarlo.

### `C3.1` · ¿El MDN es un esquema real?

✅ **Sí.** Definición formal en `ADR-038 §9` —*Modelo de Dependencias Normativas*, *«implementación
recomendada: Neo4j»*—. Tipos observados en el grafo vivo:

```
nodos     CNO · RO · SAT · SenalSAT · Dominio · Articulo · Norma
aristas   ESLABON_DE · OPERA_EN · DERIVA_DE · FUNDAMENTA_EN · CONSUME · FUNDAMENTADA_EN · RECIBE_DELEGADOS_DE
```

**Persistencia:** los `.cypher`, sin cargador localizado (`C2.1`).

### `C3.2` · ¿Tiene instancias reales?

✅ **Sí, y no es una maqueta.** El vecindario vivo de `CNO-IV-001` coincide **eslabón por eslabón**
con el ejemplo de `ADR-038 §9`:

```
CE_271 · COOTAD_192 · 198_1 · 198_2 · 198_6 · Transitoria  ─ESLABON_DE→  CNO-IV-001  ─OPERA_EN→ d02
                                              RO-IV-001  ─DERIVA_DE→  CNO-IV-001  ←FUNDAMENTADA_EN─ SAT-IV
```

⚠️ **Pero incompleto:** **12 CNO y 8 RO vivos contra 16 y 13 en disco. Faltan exactamente
`CNO-VII-001…004` y `RO-VII-001…005`** —toda la familia de Transparencia— y no sobra nada. Es el
**cuarto derivado** de esta serie envejecido de la misma forma.

### `C3.3` · ¿Se usa para recorrer impacto ante un cambio?

⛔ **No.** Ningún código lee `DERIVA_DE`, `ESLABON_DE`, `OPERA_EN`, `CONSUME` ni `FUNDAMENTA_EN`, y
**ninguna función calcula impacto** —búsqueda de `impacto` · `afectad` · `dependient` · `propaga` ·
`reforma` en nombres de función—.

> **El MDN existe como estructura de conocimiento y está poblado, pero no está demostrado como
> mecanismo operativo de propagación de cambios normativos.** *(Formulación del colega.)*

Las cuatro distinciones que el registro conserva, a pedido del colega:

| | afirmación | estado |
|---|---|---|
| 1 | **el MDN existe** | ✅ **DEMOSTRADO** |
| 2 | **el MDN está poblado** | ✅ **DEMOSTRADO PARCIALMENTE** — con el caso `CNO-IV-001`, y sin la familia VII |
| 3 | **el MDN se recorre para propagar reformas** | ⛔ **NO DEMOSTRADO** — no se identificó ningún recorrido |
| 4 | **la BRN produce derivados ejecutables** | ✅ **DEMOSTRADO** — pero su **regeneración y activación ante un cambio normativo o temporal no están gobernadas de extremo a extremo** |

**`MDN diseñado ≠ MDN poblado ≠ MDN operativo`.**

### ★ Pero la detección de divergencias SÍ existe — en otro sitio

La función que `ADR-038 §9` asigna a la BRN vive en **`app/agents/canon.py`**, no en el grafo:
`_vinculo_con_el_motor()` detecta **por qué vía llega una regla al código** y **qué parámetros
normativos quedaron copiados**; `copias_caducas()` avisa **por adelantado** —*«`65` hoy, **`70` desde
2027**: el 1 de enero habrá error, y nada avisaría»*—. **Por décima vez, lo que la pregunta buscaba ya
estaba construido.**

### El caso · `CNO-IV-001` → `RO-IV-001` → d02

La reforma simulada dice: *«el motor toma el umbral del tramo vigente a la fecha (**65 en 2026, 70
desde 2027**)»*. **Medido, en d02 la misma regla llega por DOS caminos:**

| | **camino A · puente BRN** | **camino B · celda del Gold Master** |
|---|---|---|
| **código** | `_umbral_de_la_regla()` → `brn_lector.regla("RO-IV-001")` | `u4 = _num(find(ws4, "Pct_Inversion_Minimo")) or 0.65` |
| **de dónde** | `snap["brn_cno"]`, verificado: vigente + al día + sello | celda **`H24_SAT-IV = 0.65`** —*«H01!B38=65%»*— y **literal `0.65` de respaldo** |
| **se publica en** | `isp.umbral_cootad` | la señal *«Alerta fiscal · estructura COOTAD»* |
| **custodia** | ✅ **4 pruebas**, con ataques: regla propuesta, catálogo desactualizado, sin sello | ninguna |
| **el docstring del camino A dice** | *«volver al literal como respaldo **reintroduciría la deuda**»* | …y el camino B **tiene** ese literal |

### ⛔ Y cuatro hechos que el caso deja al descubierto

**1 · El catálogo congela el tramo el día que se compila, y el candado no puede verlo.**
`brn_cno.py:170-179` resuelve `umbral_vigente` con `date.today()` **al compilar**. El candado de
`brn_lector` compara **sólo nombres y bytes del canon**. Demostrado sin tocar el sistema:

```
_umbral_vigente(RO-IV-001, 2026-12-31)  →  65
_umbral_vigente(RO-IV-001, 2027-01-01)  →  70
puente hoy: umbral_vigente = 65 · consumible · catálogo al día · compilado 2026-09-02
```

> **El 1 de enero de 2027 el canon no cambia de contenido: su hash sigue igual, el catálogo sigue «al
> día», el sello sigue acreditando, y el puente entregará `65` como consumible mientras la regla dice
> `70`** — hasta que alguien recompile. **Un candado por contenido no puede detectar un cambio que
> ocurre por el paso del tiempo.** Y es lo que el otro compilador declara prohibido: *«el compilador
> **nunca** pregunta qué tramo toca hoy — resolver la vigencia a una fecha es tarea del runtime
> (§4b)»*.

⚠️ **Y esto NO es un sello defectuoso** *(precisión del colega)*. El sello valida lo que dice validar:
**la correspondencia entre el compilado y el canon que se compiló**, y el hash lo cumple. Lo que falta es
**otro control**: *«este artefacto sigue siendo operacionalmente vigente en la fecha actual»*. Es
**cobertura incompleta del control de vigencia**, y exige separar tres controles que hoy van juntos:

```
integridad de contenido   ≠   vigencia temporal   ≠   activación operacional
   (el hash · existe)          (no existe)             (no gobernada)
```

**El hash del canon demuestra integridad del contenido que fue compilado; no demuestra vigencia
temporal del derivado compilado.**

**2 · El bloque publicado de d02 es anterior a la corrección.** El código actual publica
`umbral_cootad` como **diccionario** —valor, estado, tramos, procedencia—. El snapshot tiene el
**escalar `65`**, y se escribe sin transformación (`snap["presupuesto_dom"] = block`). **La cura de
`D-005` existe en el código y en sus pruebas, y su resultado nunca llegó a la publicación**: la última
escritura del snapshot (2026-09-03) la hizo el enricher de d08/d09.

**3 · El consumidor espera la forma vieja.** `presupuesto_render.py:203` hace
`isp.get("umbral_cootad") or 65` y formatea `%`, con la etiqueta `«regla 70% (dic-2026)»` escrita. Si
se regenera d02, **recibirá un diccionario donde espera un número** —incompatibilidad **demostrada por
lectura**, efecto en pantalla **no ejecutado**—. Y la capa de presentación **reintroduce `65` y `70`
como literales**, fuera del universo que inspecciona el detector.

**4 · El detector actual no cubre todas las formas de representación de una misma regla normativa,
particularmente puentes derivados y equivalencias escalares.** Es una **deuda instrumental
demostrada**, no un veredicto sobre el instrumento *(formulación del colega)* — y es el mismo patrón que
`CodeGraph` en `P0` y `acoplamiento.py` en `C1`: **instrumento de detección ≠ universo real**.

| el detector dice | lo que hay | por qué |
|---|---|---|
| d02 · `vinculo = solo_la_cita` | d02 **consume la regla por el puente** | reconoce `docs/brn`, `brn_cno`, `brn_manifest`, pero **no `brn_lector`** · **falsación 24** |
| d02 · `veredicto_parametros = limpio_comprobado` | `or 0.65` ejecutable | su patrón para `65` rechaza el número precedido de punto: **`0.65` no es `65` para él** |
| la prueba del literal | busca `return 0.65`, sí | pero **sólo dentro de `_umbral_de_la_regla`**; el `or 0.65` está en `build_block` |
| d08 · `solo_la_cita` | `scripts/enrich_participacion.py` pide `RO-VIII-003` al puente | ese enricher **no está en el universo** de d08 del detector |

### La respuesta a la pregunta

| estado ejecutable | camino del cambio | ¿automático? | ¿detección de divergencia? |
|---|---|---|---|
| **Gold Master** | compilado `ADR-039` → aplicar sobre copia con evidencia | ⛔ **no demostrado** · la BRN no alimenta al motor en runtime; depende de compilación, activación y su custodio | ninguna localizada que compare celdas del Gold Master con tramos de RO · y el artefacto compilado **diverge hoy** |
| **d07** | carga el YAML de la regla | ✅ sí | `canon`: `con_copias`, reportadas |
| **d02** | **A** puente verificado · **B** celda del Gold Master con literal | A ✅ · B ⛔ | el detector **no ve A ni la copia de B** · y A **congela el tramo** al compilar |
| **d08** | puente, para `RO-VIII-003` —en `propuesta`, así que no consumible— | — | fuera del universo del detector |
| **d01 · d03 · d09** | ningún uso del puente en su universo · sólo citan | — | — |
| **MDN · Neo4j** | ninguno: **sin lector** y sin la familia VII | ⛔ | ⛔ |

⚠️ **Rutas heterogéneas no es lo mismo que rutas incorrectas** *(precisión del colega)*. d07 consume
el YAML por `ROAdapter` y d02 por el puente: **existen rutas normativas de consumo heterogéneas que
deben reconciliarse arquitectónicamente**. Si corresponde unificarlas, mantenerlas diferenciadas,
jerarquizarlas o hacerlas consumir el mismo derivado, lo decide `REARQ` después. **No es un defecto
todavía.**

### El resultado de `C3`, congelado

> **La BRN tiene arquitectura normativa, el MDN tiene existencia y población real, pero no se demostró
> que el MDN sea actualmente el mecanismo que propaga una reforma normativa hacia los derivados
> ejecutables. La actualización efectiva depende de rutas de compilación y consumo heterogéneas,
> algunas de ellas con derivados congelados temporalmente y con al menos un respaldo literal que
> reproduce precisamente la clase de deuda que la BRN debía eliminar.**
>
> Y: **no está demostrado un mecanismo automático y gobernado mediante el cual una modificación
> normativa alcance el derivado ejecutable del Gold Master; el diseño vigente establece que la BRN no
> alimenta directamente al motor en runtime.**

*(Formulación del colega, 2026-09-15. `C3` queda **aprobado como diagnóstico**; la investigación no se
reabre.)*

### Correcciones a lo publicado

| # | se afirmó | lo que era |
|---|---|---|
| **22** | `P2/P3 §D`: *«7 RO compilan · 2 `no_determinable` · 1 `no_observable`»* | **10 vigentes · 3 propuesta**. Los `no_*` son casos borde **anidados** que la regla vigente declara. Corregido en `§5-quinquies D` |
| **23** | `P5-03`: `check_sat_brn` *«OBLIGATORIO — protege»* | **exit 0 siempre sin `--estricto`**: corre en el circuito, **informa y no protege**. Corregida la declaración en su docstring |
| **24** | *(no publicada)* «sólo d07 carga la regla» | **d02 la consume por el puente** — el detector no reconoce esa vía |
| **25** | *(no publicada)* «el candado del lector usa fechas» | la coincidencia era **«up-date»** en `h.update(...)`: el candado compara sólo contenido |

### Destinos `REARQ` candidatos — PROPUESTOS, decide la dirección

| | |
|---|---|
| **resolver el tramo en ejecución**, no al compilar —o hacer que el candado caduque en la fecha del próximo tramo— | cierra el hecho 1 |
| **llevar la señal de alerta de d02 al puente** y retirar `or 0.65` | cierra el camino B |
| **regenerar d02** y **adaptar el render** al diccionario, a la vez | los hechos 2 y 3 sólo se cierran juntos |
| **enseñar al detector** la vía `brn_lector`, la representación fraccionaria y la capa de presentación | el hecho 4 |
| **recompilar `ADR-039`** y **cargar la familia VII al MDN** — o declararlos derivados sin custodio | es `P5-B` otra vez: **cuarto y quinto derivado sin regeneración gobernada** |
| **comparar celdas normativas del Gold Master con los tramos de su RO** | la *detección de divergencias* que `ADR-038 §9` asigna a la BRN, del lado del motor |

#### ⚠️ El custodio de la regeneración no es una tarea: es gobierno del conocimiento

*(Precisión del colega.)* La pregunta *«¿quién regenera los derivados?»* ya apareció cinco veces
—registro, grafo de autoridad, testimonio de ejecución, artefacto `ADR-039`, MDN— y **no se resuelve
como pendiente técnico**. Es el equivalente normativo de un **circuito de release**:

```
CNO/RO cambia, o entra en vigor un tramo
      ↓   ¿quién detecta que hay que recompilar?
      ↓   ¿quién ejecuta la recompilación?
      ↓   ¿quién valida el resultado?
      ↓   ¿quién promueve el derivado?
      ↓   ¿qué artefacto queda vigente, y desde cuándo?
```

**`tener lifecycle definido ≠ tener lifecycle activado operacionalmente`.** El ciclo ya está diseñado
(`BRN_CICLO_VIDA_Y_MOLDE §5`, `§5b`) y **no se inventa otro**: lo que falta es **demostrar, y
eventualmente implementar, sus custodios y activadores**.

### Lo que `C3` NO cubrió

- **Cómo se aplica hoy un artefacto compilado al Gold Master**: el procedimiento sobre copia con evidencia no se observó.
- **Las otras señales SAT** del Gold Master y sus celdas: sólo se examinó `H24_SAT-IV`.
- **El comportamiento en 2027**, que se **simuló llamando a la función**, no ejecutando el sistema con otra fecha.
- **Qué hace hoy la pantalla** con el bloque publicado: la incompatibilidad se leyó, no se ejecutó.

## 5-quaterdecies · `Q-M2-C4` · Gold Master → dominio → indicador → inferencia · primer corte: el ICPI

> **Pregunta, fijada por el colega:** *¿aquello que el Gold Master afirma sobrevive correctamente
> cuando entra al dominio, se transforma en indicador y se convierte en inferencia? ¿Termina en una
> afirmación cuya semántica puede reconstruirse hasta la evidencia original?*

### Por qué el ICPI, y qué NO sirve como prueba

Se eligió un caso cuyo significado **ya está fijado por el canon**, para tener contra qué medir:
`DOC-024` y `D-014` establecen que `C_i` mide **calidad jurídica del proceso, no entrega material**, y la
`CARTA §2` clasifica *«Cumplimiento Institucional» como nombre del ICPI* en **📜 SUPERADO
METODOLÓGICAMENTE**.

⚠️ **El nombre por sí solo NO es la prueba.** La Carta dice *«no renombra nada — el nombre es el último
paso»* y `DOC-015` difiere la migración hasta que `011` decida qué mide el constructo. Que las páginas
sigan diciendo «Cumplimiento institucional» es **coherente con esa decisión**. Lo que se prueba es si
**lo que el motor adjunta al número llega a quien lo interpreta**.

**Universo:** `data/gm_snapshot.json["icpi"]` · `app/connectors/gold_master.py` ·
`quira_pages/{m1_situacion,p6_pulso,p7_brecha,p_command_center}.py` · `components/sentinel.py` · el
*system prompt* base de Sentinel, **construido en modo lectura** con `sentinel.prompts.build_system_prompt`
sobre `data.loader.load_all()`.

### Lo que el motor adjunta al número

```
icpi.global_pct      27.46          (27,4582 %, redondeado a dos decimales)
icpi.clasificacion   "Corte parcial - lectura preliminar (no comparable con umbral anual)"
icpi.historico       2023: 57.36 · 2024: 67.12 · 2025: 69.93
                     _nota: "Series históricas pendientes de validación analítica en v6.0"
icpi._nota           "ICPI mide velocidad de ejecución; TGI mide calidad institucional integral"
```

**El registro analítico trae su propia restricción epistemológica.** La pregunta es dónde se conserva.

### La cadena, tramo por tramo

| tramo | qué llega | ¿se conserva la restricción? |
|---|---|---|
| **Gold Master → snapshot** | valor · clasificación · serie con su nota | ✅ **sí** |
| **snapshot → `p7_brecha`** · indicador | valor, rotulado *«Corte parcial»*, con la clasificación en el encabezado y *«sin narrativa de caída»* | ✅ **parcial** — la serie 2023–2025 se rotula *«Cierre anual»* **sin** *«pendientes de validación analítica»* |
| **snapshot → `p6_pulso`** · indicador | valor con la clasificación en el encabezado | ✅ **sí** |
| **conector → `m1_situacion`** · dominio d06, `QINV-006` | `icpi_pct = 27.46` · `icpi_clasif = "Corte parcial - lectura preliminar (no comparable con umbral anual)"` | ⚠️ **se muestra, y la conclusión la contradice** — ver hallazgo 2 |
| **página → capa de razonamiento** · Sentinel, Claude Haiku | la pregunta redactada por la página | ⛔ **no** — ver hallazgo 1 |

### ⛔ Hallazgo 1 · el valor entra a la inferencia sin su restricción, y sin registro contra el cual contrastarlo

Los botones *«Analizar con IA»* (`p7_brecha`) y *«¿Qué hacemos esta semana?»* (`p6_pulso`) componen la
pregunta que consume `components/sentinel.py:167`:

> *«Al corte de abril 2026, el cumplimiento institucional de Montecristi es 27,5 %. Los vectores con
> mayor rezago son… ¿Cuáles son las acciones prioritarias del trimestre?»*
> *«Soy el alcalde de Montecristi. Al corte de abril el cumplimiento institucional es 27,5 %… ¿Cuáles
> son las 3 acciones más urgentes esta semana?»*

**Ninguna lleva la clasificación.** Y el *system prompt* base de Sentinel —25.200 caracteres,
construido en modo lectura— **no contiene el ICPI en ninguna forma**: ni el nombre, ni `27,4`, `0,27` o
`17,4`, ni «Índice Compuesto», ni «Progreso Institucional», ni la clasificación. `load_all()` no tiene
clave de ICPI.

> **El resultado analítico llega a la capa de razonamiento únicamente como una afirmación incrustada en
> la pregunta del usuario, desprendida de su registro analítico y de su restricción.** El modelo no
> tiene contra qué contrastarla. `ADR-033 §III` exige que la capa conversacional esté *«anclada a
> evidencia + índices, sin alucinar»*; aquí el ancla del índice no llega.

⚠️ **Límite declarado:** Sentinel añade bloques por pregunta —marco legal, vault normativo, RC-7.2,
contexto d4, memoria de conversación— y tiene un `trust_engine`. **No se inspeccionaron**. Tampoco se
ejecutó el modelo para ver qué responde.

### ⛔ Hallazgo 2 · una inferencia de dominio que no depende del valor

En `m1_situacion.py` la condición sólo distingue **sin dato** de **con dato**. Con cualquier valor
numérico, el titular y la conclusión son **texto fijo**:

```python
headline   = "El cumplimiento institucional necesita atención sostenida."
conclusion = ("El cumplimiento institucional está por debajo del nivel deseado para el corte. …")
```

Y la **misma tarjeta** exhibe como estado la clasificación del motor —*«no comparable con umbral
anual»*—. **La conclusión afirma una comparación que la restricción mostrada al lado prohíbe, y la
afirmaría igual con un ICPI de 90.** El semáforo, además, usa umbrales `50/75` escritos en el código,
no la clasificación del motor.

### ⚠️ Hallazgo 3 · una tensión semántica entre dos registros del canon — no creada por el tránsito

| registro | qué dice que mide el ICPI |
|---|---|
| **nota del motor** en el snapshot | *«**velocidad de ejecución**; TGI mide calidad institucional integral»* · *«D1-D5, ponderación ejecución-first»* |
| **ancla canónica de d06** (`PCD-D06`, Diccionario) y `QINV-006` | *«cumplimiento sostenible»* · hipótesis *«la capacidad institucional se mide por el cumplimiento sostenible de funciones»* |

**No la produce la página**: la página hereda el ancla de d06, que es canon. Es una **tensión entre el
registro del motor y el ancla del dominio**, del tipo `DOC-024` —*el propósito atribuido no es la
semántica demostrada*—, y se resuelve donde se decide el destino del ICPI: **`011-C4`**. `C4` la registra
y no la dictamina.

### Lo que NO apareció, y lo que no se pudo determinar

| | |
|---|---|
| **atribución de entrega material a `C_i`** | ✅ **no apareció** en `m1_situacion`, `p6_pulso` ni `p7_brecha`: ninguna menciona `C_i`, legalidad ni entrega |
| **si los seis «vectores» componen el ICPI** | ❓ **`NO DETERMINABLE` en este corte.** `p7_brecha` los titula *«vectores del cumplimiento institucional»* y dice que la IA dirá *«cuál pesa más **en el resultado**»*; el snapshot los llama *«6 vectores causales desde H73»*; el motor declara el ICPI como *«D1-D5»*. Probar si hay composición exige leer las dependencias de la fórmula en el Gold Master |
| **el corte** | observación: las páginas dicen *«abril 2026»*, el *system prompt* dice *«corte Q1-2026 (marzo 2026)»*, d01 declara `Q1-2026` y d02 `Abril 2026` |

### Falsación evitada

**26** · Con el primer universo —`quira_pages`, `app`, `utils`— la pregunta para la IA **no tenía
lector**, y se habría concluido que el salto a la inferencia no ocurre. Ampliado a todo el repositorio,
el lector está en **`components/sentinel.py`**.

### El resultado del primer corte de `C4`

> **En el caso del ICPI, la restricción epistemológica que el Gold Master adjunta al valor —corte
> parcial, lectura preliminar, no comparable con umbral anual— se conserva hasta la presentación del
> indicador, pero no en dos transiciones: la serie histórica pierde su nota de validación pendiente, y
> el valor entra a la capa de razonamiento como parte de una pregunta redactada, sin su clasificación y
> sin un registro analítico del ICPI en el contexto base del modelo. Además, una inferencia de la capa
> de dominio es un texto constante que no depende del valor y contradice la clasificación que muestra.**

Y lo que esto significa para la pregunta de `Q-M2-C`: **el tránsito no inflaba el número; perdía la
condición bajo la cual el número vale.** Es la forma más silenciosa de crear confianza que no existía
en el origen.

### Destinos `REARQ` candidatos — PROPUESTOS, decide la dirección

| | |
|---|---|
| **que el salto a la IA lleve la clasificación**, o que el contexto de Sentinel incluya el registro analítico del ICPI | cierra el hallazgo 1 |
| **derivar la conclusión de `m1_situacion` del valor y de la clasificación**, y retirar los umbrales del código | cierra el hallazgo 2 |
| **llevar la nota de validación pendiente** a la serie histórica | el primer tramo parcial |
| **llevar la tensión del hallazgo 3 a `011-C4`** | no se resuelve fuera de ahí |
| **declarar qué son los «vectores»** respecto del ICPI antes de atribuirles peso en el resultado | el `NO DETERMINABLE` |

### Lo que este corte NO cubrió

- Los bloques de contexto por pregunta de Sentinel y su `trust_engine`. *(Cubiertos después: verificación 3.)*
- **Qué responde el modelo**: no se ejecutó.
- Otros indicadores —TGI, SITA, índices de dominio— y otras inferencias.
- La composición del ICPI en la fórmula del Gold Master. *(Cubierta después: verificación 4.)*
- Las páginas en ejecución: todo se leyó en código, salvo la carga de datos y la construcción del *system prompt*.

### `C4-P0` · las cuatro verificaciones que pidió el colega antes de cerrar el ICPI

#### Precisiones de formulación, antes de las pruebas

| se escribió | se corrige a |
|---|---|
| el nombre «Cumplimiento institucional» como síntoma | ✅ ya estaba bien acotado: **la etiqueta no es por sí sola evidencia de deriva**; el nombre espera decisión canónica (`DOC-015`) |
| hallazgo 2 | **pérdida de condición de comparabilidad**: la capa de presentación conserva el estado *«corte parcial / no comparable con umbral anual»* y emite a la vez una afirmación de posición respecto de un *«nivel deseado»* cuya referencia, período y regla de comparación no están demostrados |
| *«la IA recibe la cifra sin contexto»* | **en el contexto inspeccionado de Sentinel no se identificó el ICPI ni su estado epistemológico; la pregunta transporta el valor y no la clasificación.** Esto demuestra una **debilidad del contrato de transporte**, no que el modelo haya producido una inferencia incorrecta: **no se ejecutó** |
| *«el tránsito no infla el número: pierde la condición»* | **en los tramos inspeccionados el valor no cambia, pero su condición epistemológica no se conserva íntegramente** — y lo más preciso: **la restricción permanece como metadato, pero deja de gobernar la inferencia** |
| el colega citó `DOC-034` como *«contrato de afirmación del indicador»* | ⛔ **`DOC-034` trata de no declarar ausencia ontológica sin agotar la evidencia primaria.** El canon que gobierna el paso de indicador a inferencia es **`ADR-051 §4`** —tres niveles semánticos, *«del nivel 1 al 3 no se salta»*— y el **Principio de No-Inferencia** (Carta Art. 4.5), que vigila `check_epistemico` |

> ### Criterio rector de `C4` *(formulación del colega)*
>
> **No basta comprobar que una propiedad existe en el destino. Hay que comprobar que la propiedad
> sigue gobernando lo que el destino permite afirmar.**

#### Verificación 1 · contrafactual controlado de `m1_situacion`

En laboratorio: se sustituyeron **en memoria** el cargador de datos y la salida a Streamlit, se ejecutó
`render()` con cinco valores y se capturó lo que `QINV-006` afirmaría. **El archivo del producto quedó
intacto** (hash verificado).

| ICPI | clasificación recibida | semáforo | conclusión |
|---:|---|---|---|
| 27,46 | corte parcial · no comparable | crítico | *«está por debajo del nivel deseado para el corte»* |
| 49,9 | corte parcial · no comparable | crítico | *idéntica* |
| 74,9 | corte parcial · no comparable | alerta | *idéntica* |
| **90,0** | corte parcial · no comparable | **verde** | *idéntica* |
| **90,0** | **«Excelencia anual»** | **verde** | ***idéntica*** |

```
titulares distintos ……… 1          conclusiones distintas ……… 1
```

> ✅ **DEMOSTRADO POR EJECUCIÓN: la inferencia textual de la tarjeta no depende funcionalmente del valor
> del ICPI, aunque determinados elementos de presentación sí responden a él.** Con 90 % y excelencia, la
> tarjeta se pinta de verde y afirma que el valor está *por debajo del nivel deseado*.
>
> *(Precisión del colega: no es «la página ignora el ICPI» —el color sí lo usa—. Lo demostrado es que
> **la conclusión es independiente de la variable**, y el caso de 90 descarta que fuera un efecto
> particular de 27,46.)*

#### Verificación 2 · de dónde salen los umbrales 50/75

**El motor codifica la condición de comparabilidad en su propia fórmula** —`H12!B34`, leída en modo
lectura—:

```
Clasificación_AVEP = IF( H07_S5!B22 >= 12 ,
                         IF(B33>=0.9 "Excelencia" · >=0.7 "Gestión por Mandato" · >=0.4 "Transición Crítica" · >=0.2 "Gestión por Ocurrencia" · "Ruptura Sistémica") ,
                         "Corte parcial - lectura preliminar (no comparable con umbral anual)" )

H07_S5!B22 = Mes_Activo (auto) = 4
```

**La restricción no es un comentario: es una guarda.** Con menos de 12 meses, el motor **se niega** a
clasificar.

| dónde | umbrales para el ICPI |
|---|---|
| **Gold Master** · `H12!B34` | **90 / 70 / 40 / 20**, sólo con 12 meses |
| `m1_situacion` | **50 / 75** — sin guarda temporal |
| `m2_alertas` | 50 / 65 |
| `p_sentinel_hub` | 70, rotulado *«ICPI-Metas 2025»* |
| `app/services/snapshot_diff.py` | 50 — *«Ruptura Sistémica»* |
| canon documental | 50 / 75 en `corpus_obsidian/00_CORE/05_SAT_SISTEMA` y `07_AVEP_LENGUAJE` · `NOMENCLATURA_CANONICA`: *«Rojo · Crítico · ICPI < 50 %»* |

> **Los 50/75 de `m1_situacion` no son los del motor: coinciden con una escala AVEP documental distinta
> de la vigente en `H12`, y se aplican saltando la guarda de 12 meses.** Y el producto usa **cuatro**
> umbrales distintos para el mismo índice.

⚠️ **¿Es sólo codificación visual?** Se separa en tres afirmaciones, como pidió el colega:

| | afirmación | estado |
|---|---|---|
| **A** | el estado visual cambia según 50/75 | ✅ **DEMOSTRADO** por ejecución |
| **B** | ese estado corresponde a una clasificación semántica *«crítico»* | ✅ **DEMOSTRADO en el código**: la variable vale literalmente `temp = "critico"`, y `NOMENCLATURA_CANONICA` asigna al rojo *«Crítico · ICPI < 50 %»*. ⚠️ **No se verificó** que el render use exactamente el token rojo canónico |
| **C** | esa clasificación es metodológicamente válida para un corte de cuatro meses | ⛔ **NO** — es lo que la guarda del motor impide |

> **El hallazgo, sin la palabra «color»:** *la página aplica una clasificación basada en umbrales
> distintos de los del motor, y lo hace sin preservar la guarda temporal que el motor usa para suspender
> la clasificación anual.*

**Y lo que esta verificación deja al descubierto es mayor que la página:** hay **pluralidad de reglas
semánticas para un mismo indicador** —fórmula, clasificación del motor, snapshot, cuatro páginas, AVEP
documental, nomenclatura—. **El Gold Master no es el único lugar donde vive la semántica del ICPI**, que
es exactamente lo que `GM-Ω` venía intentando establecer.

Dos observaciones del motor, **sin calificar**, para cortes siguientes: `Mes_Activo` se rotula
*«(auto)»* y contiene un `4` escrito · `Clasificación_Ti` (`H07_S5!B21`) aplica escala anual **sin
guarda temporal**.

#### Verificación 3 · todo el contexto que puede llegar a Sentinel

El prompt efectivo (`components/sentinel.py:631-651`) es la base más **nueve bloques**:

| bloque | de qué se construye | construido en lectura | ¿ICPI o su estado? |
|---|---|---|---|
| *system prompt* base | `load_all()` + PDOT | ✅ 25.200 car. | ⛔ no |
| memoria | conversación | ✅ vacío | ⛔ no |
| legal | la pregunta | ✅ 1.264 car. | ⛔ no |
| RC-7.2 | registros presupuestarios longitudinales · o routing normativo | ✅ 1.264 car. (routing) | ⛔ no |
| d4 | equidad territorial | ✅ 511 car. | ⛔ no |
| d3d4 | cruce temporal × territorial | ✅ vacío | ⛔ no |
| d3d4 normativo · d1 · d13 · d5 · síntesis | estado de sesión de los motores presupuestario y territorial | — dependen de sesión | ⛔ **ninguno recibe el ICPI como entrada** |

`vault_ctx` se calcula pero **no se concatena** al prompt. Y en todo el paquete `sentinel/`, «ICPI» sólo
aparece en etiquetas de fuente, rutas de palabras clave y un docstring.

> **En el universo de ensamblaje inspeccionado, el ICPI llega al modelo a través de la pregunta generada
> por la página, mientras que los bloques adicionales revisados no transportan su valor ni su condición
> epistemológica.** *(Formulación del colega. La primera decía «la única vía»: una búsqueda estática no
> autoriza una ausencia sobre contexto dinámico no ejecutado — `DOC-035` aplicado a este mismo registro.
> Cinco de los nueve bloques se examinaron por sus entradas, no construidos.)*

| | estado |
|---|---|
| **transporte deficiente** de la condición epistemológica | ✅ **DEMOSTRADO** |
| **inferencia incorrecta** del modelo | ⛔ **NO DEMOSTRADO** — el modelo no se ejecutó |

Dos observaciones, **sin calificar**: `sentinel/explain.py` rotula `"D2": "Planificación (ICPI)"` —una
**tercera** atribución de significado, junto a la del motor y la de d06— · y los gráficos citan como
fuente *«SIAP-ICPI Gold Master **v4.1**»*, cuando el vigente es **v5.7**.

#### Verificación 4 · ¿los seis «vectores» componen el ICPI?

Precedentes por fórmula del Gold Master, en lectura, **recorrido completo y sin `INDIRECT` ni `OFFSET`**.
**El ICPI depende de cinco hojas:** `H01_PARÁMETROS` · `H07_S5` · `H07b` · `H12` · `H14_PONDERADORES`.

| vector | celda en `H73` | hojas propias | ¿entra al ICPI? |
|---|---|---|---|
| IET | `B27` | `H99_ENGINE_CORE` | ⛔ **no** — ninguna hoja compartida |
| IGP 2026 | `B22` | `H10` · `H10b` · `H20b` | ⛔ **no** |
| IOC | `B23` | `H18_ITAM` | ⛔ **no** |
| ISP | `B11` | `H19_ICS_ISP` · `H04` · `H05` | ⛔ **no** — sólo comparte la **fuente** `H07_S5` |
| PSG | `B14` | `H16c` · `H04b` | ⛔ **no** — sólo comparte **fuentes** `H01`, `H07_S5` |
| **IED** | `B17` | `H17_IED` · **`H12_MOTOR_ICPI_CANÓNICO`** · `H12d` | ⛔ **no — al revés: el IED se calcula A PARTIR del ICPI** |

> ✅ **DEMOSTRADO: ninguno de los seis vectores compone el ICPI.** **Cinco de los índices examinados no
> aparecen como componentes de su fórmula; algunos comparten hojas de origen o insumos, pero no forman
> parte algebraica del cálculo.** *(Precisión del colega: compartir insumos no es composición, pero
> tampoco demuestra independencia estadística, causal ni ontológica, y eso no se probó.)* Y **uno es un
> derivado del propio ICPI**: la dependencia real es `ICPI → IED`, no `IED → ICPI`. `p7_brecha` los titula
> *«vectores del cumplimiento institucional»* y anuncia que la IA dirá *«cuál pesa más **en el
> resultado**»*; el snapshot los llama *«vectores causales»*; y la pregunta enviada a la IA pide
> *«acciones para fortalecerlos»*. **La relación de composición, y la causal, se crean en el tránsito:
> el motor no las tiene.**

⚠️ **Límite del método:** el rastreador sigue referencias `Hoja!Celda` y rangos; **no sigue nombres
definidos**. En el recorrido no apareció ninguna función dinámica.

### La matriz de conservación semántica del ICPI

*(Pedida por el colega para responder: ¿qué parte de la identidad epistemológica de la afirmación
sobrevive en cada salto?)*

La columna final es la que convierte el criterio rector en **prueba operativa** *(añadida a pedido del
colega)*: no pregunta si la propiedad **llega**, sino si **gobierna** lo que se afirma en la capa final.

| propiedad | Gold Master | snapshot | indicador · `p6`/`p7` | dominio · `m1` | IA · Sentinel | **¿gobierna la afirmación final?** |
|---|---|---|---|---|---|---|
| **valor** | ✅ 0,274582 | ✅ 27,46 | ✅ | ✅ | ✅ 27,5, dentro de la pregunta | ⚠️ **parcial** — gobierna el color de `m1`, **no su conclusión** (contrafactual) |
| **unidad** | ✅ razón | ✅ razón y % | ✅ % | ✅ % | ✅ % | ✅ **sí** |
| **corte** | ✅ `Mes_Activo = 4` | ✅ en la clasificación | ✅ *«abril 2026»* | ✅ | ⚠️ *«abril»* en la pregunta · el prompt base dice *«Q1-2026 (marzo)»* | ⛔ **no** — la clasificación de `m1` no lo usa · en la IA hay dos cortes |
| **estado epistemológico** | ✅ guarda de 12 meses | ✅ | ✅ | ⚠️ se muestra | ⛔ no viaja | ⛔ **no** en `m1` · **`NO DETERMINABLE`** en la IA (modelo no ejecutado) |
| **condición de comparabilidad** | ✅ | ✅ | ✅ parcial · la serie histórica pierde su nota | ⚠️ se muestra | ⛔ no viaja | ⛔ **no** — conclusión y semáforo la ignoran |
| **regla de interpretación** | ✅ AVEP 90/70/40/20 | ✅ la clasificación resultante | ✅ | ⛔ sustituida por 50/75 | ⛔ ninguna | ⛔ **no** — gobierna otra regla |
| **composición** | ✅ `Σ(P·R·V·E·T·C)/Σ(P·R)` | ⚠️ *«vectores causales»* | ⛔ *«vectores del cumplimiento»* | — | ⛔ premisa de la pregunta | ⛔ **no** — gobierna una composición inexistente |
| **procedencia** | ✅ `H12!B33` | ✅ `fuente: G4.1_ICPI` | ❓ no se inspeccionó | ❓ | ❓ | ❓ **`NO DETERMINABLE`** en este corte |
| **tipo de afirmación** | analítica | analítica | analítica | interpretación **constante** | conversacional | ⛔ **no** — la interpretación de `m1` no se deriva del resultado analítico (`ADR-033 §III`: la interpretación tiene estatus menor y se ancla a la evidencia). *No es un salto a `posible_incumplimiento` de `ADR-051 §4`: no hay calificación normativa* |
| **semántica de `C_i`** | ✅ en la fórmula | — | no representada | no representada | no representada | — **no representada**, así que no se distorsiona |

### Estado de `C4-P0`

> **CERRADO COMO DIAGNÓSTICO ANALÍTICO PARCIAL.**
>
> | verificación | estado |
> |---|---|
> | V1 · contrafactual | ✅ DEMOSTRADO |
> | V2 · umbrales | ✅ DEMOSTRADO |
> | V3 · Sentinel | ✅ DEMOSTRADO dentro del universo inspeccionado |
> | V4 · composición de los vectores | ✅ DEMOSTRADO |
>
> **El hallazgo principal, formulación del colega:**
>
> ***El problema observado no es una alteración del valor del ICPI durante su tránsito. El problema es
> que propiedades que condicionan lo que ese valor permite afirmar dejan de gobernar de manera uniforme
> las capas posteriores. El Gold Master suspende la clasificación anual cuando `Mes_Activo < 12`; la
> presentación introduce otros umbrales sin esa guarda; la inferencia textual de la tarjeta no depende
> del valor del indicador; Sentinel recibe el valor sin su condición epistemológica; y la presentación
> atribuye al ICPI una composición por seis vectores que no existe en su fórmula.***

**Canon aplicable** —corregido—: `ADR-033` · `ADR-051 §4` · Principio de No-Inferencia · `check_epistemico`
como instrumento operacional. **No se crea doctrina nueva**: el canon ya tiene la necesaria.

*Lo que el trabajo sostiene como método* *(colega)*: **no se corrige el canon para que encaje con el
hallazgo; se corrige el hallazgo para que encaje con el canon que realmente existe.**

**Estado administrativo:** commit `b51d8e2` y push **verificados por la salida de git** · **CI remoto
`NO DETERMINADO`** — su resultado no es legible con las herramientas de esta sesión.

**Las observaciones de V2 y V3 quedan fuera del hallazgo principal**, como reservas para los cortes
siguientes: `Mes_Activo «(auto)»` escrito a mano · `Clasificación_Ti` sin guarda · Sentinel rotula el ICPI
como *«Planificación»* · gráficos con fuente `v4.1`.

**No se modificó nada del producto, del motor, del Gold Master, del canon ni de Neo4j.** Siguiente:
**`C4-P1` · el Ti de d02**, para probar si la pérdida de condiciones interpretativas es un caso aislado o
un patrón.

## 5-quindecies · `Q-M2-C4-P1` · el `Ti` de d02 · ¿caso aislado o patrón?

**Instrucción del colega:** *«ya tenemos una señal concreta de que otra variable del mismo sistema
podría estar sometida a una regla temporal distinta. Eso permite probar si lo encontrado en el ICPI es
un caso aislado o si existe un patrón más general de pérdida de condiciones interpretativas.»*
**Criterio rector, el mismo de `C4`:** no basta que la propiedad exista en el destino; hay que
comprobar que **sigue gobernando lo que el destino permite afirmar**.

**Nada del producto, del motor, del Gold Master, del canon ni de Neo4j fue modificado.** Todo lo que
sigue es lectura y contrafactual de laboratorio.

### Universo inspeccionado — y lo que queda fuera

**Motor (lectura):** `H07_S5` (B10, B14-B23), `H07b`, `H19_ICS_ISP`, `H24_SAT-IV`, `H33`, `H73`,
`H01` (B33-B40), `H95`, `H97`, `H98`, `H12` (contraste) · dependientes de `H07_S5!B20-B23`,
`H19!B6/B7/B11`, `H24!B10`, `H01!B36/B37/B40` en **todas** las hojas del libro.
**Datos:** `data/gm_snapshot.json` (`presupuesto_dom`, `planificacion.presupuesto`, `financiero`,
`tgi.d3`) y los 9 `data/reportes_ciclo/CICLO_*`.
**Código:** `ti_pct`, `ti_2026_*`, `ti_2025_pct`, `absorcion_ti_pct`, `d3_ti_pct`, `top_entidad`
en `app/`, `scripts/`, `quira_pages/`, `components/` · enrutamiento en `quira_pages/env_gov.py`.
**IA:** `scripts/ia_criterio_planificacion.py` y la cadena `sentinel/budget_record_loader.py` →
`sentinel/calibration_layer.py` → `sentinel/d3d4_engine.py` → `components/sentinel.py`
*(ampliado tras la falsación 34; el modelo **no** se ejecutó)*.
**Excluidos y declarados:** `.claude/worktrees/*`, `quira_pages/_deprecated/*`, Neo4j, Supabase,
el resto de `sentinel/*`, publicación de `H33`.
⚠️ **No encontrado ≠ inexistente** (`DOC-035`/`036`): donde no hubo hallazgo se dice *no localizado
en el universo inspeccionado*.

### A · Qué afirma medir el `Ti`, demostrado por la fórmula vigente

*(El colega pidió no asumir que `Ti` sea «meses transcurridos». No lo es.)*

```
H07_S5!B18 Codificado_Total_Inversión_7+8 = B14+B16 = 30 271 811,74
H07_S5!B19 Devengado_Total_Inversión_7+8  = B15+B17 =  1 947 738,29
H07_S5!B20 Ti_Global_2026 = IF(B18>0, B19/B18, 0)   = 0,064342
H07_S5!B10 Fecha_Corte    = «Abril 2026 (Ene-Abr)»
H07_S5!B22 Mes_Activo (auto) = 4   ·   B23 FactorTemporal = CHOOSE(B22, curva…) = 0,212
```

> **`Ti = 0,064342 = 6,4342 % de ejecución acumulada de la inversión al corte enero-abril 2026.**
> Razón devengado ÷ codificado. Unidad: razón (0-1), publicada en %. Universo: grupos
> presupuestarios de inversión. **Observado, no proyectado.**
>
> El **factor temporal es OTRA celda** (`B23` = 0,212), y la magnitud normalizada es **otra más**
> (`H07b!B20 Ti_norm_2026 = MIN(1; B19/B23) = 0,3035`). Tres cosas distintas, no una.

⚠️ **El número desnudo no conserva semántica** —es justamente lo que `C4` está demostrando—, así que
en este registro el `Ti` **se escribe siempre con su unidad, su período y su universo**. *(Regla de
redacción pedida por el colega.)*

#### Corrección a una contaminación conceptual arrastrada de `C4-P0`

> **`T_i` NO significa «tiempo».** La letra dentro de la fórmula del ICPI inducía a leer *«factor
> temporal»* como *«tiempo transcurrido»*. La reconstrucción operativa lo desmiente: **`T_i` es una
> razón de ejecución acumulada respecto del codificado**. La temporalidad vive en **otra variable**
> (`FactorTemporal`) y la comparación entre ambas en **una tercera** (`Ti_norm`).
>
> ⛔ **No se renombra nada ahora.** Rige la regla que ya tenemos (`DOC-014`/`DOC-015`): **primero se
> determina la semántica, después la nomenclatura**. Queda anotado para cuando esa semántica esté
> cerrada.

⚠️ **Precisión sobre los componentes:** los rótulos `Codificado_Grupo7_Bienes` (29 654 120,37) y
`Codificado_Grupo8_Obras` (617 691,37) **no describen su contenido**: el codificado de *obras
públicas* del mismo snapshot es 15 840 150,70 —está dentro del primero— y 617 691,37 coincide
exactamente con la categoría *«bienes de larga duración»*. **El cociente no cambia**; el rótulo de
sus partes sí engaña. Registrado como precisión, no como defecto de cálculo.

### B · La misma magnitud tiene TRES reglas temporales, y las tres son de casa

| regla | dónde vive | valor para abril | `Ti` normalizado de 6,43 % |
|---|---|---|---|
| **curva de pacing 2025** | motor · `H07_S5!B23` (cirugía `D2A`, 2026-06-15) | 0,212 | **30,3 %** |
| **`W_Q` trimestral** | **canon** · Doctrina v1.3 §1.6 · `NOMENCLATURA §7.2` · `utils/top.py` | `Q2` = 0,35 | 18,4 % |
| **lineal `mes/12`** | nota `F20` de `H07b` · ficha forense `§7-ter.2` (2026-09-03) · compatible con `financiero.ti_2026_normalizada_pct` | 0,333 | 19,3 % |

Coinciden a **fin de trimestre** (`Q1` 0,128≈0,13 · `Q2` 0,36≈0,35) y **divergen dentro del
trimestre** y en `Q3` (0,766 frente a 0,60).

**Y hay una cuarta, descubierta al cerrar el contrato de transporte hacia la IA** *(§ IA)*:
`data/rc72_calibration.json` fija **baselines por entidad y grupo de gasto** —`GAD`:
`ti_q1_g7178` = **2,5 %**, `ti_q1_g5157` = 22 %, `ti_annual_expected` = 75 %; otras entidades 5,0/87
y 3,0/80— que la capa de calibración de Sentinel usa para decidir si un `Ti` bajo es estacional.
**2,5 % esperado en `Q1` frente al 12,8 % de la curva del motor para el mismo trimestre y el mismo
grupo.**

⚠️ Esto **no es un defecto del tránsito**: es una **tensión entre registros canónicos y operativos**
—como el hallazgo 3 de `C4-P0`— más una **nota desactualizada** por la cirugía de junio.
**Decisión de dirección, no de auditoría.** Lo que sí se registra: **la misma magnitud se compara
contra cuatro expectativas temporales distintas**, y sólo una de ellas gobierna el ICPI.

### C · La colisión `SAT-IV` — reconstruida antes de nombrarla

*(El colega exigió reconstruir objeto, corte, unidad, regla, umbral, pregunta, observado/proyectado y
vigencia **antes** de llamarlo contradicción. Aquí está.)*

| propiedad | **`SAT-IV` A** · `H19_ICS_ISP!B11` | **`SAT-IV` B** · `H24_SAT-IV!B10→B13` | **primo D3** · `H97!C20` |
|---|---|---|---|
| `Ti` que consume | `=H07_S5!B20` (vía `B9` *Pct_Inversion_Real*) | `=IFERROR(H07_S5!B20;0)` (vía `B9`) | `H07b!B18` |
| valor | 0,064342 | 0,064342 | 0,598535 |
| corte | Ene-Abr 2026 | Ene-Abr 2026 | **cierre 2025** |
| unidad · denominador | razón · codificado 7+8 | razón · codificado 7+8 | razón · serie anual |
| regla | `Ti < umbral` | `1 − Ti < umbral` | `Ti × 100 < 75` |
| umbral y su origen | `=H01!B33` → **`'Valor'`, el ENCABEZADO de la tabla** (el 0,65 vive en `B38`) | `=H01!B38` = 0,65 | 75 literal |
| pregunta declarada | *«¿inversión por debajo del mínimo COOTAD?»* | *«¿inversión por debajo del mínimo COOTAD?»* | *«¿D3 bajo el umbral crítico 75 %?»* |
| naturaleza | observada · vigente | observada · vigente | observada · **otro período** |
| veredicto en caché | ⚠️ *«Inversión por debajo del umbral mínimo COOTAD»* | ✅ *«Estructura fiscal conforme»* | *«ALERTA CRITICA D3=60 %»* |
| **quién la consume** | **nadie**: 0 dependientes en el libro · ningún lector Python localizado | `B13` → `B17` → `enrich_presupuesto._estado` → snapshot → cajón d02 | hoja de validaciones |

**Contrafactual variando ÚNICAMENTE el `Ti`** *(réplica de laboratorio de las fórmulas leídas)*:

| `Ti` | A · `Ti < 'Valor'` | B · `1 − Ti < 0,65` |
|---|---|---|
| 0,0000 | ⚠️ | ✅ |
| **0,0643 (hoy)** | **⚠️** | **✅** |
| 0,2120 (justo a ritmo en abril) | ⚠️ | ✅ |
| 0,3499 | ⚠️ | ✅ |
| **0,3600 (justo a ritmo en junio)** | ⚠️ | **⚠️** |
| 0,7000 · 1,0000 | ⚠️ | ⚠️ |

**Los tres hallazgos, separados y con el nombre que fijó el colega:**

> **⛔ `C.1` · DESACOPLAMIENTO INDICADOR → VEREDICTO. DEMOSTRADO.**
> *La alerta `H19!B11` declara evaluar el `Ti`, pero su condición efectiva compara contra un
> encabezado textual (`H01!B33`) y no contra el umbral numérico correspondiente (`H01!B38`). El
> contrafactual, variando exclusivamente el `Ti`, mantiene constante el veredicto. Por tanto, el
> veredicto no está funcionalmente gobernado por el `Ti`.*
>
> Es la estructura de `P0` un escalón más adentro: allí la **conclusión textual** era fija; aquí lo
> está **la propia condición lógica**.
>
> **⛔ `C.2` · SUSTITUCIÓN SEMÁNTICA DE MAGNITUD EN LA REGLA `SAT-IV`. DEMOSTRADO.**
> *`H24!B10` consume el `Ti`, pero lo transforma mediante `1 − Ti` y utiliza el resultado como
> participación estructural de la inversión. Dado que el `Ti` está definido como razón de ejecución
> presupuestaria, `1 − Ti` representa el complemento de ejecución, no la participación estructural del
> presupuesto. El contrafactual confirma que el veredicto se desplaza en sentido inverso a la
> ejecución. La fórmula conserva una dependencia numérica con el `Ti`, pero no conserva su
> significado semántico.*
>
> **Salvaguarda (colega):** esto **no demuestra** que la regla normativa del 65 % esté equivocada.
> Demostrado: `Ti` ≠ participación estructural, y `1 − Ti` = complemento de la razón de ejecución.
> **Fuera de `C.2` y no necesario para él:** cuál debería ser la fórmula normativa correcta. Eso es
> **REARQ/diseño, no diagnóstico** — no se intenta aquí.
>
> **⚠️ `C.3` · CONTRADICCIÓN INTERNA ACOTADA / ARTEFACTO INERTE. DEMOSTRADO Y ACOTADO.**
> A y B consumen **la misma celda, el mismo corte, la misma unidad, el mismo denominador y declaran
> la misma pregunta**, y hoy afirman lo contrario. **Pero no se puede decir que «QUIRA publica dos
> veredictos contradictorios»: sería falso.** A está desacoplada, tiene **0 dependientes** y ningún
> lector localizado; **sólo B alimenta la ruta productiva**. La formulación correcta:
> *existe una contradicción interna entre dos artefactos del universo inspeccionado, no entre dos
> resultados publicados, y el artefacto A es inerte respecto de la ruta productiva inspeccionada.*
> **No se eleva a defecto productivo.** Su valor es mostrar que el repositorio contiene **dos
> mecanismos que aparentan resolver la misma pregunta de maneras distintas**, uno sin ejecución
> productiva: **deuda de diseño que `REARQ` tendrá que clasificar**.
>
> **`H97!C20` · CASO DE CONTROL NEGATIVO. DEMOSTRADO.** Otro período (cierre 2025), otra referencia,
> otra pregunta y otra escala → **veredicto distinto ≠ contradicción**. No se «descarta»: se usa
> como control.

**Falsación decisiva de C.2:** hoy B dice *«conforme»*, y el cociente estructural que el propio
snapshot permite formar (codificado de inversión ÷ total municipal = 0,658) **también** caería del
lado conforme. **El resultado coincide; el gobierno no.** Es la clase de defecto que una prueba de
salida contra el valor esperado de hoy **no puede detectar** —sólo el contrafactual—.
`tests/test_d02_adversarial.py` verifica que el valor llega **idéntico** (que es lo que dice
verificar, y lo cumple); **no pretende** verificar gobierno.

**Y la vigencia tampoco gobierna:** `H24!B6 SAT_IV_Activa = H01!B40 = «SI»` literal *(marcado
«MALEABLE»)*; `H01!B37 Fecha_Vigencia_Regla_Fiscal` = 2026-06-01 **no la usa ninguna fórmula de
SAT-IV**, y el cajón d02 explica al lector que el seguimiento arranca el **1-dic-2026**. Tres fechas
conviven; **ninguna condiciona la activación**.

### D · HALLAZGO LATERAL, SEPARADO · el `ISP` de d02 empareja un valor de 2025 con la clasificación de un parcial de 2026

⚠️ **No pertenece a la colisión `SAT-IV` y no debe contaminarla** *(indicación del colega)*. Es **otro
caso de conservación temporal** y queda como **candidato a tratamiento posterior**, porque falta
reconstruir qué es el 58,4 % de la columna C: **histórico · referencia · benchmark · valor
comparativo · dato arrastrado · o texto de contexto**. Que el motor sea internamente coherente no
elimina el problema de presentación, **pero tampoco permite todavía llamarlo error**.

```
H19!B6  ISP_Global_2025_Ref  = IF(ISNUMBER(B12); IF(B12>0;B12;0,584); 0,584)  → 0,0322  (¡2026 parcial!)
H19!B12 ISP_2026_Real_eSIGEF = (B8 + POA/eSIGEF)/2                            → 0,0322
H19!B7  Clasificación_ISP    = escala sobre B6                                → «🔴 Atención Alta»
H19!C6  texto fijo                                                            → «58.40% — Transición Crítica»
```

**Dentro del motor todo es coherente:** `H28!B19/C19` publican `B6` y `B7` juntos (3,2 % + Atención
Alta). **La pérdida ocurre en el tránsito:** `enrich_presupuesto` toma el **valor** de la columna C
(texto 2025 → 58,4) y la **clasificación** de `B7` (calculada sobre el parcial 2026). El snapshot
queda `{58.4, «Atención Alta — Plan de mejora»}`, y así lo publican el cajón d02
(*«El índice de salud presupuestaria es 58.4% —Atención Alta—»*) y el agente
`d02.sostener_isp` con procedencia `leido_del_motor`. **Bajo la propia escala del motor, 0,584
clasifica como «🟡 Transición Crítica»** —lo que dice el texto de la columna C—.

⚠️ El comentario del enricher —*«col 2 = Ti, no ISP»*— **no se sostiene en el motor vigente**: `B6`
es el ISP 2026 parcial; el `Ti` está en `B8`. **La procedencia acredita el libro y el enricher, no la
celda ni el período.**

### E · Ficha forense de los consumidores del `Ti` *(formato pedido por el colega)*

| propiedad | motor `H07_S5` | snapshot | `SAT-IV` A | `SAT-IV` B | cajón d02 (`presupuesto_render`) | Planificación (`plan_render`/`m_planificacion`) | Concejo / Cadena | IA |
|---|---|---|---|---|---|---|---|---|
| `Ti` recibido | 0,064342 | 6,4 · **y 1,05** en `financiero` | 0,064342 | 0,064342 | 6,4 | 6,4 | **1,05** (respaldo literal) | 6,4 en el *prompt* |
| unidad | razón | % | razón | razón | % | % | % | % |
| corte | `B10` Ene-Abr · `B22`=4 | `ejecucion.corte` ✅ · `corte_datos` = «2026-03 (Q1)» | Ene-Abr | Ene-Abr | se **muestra**; la síntesis lo escribe literal *«corte Abril 2026»* | se muestra en el hallazgo | **`config.CORTE = "Q1-2026"`**, no el del dato | *«al corte»*, sin fecha |
| período/base | 7+8 · 30 271 811,74 | 30 271 811,74 · **22 595 464** en `financiero` | 7+8 | 7+8 | 7+8 | 7+8 | otra base | 7+8 |
| fórmula | `B19/B18` | copia | `Ti < umbral` | `1 − Ti < umbral` | color `_col_pct` | rama `ti < 30` | `TOP = Ti / W_Q` | — |
| umbral | 90/70/50/25 (`B21`) | — | texto `'Valor'` | 0,65 | 70 / 50 | 30 | 75/55/35 | — |
| guarda temporal | **ninguna en `B21`** (el ICPI sí: `B34` `Mes_Activo ≥ 12`) | no viaja | ninguna | ninguna | ninguna | ninguna | `W_Q` (otra regla) | ninguna |
| estado epistemológico | parcial declarado | parcial declarado | — | — | *«fase inicial del ejercicio»* constante | *«natural en el primer cuatrimestre»* constante | *«RUPTURA»* | — |
| afirmación permitida | razón acumulada a abril | ídem | — | — | ídem | ídem | ídem | ídem |
| afirmación emitida | `B21` «🔴 Atención» (sin consumidor) | — | ⚠️ estructura | ✅ estructura | *«riesgo de subejecución, principal alerta»* | *«la brecha reside en la velocidad»* | *«categoría RUPTURA · TOP 8,1 %»* | no materializada |
| **¿el `Ti` sigue gobernando?** | ⚠️ parcial | ✅ el valor | ⛔ **no** (C.1) | ⚠️ gobierna `1−Ti` (C.2) | ⚠️ gobierna el color, **no el dictamen** | ⚠️ gobierna la rama, **no la frase** | ⚠️ gobierna el `TOP`, no el titular | ❓ `NO DETERMINABLE` |

**Contrafactuales que sostienen la última fila** *(se varía sólo el `Ti`, sólo el corte, o ambos)*:

| superficie | `Ti`=6,4 abril | `Ti`=6,4 **diciembre** | `Ti`=25 abril *(a ritmo: `Ti_norm`=1,0)* | `Ti`=80 abril |
|---|---|---|---|---|
| `_absorcion` · color | 🔴 | 🔴 | 🔴 | 🟢 |
| `_absorcion` · texto | *«fase inicial del ejercicio»* | **igual** | **igual** | **igual** |
| `_sintesis` d02 | *«riesgo de subejecución… principal alerta»* | **igual** | **igual** | **igual** |
| `_implicaciones_plan` | *«brecha en la velocidad»* | **igual** | *«brecha en la velocidad»* | *«avanza dentro del calendario»* |
| `_hallazgos_plan` | *«Al corte X, la ejecución alcanza el N %»* | **usa el corte recibido** ✅ | ✅ | ✅ |

> El dictamen del cajón d02 **no cambia con ningún valor del `Ti`**: es la misma forma que el
> contrafactual de `m1_situacion` en `C4-P0`. `_hallazgos_plan` es el **caso de control**: conserva el
> corte y **no emite juicio** —ahí no hay pérdida—.
> `m_planificacion:641` escribe *«algo natural en el primer cuatrimestre»* **sin condición alguna**:
> la frase no depende del corte ni del valor *(lectura estática; la función necesita Streamlit)*.

**Cierre de la matriz de consumidores, en la estructura que fijó el colega** —el asterisco obliga a
**verificar** la semántica, no a asumirla—:

| consumidor | recibe `Ti` | usa `Ti` | usa su significado correcto | corte | regla | **¿gobierna la afirmación?** |
|---|---|---|---|---|---|---|
| `H19!B11` | ✓ | ✗ | ✗ | Ene-Abr | comparación defectuosa (contra encabezado) | **✗** |
| `H24!B10` | ✓ | ✓ | ✗ | Ene-Abr | COOTAD vía `1 − Ti` | **✗** |
| `H97!C20` | ✓ / referencia | ✓ | ✓* | cierre 2025 | regla propia (75 %) | **?** |
| producto d02 | ✓ | ✓ | ? | abril | regla publicada (70/50) | **?** — gobierna el color, no el dictamen |
| Planificación | ✓ | ✓ | ? | abril | rama `< 30` | **?** — gobierna la rama, no la frase |
| Concejo / Cadena | ✓ (otro corte) | ✓ | ? | `config.CORTE` | `TOP = Ti / W_Q` | **?** — gobierna el `TOP`, no el titular |
| IA · `RC-7.3` | ✓ (otra serie) | ✓ | ✓* | no viaja | baseline por entidad | **✓ dentro de la calibración** |
| IA · `criterio_planificacion` | ✓ | ? | ? | *«al corte»*, sin fecha | — | **`ND`** |

### F · El Concejo proyecta con el corte de la configuración, no con el del dato

`p_concejo.py:124` y `p_cadena_institucional.py:274` leen `financiero.ti_2026_raw_pct` **1,05 %**
—otro corte (`2026-03 (Q1)`) y otra base (22 595 464)— con **respaldo literal** `1.05`, y proyectan con
`top_entidad(ti, config.CORTE)`. **`financiero.corte_datos` no se lee.** Contrafactual: con
`CORTE="Q2-2026"` el mismo 1,05 pasa de `TOP` 8,1 a 3,0; con el string del snapshot
(*«Abril 2026 (Ene-Abr)»*) `quarter_desde_corte` **cae en silencio a `Q1`** —mismo patrón que el
`or 0.65` de `C3`—. El titular de la tarjeta A1 lleva la cifra **escrita a mano**
(*«Solo el 1.05% ejecutado en Q1»*, «$22.6M», «$238K»). ⚠️ **Falsación:** esa frase es el *argumento
de ataque anticipado del Concejo*, **no una afirmación de QUIRA**; lo que se registra es la **cifra
literal**, no el adjetivo. Ambas páginas están **enrutadas** (`env_gov.py:320` y `:378`).

### G · Lo que NO se demostró, y lo que quedó `NO DETERMINADO`

- **`Clasificación_Ti` (`B21`) sin guarda:** existe, pero **0 dependientes en el libro y ningún lector
  Python localizado** → **no gobierna ninguna afirmación publicada**. Baja de «hallazgo» a **reserva**.
- **La serie `presupuesto_dom.serie`** (2023 68,0 · 2024 79,6 · 2026 6,4) **no tiene consumidor
  localizado** → *no se publica una comparación entre cierres anuales y un parcial*. **Falsada mi
  observación preliminar.**
- **`ia_criterio_planificacion.py`** sí envía *«Ejecución de esa inversión al corte: 6.4%»* sin fecha
  ni factor, pero su salida (`planificacion.criterio_ia`) **no está en el snapshot vigente** y el
  modelo **no se ejecutó** en esta sesión → **`NO DETERMINABLE`** como afirmación emitida.

### El contrato de transporte hacia la IA — cerrado SIN ejecutar el modelo

*(El colega pidió exactamente esto: no hace falta una respuesta errónea del modelo para demostrar un
defecto de transporte; basta con establecer qué propiedades acompañan al `Ti` cuando llega.)*

**Mi primera lectura fue corta:** busqué términos del `Ti` en `components/sentinel.py` y no aparecieron.
**Hay vía, y pasa por otro módulo** *(falsación 34)*:

```
gm_snapshot.series_longitudinal.gad_inversion_g7178
  → sentinel/budget_record_loader.py  (RC-7.4)
  → RC-7.2 longitudinal  →  RC-7.3 sentinel/calibration_layer.py
  → describe_calibrated()  →  bloque inyectado en el prompt de Haiku
```

| propiedad | ¿acompaña al `Ti` hasta el prompt? |
|---|---|
| valor del `Ti` | ✅ sí — `«Ti actual: X %»` dentro de la narrativa |
| expectativa contra la que se juzga | ✅ sí — `«vs Y % esperado»` (baseline de la entidad) |
| clase y riesgo | ✅ sí — clase calibrada + `avep_riesgo` |
| confianza y peso evidencial | ✅ sí — `raw → calibrada`, peso evidencial |
| aviso de reclasificación | ✅ sí — *«Clase reclasificada … (calibración aplicada)»* |
| **fecha de corte explícita** | ⛔ **no** |
| **`seasonal_factor` numérico** | ⛔ **no** llega al texto *(su efecto sí gobernó antes)* |
| **el `Ti` del motor (`H07_S5!B20`)** | ⛔ **no** — este `Ti` es **otro**: viene de `series_longitudinal`, no de `presupuesto_dom` |

> **✅ Y aquí está el contraejemplo positivo de todo `C4`:** en `RC-7.3` la condición temporal **sí
> gobierna**. `_apply_seasonal_normalization` reclasifica `PARALISIS_ESTRUCTURAL → EXPANSION_TARDIA`
> y decae la confianza (×0,55) cuando el período es `Q1` y el grupo es de inversión; y
> `_has_mixed_frequency` **detecta que una serie mezcle períodos anuales con sub-anuales**
> —*apples-to-oranges*—. **Es la única guarda de comparabilidad hallada fuera del ICPI.**
> **El sistema ya sabe hacerlo en un sitio.** Eso convierte el problema de `REARQ` en propagación de
> una capacidad existente, no en invención de una nueva.

**Estado del transporte:** `Ti → IA` **parcialmente demostrado** (con valor, expectativa y clase).
`Ti + corte + FactorTemporal → IA` **NO demostrado**: el corte no viaja, el factor no viaja, y el
`Ti` que llega **no es el de d02**. **El modelo no se ejecutó** — y no hace falta.
- **Productor de `financiero.ti_2026_raw_pct` / `_normalizada_pct`:** no localizado en el universo
  Python (sólo lectores y copias del snapshot); introducido el 2026-05-17 (`7989774`). Mismo
  régimen que los derivados congelados de `C3`. El 4,21 es **compatible** con `1,05 / 0,25` (lineal),
  sin productor que lo acredite.
- **`tgi.d3`:** valor 59,85 (cierre 2025, coherente con `H98` y con la limitación que el propio motor
  declara en `H95!C8`), pero su `_nota_d3` afirma *«D3 usa siempre el período activo»* y atribuye
  59,85 a `PSG_EJECUCION` —que en el motor vigente apunta a `H16c` (presupuesto de género, 2,83 %)—.
  **Ningún lector Python de `_nota_d3` localizado**: metadato con condición falsa que hoy **no
  gobierna nada**, y que gobernaría si alguien lo leyera.
- **`m2_alertas`** rotula *«Ejecución (%)»* una columna que `longitudinal_engine:257` alimenta con
  `financiero.isp_salud_presup` —en el motor vigente, `H73 → H19!B12`, el **ISP** parcial—. El
  histórico de `CICLO_*` mezcla 0,1458 y 0,0322 bajo la misma clave. Origen del historial
  (`_load_supabase_snapshots`) **no inspeccionado**.
- **Hallazgo lateral, fuera del alcance de `C4-P1`, no investigado:** `H04b!K13:K37` usa
  `H01!B37` —una **fecha**— como coeficiente (`=1+B38*I+B37*J`), con caché 46 175. Mismo desfase de
  filas que el `'Valor'` de `SAT-IV` A. **Se registra; no se toca.**

### La matriz de conservación semántica del `Ti`

| propiedad | Gold Master | snapshot | `SAT-IV` publicada | cajón d02 | Planificación | Concejo | IA | **¿gobierna la afirmación final?** |
|---|---|---|---|---|---|---|---|---|
| **valor** | ✅ 0,064342 | ✅ 6,4 · ⚠️ 1,05 en otro bloque | ✅ | ✅ | ✅ | ⚠️ 1,05 + literal | ✅ en el *prompt* | ⚠️ **parcial** — gobierna color y rama; **no** el dictamen ni la frase |
| **unidad** | ✅ razón | ✅ % | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ **sí** |
| **corte** | ✅ `B10` · `B22` | ✅ dos cortes conviven | ✅ | ⚠️ se muestra · literal en la síntesis | ✅ se muestra | ⛔ manda `config.CORTE` | ⚠️ sin fecha | ⛔ **no** — ninguna afirmación evaluativa cambia con él |
| **factor temporal** | ✅ `B23` 0,212 | ⛔ no viaja | ⛔ | ⛔ | ⛔ | ⚠️ otra regla (`W_Q`) | ⛔ | ⛔ **no** — sólo gobierna dentro de `H07b→ICPI` |
| **regla de interpretación** | ⚠️ `B21` anual sin guarda *(sin consumidor)* | — | ⛔ `1−Ti` vs 0,65 · texto en A | ⛔ 70/50 propios | ⛔ umbral 30 propio | ⚠️ 75/55/35 sobre otra normalización | ⛔ | ⛔ **no** — cada superficie gobierna con su regla; ninguna es la del motor |
| **semántica de la magnitud** | ⛔ `SAT-IV` la lee como estructura | ⛔ *«estructura inversión/corriente conforme»* | ⛔ | ✅ *«absorción»* | ✅ *«ejecución»* | ✅ *«ejecución»* | — | ⛔ **no** en `SAT-IV` — el veredicto depende de la ejecución, no de la estructura |
| **período del derivado (`ISP`)** | ✅ coherente en `H28` | ⛔ 58,4 (2025) + clase del parcial 2026 | — | ⛔ lo publica | — | — | — | ⛔ **no** — la clasificación no corresponde al valor que acompaña |
| **vigencia de la norma** | ⚠️ `B37` = 2026-06-01, sin uso en `SAT-IV` | ⛔ no viaja | ⛔ literal `«SI»` | ⚠️ texto *«1-dic-2026»* | — | — | — | ⛔ **no** — la activación es un literal |
| **procedencia** | ✅ celdas | ⚠️ sin celda de origen en `ejecucion` | — | ✅ `evidencia_sha` + `motor_sha` · ⚠️ el `ISP` acredita el libro, no la celda | ✅ | ⚠️ literales sin fuente | — | ⚠️ **acredita el libro y el lector, no el período** |
| **tipo de afirmación** | analítica | analítica | clasificatoria | **interpretación constante** | interpretación por rama | proyección | conversacional | ⛔ **no** — `ADR-033 §III`: la interpretación tiene estatus menor y debe anclarse a la evidencia |

### La respuesta de `C4-P1`

> **No es un caso aislado: es la misma forma, y aparece en tres lugares distintos del circuito.**
>
> En el ICPI la condición se perdía **entre el motor y la presentación**. En el `Ti` se pierde
> **(1) dentro del motor** —`SAT-IV` A no depende del `Ti` que dice evaluar; `SAT-IV` B lo lee como
> estructura—, **(2) en el tránsito** —el `ISP` empareja períodos distintos; el agente d02 persiste
> `absorcion_ti_pct` **sin el corte**; el Concejo normaliza con el corte de la configuración— y
> **(3) en la presentación** —dictamen constante, umbrales propios, frases sin condición—.
>
> **La forma común: la propiedad está presente en el destino y no gobierna la afirmación.**
>
> ⚠️ **Alcance declarado:** *recurrente en los dos indicadores inspeccionados* (ICPI y `Ti`). Su
> extensión al resto de indicadores **`NO DETERMINADA`** — eso es lo que seguirían `C4-P2` y siguientes.

**Y una clase nueva que `C4-P0` no había mostrado:** **coincidencia de resultado sin gobierno**
(`SAT-IV` B). Ninguna prueba de salida contra el valor esperado de hoy la detecta. **Sólo el
contrafactual.** Es, además, el argumento para que las pruebas de `REARQ` incluyan
*«variar la condición con el valor fijo»* como criterio.

#### ⛔ Conclusión de arquitectura de `C4-P0 + C4-P1` — CONGELADA *(formulación del colega)*

> **En `C4-P0` y `C4-P1` no se observa principalmente corrupción del valor numérico durante el
> tránsito. Se observa pérdida o sustitución de las condiciones semánticas que determinan qué puede
> afirmarse a partir de ese valor. En el ICPI, la condición de comparabilidad deja de gobernar
> uniformemente las capas posteriores; en el `Ti`, el indicador puede llegar intacto pero ser
> desconectado del veredicto o reinterpretado como una magnitud distinta.**

**Y por eso `C4` no es una caza de bugs de página.** Lo que está apareciendo es más profundo:
**QUIRA puede conservar el número y perder el significado operacional que limita su
interpretación.** Ése es el problema que `REARQ` debe resolver.

### Falsaciones de esta fase *(instrumento, no producto)*

- **27 ·** el universo por el término `ti` incluía `p16_gobernanza:148` y `p19_genero:301`, donde `ti`
  es el **avance de una meta**, no la ejecución presupuestaria. Excluidos. *(Corolario de presencia de
  `DOC-035`: hallar el término no prueba la magnitud.)*
- **28 ·** *«la serie compara un parcial con cierres anuales»* → la serie **no tiene consumidor
  localizado**; no se publica esa comparación. Retirada.
- **29 ·** *«el Concejo afirma que la inversión está paralizada»* → es un **argumento de ataque
  anticipado**, no una afirmación de QUIRA. Se conserva sólo la cifra literal.
- **30 ·** *«`SAT-IV` da hoy un veredicto falso»* → hoy **coincide** con el cociente estructural que el
  snapshot permite formar. El hallazgo es de **gobierno**, no de resultado.
- **31 ·** *«el `TOP` es un motor paralelo no canónico»* → el `TOP` **es canon** (Doctrina v1.3 §1.6 ·
  `NOMENCLATURA §7.2`). Es **tensión entre dos registros canónicos**, no una infracción.
- **32 ·** *«el enricher lee mal la columna del `ISP`»* → lee la columna C **deliberadamente** tras
  `PCD-D02`. Lo que se registra es el **emparejamiento de períodos** y que la premisa del comentario
  (*«col 2 = Ti»*) no se sostiene en el motor vigente.
- **33 ·** *«`Clasificación_Ti` sin guarda es un defecto publicado»* → **sin consumidor localizado**.
  Queda como reserva.
- **34 ·** *«el `Ti` no llega a la IA»* → **sí llega**, por `sentinel/budget_record_loader.py` →
  `RC-7.2/7.3`, que mi primer universo (`components/sentinel.py`) no cubría. **El universo estrecho
  volvió a producir una ausencia falsa** —mismo error que la falsación 26—. Corregido: el `Ti` llega
  con valor, expectativa y clase; **sin corte ni factor**, y **no es el `Ti` de d02**.

### Estado de `C4-P1`

> **CERRADO COMO DIAGNÓSTICO ANALÍTICO PARCIAL** *(veredicto del colega, 2026-09-16)*.
>
> **No hay contradicción publicada entre dos alertas. Hay desacoplamiento, sustitución semántica de
> magnitud y una contradicción interna acotada a un artefacto inerte.**
>
> | hallazgo | estado |
> |---|---|
> | `C.1` · desacoplamiento indicador → veredicto | ✅ **DEMOSTRADO** |
> | `C.2` · sustitución semántica de magnitud | ✅ **DEMOSTRADO** |
> | `C.3` · contradicción interna entre artefactos, **no publicada** | ✅ **DEMOSTRADO Y ACOTADO** |
> | `H97` · caso de control — no contradicción | ✅ **DEMOSTRADO** |
> | serie histórica como consumidor productivo | ⛔ **FALSADA** — retirada del hallazgo |
> | `Ti` anual como requisito general | ❓ **`NO DETERMINABLE`** — reserva |
> | IA | ⚠️ **transporte parcial DEMOSTRADO** · conservación completa del contexto temporal **`NO DETERMINADA`** |
>
> **Tres reservas abiertas, por decisión del colega:** (1) **IA** — contrato de transporte cerrado,
> **sin ejecutar el modelo**; (2) **escala anual** — `NO_DETERMINABLE` hasta que haya evidencia
> suficiente; (3) **`ISP`** — hallazgo lateral separado.
>
> ⛔ **Regla de disciplina para el resto de `C4`:** **no se corrige `H19`, `H24`, `SAT-IV` ni el
> render durante `C4`.** *«La cirugía posterior se hace sobre una arquitectura entendida, no sobre el
> síntoma que acabamos de descubrir.»*

**Detalle de la demostración exigida antes del cierre:**

> | punto exigido por el colega | estado |
> |---|---|
> | qué `Ti`, corte, unidad, denominador consume cada alerta | ✅ **DEMOSTRADO** — la misma celda `H07_S5!B20` |
> | si responden la misma pregunta | ✅ **DEMOSTRADO** — texto idéntico del veredicto |
> | observada/proyectada · vigente/histórica | ✅ **DEMOSTRADO** — ambas observadas y vigentes |
> | contrafactual variando sólo el `Ti` | ✅ **DEMOSTRADO** — A constante · B se invierte en 0,35 |
> | tipo A · divergencia de regla | ✅ **DEMOSTRADO** (C.2) |
> | tipo B · contradicción de resultado | ⚠️ **DEMOSTRADO DENTRO DEL LIBRO** · **no** como veredicto publicado (A es inerte) |
> | tipo C · desacoplamiento | ✅ **DEMOSTRADO** (C.1) |
> | ¿la escala anual es semánticamente exigible al `Ti`? | ⚠️ **PARCIAL** — el motor lo declara para D3 (`H95!C8`), lo opera para el ICPI (`B34`) y construye `H07b` para eso; `B21` no lo aplica **pero no tiene consumidor** |
> | ¿la IA recibe el `Ti` y su condición? | ❓ **`NO DETERMINABLE`** |
> | ¿hay defecto en el **cálculo** del `Ti`? | ⛔ **NO** — el cociente es correcto; lo que falla es lo que otros hacen con él |

**No se declara** que el `Ti` esté mal calculado, ni que `SAT-IV` esté *«roto»*, ni que exista una
contradicción publicada. **No se creó ADR ni doctrina.** No se tocó Gold Master, motor, snapshot,
SAT, páginas, canon ni Neo4j.

### Destinos `REARQ` candidatos — PROPUESTOS, decide la dirección

⛔ **Ninguno se ejecuta durante `C4`** *(regla de disciplina del colega)*: se anotan para que la
cirugía se haga después, **sobre una arquitectura entendida**.

1. **`SAT-IV` A (`H19!B10`)** — apunta al encabezado `H01!B33` en vez del umbral `B38`: corregir la
   referencia **o retirar el gemelo inerte**. *(Sobre copia, con evidencia · Regla 1.)*
2. **`SAT-IV` B (`H24!B10`)** — alimentarla con el **cociente estructural** (inversión ÷ presupuesto),
   no con `1 − Ti`; y condicionar la activación a `H01!B37`, no al literal `«SI»`.
3. **`ISP` de d02** — valor y clasificación del **mismo período**; rotular `B6` por lo que devuelve;
   corregir el comentario del enricher.
4. **Agente d02 (`ADR-053`)** — que `absorcion_ti_pct` **viaje con su corte**; `leido_at` ≠ corte.
5. **Cajón d02 y Planificación** — derivar dictamen, color y frase del `Ti` **normalizado** o del
   corte; retirar los literales *«corte Abril 2026»* y *«primer cuatrimestre»*.
6. **Concejo / Cadena** — tomar el corte **del dato**; retirar los respaldos literales y el `Q1`
   silencioso de `quarter_desde_corte`.
7. **Una sola regla temporal del `Ti`** — curva del motor · `W_Q` de la Doctrina · nota `mes/12` ·
   baselines de `rc72_calibration.json` (2,5 % en `Q1` frente al 12,8 % de la curva): **decisión
   canónica**, con la nota `F20` y la ficha forense §7-ter.2 alineadas. → junto a `011-C4`.
8. **`tgi.d3._nota_d3`** — corregir o retirar; y resolver la colisión del nombre `PSG_EJECUCION`.
9. **`m2_alertas`** — o la columna deja de llamarse *«Ejecución (%)»*, o deja de alimentarse del `ISP`.
10. **Pruebas de gobierno** — contrafactual *(fijar el valor, variar la condición)* como criterio de
    aceptación, junto a las pruebas de identidad que ya existen.
11. **Propagar la guarda que ya existe** — `_apply_seasonal_normalization` y `_has_mixed_frequency`
    de `RC-7.3` son la única condición temporal que gobierna fuera del ICPI. **`REARQ` propaga una
    capacidad existente; no inventa una nueva.**

### Lo que `C4-P1` NO cubrió

Neo4j y el MDN · Supabase y el origen del historial de `m2_alertas` · el resto de `sentinel/*` fuera
de `calibration_layer`, `d3d4_engine` y `budget_record_loader` · la publicación de `H33` · el
productor de `financiero.ti_2026_*` · `_deprecated` y `worktrees` · la ejecución del modelo de
`ia_criterio_planificacion` *(deliberadamente no ejecutado)*.

**Siguiente: `C4-P2`**, con las tres reservas abiertas y la regla de disciplina vigente —no se toca
`H19`, `H24`, `SAT-IV` ni el render mientras `C4` siga corriendo—.

## 5-sexdecies · `Q-M2-C4-P2` · d09 · cuando la condición limitante es EPISTÉMICA

**Por qué este corte** *(hipótesis discriminante del colega)*: `C4-P0` y `C4-P1` hallaron pérdida de
condiciones **temporales**. Si la misma pérdida aparece cuando la condición es **epistémica**
—estado de evidencia, trazabilidad, carácter experto de la evaluación—, entonces no estamos ante
anomalías particulares sino ante una **clase**. Objeto: `IGP_3_Fidelidad_MFN_Global` / fidelidad
narrativa de d09. **No se tocó nada; el modelo no se ejecutó.**

### La barrera de independencia — resultado: PARCIAL, y con el punto exacto localizado

> **La cadena de evidencia y evaluación de d09 es independiente de la cadena de cálculo del `Ti` y
> del ICPI; el tramo de señalización SAT comparte infraestructura con `SAT-IV`.**

- **Independiente:** `H34b` sólo es consumida por `H39` (chequeo de lenguaje), `H85` (log) y `H89`
  (trust score). **`IGP_3` fue RETIRADO el 2026-07-29** (`H20b!A8` · nota `B12`), así que la fidelidad
  **no entra al IGP, ni al ICPI, ni al TGI**. Fuente distinta (video oficial + evidencia documental),
  unidad distinta, evaluación distinta.
- **Compartido:** el circuito CPCCS desemboca en `H75_SAT_ENGINE` → `H73_OUTPUT_API`, **la misma
  cañería de `SAT-IV`**. Todo lo que ocurra ahí queda marcado como **tramo común**, no como resultado
  de d09.

### `C4-P2-A` · Colapso epistemológico de la ausencia de evidencia en `SAT-V`

```
H24b!B7  Compromisos_CPCCS  = 0                     ← no hay datos (los informes no publican la tabla)
H24b!B9  Brecha_Compromisos = IF(B7=0; 0; 1-B8/B7)  → 0
H24b!B17 SAT_V_Estado       = IF(B9>0,3…;B9>0,1…)   → «✅ Sin señal SAT-V»
H75!D7 → E7 «INACTIVO» → G7 = 0,05 × 0 = 0 → B12 RIESGO_TOTAL = 0,2 «MEDIO» → H73!B29/B30
```

| estado real | `B7` | brecha `B9` | veredicto |
|---|---|---|---|
| **no existen datos para evaluar** | 0 | **0** | ✅ Sin señal · INACTIVO · peso 0 |
| **datos completos, cumplimiento perfecto** | `B8=B7` | **0** | ✅ Sin señal · INACTIVO · peso 0 |

> **El sistema no conserva la distinción entre «no evaluable por ausencia de evidencia» y «evaluado
> sin brecha».** Es una propiedad semántica, no un error aritmético.

**Y la misma hoja sí conserva el estado donde no gobierna:** `B19` dice *«Sin datos de compromisos
CPCCS registrados. Ingresar datos de la última RDC en B7 y B8.»* — texto honesto que **no alimenta la
señal**.

**Los tres defectos, separados como exigió el colega:**

| | qué afirma | estado |
|---|---|---|
| **A · cálculo** | la fórmula convierte `B7=0` en `brecha=0` | ✅ **DEMOSTRADO** |
| **B · interpretación** | ese `0` se trata como ausencia de señal, inactividad y contribución nula al riesgo en `H75` | ✅ **DEMOSTRADO** |
| **C · impacto en el producto actual** | que ese riesgo sea el publicado | ⛔ **NO DETERMINADO** |

**Dónde termina exactamente la cadena demostrada:** en `H73_OUTPUT_API`. Más allá, `gm_snapshot.json`
trae `sat = {}` (el bloque del pipeline, vacío) y lo que leen las páginas es otro bloque, `sat_gm`
—ver el apartado siguiente—. **Por tanto NO se afirma que el producto publique hoy la ausencia de
evidencia como ausencia de riesgo: eso es `NO DETERMINADO`.**

> **⚠️ Hallazgo de intersección con `C3`, FUERA de la demostración de `P2`.** El bloque `sat_gm`
> que leen `p_ejecutivo:114` y `p6_pulso:37` es un **derivado congelado del 2026-05-26** que **no
> coincide con el motor vigente**: dice `riesgo_total 0,35 · ALTO · 3 activas` frente al
> `0,2 · MEDIO · 2` que el motor calcula hoy, y **describe las SAT con otra semántica** —su `SAT-IV`
> es *«brecha territorial `IRS=79.7`»* (la `SAT-VIII` del motor) y su `SAT-V` es *«densidad de
> trazabilidad insuficiente»*, no la brecha CPCCS—.
>
> **Pertenece a `C3` (derivados congelados · gobernanza de materialización), no a `C4-P2`.** No se
> usa como evidencia adicional de `P2`: usarlo para inflar el hallazgo sería cometer el defecto que
> `C4` investiga.

**El cero no llega a la página, y llega a no llegar por accidente:** `enrich_rdc._clean(0)` hace
`str(s or "")`, y en Python `0` es *falsy* → devuelve `""` → el snapshot guarda
`brecha_compromisos: ""` → el cajón imprime «—» (`m_rdc:201`, `or "—"`). **La honestidad del
resultado publicado no es una decisión: es un efecto colateral del lenguaje.**

**Contrafactual del cajón** *(el cajón es fiel transportador; la pérdida está aguas arriba)*:

| lo que recibe | lo que publica |
|---|---|
| `""` (cadena real hoy) | *«la brecha de compromisos…: **—**»* |
| `"0%"` | *«…: **0 %**»* |
| `"sin evidencia — los informes no publican la tabla"` | *«…: **sin evidencia — los informes no publican la tabla**»* |

### `C4-P2-B` · Conversión silenciosa de un fallo de lectura en ausencia de penalización (`H89`)

```
H89!B27 MFN_BRECHA_NARRATIVA   = IFERROR(1-AVERAGE(H34b!L11:L37); 0)     → 0
H89!B28 PENALIZACIÓN_MFN       = IF(…>0,15; "⚠️ -10pts"; "✅ Sin penalización")
H89!B29 TRUST_AJUSTADO         = 89,6  (sin ajuste)
```

La columna `L` (`IF_n`) está guardada **como texto** (`'1.00'`, `'0.88'`, `'0.31'`). `AVERAGE` ignora
el texto; sin ningún número en el rango devuelve error; `IFERROR` lo convierte en **0**.

**Formulación acotada** *(corrección del colega)*: **en el estado actual, donde los `IF_n` de `H34b`
están almacenados como texto, la fórmula `AVERAGE(H34b!L11:L37)` no puede utilizar esos valores
textuales como valores numéricos; al no disponer de valores numéricos utilizables, el error queda
absorbido por `IFERROR(…;0)` y la penalización resulta 0.** ⚠️ **No se generaliza a «ningún valor
textual»**: una mezcla de números y texto permitiría a `AVERAGE` operar sobre los numéricos.

**Evidencia:** el valor observado en caché (`B27 = 0`) **es incompatible con una lectura numérica de
los nueve valores actuales bajo la fórmula examinada** —que daría `1 − 0,91 = 0,09`— y el
contrafactual reproduce el comportamiento esperado. **No se ejecutó Excel**: la réplica es de
laboratorio y así queda declarada.

**Contrafactual mínimo** *(se varía sólo el estado de la columna)*:

| escenario | `B27` | veredicto |
|---|---|---|
| hoy · `IF_n` como **texto** | 0,0000 | ✅ Sin penalización |
| `IF_n` **numérico**, mismos valores | 0,0767 | ✅ Sin penalización |
| `IF_n` **numérico** pésimo (0,10) | 0,9000 | ⚠️ **PENALIZACIÓN −10 pts** |
| `IF_n` **numérico** nulo (0) | 1,0000 | ⚠️ **PENALIZACIÓN −10 pts** |
| columna **ilegible/vacía** | 0,0000 | ✅ Sin penalización |
| **texto** con valores pésimos (`'0.10'`) | 0,0000 | ✅ Sin penalización |

> **En el estado actual de la columna —los nueve valores como texto— ningún cambio en esos valores
> altera el veredicto.** *Error de lectura → valor benigno → interpretación de conformidad.* Es
> **otra forma**, no la misma que `P2-A` (*ausencia de evidencia → valor benigno → ausencia de
> riesgo*). Por eso **`SAT-V` es el `P2-A` principal y `H89` el `P2-B` complementario**.

**Y el contraste que lo vuelve incontestable:** el puente Python **sí** lee esa columna —
`enrich_rdc.py:70` convierte el texto a float y lo documenta (*«L = IF_n (guardado como texto
'1.00')»*)—. **Mismo dato, dos lectores: uno lo lee; el otro falla en silencio y su fallo se publica
como conformidad.**

### `C4-P2-C` · Naturaleza del índice — discrepancia metodología/implementación

**Demostrado:**
- los nueve `IF_n` son **literales**, guardados como texto;
- `IF_n` **coincide exactamente** con `Valor_Narrativa` en los nueve;
- `Valor_Evidencia` (`K`) **no interviene en ninguna fórmula** del libro;
- la fórmula declarada en `H34b!A6` —`IF_n = Ponderación × (1 − |N − E| / max(N,E))`— **no reproduce
  ninguno de los nueve valores** (con `N=1`, `E=28 000 000` daría ≈ 0; el valor es 1,00).

**Formulación exacta** *(redacción del colega)*: **la implementación no permite reconstruir que los
nueve `IF_n` hayan sido obtenidos mediante la fórmula declarada, y la igualdad exacta entre `IF_n` y
`Valor_Narrativa` no permite atribuir a `Valor_Evidencia` un papel efectivo en su cálculo.**

⛔ **NO se declara** que «la evaluación experta dejó de serlo»: pudo haber un juicio experto manual que
produjera esos valores. Lo que falta es la **reconstrucción**, no necesariamente el experto.

**Dónde se declara el carácter experto y dónde se vuelve medición** *(la única pregunta del eje)*:

| capa | qué dice |
|---|---|
| SSoT `data/d09/catalogo_d09_v1.0.0.yaml` | *«ÍNDICE del motor — **evaluación experta trazable**…, no cómputo automático»* (líneas 14 y 33) |
| `METODOLOGIA_TRAZABILIDAD_APORTES.md` §4 | *«la máquina propone, el experto valida»*, citando el `IF_n` como el modelo |
| motor `H34b` | metodología escrita como **fórmula**; valores literales |
| `enrich_rdc.py` / snapshot | **no menciona** el carácter experto · `fuente`: *«video oficial ↔ evidencia verificada»* |
| cajón `m_rdc` §3 y síntesis | *«Cada una recibe un **índice de fidelidad**»* · *«cada barra… **medida** por su fidelidad a la evidencia»* · *«Es el control ciudadano hecho evidencia, **no opinión**»* |

> **El salto ocurre entre el SSoT y el cajón:** lo que el rector define como evaluación experta
> trazable se publica como **medición triangulada**. La palabra «experta» no aparece en ninguna capa
> del producto *(universo: `enrich_rdc.py`, `gm_snapshot.json`, `m_rdc.py`)*.
>
> **Conclusión exacta, y basta con ella:** **la trazabilidad implementativa del procedimiento
> declarado no está demostrada.** ⛔ **No** se afirma que *«el 91 % no sea una evaluación experta»*:
> eso exigiría evidencia sobre cómo se produjeron originalmente esos valores.

### `C4-P2` · Contrafactual epistémico en el consumidor

| escenario *(`if_n` constante)* | lo que publica el cajón |
|---|---|
| evidencia real presente | «8 coinciden con la evidencia verificada» · 91 % |
| **evidencia borrada en las nueve** | **idéntico** |
| evidencia = *«sin evidencia localizada»* | **idéntico** |

> **En el consumidor probado, la afirmación «coinciden con la evidencia verificada» no cambia cuando
> se elimina el contenido de evidencia, mientras `if_n` permanece constante. Por tanto, la presencia
> de evidencia no gobierna funcionalmente esa afirmación en dicho consumidor.** *(El lector sí ve la
> celda de evidencia vacía en la tabla; el recuento y la frase agregada, no.)*

### Falsaciones de esta fase

- **35 ·** *«`B21` promedia la columna equivocada»* —`J` = `Valor_Narrativa` en vez de `L` = `IF_n`—
  → **falsada**: `L` contiene exactamente los mismos valores (como texto); el promedio coincide.
  El defecto real de esa columna está en `H89`, no en `B21`.
- **36 ·** *«el 91 % compone un índice superior en `p16_gobernanza`»* → **falsada**: vive dentro de un
  **comentario** que documenta `D-006`, **ya corregido**. Precedente del patrón —una cifra escrita a
  mano que publicó el método retirado durante 22 días—, no hallazgo nuevo.
- **37 ·** *«el singular “el informe oficial” contradice las cuatro entidades»* → **falsada**: es un
  **solo discurso** del alcalde con nueve afirmaciones sobre cuatro entes, y `entidad` viaja en cada
  claim. **Cuatro entidades ≠ cuatro informes discursivos.**
- **38 ·** *«el riesgo publicado trata la ausencia como conformidad»* → **acotada**: la cadena
  demostrada termina en `H73`; el producto lee `sat_gm`, un derivado congelado que **ni siquiera
  coincide** con el motor. Convertir una ruta potencial en afirmación de producto sería repetir el
  defecto que `C4` investiga.

### Estado de `C4-P2`

> **CERRADO COMO DIAGNÓSTICO** *(taxonomía del colega, 2026-09-16)* · **sin tocar arquitectura.**
>
> | punto | estado |
> |---|---|
> | `P2-A` · colapso epistemológico en `SAT-V` | ✅ **DEMOSTRADO** (cálculo + interpretación) · impacto en producto **NO DETERMINADO** |
> | `P2-B` · fallo de lectura → ausencia de penalización (`H89`) | ✅ **DEMOSTRADO** |
> | `P2-C` · naturaleza del `MFN` | ✅ **DEMOSTRADO como discrepancia metodología/implementación**, **no** como pérdida del carácter experto |
> | universo (entidad · ejercicio · informe) | ⛔ **FALSADO** |
> | composición del 91 % | ⛔ **FALSADO** (precedente `D-006`) |
> | colisión semántica *«fidelidad»* (91 % ↔ 72,73 %) | ❓ **NO DEMOSTRADO COMO DEFECTO** — sin relación `ID → valor` ni consumidor que las mezcle |
> | ruta IA productiva de d09 | ❓ **`NO DETERMINABLE`** — no localizada *(universo: `components/sentinel.py`, `sentinel/*`, `scripts/ia_*`; las coincidencias son clasificación documental y plantillas de informe, no inyección del índice)* |
> | independencia de la cadena | ⚠️ **PARCIAL** — evidencia/evaluación independientes; señalización SAT compartida |

**Regla de disciplina vigente:** no se repara `SAT-V`, ni `H89`, ni `H19`, ni `H24`, ni el render
mientras `C4` siga corriendo.

## 5-septdecies · `Q-M2-C4` · SÍNTESIS TRANSVERSAL `P0` + `P1` + `P2`

> **Esto no es otra auditoría.** Es la operación que responde **una sola pregunta**:
> **¿qué propiedad, exactamente, debe conservar QUIRA entre una evidencia y una afirmación para que
> podamos decir que hay conservación semántica?**

### Los tres cortes, comparados

| corte | indicador | condición que debería gobernar | qué se conserva | qué se pierde | estado |
|---|---|---|---|---|---|
| **`C4-P0`** | ICPI | comparabilidad / temporalidad | el valor (`0,274582`) | la condición que limita su interpretación | ✅ DEMOSTRADO |
| **`C4-P1`** | `Ti` | significado de la magnitud + regla aplicable | el valor (`0,064342`) | la semántica al consumirse como `1 − Ti`; y existe una ruta desconectada en `H19` | ✅ DEMOSTRADO |
| **`C4-P2`** | d09 · `MFN` | estado epistemológico de la evidencia | el valor / `IF_n` y las señales | la distinción entre evidencia ausente, evidencia evaluada y fallo de lectura | ✅ DEMOSTRADO |

**La diferencia crucial, corte por corte:**
- **`P0`:** el número **permanece correcto**, y la condición que limita su interpretación deja de
  gobernar **uniformemente** las capas posteriores.
- **`P1`:** el número **permanece**, y un consumidor lo **transforma semánticamente** (`Ti → 1 − Ti`):
  conserva dependencia numérica, pierde significado.
- **`P2`:** el estado epistemológico **existe en alguna capa** y una capa posterior lo **colapsa**
  (`sin evidencia → 0 → sin señal → inactivo`), con una segunda modalidad en `H89`
  (`dato no legible → error → IFERROR(0) → sin penalización`).

### Los cuatro mecanismos — taxonomía de `C4`

> ⚠️ **Taxonomía PROVISIONAL derivada del universo `C4-P0`/`P1`/`P2`. No constituye todavía una
> clasificación exhaustiva de fallas de QUIRA.** *(Aplicación directa de `DOC-019`.)*

| | mecanismo | forma | dónde se demostró |
|---|---|---|---|
| **A** | **Desacoplamiento** | el dato llega al consumidor y la condición ya no gobierna el resultado | `P0` (`m1`) · `P1` (`H19!B11`) · `P2` (contrafactual de evidencia en d09) |
| **B** | **Sustitución semántica** | el consumidor sigue usando el número, pero como otra magnitud | `P1` (`H24!B10`, `1 − Ti` como participación estructural) |
| **C** | **Colapso epistemológico** | dos estados de conocimiento distintos resultan operacionalmente equivalentes | `P2-A` (`SAT-V`: sin datos ≡ sin brecha) |
| **D** | **Error absorbido como conformidad** | una lectura inválida se convierte en valor benigno y se interpreta como cumplimiento | `P2-B` (`H89`: `IFERROR(…;0)`) |

**Esta taxonomía es el producto.** Agrupar los cuatro bajo *«inconsistencias»* destruiría justo la
información que costó tres cortes obtener.

### ⛔ Lo que NO se declara — `DOC-019`

`DOC-019` *(custodia `GATE` · `app/agents/doctrina.py:606`)* previene exactamente esto:
*«encontré un caso con esta propiedad → todos la tienen»*. La conclusión es **ésta y nada más**:

> **`P0`, `P1` y `P2` constituyen casos demostrados de mecanismos distintos de pérdida o
> desacoplamiento semántico; no demuestran que dichos mecanismos estén presentes en todo QUIRA.**

Y la variable de control queda explícita: **el tramo de señalización `SAT` es común a `P1` y `P2`**,
así que nada observado ahí cuenta como evidencia independiente.

### El estatus de cada pieza de esta síntesis — cinco niveles, no uno

| pieza | estado |
|---|---|
| los casos `P0` / `P1` / `P2` | ✅ **DEMOSTRADOS** |
| la taxonomía de cuatro mecanismos | **SÍNTESIS ANALÍTICA** |
| la clasificación de propiedades en invariantes / condicionantes | **HIPÓTESIS PARA `REARQ`** |
| el contrafactual como criterio | **PROPUESTA METODOLÓGICA** |
| cualquier regla canónica derivada | ⛔ **NO DECLARADA** |

**`C4` diagnostica; no crea la doctrina que después usará `REARQ`.**

### La matriz de conservación — las doce propiedades

*(«transformación permitida» = la que no altera lo afirmable, si se declara. «Tipo» remite a la
taxonomía A/B/C/D.)*

> **⛔ La distinción que atraviesa toda la matriz:** cada celda de conservación/pérdida responde a
> **dos preguntas distintas**, no a una.
> **(a) conservación del dato** — ¿llegó la propiedad? · **(b) conservación de su función semántica**
> — ¿sigue limitando las inferencias del mismo modo?
> En `P1`, para el `Ti`: **(a) sí · (b) no, en `H24`.** Ése es el corazón de `C4`, y por eso
> **preservación del dato ≠ preservación de la función semántica.**

| # | propiedad | origen | transformación permitida | consumidor | evidencia de CONSERVACIÓN | evidencia de PÉRDIDA | tipo | alcance | estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **identidad del indicador** | celda del motor (`H12!B33`, `H07_S5!B20`, `H34b!B21`) | renombrar al lenguaje público (`ADR-027`), nunca cambiar de referente | snapshot · páginas · IA | ICPI y `Ti` conservan referente en el tránsito | `«Ti»` nombra seis magnitudes · `«fidelidad»` nombra dos · `sat_gm` reasigna el significado de los códigos `SAT` | B | `P1`, `P2`, `C3` | ⚠️ colisión DEMOSTRADA · contaminación entre ellas **NO DEMOSTRADA** |
| 2 | **unidad** | razón (0-1) en el motor | razón → % declarado | todos | conservada en los tres cortes | — | — | `P0`,`P1`,`P2` | ✅ conservada |
| 3 | **período / corte** | `H07_S5!B10` · `_meta.fecha_corte` · *«corte 2024»* | ninguna sin declararla | agente d02 · páginas · IA | `_hallazgos_plan` lo usa · el pie de d09 lo declara | el agente d02 lo descarta · el Concejo usa `config.CORTE` · la síntesis d02 lo escribe literal · no viaja a la IA | A | `P1`, `P2` | ✅ DEMOSTRADO |
| 4 | **universo** | grupos 7+8 · 9 afirmaciones / 4 entes | ampliar o restringir **sólo declarándolo** | páginas | **(a)** los `claims` conservan `entidad` *(falsación 37)* · **(b)** la función discriminante del universo se mantiene en d09 | **discrepancia de base DEMOSTRADA:** dos bases numéricas distintas asociadas al mismo rótulo *«grupos 7+8»* — 22 595 464 (`financiero`, corte marzo) y 30 271 811,74 (motor, Ene-Abr) | — | `P1` | ⚠️ ver la nota al pie |
| 5 | **magnitud (el valor)** | motor | ninguna: se lee, no se recalcula (Regla 1) | todos | `test_d02_adversarial` · identidad en el snapshot | ninguna hallada | — | los tres | ✅ **conservada — y ése es el punto** |
| 6 | **semántica de la magnitud** | definición de la fórmula | derivar declarando la derivación | `SAT-IV` | `_absorcion` la llama *«absorción»* | `1 − Ti` usado como participación estructural | B | `P1` | ✅ DEMOSTRADO |
| 7 | **regla aplicable** | `AVEP 90/70/40/20` · guarda `B34` | ninguna sin canon | páginas · `TOP` · `SAT` | **(a)** la regla está presente en los artefactos examinados · **(b)** gobierna efectivamente en el ICPI (`B34`) | umbrales propios 70/50, 30, 85, 75/55/35 **sin la guarda**; y en `H19!B11` la regla existe y **no gobierna** el veredicto | A | `P0`, `P1` | ⚠️ **acotado:** *en los consumidores examinados, determinadas condiciones normativas/operacionales permanecen presentes y, en algunos casos, gobiernan efectivamente el cálculo* — el estándar de `C4` no es *«¿existe la regla?»* sino *«¿sigue gobernando lo afirmable?»* |
| 8 | **estado de evidencia** | `B7=0` · `B19` *«sin datos»* · SSoT *«hoy sin evidencia»* | ninguna: la ausencia es un RESULTADO (Carta CAPA 0) | `SAT-V` → `H75` → `H73` | `B19` conserva el estado donde no gobierna | `IF(B7=0;0;…)` → *«sin señal»* → `INACTIVO` → peso 0 | C | `P2` | ✅ DEMOSTRADO · impacto en producto **NO DETERMINADO** |
| 9 | **procedencia** | celda + libro + lector | añadir eslabones, nunca quitarlos | agente d02 · snapshot · páginas | **conservación:** demostrada donde existe — `evidencia_sha` + `motor_sha` en d02 · `fuente` en d09 | **pérdida:** acredita el libro y el lector, **no la celda ni el período** · **cobertura de transmisión:** incompleta — los literales del Concejo circulan sin fuente | A | `P1`, `P2` | ⚠️ **parcial** — la ausencia en un consumidor **no se declara pérdida** de una propiedad previamente transmitida: eso sería convertir *«no la encontré»* en *«QUIRA la perdió»* (`DOC-019`) |
| 10 | **naturaleza de la evaluación** | SSoT d09: *«evaluación experta trazable»* | publicarla como tal | cajón `m_rdc` | declarada en SSoT y metodología | el producto la presenta como **medición**; la fórmula declarada no reproduce los valores | B | `P2` | ✅ DEMOSTRADO como discrepancia · **trazabilidad implementativa NO DEMOSTRADA** |
| 11 | **nivel de confianza** | `RC-7.3` (`raw → calibrada`, peso evidencial) | propagarla | prompt de la IA · páginas | **conservación:** demostrada en el canal donde existe — viaja al prompt con su reclasificación | **pérdida:** **no demostrada** como pérdida de una propiedad previamente existente · **cobertura de transmisión:** incompleta / `NO DETERMINABLE` según el consumidor | — | `P1` | ⚠️ existe en **un solo canal** |
| 12 | **condición que limita la inferencia** | guarda `B34` · `FactorTemporal` · `_has_mixed_frequency` · `ADR-033 §III` | ninguna | todos | **gobierna** en el ICPI y en `RC-7.3` | no gobierna en ninguna otra superficie inspeccionada | A | los tres | ✅ DEMOSTRADO |

#### Nota al pie de la fila 4 — la diferencia lógica que hay que respetar

*(Corrección del colega: no es lo mismo decir «hay un cambio de universo y su naturaleza es
`NO DETERMINABLE`» que decir «hay una discrepancia de base cuyo significado no podemos determinar».
Se usa la segunda.)*

> **DEMOSTRADO:** existen dos bases numéricas diferentes asociadas al mismo rótulo de universo
> (*«grupos 7+8»*), correspondientes a cortes temporales distintos, cuya diferencia **no pudo ser
> explicada documentalmente en el universo inspeccionado**.
>
> **`NO DETERMINABLE`:** el mecanismo que produce la diferencia.
>
> ⛔ **NO DEMOSTRADO:** que haya habido un cambio de universo —ni, por tanto, que ese cambio no se
> haya declarado—. **La declaración de un cambio de universo no está demostrada.**

**Y sobre `H22`:** `Total_Reformas_2026 = 0` admite **dos lecturas plausibles** —que no hubo
reformas, o que no se cargaron—, y sin productor trazable no se resuelve. **`0` ≠ ausencia demostrada
de reformas.** Por eso `H22` queda como **dato auxiliar de la investigación**, no como explicación de
los ~7,7 M.

> ⚠️ **Y queda como analogía, no como extensión del hallazgo** *(cautela del colega)*:
> **`H22` presenta una forma de representación compatible con el patrón investigado en `P2`
> (mecanismo C), pero NO constituye un caso adicional demostrado de ese mecanismo dentro de `C4`.**
> En `SAT-V` se reconstruyó la cadena completa —`B7=0 → B9=0 → B17 «Sin señal» → H75 INACTIVO`—;
> en `H22` esa reconstrucción **no se hizo**. La pista se conserva; la taxonomía no se contamina.

### Lo que la matriz deja ver — hipótesis, no doctrina

**1 · Sobre el valor numérico** *(redacción acotada, corrigiendo una versión anterior de esta síntesis
que decía «la magnitud es lo único que se conserva siempre»)*:

> **En los tres cortes examinados, la magnitud numérica observada alcanza los consumidores estudiados
> sin una alteración aritmética demostrada. Esta conservación numérica no implica conservación de su
> significado operacional.**

**2 · Dos familias de propiedades** — **HIPÓTESIS PARA `REARQ`**: hay **invariantes** (identidad,
unidad, magnitud, universo, procedencia) a las que les basta **viajar**, y **condicionantes**
(período, regla, estado de evidencia, condición limitante, naturaleza, confianza) a las que **no les
basta viajar: tienen que gobernar**. La frontera entre ambas familias **no está demostrada**: es la
pregunta que `REARQ` debe resolver, no un resultado de `C4`.

**3 · El criterio contrafactual** — **PROPUESTA METODOLÓGICA**, con su alcance explícito:

> **Para las propiedades cuya función es condicionar una afirmación, el contrafactual permite
> comprobar si dicha propiedad gobierna efectivamente el resultado: manteniendo constantes las demás
> variables, se modifica exclusivamente la propiedad y se observa si la afirmación o su clasificación
> responde a dicho cambio.**
>
> ⛔ **Este criterio no se propone como prueba universal para las doce propiedades.** Identidad,
> unidad, procedencia o naturaleza pueden ser condiciones de validez o de interpretación **sin** que
> exista una relación directa *cambio de propiedad → cambio inmediato de conclusión*. Por eso **no se
> le llama «prueba de conservación»**.

**4 · El sistema ya sabe hacerlo en dos sitios** —la guarda `B34` del ICPI y la calibración `RC-7.3`
con su `_has_mixed_frequency`—, así que la tarea de `REARQ` se parece más a **propagar una capacidad
existente** que a inventarla. *(Observación, no conclusión: dos sitios no prueban que el mecanismo
sea reutilizable en todos los demás.)*

⛔ **Nada de esto se registra como doctrina.** Convertirlo en canon exige el paso que el canon mismo
ordena: decisión de la dirección.

### La tesis de `C4` — cierre provisional

> **`C4-P0`, `C4-P1` y `C4-P2` demuestran, en los universos específicamente examinados, que la
> conservación de un dato numérico no garantiza la conservación de las propiedades semánticas y
> epistemológicas que limitan su interpretación. Los tres cortes muestran mecanismos diferentes
> —desacoplamiento, sustitución semántica, colapso epistemológico y absorción de error—, pero estos
> casos no autorizan a generalizar su presencia al conjunto de QUIRA. La síntesis transversal
> identifica como cuestión central de `REARQ` no solamente si una propiedad viaja con el dato, sino
> si continúa gobernando las afirmaciones que el consumidor puede producir a partir de él.**

Y la consecuencia arquitectónica: **`C4` ya no pregunta «¿se perdió el dato?». Está mostrando que el
objeto que QUIRA debe conservar es la RELACIÓN entre dato, contexto, condición y capacidad de
afirmar.**

**Formulación corta de la tesis** *(la que resiste)*: **`C4` no demuestra que QUIRA pierda datos;
demuestra, en los casos examinados, que conservar un dato no garantiza conservar la relación entre
dato, contexto, condición y capacidad de afirmar.**

### Estado formal de `C4`

| elemento | estado |
|---|---|
| `C4-P0` | ✅ **CERRADO — diagnóstico** |
| `C4-P1` | ✅ **CERRADO — diagnóstico** |
| `C4-P2` | ✅ **CERRADO — diagnóstico** |
| síntesis `P0`/`P1`/`P2` | **DEPURADA — pendiente de ratificación** |
| taxonomía de 4 mecanismos | **síntesis analítica provisional** |
| matriz de 12 propiedades | **síntesis analítica provisional** |
| test contrafactual | **propuesta metodológica** |
| reglas nuevas de `REARQ` | ⛔ **NO DECLARADAS** |
| `C4-P3` | ⛔ **NO ABIERTO** |
| reparaciones | ⛔ **NINGUNA** |

**`C4` ya hizo su trabajo diagnóstico. `REARQ` debe decidir qué diagnóstico merece convertirse en
arquitectura.**

## 5-octodecies · Insumo para la mesa `REARQ` — `DEMOSTRADO` → `PROPUESTO` → `POR DECIDIR`

**La mesa no se reúne para decidir *«¿qué arreglamos?»*.** Se reúne para responder:

> **¿Qué propiedades semánticas debe garantizar canónicamente QUIRA para que una afirmación
> *downstream* sea admisible?**

### Criterio rector del dossier

> **Una propiedad semántica no se considera conservada únicamente porque su dato o representación
> llegue al consumidor. Cuando dicha propiedad condiciona el alcance de una afirmación, debe
> conservarse también su función de gobierno sobre aquello que el consumidor puede afirmar.**
>
> ⛔ **Esta formulación es insumo para decisión de `REARQ`; no constituye todavía regla canónica.**

**La frontera que protege el proceso:**
**`C4` diagnostica → `REARQ` propone → `ADR` declara → el test verifica.**

> ⛔ **Esto NO entra diciendo «estas doce propiedades deben convertirse en reglas».** Cada propiedad
> pasa por el mismo filtro de tres columnas, y la tercera es de la dirección, no del diagnóstico.
> **`PROPUESTO` no significa aprobado: es la traducción arquitectónica posible del hallazgo.**
> **Insumo para decisión, no decisión.**

| # | propiedad | **DEMOSTRADO** *(evidencia `C4`)* | **PROPUESTO** *(qué haría falta)* | **POR DECIDIR** *(la mesa)* |
|---|---|---|---|---|
| 1 | identidad del indicador | un mismo nombre designa magnitudes distintas (`Ti`×6 · *«fidelidad»*×2 · códigos `SAT` reasignados en `sat_gm`) | que el nombre publicado resuelva a un referente único y verificable | ¿renombrar, o exigir referente explícito junto al nombre? *(rige `DOC-014`/`DOC-015`: semántica antes que nomenclatura)* |
| 2 | unidad | conservada en los tres cortes | — | ¿se declara como invariante exigible? |
| 3 | período / corte | viaja y **no gobierna** ninguna afirmación evaluativa fuera del ICPI | que el corte condicione la clasificación, no sólo el texto | ¿qué superficies quedan obligadas y cuáles pueden mostrarlo sin gobernarlo? |
| 4 | universo | **discrepancia de base** bajo un mismo rótulo; mecanismo `NO DETERMINABLE` | localizar el productor de `financiero` antes de cualquier regla | ¿se investiga el productor (fuera de `C4`) o se retira el derivado? |
| 5 | magnitud (valor) | llega sin alteración aritmética demostrada | — | ¿basta la Regla 1 vigente o requiere prueba automática? |
| 6 | semántica de la magnitud | `1 − Ti` usado como participación estructural | que toda transformación del valor declare qué magnitud produce | ¿contrato por consumidor, o por indicador? |
| 7 | regla aplicable | existe en los artefactos; gobierna sólo en el ICPI | que el estándar sea *«¿sigue gobernando lo afirmable?»* | ¿se exige a los umbrales de presentación o sólo a los del motor? |
| 8 | estado de evidencia | ausencia y fallo de lectura colapsan en valores benignos (`SAT-V`, `H89`) | que *«sin datos»* y *«evaluado sin brecha»* sean estados distinguibles aguas abajo | **el más urgente de decidir:** toca la Carta (`CAPA 0`) y afecta a señales publicables |
| 9 | procedencia | acredita libro y lector, no celda ni período; cobertura incompleta | extender la procedencia a celda y período | ¿mínimo exigible por tipo de afirmación? |
| 10 | naturaleza de la evaluación | el SSoT dice *«evaluación experta»*; el producto publica *«medición»* | declarar la naturaleza al lector | ¿se declara en el producto, o basta en el SSoT? |
| 11 | nivel de confianza | existe y gobierna **sólo** en `RC-7.3` | propagarla o declarar que no aplica | ¿es exigible fuera del canal de la IA? |
| 12 | condición que limita la inferencia | gobierna en el ICPI y en `RC-7.3`; en ningún otro sitio inspeccionado | propagar la capacidad que ya existe | ¿qué superficies la requieren y con qué prueba? |

### Pruebas que **ya podrían construirse** con la evidencia reunida — propuestas, no implementadas

*(Estructura pedida por el colega: cada prueba declara **la pregunta que sí responde** y **lo que no
permite concluir**. Sin esa segunda columna, una prueba acaba convertida en prueba de «integridad
total», que es justo lo que `C4` desaconseja.)*

| prueba | **pregunta que sí responde** | **lo que NO permite concluir** | evidencia que la respalda |
|---|---|---|---|
| **T1 · gobierno de la condición** | ¿la condición modifica lo afirmable? | que la condición sea **metodológicamente correcta** | contrafactuales de `P0`, `P1` (A1-A4, B) y `P2` |
| **T2 · ceros de origen indeterminado** | ¿el `0` conserva o distorsiona el estado epistemológico? | que **todo** cero sea ausencia de evidencia | `SAT-V` · `H89` · `H22` *(pista)* |
| **T3 · columnas de texto en agregaciones** | ¿el consumidor numérico recibe valores numéricos? | por sí solo, que la **fórmula conceptual** sea correcta | `H34b!L` → `H89!B27` |
| **T4 · referencias a rótulos** | ¿la regla apunta al valor o a un encabezado/metadato? | que **todo** encabezado referenciado sea defectuoso | `H19!B10 → H01!B33 'Valor'` · `H04b` con una fecha como coeficiente |
| **T5 · identidad motor/derivado** | ¿el derivado conserva el estado que afirma representar? | que **toda** divergencia sea un error | `sat_gm` vs `H75` · `PSG_EJECUCION` · `Ti` · *«fidelidad»* |
| **T6 · cobertura de transmisión** | ¿la propiedad atraviesa los saltos previstos? | que su **significado siga gobernando** al consumidor | fichas forenses de `P1` y `P2` |

### Estado ratificable de `C4`

> **`C4`: DIAGNÓSTICO COMPLETO · SÍNTESIS PENDIENTE DE RATIFICACIÓN.**
>
> - **`C4-P3`: NO SE ABRE.** La pregunta ya cambió, y fabricar un cuarto corte para *«tener más
>   evidencia»* no respondería la que está sobre la mesa.
> - **No se repara** `H19`, `H24`, `SAT-V`, `H89` ni los renders.
> - **Ninguna de las seis pruebas se convierte en test productivo** por ahora.
> - **Ninguna de las doce propiedades entra al canon** por el mero hecho de estar en la matriz.
>
> **`C4` queda listo para decisión arquitectónica, no para otra ronda de arqueología.**

### ⛔ Regla de cierre de `C4`

> **No se repara nada antes de terminar esta síntesis.** Ni `SAT-V`, ni `H89`, ni `H19`, ni `H24`,
> ni los renders, ni los literales del Concejo.
>
> Lo que hay sobre la mesa vale más que corregir tres celdas: **tres experimentos con condiciones
> limitantes de naturaleza distinta que permiten observar cómo QUIRA puede conservar un valor
> mientras pierde la condición que le daba significado operativo.** Repararlos ahora destruiría la
> evidencia antes de haberla leído del todo.

## 5-novodecies · APERTURA DE `REARQ` · la pregunta que va a la dirección

### Nota previa · qué está verificado y qué no *(reserva del colega, acogida)*

| afirmación | cómo se sostiene |
|---|---|
| los commits existen en el remoto | ✅ **VERIFICADO** — `git ls-remote origin refs/heads/main` → `0ef8224`, el mismo `HEAD` local, sin divergencia |
| `check_health` en verde | ⚠️ **EJECUCIÓN REPORTADA** por este agente, no verificación independiente |
| **CI remoto** | ⛔ **NO VERIFICADO** — `gh` no está disponible en esta sesión y el repo es privado; no se leen credenciales |

**«Publicado» significa aquí: la referencia remota apunta a ese commit. No significa que el CI haya
corrido ni que haya pasado.** La distinción es la misma que `C4` viene demostrando: *que el dato
llegue no prueba que la condición que lo hace admisible se haya cumplido*.

### La pregunta

> **¿Qué propiedades semánticas debe garantizar canónicamente QUIRA para que una afirmación
> *downstream* sea admisible?**

`REARQ` **no se abre para decidir qué se arregla.** Se abre para decidir qué debe garantizarse. La
reparación viene después, y de la decisión — no al revés. **Reparar `SAT-V`, `H89`, `H19` o `H24`
antes de fijar el mínimo semántico reproduciría el defecto que `C4` documenta:** corregir el síntoma
sin la condición que lo gobierna.

### Lo que `C4` pone sobre la mesa — y lo que NO pone

**Pone:** tres casos demostrados (`P0`, `P1`, `P2`) · cuatro mecanismos *(síntesis provisional)* ·
doce propiedades con su filtro `DEMOSTRADO → PROPUESTO → POR DECIDIR` · seis pruebas con su frontera
declarada · **cero reparaciones**.
**No pone:** ninguna regla, ningún ADR, ningún test productivo, ninguna generalización a todo QUIRA
(`DOC-019`), y ningún juicio sobre qué debe costar la corrección.

### Seis decisiones, en el orden en que se desbloquean

*(El orden es una **propuesta de secuencia**, no una prioridad decidida. Cada fila dice qué queda
bloqueado si no se decide — eso es lo que hace útil el orden.)*

| # | decisión | qué desbloquea | qué queda bloqueado sin ella | ⛔ qué NO debe decidirse aquí |
|---|---|---|---|---|
| **D1** | **el mínimo semántico de una afirmación publicable**: qué propiedades deben **acompañar** y cuáles deben **gobernar** | casi todo lo demás: es el criterio con el que se juzgan las otras cinco | cualquier reparación con criterio; las seis pruebas no tienen umbral contra el cual fallar | la lista final de doce: puede que el mínimo sea menor |
| **D2** | **el estado de evidencia** (`Carta CAPA 0`): ¿*«sin datos»* y *«evaluado sin brecha»* deben ser distinguibles aguas abajo? | `SAT-V`, `H89`, `H22` y toda señal que hoy colapsa ausencia en valor benigno | el circuito `SAT` completo: hoy no puede declarar por qué calla | **el más urgente**, porque afecta a señales publicables · pero no la fórmula concreta de `SAT-V` |
| **D3** | **una sola regla temporal para el `Ti`**: curva del motor · `W_Q` de la Doctrina · nota `mes/12` · baselines de `rc72_calibration.json` | la comparabilidad de todo lo que se publica sobre ejecución | el cierre de `011-C4`; los renders no pueden derivar su texto de nada estable | cuál de las cuatro gana: es decisión de canon, no de auditoría |
| **D4** | **identidad de los nombres**: `Ti` designa seis magnitudes; *«fidelidad»*, dos; los códigos `SAT` difieren entre motor y derivado | que un nombre publicado resuelva a un referente único | `T5`; y cualquier lectura automática que cruce artefactos | renombrar — rige `DOC-014`/`DOC-015`: **semántica antes que nomenclatura** |
| **D5** | **qué pruebas se construyen y en qué modo**: informativo o bloqueante | el paso de diagnóstico a verificación continua | que los hallazgos de `C4` reaparezcan en seis meses | el modo por defecto — hay precedente: `check_sat_brn` **informa y no bloquea**, y ese estado debe ser **declarado**, no heredado |
| **D6** | **los derivados congelados**: `sat_gm` (diverge del motor), `financiero` (productor no localizado) | el tramo común de señalización, compartido con `C3` | `D1` en su parte de procedencia y universo | si se regeneran o se retiran: exige antes localizar sus productores |

### Cómo se acoge lo que se decida — el encuadre de la dirección

> *«Todo lo que se revise y se deba acoger para la construcción debería anotarse **no como deuda**,
> sino para implementar.»* — Javo
>
> Por eso este dossier **no abre un inventario de deuda**: abre una **lista de decisiones**. Lo que la
> mesa acoja entra al trabajo de `vNEXT`; lo que no acoja queda registrado como decidido-que-no, con
> su razón — que es información, no omisión.

**Y la frontera se mantiene intacta en los cuatro pasos:**
**`C4` diagnostica → `REARQ` propone → `ADR` declara → el test verifica.**
**`PROPUESTO` ≠ `APROBADO` ≠ `CANÓNICO`.**

### Lo que esta apertura NO hace

No busca un defecto más. No abre `C4-P3`. No repara `H19`, `H24`, `SAT-V`, `H89` ni los renders. No
convierte ninguna de las seis pruebas en gate. No declara canon. **Pone a la dirección frente a la
pregunta, con la evidencia ordenada detrás de cada opción.**

## 5-vicies · `REARQ` · `D0` — autoridad, lenguaje y frontera público/propietario

### La formulación de primera página *(colega)*

> **`REARQ` no comienza reparando consumidores. Comienza estableciendo la autoridad, el lenguaje y el
> mínimo semántico desde el cual un cambio canónico puede propagarse legítimamente por todo QUIRA. El
> Excel canónico constituye la representación operacional de partida; no sustituye al canon. El
> vocabulario administrativo constituye la interfaz semántica común; la implementación interna puede
> conservar know-how técnico protegido sin alterar ni ocultar el significado, evidencia y límites de
> las afirmaciones publicables.**

### La corrección de concepto, acogida

La dirección propuso *«REARQ debe empezar en el Excel canónico»*. **Correcto en el orden; impreciso en
la autoridad.** Queda así:

```
NORMA / EVIDENCIA
   ↓
CANON VALIDADO
   ↓
GOLD MASTER  (estado canónico)
   ↓
EXCEL CANÓNICO  (representación operacional de trabajo)
   ↓
DERIVADOS / MOTORES / DOMINIOS
   ↓
PRODUCTOS / AGENTES
```

**Y el orden de trabajo es `CANÓNICO → PROPAGACIÓN → CONSUMIDORES → PRODUCTOS`**, nunca
`PRODUCTO → detectar defecto → parchear`, que es el patrón que `C4` acaba de diagnosticar.

**Objetivo de `REARQ`, reformulado** *(sustituye a «propagar cambios, actualizaciones y elevaciones»)*:

> **Reconstruir el circuito mediante el cual un cambio validado en el estado canónico puede
> propagarse de forma trazable, semánticamente conservada y verificable hacia todos los consumidores
> autorizados, sin que ningún derivado intermedio cree, altere o eleve por sí mismo la autoridad de
> una afirmación.**

### `D0` · cuatro decisiones previas a `D1`

| | decisión | propuesta para deliberación | ⛔ advertencia |
|---|---|---|---|
| **0.1** | **¿cuál es la autoridad?** | *el canon validado gobierna el Gold Master; el Excel es representación operacional del estado canónico; **los derivados no pueden convertirse en autoridad por persistencia, antigüedad o consumo*** | decir *«el Excel es la autoridad»* crearía una dependencia que contradice la arquitectura |
| **0.2** | **¿cuál es el vocabulario?** | un **vocabulario administrativo común y transversal**, con nombres técnicos internos **sólo cuando sean necesarios** y siempre con su denominación pública | ⚠️ **esto modifica una Regla de Oro**: el `CLAUDE.md` vigente exige hoy DOS vocabularios *(«AFUERA: lenguaje de administración pública. ADENTRO: lenguaje interno. La jerga jamás cruza al producto»)*. Unificar es **decisión de canon**, no de auditoría |
| **0.3** | **¿qué es público y qué es propietario?** | **público:** significado · evidencia · limitaciones · interpretación · **propietario:** implementación, arquitectura interna, mecanismos de detección, heurísticas, controles antifraude, seguridad | ⛔ la dirección habló de *«receta secreta»*: **QUIRA puede proteger CÓMO hace algo sin ocultar QUÉ afirma, sobre qué evidencia y bajo qué condiciones**. Ocultar la regla epistemológica dañaría la trazabilidad que QUIRA ofrece |
| **0.4** | **¿qué ocurre cuando cambia el canon?** | definir propagación, invalidación, regeneración y verificación | aquí `REARQ` se conecta con `C3` (derivados y vigencia) y con `C4` (conservación semántica) |

### Las seis decisiones, reordenadas bajo `D0`

`D0` autoridad + lenguaje + frontera → `D1` mínimo semántico → `D2` estado de evidencia
*(«hay» · «no hay» · «no se pudo observar» · «no determinable»)* → `D3` **tiempo y corte** → `D4`
**identidad terminológica**, partiendo ya del vocabulario de `D0` *(qué nombres técnicos sobreviven
adentro y cuáles desaparecen de la superficie)* → `D5` pruebas *(informativa · bloqueante ·
obligatoria antes de publicar · experimental)* → `D6` derivados *(no «¿los borramos?» sino **qué
autoridad tienen, qué estado temporal, cuándo caducan y bajo qué condición pueden alimentar
consumidores**)*.

### Dos reglas candidatas — sobre la mesa, **NO declaradas**

> **R1 ·** *Ningún derivado puede adquirir mayor autoridad semántica que el estado canónico del que
> deriva.*
>
> **R2 ·** *Un cambio canónico no se considera propagado porque exista una copia actualizada; se
> considera propagado cuando los consumidores relevantes han sido regenerados, validados y
> reconocidos como compatibles con el nuevo estado.*

**`C3` mostró el problema de la derivación y la vigencia; `C4`, el de la conservación semántica en el
tránsito. `REARQ` es donde ambos se encuentran.**

### Pregunta de la dirección · ¿puede QUIRA dejar de depender del Excel en una carpeta local?

*(Respuesta con el código en la mano. Universo inspeccionado: `config.py`, `utils/cache_quira.py`,
`app/connectors/gold_master.py`, `app/agents/*/motor.py`, `app/pipelines/snapshot_pipeline.py`,
`quira_pages/*`, `scripts/enrich_*.py`.)*

**Hay que separar dos dependencias que hoy se confunden en una sola pregunta.**

| | ¿depende del Excel local? | evidencia |
|---|---|---|
| **servir el producto** (páginas, cajones, agentes de lectura) | ⛔ **NO** | las páginas leen `cargar_gm_snapshot()` → `data/gm_snapshot.json`, **versionado en el repo** (372 KB). El conector del Excel sólo lo llaman `snapshot_pipeline` y `fondos_matcher` |
| **regenerar los derivados** (enrichers, pipeline, `leer_metricas` de los agentes, gobernanza) | ✅ **SÍ** | `scripts/enrich_*.py` y `app/agents/*/motor.py` abren el archivo que resuelve `config.SIAP_PATH` |
| **la ruta a esa carpeta** | ⛔ **ya NO está fijada** | `DATOS_DIR = Path(os.environ.get("QUIRA_DATOS", <carpeta por defecto>))` — `OBS-032` (2026-08-19) corrigió esa frontera **escrita a mano en 54 puntos de 49 archivos** |

> **Respuesta corta:** **la dependencia de *su* carpeta ya es removible hoy** —basta `QUIRA_DATOS`
> apuntando a otra ruta, otro equipo o un servidor—. **Lo que no se elimina con una variable de
> entorno es la dependencia del Excel como representación canónica**: alguien, en algún sitio
> gobernado, debe custodiarlo y regenerar desde él. **Dónde vive y quién puede regenerar es
> exactamente `D0.1` + `D6`.**

⚠️ **Y hay un matiz que la mesa debe conocer:** `IS_CLOUD = not DATOS_DIR.exists()`, y el comentario
de `config.py` dice que en ese caso *«la app usa `demo_data.py`»* — **módulo no localizado en el
universo inspeccionado**. El respaldo real es el snapshot versionado. Es decir: **sin el Excel el
sistema sirve «lo último regenerado» sin declarar ese estado**, y su documentación nombra un
mecanismo que no está. *(Observación, no hallazgo de `C4`: no se investigó su cadena completa.)*

**Tres caminos para `D0.1`/`D6`** *(insumo, no recomendación cerrada)*:

| | camino | qué resuelve | qué NO resuelve |
|---|---|---|---|
| **A** | Excel en **almacenamiento gobernado** (objeto privado o artefacto de *release*), con versión y `SHA`; el circuito regenera desde ahí | elimina la máquina personal del circuito · hace auditable cada regeneración | no cambia que el significado viva en fórmulas de una hoja |
| **B** | el Excel sigue siendo de **autoría local**, y cada *release* publica un **estado canónico inmutable** (snapshot + procedencia + hashes) como único insumo de los consumidores | separa **autoría** de **autoridad de consumo** · es lo más cercano a lo que ya existe (`provenance/ensayos`) | exige decidir **quién sella** y con qué prueba — el custodio de regeneración que `C3` echó de menos |
| **C** | expresar el canon en forma **legible por máquina** (fórmulas y contratos versionados) y dejar el Excel como **una** representación | ataca la raíz: el significado deja de vivir sólo en celdas | es el más caro y **no debe intentarse antes de `D1`** |

### Sobre la versión 6 del Excel

**Sí, pero después de `D0`.** Y con una advertencia que el propio repositorio documenta: el archivo
vigente se llama `v5.5_TGI` **conteniendo ya la cirugía metodológica «v6.0»**, y *«el NOMBRE del slot
se conserva a propósito (contrato con el código)»* —`CIRUGIA_GOLD_MASTER_D2A`—. **Nombre y estado ya
divergen hoy.** Construir una `v6` antes de decidir autoridad y vocabulario **reproduciría el patrón
que `C4` documentó**: un artefacto nuevo que hereda el significado sin heredar la condición que lo
gobierna.

## 5-unvicies · `REARQ` · el alcance real — **QUIRA 7**

### Principio rector *(propuesto por el colega, ratificado por la dirección)*

> **QUIRA 7 no será una actualización de los artefactos de QUIRA 5.x; será una nueva arquitectura
> gobernada desde un estado canónico capaz de conservar no solamente los datos, sino también el
> significado, contexto, autoridad, evidencia, vigencia y condiciones que determinan qué puede
> afirmarse a partir de ellos.**

**Objetivo de `REARQ`, elevado** *(sustituye a «reconstruir el circuito de propagación», que era
demasiado pequeño)*:

> **Elevar QUIRA desde su arquitectura actual hacia una nueva arquitectura de inteligencia pública
> gobernada por un estado canónico semánticamente íntegro, capaz de evolucionar de Ecuador a
> Latinoamérica, preservar la trazabilidad de sus afirmaciones y exponerlas a humanos y agentes sin
> pérdida de significado, autoridad, evidencia o condiciones de interpretación.**
>
> **La cirugía comienza en el estado canónico —representado actualmente por el Excel canónico— y se
> extiende a su modelo de datos, reglas, vocabulario, temporalidad, evidencia, procedencia,
> derivados, consumidores, productos y agentes.**

### Las reglas vigentes son INSUMOS de gobierno, no intocables

La dirección lo planteó y el colega lo formalizó: **si `REARQ` es una reconstrucción mayor, las
reglas vigentes deben ser auditadas, conservadas, reformuladas, sustituidas o derogadas
explícitamente.** Con una disciplina que no se negocia:

> **Una regla canónica tiene autoridad mientras esté vigente; `REARQ` tiene precisamente la función
> de determinar si debe continuar vigente en la nueva arquitectura.**
>
> **Secuencia obligatoria:** regla actual → análisis → propuesta `REARQ` → **decisión** → nueva
> `ADR`/canon → implementación → actualización de `BOOT`/`CLAUDE.md`.
>
> ⛔ Ni `CLAUDE.md` gobierna la arquitectura futura por ser antiguo, ni se modifica porque se nos
> ocurra una buena idea.

**Estado de la Regla de Oro 2** *(dos vocabularios)*: **VIGENTE · CANDIDATA A REFORMULACIÓN en `D0.2`.**
No está violada: está en revisión, que es exactamente lo que `REARQ` existe para hacer.

### `D0.2` · la formulación del vocabulario — mejor que «un solo idioma»

> **QUIRA debe utilizar un vocabulario semántico común para representar los fenómenos de la
> Administración Pública en todas sus capas, evitando que una misma realidad administrativa adquiera
> denominaciones diferentes según sea consumida por el sistema, un agente, un analista o el usuario
> final. Los identificadores técnicos podrán permanecer como mecanismos de implementación, pero no
> constituirán un vocabulario semántico alternativo.**

Así conviven *«ejecución presupuestaria acumulada al corte»* (concepto) y `Ti` (identificador). Lo que
queda prohibido es lo que `C4-P1` documentó: **`Ti` adentro, «absorción» en el producto y
«cumplimiento» en un agente — tres denominaciones para un fenómeno, que es donde nace la deriva.**

### La identidad semántica transversal — consecuencia natural de las doce propiedades

Concepto administrativo → **identificador estable** → denominación pública → definición → unidad →
período/corte → universo → regla aplicable → estado de evidencia → procedencia → confianza →
limitaciones → **transformaciones permitidas** → **consumidores autorizados**.

⚠️ **Esto NO convierte las doce propiedades en canon.** Significa que `REARQ` tiene ahora evidencia
para estudiar si esa estructura debe ser **el nuevo contrato semántico del ecosistema**.

### Las ocho capas de la cirugía — y qué rector EXISTE ya para cada una

*(Aporte de esta dirección: antes de diseñar, se declara qué hay. Regla de Oro 6/7 — **derivar, no
redefinir**. La columna derecha es lo que `REARQ` tendría que construir o elevar.)*

| capa | rector que YA existe | lo que falta |
|---|---|---|
| **1 · ontología administrativa** | `CONSTITUCION_ONTOLOGICA_QUIRA` (4 macroejes · 12 dominios) + Neo4j + `ADR-016/017/019/021` | extenderla a entidades administrativas finas (programa, compromiso, resultado) y a **otros países** |
| **2 · identidad** | `registry.yaml` (158 activos con id y cadena) · `MNT_UUID` · catálogos `SSoT` por dominio | nombres históricos, alias, versión y estado **por objeto**, no sólo por artefacto |
| **3 · semántica** | `DICCIONARIO_CONCEPTUAL_QUIRA` — **13 ADN · 11 campos · SELLADO** | contrastar esos 11 campos con las **12 propiedades de `C4`**: qué falta, qué sobra, qué se renombra |
| **4 · procedencia** | `app/agents/procedencia.py` (capas 5-6) · `provenance/ensayos` · `evidencia_sha` + `motor_sha` | llegar a **celda y período**, no sólo a libro y lector *(`C4` fila 9)* |
| **5 · temporalidad** | ⛔ **no hay rector**: hoy es nota al pie | **estructural**: `Q1-2026` no debe poder mezclarse en silencio con `Ene-Abr 2026` *(`C4-P1`)* |
| **6 · evidencia** | la **Carta `CAPA 0`** ya tiene la escala (independiente · institucional · parcial · sin evidencia · contradicción) | que **gobierne**: hoy `sin datos` colapsa en `0` *(`C4-P2-A`)* |
| **7 · reglas** | **BRN** (`CNO`/`RO`, 30 YAML) · `ADR-035/038/039` · `registry` | `ID → definición → vigencia → ámbito → parámetros → autoridad → versión → consumidores → estado`; y saldar las **SAT huérfanas** (`check_sat_brn` en vivo, 2026-09-17: **6 de 10 sin cadena**) |
| **8 · agentes** | `META_CATALOGO_AGENTES` · molde `ADR-053` · agentes d01/d02 con procedencia | que un agente reciba **el indicador con sus condiciones**, no un número suelto |

> **Seis de las ocho capas ya tienen rector.** Las dos que no —**temporalidad** y **evidencia como
> gobierno**— son exactamente las que `C4-P1` y `C4-P2` demostraron ausentes. **`REARQ` no parte de
> cero: parte de un diagnóstico que ya sabe dónde está el hueco.**
>
> ⚠️ **Precisión indispensable** *(colega)*: **«tiene rector» ≠ «está resuelta».** Significa que
> existe un artefacto o mecanismo **candidato** a gobernar esa dimensión. **La pregunta de `REARQ` es
> si ese rector gobierna realmente y de forma transversal** — que es, literalmente, el estándar que
> `C4` acaba de establecer: *tener la propiedad no garantiza que siga gobernando lo afirmable*.

**Por eso la formulación de `REARQ` cambia** —y mejora—:

> **QUIRA ya posee artefactos rectores dispersos para buena parte de las ocho dimensiones; `REARQ`
> debe determinar cuáles son realmente canónicos, cuáles tienen cobertura efectiva, cuáles están
> desacoplados y cómo se integran en un único estado gobernado.**

⛔ **El error a evitar, ya cometido antes:** confundir **existencia de infraestructura** con
**existencia de arquitectura operativa**. Tres ejemplos que lo hacen concreto: el
`DICCIONARIO_CONCEPTUAL` está sellado con sus 11 campos —la tarea no es *crear semántica*, sino
contrastarlos con las 12 propiedades—; `C4-P1` **no demostró que falten fechas**, sino que la
dimensión temporal **no gobierna de manera uniforme**; y la Carta `CAPA 0` ya da la base
epistemológica —falta que deje de ser clasificación documental y **acompañe y limite** las
afirmaciones *downstream*.

### La barrera tecnológica

> ⛔ *«Últimas tendencias de tecnología agéntica»* **no es criterio de diseño por sí mismo.** La
> pregunta no es *«¿cómo metemos agentes?»* sino **«¿qué arquitectura semántica necesita QUIRA para
> que los agentes puedan consumir, razonar y transmitir evidencia sin crear autoridad o significado
> que no existían en origen?»**. **La tecnología sigue a la arquitectura, no al revés.**

Y hay una razón dura para esta barrera, que `C4` ya probó: **un agente sin contexto semántico es el
consumidor perfecto para reproducir los cuatro mecanismos a escala.** Un agente que recibe
`ICPI = 53.56` sin período, universo, evidencia ni condición **no puede sino desacoplar**.

### La frontera transparente / protegido — cerrada

| **QUIRA debe poder explicar** | **QUIRA puede reservar** |
|---|---|
| qué mide · qué evidencia usa · qué significa · qué limitaciones tiene · bajo qué condiciones puede afirmarlo | cómo implementa · cómo automatiza · cómo detecta · cómo optimiza · cómo protege · qué know-how técnico usa |

> **Auditable en su significado, sin ser reproducible en su ingeniería interna.**

### Sobre el número de versión — y un dato verificado

**La versión es consecuencia, no punto de partida:** `REARQ` → decisiones → nuevo canon → modelo
canónico → cirugía del Excel → propagación → validación → **y entonces** la versión.

**Dato verificado en disco** *(lectura de la carpeta de datos, sin abrir contenido)*: el **único**
Gold Master presente es **`SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx`**.

⚠️ **Corrección a una versión anterior de este párrafo, que decía «no hay ningún archivo v6»**
*(cautela del colega, y la evidencia la confirmó)*. La formulación correcta distingue cuatro cosas:

> **archivo físico ≠ referencia documental ≠ estado operativo ≠ versión canónica.**
>
> **No existe un `v6` operativo/canónico vigente en el estado contrastado; sí existen artefactos y
> referencias que ya cargaron «v6.0» de significado histórico y documental** —incluido el changelog
> doctrinal, que lo declara **ACTIVO** *(ver `§5-duovicies`)*—.

**Conclusión para la mesa:** saltar a **7** es una decisión de nomenclatura razonable porque `6` ya
está cargado de significados divergentes. **Pero «7» no es todavía una versión canónica: el número
queda subordinado al cierre de `REARQ`.**

### Lo que este documento NO decide

No reformula la Regla de Oro 2 —la marca como candidata—. No declara el vocabulario común. No
convierte las doce propiedades en contrato. No elige tecnología. No abre la cirugía del Excel. No
numera nada. **Fija el alcance y deja la decisión donde corresponde: la mesa.**

## 5-duovicies · `REARQ` · `D0.1` · AUTORIDAD — la pregunta, y el mapa de lo que hoy la ejerce

> **¿Qué artefacto tiene autoridad para declarar el significado de una realidad administrativa, y qué
> relación debe existir entre esa autoridad y sus representaciones operacionales, derivados,
> productos y agentes?**

**No se empieza tocando el Excel.** Se empieza aquí, porque de esta respuesta cuelgan: qué significa
*«Excel canónico»* · si sigue siendo representación de trabajo · qué parte pasa a representación
máquina · qué puede regenerarse · qué puede derivarse · **qué queda invalidado cuando cambia el
canon** · y **quién tiene autoridad para promover un nuevo estado**.

### ⛔ Lo que hoy declara «cuál es el estado vigente» — cinco declarantes, cuatro respuestas

*(Lectura directa de los artefactos, 2026-09-17. Universo: `data/doctrinal/gm_changelog.json`,
`config.py`, `app/connectors/gold_master.py`, `governance/BOOT.md`, carpeta de datos.)*

| declarante | qué declara hoy |
|---|---|
| **changelog doctrinal** `data/doctrinal/gm_changelog.json` | **`v6.0` · estado `ACTIVO`** · archivo `TGI_GOLD_MASTER_v6.0_20260525.xlsx` · 34 hojas · *«nueva arquitectura `G1.x-G7.x` reemplaza `H01-H99` de v5.5»* · y `v5.5` como `CONGELADO` |
| **`config.py`** *(resolución en ejecución)* | **`v5.7_TGI`** — el mayor `vX.Y_TGI` presente en la carpeta |
| **`governance/BOOT.md`** | **`v5.7_TGI`** *(coincide con `config`)* |
| **docstring de `app/connectors/gold_master.py`** | *«`v5.5` (ACTIVO)»* · *«`v6.0` (template)»* |
| **la carpeta de datos** *(disco)* | un solo archivo: **`SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx`** |

⚠️ **Corrección a una versión anterior de este párrafo**, que decía *«hoy no existe un artefacto que
declare cuál es el estado canónico vigente»*. **Eso contradecía la evidencia que acababa de
aparecer:** sí existe una declaración explícita —`v6.0 ACTIVO`—. La formulación correcta:

> **En el universo inspeccionado existen múltiples declarantes de vigencia que no coinciden entre sí;
> no se identificó un único acto de autoridad, inequívocamente vinculante y transversal, que
> determine qué representación constituye el estado canónico vigente para todos los consumidores.**

**Y ahí está el verdadero problema de `D0.1`:** no es que QUIRA carezca de declaraciones de
autoridad; es que **no existe una relación inequívoca entre declaración de autoridad, estado
operativo y consumo.**

### Las cuatro capas que hay que mantener separadas

| capa | pregunta | respuesta hoy |
|---|---|---|
| **1 · artefacto físico** | ¿qué archivo existe? | `SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx` |
| **2 · declaración documental** | ¿qué se dice que está activo? | `gm_changelog.json`: **`v6.0 ACTIVO`** |
| **3 · resolución operativa** | ¿qué consume realmente el sistema? | `config.py` resuelve **`v5.7_TGI`** |
| **4 · autoridad canónica** | ¿qué **acto** hace que una de esas representaciones sea el estado autorizado? | ⛔ **`NO DETERMINADO`** en el corpus inspeccionado |

**La cuarta capa es exactamente lo que `D0.1` debe resolver.**

### Qué gobierna hoy la selección — y por qué no debe llamarse «autoridad»

*(Bajo un grado la formulación anterior, que decía «la autoridad la ejerce el nombre del archivo».)*

> **En la ejecución observada, la selección del estado operativo queda gobernada de facto por la
> convención de versionado del nombre de archivo utilizada por `config.py`.**

El código es cuidadoso —excluye respaldos (`_`, `~$`) y congelados (`_FREEZE`) para que *«un respaldo
jamás se vuelva canónico por accidente»*—. Pero **un mecanismo de selección no es un acto de
autoridad**, y `REARQ` tiene que separar precisamente esas dos cosas:

> *«`v5.7` es el archivo con la versión más alta»* **≠** *«`v5.7` está autorizado como estado
> canónico vigente»*. **Son proposiciones completamente distintas.**

### El acto de promoción: declarado, no operando

`app/services/gold_master_governance.py` fija la doctrina —*«cada versión del Gold Master es un hito
epistemológico; ningún cambio ocurre sin registro en `gm_changelog.json`»*— y ofrece validar,
respaldar con `SHA-256` y diagnosticar.

**Contraste con el registro real:** el changelog tiene **dos entradas**, la última del **2026-05-25**.
Desde entonces el vigente pasó por `v5.5 → v5.7` —incluida la cirugía `D2A` del 2026-06-15, que movió
el ICPI de 17,45 % a 27,46 %— **sin una sola entrada nueva**.

> **El circuito de promoción existe como capacidad y no está operando.** Es exactamente la forma que
> `C3` nombró: **lifecycle definido ≠ lifecycle activado**. *(Consumidor localizado del changelog:
> `quira_pages/env_ops.py:280`, que lo muestra — de modo que lo que se exhibe puede ser `v6.0
> ACTIVO` mientras el motor lee `v5.7`.)*

### La pregunta que realmente abre `D0.1`

> **¿Cuál es el acto que convierte una modificación del conocimiento canónico en un estado autorizado
> para ser consumido por QUIRA?**

Y obliga a separar **tres autoridades que hoy no están unificadas**:

| | autoridad | pregunta | dónde vive hoy |
|---|---|---|---|
| **A** | **semántica** | ¿quién determina qué significa una realidad administrativa? | norma · evidencia · doctrina · Diccionario · ontología · ADR |
| **B** | **de estado** | ¿quién determina qué versión constituye el estado vigente? | changelog · *release* · sello · versión · custodio |
| **C** | **de consumo** | ¿qué estado puede utilizar realmente un consumidor? | `config.py` · `gm_snapshot.json` · derivados · agentes · páginas |

**El hallazgo de `D0.1` es que esas tres no están suficientemente unificadas.**

### Las cinco preguntas, respondidas documentalmente

*(Trabajo pedido por el colega antes de elegir cadena. Universo: los artefactos citados en cada fila.)*

| # | pregunta | respuesta con evidencia |
|---|---|---|
| **1** | **¿qué artefacto determina hoy el SIGNIFICADO?** | **Cuatro rectores por tipo de verdad, ruteados por el `MASTER_INDEX`:** `DICCIONARIO_CONCEPTUAL` (concepto de dominio · 13 ADN · 11 campos · sellado) · **BRN** `CNO→RO` (norma operacionalizada) · **Gold Master** (cálculo) · **Carta/Constitución** (epistemología). **No hay artefacto único — y eso es la arquitectura declarada, no un defecto.** El defecto aparece cuando dos rectores dicen cosas distintas del mismo objeto *(`C4-P1`: el `Ti`)* |
| **2** | **¿qué artefacto determina hoy la VERSIÓN?** | **Dos respuestas desalineadas:** por doctrina, `gm_changelog.json`; en la práctica, la convención de nombres resuelta por `config.py` |
| **3** | **¿qué mecanismo determina qué versión se CONSUME?** | **Tres, según el consumidor:** `config._resolver_gold_master_vigente()` (regeneración) · `data/gm_snapshot.json` (producto) · derivados congelados como `sat_gm` (algunas páginas) |
| **4** | **¿qué ACTO convierte una modificación en estado autorizado?** | ⛔ **`NO DETERMINADO`.** Existe la doctrina (*«ningún cambio sin registro en `gm_changelog.json`»*) **sin operar desde 2026-05-25**; existe CI (`quira-health.yml` → `check_health.py` en cada *push*/PR) que **verifica el repositorio** —arranque, secretos, sintaxis, gates, suite— **pero no valida ni sella el Gold Master**, que no vive en el repo; y existe `provenance/ensayos`, que registra **ejecuciones de snapshot**, no promociones de estado. **No se localizó un acto único, explícito y verificable de autorización** |
| **5** | **¿quién o qué puede INVALIDAR formalmente el estado anterior?** | **Para la doctrina, SÍ existe:** `status` en el *frontmatter* de los artefactos + `canon.py`, que **deriva** el estado en vez de declararlo. **Para el estado canónico del Gold Master: no se localizó mecanismo de invalidación.** El sufijo `_FREEZE` excluye un archivo de la resolución —exclusión operativa, no invalidación declarada— → ⛔ **`NO DETERMINABLE`** |

> **Que `4` y `5` queden `NO DETERMINADAS` no es un fracaso de `D0.1`: es el hallazgo que justifica
> `REARQ`.**

**Y hay un precedente propio que la mesa debería mirar antes de inventar nada.** `canon.py` nació
porque *«el estado de lo construido no era consultable, había que recordarlo»*, y su respuesta fue
**derivar el estado de los artefactos en vez de declararlo**. ⚠️ Eso **no implica** que el Gold Master
deba copiar ese modelo; implica que la pregunta se puede formular con precisión:

> **¿Debe el estado canónico del Gold Master ser declarado, derivado, o declarado y verificado
> mediante derivación independiente?**

⚠️ **Corrección a una versión anterior de este párrafo**, que decía *«hoy ocurre lo peor de las dos
posibilidades»* — eso ya era una evaluación arquitectónica, y `D0.1` todavía no ha establecido cuál
de los dos mecanismos debería existir. La formulación quirúrgica:

> **Hoy coexisten dos mecanismos no unificados: la resolución operativa deriva la versión a partir de
> la convención de nombres, mientras la doctrina registra una declaración de vigencia en el
> changelog. La evidencia examinada no demuestra que ambos mecanismos formen parte de un mismo acto
> de autoridad verificable.**

**La tercera opción merece atención especial**, porque produciría una arquitectura que separa lo que
`C4` demostró mezclado —dato, significado, condición y capacidad de afirmar—:

```
ACTO DE PROMOCIÓN            → declara intención y autoridad
        ↓
ESTADO CANÓNICO              → representación efectiva
        ↓
DERIVACIÓN / VERIFICACIÓN    → comprueba que el estado declarado coincide
                               con el estado realmente consumible
        ↓
RELEASE                      → habilita consumo
```

### El papel del Excel — la pregunta correcta

⛔ Ni *«hay que arreglar el Excel porque es la fuente de verdad»*, ni *«hay que abandonarlo porque es
viejo»*. La pregunta es:

> **¿Qué papel canónico debe desempeñar la representación Excel dentro del nuevo estado gobernado de
> QUIRA?**

Con lo ya demostrado: **el *runtime* no depende del Excel**, pero **la regeneración sí**. El Excel
sigue siendo pieza arquitectónica relevante; **que deba ser la autoridad última no está demostrado.**

> **Y la conclusión que `D0.1` sí puede sostener, que es más fundamental que elegir bando:**
> **la representación Excel no puede determinar por sí sola su propia autoridad canónica. Su papel
> dentro del estado gobernado debe ser definido por `REARQ`.**

### Tres cadenas de autoridad para deliberar

| | cadena | qué exige | qué rompe / qué cuesta |
|---|---|---|---|
| **A** | **el canon declara, el Excel representa**: un artefacto canónico declara el estado vigente (versión, `SHA`, fecha, alcance) y `config` **lo lee** en vez de deducirlo del nombre | reactivar el changelog como **acto obligatorio** de promoción | barato y cercano a lo que ya existe · no toca dónde vive el significado |
| **B** | **la autoridad de consumo es el estado sellado**: cada *release* publica un estado inmutable (snapshot + procedencia + hashes) y **ningún consumidor lee otra cosa** | decidir **quién sella** y con qué prueba — el custodio que `C3` echó de menos | separa autoría de autoridad · obliga a un circuito de *release* real |
| **C** | **representación máquina primaria**: el significado se expresa en forma legible por máquina y el **Excel queda como interfaz humana** de ese estado | el contrato semántico —la discusión de `D1`— **antes** de cualquier migración | ataca la raíz · es el más caro · **no debe intentarse antes de `D1`** |

⚠️ **Las tres son compatibles por etapas** (A ahora, B en el circuito de *release*, C como destino).
**La mesa no tiene que elegir una y descartar las otras: tiene que elegir la primera.**

> ⛔ **Y `D0.1` no cierra eligiendo A/B/C.** *«`D0.1` no debe decidir todavía la arquitectura
> tecnológica definitiva del Gold Master. Debe decidir primero qué constituye autoridad y qué acto
> produce un estado autorizado.»* Después `D1` dirá qué estructura necesita ese estado.

### La secuencia, para que no se invierta

```
C4 diagnóstico → D0 (qué debe gobernar REARQ) → D0.1 (qué constituye autoridad)
   → D1 (qué estructura mínima debe tener ese estado) → cirugía del Gold Master
   → nuevo estado canónico → release gobernado → derivados → productos + agentes
   → QUIRA 7 COMO CONSECUENCIA
```

**La numeración no resuelve por sí misma qué estado está autorizado para gobernar las afirmaciones.**
Tenemos `v5.5 → v5.7 → v6.0 declarado ACTIVO → QUIRA 7 propuesto`, y ninguna de esas etiquetas
responde la pregunta de autoridad. **Por eso QUIRA 7 no puede ser «v6 mejorado».**

### Lo que `D0.1` NO decide

No elige la cadena. No reactiva el changelog. No toca `config`. No renombra el Excel. No define el
contrato semántico —eso es `D1`—. **Deja sobre la mesa el hecho que obliga a decidir: cuatro
respuestas a «¿cuál es el estado vigente?», tres autoridades sin unificar, y las preguntas 4 y 5
`NO DETERMINADAS`.**

### La distinción final — lo que `D0.1` demostró, y lo que NO

⛔ **`D0.1` NO ha demostrado que el sistema actual sea incapaz de producir resultados.** Demostró algo
más específico, y basta con eso:

> **El mecanismo mediante el cual un cambio del conocimiento canónico adquiere autoridad como estado
> consumible no está documentalmente determinado de manera transversal para el Gold Master.**

**Y esa precisión es la que permite que `D1` sea una cirugía arquitectónica y no una reconstrucción
especulativa.**

### Estado de `D0.1` y lo que abre `D1`

> **`D0.1`: DEPURADO · base documental suficiente · LISTO PARA DECISIÓN DE LA MESA.**
>
> Lo que `D1` abrirá, ya con autoridad definida: qué entidades existen · qué identidad tienen · qué
> campos son semánticos · qué propiedades deben acompañar cada valor · qué evidencia respalda cada
> afirmación · qué vigencia y corte tiene · qué regla la gobierna · **qué puede afirmar un agente** ·
> qué puede regenerarse · qué debe invalidarse.
>
> **Ahí comienza la cirugía del Gold Master** —no antes—, y así se evita el error clásico: construir
> primero «QUIRA 7» y después descubrir qué significa que algo sea canónico.

### Nota de estado

**El commit `66499e8` es publicación documental del alcance de `REARQ`. NO es declaración de que
QUIRA 7 exista**, ni de que ninguna de estas propuestas esté aprobada. La distinción se mantiene
limpia: **publicar el alcance ≠ decidir la arquitectura ≠ existir la versión.**

## 5-tervicies · `REARQ` · `D1` — estructura mínima del estado canónico · **y `D1.0` primero**

### La pregunta de `D1`

> **¿Qué estructura mínima debe poseer el estado canónico de QUIRA para que cualquier valor pueda ser
> interpretado, verificado, propagado y consumido sin perder su significado ni las condiciones que
> limitan lo que puede afirmarse?**

Deliberadamente distinta de *«¿qué columnas tiene que tener el Excel?»*: **el Excel será una
representación de esa estructura, no la estructura.**

### ⛔ `D1.0` va antes — la ontología de los cajones no se hereda

**Consulta de la dirección:** *«¿es viable reunificar Planificación + Presupuesto + Salud
Institucional? ¿y Participación + Rendición de Cuentas?»*. El colega la convierte en condición previa,
y es correcto: **si primero diseñamos los campos de trece cajones y después descubrimos que cinco
deben fusionarse, habremos operado sobre una anatomía que aún no sabemos si es la correcta.**

> **`D1.0` · ¿Los cajones actuales representan unidades conceptuales distintas y necesarias, o
> existen relaciones de dependencia, intersección o complementariedad que justifican reunificarlos,
> subdividirlos o reconfigurarlos para QUIRA 7?**
>
> **Regla de dirección:** **QUIRA 7 no heredará los cajones de QUIRA 5.x por continuidad histórica.
> Los conservará, fusionará, dividirá o transformará únicamente cuando la evidencia ontológica lo
> justifique.**

**Cuatro categorías de salida, no dos:** **MANTENER** · **FUSIONAR** · **RECONFIGURAR** ·
**ABSORBER COMO DIMENSIÓN TRANSVERSAL**. Y la prueba decisiva para cada cajón:

> **Si eliminamos el cajón y redistribuimos sus componentes, ¿perdemos una realidad administrativa o
> solamente una etiqueta?**

### Primera excavación de `D1.0` — lo que dice el Diccionario, leído hoy

*(El colega advirtió con razón que no diéramos por axioma el «13 ADN · 11 campos». Se verificó.)*

| hallazgo | estado |
|---|---|
| El Diccionario es real y rige **trece** cajones (`01`-`13`), no doce | ✅ **DEMOSTRADO** |
| La **plantilla madre de 11 campos** existe como *«estándar definitivo (post Capa 0.5)»*, con el Cajón 10 como molde, y cada ADN la sigue | ✅ **DEMOSTRADO** |
| Que esos 11 campos **gobiernen transversalmente** —el estándar de `C4`— | ⛔ **NO DEMOSTRADO** *(ver el hallazgo del campo 10, abajo)* |
| Cada ADN declara **exclusiones con ruteo explícito** a otros cajones (*«montos devengados → d02»*, *«avance físico → d01»*) | ✅ **DEMOSTRADO** — la ontología ya tiene fronteras declaradas, y cualquier fusión debe medirse contra ellas |
| **GeoTwin ya es «capa transversal · NO es un cajón»** | ✅ **DEMOSTRADO** — **precedente interno de la categoría «absorber como dimensión transversal»**: QUIRA ya tomó esa decisión una vez |

> ⛔ **Hallazgo de `D1.0`, del tipo que `C4` enseñó a buscar:** el campo 10 del ADN exige declarar el
> **estado del ancla** (`LIVE`/`PENDIENTE`/`MISSING`). El **Cajón 02** declara su ejecución devengada
> como **`⏳ PENDIENTE (CHK-08, cédula eSIGEF 2026)`** sobre `H07_S5_FINANCIERO_eSIGEF` —y es
> exactamente la hoja de la que el snapshot y las páginas publican hoy el `Ti` de 6,4 %—.
> **El rector declara pendiente lo que el producto publica como dato.** *(`INFERENCIA RAZONABLE`
> sobre la lectura de ambos artefactos; la cadena completa no se reconstruyó.)* **Es la prueba
> concreta de que «tiene rector» ≠ «gobierna».**

### Caso de prueba 1 · Planificación + Presupuesto + Salud Institucional

| | Cajón 01 · Planificación | Cajón 02 · Presupuesto | Cajón 06 · Salud Institucional |
|---|---|---|---|
| **Capacidad Universal** | **Trayectoria** | **Movilización** | **Sostenibilidad interna** |
| **pregunta estratégica** | ¿mantiene rumbo hacia las metas plurianuales? | ¿con qué eficiencia moviliza y ejecuta recursos? | ¿cumple sus funciones de forma sostenible? |
| **indicador madre** | cumplimiento de la planificación | captación y eficiencia del gasto | **ICPI + sus 6 vectores (`ISP·IED·IGP·IOC·IET·PSG`)** |
| **exclusiones declaradas** | montos devengados → **d02** | avance físico de metas → **d01** | *«el detalle operativo de cada vector vive en su dominio: presupuesto → d02 · transparencia → d07 · participación → d08 · equidad → d12»* |

**Dos evidencias que la mesa debe pesar:**

1. ⛔ **El Cajón 06 no es un dominio paralelo: por su propio ADN es el AGREGADO de vectores que viven
   en otros cajones.** Su madre es el ICPI y sus exclusiones remiten el detalle de cada vector a su
   dominio. **Candidato fuerte a la categoría D —dimensión transversal / índice de cabecera— más que
   a fusión.** *(`INFERENCIA RAZONABLE` a partir del ADN; decide la mesa.)*
2. ✅ **`d01` y `d02` consumen la misma materia**: `planificacion.presupuesto` y
   `presupuesto_dom.ejecucion` traen **los mismos números de las mismas celdas** (codificado
   `30 271 811,74` · devengado `1 947 738,29`, de `H07_S5!B18/B19`). **Eso no prueba que deban
   fusionarse; prueba que la frontera declarada no coincide con la materia consumida.** `DEMOSTRADO`.

### Caso de prueba 2 · Participación Ciudadana + Rendición de Cuentas

| | Cajón 08 · Participación | Cajón 09 · Rendición de Cuentas |
|---|---|---|
| **Capacidad Universal** | **Inteligencia colectiva** — incorporar la voz ciudadana a la decisión | **Responsabilidad pública** — someter la gestión al control social |
| **pregunta estratégica** | ¿incide la ciudadanía, y quién queda sin canal? | ¿cierra el ciclo con evidencia verificable, o es autorreportada? |
| **operativos** | IGP · parroquias sin voz · aportes de PP · **resultado CPCCS** | circuito RDC · **resultado CPCCS** · aportes consolidados |
| **anclas del motor** | `H10c_RDC_APORTES` · **`H31_REPORTE_CPCCS`** | `H10c_RDC_APORTES` · **`H31_REPORTE_CPCCS`** |
| **exclusiones** | la rendición formal ante el CPCCS → **d09** | la participación que la alimenta → **d08** |

- ✅ **Comparten dos anclas del motor y un operativo (`resultado CPCCS`)** — `DEMOSTRADO` por lectura
  de ambos ADN.
- ✅ **Hay constancia de cruce en el código**: `scripts/enrich_participacion.py:232` documenta que
  *«AQUÍ SE LEÍA `snap["rendicion"]["serie"]` — EL BLOQUE DE d09»*, ya corregido. `DEMOSTRADO`.
- ⚠️ **Ontológicamente son inversos**: uno es **entrada** de voz ciudadana; el otro, **salida** de
  responsabilidad institucional. **Comparten evidencia y mecanismos; difieren en sujeto y dirección.**
  → Candidato a **fusión bajo «control social»** *o* a **mantener con frontera reforzada**.
  **`NO DEMOSTRADO` en ambos sentidos: es precisamente lo que la mesa debe resolver.**

### Las doce preguntas que responderá cada cajón en `D1.0`

realidad administrativa que representa · sujeto · objeto · decisiones públicas que permite observar ·
indicadores propios · fuentes · evidencia · quién necesita sus datos · quién duplica su información ·
si puede existir independientemente · **si es dominio o dimensión transversal** · qué ocurre si se
fusiona.

### El átomo de `D1` — concepto de trabajo, no nombre de producto

Antes de las ocho capas hay que definir **qué objeto gobiernan todas ellas**. Provisionalmente
`CANONICAL_ASSERTION`:

```
REALIDAD ADMINISTRATIVA
   ├── identidad          ├── evidencia
   ├── significado        ├── regla
   ├── valor              ├── estado epistemológico
   ├── unidad             ├── procedencia
   ├── universo           ├── vigencia
   ├── tiempo / corte     └── condiciones de afirmación
   └── fuente
```

⛔ **No se proponen como canon.** `D1` debe determinar **cuáles son obligatorios** — y ésa es la
cirugía real del Excel: *¿puede una celda del nuevo Gold Master representar una **afirmación
completa**, o sólo una magnitud?*

### La regla propuesta para `D1` — PROPUESTA `REARQ`, no doctrina

> **Ninguna afirmación canónica debe poder existir únicamente como magnitud cuando su interpretación
> dependa de una propiedad contextual que determine qué puede afirmarse a partir de ella.**

No exige cargar cuarenta metadatos a cada número. Dice algo más preciso: **si una propiedad cambia la
admisibilidad de la afirmación, esa propiedad forma parte del estado gobernado de la afirmación.**
Nace directamente de `P0`, `P1` y `P2`.

### La prueba de estrés agéntica

> **Si un agente recibe solamente el valor, ¿puede producir una afirmación correcta sin inventar el
> resto?** Si la respuesta es no, `D1` tiene trabajo.

### Los cuatro artefactos que debe producir `D1` — documentos, no código

| | artefacto | contenido |
|---|---|---|
| **D1-A** | **matriz de estructura canónica** | las propiedades mínimas de una afirmación |
| **D1-B** | **matriz rector → propiedad** | quién la define · quién la representa · quién la valida · quién la consume |
| **D1-C** | **matriz de brecha del Gold Master** | estructura actual del Excel **vs** estructura requerida — aquí aparece la cirugía |
| **D1-D** | **contrato conceptual de consumo** | qué reciben `gm_snapshot`, los dominios, GeoTwin, Supabase/Neo4j, QUIRA IA y los agentes — y **qué no pueden perder** |

Cada hallazgo se clasifica **`DEMOSTRADO` · `INFERENCIA RAZONABLE` · `NO DEMOSTRADO` ·
`NO DETERMINABLE`**.

### Lo que `D1`/`D1.0` NO hacen

No modifican el Gold Master. No declaran los campos definitivos. No declaran el número final de
dominios. No fusionan ni eliminan cajón alguno. No tocan el Diccionario —que **no se destruye**: el
Diccionario responde *«¿qué es esta realidad administrativa?»*, y `D1` responde *«¿qué debe acompañar
a una afirmación sobre ella para ser canónica y consumible?»*—. **Y nadie «arregla» el Excel hasta
que las cuatro matrices estén cerradas.**

## 5-quatervicies · QUIRA 7 · DECISIONES DE MESA — restricciones de diseño, no hipótesis

> ⛔ **Estas decisiones ya fueron adoptadas por la dirección. NO se reabren** salvo que aparezca
> evidencia de una incompatibilidad ontológica grave. Quedan escritas aquí para que **no haya que
> volver a explicarlas**.

| # | decisión | quién y cuándo |
|---|---|---|
| **1** | **`d01` + `d02` → UNA sola estructura** en QUIRA 7 | dirección |
| **2** | **El componente de financiamiento externo sale** de esa estructura → **producto QUIRA Cooperación** | dirección |
| **3** | **Participación + Rendición de Cuentas → UN dominio**, con **secciones internas diferenciadas** | dirección |
| **4** | **SAT deja de ser dominio**: sus señales viven dentro de cada dominio y **forman parte de la BRN** | **ordenado por Javo** *(decisión previa, ya ejecutada en parte)* |
| **5** | **Transparencia NO es un cajón equivalente: es la capa de alimentación** que surte mensualmente al resto | dirección |
| **6** | **Fuentes oficiales de alimentación:** DPE/Transparencia · CPCCS · SERCOP · **web oficial del GAD** | dirección |
| **7** | **QUIRA debe ser RECURSIVA** para encontrar la información municipal en sus fuentes oficiales | dirección |
| **8** | **QUIRA 7 no se construye sobre el molde de las versiones anteriores** | dirección |

*(Nota de nomenclatura, para que el registro no herede una ambigüedad: en el Diccionario histórico el
ADN de Transparencia es el `07` y el `06` es Salud Institucional. **En QUIRA 7 la numeración heredada
deja de ser relevante**; lo que se conserva es la decisión, no el número.)*

### `D1.0` se reformula — los cajones son material arqueológico, no el resultado esperado

⛔ **La pregunta ya NO es** *«¿mantener, fusionar o eliminar los trece cajones?»*. Es:

> **¿Qué unidades de realidad administrativa necesita QUIRA 7 para observar, relacionar, verificar y
> explicar la gestión pública municipal, con independencia de cómo estuvieran divididas las versiones
> anteriores?**

**Los trece cajones se auditan sólo como EVIDENCIA** para identificar realidades, capacidades,
relaciones, fuentes, indicadores y dimensiones transversales. **No son el molde.**

### Cinco categorías de salida — «transversal» y «fuente» dejan de confundirse

**1 · DOMINIO** · **2 · FUSIÓN / ESTRUCTURA COMPUESTA** · **3 · SUBESTRUCTURA** ·
**4 · DIMENSIÓN TRANSVERSAL** · **5 · INFRAESTRUCTURA DE ALIMENTACIÓN**.

**El resultado de `D1.0` no debe leerse como *«QUIRA tiene N dominios»***, sino como: *QUIRA 7 observa
estas realidades administrativas —cada una con su sujeto, objeto, propósito analítico, evidencia,
temporalidad y relación con las demás—; y estas otras cosas **no son dominios**: son fuentes,
dimensiones transversales, reglas, productos o infraestructuras.* **El conteo viene después.**

### La arquitectura de alimentación que abre la decisión 5-7

```
FUENTES OFICIALES → DPE/Transparencia · CPCCS · SERCOP · web oficial del GAD
        ↓
MOTOR DE ADQUISICIÓN RECURSIVA
        ↓
ESTADO CANÓNICO  →  DOMINIOS  →  BRN  →  PRODUCTOS / AGENTES
```

**Transparencia deja de competir ontológicamente con los dominios que alimenta.**

### Las condiciones técnicas de cada decisión — lo que esta dirección aporta

*(La dirección pidió argumentos válidos, no apelaciones a lo existente. Ninguno de estos puntos
objeta las decisiones: son las condiciones bajo las cuales se sostienen.)*

| decisión | condición que debe cumplirse en el diseño | por qué |
|---|---|---|
| **`d01`+`d02` fusionados** | la estructura fusionada debe **declarar su régimen temporal por sección**: la planificación es plurianual y de hitos; la ejecución presupuestaria es mensual y con corte | son **dos cadencias distintas dentro de una misma realidad**. `C4-P1` demostró que hoy el sistema mezcla cadencias sin declararlo; una fusión sin esa declaración **industrializaría** ese defecto |
| **financiamiento → QUIRA Cooperación** | separar **captación externa** (cooperación, fondos, elegibilidad → sale) de **sostenibilidad fiscal propia** (estructura del gasto, regla COOTAD → **se queda**) | la sostenibilidad fiscal **no es cooperación**: es capacidad de la institución para sostener lo que planifica. Si sale con el financiamiento, el dominio fusionado pierde la variable que explica por qué la trayectoria se cumple o no |
| **participación + rendición en un dominio** | el **sujeto obligado** debe ser atributo declarado **por sección**: en participación el sujeto es la ciudadanía que incide; en rendición, la institución que responde ante el CPCCS | sin ese atributo, el dominio podría **afirmar cumplimiento institucional a partir de evidencia del lado ciudadano** — un salto de sujeto, que es la familia de defecto del mecanismo B de `C4` |
| **SAT dentro de los dominios + BRN** | ninguna: **la decisión además salda una deuda medida** — `check_sat_brn` en vivo reporta **6 de 10 señales sin cadena BRN** | hoy umbral y peso de esas señales viven sólo en el Excel; llevarlas a la BRN convierte una deuda incidental en estructura |
| **Transparencia como infraestructura** | asignar explícitamente **su segundo papel**: el cumplimiento de transparencia **también es un hecho observable** que QUIRA reporta | la decisión fija su función arquitectónica (alimentar). Falta decidir **dónde vive la observación** de si el GAD cumple — como indicador dentro del dominio de control social, o como dimensión transversal. Si no se asigna, **desaparece del mapa** |
| **recursividad en fuentes oficiales** | cada documento adquirido debe llegar con **procedencia por documento** y **estado de evidencia** desde el primer salto | un adquiridor recursivo sin esas dos propiedades **reproduce los cuatro mecanismos de `C4` a escala industrial**: traería miles de valores sin la condición que los hace afirmables |

### Clasificación del trabajo de `D1.0` hasta aquí

| | |
|---|---|
| ✅ **DEMOSTRADO** | el Diccionario contiene 13 cajones · existe la plantilla madre de 11 campos · GeoTwin tiene precedente documental como dimensión transversal · `d01`/`d02` presentan solapamiento material (mismas celdas) · `d08`/`d09` comparten anclas e indicador operativo, y existió un cruce de lectura en código |
| ⛔ **NO DEMOSTRADO** | que el solapamiento **por sí mismo** implique fusión *(la fusión es decisión de mesa, no consecuencia del hallazgo)* |
| 🏛️ **DECISIÓN DE MESA** | `d01`+`d02` se fusionan · `d08`+`d09` se fusionan con secciones · SAT deja de ser dominio · Transparencia opera como alimentación transversal · el financiamiento externo va a QUIRA Cooperación |
| ⏳ **PENDIENTE DE DISEÑO** | cuál será exactamente la nueva ontología y **cuántos** dominios tendrá QUIRA 7 |

**Y el `⏳ PENDIENTE` que circula como dato operativo** *(Cajón 02 · `CHK-08`)* **se conserva en `D1`
con su significado correcto:** no es un argumento contra los cajones — es evidencia de que **tener un
campo de estado en el Diccionario no garantiza que ese estado gobierne la circulación del dato.** Es
el aprendizaje de `C4` llevado a la cirugía.

### El orden que queda fijado

**1 ·** cerrar la **anatomía real de QUIRA 7** *(`D1.0`)* → **2 ·** diseñar el `CANONICAL_ASSERTION`
*(`D1-A`)* → **3 ·** decidir cómo debe verse el Gold Master *(`D1-C` y la cirugía)*. **No al revés.**

## 5-quinvicies · `D1.0` · **MAPA ONTOLÓGICO DE QUIRA 7** — primera propuesta

> **Regla de esta fase:** las decisiones de Javo son **restricciones de diseño**; **la forma interna
> de la nueva arquitectura sí puede corregirse** si la evidencia demuestra que una estructura
> propuesta no representa adecuadamente la realidad administrativa. *(Eso es lo que la dirección
> pidió: no obediencia a la arquitectura vieja, sino argumentos.)*
>
> **Los trece cajones se usaron como evidencia arqueológica. Ninguna unidad de abajo se hereda: cada
> una se sostiene por su realidad, su sujeto y su prueba de eliminación.**

### La prueba que ordena todo el mapa

> **Si eliminamos esta unidad, ¿qué realidad administrativa deja de poder observar QUIRA?**
> **Si sólo desaparece una etiqueta histórica, no es razón suficiente para conservarla.**

### A · Unidades propuestas como DOMINIO

| unidad | realidad administrativa | sujeto | objeto | ¿qué se pierde si desaparece? | LATAM |
|---|---|---|---|---|---|
| **U1 · Conducción estratégica y de recursos** *(fusión fijada)* | el municipio convierte una trayectoria planificada en **capacidad efectiva de acción** mediante la asignación y ejecución de recursos | la institución que conduce | el plan y los recursos que lo materializan | **todo**: es la realidad central de la gestión pública | **alta** — todo Estado subnacional planifica y presupuesta |
| **U2 · Fidelidad del mandato** | correspondencia entre **la palabra empeñada ante el electorado** y el plan que el Estado formaliza | **la autoridad electa** *(sujeto distinto de U1)* | promesa de campaña ↔ objetivo del plan | el **vínculo democrático**: sin ella QUIRA observa gestión, no mandato | **alta** — donde haya elección programática |
| **U3 · Relación pública de la gestión** *(fusión fijada, con secciones)* | el vínculo entre sociedad e institución: **la ciudadanía incide** y **la institución responde y se somete a control** | dos sujetos, uno por sección | la incidencia, la respuesta y la evidencia del vínculo | la posibilidad de observar **el circuito completo** de control social, hoy partido en dos cajones | **alta** — varía el órgano, no la realidad |
| **U4 · Cobertura y acceso territorial** | déficit real de servicios básicos e infraestructura **por parroquia**, y su brecha urbano-rural | el territorio y su población | agua, saneamiento, residuos, vialidad, NBI | la **materialidad**: dónde el gasto se convirtió en servicio y dónde no | **alta** |
| **U5 · Dinamización económica territorial** | capacidad productiva y de empleo del territorio | el tejido productivo | PEA, cadenas de valor, informalidad | la lectura de si el desarrollo **genera economía**, no sólo obra | **alta** |
| **U6 · Resiliencia ambiental** | integridad ecológica y exposición del territorio al riesgo biofísico | el patrimonio natural y quien lo administra | conservación, riesgo, ODS ambientales | la dimensión que **condiciona la viabilidad futura** de todo lo demás | **alta** |

### B · Unidades propuestas como DIMENSIÓN TRANSVERSAL

| unidad | por qué NO es dominio | cómo opera | prueba de eliminación |
|---|---|---|---|
| **Perímetro institucional** *(antes «Holding»)* | no es una realidad observada distinta: es **el sujeto sobre el que se observan las demás**. El municipio no es una entidad sino un conjunto (GAD · EP · Patronato · Bomberos) | **cada observación declara su ente**; la lectura consolidada es una **pregunta de segundo orden** sobre las mismas observaciones | si se elimina y cada unidad declara su ente, **no se pierde realidad: se gana precisión**. Sólo se perdería la vista consolidada, que es derivable |
| **Equidad e inclusión** | sus indicadores son **lentes sobre otras realidades** (presupuesto con enfoque de género = lente sobre recursos; brechas de grupos prioritarios = lente sobre cobertura) | **desagregación obligatoria** en las demás unidades | ⚠️ **caso mixto**: la protección de grupos prioritarios **sí es obligación propia** con normativa propia. → transversal **con una subestructura** donde viva esa obligación |
| **Síntesis de cumplimiento institucional** *(antes «Salud Institucional»)* | por su propio ADN **es el agregado de vectores que viven en otras unidades** | **índice de cabecera derivado**, nunca fuente | si desaparece, **no se pierde ninguna observación**: se pierde una síntesis, que es recalculable |
| **GeoTwin** | ya está declarado así en el canon vigente | espacializa indicadores reales de cada unidad | precedente propio: QUIRA ya decidió una vez que algo sea dimensión y no cajón |

### C · Infraestructura, productos y vistas — **no son dominios**

| unidad | naturaleza | argumento |
|---|---|---|
| **Adquisición recursiva de fuentes oficiales** *(DPE/Transparencia · CPCCS · SERCOP · web del GAD)* | **INFRAESTRUCTURA DE ALIMENTACIÓN** | alimenta mensualmente a todas las unidades. **No compite ontológicamente con lo que alimenta** |
| **Transparencia como hecho observado** *(cumplimiento LOTAIP, oportunidad, observancia contractual)* | **SECCIÓN dentro de `U3`** *(propuesta)* | ⚠️ **la fuente y el hecho no son lo mismo.** Que la información pública alimente a QUIRA no borra la realidad *«¿el GAD publica adecuadamente?»*. Vive en `U3` porque **comparte sujeto y familia de obligación**: la institución que debe informar. *(Alternativa para la mesa: dimensión transversal de verificabilidad.)* |
| **Riesgo institucional activo** *(antes SAT como cajón)* | **VISTA derivada** | **decisión de Javo ya ejecutada**: las señales viven en cada dominio y en la BRN. Si ninguna unidad la contiene, **no se pierde realidad — se pierde una vista**, que es derivable de las señales |
| **Cooperación y financiamiento externo** | **PRODUCTO especializado** (QUIRA Cooperación) | sale de la ontología de observación por decisión de la dirección. **Se queda en `U1` la sostenibilidad fiscal propia**, que no es cooperación sino capacidad de sostener lo planificado |

### D · Las dos fusiones, diseñadas — no debatidas

**`U1` · Conducción estratégica y de recursos**

| sección | contenido | temporalidad declarada |
|---|---|---|
| **Trayectoria** | objetivos, metas del plan, hitos, programación operativa | **plurianual + anual**, por hitos |
| **Recursos** | asignación, ejecución devengada, estructura y sostenibilidad fiscal | **mensual, con corte explícito** |

> ⛔ **La unidad ontológica no obliga a un tiempo único.** `U1` debe **expresar temporalidades
> múltiples sin romper su unidad**: cada sección declara su régimen, y ninguna afirmación puede
> cruzar de una a otra sin declarar el cambio. **Es la lección directa de `C4-P1`.**
>
> **El nombre queda abierto a propósito.** *«Planificación y Presupuesto»* seguiría pensando con el
> vocabulario de los cajones. **El objeto primero; el nombre después.**

**`U3` · Relación pública de la gestión**

| sección | sujeto | objeto |
|---|---|---|
| **A · Voz ciudadana** | la ciudadanía que incide | mecanismos, asambleas, presupuesto participativo, cobertura territorial de la voz |
| **B · Respuesta institucional** | la institución que rinde ante el CPCCS | circuito de rendición, compromisos, cumplimiento |
| **C · Evidencia del vínculo** | — | trazabilidad aporte → decisión → resultado |
| **D · Apertura verificable** *(propuesta)* | la institución que debe informar | cumplimiento LOTAIP, oportunidad, observancia contractual |

> ⛔ **Fusionar NO es igualar.** *Participación ≠ rendición*: son componentes de una realidad
> relacional mayor que **conservan sujeto, objeto, evidencia e indicadores propios**. El **sujeto
> obligado** es atributo declarado **por sección** — sin él, el dominio podría afirmar cumplimiento
> institucional con evidencia del lado ciudadano.
>
> **Ganancia para agentes:** un agente puede recorrer **la relación completa** —voz → respuesta →
> evidencia— sin inventar el vínculo entre dos cajones independientes.

### E · La adquisición recursiva — lo que debe recorrer el sistema

⛔ **El objeto que viaja no puede ser una URL ni un archivo.** Si lo fuera, la recursividad sería un
*crawler* más sofisticado, y **QUIRA escalaría la adquisición sin escalar la verificabilidad.**

```
fuente encontrada → documento → identidad → fecha → entidad → contenido
                 → procedencia → estado de evidencia → realidad administrativa que toca
```

> **Cada salto recursivo debe aumentar el grafo de evidencia sin perder la cadena de procedencia.**

### F · Lo que este mapa NO hace

⛔ **No fija el número de dominios.** Si la mesa validara el mapa tal cual, resultarían seis unidades
de dominio, cuatro transversales, una infraestructura, un producto y una vista — **pero ese conteo es
una CONSECUENCIA provisional, no un objetivo.** Lo que importa es poder defender **por qué existe cada
unidad y por qué no existen las demás.**

No modifica Excel, código ni Diccionario. No renombra nada. No declara canon. **`U2` (mandato), el
caso mixto de equidad y la ubicación de la transparencia observada son las tres preguntas que la mesa
debe resolver para cerrar `D1.0`.**

## 5-sexvicies · `D1.0` · dos correcciones al mapa — asesoría pedida por la dirección

### 1 · Grupos de atención prioritaria: **SÍ es dominio.** Y el caso mixto se disuelve

**La dirección pidió asesoría, no ratificación. Ésta es la recomendación, con su argumento.**

Mi clasificación anterior —*«transversal con subestructura»*— **mezclaba dos realidades distintas**.
Separadas, la respuesta es clara:

| | qué observa | naturaleza |
|---|---|---|
| **el sistema de protección de derechos** | ¿existe el aparato institucional de protección? ¿opera? ¿tiene presupuesto asignado? ¿atiende y con qué ruta? | **DOMINIO** |
| **el sesgo distributivo del resto** | ¿cómo se reparten recursos, servicios y cobertura entre grupos? | **DIMENSIÓN TRANSVERSAL** (desagregación obligatoria) |

⚠️ **CORRECCIÓN DE LA DIRECCIÓN (2026-09-17) — y el error era mío.** Una versión anterior de este
párrafo puso como aparato del dominio *«consejo cantonal de protección de derechos, juntas de
protección»*. **Eso confunde órganos distintos y desvía el objeto de QUIRA.** Quedan separados:

| órgano | qué es | ¿objeto de QUIRA? |
|---|---|---|
| **Concejo Cantonal del GAD** | alcalde + concejales electos · **máxima autoridad de decisión del cantón**: gobierna, legisla y fiscaliza | **sí** — es el GAD |
| **Consejo Cantonal de Protección de Derechos (CCPD)** | autoridad del GAD + delegados del Estado y sociedad civil (50/50) · **asesora y diseña política de derechos**, propone ordenanzas | **sólo indirectamente** *(ver abajo)* |
| **Junta Cantonal de Protección (JCPD)** | 3 profesionales por concurso · **dicta medidas de protección de emergencia en casos individuales** | ⛔ **NO** |

> **Lo que interesa a QUIRA es la relación entre el GAD y la dirección, empresa o entidad que
> OPERATIVIZA los programas y proyectos dirigidos a los grupos de atención prioritaria.** En
> Montecristi esa función la cumple el **Patronato Municipal**; en la mayoría de GAD del país la
> cumple una **dirección interna**, una **empresa pública** o una **entidad desconcentrada** —el
> COOTAD ordenó eliminar los patronatos y pocos subsisten—.

**Los tres argumentos que lo hacen dominio:**

1. **Sujeto propio.** Los grupos de atención prioritaria son **sujetos de derechos reconocidos
   constitucionalmente** — no son un atributo de otro sujeto ni una segmentación analítica.
2. **Función propia dentro del GAD, con presupuesto propio.** Existe una **unidad ejecutora**
   —dirección, empresa o entidad— que ejecuta programas y proyectos para esos grupos, con
   **asignación presupuestaria, cobertura y resultados observables** en POA, PAC, presupuesto,
   transparencia y rendición. Eso **es** una realidad administrativa del GAD.
3. **La prueba de eliminación lo resuelve.** Si se elimina y se reparte como desagregación,
   **se pierde la observación de esa función ejecutora**: nadie ve si existe la unidad, qué
   presupuesto recibe, qué programas ejecuta y a cuántas personas atiende. **La desagregación por
   grupo en otros dominios no puede observar eso.** → **No es una etiqueta: es una realidad que
   quedaría sin observador.**

**La frontera, escrita para que no se cruce:**

> ✅ **Dentro:** ¿existe la unidad ejecutora? · ¿qué presupuesto se le asigna y cuánto ejecuta? · ¿qué
> programas y proyectos opera? · ¿qué cobertura y qué resultados declara? · ¿el GAD constituyó y
> financia las instancias que la ley le manda constituir? · ¿produjo las ordenanzas correspondientes?
> **Todo eso son hechos del GAD, y viven en documentos que QUIRA ya adquiere.**
>
> ⛔ **Fuera:** el trabajo de casos individuales de la `JCPD` y del `CCPD` —medidas de protección,
> boletas, denuncias—. **Y no sólo por competencia: son datos personales sensibles de víctimas.**
> QUIRA observa **la gestión pública territorial**, no expedientes de personas. **Esa frontera es
> arquitectónica y ética, y no se negocia por conveniencia analítica.**

**Consecuencia para LATAM —y es de las importantes—:** el dominio debe modelar **la FUNCIÓN**
*(quién operativiza la atención a grupos prioritarios)*, **no la FIGURA** *(«Patronato»)*. La figura
cambia por municipio y por país; la función existe siempre. Esto encaja con la transversal de
**perímetro institucional**: **la entidad ejecutora es un atributo declarado de cada observación, no
la identidad del dominio** — y QUIRA ya lo hace así en el motor, donde el Patronato es `ENTE-02`
junto al GAD (`ENTE-01`), Bomberos (`ENTE-03`) y la EP de Aseo (`ENTE-04`).

**Y la función transversal no se pierde:** sigue siendo desagregación obligatoria en las demás
unidades. **Dominio y transversal no compiten: observan cosas distintas.**

> ⚠️ **Advertencia de coste, verificada hoy:** **no existe ninguna `CNO`/`RO` en la BRN sobre grupos
> de atención prioritaria ni protección integral** *(universo: `docs/brn`, `data/d12`, `docs/pcd`)*.
> Convertirlo en dominio exige **construir su cadena normativa desde cero** —Constitución, COOTAD y
> las leyes especiales de cada grupo—, **con verificación `SHA` contra el corpus antes de escribir un
> solo artículo** (Regla de Oro 3). **Es el dominio con mayor trabajo normativo pendiente del mapa**,
> y eso debe entrar en la planificación, no descubrirse después.
>
> *(El `PSG` —presupuesto con enfoque de género— es indicador de la **transversal**, no del dominio:
> mide sesgo distributivo, no funcionamiento del sistema de protección.)*

### 2 · Transparencia: no es una función, son **tres** — y eso cambia su lugar

**La dirección precisó lo que QUIRA ya construyó.** Con eso, la capa queda así:

| | función | qué produce |
|---|---|---|
| **T1** | **Calificar** la publicación mensual del GAD en el portal de la DPE | un **gate de admisión**: decide si el contenido puede alimentar, y con qué calidad |
| **T2** | **Extraer el contenido** de lo publicado | insumo que alimenta a los demás dominios, **con su calificación adherida** |
| **T3** | **Adquirir documentos oficiales primarios en la web del GAD** — PDOT, orgánico por procesos, POA, PAC, presupuestos— **en formato oficial**, no como los publica transparencia | evidencia primaria, distinta de la republicada |

**Lo ya construido y verificado:** `METODOLOGIA_D07_CUMPLIMIENTO_LOTAIP` nace en el canon (Regla 9) con
su cadena normativa **ingerida y con huella** —Guía Metodológica (Res. 019) · Instructivo de
Parámetros Técnicos (Res. 015) · Instructivo de Monitoreo—, y `app/agents/d07/scoring.py` implementa
sus reglas. **La maquinaria de calificación existe y está fundada en norma verificada.**

**Corrección a mi propuesta anterior:** dije que la transparencia observada fuera **sección de `U3`**.
Con `T1` a la vista, la ubicación correcta se parte en dos:

> **La CALIFICACIÓN vive en la infraestructura** —porque **gobierna la admisión** del contenido: es
> el control de calidad de la alimentación, no un reporte—.
> **Su RESULTADO es un hecho publicable** —*«¿el GAD publica adecuadamente?»*— y **ahí sí** propongo
> exponerlo en `U3`, por sujeto y familia de obligación compartidos. *(La mesa decide si en `U3` o
> como dimensión de verificabilidad.)*

**Y una capacidad que emerge de `T3`, que no estaba en el mapa:** el mismo documento puede llegar por
**dos vías** —portal de transparencia y web oficial del GAD— y **pueden no coincidir**. Por eso el
objeto adquirido debe registrar **vía de adquisición y versión**, y entonces:

> ⭐ **La divergencia entre lo publicado en transparencia y el documento oficial es, en sí misma, una
> observación de valor.** No es un problema técnico a resolver: es **evidencia sobre la calidad de la
> publicación**, que sólo puede verse si la procedencia distingue la vía. **Es exactamente la lección
> de `C4` aplicada a la adquisición.**

### Efecto en el mapa

| unidad | antes | ahora |
|---|---|---|
| **Grupos de atención prioritaria** | transversal con subestructura *(caso mixto)* | ✅ **DOMINIO** *(sistema de protección)* **+** dimensión transversal *(desagregación)* — **dos unidades, no una ambigua** |
| **Transparencia** | infraestructura + hecho observado en `U3` | **infraestructura con calificación** (`T1`·`T2`·`T3`) · el **resultado** se publica en `U3` · **se registra la vía de adquisición** |

**Las tres preguntas abiertas de `D1.0` bajan a dos:** el mandato (`U2`) como dominio propio, y si el
cumplimiento de transparencia se expone en `U3` o como dimensión de verificabilidad.

## 5-septvicies · **CATÁLOGO DE DOMINIOS DE QUIRA 7** — para revisión de la dirección

> **Propósito de esta sección:** que no haya sorpresas. Cada unidad declara **qué observa, qué
> contiene, qué NO contiene y adónde va lo que no contiene**, más **el estado real de su cadena
> normativa**. Los nombres son **provisionales**: el objeto primero, el nombre después.

### A · Los siete dominios

#### `U1` · Conducción estratégica y de recursos *(fusión fijada)*

| | |
|---|---|
| **observa** | cómo el GAD convierte una trayectoria planificada en capacidad efectiva de acción mediante asignación y ejecución de recursos |
| **sujeto** | la institución que conduce *(entidad ejecutora declarada por observación)* |
| **contiene · sección Trayectoria** | objetivos y metas del plan de desarrollo · hitos · programación operativa anual · alineación con instrumentos nacionales · **temporalidad plurianual/anual por hitos** |
| **contiene · sección Recursos** | asignación presupuestaria · ejecución devengada · estructura del gasto · **sostenibilidad fiscal propia** · plan de contratación · **temporalidad mensual con corte explícito** |
| **NO contiene** | captación de fondos externos y cooperación → **producto QUIRA Cooperación** · avance material en territorio → `U4` · publicación de los documentos → **infraestructura** · promesas de campaña → `U2` |
| **fuentes** | PDOT · POA · PAC · cédulas presupuestarias · portal de contratación · **documentos oficiales del GAD adquiridos por `T3`** |
| **cadena normativa** | familias **`I`** (d01) y **`IV`** (d02) existen · `BOOT` declara **`RO` de d01 NO cargada**; la de d02 **sí** |
| **falta** | cargar la `RO` de la sección Trayectoria · **declarar el régimen temporal por sección** *(condición de la fusión)* |

#### `U2` · Fidelidad del mandato

| | |
|---|---|
| **observa** | correspondencia entre la palabra empeñada ante el electorado y el plan que el Estado formaliza |
| **sujeto** | **la autoridad electa** — sujeto distinto del de `U1` |
| **contiene** | plan de trabajo inscrito ante el órgano electoral · trazabilidad promesa ↔ objetivo del plan · integridad del compromiso a lo largo del período |
| **NO contiene** | la ejecución financiera de lo prometido → `U1` · la rendición formal de lo cumplido → `U3` |
| **fuentes** | plan de trabajo del órgano electoral · PDOT · corpus de promesas |
| **cadena normativa** | familia **`III`** existe · `BOOT` declara **`RO` NO cargada** |
| **falta** | cargar la `RO` · decidir si es dominio propio o sección superior de `U1` **(pregunta abierta 1)** |

#### `U3` · Relación pública de la gestión *(fusión fijada)*

| sección | sujeto | contiene |
|---|---|---|
| **A · Voz ciudadana** | la ciudadanía que incide | mecanismos de participación · asambleas · presupuesto participativo · cobertura territorial de la voz · parroquias sin canal |
| **B · Respuesta institucional** | la institución que rinde | circuito de rendición ante el órgano de control social · compromisos asumidos · cumplimiento declarado |
| **C · Evidencia del vínculo** | — | trazabilidad aporte ciudadano → decisión → resultado · fidelidad entre discurso oficial y evidencia |
| **D · Apertura verificable** | la institución que debe informar | **resultado** de la calificación de transparencia · oportunidad · observancia contractual |

| | |
|---|---|
| **NO contiene** | la **calificación** de la publicación mensual → **infraestructura** *(es gate de admisión, no reporte)* · casos individuales de protección → **fuera de QUIRA** · los datos de origen que la rendición consolida → sus dominios |
| **fuentes** | actas y registros de participación · informes de rendición · portal del órgano de control social · **resultado de `T1`** |
| **cadena normativa** | **`VIII`** (8 `CNO`) y **`IX`** existen · `BOOT` declara **`RO` de d09 NO cargada**; `VIII` **propuesta**, con la nota *«d08 mide, NO dictamina»* |
| **falta** | cargar la `RO` de la sección B · **sujeto obligado como atributo por sección** *(condición de la fusión)* · decidir la ubicación de la sección D **(pregunta abierta 2)** |

#### `U4` · Cobertura y acceso territorial

| | |
|---|---|
| **observa** | déficit real de servicios básicos e infraestructura por parroquia, y la brecha urbano-rural |
| **contiene** | cobertura de agua, saneamiento y residuos · vialidad y conectividad física · déficit por parroquia · pobreza por necesidades básicas |
| **NO contiene** | el presupuesto que financia la obra → `U1` · la representación espacial → **GeoTwin** · la desagregación por grupo → **transversal de equidad** |
| **fuentes** | estadística oficial · PDOT · PUGS · obra ejecutada |
| **cadena normativa** | ⛔ **no existe** familia `CNO`/`RO` |
| **falta** | **construir su cadena normativa completa** |

#### `U5` · Dinamización económica territorial

| | |
|---|---|
| **observa** | capacidad productiva y de empleo del territorio |
| **contiene** | población económicamente activa · cadenas de valor · informalidad · relevo generacional · proyectos productivos |
| **NO contiene** | la infraestructura que lo habilita → `U4` · el presupuesto que lo financia → `U1` |
| **fuentes** | corpus económico del PDOT · estadística de empleo |
| **cadena normativa** | ⛔ **no existe** |
| **falta** | **construir su cadena normativa** · definir indicadores propios más allá del corpus |

#### `U6` · Resiliencia ambiental

| | |
|---|---|
| **observa** | integridad ecológica y exposición del territorio al riesgo biofísico |
| **contiene** | inventario biofísico · susceptibilidad a riesgos naturales · conservación · metas ambientales |
| **NO contiene** | redes urbanas como servicio → `U4` · fondos verdes → **producto Cooperación** · vulnerabilidad de grupos prioritarios → `U7` + transversal |
| **fuentes** | PDOT biofísico · capas de riesgo · metas ambientales |
| **cadena normativa** | ⛔ **no existe** |
| **falta** | **construir su cadena normativa** |

#### `U7` · Atención a grupos de atención prioritaria *(nuevo · corrección de la dirección)*

| | |
|---|---|
| **observa** | **la función ejecutora del GAD** hacia los grupos de atención prioritaria: qué unidad la opera, con qué presupuesto, qué programas y qué cobertura |
| **sujeto** | los grupos como sujetos de derechos · **la unidad ejecutora como atributo declarado** (dirección · empresa pública · entidad desconcentrada · patronato donde subsista) |
| **contiene** | existencia y forma de la unidad ejecutora · presupuesto asignado y ejecutado · programas y proyectos · cobertura y resultados declarados · **si el GAD constituyó y financia las instancias que la ley le manda** · ordenanzas producidas |
| **NO contiene** | ⛔ **casos individuales** de la Junta Cantonal de Protección y del Consejo Cantonal de Protección de Derechos — **competencia ajena y datos personales sensibles** · el sesgo distributivo general → **transversal de equidad** |
| **fuentes** | POA · PAC · presupuesto · transparencia · rendición · ordenanzas |
| **cadena normativa** | ⛔ **NO existe ninguna** *(verificado: `docs/brn`, `data/d12`, `docs/pcd`)* |
| **falta** | **es el dominio con mayor trabajo normativo del mapa**: Constitución, COOTAD y leyes especiales de cada grupo, **con verificación `SHA` antes de escribir articulado** |

### B · Las cuatro dimensiones transversales

| transversal | qué hace | cómo opera | estado |
|---|---|---|---|
| **Perímetro institucional** | declara **qué entidad** produce cada observación | atributo obligatorio en toda afirmación · vista consolidada **derivada** | ya existe en el motor (`ENTE-01`…`ENTE-04`) · sin cadena normativa |
| **Equidad y desagregación** | obliga a desagregar por grupo en las demás unidades | dimensión de análisis, no dominio | indicador de presupuesto con enfoque de género ya existe |
| **Síntesis de cumplimiento institucional** | índice de cabecera **derivado** de vectores de otras unidades | nunca es fuente · siempre recalculable | existe como ICPI · **su guarda temporal es el único gobierno probado** *(`C4-P0`)* |
| **GeoTwin** | espacializa indicadores reales de cada unidad | ya declarada transversal en el canon vigente | precedente documental |

### C · Infraestructura, producto y vista

| unidad | qué es | contiene | estado |
|---|---|---|---|
| **Adquisición recursiva** | **INFRAESTRUCTURA DE ALIMENTACIÓN** | `T1` calificar la publicación mensual *(gate de admisión)* · `T2` extraer contenido · `T3` adquirir documentos oficiales primarios en la web del GAD · **registro de vía y versión** | **la más madura**: familia `VII` existe y `BOOT` la declara cargada · metodología aprobada con su cadena normativa ingerida |
| **QUIRA Cooperación** | **PRODUCTO especializado** | captación externa · elegibilidad · fondos y riesgo | sale de la ontología de observación |
| **Riesgo institucional activo** | **VISTA derivada** | consolidado de señales que viven en los dominios y en la BRN | **decisión ya ejecutada**: SAT dejó de ser dominio · deuda medida en vivo: 6 de 10 señales sin cadena BRN |

### D · Verificación de que NADA se perdió — los trece cajones y su destino

| cajón histórico | destino en QUIRA 7 |
|---|---|
| 01 · Planificación Estratégica | `U1` · sección Trayectoria |
| 02 · Presupuesto & Financiamiento | `U1` · sección Recursos · **financiamiento externo → producto Cooperación** |
| 03 · Gobernanza del Mandato | `U2` |
| 04 · Alertas Institucionales | **vista derivada** + señales en cada dominio + BRN |
| 05 · Holding e Integración Municipal | **transversal · perímetro institucional** |
| 06 · Salud Institucional | **transversal · síntesis de cumplimiento** |
| 07 · Transparencia | **infraestructura** (`T1`·`T2`·`T3`) + **resultado** en `U3-D` |
| 08 · Participación Ciudadana | `U3` · sección A |
| 09 · Rendición de Cuentas | `U3` · secciones B y C |
| 10 · Cobertura de Servicios e Infraestructura | `U4` |
| 11 · Desarrollo Económico Territorial | `U5` |
| 12 · Inclusión, Equidad y Género | `U7` *(función ejecutora)* **+** transversal de equidad |
| 13 · Sostenibilidad y Resiliencia Ambiental | `U6` |
| GeoTwin *(ya transversal)* | **transversal** |

> ✅ **Ningún contenido histórico queda huérfano, y ninguna unidad nueva se creó sin realidad que
> observar.**

### E · Estado de la cadena normativa — lo que falta, sin adornos

| | unidades |
|---|---|
| ✅ **cadena existente y declarada cargada** | infraestructura de transparencia (`VII`) · `U1` sección Recursos (`IV`) |
| ⚠️ **cadena existente, `RO` NO cargada** *(según `BOOT`)* | `U1` Trayectoria (`I`) · `U2` (`III`) · `U3` sección B (`IX`) · `U3` sección A (`VIII`, propuesta) |
| ⛔ **sin ninguna cadena normativa** | `U4` · `U5` · `U6` · **`U7`** · perímetro institucional |

**Ésa es la carga real de trabajo normativo de QUIRA 7, y se conoce antes de empezar — no a mitad
de camino.**

### F · Preguntas abiertas que la dirección debe cerrar

1. **`U2`**: ¿dominio propio o sección superior de `U1`?
2. **`U3-D`**: ¿el resultado de transparencia se expone en `U3` o como dimensión de verificabilidad?
3. **Nombres definitivos** de `U1`, `U3` y `U7` — pendientes a propósito hasta que el objeto esté
   cerrado.

## 5-octovicies · `D1.0` · **PRUEBA DE EXHAUSTIVIDAD** — los siete dominios NO cubren la gestión pública intermedia

> **La dirección preguntó si los siete dominios integran toda la gestión pública intermedia y dijo no
> estar de acuerdo. Respuesta de esta dirección técnica, con inventario: NO LA CUBREN.**
> Los siete eran una **hipótesis de partición**, no una demostración de cobertura. Aquí está la
> demostración de lo que falta.

### Correcciones de la dirección, acogidas sin discusión

| # | corrección | efecto |
|---|---|---|
| **1** | **Cooperación no va en el mapa ontológico** | sale por completo: es **producto QUIRA Cooperación** |
| **2** | **Fidelidad del mandato es independiente** | queda **dominio propio**: la promesa original **también es norma** · cierra la pregunta abierta 1 |
| **3** | **«Relación pública de la gestión» no es viable como nombre** | el objeto no es comunicacional: es **CONTROL SOCIAL de la gestión pública**, y eso es profundo, no general |
| **4** | **Transparencia es dominio propio, fuera de la infraestructura** | su labor es aparte: **primero califica el cumplimiento**, **después la calidad de la información** que nutrirá a los demás dominios |

### El método que cierra la deriva

⛔ **No se bautizan más dominios hasta terminar el inventario.** El orden es:
**realidades → filtros → agrupación → dominios.** Y el filtro que las separa de una vez:

| ① realidades de la gestión | ② perspectivas de observación | ③ infraestructuras | ④ productos | ⑤ señales |
|---|---|---|---|---|
| presupuesto · contratación · prestación · planificación · participación · transparencia… | territorial · equidad · cumplimiento | adquisición recursiva · extracción · GeoTwin | QUIRA Cooperación | SAT |

**Estas cinco cosas no pueden competir por ser dominio.**

> **Regla:** **no se acepta un dominio porque sea útil para organizar información. Se acepta sólo si
> representa una realidad administrativa que QUIRA necesita conocer.**

### Inventario de realidades de la gestión pública intermedia — y **lo que ya hay** en el motor

*(Universo de «lo que ya hay»: las **123 hojas** del Gold Master vigente, leídas hoy.)*

| # | realidad administrativa | ¿hogar en el mapa de 7? | material existente en el motor |
|---|---|---|---|
| 1 | **Mandato electoral** — promesa que también es norma | ✅ `U2` | `H03_S1_ELECTORAL_CNE` · `H63_S0_CNE_TRAZABILIDAD` · `H16_IFE` |
| 2 | **Producción normativa local y fiscalización del Concejo** — ordenanzas, resoluciones, sesiones, control político | ⛔ **SIN HOGAR** | ⛔ **sin hoja** |
| 3 | **Planificación del desarrollo** | ✅ `U1-A` | `H04_S2_PLANIFICACIÓN_PDOT` · `H05_S3_OPERATIVO_POA` · `H11b_MONITOR_POLITICAS` |
| 4 | **Financiamiento público propio** — ingresos, recaudación, transferencias, **autonomía financiera**, deuda | ⛔ **SIN HOGAR** *(`U1-B` cubre el gasto, no el ingreso)* | ⚠️ parcial: `H20c_IEF` · `H90_PRESUPUESTO_CONSOLIDADO` |
| 5 | **Asignación y ejecución del gasto** | ✅ `U1-B` | `H07_S5_FINANCIERO_eSIGEF` · `H07b` · `H07c` · `H_HOLDING_CEDULAS` |
| 6 | **Contratación pública** — procedimientos, proveedores, concentración, modalidades | ⚠️ **repartida** entre `U1` (PAC) y transparencia | ✅ **dos hojas propias**: `H05b_PAC_CONTRATACIÓN` · `H06_S4_CONTRATACIÓN_SERCOP` |
| 7 | **Capacidad institucional** — estructura orgánica, unidades responsables, procesos, talento humano | ⛔ **SIN HOGAR** | ✅ **material fuerte**: `H02b_ORGÁNICO_CLASIFICADOR` · `SCHEMA_ORGANICO` · `H_ORGANICO_040_2025` · `H30_IED_POR_DIRECCIÓN` |
| 8 | **Prestación y operación de servicios** — continuidad, calidad, tarifas, mantenimiento | ⛔ **SIN HOGAR** *(`U4` observa **cobertura**, que es el resultado, no la operación)* | ⚠️ indirecto: `H19b_IE_EP_EA` · `H71_EP_ADSCRITAS` |
| 9 | **Cobertura y acceso territorial** | ✅ `U4` | `SCHEMA_NBI` · `CAPA_TERRITORIAL` · `H42_IET` · `H43_MOTOR_TERRITORIAL` |
| 10 | **Regulación y control local** — uso de suelo, PUGS, catastro, permisos, licencias | ⛔ **SIN HOGAR** | ⛔ **sin hoja** |
| 11 | **Gestión de bienes y patrimonio** — inmuebles, maquinaria, patrimonio cultural | ⛔ **SIN HOGAR** | ⛔ **sin hoja** |
| 12 | **Seguridad ciudadana y gestión de riesgos** — emergencias, respuesta | ⚠️ `U6` cubre el **riesgo natural**, no la seguridad ni la respuesta | ⚠️ `SCHEMA_RIESGOS` · bomberos existe como **ente**, no como realidad |
| 13 | **Desarrollo económico territorial** | ✅ `U5` | corpus económico del PDOT |
| 14 | **Ambiente y resiliencia** | ✅ `U6` | `KB_DIAGNOSTICO_PDOT` · `H20_ICODS` |
| 15 | **Atención a grupos prioritarios** | ✅ `U7` | `H16c_PSG` · `H04b_DIAGNÓSTICO_SOCIAL` |
| 16 | **Participación y control social** | ✅ `U3` *(renombrado)* | `H10` · `H10b` · `H10c` · `H31_REPORTE_CPCCS` · `H34b_MFN` |
| 17 | **Transparencia** — cumplimiento **y** calidad de la información | ✅ **dominio propio** *(decisión)* | ✅ `H09_S7_TRANSPARENCIA_LOTAIP` · `H70_BITACORA_LOTAIP` · `H18_ITAM` · `H41_IOC` |
| 18 | **Autoreporte a sistemas nacionales** — SIGAD y similares | ⚠️ **sin hogar claro** | ✅ `H08_S6_AUTOREPORTE_SIGAD` |
| 19 | **Coordinación intergubernamental** — mancomunidades, convenios, competencias concurrentes | ⛔ **SIN HOGAR** | ⛔ **sin hoja** |

### ⛔ Las ocho brechas — esto es lo que faltaba

| brecha | ¿por qué importa para la gestión intermedia? | ¿hay material? |
|---|---|---|
| **B1 · producción normativa y fiscalización del Concejo** | el órgano que **aprueba ordenanzas y presupuesto y fiscaliza** no tiene observador. Sin él, QUIRA ve la administración pero no el **gobierno** | ⛔ nada |
| **B2 · financiamiento propio e ingresos** | sin ingresos no se explica la **autonomía financiera**: un GAD que no recauda depende de transferencias, y eso **condiciona todo lo demás** | ⚠️ parcial |
| **B3 · contratación pública** | tiene norma propia, sujeto propio, evidencia propia (SERCOP) y riesgos propios. Hoy queda partida en dos | ✅ dos hojas |
| **B4 · capacidad institucional** | **la realidad que convierte decisiones en acción**: estructura, unidades, procesos, personal. Es la que explica por qué un plan no se ejecuta | ✅ fuerte |
| **B5 · prestación y operación de servicios** | `U4` observa **el resultado** (cobertura); nadie observa **la gestión que lo produce**: continuidad, calidad, tarifas, mantenimiento | ⚠️ indirecto |
| **B6 · regulación y control local** | uso de suelo, catastro y permisos son **competencia municipal central** y hoy no existen en QUIRA | ⛔ nada |
| **B7 · bienes y patrimonio** | el municipio administra patrimonio público: sin observarlo, falta una parte del deber de administración | ⛔ nada |
| **B8 · seguridad y respuesta ante emergencias · coordinación intergubernamental** | dos realidades distintas, ambas sin hogar | ⚠️/⛔ |

> ⭐ **Cuatro de las ocho brechas YA TIENEN MATERIAL EN EL MOTOR** —contratación, capacidad
> institucional, autoreporte y, parcialmente, financiamiento y prestación—. **Es decir: QUIRA ya
> recogía evidencia de realidades que el mapa de siete dominios dejaba sin hogar.** Ésa es la prueba
> más dura de que la partición estaba incompleta — y el motivo por el que había que mirar lo que ya
> hay antes de cerrar la ontología.

### Los tres filtros que se aplicarán a cada realidad

**F1 · Realidad** — ¿existe una realidad administrativa diferenciable?
**F2 · Independencia** — ¿eliminarla hace desaparecer una capacidad explicativa distinta?
**F3 · Cobertura** — ¿queda cubierto cada aspecto esencial de la gestión pública?

**Recién después: realidades → agrupaciones ontológicas → dominios de QUIRA 7.**

### Estado

> **`D1.0` NO se cierra.** Los siete dominios quedan como **hipótesis de partición incompleta,
> con ocho brechas demostradas**. **No se pasa a `D1-A` ni a la cirugía.**
>
> **Y una distinción que la dirección debe conservar:** que hoy no exista cadena normativa para una
> realidad **no la excluye de la ontología**. `D1` produce dos cosas separadas: **(A)** qué debe
> observar QUIRA 7 · **(B)** qué parte ya está normativamente gobernada y qué parte hay que
> construir. **La ausencia de BRN nunca determina la ontología.**

## 5-novovicies · **MATRIZ DE ELEVACIÓN** — qué se conserva, qué se retira y qué se incorpora, nivel por nivel

> **Método fijado por la dirección:** *«trabajar con lo que ya hay y elevar a QUIRA desde ahí; desde
> ahí unificamos, movemos dominios y hacemos todo lo necesario para el fin último de QUIRA 7. Es la
> base que hemos trabajado por meses.»*
>
> **Inventario real del ecosistema, contado hoy:** 123 hojas del motor · 49 `ADR` · 30 `YAML` de BRN
> (6 familias) · 158 artefactos con autoridad declarada · 7 conectores · 9 *enrichers* · 6 agentes de
> dominio · 73 módulos de Sentinel · 55 páginas vivas (+4 en `_deprecated`) · 9 renders · 14 gates ·
> 57 pruebas.
>
> ⛔ **Todo lo de abajo es PROPUESTA. Nada se ejecuta hasta que la mesa decida.**

### 1 · Canon y doctrina — *49 `ADR` · Constitución · Carta · Diccionario (13 ADN) · `doctrina.py` · `MASTER_INDEX` · `BOOT`*

| | |
|---|---|
| **se eleva** | la **Carta `CAPA 0`** pasa de clasificación documental a **gobierno operativo**: el estado de evidencia debe acompañar y limitar cada afirmación *(`C4-P2`)* · el **Diccionario** pasa de definir dominios a **contrato semántico**, contrastando sus **11 campos** con las **12 propiedades** de `C4` · `canon.py` extiende su principio —**derivar el estado, no declararlo**— al estado del Gold Master |
| **se retira** | la **Regla de Oro 2** en su forma actual *(dos vocabularios)* → **vocabulario administrativo común**, con identificadores técnicos que no constituyen lenguaje alternativo · las citas y cifras escritas a mano que sobreviven en notas |
| **se incorpora** | el contrato de **afirmación canónica** · las reglas de propagación **`R1`** *(ningún derivado por encima de su canon)* y **`R2`** *(propagado ≠ copiado)* · la **frontera público/propietario** |

### 2 · Norma operacionalizada — *BRN · 30 `YAML` · familias `I·III·IV·VII·VIII·IX`*

| | |
|---|---|
| **se eleva** | las 6 familias existentes · el contrato `ID → definición → vigencia → ámbito → parámetros → autoridad → versión → consumidores → estado` |
| **se retira** | nada: **la BRN es de lo más sano del ecosistema** |
| **se incorpora** | las cadenas **inexistentes**: cobertura · economía · ambiente · **grupos prioritarios** · capacidad institucional · contratación · ingresos · regulación local · perímetro · y las `RO` declaradas **no cargadas** *(`I`, `III`, `IX`)* · **las 9 señales SAT con su umbral y peso** *(hoy 8 sin cadena: viven sólo en el Excel)* |

### 3 · Motor canónico — *Gold Master · 123 hojas*

| | |
|---|---|
| **se eleva** | las hojas que son **cálculo canónico real** · el `ICPI` con su **guarda temporal**, que es el único gobierno probado · `H07b` y su normalización · el `MFN` como evaluación experta **declarada como tal** |
| **se retira** | valores **simulados o pegados a mano** que el propio canon ya documentó *(scores simulados, cifras sin fórmula)* · rótulos que no describen su contenido *(`Grupo7_Bienes` / `Grupo8_Obras`)* · el gemelo inerte de `SAT-IV` |
| **se incorpora** | **la celda deja de ser magnitud y pasa a representar afirmación**: valor **+** unidad **+** período **+** corte **+** universo **+** evidencia **+** regla **+** estado **+** procedencia · **estados de evidencia distinguibles** *(«sin datos» ≠ «evaluado sin brecha»)* · tipos de dato correctos *(`IF_n` numérico)* · referencias a parámetros, no a encabezados |

### 4 · Adquisición — *7 conectores: DPE · CPCCS · SERCOP · Gold Master · Neo4j ×2*

| | |
|---|---|
| **se eleva** | los conectores oficiales existentes · la **metodología de calificación de transparencia**, que ya nace en el canon con su cadena normativa ingerida |
| **se retira** | la idea de que la fuente y el hecho observado son lo mismo |
| **se incorpora** | **`T3` · adquisición primaria en la web oficial del GAD** (PDOT, orgánico, POA, PAC, presupuestos **en formato oficial**) · **recursividad** · y el objeto que viaja: `documento + identidad + fecha + entidad + vía + versión + hash + procedencia + estado de evidencia` · **la divergencia entre vías como observación**, no como error a corregir |

### 5 · Derivados y estado — *snapshot · provenance · registry (158) · grafo de autoridad*

| | |
|---|---|
| **se eleva** | el snapshot como **estado consumible**, con su procedencia · `registry.yaml` y el grafo de autoridad · `provenance/ensayos` |
| **se retira** | los **derivados congelados divergentes**: `sat_gm` *(riesgo y semántica distintos del motor)* · el bloque `financiero` *(otro corte, otra base, productor no localizado)* — o se **regeneran con acto de promoción** |
| **se incorpora** | **el acto de promoción operante** *(changelog que vuelve a operar)* · **verificación por derivación independiente** · **un solo declarante del estado vigente** *(hoy hay cuatro respuestas)* |

### 6 · Dominios y agentes — *6 agentes de dominio · 9 enrichers · molde `ADR-053`*

| | |
|---|---|
| **se eleva** | el **molde `ADR-053`** —procedencia, sujeto, `evidencia_sha` + `motor_sha`— **a todos los dominios**: hoy sólo 6 de 13 tienen agente |
| **se retira** | la partición en «cajones» como criterio · los dominios que eran **síntesis o perímetro**, que pasan a transversales |
| **se incorpora** | los dominios que salen del inventario, **incluidas las ocho brechas** · **el corte y las condiciones en el contrato del agente** *(hoy `absorcion_ti_pct` viaja sin su corte)* · el **sujeto obligado** por sección en los dominios fusionados |

### 7 · Razonamiento e IA — *73 módulos de Sentinel · `RC-7.2/7.3` · `d3d4` · criterio por dominio*

| | |
|---|---|
| **se eleva** | ⭐ **`RC-7.3`**: su normalización estacional y su detector de series mezcladas son **la única guarda de comparabilidad fuera del ICPI**. **Es el patrón a propagar, no a reinventar** |
| **se retira** | los *prompts* que reciben **valores desnudos** sin período, universo, evidencia ni condición |
| **se incorpora** | el **contrato de consumo agéntico**: ningún agente recibe una magnitud sin las propiedades que determinan qué puede afirmar con ella · la prueba: *si el agente sólo recibe el valor, ¿puede afirmar correctamente sin inventar el resto?* |

### 8 · Producto y presentación — *55 páginas vivas · 9 renders · ambientes*

| | |
|---|---|
| **se eleva** | los renders que **derivan del dato** y el hallazgo que conserva su corte *(el caso de control de `C4-P1`)* |
| **se retira** | **los literales escritos a mano** *(cifras, cortes y frases que no dependen del dato)* · los dictámenes constantes que no cambian con ningún valor · las 4 páginas en `_deprecated` · el respaldo silencioso de trimestre |
| **se incorpora** | **texto, color y clasificación derivados del valor Y de su condición** · el vocabulario común de administración pública en toda superficie |

### 9 · Verificación — *14 gates · 57 pruebas · `check_health`*

| | |
|---|---|
| **se eleva** | los 14 gates y las 57 pruebas · el gate que **acaba de demostrar su valor** al detener un `BOOT` de 7032 bytes |
| **se retira** | la ambigüedad sobre **qué gate protege y cuál sólo informa** — cada uno declara su modo |
| **se incorpora** | las **seis pruebas de `C4`** *(gobierno de la condición · ceros de origen indeterminado · columnas de texto en agregaciones · referencias a rótulos · identidad motor↔derivado · cobertura de transmisión)*, cada una **con lo que NO detecta** |

### 10 · Grafo y persistencia — *Neo4j (`QTMP`, `CRDC`) · corpus Supabase*

| | |
|---|---|
| **se eleva** | `MISMA_FUENTE_QUE` y el `MDN` · el corpus normativo con huella |
| **se retira** | las afirmaciones de reuso **no reconstruibles** del grafo vivo *(`Q-M2-C2`)* |
| **se incorpora** | **el grafo de evidencia por documento** que produce la adquisición recursiva: cada salto añade nodos **sin perder la cadena de procedencia** |

### Lo que esta matriz hace y lo que no

**Hace:** poner sobre la mesa, **nivel por nivel**, qué de lo construido en meses **se conserva y sube
de nivel**, qué **se retira** y qué **se incorpora** — con el inventario real detrás de cada línea.

**No hace:** ejecutar nada · decidir el número de dominios · reparar los defectos de `C4` · tocar el
Excel. **Sigue vigente la regla: primero la anatomía, después el bisturí.**

## 5-trigies · **ALCANCE DE QUIRA 7, CERRADO** — y los dominios con nombres de administración pública

> ⛔ **Esta sección cierra la deriva de alcance. Lo que está fuera, está fuera, y no se reabre.**

### El objeto de QUIRA 7 — dicho por la dirección

> **La mira es el cumplimiento del PDOT —sus metas, objetivos e indicadores— y la INVERSIÓN del GAD
> que lo materializa. No el gasto corriente. No la gestión ejecutiva del Concejo.**

### Criterio de admisión — el filtro que cierra la puerta

Una realidad entra al ecosistema **sólo si cumple las dos condiciones**:

| | condición |
|---|---|
| **1 · pertinencia** | sirve al **cumplimiento del PDOT** o a la **inversión** que lo materializa |
| **2 · evidencia accesible** | existe **fuente oficial que QUIRA pueda adquirir**: DPE/Transparencia · CPCCS · SERCOP · web oficial del GAD |

**Si falla cualquiera de las dos, la realidad se declara FUERA DEL UNIVERSO OBSERVABLE.** Eso no es
una omisión: **es un resultado**, y es doctrina QUIRA declararlo *(la ausencia de evidencia es un
resultado de auditoría, nunca autorización para inferir)*.

### ⛔ Lo que queda FUERA, y por qué

| realidad | por qué queda fuera |
|---|---|
| **Gasto corriente** | el objeto es la **inversión** |
| **Ordenanzas, resoluciones y sesiones del Concejo · fiscalización y control político** | **no hay acceso a la fuente.** Del Concejo sólo interesa **su planificación** —PDOT, POA—, que ya vive en Planificación Estratégica |
| **Ingresos, recaudación y autonomía financiera** | fuera del objeto *(inversión, no estructura de ingresos)* |
| **Catastro · uso y ocupación del suelo · permisos y licencias · tránsito** | fuera del objeto y **sin fuente adquirible** |
| **Talento humano · bienes y patrimonio** | fuera del objeto |
| **Mancomunidades y coordinación intergubernamental** | fuera del objeto en esta versión |
| **Operación y tarifas de los servicios** | QUIRA observa **cobertura y acceso** como resultado del cumplimiento del plan, no la operación |

> **De las ocho «brechas» del inventario anterior, sólo una sobrevive al filtro: `Contratación
> Pública`** —porque es el mecanismo por el cual **la inversión se convierte en obra, bien o
> servicio**, tiene fuente accesible (SERCOP) y **ya está instrumentada en el motor**. El resto sale.
>
> **Y el `orgánico por procesos` entra como EVIDENCIA, no como dominio:** sirve para saber **qué
> dirección responde por cada meta**, y se adquiere por `T3` junto al PDOT, POA, PAC y presupuestos.

### Los dominios, con sus nombres — tomados del Nomenclátor donde sirven

*(Se acabaron las etiquetas `U1`…`U7`. Se usa el **Nomenclátor Canónico** existente donde el nombre
sigue siendo válido, y se cambia donde dejó de serlo.)*

| # | nombre | procedencia del nombre | contenido |
|---|---|---|---|
| **1** | **Planificación Estratégica** | ✅ del Nomenclátor | PDOT · POA · metas, objetivos e indicadores · hitos · **el núcleo del objeto de QUIRA 7** |
| **2** | **Inversión Pública Municipal** | 🔄 **cambia** *(era «Presupuesto & Financiamiento»)* | presupuesto **de inversión** codificado y devengado · sostenibilidad de la inversión · **sin gasto corriente** · **sin financiamiento externo** |
| **3** | **Contratación Pública** | ➕ **nuevo**, con material existente | PAC · procedimientos y adjudicaciones en SERCOP · cobertura del plan de contratación · **cómo la inversión se vuelve obra** |
| **4** | **Gobernanza del Mandato** | ✅ del Nomenclátor | plan de trabajo inscrito ↔ PDOT · congruencia promesa↔plan |
| **5** | **Transparencia** | ✅ del Nomenclátor | **cumplimiento** de la publicación obligatoria **y calidad** de la información que nutre a los demás |
| **6** | **Participación Ciudadana y Control Social** | 🔄 **fusión** *(d08 + d09)* | **sección A · Participación Ciudadana** · **sección B · Rendición de Cuentas** · evidencia del vínculo |
| **7** | **Cobertura de Servicios e Infraestructura** | ✅ del Nomenclátor | cobertura y acceso por parroquia · déficit · brecha urbano-rural **como resultado del plan** |
| **8** | **Desarrollo Económico Territorial** | ✅ del Nomenclátor | tejido productivo · empleo · cadenas de valor |
| **9** | **Sostenibilidad y Resiliencia Ambiental** | ✅ del Nomenclátor | integridad ecológica · riesgo biofísico · metas ambientales |
| **10** | **Grupos de Atención Prioritaria** | 🔄 **cambia** *(era «Inclusión, Equidad y Género»)* | **la función ejecutora del GAD**: unidad que opera, presupuesto, programas, cobertura · **la figura institucional es atributo, no identidad** |

### Lo que NO es dominio — con su nombre también

| nombre | naturaleza | procedencia |
|---|---|---|
| **Ecosistema Municipal** | **transversal** · perímetro: qué entidad produce cada observación | 🔄 era «Holding e Integración Municipal» |
| **Equidad y Género** | **transversal** · desagregación obligatoria en los demás dominios | 🔄 era parte de «Inclusión, Equidad y Género» |
| **Cumplimiento Institucional** | **transversal derivada** · síntesis (ICPI) | 🔄 era «Salud Institucional» |
| **GeoTwin** | **transversal** · espacialización | ✅ ya lo era |
| **Alertas Institucionales** | **vista derivada** · señales en los dominios **+ BRN** | 🔄 era d04 · **decisión de Javo ya ejecutada** |
| **QUIRA Cooperación** | **producto** | ➕ sale del mapa ontológico |
| **Adquisición recursiva** | **infraestructura** (`T1`·`T2`·`T3`) | ➕ nueva |

### Por qué esta lista sí cierra

**Diez dominios**, de los cuales **siete conservan su nombre del Nomenclátor**, **dos cambian de
nombre porque cambió su objeto** y **uno es nuevo con material ya existente en el motor**. Ningún
nombre inventado, ninguna etiqueta provisional, y **cada exclusión está escrita con su razón** — que
es lo que impide que la discusión vuelva a abrirse.

**Lo que sigue pendiente y es de la mesa:** los nombres definitivos de los dos que cambiaron, y si
`Contratación Pública` es dominio propio o sección de `Inversión Pública Municipal`.

## 5-untrigies · **LISTA FINAL** — el alcance es lo ya construido · **13 dominios → 8**

> ⛔ **REGLA DE ALCANCE, de la dirección:** **el alcance de QUIRA 7 es lo que ya teníamos construido
> en la versión anterior. NADA MÁS.** No se incorporan realidades nuevas: se **reorganiza, fusiona,
> reclasifica y eleva** lo existente.

### Dos rectificaciones de esta dirección técnica

| | rectificación |
|---|---|
| **1** | **`Contratación Pública` NO es dominio nuevo. RETIRADA.** El `PAC` vuelve a la sección de inversión y la publicación en `SERCOP` a la observancia contractual de **Transparencia** — **donde ya estaban**. Proponerla como dominio era **incorporar**, y el alcance no incorpora |
| **2** | **El `orgánico por procesos` NO es «evidencia de apoyo»: tenía misión propia y se conserva.** Su misión es la **eficiencia directiva** —aterrizar la eficiencia **por dirección y por técnicos**—, instrumentada en `H17_IED`, `H30_IED_POR_DIRECCIÓN`, `H02b_ORGÁNICO_CLASIFICADOR`, `SCHEMA_ORGANICO` y `H_ORGANICO_040_2025`. ⛔ **Eso NO se desmejora: se eleva con el dominio de inversión** |

### Los ocho dominios — todos provienen de los trece existentes

| # | dominio | de dónde viene | contenido |
|---|---|---|---|
| **1** | **Planificación Estratégica e Inversión Pública** *(nombre a ratificar)* | **fusión `d01`+`d02`** *(decisión de Javo)* | **Sección Planificación:** PDOT · POA · metas, objetivos, indicadores · hitos **· Sección Inversión:** presupuesto de inversión codificado y devengado · `PAC` · sostenibilidad · **eficiencia directiva por dirección y por técnicos (`IED`)** · **sin gasto corriente · sin financiamiento externo** |
| **2** | **Gobernanza del Mandato** | `d03` | plan de trabajo inscrito ↔ PDOT · congruencia promesa↔plan |
| **3** | **Transparencia** | `d07` | cumplimiento de la publicación obligatoria · **calidad** de la información que nutre a los demás · observancia contractual |
| **4** | **Participación Ciudadana y Control Social** | **fusión `d08`+`d09`** *(decisión de Javo)* | **Sección A** participación e incidencia · **Sección B** rendición de cuentas · evidencia del vínculo |
| **5** | **Cobertura de Servicios e Infraestructura** | `d10` | cobertura y acceso por parroquia · déficit · brecha urbano-rural |
| **6** | **Desarrollo Económico Territorial** | `d11` | tejido productivo · empleo · cadenas de valor |
| **7** | **Grupos de Atención Prioritaria** | `d12` *(reenfocado)* | la **función ejecutora** del GAD: unidad, presupuesto, programas, cobertura |
| **8** | **Sostenibilidad y Resiliencia Ambiental** | `d13` | integridad ecológica · riesgo biofísico · metas ambientales |

### Los cinco que dejan de ser dominio — y adónde van

| dejó de ser dominio | pasa a ser |
|---|---|
| `d04` **Alertas Institucionales** | **vista derivada** · señales dentro de los dominios **+ BRN** *(orden de Javo, ya ejecutada)* |
| `d05` **Holding e Integración Municipal** | **transversal** · Ecosistema Municipal (perímetro: qué entidad produce cada observación) |
| `d06` **Salud Institucional** | **transversal derivada** · Cumplimiento Institucional (`ICPI`) |
| parte de `d12` · **Equidad y Género** | **transversal** · desagregación obligatoria en los ocho dominios |
| **GeoTwin** | **transversal** *(ya lo era)* |

**Y fuera del mapa ontológico:** **QUIRA Cooperación** *(producto)* · la **adquisición** `T1`·`T2`·`T3`
*(infraestructura del dominio de Transparencia y los conectores existentes)*.

### La cuenta, para que no haya dudas

**13 − 5 = 8.** Fusión `d01`+`d02` *(−1)* · fusión `d08`+`d09` *(−1)* · `d04` a vista *(−1)* · `d05` a
transversal *(−1)* · `d06` a transversal *(−1)*.

> ✅ **Ninguna realidad nueva. Ningún dominio inventado. Todo sale de lo construido en meses.**
> **Lo único pendiente de la mesa: el nombre definitivo del dominio 1.**

## 5-duotrigies · **CIRUGÍA DE ELEVACIÓN, DOMINIO POR DOMINIO** — contra los artefactos que existen

> **Regla operativa:** *QUIRA 7 no amplía arbitrariamente su objeto. **Transforma y eleva el
> ecosistema QUIRA existente** para cumplir mejor su propósito original.*
> **conservar → elevar → potenciar → unificar → mover → recortar → eliminar → reconstruir**, siempre
> **sobre algo que ya existe**.

### 1 · Planificación Estratégica e Inversión Pública *(d01 + d02)*

| | |
|---|---|
| **lo que hay** | `enrich_planificacion.py` · `enrich_presupuesto.py` · `enrich_poa_multianio.py` · agentes `d01` y `d02` · `m_planificacion.py` · `m_presupuesto.py` · `p10_inversion.py` · `plan_render.py` · `presupuesto_render.py` · motor: `H04` `H05` `H05b_PAC` `H07_S5` `H07b` `H07c` `H11b` `H16b_IPE` `H17_IED` `H30_IED_POR_DIRECCIÓN` `H19_ICS_ISP` `H90` `H_HOLDING_CEDULAS` · BRN `I` y `IV` · SAT-0/II/III/IV |
| **conservar** | los dos agentes con su procedencia (`evidencia_sha` + `motor_sha`) · el enricher como motor real (Regla 1) · el `Ti` normalizado de `H07b` |
| **elevar** | **un dominio con dos secciones** · **régimen temporal declarado por sección** · el **corte viaja** con `absorcion_ti_pct` |
| **potenciar** | ⭐ **eficiencia directiva**: `H17_IED` + `H30_IED_POR_DIRECCIÓN` + `H02b_ORGÁNICO_CLASIFICADOR` + `SCHEMA_ORGANICO` + `H_ORGANICO_040_2025` → **por dirección y por técnicos. Su misión original se mantiene** |
| **unificar** | los tres *enrichers* → uno con secciones · `m_planificacion` + `m_presupuesto` → una superficie · `plan_render` + `presupuesto_render` |
| **mover** | **radar de fondos · elegibilidad · `H20c_IEF` · `H69_ELEGIBILIDAD_FONDOS` → QUIRA Cooperación** |
| **recortar / eliminar** | literales de corte y frases constantes *(«natural en el primer cuatrimestre» · «corte Abril 2026» · dictamen invariable)* · umbrales 70/50 y rama `<30` sin guarda · **el gemelo inerte `H19!B11`** |
| **reconstruir** | `Clasificación_Ti` con guarda o sobre el normalizado · **`SAT-IV` alimentada por el cociente estructural, no por `1 − Ti`** · cargar la `RO` de la familia `I` |

### 2 · Gobernanza del Mandato *(d03)*

| | |
|---|---|
| **lo que hay** | `enrich_mandato.py` · agente `d03` · `m_mandato.py` · `p8_metas.py` · `mandato_render.py` · `H03_S1_ELECTORAL_CNE` · `H63_S0_CNE_TRAZABILIDAD` · `H16_IFE` · BRN `III` |
| **conservar** | la trazabilidad plan de trabajo → PDOT y su render propio |
| **elevar** | **sujeto «autoridad electa» declarado** · cargar la `RO` de `III` |
| **potenciar** | la congruencia promesa↔plan **con su universo declarado** (las 66 promesas) |
| **recortar** | la cifra de fidelidad **escrita a mano** en `p8_metas:272` |
| **reconstruir** | — |

### 3 · Transparencia *(d07)* — **el más maduro del ecosistema**

| | |
|---|---|
| **lo que hay** | agente `d07` (`scoring.py`, `etapas.py`) · `p07_transparencia.py` · `H09_S7` `H70_BITACORA` `H18_ITAM` `H41_IOC` · `QTMP` en Neo4j · `CATALOGO_CANONICO_CD_D07` · `METODOLOGIA_D07` · **BRN `VII` cargada** · conector `dpe.py` |
| **conservar** | **todo el núcleo**: metodología aprobada con su cadena normativa ingerida, catálogo de CD y *scoring* |
| **elevar** | a **dominio propio con dos funciones**: cumplimiento **y** calidad de la información · su calificación opera como **gate de admisión** de lo que alimenta a los demás |
| **potenciar** | **`T3`**: adquisición primaria en la web del GAD (PDOT · orgánico · POA · PAC · presupuestos) · registro de **vía, versión y hash** · **la divergencia entre vías como observación** |
| **recortar** | cualquier resto de las cifras ya desmentidas por su propia metodología *(`1−IOC` como transparencia, valores pegados, promedios simulados)* |
| **reconstruir** | — |

### 4 · Participación Ciudadana y Control Social *(d08 + d09)*

| | |
|---|---|
| **lo que hay** | `enrich_participacion.py` · `enrich_rdc.py` · `enrich_rdc_docx.py` · `enrich_aportes.py` · agentes `d08` y `d09` · `m_participacion.py` · `m_rdc.py` · `p16_gobernanza.py` · `p17_rdc.py` · `participacion_render.py` · `H10` `H10b` `H10c` `H20b_IGP` `H31` `H34b_MFN` `H24b_SAT-V` · BRN `VIII` y `IX` |
| **conservar** | el `MFN` como **evaluación experta** · los aportes ciudadanos · el circuito CPCCS |
| **elevar** | **un dominio con secciones A/B/C** · **sujeto obligado declarado por sección** · cargar la `RO` de `IX` · **declarar la naturaleza experta del `MFN` al lector** |
| **potenciar** | la sección **C · evidencia del vínculo**: aporte → decisión → resultado |
| **unificar** | los cuatro *enrichers* → uno con secciones · `m_participacion` + `m_rdc` |
| **recortar** | notas de método retirado que sigan publicándose |
| **reconstruir** | ⛔ **`SAT-V`**: hoy *«sin datos»* y *«evaluado sin brecha»* colapsan en el mismo `0` · ⛔ **`H89`**: `IF_n` guardado como texto hace inerte la penalización. **Las dos deudas de `C4-P2`** |

### 5 · Cobertura de Servicios e Infraestructura *(d10)*

| | |
|---|---|
| **lo que hay** | `p10_territorio.py` · `H42_IET` · `H43_MOTOR_TERRITORIAL` · `SCHEMA_NBI` · `SCHEMA_TERRITORIOS` · `CAPA_TERRITORIAL_MONTECRISTI` · `POA_GEOREFERENCIADO` · ⛔ **sin agente · sin cadena BRN** |
| **conservar** | el `IET` y las capas territoriales |
| **elevar** | **crear su agente con el molde `ADR-053`** |
| **potenciar** | GeoTwin como su expresión natural |
| **reconstruir** | **su cadena normativa completa** |

### 6 · Desarrollo Económico Territorial *(d11)* — **el menos construido, y hay que decirlo**

| | |
|---|---|
| **lo que hay** | corpus económico del PDOT en Supabase · ⛔ **sin agente · sin página propia · sin cadena BRN** · el Nomenclátor ya lo marcaba *«En Construcción»* |
| **conservar** | el corpus |
| **elevar** | definir sus indicadores propios y su agente |
| **reconstruir** | **casi todo** — es el dominio con menos base real |

### 7 · Grupos de Atención Prioritaria *(d12, reenfocado)*

| | |
|---|---|
| **lo que hay** | `p19_genero.py` · `H16c_PSG` · `H04b_DIAGNÓSTICO_SOCIAL` · ⛔ **sin agente · sin cadena BRN** |
| **conservar** | el diagnóstico social |
| **elevar** | **reenfocar a la función ejecutora**: unidad que opera · presupuesto · programas · cobertura · **la figura institucional como atributo** |
| **mover** | **el `PSG` pasa a la transversal de Equidad y Género** — mide sesgo distributivo, no funcionamiento de la función |
| **reconstruir** | **su cadena normativa entera** *(la mayor carga del mapa)* **y su indicador madre**, que hoy no existe: el `PSG` era de la transversal |

### 8 · Sostenibilidad y Resiliencia Ambiental *(d13)*

| | |
|---|---|
| **lo que hay** | `H20_ICODS` · `KB_DIAGNOSTICO_PDOT` · `SCHEMA_RIESGOS` · ⛔ **sin agente · sin página · sin cadena BRN** |
| **conservar** | `ICODS` y el inventario biofísico |
| **elevar** | agente propio |
| **reconstruir** | **su cadena normativa** |

### Transversales, vista y producto — qué pasa con cada uno

| | acción |
|---|---|
| **Ecosistema Municipal** *(d05)* | **conservar** `H12d_ICPI_POR_ENTIDAD` · `H71_EP_ADSCRITAS` · `H72_EP_BASE_LEGAL` · `H19b` → **elevar a atributo obligatorio** de toda observación |
| **Cumplimiento Institucional** *(d06)* | **conservar** el `ICPI` y **su guarda temporal, que es el único gobierno probado** · **recortar** su condición de cajón · `m1_situacion` pasa a **síntesis derivada** |
| **Equidad y Género** | **recibe el `PSG`** · desagregación obligatoria en los ocho |
| **GeoTwin** | sin cambios: ya era transversal |
| **Alertas Institucionales** *(d04)* | **conservar** `H75_SAT_ENGINE` y las señales · **mover** cada señal a su dominio y **a la BRN** *(deuda medida en vivo: 6 de 10 sin cadena)* · `m2_alertas` queda como **vista** |
| **QUIRA Cooperación** | **recibe** radar de fondos, elegibilidad e `H20c_IEF` |

### El resumen honesto del trabajo real

| | dominios |
|---|---|
| ✅ **con agente, enricher, página y cadena** | Transparencia · *(parcialmente)* Planificación e Inversión · Mandato · Participación y Control Social |
| ⚠️ **con material, sin agente ni cadena** | Cobertura · Grupos de Atención Prioritaria · Ambiental |
| ⛔ **con base mínima** | Desarrollo Económico Territorial |

**Cuatro de los ocho dominios tienen mayor grado de desarrollo. Cuatro necesitan agente y cadena
normativa. Y hay tres reparaciones funcionales derivadas de `C4`.** **Ése es el trabajo — y es finito.**

#### Tres precisiones del colega a esta bajada *(acogidas)*

1. **Las tres reparaciones no tienen el mismo alcance.** `SAT-IV` arrastra la reconstrucción **de una
   regla** *(`1 − Ti` usado como participación estructural)*; `SAT-V` y `H89` son reconstrucciones
   **de mecanismos** detectados por `C4` *(colapso «sin datos = sin brecha» y fallo de lectura
   absorbido)*.
2. **«Mayor grado de desarrollo» ≠ «maquinaria gobernada».** Tener artefactos no equivale a tener
   gobierno canónico efectivo — es exactamente lo que `D0.1` y `C4` demostraron.
3. **Cobertura, Económico, Grupos Prioritarios y Ambiental NO son dominios nuevos.** Están dentro del
   alcance histórico de QUIRA y **se elevan desde su material existente**.

⚠️ **Y una distinción de nivel:** *«tres enrichers → uno»* y *«dos agentes → uno»* son **decisiones de
implementación, no ontológicas.** La ontología ya está fijada —`d01`+`d02` se fusionan—; la cirugía
técnica deberá demostrar **cómo** se materializa esa fusión **sin perder las dos secciones ni sus
regímenes temporales**.

## 5-tritrigies · **LAS SAT** — dónde viven, qué normativa las produce y cómo se procede

> **La dirección confesó la duda:** *¿las SAT van en cada dominio o en la BRN como estructura? Y si van
> en cada dominio, ¿hay que parametrizar como SAT gran parte de la normativa elevada a Supabase?*
> **La respuesta ya estaba diseñada en el canon. Sólo nunca se terminó de ejecutar.**

### ⚠️ Primero, una corrección de esta dirección — falsación 39

En cuatro secciones de este registro escribí **«8 de 9 señales sin cadena BRN»**. **El gate en vivo
dice otra cosa:** `check_sat_brn` (2026-09-17) → **4 de 10 con cadena, 6 huérfanas (60 %)**.

| SAT | dominio de origen | cadena |
|---|---|---|
| `SAT-0` | d01/d02 | ✅ `RO-I-001` y `RO-I-002` |
| `SAT-IV` | d02 | ✅ `RO-IV-001` |
| `SAT-V` | d09 | ✅ `RO-IX-001` |
| `SAT-IX` | d08 | ✅ `RO-VIII-003` |
| `SAT-I` · `SAT-II` · `SAT-III` · `SAT-VI` · `SAT-VII` · `SAT-VIII` | d03 · d02 · d02 · d08 · informacional · d10/d12 | ⛔ **ninguna RO** |

**Tomé una cifra documentada** —el propio docstring del gate conserva la medición histórica del 89 %—
**en lugar de correr el gate.** Es el mismo error que `C4` enseña a evitar: *presencia de una cifra en
un documento ≠ estado actual*. Las cuatro ocurrencias quedaron corregidas con la medición en vivo.

### La respuesta: la SAT no es «del dominio» NI «de la BRN» — tiene tres lugares, con tres papeles

`ADR-038 §1b` ya lo decidió: *«una CNO todavía es Derecho; una SAT ya es control»*, y entre ambas va
la **Regla Operativa**.

```
NORMA (corpus Supabase, con SHA)
   ↓
CNO  · la cadena normativa        → es DERECHO: no tiene umbral, ni SAT, ni motor
   ↓
RO   · variable · umbral · periodo · consecuencia     → es LÓGICA
   ↓ produce:
SAT  · sólo MIDE, consume la RO
   ↓ opera en
DOMINIO  · donde la señal se lee y se explica
   ↓ se consolida en
VISTA DE ALERTAS  · el panorama, no una fuente
```

> **La SAT NACE en la BRN** —declarada en el bloque `produce:` de su `RO`, con umbral, peso,
> justificación y frontera interpretativa— · **VIVE en el dominio** donde esa `RO` opera · **y se
> CONSOLIDA en la vista de Alertas.**
>
> **Su decisión de eliminar SAT como dominio y llevarla a cada cajón y a la BRN ya era la correcta.**
> Lo que falta no es arquitectura: son **seis `RO` que nunca se escribieron.**

**El molde ya existe y es bueno:** `RO-VIII-003` declara `SAT-IX` con métrica, **umbral 0,50 con su
justificación**, peso de severidad, medición 2026 con numerador y denominador, y **frontera
interpretativa** —*«no afirma desatención, afirma no-verificabilidad»*—. Las seis que faltan se
escriben igual.

### ¿Parametrizar como SAT gran parte de la normativa de Supabase? — **NO.** Y por qué

**La mayor parte del corpus es Derecho** —definiciones, competencias, procedimientos—. **Una norma sólo
produce una SAT si pasa tres preguntas:**

| | pregunta | si la respuesta es no |
|---|---|---|
| **1** | ¿impone al GAD una **obligación medible**? | es contexto: alimenta la `CNO`, no una señal |
| **2** | ¿tiene **umbral, plazo o condición verificable**? | es métrica: puede vivir en una `RO` sin producir SAT |
| **3** | ¿su incumplimiento es **anticipable con evidencia que QUIRA pueda adquirir**? | no puede ser señal preventiva — sería una alarma sin prueba |

**Sólo si pasa las tres:** `CNO` → `RO` con `produce:` → SAT.

**Por qué no parametrizar en masa — tres razones:**

- **Fatiga de alertas.** Cientos de señales equivalen a ninguna: nadie las lee, y la que importa se
  pierde entre las demás.
- **Saltaría el nivel de la `RO`.** Convertiría Derecho en control sin operacionalizarlo, que es
  exactamente lo que `ADR-038` prohíbe: sin `RO` no hay umbral justificado ni frontera interpretativa.
- **`C4` ya mostró el costo.** `SAT-IV` y `SAT-V` son señales cuya condición no gobernaba el veredicto.
  **Más señales sin `RO` son más de lo mismo, a escala.**

### Cómo se procede — finito y en orden

| paso | qué | alcance |
|---|---|---|
| **1** | **las 6 SAT huérfanas**: pasar cada una por las tres preguntas · si sobrevive, **escribirle su `RO` con `produce:`** con el molde de `RO-VIII-003` · si no, **retirarla** | **seis decisiones, no cientos** |
| **2** | **`SAT-IV` y `SAT-V`**: ya tienen `RO`, pero cargan los defectos de `C4` *(`1 − Ti`; «sin datos = 0»)* → **se corrigen dentro de su `RO`**, no en el Excel suelto | dos |
| **3** | **las 15 `RO` existentes**: revisar cuáles tienen umbral y **podrían** producir una señal que hoy no existe — **sólo si pasan las tres preguntas** | revisión acotada |
| ⛔ | **nunca al revés**: no se parte del corpus hacia las SAT | — |

**Con eso, el gate `check_sat_brn` —que hoy informa y no bloquea— puede pasar a modo estricto cuando
las huérfanas lleguen a cero**, tal como su propio diseño lo previó.

## 5-quattrigies · **LAS SEIS SAT HUÉRFANAS** — resultado del filtro, una por una

*(Trabajo autorizado por la dirección: «avancemos con las 6 SAT huérfanas». Cada una se leyó en el
motor —`SAT_Catalogo` y su hoja propia— y se contrastó contra los eslabones con huella de las 16
`CNO`. Filtro: **1** obligación medible · **2** umbral verificable · **3** evidencia adquirible · y
**norma con `SHA`** para poder escribir la `RO`.)*

### El hallazgo que ordena todo: casi ninguna base legal citada está encadenada

El `SAT_Catalogo` del motor cita una base legal para cada señal, **pero una cita en el Excel no es
una norma verificada**: la de `SAT-IV` («COOTAD Art. 192») ya estaba documentada como errónea en el
propio código. Contrastadas contra los eslabones con `SHA` de las 16 `CNO`:

| artículo citado | SAT | ¿eslabón con huella? |
|---|---|---|
| COPLAFIP 54 | `SAT-I` · `SAT-VII` | ⛔ **ninguno** |
| COPLAFIP 115 · Acuerdo MEF 067 | `SAT-II` | ⛔ **ninguno** |
| COPLAFIP 113 | `SAT-III` | ⛔ **ninguno** |
| COOTAD 249 | `SAT-VIII` | ⛔ **ninguno** |
| **COOTAD 238** | **`SAT-VI`** | ✅ **`CNO-VIII-005`** *(con LOPC 67 y LOPC 71)* |

### Las seis decisiones

| SAT | filtro | decisión propuesta |
|---|---|---|
| **`SAT-VI`** · Desvío Presupuesto Participativo | ✅ 1 · ✅ 2 · ⚠️ 3 *(hoy sin datos)* · ✅ norma | **SOBREVIVE · `RO` escrita y verificada** → `RO-VIII-004` *(ver abajo)* · **pendiente de ratificación** |
| **`SAT-III`** · Parálisis Presupuestaria | ✅ · ✅ · ✅ · ⛔ norma | **SOBREVIVE · BLOQUEADA** hasta verificar COPLAFIP 113 **y decidir cuál de sus dos definiciones rige** *(ver hallazgos)* |
| **`SAT-II`** · Reforma Significativa Tardía | ✅ · ✅ · ⚠️ *(adquirible desde la cédula: asignado inicial vs codificado)* · ⛔ norma | **SOBREVIVE · BLOQUEADA** hasta verificar COPLAFIP 115 y adquirir las reformas de la cédula |
| **`SAT-I`** · «Fragmentación Selectiva» | ✅ · ✅ · ✅ *(autoreporte SIGAD)* · ⛔ norma | **SOBREVIVE CON REFORMULACIÓN · BLOQUEADA**: el nombre **presume intención** —lenguaje acusatorio que el canon prohíbe—. Su frontera debe decir, como `SAT-IX`: *«no afirma manipulación; afirma cobertura insuficiente del reporte»* |
| **`SAT-VII`** · Vi Sináptico Pulso | ⛔ base *«referencial»* · **peso 0** · *«INFORMACIONAL»* | **SE RETIRA COMO SAT** → el `Vi` queda como **indicador** de Planificación *(ya es componente del ICPI)* |
| **`SAT-VIII`** · Equidad Territorial | ⛔ base *«referencial»* · **peso 0** · *«INFORMACIONAL»* | **SE RETIRA COMO SAT** → el `IET` queda como **indicador** de Cobertura y de la transversal de Equidad |

> **Una señal con peso 0 y base «referencial» no es una alerta: es un indicador con disfraz de
> alerta.** Retirarlas no pierde información — el `Vi` y el `IET` siguen existiendo donde pertenecen.

### Hallazgos colaterales, verificados en el motor

- **`SAT-III` tiene DOS definiciones que no coinciden.** El catálogo dice *«Ti < 60 % antes del Q4 o
  < 80 % al cierre»*; la hoja `H23` implementa *«5 o más metas con ejecución < 10 %»*. Antes de su
  `RO` hay que decidir cuál rige.
- **El mecanismo C de `C4` aparece dos veces más.** `SAT-III` lee `H07_S5!C7:C31`, que **no tiene
  datos por meta** → cuenta 0 metas → *«✅ Sin señal»*. `SAT-VI` publica *«✅ Sin señal SAT-VI — Sin
  datos PP»*, y `H75`, que busca el `✅`, la trata como **inactiva con peso 0**. **«No evaluable»
  vuelve a colapsar en «conforme».**
- **El diagnóstico de `SAT-I` afirma algo falso.** Su rama por defecto escribe *«Alta calificación
  sobre universo completo de metas»* para cualquier caso que no dispare la alerta — **incluido el
  actual, con `ICM` = 0,01 (1 %)**. Es el mecanismo A: un texto que no depende del valor.

### `SAT-VI` · la `RO` está lista — y aplicarla es un acto de autoridad

Se escribió `RO-VIII-004` con el molde de `RO-VIII-003`, derivada de `CNO-VIII-005`, y **con la lección
de `C4-P2` aplicada desde el nacimiento**: declara **`sin_datos` como estado propio** —*«NO es
sin_señal: no se computa como inactiva ni aporta 0 al riesgo; se reporta como NO EVALUABLE»*—. El
umbral (0,20) y el peso (0,05) se declaran **heredados del motor y con su justificación PENDIENTE**:
no se inventó un fundamento para el 20 %.

**Se aplicó, se verificó y SE RETIRÓ, por lo que ocurrió al aplicarla:**

| efecto | qué significa |
|---|---|
| ✅ `check_sat_brn` pasó a **5 de 10 con cadena** | la RO funciona |
| ✅ registro regenerado: **159 activos, 0 aristas rotas** | la cadena es reconstruible |
| ⚠️ **el sello humano del catálogo BRN CADUCÓ solo** | el catálogo llevaba **la validación de Javo del 2026-09-02** atada al hash del canon `f9fa18c6…`. Con la RO nueva el canon pasó a `b34a0467…` y el sistema escribió: *«el sello valida el canon f9fa… y el actual es b34a…: describe otra compilación»* |
| ⚠️ **dos cables trampa se dispararon** | `test_canon_derivado` y `test_d08_respeta_el_estado` vigilan que no bajen los CNO sin RO; bajaron de 7 a 6, y la prueba dice: *«si BAJÓ, hay que verificar que la RO nueva es canon real y no una regla fabricada»* |
| ~~⚠️ el compilado de la BRN quedó desfasado~~ | ⛔ **FALSADO (falsación 40):** `brn_compilador --verificar` dice *«DIVERGE — falta recompilar»* **también en el estado base, sin la RO nueva**. El compilado ya estaba desfasado — es el derivado congelado que `C3` encontró. **La RO no lo causó** |

> ⭐ **Precedente positivo para `D0.1`:** el catálogo de la BRN **ya tiene un acto de autoridad que
> funciona** — un sello humano atado al hash del canon, que **caduca solo** cuando el canon cambia.
> Es exactamente lo que `D0.1` no encontró para el Gold Master. **El patrón existe en casa.**

**Por eso la RO no queda aplicada:** caducar el sello de la dirección y bajar un cable trampa **son
actos que corresponden a la dirección**, no a esta dirección técnica. El repositorio quedó en su
estado anterior —158 activos, salud en verde, 646 pruebas pasando—.

**Cuando la dirección ratifique, se aplica en un solo paso:** RO → registro y grafo → catálogo BRN
→ compilado → **nuevo sello de Javo** → los dos cables trampa pasan de 7 a 6 **con la ratificación
citada como justificación**.

<details><summary><b>Texto completo de <code>RO-VIII-004</code> propuesta — listo para aplicar</b></summary>

```yaml
id: RO-VIII-004
authority:
  parent: CNO-VIII-005
  constitution_articles: [1, 9]
  type: NORMATIVA
version: "1.0"
dimension: ejecucion_presupuesto_participativo
deriva_de: CNO-VIII-005 v1.0
metrica: { nombre: Desvio_Ejecucion_PP, unidad: proporcion }
parametros: { umbral_activacion: 0.20, frecuencia: anual }
metodo:
  tipo: lectura_del_motor
  motor: "Gold Master · H24c_SAT-VI_DESVÍO_PP (lee H10b_S8b_PARTICIPATIVO) — el motor calcula, esta RO no recalcula (Regla 1)"
  variables:
    monto_aprobado:  "SUM(H10b!D13:D17) · lo priorizado y aprobado en el PP"
    monto_ejecutado: "H24c!B9 · hoy es un LITERAL 0, sin fuente — pendiente de cablear a la ejecución del GAD"
  estados:
    - { id: activa,     condicion: "hay datos y |ejecutado − aprobado| / aprobado > umbral" }
    - { id: sin_senal,  condicion: "hay datos y el desvío no supera el umbral" }
    - { id: sin_datos,  condicion: "no hay monto aprobado registrado",
        regla: "NO es sin_senal: no se computa como INACTIVA ni aporta 0 al riesgo — se reporta como NO EVALUABLE" }
consecuencia: "Observación de ejecución: lo aprobado en el PP con desvío superior al umbral requiere justificación documentada (COOTAD 238). Lenguaje de administración pública, nunca acusatorio. Sin datos → no evaluable, nunca conforme."
produce:
  - id: SAT-VI
    nombre: "Desvio Presupuesto Participativo"
    dimension_tgi: D4
    deriva_de: CNO-VIII-005               # COOTAD 238 · LOPC 67 · LOPC 71 · verificados con SHA
    metrica: "|pp_ejecutado − pp_aprobado| / pp_aprobado"
    umbral_activacion: 0.20
    justificacion_umbral: >-
      PENDIENTE DE RATIFICACIÓN. Heredado de SAT_Catalogo, que sólo dice «desvíos
      requieren justificación». No se inventa un fundamento para el 20 %.
    peso_severidad: 0.05
    tipo: ALERTA
    medicion_2026:
      estado: sin_datos
      evidencia: "H24c!B8 Hay_Datos_PP = NO · H10b sin montos registrados"
      lectura_admisible: "no evaluable — NO «sin desvío»"
    frontera_interpretativa: >-
      Con datos, acredita desvío entre lo aprobado y lo ejecutado; NO acredita la causa
      (puede haber reformas justificadas). Sin datos, NO acredita ni desvío ni
      cumplimiento: acredita que la evidencia no está disponible (Carta CAPA 0).
    refleja_en_gold_master: "SAT_Catalogo (fila SAT-VI) + H24c_SAT-VI + H75_SAT_ENGINE fila 8 — el estado sin_datos aún NO está reflejado"
opera_en: d08
estado: propuesta
validacion: { validada_por: null, fecha_validacion: null }
```

</details>

### Lo que queda pendiente de la dirección

1. **Ratificar `RO-VIII-004`** *(y con ella, re-sellar el catálogo BRN)*.
2. **Ratificar el retiro de `SAT-VII` y `SAT-VIII` como señales** *(pasan a indicadores)*.
3. **Decidir cuál definición de `SAT-III` rige** antes de escribir su RO.

**Y el siguiente paso técnico, que no necesita decisión:** verificar COPLAFIP 54, 113 y 115 en el
corpus y encadenarlos en una CNO — eso desbloquea `SAT-I`, `SAT-II` y `SAT-III`.

⚠️ *Nota de estado:* `tests/test_d07_autonomia.py::test_los_hallazgos_de_la_corrida_llevan_su_cadena`
**falla en el estado base, antes de cualquier cambio de hoy** — verificado corriendo la suite con y
sin la RO. **No lo causó este trabajo** y queda anotado para revisarlo aparte.

⚠️ *Corrección de forma:* el commit `4a68073` dejó **el encabezado de la sección 6 duplicado**. Error
de edición de esta dirección; corregido aquí.

## 5-quinquatrigies · **MATRIZ MAESTRA DE ELEVACIÓN DE QUIRA 7** — versión operativa

> **Lo que esta matriz impide:** que *«existe»* se lea como *«está bien»*. Cada artefacto se juzga en
> cinco estados independientes y recibe **una sola** acción de elevación.
>
> **Después de esta matriz empieza el código. No antes.**

### Principio SAT, congelado como regla de `REARQ`

```
NORMA → CNO → RO ──produce──► SAT ──opera_en──► DOMINIO → VISTA DE ALERTAS
                   └──────────────opera_en──────────────►┘
BRN: registra CNO↔RO · RO↔SAT · SAT↔DOMINIO · y verifica la coherencia de la cadena
```

⛔ **Nunca** `normativa completa → parametrización SAT → Supabase`. **La señal sólo existe cuando la
norma puede traducirse legítimamente en una condición observable y preventiva.**

### Leyenda

| columna | pregunta | valores |
|---|---|---|
| **E** · existente | ¿existe el artefacto? | ✅ verificado · ❓ declarado, no verificado en este corte |
| **V** · válido | ¿su contenido/método es defendible? | ✅ demostrado · ⛔ **defecto demostrado** (con su fuente) · ❓ **no evaluado** |
| **C** · canónico | ¿tiene autoridad en el estado canónico? | ✅ vigente o registrado · ⚠️ propuesta · ⛔ sin autoridad declarada · ❓ indeterminado *(motor: `D0.1`)* |
| **G** · gobernado | ¿su producción y consumo están controlados? | ✅ prueba o sello que lo protege · ⚠️ parcial · ⛔ nada lo protege |
| **acción** | una sola | **CONSERVAR · ELEVAR · POTENCIAR · UNIFICAR · MOVER · RECORTAR · RECONSTRUIR** |

⚠️ **La mayoría de las celdas `V` dicen «no evaluado», y eso es correcto:** `C4` examinó tres cortes,
no el ecosistema entero. **Rellenar `V` con ✅ por defecto sería repetir el error que esta matriz existe
para impedir.**

**Refinamiento del colega — «válido» no es booleano:** ✅ = **V · válido demostrado** · ❓ = **V? · no
evaluado** · ⛔ = **V− · invalidado, defecto demostrado**. Y en la columna `G`, **✓\*** significa
*«gobernado demostrado para ese mecanismo concreto»*, **no** para todo el artefacto que lo contiene
—el caso del sello del catálogo BRN—. **«No encontré un defecto» nunca se lee como «está validado».**

*(Fuentes de las celdas: vigencia leída de cada `YAML` de la BRN y de `brn_compilador --verificar` ·
autoridad leída de `registry/registry.yaml` · pruebas contadas en `tests/` · defectos de `C4-P0/P1/P2`
y de `§5-quattrigies`.)*

### 1 · Planificación Estratégica e Inversión Pública

| sección | capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|---|
| — | canon | ADN `d01` + `d02` | ✅ | ✅ | ✅ sellado | ⚠️ | **ELEVAR** a contrato semántico de una estructura |
| Planificación | BRN | `CNO-I-001` · `RO-I-001` · `RO-I-002` → `SAT-0` | ✅ | ❓ | ✅ vigentes | ⚠️ compilado desfasado *(preexistente)* | **CONSERVAR** |
| Planificación | motor | `H04` · `H05` · `H11b` · `H16b_IPE` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** |
| Planificación | enricher | `enrich_planificacion` · `enrich_poa_multianio` | ✅ | ❓ | ⛔ | ⚠️ | **UNIFICAR** |
| Planificación | agente | `d01` | ✅ | ❓ | ✅ | ✅ 2 pruebas | **ELEVAR** |
| Planificación | página | `m_planificacion` · `plan_render` | ✅ | ⛔ frase constante · rama `<30` sin guarda *(`C4-P1`)* | ⛔ | ⚠️ | **RECORTAR** literales |
| Inversión | BRN | `CNO-IV-001` · `RO-IV-001` → `SAT-IV` | ✅ | ⛔ `1 − Ti` como participación *(`C4-P1` C.2)* | ✅ vigentes | ✅ | **RECONSTRUIR** dentro de su RO |
| Inversión | motor | `H07_S5` (`Ti`) · `H07b` (`Ti_norm`) · `H07c` · `H90` · `H_HOLDING_CEDULAS` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** · `H07b` como lectura gobernante |
| Inversión | motor | `H19!B11` gemelo de SAT-IV | ✅ | ⛔ compara contra un encabezado *(`C4-P1` C.1)* | ❓ | ⛔ | **RECORTAR** |
| Inversión | motor | `H07_S5!B21` clasificación del `Ti` | ✅ | ⛔ escala anual sin guarda | ❓ | ⛔ | **RECONSTRUIR** |
| Inversión | motor | `H22` reformas · `H23` SAT-III | ✅ | ⛔ `H22!B8 = 0` literal · `H23` con **dos definiciones** | ❓ | ⛔ | **RECONSTRUIR** *(bloqueada: norma)* |
| Inversión | ⭐ eficiencia directiva | `H17_IED` · `H30_IED_POR_DIRECCIÓN` · `H02b_ORGÁNICO` · `SCHEMA_ORGANICO` · `H_ORGANICO_040_2025` | ✅ | ❓ | ❓ | ⛔ | **POTENCIAR** — **misión original intacta**: por dirección y por técnicos |
| Inversión | enricher | `enrich_presupuesto` | ✅ | ⛔ el ISP empareja valor 2025 con clasificación 2026 | ⛔ | ⚠️ | **RECONSTRUIR** esa lectura · luego **UNIFICAR** |
| Inversión | agente | `d02` | ✅ | ⛔ `absorcion_ti_pct` viaja sin corte | ✅ | ✅ 3 pruebas | **ELEVAR** |
| Inversión | página | `m_presupuesto` · `p10_inversion` · `presupuesto_render` | ✅ | ⛔ dictamen constante · 70/50 sin guarda | ⛔ | ⚠️ | **RECORTAR** y **UNIFICAR** |
| — | a producto | radar de fondos · `H20c_IEF` · `H69_ELEGIBILIDAD_FONDOS` | ✅ | ❓ | ⛔ | ⛔ | **MOVER** → QUIRA Cooperación |

### 2 · Gobernanza del Mandato

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| canon | ADN `d03` | ✅ | ✅ | ✅ | ⚠️ | **ELEVAR** · sujeto «autoridad electa» |
| BRN | `CNO-III-001` · `RO-III-001` | ✅ | ⚠️ su señal se llama `SAT-III-001` y **colisiona** con la `SAT-III` del motor | ✅ vigentes | ✅ | **RECONSTRUIR** el nombre de la señal |
| motor | `H03_S1_ELECTORAL_CNE` · `H63` · `H16_IFE` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** |
| enricher | `enrich_mandato` | ✅ | ❓ | ⛔ | ⚠️ | **CONSERVAR** |
| agente | `d03` | ✅ | ❓ | ✅ | ✅ 1 prueba | **ELEVAR** |
| página | `m_mandato` · `mandato_render` | ✅ | ❓ | ⛔ | ⚠️ | **CONSERVAR** |
| página | `p8_metas` | ✅ | ⛔ cifra escrita a mano *(línea 272)* | ⛔ | ⛔ | **RECORTAR** el literal |

### 3 · Transparencia *(dominio propio · la infraestructura de adquisición se comparte, el juicio se queda aquí)*

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| canon | ADN `d07` · `CATALOGO_CANONICO_CD_D07` · `METODOLOGIA_D07` *(ratificada 2026-08-07)* | ✅ | ✅ | ✅ | ⚠️ | **CONSERVAR** |
| BRN | `CNO-VII-001…004` · `RO-VII-001…005` | ✅ | ❓ | ✅ vigentes | ✅ | **CONSERVAR** |
| motor | `H09_S7` · `H70` · `H18_ITAM` · `H41_IOC` | ✅ | ⛔ cifras históricas desmentidas por su propia metodología *(`1−IOC` como transparencia · valor pegado · promedios simulados)* | ❓ | ⛔ | **RECORTAR** esas cifras |
| agente | `d07` (`scoring.py` · `etapas.py`) | ✅ | ❓ | ✅ | ⚠️ 2 pruebas, **una falla en el estado base** | **CONSERVAR** · revisar la prueba |
| adquisición | conector `dpe.py` | ✅ | ❓ | ⛔ | ⚠️ | **CONSERVAR** |
| adquisición | `T3` · documentos oficiales en la web del GAD | ❓ práctica declarada por la dirección · implementación no verificada | ❓ | ⛔ | ⛔ | **ELEVAR** con vía, versión y hash |
| página | `p07_transparencia` | ✅ | ❓ | ⛔ | ⚠️ | **ELEVAR** a sus dos funciones: cumplimiento y calidad |

### 4 · Participación Ciudadana y Control Social

| sección | capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|---|
| Participación | BRN | `CNO-VIII-000…007` · `RO-VIII-001…003` | ✅ | ❓ | ⚠️ **propuesta** · no compiladas | ⚠️ | **ELEVAR** por ratificación |
| Participación | BRN | `RO-VIII-004` → `SAT-VI` | ✅ lista *(embebida en `§5-quattrigies`)* | ✅ | ⚠️ pendiente de ratificación | — | **ELEVAR** al ratificarse |
| Participación | motor | `H10` · `H10b` · `H10c` · `H20b_IGP` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** |
| Participación | motor | `H24c_SAT-VI` | ✅ | ⛔ «sin datos» → «✅ sin señal» *(mecanismo C)* | ❓ | ⛔ | **RECONSTRUIR** con el estado `sin_datos` |
| Participación | enricher | `enrich_participacion` | ✅ | ❓ | ⛔ | ⚠️ | **UNIFICAR** |
| Participación | agente | `d08` | ✅ | ❓ | ✅ | ✅ 1 prueba | **ELEVAR** · sujeto por sección |
| Participación | página | `m_participacion` · `p16_gobernanza` · `participacion_render` | ✅ | ❓ | ⛔ | ⚠️ | **UNIFICAR** |
| Rendición | BRN | `CNO-IX-001` · `RO-IX-001` → `SAT-V` | ✅ | ⛔ colapso «sin datos = sin brecha» *(`C4-P2-A`)* · id heredado `SAT-IX-001` | ✅ vigentes | ✅ | **RECONSTRUIR** dentro de su RO |
| Rendición | motor | `H31` · `H24b_SAT-V` | ✅ | ⛔ *(`C4-P2-A`)* | ❓ | ⛔ | **RECONSTRUIR** |
| Rendición | motor | `H34b_MFN` | ✅ | ⛔ la fórmula declarada no reproduce los valores *(`C4-P2-C`)* | ❓ | ⛔ | **ELEVAR** declarando su naturaleza experta |
| Rendición | motor | `H89_TRUST_SCORE` | ✅ | ⛔ `IF_n` como texto → penalización inerte *(`C4-P2-B`)* | ❓ | ⛔ | **RECONSTRUIR** |
| Rendición | enricher | `enrich_rdc` · `enrich_rdc_docx` · `enrich_aportes` | ✅ | ❓ | ⛔ | ⚠️ | **UNIFICAR** |
| Rendición | agente | `d09` | ✅ | ❓ | ✅ | ✅ 1 prueba | **ELEVAR** |
| Rendición | página | `m_rdc` · `p17_rdc` | ✅ | ⛔ «coinciden con la evidencia verificada» no depende de la evidencia *(`C4-P2`)* | ⛔ | ⚠️ | **RECORTAR** esa afirmación · **ELEVAR** la naturaleza del índice |

### 5 · Cobertura de Servicios e Infraestructura *(alcance histórico · se eleva desde su material)*

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| canon | ADN `d10` *(plantilla madre del Diccionario)* | ✅ | ✅ | ✅ | ⚠️ | **CONSERVAR** |
| BRN | — | ⛔ | — | — | — | **RECONSTRUIR** su cadena normativa |
| motor | `H42_IET` · `H43` · `SCHEMA_NBI` · `SCHEMA_TERRITORIOS` · `CAPA_TERRITORIAL` · `POA_GEOREFERENCIADO` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** |
| agente | — | ⛔ | — | — | — | **RECONSTRUIR** con el molde `ADR-053` |
| página | `p10_territorio` | ✅ | ❓ | ⛔ | ⛔ sin pruebas | **ELEVAR** |
| señal | `SAT-VIII` | ✅ | ⛔ peso 0 · base referencial | ⛔ | ⛔ | **RECORTAR** como señal · el `IET` queda como indicador *(pendiente de ratificación)* |

### 6 · Desarrollo Económico Territorial *(alcance histórico · el de menor base)*

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| canon | ADN `d11` *(«en construcción»)* | ✅ | ⚠️ | ✅ | ⛔ | **ELEVAR** |
| datos | corpus económico del PDOT | ❓ declarado en el ADN, no verificado en este corte | ❓ | ❓ | ⛔ | **CONSERVAR** |
| BRN · agente · página · pruebas | — | ⛔ | — | — | — | **RECONSTRUIR** |

### 7 · Grupos de Atención Prioritaria *(función ejecutora del GAD)*

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| canon | ADN `d12` | ✅ | ⚠️ define el cajón por el `PSG`, no por la función | ✅ | ⚠️ | **RECONSTRUIR** su objeto |
| motor | `H04b_DIAGNÓSTICO_SOCIAL` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** |
| motor | `H16c_PSG` | ✅ | ❓ | ❓ | ⛔ | **MOVER** → transversal de Equidad y Género *(el `PSG` **no desaparece**: cambia de función)* |
| perímetro | entidad ejecutora (`ENTE-02` en Montecristi) | ✅ | ✅ | ❓ | ⛔ | **CONSERVAR** como **atributo**, no como identidad |
| BRN | — | ⛔ *(verificado)* | — | — | — | **RECONSTRUIR** — la mayor carga normativa del mapa |
| agente · pruebas | — | ⛔ | — | — | — | **RECONSTRUIR** |
| página | `p19_genero` | ✅ | ❓ | ⛔ | ⛔ | **RECONSTRUIR** sobre la función ejecutora |

### 8 · Sostenibilidad y Resiliencia Ambiental

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| canon | ADN `d13` | ✅ | ✅ | ✅ | ⚠️ | **CONSERVAR** |
| motor | `H20_ICODS` · `KB_DIAGNOSTICO_PDOT` · `SCHEMA_RIESGOS` | ✅ | ❓ | ❓ | ⛔ | **CONSERVAR** |
| BRN · agente · página · pruebas | — | ⛔ | — | — | — | **RECONSTRUIR** |

### Transversales, señales y derivados

| capa | artefacto | E | V | C | G | acción |
|---|---|---|---|---|---|---|
| síntesis | `H12!B33` ICPI · `H12!B34` guarda temporal | ✅ | ✅ **la guarda es el único gobierno temporal probado** *(`C4-P0`)* | ❓ `D0.1` | ⚠️ | **CONSERVAR** |
| síntesis | `m1_situacion` | ✅ | ⛔ conclusión constante · umbrales 50/75 sin guarda *(`C4-P0`)* | ⛔ | ⚠️ | **RECORTAR** · pasa a síntesis derivada |
| perímetro | `H12d_ICPI_POR_ENTIDAD` · `H71_EP_ADSCRITAS` · `H72` · `H19b` | ✅ | ❓ | ❓ | ⛔ | **ELEVAR** a atributo obligatorio de toda observación |
| señales | `H75_SAT_ENGINE` | ✅ | ⛔ trata «sin datos» con `✅` como inactiva *(`C4-P2`)* | ❓ | ⛔ | **RECONSTRUIR** el estado `sin_datos` |
| señales | `SAT_Catalogo` | ✅ | ⛔ bases legales citadas **no encadenadas** · la de `SAT-IV` errada | ❓ | ⛔ | **RECONSTRUIR** desde las RO |
| señales | **nombres de las SAT** | ✅ | ⛔ **dos espacios de nombres**: códigos del motor (`SAT-0…IX`) e ids de la BRN (`SAT-<familia>-00N`), con colisiones documentadas (`SAT-III-001` ≠ `SAT-III` · `SAT-IX-001` ≠ `SAT-IX`) | ❓ | ⛔ | **RECONSTRUIR** un solo espacio de nombres |
| vista | `m2_alertas` | ✅ | ⛔ la columna «Ejecución (%)» se alimenta del ISP *(`C4-P1`)* | ⛔ | ⚠️ | **RECORTAR** · queda como vista |
| derivados | `sat_gm` · `financiero` del snapshot | ✅ | ⛔ divergen del motor · productor no localizado *(`C3`)* | ⛔ | ⛔ | **RECONSTRUIR** con acto de promoción |
| derivados | `brn_config` · `brn_manifest` | ✅ | ⛔ **divergen en el estado base** | ⚠️ | ⚠️ | **RECONSTRUIR**: recompilar con acto gobernado |
| derivados | catálogo BRN (`brn_cno` en el snapshot) | ✅ | ✅ | ✅ **sellado por Javo (2026-09-02)** | ✓\* **el sello caduca solo** *(demostrado para ese mecanismo, no para toda la BRN)* | **CONSERVAR** — ⭐ **precedente para `D0.1`** |
| razonamiento | Sentinel `RC-7.3` | ✅ | ✅ **única guarda de comparabilidad fuera del ICPI** | ❓ | ⚠️ | **POTENCIAR** · propagar el patrón |

### Lo que la matriz dice, en cinco líneas

1. **Lo más sano:** Transparencia (canon, BRN vigente, metodología ratificada) y el catálogo BRN, que ya tiene un acto de autoridad que funciona.
2. **Lo más urgente:** las señales — dos espacios de nombres, bases legales no encadenadas, y el estado `sin_datos` colapsando en `H75`.
3. **Lo más frágil:** las **páginas**, que concentran casi todos los defectos demostrados y **ninguna tiene autoridad registrada**.
4. **Lo que no hay que tocar:** la eficiencia directiva (`IED` + orgánico) — se **potencia** con su misión intacta.
5. **El trabajo nuevo real:** cadena normativa y agente para Cobertura, Económico, Grupos Prioritarios y Ambiental.

**Precisiones del colega, acogidas:** el sello de la BRN es **precedente** para `D0.1`, **no prueba**
que ese mecanismo gobierne el Gold Master · `SAT-V` y `H89` son reparaciones de hallazgos distintos, no
equivalentes a `SAT-IV` · el `PSG` **no desaparece**: su función distributiva pasa a la transversal.

**Siguen pendientes de la dirección** las tres decisiones de `§5-quattrigies`: ratificar `RO-VIII-004`,
ratificar el retiro de `SAT-VII`/`SAT-VIII` como señales, y elegir la definición de `SAT-III`.

## 5-sexquatrigies · **REGISTRO DE IDENTIDAD DE SEÑALES** — propuesta, construida desde la evidencia

> **Corrección del colega, acogida:** *«sí al objetivo; no todavía a renombrar»*. Los dos espacios de
> nombres son un **defecto de identidad canónica**, y un defecto de identidad **no se arregla
> cambiando cadenas de texto**. Primero la identidad, después el nombre, después la propagación:
>
> `identidad canónica de la señal → nombre público → ID técnico único → equivalencias históricas`
>
> **Sin este registro, renombrar es maquillaje.**

### Tres problemas que ya no se mezclan

| | problema | pregunta | quién lo trabaja |
|---|---|---|---|
| **A** | **autoridad** | ¿qué estado tiene autoridad para ser considerado vigente? | `D0.1` |
| **B** | **propagación** | dado un estado autorizado, ¿qué consumidores fueron efectivamente regenerados y validados? | la cirugía de derivados |
| **C** | **identidad** | cuando dos capas usan nombres distintos, ¿hablan del mismo objeto? | **este registro** |

**Secuencia del registro** *(colega)*: `referencias existentes → equivalencias demostradas → colisiones
→ identidad propuesta → ratificación → canon → propagación`. **Nunca** `renombrar → esperar que todo
encaje`.

> **Y una regla de reparto que evita cargar a la dirección con lo técnico:** *no todo defecto descubierto
> es una decisión humana.* **Lo técnico se resuelve técnicamente; a la mesa sólo sube lo que exige
> autoridad normativa o canónica.**

### Cómo se levantó

Cada señal se buscó **en todos los lugares donde se la nombra hoy**: el catálogo del motor
(`SAT_Catalogo`) · el motor de riesgo (`H75_SAT_ENGINE`) · los campos `produce:`, `consume:` y
`equivalencia_heredada` de las 13 `RO` · el gate `check_sat_brn` · el bloque `sat_gm` del snapshot ·
y las vistas que las presentan.

### El registro — tabla 1 · identidad

| identidad actual *(código del motor)* | nombre público | alias heredados | productor RO | CNO | dominio QUIRA 7 | estado | estado canónico |
|---|---|---|---|---|---|---|---|
| **SAT-0** | Coherencia POA-PAC | `SAT-I-001` · `SAT-I-002` | **dos**: `RO-I-001` y `RO-I-002` | `CNO-I-001` | Planificación e Inversión | RO vigente | catálogo sellado `f9fa18c6` *(Javo · 2026-09-02)* |
| **SAT-I** | «Fragmentación Selectiva» *(nombre a reformular)* | — | ⛔ ninguno | ⛔ **COPLAFIP 54 EXCLUYE a los GAD** *(corpus)* · sin norma aplicable hallada | Planificación e Inversión | sin RO · **retiro propuesto** | ⛔ ninguno |
| **SAT-II** | Reforma Significativa Tardía | — | ⛔ ninguno | ⚠️ COPLAFIP 115 trata otro asunto · **candidata: COOTAD 255** *(corpus, `12077e724540`)* | Planificación e Inversión | sin RO · desbloqueada | ⛔ ninguno |
| **SAT-III** | Parálisis Presupuestaria | *«Sub-ejecución D3»* *(`sat_gm`)* | ⛔ ninguno | ⚠️ COPLAFIP 113 es definicional · **candidata: COPLAFIP 119** *(corpus, `8a5e811f8f8b`)*, aplicabilidad a GAD por contrastar con el COOTAD | Planificación e Inversión | sin RO · **dos definiciones** | ⛔ ninguno |
| **SAT-IV** | Alerta Fiscal COOTAD | `SAT-IV-001` · *«Brecha territorial IRS=79.7»* *(`sat_gm`)* | `RO-IV-001` | `CNO-IV-001` | Planificación e Inversión | RO vigente | catálogo sellado `f9fa18c6` |
| **SAT-V** | Brecha Compromiso CPCCS | `SAT-IX-001` · *«Densidad de trazabilidad insuficiente»* *(`sat_gm`)* | `RO-IX-001` | `CNO-IX-001` | Participación y Control Social | RO vigente | catálogo sellado `f9fa18c6` |
| **SAT-VI** | Desvío Presupuesto Participativo | — | ⚠️ `RO-VIII-004` *(escrita, pendiente de ratificación)* | `CNO-VIII-005` | Participación y Control Social | sin RO vigente | ⛔ ninguno |
| **SAT-VII** | Vi Sináptico Pulso | — | ⛔ ninguno | ⛔ cita COPLAFIP 54, que **excluye a los GAD** *(corpus)* | Planificación e Inversión | retiro como señal propuesto | ⛔ ninguno |
| **SAT-VIII** | Equidad Territorial | — | ⛔ ninguno | ⛔ cita COOTAD 249, que trata del **presupuesto de grupos de atención prioritaria**, no de equidad territorial *(corpus)* | Cobertura | retiro como señal propuesto | ⛔ ninguno |
| **SAT-IX** | Brecha de Atención Ciudadana | — | `RO-VIII-003` | `CNO-VIII-005` | Participación y Control Social | RO **propuesta** | catálogo sellado `f9fa18c6` *(como propuesta)* |
| **`SAT-III-001`** | — *(señal del mandato)* | — | ⛔ ninguno *(diseñada, no implementada)* | `CNO-III-001` *(vía `RO-III-001`)* | Gobernanza del Mandato | ✅ **identidad resuelta** · ⛔ **no implementada en el motor** | ? |

### El registro — tabla 2 · operación

*(El «contrato de evidencia» es el que **declara el propio motor** en `SAT_Catalogo`: fuente + variable.
Es lo que la señal dice necesitar, **no** una verificación de que esa evidencia llegue.)*

| identidad | contrato de evidencia *(declarado)* | estado sin datos, hoy | referencia en el motor | vista que la presenta |
|---|---|---|---|---|
| **SAT-0** | SERCOP · `pac_publicado` · `brecha_poa_pac` | ? no evaluado | `H21b!B19` → `H75` fila 2 | `p_ejecutivo` · `p12_cadena` · `p8_metas` |
| **SAT-I** | DPE · `icm_global` · `pct_metas_reportadas` | ⛔ el diagnóstico afirma *«alta calificación»* con `ICM` = 1 % | `H21!B15` → `H75` fila 3 | `p_ejecutivo` |
| **SAT-II** | DPE · `reformas_presupuestarias` · `fecha_reforma` | ⛔ `H22!B8 = 0` literal → *«✅ sin señal»* | `H22!B12` → `H75` fila 4 | `p_ejecutivo` · render de presupuesto *(por nombre)* |
| **SAT-III** | DPE · `ejecucion_porcentaje` · `ti_devengado` | ⛔ sin datos por meta → *«✅ sin señal»* | `H23!B13` → `H75` fila 5 | `p_ejecutivo` · render de presupuesto *(por nombre)* |
| **SAT-IV** | DPE · `inversion_porcentaje` · `gasto_corriente_pct` | ⛔ defecto de regla: `1 − Ti` *(`C4-P1`)* | `H24!B13` → `H75` fila 6 | `p_ejecutivo` · render de presupuesto *(por nombre)* |
| **SAT-V** | CPCCS · `rdc.componente_a.score` · `score_total` | ⛔ «sin datos» → brecha 0 → *«✅ sin señal»* *(`C4-P2-A`)* | `H24b!B17` → `H75` fila 7 | `p_ejecutivo` · `p16_gobernanza` · `m_rdc` *(su valor)* |
| **SAT-VI** | DPE · `pp_registrado` · `pp_ejecutado` | ⛔ *«✅ sin señal — sin datos»* → inactiva, peso 0 | `H24c!B14` → `H75` fila 8 | `p_ejecutivo` |
| **SAT-VII** | DPE · `vi_promedio_metas` | ⛔ **cuenta como ACTIVA con peso 0** en el conteo publicado | `H25_MMP!W38` → `H75` fila 9 | `p_ejecutivo` |
| **SAT-VIII** | DPE · `iet_desviacion` · inversión urbana y rural | ? no evaluado | `H42_IET` → `H75` fila 10 | `p_ejecutivo` |
| **SAT-IX** | BRN (`RO-VIII-003`) · `brecha_atencion_pct` | ⛔ **sin fila en `H75`: no entra al riesgo** · su RO mide 0,848 con umbral 0,50 | `SAT_Catalogo` fila 15 | ? **no localizada por código** en las vistas revisadas |
| **`SAT-III-001`** | ? | ? | ⛔ **no existe en el motor** | ? |

*(Universo de vistas revisado: `p_ejecutivo` · `p_command_center` · `p6_pulso` · `p8_metas` ·
`p12_cadena` · `p16_gobernanza` · `m2_alertas` · `m_rdc` · `presupuesto_render`. Una vista fuera de
este universo podría presentar `SAT-IX`: **no encontrado ≠ inexistente**.)*

### Seis hallazgos de identidad — verificados

| # | hallazgo | evidencia |
|---|---|---|
| **I1** | **`SAT-0` tiene dos RO productoras y dos ids heredados** | `RO-I-001` y `RO-I-002` declaran `produce: SAT-0` · `consume:` `SAT-I-001` y `SAT-I-002` |
| **I2** | **`SAT-I-001` es `SAT-0`, no `SAT-I`** | `equivalencia_heredada` en `RO-I-001` |
| **I3** | ✅ **`SAT-III-001` · IDENTIDAD RESUELTA TÉCNICAMENTE** *(entró como «no resuelta»; se resolvió en este mismo corte)*: es **la señal del dominio de mandato** según la convención de `ADR-038` —el id de la señal repite la familia de la RO que consume (`RO-IV-001 → SAT-IV-001`)—. **Fue diseñada y nunca implementada en el motor.** **No tiene relación con la `SAT-III` del motor**: la colisión es sólo nominal | `RO-III-001` (vigente, ratificada 2026-07-18): *«la señal del mandato lleva solo este ID (ADR-038 §118)»* · el diagrama de `ADR-038` fija la convención |
| **I4** | ⛔ **`SAT-IX` existe en el catálogo y en la BRN, pero no en el motor de riesgo** | `H75` cubre filas 2-10 (`SAT-0…VIII`) · `RIESGO_TOTAL = SUM(G2:G10)` · **no hay fila `SAT-IX`** |
| **I5** | ⛔ **el conteo publicado de alertas activas incluye una señal informacional** | `SAT_ACTIVAS_COUNT = COUNTIF(E2:E10,"ACTIVO") = 2` → `SAT-0` **y `SAT-VII`, que pesa 0** |
| **I6** | **tres sistemas de nombres, no dos — pero de naturaleza distinta** | códigos del motor · ids de la BRN (`consume:` y heredados) — **que es una migración a medias, no un sistema rival** *(ver I3)* · **y la semántica del derivado congelado `sat_gm`**, que describe tres señales con significados distintos *(problema de propagación, familia de `C3`)* |

### Lo que la evidencia sugiere — sin decidirlo

La BRN **ya eligió de hecho**: cada vez que una RO documenta una equivalencia, marca los ids
`SAT-<familia>-00N` como **`equivalencia_heredada`** y usa **el código del motor** en `produce:`. Es
decir, **el canon ya trata los códigos del motor como identidad y los ids BRN como historia.** La única
excepción es `SAT-III-001`, que no tiene equivalencia porque **no se identificó a qué señal real
corresponde**.

> **Esto es insumo, no decisión.** El esquema definitivo —`signal_id` y nombre público— **es de la mesa.**

### ⚠️ `SAT-III-001` NO era una cuarta decisión de la dirección *(corrección del colega)* — y ya se resolvió técnicamente

Entró al registro como **IDENTIDAD NO RESUELTA · REFERENTE NO DETERMINADO** y se trató como problema
técnico. **Se resolvió en el mismo corte:**

- `ADR-038` fijó una **convención de la BRN**: la señal que consume una RO lleva el id de la familia de
  esa RO (`RO-IV-001 → SAT-IV-001`). **`SAT-III-001` es la señal del dominio de mandato**, no la
  `SAT-III` del motor.
- **Se diseñó y nunca se implementó en el motor.**
- Luego `OBS-022` (2026-07-29) introdujo `produce:` con **los códigos del motor**, y cada RO migrada
  guardó su id anterior como `equivalencia_heredada`. **`RO-III-001` no se migró** porque no existía
  señal del motor con la cual emparejarla.

> **Conclusión técnica:** el «segundo sistema de nombres» **no es desorden: es una migración que quedó
> a medias**. La convención de familia de `ADR-038` se reemplazó por los códigos del motor, y las RO
> migradas lo documentan. **Falta completarla** — no inventar una tercera.

**Lo único que sí podría subir a la mesa** es otra pregunta, distinta de la identidad: *¿se implementa
una señal del mandato en el motor?* Eso crearía una señal nueva —umbral, peso, evidencia— y **exige
autoridad**. **No se agrega a las pendientes**: queda como opción para cuando la dirección la quiera
abrir. **Las decisiones pendientes siguen siendo tres.**

### ⚠️ Cautela: defectos concretos, no «arquitectura rota»

Que `SAT-VII` cuente como activa con peso 0, o que `SAT-IX` no tenga fila en `H75`, son **defectos
concretos de representación y de consumo**. Se **clasifican** en la matriz y **se reparan** después; no
autorizan la conclusión de que la arquitectura de señales esté rota — **la arquitectura `CNO → RO → SAT`
es sana: lo que falla son instancias de ella.**

### Lo que este registro da, y no había antes

> **Un inventario cerrado de qué señales cree tener QUIRA, dónde las produce, dónde las consume y si
> todos esos lugares hablan del mismo objeto.** Eso es una pieza de QUIRA 7, no un parche del QUIRA
> anterior.

### Lo que NO se hizo, a propósito

- **Ningún id se renombró.** Ningún texto se cambió.
- **El registro no se escribió en `docs/brn/`:** cualquier archivo nuevo ahí **cambia el hash del canon y
  caduca el sello de la dirección** — lo mismo que ocurrió con `RO-VIII-004`. Materializarlo como archivo
  canónico **requiere que la dirección lo ratifique y vuelva a sellar**.
- **Las tres decisiones pendientes siguen sin tocarse.**

### El orden que queda

```
Registro de identidad (esta propuesta)
   → ✅ SAT-III-001 resuelta técnicamente (señal del mandato, diseñada y no implementada)
   → la mesa fija el esquema: signal_id · nombre público
   → se completa la migración produce:/equivalencia_heredada que quedó a medias
   → se materializa como archivo canónico + nuevo sello de la dirección
   → se propaga: produce/consume de las RO · H75 (incluida SAT-IX) · SAT_Catalogo · check_sat_brn · vistas
   → y SÓLO ENTONCES se toca un nombre
```

## 5-septquatrigies · **COPLAFIP 54 · 113 · 115 VERIFICADOS EN EL CORPUS** — ninguno dice lo que el catálogo afirma

> **Trabajo autorizado por la dirección:** *«el siguiente paso técnico sin tocar canon —verificar COPLAFIP
> 54, 113 y 115 en el corpus— es el correcto»*.
>
> **Método:** sesión **de sólo lectura** sobre `public.normativa_corpus` (Supabase), con la misma
> resolución de credenciales que usa `scripts/brn_cno.py` — **ni la URI ni ningún secreto se
> imprimieron**. Se leyó el **texto completo** de cada artículo, no sólo su comienzo. **No se tocó el
> canon, ni la BRN, ni el Gold Master.**

### Los tres artículos existen — y ninguno sostiene la señal que lo cita

| artículo · huella | lo que `SAT_Catalogo` afirma que dice | lo que el texto dice | veredicto |
|---|---|---|---|
| **COPLAFIP 54** · `377f7da7ac2e` | *«las entidades deben reportar avances de todas las metas del plan operativo en el SIGAD»* *(base de `SAT-I` y `SAT-VII`)* | *«Planes institucionales.- Las instituciones sujetas al ámbito de este código, **excluyendo los Gobiernos Autónomos Descentralizados**, reportarán a la Secretaría Nacional de Planificación…»* | ⛔ **EXCLUYE EXPRESAMENTE A LOS GAD** |
| **COPLAFIP 113** · `70c235f494c6` | *«obliga a la evaluación periódica… las entidades deben alcanzar metas de ejecución por período»* *(base de `SAT-III`)* | define **qué es** la fase de ejecución presupuestaria | ⛔ **definicional**: no contiene la obligación con umbral atribuida |
| **COPLAFIP 115** · `09bc593d0270` | *«las reformas presupuestarias deben justificarse y registrarse en eSIGEF»* *(base de `SAT-II`)* | regula la **certificación presupuestaria** | ⛔ **trata otro asunto** |

> **La cita en el Excel no era norma verificada — y ahora está demostrado con el texto.** Es la misma
> lección de siempre, en su forma más pura: *que un artículo aparezca citado no prueba que diga lo que se
> le atribuye.*

### Lo que sí existe en el corpus — candidatos, leídos completos

| señal | norma candidata · huella | qué establece | qué NO establece |
|---|---|---|---|
| **`SAT-II`** | **COOTAD 255** · `12077e724540` — *«Reforma presupuestaria»* | **propia del régimen de los GAD**: una vez aprobado, el presupuesto sólo se reforma por **traspasos, suplementos y reducciones de créditos**, conforme a las secciones siguientes | el umbral *«> 5 % después del 30 de junio»*: **es lógica de la RO** y necesita justificación propia |
| **`SAT-III`** | **COPLAFIP 119** · `8a5e811f8f8b` — *«Seguimiento y evaluación de la ejecución presupuestaria»* | **obligación**: la evaluación física y financiera es **responsabilidad del titular**, **periódica**, y sus informes **se difunden a la ciudadanía** | ⚠️ **aplicabilidad a los GAD por confirmar**: el Art. 4 somete al código a las entidades del Art. 225 de la Constitución, **pero respeta su autonomía presupuestaria**, y el régimen presupuestario de los GAD vive en el COOTAD. **Contrastar antes de fundar la CNO** |
| **`SAT-I`** | ⛔ **ninguna aplicable hallada** *(universo: COPLAFIP y COOTAD, patrones de reporte de metas y sistemas de información)* | COOTAD 195 menciona el cumplimiento de metas **como criterio del modelo de transferencias** — **no es una obligación de reporte** | — |

### Cómo cambia el estado de las tres bloqueadas

| señal | antes | ahora |
|---|---|---|
| **`SAT-II`** | bloqueada por norma | ✅ **desbloqueada**: tiene base candidata específica del GAD. Falta su CNO, su RO con umbral justificado, y la evidencia de reformas desde la cédula |
| **`SAT-III`** | bloqueada por norma | ⚠️ **desbloqueable**: base candidata con obligación real, **pendiente de contrastar con el COOTAD** — y sigue pendiente **qué definición rige** *(decisión de la dirección)* |
| **`SAT-I`** | bloqueada por norma | ⛔ **sin base normativa aplicable**: la que citaba excluye a los GAD y no apareció otra → **propuesta de retiro como señal** |

**Las decisiones pendientes siguen siendo tres.** El retiro de `SAT-I` **no abre una cuarta**: se suma a
la decisión 2, que pasa a ser *«retirar como señales `SAT-I`, `SAT-VII` y `SAT-VIII`»*.

### Dos hallazgos colaterales, verificados

- **El corpus confirma que la base de `SAT-IV` en el catálogo es errónea:** COOTAD 192 es *«Monto total a
  transferir»* (21 %), exactamente como el código del proyecto ya lo había advertido. La RO de `SAT-IV` se
  funda correctamente en el COOTAD reformado (Art. 198.1 y su Disposición Transitoria).
- ⭐ **Las leyes especiales de los Grupos de Atención Prioritaria YA ESTÁN EN EL CORPUS**, con nombre
  confirmado en `norma_nombre`: **Ley Orgánica de Discapacidades** · **Ley Orgánica de las Personas
  Adultas Mayores** · **Código de la Niñez y Adolescencia** · **Convención sobre los Derechos del Niño**
  · **CEDAW** · **Ley Orgánica de Movilidad Humana** · **Convención Americana sobre Derechos Humanos**.
  **Eso rebaja el costo del dominio de Grupos de Atención Prioritaria:** su trabajo normativo es
  **encadenar** (CNO → RO), **no ingerir**.

⚠️ **Falsación evitada (41):** una sigla del corpus la había interpretado de memoria de forma equivocada.
Se confirmó contra `norma_nombre` **antes** de escribirla — `LOIEME` es la Ley Orgánica para Impulsar la
Economía de las Mujeres Emprendedoras. **Ninguna sigla se desarrolló sin verificarla.**

## 5-octoquatrigies · **COOTAD 249 · CONSTITUCIÓN 35** — el ancla normativa de Grupos de Atención Prioritaria *(aporte de la dirección)*

> **Aporte de Javo:** *«el 249 del COOTAD habla sobre el presupuesto de los grupos de atención
> prioritaria; el 35 de la Constitución, de quiénes son esos grupos»*. **Verificado en el corpus, con el
> mismo método de sólo lectura. Ambos confirmados.**

| artículo · huella | qué establece |
|---|---|
| **Constitución 35** · `fba71e80b2f5` | **quiénes son**: personas adultas mayores · niñas, niños y adolescentes · mujeres embarazadas · personas con discapacidad · personas privadas de libertad · quienes adolezcan de enfermedades catastróficas o de alta complejidad · y, con la misma atención prioritaria, personas en situación de riesgo, víctimas de violencia doméstica y sexual, maltrato infantil y desastres · con especial protección ante la **doble vulnerabilidad** |
| **COOTAD 249** · `c0c0fce0f126` | *«**No se aprobará el presupuesto** del gobierno autónomo descentralizado si en el mismo no se asigna, **por lo menos, el diez por ciento (10 %) de sus ingresos no tributarios** para el financiamiento de la planificación y ejecución de programas sociales para la atención a grupos de atención prioritaria»* — y remite expresamente a la Constitución, Art. 35 |

### Consecuencia 1 · el dominio de Grupos de Atención Prioritaria ya tiene ancla

Antes: *«sin ninguna cadena normativa — la mayor carga del mapa»*. Ahora:

```
Constitución 35  →  quiénes son (sujeto de derechos)
       ↓  (concordancia expresa)
COOTAD 249       →  obligación presupuestaria del GAD, con UMBRAL ESCRITO EN LA LEY
       ↓
leyes especiales ya en el corpus: Discapacidades · Adultos Mayores · Niñez y Adolescencia ·
Movilidad Humana · CDN · CEDAW
```

**Todavía no hay `CNO`** —encadenarla cambia el canon y **exige ratificación y nuevo sello**—, pero el
dominio **dejó de partir de cero**: la cadena está visible y cada eslabón ya existe con huella.

### Consecuencia 2 · COOTAD 249 es la medida natural de la función ejecutora

El dominio se redefinió como **la función ejecutora del GAD hacia los grupos prioritarios** —qué unidad
opera, **con qué presupuesto**, qué programas—. **COOTAD 249 mide exactamente eso**, y pasa el filtro de
las tres preguntas mejor que cualquier otra señal revisada:

| | pregunta | COOTAD 249 |
|---|---|---|
| **1** | ¿obligación medible? | ✅ asignar a programas sociales para grupos prioritarios |
| **2** | ¿umbral verificable? | ✅ **10 % de los ingresos no tributarios — escrito en la ley, no inventado** |
| **3** | ¿evidencia adquirible? | ⚠️ el **presupuesto aprobado del GAD**: la asignación a esos programas **y** el agregado de ingresos no tributarios. **Disponibilidad en el motor: no verificada** |

> **Es el candidato natural a indicador madre del dominio** —y, si la dirección lo quiere, a su señal—.
> Es el único caso del mapa en que **el umbral no necesita justificación propia**: lo fija la ley, y la
> consecuencia también (*«no se aprobará el presupuesto»*).
>
> ⛔ **Precisión del colega: COOTAD 249 es un ancla normativa VERIFICADA del dominio; NO es
> automáticamente un nuevo SAT ni un indicador madre canonizado.** Encontrar una norma y convertirla
> de inmediato en lógica de motor sería repetir el error que se está auditando. El camino es:
> `CNO → análisis de la obligación → RO → evidencia disponible → indicador o señal, si corresponde →
> decisión de la mesa → canon`. **No antes.**
>
> ⚠️ **Precisión de alcance:** medirlo requiere el **agregado de ingresos no tributarios** como
> **denominador**. Eso **no reabre** «ingresos y recaudación» como dominio —que quedó fuera—: es un solo
> dato del presupuesto aprobado, usado para verificar una obligación que sí está dentro del alcance.

### Consecuencia 3 · la base de `SAT-VIII` en el catálogo también era errónea

`SAT_Catalogo` cita COOTAD 249 como fundamento de *«Equidad Territorial»* (inversión urbana frente a
rural). **COOTAD 249 no trata de equidad territorial: trata del presupuesto de los grupos de atención
prioritaria.** Con esto, el recuento verificado del catálogo queda así:

| estado de la cita | señales |
|---|---|
| ✅ **encadenada correctamente** en una CNO | `SAT-0` · `SAT-VI` · `SAT-IX` |
| ⛔ **el artículo citado no dice lo atribuido** *(verificado en el corpus)* | `SAT-I` y `SAT-VII` *(COPLAFIP 54 excluye a los GAD)* · `SAT-II` *(115: certificación)* · `SAT-III` *(113: definicional)* · `SAT-IV` *(COOTAD 192: monto a transferir)* · `SAT-VIII` *(COOTAD 249: grupos prioritarios)* |
| ? **no verificada en este corte** | `SAT-V` *(cita COOTAD 302)* |

> **Seis de las diez señales citan un artículo que no dice lo que el catálogo le atribuye.** No es un
> descuido aislado: es la prueba de que **la base legal escrita en el Excel nunca pasó por la BRN**. Y es,
> exactamente, el motivo por el que `ADR-038` exige que la señal nazca de una RO fundada en una CNO con
> huella.

**Nada del canon se tocó.** Las decisiones pendientes siguen siendo tres. **Encadenar COOTAD 249 y la
Constitución 35 en una CNO**, y decidir si 249 se convierte en indicador madre o en señal del dominio,
**son pasos para cuando la dirección los abra** — la evidencia ya está lista.

## 5-novoquatrigies · **CIERRE DE LA VERIFICACIÓN NORMATIVA** — criterio de reconstrucción y el paso D resuelto

### El problema que la verificación reveló — más profundo que «seis citas equivocadas»

El catálogo SAT **mezcló tres cosas que QUIRA 7 debe separar**:

`norma que realmente obliga  →  regla operativa que interpreta esa obligación  →  señal que vigila su incumplimiento`

Y conecta con `D0.1`: **tener una referencia —incluso con huella— no significa que esa referencia
gobierne semánticamente la afirmación.** `COOTAD 238` había mostrado una cara del problema *(la cadena
puede estar formalmente trazada)*; ahora aparece la complementaria: **una referencia puede existir en el
catálogo, ser formalmente localizable, y ser jurídicamente ajena a lo que la señal afirma.**

### Criterio de reconstrucción de `REARQ` *(colega — criterio de trabajo, NO doctrina)*

> **Una referencia normativa no acredita una señal. La señal sólo puede considerarse normativamente
> sustentada cuando puede reconstruirse la cadena `CNO → RO → condición verificable → evidencia → señal`
> sin alterar el significado de la norma durante el tránsito.**

Es la regla de `C4` aplicada a la norma: *no basta con que la propiedad exista en el destino; hay que
comprobar que sigue gobernando lo que el destino puede afirmar.*

**Y su contrapartida, para no exigir lo imposible:** *la norma puede fundamentar la obligación sin
contener el umbral que la RO usa para generar una señal preventiva.* **Es legítimo si la RO declara y
justifica explícitamente de dónde sale el parámetro.** No se exige que cada porcentaje aparezca en la
CNO; se exige que la separación sea **explícita y trazable**.

### Paso D · COPLAFIP 119 frente al régimen del COOTAD — **resuelto por lectura**

| artículo · huella | lo que establece |
|---|---|
| **COPLAFIP 96** · `427f23a66e7c` | el ciclo presupuestario —con sus etapas, **incluida «Evaluación y seguimiento presupuestario»**— *«es de cumplimiento obligatorio para **todas las entidades y organismos del sector público**»*. Lo que es **sólo referencial para los GAD** son **los lineamientos** del ente rector, **no la obligación** |
| **COOTAD 168** · `919882337173` | en el régimen propio del GAD, *«toda la información sobre el proceso de programación, formulación, aprobación, ejecución y **evaluación** del presupuesto será pública y se difundirá permanentemente… por la página web institucional»* · y **los ejecutivos de los GAD remitirán trimestralmente sus cédulas presupuestarias y balances financieros** al ente rector de las finanzas públicas y al de la planificación nacional |

> ✅ **Conclusión: COPLAFIP 119 SÍ aplica a los GAD**, por la vía del Art. 96 —que hace obligatorio el
> ciclo completo para todo el sector público— y con el respaldo del régimen propio (COOTAD 168). **A
> diferencia del Art. 54, nada en estos textos excluye a los GAD.**

⭐ **Y COOTAD 168 da algo más de lo que se buscaba:** obliga al GAD a **publicar** permanentemente la
información presupuestaria en su web y a **remitir trimestralmente sus cédulas** al ente rector.
~~Es la base legal de la evidencia que QUIRA adquiere.~~ ⚠️ **Corregido por la dirección
(falsación 42, ver `§5-quinquagies`):** la cadencia de la evidencia que QUIRA adquiere es **MENSUAL** y
viene de la **LOTAIP**; la remisión trimestral de COOTAD 168 es **otro canal** —hacia el ente rector, no
hacia la ciudadanía—. *(Precisión: nada de esto crea un dominio ni una funcionalidad nueva.)*

### Estado final de las señales tras la verificación

| señal | base normativa | estado |
|---|---|---|
| **`SAT-II`** | **COOTAD 255** *(reforma presupuestaria del GAD)* | **CNO posible: sí · RO posible: sí**, justificando su parámetro · ⛔ **el umbral de «> 5 % después de junio» NO está demostrado como exigencia legal** — *«COOTAD 255 existe» no es «SAT-II está validada»* |
| **`SAT-III`** | **COPLAFIP 96 + 119**, con **COOTAD 168** | **obligación de evaluar: sustentada para los GAD** · el umbral es lógica de RO y **debe declararse y justificarse** · sigue pendiente **qué definición rige** *(decisión 3)* |
| **`SAT-I` · `SAT-VII` · `SAT-VIII`** | ⛔ sin obligación aplicable hallada | **la pregunta para la mesa NO es *«¿qué artículo le ponemos para salvarlas?»***, sino ***«¿tienen realmente una obligación normativa aplicable que justifique su existencia como señales?»*** — **para no fabricar una base legal retrospectivamente** *(decisión 2)* |

### El registro de señales necesita siete capas, no una

| capa | pregunta |
|---|---|
| **identidad** | ¿qué señal es ésta? |
| **normativa** | ¿qué obligación la origina? |
| **operativa** | ¿qué regla transforma esa obligación en condición verificable? |
| **evidencia** | ¿qué dato permite comprobarla? |
| **motor** | ¿dónde se calcula? |
| **producto** | ¿dónde se consume? |
| **estado** | ¿vigente, propuesta, retirada o no implementada? |

*(Así `SAT-III-001` deja de confundirse con la `SAT-III` del motor: una es legado de la familia del
mandato, diseñada y no implementada; la otra es la señal presupuestaria de parálisis. **Eso es problema C,
identidad — no un problema normativo.**)*

### ⛔ Lo que esta verificación NO hace — escrito para que no se vuelva a abrir

**No amplía QUIRA.** Los grupos prioritarios **no crean un noveno dominio** · COOTAD 249 **no crea un
dominio financiero** · SERCOP **no crea contratación como dominio** · las SAT **no crean dominios** · las
normas halladas **no crean funcionalidades nuevas**. **No toca el canon. No crea una cuarta decisión.**

**El orden que queda:** **A** verificación normativa → ✅ **cerrada** · **B** resultados como evidencia de
`REARQ` → ✅ **registrados** · **C** tres decisiones pendientes → **intactas** · **D** COPLAFIP 119 frente
al COOTAD → ✅ **resuelto** · **E** → **incorporar estos resultados a la Matriz Maestra de Elevación**
sobre los ocho dominios fijados.

## 5-quinquagies · **LA CADENCIA ES MENSUAL, Y LA FIJA LA LOTAIP** *(corrección de la dirección)*

> **Javo:** *«la LOTAIP obliga a que la publicación de la información del GAD sea mensualizada»*.
> **Verificado — en el canon vigente y en el corpus.**

### ⚠️ Falsación 42, mía

Escribí que COOTAD 168 era *«la base legal de la evidencia que QUIRA adquiere»*. **Era incompleto y
confundía dos canales:**

| canal | norma | cadencia | destinatario | ¿es la fuente de QUIRA? |
|---|---|---|---|---|
| **transparencia activa** | **LOTAIP 19** y **LOTAIP 24** | **mensual** | **la ciudadanía**, por portal web | ✅ **sí** — es lo que QUIRA adquiere |
| remisión institucional | COOTAD 168 | trimestral | el ente rector de finanzas y el de planificación | ⛔ no — es un canal entre instituciones |

### Lo que dicen los artículos — y ya estaban en el canon

| artículo · huella | qué establece | ¿encadenado? |
|---|---|---|
| **LOTAIP 19** · `810ae0fcffd1` | los sujetos obligados difunden por portal web *«la siguiente información mínima **actualizada mensualmente**… de naturaleza obligatoria»*, que incluye la *«información total sobre el **presupuesto** anual… el asignado a cada área, programa o función, especificando **ingresos, gastos, financiamiento y resultados operativos**… así como la **liquidación** del presupuesto»* | ✅ `CNO-VII-001` · vigente · en el catálogo sellado |
| **LOTAIP 24** · `0e2435346ae1` | **obligación específica de los GAD**: *«mensualmente, informarán…»* — resoluciones, procesos legislativos e **instrumentos de planificación, incluido el PDOT** | ✅ `CNO-VII-002` · obligación central · vigente |
| **LOTAIP 29** · `570b34e6cc32` | las **empresas públicas** publican la *«información **mensual** sobre la ejecución presupuestaria»* | ⛔ no encadenado |

### Qué cambia

1. **La decisión de la dirección —Transparencia como capa de alimentación MENSUAL— tiene su raíz legal
   exacta**, y **ya estaba en el canon vigente**: LOTAIP 19 y 24. No es sólo una decisión de
   arquitectura: **es la cadencia a la que la ley obliga a la fuente.**
2. **El régimen temporal de la sección Recursos** *(«mensual con corte»)* **queda fundado en la ley**
   (LOTAIP 19), no en una conveniencia técnica.
3. **La evidencia de COOTAD 249 es de publicación mensual obligatoria**: LOTAIP 19 obliga a publicar el
   presupuesto **por programa**, con **ingresos** y gastos — es decir, **el numerador y el denominador**
   de la obligación del 10 %. *(Si ya está en el motor sigue **sin verificar**.)*
4. **LOTAIP 29 da base legal a la evidencia mensual por entidad** en la transversal de Ecosistema
   Municipal: la EP de Aseo (`ENTE-04`) está obligada a publicar su ejecución mensual.
5. **La procedencia debe registrar el canal:** una cédula remitida al ente rector y una publicada en el
   portal pueden no ser la misma versión. **Es la misma lección de `T3` —la vía importa— aplicada a las
   cadencias.**

**Nada del canon se tocó; nada amplía el alcance.** El trabajo sólo **ancló en la norma ya vigente** una
decisión que la dirección había tomado por conocimiento del terreno.

## 5-unquinquagies · **MATRIZ MAESTRA · CAPA TEMPORAL** — la cadencia como propiedad gobernada de cada realidad

> **Distinción que se conserva** *(colega)*: **COOTAD 168 describe un circuito institucional trimestral;
> LOTAIP 19 y 24 establecen el régimen mensual de publicación ciudadana que QUIRA usa como fuente.**
> **No se confunde periodicidad de remisión institucional con periodicidad de disponibilidad pública.**
>
> **La cadena que cada realidad debe hacer explícita:**
> `periodicidad normativa de la fuente → corte observado → evidencia disponible → indicador → consumidor`

### Aporte de esta dirección: no es UNA propiedad temporal, son TRES

| propiedad | pregunta | ejemplo |
|---|---|---|
| **periodicidad de publicación** | ¿cada cuánto la ley obliga a que la evidencia esté disponible? | LOTAIP 19: **mensual** |
| **periodicidad propia del objeto** | ¿cada cuánto cambia o se evalúa la realidad observada? | PDOT **plurianual** · POA **anual** · rendición **anual** |
| **corte observado** | ¿qué período declara hoy el motor? | `H07_S5`: «Abril 2026 (Ene-Abr)» |

> **Confundirlas produce justo los defectos de `C4`.** El PDOT **se publica** mes a mes (LOTAIP 24) pero
> **cambia** cada varios años; la obligación del 10 % de COOTAD 249 **se verifica** al aprobar el
> presupuesto anual, aunque su evidencia **se publique** cada mes. **Una afirmación debe declarar a cuál de
> las tres se refiere.**

### La capa temporal, realidad por realidad

| realidad | publicación *(norma · huella)* | periodicidad del objeto | corte observado hoy | evidencia | indicador | consumidores | **¿la condición temporal gobierna?** |
|---|---|---|---|---|---|---|---|
| **Inversión** *(sección Recursos)* | **mensual** · LOTAIP 19 `810ae0fcffd1` | presupuesto **anual**, ejecución **acumulada** al corte | `H07_S5!B10` «Abril 2026 (Ene-Abr)» · `B22 Mes_Activo = 4` **escrito a mano** · el bloque `financiero` con **otro corte** (2026-03) | cédula en el motor | `Ti` · `Ti_norm` (`H07b`) | ICPI · agente d02 · cajón · Concejo · IA | ⚠️ **parcial**: gobierna en el ICPI (`B34`) y en `RC-7.3`; **no** en el agente, el cajón ni el Concejo *(`C4-P1`)* |
| **Planificación** *(sección Trayectoria)* | **mensual** · LOTAIP 24 `0e2435346ae1` | PDOT **plurianual** · POA **anual** — COOTAD 233 `1522597f54b1`: antes del 10 de septiembre | ? | PDOT · POA *(vía `T3`)* | avance de metas (`H11b`, `H16b_IPE`) | `m_planificacion` · `plan_render` | ? no evaluado |
| **Transparencia** | **mensual** · LOTAIP 19 y 24 | mensual | calificación por mes *(2025 y meses 1-5 de 2026, según `BOOT`)* | portal de la DPE | cumplimiento de publicación | `p07_transparencia` · agente d07 | ? no evaluado en este corte |
| **Participación y Control Social** | anual | **anual** — ~~COOTAD 266~~ ⛔ *falsación 43*: la periodicidad la fijan **LOPC 95 · RES-CPCCS-RC-2026 Art. 5 y su cronograma para GAD** (`§5-duoquinquagies`) | fidelidad **«corte 2024»** · serie 2023-2025 | informes de rendición · actas | fidelidad narrativa · circuito CPCCS | `m_rdc` | ⚠️ el año se declara **al pie**, **no en la síntesis** donde se publica el 91 % *(`C4-P2`)* |
| **Grupos de Atención Prioritaria** | **mensual** · LOTAIP 19 *(presupuesto por programa, con ingresos)* | **anual** — COOTAD 249 se verifica **en la aprobación del presupuesto** | ? | presupuesto publicado mes a mes | *(candidato: 10 % de ingresos no tributarios)* | — | ~~aún no hay indicador~~ ⛔ *falsación 44*: el indicador **existe** en el circuito `GAP_10PCT` (`IND_G10P_01`) — y su denominador no es el de la norma (`§5-terquinquagies`) |
| **Ecosistema Municipal** *(transversal)* | **mensual** · LOTAIP 29 `570b34e6cc32` *(empresas públicas)* | anual con ejecución mensual | cortes por entidad al primer trimestre | ? | `Ti` por entidad | Concejo · holding | ? |
| **Gobernanza del Mandato** | ? | **por período de gobierno** | ? | plan de trabajo · PDOT | congruencia promesa↔plan | `m_mandato` | ? |
| **Cobertura · Económico · Ambiental** | ? — su fuente es estadística y diagnóstico del PDOT, **no normada por la LOTAIP en este corte** | multianual *(censos, diagnósticos)* | ? | ? | ? | ? | ? |

### La cadena de Grupos de Atención Prioritaria, sin saltos *(colega)*

```
LOTAIP 19  →  publicación MENSUAL del presupuesto por programa, con ingresos
     ↓
evidencia presupuestaria
     ↓
COOTAD 249  →  verificación ANUAL: 10 % de ingresos no tributarios, al aprobar el presupuesto
     ↓
eventual indicador o señal   ←  sin saltar directamente de la norma al SAT
```

> **Precisión temporal:** la evidencia mensual permite **seguir** durante el año cómo se ejecuta lo
> asignado; pero **la prueba legal es anual**, sobre el presupuesto aprobado. Un indicador futuro deberá
> declarar **régimen anual con actualización mensual** — no mezclarlos.

### ⛔ El hallazgo que la capa temporal vuelve grave

`C4-P0` había dejado como reserva que `Mes_Activo` es un **literal escrito a mano** con el rótulo
**«(auto)»**. Con la ley a la vista, deja de ser una reserva menor:

> **La ley obliga a una cadencia mensual (LOTAIP 19), y el mes que el motor declara se escribe a mano.**
> Es exactamente la forma de `C4`: la propiedad **existe** en el motor, pero **no la gobierna la fuente**
> que la ley establece.
>
> **Precisión del colega, acogida** *(`§5-quaterquinquagies`)*: la formulación demostrada es más
> estrecha — *la fuente normativa establece una periodicidad mensual de publicación, mientras que el
> estado temporal del motor (`Mes_Activo`) aparece declarado a mano y **no se ha demostrado una
> derivación gobernada** entre el corte de la evidencia y ese estado*. **La norma no decide la
> implementación**: derivación automática, metadato de corte que viaja con el dato, resolutor temporal
> central o una combinación se decide en cirugía.

### Lo que la capa temporal añade a la Matriz Maestra

| artefacto | V | acción |
|---|---|---|
| `H07_S5!B22` `Mes_Activo` | ⛔ literal a mano rotulado «(auto)» | **RECONSTRUIR** la relación gobernada entre el corte de la evidencia y el estado temporal — *el mecanismo se decide en cirugía, no desde la norma* |
| bloque `financiero` del snapshot | ⛔ corte distinto (2026-03) del vigente | **RECONSTRUIR** *(ya en la fila de derivados)* |
| agente d02 · `absorcion_ti_pct` | ⛔ viaja sin corte | **ELEVAR**: el corte y su periodicidad viajan con el valor |
| `m_rdc` · síntesis | ⛔ publica el 91 % sin su año | **RECORTAR** la ambigüedad: el año va junto a la cifra |
| procedencia de toda evidencia | ? | **ELEVAR**: registrar **el canal** —publicación ciudadana o remisión institucional— **y** las tres propiedades temporales |

**Nada del canon se tocó; ninguna cadencia se «corrigió» en el motor.** Esto es **diagnóstico de la
capa temporal**, listo para la cirugía cuando la dirección la abra.

## 5-duoquinquagies · **LA CADENA NORMATIVA DE CADA DOMINIO** — desde la Constitución, derivada de lo que QUIRA ya tiene *(corrección de la dirección)*

> **Javo:** *«el capítulo de rendición de cuentas está en la LOPC y la resolución administrativa del
> CPCCS. Tenemos la norma vectorizada… no es solo el COOTAD y el COPLAFIP. Es desde la Constitución y la
> cadena de artículos de las leyes que tocan lo que estamos trabajando; es muy ambiguo dejar la RDC solo
> con el COOTAD.»*
> **Tiene razón. El error es de método, no de lectura.**

### ⚠️ Falsación 43, mía

En la capa temporal (`§5-unquinquagies`) fundé la periodicidad de la rendición de cuentas en
**COOTAD 266**. El artículo existe (`33326955d115`) y dice lo que cité, pero **no es la norma que gobierna
la rendición de cuentas**: es una concordancia del capítulo presupuestario (el ejecutivo informa a la
asamblea territorial sobre la ejecución del presupuesto). **La cadena rectora ya estaba en el canon
vigente y sellado —`CNO-IX-001`, aprobada por la dirección el 2026-07-20— y no la leí.**

El mismo método —**ir a un artículo suelto en lugar de al rector**— se repitió en la misma tabla:
Planificación quedó anclada sólo en COOTAD 233 y Grupos de Atención Prioritaria sólo en COOTAD 249.
**Esta sección lo corrige para los ocho dominios.**

> **Regla que queda:** la norma de un dominio **se deriva de su cadena rectora** (la CNO si existe; si no,
> las capas que QUIRA ya tiene), **nunca de un artículo elegido ad hoc.** Un artículo suelto es una
> **concordancia**, no la cadena.

### 1 · La rendición de cuentas, con su propia cadena *(periodicidad verificada hoy en el corpus)*

| nivel | artículo · huella | qué establece | fuente |
|---|---|---|---|
| Constitución | CE 100 `8282b964440e` | instancias de participación en todos los niveles de gobierno | `CNO-IX-001` |
| Constitución | CE 208 `8c269ae98217` | deberes y atribuciones del CPCCS | `CNO-IX-001` |
| ley orgánica | LOPC 89 · 90 · 91 · 93 | definición · sujetos obligados · objetivos · nivel programático y operativo | `CNO-IX-001` |
| ley orgánica | **LOPC 92** `122bd1a01eb5` | **nivel político**: la autoridad electa rinde cuentas sobre su **plan de trabajo**, sus planes, el POA y el **presupuesto general y participativo** | hoy · **no encadenado** |
| ley orgánica | **LOPC 95** `e9b95d33a298` | **periodicidad**: *«una vez al año y al final de la gestión»* | hoy · **no encadenado** |
| resolución CPCCS | RES-CPCCS-RC-2026 Art. 10 · 13 · 15 · 21 | contenido mínimo · reglas para GAD · deliberación pública · consecuencia | `CNO-IX-001` |
| resolución CPCCS | **Art. 5** `2be5516ecdaf` | se rinde cuentas del **período fiscal concluido: 1 de enero a 31 de diciembre** | hoy · no encadenado |
| resolución CPCCS | **cronograma para GAD** `7606911e9f04` | feb–mar planificación desde la Asamblea Local · abril evaluación e informe · **mayo deliberación pública** · junio incorporación de la opinión ciudadana y seguimiento — *del año siguiente al período fiscal* | hoy · tabla sin número de artículo; **se atribuye al Art. 13 por su contenido** |
| concordancia | COOTAD 266 `33326955d115` | informe anual de ejecución presupuestaria a la asamblea territorial | **no es la regla de la rendición** |

**Dos consecuencias que no estaban a la vista:**

1. **El Art. 13** (`c2456d489297`) obliga también a **las personas jurídicas creadas por acto normativo
   del GAD** → el Patronato y las empresas públicas **rinden cuentas por sí mismas**. Toca a Grupos de
   Atención Prioritaria (Patronato) y a la transversal Ecosistema Municipal.
2. **LOPC 92** es el puente legal entre la rendición y **Gobernanza del Mandato**: la autoridad electa
   rinde cuentas **sobre su plan de trabajo**.

**La fila de la capa temporal, corregida:**

| realidad | publicación | periodicidad del objeto | corte observado | ¿la condición temporal gobierna? |
|---|---|---|---|---|
| **Participación y Control Social** · sección Rendición | **anual, por ciclo** — LOPC 95 · RES-CPCCS Art. 5 · cronograma para GAD (febrero a junio del año siguiente) | ejercicio fiscal | fidelidad «corte 2024» · serie 2023–2025 | ⚠️ el año va al pie y no en la síntesis (`C4-P2`) · **? por verificar:** según el cronograma, el ciclo exigible más reciente es el del ejercicio 2025 (deliberación en mayo de 2026); la síntesis debe declarar **de qué ciclo habla** |

### 2 · Lo que QUIRA ya tiene — cuatro capas, de épocas distintas

| capa | qué es | qué cubre | verificación |
|---|---|---|---|
| **BRN** · 16 CNO (`docs/brn/`) | cadena jurídica con huella por eslabón | Planificación (`I-001`) · Inversión (`IV-001`) · Mandato (`III-001`) · Transparencia (`VII-001…004`) · Participación (`VIII-000…007`, propuesta) · Rendición (`IX-001`) | ✅ huella por eslabón · **12 de 16 están en el grafo**: faltan las 4 de Transparencia (el dominio entra al grafo por 24 condiciones definidas por los numerales de LOTAIP 19) |
| **Átomos ACK** · 93 (`data/acks/`, fases F0.1–F0.6) | obligación atomizada: obligado, obligación, evidencia, consecuencia | derechos y competencias de la CE · COOTAD · LOTAIP · LOC-CGE · NCI · LOSEP · LOSNCP · CONA · adultos mayores · discapacidades · movilidad humana · COA | ⚠️ **ningún átomo lleva huella**; discrepancias abajo |
| **QLEP canónico v1.0** (`governance/qlep/`, congelado, junio 2026) | norma primaria y pregunta bautismal por dominio | los 12 dominios de la numeración antigua | ⚠️ **citas parafraseadas, no literales**; discrepancias abajo |
| **Corpus vectorizado** (Supabase) | texto oficial | 94 normas · 13 147 fragmentos | es **la fuente contra la que se verifica todo** |

Y un **índice** que no es capa: el manifiesto del corpus (`scripts/normativa/manifest.py`, 46 normas →
dominios). ⚠️ **No declara qué numeración de dominios usa** —coexisten al menos tres: la del QLEP
(`Dom01–12`), la de los scripts y conectores del grafo (`Dom03` = Contratación, `Dom04` = PDOT) y la de
los agentes (`d01–d13`)—. **En las tres el 09 es Rendición de Cuentas, y el manifiesto no etiqueta ni la
LOPC ni la resolución del CPCCS en el 09.** Es el mismo hueco que produjo mi error, en otra capa.

**Discrepancias verificadas contra el corpus** *(se registran; ninguna se repara aquí)*:

| capa | dice | el corpus dice |
|---|---|---|
| ACK `LOSNCP_21` | «Plan Anual de Contratación» | LOSNCP 21 `2406c95d781c` es el **Portal COMPRASPÚBLICAS**; el PAC es LOSNCP 22 `1d6c1b3ae153` (así lo encadena `CNO-I-001`) |
| ACK · siglas | LOAPAM · LOD · LOMH | en el corpus: **LOPAM · LODISC · LMH** |
| QLEP Dom11 | CE 264 **núm. 8** = uso del suelo | el núm. 8 es **patrimonio**; el control del uso del suelo es el **núm. 2** (contados en `8a610fc989a2`) |
| QLEP Dom02 | COOTAD 198 = «presupuesto de inversión; vinculación con POA y PAC» | COOTAD 198 `d1356370a4bd` = **destino de las transferencias** (hasta 30 % a gasto permanente, mínimo 70 % a no permanente) |
| QLEP Dom08 | COOTAD 304 = «partida específica para el presupuesto participativo» | COOTAD 304 `a1ccfa62c16f` = **sistema de participación ciudadana**; la palabra «partida» no aparece |

> **Consecuencia para QUIRA 7:** ninguna de las tres capas se hereda **literal**. Se hereda **la cadena**,
> y cada eslabón pasa por el corpus (Regla 3) antes de entrar.
>
> ✅ **Corregidas** por orden de la dirección, junto con todas las que encontró el barrido completo:
> `§5-terquinquagies`.

### 3 · La cadena de cada dominio de QUIRA 7

Orden de lectura: **Constitución → ley orgánica (competencia u obligación) → reglamento, resolución o
norma técnica (procedimiento, plazo, contenido) → publicación → control y consecuencia.** Entre
paréntesis, de dónde viene: **CNO** · **ACK** · **QLEP** · **hoy** (verificado en esta sesión, sin
encadenar). Todo artículo con huella fue leído en el corpus.

**① Planificación Estratégica e Inversión Pública** *(d01 + d02 + eficiencia directiva)*
- **Constitución:** CE 241 · 280 *(CNO-I-001)* · CE 264 núm. 1 `8a610fc989a2` *(ACK)* · CE 271 *(CNO-IV-001)*
- **Ley:** COPLAFIP 12 · 44 · COOTAD 215 · 233 `1522597f54b1` · 234 · 245 · LOSNCP 22 *(CNO-I-001)* ·
  COOTAD 192 · COOTAD-2026 198.1 · 198.2 · 198.6 · Disp. Trans. 1.ª *(CNO-IV-001)* · COPLAFIP 96
  `427f23a66e7c` · 119 `8a5e811f8f8b` *(`§5-novoquatrigies`)* · COOTAD 54 `53a6cf3041c4` · 57
  `4875f6818644` · 228 `b2c56883a157` *(ACK)* · COOTAD 60 *(CNO-III-001)*
- **Eficiencia directiva:** NCI «Administración estratégica» (200-02) `15079b69adb7` *(ACK; en el corpus
  sin número)* · NCI 200-04 estructura orgánica *(ACK; **? no localizada** en el corpus)* ·
  RES-ORG-GADMCM-2025, estructura orgánica por procesos *(en el corpus)*
- **Publicación:** LOTAIP 19 `810ae0fcffd1`, mensual *(CNO-VII-001)* · COOTAD 168 `919882337173`, canal institucional
- **Control:** COOTAD-2026 198.6 → Contraloría *(CNO-IV-001)* · LOC-CGE 12 `52784afdf867` *(ACK)*

**② Gobernanza del Mandato**
- **Constitución:** CE 61 · 105 *(CNO-III-001)*
- **Ley:** COD 97 · COOTAD 58 · 60 · COPLAFIP 41 · 42 · LOPC 89 · 90 *(CNO-III-001)* · **LOPC 92**
  `122bd1a01eb5` *(hoy — candidato a eslabón: se rinde cuentas sobre el plan de trabajo)*
- **Instrumento:** PLAN-GOB-MCR *(en el corpus)*

**③ Transparencia**
- **Constitución:** CE 18 · 91 · 238 *(CNO-VII-001…004)*
- **Ley:** LOTAIP 7 · 8 · 9 · 10 · 13 · 19 · 24 · 32–38 · COOTAD 57 · 60 *(CNO-VII)* · LOTAIP 29
  `570b34e6cc32`, empresas públicas *(`§5-quinquagies`)* · LOTAIP 11 `04b50eeb8135`, informe anual a la DPE ·
  LOTAIP 39 `9ff6a6949175`, responsabilidad del titular *(ACK)*
- **Reglamento y norma técnica:** RLOTAIP 10–15 · GUIA-LOTAIP-MEC · INST-LOTAIP-MON · INST-LOTAIP-PAR ·
  ACUERDO-PDOT-2023 *(CNO-VII)*
- **Control:** LOTAIP 42 *(CNO-VII)*

**④ Participación Ciudadana y Control Social**
- *Sección Participación* *(CNO-VIII, **propuesta**)*: CE 95 · 61 · 100 → sistema (COOTAD 304 · 312 ·
  LOPC 64 · 65) · asamblea (LOPC 56–58 · 61 · COOTAD 306 · 307) · consejo de planificación (COPLAFIP 13 ·
  28 · 29 · 46) · audiencia (LOPC 73–75 · COOTAD 60) · presupuesto participativo (LOPC 67 · 71 · COOTAD
  238) · cabildo (CE 100 · LOPC 76) · silla vacía (CE 101 · LOPC 77 · COOTAD 311)
- *Sección Rendición de cuentas y control social*: la cadena del punto 1 *(CNO-IX-001 vigente + LOPC 92 ·
  95 · RES Art. 5 · cronograma, hoy)*
- **Concordancias, no rectoras:** COOTAD 266 · COOTAD 300 `d0a387760026` · COOTAD 302 `30fa6a7bba59`

**⑤ Cobertura de Servicios e Infraestructura** *(sin CNO)*
- **Constitución:** CE 12 `e44156c3b7ed` (agua) · CE 30 `3c59f419738c` (hábitat) · CE 31 `3bde62de4695`
  (ciudad) · CE 264 núm. 3 (vialidad) · 4 (agua, alcantarillado, desechos, saneamiento) · 7
  (equipamientos de salud y educación, espacio público) · 13 (incendios) `8a610fc989a2` *(ACK · QLEP)*
- **Ley:** COOTAD 55 `7cba2417d70a` · 137 `7706e03a01f7` *(ACK)* · LOTUGS *(en el corpus, sin encadenar)*
- **Publicación y control:** **?** — el QLEP usa `LOTAIP_19_6`; no se verificó en esta sesión

**⑥ Desarrollo Económico Territorial** *(sin CNO)*
- **Constitución:** CE 276 `affc0b120408` *(QLEP)* · CE 264 núm. 2, control del uso del suelo *(el QLEP lo cita como núm. 8)*
- **Ley:** COOTAD 54 *(funciones; el QLEP usa su literal g, turismo)* · LOIEME · LOTUGS *(en el corpus, sin encadenar)*

**⑦ Grupos de Atención Prioritaria** *(sin CNO)*
- **Constitución:** CE 35 `fba71e80b2f5` · CE 11 `4d55c178a648`, acción afirmativa *(ACK)*
- **Ley orgánica general:** COOTAD 249 `c0c0fce0f126`, 10 % de los ingresos no tributarios *(ACK)*
- **Leyes especiales — obligaciones del GAD:** CONA 12 `309043e3453a` (prioridad absoluta) · LOPAM 14
  `59389f58607f` (exoneraciones) · 84 `136da121f808` (atribuciones de los GAD) · LODISC 47 `8ae3a51c82fc`
  (inclusión laboral 4 %) · 56 `662d1c6c9af8` (vivienda) · 58 `86ca98942a5a` (accesibilidad) · LMH 165
  `3a7f08ee906d` · 166 `eb07339e6543` · 167 `212336e992a6` *(ACK)* · **LPEVM 38** `631dbfded167`,
  atribuciones de los GAD *(hoy — sin átomo)*
- **Instrumentos internacionales en el corpus:** CDN · CEDAW · CADH · PIDESC
- **Publicación:** LOTAIP 19, presupuesto por programa, mensual · **Rendición:** RES-CPCCS Art. 13 — el Patronato rinde cuentas por sí mismo
- **Frontera** *(decisión de la dirección)*: CONA 207 `85b98b498b13` integra la Junta Cantonal de
  Protección de Derechos → **fuera del objeto**; se conserva como límite, no como eslabón

**⑧ Sostenibilidad y Resiliencia Ambiental** *(sin CNO)*
- **Constitución:** CE 14 `b7148c0ba23f` *(ACK)* · CE 389 `cc1f9192773c` · 390 `77dee2a1ad42`, gestión de
  riesgos *(hoy)* · CE 264 núm. 4, desechos y saneamiento ambiental
- **Ley:** COOTAD 136 `2f45a601705d`, gestión ambiental · 140 `0dc5f48de6bb`, gestión de riesgos *(hoy)* ·
  COA-AMB 27 `46d69b2c611e`, facultades ambientales de los GAD municipales *(hoy)* · RCOA-AMB *(en el corpus)*

**Transversales** *(lo mínimo, sin ampliar)*: **Ecosistema Municipal** — CE 315 `4484be1b204e` · COOTAD 57 ·
LOTAIP 29 · RES-CPCCS Art. 13; ⚠️ **la LOEP no está en el corpus** (0 fragmentos) · **Cumplimiento
Institucional** — CE 226 `a98d7fb2484f` · 227 `3618fc4dea8a` · LOC-CGE · NCI · **Equidad y Género** —
LPEVM · LOIEME · CEDAW.

### 4 · Lo que queda establecido, y lo que no se toca

| | |
|---|---|
| **establecido** | cada dominio tiene su cadena **desde la Constitución**, derivada de las capas que QUIRA ya tiene; los artículos con huella se leyeron en el corpus |
| **lo que falta** | cuatro dominios **sin CNO** (Cobertura · Económico · Grupos de Atención Prioritaria · Ambiental): su cadena existe en ACK y QLEP, **no en la BRN** · las 4 CNO de Transparencia, fuera del grafo · LOPC 92 · 95 · RES Art. 5 y el cronograma, sin encadenar en `CNO-IX-001` |
| **no se tocó** | el canon (`docs/brn`), el grafo, los ACK, el QLEP (congelado) ni el manifiesto · **no entra ninguna norma nueva: todo lo citado ya está en el corpus** |
| **a la mesa, cuando se abra la cirugía** | (a) si `CNO-IX-001` incorpora la periodicidad (LOPC 95 · RES Art. 5 · cronograma): **toca el canon sellado y requiere ratificación** · ~~(b) qué numeración de dominios gobierna el manifiesto~~ **(b) resuelta por el colega: ninguna** — QUIRA 7 define las realidades y las numeraciones anteriores pasan a ser **proveniencia** (`§5-quaterquinquagies`) · (c) las CNO de los cuatro dominios sin cadena, una por una y con el filtro de tres preguntas |

Las tres decisiones pendientes de la dirección (`RO-VIII-004` · retiro de SAT-I, VII y VIII · definición
de SAT-III) **siguen igual**.

## 5-terquinquagies · **CORRECCIÓN NORMATIVA DE LAS CAPAS HEREDADAS** — y el mecanismo para que no se repita *(orden de la dirección)*

> **Javo:** *«Ud asume y no lee… Debe hacer algo para que ya no pase eso»* · *«corregir esas partes
> donde se cita mal los artículos… en un ecosistema que se sustenta de la normativa jurídica vigente,
> eso es falsear la verdad»* · *«en derecho nada redunda: si hay que incorporar artículos que no hemos
> tomado en cuenta, hay que hacerlo»*.

### La causa, sin rodeos

El error es mío y tiene un mecanismo preciso: **cito desde lo que recuerdo en lugar de leer el rector y el
corpus.** Un recordatorio no lo corrige: el aviso «¿consultaste el índice maestro?» se disparó decenas de
veces en esta misma sesión y la falsación 43 ocurrió igual. **Lo que falta no es una advertencia más, es una
verificación de lo que se escribe, en el momento en que se escribe.**

### El mecanismo — cinco piezas, en el repositorio

| pieza | qué hace | cuándo actúa |
|---|---|---|
| `scripts/normativa/verificar_citas.py` *(sólo lectura)* | **1** cada huella corresponde al artículo citado · **2** cada artículo citado existe en el corpus · **3** si la línea trata la materia de una CNO y cita un artículo que ninguna CNO encadena: *¿rector, eslabón faltante o concordancia?* | a demanda |
| hook `PostToolUse` *(local, `.claude/settings.json`)* | revisa **lo recién escrito** en `.md`/`.yaml`: **bloquea** si hay huella falsa o artículo inexistente; **avisa** si falta el rector | después de cada edición |
| `check_health` **[6/6]** | revisa PANORAMA, QLEP, ACK, QTMP y BRN — **57 archivos** | antes de cada commit *(obligatorio)* · en CI: «2 — no determinable» |
| `CLAUDE.md` · PROHIBICIONES | *«citar un artículo sin leer su rector y el corpus»* | al arrancar cada sesión |
| `tests/test_verificar_citas.py` | **11 pruebas** que reproducen los errores reales de hoy — incluida la falsación 43 | en la suite |

**Probado:** ante *«la rendición de cuentas es anual según COOTAD 266»* el hook bloquea y devuelve la
cadena de `CNO-IX-001` completa; ante un texto correcto no dice nada.

⚠️ **Límite declarado:** el verificador prueba **huella, existencia y pertenencia a la cadena**; **no prueba
que una paráfrasis diga lo que el artículo dice.** Eso sólo lo prueba la lectura contra el texto —el
barrido de hoy—. Por eso la regla de escritura queda así: **cita literal con su huella; toda paráfrasis o
interpretación, marcada como tal.**

### El barrido — universo declarado

**93 átomos ACK · las citas de norma primaria del QLEP · 109 eslabones de las 16 CNO · las 24 condiciones de
LOTAIP 19 del grafo · los circuitos QTMP.** Todo contra el corpus vectorizado (94 normas · 13 147 fragmentos).

| capa | resultado | corrección |
|---|---|---|
| **BRN** · 16 CNO | ✅ **109 de 109 sumillas coinciden con su artículo.** El canon está limpio — salvo el mapa de numerales de `CNO-VII-001` *(abajo)* | ninguna |
| **QLEP** | **8 textos presentados como literales no son el texto de su artículo** — 5 no aparecen en ninguna parte del corpus (COOTAD 57 · 228 · 300 · 302 · LOC-CGE 12), 1 era de la LOTAIP derogada (LOTAIP 7), 2 eran paráfrasis ampliadas (COOTAD 249 · 304) · **2 descripciones de otra materia** (COOTAD 198 · COPLAFIP 44) · **3 numeraciones erradas**: el texto atribuido a CE 209 es del **CE 207** `fa7fe58c151b` · CE 264 núm. 8 → **núm. 2** · NCI 600-01 → **600** | **v1.1**: su propia regla la autoriza (*«v1.1 — solo si un error factual normativo es identificado»*). Texto literal con huella; **las preguntas bautismales no se tocaron** · 13 de 13 citas literales verificadas |
| **ACK** · artículo equivocado | LOSNCP 21 → **22** (el PAC `1d6c1b3ae153`; el 21 es el portal) · LOSNCP 22 → **23** (estudios `3cd06a225dc5`; la certificación presupuestaria es el **24** `c18eee97ef76`) · LOSEP 4 → **3** (ámbito) · LOSEP 22 → **23** (derechos; el 22 son deberes) · LOSEP 42 → **43** (sanciones; el 42 son faltas) · LOTAIP 19 núm. 21 → **núm. 18** (convenios) | átomos renumerados, texto literal con huella, `ID_ANTERIOR` para la trazabilidad |
| **ACK** · el texto dice otra cosa | LOSNCP 106 tipifica infracciones **de proveedores** (el átomo lo extendía a servidores y a la CGE) · COA 14 es el principio de **juridicidad** · CE 32: la interpretación *«el GAD puede proveer salud a los GAP»* iba como texto de la Constitución, y **COOTAD 138** `10684e6e6766` habilita **infraestructura y equipamientos**, no la prestación del servicio | texto literal · la interpretación queda **marcada como interpretación** |
| **artículos inexistentes** | «LOD Art. **563**» (la LODISC termina en el 117 → la infracción es el **Art. 116** `c695612e6a41`) · «LOTAIP Art. **47**» (la LOTAIP vigente termina en el 44 → las sanciones son el **Art. 42** `ae8004ee019f`) | corregidos |
| **QTMP** | circuito de agua: «LOSNCP Art. 21» para el PAC → **22** · *«obligación de publicación **trimestral**»* → **mensual** (LOTAIP 19) · un átomo de convenios usado como «información del servicio» → átomo general del art. 19 · circuito de transparencia: solicitudes «Art. 20» → **Arts. 32–38** | corregidos |
| **NCI** | el corpus **no conserva los códigos** de las NCI: los códigos de los 7 átomos no son verificables | se añade la **huella del título** verificado y se declara el código como no verificado |
| **propagación** | **101 referencias en 12 archivos** + 7 identificadores compuestos + 1 relación reencaminada (la publicación del PAC la ordena LOSNCP 22, no LOTAIP 19) | aplicada · 25 YAML válidos · verificador en 0 hallazgos |

### Lo que no se tocó, y por qué

| dónde | qué dice | por qué no | qué sigue |
|---|---|---|---|
| **`CNO-VII-001`** · `observa_capas` *(canon sellado)* | `numeral: "21"` · `ack: LOTAIP_19_21` para convenios | tocarlo **caduca el sello** de la dirección | **propuesta de diff, 2 líneas:** `"21"` → `"18"` · `LOTAIP_19_21` → `LOTAIP_19_18` — **para ratificar y resellar** |
| Gold Master · `SAT_Catalogo` | 6 de 10 SAT citan artículos que no dicen lo que el catálogo afirma (`§5-septquatrigies`) | Regla 1: el Excel se corrige **sobre copia, con evidencia** | en la **versión 7** del Excel |
| `docs/corpus_externo/*` · `docs/adr/*` | citas históricas (p. ej. `LOSNCP_21` en el modelo causal v1.0) | son registro de época, no afirmación vigente | ninguna |
| `data/ack_registry.json` | `LOTAIP_47` | ya declara *«Art. 47 no encontrado en corpus»* | al regenerarse, apuntar al 42 |
| `data/centrality_results.json` | ids antiguos | es **evidencia computada** del `ADR-019` | ninguna |

### ⚠️ Falsación 44, mía — y un hallazgo que el barrido destapó

En la capa temporal escribí que Grupos de Atención Prioritaria *«aún no tiene indicador»*. **Falso:** el
circuito `GAP_10PCT` lo define (`IND_G10P_01`, con 20,84 % codificado y 14,19 % devengado). No lo leí.

Y al leerlo aparece esto **(se registra; no se repara)**:

| la norma · COOTAD 249 `c0c0fce0f126` | el indicador · `IND_G10P_01` |
|---|---|
| *«por lo menos, el diez por ciento (10%) de sus **ingresos no tributarios**»* | `(partida_GAP_codificada / **presupuesto_GAD_no_salarial_codificado**) × 100` |

**El denominador no es el de la norma.** Es la forma de `C4` —**sustitución semántica**—: el 10 % existe en
el indicador, pero no mide la obligación que dice medir. Un «verde» con ese denominador no acredita el
cumplimiento del COOTAD 249.

## 5-quaterquinquagies · **MATRIZ MAESTRA · CAPA DE REALIDADES** — cadena normativa y gobierno temporal *(consolidación de `E` pedida por el colega)*

> **La regla al frente** *(colega)*: **una periodicidad normativa no se hereda como etiqueta del
> indicador. Se conserva como propiedad de la cadena temporal que vincula fuente, objeto, corte,
> evidencia, cálculo y consumidor. Cuando las periodicidades difieren, la cadena declara expresamente
> su relación.** *El tiempo deja de ser metadato del dato y pasa a ser parte de su significado.*
>
> **Y la regla de arquitectura** *(colega)*: QUIRA 7 define las **realidades administrativas**. Las capas
> anteriores —QLEP `Dom01–12`, el manifiesto, los scripts del grafo, los agentes `d01–d13`— **no compiten
> por ser «la verdadera»: pasan a ser proveniencia** de la cadena de cada realidad. **No nace una cuarta
> taxonomía.**

Esta capa **no reemplaza** la matriz de artefactos (`§5-quinquatrigies`, E/V/C/G/acción): se le **superpone**.
Aquella dice qué se conserva, eleva o retira; ésta dice **qué realidad observa cada dominio, bajo qué norma
y en qué régimen temporal**.

### Las siete propiedades temporales

| propiedad | pregunta |
|---|---|
| **periodicidad de la fuente** | ¿cuándo obliga la norma a publicar, remitir o actualizar la evidencia? |
| **periodicidad del objeto** | ¿cuál es el ciclo propio de lo que se mide? |
| **corte observado** | ¿qué período representa el dato concreto? |
| **estado de la evidencia** | ¿la evidencia de ese corte existe y fue localizada? |
| **régimen de cálculo** | ¿el indicador es mensual, anual, acumulado, plurianual? |
| **consumidor** | ¿quién recibe el valor, y con qué contexto temporal? |
| **regla de alineación** *(aporte del colega)* | ¿qué ocurre cuando la periodicidad de la fuente y la del objeto difieren? |

### A · Las ocho realidades: cadena normativa y proveniencia

| QUIRA 7 | realidad que observa | cadena normativa *(Constitución → ley → reglamento o resolución)* | rector | proviene de | construcción |
|---|---|---|---|---|---|
| **Planificación Estratégica e Inversión Pública** | cumplimiento del PDOT por la vía de la **inversión**, y la eficiencia directiva por dirección y por técnicos | CE 241 · 280 · 264 núm. 1 · 271 → COPLAFIP 12 · 44 · 96 · 119 · COOTAD 215 · 233 · 234 · 245 · 192 · 198 · COOTAD-2026 198.1 · 198.2 · 198.6 → LOSNCP 22 · 23 · 24 | `CNO-I-001` · `CNO-IV-001` | QLEP Dom01 · 02 · 03 · 06 · agentes `d01` · `d02` | iniciada |
| **Gobernanza del Mandato** | congruencia entre la promesa inscrita y la gestión | CE 61 · 105 → COD 97 → COOTAD 58 · 60 → COPLAFIP 41 · 42 → LOPC 89 · 90 *(+ LOPC 92, eslabón faltante)* | `CNO-III-001` | agente `d03` | iniciada |
| **Transparencia** | cumplimiento de la publicación obligatoria y calidad de lo publicado — **y capa de alimentación mensual** | CE 18 · 91 · 238 → LOTAIP 7 · 8 · 9 · 10 · 13 · 19 · 24 · 29 · 32–38 · 42 → RLOTAIP 10–15 → instructivos de la DPE | `CNO-VII-001…004` | QLEP Dom07 · agente `d07` | iniciada · la más sana |
| **Participación Ciudadana y Control Social** | incidencia de la ciudadanía en la inversión · rendición de cuentas | *Participación:* CE 95 · 61 · 100 → LOPC 56–77 · COOTAD 238 · 304–312 · COPLAFIP 13 · 28 · 29 · 46 — *Rendición:* CE 100 · 208 → LOPC 89–95 → RES-CPCCS-RC-2026 5 · 10 · 13 · 15 · 21 | `CNO-VIII-000…007` *(propuesta)* · `CNO-IX-001` | QLEP Dom08 · 09 · agentes `d08` · `d09` | iniciada |
| **Cobertura de Servicios e Infraestructura** | acceso equitativo y continuo a los servicios de competencia municipal | CE 12 · 30 · 31 · 264 núm. 3 · 4 · 7 · 13 → COOTAD 55 · 137 · 138 | — *(sólo ACK y QLEP)* | QLEP Dom10 · circuito `AGUA_POTABLE` | **parcial**: motor, página y circuito; sin BRN ni agente |
| **Desarrollo Económico Territorial** | condiciones que el GAD controla para la actividad económica | CE 276 núm. 2 · 264 núm. 2 → COOTAD 54 *(+ LOIEME · LOTUGS en el corpus)* | — | QLEP Dom11 *(módulo deshabilitado)* | **no iniciada** |
| **Grupos de Atención Prioritaria** | la función ejecutora del GAD hacia los grupos prioritarios | CE 35 · 11 → COOTAD 249 → CONA 12 · LOPAM 14 · 84 · LODISC 47 · 56 · 58 · 116 · LMH 165–167 · LPEVM 38 | — *(sólo ACK y QLEP)* | QLEP Dom12 · circuito `GAP_10PCT` · `p19_genero` | **parcial**: circuito e indicador; sin BRN ni agente |
| **Sostenibilidad y Resiliencia Ambiental** | gestión ambiental y de riesgos de competencia municipal | CE 14 · 389 · 390 · 264 núm. 4 → COOTAD 136 · 140 → COA-AMB 27 → RCOA-AMB | — | canon `d13` · `H20_ICODS` | **no iniciada** |

> *(Dirección: «hay dominios en los que no se ha construido nada… no se los ha empezado». En esta matriz
> **«no iniciada» no es un defecto: es un estado.** Esos dominios estaban en construcción cuando se abrió
> `REARQ`.)*

### B · Las ocho realidades: régimen temporal

| QUIRA 7 | fuente | objeto | corte observado | evidencia | cálculo | regla de alineación | consumidores | **gobierno temporal** |
|---|---|---|---|---|---|---|---|---|
| **Planificación e Inversión** | **mensual** — LOTAIP 19 `810ae0fcffd1` · PAC en los 15 primeros días de enero — LOSNCP 22 `1d6c1b3ae153` · *remisión institucional trimestral (COOTAD 168): otro canal* | PDOT plurianual · POA anual (COOTAD 233 `1522597f54b1`: antes del 10 de septiembre) · presupuesto por ejercicio | `H07_S5` «Abril 2026 (Ene–Abr)» · `Mes_Activo = 4` a mano · bloque `financiero` 2026-03 | cédula en el motor para el corte declarado ✅ · correspondencia con la publicación mensual ❓ | `Ti` acumulado al corte · ICPI anual | acumulado mensual comparado con meta anual **sólo con guarda de proporcionalidad** | ICPI · agente `d02` · cajón · Concejo · IA | **PARCIAL** — demostrado en `H12!B34` y `RC-7.3`; ausente en agente, cajón y Concejo (`C4-P1`) |
| **Mandato** | plan de trabajo inscrito **una vez**, con la candidatura (COD 97) · rendición anual sobre ese plan (LOPC 92 `122bd1a01eb5` · 95 `e9b95d33a298`) | período de gobierno | ❓ | plan de gobierno (en el corpus) · PDOT | congruencia promesa ↔ plan | ¿fracción del período transcurrido? **❓ no declarada** | `m_mandato` · agente `d03` | **NO EVALUADO** |
| **Transparencia** | **mensual** — LOTAIP 19 · 24 `0e2435346ae1` · empresas públicas LOTAIP 29 `570b34e6cc32` | mensual: cada mes es una obligación exigible | calificación 2025 y meses 1–5 de 2026 | portal de la DPE ✅ · web del GAD (`T3`) ❓ | por período exigible (`RO-VII-001`) | el mes calificado debe alimentar a los otros dominios **con su mes** — ❓ | `p07` · agente `d07` · **los otros siete dominios** | **DECLARADO** en `RO-VII-001` · no evaluado en `C4` |
| **Participación** *(sección)* | ❓ | ciclo anual del presupuesto participativo (LOPC 67 · 71 · COOTAD 238) | medición 2026-07-29: 162 de 191 demandas vinculantes sin correlato (84,8 %) | actas de presupuesto participativo, audiencias y cabildos — las escaneadas requieren OCR | incidencia sobre demandas vinculantes | ❓ | `m_participacion` | **NO EVALUADO** |
| **Rendición** *(sección)* | **anual por ciclo** — LOPC 95 · RES-CPCCS-RC-2026 Art. 5 `2be5516ecdaf` · cronograma para GAD `7606911e9f04` | ejercicio fiscal (1 de enero a 31 de diciembre) | fidelidad 91 % — fuente *«Rendición de Cuentas **2024** (video oficial)»*: **el ejercicio no se declara** | informes RC-GAD 2023 · 2024 · 2025 en el corpus; el de 2025 declara *«período fiscal 2025»* ✅ | fidelidad por afirmación (9) | **ejercicio → cronograma → fase → evidencia** *(abajo)* | `m_rdc` · `p17_rdc` | ⛔ el año va al pie y no en la síntesis (`C4-P2`) · la cifra **no declara su ejercicio** |
| **Cobertura** | ❓ | multianual (censo, NBI) | ❓ | `H42_IET` · `SCHEMA_NBI` · circuito `AGUA_POTABLE` | ❓ | ❓ | `p10_territorio` | **NO EVALUADO** |
| **Económico** | — | — | — | — | — | — | — | **NO INICIADO** |
| **Grupos de Atención Prioritaria** | **mensual** — LOTAIP 19 (presupuesto por programa) | **anual** — COOTAD 249 se verifica al aprobar el presupuesto | `IND_G10P_01`: 20,84 % codificado · 14,19 % devengado *(corte no declarado en el circuito)* | cédula SIGEF, según el propio indicador | anual · semestral (adultos mayores) · anual (inclusión laboral 4 %) | **LOTAIP mensual → acumulación → condición anual del COOTAD 249 → indicador anual con actualización mensual** *(colega)* | `p19_genero` | ⛔ **el denominador del indicador no es el de la norma** (`§5-terquinquagies`) |
| **Ambiental** | — | diagnóstico del PDOT *(plurianual)* | — | `H20_ICODS` · `SCHEMA_RIESGOS` | — | — | — | **NO INICIADO** |

### C · Transversales, por separado

| transversal | temporalidad | estado |
|---|---|---|
| **Ecosistema Municipal** | cada entidad publica su ejecución **mensual** (LOTAIP 29) y **rinde cuentas por sí misma** (RES-CPCCS-RC-2026 Art. 13) · cortes por entidad al primer trimestre | **ELEVAR** a atributo obligatorio de toda observación · gobierno temporal ❓ |
| **Equidad y desagregación** | hereda la del dato que desagrega · `PSG` (`H16c`) · LPEVM · LOIEME · CEDAW | ❓ |
| **Síntesis institucional** (ICPI) | anual, con guarda temporal `H12!B34` | ✅ **el único gobierno temporal demostrado** (`C4-P0`) |
| **GeoTwin** | la de cada capa territorial | ❓ no evaluada |
| **Cooperación** | — | **producto**: fuera de `E` |
| **Infraestructura de adquisición** | debe registrar el **canal** (publicación ciudadana o remisión institucional), la **vía**, la **versión** y la **huella** | **ELEVAR** |

### D · Rendición de cuentas: la traza que el colega exige antes de afirmar un ciclo

| paso | dato | estado |
|---|---|---|
| ejercicio | 2025, del 1 de enero al 31 de diciembre (RES-CPCCS-RC-2026 Art. 5) | norma ✅ |
| cronograma | febrero–marzo planificación · abril informe · **mayo deliberación** · junio seguimiento, **de 2026** | norma ✅ *(tabla del reglamento)* |
| fase y fecha reales en Montecristi | — | **❓ no verificada** |
| evidencia disponible | RC-GAD-2025 en el corpus, que declara *«período fiscal 2025»* | ✅ verificada |
| lo que publica QUIRA | fidelidad 91 %, fuente *«Rendición de Cuentas 2024 (video oficial)»* | ⛔ **no declara su ejercicio** |

> **Lo demostrado no es «el ciclo exigible es 2025».** Lo demostrado es más estrecho y más útil: **la
> evidencia del ejercicio 2025 existe en el corpus, y la cifra publicada no declara a qué ejercicio
> pertenece.** *(Se retira la inferencia de `§5-duoquinquagies` como hecho: queda como traza abierta en
> un paso.)*

### Lo que sigue: la cirugía, con esta matriz como plano

`E` queda **consolidado**; no se abre más excavación. La cirugía decide, propiedad por propiedad, **qué entra
al nuevo Gold Master, qué sale, qué se deriva y qué debe viajar obligatoriamente con cada valor** —el corte,
su periodicidad y su canal, en primer lugar—.

**Pendientes de la dirección:** las tres decisiones de `§5-quattrigies` (sin cambios) · y **resellar
`CNO-VII-001`** con la corrección del numeral de convenios (21 → 18).

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
