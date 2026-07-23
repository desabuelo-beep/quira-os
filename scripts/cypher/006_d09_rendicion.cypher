// ============================================================
// Cypher 006 -- d09 Rendicion de Cuentas: modelo conceptual
// QUIRA Gov . AuraDB . Dylus Lab (c) 2026
// Fuente: data/d09/catalogo_d09_v1.0.0.yaml + BRN CNO-IX-001/RO-IX-001
// (SHA256 verificados 10/10 en la auditoria 2026-07-23, OBS-012).
// d09 es el dominio mas heterogeneo migrado: 1 METRICA indice (fidelidad
//   narrativa) + 3 HECHOS documentales (brecha CPCCS, serie 3 anios,
//   cumplimiento actual) -- modelados todos como :Metrica (naturaleza
//   distingue INDICE vs HECHO, Regla 7 anti-inflacion del canon).
// CRITICO (Regla 1/4): fidelidad+cpccs se LEEN en vivo del Excel;
//   serie+cumplimiento se LEEN del snapshot persistido (extraccion DOCX,
//   PCD-D09). El agente NUNCA recalcula. Evaluacion ANUAL (RO-IX-001).
// APLICAR:
//   python scripts/cypher/apply_cypher.py scripts/cypher/006_d09_rendicion.cypher
// ============================================================

// -- 1. DOMINIO ----------------------------------------------------------------
MERGE (d:Dominio {id: 'd09'})
SET d.nombre = 'Rendición de Cuentas', d.capacidad = 'transparencia_y_control_social',
    d.catalogo_version = 'CATALOGO_D09_RENDICION_CUENTAS_v1.0.0', d.updated_at = datetime();

// -- 2. NORMAS (MERGE reusa CE/LOPC si ya existen de d01/d03; RES-CPCCS es nueva) --
MERGE (n:Norma {sigla: 'CE'})
SET n.nombre = 'Constitución de la República del Ecuador', n.tipo = 'constitucion', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'LOPC'})
SET n.nombre = 'Ley Orgánica de Participación Ciudadana', n.tipo = 'ley_organica', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'RES-CPCCS-RC-2026'})
SET n.nombre = 'Resolución CPCCS-PLE-SG-004-O-2026-0030 — Rendición de Cuentas', n.tipo = 'resolucion', n.jerarquia = 3, n.updated_at = datetime();

// -- 3. CNO-IX-001 (cadena juridica, 10 eslabones) -------------------------------
MERGE (cno:CNO {id: 'CNO-IX-001'})
SET cno.titulo = 'Obligación de Rendición de Cuentas del GAD',
    cno.dominio_normativo = 'participacion_y_control_social', cno.estado = 'vigente',
    cno.validada_por = 'Javo', cno.fecha_validacion = '2026-07-20', cno.updated_at = datetime();
MATCH (cno:CNO {id:'CNO-IX-001'}), (d:Dominio {id:'d09'}) MERGE (cno)-[:OPERA_EN]->(d);

// -- 4. ESLABONES de CNO-IX-001 --------------------------------------------------
MERGE (a:Articulo {id: 'CE_100'})
SET a.norma = 'CE', a.articulo = '100', a.sha256 = '8282b964440e', a.rol = 'fundamento_constitucional',
    a.sumilla = 'instancias de participación en todos los niveles de gobierno', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_100'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_100'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(cno);
MERGE (a:Articulo {id: 'CE_208'})
SET a.norma = 'CE', a.articulo = '208', a.sha256 = '8c269ae98217', a.rol = 'fundamento_control',
    a.sumilla = 'deberes y atribuciones del Consejo de Participación Ciudadana y Control Social', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_208'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_208'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(cno);
MERGE (a:Articulo {id: 'LOPC_89'})
SET a.norma = 'LOPC', a.articulo = '89', a.sha256 = '086fc826f996', a.rol = 'definicion',
    a.sumilla = 'definición: la rendición de cuentas como proceso participativo y obligatorio', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_89'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_89'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(cno);
MERGE (a:Articulo {id: 'LOPC_90'})
SET a.norma = 'LOPC', a.articulo = '90', a.sha256 = '547b900b8a8f', a.rol = 'sujetos_obligados',
    a.sumilla = 'autoridades del Estado, electas o de libre remoción, están obligadas a rendir cuentas', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_90'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_90'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(cno);
MERGE (a:Articulo {id: 'LOPC_91'})
SET a.norma = 'LOPC', a.articulo = '91', a.sha256 = '79733cc71e4f', a.rol = 'objetivos',
    a.sumilla = 'objetivos de la rendición de cuentas', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_91'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_91'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 5}]->(cno);
MERGE (a:Articulo {id: 'LOPC_93'})
SET a.norma = 'LOPC', a.articulo = '93', a.sha256 = '871a7da338fe', a.rol = 'alcance_programatico',
    a.sumilla = 'nivel programático y operativo sobre el que se rinde cuentas', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_93'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_93'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 6}]->(cno);
MERGE (a:Articulo {id: 'RES-CPCCS-RC-2026_10'})
SET a.norma = 'RES-CPCCS-RC-2026', a.articulo = '10', a.sha256 = '835f120780a9', a.rol = 'contenido_minimo',
    a.sumilla = 'contenido mínimo obligatorio del informe de rendición de cuentas', a.updated_at = datetime();
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_10'}), (n:Norma {sigla:'RES-CPCCS-RC-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_10'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 7}]->(cno);
MERGE (a:Articulo {id: 'RES-CPCCS-RC-2026_13'})
SET a.norma = 'RES-CPCCS-RC-2026', a.articulo = '13', a.sha256 = 'c2456d489297', a.rol = 'sujeto_gad',
    a.sumilla = 'reglas específicas para los Gobiernos Autónomos Descentralizados', a.updated_at = datetime();
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_13'}), (n:Norma {sigla:'RES-CPCCS-RC-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_13'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 8}]->(cno);
MERGE (a:Articulo {id: 'RES-CPCCS-RC-2026_15'})
SET a.norma = 'RES-CPCCS-RC-2026', a.articulo = '15', a.sha256 = 'f2648b154be4', a.rol = 'deliberacion_publica',
    a.sumilla = 'la deliberación pública como espacio obligatorio del proceso', a.updated_at = datetime();
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_15'}), (n:Norma {sigla:'RES-CPCCS-RC-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_15'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 9}]->(cno);
MERGE (a:Articulo {id: 'RES-CPCCS-RC-2026_21'})
SET a.norma = 'RES-CPCCS-RC-2026', a.articulo = '21', a.sha256 = '9c5c442d147a', a.rol = 'consecuencia',
    a.sumilla = 'entrega de informes incumplidos de períodos fiscales anteriores', a.updated_at = datetime();
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_21'}), (n:Norma {sigla:'RES-CPCCS-RC-2026'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'RES-CPCCS-RC-2026_21'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (a)-[:ESLABON_DE {orden: 10}]->(cno);

// -- 5. RO-IX-001 + SAT-IX-001 -----------------------------------------------------
MERGE (ro:RO {id: 'RO-IX-001'})
SET ro.metrica = 'Pct_Cumplimiento_Rendicion', ro.frecuencia = 'anual', ro.umbral = 100,
    ro.descripcion = 'verificación documental: informe presentado + contenido mínimo + deliberación pública',
    ro.estado = 'vigente', ro.updated_at = datetime();
MATCH (ro:RO {id:'RO-IX-001'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (ro)-[:DERIVA_DE]->(cno);
MERGE (s:SAT {id: 'SAT-IX-001'}) SET s.updated_at = datetime();
MATCH (ro:RO {id:'RO-IX-001'}), (s:SAT {id:'SAT-IX-001'}) MERGE (ro)-[:CONSUME]->(s);

// -- 6. METRICAS (1 indice + 3 hechos documentales, todas LEIDAS) ----------------
MERGE (m:Metrica {id: 'fidelidad_narrativa'})
SET m.nombre = 'Fidelidad Narrativa (discurso oficial ↔ evidencia)',
    m.naturaleza = 'ÍNDICE del motor — evaluación experta trazable (discurso↔evidencia), no cómputo automático',
    m.hoja_gold_master = 'H34b_MFN_FIDELIDAD_NARRATIVA',
    m.valor_ref_pct = 91.0,
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d09'}), (m:Metrica {id:'fidelidad_narrativa'}) MERGE (d)-[:MIDE_CON]->(m);
MERGE (m:Metrica {id: 'cpccs_brecha_compromisos'})
SET m.nombre = 'Brecha de Compromisos CPCCS',
    m.naturaleza = 'HECHO — hoy sin evidencia (los informes no publican tabla de compromisos), canon devuelve honesto, no 0% falso',
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d09'}), (m:Metrica {id:'cpccs_brecha_compromisos'}) MERGE (d)-[:MIDE_CON]->(m);
MERGE (m:Metrica {id: 'serie_rendiciones'})
SET m.nombre = 'Serie de Rendiciones (2023-2025)',
    m.naturaleza = 'HECHO — extraído de los informes DOCX oficiales del CPCCS por año, persistido en snapshot',
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d09'}), (m:Metrica {id:'serie_rendiciones'}) MERGE (d)-[:MIDE_CON]->(m);
MERGE (m:Metrica {id: 'cumplimiento_actual'})
SET m.nombre = 'Cumplimiento del Ejercicio Vigente (2025)',
    m.naturaleza = 'HECHO — 21 componentes del informe 2025, misma fuente DOCX que la serie',
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d09'}), (m:Metrica {id:'cumplimiento_actual'}) MERGE (d)-[:MIDE_CON]->(m);
MERGE (m:Metrica {id: 'aportes_ciudadanos'})
SET m.nombre = 'Trazabilidad de Aportes y Compromisos Ciudadanos',
    m.naturaleza = 'HECHO — cruce semiautomático H10c (aportes) × POA (ejecución), evaluación experta trazable, como IF_n',
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d09'}), (m:Metrica {id:'aportes_ciudadanos'}) MERGE (d)-[:MIDE_CON]->(m);

// -- 7. SENAL SAT (unica: SAT-IX-001, cadena normativa verificada) -------------
MERGE (sn:SenalSAT {id: 'SAT-IX'})
SET sn.nombre = 'Brecha de compromisos CPCCS sin evidencia publicada',
    sn.id_interno_gold_master = 'H24b_SAT-V_ALERTA_CPCCS', sn.updated_at = datetime();
MATCH (d:Dominio {id:'d09'}), (sn:SenalSAT {id:'SAT-IX'}) MERGE (d)-[:VIGILA_CON]->(sn);
MATCH (sn:SenalSAT {id:'SAT-IX'}), (cno:CNO {id:'CNO-IX-001'}) MERGE (sn)-[:FUNDAMENTADA_EN]->(cno);

// -- 8. FUENTES (2 Excel en vivo + 2 documentales, sin reuso cross-dominio hoy) --
MERGE (fu:Fuente {id: 'H34b_fidelidad'})
SET fu.origen = 'Gold Master H34b_MFN_FIDELIDAD_NARRATIVA', fu.tipo = 'excel_formula', fu.updated_at = datetime();
MATCH (fu:Fuente {id:'H34b_fidelidad'}), (d:Dominio {id:'d09'}) MERGE (fu)-[:ALIMENTA]->(d);
MERGE (fu:Fuente {id: 'H31_cpccs'})
SET fu.origen = 'Gold Master H31_REPORTE_CPCCS', fu.tipo = 'excel_formula', fu.updated_at = datetime();
MATCH (fu:Fuente {id:'H31_cpccs'}), (d:Dominio {id:'d09'}) MERGE (fu)-[:ALIMENTA]->(d);
MERGE (fu:Fuente {id: 'informes_rdc_docx'})
SET fu.origen = '3 informes DOCX oficiales de Rendición de Cuentas (2023-2025)', fu.tipo = 'documento_oficial', fu.updated_at = datetime();
MATCH (fu:Fuente {id:'informes_rdc_docx'}), (d:Dominio {id:'d09'}) MERGE (fu)-[:ALIMENTA]->(d);
MERGE (fu:Fuente {id: 'H10c_aportes'})
SET fu.origen = 'Gold Master H10c_RDC_APORTES (108 demandas verificadas) × POA oficial (extracción PDF)', fu.tipo = 'excel_mas_documento', fu.updated_at = datetime();
MATCH (fu:Fuente {id:'H10c_aportes'}), (d:Dominio {id:'d09'}) MERGE (fu)-[:ALIMENTA]->(d);
MERGE (fu:Fuente {id: 'corpus_rdc_supabase'})
SET fu.origen = 'scripts/ingest_rdc_corpus.py — 114 chunks (2023=20·2024=38·2025=56), tipo_documento=informe_rendicion', fu.tipo = 'corpus_semantico', fu.updated_at = datetime();
MATCH (fu:Fuente {id:'corpus_rdc_supabase'}), (d:Dominio {id:'d09'}) MERGE (fu)-[:ALIMENTA]->(d);

// -- 9. MUNICIPIO -----------------------------------------------------------------
MERGE (m:Municipio {id: 'MCR-001'})
SET m.nombre = 'Montecristi', m.rol = 'molde_validacion_empirica', m.updated_at = datetime();
MATCH (m:Municipio {id:'MCR-001'}), (d:Dominio {id:'d09'}) MERGE (m)-[:EVALUADO_EN]->(d);