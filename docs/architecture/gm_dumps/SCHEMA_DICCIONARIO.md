# SCHEMA_DICCIONARIO — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=43 · pobladas=42 · fórmulas=1
inputs(lee de): H00_ÍNDICE
outputs(alimenta a): H00_ÍNDICE
MARCADORES: E33: Coeficiente que pondera si el dato de cumplimiento fue verificado por  · E39: Datos cruzados con fuentes oficiales independientes: eSIGEF, SERCOP, L

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
```

## ETIQUETAS / DATOS (tope 600)
```
B1	★ SCHEMA_DICCIONARIO — Ontología de Gestión Pública Territorial Ecuador
C1	Terminología canónica SIAP-ICPI · COOTAD · SENPLADES · PDOT
A3	Termino_ID
B3	Termino
C3	Sigla
D3	Categoria
E3	Definicion_Corta
F3	Base_Legal_o_Fuente
G3	Sistema_PDOT
H3	Equivalente_Ciudadano
A4	DIC-001
B4	Índice de Cumplimiento de Planificación Institucional
C4	ICPI
D4	indicador_compuesto
E4	Mide el grado de cumplimiento efectivo del plan institucional ponderado por variables de gestión
F4	SIAP-ICPI v1.0 | DYLUS LAB
G4	POLÍTICO-INSTITUCIONAL
H4	¿Cuánto cumple el municipio su propio plan?
A5	DIC-002
B5	Trust Score
C5	TS
D5	indicador_trazabilidad
E5	Certifica que el cálculo del ICPI es verificable y auditado — 100 implica trazabilidad completa
F5	SIAP-ICPI v1.0
G5	POLÍTICO-INSTITUCIONAL
H5	¿Es confiable la medición?
A6	DIC-003
B6	Índice de Fidelidad Electoral
C6	IFE
D6	indicador_gestion
E6	Porcentaje de promesas de Plan de Gobierno efectivamente ejecutadas como metas PDOT
F6	SIAP-ICPI v1.0
G6	POLÍTICO-INSTITUCIONAL
H6	¿Cumplió el alcalde sus promesas?
A7	DIC-004
B7	Índice de Equidad Territorial
C7	IET
D7	indicador_gestion
E7	Mide la distribución equitativa de la inversión pública entre territorios del cantón
F7	SIAP-ICPI v1.0
G7	ASENTAMIENTOS HUMANOS
H7	¿Llega la inversión a todos los barrios?
A8	DIC-005
B8	Índice de Confianza Pública
C8	TCP
D8	indicador_gestion
E8	Agregado ponderado de percepción ciudadana de legitimidad institucional
F8	SIAP-ICPI v1.0 / PDOT
G8	POLÍTICO-INSTITUCIONAL
H8	¿Confía la ciudadanía en el municipio?
A9	DIC-006
B9	AVEP
C9	AVEP
D9	escala_calificacion
E9	Escala de semáforo: Avanzado(≥90%), Verde(≥70%), En riesgo(≥40%), Precario(≥20%), en Colapso(<20%)
F9	SIAP-ICPI v1.0
G9	POLÍTICO-INSTITUCIONAL
H9	Semáforo de desempeño 🔵🟢🟡🟠🔴
A10	DIC-007
B10	Tasa de Implementación
C10	Ti
D10	variable_motor
E10	Porcentaje del presupuesto devengado sobre el codificado vigente. Mide ejecución presupuestaria efectiva
F10	SIAP-ICPI v1.0 / SERCOP
G10	ECONÓMICO-PRODUCTIVO
H10	¿Cuánto del presupuesto realmente se gastó?
A11	DIC-008
B11	Plan de Desarrollo y Ordenamiento Territorial
C11	PDOT
D11	instrumento_planificacion
E11	Instrumento rector del desarrollo cantonal. Define diagnóstico, propuesta y modelo de gestión para el período
F11	COOTAD Art. 295 / COPLAFIP
G11	POLÍTICO-INSTITUCIONAL
H11	El plan de vida del cantón
A12	DIC-009
B12	Plan Operativo Anual
C12	POA
D12	instrumento_planificacion
E12	Detalla las actividades, recursos y metas a ejecutar en un año fiscal específico
F12	COPLAFIP Art. 77
G12	POLÍTICO-INSTITUCIONAL
H12	Lo que el municipio planea hacer este año
A13	DIC-010
B13	Plan Anual de Contratación
C13	PAC
D13	instrumento_planificacion
E13	Lista oficial de compras y contratos del Estado para el año. Publicado en SERCOP obligatoriamente
F13	LOSNCP Art. 22
G13	ECONÓMICO-PRODUCTIVO
H13	Las compras planificadas del municipio
A14	DIC-011
B14	Plan de Acción Institucional
C14	PAI
D14	instrumento_planificacion
E14	Proyectos de inversión derivados del PDOT con montos por año para cumplir las metas
F14	PDOT 2023-2027
G14	ECONÓMICO-PRODUCTIVO
H14	Los proyectos concretos del PDOT
A15	DIC-012
B15	Plan de Uso y Gestión del Suelo
C15	PUGS
D15	instrumento_planificacion
E15	Regula el uso, ocupación y aprovechamiento del suelo cantonal. Define zonas urbanas y rurales
F15	COOTAD / LOOTUGS
G15	ASENTAMIENTOS HUMANOS
H15	Cómo debe usarse el territorio
A16	DIC-013
B16	Necesidades Básicas Insatisfechas
C16	NBI
D16	indicador_social
E16	Hogares que no acceden a condiciones mínimas en: vivienda, saneamiento, educación, salud, economía
F16	INEC / SENPLADES
G16	SOCIOCULTURAL
H16	Hogares en condición de pobreza
A17	DIC-014
B17	Pobreza Multidimensional
C17	IPM
D17	indicador_social
E17	Mide privaciones en 4 dimensiones: educación, salud, trabajo y seguridad social, hábitat
F17	INEC / MIES
G17	SOCIOCULTURAL
H17	Pobreza más allá del dinero
A18	DIC-015
B18	Índice de Desarrollo Humano
C18	IDH
D18	indicador_social
E18	Mide el desarrollo humano combinando educación, salud y estándar de vida
F18	PNUD
G18	SOCIOCULTURAL
H18	¿Cuánto se desarrolla la gente?
A19	DIC-016
B19	Gobierno Autónomo Descentralizado
C19	GAD
D19	entidad
E19	Gobierno local con autonomía política, administrativa y financiera. Tipos: regional, provincial, cantonal, parroquial
F19	COOTAD Art. 28
G19	POLÍTICO-INSTITUCIONAL
H19	El municipio / la prefectura / la junta
A20	DIC-017
B20	Servicio Público de Agua Potable
C20	APAA
D20	servicio
E20	Servicio de captación, tratamiento, distribución de agua potable a la población
F20	COOTAD Art. 55 lit. d
G20	ASENTAMIENTOS HUMANOS
H20	El agua del grifo
A21	DIC-018
B21	Sistema eSIGEF
C21	eSIGEF
D21	sistema_informacion
E21	Sistema de Gestión Financiera del Estado. Registra toda la ejecución presupuestaria oficial
F21	Ministerio de Finanzas
G21	POLÍTICO-INSTITUCIONAL
H21	El sistema contable oficial del Estado
A22	DIC-019
B22	Sistema SERCOP
C22	SERCOP
D22	sistema_informacion
E22	Servicio Nacional de Contratación Pública. Portal de todas las compras del Estado
F22	LOSNCP
G22	ECONÓMICO-PRODUCTIVO
H22	Donde el Estado publica sus compras
A23	DIC-020
B23	Sistema LOTAIP
C23	LOTAIP
D23	sistema_informacion
E23	Ley Orgánica de Transparencia y Acceso a la Información Pública. Plataforma de transparencia
F23	LOTAIP
G23	POLÍTICO-INSTITUCIONAL
H23	Transparencia pública obligatoria
A24	DIC-021
B24	Código Orgánico de Organización Territorial
C24	COOTAD
D24	marco_legal
E24	Regula la organización, competencias y financiamiento de los GADs
F24	COOTAD 2010
G24	POLÍTICO-INSTITUCIONAL
H24	La ley que regula los municipios
A25	DIC-022
B25	Código Orgánico de Planificación y Finanzas Públicas
C25	COPLAFIP
D25	marco_legal
E25	Regula la planificación del desarrollo y las finanzas públicas en Ecuador
F25	COPLAFIP 2010
G25	POLÍTICO-INSTITUCIONAL
H25	La ley de planificación pública
A26	DIC-023
B26	Ley Orgánica de Ordenamiento Territorial, Uso y Gestión del Suelo
C26	LOOTUGS
D26	marco_legal
E26	Regula el ordenamiento territorial y la gestión del suelo a nivel nacional
F26	LOOTUGS 2016
G26	ASENTAMIENTOS HUMANOS
H26	La ley del uso del suelo
A27	DIC-024
B27	Centro Urbano Principal
C27	CUP
D27	clasificacion_territorial
E27	Concentración de 6 parroquias urbanas + 6 polígonos. Montecristi: 71.066 hab en 3.952 ha
F27	PDOT 2023-2027 / PUGS
G27	ASENTAMIENTOS HUMANOS
H27	La ciudad principal del cantón
A28	DIC-025
B28	Poblado Rural Mayor
C28	PRM
D28	clasificacion_territorial
E28	Asentamiento rural de entre 400 y 2.000 hab con densidad y equipamiento medio
F28	PDOT 2023-2027
G28	ASENTAMIENTOS HUMANOS
H28	Pueblo grande del campo
A29	DIC-026
B29	Asentamiento Irregular
C29	AI
D29	clasificacion_territorial
E29	Asentamiento no planificado, sin regularización de suelo, sin servicios formales
F29	PDOT 2023-2027
G29	ASENTAMIENTOS HUMANOS
H29	Barrio sin escrituras ni servicios
A30	DIC-027
B30	GeoTwin Municipal
C30	GT
D30	tecnologia
E30	Gemelo digital territorial — representación virtual del cantón con datos en tiempo real
F30	SIAP-ICPI v1.0 / DYLUS LAB
G30	POLÍTICO-INSTITUCIONAL
H30	El mapa digital vivo del cantón
A31	DIC-028
B31	Peso de Meta
C31	Pi
D31	variable_motor
E31	Factor de ponderación que refleja la importancia estratégica de cada meta dentro del sistema
F31	SIAP-ICPI v1.0
G31	POLÍTICO-INSTITUCIONAL
H31	¿Cuánto importa esta meta?
A32	DIC-029
B32	Índice de Riesgo
C32	Ri
D32	variable_motor
E32	Factor que ajusta el cumplimiento según el nivel de riesgo inherente de la meta
F32	SIAP-ICPI v1.0
G32	POLÍTICO-INSTITUCIONAL
H32	¿Qué tan difícil era cumplirla?
A33	DIC-030
B33	Factor de Verificación
C33	Vi
D33	variable_motor
E33	Coeficiente que pondera si el dato de cumplimiento fue verificado por fuente independiente
F33	SIAP-ICPI v1.0
G33	POLÍTICO-INSTITUCIONAL
H33	¿Fue verificado por fuente oficial?
A34	DIC-031
B34	Eficiencia de Ejecución
C34	Ei
D34	variable_motor
E34	Relación entre recursos utilizados y resultado obtenido
F34	SIAP-ICPI v1.0
G34	ECONÓMICO-PRODUCTIVO
H34	¿Cuánto logró con lo que gastó?
A35	DIC-032
B35	Factor Temporal
C35	Ti_var
D35	variable_motor
E35	Ajuste por el momento del ciclo en que se realiza la medición
F35	SIAP-ICPI v1.0
G35	POLÍTICO-INSTITUCIONAL
H35	¿A tiempo o con retraso?
A36	DIC-033
B36	Factor de Coherencia
C36	Ci
D36	variable_motor
E36	Mide la alineación de la meta con los objetivos estratégicos del PDOT y ODS
F36	SIAP-ICPI v1.0
G36	POLÍTICO-INSTITUCIONAL
H36	¿Va en la dirección correcta?
A37	DIC-034
B37	Objetivo de Desarrollo Sostenible
C37	ODS
D37	marco_internacional
E37	17 objetivos globales de la Agenda 2030 de la ONU. Los GADs deben alinear su PDOT a los ODS
F37	ONU / SENPLADES
G37	SOCIOCULTURAL
H37	Las metas de desarrollo del planeta
A38	DIC-035
B38	Ruta A — Gestión Declarada
C38	RUTA-A
D38	metodologia_siap
E38	Datos de cumplimiento que reporta el GAD mediante informes mensuales firmados por autoridad responsable
F38	SIAP-ICPI v1.0
G38	POLÍTICO-INSTITUCIONAL
H38	Lo que el municipio dice que cumplió
A39	DIC-036
B39	Ruta B — Gestión Verificada
C39	RUTA-B
D39	metodologia_siap
E39	Datos cruzados con fuentes oficiales independientes: eSIGEF, SERCOP, LOTAIP, MSP, Mineduc
F39	SIAP-ICPI v1.0
G39	POLÍTICO-INSTITUCIONAL
H39	Lo que las fuentes oficiales confirman
A40	DIC-037
B40	Monitor de Metas y Proyectos
C40	MPP
D40	modulo_siap
E40	Módulo de seguimiento mensual, trimestral y anual de metas PDOT y proyectos PAI
F40	SIAP-ICPI v1.0 H25-H26-H27
G40	POLÍTICO-INSTITUCIONAL
H40	El panel de control de las metas
A41	DIC-038
B41	Secretaría Nacional de Planificación
C41	SENAPLAN
D41	entidad_nacional
E41	Entidad rectora de la planificación del Estado ecuatoriano (antes SENPLADES)
F41	Decreto Ejecutivo
G41	POLÍTICO-INSTITUCIONAL
H41	La institución que regula los PDOT
A42	DIC-039
B42	Spondylus
C42	—
D42	patrimonio_cultural
E42	Molusco sagrado de las culturas precolombinas manteñas. Símbolo de la identidad territorial de Montecristi. Base narrativa de DYLUS LAB
F42	INPC / PDOT cultural
G42	SOCIOCULTURAL
H42	El símbolo de Montecristi y de DYLUS
A43	DIC-040
B43	Chaquira / Quira
C43	—
D43	patrimonio_cultural
E43	Cuenta pequeña de collar usada como unidad de intercambio por las culturas manteñas. Base narrativa de QUIRA
F43	INPC
G43	SOCIOCULTURAL
H43	La unidad de confianza pública de QUIRA
```