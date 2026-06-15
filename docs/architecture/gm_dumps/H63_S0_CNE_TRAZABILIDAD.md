# H63_S0_CNE_TRAZABILIDAD — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=83 · pobladas=81 · fórmulas=13
inputs(lee de): H01_PARÁMETROS, H03_S1_ELECTORAL_CNE, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H85_ALERTS_LOG
refs no resueltas: #H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#H00_ÍNDICE!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B6	=H01_PARÁMETROS!B6
B8	=H01_PARÁMETROS!B11
B9	=H01_PARÁMETROS!B17
B10	=H03_S1_ELECTORAL_CNE!B8
B11	=B9-B10
B12	=H03_S1_ELECTORAL_CNE!B9
C12	=TEXT(B12,"0.00%")&" — Fuente canónica: H03_S1_ELECTORAL_CNE!B9"
E83	=SUM(E17:E82)
G83	=B10
I83	=COUNTIF(I17:I82,"✅")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H63_S0_CNE_TRAZABILIDAD
A2	H63 — SILO 0 — TRAZABILIDAD CNE: BASE DE PROMESAS ELECTORALES
A3	Base de datos canónica de las 66 promesas del Plan de Trabajo CNE 2023. Fuente primaria del IFE. INMUTABLE una vez validado con documento oficial CNE.
A5	▌ PARÁMETROS S0
A6	GAD_Nombre
A7	Año_Elección
B7	2023
C7	Fijo — ciclo político 2023-2027
A8	Candidato
A9	Total_Promesas_CNE
C9	66 promesas — sellado en H01
A10	Promesas_Con_Meta_PDOT
A11	Promesas_Sin_Meta
A12	IFE_Calculado
A13	Fuente_Documento
B13	Plan de Trabajo Candidato Jonathan Toro Largacha — CNE Ecuador 2023
A15	▌ REGISTRO CANÓNICO DE LAS 66 PROMESAS
A16	ID_Promesa
B16	Eje_Estratégico
C16	Texto_Literal_CNE
D16	Resumen_Operativo
E16	Score_IFE
F16	Tipo_Vinculación
G16	ID_Meta_PDOT_Vinculada
H16	ID_Partida_eSIGEF
I16	Validado
A17	CNE-001
B17	Eje Social
C17	Construcción y equipamiento de centros de salud en parroquias rurales
D17	Infraestructura de salud rural
E17	1
F17	Directa
G17	AH-I-X-01
H17	530201
I17	✅
A18	CNE-002
B18	Eje Social
C18	Programa de becas estudiantiles para jóvenes de escasos recursos
D18	Apoyo educativo focalizado
E18	0.75
F18	Directa
G18	SC-L-N-02
H18	530602
I18	✅
A19	CNE-003
B19	Eje Social
C19	Ampliación de cobertura de agua potable en sectores periurbanos
D19	Agua potable periurbana
E19	1
F19	Directa
G19	AH-I-X-02
H19	736101
I19	✅
A20	CNE-004
B20	Eje Social
C20	Construcción de canchas deportivas y espacios recreativos
D20	Infraestructura deportiva comunitaria
E20	0.75
F20	Directa
G20	SC-L-G-01
H20	530201
I20	✅
A21	CNE-005
B21	Eje Social
C21	Programa de atención a adultos mayores y personas con discapacidad
D21	Grupos vulnerables — atención integral
E21	1
F21	Directa
G21	AH-I-X-03
H21	730204
I21	✅
A22	CNE-006
B22	Eje Económico
C22	Fortalecimiento del mercado municipal y comercio local
D22	Economía local — mercado
E22	0.75
F22	Directa
G22	PI-I-G-01
H22	530802
I22	✅
A23	CNE-007
B23	Eje Económico
C23	Programa de emprendimiento y capacitación productiva para jóvenes
D23	Emprendimiento y capacitación
E23	0.75
F23	Directa
G23	PI-I-G-02
H23	730806
I23	✅
A24	CNE-008
B24	Eje Económico
C24	Desarrollo de infraestructura turística en playas y sitios emblemáticos
D24	Turismo — infraestructura costera
E24	1
F24	Directa
G24	PI-TUR-01
H24	530201
I24	✅
A25	CNE-009
B25	Eje Económico
C25	Apoyo a pescadores artesanales con equipos y capacitación
D25	Pesca artesanal
E25	0.75
F25	Directa
G25	PI-TUR-02
H25	730806
I25	✅
A26	CNE-010
B26	Eje Ambiental
C26	Recuperación de manglares y áreas protegidas del cantón
D26	Ecosistemas — manglares
E26	1
F26	Directa
G26	FA-I-X-01
H26	530603
I26	✅
A27	CNE-011
B27	Eje Ambiental
C27	Implementación de sistema de reciclaje y gestión de residuos sólidos
D27	Residuos sólidos — reciclaje
E27	0.75
F27	Directa
G27	FA-C-X-01
H27	530802
I27	✅
A28	CNE-012
B28	Eje Ambiental
C28	Reforestación de cuencas hídricas y quebradas del cantón
D28	Reforestación hídrica
E28	1
F28	Directa
G28	FA-I-X-02
H28	530603
I28	✅
A29	CNE-013
B29	Eje Ambiental
C29	Programa de educación ambiental en escuelas del cantón
D29	Educación ambiental
E29	0.5
F29	Parcial
G29	FA-L-N-01
H29	730806
I29	✅
A30	CNE-014
B30	Eje Político-Institucional
C30	Transparencia presupuestaria — portal ciudadano de acceso libre
D30	Portal ciudadano transparencia
E30	1
F30	Directa
G30	PI-L-G-01
H30	730201
I30	✅
A31	CNE-015
B31	Eje Político-Institucional
C31	Creación del Consejo Cantonal de Planificación Participativa
D31	Planificación participativa
E31	0.75
F31	Directa
G31	PI-L-G-01
H31	730201
I31	✅
A32	CNE-016
B32	Eje Social
C32	Mejoramiento de vías rurales e intraparroquiales
D32	Vialidad rural
E32	1
F32	Directa
G32	SC-I-N-01
H32	530201
I32	✅
A33	CNE-017
B33	Eje Social
C33	Programa de vivienda para familias en situación vulnerable
D33	Vivienda social
E33	0.5
F33	Parcial
G33	AH-I-N-01
H33	530201
I33	✅
A34	CNE-018
B34	Eje Social
C34	Centro de atención temprana para niños con necesidades educativas especiales
D34	Atención temprana NEE
E34	0.75
F34	Directa
G34	AH-C-X-01
H34	730204
I34	✅
A35	CNE-019
B35	Eje Social
C35	Programa de prevención de violencia de género y familia
D35	Violencia de género — prevención
E35	1
F35	Directa
G35	AH-C-X-02
H35	730204
I35	✅
A36	CNE-020
B36	Eje Económico
C36	Creación de zona de desarrollo económico especial en área portuaria
D36	ZDE portuaria
E36	0.5
F36	Parcial
G36	EP-L-N-01
H36	530802
I36	✅
A37	CNE-021
B37	Eje Económico
C37	Construcción de parque industrial para artesanos de sombrero de paja toquilla y reactivación económica del sector
D37	Parque industrial artesanal toquilla
E37	0.75
F37	Directa con matiz
I37	⬜
A38	CNE-022
B38	Eje Social
C38	Ampliación de red de alcantarillado sanitario en parroquias Sucre, Leónidas Plaza y sectores rurales priorizados por diagnóstico
D38	Alcantarillado parroquias rurales
E38	1
F38	Directa
I38	⬜
A39	CNE-023
B39	Eje Ambiental
C39	Implementación de biodigestores comunitarios y planta de compostaje en relleno sanitario para reducir disposición final
D39	Biodigestores y compostaje cantonal
E39	0.75
F39	Directa con matiz
I39	⬜
A40	CNE-024
B40	Eje Económico
C40	Reactivación y modernización del puerto artesanal de Jaramijó con infraestructura de refrigeración y comercialización para pescadores
D40	Puerto artesanal Jaramijó
E40	0.5
F40	Parcial
I40	⬜
A41	CNE-025
B41	Eje Social
C41	Construcción y equipamiento de Centros Infantiles del Buen Vivir CIBV en zonas rurales del cantón Montecristi
D41	CIBV rurales — infancia temprana
E41	1
F41	Directa
I41	⬜
A42	CNE-026
B42	Eje Institucional
C42	Modernización del sistema de atención al ciudadano con implementación de ventanilla única electrónica municipal
D42	Ventanilla única electrónica GAD
E42	1
F42	Directa
I42	⬜
A43	CNE-027
B43	Eje Ambiental
C43	Descontaminación y restauración ecológica del estero La Jagua y ecosistemas de manglar adyacentes
D43	Restauración estero La Jagua
E43	0.75
F43	Directa con matiz
I43	⬜
A44	CNE-028
B44	Eje Económico
C44	Fomento de exportación de artesanías de paja toquilla con sello de origen y certificación internacional UNESCO
D44	Exportación toquilla certificada UNESCO
E44	0.75
F44	Directa con matiz
I44	⬜
A45	CNE-029
B45	Eje Infraestructura
C45	Rehabilitación integral de vía Montecristi-Jaramijó-Crucita y corredor turístico costero del cantón
D45	Corredor vial costero cantonal
E45	0.75
F45	Directa con matiz
I45	⬜
A46	CNE-030
B46	Eje Social
C46	Implementación de programa de alimentación complementaria escolar en comunidades rurales con alto índice de desnutrición
D46	Nutrición escolar comunidades rurales
E46	0.5
F46	Parcial
I46	⬜
A47	CNE-031
B47	Eje Institucional
C47	Implementación de plataforma digital de rendición de cuentas en tiempo real accesible a toda la ciudadanía
D47	Rendición cuentas digital abierta
E47	1
F47	Directa
I47	⬜
A48	CNE-032
B48	Eje Ambiental
C48	Programa de reforestación masiva con especies nativas en 500 hectáreas de bosque seco tropical degradado
D48	Reforestación 500 hectáreas bosque seco
E48	0.5
F48	Parcial
I48	⬜
A49	CNE-033
B49	Eje Infraestructura
C49	Construcción del complejo deportivo multicancha techado en Parroquia Leónidas Plaza Gutiérrez
D49	Complejo deportivo Leónidas Plaza
E49	0.5
F49	Parcial
I49	⬜
A50	CNE-034
B50	Eje Social
C50	Ampliación del programa de atención médica móvil para comunidades rurales de difícil acceso del cantón
D50	Unidad móvil médica rural
E50	0.75
F50	Directa con matiz
I50	⬜
A51	CNE-035
B51	Eje Económico
C51	Creación de centro de acopio y procesamiento agroindustrial para pequeños agricultores locales
D51	Centro acopio agroindustrial
E51	0.5
F51	Parcial
I51	⬜
A52	CNE-036
B52	Eje Institucional
C52	Instalación de sistema de videovigilancia CCTV en zonas de alta incidencia delictiva del cantón
D52	CCTV seguridad ciudadana
E52	0.75
F52	Directa con matiz
I52	⬜
A53	CNE-037
B53	Eje Social
C53	Construcción de casas comunales y centros de convivencia para adultos mayores en todas las parroquias
D53	Casas comunales adultos mayores
E53	0.75
F53	Directa con matiz
I53	⬜
A54	CNE-038
B54	Eje Ambiental
C54	Implementación de paneles solares fotovoltaicos en edificios municipales para reducir huella de carbono
D54	Energía solar edificios municipales
E54	0.5
F54	Parcial
I54	⬜
A55	CNE-039
B55	Eje Infraestructura
C55	Ampliación y mejora de la red de distribución de agua potable en sectores rurales del noroeste cantonal
D55	Red agua potable rural noroeste
E55	1
F55	Directa
I55	⬜
A56	CNE-040
B56	Eje Económico
C56	Creación de zona turística especial en corredor ruta del sombrero de paja toquilla Montecristi
D56	Zona turística ruta toquilla
E56	0.75
F56	Directa con matiz
I56	⬜
A57	CNE-041
B57	Eje Social
C57	Programa integral de vivienda digna con bono de titulación para familias en situación de pobreza extrema
D57	Vivienda digna bono titulación
E57	0.75
F57	Directa con matiz
I57	⬜
A58	CNE-042
B58	Eje Institucional
C58	Suscripción de convenio con MIDUVI para regularización masiva de asentamientos informales
D58	Convenio MIDUVI regularización urbana
E58	0.75
F58	Directa con matiz
I58	⬜
A59	CNE-043
B59	Eje Ambiental
C59	Elaboración e implementación de plan de manejo de microcuencas para prevención de inundaciones y deslaves
D59	Plan manejo cuencas riesgo
E59	0.75
F59	Directa con matiz
I59	⬜
A60	CNE-044
B60	Eje Económico
C60	Programa de microcrédito productivo con BanEcuador para emprendedores artesanales de paja toquilla
D60	Microcrédito artesanos BanEcuador
E60	0.5
F60	Parcial
I60	⬜
A61	CNE-045
B61	Eje Infraestructura
C61	Pavimentación de vías en sectores urbano-marginales de Montecristi centro y cooperativas populares
D61	Pavimentación urbano-marginal Montecristi
E61	0.75
F61	Directa con matiz
I61	⬜
A62	CNE-046
B62	Eje Social
C62	Creación del banco de medicamentos genéricos para familias en extrema pobreza del cantón
D62	Banco medicamentos familias vulnerables
E62	0.5
F62	Parcial
I62	⬜
A63	CNE-047
B63	Eje Institucional
C63	Institucionalización del presupuesto participativo cantonal como mecanismo de democracia directa
D63	Presupuesto participativo cantonal
E63	1
F63	Directa
I63	⬜
A64	CNE-048
B64	Eje Ambiental
C64	Ordenanza de control y prohibición de plásticos de un solo uso en playas y áreas protegidas
D64	Ordenanza anti-plástico playas
E64	0.75
F64	Directa con matiz
I64	⬜
A65	CNE-049
B65	Eje Económico
C65	Registro internacional y fortalecimiento de marca colectiva "Montecristi Sombrero de Paja Toquilla"
D65	Marca colectiva toquilla nivel global
E65	1
F65	Directa
I65	⬜
A66	CNE-050
B66	Eje Infraestructura
C66	Construcción de aceras, bordillos y rampas de accesibilidad en barrios periféricos del cantón
D66	Aceras accesibilidad barrios periféricos
E66	0.75
F66	Directa con matiz
I66	⬜
A67	CNE-051
B67	Eje Social
C67	Programa de mejoramiento de vivienda rural "Techo Propio" para familias sin solución habitacional
D67	Techo propio vivienda rural
E67	0.75
F67	Directa con matiz
I67	⬜
A68	CNE-052
B68	Eje Institucional
C68	Restructuración orgánica del GAD Municipal adaptada a competencias COOTAD y Resolución 040-2025
D68	Reestructuración orgánica GAD
E68	1
F68	Directa
I68	⬜
A69	CNE-053
B69	Eje Ambiental
C69	Construcción de humedal artificial para tratamiento terciario de aguas residuales urbanas
D69	Humedal artificial aguas residuales
E69	0.5
F69	Parcial
I69	⬜
A70	CNE-054
B70	Eje Económico
C70	Equipamiento de cadena de frío y comercialización para cooperativas de pescadores artesanales
D70	Cadena frío pesca artesanal
E70	0.5
F70	Parcial
I70	⬜
A71	CNE-055
B71	Eje Social
C71	Implementación del programa Mujer Productiva con apoyo del IEPS y organizaciones de la economía popular
D71	Mujer productiva economía popular
E71	0.75
F71	Directa con matiz
I71	⬜
A72	CNE-056
B72	Eje Infraestructura
C72	Rehabilitación integral del sistema de agua potable de la parroquia La Pila y comunidades aledañas
D72	Agua potable La Pila rehabilitación
E72	1
F72	Directa
I72	⬜
A73	CNE-057
B73	Eje Institucional
C73	Digitalización del archivo histórico municipal y creación del repositorio documental en línea
D73	Digitalización archivo municipal
E73	0.75
F73	Directa con matiz
I73	⬜
A74	CNE-058
B74	Eje Ambiental
C74	Plan de silvicultura urbana "Montecristi Verde" — 10.000 árboles en 3 años en el cantón
D74	Silvicultura urbana 10.000 árboles
E74	0.5
F74	Parcial
I74	⬜
A75	CNE-059
B75	Eje Económico
C75	Desarrollo del circuito ecoturístico Cerro Hojas-Jaboncillo-Agua Blanca con senderos y señalética
D75	Circuito ecoturístico Cerro Hojas
E75	0.75
F75	Directa con matiz
I75	⬜
A76	CNE-060
B76	Eje Social
C76	Convenio con Ministerio de Salud para instalación de dispensarios comunitarios en comunidades Montubia
D76	Dispensarios comunitarios MSP
E76	0.5
F76	Parcial
I76	⬜
A77	CNE-061
B77	Eje Institucional
C77	Actualización participativa del Plan de Uso y Gestión del Suelo PUGS 2026-2030
D77	PUGS 2026 actualización participativa
E77	1
F77	Directa
I77	⬜
A78	CNE-062
B78	Eje Infraestructura
C78	Ampliación de capacidad de planta de tratamiento de agua potable La Sequita para demanda 2030
D78	Planta agua potable La Sequita ampliación
E78	1
F78	Directa
I78	⬜
A79	CNE-063
B79	Eje Ambiental
C79	Implementación del sistema de alerta temprana municipal para prevención de emergencias y desastres
D79	Sistema alerta temprana desastres
E79	0.75
F79	Directa con matiz
I79	⬜
A80	CNE-064
B80	Eje Económico
C80	Creación de ruta gastronómica y cultural "Sabores de Montecristi" para potenciar turismo local
D80	Ruta gastronómica Montecristi
E80	0.5
F80	Parcial
I80	⬜
A81	CNE-065
B81	Eje Social
C81	Programa de formación laboral y emprendimiento para personas con discapacidad del cantón
D81	Inclusión productiva discapacidad
E81	0.75
F81	Directa con matiz
I81	⬜
A82	CNE-066
B82	Eje Institucional
C82	Fortalecimiento del sistema de planificación territorial con actualización del mapa catastral urbano-rural
D82	Planificación territorial PDOT actualizado
E82	0.75
F82	Directa con matiz
I82	⬜
A83	TOTALES
```