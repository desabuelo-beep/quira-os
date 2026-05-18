"""
sentinel/db_config.py
Configuración de base de datos dual — Sprint 2.5A+

Modo SQLite  (local, sin configuración):
    Activo por defecto cuando secrets.toml no tiene [database] mode="supabase"

Modo Supabase (producción):
    Requiere .streamlit/secrets.toml con:
        [database]
        mode = "supabase"
        supabase_uri = "postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres"

Para migrar: solo cambiar secrets.toml y reiniciar la app. Nada más.

Dylus Lab © 2026
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_VERSION = "1.0.0"

# ── SQLite fallback ────────────────────────────────────────────────────────────
DB_DIR  = Path(__file__).parent / "data"
DB_PATH = DB_DIR / "sentinel.db"
DB_DIR.mkdir(parents=True, exist_ok=True)


# ── DETECCIÓN DE MODO ─────────────────────────────────────────────────────────
def _db_mode() -> str:
    """Lee el modo de .streamlit/secrets.toml. Fallback: sqlite."""
    try:
        import streamlit as st
        return str(st.secrets.get("database", {}).get("mode", "sqlite")).lower()
    except Exception:
        return "sqlite"


def _supabase_uri() -> str:
    import streamlit as st
    return st.secrets["database"]["supabase_uri"]


# ── CURSOR UNIFICADO ──────────────────────────────────────────────────────────
class _Cursor:
    """
    Wrapper que unifica sqlite3 y psycopg2:
      - Convierte marcadores ? → %s para PostgreSQL
      - fetchone() / fetchall() siempre retornan dict (o list[dict])
      - rowcount funciona en ambos backends
    """
    def __init__(self, raw, mode: str):
        self._c   = raw
        self.mode = mode

    def _sql(self, sql: str) -> str:
        """Adapta placeholders SQLite→PostgreSQL si es necesario."""
        return sql.replace("?", "%s") if self.mode == "supabase" else sql

    def execute(self, sql: str, params=()) -> "_Cursor":
        self._c.execute(self._sql(sql), params)
        return self

    def executemany(self, sql: str, seq) -> "_Cursor":
        self._c.executemany(self._sql(sql), seq)
        return self

    def fetchone(self) -> dict | None:
        row = self._c.fetchone()
        if row is None:
            return None
        return dict(row)   # sqlite3.Row y psycopg2.RealDictRow soportan dict()

    def fetchall(self) -> list[dict]:
        return [dict(r) for r in self._c.fetchall()]

    @property
    def rowcount(self) -> int:
        return self._c.rowcount


# ── CONEXIÓN UNIFICADA ────────────────────────────────────────────────────────
class DbConn:
    """
    Conexión unificada SQLite / Supabase-PostgreSQL.

    Uso idéntico en ambos modos:
        conn = get_connection()
        c    = conn.cursor()
        c.execute("SELECT * WHERE id=?", (1,))   # ? funciona en ambos
        rows = c.fetchall()                       # → list[dict] siempre
        conn.commit()
        conn.close()
    """
    def __init__(self):
        self.mode = _db_mode()
        if self.mode == "supabase":
            import psycopg2
            import psycopg2.extras
            self._raw = psycopg2.connect(_supabase_uri())
            self._cf  = psycopg2.extras.RealDictCursor
        else:
            self._raw = sqlite3.connect(DB_PATH)
            self._raw.row_factory = sqlite3.Row
            self._raw.execute("PRAGMA journal_mode=WAL")
            self._raw.execute("PRAGMA foreign_keys=ON")
            self._cf  = None

    def cursor(self) -> _Cursor:
        if self.mode == "supabase":
            return _Cursor(self._raw.cursor(cursor_factory=self._cf), self.mode)
        return _Cursor(self._raw.cursor(), self.mode)

    def execute(self, sql: str, params=()) -> _Cursor:
        c = self.cursor()
        c.execute(sql, params)
        return c

    def commit(self) -> None:
        self._raw.commit()

    def close(self) -> None:
        self._raw.close()


def get_connection() -> DbConn:
    """Retorna conexión activa según el modo configurado en secrets.toml."""
    return DbConn()


# ── ESQUEMAS SQL ──────────────────────────────────────────────────────────────
_SCHEMA_SQLITE = [
    """CREATE TABLE IF NOT EXISTS document_uploads (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type   TEXT    NOT NULL,
        period_year     INTEGER NOT NULL,
        period_month    INTEGER,
        version         INTEGER NOT NULL DEFAULT 1,
        file_name       TEXT    NOT NULL,
        sha256          TEXT    NOT NULL,
        size_bytes      INTEGER NOT NULL,
        uploaded_by     TEXT    NOT NULL DEFAULT 'analista',
        uploaded_at     TEXT    NOT NULL,
        validation_status TEXT  NOT NULL DEFAULT 'PENDIENTE',
        validation_notes  TEXT,
        notes           TEXT,
        sentinel_version TEXT   NOT NULL DEFAULT '2.5.0'
    )""",
    """CREATE TABLE IF NOT EXISTS budget_execution_lines (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id       INTEGER NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        unidad_codigo   TEXT,
        unidad_nombre   TEXT,
        programa        TEXT,
        subprograma     TEXT,
        proyecto        TEXT,
        partida         TEXT,
        descripcion     TEXT,
        codificado      REAL    DEFAULT 0,
        reformas        REAL    DEFAULT 0,
        vigente         REAL    DEFAULT 0,
        comprometido    REAL    DEFAULT 0,
        devengado       REAL    DEFAULT 0,
        pagado          REAL    DEFAULT 0,
        saldo           REAL    DEFAULT 0,
        pct_ejecucion   REAL    DEFAULT 0,
        grupo_gasto     TEXT,
        es_inversion    INTEGER DEFAULT 0,
        created_at      TEXT    NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS monthly_kpis (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id       INTEGER NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        d3_ejecucion    REAL,
        d3_source       TEXT,
        irs_valor       REAL,
        codificado_total   REAL,
        devengado_total    REAL,
        devengado_inv      REAL,
        codificado_inv     REAL,
        ti_mensual_pct     REAL,
        ti_acumulado_pct   REAL,
        calculated_at   TEXT    NOT NULL,
        sentinel_version TEXT   NOT NULL DEFAULT '2.5.0'
    )""",
    """CREATE TABLE IF NOT EXISTS validation_runs (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        upload_id       INTEGER NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        d3_source_excel REAL,
        d3_source_db    REAL,
        d3_variance_pct REAL,
        d3_status       TEXT,
        overall_status  TEXT    NOT NULL DEFAULT 'PENDIENTE',
        notes           TEXT,
        run_at          TEXT    NOT NULL
    )""",
]

_SCHEMA_POSTGRES = [
    """CREATE TABLE IF NOT EXISTS document_uploads (
        id              BIGSERIAL PRIMARY KEY,
        document_type   TEXT    NOT NULL,
        period_year     INTEGER NOT NULL,
        period_month    INTEGER,
        version         INTEGER NOT NULL DEFAULT 1,
        file_name       TEXT    NOT NULL,
        sha256          TEXT    NOT NULL,
        size_bytes      INTEGER NOT NULL,
        uploaded_by     TEXT    NOT NULL DEFAULT 'analista',
        uploaded_at     TEXT    NOT NULL,
        validation_status TEXT  NOT NULL DEFAULT 'PENDIENTE',
        validation_notes  TEXT,
        notes           TEXT,
        sentinel_version TEXT   NOT NULL DEFAULT '2.5.0'
    )""",
    """CREATE TABLE IF NOT EXISTS budget_execution_lines (
        id              BIGSERIAL PRIMARY KEY,
        upload_id       BIGINT  NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        unidad_codigo   TEXT,
        unidad_nombre   TEXT,
        programa        TEXT,
        subprograma     TEXT,
        proyecto        TEXT,
        partida         TEXT,
        descripcion     TEXT,
        codificado      REAL    DEFAULT 0,
        reformas        REAL    DEFAULT 0,
        vigente         REAL    DEFAULT 0,
        comprometido    REAL    DEFAULT 0,
        devengado       REAL    DEFAULT 0,
        pagado          REAL    DEFAULT 0,
        saldo           REAL    DEFAULT 0,
        pct_ejecucion   REAL    DEFAULT 0,
        grupo_gasto     TEXT,
        es_inversion    INTEGER DEFAULT 0,
        created_at      TEXT    NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS monthly_kpis (
        id              BIGSERIAL PRIMARY KEY,
        upload_id       BIGINT  NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        d3_ejecucion    REAL,
        d3_source       TEXT,
        irs_valor       REAL,
        codificado_total   REAL,
        devengado_total    REAL,
        devengado_inv      REAL,
        codificado_inv     REAL,
        ti_mensual_pct     REAL,
        ti_acumulado_pct   REAL,
        calculated_at   TEXT    NOT NULL,
        sentinel_version TEXT   NOT NULL DEFAULT '2.5.0'
    )""",
    """CREATE TABLE IF NOT EXISTS validation_runs (
        id              BIGSERIAL PRIMARY KEY,
        upload_id       BIGINT  NOT NULL REFERENCES document_uploads(id),
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        d3_source_excel REAL,
        d3_source_db    REAL,
        d3_variance_pct REAL,
        d3_status       TEXT,
        overall_status  TEXT    NOT NULL DEFAULT 'PENDIENTE',
        notes           TEXT,
        run_at          TEXT    NOT NULL
    )""",
]

_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_uploads_period ON document_uploads(period_year, period_month)",
    "CREATE INDEX IF NOT EXISTS idx_lines_upload   ON budget_execution_lines(upload_id)",
    "CREATE INDEX IF NOT EXISTS idx_kpis_period    ON monthly_kpis(period_year, period_month)",
]


def init_db() -> None:
    """Inicializa el esquema completo. Idempotente — seguro ejecutar múltiples veces."""
    conn   = get_connection()
    c      = conn.cursor()
    schema = _SCHEMA_POSTGRES if conn.mode == "supabase" else _SCHEMA_SQLITE

    for stmt in schema:
        c.execute(stmt)

    for idx in _INDEXES:
        try:
            c.execute(idx)
        except Exception:
            pass  # Índice ya existe

    conn.commit()
    conn.close()


def db_info() -> dict:
    """Retorna diagnóstico de la base de datos (modo, tamaño, conteos)."""
    try:
        conn = get_connection()
        c    = conn.cursor()
        info = {
            "mode":    conn.mode,
            "db_path": str(DB_PATH) if conn.mode == "sqlite" else "Supabase PostgreSQL",
            "exists":  DB_PATH.exists() if conn.mode == "sqlite" else True,
            "size_kb": round(DB_PATH.stat().st_size / 1024, 1)
                       if (conn.mode == "sqlite" and DB_PATH.exists()) else 0,
        }
        try:
            info["uploads"]   = c.execute("SELECT COUNT(*) as n FROM document_uploads").fetchone()["n"]
            info["cedulas"]   = c.execute(
                "SELECT COUNT(*) as n FROM document_uploads WHERE document_type='CEDULA'"
            ).fetchone()["n"]
            info["kpis_rows"] = c.execute("SELECT COUNT(*) as n FROM monthly_kpis").fetchone()["n"]
        except Exception:
            info["uploads"] = info["cedulas"] = info["kpis_rows"] = 0
        conn.close()
        return info
    except Exception as e:
        return {"error": str(e), "exists": False, "mode": "error"}


# ── AUTO-INIT ─────────────────────────────────────────────────────────────────
try:
    init_db()
except Exception:
    pass   # Fallback: no bloquear el arranque si Supabase no está disponible aún
