# QUIRA OS — Sprint 3: Consolidación Operacional
**Estado: PLANIFICADO** · Inicio estimado: semanas 5-8 (Jun–Jul 2026)

---

## Objetivo del Sprint

Pasar de:

> **"pipeline funcional"**

a:

> **"sistema institucional confiable con memoria longitudinal"**

---

## Regla Arquitectural Establecida (Sprint 3 en adelante)

> El sidebar tiene MÁXIMO 7 módulos.
> Toda nueva vista = tab dentro del módulo correspondiente.
> Nunca un nuevo item de sidebar para una sub-feature.

**Módulos canónicos:**
| Módulo | Roles | Tabs actuales |
|---|---|---|
| Inicio | Todos | — (página única) |
| Situación | Todos | Vista Ejecutiva · Pulso · Brecha |
| Alertas | Todos | SAT activas · **[Sprint 3: Evolución Longitudinal]** |
| Municipal | Todos | Grupo · Participación · Transparencia · Inversión |
| Análisis | Concejal+Técnico | Tablero · Eficiencia · Metas · Cadena · Operación |
| Control | Técnico | Centro · Carga · Ingesta · Historial · Monitor · Reportes · **[Sprint 3: Diff Engine · GM Governance]** |
| Proyector | Todos | Simulador |

---

## PRIORIDAD 1 — Longitudinal Engine (RC-M)

**Por qué ahora:** Ya hay snapshots guardados. Sin este motor QUIRA es solo "foto", no "trayectoria".

### Entregables:
- `app/services/longitudinal_engine.py`
  - `get_snapshot_history(municipio_code, limit=12)` → lista de snapshots ordenados
  - `build_trend(municipio_code, metric_path)` → serie temporal de una métrica
  - `get_rc_m_data(municipio_code)` → tabla RC-M canónica (fecha, ICPI, D3, SAT-IV, Riesgo)

- Tab "📈 Evolución Longitudinal" en `m2_alertas.py`
  - Tabla RC-M: Período | ICPI | D3 (Ti) | SAT-IV | Riesgo ponderado
  - Gráfico línea: tendencia ICPI por período
  - Badge: deterioro / mejora / estable

### Formato RC-M canónico:
```
Período | ICPI  | D3 (Ti)  | SAT-IV   | Riesgo
Mayo    | 53.56% | 14.58%  | ACTIVA   | ALTO
Junio   | 58.10% | 32.00%  | ACTIVA   | MEDIO
Julio   | 64.20% | 55.00%  | mitigada | MEDIO
```

### Tests:
- `tests/test_longitudinal_engine.py`

---

## PRIORIDAD 2 — Snapshot Diff Engine

**Por qué:** Detectar automáticamente deterioro, mejora, reincidencia, ruptura.

### Entregables:
- `app/services/snapshot_diff.py`
  - `compare_snapshots(snap_a: dict, snap_b: dict)` → `DiffResult`
  - `DiffResult`: campos cambiados, dirección (mejora/deterioro), magnitud, alertas nuevas, alertas mitigadas
  - Clasificaciones: MEJORA / DETERIORO / ESTABLE / RUPTURA / RECUPERACIÓN / REINCIDENCIA

- Tab "🔍 Comparación" en `m2_alertas.py` (semana 2)
- Alimenta SAT longitudinal: si D3 < 60% por 3 períodos consecutivos → SAT-III REINCIDENTE

### Tests:
- `tests/test_snapshot_diff.py`

---

## PRIORIDAD 3 — Source Reliability Governance

**Por qué:** La "densidad de trazabilidad pública" es un indicador institucional en sí mismo.

### Entregables:
- Persistir `traceability_score` y `source_reliability` en cada snapshot (ya existe en esquema)
- `app/services/reliability_tracker.py`
  - `get_reliability_history(municipio_code)` → evolución de confiabilidad por fuente
  - `get_reliability_dashboard()` → tabla de fiabilidad por fuente

| Fuente | Reliability | Estado |
|---|---|---|
| Gold Master | 0.99 | Canónico |
| DPE API | 0.95 | Operativo |
| SERCOP | 0.95 | Operativo |
| CPCCS | 0.80 | Funcional |
| Evidencia social | 0.45 | Manual |

- Tab "📡 Confiabilidad" en `m5_control.py`

---

## PRIORIDAD 4 — Gold Master Governance Layer

**Por qué:** El Excel ya es infraestructura epistemológica, no solo "datos".

### Entregables:
- `app/services/gold_master_governance.py`
  - `validate_gold_master(path)` → lista de validaciones canónicas
  - `get_gm_changelog()` → historial de versiones
  - `backup_gold_master(path, dest)` → copia firmada con SHA-256

- `data/doctrinal/gm_changelog.json` — registro de cambios por versión
- `data/doctrinal/gm_schema.json` — esquema canónico de H73_OUTPUT_API

- Tab "📦 Gold Master" en `m5_control.py`

---

## QUIRA GOV vs QUIRA CIV — Separación Conceptual

> No dos apps todavía. Sí arquitectura lógica separada.

| Capa | QUIRA GOV | QUIRA CIV |
|---|---|---|
| Usuarios | Alcalde · Concejal · Técnico | Ciudadano (sin login) |
| Datos | TGI · SAT · ICPI · D1-D5 | Versión simplificada · ICPI público |
| Acceso | Auth requerida | Pública |
| Badge | `GOV` (cyan) | `CIV` (verde) |
| Estado | Operativo | Arquitectura conceptual |

**Sprint 3:** Solo agregar namespace `CIV` al código (sin segunda app).
**Sprint 4:** Vista pública `/public` en la misma app (sin auth, datos simplificados).

---

## Hardening Sprint 3 (Semana 4)

- Snapshots automáticos: cron/scheduler que ejecuta pipeline semanal
- Backup automático del Gold Master (copia SHA-256 en `data/backups/`)
- Performance: cache de snapshots en session_state (evitar re-lectura Supabase)
- Error monitoring: integrar `utils/logger.py` con alertas por email (opcional)

---

## Checklist Sprint 3

**Semana 1:**
- [ ] `app/services/longitudinal_engine.py`
- [ ] Tab "Evolución Longitudinal" en m2_alertas
- [ ] `tests/test_longitudinal_engine.py`

**Semana 2:**
- [ ] `app/services/snapshot_diff.py`
- [ ] Tab "Comparación de Períodos" en m2_alertas
- [ ] SAT-III reincidencia longitudinal
- [ ] `tests/test_snapshot_diff.py`

**Semana 3:**
- [ ] `app/services/reliability_tracker.py`
- [ ] `app/services/gold_master_governance.py`
- [ ] Tabs en m5_control (Confiabilidad · Gold Master)

**Semana 4:**
- [ ] Scheduler automático de pipeline
- [ ] Backup automático Gold Master
- [ ] Performance + cache
- [ ] Namespace CIV (conceptual)

---

*NORTH.md sigue siendo el documento canónico de doctrina. Este archivo es el plan de ejecución.*
