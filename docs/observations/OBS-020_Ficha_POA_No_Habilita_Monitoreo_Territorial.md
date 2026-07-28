---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 4, 9]
  type: OBSERVACION
---

# OBS-020 · La ficha POA no habilita el monitoreo territorial del desarrollo

**2026-07-29 · d08 · hallazgo de Javo (15 años en gestión pública de GAD) · medido por QUIRA**

> **El instrumento, no el algoritmo.** Tras tres rondas de corrección del cruce
> demanda↔POA —cada una destapando la siguiente— el límite dejó de ser el motor y pasó a
> ser el documento. Esta observación **mide** lo que Javo formuló:
>
> *"El problema real es la forma metodológica de construcción de la ficha de POA. Es una
> cuestión muy general que no aterriza las necesidades para un monitoreo y evaluación real
> e integral de la planificación del desarrollo cantonal."*

---

## 1 · La medida

`scripts/d08/diagnostico_ficha_poa.py` · **1.027 filas · POA 2023-2026 · GAD Montecristi**

| Atributo de la fila POA | Filas | % |
|---|---:|---:|
| Declara **objeto** sustantivo | 1.027 | 100% |
| **Declara TERRITORIO de ejecución** | **11** | **1,1%** |
| ↳ *corroboración independiente* (marcador de lugar) | 13 | 1,3% |
| Declara **componentes operativos** | 306 | 29,8% |

**~99% de las filas del POA no permite saber DÓNDE se ejecuta el gasto.**

### Por qué la cifra es afirmable

Se midió por **dos caminos independientes** que convergen:

1. **Registro de topónimos** (jerarquía territorial canónica de 7 niveles) → 1,1%
2. **Marcadores de lugar** (`barrio|sector|comuna|parroquia|sitio|recinto|km …`), que **no
   depende de conocer ningún nombre** → 1,3% *(y una de esas 13 es "sector Público", que
   no es un lugar)*

Un solo método podría subestimar por registro incompleto. Dos métodos distintos con la
misma medida es lo que la vuelve afirmable.

> ⚠️ **Corrección incorporada:** el primer conteo dio **75,7%**. Era falso: **769 de esos
> 777 aciertos eran la palabra "Montecristi"** — el membrete institucional del GAD, no la
> ubicación del proyecto. El cantón es el **universo** del análisis, no una localización.

## 2 · Consecuencia directa sobre la auditoría

**La trazabilidad territorial de la demanda ciudadana es imposible por construcción del
documento, no por falta de algoritmo.** Ninguna mejora del motor puede recuperar un dato
que no está escrito.

Esto reordena el hallazgo de d08: cuando una demanda de un barrio queda `sin_correlato`,
la causa dominante no es que el GAD no la atendiera — es que **el POA no registra el
territorio**, así que la correspondencia no es verificable en ningún sentido.

### `instrumental = 0` deja de ser un hueco y pasa a ser una medida

El cruce arroja **cero** relaciones de satisfacción instrumental. No significa que no
existan: significa que **el 70% de las filas no declara componentes operativos**, y sin
declaración QUIRA no infiere (Principio de No-Inferencia). El cero **es** el hallazgo.

## 3 · Un tercer patrón de opacidad — de formato a estructura

La `TEORIA_EVIDENCIA_PUBLICA_VERIFICABLE.md` tipificaba dos patrones de **opacidad de
formato**. Éste es de naturaleza distinta: la **opacidad de estructura de contenido**.

| Patrón | Naturaleza | En qué consiste |
|---|---|---|
| **Excel Cáscara** | formato | cumple la forma de publicación, el contenido es un enlace |
| **PDF Trampa** | formato | el documento existe pero es ilegible por máquina |
| **Ficha POA Agregada** *(nuevo)* | **estructura** | el documento es **perfectamente legible** y aun así **no permite verificar nada**: mezcla partida · programa · actividad · unidad en una sola fila, y omite el territorio |

> **La ficha no fue construida para ser leída, sino para ser aprobada.** Cumple el trámite
> financiero; no habilita el monitoreo de la planificación del desarrollo.

Que sea legible es lo que lo hace más grave: ningún OCR, ningún modelo, ninguna mejora de
ingesta lo resuelve. **Es el techo de la auditoría automatizada sobre planificación.**

## 4 · Evidencia de que el instrumento induce el error

Las tres rupturas del cruce fueron causadas por metadato de la ficha, no por el motor:

| # | Metadato leído como contenido | Corrección |
|---|---|---|
| 1 | membrete institucional | `es_encabezado()` |
| 2 | unidad ejecutora (`Dirección de Obras Públicas`) | **REGLA 0** (OBS-019) |
| 3 | homógrafo (`Parqueaderos` ⊃ `parque`) | `HOMOGRAFOS` |
| 4 | programa presupuestario (`Urbanización y Embellecimiento`) | *no corregido — ver §6* |

Cada capa filtrada destapó la siguiente. **Un documento bien construido no produce esa
secuencia.**

## 5 · Frontera de lo que QUIRA afirma *(Carta Art. 4.5)*

| ❌ QUIRA **no** dice | ✅ QUIRA certifica |
|---|---|
| *"el GAD incumple la planificación"* | *"el instrumento de planificación **no habilita** la verificación de correspondencia entre demanda ciudadana y ejecución territorial"* |

Es **ausencia de habilitación documental** — la segunda de las tres categorías que QUIRA sí
certifica. Determinar incumplimiento corresponde a la Contraloría, no a QUIRA.

## 6 · Decisión tomada: dejar de parchar

El programa presupuestario (`Urbanización y Embellecimiento`) es metadato igual que la
unidad ejecutora, y **no se neutralizó**. Razón: a diferencia de la unidad —que no dice
nada del objeto—, el programa **sí aporta señal temática débil**. Filtrarlo perdería
información; conservarlo produce correspondencias débiles. Ambas opciones son defendibles,
y por eso **la decisión es de Javo, no del motor**. Esas correspondencias quedan en
`pendiente_validacion`: es exactamente donde deben quedar.

## 7 · Acciones

| # | Acción | Estado |
|---|---|---|
| 1 | Medir la habilitación de la ficha POA | ✅ `diagnostico_ficha_poa.py` |
| 2 | Corroborar el ancla territorial por método independiente | ✅ dos métodos convergen |
| 3 | Excluir el cantón como ancla (Regla T1: `cantón → parroquia: PERMITIDO`) | ✅ aplicada |
| 4 | Incorporar **Ficha POA Agregada** a la Teoría de la Evidencia Pública Verificable | ✅ §3 |
| 5 | Evaluar el % de habilitación de la ficha como **SAT candidata** | ⏳ decisión de Javo (Regla 1: se sella en el Gold Master) |
| 6 | Decidir si el programa presupuestario se neutraliza | ⏳ decisión de Javo |
| 7 | Replicar el diagnóstico en un segundo GAD (¿es Montecristi o es el modelo nacional?) | ⏳ Gate 7 |

> **La pregunta que abre para los 222 GAD:** si la ficha POA de Montecristi no localiza el
> gasto, ¿es un defecto de este municipio o **la forma nacional del instrumento**? La
> respuesta cambia el alcance de QUIRA: de auditar un GAD a **auditar el instrumento con
> que Ecuador planifica su desarrollo local**.

---
*OBS-020 · Dylus Lab © 2026 · hallazgo de Javo, medido por QUIRA · deriva de OBS-019.*
