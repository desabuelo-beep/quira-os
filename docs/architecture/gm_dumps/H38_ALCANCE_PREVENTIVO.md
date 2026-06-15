# H38_ALCANCE_PREVENTIVO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=23 · pobladas=19 · fórmulas=3
inputs(lee de): H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H38_ALCANCE_PREVENTIVO
A2	H38 — ALCANCE PREVENTIVO — PROTOCOLO DE GESTIÓN ANTICIPADA
A3	Guía de acción preventiva para fortalecer la gestión antes de que los riesgos se materialicen.
A5	▌ MATRIZ DE ACCIÓN PREVENTIVA
A6	Señal_SAT
B6	Condición de activación
C6	Impacto potencial
D6	Acción preventiva recomendada
E6	Responsable
F6	Plazo sugerido
A7	SAT-0
B7	Brecha POA-PAC > 20%
C7	Retraso en contrataciones
D7	Revisar y alinear PAC con metas POA prioritarias
E7	Dir. de Contrataciones + Directores
F7	< 15 días
A8	SAT-I
B8	ICM alto + cobertura parcial
C8	Subreporte de gestión
D8	Ampliar reporte SIGAD a todas las metas del PDOT
E8	Planificación + Secretaría General
F8	30 días
A9	SAT-II
B9	Reforma > 5% presupuesto
C9	Reconfiguración de prioridades
D9	Revisar cronograma con equipo técnico
E9	Dir. Económica + Alcaldía
F9	15 días
A10	SAT-III
B10	Ti < 10% en alguna meta
C10	Sub-ejecución de inversión
D10	Identificar y eliminar bloqueos administrativos
E10	Director de área responsable
F10	7 días
A11	SAT-IV
B11	Inversión < 65%
C11	Incumplimiento fiscal COOTAD
D11	Revisar estructura del gasto con Dir. Económica
E11	Dir. Económica + Alcaldía
F11	Inmediato
A12	SAT-V
B12	Brecha compromisos CPCCS > 30%
C12	Señal de rendición de cuentas
D12	Actualizar compromisos y documentar avances
E12	Secretaría General + CPCCS
F12	30 días
A13	SAT-VI
B13	Desvío PP > 10%
C13	Pérdida de confianza ciudadana
D13	Convocar mesa técnica con asamblea ciudadana
E13	Alcaldía + CPCCS
F13	15 días
A15	▌ SEMÁFORO DE GESTIÓN PREVENTIVA
A16	Nivel Verde (0 SATs activos):
B16	Gestión en rango. Monitoreo mensual.
A17	Nivel Amarillo (1-2 SATs activos):
B17	Revisión quincenal con equipo técnico.
A18	Nivel Naranja (3-4 SATs activos):
B18	Mesa técnica mensual con alcaldía.
A19	Nivel Rojo (5+ SATs activos):
B19	Convocatoria urgente de gabinete ampliado.
A21	Nivel actual:
B21	— Ver H28_RESUMEN_EJECUTIVO para estado SAT activos —
A23	Nota: Lenguaje 100% preventivo. Ninguna señal SAT implica sanción — solo activación de protocolos de mejora continua.
```