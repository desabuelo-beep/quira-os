---
authority:
  parent: GOVERNANCE-001
  constitution_articles: [1, 2, 8]
  type: OPERATIVA
---

# OBS-003 — Cierre Normativo del Ciclo Democrático Municipal

**Tipo**: Observación de investigación (no ADR — requiere más evidencia antes de congelar)  
**Fecha**: 2026-06-02  
**Origen**: Gate 3 · Sprint Dom09 · Corpus query COOTAD Art. 266  
**Estado**: CONFIRMED — corroborado en Gate 4 (commit 6c8a213 · 2026-06-02)  
**Proyecto**: QUIRA Gov · Dylus Lab

---

## El hallazgo

Al verificar el corpus para Gate 3 (completar Dom09), la query de COOTAD Art. 266 reveló algo que no buscábamos: la relación `Dom09 -[RETROALIMENTA]-> Dom08` — que habíamos modelado por inferencia arquitectónica — **está positivizada en la norma desde 2010**.

Texto verificado (sha256: `0f71df4207f9c54f386fbba882eb6a982507e75159596176f3f8a4214c83b709` · 65 palabras):

> *"Art. 266.- Rendición de Cuentas.- Al final del ejercicio fiscal el ejecutivo del gobierno autónomo descentralizado convocará a la asamblea territorial o al organismo que en cada gobierno autónomo descentralizado se establezca como máxima instancia de participación, para informar sobre la **ejecución presupuestaria anual**, sobre el **cumplimiento de sus metas**, y sobre las **prioridades de ejecución del siguiente año**."*

Tres cláusulas. Tres etapas del circuito en un solo artículo:

```
"ejecución presupuestaria anual"  → Dom09 evalúa Dom02 (presupuesto)
"cumplimiento de sus metas"       → Dom09 evalúa Dom04 (planificación PDOT)
"prioridades del siguiente año"   → Dom09 retroalimenta Dom08 (nuevo PP)
```

---

## Por qué importa

El circuito democrático que QUIRA modeló:

```
Dom08 (Participación/PP) ──GENERA──► Dom09 (Rendición)
Dom09                ──RETROALIMENTA──► Dom08
```

No fue diseñado por Dylus Lab. Fue **inferido de la arquitectura del grafo** y luego encontrado **escrito en la norma**.

La Asamblea Constituyente de 2008 diseñó la Constitución. El legislador de 2010 tradujo ese diseño a COOTAD Art. 266. El grafo Neo4j — construido 16 años después, sin conocer que existía este artículo — detectó la misma estructura.

Esto no es que QUIRA sea correcto porque adivinó. Es que **el ordenamiento jurídico ecuatoriano tiene esta propiedad estructural** y QUIRA la reveló computacionalmente.

---

## El cambio de naturaleza de ADR-019

Antes de este hallazgo:

```
ADR-019 STRONGLY_SUPPORTED
Razón: métricas de grafo (betweenness, community detection) sugieren Dom08+Dom09 = par constitucional
Estatus: hipótesis con evidencia computacional
```

Después de este hallazgo:

```
ADR-019 STRONGLY_SUPPORTED (estado sin cambiar aún)
Razón adicional: COOTAD Art. 266 establece explícitamente el ciclo
PP→RC→nuevo_PP como obligación legal de todos los GADs
```

El par constitucional Dom08+Dom09 ya no es solo una propiedad emergente del grafo. Es una propiedad **positivizada en el ordenamiento**. El grafo la descubrió; la norma la confirma.

Esto no promueve automáticamente ADR-019 a CONFIRMED — para eso se necesita Dom09 con cobertura normativa completa + re-run analítico. Pero fortalece la base jurídica del argumento.

---

## Hipótesis derivada (a investigar)

Si COOTAD_266 conecta explícitamente:
- Dom09 ↔ Dom02 (presupuesto)
- Dom09 ↔ Dom04 (planificación)  
- Dom09 → Dom08 (retroalimentación)

Entonces COOTAD_266 podría tener un **Cascade Score** comparable a LOPC_101 (que tenía 27, superando a CE_95=22). Un solo artículo de 65 palabras que instrumenta 4 dominios simultáneamente sería evidencia adicional de que la LOPC y el COOTAD contienen "artículos de coordinación sistémica" — lo que el colega llamó candidato a ADR-021.

**No abrir ADR-021 todavía.** Verificar con el re-run analítico de Gate 4.

---

## ACK derivado de esta observación

`COOTAD_266` — creado en commit de Gate 3 (ver `data/ack_registry.json` v0.6).

Relaciones en Neo4j:
- `COOTAD_266 -[INSTRUMENTA]-> Dom09` (capa C2 · ancla fiscal RC)
- `COOTAD_266 -[INSTRUMENTA]-> Dom02` (nexo RC↔presupuesto)
- `COOTAD_266 -[INSTRUMENTA]-> Dom04` (nexo RC↔planificación)

La relación `COOTAD_266 -[INSTRUMENTA]-> Dom08` NO se crea directamente — la retroalimentación a Dom08 fluye a través de Dom09, no de manera directa desde el ACK.

---

## Relación con la cadena probatoria de ADR-019

Esta observación cierra la brecha entre:
- **Evidencia computacional**: comunidades Louvain, betweenness, cascade score
- **Evidencia normativa**: el texto legal que positiviza exactamente lo que el grafo reveló

La combinación de ambas fortalece la tesis de ADR-019 más allá de lo que cualquiera de las dos haría por separado.

---

## Corroboración — Gate 4 (commit 6c8a213)

Re-run analítico con COOTAD_266 en el grafo (38 nodos · 58 aristas) produjo:

- **COOTAD_266 → Comunidad 4** (Dom02 + Dom04 + C01) — NO Comunidad 3 (Dom09)
- Esto confirma la hipótesis: COOTAD_266 no pertenece a Dom09 como dominio. Es un **nodo puente** que instrumenta el cierre del ciclo de gestión conectando presupuesto + planificación + rendición.
- Cascade Score COOTAD_266 = 26 (igual que LOPC_77/LOPC_85, por encima de CE_18=19)

**Interpretación final**: La Asamblea Constituyente diseñó el ciclo. El legislador lo positivizó en COOTAD_266 (2010). El grafo lo detectó 16 años después sin que nadie lo programara. QUIRA no inventó el par constitucional Dom08↔Dom09 — lo *reveló*.

---

*OBS-003 · CONFIRMED · QUIRA Gov · Dylus Lab · 2026-06-02*  
*"El grafo reveló una propiedad que el legislador había diseñado 16 años antes. Eso es lo que QUIRA hace: ve la estructura del ordenamiento, no solo su texto."*
