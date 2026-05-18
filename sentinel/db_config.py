"""
sentinel/db_config.py
Configuración de base de datos — Sprint 2.5A

Hoy: SQLite local (sentinel/data/sentinel.db)
Futuro: Supabase — cambiar solo el get_connection()

Para migrar a Supabase:
  1. pip install supabase
  2. Reemplazar get_connection() con cliente Supabase
  3. Adaptar _execute() para usar supabase.table().insert()
  Todo lo demás queda igual.

Dylus Lab © 2026
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

# ── RUTA BASE DE DATOS ─────────────────────────────────────────────────────────
DB_DIR  = Path(__file__).parent / "data"
DB_PATH = DB_DIR / "sentinel.db"

DB_DIR.mkdir(parents=True, exist_ok=True)

# ── VERSION DEL ESQUEMA ───────────────────────────────────────────────────────
SCHEMA_VERSION = "1.0.0"


def get_connection() -> sqlite3.Connection:
    """Retorna conexión SQLite con row_factory para acceso por nombre de columna."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # concurrencia básica
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Inicializa el esquema completo si no existe. Idempotente."""
    conn = get_connection()
    c    = conn.cursor()

    # ── Tabla 1: document_uploads (evidencia documental) ──────────────────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS document_uploads (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type   TEXT    NOT NULL,   -- CEDULA | POA | PAC | PDOT | LOTAIP | SERCOP
        period_year     INTEGER NOT NULL,   -- 2026
        period_month    INTEGER,            -- 1-12 (NULL para baseline anual)
        version         INTEGER NOT NULL DEFAULT 1,
        file_name       TEXT    NOT NULL,
        sha256          TEXT    NOT NULL,
        size_bytes      INTEGER NOT NULL,
        uploaded_by     TEXT    NOT NULL DEFAULT 'analista',
        uploaded_at     TEXT    NOT NULL,   -- ISO timestamp
        validation_status TEXT  NOT NULL DEFAULT 'PENDIENTE',  -- OK | ERROR | PENDIENTE
        validation_notes  TEXT,
        notes           TEXT,
        sentinel_version TEXT   NOT NULL DEFAULT '2.5.0'
    )""")

    # ── Tabla 2: budget_execution_lines (toda la cédula) ──────────────────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS budget_execution_lines (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id       INTEGER NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        -- Clasificación presupuestaria
        unidad_codigo   TEXT,
        unidad_nombre   TEXT,
        programa        TEXT,
        subprograma     TEXT,
        proyecto        TEXT,
        partida         TEXT,
        descripcion     TEXT,
        -- Valores presupuestarios (USD)
        codificado      REAL    DEFAULT 0,
        reformas        REAL    DEFAULT 0,
        vigente         REAL    DEFAULT 0,
        comprometido    REAL    DEFAULT 0,
        devengado       REAL    DEFAULT 0,
        pagado          REAL    DEFAULT 0,
        saldo           REAL    DEFAULT 0,
        pct_ejecucion   REAL    DEFAULT 0,   -- devengado/vigente × 100
        -- Clasificación QUIRA
        grupo_gasto     TEXT,   -- "7" = inversión, "8" = inversión, "5" = corriente
        es_inversion    INTEGER DEFAULT 0,   -- 1 si grupo 7 u 8
        created_at      TEXT    NOT NULL
    )""")

    # ── Tabla 3: monthly_kpis (indicadores calculados por mes) ────────────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS monthly_kpis (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id       INTEGER NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        -- TGI Dimensions (calculadas desde la cédula)
        d3_ejecucion    REAL,   -- Ti = devengado_inv / codificado_inv × 100
        d3_source       TEXT,   -- 'cedula_mensual'
        -- IRS calculado
        irs_valor       REAL,
        -- Presupuesto resumen
        codificado_total   REAL,
        devengado_total    REAL,
        devengado_inv      REAL,   -- solo grupos 7+8
        codificado_inv     REAL,   -- solo grupos 7+8
        ti_mensual_pct     REAL,   -- Ti este mes
        ti_acumulado_pct   REAL,   -- Ti acumulado en el año
        -- Metadata
        calculated_at   TEXT    NOT NULL,
        sentinel_version TEXT   NOT NULL DEFAULT '2.5.0'
    )""")

    # ── Tabla 4: validation_runs (comparación Excel canónico vs DB) ───────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS validation_runs (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id       INTEGER NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        -- Comparación D3
        d3_source_excel REAL,   -- valor del Gold Master / snapshot
        d3_source_db    REAL,   -- valor calculado desde la cédula en DB
        d3_variance_pct REAL,   -- diferencia absoluta en puntos porcentuales
        d3_status       TEXT,   -- OK | ALERTA | ERROR (>2pp = ALERTA, >5pp = ERROR)
        -- Resultado global
        overall_status  TEXT    NOT NULL DEFAULT 'PENDIENTE',
        notes           TEXT,
        run_at          TEXT    NOT NULL
    )""")

    # ── Índices para consultas rápidas ────────────────────────────────────────
    c.execute("CREATE INDEX IF NOT EXISTS idx_uploads_period ON document_uploads(period_year, period_month)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_lines_upload   ON budget_execution_lines(upload_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_kpis_period    ON monthly_kpis(period_year, period_month)")

    conn.commit()
    conn.close()


def db_info() -> dict:
    """Retorna info básica de la base de datos para diagnóstico."""
    try:
        conn = get_connection()
        c    = conn.cursor()
        info = {
            "db_path":    str(DB_PATH),
            "exists":     DB_PATH.exists(),
            "size_kb":    round(DB_PATH.stat().st_size / 1024, 1) if DB_PATH.exists() else 0,
        }
        try:
            info["uploads"]   = c.execute("SELECT COUNT(*) FROM document_uploads").fetchone()[0]
            info["cedulas"]   = c.execute("SELECT COUNT(*) FROM document_uploads WHERE document_type='CEDULA'").fetchone()[0]
            info["kpis_rows"] = c.execute("SELECT COUNT(*) FROM monthly_kpis").fetchone()[0]
        except Exception:
            info["uploads"] = info["cedulas"] = info["kpis_rows"] = 0
        conn.close()
        return info
    except Exception as e:
        return {"error": str(e), "exists": False}


# ── AUTO-INIT ─────────────────────────────────────────────────────────────────
init_db()
