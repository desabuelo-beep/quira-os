---
name: "SAT — Sistema de Alertas y Trazabilidad"
description: "Catálogo canónico SAT-0 a SAT-VI: triple ancla legal, operativa y doctrinal. El SAT no es metodología paralela a la ley — es la capa de validación doctrinal SOBRE la ley."
tipo: meta-sistema
version: "v5.5"
desarrollador: "Dylus Lab / QUIRA Gov"
gold_master: "Gold Master TGI v5.5"
fecha: "2026-05-25"
tags: [sat, alertas, trazabilidad, core, quira, tgi, sat-catalogo]
---

# SAT — Sistema de Alertas y Trazabilidad

> **El SAT no es sanción. Es detección temprana.**
> Cada alerta SAT tiene base legal, base operativa y base doctrinal.
> El objetivo es siempre: actuar ANTES de que el riesgo escale.

Vincula → [[01_TGI_FRAMEWORK]] · [[02_TGI_DIMENSIONES]] · [[06_IED_DIRECTIVO]] · [[09_RCM_LONGITUDINAL]]

---

## Triple Ancla Canónica — Estructura de Toda Alerta SAT

| Capa | Qué contiene | Ejemplo |
|------|-------------|---------|
| **Legal** | Artículo de ley que activa la alerta | Art. 113 COPFP — evaluación presupuestaria |
| **Operativa** | Valor observado que dispara el umbral | D3 Ti = 14.58% (umbral < 60%) |
| **Doctrinal QUIRA** | Clasificación de riesgo y marco de acción | SAT-III REINCIDENTE — 3+ períodos |

---

## Catálogo SAT — Niveles y Activadores

| Nivel | Nombre | Activador | Dimensión TGI | Umbral |
|-------|--------|-----------|---------------|--------|
| **SAT-0** | Observación Inicial | Cualquier métrica en zona amarilla | D1-D5 | Primer período |
| **SAT-I** | Alerta Operativa | Ti < 60% en 1 período | D3 Ejecución | < 60% |
| **SAT-II** | Alerta de Planificación | D2_Score < 65% en 1 período | D2 Planificación | < 65% |
| **SAT-III** | Reincidencia Crítica | Ti < 60% por 3 períodos consecutivos | D3 Ejecución | Persistencia |
| **SAT-IV** | Brecha Territorial | IRS > 70 o IET_parroquia < 50 | D4 Equidad | IRS > 70 |
| **SAT-V** | Opacidad Directiva | Director no entrega informe firmado | D5 Capacidad | Ti_V = 0 |
| **SAT-VI** | Riesgo Sistémico | ICPI Global < 50% | D1-D5 | < 50% |

---

## SAT-III REINCIDENTE — La Regla RC-M

```
Si D3 Ti < 60% por 3 períodos consecutivos → SAT-III REINCIDENTE
```

**Base legal:** COPFP Art. 113 — evaluación obligatoria de ejecución presupuestaria
**Base operativa:** Tasa de Inversión ejecutada sostenidamente por debajo del umbral
**Base doctrinal:** La reincidencia distingue ineficiencia puntual de patrón estructural

→ Ver tabla RC-M en [[09_RCM_LONGITUDINAL]]

---

## AVEP — Lenguaje de Comunicación Política

El SAT produce señales técnicas. AVEP las traduce al lenguaje del Alcalde:

| Nivel AVEP | Icono | Condición | Mensaje |
|-----------|-------|-----------|---------|
| Gestión por Mandato | 🟢 | ICPI ≥ 75% · Sin SAT activas | Ejecución alineada al PDOT |
| Transición Crítica | 🟡 | ICPI 60-74% · SAT-I o SAT-II | Requiere decisiones correctivas |
| Gestión por Ocurrencia | 🟠 | ICPI 50-59% · SAT-III | Patrón de desviación del mandato |
| Nivel de Atención Alta | 🔴 | ICPI < 50% · SAT-IV a SAT-VI | Riesgo sistémico — acción inmediata |

→ Ver detalle en [[07_AVEP_LENGUAJE]]

---

## Flujo SAT — Del Dato a la Acción

```
DATOS OFICIALES (DPE · SERCOP · CPCCS · Gold Master)
    ↓
EVALUACIÓN (sat_evaluator.py — triple ancla)
    ↓
CLASIFICACIÓN SAT-0 a SAT-VI
    ↓
NIVEL AVEP (🟢🟡🟠🔴)
    ↓
PROTOCOLO DE ACCIÓN PREVENTIVA (Gold Master G5.4_PROTOCOLO_ACCION)
    ↓
MONITOR RC-M (registro longitudinal para detectar reincidencia)
```

---

## Estado Actual — GADM Montecristi (2026)

| Alerta | Tipo | Dimensión | Estado |
|--------|------|-----------|--------|
| D3 Ti Crítico | SAT-I | D3 Ejecución | ACTIVA |
| Brecha Rural $1.79M | SAT-IV | D4 Equidad | ACTIVA |
| ICPI Global < 65% | SAT-VI | Sistémico | ACTIVA |

**Nivel AVEP actual:** 🔴 Nivel de Atención Alta
**ICPI Global:** 53.56% · **Riesgo ponderado:** ALTO

---

## Implementación en quira-os

| Archivo | Función |
|---------|---------|
| `app/services/sat_evaluator.py` | Evaluador SAT con triple ancla |
| `app/services/snapshot_diff.py` | Detecta reincidencia entre períodos |
| `quira_pages/m2_alertas.py` | UI: tab SAT Activas + Evolución RC-M |
| `app/services/longitudinal_engine.py` | RC-M: detecta SAT-III reincidente |
| Gold Master G5.1_SAT_CATALOGO | Fuente canónica del catálogo |

---

**Fuente canónica:** Gold Master TGI v5.5 · G5.1_SAT_CATALOGO · SAT_Catalogo sheet
**Doctrina:** NORTH.md → "SAT es capa de validación doctrinal SOBRE la ley"
**Fecha:** 2026-05-25
