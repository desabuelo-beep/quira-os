---
id: ADR-056
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: APROBADO — sellado por Javo (2026-09-06)
fecha: 2026-09-06
decision_gm_omega: D3
---

> ## 🔏 SELLO · 2026-09-06
>
> **Se mantiene el esquema de pesos como decisión vigente, con REVISIÓN OBLIGATORIA ANTES DE SU
> PRIMERA ACTIVACIÓN.**
>
> El sello **no convierte un `NO DETERMINABLE` en `DEMOSTRADO`**: el fundamento cuantitativo de
> `0,15 / 0,10 / 0,05` sigue sin determinar (`§8`), y la divergencia con el glosario sobre
> `INF-03` (`D-013`) sigue abierta.

# ADR-056 · `D3` — Los pesos de deducción de `C_i`

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

## 1 · Decisión vigente

| Código | Norma | Deducción |
|---|---|---|
| `INF-01` | `LOSNCP 17/58` — alerta SERCOP verificada | **−0,15** |
| `INF-02` | `CGE / NCI 406-01` — observación de auditoría | **−0,10** |
| `INF-03` | `COPFP 10/115` — retraso > 60 días en planificación | **−0,05** |
| `INF-04` | `LO_CPCCS 11` — resolución firme de desacato | **FIJA `C_i = 0,50`** |

`H01` Sección L (`TBL_HOMOLOGACION_NORMATIVA`).

## 2 · Fenómeno que pretende representar

La **severidad relativa** de cada infracción sobre la calidad del proceso orgánico. El orden
implícito: contratación > control > planificación, y participación en categoría propia.

## 3 · Unidad afectada

La meta del PDOT, vía la unidad orgánica responsable (`H01` Sección I).

## 4 · Evidencia que la sostiene

| Fuente | Qué aporta |
|---|---|
| `GOLDMASTER_REFACTOR_MASTER_v2.0.md` | prescribe los cuatro códigos con sus pesos · `DECISIÓN 27-Abr-2026` |
| `H01` Sección L | los implementa |
| `011-C3R` | fechó el acto: entran **junto con** el mecanismo, el piso y el fallback |

⚠️ **Todas las fuentes ENUNCIAN los pesos. Ninguna los JUSTIFICA.**

## 5 · Alternativas consideradas

⚠️ **Ninguna consta.** No hay documento que compare escalas de severidad ni que explique por qué
`0,15` y no `0,20`. El único precedente declarado sobre parametrización en el sistema es
`H95` `L-07`, referido al TGI:

> *«Los pesos de las 5 dimensiones son definidos por **criterio experto (Dylus Lab)**, no por
> análisis de componentes principales (PCA) o regresión sobre resultados.»*

Eso documenta una **práctica**; no justifica **estos** pesos.

## 6 · Qué está DEMOSTRADO

- Los pesos están documentados, fechados y son coherentes entre prescripción e implementación.
- Entraron **en un solo acto de diseño** (25→29-abr-2026), no por calibración iterativa
  observable.
- ⚠️ **Divergencia latente**: el glosario `H02!Ci_Determinista` asigna a `INF-03` un peso de
  `0,20`, mientras la Sección L asigna `0,05` — **factor 4** (`D-013`).

## 7 · Qué es INFERENCIA

Que el orden `0,15 > 0,10 > 0,05` refleje una jerarquía deliberada de severidad. Es la lectura
natural; no consta declarada.

## 8 · Qué permanece NO DETERMINABLE

> **El fundamento cuantitativo de los valores.** `011-C3R` cerró este punto: están establecidos
> documentalmente, su fundamento no ha sido determinado — y **no se seguirá excavando** para
> encontrarlo.

## 9 · Consecuencias de mantenerla

| | |
|---|---|
| 🔵 | **Efecto hoy: ninguno.** Las cuatro columnas de infracción están en cero para las 25 metas |
| ⚠️ | La divergencia con el glosario es **latente**: se activa con la primera infracción registrada |
| 🔴 | Ese día es exactamente **el día en que tienen que estar bien** |

## 10 · Condición objetiva para revisarla

> **Revisión obligatoria antes de registrar la primera infracción.** No es una recomendación:
> es la condición que impide aplazar la decisión hasta el momento en que ya no pueda tomarse con
> calma.

Y antes de esa revisión hay que resolver `D-013`: **cuál de los dos pesos de `INF-03` rige**.

---

## Dictamen que este ADR declara

> **`D3` · FUNDAMENTO CUANTITATIVO NO DETERMINADO · LATENTE · REVISIÓN OBLIGATORIA ANTES DE SU
> PRIMERA ACTIVACIÓN.**

*Dylus Lab © 2026 · deriva de `GM-OMEGA_ICPI_DICTAMEN_011C4.md`*
