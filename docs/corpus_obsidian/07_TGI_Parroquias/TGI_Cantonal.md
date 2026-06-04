---
name: "TGI Cantonal — GADM Montecristi 2026"
description: "Dashboard TGI 5D cantonal — scores, brechas y prioridades de reequilibrio"
tipo: dashboard-cantonal
tgi_score_cantonal: 68.82
tgi_score_rural_avg: 66.85
d1_legalidad: 83.5
d2_planificacion: 69.93
d3_ejecucion: 59.85
d5_capacidad: 100.0
irs_global: 79.7
brecha_rural_total_usd: 1791935
parroquia_critica: "Colorado"
parroquia_prioridad_1: "Isabel Muentes"
fecha: "2026-05-16"
fuente: "QUIRA Gov · Motor TGI Territorial"
tags: [tgi, cantonal, dashboard, equidad-territorial, montecristi]
---

# TGI Cantonal — GADM Montecristi 2026

**Modelo TGI 5D** · D1 Legalidad (20%) · D2 Planificación (20%) · D3 Ejecución (25%) · D4 Equidad (25%) · D5 Capacidad (10%)

Vincula → [[_Índice_Parroquias]] · [[03_SIAP_ICPI_METHOD]] · [[02_TGI_DIMENSIONES]] · [[03_SIAP_ICPI_METHOD]]

---

## 1. Score Cantonal — Dimensiones TGI 5D

| Dimensión | Peso | Valor | Fuente Excel | Estado |
|-----------|------|-------|--------------|--------|
| D1 — Legalidad y Coherencia | 20% | 83.50% | Trust Score (Motor TGI) | ✅ |
| D2 — Fidelidad Planificación | 20% | 69.93% | H01!B15×100 | ⚠️ |
| D3 — Ejecución Presupuestaria | 25% | 59.85% | H07b!B18×100 | ⚠️ |
| **D4 — Equidad Territorial** ★ | **25%** | **variable** | H99!J7:J13 | 🔴 |
| D5 — Capacidad Institucional | 10% | 100.00% | H01!B12×100 | ✅ |

> ★ D4 es el único diferenciador parroquial. Valores van de 28.6 (Colorado) a 100.0 (Montecristi, cap 100).

| Métrica | Valor |
|---------|-------|
| **TGI_5D_Cantonal** (7 parroquias) | **68.82** |
| **TGI_5D_Rural_Avg** (6 rurales) | **66.85** |
| IRS_Global (regresividad inversión) | **79.7** — inversión concentrada en cabecera |

---

## 2. Ranking Parroquial TGI 5D

| Rank | Parroquia | Tipo | TGI Score | Nivel | IET Local | Clasif. Equidad |
|------|-----------|------|-----------|-------|-----------|-----------------|
| #1 | [[P-01_Montecristi]] | Urbana | 80.65 | 🟢 Gobernanza Inteligente | 193.75 | Sobre la media |
| #2 | [[P-05_Gral_Alfaro]] | Rural | 71.50 | 🟡 Transición con Riesgos | 63.39 | Alta |
| #3 | [[P-02_Anibal_San_Andres]] | Rural | 68.60 | 🟡 Transición con Riesgos | 51.79 | Alta |
| #4 | [[P-07_La_Pila]] | Rural | 67.26 | 🟡 Transición con Riesgos | 46.43 | Crítica |
| #5 | [[P-04_Leonidas_Proano]] | Rural | 66.36 | 🟡 Transición con Riesgos | 42.86 | Crítica |
| #6 | [[P-06_Isabel_Muentes]] | Rural | 64.58 | 🟠 Inequidad Estructural | 35.71 | Crítica |
| #7 | [[P-03_Colorado]] | Rural | 62.79 | 🟠 Inequidad Estructural | 28.57 | Crítica |

---

## 3. Mapa de Prioridad de Reequilibrio (Rurales)

Índice = NBI×0.40 + (1-Agua)×0.30 + (1-TGI/100)×0.30 · Rango 0-1

| Prioridad | Parroquia | Score | Brecha USD | NBI | Agua |
|-----------|-----------|-------|------------|-----|------|
| 1 | [[P-06_Isabel_Muentes]] | 0.648 | $+410,477 | 61.2% | 1.02% |
| 2 | [[P-03_Colorado]] | 0.530 | $+304,021 | 58.7% | 38.82% |
| 3 | [[P-07_La_Pila]] | 0.472 | $+275,984 | 55.9% | 50.0% |
| 4 | [[P-02_Anibal_San_Andres]] | 0.402 | $+280,752 | 52.1% | 67.01% |
| 5 | [[P-04_Leonidas_Proano]] | 0.318 | $+262,369 | 54.3% | 100.0% |
| 6 | [[P-05_Gral_Alfaro]] | 0.285 | $+258,332 | 49.8% | 100.0% |

**Brecha Rural Total:** $+1,791,935 USD (déficit acumulado 6 parroquias rurales vs media cantonal)

---

## 4. Alertas Cantonales

- 🔴 **IRS_Global = 79.7** — inversión fuertemente concentrada en Montecristi urbana
- 🔴 **4 de 6 parroquias rurales** en categoría Crítica (IET < 50)
- ⚠️ **D3 Ejecución = 59.9%** — ejecución presupuestaria por debajo del umbral óptimo (75%)
- ⚠️ **Colorado** — TGI más bajo (62.79) + IET=28.6
- ⚠️ **Isabel Muentes** — máxima urgencia reequilibrio (Prior=0.648)
- ⚠️ Brecha rural acumulada **$1,791,935 USD** Q1-2026

---

## 5. Metodología

| Aspecto | Detalle |
|---------|---------|
| Modelo | TGI 5D — 5 dimensiones ponderadas |
| Diferenciador parroquial | D4 = MIN(100, IET_Local) — único por parroquia |
| Fuente canónica | SIAP-ICPI_GOLD_MASTER_v5.4 · Motor TGI Territorial |
| Extracción | quira_extract.py · 2026-05-16 |
| Auditoría motor | Motor TGI QUIRA — Validaciones · Trazabilidad · Limitaciones |
| Versión Gold Master | v5.4 (Brecha/Prioridad Edition) |

---

**Fuente:** SIAP-ICPI Gold Master v5.4 · Motor TGI Territorial · QUIRA Gov
**Extracción:** 2026-05-16 · quira_extract.py
