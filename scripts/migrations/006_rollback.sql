-- ROLLBACK MIGRACIÓN 006 — origen_oportunidad
DROP INDEX IF EXISTS idx_conv_origen;
ALTER TABLE fondos_convocatorias DROP COLUMN IF EXISTS origen_oportunidad;
