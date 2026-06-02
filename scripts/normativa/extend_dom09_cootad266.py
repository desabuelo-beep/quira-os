#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extend_dom09_cootad266.py — Gate 3: COOTAD_266 + cierre normativo ciclo democrático
QUIRA Gov · Dylus Lab · 2026-06-02

PROPÓSITO:
  Cargar COOTAD_266 como nodo ACK estructural en Neo4j y establecer
  las tres relaciones que cierran el ciclo democrático municipal:
    1. COOTAD_266 -[INSTRUMENTA]-> Dom09  (ancla fiscal RC)
    2. COOTAD_266 -[INSTRUMENTA]-> Dom02  (nexo RC↔presupuesto)
    3. COOTAD_266 -[INSTRUMENTA]-> Dom04  (nexo RC↔planificación)
    4. Dom09 -[RETROALIMENTA]-> Dom08    (actualizar metadata con base normativa)

  OBS-003: El ciclo Dom09→Dom08 no fue inferido por QUIRA —
  está positivizado en COOTAD_266 desde 2010.

  sha256 verificado: 0f71df4207f9c54f386fbba882eb6a982507e75159596176f3f8a4214c83b709
  Corpus: COOTAD F0.3 · articulo_num=266 · 65 palabras

USO:
  python scripts/normativa/extend_dom09_cootad266.py
  python scripts/normativa/extend_dom09_cootad266.py --dry-run
  python scripts/normativa/extend_dom09_cootad266.py --validate

Bloomberg Model: Script INTERNO — Dylus Lab / QUIRA Operaciones.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.parent


# ══════════════════════════════════════════════════════════════════════════════
# CYPHER: COOTAD_266 — Nodo ACK estructural de cierre del ciclo democrático
# ══════════════════════════════════════════════════════════════════════════════

CYPHER_COOTAD266_NODE = """
// COOTAD Art. 266 — Rendición de Cuentas al cierre del ejercicio fiscal
// sha256: 0f71df4207f9c54f386fbba882eb6a982507e75159596176f3f8a4214c83b709
// Gate 3 · OBS-003 · 2026-06-02

MERGE (a:ACK {ack_id: 'COOTAD_266'})
SET a.nombre          = 'Rendición de Cuentas al cierre del ejercicio fiscal',
    a.tipo            = 'obligacion',
    a.es_nrc          = false,
    a.fundante        = true,
    a.norma_sigla     = 'COOTAD',
    a.articulo        = '266',
    a.jerarquia       = 1,
    a.sha256_corpus   = '0f71df4207f9c54f386fbba882eb6a982507e75159596176f3f8a4214c83b709',
    a.palabras        = 65,
    a.obs_ref         = 'OBS-003'
"""

CYPHER_COOTAD266_DOM09 = """
// COOTAD_266 → Dom09: ancla fiscal de la RC anual
MATCH (a:ACK {ack_id: 'COOTAD_266'})
MATCH (d09:Dominio {id: 'Dom09'})
MERGE (a)-[:INSTRUMENTA {
    capa: 'C2_obligacion',
    nota: 'Obliga al ejecutivo del GAD a convocar asamblea territorial al cierre fiscal para RC — ancla temporal verificable (31 dic cada año)',
    etapa_circuito: 'RENDICION',
    obs_ref: 'OBS-003'
}]->(d09)
"""

CYPHER_COOTAD266_DOM02 = """
// COOTAD_266 → Dom02: nexo RC↔presupuesto (ejecución presupuestaria anual)
MATCH (a:ACK {ack_id: 'COOTAD_266'})
MATCH (d02:Dominio {id: 'Dom02'})
MERGE (a)-[:INSTRUMENTA {
    capa: 'C2_obligacion',
    nota: 'RC debe incluir informe de ejecución presupuestaria anual — nexo directo Dom09↔Dom02',
    etapa_circuito: 'OBSERVACION',
    obs_ref: 'OBS-003'
}]->(d02)
"""

CYPHER_COOTAD266_DOM04 = """
// COOTAD_266 → Dom04: nexo RC↔planificación (cumplimiento de metas PDOT)
MATCH (a:ACK {ack_id: 'COOTAD_266'})
MATCH (d04:Dominio {id: 'Dom04'})
MERGE (a)-[:INSTRUMENTA {
    capa: 'C2_obligacion',
    nota: 'RC debe informar sobre cumplimiento de metas del plan de desarrollo — nexo Dom09↔Dom04 (PDOT)',
    etapa_circuito: 'OBSERVACION',
    obs_ref: 'OBS-003'
}]->(d04)
"""

CYPHER_DOM09_RETROALIMENTA_UPDATE = """
// Actualizar Dom09-[RETROALIMENTA]->Dom08 con base normativa COOTAD_266
// La relación ya existe (commit b6aefa6); aquí se enriquece con la cita normativa
MATCH (d09:Dominio {id: 'Dom09'})-[r:RETROALIMENTA]->(d08:Dominio {id: 'Dom08'})
SET r.base_normativa = 'COOTAD_266',
    r.texto_normativo = 'prioridades de ejecución del siguiente año',
    r.obs_ref         = 'OBS-003',
    r.nota            = 'Positivizado en COOTAD Art.266: la RC define prioridades del siguiente año → retroalimenta el nuevo ciclo PP (Dom08)'
"""

CYPHER_VALIDATE = """
// Validación: COOTAD_266 y sus relaciones en el grafo
MATCH (a:ACK {ack_id: 'COOTAD_266'})
OPTIONAL MATCH (a)-[r:INSTRUMENTA]->(d)
RETURN a.ack_id AS ack, type(r) AS rel, d.id AS dominio, r.etapa_circuito AS etapa
ORDER BY dominio
"""

CYPHER_VALIDATE_RETRO = """
// Verificar actualización Dom09-[RETROALIMENTA]->Dom08
MATCH (d09:Dominio {id:'Dom09'})-[r:RETROALIMENTA]->(d08:Dominio {id:'Dom08'})
RETURN d09.id, type(r), d08.id, r.base_normativa, r.obs_ref
"""

ALL_STEPS = [
    ("COOTAD_266 nodo ACK",              CYPHER_COOTAD266_NODE),
    ("COOTAD_266 → Dom09 INSTRUMENTA",   CYPHER_COOTAD266_DOM09),
    ("COOTAD_266 → Dom02 INSTRUMENTA",   CYPHER_COOTAD266_DOM02),
    ("COOTAD_266 → Dom04 INSTRUMENTA",   CYPHER_COOTAD266_DOM04),
    ("Dom09-[RETROALIMENTA]→Dom08 update", CYPHER_DOM09_RETROALIMENTA_UPDATE),
]


def _get_neo4j_config() -> dict:
    try:
        import toml
        secrets_path = ROOT / ".streamlit" / "secrets.toml"
        secrets = toml.load(str(secrets_path))
        cfg = secrets.get("neo4j", {})
        return cfg if cfg.get("password") else {}
    except Exception:
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="Gate 3: COOTAD_266 — cierre normativo ciclo democrático municipal")
    parser.add_argument("--dry-run",  action="store_true", help="Solo mostrar Cypher, no ejecutar")
    parser.add_argument("--validate", action="store_true", help="Solo ejecutar queries de validación")
    args = parser.parse_args()

    if args.dry_run:
        print("\n=== DRY RUN — Cypher que se ejecutaría ===\n")
        for desc, cypher in ALL_STEPS:
            print(f"--- {desc} ---")
            print(cypher.strip())
            print()
        return

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

    db_name = cfg.get("database", "neo4j")

    if args.validate:
        with driver.session(database=db_name) as s:
            print("\n=== Validación COOTAD_266 ===")
            result = s.run(CYPHER_VALIDATE)
            rows = list(result)
            if not rows:
                print("  [!] COOTAD_266 no encontrado en Neo4j")
            for r in rows:
                print(f"  {r['ack']} -[{r['rel']}]-> {r['dominio']}  etapa={r['etapa']}")

            print("\n=== Validación RETROALIMENTA metadata ===")
            result2 = s.run(CYPHER_VALIDATE_RETRO)
            for r in result2:
                print(f"  {r['d09.id']} -[{r['type(r)']}]-> {r['d08.id']}  base_normativa={r['r.base_normativa']}  obs={r['r.obs_ref']}")
        driver.close()
        return

    print(f"\n{'='*60}")
    print(f"  GATE 3 — COOTAD_266 · Cierre normativo ciclo democrático")
    print(f"{'='*60}")

    with driver.session(database=db_name) as s:
        for desc, cypher in ALL_STEPS:
            print(f"\n  → {desc}")
            result = s.run(cypher)
            summary = result.consume()
            nodes_c   = summary.counters.nodes_created
            rels_c    = summary.counters.relationships_created
            props_set = summary.counters.properties_set
            print(f"     nodos_creados={nodes_c}  rels_creadas={rels_c}  props_set={props_set}")

    print(f"\n{'='*60}")
    print(f"  RESUMEN: COOTAD_266 cargado con 3 relaciones INSTRUMENTA")
    print(f"  Dom09-[RETROALIMENTA]->Dom08 actualizado con base normativa")
    print(f"  OBS-003: ciclo democrático municipal positivizado en norma ✓")
    print(f"{'='*60}\n")

    driver.close()


if __name__ == "__main__":
    main()
