-- ============================================================
-- Rollback 003 — /fondos-radar
-- QUIRA Gov · Dylus Lab © 2026
-- ============================================================
-- PRECAUCIÓN: elimina todo el historial y las fuentes.
-- Ejecutar solo si es necesario revertir la migración 003.
-- ============================================================

DROP TABLE IF EXISTS fondos_historial CASCADE;
DROP TABLE IF EXISTS fondos_fuentes   CASCADE;
