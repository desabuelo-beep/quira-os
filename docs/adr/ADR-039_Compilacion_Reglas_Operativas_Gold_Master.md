# ADR-039 · Compilación de Reglas Operativas hacia el Gold Master

**Estado:** ACEPTADO CONCEPTUALMENTE · 2026-07-17 (síntesis del colega · director técnico redacta)
· *no "cerrado": el contrato del compilador —entradas, salidas, versionado, artefactos— se
especifica en el documento del ciclo de vida (precisión del colega · 2026-07-17)*
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
El Gold Master **nunca pregunta, nunca consulta, nunca abre una API ni un grafo**. Nace **ya
configurado** desde un artefacto que la Compilación Operativa **materializa una sola vez**. Después,
Excel hace lo suyo — el estado se calcula igual que hoy. **La Regla 1 queda intacta.**

**La Compilación Operativa es un PROCESO, no un software** (precisión del colega): *proceso mediante
el cual una Regla Operativa vigente se transforma en un artefacto de configuración compatible con el
Motor Canónico de Medición.* Puede ejecutarse con Python, Excel, Power Query, GitHub Actions o a
mano — es una **etapa del pipeline**, no un programa. Así el canon sobrevive aunque cambie la
tecnología. El compilador **no modifica** el Gold Master: **produce** un artefacto compatible con él.

**El compilador NO decide — solo materializa** (precisión del colega · 2026-07-17): *la compilación
es un proceso de construcción de artefactos, no un proceso de decisión jurídica. El compilador no
interpreta la norma ni calcula resultados; únicamente materializa una Regla Operativa previamente
validada en un formato consumible por el Gold Master.* Esto separa cuatro roles que nunca deben
confundirse: **interpretación jurídica** (humana, sobre el Corpus) · **validación** (Javo, ADR-035
§5) · **compilación** (mecánica, sin criterio) · **ejecución** (el Gold Master). Nadie convierte el
compilador en un "motor inteligente".

**El compilador debe ser DETERMINISTA, REPRODUCIBLE e IDEMPOTENTE** (colega · 2026-07-17): la misma
RO produce siempre el mismo artefacto; recompilar sin cambios no altera nada. Sin esas tres, la
trazabilidad se rompe.

### 5. Trazabilidad de la versión jurídica del cálculo (agenda del ciclo de vida)
El Gold Master debe **registrar de qué versión de RO fue configurado**, para poder responder *"¿con
qué versión jurídica se calculó este ICPI?"* — hoy esa traza está incompleta. Se especifica en el
documento del ciclo de vida:
```
RO-IV-001 v3.2 → Compilación → Gold Master build 2026.07.18 (guarda: RO usada · versión · SHA · fecha)
```

### 2. La RO es la única REPRESENTACIÓN OPERATIVA AUTORIZADA de la configuración
La RO **no es "la verdad"** —la verdad sigue siendo la norma (precisión del colega · 2026-07-17):
la RO es la única **representación operativa autorizada** de una regla normativa. Nunca reemplaza
al Derecho. El umbral 65% se especifica **solo en la RO-IV-001**; el compilador lo **materializa**
en el artefacto de configuración del Gold Master. **No se vuelve a escribir a mano en Excel.**
Cuando la norma cambia (65 → 70), se edita **un solo lugar** (la RO); se recompila; el nuevo
artefacto configura el motor. Adiós a las dos verdades.

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

**Nota de método (advertencia del colega · 2026-07-17):** la BRN v2 ya se articula en subsistemas
(Corpus · CNO · RO · MDN · Compilación Operativa) sobre 3 ADR (035/038/039). Antes de abrir un
ADR-040, se escribirá un **plano maestro — "Arquitectura General de la BRN v2"** que mapee cómo se
relacionan estos ADR; los ADR pasan a documentar decisiones sobre ese plano, no a construirlo pieza
por pieza. Con 3 ADR aún se lee bien; el plano se escribe al cerrar el ciclo de vida y el molde.

---
*ADR-039 · Compilación de Reglas Operativas · Dylus Lab © 2026 · "La Regla 1 protege el estado, no la configuración. El Gold Master no consulta la ley: nace ya configurado por un compilador que lee la RO. El 65% vive en un solo lugar — y cuando la norma cambie, se cambia una vez."*
