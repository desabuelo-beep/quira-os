# ADR-039 · Compilación de Reglas Operativas hacia el Gold Master

**Estado:** PROPUESTO · 2026-07-17 (síntesis del colega · director técnico redacta) · **pendiente de ratificación**
**Contexto de origen:** al cerrar el ADR-038 quedó una contradicción: *"la BRN explica al Gold
Master, no lo gobierna"* + *"el Gold Master es fuente autónoma del cálculo"* producen **dos
verdades del mismo parámetro** (el 65% viviría en la RO **y** estampado en Excel). Eso rompe el
principio de **único punto de verdad normativa** que el ADR-038 construye. El colega resuelve la
contradicción sin tocar la Regla 1.
**Relacionado:** ADR-038 (BRN · define la RO) · ADR-023 (Regla 1 · Gold Master inmutable · flujo
Excel→Python→Supabase→UI) · ADR-031 (Gold Master = MCM) · Regla 4 (no recalcular el motor).

---

## Contexto — la distinción que faltaba: ESTADO ≠ CONFIGURACIÓN

La Regla 1 protege el **estado calculado**: `Excel → Python → Supabase → UI, nunca al revés`. Pero
un umbral como el `65` en `H24` **no es estado — es configuración** (parámetro de entrada). El flujo
de la Regla 1 habla de *dónde va el resultado*, no de *dónde salen los parámetros*. Confundir ambos
fue lo que hizo parecer que "el Gold Master debe consultar la BRN" violaba la Regla 1.

| | **Estado** | **Configuración** |
|---|---|---|
| Qué es | el resultado del cálculo (ICPI, Ti, SAT…) | variable · umbral · periodicidad · consecuencia |
| Quién manda | **Excel, siempre** (Regla 1) | la **RO** (ADR-038) |
| Hoy vive en | Excel | Excel **y** la RO ← duplicación a resolver |

## Decisión

### 1. El Gold Master recibe su configuración COMPILADA — nunca la consulta
La RO no alimenta al motor en runtime (eso sí rompería la Regla 1). Se introduce un paso de
**compilación**, previo a la ejecución:
```
Corpus → CNO → RO → [ COMPILADOR ] → Gold Master (ya configurado) → calcula → estado
```
El Gold Master **nunca pregunta, nunca consulta, nunca abre una API ni Neo4j**. Nace **ya
configurado** desde un artefacto que el compilador genera **una sola vez**. Después, Excel hace lo
suyo — el estado se calcula igual que hoy. **La Regla 1 queda intacta.**

### 2. Un único punto de verdad de la configuración: la RO
El 65% vive **solo en la RO-IV-001**. El compilador lo lleva a la tabla de parámetros que consume
el Gold Master. **No se vuelve a escribir a mano en Excel.** Cuando la norma cambia (65 → 70), se
edita **un solo lugar** (la RO); se recompila; el nuevo artefacto configura el motor. Adiós a las
dos verdades.

### 3. Separación conceptual: Gold Master Matemático vs. Configurado
- **Gold Master Matemático** — solo fórmulas, relaciones y operaciones. **Nada jurídico.** Es el
  motor inmutable (la fórmula canónica `H12!B33` no se toca jamás).
- **Gold Master Configurado** — el matemático **+ la tabla de parámetros compilada** desde las RO.
  Es lo que se ejecuta. Los parámetros entran por **compilación**, no por runtime ni a mano.

### 4. LÍMITES DUROS (heredados)
- **La compilación NO toca la fórmula canónica** (`H12!B33` · Regla 1 · Prohibición). Solo escribe
  la **tabla de parámetros** (umbrales, periodicidades) — inputs, nunca la lógica de cálculo.
- **Sigue siendo sobre COPIA, con evidencia y dumps** (metodología del Gold Master): el compilador
  no escribe el canon vivo directamente; genera el artefacto, se verifica, y recién se promueve.
- **La IA propone, Javo valida** (ADR-035 §5): una RO no se compila al motor hasta estar `vigente`.

## Consecuencia práctica

Resuelve la duplicación que el ADR-038 no podía resolver solo: **el conocimiento normativo vive en
la RO; el motor solo lo ejecuta.** El caso del 65% deja de tener dos hogares. Y el grafo normativo
(ADR-038 §9) se extiende hasta el final de la cadena: una reforma se propaga
`CNO → RO → [recompilar] → Gold Master → SAT → DOM → dashboard → informe` — trazabilidad completa
del cambio normativo, algo que ningún software municipal tiene.

**Pendiente de diseño** (tras ratificar): el formato del artefacto compilado, cómo el compilador
localiza los parámetros en el Gold Master sin tocar fórmulas, y el disparo de recompilación cuando
una RO cambia de estado. Es **implementación** — no se toca Python hasta cerrar el ciclo de vida y
el molde CNO/RO del ADR-038.

---
*ADR-039 · Compilación de Reglas Operativas · Dylus Lab © 2026 · "La Regla 1 protege el estado, no la configuración. El Gold Master no consulta la ley: nace ya configurado por un compilador que lee la RO. El 65% vive en un solo lugar — y cuando la norma cambie, se cambia una vez."*
