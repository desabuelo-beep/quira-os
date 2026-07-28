---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 4, 9]
  type: OBSERVACION
---

# OBS-020 · La ficha POA no habilita el monitoreo territorial del desarrollo

**2026-07-29 · hallazgo de Javo (15 años en gestión pública de GAD) · medido por QUIRA**

| | |
|---|---|
| **Dominio del OBJETO** | **d01 · Planificación Estratégica** — el POA es su instrumento |
| **Dominio del DESCUBRIMIENTO** | d08 · Participación Ciudadana (cruce demanda↔POA) |
| **Métrica que instrumenta** | **CVI** · Capacidad Verificativa del Instrumento |

> **El instrumento, no el algoritmo.** Tras cuatro rondas de corrección del cruce
> demanda↔POA —cada una destapando la siguiente— el límite dejó de ser el motor y pasó a
> ser el documento. Esta observación **mide** lo que Javo formuló:
>
> *"El problema real es la forma metodológica de construcción de la ficha de POA. Es una
> cuestión muy general que no aterriza las necesidades para un monitoreo y evaluación real
> e integral de la planificación del desarrollo cantonal."*

---

## 0 · Anclaje de dominio *(corrección de Javo · 2026-07-29)*

Javo preguntó: *"todo esto de planificación debe tratarse en su dom que es planificación
estratégica, ¿o no?"* — **Sí. Estaba anclado en el dominio equivocado**, y el propio canon
ya tenía la regla escrita.

`TEORIA_EVIDENCIA_PUBLICA_VERIFICABLE.md` fija el precedente para d07:

> *"d08 y los demás dominios **consumen** la evidencia; **d07 califica cómo fue publicada**."*

La misma estructura, aplicada al instrumento en vez de al formato:

| Dominio | Rol frente al POA |
|---|---|
| **d01 · Planificación** | **CALIFICA** cómo fue construido el instrumento — el POA es suyo |
| **d07 · Transparencia** | CALIFICA cómo fue publicado (formato · ICEP) |
| **d08 · Participación** | **CONSUME** el POA para verificar satisfacción de demandas |

**Regla que se deriva y generaliza a los 12 dominios:**

> **Quien es dueño del instrumento lo califica; quien lo usa solo lo consume.** Un dominio
> que consume no puede emitir juicio sobre la calidad del instrumento ajeno — solo reportar
> qué NO pudo verificar con él.

Es **Subsidiariedad Normativa** (Carta Art. 1.2) aplicada a los dominios: la regla vive en
el nivel más bajo que la contiene por completo. d08 no necesita saber por qué el POA es
opaco; necesita saber que no puede verificar territorio con él.

### Qué implica operativamente

- El hallazgo **pertenece a d01** y debe reflejarse en `docs/pcd/PCD-D01_Planificacion.md`.
  d01 está cerrado con PCD; esta observación es la vía canónica para incorporarle un
  hallazgo posterior sin reabrir su curación (Regla 8).
- d08 **conserva** el efecto: sus `sin_correlato` quedan explicados por causa externa.
- La **medición** es transversal (CVI), no de d08 ni de d01: se aplica a todo instrumento.

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

> **Frontera de la afirmación (corrección de la asesoría · 2026-07-29).** Decir que la ficha
> *"fue construida para ser aprobada y no para ser monitoreada"* **atribuye intención
> institucional** y NO está demostrado. Es el mismo error que este sistema corrige en el
> filtro, cometido en la prosa. Lo que sí se demuestra es lo observable:
>
> *"La ficha POA observada no contiene información suficiente para reconstruir
> territorialmente la ejecución mediante evidencia documental verificable."*
>
> Establecer el **por qué** exigiría contrastar el diseño normativo del instrumento con su
> implementación, o comparar varios municipios. Es hipótesis, no hallazgo.

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

> ✅ **DECISIÓN TOMADA (2026-07-29): NO se neutraliza.** Hoy no se sabe si su bajo poder
> discriminante es defecto del instrumento, defecto del algoritmo o **característica estable
> del fenómeno** — y distinguirlo es precisamente lo que exige **R-D**. Retirarlo ahora sería
> decidir sin evidencia y perder señal temática de forma irreversible. Se conserva activo con
> sus correspondencias en `pendiente_validacion`. La reclasificación como variable auxiliar
> solo procede si, **cerrado Montecristi** (R-E), la señal sigue siendo débil.

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

## 8 · Redacción canónica del hallazgo

Toda cita de esta observación —en la tesis, en la UI o ante un revisor— usa **esta
formulación y no otra**, porque es la única enteramente demostrada:

> **Aplicando dos métodos independientes de identificación territorial (registro de topónimos
> y detección de marcadores espaciales), únicamente entre el 1,1% y el 1,3% de las filas del
> POA 2023-2026 del GAD Montecristi contienen una referencia territorial subcantonal explícita
> que permita reconstruir el lugar efectivo de ejecución del gasto.**

## 9 · El hallazgo que trasciende el 1%

> **El 1% es el resultado, no el hallazgo.** *(precisión de la asesoría · 2026-07-29)*
>
> El hallazgo es un principio metodológico que trasciende Montecristi y trasciende Ecuador:
>
> **La verificabilidad de una política pública depende de la ESTRUCTURA SEMÁNTICA del
> instrumento, no únicamente de su disponibilidad documental.**
>
> El 1% simplemente lo demuestra empíricamente. Un instrumento puede estar publicado, ser
> legible y estar completo, y aun así no habilitar verificación alguna.

## 10 · Protocolo de elevación — qué NO se puede afirmar todavía

**No se afirma nada sobre "el instrumento nacional" con un solo municipio.** Con un caso
siempre cabe la particularidad local. La secuencia obligatoria antes de elevar el hallazgo:

| Paso | Alcance | Estatus de la afirmación |
|---|---|---|
| **1 · Montecristi** | observación | ✅ **hecho** — hallazgo local, plenamente demostrado |
| **2 · Segundo GAD** | replicación | ⛔ **BLOQUEADO por R-E** — no antes de cerrar Montecristi |
| **3 · Tercer GAD, otra provincia** | confirmación | ⏳ pendiente |
| **4 · Elevación** | afirmación sobre el **diseño del instrumento** | ⛔ **prohibido hasta completar 1-3** |

### Hipótesis H-ARQ-01 · Opacidad Estructural del Registro

El patrón se observó ya en **dos instrumentos distintos del mismo GAD** —el POA no localiza el
gasto (1,1%), el PP no desagrega montos por prioridad— lo que sugiere una propiedad de la
arquitectura documental y no un defecto puntual. **Sugiere; no demuestra.** Se registra con
estatus de hipótesis, no de hallazgo:

> **H-ARQ-01** — *La ausencia sistemática de metadatos de localización territorial y de
> desagregación financiera en los instrumentos locales no es un descuido administrativo de un
> GAD, sino una propiedad del diseño de la arquitectura documental pública ecuatoriana.*

| Campo | Valor |
|---|---|
| **Estatus** | ⏳ **hipótesis de trabajo** — NO conclusión |
| **Evidencia a favor** | 2 instrumentos · 1 municipio (POA · PP) |
| **Por qué no basta** | ambos del **mismo GAD**: puede ser una práctica local |
| **Condición de contraste** | otro GAD sometido **al mismo protocolo**, con su instrumento en UDC-I |
| **Bloqueada por** | **R-E** — no antes de cerrar Montecristi |
| **Registro** | **C10 · incertidumbre estructurada** |

Hasta el paso 4, la formulación admisible es una **pregunta abierta**, no una conclusión:
*¿es un defecto de este municipio o una propiedad del instrumento?* Registrarla como pregunta
—y no como hallazgo— es un caso **C10 · Metacognición institucional** (Modelo Causal §XV): lo
que QUIRA lleva a la red académica **son sus incertidumbres estructuradas, no sus resultados**.

---
*OBS-020 · Dylus Lab © 2026 · hallazgo de Javo, medido por QUIRA · deriva de OBS-019.*
