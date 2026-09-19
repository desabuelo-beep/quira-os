---
id: ADR-059
authority:
  parent: ADR-043
  constitution_articles: [4, 6, 8]
  type: ARQUITECTONICA
status: PROPUESTO — pendiente del sello de Javo (ADR-035 §5)
fecha: 2026-09-19
supersede_al_sellarse:
  - ADR-041 §4-ter (la licencia de gestión al GAD)
  - ADR-043 §4, fila «QUIRA Institucional»
---

# ADR-059 · El norte del ecosistema QUIRA · evidencia abierta, fronteras claras y ninguna licencia al observado

> **Contexto.** Javo (2026-09-19), en un paréntesis durante `D1`: *“¿es viable aterrizar todas las QUIRA
> como un único ecosistema… cada quien desde sus espacios, fronteras, reglas y delimitaciones… un ecosistema
> abierto sin costos?”* Y después de leer al colega: *“quizá eliminar QUIRA Institucional, vender software a
> los municipios, deba eliminarse, y potenciar el marketplace / network effects como norte… debe quedar
> guardado… sin perder este norte.”*
>
> ⚖️ **Alcance.** Este ADR guarda un **norte** y cierra **una** decisión comercial pendiente. **No amplía
> QUIRA 7, no crea dominios, no toca el motor ni el canon técnico y no autoriza ninguna implementación.**
> La copia que el colega guardó vive en su propio entorno; **ésta es la del repositorio.**

## 1 · No es una idea nueva: el canon ya la contiene

Antes de decidir se leyó lo que existe — *la amnesia que ya nos costó*:

| la idea del paréntesis | dónde ya es canon |
|---|---|
| un ecosistema, no productos aislados | `docs/corpus_externo/QUIRA_ECOSYSTEM_2026_2030.md` (2026-05-31): “No es un software. Es una infraestructura independiente de observación territorial.” · `HOJA_DE_RUTA_MAESTRA §1` |
| cada QUIRA con su función, **sin su propia verdad** | `ADR-043 §3`, regla 3: “Ningún producto QUIRA constituye una fuente independiente de verdad.” · `ADR-041 §3`: un motor, dos entradas |
| ciudadanos, OSC y academia **aportan** evidencia | `ADR-045` y `ADR-046`: una superficie, tres custodias; el techo lo fija el documento, no quien lo trae |
| el conocimiento público es del territorio | Constitución Institucional, Art. 4 y Art. 6 |
| el GAD es sujeto observado, no cliente | `BOOT §LA TESIS` |

**Lo que el paréntesis añade** es el circuito entre las QUIRA y el horizonte de la red. Lo que **cierra** es
una contradicción que el canon dejó abierta a propósito (punto 2.1).

## 2 · Lo que se decide al sellar

### 2.1 · QUIRA no vende licencias al sujeto observado

`ADR-041 §4-ter` abrió la licencia de gestión al GAD y dejó escrito que contradecía a `BOOT §LA TESIS`
(“QUIRA NO vende software a municipios”) y a la Hoja de Ruta (“NO licencias GAD”): *“es decisión del
fundador, no de la dirección técnica”*. **Esta es esa decisión: la licencia se cierra.**

**Consecuencia, por el propio test de `ADR-043`:** sin licencia, QUIRA Institucional no tiene cómo
financiarse y **no pasa el gate 5**. No se elimina por decreto: **deja de ser un producto de la familia**
porque no pasa la prueba que la familia se dio. El GAD sigue en el ecosistema como lo que es —**la cabeza del
ecosistema observado**— y, como cualquier actor, puede usar la capa abierta, sin relación comercial.

### 2.2 · Independencia económica — generaliza la cláusula de `§4-ter`

> **Ningún ingreso de QUIRA depende del contenido de una observación, ni proviene de quien es observado por
> ella.**

Es la misma línea que protegía la licencia (*gestionar ≠ influir en la observación*), llevada a todo el
ecosistema. Su consecuencia más exigente está en el punto 4.

### 2.3 · El norte: ecosistema abierto con fronteras; la red, como horizonte

| capa | qué es | costo |
|---|---|---|
| **evidencia pública** | dato, evidencia, indicador y metodología publicados | **abierta** — Constitución Institucional, Art. 4 |
| **capacidad de trabajar sobre ella a escala** | interfaces avanzadas, integración, monitoreo, series y método reproducible, expedientes | servicio — es el contrato de **Impact** y de **Cooperación** en `ADR-043 §4` |
| **red** (*marketplace / network effects*) | actores que encuentran oportunidades y evidencia común | **horizonte**, no tarea de `REARQ` |

**La red tiene dos condiciones previas**, ninguna de las cuales existe hoy:

1. **Cobertura.** Es la misma dependencia que `ADR-041 §4` fijó para Impact: sin evidencia de muchos GAD no
   hay nada que intercambiar. La red llega **después** de la Fase 1, no antes.
2. **Independencia.** Si QUIRA cobra por conectar una necesidad con un financiador, gana más cuanto más
   necesidad muestra: ese incentivo **toca la observación**. Toda tarifa de la red debe ser independiente de lo
   que la observación dice (2.2).

**Los nodos** —universidades, OSC, ONG, cooperación— aportan evidencia por las custodias del Observatorio
(`ADR-045`, `ADR-046`) y construyen conocimiento propio sobre la evidencia común. **Nunca como fuentes
independientes de verdad** (`ADR-043`, regla 3).

## 3 · Dos diferencias con el texto del colega que **no se adoptan sin decisión**

| el colega | el canon sellado | por qué importa |
|---|---|---|
| **Impact** mide resultados de las intervenciones (MRV, evaluación) y **devuelve** evidencia al Observatorio | `ADR-043 §4`: Impact **abre el conocimiento a escrutinio** —datos, series, metodología, trazabilidad reproducible— y **“NO genera evidencia primaria”**; el seguimiento de lo financiado es de **Cooperación** (“seguimiento de lo colocado”) | adoptarlo sin acto **reabriría el solapamiento Impact/Cooperación** que `ADR-043` cerró (el error de `ADR-024`). El circuito sí se sostiene si la evidencia de resultados **vuelve a entrar por las custodias del Observatorio**, no por Impact |
| la familia son cuatro QUIRA | `ADR-043 §4`: **Economic** es línea futura — “no se elimina y no se fusiona con Cooperación” | queda donde está mientras no se decida otra cosa |

## 4 · Lo que decide la dirección

| # | decisión | recomendación de la dirección técnica |
|---|---|---|
| 1 | **sellar 2.1**: se cierra la licencia al GAD | **sellar** — resuelve la contradicción que `ADR-041 §4-ter` dejó abierta |
| 2 | **sellar 2.2**: independencia económica | **sellar** |
| 3 | **alcance de 2.2 sobre Cooperación**: ¿puede una QUIRA cobrar a una entidad observada —un GAD, una EP, un Patronato, un Cuerpo de Bomberos— por prepararle un proyecto de financiamiento? | **no dentro de QUIRA**: el usuario que paga en Cooperación es el financiador (`ADR-043 §4`). Si la entidad observada paga, obtiene la misma palanca que se quiso evitar con la licencia. Es la consecuencia más exigente del principio, y por eso la decide el fundador |
| 4 | **Impact**: ¿conserva la misión de `ADR-043` o pasa a medir resultados? | **conservarla**; la medición de resultados, como seguimiento de Cooperación y con evidencia que entra por el Observatorio |
| 5 | la **red** como norte | **guardarla como horizonte**, con sus dos condiciones (2.3) |

## 5 · Qué cambia cuando se selle — y no antes

| dónde | cambio |
|---|---|
| `BOOT §LA TESIS` | «Licencia de gestión al GAD SÍ (§4-ter)» → **NO (ADR-059)** |
| `governance/QUIRA_MASTER_INDEX.md` | ADR-059 como rector del norte del ecosistema |
| `HOJA_DE_RUTA_MAESTRA` | revisar «MOTOR 3 · QUIRA INSTITUCIONAL / GESTIÓN» a la luz de 2.1 |
| `ADR-041 §4-ter` y `ADR-043 §4` | se **superseden**, no se editan (`ADR-043 §6-bis`) |
| QUIRA 7 | **nada nuevo**: el trabajo de sujeto + dominio + evidencia + tiempo **ya es** el sustrato común que este norte necesita; `D1` sigue su curso |

---
*ADR-059 · Dylus Lab © 2026 · propuesto por la dirección técnica sobre el paréntesis de Javo y la lectura del
colega · deriva de ADR-043 · **PROPUESTO, sin sellar**.*
