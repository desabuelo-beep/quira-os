-- ══════════════════════════════════════════════════════════════════════════════
-- QUIRA Intelligence — Supabase RLS Security Fix
-- Proyecto: whogonqaadkkyxcnudth
-- Fecha: 2026-05-27
-- Ejecutar en: Supabase Dashboard → SQL Editor
--
-- EFECTO:
--   Bloquea acceso vía REST API anónimo (anon key) y JWT externo.
--   El backend psycopg2 (supabase_uri en secrets.toml) NO se ve afectado:
--   las conexiones directas PostgreSQL bypasan RLS automáticamente.
--
-- PROCEDIMIENTO:
--   1. Abrir https://supabase.com/dashboard/project/whogonqaadkkyxcnudth
--   2. SQL Editor → New query
--   3. Pegar y ejecutar este script completo
--   4. Ejecutar el bloque VERIFICACIÓN al final
--   5. Confirmar rowsecurity = true en todas las filas
-- ══════════════════════════════════════════════════════════════════════════════

-- ── Habilitar RLS en todas las tablas públicas identificadas ─────────────────

ALTER TABLE document_uploads         ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_execution_lines   ENABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_kpis             ENABLE ROW LEVEL SECURITY;
ALTER TABLE validation_runs          ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts_history           ENABLE ROW LEVEL SECURITY;
ALTER TABLE monthly_snapshots        ENABLE ROW LEVEL SECURITY;
ALTER TABLE resolution_patterns      ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_timeline           ENABLE ROW LEVEL SECURITY;
ALTER TABLE sla_config               ENABLE ROW LEVEL SECURITY;
ALTER TABLE scheduler_log            ENABLE ROW LEVEL SECURITY;
ALTER TABLE municipality_snapshots   ENABLE ROW LEVEL SECURITY;

-- ── Comportamiento resultante ─────────────────────────────────────────────────
--
--   Sin políticas RLS definidas = DENY ALL para anon y authenticated JWT.
--   Esto cierra el vector de ataque reportado por Supabase.
--
--   El backend QUIRA (sentinel, Streamlit, pipeline) conecta via:
--     psycopg2.connect(supabase_uri)   →  rol postgres/superuser
--   Ese rol bypasa RLS sin necesidad de políticas adicionales.
--
--   NO se crean políticas explícitas — QUIRA no usa Supabase client SDK
--   ni autenticación JWT en el frontend. La API REST queda cerrada.
--
-- ── VERIFICACIÓN — ejecutar después del bloque anterior ──────────────────────

SELECT
    tablename,
    rowsecurity,
    CASE WHEN rowsecurity THEN '✓ PROTEGIDA' ELSE '✗ EXPUESTA' END AS estado
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Resultado esperado: rowsecurity = true en todas las tablas QUIRA.
-- Si aparecen tablas con rowsecurity = false que no son de QUIRA,
-- evaluarlas por separado (pueden ser tablas de extensiones de Supabase).
