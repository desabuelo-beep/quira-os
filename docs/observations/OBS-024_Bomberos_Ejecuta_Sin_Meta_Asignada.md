---
id: OBS-024
authority:
  parent: ADR-047
  constitution_articles: [1, 3]
  type: OBSERVACION
fecha: 2026-08-11
dominio: d06 · d01 · d05
estado: VERIFICADA
---

# OBS-024 · El Cuerpo de Bomberos ejecuta el PDOT sin tener metas asignadas en él

> **Origen.** Javo, corrigiendo una extracción del director (2026-08-11): *«no estás considerando
> a la Empresa de Aseo EP y Cuerpo de Bomberos, tu análisis es corto, hay metas para estas
> también»*. La revisión confirma la corrección y encuentra algo distinto de lo esperado.

## Qué se buscaba

Clasificar quién ejecuta cada meta del PDOT, para determinar el factor `Ei` (autonomía orgánica)
sin penalizar la ejecución por entidad propia del GAD.

## Qué se encontró

**El Cuerpo de Bomberos no aparece como Unidad Responsable de ninguna meta**, ni en el Excel de
contraste ni en la matriz plurianual del PDOT oficial (tablas #341-352 del documento).

Aparece en otro sitio: las **tablas #353 y #355**, de *identificación de estrategias de
articulación*, donde figura un proyecto —«Construcción de la Estación Bomberil»— con estado
**«Sin postulación»**.

**Pero ejecuta.** Su POA 2026 declara **$1.752.000** y se alinea explícitamente al plan:

> «NO. DE PTDOT PLAN BICENTENARIO **20** · SISTEMA **Asentamientos Humanos** · OBJETIVO DE
> DESARROLLO *Montecristi Hábitat digno y sostenible* · EJE DE RESPUESTA A EMERGENCIAS»

Y tiene serie completa en el corpus: **POA 2024-2026 · PAC 2023-2026 · rendición de cuentas
2023-2024**.

## El hallazgo

> **Una entidad del holding municipal ejecuta presupuesto propio declarando alineación al PDOT,
> y el PDOT no le asigna ninguna meta.**

La cadena se rompe en un punto que ninguna de las dos partes muestra por sí sola: el PDOT dice
qué hay que lograr y a quién le toca; el POA de Bomberos dice qué hace y cuánto gasta. **Cruzados,
falta el eslabón que los une.**

No es un error de captura ni de lectura: es una **brecha real de trazabilidad**, del tipo exacto
que el sistema existe para encontrar. Y es invisible mientras se mire una sola fuente.

## Lo que la matriz sí asigna, y a quién

| Ejecutor | Metas | Naturaleza |
|---|---|---|
| Unidades del GAD | 54 | directo |
| Empresa de Aseo · Empresa de Vivienda | 6 | empresa pública propia |
| Patronato de Amparo Social | 6 | entidad adscrita propia |
| **Cuerpo de Bomberos** | **0** | **adscrita propia — ejecuta sin meta asignada** |

La gestión de riesgo, que es su competencia, aparece asignada a **«Planificación / Unidad de
gestión de riesgos»** — una unidad del GAD, no la entidad que la ejecuta con presupuesto propio.

## Por qué importa para el motor

1. **Para `Ei`:** no se puede corregir la autonomía de una meta de Bomberos porque **no hay meta
   de Bomberos que corregir**. El problema es anterior al factor.
2. **Para la cobertura:** si el ICPI mide cumplimiento de metas del PDOT, la ejecución de Bomberos
   **no entra en el índice por ninguna vía** — ni bien ni mal. Queda fuera del alcance.
3. **Para el holding (d05):** `H12d_ICPI_POR_ENTIDAD` calcula por entidad. Una entidad sin metas
   asignadas no puede tener cumplimiento medible de plan.

## Lo que NO se concluye

- **No se afirma incumplimiento de nadie.** Que el PDOT no asigne metas a Bomberos puede
  responder a una decisión de técnica de planificación, no a una omisión.
- **No se corrige el PDOT.** Es un instrumento aprobado; QUIRA lo observa, no lo edita.
- **No se inventa la meta faltante.** Si el vínculo no está declarado, no se supone.

Lo que corresponde es **declarar la brecha y medirla**: cuánto presupuesto se ejecuta bajo
alineación declarada al PDOT sin correspondencia con una meta del propio PDOT.

## Trazabilidad

| Fuente | Carácter |
|---|---|
| PDOT Montecristi 2023-2027 Bicentenario `.docx`, tablas #341-352 y #353-355 | oficial |
| Plan Plurianual PDOT 2023-2027 `.xlsx` · `sha256 09a2aacc…` | **no oficial** — contraste |
| `POA-BOMBEROS-2026` · corpus, 21 fragmentos | institucional |
| `PAC-BOMBEROS-2023..2026` · `RC-BOMBEROS-2023..2024` | institucional |

---
*OBS-024 · Dylus Lab © 2026 · hallazgo de cruce: ninguna fuente lo muestra sola.*
