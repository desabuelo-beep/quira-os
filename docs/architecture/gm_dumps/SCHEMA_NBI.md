# SCHEMA_NBI — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=90 · pobladas=83 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE, H73_OUTPUT_API

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	★ SCHEMA_NBI — Necesidades Básicas e Indicadores Sociales
C1	Fuente: INEC Censo 2022 · PDOT 2023-2027 · Montecristi
A3	▌ POBREZA MULTIDIMENSIONAL (INEC / PDOT p.316)
A4	Ambito
B4	Poblacion
C4	NBI_Total_%
D4	NBI_Extrema_%
E4	Poblacion_NBI
F4	Fuente
G4	Pagina_PDOT
A5	Urbano
B5	71066
C5	23.00
D5	4.80
E5	19756
F5	INEC Censo 2022 / PDOT
G5	316
A6	Rural
B6	28871
C6	67.90
D6	40.20
E6	31210
F6	INEC Censo 2022 / PDOT
G6	316
A7	Cantonal total
B7	99937
C7	51.0 (ponderado)
D7	—
E7	~50966
F7	Estimado ponderado
G7	316
A9	▌ DOTACIÓN SERVICIOS PÚBLICOS — PARROQUIAS CUP (PDOT 2023-2027 p.115)
A10	Parroquia
B10	Geo_ID
C10	Cobertura_Agua_%
D10	Cobertura_Saneamiento_%
E10	Cobertura_Pluvial_%
F10	Cobertura_Electricidad_%
G10	Equipamiento_m2_hab
H10	Fuente
I10	Pagina_PDOT
A11	Aníbal San Andrés
B11	GEO_MNT_0002
C11	67.01
D11	67.01
E11	7.18
F11	100.00
G11	22.66
H11	PDOT 2023-2027
I11	115
A12	Colorado
B12	GEO_MNT_0003
C12	38.82
D12	27.62
E12	0.00
G12	4.06
H12	PDOT 2023-2027
I12	115
A13	General Eloy Alfaro
B13	GEO_MNT_0008
C13	100.00
D13	12.40
E13	0.00
G13	7.16
H13	PDOT 2023-2027
I13	115
A14	Isabel Muentes
B14	GEO_MNT_0007
C14	1.02
D14	0.00
E14	0.00
G14	1.00
H14	PDOT 2023-2027
I14	115
A15	Leónidas Proaño
B15	GEO_MNT_0004
C15	100.00
D15	52.98
E15	0.00
G15	1.29
H15	PDOT 2023-2027
I15	115
A16	Montecristi
B16	GEO_MNT_0001
C16	47.12
D16	41.08
E16	8.55
G16	1.36
H16	PDOT 2023-2027
I16	115
A18	▌ NBI POR TERRITORIO (KB_NBI)
A19	Territorio
B19	Geo_ID
C19	Año_Dato
D19	NBI_Total_%
E19	NBI_Agua_%
F19	NBI_Alcantarillado_%
G19	NBI_Vivienda_%
H19	NBI_Educacion_%
I19	NBI_Salud_%
J19	Sistema_PDOT
K19	Pagina_PDOT
A20	Montecristi (área urbana)
B20	GEO_MNT_0001
C20	2022
D20	21.3
E20	None
F20	None
G20	None
H20	None
I20	None
J20	SOCIOCULTURAL
K20	316
A21	Montecristi (área urbana)
B21	GEO_MNT_0001
C21	2023
D21	21
E21	None
F21	None
G21	None
H21	None
I21	None
J21	SOCIOCULTURAL
K21	316
A22	Montecristi (área rural)
B22	GEO_MNT_0001
C22	2022
D22	53.3
E22	None
F22	None
G22	None
H22	None
I22	None
J22	SOCIOCULTURAL
K22	316
A23	Montecristi (área rural)
B23	GEO_MNT_0001
C23	2023
D23	52
E23	None
F23	None
G23	None
H23	None
I23	None
J23	SOCIOCULTURAL
K23	316
A24	Montecristi (área urbana)
B24	Montecristi (área urbana)
C24	2022
D24	21.3
E24	None
F24	None
G24	None
H24	None
I24	None
J24	316
K24	None
A25	Montecristi (área urbana)
B25	Montecristi (área urbana)
C25	2023
D25	21
E25	None
F25	None
G25	None
H25	None
I25	None
J25	316
K25	None
A26	Montecristi (área rural)
B26	Montecristi (área rural)
C26	2022
D26	53.3
E26	None
F26	None
G26	None
H26	None
I26	None
J26	316
K26	None
A27	Montecristi (área rural)
B27	Montecristi (área rural)
C27	2023
D27	52
E27	None
F27	None
G27	None
H27	None
I27	None
J27	316
K27	None
A29	▌ RECOLECCIÓN DESECHOS SÓLIDOS — SECTORES RURALES
A30	Sector
B30	Tiene_Servicio
C30	Cobertura_%
D30	Dias_por_Semana
E30	Otra_Forma_Eliminacion
F30	Fuente
A31	Las Lagunas
B31	SI
C31	100
D31	1
E31	—
F31	PDOT 2023-2027
A32	Cárcel Simón Bolívar
B32	SI
C32	100
D32	3
E32	—
F32	PDOT 2023-2027
A33	Cárcel Eloy Alfaro
B33	SI
C33	100
D33	3
E33	—
F33	PDOT 2023-2027
A34	Pepa de Huso
B34	SI
C34	100
D34	1
E34	—
F34	PDOT 2023-2027
A35	La Sequita
B35	SI
C35	100
D35	1
E35	—
F35	PDOT 2023-2027
A36	Pile
B36	SI
C36	100
D36	2
E36	—
F36	PDOT 2023-2027
A37	Cerro Guayabal
B37	SI
C37	100
D37	3
E37	—
F37	PDOT 2023-2027
A38	Estancia Las Palmas
B38	SI
C38	100
D38	1
E38	—
F38	PDOT 2023-2027
A39	Manantiales
B39	SI
C39	—
D39	2
E39	—
F39	PDOT 2023-2027
A40	Río Bravo
B40	SI
C40	100
D40	1
E40	—
F40	PDOT 2023-2027
A41	Camarón de Abajo
B41	SI
C41	100
D41	1
E41	—
F41	PDOT 2023-2027
A42	Los Cruces
B42	SI
C42	100
D42	2
E42	—
F42	PDOT 2023-2027
A43	Camarón de Arriba
B43	SI
C43	100
D43	1
E43	—
F43	PDOT 2023-2027
A44	Río Manta
B44	NO
C44	—
D44	—
E44	QUEMAN
F44	PDOT 2023-2027
A45	Aguas Nuevas
B45	SI
C45	100
D45	1
E45	—
F45	PDOT 2023-2027
A46	Unión Patria
B46	SI
C46	100
D46	3
E46	—
F46	PDOT 2023-2027
A47	Toalla Chica
B47	SI
C47	100
D47	3
E47	—
F47	PDOT 2023-2027
A48	Río de Oro
B48	NO
C48	—
D48	—
E48	OTROS
F48	PDOT 2023-2027
A49	Las Pampas
B49	SI
C49	100
D49	2
E49	—
F49	PDOT 2023-2027
A50	Ramón Silvino (Urb)
B50	NO
C50	—
D50	—
E50	—
F50	PDOT 2023-2027
A51	Ciudad Mangle (Urb)
B51	NO
C51	—
D51	—
E51	—
F51	PDOT 2023-2027
A52	Las Margaritas
B52	NO
C52	—
D52	—
E52	QUEMAN
F52	PDOT 2023-2027
A53	Cerro Copetón
B53	NO
C53	—
D53	—
E53	QUEMAN
F53	PDOT 2023-2027
A55	▌ INDICADORES DEMOGRÁFICOS Y SALUD
A56	Indicador
B56	Valor_2001
C56	Valor_2010
D56	Valor_2022
E56	Unidad
F56	Fuente
A57	Población total cantonal
B57	42875
C57	69042
D57	99937
E57	hab
F57	INEC
A58	Población urbana
B58	14610 (34.08%)
C58	45507 (65.91%)
D58	71066 (71.11%)
E58	hab
F58	INEC
A59	Población rural
B59	26156 (61.01%)
C59	21089 (30.55%)
D59	25792 (25.81%)
E59	hab
F59	INEC
A60	Parroquia La Pila
B60	2109 (4.92%)
C60	2446 (3.54%)
D60	3079 (3.08%)
E60	hab
F60	INEC
A61	Crecimiento anual promedio
B61	—
C61	5.44%
D61	3.13%
E61	% anual
F61	INEC
A62	Promedio hijos vivos
B62	—
C62	2.6
D62	2.3
E62	hijos
F62	INEC Censo
A63	Promedio hijos nacidos vivos
B63	2.1
C63	1.9
D63	1.6
E63	hijos
F63	INEC Censo
A64	Nacidos vivos (cantonal)
B64	—
C64	—
D64	25207
E64	nacidos/año
F64	INEC REVIT 2022
A65	Madres adolescentes 15-19 años
B65	—
C65	5971 (23.43%)
D65	4515 (17.90%)
E65	nacidos
F65	INEC REVIT
A66	Variación madres adolescentes
B66	—
C66	—
D66	-24.38%
E66	relativo
F66	INEC REVIT
A67	Nacidos con bajo peso
B67	—
C67	—
D67	2171 (8.60%)
E67	nacidos
F67	INEC REVIT
A68	Asistencia médica al parto
B68	—
C68	—
D68	24847 (98.60%)
E68	nacidos
F68	INEC REVIT
A69	Viviendas particulares
B69	—
C69	—
D69	36917
E69	unidades
F69	INEC
A70	Viviendas colectivas
B70	—
C70	—
D70	7
E70	unidades
F70	INEC
A71	Establecimientos salud Nivel 1
B71	—
C71	—
D71	10
E71	unidades
F71	MSP
A72	Instituciones educativas (2022-23)
B72	—
C72	—
D72	60
E72	instituciones
F72	Mineduc
A73	Estudiantes total (2022-23)
B73	—
C73	—
D73	20199
E73	alumnos
F73	Mineduc
A74	Docentes total (2022-23)
B74	—
C74	—
D74	920
E74	docentes
F74	Mineduc
A76	▌ PERCEPCIÓN CIUDADANA GOBERNABILIDAD (PDOT)
A77	Institucion
B77	Mala_%
C77	Media_%
D77	Buena_%
E77	Muy_Buena_%
F77	Fuente
A78	Municipio (GAD)
B78	18.5
C78	36.9
D78	38.75
E78	5.85
F78	PDOT 2023-2027
A79	Juntas Parroquiales
B79	25.75
C79	38.75
D79	32.25
E79	3.25
F79	PDOT 2023-2027
A80	Entidades Desconcentradas
B80	19.1
C80	38.32
D80	35.25
E80	7.33
F80	PDOT 2023-2027
A82	▌ EMPLEO Y TEJIDO EMPRESARIAL (REEM/INEC 2022)
A83	Tipo_Empresa
B83	Participacion_%
C83	Plazas_Empleo
D83	Sectores_Principales
E83	Fuente
A84	Empresas grandes
B84	65
C84	10239
D84	manufactura, comercio, primera necesidad
E84	REEM/INEC 2022
A85	Microempresas
B85	13
C85	2023
D85	comercio, servicios
E85	REEM/INEC 2022
A86	Pequeña empresa
B86	10
C86	1260
D86	servicios, comercio
E86	REEM/INEC 2022
A87	Mediana empresa tipo B
B87	7
C87	686
D87	construcción, servicios
E87	REEM/INEC 2022
A88	Mediana empresa tipo A
B88	5
C88	599
D88	manufactura, inmobiliario
E88	REEM/INEC 2022
A89	TOTAL FORMAL
B89	100
C89	15807
D89	—
E89	REEM/INEC 2022
A90	Nota: Montecristi ocupa el 3er lugar en plazas de empleo en Manabí (Manta 44.924 / Portoviejo 39.367 / Montecristi 15.807 / Chone 8.654)
E90	REEM/INEC 2022
```