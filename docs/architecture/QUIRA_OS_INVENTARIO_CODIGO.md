# QUIRA OS · Inventario Técnico a Nivel Código (verificado con CodeGraph)

**2026-06-20 · Sprint E · barrido read-only sobre el índice CodeGraph (212 archivos · 3959 nodos · 7048 aristas)**
**Relacionado:** `QUIRA_OS_MOTORES_CLI-Q.md` (mapa conceptual) · ADR-023 (3 niveles) · ADR-027/028
**Método:** `codegraph_context/callers/callees/explore` — evidencia citada como `archivo:línea`. No es conceptual: es el cableado real.

> **Veredicto:** el mapa conceptual de 7 motores **se sostiene**, con 3 cabos sueltos que el CID debe respetar (abajo).

## 1. El flujo de un dato, del Excel a la pantalla (verificado)

```
Gold Master.xlsx (SIAP-ICPI · propiedad Dylus)
   │  LEÍDO EN 1 SOLO PUNTO: scripts/_update_snapshot.py::main  → fetch_gold_master_data (gold_master.py:82)
   ▼
data/gm_snapshot.json  +  Supabase municipality_snapshots   (el "estado sellado")
   │                              │
   │                              └─→ utils/snapshot_io.py::load_snapshot:161  (Supabase → fallback JSON)
   │                                       └─→ app/services/longitudinal_engine, comparador_snapshots
   ▼
data/loader.py::load_all:101   (HÍBRIDO: estructura del Excel vía _load_excel_sheet:38 + valores sellados de demo_data.py)
   │
   ├─→ 13 dashboards (quira_pages: p3·p8·p9·p12·p13·p14·p16…)        → VISTA
   └─→ sentinel/tools.py (get_indicator·get_sat_alerts·get_budget_gap·get_all_context) → el LLM
                                                                       (frontera inferencial)
sentinel/gm_loader.py::load:28  (lee gm_snapshot.json) → componentes Sentinel/charts → VISTA
```

## 2. Fuente vs Vista — clasificación atómica (lo que pidió el colega)

| Pieza | Rol | Evidencia |
|---|---|---|
| `Gold Master.xlsx` | **FUENTE** (causalidad matemática · intocable) | leído solo por `scripts/_update_snapshot.py` |
| `app/connectors/gold_master.py` | **lector de fuente** (Excel→dict H73) | `fetch_gold_master_data:82` · **1 caller** |
| `data/gm_snapshot.json` | **estado sellado** (output verificado) | `gm_loader.py:24` · "se actualiza manualmente desde el Excel" |
| Supabase `municipality_snapshots` | **FUENTE viva** (snapshots multi-municipio) | `snapshot_io.py:161` (is_active=TRUE) |
| `data/demo_data.py` | **valores sellados Q1-2026** (de facto fuente de los dashboards) | usado por `load_all` + `get_budget_gap:92` |
| Neo4j (`neo4j_qtmp`·`neo4j_crdc`) | **FUENTE causal** (circuitos C01/C-RDC/QTMP) | consumido por p07·p10_territorio·p17_rdc·p19 (con fallback si offline) |
| `data/loader.py::load_all` | **agregador** (estructura+valores → 1 dict) | 20 callers |
| `quira_pages/*` | **VISTA** (dashboards) | consumen `load_all`, no calculan (ADR-023 N3) |
| `sentinel/tools.py` | **adaptador LLM** (getters tipados) | "Fuente única: data.loader → demo_data" |

## 3. La frontera inferencial — qué consume el LLM (y qué NO)

**El LLM (Sentinel) consume EXCLUSIVAMENTE `load_all()` + `demo_data.py`** (`sentinel/tools.py` línea 8 + 92).
**Nunca** toca el Excel, Supabase ni Neo4j directamente. Sus 5 herramientas (`get_indicator/get_parroquia/
get_sat_alerts/get_budget_gap/get_all_context`) son getters de solo-lectura sobre el dict sellado.
→ **Garantía Regla 1 verificada en código:** el LLM razona SOBRE la verdad, no la recalcula.

## 4. Cabos sueltos / duplicaciones (de-risk antes del CID)

1. **Tres rutas de carga del Gold Master coexisten:** `gold_master.py` (Excel directo · solo el script de snapshot),
   `loader.py::load_all` (demo_data + estructura · los dashboards) y `gm_loader.py::load` (gm_snapshot.json · Sentinel/charts).
   Sirven a consumidores distintos pero **deben permanecer consistentes** — si el snapshot y `demo_data` divergen, dashboards y Sentinel mostrarían números distintos. ⚠ El CID/orquestador debe tratar a `_update_snapshot.py` como la **única escritura** de verdad.
2. **`sentinel/db_config.py` está marcado deprecado** (`QUIRA-DEPR — migrar a utils/db_config en v7.0`, `snapshot_io.py:183`).
   La config de conexión (Supabase vs sqlite) vive hoy en `sentinel/` pero pertenece a `utils/`. Deuda conocida.
3. **`demo_data.py` es la fuente de facto de los valores de la UI** (Q1-2026 sellado). Es correcto para el corte
   actual, pero el camino "Excel vivo → Supabase → UI" todavía pasa por el snapshot manual, no automático.

## 5. Lo que cada motor consume/produce (verificado)

- **Gold Master** → lo lee `_update_snapshot.py` (1×) · produce `gm_snapshot.json`.
- **Supabase** → escrito por `snapshot_pipeline`/`p_carga`; leído por `snapshot_io`, `longitudinal_engine`, Sentinel.
- **Neo4j** → escrito por `scripts/*` (cypher loaders); leído por 4 páginas de circuito + `compute_centrality`.
- **Graphify** → produce `graphify-out/graph.json` (maestro 1972 nodos) del repo; consumido por Gephi + humanos.
- **LLM** → consume `load_all` (vía `sentinel/tools.py`); produce explicaciones (jamás dato nuevo).

---
*Inventario verificado · Dylus Lab © 2026 · "El Excel se lee una vez y se sella; todo lo demás lee el sello. El LLM explica el sello, nunca lo reescribe."*
