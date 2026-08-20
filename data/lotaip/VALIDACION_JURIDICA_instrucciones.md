# Validación jurídica de las condiciones · Capa 2B

**Archivo a revisar:** `VALIDACION_JURIDICA_condiciones.csv`
(separador `;`, codificación UTF-8 con BOM — abre directo en Excel)

## Qué contiene

105 segmentos normativos extraídos de la **Guía metodológica integral** de la Defensoría del
Pueblo, repartidos en tres poblaciones que **no deben mezclarse**:

| Población | Filas | Qué es |
|---|---:|---|
| `CANDIDATA_a_exigibilidad` | 89 | propuesta de condición exigible · **a validar** |
| `ORIENTACION_no_exigible` | 7 | la Guía usa «podrá», «de preferencia» · faculta, no obliga |
| `FRAGMENTO_no_es_condicion` | 9 | párrafo partido por el maquetado · no es unidad autónoma |

> **89 candidatas NO significa 89 exigencias jurídicas.** Significa 89 segmentos que el
> extractor propone como exigibles por su modo verbal. Hasta esta validación, **ese número no debe
> usarse para calcular cumplimiento, incumplimiento ni SITA** (colega, 2026-08-20).

## Qué hay que hacer

Rellenar tres columnas. Las demás son sólo lectura:

- **`TIPO_VALIDADO`** — confirmar o corregir la clasificación propuesta:

| | Tipo | Qué prescribe |
|---|---|---|
| **A** | `A_exigencia_estructural` | qué debe contener el conjunto de datos |
| **B** | `B_exigencia_material` | condición que exige que determinada información sustantiva exista, se publique, sea accesible o pueda constatarse en la materialización esperada, con independencia de la denominación formal del campo que la transporte |
| **C** | `C_regla_de_calculo` | cómo debe obtenerse o contrastarse un valor |
| **D** | `D_fuente_documental_exigida` | de dónde debe provenir la información |
| **E** | `E_periodicidad` | cada cuánto debe generarse o actualizarse |
| **F** | `F_condicion_procedimental` | qué debe hacer la entidad ante determinada situación |
| **G** | `G_orientacion_no_exigible` | posibilidad, recomendación o mecanismo facultativo · NO exigible |

- **`EXIGIBLE_VALIDADO`** — `si` / `no`
- **`OBSERVACION_JURIDICA`** — cualquier matiz, especialmente si el segmento contiene **más de una
  prescripción** (ver abajo)

## Dónde el clasificador es más débil

**1 · La categoría B se volvió el cajón residual.** 70 de las 89 cayeron ahí, muchas por el
indicio genérico «debe». Es probable que varias sean en realidad estructurales, procedimentales o
de fuente. **Es el bloque que más revisión necesita.**

**2 · Un párrafo puede contener varias prescripciones.** El caso insignia es el segmento del
párrafo 317 (numeral 5-22):

> «los sujetos obligados **deberán** generar un documento en el que se especifique: descripción del
> servicio; a quién está dirigido; requisitos; procedimiento; costo; oficinas; horarios; tiempo
> estimado de respuesta. Esta información **podrá** reportarse en cualquier formato»

Ahí hay **una obligación + ocho requisitos + una facultad de forma** en una sola unidad
tipográfica. El extractor ya separa los ocho (columna `subrequisitos`), pero la facultad accesoria
sigue dentro del mismo registro. Si encuentra más casos así, anótelo en la observación.

**3 · El clasificador ya se equivocó una vez en sentido grave.** Ese mismo párrafo 317 se clasificó
primero como **facultad no exigible**, porque el «podrá» final ganó sobre el «deberán» inicial. Se
corrigió con la regla *una facultad accesoria no degrada una obligación explícita*, pero conviene
mirar con lupa todo segmento que mezcle ambos verbos.

## Trazabilidad

La columna `parrafo` remite al número de párrafo en
`LOTAIP - guia-metodologica-mecanismos.docx` (SHA `4c76ad8934bef620ef3b486cb30e199f…`).
Cualquier fila puede auditarse hasta su texto de origen sin reconstruir el razonamiento.

---
*Capa 2B · Dylus Lab © 2026 · el algoritmo descubre y estructura; el canon determina.*
