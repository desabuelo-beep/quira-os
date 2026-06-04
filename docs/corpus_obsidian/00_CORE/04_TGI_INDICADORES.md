---
name: "TGI Indicadores — Glosario Canónico"
description: "Glosario canónico de todos los indicadores TGI con fórmulas, rangos y trazabilidad al Gold Master"
tipo: meta-indicadores
version: "v5.4"
fecha: "2026-05-16"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
tags: [tgi, indicadores, irs, iet, icpi, trust-score, formulas, core]
---

# TGI Indicadores — Glosario Canónico

> Todos los indicadores son trazables a una celda específica del Gold Master.
> Si un indicador no tiene celda fuente: **no existe en el sistema**.

Vincula → [[01_TGI_FRAMEWORK]] · [[02_TGI_DIMENSIONES]] · [[03_SIAP_ICPI_METHOD]]

---

## Indicadores Primarios

### TGI Score 5D

| Campo | Valor |
|-------|-------|
| Definición | Índice compuesto de gobernanza territorial — 5 dimensiones ponderadas |
| Fórmula | `D1×0.20 + D2×0.20 + D3×0.25 + D4×0.25 + D5×0.10` |
| Rango | 0 – 100 |
| Celda Gold Master | H99!Y7:Y13 (por parroquia) |
| Valor cantonal | 68.82 (GADM Montecristi, Q1-2026) |
| Valor rural avg | 66.85 |

**Niveles:**
- ≥ 85 → Gobernanza Inteligente
- 70–84 → Transición con Riesgos
- 50–69 → Inequidad Estructural
- < 50 → Crisis de Gobernanza

---

### IET — Índice de Equidad Territorial

| Campo | Valor |
|-------|-------|
| Definición | Proporción entre la inversión per cápita local y la media cantonal |
| Fórmula | `IET = (InvPerCap_Local / InvPerCap_Cantonal) × 100` |
| Rango | 0 – sin límite (IET > 100 = sobre la media) |
| Celda Gold Master | H99!J7:J13 |
| Uso en TGI | D4 = MIN(100, IET_Local) |

**Valores Montecristi 2026:**

| Parroquia | IET Local | Clasif |
|-----------|-----------|--------|
| Montecristi | 193.75 | Sobre la media |
| General Alfaro | 63.39 | Alta |
| Aníbal San Andrés | 51.79 | Alta |
| La Pila | 46.43 | Crítica |
| Leónidas Proaño | 42.86 | Crítica |
| Isabel Muentes | 35.71 | Crítica |
| Colorado | 28.57 | Crítica |

---

### IRS — Índice de Regresividad Social

| Campo | Valor |
|-------|-------|
| Definición | Concentración de la inversión pública en la cabecera cantonal vs territorios rurales |
| Fórmula | `IRS = (InvCabecera / InvTotal) × 100` |
| Rango | 0 – 100 (mayor IRS = mayor regresividad) |
| Valor Montecristi | 79.7 — inversión fuertemente concentrada en Montecristi urbana |
| Alerta | IRS > 70 se considera regresivo para un GAD con alta ruralidad |

---

### Brecha_Eq_USD

| Campo | Valor |
|-------|-------|
| Definición | Monto absoluto del déficit o superávit de inversión vs media cantonal (en USD) |
| Fórmula | `Pob × InvPerCap × (100/IET − 1)` equivale a `Pob × (InvPerCap_Cantonal − InvPerCap_Local)` |
| Signo | Positivo = déficit (subreinversión) · Negativo = superávit (sobre-inversión) |
| Celda Gold Master | H99!Z7:Z13 |
| Brecha Rural Total | $+1,791,935 USD (suma parroquias rurales) |

**Valores Montecristi 2026:**

| Parroquia | Brecha USD |
|-----------|-----------|
| Montecristi | −$4,176,xxx (sobre-invertida) |
| General Alfaro | +$258,332 |
| Aníbal San Andrés | +$280,752 |
| La Pila | +$275,984 |
| Leónidas Proaño | +$262,369 |
| Isabel Muentes | +$410,477 |
| Colorado | +$304,021 |

---

### Prioridad_Reequil

| Campo | Valor |
|-------|-------|
| Definición | Índice compuesto de urgencia de reequilibrio territorial |
| Fórmula | `NBI%×0.40 + (1−Agua%)×0.30 + (1−TGI/100)×0.30` |
| Rango | 0 – 1 (mayor = más urgente) |
| Celda Gold Master | H99!AA7:AA13 |

**Ponderación:**
- NBI (pobreza): 40% — necesidad básica insatisfecha
- Agua (cobertura invertida): 30% — acceso a servicio básico crítico
- TGI (déficit de gobernanza): 30% — capacidad institucional de respuesta

**Valores Montecristi 2026:**

| Prioridad | Parroquia | Score | NBI | Agua |
|-----------|-----------|-------|-----|------|
| 1 | Isabel Muentes | 0.648 | 61.2% | 1.02% |
| 2 | Colorado | 0.530 | 58.7% | 38.82% |
| 3 | La Pila | 0.472 | 55.9% | 50.0% |
| 4 | Aníbal San Andrés | 0.402 | 52.1% | 67.01% |
| 5 | Leónidas Proaño | 0.318 | 54.3% | 100.0% |
| 6 | General Alfaro | 0.285 | 49.8% | 100.0% |

---

### ICPI — Índice de Capacidad e Progreso Institucional

| Campo | Valor |
|-------|-------|
| Definición | Medida integral de la capacidad operativa y el progreso del GAD |
| Origen | Hoja H01 — ENGINE CORE institucional |
| Uso en TGI | Alimenta D1 (legalidad) y D5 (capacidad) |
| Valor Montecristi | D5 = 100% (capacidad base verificada) |

---

### CompositeNeed

| Campo | Valor |
|-------|-------|
| Definición | Índice compuesto de necesidad territorial [0-1] |
| Celda | H99!I7:I13 |
| Mayor need | Isabel Muentes (0.619) |
| Uso | Referencia de prioridad sin ponderación presupuestaria |

---

## Relaciones Entre Indicadores

```
Datos territoriales (NBI, Agua, Pob, InvPerCap)
    ↓
IET = InvPerCap / CantAvg × 100
    ↓
D4 = MIN(100, IET)       ─────────────────────┐
Brecha_USD = Pob×G×(100/IET-1)               │
Prioridad = NBI×0.4 + (1-Agua)×0.3 + (1-TGI/100)×0.3
    ↓                                         │
TGI = D1×0.2 + D2×0.2 + D3×0.25 + D4×0.25 + D5×0.1 ←┘
    ↓
Clasificación + Alertas + Recomendaciones
```

---

## Alertas Cantonales Activas (Q1-2026)

- IRS_Global = 79.7 — inversión fuertemente concentrada en Montecristi urbana
- 4 de 6 parroquias rurales con IET < 50 (categoría Crítica)
- D3 Ejecución = 59.85% — por debajo del umbral óptimo (75%)
- Brecha rural acumulada = $1,791,935 USD

---

**Fuente:** SIAP-ICPI_GOLD_MASTER_v5.4 · Motor TGI Territorial · Motor TGI Framework
**Auditoría:** Motor TGI QUIRA — Validaciones y Trazabilidad de indicadores
**Fecha:** 2026-05-16
