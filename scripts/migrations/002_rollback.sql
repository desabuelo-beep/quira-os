-- ============================================================
-- Rollback 002 — fondos_oportunidades
-- QUIRA Gov · Dylus Lab © 2026
-- ADVERTENCIA: elimina todas las tablas Y datos sembrados
-- Ejecutar SOLO si se necesita revertir la migración 002 completa
-- ============================================================

-- Orden inverso de dependencias (FK)
DROP TABLE IF EXISTS fondos_elegibilidad     CASCADE;
DROP TABLE IF EXISTS fondos_conv_requisitos  CASCADE;
DROP TABLE IF EXISTS fondos_convocatorias    CASCADE;
DROP TABLE IF EXISTS fondos_requisitos       CASCADE;
DROP TABLE IF EXISTS fondos_emisores         CASCADE;
