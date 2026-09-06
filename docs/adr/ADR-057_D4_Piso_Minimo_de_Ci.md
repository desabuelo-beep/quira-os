---
id: ADR-057
authority:
  parent: GOVERNANCE-001
  constitution_articles: [5, 9]
  type: METODOLOGICA
status: PROPUESTO — pendiente de sello de Javo
fecha: 2026-09-06
decision_gm_omega: D4
---

# ADR-057 · `D4` — El piso mínimo de `C_i`

> **Propuesto por la dirección técnica tras `GM-Ω-011-C4`.** La IA propone; el humano valida
> (`ADR-035 §5`). **Este ADR no cambia el motor.**

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

*Dylus Lab © 2026 · deriva de `GM-OMEGA_ICPI_DICTAMEN_011C4.md`*
