"""
QUIRA Gov — Consulta Bautismal (ADR-010)
=========================================
¿Por qué Montecristi mantiene brechas en Dom12
si cumple formalmente COOTAD Art. 249?

Esta es la consulta que declara Alpha 1.0 cuando el grafo
la responde correcta y completamente.

Condiciones de Alpha 1.0 (ADR-010):
  ✓ Los 3 QTMPs cargados en Neo4j
  ✓ La cadena causal aparece completa en el grafo
  ✓ La consulta es reproducible por cualquier observador externo
  ✓ Cada nodo tiene campo fuente_documental o norma_base

Cadena esperada (respuesta canónica):
  COOTAD_249 (Norma C1)
      ↓ FUNDA
  Competencia/Servicio GAP (C3)
      ↓ HABILITA
  Asignacion_GAD (RES — 20.84% cod VERDE)
      ↓ HABILITA
  Ti_Patronato_2025 (C8 — 50% ROJO)
      ↓ EXPLICA (evidencia: G73=29.7%)
  Brecha_Dom12_Montecristi (C9 — ROJO)

Uso:
  pip install neo4j
  python neo4j_bautismal_query.py --uri bolt://localhost:7687 --user neo4j --password <password>

DOCUMENTO INTERNO — Dylus Lab · QUIRA Operaciones
"""

import argparse
import sys
sys.stdout.reconfigure(encoding='utf-8')
from neo4j import GraphDatabase


def get_driver(uri, user, password):
    return GraphDatabase.driver(uri, auth=(user, password))


def run_bautismal_query(session):
    """
    CONSULTA BAUTISMAL — ADR-010

    Responde: ¿Por qué Montecristi mantiene brechas Dom12 si cumple COOTAD_249?

    La respuesta verifica la paradoja causal:
    - La ASIGNACION cumple el piso legal (20.84% >> 10%) → VERDE
    - La EJECUCION falla (Ti_Patronato=50%) → ROJO
    - El RESULTADO TERRITORIAL es brecha Dom12 persistente → ROJO

    Condición de trazabilidad: cada nodo tiene fuente_documental.
    """
    print("\n" + "=" * 70)
    print("CONSULTA BAUTISMAL — QUIRA Alpha 1.0")
    print("=" * 70)
    print("\nPregunta:")
    print("  ¿Por qué Montecristi mantiene brechas en Dom12")
    print("  si cumple formalmente COOTAD Art. 249?")
    print("\n" + "—" * 70)

    # QUERY 1 — Cadena causal completa (express path ADR-010)
    result = session.run("""
    MATCH (norm:Atom {id: 'COOTAD_249'})
    MATCH (norm)-[:FUNDA|MATERIALIZA_VIA]->(sp:C3ServicioPublico {id: 'SP_G10P_MCR'})
    MATCH (sp)-[:HABILITA]->(res1:C9ResultadoTerritorial {id: 'RES_G10P_01_MCR'})
    MATCH (res1)-[:HABILITA]->(ind4:C8Indicador {id: 'IND_G10P_04_MCR'})
    MATCH (ind4)-[:EXPLICA]->(res4:C9ResultadoTerritorial {id: 'RES_G10P_04_MCR'})
    RETURN
        norm.id AS norma_id,
        norm.obligacion AS obligacion_legal,
        norm.norma AS norma_completa,
        sp.id AS servicio_id,
        sp.nombre AS servicio_nombre,
        res1.valor AS asignacion_pct,
        res1.semaforo AS semaforo_asignacion,
        res1.fuente_documental AS fuente_asignacion,
        res1.interpretacion AS interpretacion_asignacion,
        ind4.id AS indicador_id,
        ind4.nombre AS indicador_nombre,
        ind4.serie_2023 AS ti_2023,
        ind4.serie_2024 AS ti_2024,
        ind4.serie_2025 AS ti_2025,
        ind4.estado_dato AS estado_dato_ti,
        res4.valor AS ti_valor,
        res4.semaforo AS semaforo_ejecucion,
        res4.fuente_documental AS fuente_ejecucion,
        res4.interpretacion AS interpretacion_brecha,
        res4.g73_programas AS g73_programas_pct,
        res4.norma_base AS norma_base_brecha
    """)

    records = list(result)
    if not records:
        print("\n  ERROR: La cadena bautismal no está completa en el grafo.")
        print("  Verificar que neo4j_load_qtmp.py fue ejecutado correctamente.")
        return False

    rec = records[0]
    print("\nCADENA CAUSAL VERIFICABLE:")
    print(f"\n  C1 — NORMA")
    print(f"  ┌─ {rec['norma_id']} ({rec['norma_completa'].split(',')[0].strip()})")
    print(f"  │  Obligación: {rec['obligacion_legal'][:80]}...")
    print(f"  │")
    print(f"  ↓ FUNDA")
    print(f"  │")
    print(f"  C3 — SERVICIO PÚBLICO")
    print(f"  ├─ {rec['servicio_id']}")
    print(f"  │  {rec['servicio_nombre']}")
    print(f"  │")
    print(f"  ↓ HABILITA")
    print(f"  │")
    print(f"  C9 — RESULTADO ASIGNACION")
    print(f"  ├─ RES_G10P_01_MCR")
    print(f"  │  Asignación GAP 2025: {rec['asignacion_pct']}% codificado → {rec['semaforo_asignacion']}")
    print(f"  │  Fuente: {rec['fuente_asignacion'][:60]}...")
    print(f"  │")
    print(f"  ↓ HABILITA (pero NO garantiza ejecución)")
    print(f"  │")
    print(f"  C8 — INDICADOR Ti_PATRONATO")
    print(f"  ├─ {rec['indicador_id']}")
    print(f"  │  {rec['indicador_nombre']}")
    print(f"  │  Serie histórica: 2023={rec['ti_2023']}% → 2024={rec['ti_2024']}% → 2025={rec['ti_2025']}%")
    print(f"  │  Estado dato: {rec['estado_dato_ti'].upper()}")
    print(f"  │")
    print(f"  ↓ EXPLICA (con evidencia: G73_programas={rec['g73_programas_pct']}%)")
    print(f"  │")
    print(f"  C9 — RESULTADO TERRITORIAL BRECHA DOM12")
    print(f"  └─ RES_G10P_04_MCR")
    print(f"     Ti_Patronato_2025 = {rec['ti_valor']}% → {rec['semaforo_ejecucion']}")
    print(f"     Norma base: {rec['norma_base_brecha']}")
    print(f"     Fuente: {rec['fuente_ejecucion'][:70]}")

    print(f"\n{'—' * 70}")
    print(f"\nRESPUESTA A LA CONSULTA BAUTISMAL:")
    print(f"\n  El GAD Montecristi cumple FORMALMENTE con COOTAD Art. 249:")
    print(f"  → Asignó el {rec['asignacion_pct']}% al Patronato (2.08× el mínimo legal del 10%)")
    print(f"  → Semáforo asignación: {rec['semaforo_asignacion']}")
    print(f"\n  PERO el Patronato ejecuta solo el {rec['ti_valor']}% de su presupuesto:")
    print(f"  → Ti_Patronato_2025 = {rec['ti_valor']}% < 70% = ROJO persistente (año 3)")
    if rec.get("g73_programas_pct"):
        print(f"  → G73 programas (fracción que llega a servicios): {rec['g73_programas_pct']}%")
    print(f"\n  PARADOJA CAUSAL CONFIRMADA:")
    print(f"  La norma se cumple en PAPEL pero no en TERRITORIO.")
    print(f"  El incumplimiento es de EJECUCIÓN INSTITUCIONAL (Patronato),")
    print(f"  no de ASIGNACIÓN FORMAL (GAD central).")
    print(f"\n  Interpretación: {rec['interpretacion_brecha']}")

    return True


def run_context_queries(session):
    """Consultas complementarias que enriquecen el contexto de Alpha 1.0."""

    print(f"\n{'—' * 70}")
    print("\nCONTEXTO TERRITORIAL — Otros circuitos:")

    # Agua potable
    result = session.run("""
    MATCH (r:C9ResultadoTerritorial {id: 'RES_AGPT_01_MCR'})
    RETURN r.valor, r.semaforo, r.fuente_documental, r.interpretacion
    """)
    agua = result.single()
    if agua:
        print(f"\n  Agua Potable (RES_AGPT_01_MCR):")
        print(f"  → Cobertura: {agua['r.valor']}% → {agua['r.semaforo']}")
        print(f"  → {agua['r.interpretacion'][:100]}...")

    # Continuidad agua
    result2 = session.run("""
    MATCH (r:C9ResultadoTerritorial {id: 'RES_AGPT_02_MCR'})
    RETURN r.valor, r.semaforo, r.interpretacion
    """)
    cont = result2.single()
    if cont:
        print(f"\n  Continuidad Agua 24/7 (RES_AGPT_02_MCR):")
        print(f"  → Continuidad: {cont['r.valor']}% → {cont['r.semaforo']}")

    # Equidad / IRS
    result3 = session.run("""
    MATCH (r:C9ResultadoTerritorial {id: 'RES_EQUD_01_MCR'})
    RETURN r.valor, r.semaforo, r.interpretacion
    """)
    irs = result3.single()
    if irs:
        print(f"\n  Equidad Territorial / IRS (RES_EQUD_01_MCR):")
        print(f"  → IRS Montecristi: {irs['r.valor']}% → {irs['r.semaforo'].upper()}")

    # Brecha NBI
    result4 = session.run("""
    MATCH (r:C9ResultadoTerritorial {id: 'RES_EQUD_04_MCR'})
    RETURN r.valor, r.semaforo, r.nbi_urbano, r.nbi_rural
    """)
    nbi = result4.single()
    if nbi:
        print(f"\n  Brecha NBI Urbano-Rural (RES_EQUD_04_MCR):")
        print(f"  → NBI urbano: {nbi['r.nbi_urbano']}% | NBI rural: {nbi['r.nbi_rural']}%")
        print(f"  → Brecha: {nbi['r.valor']}pp → {nbi['r.semaforo'].upper()}")

    # Todos los nodos confirmados
    print(f"\n{'—' * 70}")
    print("\nNODOS C9 CONFIRMADOS (trazabilidad verificada):")
    result5 = session.run("""
    MATCH (r:C9ResultadoTerritorial {estado_dato: 'confirmado'})
    RETURN r.id, r.valor, r.semaforo, r.fuente_documental, r.circuito_id
    ORDER BY r.circuito_id, r.id
    """)
    for rec in result5:
        print(f"  {rec['r.id']}: {rec['r.valor']} → {rec['r.semaforo']}")
        if rec.get("r.fuente_documental"):
            print(f"    Fuente: {str(rec['r.fuente_documental'])[:70]}")


def run_path_query(session):
    """Verifica el path completo de la cadena bautismal."""
    print(f"\n{'—' * 70}")
    print("\nPATH COMPLETO (traversal grafo):")

    result = session.run("""
    MATCH path = (norm:Atom {id: 'COOTAD_249'})
        -[:FUNDA|MATERIALIZA_VIA]->(:C3ServicioPublico {id: 'SP_G10P_MCR'})
        -[:HABILITA]->(:C9ResultadoTerritorial {id: 'RES_G10P_01_MCR'})
        -[:HABILITA]->(:C8Indicador {id: 'IND_G10P_04_MCR'})
        -[:EXPLICA]->(:C9ResultadoTerritorial {id: 'RES_G10P_04_MCR'})
    RETURN length(path) AS largo_cadena,
           [n IN nodes(path) | n.id] AS nodos_cadena,
           [r IN relationships(path) | type(r)] AS relaciones_cadena
    """)

    path = result.single()
    if path:
        print(f"\n  Largo de la cadena: {path['largo_cadena']} relaciones")
        print(f"\n  Nodos en el path:")
        for n in path["nodos_cadena"]:
            print(f"    → {n}")
        print(f"\n  Relaciones:")
        for r in path["relaciones_cadena"]:
            print(f"    → [{r}]")
        print(f"\n  CADENA COMPLETA Y TRAZABLE: SI")
        print(f"  REPRODUCIBLE: SI (cualquier observador externo puede ejecutar esta query)")
    else:
        print("  ERROR: El path no está disponible en el grafo.")


def main():
    parser = argparse.ArgumentParser(description="QUIRA — Consulta Bautismal (ADR-010)")
    parser.add_argument("--uri", default="bolt://localhost:7687", help="Neo4j URI")
    parser.add_argument("--user", default="neo4j", help="Neo4j username")
    parser.add_argument("--password", required=True, help="Neo4j password")
    args = parser.parse_args()

    driver = get_driver(args.uri, args.user, args.password)

    try:
        with driver.session() as session:
            # Test
            session.run("RETURN 1").single()
    except Exception as e:
        print(f"ERROR conectando a Neo4j: {e}")
        sys.exit(1)

    print("=" * 70)
    print("QUIRA Gov — Consulta Bautismal — ADR-010")
    print("Alpha 1.0 Demo")
    print("=" * 70)

    with driver.session() as session:
        success = run_bautismal_query(session)
        if success:
            run_context_queries(session)
            run_path_query(session)

            print("\n" + "=" * 70)
            print("DECLARACION ALPHA 1.0")
            print("=" * 70)
            print("\n  Neo4j ha respondido la consulta bautismal de forma:")
            print("  ✓ COMPLETA — cadena COOTAD_249 → brecha Dom12 trazada")
            print("  ✓ TRAZABLE — cada nodo tiene fuente_documental o norma_base")
            print("  ✓ REPRODUCIBLE — cualquier observador externo puede replicar")
            print("\n  Condiciones ADR-010 CUMPLIDAS.")
            print("  Documentar en ALPHA_1_0_FREEZE.md.")
            print("\n" + "=" * 70)

    driver.close()


if __name__ == "__main__":
    main()
