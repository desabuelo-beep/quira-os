# METODOLOGÍA DEL GOLD MASTER — registro canónico

**2026-06-15 · construido para que NUNCA MÁS se pierda en tesis archivadas (mandato Javo)**

> **Por qué existe:** la metodología del motor vivía en las tesis archivadas, NO en los docs canónicos.
> Eso causó la confusión de hoy (ICPI=promedio · 17.45%=Ruptura · congruencias inexistentes). Aquí queda ESTAMPADA.

## 🔒 PRINCIPIO INVIOLABLE — la fórmula canónica es INMUTABLE
> El Gold Master ES el Estado (Regla de Oro 1). La **fórmula canónica del ICPI (`H12!B33`) NUNCA se modifica.**
> El propio motor lo declara en la celda: *"★ FUENTE ÚNICA · NUNCA recalcular · NO modificar la lógica ★"*.

**Protocolo de corrección (cuando la realidad obliga a ajustar — "trabajar sobre la realidad"):**
- ✅ **Permitido:** corregir **INPUTS** con evidencia (FactorTemporal, metas Ti=0) · refinar el **SEMÁFORO/clasificación** · ajustar la **presentación/lectura** (proporcional).
- ❌ **Prohibido:** tocar la **fórmula central** (`B33`) · recalcular el ICPI en Python (motor paralelo · Regla 4) · editar el canon vivo con `openpyxl` (corrompe la malla de 123 hojas).
- 🛡️ **Cómo:** SIEMPRE sobre **copia de trabajo** (freezer = rollback) · cambios **basados en EVIDENCIA, no intuición** · **verificados con dumps** (`scripts/dev/gm_*`) antes de promover · Javo dirige metodología, Claude ejecuta mecánico.

## La fórmula canónica del ICPI (`H12!B33`)
```
ICPI = [ Σ(Pi · Ri · Vi · Ei · Ti · Ci) / Σ(Pi · Ri) ] × 100
```
- **Pi** ponderador (H14) · **Ri** relevancia (H14) · **Vi** variable/avance (H13) · **Ei** exigibilidad (1.0 autónomo / 0.9 compartido / 0.75 difuso) · **Ti** ejecución (H07b) · **Ci** calibración (H01 §M)
- `B33 = B31/B32` (Numerador/Denominador). **Todas las hojas referencian SOLO B33.** Cada factor es MULTIPLICATIVO → un Ti=0 colapsa esa meta.

## Ti — la ejecución, y su lectura proporcional (la pieza clave de hoy)
- **Ti_raw** = devengado/codificado (eSIGEF). Naturalmente bajo a mitad de año (acumulado parcial).
- **Ti_norm** (`H07b!B20`) = `MIN(1, Ti_raw / FactorTemporal(mes/12))` — *"avance proporcional al corte mensual"*. **El ICPI YA usa Ti_norm.**
- ⚠️ **Gap:** el FactorTemporal es **LINEAL** (`mes/12`); el gasto público es **back-loaded** (Q3-Q4) → penaliza meses tempranos.

## AVEP — escala de clasificación canónica (`config.py` · `H01_PARÁMETROS`)
| Nivel | Rango | Etiqueta |
|---|---|---|
| 5 | ≥ 0.90 | 🔵 Excelencia en Gobernanza |
| 4 | 0.70 – 0.89 | 🟢 Gestión por Mandato |
| 3 | 0.40 – 0.69 | 🟡 Transición Crítica |
| 2 | 0.20 – 0.39 | 🟠 Gestión por Ocurrencia |
| 1 | < 0.20 | 🔴 Ruptura Sistémica |
> Histórico full-year: 2023=57.36 · 2024=67.11 · 2025=69.93 → todos "Transición Crítica". **Los umbrales se calibraron para valor ANUAL** → aplicarlos a un corte parcial (17.45%) produce "Ruptura" falsa.

## Gaps metodológicos abiertos (a resolver CON Javo · sobre copia · con evidencia)
1. **FactorTemporal lineal → curva de ejecución HISTÓRICA real de Montecristi** (evidencia, no hipótesis nacional · corrección del colega al académico).
2. **Metas Ti=0 (`GAD_SIN_ESIGEF`)** → cada ente adscrito (Bomberos/Patronato/EMAI) con su **mini-Ti homologado** (audited financials). **NO** factor neutro 1.0 (= regalar puntos · rompe integridad · colega).
3. **Clasificación vs corte parcial** → ¿el semáforo debe ser consciente del mes? (menos invasivo que tocar la fórmula · colega).
4. **`TBL_CALIBRACION_Ci` pendiente** (H01 §M · `B40` lo marca).

## Datos disponibles para la curva histórica (auditado 2026-06-15)
- ✅ ICPI anual 2023-2025 (`H12c`) · ✅ cédulas mensuales 2026 (`H_HOLDING_CEDULAS_2026`) · ✅ metas mensuales (`H25_MMP_MENSUAL`) · `H36b` arrastre 2023-25.
- ❌ **NO hay 2021-2022 ni serie trimestral pre-2026** → la curva histórica se construye con lo que EXISTE (2023-25 anual + 2026 mensual), declarando el límite. Evidencia parcial > hipótesis nacional.

## IGAP — Índice de Grupos de Atención Prioritaria (índice NUEVO · cirugía sobre copia · 2026-06-23, validado con Javo)

> **Mide** la atención del GAD a los **grupos de atención prioritaria de su competencia** (subconjunto del Art.35 CRE habilitado por ley/ordenanza — **NO** es "índice de política social", que abarcaría Deportes/Cultura/Turismo y otras competencias de dirección). Madre del cajón **d12** (Inclusión / Grupos Prioritarios). **Nombre: IGAP, no IPS.**

**Grupos medidos (competencia GAD · subconjunto Art.35 CRE):** niñez y adolescencia · adultos mayores · personas con discapacidad · mujeres embarazadas · personas en extrema pobreza · enfermedades catastróficas. *(Mujeres en general → ODS/género vía PSG, NO GAP; el GAP toma a la embarazada.)*

**Anti-duplicación (Regla #6 — DERIVA, no redefine):**
| Componente | Ya existe → deriva de |
|---|---|
| Subíndice mujeres/género | `H16c_PSG` (dual Fidelidad 0.44 / Ejecución 0.028) |
| Base bienestar / NBI | `H12b_IBSC` + `H04b_DIAGNÓSTICO_SOCIAL` |
| Marco COOTAD corriente/inversión | `H19_ISP` (piso 65% Art.192 + SAT-IV) |
| Naturaleza de la unidad | `H02b_ORGÁNICO_CLASIFICADOR` |

**Equidad por naturaleza de la unidad (corrección Javo — principio GENERAL, no parche al Patronato):**
El IGAP lee `H02b.EVIDENCIA_PREDOMINANTE` para **NO castigar a las unidades que producen intangibles** (gasto corriente: sueldos/servicios) en vez de PAC/inversión. Unidades GAP intangibles: Patronato (U-19 · `INDICADOR/INFORME SHA-256`), Turismo-Cultura-Patrimonio (U-13), Cultura/Deporte, Desarrollo Económico, Participación (U-06). Para ellas la evidencia válida es **atención (indicador)**, no SERCOP/eSIGEF → el IGAP mide **RESULTADO (atenciones)**, no compras.

**Mapeo grupo→unidad (confirmado Javo 2026-06-23):** el **Patronato (U-19)** es la unidad GAP-dedicada — atiende a TODOS los grupos prioritarios (niñez/adolescencia, adultos mayores, discapacidad, embarazadas, extrema pobreza, enf. catastróficas). **Cultura/Deportes/Turismo (U-13)** son universales: sirven a toda la población —GAP incluido— → contribuyen al IGAP pero NO son GAP-exclusivas. Meta PDOT ancla: `AH-C-X-01` "Protección derechos sociales: atenciones a grupos" (Patronato + MIES convenio).

**Fórmula (estructura):** `SIGAP_g = f(cobertura = atenciones/población objetivo · evidencia según EVIDENCIA_PREDOMINANTE de la unidad responsable)` · `IGAP = Σ(peso_g · SIGAP_g)`, peso por vulnerabilidad/población.

**Insumos:** población objetivo/grupo ✅ PDOT/INEC · clasificador de unidades ✅ `H02b` (Res.040-2025) · gasto/competencia ✅ eSIGEF/orgánico · **atenciones mensualizadas/grupo ⏳ LOTAIP literal D (bloqueado por caída CNT — Javo descarga y avisa).**

**Construcción:** índice derivado nuevo (como IPE/IBSC) · **NO toca `H12!B33`** · sobre COPIA de trabajo · con evidencia · verificado con dumps · **openpyxl PROHIBIDO sobre el canon vivo** (corrompe la malla de 123 hojas). Cirugía documentada como la D2A.

## Cirugía H07b-2025 — corte provisional → cierre LOTAIP (2026-07-11 · Javo ejecutó en Excel, Claude verificó con dump)

**Motivo:** el multi-año profundo (Planificación) reveló que `H07b` 2025 usaba un corte **PROVISIONAL**
("Presupuesto GAD" · Codif $10.2M · Ti 59.85%), no el cierre. La cédula LOTAIP de diciembre (Numeral 6,
grupos 7+8 — **misma metodología que reprodujo 2026 con Δ=$0**) da el cierre real. Coherente con ADR-029
§Precisión (la verdad vive en la fuente; el modelo la integra) y el patrón fuente→canon.

**Cambio (input con evidencia · `B33` intacta · openpyxl NO usado — edición en Excel nativo):**
| Celda | Antes | Después |
|---|---|---|
| `H07b!B9` Codificado 7+8 | 10 202 422,21 | **17 524 308,73** |
| `H07b!C9` Devengado 7+8 | 6 106 506,58 | **12 746 168,09** |
| `H07b!D9` Ti *(fórmula, no tocada)* | 0,5985 | **0,7273** (recalc automático) |
| `H07b!E9/F9` trazabilidad | "Presupuesto GAD (provisional)" | "cierre LOTAIP diciembre (7+8)" |

**Evidencia:** `Holding_Municipal_Montecristi\Cedulas Presupuestarias 2023-2026\Presupuestos 2025\GAD Montecristi\2025-Diciembre-…Conjunto de datos.xlsx`.
**Blast radius (verificado en las 123 hojas):** `B9,C9 → D9 → H85_ALERTS_LOG` únicamente. **`H12!B33` (ICPI vivo = 0,2746)
y `H12c` 2025 (69,93) INTACTOS.** Trayectoria Ti corregida: **68 → 80 → 73** (antes 68→80→60, artefacto del corte).
Pendiente menor: `H85!D25` baseline 0,5985→0,7273 (log interno, no afecta motor).

---
*Metodología Gold Master · Dylus Lab © 2026 · la fórmula canónica es INMUTABLE · correcciones solo en inputs/semáforo/presentación, sobre copia, con evidencia verificada.*
