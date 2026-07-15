# ADR-035 · Motor de Cumplimiento Normativo (MCN) — la ley como especificación ejecutable

**Estado:** PROPUESTO · 2026-07-15 (director técnico · a partir de una inquietud de Javo desde la construcción del
Gold Master + una propuesta del colega) · **pendiente de ratificación de Javo**
**Contexto de origen:** Javo, al construir el Gold Master, ancló cada SAT a su base legal (`SAT_Catalogo` ·
columna *"BASE LEGAL (Artículo)"*), pero de forma **manual e implícita**. No tenía entonces cómo formalizarlo.
El colega lo propone como sistema: la ley → regla → indicador → SAT. Se adopta la **intuición** (correcta y de
alto potencial) con **tres líneas rojas de disciplina**.
**Relacionado:** ADR-023 (Regla 1/4 · no recalcular el motor) · ADR-031 (5 motores tipados · el MCD, cable
Normativo) · ADR-033 (dos verdades · proveniencia 🟢🔵🟣) · ADR-034 (el Orquestador corre los ciclos) ·
Regla 3 (sin norma verificada, no hay dato) · Regla 7 (anti-inflación) · Regla 9 (nace en el canon).

---

## Contexto

QUIRA ya vincula norma y control, pero **sin sistematizar**: el `SAT_Catalogo` del Gold Master lista cada SAT
con su artículo (SAT-IV → COOTAD Art. 192; SAT-III → COPFP Art. 113), y el corpus normativo (Supabase, con
SHA256) guarda el texto verificado. Lo que falta es el **puente ejecutable** entre ambos: convertir el derecho
administrativo en reglas de verificación de forma **trazable y mantenible**, no artesanal.

El colega lo nombra *Motor de Cumplimiento Normativo (MCN)* / *Biblioteca de Reglas Normativas (BRN)*. La idea
es sólida y pertenece al **núcleo** de QUIRA (Nivel 2 SO: trazabilidad + evidencia sobre norma verificada). No
es una capa ajena: es la **explicitación de algo latente** que Javo ya intuyó al construir el motor.

## Decisión

### 1. El modelo canónico: NORMA → REGLA → CONDICIÓN → INDICADOR → SEÑAL
El SAT **no nace del artículo**; nace de la **regla operacional** que el artículo contiene. Un artículo puede
engendrar varias reglas; la **regla** es la unidad atómica del cumplimiento.
```
Constitución / Ley (COOTAD · COPFP · LOTAIP · LOSNCP)
   → Artículo (verificado · SHA256)
   → Regla normativa (obligación/límite/plazo)
   → Condición lógica (IF … THEN señal)
   → Indicador verificable (medido por el Gold Master)
   → SAT / señal preventiva (en su dominio)
```

### 2. LÍMITE DURO (Regla 1 + Regla 4 + Prohibición): el MCN **TRAZA, no calcula**
El **Gold Master calcula** los SAT (H21–H24 · H75_SAT_ENGINE) sobre los indicadores del modelo. El MCN **mapea**
cada SAT a su regla y a su norma, **clasifica** el artículo y **explica** el porqué — jamás produce el valor. Un
MCN que "recalcule cumplimiento" sería el **motor de cálculo paralelo prohibido**. *El Gold Master calcula la
señal; el MCN prueba de qué ley nació.*

### 3. La Biblioteca de Reglas Normativas (BRN) — la capacidad nueva (pasa Regla 7)
Sobre lo que ya existe (corpus normativo + `SAT_Catalogo`), la BRN **añade** —y por eso no infla el canon—:
- **(a) clasificación de artículos por tipo** (qué es SATizable y qué no · §4);
- **(b) generación sistemática** regla → condición → indicador (hoy los SAT están "programados a mano");
- **(c) trazabilidad bidireccional** norma ↔ señal (de la ley a la alerta y de vuelta).
Sin estos tres aportes, la BRN solo renombraría el catálogo → **no entraría** (Regla 7).

### 4. Clasificación de artículos (disciplina anti-alucinación · Regla 3)
No todo artículo genera control. **No se SATiza lo declarativo.**

| Tipo de norma | ¿Produce SAT? | | Tipo de norma | ¿Produce SAT? |
|---|:--:|---|---|:--:|
| Obligación ("deberá publicar") | ✅ | | Competencia | ⚠️ indirecto |
| Prohibición | ✅ | | Principio ("promoverá…") | ❌ |
| Límite (65% inversión) | ✅ | | Definición | ❌ |
| Plazo (fecha de liquidación) | ✅ | | | |

### 5. "La ley es la ESPECIFICACIÓN funcional del Estado; QUIRA la implementa"
Se adopta el matiz del colega (más preciso que *"la ley es el código fuente"*). La ley define el comportamiento
esperado; QUIRA lo verifica. Coherente con el **Principio Rector** (ADR-033): QUIRA **no juzga ni legisla** —
certifica el **nivel de verificabilidad** del cumplimiento. La ausencia de evidencia es un resultado, no una
autorización para inferir incumplimiento.

### 6. Dónde vive el MCN
Es un **motor de la Capa A** (núcleo · tipado como los 5 de ADR-031), que se apoya en el **cable Normativo** del
MCD y en el corpus verificado. **NO es un producto.** Alimenta a **cada dominio** con las señales que le
corresponden (decisión Javo 2026-07-15: se elimina el DOM Alertas → cada SAT en su dominio → 12 DOM). El
**Orquestador** (ADR-034) lo corre en el **ciclo mensual**, por GAD.

### 7. Rechazo explícito (Regla 7)
- **Nomenclatura en español** (Firewall interno aparte): *Motor de Cumplimiento Normativo*, *Biblioteca de
  Reglas Normativas* — no siglas en inglés.
- **No duplicar el corpus**: la BRN **referencia** el texto normativo que ya vive en Supabase (SHA256), no lo
  recopia.
- **El SAT sigue siendo del Gold Master**: el MCN no "posee" los SAT; los **explica**.

## Consecuencia práctica

d02 ya muestra el **germen** del MCN: cada señal preventiva expone su cadena **Norma → Regla → Indicador → Señal**
(la ley materializada, visible). El MCN **formaliza** ese patrón para **todos** los dominios: ninguna señal
aparece sin su norma de origen. El trabajo de curar dominios (ADR-033) **no cambia**; se añade que cada señal
nazca **trazada** a su ley. Orden: **primero se cataloga la BRN** (clasificar artículos SATizables), **luego el
MCN traza**, **luego el Orquestador lo corre mensual**. Así los SAT dejan de programarse a mano: nacen de la
legislación vigente — **más mantenibles y más defendibles ante una contraloría, un GAD o un banco de desarrollo.**

---
*ADR-035 · Motor de Cumplimiento Normativo · Dylus Lab © 2026 · "No inventamos las alertas: las deriva la ley. El Gold Master calcula la señal; el MCN prueba de qué artículo nació. El derecho administrativo, vuelto ingeniería verificable."*
