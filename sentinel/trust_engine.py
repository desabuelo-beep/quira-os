"""
SENTINEL · trust_engine.py
Motor de Confianza Institucional — Sprint 5.
Governance Confidence Index basado en metodología H89_TRUST_SCORE del Gold Master.
Fórmula: Trust = 0.35×Integridad + 0.25×Disponibilidad + 0.25×Trazabilidad + 0.15×Cumplimiento
Doctrina: "La IA opera. La autoridad pública decide." — cada recomendación lleva su score.
Dylus Lab © 2026
"""
from __future__ import annotations

# ── PESOS H89 (Gold Master — hoja H89_TRUST_SCORE) ─────────────────────────────
_W_INTEGRIDAD    = 0.35
_W_DISPONIBILIDAD = 0.25
_W_TRAZABILIDAD  = 0.25
_W_CUMPLIMIENTO  = 0.15

# ── PERFILES DE CONFIANZA POR CONTEXTO ────────────────────────────────────────
# Cada perfil define los 4 componentes base según la naturaleza de la fuente.
# Calibrados contra H89_TRUST_SCORE Gold Master + anotaciones metodológicas H12c.

_PROFILES: dict[str, dict] = {
    # Charts determinísticos desde H99/H73 — fuente oficial sellada
    "chart_nbi": {
        "integridad":     90,   # INEC Censo 2022 oficial, metodología verificada
        "disponibilidad": 72,   # censo 2022 = 4 años de antigüedad
        "trazabilidad":   94,   # H99_ENGINE_CORE · Gold Master · SHA verificado
        "cumplimiento":   88,   # alineado con PDOT diagnóstico social
        "nota":           "NBI · INEC Censo 2022 · próxima actualización: Censo 2030",
    },
    "chart_inversion": {
        "integridad":     88,
        "disponibilidad": 92,   # POA-PAC Q1-2026, datos frescos
        "trazabilidad":   90,   # H07_eSIGEF + H99 georeferenciado
        "cumplimiento":   85,
        "nota":           "Inversión · POA-PAC Q1-2026 · eSIGEF devengado",
    },
    "chart_agua": {
        "integridad":     85,
        "disponibilidad": 88,   # dato operativo reciente
        "trazabilidad":   86,   # H99 + PDOT p.115
        "cumplimiento":   92,   # COOTAD Art.55 lit.d + ODS-6 + meta SC-I-N-01
        "nota":           "Agua · PDOT 2023-2027 + proyecto agua GAD Q1-2026",
    },
    "chart_tps": {
        "integridad":     78,   # TPS fuente INEC/PDOT diagnóstico, no H99 directo
        "disponibilidad": 68,   # diagnóstico PDOT = 2023
        "trazabilidad":   80,
        "cumplimiento":   85,
        "nota":           "TPS · INEC/PDOT diagnóstico 2023 · pendiente vinculación H99",
    },
    "chart_indices": {
        "integridad":     92,   # H73_OUTPUT_API 50 métricas verificadas
        "disponibilidad": 90,   # Q1-2026
        "trazabilidad":   94,   # H73 sellado SIAP-ICPI Gold Master v4.1
        "cumplimiento":   86,
        "nota":           "Índices · H73_OUTPUT_API · Gold Master v4.1 · Q1-2026",
    },
    "chart_icgit": {
        "integridad":     88,
        "disponibilidad": 90,
        "trazabilidad":   92,   # H12c serie histórica verificada
        "cumplimiento":   90,   # meta mandato 70% alineada con PDOT
        "nota":           "ICGI-T · H12c serie 2023-2026 · H12 motor canónico",
    },
    # Simulación paramétrica CBST v0.1
    "simulation_agua_rural": {
        "integridad":     84,   # coeficientes beta, no empíricos
        "disponibilidad": 90,
        "trazabilidad":   86,   # CBST documentado, anchored PDOT
        "cumplimiento":   92,   # meta SC-I-N-01 + COOTAD Art.55
        "nota":           "CBST v0.1 · calibración PDOT H04b · pendiente validación eSIGEF Q2-Q4",
    },
    "simulation_inversion_territorial": {
        "integridad":     80,
        "disponibilidad": 88,
        "trazabilidad":   82,
        "cumplimiento":   85,
        "nota":           "CBST v0.1 · coeficientes beta sujetos a calibración empírica",
    },
    "simulation_nbi_focalizado": {
        "integridad":     78,   # menor integridad: fricción social difícil de modelar
        "disponibilidad": 82,
        "trazabilidad":   80,
        "cumplimiento":   88,
        "nota":           "CBST v0.1 · NBI programas integrales · horizonte 2027",
    },
    "simulation_gestion_institucional": {
        "integridad":     80,
        "disponibilidad": 90,   # ejecución presupuestaria dato fresco
        "trazabilidad":   84,
        "cumplimiento":   88,
        "nota":           "CBST v0.1 · SAT-0/SAT-IV documentadas · eSIGEF Q1-2026",
    },
    # Respuesta LLM (Groq / Llama 3.3)
    "llm_response": {
        "integridad":     82,   # datos en system prompt verificados, pero LLM puede interpolar
        "disponibilidad": 88,
        "trazabilidad":   74,   # respuesta LLM menos trazable que output determinístico
        "cumplimiento":   78,
        "nota":           "Análisis Sentinel · Groq Llama 3.3 · contexto Gold Master Q1-2026",
    },
    # Respuesta con referencia legal activa
    "legal_reference": {
        "integridad":     90,
        "disponibilidad": 82,   # leyes pueden tener reformas recientes
        "trazabilidad":   92,   # artículo específico citado
        "cumplimiento":   96,   # fuente es la ley misma
        "nota":           "Marco legal Ecuador · COOTAD / COPLAFIP / Constitución",
    },
}


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def calculate_trust(
    context:       str,
    delta_penalty: int = 0,     # penalización por delta agresivo o dato faltante
    legal_boost:   bool = False, # +5 si hay referencia legal activa
) -> dict:
    """
    Calcula el Governance Confidence Index para un contexto dado.

    Args:
        context:       clave de perfil (ej: "chart_nbi", "simulation_agua_rural")
        delta_penalty: puntos a restar (0-20) por incertidumbre adicional
        legal_boost:   True si la respuesta incluye fundamento legal verificado

    Returns:
        dict con score, label, desglose por componente y nota metodológica
    """
    profile = _PROFILES.get(context, _PROFILES["llm_response"])

    I = max(0, profile["integridad"]    - delta_penalty)
    D = max(0, profile["disponibilidad"])
    T = max(0, profile["trazabilidad"]  - (delta_penalty // 2))
    C = max(0, profile["cumplimiento"])

    if legal_boost:
        C = min(100, C + 5)

    score = (
        _W_INTEGRIDAD     * I +
        _W_DISPONIBILIDAD * D +
        _W_TRAZABILIDAD   * T +
        _W_CUMPLIMIENTO   * C
    )
    score = round(min(99, max(40, score)))

    label = (
        "Muy Alta" if score >= 90 else
        "Alta"     if score >= 78 else
        "Media"    if score >= 65 else
        "Baja"
    )

    return {
        "score":      score,
        "label":      label,
        "desglose": {
            "Integridad":     round(I),
            "Disponibilidad": round(D),
            "Trazabilidad":   round(T),
            "Cumplimiento":   round(C),
        },
        "pesos": {
            "Integridad":     "35%",
            "Disponibilidad": "25%",
            "Trazabilidad":   "25%",
            "Cumplimiento":   "15%",
        },
        "nota":     profile.get("nota", ""),
        "formula":  "Trust = 0.35×I + 0.25×D + 0.25×T + 0.15×C  ·  H89_TRUST_SCORE",
        "version":  "v1.0 · Gold Master H89",
    }


def context_from_query(query: str, chart_hit: str = "", sim_policy: str = "") -> str:
    """
    Infiere el contexto de trust a partir del tipo de respuesta generada.
    Llamar después de determinar qué renderizó Sentinel.
    """
    if sim_policy:
        return f"simulation_{sim_policy}"
    if chart_hit:
        return f"chart_{chart_hit}"
    return "llm_response"


def trust_label_color(score: int) -> str:
    if score >= 90:
        return "#38A169"   # verde — Muy Alta
    if score >= 78:
        return "#00D4FF"   # cyan — Alta
    if score >= 65:
        return "#D69E2E"   # amarillo — Media
    return "#E53E3E"       # rojo — Baja
