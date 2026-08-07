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


# El pooler de Supabase expone dos puertos y NO son intercambiables:
#   5432 → session mode. Aquí ACEPTA la conexión y la cierra sin responder, y
#          psycopg2 se queda esperando ~20 s antes de rendirse.
#   6543 → transaction mode. Conecta en ~4 s.
# La URI guardada apuntaba a 5432, así que cada consulta costaba 20 segundos y
# fallaba igual: por eso el ambiente de Operaciones tardaba media hora en montar
# —bastaban unas pocas consultas encadenadas—. Se normaliza aquí, en el único
# punto por el que la aplicación abre conexiones, para que un secreto mal
# apuntado no vuelva a colgar la interfaz.
_PUERTO_POOLER = ":6543/"
_PUERTO_SESION = ":5432/"

# Sin esto, una base inalcanzable congela la pantalla en vez de dar un error.
_TIMEOUT_CONEXION = 8


def normalizar_uri(uri: str) -> str:
    """Corrige el puerto del pooler si viene el que no responde.

    Es pública porque **diecinueve archivos abren conexiones sin pasar por
    `get_connection()`** —motores, fetchers y guiones— y todos heredarían el
    mismo cuelgue de veinte segundos. Cualquiera que lea la URI de los secretos
    debe pasarla por aquí antes de conectar."""
    u = str(uri or "")
    if ".pooler.supabase.com" in u and _PUERTO_SESION in u:
        return u.replace(_PUERTO_SESION, _PUERTO_POOLER)
    return u


def _supabase_uri() -> str:
    import streamlit as st
    return normalizar_uri(st.secrets["database"]["supabase_uri"])


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
            self._raw = psycopg2.connect(_supabase_uri(),
                                         connect_timeout=_TIMEOUT_CONEXION)
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
        entidad         TEXT    NOT NULL DEFAULT 'GAD',
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
        entidad         TEXT    NOT NULL DEFAULT 'GAD',
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
    """CREATE TABLE IF NOT EXISTS alerts_history (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        detected_at     TEXT    NOT NULL,
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        entidad         TEXT    NOT NULL,
        tipo            TEXT    NOT NULL,
        status          TEXT    NOT NULL,
        severidad       TEXT    NOT NULL,
        titulo          TEXT    NOT NULL,
        detalle         TEXT,
        accion          TEXT,
        valor           REAL,
        estado          TEXT    NOT NULL DEFAULT 'pendiente',
        resuelta_en     TEXT,
        resuelta_ref    TEXT,
        UNIQUE(period_year, period_month, entidad, tipo)
    )""",
    """CREATE TABLE IF NOT EXISTS monthly_snapshots (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        period_year             INTEGER NOT NULL,
        period_month            INTEGER NOT NULL,
        generated_at            TEXT    NOT NULL,
        triggered_by            TEXT    NOT NULL DEFAULT 'manual',
        congruencia_status      TEXT,
        integridad_status       TEXT,
        integridad_n_ok         INTEGER,
        integridad_n_total      INTEGER,
        alertas_criticas        INTEGER,
        alertas_advertencias    INTEGER,
        alertas_resueltas_mes   INTEGER,
        alertas_dias_max        INTEGER,
        fuente_status           TEXT,
        memoria_status          TEXT,
        motor_status            TEXT,
        notas                   TEXT,
        UNIQUE(period_year, period_month)
    )""",
    """CREATE TABLE IF NOT EXISTS resolution_patterns (
        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
        categoria               TEXT    NOT NULL UNIQUE,
        label_display           TEXT    NOT NULL,
        frecuencia              INTEGER NOT NULL DEFAULT 0,
        tiempo_promedio_dias    REAL    DEFAULT 0,
        entidades_afectadas     TEXT,
        ejemplos                TEXT,
        primera_vez             TEXT,
        ultima_vez              TEXT,
        updated_at              TEXT    NOT NULL
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
        entidad         TEXT    NOT NULL DEFAULT 'GAD',
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
        entidad         TEXT    NOT NULL DEFAULT 'GAD',
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
    """CREATE TABLE IF NOT EXISTS alerts_history (
        id              BIGSERIAL PRIMARY KEY,
        detected_at     TEXT    NOT NULL,
        period_year     INTEGER NOT NULL,
        period_month    INTEGER NOT NULL,
        entidad         TEXT    NOT NULL,
        tipo            TEXT    NOT NULL,
        status          TEXT    NOT NULL,
        severidad       TEXT    NOT NULL,
        titulo          TEXT    NOT NULL,
        detalle         TEXT,
        accion          TEXT,
        valor           REAL,
        estado          TEXT    NOT NULL DEFAULT 'pendiente',
        resuelta_en     TEXT,
        resuelta_ref    TEXT,
        UNIQUE(period_year, period_month, entidad, tipo)
    )""",
    """CREATE TABLE IF NOT EXISTS monthly_snapshots (
        id                      BIGSERIAL PRIMARY KEY,
        period_year             INTEGER NOT NULL,
        period_month            INTEGER NOT NULL,
        generated_at            TEXT    NOT NULL,
        triggered_by            TEXT    NOT NULL DEFAULT 'manual',
        congruencia_status      TEXT,
        integridad_status       TEXT,
        integridad_n_ok         INTEGER,
        integridad_n_total      INTEGER,
        alertas_criticas        INTEGER,
        alertas_advertencias    INTEGER,
        alertas_resueltas_mes   INTEGER,
        alertas_dias_max        INTEGER,
        fuente_status           TEXT,
        memoria_status          TEXT,
        motor_status            TEXT,
        notas                   TEXT,
        UNIQUE(period_year, period_month)
    )""",
    """CREATE TABLE IF NOT EXISTS resolution_patterns (
        id                      BIGSERIAL PRIMARY KEY,
        categoria               TEXT    NOT NULL UNIQUE,
        label_display           TEXT    NOT NULL,
        frecuencia              INTEGER NOT NULL DEFAULT 0,
        tiempo_promedio_dias    REAL    DEFAULT 0,
        entidades_afectadas     TEXT,
        ejemplos                TEXT,
        primera_vez             TEXT,
        ultima_vez              TEXT,
        updated_at              TEXT    NOT NULL
    )""",
]

_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_uploads_period  ON document_uploads(period_year, period_month)",
    "CREATE INDEX IF NOT EXISTS idx_lines_upload    ON budget_execution_lines(upload_id)",
    "CREATE INDEX IF NOT EXISTS idx_kpis_period     ON monthly_kpis(period_year, period_month)",
    "CREATE INDEX IF NOT EXISTS idx_alerts_period   ON alerts_history(period_year, period_month)",
    "CREATE INDEX IF NOT EXISTS idx_alerts_entidad  ON alerts_history(entidad, estado)",
    "CREATE INDEX IF NOT EXISTS idx_snapshots_period ON monthly_snapshots(period_year, period_month)",
]


def _migrate_alerts_history(conn: "DbConn") -> None:
    """
    Crea alerts_history si no existe (instancias previas al Sprint 2.6.1).
    Idempotente.
    """
    c = conn.cursor()
    if conn.mode == "supabase":
        stmt = """CREATE TABLE IF NOT EXISTS alerts_history (
            id              BIGSERIAL PRIMARY KEY,
            detected_at     TEXT    NOT NULL,
            period_year     INTEGER NOT NULL,
            period_month    INTEGER NOT NULL,
            entidad         TEXT    NOT NULL,
            tipo            TEXT    NOT NULL,
            status          TEXT    NOT NULL,
            severidad       TEXT    NOT NULL,
            titulo          TEXT    NOT NULL,
            detalle         TEXT,
            accion          TEXT,
            valor           REAL,
            estado          TEXT    NOT NULL DEFAULT 'pendiente',
            resuelta_en     TEXT,
            resuelta_ref    TEXT,
            UNIQUE(period_year, period_month, entidad, tipo)
        )"""
    else:
        stmt = """CREATE TABLE IF NOT EXISTS alerts_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            detected_at     TEXT    NOT NULL,
            period_year     INTEGER NOT NULL,
            period_month    INTEGER NOT NULL,
            entidad         TEXT    NOT NULL,
            tipo            TEXT    NOT NULL,
            status          TEXT    NOT NULL,
            severidad       TEXT    NOT NULL,
            titulo          TEXT    NOT NULL,
            detalle         TEXT,
            accion          TEXT,
            valor           REAL,
            estado          TEXT    NOT NULL DEFAULT 'pendiente',
            resuelta_en     TEXT,
            resuelta_ref    TEXT,
            UNIQUE(period_year, period_month, entidad, tipo)
        )"""
    try:
        c.execute(stmt)
        conn.commit()
    except Exception:
        pass


def _migrate_monthly_snapshots(conn: "DbConn") -> None:
    """Crea monthly_snapshots si no existe. Idempotente."""
    c    = conn.cursor()
    pk   = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        c.execute(f"""CREATE TABLE IF NOT EXISTS monthly_snapshots (
            id                      {pk} PRIMARY KEY {auto},
            period_year             INTEGER NOT NULL,
            period_month            INTEGER NOT NULL,
            generated_at            TEXT    NOT NULL,
            triggered_by            TEXT    NOT NULL DEFAULT 'manual',
            congruencia_status      TEXT,
            integridad_status       TEXT,
            integridad_n_ok         INTEGER,
            integridad_n_total      INTEGER,
            alertas_criticas        INTEGER,
            alertas_advertencias    INTEGER,
            alertas_resueltas_mes   INTEGER,
            alertas_dias_max        INTEGER,
            fuente_status           TEXT,
            memoria_status          TEXT,
            motor_status            TEXT,
            notas                   TEXT,
            UNIQUE(period_year, period_month)
        )""")
        conn.commit()
    except Exception:
        pass


def _migrate_alerts_v2(conn: "DbConn") -> None:
    """
    Añade columnas extendidas a alerts_history (Sprint 2.6.1 v2).
    Idempotente — cada ALTER TABLE va en su propio try/except.
    """
    c = conn.cursor()
    cols = [
        ("hash_alerta",      "TEXT"),
        ("umbral",           "REAL"),
        ("fuente_datos",     "TEXT"),
        ("rol_que_consume",  "TEXT DEFAULT 'ANALISTA'"),
        ("resolucion",       "TEXT"),
    ]
    for col, typedef in cols:
        try:
            if conn.mode == "supabase":
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN IF NOT EXISTS {col} {typedef}")
            else:
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN {col} {typedef}")
        except Exception:
            pass  # columna ya existe
    conn.commit()


def _migrate_entidad(conn: "DbConn") -> None:
    """
    Migración incremental: añade columna 'entidad' a tablas existentes.
    Idempotente — si la columna ya existe no falla.
    """
    c = conn.cursor()
    for table in ("document_uploads", "monthly_kpis"):
        try:
            if conn.mode == "supabase":
                c.execute(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS entidad TEXT NOT NULL DEFAULT 'GAD'")
            else:
                c.execute(f"ALTER TABLE {table} ADD COLUMN entidad TEXT NOT NULL DEFAULT 'GAD'")
        except Exception:
            pass  # Columna ya existe — ignorar
    conn.commit()


def _migrate_ownership_fields(conn: "DbConn") -> None:
    """Añade columnas de ownership/escalamiento a alerts_history (Sprint 2.9A). Idempotente."""
    c    = conn.cursor()
    cols = [
        ("owner_actual",       "TEXT"),
        ("owner_anterior",     "TEXT"),
        ("fecha_asignacion",   "TEXT"),
        ("escalada",           "INTEGER DEFAULT 0"),
        ("nivel_escalamiento", "TEXT"),
    ]
    for col, typedef in cols:
        try:
            if conn.mode == "supabase":
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN IF NOT EXISTS {col} {typedef}")
            else:
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN {col} {typedef}")
        except Exception:
            pass
    conn.commit()


def _migrate_alert_timeline(conn: "DbConn") -> None:
    """Crea tabla alert_timeline — bitácora inmutable de eventos (Sprint 2.9A). Idempotente."""
    pk   = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        conn.cursor().execute(f"""CREATE TABLE IF NOT EXISTS alert_timeline (
            id           {pk} PRIMARY KEY {auto},
            alert_id     INTEGER NOT NULL,
            timestamp    TEXT    NOT NULL,
            actor        TEXT    NOT NULL DEFAULT 'sistema',
            evento       TEXT    NOT NULL,
            estado_desde TEXT,
            estado_hasta TEXT,
            nota         TEXT,
            nivel        TEXT    NOT NULL DEFAULT 'analista'
        )""")
        conn.commit()
    except Exception:
        pass
    try:
        conn.cursor().execute(
            "CREATE INDEX IF NOT EXISTS idx_timeline_alert ON alert_timeline(alert_id)"
        )
        conn.commit()
    except Exception:
        pass


def _migrate_suggestion_fields(conn: "DbConn") -> None:
    """
    Añade columnas de trazabilidad de sugerencias a alerts_history (Sprint 2.8C).
    Idempotente — cada ALTER va en su propio try/except.
    """
    c    = conn.cursor()
    cols = [
        ("suggestion_used",       "INTEGER DEFAULT 0"),
        ("suggestion_category",   "TEXT"),
        ("suggestion_confidence", "REAL"),
        ("edited_before_submit",  "INTEGER DEFAULT 0"),
    ]
    for col, typedef in cols:
        try:
            if conn.mode == "supabase":
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN IF NOT EXISTS {col} {typedef}")
            else:
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN {col} {typedef}")
        except Exception:
            pass  # columna ya existe
    conn.commit()


def _migrate_sla_config(conn: "DbConn") -> None:
    """
    Crea tabla sla_config e inserta configuración institucional por defecto.
    RC-2A — SLA Institucional. Idempotente.
    """
    c   = conn.cursor()
    pk  = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        c.execute(f"""CREATE TABLE IF NOT EXISTS sla_config (
            id           {pk} PRIMARY KEY {auto},
            entidad      TEXT    NOT NULL DEFAULT '*',
            severidad    TEXT    NOT NULL,
            target_hours INTEGER NOT NULL,
            descripcion  TEXT,
            activo       BOOLEAN NOT NULL DEFAULT TRUE,
            created_at   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(entidad, severidad)
        )""")
        conn.commit()
    except Exception:
        pass
    # Insertar configuración por defecto (idempotente)
    defaults = [
        ("*", "CRITICA",     48,  "SLA global alertas criticas — 48 horas"),
        ("*", "ADVERTENCIA", 120, "SLA global advertencias institucionales — 120 horas"),
    ]
    for entidad, severidad, hours, desc in defaults:
        try:
            if conn.mode == "supabase":
                c.execute(
                    "INSERT INTO sla_config (entidad, severidad, target_hours, descripcion) "
                    "VALUES (%s, %s, %s, %s) ON CONFLICT (entidad, severidad) DO NOTHING",
                    (entidad, severidad, hours, desc),
                )
            else:
                c.execute(
                    "INSERT OR IGNORE INTO sla_config "
                    "(entidad, severidad, target_hours, descripcion) VALUES (?, ?, ?, ?)",
                    (entidad, severidad, hours, desc),
                )
        except Exception:
            pass
    try:
        conn.commit()
    except Exception:
        pass


def _migrate_sla_fields(conn: "DbConn") -> None:
    """
    Añade columnas SLA a alerts_history (RC-2A). Idempotente.
    Columnas: sla_target_hours, sla_due_at, sla_status, sla_breach_reason.
    """
    c    = conn.cursor()
    cols = [
        ("sla_target_hours", "INTEGER"),
        ("sla_due_at",       "TEXT"),
        ("sla_status",       "TEXT DEFAULT 'EN_TIEMPO'"),
        ("sla_breach_reason","TEXT"),
    ]
    for col, typedef in cols:
        try:
            if conn.mode == "supabase":
                c.execute(
                    f"ALTER TABLE alerts_history ADD COLUMN IF NOT EXISTS {col} {typedef}"
                )
            else:
                c.execute(f"ALTER TABLE alerts_history ADD COLUMN {col} {typedef}")
        except Exception:
            pass  # columna ya existe
    try:
        conn.commit()
    except Exception:
        pass


def _migrate_resolution_patterns(conn: "DbConn") -> None:
    """Crea resolution_patterns si no existe (instancias previas al Sprint 2.8A). Idempotente."""
    c   = conn.cursor()
    pk  = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        c.execute(f"""CREATE TABLE IF NOT EXISTS resolution_patterns (
            id                      {pk} PRIMARY KEY {auto},
            categoria               TEXT    NOT NULL UNIQUE,
            label_display           TEXT    NOT NULL,
            frecuencia              INTEGER NOT NULL DEFAULT 0,
            tiempo_promedio_dias    REAL    DEFAULT 0,
            entidades_afectadas     TEXT,
            ejemplos                TEXT,
            primera_vez             TEXT,
            ultima_vez              TEXT,
            updated_at              TEXT    NOT NULL
        )""")
        conn.commit()
    except Exception:
        pass


def _migrate_scheduler_log(conn: "DbConn") -> None:
    """
    Crea tabla scheduler_log para el scheduler institucional (RC-2B).
    Registra última ejecución, estado y resultado de cada tarea programada.
    Idempotente.
    """
    pk   = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        conn.cursor().execute(f"""CREATE TABLE IF NOT EXISTS scheduler_log (
            id          {pk} PRIMARY KEY {auto},
            task_name   TEXT NOT NULL UNIQUE,
            last_run    TEXT,
            status      TEXT NOT NULL DEFAULT 'PENDING',
            result_msg  TEXT,
            runs_total  INTEGER NOT NULL DEFAULT 0
        )""")
        conn.commit()
    except Exception:
        pass


def _migrate_sercop_contratos(conn: "DbConn") -> None:
    """
    Crea tabla sercop_contratos — ingesta OCDS API SERCOP por entidad.
    Sprint 0: Contratación pública verificada 2023-2026 para las 5 entidades del Holding.
    Idempotente.
    """
    pk   = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        conn.cursor().execute(f"""CREATE TABLE IF NOT EXISTS sercop_contratos (
            id                  {pk} PRIMARY KEY {auto},
            -- Identificación del proceso
            sercop_id           INTEGER,
            ocid                TEXT    NOT NULL,
            -- Entidad del Holding
            entidad_codigo      TEXT    NOT NULL,
            entidad_nombre      TEXT    NOT NULL,
            entidad_ruc         TEXT,
            -- Datos del proceso
            anio                INTEGER NOT NULL,
            mes                 INTEGER,
            tipo_contratacion   TEXT,
            tipo_metodo         TEXT,
            estado              TEXT,
            -- Montos
            monto_presupuestado REAL    DEFAULT 0,
            monto_adjudicado    REAL    DEFAULT 0,
            -- Descripción
            titulo              TEXT,
            descripcion         TEXT,
            proveedor           TEXT,
            localidad           TEXT,
            -- Fechas
            fecha_publicacion   TEXT,
            -- Trazabilidad
            url_proceso         TEXT,
            fecha_ingesta       TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
            fuente              TEXT    NOT NULL DEFAULT 'SERCOP_OCDS_API',
            UNIQUE(ocid)
        )""")
        conn.commit()
    except Exception:
        pass
    # Índices para queries frecuentes
    for idx_sql in [
        "CREATE INDEX IF NOT EXISTS idx_sercop_entidad ON sercop_contratos(entidad_codigo)",
        "CREATE INDEX IF NOT EXISTS idx_sercop_anio    ON sercop_contratos(anio)",
        "CREATE INDEX IF NOT EXISTS idx_sercop_tipo    ON sercop_contratos(tipo_contratacion)",
    ]:
        try:
            conn.cursor().execute(idx_sql)
            conn.commit()
        except Exception:
            pass


def _migrate_municipality_snapshots(conn: "DbConn") -> None:
    """
    Crea municipality_snapshots — tabla maestra de snapshots por municipio.
    Sprint RC-CARGA · Idempotente.

    Permite subir gm_snapshot.json desde el browser y que el app lo lea desde
    Supabase en lugar del archivo JSON estático del repo. Multi-municipio ready.
    """
    pk   = "BIGSERIAL" if conn.mode == "supabase" else "INTEGER"
    auto = "" if conn.mode == "supabase" else "AUTOINCREMENT"
    try:
        conn.cursor().execute(f"""CREATE TABLE IF NOT EXISTS municipality_snapshots (
            id              {pk} PRIMARY KEY {auto},
            municipio_code  TEXT    NOT NULL,
            municipio_name  TEXT    NOT NULL,
            version         TEXT    NOT NULL,
            fecha_corte     TEXT    NOT NULL,
            uploaded_at     TEXT    NOT NULL,
            uploaded_by     TEXT    NOT NULL DEFAULT 'sistema',
            is_active       BOOLEAN NOT NULL DEFAULT TRUE,
            snapshot_json   TEXT    NOT NULL,
            checksum_sha256 TEXT,
            notas           TEXT,
            UNIQUE(municipio_code, version)
        )""")
        conn.commit()
    except Exception:
        pass


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

    # Migración incremental: entidad (Sprint 2.5B)
    _migrate_entidad(conn)

    # Migración incremental: alerts_history (Sprint 2.6.1)
    _migrate_alerts_history(conn)

    # Migración incremental: alerts_history v2 — campos extendidos
    _migrate_alerts_v2(conn)

    # Migración incremental: monthly_snapshots (Sprint 2.7)
    _migrate_monthly_snapshots(conn)

    # Migración incremental: resolution_patterns (Sprint 2.8A)
    _migrate_resolution_patterns(conn)

    # Migración incremental: trazabilidad sugerencias (Sprint 2.8C)
    _migrate_suggestion_fields(conn)

    # Migración incremental: ownership + timeline (Sprint 2.9A)
    _migrate_ownership_fields(conn)
    _migrate_alert_timeline(conn)

    # Migración incremental: SLA institucional (RC-2A)
    _migrate_sla_config(conn)
    _migrate_sla_fields(conn)

    # Migración incremental: Scheduler institucional (RC-2B)
    _migrate_scheduler_log(conn)

    # Migración incremental: Snapshots de municipios (RC-CARGA)
    _migrate_municipality_snapshots(conn)

    # Migración incremental: SERCOP contratación pública (Sprint 0)
    _migrate_sercop_contratos(conn)

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
# SOLO en SQLite. Contra Supabase esto ejecutaba las trece migraciones en cada
# arranque —y por ser código a nivel de módulo, con solo IMPORTAR el archivo—:
# 51 segundos antes de que la aplicación mostrara nada. Con la URI apuntando al
# puerto equivocado, cada migración sumaba además sus 20 segundos de conexión
# fallida, y el ambiente de Operaciones tardaba media hora en abrir.
#
# En SQLite el init es local y cuesta milisegundos, así que se conserva: es lo
# que permite que un clon nuevo del repositorio funcione sin preparar nada.
#
# Contra Supabase el esquema ya existe y migrar es una operación DELIBERADA, no
# algo que deba ocurrir al abrir una pantalla. Cuando haya que aplicar una
# migración nueva se llama `init_db()` explícitamente.
try:
    if _db_mode() != "supabase":
        init_db()
except Exception:
    pass   # Un fallo de esquema local no puede impedir el arranque.
