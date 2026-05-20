"""
QUIRA OS v0.1 — Configuración central
Dylus Lab © 2026
"""
import os

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
