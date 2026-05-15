"""
SENTINEL · policies.py
Reglas de gobernanza para el agente: PUEDE / NO-PUEDE / MODO SEGURO
Doctrina: "La IA opera. La autoridad pública decide."
Dylus Lab © 2026
"""
from __future__ import annotations

# ── QUÉ PUEDE HACER SENTINEL ───────────────────────────────────────────────────
PUEDE: list[str] = [
    "Explicar cualquier indicador del ICGI-T con su fuente exacta (H73_OUTPUT_API)",
    "Analizar brechas territoriales entre las 7 parroquias (H99_ENGINE_CORE)",
    "Listar SATs activas y su nivel de criticidad (CRÍTICO / ALTO / MEDIO)",
    "Calcular la distancia a metas PDOT 2027 para cualquier indicador",
    "Sugerir pantallas de QUIRA OS relevantes para la consulta del usuario",
    "Citar artículos del COOTAD, COPFP, LOSNCP, LOSEP cuando aplica",
    "Alertar sobre anomalías detectadas (IRS=79.7%, PSG=12.83%, IGP=27.98%)",
    "Responder preguntas sobre ODS, cooperación internacional, género, LOTAIP",
    "Priorizar acciones según gravedad de SATs y distancia a metas",
    "Describir fondos internacionales elegibles y sus requisitos",
    "Explicar el sistema AVEP y cómo interpreta cada nivel",
    "Detectar congruencias o incongruencias entre HPT-M y PDOT",
]

# ── QUÉ NO PUEDE HACER SENTINEL (Fase Reader) ─────────────────────────────────
NO_PUEDE: list[str] = [
    "Ejecutar acciones sobre sistemas externos (eSIGEF, SOCE, CPCCS, SRI)",
    "Modificar datos del Gold Master o demo_data.py",
    "Firmar, registrar o formalizar actos administrativos",
    "Comprometer o reasignar recursos o fondos públicos",
    "Emitir opinión política partidista o electoral",
    "Inventar indicadores no presentes en H73/H99",
    "Acceder a datos personales identificables de funcionarios",
    "Dar asesoría legal vinculante (es orientación técnica, no dictamen)",
    "Confirmar datos sin citar la fuente del Gold Master",
    "Actuar de forma autónoma sin confirmación del usuario para decisiones críticas",
]

# ── MODO SEGURO ────────────────────────────────────────────────────────────────
# Frases que Sentinel usa cuando no hay dato suficiente
SAFE_MODE_PHRASES: list[str] = [
    "No hay evidencia suficiente en el Gold Master para responder esto con precisión.",
    "Este dato no está disponible en H73_OUTPUT_API ni H99_ENGINE_CORE. "
    "Recomiendo consultar la fuente primaria (INEC, SENPLADES, CPCCS).",
    "El indicador está marcado como 'Sin dato oficial' en el sistema. "
    "Pendiente de certificación.",
]

# ── PANTALLAS QUIRA OS ─────────────────────────────────────────────────────────
# Mapa de temas → pantallas sugeribles
SCREEN_MAP: dict[str, list[str]] = {
    "género":         ["genero", "cooperacion", "ods"],
    "psg":            ["genero", "metas"],
    "agua":           ["geotwin", "metas", "inversion"],
    "parroquia":      ["geotwin", "inversion", "confianza"],
    "sat":            ["sat", "brecha", "dashboard"],
    "presupuesto":    ["inversion", "metas", "eficiencia"],
    "ods":            ["ods", "cooperacion", "genero"],
    "transparencia":  ["transparencia", "confianza", "rdc"],
    "icgi":           ["dashboard", "pulso", "simulador"],
    "irs":            ["simulador", "inversion", "geotwin"],
    "brecha":         ["brecha", "simulador", "sat"],
    "rdc":            ["rdc", "confianza", "transparencia"],
    "lotaip":         ["transparencia", "confianza"],
    "cooperacion":    ["cooperacion", "ods", "genero"],
    "holding":        ["holding", "dashboard"],
    "cadena":         ["cadena", "metas", "eficiencia"],
}

# ── FUNCIONES ──────────────────────────────────────────────────────────────────
def evaluar_seguridad(pregunta: str) -> dict:
    """
    Evalúa si la pregunta implica una acción prohibida.

    Returns:
        dict con:
          - permitido: bool
          - motivo: str (vacío si permitido)
          - modo_seguro: bool (True si la pregunta es ambigua y requiere cautela)
    """
    preg_lo = pregunta.lower()

    # Detectar intento de acción ejecutiva
    palabras_prohibidas = [
        "ejecuta", "corre", "lanza", "modifica", "cambia", "borra",
        "elimina", "firma", "registra en esigef", "transfiere fondos",
        "publica en", "envía email", "manda un correo",
    ]
    for palabra in palabras_prohibidas:
        if palabra in preg_lo:
            return {
                "permitido": False,
                "motivo": (
                    f"La acción '{palabra}' cae en la categoría NO-PUEDE. "
                    "Sentinel fase Reader no ejecuta acciones. "
                    "El alcalde o director responsable debe confirmar esta acción."
                ),
                "modo_seguro": True,
            }

    # Detectar pregunta sin datos en el sistema
    sin_datos_triggers = [
        "encuesta", "percepción ciudadana", "encuesta de satisfacción",
        "dato biométrico", "cedula", "nómina personal", "salario individual",
    ]
    for trigger in sin_datos_triggers:
        if trigger in preg_lo:
            return {
                "permitido": True,
                "motivo": "",
                "modo_seguro": True,  # Responder con cautela, citar fuente primaria
            }

    return {"permitido": True, "motivo": "", "modo_seguro": False}


def sugerir_pantallas(pregunta: str) -> list[str]:
    """
    Sugiere pantallas de QUIRA OS relevantes para la pregunta.
    Retorna lista de page_keys (str) ordenadas por relevancia.
    """
    preg_lo = pregunta.lower()
    hits: dict[str, int] = {}
    for keyword, screens in SCREEN_MAP.items():
        if keyword in preg_lo:
            for s in screens:
                hits[s] = hits.get(s, 0) + 1
    return sorted(hits, key=lambda k: hits[k], reverse=True)[:3]
