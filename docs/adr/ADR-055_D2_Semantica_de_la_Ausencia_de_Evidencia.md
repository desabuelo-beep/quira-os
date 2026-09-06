---
id: ADR-055
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: PROPUESTO — pendiente de sello de Javo
fecha: 2026-09-06
decision_gm_omega: D2
---

# ADR-055 · `D2` — Qué significa la ausencia de evidencia

> **Propuesto por la dirección técnica tras `GM-Ω-011-C4`.** La IA propone; el humano valida
> (`ADR-035 §5`). **Este ADR no cambia el motor.**

## Por qué éste es el más importante de los cinco

`011-C4` lo llamó *la sección decisiva*, y con razón: es el único de los cinco `ADR` que toca
**el principio rector del sistema**.

> *«La ausencia de evidencia es un RESULTADO de auditoría, nunca autorización para inferir
> hechos.»*

Y hoy, `V_i = 0` **anula la meta**. Hay que declarar si eso es un resultado o una inferencia.

---

## 1 · Decisión vigente

`V_i` entra **multiplicativamente** al producto. Si `V_i = 0`, entonces `J_i = 0`: la unidad
contribuye cero al numerador **y sigue pesando en el denominador**.

`V_i = 1,0` si los cuatro verificadores ≥ 1 · `0,5` si suman ≥ 2 · `0,0` si suman < 2
(`H13_VARIABLES_Vi`).

## 2 · Fenómeno que pretende representar

**Inmutabilidad documental**: que exista evidencia verificable en los silos independientes
—`SERCOP`, `eSIGEF`, `LOTAIP`, `CPCCS`—. La metodología la llama *«la variable más importante del
modelo»* y la funda en `CE 18` y `LOTAIP 7`.

## 3 · Unidad afectada

La meta del PDOT. Hoy: **6 de 25** con `V_i = 0`, arrastrando el **12,8 %** del peso.

## 4 · Evidencia que la sostiene

| Fuente | Qué aporta |
|---|---|
| `metodologia.docx` | el producto lógico `AND` tiene fundamento jurídico: si el contrato no está en SERCOP, viola `LOSNCP 22`; si no está en LOTAIP, viola `LOTAIP 7` |
| — | *«El algoritmo no castiga arbitrariamente al GAD; aplica las consecuencias de las normas ya vigentes.»* |

⚠️ Ese argumento sostiene **penalizar la no publicación**. No sostiene por sí solo que la
penalización deba ser **anulación total**.

## 5 · Alternativas consideradas

| Alternativa | ICPI resultante |
|---|---|
| **vigente** · anula, la meta sigue en el denominador | **27,4582 %** |
| «no acreditado» · la meta **sale del universo medido** | 31,4883 % · **+4,03 pp** |
| «se presume cumplida» · `V=1` | 31,8909 % · 🔴 **no defendible** |

⚠️ La tercera **contradice el principio rector** y se midió sólo para acotar el rango. Ninguna
consta como evaluada en su momento.

## 6 · Qué está DEMOSTRADO

- `V_i = 0` produce `J_i = 0` — propiedad del producto.
- Afecta a 6 de 25 metas y al 12,8 % del peso.
- **Toda** la anulación multiplicativa del motor proviene hoy de `V_i`.
- Tratar `V=0` como «no acreditado» movería el índice **+4,03 pp**: la semántica de la ausencia
  de evidencia tiene **elasticidad material medible** sobre el indicador.

## 7 · Qué es INFERENCIA

Que anular sea la traducción correcta del principio. Depende de qué mida el índice, y eso no
está declarado.

## 8 · Qué permanece NO DETERMINABLE

Cuál de las dos lecturas sostiene el sistema:

| | Lectura | Anular es… |
|---|---|---|
| **A** | el ICPI mide **congruencia acreditada** | un **RESULTADO** · lo no acreditado no cuenta como congruente |
| **B** | el ICPI mide **congruencia real** | una **INFERENCIA** · se trata la falta de evidencia como falta de cumplimiento |

Bajo `A` no hay contradicción con el principio rector. Bajo `B` sí.

## 9 · Consecuencias de mantenerla

**El índice mide dos cosas a la vez**: la gestión **y** la capacidad de documentarla.

Eso puede ser **intencional y legítimo** en un índice de congruencia *intersistémica* —donde la
trazabilidad **es** parte del fenómeno—. Pero entonces el sistema debe decir:

> ✅ «el ICPI mide **congruencia acreditada**»

y no:

> 🔴 «el ICPI mide la congruencia real de la gestión»

⚠️ Y las tres proposiciones no pueden confundirse:

```
  1. «el fenómeno NO OCURRIÓ»              afirmación sobre el mundo
  2. «no hay evidencia suficiente»         sobre el estado del conocimiento
  3. «la unidad no puede contribuir»       regla metodológica
```

La `3` es legítima. **No es consecuencia lógica de la `2`.** Y `V_i = 0` **no significa que el
fenómeno no ocurriera**: significa que, bajo esta arquitectura, la unidad no puede aportar
congruencia **acreditada**.

## 10 · Condición objetiva para revisarla

1. **Inmediata**: el sistema declara `A` o `B`. Declarar `A` **cierra esta decisión sin tocar el
   álgebra** — es la vía recomendada.
2. Si se declara `B`, la anulación debe rediseñarse: sería una inferencia prohibida.
3. `QUIRA-NEXT` responde la pregunta que este ADR deja abierta y **no resuelve**:

> ¿Debe `V_i` estar **embebida multiplicativamente** en un único ICPI, o existir **además** como
> una medida explícita e independiente de **acreditabilidad**?

---

## Dictamen que este ADR declara

> **`D2` · DEFENDIBLE BAJO LA LECTURA «CONGRUENCIA ACREDITADA». EL SISTEMA DEBE DECLARAR CUÁL
> SOSTIENE.**
>
> La diferencia no está en la fórmula: está en **lo que el sistema afirma que el número
> significa**.

*Dylus Lab © 2026 · deriva de `GM-OMEGA_ICPI_DICTAMEN_011C4.md`*
