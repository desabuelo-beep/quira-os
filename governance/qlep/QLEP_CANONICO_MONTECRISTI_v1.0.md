# QLEP_CANONICO_MONTECRISTI_v1.0
## Documento Canónico — Norma Primaria + Pregunta Bautismal
### Los 12 Dominios del Gemelo Institucional de Montecristi

**Estado**: CONGELADO  
**Versión**: 1.0  
**Fecha**: 2026-06-01  
**Proyecto**: QUIRA Gov — Dylus Lab  
**Clasificación**: Interno · QUIRA Operaciones  

---

## Principio

Este documento congela el núcleo epistemológico del Gemelo Institucional de Montecristi.

**N1** (Norma primaria) establece la base jurídica sin la cual el dominio no existe.  
**N2** (Pregunta bautismal) establece la pregunta mínima que un alcalde debe poder responder para gobernar ese dominio. No es la única pregunta posible. Es la pregunta fundacional: si no tiene respuesta, el dominio no puede gobernarse.

Las 12 preguntas bautismales no son independientes. Son interdependientes de forma estructurada.  
La coherencia entre ellas es tan importante como cada pregunta individual.  
Por eso este documento las define en una sola pasada: cambiar N2 de Dom04 puede cambiar N2 de Dom01.

**Regla de oro de este documento**: Sin norma, no hay indicador. Sin pregunta bautismal, no hay cadena causal.

---

## C10 — Registro de Cierre del Circuito Causal

Cada dominio, cuando esté completo, produce un **Registro C10**: la síntesis de todo el circuito causal en un formato legible por el Alcalde.

Los 10 campos canónicos del Registro C10:

| Campo | Capa QNKC | Contenido |
|---|---|---|
| `c01_norma` | C1 Jurídica | Texto de la norma primaria y referencia exacta |
| `c02_competencia` | C2 Competencial | Competencia o atribución habilitante del GAD |
| `c03_servicio` | C3 Servicio Público | Qué servicio o función debe existir en el territorio |
| `c04_proceso` | C4 Proceso | Cómo se ejecuta — trámite, POA, contrato, ordenanza |
| `c05_evidencia` | C5 Evidencia | Qué documenta la ejecución (SIGEF / LOTAIP / Catastro) |
| `c06_control` | C6 Control | Qué verifica o sanciona (CGE / NCI / UAI) |
| `c07_observabilidad` | C7 Observabilidad | Qué publica el municipio (LOTAIP numeral específico) |
| `c08_indicador` | C8 Indicador | Qué mide el resultado (KPI canónico del dominio) |
| `c09_resultado` | C9 Resultado Territorial | Qué ocurre realmente (dato oficial verificado) |
| `c10_estado_quira` | C10 SAT Output | Estado QUIRA: semáforo + narrativa de alerta para el Alcalde |

El Registro C10 no es una pantalla. Es la estructura de conocimiento que hace posible la pantalla.

---

## Los 12 Dominios — N1 + N2

---

### Dom01 — Planificación Estratégica

**N1 — Norma primaria:**

> **CE Art. 264 numeral 1** — Los gobiernos municipales tendrán las siguientes competencias exclusivas sin perjuicio de otras que determine la ley: 1. Planificar el desarrollo cantonal y formular los correspondientes planes de ordenamiento territorial, de manera articulada con la planificación nacional, regional, provincial y parroquial, con el fin de regular el uso y la ocupación del suelo urbano y rural.

Norma complementaria obligatoria: **COOTAD Art. 54 lit. a** (función del GAD-M: promover el desarrollo sustentable mediante implementación de políticas públicas cantonales).

**N2 — Pregunta bautismal:**

> **¿Puede Montecristi completar los compromisos del PDOT Bicentenario 2023-2027 con los recursos asignados y el tiempo restante del mandato?**

*Por qué esta pregunta y no "¿cómo está el PDOT?"*: La pregunta genérica genera un reporte de estado. La pregunta bautismal genera una alerta de gestión: fuerza al sistema a cruzar metas vs. recursos vs. cronograma vs. tiempo restante — y produce una brecha accionable.

**Estado QLEP:**
- C1/C2 cubiertos: CE_264 (F0.1), COOTAD_54 (F0.3), COOTAD_192 (F0.3)
- Circuito QTMP: no cerrado para Dom01 — PDOT como cadena causal pendiente
- Corpus disponible: 3 ACK atoms directos + 8 REL-H que cruzan con Dom02/Dom04/Dom09

**Coherencia crítica**: Dom01 falla → Dom03 no puede medir → Dom09 no puede rendir cuentas.

---

### Dom02 — Presupuesto & Financiamiento

**N1 — Norma primaria:**

> **COOTAD Art. 215** — El presupuesto de los gobiernos autónomos descentralizados se ajustará a los planes regionales, provinciales, cantonales y parroquiales respectivamente, en el marco del Plan Nacional de Desarrollo, sin menoscabo de sus competencias y autonomía. El presupuesto de los gobiernos autónomos descentralizados deberá ser elaborado participativamente, de acuerdo con lo prescrito por la Constitución y la ley.

Norma complementaria: **COOTAD Art. 198** (presupuesto de inversión; vinculación con POA y PAC).

**N2 — Pregunta bautismal:**

> **¿Qué recursos presupuestarios aprobados no están fluyendo hacia resultados territoriales verificables, y por qué?**

*Por qué esta pregunta y no "¿cómo está el presupuesto?"*: El presupuesto aprobado es una declaración de intención. La pregunta bautismal exige la cadena completa: presupuesto → devengado → ejecutado → resultado → territorio. Si hay ruptura en cualquier punto, el dominio está fallando aunque el presupuesto esté "aprobado".

**Estado QLEP:**
- C1/C2 cubiertos: COOTAD_215 (F0.3), COOTAD_198 (F0.3), NCI_PRE_DEVENGADO (F0.4)
- Circuito QTMP: **CONTROL_PREV cerrado** — NCI_PRE_COMPROMISO → D3=59.85% → TGI Dom02
- REL-H activos: H1 (Dom02↔Dom12), H5 (Dom01↔Dom02), H7 (Dom02↔Dom04), H11 (Dom03↔Dom02)

**Coherencia crítica**: Dom02 falla → Dom05 (holding sin recursos) → Dom12 (GAP sin ejecución).

---

### Dom03 — Seguimiento de Metas

**N1 — Norma primaria:**

> **COOTAD Art. 300** — Los gobiernos autónomos descentralizados contarán con un consejo de planificación, que estará presidido por el ejecutivo del GAD e integrado por representantes de la sociedad civil, según lo establezca la ley; ejercerá la facultad de control social y la contraloría ciudadana sobre el cumplimiento de los planes de desarrollo y de ordenamiento territorial.

Norma complementaria: **CE Art. 241** (GADs generan planes de desarrollo articulados con sistema nacional de planificación). Instrumento técnico: **CPFP Art. 44** (seguimiento y evaluación de planes — *pendiente atomización en F0.7*).

**N2 — Pregunta bautismal:**

> **¿Cuáles son las metas del PDOT con mayor riesgo de rezago, cuál es la causa institucional raíz de cada retraso, y qué decisión de gestión reduce ese riesgo?**

*Por qué esta pregunta y no "¿cuántas metas están en ruta?"*: El porcentaje de metas en ruta es un indicador de estado, no de causalidad. La pregunta bautismal exige explicación: ¿el rezago es de recursos (Dom02), de proceso (Dom05), de cobertura territorial (Dom10), o de participación insuficiente (Dom08)? Sin causa raíz, no hay decisión de gestión.

**Estado QLEP:**
- C1/C2 cubiertos: COOTAD_300 (F0.3), CE_241 (F0.1)
- Circuito QTMP: no cerrado — CPFP pendiente de atomización (F0.7)
- REL-H activos: H7 (Dom02↔Dom04/Dom09 vía planificación)

**Coherencia crítica**: Dom03 depende de Dom01 (sin PDOT, no hay metas). Dom03 alimenta Dom09 (rendición de cuentas sin datos de seguimiento es vacía).

---

### Dom04 — Alertas Institucionales

**N1 — Norma primaria:**

> **LOC-CGE Art. 12** — El control interno comprenderá las acciones de carácter administrativo, operativo, financiero, contable y presupuestario que realizan las autoridades, funcionarios y servidores de las entidades por sus propias acciones, con el objeto de que los recursos institucionales sean administrados con eficiencia, efectividad, economía, equidad, legalidad y transparencia. El control interno es previo, continuo y posterior.

Norma complementaria: **NCI 600-01** (seguimiento continuo — "Los directivos de la entidad, establecerán procedimientos de seguimiento continuo, evaluaciones periódicas o una combinación de ambas para asegurar la eficacia del sistema de control interno").

**N2 — Pregunta bautismal:**

> **¿Qué señales de riesgo institucional activas en el sistema de monitoreo requieren intervención directa antes de que escalen a incumplimiento normativo con consecuencia legal?**

*Por qué esta pregunta y no "¿cuántas alertas hay?"*: El número de alertas es una métrica. La pregunta bautismal exige priorización: de todas las señales activas, cuáles son las que, de no intervenirse en este período, generarán glosa CGE, observación CPCCS, o sanción DPE. Sin esa priorización, el sistema de alertas produce ruido, no decisión.

**Estado QLEP:**
- C1/C2 cubiertos: LOCCGE_12 (F0.4), NCI_600_01 (F0.4), NCI_300 (F0.4)
- Circuito QTMP: **CONTROL_LEGAL cerrado** — LOC-CGE_45 → LOTAIP_19_12 → TGI Dom01
- REL-H activos: H5 (Dom01↔Dom02), H9 (Dom01↔Dom07)

**Coherencia crítica**: Dom04 observa a todos los otros dominios. Es el dominio transversal: si fallan Dom02, Dom05, Dom07 o Dom10, Dom04 es el primero en saberlo.

---

### Dom05 — Holding Municipal

**N1 — Norma primaria:**

> **CE Art. 315** — El Estado constituirá empresas públicas para la gestión de sectores estratégicos, la prestación de servicios públicos, el aprovechamiento sustentable de recursos naturales o de bienes públicos y el desarrollo de otras actividades económicas.

Norma habilitante específica GAD: **COOTAD Art. 57 lit. h** — Al Concejo Municipal le corresponde: h) Constituir, suprimir, fusionar y escindir empresas municipales, aprobar sus estatutos, garantías, contratos, así como crear consejos de administración para las mismas, en el marco de los planes de desarrollo cantonal.

Norma de gestión: **LOEP Art. 4** — Las empresas públicas son entidades que pertenecen al Estado en los términos que establece la Constitución de la República, personas jurídicas de derecho público, con patrimonio propio, dotadas de autonomía presupuestaria, financiera, económica, administrativa y de gestión, con altos parámetros de calidad y criterios empresariales, económicos, sociales y ambientales.

**N2 — Pregunta bautismal:**

> **¿Las entidades del holding municipal están ejecutando sus mandatos de servicio público con la eficiencia y calidad que justifica su existencia jurídica?**

*Por qué esta pregunta y no "¿cómo está el promedio del holding?"*: El promedio oculta divergencias críticas. La pregunta bautismal exige justificación de existencia: cada EP fue creada para prestar un servicio específico con mandato legal. Si no lo está haciendo con calidad suficiente, hay tres opciones de gestión — mejorar, fusionar, o disolver. Sin esa pregunta, el holding se perpetúa independientemente de sus resultados.

**Estado QLEP:**
- C1/C2: CE_315 (parcialmente en F0.1 como principio), COOTAD_57 (*pendiente atomización*)
- LOEP: pendiente — no en corpus F0.1-F0.6
- Circuito QTMP: no cerrado — requiere atomización LOEP (F0.8)
- REL-H activos: H4 (Dom05↔Dom02), H4+ (LOSEP4↔COOTAD198)

**Coherencia crítica**: Dom05 consume Dom02 (recursos) y produce resultados para Dom10 (agua), Dom12 (patronato), Dom04 (empresa aseo). Es el dominio ejecutor del holding.

---

### Dom06 — Salud Institucional

**N1 — Norma primaria:**

> **CE Art. 226** — Las instituciones del Estado, sus organismos, dependencias, las servidoras o servidores públicos y las personas que actúen en virtud de una potestad estatal ejercerán solamente las competencias y facultades que les sean atribuidas en la Constitución y la ley. Tendrán el deber de coordinar acciones para el cumplimiento de sus fines y hacer efectivo el goce y ejercicio de los derechos reconocidos en la Constitución.

Norma de medición: **COOTAD Art. 228** — Los presupuestos de inversión se formularán aplicando criterios de eficiencia, equidad territorial, densidad de población, pobreza, necesidades básicas insatisfechas y logros de su disminución.

**N2 — Pregunta bautismal:**

> **¿En qué proporción el municipio está cumpliendo el universo de sus obligaciones legales vigentes, y dónde están concentradas las brechas más críticas?**

*Por qué esta pregunta y no "¿cuál es el índice de cumplimiento?"*: El índice es la respuesta; la pregunta bautismal exige la distribución: no todas las brechas tienen el mismo peso legal ni el mismo impacto territorial. Una brecha en Dom10 (agua) tiene consecuencias jurídicas distintas a una brecha en Dom07 (transparencia). La "salud institucional" no es un número — es la geografía del cumplimiento.

**Estado QLEP:**
- C1/C2: CE_226 (F0.1), COOTAD_228 (F0.3), COA_14 (F0.6 — principio legalidad administrativa)
- Circuito QTMP: **EQUIDAD cerrado** — CE_241 → COOTAD_228 → IRS=79.7% → TGI Dom06
- REL-H activos: H5 (Dom01↔Dom02 vía control)

**Coherencia crítica**: Dom06 es el dominio meta: mide la salud de todos los otros dominios. Si Dom07 falla, Dom06 cae. Si Dom10 falla, Dom06 cae. Dom06 es el ICPI expresado como dominio.

---

### Dom07 — Transparencia

**N1 — Norma primaria:**

> **CE Art. 18** — Todas las personas, en forma individual o colectiva, tienen derecho a: 1. Buscar, recibir, intercambiar, producir y difundir información veraz, verificada, oportuna, contextualizada, plural, sin censura previa acerca de los hechos, acontecimientos y procesos de interés general, y a gozar de la libertad de expresión y de opinión.

Norma operativa: **LOTAIP Art. 7** — Por transparencia activa, las instituciones del Estado y las personas jurídicas de derecho privado con participación accionaria mayoritaria del Estado deberán publicar la siguiente información mínima actualizada... (21 numerales). *Corpus F0.2 completo: 14 ACK atoms.*

**N2 — Pregunta bautismal:**

> **¿Toda la información de acceso público que el municipio debe transparentar por mandato legal está disponible, actualizada y comprensible para cualquier ciudadano en este momento?**

*Por qué esta pregunta y no "¿publicamos los 21 artículos?"*: La publicación formal no garantiza comprensibilidad ni actualización. La pregunta bautismal incluye tres dimensiones: disponibilidad (está publicado), actualidad (es del período vigente), y comprensibilidad (un ciudadano puede entenderlo y usarlo). Sin esas tres dimensiones, la transparencia es compliance formal, no derecho real.

**Estado QLEP:**
- C1/C2: CE_18 (F0.1), LOTAIP_7 (F0.2), LOTAIP_19 completo (F0.2) — **corpus más completo**
- Circuito QTMP: **YAML materializado** — `data/qtmp/qtmp_ECU-13-MONTECRISTI_TRANSPARENCIA.yaml` (2026-06-01, 811 líneas, cadena C3-C9 completa) · Neo4j load pendiente Sprint 4
- Conector: `app/connectors/neo4j_qtmp.py` — `TRANSPARENCIA` circuit registrado · fallback + query operativos
- REL-H activos: H6 (Dom07↔Dom08), H9 (Dom01↔Dom07), H3 (Dom03↔Dom08 vía LOTAIP)

**Coherencia crítica**: Dom07 es prerrequisito de Dom08 (sin información pública, la participación es vacía) y de Dom09 (sin publicaciones actualizadas, la rendición de cuentas no tiene base documental verificable).

---

### Dom08 — Participación Ciudadana

**N1 — Norma primaria:**

> **CE Art. 95** — Las ciudadanas y ciudadanos, en forma individual y colectiva, participarán de manera protagónica en la toma de decisiones, planificación y gestión de los asuntos públicos, y en el control popular de las instituciones del Estado y la sociedad, y de sus representantes, en un proceso permanente de construcción del poder ciudadano.

Norma operativa GAD: **COOTAD Art. 304** — El gobierno autónomo descentralizado municipal establecerá en su presupuesto anual una partida específica destinada a financiar el presupuesto participativo. Los gobiernos autónomos descentralizados harán el llamado público para la presentación de proyectos que puedan ser financiados con estos recursos. *Atom COOTAD_304 en corpus F0.3.*

**N2 — Pregunta bautismal:**

> **¿Los mecanismos de participación ciudadana vigentes en Montecristi están efectivamente incidiendo en las decisiones de inversión y gestión territorial, o son procesos formales sin consecuencia real?**

*Por qué esta pregunta y no "¿cuántos mecanismos de participación existen?"*: Seis mecanismos activos es un dato de proceso. La pregunta bautismal exige evidencia de incidencia real: ¿una decisión tomada en presupuesto participativo se materializó en el POA? ¿Un cabildo produjo una modificación presupuestaria? Sin esa trazabilidad, la participación es ceremonia, no gobernanza.

**Estado QLEP:**
- C1/C2: CE_95 (*pendiente atomización F0.7*), COOTAD_304 (F0.3), COOTAD_302 (F0.3)
- Circuito QTMP: **PARTICIPACION cerrado** — COOTAD_304 → PP-parroquia (C4) → TGI Dom08
- REL-H activos: H6 (Dom07↔Dom08), H8 (Dom08↔Dom12), H3 (Dom03↔Dom08), H3+ (COOTAD304↔LOSNCP21)

**Coherencia crítica**: Dom08 depende de Dom07 (información pública previa a participación) y alimenta Dom12 (grupos prioritarios participan para proteger sus derechos).

---

### Dom09 — Rendición de Cuentas

**N1 — Norma primaria:**

> **CE Art. 209** — El Consejo de Participación Ciudadana y Control Social promoverá e incentivará el ejercicio de los derechos relativos a la participación ciudadana, impulsará y establecerá mecanismos de control social en los asuntos de interés público, y designará a las autoridades que le corresponda de acuerdo con la Constitución y la ley.

Norma operativa: **COOTAD Art. 302** — Rendición de cuentas. La ciudadanía tiene el derecho de ejercer el control social de la gestión de los gobiernos autónomos descentralizados, con el propósito de evaluar el cumplimiento de los planes de desarrollo, de las metas e indicadores, la pertinencia de las políticas públicas, la gestión de sus recursos financieros... *Atom COOTAD_302 en corpus F0.3.*

**N2 — Pregunta bautismal:**

> **¿Puede el municipio demostrar ante la ciudadanía y los órganos de control el cumplimiento verificable de cada compromiso de gestión del período, con evidencia documental trazable desde la norma hasta el resultado territorial?**

*Por qué esta pregunta y no "¿completamos los 20 ítems CPCCS?"*: Los 20 ítems son la lista de compliance. La pregunta bautismal exige trazabilidad real: para cada compromiso de gestión, ¿existe la cadena norma → POA → presupuesto → contrato → ejecución → resultado → informe? Sin esa cadena, la rendición de cuentas es un reporte sin evidencia verificable.

**Estado QLEP:**
- C1/C2: CE_209 (*pendiente atomización*), COOTAD_302 (F0.3), COOTAD_300 (F0.3)
- Circuito QTMP: no cerrado específicamente para Dom09
- REL-H activos: H3 (Dom03↔Dom08 vía LOTAIP19_8↔COOTAD302), H6 (Dom07↔Dom08)

**Coherencia crítica**: Dom09 es el dominio de cierre del ciclo. Depende de todos: sin Dom01 (metas), Dom03 (seguimiento), Dom07 (transparencia), Dom08 (participación), la rendición de cuentas no tiene material. Dom09 es el test de verdad del ciclo completo.

---

### Dom10 — Territorio & Cobertura

**N1 — Norma primaria:**

> **CE Art. 264 numeral 4** — Los gobiernos municipales tendrán las siguientes competencias exclusivas sin perjuicio de otras que determine la ley: 4. Prestar los servicios públicos de agua potable, alcantarillado, depuración de aguas residuales, manejo de desechos sólidos, actividades de saneamiento ambiental y aquellos que establezca la ley.

Norma de derecho fundamental: **CE Art. 12** — El derecho humano al agua es fundamental e irrenunciable. El agua constituye patrimonio nacional estratégico de uso público, inalienable, imprescriptible, inembargable y esencial para la vida. *Atoms CE_12 y CE_264 en corpus F0.1.*

**N2 — Pregunta bautismal:**

> **¿El municipio está garantizando acceso equitativo y continuo a los servicios básicos de agua potable y saneamiento para todos los habitantes del cantón, incluyendo zonas rurales y comunidades alejadas?**

*Por qué esta pregunta y no "¿cuál es la cobertura?"*: La cobertura promedio oculta inequidad territorial. La pregunta bautismal exige dos dimensiones: equidad (¿la brecha urbano-rural está cerrándose?) y continuidad (¿el acceso es real o nominal?). Un cantón con 80% de cobertura urbana y 10% rural no está cumpliendo la norma — aunque su promedio sea aceptable.

**Estado QLEP:**
- C1/C2: CE_12 (F0.1), CE_264 (F0.1), COOTAD_137 (F0.3) — **corpus completo**
- Circuito QTMP: **AGUA_POTABLE cerrado** — CE_12 → CE_264.4 → COOTAD_137 → LOTAIP_19_6 → TGI Dom10
- REL-H activos: H2 (Dom04↔Dom12 vía cobertura territorial)
- Layer 2: p10_territorio.py implementado · ADR-013 congelado

**Coherencia crítica**: Dom10 falla → Dom12 falla (zonas sin agua = zonas con más vulnerabilidad social). Dom10 depende de Dom05 (EP Agua como ejecutor del servicio).

---

### Dom11 — Ecosistema Productivo Territorial

**N1 — Norma primaria:**

> **CE Art. 276 numeral 2** — El régimen de desarrollo tendrá los siguientes objetivos: 2. Construir un sistema económico, justo, democrático, productivo, solidario y sostenible basado en la distribución igualitaria de los beneficios del desarrollo, de los medios de producción y en la generación de trabajo digno y estable.

Norma habilitante GAD: **COOTAD Art. 54 lit. g** — Las funciones del gobierno autónomo descentralizado municipal comprenden: g) Regular, controlar y promover el desarrollo de la actividad turística cantonal en coordinación con los demás gobiernos autónomos descentralizados, promoviendo especialmente la creación y funcionamiento de organizaciones asociativas y empresas comunitarias de turismo.

Norma complementaria: **CE Art. 264 numeral 8** (planificación, regulación y control del uso del suelo como habilitante de actividad productiva).

**N2 — Pregunta bautismal:**

> **¿Las condiciones que el municipio puede controlar — suelo, infraestructura, regulación, encadenamiento productivo — están creando las condiciones para la generación de empleo digno y actividad económica sostenible en el territorio?**

*Por qué esta pregunta y no "¿cuántas empresas hay en el cantón?"*: El número de empresas depende de factores nacionales y globales fuera del control municipal. La pregunta bautismal delimita la agencia real del GAD: suelo habilitado, infraestructura disponible, trámites simplificados, encadenamientos promovidos. Esos factores sí son competencia municipal verificable.

**Estado QLEP:**
- C1/C2: CE_276 (*pendiente atomización*), COOTAD_54 (*pendiente*), CE_264_8 (*pendiente*)
- Circuito QTMP: **no existe** — dominio EN CONSTRUCCIÓN · módulo deshabilitado
- REL-H: sin circuitos horizontales cerrados para Dom11

**Coherencia crítica**: Dom11 depende de Dom01 (PDOT debe incluir componente productivo) y de Dom10 (territorio con servicios básicos atrae inversión productiva). El fracaso de Dom11 retroalimenta Dom12 (sin empleo → más grupos prioritarios en vulnerabilidad).

---

### Dom12 — Protección Social & Grupos Prioritarios

**N1 — Norma primaria:**

> **CE Art. 35** — Las personas adultas mayores, niñas, niños y adolescentes, mujeres embarazadas, personas con discapacidad, personas privadas de libertad y quienes adolezcan de enfermedades catastróficas o de alta complejidad, recibirán atención prioritaria y especializada en los ámbitos público y privado. La misma atención prioritaria recibirán las personas en situación de riesgo, las víctimas de violencia doméstica y sexual, maltrato infantil, desastres naturales o antropogénicos. El Estado prestará especial protección a las personas en condición de doble vulnerabilidad.

Norma de financiamiento: **COOTAD Art. 249** — Los gobiernos municipales tendrán la obligación de asignar en sus presupuestos, de manera prioritaria y progresiva, recursos suficientes para la dotación de infraestructura necesaria para garantizar los derechos de la naturaleza y del buen vivir, y asignarán un porcentaje no inferior al diez por ciento de sus ingresos no tributarios para el financiamiento de la planificación y ejecución de programas sociales para la atención a grupos de atención prioritaria. *Atoms CE_35 (F0.1), COOTAD_249 (F0.3) — corpus completo incluyendo CONA, LOAPAM, LOD, LOMH (F0.5).*

**N2 — Pregunta bautismal:**

> **¿El municipio está garantizando el piso mínimo de protección social a todos los grupos de atención prioritaria del cantón, con especial cobertura en las zonas de mayor vulnerabilidad, y los recursos asignados están llegando efectivamente a esos grupos?**

*Por qué esta pregunta y no "¿asignamos el 10%?"*: La asignación formal es el requisito mínimo. La pregunta bautismal agrega la dimensión de ejecución (el dinero llega) y la dimensión de cobertura territorial (llega a los más vulnerables, no solo a la cabecera cantonal). La paradoja activa de Montecristi es exactamente esta: asignación formal VERDE (20.84%), ejecución ROJO (50%).

**Estado QLEP:**
- C1/C2: CE_35 (F0.1), COOTAD_249 (F0.3), CONA_12/207 (F0.5), LOAPAM_14/84 (F0.5), LOD_47/56/58 (F0.5), LOMH_165/166/167 (F0.5) — **corpus más completo del sistema**
- Circuito QTMP: **GAP_10PCT cerrado** — CE_35 → COOTAD_249 → LOTAIP_19_6 → TGI Dom12
- Layer 2: p19_genero.py implementado · connector get_qtmp_chain("GAP_10PCT") operativo
- REL-H activos: H1 (Dom02↔Dom12), H2 (Dom04↔Dom12), H8 (Dom08↔Dom12)

**Coherencia crítica**: Dom12 es el receptor de todas las brechas. Si Dom02 falla (presupuesto), Dom10 falla (agua), Dom08 falla (participación), el primer impacto visible es en Dom12 — los grupos prioritarios son el indicador canario del sistema. Es el dominio con más acumulación de normas porque es el dominio más dependiente de que todos los otros funcionen.

---

## Mapa de Dependencias Causales

La coherencia entre las 12 preguntas bautismales se puede leer como un sistema de dependencias:

```
PLANIFICACIÓN  ──→  SEGUIMIENTO  ──→  RENDICIÓN
    (D01)                (D03)             (D09)
      │                    │                 ↑
      │                    │                 │
      ▼                    ▼                 │
PRESUPUESTO  ──→  CONTRATACIÓN (D05)  ──→  ALERTAS
    (D02)        HOLDING MUNICIPAL          (D04)
      │                    │                 │
      │                    │                 │
      ▼                    ▼                 ▼
TERRITORIO   ──→  ECOSISTEMA  ──→  SALUD INSTITUCIONAL
  COBERTURA       PRODUCTIVO            (D06)
    (D10)            (D11)
      │
      ▼
TRANSPARENCIA  ──→  PARTICIPACIÓN  ──→  PROTECCIÓN SOCIAL
    (D07)               (D08)               (D12)
```

**Regla de lectura**: Una flecha `──→` indica dependencia causal directa: si el dominio origen falla, el dominio destino se verá afectado con alta probabilidad. No es determinístico — es estructural.

**Las tres cadenas críticas de Montecristi (evidencia actual):**

1. **Cadena Cobertura → Vulnerabilidad**: Dom10 (34.9% agua) → Dom12 (grupos prioritarios más vulnerables en zonas sin agua)
2. **Cadena Presupuesto → Ejecución**: Dom02 ($3.66M condicionado) → Dom05 (holding sin liquidez) → Dom12 (Patronato al 50%)
3. **Cadena Transparencia → Participación**: Dom07 (21 artículos LOTAIP) → Dom08 (27.98% participación, bajo objetivo 40%)

---

## Estado del Corpus QLEP por Dominio

| Dom | Nombre | N1 en corpus | N2 definida | Circuito QTMP | Layer 2 |
|---|---|---|---|---|---|
| 01 | Planificación Estratégica | ✅ CE_264, COOTAD_54 | ✅ este doc | ❌ pendiente | ❌ |
| 02 | Presupuesto & Financiamiento | ✅ COOTAD_215, COOTAD_198 | ✅ este doc | ✅ CONTROL_PREV cerrado | ❌ |
| 03 | Seguimiento de Metas | ✅ COOTAD_300, CE_241 | ✅ este doc | ❌ CPFP pendiente | ❌ |
| 04 | Alertas Institucionales | ✅ LOCCGE_12, NCI_600_01 | ✅ este doc | ✅ CONTROL_LEGAL cerrado | ❌ |
| 05 | Holding Municipal | 🟡 CE_315 parcial | ✅ este doc | ❌ LOEP pendiente | ❌ |
| 06 | Salud Institucional | ✅ CE_226, COOTAD_228 | ✅ este doc | ✅ EQUIDAD cerrado | ❌ |
| 07 | Transparencia | ✅ CE_18, LOTAIP completo | ✅ este doc | 🟡 YAML materializado · Neo4j pendiente S4 | ❌ pendiente Sprint 4 |
| 08 | Participación Ciudadana | ✅ COOTAD_304, COOTAD_302 | ✅ este doc | ✅ PARTICIPACION cerrado | ❌ |
| 09 | Rendición de Cuentas | ✅ COOTAD_302 | ✅ este doc | ❌ pendiente | ❌ |
| 10 | Territorio & Cobertura | ✅ CE_12, CE_264, COOTAD_137 | ✅ este doc | ✅ AGUA_POTABLE cerrado | ✅ p10_territorio.py |
| 11 | Ecosistema Productivo | ❌ pendiente F0.7-F0.8 | ✅ este doc | ❌ sin circuito | ❌ DISABLED |
| 12 | Protección Social | ✅ corpus más completo (F0.1-F0.5) | ✅ este doc | ✅ GAP_10PCT cerrado | ✅ p19_genero.py |

**Leyenda**: ✅ = completo · 🟡 = parcial · ❌ = pendiente

**Estado BETA-CORE al 2026-06-01** (ver ADR-014 para secuencia completa):

Completados N1-N5: Dom10 ✅ · Dom12 ✅  
Circuito QTMP + conector activo (Layer 2 pendiente): Dom02 · Dom04 · Dom06 · Dom07 · Dom08  
Sin circuito (corpus disponible): Dom01 · Dom03 · Dom09  
Bloqueado corpus F0.8: Dom05  
Fuera de MILESTONE_002: Dom11

**Brechas que bloquean los sprints pendientes**:
- Dom01: requiere CPFP + PDOT Montecristi (F0.7) para cadena causal PLANIFICACION — Sprint 9
- Dom03: requiere CPFP Art. 44 (F0.7) + Dom01 completo — Sprint 10
- Dom05: requiere atomización LOEP (F0.8) — Sprint 12
- Dom07: Neo4j load + Layer 2 — **Sprint 4** (YAML ✅, conector ✅)
- Dom09: depende Dom01+Dom03+Dom07 completos — Sprint 11
- Dom11: requiere corpus completo (F0.7-F0.8) antes de activar módulo

---

## Protocolo BETA-CORE — 5 Pasos por Dominio

Para cada uno de los 9 dominios sin circuito cerrado, el camino es:

```
N1 ✅  →  N2 ✅  →  N3 (Neo4j chain)  →  N4 (dato territorial)  →  N5 (C10 record)
                        QTMP               Gold Master              Connector
```

**Secuencia recomendada** (orden de esfuerzo mínimo-máximo, basado en estado corpus):

| Prioridad | Dom | Bloqueador | Próximo paso |
|---|---|---|---|
| 1 | Dom07 | Sin circuito — pero corpus LOTAIP completo | Diseñar pregunta QTMP: "¿publicó el numeral X este mes?" |
| 2 | Dom09 | Sin circuito — COOTAD_302 existe | Conectar COOTAD_302 → CPCCS checklist → resultado |
| 3 | Dom01 | CPFP pendiente — pero CE/COOTAD base existe | Atomizar CPFP Art. 44 (una sesión QLEP) |
| 4 | Dom03 | Depende de Dom01 | Después de Dom01 |
| 5 | Dom02 | Circuito parcial — datos SIGEF disponibles | Cerrar cadena CONTROL_PREV con dato real |
| 6 | Dom05 | LOEP pendiente | Atomizar LOEP Arts. 4, 22, 47 |
| 7 | Dom08 | Circuito cerrado pero Layer 2 pendiente | Construir Layer 2 con confianza.py |
| 8 | Dom11 | Corpus completo faltante | Último — primero activar módulo |
| 9 | Dom04 | Circuito cerrado | Construir Layer 2 con alertas.py |

---

## Garantías de Coherencia Inter-Dominio

Las 12 preguntas bautismales fueron definidas en una sola pasada para garantizar estas propiedades:

**1. No redundancia**: Ninguna pregunta puede ser respondida con el mismo circuito que otra.
- Dom01 y Dom03 se diferencian: Dom01 pregunta por capacidad de cumplir; Dom03 pregunta por causas del rezago.
- Dom07 y Dom09 se diferencian: Dom07 pregunta por disponibilidad de información; Dom09 por trazabilidad de compromisos.

**2. Cobertura completa**: Las 12 preguntas cubren el ciclo completo de gobernanza municipal:
```
Planificar (D01) → Presupuestar (D02) → Contratar/Ejecutar (D05) → Medir (D03/D06)
→ Transparentar (D07) → Participar (D08) → Rendir cuentas (D09) → Alertar (D04)
→ Cubrir territorio (D10) → Proteger vulnerables (D12) → Producir (D11)
```

**3. Principio de subsidiariedad**: Cada pregunta bautismal es la pregunta mínima suficiente — la que, si no tiene respuesta, hace imposible gobernar ese dominio. No es la única pregunta importante; es la fundacional.

**4. Coherencia normativa**: Ninguna N1 contradice otra N1. El sistema normativo ecuatoriano es coherente en el nivel constitucional. Las tensiones (si las hay) están en el nivel de desarrollo reglamentario, no en las normas primarias.

---

## Artefactos Derivados Pendientes

Una vez congelado este documento (v1.0), los siguientes artefactos se derivan en secuencia:

1. **9 ACK atoms nuevos** — para los dominios con corpus incompleto (Dom05 LOEP, Dom11 corpus completo)
2. **9 circuitos QTMP** — uno por dominio sin circuito cerrado
3. **9 instancias territoriales** — `qtmp_ECU-13-MONTECRISTI_[DOM]_MCR.yaml` para cada dominio
4. **9 Registros C10** — uno por dominio, siguiendo el schema definido en este documento
5. **9 Layer 2** — páginas Streamlit, construidas sobre C10 ya cerrado (no antes)

El orden es estricto. Un Layer 2 construido sin Registro C10 cerrado es una pantalla sin raíz.

---

## Versionado y Autoridad

| Campo | Valor |
|---|---|
| Documento | QLEP_CANONICO_MONTECRISTI_v1.0 |
| Estado | CONGELADO — requiere nueva versión para modificar N1 o N2 |
| Autoridad | QUIRA Operaciones / Dylus Lab |
| Fecha congelación | 2026-06-01 |
| Referencia cruzada | ADR-013 (mapeo QTMP↔Dominio) · QLEP v1.5 · QNKC-002 |
| Próxima revisión | v1.1 — solo si un error factual normativo es identificado |

**Regla de modificación**: Las preguntas bautismales no se modifican porque un indicador cambia. Se modifican solo si una reforma normativa cambia la competencia del GAD, o si un error en la identificación de la norma primaria es documentado con evidencia.

---

*QLEP v1.5 · QUIRA Gov · Dylus Lab © 2026 · Documento interno — clasificación QUIRA Operaciones*
