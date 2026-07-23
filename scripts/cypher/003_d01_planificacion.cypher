// ============================================================
// Cypher 003 — d01 Planificacion Estrategica: modelo conceptual
// QUIRA Gov . AuraDB . Dylus Lab (c) 2026
// Fuente: BRN CNO-I-001 + RO-I-001/002 (SHA reales) + PCD-D01.
// d01 se modela por CADENA DE ARTICULACION (no por CD-XX, eso es d07).
// CRITICO (Regla 1/4): IPE y Cobertura se LEEN del Gold Master (H16b,
//   deriva de H12!B33 INMUTABLE) -- el agente NUNCA recalcula el motor.
//
// CORREGIDO 2026-07-23 (Javo, retroactivo): este script se generaba desde
// datos inline en un script Python, sin YAML intermedio -- rompia el
// principio "Neo4j deriva del catalogo, nunca al reves" (si respetado en
// d07). Fuente unica REAL ahora: data/d01/catalogo_d01_v1.0.0.yaml.
// Los valores de este .cypher NO cambiaron (verificados identicos al YAML),
// no se re-aplico a Neo4j -- solo se corrige la fuente de verdad hacia
// adelante. Regenerar desde el YAML si algo cambia (Regla 9).
// APLICAR:
//   python scripts/cypher/apply_cypher.py scripts/cypher/003_d01_planificacion.cypher
// ============================================================

// -- 1. DOMINIO --------------------------------------------------------------
MERGE (d:Dominio {id: 'd01'})
SET d.nombre = 'Planificacion Estrategica', d.capacidad = 'trayectoria',
    d.metrica_ref = 'IPE', d.macroeje = 'Direccion',
    d.pcd = 'PCD-D01', d.updated_at = datetime();

// -- 2. NORMAS (reutiliza nodos si ya existen; MERGE por sigla) -----------------
MERGE (n:Norma {sigla: 'CE'})
SET n.nombre = 'Constitución de la República del Ecuador', n.tipo = 'constitucion', n.jerarquia = 100, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COPLAFIP'})
SET n.nombre = 'Código Orgánico de Planificación y Finanzas Públicas', n.tipo = 'codigo', n.jerarquia = 90, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COOTAD'})
SET n.nombre = 'Código Orgánico de Organización Territorial, Autonomía y Descentralización', n.tipo = 'codigo', n.jerarquia = 90, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'LOSNCP'})
SET n.nombre = 'Ley Orgánica del Sistema Nacional de Contratación Pública', n.tipo = 'ley_organica', n.jerarquia = 95, n.updated_at = datetime();

// -- 3. CNO (Cadena Normativa Operativa -- puro Derecho, ADR-038) ---------------
MERGE (cno:CNO {id: 'CNO-I-001'})
SET cno.titulo = 'Articulacion de la Planificacion con el Presupuesto y la Contratacion',
    cno.dominio_normativo = 'planificacion_del_desarrollo', cno.estado = 'vigente',
    cno.validada_por = 'Javo', cno.fecha_validacion = '2026-07-20', cno.updated_at = datetime();
MATCH (cno:CNO {id:'CNO-I-001'}), (d:Dominio {id:'d01'}) MERGE (cno)-[:OPERA_EN]->(d);

// -- 4. ESLABONES de la cadena (9 articulos con SHA real) ----------------------
MERGE (a:Articulo {id: 'CE_241'})
SET a.norma = 'CE', a.articulo = '241', a.sha256 = 'da13d3789caa', a.rol = 'fundamento_constitucional',
    a.sumilla = 'la planificación garantizará el ordenamiento territorial y será obligatoria', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_241'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_241'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(cno);
MERGE (a:Articulo {id: 'CE_280'})
SET a.norma = 'CE', a.articulo = '280', a.sha256 = '5d25f2ee7268', a.rol = 'articulacion_nacional',
    a.sumilla = 'el Plan Nacional de Desarrollo como instrumento al que se sujeta la planificación', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_280'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_280'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(cno);
MERGE (a:Articulo {id: 'COPLAFIP_12'})
SET a.norma = 'COPLAFIP', a.articulo = '12', a.sha256 = '916241847fcb', a.rol = 'competencia',
    a.sumilla = 'la planificación del desarrollo y el OT es competencia del GAD', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_12'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_12'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(cno);
MERGE (a:Articulo {id: 'COPLAFIP_44'})
SET a.norma = 'COPLAFIP', a.articulo = '44', a.sha256 = 'd8f56a1d3206', a.rol = 'ordenamiento_territorial',
    a.sumilla = 'disposiciones generales sobre los planes de OT de los GAD', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_44'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_44'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_233'})
SET a.norma = 'COOTAD', a.articulo = '233', a.sha256 = '96e3b77f48fc', a.rol = 'programacion_operativa_plazo',
    a.sumilla = 'plazo: programación operativa antes del 10 de septiembre', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_233'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_233'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 5}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_234'})
SET a.norma = 'COOTAD', a.articulo = '234', a.sha256 = '6837117fda64', a.rol = 'programacion_operativa_contenido',
    a.sumilla = 'cada POA debe contener las metas del plan de desarrollo', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_234'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_234'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 6}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_215'})
SET a.norma = 'COOTAD', a.articulo = '215', a.sha256 = '60f89aebd7b3', a.rol = 'sujecion_presupuestaria',
    a.sumilla = 'el presupuesto del GAD se ajusta a los planes de desarrollo', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_215'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_215'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 7}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_245'})
SET a.norma = 'COOTAD', a.articulo = '245', a.sha256 = '78317417e719', a.rol = 'aprobacion',
    a.sumilla = 'aprobación del presupuesto por el legislativo del GAD', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_245'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_245'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 8}]->(cno);
MERGE (a:Articulo {id: 'LOSNCP_22'})
SET a.norma = 'LOSNCP', a.articulo = '22', a.sha256 = '054779c8e813', a.rol = 'contratacion',
    a.sumilla = 'el PAC se formula conforme al plan y al presupuesto', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOSNCP_22'}), (n:Norma {sigla:'LOSNCP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOSNCP_22'}), (cno:CNO {id:'CNO-I-001'}) MERGE (a)-[:ESLABON_DE {orden: 9}]->(cno);

// -- 5. RO (Reglas Operativas) + SAT -------------------------------------------
MERGE (ro:RO {id: 'RO-I-001'})
SET ro.metrica = 'Pct_Metas_Con_Programacion', ro.umbral = 100, ro.frecuencia = 'anual',
    ro.descripcion = 'articulación plan → programación operativa', ro.criterios = ['meta_con_proyecto', 'dotacion_asignada', 'responsable_definido'],
    ro.estado = 'vigente', ro.updated_at = datetime();
MATCH (ro:RO {id:'RO-I-001'}), (cno:CNO {id:'CNO-I-001'}) MERGE (ro)-[:DERIVA_DE]->(cno);
MERGE (s:SAT {id: 'SAT-I-001'}) SET s.updated_at = datetime();
MATCH (ro:RO {id:'RO-I-001'}), (s:SAT {id:'SAT-I-001'}) MERGE (ro)-[:CONSUME]->(s);
MERGE (ro:RO {id: 'RO-I-002'})
SET ro.metrica = 'Pct_Coherencia_Programacion_Contratacion', ro.umbral = 100, ro.frecuencia = 'anual',
    ro.descripcion = 'articulación programación operativa → contratación', ro.criterios = ['linea_en_pac', 'partida_coincidente', 'publicacion_portal'],
    ro.estado = 'vigente', ro.updated_at = datetime();
MATCH (ro:RO {id:'RO-I-002'}), (cno:CNO {id:'CNO-I-001'}) MERGE (ro)-[:DERIVA_DE]->(cno);
MERGE (s:SAT {id: 'SAT-I-002'}) SET s.updated_at = datetime();
MATCH (ro:RO {id:'RO-I-002'}), (s:SAT {id:'SAT-I-002'}) MERGE (ro)-[:CONSUME]->(s);

// -- 6. FUENTES documentales (lo que los AGENTES extraen) ----------------------
MERGE (f:Fuente {id: 'PDOT'})
SET f.origen = 'web_GAD', f.descripcion = 'Plan de Desarrollo y Ordenamiento Territorial', f.updated_at = datetime();
MATCH (f:Fuente {id:'PDOT'}), (d:Dominio {id:'d01'}) MERGE (f)-[:ALIMENTA]->(d);
MERGE (f:Fuente {id: 'POA'})
SET f.origen = 'web_GAD', f.descripcion = 'Plan Operativo Anual', f.updated_at = datetime();
MATCH (f:Fuente {id:'POA'}), (d:Dominio {id:'d01'}) MERGE (f)-[:ALIMENTA]->(d);
MERGE (f:Fuente {id: 'PAC'})
SET f.origen = 'portal_SERCOP / web_GAD', f.descripcion = 'Plan Anual de Contratación', f.updated_at = datetime();
MATCH (f:Fuente {id:'PAC'}), (d:Dominio {id:'d01'}) MERGE (f)-[:ALIMENTA]->(d);
MERGE (f:Fuente {id: 'Presupuesto'})
SET f.origen = 'portal_transparencia_DPE', f.descripcion = 'Cédula presupuestaria', f.updated_at = datetime();
MATCH (f:Fuente {id:'Presupuesto'}), (d:Dominio {id:'d01'}) MERGE (f)-[:ALIMENTA]->(d);
MATCH (f:Fuente {id:'Presupuesto'}), (cd:CD {id:'CD-06'}) MERGE (f)-[:MISMA_FUENTE_QUE]->(cd);
MERGE (f:Fuente {id: 'SERCOP'})
SET f.origen = 'portal_compras_publicas', f.descripcion = 'Contratación real ejecutada', f.updated_at = datetime();
MATCH (f:Fuente {id:'SERCOP'}), (d:Dominio {id:'d01'}) MERGE (f)-[:ALIMENTA]->(d);
MERGE (f:Fuente {id: 'eSIGEF'})
SET f.origen = 'transparencia / informe', f.descripcion = 'Devengado de ejecución', f.updated_at = datetime();
MATCH (f:Fuente {id:'eSIGEF'}), (d:Dominio {id:'d01'}) MERGE (f)-[:ALIMENTA]->(d);
MATCH (x:Fuente {id:'PDOT'}), (y:Fuente {id:'POA'}) MERGE (x)-[:ARTICULA_CON]->(y);
MATCH (x:Fuente {id:'POA'}), (y:Fuente {id:'PAC'}) MERGE (x)-[:ARTICULA_CON]->(y);
MATCH (x:Fuente {id:'PAC'}), (y:Fuente {id:'SERCOP'}) MERGE (x)-[:ARTICULA_CON]->(y);
MATCH (x:Fuente {id:'POA'}), (y:Fuente {id:'Presupuesto'}) MERGE (x)-[:ARTICULA_CON]->(y);

// -- 7. METRICAS (LEIDAS del Gold Master -- Regla 1/4, NO recalcular) -----------
MERGE (m:Metrica {id: 'IPE'})
SET m.nombre = 'Índice de Planificación Estratégica (ejecutado)', m.valor_ref = 95.6, m.hoja_gold_master = 'H16b',
    m.deriva_de = 'H12!B33', m.naturaleza = 'INMUTABLE — se lee del Gold Master, el agente NUNCA lo calcula', m.updated_at = datetime();
MATCH (m:Metrica {id:'IPE'}), (d:Dominio {id:'d01'}) MERGE (d)-[:MIDE_CON]->(m);
MERGE (m:Metrica {id: 'Cobertura_Metas_POA'})
SET m.nombre = 'Cobertura de metas del PDOT en el POA', m.valor_ref = 96.0, m.hoja_gold_master = 'H16b',
    m.deriva_de = 'H12!B33', m.naturaleza = 'INMUTABLE — se lee del Gold Master', m.updated_at = datetime();
MATCH (m:Metrica {id:'Cobertura_Metas_POA'}), (d:Dominio {id:'d01'}) MERGE (d)-[:MIDE_CON]->(m);

// -- 8. MUNICIPIO (Montecristi = molde) ----------------------------------------
MERGE (mun:Municipio {id: 'MCR-001'})
SET mun.nombre = 'Montecristi', mun.rol = 'molde_validacion_empirica', mun.updated_at = datetime();
MATCH (mun:Municipio {id:'MCR-001'}), (d:Dominio {id:'d01'}) MERGE (mun)-[:EVALUADO_EN]->(d);