# QUIRA-NEXT · CARTA DE REARQUITECTURA  `v2`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/carta_rearquitectura.py`.

```
  INVENTARIO_ID : QNEXT-INV-2026-09-05
  COMMIT        : b5035ad
  GENERATED_AT  : 2026-09-05T22:18:26+00:00
```

> Sin esta estampilla, «412 documentos» es una **afirmación flotante**. Con ella es una **observación reproducible de un estado concreto del repositorio** — y explica sola por qué la v1 dijo 411 y esta dice otra cifra: el propio acto de escribir la carta añadió archivos.

> ### Qué es esto
> El plan del **refactor integral de fondo y forma de todo el ecosistema**. **No ejecuta nada.**

⚠️ **El Gold Master sigue congelado hasta `011-C4`.** Planificar el refactor **no adelanta** el momento de intervenir el motor, y el baseline **27,4582 %** no se mueve.

## Por qué esta carta es una `v2` estructural y no un parche

La `v1` inventarió el repositorio y llamó a eso «el ecosistema». Javo señaló lo que faltaba, y era medular:

> *«NO estamos tomando en consideración al corpus normativo de todo el marco legal que hemos vectorizado a Supabase, que es la otra base medular de QUIRA […] se vuelve con el Excel las bases metodológica y legal para el ecosistema.»*

**El modelo de inventario de la `v1` era incompleto desde su raíz**: contaba archivos y omitía las bases de conocimiento. Eso no se parchea.

### Y una corrección de hecho, sobre la objeción a la `v1`

El colega observó que el total `1321` no cuadraba con `1265` y concluyó que había un error de cardinalidad. **Verificado: el total era correcto.** La suma omitía tres filas —`brn` (30), `governance` (23), `marco_teorico` (3) = **56**, exactamente la diferencia detectada—.

> **Pero la conclusión seguía siendo correcta por otra razón:** si un lector experto suma mal la tabla, **la tabla no era legible**. Se corrige la tabla, no el número — y se añade la regla de conteo explícita.

## ★ EJE 0 · Las cuatro bases medulares

Antes que los diez ejes. QUIRA **no se apoya en el Excel**: se apoya en cuatro bases, y el Excel es una de ellas.

| | Base | Qué es | Pregunta que responde |
|---|---|---|---|
| `BM-01` | **NORMATIVA** | corpus jurídico ecuatoriano · Supabase | ¿qué derecho vigente permite afirmar que una competencia, obligación o procedimiento existe? |
| `BM-02` | **METODOLÓGICA** | Gold Master · Excel · canon metodológico | ¿cómo transforma QUIRA esa realidad en conocimiento calculable? |
| `BM-03` | **EVIDENCIAL** | CNE · GAD · SERCOP · CPCCS · LOTAIP · eSIGEF | ¿qué documento o registro demuestra el hecho observado? |
| `BM-04` | **ONTOLÓGICA** | dominios · entidades · unidades · relaciones | ¿qué cosas existen, cómo se llaman y cómo se relacionan? |

```
                       QUIRA
                         │
           ┌─────────────┴─────────────┐
      BM-01 NORMATIVA          BM-02 METODOLÓGICA
      corpus jurídico          Gold Master · Excel
      Ecuador · GAD            metodología + datos
           └─────────────┬─────────────┘
                         │
                   MOTOR DE QUIRA
                         │
           ┌─────────────┴─────────────┐
      BM-03 EVIDENCIA          BM-04 ONTOLOGÍA
      qué ocurrió              qué cosas existen
           └─────────────┬─────────────┘
                         │
                    INFERENCIA
                         │
                   INTELIGENCIA
                         │
        ┌────────────────┼────────────────┐
      FONDO            FORMA          TRANSVERSAL
```

### ★ La distinción que no debemos volver a mezclar

| | Afirmación | Fuente |
|---|---|---|
| **NORMA** | «la ley establece X» | corpus jurídico · `BM-01` |
| **EVIDENCIA** | «el GAD hizo o no hizo X» | CNE · SERCOP · CPCCS · LOTAIP · eSIGEF · `BM-03` |
| **INFERENCIA QUIRA** | «de norma + evidencia + metodología se sigue Y» | motor metodológico · `BM-02` |

> ### La fuente normativa tiene PRECEDENCIA sobre el diseño de QUIRA
>
> Si la metodología dice que `C_i` significa X y la norma vigente determina otra cosa sobre esa competencia o responsabilidad, **la metodología no puede ignorarlo**. Es la diferencia entre `⚖️ NORMATIVO VIGENTE` y `🔧 DECISIÓN DE DISEÑO`.

Y de aquí sale lo que QUIRA **es**, dicho sin metáfora:

> No es un Excel sofisticado, ni un dashboard, ni un índice, ni un corpus jurídico, ni un RAG legal. Es un **sistema que relaciona norma, evidencia, metodología y contexto territorial para producir inferencias reproducibles sobre la gestión pública**.

## ★ `BM-01` · El corpus normativo, medido

**13.147 fragmentos · 94 normas distintas · 27 tablas** en el esquema.

| `tipo_documento` | Fragmentos | Naturaleza |
|---|---:|---|
| `ley_organica` | 4297 | ⚖️ **norma** |
| `INSTRUMENTO_TERRITORIAL` | 2995 | 📋 instrumento / evidencia |
| `reglamento` | 2053 | ⚖️ **norma** |
| `plan_territorial` | 824 | 📋 instrumento / evidencia |
| `plan` | 600 | 📋 instrumento / evidencia |
| `constitucion` | 466 | ⚖️ **norma** |
| `guia` | 416 | ⚖️ **norma** |
| `EVIDENCIA_OBSERVACIONAL` | 411 | 📋 instrumento / evidencia |
| `resolucion` | 408 | ⚖️ **norma** |
| `convenio_internacional` | 255 | ⚖️ **norma** |
| `informe_rendicion` | 114 | 📋 instrumento / evidencia |
| `resolucion_local` | 100 | ⚖️ **norma** |
| `instructivo` | 89 | ⚖️ **norma** |
| `plan_gobierno` | 55 | 📋 instrumento / evidencia |
| `acuerdo` | 44 | ⚖️ **norma** |
| `reforma` | 20 | ⚖️ **norma** |

### ⚠️ Tres hallazgos que condicionan todo el refactor

**1 · La tabla se llama `normativa_corpus` y contiene dos universos.** 8148 fragmentos son norma; 4999 son instrumentos de gestión y evidencia —PDOT, POA, PAC, PP, informes de rendición—. Es decir: **`BM-01` y `BM-03` conviven en la misma tabla**, y el nombre induce a tratarlos igual. No lo son: la norma tiene precedencia sobre el diseño; la evidencia, no.

**2 · 🔴 NO EXISTE COLUMNA DE VIGENCIA.** Las únicas columnas temporales son `ingestado_at` e `ingestado_por` — **cuándo se cargó, no cuándo rige**. El corpus no puede distinguir:

```
  NORMA VIGENTE  ·  REFORMADA  ·  DEROGADA  ·  HISTÓRICA
```

> Y esto es grave para un sistema cuya `Regla de Oro 3` dice **«sin norma verificada, no hay dato»**: hoy el corpus puede devolver un artículo derogado con la misma autoridad que uno vigente, y nada en el esquema lo impide.

**3 · `document_class` y `authority_level` están vacías en 10.618 de 13.147 fragmentos (81 %)**.

La jerarquía normativa formal **no está poblada** para la gran mayoría del corpus —Constitución y COOTAD incluidos—. Existe un campo `jerarquia` que sí está completo: **dos campos para lo mismo, uno lleno y otro vacío.** Es el patrón que `011-C2` encontró en `C_i`, repetido en el esquema de datos.

### Lo que `BM-01` necesita y hoy no tiene

| Atributo | Estado |
|---|---|
| identificador · sigla · nombre | ✅ |
| jerarquía | 🟡 duplicada: `jerarquia` llena, `authority_level` vacía |
| `sha256` y trazabilidad al archivo | ✅ |
| dominios QUIRA asociados | ✅ `dominios_quira` |
| **vigencia temporal** | 🔴 **ausente** |
| **estado jurídico** (vigente/reformada/derogada) | 🔴 **ausente** |
| **separación norma ↔ instrumento** | 🔴 **ausente** |
| institución emisora | 🟡 `source_entity`, parcial |
| relaciones entre normas | 🔴 ausente en esta tabla |

⚠️ Nada de esto se corrige aquí. Se **registra** — y `BM-01` pasa a ser un frente propio del refactor, no un detalle de `Q1`.

## 1 · Cuatro inventarios, cuatro cardinalidades

**Está prohibido sumar archivos con constructos.** Un archivo es un artefacto; una hoja es una estructura interna de un artefacto; un dominio es una entidad ontológica; un índice es un constructo metodológico; un factor es una dimensión de un constructo. No están en el mismo nivel, y decir «QUIRA tiene N cosas» sería falsear.

### ① Inventario FÍSICO · archivos del repositorio

**Regla de conteo:** se recorre cada raíz recursivamente con su extensión; se excluyen `historico` · `.git` · `__pycache__` · `.venv` · `node_modules`. Las filas en *cursiva* **no suman**: están contenidas en la de arriba.

| Artefactos | Raíz · patrón | Cuenta |
|---|---|---:|
| documentos de canon | `docs/**/*.md` | **412** |
|   ↳ de los cuales, `ADR` | `docs/adr` | *44* |
|   ↳ de los cuales, `PCD` | `docs/pcd` | *7* |
| reglas de negocio | `docs/brn/*.yaml` | **30** |
| gobernanza | `governance/**/*.md` | **23** |
| marco teórico | `marco_teorico/*.md` | **3** |
| módulos de aplicación | `app/**/*.py` | **104** |
| páginas de interfaz | `quira_pages/*.py` | **61** |
| scripts | `scripts/**/*.py` | **175** |
| pruebas | `tests/test_*.py` | **46** |
| snapshots de datos | `data/**/*.json` | **470** |
| | **TOTAL FÍSICO (suma de las filas en negrita)** | **1324** |

### ② Inventario DOCUMENTAL · el canon

| | Cuenta |
|---|---:|
| `ADR` | 44 |
| `PCD` | 7 |
| doctrina con verificador | 28 |
| deudas registradas | 14 |

### ③ Inventario ONTOLÓGICO · qué existe

| | Cuenta |
|---|---:|
| dominios | 13 |
| macroejes | 4 |
| entidades del holding municipal | 5 |
| unidades orgánicas (Res. 040-2025) | 20 |

### ④ Inventario METODOLÓGICO · qué se calcula

| | Cuenta |
|---|---:|
| índices | 12 |
| factores del ICPI | 6 |
| reglas de negocio | 30 |
| hojas del Gold Master | 123 |
| metas del universo operacional | 25 de 66 |

### ⑤ Inventario NORMATIVO · `BM-01`

| | Cuenta |
|---|---:|
| fragmentos vectorizados | 13147 |
| normas distintas | 94 |
| tipos documentales | 16 |
| tablas en el esquema | 27 |

## ★ 2 · Las cinco categorías · la regla que impide dañar lo válido

**Ninguna pieza del ecosistema se toca antes de clasificarla.**

| | Categoría | Qué es | Qué se hace con ella |
|---|---|---|---|
| 🏛️ | **HISTÓRICO** | existió y ya no opera | se PRESERVA como trazabilidad — nunca se borra |
| ⚖️ | **NORMATIVO VIGENTE** | lo fija una norma en vigor | se ACATA mientras siga vigente — no es decisión de diseño |
| 🔬 | **EMPÍRICAMENTE ÚTIL** | funciona y hay evidencia de que funciona | se CONSERVA si supera validación — y hay que poder mostrar cuál |
| 🔧 | **DECISIÓN DE DISEÑO ANTIGUA** | se eligió, no se dedujo; y nadie escribió por qué | queda ABIERTA a rediseño — ni válida ni inválida por antigüedad |
| 📜 | **SUPERADO METODOLÓGICAMENTE** | fue correcto en su momento y el conocimiento actual lo desplazó | se conserva como ANTECEDENTE, no como regla |

**🏛️ HISTÓRICO** — `SIAP` · `QUADRUM` · `TERRA` · `ICPI_v1` · versiones superadas

**⚖️ NORMATIVO VIGENTE** — `R_i`↔COOTAD 54-55 · `V_i`↔LOTAIP 7 · `T_i`↔COPFP 115-117 + Acuerdo 067 MEF · `P_i`↔COPFP 54

**🔬 EMPÍRICAMENTE ÚTIL** — producto lógico de `V_i` · jerarquía de fuentes de `T_i` · `auditabilidad` como propiedad

**🔧 DECISIÓN DE DISEÑO ANTIGUA** — pesos `0,10/0,15/0,05/0,50` · piso `0,50` · residencia de los índices · escala AVEP

**📜 SUPERADO METODOLÓGICAMENTE** — `C_i` = imputabilidad orgánica · «Cumplimiento Institucional» como nombre del ICPI

### ⚠️ `NO_DETERMINADO` no es una sexta categoría

Es un **estado de evidencia** transversal, y la distinción evita un error grave. Una pieza tiene **categoría** y **estado** a la vez:

| Pieza | Categoría | Estado de evidencia |
|---|---|---|
| `Constitución Art. 233` | ⚖️ normativo vigente | ✅ fuente primaria localizada |
| peso `C_i = 0,20` | 🔧 decisión de diseño | ❓ justificación no determinada |
| producto lógico de `V_i` | 🔬 empíricamente útil | ⚠️ evidencia insuficiente |

> ### `NO_DETERMINADO` significa «no hemos demostrado todavía la razón o la condición». **Nunca significa «la razón no existe»** — y por tanto **nunca autoriza a eliminar**.

Sin esta separación, el refactor derivaría al silogismo falso: *«no está justificado → se puede quitar»*. `DOC-027` lo prohíbe.

### La corrección que esta tabla incorpora

Una versión anterior de `DOC-027` decía:

> ~~«Donde no hay razón documentada, no hay nada que respetar.»~~

**Empujaba al extremo contrario** del sesgo conservador que venía a corregir. La formulación rigurosa es:

> Donde no existe justificación documental de una decisión de diseño, esa decisión **no adquiere autoridad metodológica por antigüedad**; su permanencia debe **evaluarse nuevamente** frente al fenómeno, la teoría, la evidencia, la norma y la arquitectura actual.

Una decisión antigua sin justificación **no es automáticamente incorrecta**. Tampoco automáticamente correcta. Queda **abierta**, que es un estado distinto de ambos.

## ★ 3 · La máquina propone, la dirección ratifica

La `v1` decía que «la clasificación sea derivable». **Es insuficiente y peligroso**: automatizar una clasificación epistemológica la convierte en una caja negra nueva.

| Lo que la máquina SÍ puede hacer | Lo que NO puede decidir |
|---|---|
| detectar referencias a normas · `ADR` · nombres históricos | «esto es una decisión de diseño antigua» |
| detectar dependencias y referencias cruzadas | «esto está superado metodológicamente» |
| detectar qué código consume qué hoja | «esto es empíricamente útil» |
| detectar dónde aparece un índice o un término | cualquier clasificación **epistemológica** |

Por eso cada pieza lleva **dos campos**:

```
  classification_candidate   ← lo propone el script
  classification_status      ← lo ratifica la dirección
                                PENDIENTE · PROPUESTO · VERIFICADO
```

| Pieza | Candidato automático | Estado |
|---|---|---|
| `Constitución Art. 233` | ⚖️ normativo vigente | **VERIFICADO** |
| `ICPI_v1` | 🏛️ histórico | **VERIFICADO** |
| peso `C_i = 0,20` | 🔧 decisión antigua | **PENDIENTE** · `011-C3` |
| `auditabilidad` | 🔬 empíricamente útil | **PENDIENTE** |
| `C_i` = imputabilidad orgánica | 📜 superado | **PROPUESTO** |

## ★ 4 · `auditoría` · la prueba patrón de migración semántica

Javo puso el ejemplo *«quitar la palabra auditoría de la documentación»* para fijar el NIVEL del refactor. Esta dirección **empezó a ejecutarlo**. Javo lo detuvo. Lo medido antes de parar:

```
  «auditoría» →  609 ocurrencias  ·  233 archivos
```

Y **no son la misma palabra**:

```
                        cadena: auditor*
                              │
     ┌──────────────┬─────────┼─────────┬──────────────┐
     ▼              ▼         ▼         ▼              ▼
 auditoría CGE   GM-Ω     QUIRA     auditable    auditabilidad
     │          «audit.»  «audita»      │              │
  ⚖️ NORMA      🔧 TERMIN. 🔧 TÉRMINO  🔬 PROPIEDAD  🔬 CONCEPTO
  referencia    de trabajo INCORRECTO   preservar     evaluar
  legal ·       revisar    sustituir    en código     en teoría
  INTOCABLE
```

> ### El gate que esto obliga a construir
>
> **Ninguna migración léxica puede alterar una referencia normativa vigente por el solo hecho de compartir una cadena de caracteres con un término que se desea reemplazar.**

Un reemplazo sin clasificación previa **habría borrado artículos de ley**. Ocurrió en el primer minuto del primer ejemplo, y por eso este caso deja de ser anécdota: es el **primer test de `Q1`**.

Y hay algo que conviene decir: **`governance/BOOT.md` declara desde el 2026-08-05 que QUIRA «⛔ NO es auditoría ni observatorio»**. La regla existía; el vocabulario del repositorio no la siguió. Es el mismo patrón que `DOC-013`, y es la razón de fondo de este refactor.

## ★ 5 · FONDO y FORMA

```
                        QUIRA
              ┌───────────┴───────────┐
            FONDO                   FORMA
     ¿QUÉ gestiona el GAD?    ¿CÓMO lo gestiona?
              │                       │
     dominios sectoriales    capacidades transversales
              │                       │
   salud · agua · vialidad    planificación · ejecución
   ambiente · riesgos ·       eficiencia · contratación
   desarrollo económico       transparencia · trazabilidad
                              coordinación · responsabilidad
```

> **La misma gestión se observa a la vez desde el fondo y desde la forma.** Eso es lo que hoy no se puede hacer, y es la razón por la que hay indicadores transversales viviendo dentro de dominios sectoriales.

### El caso que lo prueba · `IED`

Javo propuso *«establecer eficiencia directiva»*. **Ya existe**: el `IED` desglosa metas del PDOT por dirección del Estatuto Orgánico (`H17`, `H30`). Lo que no tiene es sitio: su dominio, su rol y su pregunta están los tres `POR_DECLARAR`.

En el esquema se ve por qué: **`IED` no pertenece a ningún dominio sectorial**. «¿Qué tan eficientemente funciona la dirección responsable?» aplica a Salud, a Obras Públicas y a Financiera por igual. Es **forma**, y hoy no hay dónde ponerla.

| Nivel | Unidad | Pregunta |
|---|---|---|
| **sectorial** | una competencia | ¿qué resultados está gestionando? |
| **organizacional** | una dirección | ¿cómo funciona esa unidad? |
| **transversal** | el gobierno municipal | ¿es coherente, eficiente, trazable y coordinado el sistema completo? |

## 6 · El ICPI · cuatro destinos, ninguno decidido

| | Destino | Qué significaría |
|---|---|---|
| **A** | se **conserva** | supera `C4` y la teoría justifica sus dimensiones |
| **B** | se **refactoriza** | mismo fenómeno, otros factores, otra semántica, otra escala, otra residencia |
| **C** | se **descompone** | congruencia programática · ejecución financiera · trazabilidad · responsabilidad institucional · eficiencia directiva · desempeño operativo — y un **panel multidimensional** en lugar de un índice único |
| **D** | se **depreca** | `ICPI_v1` queda para trazabilidad y deja de ser el indicador operativo principal |

**Ninguno de los cuatro es un fracaso.** `D` tampoco: sería evolución metodológica.

### Y por qué el nombre va al final

```
  1. ¿qué fenómeno sobrevive a C4?
  2. ¿cuál es su unidad?
  3. ¿cuál es su arquitectura?
  4. ¿cuál es su residencia?
  5. …y recién entonces: ¿cómo se llama?
```

> Empezar por el nombre sería hacer **branding de un concepto que todavía se está rediseñando**.

## 7 · Los diez ejes · se auditan simultáneamente

| | Eje | Pregunta | Estado hoy |
|---|---|---|---|
| **A** | Ontología | ¿qué cosas existen en QUIRA? | Constitución §CAPA 0 · `T1`/`T2` cerrados |
| **B** | Taxonomía | ¿cómo se llaman y cómo se agrupan? | `T1`-`T6` · 43 nombres · `T6` espera al dictamen |
| **C** | Metodología | ¿qué significa cada indicador? | `011-C2` ✅ los 6 factores · faltan los otros 11 índices |
| **D** | Datos | ¿qué fuente alimenta cada dato? | `004` matriz de procedencia · 150 celdas |
| **E** | Gold Master | ¿cómo se representa canónicamente? | ⚠️ CONGELADO hasta `011-C4` |
| **F** | Código | ¿la implementación coincide con la ontología? | `DOC-016` |
| **G** | Dominios | ¿cada indicador vive donde corresponde? | `R0`/`R1`/`R2` · 23 de 48 celdas `POR_DECLARAR` |
| **H** | Frontend | ¿la interfaz representa la arquitectura? | sin frente · Bloomberg Firewall vigente |
| **I** | Narrativa | ¿QUIRA explica bien lo que mide? | sin frente · es el salto de dashboard a inteligencia pública |
| **J** | Escalabilidad LATAM | ¿qué es Ecuador y qué es generalizable? | `010` · siguiente |

## ★ 8 · La secuencia · `010` alimenta el diseño, no lo cierra

```
                    CARTA v2  (este documento)
                          │
               ┌──────────┴──────────┐
          INVENTARIO             010 LATAM
       físico · normativo    ¿qué es Ecuador y
       ontológico · metod.    qué es transferible?
               └──────────┬──────────┘
                          ▼
                MATRIZ DE CLASIFICACIÓN
                 candidato → ratificado
                          ▼
                    R0 · R1 · Q1
                          ▼
                       011-C4
                          ▼
               DECISIÓN METODOLÓGICA
                          ▼
                MIGRACIÓN CONTROLADA
                          ▼
                  GOLD MASTER vNEXT
```

**`010` y el inventario no son tareas independientes.** `010` necesita saber qué se pretende generalizar, y la carta necesita que `010` le diga qué es específico de Ecuador, qué es conceptual, qué es transferible y qué exige recalibración nacional.

> ### Y una hipótesis que `010` debe poner a prueba
>
> El producto exportable de QUIRA **puede no ser el ICPI**, sino la arquitectura `NORMA + EVIDENCIA + ONTOLOGÍA + METODOLOGÍA → INTELIGENCIA PÚBLICA` — donde cada país sustituye su corpus normativo, sus fuentes institucionales y ciertos parámetros. Si se confirma, cambia la estrategia LATAM entera.

| 🟢 Se puede hacer AHORA | 🔴 CONGELADO hasta `C4` |
|---|---|
| inventario · grafo de dependencias | Gold Master |
| clasificación candidata · análisis léxico | fórmula vigente · `B33` |
| `010` · `R0` · `R1` | valores históricos |
| análisis de dominios · frontend · narrativa | residencia actual de los índices |
| matriz FONDO/FORMA · diseño de gates y migración | nombres canónicos con función metodológica |
| pruebas que **no** modifican el estado canónico | código que produce el baseline · snapshots |

> **Se puede estudiar el edificio entero sin mover una pared.**

## 9 · Las reglas de la migración

> ### `DOC-029` · REGLA MAESTRA DE REARQUITECTURA
>
> **Ningún cambio se ejecuta directamente sobre el ecosistema canónico. Primero se OBSERVA, después se CLASIFICA, luego se JUSTIFICA, después se DISEÑA LA MIGRACIÓN, y sólo entonces se EJECUTA.**
>
> Es la diferencia entre hacer limpieza y hacer una rearquitectura gobernada.

| # | Regla | De dónde sale |
|---|---|---|
| 1 | **Clasificar antes de tocar** | esta carta · §2 |
| 2 | **La norma tiene precedencia sobre el diseño** | Eje 0 |
| 3 | **El basónimo no cambia** — el identificador estable sobrevive al renombrado | `DOC-015` |
| 4 | **Nombre técnico ≠ nombre de presentación** | `DOC-014` · `Regla de Oro 2` |
| 5 | **Anti-inflación**: si sólo renombra, no entra | `Regla de Oro 7` |
| 6 | **Ningún cambio nace en Python** | `Regla de Oro 9` · `DOC-016` |
| 7 | **Lo que se retira no se borra**: pasa a `HISTÓRICO` con su linaje | `DOC-013` |
| 8 | **Continuidad histórica ≠ continuidad metodológica** | `DOC-028` |
| 9 | **`NO_DETERMINADO` nunca autoriza a eliminar** | `DOC-027` |
| 10 | **Cada dominio cierra con su `PCD`** | `Regla de Oro 8` |

## Lo que esta carta NO hace

- **No decide el destino del ICPI.** Cuatro opciones, `011-C4` elige.
- **No renombra nada.** El nombre es el último paso.
- **No toca el Gold Master** ni el corpus normativo.
- **No clasifica todavía** ninguna pieza: establece **cómo** se clasifica y **quién ratifica**.

> ### El propósito, en una línea
>
> `GM-Ω` no existe para legitimar el pasado ni para destruirlo, sino para **ponerlo en su lugar**: el pasado como **linaje**, la norma como **restricción**, la evidencia como **fundamento**, la teoría como **justificación** — y el diseño como **decisión presente**.

---
*QUIRA-NEXT · Carta de Rearquitectura `v2` · QNEXT-INV-2026-09-05 · commit `b5035ad` · el Gold Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
