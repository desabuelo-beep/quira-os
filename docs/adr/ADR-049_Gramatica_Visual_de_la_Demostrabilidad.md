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

## 2 · La regla rectora

> **La gráfica nunca debe saber más que el Gold Master.**
> *(formulación del colega, 2026-08-12 — se adopta literal)*

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

## 4 · Vocabulario visual de estados

Los estados provienen del motor y de la capa derivada; la gráfica **no inventa ninguno**:

| Estado | Trazo | Nunca |
|---|---|---|
| `validado` | continuo | — |
| `parcialmente_validado` | continuo atenuado | como pleno |
| `no_reconciliado` | **cortado**, con marca | como cero |
| `sin_evidencia` | vacío rotulado | omitido |
| `ejecución_no_atribuible` | punteado | como atribuido |
| `extraccion_corrupta` | marca de defecto **propio** | como carencia del GAD |
| `fuente_no_accesible` | marca de captura | como ausencia |
| `contradiccion` | bifurcación | resuelta a una rama |

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
