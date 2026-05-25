"""
QUIRA OS — Configuración central
Sprint 1 — Consolidación Base (Junio–Agosto 2026)

Doctrina: QUIRA = infraestructura operativa de observación y validación
territorial. Stack técnico (Streamlit, Supabase, etc.) es reemplazable.
Este config.py abstrae esa reemplazabilidad.

Dylus Lab © 2026
"""
import os
from pathlib import Path

# ── MODO CLOUD ────────────────────────────────────────────────────────────────
# En Streamlit Community Cloud no hay Excel local.
# La app detecta esto automáticamente y usa demo_data.py como fuente de verdad.
IS_CLOUD = not os.path.exists(r"C:\Users\DELL")

# ── PATHS EXCEL (solo relevante en desarrollo local) ──────────────────────────
BASE_EXCEL = r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT"

# Gold Master canónico (v5.5 — 2026-05-18) — fuente de verdad
GOLD_MASTER_VERSION = "v5.5_TGI_20260518"
SIAP_PATH = os.path.join(BASE_EXCEL, "SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.xlsx")

# Nombre legacy del archivo (v4.1 y anteriores) — fallback compatibilidad
SIAP_PATH_LEGACY = os.path.join(BASE_EXCEL,
    "Dylus Lab - Sistema de Integridad Algorítmica Predictivo (SIAP-ICPI v1.0)222.xlsx")
SIAP_PATH_ALT = os.path.join(BASE_EXCEL, "quira-data",
    "SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518.xlsx")

PDOT_PATH = os.path.join(BASE_EXCEL, "PDOT_MONTECRISTI_KB.xlsx")


def get_siap_path() -> str:
    """
    Retorna la ruta del Excel SIAP-ICPI Gold Master.
    Orden de búsqueda: v5.5 canónico → alt → legacy v4.1.
    Lanza FileNotFoundError si ninguno existe → la app usa demo_data.py.
    """
    if os.path.exists(SIAP_PATH):
        return SIAP_PATH
    if os.path.exists(SIAP_PATH_ALT):
        return SIAP_PATH_ALT
    if os.path.exists(SIAP_PATH_LEGACY):
        return SIAP_PATH_LEGACY
    raise FileNotFoundError(
        f"Gold Master no encontrado [{GOLD_MASTER_VERSION}] — modo demo activado."
    )


def get_pdot_path() -> str:
    """
    Retorna la ruta del Excel PDOT_KB.
    Orden de búsqueda:
      1. data/ dentro del repo (cloud + local con copia)
      2. Ruta absoluta local (desarrollo)
    """
    # 1. En el repo (data/PDOT_MONTECRISTI_KB.xlsx) — funciona en cloud y local
    repo_path = os.path.join(os.path.dirname(__file__), "data", "PDOT_MONTECRISTI_KB.xlsx")
    if os.path.exists(repo_path):
        return repo_path
    # 2. Ruta local absoluta (fallback desarrollo sin copia en data/)
    if os.path.exists(PDOT_PATH):
        return PDOT_PATH
    raise FileNotFoundError("PDOT_KB Excel no encontrado — Sentinel operará sin KB territorial.")


# ── IDENTIDAD ─────────────────────────────────────────────────────────────────
APP_NAME    = "QUIRA OS"
APP_VERSION = "v0.1"
GAD_NOMBRE  = "GAD Municipal de Montecristi"
GAD_PERIODO = "2023–2027"
ALCALDE     = "Ing. Jonathan Toro Largacha"
CORTE       = "Q1-2026"

# ── ROLES (sin contraseñas — credenciales viven en models/auth.py + st.secrets) ─
USERS = {
    "alcalde":  {"rol": "Alcalde",  "emoji": "🏛️"},
    "concejal": {"rol": "Concejal", "emoji": "⚖️"},
    "tecnico":  {"rol": "Técnico",  "emoji": "⚙️"},
}

# ── AVEP — ESCALA CANÓNICA (H01_PARÁMETROS) ──────────────────────────────────
AVEP = [
    {"nivel": 5, "min": 0.90, "max": 1.00, "label": "Excelencia en Gobernanza",  "color": "#3182CE", "emoji": "🔵"},
    {"nivel": 4, "min": 0.70, "max": 0.89, "label": "Gestión por Mandato",       "color": "#38A169", "emoji": "🟢"},
    {"nivel": 3, "min": 0.40, "max": 0.69, "label": "Transición Crítica",        "color": "#D69E2E", "emoji": "🟡"},
    {"nivel": 2, "min": 0.20, "max": 0.39, "label": "Gestión por Ocurrencia",    "color": "#E67E22", "emoji": "🟠"},
    {"nivel": 1, "min": 0.00, "max": 0.19, "label": "Ruptura Sistémica",         "color": "#E53E3E", "emoji": "🔴"},
]

# ── COLORES DESIGN SYSTEM ─────────────────────────────────────────────────────
CYAN   = "#00D4FF"
AMBER  = "#FFB700"
GREEN  = "#00E096"
RED    = "#FF4D6D"
PURPLE = "#7C5CFC"
NAVY   = "#0A1628"


# ══════════════════════════════════════════════════════════════════════════════
# SPRINT 1 — Consolidación Base — Configuración Pipeline Territorial
# ══════════════════════════════════════════════════════════════════════════════

# ── Rutas Sprint 1 ────────────────────────────────────────────────────────────
_BASE_DIR      = Path(__file__).parent
DATA_DIR       = _BASE_DIR / "data"
DOCTRINAL_DIR  = DATA_DIR / "doctrinal"    # Gold Master (lectura)
SNAPSHOTS_DIR  = DATA_DIR / "snapshots"    # longitudinalidad
RAW_DIR        = DATA_DIR / "raw"           # CSVs DPE sin procesar
SCOUTING_DIR   = DATA_DIR / "scouting"
REGISTRY_PATH  = DATA_DIR / "municipality_registry.json"

# ── Municipio canónico Sprint 1 ───────────────────────────────────────────────
CANONICAL_MUNICIPIO_CODE = "130801"
CANONICAL_MUNICIPIO_NAME = "GAD Municipal de Montecristi"
CANONICAL_RUC            = "1360000430001"

# ── Versión pipeline ──────────────────────────────────────────────────────────
PIPELINE_VERSION = "1.0.0-sprint1"
SNAPSHOT_SCHEMA  = "1.0"

# ── Doctrina TGI (namespace permanente — NO CAMBIAR) ─────────────────────────
DOCTRINE = {
    "framework":    "TGI Territorial",
    "dimensions":   ["D1", "D2", "D3", "D4", "D5"],
    "sat_enabled":  True,
    "icpi_enabled": True,
    "rc_m_enabled": False,   # Fase 4
    "quira_layer":  "Q1",    # Observación
}

# ── Fuentes habilitadas ───────────────────────────────────────────────────────
ENABLE_DPE    = True
ENABLE_SERCOP = True
ENABLE_CPCCS  = True
ENABLE_SOCIAL = False   # manual — Fase 2

# ── Source Reliability Weights ────────────────────────────────────────────────
SOURCE_RELIABILITY = {
    "dpe":      0.95,
    "sercop":   0.95,
    "cpccs":    0.80,
    "youtube":  0.65,
    "facebook": 0.45,
}

# ── Pipeline weights para TRACEABILITY_SCORE (suma = 1.0) ────────────────────
PIPELINE_WEIGHTS = {
    "dpe":    0.40,
    "sercop": 0.35,
    "cpccs":  0.25,
}

# ── Thresholds SAT (Base Legal: COPFP, LOCP, COOTAD, SERCOP) ─────────────────
SAT_THRESHOLDS = {
    "ejecucion_critica":  0.60,   # COPFP Art. 113 — crítico
    "ejecucion_alerta":   0.75,   # LOCP Art. 92 — alerta
    "cancelados_alerta":  0.15,   # SERCOP — >15% cancelados
    "paralisis_dias":     90,     # SERCOP — parálisis
    "emergencias_alerta": 0.10,   # SERCOP — >10% emergencias
    "rdc_score_minimo":   50,     # CPCCS — RdC parcial mínima
}

# ── URLs APIs externas ────────────────────────────────────────────────────────
DPE_API_BASE    = "https://api.transparencia.dpe.gob.ec/backend/v1"
SERCOP_API_BASE = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/v1"
CPCCS_API_BASE  = "https://rendiciondecuentas.cpccs.gob.ec/api/v1"

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def ensure_sprint1_dirs() -> None:
    """Crea directorios Sprint 1 si no existen."""
    for d in [DOCTRINAL_DIR, SNAPSHOTS_DIR, RAW_DIR, SCOUTING_DIR]:
        d.mkdir(parents=True, exist_ok=True)
