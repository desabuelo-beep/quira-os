---
name: "ALERTA — D3 Ejecución Presupuestaria Crítica (59.85%)"
description: "Nota ALERTA QUIRA: D3=59.85% — categoría En riesgo según Tabla 200 PDOT. Cada punto = ~$144K no ejecutado. +10pp D3 → TGI 68.82→71.32."
tipo: alerta-tgi
prioridad: ALTA
dimension: "D3 Ejecución"
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
origen_dato: "Motor TGI Territorial — D3 Ejecución Presupuestaria"
fecha: "2026-05-16"
tags: [alerta, d3, ejecucion, presupuesto, tgi, copfp, poa, institucional]
---

# ALERTA — D3 Ejecución Presupuestaria Crítica (59.85%)

> **DIMENSIÓN CON MAYOR BRECHA TGI.** D3 = 59.85% — categoría "En riesgo" según la Tabla 200 del propio PDOT. La sub-ejecución bloquea el cierre de la brecha rural aunque el presupuesto exista en papel.

---

## Indicadores de Alarma

| Dimensión | Valor actual | Umbral óptimo | Brecha | Categoría |
|-----------|-------------|--------------|--------|-----------|
| D3 Ejecución | **59.85%** | ≥ 75% | **−15.15pp** | **EN RIESGO** |
| D2 Planificación | 69.93% | ≥ 75% | −5.07pp | Media |
| TGI Cantonal | **68.82** | ≥ 75 | −6.18pp | Bajo |

**Escala Tabla 200 PDOT:**
- ≥ 75% → Óptimo
- 50-74% → **En riesgo** ← D3 está aquí
- < 50% → Crítico

**Validación Gold Master:** V-18 — `D3=59.85% < 75% → ALERTA D3 EJECUCIÓN`

---

## Impacto Cuantificado

- **Cada punto porcentual de D3** = ~$144,000 USD no ejecutados en el cantón
- **Brecha D3 actual** (−15.15pp) = ~$2,182,000 USD dejados de ejecutar
- **La brecha rural de $1,791,935 no puede cerrarse si D3 permanece en 59.85%** — el presupuesto existe pero no llega al territorio
- **Efecto TGI:** +10pp en D3 → TGI cantonal sube de **68.82 a 71.32** (cruza umbral "Transición")

---

## Causas Diagnósticas (PDOT Modelo Gestión)

Según el PDOT y el análisis QUIRA, las causas típicas de D3 bajo son:

| Causa | Evidencia en Montecristi |
|-------|--------------------------|
| Coherencia POA-PDOT insuficiente | D2=69.93% — planificación media → POA puede estar desalineado |
| Capacidad técnica de unidades ejecutoras | PROG-PI-01 apunta a esta brecha |
| Procesos de contratación pública lentos | Ciclo SERCOP → retrasos en ejecución física |
| Proyectos sin financiamiento comprometido | Isabel Muentes sin proyecto activo Fase 4 |
| M&E semestral no activado | Art. 29 CPFP → Consejo Planificación debe verificar |

---

## Acciones Recomendadas QUIRA

```
NORMATIVO (Art. 29 CPFP):
  1. Activar Consejo de Planificación para revisión semestral POA-PDOT
  2. Verificar coherencia de todas las partidas presupuestarias con metas PDOT
  3. Documentar desviaciones y emitir resolución correctiva

OPERATIVO:
  4. Revisar cronograma de contrataciones — identificar cuellos de botella SERCOP
  5. Priorizar contratos parroquias rurales críticas (IET < 50)
  6. Implementar tablero D3 en tiempo real (SIAP-ICPI → dashboard alcaldía)

META:
  D3 ≥ 70% al cierre 2026 → TGI cantonal ≥ 70 (zona Básico consolidado)
  D3 ≥ 75% al cierre 2027 → TGI cantonal ≥ 71.5 (zona Transición)
```

---

## Vinculación QUIRA

- **Dimensión:** [[02_TGI_DIMENSIONES]] → D3 Ejecución
- **Indicadores fuente:** [[04_TGI_INDICADORES]] → D3=59.85%
- **Programas respuesta:** [[PROG-PI-01_Fortalecimiento_Institucional]] · [[PROG-PI-02_Posicionamiento_Difusion]]
- **Eje TGI:** [[EJE-PI_Institucional_Ejecucion]]
- **Marco legal:** [[CPFP-Sistema-Planificacion-Participativa]] Art.29 · [[CPFP-PDyOT-GADs-Montecristi]] Art.49
- **Modelo gestión:** [[MG-03_Responsabilidades_Herramientas]] · [[MG-05_Seguimiento_Evaluacion]]
- **Fondos cooperación técnica:** [[USAID-Gobernanza-Inclusion]] · [[GIZ-Cooperacion-Alemana]]
- **Datos fuente:** [[03_SIAP_ICPI_METHOD]]

**Módulo EJECUCIÓN — Contexto:**
- [[_Índice_Ejecucion]] — Índice CAPA EJECUCIÓN · 4 entes Holding
- [[FUENTES_Holding_Operativa]] — Registro documentos oficiales POA/PAC/eSIGEF
- [[PAC_2026_Contexto]] — Contratación como palanca D3 · USD 144K por pp
- [[POA_2026_Contexto]] — ICPI=69.93% · fricción narrativa 30 pp

---

*Alerta generada por QUIRA Gov desde SIAP-ICPI_GOLD_MASTER_v5.4 — 2026-05-16*
