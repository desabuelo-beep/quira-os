# H04b_DIAGNÓSTICO_SOCIAL — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=44 · pobladas=38 · fórmulas=52
inputs(lee de): H01_PARÁMETROS, H12b_MOTOR_IBSC
outputs(alimenta a): H00_ÍNDICE, H12b_MOTOR_IBSC, H16c_PSG_PRESUPUESTO_GENERO
MARCADORES: A3: ← H01 | Fuente: PDOT 2023-2027 Diagnóstico Territorial. Esta hoja alim · M37: KB PDOT p.281 | Ordenanzas patrimonio cultural: 1 | inventario patrimo · B42: =IFERROR(H12b_MOTOR_IBSC!B41,"Pendiente ingesta Si_NBI") · A44: ⚠️ IBSC PENDIENTE DE DATOS: Las columnas Resultado_Real_2026 (col F) r

## FÓRMULAS
```
K13	=1+H01_PARÁMETROS!B38*I13+H01_PARÁMETROS!B37*J13
L13	=G13*K13
K14	=1+H01_PARÁMETROS!B38*I14+H01_PARÁMETROS!B37*J14
L14	=G14*K14
K15	=1+H01_PARÁMETROS!B38*I15+H01_PARÁMETROS!B37*J15
L15	=G15*K15
K16	=1+H01_PARÁMETROS!B38*I16+H01_PARÁMETROS!B37*J16
L16	=G16*K16
K17	=1+H01_PARÁMETROS!B38*I17+H01_PARÁMETROS!B37*J17
L17	=G17*K17
K18	=1+H01_PARÁMETROS!B38*I18+H01_PARÁMETROS!B37*J18
L18	=G18*K18
K19	=1+H01_PARÁMETROS!B38*I19+H01_PARÁMETROS!B37*J19
L19	=G19*K19
K20	=1+H01_PARÁMETROS!B38*I20+H01_PARÁMETROS!B37*J20
L20	=G20*K20
K21	=1+H01_PARÁMETROS!B38*I21+H01_PARÁMETROS!B37*J21
L21	=G21*K21
K22	=1+H01_PARÁMETROS!B38*I22+H01_PARÁMETROS!B37*J22
L22	=G22*K22
K23	=1+H01_PARÁMETROS!B38*I23+H01_PARÁMETROS!B37*J23
L23	=G23*K23
K24	=1+H01_PARÁMETROS!B38*I24+H01_PARÁMETROS!B37*J24
L24	=G24*K24
K25	=1+H01_PARÁMETROS!B38*I25+H01_PARÁMETROS!B37*J25
L25	=G25*K25
K26	=1+H01_PARÁMETROS!B38*I26+H01_PARÁMETROS!B37*J26
L26	=G26*K26
K27	=1+H01_PARÁMETROS!B38*I27+H01_PARÁMETROS!B37*J27
L27	=G27*K27
K28	=1+H01_PARÁMETROS!B38*I28+H01_PARÁMETROS!B37*J28
L28	=G28*K28
K29	=1+H01_PARÁMETROS!B38*I29+H01_PARÁMETROS!B37*J29
L29	=G29*K29
K30	=1+H01_PARÁMETROS!B38*I30+H01_PARÁMETROS!B37*J30
L30	=G30*K30
K31	=1+H01_PARÁMETROS!B38*I31+H01_PARÁMETROS!B37*J31
L31	=G31*K31
K32	=1+H01_PARÁMETROS!B38*I32+H01_PARÁMETROS!B37*J32
L32	=G32*K32
K33	=1+H01_PARÁMETROS!B38*I33+H01_PARÁMETROS!B37*J33
L33	=G33*K33
K34	=1+H01_PARÁMETROS!B38*I34+H01_PARÁMETROS!B37*J34
L34	=G34*K34
K35	=1+H01_PARÁMETROS!B38*I35+H01_PARÁMETROS!B37*J35
L35	=G35*K35
K36	=1+H01_PARÁMETROS!B38*I36+H01_PARÁMETROS!B37*J36
L36	=G36*K36
K37	=1+H01_PARÁMETROS!B38*I37+H01_PARÁMETROS!B37*J37
L37	=G37*K37
B41	=IFERROR(H12b_MOTOR_IBSC!B40,0)
B42	=IFERROR(H12b_MOTOR_IBSC!B41,"Pendiente ingesta Si_NBI")
```

## ETIQUETAS / DATOS (tope 600)
```
A1	⬅️ ÍNDICE GENERAL
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H04b_DIAGNÓSTICO_SOCIAL
A2	H04b — DIAGNÓSTICO SOCIAL NBI — Base para IBSC
A3	← H01 | Fuente: PDOT 2023-2027 Diagnóstico Territorial. Esta hoja alimenta H12b_MOTOR_IBSC. Sin datos NBI el IBSC queda en PENDIENTE DE VALIDACIÓN.
A5	▌ PARÁMETROS DIAGNÓSTICO NBI
A6	Año_Linea_Base
B6	2023
A7	Año_Meta
B7	2027
A8	Fuente_NBI
B8	PDOT GAD Montecristi 2023-2027 Cap. Diagnóstico
A9	Estado_IBSC
B9	[SIMULADO Q1-2026] — Actualizar con datos de campo reales
A12	ID_Meta
B12	Descripcion_Breve
C12	Dimension_NBI
D12	Linea_Base_NBI_Pct
E12	Meta_Reduccion_2027_Pct
F12	Resultado_Real_2026
G12	Cierre_Brecha_Pct
H12	Poblacion_Objetivo
I12	Flag_Genero_ODS5
J12	Flag_Ambiente_ODS13
K12	Factor_ODS
L12	Si_IBSC
M12	Fuente_Dato
A13	SC-I-N-01
B13	Agua Potable Rural
C13	Agua
D13	39.25
E13	42.38
F13	41.2% (Q1 simulado — avance parcial obras infraestructura)
G13	0.62
H13	12500
I13	1
J13	1
M13	KB PDOT p.115+185 | AGUA x PARROQUIA: Aníbal 67.01%, Colorado 38.82%, Gral.Alfaro 100%, Isabel Muentes 1.02%, Leonidas Proaño 100%, Montecristi 47.12% | Base cantón: cobertura red pública 66.13%
A14	SC-L-G-01
B14	Alcantarillado
C14	Saneamiento
D14	19.78
E14	24
F14	21.5% (Q1 simulado — estudios preliminares)
G14	0.41
H14	18000
I14	0
J14	1
M14	KB PDOT p.115 | SANEAMIENTO x PARROQUIA: Aníbal 67.01%, Colorado 27.62%, Gral.Alfaro 12.40%, Isabel Muentes 0%, Leonidas Proaño 52.98%, Montecristi 41.08% | Déficit crítico: Isabel Muentes, Gral.Alfaro
A15	AH-I-N-01
B15	Desechos Sólidos
C15	Hábitat
D15	18.5
E15	22
F15	18.8% (Q1 simulado — recolección EP Aseo activa)
G15	0.09
H15	38000
I15	1
J15	0
M15	KB PDOT p.186 | Cobertura recolección desechos sólidos: 100% área urbana | p.101: celda emergente 1,490 Ton reciclados | Diagnóstico componente asentamientos humanos
A16	AH-I-X-02
B16	Vialidad Cantonal
C16	Movilidad
D16	35.2
E16	40
F16	36.4% (Q1 simulado — vialidad en ejecución GAD)
G16	0.25
H16	65000
I16	0
J16	0
M16	KB PDOT p.309 | Vías CUP con tratamiento medio: 53% | sin tratamiento: 15.61% | p.178: equipamiento urbano CUP 445,544m²
A17	AH-I-X-01
B17	Finanzas Municipal
C17	Institucional
D17	0
E17	0
F17	23.8% (Q1 simulado — ejecución financiera parcial)
G17	0
H17	320
I17	0
J17	0
M17	KB PDOT p.281 | Ordenanzas gestión financiera: referencia cap. institucional | PDOT Cap. Institucional
A18	AH-I-X-03
B18	Salud Municipal
C18	Salud
D18	28.4
E18	32
F18	9.7% (Q1 simulado — Ti Patronato 9.71% Q1)
G18	0.05
H18	8500
I18	1
J18	0
M18	KB PDOT p.212 | Nacidos vivos establec. salud: 30.6% privado | p.208: indicadores salud materno-infantil | base devengado Patronato
A19	AH-C-X-01
B19	Protección Social
C19	Social
D19	22.1
E19	26
F19	22.5% (Q1 simulado — atención grupos vulnerables)
G19	0.1
H19	9200
I19	1
J19	0
M19	KB PDOT p.201 | Indicadores discapacidad y grupos prioritarios Montecristi | p.200: pop. adultos mayores | atención grupos prioritarios
A20	FA-I-X-01
B20	Gestión Riesgo
C20	Riesgo
D20	15
E20	12
F20	0.0% (Q1 — Bomberos sin devengado G7+8)
G20	0
H20	65000
I20	1
J20	1
M20	KB PDOT p.145 | Equipamientos en riesgo por inundaciones: 80% | p.113: zonas susceptibles inundación | riesgos diagnóstico
A21	FA-C-X-01
B21	Áreas Verdes
C21	Ambiente
D21	8.5
E21	12
F21	17.7% (Q1 simulado — EP Aseo áreas verdes)
G21	0.3
H21	45000
I21	0
J21	1
M21	KB PDOT p.179 | IVU Plan Bicentenario: 10.94 m²/hab | índice verde INEC: 1.89 m²/hab | meta 17.32 m²/hab al 2027
A22	FA-I-X-02
B22	Equipamiento Urbano
C22	Hábitat
D22	25.3
E22	28
F22	17.7% (Q1 simulado — EP Aseo equipamiento)
G22	0.25
H22	38000
I22	0
J22	1
M22	KB PDOT p.115+179 | EQUIPAMIENTO x PARROQUIA (m²/hab): Aníbal 22.66, Colorado 4.06, Gral.Alfaro 7.16, Isabel Muentes 1.00, Leonidas Proaño 1.29, Montecristi 1.36 | CUP total 3,952.2 ha
A23	SC-I-N-03
B23	Participación Ciudadana
C23	Gobernanza
D23	12
E23	18
F23	23.8% (Q1 simulado — participación ciudadana)
G23	0.2
H23	4500
I23	0
J23	0
M23	KB PDOT p.192 | Participación Montecristi en población provincial: 4.46-6.27% | PDOT Cap. Participación ciudadana
A24	PI-I-G-01
B24	Equipamientos Públicos
C24	Equipamiento
D24	20
E24	24
F24	23.8% (Q1 simulado — equipamiento público)
G24	0.25
H24	15000
I24	0
J24	0
M24	KB PDOT p.271 | Mercado central: 1,102.2m² | p.179: equipamientos CUP 445,544m² | estado regular: 73.34%, bueno: 26.34%
A25	PI-I-G-02
B25	PDOT/PUGS
C25	Planificación
D25	0
E25	0
F25	23.8% (Q1 simulado — PDOT seguimiento)
G25	0
H25	65000
I25	0
J25	0
M25	KB PDOT p.281 | Ordenanzas planificación territorial (PDOT/PUGS): 4 | SIL catastro digital en proceso
A26	PI-L-G-01
B26	Señalización Vial
C26	Movilidad
D26	18
E26	22
F26	23.8% (Q1 simulado — LOTAIP actualizado)
G26	0.25
H26	65000
I26	0
J26	0
M26	KB PDOT p.141 | Lesiones siniestralidad vial: 79% ciudadanos afectados | p.309: vías sin señalización CUP: 15.61%
A27	EP-L-N-01
B27	Vivienda Social
C27	Hábitat
D27	32.5
E27	36
F27	23.8% (Q1 simulado — convenio vivienda)
G27	0.25
H27	6800
I27	1
J27	0
M27	KB PDOT p.227 | Crecimiento viviendas ocupadas 2001-2010: 76 unidades | déficit habitacional cualitativo diagnóstico p.46
A28	EP-L-X-01
B28	Productivo
C28	Economía
D28	14.5
E28	18
F28	23.8% (Q1 simulado — turismo costero)
G28	0.25
H28	22000
I28	0
J28	0
M28	KB PDOT p.270 | Reincorporación polvo trigo proceso productivo: 9,092 kg | indicadores sector artesanal-productivo diagnóstico
A29	PI-TUR-01
B29	Turismo
C29	Economía
D29	5
E29	8
F29	0.0% (Q1 — sin devengado turismo)
G29	0
H29	8500
I29	0
J29	0
M29	KB PDOT p.179 | Área equipamiento turístico CUP: 48,895m² | Montecristi Ciudad Creativa — establecimientos turísticos
A30	PI-TUR-02
B30	Eventos Turísticos
C30	Economía
D30	3
E30	6
F30	0.0% (Q1 — sin devengado eventos)
G30	0
H30	5500
I30	0
J30	0
M30	PDOT Cap. Económico-Turístico | KB: sin indicador cuantitativo eventos en diagnóstico — requiere reporte GAD base cero
A31	FA-CC-01
B31	Cambio Climático
C31	Ambiente
D31	0
E31	0
F31	0.0% (Q1 — sin devengado cambio climático)
G31	0
H31	65000
I31	1
J31	1
M31	KB PDOT p.104 | Emisiones CO2 Manta-Montecristi: 14,075 Ton | p.103: PM2.5=17.04µg/m³, PM10=38.23µg/m³ | base cambio climático
A32	AH-AP-04
B32	Continuidad Agua
C32	Agua
D32	45
E32	48
F32	23.8% (Q1 simulado — agua potable continuidad)
G32	0.2
H32	12500
I32	0
J32	0
M32	KB PDOT p.185 | Abastecimiento agua por pozos: 5.14% | servicio agua 1x/15días: 28.18% | meta: continuidad diaria
A33	FA-DIS-01
B33	Disposición Final Desechos
C33	Hábitat
D33	22
E33	26
F33	17.7% (Q1 simulado — EP Aseo relleno)
G33	0.25
H33	65000
I33	1
J33	1
M33	KB PDOT p.101 | Material reciclable celda emergente: 1,490.46 Ton | capacidad disposición final: base 0% operativa inicio período
A34	SC-L-N-02
B34	Talento Humano
C34	Institucional
D34	0
E34	0
F34	23.8% (Q1 simulado — talento humano)
G34	0
H34	850
I34	1
J34	0
M34	KB PDOT p.92 | Capacitaciones Cuerpo Bomberos: 23 eventos referencia | PDOT Cap. Institucional — RR.HH. municipal
A35	AH-I-X-04
B35	Modernización Admin
C35	Institucional
D35	0
E35	0
F35	23.8% (Q1 simulado — transformación digital)
G35	0
H35	320
I35	0
J35	0
M35	PDOT Cap. Institucional | KB: indicadores tecnología/modernización no cuantificados en diagnóstico — base=0 intencional
A36	AH-C-X-02
B36	Catastro/SIT
C36	Institucional
D36	0
E36	0
F36	23.8% (Q1 simulado — catastro SIT)
G36	0
H36	65000
I36	1
J36	0
M36	KB PDOT p.281 | Ordenanzas catastro-SIT: 3 | p.115: CUP 3,952ha | p.120: suelo urbano 5.6% del cantón
A37	FA-L-N-01
B37	Patrimonio
C37	Cultural
D37	10
E37	13
F37	23.8% (Q1 simulado — patrimonio cultural)
G37	0.25
H37	12000
I37	1
J37	0
M37	KB PDOT p.281 | Ordenanzas patrimonio cultural: 1 | inventario patrimonial 100% pendiente al inicio del período
A40	▌ RESUMEN IBSC GLOBAL
A41	IBSC_Global_Provisional
A42	Estado_IBSC
A44	⚠️ IBSC PENDIENTE DE DATOS: Las columnas Resultado_Real_2026 (col F) requieren ingesta de datos de campo o reportes sectoriales verificados. Los valores del PDOT diagnóstico (LB y Meta) ya están cargados. Fase 2: completar col F con datos reales verificados.
```