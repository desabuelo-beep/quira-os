// ============================================================
// Cypher 002 — d07 Transparencia: ontologia completa (CD-XX)
// QUIRA Gov . AuraDB . Dylus Lab (c) 2026
// Fuente: CATALOGO_CANONICO_CD_D07_v1.0.0 (Single Source of Truth)
// Ontologia (colega, 2026-07-22): Dominio, CD, Norma, Articulo, Regla,
//   Componente, Portal, Evidencia, Observacion, Municipio.
// NOTA: :Campo se omite deliberadamente -- Campos[] sigue pendiente de
//   extraccion formal (ver CATALOGO_CANONICO_CD_D07 Pendiente explicito),
//   no se inventa (Regla 3).
// APLICAR:
//   python scripts/cypher/apply_cypher.py scripts/cypher/002_d07_transparencia.cypher
// ============================================================

// -- 1. DOMINIO --------------------------------------------------------------
MERGE (d:Dominio {id: 'd07'})
SET d.nombre = 'Transparencia', d.capacidad = 'verificabilidad',
    d.metrica_ref = 'SITA', d.catalogo_version = 'CATALOGO_CANONICO_CD_D07_v1.0.0',
    d.updated_at = datetime();

// -- 2. NORMAS -----------------------------------------------------------------
MERGE (n:Norma {sigla: 'LOTAIP'})
SET n.nombre = 'Ley Orgánica de Transparencia y Acceso a la Información Pública', n.tipo = 'ley', n.jerarquia = 1,
    n.estado_corpus = 'ingresado', n.updated_at = datetime();
MERGE (n:Norma {sigla: 'RLOTAIP'})
SET n.nombre = 'Reglamento General LOTAIP', n.tipo = 'reglamento', n.jerarquia = 2,
    n.estado_corpus = 'ingresado', n.updated_at = datetime();
MERGE (n:Norma {sigla: 'GUIA-LOTAIP-MEC'})
SET n.nombre = 'Guía Metodológica de Mecanismos 2024', n.tipo = 'guia', n.jerarquia = 5,
    n.estado_corpus = 'ingresado', n.updated_at = datetime();
MERGE (n:Norma {sigla: 'INST-TA-2024'})
SET n.nombre = 'Instructivo de Monitoreo de Transparencia Activa 2024', n.tipo = 'instructivo', n.jerarquia = 6,
    n.estado_corpus = 'arqueologia_no_ingerido', n.updated_at = datetime();

// -- 3. REGLAS (SITA) ------------------------------------------------------------
MERGE (r:Regla {sigla: 'CTA'})
SET r.nombre = 'Condiciones de Transparencia Activa', r.escala = '1.0/0.5/0.0', r.fuente = 'Tabla 0 Instructivo',
    r.updated_at = datetime();
MERGE (r:Regla {sigla: 'ETA'})
SET r.nombre = 'Estructura de Datos Abiertos', r.escala = '1/0', r.fuente = 'Tabla 1 Instructivo',
    r.updated_at = datetime();
MERGE (r:Regla {sigla: 'RP'})
SET r.nombre = 'Registro dentro del Plazo', r.escala = '1/0', r.fuente = 'Tabla 2 Instructivo',
    r.updated_at = datetime();
MERGE (r:Regla {sigla: 'CI'})
SET r.nombre = 'Calidad de la Información', r.escala = 'SI/NO', r.fuente = 'Tabla 5 Instructivo',
    r.updated_at = datetime();

// -- 4. PORTAL (nodo unico -- Portal Nacional de Transparencia) -----------------
MERGE (p:Portal {id: 'PNT-DPE'})
SET p.nombre = 'Portal Nacional de Transparencia', p.entidad_rectora = 'DPE',
    p.updated_at = datetime();

// -- 5. ARTICULOS (uno por numeral real de la LOTAIP) ---------------------------
MERGE (a:Articulo {id: 'Art19_1'})
SET a.numeral = '1', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_1'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_2'})
SET a.numeral = '2', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_2'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_3'})
SET a.numeral = '3', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_3'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_4'})
SET a.numeral = '4', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_4'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_6'})
SET a.numeral = '6', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_6'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_7'})
SET a.numeral = '7', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_7'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_8'})
SET a.numeral = '8', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_8'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_9'})
SET a.numeral = '9', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_9'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_10'})
SET a.numeral = '10', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_10'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_11'})
SET a.numeral = '11', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_11'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_12'})
SET a.numeral = '12', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_12'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_13'})
SET a.numeral = '13', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_13'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_14'})
SET a.numeral = '14', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_14'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_15'})
SET a.numeral = '15', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_15'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_16'})
SET a.numeral = '16', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_16'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_17'})
SET a.numeral = '17', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_17'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_18'})
SET a.numeral = '18', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_18'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_19'})
SET a.numeral = '19', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_19'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_20'})
SET a.numeral = '20', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_20'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_21'})
SET a.numeral = '21', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_21'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_23'})
SET a.numeral = '23', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_23'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_24'})
SET a.numeral = '24', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_24'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Art19_5_22'})
SET a.numeral = '5+22', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Art19_5_22'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);
MERGE (a:Articulo {id: 'Articulo24_GAD'})
SET a.numeral = 'Art.24 (capitulo propio, no Art.19)', a.updated_at = datetime();
MATCH (a:Articulo {id: 'Articulo24_GAD'}), (n:Norma {sigla: 'LOTAIP'}) MERGE (a)-[:PARTE_DE]->(n);

// -- 6. CD + relaciones (Dominio, Articulo, Norma, Reglas, Portal) --------------
MERGE (cd:CD {id: 'CD-01'})
SET cd.numeral_ley = '1',
    cd.nombre = 'Estructura orgánica + base legal + metas',
    cd.estado_normativa = true,
    cd.estado_operativa = false,
    cd.estado_empirica = false,
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-01'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-01'}), (a:Articulo {id: 'Art19_1'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-01'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-01'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-01'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-01'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-01'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-01'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-01'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-02'})
SET cd.numeral_ley = '2',
    cd.nombre = 'Directorio y distributivo de personal',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14338,
    cd.guia_sha256 = '47d5c63d41',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-02'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-02'}), (a:Articulo {id: 'Art19_2'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-02'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-02'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-02'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-02'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-02'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-02'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-02'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-02'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-03'})
SET cd.numeral_ley = '3',
    cd.nombre = 'Remuneraciones salariales',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14339,
    cd.guia_sha256 = 'fbbcdf5f0e',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-03'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-03'}), (a:Articulo {id: 'Art19_3'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-03'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-03'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-03'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-03'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-03'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-03'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-03'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-03'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-04'})
SET cd.numeral_ley = '4',
    cd.nombre = 'Licencias/comisión de servicio',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14340,
    cd.guia_sha256 = 'd9d1a19288',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-04'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-04'}), (a:Articulo {id: 'Art19_4'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-04'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-04'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-04'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-04'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-04'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-04'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-04'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-04'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-05'})
SET cd.numeral_ley = '5+22',
    cd.nombre = 'Servicios + formularios de trámites',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14341,
    cd.guia_sha256 = '5e27a9a3d7',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-05'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-05'}), (a:Articulo {id: 'Art19_5_22'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-05'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-05'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-05'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-05'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-05'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-05'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-05'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-05'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-06'})
SET cd.numeral_ley = '6',
    cd.nombre = 'Presupuesto Institucional',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = true,
    cd.guia_chunk_id = 14342,
    cd.guia_sha256 = '9b50ff1592',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-06'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-06'}), (a:Articulo {id: 'Art19_6'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-06'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-06'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-06'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-06'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-06'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-06'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-06'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-06'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-07'})
SET cd.numeral_ley = '7',
    cd.nombre = 'Auditorías internas/gubernamentales',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14343,
    cd.guia_sha256 = 'e9f4d38340',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-07'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-07'}), (a:Articulo {id: 'Art19_7'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-07'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-07'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-07'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-07'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-07'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-07'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-07'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-07'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-08'})
SET cd.numeral_ley = '8',
    cd.nombre = 'Contratación (precontractual→liquidación)',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14344,
    cd.guia_sha256 = 'be252c5009',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-08'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-08'}), (a:Articulo {id: 'Art19_8'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-08'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-08'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-08'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-08'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-08'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-08'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-08'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-08'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-09'})
SET cd.numeral_ley = '9',
    cd.nombre = 'Empresas que incumplieron contratos',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14345,
    cd.guia_sha256 = 'ec64c0df9d',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-09'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-09'}), (a:Articulo {id: 'Art19_9'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-09'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-09'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-09'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-09'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-09'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-09'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-09'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-09'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-10'})
SET cd.numeral_ley = '10',
    cd.nombre = 'Planes y programas',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14346,
    cd.guia_sha256 = 'c51d4955ac',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-10'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-10'}), (a:Articulo {id: 'Art19_10'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-10'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-10'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-10'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-10'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-10'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-10'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-10'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-10'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-11'})
SET cd.numeral_ley = '11',
    cd.nombre = 'Contratos de crédito',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14347,
    cd.guia_sha256 = 'cf2ef7f783',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-11'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-11'}), (a:Articulo {id: 'Art19_11'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-11'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-11'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-11'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-11'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-11'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-11'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-11'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-11'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-12'})
SET cd.numeral_ley = '12',
    cd.nombre = 'Mecanismos de rendición de cuentas',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14348,
    cd.guia_sha256 = '1fc319d264',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-12'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-12'}), (a:Articulo {id: 'Art19_12'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-12'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-12'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-12'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-12'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-12'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-12'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-12'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-12'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-13'})
SET cd.numeral_ley = '13',
    cd.nombre = 'Viáticos',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14349,
    cd.guia_sha256 = '414116b17d',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-13'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-13'}), (a:Articulo {id: 'Art19_13'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-13'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-13'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-13'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-13'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-13'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-13'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-13'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-13'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-14'})
SET cd.numeral_ley = '14',
    cd.nombre = 'Responsable de acceso a la información',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14350,
    cd.guia_sha256 = '123c0c355d',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-14'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-14'}), (a:Articulo {id: 'Art19_14'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-14'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-14'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-14'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-14'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-14'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-14'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-14'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-14'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-15'})
SET cd.numeral_ley = '15',
    cd.nombre = 'Contratos colectivos vigentes',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14351,
    cd.guia_sha256 = 'e7c409c65c',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-15'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-15'}), (a:Articulo {id: 'Art19_15'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-15'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-15'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-15'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-15'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-15'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-15'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-15'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-15'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-16'})
SET cd.numeral_ley = '16',
    cd.nombre = 'Índice de información reservada',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14352,
    cd.guia_sha256 = 'a7bd15f17f',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-16'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-16'}), (a:Articulo {id: 'Art19_16'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-16'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-16'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-16'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-16'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-16'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-16'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-16'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-16'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-17'})
SET cd.numeral_ley = '17',
    cd.nombre = 'Audiencias y reuniones de autoridades',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14353,
    cd.guia_sha256 = '46eab0be54',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-17'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-17'}), (a:Articulo {id: 'Art19_17'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-17'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-17'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-17'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-17'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-17'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-17'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-17'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-17'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-18'})
SET cd.numeral_ley = '18',
    cd.nombre = 'Convenios nacionales/internacionales',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14354,
    cd.guia_sha256 = '984b95ca6d',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-18'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-18'}), (a:Articulo {id: 'Art19_18'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-18'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-18'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-18'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-18'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-18'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-18'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-18'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-18'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-19'})
SET cd.numeral_ley = '19',
    cd.nombre = 'Donativos oficiales y protocolares',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14355,
    cd.guia_sha256 = 'bcb7cbd47a',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-19'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-19'}), (a:Articulo {id: 'Art19_19'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-19'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-19'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-19'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-19'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-19'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-19'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-19'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-19'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-20'})
SET cd.numeral_ley = '20',
    cd.nombre = 'Registro de activos de información',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14356,
    cd.guia_sha256 = 'a93dda6314',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-20'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-20'}), (a:Articulo {id: 'Art19_20'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-20'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-20'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-20'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-20'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-20'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-20'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-20'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-20'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-21'})
SET cd.numeral_ley = '21',
    cd.nombre = 'Políticas públicas / grupo específico',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14357,
    cd.guia_sha256 = '17bbfd0611',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-21'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-21'}), (a:Articulo {id: 'Art19_21'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-21'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-21'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-21'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-21'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-21'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-21'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-21'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-21'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-23'})
SET cd.numeral_ley = '23',
    cd.nombre = 'Cuotas laborales (discapacidad/pueblos)',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14358,
    cd.guia_sha256 = '14b51ad72f',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-23'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-23'}), (a:Articulo {id: 'Art19_23'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-23'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-23'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-23'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-23'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-23'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-23'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-23'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-23'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-24'})
SET cd.numeral_ley = '24',
    cd.nombre = 'Información relevante adicional (ODS)',
    cd.estado_normativa = true,
    cd.estado_operativa = true,
    cd.estado_empirica = false,
    cd.guia_chunk_id = 14359,
    cd.guia_sha256 = 'f64155a202',
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-24'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-24'}), (a:Articulo {id: 'Art19_24'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-24'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-24'}), (n:Norma {sigla: 'GUIA-LOTAIP-MEC'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-24'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-24'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-24'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-24'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-24'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-24'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

MERGE (cd:CD {id: 'CD-A24'})
SET cd.numeral_ley = 'Art.24',
    cd.nombre = 'Ordenanzas/actas de sesión/contratación',
    cd.estado_normativa = true,
    cd.estado_operativa = false,
    cd.estado_empirica = false,
    cd.updated_at = datetime();
MATCH (dm:Dominio {id: 'd07'}), (cd:CD {id: 'CD-A24'}) MERGE (dm)-[:CONTIENE]->(cd);
MATCH (cd:CD {id: 'CD-A24'}), (a:Articulo {id: 'Articulo24_GAD'}) MERGE (cd)-[:DEFINIDO_POR]->(a);
MATCH (cd:CD {id: 'CD-A24'}), (n:Norma {sigla: 'RLOTAIP'}) MERGE (cd)-[:DEFINIDO_POR]->(n);
MATCH (cd:CD {id: 'CD-A24'}), (n:Norma {sigla: 'INST-TA-2024'}) MERGE (cd)-[:OPERATIVIZADO_POR]->(n);
MATCH (cd:CD {id: 'CD-A24'}), (r:Regla {sigla: 'CTA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-A24'}), (r:Regla {sigla: 'ETA'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-A24'}), (r:Regla {sigla: 'RP'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-A24'}), (r:Regla {sigla: 'CI'}) MERGE (cd)-[:EVALUADO_MEDIANTE]->(r);
MATCH (cd:CD {id: 'CD-A24'}), (p:Portal {id: 'PNT-DPE'}) MERGE (cd)-[:VERIFICADO_EN]->(p);

// -- 7. CD-06 -- Componentes internos (arbol, S6b METODOLOGIA_D07) --------------
MERGE (c:Componente {id: 'CD06_Ingresos'})
SET c.nombre = 'Ingresos', c.cd_padre = 'CD-06',
    c.evidencia_ausente = true, c.updated_at = datetime();
MATCH (cd:CD {id: 'CD-06'}), (c:Componente {id: 'CD06_Ingresos'}) MERGE (cd)-[:TIENE_COMPONENTE]->(c);
MERGE (c:Componente {id: 'CD06_Gastos'})
SET c.nombre = 'Gastos', c.cd_padre = 'CD-06',
    c.evidencia_ausente = false, c.updated_at = datetime();
MATCH (cd:CD {id: 'CD-06'}), (c:Componente {id: 'CD06_Gastos'}) MERGE (cd)-[:TIENE_COMPONENTE]->(c);
MERGE (c:Componente {id: 'CD06_Financiamiento'})
SET c.nombre = 'Financiamiento', c.cd_padre = 'CD-06',
    c.evidencia_ausente = false, c.updated_at = datetime();
MATCH (cd:CD {id: 'CD-06'}), (c:Componente {id: 'CD06_Financiamiento'}) MERGE (cd)-[:TIENE_COMPONENTE]->(c);
MERGE (c:Componente {id: 'CD06_Resultados_operativos'})
SET c.nombre = 'Resultados operativos', c.cd_padre = 'CD-06',
    c.evidencia_ausente = false, c.updated_at = datetime();
MATCH (cd:CD {id: 'CD-06'}), (c:Componente {id: 'CD06_Resultados_operativos'}) MERGE (cd)-[:TIENE_COMPONENTE]->(c);
MERGE (c:Componente {id: 'CD06_Liquidacion'})
SET c.nombre = 'Liquidacion', c.cd_padre = 'CD-06',
    c.evidencia_ausente = false, c.updated_at = datetime();
MATCH (cd:CD {id: 'CD-06'}), (c:Componente {id: 'CD06_Liquidacion'}) MERGE (cd)-[:TIENE_COMPONENTE]->(c);

// -- 8. EVIDENCIA real (unica confirmada: CD-06, CSV oficial 2026-05) ----------
MERGE (ev:Evidencia {id: 'EVID-CD06-2026-05'})
SET ev.fuente = 'CSV oficial 2026-Mayo-Numeral 6-datos6.csv',
    ev.hallazgo = 'ausencia de cedula de ingresos',
    ev.registros = 75, ev.cuentas_gasto_pct = 100.0,
    ev.referencia_obs = 'OBS-011', ev.updated_at = datetime();
MATCH (c:Componente {id: 'CD06_Ingresos'}), (ev:Evidencia {id: 'EVID-CD06-2026-05'}) MERGE (c)-[:RESPALDADO_POR]->(ev);

// -- 9. OBSERVACION (hallazgo OBS-011 -- incongruencia intersistemica) ---------
MERGE (o:Observacion {id: 'OBS-011'})
SET o.titulo = 'Incongruencia Intersistemica LOTAIP Numeral 6',
    o.tipo = 'contradiccion_norma_operativa',
    o.responsabilidad = 'DPE reconoce discrepancia (correo 2026-07-09)',
    o.updated_at = datetime();
MATCH (cd:CD {id: 'CD-06'}), (o:Observacion {id: 'OBS-011'}) MERGE (cd)-[:GENERA]->(o);

// -- 10. MUNICIPIO (Montecristi = molde de validacion empirica) ----------------
MERGE (m:Municipio {id: 'MCR-001'})
SET m.nombre = 'Montecristi', m.rol = 'molde_validacion_empirica',
    m.updated_at = datetime();
MATCH (m:Municipio {id: 'MCR-001'}), (cd:CD {id: 'CD-06'}) MERGE (m)-[:OBSERVADO_EN {estado: 'evidencia_real_confirmada'}]->(cd);