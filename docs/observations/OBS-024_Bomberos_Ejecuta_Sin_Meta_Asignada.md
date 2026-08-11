---
id: OBS-024
authority:
  parent: ADR-047
  constitution_articles: [1, 3]
  type: OBSERVACION
fecha: 2026-08-11
dominio: d06 · d01 · d05
estado: VERIFICADA
---

# OBS-024 · El Cuerpo de Bomberos ejecuta el PDOT sin tener metas asignadas en él

> **Origen.** Javo, corrigiendo una extracción del director (2026-08-11): *«no estás considerando
> a la Empresa de Aseo EP y Cuerpo de Bomberos, tu análisis es corto, hay metas para estas
> también»*. La revisión confirma la corrección y encuentra algo distinto de lo esperado.

## Qué se buscaba

Clasificar quién ejecuta cada meta del PDOT, para determinar el factor `Ei` (autonomía orgánica)
sin penalizar la ejecución por entidad propia del GAD.

## Qué se encontró

**El Cuerpo de Bomberos no aparece como Unidad Responsable de ninguna meta**, ni en el Excel de
contraste ni en la matriz plurianual del PDOT oficial (tablas #341-352 del documento).

Aparece en otro sitio: las **tablas #353 y #355**, de *identificación de estrategias de
articulación*, donde figura un proyecto —«Construcción de la Estación Bomberil»— con estado
**«Sin postulación»**.

**Pero ejecuta.** Su POA 2026 declara **$1.752.000** y se alinea explícitamente al plan:

> «NO. DE PTDOT PLAN BICENTENARIO **20** · SISTEMA **Asentamientos Humanos** · OBJETIVO DE
> DESARROLLO *Montecristi Hábitat digno y sostenible* · EJE DE RESPUESTA A EMERGENCIAS»

Y tiene serie completa en el corpus: **POA 2024-2026 · PAC 2023-2026 · rendición de cuentas
2023-2024**.

## El hallazgo

> **Una entidad adscrita del holding municipal ejecuta presupuesto propio declarando alineación
> al PDOT, y la matriz de metas del PDOT no le asigna ninguna meta.**
>
> Formulado con precisión tras verificar COOTAD 140 (ver §«¿Hay otra vía?»): **no es que esté
> desarticulada — es que su articulación no es medible por el instrumento con el que se mide el
> cumplimiento de metas.**

La cadena se rompe en un punto que ninguna de las dos partes muestra por sí sola: el PDOT dice
qué hay que lograr y a quién le toca; el POA de Bomberos dice qué hace y cuánto gasta. **Cruzados,
falta el eslabón que los une.**

No es un error de captura ni de lectura: es una **brecha real de trazabilidad**, del tipo exacto
que el sistema existe para encontrar. Y es invisible mientras se mire una sola fuente.

## Lo que la matriz sí asigna, y a quién

| Ejecutor | Metas | Naturaleza |
|---|---|---|
| Unidades del GAD | 54 | directo |
| Empresa de Aseo · Empresa de Vivienda | 6 | empresa pública propia |
| Patronato de Amparo Social | 6 | entidad adscrita propia |
| **Cuerpo de Bomberos** | **0** | **adscrita propia — ejecuta sin meta asignada** |

La gestión de riesgo, que es su competencia, aparece asignada a **«Planificación / Unidad de
gestión de riesgos»** — una unidad del GAD, no la entidad que la ejecuta con presupuesto propio.

## Por qué importa para el motor

1. **Para `Ei`:** no se puede corregir la autonomía de una meta de Bomberos porque **no hay meta
   de Bomberos que corregir**. El problema es anterior al factor.
2. **Para la cobertura:** si el ICPI mide cumplimiento de metas del PDOT, la ejecución de Bomberos
   **no entra en el índice por ninguna vía** — ni bien ni mal. Queda fuera del alcance.
3. **Para el holding (d05):** `H12d_ICPI_POR_ENTIDAD` calcula por entidad. Una entidad sin metas
   asignadas no puede tener cumplimiento medible de plan.

## ¿Hay otra vía legal de articulación? Sí, y hay que decirlo

Pregunta de Javo (2026-08-11): *«¿técnicamente hay otra forma de ligar o articular Bomberos al
PDOT? No quiero decir estas cosas y que salga por ahí alguna situación que los ligue de otra
manera».* La pregunta es correcta: **un hallazgo que no agota las vías alternativas es un hallazgo
frágil.** Se agotaron, y el resultado **matiza la observación sin anularla**.

### La norma que gobierna el caso — verificada

**COOTAD Art. 140** · `SHA256 0dc5f48de6bb9af5f8bd0b595c179b5224842dd0b2531762e858d617c58c8ecb`:

> «La gestión de riesgos […] se gestionará **de manera concurrente y de forma articulada por todos
> los niveles de gobierno** […] Los cuerpos de bomberos del país **serán considerados como
> entidades adscritas a los gobiernos autónomos descentralizados municipales**, quienes
> funcionarán **con autonomía administrativa y financiera, presupuestaria y operativa**.»

De ahí se siguen tres cosas, y las tres importan:

1. **Bomberos es entidad adscrita del GAD.** No es un tercero: pertenece al holding municipal.
2. **Tiene autonomía presupuestaria por ley.** Ejecutar con presupuesto propio **no es una
   anomalía**: es exactamente lo que la norma dispone.
3. **La competencia es concurrente y debe ejercerse de forma articulada.** La articulación es una
   exigencia legal, pero el artículo **no impone que se instrumente mediante una fila en la matriz
   de metas del PDOT.**

### Las vías alternativas, evaluadas una por una

| Vía | ¿Existe? | ¿Articula a Bomberos con el PDOT? |
|---|---|---|
| **Fila en la matriz plurianual de metas** | no | — |
| **Tablas de estrategias de articulación del PDOT** (#353, #355) | **sí** | parcialmente: proyecto «Estación Bomberil», estado *sin postulación* |
| **Alineación declarada en su propio POA** | **sí** | sí: PTDOT 20 · Asentamientos Humanos · Hábitat digno |
| **Concurrencia por COOTAD 140** | **sí** | sí, por mandato legal directo |

**Conclusión:** Bomberos **sí está articulado al PDOT**, por al menos tres vías. Lo que **no
existe** es correspondencia en la matriz de metas — que es la única vía con la que el motor puede
medir cumplimiento de plan.

### Lo que esto cambia en la formulación del hallazgo

> **No es que Bomberos esté desarticulado del PDOT. Es que su articulación no es medible por el
> instrumento con el que se mide el cumplimiento de metas.**

Eso es más preciso, más difícil de refutar, y sigue siendo un hallazgo: **la trazabilidad
documental se interrumpe aunque la articulación jurídica exista.**

### Advertencia sobre citas que NO se sostienen

Un aporte externo propuso respaldar el caso con **COESCOP Art. 274** y con **COPLAFIP Arts. 115 y
116** como fundamento de «modificaciones de inclusión en el PAI». Verificado contra corpus:

- **COESCOP no está ingerida.** Sin SHA no se cita (Regla 3), por correcta que parezca.
- **COPLAFIP 115 es *Certificación Presupuestaria* y 116 es *Establecimiento de Compromisos***.
  Ninguno regula modificaciones al PAI. Citarlos así habría sido desmontable en un minuto por
  cualquier técnico del GAD.

Se registran aquí, no para señalar a nadie, sino porque **este expediente debe mostrar también qué
fundamento se descartó y por qué**.

## Lo que NO se concluye

- **No se afirma incumplimiento de nadie.** Que el PDOT no asigne metas a Bomberos puede
  responder a una decisión de técnica de planificación, no a una omisión.
- **No se corrige el PDOT.** Es un instrumento aprobado; QUIRA lo observa, no lo edita.
- **No se inventa la meta faltante.** Si el vínculo no está declarado, no se supone.

Lo que corresponde es **declarar la brecha y medirla**: cuánto presupuesto se ejecuta bajo
alineación declarada al PDOT sin correspondencia con una meta del propio PDOT.

## Trazabilidad

| Fuente | Carácter |
|---|---|
| PDOT Montecristi 2023-2027 Bicentenario `.docx`, tablas #341-352 y #353-355 | oficial |
| Plan Plurianual PDOT 2023-2027 `.xlsx` · `sha256 09a2aacc…` | **no oficial** — contraste |
| `POA-BOMBEROS-2026` · corpus, 21 fragmentos | institucional |
| `PAC-BOMBEROS-2023..2026` · `RC-BOMBEROS-2023..2024` | institucional |

---
*OBS-024 · Dylus Lab © 2026 · hallazgo de cruce: ninguna fuente lo muestra sola.*
