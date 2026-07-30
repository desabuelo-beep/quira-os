---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 8, 9]
  type: OBSERVACION
---

# OBS-022 · Las SAT del motor no tienen cadena BRN que las funde

**2026-07-29 · hallazgo de Javo · alcance: los 4 dominios cerrados con PCD**

> **La pregunta que lo abrió** *(Javo):* *"esta estructuración SAT-BRN debe hacerse en los otros
> DOM que tenemos culminados; entonces su estado **no puede estar cerrado totalmente** si hay
> grietas como esta y la de los POA por subsanar."*

---

## 1 · La medida

| | |
|---|---:|
| SAT existentes en el Gold Master (`SAT_Catalogo`) | **9** — SAT-0 … SAT-VIII |
| SAT declaradas en alguna RO (bloque `produce:`) | **1** |
| **SAT sin cadena `CNO → RO → SAT`** | **8 de 9 (89%)** |

La única declarada es **SAT-IX**, creada hoy tras la corrección de procedimiento. **Ninguna RO
tenía bloque `produce:`** antes de esta sesión — el concepto no existía en la práctica, aunque
ADR-038 §1b lo exigía desde julio.

```
docs/brn/RO-*.yaml          produce      consume
  RO-I-001                    []         [SAT-I-001]
  RO-I-002                    []         [SAT-I-002]
  RO-III-001                  []         [SAT-III-001]
  RO-IV-001                   []         [SAT-IV-001]
  RO-IX-001                   []         [SAT-IX-001]
  RO-VIII-001 / 002           []         []
  RO-VIII-003            [SAT-IX]        [SAT-VI]      ← única
```

**Consecuencia:** el umbral y el peso de las 8 SAT restantes viven **solo en el Excel**. Si mañana
cambia la norma que las funda, nada obliga a revisarlas, porque no hay cadena que lo señale. Es
exactamente lo que ADR-038 pretendía evitar.

## 2 · Colisión de nomenclatura que esta sesión agravó

`RO-IX-001` declara `consume: [SAT-IX-001]`. Hoy se creó **`SAT-IX`**. Son cadenas distintas, pero
la confusión visual es inevitable — y **OBS-016 ya había documentado el problema de raíz**:

| Sistema | Nomenclatura | Ejemplo |
|---|---|---|
| Canon BRN | `SAT-{romano del dominio}-001` | `SAT-IX-001` (d09) |
| **Gold Master** | `SAT-0 … SAT-VIII` por **dimensión TGI** | `SAT-V` = CPCCS |

OBS-016 concluyó que la nomenclatura BRN es la **incorrecta**: *"d09: puse `SAT-IX-001` → el GM no
tiene `SAT-IX`; la señal de CPCCS es `SAT-V`"*. Las RO citan SAT **que no existen en el motor**.

> **`SAT-IX` (nueva) es legítima**: continúa la serie del Gold Master, que es la autoridad
> (Regla 1). Las que deben corregirse son las referencias BRN heredadas — trabajo pendiente que
> OBS-016 ya había abierto y que sigue sin saldarse.

## 3 · Respuesta a la pregunta de Javo sobre los PCD cerrados

**Sí hay grieta. No, los PCD no se invalidan.** La distinción importa:

| | |
|---|---|
| **R-G nació el 2026-07-29** | exige que todo DOM declare su cableado al motor |
| Los PCD de d01·d02·d03·d09 se cerraron **antes** | cumplieron el protocolo **vigente entonces** |

Una regla nueva **no invalida retroactivamente** el trabajo previo — pero **sí abre una deuda
explícita**. Declararlos "cerrados" sin registrar la deuda sería la afirmación no verificada que
este sistema combate.

### Estado corregido de los dominios

| DOM | PCD | Deuda BRN↔SAT | Deuda POA (OBS-020/021) |
|---|---|---|---|
| **d01** Planificación | cerrado | SAT-0 sin RO | ✅ **abierta** — el POA localiza el 1% |
| **d02** Presupuesto | cerrado | SAT-II · SAT-III · SAT-IV sin RO | — |
| **d03** Contratación | cerrado | SAT-I sin RO | — |
| **d09** RDC | cerrado | SAT-V sin RO · cita `SAT-IX-001` inexistente | — |
| **d08** Participación | en curso | ✅ **SAT-IX declarada** (única sana) | ✅ abierta |

> **Nomenclatura propuesta: `cerrado con deuda declarada`.** Ni "cerrado" a secas —falso— ni
> "reabierto" —destruiría el trabajo y violaría la Regla 8—. El PCD conserva su validez y **anexa
> su deuda**, como ya se hizo con `PCD-D01` y OBS-020.

## 4 · Por qué NO se reabren los PCD

1. **Regla 8** — un dominio cerrado incorpora hallazgos posteriores por vía de OBS, no reabriendo
   su curación. Es el mecanismo que ya funcionó con OBS-020 en `PCD-D01`.
2. **Costo** — reabrir 4 dominios para añadir un bloque `produce:` en sus RO es
   desproporcionado frente a saldar la deuda dominio por dominio.
3. **R-E** — el esfuerzo disponible está comprometido en cerrar Montecristi.

## 5 · Acciones

| # | Acción | Estado |
|---|---|---|
| 1 | Medir la grieta (8 de 9 SAT sin RO) | ✅ |
| 2 | Declarar `SAT-IX` en `RO-VIII-003` | ✅ |
| 3 | Anexar la deuda a cada PCD cerrado | ⏳ |
| 4 | Declarar SAT-0·I·II·III·IV·V·VII·VIII en sus RO | ⏳ **el grueso del trabajo** |
| 5 | Corregir referencias BRN a SAT inexistentes (OBS-016) | ⏳ abierta desde 2026-07-24 |
| 6 | Añadir el bloque `produce:` al esquema de RO y al verificador `brn_cno.py` | ⏳ **evita que se repita** |

> **La acción 6 es la que impide la recurrencia:** mientras el verificador no exija `produce:`,
> nada impide crear otra SAT huérfana. Es el mismo principio del test de regresión del filtro
> ontológico — convertir el hallazgo en verificación permanente.

---
*OBS-022 · Dylus Lab © 2026 · hallazgo de Javo · deriva de ADR-038 §1b · relacionada con OBS-016.*
