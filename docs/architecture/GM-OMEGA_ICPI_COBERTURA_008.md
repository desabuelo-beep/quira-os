# GM-Ω · ICPI — COBERTURA  `008`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/cobertura_icpi.py`.

> ### La regla en rojo de 008
> **No se corrige el 25/66.** Primero hay que saber cuál de los tres es: un error, una muestra estratégica prevista, o una muestra prevista pero mal ejecutada. Y la cifra madre **27,4582 % sigue congelada** durante todo el diagnóstico.

## ⚠️ Lo primero que encontró 008 fue que ya estaba respondido

`ADR-036 · Universo Operacional del Modelo`, **RATIFICADO el 2026-07-15**:

> «El Gold Master utiliza el **subconjunto estratégico de 25 metas del PDOT** como **universo operacional** para el cálculo del ICPI. No mide el PDOT completo (66 metas).» […] «las 25 existen todas en el PDOT — ninguna inventada. Es un subconjunto legítimo, no un error de carga.» […] «Ampliar el rango de 25 a 66 **no sería una corrección**.»

**El veredicto de las tres hipótesis, entonces:**

| Hipótesis | |
|---|---|
| `25/66 = error` | ❌ descartada — las 25 existen todas en el PDOT |
| `25/66 = muestra estratégica prevista` | ✅ **ratificada por ADR** |
| `25/66 = muestra mal ejecutada` | ⚠️ no descartable: falta el criterio |

Y una constancia metodológica: **este frente empezó a investigar algo que el canon ya había decidido.** Es la tercera vez en esta auditoría —`E_i`, el mapa índice→dominio, y ahora la cobertura—. La regla ya está escrita y hay que aplicarla antes, no después: **buscar donde debía estar, antes de declarar nada.**

## 1 · La aritmética no cuadra

| | |
|---|---:|
| Metas del PDOT (declaradas en el catálogo) | 66 |
| Metas del PDOT (filas reales del catálogo) | 66 |
| Metas en el motor (`H12` filas 6-30) | 25 |
| Metas en el catálogo «fuera del motor» | 50 |
| Diferencia simple `PDOT − motor` | 41 |
| Metas del PDOT que NO están en «fuera» (cruce por texto) | 16 |

⚠️ **`66 − 25 = 41`, pero el catálogo de exclusiones tiene 50.** Sobran **9**. Los tres artefactos —el PDOT extraído, el motor y el catálogo de exclusiones— no describen el mismo universo.

Y el cruce por texto lo confirma desde el otro lado: de las 66 metas del PDOT, **16 no aparecen en el catálogo de exclusiones** — pero el motor opera con 25. Faltan **9** por explicar.

Eso **no invalida el ADR-036**: la decisión de operar sobre 25 sigue en pie, y el ADR verificó que las 25 existen en el PDOT. Lo que dice es que **el complemento nunca se cuadró**: los catálogos que describen lo que queda fuera no reconstruyen el universo. Hoy no se puede afirmar con precisión qué metas quedan excluidas, y por tanto **tampoco publicar un porcentaje de cobertura**.

Las causas posibles son ordinarias —el catálogo de exclusiones puede incluir metas de otra versión del PDOT, o el cruce por texto puede fallar por redacciones que difieren— y **ninguna se elige aquí**: distinguirlas exige comparar meta a meta contra el documento, que es trabajo de curación, no de conteo.

## 2 · El denominador y su estado — con una corrección de fondo

Antes de dividir 25 entre 66, de dónde sale el 66:

- **Fuente**: `Plan Plurianual PDOT 2023-2027 GAD Montecristi.xlsx`
- **SHA256**: `09a2aaccca4bc90d829397a368254255…`
- **Carácter**: OFICIAL — obtenido del portal público del GAD. Javo (2026-09-03) corrigió la etiqueta anterior: «no remitido formalmente» describe el CANAL, no el carácter del documento. LOTAIP Art. 7 obliga a publicarlo y el canon de QUIRA sostiene que el portal es materialización de una obligación — degradar lo publicado a «no oficial» anularía toda la transparencia activa, incluida V_LOTAIP.
- **Verificabilidad**: parcial — NO por su oficialidad, sino porque lo leído es el Plan Plurianual .xlsx y la fuente canónica de metas es el PDOT aprobado (escalón 7: lo leído ≠ la fuente). Requiere corroboración contra las tablas #341-352 del PDOT Bicentenario.
- **Corroborar contra**: `PDOT MOntecristi 2023-2027 Bicentenario.docx · tablas #341-352`

### ⚠️ «No remitido formalmente» NO es «no oficial»

Javo lo corrigió y va al fondo de la doctrina: **el documento se obtuvo del portal del GAD, y eso lo hace oficial.** La `LOTAIP Art. 7` obliga a publicarlo, y el canon de QUIRA dice literalmente que **el portal es la materialización de una obligación**. Degradar lo publicado a «no oficial» porque no llegó por oficio contradice el modelo entero: si sólo valiera lo remitido a solicitud, **toda la transparencia activa valdría cero** — y con ella `V_LOTAIP`, que puntúa 1,0 justamente por «documento en URL pública del GAD, accesible y verificable» (`H13!C10`).

Son dos cosas distintas que la etiqueta mezclaba:

| | |
|---|---|
| **no remitido formalmente** | no hubo entrega institucional por solicitud — es un hecho sobre el CANAL |
| **no oficial** | el documento no tiene carácter oficial — es un juicio sobre el DOCUMENTO, y aquí es **falso** |

### Pero la reserva se mantiene, por otra razón

La `verificabilidad: parcial` **sigue siendo correcta**, y no por la oficialidad: lo leído fue el **Plan Plurianual `.xlsx`**, y la propia procedencia pide corroborarlo contra el **PDOT Bicentenario `.docx`, tablas #341-352**. Son **dos documentos distintos**; que ambos sean oficiales no los hace el mismo.

Es el **escalón 7** de la escalera prueba↔verificador: *lo leído ≠ la fuente*. El conteo de 66 procede del instrumento de programación plurianual, no del PDOT aprobado por ordenanza. Mientras no se corrobore, el denominador es **oficial y provisional a la vez** — dos atributos que no se contradicen.

## 3 · Composición y sesgo por sistema del PDOT

| Sistema | En el PDOT | Fuera del motor | Dentro (inferido) | % dentro |
|---|---:|---:|---:|---:|
| 1. FIS AM | 9 | 7 | 2 | 22 % |
| 2. ASEN | 26 | 20 | 6 | 23 % |
| 3.SOC | 13 | 9 | 4 | 31 % |
| 4. EC | 5 | 3 | 2 | 40 % |
| 5. INST | 13 | 11 | 2 | 15 % |

⚠️ **Esta tabla mide composición, NO sesgo.** Un reparto desigual puede ser exactamente lo que una muestra **estratégica** debe producir: si el criterio era «las metas de mayor peso presupuestario», concentrar en unos sistemas es el resultado correcto, no una distorsión.

**Para hablar de sesgo hace falta el criterio, y el criterio no está declarado** (§4). Sin él, cualquier lectura de esta tabla sería inferir la regla desde el patrón de sus resultados — `DOC-009`.

## 4 · ★ EL CRITERIO, DECLARADO POR SU FUENTE LEGÍTIMA

> **«Las 25 fueron tomadas por contener el monto económico más amplio en relación al total de metas, las 66. Eso fue para fines sólo de tesis.»**
> — Javo, 2026-09-03

**El criterio deja de ser `NOT_DETERMINABLE`.** Y la forma en que se resolvió importa tanto como el contenido: **no se dedujo mirando las 25** —eso habría sido `DOC-009`— sino que **lo declaró quien lo aplicó**. Es exactamente lo que a `E_i` le sigue faltando: una fuente con autoridad sobre la regla, no una explicación que encaje con los datos.

### Y el criterio tiene una consecuencia medible

Si la selección fue **por monto**, entonces la muestra es representativa del **gasto**, no del PDOT como instrumento de planificación. Contrastado con la composición por sistema (§3), el efecto es sistemático:

- **5. INST** queda al **15 %** de cobertura
- **1. FIS AM** queda al **22 %** de cobertura

El sistema **institucional** es el de menor cobertura — y es precisamente donde viven la gobernanza, la transparencia y la participación: metas de **bajo costo y alta relevancia** para un observatorio de integridad. Un criterio de monto las excluye por construcción.

⚠️ **Esto no es un defecto de la tesis.** Para validar un modelo con recursos limitados, tomar las metas de mayor peso económico es una decisión metodológica razonable y transparente: concentra la validación donde está el dinero. **Lo que dice es qué puede afirmar el ICPI v1** — desempeño sobre el gasto estratégico— **y qué no**: desempeño sobre el PDOT como mandato completo.

### La regla que queda

> **La justificación del universo operacional no implica la justificación de su mecanismo de selección.**

`ADR-036` justificó **usar 25 como universo operacional v1**. Eso no era lo mismo que justificar **por qué esas 25 son representativas** — y hasta hoy sólo teníamos lo primero. Son dos afirmaciones distintas y confundirlas es la misma trampa que `E_i`: conocer el valor no es conocer la regla que lo produjo. → `DOC-018`

### Nota histórica · lo que este apartado decía antes

**Búsqueda en `docs/`, `governance/` e `identity/`: ningún documento declara por qué esas 25 y no otras 25.**

`ADR-036` verifica que las 25 **existen** en el PDOT —ninguna inventada—, y eso responde «son legítimas». **No responde «por qué éstas».** Es la misma forma del problema de `E_i`: valores conocidos, regla generadora no reconstruible.

Y aquí importa más que en `E_i`, porque de ese criterio depende si la muestra es **representativa**:

| Si el criterio fue… | Entonces la muestra… |
|---|---|
| mayor peso presupuestario | es materialmente representativa aunque sea el 38 % de las metas |
| competencia exclusiva crítica | representa el mandato, no el gasto |
| disponibilidad de evidencia | **está sesgada hacia lo verificable**, y el ICPI mediría lo que es fácil de medir |
| conveniencia o disponibilidad | no es una muestra estratégica |

Las cuatro producen el mismo conjunto de 25 y **significados completamente distintos del 27,4582 %**.

## 5 · El ADR-036 §1 exige declarar el alcance · ¿se cumple?

> «Toda publicación de d01/d03 debe declararlo: *se mide contra las 25 metas estratégicas del modelo*.»

- En **texto que la interfaz puede pintar**: **0**
- Sólo en **comentarios de código**: 1 — `quira_pages/p_command_center_v2.py:200`

⚠️ **La consecuencia práctica del ADR no se ejecutó.** El alcance se declaró en el ADR y en un comentario de código; **el producto no lo dice**. Un usuario que lee el ICPI en cualquier superficie recibe un índice que se presenta como global sobre un universo del que nadie le informa.

Es el patrón del «48,33 %» invertido: allí una cifra retirada seguía publicándose; aquí **una declaración obligatoria nunca llegó a publicarse**. Un ADR ratificado cuya consecuencia práctica nadie comprueba es una decisión que existe sólo en el papel.

## Veredicto de 008

> ### COBERTURA LIMITADA, METODOLÓGICAMENTE JUSTIFICADA EN SU ALCANCE v1,
> ### con criterio de selección DECLARADO y correspondencia exclusión/universo AÚN NO RECONCILIADA.

La formulación es deliberadamente estrecha. Decir «metodológicamente justificada» a secas sonaría a que está demostrada la **representatividad** de las 25, y lo que `ADR-036` justifica es algo más específico: **la decisión de usar 25 como universo operacional v1**.

| | Estado |
|---|---|
| `25/66` como cobertura documental | **37,88 %** — relación válida |
| 25 = universo operacional v1 | **RATIFICADO** (`ADR-036`) |
| Criterio de selección | **DECLARADO**: mayor monto económico (Javo) |
| Representatividad respecto del PDOT | **del gasto sí · del mandato no** |
| Identidad de las metas excluidas | ⚠️ **pendiente de reconciliación** |
| Sesgo | no es sesgo: es el criterio operando como fue definido |
| Ampliar 25→66 ahora | **NO** — es metodología nueva (`ADR-036 §4`) |
| ICPI 27,4582 % | **CONGELADO** · no se recalcula |

**La afirmación que el ICPI v1 sostiene**, y ninguna más amplia:

> El ICPI v1 opera sobre un subconjunto de 25 metas —las de mayor monto económico— de un PDOT que contiene 66. Su resultado **no representa el desempeño del PDOT completo**, sino el desempeño respecto de su universo operacional v1.

**Reserva única que queda abierta · la correspondencia meta a meta.** No existe todavía un catálogo canónico que enlace las 66 con las 25. La resta `66−25=41` es aritméticamente correcta, pero **la identidad de esas 41 no está demostrada documentalmente** — y los 50 del catálogo de exclusiones no pueden asumirse equivalentes. Ése es el único pendiente técnico real de 008.

**Y la obligación del `ADR-036 §1` sigue incumplida**: el alcance no se declara en ninguna superficie visible (`DOC-017`).

## ★ DECISIÓN v2 · el universo completo

> **«Ahora, como ecosistema de Ecuador para LATAM, debemos trabajar con todo el universo del PDOT.»** — Javo, 2026-09-03

Es exactamente la evolución que `ADR-036 §3/§4` anticipó, y la decisión es correcta: un observatorio que aspira a 222 GAD no puede medir sobre una muestra tomada para validar una tesis. **El criterio de monto sirvió para demostrar que el modelo funciona; no sirve para observar un mandato.**

Pero el `ADR-036 §4` fija cómo: **versión nueva del motor · recalibración · nueva validación empírica · ADR específico**. Y hay una razón de secuencia que conviene respetar:

> `011` todavía no ha dictaminado si la fórmula es válida. **Cargar 66 metas en un álgebra que puede cambiar sería hacer el trabajo dos veces** — justo lo que este proyecto decidió evitar al construir el mapa de frentes.

Por eso la decisión se **registra ahora** y su ejecución va **después de `011`**. Con una excepción importante, y es la parte más cara:

**La reconciliación meta a meta (`66 ↔ 25`) puede y debe empezar ya.** No depende de `011` —hay que hacerla sea cual sea el dictamen—, es prerequisito de v2, y además cierra la única reserva que 008 deja abierta. Es el trabajo que desbloquea todo lo demás.

### Lo que 008 NO hace

- **No amplía de 25 a 66.** `ADR-036 §2/§4`: sería una versión metodológica nueva, con recalibración y ADR propio. No entra por la puerta de una cura.
- **No toca la cifra madre.** 27,4582 % sigue congelada.
- **No declara sesgo.** Falta el criterio, y sin él sería `DOC-009`.
- **No cuadra el complemento.** Señala que 41 ≠ 50 y deja el trabajo identificado, porque cuadrarlo exige cruzar meta a meta contra el PDOT.

---
*GM-Ω-ICPI-008 · universo operacional 25 · PDOT 66 (verificabilidad parcial) · el Gold Master no se modificó · Dylus Lab © 2026*
