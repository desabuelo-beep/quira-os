# H11_S9_AGENDA_GLOBAL_ODS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=44 · pobladas=39 · fórmulas=32
inputs(lee de): H01_PARÁMETROS, H04_S2_PLANIFICACIÓN_PDOT, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H20_ICODS, H32_REPORTE_ODS_BILATERALES, H69_ELEGIBILIDAD_FONDOS, H89_TRUST_SCORE
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B55
B7	=H01_PARÁMETROS!B57
B10	=AVERAGE(F13:F37)
B14	=H04_S2_PLANIFICACIÓN_PDOT!C15
B15	=H04_S2_PLANIFICACIÓN_PDOT!C16
B16	=H04_S2_PLANIFICACIÓN_PDOT!C17
B17	=H04_S2_PLANIFICACIÓN_PDOT!C18
B18	=H04_S2_PLANIFICACIÓN_PDOT!C19
B19	=H04_S2_PLANIFICACIÓN_PDOT!C20
B20	=H04_S2_PLANIFICACIÓN_PDOT!C21
B21	=H04_S2_PLANIFICACIÓN_PDOT!C22
B22	=H04_S2_PLANIFICACIÓN_PDOT!C23
B23	=H04_S2_PLANIFICACIÓN_PDOT!C24
B24	=H04_S2_PLANIFICACIÓN_PDOT!C25
B25	=H04_S2_PLANIFICACIÓN_PDOT!C26
B26	=H04_S2_PLANIFICACIÓN_PDOT!C27
B27	=H04_S2_PLANIFICACIÓN_PDOT!C28
B28	=H04_S2_PLANIFICACIÓN_PDOT!C29
B29	=H04_S2_PLANIFICACIÓN_PDOT!C30
B30	=H04_S2_PLANIFICACIÓN_PDOT!C31
B31	=H04_S2_PLANIFICACIÓN_PDOT!C32
B32	=H04_S2_PLANIFICACIÓN_PDOT!C33
B33	=H04_S2_PLANIFICACIÓN_PDOT!C34
B34	=H04_S2_PLANIFICACIÓN_PDOT!C35
B35	=H04_S2_PLANIFICACIÓN_PDOT!C36
B36	=H04_S2_PLANIFICACIÓN_PDOT!C37
B37	=H04_S2_PLANIFICACIÓN_PDOT!C38
B38	=H04_S2_PLANIFICACIÓN_PDOT!C39
B44	=AVERAGE(F14:F38)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H11_S9_AGENDA_GLOBAL_ODS
A2	H11 — S9 AGENDA GLOBAL ODS — VINCULACIÓN PDOT ↔ AGENDA 2030
A3	Silo 9: Mapeo de las 25 metas PDOT con los 17 ODS de la Agenda 2030. Alimenta el ICODS (H20).
A5	▌ PARÁMETROS ODS
A6	PND_Nombre
A7	PND_Metas_ODS
A8	Total_ODS_Agenda_2030
B8	17
A9	ODS_Cubiertos_PDOT
B9	<openpyxl.worksheet.formula.ArrayFormula object at 0x0000025C380052B0>
A10	ICODS_Preliminar
A12	▌ REGISTRO VINCULACIÓN ODS — 25 METAS
A13	ID_Meta
B13	Descripción_Meta
C13	ODS_Principal
D13	ODS_Secundario
E13	Meta_ODS_Específica
F13	Score_Alineación
G13	Alineación_PND
A14	SC-I-N-01
C14	ODS 6 — Agua limpia
D14	ODS 3 — Salud
E14	6.1 Agua potable universal
F14	1
G14	Eje 3 Servicios Básicos
A15	SC-L-N-02
C15	ODS 8 — Trabajo
D15	ODS 16 — Instituciones
E15	8.3 Empleo y crecimiento
F15	0.75
G15	Eje 2 Economía
A16	AH-I-X-01
C16	ODS 16 — Instituciones
D16	ODS 8 — Trabajo
E16	16.6 Instituciones eficaces
F16	0.75
G16	Eje 4 Gobernanza
A17	AH-I-X-02
C17	ODS 9 — Infraestructura
D17	ODS 11 — Ciudades
E17	9.1 Infraestructura resiliente
F17	1
G17	Eje 3 Servicios Básicos
A18	AH-I-X-03
C18	ODS 3 — Salud
D18	ODS 10 — Igualdad
E18	3.8 Cobertura sanitaria universal
F18	1
G18	Eje 1 Derechos
A19	AH-I-N-01
C19	ODS 11 — Ciudades
D19	ODS 13 — Clima
E19	11.6 Impacto ambiental urbano
F19	1
G19	Eje 3 Servicios Básicos
A20	SC-L-G-01
C20	ODS 6 — Agua limpia
D20	ODS 11 — Ciudades
E20	6.2 Saneamiento y alcantarillado
F20	1
G20	Eje 3 Servicios Básicos
A21	AH-I-X-04
C21	ODS 16 — Instituciones
D21	—
E21	16.6 Instituciones eficaces
F21	0.75
G21	Eje 4 Gobernanza
A22	PI-I-G-01
C22	ODS 11 — Ciudades
D22	ODS 3 — Salud
E22	11.7 Espacios públicos inclusivos
F22	0.75
G22	Eje 3 Servicios Básicos
A23	AH-C-X-01
C23	ODS 5 — Género
D23	ODS 10 — Igualdad
E23	5.2 Erradicar violencia de género
F23	1
G23	Eje 1 Derechos
A24	AH-C-X-02
C24	ODS 16 — Instituciones
D24	ODS 11 — Ciudades
E24	16.6 Trámites digitales
F24	0.75
G24	Eje 4 Gobernanza
A25	SC-I-N-03
C25	ODS 16 — Instituciones
D25	ODS 10 — Igualdad
E25	16.7 Participación inclusiva
F25	0.75
G25	Eje 4 Gobernanza
A26	FA-I-X-01
C26	ODS 13 — Clima
D26	ODS 11 — Ciudades
E26	13.1 Resiliencia climática
F26	1
G26	Eje 5 Ambiente
A27	FA-C-X-01
C27	ODS 11 — Ciudades
D27	ODS 15 — Vida terrestre
E27	11.7 Áreas verdes urbanas
F27	1
G27	Eje 5 Ambiente
A28	FA-I-X-02
C28	ODS 11 — Ciudades
D28	ODS 12 — Producción
E28	11.3 Urbanización inclusiva
F28	0.75
G28	Eje 3 Servicios Básicos
A29	FA-L-N-01
C29	ODS 11 — Ciudades
D29	—
E29	11.4 Patrimonio cultural
F29	0.75
G29	Eje 1 Derechos
A30	PI-I-G-02
C30	ODS 16 — Instituciones
D30	—
E30	16.6 Planificación territorial
F30	1
G30	Eje 4 Gobernanza
A31	PI-L-G-01
C31	ODS 11 — Ciudades
D31	—
E31	11.2 Transporte sostenible
F31	0.75
G31	Eje 3 Servicios Básicos
A32	EP-L-N-01
C32	ODS 11 — Ciudades
D32	ODS 1 — Pobreza
E32	11.1 Vivienda digna y asequible
F32	1
G32	Eje 1 Derechos
A33	EP-L-X-01
C33	ODS 8 — Trabajo
D33	ODS 10 — Igualdad
E33	8.3 Emprendimiento y MIPYMES
F33	0.75
G33	Eje 2 Economía
A34	PI-TUR-01
C34	ODS 8 — Trabajo
D34	ODS 11 — Ciudades
E34	8.9 Turismo sostenible
F34	0.75
G34	Eje 2 Economía
A35	PI-TUR-02
C35	ODS 8 — Trabajo
D35	—
E35	8.9 Turismo y empleo
F35	0.75
G35	Eje 2 Economía
A36	FA-CC-01
C36	ODS 13 — Clima
D36	ODS 15 — Vida terrestre
E36	13.2 Planes de acción climática
F36	1
G36	Eje 5 Ambiente
A37	AH-AP-04
C37	ODS 6 — Agua limpia
D37	—
E37	6.1 Continuidad servicio agua
F37	1
G37	Eje 3 Servicios Básicos
A38	FA-DIS-01
C38	ODS 11 — Ciudades
D38	ODS 13 — Clima
E38	11.6 Gestión residuos sólidos
F38	1
G38	Eje 5 Ambiente
A41	⚠️ NOTA FALLA 19 — REGLA DE APLICACIÓN ÚNICA DEL BONO ODS:
B41	La columna Score_Alineación de H11 es INFORMATIVA — alimenta ICODS (H20) y reportes ODS, pero NO alimenta R_i del motor H12. El modificador ODS (Bono_Equidad ×1.15 para ODS 13 y ODS 5) se aplica UNA SOLA VEZ en H14_PONDERADORES columna Bono_Equidad. H12 lee R_i de H14!R_i_final directamente. Si H12 en algún momento referenciara el Score_Alineación de H11 para ajustar R_i, el bono se aplicaría ×1.3225 (dos veces). Esta hoja NO tiene ningún campo de R_i — es solo mapeo ODS.
A43	ODS_CUBIERTOS:
B43	<openpyxl.worksheet.formula.ArrayFormula object at 0x0000025C33882490>
C43	ODS distintos cubiertos por el PDOT (de 17 posibles)
A44	ICODS_Preliminar:
C44	Score promedio de alineación ODS — input para H20_ICODS
```