# Ciclo Mensual de Gobernanza — QUIRA Intelligence
**Documento Doctrinal Permanente**
*Establecido: 2026-05-25 · Sprint 3 · Validado por equipo QUIRA*

> El dashboard es la interfaz. El ciclo mensual es el producto.

---

## 1. Por Qué el Ciclo es el Producto Real

QUIRA Intelligence no es un dashboard que muestra datos.
Es una **infraestructura de memoria longitudinal** que convierte documentos institucionales dispersos en trayectoria observable y verificable mes a mes.

El valor diferencial no aparece en el día 1 ni en el snapshot 1.
Aparece en el snapshot 4 — cuando el sistema detecta que D3 lleva 3 períodos consecutivos bajo 60% y activa SAT-III por reincidencia.
Eso no lo puede hacer ningún dashboard estático.

**El ciclo mensual es la unidad mínima de valor.**

---

## 2. Ritmo y Cadencia

| Evento | Cuándo | Duración estimada |
|---|---|---|
| Ejecución del pipeline | Primera semana del mes (días 1-5) | 30-90 minutos |
| Validación analítica | Día 6-7 del mes | 60-120 minutos |
| Entrega GOV al municipio | Día 8-10 del mes | — |
| Archivado en memoria Supabase | Automático al guardar | — |

**Cadencia mínima:** mensual.
**Cadencia recomendada para D3 en crisis:** quincenal.

---

## 3. Los 6 Pasos del Ciclo

```
CAPTURAR → ANALIZAR → COMPARAR → ALERTAR → MEMORIZAR → ENTREGAR
```

### Paso 1 — CAPTURAR (Ops → Pipeline)
**Cuándo:** Días 1-5 del mes  
**Quién:** Operador QUIRA  
**Ambiente:** ⚙ Ops → Pipeline

| Input | Fuente |
|---|---|
| Cédula presupuestaria | eSIGEF / DPE API |
| Contratos activos | SERCOP OCDS |
| Rendición de cuentas | CPCCS portal |
| Métricas TGI/ICPI | Gold Master Excel (canónico) |
| PAC / POA | Transparencia activa (LOTAIP) |

**Output:** Snapshot canónico JSON guardado en `data/snapshots/130801/` + Supabase  
**Tool:** `scripts/run_pipeline.py` → `SnapshotPipeline.run()`  
**Criterio de calidad:** `traceability_score ≥ 0.80` · Gold Master `reliability = 0.99`

---

### Paso 2 — ANALIZAR (RC-M automático)
**Cuándo:** Automático al guardar snapshot  
**Quién:** Sistema  
**Ambiente:** ⚙ Ops (background) → 🏛 GOV (visualización)

Procesos automáticos:
- `longitudinal_engine.build_rcm_table()` → actualiza trayectoria RC-M
- `sat_evaluator.evaluate_sat()` → activa/desactiva alertas SAT
- `longitudinal_engine.detect_trend()` → clasifica MEJORA / DETERIORO / ESTABLE
- `reliability_tracker.get_reliability_dashboard()` → registra confiabilidad de fuentes

**Output:** RC-M actualizado + SAT evaluado + tendencia calculada

---

### Paso 3 — COMPARAR (Diff Engine, validación analítica)
**Cuándo:** Días 6-7 del mes  
**Quién:** Analista QUIRA  
**Ambiente:** 🏛 GOV → Comparación

- `snapshot_diff.compare_snapshots(mes_m-1, mes_m)` → DiffResult
- Clasificación: MEJORA / DETERIORO / ESTABLE / RUPTURA / RECUPERACIÓN / REINCIDENCIA
- SAT-III: si D3 < 60% por 3 períodos consecutivos → alerta reincidente

**Output:** DiffResult validado · informe de brechas y cambios

---

### Paso 4 — ALERTAR (SAT activas → protocolo)
**Cuándo:** Simultáneo con el análisis  
**Quién:** Analista QUIRA + Operator  
**Ambiente:** 🏛 GOV → Alertas SAT

Cada alerta SAT activa tiene triple ancla verificada:
1. **Base legal** (artículo, código, obligación)
2. **Valor observado** (número real, período, fuente)
3. **Base doctrinal QUIRA** (dimensión afectada, riesgo sistémico)

| Nivel riesgo | Protocolo |
|---|---|
| BAJO | Solo registro en memoria |
| MEDIO | Mención en resumen ejecutivo mensual |
| ALTO | Sección dedicada + recomendaciones |
| CRÍTICO | Informe de emergencia + escalamiento |

---

### Paso 5 — MEMORIZAR (Supabase, indestructible)
**Cuándo:** Automático al finalizar pipeline  
**Quién:** Sistema  
**Ambiente:** ⚙ Ops → Snapshots

El snapshot del mes M queda archivado en Supabase con:
- Checksum SHA-256 (integridad)
- `is_active = TRUE` (snapshot vigente)
- Versión Gold Master y fecha de corte
- Historial de snapshots anteriores preservado (`is_active = FALSE`)

**Esta memoria es indestructible y auditable.**
Cada período es un nodo permanente en la trayectoria institucional.

---

### Paso 6 — ENTREGAR (GOV output al municipio)
**Cuándo:** Días 8-10 del mes  
**Quién:** Analista QUIRA → municipio (Viewer/Analyst)  
**Ambiente:** 🏛 GOV → Estado Municipal + RC-M + Alertas

Entregables del ciclo mensual:

| Entregable | Qué contiene | Dónde |
|---|---|---|
| Estado Municipal | ICPI, TGI 5D, riesgo SAT | GOV → Estado Municipal |
| RC-M Actualizado | Trayectoria completa, tendencia | GOV → RC-M Longitudinal |
| Alertas SAT activas | Triple ancla, protocolo | GOV → Alertas SAT |
| Comparación del período | MEJORA/DETERIORO + campos | GOV → Comparación |
| Informe ejecutivo PDF | Resumen analítico [Fase Impact] | 📑 Impact (futuro) |

---

## 4. Flujo por Ambientes

```
⚙ Ops (Operator)
  └── Pipeline ejecutado
  └── Snapshot guardado
      │
      ▼
🏛 GOV (Viewer/Analyst/Operator/Admin)
  └── Estado Municipal (ICPI + TGI)
  └── RC-M actualizado
  └── Alertas SAT activas
  └── Comparación del período
  └── Ejecución Presupuestaria
  └── Trazabilidad fuentes
      │
      ▼ [futuro — cuando ≥6 meses datos]
🌎 Civic (público)
  └── Ciudadanía ve trayectoria simplificada
  └── Aporta evidencia faltante
      │
      ▼ [futuro — cuando Impact esté activo]
📑 Impact
  └── Informe ejecutivo exportable
  └── Policy brief para cooperación
  └── Dashboard multilateral (BID/PNUD/CAF)
```

---

## 5. Escalamiento — Cuándo Actuar Más Allá del Informe

| Condición | Acción |
|---|---|
| D3 Ti < 60% por 3 meses consecutivos (SAT-III) | Informe especial + alerta a Alcaldía |
| ICPI cae > 10pp en un período (RUPTURA) | Reunión técnica QUIRA + municipio |
| Riesgo SAT = CRÍTICO | Informe de emergencia inmediato |
| Gold Master sin actualizar > 60 días | Advertencia en Ops → Gold Master |
| `traceability_score < 0.60` | Revisión de fuentes + diagnóstico |

---

## 6. Hoja de Ruta de Automatización

| Fase | Estado | Descripción |
|---|---|---|
| Manual mensual | **ACTIVO** | Operador ejecuta pipeline manualmente |
| Semi-automático | Sprint 4 | Scheduler semanal + alertas por email |
| Fully automated | Fase 2 | Pipeline automático + notificaciones push |
| Multi-GAD | Fase 3 | Ciclo replicado en Manta + Jipijapa |

---

## 7. El Primer Informe Longitudinal Real

**Condición:** 2 snapshots mensuales guardados en Supabase.

Cuando existan 2 períodos:
- RC-M tiene su primera trayectoria
- Diff Engine tiene su primera comparación real
- El informe longitudinal pasa de simulación a evidencia

**Ese momento es el verdadero nacimiento del producto.**

---

## 8. Lo Que Este Ciclo NO Hace

Para mantener contención doctrinal:

| Fuera del ciclo | Razón |
|---|---|
| Simulación de escenarios | Fase 5 — QUIRA Proyección Contextual |
| Análisis de género / etario | Datos no disponibles en fuentes conectadas |
| Evaluación interna de directores | Modelo SaaS — fuera del PMV |
| Cooperación internacional directa | 📑 Impact — futuro |
| Comparación multi-municipio | Fase 3 — requiere 2+ municipios activos |

---

*MONTHLY_CYCLE.md es documento doctrinal permanente.*
*El ciclo es la doctrina. Las herramientas son reemplazables.*
*QUIRA Intelligence — Dylus Lab © 2026*
