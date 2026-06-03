-- ============================================================
-- Migration 001 — Schema v2.0: Corpus Semántico Gobernado
-- QUIRA Gov · Dylus Lab © 2026
-- Referencia: ADR-021 · CANONICAL_CHUNK_SCHEMA.md v1.1
-- Fecha: 2026-06-02
-- Autor: Claude (director técnico) + Colega (asesor)
-- ============================================================
-- PROPÓSITO:
--   Transición de "corpus documental plano" a "corpus semántico gobernado"
--   con clasificación ontológica de 4 capas (A/B/C/D) y trazabilidad completa.
--
-- DISEÑO: Star Schema
--   documents       → dimension table (fuente de verdad)
--   normativa_corpus → fact table (chunks con dimensiones denormalizadas)
--
-- SEGURIDAD: todas las columnas nuevas son nullable (no rompe datos existentes)
-- REVERSIBLE: ver 001_rollback.sql
-- ============================================================

-- ── PASO 1: Tabla documents (dimension table) ─────────────────────────────────
-- Una fila por documento. Fuente de verdad para document_class, authority_level.
-- Reclasificar un documento = 1 UPDATE aquí + UPDATE normativa_corpus WHERE sigla=X

CREATE TABLE IF NOT EXISTS documents (
    document_id     SERIAL          PRIMARY KEY,
    norma_sigla     TEXT            UNIQUE NOT NULL,
    norma_nombre    TEXT            NOT NULL,

    -- Clasificación ontológica (ADR-021)
    document_class  TEXT            NOT NULL DEFAULT 'NORMA'
                    CHECK (document_class IN (
                        'NORMA',                     -- Capa A: obliga
                        'METODOLOGIA',               -- Capa B: explica cómo cumplir
                        'INSTRUMENTO_TERRITORIAL',   -- Capa C: planificó/ejecutó
                        'EVIDENCIA_OBSERVACIONAL'    -- Capa D: ciudadanía observó
                    )),

    -- Autoridad epistemológica (10-100)
    authority_level INTEGER         NOT NULL DEFAULT 70
                    CHECK (authority_level BETWEEN 10 AND 100),

    -- Entidad productora (catálogo en CANONICAL_CHUNK_SCHEMA.md §2.3)
    source_entity   TEXT,

    -- Especificidad cantonal (NULL = norma nacional aplicable a todos los GADs)
    canton_id       TEXT            DEFAULT NULL,

    -- Tipo de evidencia (solo Capa D — EVIDENCIA_OBSERVACIONAL)
    evidence_type   TEXT            DEFAULT NULL
                    CHECK (evidence_type IN (
                        'RC_INFORME',     -- Informe Rendición de Cuentas
                        'PP_INFORME',     -- Informe Presupuesto Participativo
                        'EDV',            -- Evidencia Digital Verificable
                        'SIGAD_ICM',      -- Reporte ICM SIGAD
                        'LOTAIP_DATOS'    -- Conjunto datos LOTAIP
                    ) OR evidence_type IS NULL),

    -- Vigencia temporal
    valid_from      DATE            DEFAULT NULL,
    valid_to        DATE            DEFAULT NULL,   -- NULL = vigente

    -- Metadatos heredados de manifest.py (para compatibilidad)
    jerarquia       INTEGER,
    milestone_qlep  TEXT,
    tipo_documento  TEXT,
    archivo_nombre  TEXT,
    vigente         BOOLEAN         DEFAULT TRUE,

    -- Metadatos flexibles
    metadata_json   JSONB           DEFAULT '{}',

    -- Auditoría
    created_at      TIMESTAMPTZ     DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     DEFAULT NOW()
);

COMMENT ON TABLE documents IS
    'Dimension table — fuente de verdad para clasificación ontológica de documentos. '
    'Una fila por documento. Reclasificar un documento = 1 UPDATE aquí. '
    'ADR-021 · CANONICAL_CHUNK_SCHEMA v1.1 · Dylus Lab 2026';

-- ── PASO 2: Índices tabla documents ──────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_documents_class
    ON documents(document_class);

CREATE INDEX IF NOT EXISTS idx_documents_authority
    ON documents(authority_level);

CREATE INDEX IF NOT EXISTS idx_documents_canton
    ON documents(canton_id);

CREATE INDEX IF NOT EXISTS idx_documents_source
    ON documents(source_entity);


-- ── PASO 3: Nuevas columnas en normativa_corpus (fact table) ──────────────────
-- Copia denormalizada de dimensiones para performance de búsqueda vectorial.
-- No requiere JOIN en queries pgvector: WHERE document_class='NORMA' AND authority_level > 80

ALTER TABLE normativa_corpus
    ADD COLUMN IF NOT EXISTS document_id      INTEGER    DEFAULT NULL
        REFERENCES documents(document_id) ON DELETE SET NULL,

    ADD COLUMN IF NOT EXISTS document_class   TEXT       DEFAULT NULL
        CHECK (document_class IN (
            'NORMA','METODOLOGIA',
            'INSTRUMENTO_TERRITORIAL','EVIDENCIA_OBSERVACIONAL'
        )),

    ADD COLUMN IF NOT EXISTS authority_level  INTEGER    DEFAULT NULL
        CHECK (authority_level BETWEEN 10 AND 100),

    ADD COLUMN IF NOT EXISTS source_entity    TEXT       DEFAULT NULL,

    ADD COLUMN IF NOT EXISTS canton_id        TEXT       DEFAULT NULL,

    -- circuit_refs: chunk-level (distintos artículos del mismo doc tocan distintos circuitos)
    -- Ej: COOTAD_266 → ['C01','C02'] · COOTAD_302 → ['C01','C03']
    ADD COLUMN IF NOT EXISTS circuit_refs     TEXT[]     DEFAULT NULL,

    ADD COLUMN IF NOT EXISTS evidence_type    TEXT       DEFAULT NULL
        CHECK (evidence_type IN (
            'RC_INFORME','PP_INFORME','EDV','SIGAD_ICM','LOTAIP_DATOS'
        ) OR evidence_type IS NULL),

    ADD COLUMN IF NOT EXISTS metadata_json    JSONB      DEFAULT '{}';

COMMENT ON COLUMN normativa_corpus.document_id IS
    'FK → documents.document_id. Permite reclasificación centralizada.';

COMMENT ON COLUMN normativa_corpus.document_class IS
    'Copia denormalizada de documents.document_class para performance pgvector.';

COMMENT ON COLUMN normativa_corpus.authority_level IS
    'Copia denormalizada de documents.authority_level. Permite WHERE sin JOIN.';

COMMENT ON COLUMN normativa_corpus.circuit_refs IS
    'Chunk-level: circuitos constitucionales que aplican a ESTE artículo específico. '
    'Puede diferir de otros chunks del mismo documento. '
    'Ej: COOTAD_266 → [C01,C02,C03] vs COOTAD_302 → [C01,C03]';


-- ── PASO 4: Índices normativa_corpus (nuevas columnas) ───────────────────────
CREATE INDEX IF NOT EXISTS idx_corpus_document_id
    ON normativa_corpus(document_id);

CREATE INDEX IF NOT EXISTS idx_corpus_document_class
    ON normativa_corpus(document_class);

CREATE INDEX IF NOT EXISTS idx_corpus_authority_level
    ON normativa_corpus(authority_level);

CREATE INDEX IF NOT EXISTS idx_corpus_canton_id
    ON normativa_corpus(canton_id);

CREATE INDEX IF NOT EXISTS idx_corpus_circuit_refs
    ON normativa_corpus USING GIN(circuit_refs);


-- ── PASO 5: Tabla holding_structured_data (nueva — Gate 6.5) ─────────────────
-- Para archivos XLSX/CSV del Holding (presupuestos mensuales, LOTAIP datasets).
-- NO son chunks semánticos — son datos estructurados tabulares.

CREATE TABLE IF NOT EXISTS holding_structured_data (
    id              BIGSERIAL       PRIMARY KEY,
    source_entity   TEXT            NOT NULL,
    canton_id       TEXT            NOT NULL    DEFAULT 'MCR',
    document_class  TEXT            NOT NULL
                    CHECK (document_class IN (
                        'INSTRUMENTO_TERRITORIAL',
                        'EVIDENCIA_OBSERVACIONAL'
                    )),
    authority_level INTEGER,
    evidence_type   TEXT
                    CHECK (evidence_type IN (
                        'RC_INFORME','PP_INFORME','EDV','SIGAD_ICM','LOTAIP_DATOS'
                    ) OR evidence_type IS NULL),
    periodo         TEXT,               -- '2025-01', '2025-Q1', '2025', etc.
    archivo_nombre  TEXT,
    archivo_sha256  TEXT    UNIQUE,
    datos_json      JSONB,
    ingestado_at    TIMESTAMPTZ     DEFAULT NOW(),
    ingestado_por   TEXT
);

COMMENT ON TABLE holding_structured_data IS
    'Datos tabulares estructurados del Holding Municipal Montecristi. '
    'Presupuestos mensuales, conjuntos de datos LOTAIP Numeral 6. '
    'NO contiene embeddings — no es tabla vectorial. Gate 6.5.';

CREATE INDEX IF NOT EXISTS idx_holding_entity
    ON holding_structured_data(source_entity);

CREATE INDEX IF NOT EXISTS idx_holding_periodo
    ON holding_structured_data(periodo);

CREATE INDEX IF NOT EXISTS idx_holding_class
    ON holding_structured_data(document_class);


-- ── VERIFICACIÓN ──────────────────────────────────────────────────────────────
-- Ejecutar después de aplicar la migración para verificar integridad:
--
-- SELECT table_name, column_name, data_type
-- FROM information_schema.columns
-- WHERE table_name IN ('documents','normativa_corpus','holding_structured_data')
-- AND column_name IN ('document_class','authority_level','circuit_refs','canton_id')
-- ORDER BY table_name, column_name;
--
-- Expected: 8 rows (2 tables × 4 new columns)
-- ============================================================
-- FIN Migration 001
-- ============================================================
