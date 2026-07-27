---
id: CONSTITUCION-001
kind: identity
level: 0
status: vigente
authority:
  parent: null                    # RAÍZ del árbol de autoridad — no deriva de nada
  type: CONSTITUCIONAL
owner: Dylus Lab
version: "1.0"
fecha: 2026-07-25
saneada: 2026-07-27
---

# CONSTITUCIÓN INSTITUCIONAL DE QUIRA

**Documento Fundacional · v1.0 · 2026-07-25** · *(saneada 2026-07-27)*

> **Órgano productor:** Constituyente. Este documento responde a UNA sola pregunta:
> **¿qué nunca puede cambiar sin dejar de ser QUIRA?** Todo lo demás —cómo se gobierna,
> cómo se modela el conocimiento, cómo se implementa— pertenece a niveles inferiores
> (Carta de Gobernanza · Canon · Implementación). No contiene especificaciones técnicas.

## Nota de saneamiento (2026-07-27)

El documento fuente (`Constitución QUIRA OS.txt`) contenía **dos versiones con numeración
incompatible** (una de Art. 0-30 y otra de Art. 1-21), lo que rompía toda referencia de
autoridad del tipo `constitution_articles: [2, 5, 9]`. Por decisión de Javo se adopta la
**Versión B (Art. 1-21)** como numeración oficial; la otra queda **derogada**. Registrado en
`governance/decisions/DEC-0001.md`.

## Relación con la Constitución Ontológica

QUIRA tiene **dos documentos de identidad, no en conflicto** — cada uno con su objeto:

| Documento | Responde | Ubicación |
|---|---|---|
| **Constitución Institucional** (este) | ¿Qué ES QUIRA como institución de conocimiento? | `identity/` |
| **Constitución Ontológica** | ¿Qué ES la integridad territorial que QUIRA observa? | `docs/sprint-c/CONSTITUCION_ONTOLOGICA_QUIRA.md` |

La Ontológica define el **objeto observado** (el GAD, sus 4 macroejes y 13 dominios); esta
define el **sujeto observador** (QUIRA y su gobernanza del conocimiento). Ambas son L0.

---

## Preámbulo

La evidencia pública debe poder transformarse en conocimiento verificable mediante procesos de
gobernanza, trazabilidad y preservación.

La presente Constitución constituye simultáneamente la **Plataforma**, el **Método** y el
**Patrimonio Cognitivo** que conforman QUIRA. QUIRA es una plataforma de inteligencia pública
orientada a materializar este principio.

Esta Constitución establece los principios inmutables, las definiciones fundacionales y la
arquitectura conceptual de QUIRA, como infraestructura de conocimiento verificable al servicio
de los gobiernos, la ciudadanía, la academia y la cooperación internacional.

---

## Título I · Principios Inmutables

**Artículo 1.** Toda afirmación sobre la gestión pública debe poder verificarse mediante
evidencia documental.

**Artículo 2.** La evidencia documental prevalece sobre cualquier narrativa, interpretación o
declaración institucional.

**Artículo 3.** La inteligencia artificial no constituye fuente de verdad institucional. Su
función es exclusivamente interpretar conocimiento sustentado en evidencia verificable.

**Artículo 4.** El conocimiento público pertenece al territorio que lo genera y debe preservarse
como patrimonio de la comunidad.

**Artículo 5.** La gobernanza del conocimiento es condición necesaria para la confianza
institucional.

**Artículo 6.** Cada incorporación al sistema incrementa el valor del patrimonio cognitivo
colectivo.

**Artículo 7.** El conocimiento nunca sustituye la evidencia; emerge de ella.

**Artículo 8. Neutralidad institucional.** QUIRA no produce decisiones públicas ni reemplaza la
autoridad competente. Su función consiste exclusivamente en organizar, preservar e interpretar
evidencia verificable.

**Artículo 9. Trazabilidad.** Toda inferencia generada por la Plataforma deberá conservar la
cadena completa de trazabilidad hacia la evidencia que la sustenta.

---

## Título II · Definiciones Fundacionales

**Artículo 10. De la Verdad Verificable**

Se entiende por verdad verificable toda afirmación cuya trazabilidad documental pueda
reconstruirse íntegramente mediante evidencia, reglas de gobernanza y registro de eventos.

**Artículo 11. De la Gobernanza del Conocimiento**

La Gobernanza del Conocimiento es el conjunto de reglas, procesos, responsabilidades y
mecanismos mediante los cuales la evidencia es validada, preservada, versionada e interpretada
para convertirse en conocimiento verificable.

**Artículo 12. De la Jerarquía del Conocimiento**

| Concepto | Definición |
| :--- | :--- |
| **Evidencia** | El dato primario, el documento, el registro administrativo. |
| **Memoria Pública Digital** | El repositorio estructurado de la evidencia. |
| **Patrimonio Cognitivo Público** | El conjunto de conocimiento preservado, organizado y gobernado. |
| **Capital Cognitivo Público** | El valor económico, institucional y estratégico que ese patrimonio genera. |
| **Inteligencia Pública** | La capacidad de tomar decisiones informadas a partir de ese capital. |

```
Evidencia → Memoria Pública Digital → Patrimonio Cognitivo Público
          → Capital Cognitivo Público → Inteligencia Pública
```

---

## Título III · De la Tesis Fundacional

**Artículo 13.** QUIRA transforma evidencia administrativa dispersa en patrimonio cognitivo
público.

---

## Título IV · De la Arquitectura de Capacidades

**Artículo 14.** La plataforma QUIRA se organiza en una arquitectura de capacidades que
distingue:

```
                    QUIRA PLATFORM
                         │
           ┌─────────────┴─────────────┐
      QUIRA FABRIC               QUIRA METHOD
      (activo cognitivo)      (metodología de gobernanza)
           └─────────────┬─────────────┘
                QUIRA CORE ENGINE
             (ejecución y gobernanza)
                         │
                COGNITIVE LAYER
                         │
   Interfaces: gobiernos · ciudadanía · observación
               impacto · cooperación · economía
```

La Plataforma podrá ofrecer múltiples interfaces especializadas. La nomenclatura y el número de
estas interfaces puede evolucionar; lo que permanece es que **todas comparten la misma fuente de
evidencia verificable**.

---

## Título V · De los Componentes Permanentes

**Artículo 15. QUIRA Fabric.** Capa donde la evidencia se transforma en conocimiento
estructurado y gobernado: grafo de conocimiento territorial, corpus verificado con hash SHA-256,
y event sourcing (registro inmutable de cada decisión y validación).

**Artículo 16. QUIRA Method.** Metodología para construir conocimiento institucional verificable.
Permite consultoría, certificación, capacitación e investigación sin necesidad de escribir código.

**Artículo 17. QUIRA Core Engine.** Ejecuta la gobernanza del conocimiento: ingesta, validación,
curaduría y normalización.

**Artículo 18. Cognitive Layer.** Interpreta el conocimiento mediante agentes especializados
(Navigator, Collector, Interpreter, Reporter) que traducen preguntas en respuestas verificables.
Nunca reemplaza ni sustituye la evidencia.

---

## Título VI · Del Foso Competitivo

**Artículo 19.** Un competidor puede desarrollar una plataforma similar. Lo que no puede
reproducirse es el patrimonio cognitivo acumulado, gobernado y verificable que constituye
QUIRA Fabric.

---

## Título VII · Disposiciones Finales

**Artículo 20. De la inmutabilidad de la Constitución.** Esta Constitución es el documento
fundacional de QUIRA. Sus principios, definiciones y artículos son inmutables. Cualquier
evolución futura deberá ser compatible con ella. Las modificaciones solo podrán realizarse
mediante proceso de enmienda que requiera la aprobación del equipo fundador y la constatación
de que preserva la identidad y los principios de la plataforma.

**Artículo 21. De los documentos derivados.** De esta Constitución derivan los siguientes
artefactos, que se actualizarán periódicamente:

1. **Carta de Gobernanza** (`governance/GOVERNANCE_CHARTER.md`) — cómo se gobierna QUIRA.
2. **Canon Institucional** (`canon/`) — cómo modela QUIRA el conocimiento normativo.
3. **Plan Estratégico · White Paper · Investor Deck · QUIRA Method · Manifiesto.**

---

## Cierre Institucional

> **La evidencia permanece. El conocimiento se acumula. La confianza se construye.**

QUIRA convierte evidencia administrativa en capital cognitivo público, para fortalecer la
inteligencia territorial y la confianza institucional. Su identidad no reside en sus interfaces,
sino en la preservación, organización e interpretación del conocimiento público verificable.

---

## Anexo · Definición síntesis

> **Los gobiernos producen evidencia. QUIRA preserva, organiza e interpreta esa evidencia para
> convertirla en conocimiento verificable.**

---

*QUIRA Constitution v1.0 · congelada · Dylus Lab © 2026 · Montecristi = Municipio 001.*
