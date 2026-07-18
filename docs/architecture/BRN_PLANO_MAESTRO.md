# BRN v2 · Plano Maestro — Arquitectura General

> **Qué es este documento.** El **mapa** que integra todas las piezas de la BRN v2. No decide nada
> nuevo: muestra **cómo se relacionan** las decisiones ya tomadas (ADR-035/037/038/039 + el molde)
> para que se lean como **un solo sistema**, no como cuatro ADR sueltos (ADR-039 nota del colega ·
> 2026-07-18). A partir de aquí, los ADR documentan decisiones **sobre este plano**; no lo construyen
> pieza por pieza.

**Estado:** VIGENTE como mapa · 2026-07-18 (se cierra tras el ciclo de vida y el molde · ADR-039 nota)
**Ámbito:** conceptual. La implementación (piloto, catálogo) ya empezó y este plano la ordena.

---

## 1. La BRN en una frase
> La **BRN** transforma el ordenamiento jurídico vigente en **reglas operativas únicas, trazables y
> reutilizables** por las SAT, los DOM y QUIRA IA, manteniendo **un único punto de verdad normativa**
> (ADR-038). No calcula (eso es el Gold Master), no interpreta (eso es la validación humana): **consolida**.

## 2. Las cinco capas — quién hace qué
```
   QUIRA IA · DOM · dashboards · informes          ← CONSUMEN (explican, no deciden)
        │
        ▼
   SAT  ── lleva solo el ID de su RO                ← MIDE (Gold Master computa)
        │
        ▼
   RO   ── variable · umbral · periodo              ← OPERACIONALIZA (no interpreta · Neutralidad Op.)
        │
        ▼
   CNO  ── la cadena jurídica completa              ← REPRESENTA el Derecho (puro Derecho)
        │
        ▼
   Corpus ── texto oficial + SHA256                 ← PRUEBA (la verdad vive aquí)
   ════════════════════════════════════════════════════════════════════════════
   Gold Master  ── motor matemático inmutable       ← EJECUTA (recibe config COMPILADA, no consulta)
```
**Regla de oro del plano:** el conocimiento **baja** para probarse (IA→RO→CNO→Corpus) y **sube**
compilado para ejecutarse (RO→[compilador]→Gold Master). Nunca la BRN escribe al motor en runtime.

## 3. Cómo encaja cada ADR (el mapa de decisiones)
| Pieza | Qué decidió | Rol en el plano |
|---|---|---|
| **ADR-035** | la BRN existe · la IA propone, el humano valida | **regla constitucional** — gobierna todo el ciclo |
| **ADR-037** | frame de 4 dimensiones (Gobierno·Territorio·Inteligencia·Norma) | la **cara visible** de la BRN (su cajón = 4ª lente) |
| **ADR-038** | el nodo es la REGLA (CNO), no el artículo · 4 niveles · MDN | el **corazón** — define CNO/RO/MDN |
| **ADR-039** | Estado ≠ Configuración · compilación de la RO al motor | el **puente** BRN → Gold Master sin romper Regla 1 |
| **Molde** (`BRN_CICLO_VIDA_Y_MOLDE`) | ciclo de vida + estructura CNO/RO + 7 preguntas | el **contrato** estable sobre el que se construye |
| **Corpus** (`PROTOCOLO_CURACION_CORPUS_BRN`) | qué se sube y cómo se cura | la **base** — sin SHA no hay eslabón |

## 4. El flujo de una regla, de la ley al informe (síntesis del ciclo)
```
norma nueva → FUENTE → Corpus (SHA) → PROPUESTA de CNO → VALIDACIÓN HUMANA (Javo · ADR-035 §5)
   → CNO vigente → RO → [COMPILADOR · ADR-039] → Gold Master → SAT → DOM → dashboard → informe
```
Un solo punto de intervención humana (la validación de la CNO); lo demás es mecánico y trazable.

## 5. El MDN — por qué esto es un sistema de gestión del cambio, no una lista
La BRN es un **grafo de dependencias** (Modelo de Dependencias Normativas · ADR-038 §9; implementación
recomendada Neo4j, ya en el stack). Cada CNO, RO, SAT y DOM es un nodo; las dependencias, aristas. Una
reforma deja de decir *"cambió el Art. 198"* y dice *"cambió CNO-IV-001 → 1 RO → 1 SAT → d02 → informes"*.
**Trazabilidad bidireccional** (Principio de Dependencia Normativa): todo activo reconstruye su
fundamento hasta el texto oficial, y todo texto sabe qué activos dependen de él.

## 6. Gobernanza — propietario y estabilidad (del molde, Parte VI)
| Corpus | CNO | RO | Compilación | Gold Master | SAT |
|---|---|---|---|---|---|
| Estado · **alta** | Dylus·jurídica · media | Dylus·operativa · media | proceso · baja | motor · **muy baja** | consumidor · casi nunca |
La BRN vive **entre** el Corpus (cambia seguido) y el Gold Master (casi nunca): **absorbe el cambio
jurídico sin tocar el motor**. Esa es su razón de ser.

## 7. Las tres salvaguardas que nunca se cruzan
1. **Regla 3** — sin SHA no hay eslabón; la cadena íntegra o la CNO no es vigente (imposibilita el "65% = Art. 192").
2. **Regla 1** — el Gold Master recibe configuración compilada; nunca consulta la BRN en runtime.
3. **ADR-035 §5** — ninguna IA promueve a `vigente`; la interpretación jurídica es humana (Neutralidad Operativa).

## 8. Estado actual y frontera
- **Cerrado:** doctrina (ADR-035/037/038/039), molde (ciclo+CNO/RO), piloto **CNO-IV-001** (6/6 eslabones
  íntegros → RO-IV-001), catálogo de CNO (`brn_cno.py` · MDN como datos). Todo en estado `propuesta`.
- **Pendiente — en el orden del colega (probar la gobernanza antes que el motor · 2026-07-18):**
  1. **Validación humana** del piloto por Javo → `propuesta` a `vigente` (CNO-IV-001 · RO-IV-001).
  2. **Reforma simulada** — cambiar un umbral o agregar un artículo ficticio y comprobar que la
     propagación documental (Corpus→CNO→RO→SAT→DOM) se comporta **exactamente como está descrita**,
     ANTES de escribir una línea de integración con el motor.
  3. Solo entonces la implementación: compilador RO→Gold Master (ADR-039), migrar la cadena del
     mandato (d03) y las SAT financieras, y ampliar el Corpus (2ª fase · Municipio 002+).

---
*BRN v2 · Plano Maestro · Dylus Lab © 2026 · "Cuatro ADR, un molde y un corpus dejaron de ser piezas sueltas: son una sola capa que consolida el Derecho en reglas, lo prueba con SHA y lo entrega compilado al motor — sin interpretarlo, sin calcularlo, sin tocarlo."*
