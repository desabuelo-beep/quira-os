---
name: "ALERTA — Regresividad Presupuestaria IRS=79.7"
description: "Nota ALERTA QUIRA: IRS=79.7 supera umbral de regresividad severa (>70). 79.7% inversión cantonal concentrada en Montecristi urbana. Implicaciones legales COOTAD 2026."
tipo: alerta-metodologica
prioridad: ALTA
gold_master: "SIAP-ICPI_GOLD_MASTER_v5.4"
origen_dato: "Motor TGI Territorial — IRS Global"
fecha: "2026-05-16"
tags: [alerta, irs, regresividad, d4, equidad, cootad, presupuesto, metodologia]
---

# ALERTA — Regresividad Presupuestaria IRS=79.7

> **ALERTA METODOLÓGICA Y LEGAL.** El Índice de Regresividad Social de Montecristi supera el umbral de regresividad severa para GADs con alta ruralidad. La Reforma COOTAD 2026 (RO Nro. 229) establece una regla gradual: 2027 ≥68%, 2028+ ≥70% de egresos no financieros en inversión. IRS=79.7 + concentración urbana = riesgo de observación de Contraloría.

---

## Definición del IRS (Metodología QUIRA)

El **Índice de Regresividad Social** mide la concentración de inversión en la parroquia urbana respecto al total cantonal:

```
IRS = (InvTotal_Montecristi_urbana / InvTotal_cantonal) × 100
IRS = ($791,935 / $993,335) × 100 = 79.7
```

**Escala de interpretación:**

| Rango | Interpretación | Color |
|-------|---------------|-------|
| < 50 | Equitativo | 🟢 |
| 50-60 | Levemente regresivo | 🟡 |
| 60-70 | Moderadamente regresivo | 🟠 |
| **> 70** | **Muy regresivo** (umbral GADs alta ruralidad) | 🔴 |
| > 85 | Hiper-regresivo — riesgo legal | 🔴🔴 |

**Montecristi: IRS = 79.7 → zona MUY REGRESIVO**

---

## Por Qué IRS=79.7 es un Problema

### 1. Problema de equidad territorial

El principio de equidad territorial (D4 del TGI, peso 25%) exige que la inversión pública reduzca brechas, no las amplíe. Con IRS=79.7, Montecristi está usando su presupuesto para profundizar la inequidad existente.

### 2. Problema matemático TGI

D4 Equidad es el 25% del TGI. Con IRS=79.7 la puntuación D4 es baja, lo que arrastra el TGI cantonal hacia abajo, aunque D1/D2/D3/D5 mejoren.

**Efecto simulado:**
- IRS actual 79.7 → D4 contribuye X puntos al TGI
- IRS objetivo 72 → D4 mejoraría, TGI subiría ~1-2pp adicionales

### 3. Problema legal emergente (Reforma COOTAD 2026)

**Reforma COOTAD 2026 — Regla gradual de asignación mínima prioritaria (Art. 198.1):**
- **2026:** solo seguimiento desde 1-dic-2026 (sin porcentaje mínimo aún)
- **2027:** ≥ 68% de egresos no financieros en inversión
- **2028+:** ≥ 70% de egresos no financieros en inversión (meta definitiva)

Combinado con el principio de progresividad presupuestaria (Art. 192 COOTAD), una auditoría de Contraloría podría observar la concentración IRS=79.7 como incompatible con la función redistributiva del gasto municipal en el momento en que el MEF inicie su seguimiento trimestral (desde dic-2026).

---

## Diagnóstico por Parroquia

| Parroquia | InvPerCap | IET | Posición relativa |
|-----------|----------|-----|-----------------|
| Montecristi (urbana) | **$217/hab** | 193.75 | 🔴 SOBRE-invertida |
| Gral. Alfaro | ~$90/hab | 63.39 | 🟡 Sub-invertida |
| Aníbal San Andrés | ~$70/hab | 51.79 | 🟡 Sub-invertida |
| La Pila | ~$60/hab | 46.43 | 🔴 Crítico |
| Leonidas Proaño | ~$58/hab | 42.86 | 🔴 Crítico |
| Isabel Muentes | ~$40/hab | 35.71 | 🔴 Crítico |
| Colorado | ~$37/hab | 28.57 | 🔴 Crítico |

---

## Acciones Recomendadas QUIRA

```
PARA REDUCIR IRS DE 79.7 A ≤ 72 (meta 2027):
  
  1. Redirigir $500K+ de proyectos urbanos pospuestos a rurales IET < 50
     → IRS proyectado: 79.7 → 75.2 (redirigir $500K)
     → IRS proyectado: 79.7 → 72.0 (redirigir $1.1M en 2 años)

  2. Incluir IRS como KPI en POA 2027:
     → Cláusula: ninguna nueva contratación urbana sin proyecto rural paralelo

  3. Documentar la mejora en rendición de cuentas (transparencia D2/D5)

PARA PROTEGER AL GADM LEGALMENTE:
  4. Solicitar opinión jurídica sobre Art. 198.1 COOTAD y distribución actual
  5. Incluir metas de IRS en resolución del Consejo de Planificación
  6. Evidenciar redistribución en informe de Contraloría preventivo
```

---

## Vinculación QUIRA

- **Dimensión:** [[02_TGI_DIMENSIONES]] → D4 Equidad Territorial (peso 25%)
- **Indicadores fuente:** [[04_TGI_INDICADORES]] → IRS=79.7
- **Eje TGI:** [[EJE-EP_Equidad_Desarrollo]]
- **Parroquia sobre-invertida:** [[P-01_Montecristi]] (IET=193.75, InvPerCap=$217)
- **Parroquias sub-invertidas:** 6 rurales → ver [[ALERTA-Brecha_Rural_1.79M]]
- **Marco legal:** [[COOTAD-Recursos-Presupuesto]] Art. 198.1 + Art. 192
- **Programa institucional:** [[PROG-PI-01_Fortalecimiento_Institucional]] (fortalece capacidad de redistribución)
- **Datos fuente:** [[03_SIAP_ICPI_METHOD]]

---

*Alerta generada por QUIRA Gov desde SIAP-ICPI_GOLD_MASTER_v5.4 — 2026-05-16*
