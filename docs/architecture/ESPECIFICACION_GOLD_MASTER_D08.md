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

## 0 · El diagnóstico que motiva esto

**d08 está fuera del contrato del motor.** `H73_OUTPUT_API` —la única hoja que QUIRA lee
(`app/connectors/gold_master.py`)— expone 24 claves y **ninguna es de participación**:

```
ICPI_* · ISP_* · PSG_* · IFE_* · PAC_* · RDC_* · SAT_RIESGO_* · TGI_D1..D5
```

`TGI_D4` existe —es la dimensión donde vive participación— pero **el IGP no se expone**. El
indicador madre de d08 se calcula en `H20b_IGP_GOBERNANZA_PARTICIPATIVA` y **no sale al
contrato**. Los dominios d01·d02·d03·d09 sí están; d08 no.

**Consecuencia:** la UI de participación no puede leer su propio indicador del motor. Cualquier
número que muestre hoy vendría de fuera del Gold Master — exactamente lo que las Reglas 1 y 4
prohíben.

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

## 2 · Alimentar IGP_2 — PP en 0 con evidencia de tres años *(OBS-015 · Hallazgo 2)*

`IGP_2 = 0,00` pese a existir actas de Presupuesto Participativo de **2023, 2024 y 2025**
(`…/Participación Ciudadana`, ya procesadas por `scripts/d08/extraer_demandas.py`).

El flag interno `Hay_Datos_PP = NO` es lo que mantiene el cero, y **ya no es cierto**.

| Insumo disponible hoy | Origen |
|---|---|
| 223 demandas ciudadanas extraídas, con documento y año | `data/d08/demandas_ciudadanas.json` |
| 191 de naturaleza **vinculante** (COOTAD 238) | idem |
| Actas de PP de 3 ejercicios | fuente documental oficial |

**Acción:** `Hay_Datos_PP = SÍ` + cargar los insumos de PP. La **fórmula de IGP_2 no se toca**:
se alimentan sus inputs (Regla 1 — corrección sobre inputs, nunca sobre la fórmula canónica).

## 3 · Activar SAT-VI — la única SAT de participación *(OBS-016)*

`H24c_SAT-VI_DESVÍO_PP` · dimensión **D4** · consumida por `RO-VIII-003`.
Estado actual: **"sin datos (Hay_Datos_PP = NO)"** — se destraba con §2.

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

| # | Acción | Quién | Bloquea a |
|---|---|---|---|
| 1 | `Hay_Datos_PP = SÍ` + cargar insumos de PP | **Javo** (Excel) | 2, 3 |
| 2 | Decidir destino de IGP_3 (retirar / migrar / sustituir) | **Javo** | 4 |
| 3 | Activar `SAT-VI` con datos reales | **Javo** (Excel) | 5 |
| 4 | Sellar métricas observables de §4 | **Javo** (Excel) | 5 |
| 5 | Crear `SAT-IX` Brecha de Atención (umbral y peso) | **Javo** (Excel) | 6 |
| 6 | Exponer claves d08 en `H73_OUTPUT_API` | **Javo** (Excel) | 7 |
| 7 | Añadir claves a `_KEYS_OF_INTEREST` + leerlas en la UI | dirección técnica | — |
| 8 | Añadir el **CVI** como 2ª dimensión del IOC (`H41`) | **Javo** — *transversal, no d08* | — |

**Nada de esto recalcula el motor.** El ICPI (`H12!B33`) permanece intacto: son inputs, señales
nuevas y exposición de contrato.

---
*Especificación · Dylus Lab © 2026 · deriva de OBS-015 · OBS-016 · OBS-017 · OBS-020.*
*El Excel es el motor: QUIRA especifica, Javo sella.*
