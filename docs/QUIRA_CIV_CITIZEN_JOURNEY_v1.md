# QUIRA CIV — Citizen Journey v1.0
**Documento Maestro de UX · Constitución Pública · Contrato de Construcción**
Dylus Lab © 2026 · Versión 1.0 · 2026-05-26

---

> **Este documento es el Gold Master del ambiente CIV.**
> Ningún componente, pantalla, texto, alerta o respuesta IA se construye sin consultarlo primero.
> No se modifica sin acuerdo del equipo. No se improvisa. No se omite.

---

## 0. Doctrina Fundacional

### El ciudadano nunca ve la maquinaria interna

El ciudadano **jamás** verá: H73, ICPI, SAT, TGI, dimensiones, fórmulas, hojas Excel, scores, percentiles técnicos, códigos de indicador, nor terminología de auditoría.

El ciudadano **sí** verá: traducción institucional, lenguaje humano, narrativa territorial, alertas claras, mapas, preguntas que puede hacer, documentos que puede exigir, derechos que puede ejercer.

Esta doctrina no es opcional. Es la diferencia entre una herramienta de gobierno y una herramienta ciudadana.

### La IA no sustituye — contextualiza

QUIRA IA (panel derecho) no reemplaza al ciudadano como actor. Explica, contextualiza, traduce, advierte y conecta. El poder de actuar sigue siendo del ciudadano. La IA abre la puerta — el ciudadano entra solo.

### Acceso sin login — siempre

QUIRA CIV es público. Cero autenticación para acceder. La información territorial es un derecho, no un privilegio.

---

## 1. Audiencia

QUIRA CIV tiene cuatro perfiles de usuario, todos igualmente válidos:

| Perfil | Quién es | Qué busca |
|--------|----------|-----------|
| **Ciudadano común** | Residente del cantón, sin formación técnica | Saber si su municipio cumple, entender qué se hace con sus impuestos, reportar un problema |
| **Profesional / técnico** | Abogado, periodista, contratista, planificador | Datos verificables, documentos oficiales, trazabilidad, comparación cantonal |
| **Académico / investigador** | Universidad, think tank, consultor | Series históricas, metodología, indicadores desagregados, exportación |
| **Organización social / ONG** | Colectivos, juntas parroquiales, ONGs, fundaciones | Alertas de incumplimiento, brechas de género, fondos disponibles, rutas de incidencia |

La interfaz sirve a los cuatro sin discriminar. No hay modo "experto" ni modo "básico" — hay **una sola experiencia** que responde al nivel de la pregunta.

---

## 2. Arquitectura de Pantallas (P0 → P4)

### Estructura general — tres paneles

```
┌─────────────────────────────────────────────────────────────────┐
│  QUIRA CIV · Inteligencia Territorial Ciudadana                 │
├──────────────┬──────────────────────────────┬───────────────────┤
│  PANEL IZQ   │      PANEL CENTRAL           │   PANEL DER       │
│  Navegación  │      Contenido principal      │   QUIRA IA        │
│  y contexto  │      Dashboards / Mapas /     │   Conversacional  │
│              │      Tablas / Narrativa       │                   │
│  · Docs      │                              │   "¿Qué significa │
│  · Alertas   │                              │    esto para mí?" │
│  · Terit.    │                              │                   │
│  · Ejecuci.  │                              │   Explica         │
│  · Particip. │                              │   Contextualiza   │
│  · Rendición │                              │   Traduce         │
│              │                              │   Advierte        │
└──────────────┴──────────────────────────────┴───────────────────┘
```

---

### P0 — Entrada / Portal Territorial

**Propósito:** Primera impresión. El ciudadano aterriza aquí. Debe sentir que llegó a algo que le pertenece.

**Elementos:**

- **Hero visual:** Mapa del cantón con indicador de estado general. No un número — una señal semáforo (verde/amarillo/rojo) con etiqueta humana: "Tu municipio está cumpliendo sus metas" / "Hay alertas activas en tu cantón" / "Atención: se detectaron retrasos en ejecución"
- **Resumen narrativo del período:** 2-3 frases en lenguaje plain. "En lo que va de 2026, el GAD de Montecristi ha ejecutado el 67% de su plan. El agua potable y las vías rurales muestran avance. La gestión ambiental presenta retrasos."
- **Tres acciones rápidas:**
  - 🔍 Buscar un tema o proyecto
  - 📄 Subir o buscar un documento
  - 💬 Preguntar a QUIRA IA
- **Alertas ciudadanas activas** (si las hay): tarjetas compactas en rojo/naranja con texto humano. "El indicador de Acceso al Agua en zonas rurales bajó este trimestre."
- **Barra de selección cantonal:** Dropdown para cambiar de cantón (escalabilidad SaaS). Por defecto: Montecristi.

**QUIRA IA en P0:** "Hola, soy QUIRA. Puedo ayudarte a entender cómo está funcionando tu municipio. ¿Qué te preocupa?"

---

### P1 — Búsqueda y Carga Documental

**Propósito:** El ciudadano busca un tema, un proyecto, un documento. También puede subir un documento para análisis.

**Elementos:**

**Sub-panel 1.1 — Búsqueda temática:**
- Barra de búsqueda con lenguaje natural: "agua potable", "escuela rural", "contratación pública 2026", "presupuesto participativo"
- Resultados organizados en 3 categorías: Indicadores de estado · Documentos disponibles · Alertas relacionadas
- Filtros: cantón, período, tema PDOT, entidad del Holding

**Sub-panel 1.2 — LOTAIP y acceso a información:**
- Listado de documentos exigibles por LOTAIP con estado: ✓ Publicado / ⚠ Tardío / ✗ Ausente
- Botón "Exigir este documento" → genera texto de solicitud formal listo para usar
- Timer de días restantes para respuesta legal (15 días hábiles LOTAIP)
- Índice Opacidad Cantonal (traducido): "Tu municipio tiene pendiente publicar 3 documentos obligatorios este trimestre"

**Sub-panel 1.3 — Carga documental ciudadana:**
- El ciudadano puede subir un documento público (resolución, contrato, informe) para que QUIRA IA lo analice
- QUIRA IA extrae: entidad, monto, período, tipo de contrato, alertas de irregularidad potencial
- No almacena el documento — análisis en sesión

**QUIRA IA en P1:** Responde búsquedas. "Encontré 4 proyectos de agua potable en tu zona. El más reciente tiene un retraso de 3 meses respecto al plan original. ¿Quieres ver los detalles?"

---

### P2 — Análisis Completo del Territorio

**Propósito:** La vista de fondo — el estado del territorio traducido. Aquí vive el corazón de QUIRA CIV.

**Tabs del panel central:**

#### 2.1 — Estado Municipal (traducción del GOV)
- Dashboard con 5 dimensiones del PDOT en lenguaje ciudadano:
  - "Servicios básicos" (← AH/Agua Saneamiento)
  - "Desarrollo económico" (← EP/Equidad Productiva)
  - "Medio ambiente y riesgo" (← FA/Físico Ambiental)
  - "Participación y gobierno" (← PI/Institucional)
  - "Infraestructura y conectividad" (← BF/Bienestar Físico)
- Cada dimensión: semáforo + frase + porcentaje de avance
- Botón "¿Qué significa esto?" → QUIRA IA explica en contexto

#### 2.2 — Mapa Territorial
Geo-visualización con tres capas:
- **Pin Rojo** — Problemas reportados / alertas activas / rezagos en ejecución
- **Pin Verde** — Proyectos activos / metas cumplidas / iniciativas ciudadanas
- **Pin Morado** — Brechas de género e inclusión identificadas

Interacción: click en pin → panel lateral con detalle. QUIRA IA puede narrar el mapa: "En la parroquia Leonidas Plaza hay 2 alertas activas relacionadas con acceso al agua."

#### 2.3 — Ejecución Presupuestaria
- Presupuesto total vs ejecutado: barra de progreso con lenguaje humano
- "De cada $100 asignados, se han gastado $67"
- Tabla de las 10 obras más grandes: nombre, monto, avance, alerta si corresponde
- Filtro por parroquia, por tipo de obra, por entidad del Holding

#### 2.4 — Holding Municipal
- Tarjetas de EP Aseo · Bomberos · Patronato: estado, servicio, cobertura
- No hay números técnicos — hay preguntas: "¿Llega el servicio de aseo a tu zona?" con respuesta de cobertura real

#### 2.5 — Comparación Cantonal
- QUIRA CIV vs otros cantones de Manabí (y Ecuador cuando haya datos)
- Lenguaje: "Montecristi está en el tercio superior en ejecución presupuestaria comparado con cantones similares"
- Sin rankings numéricos — posición narrativa

#### 2.6 — Narrativa del Alcalde (Fricción Narrativa)
- Análisis NLP del discurso oficial vs datos reales
- "El alcalde anunció X. Los datos muestran Y."
- Visualización de consistencia: "Lo que se prometió / Lo que se ejecutó"
- Fuente: discursos públicos, informes de rendición de cuentas, LOTAIP

**QUIRA IA en P2:** Contextualiza cualquier dato. "Ese 67% de ejecución es normal para este período del año. Históricamente, el primer trimestre tiene ejecución baja por procesos de contratación. La preocupación real sería si al cierre de junio no supera el 45%."

---

### P3 — Conversación con QUIRA IA

**Propósito:** Pantalla dedicada al diálogo. El ciudadano puede hacer cualquier pregunta sobre el territorio.

**Capacidades del chat:**

- **Traducción institucional:** Convierte cualquier métrica interna en lenguaje humano
- **Respuesta contextual:** Conoce el cantón, el período, el historial
- **Educación ciudadana:**
  - Explica qué es el PDOT y por qué importa
  - Explica qué es el presupuesto participativo y cómo participar
  - Explica qué es la Silla Vacía y cómo convocarse
  - Explica qué son las Audiencias Públicas y cómo pedirlas
  - Explica la LOTAIP y cómo exigir información
- **Alertas proactivas:** "Detecté que la escuela en tu zona lleva 6 meses sin actualización en el plan. ¿Quieres saber cómo hacer seguimiento?"
- **Rutas de acción:** "Si quieres exigir este informe, aquí está el texto de la solicitud LOTAIP. Si quieres reportar este problema, aquí está el canal de Contraloría."
- **Conexión normativa:** Cita artículos de COOTAD, LOTAIP, LOPC sin tecnicismos: "Tienes derecho legal a pedir ese informe. Aquí te explico cómo."

**Preguntas de ejemplo que el sistema debe poder responder:**
- "¿En qué se está gastando la plata del municipio?"
- "¿Por qué no han arreglado la calle frente a mi casa?"
- "¿Cómo sé si el agua de mi barrio cumple normas?"
- "¿Cómo pido cuentas al alcalde?"
- "¿El municipio cumplió con los ODS?"
- "¿Qué proyectos hay en mi parroquia?"
- "¿Cómo puedo participar en el presupuesto participativo?"

**Límites de la IA (no negociables):**
- No emite opinión política sobre el alcalde o el gobierno
- No hace predicciones electorales
- No inventa datos — si no sabe, lo dice y redirige a la fuente
- No identifica personas — trabaja con entidades, no individuos
- No almacena conversaciones entre sesiones

**QUIRA IA en P3:** Modo conversacional pleno. El panel derecho se expande o el usuario cambia a vista full-chat.

---

### P4 — Exportación / Solicitud Formal / Poder Ciudadano

**Propósito:** Convertir el análisis en acción. Aquí el ciudadano pasa de observar a actuar.

**Herramientas disponibles:**

#### 4.1 — Generador de Solicitudes LOTAIP
- El ciudadano elige el documento que quiere exigir
- QUIRA genera el texto formal completo, con artículos legales, plazos y canal de envío
- Formatos: PDF descargable / texto para copiar / envío por email (si el municipio tiene canal)

#### 4.2 — Dossier Ciudadano (exportación)
- El ciudadano arma su propio reporte del territorio: selecciona indicadores, alertas, mapas, documentos
- Exporta como PDF o presentación
- Diseñado para: audiencias públicas, medios de comunicación, ONGs, universidades

#### 4.3 — Contraloría y Control Social
- Ruta directa para reportar irregularidades a Contraloría General del Estado
- QUIRA explica el proceso y ayuda a estructurar el reporte
- Vincula con el Consejo de Participación Ciudadana (CPCCS) y RDC

#### 4.4 — Fondos y Cooperación
- Proyectos ciudadanos que califican para fondos internacionales (basado en brechas detectadas)
- Gender Bonds: brechas de género que pueden convertirse en proyectos financiables
- ONGs activas en el cantón con líneas de trabajo afines
- No hace promesas — hace conexiones

#### 4.5 — Silla Vacía y Audiencias Públicas
- Información sobre mecanismos de participación directa
- Cómo convocar Silla Vacía (COOTAD Art. 101)
- Cómo solicitar Audiencia Pública
- Calendario de sesiones del Concejo Municipal
- QUIRA genera el texto de convocatoria si el ciudadano lo necesita

**QUIRA IA en P4:** "Con los datos que revisamos, tienes base para presentar una solicitud formal. ¿Quieres que te ayude a redactarla?"

---

## 3. Panel Izquierdo — Navegación Contextual

El panel izquierdo no es solo un menú — es el mapa de opciones del territorio:

```
QUIRA CIV
───────────────
🗺 Mi Territorio
   · Estado general
   · Mapa
   · Alertas activas

📋 Documentos
   · LOTAIP pendientes
   · Presupuesto
   · Contratos
   · Rendición de cuentas

⚡ Ejecución
   · Presupuesto
   · Obras y proyectos
   · Holding Municipal

👥 Participación
   · Silla Vacía
   · Audiencias Públicas
   · Presupuesto Participativo
   · RDC y CPCCS

📊 Comparar
   · Otros cantones
   · Evolución histórica

📤 Actuar
   · Solicitar documento (LOTAIP)
   · Reportar a Contraloría
   · Exportar dossier
   · Conectar con fondos
```

---

## 4. QUIRA IA — Especificaciones Técnicas del Comportamiento

### Tono
- Simple, directo, sin condescendencia
- No dice "según mis datos" — dice "los datos muestran"
- No usa jerga institucional sin explicarla primero
- No dice "lamentablemente" ni "desafortunadamente" — es informativo, no dramático
- Primer mensaje de cada sesión: siempre un saludo + pregunta abierta

### Niveles de respuesta
La IA detecta el perfil de la pregunta y ajusta:
- Pregunta ciudadana simple → respuesta en 2-3 frases, con semáforo y acción sugerida
- Pregunta técnica/profesional → respuesta con datos, fuente, metodología disponible
- Pregunta investigadora → respuesta con exportación de datos, serie histórica, cita de fuente primaria

### Fuentes que puede citar
- Gold Master QUIRA (datos oficiales)
- PDOT Montecristi 2023-2027
- LOTAIP vigente
- COOTAD
- COPFP
- Rendiciones de Cuentas publicadas
- Snapshots longitudinales QUIRA (histórico)

### Lo que la IA NO puede hacer (hardcoded)
- Inventar datos
- Emitir opinión política
- Identificar personas individualmente
- Almacenar conversaciones
- Hacer predicciones sobre resultados electorales
- Asesoría legal vinculante (puede explicar la ley, no interpretar para un caso específico)

---

## 5. Diccionario de Traducción Institucional

Esta tabla es la ley. Toda interfaz ciudadana usa la columna "Lenguaje QUIRA CIV":

| Término interno QUIRA GOV | Lenguaje QUIRA CIV |
|---------------------------|---------------------|
| ICPI_GLOBAL_PCT | Cumplimiento general del plan municipal |
| TGI_SCORE | Índice de gobernanza territorial |
| SAT (alerta) | ⚠ Alerta activa en este indicador |
| Dimensión AH | Servicios básicos y hábitat |
| Dimensión EP | Desarrollo económico |
| Dimensión FA | Medio ambiente y gestión de riesgo |
| Dimensión BF | Infraestructura y bienestar físico |
| Dimensión PI | Participación y gobierno |
| MMP_AVANCE_PCT | Avance del Plan Municipal de Metas |
| Holding Municipal | El grupo de empresas públicas del municipio |
| EP Aseo | Empresa pública de aseo y recolección |
| Snapshot / Corte | Foto del estado del municipio en ese mes |
| Gold Master | Base de datos oficial del municipio |
| PBKDF2 / hash | (nunca visible al ciudadano) |
| H73 OUTPUT API | (nunca visible al ciudadano) |
| rc_score / rc_pct | Resultado de rendición de cuentas |
| CPCCS | Consejo de Participación Ciudadana |
| RDC | Rendición de Cuentas |

---

## 6. Alertas Ciudadanas — Protocolo

Las alertas en QUIRA CIV son siempre:
1. **Traducidas** — nunca código SAT, siempre texto humano
2. **Contextualizadas** — por qué importa, no solo qué pasó
3. **Accionables** — qué puede hacer el ciudadano con esa alerta
4. **Proporcionales** — no alarmar sin base; distinguir retraso normal de incumplimiento crítico

**Formato de alerta:**
```
⚠ [Título en lenguaje humano]
   [Una frase de contexto]
   [Una acción sugerida]
   Actualizado: [fecha]
```

**Ejemplo:**
```
⚠ El servicio de agua potable en zonas rurales bajó este trimestre
   La cobertura pasó del 78% al 71% en las parroquias Montecristi y Leonidas Plaza.
   Puedes solicitar el informe oficial de agua potable usando el botón de abajo.
   Actualizado: Abril 2026
```

---

## 7. Flujo de Construcción — Fases

El ambiente CIV se construye en este orden. No se salta fases:

### Fase 0 — Infraestructura base (inmediata)
- [ ] `env_civic.py` deja de ser placeholder — renderiza P0 básico
- [ ] Panel de 3 columnas configurado (nav izq / contenido / IA der)
- [ ] QUIRA IA inicial: chatbot básico con contexto del cantón (sin datos reales aún)
- [ ] Mapa de Montecristi estático con semáforo general

### Fase 1 — Traducción y datos reales
- [ ] Conectar con Supabase: leer último snapshot
- [ ] Renderizar P2.1 (Estado Municipal) con datos reales traducidos
- [ ] Diccionario de traducción aplicado en toda la interfaz
- [ ] Alertas SAT traducidas y visibles en P0

### Fase 2 — Documental
- [ ] P1.2 LOTAIP: listado de documentos con estado real
- [ ] Generador de solicitudes LOTAIP (P4.1)
- [ ] P1.3 carga de documentos y análisis IA

### Fase 3 — Geo y narrativa
- [ ] P2.2 Mapa territorial con pins (Mapbox o Folium)
- [ ] P2.6 Fricción Narrativa: primer análisis discurso vs datos
- [ ] P2.5 Comparación cantonal (requiere datos de otros cantones)

### Fase 4 — Poder ciudadano
- [ ] P4.3 Ruta Contraloría
- [ ] P4.4 Fondos y cooperación
- [ ] P4.5 Silla Vacía y Audiencias
- [ ] P3 Chat QUIRA IA completo (LLM integrado)

### Fase 5 — Escalabilidad SaaS
- [ ] Selector de cantón funcional (multi-GAD)
- [ ] Cada cantón con su propio Gold Master
- [ ] Panel de comparación multi-cantonal

---

## 8. Reglas de Diseño Visual

QUIRA CIV es **diferente** a QUIRA GOV. No comparten paleta de forma indiscriminada:

| Dimensión | QUIRA GOV | QUIRA CIV |
|-----------|-----------|-----------|
| Audiencia | Técnicos institucionales | Ciudadanía abierta |
| Tono visual | Denso, analítico, oscuro | Abierto, claro, accesible |
| Fondo principal | #0A1128 (navy oscuro) | Blanco o gris muy claro |
| Color primario | #00D4FF (cyan eléctrico) | #2563EB (azul institucional accesible) |
| Color de alerta | #FF4D6D | #DC2626 (rojo legible en claro) |
| Color positivo | #00E096 | #16A34A (verde accesible) |
| Tipografía | Inter 700 + JetBrains Mono | Inter 400/600 (más legible) |
| Densidad | Alta — muchos datos en pantalla | Media — espacio para respirar |
| Mobile first | Secundario | CRÍTICO — ciudadano accede desde celular |

**Regla de oro de diseño CIV:** Si el ciudadano no puede leerlo en un celular de gama media con mala conexión, no va a producción.

---

## 9. Anti-Patrones Prohibidos en QUIRA CIV

Estos elementos están prohibidos en cualquier vista ciudadana:

- ❌ Mostrar nombres de hojas Excel (H73, OUTPUT_API, etc.)
- ❌ Mostrar IDs de indicador (eje_ah_02, icpi_dim_1, etc.)
- ❌ Mostrar fórmulas o ponderaciones
- ❌ Mostrar errores técnicos crudos al usuario (500, None, NaN)
- ❌ Tablas sin contexto narrativo
- ❌ Gráficos sin etiquetas en lenguaje humano
- ❌ Porcentajes sin referencia ("67%" → "67% de las metas cumplidas")
- ❌ Rankings sin explicación de criterio
- ❌ Alertas sin acción sugerida
- ❌ QUIRA IA inventando datos no disponibles
- ❌ Textos en inglés en la interfaz ciudadana
- ❌ Terminología jurídica sin traducción

---

## 10. Principio Final

QUIRA CIV no es un portal de datos abiertos.
No es un dashboard técnico con acceso público.
No es un mapa bonito de gestión municipal.

**QUIRA CIV es infraestructura pública de rendición de cuentas.**

Su éxito se mide en una sola pregunta: **¿Un ciudadano sin formación técnica puede entender cómo está su municipio y saber qué hacer con esa información?**

Si la respuesta es sí, funciona.
Si es no, se rediseña.

---

*Documento controlado — Dylus Lab · QUIRA Intelligence · 2026-05-26*
*Versión siguiente: cuando entre la Fase 1 de construcción. No antes.*
