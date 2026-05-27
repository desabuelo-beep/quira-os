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
- [x] `app/services/longitudinal_engine.py` — 5 funciones canónicas RC-M
- [x] Tab "📈 Evolución Longitudinal" en m2_alertas — tabla RC-M + Plotly + nota doctrinal
- [x] `tests/test_longitudinal_engine.py` — 53 tests en verde (102 totales acumulados)

**Semana 2 (COMPLETA):**
- [x] `app/services/snapshot_diff.py` — 6 clasificaciones canónicas + SAT-III + notas doctrinales
- [x] SAT-III reincidencia longitudinal — `detect_reincidence_from_history()` + `_detectar_sat_iii()`
- [x] `tests/test_snapshot_diff.py` — 109 tests en verde (211 totales acumulados)
- [x] **QUIRA Intelligence Pivot** — frontend integral restructurado:
  - `models/auth.py` — roles Viewer/Analyst/Operator/Admin
  - `utils/session.py` — is_operator(), is_analyst(), is_viewer()
  - `quira_pages/env_gov.py` — 6 tabs GOV (Estado · RC-M · SAT · Comparación · Ejecución · Trazabilidad)
  - `quira_pages/env_civic.py` + `env_impact.py` — placeholders PMV
  - `quira_pages/env_ops.py` — 5 tabs Ops (Pipeline · Snapshots · Reliability · GM · Config)
  - `app.py` — 4-environment selector · branding QUIRA Intelligence · legacy routing

**Semana 3 (COMPLETA — 2026-05-26):**
- [x] `docs/MONTHLY_CYCLE.md` — ciclo mensual formalizado como documento doctrinal
- [x] `app/services/reliability_tracker.py` — 5 funciones: dashboard · history · trend · health · report
- [x] `tests/test_reliability_tracker.py` — 58 tests en verde (269 totales acumulados)
- [x] `TGI_GOLD_MASTER_v6.0_20260525.xlsx` — 34 hojas completas con datos canónicos institucionales:
  - G3.1 D1 Legalidad · G3.2 D2 Planificación · G3.3 D3 GAD · G3.4 D3 Holding
  - G3.5 D3 Consolidado · G3.6 D4 Equidad · G3.7 D5 Capacidad
  - G4.1 ICPI=66.85% · G4.2 TGI=66.85% · G5.2 SAT activas · G6.1_OUTPUT_API actualizado
  - `data/gm_snapshot.json` — sincronizado a v6.0 · ICPI=66.85% · D3=59.85% · D4=66.85%
- [x] `app/services/gold_master_governance.py` — versionado, changelog, backup SHA-256
  - `validar_gold_master()` — 18 hojas requeridas + 14 claves G6.1 + rangos numéricos + versión v6.x
  - `obtener_changelog_gm()` — historial de versiones desde `gm_changelog.json`
  - `respaldar_gold_master()` — copia firmada SHA-256 + archivo `.sha256.json` de integridad
  - `obtener_estado_gm()` — diagnóstico completo: disponibilidad · métricas · errores · changelog
  - `data/doctrinal/gm_changelog.json` — registro v6.0 (ACTIVO) + v5.5 (CONGELADO)
- [x] `tests/test_gold_master_governance.py` — 58 tests en verde (327 totales acumulados)

**Semana 4 (COMPLETA — 2026-05-26):**
- [x] `scripts/ejecutar_ciclo_mensual.py` — orquestador del ciclo mensual con 5 pasos: validar GM · respaldar SHA-256 · pipeline · verificar snapshot · reporte JSON
- [x] `docs/DEPLOY_STREAMLIT_CLOUD.md` — guía completa GitHub→Streamlit Cloud: secrets · dominio · flujo CI/CD · checklist
- [x] `.gitignore` actualizado — `TGI_GOLD_MASTER*.xlsx` + `data/backups/` excluidos del repo
- [x] `.streamlit/secrets.toml.template` actualizado — sin referencias a Sentinel, estructura de secrets correcta para Cloud
- [x] `docs/ARQUITECTURA_CANONICA.md` — contrato arquitectónico permanente de 6 capas (480 líneas)
- [x] Deprecación Sentinel (fase 1) — imports marcados con `# noqa: QUIRA-DEPR`, `sentinel/__init__.py` formalizado como paquete legado
- [x] `utils/cache_quira.py` — capa de cache centralizada (`@st.cache_data`): snapshot (5 min) · historial RC-M (5 min) · reliability (10 min) · Gold Master JSON (15 min) · estado xlsx (10 min) · invalidación manual
  - `env_gov.py` — `_load()` + `_tab_diff()` ahora usan cache: cero re-lecturas Supabase por cambio de tab
  - `env_ops.py` — reliability + Gold Master tab con cache + botón "Refrescar datos" para Operator
  - `p0_inicio.py` + `p_ejecutivo.py` — snapshot con cache de 5 minutos
- [x] Ciclo mensual dry-run validado — `ejecutar_ciclo_mensual.py --dry-run` pasa 6/6 verificaciones: ICPI=53.56% · TGI=68.82 · municipio=130801 · período=2026-05-26 · persistencia=skipped · Estado: OK
  - Bug corregido: `paso_verificar_snapshot()` — claves correctas para snapshot directo de `pipeline.run()` (`gad.codigo`, `_meta.fecha_corte`, `_pipeline.save_result.status`)
- [x] `scripts/generar_informe_mensual.py` — primer informe longitudinal institucional: 7 secciones (resumen ejecutivo · RC-M · TGI D1-D5 · SAT activas · financiero · trazabilidad · metadatos) · salida JSON + Markdown
  - `data/informes/INFORME_202605_130801.json` + `INFORME_202605_130801.md` — primer documento de memoria institucional QUIRA
  - v6.0 sincronizado: TGI=68.82% (titular) · ICPI=53.56% (lente complementario) · clasificación "Ruptura Sistémica" desde Gold Master
  - Bug corregido: clasificación ICPI prioriza `gm_snapshot.json` sobre snapshot local (pipeline v5.5 guardaba sin tilde)
  - Bug corregido: texto doctrinal en `snapshot_diff.py` "Ruptura Sistémica" + tildes en español canónico
- [x] `data/gm_snapshot.json` — sincronizado a v5.5+TGI (H73_OUTPUT_API): TGI=68.82 · ICPI=53.56% · D3=14.58% · D4=66.85% · nuevas secciones `icpi`, `sat_gm`, `psg`
  - **Sprint Canon:** `sat_gm.riesgo_total` corregido de 0.72 → **0.35** (reconciliación SAT completa) · fuente actualizada a `H75_SAT_ENGINE · H73_OUTPUT_API · v5.5`
- [x] `quira_pages/p0_inicio.py` — TGI como métrica primaria (orden: TGI → SAT → ICPI) · fallback a gm_snapshot.json si snap.tgi.score es None
- [x] Transición semántica español (Fase 1 — shims de reexportación):
  - `app/services/rastreador_confiabilidad.py` → alias de `reliability_tracker.py`
  - `app/services/comparador_snapshots.py` → alias de `snapshot_diff.py`
  - `app/services/gobernanza_gold_master.py` → alias de `gold_master_governance.py`
- [x] Conceptual clarity v6.0: TGI = índice titular canónico (D1-D5, largo plazo) · ICPI = lente complementario (ejecución, más exigente) · ambos coexisten por diseño
- [ ] Namespace CIV (conceptual)

---

---

## DECISIÓN ARQUITECTÓNICA — Gold Master (2026-05-26)

> **v5.5 ES y continúa siendo el Gold Master canónico activo.**

| Archivo | Tamaño | Hojas | Estado |
|---|---|---|---|
| `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.xlsx` | 931 KB | **123 hojas llenas** | ✅ **ACTIVO — L1 canónico** |
| `TGI_GOLD_MASTER_v6.0_20260525.xlsx` | 38 KB | 34 hojas (17 vacías) | ⚠️ Template de referencia — sin datos de soporte |

**Acciones ejecutadas:**
- H73_OUTPUT_API en v5.5 actualizado con claves TGI Framework:
  - `TGI_SCORE=68.82` · `TGI_D1=83.5` · `TGI_D2=69.93` · `TGI_D3=14.58` · `TGI_D4=66.85` · `TGI_D5=100.0`
  - `SAT_CLASIF_RIESGO=ALTO` · `SAT_ACTIVAS_COUNT=3` · `SAT_RIESGO_TOTAL=0.35` (reconciliado — ver Sprint Canon)
  - `ICPI_CLASIFICACION=Ruptura Sistémica` (tilde añadida)
  - `IED_GLOBAL=0.3114` · `IED_DIRECCIONES_N=11` · `BRECHA_RURAL_USD=1791935`
- `app/connectors/gold_master.py` — v5.5 como primario, v6.0 como fallback
- `data/gm_snapshot.json` — _meta corregido a v5.5+TGI
- Backup: `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518_BACKUP_20260526.xlsx`

**Cadena canónica restaurada:**
```
v5.5 H73_OUTPUT_API → gold_master.py → pipeline → Supabase → Streamlit
```

---

## SPRINT CANON — Consolidación Epistemológica (2026-05-26)

> **Iniciado** tras análisis técnico del colega: QUIRA tiene arquitectura de memoria longitudinal pero no memoria real aún.
> **Prioridad absoluta:** estabilidad epistemológica antes de cualquier feature nueva.

**Freeze en vigor:** Frontend/AI/Civic/Sprint 4 congelados hasta que la cadena canónica sea auditablemente consistente.

### Prioridad 1 — Reconciliación SAT ✅ COMPLETADA

**Problema:** Gold Master v6.0 (G6.1) tenía `SAT_RIESGO_TOTAL=0.72` — estimación manual inconsistente con H75 thresholds documentados (0.72≥0.50=CRÍTICO pero G6.1 decía ALTO). Pipeline calculaba 0.35 por metodología correcta.

**Causa raíz confirmada:**
- G5.2_SAT_ACTIVAS (v6.0) es hoja vacía — la estimación manual no tiene respaldo de fórmulas
- H75_SAT_ENGINE pesos IDÉNTICOS al pipeline (SAT-III=0.20, SAT-IV=0.10, SAT-V=0.05)
- SAT-III(0.20) + SAT-IV(0.10) + SAT-V(0.05) = **0.35/ALTO** por definición canónica

**Acciones ejecutadas:**
- `SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.xlsx` H73_OUTPUT_API: `SAT_RIESGO_TOTAL=0.35` + nota en col C
- `data/gm_snapshot.json`: `sat_gm.riesgo_total=0.35` · fuente=`H75_SAT_ENGINE · H73_OUTPUT_API · v5.5` · detalle de las 3 SATs activas
- `scripts/generar_informe_mensual.py`: referencias v6.0 → v5.5 en encabezado y metadatos
- **Verificación:** dry-run pasa 6/6 · pipeline muestra `SAT RIESGO: 0.350 → ALTO` · 327 tests verdes

**Meta canónica cumplida:**
> Gold Master SAT = Pipeline SAT = Snapshot SAT = Informe SAT = Streamlit SAT.
> Verdad institucional única establecida. ✅

### Prioridad 2 — G3.x / H85 Checklist (PENDIENTE)
- CHK-08: eSIGEF 2026 cédula presupuestaria completa (H07 zona cruda)
- CHK-12: PP 2026 actas participativas + CPCCS informe rendición
- Bloqueado por datos reales — no se puede simular

### Prioridad 3 — Snapshot Real #1 (PENDIENTE)
- Solo después de que G3.x data esté completa
- Supabase persistence habilitado (quitar dry-run flag)

---

*NORTH.md sigue siendo el documento canónico de doctrina. Este archivo es el plan de ejecución.*
