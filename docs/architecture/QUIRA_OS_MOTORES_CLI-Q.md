# QUIRA OS · Inventario de Motores + Hoja de Ruta CLI-Q (Sprint E)

**2026-06-20 · captura de mesa (Javo + colega + académico) · post-Firewall Blitz (deuda 119→0)**
**Relacionado:** ADR-028 (Compilador + CID) · ADR-027 (3 capas) · ADR-023 (3 niveles) · `scripts/dev/firewall_dictionary.json`

> **El reframe:** QUIRA dejó de ser "el Excel". El Excel es un **origen** del conocimiento, no el
> sistema. QUIRA OS = la **orquestación** de varios motores, cada uno dueño de UNA verdad.

## Los 7 motores y su frontera de verdad (ninguno se reemplaza · cada uno gobierna UNA verdad)

| Motor | Contiene | Lo alimenta | Lo consulta | Estado |
|---|---|---|---|---|
| **Gold Master** (Excel SIAP-ICPI v6.0) | causalidad **matemática** — fórmulas, pesos, ICPI/TGI/holding · H12!B33 inmutable | ingesta metodológica | Neo4j · CLI-Q | **Fuente** (analítica · intocable) |
| **Supabase** (PostgreSQL) | el **hecho observado** — SERCOP, corpus parroquial (NBI/PUGS/INEC), snapshots | pipelines ETL | Neo4j · CLI-Q | **Fuente** (facto-territorial) |
| **Neo4j** (capa QUIRA IA) | causalidad **operacional viva** — cadena Promesa→…→Territorio · las 4 congruencias | ETL (Gold Master + Supabase) | CLI-Q · export visual | **Fuente** (doctrinal · el porqué) |
| **Graphify** (AST) | **estructura del código** — dependencias, imports, 16 ADRs (NO conocimiento institucional) | análisis estático del repo | Gephi · CLI-Q | **Fuente** (estructural · el plano) |
| **Gephi** | **visualización analítica** — comunidades, centralidad, modularidad, puentes, hubs | exporta de Graphify **y** Neo4j | analistas Dylus · auditores | **Vista** (explicación) |
| **CLI-Q** (LLM en CID · Dylus) | **exposición** — traduce canon→idioma vía `firewall_dictionary.json` · jamás inventa el dato | todos los anteriores + diccionario | usuario final | **Vista** (exposición) |
| **Streamlit / GeoTwin** | **presentación** del producto — dashboards, mapa (ADR-023 Nivel 3) | CLI-Q (idioma público) | el GAD | **Vista** (producto) |

**Distinción clave (lo que la conversación había simplificado):** `Graphify` produce el grafo del **código**;
`Neo4j` guarda el grafo **causal institucional**; `Gephi` **explica** visualmente a cualquiera de los dos.
Ninguno reemplaza al otro → `código → Graphify → Gephi` · `causalidad → Neo4j → Gephi`.
*(Custodia de grafos: `graph.json`=maestro repo · `graph_fullrepo.json`=respaldo maestro · `graph_adr.json`=subgrafo ADR. El maestro NUNCA se destruye.)*

**La causalidad no se reconstruye — se ORQUESTA** (está repartida por frontera de verdad):
```
Gold Master ─→ Supabase ─→ Neo4j ─┬─→ Graphify ─→ Gephi   (estructura → se explica)
 (matemática) (evidencia) (causal) │
                                   └─→ CLI-Q / Compilador ─→ Público · Académico · Financiero …
                                        (el motor nunca cambia; cambia sólo el backend de salida)
```

## Hoja de Ruta — Sprint E: Industrialización del CID (CLI-Q Compiler)

La cacería manual de strings **terminó** (superficie pública al 100% limpia). El próximo vuelo NO abre
módulos nuevos: construye el compilador que vuelve el Blitz un comando reproducible.

- **Fase 1 — Diccionario Soberano** ✅ `scripts/dev/firewall_dictionary.json` (este commit).
  20 índices + motor + infra + node-IDs, extraídos de la tabla `PROHIBITED` (fuente única). Estructura
  multi-backend (`publico` hoy; `academico/juridico/financiero` mañana = claves paralelas).
- **Fase 2 — Bucle Determinista (CID)** ⛏️ Agente Python: `scan → leer diccionario → patch → verificar AST → git commit`.
  Memoria estructurada (`estado.json`, no conversacional) · escaneo por-archivo O(1) · Haiku + `task_budget`.
  *Prerrequisitos:* (a) `firewall_audit.py` acepta un archivo; (b) modo `--suggest` (emite el `alt`); (c) modo `--fix` (transform).
  **Vive SÓLO en Dylus Lab** — nunca en el cliente (ADR-028).
- **Fase 3 — Multi-backend de salida** ⛏️ `quira firewall --backend <publico|academico|financiero|…>`. Un motor, N idiomas.

## Pendiente antes de escalar (prioridad del colega)
**Inventario de capacidades a nivel código**, no de archivos: ¿qué consulta hoy el LLM y qué no? ¿qué es
fuente de verdad vs sólo visualización? Verificar cada motor contra su frontera declarada arriba.
*(Candidato: correr graphify sobre `app/connectors/` para mapear el cableado real entre motores.)*

---
*QUIRA OS · Inventario de Motores · Dylus Lab © 2026 · "Ya no limpiamos código; compilamos lenguajes institucionales. El motor produce la verdad; el compilador la traduce a N idiomas sin tocarla."*
