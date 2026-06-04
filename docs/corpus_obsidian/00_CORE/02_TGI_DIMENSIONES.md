---
name: "TGI Dimensiones — D1 a D5"
description: "Definición canónica de las 5 dimensiones TGI con fórmulas, fuentes Excel y umbrales"
tipo: meta-dimensiones
version: "v5.4"
fecha: "2026-05-16"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
tags: [tgi, dimensiones, d1, d2, d3, d4, d5, formulas, core]
---

	# TGI — Las 5 Dimensiones
	
> 	**TGI Score = D1×0.20 + D2×0.20 + D3×0.25 + D4×0.25 + D5×0.10**
>	
> 	Fuente canónica: SIAP-ICPI_GOLD_MASTER_v5.4 · Motor TGI Framework · Motor TGI Territorial
	
	Vincula → [[01_TGI_FRAMEWORK]] · [[03_SIAP_ICPI_METHOD]] · [[04_TGI_INDICADORES]]
	
	---
	
	## D1 — Legalidad y Coherencia Normativa (20%)
	
	| Campo | Valor |
	|-------|-------|
	| Peso | 20% |
	| Fuente Motor TGI | Trust Score institucional |
	| Valor GADM Montecristi | 83.50% |
	| Estado | OK |
	
	**Qué mide:** Grado en que el GAD opera dentro del marco normativo vigente: coherencia entre PDOT, POA, PAC, LOTAIP, COOTAD/COPFP.
	
	**Norma habilitante:** Art. 215-228 COOTAD — obligaciones de planificación y transparencia de los GAD municipales.
	
	**Componentes verificables:**
	- Existencia y aprobación del PDOT vigente
	- Coherencia PDOT–POA–PAC
	- Cumplimiento LOTAIP (publicación indicadores)
	- Resoluciones del Consejo Municipal alineadas al PDOT
	
	---
	
	## D2 — Fidelidad a la Planificación (20%)
	
	| Campo | Valor |
	|-------|-------|
	| Peso | 20% |
	| Celda Gold Master | H01!B15×100 |
	| Valor GADM Montecristi | 69.93% |
	| Estado | Alerta moderada |
	
	**Qué mide:** Porcentaje de metas del PDOT/POA efectivamente cumplidas en el período evaluado. Mide la brecha entre lo planificado y lo ejecutado en términos de outputs.
	
	**Norma habilitante:** Art. 41-44 COPFP — obligatoriedad del seguimiento y evaluación del plan.
	
	**Alerta GADM Montecristi:** 69.93% indica que aproximadamente 30% de las metas planificadas no se ejecutaron. Riesgo de incumplimiento del Plan Bicentenario 2023-2027.
	
	---
	
	## D3 — Ejecución Presupuestaria (25%)
	
	| Campo | Valor |
	|-------|-------|
	| Peso | 25% (mayor peso individual junto a D4) |
	| Celda Gold Master | H07b!B18×100 |
	| Valor GADM Montecristi | 59.85% |
	| Estado | ALERTA — por debajo del umbral óptimo (75%) |
	
	**Qué mide:** Porcentaje del presupuesto devengado respecto al codificado en el período. Indicador de eficiencia de gasto público.
	
	**Norma habilitante:** Art. 215-220 COOTAD — ciclo presupuestario y ejecución. Art. 113 COPFP — evaluación de la ejecución presupuestaria.
	
	**Alerta crítica:** 59.85% es preocupante. El umbral óptimo para GAD municipales ecuatorianos es ≥75%. Implica que más de 40% del presupuesto no se ejecutó, generando devoluciones y subejecución que afectan la calidad del servicio.
	
	**Impacto en TGI:** D3 tiene el mismo peso que D4 (25% c/u). Una mejora de 10pp en D3 (de 59.85 a 69.85) elevaría el TGI cantonal de 68.82 a 71.32.
	
	---
	
	## D4 — Equidad Territorial (25%) ★
	
	| Campo | Valor |
	|-------|-------|
	| Peso | 25% (mayor peso individual junto a D3) |
	| Celda Gold Master | H99!J7:J13 |
	| Fórmula | D4 = MIN(100, IET_Local) |
	| Valor | Variable por parroquia (28.57 a 100.0) |
	| Estado | CRITICO — 4 de 6 parroquias rurales en déficit |
	
	**Qué mide:** Equidad en la distribución territorial de la inversión pública. Es el único indicador que DIFERENCIA por parroquia.
	
	**Fórmula IET:** `IET_Local = (InvPerCap_Local / InvPerCap_Cantonal) × 100`
	
	**Norma habilitante:** Art. 249 CRE — garantía de servicios básicos. Art. 3 COOTAD — principio de equidad territorial.
	
	**Clasificación de equidad:**
	
	| IET Local | Clasificación | Parroquias Montecristi |
	|-----------|--------------|----------------------|
	| ≥ 100 | Sobre la media | Montecristi (193.75) |
	| ≥ 70 | Media | General Alfaro (63.39) |
	| ≥ 50 | Alta | Aníbal San Andrés (51.79) |
	| < 50 | Crítica | La Pila, Leónidas Proaño, Isabel Muentes, Colorado |
	
	**Brecha territorial:** $1,791,935 USD acumulados en 6 parroquias rurales. IRS_Global = 79.7 (inversión concentrada en Montecristi urbana).
	
	---
	
	## D5 — Capacidad Institucional (10%)
	
	| Campo | Valor |
	|-------|-------|
	| Peso | 10% (menor peso — considerado umbral mínimo) |
	| Celda Gold Master | H01!B12×100 |
	| Valor GADM Montecristi | 100.00% |
	| Estado | OK |
	
	**Qué mide:** Capacidad operativa, técnica y administrativa del GAD para gestionar sus competencias. Incluye: existencia de unidades técnicas, sistemas de información, capacidad de contratación.
	
	**Norma habilitante:** Art. 338 COOTAD — competencias y capacidades de los GAD municipales. ICO — Índice de Capacidad Operativa (SENPLADES/PLADES).
	
	**Nota metodológica:** El valor 100% para GADM Montecristi se debe a que la capacidad institucional base fue verificada como suficiente. La escala es binaria-gradual: GADs que no cumplen requisitos mínimos reciben penalización directa.
	
	---
	
	## Resumen Dimensional — GADM Montecristi 2026
	
	| Dimensión | Peso | Valor | Umbral Óptimo | Estado |
	|-----------|------|-------|---------------|--------|
	| D1 Legalidad | 20% | 83.50% | ≥ 80% | OK |
	| D2 Planificación | 20% | 69.93% | ≥ 75% | Alerta |
	| D3 Ejecución | 25% | 59.85% | ≥ 75% | Alerta critica |
	| D4 Equidad | 25% | variable | IET ≥ 70 | Critico rural |
	| D5 Capacidad | 10% | 100.00% | ≥ 80% | OK |
	| **TGI Cantonal** | **100%** | **68.82** | **≥ 75** | **Transición** |
	
	---
	
	**Fuente:** QUIRA Gov · Motor TGI Territorial
	**Auditoría:** Motor TGI QUIRA — Validaciones · Trazabilidad · Limitaciones declaradas
	**Fecha:** 2026-05-16
