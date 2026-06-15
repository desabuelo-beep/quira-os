# H20_ICODS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=22 · pobladas=20 · fórmulas=7
inputs(lee de): H11_S9_AGENDA_GLOBAL_ODS, H11b_MONITOR_POLITICAS_PUBLICAS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H32_REPORTE_ODS_BILATERALES, H73_OUTPUT_API
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=AVERAGE(H11_S9_AGENDA_GLOBAL_ODS!F13:F37)
B7	=H11_S9_AGENDA_GLOBAL_ODS!B9
B8	=IFERROR(AVERAGE(H11b_MONITOR_POLITICAS_PUBLICAS!F13:F37),0.75)
B22	=SUM(B13:B21)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H20_ICODS
A2	H20 — ICODS — ÍNDICE DE CUMPLIMIENTO DE ODS
A3	Mide el grado de alineación de las metas PDOT con la Agenda 2030. Fuente: H11_S9_AGENDA_GLOBAL_ODS.
A5	▌ PANEL ICODS
A6	ICODS_Global
C6	← Dinámico desde H11 col F (alineación por meta)
A7	ODS_Cubiertos
A8	PND_Alineación
A9	Ref_2025
B9	0.9142
C9	🔵 Excelencia Territorial 2025
A11	▌ ODS CUBIERTOS (25 METAS)
A12	ODS
B12	Número_Metas_Vinculadas
C12	Nivel_Cobertura
A13	ODS 1 — Fin de la Pobreza
B13	3
A14	ODS 3 — Salud y Bienestar
B14	2
A15	ODS 4 — Educación de Calidad
B15	1
A16	ODS 5 — Igualdad de Género
B16	4
A17	ODS 6 — Agua Limpia
B17	3
A18	ODS 8 — Trabajo Decente
B18	2
A19	ODS 11 — Ciudades Sostenibles
B19	5
A20	ODS 13 — Acción Climática
B20	4
A21	ODS 15 — Vida de Ecosistemas
B21	1
A22	TOTAL
```