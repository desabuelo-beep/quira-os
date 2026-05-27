# RC-2 — Automatización Institucional QUIRA OS

**GAD Municipal de Montecristi · Holding Municipal**
Versión 1.0 · Completado: 2026-05-18 · Dylus Lab © 2026

---

## Resumen ejecutivo

RC-2 implementa dos capacidades de automatización institucional que hacen que
el sistema funcione de forma autónoma, sin intervención humana para las tareas
administrativas de vigilancia y escalamiento.

> **El sistema vigila aunque nadie lo abra.**

---

## RC-2A — SLA Institucional

### Qué hace
Cada alerta en el sistema tiene un plazo institucional para ser resuelta:
- **Alertas críticas**: 48 horas
- **Advertencias**: 120 horas (5 días)

### Cómo se ve
- **Badge SLA** en cada tarjeta de alerta: muestra tiempo restante y estado
- **Widget de cumplimiento** en Vista Ejecutiva: % de alertas dentro del plazo
- Semáforo: EN_TIEMPO → PROXIMO_VENCER → VENCIDO → ESCALADO

### Archivos involucrados
- `sentinel/sla_db.py` — lógica de cálculo SLA y backfill
- `quira_pages/p_alertas.py` — badge SLA en tarjetas
- `quira_pages/p_ejecutivo.py` — widget cumplimiento SLA

### Principio de diseño
RC-2A es **informativa**: muestra el estado SLA pero no toma decisiones.
Las decisiones de escalamiento las toma RC-2B automáticamente.

---

## RC-2B — Watchdog y Scheduler

### Componente 1: Watchdog de Silencio Operativo
Detecta entidades del Holding que no han cargado evidencia mensual en 7 días.
Genera automáticamente una alerta tipo `silencio` en el sistema.

**Umbral**: 7 días sin upload → alerta automática
**Acción**: genera alerta, calcula SLA, notifica en Centro de Control
**NO hace**: no cierra, no resuelve, no interpreta causas

### Componente 2: Watchdog de Escalamiento SLA
Identifica alertas vencidas (+7 días en VENCIDO) sin resolución.
Las marca como ESCALADO y registra en la bitácora de atención.

**Umbral**: 7 días en VENCIDO sin resolución → auto-escalamiento
**Acción**: escalada=1, sla_status='ESCALADO', nivel='director', timeline event
**NO hace**: no cierra, no resuelve, no interpreta causas

### Componente 3: Scheduler Autónomo
Ejecuta las tareas periódicas en cada sesión autenticada (no usa hilos).

| Tarea | Frecuencia |
|-------|-----------|
| sla_refresh | cada 30 min |
| watchdog_escalamiento | cada 60 min |
| watchdog_silencio | cada 4 horas |

### Componente 4: Digest Ejecutivo Automático
Botón en Vista Ejecutiva que genera el PDF del mes anterior con un clic.
No requiere seleccionar el período — el sistema lo calcula automáticamente.

### Archivos involucrados
- `sentinel/watchdog.py` — watchdog silencio + escalamiento
- `sentinel/scheduler.py` — scheduler oportunista (tick por sesión)
- `sentinel/db_config.py` — tabla `scheduler_log` (migración automática)
- `app.py` — wiring del scheduler en cada sesión autenticada
- `quira_pages/p_ejecutivo.py` — botón Digest Automático

---

## Principio RC-2: Automatización no-decisional

> RC-2B automatiza administración, nunca decisiones.

**Hace automáticamente:**
- Detectar silencio operativo
- Generar alertas institucionales
- Escalar alertas vencidas
- Refrescar estados SLA
- Generar PDFs de período anterior

**NUNCA hace automáticamente:**
- Cerrar alertas
- Resolver situaciones
- Interpretar causas
- Enviar notificaciones externas
- Modificar datos de cédulas

---

## Histórico 2025 — Ingesta masiva completada

Con RC-2 operativo, se realizó la ingesta completa del histórico 2025:

| Entidad  | Meses | Cobertura | Ti dic-2025 |
|----------|-------|-----------|-------------|
| BOMBEROS | 12/12 | 100%      | 16.38% 🟡  |
| EMAI-EP  | 11/12 | 91.7%     | 90.47% 🟢  |
| GAD      | 3/12  | 25% (Q4)  | 72.73% 🟢  |
| PATRONATO| 12/12 | 100%      | 50.00% 🟢  |

**Nota EMAI-EP**: Marzo 2025 no disponible en LOTAIP.
**Nota GAD**: Enero–Septiembre pendientes de obtener del GAD.

### Proceso de ingesta PDF (PATRONATO Ene, Mayo, Dic)
Los 3 meses en formato PDF fueron procesados con `pdfplumber`:
- Extracción de tablas eSIGEF (14 columnas, 105–108 filas/mes)
- Conversión a xlsx en memoria (sin archivo temporal en disco)
- Pipeline estándar: `parse_cedula()` → `ingest_cedula()`

Script: `scripts/ingest_patronato_pdf.py`

---

## Estado de implementación

| Componente | Estado | Fecha |
|------------|--------|-------|
| SLA backfill automático | ✅ Completo | 2026-05-18 |
| Badge SLA en alertas | ✅ Completo | 2026-05-18 |
| Widget cumplimiento Vista Ejecutiva | ✅ Completo | 2026-05-18 |
| Watchdog silencio operativo | ✅ Completo | 2026-05-18 |
| Watchdog escalamiento SLA | ✅ Completo | 2026-05-18 |
| Scheduler autónomo (3 tareas) | ✅ Completo | 2026-05-18 |
| Digest ejecutivo automático | ✅ Completo | 2026-05-18 |
| Ingesta histórico 2025 (35 xlsx) | ✅ Completo | 2026-05-18 |
| Ingesta PATRONATO PDF (3 meses) | ✅ Completo | 2026-05-18 |

---

*Siguiente fase: RC-2C (Centro de Control) / RC-3 (segunda municipalidad)*
*Responsable: Dylus Lab · Arquitecto: Claude (Anthropic)*
*Documento: RC2_AUTOMATIZACION.md v1.0 · 2026-05-18*
