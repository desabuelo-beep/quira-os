# H11b_MONITOR_POLITICAS_PUBLICAS — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=47 · pobladas=41 · fórmulas=35
inputs(lee de): H01_PARÁMETROS, H04_S2_PLANIFICACIÓN_PDOT, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H01_PARÁMETROS, H20_ICODS, H69_ELEGIBILIDAD_FONDOS
refs no resueltas: #H00_ÍNDICE
MARCADORES: A43: Metas pendientes vinculación

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B55
B7	=H01_PARÁMETROS!B56
B8	=H01_PARÁMETROS!B57
B9	=H01_PARÁMETROS!B58
B13	=H04_S2_PLANIFICACIÓN_PDOT!C15
B14	=H04_S2_PLANIFICACIÓN_PDOT!C16
B15	=H04_S2_PLANIFICACIÓN_PDOT!C17
B16	=H04_S2_PLANIFICACIÓN_PDOT!C18
B17	=H04_S2_PLANIFICACIÓN_PDOT!C19
B18	=H04_S2_PLANIFICACIÓN_PDOT!C20
B19	=H04_S2_PLANIFICACIÓN_PDOT!C21
B20	=H04_S2_PLANIFICACIÓN_PDOT!C22
B21	=H04_S2_PLANIFICACIÓN_PDOT!C23
B22	=H04_S2_PLANIFICACIÓN_PDOT!C24
B23	=H04_S2_PLANIFICACIÓN_PDOT!C25
B24	=H04_S2_PLANIFICACIÓN_PDOT!C26
B25	=H04_S2_PLANIFICACIÓN_PDOT!C27
B26	=H04_S2_PLANIFICACIÓN_PDOT!C28
B27	=H04_S2_PLANIFICACIÓN_PDOT!C29
B28	=H04_S2_PLANIFICACIÓN_PDOT!C30
B29	=H04_S2_PLANIFICACIÓN_PDOT!C31
B30	=H04_S2_PLANIFICACIÓN_PDOT!C32
B31	=H04_S2_PLANIFICACIÓN_PDOT!C33
B32	=H04_S2_PLANIFICACIÓN_PDOT!C34
B33	=H04_S2_PLANIFICACIÓN_PDOT!C35
B34	=H04_S2_PLANIFICACIÓN_PDOT!C36
B35	=H04_S2_PLANIFICACIÓN_PDOT!C37
B36	=H04_S2_PLANIFICACIÓN_PDOT!C38
B37	=H04_S2_PLANIFICACIÓN_PDOT!C39
B41	=AVERAGE(F13:F37)
B42	=COUNTIF(F13:F37,">0")
B43	=COUNTIF(F13:F37,0)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H11b_MONITOR_POLITICAS_PUBLICAS
A2	H11b — MONITOR DE POLÍTICAS PÚBLICAS — PND 2025-2029
A3	Seguimiento de la alineación entre metas PDOT Montecristi y el Plan Nacional de Desarrollo "Ecuador No Se Detiene 2025-2029".
A5	▌ PARÁMETROS PND
A6	PND_Nombre
A7	PND_Resolución
A8	PND_Metas_ODS
A9	SNP_Nombre
A11	▌ VINCULACIÓN PDOT-PND — 25 METAS
A12	ID_Meta_PDOT
B12	Descripción
C12	Eje_PND
D12	Objetivo_PND
E12	Política_PND
F12	Score_Vinculación
G12	Observación
A13	SC-I-N-01
C13	Eje 3 — Servicios Básicos y Habitat
D13	Obj. 3.2 — Acceso universal agua potable
E13	P.3.2.1 — Ampliar infraestructura rural
F13	0.9
G13	Completar con documento PND 2025-2029
A14	SC-L-N-02
C14	Eje 2 — Economía al Servicio de la Vida
D14	Obj. 4.3 — Capacidades institucionales
E14	P.4.3.2 — Talento humano del sector público
F14	0.85
G14	Completar con documento PND 2025-2029
A15	AH-I-X-01
C15	Eje 4 — Gobernanza
D15	Obj. 4.1 — Finanzas públicas sanas
E15	P.4.1.1 — Eficiencia fiscal GAD
F15	0.9
G15	Completar con documento PND 2025-2029
A16	AH-I-X-02
C16	Eje 3 — Servicios Básicos y Habitat
D16	Obj. 3.4 — Movilidad sostenible
E16	P.3.4.1 — Vialidad urbano-rural
F16	0.85
G16	Completar con documento PND 2025-2029
A17	AH-I-X-03
C17	Eje 1 — Derechos para Todos
D17	Obj. 1.3 — Grupos vulnerables y prioritarios
E17	P.1.3.2 — Patronatos municipales
F17	0.9
G17	Completar con documento PND 2025-2029
A18	AH-I-N-01
C18	Eje 3 — Servicios Básicos y Habitat
D18	Obj. 5.2 — Gestión de residuos sólidos
E18	P.5.2.1 — EP de aseo integral
F18	0.85
G18	Completar con documento PND 2025-2029
A19	SC-L-G-01
C19	Eje 3 — Servicios Básicos y Habitat
D19	Obj. 3.3 — Saneamiento y alcantarillado
E19	P.3.3.1 — Alcantarillado rural GAD
F19	0.9
G19	Completar con documento PND 2025-2029
A20	AH-I-X-04
C20	Eje 4 — Gobernanza
D20	Obj. 4.2 — Transformación digital
E20	P.4.2.1 — Trámites electrónicos GAD
F20	0.85
G20	Completar con documento PND 2025-2029
A21	PI-I-G-01
C21	Eje 3 — Servicios Básicos y Habitat
D21	Obj. 3.5 — Equipamiento público
E21	P.3.5.2 — Mercados y espacios públicos
F21	0.8
G21	Completar con documento PND 2025-2029
A22	AH-C-X-01
C22	Eje 1 — Derechos para Todos
D22	Obj. 1.2 — Protección social
E22	P.1.2.1 — Grupos de atención prioritaria
F22	0.9
G22	Completar con documento PND 2025-2029
A23	AH-C-X-02
C23	Eje 4 — Gobernanza
D23	Obj. 4.4 — Información territorial
E23	P.4.4.1 — Catastro actualizado
F23	0.8
G23	Completar con documento PND 2025-2029
A24	SC-I-N-03
C24	Eje 4 — Gobernanza
D24	Obj. 4.5 — Participación ciudadana
E24	P.4.5.1 — Democracia participativa local
F24	0.85
G24	Completar con documento PND 2025-2029
A25	FA-I-X-01
C25	Eje 5 — Ambiente y Seguridad
D25	Obj. 5.4 — Gestión de riesgos
E25	P.5.4.2 — Cuerpos de bomberos locales
F25	0.8
G25	Completar con documento PND 2025-2029
A26	FA-C-X-01
C26	Eje 5 — Ambiente y Seguridad
D26	Obj. 5.2 — Gestión ambiental urbana
E26	P.5.2.2 — Áreas verdes y parques
F26	0.75
G26	Completar con documento PND 2025-2029
A27	FA-I-X-02
C27	Eje 3 — Servicios Básicos y Habitat
D27	Obj. 3.6 — Hábitat digno
E27	P.3.6.1 — Equipamiento urbano EP
F27	0.8
G27	Completar con documento PND 2025-2029
A28	FA-L-N-01
C28	Eje 1 — Derechos para Todos
D28	Obj. 2.5 — Cultura y patrimonio
E28	P.2.5.1 — Patrimonio arqueológico
F28	0.75
G28	Completar con documento PND 2025-2029
A29	PI-I-G-02
C29	Eje 4 — Gobernanza
D29	Obj. 4.1 — Planificación territorial
E29	P.4.1.2 — PDOT y OT municipal
F29	0.9
G29	Completar con documento PND 2025-2029
A30	PI-L-G-01
C30	Eje 3 — Servicios Básicos y Habitat
D30	Obj. 4.3 — Transparencia y acceso información
E30	P.4.3.1 — LOTAIP GAD
F30	0.85
G30	Completar con documento PND 2025-2029
A31	EP-L-N-01
C31	Eje 1 — Derechos para Todos
D31	Obj. 1.1 — Derecho a la vivienda
E31	P.1.1.2 — Vivienda social rural GAD
F31	0.8
G31	Completar con documento PND 2025-2029
A32	EP-L-X-01
C32	Eje 2 — Economía al Servicio de la Vida
D32	Obj. 2.3 — Turismo sostenible
E32	P.2.3.1 — Destinos turísticos costeros
F32	0.85
G32	Completar con documento PND 2025-2029
A33	PI-TUR-01
C33	Eje 2 — Economía al Servicio de la Vida
D33	Obj. 2.3 — Infraestructura turística
E33	P.2.3.2 — Balnearios y playas locales
F33	0.75
G33	Completar con documento PND 2025-2029
A34	PI-TUR-02
C34	Eje 2 — Economía al Servicio de la Vida
D34	Obj. 2.4 — Economía creativa
E34	P.2.4.1 — Eventos y ferias culturales
F34	0.7
G34	Completar con documento PND 2025-2029
A35	FA-CC-01
C35	Eje 5 — Ambiente y Seguridad
D35	Obj. 5.1 — Cambio climático
E35	P.5.1.1 — Municipios resilientes
F35	0.8
G35	Completar con documento PND 2025-2029
A36	AH-AP-04
C36	Eje 3 — Servicios Básicos y Habitat
D36	Obj. 3.2 — Continuidad de servicios básicos
E36	P.3.2.3 — Continuidad agua potable
F36	0.85
G36	Completar con documento PND 2025-2029
A37	FA-DIS-01
C37	Eje 5 — Ambiente y Seguridad
D37	Obj. 5.2 — Gestión integrada de residuos
E37	P.5.2.3 — Relleno sanitario cantonal
F37	0.85
G37	Completar con documento PND 2025-2029
A40	RESUMEN PND:
A41	Score_Vinculación promedio
A42	Metas vinculadas (Score > 0)
A43	Metas pendientes vinculación
A45	NOTA:
B45	Esta hoja se completa cuando esté disponible el documento oficial del PND 2025-2029 'Ecuador No Se Detiene'. Los Ejes PND han sido pre-asignados por afinidad temática. Los campos Objetivo_PND y Política_PND deben completarse con los números/códigos exactos del PND una vez publicado. Score_Vinculación alimenta H11 para el cálculo del ICODS.
A47	FUENTE PND:
B47	https://www.planificacion.gob.ec/plan-nacional-de-desarrollo/
```