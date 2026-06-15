# H04_S2_PLANIFICACIÓN_PDOT — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=43 · pobladas=40 · fórmulas=10
inputs(lee de): H00_ÍNDICE, H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H05_S3_OPERATIVO_POA, H06_S4_CONTRATACIÓN_SERCOP, H08_S6_AUTOREPORTE_SIGAD, H10_S8_PARTICIPACIÓN_CPCCS, H11_S9_AGENDA_GLOBAL_ODS, H11b_MONITOR_POLITICAS_PUBLICAS, H12d_ICPI_POR_ENTIDAD, H15_ICPI_GLOBAL, H17_IED, H25_MMP_MENSUAL, H31_REPORTE_CPCCS, H32_REPORTE_ODS_BILATERALES, H39_AUTOCONTROL_ECOSISTEMA, H71_EP_ADSCRITAS

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B7	=H01_PARÁMETROS!B18
B8	=H01_PARÁMETROS!B10
B9	=H01_PARÁMETROS!B13
B10	=H01_PARÁMETROS!B37
B11	=H01_PARÁMETROS!B38
E40	=SUM(E15:E39)
G40	=SUM(G15:G39)
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H04_S2_PLANIFICACIÓN_PDOT
A2	H04 — S2 PLANIFICACIÓN PDOT — 25 METAS ESTRATÉGICAS 2023-2027
A3	Silo 2: Fuente de las 25 metas del Plan de Desarrollo y Ordenamiento Territorial. Base del motor H12. Pi y Ri se calculan en H14.
A4	ATENCIÓN: Los Pi y Ri detallados aquí son INFORMATIVOS. Los valores canónicos que usa el motor H12 provienen de H14_PONDERADORES.
A6	▌ PARÁMETROS PDOT
A7	Total_Metas_PDOT
A8	GAD_Período
A9	Año_Activo
A10	Multiplicador_Clima
A11	Multiplicador_Genero
A13	▌ REGISTRO DE LAS 25 METAS PDOT 2023-2027
A14	ID_Meta
B14	Sistema
C14	Descripción_Meta_PDOT
D14	Competencia_GAD
E14	R_i_raw
F14	Bono_ODS
G14	R_i_final
H14	Eje_ODS
I14	Vinculación_CNE
J14	Estado_2026
K14	Cod_Unidad
L14	Unidad_Responsable
M14	ENTE_EJECUTOR
N14	ID_Meta_PDOT
O14	TIPO_FINANCIAMIENTO
P14	⚠️ NUNCA sobrescribir esta fila — es el ENCABEZADO. Los datos comienzan en fila 15.
A15	SC-I-N-01
B15	Agua potable
C15	Agua potable: cobertura 39.25%→42.38%; calidad 100% INEN 1108; infraestructura BUENA 22.74%→41.64%
D15	Exclusiva_Crítica
E15	1.5
F15	1
G15	0.8696
H15	ODS 6
I15	SC-002
J15	🔄 En seguimiento
K15	DAPS-01
L15	Dir. Agua Potable y Alcantarillado Sanitario
M15	ENTE-01
N15	SO-01-01
O15	PRESUPUESTO_GAD
A16	SC-L-N-02
B16	Talento humano
C16	Gestión del talento humano municipal: desempeño 80%→90%; plan capacitación 90% anual
D16	Exclusiva_Importante
E16	1
F16	1
G16	0.5797
H16	ODS 8
I16	SC-004
J16	🔄 En seguimiento
K16	RR.HH-01
L16	Dir. Talento Humano
M16	ENTE-01
N16	IN-01-01
O16	PRESUPUESTO_GAD
A17	AH-I-X-01
B17	Finanzas
C17	Sostenibilidad financiera: autonomía 43.35%→45.30%; gestión cobros y coactivas
D17	Exclusiva_Importante
E17	1
F17	1
G17	0.5797
H17	ODS 16
I17	IN-001
J17	🔄 En seguimiento
K17	FIN-01
L17	Dir. Financiera
M17	ENTE-01
N17	IN-02-01
O17	PRESUPUESTO_GAD
A18	AH-I-X-02
B18	Vialidad
C18	Vialidad cantonal: mantenimiento 43.8 km vías CUP + 57.22 km rurales; 23.77 km tratamiento medio
D18	Exclusiva_Crítica
E18	1.5
F18	1
G18	0.8696
H18	ODS 9
I18	IN-004
J18	🔄 En seguimiento
K18	DOP-01
L18	Dir. Obras Públicas y Fiscalización
M18	ENTE-01
N18	TE-01-01
O18	PRESUPUESTO_GAD
A19	AH-I-X-03
B19	Salud
C19	Salud integral municipal: población atendida 57,401→84,041 personas (+10% anual)
D19	Concurrente_Crítica
E19	0.5
F19	1
G19	0.2899
H19	ODS 3
I19	SC-001
J19	🔄 En seguimiento
K19	PAT-01
L19	Patronato Municipal de Montecristi
M19	ENTE-02
N19	SO-02-01
O19	PRESUPUESTO_GAD
A20	AH-I-N-01
B20	Desechos
C20	Gestión integral desechos sólidos: 20,118→23,086 Tn/año; relleno sanitario; capacidad disposición 0%→20%
D20	Exclusiva_Crítica
E20	1.5
F20	1.15
G20	1
H20	ODS 11+13
I20	SC-006
J20	🔄 En seguimiento
K20	EPAM-01
L20	Dir. Gestión Ambiental y Riesgos + EP Aseo
M20	ENTE-04
N20	AM-01-01
O20	PRESUPUESTO_GAD
A21	SC-L-G-01
B21	Alcantarillado
C21	Alcantarillado sanitario: cobertura 19.77%→24.32%; PTAR 0%→75%; estaciones bombeo 36%→72%
D21	Exclusiva_Crítica
E21	1.5
F21	1
G21	0.8696
H21	ODS 6
I21	SC-002
J21	🔄 En seguimiento
K21	DAPS-01
L21	Dir. Agua Potable y Alcantarillado Sanitario
M21	ENTE-01
N21	SO-01-02
O21	PRESUPUESTO_GAD
A22	AH-I-X-04
B22	Modernización
C22	Modernización recursos administrativos: parque automotor, tecnología e infraestructura municipal
D22	Exclusiva_Importante
E22	1
F22	1
G22	0.5797
H22	ODS 16
I22	IN-003
J22	🔄 En seguimiento
K22	RR.HH-01
L22	Dir. Administrativa + Coord. Tecnología de la Información
M22	ENTE-01
N22	IN-02-02
O22	PRESUPUESTO_GAD
A23	PI-I-G-01
B23	Equipamientos
C23	Equipamientos públicos: terminal terrestre, mercado, estación bomberil, centro salud tipo C, espacios recreativos
D23	Exclusiva_Importante
E23	1
F23	1
G23	0.5797
H23	ODS 11
I23	SC-001
J23	🔄 En seguimiento
K23	DOP-01
L23	Dir. Obras Públicas y Fiscalización
M23	ENTE-01
N23	TE-02-01
O23	PRESUPUESTO_GAD
A24	AH-C-X-01
B24	Derechos sociales
C24	Protección derechos sociales: atenciones grupos prioritarios 943→1,649 (+15%/año); CDI; adultos mayores; violencia de género
D24	Concurrente_Crítica
E24	0.5
F24	1.15
G24	0.3333
H24	ODS 5+10
I24	SC-007
J24	🔄 En seguimiento
K24	PAT-01
L24	Patronato Municipal + MIES (convenio)
M24	ENTE-02
N24	SO-03-01
O24	PRESUPUESTO_GAD
A25	AH-C-X-02
B25	Información territorial
C25	Sistema información territorial: catastro urbano-rural 19.52%→80%; 12 procesos sistematizados; 37 trámites en línea
D25	Exclusiva_Importante
E25	1
F25	1
G25	0.5797
H25	ODS 16
I25	IN-002
J25	🔄 En seguimiento
K25	ALC-01
L25	Dir. Catastro y Gestión del Suelo
M25	ENTE-01
N25	IN-03-01
O25	PRESUPUESTO_GAD
A26	SC-I-N-03
B26	Participación
C26	Participación ciudadana: 50→100 Unidades Territoriales; 2→4 instancias efectivas (COPFP Art.115)
D26	Exclusiva_Importante
E26	1
F26	1
G26	0.5797
H26	ODS 16
I26	SC-005
J26	🔄 En seguimiento
K26	ALC-01
L26	Dir. Participación Ciudadana y Comunicación Social
M26	ENTE-01
N26	IN-04-01
O26	PRESUPUESTO_GAD
A27	FA-I-X-01
B27	Riesgo
C27	Gestión del riesgo: reducir 10% infraestructura susceptible (3,655→2,398 unidades); alerta temprana climática
D27	Exclusiva_Importante
E27	1
F27	1.15
G27	0.6667
H27	ODS 13
I27	IN-005
J27	🔄 En seguimiento
K27	BOMB-01
L27	Dir. Gestión Ambiental y Riesgos
M27	ENTE-01
N27	AM-02-01
O27	PRESUPUESTO_GAD
A28	FA-C-X-01
B28	Áreas verdes
C28	Áreas verdes y parques: IVU 10.94→17.32 m²/hab; parques inter-barriales; recuperación manglar perfil costero
D28	Exclusiva_Importante
E28	1
F28	1.15
G28	0.6667
H28	ODS 11+15
I28	SC-006
J28	🔄 En seguimiento
K28	EPAM-01
L28	Dir. Gestión Ambiental y Riesgos + EP Aseo
M28	ENTE-01
N28	AM-03-01
O28	PRESUPUESTO_GAD
A29	FA-I-X-02
B29	Equipamiento urbano
C29	Índice equipamiento urbano CUP 9.96→10.73 m²/hab; recolección desechos 91.95%→97.95%; 77.83→81.07 km/día barrido
D29	Exclusiva_Importante
E29	1
F29	1
G29	0.5797
H29	ODS 11
I29	SC-006
J29	🔄 En seguimiento
K29	EPAM-01
L29	Dir. Obras Públicas y Fiscalización + EP Aseo
M29	ENTE-01
N29	TE-02-02
O29	PRESUPUESTO_GAD
A30	FA-L-N-01
B30	Cultura
C30	Inventario patrimonial 100% al 2026; 8,000→10,000 participantes eventos culturales; Museo del Sombrero
D30	Exclusiva_Importante
E30	1
F30	1
G30	0.5797
H30	ODS 11
I30	SC-003
J30	🔄 En seguimiento
K30	ALC-01
L30	Dir. Turismo, Cultura, Patrimonio y Fomento Productivo
M30	ENTE-01
N30	SO-04-01
O30	PRESUPUESTO_GAD
A31	PI-I-G-02
B31	PDOT/PUGS
C31	Cumplimiento PDOT/PUGS 0%→80%; SIL 19.52%→80%; 37 trámites digitales implementados
D31	Exclusiva_Importante
E31	1
F31	1
G31	0.5797
H31	ODS 16
I31	IN-001
J31	🔄 En seguimiento
K31	ALC-01
L31	Dir. Planificación Estratégica e Institucional
M31	ENTE-01
N31	IN-03-02
O31	PRESUPUESTO_GAD
A32	PI-L-G-01
B32	Señalización vial
C32	Señalización vial 0→10,000 m²; 0→8 semáforos; revisiones técnicas 4,000→20,000; educación vial 40 instituciones
D32	Exclusiva_Importante
E32	1
F32	1
G32	0.5797
H32	ODS 11
I32	IN-004
J32	🔄 En seguimiento
K32	DOP-01
L32	Dir. Obras Públicas y Fiscalización
M32	ENTE-01
N32	TE-01-02
O32	PRESUPUESTO_GAD
A33	EP-L-N-01
B33	Vivienda
C33	Vivienda de interés social: 50 VIS/VIP hasta 2027; reducción déficit habitacional cualitativo
D33	Exclusiva_Importante
E33	1
F33	1
G33	0.5797
H33	ODS 11
I33	IN-001
J33	🔄 En seguimiento
K33	DOP-01
L33	Dir. Obras Públicas y Fiscalización + MIDUVI
M33	ENTE-01
N33	TE-03-01
O33	FONDO_CONCURSABLE
A34	EP-L-X-01
B34	Productivo
C34	Fortalecimiento productivo: beneficiarios artesanos, mipymes, emprendedores, huertos comunitarios y cadenas de valor
D34	Concurrente
E34	0.5
F34	1
G34	0.2899
H34	ODS 8
I34	EC-002
J34	🔄 En seguimiento
K34	ALC-01
L34	Dir. Turismo, Cultura, Patrimonio y Fomento Productivo + MinProd
M34	ENTE-01
N34	EC-01-01
O34	FONDO_CONCURSABLE
A35	PI-TUR-01
B35	Turismo certif.
C35	Turismo cantonal: establecimientos certificación Montecristi Ciudad Creativa 0→60 al 2027; visitantes eventos 2,700→4,300/año
D35	Concurrente
E35	0.5
F35	1
G35	0.2899
H35	ODS 8
I35	EC-001
J35	🔄 En seguimiento
K35	ALC-01
L35	Dir. Turismo, Cultura, Patrimonio y Fomento Productivo + MinTurismo
M35	ENTE-01
N35	EC-02-01
O35	PRESUPUESTO_GAD
A36	PI-TUR-02
B36	Turismo eventos
C36	Eventos turísticos anuales: 10 eventos/año 2023 → 22 eventos/año al 2027
D36	Concurrente
E36	0.5
F36	1
G36	0.2899
H36	ODS 8
I36	EC-001
J36	🔄 En seguimiento
K36	ALC-01
L36	Dir. Turismo, Cultura, Patrimonio y Fomento Productivo
M36	ENTE-01
N36	EC-02-02
O36	PRESUPUESTO_GAD
A37	FA-CC-01
B37	Cambio climático
C37	Cambio climático: formulación de 4 planes de acción al 2027 (0%→100%)
D37	Exclusiva_Importante
E37	1
F37	1.15
G37	0.6667
H37	ODS 13
I37	FA-I-X-01
J37	🔄 En seguimiento
K37	EPAM-01
L37	Dir. Gestión Ambiental y Riesgos
M37	ENTE-01
N37	AM-02-02
O37	FONDO_CONCURSABLE
A38	AH-AP-04
B38	Agua continuidad
C38	Continuidad servicio agua potable: índice ALTO de 0% → 10% al 2027
D38	Exclusiva_Crítica
E38	1.5
F38	1
G38	0.8696
H38	ODS 6
I38	SC-002
J38	🔄 En seguimiento
K38	DAPS-01
L38	Dir. Agua Potable y Alcantarillado Sanitario
M38	ENTE-01
N38	SO-01-03
O38	PRESUPUESTO_GAD
A39	FA-DIS-01
B39	Disposición final
C39	Disposición final desechos sólidos: capacidad operativa 0%→20% al 2027
D39	Exclusiva_Crítica
E39	1.5
F39	1.15
G39	1
H39	ODS 11+13
I39	SC-006
J39	🔄 En seguimiento
K39	EPAM-01
L39	Dir. Gestión Ambiental y Riesgos + EP Aseo
M39	ENTE-04
N39	AM-01-02
O39	FONDO_CONCURSABLE
A40	TOTALES
A42	▌ NOTA METODOLÓGICA
A43	Los valores Pi (peso financiero) NO se registran en esta hoja. Pi se calcula en H14_PONDERADORES con base en el presupuesto anual asignado por meta. | Columnas K-L (Cod_Unidad / Unidad_Responsable): provienen de Res. 040-2025 (H02b) — fuente primaria para H17_IED — no modificar sin actualizar H02b y H01!Sección I. | Columna M (ENTE_EJECUTOR): fuente del filtro H01!K3 y del motor H12d — distribución v1.0: ENTE-01×21, ENTE-02×2, ENTE-03×0, ENTE-04×2. | Columna N (ID_Meta_PDOT): codificación provisional [EJE]-[OBJ]-[META] — verificar contra PDOT oficial antes de publicar. | Columna O (TIPO_FINANCIAMIENTO): ★ ATRIBUTO DE LA META v1.0. Valores con FONDO_CONCURSABLE: EP-L-N-01, EP-L-X-01, FA-CC-01, FA-DIS-01.
```