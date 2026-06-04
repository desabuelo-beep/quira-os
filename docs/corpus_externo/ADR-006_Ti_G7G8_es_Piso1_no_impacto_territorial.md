# ADR-006 — Ti_G7+G8 mide Piso 1 (compliance financiero), no impacto territorial

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  
**Origen**: Hallazgo C10 — Alpha 0.9 P2 (Patronato)  

## Contexto

Al analizar el Patronato Municipal de Montecristi se observó que `Ti_G7+G8 = 50%` (ROJO). Sin embargo, este indicador mide la tasa de ejecución presupuestaria de los grupos de inversión G7 y G8 — no mide cuántos adultos mayores fueron atendidos, cuántos pacientes de diálisis mantuvieron continuidad, ni qué porcentaje de la población objetivo recibió servicios.

En servicios sociales intensivos en capital humano (diálisis, psicología, gerontología, nutrición, educación inicial), pueden coexistir:

```
Ti financiero ROJO + Cobertura real VERDE
Ti financiero VERDE + Cobertura real ROJO
```

## Decisión

**`Ti_G7+G8` es un indicador de Piso 1 (compliance financiero presupuestario). Es válido y necesario. No mide impacto territorial.**

Piso 1 = compliance financiero:
- `Ti_G7+G8` — tasa de ejecución grupos inversión
- `Ratio_COOTAD_249` — cumplimiento asignación 10%
- Fuente: SIGEF

Piso 2 = impacto territorial (deferred a Beta):
- Cobertura adultos mayores (atendidos / población objetivo)
- Continuidad pacientes diálisis
- NNA con seguimiento activo
- Cobertura nutricional
- Fuente: INEC + registros administrativos institucionales

QUIRA puede mostrar `Ti_Patronato ROJO` y simultáneamente declarar que no conoce el impacto real en cobertura de servicios.

## Consecuencias

- En Alpha: `Ti=50% ROJO` es dato correcto y válido en su capa
- En Beta: agregar C8 de Piso 2 para Dom12 (BETA-DOM12-001)
- En UI: el semáforo Dom12 debe distinguir visualmente Piso 1 vs Piso 2
- Los sub-indicadores G71 vs G73 también son Beta (BETA-DOM12-002)

## Dato verificable Alpha 0.9

```
Ti_Patronato_2025 = 50.00%     → Piso 1 ROJO  — confirmado
Ratio_COOTAD_249  = 20.84%     → Piso 1 VERDE — pendiente_validacion (falta dic-2025)
Piso 2 Patronato               → no medido en Alpha — declarado abiertamente
```

## Ver también

ADR-002 (COOTAD vs INEC), BETA-DOM12-001, NOTA_METODOLOGICA_DOM12
