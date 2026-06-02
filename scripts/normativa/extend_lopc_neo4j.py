#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extend_lopc_neo4j.py — Sprint LOPC Dom08-Core: 15 ACKs + relaciones cross-domain
QUIRA Gov · Dylus Lab · 2026-06-02

PROPÓSITO:
  Extender el grafo constitucional C01 con los ACKs núcleo de la LOPC
  (Ley Orgánica de Participación Ciudadana) que crean mecanismos obligatorios
  para los GADs Municipales.

  Cuando este script termina exitosamente, Neo4j puede responder:
    "¿Dom08 es un hub de legitimación democrática?"
    → Centralidad medible: grado de Dom08 vs. todos los dominios
    → Cruce de dominios: cuántos dominios independientes toca LOPC via Dom08

  Hipótesis a validar (ADR-019 PROPUESTO):
    CE_1 → CE_95 → Dom08 → Dom02, Dom03, Dom04, Dom07, Dom09
    Si Dom08 tiene grado > cualquier otro dominio → Escenario B confirmado
    Si CE_1 tiene betweenness > CE_226 → Escenario C confirmado

  QLEP Block procesado:
    15 artículos núcleo: LOPC 1, 4, 60, 65, 69, 71, 74, 77, 79, 80, 85, 87, 90, 95, 101
    sha256 verificados vía Supabase normativa_corpus 2026-06-02

  Fuentes:
    ADR-019: hipótesis Dominios de Legitimación Democrática
    QLEP-v1.0: protocolo de atomización
    Corpus: 94 chunks LOPC (Arts. 1-101)

USO:
  python scripts/normativa/extend_lopc_neo4j.py             # carga + valida
  python scripts/normativa/extend_lopc_neo4j.py --dry-run   # solo muestra Cypher
  python scripts/normativa/extend_lopc_neo4j.py --validate  # solo queries

Bloomberg Model:
  Script INTERNO — Dylus Lab / QUIRA Operaciones.
  Los node IDs NUNCA se exponen en UI pública.
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
# CYPHER: LOPC DOM08-CORE — 15 ACKs NÚCLEO
# ══════════════════════════════════════════════════════════════════════════════

# ─ Paso L1: Dom09 seed + dominios adicionales ────────────────────────────────
CYPHER_DOMINIOS_EXT = """
// Dom09 — Rendición de Cuentas: nodo seed (antes del DCO completo)
// Dom02, Dom03: nodos placeholder para relaciones cross-domain
MERGE (d09:Dominio {id: 'Dom09'})
SET d09.nombre    = 'Rendición de Cuentas & Control Social',
    d09.dco_activo = false,
    d09.chs_rol   = 'PENDIENTE_DCO'

MERGE (d02:Dominio {id: 'Dom02'})
SET d02.nombre    = 'Presupuesto, Inversión & Financiamiento',
    d02.dco_activo = false

MERGE (d03:Dominio {id: 'Dom03'})
SET d03.nombre    = 'Contratación Pública & Obras',
    d03.dco_activo = false
"""

# ─ Paso L2: 15 ACK nodes de LOPC Dom08-Core ──────────────────────────────────
CYPHER_LOPC_NODES = """
// 15 ACKs núcleo LOPC — sha256 verificados Supabase normativa_corpus 2026-06-02
// QLEP-v1.0 · Sprint LOPC-Dom08-Core

MERGE (a:ACK {ack_id: 'LOPC_1'})
SET a.nombre = 'Objeto de la LOPC — instancias y mecanismos de participación ciudadana',
    a.tipo = 'definicion', a.es_nrc = false,
    a.norma_sigla = 'LOPC', a.articulo = '1', a.jerarquia = 1,
    a.sha256_corpus = '9712d64cd4dd087433b2c4fb7a1c0149f41fb0fd5bf77ff89820c3141de89e5e'

MERGE (b:ACK {ack_id: 'LOPC_4'})
SET b.nombre = 'Principios rectores de la participación ciudadana — 13 principios LOPC',
    b.tipo = 'principio', b.es_nrc = false,
    b.norma_sigla = 'LOPC', b.articulo = '4', b.jerarquia = 1,
    b.sha256_corpus = '46789b7a0ce4a059362c413e482a0eef7834085d16da4d96b95072c307e4ebe1'

MERGE (c:ACK {ack_id: 'LOPC_60'})
SET c.nombre = 'Funciones de las asambleas locales de participación ciudadana',
    c.tipo = 'obligacion', c.es_nrc = false,
    c.norma_sigla = 'LOPC', c.articulo = '60', c.jerarquia = 1,
    c.sha256_corpus = '2617f6cb8077352a4e96e1b2f2668229dc0e815dac24c98bce8e899d4a836b15'

MERGE (d:ACK {ack_id: 'LOPC_65'})
SET d.nombre = 'Instancias de participación ciudadana local — convocatoria obligatoria mínimo 3 veces al año',
    d.tipo = 'obligacion', d.es_nrc = false,
    d.norma_sigla = 'LOPC', d.articulo = '65', d.jerarquia = 1,
    d.sha256_corpus = '01cbf6da62224e6af00e3f81a6e7f311e3e27d2f7064955a1ee852f031a6622c'

MERGE (e:ACK {ack_id: 'LOPC_69'})
SET e.nombre = 'Articulación del presupuesto participativo con los planes de desarrollo (nexo Dom08-Dom04)',
    e.tipo = 'procedimiento', e.es_nrc = false,
    e.norma_sigla = 'LOPC', e.articulo = '69', e.jerarquia = 1,
    e.sha256_corpus = 'e7417b5d4ddf589e31ecef61fa33ed054b37bc22242a86ac9c960cb021597198'

MERGE (f:ACK {ack_id: 'LOPC_71'})
SET f.nombre = 'Obligatoriedad del presupuesto participativo — sanción explícita por incumplimiento',
    f.tipo = 'obligacion', f.es_nrc = false,
    f.norma_sigla = 'LOPC', f.articulo = '71', f.jerarquia = 1,
    f.sha256_corpus = '117ee8fc9d6b751538f6d83c8a694a58a1aec1c906e8fe93fa89dce78d25d8f1'

MERGE (g:ACK {ack_id: 'LOPC_74'})
SET g.nombre = 'Audiencias públicas — convocatoria obligatoria y plazo 30 días',
    g.tipo = 'procedimiento', g.es_nrc = false,
    g.norma_sigla = 'LOPC', g.articulo = '74', g.jerarquia = 1,
    g.sha256_corpus = '255d189959c72e7d81374565dc1b6a775d8e85172283ba25e0379322c9fefb85'

MERGE (h:ACK {ack_id: 'LOPC_77'})
SET h.nombre = 'Silla vacía en sesiones del GAD — voz y voto ciudadano, nulidad por incumplimiento',
    h.tipo = 'procedimiento', h.es_nrc = false,
    h.norma_sigla = 'LOPC', h.articulo = '77', h.jerarquia = 1,
    h.sha256_corpus = 'bcbec672000a38ee564f2bcb350ec943ae70a66135dce6ec6d1adde291b69d7b'

MERGE (i:ACK {ack_id: 'LOPC_79'})
SET i.nombre = 'Observatorios ciudadanos — mecanismo de monitoreo independiente',
    i.tipo = 'definicion', i.es_nrc = false,
    i.norma_sigla = 'LOPC', i.articulo = '79', i.jerarquia = 1,
    i.sha256_corpus = '87b587756d87ef0e55d36bd6a9cd12c2668cc357a49d37a8b919b53fe6218491'

MERGE (j:ACK {ack_id: 'LOPC_80'})
SET j.nombre = 'Consejos consultivos — mecanismos de asesoramiento ciudadano',
    j.tipo = 'definicion', j.es_nrc = false,
    j.norma_sigla = 'LOPC', j.articulo = '80', j.jerarquia = 1,
    j.sha256_corpus = '5849d42ad3a87aabd843ac94878a396951d818eeedc2cb69667693bcffbbeeed'

MERGE (k:ACK {ack_id: 'LOPC_85'})
SET k.nombre = 'Veedurías ciudadanas — modalidades y facultades de control social',
    k.tipo = 'procedimiento', k.es_nrc = false,
    k.norma_sigla = 'LOPC', k.articulo = '85', k.jerarquia = 1,
    k.sha256_corpus = '5cd57fe5d318f29d96d681ea49f069c311d0f16f560062100c741c3d3b9b546a'

MERGE (l:ACK {ack_id: 'LOPC_87'})
SET l.nombre = 'Obligación del GAD de garantizar acceso de información a veedurías ciudadanas',
    l.tipo = 'obligacion', l.es_nrc = false,
    l.norma_sigla = 'LOPC', l.articulo = '87', l.jerarquia = 1,
    l.sha256_corpus = '98dc74b0a9a904d966c5a8c7d1ffd6538afd72781d798a0966dcd2525a66ad0c'

MERGE (m:ACK {ack_id: 'LOPC_90'})
SET m.nombre = 'Sujetos obligados a rendir cuentas — autoridades electas y funcionarios',
    m.tipo = 'obligacion', m.es_nrc = false,
    m.norma_sigla = 'LOPC', m.articulo = '90', m.jerarquia = 1,
    m.sha256_corpus = '547b900b8a8f28271aa0084a24f8a89e1395791011b19d251984ff39e0c8f739'

MERGE (n:ACK {ack_id: 'LOPC_95'})
SET n.nombre = 'Periodicidad de la rendición de cuentas — una vez por año y al final de gestión',
    n.tipo = 'plazo', n.es_nrc = false,
    n.norma_sigla = 'LOPC', n.articulo = '95', n.jerarquia = 1,
    n.sha256_corpus = '88db254371a24a0935384644bcb442babc785a464f8822d1a961a8dde2a67e17'

MERGE (o:ACK {ack_id: 'LOPC_101'})
SET o.nombre = 'Democracia electrónica — obligación del GAD de implementar mecanismos digitales de participación',
    o.tipo = 'obligacion', o.es_nrc = false,
    o.norma_sigla = 'LOPC', o.articulo = '101', o.jerarquia = 1,
    o.sha256_corpus = 'b7cd10e123ff9e548a9c1231c7fbd87f40f1d1222543ddc5fa26a523afad0120'
"""

# ─ Paso L3: LOPC → Dom08 (MATCH + MERGE — patrón correcto para nodos existentes)
CYPHER_LOPC_DOM08 = """
// LOPC instrumenta Dom08 — 10 ACKs → Participación Ciudadana
// Patrón: MATCH nodos existentes + MERGE solo la relación (evita duplicados)
MATCH (d08:Dominio {id:'Dom08'})
MATCH (a1:ACK  {ack_id:'LOPC_1'})
MATCH (a4:ACK  {ack_id:'LOPC_4'})
MATCH (a60:ACK {ack_id:'LOPC_60'})
MATCH (a65:ACK {ack_id:'LOPC_65'})
MATCH (a74:ACK {ack_id:'LOPC_74'})
MATCH (a77:ACK {ack_id:'LOPC_77'})
MATCH (a79:ACK {ack_id:'LOPC_79'})
MATCH (a85:ACK {ack_id:'LOPC_85'})
MATCH (a87:ACK {ack_id:'LOPC_87'})
MATCH (a101:ACK{ack_id:'LOPC_101'})
MERGE (a1)  -[:INSTRUMENTA {capa:'C1_definicion',   nota:'Objeto LOPC — define mecanismos de deliberación pública'}]->(d08)
MERGE (a4)  -[:INSTRUMENTA {capa:'C1_principio',    nota:'13 principios: paridad género, interculturalidad, gratuidad'}]->(d08)
MERGE (a60) -[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Asambleas locales: exigir servicios, proponer planes, control social'}]->(d08)
MERGE (a65) -[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Alcalde convoca instancias locales — mínimo 3 veces al año'}]->(d08)
MERGE (a74) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Audiencias públicas — ciudadanía exige información y decisiones'}]->(d08)
MERGE (a77) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Silla vacía — voz y voto en Concejo, nulidad si se incumple'}]->(d08)
MERGE (a79) -[:INSTRUMENTA {capa:'C2_definicion',   nota:'Observatorios — vigilancia técnica independiente de políticas públicas'}]->(d08)
MERGE (a85) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Veedurías — control social sobre recursos e instituciones públicas'}]->(d08)
MERGE (a87) -[:INSTRUMENTA {capa:'C2_obligacion',   nota:'GAD obligado a facilitar información a veedurías'}]->(d08)
MERGE (a101)-[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Portal web + mecanismos digitales obligatorios de participación'}]->(d08)
"""

# ─ Paso L4: LOPC → Dom09 (MATCH + MERGE) ─────────────────────────────────────
CYPHER_LOPC_DOM09 = """
// LOPC instrumenta Dom09 — Dom08 genera la demanda, Dom09 la satisface
MATCH (d09:Dominio {id:'Dom09'})
MATCH (a60:ACK {ack_id:'LOPC_60'})
MATCH (a90:ACK {ack_id:'LOPC_90'})
MATCH (a95:ACK {ack_id:'LOPC_95'})
MERGE (a60)-[:INSTRUMENTA {capa:'C2_obligacion', nota:'Asambleas organizan rendición de cuentas de autoridades electas'}]->(d09)
MERGE (a90)-[:INSTRUMENTA {capa:'C2_obligacion', nota:'Define sujetos obligados — Alcalde + funcionarios deben rendir cuentas'}]->(d09)
MERGE (a95)-[:INSTRUMENTA {capa:'C2_plazo',      nota:'Timer anual verificable — 12 meses máximo entre rendiciones'}]->(d09)
"""

# ─ Paso L5: LOPC → Dom02 + Dom04 (MATCH + MERGE) ─────────────────────────────
CYPHER_LOPC_DOM02_DOM04 = """
// LOPC nexo Dom08 ↔ Dom02 (presupuesto participativo) + Dom04 (PDOT)
MATCH (d02:Dominio {id:'Dom02'})
MATCH (d04:Dominio {id:'Dom04'})
MATCH (a65:ACK  {ack_id:'LOPC_65'})
MATCH (a69:ACK  {ack_id:'LOPC_69'})
MATCH (a71:ACK  {ack_id:'LOPC_71'})
MATCH (a101:ACK {ack_id:'LOPC_101'})
MERGE (a69) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Presupuesto participativo articulado al PDOT — nexo Dom02-Dom04-Dom08'}]->(d02)
MERGE (a71) -[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Presupuesto participativo obligatorio con sanción política y administrativa'}]->(d02)
MERGE (a65) -[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Consejos locales planificación: mín. 30% ciudadanía — Dom08 entra al PDOT'}]->(d04)
MERGE (a69) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'PDOT debe elaborarse de abajo hacia arriba — participación territorial'}]->(d04)
MERGE (a101)-[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Portal: planes y presupuestos disponibles para participación informada'}]->(d04)
"""

# ─ Paso L6: LOPC → Dom03 + Dom07 (MATCH + MERGE) ─────────────────────────────
CYPHER_LOPC_DOM03_DOM07 = """
// LOPC nexo Dom08 ↔ Dom03 (contratación) + Dom07 (transparencia)
MATCH (d03:Dominio {id:'Dom03'})
MATCH (d07:Dominio {id:'Dom07'})
MATCH (a74:ACK  {ack_id:'LOPC_74'})
MATCH (a77:ACK  {ack_id:'LOPC_77'})
MATCH (a85:ACK  {ack_id:'LOPC_85'})
MATCH (a87:ACK  {ack_id:'LOPC_87'})
MATCH (a101:ACK {ack_id:'LOPC_101'})
MERGE (a77) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Silla vacía en sesiones donde se aprueban contratos y ordenanzas'}]->(d03)
MERGE (a85) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Veedurías pueden vigilar procesos de contratación pública'}]->(d03)
MERGE (a101)-[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Portal: procesos contratación, licitación y compras públicos'}]->(d03)
MERGE (a74) -[:INSTRUMENTA {capa:'C2_procedimiento',nota:'Audiencias públicas para solicitar información de gestión — refuerza Dom07'}]->(d07)
MERGE (a87) -[:INSTRUMENTA {capa:'C2_obligacion',   nota:'Obligación de facilitar información a veedurías — nexo Dom08-Dom07'}]->(d07)
"""

# ─ Paso L7: Dom08 GENERA Dom09 (MATCH + MERGE) ────────────────────────────────
CYPHER_DOM08_ALIMENTA_DOM09 = """
// Dom08 (Participación) genera la demanda de Dom09 (Rendición de Cuentas)
MATCH (d08:Dominio {id:'Dom08'})
MATCH (d09:Dominio {id:'Dom09'})
MERGE (d08)-[:GENERA {
    circuito: 'C04_PENDIENTE',
    mecanismo: 'CE_95 → LOPC_90',
    texto: 'La participación ciudadana (Dom08) genera la obligación de rendición de cuentas (Dom09). Sin Dom08 activo, Dom09 carece de demanda ciudadana que lo active.',
    acks: 'CE_95, LOPC_65, LOPC_90, LOPC_95'
}]->(d09)
"""

# ── Todos los pasos en orden ──────────────────────────────────────────────────
ALL_LOPC_STEPS = [
    ("Dom09 seed + Dom02/Dom03 placeholders",                      CYPHER_DOMINIOS_EXT),
    ("15 ACKs LOPC Dom08-Core (sha256 verificados)",               CYPHER_LOPC_NODES),
    ("LOPC → Dom08: 10 relaciones INSTRUMENTA",                    CYPHER_LOPC_DOM08),
    ("LOPC → Dom09: rendición de cuentas (3 relaciones)",          CYPHER_LOPC_DOM09),
    ("LOPC → Dom02 + Dom04: presupuesto+planificación (5 rels)",   CYPHER_LOPC_DOM02_DOM04),
    ("LOPC → Dom03 + Dom07: contratación+transparencia (5 rels)",  CYPHER_LOPC_DOM03_DOM07),
    ("Dom08 -[GENERA]-> Dom09: causalidad participación→rendición", CYPHER_DOM08_ALIMENTA_DOM09),
]


# ══════════════════════════════════════════════════════════════════════════════
# QUERIES DE VALIDACIÓN — Hipótesis ADR-019
# ══════════════════════════════════════════════════════════════════════════════

VALIDATION_QUERIES = [
    {
        "id": "QL1_lopc_count",
        "descripcion": "LOPC cargada — 15 ACKs en grafo",
        "cypher": "MATCH (a:ACK {norma_sigla:'LOPC'}) RETURN COUNT(a) AS total_lopc_acks",
        "expect": "15 nodos LOPC",
    },
    {
        "id": "QL2_domain_degrees",
        "descripcion": "Grado de cada dominio — ¿Dom08 domina? (hipótesis B)",
        "cypher": (
            "MATCH (d:Dominio) "
            "OPTIONAL MATCH (n)-[r]-(d) "
            "RETURN d.id AS dominio, d.nombre AS nombre, COUNT(r) AS degree "
            "ORDER BY degree DESC"
        ),
        "expect": "Dom08 con mayor degree — confirmaría Escenario B ADR-019",
    },
    {
        "id": "QL3_lopc_cross_domain",
        "descripcion": "¿Cuántos dominios únicos toca LOPC? (prueba hipótesis hub)",
        "cypher": (
            "MATCH (a:ACK {norma_sigla:'LOPC'})-[r]-(d:Dominio) "
            "RETURN COLLECT(DISTINCT d.id) AS dominios_tocados, "
            "COUNT(DISTINCT d.id) AS total_dominios"
        ),
        "expect": "7+ dominios únicos — LOPC es ley de arquitectura, no temática",
    },
    {
        "id": "QL4_dom08_neighborhood",
        "descripcion": "Vecindad de Dom08 — qué dominios conecta directamente",
        "cypher": (
            "MATCH (d08:Dominio {id:'Dom08'})-[r]-(x) "
            "WHERE x:Dominio OR x:ACK "
            "RETURN labels(x)[0] AS tipo, "
            "CASE WHEN x:Dominio THEN x.id ELSE x.ack_id END AS id, "
            "type(r) AS relacion "
            "ORDER BY tipo, id"
        ),
        "expect": "Dom08 conectado a Dom02, Dom03, Dom04, Dom07, Dom09 y múltiples ACKs",
    },
    {
        "id": "QL5_sovereignty_chain",
        "descripcion": "Cadena soberanía: CE_1 → CE_95 → Dom08 → dominios instrumentados",
        "cypher": (
            "MATCH (ce1:ACK {ack_id:'CE_1'})-[:CONSTITUYE]->(ce95:ACK {ack_id:'CE_95'}) "
            "-[:FUNDA]->(d08:Dominio {id:'Dom08'}) "
            "OPTIONAL MATCH (a:ACK {norma_sigla:'LOPC'})-[:INSTRUMENTA]->(d:Dominio) "
            "RETURN ce1.ack_id AS apex, ce95.ack_id AS nrc, d08.id AS hub, "
            "COLLECT(DISTINCT d.id) AS dominios_via_lopc, "
            "COUNT(DISTINCT d.id) AS total_dominios"
        ),
        "expect": "CE_1 → CE_95 → Dom08 + Dom08 instrumenta 6+ dominios via LOPC",
    },
    {
        "id": "QL6_silla_vacia_impact",
        "descripcion": "Silla vacía (LOPC_77) — impacto cross-domain (Dom08 + Dom03)",
        "cypher": (
            "MATCH (a:ACK {ack_id:'LOPC_77'})-[r:INSTRUMENTA]->(d:Dominio) "
            "RETURN a.ack_id AS ack, a.nombre AS mecanismo, "
            "COLLECT(d.id) AS dominios_afectados, a.sha256_corpus AS sha256"
        ),
        "expect": "LOPC_77 instrumenta Dom08 + Dom03 — nulidad de sesión confirma poder real",
    },
    {
        "id": "QL7_dom08_genera_dom09",
        "descripcion": "Dom08 genera Dom09 — causalidad participación→rendición verificada",
        "cypher": (
            "MATCH (d08:Dominio {id:'Dom08'})-[r:GENERA]->(d09:Dominio {id:'Dom09'}) "
            "RETURN d08.id AS origen, type(r) AS relacion, d09.id AS destino, r.mecanismo AS mecanismo"
        ),
        "expect": "1 result: Dom08-[GENERA]->Dom09 via CE_95+LOPC_90",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# CONEXIÓN NEO4J (reutiliza config de load_c01_neo4j.py)
# ══════════════════════════════════════════════════════════════════════════════

def _get_neo4j_config() -> dict:
    try:
        import toml
        secrets_path = ROOT / ".streamlit" / "secrets.toml"
        if not secrets_path.exists():
            return {}
        secrets = toml.load(str(secrets_path))
        cfg = secrets.get("neo4j", {})
        return cfg if cfg.get("password") else {}
    except Exception:
        return {}


def _get_driver():
    cfg = _get_neo4j_config()
    if not cfg:
        return None
    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("[ERROR] pip install neo4j")
        return None
    try:
        driver = GraphDatabase.driver(cfg["uri"], auth=(cfg["user"], cfg["password"]))
        driver.verify_connectivity()
        print(f"[OK] Neo4j: {cfg['uri']}")
        return driver
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return None


def _session(driver):
    cfg = _get_neo4j_config()
    return driver.session(database=cfg.get("database", "neo4j"))


# ══════════════════════════════════════════════════════════════════════════════
# CARGA Y VALIDACIÓN
# ══════════════════════════════════════════════════════════════════════════════

def load_lopc(driver, dry_run: bool = False) -> bool:
    print(f"\n{'='*65}")
    print(f"  SPRINT LOPC DOM08-CORE — Grafo Constitucional QUIRA")
    print(f"  15 ACKs · 7 dominios · Hipótesis ADR-019")
    print(f"{'='*65}")

    if dry_run:
        print("\n  [DRY RUN] Solo mostrando Cypher\n")

    for i, (nombre, cypher) in enumerate(ALL_LOPC_STEPS, 1):
        print(f"\n  Paso L{i}/{len(ALL_LOPC_STEPS)}: {nombre}")
        if dry_run:
            for line in cypher.strip().split('\n'):
                if line.strip():
                    print(f"  {line}")
        else:
            try:
                with _session(driver) as session:
                    result = session.run(cypher)
                    s = result.consume().counters
                    print(f"    [OK] nodos={s.nodes_created} · rels={s.relationships_created} · props={s.properties_set}")
            except Exception as exc:
                print(f"    [ERROR] {exc}")
                return False

    if not dry_run:
        print(f"\n  [OK] LOPC cargada — {len(ALL_LOPC_STEPS)} pasos completados")
    return True


def validate_lopc(driver) -> bool:
    print(f"\n{'='*65}")
    print(f"  VALIDACIÓN ADR-019 — Hipótesis Dom08 como Hub")
    print(f"{'='*65}")

    all_ok = True
    for q in VALIDATION_QUERIES:
        print(f"\n  [{q['id']}] {q['descripcion']}")
        print(f"  Esperado: {q['expect']}")
        try:
            with _session(driver) as session:
                results = list(session.run(q["cypher"]))
                if results:
                    print(f"  [OK] {len(results)} resultado(s):")
                    for r in results[:5]:
                        print(f"       {dict(r)}")
                    if len(results) > 5:
                        print(f"       ... ({len(results) - 5} más)")
                else:
                    print(f"  [WARN] 0 resultados")
                    all_ok = False
        except Exception as exc:
            print(f"  [ERROR] {exc}")
            all_ok = False

    print(f"\n{'='*65}")
    if all_ok:
        print("  RESULTADO: LOPC cargada y hipótesis inicialmente observable.")
        print("  Ver QL2 (degrees) y QL3 (dominios LOPC) para evaluar Escenario B/C.")
    else:
        print("  RESULTADO: revisar errores anteriores")
    print(f"{'='*65}\n")
    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Sprint LOPC Dom08-Core — QUIRA Gov")
    parser.add_argument("--dry-run",  action="store_true", help="Mostrar Cypher sin ejecutar")
    parser.add_argument("--validate", action="store_true", help="Solo ejecutar queries de validación")
    args = parser.parse_args()

    if args.dry_run:
        load_lopc(driver=None, dry_run=True)
        return

    driver = _get_driver()
    if not driver:
        print("\n[BLOQUEADO] Neo4j no disponible — revisar .streamlit/secrets.toml")
        sys.exit(1)

    try:
        if args.validate:
            validate_lopc(driver)
        else:
            ok = load_lopc(driver)
            if ok:
                validate_lopc(driver)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
