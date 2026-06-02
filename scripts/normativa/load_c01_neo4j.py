#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
load_c01_neo4j.py — Carga C01 en Neo4j con grafo constitucional completo
QUIRA Gov · Dylus Lab · 2026-06-02

PROPÓSITO:
  Cargar el Circuito Constitucional C01 (Transparencia → Participación → Planificación)
  en Neo4j, incluyendo los Nodos Raíz Constitucionales (NRC) definidos en ADR-018.

  Cuando este script termina exitosamente, Neo4j puede responder:
    "¿Por qué C01 está colapsado?" → trazabilidad descendente:
    Diagnóstico → C01 → Dom07 → CE_18 → CE_226

  Fuentes de doctrina:
    ADR-017: Cypher base de C01 (nodos + aristas causales entre dominios)
    ADR-018: Extensión NRC (CE_226 como axioma raíz · relaciones HABILITA)
    ACK Registry v0.2: 4 NRCs confirmados

PREREQUISITO — secrets.toml debe tener:
  [neo4j]
  uri      = "bolt://localhost:7687"          # o Neo4j Aura URI
  user     = "neo4j"
  password = "tu_password"

  Para Neo4j Aura (cloud gratuito): https://neo4j.com/cloud/platform/aura-graph-database/
  URI tiene formato: neo4j+s://xxxx.databases.neo4j.io

USO:
  python scripts/normativa/load_c01_neo4j.py             # carga + valida
  python scripts/normativa/load_c01_neo4j.py --dry-run   # solo muestra Cypher
  python scripts/normativa/load_c01_neo4j.py --validate  # solo validación (requiere nodos)
  python scripts/normativa/load_c01_neo4j.py --link-results  # conecta C01 al resultado TRANS

Bloomberg Model:
  Este script es INTERNO — Dylus Lab / QUIRA Operaciones.
  Los node IDs (Dom07, C01, CE_226) NUNCA se exponen en UI pública.
"""
from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

# Windows console UTF-8 fix
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent.parent


# ══════════════════════════════════════════════════════════════════════════════
# CYPHER: GRAFO CONSTITUCIONAL C01 + NRCs
# Base: ADR-017 · Extensión: ADR-018 (NRC)
# ══════════════════════════════════════════════════════════════════════════════

# ─ Paso 1: Nodos Raíz Constitucionales (NRC) ─ ADR-018 ───────────────────────
CYPHER_NRC = """
// ADR-018: Nodos Raíz Constitucionales — axiomas del sistema QUIRA
// Criterio: su eliminación rompe 2+ dominios independientes

MERGE (nrc226:ACK {ack_id: 'CE_226'})
SET nrc226.nombre     = 'Principio de Legalidad Administrativa',
    nrc226.tipo       = 'principio',
    nrc226.es_nrc     = true,
    nrc226.norma_sigla = 'CE',
    nrc226.articulo   = '226',
    nrc226.jerarquia  = 0,
    nrc226.obligacion = 'Las instituciones del Estado ejercerán solamente las competencias y facultades que les sean atribuidas en la Constitución y la ley.',
    nrc226.sha256_corpus = 'f1ea501c97afb2e9dab889ee061fd22c6d87176828fc3a21d61e2cdab4796c5d'

MERGE (nrc18:ACK {ack_id: 'CE_18'})
SET nrc18.nombre     = 'Derecho de acceso a información pública',
    nrc18.tipo       = 'derecho',
    nrc18.es_nrc     = true,
    nrc18.norma_sigla = 'CE',
    nrc18.articulo   = '18',
    nrc18.jerarquia  = 0,
    nrc18.obligacion = 'Toda persona tiene derecho a acceder libremente a la información generada en entidades públicas.',
    nrc18.sha256_corpus = '848f507bcaf4654bf78887e3ac5291fc48d738bc5c8f2749dc9fdc502cbd7c07'

MERGE (nrc95:ACK {ack_id: 'CE_95'})
SET nrc95.nombre     = 'Participación ciudadana protagónica en asuntos públicos',
    nrc95.tipo       = 'derecho',
    nrc95.es_nrc     = true,
    nrc95.norma_sigla = 'CE',
    nrc95.articulo   = '95',
    nrc95.jerarquia  = 0,
    nrc95.obligacion = 'Las ciudadanas y ciudadanos participarán de manera protagónica en la toma de decisiones, planificación y gestión de los asuntos públicos.',
    nrc95.sha256_corpus = 'b92f8bff98e7ecc396c345febdadaacff534862b691f159b90ab07ff9aaf82e5'

MERGE (nrc264:ACK {ack_id: 'CE_264'})
SET nrc264.nombre     = 'Competencias exclusivas del GAD Municipal',
    nrc264.tipo       = 'competencia_exclusiva',
    nrc264.es_nrc     = true,
    nrc264.norma_sigla = 'CE',
    nrc264.articulo   = '264',
    nrc264.jerarquia  = 0,
    nrc264.sha256_corpus = '8a610fc989a27680bc74773949859e89e1a17000a4f3e8c6c4a7f7b8f9906958'
"""

# ─ Paso 2: ACKs sectoriales ───────────────────────────────────────────────────
CYPHER_ACKS_SECTORIALES = """
// ACKs sectoriales que instrumentan los NRCs en Dom07
MERGE (lotaip7:ACK {ack_id: 'LOTAIP_7'})
SET lotaip7.nombre     = 'Obligaciones de transparencia activa — publicación portal oficial',
    lotaip7.tipo       = 'obligacion',
    lotaip7.es_nrc     = false,
    lotaip7.norma_sigla = 'LOTAIP',
    lotaip7.articulo   = '7',
    lotaip7.jerarquia  = 1,
    lotaip7.sha256_corpus = '415a04b64d24208424018e8b3f24126c3a13195c7129cc9ec31772389f32695b'
"""

# ─ Paso 3: Dominios ───────────────────────────────────────────────────────────
CYPHER_DOMINIOS = """
// Dominios del Circuito C01
MERGE (d07:Dominio {id: 'Dom07'})
SET d07.nombre    = 'Transparencia',
    d07.dco_activo = true,
    d07.chs_rol   = 'ORIGEN'

MERGE (d08:Dominio {id: 'Dom08'})
SET d08.nombre    = 'Participación',
    d08.dco_activo = false,
    d08.chs_rol   = 'INTERMEDIARIO'

MERGE (d04:Dominio {id: 'Dom04'})
SET d04.nombre    = 'Planificación',
    d04.dco_activo = false,
    d04.chs_rol   = 'DESTINO'
"""

# ─ Paso 4: Circuito C01 ───────────────────────────────────────────────────────
CYPHER_CIRCUITO = """
// Circuito Constitucional C01 (ADR-017)
MERGE (c01:Circuito {id: 'C01'})
SET c01.nombre         = 'Transparencia → Participación → Planificación',
    c01.triangulo      = 'P-02',
    c01.estado         = 'ACTIVO',
    c01.version        = '1.0',
    c01.peso_total     = 3.2,
    c01.chs_formula    = 'Sigma(NodeOK_i × peso_rol_i) / Sigma(peso_rol_i)',
    c01.colapso_regla  = 'Si ORIGEN falla, CHS = 0.0 independiente del resto'
"""

# ─ Paso 5: Relaciones NRC → NRC (HABILITA) — ADR-018 ─────────────────────────
CYPHER_NRC_HABILITA = """
// CE_226 (axioma raíz) habilita a todos los demás NRCs
MERGE (nrc226:ACK {ack_id: 'CE_226'})
MERGE (nrc18:ACK {ack_id: 'CE_18'})
MERGE (nrc95:ACK {ack_id: 'CE_95'})
MERGE (nrc264:ACK {ack_id: 'CE_264'})

MERGE (nrc226)-[:HABILITA {
    razon: 'El principio de legalidad habilita el ejercicio del derecho a la información',
    adr: 'ADR-018'
}]->(nrc18)

MERGE (nrc226)-[:HABILITA {
    razon: 'El principio de legalidad habilita el derecho de participación protagónica',
    adr: 'ADR-018'
}]->(nrc95)

MERGE (nrc226)-[:HABILITA {
    razon: 'El principio de legalidad habilita las competencias exclusivas del GAD',
    adr: 'ADR-018'
}]->(nrc264)
"""

# ─ Paso 6: Relaciones ACK → Dominio (FUNDA) ──────────────────────────────────
CYPHER_ACK_FUNDA = """
// NRCs fundan dominios (relación constitucional directa)
MERGE (nrc18:ACK  {ack_id: 'CE_18'})
MERGE (nrc95:ACK  {ack_id: 'CE_95'})
MERGE (nrc264:ACK {ack_id: 'CE_264'})
MERGE (lotaip7:ACK {ack_id: 'LOTAIP_7'})
MERGE (d07:Dominio {id: 'Dom07'})
MERGE (d08:Dominio {id: 'Dom08'})
MERGE (d04:Dominio {id: 'Dom04'})

MERGE (nrc18)-[:FUNDA {
    tipo: 'norma_fundante',
    circuito: 'C01',
    nota: 'CE_18 crea el derecho — Dom07 lo institucionaliza'
}]->(d07)

MERGE (nrc95)-[:FUNDA {
    tipo: 'norma_fundante',
    circuito: 'C01',
    nota: 'CE_95 crea el mandato de participación protagónica'
}]->(d08)

MERGE (nrc264)-[:FUNDA {
    tipo: 'norma_fundante',
    circuito: 'C01',
    nota: 'CE_264.1 habilita planificación cantonal como competencia exclusiva'
}]->(d04)

// LOTAIP_7 instrumenta (no funda) — está en C4 del DCO Dom07
MERGE (lotaip7)-[:INSTRUMENTA {
    capa: 'C4_observacion',
    nota: 'LOTAIP_7 es la ventana de observación, no la norma fundante (ADR-016)'
}]->(d07)
"""

# ─ Paso 7: Relaciones Dominio → Circuito (ALIMENTA — dirección causal) ───────
CYPHER_DOM_ALIMENTA = """
// Dominios alimentan al circuito (dirección causal — para queries de trazabilidad)
MERGE (d07:Dominio {id: 'Dom07'})
MERGE (d08:Dominio {id: 'Dom08'})
MERGE (d04:Dominio {id: 'Dom04'})
MERGE (c01:Circuito {id: 'C01'})

MERGE (d07)-[:ALIMENTA {rol: 'ORIGEN',        peso: 1.5, circuito: 'C01'}]->(c01)
MERGE (d08)-[:ALIMENTA {rol: 'INTERMEDIARIO', peso: 1.0, circuito: 'C01'}]->(c01)
MERGE (d04)-[:ALIMENTA {rol: 'DESTINO',       peso: 0.7, circuito: 'C01'}]->(c01)
"""

# ─ Paso 8: Relaciones Circuito → Dominio (INCLUYE — dirección estructural) ───
CYPHER_CIRC_INCLUYE = """
// Circuito incluye dominios (dirección estructural — para queries de composición)
MERGE (c01:Circuito {id: 'C01'})
MERGE (d07:Dominio {id: 'Dom07'})
MERGE (d08:Dominio {id: 'Dom08'})
MERGE (d04:Dominio {id: 'Dom04'})

MERGE (c01)-[:INCLUYE {rol: 'ORIGEN',        peso: 1.5}]->(d07)
MERGE (c01)-[:INCLUYE {rol: 'INTERMEDIARIO', peso: 1.0}]->(d08)
MERGE (c01)-[:INCLUYE {rol: 'DESTINO',       peso: 0.7}]->(d04)
"""

# ─ Paso 9: Relaciones causales entre dominios (ADR-017) ──────────────────────
CYPHER_ARISTAS_CAUSALES = """
// Causalidad constitucional entre dominios (ADR-017 aristas)
MERGE (d07:Dominio {id: 'Dom07'})
MERGE (d08:Dominio {id: 'Dom08'})
MERGE (d04:Dominio {id: 'Dom04'})

MERGE (d07)-[:INFORMA {
    circuito:  'C01',
    mecanismo: 'CE_18 → CE_95',
    texto:     'Sin información pública actualizada, la participación ciudadana carece de insumo. CE Art.18 garantiza el derecho a recibir información veraz y oportuna.',
    acks:      'CE_18, LOTAIP_7, LOTAIP_34'
}]->(d08)

MERGE (d08)-[:HABILITA {
    circuito:  'C01',
    mecanismo: 'CE_95 → CE_264_1',
    texto:     'La participación ciudadana es un insumo constitucional de la planificación territorial. Sin procesos participativos formales, el PDOT no tiene legitimidad democrática constitucional.',
    acks:      'CE_95, CE_264_1, COOTAD_302'
}]->(d04)
"""

# ── Todos los pasos en orden canónico ────────────────────────────────────────
ALL_CYPHER_STEPS = [
    ("NRCs — Nodos Raíz Constitucionales (ADR-018)",           CYPHER_NRC),
    ("ACKs sectoriales",                                        CYPHER_ACKS_SECTORIALES),
    ("Dominios C01",                                            CYPHER_DOMINIOS),
    ("Circuito C01 (ADR-017)",                                  CYPHER_CIRCUITO),
    ("Relaciones NRC → NRC (HABILITA — ADR-018)",               CYPHER_NRC_HABILITA),
    ("Relaciones ACK → Dominio (FUNDA / INSTRUMENTA)",          CYPHER_ACK_FUNDA),
    ("Relaciones Dominio → Circuito (ALIMENTA — causal)",       CYPHER_DOM_ALIMENTA),
    ("Relaciones Circuito → Dominio (INCLUYE — estructural)",   CYPHER_CIRC_INCLUYE),
    ("Aristas causales entre dominios (ADR-017)",               CYPHER_ARISTAS_CAUSALES),
]


# ══════════════════════════════════════════════════════════════════════════════
# CYPHER DE VALIDACIÓN — Las 4 consultas del colega asesor
# Estas consultas demuestran que el grafo responde la cadena completa
# ══════════════════════════════════════════════════════════════════════════════

VALIDATION_QUERIES = [
    {
        "id": "Q1",
        "descripcion": "Circuito completo — Dom07 alimenta C01",
        "cypher": "MATCH p=(:Dominio {id:'Dom07'})-[:ALIMENTA]->(:Circuito {id:'C01'}) RETURN p",
        "expect": "1 path: Dom07 -[ALIMENTA {rol:ORIGEN, peso:1.5}]-> C01",
    },
    {
        "id": "Q2",
        "descripcion": "Fundamento normativo — CE_18 funda Dom07",
        "cypher": "MATCH p=(:ACK {ack_id:'CE_18'})-[:FUNDA]->(:Dominio {id:'Dom07'}) RETURN p",
        "expect": "1 path: CE_18 -[FUNDA {tipo:norma_fundante}]-> Dom07",
    },
    {
        "id": "Q3",
        "descripcion": "NRC superior — CE_226 habilita CE_18",
        "cypher": "MATCH p=(:ACK {ack_id:'CE_226'})-[:HABILITA]->(:ACK {ack_id:'CE_18'}) RETURN p",
        "expect": "1 path: CE_226 -[HABILITA]-> CE_18",
    },
    {
        "id": "Q4_explicit",
        "descripcion": "Explicación completa (cadena explícita) — CE_226 → CE_18 → Dom07 → C01",
        "cypher": (
            "MATCH p=(:ACK {ack_id:'CE_226'})-[:HABILITA]->(:ACK {ack_id:'CE_18'})"
            "-[:FUNDA]->(:Dominio {id:'Dom07'})-[:ALIMENTA]->(:Circuito {id:'C01'}) RETURN p"
        ),
        "expect": "1 path: CE_226 → CE_18 → Dom07 → C01 (primera gobernanza explicable)",
    },
    {
        "id": "Q4_variable",
        "descripcion": "Explicación completa (path variable) — CE_226 cualquier relación hacia C01",
        "cypher": (
            "MATCH p=(:ACK {ack_id:'CE_226'})-[:HABILITA|:FUNDA|:ALIMENTA*1..5]->"
            "(:Circuito {id:'C01'}) RETURN p"
        ),
        "expect": "1+ paths: todos los caminos de CE_226 a C01",
    },
    {
        "id": "Q5_chs",
        "descripcion": "CHS de C01 — pesos de todos los nodos del circuito",
        "cypher": (
            "MATCH (:Circuito {id:'C01'})-[r:INCLUYE]->(d:Dominio) "
            "RETURN d.id AS dominio, d.nombre AS nombre, r.rol AS rol, r.peso AS peso "
            "ORDER BY r.peso DESC"
        ),
        "expect": "3 rows: Dom07 (1.5), Dom08 (1.0), Dom04 (0.7)",
    },
]

# Cypher para conectar C01 con el resultado operacional existente (opcional)
CYPHER_LINK_RESULTS = """
// Conecta el nodo operacional TRANSPARENCIA con el circuito constitucional C01
// Requiere que los resultados TRANSPARENCIA ya estén en Neo4j
MATCH (c01:Circuito {id: 'C01'})
MATCH (d07:Dominio   {id: 'Dom07'})
// Busca el nodo de resultado TRANSPARENCIA si existe en el grafo operacional
OPTIONAL MATCH (res:C9ResultadoTerritorial {id: 'RES_TRANS_01_MCR'})
FOREACH (r IN CASE WHEN res IS NOT NULL THEN [res] ELSE [] END |
    MERGE (res)-[:EVIDENCIA_EN {
        tipo: 'diagnostico_dominio',
        nota: 'Estado operacional de Dom07 medido por auditoría DPE 2025'
    }]->(d07)
)
RETURN 'C01 conectado a resultados operacionales' AS status,
       (res IS NOT NULL) AS resultado_encontrado
"""


# ══════════════════════════════════════════════════════════════════════════════
# CONEXIÓN NEO4J
# ══════════════════════════════════════════════════════════════════════════════

def _get_neo4j_driver():
    """
    Establece conexión con Neo4j usando secrets.toml.
    Requiere:
      [neo4j]
      uri      = "bolt://localhost:7687"
      user     = "neo4j"
      password = "..."
    """
    try:
        import toml
        secrets_path = ROOT / ".streamlit" / "secrets.toml"
        if not secrets_path.exists():
            print("[ERROR] .streamlit/secrets.toml no encontrado")
            return None
        secrets = toml.load(str(secrets_path))
        neo4j_cfg = secrets.get("neo4j", {})
        uri  = neo4j_cfg.get("uri",  "bolt://localhost:7687")
        user = neo4j_cfg.get("user", "neo4j")
        pw   = neo4j_cfg.get("password", "")
        if not pw:
            print("[ERROR] neo4j.password no configurado en secrets.toml")
            print("        Agrega [neo4j] con uri/user/password")
            print("        Neo4j Aura gratuito: https://neo4j.com/cloud/platform/aura-graph-database/")
            return None
    except Exception as exc:
        print(f"[ERROR] No se pudo leer secrets.toml: {exc}")
        return None

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("[ERROR] Paquete neo4j no instalado: pip install neo4j")
        return None

    try:
        driver = GraphDatabase.driver(uri, auth=(user, pw))
        driver.verify_connectivity()
        print(f"[OK] Neo4j conectado: {uri}")
        return driver
    except Exception as exc:
        print(f"[ERROR] Neo4j no disponible: {exc.__class__.__name__}: {exc}")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# CARGA Y VALIDACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def load_c01(driver, dry_run: bool = False) -> bool:
    """Ejecuta todos los pasos de carga de C01."""
    print(f"\n{'='*65}")
    print(f"  CARGA C01 — Grafo Constitucional QUIRA")
    print(f"  ADR-017 (Circuitos) + ADR-018 (NRC)")
    print(f"{'='*65}")

    if dry_run:
        print("\n  [DRY RUN] Solo mostrando Cypher — sin ejecutar en Neo4j\n")

    total_steps = len(ALL_CYPHER_STEPS)
    for i, (nombre, cypher) in enumerate(ALL_CYPHER_STEPS, 1):
        print(f"\n  Paso {i}/{total_steps}: {nombre}")
        if dry_run:
            print(f"  {'─'*55}")
            for line in cypher.strip().split('\n'):
                if line.strip():
                    print(f"  {line}")
        else:
            try:
                with driver.session() as session:
                    result = session.run(cypher)
                    summary = result.consume()
                    counters = summary.counters
                    created_nodes = counters.nodes_created
                    created_rels  = counters.relationships_created
                    set_props     = counters.properties_set
                    print(f"    [OK] nodos_nuevos={created_nodes} · rels_nuevas={created_rels} · props={set_props}")
            except Exception as exc:
                print(f"    [ERROR] {exc}")
                return False

    if not dry_run:
        print(f"\n  [OK] C01 cargado en Neo4j — {total_steps} pasos completados")
    return True


def validate_c01(driver) -> bool:
    """
    Ejecuta las 4 consultas de validación del colega asesor.
    Si las 4 pasan, QUIRA tiene su primer 'explainable governance graph'.
    """
    print(f"\n{'='*65}")
    print(f"  VALIDACIÓN C01 — Las 4 consultas del colega asesor")
    print(f"{'='*65}")

    all_ok = True
    for q in VALIDATION_QUERIES:
        print(f"\n  [{q['id']}] {q['descripcion']}")
        print(f"  Esperado: {q['expect']}")
        try:
            with driver.session() as session:
                results = list(session.run(q["cypher"]))
                if results:
                    print(f"  [OK] {len(results)} resultado(s) — recorrido verificado")
                else:
                    print(f"  [WARN] 0 resultados — el path no existe en el grafo")
                    all_ok = False
        except Exception as exc:
            print(f"  [ERROR] {exc}")
            all_ok = False

    print(f"\n{'='*65}")
    if all_ok:
        print("  RESULTADO: TODOS LOS RECORRIDOS VERIFICADOS")
        print("  QUIRA tiene su primer 'explainable governance graph' operativo.")
        print("  CE_226 → CE_18 → Dom07 → C01 — cadena computable y navegable.")
    else:
        print("  RESULTADO: RECORRIDOS INCOMPLETOS — revisar pasos de carga")
    print(f"{'='*65}\n")
    return all_ok


def print_dry_validation():
    """Muestra las consultas de validación sin ejecutarlas."""
    print(f"\n{'='*65}")
    print(f"  CONSULTAS DE VALIDACIÓN (para ejecutar en Neo4j Browser)")
    print(f"{'='*65}")
    for q in VALIDATION_QUERIES:
        print(f"\n  [{q['id']}] {q['descripcion']}")
        print(f"  {q['cypher']}")
        print(f"  // Esperado: {q['expect']}")
    print(f"\n{'='*65}\n")


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Carga C01 en Neo4j — QUIRA Gov / Dylus Lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python load_c01_neo4j.py               # carga completa + validación
  python load_c01_neo4j.py --dry-run     # muestra Cypher sin ejecutar
  python load_c01_neo4j.py --validate    # solo validación (nodos ya cargados)
  python load_c01_neo4j.py --link-results  # conecta a resultados operacionales

Prerequisito secrets.toml:
  [neo4j]
  uri      = "bolt://localhost:7687"
  user     = "neo4j"
  password = "tu_password"
        """,
    )
    parser.add_argument("--dry-run",      action="store_true", help="Mostrar Cypher sin ejecutar")
    parser.add_argument("--validate",     action="store_true", help="Solo ejecutar consultas de validación")
    parser.add_argument("--link-results", action="store_true", help="Conectar C01 a resultados operacionales existentes")
    args = parser.parse_args()

    if args.dry_run:
        load_c01(driver=None, dry_run=True)
        print_dry_validation()
        return

    driver = _get_neo4j_driver()
    if not driver:
        print("\n[BLOQUEADO] Neo4j no disponible.")
        print("  Para activar:")
        print("  1. Crear instancia Neo4j (local o Aura gratuito)")
        print("  2. Agregar [neo4j] en .streamlit/secrets.toml")
        print("  3. Ejecutar: python load_c01_neo4j.py")
        print("\n  Para ver el Cypher sin ejecutar:")
        print("  python load_c01_neo4j.py --dry-run")
        sys.exit(1)

    try:
        if args.validate:
            ok = validate_c01(driver)
        elif args.link_results:
            print("\n  Conectando C01 a resultados operacionales...")
            with driver.session() as session:
                result = session.run(CYPHER_LINK_RESULTS).single()
                if result:
                    print(f"  [OK] {result['status']}")
                    print(f"       Resultado encontrado: {result['resultado_encontrado']}")
            ok = True
        else:
            ok = load_c01(driver)
            if ok:
                validate_c01(driver)
    finally:
        driver.close()

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
