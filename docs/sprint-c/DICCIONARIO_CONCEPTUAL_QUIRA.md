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

## COSECHA ATÓMICA (Javo · 2026-06-13)

> La refactorización NO es por pantalla — es por SECCIONES/PARTES. Una sección,
> gráfica o componente de una pantalla antigua puede servir a un dominio, a otro,
> o a varios. Se cosecha parte por parte. Solo se CREA nuevo lo que falte para
> completar el interior del dominio.

```
[ PANTALLA CANTERA ]   →   [ SECCIÓN/COMPONENTE cosechado ]   →   [ DASHBOARD destino ]
```

---

## 📁 CAJÓN 10 · TERRITORIO & COBERTURA  (plantilla madre — corregida)

| Elemento | Definición |
|---|---|
| **Nombre** | Territorio & Cobertura |
| **Definición conceptual** | Dimensión espacial de la política pública. Representa cómo se distribuyen las condiciones de vida, las capacidades instaladas, las vulnerabilidades ambientales y la asignación de recursos sobre el espacio geográfico del cantón. |
| **Propósito** | Identificar patrones de asimetría territorial, brechas de cobertura de servicios y niveles de exposición al riesgo, para orientar la planificación y la inversión pública basada en evidencia. |
| **Pregunta estratégica** | ¿Cómo se distribuyen las brechas de servicios y los riesgos en el territorio, y de qué manera la inversión pública las mitiga o las acentúa? |
| **Alcance (qué incluye)** | Cartografía (SIG), modelo de terreno, zonificación del PUGS, coberturas sectoriales por parroquia/barrio, mapas de vulnerabilidad física y ambiental. |
| **Exclusiones (qué NO incluye)** | Capacidad administrativa interna (→ Salud Institucional) · presupuesto institucional global (→ Presupuesto) · transparencia (→ Transparencia) · gobernanza de empresas públicas (→ Holding). |
| **Data central** | Matriz de cobertura y brecha parroquial + capa de visualización transversal GeoTwin. |
| **Indicadores madre (REALES — Tabla de Equivalencias)** | • Cobertura de agua por red pública (% · INEC) • Cobertura de saneamiento (% · INEC) • **Equidad Territorial** (IET · Gold Master) • Pobreza por servicios / NBI (INEC) • Inversión pública per cápita por parroquia (eSIGEF) • Exposición a riesgos naturales (susceptibilidad · PDOT) |
| **Conexiones** | Recibe capas de Planificación (01), Presupuesto (02), Alertas (04) y Protección Social & Género (12) para proyectarlas sobre el espacio. Converge en GeoTwin (capa 3). |

### Plano de cosecha atómica — Cajón 10
| Pantalla cantera | Sección/componente a cosechar | → Dashboard |
|---|---|---|
| p10_territorio | Tabla de cobertura por parroquia | D1 · Tablero Cobertura & Brecha |
| p7_brecha | Gráfico comparativo urbano/rural | D1 |
| p10_inversion | Inversión per cápita parroquial | D1 + D2 |
| p4_geotwin | Mapa Folium interactivo + GeoTwin narrativo (F1) | D2 · GeoTwin |
| pdot_indicadores (datos) | Servicios + riesgos parroquiales (extraídos) | D1 + D2 |
| *crear nuevo si falta* | capa de prismas 3D de inversión (futuro PyDeck) | D2 |

**Dashboards finales: 2** — (1) Tablero de Cobertura & Brecha · (2) GeoTwin.

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

*Diccionario Conceptual QUIRA · Sprint C · Dylus Lab © 2026 · plantilla madre = Cajón 10.*
