# DICCIONARIO CONCEPTUAL QUIRA — Fundación Ontológica de los 13 Cajones
**Sprint C · 2026-06-13 (actualizado 2026-06-14) · el documento fundacional · nivel estándar LAC (CAF/BID)**

> Antes de diseñar un solo dashboard, se define QUÉ representa cada dominio de
> gestión pública dentro de QUIRA. Una vez existe esto: los dashboards salen
> solos, las cosechas son evidentes, los 3 productos hablan el mismo idioma, y
> CAF/UEB/BID/municipios entienden QUIRA sin ver una pantalla. (Propuesta colega.)

## DOS REGLAS QUE GOBIERNAN ESTE DICCIONARIO

1. **Nivel conceptual, no operativo (colega · 2026-06-13).** La definición de un
   cajón describe el DOMINIO de gestión pública en abstracto — NO da ejemplos
   ("quién carga baldes", "$217", "Isabel Muentes"). Esos son casos que viven
   DENTRO del cajón, no su definición.
2. **Indicadores madre REALES, nunca inventados (Regla de Oro 3).** Los
   indicadores son los que el Gold Master CALCULA, con su nombre público de la
   Tabla de Equivalencias. PROHIBIDO inventar nombres grandilocuentes que no
   correspondan a una métrica real del motor (= motor paralelo alucinado).
   **Convención sellada (mesa · 2026-06-14): el indicador madre es el CONCEPTO en
   prosa (ej. "Acceso territorial a bienes públicos") — NUNCA "Índice de…".** Un
   "Índice" solo se nombra si el motor lo calcula con ese nombre propio (ICPI,
   IET, IGP), y entonces aparece como operativo, no inflando el madre.

## REGLA TERRITORIAL (Javo + colega · 2026-06-13 · arquitectónica)

> **Ningún cajón es territorial por sí mismo. Todos los cajones pueden
> territorializarse a través de GeoTwin.**

GeoTwin NO es un cajón (dominio) — es la **CAPA TRANSVERSAL de visualización e
inferencia territorial**. Los cajones responden *¿qué pasa?*; GeoTwin responde
*¿DÓNDE pasa?*. Arquitectura: **13 dominios de gestión + 1 capa territorial
transversal.** Cada cajón gana un botón "🛰️ Ver en Territorio (GeoTwin)" que
espacializa SU indicador. Es el mismo mapa mutando según el dominio activo.

(El concepto de cada cajón se expresa en UI de DOS formas: encabezado estático
breve "qué es" + QUIRA IA para la explicación profunda bajo demanda. El
Diccionario es la fuente única de ambas.)

## COSECHA ATÓMICA (Javo · 2026-06-13)

> La refactorización NO es por pantalla — es por SECCIONES/PARTES. Una sección,
> gráfica o componente de una pantalla antigua puede servir a un dominio, a otro,
> o a varios. Se cosecha parte por parte. Solo se CREA nuevo lo que falte para
> completar el interior del dominio.

```
[ PANTALLA CANTERA ]   →   [ SECCIÓN/COMPONENTE cosechado ]   →   [ DASHBOARD destino ]
```

---

## 🧬 NOMENCLÁTOR CANÓNICO (académico + mesa · 2026-06-14 · FUENTE ÚNICA de nombres)

> Un nombre oficial por cajón. El White Paper, CAF, GeoTwin, la Tabla de
> Equivalencias y el repo usan EL MISMO. El alias histórico preserva la
> trazabilidad documental y el mapeo al backend.

| # | Nombre Canónico (oficial · CAF) | Alias histórico / técnico (backend) |
|---|---|---|
| d01 | Planificación Estratégica | p11_ods · p8_metas |
| d02 | Presupuesto & Financiamiento | p18_cooperacion · radar_fondos |
| d03 | Gobernanza del Mandato | Metas PDOT·Mandato · promesas_cne |
| d04 | Alertas Institucionales | Sistema de Alerta Temprana (SAT) · m2_alertas |
| d05 | Holding e Integración Municipal | Holding/Ecosistema Municipal · p2_holding |
| d06 | Salud Institucional | Cumplimiento Institucional (ICPI) · m1_situacion |
| d07 | Transparencia | Transparencia Activa (LOTAIP) · p07_transparencia |
| d08 | Participación Ciudadana | Gobernanza Participativa · p16_gobernanza |
| d09 | Rendición de Cuentas | Circuito RDC Live · p17_rdc |
| d10 | Cobertura de Servicios e Infraestructura | Territorio & Cobertura · p10_territorio |
| d11 | Desarrollo Económico Territorial | Ecosistema Productivo Territorial (En Const.) |
| d12 | Inclusión, Equidad y Género | Protección Social & Género · p19_genero |

⚠️ **Pendiente de reconciliación al Nomenclátor** (propuesta, NO ejecutado aún): el
índice de la Constitución Ontológica (§12 dominios) y las referencias de la Hoja
de Ruta aún citan nombres previos (d03 "Mandato", d05 "Holding", d12 "Equidad y
Género"). Propagar en pase siguiente para no fracturar la ontología entre docs.
*(2026-06-14: Constitución + PLANO ya propagados · check 2.5 OK.)*

## 🗺️ MATRIZ MAESTRA — el índice de toda la ontología (colega · 2026-06-14)

> Capacidad (Capa 0.5) ↕ Dominio canónico ↕ Indicador madre (concepto) ↕
> Operativos REALES del motor ↕ Expresión GeoTwin. El mapa de una sola página de QUIRA.
>
> **Anclaje al motor + estado (LIVE/PENDIENTE/MISSING) por operativo → `docs/architecture/MAPA_ANCLAJE_MOTOR.md`.**

| # | Capacidad (0.5) | Dominio canónico | Indicador madre (concepto) | Operativos REALES (motor) | Expresión GeoTwin |
|---|---|---|---|---|---|
| d01 | Trayectoria | Planificación Estratégica | Cumplimiento de la planificación de desarrollo | Avance físico metas PDOT (4 ejes) | Cumplimiento territorial de metas |
| d02 | Movilización | Presupuesto & Financiamiento | Captación y eficiencia del gasto | Sostenibilidad (ISP) · eficiencia (IED) · ejecución (devengado) · elegibilidad (radar D02) | Inversión per cápita por parroquia |
| d03 | Fidelidad democrática | Gobernanza del Mandato | Congruencia promesa↔plan | Consistencia plan de campaña (IFE-A) | Promesas espacializadas (PUGS) |
| d04 | Anticipación | Alertas Institucionales | Riesgo operativo y legal activo | Cola del Sistema de Alerta Temprana | Pulsos de alerta geolocalizados |
| d05 | Articulación | Holding e Integración Municipal | Desempeño del ecosistema de entidades | Promedio de entidades | Entidades por ubicación |
| d06 | Sostenibilidad interna | Salud Institucional | Cumplimiento sostenible de funciones | Cumplimiento Institucional (ICPI) | Capacidad por sede/territorio |
| d07 | Verificabilidad | Transparencia | Apertura verificable de la información | Transparencia activa (LOTAIP 21/21) | Cumplimiento por entidad |
| d08 | Inteligencia colectiva | Participación Ciudadana | Incidencia de la ciudadanía | Gobernanza participativa (IGP) | Participación por parroquia |
| d09 | Responsabilidad pública | Rendición de Cuentas | Validación pública de la gestión | Estado del circuito de rendición (RDC) | Cobertura RDC territorial |
| d10 | Acceso colectivo | Cobertura de Servicios e Infraestructura | Acceso territorial a bienes públicos | Cobertura agua/saneamiento/recolección (INEC) · NBI (INEC) · Equidad Territorial (Gold Master) · inversión p.c. (eSIGEF) | Déficit estructural por polígono (NBI) |
| d11 | Dinamización | Desarrollo Económico Territorial | Capacidad productiva y de empleo del territorio | PEA / cadenas de valor (PDOT) | Tejido productivo territorial |
| d12 | Inclusión y equidad | Inclusión, Equidad y Género | Protección de los grupos prioritarios | Presupuesto con enfoque de género (PSG) | Geografía de la equidad (PSG × grupos) |
| d13 | Resiliencia | Sostenibilidad y Resiliencia Ambiental | Integridad ecológica y resiliencia del territorio | ODS ambientales (ICODS) · riesgo biofísico (PDOT) · conservación | Vulnerabilidad ecológica (riesgo × asentamientos) |

---

## 🔗 MATRIZ DE CONGRUENCIAS (Sprint D.0 · Modelo B · operacionaliza la Doctrina · mesa 2026-06-14)

> Cómo las 4 congruencias **leen los dominios** en las uniones de la Cadena Madre. Anclas VERIFICADAS contra
> `MAPA_ANCLAJE_MOTOR` — corregida la deriva del académico (d03 IFE-A vive en H73 + corpus, **NO** en H26/H31).

| Congruencia | Eslabón (Cadena Madre) | Dominios que lee | Indicador madre (concepto) | Ancla real (motor/corpus) | Estado |
|---|---|---|---|---|---|
| **Política** | Promesa → Plan | d03 · d01 | Congruencia promesa↔plan · cumplimiento de la planificación | IFE-A → `H73_OUTPUT_API` + corpus promesas CNE/PDOT (Supabase) · metas PDOT → `H11b`·`H12c` | ✅ LIVE |
| **Operativa** | Plan → Presupuesto → Ejecución | d02 · d04 · d05 · d06\* | captación/eficiencia del gasto · riesgo activo · cumplimiento institucional | ISP·IED → `H73` · SAT → `H75`/`H24` · entidades → `H12d` · ICPI → `H73`·`H12` *(cimiento)* · devengado → `H07_S5` | ⏳ MEDIO (eSIGEF 2026) |
| **Territorial** | Ejecución → Resultado → Territorio | d10 · d11 | acceso territorial a bienes públicos · capacidad productiva | agua → QTMP · NBI/saneam. → INEC/loader · IET → `H73` · inversión → `H07b` · PEA/cadenas → corpus PDOT | ✅ LIVE *(d11 corpus)* |
| **Ecosistémica** | Territorio → Sostenibilidad | d12 · d13 | protección de grupos prioritarios · integridad ecológica | PSG → `H73` · brechas → corpus · biofísico 362 + riesgo `KB_RIESGOS` · ICODS sub-eje ⚠️ | 🟡 LIVE parcial *(IGM/ODS5 MISSING · ICODS-amb a precisar)* |

\* **d06 entra como CIMIENTO** (no se promedia) — la Congruencia Operativa lo lee como base.
**Capa de verificación:** d07 · d08 · d09 **auditan cada unión** (¿la congruencia es verificable públicamente?).

**El diferencial QUIRA (causa, no síntoma):** un BI dice *"60% de ejecución"*. QUIRA dice *"Congruencia Operativa en
saldo negativo: el presupuesto está devengado en papel, pero el Cumplimiento Institucional (d06) está bajo y las obras
viales (d04 SAT) están frenadas"*. → UX: 4 barras de tensión = **"Sensores de Presión del Estado"** (clic → zoom relacional al cajón).

> ⚠️ **ESTADO (Javo · 2026-06-14):** esta Matriz es el MARCO METODOLÓGICO correcto, pero las 4 congruencias **NO están
> formalizadas en el Excel canónico** (son el espíritu de las tesis anteriores, nunca aterrizado). Los anclajes de la
> tabla son los indicadores que las congruencias *leerían* — la congruencia en sí **aún no se calcula en el motor.**
> Pendiente: formalizarla en el Gold Master (Javo) o reubicarla en QUIRA IA (C3). Hasta entonces = capa conceptual, NO dato.

---

## 🧱 LA PLANTILLA MADRE — 11 CAMPOS (estándar definitivo · post Capa 0.5)

Todo ADN se redacta con estos 11 campos, en este orden (Cajón 10 = molde):

1. **Capacidad Universal** (Capa 0.5) — el poder del Estado que se evalúa.
2. **Dominio Canónico** (Capa 1) — el nombre oficial del Nomenclátor.
3. **Alias histórico / técnico** — trazabilidad documental y backend.
4. **Definición conceptual abstracta** — el dominio en abstracto, sin ejemplos.
5. **Propósito institucional** — para qué sirve.
6. **Pregunta estratégica** — la pregunta epistemológica que responde.
7. **Alcance** — qué incluye.
8. **Exclusiones** — qué NO incluye (y a qué cajón va).
9. **Data central** — la materia prima.
10. **Indicador madre (concepto) + operativos REALES + ancla motor** — concepto arriba; métricas del motor abajo; cada operativo con su hoja del Gold Master y estado (LIVE/PENDIENTE/MISSING · ver `MAPA_ANCLAJE_MOTOR.md`).
11. **Expresión GeoTwin** (Capa 3) — cómo se espacializa la capacidad.

---

## 📁 CAJÓN 10 · COBERTURA DE SERVICIOS E INFRAESTRUCTURA  (plantilla madre · re-sellada 11 campos · anclada · 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Acceso Colectivo** — garantizar la distribución equitativa de infraestructura, servicios básicos y conectividad física sobre el suelo cantonal. |
| 2 | **Dominio Canónico** | Cobertura de Servicios e Infraestructura *(antes "Territorio & Cobertura" — el mapa pasó a GeoTwin transversal)* |
| 3 | **Alias histórico / técnico** | Territorio & Cobertura · p10_territorio |
| 4 | **Definición conceptual** | Dimensión de efectividad material e impacto sectorial de la política pública: la distribución física y el nivel de penetración de las redes de servicios esenciales y bienes públicos sobre el mapa cantonal. |
| 5 | **Propósito** | Cuantificar el déficit estructural de infraestructura y medir la equidad en el abastecimiento público para orientar la inversión hacia las zonas prioritarias. |
| 6 | **Pregunta estratégica** | ¿Cuál es la magnitud real del déficit de servicios básicos por parroquia y en qué medida las intervenciones mitigan la brecha urbano-rural? |
| 7 | **Alcance (incluye)** | Acceso a agua por red, alcantarillado, saneamiento, recolección de desechos, electrificación y conectividad física por polígono. |
| 8 | **Exclusiones (no incluye)** | Presupuestos globales de obras (→ d02) · contratos de fiscalización (→ d07) · capacidad del personal técnico (→ d06) · la representación espacial/mapa (→ GeoTwin transversal). |
| 9 | **Data central** | Matriz viva de cobertura sectorial parroquial + capas de delimitación geográfica del PUGS. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Acceso territorial a bienes públicos. **Operativos REALES:** Cobertura de agua por red pública (% · INEC) · Cobertura de saneamiento (% · INEC) · Cobertura de recolección de desechos (% · INEC) · Pobreza por NBI (INEC) · Equidad Territorial (Gold Master) · Inversión per cápita por parroquia (eSIGEF). **Ancla motor:** IET → `H73_OUTPUT_API` ✅ · inversión p.c. → `H07b_Ti_INVERSIÓN_eSIGEF` (27/30) ✅ · agua/saneamiento/NBI → INEC·QTMP·loader ✅ **LIVE**. |
| 11 | **Expresión GeoTwin (Capa 3)** | **Déficit estructural:** extrusión volumétrica 3D de los polígonos parroquiales según NBI; cruza el diagnóstico base del PDOT con los proyectos ejecutados, encendiendo gradientes rojos en las coordenadas de las comunidades excluidas. |

### Plano de cosecha atómica — Cajón 10 (VERIFICADO contra pantallas reales · 2026-06-14)
> Inventario real (leyendo el código, no adivinando). El test de falsación cazó un mapeo falso
> y dos huecos — la ontología sobrevivió; el plano se corrige (no se fuerza nada).

| Pantalla cantera | Componente REAL | Indicador → ancla | Veredicto |
|---|---|---|---|
| p10_territorio | KPI agua + semáforo + barras de escenarios | Cobertura agua potable → QTMP AGUA_POTABLE (Neo4j) ✅ LIVE | 🅰️ encaja en d10 |
| p10_inversion | Barras inversión per cápita por parroquia + brecha 5.4× | Inversión p.c. · IET · brecha → `data.loader` ✅ LIVE | 🅰️ encaja en d10 |
| p10_inversion | `EJES_INVERSION` (distribución sectorial) | Presupuesto por sector → ⚠️ HARDCODED | 🅱️ dato de **d02**, no d10 |
| ~~p7_brecha~~ | 6 vectores causales del ICGI-T (ISP·IED·IGP·IOC·IET·PSG) | ICPI + vectores → `data.loader` | 🅲 **es d06, NO d10** (el plano lo asignó mal) |
| (ninguna) | saneamiento · recolección de desechos | prometidos en el ADN | 🅲 **sin pantalla cantera** (concepto sin evidencia hoy) |

**Veredicto del piloto:** el núcleo de d10 (agua + equidad territorial) SÍ se alimenta de pantallas reales con anclas reales (Tipo A). El test cazó: `p7_brecha` mal asignada (→ va a la cosecha de **d06**) · saneamiento/recolección sin pantalla (Tipo C, huecos a llenar) · `EJES_INVERSION` = material de d02 + hardcoded (Tipo B). **La ontología no se fuerza: se corrige.**

**Dashboards finales: 1** — Tablero de Cobertura & Brecha + botón "🛰️ Ver en Territorio (GeoTwin)".
*(El mapa ya NO es dashboard del Cajón 10 — es la capa transversal · ver §GeoTwin abajo.)*

---

## 📁 CAJÓN 01 · PLANIFICACIÓN ESTRATÉGICA  (ADN anclado · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Trayectoria** — convertir la intención política y los lineamientos legales en objetivos de desarrollo estables y metas de cumplimiento medibles en el tiempo. |
| 2 | **Dominio Canónico** | Planificación Estratégica |
| 3 | **Alias histórico / técnico** | p11_ods · p8_metas |
| 4 | **Definición conceptual** | Dimensión de direccionamiento y gobernanza de largo plazo: la consistencia de la programación plurianual frente a los hitos de cumplimiento establecidos en las herramientas de planificación nacional y territorial. |
| 5 | **Propósito** | Medir de forma continua el avance físico de los objetivos estratégicos del gobierno para corregir desvíos antes de la parálisis del plan institucional. |
| 6 | **Pregunta estratégica** | ¿El aparato público mantiene un rumbo consistente hacia las metas plurianuales comprometidas o sufre desviaciones en sus ejes estratégicos? |
| 7 | **Alcance (incluye)** | Metas físicas del PDOT, hitos temporales de proyectos estratégicos y ponderación de alineación con los ODS. |
| 8 | **Exclusiones (no incluye)** | Montos devengados o flujo de caja (→ d02) · contratos en portales (→ d07) · compromisos discursivos de campaña no normados (→ d03). |
| 9 | **Data central** | Matriz consolidada de hitos y metas físicas por componente de desarrollo. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Cumplimiento de la planificación de desarrollo. **Operativos REALES:** Avance físico de metas PDOT (4 ejes oficiales). **Ancla motor:** `H11b_MONITOR_POLITICAS` (41/47) · `H12c_ICPI_HISTÓRICO` · corpus METAS_PDOT (Supabase) → ✅ **LIVE** *(conexión a TGI D1/D2 = auditoría de fórmulas, diferida)*. |
| 11 | **Expresión GeoTwin (Capa 3)** | **Cumplimiento territorial:** mapas temáticos donde las capas base de diagnóstico del PDOT (biofísico, movilidad…) se intersectan con los % de avance del plan; tiñe parroquias según el rezago de metas sectoriales, mostrando dónde la planificación no se materializó. |

---

## 📁 CAJÓN 02 · PRESUPUESTO & FINANCIAMIENTO  (ADN anclado · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Movilización** — captar, gestionar, optimizar y distribuir recursos financieros y de cooperación de forma eficiente, oportuna y fiscalmente sostenible. |
| 2 | **Dominio Canónico** | Presupuesto & Financiamiento |
| 3 | **Alias histórico / técnico** | p18_cooperacion · radar_fondos |
| 4 | **Definición conceptual** | Dimensión de viabilidad, flujo y asignación de los recursos públicos: el comportamiento de la ingeniería financiera institucional frente a los compromisos de gasto y el apalancamiento de capital externo. |
| 5 | **Propósito** | Garantizar la sostenibilidad fiscal, minimizar el volumen de fondos en riesgo y maximizar el espacio fiscal disponible para financiar el desarrollo. |
| 6 | **Pregunta estratégica** | ¿Con qué eficiencia, oportunidad y viabilidad se movilizan y ejecutan los recursos frente a la capacidad de captación y el riesgo de subejecución? |
| 7 | **Alcance (incluye)** | Cédulas presupuestarias (codificado vs devengado), sostenibilidad y liquidez, eficiencia del gasto por dirección, y elegibilidad/riesgo de fondos de cooperación (radar D02). |
| 8 | **Exclusiones (no incluye)** | Avance físico de las metas que el presupuesto financia (→ d01) · contratación pública específica y su apertura (→ d07) · cobertura material resultante en el territorio (→ d10). |
| 9 | **Data central** | Cédulas de ejecución eSIGEF + matriz de elegibilidad del radar D02. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Captación y eficiencia del gasto. **Operativos REALES:** Sostenibilidad presupuestaria (ISP) · Eficiencia de gestión (IED) · Ejecución presupuestaria (devengado) · Elegibilidad/fondos en riesgo. **Ancla motor:** ISP·IED → `H73_OUTPUT_API` ✅ LIVE · elegibilidad → Supabase `fondos_*` ✅ LIVE · ejecución devengado → `H07_S5_FINANCIERO_eSIGEF` (zona 2026 cruda) ⏳ **PENDIENTE** (CHK-08, cédula eSIGEF 2026). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Inversión territorializada:** prismas de inversión per cápita por parroquia (eSIGEF) — la altura = gasto devengado por habitante, desnudando las asimetrías de asignación financiera sobre el suelo. |

---

## 📁 CAJÓN 03 · GOBERNANZA DEL MANDATO  (ADN anclado · el sello QUIRA · mesa 2026-06-14)

> **Primer dominio donde la Doctrina se vuelve visible.** Trabaja el eslabón
> **PROMESA↔PLAN** de la cadena madre — lo que separa a QUIRA de un BI: ningún
> dashboard tradicional pregunta si la planificación sigue fiel al mandato ciudadano.
> Aterriza el diferencial epistemológico para CAF/BID/CEPAL/PNUD.

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Fidelidad Democrática** — mantener la coherencia y la integridad entre la palabra empeñada ante el soberano (el cuerpo electoral) y la acción normativa formalizada por el Estado. |
| 2 | **Dominio Canónico** | Gobernanza del Mandato |
| 3 | **Alias histórico / técnico** | Metas PDOT·Mandato · promesas_cne |
| 4 | **Definición conceptual** | Dimensión de correspondencia de origen y consistencia democrática: la degradación o persistencia de la oferta de campaña inscrita legalmente, una vez procesada por las estructuras burocráticas y los planes plurianuales del gobierno local. |
| 5 | **Propósito** | Garantizar que la voluntad popular que legitimó al gobierno se mantenga como eje rector del planeamiento, blindando la gestión contra desvíos programáticos u omisiones selectivas. |
| 6 | **Pregunta estratégica** | ¿La planificación institucional mantiene su integridad y correspondencia respecto a los compromisos originales validados por la ciudadanía en las urnas? |
| 7 | **Alcance (incluye)** | Ofertas de campaña inscritas formalmente ante el CNE, objetivos del plan de trabajo de la autoridad, metas del PDOT, y la matriz de trazabilidad CNE↔PDOT. *(El NLP del discurso en RDC = capa diferenciadora DISEÑADA · Sprint E · depende de créditos API · no operativa hoy.)* |
| 8 | **Exclusiones (no incluye)** | Ejecución presupuestaria financiera (→ d02) · presupuesto participativo (→ d08) · estado del circuito formal ante el CPCCS (→ d09). |
| 9 | **Data central** | Matriz de trazabilidad Plan de Trabajo (CNE) ↔ Objetivos Estratégicos (PDOT). |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Congruencia promesa↔plan. **Operativos REALES:** Consistencia del plan de campaña (IFE-A · 48/66 promesas CNE→PDOT). **Ancla motor:** IFE-A → `H73_OUTPUT_API` (consolidado) + corpus promesas CNE/PDOT (Supabase C1) → ✅ **LIVE**. *(Fidelidad de ejecución IFE-E → eSIGEF → ⏳ PENDIENTE Q2-2026.)* |
| 11 | **Expresión GeoTwin (Capa 3)** | **Promesas espacializadas:** los compromisos geográficos de campaña frente a las zonas de intervención real (PUGS) — qué promesas locales se formalizaron en obra y cuáles se omitieron de la geografía del desarrollo cantonal. |

---

## 📁 CAJÓN 04 · ALERTAS INSTITUCIONALES  (ADN anclado · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Anticipación** — detectar el riesgo operativo y legal antes de que se convierta en crisis. |
| 2 | **Dominio Canónico** | Alertas Institucionales |
| 3 | **Alias histórico / técnico** | Sistema de Alerta Temprana (SAT) · m2_alertas |
| 4 | **Definición conceptual** | Dimensión de vigilancia preventiva: el sistema de detección temprana que identifica desviaciones, incumplimientos y exposiciones de riesgo institucional antes de que escalen. |
| 5 | **Propósito** | Anticipar y priorizar los riesgos operativos y legales activos para habilitar la corrección preventiva, no la reacción tardía. |
| 6 | **Pregunta estratégica** | ¿Qué riesgos institucionales están activos hoy, con qué severidad, y cuáles exigen intervención antes de volverse crisis? |
| 7 | **Alcance (incluye)** | Metas sin respaldo de contratación (PAC), indicadores bajo umbral crítico, desvíos de participación y liquidez, y la cola priorizada de alertas activas. |
| 8 | **Exclusiones (no incluye)** | La causa presupuestaria de fondo (→ d02) · el cumplimiento institucional que las alertas alimentan (→ d06) · la rendición formal del riesgo (→ d09). |
| 9 | **Data central** | Cola priorizada del Sistema de Alerta Temprana + matriz de severidad por tipo de riesgo. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Riesgo operativo y legal activo. **Operativos REALES:** Cola del Sistema de Alerta Temprana (SAT-0 · SAT-IV · SAT-V). **Ancla motor:** `H75_SAT_ENGINE` (14/14) · `H24_SAT-IV` (15/20) → ✅ **LIVE** · matriz de riesgo (4 categorías) → demo_data → ⚠️ HARDCODED (conectar a snapshot `H75`). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Pulsos de alerta geolocalizados:** los riesgos activos encendidos sobre la infraestructura crítica del cantón. |

---

## 📁 CAJÓN 05 · HOLDING E INTEGRACIÓN MUNICIPAL  (ADN anclado · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Articulación** — gobernar el ecosistema de entidades y empresas públicas del cantón como un conjunto coherente. |
| 2 | **Dominio Canónico** | Holding e Integración Municipal |
| 3 | **Alias histórico / técnico** | Holding/Ecosistema Municipal · p2_holding |
| 4 | **Definición conceptual** | Dimensión de gobernanza corporativa territorial: el desempeño agregado y la coordinación del conjunto de entidades, empresas públicas y unidades adscritas que ejecutan la gestión cantonal. |
| 5 | **Propósito** | Medir la salud y la articulación del ecosistema institucional para evitar que la fragmentación entre entidades degrade el resultado conjunto. |
| 6 | **Pregunta estratégica** | ¿El conjunto de entidades del cantón opera de forma articulada y con desempeño consistente, o hay piezas que arrastran al sistema? |
| 7 | **Alcance (incluye)** | Desempeño comparado de las entidades y empresas públicas adscritas, su contribución al cumplimiento institucional y su grado de integración. |
| 8 | **Exclusiones (no incluye)** | El cumplimiento de la entidad matriz aislada (→ d06) · la ejecución presupuestaria de cada entidad (→ d02) · la transparencia individual (→ d07). |
| 9 | **Data central** | Matriz de desempeño por entidad del ecosistema municipal. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Desempeño del ecosistema de entidades. **Operativos REALES:** Promedio de desempeño de entidades. **Ancla motor:** `H12d_ICPI_POR_ENTIDAD` (19/24) → ✅ **LIVE**. |
| 11 | **Expresión GeoTwin (Capa 3)** | **Entidades por ubicación:** el mapa de las unidades del ecosistema y su desempeño territorial. |

---

## 📁 CAJÓN 06 · SALUD INSTITUCIONAL  (ADN anclado · indicador de cabecera · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Sostenibilidad interna** — cumplir las funciones públicas de forma consistente, eficiente y sostenible en el tiempo. |
| 2 | **Dominio Canónico** | Salud Institucional |
| 3 | **Alias histórico / técnico** | Cumplimiento Institucional (ICPI) · m1_situacion |
| 4 | **Definición conceptual** | Dimensión sintética de la salud del aparato público: la capacidad de la organización de sostener el cumplimiento de sus funciones combinando eficiencia, sostenibilidad financiera, observancia, participación y equidad. |
| 5 | **Propósito** | Ofrecer la lectura integral del estado institucional — el indicador de cabecera que sintetiza los vectores causales en una sola señal de salud. |
| 6 | **Pregunta estratégica** | ¿El gobierno local cumple sus funciones de forma sostenible y consistente, o hay un deterioro estructural en su capacidad institucional? |
| 7 | **Alcance (incluye)** | El cumplimiento institucional global, su composición por vectores causales y su evolución histórica. |
| 8 | **Exclusiones (no incluye)** | El detalle operativo de cada vector, que vive en su dominio (presupuesto → d02 · transparencia → d07 · participación → d08 · equidad → d12) · las alertas que lo amenazan (→ d04). |
| 9 | **Data central** | Score de cumplimiento institucional + su descomposición por vectores + serie histórica. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Cumplimiento sostenible de funciones. **Operativos REALES:** Cumplimiento Institucional (ICPI) + sus 6 vectores (ISP·IED·IGP·IOC·IET·PSG) + histórico. **Ancla motor:** `H73_OUTPUT_API` → `ICPI_GLOBAL` · `H12_MOTOR_ICPI` · `H12c_ICPI_HISTÓRICO` (2023-25) → ✅ **LIVE** *(ICPI 2026 vivo depende de `T_i_2026`/eSIGEF 2026 → ⏳ CHK-08)*. **NUNCA recalcular — solo leer (Regla 1).** |
| 11 | **Expresión GeoTwin (Capa 3)** | **Capacidad por sede/territorio:** la salud institucional proyectada sobre las unidades territoriales. |

### Plano de cosecha atómica — Cajón 06 (VERIFICADO contra pantallas reales · 2026-06-14)
> d06 valida la TEORÍA (no solo el método). Hallazgo mayor: **d06 es un dominio SÍNTESIS** — sus pantallas
> ejecutivas son cross-domain por NATURALEZA, no por error. La teoría aguantó y se explicó a sí misma.

| Pantalla cantera | Componente REAL | Indicador → ancla | Veredicto |
|---|---|---|---|
| p_ejecutivo (tab) | TGI/ICPI/Riesgo headline + estado + Q&A autoridad | ICPI/TGI/SAT → **SNAPSHOT vivo** (cache_quira·sentinel·GM v5.5) | 🅰️ d06 núcleo · LIVE pipeline |
| p_ejecutivo | Semáforos por entidad (GAD·BOMBEROS·EMAI·PATRONATO) | Ti ejecución por entidad | 🅱️ es **d05 Holding** |
| p_ejecutivo | Señales SAT (SAT-0..VIII) + SLA institucional | alertas activas | 🅱️ es **d04 Alertas** |
| p7_brecha (tab) | 6 vectores del ICPI (ISP·IED·IGP·IOC·IET·PSG) + ICGI-T + AVEP | data.loader + ⚠️ vectores **HARDCODED** | 🅰️ d06 (la causalidad) · ⚠️ valores fijos |
| p6_pulso (tab) | **4 congruencias** (política·operativa·territorial·ecosistémica) | data.loader | 🅲 **concepto SIN hogar** en los 13 ADN |
| p6_pulso | alertas·riesgo·holding·IET·PSG | data.loader (demo) | 🅱️ cross-domain + ruta de datos ≠ p_ejecutivo |

**Veredicto del piloto d06:** la TEORÍA se sostuvo. (1) 🅰️ el ICPI núcleo se alimenta de un snapshot REAL del
pipeline (no inventado). (2) 🅲 **d06 = SÍNTESIS**: el ICPI es el CIMIENTO y los índices superiores se posan ENCIMA cruzándolo — NUNCA lo promedian (Regla 1 · síntesis por RELACIÓN, no por promedio); sus vectores enlazan a otros cajones
(ISP→d02 · IGP→d08 · IOC→d07 · IET→d10 · PSG→d12). Su dashboard se diseña como **mapa de causalidad que enlaza
a los otros**, no como pantalla aislada. Confirma ADR-026 (d06 = Sintetizador), no lo rompe. (3) 🅱️ DOS rutas
de datos a unificar (p_ejecutivo snapshot/sentinel vivo vs p6_pulso data.loader demo) + 6 vectores hardcoded en
p7_brecha → cablear al conector canónico. (4) ✅ **4 congruencias = Capa de Congruencia (sellada en Constitución · lectura relacional sobre el cimiento ICPI)** (política/operativa/territorial/
ecosistémica): NO es dominio nuevo (no dispara Protocolo) · candidata = expresión de la Doctrina "congruencia"
a nivel macroeje · **decisión de mesa**.

---

## 📁 CAJÓN 07 · TRANSPARENCIA  (ADN anclado · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Verificabilidad** — hacer auditable y verificable la acción pública ante cualquier observador. |
| 2 | **Dominio Canónico** | Transparencia |
| 3 | **Alias histórico / técnico** | Transparencia Activa (LOTAIP) · p07_transparencia |
| 4 | **Definición conceptual** | Dimensión de apertura verificable: el grado en que la información pública es accesible, oportuna, completa y consistente, de modo que la gestión pueda ser auditada por la ciudadanía y los órganos de control. |
| 5 | **Propósito** | Cuantificar la apertura real (no declarativa) de la información pública para que la verificación ciudadana sea posible y la opacidad quede expuesta. |
| 6 | **Pregunta estratégica** | ¿La información pública del cantón es accesible, oportuna y consistente de forma verificable, o hay opacidad que impide auditar la gestión? |
| 7 | **Alcance (incluye)** | Cumplimiento formal de la LOTAIP (21 artículos), accesibilidad del portal, oportunidad temporal y consistencia de la información publicada. |
| 8 | **Exclusiones (no incluye)** | La participación que la transparencia habilita (→ d08) · la rendición formal de cuentas (→ d09) · la contratación específica como dato presupuestario (→ d02). |
| 9 | **Data central** | Matriz de cumplimiento LOTAIP 21/21 + métricas de accesibilidad/oportunidad/consistencia. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Apertura verificable de la información. **Operativos REALES:** Transparencia activa (LOTAIP 21/21) · accesibilidad · oportunidad (DPE) · Observancia Contractual (IOC). **Ancla motor:** QTMP (Neo4j) C4/C5 · `H73_OUTPUT_API` (IOC) → ✅ **LIVE**. |
| 11 | **Expresión GeoTwin (Capa 3)** | **Cumplimiento por entidad:** la apertura proyectada sobre las unidades del ecosistema. |

---

## 📁 CAJÓN 08 · PARTICIPACIÓN CIUDADANA  (ADN anclado · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Inteligencia colectiva** — incorporar la voz ciudadana a la decisión pública. |
| 2 | **Dominio Canónico** | Participación Ciudadana |
| 3 | **Alias histórico / técnico** | Gobernanza Participativa · p16_gobernanza |
| 4 | **Definición conceptual** | Dimensión de incidencia ciudadana: el grado en que los mecanismos de participación efectivamente influyen en las decisiones públicas, más allá de su existencia formal. |
| 5 | **Propósito** | Medir la incidencia real de la ciudadanía en la gestión — cuántos mecanismos funcionan y qué territorios quedan sin voz. |
| 6 | **Pregunta estratégica** | ¿La ciudadanía incide realmente en las decisiones públicas, y qué territorios o grupos quedan sin canal de participación? |
| 7 | **Alcance (incluye)** | Mecanismos de participación activos (presupuesto participativo, sillas, audiencias), aportes ciudadanos procesados, y cobertura territorial de la voz. |
| 8 | **Exclusiones (no incluye)** | La transparencia que habilita la participación (→ d07) · la rendición formal ante el CPCCS (→ d09) · la equidad de los grupos prioritarios (→ d12). |
| 9 | **Data central** | Matriz de mecanismos de participación + aportes + cobertura parroquial de la voz. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Incidencia de la ciudadanía. **Operativos REALES:** Gobernanza participativa (IGP) · parroquias sin voz · aportes de presupuesto participativo · resultado CPCCS. **Ancla motor:** `H73_OUTPUT_API` (IGP) · `H10c_RDC_APORTES` (132/134) · `H31_REPORTE_CPCCS` (58/65) → ✅ **LIVE**. |
| 11 | **Expresión GeoTwin (Capa 3)** | **Participación por parroquia:** el mapa de dónde la ciudadanía incide y dónde no tiene voz. |

---

## 📁 CAJÓN 09 · RENDICIÓN DE CUENTAS  (ADN anclado · dominio terminal · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Responsabilidad pública** — someter la gestión al control social y validarla públicamente. |
| 2 | **Dominio Canónico** | Rendición de Cuentas |
| 3 | **Alias histórico / técnico** | Circuito RDC Live · p17_rdc |
| 4 | **Definición conceptual** | Dimensión de validación pública: el estado del proceso formal por el cual la gestión se somete al control social y al órgano rector, integrando la evidencia de todos los demás dominios. |
| 5 | **Propósito** | Verificar que el gobierno cierra el ciclo democrático rindiendo cuentas con evidencia, no con autorreporte — el dominio terminal que consolida la responsabilidad. |
| 6 | **Pregunta estratégica** | ¿El gobierno cierra el ciclo de responsabilidad pública con evidencia verificable, o la rendición es formal y autorreportada? |
| 7 | **Alcance (incluye)** | Estado del circuito de rendición de cuentas, su checklist de requisitos, el resultado ante el CPCCS y el calendario del proceso. |
| 8 | **Exclusiones (no incluye)** | Los datos de origen que la rendición consolida (viven en sus dominios) · la participación que la alimenta (→ d08) · la transparencia que la sostiene (→ d07). |
| 9 | **Data central** | Estado del circuito RDC + checklist de cumplimiento + resultado CPCCS. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Validación pública de la gestión. **Operativos REALES:** Estado del circuito de rendición (RDC) · resultado CPCCS · aportes consolidados. **Ancla motor:** `H73_OUTPUT_API` (RDC_SCORE) · `H10c_RDC_APORTES` (132/134) · `H31_REPORTE_CPCCS` (58/65) · circuito C-RDC (Neo4j) → ✅ **LIVE**. |
| 11 | **Expresión GeoTwin (Capa 3)** | **Cobertura RDC territorial:** el alcance de la rendición proyectado sobre el cantón. |

---

## 📁 CAJÓN 11 · DESARROLLO ECONÓMICO TERRITORIAL  (ADN anclado · campo verde · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Dinamización** — potenciar el tejido productivo y el empleo del territorio. |
| 2 | **Dominio Canónico** | Desarrollo Económico Territorial |
| 3 | **Alias histórico / técnico** | Ecosistema Productivo Territorial · (En Const.) |
| 4 | **Definición conceptual** | Dimensión de vitalidad económica del territorio: la capacidad del cantón de sostener producción, empleo, cadenas de valor y relevo generacional en su base productiva. |
| 5 | **Propósito** | Caracterizar el tejido económico territorial y sus brechas (empleo, cadenas, materialización de proyectos) para orientar la política de dinamización productiva. |
| 6 | **Pregunta estratégica** | ¿El territorio sostiene un tejido productivo dinámico y con empleo, o arrastra brechas estructurales (informalidad, relevo generacional roto, proyectos no materializados)? |
| 7 | **Alcance (incluye)** | PEA y empleo, cadenas de valor y vocación productiva, tenencia y uso económico del suelo, y el estado de materialización de los proyectos estratégicos. *(Estado de materialización planificado vs construido = dimensión candidata · G-27.)* |
| 8 | **Exclusiones (no incluye)** | La cobertura de servicios e infraestructura física (→ d10) · el presupuesto que financia la inversión (→ d02) · la equidad de los grupos prioritarios (→ d12). |
| 9 | **Data central** | Caracterización económica territorial extraída del PDOT (corpus) + indicadores de empleo/PEA. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Capacidad productiva y de empleo del territorio. **Operativos REALES:** PEA · cadenas de valor · relevo generacional agro (PDOT). **Ancla motor:** corpus PDOT económico (139 indicadores · Supabase C1) → ✅ **LIVE (corpus)**. ⚠️ **SIN hoja GM dedicada** — el motor aún NO calcula un indicador madre económico (campo verde · candidato a futura métrica del Gold Master · NO inventar hoy). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Tejido productivo territorial:** la actividad económica, las cadenas y los proyectos (materializados vs estancados) proyectados sobre el suelo. |

---

## 📁 CAJÓN 12 · INCLUSIÓN, EQUIDAD Y GÉNERO  (ADN anclado · PD-GEN-01 · mesa 2026-06-14)

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Inclusión y equidad** — proteger y garantizar los derechos de los grupos de atención prioritaria. |
| 2 | **Dominio Canónico** | Inclusión, Equidad y Género |
| 3 | **Alias histórico / técnico** | Protección Social & Género · p19_genero |
| 4 | **Definición conceptual** | Dimensión de equidad y protección: la capacidad del Estado de garantizar derechos y cerrar brechas de los grupos de atención prioritaria, primariamente sobre el territorio (PD-GEN-01: 80% territorial / 20% institucional). |
| 5 | **Propósito** | Medir la equidad institucional (presupuesto con enfoque de género) y las brechas territoriales de los grupos prioritarios, para orientar la protección hacia donde la brecha duele. |
| 6 | **Pregunta estratégica** | ¿El gobierno protege a los grupos de atención prioritaria con presupuesto real y cierra las brechas territoriales donde la vulnerabilidad se concentra? |
| 7 | **Alcance (incluye)** | Presupuesto con enfoque de género (capacidad institucional · 20%) y las brechas territoriales de los grupos prioritarios (violencia, cuidados, empleo, jefatura femenina · 80% · vía PDOT). *(PD-GEN-01.)* |
| 8 | **Exclusiones (no incluye)** | La participación ciudadana general (→ d08) · la cobertura de servicios básicos no desagregada por grupo (→ d10) · el presupuesto global (→ d02). |
| 9 | **Data central** | Presupuesto con enfoque de género + matriz de brechas territoriales de grupos prioritarios (PDOT). |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Protección de los grupos prioritarios. **Operativos REALES:** Presupuesto con enfoque de género (PSG) · brechas territoriales (violencia/cuidados/empleo). **Ancla motor:** PSG → `H73_OUTPUT_API` (`PSG_EJECUCION`) → ✅ **LIVE** · brechas territoriales → corpus PDOT (Supabase) → ✅ LIVE. ❌ **MISSING** (externos · gestión cooperación): IGM-A/B (RRHH/DAF) · IGM-C (PNUD/INEC) · IGM-F (CNE) · ODS 5.x (6/6 · PNUD/SENPLADES). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Geografía de la equidad:** el PSG y los grupos prioritarios cruzados con la densidad de vulnerabilidad territorial — el **Pin Morado** de PD-GEN-01. |

---

## 📁 CAJÓN 13 · SOSTENIBILIDAD Y RESILIENCIA AMBIENTAL  (ADN anclado · 1er ejercicio de Mutabilidad · escudo ESG · mesa 2026-06-14)

> **Primer dominio anexado vía la Declaración de Mutabilidad.** Da casa al dato
> biofísico huérfano (362 indicadores · Sprint B) y completa el ESG material del
> Macroeje 4. Gemelo de género (d12) en cooperación: ambos son los mayores imanes
> de financiamiento climático/social (Banco Verde CAF). Pasó el gate (capacidad
> distinta + data huérfana propia).

| # | Campo | Contenido |
|---|---|---|
| 1 | **Capacidad Universal (0.5)** | **Resiliencia** — proteger el patrimonio natural, mitigar el cambio climático y adaptar el territorio ante riesgos biofísicos y ambientales. |
| 2 | **Dominio Canónico** | Sostenibilidad y Resiliencia Ambiental |
| 3 | **Alias histórico / técnico** | componente_biofisico · p11_ods (eje ambiental) |
| 4 | **Definición conceptual** | Dimensión de preservación, mitigación e integridad ecológica: la correspondencia entre las presiones antrópicas sobre el entorno y la capacidad institucional de sostener el equilibrio ecosistémico y adaptar el territorio al riesgo climático. |
| 5 | **Propósito** | Monitorear la degradación de los activos naturales, garantizar la adaptación al cambio climático y activar las alarmas de riesgo biofísico — habilitando el acceso al financiamiento climático internacional. |
| 6 | **Pregunta estratégica** | ¿Qué tan efectiva es la intervención pública para mitigar la vulnerabilidad ambiental del territorio y conservar sus recursos vitales frente a la presión del desarrollo? |
| 7 | **Alcance (incluye)** | Conservación de ecosistemas y microcuencas, deforestación y uso del suelo, gestión de riesgo biofísico (deslizamientos, inundación, sismo), mitigación de huella de carbono y cumplimiento de los ODS ambientales (6 Agua · 13 Clima · 14/15 Ecosistemas). |
| 8 | **Exclusiones (no incluye)** | Redes urbanas de alcantarillado doméstico como servicio (→ d10) · los fondos verdes que financian la acción (→ d02) · las alertas operativas institucionales (→ d04) · la vulnerabilidad climática de los grupos prioritarios (→ d12, hilo compartido). |
| 9 | **Data central** | Inventario biofísico del PDOT (corpus) + capa de riesgo georreferenciada (KB_RIESGOS) + metas ODS ambientales. |
| 10 | **Madre + operativos + ancla** | **Madre (concepto):** Integridad ecológica y resiliencia del territorio. **Operativos REALES:** Cumplimiento de ODS ambientales (ICODS · sub-eje) · susceptibilidad a riesgos naturales (PDOT) · estado de conservación biofísico. **Ancla motor:** ICODS → `H73_OUTPUT_API` (ODS · sub-eje ambiental a precisar) · corpus biofísico (Supabase · 362 ind) · capa de riesgo (KB_RIESGOS) → ✅ **LIVE (corpus/riesgo)** · ⚠️ desglose ODS-ambiental del motor a confirmar (NO inventar el sub-índice). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Vulnerabilidad ecológica:** superposición de degradación del suelo + áreas de conservación + riesgo (deslave/inundación/estrés hídrico) sobre los asentamientos humanos — la pantalla de negociación de créditos climáticos con CAF. |

---

## ✅ LOS 13 ADN — COMPLETOS Y ANCLADOS (fundación + 1er ejercicio de Mutabilidad · 2026-06-14)

Los 13 dominios tienen ADN de 11 campos, nombre canónico y **ancla al motor con estado**.
Resumen de anclaje (detalle vivo en `docs/architecture/MAPA_ANCLAJE_MOTOR.md`):
- **✅ LIVE (núcleo):** d01 · d03 · d05 · d06 · d07 · d08 · d09 · d10 · d12-PSG · d13 (biofísico/riesgo corpus · ICODS a precisar) · d02 (ISP/IED/elegibilidad).
- **⏳ PENDIENTE 2026:** d02 ejecución · d03 IFE-E · d06 ICPI 2026 — un solo hueco: cédula eSIGEF 2026 (CHK-08).
- **⚠️ HARDCODED:** d04 matriz de riesgo (conectar a snapshot `H75`).
- **🌱 campo verde:** d11 (corpus PDOT · sin hoja GM dedicada · no inventar madre del motor).
- **❌ MISSING (externos):** d12 IGM/ODS5 (gestión de cooperación, no falla del motor).

**SIGUIENTE (orden de mesa):** Tabla de Equivalencias definitiva → cosecha atómica → recién dashboards.
La auditoría de fórmulas del motor (B) sigue **diferida** hasta su disparador.

---

## 🛰️ GEOTWIN — CAPA TRANSVERSAL (no es un cajón)

> **GeoTwin constituye la capa territorial transversal de QUIRA. Todos los
> dominios de gestión pueden ser espacializados sobre GeoTwin para visualizar
> cómo sus indicadores, riesgos, brechas, inversiones y resultados se distribuyen
> en el territorio.** No es un dashboard del Cajón 10 — es la infraestructura
> territorial de toda la plataforma.

### Matriz de Espacialización (qué indicador REAL de cada cajón se territorializa)
| Dominio (Capa 2) | Pregunta de gestión | Respuesta territorial en GeoTwin |
|---|---|---|
| d02 Presupuesto & Financiamiento | ¿Cuánto se ejecutó? | Inversión per cápita (eSIGEF) por parroquia — qué zonas excluidas |
| d04 Alertas Institucionales | ¿Qué riesgos operativos? | Exposición a riesgos naturales (PDOT) sobre infraestructura crítica |
| d10 Cobertura de Servicios | ¿Cuál es el déficit? | Pobreza por servicios / NBI (INEC) + déficit agua/saneamiento por parroquia |
| d12 Inclusión, Equidad y Género | ¿Dónde la brecha? | Presupuesto con enfoque de género (PSG) × grupos prioritarios por sector |
| (…todos los demás) | ¿qué pasa? | …su indicador madre, proyectado en el mapa |

### Evolución de fases (diseñada y documentada — `docs/geotwin/GEOTWIN_PLAN_IMPLEMENTACION.md`)
```
GeoTwin v1 · TERRITORIALIZA → mapa 2D Folium + motor narrativo F1 (clic → explica).
  Parcial HOY. Pendiente: botón "Ver en Territorio" por cajón + mapa que muta por dominio.
GeoTwin v2 · VISUALIZA 3D   → prismas PyDeck + polígonos PostGIS + DEM NASA. Stack $0,
  DISEÑADO Y DOCUMENTADO · implementación DIFERIDA (no "futuro/fantasía" — fase posterior
  de ejecución, tras consolidar la Fundación Ontológica). Falta: shapefiles PUGS + DEM + PostGIS.
GeoTwin v3 · PREDICE        → series temporales + IA → "¿qué ocurrirá?" (con tracción).
```

---

*Diccionario Conceptual QUIRA · Sprint C · Dylus Lab © 2026 · plantilla madre = Cajón 10 (11 campos) · Nomenclátor canónico = fuente única · ADN anclados al motor (MAPA_ANCLAJE_MOTOR) · GeoTwin = capa transversal.*
