---
name: "Índice TGI Parroquias — GADM Montecristi"
description: "Índice del módulo 07 — perfiles TGI 5D de las 7 parroquias del cantón Montecristi 2026"
tipo: indice-modulo
modulo: "07_TGI_Parroquias"
total_parroquias: 7
tgi_rural_avg: 66.85
tgi_cantonal: 68.82
fecha: "2026-05-16"
fuente: "SIAP-ICPI_GOLD_MASTER_v5.3 · quira_extract.py"
---

# Módulo 07 — TGI Parroquias · GADM Montecristi 2026

**Fuente canónica:** SIAP-ICPI_GOLD_MASTER_v5.3_TGI_20260516.xlsx · Motor TGI Territorial  
**Modelo:** TGI 5D — D1 Legalidad (20%) · D2 Planificación (20%) · D3 Ejecución (25%) · D4 Equidad (25%) · D5 Capacidad (10%)  
**Diferenciador territorial:** D4 = MIN(100, IET_Local) — único indicador que varía por parroquia

---

## Ranking TGI 5D — Cantón Montecristi

| Rank | Parroquia | Tipo | TGI Score | Nivel | IET Local |
|------|-----------|------|-----------|-------|-----------|
| #1 | [[P-01_Montecristi]] | Urbana | 80.65 | 🟢 Gobernanza Inteligente | 193.75 |
| #2 | [[P-05_Gral_Alfaro]] | Rural | 71.50 | 🟡 Transición con Riesgos | 63.39 |
| #3 | [[P-02_Anibal_San_Andres]] | Rural | 68.60 | 🟡 Transición con Riesgos | 51.79 |
| #4 | [[P-07_La_Pila]] | Rural | 67.26 | 🟡 Transición con Riesgos | 46.43 |
| #5 | [[P-04_Leonidas_Proano]] | Rural | 66.36 | 🟡 Transición con Riesgos | 42.86 |
| #6 | [[P-06_Isabel_Muentes]] | Rural | 64.58 | 🟠 Inequidad Estructural | 35.71 |
| #7 | [[P-03_Colorado]] | Rural | 62.79 | 🟠 Inequidad Estructural | 28.57 |

**TGI_5D_Rural_Avg:** 66.85 · 🟡 Transición con Riesgos  
**TGI_5D_Cantonal:** 68.82

---

## Parroquias Críticas por Indicador

| Indicador | Parroquia más crítica | Valor |
|-----------|-----------------------|-------|
| Mayor NBI (pobreza) | Isabel Muentes | 61.2% |
| Menor cobertura agua | Isabel Muentes | 1.02% |
| Menor IET (sub-inversión) | Colorado | 28.57 |
| Menor TGI Score | Colorado | 62.79 |
| Mayor Composite Need | Isabel Muentes | 0.619 |

---

## Dimensiones TGI (valores cantorales)

| Dimensión | Peso | Valor | Fuente Excel |
|-----------|------|-------|--------------|
| D1 — Legalidad y Coherencia | 20% | 83.50 | Trust Score (Motor TGI) |
| D2 — Fidelidad Planificación | 20% | 69.93 | H01!B15×100 |
| D3 — Ejecución Presupuestaria | 25% | 59.85 | H07b!B18×100 |
| **D4 — Equidad Territorial** ★ | **25%** | **variable** | H99!J7:J13 |
| D5 — Capacidad Institucional | 10% | 100.00 | H01!B12×100 |

> ★ D4 es el único diferenciador parroquial real. D1/D2/D3/D5 son cantorales.

---

## Nota Maestra

- [[TGI_Cantonal]] — Dashboard cantonal: ranking, brechas acumuladas, prioridades de reequilibrio, alertas

---

## Hojas de Auditoría (v5.4)

- [[03_SIAP_ICPI_METHOD]] — Motor TGI QUIRA — Validaciones metodológicas
- [[03_SIAP_ICPI_METHOD]] — Trazabilidad de variables (Motor TGI)
- [[03_SIAP_ICPI_METHOD]] — Limitaciones metodológicas declaradas
- [[02_TGI_DIMENSIONES]] — Marco metodológico completo 5D
- [[03_SIAP_ICPI_METHOD]] — Motor de cálculo territorial

---

Vincula → [[03_SIAP_ICPI_METHOD]] · [[02_TGI_DIMENSIONES]] · [[03_SIAP_ICPI_METHOD]]
