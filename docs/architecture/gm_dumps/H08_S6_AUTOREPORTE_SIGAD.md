# H08_S6_AUTOREPORTE_SIGAD — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=44 · pobladas=39 · fórmulas=33
inputs(lee de): H01_PARÁMETROS, H04_S2_PLANIFICACIÓN_PDOT, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H12_MOTOR_ICPI_CANÓNICO, H15_ICPI_GLOBAL, H21_SAT-I
refs no resueltas: #H00_ÍNDICE
MARCADORES: A3: Silo 6: Registro del ICM oficial autoreportado al SNP/SIGAD. El ICM es · B44: ICM_Global=100% simulado desde reportes SIGAD oficiales 2023 y 2024 (a

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B13
B8	=H01_PARÁMETROS!B18
B9	=H12_MOTOR_ICPI_CANÓNICO!B33/100
B10	=B7-B9
B11	=B10*100
B17	=H04_S2_PLANIFICACIÓN_PDOT!C15
B18	=H04_S2_PLANIFICACIÓN_PDOT!C16
B19	=H04_S2_PLANIFICACIÓN_PDOT!C17
B20	=H04_S2_PLANIFICACIÓN_PDOT!C18
B21	=H04_S2_PLANIFICACIÓN_PDOT!C19
B22	=H04_S2_PLANIFICACIÓN_PDOT!C20
B23	=H04_S2_PLANIFICACIÓN_PDOT!C21
B24	=H04_S2_PLANIFICACIÓN_PDOT!C22
B25	=H04_S2_PLANIFICACIÓN_PDOT!C23
B26	=H04_S2_PLANIFICACIÓN_PDOT!C24
B27	=H04_S2_PLANIFICACIÓN_PDOT!C25
B28	=H04_S2_PLANIFICACIÓN_PDOT!C26
B29	=H04_S2_PLANIFICACIÓN_PDOT!C27
B30	=H04_S2_PLANIFICACIÓN_PDOT!C28
B31	=H04_S2_PLANIFICACIÓN_PDOT!C29
B32	=H04_S2_PLANIFICACIÓN_PDOT!C30
B33	=H04_S2_PLANIFICACIÓN_PDOT!C31
B34	=H04_S2_PLANIFICACIÓN_PDOT!C32
B35	=H04_S2_PLANIFICACIÓN_PDOT!C33
B36	=H04_S2_PLANIFICACIÓN_PDOT!C34
B37	=H04_S2_PLANIFICACIÓN_PDOT!C35
B38	=H04_S2_PLANIFICACIÓN_PDOT!C36
B39	=H04_S2_PLANIFICACIÓN_PDOT!C37
B40	=H04_S2_PLANIFICACIÓN_PDOT!C38
B41	=H04_S2_PLANIFICACIÓN_PDOT!C39
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H08_S6_AUTOREPORTE_SIGAD
A2	H08 — S6 AUTOREPORTE SIGAD — ICM OFICIAL 2026
B2	0.76
C2	[SIM-2026] RDC Ene-Abr 2026 — simulado coherente con tendencia histórica
A3	Silo 6: Registro del ICM oficial autoreportado al SNP/SIGAD. El ICM es diferente del ICPI: no tiene verificación algorítmica de los 8 silos. La diferencia ICM-ICPI es la Brecha de Verificación — mide la distancia entre el discurso oficial y la evidencia verificable en fuentes independientes.
A5	▌ PARÁMETROS S6
A6	Año_Fiscal
A7	ICM_Global_SIGAD_2026
B7	0.01
A8	Total_Metas_Reportadas
A9	ICPI_Verificado
A10	Brecha_Verificacion
A11	Brecha_puntos
A13	NOTA IMPORTANTE:
B13	El ICM autoreportado (100%) y el ICPI verificado (69.93%) miden cosas distintas. El ICM no es un error — refleja el cumplimiento programático declarado. El ICPI incorpora verificación algorítmica cruzada. La brecha de 30 puntos es una oportunidad de mejora metodológica.
A15	▌ DETALLE ICM POR META (2026)
A16	ID_Meta
B16	Descripción
C16	ICM_Meta_%
D16	Fuente_SIGAD
E16	Fecha_Reporte
A17	SC-I-N-01
C17	1
D17	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E17	2026-Q1 (simulado desde SIGAD 2023/2024)
F17	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A18	SC-L-N-02
C18	1
D18	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E18	2026-Q1 (simulado desde SIGAD 2023/2024)
F18	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A19	AH-I-X-01
C19	1
D19	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E19	2026-Q1 (simulado desde SIGAD 2023/2024)
F19	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A20	AH-I-X-02
C20	1
D20	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E20	2026-Q1 (simulado desde SIGAD 2023/2024)
F20	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A21	AH-I-X-03
C21	1
D21	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E21	2026-Q1 (simulado desde SIGAD 2023/2024)
F21	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A22	AH-I-N-01
C22	1
D22	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E22	2026-Q1 (simulado desde SIGAD 2023/2024)
F22	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A23	SC-L-G-01
C23	1
D23	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E23	2026-Q1 (simulado desde SIGAD 2023/2024)
F23	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A24	AH-I-X-04
C24	1
D24	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E24	2026-Q1 (simulado desde SIGAD 2023/2024)
F24	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A25	PI-I-G-01
C25	1
D25	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E25	2026-Q1 (simulado desde SIGAD 2023/2024)
F25	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A26	AH-C-X-01
C26	1
D26	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E26	2026-Q1 (simulado desde SIGAD 2023/2024)
F26	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A27	AH-C-X-02
C27	1
D27	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E27	2026-Q1 (simulado desde SIGAD 2023/2024)
F27	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A28	SC-I-N-03
C28	1
D28	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E28	2026-Q1 (simulado desde SIGAD 2023/2024)
F28	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A29	FA-I-X-01
C29	1
D29	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E29	2026-Q1 (simulado desde SIGAD 2023/2024)
F29	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A30	FA-C-X-01
C30	1
D30	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E30	2026-Q1 (simulado desde SIGAD 2023/2024)
F30	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A31	FA-I-X-02
C31	1
D31	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E31	2026-Q1 (simulado desde SIGAD 2023/2024)
F31	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A32	FA-L-N-01
C32	1
D32	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E32	2026-Q1 (simulado desde SIGAD 2023/2024)
F32	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A33	PI-I-G-02
C33	1
D33	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E33	2026-Q1 (simulado desde SIGAD 2023/2024)
F33	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A34	PI-L-G-01
C34	1
D34	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E34	2026-Q1 (simulado desde SIGAD 2023/2024)
F34	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A35	EP-L-N-01
C35	1
D35	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E35	2026-Q1 (simulado desde SIGAD 2023/2024)
F35	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A36	EP-L-X-01
C36	1
D36	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E36	2026-Q1 (simulado desde SIGAD 2023/2024)
F36	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A37	PI-TUR-01
C37	1
D37	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E37	2026-Q1 (simulado desde SIGAD 2023/2024)
F37	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A38	PI-TUR-02
C38	1
D38	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E38	2026-Q1 (simulado desde SIGAD 2023/2024)
F38	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A39	FA-CC-01
C39	1
D39	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E39	2026-Q1 (simulado desde SIGAD 2023/2024)
F39	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A40	AH-AP-04
C40	1
D40	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E40	2026-Q1 (simulado desde SIGAD 2023/2024)
F40	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A41	FA-DIS-01
C41	1
D41	SIGAD/SNP — Reporte ICM 2024 (extrapolado 2026)
E41	2026-Q1 (simulado desde SIGAD 2023/2024)
F41	[SIM] ICM=100% proyectado desde SIGAD 2023 y 2024 (ambos 100%). Actualizar cuando GADM publique RDC 2026 (previsto Q1-2027).
A44	⚠️ NOTA SIMULACIÓN H08
B44	ICM_Global=100% simulado desde reportes SIGAD oficiales 2023 y 2024 (ambos 100%). GAD Montecristi mantiene ICM=1.00 por 2 años consecutivos. RDC 2026 no disponible en Q1-2026 (se publica en Q1-2027). Esto genera la Brecha ICM-ICPI = 69 puntos — hallazgo central SIAP-ICPI.
```