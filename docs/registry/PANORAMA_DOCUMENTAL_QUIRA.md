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

## 6 · Y la finalidad, dicha por la dirección

> *«No es una auditoría, sino **elevar este ecosistema**… para potenciar, mejorar y elevar el nivel
> de QUIRA en cada ámbito.»*

⛔ Por eso este registro **no propone conservar por defecto**. La cautela de `REARQ-001` —no
inventar canon duplicado, no destruir procedencia histórica— **no es un mandato de congelación**.
Elevar el ecosistema **incluye crear y elevar capacidades**, y también **retirar lo que ya no
sostiene ninguna**.

---
*Panorama documental · 275 documentos · 2,83 MB · 472 reglas · Dylus Lab © 2026 · insumo para
decisión de gobernanza, no decisión.*
