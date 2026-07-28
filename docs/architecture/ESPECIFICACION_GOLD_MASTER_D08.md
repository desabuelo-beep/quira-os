---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 4, 8]
  type: OPERATIVA
---

# ESPECIFICACIÓN · Lo que falta sellar en el Gold Master para d08

**2026-07-29 · a pedido de Javo:** *"falta integralmente subsanar el excel con todo lo que
corresponde al dom, sus indicadores y sus sat"*

> ⚠️ **Este documento NO modifica el Gold Master.** Regla 1: el Excel es el motor y el estado;
> **sellar es acto de Javo**, sobre copia, con evidencia. Aquí solo se especifica QUÉ falta y
> con qué evidencia se respalda. Regla 9: ningún cambio nace en Python.

---

## Matriz de trazabilidad *(qué cambio nace de qué evidencia)*

| Cambio | Evidencia origen | Dónde se decide | Estado |
|---|---|---|---|
| Conector no leía el IGP | lectura directa del GM · 2026-07-29 | Python (conector) | ✅ **hecho** |
| Composición del IGP mezcla d09 | **OBS-015** | Excel · **Javo** | ⏳ |
| `IGP_2 = 0` — faltan montos por proyecto PP | lectura `H10b!D13:E17` | **terreno** (dato inexistente) | ⛔ bloqueado |
| Nomenclatura SAT · serie sigue en IX | **OBS-016** | Excel · **Javo** | ⏳ |
| `SAT-IX` Brecha de Atención (46,2%) | `trazabilidad_demandas.json` | Excel · **Javo** | ⏳ |
| CVI como 2ª dimensión del IOC | **OBS-020** | Excel · **Javo** · *dominio d01* | ⏳ |

---

## 0 · El diagnóstico, corregido contra el Excel real

> ⚠️ **Corrección (2026-07-29).** La primera versión de este documento afirmaba que *"d08 está
> fuera del contrato del motor"*. **Era falso**, y el error fue mío: revisé
> `_KEYS_OF_INTEREST` del conector en vez del Excel. Al leer el Gold Master:
>
> **`H73_OUTPUT_API` SÍ publica el IGP** — fila 21 `IGP_REF_2025` = 0,2798 · fila 22
> `IGP_2026_ACTUAL` = 0,4833. El motor **nunca dejó de exponerlo**.

**El hueco real estaba en Python, no en el Excel:** `app/connectors/gold_master.py` no incluía
esas claves en `_KEYS_OF_INTEREST`, así que QUIRA no las leía aunque el canon las publicara.
**Ya corregido** — el conector expone ahora un bloque `participacion`.

### Lo que el Excel dice de verdad *(verificado celda a celda)*

| Celda | Contenido real | Lectura |
|---|---|---|
| `H20b!B6` IGP_1 Asamblea CPCCS | 0,54 — `AVERAGE(H10!E18:E42)` | ✅ d08, conectado |
| `H20b!B7` IGP_2 Presup. Participativo | **0** — `AVERAGE(H10b!F13:F17)/100` | ⚠️ ver §2 |
| `H20b!B8` IGP_3 Fidelidad Narrativa | 0,91 — `AVERAGE(H34b!J11:J3x)` | ❌ **es d09** |
| `H20b!B9` IGP_Global | 0,4833 — `AVERAGE(B6:B8)` | fórmula sana |
| `H24c!B7` Monto_PP_Aprobado | **`0` literal — sin fórmula** | ⚠️ ver §3 |
| `H24c!B8` Hay_Datos_PP | `NO` — `=IF(B7>0,"SÍ","NO")` | consecuencia de B7 |

**Riesgo de escritura medido:** 0 reglas de formato condicional · 0 gráficos · 0 macros · 6
validaciones · 123 hojas. Los semáforos son emojis en texto, no formato condicional. **Escribir
con `openpyxl` es viable sin destruir el libro** — pero ver §2 antes de escribir nada.

---

## 1 · Corregir el IGP — mezcla dos dominios *(OBS-015 · Hallazgo 1)*

`H20b_IGP_GOBERNANZA_PARTICIPATIVA` compone hoy:

| Componente | Valor | Dominio real | Acción |
|---|---:|---|---|
| **IGP_1** · Asamblea CPCCS | 0,54 | d08 ✅ | conservar |
| **IGP_2** · Presupuesto Participativo | **0,00** | d08 ✅ | **alimentar** — §2 |
| **IGP_3** · Fidelidad Narrativa MFN (`H34b`) | 0,91 | **d09** ❌ | **retirar o migrar** |

**Por qué se retira IGP_3:** la Fidelidad Narrativa es *control social* (d09), no *participación
ciudadana* (d08) en términos LOPC. La frontera d08≠d09 está fijada en DEC-0004. El IGP —
indicador madre de d08— incorpora una variable de otro dominio.

> **Advertencia honesta sobre el efecto:** IGP_3 es el componente **más alto** (0,91). Retirarlo
> **hará BAJAR el IGP**. Eso no es un deterioro de la gestión del GAD: es la corrección de una
> composición previa a la separación de dominios. **Debe documentarse como cambio metodológico
> con fecha**, no como caída de desempeño, o la serie histórica se vuelve ilegible.

**Decisión pendiente de Javo:** ¿retirar IGP_3 (IGP queda con 2 componentes) o sustituirlo por
un tercer componente propio de d08? Candidato natural en §4.

## 2 · IGP_2 = 0 — **no es un bug: es ausencia de dato** ⛔

`H10b_S8b_PARTICIPATIVO` **sí tiene registro de PP 2026**: `Ingresos_Base` = 20.982.884,
`Fichas_PP` = 149, y cinco prioridades verificadas con su meta PDOT:

| Fila | Proyecto PP 2026 | `D` Monto_Aprobado | `E` Monto_Ejecutado | `F` Cumplimiento_% |
|---|---|---:|---:|---:|
| 13 | Agua Potable / Saneamiento rural | **0** | **0** | 0 |
| 14 | Áreas verdes / Parques | **0** | **0** | 0 |
| 15 | Vialidad cantonal | **0** | **0** | 0 |
| 16 | Salud / Equipamiento médico | **0** | **0** | 0 |
| 17 | Aseo / Recolección | **0** | **0** | 0 |

`IGP_2 = AVERAGE(H10b!F13:F17)/100` → promedio de cinco ceros → **0**. **La fórmula funciona
perfectamente.** El cero refleja que **no hay montos cargados por proyecto**.

> **Y ese dato no lo tengo.** Las actas procesadas producen *demandas*, no *montos asignados
> ni ejecutados por proyecto*. Rellenarlo con una estimación sería inventar cifra pública —
> exactamente lo prohibido. **`IGP_2` queda bloqueado hasta obtener del GAD el desglose de
> montos del PP** (vía acceso a información pública, como el XLSX del POA).
>
> **Esto es en sí un hallazgo de CVI:** el instrumento de PP publica *prioridades* y *número
> de fichas*, pero **no publica cuánto se asignó ni cuánto se ejecutó por prioridad**. Sin eso,
> el cumplimiento del PP es **inverificable por construcción** — el mismo patrón que OBS-020
> encontró en el POA, ahora en el PP.

## 3 · `H24c!B7` — la fórmula rota que NO debe restaurarse tal cual ⚠️

`H24c_SAT-VI_DESVÍO_PP` · dimensión **D4** · consumida por `RO-VIII-003`.

`B7` (Monto_PP_Aprobado) es un **`0` literal sin fórmula**, y su comentario dice que debería ser
`IFERROR(H10b!B9,0)` — la llamada "FALLA 17".

> ⛔ **NO restaurar esa fórmula.** `H10b!B9` es **`Ingresos_Base_2026` = 20.982.884**, es decir
> **los ingresos del GAD**, no el monto del Presupuesto Participativo. El PP es una fracción de
> la inversión, no el ingreso total. Restaurarla haría que:
> - `B7` = 20.982.884 (cifra **falsa** como monto PP)
> - `B8` `Hay_Datos_PP` → **"SÍ"** automáticamente
> - **SAT-VI se activaría sobre un dato inventado**
>
> Es la trampa más peligrosa encontrada hoy: *parece* un arreglo de una línea y **mete una cifra
> falsa al motor**. Probablemente por eso alguien anuló la fórmula en su momento.

**La fórmula correcta sería** `=SUM(H10b!D13:D17)` (suma de montos aprobados por proyecto) —
pero **da 0 hasta que §2 se desbloquee**. Se deja documentada, no aplicada.

**Acción:** ninguna sobre el Excel hasta tener los montos. Se corrige el **comentario** de `C7`
para que no vuelva a inducir la restauración equivocada — eso sí es presentación (Regla 1).

> ⛔ **CORRECCIÓN DE NOMENCLATURA — colisión detectada.** La propuesta de numerar las nuevas
> señales como `SAT-1 · SAT-2 · SAT-3 · SAT-4` **pisaría cuatro señales existentes** del Gold
> Master: `SAT-I` Fragmentación Selectiva · `SAT-II` Reforma Tardía · `SAT-III` Parálisis
> Presupuestaria · `SAT-IV` Alerta Fiscal COOTAD. **Las SAT se numeran por orden de creación /
> dimensión TGI, NO por dominio** (OBS-016). La serie actual llega a `SAT-VIII`; toda señal
> nueva continúa en **`SAT-IX`** en adelante.

### Y tres de las cuatro "SAT" propuestas NO son SAT *(Regla 7 · anti-inflación)*

| Propuesta | Qué es en realidad | Dónde vive ya |
|---|---|---|
| Excel Cáscara | **nivel del ICEP** (formato) | dimensión del **IOC** |
| Opacidad crítica | **es el IOC mismo** | `H41_IOC_OPACIDAD_CRITICA` — ya existe |
| CVI · baja capacidad verificativa | **2ª dimensión del IOC** (estructura) | `TEORIA_EVIDENCIA_PUBLICA_VERIFICABLE.md` §6-bis |
| **Brecha de atención** | **sí es señal nueva de d08** | **no existe → candidata a `SAT-IX`** |

Crear cuatro SAT donde tres son componentes de un índice existente sería inflar el marco. **La
opacidad ya tiene su indicador: el IOC.** Lo que le falta es la **segunda dimensión (CVI)**, y
eso es una fórmula del IOC, no una señal nueva.

## 4 · Lo que d08 produce hoy y el Excel todavía no recibe

Insumos **ya generados y trazables** que esperan sellado:

| Métrica | Valor medido | Fuente | Naturaleza |
|---|---:|---|---|
| Demandas ciudadanas identificadas | 223 | `demandas_ciudadanas.json` | hecho observable |
| …de naturaleza vinculante (COOTAD 238) | 191 | idem | hecho observable |
| **Brecha de atención** — sin correlato presupuestario | **103** (46,2%) | `trazabilidad_demandas.json` | hecho observable |
| Correspondencia **directa** | 68 | MRSPP v3 | propuesta · requiere validación |
| Correspondencia **funcional** | 27 | MRSPP v3 | propuesta · requiere validación |
| Correspondencia **instrumental** | **0** | MRSPP v3 | **hallazgo** — el POA no declara componentes |
| Correspondencia **complementaria** | 25 | MRSPP v3 | propuesta · requiere validación |
| Audiencias sin resolución Art. 75 | **28 / 28** | OBS-017 | hecho observable |
| Audiencias sin habilitación de presidencia | **28 / 28** | OBS-017 | hecho observable |

> ⚠️ **Regla epistémica para el sellado (Modelo Causal · Regla C2):** solo entran al Excel como
> dato duro los **hechos observables**. Las correspondencias en `pendiente_validacion` (113 de
> 223) **informan hipótesis, no conclusiones**, y no pueden alimentar un indicador publicable
> hasta la 2ª ronda de validación experta.
>
> **De la tabla anterior, hoy son sellables:** 223 · 191 · **103 (brecha)** · 28/28 · 28/28.
> El desglose del MRSPP espera validación.

### Candidata a SAT-IX · Brecha de Atención Ciudadana

| Campo | Propuesta |
|---|---|
| **Id** | `SAT-IX` *(continúa la serie — no colisiona)* |
| **Alerta** | Brecha de Atención Ciudadana |
| **Dimensión TGI** | **D4** *(la misma de SAT-VI — participación)* |
| **Métrica observable** | % de demandas ciudadanas vinculantes **sin correlato presupuestario verificable** |
| **Medición actual** | **46,2%** (103 de 223) |
| **Base legal** | COOTAD 238 — la incorporación de las prioridades del PP es **exigible** |
| **Umbral · peso** | **decisión de Javo** — se sella en el Excel, no aquí |

> **Frontera obligatoria (Carta Art. 4.5):** `sin_correlato` **NO significa "no se atendió"**.
> Significa que el expediente **no acredita** la correspondencia. La SAT mide *falta de
> acreditación documental*, no incumplimiento. La redacción de la alerta debe decir eso.
>
> Y **OBS-020 explica buena parte de esa brecha por causa externa**: si el POA localiza el 1%
> del gasto, una porción del 46,2% es **inverificable por el instrumento**, no desatención del
> GAD. Publicar la brecha sin ese matiz sería injusto y técnicamente falso.

## 5 · Exponer d08 en el contrato `H73_OUTPUT_API`

Sin esto, nada de lo anterior llega a QUIRA. Claves propuestas, siguiendo la convención
existente del contrato:

| Clave sugerida | Contenido |
|---|---|
| `IGP_GLOBAL` · `IGP_GLOBAL_PCT` | índice de gobernanza participativa (corregido, §1) |
| `IGP_CLASIFICACION` | semáforo, como `ICPI_CLASIFICACION` |
| `PP_DEMANDAS_TOTAL` · `PP_DEMANDAS_VINCULANTES` | 223 · 191 |
| `PP_BRECHA_ATENCION_PCT` | 46,2% — alimenta `SAT-IX` |
| `PC_AUDIENCIAS_SIN_RESOLUCION` | 28/28 (OBS-017) |

Tras sellarlas, añadir las mismas claves a `_KEYS_OF_INTEREST` en
`app/connectors/gold_master.py`. **Ese es el único cambio en Python, y va DESPUÉS** — el código
refleja el canon, nunca lo precede (Regla 9).

## 6 · Orden de ejecución sugerido

| # | Acción | Quién | Estado |
|---|---|---|---|
| 0 | Leer IGP desde `H73` en el conector + bloque `participacion` | dirección técnica | ✅ **hecho** |
| 1 | **Conseguir del GAD los montos del PP por proyecto** (acceso a información pública) | **Javo** — *terreno* | ⛔ **bloquea 2 y 3** |
| 2 | Cargar montos en `H10b!D13:E17` → `IGP_2` se calcula solo | **Javo** (Excel) | depende de 1 |
| 3 | `H24c!B7 = SUM(H10b!D13:D17)` — **jamás** `H10b!B9` | **Javo** (Excel) | depende de 1 |
| 4 | Decidir destino de IGP_3 (retirar / migrar / sustituir) | **Javo** | libre — §1 |
| 5 | Sellar métricas observables de §4 (223 · 191 · 103 · 28/28) | **Javo** (Excel) | libre |
| 6 | Crear `SAT-IX` Brecha de Atención (umbral y peso) | **Javo** (Excel) | tras 5 |
| 7 | Exponer claves nuevas de d08 en `H73` + añadirlas al conector | Javo → dirección técnica | tras 5-6 |
| 8 | Añadir el **CVI** como 2ª dimensión del IOC (`H41`) | **Javo** — *transversal, es d01* | libre |

> **Se puede avanzar YA con 4, 5, 6 y 8.** Solo 2 y 3 dependen de un dato que hoy no existe en
> ningún documento disponible.

**Nada de esto recalcula el motor.** El ICPI (`H12!B33`) permanece intacto: son inputs, señales
nuevas y exposición de contrato.

---
*Especificación · Dylus Lab © 2026 · deriva de OBS-015 · OBS-016 · OBS-017 · OBS-020.*
*El Excel es el motor: QUIRA especifica, Javo sella.*
