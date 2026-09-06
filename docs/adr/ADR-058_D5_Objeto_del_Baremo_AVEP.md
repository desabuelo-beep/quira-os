---
id: ADR-058
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: APROBADO — sellado por Javo (2026-09-06)
fecha: 2026-09-06
decision_gm_omega: D5
---

> ## 🔏 SELLO · 2026-09-06
>
> ⚠️ **Este sello NO valida el baremo `AVEP` como medida sustantiva.**
>
> Se adopta **únicamente** la decisión de que **`AVEP` no puede interpretarse hasta declarar
> formalmente su objeto**. Es un sello sobre el **procedimiento**, no sobre la escala.
>
> Mientras el objeto no se declare, ninguna superficie puede presentar una categoría `AVEP` como
> juicio de integridad, cumplimiento o desempeño — porque no está establecido cuál de esas cosas
> clasifica.

# ADR-058 · `D5` — El objeto del baremo `AVEP`

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

## Por qué este ADR no propone una escala

Porque **no se puede validar una escala antes de declarar el fenómeno que pretende clasificar**
(`DOC-012`: un porcentaje no tiene significado semántico por sí mismo).

> `011-C4` no preguntó «¿qué escala es correcta?». Preguntó **«¿qué fenómeno representa `AVEP`?»**
> — y ésa es la pregunta que este ADR abre, no cierra.

---

## 1 · Decisión vigente

Un baremo traduce el valor continuo del ICPI en categorías cualitativas. **Y hay dos versiones
conviviendo** (`D-012`):

| | Niveles | Umbrales | Entradas | Dónde |
|---|---|---|---|---|
| **motor** | 5 | 90 / 70 / 40 / 20 | sólo ICPI | `config.AVEP` · `H12!B34` |
| **canon** | 4 | 75 / 60 / 50 | ICPI + SAT + Ti | `07_AVEP_LENGUAJE.md` · `H29!B14` |

Para el mismo baseline **27,4582 %**, el motor dice «🟠 Gestión por Ocurrencia» y el canon dice
«🔴 Nivel de Atención Alta».

## 2 · Fenómeno que pretende representar

⚠️ **NO DECLARADO.** Es exactamente el problema. Las categorías podrían representar niveles de:

| Candidato | Implicaría |
|---|---|
| **integridad** | un juicio sobre la conducta institucional |
| **cumplimiento** | un grado de avance frente a lo comprometido |
| **desempeño** | una evaluación de gestión |
| **evidencia** | cuánto se puede acreditar |
| **riesgo** | probabilidad de incumplimiento futuro |
| **comunicación institucional** | una traducción para el lector, sin pretensión analítica |

Los seis producen escalas distintas. **Elegir umbrales antes de elegir objeto es elegir al azar.**

## 3 · Unidad afectada

El GAD como conjunto — `AVEP` clasifica el ICPI global, no cada meta.

## 4 · Evidencia que la sostiene

| Fuente | Qué aporta |
|---|---|
| Javo (2026-09-03) | *«La escala AVEP es nuestra invención, pero luego la sacamos para ajustarnos a lo que la normativa pública exigía»* |
| `007-X-bis` | es un **baremo propio**, no una norma externa; la sigla se perdió |
| `H01` Sección B | «ESCALA AVEP (5 NIVELES)» |

⚠️ Y un incidente que el propio libro conserva (`H01!A28`): **no existe una función `=AVEP()`** —
en algún momento se la trató como fórmula y no lo es. Es un **baremo de presentación**.

## 5 · Alternativas consideradas

⚠️ Ninguna consta evaluada. Y no puede evaluarse ninguna mientras el objeto no esté declarado.

## 6 · Qué está DEMOSTRADO

- Conviven **dos escalas divergentes** en superficies distintas del mismo sistema.
- Ninguna superficie declara cuál rige.
- La divergencia **ya alcanzó al Gold Master**: `H12!B34` y `H29!B14` implementan escalas
  distintas.
- `AVEP` es un baremo propio, no una obligación normativa externa.

## 7 · Qué es INFERENCIA

Que la versión de 5 niveles sea la vigente por estar en `H12`. Es plausible —`H12` es el motor—
pero `H29` es la superficie que ve un alcalde.

## 8 · Qué permanece NO DETERMINABLE

- **Qué fenómeno clasifica.**
- Cuál de las dos escalas rige.
- Por qué los umbrales son los que son — en ninguna de las dos versiones.

## 9 · Consecuencias de mantenerla

| | |
|---|---|
| 🔴 | El **mismo número admite dos lecturas institucionales distintas** según qué pantalla se abra |
| 🔴 | Una categoría cualitativa es **lo que el lector recuerda** — no el 27,4582 % |
| ⚠️ | Y sin objeto declarado, la categoría puede leerse como juicio de integridad cuando quizá sólo traduce un porcentaje |

## 10 · Condición objetiva para revisarla

**Bloqueada hasta declarar el objeto.** El orden es forzoso:

```
  1. declarar QUÉ FENÓMENO clasifica AVEP
  2. sólo entonces, cuál escala lo representa
  3. sólo entonces, qué umbrales
  4. y unificar en UNA fuente parametrizable (DOC-012 · arquitectura BAREMO de 007-X-bis §9)
```

⚠️ **Y no se elige umbral desde el resultado que produce**: eso es lo que `DOC-009` prohíbe.

---

## Dictamen que este ADR declara

> **`D5` · NO EVALUABLE HASTA QUE SE DECLARE SU OBJETO.**
>
> No es que la escala esté mal: es que **no se puede juzgar**. Y mientras dos versiones convivan
> sin que ninguna superficie declare cuál rige, el mismo número admite dos lecturas distintas.

Este ADR **desbloquea `D-012`** en cuanto se responda su campo `2`.

*Dylus Lab © 2026 · deriva de `GM-OMEGA_ICPI_DICTAMEN_011C4.md`*
