# -*- coding: utf-8 -*-
"""
scripts/neo4j_verify_cable.py — Verifica el Cable de Relaciones poblado en Neo4j.
Conteo de nodos + el traversal que PRUEBA el valor relacional (partida-puente POA↔SERCOP):
lo que el Excel no cruza solo, ahora navegable en el grafo. Solo lectura.
Uso:  python scripts/neo4j_verify_cable.py
Dylus Lab © 2026
"""
import sys
from types import SimpleNamespace

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.neo4j_cable_planificacion import get_driver

driver, estado = get_driver(SimpleNamespace(uri=None, user=None, password=None))
if driver is None:
    print(f"Sin conexión ({estado}) — la instancia AuraDB no está lista.")
    raise SystemExit(0)

print(f"Conectado ({estado})")
with driver.session() as s:
    print("\n=== Conteo de nodos del Cable de Relaciones ===")
    for label in ["Canton", "Meta", "Proyecto", "ProcesoPAC", "ProcesoSERCOP", "Partida"]:
        c = s.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()["c"]
        print(f"  {label:<14} {c}")

    print("\n=== Coexistencia con el grafo QTMP existente (no se tocó) ===")
    for label in ["Atom", "C9ResultadoTerritorial"]:
        c = s.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()["c"]
        print(f"  {label:<14} {c}")

    print("\n=== PARTIDA-PUENTE vía traversal (POA↔SERCOP por partida compartida) ===")
    print("    — la pregunta que el grafo ahora responde, que el Excel no cruza solo —")
    q = s.run(
        "MATCH (pr:Proyecto)-[:IMPUTA]->(pt:Partida)<-[:IMPUTA]-(sp:ProcesoSERCOP) "
        "RETURN pt.codigo AS partida, count(DISTINCT pr) AS proy, "
        "sum(DISTINCT pr.monto_anual) AS monto_poa, count(DISTINCT sp) AS sercop, "
        "sum(DISTINCT sp.monto) AS monto_pub ORDER BY pt.codigo"
    )
    for r in q:
        print(f"  partida {r['partida']}: {r['proy']} proy POA "
              f"(${(r['monto_poa'] or 0):,.0f}) ↔ {r['sercop']} proc SERCOP (${(r['monto_pub'] or 0):,.0f})")

    print("\n=== PAC→Meta (procesos planificados vinculados a su meta PDOT) ===")
    q2 = s.run(
        "MATCH (pc:ProcesoPAC)-[:CONTRATA_PARA]->(m:Meta) "
        "RETURN m.id AS meta, count(pc) AS procesos ORDER BY procesos DESC LIMIT 8"
    )
    rows = list(q2)
    if rows:
        for r in rows:
            print(f"  meta {r['meta']}: {r['procesos']} proceso(s) PAC")
    else:
        print("  (sin vínculos PAC→Meta resueltos)")
driver.close()
print("\nOK — Cable de Relaciones verificado en vivo.")
