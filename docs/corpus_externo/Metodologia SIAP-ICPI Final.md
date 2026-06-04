METODOLOGÍA SIAP-ICPI v2.0

Sistema de Integridad Algorítmica y Planificación Intersistémica

QUADRUM GovTech | Ronald Javier Delgado Santana | Abril 2026

🔒 Propiedad Intelectual Protegida — Confidencial

1\. Los Nueve Silos de Información Pública Municipal

La administración pública municipal ecuatoriana opera con nueve sistemas de información que, en teoría, construyen una cadena ininterrumpida de trazabilidad desde la promesa electoral hasta la rendición de cuentas. En la práctica operan como compartimentos estancos: sin nomenclatura compartida, sin protocolos de interoperabilidad, sin mecanismos de verificación cruzada obligatoria.

El resultado no es meramente desorden administrativo. Es la producción sistemática de opacidad como estado natural del sistema, independientemente de la voluntad de quienes lo operan. A esto se denomina la Trampa de la Transparencia Formal: publicar datos sin proporcionar los medios técnicos para verificarlos viola el espíritu del Art. 18 de la Constitución que garantiza información "veraz y verificada".

Silo	Sistema	Descripción

H01	Electoral CNE	Plan de Trabajo inscrito como requisito legal de candidatura. Origen democrático del mandato. Responsable: CNE. Ningún otro silo está formalmente obligado a vincular sus registros a este documento.

H02	Planificación PDOT/SNP	Plan de Desarrollo y Ordenamiento Territorial quinquenal aprobado por ordenanza. Instrumento jurídico vinculante que traduce la promesa electoral en metas estratégicas con presupuesto asignado.

H03	Programación Operativa POA/PAC	Plan Operativo Anual con metas desagregadas, cronograma y responsables. El PAC vincula las metas POA con compromisos contractuales verificables. Fundamento: COPFP Art. 97.

H04	Contratación Pública SERCOP	Procesos contractuales publicados obligatoriamente en el portal del SERCOP. Único registro público que certifica el inicio del compromiso contractual. Fundamento: LOSNCP Art. 13.

H05	Financiero eSIGEF/MEF	Ejecución presupuestaria con devengado certificado. El devengado es el único registro admisible de gasto ejecutado. Fundamento: COPFP Art. 113-114.

H06	Auto-reporte SIGAD/SNP	Índice de Cumplimiento de Metas (ICM) reportado unilateralmente por el GAD. Métrica oficial sin validación cruzada contra silos independientes.

H07	Transparencia Activa LOTAIP	Documentos publicados en el portal institucional del GAD, cumpliendo las 45 categorías de publicación mensual obligatoria. Fundamento: LOTAIP Art. 7.

H08	Participación Ciudadana CPCCS	Informe de rendición de cuentas anual. Cierra el ciclo democrático entre mandato y evaluación. Fundamento: Constitución Art. 100.

H09	Estatuto Orgánico Funcional	Estructura institucional verificable que determina la capacidad operativa real de cada Dirección. Fundamento: LOSEP Art. 76-80.

El problema central: cada silo responde a una lógica institucional distinta, tiene responsables orgánicos diferentes, usa nomenclaturas no estandarizadas. La vinculación entre sistemas depende de la memoria institucional de un funcionario, no de un mecanismo algorítmico. El SIAP-ICPI es la capa de interoperabilidad que conecta algorítmicamente los registros ya existentes, sin agregar un sistema nuevo: opera exclusivamente sobre datos que el Estado ya publica por obligación legal.

2\. Marco Jurídico-Normativo

El SIAP-ICPI no es un sistema de auditoría extrajurídica. Cada componente está anclado en normas del ordenamiento ecuatoriano que ya imponen obligaciones a los GAD. La metodología operacionaliza algorítmicamente obligaciones preexistentes.

Norma	Obligación y componente que sustenta

Constitución Art. 18	Información "veraz, verificada, oportuna y contextualizada". Sustenta Vi: si no es verificable, ICPI lo refleja como Vi = 0.

Constitución Art. 95-100	Participación ciudadana y control social. Sustenta la dimensión ciudadana del sistema y el Silo H08.

Constitución Art. 204	"El pueblo es el mandante y primer fiscalizador del poder público." Sustenta la inversión de la carga de la prueba.

Constitución Art. 225-226	Principio de legalidad y planificación vinculante al presupuesto. Sustenta Pi.

COOTAD Art. 295-296	PDOT quinquenal con metas, indicadores y presupuesto vinculante. Sustenta Ri.

COOTAD Art. 339	Autonomía administrativa y financiera. Sustenta Ci: imputabilidad orgánica por Dirección.

COPFP Art. 97	POA y PAC alineados con el PDOT antes del inicio del año fiscal. Sustenta Ti.

COPFP Art. 113-114	El devengado como único registro válido de gasto ejecutado. Sustenta Ei.

COPFP Art. 118	Seguimiento y evaluación trimestral y semestral obligatorio. Sustenta los cortes temporales del ICPI.

LOTAIP Art. 7	45 categorías de publicación mensual obligatoria. Sustenta Vi, EED e ITAM.

LOSNCP Art. 13	Publicación obligatoria de procesos contractuales. Sustenta Silo H04.

LOSEP Art. 76-80	Evaluación de desempeño obligatoria. Sustenta Ci y el IED.

Ley Electoral Art. 97	Obligación de inscribir Plan de Trabajo ante el CNE. Sustenta el origen del Silo H01.

LOEP Art. 44-45	Empresas públicas deben formular presupuestos sujetos a planificación estratégica. Sustenta el módulo de EPs.

COESCOP Art. 274	Cuerpos de Bomberos obligados a articular su planificación al PDOT cantonal.

NCI 200-04 CGE	Normas de Control Interno — evaluación de eficiencia directiva. Sustenta el IED y las alertas automáticas hacia la CGE.



3\. La Fórmula Canónica ICPI

3.1. Definición

El Índice de Congruencia Programática e Institucional (ICPI) mide el grado de alineación certificable entre lo planificado en el PDOT y lo ejecutado con trazabilidad documental verificable en repositorios oficiales del Estado.

ICPI = \[ Σ(Pi × Ri × Vi × Ei × Ti × Ci) / Σ(Pi × Ri) ] × 100

Principio de invarianza computacional: ante el mismo conjunto de datos certificados, la fórmula siempre produce el mismo resultado, independientemente de quién la aplique. Esta invarianza elimina la discrecionalidad política del proceso de evaluación.

Resultado verificado — GAD Montecristi 2024: ICPI = 69.93%

Principio de colapso por Vi = 0: si una meta no tiene evidencia documental verificable (Vi = 0), su contribución al numerador es automáticamente cero, sin importar los valores de las demás variables. Este es el blindaje fundamental del sistema contra el autorreporte sin soporte documental.

3.2. Las Seis Variables Constitutivas

Variable	Nombre	Rango	Fuente	Fundamento	Descripción

Pi	Peso Estratégico	0–1, Σ=1.0000	PDOT/POA	COPFP Art. 97	Proporción del presupuesto total asignada a la meta. Normalizado: suma exacta = 1.0000. Las metas de mayor impacto presupuestario pesan más en el ICPI.

Ri	Relevancia Territorial/ODS	0–1	PDOT/ODS	COOTAD Art. 295-296	Vinculación con ODS, normativa sectorial y relevancia territorial. Metas ODS 5, 6 y 11 reciben Ri más alto. No manipulable post-PDOT.

Vi	Verificación Documental	0 o 0–1	LOTAIP/SERCOP	LOTAIP Art. 7	Confirma existencia y accesibilidad pública de evidencia. Vi = 0 colapsa el numerador. Es el blindaje central contra el autorreporte sin evidencia.

Ei	Evidencia Financiera	0–1	eSIGEF/MEF	COPFP Art. 113-114	Consistencia entre presupuesto codificado y devengado certificado. Solo se acepta el devengado, nunca el comprometido ni el girado.

Ti	Temporalidad/Avance físico	0–1	POA/RDC	COPFP Art. 97	Avance porcentual en el período fiscal. Excepción EAS activa para metas sociales.

Ci	Capacidad Operativa Directiva	0–1	Estatuto Orgánico	LOSEP Art. 76-80	Capacidad institucional real de la Dirección: talento humano, infraestructura, historial contractual. Único factor parcialmente exógeno al GAD.

3.3. La Nomenclatura Canónica de Metas

Cada meta del sistema lleva un código estructurado de cuatro componentes:

\[SISTEMA]-\[COMPETENCIA]-\[ODS\_CLUSTER]-\[SECUENCIA]

Código	Significado

SISTEMA: AH	Asentamientos Humanos

SISTEMA: PI	Político Institucional

SISTEMA: SC	Socio Cultural

SISTEMA: FA	Físico Ambiental

SISTEMA: EP	Económico Productivo

COMPETENCIA: C	Exclusiva Crítica (agua, saneamiento, desechos)

COMPETENCIA: I	Exclusiva Importante (salud, vialidad, equipamientos)

COMPETENCIA: L	Complementaria (cultura, turismo, participación)

ODS\_CLUSTER: G	Gobernanza (ODS 16-17)

ODS\_CLUSTER: X	Infraestructura (ODS 6-9-11-13)

ODS\_CLUSTER: N	Inclusión/NBI (ODS 1-3-4-5-10)

Ejemplo: AH-C-X-01 = Asentamientos Humanos, Competencia Crítica, Clúster Infraestructura, Meta 01 (Agua Potable).

Esta nomenclatura permite análisis cruzados instantáneos: filtrar todas las metas \*-C-\* identifica las competencias constitucionales críticas; filtrar \*-X-\* agrupa todas las metas de infraestructura elegibles para financiamiento CAF/BID.

3.4. Las 20 Metas Estratégicas — GAD Montecristi 2024

ID	Meta	ICPI	AVEP	Dirección

SC-I-N-01	Salud Municipal	95.0%	🔵 Excelencia	Patronato

SC-L-N-02	TICs y Educativo	85.0%	🟢 

Mandato	Dir. TIC

AH-I-X-01	Vialidad Cantonal	58.3%	🟡 Transición	Dir. Obras

AH-I-X-02	Señalización e IVU	0.0%	🔴 

Ruptura	Dir. Obras

AH-I-X-03	Equipamientos Públicos	58.3%	🟡 Transición	Dir. Obras

AH-I-N-01	Vivienda Interés Social	22.5%	🟠 Ocurrencia	EP Montehogar

SC-L-G-01	Cultura y Patrimonio	47.8%	🟡 Transición	Dir. Cultura

AH-I-X-04	Tránsito y Seguridad Vial	40.5%	🟡 Transición	Dir. Obras

PI-I-G-01	Modernización Administrativa	85.0%	🟢 

Mandato	Dir. Administrativa

AH-C-X-01	Agua Potable	72.0%	🟢 

Mandato	Dir. Agua

AH-C-X-02	Alcantarillado y PTAR	72.0%	🟢 

Mandato	Dir. Agua

SC-I-N-03	Grupos Prioritarios	53.4%	🟡 Transición	Patronato

FA-I-X-01	Gestión del Riesgo	65.0%	🟡 Transición	Dir. Ambiental

FA-C-X-01	Desechos Sólidos	80.0%	🟢 

Mandato	EP Aseo

FA-I-X-02	Áreas Verdes e IVU	68.8%	🟡 Transición	Dir. Ambiental

FA-L-N-01	Fauna Urbana	77.0%	🟢 

Mandato	Dir. Ambiental

PI-I-G-02	PDOT/Catastro/Trámites	85.0%	🟢 

Mandato	Dir. Planificación

PI-L-G-01	Participación Ciudadana	53.4%	🟡 Transición	Dir. Planificación

EP-L-N-01	Fortalecimiento Productivo	95.0%	🔵 Excelencia	Dir. Económica

EP-L-X-01	Turismo	85.0%	🟢 Mandato	Dir. Turismo

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

4\. La Escala AVEP

La Escala AVEP clasifica el nivel de cumplimiento institucional. Es inamovible: en ninguna capa del sistema TERRA puede usarse una escala alternativa.

Nivel	Rango	Clasificación	Descripción

🔴 Ruptura	0% — 19.99%	Ruptura Institucional	Ausencia sistemática de evidencia. Riesgo institucional crítico.

🟠 Ocurrencia	20% — 39.99%	Gestión por Ocurrencia	Ejecución improvisada sin alineación con el mandato.

🟡 Transición	40% — 69.99%	Transición Crítica	Avance verificable pero brecha significativa. Montecristi 2024: 69.93%.

🟢 Mandato	70% — 89.99%	Gestión por Mandato	Congruencia sustantiva entre lo planificado y lo ejecutado.

🔵 Excelencia	90% — 100%	Excelencia Cívica	Alineación completa. Meta aspiracional.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

5\. Los Índices Complementarios

El ICPI es el índice maestro. El sistema calcula nueve índices adicionales que capturan dimensiones que el ICPI no mide directamente. Valores de referencia: GAD Montecristi 2024.

IFE — Índice de Fidelidad Electoral (77.0%) Porcentaje de compromisos del Plan CNE incorporados al PDOT. Mide la fidelidad entre promesa electoral y planificación. De las 25 promesas del Plan CNE de Jonathan Toro, 19 tienen vinculación directa al PDOT (score 1.0), 4 tienen vinculación parcial, y 2 no tienen equivalente verificable. Un IFE bajo indica que el GAD gobernó con un plan distinto al que votó la ciudadanía.

IED — Índice de Eficiencia Directiva (70.33%) Promedio ponderado del ICPI desagregado por Dirección responsable. Identifica qué unidades administrativas explican la brecha global y asigna responsabilidad orgánica específica. Sustentado en LOSEP Art. 76-80.

Dirección	IED	Nivel LOSEP

Dir. Proyectos Estratégicos	93.0%	⭐ Excelente

Dir. Talento Humano	89.0%	🟢 Muy Bueno

Dir. Catastro	88.0%	🟢 Muy Bueno

Dir. Planificación	82.0%	🟢 Satisfactorio

Dir. Turismo/Cultura	81.7%	🟢 Satisfactorio

Dir. Gestión Ambiental	75.6%	🟡 Regular

Dir. Participación	72.0%	🟡 Regular

Dir. Agua Potable	68.8%	🟠 Regular Bajo

Dir. Financiera	68.0%	🟠 Regular Bajo

Dir. Tránsito	52.3%	🔴 Insuficiente

Dir. Administrativa	46.1%	🔴 Insuficiente

EP Aseo	55.7%	🔴 Insuficiente

Dir. Obras Públicas	42.0%	🔴 Insuficiente

ITAM — Índice de Transparencia Activa Municipal (56.0%) Porcentaje de las 45 categorías LOTAIP publicadas correctamente, en plazo y con metadatos requeridos. Montecristi 2024 tiene 14 metas con URL pública verificada de 20 posibles.

ICM SIGAD — Autorreporte oficial (100.0%) El Índice de Cumplimiento de Metas reportado unilateralmente por el GAD al SNP. No tiene validación cruzada. Es el benchmark de contraste para la Brecha de Integridad.

Brecha de Integridad (30.07 puntos) Brecha = ICM\_SIGAD − ICPI = 100.0% − 69.93% = 30.07 pp Clasificación: Brecha Controlada < 10 pts / Brecha Moderada 10-20 pts / Brecha Crítica > 20 pts → Montecristi 2024.

ICS — Índice de Cohesión Social (63.51%) Combina percepción de seguridad territorial, calidad de espacios de participación y acceso efectivo a servicios para población vulnerable.

IET — Índice de Equidad Territorial (91.42% 🔵) Distribución geográfica de la inversión pública. El indicador más sólido de Montecristi 2024.

IGP — Índice de Gobernanza Participativa (27.98%) Calidad e incidencia real de los mecanismos de participación ciudadana. Mide participación efectiva, no formal declarada.

IOC — Índice de Opacidad Crítica (17.71%) Porcentaje de metas con alta inversión (Pi alto) y baja evidencia documental (Vi bajo). Zona de mayor riesgo reputacional.

PSG — Presupuesto Sensible al Género Dualidad metodológica obligatoria:

•	PSG\_Fidelidad: 86.75% — metas con vinculación género declarada

•	PSG\_Ejecución: 2.80% — presupuesto realmente ejecutado con enfoque de género

•	Brecha: 83.95 pp → indicador de pinkwashing institucional

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

6\. El Sistema de Alertas Preventivas (SAT)

El SAT es la capa proactiva del sistema. No espera al cierre del año fiscal — anticipa durante la ejecución. Opera como sensor algorítmico continuo.

Principio diferenciador: el SAT no solo informa el problema sino que recomienda la acción correctiva específica priorizada por urgencia e impacto potencial en el ICPI.

Alerta	Umbral	Acción correctiva

SAT-0 Desconexión POA-PAC	>15% del presupuesto POA sin respaldo PAC	Revisión POA-PAC con Director Financiero antes del inicio del año fiscal

SAT-I Baja Ejecución Crítica	Meta con Pi>5% y Ei<30% al 30 de junio	Aceleración contractual o reformulación con ordenanza

SAT-II Transparencia Vencida	Cualquier categoría LOTAIP con >30 días de rezago	Carga inmediata por Unidad de Transparencia

SAT-V Compras Riesgosas	Mismo proveedor con >3 contratos ínfima cuantía en 60 días	Derivación a auditoría interna con documentación del patrón

SAT-VI Fuga Participativa	IGP < 30%	Revisión del modelo de participación con Dir. Ciudadanía

SAT-N Riesgo Narrativo	Declarado público − ICPI > 15 puntos	Revisión comunicacional y carga urgente de evidencia

SAT documentadas para TERRA v3.0:

•	SAT-0.1 Reformas Silenciosas: monitorea desfinanciamiento silencioso de metas (PC cae >20% respecto al PI a mitad de año). Requiere acceso en tiempo real al eSIGEF.

•	SAT-0.2 Limbo Precontractual: mide retraso >90 días entre mes planificado en PAC y adjudicación real en SERCOP.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

7\. Conceptos Propios — Aportes Originales

7.1. Cadena de Integridad Intersistémica (CINI)

La CINI es el flujo ininterrumpido de trazabilidad del dato público desde el mandato democrático inscrito en el CNE hasta el reporte oficial en el SIGAD/SNP, que garantiza que la promesa electoral no sufra degradación semántica, omisión deliberada ni manipulación estadística en ninguno de los nueve silos de tránsito institucional.

La CINI se manifiesta cuando existe trazabilidad biográfica completa del dato: cuando un auditor, periodista o ciudadano puede reconstruir el viaje de una meta desde la papeleta electoral hasta el contrato firmado y la obra entregada, usando únicamente fuentes de datos públicas oficiales, sin depender de la buena voluntad del GAD.

7.2. Mutación del Objeto de Medición (MOM)

La MOM ocurre cuando un GAD, en lugar de ejecutar lo planificado para mejorar el indicador de gestión, modifica el indicador para que refleje lo que sí puede ejecutar. Se persigue la métrica en lugar del objetivo que la métrica debía representar.

Tipo	Descripción	Detección algorítmica

MOM-I Fragmentación Selectiva	El GAD reporta solo metas de bajo presupuesto ejecutadas, omitiendo las de alta inversión.	ICPI pondera por Pi — las metas grandes tienen mayor peso.

MOM-II Sustitución Estratégica	El GAD reforma retroactivamente el POA reemplazando una meta costosa por una barata.	SAT-II activa si el hash SHA-256 del POA inicial difiere del POA al cierre sin ordenanza que lo justifique.

MOM-III Inflación de Unidades	El GAD redefine qué cuenta como unidad: métricas verificables se convierten en métricas elásticas.	El sistema exige evidencia documental firmada — no acepta autorreportes de unidades no verificables.

7.3. Brecha de Integridad

Brecha de Integridad = ICM\_SIGAD − ICPI

Montecristi 2024: 100.0% − 69.93% = 30.07 pp → BRECHA CRÍTICA

No es sinónimo de irregularidad. Puede originarse en: incumplimiento real, documentación insuficiente de cumplimiento que sí ocurrió, o debilidades en transparencia activa.

7.4. Algoritmo de Fidelidad de la Palabra (AFP)

AFP = 1 − ( |% Declarado Público − % Verificado TERRA| / 100 )

AFP = 1.00: congruencia perfecta. AFP = 0.00: discurso completamente desconectado de la evidencia. Alimenta la Matriz de Fidelidad Narrativa (MFN) del componente TERRA EVALÚA.

7.5. Excepción de Autogestión Social (EAS)

Para metas donde el valor público se genera mediante capital humano, voluntariado o articulación comunitaria, la variable Ti se calcula con base en el avance físico documentado, no en el porcentaje de ejecución financiera. Esta regla evita castigar programas sociales eficientes que tienen baja ejecución presupuestaria precisamente porque operan con capital humano.

7.6. Gestión Emergente de Valor Público (GEVP)

Conjunto de acciones no planificadas originalmente en el POA que generan valor territorial verificable mediante afectación positiva de indicadores del PDOT. Fundamentación: COPFP Arts. 41-42. Categorías: Servicio Personal Directo, Fondos Externos Ganados, Convenios Interinstitucionales, Recursos no Presupuestarios. Documentado para incorporación en TERRA v2.1.

7.7. Escala de Evidencia Documental (EED)

Metadato de calidad probatoria independiente de Vi:

Rango	Nivel

0.00 – 0.25	Sin evidencia o evidencia inválida. Vi = 0 en el ICPI.

0.26 – 0.50	Evidencia parcial: documento incompleto, sin firmas o metadatos insuficientes.

0.51 – 0.75	Evidencia básica: documento accesible pero sin acta de entrega-recepción.

0.76 – 1.00	Evidencia sólida: documento completo, firmado, publicado en LOTAIP, con trazabilidad completa.

7.8. Gasto Extrapiramidal (GEP)

GEP = Inversión Total (Grupos 7+8 eSIGEF) − Σ Presupuesto Codificado Anual de Metas PDOT

Brecha de Pertinencia = GEP / Inversión Total × 100

⚠️ El cálculo usa el Presupuesto Codificado Anual en dólares, NO los pesos Pi (que son proporciones normalizadas). Confundirlos produce resultados matemáticamente inválidos.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

8\. El Módulo de Empresas Públicas y Entidades Adscritas

8.1. Fundamento

Las empresas públicas municipales, entidades adscritas y desconcentradas forman parte del ecosistema de ejecución del PDOT. El SIAP-ICPI las evalúa con una lógica de doble salida: eficacia operativa y legalidad administrativa.

8.2. Lógica "No Privar pero Alertar"

SI PEI\_Existe = NO:

&#x20; Estado\_Legal = "🔴 ILEGAL — Violación LOEP Art. 44"

&#x20; ICPI\_Operativo = calculado normalmente con POA+PAC+Cédula

&#x20; ICPI\_Final = 0% automático

&#x20; Alerta: "Gasto sin rumbo legal → Causal glosa CGE (NCI 200-04)"



SI PEI\_Existe = SÍ y POA\_Cargado = SÍ:

&#x20; ICPI\_Final = ICPI\_Operativo × R\_i\_PEI (0.85-1.0)



SI PEI\_Existe = SÍ y POA\_Cargado = NO:

&#x20; Estado = "🟡 INCOMPLETO"

8.3. Marco Legal por Tipo de Entidad

Entidad	Norma principal	Obligación

Empresas Públicas EP	LOEP Art. 44-45 + COOTAD Art. 234	PEI obligatorio para formular presupuesto

Cuerpos de Bomberos	COESCOP Art. 274 + Ley Defensa Incendios	PEI operativo articulado al PDOT cantonal

Entidades Adscritas	COPFP Arts. 9, 13, 54	Afectación positiva indicadores PDOT como fuente de legitimación

GAD Base	COOTAD Art. 295	POA sujeto al PDOT aprobado por ordenanza

8.4. Bypass Ciudadano — COPFP Art. 54

Aunque la EP no tenga PEI, el ciudadano puede desarrollar el análisis completo si dispone del POA, PAC y Cédula Presupuestaria. El sistema calcula el ICPI operativo y lo muestra con doble salida: cumplimiento real + alerta de ilegalidad administrativa. Esto permite documentar que la EP "cumplió operativamente" mientras se expone la "orfandad legal" en planificación.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

9\. Cortes Temporales y Análisis Longitudinal

9.1. ICPI Dual

Perspectiva	Qué mide	Fuente

ICPI Anual (corte fiscal)	Cumplimiento de metas en un año fiscal usando Ti = avance anual	Hoja H12

ICPI Acumulado (mandato)	Avance acumulado sobre la meta total del PDOT quinquenal	Hoja H12b

La divergencia entre ambas perspectivas es información estratégica: revela si el GAD ejecuta de manera consistente o concentra ejecución en ciertos años.

9.2. Curva S de Ejecución

Fundamentada en COPFP Art. 118 (seguimiento trimestral obligatorio):

Trimestre	Expectativa histórica	Por debajo →

Q1 (31/03)	15-20%	Alerta preventiva

Q2 (30/06)	35-40%	SAT-I activado

Q3 (30/09)	65-75%	Riesgo de incumplimiento

Q4 (31/12)	90-100%	Cierre fiscal

9.3. Análisis Longitudinal 2023-2027

Para análisis del período completo de gobierno, el ciudadano carga 4 años de documentos (POA, PAC, Cédulas) más el PDOT y el Plan CNE. El sistema calcula:

ICPI\_Periodo = Σ(Ti\_2023 + Ti\_2024 + ... + Ti\_2027) / Meta\_PDOT\_Quinquenal

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

10\. TERRA CIUDADANA — Arquitectura de la Plataforma Ciudadana

El SIAP-ICPI tiene dos implementaciones: TERRA GAD (institucional, SaaS B2G) y TERRA CIUDADANA (pública, gratuita). TERRA CIUDADANA democratiza el acceso a la metodología mediante siete componentes con identidad propia.

Componente	Función	Tecnología

TERRA ACCEDE	Generador de oficio LOTAIP blindado jurídicamente	python-docx

TERRA VERIFICA	Ingesta de documentos + OCR + hash SHA-256	Tesseract (fase 2)

TERRA CALCULA	Motor ICPI ciudadano con fórmula canónica	Motor SIAP-ICPI

TERRA MAPEA	Mapa territorial interactivo de brechas	Folium

TERRA ARTICULA	Marco legal + argumento de elegibilidad bilateral	API Anthropic (fase 2)

TERRA ACTÚA	Modos A/B/C de incidencia + cartas + proyectos	python-docx + fpdf2

TERRA EVALÚA	Discurso vs informe técnico vs ICPI (NLP/Whisper)	Whisper + NLP (fase 2)

Principio: el ciudadano que obtiene documentos del GAD via LOTAIP puede calcular su propio ICPI independiente del autorreporte institucional. Si el ICPI ciudadano difiere del ICM oficial, el ciudadano tiene la prueba.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

11\. Nota Metodológica — Caso Piloto Montecristi 2024

Categoría	Fuente	Estado

PDOT 2023-2027	Registro Oficial — ordenanza aprobada	✅ Real

Plan de Trabajo CNE	CNE — inscripción candidatura	✅ Real

POA 2024	GAD Montecristi	✅ Real

PAC 2024	GAD Montecristi (SERCOP)	✅ Real

Informe CPCCS N° 22844	CPCCS — rendición de cuentas	✅ Real

Cédula presupuestaria	Memorandum 0511-CNVC-DF-GADMCM-2026	⚠️ Proxy 2025 como estimación 2024

LOTAIP / Verificables físicos	Portal institucional GAD	⚠️ Simulación técnica documentada

La cédula presupuestaria 2024 real no está disponible públicamente en el portal eSIGEF. Esta limitación es en sí misma un hallazgo: los sistemas de planificación del Estado no son accesibles para verificación ciudadana independiente, lo que justifica la existencia de TERRA CIUDADANA.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

12\. Glosario Canónico

Término	Definición

AFP	Algoritmo de Fidelidad de la Palabra. AFP = 1 − (

AVEP	Escala canónica de clasificación del ICPI: 5 niveles. Inamovible.

Brecha de Integridad	ICM\_SIGAD − ICPI. No es sinónimo de irregularidad.

CINI	Cadena de Integridad Intersistémica. Flujo de trazabilidad del dato público desde el CNE hasta el SIGAD.

EAS	Excepción de Autogestión Social. Ti = avance físico (no financiero) para metas sociales con capital humano.

EED	Escala de Evidencia Documental (0.0-1.0). Metadato de calidad probatoria. No es la variable Vi.

GEP	Gasto Extrapiramidal. Inversión fuera de la pirámide del PDOT. En dólares, nunca en Pi.

GEVP	Gestión Emergente de Valor Público. Acciones no planificadas con afectación positiva de indicadores. COPFP Arts. 41-42.

ICM	Índice de Cumplimiento de Metas. Autorreporte oficial al SIGAD. Sin validación cruzada.

ICPI	Índice de Congruencia Programática e Institucional. Índice maestro del sistema.

ICPI Dual	Perspectiva anual (H12) vs acumulada de mandato (H12b). La fórmula no cambia, solo Ti.

MOM	Mutación del Objeto de Medición. Tres tipos: Fragmentación Selectiva (I), Sustitución Estratégica (II), Inflación de Unidades (III).

Pinkwashing	PSG\_Fidelidad alta + PSG\_Ejecución baja. Declaración retórica de género sin inversión real.

PSG	Presupuesto Sensible al Género. Dualidad: PSG\_Fidelidad ≠ PSG\_Ejecución. El dashboard muestra PSG\_Ejecución.

SAT	Sistema de Alertas Preventivas. 6 activas + 2 documentadas para v3.0.

SIAP-ICPI	Sistema de Integridad Algorítmica y Planificación Intersistémica. Motor metodológico. TERRA es la plataforma.

Axioma de Invarianza	Ante los mismos datos certificados, el ICPI siempre produce el mismo resultado.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

TERRA SIAP-ICPI v2.0 — QUADRUM GovTech Ronald Javier Delgado Santana — Diplomado DGIP CAF-ESPOL 2026 🔒 Propiedad Intelectual Protegida





