-- ============================================================
-- Migración 004 — Row-Level Security en todas las tablas públicas
-- QUIRA OS · Dylus Lab © 2026
-- ============================================================
-- MOTIVO: Correo Supabase 08-Jun-2026 — "rls_disabled_in_public"
--   Tablas expuestas públicamente via REST API (PostgREST + anon key).
--   Cualquier persona con la project URL podía leer/editar/borrar.
--
-- IMPACTO EN EL APP: NINGUNO
--   El app usa conexión directa PostgreSQL (supabase_uri como postgres).
--   El rol postgres es superuser → bypasea RLS por diseño de PostgreSQL.
--   Solo se bloquea el acceso via REST API con anon key.
--
-- TABLAS PROTEGIDAS (9 tablas, todas en schema public):
--   001: documents              — corpus de normas
--   001: holding_structured_data — datos holding estructurados
--   002: fondos_emisores        — emisores de convocatorias
--   002: fondos_convocatorias   — convocatorias de financiamiento
--   002: fondos_requisitos      — requisitos de elegibilidad
--   002: fondos_conv_requisitos — relación convocatoria-requisito
--   002: fondos_elegibilidad    — resultados del matcher D02
--   003: fondos_fuentes         — salud operativa de fuentes
--   003: fondos_historial       — auditoría inmutable del fetcher
--
-- ROLLBACK: ver 004_rollback.sql
-- ============================================================

-- ── PASO 1: Habilitar RLS en todas las tablas ─────────────────────────────────
ALTER TABLE public.documents               ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.holding_structured_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_emisores         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_convocatorias    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_requisitos       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_conv_requisitos  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_elegibilidad     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_fuentes          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_historial        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.corpus_mnt_mapping      ENABLE ROW LEVEL SECURITY;

-- ── PASO 2: Política de solo lectura para anon (optional, actualmente bloqueado)
-- Las tablas de fondos/emisores son datos de referencia pública (no PII).
-- Si en el futuro se necesita exponer via API pública, descomentar:
--
-- CREATE POLICY "anon_read_fondos_emisores"
--     ON public.fondos_emisores FOR SELECT
--     TO anon USING (true);
--
-- CREATE POLICY "anon_read_fondos_convocatorias"
--     ON public.fondos_convocatorias FOR SELECT
--     TO anon USING (estado = 'abierta');
--
-- CREATE POLICY "anon_read_fondos_elegibilidad"
--     ON public.fondos_elegibilidad FOR SELECT
--     TO anon USING (true);
--
-- POR AHORA: sin políticas = acceso REST API bloqueado para todos los roles
-- excepto postgres (superuser) y service_role (que también bypasean RLS).

-- ── PASO 3: Verificación ──────────────────────────────────────────────────────
-- Ejecutar para confirmar:
--
-- SELECT schemaname, tablename, rowsecurity
-- FROM pg_tables
-- WHERE schemaname = 'public'
-- ORDER BY tablename;
--
-- Resultado esperado: rowsecurity = true para las 9 tablas.

-- ============================================================
-- NOTA DE SEGURIDAD (Bloomberg Model)
-- ============================================================
-- fondos_historial y fondos_elegibilidad contienen referencias a
-- indicadores internos (PSG, ISP) en las columnas de requisitos.
-- Aunque los valores son de gobernanza (no QTMP/TGI), el acceso
-- directo via REST API podría revelar la lógica de elegibilidad.
-- RLS correctamente configurado cierra este vector.
-- ============================================================
