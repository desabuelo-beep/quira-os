# GM-Ω · TRANSFERIBILIDAD LATAM  `010`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/transferibilidad_latam.py`. Las **dependencias** se miden del repositorio; la **clasificación funcional** se declara, porque es un juicio.

> ### La pregunta
> ¿Qué elementos de QUIRA constituyen **arquitectura generalizable de inteligencia pública** y cuáles son **soluciones contingentes** derivadas de la historia normativa, institucional, documental y metodológica del Ecuador?

⚠️ **No es «¿puede QUIRA aplicarse en otro país?».** Esa pregunta se responde con un sí vacío. La útil separa dos cosas:

> **QUIRA no debe exportar Ecuador. Debe poder exportar su ARQUITECTURA y adaptar su CORPUS.**

## ★ La regla que ordena esta etapa

| | |
|---|---|
| La **presencia** de una norma ecuatoriana | **NO** demuestra que un componente sea contingente. Demuestra que existe un **acoplamiento normativo** que hay que identificar |
| La **ausencia** de cita normativa | **NO** demuestra que un componente sea universal |

> ### La máquina detecta dependencia; la dirección determina significado

Sin esta regla, `010` repetiría `DOC-009` en versión automatizada: **detectar → clasificar → convertir la detección en ontología**. Un documento puede citar la Constitución ecuatoriana sólo para **ilustrar un caso de implementación** de un principio generalizable — y ese matiz puede ser uno de los hallazgos de esta etapa.

## Las cuatro categorías

| | Categoría | Qué es | ¿Qué habría que cambiar para desplegarlo? |
|---|---|---|---|
| 🟢 **A** | NÚCLEO ARQUITECTÓNICO | su función no depende de ninguna norma ecuatoriana concreta | *no tendría que cambiar* |
| 🔵 **B** | ADAPTADOR NORMATIVO | la FUNCIÓN permanece; cambia el corpus jurídico que la alimenta | *sólo cambiar el corpus normativo* |
| 🟠 **C** | SEDIMENTACIÓN HISTÓRICA | existe porque QUIRA nació en una trayectoria concreta | *cambiar ontología, unidad, fuente y lógica* |
| 🟣 **D** | DECISIÓN DE DISEÑO CONTINGENTE | ni normativa ni histórica: se eligió, y podría haberse elegido otra | *⚠️ lo somete a prueba `011-C4`* |

⚠️ **La categoría `D` evita una falsa dicotomía**, y la añadió el colega. Algo puede **no ser normativo ni histórico** y aun así no ser arquitectura generalizable: «elegimos esta fórmula porque en ese momento parecía adecuada» no es Ecuador, pero tampoco es universal. Sin `D`, toda decisión propia se colaría como núcleo **por el mero hecho de no citar una norma**.

### El test que decide la categoría

```
  ¿qué tendría que cambiar para desplegarlo en otro país?

    «nada»                                    → 🟢 A núcleo
    «sólo el corpus normativo»                → 🔵 B adaptador
    «ontología, unidad, fuente y lógica»      → 🟠 C sedimentación
    «depende de si la decisión era necesaria» → 🟣 D contingente
```

## ★ La matriz de componentes

| Componente | Función | | ¿Qué habría que cambiar? |
|---|---|---|---|
| **Ingesta de fuentes** | incorporar documentos y datos al corpus | 🟢 `A` | los conectores concretos |
| **Trazabilidad / provenance** | saber de dónde viene cada afirmación · `MNT_UUID` · cadena de autoridad | 🟢 `A` | nada |
| **Los 8 estados de la evidencia** | distinguir «no existe» de «no pude obtener» de «falló» · ★ probablemente lo más exportable del constructo | 🟢 `A` | nada |
| **Escalera prueba↔verificador** | graduar qué acredita cada artefacto · el escalón 7 —lo leído ≠ la fuente— es universal | 🟢 `A` | nada |
| **Separación norma→evidencia→inferencia** | no confundir lo que la ley manda con lo que ocurrió ni con lo que se concluye · `DOC-030` · Eje 0 de la carta | 🟢 `A` | nada |
| **Gold Master como estado canónico** | una sola fuente del número · el formato Excel es contingente; la función no | 🟢 `A` | nada |
| **Versionado y hash-chain** | que un resultado sea reproducible | 🟢 `A` | nada |
| **Motor de congruencia multiplicativa** | un eslabón roto anula la cadena · ★ `011-C4` decide si es necesario | 🟣 `D` | ⚠️ por determinar |
| **Producto lógico de `V_i`** | un silo en cero anula la meta · regla fuerte, sin justificación cuantitativa | 🟣 `D` | ⚠️ por determinar |
| **Los cuatro silos de verificación** | contrastar una afirmación contra fuentes independientes · la función es universal; `SERCOP`/`eSIGEF`/`LOTAIP`/`CPCCS` no | 🔵 `B` | qué sistemas ocupan cada silo |
| **`P_i` peso presupuestario** | ponderar por magnitud del compromiso · `COPFP 54` ↔ su equivalente | 🔵 `B` | el artículo que lo funda |
| **`R_i` relevancia normativa** | ponderar por jerarquía de la competencia · `COOTAD 54-55` ↔ su equivalente | 🔵 `B` | el catálogo de competencias del país |
| **`T_i` materialización temporal** | medir devengo, no compromiso · `COPFP 115-117` + Acuerdo 067 ↔ equivalente | 🔵 `B` | la norma que define el devengado |
| **`V_i` inmutabilidad documental** | exigir evidencia en varios silos | 🔵 `B` | las leyes de transparencia y contratación |
| **`E_i` fricción de autonomía** | ajustar por modalidad de ejecución | 🔵 `B` | el régimen de entidades adscritas |
| **`C_i` calidad de proceso** | descontar por infracciones verificadas · ⚠️ su semántica cerró en `011-C2`; sus parámetros siguen abiertos | 🔵 `B` | el catálogo de infracciones del país |
| **Pesos `0,15 / 0,10 / 0,05`** | graduar la severidad de cada infracción · sin fundamento cuantitativo (`C3-R`) | 🟣 `D` | ⚠️ por determinar |
| **Piso `C_i ≥ 0,50`** | impedir que una infracción anule la meta · sin fundamento cuantitativo (`C3-R`) | 🟣 `D` | ⚠️ por determinar |
| **Escala AVEP** | traducir un número a un juicio institucional · baremo propio · dos versiones divergen (`D-012`) | 🟣 `D` | ⚠️ por determinar |
| **Los 13 dominios** | organizar el objeto observado · nacieron del caso Montecristi | 🟠 `C` | la estructura de competencias del país |
| **Universo de 25 metas** | acotar la muestra operacional · `ADR-036` · `D-001` | 🟠 `C` | todo: es una decisión del caso |
| **`SAT` I-VI** | alertar sobre patrones de riesgo · la función viaja | 🔵 `B` | los artículos que fundan cada alerta |
| **Corpus normativo vectorizado** | poder afirmar que una obligación existe · ★ `BM-01` · la estructura viaja, el contenido se sustituye | 🔵 `B` | el corpus entero del país |
| **Estatuto Orgánico como fuente de `E_i`/`C_i`** | imputar cada meta a una unidad responsable · `Res. 040-2025` es la instancia | 🔵 `B` | el instrumento equivalente |

| Categoría | Componentes |
|---|---:|
| 🟢 **A** NÚCLEO ARQUITECTÓNICO | 7 |
| 🔵 **B** ADAPTADOR NORMATIVO | 10 |
| 🟠 **C** SEDIMENTACIÓN HISTÓRICA | 2 |
| 🟣 **D** DECISIÓN DE DISEÑO CONTINGENTE | 5 |

## ★ Función ≠ instancia · el corazón de `010`

Lo que hace transferible a un adaptador normativo es que su **función** existe en cualquier Estado, aunque la **institución** que la encarna sea ecuatoriana:

| Instancia ecuatoriana | Menciones | Función generalizable |
|---|---:|---|
| `eSIGEF` | 490 | sistema de ejecución presupuestaria del Estado |
| `CPCCS` | 443 | órgano de participación ciudadana y control social |
| `SERCOP` | 421 | portal nacional de contratación pública |
| `CNE` | 291 | autoridad electoral |
| `INEC` | 262 | instituto nacional de estadística |
| `SIGAD` | 258 | sistema de autorreporte de cumplimiento del gobierno local |
| `SNP` | 118 | órgano nacional de planificación |
| `CGE` | 84 | entidad fiscalizadora superior |
| `MEF` | 25 | ministerio de finanzas |
| `AME` | 18 | asociación de municipalidades |

| Norma ecuatoriana | Menciones | Materia generalizable |
|---|---:|---|
| `LOTAIP` | 590 | transparencia y acceso a la información |
| `COOTAD` | 486 | régimen de competencias del gobierno local |
| `LOPC` | 191 | participación ciudadana |
| `COPFP` | 137 | planificación y finanzas públicas |
| `LOSNCP` | 73 | contratación pública |
| `LOSEP` | 53 | servicio público |
| `COPLAFIP` | 33 | planificación y finanzas públicas |
| `NCI` | 27 | normas de control interno |

Y las **30 reglas de negocio** de `docs/brn/` son el caso más nítido: cada una declara la norma que la funda. **Esa estructura es el adaptador**: la regla viaja, el artículo se sustituye.

> ### El acoplamiento no es un defecto: es lo que hace verificable al sistema
>
> Un motor que no cite norma no sería más universal — sería **menos auditable**. La `Regla de Oro 3` («sin norma verificada, no hay dato») exige el acoplamiento. Lo que `010` separa no es «con norma» de «sin norma», sino **norma como parámetro** de **norma como supuesto estructural**.

## ★ La hipótesis que `010` tenía que poner a prueba

La carta `Q0` la formuló así:

> El producto exportable de QUIRA **puede no ser el ICPI**, sino la arquitectura `NORMA + EVIDENCIA + ONTOLOGÍA + METODOLOGÍA → INTELIGENCIA PÚBLICA`.

Lo que la matriz muestra:

| | |
|---|---|
| componentes que **no tendrían que cambiar** | 7 |
| …y **ninguno de ellos es el ICPI** | ✅ |

Los candidatos a núcleo son de otra naturaleza: **los 8 estados de la evidencia**, la **escalera prueba↔verificador**, la **separación norma→evidencia→inferencia**, la **trazabilidad**, el **estado canónico único**. Ninguno depende de qué mida el índice.

> ### `010` no confirma ni refuta la hipótesis: la hace formulable
>
> Que el núcleo identificado sea **metodológico y no métrico** es **compatible** con la hipótesis. No la demuestra: para eso haría falta un segundo caso —otro país, u otro municipio con otro marco— y hoy no existe. `DOC-019`: un caso no autoriza la regla general.

## Lo que `010` entrega a `011-C4`

| Hallazgo | Consecuencia para el dictamen |
|---|---|
| **5 componentes** caen en `D` — decisión de diseño contingente | son exactamente los que `C4` tiene que juzgar, y ahora están **enumerados** |
| la multiplicatividad está en `D`, no en `A` | **no se puede defender como necesaria por ser transferible**: su transferibilidad depende de que la decisión fuera necesaria, que es lo que se juzga |
| **10 componentes** son adaptadores | el acoplamiento normativo es **denso y explícito** — y eso es una fortaleza auditable, no una atadura |
| **2 componentes** son sedimentación | incluidos los 13 dominios y el universo de 25: **`R0` y `v2` heredan esto** |

> ### Y la advertencia con la que se entra a `C4`
>
> `010` no se hizo para demostrar que QUIRA es universal. La pregunta no era si todo QUIRA es transferible, sino **qué parte merece llamarse arquitectura** y qué parte debe reconocerse como adaptación, sedimentación o decisión contingente. Un `010` que devolviera «todo es núcleo» habría sido un `010` mal hecho.

## Dictamen de `010` · por grado de certeza

| Afirmación | Estado |
|---|---|
| El acoplamiento normativo del motor es explícito y localizable | **DEMOSTRADO** · norma declarada componente a componente |
| La función de cada silo existe con independencia de la institución ecuatoriana que la ocupa | **DEMOSTRADO** |
| Los candidatos a núcleo son metodológicos, no métricos | **DEMOSTRADO** sobre la matriz declarada |
| El ICPI no está entre ellos | **DEMOSTRADO** |
| La arquitectura es efectivamente transferible a otro país | ⬜ **NO DETERMINABLE** · exigiría un segundo caso (`DOC-019`) |
| Los componentes `D` son o no necesarios al constructo | ⬜ **FUERA DE ALCANCE** · `011-C4` |

> ### GM-Ω-010 — CERRADO COMO SEPARACIÓN ARQUITECTURA / CONTINGENCIA
>
> Se clasificaron los componentes del constructo en **núcleo**, **adaptador normativo**, **sedimentación histórica** y **decisión de diseño contingente**, con el criterio explícito de qué habría que cambiar para desplegarlo en otro país.
>
> **No demuestra** que QUIRA sea transferible: eso requiere un segundo caso. Demuestra **dónde está el acoplamiento** y **qué parte del sistema no depende de él**.

---
*GM-Ω-ICPI-010 · 24 componentes clasificados · 30 reglas de negocio · el Gold Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
