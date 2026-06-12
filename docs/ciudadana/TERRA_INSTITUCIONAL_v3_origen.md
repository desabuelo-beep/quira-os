Pantalla 1 — **Dashboard Ejecutivo TERRA / Centro de Mando Municipal**  
**(completa, nivel ingeniería PMV, flujo real, backend, roles, validaciones, UX real)**

---

**1\. Objetivo Estratégico de la Pantalla**

Es la **pantalla principal** donde Alcalde, Director Financiero, Planificación y Control Interno ingresan diariamente para conocer el estado real del municipio en una sola vista.

Debe responder en menos de **7 segundos** estas preguntas:

1. ¿Cómo está el municipio hoy?

2. ¿Qué riesgo crítico existe?

3. ¿Qué índice cayó?

4. ¿Qué dirección está fallando?

5. ¿Qué hacer primero?

6. ¿Qué mejora produce más impacto inmediato?

---

**2\. Nombre Interno**

/app/executive-dashboard

---

**3\. Usuarios que ingresan**

| Rol | Acceso |
| :---- | :---- |
| Alcalde | Total lectura |
| Vicealcaldía | Lectura |
| Director Financiero | Total |
| Planificación | Total |
| Auditoría Interna | Lectura avanzada |
| Concejales | Resumen |
| Ciudadanía (futuro) | Portal simplificado |

---

**4\. Layout Real PMV**

┌─────────────────────────────────────────────┐

│ HEADER SUPERIOR                           │

│ Logo TERRA | Municipio | Año Fiscal | User│

├─────────────────────────────────────────────┤

│ KPIs PRINCIPALES (10 cards)              │

├─────────────────────────────────────────────┤

│ Radar SAT | Heatmap Direcciones | Alertas │

├─────────────────────────────────────────────┤

│ Evolución ICPI | Índices Históricos       │

├─────────────────────────────────────────────┤

│ Recomendaciones IA Priorizadas            │

├─────────────────────────────────────────────┤

│ Últimos eventos / logs / integraciones    │

└─────────────────────────────────────────────┘

---

**5\. Sección Superior Header**

**Componentes:**

* Logo Municipio

* Logo TERRA

* Selector Año Fiscal:

  * 2024

  * 2025

  * 2026

  * 2027

* Estado Integraciones:

| Sistema | Estado |
| :---- | :---- |
| eSIGEF | 🟢 |
| SERCOP | 🟢 |
| RRHH | 🟡 |
| LOTAIP | 🔴 |
| GIS | 🟢 |

* Usuario conectado

* Última actualización:

17 Abr 2026 \- 09:14 AM

---

**6\. KPIs Principales (10 tarjetas)**

┌ ICPI ┐

69.93%

🟡 Transición

\+2.4 vs mes anterior

┌ Brecha Integridad ┐

30.07 pts

🔴 Crítica

┌ IGP ┐

28.0%

🟠 Gobernanza débil

┌ IET ┐

91.42%

🟢 Equidad alta

┌ IOC ┐

17.71%

🟡 Riesgo moderado

Y así las 10\.

---

**7\. Backend Real de KPIs**

**Endpoint:**

GET /api/dashboard/summary?year=2025

**Response:**

{

  "municipality":"Montecristi",

  "year":2025,

  "updated\_at":"2026-04-17T09:14:00",

  "indices":{

    "icpi":69.93,

    "ife":72.83,

    "ied":69.93,

    "itam":56.00,

    "igp":28.00,

    "ipe":69.93,

    "psg":87.55,

    "isp":58.40,

    "ioc":17.71,

    "iet":91.42

  }

}

---

**8\. Colores Automáticos**

**Frontend Rule Engine**

if value \>= 90 \=\> green

if 70-89 \=\> lime

if 40-69 \=\> yellow

if 20-39 \=\> orange

if \<20 \=\> red

---

**9\. Radar Preventivo SAT**

Visual:

SAT-I    🔴

SAT-II   🟢

SAT-III  🟡

SAT-IV   🔴

SAT-V    🟢

SAT-VI   🔴

SAT-VII  🟢

**Click SAT-VI abre:**

* dependencia riesgosa

* dirección afectada

* metas involucradas

* monto asociado

* acción correctiva

---

**10\. Endpoint SAT**

GET /api/sats/status

Response:

\[

 {"code":"SAT-I","status":"red"},

 {"code":"SAT-II","status":"green"},

 {"code":"SAT-VI","status":"red"}

\]

---

**11\. Heatmap Direcciones Municipales**

Tabla:

| Dirección | Riesgo | ICPI interno |
| :---- | :---- | :---- |
| Obras Públicas | 🔴 | 42 |
| Financiero | 🟢 | 88 |
| Agua Potable | 🟡 | 63 |
| Patronato | 🔴 | 39 |
| Participación | 🟠 | 54 |

Click fila → Pantalla 2 (Detalle Dirección)

---

**12\. Evolución Histórica ICPI**

Gráfico línea:

2024 61%

2025 69.9%

2026 74%

2027 82%

Con meta PDOT punteada.

---

**13\. Motor IA Recomendaciones**

Caja automática:

TOP 3 acciones hoy:

1\. Regularizar Obras Públicas (+6.4 ICPI)

2\. Subir LOTAIP archivos (+2.1)

3\. Ejecutar metas Patronato (+4.8)

---

**14\. Endpoint IA**

POST /api/ai/recommendations

Payload:

{

 "year":2025

}

---

**15\. Logs de Integraciones**

09:00 eSIGEF sync OK

09:02 SERCOP sync OK

09:03 RRHH timeout

09:05 GIS sync OK

---

**16\. Base de Datos Real**

**Tabla dashboard\_cache**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| municipality\_id | uuid |
| year | int |
| icpi | decimal |
| igp | decimal |
| ioc | decimal |
| snapshot\_json | jsonb |
| updated\_at | timestamp |

---

**17\. Performance Engineering**

**Tiempo máximo carga:**

\< 2.5 segundos

**Estrategia:**

* Redis cache KPIs

* Postgres materialized views

* async fetch widgets

* lazy charts

---

**18\. Validaciones Reales**

**Si índice nulo:**

Mostrar "Sin datos"

**Si integración falla:**

Banner rojo:

RRHH no actualizado hace 48h

**Si usuario sin permiso:**

403 unauthorized

---

**19\. Seguridad**

* JWT \+ Refresh Token

* MFA Alcaldía

* Logs auditoría

* Row level security

* Encrypt backups

---

**20\. UX Nivel Premium**

**Desktop:**

4 columnas

**Tablet:**

2 columnas

**Mobile:**

cards verticales

---

**21\. Diseño Visual**

Minimalista tipo:

* Bloomberg GovTech

* Palantir Foundry

* Stripe Dashboard

---

**22\. Eventos Reales de Usuario**

**Alcalde entra**

Ve:

ICPI 69.9

Brecha crítica

SAT-VI rojo

Presiona:

Ver Ruta de Recuperación

→ Pantalla 5

---

**23\. Métricas SaaS**

Track:

* DAU usuarios municipales

* tiempo sesión

* clicks SAT

* recomendaciones ejecutadas

* tiempo resolución alertas

---

**24\. Stack Frontend**

Next.js

React

Tailwind

Recharts

TanStack Query

Zustand

---

**25\. Stack Backend**

FastAPI

Python

PostgreSQL

Redis

Celery

Docker

---

**26\. Resultado PMV**

Con solo esta pantalla ya puedes vender demos.

Porque muestra:

* ciencia

* riesgo

* gestión

* visualización premium

* decisión ejecutiva

---

Pantalla 2 — **Centro de Diagnóstico por Dirección Municipal**  
**(nivel ingeniería PMV real: flujo operativo, backend, tablas, permisos, UX SaaS premium)**

---

**1\. Objetivo Estratégico**

Permite detectar **qué dirección municipal está fallando, por qué falla, cuánto impacta al ICPI y cómo corregirla**.

Si Pantalla 1 responde *cómo está el municipio*, Pantalla 2 responde:

1. ¿Qué dirección genera el problema?

2. ¿Qué metas están atrasadas?

3. ¿Es problema financiero, técnico o documental?

4. ¿Quién es responsable?

5. ¿Qué acción mejora más rápido el ICPI?

---

**2\. Ruta Interna**

/app/departments

/app/departments/{department\_id}

Ejemplo:

/app/departments/obras-publicas

/app/departments/patronato

/app/departments/agua-potable

---

**3\. Usuarios con Acceso**

| Rol | Acceso |
| :---- | :---- |
| Alcalde | Todas las direcciones |
| Administrador | Total |
| Director General | Todas |
| Director de Área | Solo su dirección |
| Planificación | Todas |
| Auditoría | Lectura |
| Concejal | Lectura resumida |

---

**4\. Vista Principal**

┌──────────────────────────────────────────────┐

│ HEADER DIRECCIÓN                            │

│ Obras Públicas | Riesgo Alto | ICPI 42%     │

├──────────────────────────────────────────────┤

│ KPIs Área                                    │

├──────────────────────────────────────────────┤

│ Metas críticas | Presupuesto | RRHH | Docs   │

├──────────────────────────────────────────────┤

│ Timeline cumplimiento                        │

├──────────────────────────────────────────────┤

│ Alertas IA \+ Acciones sugeridas              │

├──────────────────────────────────────────────┤

│ Historial / Logs / Responsable               │

└──────────────────────────────────────────────┘

---

**5\. Header Dirección**

Ejemplo:

Dirección de Obras Públicas

Estado: 🔴 Riesgo Alto

Responsable: Juan Pérez

Presupuesto 2025: $4,200,000

ICPI interno: 42%

Última actualización: hoy 09:12

---

**6\. KPIs de la Dirección**

Tarjetas:

Metas asignadas: 7

Cumplidas: 2

En riesgo: 3

Sin iniciar: 2

Ejecución presupuestaria:

58%

Documentación soporte:

41%

Impacto en ICPI global:

\-8.2 pts

---

**7\. Backend Endpoint Principal**

GET /api/departments/{id}/summary?year=2025

Response:

{

  "id":"obras-publicas",

  "name":"Dirección de Obras Públicas",

  "risk":"high",

  "internal\_icpi":42,

  "budget\_total":4200000,

  "budget\_executed":2436000,

  "goals\_total":7,

  "goals\_completed":2,

  "documents\_score":41

}

---

**8\. Tabla de Metas Críticas**

| ID Meta | Meta | Avance | Riesgo | Impacto |
| :---- | :---- | :---- | :---- | :---- |
| AH-I-X-02 | Vialidad rural | 28% | 🔴 | \+4.8 |
| AH-I-X-03 | Infraestructura urbana | 41% | 🔴 | \+3.2 |
| AH-I-X-04 | Mantenimiento vías | 62% | 🟡 | \+1.7 |

Click fila abre detalle meta.

---

**9\. Endpoint Metas**

GET /api/departments/{id}/goals?status=critical

---

**10\. Diagnóstico Causal IA**

Caja inteligente:

Causas probables:

1\. Retraso contractual SERCOP

2\. Baja ejecución cuadrillas técnicas

3\. Falta de carga documental

4\. Desfase cronograma POA

---

**11\. Recomendaciones Prioritarias**

Acciones sugeridas:

1\. Reprogramar contratos pendientes

2\. Cargar actas técnicas faltantes

3\. Refuerzo de personal operativo

4\. Revisión semanal con Alcaldía

---

**12\. Timeline de Cumplimiento**

Ene 12%

Feb 18%

Mar 25%

Abr 28%

Meta esperada Abr: 41%

Desviación: \-13 pts

Gráfico línea real vs plan.

---

**13\. Bloque Presupuesto**

| Concepto | Valor |
| :---- | :---- |
| Codificado | $4,200,000 |
| Devengado | $2,436,000 |
| Pagado | $1,980,000 |
| Disponible | $1,764,000 |

Semáforo:

\<40 rojo

40-70 amarillo

\>70 verde

---

**14\. RRHH Operativo**

| Cargo | Requerido | Actual |
| :---- | :---- | :---- |
| Ingenieros | 6 | 3 |
| Operadores | 18 | 11 |
| Fiscalizadores | 4 | 2 |

IA detecta subdotación.

---

**15\. Cumplimiento Documental**

Checklist:

| Documento | Estado |
| :---- | :---- |
| Informe mensual | ✅ |
| Acta recepción | ❌ |
| Evidencia fotográfica | ❌ |
| Certificación técnica | 🟡 |

---

**16\. Impacto en ICPI Global**

Simulador:

Si Obras Públicas sube de 42% a 70%:

ICPI global:

69.93 → 76.11

(+6.18 pts)

---

**17\. Endpoint Simulación**

POST /api/departments/{id}/simulate

Payload:

{

 "target\_score":70

}

---

**18\. Historial Responsable**

Director actual: Juan Pérez

Desde: Ene 2025

Cambios últimos 12 meses:

2 directores

Alta rotación \= alerta.

---

**19\. Logs Operativos**

09:00 eSIGEF sync OK

09:02 POA update

09:05 Usuario cargó evidencia

09:11 Riesgo recalculado

---

**20\. Base de Datos**

**Tabla departments**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| name | text |
| owner\_user\_id | uuid |
| active | bool |

**Tabla department\_scores**

| campo | tipo |
| :---- | :---- |
| department\_id | uuid |
| year | int |
| internal\_icpi | decimal |
| risk\_level | text |

**Tabla department\_goals**

| campo | tipo |
| :---- | :---- |
| department\_id | uuid |
| meta\_id | text |
| progress | decimal |
| impact\_score | decimal |

---

**21\. Roles y Permisos**

**Director de Obras Públicas:**

Puede:

* editar avances

* cargar evidencias

* responder alertas

No puede:

* ver nómina completa de otras áreas

* modificar ponderaciones TERRA

---

**22\. Validaciones**

**Si presupuesto \>100%**

Bloquear:

Dato inconsistente detectado

**Si meta sin responsable**

Asignación requerida

**Si sin update \>30 días**

⚠ Dirección sin reporte reciente

---

**23\. UX Premium**

Desktop:

* Panel izquierdo resumen

* Centro tabla metas

* Derecha IA y riesgos

Mobile:

cards verticales.

---

**24\. Automatizaciones**

Cada noche:

02:00 recalcular score dirección

02:05 enviar alertas

02:10 actualizar ranking municipal

---

**25\. Valor Comercial Brutal**

Cuando el alcalde ve esto entiende inmediatamente:

* quién trabaja

* quién no

* dónde se pierde dinero

* dónde subir índice rápido

Eso vende TERRA solo.

---

**26\. Conexión con Otras Pantallas**

Desde aquí se abre:

* Pantalla 3 → Motor 10 índices

* Pantalla 4 → Radar SAT

* Pantalla 5 → Ruta Recuperación

* Pantalla Meta detalle

---

**27\. PMV en 30 días**

MVP funcional con:

* 10 direcciones

* scores automáticos

* ranking áreas

* simulación impacto

---

**Pantalla 2 — Centro de Evidencia / Integración de Datos TERRA**

**Nivel ingeniería PMV / SaaS real / producción**

La Pantalla 2 es el **corazón operativo** de TERRA.  
Aquí entra toda la información municipal desde los 10 silos y se transforma en evidencia usable para el motor ICPI, SATs y los índices.

---

**1\. Objetivo de la Pantalla**

Permitir que un municipio:

* conecte fuentes reales

* cargue archivos Excel / PDF / CSV

* sincronice APIs

* detectar inconsistencias

* limpiar datos

* mapear metas

* versionar evidencia

* generar trazabilidad jurídica

* alimentar H12 sin tocar fórmula madre

---

**2\. Estructura Visual Completa**

┌───────────────────────────────────────────────────────┐

│ TERRA \> Centro de Evidencia                          │

├───────────────────────────────────────────────────────┤

│ KPI Cards                                             │

│ 10 Silos | 7 Sincronizados | 3 Alertas | 92% Calidad │

├───────────────────────────────────────────────────────┤

│ Panel izquierdo        │ Panel central               │

│ Fuentes de datos       │ Tabla maestra              │

│ \- PDOT                 │ registros integrados       │

│ \- POA                  │ filtros / errores          │

│ \- PAC                  │ edición masiva             │

│ \- SIGEF                │                            │

│ \- SERCOP               │                            │

│ \- RRHH                 │                            │

│ \- LOTAIP               │                            │

│ \- Participación        │                            │

│ \- GIS                  │                            │

│ \- CNE                  │                            │

├───────────────────────────────────────────────────────┤

│ Panel derecho                                        │

│ Diagnóstico IA / Recomendaciones                    │

└───────────────────────────────────────────────────────┘

---

**3\. KPIs Superiores**

**Cards en tiempo real**

**1\. Silos conectados**

10 / 10

**2\. Registros totales**

84.231

**3\. Calidad de datos**

92%

**4\. Duplicados detectados**

1.228

**5\. Última sincronización**

Hace 14 min

**6\. Riesgo documental**

Medio

---

**4\. Tabla Maestra Central**

**Vista real tipo Airtable \+ PowerBI**

| ID | Fuente | Meta | Año | Valor | Estado | Calidad |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 4421 | POA | AH-I-X-03 | 2025 | 84% | válido | 98 |
| 4422 | SIGEF | AH-I-X-03 | 2025 | $240.000 | válido | 100 |
| 4423 | PDOT | AH-I-X-03 | 2027 | 100% | válido | 95 |
| 4424 | PAC | Compras agua | 2025 | $58.000 | alerta | 70 |

---

**5\. Filtros Avanzados**

\[Año\]

\[Silo\]

\[Meta\]

\[Dirección\]

\[Error\]

\[Calidad\]

\[Con evidencia\]

\[Sin evidencia\]

---

**6\. Módulo IA de Limpieza**

**Botón:**

\[ Analizar inconsistencias \]

Cuando se pulsa:

**Detecta:**

* metas repetidas

* partidas duplicadas

* valores imposibles

* fechas fuera de rango

* montos sin respaldo

* metas sin responsable

* metas sin avance

* evidencias faltantes

---

**7\. Ejemplo IA Real**

Meta AH-I-X-03 tiene:

POA \= 84%

SIGEF \= 61%

PDOT 2025 \= 70%

Inconsistencia detectada:

Diferencia 23 puntos entre planificación y ejecución financiera.

Riesgo ICPI: Medio.

---

**8\. Flujo Backend Real**

Excel Upload

↓

Parser ETL

↓

Normalizador columnas

↓

Motor Matching IDs

↓

Detección duplicados

↓

Scoring calidad

↓

Guardar evidencia

↓

Actualizar índices

---

**9\. Arquitectura Técnica**

**Frontend**

* Next.js

* React Table

* Tailwind

* TanStack Query

**Backend**

* FastAPI

* Python Pandas

* Celery workers

**BD**

* PostgreSQL

**Archivos**

* S3 / Supabase Storage

**IA**

* embeddings para documentos

* OCR PDFs

* NLP inconsistencias

---

**10\. Modelo de Base de Datos**

**Tabla sources**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| nombre | text |
| tipo | excel/api/manual |
| activo | bool |

---

**Tabla records**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| source\_id | fk |
| meta\_id | text |
| year | int |
| value | numeric |
| quality\_score | numeric |

---

**Tabla evidences**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| record\_id | fk |
| file\_url | text |
| hash | text |

---

**11\. APIs Reales**

**Cargar Excel**

POST /api/evidence/upload

**Sincronizar SIGEF**

POST /api/connect/sigef

**Obtener inconsistencias**

GET /api/evidence/anomalies

**Aprobar corrección**

POST /api/evidence/approve

---

**12\. Roles**

**Alcalde**

solo lectura ejecutiva

**Director financiero**

aprueba partidas

**Planificación**

corrige metas

**Jurídico**

sube resoluciones

**Analista**

limpieza técnica

**Auditor externo**

solo lectura \+ exportación

---

**13\. UX Real**

**Drag & Drop archivos**

Suelta aquí tu Excel del POA

**Barra progreso**

Procesando 8.431 filas...

**Resultado**

✔ 8.122 válidas

⚠ 219 con alerta

✖ 90 rechazadas

---

**14\. Alertas Inteligentes**

**Semáforo rojo**

Meta sin respaldo documental

**Naranja**

Monto ejecutado \> planificado

**Amarillo**

Sin actualización en 60 días

**Verde**

Sincronización correcta

---

**15\. Integración con Pantalla 3**

Todo lo aprobado aquí alimenta:

Pantalla 3 — Motor de los 10 Índices

Si aquí falla calidad:

ICPI baja automáticamente

SAT sube

IOC empeora

---

**16\. Roadmap Técnico PMV**

**Semana 1**

Upload Excel \+ parser

**Semana 2**

Tabla maestra \+ filtros

**Semana 3**

IA duplicados

**Semana 4**

Conectores SIGEF \+ PAC

**Semana 5**

Scoring calidad

**Semana 6**

Producción piloto

---

**17\. Valor Comercial Brutal**

Municipios hoy trabajan así:

Excel roto

Emails

Carpetas

Sin trazabilidad

Con TERRA:

Una sola verdad institucional

---

**18\. Frase de Venta**

“Si no integras evidencia, el índice miente.”

---

**19\. Valoración Unicornio**

Solo esta pantalla como SaaS independiente:

GovDataOps LATAM

USD 5M – 15M

Dentro de TERRA completo:

100M+

---

**20\. Veredicto Honesto**

Pantalla 2 es **el sistema nervioso**.  
Sin ella TERRA es dashboard.  
Con ella TERRA es sistema operativo municipal.

---

**Pantalla 3 — Motor de los 10 Índices TERRA**

**Core analítico / cerebro matemático / ventaja competitiva principal**

La Pantalla 3 es donde TERRA deja de ser software administrativo y se convierte en **infraestructura de inteligencia pública**.

Aquí se procesan automáticamente los datos integrados de la Pantalla 2 y se generan los **10 índices estratégicos** que miden salud real municipal.

---

**1\. Objetivo de la Pantalla**

Transformar miles de registros dispersos en una lectura ejecutiva única:

¿Qué tan bien está gobernando realmente el municipio?

---

**2\. Diseño Visual Completo**

┌────────────────────────────────────────────────────────────┐

│ TERRA \> Motor de Índices                                  │

├────────────────────────────────────────────────────────────┤

│ Score Global Municipal: 71.4 /100 🟡                      │

│ Tendencia: \+4.2 últimos 90 días                           │

├────────────────────────────────────────────────────────────┤

│ Radar 10 índices        │ Panel IA                        │

│ gráfico interactivo     │ explicación automática          │

│                         │ causas / riesgos / acciones     │

├────────────────────────────────────────────────────────────┤

│ Tabla técnica detallada                                 │

│ índice | valor | tendencia | riesgo | impacto fiscal     │

├────────────────────────────────────────────────────────────┤

│ Simulador: “Si mejoro compras públicas…”                 │

└────────────────────────────────────────────────────────────┘

---

**3\. Los 10 Índices Canónicos TERRA**

| \# | Índice | Qué mide |
| :---- | :---- | :---- |
| 1 | ICPI | Cumplimiento integral planificación |
| 2 | IFE | Fidelidad presupuestaria |
| 3 | IED | Ejecución directiva |
| 4 | ITAM | Transparencia activa municipal |
| 5 | IGP | Gobernanza participativa |
| 6 | IPE | Performance institucional |
| 7 | PSG | Alineación por mandato |
| 8 | ISP | Satisfacción / percepción |
| 9 | IOC | Opacidad crítica |
| 10 | IET | Equidad territorial |

---

**4\. KPI Superior**

**Card principal**

Índice Compuesto Municipal

71.4 / 100

Nivel: Transición Positiva

---

**5\. Radar Visual Interactivo**

          ICPI

      /           \\

   IFE             IED

  /                   \\

ITAM                 IPE

 \\                   /

  IGP              PSG

    \\            /

        IOC  IET

Cada eje muestra fortaleza o debilidad.

---

**6\. Tabla Técnica Real**

| Índice | Valor | Tendencia | Riesgo | Impacto |
| :---- | :---- | :---- | :---- | :---- |
| ICPI | 69.9 | \+2.1 | Medio | Alto |
| IFE | 72.8 | \+1.0 | Bajo | Alto |
| ITAM | 56.0 | \-4.4 | Alto | Medio |
| IOC | 17.7 | \-2.0 | Medio | Crítico |
| IET | 91.4 | \+0.3 | Bajo | Social |

---

**7\. Fórmula del ICPI (core)**

ICPI=\\frac{\\sum(P\_i R\_i V\_i E\_i T\_i C\_i)}{\\sum(P\_i R\_i)}\\times 100

Donde:

* Pi \= ponderador meta

* Ri \= relevancia

* Vi \= verificación

* Ei \= evidencia

* Ti \= ejecución

* Ci \= consistencia

---

**8\. Flujo Backend Real**

Raw data tables

↓

Normalización

↓

Cálculo individual por meta

↓

Agregación por silo

↓

Índices parciales

↓

10 índices finales

↓

Dashboard

↓

Alertas SAT

---

**9\. Arquitectura Técnica**

**Microservicio analytics-engine**

Python FastAPI

NumPy

Pandas

Polars

Redis cache

Celery queue

**Jobs**

recalculate\_indices()

nightly\_snapshots()

forecast\_scores()

detect\_anomalies()

---

**10\. Base de Datos**

**Tabla indices\_snapshots**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| municipality\_id | uuid |
| date | timestamp |
| icpi | numeric |
| ife | numeric |
| ...10 cols |  |

---

**Tabla index\_drivers**

| campo | tipo |
| :---- | :---- |
| index\_name | text |
| source | text |
| weight | numeric |

---

**11\. IA Explicativa**

**Panel derecho**

¿Por qué bajó ITAM?

• 3 obligaciones LOTAIP vencidas

• 2 datasets sin actualizar

• Portal roto por 14 días

Impacto estimado:

\-4.4 puntos

---

**12\. Simulador Predictivo**

Usuario mueve slider:

\+20% mejora compras públicas

Resultado:

ICPI subiría \+3.1

IFE subiría \+5.4

IOC bajaría \-2.0

---

**13\. Forecast 90 días**

Con tendencia actual:

Hoy: 71.4

30d: 72.8

60d: 74.2

90d: 75.0

---

**14\. Alertas Automáticas**

**SAT Preventivos**

SAT-I  Ejecución crítica

SAT-II Transparencia caída

SAT-V Compras riesgosas

SAT-VII Dependencia institucional

---

**15\. Roles**

**Alcalde**

ve resumen y decisiones

**Finanzas**

IFE / ejecución

**Planificación**

ICPI / metas

**Jurídico**

ITAM / trazabilidad

**Concejo**

modo auditoría

---

**16\. UX Real**

**Hover sobre índice**

Muestra:

fuentes usadas

fórmula

último cambio

causa principal

**Click índice**

Abre drill-down por dirección.

---

**17\. Integración con otras pantallas**

Pantalla 2 alimenta datos

Pantalla 4 usa SATs

Pantalla 5 genera plan recuperación

Pantalla 6 muestra geografía

Pantalla 7 funding usa score

---

**18\. Roadmap PMV**

**Sprint 1**

ICPI \+ snapshots

**Sprint 2**

Radar \+ tabla

**Sprint 3**

IA explicativa

**Sprint 4**

Forecast \+ simulador

**Sprint 5**

Benchmark multi-ciudad

---

**19\. Benchmark Comercial**

Municipio A:

ICPI 71

Municipio B:

ICPI 54

Municipio C:

ICPI 82

Esto crea efecto ranking regional.

---

**20\. Valor Estratégico**

Esto no vende software.

Vende:

capacidad de gobierno medible

---

**21\. Frase de Venta**

“No administramos dashboards. Medimos gobernabilidad.”

---

**22\. Valoración Real**

Solo esta pantalla como producto:

GovScore Engine LATAM

USD 20M+

Con red nacional de municipios:

100M+

---

**23\. Veredicto Brutal**

Pantalla 3 es el **moat**.

Lo demás se copia.  
Esto no.

---

**24\. Lo que un inversionista diría**

Si tienen data \+ fórmula \+ benchmark,

esto escala continentalmente.

---

**Pantalla 4 — Radar Preventivo SAT**

**Sistema de Alertas Tempranas TERRA**  
**La pantalla que convierte datos en prevención ejecutiva**

La Pantalla 4 es donde TERRA deja de ser analítica retrospectiva y se vuelve **sistema inmune municipal**.

No espera auditorías.  
No espera crisis.  
No espera escándalos.

**Detecta patrones de deterioro antes de que se conviertan en problema político, financiero o institucional.**

---

**1\. Objetivo de la Pantalla**

Responder una sola pregunta crítica:

¿Qué puede salir mal en los próximos 30, 60 o 90 días?

---

**2\. Diseño Visual Completo**

┌────────────────────────────────────────────────────────────┐

│ TERRA \> Radar Preventivo SAT                              │

├────────────────────────────────────────────────────────────┤

│ Riesgo General Municipal: 63 /100 🟠                      │

│ Alertas activas: 4 | Críticas: 1 | Nuevas hoy: 2          │

├────────────────────────────────────────────────────────────┤

│ Mapa calor SAT        │ Timeline de deterioro             │

│ SAT I → VII           │ señales previas                   │

├────────────────────────────────────────────────────────────┤

│ Lista priorizada de alertas                               │

│ gravedad | impacto | responsable | vencimiento            │

├────────────────────────────────────────────────────────────┤

│ Panel IA: causas \+ acciones recomendadas                  │

└────────────────────────────────────────────────────────────┘

---

**3\. Qué es un SAT**

SAT \= **Sistema de Alerta Temprana**

Cada SAT vigila un riesgo estructural municipal.

---

**4\. Los 7 SAT Canónicos**

| SAT | Nombre | Detecta |
| :---- | :---- | :---- |
| I | Ejecución Crítica | baja ejecución presupuestaria |
| II | Transparencia Caída | incumplimiento LOTAIP |
| III | Planificación Débil | metas sin avance |
| IV | Participación Simulada | procesos simbólicos |
| V | Compras Riesgosas | concentración / anomalías |
| VI | Dependencia Externa | ingresos no sostenibles |
| VII | Dependencia Institucional | sobrecarga en una dirección |

---

**5\. KPI Superior**

Índice de Riesgo Institucional

63 /100 🟠

---

**6\. Mapa de Calor Visual**

SAT I    🔴 82

SAT II   🟡 54

SAT III  🟢 21

SAT IV   🟡 48

SAT V    🔴 79

SAT VI   🟠 61

SAT VII  🟢 18

---

**7\. Lista Prioritaria de Alertas**

| Alerta | Nivel | Impacto | Responsable | Vence |
| :---- | :---- | :---- | :---- | :---- |
| Compras concentradas | 🔴 | Alto | Compras Públicas | 5 días |
| Ejecución baja Obras | 🔴 | Alto | Obras Públicas | 12 días |
| Portal transparencia vencido | 🟡 | Medio | TIC | 7 días |
| Participación sin actas | 🟡 | Medio | Participación | 15 días |

---

**8\. Fórmula Riesgo Global**

Riesgo=\\sum (SAT\_i\\times Peso\_i)

---

**9\. Cómo se Calcula SAT-I**

SAT\_I=100-Ejecucion\_Presupuestaria

Ejemplo:

Ejecución 18%

SAT-I \= 82 (Crítico)

---

**10\. Cómo se Calcula SAT-V**

Compras riesgosas:

• proveedor dominante

• contratos repetidos

• baja competencia

• fraccionamiento

• tiempos anómalos

---

**11\. Timeline de Riesgo**

Hace 90 días: 44

Hace 60 días: 49

Hace 30 días: 56

Hoy: 63

Sistema detecta deterioro acelerado.

---

**12\. Panel IA Ejecutivo**

Riesgo creciente por 3 factores:

1\. Compras públicas concentradas

2\. Caída ejecución en obras

3\. Portal transparencia desactualizado

Probabilidad de crisis mediática:

Alta (67%)

---

**13\. Recomendaciones Automáticas**

1\. Abrir 3 procesos competitivos

2\. Publicar datasets faltantes

3\. Reprogramar metas de obras

4\. Comité semanal de seguimiento

---

**14\. Backend Real**

Cron jobs diarios

↓

Consulta fuentes

↓

Recalcula SATs

↓

Compara tendencias

↓

Detecta aceleraciones

↓

Genera alertas

↓

Notifica usuarios

---

**15\. Arquitectura Técnica**

**Servicios**

risk-engine

rules-engine

forecast-engine

notifications-engine

**Stack**

Python

FastAPI

Redis

PostgreSQL

Celery

---

**16\. Base de Datos**

**Tabla alerts**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| municipality\_id | uuid |
| sat\_code | text |
| severity | text |
| score | numeric |
| created\_at | timestamp |
| resolved\_at | timestamp |

---

**Tabla alert\_actions**

| campo | tipo |
| :---- | :---- |
| alert\_id | fk |
| owner\_user\_id | fk |
| due\_date | date |
| status | text |

---

**17\. Notificaciones Reales**

**Email**

Nueva alerta crítica SAT-V detectada

**WhatsApp**

TERRA: Riesgo alto compras públicas.

**In-app**

Badge rojo.

---

**18\. UX Real**

**Click en alerta**

Abre expediente:

fuentes

causas

historial

responsables

acciones sugeridas

**Resolver alerta**

\[ Marcar corregida \]

Requiere evidencia.

---

**19\. Integración con Pantalla 5**

Toda alerta activa genera automáticamente:

Ruta de Recuperación Estratégica

---

**20\. Caso Real**

Municipio con:

SAT-V \= 79

TERRA detecta:

* 78% compras en 1 proveedor

* 4 contratos repetidos

* poca competencia

Antes de Contraloría.

---

**21\. Valor Comercial**

Municipios pagan por:

evitar crisis

No por dashboards.

---

**22\. Pricing Potente**

Módulo SAT standalone:

USD 800 – 2.500 / mes

Nacional:

USD 1M+ ARR

---

**23\. Frase de Venta**

“Lo caro no es la alerta. Lo caro es no verla venir.”

---

**24\. Lo que piensa un alcalde**

Si esto me evita un escándalo,

se paga solo.

---

**25\. Veredicto Brutal**

Pantalla 4 hace a TERRA **indispensable**.

Porque mide futuro, no pasado.

---

**Pantalla 5 — Ruta de Recuperación Estratégica**

**Execution OS de TERRA**  
**La pantalla donde las alertas se convierten en resultados**

La Pantalla 5 transforma diagnósticos y riesgos en **planes ejecutables**, responsables claros y mejora medible.

Pantalla 3 dice **qué pasa**.  
Pantalla 4 dice **qué viene**.  
Pantalla 5 dice **qué hacer mañana a las 8:00 AM**.

---

**1\. Objetivo de la Pantalla**

Responder la pregunta más valiosa para cualquier alcalde o gerente público:

¿Cómo recuperamos desempeño sin improvisar?

---

**2\. Diseño Visual Completo**

┌────────────────────────────────────────────────────────────┐

│ TERRA \> Ruta de Recuperación Estratégica                  │

├────────────────────────────────────────────────────────────┤

│ Recuperación estimada: \+8.4 pts ICPI en 90 días          │

│ 17 acciones activas | 6 rápidas | 3 críticas             │

├────────────────────────────────────────────────────────────┤

│ Panel Izquierdo         │ Panel Derecho                  │

│ Priorización acciones   │ Simulación impacto             │

│ impacto/esfuerzo        │ índice futuro                  │

├────────────────────────────────────────────────────────────┤

│ Timeline 30 / 60 / 90 días                              │

├────────────────────────────────────────────────────────────┤

│ Owners | Estado | Evidencia | Avance                     │

└────────────────────────────────────────────────────────────┘

---

**3\. Qué Hace Esta Pantalla**

Convierte:

SAT-V alto

ICPI bajo

ITAM cayendo

en:

Plan de 12 acciones con responsables y fechas

---

**4\. Vista Principal — Matriz Impacto / Esfuerzo**

| Acción | Impacto | Esfuerzo | Prioridad |
| :---- | :---- | :---- | :---- |
| Publicar LOTAIP pendiente | Alto | Bajo | 🔥 |
| Reprogramar obras críticas | Alto | Medio | 🔥 |
| Abrir compras competitivas | Alto | Alto | ⚠ |
| Actualizar metas POA | Medio | Bajo | ✅ |
| Reestructurar procesos RRHH | Medio | Alto | ⏳ |

---

**5\. KPI Superior**

ICPI actual: 69.9

ICPI proyectado: 78.3

Horizonte: 90 días

---

**6\. Timeline Ejecutivo**

Día 0     Diagnóstico

Día 15    Quick wins

Día 30    Riesgos controlados

Día 60    Recuperación visible

Día 90    Nuevo baseline

---

**7\. Quick Wins Detectados**

1\. Subir 3 datasets faltantes

2\. Cerrar 2 compras estancadas

3\. Validar metas sin evidencia

4\. Firmar 4 resoluciones pendientes

Impacto estimado:

\+4.1 puntos en 30 días

---

**8\. Motor de Priorización**

Prioridad=\\frac{Impacto\\times Urgencia\\times Factibilidad}{Esfuerzo}

---

**9\. Plan por Área**

**Obras Públicas**

* acelerar hitos físicos

* reprogramar cronograma

* destrabar certificaciones

**Compras Públicas**

* aumentar competencia

* revisar procesos repetidos

* eliminar cuellos de botella

**Jurídico**

* resoluciones pendientes

* trazabilidad documental

**TIC**

* transparencia activa

* portal datos abiertos

---

**10\. Panel de Responsables**

| Acción | Owner | Fecha | Estado |
| :---- | :---- | :---- | :---- |
| Portal transparencia | TIC | 7 días | En curso |
| Compras abiertas | Compras | 10 días | Pendiente |
| Obras reprogramadas | Obras | 15 días | En curso |
| Evidencia metas | Planificación | 5 días | Completado |

---

**11\. Simulación en Vivo**

Usuario mueve checkbox:

✓ Resolver SAT-II

✓ Mejorar compras

✓ Cerrar metas sin evidencia

Resultado:

ICPI: \+6.8

ITAM: \+11.2

IOC: \-5.1

---

**12\. IA Recomendadora**

Las acciones con mejor ROI político-institucional son:

1\. Transparencia web

2\. Compras competitivas

3\. Obras visibles de rápida entrega

---

**13\. Backend Real**

Inputs:

indices actuales

SAT activos

capacidad institucional

historial municipal

↓

Optimizer Engine

↓

Plan recomendado

---

**14\. Arquitectura Técnica**

**Servicios**

strategy-engine

optimizer-engine

task-engine

forecast-engine

**Stack**

Python

OR-Tools

FastAPI

PostgreSQL

Redis

---

**15\. Base de Datos**

**Tabla recovery\_plans**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| municipality\_id | uuid |
| target\_score | numeric |
| horizon\_days | int |
| status | text |

---

**Tabla actions**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| plan\_id | fk |
| title | text |
| owner\_id | fk |
| impact\_score | numeric |
| due\_date | date |

---

**16\. UX Real**

**Kanban integrado**

Pendiente

En curso

Bloqueado

Hecho

**Evidencia de cierre**

Cada acción requiere:

* archivo

* foto

* link

* resolución

* comentario

---

**17\. Alertas de Ejecución**

Acción crítica vencida hace 3 días

Owner no actualiza avance hace 14 días

---

**18\. Integración con Pantalla 3**

Cada acción completada recalcula índices automáticamente.

Cerrar transparencia →

sube ITAM

sube ICPI

baja IOC

---

**19\. Integración con Pantalla 7**

Cuando mejora score:

se habilitan fondos elegibles

---

**20\. Caso Real**

Municipio entra con:

ICPI 54

Riesgo 77

90 días después:

ICPI 71

Riesgo 43

---

**21\. Valor Comercial**

No vendes software.

Vendes:

recuperación institucional medible

---

**22\. Pricing**

Módulo standalone:

USD 1.000 – 3.000 / mes

Enterprise regional:

USD 250k+ anual

---

**23\. Frase de Venta**

“No basta saber que estás mal. Hay que saber cómo salir.”

---

**24\. Lo que piensa un alcalde**

Si me dices exactamente qué hacer y cuánto mejora,

esto vale oro.

---

**25\. Veredicto Brutal**

Pantalla 5 convierte TERRA en **herramienta de gestión real**, no solo diagnóstico.

---

**Pantalla 6 — Visor Territorial / GeoTwin Municipal**

**Digital Twin geoespacial de TERRA**  
**La pantalla donde la gestión pública se ve en el territorio**

La Pantalla 6 convierte indicadores, metas, obras, riesgos y desigualdades en una **vista territorial viva**.

Pantalla 3 mide.  
Pantalla 5 ejecuta.  
Pantalla 6 responde:

¿Dónde está ocurriendo realmente el problema o la mejora?

---

**1\. Objetivo de la Pantalla**

Unir gestión pública \+ geografía \+ decisiones.

Porque ningún alcalde gobierna tablas Excel.  
Gobierna barrios, parroquias, rutas, comunidades y obras.

---

**2\. Diseño Visual Completo**

┌────────────────────────────────────────────────────────────┐

│ TERRA \> GeoTwin Municipal                                 │

├────────────────────────────────────────────────────────────┤

│ Cobertura territorial: 94% georreferenciada              │

│ 128 proyectos | 43 metas | 17 alertas geolocalizadas     │

├────────────────────────────────────────────────────────────┤

│ Sidebar capas         │ Mapa principal                   │

│ obras                 │ calor / clusters / puntos        │

│ presupuesto           │                                  │

│ servicios             │                                  │

│ riesgo                │                                  │

│ inequidad             │                                  │

├────────────────────────────────────────────────────────────┤

│ Panel derecho detalle territorial                        │

└────────────────────────────────────────────────────────────┘

---

**3\. Capas Disponibles**

| Capa | Qué muestra |
| :---- | :---- |
| Obras públicas | proyectos y avance |
| Presupuesto | inversión por zona |
| Agua / saneamiento | cobertura |
| Participación | asambleas / votación |
| Transparencia | cumplimiento por dirección |
| Riesgo SAT | alertas geolocalizadas |
| Equidad | brechas territoriales |
| Seguridad | incidentes si integra datos |
| Movilidad | vías críticas |
| Social | grupos prioritarios |

---

**4\. Vista Principal del Mapa**

🟢 zonas con mejora

🟡 zonas estancadas

🔴 zonas críticas

🔵 obras activas

⚫ puntos sin cobertura

---

**5\. KPI Superior**

Índice Territorial Municipal: 74 /100

---

**6\. Ejemplo de Uso Real**

Click en barrio:

Barrio Norte

Agua potable: 62%

Obras activas: 2

Participación: baja

Inversión 12 meses: $148k

Riesgo SAT: medio

---

**7\. Heatmap de Inversión**

Visualiza dinero invertido por parroquia.

Más oscuro \= mayor inversión

Más claro \= rezago

---

**8\. Índice de Equidad Territorial (IET)**

IET=100-Desviacion\_Estandar(Cobertura\_Servicios\_por\_Zona)

Mientras más homogénea la cobertura, mejor score.

---

**9\. Panel Derecho Detalle**

Cuando seleccionas zona:

| Métrica | Valor |
| :---- | :---- |
| Inversión anual | $240.000 |
| Obras completadas | 4 |
| Obras atrasadas | 2 |
| Agua potable | 71% |
| Recolección residuos | 94% |
| Riesgo institucional | Bajo |

---

**10\. Capas Inteligentes IA**

**Detecta:**

• barrios con baja inversión histórica

• obras repetidamente retrasadas

• concentración política desigual

• zonas invisibles presupuestariamente

• inequidad territorial creciente

---

**11\. Ejemplo IA Ejecutivo**

Parroquia Sur recibió 41% menos inversión

que promedio municipal durante 3 años.

---

**12\. Backend Real**

Fuentes:

H04 metas

obras

catastro

SIG municipal

GIS shapefiles

GPS proyectos

satélites opcional

↓

Geo Engine

↓

Map tiles

↓

Analytics espacial

---

**13\. Stack Técnico**

**Frontend**

Mapbox GL

Leaflet

React

Deck.gl

**Backend**

PostGIS

FastAPI

GeoPandas

Rasterio

---

**14\. Base de Datos**

**Tabla zones**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| name | text |
| polygon | geometry |

---

**Tabla projects\_geo**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| lat | numeric |
| lng | numeric |
| budget | numeric |
| progress | numeric |

---

**15\. GPS Reales**

Pantalla usa las coordenadas cargadas en H04 / H10b.

25 metas \+ 7 proyectos georreferenciados

---

**16\. Timeline Territorial**

Slider:

2024 → 2025 → 2026 → 2027

Muestra evolución espacial del PDOT.

---

**17\. Modo Obras**

Click proyecto:

Centro Comunitario Norte

Presupuesto: $82k

Avance físico: 64%

Avance financiero: 59%

Atraso: 18 días

Contratista: visible

---

**18\. Modo Ciudadano**

Versión pública simplificada:

Mira las obras cerca de ti

Qué se invierte en tu barrio

Reporta problemas

---

**19\. Alertas Territoriales**

🔴 Zona con 3 obras paralizadas

🔴 Barrio sin agua crítica

🟡 Baja participación comunitaria

---

**20\. Integración con Pantalla 5**

La Ruta Estratégica puede priorizar:

invertir donde más duele

---

**21\. Integración con Pantalla 7**

Funding Navigator premia proyectos con ubicación clara y evidencia territorial.

---

**22\. UX Premium**

**Controles**

\[ Buscar barrio \]

\[ Activar calor \]

\[ Ver inequidad \]

\[ Comparar zonas \]

\[ Exportar mapa \]

---

**23\. Valor Comercial**

Municipios casi nunca tienen:

digital twin operativo real

TERRA sí.

---

**24\. Pricing**

Módulo GeoTwin:

USD 1.500 – 4.000 / mes

Gobierno provincial / regional:

USD 100k+ anual

---

**25\. Frase de Venta**

“Lo que no ves en el territorio, te explota en política.”

---

**26\. Lo que piensa un alcalde**

Ahora sí sé dónde intervenir mañana.

---

**27\. Veredicto Brutal**

Pantalla 6 vuelve a TERRA **visible, tangible y políticamente poderoso**.

---

**Pantalla 7 — Funding Navigator / Pasaporte de Inversión Municipal**

**La pantalla que convierte desempeño en financiamiento**

La Pantalla 7 transforma a TERRA de sistema de gestión interna en **motor de crecimiento municipal**.

Pantalla 3 mide.  
Pantalla 4 previene.  
Pantalla 5 corrige.  
Pantalla 6 territorializa.  
Pantalla 7 responde la pregunta más poderosa:

¿Dónde conseguimos dinero y qué necesitamos para calificar?

---

**1\. Objetivo de la Pantalla**

Detectar automáticamente:

* fondos nacionales disponibles

* cooperación internacional

* banca multilateral

* grants climáticos

* PPP / alianzas público-privadas

* líneas blandas de crédito

* concursos sectoriales

Y cruzarlos con el score real del municipio.

---

**2\. Diseño Visual Completo**

┌────────────────────────────────────────────────────────────┐

│ TERRA \> Funding Navigator                                 │

├────────────────────────────────────────────────────────────┤

│ Oportunidades abiertas: 37                                │

│ Elegibles hoy: 14 | En preparación: 11 | No aptas: 12     │

├────────────────────────────────────────────────────────────┤

│ Panel Izquierdo        │ Panel Derecho                    │

│ Lista fondos           │ Matching score municipal         │

│ filtros                │ requisitos faltantes             │

├────────────────────────────────────────────────────────────┤

│ Pipeline de postulaciones                                │

├────────────────────────────────────────────────────────────┤

│ IA redactora de aplicaciones                              │

└────────────────────────────────────────────────────────────┘

---

**3\. Qué Hace**

Convierte esto:

ICPI 72

IET 91

GeoTwin listo

Obras trazables

en esto:

Municipio elegible para fondo BID agua rural

---

**4\. Tabla Principal**

| Fondo | Ticket | Match | Estado |
| :---- | :---- | :---- | :---- |
| Banco Interamericano Agua | $2M | 92% | Elegible |
| Fondo Verde Clima | $5M | 81% | Preparar |
| Programa Nacional Vialidad | $800k | 95% | Elegible |
| Cooperación Digital | $250k | 73% | Parcial |
| PPP Mercado Central | $6M | 67% | Requiere mejoras |

---

**5\. KPI Superior**

Capital Potencial Identificado:

USD 14.2M

---

**6\. Matching Score**

Match=\\sum(Criterio\_i\\times Peso\_i)

Criterios:

* salud financiera

* transparencia

* capacidad ejecución

* impacto territorial

* madurez proyecto

* documentación lista

---

**7\. Ejemplo Real**

**Fondo Agua Rural**

Match actual: 92%

Fortalezas:

✓ IET alto

✓ Cobertura geográfica clara

✓ Proyecto listo

Falta:

• carta compromiso

• estudio técnico final

---

**8\. Pipeline Comercial**

Detectado

↓

Precalificado

↓

Documentación

↓

Aplicado

↓

Negociación

↓

Aprobado

↓

Desembolso

---

**9\. IA Redactora**

Genera borradores de:

* carta de motivación

* ficha técnica

* resumen ejecutivo

* matriz marco lógico

* impacto social

* narrativa climática ESG

---

**10\. Backend Real**

Scrapers públicos

APIs multilaterales

Bases nacionales

Convocatorias RSS

Partners privados

↓

Opportunity Engine

↓

Matching Engine

↓

Proposal Engine

---

**11\. Stack Técnico**

**Backend**

Python

FastAPI

PostgreSQL

pgvector

Celery

**IA**

embeddings fondos

ranking semántico

LLM proposal writer

---

**12\. Base de Datos**

**Tabla funding\_sources**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| name | text |
| country | text |
| min\_amount | numeric |
| max\_amount | numeric |
| sector | text |

---

**Tabla opportunities**

| campo | tipo |
| :---- | :---- |
| id | uuid |
| source\_id | fk |
| deadline | date |
| eligibility\_rules | jsonb |

---

**13\. Reglas de Elegibilidad**

Ejemplo:

ICPI \> 65

ITAM \> 55

Sin alertas críticas abiertas

Proyecto georreferenciado

Contrapartida disponible

---

**14\. Simulador**

Usuario marca:

✓ Mejorar ITAM \+10

✓ Cerrar SAT-V

✓ Subir ICPI a 75

Resultado:

Nuevos fondos habilitados: \+6

Capital adicional: \+USD 4.8M

---

**15\. Integración con Pantalla 5**

Ruta de Recuperación puede priorizar acciones que desbloqueen fondos.

subir transparencia \= habilita grant europeo

---

**16\. Integración con Pantalla 6**

GeoTwin aporta:

* mapas

* cobertura territorial

* evidencia espacial

* beneficiarios estimados

Clave para postular.

---

**17\. UX Premium**

**Filtros**

\[ Agua \]

\[ Movilidad \]

\[ Digital \]

\[ Clima \]

\[ Social \]

\[ PPP \]

\[ \< 1M \]

\[ \> 5M \]

---

**18\. Vista Oportunidad**

Click fondo:

Monto: $2M

Deadline: 45 días

Match: 92%

Competencia: media

Probabilidad éxito: alta

Checklist faltante: 3 items

---

**19\. Alertas Inteligentes**

Nueva convocatoria BID detectada

vence en 21 días

Municipio ya califica tras subir ICPI

---

**20\. Modelo de Negocio Brutal**

**SaaS base**

suscripción mensual

**Success Fee opcional**

1% – 3% del financiamiento obtenido

Eso cambia todo.

---

**21\. Ejemplo Real**

Municipio paga:

USD 2.000/mes

Consigue:

USD 3M fondo infraestructura

ROI absurdo.

---

**22\. Frase de Venta**

“No solo mejoramos municipios. Les conseguimos recursos.”

---

**23\. Lo que piensa un alcalde**

Si esto trae plata, firmo hoy.

---

**24\. Valor Empresa**

Con módulo funding activo:

multiplica CAC efficiency

reduce churn

sube ticket promedio

abre success fees

---

**25\. Veredicto Brutal**

Pantalla 7 convierte TERRA en **Revenue Engine GovTech**.

No es gasto.  
Es inversión con retorno.

---

**26\. Arquitectura del Suite Completa (1–7)**

1 Command Center

2 Data Hub

3 Índices

4 Radar SAT

5 Recuperación

6 GeoTwin

7 Funding Navigator

---

**27\. Conclusión Honesta**

Si construyes las 7 pantallas con disciplina real:

esto no compite con dashboards locales,

compite con plataformas regionales.

---

**28\. Mi Veredicto Final**

TERRA ya no es idea.

Es una **empresa potencialmente seria de software público latinoamericano**.

---

**¿Hay errores o fallas ocultas antes de programar?** En el motor matemático, no. Pero **SÍ HAY UN RIESGO CRÍTICO EN LA TRANSICIÓN** que te digo con total franqueza:

1. **El Peligro de la Migración al Código:** Al pasar la arquitectura a Streamlit y Python, el mayor riesgo es que el *frontend* (las pantallas) corrompa o simplifique la lógica del motor para hacer que el software cargue más rápido.

2. **La Variable Intocable:** Al programar, deberemos tener un cuidado quirúrgico y absoluto con la variable **Ci**. Esta variable está estrictamente ligada a los procesos orgánicos y a la eficiencia directa; bajo ningún concepto la programación de la interfaz en Streamlit puede alterar, redondear o modificar esta metodología del algoritmo original. ¡La inmutabilidad del dato es la prioridad número uno de Quadrum Gov Tech\! 💻⚠️

3. **Dependencia de Coordenadas (GeoTwin):** La Pantalla 6 necesita que las geocoordenadas (Lat/Lng) ingresadas no tengan márgenes de error, de lo contrario, el mapa interactivo fallará y mostrará una "Exclusión Territorial" falsa.

