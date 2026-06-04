---
name: "Motor TGI — Metodología QUIRA Gov"
description: "Metodología del motor cuantitativo TGI que alimenta el sistema 5D. Documenta lógica y outputs; la arquitectura interna es trade secret de Dylus Lab. Anteriormente llamado SIAP-ICPI — nombre histórico preservado en data/doctrinal/historical/."
tipo: meta-metodologia
version: "Gold Master TGI v5.5"
quira_motor: "Motor TGI"
fecha: "2026-05-25"
tags: [motor-tgi, icpi, quira, tgi, motor, metodologia, core, gold-master]
---

# Motor TGI — Metodología QUIRA Gov

> **Nota histórica:** Este motor fue denominado "SIAP-ICPI" en versiones anteriores (v5.0-v5.4). El nombre canónico desde v5.5 es "Motor TGI" / "Gold Master TGI". El nombre histórico está preservado en `data/doctrinal/historical/TERMINOLOGY_ORIGIN_v1.md` como registro de IP fundacional.

> **El QUIRA Engine es la única fuente de verdad cuantitativa del sistema.**
> Todo dato que aparece en Obsidian, reportes o Sentinel proviene de este motor.
> Ningún valor TGI se estima — todo tiene fuente documental verificable.

Vincula → [[00_QUIRA_GOV]] · [[01_TGI_FRAMEWORK]] · [[02_TGI_DIMENSIONES]] · [[04_TGI_INDICADORES]]

---

## Identificación del Motor

| Campo | Valor |
|-------|-------|
| Nombre comercial | QUIRA Gov · TGI Engine |
| Motor subyacente | SIAP-ICPI Gold Master v5.4 |
| Caso piloto activo | GADM Montecristi 2023-2027 |
| Fecha de corte | 2026-05-16 |
| Entidades analizadas | 4 (GAD central + 3 adscritas) |
| Parroquias analizadas | 7 (1 urbana + 6 rurales) |

**Regla de oro:** El motor es la fuente canónica. Obsidian consume sus outputs; nunca los sobreescribe. La arquitectura interna del motor es propiedad intelectual de Dylus Lab y no se expone en este vault.

---

## Capas del Motor QUIRA

| Capa | Función | Outputs hacia Obsidian |
|------|---------|------------------------|
| **Silos de Datos** | Ingesta de fuentes oficiales: CNE, PDOT, eSIGEF, SIGAD, SERCOP, CPCCS | Valores brutos verificados |
| **Motor ICPI** | Calcula el D2_Score de Planificación (25 metas PDOT × ciclos anuales) | D2_Score = 69.93% → D2 ⚠️ NO confundir con ICPI Global (53.56%) |
| **Motor Financiero** | Analiza ejecución presupuestaria grupos 7+8 de los 4 entes municipales | Ti = 59.85% → D3 |
| **Motor Territorial** | Calcula IET, IRS, Composite Need y TGI por parroquia | IRS=79.7 · TGI≈66.85 → D4 |
| **Motor TGI 5D** | Integra las 5 dimensiones en el Score cantonal final | TGI_Score → [[02_TGI_DIMENSIONES]] |

---

## Variables del Análisis Territorial

> Estas son las variables que produce el motor y aparecen en el vault. No se expone cómo se calculan internamente — solo qué significan y cuál es su valor actual.

| Variable | Significado | Valor actual (2026) | Dimensión TGI |
|---------|-------------|---------------------|---------------|
| **IRS_Global** | Índice de Regresividad Espacial: correlación negativa entre NBI e inversión per cápita | **79.7** — Muy Regresivo | D4 |
| **D3_Ti** | Tasa de inversión ejecutada (devengado/codificado) en obra pública | **59.85%** — Crítico | D3 |
| **TGI_Score** | Score cantonal ponderado 5 dimensiones | **≈ 66.85** — 🟡 Transición | D1-D5 |
| **NBI_Rural_Prom** | NBI promedio de las 6 parroquias rurales | **55.7%** | D4 |
| **Composite_Need** | Índice necesidad compuesta: NBI + Agua_gap + participación poblacional | **Líder: Isabel Muentes** | D4 |
| **IET_Local** | Inversión per cápita local vs media cantonal (índice 0-200) | **Mín: ≈44.8** | D4 |
| **Brecha_USD** | Fondos no llegados al territorio por regresividad | **≈ 1.79 M USD** | D4 |
| **ICPI_Global** | Índice Compuesto de Progreso Institucional (D1+D2+D3+D4+D5) | **53.56%** | D1-D5 |
| **D2_Score** | Fidelidad a la Planificación (antes erróneamente = ICPI_Global) | **69.93%** | D2 |
| **Trust_Score** | Calidad metodológica del proceso normativo institucional | **83.5%** | D1 |
| **ICM_SNP** | Cumplimiento de reporte al Sistema Nacional de Planificación | **100%** | D5 |

---

## Fórmulas Metodológicas TGI

> Las fórmulas se expresan en notación matemática. La implementación técnica es interna al motor.

**TGI Score 5 Dimensiones:**
```
TGI = D1×0.20 + D2×0.20 + D3×0.25 + D4×0.25 + D5×0.10
```

**Índice de Equidad Territorial (IET):**
```
IET_Local = (InvPerCap_Parroquia / InvPerCap_Cantonal_Promedio) × 100
```

**Índice de Regresividad Espacial (IRS):**
```
IRS = –CORREL(NBI%, InvPerCap) × 100
```
> IRS > 0 → inversión regresiva (va más a zonas con menos necesidad).
> IRS = 79.7 → correlación negativa fuerte — inversión concentrada en cabecera.

**Composite Need (CN) v2.1:**
```
CN = 0.30 × (NBI/100) + 0.50 × (1 – Agua/100) + 0.20 × (Pob_Parroquia / Pob_Total)
```

**Brecha de Reequilibrio:**
```
Brecha_USD = Población × (InvPerCap_Cantonal – InvPerCap_Local)
```
> Brecha positiva → la parroquia debería haber recibido más inversión.

**Prioridad de Reequilibrio:**
```
Prioridad = 0.40 × NBI% + 0.30 × (1 – Agua%) + 0.30 × (1 – TGI_Score%)
```

---

## Flujo de Información — Excel → QUIRA → Obsidian

```
Fuentes oficiales (CNE · PDOT · eSIGEF · SIGAD · SERCOP · CPCCS)
    ↓
QUIRA Engine — Motor cuantitativo (propietario Dylus Lab)
    ↓
OUTPUTS verificados
    ├── [[02_TGI_DIMENSIONES]] — Score y clasificación cantonal
    ├── [[04_TGI_INDICADORES]] — Variables por dimensión
    ├── [[ALERTA-D3_Ejecucion_Critica]] — Ti=59.85%
    ├── [[ALERTA-Regresividad_IRS79]] — IRS=79.7
    ├── [[ALERTA-Isabel_Muentes]] — CN líder
    ├── [[ALERTA-Brecha_Rural_1.79M]] — Brecha USD
    └── [[07_TGI_Parroquias/TGI_Cantonal]] — TGI por parroquia
```

> **Contrato de integridad:** Obsidian consume OUTPUTS. Nunca arquitectura interna, nombres de componentes técnicos ni estructuras del motor.

---

## Progresión de Versiones

| Versión | Fecha | Cambio principal |
|---------|-------|-----------------|
| v5.0 | 2026-05 | Base TGI 3D inicial |
| v5.1 | 2026-05 | Agrega D4 Equidad territorial |
| v5.2 | 2026-05 | IRS Global + alertas cantonales |
| v5.3 | 2026-05-16 | TGI 5D completo, 7 parroquias |
| **v5.4** | **2026-05-16** | **Brecha USD · Prioridad Reequil · Clasif Equidad** |

---

## Regla de Actualización

1. El motor es la fuente — Obsidian nunca crea datos, solo los refleja
2. Toda actualización de datos requiere nueva versión del motor con trazabilidad
3. Los outputs validados se propagan desde el motor hacia este vault
4. La versión anterior del motor se archiva — nunca se elimina
5. En caso de discrepancia entre Obsidian y el motor: **el motor prevalece**

---

**Motor:** QUIRA Gov · TGI Engine · SIAP-ICPI Gold Master v5.4
**Propietario:** Dylus Lab © 2026
**Fecha:** 2026-05-17

*Nota: La arquitectura interna del motor (componentes, estructuras de cálculo, implementación) es trade secret de Dylus Lab. Este documento solo documenta metodología y outputs.*
