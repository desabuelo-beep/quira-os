---
id: ADR-057
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: APROBADO — sellado por Javo (2026-09-06)
fecha: 2026-09-06
decision_gm_omega: D4
---

> ## 🔏 SELLO · 2026-09-06
>
> **Se mantiene PROVISIONALMENTE el piso `C_i ≥ 0,50`, SIN afirmar que esté teóricamente
> fundamentado, y queda MANDATADO PARA REVISIÓN en `REARQUITECTURA`.**
>
> El sello **no convierte un `NO DETERMINABLE` en `DEMOSTRADO`**. La tesis sustantiva que el piso
> sostiene —que ninguna cantidad de infracciones puede destruir completamente la contribución de
> una unidad— queda **enunciada y abierta**, no acreditada.

# ADR-057 · `D4` — El piso mínimo de `C_i`

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

## Por qué este ADR es distinto de los demás

`D4` parece el más pequeño de los cinco —un número—, y es el que **afirma más**.

> El piso no es un parámetro técnico. Sostiene una **tesis sustantiva sobre la relación entre
> infracción y desempeño**: que incluso acumulando infracciones existe un mínimo de contribución
> institucional que debe preservarse.

Esa tesis puede ser correcta. Pero es una tesis, y hoy nadie la ha enunciado como tal.

---

## 1 · Decisión vigente

```
C_i = SI(INF-04 = 1; 0,50;
         SI(O(INF-01>0; INF-02>0; INF-03>0);
            MÁX(0,50; 1 − (INF-01×0,15 + INF-02×0,10 + INF-03×0,05));
            Ci_Manual_2025))
```

**`C_i` nunca baja de `0,50`**, ocurra lo que ocurra.

## 2 · Fenómeno que pretende representar

Que una infracción **degrada** la calidad del proceso orgánico, pero **no la anula**. Es decir:
una unidad sancionada sigue siendo una unidad que gestiona.

## 3 · Unidad afectada

La meta del PDOT, vía su unidad orgánica responsable.

## 4 · Evidencia que la sostiene

| Fuente | Qué dice |
|---|---|
| `GOLDMASTER_REFACTOR_MASTER_v2.0.md` | `DETECTAR: Ci_mínimo = 0 (debe ser 0.50)` · `Ci_mínimo = 0.50 (NUNCA 0)` |
| `H01` Sección L | `Ci = MÁX(0,50; 1,00 − Σ penalizaciones)` |
| `011-C3R` | entra en el mismo acto que el mecanismo y los pesos |

⚠️ **Dice «nunca 0». No dice por qué `0,50`.**

## 5 · Alternativas consideradas

| Alternativa | Qué implicaría |
|---|---|
| **piso `0`** | una acumulación de infracciones **podría anular** la meta |
| **otro piso** — `0,25`, `0,75` | misma tesis, distinta severidad máxima |
| **sin piso, con función asintótica** | degradación creciente que nunca llega a cero |

⚠️ **Ninguna consta como evaluada.** Y hay una divergencia latente: el glosario
`H02!Ci_Determinista` declara `MAX(…, 0)` — **piso cero** — mientras la Sección L declara
`MÁX(0,50; …)` (`D-013`).

## 6 · Qué está DEMOSTRADO

- El piso está implementado y es coherente entre la prescripción y la Sección L.
- **Consecuencia estructural**: con este piso, **`C_i` no puede anular una meta**. La anulación
  multiplicativa sólo puede venir de otro factor.
- Entró en el mismo acto de diseño que el mecanismo y los pesos (25→29-abr-2026).
- Y **cambia el rango respecto del constructo original**: la escala de `C_i` como imputabilidad
  orgánica tenía mínimo `0,75`; el mecanismo determinista admite `0,50`.

## 7 · Qué es INFERENCIA

Que `0,50` represente «la mitad de la calidad institucional preservada». El valor es redondo y
sugiere esa lectura; no consta declarada.

## 8 · Qué permanece NO DETERMINABLE

> **Qué propiedad del fenómeno justifica que ninguna infracción pueda reducir `C_i` por debajo
> de `0,50`.** `011-C3R` cerró: documentado, sin fundamento cuantitativo.

### ★ Y la pregunta real, que es más profunda que «¿por qué 0,50?»

> **¿Qué relación teórica existe entre una infracción normativa y la capacidad de una unidad de
> gestión para contribuir a la congruencia medida?**

El piso contiene una afirmación muy concreta, y hay que verla escrita:

> **Ninguna cantidad de infracciones contempladas por el mecanismo puede destruir completamente
> la contribución de la unidad.**

Eso **no se deriva de la matemática**. **Tampoco se deriva automáticamente de la presunción de
inocencia** —que justifica *empezar* en `1,00`, no *terminar* en `0,50`—. Y no basta invocar que
QUIRA evita el lenguaje acusatorio:

| Afirmación | Naturaleza |
|---|---|
| «QUIRA no declara culpabilidad» | principio de **lenguaje** (`Regla de Oro 2`) |
| «una infracción verificada nunca puede reducir `C_i` por debajo de `0,50`» | decisión sobre la **función de medición** |

**Son cosas distintas**, y la segunda necesita fundamento propio.

### La censura superior de la penalización

Hay una consecuencia estructural que conviene dejar explícita:

> El piso introduce una **censura superior de la penalización**. El sistema puede degradar `C_i`,
> pero existe un **límite estructural** a cuánto puede este factor afectar al índice —
> exactamente `0,50` de recorrido, la mitad del rango teórico.

Dicho de otro modo: por muchas infracciones que se registren, `C_i` **no puede** aportar menos de
la mitad. La capacidad punitiva del factor está acotada por diseño, y esa acotación no se declara
en ninguna superficie.

## 9 · Consecuencias de mantenerla

| | |
|---|---|
| 🔵 | **Efecto hoy: ninguno.** Sin infracciones registradas, el piso no se alcanza |
| ✅ | Protege contra una anulación por vía punitiva: coherente con la prohibición de lenguaje acusatorio (`Regla de Oro 2`) |
| ⚠️ | Pero también **acota cuánto puede penalizar el sistema**. Un GAD con desacato firme del CPCCS conserva la mitad de su `C_i` |
| 🔴 | Esa segunda consecuencia **no está declarada en ninguna parte** |

## 10 · Condición objetiva para revisarla

1. **Revisión obligatoria antes de registrar la primera infracción** — igual que `D3`.
2. Antes de esa revisión hay que resolver `D-013`: **si el piso es `0` o `0,50`**.
3. Y hay que **enunciar la tesis sustantiva** que el piso sostiene, para que pueda discutirse:
   *¿debe preservarse una contribución mínima aun con infracciones firmes acumuladas?*

---

## Dictamen que este ADR declara

> **`D4` · FUNDAMENTO NO DETERMINADO · LATENTE · Y SOSTIENE UNA TESIS SUSTANTIVA SOBRE LA
> RELACIÓN INFRACCIÓN ↔ DESEMPEÑO QUE REQUIERE FUNDAMENTO PROPIO.**

## ★ Marcado para `REARQUITECTURA` · probablemente la que más trabajo requiera

⚠️ **No porque sepamos que `0,50` está mal.** Precisamente porque **todavía no sabemos qué
afirmación sustantiva representa**.

La pregunta que emerge, y que ningún documento del sistema ha planteado:

> **¿Qué función debe cumplir una infracción normativa dentro de una medida de congruencia de
> gestión?**

Porque conceptualmente caben relaciones muy distintas, y elegir una es una decisión de diseño:

```
  infracción  →  deterioro del PROCESO
                 (la infracción dice algo sobre cómo se gestionó)

  infracción  →  deterioro PROPORCIONAL del desempeño
                 (ya asume una función de transferencia)

  infracción  →  pérdida MÁXIMA del 50 % de la contribución
                 (asume además una cota, y una cota concreta)
```

> **El `0,50` introduce una relación CUANTITATIVA que no está contenida en las premisas
> jurídicas.** `LOSNCP`, `NCI 406-01`, `COPFP` y `LO_CPCCS` definen **qué es** una infracción.
> Ninguna define **cuánto** debe descontar de una medida de congruencia, ni establece un tope.

Eso queda como **pregunta de diseño abierta**, no como defecto probado.

*Dylus Lab © 2026 · deriva de `GM-OMEGA_ICPI_DICTAMEN_011C4.md`*
