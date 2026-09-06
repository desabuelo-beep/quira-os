---
id: ADR-055
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: APROBADO — sellado por Javo (2026-09-06)
fecha: 2026-09-06
decision_gm_omega: D2
---

> ## 🔏 SELLO · 2026-09-06 — el más sustantivo de los cinco
>
> **Se adopta explícitamente la LECTURA `A`: el ICPI mide CONGRUENCIA ACREDITADA.**
>
> Con eso, `V_i = 0` queda declarado como **un resultado de auditoría**, no como una inferencia
> sobre el mundo: la unidad **no puede aportar congruencia acreditada**, y eso **no afirma que el
> fenómeno no ocurriera**.
>
> ⚠️ **Lo que este sello NO significa.** No declara que el ICPI sea una medida sustantivamente
> válida de toda la gestión pública. Elimina **una ambigüedad semántica fundamental** — nada más,
> y nada menos. La capa 3 de `011-C4` (validez sustantiva) sigue `NO DEMOSTRADA`.
>
> **Consecuencia operativa inmediata:** queda prohibido que cualquier superficie describa un
> `V_i = 0` como «la meta no se ejecutó» o «el fenómeno no ocurrió». Custodiado por
> `test_contrato_semantico_D2_congruencia_acreditada`.

# ADR-055 · `D2` — Qué significa la ausencia de evidencia

> **Propuesto por la dirección técnica tras `GM-Ω-011-C4`.** La IA propone; el humano valida
> (`ADR-035 §5`). **Este ADR no cambia el motor.**

## ⚠️ Qué significa —y qué no— sellar este ADR

```
NO DEMOSTRADO COMO NECESARIO  ≠  INCORRECTO  ≠  APROBADO
```

Este ADR **no razona** «como no encontramos evidencia de que la decisión sea incorrecta, se
mantiene». Eso sería exactamente lo contrario de la disciplina que `GM-Ω` construyó.

Y el sello **no significa** «la investigación demostró que esta decisión es verdadera». Significa:

> **La dirección decide conscientemente adoptar esta decisión, conociendo qué está demostrado,
> qué es inferencia y qué permanece abierto.**

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

### ⚠️ Y quién aplica esa regla hoy

> **La implementación actual aplica la regla `3`.** No es lo mismo que decir «QUIRA adopta la
> regla `3`»: mientras este ADR esté `PROPUESTO`, la regla está **implementada**, no **adoptada
> como decisión canónica**.

Lo que este ADR propone:

> **Declarar explícitamente que dicha regla opera bajo la lectura `A`: el ICPI mide congruencia
> acreditada.**

⚠️ Y declarar `A` **no demuestra que el ICPI sea un indicador sustantivamente válido**. Elimina
una ambigüedad semántica fundamental — nada más, y nada menos. La validez sustantiva sigue
`NO DEMOSTRADA` (`011-C4`, capa 3).

## 10 · Condición objetiva para revisarla

1. **Inmediata**: el sistema declara `A` o `B`. Declarar `A` **cierra esta decisión sin tocar el
   álgebra** — es la vía recomendada.
2. Si se declara `B`, la anulación debe rediseñarse: sería una inferencia prohibida.
3. `REARQUITECTURA` responde la pregunta que este ADR deja abierta y **no resuelve**:

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
