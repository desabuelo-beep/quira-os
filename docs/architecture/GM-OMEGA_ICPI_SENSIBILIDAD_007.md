# GM-Ω · ICPI — SENSIBILIDAD  `007-A/B/C/D/X`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/sensibilidad_icpi.py` leyendo el Gold Master vigente.

> ### ⚠️ LAS TRES ETIQUETAS
> Cada escenario de este documento es, sin excepción:
> **MATEMÁTICAMENTE REPRODUCIBLE** · **METODOLÓGICAMENTE CONTRAFACTUAL** · **NO AUTORIZADO PARA PUBLICACIÓN**.
>
> El único número oficial es **27,4582 %** (regla `GM-Ω-ICPI-000`) hasta que `GM-Ω-ICPI-011` dictamine. Ninguna cifra de aquí puede citarse fuera de esta auditoría, ni siquiera para ilustrar: el patrón que perseguimos —el «48,33 %»— nació de un número de trabajo que sobrevivió a su contexto.

Baseline reproducido por el laboratorio: **27.458227 %** (desvío 1.11e-16 respecto de `H12!B33`). Sin esa reproducción exacta, ningún contrafactual sería interpretable.

**`E_i` no entra en ningún escenario.** Su regla generadora está `NOT_DETERMINABLE` (`007-B0`): mover una variable cuya biografía no conocemos sería inferir su regla desde el efecto que produce, que es lo que `DOC-009` prohíbe. Entra en `011` o no entra.

## La jerarquía de sensibilidad

> La pregunta con la que arrancó `007` era si el ICPI mide la integridad de la cadena de gestión o está fuertemente condicionado por cómo repartimos el peso presupuestario y jurídico. La respuesta es que el peso **apenas** lo condiciona, y su álgebra **lo gobierna**.

| Decisión metodológica | Rango que abre | Peor caso | Mejor caso |
|---|---:|---:|---:|
| `007-D` · la estructura algebraica | **51.26 pp** | +0.00 pp | +51.26 pp |
| `007-B` · la especificación de `V` | **12.41 pp** | -10.82 pp | +1.58 pp |
| `007-A` · el peso  `P × R` | **3.54 pp** | -2.37 pp | +1.17 pp |
| `007-C` · el tope de `T` | **0.47 pp** | +0.00 pp | +0.47 pp |

Ordenado así, el resultado es inequívoco y **no era el esperado**: cambiar la estructura algebraica mueve el índice hasta **51.3 puntos**, mientras que redistribuir todo el peso —o eliminarlo del todo— lo mueve **3.5**.

### La conclusión, formulada con precisión

> **El ICPI presenta baja sensibilidad a las alternativas de ponderación ENSAYADAS y alta sensibilidad a la arquitectura algebraica de agregación. Por tanto, la validez sustantiva del índice depende mucho más de la justificación teórica de su estructura multiplicativa que de la elección entre las ponderaciones evaluadas.**

⚠️ **La formulación importa, y la primera versión era peor.** Decir que el índice es «frágil a su forma matemática» suena a diagnóstico y en realidad contrabandea un juicio: sugiere que la multiplicatividad es un defecto. `007-D` **no demuestra que multiplicar esté mal** — demuestra que multiplicar es **altamente determinante**. Son dos afirmaciones distintas y sólo la segunda está medida.

Y las dos precisiones del enunciado no son adorno:

- **«ensayadas»** — se probaron cuatro alternativas de peso, no todas las posibles. Una ponderación radicalmente distinta podría mover más. Lo medido es lo medido.
- **«validez sustantiva»** — lo que está en juego no es qué número sale, sino si el número significa lo que el constructo promete.

Eso reordena `011`: la discusión sobre si el agua potable debe pesar más que un taller —legítima, y respondida por `P·R`— resulta ser de **segundo orden** frente a la pregunta de primer orden, que es:

> **¿Qué teoría de la integridad representa realmente `J = P·R·V·E·T·C`, y qué la fundamenta?**

La estructura multiplicativa no queda impugnada por `007`. Queda **obligada a demostrar por qué debe existir**.

## 007-X · Robustez de clasificación

La pregunta de 007-X no es cuánto cambia el número, sino si cambia **la categoría** — porque es la categoría, no el decimal, lo que se convierte en decisión.

| Esc. | Escenario | ICPI | Δ abs. | Δ rel. | Categoría AVEP |
|---|---|---:|---:|---:|---|
| `A0` | P × R  (baseline) | 27.4582 % | +0.0000 | +0.0 % | 🟠 Gestión por Ocurrencia |
| `A1` | sólo P (peso presupuestario) | 28.6292 % | +1.1710 | +4.3 % | 🟠 Gestión por Ocurrencia |
| `A2` | sólo R (relevancia jurídica) | 25.0883 % | -2.3699 | -8.6 % | 🟠 Gestión por Ocurrencia |
| `A3` | P × R con R normalizado por la suma | 27.4582 % | +0.0000 | +0.0 % | 🟠 Gestión por Ocurrencia |
| `A4` | peso uniforme (todas las metas valen igual) | 26.8488 % | -0.6094 | -2.2 % | 🟠 Gestión por Ocurrencia |
| `B0` | V implementado (H13!F · literales) | 27.4582 % | +0.0000 | +0.0 % | 🟠 Gestión por Ocurrencia |
| `B1` | V por la regla documentada (H13!B20) | 27.4582 % | +0.0000 | +0.0 % | 🟠 Gestión por Ocurrencia |
| `B2a` | V por la regla anterior · lectura literal | 16.6365 % | -10.8217 | -39.4 % | 🔴 Ruptura Sistémica ⚠️ |
| `B2b` | V por la regla anterior · lectura de tres niveles | 28.4089 % | +0.9507 | +3.5 % | 🟠 Gestión por Ocurrencia |
| `B3` | V sin núcleo obligatorio (media de los 4 silos) | 29.0417 % | +1.5835 | +5.8 % | 🟠 Gestión por Ocurrencia |
| `C0` | T con tope MIN(1, ·)  (baseline) | 27.4582 % | +0.0000 | +0.0 % | 🟠 Gestión por Ocurrencia |
| `C1` | T sin tope | 27.9314 % | +0.4732 | +1.7 % | 🟠 Gestión por Ocurrencia |
| `D0` | multiplicativa  V×E×T×C  (baseline) | 27.4582 % | +0.0000 | +0.0 % | 🟠 Gestión por Ocurrencia |
| `D1` | media aritmética de las 4 dimensiones | 78.7210 % | +51.2628 | +186.7 % | 🟢 Gestión por Mandato ⚠️ |
| `D2` | media geométrica de las 4 dimensiones | 64.8333 % | +37.3751 | +136.1 % | 🟡 Transición Crítica ⚠️ |
| `D3` | por bloques: V eliminatorio × media(E, T, C) | 64.6741 % | +37.2159 | +135.5 % | 🟡 Transición Crítica ⚠️ |

**Categoría del baseline: 🟠 Gestión por Ocurrencia.** Se mantiene en **12 de 16** escenarios.

Escenarios que **cambian la categoría** — sensibilidad decisional, no sólo numérica:

- `B2a` V por la regla anterior · lectura literal → **🔴 Ruptura Sistémica**
- `D1` media aritmética de las 4 dimensiones → **🟢 Gestión por Mandato**
- `D2` media geométrica de las 4 dimensiones → **🟡 Transición Crítica**
- `D3` por bloques: V eliminatorio × media(E, T, C) → **🟡 Transición Crítica**

⚠️ **El baseline está a 7.46 puntos porcentuales del umbral de 20 %.** Esa distancia es la que convierte cualquier decisión metodológica de este documento en una decisión sobre la categoría publicable, y no sólo sobre un decimal.

⚠️ Y una precisión que cambia cómo se lee toda esta tabla: **hoy el motor NO emite categoría.** `H12!B34` la condiciona a `H07!B22>=12` —doce meses de corte— y el corte vigente es el mes **4**, así que la celda devuelve «Corte parcial · lectura preliminar (no comparable con umbral anual)». Las categorías de esta tabla son **las que el motor emitiría al cierre**, calculadas con sus mismos umbrales. No son lo que el motor dice hoy.

### ★ 007-X-bis · ¿Y de dónde salen los umbrales?

Javo aportó el contexto que faltaba: **la escala AVEP es invención de Dylus Lab**, ajustada después a lo que la normativa pública exigía. Eso obliga a hacer explícito un supuesto que toda esta sección arrastraba: **`007-X` mide la robustez de la categoría contra unos umbrales cuya procedencia no estaba auditada.** Auditada ahora, esto es lo que hay.

**1 · La norma sostiene el CONSTRUCTO, no los CORTES.** La tesis titula un apartado «Baremo AVEP — Interpretación jurídica» y lo que fundamenta allí es *por qué* medir congruencia: `COPFP Art. 41` —el PDOT es la directriz **principal**, luego una inversión no alineada es jurídicamente cuestionable—. Las variables sí tienen norma citada (`P_i` → COPFP 54; `R_i` → COOTAD 54-55 + Constitución 3, 12, 66). **Dónde cortar en 70 o en 40 no la tiene.**

**2 · La escala está COPIADA en 11 hojas** `H01_PARÁMETROS`, `H02_GLOSARIO_QUIRA`, `H12_MOTOR_ICPI_CANÓNICO`, `H12b_MOTOR_IBSC`, `H12c_ICPI_HISTÓRICO_ANUAL`, `H16b_IPE`, `H17_IED`, `H18_ITAM` …, y **ninguna de esas copias cita una norma**, mientras que los umbrales de inversión del mismo libro sí citan COOTAD.

   Y la copia no es accidental: `H01!A30` **instruye a copiarla literalmente**. Viene de un incidente real que `H01!A28` conserva —

   > «AVEP NO es una función de Excel. NO existe `=AVEP()`. Si se escribe `=AVEP(...)` el resultado será `#¿NOMBRE?` y el ecosistema fallará.»

   El motor confundió la escala con una fórmula, y la solución adoptada —replicar el `IF` en todas las hojas— **resolvió el síntoma y consolidó la causa**: una capa de interpretación quedó incrustada dentro del cálculo, y duplicada. Cambiar un umbral hoy exige editar N celdas a mano.

**4 · La tesis nunca dijo que fuera una fórmula.** La llama «Baremo de Valoración» y «Baremo de **Interpretación**», y dice que los resultados «se **contrastan** con» él. La doctrina correcta ya estaba escrita antes que el motor:

   ```
   dato → estado epistemológico → INTERPRETACIÓN → producto
                                      ↑ aquí vive AVEP
   ```

**5 · Qué significa esto para LATAM (`010`).** Aquí está la tensión que Javo intuye, y tiene salida:

| | Anclar los cortes a normativa local | Mantenerlos propios |
|---|---|---|
| Defensa en Ecuador | fuerte (hay norma) | exige argumento teórico |
| Viaje a LATAM | ❌ no viaja: se recalibra por país | ✅ viaja |

   La salida no es elegir una: es **separar las capas**. El constructo se ancla a norma —y esa parte es local por naturaleza—; los **cortes** son una decisión metodológica propia, explícita y **calibrable por país**. Que es justamente la arquitectura núcleo/adaptador que `010` tiene que demostrar.

⚠️ **Nada de esto dice que la escala esté mal.** Los umbrales de un índice compuesto casi nunca salen de una norma: son una decisión metodológica, y es legítima. Lo que `007-X-bis` establece es que **hoy se presenta con la misma autoridad que un umbral legal y no la tiene**, que vive en la capa equivocada, y que de ella depende un Certificado (`H01!C59` fija la emisión en AVEP ≥ 70 %). Una escala con consecuencia contractual necesita procedencia declarada. → `011`.

## Concentración del resultado (baseline)

| Medida | Valor |
|---|---:|
| Meta que más aporta | 38.53 % del numerador |
| Tres metas que más aportan | 76.39 % |
| Cinco metas que más aportan | 88.73 % |
| Metas que explican el 50 % | 2 de 25 |
| Metas que explican el 80 % | 4 de 25 |
| HHI de las contribuciones | 0.2498 |

Esto **no convierte el índice en malo**: concentrar el peso en las metas estratégicas puede ser exactamente lo que QUIRA quiere medir, y es lo que `P_i` hace a propósito —impedir que metas baratas inflen el resultado mientras el alcantarillado sigue parado—. Pero un índice que se presenta como global y depende de unas pocas metas tiene que ser **consciente y declarado**, no descubierto por un tercero.

### Las diez metas que más pesan

| # | Meta | P | R | K=P·R | peso efec. | S=V·E·T·C | J | % del num. |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `SC-I-N-01` | 0.2736 | 0.8696 | 0.2379 | 34.86 % | 0.3035 | 0.0722 | 38.53 % |
| 2 | `SC-L-N-02` | 0.3079 | 0.5797 | 0.1785 | 26.15 % | 0.3035 | 0.0542 | 28.90 % |
| 3 | `AH-I-X-01` | 0.1179 | 0.5797 | 0.0683 | 10.01 % | 0.2458 | 0.0168 | 8.96 % |
| 4 | `FA-I-X-02` | 0.0292 | 0.5797 | 0.0169 | 2.48 % | 0.8100 | 0.0137 | 7.31 % |
| 5 | `AH-I-N-01` | 0.0335 | 1.0000 | 0.0335 | 4.91 % | 0.2812 | 0.0094 | 5.03 % |
| 6 | `AH-I-X-03` | 0.0343 | 0.2899 | 0.0099 | 1.46 % | 0.5904 | 0.0059 | 3.13 % |
| 7 | `FA-I-X-01` | 0.0055 | 0.6667 | 0.0037 | 0.54 % | 0.9165 | 0.0034 | 1.81 % |
| 8 | `PI-I-G-01` | 0.0151 | 0.5797 | 0.0088 | 1.28 % | 0.3035 | 0.0027 | 1.42 % |
| 9 | `AH-I-X-04` | 0.0220 | 0.5797 | 0.0127 | 1.87 % | 0.1707 | 0.0022 | 1.16 % |
| 10 | `AH-C-X-01` | 0.0102 | 0.3333 | 0.0034 | 0.50 % | 0.5904 | 0.0020 | 1.08 % |

Y **6 metas aportan exactamente 0 al numerador** mientras siguen ocupando 12.80 % del denominador: `AH-I-X-02`, `PI-TUR-01`, `PI-TUR-02`, `FA-CC-01`, `AH-AP-04`, `FA-DIS-01`. Es la multiplicatividad operando — y lo que 007-D mide.

⚠️ Y entre ellas están metas de **máxima relevancia jurídica**: `FA-DIS-01` (R=1.0000), `AH-I-X-02` (R=0.8696), `AH-AP-04` (R=0.8696). El motor las reconoce como competencia exclusiva crítica y acto seguido las anula, porque una sola dimensión en cero extingue el producto. Que eso sea correcto —una obra crítica sin verificación no debería puntuar— o excesivo —desaparece del índice justo la meta que más importaba vigilar— es la decisión de `011`. Aquí sólo se mide que ocurre.

## 007-A · Sensibilidad del peso (`P × R`)

> ¿El ICPI mide la integridad de la cadena de gestión, o está fuertemente condicionado por cómo repartimos el peso presupuestario y jurídico?

**Hallazgo de estructura, previo a los escenarios.** La fórmula canónica `Σ(P·R·V·E·T·C) / Σ(P·R)` es algebraicamente una **media ponderada** de `S = V·E·T·C` con pesos `K = P·R`. La multiplicatividad no está en la agregación entre metas —que es lineal— sino **dentro** de cada meta, entre sus cuatro dimensiones. Son dos decisiones distintas y hasta ahora se leían como una: `007-A` audita la primera, `007-D` la segunda.

**Y las dos normalizaciones no son la misma.** `P_i` se normaliza por la **suma** (Σ=1 exacto, verificado en `H14!G33`); `R_i` por el **máximo teórico** `1,5 × 1,15 = 1,725`, y por eso Σ`R_i` = 15.3478, no 1. Conviven en el mismo producto. `A3` mide qué pasaría si `R` se normalizara como `P`.

| Esc. | Escenario | ICPI | Δ vs. baseline | Categoría | Nota |
|---|---|---:|---:|---|---|
| `A0` | P × R  (baseline) | 27.4582 % | +0.0000 pp | 🟠 Gestión por Ocurrencia |  |
| `A1` | sólo P (peso presupuestario) | 28.6292 % | +1.1710 pp | 🟠 Gestión por Ocurrencia |  |
| `A2` | sólo R (relevancia jurídica) | 25.0883 % | -2.3699 pp | 🟠 Gestión por Ocurrencia |  |
| `A3` | P × R con R normalizado por la suma | 27.4582 % | +0.0000 pp | 🟠 Gestión por Ocurrencia | R por suma en vez de por el máximo teórico 1,725 |
| `A4` | peso uniforme (todas las metas valen igual) | 26.8488 % | -0.6094 pp | 🟠 Gestión por Ocurrencia | la pregunta literal de Javo: ¿todo debe valer igual? |

### ★ HALLAZGO DE INVARIANCIA DE ESCALA

`A3` se desvía 6e-15 pp del baseline. Eso no es «casi igual»: es **cero algebraico**, y no es un resultado empírico de este conjunto de datos — es una **propiedad del estimador**. La demostración cabe en tres líneas:

```
        K_i = P_i · R_i                        peso vigente
       R'_i = R_i / ΣR                         normalizar R por la suma
       K'_i = P_i · R_i / ΣR = (1/ΣR) · K_i    una constante común

   ICPI(K') = Σ(cK_i·S_i) / Σ(cK_i)
            = c·Σ(K_i·S_i) / c·Σ(K_i)
            = ICPI(K)                          ∎
```

Toda transformación de `R` que sea una constante multiplicativa común deja el ICPI **exactamente igual**. De ahí se siguen dos cosas:

1. **La escala de `R_i` es irrelevante para el índice; sólo importa su forma relativa entre metas.** Que `R` se normalice por el máximo teórico y `P` por la suma es una inconsistencia de presentación —dos variables que parecen comparables y no lo son— **sin ningún efecto sobre el resultado**. `011` puede cerrarlo sin discutirlo.
2. Y una **falsa preocupación queda eliminada**: no hay que decidir cómo normalizar `R`, porque la decisión no existe. Saber qué transformaciones son irrelevantes *por construcción* es tan parte de auditar un estimador como saber cuáles lo mueven — y es lo que separa correr escenarios de entender el instrumento.

### La respuesta a la pregunta de Javo

> *«¿pesa más el agua potable por necesidad de extrema urgencia, o todo debe valer igual si se planificó?»*

`A4` responde con un número: si **todas las metas pesaran igual**, el ICPI sería -0.61 pp distinto. Menos de un punto. Y las dos mitades del peso, por separado, abren apenas 3.54 pp entre sí.

Lo cual **no invalida la ponderación** —`P·R` sigue siendo el antídoto anti-gaming que impide que metas baratas inflen el índice, y sigue gobernando el **ranking** de metas, que es donde se toman decisiones concretas—. Lo que dice es más preciso: la ponderación decide **a quién se mira**, no **cuánto sale**. El agregado lo decide `S = V·E·T·C`.

## 007-B · `V_i` — especificación implementada vs. documentada

**A diferencia de `E_i`, aquí sí hay biografía.** El propio libro conserva la regla vigente, la regla anterior y la justificación del cambio:

```
H13!B16-B20 · REGLA VIGENTE (documentada en prosa)
  Vi = 0.0  si V_eSIGEF=0 O V_SERCOP=0     sin núcleo financiero, sin score
  Vi = 0.5  si núcleo OK y sin LOTAIP ni CPCCS
  Vi = 1.0  si núcleo OK y (LOTAIP=1 O CPCCS=1)

H13!B21 · POR QUÉ CAMBIÓ
  «La fórmula original SI(suma≥2,0.5) era incorrecta: producía Vi=0.5
   para metas con SERCOP=0/eSIGEF=0 pero LOTAIP=1/CPCCS=1.»
```

Eso es exactamente lo que a `E_i` le falta, y conviene decirlo en voz alta: **`E_i` es la excepción del motor, no su norma.** El resto de las variables documenta sus cambios.

### ⚠️ Pero la regla está documentada y NO implementada

`H12!D` lee `VLOOKUP(A, H13!$A:$F, 6)` → la columna `F` de `H13`, que contiene **25 literales**, no la fórmula. La regla vive en prosa, en las celdas `B16..B20`, donde ningún recálculo la aplica. Es el mismo patrón que `E_i`, un escalón más arriba: allí no había regla; aquí la hay y no está conectada a los valores que el motor consume.

Y esa columna se llama `Vi_2025`, bajo un título que dice «VALORES Vi DE REFERENCIA 2025 — para verificar ICPI_Real_2025». **El ICPI 2026 está consumiendo la columna de referencia de 2025** (`TEMPORAL_SEMANTIC_GAP`, ya registrado en la matriz `004`).

### Coherencia regla ↔ valor, meta a meta

De las **25 metas comparables**, **25 coinciden** con la regla documentada y **0 no**.

**Los valores implementados obedecen la regla documentada, uno por uno.** La especificación de `V_i` es reconstruible y está cumplida: lo que falla no es la regla, es que viva en prosa y en la columna de otro año.

### La regla anterior: reconstruible sólo en parte

`H13!B21` conserva un **fragmento** —el umbral de 2 y el 0,5— pero no dice qué producía la regla original con los cuatro verificadores en 1. **Su forma exacta es `NOT_DETERMINABLE`**, y por eso se prueban las dos lecturas posibles y se declaran como lecturas. `DOC-009` aplicado a `V`: la nota documenta el **cambio**, no reconstruye el **original**.

| Esc. | Escenario | ICPI | Δ vs. baseline | Categoría | Nota |
|---|---|---:|---:|---|---|
| `B0` | V implementado (H13!F · literales) | 27.4582 % | +0.0000 pp | 🟠 Gestión por Ocurrencia |  |
| `B1` | V por la regla documentada (H13!B20) | 27.4582 % | +0.0000 pp | 🟠 Gestión por Ocurrencia |  |
| `B2a` | V por la regla anterior · lectura literal | 16.6365 % | -10.8217 pp | 🔴 Ruptura Sistémica ⚠️ | ≥2 verificadores → 0,5 · si no 0 · forma exacta NOT_DETERMINABLE |
| `B2b` | V por la regla anterior · lectura de tres niveles | 28.4089 % | +0.9507 pp | 🟠 Gestión por Ocurrencia | 4 verificadores → 1 · ≥2 → 0,5 · forma exacta NOT_DETERMINABLE |
| `B3` | V sin núcleo obligatorio (media de los 4 silos) | 29.0417 % | +1.5835 pp | 🟠 Gestión por Ocurrencia | diagnóstico: cuánto pesa que eSIGEF+SERCOP sean eliminatorios |

### ⚠️ El hallazgo de `B2`: la incertidumbre abarca dos categorías

`B2a` y `B2b` son **dos lecturas de la misma regla anterior**, y difieren en **11.77 puntos** — de 16.64 % a 28.41 %. No cruzan un decimal: cruzan una frontera de categoría, de «🔴 Ruptura Sistémica» a «🟠 Gestión por Ocurrencia».

La lectura correcta **no** es «el motor antiguo daba 16 %». Es esta:

> El fragmento que el libro conserva de la regla anterior es **insuficiente para reconstruir el pasado**, y el margen de esa insuficiencia vale dos categorías AVEP.

Es `DOC-009` en su forma más útil: la nota de `H13!B21` **parece** documentar la regla anterior y en realidad documenta sólo por qué se abandonó. Dos auditorías igual de rigurosas, partiendo del mismo libro, reconstruirían historias distintas — y ninguna de las dos podría demostrar la suya.

### ★ DOS VACÍOS DE NATURALEZA DISTINTA — `V` no tiene el problema de `E`

Este es el resultado que más lejos llega de todo `007`, y no es un número. Puestos uno al lado del otro, `V` y `E` **no tienen el mismo problema**, y tratarlos igual sería el error:

| | `V_i` | `E_i` |
|---|---|---|
| Definición del constructo | ✅ existe | ✅ existe |
| Regla vigente documentada | ✅ `H13!B16-B20` | ❌ no consta |
| Regla histórica documentada | ✅ fragmento en `H13!B21` | ✅ tesis: 1 · 0,90 · 0,75 |
| Explicación del cambio | ✅ y con su motivo | ❌ ninguna |
| Valores reproducibles contra su regla | ✅ 25 de 25 | ❌ ninguno |
| **Naturaleza del vacío** | **límite de reconstrucción** | **ausencia de regla generadora** |

`V` está en una situación **sana para una auditoría**: hay genealogía, y hay un límite explícito de lo que sabemos. Se puede decir con precisión qué se sabe, qué no, y por qué. `E` no: existe la variable, existe una regla histórica en la tesis, existe la corrección de Javo sobre no penalizar la afiliación, existen los valores — y **no existe evidencia preservada que permita reconstruir la regla que produjo esos valores**.

> Un vacío de trazabilidad se clasifica por su **naturaleza**, no por su tamaño. «No puedo reconstruirlo del todo» y «no hay nada que reconstruir» exigen auditorías distintas y admiten conclusiones distintas.

Y de ahí se sigue, retroactivamente, que **fue correcto dejar `E_i` fuera de `007`**: hacer sensibilidad sobre una variable cuya regla generadora se desconoce habría producido números impecables sobre una premisa epistemológicamente vacía. Elegante y sin fundamento — que es la forma más difícil de detectar un error.

**Y hay que separar dos cosas que 007 no mezcla.** `V` como **regla** —qué significa verificación intersistémica— y `V` como **evidencia** —si lo capturado satisface esa regla—. Este documento mide sólo la **sensibilidad del resultado** a la elección de arquitectura. Cuál de las dos representa mejor el constructo que QUIRA quiere medir es una pregunta de `011`.

## 007-C · El tope `MIN(1, ·)` de `T_i`

No se parte de que el tope sea un defecto: **puede ser correcto**. Si la teoría dice que una meta que alcanzó el umbral temporal esperado ya obtuvo el máximo crédito temporal, truncar es la implementación fiel de esa idea. La pregunta auditable es otra:

> ¿El tope elimina información que la teoría del indicador necesitaría conservar?

`T_i = MIN(1, Ti_raw / FactorTemporal)`, con `FactorTemporal` = **0.212** para el mes de corte **4**.

| Entidad | `Ti_raw` | sin tope | con tope | ¿truncada? |
|---|---:|---:|---:|---|
| ENTE-01 GAD central | 0.064342 | 0.303498 | 0.303498 | no |
| ENTE-02 Patronato | 0.139075 | 0.656014 | 0.656014 | no |
| ENTE-03 Bomberos | 0.194300 | 0.916509 | 0.916509 | no |
| ENTE-04 EP Aseo | 0.241599 | 1.139618 | 1.000000 | ⚠️ **sí** |

**1 de 4 entidades está truncada**, y arrastra **3 de 25 metas**: `AH-I-N-01`, `FA-I-X-02`, `FA-DIS-01`.

### ⚠️ Y el `FactorTemporal` ya no es lo que su nota dice

La fórmula real es una **curva de pacing empírica**:

```
H07!B23 = CHOOSE(mes, 0.011, 0.11, 0.128, 0.212, 0.266, 0.36,
                      0.442, 0.516, 0.766, 0.883, 0.925, 1)
  «curva pacing Montecristi 2025: promedio de 3 adscritas»
```

pero la nota que la describe en `H07b!F20` sigue diciendo «`Ti normalizada: Ti_raw / FactorTemporal (mes/12). Refleja avance proporcional al`». Para abril, la curva da **0.212** y la descripción lineal daría **0,3333**: un 57 % más exigente. La fórmula cambió y su descripción se quedó atrás — el mismo patrón del «48,33 %», aquí en la nota de una celda.

Hay además una circularidad que `011` tendrá que juzgar: la curva se construyó con el pacing de **las tres adscritas en 2025**, y se usa para normalizar el desempeño de **esas mismas adscritas en 2026**. El denominador y el numerador comparten origen.

| Esc. | Escenario | ICPI | Δ vs. baseline | Categoría | Nota |
|---|---|---:|---:|---|---|
| `C0` | T con tope MIN(1, ·)  (baseline) | 27.4582 % | +0.0000 pp | 🟠 Gestión por Ocurrencia |  |
| `C1` | T sin tope | 27.9314 % | +0.4732 pp | 🟠 Gestión por Ocurrencia | 3 de 25 metas están truncadas hoy |

## 007-D · La arquitectura multiplicativa

Aquí ya no se audita un parámetro: se audita la **teoría matemática del indicador**. `J = P·R·V·E·T·C` afirma algo muy fuerte —que las dimensiones son **conjuntamente necesarias**— y por tanto que `V=0 → J=0`, y que cuatro deficiencias moderadas se **componen** en vez de promediarse. Eso puede ser exactamente lo que significa «integridad».

> ### ⚠️ `D1`–`D3` NO son candidatos de reemplazo
> Son instrumentos de diagnóstico. Si la media ponderada diera 61 % y la multiplicativa 27 %, eso **no haría al 61 más correcto**: mediría la consecuencia sustantiva de la multiplicatividad. Y una consecuencia de ese tamaño hay que justificarla, no heredarla.

| Esc. | Escenario | ICPI | Δ vs. baseline | Categoría | Nota |
|---|---|---:|---:|---|---|
| `D0` | multiplicativa  V×E×T×C  (baseline) | 27.4582 % | +0.0000 pp | 🟠 Gestión por Ocurrencia |  |
| `D1` | media aritmética de las 4 dimensiones | 78.7210 % | +51.2628 pp | 🟢 Gestión por Mandato ⚠️ | las deficiencias se suman en vez de interactuar |
| `D2` | media geométrica de las 4 dimensiones | 64.8333 % | +37.3751 pp | 🟡 Transición Crítica ⚠️ | conserva el cero eliminatorio, suaviza la penalización compuesta |
| `D3` | por bloques: V eliminatorio × media(E, T, C) | 64.6741 % | +37.2159 pp | 🟡 Transición Crítica ⚠️ | aísla cuánto viene del cero de V y cuánto de la interacción del resto |

### Qué significa esta tabla

**+51.3 puntos.** Ninguna otra decisión del motor se acerca. La multiplicatividad no es un detalle de implementación: es **la decisión que define el indicador**, y su efecto es tres categorías AVEP de distancia.

Y la comparación entre `D2` (64.83 %) y `D3` (64.67 %) —dos construcciones distintas que caen a 0.16 pp— **separa los dos efectos que hasta ahora iban juntos**:

- el **cero eliminatorio** (`V=0 → J=0`), que `D3` conserva íntegro;
- la **penalización compuesta** entre las dimensiones que no son cero, que `D3` sustituye por un promedio.

Que ambos den casi lo mismo dice que **casi toda la severidad del motor viene de la composición de deficiencias moderadas, no de los ceros**. Con `S = V·E·T·C`, una meta con las cuatro dimensiones en 0,75 —que en lenguaje llano es «va aceptablemente en todo»— puntúa 0,32. Ese es el núcleo del constructo, y hay que sostenerlo explícitamente o cambiarlo: hoy no está argumentado en ninguna parte del libro.

## Hallazgos colaterales del sondeo

Aparecieron al leer el motor para montar el laboratorio. No son contrafactuales: son **estado observado**, y por tanto sí son citables dentro de la auditoría.

1. **El rótulo del ICPI imprime `0,27 %` en 69 hojas del libro.** `H12!B33` guarda el índice en escala 0-1 (`=B31/B32`, sin el `×100` que declara la fórmula de `A3`), y la cabecera `E1` de cada hoja lo rotula con `ROUND(B33,2)&"%"`. El resultado literal es «ICPI 2026: 0,27 %» donde el índice es 27,46 %.

   ⚠️ **Y esto NO llega al producto** — hay que decirlo con la misma precisión con que se señala el defecto. La capa API corrige la escala: `H73!ICPI_GLOBAL_PCT = H12!B33*100`, y es de ahí de donde lee el conector. La UI publica 27,46 %. El defecto es **interno al libro**, en lo que ve quien abre el Excel: un auditor externo leyendo el Gold Master vería 0,27 % en la cabecera de cada hoja. Grave para la defensa documental, inocuo para la UI.

2. **La brecha ICM–ICPI compara escalas incompatibles.** `B36 = B35 − B33` resta un valor en escala 0-100 (`B35 = H08!B7×100`) menos uno en 0-1 (`B33`), y `B37` clasifica el resultado contra umbrales de 30 y 15. Con `B36` acotado a ese rango, el veredicto «✅ Brecha de Verificación mínima» es **estructuralmente inalcanzable de otro modo**: no es un resultado, es el único desenlace posible de la fórmula.

3. **La categoría AVEP no se emite hoy — y ese silencio SÍ llega al producto.** `H12!B34` exige 12 meses de corte y devuelve una frase de diagnóstico interno. La capa API la propaga tal cual:

   > `H73!ICPI_CLASIFICACION` = «Corte parcial - lectura preliminar (no comparable con umbral anual)»

   Y **5 superficies del producto** consumen ese campo: `quira_pages/p6_pulso.py`, `quira_pages/p7_brecha.py`, `quira_pages/p_command_center.py`, `quira_pages/p_concejo.py`, `quira_pages/p_ejecutivo.py`.

   Son dos problemas encadenados. Uno: donde debería haber una categoría de gobernanza hay una frase que no lo es. Dos: esa frase está escrita en **lenguaje interno** —«no comparable con umbral anual»— y cruza al producto, que es justo lo que el Bloomberg Firewall existe para impedir.

   ### ⚠️ Y este hallazgo pesa MÁS que el del rótulo `0,27 %`

   El `0,27 %` es real pero se queda dentro del libro. Este **cruza la frontera entre motor y producto**, que es de otra categoría arquitectónica. El motor *sabe* que está en corte parcial —y hace bien en negarse a clasificar—, pero esa condición interna termina **presentada como si fuera una categoría de gestión**. Es exactamente lo que la doctrina de QUIRA separa:

   ```
   dato → estado epistemológico → interpretación → producto
   ```

   Un estado de disponibilidad del indicador se convirtió en una categoría sustantiva. La cura no es «poner una categoría igualmente» —sería fabricar una lectura anual que el corte no sostiene—, sino **dos campos donde hoy hay uno**:

   ```
   estado_determinabilidad = CORTE_PARCIAL      (o ANUAL_COMPLETO)
   clasificacion_avep      = NO_EMITIDA         (o la categoría)
   ```

   Con eso, la UI puede decir en lenguaje de administración pública que la lectura anual todavía no es comparable, sin inventar una categoría ni publicar la jerga del motor. Queda especificado en `D-011`; no se implementa aquí, porque `007` observa.

Los tres van al dictamen `011`. Ninguno se corrige aquí. Pero el tercero no puede esperar a `011` sin que alguien lo sepa, y por eso queda escrito aquí y en el registro de deudas.

---
*GM-Ω-ICPI-007 · 16 escenarios · baseline congelado 27,4582 % · el Gold Master no se modificó · Dylus Lab © 2026*
