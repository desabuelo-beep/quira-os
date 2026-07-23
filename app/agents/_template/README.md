# DOM_TEMPLATE — cómo instanciar un dominio nuevo

> Propuesta del colega, 2026-07-23. Extraído por comparación real de
> `app/agents/d07/` vs `app/agents/d01/` (no supuesto) — ya construidos
> ambos, se identificó qué es forma (genérico) y qué es sustancia
> (específico de cada DOM).
>
> **Dogfooding real (2026-07-23, refactor retroactivo — no "mejora
> futura"):** d07 y d01 ya **importan** este template (`from .._template
> import catalogo/persistencia as _base`), no lo copian. Al corregirlo, se
> corrigen ambos dominios a la vez. Se detectaron y corrigieron 3 deudas
> reales en ese refactor: `d07/persistencia.py` no generaba
> `evaluation_id` (violaba el contrato ya documentado), `d01/` no tenía
> `persistencia.py`, y el grafo de d01 se generaba sin YAML intermedio
> (ahora: `data/d01/catalogo_d01_v1.0.0.yaml`).

## Qué es genérico (viene de aquí, casi sin cambios)
- `catalogo.py` — carga cualquier YAML, indexa por id.
- `fuentes.py` — stub de Navigator/Collector/Interpreter (Fase 4, IA).
- `persistencia.py` — `EvaluationID = Municipio+Dominio+Unidad+Periodo`, `construir_resultado`.

## Qué NO es genérico (cada DOM lo escribe desde cero)
- **`scoring.py` o `motor.py`** — el corazón determinístico. En d07 es el
  algoritmo SITA (calcula). En d01 es `motor.leer_metricas()` (solo LEE
  el Gold Master, Regla 1). **Cada DOM decide si calcula o lee** — nunca
  asumir uno u otro sin verificar si el Gold Master ya resolvió la métrica.
- **`articulacion.py` / lógica de cruce** — si el DOM tiene una Regla
  Operativa tipo BRN (RO-I-00X), aquí vive el Alignment Agent. Si no,
  se omite.
- El **catálogo de contenido** (`data/d0X/catalogo_*.yaml`) — la unidad de
  medición cambia por DOM (CD-XX en d07, eslabones de cadena en d01).

## Checklist para instanciar `app/agents/d0X/`

1. **Verificar el Gold Master primero** (`app/connectors/gold_master.py` o
   la hoja específica): ¿la métrica del DOM ya está calculada ahí? Si sí →
   `motor.py` que LEE (como d01). Si no → hay que reconstruir el estándar
   primero (como se hizo con d07, Fase 0 completa antes de tocar código).
2. Copiar `catalogo.py`, `fuentes.py`, `persistencia.py` de este template.
3. Escribir el catálogo de contenido del DOM (YAML), consultando su BRN
   (`docs/brn/CNO-*.yaml`) o su PCD-D0X si ya existe.
4. Escribir `motor.py` o `scoring.py` según el paso 1.
5. Si aplica, escribir `articulacion.py` (cruce entre fuentes).
6. Generar el grafo Neo4j (`scripts/cypher/00N_d0X_*.cypher`, mismo patrón
   de `002_d07` / `003_d01`) — marcar reuso cross-dominio con
   `MISMA_FUENTE_QUE` donde exista (ej. cédula presupuestaria).
7. Registrar el nuevo rector en `governance/QUIRA_MASTER_INDEX.md` el
   mismo día (Regla del Index — o se pierde).
8. Añadir sus agentes al `docs/architecture/META_CATALOGO_AGENTES.md`.

## Convención de propiedad clave en Neo4j (auditoría 2026-07-23)

La mayoría de labels usan `.id` (`:CD`, `:Articulo`, `:RO`, `:CNO`, `:Dominio`, `:Fuente`,
`:Componente`, `:Portal`, `:Evidencia`, `:Observacion`, `:Municipio`). **`:Norma` y `:Regla` usan
`.sigla`, no `.id`** — deliberado: son catálogos compartidos entre dominios (una norma como CE o
una regla como CTA no "pertenece" a un DOM, la referencian varios), y `sigla` es su nombre
semánticamente estable. Mantener esta distinción al migrar d02/d03/d09 — no es un olvido, es la
regla: **entidad propia de un DOM → `.id`; catálogo compartido entre DOM → su clave natural**.

## Lo que este template NO resuelve (a propósito)
No decide si el DOM necesita Portal Navigator, NLP de video, o solo lectura
del Gold Master — eso lo determina el paso 1 del checklist, DOM por DOM.
No hay atajo: cada dominio exige verificar su propio estado real antes de
programar nada (mismo principio que evitó reconstruir H09 sin evidencia).

---
*DOM_TEMPLATE · Dylus Lab © 2026*
