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

## 6 · Lo que esta ficha NO responde

- **Procedencia documental completa** (`GM-Ω-ICPI-005`): falta bajar de `H14`, `H13`,
  `H07b` y `H01 §M` hasta el documento y la fuente institucional de cada valor.
- **Transferibilidad LATAM** (`GM-Ω-ICPI-010`): SERCOP, eSIGEF, LOTAIP y CPCCS son
  instituciones **ecuatorianas**. El núcleo matemático parece separable del adaptador
  institucional, pero eso hay que demostrarlo, no suponerlo.
- **El nombre** (`GM-Ω-ICPI-011`): Javo señala que «ICPI» viene de TERRA/QUADRUM, no de
  QUIRA. Renombrar antes de cerrar el diagnóstico sería poner etiqueta nueva a un
  contenido no auditado — exactamente lo que esta auditoría persigue.

---

## 7 · Dictamen preliminar (no es el dictamen)

**El motor está bien construido y puede estar midiendo mal el fenómeno.** Son dos cosas
distintas y ambas son ciertas:

| Verdad | Estado |
|---|---|
| **Matemática** — ¿la fórmula calcula lo que dice? | ✅ reproducible, verificada, con axioma propio |
| **Epistemológica** — ¿la variable significa lo que dice? | 🔴 `V_i=0` significa dos cosas incompatibles |
| **Empírica** — ¿la evidencia permite afirmarlo? | 🟡 sí para OBRA; para SERVICIO/NORMATIVO la evidencia existe (LOTAIP/CPCCS) y el índice la ignora |

*Dylus Lab © 2026 · GM-Ω Fase 0 · no modifica el Gold Master*
