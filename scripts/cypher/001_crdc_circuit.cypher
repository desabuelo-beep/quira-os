// ============================================================
// Cypher 001 — C-RDC: Circuito de Rendición Anual
// QUIRA Gov · AuraDB · Dylus Lab © 2026
// ADR-026 §C-RDC · Formalización Neo4j
// ============================================================
// Propósito:
//   Materializar el Circuito C-RDC en AuraDB con:
//   1. Nodo :Circuito (definición estructural del circuito)
//   2. Nodos :NodoConvergente (6 dominios de entrada)
//   3. Nodo :NodoProtocolo (Dom09 — punto de convergencia)
//   4. Relaciones CONVERGE_EN con propiedades de umbral
//   5. Evaluación inicial MCR-001 como :EvaluacionCircuito
//
// Topología:
//   Dom07 ──┐
//   Dom08 ──┤
//   Dom02 ──┼──► Dom09 ──► CPCCS (V=0 / V≥70)
//   Dom04 ──┤
//   Dom10 ──┤
//   Dom19 ──┘
//
// DIFERENCIA CON C01:
//   C01: causal (un fallo colapsa el siguiente — PROPAGACIÓN)
//   C-RDC: convergente (todos deben pasar — ACUMULACIÓN)
//
// BLOOMBERG FIREWALL:
//   Los IDs internos (DOM07_TRANS, RES_CRDC_*) nunca se exponen en UI.
//   Solo se expone: nombre, umbral_descripcion, estado, pct_ok.
//
// APLICAR:
//   python scripts/cypher/apply_cypher.py scripts/cypher/001_crdc_circuit.cypher
// ============================================================

// ── 1. NODO CIRCUITO ──────────────────────────────────────────────────────────
MERGE (c:Circuito {id: 'C-RDC'})
SET c.nombre              = 'Convergencia Anual — Rendición de Cuentas',
    c.tipo                = 'CONVERGENTE',
    c.escala_temporal     = 'ANUAL',
    c.arbitro_externo     = 'CPCCS',
    c.resultado_posible   = 'V=0 / V>=70',
    c.activacion_inicio   = 'Mayo',
    c.activacion_ejecucion= 'Agosto',
    c.activacion_cierre   = 'Septiembre',
    c.diferencia_c01      = 'C01 es causal (propagación); C-RDC es convergente (acumulación)',
    c.adr_referencia      = 'ADR-026 §C-RDC',
    c.estado_implementacion= 'activo',
    c.updated_at          = datetime()
RETURN c.id AS circuito_creado;

// ── 2. NODO PROTOCOLO (punto de convergencia) ─────────────────────────────────
MERGE (p:NodoProtocolo {id: 'DOM09_RDC'})
SET p.dominio             = 'Dom09',
    p.nombre              = 'Protocolo de Rendición de Cuentas',
    p.tipo                = 'CONVERGENCIA',
    p.modulo_quira        = 'p17_rdc.py',
    p.output              = 'checklist_pct_ok + evidencias',
    p.arbitro_externo     = 'CPCCS',
    p.umbral_aprobacion   = 70,
    p.escala_temporal     = 'ANUAL',
    p.updated_at          = datetime()
RETURN p.id AS protocolo_creado;

// ── 3. NODOS CONVERGENTES (6 dominios de entrada) ────────────────────────────

// Dom07 — Transparencia y LOTAIP
MERGE (n1:NodoConvergente {id: 'DOM07_TRANS'})
SET n1.dominio             = 'Dom07',
    n1.nombre              = 'Transparencia y LOTAIP',
    n1.indicador_quira     = 'ITAM',
    n1.umbral_descripcion  = 'ITAM >= 80% · 21 arts LOTAIP completos · Art.7r publicado',
    n1.umbral_valor        = 80.0,
    n1.umbral_operador     = 'gte',
    n1.es_critico          = true,
    n1.modulo_quira        = 'p15_transparencia.py',
    n1.updated_at          = datetime();

// Dom08 — Participación y Asambleas
MERGE (n2:NodoConvergente {id: 'DOM08_PART'})
SET n2.dominio             = 'Dom08',
    n2.nombre              = 'Participación Ciudadana y Asambleas',
    n2.indicador_quira     = 'IGP',
    n2.umbral_descripcion  = 'IGP >= 25% · 7/7 asambleas realizadas · PP rendido por parroquia',
    n2.umbral_valor        = 25.0,
    n2.umbral_operador     = 'gte',
    n2.es_critico          = true,
    n2.modulo_quira        = 'p6_participacion.py',
    n2.updated_at          = datetime();

// Dom02+Dom03 — Salud Presupuestaria y Ejecución Fiscal
MERGE (n3:NodoConvergente {id: 'DOM0203_FISCAL'})
SET n3.dominio             = 'Dom02+Dom03',
    n3.nombre              = 'Salud Presupuestaria y Ejecución Fiscal',
    n3.indicador_quira     = 'ISP',
    n3.umbral_descripcion  = 'ISP >= 25% regularizado · ejecución Q2 documentada',
    n3.umbral_valor        = 25.0,
    n3.umbral_operador     = 'gte',
    n3.es_critico          = true,
    n3.modulo_quira        = 'p16_inversion.py',
    n3.updated_at          = datetime();

// Dom04 — Planificación PDOT
MERGE (n4:NodoConvergente {id: 'DOM04_PDOT'})
SET n4.dominio             = 'Dom04',
    n4.nombre              = 'Planificación PDOT y Metas',
    n4.indicador_quira     = 'META_PDOT_ASOCIADA',
    n4.umbral_descripcion  = '4 metas SAT-0 regularizadas · avance PDOT con indicadores',
    n4.umbral_valor        = 4.0,
    n4.umbral_operador     = 'gte',
    n4.es_critico          = false,
    n4.modulo_quira        = 'p8_metas.py',
    n4.updated_at          = datetime();

// Dom10 — Territorio y Cobertura
MERGE (n5:NodoConvergente {id: 'DOM10_TERR'})
SET n5.dominio             = 'Dom10',
    n5.nombre              = 'Cobertura de Servicios Territoriales',
    n5.indicador_quira     = 'EVIDENCIA_EJECUCION',
    n5.umbral_descripcion  = 'Informe de cobertura de agua actualizado y documentado',
    n5.umbral_valor        = null,
    n5.umbral_operador     = 'eq_true',
    n5.es_critico          = false,
    n5.modulo_quira        = 'p10_inversion.py',
    n5.updated_at          = datetime();

// Dom19 — Género y PSG
MERGE (n6:NodoConvergente {id: 'DOM19_PSG'})
SET n6.dominio             = 'Dom19',
    n6.nombre              = 'Presupuesto Sensible al Género',
    n6.indicador_quira     = 'PSG',
    n6.umbral_descripcion  = 'PSG >= 20% documentado y trazable',
    n6.umbral_valor        = 20.0,
    n6.umbral_operador     = 'gte',
    n6.es_critico          = true,
    n6.modulo_quira        = 'p19_genero.py',
    n6.updated_at          = datetime();

// ── 4. RELACIONES CONVERGE_EN ─────────────────────────────────────────────────

MATCH (n1:NodoConvergente {id: 'DOM07_TRANS'}),  (p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (n1)-[r:CONVERGE_EN]->(p)
SET r.orden = 1, r.es_critico = true,  r.peso = 1.0;

MATCH (n2:NodoConvergente {id: 'DOM08_PART'}),   (p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (n2)-[r:CONVERGE_EN]->(p)
SET r.orden = 2, r.es_critico = true,  r.peso = 1.0;

MATCH (n3:NodoConvergente {id: 'DOM0203_FISCAL'}),(p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (n3)-[r:CONVERGE_EN]->(p)
SET r.orden = 3, r.es_critico = true,  r.peso = 1.0;

MATCH (n4:NodoConvergente {id: 'DOM04_PDOT'}),   (p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (n4)-[r:CONVERGE_EN]->(p)
SET r.orden = 4, r.es_critico = false, r.peso = 0.5;

MATCH (n5:NodoConvergente {id: 'DOM10_TERR'}),   (p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (n5)-[r:CONVERGE_EN]->(p)
SET r.orden = 5, r.es_critico = false, r.peso = 0.5;

MATCH (n6:NodoConvergente {id: 'DOM19_PSG'}),    (p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (n6)-[r:CONVERGE_EN]->(p)
SET r.orden = 6, r.es_critico = true,  r.peso = 1.0;

// ── 5. CIRCUITO CONTIENE NODOS ────────────────────────────────────────────────

MATCH (c:Circuito {id: 'C-RDC'}), (p:NodoProtocolo {id: 'DOM09_RDC'})
MERGE (c)-[:TIENE_PROTOCOLO]->(p);

MATCH (c:Circuito {id: 'C-RDC'}), (n:NodoConvergente)
WHERE n.id IN ['DOM07_TRANS','DOM08_PART','DOM0203_FISCAL','DOM04_PDOT','DOM10_TERR','DOM19_PSG']
MERGE (c)-[:TIENE_NODO]->(n);

// ── 6. EVALUACIÓN INICIAL MCR-001 ─────────────────────────────────────────────
// Valores al 2026-06-09 — actualizar periódicamente via app/connectors/neo4j_crdc.py
// ITAM=56.0  IGP=27.98  ISP=14.58  PSG=12.83  (demo_data · Gold Master)

MERGE (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
SET ev.gad_id              = 'MCR-001',
    ev.circuito_id         = 'C-RDC',
    ev.fecha_evaluacion    = date('2026-06-09'),
    ev.nodos_total         = 6,
    ev.nodos_ok            = 2,
    ev.nodos_fallidos      = 3,
    ev.nodos_pendientes    = 1,
    ev.pct_ok              = 33.3,
    ev.estado              = 'BLOQUEADO',
    // Estado: PREPARADO (>=100%) / CON_BRECHAS (67-99%) / BLOQUEADO (<67%)
    ev.estado_desc         = '3 nodos fallan: ISP (14.58% < 25%), PSG (12.83% < 20%), ITAM (56% < 80%)',
    ev.impacto_d02_usd     = 5300000,
    // ISP falla → BDE $5M bloqueado; PSG falla → ONU Mujeres $300K bloqueado
    ev.updated_at          = datetime()
RETURN ev.id AS evaluacion_creada;

// ── 7. RESULTADO NODOS INDIVIDUALES ──────────────────────────────────────────

MERGE (r1:C9ResultadoTerritorial {id: 'RES_CRDC_DOM07_MCR'})
SET r1.valor = 56.0, r1.semaforo = 'ROJO', r1.pasa = false,
    r1.brecha_pp = -24.0, r1.indicador = 'ITAM', r1.dominio = 'Dom07',
    r1.periodo = '2026-06-09', r1.estado_dato = 'confirmado',
    r1.fuente_documental = 'QUIRA ITAM — Portal DPE auditoría junio 2026';

MERGE (r2:C9ResultadoTerritorial {id: 'RES_CRDC_DOM08_MCR'})
SET r2.valor = 27.98, r2.semaforo = 'VERDE', r2.pasa = true,
    r2.brecha_pp = 2.98, r2.indicador = 'IGP', r2.dominio = 'Dom08',
    r2.periodo = '2026-06-09', r2.estado_dato = 'confirmado',
    r2.fuente_documental = 'QUIRA IGP — Gold Master v5.5';

MERGE (r3:C9ResultadoTerritorial {id: 'RES_CRDC_DOM0203_MCR'})
SET r3.valor = 14.58, r3.semaforo = 'ROJO', r3.pasa = false,
    r3.brecha_pp = -10.42, r3.indicador = 'ISP', r3.dominio = 'Dom02/Dom03',
    r3.periodo = '2026-06-09', r3.estado_dato = 'confirmado',
    r3.fuente_documental = 'QUIRA ISP — Gold Master v5.5 · SIGEF';

MERGE (r4:C9ResultadoTerritorial {id: 'RES_CRDC_DOM04_MCR'})
SET r4.valor = null, r4.semaforo = 'PENDIENTE', r4.pasa = false,
    r4.brecha_pp = null, r4.indicador = 'META_PDOT_ASOCIADA', r4.dominio = 'Dom04',
    r4.periodo = '2026-06-09', r4.estado_dato = 'pendiente_validacion',
    r4.fuente_documental = 'D04 pendiente — solicitar avance PDOT a Dirección de Planificación';

MERGE (r5:C9ResultadoTerritorial {id: 'RES_CRDC_DOM10_MCR'})
SET r5.valor = 1.0, r5.semaforo = 'VERDE', r5.pasa = true,
    r5.brecha_pp = null, r5.indicador = 'EVIDENCIA_EJECUCION', r5.dominio = 'Dom10',
    r5.periodo = '2026-06-09', r5.estado_dato = 'confirmado',
    r5.fuente_documental = 'INEC Censo 2022 · PDOT Bicentenario 2023 — informe disponible';

MERGE (r6:C9ResultadoTerritorial {id: 'RES_CRDC_DOM19_MCR'})
SET r6.valor = 12.83, r6.semaforo = 'ROJO', r6.pasa = false,
    r6.brecha_pp = -7.17, r6.indicador = 'PSG', r6.dominio = 'Dom19',
    r6.periodo = '2026-06-09', r6.estado_dato = 'confirmado',
    r6.fuente_documental = 'QUIRA PSG — Gold Master v5.5 · cédula presupuestaria';

// ── 8. RELACIONES EVALUACION → NODOS ────────────────────────────────────────

MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
MATCH (r1:C9ResultadoTerritorial {id: 'RES_CRDC_DOM07_MCR'})
MERGE (ev)-[:EVALUA_NODO {nodo: 'DOM07_TRANS'}]->(r1);

MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
MATCH (r2:C9ResultadoTerritorial {id: 'RES_CRDC_DOM08_MCR'})
MERGE (ev)-[:EVALUA_NODO {nodo: 'DOM08_PART'}]->(r2);

MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
MATCH (r3:C9ResultadoTerritorial {id: 'RES_CRDC_DOM0203_MCR'})
MERGE (ev)-[:EVALUA_NODO {nodo: 'DOM0203_FISCAL'}]->(r3);

MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
MATCH (r4:C9ResultadoTerritorial {id: 'RES_CRDC_DOM04_MCR'})
MERGE (ev)-[:EVALUA_NODO {nodo: 'DOM04_PDOT'}]->(r4);

MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
MATCH (r5:C9ResultadoTerritorial {id: 'RES_CRDC_DOM10_MCR'})
MERGE (ev)-[:EVALUA_NODO {nodo: 'DOM10_TERR'}]->(r5);

MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})
MATCH (r6:C9ResultadoTerritorial {id: 'RES_CRDC_DOM19_MCR'})
MERGE (ev)-[:EVALUA_NODO {nodo: 'DOM19_PSG'}]->(r6);

// ── VERIFICACION ──────────────────────────────────────────────────────────────
// MATCH (c:Circuito {id: 'C-RDC'})-[:TIENE_NODO]->(n:NodoConvergente)
// RETURN c.nombre, n.dominio, n.nombre, n.umbral_descripcion ORDER BY n.id;
//
// MATCH (n:NodoConvergente)-[r:CONVERGE_EN]->(p:NodoProtocolo)
// RETURN n.nombre, r.orden, r.es_critico, p.nombre ORDER BY r.orden;
//
// MATCH (ev:EvaluacionCircuito {id: 'EVAL_CRDC_MCR_2026'})-[:EVALUA_NODO]->(r)
// RETURN r.indicador, r.valor, r.semaforo, r.pasa, r.brecha_pp ORDER BY r.indicador;
