# RC-2.0 — Walkthrough Institucional Completo

**QUIRA OS · GAD Municipal de Montecristi**
Versión RC-2.0 · Dylus Lab © 2026 *(actualizado con RC-2A SLA + RC-2B Watchdog)*

---

## Propósito

Validar end-to-end el flujo institucional completo antes de cualquier demo externa.
Este script detecta: errores UX, textos confusos, estados ambiguos, fricciones innecesarias.

**Regla:** si algo tarda más de 3 clics o requiere explicación, es un problema de UX.

---

## Credenciales para el walkthrough

| Rol             | Usuario    | Contraseña |
|-----------------|------------|------------|
| Alcalde         | alcalde    | quira2026  |
| Analista        | tecnico    | quira2026  |
| Director        | concejal   | quira2026  |

---

## Flujo 1 — Ingesta y detección (rol: Analista)

### Paso 1 · Iniciar sesión como Analista

- [ ] Abrir QUIRA OS en el navegador
- [ ] Ingresar usuario `tecnico` y contraseña `quira2026`
- [ ] Verificar: aparece sidebar con secciones CONTROL, ENTENDER, GOBERNAR
- [ ] Verificar: nombre de rol visible en el panel de sesión
- [ ] **UX:** ¿el login es fluido? ¿hay lag notable?
- [ ] **Texto:** ¿el mensaje de bienvenida es institucional?

### Paso 2 · Centro de Control

- [ ] Navegar a **Centro de Control** (⬡)
- [ ] Verificar: KPIs del sistema visibles (documentos indexados, alertas activas, etc.)
- [ ] Verificar: el estado del sistema NO muestra términos técnicos (sin "API", "LLM", "supabase")
- [ ] **UX:** ¿la pantalla carga en menos de 5 segundos?
- [ ] **Texto:** ¿los labels son institucionales?

### Paso 3 · Ingesta Mensual

- [ ] Navegar a **Ingesta Mensual** (📥)
- [ ] Seleccionar período: Abril 2026
- [ ] Seleccionar entidad: GAD
- [ ] Subir una cédula presupuestaria de prueba (cualquier Excel válido)
- [ ] Verificar: mensaje de confirmación visible, sin términos técnicos
- [ ] Verificar: el archivo aparece en el historial de ingestas
- [ ] **UX:** ¿el proceso de subida es claro? ¿hay indicador de progreso?
- [ ] **Error UX a registrar:** _________________________________

### Paso 4 · Detección de alerta

- [ ] Navegar a **Alertas de Cumplimiento** (🔔)
- [ ] Verificar: aparecen alertas del período demo (Q1 2026)
- [ ] Verificar: semáforos correctos (🔴 GAD Ene, 🟡 BOMBEROS, 🟢 EMAI-EP)
- [ ] Verificar: terminología institucional en títulos y detalles
- [ ] **UX:** ¿se entiende la diferencia entre CRITICA y ADVERTENCIA?
- [ ] **Texto confuso detectado:** _________________________________

---

## Flujo 2 — Gestión de alerta (rol: Analista → Director)

### Paso 5 · Tomar alerta en revisión

- [ ] En Alertas, seleccionar alerta: "Ejecución de inversión baja — Bomberos Enero 2026"
- [ ] Verificar: aparece panel de gestión con estado "Abierta"
- [ ] Verificar: aparece sección "Antecedentes comparables" (si existen patrones)
- [ ] Presionar **Tomar en revisión**
- [ ] Verificar: estado cambia a "En Revisión"
- [ ] Verificar: confirmación visible sin términos técnicos
- [ ] **UX:** ¿el cambio de estado es obvio visualmente?

### Paso 6 · Asignar responsable

- [ ] Navegar a **Ruta de Atención** (🗓)
- [ ] Ubicar la misma alerta (Bomberos Enero)
- [ ] En el campo "Asignar responsable": ingresar "Lic. Carmen Suárez"
- [ ] Seleccionar nivel: "Analista Institucional"
- [ ] Presionar **Asignar**
- [ ] Verificar: confirmación de asignación
- [ ] Verificar: el responsable aparece reflejado en la alerta
- [ ] **UX:** ¿es claro qué hace el campo de asignación?

### Paso 7 · Escalar a nivel superior

- [ ] En la misma alerta, expandir "🔺 Escalar a nivel superior"
- [ ] Seleccionar nivel destino: "Dirección de Área"
- [ ] Ingresar motivo: "Requiere decisión de área para acelerar desembolsos"
- [ ] Presionar **Escalar**
- [ ] Verificar: alerta marcada como escalada (🔺)
- [ ] Verificar: evento registrado en la ruta de atención
- [ ] **UX:** ¿la opción de escalamiento es fácil de encontrar?

### Paso 8 · Registrar resolución

- [ ] Volver a **Alertas de Cumplimiento**
- [ ] Abrir la misma alerta (Bomberos Enero, en revisión)
- [ ] En el campo de resolución, ingresar:
  `"Se aceleró el proceso de certificación presupuestaria. Contratos comprometidos por $89.200."`
- [ ] Verificar: aparece borrador institucional sugerido (si aplica)
- [ ] Presionar **Registrar Resolución**
- [ ] Verificar: estado cambia a "Resuelta (pendiente validación)"
- [ ] **UX:** ¿el campo de resolución es intuitivo?
- [ ] **Texto confuso detectado:** _________________________________

---

## Flujo 3 — Validación y cierre (rol: Director)

### Paso 9 · Validar resolución

- [ ] En **Ruta de Atención**, localizar alerta resuelta
- [ ] Revisar la resolución registrada
- [ ] Presionar **Validar resolución**
- [ ] Verificar: estado cambia a "Validada institucionalmente"
- [ ] Verificar: evento registrado con actor y timestamp
- [ ] **UX:** ¿queda claro que la validación es un acto formal?

### Paso 10 · Archivar — cierre institucional

- [ ] Presionar **Archivar — cierre institucional**
- [ ] Verificar: estado cambia a "Archivada — caso cerrado"
- [ ] Verificar: la alerta desaparece de "Gestión Activa"
- [ ] Verificar: sigue visible en "Ruta de Atención" (timeline completo)
- [ ] **UX:** ¿el usuario entiende que "archivar" es el cierre formal?

---

## Flujo 4 — Vista ejecutiva (rol: Alcalde)

### Paso 11 · Cerrar sesión y entrar como Alcalde

- [ ] Presionar **← Cerrar Sesión**
- [ ] Ingresar usuario `alcalde` y contraseña `quira2026`
- [ ] Verificar: pantalla de inicio muestra Vista Ejecutiva como primer ítem

### Paso 12 · Revisar Vista Ejecutiva

- [ ] Navegar a **Vista Ejecutiva** (🏛)
- [ ] Seleccionar período: Enero 2026
- [ ] Presionar **Actualizar vista ejecutiva**
- [ ] Verificar: aparece semáforo global (🔴 Requiere atención)
- [ ] Verificar: aparece "Resumen para la autoridad" con 4 preguntas
- [ ] Verificar: semáforos por entidad (GAD 🔴, BOMBEROS 🟡, EMAI-EP 🟢, PATRONATO 🔴)
- [ ] Verificar: sección "Requiere atención" lista alertas críticas
- [ ] Verificar: NO aparecen términos técnicos (sin hashes, sin columnas, sin sprints)
- [ ] **UX:** ¿el alcalde puede leer esta pantalla sin ayuda?
- [ ] **Texto confuso detectado:** _________________________________

### Paso 13 · Cambiar período

- [ ] Cambiar a Marzo 2026
- [ ] Presionar **Actualizar**
- [ ] Verificar: semáforo global cambia (debería mejorar vs Enero)
- [ ] Verificar: GAD pasa de 🔴 a 🟡
- [ ] **UX:** ¿el cambio de período es intuitivo?

---

## Flujo 5 — PDF y exportación

### Paso 14 · Descargar Informe Ejecutivo PDF

- [ ] En Vista Ejecutiva, período Enero 2026
- [ ] Presionar **📄 Descargar Informe Ejecutivo (PDF)**
- [ ] Verificar: PDF descargado con nombre institucional (`estado_institucional_202601_...pdf`)
- [ ] Abrir PDF y verificar: portada con nombre del municipio
- [ ] Verificar: secciones legibles sin términos técnicos
- [ ] **UX:** ¿el PDF tiene calidad para presentar a directivos?
- [ ] **Hallazgo en PDF:** _________________________________

### Paso 15 · Exportar registro Excel

- [ ] Navegar a **Centro de Control** (como analista)
- [ ] Buscar botón de descarga del registro mensual
- [ ] Descargar Excel del período
- [ ] Verificar: columnas con nombres institucionales
- [ ] **UX:** ¿el Excel es usable sin conocer el sistema?

---

## Flujo 6 — Ruta de atención (timeline)

### Paso 16 · Revisar bitácora institucional

- [ ] Navegar a **Ruta de Atención** → tab "🗓 Ruta de Atención"
- [ ] Seleccionar alerta: "Ejecución de inversión crítica — GAD Enero 2026" (archivada)
- [ ] Verificar: timeline muestra todos los eventos (detección → revisión → resolución → validación → archivo)
- [ ] Verificar: cada evento tiene actor, timestamp y nota
- [ ] Verificar: el último evento está resaltado
- [ ] **UX:** ¿la timeline es fácil de leer para un director?
- [ ] **Texto confuso detectado:** _________________________________

---

## Flujo 7 — Aprendizaje institucional

### Paso 17 · Actualizar memoria operativa

- [ ] Navegar a **Aprendizaje Institucional** (🧠)
- [ ] Presionar **🔄 Actualizar Aprendizaje**
- [ ] Verificar: KPIs actualizados (resoluciones clasificadas, cobertura %)
- [ ] Verificar: ranking de causas visible (reforma presupuestaria, retraso documental, etc.)
- [ ] Verificar: el lenguaje es institucional (sin "ML", sin "clasificación automática")
- [ ] **UX:** ¿un analista entiende qué hace esta pantalla?

---

## Registro de hallazgos UX

| # | Pantalla         | Descripción del hallazgo        | Severidad | Acción requerida |
|---|------------------|---------------------------------|-----------|------------------|
| 1 |                  |                                 |           |                  |
| 2 |                  |                                 |           |                  |
| 3 |                  |                                 |           |                  |
| 4 |                  |                                 |           |                  |
| 5 |                  |                                 |           |                  |

**Severidades:** 🔴 Bloquea demo · 🟡 Confunde al usuario · 🟢 Mejora menor

---

## Flujo 8 — RC-2A SLA Institucional (rol: Analista / Director)

### Paso 18 · Verificar badge SLA en alertas

- [ ] Navegar a **Alertas de Cumplimiento** (🔔)
- [ ] Verificar: cada alerta muestra un badge de estado SLA (dentro del plazo / próxima a vencer / fuera de plazo)
- [ ] Verificar: badge usa texto institucional (NO muestra "SLA_STATUS" ni términos técnicos)
- [ ] **UX:** ¿el badge es visible sin tener que expandir la alerta?

### Paso 19 · Verificar widget SLA en Vista Ejecutiva

- [ ] Navegar a **Vista Ejecutiva**, período actual
- [ ] Verificar: aparece widget "SLA Institucional — XX% de cumplimiento"
- [ ] Verificar: muestra vencidas, escaladas y próximas a vencer
- [ ] Verificar: semáforo verde/rojo del cumplimiento SLA global
- [ ] **UX:** ¿el alcalde entiende qué significa el porcentaje de cumplimiento SLA?

---

## Flujo 9 — RC-2B Vigilancia Autónoma (rol: Alcalde / Analista)

### Paso 20 · Verificar Digest Ejecutivo Automático

- [ ] En **Vista Ejecutiva**, buscar botón "📊 Digest Automático — [mes anterior]"
- [ ] Presionar el botón
- [ ] Verificar: se genera PDF del mes anterior automáticamente (sin seleccionar período)
- [ ] Verificar: el nombre del archivo refleja el mes anterior correcto
- [ ] **UX:** ¿es claro que el digest es del mes anterior?

### Paso 21 · Verificar Histórico 2025

- [ ] En Vista Ejecutiva, seleccionar Octubre 2025
- [ ] Verificar: semáforos reflejan datos reales (GAD 🟢 61%, EMAI-EP 🟢 78%)
- [ ] Seleccionar Enero 2025
- [ ] Verificar: BOMBEROS en 🔴 (0% inversión), PATRONATO en 🔴 (1.71%)
- [ ] **UX:** ¿el historial 2025 es accesible sin pasos adicionales?

---

## Criterios de aprobación RC-2.0

El walkthrough es exitoso si:

- [ ] Los 21 pasos se completan sin errores de sistema
- [ ] Ningún mensaje visible al usuario contiene términos técnicos prohibidos
- [ ] El PDF se genera correctamente (período activo y digest automático)
- [ ] La Vista Ejecutiva es legible sin explicación para el alcalde
- [ ] El timeline refleja todos los eventos del flujo
- [ ] Badges SLA visibles y con lenguaje institucional
- [ ] Widget SLA en Vista Ejecutiva con % de cumplimiento correcto
- [ ] Digest Automático genera PDF del mes anterior en 1 clic
- [ ] Histórico 2025 accesible (38 cédulas, semáforos reales)
- [ ] Cero mensajes de error inesperados
- [ ] El tiempo total del walkthrough es menor a 25 minutos

---

## Estado del walkthrough

| Fecha | Ejecutado por | Resultado | Hallazgos | Observaciones |
|-------|---------------|-----------|-----------|---------------|
| 2026-05-18 | Dylus Lab | RC-2.0 implementado | 0 bloqueantes | RC-2A+B completo |

---

*Ejecutar este walkthrough antes de toda demo externa.*
*Actualizar la tabla de hallazgos después de cada sesión.*
*Responsable: Equipo Dylus Lab.*
*Ver también: [[RC2_AUTOMATIZACION.md]] para documentación técnica RC-2.*
