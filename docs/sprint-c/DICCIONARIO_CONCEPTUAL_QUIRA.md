# DICCIONARIO CONCEPTUAL QUIRA — Fundación Ontológica de los 12 Cajones
**Sprint C · 2026-06-13 · el documento fundacional · nivel estándar LAC (CAF/BID)**

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

## 📁 CAJÓN 10 · COBERTURA DE SERVICIOS E INFRAESTRUCTURA  (purificado — ya NO "es el mapa")

| Elemento | Definición |
|---|---|
| **Nombre** | Cobertura de Servicios e Infraestructura *(antes "Territorio & Cobertura" — el mapa pasó a GeoTwin transversal)* |
| **Definición conceptual** | Capacidad del territorio de garantizar el acceso de la población a los servicios básicos e infraestructura física. Mide el cumplimiento de las metas de provisión de agua, saneamiento, manejo de desechos y conectividad sobre el espacio del cantón. |
| **Propósito** | Cuantificar la cobertura y el déficit de servicios básicos e infraestructura, e identificar las brechas de provisión para orientar la priorización de la inversión. |
| **Pregunta estratégica** | ¿Cuál es el déficit de servicios e infraestructura del cantón y cómo se distribuye entre sus parroquias? |
| **Alcance (qué incluye)** | Cobertura de agua potable, alcantarillado/saneamiento, recolección de desechos, conectividad vial y equipamiento por parroquia. |
| **Exclusiones (qué NO incluye)** | La representación espacial/mapa (→ **GeoTwin**, capa transversal) · capacidad administrativa interna (→ Salud Institucional) · presupuesto global (→ Presupuesto) · transparencia (→ Transparencia). |
| **Data central** | Matriz de cobertura y brecha de servicios por parroquia. |
| **Indicadores madre (REALES — Tabla de Equivalencias)** | • Cobertura de agua por red pública (% · INEC) • Cobertura de saneamiento (% · INEC) • Cobertura de recolección de desechos (% · INEC) • Pobreza por servicios / NBI (INEC) • **Equidad Territorial** (IET · Gold Master) • Inversión per cápita por parroquia (eSIGEF) |
| **Conexiones** | Sus indicadores se espacializan en **GeoTwin** (capa transversal) junto con los de todos los demás cajones. GeoTwin recibe las brechas de cobertura de ESTE cajón para mostrarlas sobre el mapa del cantón. |

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

## ESQUELETO — Cajones 01-09, 11, 12 (a co-crear, mismo nivel conceptual)

Cada uno se redactará con los 9 campos + cosecha atómica + indicadores REALES.
Nombres públicos: Tabla de Equivalencias. Indicadores: solo los del motor.

| # | Cajón | Definición conceptual (1 línea — a pulir) | Indicadores madre reales |
|---|---|---|---|
| 01 | Planificación Estratégica | Capacidad de traducir el mandato en objetivos y metas verificables | avance metas PDOT · 4 ejes |
| 02 | Presupuesto & Financiamiento | Dimensión de los recursos: origen, asignación y oportunidades de financiamiento | elegibilidad fondos (radar D02) |
| 03 | Metas PDOT · Mandato | Correspondencia entre la palabra empeñada y su formalización en el plan | Cumplimiento del plan de campaña (IFE-A) |
| 04 | Alertas Institucionales | Sistema de detección temprana de riesgos institucionales | Alertas activas (Sistema de Alerta Temprana) |
| 05 | Holding / Ecosistema Municipal | Desempeño del conjunto de entidades de gobernanza del cantón | promedio entidades |
| 06 | Salud Institucional | Capacidad de la organización pública de cumplir funciones de forma consistente, eficiente y sostenible | Cumplimiento Institucional (ICPI) |
| 07 | Transparencia | Capacidad de garantizar acceso oportuno, verificable y comprensible a la información pública | Transparencia activa (LOTAIP) |
| 08 | Participación Ciudadana | Mecanismos de incidencia de la ciudadanía en las decisiones públicas | Participación / gobernanza participativa (IGP) |
| 09 | Rendición de Cuentas | Proceso de validación pública de la gestión ante el órgano de control y la ciudadanía | estado del circuito de rendición |
| 11 | Ecosistema Productivo Territorial | Dimensión económica del territorio: producción, empleo y desarrollo | (en construcción) |
| 12 | Protección Social & Género | Capacidad de garantizar derechos de los grupos de atención prioritaria | Presupuesto con enfoque de género (PSG) |

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
| 02 Presupuesto | ¿Cuánto se ejecutó? | Inversión per cápita (eSIGEF) por parroquia — qué zonas excluidas |
| 04 Alertas | ¿Qué riesgos operativos? | Exposición a riesgos naturales (PDOT) sobre infraestructura crítica |
| 10 Cobertura de Servicios | ¿Cuál es el déficit? | Pobreza por servicios / NBI (INEC) + déficit agua/saneamiento por parroquia |
| 12 Protección Social & Género | ¿Dónde la brecha? | Presupuesto con enfoque de género (PSG) × grupos prioritarios por sector |
| (…todos los demás) | ¿qué pasa? | …su indicador madre, proyectado en el mapa |

### Implementación — honestidad de fases (Director)
```
GeoTwin v1 · AHORA   → capa transversal con lo que YA existe: mapa 2D Folium +
                       motor narrativo F1 (clic → explica) + el botón de anclaje
                       por cajón. El mapa muta sus datos según el dominio activo.
GeoTwin 3D · DESPUÉS → prismas/extrusión PyDeck + polígonos PostGIS + DEM.
                       Requiere construir la capa geoespacial (hoy hay centroides,
                       no polígonos). NO se promete como inmediato (ver docs/geotwin).
```

---

*Diccionario Conceptual QUIRA · Sprint C · Dylus Lab © 2026 · plantilla madre = Cajón 10 · GeoTwin = capa transversal.*
