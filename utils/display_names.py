"""
utils/display_names.py — QUIRA OS v0.1
Capa de traducción semántica: nombres técnicos internos → lenguaje de administración pública.

DOCTRINA: Todo string técnico visible al ciudadano o al funcionario debe pasar por este módulo.
  - Nunca exponer nombres de hojas Excel (H73, H90, H99, H10c, etc.) en la UI pública.
  - Nunca exponer nombres de archivos internos (SIAP-ICPI_GOLD_MASTER, etc.) en la UI pública.
  - Los acrónimos de indicadores OFICIALES (ICPI, PSG, IET, IGP...) se mantienen con su
    descripción completa disponible a través de INDICATOR_LABELS.

Uso:
    from utils.display_names import tech_to_admin, source_label, INDICATOR_LABELS

Dylus Lab © 2026
"""

# ── 1. Nombres de hojas / módulos internos → lenguaje de administración pública ─────────────────

_TECH_MAP: dict[str, str] = {
    # Archivos / sistema
    "SIAP-ICPI_GOLD_MASTER_v5.5_TGI":          "Sistema de Información Institucional QUIRA v5.5",
    "SIAP-ICPI_GOLD_MASTER_v5.5_TGI_20260518": "Sistema de Información Institucional QUIRA v5.5",
    "SIAP-ICPI_GOLD_MASTER_v4.1":              "Sistema de Información Institucional QUIRA",
    "SIAP-ICPI_GOLD_MASTER":                   "Sistema de Información Institucional QUIRA",
    "SIAP-ICPI":                               "Sistema QUIRA",
    "Gold Master":                             "Sistema de Información Institucional QUIRA",
    "gold_master":                             "Sistema de Información Institucional QUIRA",
    # Módulos / hojas Excel
    "H73_OUTPUT_API":             "Módulo de Ejecución Presupuestaria",
    "H73":                        "Ejecución Presupuestaria",
    "H99_ENGINE_CORE":            "Módulo de Inversión Territorial Parroquial",
    "H99":                        "Inversión Territorial Parroquial",
    "H90_PRESUPUESTO_CONSOLIDADO":"Consolidado del Grupo Municipal",
    "H90":                        "Consolidado del Grupo Municipal",
    "H10c_RDC":                   "Registro Documental Complementario",
    "H10c":                       "Documentación Complementaria",
    "H08_SIGAD":                  "Sistema SIGAD",
    "H08":                        "Sistema SIGAD",
    "H12c_ICPI_HISTÓRICO_ANUAL":  "Histórico de Verificación ICPI (Anual)",
    "H12c_HISTÓRICO":             "Histórico de Verificación ICPI",
    "H12c":                       "Histórico Verificado",
    "H20b":                       "Gestión por Procesos",
    "H24b_SAT-V":                 "Sistema de Alertas Tempranas — Verificado",
    "H24":                        "Alertas Institucionales",
    "H16":                        "Financiamiento Externo",
    "H03b":                       "Clasificador Presupuestario",
    # Fuente/proveedor
    "Dylus Lab":                  "QUIRA Gov",
    # Variables de sistema visibles en UI
    "n_periodos":                 "Períodos analizados",
    "rc73_calibrated":            "Análisis calibrado de ejecución",
    "d4_calibrated":              "Análisis calibrado territorial",
    "d3d4_cross":                 "Análisis cruzado presupuesto-territorio",
    "d1_result":                  "Verificación de legalidad",
    "d13_result":                 "Coherencia normativa PDOT",
    "d5_propagation":             "Propagación de tensiones institucionales",
}


def tech_to_admin(name: str) -> str:
    """Convierte un nombre técnico interno al equivalente en lenguaje de administración pública.

    Si no existe traducción registrada, devuelve el nombre original sin modificación
    (para no romper displays con datos no catalogados aún).

    Args:
        name: Nombre técnico (ej. "H73_OUTPUT_API", "SIAP-ICPI_GOLD_MASTER_v4.1")

    Returns:
        Nombre en lenguaje de administración pública.
    """
    return _TECH_MAP.get(name, name)


def source_label(raw_source: str) -> str:
    """Genera una etiqueta de fuente adecuada para mostrar en la UI.

    Limpia prefijos de versión y sustituye nombres técnicos.
    Ej: "SIAP-ICPI_GOLD_MASTER_v4.1 (H73)" → "Sistema de Información Institucional QUIRA"

    Args:
        raw_source: String de fuente tal como aparece en el código (puede ser compuesto).

    Returns:
        Etiqueta limpia para mostrar al funcionario.
    """
    # Buscar match exacto primero
    if raw_source in _TECH_MAP:
        return _TECH_MAP[raw_source]
    # Buscar match parcial (el raw_source puede contener paréntesis con H-codes)
    cleaned = raw_source
    for tech, admin in sorted(_TECH_MAP.items(), key=lambda x: -len(x[0])):
        if tech in cleaned:
            cleaned = cleaned.replace(tech, admin)
    return cleaned.strip(" ·()").strip()


# ── 2. Etiquetas canónicas de indicadores oficiales ──────────────────────────────────────────────
# Mantienen su acrónimo pero con descripción completa disponible.

INDICATOR_LABELS: dict[str, dict] = {
    "ICPI": {
        "acronym":   "ICPI",
        "full":      "Índice de Cumplimiento de Planificación Institucional",
        "short":     "Cumplimiento de Planificación",
        "fuente":    "Sistema QUIRA — Verificación algorítmica cruzada",
        "umbral_ok": 70.0,
    },
    "ICM": {
        "acronym":   "ICM",
        "full":      "Índice de Cumplimiento Municipal",
        "short":     "Cumplimiento Municipal (autoreportado)",
        "fuente":    "SIGAD — Sistema Gubernamental de Auditoría y Datos",
        "nota":      "Autoreportado por la entidad",
    },
    "PSG": {
        "acronym":   "PSG",
        "full":      "Participación Social con Enfoque de Género",
        "short":     "Participación de Género",
        "fuente":    "Módulo de Ejecución Presupuestaria",
        "umbral_ok": 30.0,
    },
    "IET": {
        "acronym":   "IET",
        "full":      "Índice de Equidad Territorial",
        "short":     "Equidad Territorial",
        "fuente":    "Módulo de Inversión Territorial Parroquial",
    },
    "IGP": {
        "acronym":   "IGP",
        "full":      "Índice de Gestión por Procesos",
        "short":     "Gestión por Procesos",
        "fuente":    "Módulo de Ejecución Presupuestaria",
        "umbral_ok": 45.0,
    },
    "IED": {
        "acronym":   "IED",
        "full":      "Índice de Eficiencia Direccional",
        "short":     "Eficiencia por Dirección",
        "fuente":    "Sistema QUIRA — Análisis por dirección",
    },
    "IFE": {
        "acronym":   "IFE",
        "full":      "Índice de Fomento Electoral",
        "short":     "Fomento Electoral",
        "fuente":    "CNE — Consejo Nacional Electoral",
    },
    "TPS": {
        "acronym":   "TPS",
        "full":      "Tasa de Pobreza por Servicios",
        "short":     "Pobreza por Servicios",
        "fuente":    "INEC 2022",
    },
    "NBI": {
        "acronym":   "NBI",
        "full":      "Necesidades Básicas Insatisfechas",
        "short":     "Necesidades Básicas",
        "fuente":    "INEC 2022",
    },
}


def indicator_label(acronym: str, mode: str = "short") -> str:
    """Devuelve la etiqueta del indicador en el modo especificado.

    Args:
        acronym: Acrónimo del indicador (ej. "ICPI", "PSG").
        mode: "short" (etiqueta corta), "full" (nombre completo), "acronym" (solo acrónimo).

    Returns:
        Etiqueta del indicador según el modo solicitado.
        Si el acrónimo no está registrado, devuelve el acrónimo original.
    """
    entry = INDICATOR_LABELS.get(acronym.upper())
    if not entry:
        return acronym
    return entry.get(mode, entry.get("short", acronym))


# ── 3. Fuente canónica para footer de páginas ────────────────────────────────────────────────────

FUENTE_CANONICA = "Sistema de Información Institucional QUIRA · Corte Q1-2026"
FUENTE_TERRITORIAL = (
    "Sistema QUIRA · Módulo de Inversión Territorial Parroquial · Corte Q1-2026"
)
FUENTE_CONSOLIDADO = (
    "Sistema QUIRA · Consolidado del Grupo Municipal · Corte Q1-2026"
)
