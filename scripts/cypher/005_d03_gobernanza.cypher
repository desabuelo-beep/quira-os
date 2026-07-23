// ============================================================
// Cypher 005 -- d03 Gobernanza del Mandato: modelo conceptual
// QUIRA Gov . AuraDB . Dylus Lab (c) 2026
// Fuente: data/d03/catalogo_d03_v1.0.0.yaml + BRN CNO-III-001/RO-III-001
// (SHA256 verificados 9/9 en la auditoria 2026-07-23, OBS-012).
// d03 se modela por 2 METRICAS (incorporacion=hecho, calidad=indice) + 1 SAT.
// CRITICO (Regla 1/4): ambas metricas se LEEN via enrich_mandato.py -- el
//   agente NUNCA recalcula. Evaluacion ANUAL, no mensual (RO-III-001).
// APLICAR:
//   python scripts/cypher/apply_cypher.py scripts/cypher/005_d03_gobernanza.cypher
// ============================================================

// -- 1. DOMINIO ----------------------------------------------------------------
MERGE (d:Dominio {id: 'd03'})
SET d.nombre = 'Gobernanza del Mandato', d.capacidad = 'fidelidad_democratica',
    d.catalogo_version = 'CATALOGO_D03_GOBERNANZA_MANDATO_v1.0.0', d.updated_at = datetime();

// -- 2. NORMAS (MERGE reusa CE/COOTAD/COPLAFIP si ya existen de d01/d02) --------
MERGE (n:Norma {sigla: 'CE'})
SET n.nombre = 'Constitución de la República del Ecuador', n.tipo = 'constitucion', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COD'})
SET n.nombre = 'Código de la Democracia (Ley Orgánica Electoral)', n.tipo = 'ley_organica', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COOTAD'})
SET n.nombre = 'Código Orgánico de Organización Territorial, Autonomía y Descentralización', n.tipo = 'codigo', n.jerarquia = 2, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COPLAFIP'})
SET n.nombre = 'Código Orgánico de Planificación y Finanzas Públicas', n.tipo = 'codigo', n.jerarquia = 2, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'LOPC'})
SET n.nombre = 'Ley Orgánica de Participación Ciudadana', n.tipo = 'ley_organica', n.jerarquia = 1, n.updated_at = datetime();

// -- 3. CNO-III-001 (cadena juridica, 9 eslabones) -------------------------------
MERGE (cno:CNO {id: 'CNO-III-001'})
SET cno.titulo = 'Traduccion del Mandato Electoral a la Gestion Publica',
    cno.dominio_normativo = 'mandato_electoral_y_representacion', cno.estado = 'vigente',
    cno.validada_por = 'Javo', cno.fecha_validacion = '2026-07-18', cno.updated_at = datetime();
MATCH (cno:CNO {id:'CNO-III-001'}), (d:Dominio {id:'d03'}) MERGE (cno)-[:OPERA_EN]->(d);

// -- 4. ESLABONES de CNO-III-001 --------------------------------------------------
MERGE (a:Articulo {id: 'CE_61'})
SET a.norma = 'CE', a.articulo = '61', a.sha256 = '981cf97fbafe', a.rol = 'fundamento_constitucional',
    a.sumilla = 'derechos de participación — elegir y ser elegidos: origen del mandato popular', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_61'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_61'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(cno);
MERGE (a:Articulo {id: 'COD_97'})
SET a.norma = 'COD', a.articulo = '97', a.sha256 = 'b243e8693685', a.rol = 'compromiso',
    a.sumilla = 'el candidato inscribe su Plan de Trabajo ante el CNE — la palabra empeñada', a.updated_at = datetime();
MATCH (a:Articulo {id:'COD_97'}), (n:Norma {sigla:'COD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COD_97'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_60'})
SET a.norma = 'COOTAD', a.articulo = '60', a.sha256 = '1baac1f8b508', a.rol = 'investidura',
    a.sumilla = 'atribuciones del alcalde: dirige la gestión con que debe cumplir el mandato', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_60'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_60'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(cno);
MERGE (a:Articulo {id: 'COOTAD_58'})
SET a.norma = 'COOTAD', a.articulo = '58', a.sha256 = '240cb67911e9', a.rol = 'investidura_legislativa',
    a.sumilla = 'atribuciones de los concejales: fiscalizan y aprueban los instrumentos', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_58'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_58'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(cno);
MERGE (a:Articulo {id: 'COPLAFIP_41'})
SET a.norma = 'COPLAFIP', a.articulo = '41', a.sha256 = 'e3c9fad328f3', a.rol = 'traduccion',
    a.sumilla = 'el mandato se traduce en el plan de desarrollo (directrices del GAD)', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_41'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_41'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 5}]->(cno);
MERGE (a:Articulo {id: 'COPLAFIP_42'})
SET a.norma = 'COPLAFIP', a.articulo = '42', a.sha256 = '349a6ad45c33', a.rol = 'traduccion_contenido',
    a.sumilla = 'contenidos mínimos del plan de desarrollo', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_42'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_42'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 6}]->(cno);
MERGE (a:Articulo {id: 'LOPC_89'})
SET a.norma = 'LOPC', a.articulo = '89', a.sha256 = '086fc826f996', a.rol = 'rendicion',
    a.sumilla = 'rendición de cuentas: el mandatario responde por el mandato ejercido', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_89'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_89'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 7}]->(cno);
MERGE (a:Articulo {id: 'LOPC_90'})
SET a.norma = 'LOPC', a.articulo = '90', a.sha256 = '547b900b8a8f', a.rol = 'rendicion_sujetos',
    a.sumilla = 'sujetos obligados a rendir cuentas — autoridades electas', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_90'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_90'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 8}]->(cno);
MERGE (a:Articulo {id: 'CE_105'})
SET a.norma = 'CE', a.articulo = '105', a.sha256 = 'f7819a49cbe9', a.rol = 'consecuencia',
    a.sumilla = 'revocatoria del mandato: la consecuencia del incumplimiento ante el electorado', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_105'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_105'}), (cno:CNO {id:'CNO-III-001'}) MERGE (a)-[:ESLABON_DE {orden: 9}]->(cno);

// -- 5. RO-III-001 + SAT-III-001 --------------------------------------------------
MERGE (ro:RO {id: 'RO-III-001'})
SET ro.metrica = 'Pct_Fidelidad_Mandato', ro.frecuencia = 'anual', ro.umbral_alto = 85,
    ro.umbral_medio = 60, ro.descripcion = 'congruencia documental promesa-CNE -> meta PDOT',
    ro.estado = 'vigente', ro.updated_at = datetime();
MATCH (ro:RO {id:'RO-III-001'}), (cno:CNO {id:'CNO-III-001'}) MERGE (ro)-[:DERIVA_DE]->(cno);
MERGE (s:SAT {id: 'SAT-III-001'}) SET s.updated_at = datetime();
MATCH (ro:RO {id:'RO-III-001'}), (s:SAT {id:'SAT-III-001'}) MERGE (ro)-[:CONSUME]->(s);

// -- 6. METRICAS (2: incorporacion=hecho, calidad=indice, ambas LEIDAS) ----------
MERGE (m:Metrica {id: 'incorporacion'})
SET m.nombre = 'Incorporación — ¿la promesa ingresó al plan?',
    m.naturaleza = 'HECHO documental — se cuenta el registro curado, no se recalcula',
    m.hoja_gold_master = 'H03_S1_ELECTORAL_CNE',
    m.valor_ref_pct = 98.7,
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d03'}), (m:Metrica {id:'incorporacion'}) MERGE (d)-[:MIDE_CON]->(m);
MERGE (m:Metrica {id: 'calidad'})
SET m.nombre = 'Calidad (IFE) — ¿con qué nivel de congruencia ingresó?',
    m.naturaleza = 'ÍNDICE del motor — se LEE, no se recalcula (Regla 1)',
    m.hoja_gold_master = 'H16_IFE',
    m.valor_ref_pct = 79.3,
    m.updated_at = datetime();
MATCH (d:Dominio {id:'d03'}), (m:Metrica {id:'calidad'}) MERGE (d)-[:MIDE_CON]->(m);

// -- 7. SENAL SAT (unica: SAT-III-001, cadena normativa verificada) -------------
MERGE (sn:SenalSAT {id: 'SAT-III'})
SET sn.nombre = 'Fidelidad del mandato bajo el piso preventivo',
    sn.hoja_gold_master = 'H85_ALERTS_LOG', sn.estado_2026_07_23 = '✅ CORRECTO',
    sn.updated_at = datetime();
MATCH (d:Dominio {id:'d03'}), (sn:SenalSAT {id:'SAT-III'}) MERGE (d)-[:VIGILA_CON]->(sn);
MATCH (sn:SenalSAT {id:'SAT-III'}), (cno:CNO {id:'CNO-III-001'}) MERGE (sn)-[:FUNDAMENTADA_EN]->(cno);

// -- 8. Reuso cross-dominio: metas PDOT (d01) alimentan la incorporacion (d03) --
MERGE (f:Fuente {id: 'PDOT_metas_d03'})
SET f.origen = 'H03/PDOT (consumido de d01)', f.descripcion = 'metas del plan de desarrollo, reuso',
    f.updated_at = datetime();
MATCH (f:Fuente {id:'PDOT_metas_d03'}), (d:Dominio {id:'d03'}) MERGE (f)-[:ALIMENTA]->(d);
MATCH (f:Fuente {id:'PDOT_metas_d03'}), (dd:Dominio {id:'d01'}) MERGE (f)-[:MISMA_FUENTE_QUE]->(dd);

// -- 9. MUNICIPIO -----------------------------------------------------------------
MERGE (m:Municipio {id: 'MCR-001'})
SET m.nombre = 'Montecristi', m.rol = 'molde_validacion_empirica', m.updated_at = datetime();
MATCH (m:Municipio {id:'MCR-001'}), (d:Dominio {id:'d03'}) MERGE (m)-[:EVALUADO_EN]->(d);