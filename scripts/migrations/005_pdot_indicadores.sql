-- ============================================================================
-- MIGRACIÓN 005 — pdot_indicadores · Operación Minera del PDOT (Sprint B.2)
-- QUIRA OS · Dylus Lab © 2026
--
-- Propósito:
--   Base estructurada de indicadores territoriales extraídos del corpus
--   narrativo PDOT (normativa_corpus) vía extractor LLM (Haiku).
--   Aprobada por mesa (Javo + Colega + Director) 2026-06-10.
--
-- Arquitectura (idéntica hoy y a escala nacional — ADR-024):
--   PDOT → Extractor → pdot_indicadores → GeoTwin → QUIRA Operaciones
--
-- Reglas de Oro respetadas:
--   - NO recalcula el motor: estructura evidencia documental del PDOT.
--   - Trazabilidad total: chunk_id + sha256 del chunk fuente (Regla 3).
--   - RLS habilitado desde el día 1 (lección migración 004).
-- ============================================================================

-- ── TABLA 1: pdot_indicadores ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS pdot_indicadores (
    id              BIGSERIAL PRIMARY KEY,
    canton_id       TEXT        NOT NULL DEFAULT 'MCR-001',
    norma_sigla     TEXT        NOT NULL,
    chunk_id        BIGINT      REFERENCES normativa_corpus(id),
    chunk_sha256    TEXT,
    sistema         TEXT        CHECK (sistema IN (
                        'BIOFISICO', 'SOCIOCULTURAL', 'ECONOMICO_PRODUCTIVO',
                        'ASENTAMIENTOS_HUMANOS', 'MOVILIDAD_ENERGIA_CONECTIVIDAD',
                        'POLITICO_INSTITUCIONAL', 'PUGS', 'OTRO')),
    indicador       TEXT        NOT NULL,
    unidad          TEXT,
    valor_texto     TEXT        NOT NULL,
    valor_num       NUMERIC,
    anio            TEXT,
    territorio      TEXT        NOT NULL DEFAULT 'cantonal',
    fuente_original TEXT,
    pagina_pdot     TEXT,
    confianza       TEXT        NOT NULL DEFAULT 'media'
                                CHECK (confianza IN ('alta', 'media', 'baja')),
    validado        BOOLEAN     NOT NULL DEFAULT FALSE,
    extractor_ver   TEXT        NOT NULL DEFAULT 'v1',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (canton_id, indicador, territorio, anio, valor_texto)
);

COMMENT ON TABLE pdot_indicadores IS
    'Indicadores territoriales extraídos del corpus PDOT vía LLM. '
    'Evidencia documental estructurada — NO métricas del motor. '
    'Sprint B.2 Operación Minera · trazabilidad por chunk.';

CREATE INDEX IF NOT EXISTS idx_pdotind_sistema    ON pdot_indicadores (sistema);
CREATE INDEX IF NOT EXISTS idx_pdotind_territorio ON pdot_indicadores (territorio);
CREATE INDEX IF NOT EXISTS idx_pdotind_canton     ON pdot_indicadores (canton_id);
CREATE INDEX IF NOT EXISTS idx_pdotind_confianza  ON pdot_indicadores (confianza);

-- ── TABLA 2: pdot_extract_log — control de corrida (reanudable) ─────────────
CREATE TABLE IF NOT EXISTS pdot_extract_log (
    chunk_id        BIGINT      PRIMARY KEY REFERENCES normativa_corpus(id),
    norma_sigla     TEXT        NOT NULL,
    chunk_seq       INTEGER,
    n_indicadores   INTEGER     NOT NULL DEFAULT 0,
    status          TEXT        NOT NULL DEFAULT 'ok'
                                CHECK (status IN ('ok', 'error', 'skip', 'vacio')),
    error_msg       TEXT,
    extractor_ver   TEXT        NOT NULL DEFAULT 'v1',
    processed_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE pdot_extract_log IS
    'Log de chunks procesados por el extractor PDOT — permite corridas reanudables.';

-- ── RLS desde el día 1 ──────────────────────────────────────────────────────
ALTER TABLE pdot_indicadores  ENABLE ROW LEVEL SECURITY;
ALTER TABLE pdot_extract_log  ENABLE ROW LEVEL SECURITY;
