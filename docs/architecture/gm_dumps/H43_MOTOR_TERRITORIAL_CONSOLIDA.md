# H43_MOTOR_TERRITORIAL_CONSOLIDA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=37 · pobladas=34 · fórmulas=0
inputs(lee de): —
outputs(alimenta a): H00_ÍNDICE, H73_OUTPUT_API

## FÓRMULAS
```
(sin fórmulas)
```

## ETIQUETAS / DATOS (tope 600)
```
A1	🏛️ SIAP-ICPI v1.0 | Quira by Dylus Lab — H43_MOTOR_TERRITORIAL_CONSOLIDADO
A2	Territorial Intelligence Engine (TIE) | TPS = 0.35·N + 0.25·B + 0.20·S + 0.20·T | Ejecutado: 2026-05-10 | Montecristi 2023-2027
A3	"¿Dónde debe intervenir el alcalde primero para maximizar la transformación territorial de Montecristi?"
A5	N = NBI % (PDOT p.316/INEC 2022) | B = Brecha inversión 0-100 | S = Déficit servicios básicos 0-100 (PDOT p.115) | T = Tendencia histórica rezago 0-100
A6	⚠️ v1.1 CORREGIDO 2026-05-10: Datos agua/saneamiento actualizados — eliminados valores 100% (eran solo CUP PDOT p.115, no territorio parroquial completo). Ninguna parroquia tiene 100% de cobertura hídrica cantonal. Proyecto agua GAD 2026 confirma déficit severo.
A7	Ranking
B7	Geo_ID
C7	Parroquia
D7	Tipo
E7	Pob_Est
F7	N_NBI_%
G7	B_Inversion
H7	S_Servicios
I7	T_Tendencia
J7	TPS_Score
K7	Risk_Band
L7	Agua_%
M7	Saneamiento_%
N7	Equip_norm_%
O7	Pobla_en_Riesgo
P7	Priority_Index
Q7	Fuente_B
R7	Fuente_T
A8	1
B8	GEO_MNT_P06
C8	Isabel Muentes
D8	Urbana
E8	5700
F8	61.2
G8	86.36
H8	98.19
I8	76.48
J8	77.94
K8	ALTA
L8	1.02
M8	0
N8	4.4
O8	3488
P8	271.9
Q8	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R8	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A9	2
B9	GEO_MNT_0003
C9	Colorado
D9	Urbana
E9	3800
F9	58.7
G9	85.61
H9	71.88
I9	75.48
J9	71.42
K9	ALTA
L9	38.82
M9	27.62
N9	17.9
O9	2230
P9	159.3
Q9	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R9	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A10	3
B10	GEO_MNT_0006
C10	La Pila
D10	Rural
E10	4600
F10	55.9
G10	88
H10	76.88
I10	70
J10	70.94
K10	ALTA
L10	35
M10	22
N10	12.4
O10	2571
P10	182.4
Q10	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R10	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A11	4
B11	GEO_MNT_0004
C11	Leónidas Proaño
D11	Urbana
E11	4100
F11	54.3
G11	84.29
H11	77.94
I11	73.72
J11	70.41
K11	ALTA
L11	42
M11	18.5
N11	5.7
O11	2226
P11	156.7
Q11	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R11	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A12	5
B12	GEO_MNT_0005
C12	Gral. Alfaro
D12	Urbana
E12	6300
F12	49.8
G12	82.94
H12	72.67
I12	71.92
J12	67.08
K12	ALTA
L12	38
M12	12.4
N12	31.6
O12	3137
P12	210.4
Q12	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R12	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A13	6
B13	GEO_MNT_0002
C13	Aníbal San Andrés
D13	Urbana
E13	5200
F13	52.1
G13	83.63
H13	21.99
I13	72.84
J13	58.11
K13	MEDIA
L13	67.01
M13	67.01
N13	100
O13	2709
P13	157.4
Q13	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R13	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A14	7
B14	GEO_MNT_0001
C14	Montecristi
D14	Urbana
E14	39800
F14	38.4
G14	20
H14	68.6
I14	55
J14	43.16
K14	MEDIA
L14	47.12
M14	41.08
N14	6
O14	15283
P14	659.6
Q14	Agua/saneamiento CORREGIDO — ver nota CUP PDOT p.115
R14	ANÁLISIS_TENDENCIA_TERRITORIAL · eSIGEF / NBI rural cantonal
A16	═══ ANÁLISIS EJECUTIVO — SENTINEL READY OUTPUT ═══
A17	North Star Output
B17	¿Dónde intervenir primero?
C17	#Isabel Muentes (TPS 77.94) y #Colorado (TPS 71.42) son las zonas de intervención crítica para maximizar impacto territorial en el mandato 2023-2027.
A18	Parroquias Críticas
B18	1 parroquias en zona CRÍTICA
C18	Parroquia Isabel Muentes - Sectores criticos: Santa Isabela, Tierra Santa, San Eloy, Los Artesanos
A19	Parroquias Alta Prioridad
B19	4 parroquias en Alta Prioridad
C19	Colorado · La Pila · Leónidas Proaño · Gral. Alfaro
A20	Parroquias Estables
B20	2 en Seguimiento/Estable
C20	Aníbal San Andrés · Montecristi
A21	Impacto Humano — Crítico
B21	Personas en riesgo territorial (NBI × Población) en zonas críticas
C21	0 personas en zonas CRÍTICAS requieren intervención prioritaria
A22	Servicios — Caso extremo
B22	Isabel Muentes: cobertura crítica documentada (PDOT p.115)
C22	Agua: 1.02% · Saneamiento: 0.00% · Equipamiento: 1.00 m²/hab — Peores coberturas del cantón → TPS más alto
A23	Equidad Territorial
B23	Brecha de inversión vs NBI en parroquias rurales
C23	6 de 6 parroquias rurales sin inversión georeferenciada documentada — Brecha inversión > 80/100
A25	═══ METADATA — GOBERNANZA SEMÁNTICA ═══
A26	Dominio TGI
B26	III — Inteligencia Territorial
A27	Rol en SIAP
B27	MOTOR/OUTPUT — alimenta P-04 GeoTwin + P-05 Impacto Humano + P-10 Motor Predictivo
A28	Hojas INPUT
B28	KB_SERVICIOS_PARROQUIAS · ANÁLISIS_TENDENCIA_TERRITORIAL · CAPA_TERRITORIAL_MONTECRISTI · SCHEMA_NBI
A29	Fuente NBI N
B29	PDOT 2023-2027 p.316 + INEC Censo 2022
A30	Fuente Servicios S
B30	PDOT 2023-2027 p.115 · KB_SERVICIOS_PARROQUIAS
A31	Fuente Inversión B
B31	ANÁLISIS_TENDENCIA_TERRITORIAL (eSIGEF / POA georeferenciado)
A32	Fuente Tendencia T
B32	ANÁLISIS_TENDENCIA_TERRITORIAL 2023-2026
A33	Pesos fórmula
B33	N=35% · B=25% · S=20% · T=20% (Sum=100%)
A34	Próxima revisión
B34	Q2 2026 — cuando datos eSIGEF Q2 estén disponibles
A35	Alias UI
B35	Territorial Intelligence Engine (TIE) | Visible en P-04, P-05, P-10
A36	Creado
B36	2026-05-10
A37	Versión
B37	H43 v1.0 · SIAP-ICPI v1.0 · Quira by Dylus Lab
```