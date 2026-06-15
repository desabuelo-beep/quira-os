# SCHEMA_ECIAP_BRIDGE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=19 · pobladas=18 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE
MARCADORES: T11: Datos servicio pendientes

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	★ SCHEMA_ECIAP_BRIDGE — Tabla de Cruce PDOT ↔ SIAP por Territorio
C1	Vista única por Geo_ID · Fuente de verdad para PMV Demo Gestión
A3	Geo_ID
B3	Nombre_Territorio
C3	Tipo
D3	Nivel_Jerarquico
E3	Poblacion_2022
F3	Superficie_ha
G3	Num_Metas_PDOT
H3	Num_Proyectos_PAI
I3	Monto_PAI_Total_USD
J3	NBI_Total_Pct
K3	NBI_Agua_Pct
L3	NBI_Alcantarillado_Pct
M3	Cobertura_Agua_Servicio_Pct
N3	Cobertura_Sanea_Servicio_Pct
O3	Ti_POA_2026
P3	Monto_POA_2026_USD
Q3	Riesgo_Principal
R3	Riesgo_Nivel
S3	Unidad_Responsable_Principal
T3	Alerta_Principal
U3	Estado_AVEP
A4	GEO_MNT_CUP
B4	Centro Urbano Principal (Total)
C4	area_total
D4	1
E4	71066
F4	3952.20
G4	56
H4	145
I4	146,724,877
J4	23.00
K4	—
L4	—
M4	Prom:65.68
N4	Prom:36.82
O4	12.40%
P4	7,115,890
Q4	Inundación costera
R4	MEDIO
S4	GAD Municipal
T4	ICPI 53.56% — Transición Crítica
U4	🟡 EN RIESGO
A5	GEO_MNT_0001
B5	Montecristi
C5	parroquia_urbana
D5	1
F5	376.84
G5	—
H5	—
I5	—
J5	21.30
K5	—
L5	—
M5	47.12
N5	41.08
O5	12.40%
P5	6,900,860
Q5	Deslizamiento
R5	MEDIO
S5	GAD / Planificación
T5	Agua < 50%
U5	🟡 EN RIESGO
A6	GEO_MNT_0002
B6	Aníbal San Andrés
C6	parroquia_urbana
D6	1
F6	222.31
G6	—
H6	—
I6	—
J6	—
K6	—
L6	—
M6	67.01
N6	67.01
O6	12.40%
P6	10
Q6	Inundación
R6	BAJO
S6	GAD / APAA
T6	Mejor cobertura CUP
U6	🟢 SÓLIDA
A7	GEO_MNT_0003
B7	Colorado
C7	parroquia_urbana
D7	1
F7	386.80
G7	—
H7	—
I7	—
J7	—
K7	—
L7	—
M7	38.82
N7	27.62
O7	12.40%
P7	215,020
Q7	Inundación
R7	MEDIO
S7	GAD / APAA
T7	Agua y saneamiento críticos
U7	🟠 PRECARIA
A8	GEO_MNT_0004
B8	Leónidas Proaño
C8	parroquia_urbana
D8	1
F8	273.86
G8	—
H8	—
I8	—
J8	—
K8	—
L8	—
M8	100.00
N8	52.98
O8	12.40%
P8	0
Q8	Inundación
R8	BAJO
S8	GAD / APAA
T8	Saneamiento 52% — brecha
U8	🟡 EN RIESGO
A9	GEO_MNT_0007
B9	Isabel Muentes
C9	parroquia_urbana
D9	1
F9	777.27
G9	—
H9	—
I9	—
J9	—
K9	—
L9	—
M9	1.02
N9	0.00
O9	12.40%
P9	0
Q9	Inundación
R9	ALTO
S9	GAD / APAA
T9	BRECHA CRÍTICA — Agua 1%
U9	🔴 COLAPSO
A10	GEO_MNT_0008
B10	General Eloy Alfaro
C10	parroquia_urbana
D10	1
F10	511.13
G10	—
H10	—
I10	—
J10	—
K10	—
L10	—
M10	100.00
N10	12.40
O10	12.40%
P10	0
Q10	Deslizamiento
R10	MEDIO
S10	GAD / APAA
T10	Saneamiento 12% — crítico
U10	🔴 COLAPSO
A11	GEO_MNT_0006
B11	La Pila (Cabecera Parroquial Rural)
C11	parroquia_rural
D11	2
E11	2145
F11	66.28
G11	—
H11	—
I11	—
J11	—
K11	—
L11	—
M11	NO_ENCONTRADO
N11	NO_ENCONTRADO
O11	NO_ENCONTRADO
P11	328,180
Q11	Sequía
R11	MEDIO
S11	Junta Parroquial
T11	Datos servicio pendientes
U11	🟡 EN RIESGO
A12	GEO_MNT_0015
B12	Bajo del Pechiche
C12	poblado_rural_centro
D12	3
E12	3060
F12	172.44
G12	—
H12	—
I12	—
J12	67.90
K12	—
L12	—
M12	NO_ENCONTRADO
N12	NO_ENCONTRADO
O12	NO_ENCONTRADO
P12	0
Q12	Sequía
R12	ALTO
S12	GAD / Planificación
T12	NBI rural 67.9% — brecha
U12	🔴 COLAPSO
A13	GEO_MNT_0013
B13	Bajo de Afuera
C13	poblado_rural_centro
D13	3
E13	3172
F13	114.70
G13	—
H13	—
I13	—
J13	67.90
K13	—
L13	—
M13	NO_ENCONTRADO
N13	NO_ENCONTRADO
O13	NO_ENCONTRADO
P13	0
Q13	Sequía
R13	ALTO
S13	GAD / Planificación
T13	NBI rural 67.9% — brecha
U13	🔴 COLAPSO
A14	GEO_MNT_0014
B14	Bajo de la Palma
C14	poblado_rural_centro
D14	3
E14	3175
F14	90.03
G14	—
H14	—
I14	—
J14	67.90
K14	—
L14	—
M14	NO_ENCONTRADO
N14	NO_ENCONTRADO
O14	NO_ENCONTRADO
P14	0
Q14	Sequía
R14	ALTO
S14	GAD / Planificación
T14	NBI rural 67.9% — brecha
U14	🔴 COLAPSO
A15	GEO_MNT_0022
B15	Estancia Las Palmas
C15	poblado_rural_mayor
D15	4
E15	1612
F15	136.46
G15	—
H15	—
I15	—
J15	67.90
K15	—
L15	—
M15	NO_ENCONTRADO
N15	NO_ENCONTRADO
O15	NO_ENCONTRADO
P15	0
Q15	Sequía
R15	MEDIO
S15	GAD / EP Aseo
T15	NBI rural estimado
U15	🟠 PRECARIA
A16	GEO_MNT_0018
B16	Cárcel Eloy Alfaro
C16	poblado_rural_mayor
D16	4
E16	1638
F16	35.88
G16	—
H16	—
I16	—
J16	67.90
K16	—
L16	—
M16	NO_ENCONTRADO
N16	NO_ENCONTRADO
O16	NO_ENCONTRADO
P16	0
Q16	Sequía
R16	MEDIO
S16	GAD / Planificación
T16	Recolección 3 días/sem
U16	🟡 EN RIESGO
A17	GEO_MNT_0010
B17	Pile
C17	poblado_rural_mayor
D17	4
E17	1027
F17	52.94
G17	—
H17	—
I17	—
J17	67.90
K17	—
L17	—
M17	NO_ENCONTRADO
N17	NO_ENCONTRADO
O17	NO_ENCONTRADO
P17	0
Q17	Sequía
R17	MEDIO
S17	Junta Parroquial
T17	Recolección 2 días/sem
U17	🟡 EN RIESGO
A18	GEO_MNT_0027
B18	Río Manta
C18	poblado_rural_menor
D18	5
E18	333
F18	6.16
G18	—
H18	—
I18	—
J18	67.90
K18	—
L18	—
M18	NO_ENCONTRADO
N18	NO_ENCONTRADO
O18	NO_ENCONTRADO
P18	0
Q18	Inundación
R18	ALTO
S18	GAD / EP Aseo
T18	Sin recolección — QUEMAN
U18	🔴 COLAPSO
A19	GEO_MNT_0041
B19	Río de Oro
C19	poblado_rural_menor
D19	5
E19	75
F19	15.53
G19	—
H19	—
I19	—
J19	67.90
K19	—
L19	—
M19	NO_ENCONTRADO
N19	NO_ENCONTRADO
O19	NO_ENCONTRADO
P19	0
Q19	Sequía
R19	ALTO
S19	GAD / Planificación
T19	Sin recolección — OTROS
U19	🔴 COLAPSO
```