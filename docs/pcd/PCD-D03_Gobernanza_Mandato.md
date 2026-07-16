# PCD-D03 · Gobernanza del Mandato (QINV-003)

**Estado:** CERRADO · 2026-07-16 · Javo + director técnico · revisión del colega
**Dominio:** la palabra empeñada — qué ocurrió con el mandato electoral al atravesar la puerta
de entrada del sistema de planificación.
**Fuente:** Plan de Trabajo del CNE 2023 (`Plan CNE ALcalde Montecristi.docx` · SHA256
`7dcbc36a…`) + base depurada por Javo (`Base de solo las promesas del plan CNE.docx` · SHA256
`642f5b87…`) + Plan Plurianual PDOT 2023-2027 (`09a2aacc…`).
**Relacionado:** ADR-035 (BRN · la IA propone, el humano valida) · ADR-036 (universo
operacional) · OBS-010 (25 de 66 metas).

---

## Estado inicial

d03 heredaba de la construcción previa un registro de **66 promesas** y un índice de fidelidad
de **72.73%**. Todo parecía sano: el índice tenía serie histórica (72.83% en 2025), su
clasificación, y un centinela vigilándolo.

## Hallazgos (auditoría del canon)

| # | Hallazgo | Origen |
|---|---|---|
| 1 | **46 de las 66 promesas no salieron del Plan CNE.** Nadie las ingestó: aparecieron. Tres mencionaban **otros cantones** (Sucre, Jaramijó, Crucita) | **Javo** — las detectó antes que ningún análisis |
| 2 | **El "48" no era un conteo de promesas**: era la *suma de scores* (48.75) con el rótulo `Promesas_Con_Meta_PDOT`. Quien leyera la hoja en dos años entendería mal | director |
| 3 | **`Clasificación_IFE` era texto estampado**, no fórmula → podía contradecir a H16 (y lo hizo) | director |
| 4 | **El estado de verificación no existía como dato**: el enricher lo *inferría* del prefijo del ID (`PR-` = pendiente) → violaba la Regla 9 | director |
| 5 | **El PDOT real tiene 66 metas; el canon opera con 25.** El caso que lo destapó: *Infocentro* tenía meta real (*puntos digitales 19.265→23.265*, `3.SOC`) ausente del canon | **Javo** — pidió un "último filtro" y aportó el Plan Plurianual |
| 6 | **d03 publicaba las 46 falsas** en la web (quedó entrable antes de conocerse la contaminación) | director |

## Cambios en el canon (ninguna fórmula del motor tocada)

| Celda | Antes | Después |
|---|---|---|
| `H03!A8` | `Promesas_Con_Meta_PDOT` | **`Suma_Score_Vinculación`** (dice lo que es) |
| `H03!B8` | 48 | **60.25** (suma real de las 76) |
| `H03!A12/B12` | *(no existía)* | **`Promesas_Con_Meta_PDOT` = 75** (el conteo, en su propia celda) |
| `H03!B10` | texto estampado | **fórmula** — ya no puede desincronizarse |
| `H03!G` | *(no existía)* | **`Estado_Verificación`** — el estado nace como dato (Regla 9) |
| `H03!17:93` | 66 promesas (46 falsas) | **76 promesas reales**, 5 ejes, cero contaminación |
| `H01!B17` | 66 | **76** |
| `H85!D21` | centinela en 0.7273 | **0.7928** (recalibrado) |
| **`H12!B33`** | `0.27458226534062735` | **INTACTO** — la fórmula canónica jamás se tocó |

**Método:** todo sobre **copia de trabajo**, con dumps ANTES/DESPUÉS (`data/dumps/`), y **Javo
ejecutando las escrituras en Excel**. Se descubrió *por qué* la metodología prohíbe openpyxl:
**vacía el caché de valores de las 123 hojas** — las fórmulas sobreviven, pero QUIRA (que lee
`data_only=True`) leería `None` en todo hasta que Excel reabra. La copia atrapó además que las
promesas nuevas **aplastaban las filas `TOTALES` e `IFE_Global`**.

## Validación

- **Vinculación:** propuesta por el director (razonamiento semántico promesa↔meta; se descartó
  la similitud textual: emparejaba *"destino turístico"* con *"Concejo de Salud"*), **validada
  por Javo** y **corroborada** contra las 25 metas: metas existentes ✔ · scores coherentes con
  su tipo ✔ · coherencia eje↔sistema ✔ · 24 de 25 metas con promesa.
- **Correcciones de Javo:** `AM-008` eliminada (derogar un decreto nacional no es competencia
  municipal → no vinculable; excluirla evita penalizar al GAD en el denominador) · `IN-007` y
  `SC-009` Parcial · `SC-017` Directa.
- **Error propio detectado por la corroboración:** `AM-005` (*ampliación del basurero*) estaba
  en gestión integral; el basurero **es disposición final** → `FA-DIS-01`. Lo delató que esa
  meta quedara huérfana.
- **Canon coherente = True:** el conteo declarado (75) coincide con el real, y el índice del
  motor coincide con el recálculo del registro. **Centinela: ✅ CORRECTO.**

## Doctrina fijada (lo que este dominio enseñó)

1. **El IFE es UNIDIRECCIONAL** (corrección de Javo): d03 mide *promesa → ¿llegó al plan?*, no
   *meta → ¿venía de una promesa?*. Una meta sin promesa electoral es **normal y legítima**: el
   PDOT nace del **diagnóstico técnico**, y estando en el PDOT ya cumple el **Art. 264 núm. 1**
   de la Constitución. Tratarlo como hallazgo insinuaría que el GAD solo debe planificar lo
   prometido — falso, y lenguaje acusatorio disfrazado de dato.
2. **La cocina no va al producto** (corrección de Javo · Regla 2): las fallas, contradicciones
   y errores de las etapas de **construcción** son internos. Viven en el PCD, los ADR y las OBS
   — **nunca en el DOM**, que publica el **resultado curado**. Contarlos allí solo sembraría
   dudas sobre QUIRA sin aportar nada sobre el GAD.
3. **El alcance sí se declara** (ADR-036): el dominio mide contra el **universo estratégico**,
   no contra el plan completo. Una promesa cuya meta exista fuera de ese subconjunto se declara
   **fuera de alcance**, no como incumplimiento (caso `SC-017`).
4. **El DOM cura el canon** (Regla 8): el Gold Master entró con un rótulo que mentía, una
   clasificación que podía contradecirse, 46 promesas falsas y un universo tácito. **Salió
   autoexplicativo, coherente y con su alcance escrito.** La curación del canon es un
   **entregable** del dominio, no un efecto secundario.

## Estado final

**Fidelidad del mandato: 79.28%** (*Media*) · **76 promesas reales** · 75 con correspondencia
documental · 1 fuera del universo operacional · **canon coherente** · **centinela ✅** ·
**ICPI intacto**.

> El valor **no es comparable** con el 72.73% previo: aquel se calculaba sobre un universo
> distinto. La serie de v1 se reinicia con este registro. *(Nota interna — no se publica en el
> DOM: es historia de construcción.)*

**Abierto:** las autoridades electas siguen con **7 de 8 sin verificar** (ausencia declarada,
no defecto) · la ampliación del universo **25 → 66** espera decisión de arquitectura (ADR-036
§4 · sería v2, al escalar a los 221 GAD — no una corrección).

---
*PCD-D03 · Dylus Lab © 2026 · "El dominio que mide la palabra empeñada no podía permitirse una palabra sin respaldo. Encontró 46 promesas que nadie prometió, un rótulo que mentía y un universo que nunca se declaró — y salió con las 76 reales, el canon coherente y su alcance por escrito."*
