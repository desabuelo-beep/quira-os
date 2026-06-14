# DICCIONARIO CONCEPTUAL QUIRA — Fundación Ontológica de los 12 Cajones
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
*¿DÓNDE pasa?*. Arquitectura: **12 dominios de gestión + 1 capa territorial
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

## 🗺️ MATRIZ MAESTRA — el índice de toda la ontología (colega · 2026-06-14)

> Capacidad (Capa 0.5) ↕ Dominio canónico ↕ Indicador madre (concepto) ↕
> Operativos REALES del motor ↕ Expresión GeoTwin. El mapa de una sola página de QUIRA.

| # | Capacidad (0.5) | Dominio canónico | Indicador madre (concepto) | Operativos REALES (motor) | Expresión GeoTwin |
|---|---|---|---|---|---|
| d01 | Trayectoria | Planificación Estratégica | Cumplimiento de la planificación de desarrollo | Avance físico metas PDOT (4 ejes) | Cumplimiento territorial de metas |
| d02 | Movilización | Presupuesto & Financiamiento | Captación y eficiencia del gasto | Elegibilidad/fondos en riesgo (radar D02) · inversión p.c. (eSIGEF) | Inversión per cápita por parroquia |
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
10. **Indicador madre (concepto) + operativos REALES** — concepto arriba, métricas del motor abajo.
11. **Expresión GeoTwin** (Capa 3) — cómo se espacializa la capacidad.

---

## 📁 CAJÓN 10 · COBERTURA DE SERVICIOS E INFRAESTRUCTURA  (plantilla madre · re-sellada 11 campos · 2026-06-14)

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
| 10 | **Indicador madre + operativos** | **Madre (concepto):** Acceso territorial a bienes públicos. **Operativos REALES:** Cobertura de agua por red pública (% · INEC) · Cobertura de saneamiento (% · INEC) · Cobertura de recolección de desechos (% · INEC) · Pobreza por NBI (INEC) · Equidad Territorial (Gold Master) · Inversión per cápita por parroquia (eSIGEF). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Déficit estructural:** extrusión volumétrica 3D de los polígonos parroquiales según NBI; cruza el diagnóstico base del PDOT con los proyectos ejecutados, encendiendo gradientes rojos en las coordenadas de las comunidades excluidas. |

### Plano de cosecha atómica — Cajón 10
| Pantalla cantera | Sección/componente a cosechar | → Dashboard |
|---|---|---|
| p10_territorio | Tabla de cobertura por parroquia | D1 · Tablero Cobertura & Brecha |
| p7_brecha | Gráfico comparativo urbano/rural | D1 |
| p10_inversion | Inversión per cápita parroquial | D1 |
| pdot_indicadores (datos) | Servicios parroquiales (extraídos) | D1 |

**Dashboards finales: 1** — Tablero de Cobertura & Brecha + botón "🛰️ Ver en Territorio (GeoTwin)".
*(El mapa ya NO es dashboard del Cajón 10 — es la capa transversal · ver §GeoTwin abajo.)*

---

## 📁 CAJÓN 01 · PLANIFICACIÓN ESTRATÉGICA  (primer ADN bajo la nueva arquitectura · mesa 2026-06-14)

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
| 10 | **Indicador madre + operativos** | **Madre (concepto):** Cumplimiento de la planificación de desarrollo. **Operativos REALES:** Avance físico consolidado de metas PDOT (4 ejes oficiales del plan de desarrollo). |
| 11 | **Expresión GeoTwin (Capa 3)** | **Cumplimiento territorial:** mapas temáticos donde las capas base de diagnóstico del PDOT (biofísico, movilidad…) se intersectan con los % de avance del plan; tiñe parroquias según el rezago de metas sectoriales, mostrando dónde la planificación no se materializó. |

---

## ESQUELETO — Cajones 02-09, 11, 12 (pendientes de ADN completo · mismo nivel conceptual)

> d01 ✅ y d10 ✅ ya tienen ADN completo (arriba). Faltan estos 10, en orden de
> mesa: d02 → d09 → d11 → d12. Cada uno se redactará con los **11 campos** +
> cosecha atómica. Nombres = Nomenclátor. Indicadores = solo los del motor
> (concepto puro arriba, métrica real abajo).

| # | Cajón (canónico) | Capacidad (0.5) | Definición conceptual (1 línea — a pulir) | Madre (concepto) · operativos reales |
|---|---|---|---|---|
| 02 | Presupuesto & Financiamiento | Movilización | Origen, asignación y oportunidades de financiamiento de los recursos | Captación y eficiencia del gasto · elegibilidad/fondos en riesgo (radar D02) |
| 03 | Gobernanza del Mandato | Fidelidad democrática | Correspondencia entre la palabra empeñada y su formalización en el plan | Congruencia promesa↔plan · consistencia plan de campaña (IFE-A) |
| 04 | Alertas Institucionales | Anticipación | Detección temprana de riesgos institucionales | Riesgo operativo y legal activo · cola del Sistema de Alerta Temprana |
| 05 | Holding e Integración Municipal | Articulación | Desempeño del conjunto de entidades de gobernanza del cantón | Desempeño del ecosistema · promedio de entidades |
| 06 | Salud Institucional | Sostenibilidad interna | Cumplir funciones de forma consistente, eficiente y sostenible | Cumplimiento sostenible · Cumplimiento Institucional (ICPI) |
| 07 | Transparencia | Verificabilidad | Acceso oportuno, verificable y comprensible a la información pública | Apertura verificable · Transparencia activa (LOTAIP 21/21) |
| 08 | Participación Ciudadana | Inteligencia colectiva | Incidencia de la ciudadanía en las decisiones públicas | Incidencia ciudadana · Gobernanza participativa (IGP) |
| 09 | Rendición de Cuentas | Responsabilidad pública | Validación pública de la gestión ante el control y la ciudadanía | Validación pública · estado del circuito de rendición (RDC) |
| 11 | Desarrollo Económico Territorial | Dinamización | Dimensión económica: producción, empleo y desarrollo del territorio | Capacidad productiva y de empleo · PEA / cadenas de valor (PDOT) |
| 12 | Inclusión, Equidad y Género | Inclusión y equidad | Garantizar los derechos de los grupos de atención prioritaria | Protección de grupos prioritarios · Presupuesto con enfoque de género (PSG) |

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

*Diccionario Conceptual QUIRA · Sprint C · Dylus Lab © 2026 · plantilla madre = Cajón 10 (11 campos) · Nomenclátor canónico = fuente única de nombres · GeoTwin = capa transversal.*
