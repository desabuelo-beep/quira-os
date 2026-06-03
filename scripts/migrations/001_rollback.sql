-- ============================================================
-- ROLLBACK Migration 001 — Schema v2.0
-- QUIRA Gov · Dylus Lab © 2026
-- Ejecutar SOLO si la migración falla o se necesita revertir.
-- ============================================================

-- Paso R1: quitar índices nuevos de normativa_corpus
DROP INDEX IF EXISTS idx_corpus_document_id;
DROP INDEX IF EXISTS idx_corpus_document_class;
DROP INDEX IF EXISTS idx_corpus_authority_level;
DROP INDEX IF EXISTS idx_corpus_canton_id;
DROP INDEX IF EXISTS idx_corpus_circuit_refs;

-- Paso R2: quitar columnas nuevas de normativa_corpus
ALTER TABLE normativa_corpus
    DROP COLUMN IF EXISTS document_id,
    DROP COLUMN IF EXISTS document_class,
    DROP COLUMN IF EXISTS authority_level,
    DROP COLUMN IF EXISTS source_entity,
    DROP COLUMN IF EXISTS canton_id,
    DROP COLUMN IF EXISTS circuit_refs,
    DROP COLUMN IF EXISTS evidence_type,
    DROP COLUMN IF EXISTS metadata_json;

-- Paso R3: drop holding_structured_data
DROP TABLE IF EXISTS holding_structured_data CASCADE;

-- Paso R4: drop documents (después de quitar FK en normativa_corpus)
DROP TABLE IF EXISTS documents CASCADE;

-- Verificación:
-- SELECT COUNT(*) FROM normativa_corpus; -- debe seguir igual
-- ============================================================
