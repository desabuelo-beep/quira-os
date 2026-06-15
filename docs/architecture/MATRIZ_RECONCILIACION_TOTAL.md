# MATRIZ DE RECONCILIACIÓN TOTAL — una sola verdad

**Sprint D.2 · 2026-06-14 · elimina toda diferencia entre Motor ↔ Pantallas ↔ Ontología ↔ Congruencias**

> El activo de QUIRA es el **MOTOR**, no las pantallas — PERO leído CORRECTAMENTE.
> ⚠️ **CORRECCIÓN Javo (2026-06-15):** el `ICPI_GLOBAL` 17.45% es el **acumulado anual leído en Q1 (mes ~4-5)** —
> naturalmente bajo (apenas 3-4 meses de gestión). Clasificarlo "Ruptura Sistémica" (umbral ANUAL sobre valor PARCIAL)
> es un MISREAD. **Anualizado ≈ 17.45%×3 ≈ 52% ≈ el 53.56% del demo → NO se contradicen: es el mismo estado en dos
> lentes temporales** (crudo Q1 vs proyección anual). La reconciliación NO es "cablear al 17.45% crudo" — es definir la
> **lectura PROPORCIONAL al tiempo de gestión** que refleje la gestión REAL al corte (decisión de metodología · Javo/motor).
> Verificado contra `GM_H73_DUMP.md` (65 claves reales con celda fuente). Cifras del académico filtradas (IET≠TGI; ISP←H19, no H07_S5).
> La verdad incómoda (17.45% "Ruptura Sistémica") = el activo comercial: QUIRA **no maquilla, expone con precisión científica.**

## Inventario 1 · PANTALLAS → MOTOR (deuda técnica de cableado)

| Pantalla cantera | Lee hoy de | Estado | Acción Sprint D.2 |
|---|---|---|---|
| `p_ejecutivo` | snapshot pipeline (cache_quira/sentinel) | 🟡 semi-live | verificar que el snapshot = H73 actual |
| `p6_pulso` | `data.loader` → demo_data | 🔴 DESYNC (ICPI 53.56 · ISP 14.58 · PSG 12.83) | cablear a H73 |
| `p7_brecha` | `data.loader` + **6 vectores HARDCODED** | 🔴 DESYNC | cablear a H73 (ISP/IED/IGP/IOC/IET/PSG vivos) |
| `p10_territorio` | QTMP (Neo4j) | 🟢 live | ok (verificar corte) |
| `p10_inversion` | `data.loader` → demo_data + `EJES_INVERSION` hardcoded | 🔴 DESYNC | cablear a H73 / H07b |

**Resultado: mapa de deuda técnica.** Las pantallas `data.loader/demo_data` son las desincronizadas. → reemplazar por `gold_master.py`.

## Inventario 2 · ONTOLOGÍA → MOTOR (¿cada ADN tiene respaldo en las 65 claves?)

| ADN | Clave(s) viva(s) en H73 | Valor real | Respaldo |
|---|---|---|---|
| d01 Planificación | `MMP_AVANCE_PCT` (pendiente) · metas vía ICODS | — | 🟡 parcial |
| d02 Presupuesto | `ISP_SALUD_PRESUP` · `IED_GLOBAL` · `GAD_DEVENGADO_Q1` · `FONDOS_*` | ISP 3.22% · dev $5.14M | ✅ |
| d03 Gob. del Mandato | `IFE_GLOBAL` | 72.73% | ✅ |
| d04 Alertas | `SAT_ACTIVAS_COUNT` · `SAT_RIESGO_TOTAL` · `SAT_CLASIFICACION` | 2 · MEDIO | ✅ |
| d05 Holding | `PRESUPUESTO_TOTAL_4E` | $54.2M | 🟡 parcial |
| **d06 Salud** | `ICPI_GLOBAL` (cimiento) | **17.45% Ruptura** | ✅ |
| d07 Transparencia | `ITAM_2025_REF` · `IOC_OPACIDAD` | 82.29% / 17.71% | ✅ |
| d08 Participación | `IGP_2026_ACTUAL` | 48.33% | ✅ |
| d09 RDC | *(sin clave directa en H73 — `TRUST_SCORE`?)* | — | 🔴 a verificar |
| d10 Cobertura | `IET_*` · `NBI_RURAL/URBANA` · `PARROQUIAS_TOTAL` | IET 44.8% · NBI 67.9/23 | ✅ |
| d11 Económico | `IEF_CAPTACION` (parcial) | 6.19% | 🟡 corpus |
| d12 Género | `PSG_EJECUCION` | 2.83% | ✅ |
| **d13 Ambiente** | `ICODS_GLOBAL` | **87.5%** | ✅ **validación dorada** (el motor SÍ entrega el eje ambiental) |

**Cobertura ontológica:** 9/13 ✅ respaldo total · 3 🟡 parcial (d01·d05·d11) · 1 🔴 a verificar (d09).

## Inventario 3 · H73 → HOJAS DEL EXCEL (la genealogía · ya en el dump)

> Cada salida trae su celda fuente. Si el ICPI cae, sabemos QUÉ celda lo arrastró al sótano:
- `ICPI_GLOBAL` ← `H12_MOTOR_ICPI_CANÓNICO!B33` (= B31/B32 num/den) · histórico ← `H07b`·`H12c`·`H12b`
- `ISP` ← `H19_ICS_ISP!B12` · `IED` ← `H17_IED!B6` · `IGP` ← `H20b_IGP!B9` · `IOC` ← `H18_ITAM!B20` · `IET` ← `H42_IET` · `PSG` ← `H16c_PSG!B11`
- `IFE` ← `H16_IFE!B6` · `TGI` (D1-D5) ← `H98_TGI_FRAMEWORK!B25` · `ICODS` ← `H20_ICODS!B6` (=AVG `H11!F13:F37`)
- `SAT` ← `H75_SAT_ENGINE` · presupuesto ← `H90_PRESUPUESTO_CONSOLIDADO` · NBI ← `SCHEMA_NBI` · fondos ← `H69_ELEGIBILIDAD`
- ⚠️ `MMP_AVANCE_PCT` = la ÚNICA salida marcada `VALIDACION_OK=NO` (pendiente · D2)

## Inventario 4 · CONGRUENCIAS → DATOS (el puente teoría↔algoritmo · PENDIENTE de formalizar)

> Las 4 congruencias **NO están en H73** (no son salidas simples — son funciones RELACIONALES que cruzan dominios).
> Marco Modelo B (los insumos que LEERÍAN, no su cálculo · aún no formalizado en el Excel):

| Congruencia | Insumos (Modelo B) | Estado |
|---|---|---|
| Política (Promesa→Plan) | `IFE` (H16) ↔ metas `H11b` | marco · sin fórmula |
| Operativa (Plan→Ejecución) | salud `ICPI` (H12) ↔ devengado (`GAD_DEVENGADO`/`H07_S5`) | marco · sin fórmula |
| Territorial (Ejec.→Territorio) | `IET` (H42) ↔ `NBI`/cobertura (INEC) | marco · sin fórmula |
| Ecosistémica (Terr.→Sostenib.) | `PSG` (H16c) + `ICODS` (H20) + biofísico | marco · sin fórmula |

✅ **DECIDIDO (Javo · 2026-06-15):** las congruencias viven en **QUIRA IA (C3)** — son JUICIOS, no aritmética. NO se calculan en el Excel · las razona la IA sobre las claves del motor.

---

## Veredicto de la reconciliación
- **El motor entrega 65 claves reales, trazables hasta la celda.** Las pantallas `demo_data` están desincronizadas (≥5 casos: ICPI·ISP·PSG·…).
- **Acción Sprint D.2 (código · fresco + harness):** cablear pantallas `demo_data` → H73 (`gold_master.py`) · normalizar unidades (decimal↔%) · verificación VISUAL en deploy.
- **Definir la lectura PROPORCIONAL del ICPI al corte** (no presentar el crudo Q1 como si fuera anual → evita la falsa "Ruptura"). Metodología: Javo/motor.
- **Recién entonces** el MVP de d06 se construye sobre dato VIVO leído correctamente. Congruencias → **QUIRA IA (C3)** decidido (Javo · son juicios, no aritmética).
- **El activo comercial** NO es un número crudo — es la **trazabilidad + la lectura correcta**: QUIRA no maquilla (53.56% sin base) NI da falsas alarmas (17.45% "Ruptura" mal leído). Expone la gestión REAL al corte, proporcional y trazable hasta la celda.

*Matriz de Reconciliación Total · Sprint D.2 · Dylus Lab © 2026 · una sola verdad · regenerar contrato: `python scripts/dev/gm_h73_dump.py`*
