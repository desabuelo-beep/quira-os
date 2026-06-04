# ADR-002 — COOTAD e INEC son dominios normativos distintos, no intercambiables

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

Al construir indicadores de equidad territorial, QUIRA necesitaba medir tanto el cumplimiento legal (qué dice COOTAD sobre distribución de recursos) como la realidad demográfica (qué dice INEC sobre la población). Existía riesgo de mezclar unidades de medida incompatibles.

Ejemplo crítico: COOTAD Art. 249 define asignación en porcentaje del presupuesto. INEC define cobertura en porcentaje de la población. Ambos son porcentajes pero miden cosas distintas.

## Decisión

**COOTAD e INEC son dominios normativos separados. Sus métricas no se suman ni promedian entre sí.**

- **COOTAD**: mide cumplimiento normativo-presupuestario (compliance financiero = Piso 1)
- **INEC**: mide realidad demográfica y cobertura territorial (impacto real = Piso 2)
- Un indicador puede ser VERDE en COOTAD y ROJO en INEC simultáneamente — esto es dato, no contradicción
- En QTMP: cada indicador declara su `norma_fuente` (COOTAD vs INEC vs otro)

## Consecuencias

- Los C8 (indicadores) deben declarar explícitamente si miden compliance o impacto
- La "Paradoja COOTAD_249" (GAD cumple ley, Patronato no ejecuta, brechas persisten) es la demostración empírica de esta decisión
- Los índices complementarios Piso 2 (BETA-DOM12-001) son INEC, no COOTAD

## Ver también

ADR-006 (Ti = Piso 1), BETA-DOM12-001 (índices Piso 2)
