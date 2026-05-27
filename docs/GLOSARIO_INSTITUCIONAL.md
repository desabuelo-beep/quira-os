# Glosario Institucional — QUIRA OS

**GAD Municipal de Montecristi · Holding Municipal**
Versión RC-2.0 · Dylus Lab © 2026

---

## Propósito

Este glosario **congela** el lenguaje del sistema.
A partir de RC-1 los términos aquí definidos son la nomenclatura oficial de QUIRA OS.
No se cambian nombres de estados, tabs, semáforos ni categorías sin actualizar este documento.

Regla: **lo que el usuario ya aprendió no se renombra.**

---

## Tabla de equivalencias — Técnico → Institucional

| Término técnico         | Término institucional             | Contexto de uso                                      |
|-------------------------|-----------------------------------|------------------------------------------------------|
| engine / motor          | módulo institucional              | Al referirse internamente a componentes del sistema  |
| workflow                | ruta institucional                | Proceso formal de atención de alertas                |
| snapshot                | corte institucional / registro de estado | Estado del sistema en un período cerrado       |
| learning / ML           | memoria operativa                 | Patrones detectados de resoluciones anteriores       |
| parser                  | validación documental             | Proceso de lectura y verificación de cédulas         |
| scoring / score         | nivel de atención                 | Prioridad calculada de una alerta                    |
| pipeline                | flujo de procesamiento            | Secuencia de validación y carga de datos             |
| hash / SHA256           | huella de integridad              | Verificación de autenticidad de un documento         |
| drift                   | tendencia operativa               | Evolución del indicador en el tiempo                 |
| API                     | sistema analítico                 | Conexión con servicios externos                      |
| LLM / IA generativa     | motor de consulta                 | Componente de respuesta semántica                    |
| embedding / RAG         | búsqueda semántica                | Recuperación inteligente de antecedentes             |
| chunk / token           | fragmento documental              | Unidad de análisis de documentos                     |
| indexar                 | registrar en memoria              | Incorporar documentos al sistema                     |
| alert trigger           | detección automática              | Generación de alerta por el sistema                  |
| threshold / umbral      | parámetro institucional           | Valor límite para activar una alerta                 |
| Ti / Tasa de Inversión  | ejecución de inversión            | Indicador clave de ejecución presupuestaria          |
| estado pendiente        | alerta abierta                    | Alerta detectada, sin asignar                        |
| estado en_revision      | en revisión institucional         | Alerta asignada, bajo análisis                       |
| estado derivada         | derivada a dirección              | Escalada al nivel de área responsable                |
| estado resuelta         | resuelta (pendiente validación)   | Resolución registrada, en espera de validación       |
| estado observada        | observada — resolución insuficiente | Resolución devuelta para complementación           |
| estado validada         | validada institucionalmente       | Resolución aprobada, lista para cierre               |
| estado archivada        | archivada — caso cerrado          | Cierre institucional formal                          |
| owner                   | responsable institucional         | Funcionario asignado a la alerta                     |
| escalamiento            | escalamiento institucional        | Traslado formal a nivel jerárquico superior          |
| timeline / bitácora     | ruta de atención                  | Historial auditado de acciones sobre una alerta      |
| seed / datos demo       | escenario de demostración         | Datos controlados para pruebas y presentaciones      |
| deploy                  | despliegue institucional          | Puesta en producción del sistema                     |
| rollback                | reversión de versión              | Regreso a versión anterior del sistema               |
| debug                   | diagnóstico técnico               | Identificación y corrección de errores               |
| SLA / Service Level     | plazo institucional               | Tiempo máximo para atender una alerta según severidad |
| SLA_STATUS=EN_TIEMPO    | dentro del plazo                  | Alerta con tiempo disponible para resolución          |
| SLA_STATUS=PROXIMO_VENCER | próxima a vencer                | Alerta con < 20% de plazo restante                   |
| SLA_STATUS=VENCIDO      | fuera de plazo                    | Alerta que superó el plazo institucional              |
| SLA_STATUS=ESCALADO     | escalada institucionalmente       | Alerta auto-escalada al director por vencimiento      |
| watchdog / vigía        | vigilancia autónoma               | Módulo que detecta silencio operativo sin intervención|
| silencio operativo      | silencio operativo                | Entidad sin carga de evidencia en período establecido |
| scheduler / planificador| módulo de control automático      | Ejecuta tareas periódicas en cada sesión autenticada  |
| digest / resumen ejecutivo | informe mensual automático    | PDF del período anterior generado automáticamente     |
| escalamiento automático | escalamiento institucional        | Traslado automático a director cuando SLA vence 7d+   |
| tick / ciclo autónomo   | ciclo de control                  | Ejecución periódica del módulo de control automático  |

---

## Nomenclatura de semáforos (congelada)

| Color   | Rango Ti%     | Término institucional            |
|---------|---------------|----------------------------------|
| 🟢 Verde | ≥ 35%         | Dentro de parámetros normales    |
| 🟡 Amarillo | 15% – 34.9% | Requiere seguimiento           |
| 🔴 Rojo  | < 15%         | Requiere atención inmediata      |

---

## Nomenclatura de severidad de alertas (congelada)

| Código    | Término institucional | Visibilidad                          |
|-----------|-----------------------|--------------------------------------|
| CRITICA   | Alerta crítica        | Vista Ejecutiva + Gestión + Alertas  |
| ADVERTENCIA | Advertencia institucional | Gestión + Alertas               |

---

## Nomenclatura de entidades del Holding Municipal (congelada)

| Código     | Nombre completo oficial                             |
|------------|-----------------------------------------------------|
| GAD        | GAD Municipal de Montecristi                        |
| BOMBEROS   | Cuerpo de Bomberos de Montecristi                   |
| EMAI-EP    | Empresa Municipal de Aseo Integral                  |
| PATRONATO  | Patronato Municipal de Amparo Social                |

---

## Nomenclatura de niveles institucionales (congelada)

| Código      | Denominación institucional      |
|-------------|---------------------------------|
| analista    | Analista Institucional          |
| director    | Dirección de Área               |
| financiero  | Dirección Financiera            |
| alcalde     | Despacho del Alcalde            |

---

## Nomenclatura de vistas del sistema (congelada)

| Clave interna  | Etiqueta visible al usuario          | Audiencia principal      |
|----------------|--------------------------------------|--------------------------|
| ejecutivo      | Vista Ejecutiva                      | Alcalde / Directivos     |
| sentinel_hub   | Centro de Control                    | Analista institucional   |
| ingesta        | Ingesta Mensual                      | Analista institucional   |
| historico      | Inteligencia Histórica               | Analista / Director      |
| congruencia    | Congruencia Institucional            | Director / Auditoría     |
| alertas        | Alertas de Cumplimiento              | Analista / Director      |
| gestion        | Ruta de Atención                     | Director / Analista      |
| seguimiento    | Seguimiento Institucional            | Director                 |
| reportes       | Reportes Institucionales             | Alcalde / Director       |
| aprendizaje    | Aprendizaje Institucional            | Analista                 |
| dashboard      | Tablero Ejecutivo                    | Alcalde / Concejal       |

---

## Lo que NO decimos al usuario

Estos términos **nunca aparecen** en la interfaz institucional:

- Supabase / PostgreSQL / SQLite
- Sprint / RC / PMV / prototipo
- LLM / GPT / IA generativa / Claude
- hash / sha256 / token / embedding
- pipeline / trigger / worker
- debug / log / stack trace
- engine / parser / scorer

---

## Frases institucionales clave

| Situación                        | Frase correcta                                                    |
|----------------------------------|-------------------------------------------------------------------|
| El sistema detectó una alerta    | "Se detectó automáticamente una situación que requiere atención." |
| Hubo un error de datos           | "No se pudo procesar la información del período. Verificar archivo." |
| La IA sugiere una resolución     | "El sistema propone un borrador institucional basado en antecedentes comparables." |
| No hay datos del período         | "No se registraron datos para este período. Verificar ingesta mensual." |
| Alerta resuelta y cerrada        | "Alerta archivada. Caso cerrado institucionalmente."              |
| Sistema funcionando bien         | "El municipio opera dentro de los parámetros institucionales."    |

---

---

## SLA institucional (congelado RC-2A)

| Severidad        | Plazo máximo | Término visible al usuario                      |
|------------------|--------------|-------------------------------------------------|
| Alerta crítica   | 48 horas     | "Esta alerta vence en menos de 48 horas."       |
| Advertencia      | 120 horas    | "Esta advertencia tiene 5 días para resolverse." |

**Estados SLA visibles al usuario:**

| Estado interno   | Frase institucional                                        |
|------------------|------------------------------------------------------------|
| EN_TIEMPO        | "Dentro del plazo institucional"                           |
| PROXIMO_VENCER   | "Próxima a vencer — requiere acción urgente"               |
| VENCIDO          | "Fuera de plazo — requiere escalamiento"                   |
| ESCALADO         | "Escalada al director de área"                             |

---

## Datos reales 2025 — Ti por entidad (ingesta Sentinel)

| Entidad  | Dic 2025 | Cierre año |
|----------|----------|------------|
| BOMBEROS | 16.38%   | 🟡 AMARILLO |
| EMAI-EP  | 90.47%   | 🟢 VERDE    |
| GAD      | 72.73%   | 🟢 VERDE (Q4 únicamente) |
| PATRONATO| 50.00%   | 🟢 VERDE    |

---

*Actualizar este glosario cada vez que se introduce un término nuevo visible al usuario.*
*Responsable: Equipo Dylus Lab.*
*Actualizado: RC-2.0 — 2026-05-18 — SLA + Watchdog + Histórico 2025*
