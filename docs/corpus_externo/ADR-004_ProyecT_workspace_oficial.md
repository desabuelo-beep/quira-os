# ADR-004 — ProyecT es el workspace oficial de trabajo activo

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

El ecosistema Dylus Lab tenía archivos de trabajo activo distribuidos en múltiples carpetas: Gold_Master\, datos_fuente\, ProyecT\, Refactorización\, y otras. El Gold Master canónico no tenía una ubicación estable. Las cédulas SIGEF estaban mezcladas con scripts ETL.

Esto causaba:
- Sesiones que comenzaban con "¿dónde está el Excel canónico?"
- Riesgo de actualizar una versión histórica en lugar de la canónica
- Incapacidad de auditar el proyecto de forma externa

## Decisión

**`ProyecT\` es el workspace oficial de trabajo activo de QUIRA Montecristi.**

Contiene:
- `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` — aquí se abre, aquí se actualiza
- `Holding_Municipal_Montecristi\` — todos los documentos fuente del Holding
- `Cedulas_SIGEF_2026\` — cédulas presupuestarias (solo Excel, sin scripts)
- `Documentos_Montecristi\` — PDOT, resoluciones, planes oficiales
- `Normativa_PDF\` y `Normativa_Word\` — cuerpo normativo de referencia
- `historial_gold_master\` — 15 versiones históricas (solo referencia)

NO contiene scripts, legacy, ni archivos de otros proyectos.

## Consecuencias

- Cualquier nueva cédula SIGEF que llegue va a `ProyecT\Cedulas_SIGEF_2026\`
- Cualquier actualización al Gold Master se hace en `ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx`
- Los documentos oficiales nuevos del GAD van a `ProyecT\Holding_Municipal_Montecristi\` o `Documentos_Montecristi\`
- Un auditor externo puede abrir `ProyecT\` y encontrar todo el material fuente en orden

## Ver también

MAPA_ECOSISTEMA_QUIRA.md v2.0 (estructura completa), ADR-007 (Gold Master como fuente única)
