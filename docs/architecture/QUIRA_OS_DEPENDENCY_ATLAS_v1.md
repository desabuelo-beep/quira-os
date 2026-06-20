# QUIRA System Dependency Atlas v1.0 — La Carta de Navegación

**2026-06-21 · Sprint E · contratos VERIFICADOS contra el código (CodeGraph + barrido de escrituras)**
**No es:** un ADR · un mapa conceptual · un UML. **Es:** el grafo de dependencias OPERACIONALES + contratos + invariantes.
**Hermano mayor del:** `QUIRA_OS_ARCHITECTURE_v1.md` (el qué) · este Atlas responde **¿qué depende de qué, y quién puede tocar qué?**

> **Para qué sirve.** Tras este documento, cualquier desarrollador, investigador o institución puede
> incorporarse a QUIRA sin depender de quienes lo iniciaron. Convierte un proyecto complejo en un
> **sistema gobernable**. Es la condición para escalar 10 años.

## Capa 0 — Ingeniería de sistemas (este Atlas)
Las dependencias no son causales (eso es Neo4j) ni de código (eso es Graphify): son **operacionales**.
Quién corre antes que quién, quién escribe lo que otro lee, qué nunca debe cruzarse.

## 1. Las 8 capas de construcción (madurez real, hoy)

| Capa | Qué vive aquí | Madurez |
|---|---|---|
| **0 · Sistemas** | este Atlas · BOOT · CodeGraph | 🟢 naciendo (hoy) |
| **1 · Conocimiento** | Gold Master · PDOT · ICPI/SAT · ADRs · ontología · Constitución metodológica | 🟢 terminada |
| **2 · Causalidad** | Neo4j · circuitos C01/C-RDC/QTMP · DCO · 4 congruencias | 🟢 madura |
| **3 · Evidencia** | Supabase · snapshots · auditoría | 🟢 existe |
| **4 · Arquitectura** | ADR-027/028 · mapa maestro · inventario · Graphify · CodeGraph | 🟢 sólida |
| **5 · Observabilidad** | Gephi (el microscopio: centralidad/comunidades/puentes) | 🟡 disponible, infrautilizada |
| **6 · Lenguaje** | CLI-Q · Firewall · Diccionario Soberano · Compilador · CID | 🟠 recién empieza |
| **7 · Operación autónoma** | Sentinel · agentes · loops · autocorrección · memoria · CID completo | 🔴 no empieza (y está bien) |

## 2. Contratos por motor — quién LEE · quién ESCRIBE · quién NUNCA (verificado)

| Motor | Lo ESCRIBE | Lo LEE | NUNCA |
|---|---|---|---|
| **Gold Master.xlsx** | solo scripts de gobernanza (`sync_protocol`·`update_gold_master_rc1`·`gold_master_governance`) | solo `scripts/_update_snapshot.py` → sello | ❌ la UI/LLM jamás lo tocan |
| **Snapshot** (`gm_snapshot.json` + Supabase `municipality_snapshots`) | `_update_snapshot` · `snapshot_pipeline` · `p_carga` (consola Dylus) | `snapshot_io` · `gm_loader` · `longitudinal_engine` | ❌ el LLM no lo escribe |
| **`load_all()`** | nadie (es agregador puro) | 13 dashboards + `sentinel/tools.py` | ❌ no calcula, no persiste |
| **Neo4j** | solo cypher loaders (`scripts/cypher`·`normativa`) | conectores `neo4j_crdc`/`qtmp` → 4 páginas (fallback si offline) | ❌ jamás interpreta lenguaje |
| **Supabase (estado Sentinel)** | `db_ops`·`sla_db`·`learning_engine`·`governance_engine` (su PROPIO estado: alertas/SLA/memoria) | Sentinel | ❌ jamás escribe el Gold Master ni el sello |
| **Graphify `graph.json`** | solo Graphify (AST del repo) | Gephi · humanos · CodeGraph | ❌ jamás interpreta causalidad |
| **Gephi** | nada (solo visualiza) | analistas Dylus | ❌ jamás modifica grafos |
| **LLM / CLI-Q** | nada en datos (produce texto/parches de UI) | solo `load_all` (datos) · `firewall_dictionary.json` (lenguaje) | ❌ jamás Excel/Supabase/Neo4j directo |

## 3. Dependencias por componente (entradas → salidas · propietario · frecuencia)

| Componente | Entradas | Salidas | Propietario | Frecuencia |
|---|---|---|---|---|
| `_update_snapshot.py` | Gold Master.xlsx | `gm_snapshot.json` | Dylus | manual (por corte) |
| `data/loader.py::load_all` | Excel (estructura) + `demo_data.py` | dict de estado | Dylus | en cada request UI |
| `snapshot_io.py` | Supabase / JSON fallback | snapshot dict | Dylus | por sesión |
| conectores Neo4j | Neo4j (Cypher MATCH) | dict de circuito | QUIRA IA | en vivo (con caché/fallback) |
| Graphify | repo (`.py`/`.md`) | `graph.json` (1972 nodos) | Dylus | al cierre / on-demand |
| `sentinel/tools.py` | `load_all` | getters tipados al LLM | Dylus | por consulta |
| CLI-Q (futuro) | `firewall_dictionary.json` + fuente UI | parches de lenguaje | Dylus | bajo demanda (`quira firewall`) |

## 4. Invariantes — las reglas que NUNCA se rompen (verificadas)

1. **El Gold Master jamás lo lee/escribe la UI ni el LLM.** Solo scripts de gobernanza (escritura) y `_update_snapshot` (lectura→sello). *(verificado: 1 lector app, escritores solo en `scripts/`)*
2. **El LLM jamás consulta directamente Excel/Supabase/Neo4j.** Solo `load_all`. *(verificado: `sentinel/tools.py:8`)*
3. **Toda traducción institucional pasa por el Diccionario Soberano** (`firewall_dictionary.json` · ADR-028).
4. **La vista jamás calcula.** Los dashboards consumen `load_all`, no recalculan (ADR-023 Nivel 3).
5. **El grafo maestro (`graph.json`, 1972 nodos) jamás se destruye.** Los subgrafos son vistas.
6. **Graphify produce, Gephi explica, Neo4j significa.** Ningún grafo modifica a otro.
7. **Toda modificación visible debe rastrearse a evidencia verificable** (SHA-256 / norma · Regla 3).
8. **El Excel = Estado.** Excel→Python→Supabase→UI, nunca al revés (Regla 1).

## 5. Cómo usar este Atlas
- **Onboarding:** lee Capa 1 (qué hay) → §2 contratos (qué puedes tocar) → §4 invariantes (qué nunca).
- **Antes de construir** cualquier motor nuevo: ubícalo en una capa, declara sus contratos, no rompas invariantes.
- **El CID (capa 6→7)** se construye respetando §2: opera sobre fuente de UI + diccionario, jamás sobre el espinazo de datos.

---
*QUIRA System Dependency Atlas v1.0 · Dylus Lab © 2026 · "Un sistema es gobernable cuando cualquiera puede leer qué depende de qué y qué nunca debe cruzarse. Eso es lo que separa un proyecto de una plataforma."*
