---
id: OBS-027
authority:
  parent: ADR-047
  constitution_articles: [1, 3]
  type: OBSERVACION
fecha: 2026-08-12
dominio: d01 · d06
estado: VERIFICADA
---

# OBS-027 · El POA 2026 conserva seis niveles de objetivo y pierde la meta

> **Origen.** Javo (2026-08-12): *«revisando POA 2025 tiene anclaje a meta y objetivos PDOT. Pero
> POA 2026 tiene anclaje a todo menos a metas. Esto es tan frustrante»*. Verificado sobre los
> originales del GAD: **es exacto**.

## Lo que cambió entre dos años consecutivos

Contrastados los `.xlsx` originales de la carpeta oficial del GAD:

| | POA 2025 | POA 2026 |
|---|---|---|
| `INDICADOR ESTRATÉGICO PDOT` | **columna 7** | **ausente** |
| Indicador («Porcentaje del parque automotor útil») | **columna 8** | **ausente** |
| **Meta** («Aumentar del 91 % de vehículos en funcionamiento…») | **columna 9** | **ausente** |
| Objetivo de Desarrollo Sostenible | sí | sí |
| Objetivo Plan Nacional de Desarrollo | sí | sí |
| Sistema PDOT | sí | sí |
| Objetivo de Desarrollo del PDOT | sí | sí |
| Objetivo Estratégico del PDOT | sí | sí |
| Objetivo de Gestión | sí | sí |
| Columnas totales | 40 | 30 |
| Filas de actividad | 644 | 51 |

> **El POA 2026 mantiene SEIS niveles de objetivo y no declara ninguna meta ni indicador.**

No es una diferencia de redacción ni un problema de lectura: son **columnas que existían en 2025 y
no existen en 2026**.

## Por qué importa

La meta es lo único **cuantificable** de la cadena. Un objetivo dice hacia dónde; una meta dice
**cuánto y para cuándo**. Sin esa columna, el POA declara alineación estratégica pero **no declara
contra qué se mide**.

Consecuencia directa y verificable: **el vínculo entre una partida presupuestaria de 2026 y una
meta del PDOT no es recuperable desde el propio instrumento.** Hay que inferirlo — y la inferencia
es precisamente lo que este sistema no hace.

## Lo que NO se concluye

- **No se afirma incumplimiento.** La normativa de planificación exige alineación al PDOT, y el
  POA 2026 la declara por seis vías distintas. Que no incluya la meta puede responder a un cambio
  de formato de la herramienta, a una directriz del ente rector o a una decisión interna.
- **No se compara desempeño entre años a partir de esto.** Es una diferencia de *instrumento*, no
  de gestión.
- **No se rellena la columna faltante.** Si el POA no lo declara, QUIRA no lo supone.

## La regla que este caso obliga a fijar

Javo (2026-08-12): *«solo estamos evaluando metas y no objetivos, deberíamos evaluar ambos. Pero
no tomar una porque falta la otra».*

Queda como regla metodológica:

> **Objetivo y meta son dimensiones distintas de la articulación y se evalúan por separado. La
> ausencia de una no anula la otra, y ninguna se infiere de la otra.**

De ahí una matriz de cuatro estados, en lugar de un binario cumple/no cumple:

| Objetivo | Meta | Lectura |
|---|---|---|
| ✓ | ✓ | articulación completa |
| ✓ | — | **articulación estratégica sin operacionalización medible** ← POA 2026 |
| — | ✓ | requiere revisión metodológica |
| — | — | sin vínculo documental hallado |

Esto además resuelve el caso de **Bomberos** (OBS-024) sin forzarlo: articula por objetivo aunque
no tenga meta asignada. Deja de ser una contradicción y pasa a ser una casilla legítima.

## Confirmado por una segunda fuente: el PAI 2026 tampoco declara meta

*(2026-08-12)* Quedaba abierta una posibilidad razonable: que la meta viviera en otro instrumento
del mismo año. El **Plan Anual de Inversiones** era el candidato natural — ordena la inversión y
trae la partida. Verificado sobre los originales:

| Año | filas | objetivo | **META** | indicador | partida | cód. actividad |
|---|---|---|---|---|---|---|
| PAI 2023 | 104 | 104 | **0** | 0 | 104 | 0 |
| PAI 2025 | 109 | 109 | **109** | 109 | 109 | 0 |
| **PAI 2026** | **101** | **93** | **0** | **0** | **95** | **95** |

> **En 2026 la meta desaparece de toda la cadena operativa —POA y PAI—, no de una hoja suelta.**

### Y un cambio que dice más que la ausencia

**El mismo instrumento que elimina la meta introduce el `CÓDIGO DE LA ACTIVIDAD`** (`APAA-01`,
`OOPP-25`), presente en 95 de 101 filas y ausente en 2023 y 2025.

No se perdió trazabilidad sin más: **se movió del plan a la organización.** El identificador nuevo
ancla la actividad a la dirección que la ejecuta; el que se fue la anclaba al plan que debía
cumplir. Es un objeto de gestión con llave propia —lo que OBS-026 echaba en falta— pero apuntando
al organigrama en vez de al PDOT.

### Lo que sí se puede afirmar de 2026

Cruzado el PAI 2026 contra la cédula del GAD (corte abril, acumulada):

| | objetivos |
|---|---|
| Con **devengado certificado** | **8 / 9** |
| Con codificado sin devengado | 1 / 9 |
| **Sin evidencia financiera** | **0** |

Los nueve objetivos estratégicos del PAI tienen respaldo financiero verificable; alcanzan
**$1.781.928** de los $7.752.518 devengados al corte —el 23 %, coherente con que el PAI cubra
inversión y no el presupuesto entero—.

> **Formulación admisible:** *el POA y el PAI 2026 presentan articulación estratégica con el PDOT,
> verificable hasta el devengado; el instrumento no declara anclaje explícito a metas, por lo que
> la trazabilidad operacional hacia metas no es demostrable desde ninguno de los dos.*
>
> ⛔ **No admisible:** «el POA 2026 no está articulado al PDOT». La primera afirmación está
> respaldada por lo hallado; la segunda es más fuerte de lo que la evidencia permite.

### Nota de método: un desalineamiento que no dio error

Sólo la primera de las cuatro hojas del PAI 2026 trae títulos; las demás arrancan en datos. Una de
ellas —`Table 3`— viene **corrida una columna** por celdas combinadas que la exportación abrió.
Heredar el mapa de títulos tal cual leía el objetivo de desarrollo como objetivo estratégico y el
grupo de gasto como partida, **sin producir un solo error**: las filas salían completas y
equivocadas. Se detectó porque aparecían «objetivos estratégicos» llamados *Montecristi Natural y
Protegido*, que son objetivos de desarrollo.

Corregido anclando por la partida de 6 dígitos, reconocible por su forma. **De 12 objetivos
contaminados a 9 reales.**

## Un tercer hallazgo, y este es nuestro

Antes de llegar aquí, el corpus mostraba el POA del GAD con **53 % de texto roto** —columnas de
tabla leídas carácter a carácter— y eso llevó a concluir que el POA «no anclaba». **Era un defecto
de nuestra ingesta**: los documentos se habían convertido a `.docx` y la estructura tabular se
destruyó.

Los originales del GAD son **`.xlsx` con columnas limpias**. El municipio sí entregaba
trazabilidad; nosotros la perdíamos al ingerirla.

> **Antes de atribuir una carencia a la fuente, hay que descartar que sea del capturador.** Es la
> misma lección de ADR-042 §6 —«no existe» ≠ «no pude obtener»— aplicada a la ingesta documental.

## Trazabilidad

| Fuente | Carácter |
|---|---|
| `POA 2023-2026/GAD Montecristi/GAD Monteristi POA 2025.xlsx` | oficial · carpeta del GAD |
| `POA 2023-2026/GAD Montecristi/GAD Montecristi POA 2026.xlsx` | oficial · carpeta del GAD |
| POA 2023 y 2024 (7 y 6 columnas) | oficial — **tampoco declaran alineación al PDOT** |

Nota: el anclaje al PDOT aparece **solo en 2025 y 2026**. En 2023 y 2024 el POA se limita a
actividad, partida, monto, financiamiento y responsable.

---
*OBS-027 · Dylus Lab © 2026 · verificado sobre los originales, no sobre la copia ingerida.*
