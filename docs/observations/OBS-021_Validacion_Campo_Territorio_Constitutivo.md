---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 3, 4, 9]
  type: OBSERVACION
---

# OBS-021 · El territorio es constitutivo de la demanda ciudadana

**2026-07-29 · validación experta de campo (Javo) sobre 24 correspondencias del MRSPP v3**

| | |
|---|---|
| **Precisión medida** | **3 / 24 = 12%** |
| **Veredicto de Javo** | *"NO es real la vinculación, es solo semántica y nada técnica"* |
| **Corrección** | **REGLA T0** — el territorio deja de ser filtro y pasa a ser constitutivo |
| **Efecto** | correspondencias 120 → **43** · sin correlato 103 → **180 (81%)** |

---

## 1 · La medición

| Nivel MRSPP | Correctas | Precisión |
|---|---:|---:|
| **directa** | 2 / 8 | 25% |
| **funcional** | 1 / 8 *(+2 parciales)* | 12% |
| **complementaria** | **0 / 8** | **0%** |
| **Global** | **3 / 24** | **12%** |

Un motor con 12% de precisión no está descalibrado: **responde la pregunta equivocada**.

## 2 · La causa, en las palabras de Javo

> *"El sector Nuevo Montecristi es real, pero la relación está mal, es solo semántica. Si la
> petición fue para Nuevo Montecristi, el parque de Las Pampas (zona rural) no es un acatamiento
> de las demandas ciudadanas. Solo estás juntando semánticamente. **La única relación es que en
> ambas se pide un parque. NO, eso no es incorporar las necesidades ciudadanas a la planificación,
> ya que son distintos lugares.**"*

### El contraste que lo prueba

De los 24 casos, el único `directa` confirmado sin reservas:

| # | Demanda | Proyecto POA | Veredicto |
|---|---|---|---|
| **5** | tapas de alcantarillado **LA PILA** | alcantarillado sanitario **Parroquia La Pila** | ✅ *"aquí sí hay relación que se puede trazar"* |
| 1 | parque **Nuevo Montecristi** | parque **Las Pampas** | ❌ solo semántica |
| 8 | parques **Barrio San José** | parque **Las Pampas** | ❌ solo semántica |

**La diferencia no es el rubro ni el score: es que en el caso 5 AMBOS lados declaran el mismo
lugar.** Esa es la condición de verificabilidad.

### El principio

> **Una demanda ciudadana no es «X». Es «X en el lugar Y».** El lugar no es un atributo
> secundario que refine la coincidencia: **es parte del objeto demandado**. Si el proyecto ejecuta
> X en otro lugar —o no dice dónde— **no atendió esa demanda**.

## 3 · Segunda causa · el proyecto genérico que captura todo

**6 de las 8 `complementaria`** emparejaban contra el mismo proyecto:
*"Desarrollo de actividades que promueven la participación ciudadana en el cantón"*.

Es el patrón del membrete y de la unidad ejecutora **por tercera vez**: enunciado institucional
genérico que empareja con cualquier cosa. Corregido con `PROYECTOS_GENERICOS`.

## 4 · Lo que se corrigió en el motor

| Regla | Antes | Ahora |
|---|---|---|
| **T0 · territorio constitutivo** | solo descartaba si **ambos** declaraban lugares distintos | si la demanda declara lugar y el proyecto **no declara ninguno** → `inverificable_territorialmente` |
| **Ancla genérica** | lista fija de topónimos (nunca completa, menos para 222 GAD) | detección **por patrón** (`sector\|barrio\|parroquia\|comuna…` + paréntesis/viñeta) — no requiere conocer el nombre |
| **Proyectos genéricos** | — | enunciados institucionales no satisfacen demandas concretas |

**Verificación:** los 9 casos de la validación reproducidos → **9/9 coinciden con el criterio de
Javo**. Regresión: **16/16**.

### Dos expectativas MÍAS que la validación invalidó

Ambas estaban en el test y eran supuestos de la dirección técnica, no criterio de campo:

1. *"letrinas Barrio Santa Ana ↔ plantas de tratamiento"* — se daba por válida. **No lo es**: el
   proyecto no dice dónde se ejecuta.
2. *"parque Las Paolas ↔ parques del cantón"* — se justificó invocando la Regla T1
   (`cantón → parroquia: PERMITIDO`). **Mezcla dos cosas distintas**: esa regla habilita **proxies
   estadísticos** (NBI, cobertura), **no la acreditación de que una petición concreta fue
   atendida**.

## 5 · El resultado es el hallazgo

| | v3 | **v4 (territorio constitutivo)** |
|---|---:|---:|
| directa | 68 | **26** |
| funcional | 27 | **8** |
| instrumental | 0 | **0** |
| complementaria | 25 | **9** |
| **sin correlato** | 103 | **180 · 81%** |

**El 81% no es una falla del motor: es la medida de la brecha.** Y confirma **OBS-020 desde el
lado opuesto** — allí se midió que el POA localiza el 1% del gasto; aquí se mide la consecuencia:
**cuatro de cada cinco demandas ciudadanas no tienen correspondencia verificable en la
planificación.**

> Javo lo formuló antes de que se midiera: *"si no se sabe dónde fue hecha la obra, y desde la
> petición sabemos quién la pidió y para qué sector, **eso es evidencia**, ya que el GAD no
> aterriza sus POA y esa opacidad hace que no se pueda determinar si las peticiones fueron
> atendidas realmente en POA, PAC y presupuesto."*

## 6 · Frontera de lo que se afirma *(Carta Art. 4.5)*

| ❌ NO se dice | ✅ Se certifica |
|---|---|
| *"el GAD no atendió el 81% de las demandas"* | *"el 81% de las demandas ciudadanas **no tiene correspondencia verificable** en el instrumento de planificación"* |

**`inverificable_territorialmente` ≠ `no atendido`.** Puede haberse atendido: el expediente no
permite comprobarlo. Es **ausencia de habilitación documental**, no incumplimiento.

## 7 · Acciones

| # | Acción | Estado |
|---|---|---|
| 1 | REGLA T0 · territorio constitutivo | ✅ |
| 2 | Ancla territorial genérica por patrón (escala a 222 GAD) | ✅ |
| 3 | Descarte de proyectos genéricos institucionales | ✅ |
| 4 | Corregir las 2 expectativas invalidadas del test | ✅ 16/16 |
| 5 | Segunda validación sobre la mezcla v4 | ⏳ Javo |
| 6 | Revisar el nivel `complementaria` — 0% de precisión | ⏳ ¿aporta algo o se retira? |

> **Pregunta abierta para Javo (§6):** `complementaria` obtuvo **0/8**. Con el territorio ya
> corregido quedan 9 casos. Si en la segunda ronda vuelve a fallar, el nivel **no está aportando
> capacidad analítica** y debería retirarse del MRSPP — sería inflación (Regla 7).

---
*OBS-021 · Dylus Lab © 2026 · validación de campo de Javo · deriva de OBS-020.*
