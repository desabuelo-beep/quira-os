-- ============================================================
-- Migration 002 — fondos_oportunidades: Motor de Elegibilidad D02
-- QUIRA Gov · Dylus Lab © 2026
-- Referencia: ADR-026 §D02 Consecuencia · /fondos-radar skill
-- Fecha: 2026-06-09
-- Autores: Claude (director técnico) + Colega (asesor externo)
-- ============================================================
-- PROPÓSITO:
--   Reemplaza p18_cooperacion.py hardcodeado (bonds sin base Excel)
--   con un motor de elegibilidad institucional dinámico.
--   Responde: "¿Cuánto cuesta al GAD no cumplir sus indicadores?"
--
-- DISEÑO: 5 tablas relacionales + semilla canónica
--   fondos_emisores          → actores estables (índice permanente)
--   fondos_convocatorias     → eventos temporales (adjuntos al emisor)
--   fondos_requisitos        → 21 indicadores canónicos QUIRA
--   fondos_conv_requisitos   → junction: convocatoria × requisito × umbral
--   fondos_elegibilidad      → output del Matcher (calculado, no editado)
--
-- PRINCIPIO:
--   requisitos = QUÉ se mide (el indicador, sin valor)
--   conv_requisitos = CUÁNTO pide esta convocatoria (operador + umbral)
--   Esto evita duplicar reglas: PSG_30, PSG_20, PSG_25 son la misma columna.
--
-- BLOOMBERG FIREWALL:
--   nombre_publico en fondos_requisitos = lenguaje de gobernanza (no metodología interna)
--   NUNCA exponer: ICPI · TGI · Ti · QTMP · H73 · Gold Master en UI
--
-- SEGURIDAD: todas las columnas nuevas son nullable donde aplica (no rompe datos existentes)
-- REVERSIBLE: ver 002_rollback.sql
-- ============================================================


-- ── TABLA 1: fondos_emisores ──────────────────────────────────────────────────
-- Índice permanente de actores que emiten oportunidades de financiamiento.
-- Los emisores NO se eliminan: se marcan activo=false cuando dejan de operar.
-- Las convocatorias desaparecen; el emisor permanece con su historial.

CREATE TABLE IF NOT EXISTS fondos_emisores (
    id              SERIAL          PRIMARY KEY,
    codigo          TEXT            UNIQUE NOT NULL,   -- slug legible: BID, FORD, GIZ
    nombre          TEXT            NOT NULL,

    -- Clasificación dimensional (Colega v3: 2 dimensiones ortogonales)
    tipo_emisor     TEXT            NOT NULL
                    CHECK (tipo_emisor IN (
                        -- Reembolsable
                        'multilateral',         -- BID, CAF, BM
                        'bilateral',            -- AECID, GIZ, AFD
                        'banca_desarrollo',     -- BDE, CFN
                        'banco_comercial',
                        'fondo_inversion',
                        'blended_finance',
                        -- No reembolsable
                        'multilateral_onu',     -- PNUD, ONU Mujeres, UNICEF
                        'fundacion',            -- Ford, Rockefeller
                        'embajada',             -- Canadá, Alemania, Japón
                        'empresa_esg',          -- Holcim, programas RSE
                        'camara',               -- AME, cámaras binacionales
                        'academia',             -- Erasmus, Horizon
                        'ong_internacional',    -- WWF, TNC
                        'fondo_climatico',      -- GEF, GCF
                        'fondo_innovacion',     -- innovación pública, smart cities
                        'aceleradora',
                        'incubadora',
                        'venture_philanthropy',
                        'premio_challenge'
                    )),

    naturaleza      TEXT            NOT NULL
                    CHECK (naturaleza IN ('reembolsable', 'no_reembolsable', 'ambas')),

    -- Geografía
    pais_origen     TEXT,
    region          TEXT            CHECK (region IN ('Ecuador', 'AL', 'global', 'EU', 'NA', 'AS')),

    -- Alcance temático y entidades elegibles (arrays PostgreSQL)
    temas           TEXT[]          DEFAULT ARRAY[]::TEXT[],
    elegibles       TEXT[]          DEFAULT ARRAY[]::TEXT[],
                    -- valores válidos: GAD, ONG, OSC, academia, startup,
                    --                  empresa, coalicion, Estado

    -- Referencia histórica para estimaciones (sin convocatoria activa)
    monto_min_usd   BIGINT,
    monto_max_usd   BIGINT,
    frecuencia      TEXT            CHECK (frecuencia IN (
                        'continua', 'anual', 'bienal', 'irregular', 'unica', 'desconocida'
                    )),

    web             TEXT,
    activo          BOOLEAN         DEFAULT TRUE,
    notas           TEXT,
    metadata_json   JSONB           DEFAULT '{}',

    created_at      TIMESTAMPTZ     DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     DEFAULT NOW()
);

COMMENT ON TABLE fondos_emisores IS
    'Índice permanente de actores que emiten financiamiento. '
    'Emisores = entidades estables (no se borran). '
    'Convocatorias = eventos temporales adjuntos al emisor. '
    'ADR-026 §D02 Motor Elegibilidad · /fondos-radar · Dylus Lab 2026';

CREATE INDEX IF NOT EXISTS idx_emisores_tipo ON fondos_emisores (tipo_emisor);
CREATE INDEX IF NOT EXISTS idx_emisores_naturaleza ON fondos_emisores (naturaleza);
CREATE INDEX IF NOT EXISTS idx_emisores_activo ON fondos_emisores (activo);


-- ── TABLA 2: fondos_convocatorias ─────────────────────────────────────────────
-- Eventos temporales de financiamiento adjuntos a un emisor.
-- Los estados siguen el ciclo de vida: proxima → abierta → cerrada | recurrente

CREATE TABLE IF NOT EXISTS fondos_convocatorias (
    id              SERIAL          PRIMARY KEY,
    codigo          TEXT            UNIQUE NOT NULL,   -- slug: BID-2026-A, FORD-GOBERNANZA-2026
    emisor_id       INTEGER         NOT NULL REFERENCES fondos_emisores(id) ON DELETE RESTRICT,
    nombre          TEXT            NOT NULL,

    estado          TEXT            NOT NULL
                    CHECK (estado IN (
                        'abierta',          -- activa ahora, puede aplicarse
                        'proxima',          -- anunciada, aún no abierta
                        'cerrada',          -- este ciclo terminó
                        'recurrente',       -- abre periódicamente (sin fecha fija)
                        'discontinuada'     -- ya no existe
                    )),

    fecha_apertura  DATE,
    fecha_cierre    DATE,

    -- Montos específicos de esta convocatoria (pueden diferir del emisor histórico)
    monto_min_usd   BIGINT,
    monto_max_usd   BIGINT,
    moneda          TEXT            DEFAULT 'USD',

    -- Elegibles específicos (si más restrictivo que el emisor)
    elegibles       TEXT[]          DEFAULT NULL,      -- NULL = hereda del emisor
    temas           TEXT[]          DEFAULT ARRAY[]::TEXT[],

    url             TEXT,
    descripcion     TEXT,
    notas           TEXT,

    snapshot_date       DATE        DEFAULT CURRENT_DATE,
    proxima_revision    DATE,

    metadata_json   JSONB           DEFAULT '{}',
    created_at      TIMESTAMPTZ     DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     DEFAULT NOW()
);

COMMENT ON TABLE fondos_convocatorias IS
    'Eventos temporales de financiamiento. FK: emisor_id → fondos_emisores. '
    'Elegibles=NULL hereda del emisor. El Matcher opera sobre abierta+recurrente. '
    'ADR-026 §D02 · /fondos-radar · Dylus Lab 2026';

CREATE INDEX IF NOT EXISTS idx_conv_emisor ON fondos_convocatorias (emisor_id);
CREATE INDEX IF NOT EXISTS idx_conv_estado ON fondos_convocatorias (estado);
CREATE INDEX IF NOT EXISTS idx_conv_cierre ON fondos_convocatorias (fecha_cierre);


-- ── TABLA 3: fondos_requisitos ────────────────────────────────────────────────
-- Catálogo canónico de 21 indicadores QUIRA usables como gates de elegibilidad.
-- QUÉ se puede medir — sin valores ni umbrales (esos van en conv_requisitos).
-- fuente_quira: dónde lee el Matcher el valor actual del GAD.
-- NUNCA hardcodear umbrales aquí — eso duplica reglas y rompe el modelo.

CREATE TABLE IF NOT EXISTS fondos_requisitos (
    id              SERIAL          PRIMARY KEY,
    codigo          TEXT            UNIQUE NOT NULL,   -- PSG, ISP, IFE_A, RDC_PRESENTADA

    familia         TEXT            NOT NULL
                    CHECK (familia IN (
                        'operacional',      -- outputs Tipo A del Gold Master
                        'institucional',    -- comportamientos D09/D07
                        'territorial',      -- D05 PDOT + D10
                        'gobernanza'        -- D03 IFE + ITAM
                    )),

    -- Bloomberg-safe: lenguaje de gobernanza, nunca códigos internos en UI
    nombre_publico  TEXT            NOT NULL,

    tipo_valor      TEXT            NOT NULL
                    CHECK (tipo_valor IN (
                        'porcentaje',   -- 0–100, comparar con gte/lte
                        'boolean',      -- True/False
                        'exists',       -- el dato existe en corpus (≥1 registro)
                        'enum',         -- valor pertenece a conjunto
                        'valor_usd',    -- monto en dólares
                        'entero'        -- número entero
                    )),

    unidad          TEXT,           -- %, USD, null para boolean/exists

    -- Dónde lee el Matcher el valor actual del GAD
    -- Valores canónicos: H73_OUTPUT_API | D09 | D07 | D07/Neo4j |
    --                    D05/Supabase | D03 | D03/Supabase | D10
    fuente_quira    TEXT            NOT NULL,

    descripcion     TEXT,
    activo          BOOLEAN         DEFAULT TRUE,
    created_at      TIMESTAMPTZ     DEFAULT NOW()
);

COMMENT ON TABLE fondos_requisitos IS
    'Catálogo canónico de indicadores QUIRA usables como gates de elegibilidad. '
    'Contiene QUÉ se mide (el indicador), NO el umbral. '
    'El umbral vive en fondos_conv_requisitos (una convocatoria puede pedir PSG≥30, otra PSG≥20). '
    'fuente_quira conecta el Matcher al Gold Master / módulos QUIRA. '
    'ADR-026 topología funcional completa · /fondos-radar · Dylus Lab 2026';


-- ── TABLA 4: fondos_conv_requisitos ───────────────────────────────────────────
-- Junction: qué requisito pide cada convocatoria y con qué umbral.
-- Aquí viven los valores específicos. Un mismo requisito reutilizado N veces.

CREATE TABLE IF NOT EXISTS fondos_conv_requisitos (
    id              SERIAL          PRIMARY KEY,
    convocatoria_id INTEGER         NOT NULL REFERENCES fondos_convocatorias(id) ON DELETE CASCADE,
    requisito_id    INTEGER         NOT NULL REFERENCES fondos_requisitos(id) ON DELETE RESTRICT,

    -- Lógica de evaluación
    operador        TEXT            NOT NULL
                    CHECK (operador IN (
                        'gte',      -- ≥ (mayor o igual)
                        'lte',      -- ≤
                        'gt',       -- >
                        'lt',       -- <
                        'eq',       -- = (igualdad exacta)
                        'exists',   -- el dato existe (para tipo exists)
                        'eq_true',  -- debe ser True (para boolean)
                        'in'        -- valor pertenece a lista (para enum)
                    )),

    valor           NUMERIC,        -- umbral numérico (NULL para boolean/exists)
    valor_enum      TEXT[],         -- lista válida para operador 'in'

    -- Lógica booleana entre requisitos de la misma convocatoria
    logica          TEXT            DEFAULT 'AND'
                    CHECK (logica IN ('AND', 'OR')),

    -- Si es crítico: fallar → no_elegible. Si no: fallar → elegible_con_brecha
    es_critico      BOOLEAN         DEFAULT TRUE,

    notas           TEXT,

    UNIQUE (convocatoria_id, requisito_id)
);

COMMENT ON TABLE fondos_conv_requisitos IS
    'Requisitos específicos de cada convocatoria: indicador + operador + umbral. '
    'Reutiliza fondos_requisitos sin duplicar definiciones. '
    'es_critico=true: fallar → no_elegible. es_critico=false: fallar → elegible_con_brecha. '
    'ADR-026 §D02 · Dylus Lab 2026';

CREATE INDEX IF NOT EXISTS idx_convreq_conv ON fondos_conv_requisitos (convocatoria_id);
CREATE INDEX IF NOT EXISTS idx_convreq_req ON fondos_conv_requisitos (requisito_id);


-- ── TABLA 5: fondos_elegibilidad ──────────────────────────────────────────────
-- Output del Matcher (fondos_matcher.py). NO se edita manualmente.
-- Se recalcula cada vez que el Matcher corre (~15 días o cuando indicators cambian).
-- computed_at permite saber si el cálculo está desactualizado.

CREATE TABLE IF NOT EXISTS fondos_elegibilidad (
    id              SERIAL          PRIMARY KEY,
    convocatoria_id INTEGER         NOT NULL REFERENCES fondos_convocatorias(id) ON DELETE CASCADE,
    gad_id          TEXT            NOT NULL DEFAULT 'MCR-001',
                    -- MCR-001 = Montecristi. Preparado para multi-GAD futuro.

    estado_quira    TEXT            NOT NULL
                    CHECK (estado_quira IN (
                        'elegible_hoy',         -- cumple TODOS los requisitos
                        'elegible_con_brecha',  -- cumple los críticos, brecha en opcionales
                        'no_elegible',          -- falla al menos un requisito crítico
                        'pendiente_datos'       -- fuente no disponible para calcular
                    )),

    -- Detalle de brechas por indicador: {"psg": -17.17, "isp": -50.42}
    -- Valores negativos = cuánto falta para alcanzar el umbral
    brechas_json    JSONB           DEFAULT '{}',

    -- Monto potencial desbloqueado si se cierran brechas
    potencial_usd   BIGINT,
    monto_confianza TEXT            CHECK (monto_confianza IN (
                        'alta',     -- convocatoria abierta con monto publicado
                        'media',    -- convocatoria próxima o estimada
                        'estimado'  -- histórico del emisor sin convocatoria activa
                    )),

    -- Snapshot de indicadores al momento del cálculo (auditoría)
    indicadores_json JSONB          DEFAULT '{}',
                    -- {"psg": 12.83, "isp": 14.58, "itam": 56, "ife_a": 72.73, ...}

    computed_at     TIMESTAMPTZ     DEFAULT NOW(),

    UNIQUE (convocatoria_id, gad_id)
);

COMMENT ON TABLE fondos_elegibilidad IS
    'Output calculado del Matcher. NO editar manualmente. '
    'Actualizar con fondos_matcher.py cada ~15 días o cuando indicadores QUIRA cambien. '
    'brechas_json: valores negativos = cuánto falta. potencial_usd = monto desbloqueado. '
    'indicadores_json: snapshot de valores en el momento del cálculo (auditoría). '
    'ADR-026 §D02 Consecuencia · /fondos-radar · Dylus Lab 2026';

CREATE INDEX IF NOT EXISTS idx_eleg_conv ON fondos_elegibilidad (convocatoria_id);
CREATE INDEX IF NOT EXISTS idx_eleg_gad ON fondos_elegibilidad (gad_id);
CREATE INDEX IF NOT EXISTS idx_eleg_estado ON fondos_elegibilidad (estado_quira);
CREATE INDEX IF NOT EXISTS idx_eleg_computed ON fondos_elegibilidad (computed_at);


-- ============================================================
-- SEMILLA — fondos_requisitos (21 indicadores canónicos v1)
-- Deriva de ADR-026 topología funcional completa.
-- Cubre los 4 tipos: Operacional (6) · Institucional (6) · Territorial (4) · Gobernanza (5)
-- NUNCA incluir umbrales aquí: van en fondos_conv_requisitos.
-- ============================================================

INSERT INTO fondos_requisitos (codigo, familia, nombre_publico, tipo_valor, unidad, fuente_quira, descripcion) VALUES

-- ── FAMILIA A: OPERACIONALES (6) — outputs directos Gold Master H73 ──────────
('PSG',
 'operacional',
 'Presupuesto Sensible al Género',
 'porcentaje', '%',
 'H73_OUTPUT_API',
 'Porcentaje del presupuesto institucional con enfoque de género · D12'),

('ISP',
 'operacional',
 'Índice de Salud Presupuestaria',
 'porcentaje', '%',
 'H73_OUTPUT_API',
 'Capacidad de ejecución presupuestaria del GAD · SAT-IV gate'),

('IGP',
 'operacional',
 'Índice de Gestión Participativa',
 'porcentaje', '%',
 'H73_OUTPUT_API',
 'Participación ciudadana activa en gestión · D08'),

('IOC',
 'operacional',
 'Índice de Observancia Contractual',
 'porcentaje', '%',
 'H73_OUTPUT_API',
 'Cumplimiento de contratos y compromisos institucionales · D07'),

('IET',
 'operacional',
 'Inversión por Habitante',
 'valor_usd', 'USD',
 'H73_OUTPUT_API',
 'Inversión pública per cápita en el territorio · D10'),

('IED',
 'operacional',
 'Índice de Equidad Territorial',
 'porcentaje', '%',
 'H73_OUTPUT_API',
 'Distribución equitativa de la inversión entre parroquias · D10'),

-- ── FAMILIA B: INSTITUCIONALES (6) — comportamientos verificables ─────────────
('RDC_PRESENTADA',
 'institucional',
 'Rendición de Cuentas presentada',
 'boolean', NULL,
 'D09',
 'RDC formal presentada ante CPCCS en el período vigente'),

('LOTAIP_VIGENTE',
 'institucional',
 'LOTAIP vigente y publicada',
 'boolean', NULL,
 'D07',
 'Portal LOTAIP actualizado con los 21 artículos'),

('PORTAL_OPERATIVO',
 'institucional',
 'Portal de transparencia operativo',
 'boolean', NULL,
 'D07',
 'Portal web de transparencia accesible y descargable · DPE API'),

('POA_APROBADO',
 'institucional',
 'POA aprobado',
 'boolean', NULL,
 'D09',
 'Plan Operativo Anual aprobado formalmente por Concejo'),

('PAC_APROBADO',
 'institucional',
 'PAC publicado',
 'boolean', NULL,
 'D09',
 'Plan Anual de Contratación aprobado y publicado en SERCOP'),

('CPCCS_SIN_OBS',
 'institucional',
 'Sin observaciones CPCCS vigentes',
 'boolean', NULL,
 'D09',
 'El GAD no tiene observaciones activas de la CPCCS · H31_REPORTE_CPCCS'),

-- ── FAMILIA C: TERRITORIALES (4) — D05 PDOT + D10 ────────────────────────────
('META_PDOT_ASOCIADA',
 'territorial',
 'Meta PDOT asociada al proyecto',
 'exists', NULL,
 'D05/Supabase',
 'El proyecto tiene al menos una meta del PDOT 2027 vinculada en corpus C1'),

('PDOT_ALINEADO',
 'territorial',
 'Proyecto alineado al PDOT vigente',
 'boolean', NULL,
 'D05/Supabase',
 'Alineación formal al PDOT 2027 verificable con MNT_UUID'),

('PRIORIDAD_TERRITORIAL',
 'territorial',
 'Área de intervención priorizada',
 'enum', NULL,
 'D10',
 'La intervención es en zona con IET bajo o meta territorial definida'),

('PARROQUIA_PRIORIZADA',
 'territorial',
 'Parroquia priorizada beneficiada',
 'enum', NULL,
 'D10',
 'Intervención directa en parroquia con menor inversión per cápita'),

-- ── FAMILIA D: GOBERNANZA DEMOCRÁTICA (5) — D03 IFE + D07 ITAM ───────────────
-- Esta familia es el diferenciador competitivo de QUIRA.
-- Ningún sistema de cooperación convencional tiene estos indicadores.
('IFE_A',
 'gobernanza',
 'Fidelidad del Mandato Electoral',
 'porcentaje', '%',
 'H73_OUTPUT_API',
 'Porcentaje de promesas CNE formalizadas en PDOT · D03 · IFE-A 72.73%'),

('PROMESA_CNE',
 'gobernanza',
 'Promesa CNE asociada al proyecto',
 'exists', NULL,
 'D03/Supabase',
 'El proyecto responde directamente a una promesa CNE con MNT_UUID trazable'),

('META_INST_FORMALIZADA',
 'gobernanza',
 'Meta institucional formalizada en PDOT',
 'boolean', NULL,
 'D03',
 'La meta está en PDOT con trazabilidad documental verificable'),

('EVIDENCIA_EJECUCION',
 'gobernanza',
 'Evidencia de ejecución documentada',
 'boolean', NULL,
 'D03',
 'Evidencia POA/PAC/eSIGEF vinculada · IFE-E (Q2-2026 cuando disponible)'),

('ITAM',
 'gobernanza',
 'Acceso a la Información Pública',
 'porcentaje', '%',
 'D07/Neo4j',
 'Cumplimiento LOTAIP 21 artículos · verificado Neo4j QTMP TRANSPARENCIA');


-- ============================================================
-- SEMILLA — fondos_emisores (21 emisores ancla v1)
-- Cubre todos los tipos del catálogo · ~18 Colega + 2 Director + 1 AME Ecuador
-- Columnas temas[] y elegibles[] llenadas para habilitar filtros inmediatos.
-- Montos son referencias históricas, NO umbrales formales de convocatoria.
-- ============================================================

INSERT INTO fondos_emisores
    (codigo, nombre, tipo_emisor, naturaleza, pais_origen, region,
     temas, elegibles, monto_min_usd, monto_max_usd, frecuencia, web, activo)
VALUES

-- ── MULTILATERALES REEMBOLSABLES ─────────────────────────────────────────────
('BID',
 'Banco Interamericano de Desarrollo',
 'multilateral', 'reembolsable', 'US', 'AL',
 ARRAY['infraestructura','desarrollo_local','genero','gobernanza'],
 ARRAY['GAD','Estado'],
 500000, 50000000, 'irregular',
 'https://iadb.org', true),

('CAF',
 'CAF - Banco de Desarrollo de América Latina',
 'multilateral', 'reembolsable', 'VE', 'AL',
 ARRAY['infraestructura','agua','sostenibilidad','transporte'],
 ARRAY['GAD','Estado'],
 1000000, 100000000, 'irregular',
 'https://caf.com', true),

('BM',
 'Banco Mundial',
 'multilateral', 'reembolsable', 'US', 'global',
 ARRAY['desarrollo_local','clima','gobernanza','reduccion_pobreza'],
 ARRAY['GAD','Estado'],
 500000, 200000000, 'irregular',
 'https://worldbank.org', true),

-- ── MULTILATERALES ONU NO REEMBOLSABLES ──────────────────────────────────────
('PNUD',
 'Programa de las Naciones Unidas para el Desarrollo',
 'multilateral_onu', 'no_reembolsable', 'US', 'global',
 ARRAY['gobernanza','desarrollo_local','clima','democracia'],
 ARRAY['GAD','ONG','OSC','academia'],
 50000, 2000000, 'anual',
 'https://undp.org', true),

('ONU_MUJERES',
 'ONU Mujeres',
 'multilateral_onu', 'no_reembolsable', 'US', 'global',
 ARRAY['genero','participacion','liderazgo','violencia_genero'],
 ARRAY['GAD','ONG','OSC'],
 30000, 500000, 'anual',
 'https://unwomen.org', true),

-- ── FONDOS CLIMÁTICOS ─────────────────────────────────────────────────────────
('GEF',
 'Global Environment Facility',
 'fondo_climatico', 'no_reembolsable', 'US', 'global',
 ARRAY['clima','biodiversidad','agua','economia_circular'],
 ARRAY['GAD','ONG','Estado'],
 100000, 10000000, 'irregular',
 'https://thegef.org', true),

('GCF',
 'Green Climate Fund',
 'fondo_climatico', 'no_reembolsable', 'KR', 'global',
 ARRAY['clima','adaptacion','mitigacion','resilencia'],
 ARRAY['GAD','Estado'],
 500000, 50000000, 'continua',
 'https://greenclimate.fund', true),

-- ── BILATERALES NO REEMBOLSABLES ─────────────────────────────────────────────
('AECID',
 'Agencia Española de Cooperación Internacional para el Desarrollo',
 'bilateral', 'no_reembolsable', 'ES', 'AL',
 ARRAY['gobernanza','desarrollo_local','cultura','genero'],
 ARRAY['GAD','ONG','academia'],
 30000, 1000000, 'anual',
 'https://aecid.es', true),

('GIZ',
 'Deutsche Gesellschaft für Internationale Zusammenarbeit',
 'bilateral', 'no_reembolsable', 'DE', 'global',
 ARRAY['gobernanza','clima','agua','innovacion_publica'],
 ARRAY['GAD','ONG','academia'],
 50000, 5000000, 'irregular',
 'https://giz.de', true),

('AFD',
 'Agencia Francesa de Desarrollo',
 'bilateral', 'ambas', 'FR', 'AL',
 ARRAY['clima','agua','infraestructura','ciudades'],
 ARRAY['GAD','Estado'],
 100000, 20000000, 'irregular',
 'https://afd.fr', true),

-- ── FUNDACIONES FILANTRÓPICAS ─────────────────────────────────────────────────
('FORD',
 'Ford Foundation',
 'fundacion', 'no_reembolsable', 'US', 'global',
 ARRAY['democracia','derechos_humanos','genero','justicia'],
 ARRAY['ONG','OSC','academia'],
 50000, 500000, 'anual',
 'https://fordfoundation.org', true),

('OSF',
 'Open Society Foundations',
 'fundacion', 'no_reembolsable', 'US', 'global',
 ARRAY['democracia','transparencia','justicia','gobierno_abierto'],
 ARRAY['ONG','OSC','academia'],
 50000, 1000000, 'anual',
 'https://opensocietyfoundations.org', true),

('ROCKEFELLER',
 'Rockefeller Foundation',
 'fundacion', 'no_reembolsable', 'US', 'global',
 ARRAY['clima','salud','alimentacion','innovacion'],
 ARRAY['ONG','academia','GAD'],
 100000, 5000000, 'irregular',
 'https://rockefellerfoundation.org', true),

-- ── GÉNERO ESPECÍFICO ─────────────────────────────────────────────────────────
('GFW',
 'Global Fund for Women',
 'fundacion', 'no_reembolsable', 'US', 'global',
 ARRAY['genero','derechos_humanos','liderazgo'],
 ARRAY['ONG','OSC'],
 5000, 100000, 'continua',
 'https://globalfundforwomen.org', true),

-- ── ACADEMIA ─────────────────────────────────────────────────────────────────
('ERASMUS',
 'Erasmus+',
 'academia', 'no_reembolsable', 'EU', 'global',
 ARRAY['educacion','innovacion','juventud','movilidad'],
 ARRAY['academia','GAD','ONG'],
 20000, 500000, 'anual',
 'https://erasmus-plus.ec.europa.eu', true),

('HORIZON',
 'Horizon Europe',
 'fondo_innovacion', 'no_reembolsable', 'EU', 'global',
 ARRAY['investigacion','innovacion','clima','tecnologia'],
 ARRAY['academia','empresa','ONG'],
 50000, 5000000, 'continua',
 'https://research-and-innovation.ec.europa.eu', true),

-- ── ECUADOR NACIONAL ─────────────────────────────────────────────────────────
('BDE',
 'Banco de Desarrollo del Ecuador',
 'banca_desarrollo', 'reembolsable', 'EC', 'Ecuador',
 ARRAY['agua','infraestructura','vialidad','saneamiento'],
 ARRAY['GAD'],
 200000, 20000000, 'continua',
 'https://bde.fin.ec', true),

('CFN',
 'Corporación Financiera Nacional',
 'banca_desarrollo', 'reembolsable', 'EC', 'Ecuador',
 ARRAY['produccion','emprendimiento','innovacion','agroindustria'],
 ARRAY['empresa','startup'],
 10000, 5000000, 'continua',
 'https://cfn.fin.ec', true),

('AME',
 'Asociación de Municipalidades Ecuatorianas',
 'camara', 'no_reembolsable', 'EC', 'Ecuador',
 ARRAY['gobernanza','fortalecimiento_municipal','cooperacion_horizontal'],
 ARRAY['GAD'],
 5000, 200000, 'irregular',
 'https://ame.gob.ec', true),

-- ── EMPRESA ESG (patrón corporativo) ─────────────────────────────────────────
('HOLCIM_F',
 'Holcim Foundation for Sustainable Construction',
 'empresa_esg', 'no_reembolsable', 'CH', 'global',
 ARRAY['construccion','vivienda','sostenibilidad','innovacion'],
 ARRAY['ONG','academia','GAD'],
 25000, 250000, 'anual',
 'https://holcimfoundation.org', true),

-- ── EMBAJADA (patrón diplomático) ─────────────────────────────────────────────
('EMB_CANADA',
 'Fondo Embajada de Canadá — Ecuador',
 'embajada', 'no_reembolsable', 'CA', 'Ecuador',
 ARRAY['democracia','genero','derechos_humanos','gobernanza'],
 ARRAY['ONG','OSC'],
 5000, 75000, 'anual',
 'https://international.gc.ca/ecuador', true);


-- ============================================================
-- VERIFICACIÓN SEMILLA
-- ============================================================

-- Contar registros sembrados
-- SELECT 'fondos_requisitos' AS tabla, COUNT(*) AS total FROM fondos_requisitos;
-- SELECT 'fondos_emisores'   AS tabla, COUNT(*) AS total FROM fondos_emisores;

-- Verificar cobertura de familias
-- SELECT familia, COUNT(*) FROM fondos_requisitos GROUP BY familia ORDER BY familia;

-- Verificar cobertura de tipos de emisor
-- SELECT tipo_emisor, naturaleza, COUNT(*) FROM fondos_emisores GROUP BY tipo_emisor, naturaleza ORDER BY naturaleza, tipo_emisor;
