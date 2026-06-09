-- ============================================================
-- Migración 003 — /fondos-radar: observabilidad + historial
-- QUIRA Gov · Dylus Lab © 2026
-- ADR-026 §D02.2 · Fetcher Layer
-- ============================================================
-- Tablas nuevas:
--   fondos_fuentes   — salud operativa por fuente (BID, PNUD, AECID…)
--   fondos_historial — auditoría de cambios en convocatorias
-- Prerequisito: migración 002 aplicada (fondos_convocatorias EXISTS)
-- ============================================================

-- ── 1. fondos_fuentes ────────────────────────────────────────────────────────
-- Registro de cada fuente de datos del Fetcher.
-- Permite responder: "¿El BID no publicó nada o el adaptador está roto?"

CREATE TABLE IF NOT EXISTS fondos_fuentes (
    id                       BIGSERIAL    PRIMARY KEY,
    codigo                   TEXT         NOT NULL UNIQUE,
    -- Ejemplos: 'PNUD', 'BID', 'AECID', 'CAF', 'FORD', 'ONU_MUJERES'

    nombre                   TEXT         NOT NULL,
    url_base                 TEXT,
    tipo_fetch               TEXT         NOT NULL DEFAULT 'scraping',
    -- Valores: scraping | api | manual | rss

    activo                   BOOLEAN      NOT NULL DEFAULT TRUE,

    -- Estado del último refresh
    ultimo_refresh           TIMESTAMPTZ,
    estado                   TEXT         NOT NULL DEFAULT 'nunca',
    -- Valores: ok | error | parcial | nunca

    oportunidades_detectadas INTEGER      NOT NULL DEFAULT 0,
    -- Total de convocatorias encontradas en el último refresh

    oportunidades_nuevas     INTEGER      NOT NULL DEFAULT 0,
    -- Convocatorias INSERT (no duplicadas) en el último refresh

    error_msg                TEXT,
    -- Mensaje de error del último refresh (NULL si OK)

    duracion_ms              INTEGER,
    -- Tiempo de ejecución del último refresh en milisegundos

    config_json              JSONB,
    -- Configuración específica del adaptador:
    -- {
    --   "url_search": "...",
    --   "selector_lista": "...",
    --   "paises_filtro": ["Ecuador", "LAC"],
    --   "temas_filtro": ["gobernanza", "genero"],
    --   "max_paginas": 5
    -- }

    created_at               TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at               TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE fondos_fuentes IS
    'Registro de salud operativa por fuente del Fetcher /fondos-radar. '
    'Permite monitorear qué adaptadores funcionan y qué volumen generan. '
    'ADR-026 §D02.2 · Fetcher Layer.';

COMMENT ON COLUMN fondos_fuentes.estado IS
    'ok = refresh exitoso; error = falló completamente; '
    'parcial = algunos items fallaron; nunca = sin ejecución aún.';

-- ── 2. fondos_historial ──────────────────────────────────────────────────────
-- Auditoría inmutable de todos los cambios en convocatorias.
-- Permite inteligencia histórica: ¿cuántos fondos apareció en 2026?
-- ¿Qué emisores son más activos? ¿Cuándo cerró X convocatoria?

CREATE TABLE IF NOT EXISTS fondos_historial (
    id                 BIGSERIAL    PRIMARY KEY,
    convocatoria_id    BIGINT       REFERENCES fondos_convocatorias(id) ON DELETE SET NULL,
    convocatoria_codigo TEXT,
    -- Guardamos el código también por si ON DELETE SET NULL

    evento             TEXT         NOT NULL,
    -- Valores:
    --   creada          — nueva convocatoria INSERT
    --   actualizada     — campo modificado (campo_cambiado especifica cuál)
    --   cerrada         — estado → 'cerrada'
    --   reabierta       — estado vuelve a 'abierta'
    --   monto_cambiado  — monto_min_usd o monto_max_usd cambió
    --   deadline_cambiado — fecha_cierre cambió
    --   detectada_sin_cambio — el fetcher la vio pero ya existía igual

    campo_cambiado     TEXT,
    -- Nombre de columna que cambió (solo para evento='actualizada')

    valor_anterior     TEXT,
    valor_nuevo        TEXT,

    fuente_codigo      TEXT,
    -- Código del adaptador que generó este evento ('PNUD', 'BID', etc.)

    normalizer_confidence NUMERIC(4,3),
    -- Score de confianza del normalizador Haiku (0.000 a 1.000)

    raw_snippet        TEXT,
    -- Fragmento del texto fuente que originó el evento (max 500 chars)

    capturado_en       TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Índices para consultas históricas eficientes
CREATE INDEX IF NOT EXISTS idx_historial_conv
    ON fondos_historial(convocatoria_id, capturado_en DESC);

CREATE INDEX IF NOT EXISTS idx_historial_evento
    ON fondos_historial(evento, capturado_en DESC);

CREATE INDEX IF NOT EXISTS idx_historial_fuente
    ON fondos_historial(fuente_codigo, capturado_en DESC);

COMMENT ON TABLE fondos_historial IS
    'Auditoría inmutable de cambios en convocatorias de fondos. '
    'Fuente de inteligencia histórica: actividad por emisor, '
    'fondos detectados por año, ciclos de apertura/cierre. '
    'ADR-026 §D02.2 · Fetcher Layer.';

-- ── 3. Seed fondos_fuentes (3 adaptadores MVP) ───────────────────────────────

INSERT INTO fondos_fuentes
    (codigo, nombre, url_base, tipo_fetch, estado, config_json)
VALUES
(
  'PNUD',
  'PNUD Ecuador — Programa de las Naciones Unidas para el Desarrollo',
  'https://www.undp.org/es/ecuador',
  'scraping',
  'nunca',
  '{"url_search": "https://www.undp.org/es/ecuador/grants-and-funding",
    "paises_filtro": ["Ecuador"],
    "temas_filtro": ["gobernanza", "genero", "medioambiente", "democracia"],
    "max_paginas": 3}'::jsonb
),
(
  'BID',
  'BID — Banco Interamericano de Desarrollo',
  'https://www.iadb.org',
  'scraping',
  'nunca',
  '{"url_search": "https://www.iadb.org/es/busqueda?keywords=convocatoria+ecuador&type=proyecto",
    "paises_filtro": ["Ecuador"],
    "max_paginas": 5}'::jsonb
),
(
  'AECID',
  'AECID — Agencia Española de Cooperación Internacional para el Desarrollo',
  'https://www.aecid.es',
  'scraping',
  'nunca',
  '{"url_search": "https://www.aecid.es/es/convocatorias",
    "paises_filtro": ["Ecuador", "LAC"],
    "temas_filtro": ["gobernanza", "genero", "agua", "participacion"],
    "max_paginas": 3}'::jsonb
)
ON CONFLICT (codigo) DO NOTHING;

-- ── VERIFICACIÓN ──────────────────────────────────────────────────────────────
-- SELECT codigo, nombre, tipo_fetch, estado FROM fondos_fuentes ORDER BY codigo;
-- SELECT COUNT(*) FROM fondos_historial;
