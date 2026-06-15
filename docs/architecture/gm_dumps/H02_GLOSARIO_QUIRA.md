# H02_GLOSARIO_QUIRA — volcado determinista (fórmulas + etiquetas)
fuente: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx` · filas=96 · pobladas=94 · fórmulas=5
inputs(lee de): H00_ÍNDICE, H12_MOTOR_ICPI_CANÓNICO
outputs(alimenta a): H00_ÍNDICE
MARCADORES: B9: Diferencia entre el ICPI verificado algorítmicamente (69.93%) y el ICM · B26: Hoja H01_PARÁMETROS. Fuente única de verdad del ecosistema. Todas las  · B42: Índice de Pertinencia Estratégica. Mide qué fracción del gasto de inve

## FÓRMULAS
```
A1	=HYPERLINK("#'H00_ÍNDICE'!A1","⬅️ ÍNDICE GENERAL")
E1	="ICPI 2026: "&ROUND(H12_MOTOR_ICPI_CANÓNICO!B33,2)&"% ★"
F1	=TODAY()
B96	=TODAY()
C96	=COUNTA(A7:A200)&" términos registrados"
```

## ETIQUETAS / DATOS (tope 600)
```
B1	🏛️ QUIRA Gov · Powered by Dylus Lab · TGI Engine
D1	H02_GLOSARIO_QUIRA
A2	H02 — GLOSARIO TÉCNICO SIAP-ICPI v1.0
A3	Diccionario oficial de términos. Toda duda terminológica se resuelve aquí. Lenguaje 100% preventivo y de gestión.
A5	▌ GLOSARIO ALFABÉTICO
A6	Término
B6	Definición
C6	Referencia Legal / Metodológica
A7	AVEP
B7	Escala de 5 niveles: Ruptura Sistémica (0-19%) / Gestión por Ocurrencia (20-39%) / Transición Crítica (40-69%) / Gestión por Mandato (70-89%) / Excelencia en Gobernanza (90-100%). Clasifica el ICPI global y por meta.
C7	SIAP-ICPI Metodología v1.0
A8	Axioma de Invarianza Computacional
B8	Principio que establece la INMUTABILIDAD DE LA FÓRMULA CANÓNICA del ICPI: ICPI = Σ(Pi·Ri·Vi·Ei·Ti·Ci) / Σ(Pi·Ri) × 100, implementada en H12!B33 = B31/B32*100. EL AXIOMA ES LA FÓRMULA — su lógica matemática y metodológica es invariante. Los resultados numéricos (ej. ICPI_Real_2025 = 69.9309%) son consecuencia de los datos ingresados en cada período, NO el axioma en sí. Fuente: H12_MOTOR_ICPI_CANÓNICO (hoja inmutable).
C8	SIAP-ICPI Metodología v1.0
A9	Brecha ICPI-SIGAD
B9	Diferencia entre el ICPI verificado algorítmicamente (69.93%) y el ICM autoreportado al SNP (100%). La brecha revela el margen de mejora entre narrativa oficial y verificación independiente.
C9	H15_ICPI_GLOBAL — Señal de Divergencia
A10	Ci (Calidad de proceso)
B10	Variable que mide la calidad institucional del proceso orgánico responsable de una meta. ★ DETERMINISTA v1.0: Ci = MAX(1.00 - Σ deducciones normativas, 0). El proceso nace con Ci=1.00 (presunción de legalidad). Las infracciones CGE/SERCOP/COPFP/CPCCS deducen puntos. Fuente: H01 Sección L. Marco legal: LOSNCP + COPFP + CGE + CPCCS (NO LOSEP — LOSEP evalúa personas, SIAP-ICPI evalúa procesos de inversión).
C10	SIAP-ICPI Metodología v1.0 — DECISIÓN Javo Delgado Santana, 27-Abr-2026
A11	Ci_Adaptativo
B11	Versión calculada del Ci que incorpora modificadores según TIPO_FINANCIAMIENTO e INTANGIBLE_FLAG. Fórmula: Ci_adaptativo = MIN(Ci_base × Modificador, 1.0). El Ci_base siempre viene de H01 Sección I. Calculado en H12.
C11	H12_MOTOR_ICPI_CANÓNICO — columna Ci_Calc
A12	Ci_Determinista
B12	Algoritmo que calcula Ci a partir de infracciones normativas reales documentadas. Fórmula: Ci = MAX(1.00 - (CGE_Obs × 0.10) - (SERCOP_Alert × 0.15) - (POA_Retraso × 0.20) - (CPCCS_Desacato × 0.50), 0). Garantiza objetividad, auditabilidad y reproducibilidad. Fuente de datos: Sección L de H01.
C12	LOSNCP Art.17 / COPFP Art.9 / Ley Orgánica CGE / Ley CPCCS
A13	CLASE_PRODUCTO
B13	Taxonomía del producto de cada META. Valores: OBRA / BIEN / SERVICIO / NORMATIVO. ★ ATRIBUTO DE LA META (v1.0): se ingresa en H13_VARIABLES_Vi por meta — NO en H02b. Una misma dirección puede producir OBRAS en una meta y SERVICIOS en otra.
C13	H13_VARIABLES_Vi — Res. 040-2025
A14	COOTAD
B14	Código Orgánico de Organización Territorial, Autonomía y Descentralización. Marco legal principal de los GADs municipales.
C14	R.O. 303 de 19-oct-2010 y reformas
A15	COPFP
B15	Código Orgánico de Planificación y Finanzas Públicas. Regula la planificación territorial y presupuesto público.
C15	R.O. 306 de 22-oct-2010
A16	Devengado
B16	Valor presupuestario reconocido como obligación pagada o en proceso de pago. Es el denominador real de la ejecución financiera.
C16	Acuerdo Ministerial MEF 067
A17	EAS (Ecosistema Algorítmico de Supervisión)
B17	Sistema SIAP-ICPI compuesto por ICPI + 9 índices complementarios + 7 señales SAT + tableros AVEP. Opera como supervisor algorítmico preventivo de la gestión municipal.
C17	SIAP-ICPI Metodología v1.0
A18	Ei (Autonomía orgánica)
B18	Variable que mide el grado de autonomía con que el GAD ejerce una competencia. Escala: 1.0=autónomo / 0.9=compartido / 0.75=difuso o ambiguo.
C18	SIAP-ICPI Metodología v1.0
A19	eSIGEF
B19	Sistema Integrado de Gestión Financiera del Estado. Fuente oficial de datos de ejecución presupuestaria del MEF.
C19	Acuerdo MEF 067
A20	Fidelidad Alta
B20	Categoría del Índice de Fidelidad Narrativa (MFN) cuando IF_n ≥ 0.85. Indica que la narrativa oficial coincide con la evidencia documental verificada.
C20	H34b_MFN — escala IF_n
A21	Fidelidad Baja
B21	Categoría MFN cuando IF_n < 0.60. La narrativa no tiene respaldo documental suficiente. Requiere triangulación adicional.
C21	H34b_MFN — escala IF_n
A22	Fidelidad Media
B22	Categoría MFN cuando 0.60 ≤ IF_n < 0.85. La narrativa es parcialmente verificable.
C22	H34b_MFN — escala IF_n
A23	FONDO_CONCURSABLE
B23	Tipo de financiamiento de fondos externos no reembolsables obtenidos por concurso competitivo. Su captura exitosa activa discriminación positiva en Ci (×1.15). No impacta presupuesto propio del GAD.
C23	H07c — TIPO_FINANCIAMIENTO
A24	Gold Master
B24	Primera versión publicable del ecosistema SIAP-ICPI. Excel construido desde cero con arquitectura limpia, lenguaje preventivo, Ci por Estatuto Orgánico, y datos históricos verificados 2023-2025.
C24	SIAP-ICPI v1.0
A25	Grupos 7+8
B25	Grupos presupuestarios de inversión en el clasificador eSIGEF: Grupo 7 (Bienes de Larga Duración) y Grupo 8 (Obras). Son la base del cálculo del Ti canónico.
C25	Clasificador presupuestario MEF
A26	H01
B26	Hoja H01_PARÁMETROS. Fuente única de verdad del ecosistema. Todas las hojas leen configuración de aquí. Cero valores hardcodeados en otras hojas.
C26	SIAP-ICPI v1.0
A27	H02b
B27	Hoja H02b_ORGÁNICO_CLASIFICADOR. ADN institucional del sistema SIAP-ICPI. Contiene la clasificación de 20 unidades del GAD por TIPO_PROCESO, ROL_INSTITUCIONAL y EVIDENCIA_PREDOMINANTE. ★ ARQUITECTURA v1.0: clasifica UNIDADES ORGÁNICAS. CLASE_PRODUCTO, INTANGIBLE_FLAG y TIPO_FINANCIAMIENTO son atributos de METAS ESPECÍFICAS — están en H13 y H04.
C27	Estatuto Orgánico GAD Montecristi 2025 — Decisión Javo Delgado Santana, 27-Abr-2026
A28	H07c
B28	Hoja H07c_Ti_VERIFICADO_INFORME. Silo de evidencia verificada no-eSIGEF. Registra informes firmados con hash SHA-256 para metas intangibles y fondos concursables. Activa la lógica Ti_V en H12.
C28	SIAP-ICPI v1.0
A29	H12
B29	Hoja H12_MOTOR_ICPI_CANÓNICO. Fuente única del ICPI. Ninguna otra hoja recalcula el ICPI — solo referencian H12!B33.
C29	SIAP-ICPI v1.0
A30	H36b
B30	Hoja H36b_LOOKUP_ARRASTRE. Registro histórico inmutable de todos los ARRASTREs 2023-2025 de las 4 entidades del ecosistema.
C30	SIAP-ICPI v1.0
A31	Hash SHA-256
B31	Función criptográfica de 256 bits que genera una huella digital única de un PDF firmado electrónicamente. Su presencia en H07c valida la autenticidad del informe de ejecución. Condición requerida para usar Ti_V.
C31	H07c_Ti_VERIFICADO_INFORME
A32	ICM
B32	Índice de Cumplimiento de Metas. Indicador oficial autoreportado al SNP/SIGAD por el GAD. Diferente del ICPI: no incorpora verificación algorítmica de los 8 silos. Valor 2025: 100% (autoreporte).
C32	SNP / SIGAD — reporte oficial
A33	ICODS
B33	Índice de Cumplimiento de ODS. Mide el grado en que las metas del PDOT están alineadas con la Agenda 2030.
C33	H20_ICODS
A34	ICPI
B34	Índice de Cumplimiento de Procesos de Integridad. Fórmula: ICPI = [Σ(Pi×Ri×Vi×Ei×Ti×Ci) / Σ(Pi×Ri)] × 100. Valor canónico 2025: 69.9309%. Fuente única: H12!B33.
C34	SIAP-ICPI Metodología v1.0
A35	IED
B35	Índice de Eficiencia por Dirección. Mide la ejecución de metas PDOT desglosada por dirección municipal del Estatuto Orgánico. Valor 2025: 70.33%.
C35	H17_IED
A36	IEF
B36	Índice de Eficiencia Financiera. Mide la capacidad del GAD de capturar fondos externos. IEF = Σ(Fondos_Externos_Captados) / Presupuesto_Codificado_Total. Escala: ≥20% Alta capacidad / 10-19% Buena gestión / 5-9% Moderada / <5% Oportunidad.
C36	H20c_IEF_EFICIENCIA_FINANCIERA
A37	IET
B37	Índice de Equidad Territorial. Mide la distribución geográfica de la inversión entre zonas urbanas y rurales del cantón. Valor 2025: 91.42%.
C37	H42_IET_EQUIDAD_TERRITORIAL
A38	IFE
B38	Índice de Fidelidad Electoral. Mide qué porcentaje de las 66 promesas CNE se convirtió en metas PDOT. Valor 2025: 72.83%.
C38	H16_IFE
A39	IGP
B39	Índice de Gobernanza Participativa. Mide la calidad de los procesos de rendición de cuentas y participación ciudadana. Valor 2025: 27.98%.
C39	H20b_IGP_GOBERNANZA_PARTIC
A40	INTANGIBLE_FLAG
B40	Indicador booleano (VERDADERO/FALSO) que señala si una META específica produce un resultado intangible (psicología, trabajo social, capacitación, normativa) sin evidencia eSIGEF directa. Activa la lógica Ti_V en H12. ★ ATRIBUTO DE LA META (v1.0): se ingresa en H13_VARIABLES_Vi por meta — NO en H02b. La misma dirección puede tener metas tangibles e intangibles simultáneamente.
C40	H13_VARIABLES_Vi
A41	IOC
B41	Índice de Opacidad Crítica. Mide el porcentaje de información pública con acceso restringido o no publicada según LOTAIP. Valor 2025: 17.71%.
C41	H41_IOC_OPACIDAD_CRITICA
A42	IPE
B42	Índice de Pertinencia Estratégica. Mide qué fracción del gasto de inversión está vinculada a metas PDOT. Valor 2025: 0.00% (POA verificable no disponible).
C42	H16b_IPE
A43	ISP
B43	Índice de Salud Presupuestaria. Mide la coherencia entre presupuesto codificado, devengado y metas programadas. Valor 2025: 58.40%.
C43	H19_ICS_ISP
A44	ITAM
B44	Índice de Transparencia Algorítmica Municipal. Mide el grado de cumplimiento de obligaciones de transparencia (LOTAIP Art.7). Valor 2025: 56.00%.
C44	H18_ITAM
A45	LOSNCP
B45	Ley Orgánica del Sistema Nacional de Contratación Pública. Regula los procesos de contratación pública en Ecuador.
C45	R.O. 395 de 4-ago-2008
A46	LOTAIP
B46	Ley Orgánica de Transparencia y Acceso a la Información Pública. Obliga a publicar información en sitios web institucionales.
C46	R.O. 337 de 18-may-2004
A47	Mapeo Retrospectivo
B47	Técnica de reverse engineering que inyecta los valores históricos 2025 de infracciones normativas en H01 Sección L para que el algoritmo Ci reproduzca exactamente el ICPI canónico 69.9309%. Distribución 2025: 11 metas Ci=1.00 / 9 metas Ci=0.90 / 5 metas Ci=0.75. En 2026, los valores reales sustituyen el mapeo.
C47	SIAP-ICPI Metodología v1.0 — Fórmula Canónica (Axioma de Invarianza)
A48	MFN
B48	Matriz de Fidelidad Narrativa. Instrumento que triangula las afirmaciones oficiales de rendición de cuentas con la evidencia documental verificable. Escala: Fidelidad Alta (≥0.85) / Fidelidad Media (≥0.60) / Fidelidad Baja (<0.60).
C48	H34b_MFN_FIDELIDAD_NARRATIVA
A49	MMP
B49	Monitor de Monitoreo de Progreso. Sistema de seguimiento mensual/trimestral/anual del avance de metas.
C49	H25, H26, H27
A50	MPE
B50	Modelo de Probabilidad de Ejecución. Modelo proxy que estima Ti inversión cuando no se dispone de cédula eSIGEF real. Rangos por sector: Infraestructura 0.65-0.75 / Social 0.92-0.98 / Bienes 0.78-0.82 / Ambiental 0.68-0.78 / Bomberil 0.60-0.70.
C50	H36b Sección MPE
A51	PAC
B51	Plan Anual de Contratación. Instrumento que programa todas las adquisiciones de un ente público para el año fiscal.
C51	LOSNCP Art.22
A52	PDOT
B52	Plan de Desarrollo y Ordenamiento Territorial. Documento rector de la planificación cantonal 2023-2027. Contiene 25 metas verificadas.
C52	COPFP Art.41-43
A53	Pi (Peso financiero)
B53	Variable que pondera cada meta según su participación en el presupuesto anual del PDOT. La suma de todos los Pi debe ser exactamente 1.0000.
C53	H14_PONDERADORES
A54	POA
B54	Plan Operativo Anual. Instrumento de planificación operativa que desglosa las metas PDOT en actividades con cronograma y presupuesto mensual.
C54	COPFP Art.9
A55	PSG
B55	Presupuesto Sensible al Género. Mide la proporción del presupuesto destinado a metas con equidad de género. PSG_Fidelidad (86.75%) ≠ PSG_Ejecución (2.80%). El dashboard muestra PSG_Ejecución.
C55	H16c_PSG_PRESUPUESTO_GENERO
A56	Ri (Relevancia competencial)
B56	Variable que pondera la relevancia de una competencia: Exclusiva Crítica (1.5) / Exclusiva Importante (1.0) / Complementaria (0.5). Incorpora bonos ODS 5 y ODS 13 (×1.15).
C56	H14_PONDERADORES
A57	SAT
B57	Sistema de Atención Temprana. Conjunto de 7 señales preventivas que detectan riesgos de gestión antes de que se materialicen. SAT-0 a SAT-VI activos en v1.0.
C57	H21b-H24c
A58	SAT-0
B58	Señal de Coherencia PAC: detecta brechas entre programación POA y contratación PAC superiores al 20%. Incluye alerta de downcoding.
C58	H21b_SAT-0_COHERENCIA_PAC
A59	SAT-I
B59	Señal de Fragmentación Selectiva: detecta alta calificación SIGAD con cobertura parcial de metas.
C59	H21_SAT-I
A60	SAT-II
B60	Señal de Reforma Tardía: detecta reformas presupuestarias superiores al 5% del total.
C60	H22_SAT-II
A61	SAT-III
B61	Señal de Parálisis Presupuestaria: detecta metas con devengado inferior al 10% del codificado.
C61	H23_SAT-III
A62	SAT-IV
B62	Señal de Alerta Fiscal COOTAD: activa si el gasto corriente supera el 35% o la inversión baja del 65%.
C62	H24_SAT-IV
A63	SAT-V
B63	Señal de Alerta de Brecha CPCCS: detecta diferencias entre compromisos CPCCS y ejecución real.
C63	H24b_SAT-V_ALERTA_CPCCS
A64	SAT-VI
B64	Señal de Desvío de Presupuesto Participativo: detecta uso de fondos PP en fines distintos a los aprobados.
C64	H24c_SAT-VI_DESVÍO_PP
A65	SERCOP
B65	Servicio Nacional de Contratación Pública. Portal oficial de transparencia de compras públicas.
C65	LOSNCP / portal sercop.gob.ec
A66	SIAP
B66	Sistema de Integridad Algorítmica Preventiva. Nombre completo del ecosistema SIAP-ICPI.
C66	SIAP-ICPI v1.0
A67	SIGAD
B67	Sistema de Información para los Gobiernos Autónomos Descentralizados. Sistema oficial del SNP para reporte de cumplimiento de metas.
C67	SNP / Secretaría Nacional de Planificación
A68	SNP
B68	Secretaría Nacional de Planificación. Institución rectora de la planificación nacional. NOTA: NO usar 'SENPLADES' — fue suprimida en 2019.
C68	Decreto Ejecutivo 732 (2019)
A69	SUPERSEDED
B69	Estado de un registro ARRASTRE que ha sido reemplazado por datos más recientes o de mejor calidad. Los registros SUPERSEDED se mantienen para auditoría histórica.
C69	H36b_LOOKUP_ARRASTRE §Estado
A70	TAC
B70	Tablero de Accountability Ciudadana. Dashboard diseñado para SIAP-ICPI Ciudadana — interfaz pública de consulta de la gestión del GAD.
C70	H33_TAC_QUIRA_CIUDADANA
A71	QUIRA
B71	Sistema de Integridad Algorítmica Preventiva (SIAP-ICPI). Plataforma desarrollada por DYLUS LAB para monitoreo preventivo de la gestión de los GADs.
C71	DYLUS LAB © 2026
A72	QUIRA Ciudadana
B72	Módulo de SIAP-ICPI orientado a la ciudadanía para consulta pública de indicadores de gestión.
C72	H33_TAC + SIAP-ICPI Institucional
A73	SIAP-ICPI Institucional
B73	Módulo de SIAP-ICPI orientado a las autoridades municipales para gestión interna. Incluye todas las 62 hojas del Gold Master.
C73	SIAP-ICPI v1.0
A74	Ti (Ejecución de inversión)
B74	Variable que mide la ejecución financiera de inversión. Fórmula: Ti = Devengado_Grupos_7+8 / Codificado_Grupos_7+8. Solo Grupos 7 y 8. Jerarquía adaptativa: 1-eSIGEF → 2-Ti_V → 3-Ti_Histórico → 4=0.
C74	H07_S5_FINANCIERO_eSIGEF + H07c
A75	Ti_FUENTE
B75	Columna informativa en H12 que indica de dónde provino el Ti de cada meta: 'eSIGEF' / 'Ti_V' / 'Ti_Histórico' / 'Sin_evidencia'. No entra al cálculo ICPI.
C75	H12_MOTOR_ICPI_CANÓNICO
A76	Ti_Histórico
B76	Tercer tipo de Ti. Usa datos históricos verificados (H07b) cuando no hay eSIGEF ni Ti_V. Solo para cálculo provisional.
C76	H07b_Ti_INVERSIÓN_eSIGEF
A77	Ti_V (Ti Verificado)
B77	Cuarto tipo de Ti. Aplica cuando no existe cédula eSIGEF pero sí existe un informe firmado electrónicamente con hash SHA-256 (PDF). Típico de metas intangibles y fondos concursables.
C77	SIAP-ICPI Metodología v1.0
A78	TIPO_FINANCIAMIENTO
B78	Clasificación del origen de los fondos de una meta/inversión. Valores: PRESUPUESTO_GAD / FONDO_CONCURSABLE / DONACION_ESPECIE / COOPERACION_DIRECTA / AUTOGESTIÓN. ★ ATRIBUTO DE LA META (v1.0): se registra en H04 columna O y en H07c — NO en H02b. La gestión pública es dialéctica: una misma dirección puede usar distintos tipos de fondos en diferentes metas.
C78	H04_S2_PLANIFICACIÓN_PDOT (col O) + H07c_Ti_VERIFICADO_INFORME
A79	TIPO_PROCESO
B79	Clasificación de cada unidad del GAD según el Estatuto Orgánico. Valores: GOBERNANTE / HABILITANTE_ASESORIA / HABILITANTE_APOYO / AGREGADOR_VALOR / ENTIDAD_ADSCRITA. Fuente: H02b.
C79	H02b_ORGÁNICO_CLASIFICADOR — Cap. IV
A80	Vi (Verificación intersistémica)
B80	Variable binaria que mide si una meta tiene evidencia verificable en los silos. Fórmula: Si los 4 verificadores (S4/S5/S7/S8) ≥1 → Vi=1.0; si suma ≥2 → Vi=0.5; si suma <2 → Vi=0.0.
C80	H13_VARIABLES_Vi
A81	Zona de Convergencia
B81	Objetivo ideal donde ICPI ≈ ICM. Significa que el autoreporte SIGAD coincide con la verificación algorítmica. En v1.0 la brecha es 30 puntos.
C81	H15_ICPI_GLOBAL — meta estratégica
A83	Modulo SENTINEL - QUIRA OS RC-1.1 (lenguaje institucional congelado)
A84	Antecedentes Comparables
B84	Alertas similares del pasado recuperadas para contextualizar la situacion actual. Scoring: tipo+3 entidad+2 severidad+2 trimestre+1
C84	QUIRA OS RC-1.1 - SENTINEL-Aprendizaje Sprint 2.8B
A85	Borrador Institucional
B85	Texto pre-redactado sugerido al funcionario basado en antecedentes comparables y patrones de resolucion aprendidos por Sentinel
C85	QUIRA OS RC-1.1 - SENTINEL-Aprendizaje Sprint 2.8C
A86	Corte Institucional
B86	Estado registrado del sistema en un periodo cerrado (mes/anio). Equivalente institucional del termino tecnico snapshot
C86	QUIRA OS RC-1.1 - Glosario Institucional
A87	Holding Municipal
B87	Conjunto de 4 entidades del GAD Municipal de Montecristi: GADMCM + Cuerpo de Bomberos + EMAI-EP + Patronato Municipal
C87	QUIRA OS RC-1.1 - Estructura institucional Montecristi
A88	Memoria Operativa
B88	Modulo que aprende de resoluciones anteriores para sugerir soluciones contextualizadas. Sin ML - solo reglas deterministicas auditables
C88	QUIRA OS RC-1.1 - SENTINEL-Aprendizaje Sprint 2.8A
A89	QUIRA OS
B89	Sistema operativo de gobernanza institucional digital para el GAD Municipal de Montecristi. Desarrollado por Dylus Lab (c) 2026 - TGI Framework
C89	Dylus Lab - TGI Framework RC-1.1
A90	Registro de Estado
B90	Documento generado al cerrar un periodo con el estado completo del Holding Municipal. Exportable como PDF institucional
C90	QUIRA OS RC-1.1 - Vista Ejecutiva RC-1.B
A91	Ruta de Atencion
B91	Flujo formal de gestion de alertas con 7 estados institucionales y bitacora inmutable append-only. 7 estados: Abierta -> Archivada
C91	QUIRA OS RC-1.1 - SENTINEL-Ruta-Atencion Sprint 2.9A
A92	Sentinel
B92	Asistente de inteligencia artificial integrado a QUIRA OS. Copiloto institucional para el GADM Montecristi - interpreta SIAP-ICPI
C92	QUIRA OS RC-1.1 - _Indice Sentinel
A93	Ti (Tasa de Inversion)
B93	Indicador de ejecucion presupuestaria mensual por entidad. Semaforo Holding: Verde>=35% Amarillo 15-34.9% Rojo<15%
C93	QUIRA OS RC-1.1 - Semaforos Holding Municipal
A94	Validacion Documental
B94	Proceso de lectura verificacion e ingesta de cedulas presupuestarias eSIGEF. Equivalente institucional del termino tecnico parser
C94	QUIRA OS RC-1.1 - Sprint 2.5B Ingesta Mensual
A95	Vista Ejecutiva
B95	Panel simplificado para Alcalde y Directivos con semaforos del Holding Municipal alertas criticas y resumen institucional sin tecnicismos
C95	QUIRA OS RC-1.1 - p_ejecutivo.py RC-1.B
A96	SIAP-ICPI v1.0 Gold Master by DYLUS LAB © 2026 | Glosario actualizado:
```