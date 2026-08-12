---
id: OBS-028
authority:
  parent: ADR-047
  constitution_articles: [1, 3, 4]
  type: OBSERVACION
fecha: 2026-08-12
dominio: d01 · d06 · motor
estado: VERIFICADA
---

# OBS-028 · `V_eSIGEF` se derivaba de la fuente equivocada — y los ceros del motor no se sostienen

> **Origen.** El derivador de `V_eSIGEF` acertaba 33 %, luego 58 %. Los fallos se repartían en dos
> grupos exactos de cinco, y esa simetría no era ruido: **se estaba midiendo con el instrumento
> equivocado.**

## El error de fondo

`V_eSIGEF` no pregunta «¿está la meta en el POA?». H13 lo define literalmente: **«devengado
certificado»**. Estar en el POA es **planificación**; tener devengado es **ejecución**. Una meta
puede planificarse y no ejecutarse, o ejecutarse por reforma sin constar en el POA original.

> **El POA no acredita devengado. La cédula presupuestaria sí.**

La cadena real tiene dos saltos, y **cada fuente prueba sólo el suyo**:

```
meta PDOT  ──POA──▶  partida  ──cédula──▶  devengado
           (planificación)     (ejecución)
```

Pedirle a una sola fuente que pruebe la cadena entera es lo que produjo el 33 %.

## Alcance: 2025 en adelante — y por qué

**Ordenanza Nro. 07-2024-CM-GADMCM**, que aprueba la actualización del PDOT y el PUGS 2023-2027
(«Plan Bicentenario»), **sancionada el 5 de noviembre de 2024** —firma digital del Secretario del
Concejo, `2024.11.05 16:12:09 -05'00'`—. `sha256 662756aac591b247decdf3428fd9df03d09c8744c4e580e5…`

Hallazgo de Javo (2026-08-12): *«el POA 2023 y 2024 se trabajaron con el PDOT anterior, así lo
establece la norma; no deberían entrar en nuestro análisis»*. **Correcto**, y hay un segundo motivo
independiente ya verificado: el POA 2023 y 2024 **no traen columnas de alineación al PDOT**
(OBS-027). No pueden acreditar nada sobre estas 66 metas, por la razón que sea.

> **Corrección de una lectura previa.** El director había registrado como hallazgo que «el POA
> 2023-2024 no declara anclaje al PDOT mientras su cédula sí es detallada». **Eso no es opacidad: es
> cronología.** Ese POA no podía anclar a un plan que aún no existía en su versión vigente.

La ordenanza aprueba una **actualización** del PDOT, y eso no es una irregularidad ni un cabo
suelto: **es el procedimiento reglado.** El *Acuerdo Ministerial SNP-SNP-2023-0049-A* —Guía para la
formulación/actualización de PDOT, proceso 2023-2027, en corpus, `sha f3b8ed699e64`— fija los casos
en que un PDOT se formula o actualiza, y el primero es:

> «**Al inicio del periodo de gestión de las autoridades locales.**» *(los otros: proyecto nacional
> estratégico en la jurisdicción · fuerza mayor, como un desastre · creación o modificación de una
> circunscripción territorial)*

El Plan Bicentenario **es** el PDOT del período 2023-2027; el plan anterior corresponde al ciclo de
la administración precedente. Por eso el corte en la fecha de sanción no es una convención del
analista: **es el límite que la norma establece.**

> **Corrección (Javo · 2026-08-12):** el director había anotado la actualización como una
> incógnita —«qué metas cambiaron no está establecido»—. *«No es ambigüedad, es norma, y el
> procedimiento está en las guías de PDOT que están en el corpus.»* Exacto: estaba en `ACUERDO-PDOT-2023`,
> a una consulta de distancia. **Marcar como desconocido lo que la fuente ya responde es tan
> defectuoso como inventarlo.**

## Lo que la cadena sí produce

Sobre POA 2025 (644 filas) y cédula de **diciembre 2025** —verificada acumulada: entre octubre y
diciembre, 69 partidas suben, 68 quedan igual y **ninguna baja**—:

| | metas |
|---|---|
| Reconciliadas con el POA 2025 | **46 / 66** |
| **`no_reconciliado`** — el procedimiento vigente no las alcanzó | 20 / 66 |
| `devengado_certificado` | 41 |
| `codificado_sin_devengado` | 5 |

> **Corrección del colega (2026-08-12), aplicada al código.** El director escribió «23 metas no
> tienen partida». Eso **afirma una ausencia que el procedimiento no probó**. El estado correcto es
> **`no_reconciliado`**: *no fueron vinculadas con una actividad del POA 2025 bajo el procedimiento
> de reconciliación actualmente implementado*. La diferencia no es de redacción —`sin_partida`
> habla de la fuente, `no_reconciliado` habla de nosotros—, y en el código estaban colapsadas en un
> mismo estado. Ahora se distinguen:
>
> | estado | qué afirma |
> |---|---|
> | `no_reconciliado` | **nuestro** procedimiento no alcanzó la meta |
> | `sin_partida_declarada` | **el POA** la trae y no le ancla partida |
>
> Es la Regla de Oro 3 aplicada contra el propio sistema: **ausencia de evidencia ≠ evidencia de
> ausencia**, y el derivador no está exento.

## Pero la atribución es débil, y eso importa más que el porcentaje

| Atribución | metas |
|---|---|
| **Unívoca** — alguna partida exclusiva sostiene el estado | **9** |
| **Compartida** — ninguna partida es exclusiva | **37** |

La partida presupuestaria es un **ítem de gasto** («consultoría», «edificios»), no un identificador
de meta. `730606` sirve a **16 metas distintas**; `840104` a 11. Que varias metas compartan un ítem
es normal en técnica presupuestaria — **lo inadmisible es tratar el devengado de ese ítem como
prueba de una meta en particular.**

> Para 37 de 46 metas puede afirmarse *«hay ejecución en la línea que financia esta meta»*, y **no**
> *«esta meta se ejecutó»*. Son afirmaciones distintas y el sistema conserva cuál sostiene.

## Los ceros de H13 no se sostienen

Contrastado el derivado contra los 25 valores que el motor ya tenía:

| H13 | derivado | casos |
|---|---|---|
| **0** | devengado certificado | **5** |
| 1 | 0,5 | 1 |
| 1 | no derivable (meta ausente del POA 2025) | 6 |
| coinciden | | 12 |

**De los 6 ceros que H13 declara en `V_eSIGEF`, cinco los contradice la cédula y el sexto no tiene
partida. Ninguno se confirma.**

Precisión necesaria: los cinco contradichos se apoyan en partidas **compartidas**. Lo que queda
establecido es que **el cero no es sostenible** —«sin registro presupuestario» es falso, hay
devengado en las líneas que las financian—; que el valor correcto sea 1,0 **no queda establecido**.

### Y un indicio sobre cómo se llenó H13

**`V_SERCOP` y `V_eSIGEF` son idénticos en las 25 filas.** Dos verificadores que la propia hoja
define como independientes —uno lee SERCOP, otro lee eSIGEF— no coinciden 25 de 25 veces por azar.
Es consistente con una asignación en bloque, no con una lectura de cédulas.

> **Los tres factores manuales del motor** (`Ei`, `Ci_Manual`, `Competencia_GAD`) ya estaban
> identificados. **`V_eSIGEF` y `V_SERCOP` se suman a la lista**: entran a la fórmula canónica sin
> cadena documental verificable.

## Ejecución sin meta demostrable

**$235.678,50** devengados en 5 partidas que el POA 2025 no vincula a ninguna meta. La mayor es
`990101` *Obligaciones de Ejercicios Anteriores* ($194.853,21); el resto son compensación de
transporte, jubilados patronales y horas extraordinarias.

No se concluye irregularidad: son rubros que por naturaleza no tributan a una meta de desarrollo.
Se registra porque **es la dirección inversa del cruce y también es un resultado.**

## Lo que se corrigió del propio derivador

1. **Descartaba evidencia válida.** Cuando una meta tenía alguna partida exclusiva, ignoraba todas
   las demás. Llegó a declarar `sin_registro_presupuestario` en una meta con **$187.200 devengados**
   en otra de sus partidas. La exclusividad sirve para *atribuir un monto*; para responder *«¿hay
   devengado?»* descartar partidas **es fabricar una ausencia estrechando la mirada.**
2. **Umbral de reconciliación absoluto.** Exigía 50 caracteres de prefijo exacto y rechazó cuatro
   metas cuyo enunciado **completo** mide 33 y 41. Coincidían enteras y se descartaron por cortas.
3. **Dos convenciones numéricas conviviendo.** El Numeral 6 escribe `1.866.275,79`; la cédula del
   eSIGEF, `23,327,341.51`. Fijar una habría devuelto `None` en silencio para todo un instrumento.

## Hallazgos colaterales del instrumento

- **La ordenanza que da vigencia al plan no es legible por máquina.** 242 páginas escaneadas, **241
  caracteres** de capa de texto. Se leyó renderizando las páginas. Es el caso concreto que sostiene
  la propuesta de OCR del colega del GAD.
- **El Patronato publica su Conjunto de Datos del Numeral 6 dentro de un documento de Word**
  (`…CONJUNTO DE DATOS.csv.docx`). Dato abierto en formato que no lo es.
- **La cédula del Numeral 6 (2025-2026) tiene menos estructura que la que reemplazó.** La de
  2023-2024 traía el código estructurado completo —programa · proyecto · actividad · ítem—; la
  nueva trae sólo el ítem de 6 dígitos. **Es el mismo patrón que OBS-027 halló en el POA: el
  instrumento nuevo pierde trazabilidad respecto del anterior.**
- **M002 y M018 comparten enunciado literal** en el PDOT. Ninguna reconciliación por texto puede
  separarlas; el cruce marca `reconciliacion_ambigua` en vez de elegir.

## Regla que queda fijada

> **Ninguna fuente prueba la cadena entera.** El POA prueba planificación; la cédula prueba
> ejecución. El cruce **conserva estados con su procedencia** —archivo, hoja, fila, partida,
> período— y `no_hallado` **nunca** significa `no existe`.

## Trazabilidad

| Fuente | Carácter |
|---|---|
| `Ordenanza del Plan Bicentenario Montecristi SIGNED.pdf` | oficial · firmada · `sha256 662756aa…` |
| `POA 2023-2026/GAD Montecristi/GAD Monteristi POA 2025.xlsx` | oficial |
| `Cedulas Presupuestarias 2023-2026/Presupuestos 2025/GAD Montecristi/…Diciembre…xlsx` | oficial · Numeral 6 LOTAIP |
| `data/pdot/cruce_poa_cedula.json` | **capa derivada** · no sustituye ninguna fuente |

---
*OBS-028 · Dylus Lab © 2026 · fecha de la ordenanza aportada por Javo, verificada contra la firma digital.*
