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
| ¿Qué contratos generó? | **reconciliado PAC↔POA por descripción** (100/109 · 92% · confianza alta) | POA + PAC oficial |
| ¿Qué reformas sufrió? ¿Cómo terminó? | *ausencia documentada* | — |

**Hallazgo (FASE 1.5) — y la INNOVACIÓN que salta el muro (corrección de Javo · 2026-07-11):**
La atribución **RAW por partida** es limitada: la partida se comparte entre metas (estructura del sistema
SERCOP / presupuesto del GAD). *Declararlo como muro fue prematuro.* QUIRA lo **SALTA** con **reconciliación
intersistémica por DESCRIPCIÓN**: el POA y el PAC describen el **mismo trabajo real** → el matching de
descripción (restringido a la misma partida) atribuye el proceso a la actividad → su meta. **92% de los
procesos, alta confianza (0.78–0.98).** Esto **no es inferencia** —es reconciliar dos fuentes del mismo
hecho—, y es precisamente la *cadena de integridad intersistémica* que define a QUIRA como inteligencia,
no como tablero. **Regla:** cuando el dato existe pero la estructura lo esconde, QUIRA innova para
reconciliarlo; solo declara ausencia cuando el dato **no existe** en ninguna fuente.

**Ejecución real per-meta — investigado (2026-07-11) · la lección en ambos sentidos:** intenté cerrar el
eslabón `ejecutó` por SERCOP real (H06). Resultado: para el GAD 2025 el SERCOP publicado es **genuinamente
escaso** —20 contratos, *por_verificar*, la descripción es el **nombre del proveedor** (no el objeto)—; y la
cédula devenga por **partida compartida**. A diferencia del PAC (info *escondida por la estructura*, que se
**recupera** por reconciliación), aquí el dato **es thin en la fuente**: el GAD publicó poco en SERCOP 2025.
**Esconder ≠ no existir:** lo primero se innova, lo segundo se **declara**. → Ejecución real per-meta 2025 =
**nivel de dominio** (Ti 73%); la escasez del SERCOP es, en sí, un hallazgo de transparencia del GAD.
**Núcleo verificado de la biografía: nació → planificó → contrató (planificado).**

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

## Principio rector — la contribución metodológica (Javo · 2026-07-11, cierre de sesión)

> **La Biografía Administrativa es un OBJETO CANÓNICO reconciliado entre sistemas heterogéneos — y ese
> concepto es más potente que cualquier tecnología concreta.**
> Neo4j puede cambiar. Supabase puede cambiar. Python puede cambiar. Pero la idea de que **un compromiso
> público tiene una biografía verificable desde que nace hasta que termina** es una **contribución
> metodológica** que sobrevive a todas esas herramientas.

**Implicación estratégica:** el valor de QUIRA no reside en su *stack* (reemplazable) sino en el **método**
—reconstruir, desde fuentes heterogéneas que hablan del mismo hecho, la vida verificable de cada compromiso,
declarando el nivel de verificabilidad de cada eslabón—. *Las herramientas implementan; el método permanece.*
Esto es lo publicable (tesis / estándar), lo escalable a los 221 GAD, y lo que ninguna migración tecnológica
puede volver obsoleto. La Biografía Administrativa es la contribución de QUIRA a la ciencia de la gestión pública.

---
*ADR-032 · Motor de Biografía · Dylus Lab © 2026 · "QUIRA no inventa la historia de una meta: la reconstruye hasta donde la fuente la sostiene, y declara dónde la fuente calla. Las herramientas implementan; el método permanece."*
