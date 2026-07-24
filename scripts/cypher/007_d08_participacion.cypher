// ============================================================
// Cypher 007 -- d08 Participación Ciudadana: modelo conceptual
// QUIRA Gov . AuraDB . Dylus Lab (c) 2026
// Fuente: docs/brn/CNO-VIII-000..007 + RO-VIII-001..003 + data/d08/catalogo_d08.
// Familia jerárquica (aporte de Javo, 15 anios GAD): marco -> Sistema -> Asamblea
//   (organo ciudadano autonomo) -> Consejo -> mecanismos. 3 DIMENSIONES:
//   integridad normativa (RO-1) + vitalidad democratica (RO-2, disenio) +
//   efectividad/incidencia (RO-3, disenio).
// SAT (OBS-016): las SAT NO son 1:1 con mecanismos -- son senales del Gold Master
//   (SAT-0..VIII por dimension TGI). Solo SAT-VI (Desvio PP, D4) es de participacion,
//   consumida por RO-VIII-003. Las que falten se crean en fase 2. La verificabilidad
//   por instancia (RO-VIII-001) NO es SAT: es estado de evidencia.
// IGP: indicador madre, se LEE; su MODELO DE CALCULO se reconstruye en fase 2 (OBS-015).
// APLICAR: python scripts/cypher/apply_cypher.py scripts/cypher/007_d08_participacion.cypher
// ============================================================

// -- 1. DOMINIO ----------------------------------------------------------------
MERGE (d:Dominio {id: 'd08'})
SET d.nombre = 'Participación Ciudadana', d.macroeje = 3,
    d.indicador_madre = 'IGP', d.catalogo_version = 'CATALOGO_D08_PARTICIPACION_CIUDADANA_v1.0.0',
    d.frontera = 'participacion (d08) != control social/RDC (d09) -- aportes de instancias, no del informe RDC',
    d.updated_at = datetime();

// -- 2. NORMAS (MERGE reusa las que ya existen de otros dominios) --------------
MERGE (n:Norma {sigla: 'CE'})
SET n.nombre = 'Constitución de la República del Ecuador', n.tipo = 'constitucion', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'LOPC'})
SET n.nombre = 'Ley Orgánica de Participación Ciudadana', n.tipo = 'ley_organica', n.jerarquia = 1, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COOTAD'})
SET n.nombre = 'Código Orgánico de Organización Territorial, Autonomía y Descentralización', n.tipo = 'codigo', n.jerarquia = 2, n.updated_at = datetime();
MERGE (n:Norma {sigla: 'COPLAFIP'})
SET n.nombre = 'Código Orgánico de Planificación y Finanzas Públicas', n.tipo = 'codigo', n.jerarquia = 2, n.updated_at = datetime();

// -- 3. FAMILIA CNO-VIII (000 marco arquitectonico + 001-007 operativas) -------
MERGE (c:CNO {id: 'CNO-VIII-000'})
SET c.titulo = 'Marco Constitucional del Sistema de Participación Ciudadana', c.tipo = 'arquitectonica', c.mecanismo = 'marco',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-000'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'CE_95'})
SET a.norma = 'CE', a.articulo = '95', a.sha256 = 'd7053ac933f4',
    a.rol = 'fundamento_principio', a.sumilla = 'participación protagónica en las decisiones, planificación y gestión de lo público — el principio matriz', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_95'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_95'}), (c:CNO {id:'CNO-VIII-000'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'CE_61'})
SET a.norma = 'CE', a.articulo = '61', a.sha256 = '981cf97fbafe',
    a.rol = 'fundamento_derechos', a.sumilla = 'derechos de participación: participar en asuntos públicos, ser consultado, fiscalizar los actos del poder', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_61'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_61'}), (c:CNO {id:'CNO-VIII-000'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'CE_100'})
SET a.norma = 'CE', a.articulo = '100', a.sha256 = '8282b964440e',
    a.rol = 'fundamento_instancias', a.sumilla = 'instancias de participación en todos los niveles de gobierno y sus mecanismos', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_100'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_100'}), (c:CNO {id:'CNO-VIII-000'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-001'})
SET c.titulo = 'Sistema Cantonal de Participación', c.tipo = 'operativa', c.mecanismo = 'sistema_cantonal',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-001'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'COOTAD_304'})
SET a.norma = 'COOTAD', a.articulo = '304', a.sha256 = 'a1ccfa62c16f',
    a.rol = 'sistema_obligatorio', a.sumilla = 'el GAD conformará un sistema de participación ciudadana regulado por acto normativo — estructura obligatoria', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_304'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_304'}), (c:CNO {id:'CNO-VIII-001'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'LOPC_64'})
SET a.norma = 'LOPC', a.articulo = '64', a.sha256 = '9490de910d1a',
    a.rol = 'instancia_local', a.sumilla = 'instancia de participación ciudadana a nivel local: elaborar planes y políticas entre gobierno y ciudadanía', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_64'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_64'}), (c:CNO {id:'CNO-VIII-001'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'LOPC_65'})
SET a.norma = 'LOPC', a.articulo = '65', a.sha256 = 'a1302c84530e',
    a.rol = 'estructura_composicion', a.sumilla = 'composición y convocatoria de las instancias de participación local: autoridades electas + régimen dependiente + representantes de la sociedad — la estructura LEGAL que la ordenanza municipal replica', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_65'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_65'}), (c:CNO {id:'CNO-VIII-001'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);
MERGE (a:Articulo {id: 'COOTAD_312'})
SET a.norma = 'COOTAD', a.articulo = '312', a.sha256 = '2ed574a48921',
    a.rol = 'consecuencia_sancion', a.sumilla = 'sanción: el incumplimiento de las disposiciones de participación ciudadana genera responsabilidades y sanciones a las autoridades del GAD', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_312'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_312'}), (c:CNO {id:'CNO-VIII-001'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-002'})
SET c.titulo = 'Asamblea Ciudadana Cantonal', c.tipo = 'operativa', c.mecanismo = 'asamblea_ciudadana',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-002'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'LOPC_56'})
SET a.norma = 'LOPC', a.articulo = '56', a.sha256 = '53a22c333f1b',
    a.rol = 'asamblea_local', a.sumilla = 'asambleas locales: espacio de deliberación pública para fortalecer la interlocución ciudadana con el gobierno', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_56'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_56'}), (c:CNO {id:'CNO-VIII-002'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'LOPC_57'})
SET a.norma = 'LOPC', a.articulo = '57', a.sha256 = '0366370fb8ac',
    a.rol = 'composicion_diversidad', a.sumilla = 'composición de las asambleas locales: pluralidad, identidades territoriales, equidad de género y generacional', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_57'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_57'}), (c:CNO {id:'CNO-VIII-002'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'LOPC_58'})
SET a.norma = 'LOPC', a.articulo = '58', a.sha256 = 'ce1103859360',
    a.rol = 'autonomia_estatutos', a.sumilla = 'funcionamiento de las asambleas: democracia, equidad, alternabilidad — SE REGULAN POR SUS PROPIOS ESTATUTOS (fundamento legal verificado de la autonomía de la ACC ante el GAD)', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_58'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_58'}), (c:CNO {id:'CNO-VIII-002'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);
MERGE (a:Articulo {id: 'LOPC_61'})
SET a.norma = 'LOPC', a.articulo = '61', a.sha256 = 'd1d0e67b3aec',
    a.rol = 'interrelacion_cantonal', a.sumilla = 'interrelación entre asambleas de diversos niveles territoriales (cantonales, provinciales, regionales)', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_61'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_61'}), (c:CNO {id:'CNO-VIII-002'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(c);
MERGE (a:Articulo {id: 'COOTAD_306'})
SET a.norma = 'COOTAD', a.articulo = '306', a.sha256 = '349beae574ee',
    a.rol = 'unidad_basica_territorial', a.sumilla = 'barrios y parroquias urbanas como unidades básicas de participación — consejos barriales como órganos de representación comunitaria articulados al sistema', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_306'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_306'}), (c:CNO {id:'CNO-VIII-002'}) MERGE (a)-[:ESLABON_DE {orden: 5}]->(c);
MERGE (a:Articulo {id: 'COOTAD_307'})
SET a.norma = 'COOTAD', a.articulo = '307', a.sha256 = '600dc6063347',
    a.rol = 'funciones_representacion', a.sumilla = 'funciones de los consejos barriales y parroquiales: representar a la ciudadanía del territorio y ejercer control social', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_307'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_307'}), (c:CNO {id:'CNO-VIII-002'}) MERGE (a)-[:ESLABON_DE {orden: 6}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-003'})
SET c.titulo = 'Consejo de Planificación', c.tipo = 'operativa', c.mecanismo = 'consejo_planificacion',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-003'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'COPLAFIP_13'})
SET a.norma = 'COPLAFIP', a.articulo = '13', a.sha256 = '6e5fe9c9ec8c',
    a.rol = 'planificacion_participativa', a.sumilla = 'planificación participativa: mecanismos de participación para la formulación de planes y políticas', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_13'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_13'}), (c:CNO {id:'CNO-VIII-003'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'COPLAFIP_28'})
SET a.norma = 'COPLAFIP', a.articulo = '28', a.sha256 = 'b987e68379f6',
    a.rol = 'conformacion', a.sumilla = 'conformación del Consejo de Planificación del GAD — órgano de participación en la planificación', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_28'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_28'}), (c:CNO {id:'CNO-VIII-003'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'COPLAFIP_29'})
SET a.norma = 'COPLAFIP', a.articulo = '29', a.sha256 = '52cd154eaa35',
    a.rol = 'formalizacion_resolucion', a.sumilla = 'el Consejo emite RESOLUCIÓN favorable sobre las prioridades estratégicas — formalización que SÍ consta en la evidencia', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_29'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_29'}), (c:CNO {id:'CNO-VIII-003'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);
MERGE (a:Articulo {id: 'COPLAFIP_46'})
SET a.norma = 'COPLAFIP', a.articulo = '46', a.sha256 = '653cf4898187',
    a.rol = 'formulacion_pdot', a.sumilla = 'formulación participativa del PDOT — el Consejo participa en el plan de desarrollo y ordenamiento territorial', a.updated_at = datetime();
MATCH (a:Articulo {id:'COPLAFIP_46'}), (n:Norma {sigla:'COPLAFIP'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COPLAFIP_46'}), (c:CNO {id:'CNO-VIII-003'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-004'})
SET c.titulo = 'Audiencia Pública', c.tipo = 'operativa', c.mecanismo = 'audiencia_publica',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-004'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'LOPC_73'})
SET a.norma = 'LOPC', a.articulo = '73', a.sha256 = 'a1596df98b10',
    a.rol = 'habilitacion', a.sumilla = 'audiencia pública: instancia habilitada por la autoridad responsable — exige acto de habilitación', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_73'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_73'}), (c:CNO {id:'CNO-VIII-004'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'LOPC_74'})
SET a.norma = 'LOPC', a.articulo = '74', a.sha256 = '29970f83790d',
    a.rol = 'convocatoria', a.sumilla = 'convocatoria a audiencias públicas: la solicitud ciudadana debe ser atendida por la autoridad', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_74'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_74'}), (c:CNO {id:'CNO-VIII-004'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'LOPC_75'})
SET a.norma = 'LOPC', a.articulo = '75', a.sha256 = '6c126fb90c51',
    a.rol = 'formalizacion_resolucion', a.sumilla = 'RESOLUCIONES de las audiencias públicas: la autoridad resuelve el mismo día o en 10 días hábiles — la formalización exigible (★)', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_75'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_75'}), (c:CNO {id:'CNO-VIII-004'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);
MERGE (a:Articulo {id: 'COOTAD_60'})
SET a.norma = 'COOTAD', a.articulo = '60', a.sha256 = 'a83bf2157a76',
    a.rol = 'habilitacion_delegacion', a.sumilla = 'el alcalde delega atribuciones y preside directa o por delegado: si no preside la audiencia, el acto de delegación debe existir (★)', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_60'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_60'}), (c:CNO {id:'CNO-VIII-004'}) MERGE (a)-[:ESLABON_DE {orden: 4}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-005'})
SET c.titulo = 'Presupuesto Participativo', c.tipo = 'operativa', c.mecanismo = 'presupuesto_participativo',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-005'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'LOPC_67'})
SET a.norma = 'LOPC', a.articulo = '67', a.sha256 = '71d0907bfb13',
    a.rol = 'definicion', a.sumilla = 'presupuesto participativo: proceso por el cual la ciudadanía contribuye a la toma de decisiones sobre los recursos', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_67'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_67'}), (c:CNO {id:'CNO-VIII-005'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'LOPC_71'})
SET a.norma = 'LOPC', a.articulo = '71', a.sha256 = 'f8cbbe8dccbd',
    a.rol = 'obligatoriedad', a.sumilla = 'obligatoriedad del presupuesto participativo articulado a los planes de desarrollo, en convocatoria abierta', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_71'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_71'}), (c:CNO {id:'CNO-VIII-005'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'COOTAD_238'})
SET a.norma = 'COOTAD', a.articulo = '238', a.sha256 = 'f682cd88ba15',
    a.rol = 'priorizacion_gasto_vinculante', a.sumilla = 'las prioridades de gasto se establecen desde las unidades básicas de participación — carácter vinculante del PP en el GAD', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_238'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_238'}), (c:CNO {id:'CNO-VIII-005'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-006'})
SET c.titulo = 'Cabildo Popular', c.tipo = 'operativa', c.mecanismo = 'cabildo_popular',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-006'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'CE_100'})
SET a.norma = 'CE', a.articulo = '100', a.sha256 = '8282b964440e',
    a.rol = 'fundamento_mecanismos', a.sumilla = 'los mecanismos de participación en los niveles de gobierno incluyen los cabildos populares', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_100'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_100'}), (c:CNO {id:'CNO-VIII-006'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'LOPC_76'})
SET a.norma = 'LOPC', a.articulo = '76', a.sha256 = '14fefd6d0ece',
    a.rol = 'definicion', a.sumilla = 'cabildo popular: instancia cantonal de sesión pública, convocatoria abierta, para discutir asuntos específicos', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_76'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_76'}), (c:CNO {id:'CNO-VIII-006'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);

MERGE (c:CNO {id: 'CNO-VIII-007'})
SET c.titulo = 'Silla Vacía', c.tipo = 'operativa', c.mecanismo = 'silla_vacia',
    c.familia = 'CNO-VIII', c.estado = 'propuesta', c.updated_at = datetime();
MATCH (c:CNO {id:'CNO-VIII-007'}), (d:Dominio {id:'d08'}) MERGE (c)-[:OPERA_EN]->(d);
MERGE (a:Articulo {id: 'CE_101'})
SET a.norma = 'CE', a.articulo = '101', a.sha256 = '86ec8e96fbf1',
    a.rol = 'fundamento_constitucional', a.sumilla = 'sesiones públicas del GAD con silla vacía para un representante ciudadano según el tema', a.updated_at = datetime();
MATCH (a:Articulo {id:'CE_101'}), (n:Norma {sigla:'CE'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'CE_101'}), (c:CNO {id:'CNO-VIII-007'}) MERGE (a)-[:ESLABON_DE {orden: 1}]->(c);
MERGE (a:Articulo {id: 'LOPC_77'})
SET a.norma = 'LOPC', a.articulo = '77', a.sha256 = '52d1ccab33d4',
    a.rol = 'mecanismo_lopc', a.sumilla = 'silla vacía operativa en las sesiones del GAD: participación con voz y voto', a.updated_at = datetime();
MATCH (a:Articulo {id:'LOPC_77'}), (n:Norma {sigla:'LOPC'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'LOPC_77'}), (c:CNO {id:'CNO-VIII-007'}) MERGE (a)-[:ESLABON_DE {orden: 2}]->(c);
MERGE (a:Articulo {id: 'COOTAD_311'})
SET a.norma = 'COOTAD', a.articulo = '311', a.sha256 = '9055359360bb',
    a.rol = 'mecanismo_cootad', a.sumilla = 'silla vacía en las sesiones del GAD: representante de la ciudadanía en función de los temas a tratarse', a.updated_at = datetime();
MATCH (a:Articulo {id:'COOTAD_311'}), (n:Norma {sigla:'COOTAD'}) MERGE (a)-[:PARTE_DE]->(n);
MATCH (a:Articulo {id:'COOTAD_311'}), (c:CNO {id:'CNO-VIII-007'}) MERGE (a)-[:ESLABON_DE {orden: 3}]->(c);

// -- 4. JERARQUIA institucional (FUNDAMENTA + delegados) -----------------------
MATCH (c:CNO {id:'CNO-VIII-001'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);
MATCH (c:CNO {id:'CNO-VIII-002'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);
MATCH (c:CNO {id:'CNO-VIII-003'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);
MATCH (c:CNO {id:'CNO-VIII-003'}), (a:CNO {id:'CNO-VIII-002'}) MERGE (c)-[:RECIBE_DELEGADOS_DE]->(a);
MATCH (c:CNO {id:'CNO-VIII-004'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);
MATCH (c:CNO {id:'CNO-VIII-005'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);
MATCH (c:CNO {id:'CNO-VIII-006'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);
MATCH (c:CNO {id:'CNO-VIII-007'}), (m:CNO {id:'CNO-VIII-000'}) MERGE (c)-[:FUNDAMENTA_EN]->(m);

// -- 5. SENAL SAT del Gold Master (SAT-VI Desvio PP · unica de participacion · OBS-016) --
MERGE (s:SenalSAT {id: 'SAT-VI'})
SET s.nombre = 'Desvío Presupuesto Participativo', s.dimension_tgi = 'D4',
    s.hoja_gold_master = 'H24c_SAT-VI_DESVÍO_PP', s.dominio = 'd08',
    s.estado = 'sin datos (Hay_Datos_PP = NO) — coherente con OBS-015 (IGP_PP=0)', s.updated_at = datetime();
MATCH (s:SenalSAT {id:'SAT-VI'}), (d:Dominio {id:'d08'}) MERGE (s)-[:VIGILA_A]->(d);
MATCH (s:SenalSAT {id:'SAT-VI'}), (c:CNO {id:'CNO-VIII-005'}) MERGE (s)-[:FUNDAMENTADA_EN]->(c);
// NOTA: las SAT que falten para d08 se disenian en fase 2 (Excel canonico). La
//   verificabilidad por instancia (RO-VIII-001) NO es SAT: es estado de evidencia.

// -- 6. REGLAS OPERATIVAS (3 dimensiones) --------------------------------------
MERGE (r:RO {id: 'RO-VIII-001'})
SET r.dimension = 'integridad_normativa', r.metrica = 'Integridad_Normativa_Sistema_Participacion',
    r.estado = 'propuesta', r.opera_en = 'd08', r.updated_at = datetime();
MATCH (r:RO {id:'RO-VIII-001'}), (c:CNO {id:'CNO-VIII-000'}) MERGE (r)-[:DERIVA_DE]->(c);
MERGE (r:RO {id: 'RO-VIII-002'})
SET r.dimension = 'vitalidad_democratica', r.metrica = 'Vitalidad_Democratica_Participacion',
    r.estado = 'propuesta', r.opera_en = 'd08', r.updated_at = datetime();
MATCH (r:RO {id:'RO-VIII-002'}), (c:CNO {id:'CNO-VIII-000'}) MERGE (r)-[:DERIVA_DE]->(c);
MERGE (r:RO {id: 'RO-VIII-003'})
SET r.dimension = 'efectividad_incidencia', r.metrica = 'Efectividad_Incidencia_Participacion',
    r.estado = 'propuesta', r.opera_en = 'd08', r.updated_at = datetime();
MATCH (r:RO {id:'RO-VIII-003'}), (c:CNO {id:'CNO-VIII-000'}) MERGE (r)-[:DERIVA_DE]->(c);
MATCH (r:RO {id:'RO-VIII-003'}), (s:SenalSAT {id:'SAT-VI'}) MERGE (r)-[:CONSUME]->(s);

// -- 7. MUNICIPIO -------------------------------------------------------------
MERGE (m:Municipio {id: 'MCR-001'})
SET m.nombre = 'Montecristi', m.rol = 'molde_validacion_empirica', m.updated_at = datetime();
MATCH (m:Municipio {id:'MCR-001'}), (d:Dominio {id:'d08'}) MERGE (m)-[:EVALUADO_EN]->(d);