---
name: "ALERTA — Holding Municipal Ti Inversión Crítica Q1-2026"
description: "Alerta QUIRA: Todo el Holding Municipal de Montecristi (4 entidades) registra Ti inversión < 15% en Q1-2026. Patronato lidera con 9.71%; Bomberos sin ejecución (0%). Datos Sentinel Sprint 2.5B desde Supabase PostgreSQL."
tipo: alerta-tgi
prioridad: CRITICA
dimension: "D3 Ejecución"
scope: "Holding Municipal — 4 Entidades"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.5"
sentinel_sprint: "2.5B"
origen_dato: "Supabase PostgreSQL — monthly_kpis — Sentinel Sprint 2.5B"
fecha: "2026-05-18"
tags: [alerta, ti-inversion, holding, gad, bomberos, emai-ep, patronato, 2026, d3, critico, semaforo-rojo, sentinel]
---

# ALERTA — Holding Municipal Ti Inversión Crítica Q1-2026

> **LAS 4 ENTIDADES DEL HOLDING ESTÁN EN SEMÁFORO ROJO.** Ti Inversión < 15% en todos los entes al corte de marzo 2026. La inversión pública del cantón Montecristi está en zona crítica. Umbral zona verde: ≥ 35%.

→ [[CEDULAS_HOLDING_ENE_MAR_2026]] · [[ALERTA-D3_Ejecucion_Critica]] · [[_Índice_Ejecucion]]

---

## Estado Ti Inversión — Corte Marzo 2026

| Entidad | Ti Inversión | Vs. Umbral Verde (35%) | Clasificación | Urgencia |
|---------|-------------|----------------------|--------------|---------|
| **GAD Municipal** | **0.81%** | −34.19 pp | 🔴 CRÍTICO | MÁXIMA |
| **Cuerpo de Bomberos** | **0.00%** | −35.00 pp | 🔴 CRÍTICO | MÁXIMA |
| **EMAI-EP** | **1.65%** | −33.35 pp | 🔴 CRÍTICO | MÁXIMA |
| **Patronato** | **9.71%** | −25.29 pp | 🔴 CRÍTICO | ALTA |

**Umbrales:** 🔴 < 15% · 🟡 15–35% · 🟢 ≥ 35%

---

## Serie Temporal Q1-2026 — Trayectorias

| Entidad | Enero | Febrero | Marzo | Tendencia |
|---------|-------|---------|-------|----------|
| GAD Municipal | 0.60% | — | 0.81% | ↗ Mejorando, ritmo lento |
| Bomberos | 0.00% | 0.00% | 0.00% | → Sin inicio de inversión |
| EMAI-EP | 0.00% | 0.97% | 1.65% | ↗ Activando desde Feb |
| Patronato | 2.83% | 6.92% | 9.71% | ↗↗ Mejor ritmo del holding |

> **Señal positiva:** 3 de 4 entidades muestran trayectoria creciente. Bomberos es el único en $0 devengado inversión durante todo el Q1.

---

## Impacto en D3 TGI

- **D3 Ejecución Presupuestaria (holding GAD)** = 59.85% → alerta preexistente: [[ALERTA-D3_Ejecucion_Critica]]
- La Ti inversión baja agrava D3: si los grupos 7+8 no avanzan, el codificado no se devenga
- **Riesgo fiscal 2026:** Entes con Ti=0% o Ti<2% corren riesgo de sub-ejecución anual y pérdida de asignación futura
- **Patronato como referente:** su modelo de ejecución en grupos 7+8 es replicable en Bomberos y EMAI-EP

---

## Análisis por Entidad

### GAD Municipal
- Cod. Inv. creció de $26.6M (Ene) a $30.2M (Mar) — partidas adicionales comprometidas
- Dev. Inv. solo $243,514 sobre $30.2M = 0.81% → brecha crítica entre comprometido y ejecutado
- Causa probable: contratos en proceso (SIE-SERCOP) sin desembolso al corte del período

### Cuerpo de Bomberos
- Cod. Inv. = $216,502 (grupos 84.xx) estable en los 3 meses
- Dev. Inv. = $0 en Enero, Febrero y Marzo — todo el Q1 sin inversión
- **Alerta máxima:** verificar si los contratos de bienes de capital existen en el portal SERCOP
- Si no existen: emitir procesos de contratación urgentes antes de Q2

### EMAI-EP
- Inversión iniciando en Febrero ($1,491) y Marzo ($2,552) — montos pequeños pero señal positiva
- Ti proyectada: si mantiene ritmo de aceleración, alcanza ~3-5% al cierre Q2

### Patronato Municipal
- Mejor ejecutor del holding: 9.71% al cierre de marzo
- Inversiones activas desde Enero con crecimiento sostenido y acelerado
- Proyección optimista: Ti ≈ 18–25% al cierre Q2 si mantiene ritmo

---

## Acciones Correctivas Recomendadas

```
INMEDIATO (Mayo-Junio 2026):
  1. BOMBEROS: verificar contratos grupos 84.xx en SERCOP
     → Si no existen: generar procesos de contratación urgentes
  2. GAD: mapear los $30.2M en grupos 7+8 → qué contratos están pendientes de desembolso
  3. EMAI-EP: acelerar desembolsos existentes en grupos 84.xx

ESTRATÉGICO (Q2-Q3 2026):
  4. Replicar modelo Patronato (inversión activa desde mes 1) en demás entidades
  5. Activar tablero Ti-inversión en QUIRA OS para monitoreo semanal del holding
  6. Meta intermedia: Ti ≥ 15% para todas las entidades al cierre Q2-2026

META ANUAL 2026:
  Ti ≥ 35% todo el holding → Zona verde D3
  (requiere Dev. Inv. ≥ $22.3M sobre ~$63.9M codificado holding)
```

---

## Vinculación QUIRA

- **Datos fuente:** [[CEDULAS_HOLDING_ENE_MAR_2026]] — serie mensual eSIGEF Q1-2026
- **Alerta D3 macro:** [[ALERTA-D3_Ejecucion_Critica]] — D3=59.85% GAD
- **Fuentes documentales:** [[FUENTES_Holding_Operativa]] — cédulas eSIGEF oficiales
- **Índice ejecución:** [[_Índice_Ejecucion]] — módulo 08
- **Dimensión TGI:** [[02_TGI_DIMENSIONES]] → D3 Ejecución Presupuestaria
- **Método Ti:** [[03_SIAP_ICPI_METHOD]] → Ti inversión = grupos 7+8 / codificado
- **Excel:** Hoja `H_HOLDING_CEDULAS_2026` — SIAP-ICPI_GOLD_MASTER_v5.5
- **Supabase:** tabla `monthly_kpis` — entidad field — Sprint 2.5B — 2026-05-18

---

*Alerta generada por Sentinel Sprint 2.5B desde Supabase PostgreSQL · QUIRA Gov · 2026-05-18*
