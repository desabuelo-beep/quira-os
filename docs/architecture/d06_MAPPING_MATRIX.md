# d06_MAPPING_MATRIX.md — Pixel ↔ Snapshot ↔ Celda

**Sprint D.1 · Paso 2 · 2026-06-15 · matriz de correspondencia canónica de d06 (Integridad/Salud Institucional)**

> 🛡️ REGLA: prohibido `demo_data` y claves inventadas. Si un widget no tiene clave REAL aquí, se marca **GAP** (no se renderiza con dato falso). **Cada pixel se debe a su celda.**
> Claves VERIFICADAS por `scripts/dev/gm_contract_check.py` (ejecución real sobre el vivo corregido) — NO las del borrador del académico.

## El contrato real del snapshot (lo que QUIRA puede leer HOY)
`cargar_snapshot()` (salida del pipeline) expone:
- `icpi.{global_pct, global, clasificacion, historico.{2023,2024,2025}, acumulado_q1}`
- `tgi.{score, d1, d2, d3, d4, d5}`
- `sat.{alertas_activas, clasif_riesgo, riesgo_ponderado}`  ← (del `eval_sat` del pipeline · DISTINTO de `sat_engine` del GM)
- `_meta.fecha_corte`
- vía `_raw_h73` (las 64 claves del GM): `ISP_SALUD_PRESUP · PSG_EJECUCION · IED_GLOBAL · IGP_2026_ACTUAL · IOC_OPACIDAD · IET_PERCAPITA_PEOR · IFE_GLOBAL · ITAM_2025_REF · ICODS_GLOBAL · IEF_CAPTACION · TRUST_SCORE · NBI_* · FONDOS_* · BRECHA_RURAL_USD · IRS_GLOBAL · COMPOSITE_NEED_LEADER …`

---

## Tab 1 · `p_ejecutivo` (Vista Ejecutiva) — panel Q1 YA CABLEADO ✅
| Widget UI | Clave real | Fuente | Estado |
|---|---|---|---|
| Banner TGI (titular) | `tgi.score` → 66.79 | snapshot | ✅ live |
| Riesgo SAT | `sat.clasif_riesgo` + `len(sat.alertas_activas)` | snapshot | ✅ live |
| ICPI Progreso | `icpi.global_pct` → 27.46 · `icpi.clasificacion` | snapshot | ✅ live |
| Señales SAT activas | `sat.alertas_activas` (SAT-III/IV/V) | snapshot | ✅ live |
| Semáforos × entidad (GAD/BOM/EMAI/PAT) | `holding_kpis[ent]` (Ti) | `report_engine` (DB) | 🟡 DB (no snapshot) |
| SLA · críticas · resumen Q&A | `build_report_data` | `report_engine` (DB) | 🟡 DB (alertas) |
> Cosmético: footer "Gold Master v5.5" (`p_ejecutivo.py:193`) → actualizar a v6.0.

## Tab 2 · `p6_pulso` (Pulso) — `demo_data`, A CABLEAR
| Widget UI | Lee hoy (demo) | Clave real destino | Estado |
|---|---|---|---|
| Header score (ICGI-T 53.56) | `icgit.score` | **DECISIÓN**: `icpi.global_pct` (27.46) o `tgi.score` (66.79) | 🔴 mapear + decidir |
| Card PSG (12.83%) | `indices.PSG.valor` | `_raw_h73.PSG_EJECUCION` → **2.83%** | 🔴 demo→real |
| IET (44.80) | `indices.IET.valor` | `_raw_h73.IET_PERCAPITA_PEOR` → 0.448 | 🔴 demo→real |
| **4 Congruencias** (pol/ope/ter/eco) | `congruencias.*.score` | ⚠️ **NO existen en snapshot** | 🟥 **GAP → QUIRA IA (C3)** |
| Holding radar (score × ente) | `holding.entidades[].score` | `report_engine` (DB) o H73 parcial | 🟡 reconciliar fuente |
| Riesgo/Oportunidad Q2 | **TODO hardcoded** (ISP 14.58 · Ti 70% · IFE 72.73 · ICODS 87.5) | `_raw_h73.{ISP_SALUD_PRESUP, IFE_GLOBAL, ICODS_GLOBAL}` o eliminar | 🔴 hardcode→real |
| "$40/hab · Isabel Muentes" | hardcoded | `_raw_h73.{IRS_GLOBAL, COMPOSITE_NEED_LEADER}` | 🟡 verificar |

## Tab 3 · `p7_brecha` (Causas · 6 vectores) — HARDCODED, A CABLEAR
Los 6 vectores causales SÍ tienen clave real (en `_raw_h73`):
| Vector | Clave real | Valor real (vivo) |
|---|---|---|
| ISP (Salud Presup.) | `_raw_h73.ISP_SALUD_PRESUP` | 3.22% |
| IED (Eficiencia Dir.) | `_raw_h73.IED_GLOBAL` | 24.94% |
| IGP (Gobernanza Partic.) | `_raw_h73.IGP_2026_ACTUAL` | 48.33% |
| IOC (Opacidad) | `_raw_h73.IOC_OPACIDAD` | 17.71% |
| IET (Equidad Territ.) | `_raw_h73.IET_PERCAPITA_PEOR` | 44.80% |
| PSG (Presup. Género) | `_raw_h73.PSG_EJECUCION` | 2.83% |
> (Inventario línea-a-línea de widgets se confirma al cablear · Paso 3.)

---

## 🔍 Diagnóstico HONESTO de huecos (corrige al académico: NO son "ninguno")
1. 🟥 **Las 4 congruencias** (corazón del Pulso) NO están en el snapshot — son juicios de **QUIRA IA (C3)**, decisión sellada (`MATRIZ_RECONCILIACION_TOTAL §4`). Hasta que C3 las emita, esos 4 widgets no tienen clave real. **Hueco mayor.**
2. 🟥 **FactorTemporal · Ti_raw GAD · adscritas-status** (el Bloque 3 inventado por el académico) NO están en H73 — son celdas INTERNAS del Excel (`H07_S5!B23`, `H07b!B19/D19`). Para mostrarlas en d06 → exportarlas a H73 primero (**Carril B**), o no mostrarlas.
3. 🟡 **Texto hardcoded** (riesgo/oportunidad, $40/hab, "ICGI-T 53.56%") → reemplazar por `_raw_h73.*` o eliminar.
4. 🟡 **Holding por entidad** viene de `report_engine` (DB de alertas), no del snapshot GM — coexisten dos fuentes; decidir cuál es canónica para d06.
5. 🔵 **Decisión de diseño** (no metodológica): ¿el headline de d06 es `icpi.global_pct` (27.46 · el cimiento) o `tgi.score` (66.79 · el índice titular)? `p_ejecutivo` ya usa TGI titular + ICPI complementario.

## Plan mecánico (Paso 3 · Carril A · cuando Javo dé luz verde)
1. **Persistir `gm_snapshot.json`** (escritura producción consciente — Supabase+JSON).
2. `p6_pulso`: `load_all()` → `cargar_snapshot()` + `_raw_h73` para widgets con clave real · 4 congruencias → placeholder "C3 pendiente" · eliminar hardcode.
3. `p7_brecha`: 6 vectores hardcoded → `_raw_h73.*`.
4. **Auditoría visual:** QUIRA en pantalla vs Excel — coincidencia exacta (27.46% · semáforo · 6 vectores).

---
*d06 Mapping Matrix · Sprint D.1 Paso 2 · Dylus Lab © 2026 · cada pixel con su celda, cada celda con su tesis.*
