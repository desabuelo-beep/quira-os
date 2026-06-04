---
name: "MMP — Monitor de Progreso Mensual"
description: "Matriz 25 metas PDOT × 12 meses. Captura el progreso mensual de cada meta estratégica del Plan Bicentenario 2023-2027. Alimenta D2_Score (Fidelidad a la Planificación)."
tipo: meta-monitor
version: "v5.5"
desarrollador: "Dylus Lab / QUIRA Gov"
gold_master: "Gold Master TGI v5.5"
fecha: "2026-05-25"
tags: [mmp, mensual, metas, pdot, planificacion, d2, monitor, core]
---

# MMP — Monitor de Progreso Mensual

> **El MMP convierte el PDOT de documento a instrumento vivo.**
> 25 metas estratégicas × 12 meses = 300 celdas de trazabilidad anual.
> Cada meta tiene responsable, presupuesto y evidencia verificable.

Vincula → [[02_TGI_DIMENSIONES]] D2 · [[06_IED_DIRECTIVO]] · [[09_RCM_LONGITUDINAL]]

---

## Estructura MMP

```
Fila = Meta PDOT (25 metas del Plan Bicentenario 2023-2027)
Columna = Mes (Enero a Diciembre)
Celda = % avance mensual verificado

Valor celda:
  0% = sin avance registrado
  Parcial = avance documentado con evidencia
  100% = meta cumplida con SHA-256 de evidencia
```

**Hoja Gold Master:** G4.3_MMP (antes H25_MMP en v5.5)
**Alimenta:** D2_Score = promedio ponderado de avance acumulado

---

## Las 25 Metas PDOT — Plan Bicentenario 2023-2027

El MMP cubre las 25 metas vinculantes del PDOT vigente, organizadas por eje:

| Eje | Metas | Dimensión TGI |
|-----|-------|---------------|
| FA — Físico Ambiental | 5 metas | D4 Equidad · D3 Ejecución |
| SC — Socio-Cultural | 6 metas | D2 Planificación |
| EP — Económico Productivo | 4 metas | D2 Planificación · D3 |
| AH — Asentamientos Humanos | 6 metas | D3 Ejecución · D4 Equidad |
| PI — Político Institucional | 4 metas | D1 Legalidad · D5 Capacidad |

→ Ver programas detallados en `01_PDOT/propuesta_tgi/`

---

## Flujo MMP — Del PDOT a la Celda

```
1. PDOT define 25 metas estratégicas con responsable y presupuesto
2. POA desagrega cada meta en actividades anuales
3. Cada mes, Director responsable sube informe de avance
4. Técnico QUIRA verifica evidencia → actualiza celda MMP
5. D2_Score = f(celdas completadas / total celdas del período)
6. ICPI Global → recalculado con nuevo D2_Score
```

**Evidencia aceptada:** acta, resolución, informe técnico, foto de obra, datos SERCOP

---

## Relación MMP ↔ IED ↔ H07c

El MMP y el IED se alimentan del mismo flujo de ingesta mensual (H07c):

```
Director → informe mensual firmado → SHA-256
    ↓
    ├── Actualiza IED de esa dirección (G4.4)
    └── Actualiza MMP de las metas bajo su responsabilidad (G4.3)
```

Un solo acto de ingesta alimenta ambos índices.

---

## D2_Score vs D2 Antiguo (ICPI_69.93%)

**Importante:** El valor 69.93% que aparece en notas anteriores del vault (v5.4) corresponde al D2_Score del período base. Este valor es distinto del ICPI Global:

| Métrica | Valor | Qué mide |
|---------|-------|----------|
| ICPI Global | 53.56% | Composite D1-D5 ponderado |
| D2_Score | 69.93% | Solo fidelidad a la planificación |

En notas anteriores, D2_Score fue erróneamente llamado "ICPI_Global". En v6.0 queda disambiguado: el ICPI Global es el composite, D2_Score es solo la dimensión de planificación.

---

## Estado Actual MMP — GADM Montecristi

| Período | Metas con avance | % completitud |
|---------|-----------------|---------------|
| 2023 | Verificando | — |
| 2024 | Verificando | — |
| 2025 (acumulado) | En proceso | — |
| 2026 (activo) | Ingesta manual | — |

*El MMP completo se activa cuando el flujo H07c digital esté implementado.*

---

**Fuente canónica:** Gold Master TGI v5.5 · H25_MMP → G4.3_MMP (v6.0)
**Marco legal:** COPFP Art. 41-44 — seguimiento y evaluación obligatorio del plan
**Fecha:** 2026-05-25
