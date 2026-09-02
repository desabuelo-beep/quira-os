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

# ── LA FRONTERA ENTRE EL CÓDIGO Y LOS DOCUMENTOS ──────────────────────────────
# Los documentos fuente y el Gold Master viven FUERA del repositorio, y eso es
# deliberado: el repo es privado y los documentos del sujeto observado no se
# suben. Lo que no era deliberado es que esa frontera estuviera **escrita a mano
# en 54 puntos de 49 archivos** (OBS-032, 2026-08-19), incluido este.
#
# Se declara UNA vez y se recibe del entorno. El valor por defecto conserva la
# máquina donde hoy vive el proyecto —nada se rompe— pero deja de ser la única
# posible: en otro equipo o en un servidor basta `QUIRA_DATOS=/ruta/a/los/datos`.
DATOS_DIR = Path(os.environ.get(
    "QUIRA_DATOS",
    r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT"))

# La bóveda de conocimiento territorial vive en OTRA raíz externa, y estaba
# escrita a mano en tres scripts distintos. Misma decisión arquitectónica, mismo
# defecto: replicada en vez de parametrizada (OBS-032).
VAULT_DIR = Path(os.environ.get(
    "QUIRA_VAULT",
    r"C:\Proyectos\QUIRA\knowledge_base\QUIRA_KB_Montecristi"))

# ── MODO CLOUD ────────────────────────────────────────────────────────────────
# En Streamlit Community Cloud no hay Excel local y la app usa `demo_data.py`.
#
# ⚠️ ANTES ESTO PREGUNTABA SI EXISTÍA EL DISCO DE UNA PERSONA (`C:/Users/DELL`).
# Es decir: en cualquier otro ordenador del mundo —incluido un servidor propio—
# QUIRA se declaraba «en la nube» y pasaba a datos de demostración **sin avisar**.
# Un sistema que se degrada en silencio al cambiar de máquina no es portable: es
# una instalación local que finge serlo. Ahora la pregunta es la correcta: ¿están
# los datos donde se declaró que están?
IS_CLOUD = not DATOS_DIR.exists()

# ── PATHS EXCEL (solo relevante en desarrollo local) ──────────────────────────
BASE_EXCEL = str(DATOS_DIR)

# ── GOLD MASTER VIGENTE · SE RESUELVE, NO SE ESCRIBE ──────────────────────────
# Aquí estaba la raíz de D-002 (2026-09-01). Esta puerta fijaba
# `GOLD_MASTER_VERSION = "v5.5_TGI"` a mano, y **once archivos replicaban lo que
# ella declaraba** — enrichers, motores y pipeline—, mientras BOOT declaraba
# v5.7 y `app/connectors/gold_master.py` ya resolvía correctamente por patrón.
# El sistema tenía dos respuestas a «¿cuál es mi Gold Master?» y la mayoría del
# código leía la equivocada.
#
# LA REGLA DE AUTORIDAD, declarada por Javo (2026-09-01):
#
#   > *«debe terminar en TGI para ser tomada por el sistema, y lo que cambia es
#   > 5.6, 5.7, etc. La versión final aprobada es v5.7_TGI.»*
#
# Es decir: **el sufijo `_TGI` marca el slot vivo y el número ordena**. Eso es
# derivable sin intervención humana, que era la pregunta del colega —*«¿puede
# QUIRA demostrar cuál Gold Master es la autoridad vigente y por qué?»*—. Ahora
# sí, y en un solo lugar: duplicar la regla habría reproducido el defecto que la
# creó.
def _resolver_gold_master_vigente() -> "tuple[str, str, bool]":
    """`(version, ruta, resuelto)` del Gold Master vigente.

    Devuelve el histórico si no hay ninguno resoluble — y entonces el sistema
    sigue funcionando con lo que siempre usó, en vez de quedarse sin motor.

    ⚠️ Y DEVUELVE `resuelto=False` CUANDO ESO PASA (2026-09-02). El fallback
    operativo es correcto: la app no debe morir porque el Excel no esté a mano.
    Lo que NO era correcto es que el sistema afirmara `GOLD_MASTER_VERSION =
    "v5.5_TGI"` sin haber encontrado nada — «no lo encontré» convertido en «es
    la v5.5», que es justo lo que este sistema existe para no hacer.

    Lo encontró el primer CI real: en el runner, sin el Excel —vive fuera del
    repositorio—, `test_el_motor_lee_la_version_que_el_canon_declara` falló
    diciendo «el desfase volvió». No había vuelto D-002: el gate estaba
    comparando el canon contra un valor que nadie resolvió.

    Quien necesite saberlo consulta `GOLD_MASTER_RESUELTO`. El fallback sigue
    ahí; lo que ya no hay es la afirmación silenciosa."""
    import re
    historico = ("v5.5_TGI", os.path.join(BASE_EXCEL,
                                          "SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx"),
                 False)
    if not DATOS_DIR.is_dir():
        return historico
    validos = []
    for f in DATOS_DIR.glob("SIAP-ICPI_GOLD_MASTER_v*_TGI.xlsx"):
        # Un respaldo jamás debe volverse canónico por accidente.
        if f.name.startswith(("_", "~$")) or "_FREEZE" in f.name.upper():
            continue
        m = re.search(r"_v(\d+)\.(\d+)_TGI", f.name)
        if m:
            validos.append(((int(m.group(1)), int(m.group(2))), f))
    if not validos:
        return historico
    mayor, ruta = max(validos, key=lambda x: x[0])
    return f"v{mayor[0]}.{mayor[1]}_TGI", str(ruta), True


GOLD_MASTER_VERSION, SIAP_PATH, GOLD_MASTER_RESUELTO = _resolver_gold_master_vigente()
GOLD_MASTER_PATH = SIAP_PATH  # alias explícito para gold_master_governance.py

# Fallback por nombre con fecha (copia de trabajo previa — 2026-05-18)
SIAP_PATH_LEGACY = os.path.join(BASE_EXCEL,
    "Dylus Lab - Sistema de Integridad Algorítmica Predictivo (SIAP-ICPI v1.0)222.xlsx")
SIAP_PATH_ALT = os.path.join(BASE_EXCEL, "quira-data",
    "SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx")

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
PIPELINE_VERSION = "1.0.0-sprint2"
SNAPSHOT_SCHEMA  = "1.0"

# ── Logging ───────────────────────────────────────────────────────────────────
LOG_LEVEL = "INFO"    # consola: DEBUG | INFO | WARNING | ERROR
LOG_DIR   = Path(__file__).parent / "logs"

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
