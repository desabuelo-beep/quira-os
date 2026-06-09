-- Rollback 004 — Deshabilitar RLS (solo si es absolutamente necesario)
-- ADVERTENCIA: Esto re-expone todas las tablas públicamente.
-- Usar solo para diagnóstico. NO ejecutar en producción.

ALTER TABLE public.documents               DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.holding_structured_data DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_emisores         DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_convocatorias    DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_requisitos       DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_conv_requisitos  DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_elegibilidad     DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_fuentes          DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.fondos_historial        DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.corpus_mnt_mapping      DISABLE ROW LEVEL SECURITY;
