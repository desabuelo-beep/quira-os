# BRN v2 · Matriz de Cobertura del Molde

> **Qué es.** La tabla que mide **objetivamente** cuánto está validado el molde CNO/RO — para decidir
> con evidencia, no con percepción, cuándo está listo para escalar a los 222 cantones (recomendación
> del colega · 2026-07-18). Cada dominio prueba una faceta distinta del modelo. Se actualiza al
> cerrar cada CNO.

## Los 4 invariantes que cada dominio debe cumplir
1. **El molde sirve** para ese dominio (la cadena se modela como CNO; la lógica, como RO).
2. **El compilador no cambia al incorporar el dominio** (matiz del colega · 2026-07-18: el compilador
   *sí* evolucionó durante el diseño, y era normal; el criterio de generalidad es que **agregar d05,
   d06 o d222 no toque su lógica** — `if dominio==...` = fuga).
3. **El runtime tampoco cambia** (resuelve vigencia igual para todos).
4. **Solo cambia el contenido de la RO** (la estructura del molde se mantiene).

## Matriz
| Dominio | Naturaleza de la regla | CNO | RO | Compilador | Runtime | Estado |
|---|---|---|---|---|---|---|
| **d02 · Finanzas** | umbral cuantitativo (65/70%) | ✓ vigente · 6/6 SHA | ✓ vigente | ✓ compila | ✓ | **Validado** |
| **d03 · Mandato** | congruencia programática (fidelidad ≥85%) | ✓ vigente · 9/9 SHA | ✓ vigente | ✓ compila (sin `if`) | ✓ | **Validado** |
| d01 · Planificación | — | pendiente | | | | Pendiente |
| d09 · Rendición | — | pendiente | | | | Pendiente |
| … | | | | | | |

## Lectura del examen d03 — los 4 invariantes CONFIRMADOS
d03 era la prueba dura: su regla **no** desemboca en un techo de gasto sino en un **procedimiento de
congruencia** (promesa→plan, ponderado). Resultado con ambas CNO/RO ya `vigentes` y compiladas:
1. **El molde sirve** ✅ — cadena de 9 eslabones (CE·COD·COOTAD·COPLAFIP·LOPC) con SHA verificado; la
   lógica de medición (umbral 85% + método estructurado) cabe en la RO sin forzar el molde.
2. **El compilador no cambió** ✅ — 0 ramas de dominio; el mismo `_parametros_de` (el **adaptador**,
   único punto que conoce la estructura YAML) procesó la RO del mandato y la financiera.
3. **El runtime** ✅ — el compilador emite ahora **2 RO vigentes → 3 filas** (d02 con 2 tramos, d03
   con 1); el runtime resuelve la vigencia igual para ambos.
4. **Solo cambió la RO** ✅ — molde, catálogo y compilador intactos; la suite de regresión (7/7) verde.

**Conclusión:** el molde deja de estar validado sobre **un** caso y pasa a estarlo sobre **dos
naturalezas distintas** de regla — el salto de "caso de uso validado" a "**modelo BRN** validado".

## Criterio de escalamiento a 222 cantones
El molde se considera **suficientemente validado para escalar** cuando ≥2 dominios de **naturaleza
distinta** cumplan los 4 invariantes con CNO/RO `vigentes` y compiladas. **Estado hoy: CUMPLIDO** —
d02 (umbral) y d03 (congruencia) validados. El siguiente dominio ya no *valida* la arquitectura: la
*ejerce*. No se escala por percepción — esta tabla lo muestra.

## Evolución prevista (colega · 2026-07-18 · refinamiento, no fundamento)
No urgente; se abordará cuando aparezca la necesidad, cada una con su ADR si toca decisión:
- **Método estructurado** — ✅ hecho (RO-III-001: `metodo.tipo` + `criterios` como lista de objetos,
  extensibles con peso/obligatorio/origen sin romper compatibilidad).
- **Adaptador formalizado** — hoy `_parametros_de` es el único punto de acoplamiento al YAML
  (documentado); si BRN v3 cambia el formato, solo cambia el adaptador.
- **Artefacto multi-consumidor** — cuando haya más consumidores (Dashboard·API·Auditor·IA), el
  artefacto podría estructurarse en `runtime · metadata · provenance · schema`.
- **BRN Readiness Index** — convertir esta matriz en un índice con puntaje por dominio (Corpus·CNO·
  RO·SAT·Compilación·Validación·Runtime·Evidencia) para medir objetivamente la madurez de producción.

---
*BRN v2 · Matriz de Cobertura · Dylus Lab © 2026 · "El molde no está validado porque funcione una vez, sino cuando dos reglas de naturaleza distinta pasan por él sin que el compilador se entere de la diferencia. Ese punto ya se cruzó."*
