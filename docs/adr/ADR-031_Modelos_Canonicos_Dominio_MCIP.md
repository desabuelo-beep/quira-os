# ADR-031 · Modelos Canónicos de Dominio (MCD) y el MCIP — reconciliación, no refundación

**Estado:** RATIFICADO · 2026-06-29 (Javo) · refrendado por el asesor en 2ª vuelta (alineado tras revisión)
**Origen:** propuesta de la mesa — asesor: "reorganizar QUIRA por capas horizontales · cajón = Modelo
Canónico, no dashboard · 5 motores"; académico: "tracer bullet vertical sobre QINV-001". Revisado por
dirección contra el canon vigente (Regla #6 · anti-amnesia) y refrendado por el asesor en 2ª vuelta.
**Alcance estricto:** NO redefine arquitectura. Toma SOLO lo genuinamente nuevo y resuelve dos colisiones.
**Relacionado / NO duplica:** `ARQUITECTURA_CANONICA.md` (6 capas) · `ADR-029` (Modelo Canónico Matemático) ·
`ADR-026` (Topología Funcional de dominios) · `ADR-023` (3 niveles) · `DICCIONARIO_CONCEPTUAL_QUIRA.md`
(13 ADN · contenido sellado) · `ADR-030` (render).

---

## Por qué existe (y por qué NO refunda)

La mesa propuso pensar QUIRA "en capas horizontales" y cada cajón como "Modelo Canónico". Revisión de
dirección: **~85% de eso YA es canon ratificado.** El flujo de 6 capas (GoldMaster→Pipeline→Supabase→
Streamlit+Obsidian+GitHub) está en `ARQUITECTURA_CANONICA`; el Excel-como-conector y el Gold Master como
Modelo Canónico en `ADR-029`; la topología tipada de dominios (Norma→Observación→Interpretación→Validación)
en `ADR-026`. Redibujar todo sería **redefinir lo sellado — y el que redefine se detiene** (Regla #6).

> Es el mismo patrón que `ADR-030` ya cazó: *"la mesa re-derivó una anatomía de '4 preguntas' sin recordar
> el ADN ya sellado."* Este ADR no repite el error: deriva del canon, nombra lo nuevo, resuelve colisiones.

---

## §0 · La jerarquía en 3 niveles (síntesis · asesor 2ª vuelta)

> **No existe "un cajón de Planificación". Existe un Modelo Canónico de Planificación Estratégica que
> casualmente se visualiza mediante un cajón.**

```
Nivel 1 — MCM   Modelo Canónico Matemático = el Excel. Nunca cambia. Es la verdad.
Nivel 2 — MCD   Modelo Canónico de Dominio (uno por dominio: Planificación, Gobernanza,
                Transparencia, Inclusión…). Sabe qué indicadores, relaciones, leyes,
                algoritmos, IA y vista usar para responder la pregunta de su ADN.
Nivel 3 — VISTA Dashboard · Grafo · Sankey · Flujo · Timeline · GeoTwin · Simulación.
                Aparece AL FINAL — es UNA de muchas vistas del MCD, jamás el punto de partida.
```

---

## §1 · Disambiguación obligatoria de "Modelo Canónico" (resuelve colisión 1)

`ADR-029` ya fijó: **Modelo Canónico = el Gold Master** (la verdad matemática · forma física reemplazable).
La mesa reusó "Modelos Canónicos" para los modelos *por cajón* → mismo nombre, cosa distinta. Se fija:

- **MCM — Modelo Canónico Matemático** = el Gold Master. Única autoridad de cálculo (Regla 1 · `ADR-023` Regla 4).
  Inmutable (H12!B33). Produce los NÚMEROS.
- **MCD — Modelo Canónico de Dominio** = el interior de cada cajón (QINV). **NO calcula verdad: integra las
  capas tipadas para responder la Pregunta estratégica del ADN** (Diccionario · campo 6). Un MCD jamás
  recalcula lo que el MCM ya calculó — le PIDE la verdad; las demás capas le dan contexto.

*Ejemplo vivo:* QINV-001 = **MCD de Planificación**; su sección plan-PAC ↔ publicado-SERCOP (Integridad
Contractual) es un MCD en operación — cruza Canon (montos) + datos vivos (SERCOP) sin recalcular el motor.

---

## §2 · El cajón NO es dashboard: es un MCD (deriva del ADN, no lo redefine)

El **Diccionario (13 ADN)** define QUÉ es cada cajón. `ADR-030` define CÓMO se ve. Este ADR define la
**naturaleza del interior:** un MCD que consume capas para responder la pregunta del ADN. La visualización
(Sankey · grafo · tabla · flujo) es intercambiable. **El activo es el modelo, no la gráfica ni el algoritmo.**

---

## §3 · MCIP — los 5 motores, TIPADOS (genuinamente nuevo)

El MCD se construye con motores, cada uno con rol **tipado** (no fuentes intercambiables — esto ES el
antialucinación real: cada motor responde SOLO lo suyo):

| Motor | Lee de | Responde | Naturaleza |
|---|---|---|---|
| **Matemático** | Gold Master (MCM) | los NÚMEROS — la verdad | runtime · **supremo** |
| **Grafos** | Neo4j | las RELACIONES (meta→POA→PAC→SERCOP→proveedor→pago) | runtime |
| **Causal** | econometría | ¿qué CAUSÓ este resultado? | lab → promueve hallazgo |
| **Descubrimiento** | K-Means · HDBSCAN · UMAP | PATRONES ocultos / anomalías | **laboratorio, NO runtime** |
| **Prospectivo** | simulación | ¿qué pasa SI…? (escenarios) | lab → runtime |

Los motores consultan además el **Corpus** (Supabase · texto normativo/evidencia) y la **Memoria** (Obsidian,
vía §4). **K-Means, Gephi, Jupyter = laboratorio (el microscopio), no capas del runtime** — sus hallazgos
*vuelven al MCD*; no viven en el sistema (igual que Python o el propio Excel son herramientas, no capas).

**Secuencia (asesor):** el Motor de Descubrimiento entra *cuando el grafo (o el dato canónico) ya genera la
pregunta* — no antes. Primero el grafo; de él emergen las preguntas naturales (¿barrios parecidos?→KMeans;
¿contratos anómalos?→DBSCAN; ¿comunidades?→Louvain), no al revés. Neo4j = el motor del grafo · Gephi = el
microscopio que lo explora; Gephi nunca alimenta la interfaz directamente.

---

## §4 · Obsidian se consume vía QUIRA IA, nunca directo (resuelve colisión 2)

`ARQUITECTURA_CANONICA` Anti-patrón #4: **Obsidian está DESACOPLADO del runtime** (alimenta solo a QUIRA IA,
Fase 2+). La mesa pidió que el cajón consulte Obsidian directo → contradice el canon. **Resolución:** el MCD
accede a la memoria de diseño (Obsidian) **a través de la capa QUIRA IA, jamás directo.** Preserva el
desacople y entrega la memoria al cajón por el canal correcto.

---

## §5 · Arquitectura horizontal, ENTREGA vertical (corrección de dirección)

"Construyo todas las capas y luego el cajón" es el big-bang que no despliega. `ADR-029` ya lo dijo: la
Desexcelización (capas plenas) es **futuro (VÍA SISTEMA · Sprint F), "primero el MOLDE Montecristi
mostrable"**. Se ratifica: **la Espina Dorsal QINV-001 es el tracer bullet** que obliga a cada capa a existir
"lo justo", end-to-end. Arquitectura horizontal = el mapa; entrega vertical = el vehículo. **No se detiene el envío.**

**Doctrina de construcción (asesor · refrendada):** *construir verticalmente, conectando horizontalmente.*
Se elige UN MCD (hoy: Planificación) y, mientras se construye, se dejan **conectadas todas sus capas**
(MCM · Supabase · Neo4j · Obsidian · QUIRA IA · GeoTwin · interfaz). Cuando ese dominio queda completo, se
repite el patrón con el siguiente. Así no reaparecen las **"islas tecnológicas"** —Excel por un lado, Neo4j
por otro, todo existía pero nada conversaba—, el problema que el propio equipo ya había identificado.

---

## Consecuencias

- **Cero refundación.** El canon de 6 capas, el Diccionario (13 ADN) y `ADR-026`/`029` siguen vigentes; este
  ADR los **conecta**, no los reemplaza.
- "Modelo Canónico" deja de estar sobrecargado: **MCM** (Gold Master · verdad) vs **MCD** (cajón · integración).
- El interior del cajón se construye como **MCD con capas tipadas**, no como dashboard.
- Los algoritmos (clustering) y herramientas (Gephi/Jupyter) son **laboratorio**, no runtime.
- Obsidian permanece desacoplado; el MCD lo consume vía QUIRA IA.
- **QINV-001 (Planificación) es el primer MCD de referencia**; su Integridad Contractual es la prueba viva.
- **Doctrina de build:** vertical (un MCD a la vez), conectando horizontalmente (todas sus capas) — sin islas.
- **Definición-norte (interna · firewall):** QUIRA = *Sistema Operativo de Inteligencia Territorial basado en
  un Modelo Canónico Matemático, enriquecido por conocimiento normativo, relaciones semánticas e IA, cuya
  unidad funcional es el Modelo Canónico de Dominio.* (Público: "Centro de Inteligencia Territorial".)
- **Siguiente:** registrar en `QUIRA_MASTER_INDEX.md` + completar las capas faltantes del MCD de Planificación
  (Neo4j relaciones meta→POA→PAC→SERCOP · Supabase normativa · QUIRA IA).

---
*ADR-031 · QUIRA Gov · Dylus Lab © 2026 · "No refundamos la arquitectura: ya estaba escrita. Nombramos lo nuevo, resolvemos las colisiones, y dejamos que el cajón sea un modelo —no una pantalla."*
