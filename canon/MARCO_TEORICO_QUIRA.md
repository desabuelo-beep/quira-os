---
id: MARCO-TEORICO-001
kind: canon_teorico
level: 2
status: vigente
authority:
  parent: CONSTITUCION-001
  constitution_articles: [1, 2, 9, 13]
  type: NORMATIVA
autoria: "Javier (Javo) De Santana — postulados originales de su tesis de grado"
owner: Dylus Lab
version: "1.0"
fecha: 2026-07-27
---

# MARCO TEÓRICO DE QUIRA

**Los dos postulados de los que deriva toda la metodología · v1.0 · 2026-07-27**

> **Autoría:** ambos postulados son formulación original de **Javo**, planteados en el borrador
> de su tesis de grado, **antes** de que existiera su implementación en la plataforma.
> Este documento los registra como **fundamento declarado del canon** — no los inventa.

## Por qué existe este documento

Durante la construcción de d08 emergieron dos artefactos metodológicos: la **Matriz Canónica de
la Cadena Participativa** (C01→C09) y la categoría **Fragmentación Intersistémica**. Ambos se
atribuyeron inicialmente a la asesoría externa.

**Es una atribución incorrecta.** Ambos son la *operacionalización* de dos postulados que Javo
había formulado previamente en su tesis. La asesoría afinó la forma; el fundamento es anterior.

Esto revelaba, además, un hueco en nuestra propia cadena de autoridad (Carta Art. 1): artefactos
que declaraban su `parent` pero **no su fundamento teórico**. Este documento lo cierra.

---

## Postulado I · La Trazabilidad Biográfica del Dato
*(dimensión TEMPORAL y evolutiva de la evidencia)*

> **El dato público no es una cifra estática en una hoja de cálculo: es un organismo vivo que
> nace en el discurso político, se formaliza en la planificación, se compromete en la
> contratación y se consolida —o muere— en la ejecución presupuestaria.**

```
discurso político → planificación → contratación → ejecución → territorio
   (nace)            (se formaliza)   (se compromete)  (se consolida o muere)
```

**Consecuencia metodológica:** auditar un dato exige reconstruir su **historia de vida completa**,
sin saltarse eslabones. Un dato que aparece en la ejecución sin haber nacido en la planificación
—o una demanda que muere entre el acta y el POA— es un hallazgo, no un vacío.

**Implementaciones que derivan de este postulado:**
- `docs/brn/RO-VIII-001.yaml` → **Matriz Canónica de la Cadena Participativa** (C01→C09): la
  herramienta que audita la biografía de un mecanismo participativo eslabón por eslabón.
- Las cadenas normativas (CNO) de la BRN: la biografía jurídica de una obligación.
- El cruce `demanda → POA → PAC → presupuesto → ejecución` (RO-VIII-003, Fase 2).

---

## Postulado II · La Cadena de Integridad Intersistémica
*(dimensión ESPACIAL y relacional de la evidencia)*

> **La transparencia no se mide evaluando sistemas aislados, sino verificando la coherencia
> entre ellos. Los municipios operan en silos; la integridad nace cuando los sistemas del Estado
> están obligados a dialogar.**

**Consecuencia metodológica:** cuando el CPCCS declara *"existe"* y el Portal de Transparencia
dice *"no existe"*, el marco no detecta solo la falta de un papel: **nombra y mide la ruptura de
la cadena de integridad entre sistemas del Estado**.

**Implementaciones que derivan de este postulado:**
- `governance/GOVERNANCE_CHARTER.md` Art. 4.5 → 5ª categoría **Fragmentación Intersistémica**.
- El índice de cumplimiento institucional (motor): la congruencia intersistémica es su objeto.
- Nodo **C09 · publicidad intersistémica** de la Matriz Canónica.
- OBS-017 §hallazgo cruzado d08↔d07 (RDC declara ejecutado / transparencia no lo publica).

---

## Lo que ambos postulados comparten

Un mismo principio rector, señalado por la asesoría externa (2026-07-27):

> **Ninguna transformación puede perder su trazabilidad.**

El Postulado I lo aplica **en el tiempo** (del discurso a la ejecución); el Postulado II **en el
espacio institucional** (entre sistemas del Estado). Juntos definen qué es, para QUIRA, la
integridad: no la ausencia de faltas, sino la **reconstructibilidad completa de la cadena**.

## La dimensión que esto abre — integridad procedimental

El índice de cumplimiento medía hasta ahora, sobre todo, **congruencia programática** (¿la
demanda llegó al POA?). Los postulados habilitan una dimensión distinta: la **integridad
procedimental** — *¿llegó mediante un procedimiento institucionalmente íntegro?*

No basta con que una demanda alcance el POA: importa si el mecanismo que la recogió tenía
convocatoria, presidencia acreditada, habilitación, resolución y publicidad congruente. Esa es
la contribución que la Matriz Canónica hace posible.

## Frontera obligatoria para la Fase 2 (asesoría · 2026-07-27)

Al entrar al cruce semántico aparecerá inevitablemente interpretación. Se mantiene una
separación **estricta y explícita**:

| **Hechos observables** *(QUIRA certifica)* | **Inferencias analíticas** *(QUIRA propone, el humano valida)* |
|---|---|
| la demanda existe · el proyecto existe · hay coincidencia textual · existe partida presupuestaria · existe ejecución | *"esta demanda fue satisfecha"* · *"este proyecto responde a aquella necesidad"* |

Todo resultado del cruce debe declarar en cuál de las dos columnas cae. Concuerda con la
Constitución Art. 3 (la IA interpreta, no es fuente de verdad) y con el Principio de
No-Inferencia (Carta Art. 4.5).

---
*Marco Teórico de QUIRA v1.0 · postulados de Javo · Dylus Lab © 2026 · deriva de CONSTITUCION-001.*
