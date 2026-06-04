---
name: "TGI Framework — Territorial Governance Intelligence"
description: "Marco metodológico canónico TGI 5D desarrollado por QUIRA Gov / Dylus Lab"
tipo: meta-framework
version: "v5.4"
desarrollador: "Dylus Lab / QUIRA Gov"
caso_piloto: "GADM Montecristi 2026"
fecha: "2026-05-16"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
tags: [tgi, framework, metodologia, core, quira]
---

# TGI — Territorial Governance Intelligence

> **TGI** es el framework metodológico propietario de QUIRA Gov para transformar normativa, planificación, ejecución fiscal y realidad territorial en señales accionables de gobernanza basada en evidencia.
>
> **Desarrollado por:** Dylus Lab · QUIRA Gov
> **Origen:** Modelo canónico Excel SIAP-ICPI, validado en GADM Montecristi 2026

Vincula → [[00_QUIRA_GOV]] · [[02_TGI_DIMENSIONES]] · [[03_SIAP_ICPI_METHOD]] · [[04_TGI_INDICADORES]]

---

## Arquitectura del Framework

```
TGI (Territorial Governance Intelligence)
├── D1 — Legalidad y Coherencia Normativa     [20%]
├── D2 — Fidelidad a la Planificación          [20%]
├── D3 — Ejecución Presupuestaria              [25%]
├── D4 — Equidad Territorial                   [25%]  ★ diferenciador parroquial
└── D5 — Capacidad Institucional               [10%]
```

**TGI Score = D1×0.20 + D2×0.20 + D3×0.25 + D4×0.25 + D5×0.10**

---

## Módulos Conectados

| Módulo | Vínculo | Tipo |
|--------|---------|------|
| [[../01_PDOT/_Índice_PDOT]] | Alimenta D1/D2 | Planificación y normativa |
| [[../06_Normativa/_Índice_Normativa]] | Alimenta D1 | Legalidad |
| [[../05_Presupuesto/_Índice_Presupuesto]] | Alimenta D3 | Ejecución fiscal |
| [[../07_TGI_Parroquias/_Índice_Parroquias]] | Resultados D4 | Equidad territorial |
| [[../03_Cooperacion/_Índice_Cooperacion]] | Contexto D5 | Capacidad institucional |

---

## Normas Habilitantes Ecuador

| Artículo | Norma | Dimensión TGI |
|----------|-------|---------------|
| Art. 238 CRE | Autonomía GAD | D1 Legalidad |
| Art. 41-43 COPFP | Planificación obligatoria | D2 Planificación |
| Art. 215-220 COOTAD | Presupuesto participativo | D3 Ejecución |
| Art. 249 CRE | Servicios básicos garantizados | D4 Equidad |
| Art. 338 COOTAD | Capacidades institucionales GAD | D5 Capacidad |

> Fuente verificable: COOTAD, COPFP, CRE vigentes. Sin alucinación normativa.

---

## Niveles de Gobernanza TGI

| Score | Nivel | Descripción |
|-------|-------|-------------|
| ≥ 85 | Gobernanza Inteligente | GAD líder — modelo replicable |
| 70–84 | Transición con Riesgos | Avances sólidos con brechas identificadas |
| 50–69 | Inequidad Estructural | Requiere intervención focalizada |
| < 50 | Crisis de Gobernanza | Riesgo institucional — alerta máxima |

---

## Resultados Validados — GADM Montecristi 2026

| Parroquia | TGI Score | Nivel | IET Local |
|-----------|-----------|-------|-----------|
| Montecristi (urbana) | 80.65 | Gobernanza Inteligente | 193.75 |
| General Alfaro | 71.50 | Transición con Riesgos | 63.39 |
| Aníbal San Andrés | 68.60 | Transición con Riesgos | 51.79 |
| La Pila | 67.26 | Transición con Riesgos | 46.43 |
| Leónidas Proaño | 66.36 | Transición con Riesgos | 42.86 |
| Isabel Muentes | 64.58 | Inequidad Estructural | 35.71 |
| Colorado | 62.79 | Inequidad Estructural | 28.57 |

**TGI Cantonal:** 68.82 · **TGI Rural Avg:** 66.85 · **IRS Global:** 79.7

---

## Indicadores Base

Ver [[04_TGI_INDICADORES]] para fórmulas completas y trazabilidad.

| Indicador | Definición | Fuente Gold Master |
|-----------|------------|-------------------|
| **TGI Score** | Índice compuesto 5D ponderado | H99!Y7:Y13 |
| **IET** | Índice de Equidad Territorial = InvPerCap/CantAvg×100 | H99!J7:J13 |
| **IRS** | Índice de Regresividad Social = InvUrb/InvTotal×100 | **Motor TGI Territorial** |
| **ICPI** | Índice de Capacidad e Progreso Institucional | H01 ENGINE |
| **Brecha_USD** | Pob×InvPerCap×(100/IET−1) | H99!Z7:Z13 |
| **Prioridad_Reequil** | NBI×0.40 + (1-Agua)×0.30 + (1-TGI/100)×0.30 | H99!AA7:AA13 |

---

## Estado Metodológico

| Campo | Valor |
|-------|-------|
| Versión | TGI v5.4 (Brecha/Prioridad Edition) |
| Estado | Experimental validado en GADM Montecristi |
| Auditoría motor | Motor TGI QUIRA — Validaciones · Trazabilidad · Limitaciones |
| Limitaciones | Ver [[03_SIAP_ICPI_METHOD]] |
| Replicabilidad | Alta — requiere adaptación de IET por territorio |

---

**Fuente canónica:** QUIRA Gov · Motor TGI Territorial · Motor TGI Framework
**Extracción:** quira_extract.py · 2026-05-16
