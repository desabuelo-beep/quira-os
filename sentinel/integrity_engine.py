"""
sentinel/integrity_engine.py
Integridad Semántica — Sprint 2.5C.1

Verifica que las tres capas digan LO MISMO sobre 6 KPIs canónicos:
  Motor Analítico  = Supabase monthly_kpis + gm_snapshot.json
  Memoria Inst.    = Obsidian vault .md

KPIs verificados (Marzo 2026):
  1. Ti GAD          — DB vs Obsidian  (±0.05 pp)
  2. Ti Bomberos     — DB vs Obsidian  (±0.05 pp)
  3. Ti EMAI-EP      — DB vs Obsidian  (±0.05 pp)
  4. Ti Patronato    — DB vs Obsidian  (±0.05 pp)
  5. D3 Ejecución    — GM vs Obsidian  (±0.50 pp)
  6. IRS             — GM vs Obsidian  (±1.00)

Salida: 🟢 Integridad Confirmada / 🟡 Diferencias detectadas / 🔴 Inconsistencia crítica

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from sentinel.db_config import get_connection

# ── RUTAS ─────────────────────────────────────────────────────────────────────
OBSIDIAN_KB = Path(r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi")
GM_SNAPSHOT  = Path(__file__).parent.parent / "data" / "gm_snapshot.json"

_CEDULAS_FILE    = OBSIDIAN_KB / "08_EJECUCION" / "CEDULAS_HOLDING_ENE_MAR_2026.md"
_EJECUCION_FILE  = OBSIDIAN_KB / "08_EJECUCION" / "_Índice_Ejecucion.md"
_IRS_FILE        = OBSIDIAN_KB / "00_CORE" / "ALERTA-Regresividad_IRS79.md"

# ── TOLERANCIAS ───────────────────────────────────────────────────────────────
_TOL_TI  = 0.05   # pp
_TOL_D3  = 0.50   # pp
_TOL_IRS = 1.00   # pp

# ── ENTIDAD → SECCIÓN OBSIDIAN ────────────────────────────────────────────────
_ENTITY_SECTION = {
    "GAD":       "GAD Municipal de Montecristi",
    "BOMBEROS":  "Cuerpo de Bomberos Montecristi",
    "EMAI-EP":   "EMAI-EP",
    "PATRONATO": "Patronato Municipal de Amparo Social",
}

OK      = "ok"
WARNING = "warning"
ERROR   = "error"


# ── HELPERS COMPARACIÓN ───────────────────────────────────────────────────────
def _compare(a: Optional[float], b: Optional[float], tolerance: float) -> str:
    """Compara dos valores con tolerancia. None → error."""
    if a is None or b is None:
        return ERROR
    if abs(a - b) <= tolerance:
        return OK
    if abs(a - b) <= tolerance * 4:
        return WARNING
    return ERROR


def _delta(a: Optional[float], b: Optional[float]) -> str:
    if a is None or b is None:
        return "–"
    d = a - b
    sign = "+" if d >= 0 else ""
    return f"{sign}{d:.2f}"


# ── FUENTE: MOTOR ANALÍTICO (DB) ──────────────────────────────────────────────
def _db_ti(entidad: str, year: int, month: int) -> Optional[float]:
    """Obtiene Ti mensual promedio de monthly_kpis para la entidad y período."""
    try:
        conn = get_connection()
        c    = conn.cursor()
        row  = c.execute(
            "SELECT AVG(ti_mensual_pct) as v FROM monthly_kpis "
            "WHERE entidad=? AND period_year=? AND period_month=?",
            (entidad, year, month),
        ).fetchone()
        conn.close()
        val = (row or {}).get("v")
        return round(float(val), 4) if val is not None else None
    except Exception:
        return None


# ── FUENTE: MOTOR ANALÍTICO (gm_snapshot) ────────────────────────────────────
def _gm_value(*keys: str) -> Optional[float]:
    """
    Lee gm_snapshot.json y extrae un valor por ruta de claves.
    Ej: _gm_value("tgi", "d3", "valor") → 59.85
    """
    try:
        with open(GM_SNAPSHOT, encoding="utf-8") as f:
            data = json.load(f)
        node = data
        for k in keys:
            node = node[k]
        return float(node)
    except Exception:
        return None


# ── FUENTE: MEMORIA INSTITUCIONAL (Obsidian) ──────────────────────────────────
def _obsidian_ti(entidad: str, periodo: str = "Marzo 2026") -> Optional[float]:
    """
    Extrae Ti de la sección de la entidad en CEDULAS_HOLDING_ENE_MAR_2026.md.
    Busca la fila del período y extrae el valor **X.XX%** de la columna Ti Inv.
    """
    section_header = _ENTITY_SECTION.get(entidad)
    if not section_header or not _CEDULAS_FILE.exists():
        return None
    try:
        text = _CEDULAS_FILE.read_text(encoding="utf-8")

        # Aislar la sección de la entidad (de su ## hasta el siguiente ##)
        sec_pattern = re.compile(
            rf"##\s+{re.escape(section_header)}.*?(?=\n##\s|\Z)", re.DOTALL
        )
        m_sec = sec_pattern.search(text)
        if not m_sec:
            return None
        section = m_sec.group(0)

        # Buscar fila del período: | Marzo 2026 | ... | **X.XX%** | ...
        row_pattern = re.compile(
            rf"\|\s*{re.escape(periodo)}\s*\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*\*\*(\d+\.?\d*)%\*\*"
        )
        m_row = row_pattern.search(section)
        if not m_row:
            return None
        return float(m_row.group(1))
    except Exception:
        return None


def _obsidian_d3() -> Optional[float]:
    """
    Extrae D3 de la tabla 'Señales del Motor' en _Índice_Ejecucion.md.
    Busca: | **D3 Ejecución Presupuestaria** | **59.85%** | ...
    """
    if not _EJECUCION_FILE.exists():
        return None
    try:
        text = _EJECUCION_FILE.read_text(encoding="utf-8")
        pattern = re.compile(
            r'\*\*D3 Ejecuci[oó]n Presupuestaria\*\*\s*\|\s*\*\*(\d+\.?\d*)%\*\*'
        )
        m = pattern.search(text)
        return float(m.group(1)) if m else None
    except Exception:
        return None


def _obsidian_irs() -> Optional[float]:
    """
    Extrae IRS de ALERTA-Regresividad_IRS79.md.
    Busca: 'Montecristi: IRS = 79.7' o '× 100 = 79.7'
    """
    if not _IRS_FILE.exists():
        return None
    try:
        text = _IRS_FILE.read_text(encoding="utf-8")
        # Patrón primario: "Montecristi: IRS = 79.7"
        m = re.search(r'Montecristi[^:]*:\s*IRS\s*=\s*(\d+\.?\d*)', text)
        if m:
            return float(m.group(1))
        # Patrón alternativo: "× 100 = 79.7"
        m = re.search(r'[×x]\s*100\s*=\s*(\d+\.?\d*)', text)
        return float(m.group(1)) if m else None
    except Exception:
        return None


# ── MOTOR DE INTEGRIDAD ───────────────────────────────────────────────────────
def run_integrity_check() -> dict:
    """
    Ejecuta los 6 checks de integridad semántica.
    Retorna dict con status global, label, emoji, sublabel y lista de checks.
    """
    checks = []

    # ── Ti inversión por entidad (DB vs Obsidian, Marzo 2026) ─────────────────
    for ent in ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]:
        v_db  = _db_ti(ent, 2026, 3)
        v_obs = _obsidian_ti(ent, "Marzo 2026")
        st    = _compare(v_db, v_obs, _TOL_TI)
        checks.append({
            "id":       f"ti_{ent.lower().replace('-', '_')}",
            "label":    f"Ti {ent} · Mar-2026",
            "motor":    v_db,
            "memoria":  v_obs,
            "delta":    _delta(v_db, v_obs),
            "tolerancia": _TOL_TI,
            "status":   st,
            "unit":     "%",
        })

    # ── D3 Ejecución (GM vs Obsidian) ─────────────────────────────────────────
    v_gm_d3  = _gm_value("tgi", "d3", "valor")
    v_obs_d3 = _obsidian_d3()
    st_d3    = _compare(v_gm_d3, v_obs_d3, _TOL_D3)
    checks.append({
        "id":       "d3_ejecucion",
        "label":    "D3 Ejecución Presupuestaria",
        "motor":    v_gm_d3,
        "memoria":  v_obs_d3,
        "delta":    _delta(v_gm_d3, v_obs_d3),
        "tolerancia": _TOL_D3,
        "status":   st_d3,
        "unit":     "%",
    })

    # ── IRS Regresividad (GM vs Obsidian) ─────────────────────────────────────
    v_gm_irs  = _gm_value("tgi", "irs", "valor")
    v_obs_irs = _obsidian_irs()
    st_irs    = _compare(v_gm_irs, v_obs_irs, _TOL_IRS)
    checks.append({
        "id":       "irs_regresividad",
        "label":    "IRS Regresividad Territorial",
        "motor":    v_gm_irs,
        "memoria":  v_obs_irs,
        "delta":    _delta(v_gm_irs, v_obs_irs),
        "tolerancia": _TOL_IRS,
        "status":   st_irs,
        "unit":     "",
    })

    # ── Agregación ────────────────────────────────────────────────────────────
    n_ok      = sum(1 for c in checks if c["status"] == OK)
    n_warning = sum(1 for c in checks if c["status"] == WARNING)
    n_error   = sum(1 for c in checks if c["status"] == ERROR)
    n_total   = len(checks)

    if n_error > 0:
        g_status = ERROR
        g_label  = "Inconsistencia Crítica"
        g_emoji  = "🔴"
        g_sublabel = f"{n_error} indicador{'es' if n_error > 1 else ''} con valores divergentes — bloqueo de recomendaciones activado"
        g_color  = "#FF4D6D"
    elif n_warning > 0:
        g_status = WARNING
        g_label  = "Diferencias Detectadas"
        g_emoji  = "🟡"
        g_sublabel = f"{n_warning} indicador{'es' if n_warning > 1 else ''} requiere{'n' if n_warning > 1 else ''} revisión"
        g_color  = "#FFB800"
    else:
        g_status = OK
        g_label  = "Integridad Confirmada"
        g_emoji  = "🟢"
        g_sublabel = f"{n_ok}/{n_total} indicadores coinciden entre Motor y Memoria Institucional"
        g_color  = "#00E096"

    return {
        "status":    g_status,
        "label":     g_label,
        "emoji":     g_emoji,
        "sublabel":  g_sublabel,
        "color":     g_color,
        "checks":    checks,
        "n_ok":      n_ok,
        "n_warning": n_warning,
        "n_error":   n_error,
        "n_total":   n_total,
    }
