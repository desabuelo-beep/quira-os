# ADR-035 · Biblioteca de Reglas Normativas (BRN) — la ley como fuente autorizada de lógica de cumplimiento

**Estado:** RATIFICADO · 2026-07-15 (Javo + director técnico · refinado por el colega)
**Contexto de origen:** inquietud que Javo carga **desde la construcción del Gold Master** (ancló cada SAT a su
base legal en `SAT_Catalogo`, pero de forma manual e implícita; no tenía entonces cómo formalizarlo). El colega
lo propone como *Motor de Cumplimiento Normativo (MCN)*. **Dos correcciones cierran el diseño:**
- **Javo:** el **DOM de Alertas Institucionales NO se elimina — TRANSMUTA en la BRN.**
- **Colega:** **no es un "motor"** (motor implica ejecutar → chocaría con el Gold Master). Es una **BIBLIOTECA**.
**Relacionado:** ADR-023 (Regla 1/4 · no recalcular el motor) · ADR-031 (5 motores tipados · cable Normativo del
MCD) · ADR-033 (dos verdades · Principio Rector) · ADR-034 (el Orquestador corre los ciclos) · Regla 3 (sin norma
verificada, no hay dato) · Regla 7 (anti-inflación) · Regla 9 (nace en el canon).

---

## Contexto

QUIRA ya vincula norma y control, pero **sin sistematizar**: el `SAT_Catalogo` lista cada SAT con su artículo
(SAT-IV → COOTAD Art. 192; SAT-III → COPFP Art. 113) y el corpus normativo (Supabase · SHA256) guarda el texto
verificado. Falta el **puente ejecutable y trazable** entre ambos. La tentación era crear un "motor" que generara
verificaciones; eso habría producido **dos motores** — el pecado capital del proyecto.

## Decisión

### 1. La cadena canónica: LEY → ARTÍCULO → REGLA → TIPO → CONDICIÓN → INDICADOR → SAT → SEÑAL
El SAT **no nace del artículo**; nace de la **regla operacional** que el artículo contiene. Un mismo artículo
puede engendrar **varias** reglas, indicadores y SAT. La **regla** es la unidad atómica del cumplimiento.
```
Ley (COOTAD · COPFP · LOTAIP · LOSNCP · Constitución)
   → Artículo (texto verificado · SHA256)
   → Regla normativa  ·  IDENTIFICADOR PROPIO: COOTAD-192-R01
   → Tipo de regla (obligación · prohibición · límite · plazo…)
   → Condición operacional (IF … THEN)
   → Indicador verificable
   → SAT (lo CALCULA el Gold Master)
   → Señal (se muestra en su dominio)
```

### 2. SEPARACIÓN DE PODERES — nunca dos motores (Regla 1 + Regla 4)
```
Ley  →  BRN  →  Gold Master  →  SAT  →  QUIRA
```
| Pieza | Rol | Qué NO hace |
|---|---|---|
| **La ley** | fuente de **verdad jurídica** (inmutable) | no se contamina con implementación |
| **La BRN** | **única fuente autorizada de lógica normativa** — organiza, clasifica y **versiona** las reglas | **NO ejecuta. NO calcula.** |
| **El Gold Master** | **único motor**: calcula los SAT | no interpreta derecho |
| **QUIRA** | explica, traza y presenta | no recalcula |

*La ley es la **especificación funcional** del Estado (matiz del colega, adoptado — más preciso que "la ley es el
código fuente"). La BRN la organiza; el Gold Master la ejecuta; QUIRA la explica.*

### 3. El DOM de Alertas Institucionales TRANSMUTA en la BRN (decisión de Javo · 2026-07-15)
**No se elimina** (queda sin efecto la decisión previa de suprimirlo). **Cambia de naturaleza:** deja de ser un
*tablero de alertas sueltas* y pasa a ser la **biblioteca-fuente de la lógica normativa** del ecosistema.
- Las **señales se muestran en su dominio** (d02 muestra las presupuestarias) — eso se mantiene.
- La **BRN es transversal**: no observa una capacidad del Estado; **alimenta** a los dominios que sí lo hacen.
- Ajuste de conteo de dominios → se refleja en la **Constitución Ontológica** (nota de seguimiento).

### 4. Clasificación por TIPO de regla (disciplina anti-alucinación · Regla 3)
**No todo artículo produce control. No se SATiza lo declarativo** — eso evita convertir el ordenamiento jurídico
en miles de alertas absurdas.

| Tipo | ¿Produce SAT? | Tipo | ¿Produce SAT? |
|---|:--:|---|:--:|
| Obligación ("deberá publicar") | ✅ | Competencia | ⚠️ indirecto |
| Prohibición | ✅ | Principio ("promoverá…") | ❌ |
| Límite (65% inversión) | ✅ | Definición | ❌ |
| Plazo (fecha de liquidación) | ✅ | Objetivo político | ❌ |

### 5. REGLA CONSTITUCIONAL — la IA jamás deriva reglas por su cuenta (aporte del colega)
```
Ley → Extracción → PROPUESTA de regla → VALIDACIÓN HUMANA → BRN → Gold Master → SAT
```
**JAMÁS:** `Ley → IA → SAT`. La IA **propone**; el humano **valida**. Sin validación humana **no entra a la BRN**.
Una regla no validada es una **interpretación jurídica no controlada** — inaceptable en un observatorio cuya
autoridad depende de su rigor. Coherente con el Principio Rector (ADR-033): QUIRA no juzga; verifica.

### 6. Anti-inflación (Regla 7) — por qué la BRN sí entra
No entra por "renombrar": entra por **tres capacidades reales** que hoy no existen:
**(a)** clasificación de artículos por tipo (§4) · **(b)** reglas con **ID propio** y versionables
(COOTAD-192-R01/R02…), reutilizables entre dominios y GAD · **(c)** trazabilidad **bidireccional** norma ↔ señal.
Además: **no duplica el corpus** (referencia el texto SHA256 existente) y **no posee los SAT** (los explica).

## Consecuencia práctica

**d02 ya muestra el germen**: cada señal expone su cadena *Norma → Regla → Indicador → Señal* (la ley
materializada, visible). La BRN generaliza el patrón: **ninguna señal aparece sin su norma de origen, en ningún
dominio**. Orden de construcción: **catalogar la BRN** (extraer → clasificar → ID → **validar humanamente**) →
**el Gold Master ejecuta** → **cada dominio muestra sus señales** → **el Orquestador** (ADR-034) lo corre mensual,
por GAD. Así los SAT dejan de programarse a mano: **nacen de la legislación vigente** — más mantenibles y más
defendibles ante una contraloría, un GAD o un banco de desarrollo. Una ley nueva ya no exige rediseñar el sistema
de alertas: se cataloga su artículo, se valida su regla, y el SAT aparece.

---
*ADR-035 · Biblioteca de Reglas Normativas · Dylus Lab © 2026 · "No inventamos las alertas: las deriva la ley. La ley manda, la BRN organiza, el Gold Master calcula, QUIRA explica. Un solo motor, una sola fuente de lógica, y siempre un humano validando la interpretación del derecho."*
