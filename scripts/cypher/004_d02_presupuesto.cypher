// ============================================================
// Cypher 004 -- d02 Presupuesto & Financiamiento: modelo conceptual
// QUIRA Gov . AuraDB . Dylus Lab (c) 2026
// Fuente: data/d02/catalogo_d02_v1.0.0.yaml + BRN CNO-IV-001/RO-IV-001
// (SHA256 corregidos en la auditoria 2026-07-23, OBS-012).
// d02 se modela por 4 CAPACIDADES + 3 SENALES SAT (no CD-XX, no cadena pura).
// CRITICO (Regla 1/4): las 4 capacidades y las 3 senales se LEEN del Gold
//   Master via scripts/enrich_presupuesto.py -- el agente NUNCA recalcula.
// APLICAR:
//   python scripts/cypher/apply_cypher.py scripts/cypher/004_d02_presupuesto.cypher
// ============================================================

// -- 1. DOMINIO ----------------------------------------------------------------
MERGE (d:Dominio {id: 'd02'})
SET d.nombre = 'Presupuesto y Financiamiento', d.capacidad = 'movilizacion',
    d.catalogo_version = 'CATALOGO_D02_PRESUPUESTO_v1.0.0', d.updated_at = datetime();

// -- 2. NORMAS (MERGE reusa CE si ya existe de d01) -----------------------------
MERGE (n:Norma {sigla: 'CE'})
SET n.nombre = 'Constitución de la República del Ecuador', n.tipo = 'constitucion', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COOTAD'})
SET n.nombre = 'Código Orgánico de Organización Territorial, Autonomía y Descentralización', n.tipo = 'codigo', n.jerarquia = 2, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COOTAD-2026'})
SET n.nombre = 'Ley Reformatoria al COOTAD (sostenibilidad del gasto GAD)', n.tipo = 'ley_reformatoria', n.jerarquia = 2, n.updated_at = datetime();

// -- 3. CNO-IV-001 (cadena juridica, 6 eslabones, SHA corregidos hoy) -----------
MERGE (cno:CNO {id: 'CNO-IV-001'})
SET cno.titulo = 'Regla de Asignacion Minima Prioritaria',
    cno.dominio_normativo = 'finanzas_publicas_municipales', cno.estado = 'vigente',
    cno.validada_por = 'Javo', cno.fecha_validacion = '2026-07-18', cno.updated_at = datetime();
MATCH (cno:CNO {id:'CNO-IV-001'}), (d:Dominio {id:'d02'}) MERGE (cno)-[:OPERA_EN]->(d);

// -- 4. ESLABONES de CNO-IV-001 --------------------------------------------------
MERGE (a:Articulo {id: 'CE_271'})
SET a.norma = 'CE', a.articulo = '271', a.sha256 = 'a76e4e0dea62', a.rol = 'fundamento_constitucional',
    a.sumilla = 'los GAD participarán de las rentas del Estado (base de la corresponsabilidad fiscal)', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_271'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_271'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_192'})
SET a.norma = 'COOTAD', a.articulo = '192', a.sha256 = 'd5d1431a8a38', a.rol = 'fundamento_legal_base',
    a.sumilla = 'Monto total a transferir — 21% de ingresos permanentes + 10% de los no permanentes', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_192'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_192'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(cno);
MERGE (a:Articulo {id: 'COOTAD-2026_198_1'})
SET a.norma = 'COOTAD-2026', a.articulo = '198.1', a.sha256 = 'bbe4c79ad522', a.rol = 'regla',
    a.sumilla = 'Regla de asignación mínima prioritaria — al menos el 70% del presupuesto codificado de egresos no financieros a gasto no permanente de inversión, mantenimiento y reposición de infraestructura, bienes y activos públicos.', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD-2026_198_1'}), (n:Norma {sigla:'COOTAD-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD-2026_198_1'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(cno);
MERGE (a:Articulo {id: 'COOTAD-2026_198_2'})
SET a.norma = 'COOTAD-2026', a.articulo = '198.2', a.sha256 = 'fb68a4b54330', a.rol = 'gasto_computable',
    a.sumilla = 'Determinación del gasto computable para el cumplimiento de la regla', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD-2026_198_2'}), (n:Norma {sigla:'COOTAD-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD-2026_198_2'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(cno);
MERGE (a:Articulo {id: 'COOTAD-2026_198_6'})
SET a.norma = 'COOTAD-2026', a.articulo = '198.6', a.sha256 = '7c01b48dce14', a.rol = 'consecuencia',
    a.sumilla = 'Incumplimiento de la regla → se informa a la Contraloría General del Estado', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD-2026_198_6'}), (n:Norma {sigla:'COOTAD-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD-2026_198_6'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (a)-[:ESLABON_DE {orden: 5}]->(cno);
MERGE (a:Articulo {id: 'COOTAD-2026_Disposición_Transitoria_Primera'})
SET a.norma = 'COOTAD-2026', a.articulo = 'Disposición Transitoria Primera', a.sha256 = 'b5d7a5aab557', a.rol = 'disposicion_transitoria',
    a.sumilla = 'piso inicial del 65% con seguimiento del ente rector a partir del 1-dic-2026, sobre el presupuesto codificado al 31-dic-2026.', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD-2026_Disposición_Transitoria_Primera'}), (n:Norma {sigla:'COOTAD-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD-2026_Disposición_Transitoria_Primera'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (a)-[:ESLABON_DE {orden: 6}]->(cno);

// -- 5. RO-IV-001 + SAT-IV-001 --------------------------------------------------
MERGE (rox:RO {id: 'RO-IV-001'})
SET rox.metrica = 'Pct_Gasto_No_Permanente', rox.frecuencia = 'mensual',
    rox.umbral_transitorio = 65, rox.umbral_pleno = 70, rox.transicion_desde = '2027-01-01',
    rox.descripcion = 'regla de asignacion minima prioritaria', rox.estado = 'vigente',
    rox.updated_at = datetime();
MATCH (rox:RO {id:'RO-IV-001'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (rox)-[:DERIVA_DE]->(cno);
MERGE (s:SAT {id: 'SAT-IV-001'}) SET s.updated_at = datetime();
MATCH (rox:RO {id:'RO-IV-001'}), (s:SAT {id:'SAT-IV-001'}) MERGE (rox)-[:CONSUME]->(s);

// -- 6. CAPACIDADES (4, todas LEIDAS del Gold Master) ----------------------------
MERGE (c:Capacidad {id: 'sostenibilidad'})
SET c.nombre = 'Salud presupuestaria (ISP)',
    c.hoja_gold_master = 'H19_ICS_ISP',
    c.naturaleza = 'se LEE, no se recalcula (Regla 1)',
    c.valor_ref_pct = 58.4,
    c.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (c:Capacidad {id:'sostenibilidad'}) MERGE (d)-[:TIENE_CAPACIDAD]->(c);
MERGE (c:Capacidad {id: 'absorcion'})
SET c.nombre = 'Ejecución presupuestaria (Ti)',
    c.hoja_gold_master = 'H07_S5_FINANCIERO_eSIGEF',
    c.naturaleza = 'se LEE, no se recalcula (Regla 1)',
    c.valor_ref_pct = 6.4,
    c.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (c:Capacidad {id:'absorcion'}) MERGE (d)-[:TIENE_CAPACIDAD]->(c);
MERGE (c:Capacidad {id: 'movilizacion'})
SET c.nombre = 'Captación de fondos externos',
    c.hoja_gold_master = 'H20c_IEF_EFICIENCIA_FINANCIERA',
    c.naturaleza = 'se LEE, no se recalcula (Regla 1)',
    c.valor_ref_usd = 1874500,
    c.n_convenios = 4,
    c.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (c:Capacidad {id:'movilizacion'}) MERGE (d)-[:TIENE_CAPACIDAD]->(c);
MERGE (c:Capacidad {id: 'elegibilidad'})
SET c.nombre = 'Alineación PND + vinculación ODS',
    c.hoja_gold_master = 'H11_S9_AGENDA_GLOBAL_ODS + H11b (consumido de d01, ADR-032)',
    c.naturaleza = 'se LEE, no se recalcula (Regla 1)',
    c.alineacion_pnd_pct = 83,
    c.icods_pct = 87.5,
    c.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (c:Capacidad {id:'elegibilidad'}) MERGE (d)-[:TIENE_CAPACIDAD]->(c);

// -- 7. SENALES SAT (3; solo SAT-IV con cadena normativa verificada) -------------
MERGE (sn:SenalSAT {id: 'SAT-II'})
SET sn.nombre = 'Reforma presupuestaria tardía', sn.hoja_gold_master = 'H22_SAT-II', sn.umbral = 'máx 5% del presupuesto anual',
    sn.estado_2026_07_23 = 'sin_senal', sn.nota = 'COPFP Art.115 citado originalmente era incorrecto (ver enrich_presupuesto.py). Sin cadena normativa verificada todavía.', sn.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (sn:SenalSAT {id:'SAT-II'}) MERGE (d)-[:VIGILA_CON]->(sn);
MERGE (sn:SenalSAT {id: 'SAT-III'})
SET sn.nombre = 'Parálisis presupuestaria', sn.hoja_gold_master = 'H23_SAT-III', sn.umbral = 'ejecución mínima 10%',
    sn.estado_2026_07_23 = 'sin_senal', sn.nota = 'COPFP Art.113 citado originalmente era incorrecto. Sin cadena normativa verificada todavía.', sn.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (sn:SenalSAT {id:'SAT-III'}) MERGE (d)-[:VIGILA_CON]->(sn);
MERGE (sn:SenalSAT {id: 'SAT-IV'})
SET sn.nombre = 'Alerta fiscal · estructura COOTAD', sn.hoja_gold_master = 'H24_SAT-IV', sn.umbral = 'inversión ≥ 65% del presupuesto',
    sn.estado_2026_07_23 = 'sin_senal', sn.nota = 'Único caso con cadena normativa completa: CE Art.271 → COOTAD Art.192 → COOTAD-2026 Art.198.1-198.6 + Disp. Transitoria (34/34 SHA verificados, OBS-012).', sn.updated_at = datetime();
MATCH (d:Dominio {id:'d02'}), (sn:SenalSAT {id:'SAT-IV'}) MERGE (d)-[:VIGILA_CON]->(sn);
MATCH (sn:SenalSAT {id:'SAT-IV'}), (cno:CNO {id:'CNO-IV-001'}) MERGE (sn)-[:FUNDAMENTADA_EN]->(cno);

// -- 8. Reuso cross-dominio: eSIGEF d02 = misma cedula que CD-06 d07 -------------
MERGE (f:Fuente {id: 'eSIGEF_d02'})
SET f.origen = 'Gold Master H07', f.descripcion = 'Cedula presupuestaria - ejecucion',
    f.updated_at = datetime();
MATCH (f:Fuente {id:'eSIGEF_d02'}), (d:Dominio {id:'d02'}) MERGE (f)-[:ALIMENTA]->(d);
MATCH (f:Fuente {id:'eSIGEF_d02'}), (cd:CD {id:'CD-06'}) MERGE (f)-[:MISMA_FUENTE_QUE]->(cd);

// -- 9. MUNICIPIO -----------------------------------------------------------------
MERGE (m:Municipio {id: 'MCR-001'})
SET m.nombre = 'Montecristi', m.rol = 'molde_validacion_empirica', m.updated_at = datetime();
MATCH (m:Municipio {id:'MCR-001'}), (d:Dominio {id:'d02'}) MERGE (m)-[:EVALUADO_EN]->(d);