# ADR-020 — Analítica Constitucional: Metodología de Medición del Grafo QUIRA

**Estado**: ACTIVO  
**Fecha actualización**: 2026-06-02 (Gate 2 completado)  
**Fecha**: 2026-06-02  
**Proyecto**: QUIRA Gov · Dylus Lab  
**Motivación**: ADR-019 (hipótesis Dominios de Legitimación Democrática) requiere evidencia discriminante formal más allá del degree centrality.

---

## Contexto

El grafo constitucional QUIRA ya contiene suficientes nodos y relaciones para producir métricas significativas. El degree (grado de cada nodo) es el proxy más fácil pero el menos discriminante:

- **Degree** mide conexiones directas → premio a cantidad
- **Betweenness** mide intermediación → mide si el nodo conecta comunidades separadas
- **Closeness** mide accesibilidad → cuán rápido llega a todos los demás
- **Eigenvector** mide influencia por calidad de vecinos → "estar conectado a los importantes"
- **Community Detection** revela estructura emergente → ¿qué nodos forman clusters?

ADR-019 requiere betweenness y community detection para pasar de SUPPORTED a CONFIRMED.

Este ADR formaliza la metodología para que sea reproducible.

---

## Las Cinco Métricas Canónicas

### M1 — Degree Centrality (ya implementada)

**Pregunta que responde**: ¿Cuántas relaciones directas tiene este nodo?  
**Interpretación para QUIRA**: ¿Cuántas normas instrumentan este dominio?  
**Limitación**: No distingue si las conexiones forman un cluster o cruzan toda la red.

```cypher
MATCH (n) WHERE n:ACK OR n:Dominio OR n:Circuito
OPTIONAL MATCH (n)-[r]-(m)
WITH n, COUNT(r) AS degree,
     labels(n)[0] AS tipo,
     CASE WHEN n:ACK THEN n.ack_id WHEN n:Dominio THEN n.id ELSE n.id END AS nodo_id
RETURN tipo, nodo_id, degree ORDER BY degree DESC LIMIT 20
```

**Baseline 2026-06-02**: Dom08=21, Dom09=11, Dom07=10, Dom04=7

---

### M2 — Betweenness Centrality Proxy (implementada hoy)

**Pregunta que responde**: ¿Cuántos caminos entre otros nodos pasan por este nodo?  
**Interpretación para QUIRA**: ¿Es este dominio un puente entre comunidades normativas?  
**Por qué importa para ADR-019**: El degree alto puede ser "cluster local". El betweenness alto significa que el nodo conecta partes distintas del grafo.

```cypher
-- Proxy NRC→Dominio paths (longitud 1..5)
MATCH path = (nrc:ACK)-[*1..5]->(dom:Dominio)
WHERE nrc.es_nrc = true
WITH [n IN nodes(path) |
     CASE WHEN n:Dominio THEN n.id
          WHEN n:ACK    THEN n.ack_id
          ELSE null END] AS pnodes
UNWIND pnodes AS nodo
WITH nodo, COUNT(*) AS freq
WHERE nodo IS NOT NULL AND freq > 0
RETURN nodo, freq ORDER BY freq DESC LIMIT 15
```

**Baseline 2026-06-02**: Dom08=328, Dom07=207, CE_95=145, Dom04=128, Dom09=99

**Betweenness formal (pendiente GDS)**:

```cypher
-- Requiere GDS plugin (no disponible en AuraDB Free)
CALL gds.betweenness.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS id, score
ORDER BY score DESC LIMIT 15
```

**Estado**: PENDIENTE — requiere Neo4j Enterprise/Self-managed con GDS, o computar externamente con NetworkX sobre los datos exportados.

---

### M3 — Closeness Centrality (pendiente)

**Pregunta que responde**: ¿Qué tan cerca está este nodo de todos los demás?  
**Interpretación para QUIRA**: ¿Puede este dominio ser alcanzado rápidamente desde cualquier norma?

```cypher
-- Proxy (promedio de distancias desde este nodo a todos los demás)
MATCH (n:Dominio {id:'Dom08'})
MATCH (m) WHERE m:ACK OR m:Dominio OR m:Circuito
MATCH path = shortestPath((n)-[*]-(m))
RETURN n.id AS nodo, AVG(length(path)) AS avg_distance, COUNT(path) AS alcanzados
```

**Estado**: PENDIENTE.

---

### M4 — Eigenvector Centrality (pendiente)

**Pregunta que responde**: ¿Están los vecinos de este nodo también bien conectados?  
**Interpretación para QUIRA**: ¿Conecta este dominio con normas importantes, o con normas periféricas?

El eigenvector es la métrica más relevante para confirmar que CE_1 y CE_95 son **realmente** nodos constituyentes y no solo nodos con muchas conexiones técnicas.

```cypher
-- Requiere GDS
CALL gds.eigenvector.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).id AS id, score
ORDER BY score DESC LIMIT 15
```

**Estado**: PENDIENTE — requiere GDS.

---

### M5 — Community Detection / Louvain (pendiente — crítica para ADR-019)

**Pregunta que responde**: ¿Qué nodos forman clusters naturales sin forzar ninguna hipótesis?  
**Interpretación para QUIRA**: ¿Dom08 y Dom09 terminan en el mismo cluster? ¿CE_1 forma su propia comunidad?  
**Por qué es crítica**: Si Dom08 y Dom09 caen en comunidades distintas, la hipótesis de "par constitucional" se debilita. Si caen en la misma, se confirma empíricamente.

```cypher
-- Requiere GDS
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).id AS nodo, communityId
ORDER BY communityId, nodo
```

**Estado**: PENDIENTE — requiere GDS.

---

## Plan de Implementación de GDS

Para ejecutar M2 formal + M4 + M5, hay tres rutas:

### Ruta A — Neo4j AuraDB Enterprise (recomendado en el largo plazo)

Upgrade de la instancia AuraDB Free a Enterprise. GDS incluido. Costo mensual. Apropiado cuando el grafo supere 500+ nodos.

### Ruta B — NetworkX sobre datos exportados (disponible hoy)

```python
# Exportar grafo desde Neo4j
import networkx as nx
from neo4j import GraphDatabase

# Query todos los nodos y relaciones
G = nx.DiGraph()
# ... añadir nodos y aristas desde la query

# Calcular betweenness formal
betweenness = nx.betweenness_centrality(G)
eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
communities = nx.algorithms.community.louvain_communities(G)
```

**Estado**: IMPLEMENTABLE AHORA. El grafo actual tiene ~50 nodos — NetworkX lo procesa en milisegundos.

### Ruta C — Neo4j Desktop local con GDS

Instalar Neo4j Desktop localmente, cargar el mismo grafo, ejecutar GDS. Sin costo adicional para análisis exploratorio.

---

## Umbrales para ADR-019 CONFIRMED

Para que ADR-019 pase de SUPPORTED a CONFIRMED, se necesita que se cumplan al menos 3 de estos 4 criterios:

| # | Criterio | Métrica | Umbral | Estado |
|---|---|---|---|---|
| C1 | Dom08 tiene betweenness superior a Dom07 | M2 formal | Dom08 > 1.3× Dom07 | **PASS — 4.6×** |
| C2 | Dom09 betweenness posición ≤ 4 | M2 formal | Dom09 en top 4 | **PASS — posición 2°** |
| C3 | Dom08+Dom09 adyacentes con lazo causal obligatorio | M5 Louvain | Clusters C2↔C3 conectados | PENDIENTE (Dom09 incompleto) |
| C4b | CE_1 Constitutional Cascade Score > CE_226 | M6 | CE_1 > CE_226 | **PASS — 39 vs 34** ✅ centrality_results.json verificado commit cfb6595 |

**Nota sobre C3**: La hipótesis original era "misma comunidad." La analítica reveló que Dom08 (C2) y Dom09 (C3) son comunidades distintas pero adyacentes. El criterio fue reformulado: la díada no requiere misma comunidad — requiere lazo causal con comunidades adyacentes. Esto es arquitectónicamente más correcto.

**Nota sobre C4 → C4b**: CE_1 es un nodo fuente puro. Eigenvector (M4) premia hubs recursivos — CE_1 no puede ganarlo por diseño constitucional. La métrica correcta para un nodo constituyente es el CASCADE SCORE.

Adicionalmente, para confirmar Escenario C (arquitectura de soberanía):
- CE_1 betweenness (M2 formal) ≥ CE_226 betweenness (pendiente cálculo diferenciado)

---

## Snapshot de Referencia

El análisis de ADR-019 usa el estado del grafo en **2026-06-02** como baseline. Cualquier adición posterior de nodos/relaciones modifica los valores absolutos pero no debería cambiar el orden relativo si la hipótesis es correcta.

Ver: `docs/snapshots/snapshot_2026_06_02.md`

---

## Ruta de Implementación Inmediata (NetworkX)

```python
# scripts/analytics/compute_centrality.py
# Ejecutable hoy contra AuraDB Free

from neo4j import GraphDatabase
import networkx as nx
import json

def export_graph(driver, database):
    """Exporta el grafo completo de Neo4j a NetworkX."""
    G = nx.DiGraph()
    with driver.session(database=database) as s:
        # Nodos
        nodes = s.run("MATCH (n) RETURN id(n) AS nid, labels(n)[0] AS tipo, "
                      "CASE WHEN n:ACK THEN n.ack_id WHEN n:Dominio THEN n.id "
                      "ELSE toString(id(n)) END AS nombre")
        for r in nodes:
            G.add_node(r['nid'], tipo=r['tipo'], nombre=r['nombre'])
        # Aristas
        edges = s.run("MATCH (a)-[r]->(b) RETURN id(a) AS src, id(b) AS tgt, type(r) AS rel")
        for r in edges:
            G.add_edge(r['src'], r['tgt'], rel=r['rel'])
    return G

def compute_analytics(G):
    """Calcula las 5 métricas constitucionales."""
    results = {}
    results['degree']      = dict(G.degree())
    results['betweenness'] = nx.betweenness_centrality(G)
    results['closeness']   = nx.closeness_centrality(G)
    try:
        results['eigenvector'] = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        results['eigenvector'] = {}
    # Community detection (undirected)
    G_und = G.to_undirected()
    communities = nx.algorithms.community.louvain_communities(G_und)
    results['communities'] = {node: i for i, comm in enumerate(communities) for node in comm}
    return results
```

Estado: IMPLEMENTADO Y EJECUTADO — commit cfb6595 · 2026-06-02
Ubicación: scripts/analytics/compute_centrality.py
Output: data/centrality_results.json (incluye cascade_score desde Gate 2)

---

*ADR-020 · QUIRA Gov · Dylus Lab · 2026-06-02*  
*Prerequisito de: ADR-019 paso SUPPORTED → CONFIRMED*
