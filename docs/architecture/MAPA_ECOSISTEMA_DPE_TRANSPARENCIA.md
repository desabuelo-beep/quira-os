# Mapa del Ecosistema Normativo DPE — Transparencia Activa (d07)

> **Estado:** Fase 0 · Producto A · 2026-07-22 (colega: modelo de 5 capas · director: población)
> **Objetivo:** no es "recolectar documentos" — es fijar **qué rol cumple cada artefacto oficial**
> antes de construir el Catálogo Canónico CD-XX (Producto C), para que el catálogo sea un mapa de
> trazabilidad normativa y no un inventario plano.

## Las 5 capas

```
Capa A · Norma jurídica        → ¿Qué es obligatorio?
Capa B · Norma operativa       → ¿Cómo debe cumplirse?
Capa C · Instrumentos          → ¿Cómo se llena?
Capa D · Capacitación          → ¿Cómo interpreta la DPE su propio estándar?
Capa E · Evidencia institucional → ¿Qué hace la DPE cuando el estándar choca con la realidad?
```

## Capa A — Norma jurídica

| Documento | Sigla | Estado |
|---|---|---|
| Constitución (Art. 18, derecho de acceso a la información) | CE | ✅ en Corpus v1.0 |
| LOTAIP (Ley, RO 245, 7-feb-2023) | `LOTAIP` | ✅ en Corpus v1.0 |
| Reglamento General LOTAIP | `RLOTAIP` | ✅ en Corpus v1.0 |

## Capa B — Norma operativa

| Documento | Sigla | Estado |
|---|---|---|
| Guía Metodológica de Mecanismos 2024 (Res. 019-DPE-CGAJ-2024) | `GUIA-LOTAIP-MEC` | ✅ en Corpus v1.0 · vigente |
| Guía Cumplimiento Entidades Obligadas (2018, Res. 007-DPE-CGAJ) | `GUIA-LOTAIP-ENT` | ✅ en Corpus v1.0 · **histórica**, marcada `estado_normativo.vigente=false` |
| **Instructivo de Monitoreo de Transparencia Activa 2024** (v1.0, jul-2024) | *(sin sigla aún)* | 🟡 hallado 2026-07-22, **NO ingerido** — en arqueología, fuera del corpus congelado |

## Capa C — Instrumentos

| Documento | Estado |
|---|---|
| Formatos oficiales de difusión (uno por numeral/conjunto — Anexo 1 del Instructivo, Tablas 6-19) | 🟡 identificados dentro del Instructivo, no separados como artefacto propio |
| Matriz descargable real del portal (ej. CSV numeral 6 "2026-Mayo-Numeral 6-datos6.csv") | ✅ evidencia empírica levantada (OBS-011) |
| Diccionario de datos / metadatos (exigidos por CTA, Instructivo §6.2.1) | ⬜ no levantado aún — es la evidencia que sustenta la calificación CTA |

## Capa D — Capacitación

| Documento | Estado |
|---|---|
| Videos de capacitación DPE por formato (1.1, 1.2, 1.3, 4, 5-22, 10, 16, 17, 18, 19, 20, 21, 23, 24) | 🟡 catalogados por Javo (lista completa en conversación 2026-07-22) |
| **Video del formato de Presupuesto Institucional (CD-06)** | ❌ **ausente** — documentado como observación metodológica (METODOLOGIA_D07 §5b), no como acusación |
| FAQs / preguntas frecuentes DPE | ⬜ no localizadas aún |

## Capa E — Evidencia institucional

| Documento | Estado |
|---|---|
| Correspondencia Ronald Delgado ↔ DPE (Mónica Prado, jul-2026) | ✅ evidencia primaria, documentada en OBS-011 |
| Respuesta oficial DNPMTA (2026-07-09, reconoce discrepancia numeral 6) | ✅ documentada en OBS-011 |
| Oficios / resoluciones aclaratorias adicionales | ⬜ no se ha buscado más allá de lo ya recibido |

## Lectura del mapa (por qué importa antes del Catálogo)

- El Catálogo CD-XX **no puede construirse solo desde la Capa B** (Guía) como se intentó al inicio
  — necesita la Capa C (Instructivo/Formatos, que define los criterios de calificación reales) y
  debe poder anclar cada CD a evidencia de Capa E cuando exista una divergencia conocida (CD-06).
- La ausencia en Capa D (video Presupuesto) y el hallazgo de gobernanza del ACK (ADR-040, Capa A
  mal versionada en una extracción previa) son la prueba de que **cada capa debe verificarse por
  separado contra su fuente primaria** — no hay atajos entre capas.
- **No se ingiere nada al Corpus todavía.** El Instructivo permanece en arqueología (fuera del
  freeze v1.0) hasta cerrar Producto B (algoritmo SITA) y Producto C (Catálogo CD-XX).

---
*Mapa del Ecosistema DPE · Fase 0 Producto A · Dylus Lab © 2026*
