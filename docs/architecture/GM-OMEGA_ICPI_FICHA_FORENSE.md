# GM-Ω · ICPI — FICHA FORENSE v1.0

**2026-09-03 · Auditoría integral del Gold Master, primera pieza · Dylus Lab**

> **Javo:** *«deberíamos empezar la GM-Ω por el ICPI, esa es la cifra madre. Y si toca
> subsanarla, potenciarla y elevarla habría que hacerlo. Debemos capturar la gestión
> pública real de EC y LATAM desde el Excel, para todo el ecosistema.»*
>
> **El colega:** *«no debemos entrar pensando "vamos a auditar el ICPI para encontrar
> errores", sino: determinar si el ICPI merece seguir siendo la arquitectura matemática
> sobre la que se construye el resto. No debemos proteger una fórmula porque ya esté
> construida.»*

⚠️ **ESTE DOCUMENTO NO MODIFICA NADA.** Es la Fase 0: la ficha de identidad del ICPI
tal como está hoy, medida directamente sobre `SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx` por
la puerta canónica. El dictamen —conservar, subsanar, potenciar o rediseñar— es
GM-Ω-ICPI-011 y lo decide Javo.

---

## REGLA GM-Ω-ICPI-000 · el baseline se congela

    Mientras GM-Ω-ICPI-011 no emita dictamen:
      ICPI_2026_ACTUAL = 27,4582 %
      · no se modifica
      · no se recalcula con reglas alternativas
      · no se publica una cifra «corregida»
      · no se sustituye una metodología por otra durante el diagnóstico
      · las simulaciones son contrafactuales y NO constituyen resultado oficial

Propuesta del colega y adoptada: evita que la auditoría se contamine con su propia
propuesta. Precisamente porque ahora sabemos reproducir la cifra, es cuando más hay que
dejarla quieta.

---

## 1 · Identidad y árbol matemático  `GM-Ω-ICPI-001/003`

Fuente única: **`H12_MOTOR_ICPI_CANÓNICO!B33`**, declarada en `C33`:
*«FUENTE ÚNICA ICPI. Valor VIVO 2026. TODAS las hojas referencian SOLO B33. NUNCA
recalcular.»*

```
J_i (numerador_i)   = P_i × R_i × V_i × E_i × T_i × C_i
K_i (denominador_i) = P_i × R_i

ICPI = Σ J_i / Σ K_i        (B33 = B31/B32)
```

| Var | Qué es | De dónde sale |
|---|---|---|
| **P_i** | ponderador de la meta | `H14_PONDERADORES!G` |
| **R_i** | relevancia | `H14_PONDERADORES!F` |
| **V_i** | verificación intersistemas | `H13_VARIABLES_Vi` (VLOOKUP) |
| **E_i** | competencia: 1,0 autónomo · 0,9 compartido · 0,75 difuso | **valor estampado** en H12 |
| **T_i** | ejecución | `H07b_Ti_INVERSIÓN_eSIGEF` |
| **C_i** | calibración | `H01_PARÁMETROS §M · TBL_CALIBRACION_Ci` |

**Verificado numéricamente:** ΣJ = 0,187423 · ΣK = 0,682576 → **ICPI = 27,4582 %**,
idéntico al valor publicado. La fórmula es reproducible y el libro trae su propio
axioma de integridad histórica (`B40`, contra 69,9309061706625 de 2025).

**Lo que el motor hace bien y hay que decirlo:** una sola celda como fuente, cadena de
referencias explícita, verificación interna del axioma, y cada verificador con su base
legal citada (LOSNCP 22/73 · COPFP 115-117 · LOTAIP 7 · LOPC 88).

---

## 2 · HALLAZGO PRINCIPAL — el veto de la obra sobre la norma  `GM-Ω-ICPI-002/008/009`

`H13!A4`, **regla maestra textual**:

> *«V_eSIGEF y V_SERCOP son verificadores NÚCLEO obligatorios (ejecución financiera).
> V_LOTAIP y V_CPCCS son verificadores de TRANSPARENCIA/RENDICIÓN.»*

Y la lógica de tres niveles:

```
V_i = 0,0   si V_eSIGEF = 0  Ó  V_SERCOP = 0     ← veto absoluto
V_i = 0,5   si eSIGEF=1 Y SERCOP=1 Y sin transparencia ni rendición
V_i = 1,0   si eSIGEF=1 Y SERCOP=1 Y (LOTAIP=1 Ó CPCCS=1)
```

**El problema no es la fórmula: es a quién se le aplica.** El propio Gold Master
clasifica las metas por naturaleza —OBRA · SERVICIO · NORMATIVO— y anota, en sus
propias celdas, que algunas **no pueden generar** los rastros que el veto exige:

| Meta | Naturaleza | Nota del Gold Master | Peso |
|---|---|---|---|
| `AH-I-X-02` | OBRA | «Vi=0.0 **aunque LOTAIP=1/CPCCS=1**» | 8,1 % |
| `AH-AP-04` | SERVICIO | «Continuidad agua — índice de servicio, **no obra**» | 1,9 % |
| `FA-DIS-01` | OBRA | «capacidad operativa relleno» | 1,3 % |
| `PI-TUR-01` | SERVICIO | «Turismo/certificación — **no genera obra ni eSIGEF**» | 0,8 % |
| `FA-CC-01` | NORMATIVO | «Planes cambio climático — **instrumento normativo**» | 0,5 % |
| `PI-TUR-02` | SERVICIO | «Eventos turísticos — **intangible**» | 0,3 % |

**Seis metas de veinticinco puntúan CERO en el numerador y arrastran su peso completo
en el denominador: 12,8 % del índice.** Las seis tienen `LOTAIP=1` y `CPCCS=1` — están
documentadas y fueron rendidas.

### La consecuencia, y es de política pública

> **El índice premia el hormigón sobre la norma.** Un GAD que ejecute política
> normativa, servicios o instrumentos intangibles baja su ICPI aunque documente y
> rinda cuentas. Uno que contrate obra sube. La ausencia de un rastro que la meta **no
> puede producir por su naturaleza** se computa igual que no haber hecho nada.

Esto es, a la vez:

- **Prueba 1 del colega (universo):** se aplican verificadores de ejecución financiera
  a metas fuera de ese universo.
- **Prueba 2 (ausencia):** «no genera eSIGEF por naturaleza» y «no ejecutó» producen el
  mismo 0. Es la regla de DETERMINABILIDAD de la Capa 0 rota dentro del motor.
- **Prueba 6 (incentivos):** existe una vía de mejora del índice que no es mejora de
  gestión — reclasificar metas hacia OBRA, o priorizar lo contratable.

⚠️ **No se afirma que la regla sea un error.** Puede ser una decisión metodológica
deliberada: exigir ejecución financiera como piso de verificabilidad tiene fundamento.
Lo que **no** está declarado es que esa decisión deja fuera, por construcción, a las
metas de naturaleza no financiera — y que el índice las penaliza en vez de excluirlas
del universo o medirlas con sus verificadores aplicables.

---

## 3 · Concentración — dos metas son el 61 %  `GM-Ω-ICPI-007`

| Meta | Peso en el denominador |
|---|---|
| `SC-I-N-01` (agua potable) | **34,9 %** |
| `SC-L-N-02` (talento humano) | **26,1 %** |
| las otras 23 juntas | 39,0 % |

**El ICPI global es, en 3 de cada 5 partes, el desempeño de dos metas.** No es
necesariamente un defecto —la ponderación puede ser deliberada— pero sí obliga a
declararlo: mover `SC-I-N-01` mueve el índice nacional del cantón más que mover
veinte metas menores juntas. Cualquier lectura de «el ICPI subió» debe saberlo.

---

## 4 · La dimensión de ejecución casi no discrimina  `GM-Ω-ICPI-007`

**19 de 25 metas comparten exactamente el mismo `T_i` = 0,30349834503004025.** Sólo
seis tienen valor propio (tres en 1,0 y dos en 0,656).

Es decir: la variable que representa *ejecución* aplica un valor global a la gran
mayoría de metas. El índice discrimina por P, R, V, E y C — pero en T, para el 76 % de
las metas, todas valen lo mismo. Habrá que determinar si eso es un dato agregado
legítimo (ejecución presupuestaria global del GAD) o una carencia de dato por meta.

---

## 5 · Reglas del cero declaradas  `GM-Ω-ICPI-006`

`H12!A4`, textual: **«Ti: Jerarquía adaptativa eSIGEF→Ti_V→Ti_Hist→0.»**

La regla declara que, agotadas las tres fuentes, `T_i` **cae a 0**. Hoy **no se activa**
—ninguna meta tiene `T_i = 0`— pero la regla existe y, el día que se active, convertirá
«ninguna fuente tenía el dato» en «ejecución nula».

Es el mismo patrón que D-010 encontró en el IGP (`IGP_2 = 0` siendo un pendiente). **Dos
de dos índices auditados tratan la ausencia como cero.** Deja de parecer un caso y
empieza a parecer una regla implícita de todo el Gold Master.

---

## 6 · Las dos preguntas de Javo, medidas  `GM-Ω-ICPI-002/006`

> *«¿pesa más el agua potable por necesidades de extrema urgencia, o todo debe valer
> igual si se planifica? … no se puede puntuar al mismo nivel si una obra está
> planificada y publicada pero nunca adjudicada o ejecutada»*

### 6.1 · ¿Debe pesar más el agua? — el motor ya lo hace, y con fuente

`H14!A4` declara la escala: **«R_i_raw: 1,5 = Exclusiva Crítica (agua/alcantarillado) ·
1,0 = Exclusiva Importante · 0,5 = Concurrente»**, y **cada meta cita su norma** en la
columna `Justificación R_i`:

| Meta | Competencia | R_i_raw | Fuente citada |
|---|---|---|---|
| Agua potable | Exclusiva_Crítica | 1,5 | COOTAD Art. 55d |
| Vialidad | Exclusiva_Crítica | 1,5 | COOTAD Art. 55f |
| Talento humano | Exclusiva_Importante | 1,0 | COOTAD Art. 57 |
| Salud integral | Concurrente_Crítica | 0,5 | COOTAD Art. 135 |

**Esto está bien hecho y hay que decirlo:** la desigualdad de peso no nace del criterio
del analista, sino de la competencia que el COOTAD asigna al GAD. Es la Regla de Oro 3
aplicada a la ponderación — y es lo que impide que QUIRA fije política pública decidiendo
por su cuenta qué importa más.

**PERO la magnitud la decide el dinero.** `H14!A3`: *«P_i = Peso financiero
normalizado»*. El denominador es `P_i × R_i`, de modo que el índice pondera por
**presupuesto × relevancia jurídica**. Consecuencia medible:

- `SC-L-N-02` (talento humano, R=1,0) tiene **P_i = 0,3079** — mayor que
  `SC-I-N-01` (agua potable, R=1,5) con **P_i = 0,2736**.
- `SC-I-N-03` (participación ciudadana) tiene **P_i = 0,001**: es prácticamente
  invisible en el índice porque mueve poco presupuesto.

> **Una meta de derecho fundamental con poco presupuesto pesa casi nada.** El agua
> termina primera (34,9 %) porque su R la compensa, pero el orden de magnitud lo fija el
> gasto, no el derecho. Si eso es deliberado, debe declararse; si no lo es, es deuda.

### 6.2 · Las etapas de la obra — el vocabulario existe y está inerte

`H13` filas 8-11 definen **tres niveles por verificador**, con criterio escrito:

```
V_SERCOP   1,0 adjudicado publicado  ·  0,5 registrado NO adjudicado  ·  0,0 sin proceso
V_eSIGEF   1,0 devengado > 0         ·  0,5 codificado SIN devengar   ·  0,0 sin registro
V_LOTAIP   1,0 documento accesible   ·  0,5 URL no accesible          ·  0,0 sin URL
V_CPCCS    1,0 mencionada con evid.  ·  0,5 mencionada sin evidencia  ·  0,0 no mencionada
```

**Medido: ninguna de las 25 metas usa el 0,5 en ningún verificador.** Todo está en 0 o
en 1. La escala que distingue *publicado* de *adjudicado* está documentada, tiene
criterio, y no se aplica.

Y aunque se aplicara, **la fórmula de `V_i` la ignoraría**:

```
=SI(O(V_eSIGEF=0, V_SERCOP=0), 0, SI(O(V_LOTAIP=1, V_CPCCS=1), 1, 0.5))
```

Un `V_eSIGEF = 0,5` —codificado, nunca pagado— **no es 0**, así que pasa al segundo `SI`
y, si hay transparencia, sale **`V_i = 1,0`**: puntúa igual que una obra devengada.

**Y la cadena no llega al final.** `V_eSIGEF = 1,0` significa *devengado*, es decir
**pagado** — no *recibido*, no *funcionando*. Entre «se pagó» y «la obra sirve» hay un
tramo que el índice no observa: acta de entrega-recepción, informe de fiscalización,
puesta en servicio.

    planificado → publicado → adjudicado → codificado → devengado → RECIBIDO → EN SERVICIO
    └── fuera (V_POA no entra) ──┘         └── modelado ──┘        └── no modelado ──┘

> La intuición de Javo es correcta y el modelo ya tiene la mitad de la respuesta: sabe
> distinguir las etapas, decidió no usarlas, y no observa el tramo final.

### 6.3 · HALLAZGO GRAVE — el ICPI 2026 lee verificaciones de 2025

`H12!D6`, la fórmula que trae `V_i` a cada meta del motor vigente:

```
=IFERROR(VLOOKUP(A6, H13_VARIABLES_Vi!$A:$F, 6, FALSE), "⚠️ Vi NO ENCONTRADO")
```

La columna 6 del rango `A:F` es **`F`**. Y `H13!F24`, su cabecera, dice: **`Vi_2025`**.
La sección que la contiene, `H13!A23`, se titula: *«VALORES Vi DE REFERENCIA 2025 (para
verificar ICPI_Real_2025…)»*.

**Barrida la hoja completa: no existe ninguna otra tabla de `V_i`.** Es la única, y el
motor 2026 la consume como su verificación vigente.

> El ICPI publicado como **2026** toma su dimensión de verificación intersistémica de una
> tabla que el propio Gold Master rotula **de referencia 2025**, y que fue construida
> para verificar el índice del año anterior.

Es «período mezclado» en el sentido exacto del protocolo GM-Ω. No se afirma que sea un
error —puede que `V_i` se considere estable entre años, o que la actualización esté
pendiente— pero **eso no está declarado en ninguna parte**, y un índice anual que lee
verificaciones del año previo debe decirlo en su propia cara.

---

## 7 · GENEALOGÍA — la intención documental original  `GM-Ω-ICPI-001`

El colega puso la condición: *«no convertir anomalía en veredicto sin reconstruir la
regla que la produjo»*. Javo aportó la fuente primigenia —las tesis con que nació QUIRA,
`tesis historicas/`— y ahí está la intención, con fundamentación jurídica variable por
variable.

### 7.1 · Lo que el ICPI dice ser

> **ICPI = Índice de CONGRUENCIA PROGRAMÁTICA E INTERSISTÉMICA**
> *«calculado mediante auditoría algorítmica del SIAP»*, como contraparte del **ICM**
> auto-reportado por el GAD en SIGAD. La tesis investiga **la brecha ICM − ICPI**, y la
> declara sustantiva si supera **30 puntos**.

**No es un índice de cumplimiento.** Mide si lo programado es *congruente* a través de
los sistemas transaccionales del Estado. Eso reencuadra el «veto» de la sección 2: exigir
presencia en los silos **no es un accidente, es el constructo**.

Y es **determinístico, no inferencial**: *«opera sobre el universo exacto de datos
devengados registrados en e-SIGEF para las metas incluidas en la muestra estratégica.
Las brechas no son estimaciones con margen de error; son hechos fácticos.»*

### 7.2 · Las seis variables, con su nombre y su ley

| Var | Nombre original | Fundamento citado |
|---|---|---|
| `P_i` | Coeficiente de **Peso Presupuestario** | COPFP Art. 54 |
| `R_i` | Coeficiente de **Relevancia Normativa** | COOTAD 54-55 + CE 3, 12, 66 |
| `V_i` | **Inmutabilidad Documental** (Filtro de Interoperabilidad Cero) | CE 18 · LOTAIP 7 · NCI 410-11 CGE · LOSNCP 7 |
| `E_i` | Coeficiente de **Fricción de Autonomía** | ejecución directa vs delegada |
| `T_i` | **Materialización Temporal** | COPFP 115-117 · Acuerdo 067 MEF |
| `C_i` | **Trazabilidad Orgánica** (imputabilidad responsable) | — |

**`P_i` tiene justificación anti-gaming explícita**, y responde por adelantado a la
Prueba 6 del colega:

> *«Esto impide que metas de bajo costo ($5K en talleres) inflen artificialmente el
> índice mientras metas estratégicas ($8.5M en alcantarillado) permanecen paralizadas.»*

**`R_i` tiene jerarquía constitucional declarada**, y responde a la pregunta de Javo:

> *«Un GAD que cumple 80 % en cultura pero 20 % en agua potable tiene peor ICPI que uno
> con 80 % en agua y 20 % en cultura. Esto refleja la jerarquía legal: no todas las
> competencias valen igual.»*

### 7.3 · LAS DIVERGENCIAS — diseño 2026-04 vs. motor v5.7

Aquí está lo que GM-Ω vino a buscar. **La metodología original es más exigente que su
implementación**, y en los cinco casos la diferencia va en la misma dirección: se
perdió el eslabón que certifica que la obra existe.

| # | Tesis fundacional | Gold Master v5.7 | Veredicto |
|---|---|---|---|
| 1 | `V_i = V_POA ∧ V_SERCOP ∧ V_LOTAIP ∧ V_CPCCS` — **AND de cuatro silos** | `V_POA` **excluido**, `V_eSIGEF` **añadido**, y el AND sustituido por veto-de-dos + OR-de-dos | **divergente**; el cambio del AND no tiene justificación escrita |
| 2 | Criterio `V_LOTAIP` = *«PDF contrato descargable **+ acta entrega-recepción**»* | *«Documento en URL pública — accesible»* | **se perdió la entrega** |
| 3 | Criterio `V_SERCOP` = estado **«Adjudicado» o «Finalizado»** (vs. Desierto/Cancelado) | *«Proceso adjudicado publicado»* | «Finalizado» dejó de distinguirse |
| 4 | **Compromiso NO cuenta** — *«promesa, no materialización»* | `V_eSIGEF = 0,5` (codificado sin devengar) **pasa el veto** y con transparencia da `V_i = 1,0` | **divergente**: la promesa puntúa como la ejecución |
| 5 | `T_i = Devengado al 31/12 / Codificado Vigente` — ratio **por meta** | 19 de 25 comparten `0,3035` | probable ratio global; contradice la granularidad declarada |

### 7.4 · Y D-001 se reduce: era la etiqueta, no el método

La tesis declara, en la definición de la fórmula:

> **«n = Número de metas en la MUESTRA ESTRATÉGICA del PDOT»**

**La metodología nunca prometió el total.** Fue el Gold Master el que rotuló esa celda
`Total_Metas_PDOT` (`H04!B7`). El alcance sigue siendo 25 de 66 y eso limita lo que el
ICPI puede afirmar — pero **D-001 deja de ser «el motor miente sobre su universo» y pasa
a ser «una celda está mal rotulada»**. La honestidad estaba en el origen; se perdió al
escribir la etiqueta.

### 7.5 · El baremo AVEP, y de dónde salió «Gestión por Ocurrencia»

| Rango | Categoría | Señal para CGE/CPCCS |
|---|---|---|
| 90-100 % | Excelencia en Trazabilidad | Certificación de calidad |
| 70-89 % | Gestión por Mandato | Monitoreo rutinario |
| 40-69 % | Transición Crítica | Auditoría focalizada |
| **20-39 %** | **Gestión por Ocurrencia** | Auditoría integral |
| 0-19 % | Ruptura Sistémica | Intervención inmediata |

Montecristi, con **27,4582 %**, cae en *Gestión por Ocurrencia*. Es el mismo rótulo que
`H20b!C11` usa para el IGP de 2025 — el vocabulario es coherente en todo el sistema.

### 7.6 · La conclusión que cambia el dictamen

> **El Gold Master no tiene una metodología equivocada: tiene una metodología correcta
> implementada a medias.** En los cinco puntos divergentes, la tesis era MÁS exigente —
> pedía POA, acta de entrega-recepción, estado «Finalizado», y excluía la promesa. La
> implementación relajó cada uno de esos requisitos sin dejar constancia de por qué.

Eso convierte a GM-Ω de «auditoría en busca de errores» en algo más útil: **la
reconstrucción de un estándar que el propio proyecto se fijó y que su motor dejó de
cumplir.**

---

## 8 · Lo que esta ficha NO responde

- **Procedencia documental completa** (`GM-Ω-ICPI-005`): falta bajar de `H14`, `H13`,
  `H07b` y `H01 §M` hasta el documento y la fuente institucional de cada valor.
- **Transferibilidad LATAM** (`GM-Ω-ICPI-010`): SERCOP, eSIGEF, LOTAIP y CPCCS son
  instituciones **ecuatorianas**. El núcleo matemático parece separable del adaptador
  institucional, pero eso hay que demostrarlo, no suponerlo.
- **El nombre** (`GM-Ω-ICPI-011`): Javo señala que «ICPI» viene de TERRA/QUADRUM, no de
  QUIRA. Renombrar antes de cerrar el diagnóstico sería poner etiqueta nueva a un
  contenido no auditado — exactamente lo que esta auditoría persigue.

---

## 9 · Dictamen preliminar (no es el dictamen)

**El motor está bien construido y puede estar midiendo mal el fenómeno.** Son dos cosas
distintas y ambas son ciertas:

| Verdad | Estado |
|---|---|
| **Matemática** — ¿la fórmula calcula lo que dice? | ✅ reproducible, verificada, con axioma propio |
| **Epistemológica** — ¿la variable significa lo que dice? | 🔴 `V_i=0` significa dos cosas incompatibles |
| **Empírica** — ¿la evidencia permite afirmarlo? | 🟡 sí para OBRA; para SERVICIO/NORMATIVO la evidencia existe (LOTAIP/CPCCS) y el índice la ignora |
| **Temporal** — ¿el período de la evidencia es el del índice? | 🔴 el ICPI 2026 lee `Vi_2025` |

**Los tres hallazgos comparten una raíz**: el modelo tiene el vocabulario para hacer las
distinciones correctas —naturaleza de la meta, etapas de la contratación, período de la
verificación— y en los tres casos **el vocabulario está declarado y no se aplica**. No es
un motor mal construido: es un motor cuya semántica quedó a medio implementar, y nadie
podía verlo porque la aritmética siempre cerró.

*Dylus Lab © 2026 · GM-Ω Fase 0 · no modifica el Gold Master*
