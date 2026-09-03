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
mayoría de metas.

⚠️ **RESUELTO EN §7-ter.1 — NO era una carencia.** `T_i` mide ejecución **por ENTIDAD
EJECUTORA**, no por meta: 19 metas las ejecuta el GAD central (0,3035), 2 el Patronato
(0,6560) y 3 EP Aseo (1,0). Coincide con la tesis, que define `T_i = Devengado /
Codificado` — un ratio institucional. Se conserva este párrafo con su corrección al lado
porque la secuencia del hallazgo es parte de la evidencia.

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
| 1 | `V_i = V_POA ∧ V_SERCOP ∧ V_LOTAIP ∧ V_CPCCS` — **AND de silos** ⚠️ *ver §7-bis: la tesis de licenciatura define CINCO, con eSIGEF* | `V_POA` excluido y el AND sustituido por veto-de-dos + OR-de-dos | **divergente en el AND**; eSIGEF resultó ser evolución documentada, no divergencia |
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

## 7-bis · ACTA DE NACIMIENTO METODOLÓGICA  `GM-Ω-ICPI-001 · cerrado`

### El testigo documental: son DOS, y difieren

Javo aportó tres tesis advirtiendo que no sabía en qué se diferenciaban. **Sí importa**,
y el escalón 7 de la escalera se aplica aquí: *lo leído ≠ la fuente*. La primera pasada
de esta ficha leyó **una** y afirmó sobre las tres.

| Documento | Extensión | Qué aporta |
|---|---|---|
| **«MACRO TRAYECTO DE VIDA · más antigua completa»** | 324.939 car | **operacionalización completa**: fases del ciclo presupuestario, acta entrega-recepción (×9), «promesa no materialización», «muestra estratégica» |
| **«DE LICENCIATURA · menos punitiva»** | 110.988 car | fórmula íntegra + **`V_i` con CINCO silos** y su fundamento constitucional |
| «borrador inicial punitivo» | 112.677 car | sin fórmula ni definiciones operacionales — descartado como testigo |

**No se contradicen: se complementan**, y cada una tiene algo que la otra no.

⚠️ **CORRECCIÓN A LA PASADA ANTERIOR.** Esta ficha afirmó que el motor «añadió eSIGEF,
que no estaba en la definición original». **Es falso.** La tesis de licenciatura define:

> `V_i = V_POA ∧ V_SERCOP ∧ **V_eSIGEF** ∧ V_LOTAIP ∧ V_CPCCS`
> *«Es la variable más importante del modelo porque operacionaliza el artículo 18 de la
> Constitución —derecho a información verificada— y el artículo 7 de la LOTAIP.»*

eSIGEF **sí** estaba. La divergencia real es otra y más estrecha.

### Identidad reconstruida

| Elemento | Reconstrucción |
|---|---|
| Nombre | Índice de **Congruencia Programática e Intersistémica** |
| Constructo | congruencia entre mandato programático y trazabilidad intersistémica |
| Contraparte | **ICM** auto-reportado por el GAD en SIGAD |
| Unidad de análisis | la meta |
| Universo | **muestra estratégica** de metas del PDOT |
| Finalidad | detectar congruencia o **ruptura documental** del mandato |
| Naturaleza | **determinística, no inferencial** — censo del universo analizado |
| Escala | AVEP · 5 rangos, de «Ruptura Sistémica» a «Excelencia en Trazabilidad» |
| Propósito anti-gaming | que metas pequeñas no compensen metas estratégicas paralizadas |
| Lo que NO debe medir | eficiencia del gasto (vive en ISP y d05) · participación (d08) · control social (d09) |
| Estado | **baseline congelado: 27,4582 %** |

### Matriz de genealogía  `TESIS → GOLD MASTER`, con la clasificación del colega

| # | Divergencia | Clasificación | Evidencia |
|---|---|---|---|
| 1 | eSIGEF entre los silos | ✅ **EVOLUCIÓN JUSTIFICADA** | está en la tesis de licenciatura |
| 2 | `V_POA` excluido | 🟡 **ADAPTACIÓN DOCUMENTADA** | `H13!A3`: *«V_POA (S3) NO entra — es verificador de programación, no de ejecución»* |
| 3 | AND → veto-de-dos + OR-de-dos | 🟡 **ADAPTACIÓN PARCIALMENTE DOCUMENTADA** | `H13!B21` justifica el paso desde una fórmula **intermedia** (`SI(suma≥2;0,5)`, en `H02!B80`), **no desde el AND original**. El tramo AND → conteo no tiene razón escrita |
| 4 | Criterio LOTAIP pierde el **acta entrega-recepción** | 🔴 **PÉRDIDA DE ESPECIFICACIÓN** | sin justificación en ninguna celda ni documento |
| 5 | Criterio SERCOP pierde el estado **«Finalizado»** | 🔴 **PÉRDIDA DE ESPECIFICACIÓN** | sin justificación |
| 6 | `V_eSIGEF = 0,5` (compromiso) pasa el veto | 🔴 **PÉRDIDA LATENTE** | la tesis lo excluye —«promesa, no materialización»—; hoy ninguna meta usa 0,5, así que el defecto está inactivo pero armado |
| 7 | `T_i` uniforme en 19 de 25 | ⬜ **NO DETERMINABLE** | falta establecer si es ratio global deliberado o carencia de granularidad |
| 8 | Etiqueta `Total_Metas_PDOT` sobre una muestra | 🔴 **PÉRDIDA DE ESPECIFICACIÓN** | la tesis dice «muestra estratégica»; el rótulo promete el total |

### Una observación sobre el método de calibración

`H13!B21` dice que la fórmula se corrigió porque *«los valores Vi_2025 canónicos prueban
que AH-I-X-02 tiene Vi=0.0»*. Es decir: **la regla se ajustó para reproducir un resultado
conocido.** Es una práctica legítima de calibración —y honesta, porque está escrita— pero
conviene nombrarla: cuando la regla se ajusta al caso, el caso deja de poder validarla.
La validación tendría que venir de fuera de esa serie.

---

## 7-ter · MATRIZ DE PROCEDENCIA  `GM-Ω-ICPI-004`

**Las 150 celdas, una por una, están en
[`GM-OMEGA_ICPI_MATRIZ_004.md`](GM-OMEGA_ICPI_MATRIZ_004.md)** — derivada del Gold
Master por `scripts/gm_omega/matriz_procedencia_icpi.py`, no escrita a mano.

⚠️ La primera versión de esta sección comprimió las 150 celdas en 6 patrones. El colega
lo corrigió: *«el patrón por variable no sustituye la trazabilidad de las 150 celdas»*, y
tenía razón — comprimir responde «cómo se calcula esta variable», no «por qué ESTA meta
tiene ESTE número». Y escribir la tabla a mano habría reproducido el patrón del
«48,33 %» dentro de la auditoría que lo persigue: se DERIVA cada vez.

### Estado provisional de trazabilidad (acordado con el colega · NO son veredictos)

| Var | Estado | Por qué |
|---|---|---|
| `P_i` `R_i` `C_i` | `provenance provisionally verified` | referencia o fórmula, con norma citada en `R_i` |
| `T_i` | `provenance verified · sensitivity pending` | origen claro; el tope `MIN(1,…)` se juzga en 007 |
| `V_i` | 🔴 `TEMPORAL_SEMANTIC_GAP` | la columna leída se llama `Vi_2025` |
| `E_i` | 🟡 `PARCIALMENTE_VERIFICADO` | la **regla existe** en la tesis (COOTAD 54 · NCI 200-04); lo que no consta en el libro es la MODALIDAD de cada meta |

⚠️ **`E_i` estuvo clasificado aquí como `UNTRACEABLE`, y era afirmar más de lo medido.**
El colega lo frenó: *«una cosa es "no tiene procedencia declarada en el Gold Master" y
otra muy distinta "es epistemológicamente imposible de rastrear"»*. Agotada la búsqueda:
no deriva de `Competencia_GAD` —`Exclusiva_Crítica` toma 0,75 y 1—, no deriva de la
entidad ejecutora —EP Aseo toma los tres valores—, **pero la tesis SÍ define su regla**:

| Modalidad de ejecución | `E_i` | |
|---|---|---|
| directa por direcciones del GAD | 1,00 | control total, rendición directa |
| compartida por convenio interinstitucional | 0,90 | responsabilidad compartida |
| **delegación a entidad adscrita** (EP municipal, patronato) | **0,75** | fricción por autonomía administrativa |

Y la tesis añade una aclaración que conviene conservar: *«`E_i` no penaliza la delegación
como mala práctica […] reconoce que cuando la ejecución se delega, la trazabilidad
directa del GAD sobre esa inversión se debilita»*.

**Al contrastar la regla con los valores aparece una incoherencia: 5 de las 6 metas
ejecutadas por entidades adscritas tienen `E_i` distinto de 0,75.** Sólo `AH-I-N-01`
(EP Aseo, 0,75) concuerda.

⚠️ **No se declara defecto**, y la distinción importa: la entidad se infiere de la
columna de `T_i` —el mejor proxy del libro— y la **modalidad real** de ejecución no
consta en ninguna celda. Señalar dónde la regla documentada y el valor no concuerdan es
medir; llamarlo error sería afirmar sobre lo que no se midió.

#### Y la incoherencia no era un error: era una corrección de Javo

> *«castigar la institucionalidad del GAD solo por derivar una obra del GAD a EP Aseo o
> al Patronato, y castigar a la entidad adscrita, no es técnicamente viable: es la misma
> institucionalidad. NO es otro nivel de gobierno. Por eso lo cambié.»*

**Tiene razón, y su corrección es más coherente con QUIRA que la regla original.** Dos
argumentos, y el segundo es de doctrina:

1 · **Institucional.** Una EP municipal o un patronato se crean por ordenanza del propio
GAD, su directorio lo preside el Alcalde y su presupuesto se consolida. Otro nivel de
gobierno sería la prefectura, un ministerio o una junta parroquial. Penalizar al GAD por
usar la figura que la ley le concede penaliza **una forma de organización, no un
resultado**.

2 · **Doble conteo, y contra la propia doctrina.** Si delegar debilitara la
trazabilidad, **`V_i` ya lo mediría**: verifica el rastro real en SERCOP, eSIGEF, LOTAIP
y CPCCS. Si la EP no deja rastro, `V_i` lo detecta. Con la regla de la tesis, `E_i`
penalizaría el mismo fenómeno **por presunción** mientras `V_i` lo penaliza **por
evidencia** — y QUIRA existe para lo segundo. Presumir que «una EP rastrea peor» es
imputar sin verificar.

**Clasificación corregida:** no es `PÉRDIDA DE ESPECIFICACIÓN` sino
**`EVOLUCIÓN DELIBERADA · sin documentar`**. La decisión es correcta; lo que falta es su
constancia.

#### Lo que queda pendiente, y es una pregunta para Javo

Si la delegación intra-GAD ya no penaliza, entonces **las 5 metas en 0,75 y las 4 en
0,90 necesitan otro criterio**, y ése no consta en ninguna celda:

| `E_i` | Metas | Patrón visible |
|---|---|---|
| 0,75 | desechos sólidos · alcantarillado · modernización administrativa · participación ciudadana · señalización vial | ninguno identificable desde el libro |
| 0,90 | sostenibilidad financiera · **salud integral** · equipamiento urbano · **inventario patrimonial** | dos involucran a otra institución del Estado (Ministerio de Salud, INPC) |
| 1,00 | las 16 restantes, **incluidas dos de EP Aseo y Patronato** | coherente con la corrección |

⚠️ **AQUÍ PROPUSE UN CRITERIO Y ERA UNA HIPÓTESIS MÍA, NO UN HALLAZGO.** Escribí que
«la fricción existe cuando interviene otra institucionalidad», y el colega lo frenó:

> *«no debemos pasar de "la regla de la tesis fue superada" a "el nuevo criterio es 0,90
> cuando interviene otra institucionalidad". Eso último todavía sería una hipótesis
> nuestra, no un hecho medido.»*

Tiene razón, y es el mismo exceso que esta auditoría lleva cometiendo: **inferir una
regla desde los datos y enunciarla como si estuviera medida**. Que el 0,90 de salud y el
de patrimonio *encajen* con esa hipótesis no la demuestra — encajar no es derivar, y con
25 casos y tres valores posibles, cualquier hipótesis encuentra algunos que la respaldan.

    «La regla anterior fue descartada»  ≠  «ya conocemos la regla nueva».

### `E_i` clasificado por capas (propuesta del colega, adoptada)

| Elemento | Estado |
|---|---|
| Existencia de `E_i` como variable | ✅ `VERIFICADO` |
| Definición conceptual (fricción de autonomía) | ✅ `VERIFICADO` — tesis |
| Regla histórica 1,00 / 0,90 / 0,75 | ✅ `VERIFICADO` — **como regla histórica** |
| Razón para abandonar la penalización a adscritas | ✅ `VERIFICADO` — evolución declarada por Javo |
| Valores actuales de cada meta | ✅ `VERIFICADO` — como valores del Gold Master |
| **Regla que produce hoy cada 0,75 / 0,90 / 1,00** | 🔴 **`NOT_DETERMINABLE`** |
| Modalidad institucional de cada meta | 🔴 `NOT_DETERMINABLE` |
| Nueva especificación canónica de `E_i` | ⬜ **pendiente de decisión GM-Ω** |

**Y por eso `E_i` NO entra todavía a 007.** El colega lo formula con precisión: sería
*«hacer un análisis de sensibilidad de una variable cuya regla de asignación no está
identificada — matemáticamente elegante y epistemológicamente débil»*. Antes hace falta
**007-B0 · genealogía de `E_i`**, con la misma prueba de biografía: ¿se puede reconstruir
por qué vale 0,75 sin mirar el resultado esperado? Hoy la respuesta es no.

Los cinco valores en 0,75 y los cuatro en 0,90 quedan **sin criterio identificado**, y
eso es lo que hay que decir — no una explicación que los acomode.

### 007-B0 · Genealogía de `E_i`: cuándo nació cada valor

El colega añadió la pregunta temporal —*«si los valores fueron asignados manualmente
durante una versión posterior, eso explicaría por qué la tesis tiene una regla y el GM
otra distribución»*—. Se midió sobre **siete versiones del Gold Master**:

| Versión | Fecha | `E_i` |
|---|---|---|
| `ECIAP v1.1` | 10-may-2026 | ya los actuales |
| `v4.1` | 14-may | idénticos |
| `v5.0` · `v5.4` · `v5.5` | 16 a 30-may | idénticos |
| candidato `v5.7` | 30-jul | idénticos |
| **`v5.7` vigente** | hoy | **idénticos** |

**Metas cuyo `E_i` cambió entre versiones: 0 de 25.**

La hipótesis de la asignación posterior **queda descartada**: los valores nacieron con la
primera versión conservada y no se tocaron en cuatro meses. Y la tesis es de **abril**,
anterior a todas.

> **La regla escrita y los valores implementados nunca coincidieron.** No hubo un evento
> de cambio que explique la divergencia: la divergencia nació con la implementación
> misma.

Eso matiza lo que Javo recordaba —«por eso lo cambié»—: lo que cambió fue **la doctrina**,
no los valores. O el cambio ocurrió antes de que existiera cualquier Gold Master
conservado, y entonces **no queda rastro de él**.

Dato de linaje que aparece de paso: la cabecera de `ECIAP v1.1` dice **«ECIAP-EGG-7.8 by
GNOMIKA»**. El motor tiene un linaje anterior a QUIRA —y anterior incluso a SIAP—, lo que
conecta con la observación de Javo sobre el nombre «ICPI» viniendo de TERRA/QUADRUM.

### Clasificación de las 25 metas (taxonomía A/B/C/D del colega)

| | Casos | |
|---|---|---|
| **A · RECONSTRUIBLE** — fuente + regla + dato | **0** | no hay regla que produzca los valores |
| **B · REGLA CONOCIDA / DATO FALTANTE** | **0** | la regla de la tesis existe pero **fue superada**; la vigente no está escrita |
| **C · VALOR CONOCIDO / REGLA NO RECONSTRUIBLE** | **25** | 🔴 `NOT_DETERMINABLE` |
| **D · CONTRADICCIÓN DOCUMENTAL** | **0** | no hay fuente que declare la modalidad de cada meta, así que nada puede contradecirla |

**Ninguna de las 25 pasa la prueba de biografía**: no se puede reconstruir por qué una
meta recibió 0,75 sin mirar el resultado. `E_i` es la única variable del ICPI en esa
situación.

**Declararlo es lo que falta.** Sin criterio escrito, la próxima auditoría —o el GAD
número 47— no podrá saber por qué una meta vale 0,75 y otra 1,00. Es el mismo patrón
que esta auditoría lleva encontrando toda la sesión, sólo que al revés: aquí **la mejora
es la que no dejó rastro**.

El resumen por variable se conserva abajo porque el patrón **sí** es idéntico dentro de
cada una, y saberlo es parte del hallazgo.

| Var | Origen (25/25) | Trazable | Período | Naturaleza |
|---|---|---|---|---|
| `P_i` | `=H14_PONDERADORES!G{n}` | ✅ referencia directa | codificado vigente | DERIVADO |
| `R_i` | `=H14_PONDERADORES!F{n}` → `(R_raw × Bono)/1,725` | ✅ fórmula + norma citada por meta | permanente | NORMATIVO |
| `V_i` | `VLOOKUP(A{n}, H13!$A:$F, 6)` → columna **`Vi_2025`** | ✅ trazable | **2025** | 🔴 **HISTÓRICO usado como ACTUAL** |
| `E_i` | **literal** (16 enteros + 9 decimales) | 🔴 **sin fórmula, sin referencia, sin fuente en el libro** | — | ⬜ NO DETERMINABLE |
| `T_i` | `=H07b!B20` (19) · `!C20` (2) · `!E20` (3) | ✅ pero **por ENTIDAD**, no por meta | 2026 vivo | ACTUAL |
| `C_i` | `VLOOKUP(A{n}, H01!$A$189:$G$213, 6)` | ✅ trazable | — | DERIVADO |

### 7-ter.1 · `T_i` resuelto: mide la ENTIDAD, no la meta

⚠️ **CORRECCIÓN A LA SECCIÓN 4 de esta ficha.** Ahí se dijo que 19 de 25 metas comparten
`T_i` y que «habrá que determinar si es un agregado legítimo o una carencia de dato».
**Es lo primero, y es deliberado.** La fila `Ti_norm_2026` de `H07b` tiene una columna
por entidad ejecutora:

| Columna | Valor | Entidad | Metas |
|---|---|---|---|
| `B20` | 0,3035 | ENTE-01 **GAD central** | 19 |
| `C20` | 0,6560 | ENTE-02 Patronato | 2 |
| `E20` | 1,0000 | ENTE-04 EP Aseo | 3 |

Coincide con la tesis, que define `T_i = Devengado / Codificado` — un ratio **de la
entidad**, no de la meta. No es falta de granularidad: es la unidad de medida elegida.

**Lo que sí exige declaración**: una meta bien ejecutada dentro de una entidad con baja
ejecución global **hereda el ratio de su entidad**. Es defendible —la ejecución
presupuestaria es institucional— pero significa que `T_i` no premia ni castiga la meta:
premia o castiga a quien la ejecuta.

### 7-ter.2 · El tope que borra información

```
Ti_norm = MIN(1, Ti_raw / FactorTemporal)        FactorTemporal = mes/12
```

El `MIN(1, …)` es correcto —no se ejecuta más del 100 %— pero **satura**: EP Aseo llega
a `1,0000` exacto, y en ese punto «justo a ritmo» y «muy por delante» se vuelven
indistinguibles. Tres de las 25 metas están en el tope.

### 7-ter.3 · `E_i` es el único componente sin biografía

**Las 25 celdas de `E_i` son literales.** No hay fórmula, no hay referencia, no hay
fuente citada en el libro. Y es la única de las seis variables en esa situación.

Lo notable es que **podría derivarse**: `H14` ya trae `Competencia_GAD` por meta
—`Exclusiva_Crítica`, `Exclusiva_Importante`, `Concurrente_Crítica`— y `E_i` es
justamente el «Coeficiente de Fricción de Autonomía» (1,0 autónomo · 0,9 compartido ·
0,75 difuso). El dato para derivarlo existe a dos columnas de distancia.

> No se afirma que los valores sean incorrectos: se afirma que **no son verificables
> desde el libro**. Es el único punto del árbol donde la cadena `celda → regla → fuente`
> se interrumpe.

---

## 7-quater · TEMPORALIDAD Y DETERMINABILIDAD  `GM-Ω-ICPI-005`

Clasificación temporal de cada insumo, con la taxonomía del colega:

| Insumo | Período real | Se presenta como | Estado |
|---|---|---|---|
| `P_i` | codificado vigente | actual | ✅ `ACTUAL` |
| `R_i` | permanente (norma) | actual | ✅ `NORMATIVO` |
| **`V_i`** | **2025** | 2026 | 🔴 **`HISTÓRICO` presentado como `ACTUAL`** |
| `T_i` | 2026 Ene-Abr, normalizado | actual | ✅ `ACTUAL` |
| `C_i` | tabla de calibración | actual | ✅ `DERIVADO` |
| `E_i` | — | actual | ⬜ `NO_DETERMINABLE` |

**Un solo insumo de seis rompe la coherencia temporal, y es `V_i`** — pero es
precisamente la variable que la tesis llama *«la más importante del modelo»*.

### Datos PROXY y SIMULADOS: dónde están y dónde NO

`H07b` contiene, en la serie histórica **2023**, dos valores declarados como no
observados: `D16 = "PROXY 77%"` (Bomberos) y `E16 = "SIMULADO-MPE"` (EP Aseo).

**Verificado: no entran en el ICPI 2026.** El motor consume la fila 20
(`Ti_norm_2026`), que deriva de la fila 19 (año 2026). Los simulados viven en la fila 16
y sólo alimentarían el índice si se activara el escalón `Ti_Hist` de la jerarquía
adaptativa.

> Es un riesgo **armado pero inactivo**, igual que el `0,5` del compromiso: la ruta
> existe, hoy nadie la toma, y el día que se tome introducirá un valor simulado en la
> cifra madre sin que nada lo declare.

### Prueba de biografía del dato — el resultado

El colega la formuló así: *«si borro el número de la celda, ¿puedo reconstruirlo desde su
evidencia de origen sin mirar primero el resultado esperado?»*

| Variable | ¿Reconstruible sin mirar el resultado? |
|---|---|
| `P_i` | ✅ desde el presupuesto codificado por meta |
| `R_i` | ✅ desde el COOTAD — la norma está citada celda a celda |
| `V_i` | 🟡 sí, **pero la regla que los combina se calibró contra el resultado 2025** (`H13!B21`) |
| `E_i` | 🔴 **no**: no hay de dónde |
| `T_i` | ✅ desde las cédulas eSIGEF/LOTAIP, con fuente citada por año |
| `C_i` | ✅ desde `TBL_CALIBRACION_Ci` |

**Cuatro de seis son reproducibles de forma independiente.** Una lo es con la salvedad de
su calibración, y una no lo es en absoluto.

---

## 7-quinquies · QUÉ SIGNIFICA UN CERO  `GM-Ω-ICPI-006`

El colega anunció que aquí estaría la conexión profunda entre el ICPI, el IGP y la regla
de QUIRA. La hay, y es más estructural de lo que parecía.

**Medido sobre el motor completo:**

```
ceros en las 150 celdas del ICPI      6   — y los SEIS son V_i
celdas vacías                          0
celdas con «N/A», «no aplica»,
«pendiente» o «sin dato» en las
cuatro hojas del núcleo                0
```

### El hallazgo

> **En el núcleo operacional auditado del ICPI —las cuatro hojas que lo alimentan— no
> existe representación explícita de estados de ausencia, no aplicabilidad o
> indeterminación: los valores observados son numéricos.**

⚠️ La primera redacción decía «el motor del Gold Master no tiene vocabulario para la
ausencia». El colega acotó bien: eso **extrapola de cuatro hojas a las 123** del libro.
Lo medido son cuatro; lo afirmado, cuatro.

No es que confunda «no ejecutó» con «no aplica»: es que **no puede distinguirlos**,
porque no existe ninguna representación para lo segundo. Cuando algo no se puede
determinar, el único valor disponible es `0`.

Y en una estructura multiplicativa eso no es «un valor bajo»:

```
J_i = P_i × R_i × V_i × E_i × T_i × C_i     un cero ANULA la meta entera
K_i = P_i × R_i                             pero la meta sigue pesando completa
```

**Un cero en `V`, `E`, `T` o `C` convierte a la meta en peso puro sin aporte** — la
penalización máxima que el modelo puede aplicar. Es el aniquilador, no un valor pequeño.

### Lo que sí está declarado, y lo que no

Para `V_i`, la tesis **lo declara y lo fundamenta**:

> *«Cuando `V_i = 0`, el sistema NO está castigando al GAD; está aplicando las normas
> vigentes: si el contrato no está en SERCOP viola LOSNCP Art. 7 […] sin evidencia
> pública verificable, la transacción no existe para efectos de certificación.»*

Eso es una decisión metodológica explícita y defendible. **El problema no es el cero: es
que sólo hay una forma de decirlo.** Cuatro situaciones ontológicamente distintas
comparten representación:

| Situación real | Cómo se representa | ¿Debería? |
|---|---|---|
| ejecutó y no dejó rastro | `0` | ✅ sí — es el caso que la tesis quiere castigar |
| no ejecutó | `0` | ✅ sí |
| **no puede dejar ese rastro** (meta normativa o de servicio) | `0` | 🔴 no |
| **no se pudo verificar** (fuente caída, dato pendiente) | `0` | 🔴 no |

Las dos últimas son las que la Capa 0 de QUIRA prohíbe expresamente colapsar. **El canon
del proyecto exige ocho estados y su motor tiene uno.**

### La conexión con el IGP

D-010 encontró exactamente lo mismo en el otro índice auditado: `IGP_2 = 0` con la nota
«actualizar cuando PP 2026 esté disponible» — un pendiente pesando como un cero, mientras
d08 tenía 191 demandas documentadas.

> **Dos de dos índices auditados carecen de vocabulario para la ausencia.** Dos de dos no
> es «el Gold Master entero» —eso está por medir— pero ya no es un caso aislado. Una hoja de cálculo representa
> magnitudes, y la epistemología de QUIRA necesita representar *estados de conocimiento*.
> Ese desajuste no se arregla cambiando una fórmula.

### La pregunta que queda abierta, y la salida que no es «sustituir ceros por NA»

El colega la formula con precisión: **¿el cero es una propiedad matemática o una
propiedad epistemológica?** En `V_i` puede ser perfectamente intencional —«no hay
evidencia documental suficiente → no certifico»— y eso NO es lo mismo que «no ocurrió».
El ICPI original parece haber querido exactamente lo primero.

Por eso la reparación futura probablemente no sea reemplazar los ceros. Sería separar el
valor del estado:

```
VALOR = 0      ESTADO = CERTIFICABLE_CERO     ← lo que la tesis quiere castigar
VALOR = null   ESTADO = NO_APLICABLE          ← meta normativa o de servicio
VALOR = null   ESTADO = PENDIENTE             ← el caso del IGP_2
VALOR = null   ESTADO = NO_DETERMINABLE       ← fuente caída
```

Así se conserva la matemática histórica donde corresponde y se impide que el motor
confunda **el estado del fenómeno** con **el estado del conocimiento**.

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
