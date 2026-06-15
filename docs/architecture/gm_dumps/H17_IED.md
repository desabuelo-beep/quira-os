# H17_IED — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=25 · pobladas=22 · fórmulas=51
inputs(lee de): H04_S2_PLANIFICACIÓN_PDOT, H12_MOTOR_ICPI_CANÓNICO, H12d_ICPI_POR_ENTIDAD
outputs(alimenta a): H00_ÍNDICE, H28_RESUMEN_EJECUTIVO, H29_TABLERO_ALCALDE, H30_IED_POR_DIRECCIÓN, H73_OUTPUT_API, H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE
MARCADORES: F11: =IF(B11=0,"⚠️ Sin datos — conectar H04 dirección",IF(B11>=0.9,"🔵 Excel · F12: =IF(B12=0,"⚠️ Sin datos — conectar H04 dirección",IF(B12>=0.9,"🔵 Excel · F16: =IF(B16=0,"⚠️ Sin datos — conectar H04 dirección",IF(B16>=0.9,"🔵 Excel · F17: =IF(B17=0,"⚠️ Sin datos — conectar H04 dirección",IF(B17>=0.9,"🔵 Excel · F18: =IF(B18=0,"⚠️ Sin datos — conectar H04 dirección",IF(B18>=0.9,"🔵 Excel · F20: =IF(B20=0,"⚠️ Sin datos — conectar H04 dirección",IF(B20>=0.9,"🔵 Excel · F21: =IF(B21=0,"⚠️ Sin datos — conectar H04 dirección",IF(B21>=0.9,"🔵 Excel

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=IFERROR(B22,0)
B7	=IF(B6>=0.9,"🔵 Excelencia en Gobernanza",IF(B6>=0.7,"🟢 Gestión por Mandato",IF(B6>=0.4,"🟡 Transición Crítica",IF(B6>=0.2,"🟠 Gestión por Ocurrencia","🔴 Ruptura Sistémica"))))
B11	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="DAPS-01")*H12_MOTOR_ICPI_CANÓNICO!$J$6:$J$30)/SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="DAPS-01")*H12_MOTOR_ICPI_CANÓNICO!$K$6:$K$30),0)
C11	=IF(B11>=0.9,"🔵",IF(B11>=0.7,"🟢",IF(B11>=0.4,"🟡",IF(B11>=0.2,"🟠","🔴"))))
D11	=COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"DAPS-01")
E11	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="DAPS-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"DAPS-01")),0)
F11	=IF(B11=0,"⚠️ Sin datos — conectar H04 dirección",IF(B11>=0.9,"🔵 Excelencia — mantener estándares",IF(B11>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B11>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B12	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="DOP-01")*H12_MOTOR_ICPI_CANÓNICO!$J$6:$J$30)/SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="DOP-01")*H12_MOTOR_ICPI_CANÓNICO!$K$6:$K$30),0)
C12	=IF(B12>=0.9,"🔵",IF(B12>=0.7,"🟢",IF(B12>=0.4,"🟡",IF(B12>=0.2,"🟠","🔴"))))
D12	=COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"DOP-01")
E12	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="DOP-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"DOP-01")),0)
F12	=IF(B12=0,"⚠️ Sin datos — conectar H04 dirección",IF(B12>=0.9,"🔵 Excelencia — mantener estándares",IF(B12>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B12>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B13	=0
C13	=IF(B13>=0.9,"🔵",IF(B13>=0.7,"🟢",IF(B13>=0.4,"🟡",IF(B13>=0.2,"🟠","🔴"))))
D13	=0
E13	=0
F13	=IF(B13=0,"⚠️ Sin metas PDOT — TIC — sin metas PDOT asignadas","OK")
B16	=IFERROR(H12d_ICPI_POR_ENTIDAD!E10/100,0)
C16	=IF(B16>=0.9,"🔵",IF(B16>=0.7,"🟢",IF(B16>=0.4,"🟡",IF(B16>=0.2,"🟠","🔴"))))
D16	=IFERROR(H12d_ICPI_POR_ENTIDAD!C10,0)
E16	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="PAT-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"PAT-01")),0)
F16	=IF(B16=0,"⚠️ Sin datos — conectar H04 dirección",IF(B16>=0.9,"🔵 Excelencia — mantener estándares",IF(B16>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B16>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B17	=IFERROR(H12d_ICPI_POR_ENTIDAD!E8/100,0)
C17	=IF(B17>=0.9,"🔵",IF(B17>=0.7,"🟢",IF(B17>=0.4,"🟡",IF(B17>=0.2,"🟠","🔴"))))
D17	=IFERROR(H12d_ICPI_POR_ENTIDAD!C8,0)
E17	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="EPAM-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"EPAM-01")),0)
F17	=IF(B17=0,"⚠️ Sin datos — conectar H04 dirección",IF(B17>=0.9,"🔵 Excelencia — mantener estándares",IF(B17>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B17>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B18	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="RR.HH-01")*H12_MOTOR_ICPI_CANÓNICO!$J$6:$J$30)/SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="RR.HH-01")*H12_MOTOR_ICPI_CANÓNICO!$K$6:$K$30),0)
C18	=IF(B18>=0.9,"🔵",IF(B18>=0.7,"🟢",IF(B18>=0.4,"🟡",IF(B18>=0.2,"🟠","🔴"))))
D18	=COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"RR.HH-01")
E18	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="RR.HH-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"RR.HH-01")),0)
F18	=IF(B18=0,"⚠️ Sin datos — conectar H04 dirección",IF(B18>=0.9,"🔵 Excelencia — mantener estándares",IF(B18>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B18>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B19	=0
C19	=IF(B19>=0.9,"🔵",IF(B19>=0.7,"🟢",IF(B19>=0.4,"🟡",IF(B19>=0.2,"🟠","🔴"))))
D19	=0
E19	=0
F19	=IF(B19=0,"⚠️ Sin metas PDOT — Secretaría General — sin metas PDOT","OK")
B20	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="ALC-01")*H12_MOTOR_ICPI_CANÓNICO!$J$6:$J$30)/SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="ALC-01")*H12_MOTOR_ICPI_CANÓNICO!$K$6:$K$30),0)
C20	=IF(B20>=0.9,"🔵",IF(B20>=0.7,"🟢",IF(B20>=0.4,"🟡",IF(B20>=0.2,"🟠","🔴"))))
D20	=COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"ALC-01")
E20	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="ALC-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"ALC-01")),0)
F20	=IF(B20=0,"⚠️ Sin datos — conectar H04 dirección",IF(B20>=0.9,"🔵 Excelencia — mantener estándares",IF(B20>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B20>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B21	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="FIN-01")*H12_MOTOR_ICPI_CANÓNICO!$J$6:$J$30)/SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="FIN-01")*H12_MOTOR_ICPI_CANÓNICO!$K$6:$K$30),0)
C21	=IF(B21>=0.9,"🔵",IF(B21>=0.7,"🟢",IF(B21>=0.4,"🟡",IF(B21>=0.2,"🟠","🔴"))))
D21	=COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"FIN-01")
E21	=IFERROR(SUMPRODUCT((H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39="FIN-01")*H12_MOTOR_ICPI_CANÓNICO!$I$6:$I$30)/MAX(1,COUNTIF(H04_S2_PLANIFICACIÓN_PDOT!$K$15:$K$39,"FIN-01")),0)
F21	=IF(B21=0,"⚠️ Sin datos — conectar H04 dirección",IF(B21>=0.9,"🔵 Excelencia — mantener estándares",IF(B21>=0.7,"🟢 Gestión por Mandato — monitoreo continuo",IF(B21>=0.4,"🟡 Transición Crítica — plan de mejora","🔴 Nivel de Atención Alta — intervención requerida"))))
B22	=IFERROR(SUMPRODUCT((D11:D21>0)*B11:B21*D11:D21)/MAX(1,SUMPRODUCT((D11:D21>0)*D11:D21)),0)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H17_IED
A2	H17 — IED — ÍNDICE DE EFICIENCIA POR DIRECCIÓN
A3	Desglosa el ICPI por dirección municipal según Estatuto Orgánico. Alimenta H29 (Tablero Alcalde) y H30 (IED por Dirección).
A5	▌ IED GLOBAL
A6	IED_Global_2025
A7	Clasificación_IED
A9	▌ IED POR DIRECCIÓN (valores 2025 de referencia)
A10	Dirección
B10	IED_%
C10	Nivel_AVEP
D10	Metas_Asignadas
E10	Ci_Promedio
F10	Diagnóstico
A11	Dirección de Agua y Saneamiento
A12	Dirección de Obras Públicas
A13	Dirección TIC
A14	❌ Dir. Salud — Competencia del Ministerio, no en Res. 040-2025
B14	0
C14	⚫
D14	0
E14	0
F14	⚫ Excluida del organigrama GAD · Ver H_ORGANICO_040_2025 — Res. 040-2025
A15	❌ Dir. Educación — Competencia del Ministerio, no en Res. 040-2025
B15	0
C15	⚫
D15	0
E15	0
F15	⚫ Excluida del organigrama GAD · Ver H_ORGANICO_040_2025 — Res. 040-2025
A16	Patronato Municipal
A17	Dirección Ambiental
A18	Dirección Administrativa
A19	Secretaría General
A20	Dirección de Cultura y Deporte
A21	Dirección Económica
A22	IED_Global_Calculado
C22	⚠️ IED_Global ponderado por N°metas. Dirs sin PDOT (TIC/Salud/Edu/Sec) = 0 no arrastran la media.
A24	▌ LENGUAJE PREVENTIVO — PROTOCOLO QUIRA
B24	🔴 'Nivel de Atención Alta' = requiere plan de acción. No usar 'Ruptura' ni 'Intervención urgente'.
B25	🟠 'Gestión por Ocurrencia' = plan de mejora recomendado. No usar 'Insuficiente'.
```