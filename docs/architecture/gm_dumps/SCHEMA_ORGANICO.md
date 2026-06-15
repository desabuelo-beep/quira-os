# SCHEMA_ORGANICO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=95 · pobladas=91 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	★ SCHEMA_ORGANICO — Estructura Orgánica y Competencias GAD Montecristi
C1	Fuente: COOTAD · PDOT · KB_MODELO_PROGRAMAS
A3	▌ ENTIDADES DEL SISTEMA CONSOLIDADO
A4	Entidad_ID
B4	Nombre
C4	Tipo
D4	Presupuesto_2026
E4	Ti_Q1_%
F4	Competencia_Principal
G4	Ente_Rector
H4	Pagina
A5	ENT-GAD
B5	GAD Municipal de Montecristi
C5	gobierno_autonomo
D5	45977893.81
E5	11.20
F5	Planificación, obras, servicios municipales, ordenamiento territorial
G5	Municipio
H5	H90
A6	ENT-PAT
B6	Patronato Municipal de Montecristi
C6	empresa_publica_social
D6	4341242.62
E6	19.56
F6	Servicios sociales: discapacidad, adulto mayor, género, primera infancia
G6	Patronato
H6	H90
A7	ENT-ASE
B7	EP Aseo y Espacios Públicos Montecristi
C7	empresa_publica
D7	2438254.45
E7	18.17
F7	Recolección de desechos sólidos, mantenimiento espacios públicos
G7	EP Aseo
H7	H90
A8	ENT-BOM
B8	Cuerpo de Bomberos Montecristi
C8	servicio_emergencias
D8	1485033.40
E8	19.43
F8	Prevención y control de incendios, emergencias, rescate
G8	Bomberos
H8	H90
A10	▌ COMPETENCIAS EXCLUSIVAS GAD CANTONAL (COOTAD Art. 55)
A11	Competencia_ID
B11	Competencia
C11	Base_Legal
D11	Articulo_COOTAD
E11	Sistema_PDOT
A12	COMP-001
B12	Planificación del desarrollo cantonal y ordenamiento territorial
C12	COOTAD
D12	Art. 55 lit. a
E12	ASENTAMIENTOS HUMANOS
A13	COMP-002
B13	Ejercer el control sobre el uso y ocupación del suelo
C13	COOTAD
D13	Art. 55 lit. b
E13	ASENTAMIENTOS HUMANOS
A14	COMP-003
B14	Planificar, construir y mantener la vialidad urbana
C14	COOTAD
D14	Art. 55 lit. c
E14	MOVILIDAD, ENERGÍA Y CONECTIVIDAD
A15	COMP-004
B15	Prestar servicios públicos de agua potable, alcantarillado, depuración
C15	COOTAD
D15	Art. 55 lit. d
E15	ASENTAMIENTOS HUMANOS
A16	COMP-005
B16	Crear, modificar, exonerar o suprimir tasas y contribuciones
C16	COOTAD
D16	Art. 55 lit. e
E16	ECONÓMICO-PRODUCTIVO
A17	COMP-006
B17	Planificar, regular y controlar el tránsito y transporte terrestre
C17	COOTAD
D17	Art. 55 lit. f
E17	MOVILIDAD, ENERGÍA Y CONECTIVIDAD
A18	COMP-007
B18	Planificar, construir y mantener infraestructura física y equipamientos
C18	COOTAD
D18	Art. 55 lit. g
E18	ASENTAMIENTOS HUMANOS
A19	COMP-008
B19	Preservar, mantener y difundir el patrimonio arquitectónico y natural
C19	COOTAD
D19	Art. 55 lit. h
E19	SOCIOCULTURAL
A20	COMP-009
B20	Elaborar y administrar los catastros inmobiliarios urbanos y rurales
C20	COOTAD
D20	Art. 55 lit. i
E20	POLÍTICO-INSTITUCIONAL
A21	COMP-010
B21	Delimitar, regular, autorizar y controlar el uso de playas de mar
C21	COOTAD
D21	Art. 55 lit. j
E21	FÍSICO AMBIENTAL
A22	COMP-011
B22	Preservar y garantizar el acceso efectivo de las personas al uso del espacio
C22	COOTAD
D22	Art. 55 lit. k
E22	ASENTAMIENTOS HUMANOS
A23	COMP-012
B23	Regular y controlar las construcciones en la circunscripción cantonal
C23	COOTAD
D23	Art. 55 lit. l
E23	ASENTAMIENTOS HUMANOS
A24	COMP-013
B24	Regular, prevenir y controlar la contaminación ambiental
C24	COOTAD
D24	Art. 55 lit. m
E24	FÍSICO AMBIENTAL
A25	COMP-014
B25	Gestión de la cooperación internacional para el cumplimiento del PDOT
C25	COOTAD
D25	Art. 55 lit. n
E25	POLÍTICO-INSTITUCIONAL
A27	▌ PROGRAMAS Y UNIDADES RESPONSABLES (KB_MODELO_PROGRAMAS)
A28	Prog_ID
B28	Sistema
C28	Programa
D28	Unidad_Responsable
E28	Subprogramas_Resumen
F28	N_Indicadores
G28	N_Proyectos
H28	Pagina
A29	PROG-MNT-001
B29	Sistema Físico Ambiental
C29	Áreas verdes y zonas de Protección
D29	Planificación/ Espacios públicos
E29	['Nuevos parques y zonas de protección', 'Mantenimiento de áreas verdes', 'Recup
F29	2
G29	4
H29	404
A30	PROG-MNT-002
B30	Sistema Físico Ambiental
C30	Gestión del Riesgo
D30	Planificación/ Unidad de gestión de riesgos
E30	['Infraestructura de mitigación', 'Zonas de evacuación y albergues', 'Asistencia
F30	1
G30	7
H30	405
A31	PROG-MNT-003
B31	Sistema Físico Ambiental
C31	Ambiente
D31	Dirección de Ambiente
E31	['Mitigación Ambiental']
F31	2
G31	4
H31	405
A32	PROG-MNT-004
B32	Sistema Físico Ambiental
C32	Aseo e Higiene
D32	Empresa de Aseo
E32	['Recolección de desechos', 'Tratamiento de desechos']
F32	3
G32	7
H32	406
A33	PROG-MNT-005
B33	Asentamientos Humanos
C33	Agua y saneamiento
D33	Planificación/ Dirección de agua potable, alcantarillado y saneamiento/ Proyectos Estratégicos
E33	['Agua Potable', 'Saneamiento', 'Pluvial']
F33	8
G33	7
H33	406
A34	PROG-MNT-006
B34	Asentamientos Humanos
C34	Equipamientos y espacios públicos
D34	Planificación/ Unidad de espacios públicos/ Proyectos Estratégicos
E34	['Infraestructura actual', 'Nuevos equipamientos y servicios públicos']
F34	2
G34	3
H34	407
A35	PROG-MNT-007
B35	Asentamientos Humanos
C35	Vialidad
D35	Planificación/ Obras públicas
E35	['Infraestructura vial actual', 'Ciclovías']
F35	8
G35	3
H35	408
A36	PROG-MNT-008
B36	Asentamientos Humanos
C36	Tránsito, transporte terrestre y seguridad vial
D36	Planificación/ Dirección de Tránsito, Transporte y Seguridad Vial
E36	['Seguridad vial', 'Servicios de transporte', 'Unidos por la Seguridad Vial']
F36	5
G36	3
H36	409
A37	PROG-MNT-009
B37	Asentamientos Humanos
C37	Vivienda
D37	Planificación/ Empresa de Vivienda
E37	['Proyectos habitacionales']
F37	1
G37	2
H37	409
A38	PROG-MNT-010
B38	Asentamientos Humanos
C38	Aseo e Higiene
D38	Planificación/ Empresa de Aseo
E38	['Recolección de desechos', 'Tratamiento de desechos']
F38	2
G38	2
H38	410
A39	PROG-MNT-011
B39	Sociocultural
C39	Salud Integral para la comunidad
D39	Patronato de Amparo Social
E39	['Plan de Servicios de Salud', 'Plan Salud Preventiva']
F39	2
G39	2
H39	410
A40	PROG-MNT-012
B40	Sociocultural
C40	Educa e Innova
D40	Acción Social
E40	['Plan de Acceso a la Tecnología', 'Fortalecimiento Educativo']
F40	2
G40	2
H40	411
A41	PROG-MNT-013
B41	Sociocultural
C41	Derechos en Acción
D41	Acción Social/ Patronato de Amparo Social
E41	['Protección de Derecho', 'Montecristi Solidario']
F41	4
G41	2
H41	411
A42	PROG-MNT-014
B42	Político Institucional
C42	Fortalecimiento Institucional
D42	Planificación/ Catastro/ UTICS/ Dirección Financiera/ Talento Humano/ Dirección Administrativa
E42	['Planificación Institucional', 'Planificación Territorial', 'Información y Cont
F42	8
G42	7
H42	415
A43	PROG-MNT-015
B43	Político Institucional
C43	Posicionamiento institucional y difusión
D43	Planificación/ Comunicación
E43	['Difusión Activa']
F43	3
G43	1
H43	416
A44	PROG-MNT-016
B44	Político Institucional
C44	Participación y cogestión ciudadana
D44	Planificación/ Participación ciudadana
E44	['Construcción participativa ciudadana']
F44	2
G44	1
H44	416
A46	▌ ARTICULACIONES INTERINSTITUCIONALES (KB_ARTICULACIONES)
A47	Art_ID
B47	Iniciativa
C47	Institucion
D47	Objetivo
E47	Forma_Gestion
F47	Pagina
A48	ART-MNT-001
B48	PUNTOS DIGITALES GRATUITOS PGD
C48	Ministerio de telecomunicaciones y de la Sociedad de la Información (MINTEL)
D48	Brindar atención gratuita para acceder a plataformas tecnológicas y a servicios de investigación e impresión
E48	convenio
F48	398
A49	ART-MNT-002
B49	VINCULACIÓN CON LA SOCIEDAD
C49	Instituto Superior Tecnológico Luis Arboleda Martínez
D49	Promover la transformación social, difusión y devolución de conocimientos académicos, científicos desde un enfoque de derecho, equidad y responsabilidad social.
E49	convenio
F49	398
A50	ART-MNT-003
B50	PRESTAMOS DE USO TEMPORAL
C50	Instituto Artesanal Aníbal Palacios Lucas y el MINEDUC
D50	Dar en préstamos de uso temporal para realizar cursos de carrera técnica en electricidad y mecánica para los jóvenes del cantón.
E50	convenio
F50	398
A51	ART-MNT-004
B51	PRESTACIÓN Y OCUPACIÓN DE LA SEDE
C51	Compañía de Transporte de Carga Pesada "ONCE DE MAYO" Sociedad Anónima COTRONA S.A.
D51	Prestar la sede de la Compañía para el funcionamiento del Punto Digital Gratuito Montecristi ubicado en la Comuna Cárcel Eloy Alfaro.
E51	convenio
F51	398
A52	ART-MNT-005
B52	VINCULACIÓN Y PRÁCTICAS PRE PROFESIONALES
C52	Universidad "Laica Eloy Alfaro de Manabí"
D52	Garantizar la participación efectiva en la sociedad y la responsabilidad de las instituciones del Sistema Educativo, que permitan generar incidencia local y provincial.
E52	convenio
F52	398
A53	ART-MNT-006
B53	MANTA BACHILLER
C53	Gobierno Autónomo Descentralizado Municipal del Cantón Manta
D53	Desarrollar líneas de capacitación y formación estudiantil con la finalidad de brindar habilidades cognitivas.
E53	convenio
F53	398
A54	ART-MNT-007
B54	EDUCACIÓN FINANCIERA
C54	BANECUADOR B. P
D54	Contribuir al crecimiento, posicionamiento, solvencia y gestión Social
E54	convenio
F54	398
A55	ART-MNT-008
B55	MONTECRISTI CRECE EN VALORES
C55	Fundación Plan Ecuador (Plan Internacional)
D55	Establecer acciones y relaciones en conjunto que permitan la cooperación interinstitucional entre ambas partes.
E55	convenio
F55	398
A56	ART-MNT-009
B56	Construcción del Acueducto para la captación del agua cruda para el cantón Montecristi
C56	CAF
D56	Transformar las condiciones de vida en el cantón Montecristi mediante la implementación de un sistema integral de abastecimiento de agua, asegurando un suministro continuo y de calidad.
E56	credito
F56	399
A57	ART-MNT-010
B57	Construcción de la Fase I del Sistema de Alcantarillado Sanitario de la Parroquia General Eloy Alfaro, cantón Montecristi, provincia de Manabí
C57	BEI Línea PROGAPSA (A través del BDE)
D57	Ejecutar la construcción del alcantarillado sanitario y una planta de tratamiento de aguas residuales que reduzca la contaminación del Rio Muerto de las descargas que se derivan de la parroquia General Eloy Alfaro.
E57	credito
F57	399
A58	ART-MNT-011
B58	Construcción de proyecto Ecoturístico "Manglar Vivo" en la Playa San José del cantón Montecristi, Provincia de Manabí
C58	BDE - Postulación premio verde
D58	Realizar acciones en apoyo al desarrollo sostenible del cantón, a través del proyecto se busca el mejoramiento de la infraestructura turística y ampliación de las mismas, integrando a la comunidad local generando externalidades positivas.
E58	subvencion
F58	399
A59	ART-MNT-012
B59	Construcción del Acueducto para la captación del agua cruda para el cantón Montecristi
C59	CAF
D59	Transformar las condiciones de vida en el cantón Montecristi mediante la implementación de un sistema integral de abastecimiento de agua, asegurando un suministro continuo y de calidad. Este proyecto estratégico busca mejorar la salud de los habitantes de Montecristi, impulsar el desarrollo económico y promover la recuperación y sostenibilidad ambiental, garantizando el acceso equitativo al agua potable para todos los habitantes marcando un hito histórico en el progreso del cantón.
E59	credito
F59	399
A60	ART-MNT-013
B60	Construcción de la Fase I del Sistema de Alcantarillado Sanitario de la Parroquia General Eloy Alfaro, cantón Montecristi, provincia de Manabí
C60	BEI Línea PROGAPSA (A través del BDE)
D60	Ejecutar la construcción del alcantarillado sanitario y una planta de tratamiento de aguas residuales que reduzca la contaminación del Rio Muerto de las descargas que se derivan de la parroquia General Eloy Alfaro.
E60	credito
F60	399
A61	ART-MNT-014
B61	Construcción de proyecto Ecoturístico "Manglar Vivo" en la Playa San José del cantón Montecristi, Provincia de Manabí
C61	BDE - Postulación Premio Verde
D61	Realizar acciones en apoyo al desarrollo sostenible del cantón, a través del proyecto se busca el mejoramiento de la infraestructura turística y ampliación de las mismas, integrando a la comunidad local generando externalidades positivas, entre las cuales están; las nuevas líneas de negocios y emprendimientos directos e indirectos, reconocimiento cultural y turístico resultantes del proyecto con un cambio en su giro de negocio, cuyos beneficiarios principales son las comunidades locales y la ciudadanía Montecristense.
E61	subvencion
F61	399
A62	ART-MNT-015
B62	Estudios Definitivos del Sistema de Alcantarillado para la Comuna la Sequita – Pepa de Huso del cantón Montecristi, Provincia de Manabí
C62	CELEC - Por medidas de compensación
D62	Generar la solución y propuesta actualizada de un sistema de recolección de aguas servidas y sistema de tratamiento de aguas residuales, que consiste en la propuesta planimétrica y de implementación de los componentes (pozos de descarga, colectores, redes terciarias) y planta de tratamiento que conforman el sistema integral de aguas residuales (sistema de tratamiento).
E62	subvencion
F62	400
A63	ART-MNT-016
B63	Construcción del Colector Principal y de la Planta de Tratamiento para Aguas Residuales para la Parroquia Montecristi y Aníbal San Andrés
C63	Sin postulación
D63	Implementar un sistema integral de recolección y tratamiento de aguas residuales en las parroquias de Montecristi y Aníbal San Andrés, a través de la construcción del colector principal y una planta de tratamiento de aguas residuales (Incluye Sistema Eléctrico, Conducción y Tratamiento). Este proyecto busca mejorar la calidad de vida de los habitantes, proteger el medio ambiente, y cumplir con los estándares de saneamiento y salud pública, garantizando la disposición adecuada y sostenible de las aguas residuales.
E63	otro
F63	400
A64	ART-MNT-017
B64	Construcción de la Estación Bomberil en la Parroquia Leonidas Proaño del Cantón Montecristi
C64	Sin postulación
D64	Fortalecer la capacidad de respuesta ante emergencias, garantizar la seguridad de los habitantes y proteger bienes e infraestructuras. Este proyecto busca mejorar la eficiencia y efectividad de los servicios de bomberos, reducir el tiempo de respuesta ante incendios y otros incidentes, fomentando un entorno más seguro y resiliente para la comunidad.
E64	otro
F64	400
A65	ART-MNT-018
B65	Construcción del Acueducto para la captación del agua cruda para el cantón Montecristi
C65	CAF
D65	Transformar las condiciones de vida en el cantón Montecristi mediante la implementación de un sistema integral de abastecimiento de agua, asegurando un suministro continuo y de calidad.
E65	credito
F65	402
A66	ART-MNT-019
B66	Construcción de la Fase I del Sistema de Alcantarillado Sanitario de la Parroquia General Eloy Alfaro, cantón Montecristi, provincia de Manabí
C66	BEI Línea PROGAPSA (A través del BDE)
D66	Ejecutar la construcción del alcantarillado sanitario y una planta de tratamiento de aguas residuales que reduzca la contaminación del Rio Muerto de las descargas que se derivan de la parroquia General Eloy Alfaro.
E66	credito
F66	402
A67	ART-MNT-020
B67	Construcción de proyecto Ecoturístico "Manglar Vivo" en la Playa San José del cantón Montecristi, Provincia de Manabí
C67	BDE - Postulación Premio Verde
D67	Realizar acciones en apoyo al desarrollo sostenible del cantón, a través del proyecto se busca el mejoramiento de la infraestructura turística y ampliación de las mismas, integrando a la comunidad local generando externalidades positivas.
E67	subvencion
F67	402
A68	ART-MNT-021
B68	Estudios Definitivos del Sistema de Alcantarillado para la Comuna la Sequita – Pepa de Huso del cantón Montecristi, Provincia de Manabí
C68	CELEC - Por medidas de compensación
D68	Generar la solución y propuesta actualizada de un sistema de recolección de aguas servidas y sistema de tratamiento de aguas residuales.
E68	subvencion
F68	403
A69	ART-MNT-022
B69	Construcción del Colector Principal y de la Planta de Tratamiento para Aguas Residuales para la Parroquia Montecristi y Aníbal San Andrés
C69	Sin postulación
D69	Implementar un sistema integral de recolección y tratamiento de aguas residuales en las parroquias de Montecristi y Aníbal San Andrés.
E69	otro
F69	403
A70	ART-MNT-023
B70	Construcción de la Estación Bomberil en la Parroquia Leonidas Proaño del Cantón Montecristi
C70	Sin postulación
D70	Fortalecer la capacidad de respuesta ante emergencias, garantizar la seguridad de los habitantes y proteger bienes e infraestructuras.
E70	otro
F70	403
A71	ART-MNT-024
B71	Estudios Definitivos del Sistema de Alcantarillado para la Comuna la Sequita – Pepa de Huso del cantón Montecristi, Provincia de Manabí
C71	CELEC
D71	Generar la solución y propuesta actualizada de un sistema de recolección de aguas servidas y sistema de tratamiento de aguas residuales, que consiste en la propuesta planimétrica y de implementación de los componentes (pozos de descarga, colectores, redes terciarias) y planta de tratamiento que conforman el sistema integral de aguas residuales (sistema de tratamiento).
E71	subvencion
F71	403
A72	ART-MNT-025
B72	Construcción del Colector Principal y de la Planta de Tratamiento para Aguas Residuales para la Parroquia Montecristi y Aníbal San Andrés
C72	Sin postulación
D72	Implementar un sistema integral de recolección y tratamiento de aguas residuales en las parroquias de Montecristi y Aníbal San Andrés, a través de la construcción del colector principal y una planta de tratamiento de aguas residuales (Incluye Sistema Eléctrico, Conducción y Tratamiento).
E72	otro
F72	403
A73	ART-MNT-026
B73	Construcción de la Estación Bomberil en la Parroquia Leonidas Proaño del Cantón Montecristi.
C73	Sin postulación
D73	Fortalecer la capacidad de respuesta ante emergencias, garantizar la seguridad de los habitantes y proteger bienes e infraestructuras.
E73	otro
F73	403
A74	ART-MNT-027
B74	Convenio con Fundación Adelanto Comunitario Ecuatoriano (FASE) para procesos complementarios de desarrollo comunitario, salud, educación y discapacidad bajo el principio de la Misión Integral
C74	Fundación Adelanto Comunitario Ecuatoriano (FASE)
D74	Desarrollar procesos complementarios de apoyo en erradicación de violencia intrafamiliar y de género, desarrollo comunitario, salud, educación y discapacidad
E74	convenio
F74	418
A75	ART-MNT-028
B75	Programa Alas de Libertad - Prevención e Intervención de Violencia Intrafamiliar y conformación del Centro de Prevención, Intervención y Empoderamiento de Abuso y Violencia
C75	Alas de Libertad
D75	Prevenir e intervenir en casos de Violencia Intrafamiliar y de género mediante jornadas en unidades educativas y grupos dirigentes comunitarios
E75	alianza
F75	418
A76	ART-MNT-029
B76	Articulación con Junta y Consejo Cantonal de Protección de Derechos para atención integral y acceso a servicios sociales de grupos de atención prioritaria
C76	Junta y Consejo Cantonal de Protección de Derechos
D76	Apoyar la atención integral y acceso a los servicios sociales con énfasis en grupos de atención prioritaria, promoviendo mejoramiento de condiciones de vida y protección de derechos ciudadanos
E76	alianza
F76	418
A77	ART-MNT-030
B77	Plan International a través del GAD del cantón Montecristi llega a 18 comunidades para fortalecimiento de niñas, niños, adolescentes y jóvenes e Implementación de Escuela de Liderazgo
C77	Plan International
D77	Fortalecer capacidades de niñas, adolescentes y jóvenes para toma de decisiones sobre derechos sexuales y reproductivos, emprendimiento y liderazgo
E77	alianza
F77	419
A78	ART-MNT-031
B78	Gestión de líneas de financiamiento directo para planes, programas y proyectos de género
C78	Cooperación internacional
D78	Alcanzar el desarrollo sostenible con igualdad y autonomía de las mujeres, implementando acciones y estrategias para transformar sus vidas
E78	credito
F78	417
A79	ART-MNT-032
B79	Gestión de líneas de financiamiento directo para planes, programas y proyectos para prevención y atención de problemáticas de niños, niñas, adolescentes, jóvenes y personas adultas mayores
C79	Cooperación internacional
D79	Garantizar el cumplimiento de los derechos de los grupos generacionales con énfasis en la prevención y atención en casos de vulneración de derechos
E79	credito
F79	419
A80	ART-MNT-033
B80	Gestión de cooperación internacional para derechos de grupos generacionales
C80	Plan Internacional / GAD Montecristi
D80	Gestionar líneas de financiamiento directo para la ejecución de planes, programas y proyectos para la prevención y atención de problemáticas de niños, niñas, adolescentes, jóvenes y personas adultas mayores
E80	convenio
F80	419
A81	ART-MNT-034
B81	Planificación del desarrollo cantonal con enfoque intergeneracional
C81	GAD Montecristi
D81	Asegurar la participación de los consejos consultivos y organizaciones de niñas y niños, adolescentes, jóvenes y personas adultas mayores en los procesos de decisión y planificación del desarrollo local
E81	otro
F81	419
A82	ART-MNT-035
B82	Gestión de cooperación internacional para personas con discapacidad
C82	GAD Montecristi / Organismos de cooperación internacional
D82	Fortalecer la gestión de los GAD para mejorar el trabajo con los grupos de atención prioritaria e incorporar los enfoques de igualdad en la intervención de los GAD (PDOT)
E82	convenio
F82	420
A83	ART-MNT-036
B83	Planificación del desarrollo cantonal con enfoque de discapacidades
C83	GAD Montecristi
D83	Promover la participación de las personas con discapacidad en la elaboración, ejecución, seguimiento y evaluación del PDOT
E83	otro
F83	420
A84	ART-MNT-037
B84	Capacitaciones en Derechos Humanos para personas con discapacidad
C84	Fundación Rayito de Esperanza / CONADIS
D84	Capacitaciones en temas de Derechos Humanos para personas con discapacidad
E84	alianza
F84	421
A85	ART-MNT-038
B85	Gestión de cooperación internacional para movilidad humana
C85	GAD Montecristi / ONG internacionales
D85	Gestionar asistencia financiera y técnica para el proceso de formulación de políticas públicas locales en temas de movilidad humana; establecer acuerdos de cooperación fronteriza para garantizar una migración segura y ordenada
E85	convenio
F85	421
A86	ART-MNT-039
B86	Planificación del desarrollo cantonal con enfoque de movilidad humana
C86	GAD Montecristi
D86	Sensibilizar y fortalecer la capacitación a los servidores públicos sobre normativa vigente en movilidad humana e incluir en los procesos de formación a inmigrantes para fomentar la corresponsabilidad
E86	otro
F86	421
A87	ART-MNT-040
B87	Movilidad Humana, Protección Integral y Principios / Apoyo en construcción de espacios públicos
C87	ACNUR / ONG AVSI / FUNDER
D87	Atención a movilidad humana, protección integral y apoyo en la construcción de espacios públicos y equipamientos sociales
E87	alianza
F87	422
A88	ART-MNT-041
B88	Monitoreo de prevención y erradicación del trabajo infantil / Protección de infancia en movilidad humana
C88	MIES / DINAPEN / COOPI / MINEDUC
D88	Monitoreo de prevención y erradicación del trabajo infantil, lineamientos para la protección de la infancia en movilidad humana e inclusión al sistema educativo a niños migrantes
E88	alianza
F88	422
A89	ART-MNT-042
B89	Feria de servicios proyecto SCALE para jóvenes en movilidad humana
C89	Consejo Noruego para Refugiados
D89	Fortalecer habilidades en empleabilidad y emprendimiento de jóvenes entre 16 a 28 años
E89	alianza
F89	422
A90	ART-MNT-043
B90	Visitas domiciliarias a refugiados y cumplimiento de compromisos mesa técnica de Movilidad Humana
C90	HIAS / Fundación Colón Muñoz
D90	Cumplimiento a compromisos de la mesa técnica de Movilidad Humana y visitas domiciliarias a refugiados
E90	alianza
F90	422
A91	ART-MNT-044
B91	Asistencia técnica a personas en situación de movilidad humana
C91	Fundación Género
D91	Brindar asistencia técnica a las personas en situación de movilidad humana
E91	alianza
F91	422
A92	ART-MNT-045
B92	Conformar El Sistema Cantonal de Gestión de Riesgos – SCGR / Comité de Operaciones de Emergencia Municipal (COE-M)
C92	Secretaría de Gestión de Riesgos (SGR)
D92	Promover, planear y mantener la coordinación y operación conjunta en emergencias o desastres a nivel municipal; validación y registro del COE-M
E92	alianza
F92	423
A93	ART-MNT-046
B93	Regular la Gestión del Riesgo de Desastres – Ordenanza Unidad de Gestión de Riesgos
C93	Secretaría de Gestión de Riesgos (SGR)
D93	Emitir el Reglamento de la Ley Orgánica para la Gestión Integral del Riesgo de Desastres y normar procesos de planificación, organización y articulación de políticas ante emergencias y desastres
E93	otro
F93	424
A94	ART-MNT-047
B94	Coordinación con Dependencias Municipales – Plan de Acción de riesgo de amenazas
C94	Dependencias del GADM del cantón Montecristi
D94	Coordinar acciones de las dependencias municipales como parte del Plan de Acción frente al riesgo de amenazas
E94	alianza
F94	425
A95	ART-MNT-048
B95	Adopción de medidas frente al cambio climático / Plan Nacional de Adaptación al Cambio Climático 2023-2027
C95	Coordinación Zonal 4 de la Secretaría de Gestión de Riesgos
D95	Registrar eventos de desastres naturales y antrópicos y articular acciones de adaptación y mitigación del cambio climático en el cantón Montecristi
E95	alianza
F95	427
```