# ADR-032 · Motor de Biografía — la unidad narrativa canónica de QUIRA

**Estado:** RATIFICADO · 2026-07-11 (Javo + colega + auto-revisión del director técnico)
**Contexto de origen:** FASE 1.5 · Consolidación Canónica. La sesión reveló que el verdadero producto
que emergió no es Neo4j — es la **BIOGRAFÍA de la meta** (colega: *"el corazón narrativo de QUIRA"*).
**Relacionado:** ADR-029 (fuente→canon · el modelo integra, la verdad vive en la fuente) · ADR-031
(5 motores tipados MCIP) · `TRES_CEREBROS_QUIRA.md` · Constitución CAPA 0 (Principio Rector).

---

## Contexto

La biografía de una meta —su vida documental de la promesa al gasto, a través de los años— emergió como
la **unidad narrativa central** del observatorio. Un porcentaje aislado no explica nada; una biografía, sí.
FASE 1.5 la consolida como **objeto canónico**, y —fiel al Principio Rector— declara sus fronteras en vez
de fingir completitud.

## Decisión

1. **La Biografía es un OBJETO canónico de primer orden** (como la meta o la partida): la vida documental
   de un compromiso público, con identidad propia.
2. **El Motor de Biografía es un motor de SÍNTESIS**, NO un 6º motor tipado (Regla 7 · ADR-031): *compone*
   la salida de los motores tipados (Matemático · Documental · Relacional · Prospectivo) en una narrativa
   verificable. Igual que el sintetizador de hallazgos y el motor Relacional. **Nombre en español** (no
   `BIOGRAPHY_ENGINE` · Bloomberg Firewall).
3. **Cada campo de la biografía lleva su NIVEL DE VERIFICABILIDAD** (QUIRA certifica el nivel, no inventa):

| Campo (¿qué responde?) | Nivel de verificabilidad | Fuente |
|---|---|---|
| ¿Dónde nació? (PDOT · año) | **verificado** | PDOT / POA |
| ¿Cuántas veces apareció? | **verificado** (2025) · **inferido** (previos, vía partida determinista) | POA multi-año |
| ¿Qué actividades tuvo? | **verificado** | POA oficial (Excel) |
| ¿Qué presupuesto planificó? | **verificado** | POA oficial |
| ¿Qué % ejecutó? | **DOMINIO** (agregado, p.ej. 73%) — **NO per-meta** | cédula (partida compartida) |
| ¿Qué contratos generó? | **DOMINIO** ($4.9M · 109 procesos) — per-meta solo subconjunto exclusivo (23/109) | PAC oficial (docx) |
| ¿Qué reformas sufrió? ¿Cómo terminó? | *ausencia documentada* | — |

**Hallazgo estructural definitivo (FASE 1.5 · investigado ejecución Y contratos):** la cadena
`meta↔actividad↔partida` es **limpia** (del POA fuente), pero **aguas abajo la partida presupuestaria
se comparte entre metas** — por tanto *todo lo que cuelga de la partida (ejecución, contratos, reformas)
no es atribuible limpiamente por meta*. No es un defecto de QUIRA: es la estructura presupuestaria del
GAD (partidas genéricas). La atribución exclusiva (partidas deterministas) captura solo el subconjunto
pequeño/específico; los ítems grandes (obras) van por partidas compartidas. **Conclusión: el núcleo
verificado de la biografía es la CADENA DEL PLAN; aguas abajo se reporta a nivel de dominio.**

## Límite documentado (la honestidad que distingue a QUIRA)

**La ejecución NO es atribuible limpiamente por meta.** Las partidas presupuestarias son **compartidas**
entre varias metas, y el GAD **no publica ejecución a nivel de actividad** (el POA trae el cronograma
*planificado*, no el devengado real por actividad; la cédula devenga por *partida*). La atribución
*exclusiva* (solo partidas propias) captura muy poco e inconsistente; la *total* sobre-cuenta. Por el
**Principio Rector** —*la ausencia de evidencia es un resultado, nunca una autorización a inferir*— la
ejecución per-meta se reporta a nivel de **dominio** (agregada, verificada) o como **ausencia declarada**,
jamás estimada como si fuera dato per-meta.

## Consecuencias

- La biografía es el **corazón narrativo**; sus objetos limpios alimentan **Neo4j** (memoria relacional) y
  **QUIRA IA** (la capa conversacional · = "Sentinel"). Primero el objeto, después el grafo.
- **FASE 1.5 = consolidar el objeto + declarar sus fronteras**, no fabricar granularidad. La memoria
  institucional *completa* (ejecución/contratos/reformas per-meta) exige una fuente más rica —ejecución a
  nivel de actividad— que hoy **no existe públicamente**. Esa ausencia es, en sí misma, un hallazgo de
  verificabilidad del GAD, no un defecto de QUIRA.

---
*ADR-032 · Motor de Biografía · Dylus Lab © 2026 · "QUIRA no inventa la historia de una meta: la reconstruye hasta donde la fuente la sostiene, y declara dónde la fuente calla."*
