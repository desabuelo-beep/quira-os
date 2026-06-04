---
name: "QUIRA Gov — Identidad y Arquitectura"
description: "Nota madre del sistema QUIRA Gov — identidad, arquitectura, módulos y jerarquía conceptual"
tipo: meta-sistema
version: "1.1"
desarrollador: "Dylus Lab"
fecha: "2026-05-25"
gold_master: "Gold Master TGI v5.5"
pmv: "quira-os (Streamlit · Python · Supabase)"
tags: [quira, meta, core, arquitectura]
---

# QUIRA Gov

> **Dylus Lab desarrolló QUIRA Gov**, una infraestructura de inteligencia pública territorial, y **TGI (Territorial Governance Intelligence)**, el framework metodológico que articula normativa, planificación, ejecución presupuestaria y realidad territorial para apoyar la toma de decisiones basada en evidencia.

---

## Jerarquía Canónica — 6 Capas

```
CAPA 0 — Dylus Lab
              Gobernanza metodológica · IP · versiones · evolución

CAPA 1 — QUIRA OS  ◄──── (este nodo)
              Ecosistema operativo · módulos · flujos · entidades

CAPA 2 — TGI Framework
              Marco metodológico · D1–D5 · ciencia de evaluación

CAPA 3 — SIAP Engine  [privado]
              Motor Excel · fórmulas · scoring · alertas · calibraciones

CAPA 4 — Knowledge Layer
              Obsidian KB · leyes · PDOT · POA · PAC · territorios

CAPA 5 — Sentinel
              Decisión · aplica / no aplica / requiere preparación
```

→ [[QUIRA_OS_Ontologia]] — arquitectura completa

**Principio rector de cada capa:**
- Excel **calcula** el número.
- Obsidian **interpreta** el sentido.
- Sentinel **decide** la acción.

---

## Definición

**QUIRA OS** es el sistema operativo de gobernanza territorial. No es un dashboard. No es consultoría. Es el ecosistema que organiza la relación entre territorio, metodología, ejecución, fondos, actores y decisión.

**Lo que QUIRA no es:** el motor cuantitativo (eso es el SIAP Engine), ni la metodología (eso es TGI Framework).

**Lo que QUIRA sí es:**
- **Sistema operativo** — da orden, navegación y coherencia al stack completo
- **Integrador** — conecta Excel + Obsidian + Sentinel en una sola arquitectura
- **Escalador** — la misma lógica replica a cualquier municipio

---

## Componentes del Sistema

| Componente | Descripción | Estado |
|------------|-------------|--------|
| **Gold Master TGI v5.5** | Motor Excel — fuente de verdad canónica | ✅ Activo |
| **Gold Master TGI v6.0** | Refactorización completa (34 hojas/7 grupos) | 🔨 En diseño |
| **quira-os** | PMV Streamlit + Python + Supabase | ✅ Sprint 3 activo |
| **snapshot_pipeline.py** | Orquestador principal — 11 pasos | ✅ Operativo |
| **longitudinal_engine.py** | RC-M + tendencias + detección reincidencia | ✅ 53 tests |
| **QUIRA KB** | Vault Obsidian — base epistemológica territorial | ✅ 219 notas |
| **TGI Framework** | Marco metodológico 5D | ✅ Validado Montecristi |

---

## Escalabilidad QUIRA

```
QUIRA
├── Gov     → Gobernanza territorial (caso: GADM Montecristi)
├── Funds   → Gestión de cooperación y fondos internacionales
├── Audit   → Auditoría fiscal y transparencia LOTAIP
├── Civic   → Participación ciudadana y rendición de cuentas
└── Climate → Adaptación climática y riesgo territorial
```

Todos los módulos comparten **TGI** como framework metodológico común.

---

## Regla de Oro QUIRA

> **Prohibido:** alucinar, inventar, simular o falsear normativas, datos o procesos fiscales.
> Todo dato debe ser real, auditable y legalmente aplicable en Ecuador.
> Fuente canónica: SIAP-ICPI_GOLD_MASTER_v5.4

---

## Cadena Canónica — Nodos del Vault

```
[[QUIRA_OS_Ontologia]]       ←  Arquitectura 6 capas
    ↓
[[00_QUIRA_GOV]]             ←  (este nodo) QUIRA OS — ecosistema
    ↓
[[01_TGI_FRAMEWORK]]         ←  TGI — metodología (CAPA 2)
    ↓
[[03_SIAP_ICPI_METHOD]]      ←  SIAP Engine — motor (CAPA 3)
    ↓
[[02_TGI_DIMENSIONES]]       ←  Outputs D1-D5 · TGI=66.85
    ↓
[[03_SENTINEL_LOGICA]]       ←  Sentinel — decisión (CAPA 5)
```

## Módulos Activos — GADM Montecristi 2026

**Motor y metodología:**
- [[03_SIAP_ICPI_METHOD]] — Motor de cálculo Gold Master
- [[01_TGI_FRAMEWORK]] — Marco metodológico TGI 5D
- [[02_TGI_DIMENSIONES]] — D1 a D5 con scores actuales
- [[04_TGI_INDICADORES]] — IRS, IET, ICPI, Trust Score, TGI Score

**Territorio:**
- [[../07_TGI_Parroquias/_Índice_Parroquias]] — TGI 5D por parroquia
- [[../07_TGI_Parroquias/TGI_Cantonal]] — Dashboard cantonal

**Normativa (22 CAPAs):**
- [[../02_NORMATIVA/_Indice_Normativa]] — Marco legal completo

**Planificación:**
- [[../01_PDOT/_Índice_PDOT]] — Diagnóstico y Propuesta PDyOT

---

## Posicionamiento Institucional

| Nivel | Entidad | Descripción |
|-------|---------|-------------|
| Corporativo | Dylus Lab | Desarrollador del sistema |
| Producto | QUIRA Gov | Infraestructura de inteligencia territorial |
| Metodología | TGI | Framework propietario de gobernanza basada en evidencia |
| Caso piloto | GADM Montecristi | Primer municipio validado (2026) |

---

**Fuente canónica:** Gold Master TGI v5.5 · Dylus Lab · QUIRA Gov
**PMV:** quira-os (GitHub: Dylus Lab / quira-os · Streamlit · Python 3.11 · Supabase)
**Fecha actualización:** 2026-05-25
