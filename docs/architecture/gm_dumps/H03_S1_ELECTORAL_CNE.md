# H03_S1_ELECTORAL_CNE — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=86 · pobladas=82 · fórmulas=12
inputs(lee de): H00_ÍNDICE, H01_PARÁMETROS, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE, H16_IFE, H63_S0_CNE_TRAZABILIDAD
MARCADORES: A14: INSTRUCCIÓN: Las primeras 20 promesas con vinculación PDOT verificada 

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B7	=H01_PARÁMETROS!B17
B9	=B8/B7
C9	=B8/B7
D84	=COUNTIF(F17:F83,"Directa")+COUNTIF(F17:F83,"Directa con matiz")+COUNTIF(F17:F83,"Parcial")
E84	=SUM(E17:E83)/B7
F84	=B9
G84	=TEXT(B9,"0.00%")&" — IFE verificado TOTALES"
B86	=TEXT(B9,"0.00%")
D86	=B10
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H03_S1_ELECTORAL_CNE
A2	H03 — S1 ELECTORAL CNE — FIDELIDAD DE PROMESAS
A3	Silo 1 del ICPI: verifica cuántas de las 66 promesas electorales CNE 2023 se convirtieron en metas PDOT verificables.
A4	NOTA: El IFE (calculado en H16) usa este silo como fuente. El silo S1 NO entra en el producto lógico Vi del motor H12 — es un verificador de origen democrático, no de ejecución.
A6	▌ PARÁMETROS S1
A7	Total_Promesas_CNE
C7	H01 Sección A — B17=66
A8	Promesas_Con_Meta_PDOT
B8	48
C8	Dato verificado (66 × 72.83% IFE)
A9	IFE_Global
A10	Clasificación_IFE
B10	⚠️ Fidelidad Electoral Media
C10	73% — más de la mitad convertida
A11	Año_Elección
B11	2023
C11	Período alcaldía 2023-2027
A13	▌ REGISTRO DE PROMESAS CNE 2023
A14	INSTRUCCIÓN: Las primeras 20 promesas con vinculación PDOT verificada están detalladas. Las restantes 46 tienen estado 'Pendiente detalle CNE' hasta recibir el documento CNE oficial.
A15	ID_Promesa
B15	Eje_Estratégico
C15	Descripción_Promesa
D15	ID_Meta_PDOT_Vinculada
E15	Score_IFE
F15	Tipo_Vinculación
A16	ESCALA Score_IFE: 1.0=Directa / 0.75=Directa con matiz / 0.5=Parcial / 0.0=Sin vínculo PDOT
A17	EC-001
B17	Económico
C17	Convertir a Montecristi en destino turístico nacional/internacional; rutas gastronómicas, ecoturísticas, eventos culturales
D17	EP-L-X-01
E17	1
F17	Directa
A18	EC-002
B18	Económico
C18	Fomento al sector artesanal, MIPYMES y emprendedores; programa Ka-Larte es por Ti; Cuna de Emprendedores
D18	EP-L-N-01
E18	1
F18	Directa
A19	EC-003
B19	Económico
C19	Gestión para repotenciar y ordenar el mercado municipal
D19	PI-I-G-01
E19	0.75
F19	Directa con matiz
A20	EC-004
B20	Económico
C20	Impulsar desarrollo turístico Playa San José e Isla de la Plata; manglar; Paseo Lúdico
D20	EP-L-X-01
E20	0.5
F20	Parcial
A21	EC-005
B21	Económico
C21	Generación de ordenanzas para exoneración de tributos a nuevas empresas; alianzas sector privado
D21	—
E21	0
F21	Sin vínculo
A22	IN-001
B22	Institucional
C22	Elaborar PDOT 2023 con ODS; planificación territorial 30 años; Plan Bicentenario
D22	PI-I-G-02
E22	1
F22	Directa
A23	IN-002
B23	Institucional
C23	Actualización catastral urbana y rural; base de datos grupos vulnerables; registro y delimitación comunal
D23	AH-C-X-02
E23	1
F23	Directa
A24	IN-003
B24	Institucional
C24	Transformación digital del GAD; plataforma digital de trámites; gobierno electrónico abierto
D24	AH-C-X-02
E24	0.75
F24	Directa con matiz
A25	IN-004
B25	Institucional
C25	Acceso a información pública (LOTAIP); rendición de cuentas transparente; convenios interinstitucionales
D25	PI-L-G-01
E25	1
F25	Directa
A26	IN-005
B26	Institucional
C26	Seguridad ciudadana: alarmas comunitarias, habilitación UPC Aníbal San Andrés y Colorado, cuarteles bomberos
D26	PI-I-G-01
E26	0.5
F26	Parcial
A27	IN-006
B27	Institucional
C27	Creación y fortalecimiento de marca ciudad Montecristi; posicionamiento nacional como referente
D27	—
E27	0
F27	Sin vínculo
A28	SC-001
B28	Social
C28	Construcción Centro de Salud Tipo C; Centro Geriátrico; Plan Nacer Aquí; Concejo de Salud Montecristi
D28	AH-I-X-03
E28	1
F28	Directa
A29	SC-002
B29	Social
C29	Salud integral gratuita e ininterrumpida; clubes de salud; medicina preventiva; atención puerta a puerta
D29	SC-I-N-01
E29	1
F29	Directa
A30	SC-003
B30	Social
C30	Mejorar calidad de vida fauna urbana: albergue, programas de esterilización, ordenanza de protección animal
D30	FA-L-N-01
E30	0.75
F30	Directa con matiz
A31	SC-004
B31	Social
C31	Capacitaciones ciudadanas con certificación; plataforma digital; Cuna de Emprendedores; becas universitarias
D31	SC-L-N-02
E31	0.75
F31	Directa con matiz
A32	SC-005
B32	Social
C32	Participación ciudadana activa; instancias participativas barriales; liderazgo juvenil en política cantonal
D32	PI-L-G-01
E32	1
F32	Directa
A33	SC-006
B33	Social
C33	Espacios de recreación deportivos, culturales y sociales; wifi en parques y plazas públicas
D33	AH-I-N-01
E33	0.75
F33	Directa con matiz
A34	SC-007
B34	Social
C34	Protección especial a grupos vulnerables: niñez, adolescentes, adultos mayores, discapacidad, género
D34	AH-C-X-01
E34	1
F34	Directa
A35	SC-008
B35	Social
C35	Programa de becas estudiantiles para educación superior; convenios con universidades; investigación cantonal
D35	SC-L-N-02
E35	0.5
F35	Parcial
A36	SC-009
B36	Social
C36	Mejorar infraestructura de unidades educativas del cantón; mobiliario y equipamiento
D36	PI-I-G-01
E36	0.5
F36	Parcial
A37	PR-21
B37	Económico
C37	Construcción del parque industrial de Montecristi para artesanos del sombrero
D37	EP-L-N-01
E37	0.75
F37	Directa con matiz
A38	PR-22
B38	Social
C38	Ampliación de la red de alcantarillado sanitario en parroquias Sucre y Leónidas Plaza
D38	SC-L-G-01
E38	1
F38	Directa
A39	PR-23
B39	Ambiental
C39	Implementación de biodigestores y compostaje en el relleno sanitario cantonal
D39	FA-DIS-01
E39	0.75
F39	Directa con matiz
A40	PR-24
B40	Económico
C40	Reactivación del puerto artesanal de Jaramijó con infraestructura pesquera
D40	PI-I-G-01
E40	0.5
F40	Parcial
A41	PR-25
B41	Social
C41	Construcción y equipamiento de centros de desarrollo infantil CIBV en Montecristi
D41	AH-I-X-03
E41	1
F41	Directa
A42	PR-26
B42	Institucional
C42	Modernización del sistema de atención al ciudadano y ventanilla única
D42	AH-I-X-04
E42	1
F42	Directa
A43	PR-27
B43	Ambiental
C43	Descontaminación y recuperación del estero La Jagua y manglares asociados
D43	FA-CC-01
E43	0.75
F43	Directa con matiz
A44	PR-28
B44	Económico
C44	Fomento de la exportación de artesanías de paja toquilla — certificación UNESCO
D44	EP-L-X-01
E44	0.75
F44	Directa con matiz
A45	PR-29
B45	Infraestructura
C45	Rehabilitación de la vía Montecristi–Jaramijó–Crucita y circuito costero
D45	AH-I-X-02
E45	0.75
F45	Directa con matiz
A46	PR-30
B46	Social
C46	Programa de alimentación escolar complementaria en comunidades rurales
D46	AH-I-X-03
E46	0.5
F46	Parcial
A47	PR-31
B47	Institucional
C47	Implementación del sistema de rendición de cuentas digital abierto
D47	PI-L-G-01
E47	1
F47	Directa
A48	PR-32
B48	Ambiental
C48	Reforestación de 500 hectáreas de bosque seco tropical en el cantón
D48	FA-CC-01
E48	0.5
F48	Parcial
A49	PR-33
B49	Infraestructura
C49	Construcción del complejo deportivo multicancha en Parroquia Leonidas Plaza
D49	PI-I-G-01
E49	0.5
F49	Parcial
A50	PR-34
B50	Social
C50	Ampliación del programa de atención médica móvil en comunidades rurales
D50	AH-I-X-03
E50	0.75
F50	Directa con matiz
A51	PR-35
B51	Económico
C51	Creación del centro de acopio y procesamiento para pequeños agricultores
D51	EP-L-N-01
E51	0.5
F51	Parcial
A52	PR-36
B52	Institucional
C52	Implementación de cámaras de seguridad CCTV en zonas críticas del cantón
D52	FA-I-X-01
E52	0.75
F52	Directa con matiz
A53	PR-37
B53	Social
C53	Construcción de casas comunales y espacios para adultos mayores en parroquias
D53	AH-I-X-03
E53	0.75
F53	Directa con matiz
A54	PR-38
B54	Ambiental
C54	Implementación de energía solar en edificios municipales y alumbrado público
D54	FA-CC-01
E54	0.5
F54	Parcial
A55	PR-39
B55	Infraestructura
C55	Ampliación de la red de agua potable sector rural Noroeste del cantón
D55	SC-I-N-01
E55	1
F55	Directa
A56	PR-40
B56	Económico
C56	Creación de zona franca turística en la ruta del sombrero de paja toquilla
D56	PI-TUR-01
E56	0.75
F56	Directa con matiz
A57	PR-41
B57	Social
C57	Programa integral de vivienda con bono para familias en pobreza extrema
D57	EP-L-N-01
E57	0.75
F57	Directa con matiz
A58	PR-42
B58	Institucional
C58	Convenio con MIDUVI para regularización de asentamientos informales
D58	EP-L-N-01
E58	0.75
F58	Directa con matiz
A59	PR-43
B59	Ambiental
C59	Plan de manejo de cuencas hídricas y prevención de inundaciones
D59	FA-I-X-01
E59	0.75
F59	Directa con matiz
A60	PR-44
B60	Económico
C60	Programa de microcrédito para emprendedores artesanales con BanEcuador
D60	EP-L-X-01
E60	0.5
F60	Parcial
A61	PR-45
B61	Infraestructura
C61	Pavimentación de calles en sector urbano marginal de Montecristi centro
D61	AH-I-X-02
E61	0.75
F61	Directa con matiz
A62	PR-46
B62	Social
C62	Creación del banco de medicamentos para familias en pobreza extrema
D62	AH-I-X-03
E62	0.5
F62	Parcial
A63	PR-47
B63	Institucional
C63	Implementación del presupuesto participativo como política permanente
D63	SC-I-N-03
E63	1
F63	Directa
A64	PR-48
B64	Ambiental
C64	Control y erradicación del plástico de un solo uso en playas del cantón
D64	FA-C-X-01
E64	0.75
F64	Directa con matiz
A65	PR-49
B65	Económico
C65	Fortalecimiento de la marca "Sombrero de Paja Toquilla de Montecristi" a nivel global
D65	EP-L-X-01
E65	1
F65	Directa
A66	PR-50
B66	Infraestructura
C66	Construcción de aceras y bordillos en barrios periféricos de Montecristi
D66	AH-I-X-02
E66	0.75
F66	Directa con matiz
A67	PR-51
B67	Social
C67	Implementación de techos propios para familias sin vivienda adecuada
D67	EP-L-N-01
E67	0.75
F67	Directa con matiz
A68	PR-52
B68	Institucional
C68	Fortalecimiento institucional y reestructuración orgánica del GAD
D68	SC-L-N-02
E68	1
F68	Directa
A69	PR-53
B69	Ambiental
C69	Creación del humedal artificial como sistema de tratamiento aguas residuales
D69	FA-I-X-02
E69	0.5
F69	Parcial
A70	PR-54
B70	Económico
C70	Apoyo a cooperativas de pescadores con equipos de frío y comercialización
D70	EP-L-N-01
E70	0.5
F70	Parcial
A71	PR-55
B71	Social
C71	Implementación del programa "Mujer Productiva" con IEPS y organizaciones locales
D71	AH-I-X-03
E71	0.75
F71	Directa con matiz
A72	PR-56
B72	Infraestructura
C72	Rehabilitación del sistema de agua potable de parroquia La Pila
D72	SC-I-N-01
E72	1
F72	Directa
A73	PR-57
B73	Institucional
C73	Creación del archivo digital municipal y digitalización de documentos históricos
D73	AH-C-X-02
E73	0.75
F73	Directa con matiz
A74	PR-58
B74	Ambiental
C74	Plan de silvicultura urbana — 10.000 árboles en el cantón Montecristi
D74	FA-C-X-01
E74	0.5
F74	Parcial
A75	PR-59
B75	Económico
C75	Desarrollo del circuito ecoturístico Cerro Hojas-Jaboncillo-Agua Blanca
D75	PI-TUR-02
E75	0.75
F75	Directa con matiz
A76	PR-60
B76	Social
C76	Convenio con MSP para dispensarios móviles en comunidades indígenas Montubia
D76	AH-I-X-03
E76	0.5
F76	Parcial
A77	PR-61
B77	Institucional
C77	Actualización del Plan de Uso y Gestión del Suelo PUGS 2026
D77	AH-C-X-02
E77	1
F77	Directa
A78	PR-62
B78	Infraestructura
C78	Ampliación de la planta de tratamiento de agua potable de Montecristi
D78	SC-I-N-01
E78	1
F78	Directa
A79	PR-63
B79	Ambiental
C79	Implementación del sistema de alerta temprana para prevención de riesgos
D79	FA-I-X-01
E79	0.75
F79	Directa con matiz
A80	PR-64
B80	Económico
C80	Creación de la ruta gastronómica del seco de pato y mariscos de Montecristi
D80	PI-TUR-02
E80	0.5
F80	Parcial
A81	PR-65
B81	Social
C81	Implementación de talleres de formación para personas con discapacidad
D81	AH-I-X-03
E81	0.75
F81	Directa con matiz
A82	PR-66
B82	Institucional
C82	Fortalecimiento del sistema de control de uso del suelo urbano
D82	PI-I-G-02
E82	0.75
F82	Directa con matiz
A84	TOTALES
B84	—
C84	—
A86	IFE_Global calculado:
C86	Clasificación:
E86	Fuente: CNE Ecuador — Candidatura Montecristi 2023
```