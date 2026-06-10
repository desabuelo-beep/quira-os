-- ============================================================================
-- MIGRACIÓN 006 — origen_oportunidad · Taxonomía de honestidad D02
-- QUIRA OS · Dylus Lab © 2026 · Decisión de mesa (Colega) 2026-06-10
--
-- Bandera OBLIGATORIA para toda oportunidad de financiamiento:
--   SIMULADA  (gris)  → escenario de prueba metodológica del motor
--   VALIDADA  (azul)  → convocatoria real identificada, vigencia pendiente
--   VIGENTE   (verde) → convocatoria real abierta y comprobada
--   CERRADA   (rojo)  → convocatoria real finalizada
--
-- Regla de presentación: SOLO VIGENTE se muestra como oportunidad operativa.
-- SIMULADA se presenta únicamente como "caso de validación del motor".
-- Sin esta bandera, $1.3M de plantillas de prueba parecían pipeline real.
-- ============================================================================

ALTER TABLE fondos_convocatorias
    ADD COLUMN IF NOT EXISTS origen_oportunidad TEXT NOT NULL DEFAULT 'SIMULADA'
    CHECK (origen_oportunidad IN ('SIMULADA', 'VALIDADA', 'VIGENTE', 'CERRADA'));

COMMENT ON COLUMN fondos_convocatorias.origen_oportunidad IS
    'Taxonomía de honestidad D02 (mesa 2026-06-10): SIMULADA=prueba motor · '
    'VALIDADA=real sin verificar vigencia · VIGENTE=real abierta · CERRADA=finalizada. '
    'Solo VIGENTE es oportunidad operativa.';

CREATE INDEX IF NOT EXISTS idx_conv_origen ON fondos_convocatorias (origen_oportunidad);

-- Todo el contenido existente (seed test + fetcher demo) es SIMULADA — el
-- DEFAULT lo aplica automáticamente a las filas existentes.
