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

> La pregunta con la que arrancó `007` era si el ICPI mide la integridad de la cadena de gestión o está fuertemente condicionado por cómo repartimos el peso presupuestario y jurídico. **La respuesta es que el peso casi no lo condiciona.** Lo que lo condiciona es su álgebra.

| Decisión metodológica | Rango que abre | Peor caso | Mejor caso |
|---|---:|---:|---:|
| `007-D` · la estructura algebraica | **51.26 pp** | +0.00 pp | +51.26 pp |
| `007-B` · la especificación de `V` | **12.41 pp** | -10.82 pp | +1.58 pp |
| `007-A` · el peso  `P × R` | **3.54 pp** | -2.37 pp | +1.17 pp |
| `007-C` · el tope de `T` | **0.47 pp** | +0.00 pp | +0.47 pp |

Ordenado así, el resultado es inequívoco y **no era el esperado**: cambiar la estructura algebraica mueve el índice hasta **51.3 puntos**, mientras que redistribuir todo el peso —o eliminarlo del todo— lo mueve **3.5**. El ICPI es **robusto a la ponderación y frágil a su propia forma matemática**.

Eso reordena `011`: la discusión sobre si el agua potable debe pesar más que un taller —legítima, y respondida por `P·R`— resulta ser de **segundo orden** frente a la pregunta de si las seis dimensiones deben multiplicarse. La decisión grande del motor nunca estuvo en los ponderadores.

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

### `A3` da exactamente el baseline, y no es una coincidencia numérica

`A3` se desvía 6e-15 pp. Eso no es «casi igual»: es **cero algebraico**. Multiplicar todos los pesos por una constante no cambia una media ponderada —`Σ(cK·S)/Σ(cK) = Σ(K·S)/Σ(K)`— y normalizar `R` por la suma es exactamente eso.

La consecuencia es una **propiedad demostrada del motor**, no una observación: **la escala de `R_i` es irrelevante para el ICPI; sólo importa su forma relativa entre metas.** Que `R` se normalice por el máximo teórico y `P` por la suma es, por tanto, una inconsistencia de presentación —dos variables que parecen comparables y no lo son— sin ningún efecto sobre el resultado. Es de las pocas cosas que `011` puede cerrar sin discutir.

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

   Son dos problemas encadenados. Uno: donde debería haber una categoría de gobernanza hay una frase que no lo es. Dos: esa frase está escrita en **lenguaje interno** —«no comparable con umbral anual»— y cruza al producto, que es justo lo que el Bloomberg Firewall existe para impedir. **Este es el único de los tres hallazgos que toca al usuario final**, y por eso es el primero que `011` debe resolver.

Los tres van al dictamen `011`. Ninguno se corrige aquí: `007` observa. Pero el tercero no puede esperar a `011` sin que alguien lo sepa, y por eso queda escrito aquí y en el registro de deudas.

---
*GM-Ω-ICPI-007 · 16 escenarios · baseline congelado 27,4582 % · el Gold Master no se modificó · Dylus Lab © 2026*
