---
name: "IED — Índice de Eficiencia Directiva"
description: "Métrica que cuantifica el cumplimiento del mandato por dirección municipal. Desagrega el ICPI Global al nivel de cada unidad administrativa. Base: LOSEP Art. 76-82."
tipo: meta-indice
version: "v5.5"
desarrollador: "Dylus Lab / QUIRA Gov"
gold_master: "Gold Master TGI v5.5"
fecha: "2026-05-25"
tags: [ied, eficiencia, directiva, losep, d5, capacidad, holding, core]
---

# IED — Índice de Eficiencia Directiva

> **El IED convierte el mandato municipal en responsabilidad individual medible.**
> Cada Director responde por su Ti. No hay "burocracia diluida".
> Origen conceptual: "Responsabilidad Orgánica Vinculante (Ci)" — IP Dylus Lab.

Vincula → [[02_TGI_DIMENSIONES]] D5 · [[05_SAT_SISTEMA]] SAT-V · [[08_MMP_MENSUAL]]

---

## Definición

El IED es la métrica derivada del ICPI Global que cuantifica el cumplimiento del mandato **bajo la responsabilidad directa de una unidad administrativa específica**.

Funciona como índice desagregado (micro) que permite la individualización de responsabilidades operativas mediante la triangulación de:
- **Competencia:** ¿Cuáles son las obligaciones legales de esta dirección?
- **Planificación:** ¿Qué prometió hacer en el POA?
- **Contratación:** ¿Qué comprometió vía SERCOP?
- **Ejecución:** ¿Qué recursos devengó efectivamente?

**Marco legal:** LOSEP Art. 76-82 — evaluación de desempeño del personal jerárquico superior.

---

## Las 11 Direcciones Municipales — GADM Montecristi

| # | Dirección | Ti Actual | Estado |
|---|-----------|-----------|--------|
| 01 | Dirección de Planificación | — | Pendiente ingesta |
| 02 | Dirección Financiera | — | Pendiente ingesta |
| 03 | Dirección de Obras Públicas | — | Pendiente ingesta |
| 04 | Dirección de Servicios Públicos | — | Pendiente ingesta |
| 05 | Dirección de Gestión Ambiental | — | Pendiente ingesta |
| 06 | Dirección de Desarrollo Social | — | Pendiente ingesta |
| 07 | Dirección de Participación Ciudadana | — | Pendiente ingesta |
| 08 | Dirección Jurídica | — | Pendiente ingesta |
| 09 | Dirección de TI y Comunicación | — | Pendiente ingesta |
| 10 | Unidad de Talento Humano | — | Pendiente ingesta |
| 11 | Secretaría General | — | Pendiente ingesta |

**IED Global actual:** 31.14% — calculado con datos disponibles v5.5

---

## Fórmula IED por Dirección

```
IED_Dirección = (Ti_Devengado / Ti_Codificado) × 100

Donde:
  Ti_Devengado = recursos ejecutados (grupos 7+8 GADM) en zona de responsabilidad
  Ti_Codificado = recursos asignados en el presupuesto codificado
```

**Ponderación Cruzada de Desempeño** (IP Dylus Lab):
- Ti financiero × cumplimiento de metas POA × evidencia SERCOP
- Distingue incumplimiento por restricción presupuestaria exógena vs. inacción directiva

---

## Flujo H07c — El Corazón del IED

```
1. Director recibe informe mensual de su dirección (POA + ejecución)
2. Director firma el informe (firma digital / física)
3. Técnico QUIRA sube informe al sistema (pantalla de ingesta)
4. Sistema genera SHA-256 del documento
5. SHA-256 activa Ti_V en Gold Master G3.3
6. Ti_V activado → IED de esa dirección actualizado
7. IED global recalculado → ICPI Global actualizado
```

**Sin SHA → Ti_V = 0 → esa dirección no cuenta en el composite**
Este es el mecanismo de "Responsabilidad Orgánica Vinculante" operacionalizado.

---

## Relación IED ↔ SAT-V

Si un Director **no entrega informe firmado** en el período:
- Ti_V = 0 para esa dirección
- IED de esa dirección = 0%
- Activa **SAT-V: Opacidad Directiva**
- Aparece en pantalla Alcalde con nivel AVEP 🔴

**El sistema no castiga — alerta. El Alcalde decide.**

---

## Holding Municipal — 4 Entidades

El IED también aplica a las entidades adscritas del Holding:

| Entidad | Tipo | Responsable |
|---------|------|-------------|
| GAD Central | Municipal | Alcalde / Direcciones |
| EMAI (EP Aseo) | Empresa Municipal | Gerente EP Aseo |
| Cuerpo de Bomberos | Adscrita | Jefe Bomberos |
| Patronato Municipal | Adscrita | Presidente Patronato |

Cada entidad tiene su Ti y contribuye al D3 Consolidado (Gold Master G3.5).

---

## Implementación Frontend — Ambiente Técnico

```
Pantalla: Ingesta Mensual por Dirección (11 pantallas + 4 entidades)
  ↓ Director sube informe firmado
  ↓ Sistema procesa SHA-256
  ↓ IED actualizado en tiempo real
  ↓ Dashboard IED visible para Alcalde (Ambiente Político)
```

**Tabla IED en quira_pages/m5_control.py** (tab a implementar)

---

## Origen Conceptual — IP Dylus Lab

El IED tiene su origen en:
- "Índice de Evaluación Directiva" — terminología fundacional QUIRA
- "Módulo F-EDS (Evaluación de Desempeño Basada en Congruencia)"
- "Responsabilidad Orgánica Vinculante (Ci)"

Estos conceptos evolucionaron al IED operativo con el marco TGI.

→ Ver historia completa en `data/doctrinal/historical/TERMINOLOGY_ORIGIN_v1.md` (quira-os)

---

**Fuente canónica:** Gold Master TGI v5.5 · G4.4_IED · G3.7_D5_CAPACIDAD
**Marco legal:** LOSEP Art. 76-82 · Resolución 040-2025 (Orgánico Estructural GADM)
**Fecha:** 2026-05-25
