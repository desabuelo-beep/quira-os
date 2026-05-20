"""
sentinel/parity_engine.py
Motor de Congruencia Institucional — Sprint 2.5C

Verifica la alineación entre las tres capas de QUIRA OS:
  Fuente Operativa      = Supabase (document_uploads + monthly_kpis)
  Memoria Institucional = Obsidian KB (vault .md)
  Motor Analítico       = KPIs históricos + reglas activas

El usuario final ve: Congruencia Institucional / Requiere Validación / Revisión Pendiente
El técnico puede inspeccionar el detalle interno de cada capa.

Dylus Lab © 2026
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from sentinel.db_config import get_connection

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
OBSIDIAN_KB_PATH   = Path(r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi")
EXPECTED_ENTITIES  = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]
EXPECTED_MIN_FILES = 200       # mínimo de notas .md en vault
MAX_DAYS_STALE     = 60        # días sin actualización → warning
REGLAS_ACTIVAS     = 12        # reglas de detección activas (fijas Sprint 2.5C)
LOG_DIR            = Path(__file__).parent / "logs"
LOG_FILE           = LOG_DIR / "congruencia_log.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── STATUS CODES ──────────────────────────────────────────────────────────────
OK      = "ok"
WARNING = "warning"
ERROR   = "error"

_ICONS = {OK: "✓", WARNING: "⚠", ERROR: "✗"}


def _icon(status: str) -> str:
    return _ICONS.get(status, "?")


# ── CAPA 1 — FUENTE OPERATIVA ─────────────────────────────────────────────────
def check_fuente_operativa() -> dict:
    """
    Capa de datos operativos: documentos cargados y KPIs mensuales.
    Técnicamente: Supabase document_uploads + monthly_kpis.
    """
    try:
        conn = get_connection()
        c    = conn.cursor()

        total_uploads = c.execute(
            "SELECT COUNT(*) as n FROM document_uploads"
        ).fetchone()["n"]

        ents_q = c.execute(
            "SELECT DISTINCT entidad FROM document_uploads ORDER BY entidad"
        ).fetchall()
        entidades_cargadas = [r["entidad"] for r in ents_q]

        last_q = c.execute(
            "SELECT MAX(uploaded_at) as ts FROM document_uploads"
        ).fetchone()
        last_ts = (last_q or {}).get("ts")

        kpi_rows = c.execute(
            "SELECT COUNT(*) as n FROM monthly_kpis"
        ).fetchone()["n"]

        last_period_q = c.execute(
            "SELECT MAX(period_year*100 + period_month) as ym FROM monthly_kpis"
        ).fetchone()
        last_ym = (last_period_q or {}).get("ym")

        conn.close()

        days_since = None
        if last_ts:
            try:
                days_since = (datetime.now() - datetime.fromisoformat(last_ts[:19])).days
            except Exception:
                pass

        entidades_faltantes = [e for e in EXPECTED_ENTITIES if e not in entidades_cargadas]
        status, issues = OK, []

        if total_uploads == 0:
            status = ERROR
            issues.append("Sin documentos cargados")
        elif entidades_faltantes:
            status = WARNING
            issues.append(f"Entidades sin datos: {', '.join(entidades_faltantes)}")
        elif days_since is not None and days_since > MAX_DAYS_STALE:
            status = WARNING
            issues.append(f"Último upload hace {days_since} días (máx. {MAX_DAYS_STALE})")

        fecha_display = "Sin datos"
        if last_ts:
            try:
                fecha_display = datetime.fromisoformat(last_ts[:10]).strftime("%d %b %Y")
            except Exception:
                fecha_display = last_ts[:10]

        return {
            "status":              status,
            "icon":                _icon(status),
            "total_uploads":       total_uploads,
            "entidades_cargadas":  entidades_cargadas,
            "entidades_faltantes": entidades_faltantes,
            "kpi_rows":            kpi_rows,
            "last_upload_display": fecha_display,
            "days_since_update":   days_since,
            "last_period":         last_ym,
            "issues":              issues,
        }
    except Exception as e:
        return {
            "status": ERROR, "icon": "✗",
            "total_uploads": 0, "entidades_cargadas": [],
            "entidades_faltantes": EXPECTED_ENTITIES,
            "kpi_rows": 0, "last_upload_display": "Error",
            "days_since_update": None, "last_period": None,
            "issues": [f"Error al consultar base de datos: {str(e)[:80]}"],
        }


# ── CAPA 2 — MEMORIA INSTITUCIONAL ───────────────────────────────────────────
def check_memoria_institucional() -> dict:
    """
    Capa de conocimiento narrativo: vault Obsidian QUIRA KB.
    Técnicamente: sistema de archivos .md en QUIRA_KB_Montecristi.
    """
    KEY_NOTES = [
        "FUENTES_Holding_Operativa.md",
        "CEDULAS_HOLDING_ENE_MAR_2026.md",
        "ALERTA-Holding_Ti_Critico_2026.md",
        "ALERTA-D3_Ejecucion_Critica.md",
    ]
    try:
        if not OBSIDIAN_KB_PATH.exists():
            return {
                "status": ERROR, "icon": "✗",
                "file_count": 0, "last_updated": "No encontrado",
                "days_since": None, "notes_missing": KEY_NOTES,
                "issues": [f"Vault no encontrado: {OBSIDIAN_KB_PATH}"],
            }

        md_files   = list(OBSIDIAN_KB_PATH.rglob("*.md"))
        file_count = len(md_files)

        latest_mtime = max((f.stat().st_mtime for f in md_files), default=0)
        latest_dt    = datetime.fromtimestamp(latest_mtime)
        days_since   = (datetime.now() - latest_dt).days

        all_names     = {f.name for f in md_files}
        notes_missing = [n for n in KEY_NOTES if n not in all_names]

        status, issues = OK, []

        if file_count == 0:
            status = ERROR
            issues.append("Vault vacío o inaccesible")
        elif file_count < EXPECTED_MIN_FILES:
            status = WARNING
            issues.append(f"Solo {file_count} notas (esperadas ≥{EXPECTED_MIN_FILES})")

        if notes_missing:
            if status == OK:
                status = WARNING
            issues.append(f"Notas clave faltantes: {', '.join(notes_missing)}")

        if days_since > MAX_DAYS_STALE and status == OK:
            status = WARNING
            issues.append(f"Sin actualización hace {days_since} días")

        return {
            "status":        status,
            "icon":          _icon(status),
            "file_count":    file_count,
            "last_updated":  latest_dt.strftime("%d %b %Y"),
            "days_since":    days_since,
            "notes_missing": notes_missing,
            "issues":        issues,
        }
    except Exception as e:
        return {
            "status": ERROR, "icon": "✗",
            "file_count": 0, "last_updated": "Error",
            "days_since": None, "notes_missing": KEY_NOTES,
            "issues": [f"Error al leer vault: {str(e)[:80]}"],
        }


# ── CAPA 3 — MOTOR ANALÍTICO ──────────────────────────────────────────────────
def check_motor_analitico() -> dict:
    """
    Capa analítica: KPIs históricos, cobertura de entidades y versiones.
    Técnicamente: monthly_kpis + sentinel_version consistency.
    """
    try:
        conn = get_connection()
        c    = conn.cursor()

        ents_q = c.execute(
            "SELECT DISTINCT entidad FROM monthly_kpis ORDER BY entidad"
        ).fetchall()
        entidades_con_kpis = [r["entidad"] for r in ents_q]

        n_periodos = c.execute(
            "SELECT COUNT(DISTINCT period_year*100 + period_month) as n FROM monthly_kpis"
        ).fetchone()["n"]

        vers_q = c.execute(
            "SELECT DISTINCT sentinel_version FROM monthly_kpis ORDER BY sentinel_version DESC"
        ).fetchall()
        versiones     = [r["sentinel_version"] for r in vers_q]
        version_latest = versiones[0] if versiones else "–"

        pct_cobertura = len(entidades_con_kpis) / len(EXPECTED_ENTITIES) * 100

        conn.close()

        entidades_sin_kpi = [e for e in EXPECTED_ENTITIES if e not in entidades_con_kpis]
        status, issues = OK, []

        if not entidades_con_kpis:
            status = ERROR
            issues.append("Sin KPIs registrados en el motor")
        elif entidades_sin_kpi:
            status = WARNING
            issues.append(f"Sin KPIs: {', '.join(entidades_sin_kpi)}")

        if len(versiones) > 2:
            if status == OK:
                status = WARNING
            issues.append(f"Múltiples versiones: {', '.join(versiones[:3])}")

        return {
            "status":             status,
            "icon":               _icon(status),
            "entidades_con_kpis": entidades_con_kpis,
            "entidades_sin_kpi":  entidades_sin_kpi,
            "n_periodos":         n_periodos,
            "versiones":          versiones,
            "version_latest":     version_latest,
            "pct_cobertura":      round(pct_cobertura, 1),
            "reglas_activas":     REGLAS_ACTIVAS,
            "issues":             issues,
        }
    except Exception as e:
        return {
            "status": ERROR, "icon": "✗",
            "entidades_con_kpis": [], "entidades_sin_kpi": EXPECTED_ENTITIES,
            "n_periodos": 0, "versiones": [], "version_latest": "–",
            "pct_cobertura": 0.0, "reglas_activas": REGLAS_ACTIVAS,
            "issues": [f"Error en motor analítico: {str(e)[:80]}"],
        }


# ── CONGRUENCIA GLOBAL ────────────────────────────────────────────────────────
def get_congruencia_status() -> dict:
    """
    Retorna el estado unificado de congruencia institucional.
    Evalúa las tres capas y agrega en un único resultado.
    """
    fuente  = check_fuente_operativa()
    memoria = check_memoria_institucional()
    motor   = check_motor_analitico()

    capas = [fuente["status"], memoria["status"], motor["status"]]

    if ERROR in capas:
        g_status, g_label, g_color, g_emoji = ERROR, "Revisión Pendiente",     "#FF4D6D", "🔴"
    elif WARNING in capas:
        g_status, g_label, g_color, g_emoji = WARNING, "Requiere Validación",  "#FFB800", "🟡"
    else:
        g_status, g_label, g_color, g_emoji = OK, "Congruencia Institucional", "#00E096", "🟢"

    now = datetime.now()
    result = {
        "global_status":   g_status,
        "global_label":    g_label,
        "global_color":    g_color,
        "global_emoji":    g_emoji,
        "checked_at":      now.isoformat(),
        "checked_display": now.strftime("%d %b %Y, %H:%M"),
        "fuente":          fuente,
        "memoria":         memoria,
        "motor":           motor,
    }
    _log(result)
    return result


# ── LOG HISTÓRICO ─────────────────────────────────────────────────────────────
def _log(result: dict) -> None:
    """Guarda en log JSON rotatorio (últimas 100 entradas). Nunca bloquea el flujo."""
    try:
        existing = []
        if LOG_FILE.exists():
            with open(LOG_FILE, encoding="utf-8") as f:
                existing = json.load(f)
        existing.append({
            "ts":      result.get("checked_at"),
            "status":  result.get("global_status"),
            "label":   result.get("global_label"),
            "fuente":  result["fuente"].get("status"),
            "memoria": result["memoria"].get("status"),
            "motor":   result["motor"].get("status"),
        })
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(existing[-100:], f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_historial_congruencia(limit: int = 20) -> list[dict]:
    """Retorna las últimas N entradas del log de congruencia."""
    try:
        if not LOG_FILE.exists():
            return []
        with open(LOG_FILE, encoding="utf-8") as f:
            data = json.load(f)
        return list(reversed(data[-limit:]))
    except Exception:
        return []
