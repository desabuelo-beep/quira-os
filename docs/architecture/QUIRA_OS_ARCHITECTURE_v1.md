# QUIRA OS · Architecture v1.0 — El Mapa del Metro

**2026-06-20 · documento maestro de arquitectura (Javo + mesa) · sintetiza la evidencia verificada en silicio**
**Estado:** vivo · es el mapa único del sistema. Subordinados: `QUIRA_OS_MOTORES_CLI-Q.md` · `QUIRA_OS_INVENTARIO_CODIGO.md` · ADR-023/027/028.

> **Qué es QUIRA OS (1 párrafo).** QUIRA dejó de ser "un Excel" y dejó de ser "un dashboard". Es un
> **sistema operativo de inteligencia pública**: 7 capas que convierten una constitución matemática
> (el Gold Master) en lenguaje institucional verificable, sin que ninguna capa recalcule la verdad de otra.
> El Excel es el **origen**, no el sistema. El sistema es la **orquestación**.

## 1. Las 7 capas de soberanía (cada una gobierna UNA dimensión)

| # | Capa | Motor | Frontera de verdad (la dimensión que gobierna) | Rol |
|---|---|---|---|---|
| 1 | **Matemática** | Gold Master (Excel SIAP-ICPI v6.0) | la **causalidad** — fórmulas, pesos, ICPI/TGI/holding · H12!B33 inmutable | **Fuente** (constitución) |
| 2 | **Persistencia** | Supabase (PostgreSQL) | la **evidencia** — hechos observados del territorio (SERCOP, NBI/PUGS/INEC, snapshots) | **Fuente** (hecho) |
| 3 | **Causal** | Neo4j (QUIRA IA) | la **doctrina** — cadena Promesa→…→Territorio, 4 congruencias, circuitos C01/C-RDC/QTMP | **Fuente** (el porqué) |
| 4 | **Arquitectura** | Graphify (AST) | la **ontología del software** — qué existe, dependencias, 16 ADRs | **Fuente** (el plano) |
| 5 | **Análisis** | Gephi | la **comprensión** — centralidad, comunidades, puentes, hubs, autoridad | **Vista** (explica) |
| 6 | **Gobernanza** | Firewall + `firewall_dictionary.json` | la **frontera** — qué nomenclatura es pública vs interna (ADR-027) | filtro |
| 7 | **Lenguaje** | CLI-Q / LLM (CID · Dylus) | la **exposición** — traduce canon → idioma del cliente; jamás inventa el dato | **Vista** (idioma) |

**Graphify produce, Gephi explica, Neo4j significa.** Tres grafos, tres preguntas distintas:
`Graphify → ¿qué existe?` · `Neo4j → ¿qué significa?` · `Gephi → ¿qué es importante?` Nadie caniba­liza a nadie.

## 2. El flujo de un dato — del Excel a la pantalla (verificado con CodeGraph)

```
[1] Gold Master.xlsx ─(leído 1× · scripts/_update_snapshot.py → gold_master.py:82)─┐
                                                                                    ▼
[2] data/gm_snapshot.json  +  Supabase municipality_snapshots  ── el ESTADO SELLADO
            │                          │ (snapshot_io.py:161 · Supabase→fallback JSON)
            │                          └─→ longitudinal_engine · comparador_snapshots
            ▼
    data/loader.py::load_all  (HÍBRIDO: estructura del Excel + valores sellados de demo_data.py)
            │
       ┌────┴───────────────────────────────┐
       ▼                                     ▼
[3] 13 dashboards (quira_pages)        sentinel/tools.py ─→ [7] LLM / Sentinel
    Streamlit · GeoTwin  (VISTA)        (frontera inferencial · Regla 1)
[4..5] Graphify→Gephi corren sobre el REPО (no sobre el dato vivo): mapa+comprensión del software.
```

## 3. Taxonomía del sistema (qué es cada cosa)

| Concepto | Dónde vive | Verificación |
|---|---|---|
| **Causalidad** (matemática) | Gold Master | leído 1× por `_update_snapshot.py` |
| **Evidencia** (hecho) | Supabase `municipality_snapshots` | `snapshot_io.py:161` |
| **Causalidad** (relacional/doctrina) | Neo4j (circuitos) | `neo4j_qtmp` · `neo4j_crdc` |
| **Ontología** (estructura del código) | Graphify `graph.json` (1972 nodos) | maestro íntegro |
| **Comprensión** (importancia) | Gephi | exporta de Graphify+Neo4j |
| **Lenguaje** (exposición) | CLI-Q + `firewall_dictionary.json` | ADR-028 |
| **Vista** (presentación) | `quira_pages/*` (consumen `load_all`) | 13 dashboards · no calculan (ADR-023 N3) |
| **Estado sellado** | `gm_snapshot.json` / `demo_data.py` | fuente de facto de la UI Q1-2026 |

## 4. La frontera inferencial — la garantía Regla 1, cableada

**El LLM (Sentinel) consume EXCLUSIVAMENTE `load_all()` + `demo_data.py`** (`sentinel/tools.py:8`).
Nunca toca el Excel, Supabase ni Neo4j directamente. Razona **sobre** la verdad sellada; no la recalcula.
→ La frontera que la mesa imaginó **ya existe en el código** — y es lo que vuelve el futuro CID seguro.

## 4.5 Las 3 capas de EXPERIENCIA (la UI que navega el usuario · 2026-06-21)

Sobre el stack técnico, el usuario navega **3 capas de experiencia** (no son las 7 de soberanía):

- **L1 · Centro de Mando** — las **13 investigaciones (QINV-001…013)**: entrada (grilla · el ícono alusivo = acceso, sin numeración) + el expediente de cada una (molde **UMI** · `umi.py` · regla **20/70/10**: pregunta forense · evidencia protagonista · lectura).
- **L2 · GeoTwin** — la **convergencia territorial**: todas las brechas de las 13 aterrizan en el mapa.
- **L3 · QUIRA IA** — la **inteligencia que CONSOLIDA**: lee las 13 + GeoTwin, copiloto omnipresente, ápice de la inteligencia territorial. **Es una CAPA, no el 10%** de un expediente — el 20/70/10 es el layout *local*; la IA como capa es full-power (capa Causal/Neo4j + Gephi externo). *(Javo · 2026-06-21: no relegar la IA.)*

**Polimorfismo QINV (dual-lente):** cada investigación sirve **dos sujetos obligados** con el mismo método — **Lente GAD** (territorial · PDOT · eSIGEF local) y **Lente Central** (sectorial · PEI · Plan Nacional · LOSEP/Contraloría). QUIRA deja de ser solo-cantón → **sistema del Estado**; el lente se adapta, la pregunta forense es la misma. *(Enriquece el `DICCIONARIO_CONCEPTUAL` —el rector— con la columna Lente Central; se integra al construir cada QINV.)*

## 5. Las 3 capas de soberanía de lenguaje (ADR-027) mapeadas sobre el stack

- **Dylus Lab** (capas 1-6 internas + consolas) → canon legítimo (ICPI/TGI/SAT/H##). NO se purga.
- **QUIRA IA** (Neo4j, router, motor causal) → infraestructura invisible. NO se purga.
- **Familia QUIRA** (la VISTA, capa 3) → firewall obligatorio. Deuda **0** (Sprint D.2A).
El **Compilador CLI-Q** (capa 7) es el puente: traduce 1→6 (canon) a la salida pública de la Familia.

## 6. Custodia de grafos (nunca destruir el maestro)
`graph.json` = **maestro** del repo (1972 nodos · 3290 aristas · activo para queries) · `graph_fullrepo.json` = respaldo maestro · `graph_adr.json` = subgrafo temático (47). Los subgrafos son **vistas**, jamás sustituyen al maestro.

## 7. Estado y próximo paso
- ✅ Firewall Familia 119→0 · escáner calibrado · ADR-027/028 · inventario en silicio · este mapa.
- ⛏️ **Cabos sueltos** (capa de datos, no bloquean el compilador): 3 loaders GM coexisten · `sentinel/db_config`→`utils/db_config` (v7.0) · `demo_data` = fuente de facto (snapshot manual).
- ▶ **Siguiente:** con el mapa dibujado, construir el **Compilador CLI-Q / CID** (ADR-028 Fase 2) sobre roca firme.

---
*QUIRA OS Architecture v1.0 · Dylus Lab © 2026 · "7 capas, un organismo. El Excel es el origen; la orquestación es el sistema. Cada motor gobierna una verdad y ninguno recalcula la del otro."*
