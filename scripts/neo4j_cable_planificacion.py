# -*- coding: utf-8 -*-
"""
scripts/neo4j_cable_planificacion.py — QUIRA OS · Cable de Relaciones del MCD Planificación
═══════════════════════════════════════════════════════════════════════════════════════════
ADR-031: el MCD se construye cableando capacidades. Esta es la capacidad RELACIONES (Neo4j) —
"lo que el Excel jamás puede hacer solo". NO redefine el grafo QNKC existente (Atom→C3→…→C9):
añade un esquema OPERACIONAL que COEXISTE y se ancla al `Canton` ya existente (Regla #6: derivar).

Cadena (extensible a proveedor→contrato→pago→impacto · ADR-031 §5):

    (:Meta)──EJECUTA──►              (Meta PDOT 25)
       ▲                            (:Proyecto POA 257)──IMPUTA──►(:Partida)
    (:Proyecto)                     (:ProcesoPAC)──CONTRATA_PARA──►(:Meta)
    (:ProcesoSERCOP)──IMPUTA──►(:Partida)   ← la Partida es el tejido conectivo plan↔publicado
    (:Meta)──DEL_CANTON──►(:Canton ECU-13-MONTECRISTI)   ← ancla al grafo existente

Doctrina (ADR-031): "No diseñamos; leemos y ruteamos." Lee el snapshot (ya verificado, del
Canon vía enricher); NO recalcula nada. Idempotente (MERGE). Si no hay Neo4j vivo → DRY-RUN
(construye y reporta el Cable sin escribir; sirve para verificar la cosecha).

Uso:
  python scripts/neo4j_cable_planificacion.py                 # dry-run (sin credenciales)
  python scripts/neo4j_cable_planificacion.py --uri bolt://… --user neo4j --password ***   # vivo
  (o credenciales en .streamlit/secrets.toml [neo4j] / env NEO4J_URI·NEO4J_USER·NEO4J_PASSWORD)
Dylus Lab © 2026 — DOCUMENTO INTERNO
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
SECRETS = REPO / ".streamlit" / "secrets.toml"
CANTON_ID = "ECU-13-MONTECRISTI"   # nodo ya existente en el grafo (neo4j_load_qtmp)


# ══════════════════════════════════════════════════════════════════════════════
# CONEXIÓN (deriva del patrón de neo4j_load_qtmp · con fallback a DRY-RUN)
# ══════════════════════════════════════════════════════════════════════════════
def get_driver(args):
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return None, "lib 'neo4j' no instalada"
    uri = args.uri or os.getenv("NEO4J_URI")
    user = args.user or os.getenv("NEO4J_USER") or "neo4j"
    pwd = args.password or os.getenv("NEO4J_PASSWORD")
    if (not uri or not pwd) and SECRETS.exists():
        try:
            import tomllib  # py3.11+
            with open(SECRETS, "rb") as f:
                n = (tomllib.load(f) or {}).get("neo4j", {})
            uri = uri or n.get("uri") or n.get("url")
            user = n.get("user", user)
            pwd = pwd or n.get("password")
        except Exception:
            pass
    if not uri or not pwd:
        return None, "sin credenciales (uri/password)"
    try:
        drv = GraphDatabase.driver(uri, auth=(user, pwd))
        with drv.session() as s:
            s.run("RETURN 1").consume()
        return drv, f"conectado a {uri}"
    except Exception as e:
        return None, f"conexión falló: {str(e)[:60]}"


# ══════════════════════════════════════════════════════════════════════════════
# COSECHA — del snapshot al Cable (statements idempotentes)
# ══════════════════════════════════════════════════════════════════════════════
def construir_cable(plan: dict) -> tuple[list, dict]:
    """Devuelve (statements, stats). Cada statement = (cypher, params)."""
    metas = plan.get("metas_detalle", [])
    proys = plan.get("poa_proyectos", [])
    pac = plan.get("pac_detalle", [])
    pub = (plan.get("publicado", {}) or {}).get("procesos", [])

    meta_ids = {str(m["id"]).strip() for m in metas if m.get("id")}
    partidas: set[str] = set()
    st = []  # statements

    # Canton ancla (MERGE — ya existe; no lo pisa)
    st.append(("MERGE (c:Canton {id:$id})", {"id": CANTON_ID}))

    # 1 · Metas (PDOT) → ancladas al Canton
    for m in metas:
        mid = str(m.get("id", "")).strip()
        if not mid:
            continue
        st.append((
            """MERGE (m:Meta {id:$id})
               SET m.descripcion=$desc, m.sistema=$sis, m.competencia=$comp,
                   m.direccion=$dir, m.canton_id=$cant, m.capa='RELACIONES'
               WITH m MATCH (c:Canton {id:$cant}) MERGE (m)-[:DEL_CANTON]->(c)""",
            {"id": mid, "desc": (m.get("meta") or "")[:120], "sis": m.get("sistema", ""),
             "comp": m.get("competencia", ""), "dir": m.get("direccion", ""), "cant": CANTON_ID},
        ))

    # 2 · Proyectos (POA) → EJECUTA Meta (si resuelve) · IMPUTA Partida
    links_poa_meta = {"ok": 0, "miss": 0}
    for i, p in enumerate(proys):
        pid = f"POA-{i:03d}"
        part = str(p.get("partida", "")).strip()
        st.append((
            """MERGE (pr:Proyecto {id:$id})
               SET pr.descripcion=$desc, pr.direccion=$dir, pr.partida=$part,
                   pr.monto_anual=$monto, pr.canton_id=$cant, pr.capa='RELACIONES'""",
            {"id": pid, "desc": (p.get("desc") or p.get("proyecto") or "")[:120],
             "dir": p.get("dir", ""), "part": part, "monto": p.get("anual") or 0, "cant": CANTON_ID},
        ))
        mref = str(p.get("meta", "")).strip()
        if mref in meta_ids:
            st.append(("MATCH (pr:Proyecto {id:$pid}),(m:Meta {id:$mid}) MERGE (pr)-[:EJECUTA]->(m)",
                       {"pid": pid, "mid": mref}))
            links_poa_meta["ok"] += 1
        else:
            links_poa_meta["miss"] += 1
        if part:
            partidas.add(part)
            st.append((
                """MERGE (pt:Partida {codigo:$cod})
                   WITH pt MATCH (pr:Proyecto {id:$pid}) MERGE (pr)-[:IMPUTA]->(pt)""",
                {"cod": part, "pid": pid}))

    # 3 · Procesos PAC (plan) → CONTRATA_PARA Meta (si resuelve)
    links_pac_meta = {"ok": 0, "miss": 0}
    for p in pac:
        pid = str(p.get("id", "")).strip()
        if not pid:
            continue
        st.append((
            """MERGE (pc:ProcesoPAC {id:$id})
               SET pc.descripcion=$desc, pc.tipo=$tipo, pc.monto=$monto,
                   pc.canton_id=$cant, pc.capa='RELACIONES'""",
            {"id": pid, "desc": (p.get("desc") or "")[:120], "tipo": p.get("tipo", ""),
             "monto": p.get("monto") or 0, "cant": CANTON_ID},
        ))
        mref = str(p.get("meta", "")).strip()
        if mref in meta_ids:
            st.append(("MATCH (pc:ProcesoPAC {id:$pid}),(m:Meta {id:$mid}) MERGE (pc)-[:CONTRATA_PARA]->(m)",
                       {"pid": pid, "mid": mref}))
            links_pac_meta["ok"] += 1
        else:
            links_pac_meta["miss"] += 1

    # 4 · Procesos SERCOP (publicado · verificado) → IMPUTA Partida (el tejido conectivo)
    for p in pub:
        ocid = str(p.get("cod", "")).strip()
        if not ocid:
            continue
        part = str(p.get("partida", "")).strip()
        st.append((
            """MERGE (sp:ProcesoSERCOP {ocid:$ocid})
               SET sp.descripcion=$desc, sp.monto=$monto, sp.monto_tipo=$mt,
                   sp.etapa=$etapa, sp.partida=$part, sp.canton_id=$cant, sp.capa='RELACIONES'""",
            {"ocid": ocid, "desc": (p.get("desc") or "")[:120], "monto": p.get("monto") or 0,
             "mt": p.get("monto_tipo", ""), "etapa": p.get("etapa", ""), "part": part, "cant": CANTON_ID},
        ))
        if part:
            partidas.add(part)
            st.append((
                """MERGE (pt:Partida {codigo:$cod})
                   WITH pt MATCH (sp:ProcesoSERCOP {ocid:$ocid}) MERGE (sp)-[:IMPUTA]->(pt)""",
                {"cod": part, "ocid": ocid}))

    # Partidas que conectan POA↔SERCOP (el cruce que el Excel no hace solo)
    poa_parts = {str(p.get("partida", "")).strip() for p in proys if p.get("partida")}
    pub_parts = {str(p.get("partida", "")).strip() for p in pub if p.get("partida")}
    puente = poa_parts & pub_parts

    stats = {
        "metas": len(meta_ids), "proyectos": len(proys), "pac": len([p for p in pac if p.get("id")]),
        "sercop": len([p for p in pub if p.get("cod")]), "partidas": len(partidas),
        "EJECUTA(POA→Meta)": links_poa_meta, "CONTRATA_PARA(PAC→Meta)": links_pac_meta,
        "partidas_puente_POA∩SERCOP": sorted(puente), "statements": len(st),
    }
    return st, stats


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    ap = argparse.ArgumentParser(description="Cable de Relaciones — MCD Planificación | QUIRA OS")
    ap.add_argument("--uri", default=None)
    ap.add_argument("--user", default=None)
    ap.add_argument("--password", default=None)
    args = ap.parse_args()

    plan = (json.loads(SNAP.read_text(encoding="utf-8")) or {}).get("planificacion", {})
    if not plan:
        print("[ERR] sin bloque 'planificacion' en el snapshot — corre enrich_planificacion.py")
        return 1

    statements, stats = construir_cable(plan)

    print("=" * 64)
    print("CABLE DE RELACIONES — MCD Planificación (Neo4j)")
    print("=" * 64)
    for k, v in stats.items():
        print(f"  {k}: {v}")

    driver, estado = get_driver(args)
    print("-" * 64)
    if driver is None:
        print(f"DRY-RUN ({estado}) — Cable construido y verificado, NO escrito.")
        print("Para poblar en vivo: credenciales en .streamlit/secrets.toml [neo4j] o --uri/--password.")
        return 0

    print(f"VIVO ({estado}) — escribiendo el Cable…")
    try:
        from neo4j import GraphDatabase  # noqa
        with driver.session() as s:
            for label, prop in [("Meta", "id"), ("Proyecto", "id"), ("ProcesoPAC", "id"),
                                ("ProcesoSERCOP", "ocid"), ("Partida", "codigo")]:
                try:
                    s.run(f"CREATE INDEX IF NOT EXISTS FOR (n:{label}) ON (n.{prop})")
                except Exception:
                    pass
            for cypher, params in statements:
                s.run(cypher, **params)
        print(f"OK — {len(statements)} statements aplicados (idempotente).")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
