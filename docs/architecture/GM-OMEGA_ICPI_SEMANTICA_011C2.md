# GM-Ω · ICPI — GENEALOGÍA SEMÁNTICA  `011-C2`

**DERIVADO — no editar a mano.** Lo regenera `scripts/gm_omega/semantica_factores.py` leyendo `H02_GLOSARIO_QUIRA`, `H01` Secciones I y M, y `H12`.

> ### La pregunta
> `011-C1` reconstruyó **el álgebra**. Ésta reconstruye **el significado**: qué mide cada letra, y si lo que el motor DECLARA medir coincide con lo que su mecanismo EFECTIVAMENTE mide.

⚠️ **No dictamina.** Que una semántica resulte confusa, solapada o calibrada al revés es un hecho que aquí se REGISTRA. Si eso invalida el constructo lo juzga `011-C4`.

## Por qué esta etapa se adelantó a `010`

`009` clasificó `C_i` **dos veces y las dos se equivocó**:

| Intento | Clasificación | Quién la propuso | Por qué falló |
|---|---|---|---|
| 1.º | DOCUMENTAL | esta dirección | inflaba el techo de la vía documental, que es justamente el resultado que 009 medía |
| 2.º | MATERIAL | Javo | plausible e institucionalmente coherente, pero **hipótesis del autor**, no semántica demostrada |
| 3.º | PENDIENTE | el colega | ✅ un análisis de incentivos no puede fijar la ontología de la variable que lo audita |

> Mientras no se sepa qué significan `E_i` y `C_i`, todo análisis de comportamiento se hace sobre variables cuya ontología seguimos reconstruyendo. **Por eso `011-C2` va antes que `010`.**

## 1 · Qué DECLARA medir cada factor

Fuente: `H02_GLOSARIO_QUIRA`, el glosario del propio Gold Master. Literal, sin parafrasear.

### `P_i`

**Pi (Peso financiero)** · fuente declarada: H14_PONDERADORES

> Variable que pondera cada meta según su participación en el presupuesto anual del PDOT. La suma de todos los Pi debe ser exactamente 1.0000.

### `R_i`

**Ri (Relevancia competencial)** · fuente declarada: H14_PONDERADORES

> Variable que pondera la relevancia de una competencia: Exclusiva Crítica (1.5) / Exclusiva Importante (1.0) / Complementaria (0.5). Incorpora bonos ODS 5 y ODS 13 (×1.15).

### `V_i`

**Vi (Verificación intersistémica)** · fuente declarada: H13_VARIABLES_Vi

> Variable binaria que mide si una meta tiene evidencia verificable en los silos. Fórmula: Si los 4 verificadores (S4/S5/S7/S8) ≥1 → Vi=1.0; si suma ≥2 → Vi=0.5; si suma <2 → Vi=0.0.

### `E_i`

**Ei (Autonomía orgánica)** · fuente declarada: SIAP-ICPI Metodología v1.0

> Variable que mide el grado de autonomía con que el GAD ejerce una competencia. Escala: 1.0=autónomo / 0.9=compartido / 0.75=difuso o ambiguo.

### `T_i`

**Ti (Ejecución de inversión)** · fuente declarada: H07_S5_FINANCIERO_eSIGEF + H07c

> Variable que mide la ejecución financiera de inversión. Fórmula: Ti = Devengado_Grupos_7+8 / Codificado_Grupos_7+8. Solo Grupos 7 y 8. Jerarquía adaptativa: 1-eSIGEF → 2-Ti_V → 3-Ti_Histórico → 4=0.

**Ti_FUENTE** · fuente declarada: H12_MOTOR_ICPI_CANÓNICO

> Columna informativa en H12 que indica de dónde provino el Ti de cada meta: 'eSIGEF' / 'Ti_V' / 'Ti_Histórico' / 'Sin_evidencia'. No entra al cálculo ICPI.

**Ti_Histórico** · fuente declarada: H07b_Ti_INVERSIÓN_eSIGEF

> Tercer tipo de Ti. Usa datos históricos verificados (H07b) cuando no hay eSIGEF ni Ti_V. Solo para cálculo provisional.

**Ti_V (Ti Verificado)** · fuente declarada: SIAP-ICPI Metodología v1.0

> Cuarto tipo de Ti. Aplica cuando no existe cédula eSIGEF pero sí existe un informe firmado electrónicamente con hash SHA-256 (PDF). Típico de metas intangibles y fondos concursables.

**Ti (Tasa de Inversion)** · fuente declarada: QUIRA OS RC-1.1 - Semaforos Holding Municipal

> Indicador de ejecucion presupuestaria mensual por entidad. Semaforo Holding: Verde>=35% Amarillo 15-34.9% Rojo<15%

### `C_i`

**Ci (Calidad de proceso)** · fuente declarada: SIAP-ICPI Metodología v1.0 — DECISIÓN Javo Delgado Santana, 27-Abr-2026

> Variable que mide la calidad institucional del proceso orgánico responsable de una meta. ★ DETERMINISTA v1.0: Ci = MAX(1.00 - Σ deducciones normativas, 0). El proceso nace con Ci=1.00 (presunción de legalidad). Las infracciones CGE/SERCOP/COPFP/CPCCS deducen puntos. Fuente: H01 Sección L. Marco legal: LOSNCP + COPFP + CGE + CPCCS (NO LOSEP — LOSEP evalúa personas, SIAP-ICPI evalúa procesos de inversión).

**Ci_Adaptativo** · fuente declarada: H12_MOTOR_ICPI_CANÓNICO — columna Ci_Calc

> Versión calculada del Ci que incorpora modificadores según TIPO_FINANCIAMIENTO e INTANGIBLE_FLAG. Fórmula: Ci_adaptativo = MIN(Ci_base × Modificador, 1.0). El Ci_base siempre viene de H01 Sección I. Calculado en H12.

**Ci_Determinista** · fuente declarada: LOSNCP Art.17 / COPFP Art.9 / Ley Orgánica CGE / Ley CPCCS

> Algoritmo que calcula Ci a partir de infracciones normativas reales documentadas. Fórmula: Ci = MAX(1.00 - (CGE_Obs × 0.10) - (SERCOP_Alert × 0.15) - (POA_Retraso × 0.20) - (CPCCS_Desacato × 0.50), 0). Garantiza objetividad, auditabilidad y reproducibilidad. Fuente de datos: Sección L de H01.

**Mapeo Retrospectivo** · fuente declarada: SIAP-ICPI Metodología v1.0 — Fórmula Canónica (Axioma de Invarianza)

> Técnica de reverse engineering que inyecta los valores históricos 2025 de infracciones normativas en H01 Sección L para que el algoritmo Ci reproduzca exactamente el ICPI canónico 69.9309%. Distribución 2025: 11 metas Ci=1.00 / 9 metas Ci=0.90 / 5 metas Ci=0.75. En 2026, los valores reales sustituyen el mapeo.

## 2 · Qué hace EFECTIVAMENTE la celda

Una definición no dice cómo se calcula. Esta tabla lee la fórmula real de `H12`, meta a meta:

| Factor | Celdas literales | Valores distintos | Referencias | Estado |
|---|---:|---|---|---|
| `P_i` | 0/25 | 0.0008, 0.0013, 0.0016, 0.0019, 0.0028, 0.0029, … (25) | `H14_PONDERADORES` | ✅ derivado |
| `R_i` | 0/25 | 0.2899, 0.3333, 0.5797, 0.6667, 0.8696, 1 | `H14_PONDERADORES` | ✅ derivado |
| `V_i` | 0/25 | 0, 0.5, 1 | `H13_VARIABLES_Vi` | ✅ derivado |
| `E_i` | 25/25 | 0.75, 0.9, 1 | — | 🔴 **literal · sin fórmula** |
| `T_i` | 0/25 | 0.3035, 0.656, 0.9165, 1 | `H07b_Ti_INVERSIÓN_eSIGEF` | ✅ derivado |
| `C_i` | 0/25 | 0.75, 0.9, 1 | `H01_PARÁMETROS` | ✅ derivado |

## ★ 3 · `C_i` — la hipótesis contrastada contra el instrumento

La hipótesis que `009` tenía prohibido dar por buena:

> «`C_i` mide **atribución y entrega material verificada** — acta de entrega-recepción e impacto verificado. Si `T=1` (dinero entregado) pero la obra no tiene acta ni impacto (`C→0`), el producto penaliza la meta y anula el maquillaje contable de fin de año.»

Esto es lo que el Gold Master dice de sí mismo:

| Encabezado de `H01` Sección I | ▌ SECCIÓN I — TABLA Ci — CALIDAD DE PROCESO ORGÁNICO POR META |
|---|---|
| Registro de la creación (`H01!A94`) | ★ Ci DETERMINISTA v1.0 (Javo Delgado Santana, 27-Abr-2026): Ci arranca en 1.00. Deducciones legales Sección L calculan Ci final. Ci_Base columna E es FÓRMULA de Sección M — NO hardcodeado. Nombres de Dirección = H02b exacto (Res. 040-2025). |
| Encabezado de Sección M | ▌ SECCIÓN M — REGISTRO DE INFRACCIONES Y CALIBRACIÓN Ci (TBL_CALIBRACION_Ci) |

Y las **cuatro deducciones** que la Sección M registra son:

| # | Deducción | Qué mide |
|---|---|---|
| 1 | `INF-01 (LOSNCP)` | infracción de contratación pública |
| 2 | `INF-02 (CGE/NCI)` | observación de la Contraloría |
| 3 | `INF-03 (COPFP)` | incumplimiento de planificación/finanzas |
| 4 | `INF-04 (CPCCS)` | desacato en participación ciudadana |

### El veredicto de la comparación

| Mitad de la hipótesis | ¿Está en el instrumento? |
|---|---|
| **Atribución** — imputar la meta a un responsable | ✅ **SÍ** · la Sección I asigna a cada meta `Cod_Unidad`, `Dirección Responsable (Res.040-2025)` y `Base Legal Estatuto` |
| **Entrega material verificada** — acta de entrega-recepción, impacto | 🔴 **NO** · ninguna de las cuatro deducciones mide entrega. Todas miden **infracciones normativas verificadas** |

> ### `C_i` mide legalidad del proceso, no entrega del producto
>
> El nombre canónico es **«Calidad de Proceso Orgánico»** / **«Trazabilidad Orgánica (imputabilidad responsable)»**. El proceso **nace en 1,00 por presunción de legalidad** y se deduce por infracciones documentadas. Es un **descuento punitivo-jurídico**, no una verificación de entrega.

⚠️ **La hipótesis no era descabellada: era una lectura del propósito, no del mecanismo.** La mitad de atribución se sostiene; la mitad de entrega material **no está implementada en ninguna variable del ICPI**. Y eso tiene una consecuencia directa sobre `009`:

| Distorsión institucional | Estado real de la respuesta |
|---|---|
| anticipo de noviembre con obra sin empezar | 🔴 **el motor no lo captura hoy** · `T_i` sube y `C_i` no baja, porque `C_i` sólo baja ante una infracción registrada |

Es decir: la cuarta distorsión de la lista de `009` —la que se declaró no cubierta— **no es la única**. La segunda tampoco lo está. Se corrige en el expediente de `009` como consecuencia de esta etapa.

## ★ 3-bis · El mismo factor, tres reglas distintas

Al verificar la referencia del glosario —«Fuente: `H01` Sección L»— apareció algo que no se buscaba. La Sección L **sí existe** y define cuánto deduce cada infracción. El problema es que **el glosario la define otra vez, y no dicen lo mismo**.

| Código | Norma | Deducción · **Sección L** | Deducción · **glosario `Ci_Determinista`** | |
|---|---|---|---|---|
| `INF-01` | LOSNCP Art. 17 / 58 | `-0.15` | `×0.15` | ✅ coinciden |
| `INF-02` | CGE / NCI 406-01 | `-0.1` | `×0.1` | ✅ coinciden |
| `INF-03` | COPFP Art. 10 / 115 | `-0.05` | `×0.2` | 🔴 **divergen** · ×4 |
| `INF-04` | LO_CPCCS Art. 11 | `FIJA Ci=0.50` | `×0.5` | 🔴 **otra operación** · el glosario resta, la matriz FIJA |

Y hay una tercera regla, en la propia Sección L:

> `★ MOTOR DETERMINISTA Ci: abandona valoración heurística. Ci = MÁX(0.50, 1.00 - Σ penalizaciones). Marco legal: LOSNCP + COPFP + CGE + CPCCS. Principio de inocencia: todo proceso nace Ci=1.00`
> `⚠️ REGLA INF-04 — FIJACIÓN ABSOLUTA:`
> `Si INF-04=1 para cualquier meta, Ci=0.50 DIRECTAMENTE sin importar otros INF. Es fijación, no resta.`
> `=SI(INF-04=1, 0.50, MÁX(0.50, 1.00-(INF-01*0.15+INF-02*0.10+INF-03*0.05)))`

### Las tres divergencias

| # | Qué difiere | Consecuencia |
|---|---|---|
| 1 | **`INF-03` deduce 0,05 o 0,20** según qué artefacto se lea | un retraso de planificación pesa **4 veces más** en el glosario que en la matriz normativa |
| 2 | **`INF-04` resta 0,50 o FIJA `Ci=0,50`** | no es formato, es **otra operación**: sobre una meta con `Ci=0,75`, restar da `0,25`; fijar da `0,50` |
| 3 | **El piso es `0` o `0,50`** | el glosario dice `MAX(…, 0)`; la regla de la Sección L dice `MÁX(0,50; …)`. Con el piso alto, `C_i` **nunca puede anular una meta** |

> ### Es el patrón del «48,33 %», aplicado a una variable del motor
>
> Un **derivado narrativo** —el glosario— se desacopló de su **fuente canónica** —la Sección L—, y ambos siguen circulando como si dijeran lo mismo. `QUIRA` fue construido para detectar exactamente esto en los documentos que audita. Aquí ocurre **dentro del instrumento que audita**.

⚠️ **Y hoy no cambia ningún número**: sin infracciones registradas, ninguna de las tres reglas se ejecuta. La divergencia es **latente**. Se activaría el día que se registre la primera infracción — que es precisamente el día en que el motor tiene que estar bien.

### Qué NO se afirma aquí

- **No se afirma cuál de las tres es la correcta.** Determinar la regla vigente exige la razón de cada versión: `011-C3`.
- **No se afirma que sea un error de diseño.** Puede ser una versión anterior no propagada, y eso también lo dice `011-C3`.
- **No se toca nada.** El Gold Master es inmutable (`Regla de Oro 1`); `011-C2` levanta acta.

## 3-ter · Qué entra REALMENTE al índice

Una definición en el glosario no es participación en el cálculo. La única autoridad es el numerador:

```
  Numerador_i = =B6*C6*D6*E6*F6*I6
```

Es decir, entran: `P_i` · `R_i` · `V_i` · `E_i` · `T_i_2026` · `C_i`.

| Definido en el glosario | ¿Entra al ICPI? |
|---|---|
| `Ci (Calidad de proceso)` — vía `H01` Sección M | ✅ sí, es la columna `C_i` |
| `Ci_Adaptativo` — modificadores por `TIPO_FINANCIAMIENTO` e `INTANGIBLE_FLAG` | 🔴 **NO** · el numerador no lo referencia |

⚠️ Eso incluye la **discriminación positiva ×1,15 por `FONDO_CONCURSABLE`**, que el glosario declara y el motor canónico no aplica. Un premio definido y no implementado no es lo mismo que un premio inexistente: es una **capacidad declarada sin efecto**, y va a `011-C3`.

## ★ 4 · ¿Está OPERANDO el mecanismo declarado?

De las **25 metas** de la Sección M, las que registran alguna infracción son **0**.

Ninguna. Y sin embargo `C_i` **no es constante**: toma los valores `0.75`, `0.9`, `1`.

> ### Si todas las deducciones son cero, el valor vigente NO procede del mecanismo declarado

No hay que inferirlo: **el instrumento lo dice de sí mismo**.

> ▌ SECCIÓN M — REGISTRO DE INFRACCIONES Y CALIBRACIÓN Ci (TBL_CALIBRACION_Ci)

> Propósito: Registrar infracciones verificadas y calcular Ci algorítmicamente. INF-01..04 VACÍOS al inicio — los ingresa el analista SIAP-ICPI con evidencia. Ci_Calculado = fórmula automática. NUNCA inventar infracciones.

> Distribución Ci_Manual_2025: Ci=1.00 → 11 metas | Ci=0.90 → 9 metas | Ci=0.75 → 5 metas. Total=25. Estos valores producen ICPI=69.9309%.

Y el glosario nombra la técnica sin eufemismo:

> **Mapeo Retrospectivo** · Técnica de reverse engineering que inyecta los valores históricos 2025 de infracciones normativas en H01 Sección L para que el algoritmo Ci reproduzca exactamente el ICPI canónico 69.9309%. Distribución 2025: 11 metas Ci=1.00 / 9 metas Ci=0.90 / 5 metas Ci=0.75. En 2026, los valores reales sustituyen el mapeo.

### ⚠️ Cuarta divergencia · las dos secciones se contradicen

Puestas una junto a otra, la Sección L y la Sección M **del mismo libro** afirman lo contrario sobre el mismo factor:

| Sección | Qué declara |
|---|---|
| **L** — matriz normativa | «★ MOTOR DETERMINISTA Ci: abandona valoración heurística. Ci = MÁX(0.50, 1.00 - Σ penalizaciones). Marco legal: LOSNCP + COPFP + CGE + CPCCS. Principio» |
| **M** — registro y calibración | «Nota metodológica: La Calibración Retrospectiva 2025 establece la línea base. Ci_Manual_2025 = REAL-HEURÍSTICO. Ci_Calculado usa Ci_Manual_2025 como fallback cuando no hay infracciones → preserva ICPI_Axioma=69» |

> La L declara que el motor **abandona** la valoración heurística. La M declara que la heurística de 2025 **es el fallback vigente**. Ambas son ciertas a la vez sólo si «abandonar» significa «dejar de usarla cuando haya infracciones» — que es una lectura posible, pero **es una lectura, no lo que el texto dice**.

Ésta es la divergencia **más consecuente de las cuatro**, porque no es sobre un peso ni sobre una operación: es sobre **si el factor es determinista o heurístico hoy**. Y de eso depende cómo se puede presentar el ICPI públicamente.

### Cómo se clasifica esto

| Afirmación | Grado |
|---|---|
| El mecanismo declarado de `C_i` es la deducción por infracciones | **DEMOSTRADO** · glosario + Sección M |
| Hoy no hay ninguna infracción registrada | **DEMOSTRADO** · Sección M |
| El valor vigente de `C_i` procede de `Ci_Manual_2025` | **DECLARADO POR EL INSTRUMENTO** · nota metodológica de la Sección M |
| La calibración se ajustó para reproducir un ICPI previamente fijado | **DECLARADO POR EL INSTRUMENTO** · glosario, «Mapeo Retrospectivo» |
| Esa calibración es metodológicamente admisible | ⬜ **NO LO JUZGA `011-C2`** · `011-C3` (justificación) y `011-C4` (dictamen) |

⚠️ **Y hay que decir lo que esto NO es.** No registrar una infracción que no existe es **correcto**: el canon prohíbe fabricar infracciones para alimentar el motor. La cuestión abierta es distinta y es de vigencia: **usar una calibración heurística de 2025 como valor de 2026**. `007-B0` ya dejó esa pregunta abierta; `011-C2` le pone nombre propio y la entrega a `011-C3`.

## ★ 5 · `E_i` y `C_i` — dos variables, una escala, un vocabulario

El hallazgo que obligó a mirar dos veces:

| | `E_i` | `C_i` (base) |
|---|---|---|
| Nombre | Autonomía orgánica | Calidad de proceso orgánico |
| Escala observada | `0.75` · `0.9` · `1` | `0.75` · `0.9` · `1` |
| Vocabulario de la escala | autónomo / compartido / difuso | proceso **exclusivo / compartido / difuso** (Sección I, «Base Legal Estatuto») |
| Fuente declarada | Estatuto Orgánico (Res. 040-2025) | Estatuto Orgánico (Res. 040-2025) |

Misma escala, mismo vocabulario, misma fuente. **La pregunta obligada es si son la misma variable dos veces.** Se mide meta a meta:

> **`E_i` = `C_i` en 13 de 25 metas (52 %).**

| Meta | `E_i` | `C_i` | Etiqueta legal (Sección I) | ¿Coinciden? |
|---|---:|---:|---|---|
| `SC-I-N-01` | 1 | 1 | exclusivo | ✅ |
| `SC-L-N-02` | 1 | 1 | exclusivo | ✅ |
| `AH-I-X-01` | 0.9 | 0.9 | compartido | ✅ |
| `AH-I-X-02` | 1 | 1 | exclusivo | ✅ |
| `AH-I-X-03` | 0.9 | 1 | exclusivo | 🔴 **divergen** |
| `AH-I-N-01` | 0.75 | 0.75 | difuso | ✅ |
| `SC-L-G-01` | 0.75 | 0.75 | compartido | ✅ |
| `AH-I-X-04` | 0.75 | 0.75 | difuso | ✅ |
| `PI-I-G-01` | 1 | 1 | exclusivo | ✅ |
| `AH-C-X-01` | 1 | 0.9 | compartido | 🔴 **divergen** |
| `AH-C-X-02` | 1 | 0.9 | compartido | 🔴 **divergen** |
| `SC-I-N-03` | 0.75 | 0.9 | compartido | 🔴 **divergen** |
| `FA-I-X-01` | 1 | 1 | exclusivo | ✅ |
| `FA-C-X-01` | 1 | 0.75 | difuso | 🔴 **divergen** |
| `FA-I-X-02` | 0.9 | 0.9 | compartido | ✅ |
| `FA-L-N-01` | 0.9 | 1 | exclusivo | 🔴 **divergen** |
| `PI-I-G-02` | 1 | 0.9 | compartido | 🔴 **divergen** |
| `PI-L-G-01` | 0.75 | 1 | exclusivo | 🔴 **divergen** |
| `EP-L-N-01` | 1 | 0.9 | compartido | 🔴 **divergen** |
| `EP-L-X-01` | 1 | 0.9 | compartido | 🔴 **divergen** |
| `PI-TUR-01` | 1 | 0.9 | compartido | 🔴 **divergen** |
| `PI-TUR-02` | 1 | 1 | exclusivo | ✅ |
| `FA-CC-01` | 1 | 1 | exclusivo | ✅ |
| `AH-AP-04` | 1 | 1 | exclusivo | ✅ |
| `FA-DIS-01` | 1 | 0.75 | difuso | 🔴 **divergen** |

### Qué se puede y qué no se puede concluir

| Afirmación | Grado |
|---|---|
| Comparten escala, vocabulario y fuente declarada | **DEMOSTRADO** |
| Coinciden en 52 % de las metas | **DEMOSTRADO** |
| **Son la misma variable duplicada** | 🔴 **REFUTADO** · divergen en 12 metas; si fueran la misma, coincidirían en todas |
| La etiqueta legal predice `E_i` | en 12/25 metas con etiqueta |
| La etiqueta legal predice `C_i` | en 24/25 metas con etiqueta |
| Existe **ambigüedad ontológica** entre ambas | **DEMOSTRADO** · dos dimensiones distintas de la fórmula usan el mismo vocabulario y la misma escala sobre la misma fuente |

> ### El hallazgo NO es «están duplicadas». Es peor de diagnosticar y mejor de corregir: **están parcialmente solapadas y no se sabe por qué divergen donde divergen.**

Porque una divergencia puede significar dos cosas opuestas:

```
  E = 1,00  ·  C = 0,75      ¿la competencia es autónoma pero el
                             proceso orgánico es difuso?          ← legítimo
                             ¿o una de las dos está mal asignada? ← defecto
```

Y `011-C2` **no puede distinguirlas**: exigiría la razón de cada asignación, que es material de `011-C3`. Lo que sí puede decir es que **nada en el instrumento explica la diferencia** — no hay columna de justificación para `E_i`, que es literal en `H12` y carece de entrada propia en la Sección I.

## Lo que `011-C2` entrega

### A `011-C3` · justificación de cada transformación

| # | Pregunta que `C3` hereda | De dónde sale |
|---|---|---|
| 1 | ¿Por qué `C_i` se calibró retrospectivamente contra un ICPI ya fijado, y quién lo decidió? | §4 |
| 2 | ¿Por qué una calibración declarada «2025» sigue vigente en 2026? | §4 |
| 3 | ¿Cuál de las reglas de deducción es la vigente — la Sección L o el glosario? | §3-bis |
| 4 | ¿El piso de `C_i` es `0` o `0,50`? De ello depende si `C_i` **puede anular una meta** | §3-bis |
| 5 | ¿`INF-04` resta o fija? | §3-bis |
| 6 | ¿Es `C_i` determinista o heurístico **hoy**? | §4 |
| 7 | ¿Por qué `E_i` y `C_i` divergen en las metas donde divergen? | §5 |
| 8 | ¿Se incorporó `C_i` sabiendo que solaparía con `E_i`, o se descubrió después? | §5 |
| 9 | ¿Por qué `Ci_Adaptativo` está definido y no se aplica? | §3-ter |

### A `011-C4` · el dictamen

> Si dos de los seis factores comparten escala, vocabulario y fuente, la pregunta de la multiplicatividad **cambia de forma**: ya no es sólo si el producto es la operación correcta, sino **sobre cuántas dimensiones realmente independientes opera**.

### A `009` · una corrección

El expediente de `009` afirma que el motor responde a la disociación financiero ↔ físico mediante `C_i`. **Esta etapa lo desmiente**: `C_i` sólo baja ante una infracción registrada, y hoy no hay ninguna. La corrección se aplica en `009` marcando esa fila como no cubierta.

## Dictamen de `011-C2` · por grado de certeza

| Afirmación | Estado |
|---|---|
| Cada factor tiene una definición canónica en el glosario del motor | **DEMOSTRADO** |
| `C_i` mide calidad jurídica del proceso orgánico | **DEMOSTRADO** · glosario `H02` + Secciones I/M |
| `C_i` mide entrega material verificada | 🔴 **REFUTADO** · ninguna deducción mide entrega |
| `C_i` imputa la meta a una unidad orgánica responsable | **DEMOSTRADO** · Sección I |
| El valor vigente de `C_i` no procede del mecanismo declarado | **DECLARADO POR EL INSTRUMENTO** |
| `E_i` mide autonomía en el ejercicio de la competencia | **DEMOSTRADO** · glosario `H02` |
| `E_i` y `C_i` son la misma variable | 🔴 **REFUTADO** |
| `E_i` y `C_i` presentan ambigüedad ontológica | **DEMOSTRADO** |
| La razón de cada divergencia `E_i` ↔ `C_i` | ⬜ **NO DETERMINABLE** aquí · `011-C3` |
| El glosario y la Sección L discrepan sobre `INF-03`, `INF-04` y el piso | **DEMOSTRADO** |
| `Ci_Adaptativo` no entra al numerador | **DEMOSTRADO** · la fórmula del numerador no lo referencia |
| Cuál de las reglas discrepantes es la vigente | ⬜ **NO DETERMINABLE** aquí · `011-C3` |
| Si el solapamiento invalida la arquitectura | ⬜ **FUERA DE ALCANCE** · `011-C4` |

> ### GM-Ω-011-C2 — CERRADO COMO RECONSTRUCCIÓN SEMÁNTICA
>
> Se estableció **qué declara medir cada factor** y **qué mide su mecanismo**. Aparecieron cuatro divergencias: `C_i` no verifica entrega material; `E_i` y `C_i` comparten escala y vocabulario sin ser la misma variable; el glosario y la matriz normativa discrepan sobre tres reglas de deducción; y las Secciones L y M se contradicen sobre si el factor es determinista o heurístico.
>
> **Ninguna cambia hoy el ICPI** — las tres primeras son latentes y la cuarta ya está resuelta de facto por el fallback. Eso las hace más fáciles de corregir, **no menos importantes**.
>
> **No juzga** si son defectos. Reconstruir el significado no es aprobarlo ni condenarlo — eso es `011-C3` y `011-C4`.

---
*GM-Ω-ICPI-011-C2 · 25 metas · 6 factores · leído del Gold Master, no de la memoria · el Gold Master no se modificó · Dylus Lab © 2026*
