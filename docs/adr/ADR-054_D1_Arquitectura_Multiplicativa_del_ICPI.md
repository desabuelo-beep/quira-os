---
id: ADR-054
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: PROPUESTO — pendiente de sello de Javo
fecha: 2026-09-06
decision_gm_omega: D1
---

# ADR-054 · `D1` — La arquitectura multiplicativa del ICPI

> **Propuesto por la dirección técnica tras `GM-Ω-011-C4`.** La IA propone; el humano valida
> (`ADR-035 §5`). **Este ADR no cambia el motor**: declara una decisión que hasta hoy operaba
> sin declararse.

## ⚠️ Qué significa —y qué no— sellar este ADR

```
NO DEMOSTRADO COMO NECESARIO  ≠  INCORRECTO  ≠  APROBADO
```

Este ADR **no razona** «como no encontramos evidencia de que la decisión sea incorrecta, se
mantiene». Eso sería exactamente lo contrario de la disciplina que `GM-Ω` construyó.

Y el sello **no significa** «la investigación demostró que esta decisión es verdadera». Significa:

> **La dirección decide conscientemente adoptar esta decisión, conociendo qué está demostrado,
> qué es inferencia y qué permanece abierto.**

Institucionalmente eso es mucho más fuerte, y es lo que los diez campos hacen posible.

## Por qué existe este ADR

`011-C4` estableció que **cinco decisiones sostienen el ICPI y ninguna está declarada como
decisión** — se presentan como si fueran propiedades del fenómeno. Ésta es la primera.

⚠️ Declarar no es justificar. Un ADR que sólo explicara por qué la decisión está bien sería
una **justificación retrospectiva**. Los diez campos obligan a separar lo demostrado de lo
inferido y de lo que sigue abierto.

---

## 1 · Decisión vigente

```
J_i = P_i × R_i × V_i × E_i × T_i × C_i
ICPI = Σ J_i / Σ (P_i × R_i)
```

La contribución de cada unidad es el **producto** de sus seis dimensiones. Un factor en cero
anula la unidad completa, con independencia del valor de los otros cinco.

Implementada en `H12!J{n}` (`=B*C*D*E*F*I`) y `H12!B33`. **Inmutable** por `Regla de Oro 1`.

## 2 · Fenómeno que pretende representar

**Congruencia programática e intersistémica**: si la cadena
`programa → norma → verificación → ejecución → tiempo → trazabilidad` **se sostiene entera**.

La lectura que la multiplicatividad encarna: *una cadena de congruencia en la que cualquier
eslabón roto invalida el conjunto.*

## 3 · Unidad afectada

La meta del PDOT identificada por su ID canónico — 25 unidades del universo operacional
(`ADR-036`). ⚠️ La unidad **no está declarada en el canon** (`011-A2`, abierta), lo que acota el
alcance de las afirmaciones pero no la validez del cálculo.

## 4 · Evidencia que la sostiene

| Fuente | Qué aporta |
|---|---|
| `metodologia.docx` (25-mar-2026) | define las seis variables y su composición |
| `007-D` | la multiplicatividad es **la decisión más consecuente del motor**: Δ ≈ 51,26 pp |
| `011-C3R` | la arquitectura no derivó: se estableció y se mantuvo |

## 5 · Alternativas consideradas

| Alternativa | Qué cambiaría |
|---|---|
| **media ponderada** | ningún factor anularía; degradación gradual |
| **producto con piso** | anulación acotada, como ya hace `C_i` con su `0,50` |
| **producto parcial** | sólo algunos factores multiplican; otros suman |
| **panel multidimensional** | sin agregación a un número único |

⚠️ **Ninguna consta como evaluada y descartada.** No hay documento que compare alternativas.

## 6 · Qué está DEMOSTRADO

- La multiplicatividad produce **anulación total** ante un solo factor en cero — es su definición.
- Hoy afecta a **6 de 25 metas**, que arrastran el **12,8 %** del peso del denominador.
- Toda la anulación proviene **exclusivamente de `V_i`**: ningún `E_i`, `T_i` ni `C_i` vale cero.
- Es la decisión de mayor efecto medido sobre el resultado (`007-D`).

## 7 · Qué es INFERENCIA

- Que la multiplicatividad **represente** la naturaleza encadenada del fenómeno. Es una lectura
  coherente; coherente no es necesario.
- Que fuera elegida **por** esa razón. `011-C3R` fechó el diseño; no encontró su justificación.

## 8 · Qué permanece NO DETERMINABLE

- **Por qué se eligió el producto** y no otra agregación.
- Si existe razón **teórica, normativa o empírica** que la funde. `C4`: no consta.

## 9 · Consecuencias de mantenerla

| | |
|---|---|
| ✅ | Una unidad sin evidencia en un silo **no puede acreditar congruencia**, que es coherente con el constructo |
| ⚠️ | El índice es **muy sensible**: el 12,8 % del peso queda en cero por una sola dimensión |
| ⚠️ | En la práctica, `D1` **se manifiesta enteramente a través de `D2`** — son la misma pregunta hoy |
| 🔴 | Mientras no se declare, se lee como propiedad del fenómeno y no como elección |

## 10 · Condición objetiva para revisarla

Se revisa si ocurre **cualquiera** de estas cosas:

1. Aparece un factor distinto de `V_i` con valor cero — la anulación dejaría de ser un problema
   de acreditación y pasaría a ser uno de agregación.
2. `011-A2` declara la unidad y la correspondencia `011-B` cambia el universo.
3. Se adopta el universo completo de 66 metas (`v2`).
4. `QUIRA-NEXT` decide extraer la verificabilidad a una dimensión propia (ver `ADR-055 §10`).

---

## Dictamen que este ADR declara

> **`D1` · DECISIÓN DE DISEÑO NO FUNDAMENTADA COMO NECESARIA, CONSERVABLE BAJO DECLARACIÓN
> EXPLÍCITA.**
>
> No se demuestra necesaria **ni incorrecta**. Puede conservarse siempre que el sistema declare
> que es una **elección metodológica** y no una propiedad derivada del fenómeno.

⚠️ Lo que este ADR **no** hace: no valida la decisión, no autoriza a cambiarla y no toca el
motor. Cambia su **estatus epistemológico** — de regla aplicada sin declarar a decisión
identificada, acotada y con condición de revisión.

*Dylus Lab © 2026 · deriva de `GM-OMEGA_ICPI_DICTAMEN_011C4.md`*
