"""
SENTINEL · simulate_policy.py
Motor de Simulación Paramétrica — Sprint 4.
Coeficientes Beta de Simulación Territorial (CBST v0.1).
Calibración: PDOT Montecristi 2023-2027 (H04b) · INEC Censo 2022 NBI · H99 Q1-2026.
MODEL_STATUS = "Beta Policy Engine" — sujeto a calibración con eSIGEF Q2-Q4 2026.
Dylus Lab © 2026
"""
from __future__ import annotations
import re
import unicodedata

# ── METADATOS DEL MODELO ───────────────────────────────────────────────────────

MODEL_STATUS      = "Beta Policy Engine"
CBST_VERSION      = "v0.1"
CALIBRATION_BASIS = (
    "PDOT Montecristi 2023-2027 meta SC-I-N-01 (H04b) · "
    "INEC Censo 2022 NBI baseline · H99_ENGINE_CORE Q1-2026"
)

# ── CBST v0.1 — COEFICIENTES BETA ─────────────────────────────────────────────
# Tester-validated: bajados de heurísticas iniciales tras revisión metodológica.
# Pendiente: calibración empírica con eSIGEF Q2-Q4 2026 cuando exista serie georef.

_AGUA_BASE_COEF    = 20.0   # pts agua por cada 100% de delta (tester: 20, no 25)
_AGUA_NBI_RATIO    = 0.15   # agua → reducción NBI (~15% del basket NBI)
_AGUA_TPS_RATIO    = 0.12   # agua → reducción TPS

_INV_NBI_COEF      = 6.5    # inversion_territorial → NBI (con quality_factor)
_INV_TPS_COEF      = 5.0    # inversion_territorial → TPS

_NBI_FOCALIZADO_COEF = 6.5  # nbi_focalizado → NBI (con brecha_factor, tester: 6.5 no 8.0)
_NBI_TPS_RATIO       = 0.70 # correlación NBI-TPS documentada H43
_NBI_AGUA_BONUS      = 3.0  # componente hídrico del programa integral

_GESTION_TPS_COEF    = 4.5  # gestion_institucional → TPS
_GESTION_ICGIT_COEF  = 8.0  # ejecución presupuestaria → ICGI-T directo

_CANTONAL_POP = 69_500      # H99: suma 7 parroquias Montecristi

# ── QUALITY FACTORS — inversion_territorial ───────────────────────────────────

QUALITY_FACTORS: dict[str, float] = {
    "capex_productivo": 1.00,
    "infraestructura":  0.85,
    "social":           0.70,
    "gasto_corriente":  0.45,
}
_DEFAULT_QUALITY = 0.75

# ── CATÁLOGO DE POLÍTICAS ──────────────────────────────────────────────────────

POLICY_LABELS: dict[str, str] = {
    "agua_rural":            "Inversión Hídrica Rural",
    "inversion_territorial": "Inversión Territorial General",
    "nbi_focalizado":        "Programa NBI Focalizado",
    "gestion_institucional": "Eficiencia de Gestión Institucional",
}

# ── HELPERS ────────────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def _find_parroquia(territorio: str, parroquias: list[dict]) -> dict | None:
    q = _norm(territorio)
    for p in parroquias:
        n = _norm(p["nombre"])
        if n in q or q in n:
            return p
    return None


def _territory_factor_agua(agua_actual: float) -> float:
    """Mayor déficit hídrico → mayor retorno marginal. Isabel Muentes ≈ 1.5x (max)."""
    return min(1.5, (100.0 - agua_actual) / 60.0)


def _brecha_factor_nbi(nbi_actual: float) -> float:
    """Normalizado al umbral AVEP crítico (50%). Más NBI → más impacto por inversión."""
    return max(0.5, nbi_actual / 50.0)


def _pop_weight(parroquia: dict) -> float:
    return parroquia.get("habitantes", 5_000) / _CANTONAL_POP


def _calc_confidence(
    policy_type: str,
    delta: float,
    parroquia: dict,
) -> tuple[int, str]:
    """
    Confidence score v0.1 (Sprint 4).
    Sprint 5 lo reemplaza con trust_engine.py usando la fórmula H89 completa:
    Trust = 0.35×Integridad + 0.25×Disponibilidad + 0.25×Trazabilidad + 0.15×Cumplimiento
    """
    base = {
        "agua_rural":             78,
        "inversion_territorial":  72,
        "nbi_focalizado":         68,
        "gestion_institucional":  75,
    }.get(policy_type, 65)

    if delta <= 0.15:
        base += 5        # delta conservador → mayor confianza
    elif delta <= 0.25:
        base += 2
    elif delta > 0.40:
        base -= 12       # delta agresivo penalizado

    if parroquia.get("agua") is not None:
        base += 3        # dato oficial disponible
    if parroquia.get("estado") == "EMERGENCIA":
        base -= 4        # mayor incertidumbre en zonas críticas

    score = min(95, max(50, base))
    label = (
        "Muy Alta" if score >= 88 else
        "Alta"     if score >= 78 else
        "Media"    if score >= 65 else
        "Baja"
    )
    return score, label


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def simulate_policy(
    policy_type: str,
    territorio:  str,
    delta:       float,
    quality:     str = "infraestructura",
) -> dict | None:
    """
    Simula el impacto de una política de inversión sobre indicadores de una parroquia.

    Args:
        policy_type: "agua_rural" | "inversion_territorial" | "nbi_focalizado" | "gestion_institucional"
        territorio:  nombre parroquia (acepta variantes sin tilde)
        delta:       incremento como fracción — 0.15 = +15%
        quality:     tipo de inversión para inversion_territorial

    Returns:
        dict con baseline, proyectado, inversión y metadata — o None si no encuentra parroquia.
    """
    from data.loader import load_all
    data       = load_all()
    parroquias = data.get("parroquias", [])
    parroquia  = _find_parroquia(territorio, parroquias)
    if not parroquia:
        return None

    nombre       = parroquia["nombre"]
    agua_actual  = parroquia.get("agua", 50.0)
    nbi_actual   = parroquia.get("nbi", 50.0)
    tps_actual   = parroquia.get("tps", 50.0)
    per_capita   = parroquia.get("per_capita", 60)
    inv_actual   = parroquia.get("inversion",
                       per_capita * parroquia.get("habitantes", 5_000))
    icgit_actual = data.get("icgit", {}).get("score", 53.56)

    inv_adicional = inv_actual * delta
    inv_nueva     = inv_actual + inv_adicional
    pc_nuevo      = int(per_capita * (1 + delta))
    pop_w         = _pop_weight(parroquia)

    agua_delta = nbi_delta = tps_delta = icgit_delta = 0.0

    if policy_type == "agua_rural":
        tf          = _territory_factor_agua(agua_actual)
        agua_delta  = delta * _AGUA_BASE_COEF * tf
        nbi_delta   = -(agua_delta * _AGUA_NBI_RATIO)
        tps_delta   = -(agua_delta * _AGUA_TPS_RATIO)
        icgit_delta = (agua_delta * 0.20 + abs(nbi_delta) * 0.35) * pop_w * 0.9

    elif policy_type == "inversion_territorial":
        qf          = QUALITY_FACTORS.get(quality, _DEFAULT_QUALITY)
        nbi_delta   = -(delta * _INV_NBI_COEF * qf)
        tps_delta   = -(delta * _INV_TPS_COEF * qf)
        icgit_delta = (abs(nbi_delta) * 0.40 + abs(tps_delta) * 0.25) * pop_w * 0.8

    elif policy_type == "nbi_focalizado":
        bf          = _brecha_factor_nbi(nbi_actual)
        nbi_delta   = -(delta * _NBI_FOCALIZADO_COEF * bf)
        tps_delta   = nbi_delta * _NBI_TPS_RATIO
        agua_delta  = delta * _NBI_AGUA_BONUS
        icgit_delta = abs(nbi_delta) * 0.50 * pop_w * 0.9

    elif policy_type == "gestion_institucional":
        tps_delta   = -(delta * _GESTION_TPS_COEF)
        icgit_delta = delta * _GESTION_ICGIT_COEF

    agua_nueva  = min(99.0, agua_actual + agua_delta)
    nbi_nuevo   = max(0.0,  nbi_actual  + nbi_delta)
    tps_nuevo   = max(0.0,  tps_actual  + tps_delta)
    icgit_proj  = min(100.0, icgit_actual + icgit_delta)

    confidence, conf_label = _calc_confidence(policy_type, delta, parroquia)

    # ── Nota de impacto cantonal — se activa cuando el delta ICGI-T parece pequeño ──
    pop_pct = round(pop_w * 100, 1)
    if abs(icgit_delta) < 0.5 and policy_type != "gestion_institucional":
        nota_cantonal = (
            f"El impacto cantonal ({icgit_delta:+.3f} pts ICGI-T) es moderado porque "
            f"{nombre} representa el {pop_pct}% de la población cantonal. "
            f"El efecto local sobre agua y NBI es alto; el efecto agregado es gradual "
            f"y se potencia con intervención simultánea en otras parroquias."
        )
    else:
        nota_cantonal = ""

    return {
        "policy_type":     policy_type,
        "policy_label":    POLICY_LABELS.get(policy_type, policy_type),
        "territorio":      nombre,
        "delta_pct":       round(delta * 100, 1),
        "baseline": {
            "agua":        round(agua_actual, 2),
            "nbi":         round(nbi_actual,  1),
            "tps":         round(tps_actual,  2),
            "per_capita":  per_capita,
            "inversion":   int(inv_actual),
            "icgit":       round(icgit_actual, 2),
        },
        "proyectado": {
            "agua":        round(agua_nueva,   2),
            "agua_delta":  round(agua_delta,   2),
            "nbi":         round(nbi_nuevo,    2),
            "nbi_delta":   round(nbi_delta,    2),
            "tps":         round(tps_nuevo,    2),
            "tps_delta":   round(tps_delta,    2),
            "icgit":       round(icgit_proj,   2),
            "icgit_delta": round(icgit_delta,  3),
        },
        "inversion_adicional":   int(inv_adicional),
        "inversion_nueva":       int(inv_nueva),
        "per_capita_nuevo":      pc_nuevo,
        "pop_pct_cantonal":      pop_pct,
        "nota_impacto_cantonal": nota_cantonal,
        "confidence":            confidence,
        "confidence_label":      conf_label,
        "cbst_version":          CBST_VERSION,
        "model_status":          MODEL_STATUS,
        "calibration_basis":     CALIBRATION_BASIS,
        "nota": (
            f"CBST {CBST_VERSION} · {POLICY_LABELS.get(policy_type, policy_type)}. "
            f"Sujeto a calibración con datos eSIGEF Q2-Q4 2026."
        ),
    }


def detect_simulation_intent(query: str) -> dict | None:
    """
    Detecta si la query es una solicitud de simulación de política.
    Extrae: policy_type, territorio, delta.
    Devuelve None si no hay intención de simulación.
    """
    q = _norm(query)

    # Triggers de simulación
    sim_triggers = [
        "si subimos", "si aumentamos", "si invertimos", "si se aumenta",
        "simular", "simula", "que pasa si", "que pasaria", "que pasara",
        "proyectar", "escenario", "impacto de", "efecto de",
        "si mejoramos", "si duplicamos", "si reducimos",
    ]
    if not any(t in q for t in sim_triggers):
        return None

    # ── Detectar tipo de política ─────────────────────────────────────────────
    if any(t in q for t in ["hidric", "agua", "potable", "agua rural"]):
        policy = "agua_rural"
    elif any(t in q for t in ["nbi", "pobreza", "necesidades basicas", "integral"]):
        policy = "nbi_focalizado"
    elif any(t in q for t in ["gestion", "ejecucion", "institucional", "sat", "pac"]):
        policy = "gestion_institucional"
    else:
        policy = "inversion_territorial"  # default

    # ── Detectar delta (%) ────────────────────────────────────────────────────
    pct_match = re.search(r"(\d+(?:\.\d+)?)\s*%", query)
    delta = float(pct_match.group(1)) / 100 if pct_match else 0.15  # default 15%
    delta = max(0.01, min(1.0, delta))  # clamp [1%, 100%]

    # ── Detectar territorio ───────────────────────────────────────────────────
    parroquias_search = [
        "isabel muentes", "anibal san andres", "colorado",
        "la pila", "eloy alfaro", "leonidas plaza", "leonidas proano",
        "montecristi",
    ]
    territorio = "isabel muentes"  # default: parroquia más crítica
    for par in parroquias_search:
        if par in q:
            territorio = par
            break

    # Fallback: usar última parroquia de state_memory si no se menciona explícitamente
    if territorio == "isabel muentes" and "isabel" not in q and "muentes" not in q:
        try:
            from sentinel import state_memory
            mem_par = state_memory.get_parroquia_key()
            if mem_par:
                territorio = mem_par
        except Exception:
            pass

    return {
        "policy_type": policy,
        "territorio":  territorio,
        "delta":       delta,
    }
