---
id: ADR-049
authority:
  parent: ADR-023
  constitution_articles: [1, 2, 3, 4]
  type: ARQUITECTONICA
status: PROPUESTO — pendiente de sello (ADR-035 §5)
fecha: 2026-08-12
---

# ADR-049 · Gramática visual de la demostrabilidad

> **Qué decide.** Cómo QUIRA representa gráficamente un hallazgo: qué tres formas existen, qué
> vocabulario de estados usan y —lo decisivo— **cómo se dibuja lo que no se puede demostrar**.
>
> **Qué NO decide.** No define paleta, tipografía ni componentes. No autoriza a graficar nada que
> el motor no haya establecido. No crea métricas.

## 1 · El problema, y no es estético

Una tabla que omite una fila se nota. **Una gráfica que omite un eslabón, no**: el ojo completa la
línea. Dibujar

```
PDOT ──────────────────────▶ DEVENGADO
```

cuando entre ambos falta el vínculo demostrable **no es una simplificación: es una afirmación
falsa**, y más persuasiva que cualquier texto porque no parece una afirmación.

Esto no es hipotético. La curación de agosto 2026 produjo hallazgos cuya naturaleza es
exactamente esa: cadenas que llegan hasta cierto punto y **no más allá**. Presentarlos como
continuidad destruiría el hallazgo.

## 2 · Las dos reglas fundacionales

> **Regla 1 — La gráfica nunca puede saber más que el estado canónico autorizado por el Gold
> Master, los motores y sus capas derivadas.**
> **Regla 2 — Lo que no puede demostrarse debe permanecer visible como no demostrable.**
> *(formulación del colega, 2026-08-12 — se adoptan literales)*

La Regla 1 nació como *«nunca más que el Gold Master»* y hubo que ampliarla el mismo día: el motor
fija el valor, pero **el estado de demostrabilidad, la procedencia y el límite de captura los
establecen otros componentes autorizados**, y con la formulación estrecha habrían quedado fuera.

La primera impide que QUIRA **invente**. La segunda impide que QUIRA **esconda**. Juntas producen
algo infrecuente en un sistema de información pública: **una visualización capaz de decir «no sé».**

### VIS-INV-001 · invariante arquitectónica

> **Ninguna representación visual puede introducir una entidad, relación, estado, valor, causalidad
> o grado de certeza que no exista previamente en el estado canónico o en una capa derivada
> autorizada por el motor correspondiente.**

*(formulación endurecida por el colega, 2026-08-12)*. La versión anterior decía «del Gold Master» y
**se quedaba corta**: el motor fija el valor, pero el estado de demostrabilidad, la procedencia, el
límite de captura y la distinción hecho/inferencia los establecen otros componentes autorizados.
Escrito de aquel modo, alguien podría objetar *«ese dato no está en el Excel, no puede aparecer»* —
cuando sí puede, **si un motor autorizado lo produjo**. Y a la inversa, cerraba mal la puerta de
*«como sería útil mostrarlo, lo calculamos aquí»*.

Y su consecuencia, que resume mejor que ninguna otra frase lo que esta capa protege:

> **Una visualización de QUIRA no puede ser fuente de una afirmación que el estado canónico no
> pueda reconstruir.**

### VIS-INV-002 · la caja no confiere hechos

> **Una etiqueta visual que describa una relación, causa, migración, efecto o significado que no
> haya sido producida por un motor autorizado deberá clasificarse como interpretación, y nunca
> podrá presentarse con la misma gramática visual que un hecho documental.**

*(propuesta del colega, 2026-08-12 — adoptada)*. VIS-INV-001 impide que el dibujo **invente datos**.
Ésta cierra un agujero distinto y más sutil:

> **que el dibujo convierta una interpretación humana en un hecho por el solo acto de ponerla dentro
> de una caja.**

No es hipotético: ocurrió el mismo día en que se escribió este ADR. El primer objeto canónico
rotulaba una rama como «TRAZABILIDAD DESVIADA» y afirmaba que *«la trazabilidad no desapareció:
cambió de destino»*. El hecho medido era otro —95 de 101 actividades con código orgánico, 0 con
meta—; la lectura la puso el analista. **Con el mismo trazo, el mismo marco y el mismo peso
tipográfico que las cifras verificadas.**

Un límite honesto de estas invariantes: `verificar_procedencia` detecta un elemento sin dueño, pero
**no habría detectado esa frase**, porque tenía dueño aparente. La distinción hecho/interpretación
todavía depende de revisión humana. Conviene saberlo antes de escalar a doce dominios.

### VIS-INT-001 · integridad de procedencia visual

> **Si un elemento del dibujo no tiene propietario canónico, ese elemento no puede existir.**

Para cada elemento visual debe poder responderse: qué dato representa · de qué estado proviene ·
qué componente lo produjo o autorizó · cuál es su procedencia · qué estado tiene · qué
transformación visual se le aplicó · si esa transformación altera su significado. Y a la pregunta
*«¿hay información visual sin propietario canónico?»* la respuesta debe ser **no**.

Es una regla más fuerte que «la gráfica no calcula»: obliga a que cada cifra pueda **señalar de
quién es**. Implementada en `scripts/vis/objeto_canonico.py::verificar_procedencia`, que aborta la
generación si algún elemento queda huérfano.

| Elemento | Propietario |
|---|---|
| importes y proporciones | Motor Matemático · estado canónico |
| cadenas y vínculos entre instrumentos | Motor de Grafos · capa derivada |
| `sin_evidencia`, `no_reconciliado`, límites de captura | validación de evidencia |
| procedencia, SHA, corte, conteos | registro de procedencia |
| relaciones causales | **Motor Causal — y sólo si las estableció** |

No es una recomendación de estilo: es una restricción de flujo. La información viaja en un solo
sentido y **la gráfica no vuelve hacia arriba a buscar lo que le falta**:

```
fuentes → extracción → validación → reconciliación → GOLD MASTER → visualización
```

Si un componente visual necesita un dato que el motor no produjo, **ese dato no existe** — no se
calcula en la capa gráfica, no se pide a otra fuente, no se estima. Se dibuja su ausencia.

De ahí, sin margen de interpretación:

| Si el motor dice | La gráfica debe mostrar |
|---|---|
| `validado` | continuidad |
| `no_reconciliado` | **tramo roto**, no ausencia de tramo |
| `sin_evidencia` | vacío **declarado**, no cero |
| `ejecución_no_atribuible` | vínculo **débil y marcado**, no vínculo pleno |
| inferencia | **distinguible** de hecho documental |
| contradicción | **ambas** ramas visibles |

Y su consecuencia operativa: **una visualización no puede computar, promediar ni interpolar.**
Si necesita un número que el motor no produjo, el número no existe — no se calcula en la capa
gráfica (Regla de Oro 4; ADR-023).

## 3 · Las tres formas canónicas

Tres, no veinte. Cada una responde una pregunta distinta y **no son intercambiables**.

### I · Trazabilidad — «¿por dónde viaja la evidencia?»

La cadena intersistémica completa, con el estado de cada tramo:

```
PDOT ─▶ POA ─▶ PAC ─▶ SERCOP ─▶ cédula ─▶ devengado
```

Cada arista lleva su estado y su procedencia (archivo · hoja · fila · período). **Una arista sin
procedencia no se dibuja.**

### II · Ruptura — «¿dónde se interrumpe?»

La misma cadena, resaltando el punto de corte y **conservando visible lo que sí se demostró**. El
hallazgo no es «falta información»: es *hasta aquí sí, desde aquí no*.

### III · Causal — «¿qué significa esa ruptura?»

Mecanismo y consecuencia, no opinión:

```
desaparece la META del instrumento
        ↓
el gasto no puede vincularse al resultado esperado
        ↓
la articulación estratégica permanece demostrable
        ↓
la efectividad operacional no es auditable documentalmente
```

⚠️ Cada eslabón causal exige respaldo. **Una cadena causal sin evidencia por tramo es una opinión
dibujada**, y eso es peor que una opinión escrita.

### Relación con los cinco motores (ADR-031) — la puerta que hay que cerrar

**La capa visual no es un motor.** Un motor produce conocimiento; ésta proyecta el que ya existe.
No compite con los cinco: los explota. Pero la forma III abre un riesgo que conviene clausurar por
escrito, porque la redacción anterior lo permitía:

> **La gráfica causal no deriva causalidad: representa la que el Motor Causal ya estableció.** Si
> ningún motor estableció el vínculo, **la forma III no puede dibujarse** — ni «provisionalmente»,
> ni «como hipótesis visual».

Dibujar una flecha causal que ningún motor produjo sería construir un motor paralelo por la vía
gráfica, que es exactamente lo que la Regla de Oro 4 prohíbe. Mientras el Motor Causal siga en
laboratorio y no en runtime (ADR-031 §3), **sólo las formas I y II son admisibles en producto**; la
III se limita a documentación interna y lleva marca visible de hipótesis.

## 4 · Vocabulario visual de estados

Los estados provienen del motor y de la capa derivada; la gráfica **no inventa ninguno**:

**La visualización no interpreta silenciosamente ningún estado.** Cada uno tiene una lectura fija y
—esto es lo decisivo— **declara a quién pertenece la ruptura**:

| Estado del motor | Lectura visual | Ruptura atribuible a | Nunca |
|---|---|---|---|
| `validado` | conexión demostrada | — | — |
| `parcialmente_validado` | conexión degradada | — | como plena |
| `requiere_revision` | conexión advertida | **QUIRA** | como demostrada |
| `no_reconciliado` | conexión rota | **QUIRA** (procedimiento) | como incumplimiento |
| `sin_evidencia` | vacío declarado | **observado** | como cero |
| `no_observable` | zona no observable | ninguno | como ausencia |
| `ejecución_no_atribuible` | vínculo débil, punteado | — | como atribuido |
| `extraccion_corrupta` | ruptura **de QUIRA** | **QUIRA** | como carencia del GAD |
| `fuente_no_accesible` | ruptura **de la fuente** | **fuente externa** | como ausencia |
| `contradiccion` | bifurcación, ambas ramas | — | resuelta a una rama |

⛔ **Ninguna caja puede rotularse «no verificable», «sin datos» ni «no disponible».** Esas fórmulas
colapsan cuatro situaciones que no son la misma —`sin_evidencia` · `no_reconciliado` ·
`fuente_no_accesible` · `extraccion_corrupta`— y reintroducen por la puerta del texto el binario que
esta gramática existe para eliminar. **Se declara cuál de las cuatro es, y por qué.**

> **La trampa más peligrosa de una plataforma de inteligencia pública es que el diseño gráfico
> convierta un «no sé» en un «no existe».** La columna de atribución existe para impedirlo: quien
> mira debe poder distinguir, sin leer una nota al pie, si la cadena se rompió en el municipio, en
> la fuente o en nosotros.

> **`extraccion_corrupta` y `fuente_no_accesible` señalan a QUIRA, no al municipio.** Deben verse
> distintos de todo lo demás: son límites del observador. Confundirlos con hallazgos es la falla
> que ADR-042 §6 prohíbe, y en una gráfica sería indetectable para el lector.

## 5 · Lo que esta capa no es

- **No es un tablero de indicadores.** Un tablero muestra el resultado; esto muestra **cómo se
  construyó y dónde dejó de ser demostrable**.
- **No es una capa decorativa sobre el motor.** Es **otra forma de consultar el mismo motor**
  (ADR-023: un solo motor, una sola verdad, múltiples explotaciones).
- **No cruza la frontera de lenguaje.** Rige el Firewall: fuera no aparecen `ICPI`, `TGI`, `Ti`,
  `QTMP`, `H01`-`H99` ni identificadores internos. La gramática es visual, **no una ventana al
  interior**.

## 6 · Relación con la BRN — un matiz que ya se equivocó una vez

Javo (2026-08-12): *«todo con su BRN diría yo para la garantía y certeza»*. El propósito es
correcto y el orden importa: **ADR-038 fija que la BRN traza el motor, no lo alimenta.**

> Las gráficas **no derivan de la BRN**. Derivan del motor y de la capa derivada; **la BRN explica
> por qué esa cadena es exigible** —qué norma la sostiene, con qué SHA—.

La flecha va del hallazgo a la norma, nunca al revés. El director invirtió esta relación en el
borrador de ADR-047 y hubo que corregirlo; queda escrito para no repetirlo.

## 7 · Caso de prueba — ya medido, no supuesto

El hallazgo de 2026 (OBS-027) es el banco de pruebas de las tres formas:

```
PDOT ─▶ objetivo estratégico ─▶ PAI/POA ─▶ partida ─▶ cédula ─▶ devengado
           9 objetivos            95 filas    27       abril      8/9 ✓

        ╌╌▶ META ✗ ╌╌▶ indicador ✗ ╌╌▶ resultado ✗
             0/66          0/66         no auditable
```

Si las tres formas representan **esto** sin mentir —sin insinuar continuidad donde hay corte y sin
convertir el corte en un cero—, la gramática sirve. Si no, no sirve, y da igual lo bien que se vea.

## 8 · Invariantes

1. La gráfica **nunca sabe más que el motor**.
2. Ningún cálculo nace en la capa visual.
3. La ausencia de evidencia **se dibuja**; jamás se omite.
4. `no_reconciliado` **nunca** se representa como incumplimiento.
5. Los límites propios (`extraccion_corrupta`, `fuente_no_accesible`) se distinguen de los
   hallazgos sobre el observado.
6. Toda arista lleva procedencia; sin procedencia no hay arista.
7. Tres formas canónicas. Añadir una cuarta exige ADR.
8. La inferencia se distingue del hecho documental **siempre**.

## 9 · Lo que queda abierto

- Prototipo de las tres formas sobre el caso 2026, **antes** de tocar la interfaz existente.
- Fuente de datos: la capa derivada (`data/pdot/cruce_poa_cedula.json`) ya conserva estados y
  procedencia; no hace falta estructura nueva para empezar.
- Reutilización en los 12 dominios y los 222 GAD: **sólo después** de que las tres funcionen en uno.

---
*ADR-049 · Dylus Lab © 2026 · propuesto por Javo · regla rectora del colega, adoptada literal.*
