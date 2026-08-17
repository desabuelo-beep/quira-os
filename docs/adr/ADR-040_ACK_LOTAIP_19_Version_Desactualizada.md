---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 20]
  type: ARQUITECTONICA
---

# ADR-040 · ACK `LOTAIP_19` construido sobre versión anterior de la ley

**Estado:** ⛔ **REVERTIDO — EL HALLAZGO ERA FALSO** · verificado contra el original 2026-08-17.
Registrado el 2026-07-22 (director técnico · formalizado por el colega); **desmentido por la fuente
primaria**. El ACK y el Catálogo estaban correctos; **este ADR era el error**. Ver §Reversión.
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

## Reversión · 2026-08-17

**Este ADR afirmó algo falso y bloqueó trabajo durante veintiséis días.**

Javo (2026-08-17): *«hay que corregir ese problema de ADR-040, está mal; tenemos ley actualizada y
hay que hacerlo con lo vigente, si no es incoherente»*. Al ir a rehacer el ACK apareció lo
contrario de lo esperado.

### La verificación, sobre el original y no sobre el corpus

`Normativa_Word/LOTAIP.docx`, Art. 19, contando **por nivel de lista** —24 párrafos en nivel 0;
los cuatro sub-incisos de audiencias en nivel 1—:

| Numeral | Texto vigente |
|---|---|
| **18** | **Detalle de los convenios nacionales o internacionales** que celebre la entidad… |
| **19** | **Un detalle actualizado de los donativos oficiales y protocolares**… |
| **20** | **Registro de Activos de Información**, que contenga información solicitada con frecuencia… |

> **El Art. 19 de la LOTAIP 2023 tiene 24 numerales, y los tres que este ADR declaró «de la ley de
> 2004» están en el texto vigente.**

El ACK decía «Transparencia Activa 24 Ítems Obligatorios» y el Catálogo Canónico mapea `CD-18`
Convenios, `CD-19` Donativos y `CD-20` Registro de Activos a esos mismos numerales. **Ambos eran
correctos.**

### De dónde salió el error

El archivo de la guía se llama, literalmente, `guia-para-el-cumplimiento-entidades-obligadas-LOTAIP
**2015 ANTIGUA**, ya que tiene formularios.docx`. **Esa guía sí es de una versión anterior** — y
este ADR lo dice: *«la misma que ya se identificó como base de `GUIA-LOTAIP-ENT`»*.

El error fue **extender esa conclusión al ACK sin contrastarlo contra el texto de la ley**. Un
documento contaminado hizo sospechosos a sus vecinos.

Y hay una trampa que estuvo a punto de repetir el error hoy: contar los numerales **sobre el
corpus** devuelve 31, porque el troceado con solapamiento duplica incisos —«Mecanismos de rendición
de cuentas» aparece dos veces, «Formularios» dos veces—. Sólo el original permite contar.

### La regla que queda

> **Un documento contaminado no contamina a los que están cerca.** La sospecha se hereda; **la
> conclusión, no**. Cada pieza se verifica contra su propia fuente primaria.

Es OBS-030 un nivel más arriba: **antes de atribuir un defecto, falsar que el defecto sea de la
inferencia propia.** Aquí no se dañó a un municipio — se dañó el propio canon, y bloqueó el cierre
del Catálogo durante casi un mes.

### Estado corregido

| Campo | Valor |
|---|---|
| `data/acks/lotaip_f02.yaml` → `LOTAIP_19` | **correcto · no requiere reconstrucción** |
| `data/d07/catalogo_cd_d07_v1.0.0.yaml` | **correcto · 24 numerales + `CD-A24` (Art. 24 GAD)** |
| Bloqueo sobre el Catálogo CD-XX | **levantado** |
| Fuente de la verificación | `LOTAIP.docx` · Art. 19 · 24 numerales en nivel de lista 0 |

---
*ADR-040 · Dylus Lab © 2026 · revertido por la fuente primaria, no por opinión.*
