---
id: OBS-025
authority:
  parent: ADR-047
  constitution_articles: [1, 3, 4]
  type: OBSERVACION
fecha: 2026-08-11
dominio: d06 · motor
estado: VERIFICADA
---

# OBS-025 · `Ei` mide autonomía con una etiqueta que la Constitución no reconoce como binaria

> **Origen.** Javo, con una pregunta de cuatro palabras (2026-08-11): *«¿y esto no pasa por la
> BRN?»*. Pasa. Y al seguirla se cayó la regla que el director estaba a punto de proponer.

## Lo que se iba a proponer, y por qué era un error

Tras encontrar que `Ei` no correspondía a la columna `Competencia_GAD` en 12 de 25 metas, el
director iba a proponer esta regla:

```
Exclusiva → Ei = 1,0     ·     Concurrente → Ei = 0,9
```

**Habría sido el mismo error que veníamos corrigiendo**, con mejor apariencia: tomar una
clasificación asignada a mano y convertirla en regla, solo porque está más estructurada que el
valor anterior. Cambia el síntoma, no la causa.

## Primer hallazgo · la columna tampoco tiene fundamento verificado

`Exclusiva/Concurrente` no es una categoría del Excel: es **jurídica**. Su fuente primaria es la
**Constitución Art. 264** · `SHA256 8a610fc989a27680bc74773949…`, que lista las competencias
exclusivas municipales — planificación y PDOT · uso del suelo · vialidad urbana · agua potable,
alcantarillado y desechos · tasas y contribuciones · tránsito y transporte. `COOTAD 55` la
desarrolla; **no la origina**.

Contrastadas las 25 metas del motor contra ese listado:

| | |
|---|---|
| Coinciden | 11 |
| Marcadas «Exclusiva» **sin figurar en el listado constitucional** | **9** |
| Marcadas «Concurrente» | 5 |

Las nueve: *talento humano · sostenibilidad financiera · modernización administrativa · sistema de
información territorial · participación ciudadana · gestión del riesgo · inventario patrimonial ·
vivienda de interés social · cambio climático*.

Algunas tienen fundamento en **otras** normas —gestión del riesgo en COOTAD 140, participación
ciudadana en la LOPC—; otras son función administrativa interna, no competencia territorial.
**Ninguna en el Art. 264.**

> Derivar `Ei` de esa columna habría propagado nueve clasificaciones sin fundamento verificado,
> **con apariencia de rigor** — que es peor que el criterio manual, porque el criterio manual al
> menos se sabe criterio.

## Segundo hallazgo · la dicotomía no existe en la Constitución

**Constitución Art. 260** · `SHA256 031339ad776e504617dc25c45d…`:

> «El ejercicio de las **competencias exclusivas NO EXCLUIRÁ el ejercicio concurrente de la
> gestión** en la prestación de servicios públicos y actividades de colaboración y
> complementariedad entre los distintos niveles de gobierno.»

Esto es lo decisivo, y desmonta la regla entera:

> **Una competencia puede ser exclusiva en TITULARIDAD y concurrente en GESTIÓN, al mismo tiempo.
> No son categorías opuestas.**

La columna `Competencia_GAD` **colapsa dos dimensiones distintas en una sola etiqueta**, y por eso
no puede sostener a `Ei`:

| Dimensión | Pregunta | Norma |
|---|---|---|
| **Titularidad** | ¿de quién es la competencia? | CE 264 · COOTAD 55 |
| **Régimen de gestión** | ¿se ejerce concurrentemente? | **CE 260** |

Y `Ei` —«autonomía orgánica»— no mide titularidad: mide **con qué autonomía se ejerce**. Es decir,
depende de la segunda dimensión, que es justo la que la etiqueta no captura.

Eso explica de paso la incoherencia original: *alcantarillado* y *desechos sólidos* son
titularidad exclusiva por CE 264 y estaban con `Ei = 0,75`. Puede que quien asignó ese valor
estuviera viendo la **gestión** —que en Montecristi se ejerce vía Empresa de Aseo— y no la
titularidad. **El criterio manual no era arbitrario: estaba midiendo la dimensión correcta con la
etiqueta equivocada.**

## Tercer hallazgo · es el tercer factor manual del mismo motor

| Factor | Cómo se asigna | Estado |
|---|---|---|
| `Ci_Manual` | a mano, calibrado hacia atrás para reproducir el ICPI 2025 | declarado en el glosario |
| `Ei` | a mano, sin regla derivable | OBS-025 |
| `Competencia_GAD` | a mano, sin trazabilidad normativa | OBS-025 |

**Los tres alimentan la fórmula canónica.** El patrón importa más que cualquiera de ellos por
separado:

> Cuando un factor puede derivarse de evidencia normativa verificable, **no debería existir una
> asignación manual equivalente** — y si existe, debe declararse como calibración, no como medida.

## La simulación queda como contrafactual, no como resultado

Se aplicó la regla candidata sobre copia y se recalculó con Excel real:

```
ICPI  27,4582 %  →  28,5665 %      (+1,1083 pp)
```

**No es el ICPI corregido.** Es la medida del efecto de una regla que este mismo expediente
descarta. Se conserva porque dimensiona algo útil: **el índice es robusto** — corregir doce de
veinticinco valores de un factor secundario lo mueve un punto. Lo que pesa es `Vi` y `Ti`.

## Dónde entra la BRN, y dónde no

Respondiendo la pregunta que originó todo:

```
CE 260 · CE 264 · COOTAD 55 · COOTAD 140 · LOPC …
        ↓
  clasificación de competencia (titularidad + régimen de gestión)
        ↓
  regla metodológica de Ei
        ↓
  Gold Master  →  ICPI
        │
        └──→ BRN: qué normas, en conjunto, sostienen cada clasificación
```

**La BRN no calcula `Ei`** (ADR-038: traza el motor, no lo alimenta). Lo que sí hace, y hoy falta,
es permitir auditar **qué conjunto de normas sostiene cada clasificación** — porque, como muestra
este caso, *una celda no corresponde a un artículo*: corresponde a **varias normas que
conjuntamente la sustentan**.

## Lo que NO se hace

- **No se toca el motor vivo.** La regla candidata queda descartada, no aplicada.
- **No se recalibra `Ci_Manual`** para compensar. Sería repetir el reverse engineering que ya se
  documentó.
- **No se inventan los valores de `Ei` por categoría.** Deben salir de la metodología o aprobarse
  como regla nueva, con su fundamento.

## Lo que corresponde

1. Modelar las **dos dimensiones** —titularidad y régimen de gestión— en vez de una etiqueta.
2. Fundamentar cada clasificación con **el conjunto** de normas que la sostienen, con SHA.
3. Definir qué significa cada situación para **autonomía**, que es lo que `Ei` mide.
4. Recién entonces derivar `Ei`, y recalcular.

---
*OBS-025 · Dylus Lab © 2026 · una pregunta de cuatro palabras evitó publicar una regla sin fundamento.*
