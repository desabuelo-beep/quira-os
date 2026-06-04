# Gold Master Schema — SIAP-ICPI v5.5 · Motor QUIRA

> **Uso interno Dylus Lab.** Este documento describe la estructura del Excel canónico.
> Nunca exponer en UI pública. Bloomberg Firewall activo.
> Archivo real: `C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx`
> Acceso vía: `app/connectors/gold_master.py` — SOLO LECTURA, nunca modificar.
> Hoja de salida API: `H73_OUTPUT_API` (123 hojas · 931 KB)

## Arquitectura del Excel (3 niveles — ADR-023)

```
Nivel 1 (Motor): Gold Master SIAP-ICPI v5.5 — calcula todo
Nivel 2 (SO):    QUIRA — lee vía connector, traza, explica
Nivel 3 (UI):    Dashboards — solo visualizan, no calculan
```

## Índices Principales (LECTURA CONFIRMADA — Q1-2026)

### TGI — Territorial Governance Index (5 dimensiones)

| Dimensión | Clave | Peso | Valor Q1-2026 | Semáforo |
|---|---|---|---|---|
| D1 Trust Score Metodológico | TGI_D1 | 20% | 83.2% | 🟢 |
| D2 ICPI Cumplimiento Metas PDyOT | TGI_D2 | 20% | 69.93% | 🟡 |
| D3 Ti Inversión eSIGEF G7+G8 | TGI_D3 | 25% | 59.85% | 🟡 |
| D4 IET Equidad Territorial Rural | TGI_D4 | 25% | 44.79% | 🔴 CRÍTICO |
| D5 ICM Reporte SNP | TGI_D5 | 10% | 100% | 🟢 |
| **GLOBAL** | **TGI_SCORE** | **100%** | **66.79%** 🟡 | Transición con Riesgos |

### ICPI — Índice Cantonal de Planificación Integrada

| Clave | Valor | Descripción |
|---|---|---|
| ICPI_GLOBAL_PCT | 17.45% (Q1) / 69.93% (2025) | Acumulado Q1 vs anual 2025 |
| ICPI_2023 | 57.36% | Histórico |
| ICPI_2024 | 67.12% | Histórico |
| ICPI_2025 | 69.93% | Certificado — fuente de verdad |
| ICPI_META_PDOT | 65% | Umbral institucional |
| BRECHA_ICPI_PP | 47.55% | Brecha vs meta |
| ICPI_CLASIFICACION | Ruptura Sistémica (Q1) | Clasificación actual |

### IED — Índice de Eficiencia Documental

| Clave | Valor | Descripción |
|---|---|---|
| IED_GLOBAL | 16.52% | Eficiencia documental global |
| IED_DIRECCIONES_N | 11 | Número de direcciones evaluadas |

### ITAM — Índice de Transparencia y Acceso Municipal

| Clave | Valor | Descripción |
|---|---|---|
| ITAM_2025_REF | 82.29% | Referencia 2025 |

### IGP — Índice de Gobernanza Participativa

| Clave | Valor |
|---|---|
| IGP_REF_2025 | 27.98% |
| IGP_2026_ACTUAL | 48.33% |

### IOC — Índice de Opacidad Cantonal

| Clave | Valor | Descripción |
|---|---|---|
| IOC_OPACIDAD | 17.71% | Gap A↔D — base de ADR-022 |
| IOC_METAS_SIN_URL | 4 | Metas sin evidencia URL |

### IRS — Índice de Regresividad Social

| Clave | Valor |
|---|---|
| IRS_GLOBAL | 79.7% |
| IRS_CLASIFICACION | Muy Regresivo · Composite_Need v2.1 |
| COMPOSITE_NEED_LEADER | Isabel Muentes |

### IET — Índice de Equidad Territorial

| Clave | Valor |
|---|---|
| IET_GINI_TERRITORIAL | 0.9273 |
| IET_PERCAPITA_PEOR | 44.80% |
| BRECHA_RURAL_USD | $1,371,051 |

### IRS / NBI (Necesidades Básicas Insatisfechas)

| Clave | Valor |
|---|---|
| NBI_RURAL_PCT | 67.90% |
| NBI_URBANA_PCT | 23.00% |

## Datos Presupuestarios (Montecristi 2026)

| Clave | Valor |
|---|---|
| PRESUPUESTO_TOTAL_4E | $54,242,424.28 |
| GAD_CODIFICADO_2026 | $45,977,893.81 |
| GAD_DEVENGADO_Q1 | $5,147,258.86 |
| FONDOS_PORTAFOLIO | $7,440,000 |
| FONDOS_ELEGIBLES | $2,580,000 |
| BRECHA_FONDOS_BLOQ | $3,660,000 |

## SAT — Sistema de Alertas Tempranas

| Clave | Valor |
|---|---|
| SAT_ACTIVAS_COUNT | 2 |
| SAT_RIESGO_TOTAL | 20% |
| SAT_CLASIF_RIESGO | MEDIO |

## Datos Institucionales

| Clave | Valor |
|---|---|
| ENTIDAD | GAD Municipal de Montecristi |
| PERIODO_CORTE | 2026-04-30 |
| VERSION_SISTEMA | v1.0 Gold Master |
| MODELO_VALIDO | VÁLIDO |
| PARROQUIAS_TOTAL | 7 |
| MMP_AVANCE_PCT | 1% |
| TRUST_SCORE (H89) | 89.6 |
| IFE_PROMESAS_TOTAL | 66 |
| IFE_PROMESAS_PDOT | 48 |
| IFE_GLOBAL | 72.73% |
| ICODS_GLOBAL | 87.5% |

## Estructura de Hojas (H01-H99+)

```
H01        — Parámetros base y configuración global
H73_OUTPUT_API — Hoja de salida API (lectura del connector)
H89_TRUST_SCORE — Trust Score metodológico (D1 del TGI)
G6.1_OUTPUT_API — Fallback v6.0 template
```

## Reglas de Uso (ADR-023 — INMUTABLE)

1. **NUNCA recalcular** fuera del Excel. El Gold Master ES la fuente de verdad.
2. **Solo leer** vía `app/connectors/gold_master.py`. Nunca modificar el Excel desde código.
3. **Bloomberg Firewall**: H01-H99, QTMP, node IDs (Dom07, C01, CE_226) nunca en UI pública.
4. **Flujo canónico**: Excel → Python (connector) → Supabase → UI. Nunca al revés.

## Cadena ICPI→TGI→QUIRA

```
Gold Master SIAP-ICPI v5.5
  ↓ calcula
  ICPI (D2 del TGI) = 69.93% anual 2025
  Ti (D3 del TGI) = 59.85%
  Trust Score (D1 del TGI) = 83.2%
  IET Rural (D4 del TGI) = 44.79% ← CRÍTICO
  ICM SNP (D5 del TGI) = 100%
  ↓ compone
  TGI = 66.79% 🟡 Transición con Riesgos
  ↓ QUIRA ingesta y explica
  "¿Por qué TGI = 66.79%?" → explainability_report.py
```

---
*Gold Master Schema v1.0 · Dylus Lab · 2026-06-03*
*Generado desde app/connectors/gold_master.py — datos Q1-2026*
*CONFIDENCIAL — solo Dylus Lab*
