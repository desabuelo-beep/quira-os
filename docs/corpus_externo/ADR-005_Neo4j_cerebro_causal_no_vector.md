# ADR-005 — Neo4j como cerebro causal (grafo, no vector store)

**Estado**: Aceptado  
**Fecha**: 2026-05-31  
**Decisores**: Dylus Lab · QUIRA Operaciones  

## Contexto

QUIRA necesita razonar sobre relaciones causales: ¿por qué un indicador está rojo? ¿qué nodo de la cadena C1-C9 está fallando? ¿cómo se propaga una intervención?

Las opciones consideradas:
1. **pgvector / Supabase**: búsqueda semántica vectorial — bueno para recuperación, malo para razonamiento causal
2. **Neo4j**: grafo de propiedades — nativo para relaciones, cadenas causales, trazabilidad de hipótesis
3. **Combinación**: Neo4j como razonamiento + pgvector como memoria de acceso rápido

## Decisión

**Neo4j es el cerebro causal. pgvector/Supabase es la memoria de acceso rápido.**

```
Neo4j:
  - Nodos: Norma → Competencia → Servicio → Proceso → Evidencia
            → Control → Observabilidad → Indicador → Resultado
  - Edges: [:HABILITA], [:EXPLICA], [:FUNDA], [:DEPENDE_DE]
  - Hipótesis H1-H8 como relaciones tipadas entre C9 nodes
  - PRIMERA CONSULTA BAUTISMAL (Alpha 1.0):
    ¿Por qué brechas Dom12 si COOTAD_249 cumplido?

pgvector / Supabase:
  - Embeddings de documentos para búsqueda semántica rápida
  - Métricas H73 con cadena de provenance
  - Snapshot longitudinal (eje temporal)
```

El vector no es el cerebro. El grafo es donde vive el razonamiento.

## Consecuencias

- Los 3 QTMPs están en estado `listo_neo4j` — esto define Alpha 1.0
- Los ACK del QLEP se cargan como nodos `:Atom` en Neo4j
- Un C9 confirmado activa inferencia causal en el grafo (no en el vector)
- La UI de QUIRA consulta Neo4j para explicar — Supabase para buscar

## Alternativa rechazada

RAG clásico (vector store + LLM): no puede razonar causalmente sobre normativa. Puede recuperar texto similar pero no trazarlo a través de una cadena institucional.

## Fundamento teórico

Critical Realism (Bhaskar): los mecanismos generativos (C1-C4) producen eventos (C5-C8) → experimentos (C9). El grafo modela mecanismos, no solo eventos. Ver QUIRA_CAUSAL_MODEL_v1.0.md Sec. XI.
