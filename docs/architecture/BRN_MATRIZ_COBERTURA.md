# BRN v2 · Matriz de Cobertura del Molde

> **Qué es.** La tabla que mide **objetivamente** cuánto está validado el molde CNO/RO — para decidir
> con evidencia, no con percepción, cuándo está listo para escalar a los 222 cantones (recomendación
> del colega · 2026-07-18). Cada dominio prueba una faceta distinta del modelo. Se actualiza al
> cerrar cada CNO.

## Los 4 invariantes que cada dominio debe cumplir
1. **El molde sirve** para ese dominio (la cadena se modela como CNO; la lógica, como RO).
2. **El compilador no cambia** (ni una línea específica del dominio; `if dominio==...` = fuga).
3. **El runtime tampoco cambia** (resuelve vigencia igual para todos).
4. **Solo cambia el contenido de la RO** (la estructura del molde se mantiene).

## Matriz
| Dominio | Naturaleza de la regla | CNO | RO | Compilador | Runtime | Estado |
|---|---|---|---|---|---|---|
| **d02 · Finanzas** | umbral cuantitativo (65/70%) | ✓ vigente · 6/6 SHA | ✓ vigente | ✓ compila | ✓ | **Validado** |
| **d03 · Mandato** | congruencia programática (fidelidad ≥85%) | ✓ 9/9 SHA | ✓ | ✓ sin `if` (grep=0) | — | **Propuesta** · pend. validación Javo |
| d01 · Planificación | — | pendiente | | | | Pendiente |
| d09 · Rendición | — | pendiente | | | | Pendiente |
| … | | | | | | |

## Lectura del examen d03 (colega · 2026-07-18)
d03 es la prueba dura: su regla **no** desemboca en un techo de gasto sino en un **procedimiento de
congruencia** (promesa→plan, ponderado). Resultado:
1. **El molde sirve** ✅ — cadena de 9 eslabones (CE·COD·COOTAD·COPLAFIP·LOPC), toda con SHA
   verificado; la lógica de medición (umbral 85% + criterios congruencia/cobertura/trazabilidad)
   cabe en la RO sin forzar el molde.
2. **El compilador no cambia** ✅ — 0 ramas de dominio (verificado por inspección); procesa la RO del
   mandato con el mismo `_parametros_de` que la financiera.
3. **El runtime** ⏳ — se confirmará al promover d03 a `vigente` y compilar (el gate hoy la salta por
   estar en `propuesta`, no por incapacidad).
4. **Solo cambia la RO** ✅ — CNO y RO nuevas; molde, catálogo (`brn_cno.py`) y compilador
   (`brn_compilador.py`) intactos.

**Conclusión parcial:** 3 de 4 invariantes confirmados con d03; el 4º (runtime) queda a un paso —
la validación humana de la CNO/RO del mandato. Con eso, el molde deja de estar validado sobre **un**
caso y pasa a estarlo sobre **dos naturalezas distintas** de regla — la señal que el colega marca como
el salto de "caso de uso validado" a "**modelo BRN** validado".

## Criterio de escalamiento a 222 cantones
El molde se considera **suficientemente validado para escalar** cuando ≥2 dominios de **naturaleza
distinta** cumplan los 4 invariantes con CNO/RO `vigentes` y compiladas. Hoy: d02 completo; d03 a un
paso. No se escala por percepción — se escala cuando esta tabla lo muestra.

---
*BRN v2 · Matriz de Cobertura · Dylus Lab © 2026 · "El molde no está validado porque funcione una vez, sino cuando dos reglas de naturaleza distinta pasan por él sin que el compilador se entere de la diferencia."*
