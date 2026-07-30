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

## ✅ v5.6_TGI PROMOVIDO · 2026-07-29

**El canónico activo es ahora `SIAP-ICPI_GOLD_MASTER_v5.6_TGI.xlsx`.** Javo lo promovió, lo abrió
en Excel (recalculó) y **retiró IGP_3 él mismo**. El conector lo tomó **automáticamente**, sin
tocar código — la corrección del resolver funcionó en producción.

| | v5.5 | **v5.6** |
|---|---:|---:|
| `H20b!B8` IGP_3 (MFN · d09) | 0,91 | **retirado** |
| `H20b!B9` **IGP_Global** | 0,4833 | **0,27** |
| `H73` IGP_2026_ACTUAL | 0,4833 | **0,27** |
| `H12!B33` ICPI | 0,27458226534062735 | **idéntico** ✅ |

> **La baja de 48,33% → 27% es corrección metodológica, no deterioro de gestión.** El IGP ya no
> mezcla d09. Debe citarse siempre con esa nota o la serie histórica se vuelve ilegible.

## ★ CANDIDATO v5.7 · `_CANDIDATO_v5.7_IGP3-SATIX-CVI.xlsx`

Lo que falta, sobre copia de v5.6:

| Cambio | Detalle |
|---|---|
| **Limpieza IGP** | `B9`/`B10` aún referencian `B8`; pasan a `AVERAGE(B6:B7)` · etiqueta `IGP_3_RETIRADO` + nota metodológica |
| **`SAT-IX`** | Brecha de Atención Ciudadana · **D4** · COOTAD 238 · umbral **0,50** · peso **0,05** |
| **Panel CVI** | `H41!A19:C23` — `CVI_POA = 0,989` · `IOC_COMPUESTO = AVERAGE(ICEP, CVI)` **como propuesta**, no reemplaza `IOC_Global` |

### Por qué esos números

**`SAT-IX` umbral 0,50** — se mide sobre demandas **vinculantes** (COOTAD 238, incorporación
exigible), no sobre todas: **84,8% (162 de 191)** sin correlato verificable. El umbral en 0,50
dice: *si más de la mitad de lo legalmente exigible no puede verificarse, el mecanismo no cumple
su función*. Peso 0,05, el mismo de `SAT-VI` por ser de la misma dimensión D4.

**`IOC_COMPUESTO` no se aplica, se propone.** Cambiar `IOC_Global` afecta lo que ya lo consume;
el panel deja el dato calculado y visible para que Javo decida si lo promueve.

## Procedimiento de promoción *(el mismo que funcionó)*

1. Abrir el candidato en Excel y **guardar** — openpyxl no deja valores cacheados.
2. Verificar `H12!B33` = **0,27458226534062735**.
3. Renombrar a **`SIAP-ICPI_GOLD_MASTER_v5.7_TGI.xlsx`** *(sufijo `_TGI` obligatorio)*.
4. El conector lo toma solo.

> ⚠️ **Nunca** renombrar un `_FREEZE` a `_TGI`: son respaldos, no motores.

---

## ESTIMACIÓN Haiku · monitoreo d07 LOTAIP

> ⚠️ **Es una ESTIMACIÓN basada en hipótesis de volumen, no un presupuesto** (asesoría). Hasta procesar un mes real no se conoce el tamaño medio de los PDF y Excel, los tokens efectivos ni el porcentaje de caché. Sirve para decidir cuánto comprar, no para facturar.

Precios Haiku 4.5: **$1/MTok** entrada · **$5/MTok** salida.

| Escenario | 6 meses (solo 2026) | **18 meses (2025+2026)** |
|---|---:|---:|
| Conservador (55 docs/mes · 6k tok) | $7,42 | **$22,27** |
| Pesado (80 docs/mes · 10k tok) | $16,80 | **$50,40** |

*(cifras con factor ×2,5 por reprocesos y desarrollo)*

> **Recomendación: comprar $60 y hacer los 18 meses completos.** No hay razón para recortar a
> 2026: la serie de 2025 es lo que da **longitudinalidad** —el activo que un competidor no puede
> comprar (Constitución Art. 19)— y el costo diferencial son ~$30.
>
> Con *prompt caching* (los prompts de sistema se repiten en cada documento) la entrada baja
> 40-50%, así que el escenario real estará más cerca de $25 que de $50.

**Antes de gastar:** procesar **1 mes real** de LOTAIP mide tokens efectivos y convierte esta
estimación en cifra exacta. Requiere construir primero el extractor de d07, que hoy no existe.

---

## ★ CANDIDATO ANTERIOR (v5.6) · histórico

**Archivo:** `ProyecT/_CANDIDATO_d08_REVISAR_NO_ES_CANONICO.xlsx` — copia de v5.5 con 5 celdas
cambiadas. **NO es el canónico** y el conector lo ignora por el prefijo `_`.

| Celda | Antes | Ahora |
|---|---|---|
| `H24c!B7` | `0` literal | `=SUM(H10b_S8b_PARTICIPATIVO!D13:D17)` |
| `H24c!C7` | *"FALLA 17: IFERROR(H10b!B9,0)"* | advertencia de **no** usar `B9` (Ingresos_Base) |
| `H24c!C8` | *"sin datos PP"* | *"ausencia MEDIDA, no pendiente"* (OBS-021) |
| `H36!A9` | `H05_S3_COMPETENCIAS_COOTAD` | `H05_S3_OPERATIVO_POA` |
| `H36!A14` | `H13_S6_VERIFICACIÓN` | `H13_VARIABLES_Vi` |

**Verificado:** diff completo = **5 celdas** · 123 hojas en ambos · `H12!B31/B32/B33` **idénticas**
· 3 fórmulas matriciales preservadas (texto y `ref` iguales).

### Cómo se promueve a canónico *(decisión de Javo)*

1. Abrir el candidato en Excel y **guardar** — openpyxl no deja valores cacheados; Excel recalcula.
2. Verificar que `H12!B33` siga dando **0,27458226534062735**.
3. Renombrar a **`SIAP-ICPI_GOLD_MASTER_v5.6_TGI.xlsx`** *(el sufijo `_TGI` es obligatorio:
   es lo que el conector reconoce como slot vivo)*.
4. El conector lo toma **automáticamente** — ya no hay que tocar código.

> ⚠️ **Nunca** renombrar un `_FREEZE` a `_TGI`: son respaldos pre-cirugía, no motores.

---

## Matriz de trazabilidad *(qué cambio nace de qué evidencia)*

| Cambio | Evidencia origen | Dónde se decide | Estado |
|---|---|---|---|
| Conector no leía el IGP | lectura directa del GM · 2026-07-29 | Python (conector) | ✅ **hecho** |
| Composición del IGP mezcla d09 | **OBS-015** | Excel · **Javo** | ⏳ |
| `IGP_2 = 0` — el GAD no desagrega montos PP | lectura `H10b!D13:E17` | **R-F**: no se pide | ✅ **medido** (es el hallazgo) |
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
| **IGP_2** · Presupuesto Participativo | **0,00** | d08 ✅ | **sellar como medido** — §2 |
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

## 2 · Limitación Estructural del Instrumento de Participación Presupuestaria

> **Denominación canónica del hallazgo** *(asesoría · 2026-07-29).* `IGP_2 = 0` **no se registra
> como "dato faltante"**. Se registra con su nombre: **limitación estructural del instrumento**.
> El PP prioriza proyectos por puntuación, pero **no incorpora la dimensión financiera en su
> origen**. No es error del Excel, ni del algoritmo, ni del conector: es una **característica del
> instrumento administrativo**. Ese lenguaje es el defendible académicamente.
>
> **Afirmable porque el PP está en UDC** (Protocolo R-F.1): se conoce su universo documental.

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

> **Naturaleza de la limitación (precisión de la asesoría):** no es una limitación **del GAD**
> —no se le imputa conducta— ni una limitación **de QUIRA**. Es una limitación **del instrumento
> administrativo**. Fijar eso por escrito evita interpretaciones políticas posteriores.
>
> **HECHO VERIFICADO, no inferencia (Javo · 15 años en gestión GAD):** los documentos de
> Presupuesto Participativo de Montecristi **puntúan la PRIORIDAD de cada obra o servicio
> solicitado, pero no establecen su COSTO económico**. No es que el dato esté mal publicado ni
> que falte una fuente: **el instrumento no lo produce**. Se conoce el universo documental
> completo de este GAD, así que la ausencia está **determinada**, no supuesta.
>
> **Por eso no se solicita (R-F · caso 2).** Pedirlo haría que el GAD lo construya recién, y ese
> documento nacería después de nuestra pregunta: sería evidencia de reacción, no de gestión.
> *(En un GAD cuyo universo NO conocemos, el régimen sería el caso 3 y sí se solicitaría, vía
> Observatorio QUIRA — pero R-E mantiene a los otros 221 fuera de alcance por ahora.)*
>
> **Por tanto `IGP_2 = 0` NO está bloqueado: está MEDIDO.** El cero es el resultado, y es
> definitivo mientras el GAD no publique el desglose por iniciativa propia. Registrarlo como
> "pendiente de dato" sería tratar un hallazgo como un hueco.
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

### ★ PRECEDENTE H24c · Integridad Semántica de Fórmulas

Se registra como caso canónico de la Carta, a pedido de la asesoría. Reconstrucción:

| Paso | Qué pasó |
|---|---|
| 1 | Se detecta `H24c!B7 = 0` **sin fórmula**, con un comentario que indica cuál debería ser |
| 2 | **Intuición inicial:** restaurar `IFERROR(H10b!B9,0)`. Parece corrección obvia de una línea |
| 3 | **Verificación:** `H10b!B9` = `Ingresos_Base_2026` = **20.982.884** — los ingresos del GAD |
| 4 | El PP es una **fracción de la inversión**, no el ingreso total → la fórmula era **conceptualmente errónea** |
| 5 | Restaurarla habría puesto cifra falsa en `B7` → `Hay_Datos_PP` a **"SÍ"** por fórmula → **`SAT-VI` disparada sobre un dato inventado** |

> ### Enunciado canónico del **Precedente H24c**
>
> **La validez sintáctica de una fórmula no garantiza su validez semántica.** Restaurar un
> operando cuyo significado corresponde a **otra entidad** —`Ingresos_Base` en lugar de
> `Monto_PP`— degrada la integridad del motor aunque la fórmula sea correcta.
>
> **Una fórmula correcta puede producir un dato falso si el operando representa otra realidad.**
>
> **Regla derivada:** toda restauración o reconexión de fórmula exige verificar la **semántica del
> operando**, no solo su existencia. Lo que impidió el error no fue desconfiar del Excel: fue
> **leer qué significaba la celda de origen antes de conectarla**.

**La fórmula correcta es** `=SUM(H10b!D13:D17)` — suma de montos aprobados por proyecto. Da **0**,
y ese 0 es correcto: el GAD no los desagrega (§2 · R-F).

**Acción:** aplicarla con su resultado 0, y corregir el comentario de `C7` para que nadie vuelva
a intentar la restauración equivocada. `SAT-VI` queda **sin señal por ausencia declarada** — que
no es lo mismo que *sin datos*: es una **ausencia medida**.

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
| 1 | ~~Solicitar montos del PP al GAD~~ | — | ⛔ **PROHIBIDO por R-F** — induciría su creación |
| 2 | `IGP_2 = 0` se sella como **medido**, no como pendiente | **Javo** (Excel) | libre |
| 3 | `H24c!B7 = SUM(H10b!D13:D17)` (=0) — **jamás** `H10b!B9` · `SAT-VI` queda **sin señal por ausencia declarada** | **Javo** (Excel) | libre |
| 4 | Decidir destino de IGP_3 (retirar / migrar / sustituir) | **Javo** | libre — §1 |
| 5 | Sellar métricas observables de §4 (223 · 191 · 103 · 28/28) | **Javo** (Excel) | libre |
| 6 | Crear `SAT-IX` Brecha de Atención (umbral y peso) | **Javo** (Excel) | tras 5 |
| 7 | Exponer claves nuevas de d08 en `H73` + añadirlas al conector | Javo → dirección técnica | tras 5-6 |
| 8 | Añadir el **CVI** como 2ª dimensión del IOC (`H41`) | **Javo** — *transversal, es d01* | libre |

> **Se puede avanzar con TODO.** Ya no hay pasos bloqueados: R-F convierte la ausencia de montos
> de *dato pendiente* en *hallazgo cerrado*. El universo documental de Montecristi está cerrado
> (R-E + R-F): **lo que hay es lo que hay, y eso es exactamente lo que se mide.**

**Nada de esto recalcula el motor.** El ICPI (`H12!B33`) permanece intacto: son inputs, señales
nuevas y exposición de contrato.

---
*Especificación · Dylus Lab © 2026 · deriva de OBS-015 · OBS-016 · OBS-017 · OBS-020.*
*El Excel es el motor: QUIRA especifica, Javo sella.*
