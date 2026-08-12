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

## Un segundo hallazgo, y este es nuestro

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
