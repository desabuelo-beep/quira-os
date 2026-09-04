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

## 4 · El hueco real: el criterio de selección no está en ninguna parte

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

> ### COBERTURA LIMITADA PERO METODOLÓGICAMENTE JUSTIFICADA · **con dos reservas**

**Justificada** porque `ADR-036` la decidió, la ratificó, verificó que las 25 pertenecen al PDOT, congeló el motor y planificó la evolución a v2. No es un error ni una omisión: es una decisión arquitectónica explícita y defendible.

**Reserva 1 · el criterio de selección es `NOT_DETERMINABLE`.** Sin él no se puede afirmar que la muestra sea representativa, y por tanto tampoco que el 27,4582 % sea extrapolable al PDOT completo. Hoy el índice sólo puede afirmarse **sobre su universo operacional**.

**Reserva 2 · el alcance no llega al producto.** La obligación del `ADR-036 §1` no se cumplió en ninguna superficie visible.

### Lo que 008 NO hace

- **No amplía de 25 a 66.** `ADR-036 §2/§4`: sería una versión metodológica nueva, con recalibración y ADR propio. No entra por la puerta de una cura.
- **No toca la cifra madre.** 27,4582 % sigue congelada.
- **No declara sesgo.** Falta el criterio, y sin él sería `DOC-009`.
- **No cuadra el complemento.** Señala que 41 ≠ 50 y deja el trabajo identificado, porque cuadrarlo exige cruzar meta a meta contra el PDOT.

---
*GM-Ω-ICPI-008 · universo operacional 25 · PDOT 66 (verificabilidad parcial) · el Gold Master no se modificó · Dylus Lab © 2026*
