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

### ★ La deuda real: `C` · 100 rectores de facto

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
