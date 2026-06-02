#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_centrality.py — Analítica Constitucional QUIRA (ADR-020)
QUIRA Gov · Dylus Lab · 2026-06-02

Calcula las 5 métricas canónicas del grafo constitucional usando NetworkX:
  M1 Degree centrality        (ya en Neo4j, aquí como referencia)
  M2 Betweenness centrality   (proxy formal — no requiere GDS)
  M3 Closeness centrality
  M4 Eigenvector centrality
  M5 Community detection (Louvain)

Propósito: Generar la evidencia discriminante para ADR-019 CONFIRMED.

USO:
  python scripts/analytics/compute_centrality.py           # todas las métricas
  python scripts/analytics/compute_centrality.py --metric betweenness
  python scripts/analytics/compute_centrality.py --top 10
  python scripts/analytics/compute_centrality.py --save    # guarda JSON

Bloomberg Model:
  Script INTERNO — Dylus Lab / QUIRA Operaciones.
"""
from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.parent


# ══════════════════════════════════════════════════════════════════════════════
# EXPORTACIÓN NEO4J → NETWORKX
# ══════════════════════════════════════════════════════════════════════════════

def _get_neo4j_config() -> dict:
    try:
        import toml
        secrets_path = ROOT / ".streamlit" / "secrets.toml"
        secrets = toml.load(str(secrets_path))
        cfg = secrets.get("neo4j", {})
        return cfg if cfg.get("password") else {}
    except Exception:
        return {}


def export_to_networkx(driver):
    """Exporta el grafo Neo4j a NetworkX DiGraph."""
    try:
        import networkx as nx
    except ImportError:
        print("[ERROR] pip install networkx")
        sys.exit(1)

    cfg = _get_neo4j_config()
    G = nx.DiGraph()
    id_to_name = {}

    with driver.session(database=cfg.get("database", "neo4j")) as s:
        # Nodos
        nodes = s.run("""
            MATCH (n) WHERE n:ACK OR n:Dominio OR n:Circuito
            RETURN id(n) AS nid,
                   labels(n)[0] AS tipo,
                   CASE WHEN n:ACK     THEN n.ack_id
                        WHEN n:Dominio THEN n.id
                        ELSE n.id END AS nombre,
                   CASE WHEN n:ACK THEN n.es_nrc ELSE false END AS es_nrc,
                   CASE WHEN n:ACK THEN n.norma_sigla ELSE null END AS norma
        """)
        for r in nodes:
            nid, nombre, tipo = r['nid'], r['nombre'], r['tipo']
            id_to_name[nid] = nombre
            G.add_node(nid, nombre=nombre, tipo=tipo,
                       es_nrc=r['es_nrc'], norma=r['norma'])

        # Aristas
        edges = s.run("""
            MATCH (a)-[r]->(b)
            WHERE (a:ACK OR a:Dominio OR a:Circuito)
              AND (b:ACK OR b:Dominio OR b:Circuito)
            RETURN id(a) AS src, id(b) AS tgt, type(r) AS rel
        """)
        for r in edges:
            G.add_edge(r['src'], r['tgt'], rel=r['rel'])

    print(f"  Grafo exportado: {G.number_of_nodes()} nodos · {G.number_of_edges()} aristas")
    return G, id_to_name


# ══════════════════════════════════════════════════════════════════════════════
# LAS 5 MÉTRICAS CANÓNICAS (ADR-020)
# ══════════════════════════════════════════════════════════════════════════════

def compute_all(G, id_to_name, top_n=15):
    """Calcula y presenta las 5 métricas constitucionales."""
    import networkx as nx
    import networkx.algorithms.community as nx_comm

    results = {}

    # ── M1: Degree ────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  M1 — DEGREE CENTRALITY")
    print(f"{'='*60}")
    degree = dict(G.degree())
    degree_named = {id_to_name.get(nid, str(nid)): d for nid, d in degree.items()}
    results['degree'] = degree_named
    _print_ranking(degree_named, top_n)

    # ── M2: Betweenness ───────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  M2 — BETWEENNESS CENTRALITY (formal)")
    print(f"{'='*60}")
    betweenness = nx.betweenness_centrality(G, normalized=True)
    betweenness_named = {id_to_name.get(nid, str(nid)): b for nid, b in betweenness.items()}
    results['betweenness'] = betweenness_named
    _print_ranking(betweenness_named, top_n)

    # ── M3: Closeness ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  M3 — CLOSENESS CENTRALITY")
    print(f"{'='*60}")
    closeness = nx.closeness_centrality(G)
    closeness_named = {id_to_name.get(nid, str(nid)): c for nid, c in closeness.items()}
    results['closeness'] = closeness_named
    _print_ranking(closeness_named, top_n)

    # ── M4: Eigenvector ───────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  M4 — EIGENVECTOR CENTRALITY")
    print(f"{'='*60}")
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
        eigenvector_named = {id_to_name.get(nid, str(nid)): e for nid, e in eigenvector.items()}
        results['eigenvector'] = eigenvector_named
        _print_ranking(eigenvector_named, top_n)
    except nx.PowerIterationFailedConvergence:
        print("  [WARN] No convergió — grafo puede tener estructura DAG sin ciclos")
        results['eigenvector'] = {}

    # ── M5: Community Detection (Louvain) ─────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  M5 — COMMUNITY DETECTION (Louvain)")
    print(f"{'='*60}")
    G_und = G.to_undirected()
    try:
        communities = nx_comm.louvain_communities(G_und, seed=42)
        community_map = {nid: i for i, comm in enumerate(communities) for nid in comm}
        community_named = {id_to_name.get(nid, str(nid)): cid for nid, cid in community_map.items()}
        results['communities'] = community_named

        # Agrupar por comunidad
        by_community: dict[int, list[str]] = {}
        for nombre, cid in community_named.items():
            by_community.setdefault(cid, []).append(nombre)

        for cid, members in sorted(by_community.items()):
            print(f"\n  Comunidad {cid}:")
            for m in sorted(members):
                print(f"    {m}")

        # Check ADR-019: ¿Dom08 y Dom09 en mismo cluster?
        dom08_comm = community_named.get('Dom08')
        dom09_comm = community_named.get('Dom09')
        print(f"\n  ADR-019 C3 — Dom08 comunidad={dom08_comm}, Dom09 comunidad={dom09_comm}")
        if dom08_comm is not None and dom08_comm == dom09_comm:
            print(f"  [CONFIRMED] Dom08 y Dom09 en misma comunidad → Díada constitucional empírica")
        else:
            print(f"  [PENDIENTE] Dom08 y Dom09 en comunidades distintas → Díada no confirmada por community detection")

    except Exception as exc:
        print(f"  [ERROR] {exc}")
        results['communities'] = {}

    return results


def _print_ranking(data: dict, top_n: int):
    """Imprime ranking ordenado de una métrica."""
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    max_val = sorted_items[0][1] if sorted_items else 1
    for nodo, val in sorted_items:
        bar_len = int(val * 40 / max_val) if max_val > 0 else 0
        bar = '█' * bar_len
        print(f"  {nodo:18} {val:.4f}  {bar}")


# ══════════════════════════════════════════════════════════════════════════════
# ADR-019 VERDICT
# ══════════════════════════════════════════════════════════════════════════════

def evaluate_adr019(results: dict):
    """Evalúa los 4 criterios de ADR-019 CONFIRMED."""
    print(f"\n{'='*60}")
    print(f"  VEREDICTO ADR-019 — Dominios de Legitimación Democrática")
    print(f"{'='*60}")

    betweenness = results.get('betweenness', {})
    communities = results.get('communities', {})
    eigenvector = results.get('eigenvector', {})

    b_dom08 = betweenness.get('Dom08', 0)
    b_dom09 = betweenness.get('Dom09', 0)
    b_dom07 = betweenness.get('Dom07', 0)
    dom08_comm = communities.get('Dom08')
    dom09_comm = communities.get('Dom09')
    e_ce1  = eigenvector.get('CE_1', 0)
    e_ce226 = eigenvector.get('CE_226', 0)

    criteria = {
        'C1': ('Dom08 betweenness > 1.3× Dom07', b_dom08 > 1.3 * b_dom07 if b_dom07 > 0 else None),
        'C2': ('Dom09 en top 4 betweenness', None),  # calculado abajo
        'C3': ('Dom08 y Dom09 en misma comunidad', dom08_comm == dom09_comm if dom08_comm is not None else None),
        'C4': ('CE_1 eigenvector ≥ CE_226', e_ce1 >= e_ce226 if e_ce1 > 0 else None),
    }

    # C2: verificar si Dom09 está en top 4
    top4 = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:4]
    top4_names = [x[0] for x in top4]
    criteria['C2'] = ('Dom09 en top 4 betweenness', 'Dom09' in top4_names)

    confirmed = 0
    for cid, (desc, result) in criteria.items():
        if result is True:
            status = '[PASS]'
            confirmed += 1
        elif result is False:
            status = '[FAIL]'
        else:
            status = '[N/A] '
        print(f"  {cid} {status} {desc}")

    print()
    if confirmed >= 3:
        print(f"  RESULTADO: ADR-019 → CONFIRMED ({confirmed}/4 criterios)")
        print(f"  La hipótesis 'Dominios de Legitimación Democrática' tiene soporte empírico formal.")
    elif confirmed >= 2:
        print(f"  RESULTADO: ADR-019 → SUPPORTED ({confirmed}/4 criterios)")
        print(f"  Evidencia positiva pero insuficiente para confirmación formal.")
    else:
        print(f"  RESULTADO: ADR-019 → INCONCLUSO ({confirmed}/4 criterios)")
        print(f"  Agregar más datos normativos antes de re-evaluar.")

    print(f"{'='*60}\n")


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Analítica Constitucional QUIRA — ADR-020")
    parser.add_argument("--metric", choices=["degree","betweenness","closeness","eigenvector","community","all"],
                        default="all", help="Métrica a calcular")
    parser.add_argument("--top", type=int, default=15, help="Top N nodos a mostrar")
    parser.add_argument("--save", action="store_true", help="Guardar resultados en JSON")
    args = parser.parse_args()

    cfg = _get_neo4j_config()
    if not cfg:
        print("[ERROR] Neo4j no configurado — verificar .streamlit/secrets.toml")
        sys.exit(1)

    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver(cfg["uri"], auth=(cfg["user"], cfg["password"]))
        driver.verify_connectivity()
        print(f"[OK] Neo4j: {cfg['uri']}")
    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  ANALÍTICA CONSTITUCIONAL QUIRA — ADR-020")
    print(f"{'='*60}")

    G, id_to_name = export_to_networkx(driver)
    driver.close()

    results = compute_all(G, id_to_name, top_n=args.top)
    evaluate_adr019(results)

    if args.save:
        out_path = ROOT / "data" / "centrality_results.json"
        # Serializar (NetworkX usa node IDs como keys)
        serializable = {metric: {k: round(v, 6) for k, v in vals.items()}
                       for metric, vals in results.items()}
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
        print(f"[OK] Resultados guardados en {out_path}")


if __name__ == "__main__":
    main()
