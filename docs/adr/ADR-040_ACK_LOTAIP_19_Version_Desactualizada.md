---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-040 · ACK `LOTAIP_19` construido sobre versión anterior de la ley

**Estado:** REGISTRADO · pendiente de reconstrucción · 2026-07-22 (hallazgo director técnico ·
formalización propuesta por el colega)
**Contexto de origen:** al reconstruir el estándar oficial de d07 (Fase 0, arqueología normativa
DPE), se comparó el ACK `LOTAIP_19` (`data/acks/lotaip_f02.yaml`, extraído 2026-05-30 vía QLEP v1.2)
contra el texto literal del Art. 19 de la LOTAIP vigente en el corpus (verificado 2026-07-22).
**Relacionado:** OBS-011 (numeral 6 · ingresos) · METODOLOGIA_D07_CUMPLIMIENTO_LOTAIP.md.

---

## Hallazgo

El ACK `LOTAIP_19` describe numerales (Convenios, Donativos, Registro de Activos de Información
como ítems propios del Art. 19) que **no corresponden a la redacción vigente** de la LOTAIP 2023
(RO 245, 7-feb-2023). Esa numeración pertenece a una **versión anterior de la ley** (la de 2004,
la misma que ya se identificó como base de `GUIA-LOTAIP-ENT`, ver `manifest.py`).

No es un detalle de transcripción: es un **evento de gobernanza del corpus** — el mismo error
estructural (extraer sin verificar contra la versión vigente) que ya se corrigió una vez para
`GUIA-LOTAIP-ENT`, ahora aparece también en la capa de ACKs (QLEP), no solo en el manifiesto de
documentos.

## Decisión

**No se modifica el ACK todavía.** Se registra el hallazgo con este ADR para dejar trazabilidad de
por qué cambiará, y se pospone la reconstrucción hasta cerrar el Catálogo Canónico CD-XX (Fase 0,
Producto C) — que de todos modos requiere fijar la numeración vigente del Art. 19 desde la fuente
primaria (el corpus, no un ACK de mayo).

| Campo | Valor |
|---|---|
| Elemento afectado | `data/acks/lotaip_f02.yaml` → `LOTAIP_19` y sub-átomos `LOTAIP_19_X` |
| Estado | Pendiente de reconstrucción |
| Impacto | Dominio d07 (Transparencia) |
| Prioridad | Alta — bloquea cerrar el Catálogo CD-XX con confianza total |
| Acción | Reconstrucción completa del ACK desde el texto literal vigente del corpus (no desde memoria ni desde el ACK anterior) |
| Bloqueado por | Nada — puede ejecutarse en paralelo al Catálogo, pero se prioriza después de éste para evitar doble trabajo |

## Por qué no se corrige de inmediato

Corregir el ACK ahora, aislado, arriesga repetir el mismo error una tercera vez (extraer rápido sin
el contexto completo del Instructivo + Guía + Formatos que se está reconstruyendo en paralelo). Se
espera a tener el Catálogo Canónico CD-XX (que ya exige fijar la numeración correcta) y de ahí se
deriva el ACK corregido — una sola fuente de verdad, no dos reconstrucciones independientes que
puedan divergir entre sí.

---
*ADR-040 · Dylus Lab © 2026*
