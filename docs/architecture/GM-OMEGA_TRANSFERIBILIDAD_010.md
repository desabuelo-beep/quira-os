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

### ★ Las cuatro NO son categorías del mismo tipo

| | Qué tipo de afirmación es |
|---|---|
| 🟢 `A` | una **propiedad arquitectónica** |
| 🔵 `B` | una arquitectura **parametrizada por un contexto normativo** |
| 🟠 `C` | una **procedencia** histórica |
| 🟣 `D` | ⚠️ **una incertidumbre sobre la necesidad del diseño** |

`A`, `B` y `C` son clasificaciones **estructurales**. `D` **no lo es**: es un estado de duda. Y de ahí sale la lectura que `011-C4` tiene prohibido hacer:

| Lectura | Veredicto |
|---|---|
| `D` = incorrecto | 🔴 **falso** |
| `D` = debe eliminarse | 🔴 **falso** |
| **`D` = no puede recibir presunción de necesidad arquitectónica** | ✅ |

> Es la misma disciplina que `DOC-027` aplicada a la arquitectura: no validado **no es** invalidado.

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
| `eSIGEF` | 492 | sistema de ejecución presupuestaria del Estado |
| `CPCCS` | 445 | órgano de participación ciudadana y control social |
| `SERCOP` | 423 | portal nacional de contratación pública |
| `CNE` | 292 | autoridad electoral |
| `INEC` | 263 | instituto nacional de estadística |
| `SIGAD` | 259 | sistema de autorreporte de cumplimiento del gobierno local |
| `SNP` | 119 | órgano nacional de planificación |
| `CGE` | 85 | entidad fiscalizadora superior |
| `MEF` | 26 | ministerio de finanzas |
| `AME` | 19 | asociación de municipalidades |

| Norma ecuatoriana | Menciones | Materia generalizable |
|---|---:|---|
| `LOTAIP` | 592 | transparencia y acceso a la información |
| `COOTAD` | 488 | régimen de competencias del gobierno local |
| `LOPC` | 192 | participación ciudadana |
| `COPFP` | 140 | planificación y finanzas públicas |
| `LOSNCP` | 74 | contratación pública |
| `LOSEP` | 54 | servicio público |
| `COPLAFIP` | 34 | planificación y finanzas públicas |
| `NCI` | 28 | normas de control interno |

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

### ⚠️ La formulación exacta de este resultado

Hay una diferencia que no puede perderse:

| Afirmación | ¿Autorizada? |
|---|---|
| «en el caso analizado, los componentes clasificados como `A` son metodológicos» | ✅ sí — es el resultado de la clasificación |
| «el núcleo transferible de QUIRA es metodológico» | 🔴 **no** — eso exigiría el segundo caso |

La conclusión queda congelada así:

> `010` identifica **candidatos a núcleo arquitectónico** cuya función no presenta, **en el caso analizado**, dependencia necesaria de una instancia normativa o institucional ecuatoriana. **Su generalización efectiva permanece pendiente de validación externa.**

Es más fuerte epistemológicamente, porque **no convierte el resultado de una clasificación interna en evidencia externa de transferibilidad**.

> ### `010` no confirma ni refuta la hipótesis: la hace formulable
>
> Que los candidatos a núcleo sean **metodológicos y no métricos** es **compatible** con la hipótesis. No la demuestra: para eso haría falta un segundo caso —otro país, u otro municipio con otro marco— y hoy no existe. `DOC-019`: un caso no autoriza la regla general.

⚠️ Y hay una **hipótesis arquitectónica emergente** que conviene nombrar sin convertirla en doctrina:

> QUIRA podría ser una **arquitectura de inteligencia pública que admite múltiples modelos métricos**, en lugar de una arquitectura construida alrededor de un único índice.

Emergente significa exactamente eso: **todavía no es un hallazgo**. Se registra para que `C4` pueda considerarla, no para que la dé por buena.

## Lo que `010` entrega a `011-C4`

| Hallazgo | Consecuencia para el dictamen |
|---|---|
| **5 componentes** caen en `D` — decisión de diseño contingente | son exactamente los que `C4` tiene que juzgar, y ahora están **enumerados** |
| la multiplicatividad está en `D`, no en `A` | **no se puede defender como necesaria por ser transferible**: su transferibilidad depende de que la decisión fuera necesaria, que es lo que se juzga |
| **10 componentes** son adaptadores | el acoplamiento normativo es **denso y explícito** — y eso es una fortaleza auditable, no una atadura |
| **2 componentes** son sedimentación | incluidos los 13 dominios y el universo de 25: **`R0` y `v2` heredan esto** |

### ★ Las cinco decisiones `D`, con la pregunta que `C4` debe hacerle a cada una

`C4` ya no pregunta vagamente «¿está bien el ICPI?». Somete a prueba **cinco decisiones enumeradas**:

#### `D1` · Arquitectura multiplicativa

`J_i = P_i × R_i × V_i × E_i × T_i × C_i`

> ¿Existe razón **teórica, normativa o empírica** suficiente para que la degradación de un componente reduzca **multiplicativamente** la contribución de una unidad?

⚠️ No basta con «así funciona el modelo».

#### `D2` · `V_i` como factor multiplicativo

> ¿La ausencia o insuficiencia documental debe poder **anular** la contribución de una unidad al índice?

Aquí hay una tensión epistemológica de primer orden, y toca la raíz del canon:

```
  «no tengo evidencia»  ≠  «el fenómeno no ocurrió»
```

Si `V=0` produce `J=0`, el índice mide **dos cosas a la vez**: la gestión **y** la capacidad de demostrarla documentalmente. Puede ser **intencional y legítimo** —un índice de congruencia bien podría querer eso—, pero entonces debe **demostrarse como elección metodológica**, no asumirse.

Y choca de frente con el principio rector: *«la ausencia de evidencia es un RESULTADO de auditoría, nunca autorización para inferir hechos»*. `C4` tiene que resolver si anular la meta es un resultado o una inferencia.

#### `D3` · Pesos de `C_i` — `0,15 / 0,10 / 0,05`

> ¿Por qué esos valores y no otros?

**No hay que volver a hacer genealogía.** `C3-R` ya cerró: están documentados, su fundamento cuantitativo no está determinado. `C4` pregunta sólo si existe **justificación metodológica suficiente para conservarlos**.

#### `D4` · Piso `C_i ≥ 0,50`

> ¿Qué propiedad del fenómeno justifica que **ninguna infracción** pueda reducir `C_i` por debajo de `0,50`?

⚠️ **El piso no es sólo un parámetro técnico.** Introduce una afirmación sustantiva sobre la relación entre infracción y desempeño: presupone que **incluso acumulando infracciones existe un mínimo de contribución institucional que debe preservarse**. Eso requiere fundamento.

#### `D5` · Escala `AVEP`

⚠️ **No se pregunta todavía «¿qué escala es correcta?».** Primero:

> ¿Qué **fenómeno** pretende representar `AVEP`?

Si transforma un valor continuo del ICPI en categorías cualitativas, hay que saber si esas categorías representan niveles de **integridad**, de **cumplimiento**, de **desempeño**, de **evidencia**, de **riesgo** — o si son **comunicación institucional**.

**No se puede validar una escala antes de declarar el fenómeno que pretende clasificar** (`DOC-012`: un porcentaje no tiene significado semántico por sí mismo). Y hay dos versiones divergentes conviviendo (`D-012`).

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

## ★ La regla que ordena toda la cadena

```
  007-B0   genealogía del constructo
  008      universo y correspondencia
  009      superficie contrafactual de gameabilidad
  011-C2   semántica de C_i
  011-C3   mecanismo y genealogía documental
  C3-R     cierre ante el corpus histórico adicional
  010      arquitectura frente a contingencia
  P6       reconciliación de artefactos y versiones
  011-C4   juicio metodológico de las decisiones D
```

Y la transición entre las tres últimas etapas es limpia:

| Etapa | Pregunta |
|---|---|
| `C3` | ¿**de dónde vino** la decisión? |
| `010` | ¿la decisión pertenece al **núcleo** o al **contexto**? |
| `C4` | ¿la decisión **merece permanecer**? |

> ### La historia explica. La transferibilidad clasifica. La metodología justifica. La evidencia decide.

Esa secuencia bloquea los **dos errores simétricos**, y ninguno está autorizado:

| Error | Por qué es falso |
|---|---|
| «es antiguo, por tanto debe conservarse» | `DOC-013` · QUIRA no conserva por herencia |
| «es contingente, por tanto debe eliminarse» | `DOC-027` · no validado no es invalidado |

> ### GM-Ω-010 — CERRADO COMO SEPARACIÓN ARQUITECTURA / CONTINGENCIA
>
> Se clasificaron los componentes del constructo en **núcleo**, **adaptador normativo**, **sedimentación histórica** y **decisión de diseño contingente**, con el criterio explícito de qué habría que cambiar para desplegarlo en otro país.
>
> **No demuestra** que QUIRA sea transferible: eso requiere un segundo caso. Demuestra **dónde está el acoplamiento** y **qué parte del sistema no depende de él**.

---
*GM-Ω-ICPI-010 · 24 componentes clasificados · 30 reglas de negocio · el Gold Master no se modificó · baseline 27,4582 % congelado · Dylus Lab © 2026*
