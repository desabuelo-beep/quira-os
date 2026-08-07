---
id: ADR-043
authority:
  parent: ADR-041
  constitution_articles: [1, 2, 3, 4, 5]
  type: ARQUITECTONICA
status: APROBADO — sellado por Javo (2026-08-07)
fecha: 2026-08-07
---

# ADR-043 · La familia QUIRA · qué hace que algo sea una QUIRA

> **Contexto.** Javo (2026-08-07): *"¿o son muchas QUIRAs y deberíamos definir los alcances
> de cada una para establecer la familia real?"*. La pregunta correcta no es cuántas hay,
> sino **qué tiene que demostrar una propuesta para ser una**. Este ADR fija esa prueba, y
> la aplica a lo que existe hoy.
>
> ⚖️ **Alcance.** Este ADR **no crea productos nuevos**: establece el criterio por el cual una
> capacidad futura puede ser reconocida como producto QUIRA — y por el cual otra puede ser
> rechazada por ser una vista.

## 1 · El problema que se resuelve

El canon acumuló nombres sin fijar fronteras, y eso produjo contradicciones reales:

- **ADR-024** daba a Impact y a Cooperación **el mismo destinatario** (BID, CAF, PNUD),
  siendo dos productos distintos.
- **ADR-041 §3-4** los fusionó en una sola entrada: *"QUIRA Cooperación / Impact"*.
- El código llevaba la clave `impact` con el nombre público «Cooperación» — subsanado el
  2026-08-07, con `impact` reservado.
- «QUIRA Institucional» nombraba a la vez **el ambiente de observación** y **el producto de
  gestión para el GAD**. Un reemplazo automático confundió ambos y llegó a escribir que el
  GAD *"opera el Observatorio como herramienta diaria"* — invirtiendo la Tesis.

Ninguno de esos errores fue de implementación: todos vinieron de no tener un criterio para
decir qué es y qué no es una QUIRA.

## 2 · Tres niveles que no deben confundirse

**QUIRA es un sistema de conocimiento territorial verificable**, no una colección de
sistemas que comparten nombre. Dentro de él hay tres clases de cosa:

| Nivel | Qué es | Elementos |
|---|---|---|
| **Adquisición** | producen evidencia y la incorporan al sistema | Observatorio · QUIRA Ciudadana |
| **Núcleo** | custodia, integra y calcula | Corpus + Grafo · MATRIZ_CANONICA · Gold Master · DOM · Centro |
| **Productos** | explotan ese conocimiento con contratos de salida distintos | Institucional · Cooperación · Impact · Economic |

Y dos cosas que **no son ninguna de las tres**:

- **Capas transversales** — QUIRA IA y GeoTwin. Atraviesan todos los productos: la primera
  explica, la segunda representa. No tienen usuario propio ni contrato de salida propio.
- **Mantenimiento** — Operaciones. Sostiene la máquina; no es producto (ADR-041 §2).

> **Una familia de productos no implica una familia de sistemas.** Seis productos pueden
> vivir sobre un único núcleo sin que existan seis motores ni seis verdades.

## 3 · La prueba de existencia — cuatro dimensiones y un gate

Una propuesta debe demostrar las **cuatro** para ser producto:

| # | Dimensión | Pregunta |
|---|---|---|
| 1 | **Misión** | ¿qué trabajo distinto realiza? |
| 2 | **Usuario y contrato** | ¿quién lo usa y bajo qué relación? |
| 3 | **Contrato de salida** | ¿qué entrega que ningún otro entrega? **Decisiva.** |
| 4 | **Promesa y frontera** | ¿qué puede prometer legítimamente, y qué NO puede hacer? |

Y después el **gate 5 · sostenibilidad**, que no es una dimensión más:

> Si no puede operar y financiarse de forma repetible, **no es todavía un producto
> consolidado**: es un experimento, un prototipo o una línea futura.

El gate existe porque QUIRA se financia sola. Un producto cuya operación no se puede pagar
no es un producto: es una aspiración con nombre. Es el mismo criterio que ADR-042 §4 aplica
al costo por corrida — *un método que no se puede repetir no es un método*.

### Las tres reglas que el test protege

> **1 · Una QUIRA no se distingue por los datos que consume, sino por el contrato de salida
> que establece con su usuario.**
>
> **2 · Compartir conocimiento, evidencia, motor o infraestructura NO convierte dos
> productos en uno. Compartir únicamente interfaz, permisos o presentación SÍ puede
> convertirlos en vistas.**
>
> **3 · Ningún producto QUIRA constituye una fuente independiente de verdad.** Todos
> explotan el conocimiento producido y trazado por el sistema común.

La primera es la que evita el error más caro. Cooperación e Impact pueden leer exactamente
la misma evidencia sobre salud institucional de un municipio: uno entrega una lectura de
elegibilidad, el otro el conjunto de datos y el método para reproducirlo. **Mismo
conocimiento, distinto producto.**

## 4 · La familia, aplicando la prueba

| Producto | Misión | Usuario | Contrato de salida | Gate |
|---|---|---|---|---|
| **QUIRA Institucional** | gestionar con evidencia | el GAD (alcaldía, técnicos, planificación) | herramientas de gestión, seguimiento y trazabilidad interna | ⏳ licencia — modelo por definir |
| **QUIRA Cooperación** | hacer financiable una intervención | bilaterales · multilaterales · banca de desarrollo | elegibilidad, alineación, expediente y seguimiento de lo colocado | ⏳ ingreso por operación, alto trabajo humano |
| **QUIRA Impact** | abrir el conocimiento a escrutinio | academia · observatorios · investigadores | datos, series, metodología y trazabilidad reproducible | ✅ costo marginal bajo, ingreso recurrente |
| **QUIRA Economic** | orientar el desarrollo económico | quien decide inversión en el territorio | inteligencia económica territorial | ❌ **no pasa el gate todavía** — línea futura |

**Economic no se elimina y no se fusiona con Cooperación.** Preguntan cosas distintas: una,
*¿qué necesita desarrollar este territorio?*; la otra, *¿qué instrumento puede financiarlo?*
Pasa las dimensiones 1 a 4 pero no el gate 5 —no está definido quién paga ni cuánto cuesta—,
así que queda como **línea futura**, no como producto consolidado. Esa, y no la madurez
técnica, es la razón real de que esté en Fase 3.

### Lo que NO son — la cuarta dimensión, escrita

- **Impact NO es un think tank.** Un think tank investiga, interpreta, toma posición y
  recomienda. Impact hace lo contrario: no produce la conclusión, **produce las condiciones
  para que otros produzcan conclusiones verificables**. La diferencia no es de estilo: el día
  que Impact emita juicio propio sobre la gestión de un municipio, QUIRA pasa a ser un actor
  con posición y cualquier señalado podrá alegar parte interesada. Se perdería lo que sostiene
  todo lo demás.
- **Impact NO genera evidencia primaria** ni sustituye al Observatorio.

  > **Impact puede habilitar investigación aplicada, pero no sustituye la función
  > epistemológica del investigador.**
  >
  > Si una universidad publica un estudio con datos de QUIRA, el mérito interpretativo es de
  > quien investiga — y la responsabilidad por la interpretación, también. QUIRA entrega
  > evidencia, método, trazabilidad y reproducibilidad; **no entrega opinión, ni ranking
  > ideológico, ni juicio político.** La distinción protege al investigador, que conserva su
  > autoría, y a Dylus Lab, que no responde por conclusiones ajenas.
- **Cooperación NO decide financiamiento** ni gestiona fondos: informa la decisión de quien
  la toma.
- **Institucional NO convierte al GAD en cliente de la observación** (ADR-041 §4-ter). Puede
  serlo de una herramienta de gestión; el GAD sigue siendo sujeto observado.

  > **El usuario institucional puede ser el GAD como entidad de gestión, pero nunca como
  > sujeto que controla, condiciona o modifica la observación pública que realiza el
  > Observatorio.**
  >
  > Es la cláusula que hace viable el modelo mixto. QUIRA observa al GAD y a la vez puede
  > venderle herramientas para gestionarse: sin esta línea, un municipio con licencia tendría
  > una palanca sobre lo que se publica de él, y la independencia del Observatorio quedaría
  > en entredicho ante cualquier tercero. **Gestionar ≠ influir en la observación.** La
  > relación comercial se establece sobre la herramienta de gestión, jamás sobre el alcance,
  > el método o el resultado de la observación.
- **Ningún producto certifica verdad.** Certifican verificabilidad, con la escala de cinco
  niveles del canon.

## 5 · El Centro no es la puerta obligatoria

ADR-042 fijó que el Centro de Inteligencia Territorial es **la capa de consulta y
articulación**. Este ADR añade la consecuencia:

> **El Centro organiza el conocimiento para ser consultado; no monopoliza el acceso a él.**

Los productos **no cuelgan** del Centro. **El Centro y los productos son capas paralelas de
explotación del mismo conocimiento** —no son de la misma naturaleza: el Centro no es un
producto, es la capa de consulta— y cada uno entra por donde su contrato lo exige.

```
                    GOLD MASTER
                         │
                         ▼
        CONOCIMIENTO TERRITORIAL VERIFICABLE
                         │
              ┌──────────┴──────────┐
              │                     │
            CENTRO              PRODUCTOS
        capa de consulta    contratos especializados
```

| Producto | Entra por |
|---|---|
| Institucional · Cooperación · Economic | Centro — necesitan conocimiento interpretado |
| **Impact** | **corpus y DOM directamente**, con trazabilidad completa |

La excepción de Impact no es una concesión: es su razón de ser. Obligar a un investigador a
pasar por una capa de interpretación pensada para lectura humana pondría un intérprete entre
él y el dato — exactamente lo que Impact existe para evitar. Y convertiría al Centro en
cuello de botella de todo el sistema.

## 6 · Consecuencias

| # | Qué se toca | Estado |
|---|---|---|
| 1 | `NOMENCLATURA_CANONICA §2` — `impact` reservado, `coop` activo | ✅ hecho (2026-08-07) |
| 2 | Portada — publicar la familia con entradas y productos separados | ⏳ tras el sello |
| 3 | `ADR-024` §Capa C — Impact y Cooperación con el mismo destinatario | ⏳ **ADR-044 de rectificación** — NO se edita |
| 4 | Ambiente para `QUIRA Institucional` como producto de gestión | ⛔ no existe; depende del modelo de licencia |

### 6-bis · Por qué ADR-024 no se corrige editándolo

`ADR-024 §Capa C` da a Impact y a Cooperación el mismo destinatario. Este ADR dice lo
contrario, y la contradicción es real. **Pero no se resuelve reescribiendo el documento
anterior.**

Un ADR sellado registra una decisión tomada con el vocabulario y la información de su
momento. Cambiarle las palabras no corrige un error: **borra la evidencia de que se cometió**,
y con ella la posibilidad de entender por qué se decidió así.

La lección es reciente y costó cuatro reversiones: el 2026-08-07 un reemplazo automático de
«QUIRA Institucional» por «Observatorio» alcanzó a ADR-024, ADR-026 y al propio ADR-041, y
produjo afirmaciones falsas —entre ellas que el Observatorio era a la vez entrada de Fase 1
y consumidor de Fase 2—. La contradicción no estaba en los ADR: la introdujo la edición.

Forma correcta: **ADR-044 · Rectificación de taxonomía de productos heredada**, que declare
expresamente qué parte de ADR-024 queda superada y por qué. La trazabilidad documental vale
más que la pulcritud del texto viejo.

## 7 · Lo que este ADR NO decide

- **El modelo de negocio de cada producto.** Fija que la sostenibilidad es condición, no cuál
  es el precio ni el instrumento.
- **Cuándo se construye cada uno.** El orden de fases lo fija ADR-041 §4.
- **El estatuto del aporte ciudadano** — sigue abierto en ADR-041 §6.
- **Si Economic termina absorbido.** Se revisa cuando tenga usuario y costo conocidos; hoy no
  hay base para eliminarlo ni para consolidarlo.

---
*ADR-043 · Dylus Lab © 2026 · propuesto por la dirección técnica sobre la duda de Javo y la
revisión del colega · deriva de ADR-041.*
