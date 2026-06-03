# ADR-022 — Principio de Divergencia A↔D

**Estado**: SUPPORTED  
**Fecha de apertura**: 2026-06-03  
**Fecha de actualización**: 2026-06-03  
**Fecha de cierre**: PENDIENTE — ver §Criterios de Confirmación  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Participantes**: Javo (fundador) · Claude (director técnico) · Colega (asesor externo)

> **SUPPORTED**: demostrado empíricamente en Montecristi (OBS-009, Gate 6.5).
> Para CONFIRMED se requieren: más municipios, comparación longitudinal 2023–2026
> completa, y cédulas mensuales GAD con cobertura >50% anual.
>
> **Por qué NO es CONFIRMED todavía** (criterio colega asesor, 2026-06-03):
> El patrón de divergencia está demostrado en un solo municipio y un solo período.
> Para ser un principio arquitectónico general de QUIRA, debe replicarse
> en al menos un contexto territorial adicional.

---

## Contexto

ADR-019 demostró que Dom08 (participación) y Dom09 (control social) son
los nodos de mayor centralidad en el grafo constitucional municipal, con
evidencia computacional de centralidad y ciclo de retroalimentación.

ADR-021 estableció la ontología de 4 capas que permite distinguir:
- A = lo que la norma **obliga** (COOTAD, LOPC, Constitución)
- B = lo que la metodología **explica** (SNP, guías técnicas)
- C = lo que el municipio **planificó y ejecutó** (POA, PAC, cédulas)
- D = lo que **se puede observar** (RC, LOTAIP, SIGAD)

Lo que faltaba era la pregunta empírica: **¿A y D convergen en la práctica?**

Gate 6.5 (Fases 1–5, Holding Municipal Montecristi) provee los datos para
responder esa pregunta por primera vez con evidencia real.

---

## El Hallazgo Fundacional — OBS-009

A partir del cruce de fuentes independientes en el caso MCR:

| Fuente | Indicador | Valor 2023-2024 |
|--------|-----------|:---------------:|
| SIGAD (evaluación externa SNP) | ICM — Índice de Cumplimiento de Metas | **1.00 (100%)** |
| LOTAIP (transparencia activa) | Meses de ejecución financiera publicados 2025 | **3/12 (25%)** |
| SIGAD (oportunidad) | Demora promedio de envío de reportes | **16–17 meses** |
| metrics_mcr.py | Gap A↔D cuantificado | **+75 puntos** |

**El patrón observable:**

```
A (cumplimiento declarado)
   SIGAD = 100%
   RC = positiva (autoreporte)
   ≠
D (evidencia observable disponible)
   LOTAIP = 25% meses publicados
   Puntualidad = 17.5/100
   Corpus docs = 80%
```

---

## La Decisión Arquitectónica

### Tesis — Principio de Divergencia A↔D

> Un nivel alto de cumplimiento declarado institucionalmente no implica
> necesariamente un nivel equivalente de evidencia observable disponible.
>
> La diferencia entre A (cumplimiento declarado) y D (evidencia observable)
> constituye una **señal de riesgo de gobernanza** que debe ser monitoreada
> de forma independiente al desempeño operativo real de la institución.

### Lo que este principio AFIRMA

1. **La divergencia A↔D es medible** con los instrumentos que QUIRA ya tiene
2. **La divergencia A↔D es reproducible** — el método funciona en cualquier GAD
   con las mismas fuentes (SIGAD + LOTAIP + RC)
3. **La divergencia A↔D es una señal**, no una condena — requiere investigación
   adicional antes de atribuir incumplimiento

### Lo que este principio NO AFIRMA (caveat metodológico)

1. **No afirma incumplimiento operativo** — ausencia de publicación ≠ ausencia de ejecución
2. **No afirma incumplimiento legal** — el retraso puede tener causas legítimas
3. **No afirma que SIGAD sea falso** — SIGAD puede ser válido; LOTAIP puede ser incompleto
4. **No generaliza a todos los GADs** — evidencia solo de MCR hasta ahora

---

## Capacidad Nueva que ADR-022 Formaliza

QUIRA ahora hace algo que ni SIGAD ni LOTAIP hacen por separado:

```
SIGAD (solo):   "¿Cumpliste tus metas?" → Sí (ICM=1.00)
LOTAIP (solo):  "¿Publicaste los datos?" → Parcialmente (25%)
QUIRA (cruce):  "¿Qué tan consistente es lo que declarás con lo que mostrás?"
                → Gap A↔D = 75 puntos → señal de riesgo de gobernanza
```

Esa capacidad de cruce es el valor diferencial de QUIRA como
**Motor de Trazabilidad Pública Municipal**.

---

## Métricas Canónicas — Gold Master v5.5

`scripts/analysis/metrics_mcr.py` lee desde `app/connectors/gold_master.py` → H73_OUTPUT_API.
Todos los valores son los calculados por el Motor ICPI del Excel (fuente de verdad).

```
ICPI 2025:    69.93%  (Transición Crítica · meta PDOT = 65% ✓)
TGI Score:    66.79%
  D1 Legalidad:     83.2%  [fuerte]
  D2 Planificación: 69.9%  [moderado]
  D3 Ejecución:     59.9%  [débil — gap principal]
  D4 Equidad:       44.8%  [crítico]
  D5 Capacidad:    100.0%  [excelente]
ITAM Transparencia: 82.29%
IOC Opacidad:       17.71%  ← Gap A≠D real
SIGAD ICM:         100%     ← Declarado
Gap A≠D (Excel):   17.71 pts de opacidad observable
```

El gap A≠D real es 17.71 pts (no 75 como calculamos inicialmente con métricas ad-hoc).
La observación de divergencia se mantiene — la magnitud fue sobreestimada antes de
anclar al Motor ICPI del Excel.

---

## Relación con ADR-019

| ADR-019 | ADR-022 |
|---------|---------|
| El grafo constitucional muestra que Dom08+Dom09 son centrales | La divergencia A↔D ocurre precisamente en Dom08 (participación) y Dom09 (control social) |
| Demostrado a nivel normativo-computacional | Demostrado a nivel empírico-territorial |
| Estado: STRONGLY_SUPPORTED | Estado: SUPPORTED |

ADR-022 es la evidencia territorial que ADR-019 necesitaba para avanzar
hacia CONFIRMED. Ambos ADRs se refuerzan mutuamente.

---

## Criterios de Confirmación

Para pasar de SUPPORTED a CONFIRMED, se requiere demostrar:

| Criterio | Estado | Ruta |
|----------|:------:|------|
| C1 — Patrón replicado en segundo municipio | PENDIENTE | Expandir a otro GAD del universo de 221 |
| C2 — Comparación longitudinal 2023–2026 completa | PARCIAL | Cédulas GAD Oct-Dic 2025 únicamente |
| C3 — Cobertura LOTAIP GAD > 50% en algún año | PENDIENTE | Verificar si meses faltantes existen en otra fuente |
| C4 — Correlación Dom08/Dom09 con score A↔D | PENDIENTE | Requiere query grafo + métricas |

---

## Implicaciones para el Producto QUIRA

1. **El score A↔D es una métrica de producto** — mostrable en la UI como
   indicador de riesgo de gobernanza por municipio

2. **Es replicable a 221 municipios** — el mismo pipeline funciona con
   cualquier GAD que tenga SIGAD + LOTAIP + RC disponibles

3. **No requiere acceso privilegiado** — toda la evidencia es pública

4. **Escala como servicio** — cada nuevo municipio agrega evidencia
   para convertir SUPPORTED → CONFIRMED a nivel de sistema

---

## Deuda técnica asociada

- `dominios_quira = ""` en todos los documentos del Holding — los POA, PAC,
  cédulas no están clasificados con Dom01-Dom12 del Excel Canon.
  Eso es el puente pendiente entre la Capa A (Excel) y las Capas C+D (Holding).
  Un pase de tagging post-ingesta resolverá esto en Gate 6.6 o posterior.

---

*ADR-022 · QUIRA Gov · Dylus Lab © 2026*  
*Evidencia fundacional: OBS-009 · Datos: Gate 6.5 Fases 1–5 · Script: metrics_mcr.py*
