# H36b_LOOKUP_ARRASTRE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=44 · pobladas=41 · fórmulas=8
inputs(lee de): —
outputs(alimenta a): H00_ÍNDICE, H39_AUTOCONTROL_ECOSISTEMA
refs no resueltas: #H00_ÍNDICE
MARCADORES: P32: 🔴 PENDIENTE — Requiere Presupuesto/POA Bomberos 2023 para dato real · P34: 🟡 PARCIAL — eSIGEF 2025 corte inicial. Obra principal pendiente ejecuc · P36: ✅ REAL — eSIGEF EP Aseo 2024 verificado · POA pendiente · P37: ✅ REAL — eSIGEF EP Aseo 2025 verificado · POA/RDC pendientes · J39: =SUMIF(J21:J37,"<>🔴 PENDIENTE",J21:J37)

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
F1	=TODAY()
C39	=COUNTA(C21:C37)
D39	=COUNTA(D21:D37)
J39	=SUMIF(J21:J37,"<>🔴 PENDIENTE",J21:J37)
K39	=AVERAGE(K21:K37)
Q39	=AVERAGE(Q21:Q37)
A44	="SIAP-ICPI v1.0 Gold Master by DYLUS LAB © 2026 · 17 registros · 4 entidades · Actualización: "&TEXT(TODAY(),"dd/mm/yyyy")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H36b_LOOKUP_ARRASTRE
E1	⚠️ DATOS INMUTABLES
A2	H36b — LOOKUP ARRASTRE — REGISTRO HISTÓRICO INMUTABLE 2023-2025
A3	★ DATOS INMUTABLES: Este registro NO debe ser modificado una vez validado. Contiene los ARRASTREs históricos verificados de las 4 entidades.
A5	▌ ENTIDADES REGISTRADAS — ECOSISTEMA QUIRA
A6	ID_Ente
B6	RUC
C6	Nombre_Entidad
D6	Tipo_Entidad
E6	Marco_Legal
F6	Metas_PDOT_Vinculadas
G6	Estado
A7	ENTE-01
B7	1360000430001
C7	GAD Municipal de Montecristi
D7	GAD Central
E7	COOTAD Art.53
F7	Todas (25 metas)
G7	✅ ACTIVO
A8	ENTE-02
B8	1360059440001
C8	Patronato Municipal de Montecristi
D8	Adscrita Social
E8	COOTAD Art.249
F8	AH-I-X-03
G8	✅ ACTIVO
A9	ENTE-03
B9	1360051380001
C9	Cuerpo de Bomberos de Montecristi
D9	Autónoma Adscrita
E9	LOSC / COOTAD Art.140
F9	PI-I-G-01
G9	✅ ACTIVO
A10	ENTE-04
B10	1360086760001
C10	Empresa Pública Municipal de Aseo Integral Montecristi - EP
D10	Empresa Pública Adscrita
E10	LOEP Art.4 / COOTAD Art.55 lit.d)
F10	FA-C-X-01 · FA-I-X-02 · AH-I-N-01 · FA-DIS-01
G10	✅ ACTIVO
A11	ENTE-05
B11	(reservado)
C11	[Entidad futura]
D11	—
E11	—
F11	—
G11	⬜ RESERVADO
A12	▌ MODELO MPE — SECTORES
A13	Sector
B13	Min
C13	Max
D13	Pto_Medio
E13	Uso
A14	Infraestructura (Agua / Vías / Obras)
B14	0.65
C14	0.75
D14	0.7
E14	GAD Central — Grupos 7+8
A15	Social / Talento Humano / Patronato
B15	0.92
C15	0.98
D15	0.95
E15	Patronato Municipal
A16	Bienes y Servicios / Equipamiento
B16	0.78
C16	0.82
D16	0.8
E16	Todas las entidades
A17	Ambiental / Aseo / Relleno Sanitario
B17	0.68
C17	0.78
D17	0.73
E17	EP Aseo Integral
A18	Bomberil / Seguridad / Emergencias
B18	0.6
C18	0.7
D18	0.65
E18	Cuerpo de Bomberos
A19	▌ REGISTRO DE ARRASTREs HISTÓRICOS — 17 REGISTROS — 4 ENTIDADES — INMUTABLE
A20	ID_Registro
B20	ID_Ente
C20	Nombre_Entidad
D20	Año_Origen
E20	ID_Meta_PDOT
F20	Descripcion_Meta
G20	Codigo_Proceso_PAC
H20	Presupuesto_Codificado_Historico
I20	Devengado_Acumulado_T1
J20	Saldo_Arrastrado
K20	Porcentaje_Ejecutado_Historico
L20	Fuente_Documental
M20	Tipo_Dato
N20	Tasa_MPE_Aplicada
O20	Hash_SHA256_Forense
P20	Validado_Cascada
Q20	EED_Score
A21	ARRASTRE-001
B21	ENTE-01
C21	GAD Central
D21	2024
E21	AH-I-X-02
F21	Vialidad urbana
G21	PAC-2024-001
H21	850000
I21	595000
J21	255000
K21	0.7
L21	PAC_GAD_2024.pdf
M21	SIMULADO-MPE-v1.0
N21	0.7
O21	[SIMULADO-MPE-v1.0]
P21	✅ ARRASTRE SIMULADO [MPE]
Q21	0.5
A22	ARRASTRE-002
B22	ENTE-01
C22	GAD Central
D22	2024
E22	PI-L-G-01
F22	LOTAIP transparencia (renombrada a PI-L-G-01 en PDOT 2025 — antes AH-GO-01 SIMULADO-LEGACY)
G22	PAC-2024-002
H22	45000
I22	36000
J22	9000
K22	0.8
L22	PAC_GAD_2024.pdf
M22	SIMULADO-LEGACY-v1.0
N22	0.8
O22	[SIMULADO-MPE-v1.0]
P22	✅ ARRASTRE SIMULADO [MPE]
Q22	0.5
A23	ARRASTRE-003
B23	ENTE-02
C23	Patronato Municipal de Montecristi
D23	2024
E23	AH-I-X-03
F23	Grupos prioritarios
G23	PAC-PAT-2024-001
H23	1994567.57
I23	1072502.87
J23	922064.7
K23	0.5377
L23	Patronato_Presupesto_2024.xlsx · PAC_PATRONATO_2024.pdf · Patronato_RDC_2024.pdf
M23	REAL-VERIFICADO-v1.0
N23	0.5377
O23	[REAL-VERIFICADO · 101 partidas · 12 grupos]
P23	✅ ARRASTRE VERIFICADO
Q23	1
A24	ARRASTRE-004
B24	ENTE-01
C24	GAD Central
D24	2023
E24	AH-AP-04
F24	Participación ciudadana
G24	PAC-2023-015
H24	120000
I24	84000
J24	36000
K24	0.7
L24	PAC_GAD_2023.pdf
M24	SIMULADO-MPE-v1.0
N24	0.7
O24	[SIMULADO-MPE-v1.0]
P24	✅ ARRASTRE SIMULADO [MPE]
Q24	0.5
A25	ARRASTRE-005
B25	ENTE-04
C25	EP Aseo
D25	2024
E25	FA-C-X-01
F25	Desechos sólidos relleno
G25	PAC-EPASEO-2024-001
H25	650000
I25	474500
J25	175500
K25	0.73
L25	PAC_EPASEO_2024.pdf
M25	⚫ SUPERSEDED
N25	0.73
O25	[SIMULADO-MPE-v1.0 — SUPERSEDED por ARRASTRE-016]
P25	⚫ SUPERSEDED — Reemplazado por ARRASTRE-016
Q25	0
A26	ARRASTRE-006
B26	ENTE-04
C26	EP Aseo
D26	2024
E26	FA-I-X-02
F26	Recolección barrido
G26	PAC-EPASEO-2024-002
H26	280000
I26	204400
J26	75600
K26	0.73
L26	PAC_EPASEO_2024.pdf
M26	⚫ SUPERSEDED
N26	0.73
O26	[SIMULADO-MPE-v1.0 — SUPERSEDED por ARRASTRE-017]
P26	⚫ SUPERSEDED — Reemplazado por ARRASTRE-017
Q26	0
A27	ARRASTRE-007
B27	ENTE-03
C27	Cuerpo de Bomberos de Montecristi
D27	2024
E27	PI-I-G-01
F27	Estación bomberil
G27	PAC-BOMB-2024-001
H27	320000
I27	208000
J27	112000
K27	0.65
L27	PAC_BOMBEROS_2024.pdf
M27	SIMULADO-MPE-v1.0
N27	0.65
O27	[SIMULADO-MPE-v1.0]
P27	✅ ARRASTRE SIMULADO [MPE]
Q27	0.5
A28	ARRASTRE-008
B28	ENTE-01
C28	GAD Central
D28	2023
E28	AH-I-X-01
F28	Agua potable rural
G28	PAC-2023-008
H28	1200000
I28	840000
J28	360000
K28	0.7
L28	PAC_GAD_2023.pdf
M28	SIMULADO-MPE-v1.0
N28	0.7
O28	[SIMULADO-MPE-v1.0]
P28	✅ ARRASTRE SIMULADO [MPE]
Q28	0.5
A29	ARRASTRE-009
B29	ENTE-02
C29	Patronato Municipal de Montecristi
D29	2023
E29	AH-I-X-03
F29	Inversión social integral
G29	PAC-PAT-2023-GLOBAL
H29	1508072.98
I29	528268.01
J29	979804.97
K29	0.3503
L29	Patronato_RDC_2023.pdf · PAC_PATRONATO_2023.pdf
M29	REAL-VERIFICADO-v1.0
N29	0.3503
O29	[REAL-VERIFICADO · RDC 2023 verificado]
P29	✅ ARRASTRE VERIFICADO
Q29	0.75
A30	ARRASTRE-010
B30	ENTE-01
C30	GAD Municipal de Montecristi
D30	2023
E30	AH-I-X-02
F30	Ejecución GAD Central 2023 · Ti Inversión Grupos 7+8 = 68.04%
G30	PAC-GADM-MONTECRISTI-2023 (cedula eSIGEF)
H30	19257163.75
I30	13102087.01
J30	6155076.74
K30	0.6803747
L30	Cedula_Presupuestaria_Gastos_2023.xls — Grupos 7+8
M30	REAL
N30	N/A
O30	Cédula 2023: Cod=$19,257,163.75 Dev=$13,102,087.01 Ti=68.04% Grupos 7+8. Total=$28,657,171.35.
P30	✅ REAL — Cédula eSIGEF 2023 verificada
Q30	0.75
A31	ARRASTRE-011
B31	ENTE-01
C31	GAD Municipal de Montecristi
D31	2024
E31	AH-I-X-02
F31	Ejecución GAD Central 2024 · Ti Inversión Grupos 7+8 = 79.61%
G31	PAC-GADM-MONTECRISTI-2024 (cedula eSIGEF)
H31	13616171.34
I31	10840503.33
J31	2775668.01
K31	0.7961492
L31	Cedula_Presupuestaria_Gastos_2024.xls — Grupos 7+8 + MFN-003 RDC 2024
M31	REAL
N31	N/A
O31	Cédula 2024: Cod=$13,616,171.34 Dev=$10,840,503.33 Ti=79.61% Grupos 7+8. Total=$27,920,762.02.
P31	✅ REAL — Cédula eSIGEF 2024 verificada
Q31	0.75
A32	ARRASTRE-012
B32	ENTE-03
C32	Cuerpo de Bomberos de Montecristi
D32	2023
E32	PI-I-G-01
F32	Bomberos 2023 — Sin Presupuesto/POA 2023
G32	PAC-BOMBEROS-2023 SERCOP: $354,600
H32	354600
I32	273042
J32	81558
K32	0.77
L32	PAC Bomberos 2023.pdf + RDC Bomberos 2023.pdf
M32	PROXY-RDC
N32	0.77
O32	RDC 2023: Meta1=77% capacitación / Meta2=110% inspecciones. PAC=$354,600. Sin eSIGEF 2023.
P32	🔴 PENDIENTE — Requiere Presupuesto/POA Bomberos 2023 para dato real
Q32	0.25
A33	ARRASTRE-013
B33	ENTE-03
C33	Cuerpo de Bomberos de Montecristi
D33	2024
E33	PI-I-G-01
F33	Bomberos 2024 — Datos reales eSIGEF
G33	PAC-BOMBEROS-2024 SERCOP: $542,904
H33	270884.84
I33	183667.02
J33	87217.82
K33	0.6780262
L33	Bomberos Presupuesto 2024.xlsx + PAC 2024.pdf + RDC 2024.pdf
M33	REAL
N33	N/A
O33	eSIGEF 2024: Cod=$270,884.84 Dev=$183,667.02 Ti=67.80% Grupos 7+8. Total cod=$1,500,000 Ti global=88.68%.
P33	✅ REAL — eSIGEF Bomberos 2024 verificado
Q33	1
A34	ARRASTRE-014
B34	ENTE-03
C34	Cuerpo de Bomberos de Montecristi
D34	2025
E34	PI-I-G-01
F34	Bomberos 2025 — Ti inversión bajo por obra edilicia sin iniciar
G34	PAC-BOMBEROS-2025
H34	285556.6
I34	46772.46
J34	238784.14
K34	0.1638
L34	Bomberos Presupuesto 2025.xlsx + PAC 2025.pdf + POA 2025.pdf
M34	REAL-PARCIAL
N34	N/A
O34	eSIGEF 2025: Cod=$285,556.60 Dev=$46,772.46 Ti=16.38%. Obra edilicia 84.02.02 ($174,500) con Dev=$0 explica bajo Ti. Ti global=83.24%.
P34	🟡 PARCIAL — eSIGEF 2025 corte inicial. Obra principal pendiente ejecución.
Q34	0.75
A35	ARRASTRE-015
B35	ENTE-04
C35	Empresa Pública Municipal de Aseo Integral Montecristi - EP
D35	2023
E35	FA-C-X-01
F35	EP Aseo 2023 — Simulación MPE. Sin Presupuesto/POA 2023. Rep. Legal: Andrea Amarilis Macías Vinces
G35	PAC-EP-ASEO-2023 SERCOP: $529,362.76
H35	529362.7
I35	423490.2
J35	0.8
K35	0.8
L35	PAC EP Aseo 2023.pdf + RDC EP Aseo 2023.pdf
M35	SIMULADO-MPE
N35	0.8
O35	RDC 2023: metas operativas 100%. PAC=$529,362.76. Sin eSIGEF 2023.
P35	🔴 SIMULADO — Requiere Presupuesto eSIGEF y POA 2023 para dato real
Q35	0.25
A36	ARRASTRE-016
B36	ENTE-04
C36	Empresa Pública Municipal de Aseo Integral Montecristi - EP
D36	2024
E36	FA-I-X-02
F36	EP Aseo 2024 — Datos reales eSIGEF. Sin POA 2024. Rep. Legal: Elias Gustavo Falconez Reyes
G36	PAC-EP-ASEO-2024 SERCOP: $686,657.35
H36	1686370.33
I36	1139741.48
J36	546628.85
K36	0.6759
L36	Aseo EP - Presupuesto diciembre 2024.xlsx + PAC 2024.pdf + RDC 2024.pdf
M36	REAL
N36	N/A
O36	eSIGEF dic.2024: Cod(7+8)=$1,686,370.33 Dev(7+8)=$1,139,741.48 Ti=67.59%. Total cod=$2,088,598.93.
P36	✅ REAL — eSIGEF EP Aseo 2024 verificado · POA pendiente
Q36	0.75
A37	ARRASTRE-017
B37	ENTE-04
C37	Empresa Pública Municipal de Aseo Integral Montecristi - EP
D37	2025
E37	FA-I-X-02
F37	EP Aseo 2025 — Datos reales eSIGEF. Ti inversión más alto del ecosistema (90.47%). Rep. Legal: Elias Gustavo Falconez Reyes
G37	PAC-EP-ASEO-2025 SERCOP: $582,698.73
H37	2362835.39
I37	2137680.33
J37	225155.06
K37	0.9047
L37	Aseo EP - Presupuesto diciembre 2025.xlsx + PAC 2025.pdf
M37	REAL
N37	N/A
O37	eSIGEF dic.2025: Cod(7+8)=$2,362,835.39 Dev(7+8)=$2,137,680.33 Ti=90.47%. Vehículos 84.01.05: $641,678→$641,182 (99.93%).
P37	✅ REAL — eSIGEF EP Aseo 2025 verificado · POA/RDC pendientes
Q37	0.75
A39	TOTALES
H39	[Simulado — actualizar con datos campo]
I39	[Simulado — actualizar con datos campo]
A41	NOTA 1: ARRASTRE-005 y ARRASTRE-006 marcados como ⚫ SUPERSEDED. Reemplazados por ARRASTRE-016 y ARRASTRE-017 con datos reales eSIGEF.
A42	NOTA 2: ARRASTRE-010 y ARRASTRE-011 contienen los datos canónicos de GAD Central. Ti 2023=68.04%, Ti 2024=79.61%. Estos valores son la base del ICPI histórico.
A43	NOTA 3: ICPI histórico REAL-eSIGEF ★ INMUTABLES: 2023=57.36% / 2024=67.12% / 2025=69.93% (canónico). Tendencia: +12.57pp en 3 años.
```