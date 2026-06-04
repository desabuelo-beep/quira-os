---
name: "RC-M — Tabla de Memoria Longitudinal"
description: "Tabla canónica RC-M: Período | ICPI | D3_Ti | SAT-IV | Riesgo. Convierte observaciones puntuales en trayectoria institucional. Base del Longitudinal Engine de QUIRA."
tipo: meta-longitudinal
version: "v5.5"
desarrollador: "Dylus Lab / QUIRA Gov"
gold_master: "Gold Master TGI v5.5"
fecha: "2026-05-25"
tags: [rcm, longitudinal, trayectoria, memoria, icpi, d3, sat, riesgo, core]
---

# RC-M — Tabla de Memoria Longitudinal

> **RC-M convierte observaciones puntuales en trayectoria institucional.**
> Un municipio no se evalúa por lo que hizo hoy — se evalúa por su trayectoria.
> La reincidencia es el peor diagnóstico. La recuperación es el mejor pronóstico.

Vincula → [[05_SAT_SISTEMA]] SAT-III · [[02_TGI_DIMENSIONES]] D3 · [[01_TGI_FRAMEWORK]]

---

## Estructura RC-M Canónica

```
Período | ICPI (%)  | D3 Ti (%) | SAT-IV   | Riesgo
--------|-----------|-----------|----------|--------
Mayo    | 53.56%    | 14.58%    | ACTIVA   | ALTO
Junio   | 58.10%    | 32.00%    | ACTIVA   | MEDIO
Julio   | 64.20%    | 55.00%    | mitigada | MEDIO
```

**Hoja Gold Master:** G4.5_RC_M (antes H12b / H63 en v5.5)
**Implementación Python:** `app/services/longitudinal_engine.py`

---

## Definición de Columnas

| Columna | Fuente | Threshold | Colores UI |
|---------|--------|-----------|------------|
| Período | fecha_corte del snapshot | — | — |
| ICPI (%) | icpi.score × 100 | < 50% 🔴 · < 65% 🟡 · ≥ 65% 🟢 | Semántico |
| D3 Ti (%) | tgi.dimensiones.d3 × 100 | < 40% 🔴 · < 60% 🟡 · ≥ 60% 🟢 | Semántico |
| SAT-IV | sat.activas lista | ACTIVA / mitigada / SIN DATOS | Por estado |
| Riesgo | Calculado: ICPI + D3 + SAT | ALTO / MEDIO / BAJO / CRÍTICO | Semántico |

---

## La Regla de Reincidencia — SAT-III

```
IF D3_Ti < 60% por 3 períodos consecutivos
    THEN → SAT-III REINCIDENTE (D3-Ejecución · COPFP Art. 113)

IF ICPI < 65% sostenido
    THEN → Riesgo pérdida elegibilidad fondos externos (Q5-Proyección)
```

**Base legal:** COPFP Art. 113 — evaluación de la ejecución presupuestaria
**Base doctrinal:** La reincidencia distingue ineficiencia puntual de patrón estructural crónico

---

## Clasificaciones de Tendencia

| Tendencia | Condición | Badge |
|-----------|-----------|-------|
| MEJORA | ICPI período N > ICPI período N-1 por ≥ 1pp | 📈 |
| DETERIORO | ICPI período N < ICPI período N-1 por ≥ 1pp | 📉 |
| ESTABLE | Diferencia < 1pp | ➡️ |
| RUPTURA | Caída > 10pp entre períodos | 📉🚨 |
| RECUPERACIÓN | ICPI > 65% después de haber estado < 60% | 📈✅ |
| REINCIDENCIA | Ti < 60% × 3 períodos → SAT-III | 🔄🚨 |

---

## Flujo RC-M — Del Snapshot a la Trayectoria

```
Pipeline QUIRA ejecuta snapshot semanal/mensual
    ↓
Snapshot guardado en Supabase (municipality_snapshots)
    ↓
longitudinal_engine.py carga historial de snapshots
    ↓
get_rc_m_data() construye tabla RC-M período por período
    ↓
detect_trend() calcula MEJORA / DETERIORO / ESTABLE
    ↓
UI: m2_alertas.py → tab "📈 Evolución Longitudinal"
    ↓
Si Ti < 60% × 3 períodos → SAT-III activada automáticamente
```

---

## Estado RC-M Actual — GADM Montecristi

| Sprint | Períodos registrados | Estado |
|--------|---------------------|--------|
| Sprint 2 | 1 snapshot | Punto único — sin trayectoria |
| Sprint 3 | Creciendo | Tabla RC-M activa en UI |
| Sprint 4+ | 4+ snapshots | Reincidencia detectable |

**Activación SAT-III automática:** requiere mínimo 3 snapshots con Ti < 60%

---

## Snapshot Diff Engine — Sprint 3 P2

El RC-M se complementa con el Snapshot Diff Engine (Sprint 3 P2):

```
compare_snapshots(snap_anterior, snap_actual)
    → DiffResult:
        - campos_cambiados
        - direccion (MEJORA / DETERIORO)
        - magnitud (pp de cambio)
        - alertas_nuevas
        - alertas_mitigadas
        - clasificacion: RUPTURA / RECUPERACION / REINCIDENCIA / MEJORA / ESTABLE
```

Archivo: `app/services/snapshot_diff.py` (Sprint 3 P2 — pendiente)

---

## Conexión con Q5 — Proyección Contextual Limitada

La RC-M es la base de la proyección contextual (QUIRA Fase 5):

```
Si ICPI < 65% sostenido × N períodos
    → Proyección: riesgo pérdida elegibilidad fondos CAF/BID/GIZ
    → Proyección: riesgo intervención Contraloría por subejecución crónica
    → Proyección: alerta Plan Bicentenario en riesgo de incumplimiento
```

*La proyección en QUIRA es siempre acotada, explicable y causal — nunca especulativa.*

---

**Fuente canónica:** Gold Master TGI v5.5 · G4.5_RC_M
**Implementación:** `app/services/longitudinal_engine.py` · 53 tests (Sprint 3 P1 ✅)
**Doctrina:** NORTH.md → "memoria longitudinal territorial"
**Fecha:** 2026-05-25
