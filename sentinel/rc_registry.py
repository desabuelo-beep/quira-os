"""
sentinel/rc_registry.py
RC-CORE Registry Layer — QUIRA OS
Dylus Lab © 2026-05-20

Nucleo centralizado de contratos inferenciales para todos los motores RC.
Fuente unica de verdad para:
  - Thresholds de confianza y pisos
  - Reglas de overwhelm y observacional
  - Caps de tier por motor
  - SAT mappings canonicos
  - Metas PDOT y umbrales EED
  - Descuentos de calibracion

RAZON DE SER:
  La logica transversal (observational_only, tier caps, confidence suppression,
  overwhelm bypass, severity normalization) estaba distribuida en 8+ archivos.
  Cuando llegue RC-D1 Legalidad, la entropia de reglas explotar sin este nucleo.

USO:
  from sentinel.rc_registry import RC, get_threshold, overwhelm_active

  # Acceso directo por motor
  floor = RC["RC-D4"]["min_floor_confidence"]          # 0.35
  meta  = RC["PDOT"]["irs_meta_2027"]                  # 45.0
  cap   = RC["RC-D3D4"]["observational_threshold"]     # 0.25

  # Funciones de query
  overwhelm_active("RC-D4", irs=93.1)                  # True
  needs_tier_cap("RC-D3D4", observational=True)        # True

POLITICA DE ACTUALIZACION:
  Los valores de este registro son contratos inferenciales.
  Modificar solo tras validacion con analista Dylus Lab.
  Cada cambio debe ir acompanado de commit explicativo.

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


# ── CARGA DE JSON BASE ─────────────────────────────────────────────────────────
_DATA_DIR = Path(__file__).parent.parent / "data"

def _load_json(name: str) -> dict:
    p = _DATA_DIR / name
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except Exception:
        return {}

_D4_CALIB  = _load_json("d4_calibration.json")
_RC72_CALIB = _load_json("rc72_calibration.json")
_D4_NORM   = _load_json("d4_normative.json")


# ── REGISTRO CANÓNICO ──────────────────────────────────────────────────────────

RC: dict[str, dict[str, Any]] = {

    # ── RC-7.2 Longitudinal Engine ─────────────────────────────────────────────
    "RC-7.2": {
        "description": "Motor de analisis temporal longitudinal",
        "n_periodos_min_full":    _RC72_CALIB.get("confidence_decay", {}).get("n_periodos_min_full", 4),
        "n_periodos_min_basic":   _RC72_CALIB.get("confidence_decay", {}).get("n_periodos_min_basic", 2),
        "decay_1_period":         _RC72_CALIB.get("confidence_decay", {}).get("decay_1_period", 0.50),
        "decay_2_periods":        _RC72_CALIB.get("confidence_decay", {}).get("decay_2_periods", 0.70),
        "decay_3_periods":        _RC72_CALIB.get("confidence_decay", {}).get("decay_3_periods", 0.85),
        "decay_4plus_periods":    _RC72_CALIB.get("confidence_decay", {}).get("decay_4plus_periods", 1.00),
        "reform_threshold_pct":   _RC72_CALIB.get("reform_whitelist", {}).get("alcalde_threshold_pct", 10.0),
        "sat_suppression_min":    _RC72_CALIB.get("sat_suppression_thresholds", {}).get("min_confidence_for_sat", 0.40),
        # Patrones canonicos
        "patterns": [
            "EXPANSION_TARDIA", "REFORMA_LEGITIMA", "PARALISIS_ESTRUCTURAL",
            "MANIPULACION_TEMPORAL", "CIERRE_TARDIO", "DETERIORO_PROGRESIVO",
            "RECUPERACION_VERIFICADA", "INFRAEJECUCION_CRONICA",
            "SHOCK_EXTERNO", "SIN_PATRON_CLARO",
        ],
        # SAT codes que puede emitir
        "sat_codes": ["SAT-X-A", "SAT-X-B", "SAT-X-C", "SAT-X-D"],
        # Tier cap: RC-7.2 nunca emite "severa" con n_periodos < 2
        "tier_cap_observational": "potencial",
    },

    # ── RC-7.3 Calibration Layer ───────────────────────────────────────────────
    "RC-7.3": {
        "description": "Capa de calibracion epistemologica temporal",
        "min_confidence_floor":  0.10,   # nunca baja de 10% (proteccion vs supresion total)
        "evidence_weight_full":  1.00,   # n_periodos >= 4
        "evidence_weight_basic": 0.60,   # n_periodos 2-3
        "evidence_weight_min":   0.30,   # n_periodos 1
        "seasonal_q1_g7178_ti":  2.5,    # Ti esperado Q1 inversion
        "entity_baselines": {
            "GAD":     {"ti_annual_expected": 75.0, "ti_q1_g7178": 2.5,  "ti_q1_g5157": 22.0},
            "BOMB":    {"ti_annual_expected": 85.0, "ti_q1_g7178": 5.0,  "ti_q1_g5157": 30.0},
            "PAT":     {"ti_annual_expected": 70.0, "ti_q1_g7178": 2.0,  "ti_q1_g5157": 18.0},
            "EP_ASEO": {"ti_annual_expected": 80.0, "ti_q1_g7178": 3.5,  "ti_q1_g5157": 25.0},
            "HOLDING": {"ti_annual_expected": 75.0, "ti_q1_g7178": 2.5,  "ti_q1_g5157": 22.0},
        },
    },

    # ── RC-D4 Spatial Equity Engine ───────────────────────────────────────────
    "RC-D4": {
        "description": "Motor de equidad territorial interparroquial",
        # Descuentos de prudencia espacial
        "capital_effect_discount":         _D4_CALIB.get("capital_effect_discount",         0.18),
        "competence_scope_discount":       _D4_CALIB.get("competence_scope_discount",       0.12),
        "single_period_discount":          _D4_CALIB.get("single_period_discount",          0.08),
        "population_concentration_discount": _D4_CALIB.get("population_concentration_discount", 0.10),
        # Umbrales criticos
        "sat_d4_min_confidence":           _D4_CALIB.get("sat_d4_min_confidence",           0.45),
        "min_floor_confidence":            _D4_CALIB.get("min_floor_confidence",            0.35),
        "irs_overwhelm_threshold":         _D4_CALIB.get("irs_overwhelm_threshold",         85.0),
        # Triple Signal (asimetria territorial institucionalizada)
        "triple_signal_irs_min":  70.0,
        "triple_signal_cr1_min":  0.65,
        "triple_signal_cap_min":  3.0,
        # Patrones canonicos D4
        "patterns": [
            "CONCENTRACION_TERRITORIAL",
            "REZAGO_PERSISTENTE",
            "CAPTURA_CAPITAL",
            "INEQUIDAD_HIDRICA",
            "SESGO_DISTRIBUTIVO",
        ],
        # SAT codes D4
        "sat_codes": ["SAT-D4-A", "SAT-D4-B", "SAT-D4-C", "SAT-D4-D", "SAT-D4-E"],
        # AVEP D4 escala: (irs_min, riesgo, score)
        "avep_d4_scale": [
            (80, "Ruptura Territorial",    20),
            (60, "Inequidad Estructural",  40),
            (40, "Sesgo Distributivo",     60),
            (20, "Distribucion Aceptable", 80),
            (0,  "Equidad Territorial",    100),
        ],
        # Tier cap: D4 con single_period siempre <= moderada (sin overwhelm)
        "tier_cap_single_period": "moderada",
    },

    # ── RC-D4-Normative ───────────────────────────────────────────────────────
    "RC-D4-Normative": {
        "description": "Binding normativo espacial (tension-aware, no acusatorio)",
        "tier_cap_unverified": "moderada",  # art. no verificado: max moderada aunque tier sea severa
        "max_refs":            4,           # max refs para conservar tokens Haiku
        "tier_language": {
            "severa":    "presenta una divergencia estructural significativa respecto a",
            "moderada":  "muestra patrones que ameritan revision a la luz de",
            "potencial": "genera indicadores de tension potencial en relacion con",
        },
        "prohibited_language": [
            "incumplio", "violo", "es responsable de", "decision ilegal",
            "incumplimiento", "violacion", "responsabilidad legal",
        ],
    },

    # ── RC-D3D4 Cross-Inference Engine ────────────────────────────────────────
    "RC-D3D4": {
        "description": "Motor de inferencia cruzada temporal x territorial",
        # Epistemia
        "cross_conf_penalty_threshold":  0.30,   # d3_conf < 0.30 → cross_conf × 0.5
        "observational_threshold":       0.25,   # cross_conf < 0.25 → observational_only=True
        "d3_min_confidence_threshold":   0.15,   # d3_conf < 0.15 → fuerza observacional
        # EED Score (Execution-Equity Divergence)
        "eed_expansion_concentrada":     15.0,   # EED > 15 → expansion_concentrada
        "eed_rezago_distributivo":      -15.0,   # EED < -15 → rezago_distributivo
        # Tier cap epistemico
        "tier_cap_observational": "potencial",   # observational_only siempre → max potencial
        # Patrones canonicos D3xD4
        "patterns": [
            "EXPANSION_CONCENTRADA",
            "EXPANSION_CON_EXCLUSION",
            "CRISIS_DOBLE",
            "EXCLUSION_PERIFERICA",
            "VULNERABILIDAD_HIDRICA",
            "MAQUILLAJE_TERRITORIAL",
            "REDISTRIBUCION_REGRESIVA",
            "CONVERGENCIA_CRITICA",
            "SIN_CRUCE_CONFIRMADO",
        ],
        # SAT codes D3xD4
        "sat_codes": ["SAT-D3D4-A", "SAT-D3D4-B", "SAT-D3D4-C", "SAT-D3D4-D", "SAT-D3D4-E"],
        # Patrones que requieren human review cuando confirmados (cross_conf >= threshold)
        "human_review_patterns": ["CRISIS_DOBLE", "EXCLUSION_PERIFERICA", "EXPANSION_CONCENTRADA"],
        "human_review_cross_conf_min": 0.40,   # cross_conf minimo para activar human review
    },

    # ── RC-D3D4-Normative ─────────────────────────────────────────────────────
    "RC-D3D4-Normative": {
        "description": "Binding normativo cruzado (divergencia temporal x territorial)",
        "eed_severo_umbral":    25.0,
        "eed_moderado_umbral":  12.0,
        "tier_cap_observational": "potencial",
        "tier_cap_unverified": "moderada",
        "max_refs":            4,
    },

    # ── PDOT Montecristi 2023-2027 ────────────────────────────────────────────
    "PDOT": {
        "description": "Plan de Desarrollo y Ordenamiento Territorial Montecristi 2023-2027",
        "irs_meta_2027": float(
            _D4_NORM.get("pdot_targets", {}).get("irs_meta_2027", 45.0)
        ),
        "fuente": "PDOT Montecristi 2023-2027 — D4_EQUIDAD meta institucional",
        "nota": (
            "Autocompromiso del GAD. Instrumento prioritario sobre norma externa: "
            "el municipio se comprometio con IRS<=45 para 2027."
        ),
        # Brechas criticas de la meta PDOT
        "brecha_severa":   40.0,   # brecha > 40 pts → severa
        "brecha_moderada": 10.0,   # brecha > 10 pts → moderada
    },

    # ── RC-D1 Legalidad Engine ────────────────────────────────────────────────
    "RC-D1": {
        "description": "Motor de coherencia normativa institucional — NO es detector de infracciones",
        # Confianza mínima para emitir estados de riesgo (no observacional)
        "min_confidence_for_risk":    0.25,
        # Confianza mínima para escalar a human review
        "min_confidence_for_review":  0.40,
        # Umbral Alcalde GAD para reforma sin Concejo (COPFP Art. 97)
        "alcalde_reform_threshold":   10.0,
        # Parroquias que deben cubrir el PP en Montecristi (COOTAD Art. 238)
        "n_parroquias_montecristi":   7,
        # Cap de status cuando observational_only=True
        "status_cap_observational":   "OBSERVADO",
        # Estados D1 (ordenados por severidad ascendente)
        "status_severity": {
            "LEGAL":                   0,
            "OBSERVADO":               1,
            "RIESGO_DE_EVIDENCIA":     2,
            "RIESGO_DE_PROCEDIMIENTO": 3,
            "RIESGO_DE_COMPETENCIA":   4,
            "REQUIERE_REVIEW":         5,
        },
        # SAT codes D1
        "sat_codes": ["SAT-D1-A", "SAT-D1-B", "SAT-D1-C"],
        # Entidades soportadas
        "entities": ["GAD", "EMAI-EP", "BOMBEROS", "PATRONATO"],
        # Norms vault-verified en RC-D1.1
        "verified_norms": [
            "COOTAD Art. 55", "COOTAD Art. 238", "COOTAD Art. 263",
            "COOTAD Art. 265", "COOTAD Art. 267", "COOTAD Art. 272",
            "COOTAD Art. 432", "CRE Art. 238", "CRE Art. 264(4)",
            "COPFP Art. 97", "LOSNCP",
        ],
        # Tier language D1 (tension-aware, nunca acusatorio)
        "tier_language": {
            "RIESGO_DE_COMPETENCIA":   "genera indicadores de potencial exceso de competencia respecto a",
            "RIESGO_DE_PROCEDIMIENTO": "el canal aprobatorio puede no haberse seguido según",
            "RIESGO_DE_EVIDENCIA":     "la documentación de respaldo no es verificable bajo",
            "REQUIERE_REVIEW":         "la complejidad supera el umbral de valoración automatizada para",
        },
        "prohibited_language": [
            "incumplio", "violo", "es responsable de", "decision ilegal",
            "incumplimiento", "violacion", "responsabilidad legal",
        ],
    },

    # ── RC-D1.3 Normative Coherence ──────────────────────────────────────────
    "RC-D1.3": {
        "description": "Coherencia estratégica: PDOT ↔ POA ↔ PAI ↔ presupuesto ↔ ejecucion ↔ territorio",
        # Meta PDOT vault-verified
        "irs_meta_pdot_2027":       45.0,      # PDOT Montecristi 2023-2027 (data/d4_normative.json)
        # Umbrales de brecha compuesta
        "threshold_critica_composite":    0.60,
        "threshold_critica_territorial":  0.60,   # Ruta B: brecha territorial extrema
        "threshold_estrategica_composite":0.40,
        "threshold_menor":                0.15,
        # Confianza mínima para estados severos
        "min_conf_critica":     0.40,
        "min_conf_estrategica": 0.25,
        # SAT D1.3
        "sat_codes": ["SAT-D1-D"],
        # Estados (5 — incluye EVIDENCIA_INSUFICIENTE heredando prudencia RC-CORE)
        "states": [
            "ALINEADO", "DESVIACION_MENOR", "DESVIACION_ESTRATEGICA",
            "CONTRADICCION_CRITICA", "EVIDENCIA_INSUFICIENTE",
        ],
        # Compromisos vault-verified activos
        "commitments_verified": [
            "PDOT-EQUIDAD-01",  # IRS ≤ 45 para 2027
            "PDOT-AGUA-01",     # cobertura agua rural (CRE 264(4))
            "PDOT-PP-01",       # PP 7 parroquias (COOTAD 238)
            "PDOT-DIST-01",     # distribución equitativa (COOTAD 272)
        ],
        # Entidades con PDOT propio (solo GAD)
        "entities_with_pdot": ["GAD"],
        # Tier language (tension-aware)
        "tier_language": {
            "CONTRADICCION_CRITICA":  "presenta divergencia estructural entre compromiso declarado y comportamiento material en relacion con",
            "DESVIACION_ESTRATEGICA": "genera indicadores de desacople estrategico sostenido respecto a",
            "DESVIACION_MENOR":       "muestra gap marginal respecto a",
        },
        "prohibited_language": [
            "incumplio", "violo", "es responsable de", "fraude", "corrupcion",
        ],
    },

    # ── RC-SYNTHESIS Meta-Orquestador Epistemologico ─────────────────────────
    "RC-SYNTHESIS": {
        "description": "Contratos del meta-orquestador epistemologico SENTINEL-SYNTHESIS",
        # Pesos por motor (mayor peso = mayor autoridad epistemica)
        "engine_weights": {
            "D3xD4":       1.20,   # Cross-dimensional — mayor evidencia combinada
            "D4":          1.10,   # Territorial — alta especificidad
            "D1.3":        1.05,   # Normative coherence — PDOT verificado
            "D3":          1.00,   # Temporal — base epistemica
            "D1":          0.90,   # Procedural — evidencia documental
            "HUMAN_REVIEW":0.80,   # Revision humana — activada externamente
        },
        # Penalizacion epistemica por observacional
        "observational_penalty": 0.40,
        # Maximo de señales accionables (doctrina inmutable)
        "max_signals": 3,
        # Umbrales de severidad global
        "severity_critica_min_severity":    5,
        "severity_critica_min_conf":        0.40,
        "severity_alta_min_severity":       4,
        "severity_alta_min_conf":           0.35,
        # Piso de confianza para incluir señal en top-3
        "signal_min_confidence":            0.05,
        # Tensiones dominantes semanticas registradas
        "dominant_tensions": [
            "EXPANSION_REGRESIVA",
            "BLOQUEO_INSTITUCIONAL",
            "DESACOPLE_ESTRATEGICO",
            "CRISIS_TERRITORIAL_CRITICA",
            "VULNERABILIDAD_HIDRICA_SISTEMICA",
            "MAQUILLAJE_INSTITUCIONAL",
            "FRICCION_PROCEDIMENTAL",
            "SIN_TENSION_DOMINANTE",
            "COHERENCIA_POSITIVA",
            "TENSION_COMPUESTA",
        ],
        # Doctrina inmutable (3 reglas del colega)
        "doctrine": [
            "Nunca sumar tensiones linealmente — tipos institucionales emergentes",
            "La dimension con mayor evidencia domina — conf es primaria en ranking",
            "Maximo 3 senales — siempre; sin excepciones",
        ],
    },

    # ── Human Review Layer ───────────────────────────────────────────────────
    "HUMAN_REVIEW": {
        "description": "Reglas para activar revision institucional humana",
        # Condiciones que siempre disparan human review (cross_conf confirmado)
        "auto_trigger_patterns": [
            "CRISIS_DOBLE",
            "EXCLUSION_PERIFERICA",
        ],
        # Condicion adicional: cross_conf minimo para no-observacional
        "confirmed_cross_conf_min": 0.40,
        # D4: overwhelm + SATs criticos
        "d4_overwhelm_with_sats_triggers": True,
        # IRS umbral para human review D4 independiente
        "irs_human_review_min": 80.0,
        # Nivel EED para trigger adicional
        "eed_human_review_min": 25.0,
    },
}


# ── FUNCIONES DE CONSULTA ──────────────────────────────────────────────────────

def get_threshold(engine: str, key: str, default: Any = None) -> Any:
    """
    Retorna el valor de un threshold para un motor dado.

    Ejemplo:
        get_threshold("RC-D4", "irs_overwhelm_threshold")  # 85.0
        get_threshold("RC-D3D4", "observational_threshold")  # 0.25
    """
    return RC.get(engine, {}).get(key, default)


def overwhelm_active(engine: str, **kwargs) -> bool:
    """
    Verifica si el bypass de evidencia abrumadora esta activo.

    RC-D4:   overwhelm_active("RC-D4", irs=93.1) → True
    RC-D3D4: siempre False (no tiene overwhelm propio — usa D4)
    """
    if engine == "RC-D4":
        irs_th = RC["RC-D4"]["irs_overwhelm_threshold"]
        return float(kwargs.get("irs", 0)) >= irs_th
    return False


def needs_tier_cap(engine: str, observational: bool = False, verified: bool = True) -> bool:
    """
    True si la regla de tier cap aplica en el contexto dado.

    observational=True → siempre cap en 'potencial'
    verified=False     → cap en 'moderada' para articulos no verificados
    """
    if observational and RC.get(engine, {}).get("tier_cap_observational"):
        return True
    if not verified and RC.get(engine, {}).get("tier_cap_unverified"):
        return True
    return False


def get_tier_cap(engine: str, observational: bool = False, verified: bool = True) -> Optional[str]:
    """
    Retorna el tier maximo permitido dado el contexto.
    None si no hay cap aplicable.
    """
    if observational:
        return RC.get(engine, {}).get("tier_cap_observational")
    if not verified:
        return RC.get(engine, {}).get("tier_cap_unverified")
    return None


def get_tier_language(tier: str) -> str:
    """Verbo canonico de tension para el tier dado (fuente unica de verdad)."""
    return RC["RC-D4-Normative"]["tier_language"].get(
        tier, "presenta indicadores en relacion con"
    )


def is_prohibited_language(text: str) -> list[str]:
    """
    Verifica si el texto contiene lenguaje prohibido (acusatorio).
    Retorna lista de terminos encontrados (vacia si es correcto).
    """
    prohibited = RC["RC-D4-Normative"]["prohibited_language"]
    text_low   = text.lower()
    return [p for p in prohibited if p in text_low]


def get_pdot_meta() -> float:
    """Meta PDOT IRS <= N para 2027. Fuente unica."""
    return RC["PDOT"]["irs_meta_2027"]


def get_eed_class(eed: float) -> str:
    """
    Clasifica el EED score segun los umbrales del registro.
    Fuente unica para todos los motores.
    """
    if eed > RC["RC-D3D4"]["eed_expansion_concentrada"]:
        return "expansion_concentrada"
    if eed < RC["RC-D3D4"]["eed_rezago_distributivo"]:
        return "rezago_distributivo"
    return "alineado"


def get_cross_conf(d3_conf: float, d4_conf: float) -> float:
    """
    Calcula cross_confidence segun formula canonica del registro.
    Fuente unica — evita que cada motor la reimplemente distinto.
    """
    import math
    penalty_threshold = RC["RC-D3D4"]["cross_conf_penalty_threshold"]
    base = math.sqrt(max(0.0, d3_conf) * max(0.0, d4_conf))
    if d3_conf < penalty_threshold:
        base *= 0.5
    return round(base, 4)


def is_observational(cross_conf: float, d3_conf: float) -> bool:
    """
    Determina si una inferencia es solo observacional.
    Fuente unica de la regla epistemica.
    """
    return (
        cross_conf < RC["RC-D3D4"]["observational_threshold"]
        or d3_conf < RC["RC-D3D4"]["d3_min_confidence_threshold"]
    )


def needs_human_review(
    cross_pattern:  str   = "",
    cross_conf:     float = 0.0,
    observational:  bool  = True,
    irs:            float = 0.0,
    eed:            float = 0.0,
    d4_overwhelm:   bool  = False,
    d4_sat_codes:   list  = None,
) -> tuple[bool, str]:
    """
    Determina si una inferencia requiere revision institucional humana.

    Retorna: (bool, razon_str)

    Reglas:
      1. Patron D3xD4 critico confirmado (cross_conf >= umbral, no observacional)
      2. D4 overwhelm activo con SATs criticos (IRS >= 85 + SATs)
      3. EED severo confirmado (EED > 25, no observacional)
    """
    hr = RC["HUMAN_REVIEW"]
    d4_sat_codes = d4_sat_codes or []

    # Regla 1: patron D3xD4 critico confirmado
    if (
        not observational
        and cross_pattern in hr["auto_trigger_patterns"]
        and cross_conf >= hr["confirmed_cross_conf_min"]
    ):
        return True, (
            f"Patron D3xD4 critico confirmado: {cross_pattern} "
            f"(cross_conf={cross_conf:.2f} >= {hr['confirmed_cross_conf_min']}). "
            f"Requiere validacion institucional antes de elevar tension normativa."
        )

    # Regla 2: D4 overwhelm con SATs criticos
    if hr["d4_overwhelm_with_sats_triggers"] and d4_overwhelm and len(d4_sat_codes) >= 2:
        return True, (
            f"Evidencia D4 abrumadora (IRS={irs:.1f} >= {RC['RC-D4']['irs_overwhelm_threshold']}) "
            f"con {len(d4_sat_codes)} SATs activos. "
            f"La sobrecarga de senales requiere validacion institucional."
        )

    # Regla 3: EED severo confirmado
    if not observational and abs(eed) >= hr["eed_human_review_min"]:
        return True, (
            f"Divergencia temporal-territorial severa (|EED|={abs(eed):.1f} >= {hr['eed_human_review_min']}) "
            f"confirmada (no observacional). Requiere revision institucional."
        )

    return False, ""


def audit_registry_consistency() -> list[str]:
    """
    Verifica consistencia interna del registro.
    Retorna lista de inconsistencias (vacia si todo correcto).
    """
    issues = []

    # PDOT meta debe coincidir entre RC["PDOT"] y d4_normative.json
    pdot_meta = RC["PDOT"]["irs_meta_2027"]
    d4_norm_meta = float(_D4_NORM.get("pdot_targets", {}).get("irs_meta_2027", 45.0))
    if abs(pdot_meta - d4_norm_meta) > 0.01:
        issues.append(
            f"PDOT meta inconsistente: RC['PDOT']={pdot_meta} vs d4_normative.json={d4_norm_meta}"
        )

    # D4 overwhelm threshold debe coincidir con d4_calibration.json
    reg_overwhelm = RC["RC-D4"]["irs_overwhelm_threshold"]
    json_overwhelm = float(_D4_CALIB.get("irs_overwhelm_threshold", 85.0))
    if abs(reg_overwhelm - json_overwhelm) > 0.01:
        issues.append(
            f"D4 overwhelm inconsistente: registry={reg_overwhelm} vs d4_calibration.json={json_overwhelm}"
        )

    # EED: los umbrales son intencionalmente distintos (propósitos diferentes)
    # eed_expansion_concentrada (15.0) = umbral de clasificación de PATRÓN D3xD4
    # eed_severo_umbral (25.0) = umbral para tier NORMATIVO "severa"
    # No deben ser iguales → validamos solo que eed_severo_umbral > eed_expansion_concentrada
    eed_pattern_th = RC["RC-D3D4"]["eed_expansion_concentrada"]
    eed_norm_sev   = RC["RC-D3D4-Normative"]["eed_severo_umbral"]
    if eed_norm_sev <= eed_pattern_th:
        issues.append(
            f"EED umbrales invertidos: eed_severo_normativo ({eed_norm_sev}) "
            f"debe ser mayor que eed_expansion_concentrada ({eed_pattern_th})"
        )

    return issues


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-CORE Registry Layer — QUIRA OS")
    print("=" * 65)

    for engine, contract in RC.items():
        desc = contract.get("description", "")
        n_keys = len([k for k in contract if not k.startswith("_")])
        print(f"\n  {engine:<22} — {desc}")
        print(f"  {'':22}   {n_keys} contratos registrados")

    print("\n── Funciones de consulta ──")
    print(f"  PDOT meta 2027        : IRS <= {get_pdot_meta():.0f}")
    print(f"  D4 overwhelm (IRS=93) : {overwhelm_active('RC-D4', irs=93.1)}")
    print(f"  D4 overwhelm (IRS=70) : {overwhelm_active('RC-D4', irs=70.0)}")
    print(f"  EED class (+18.9)     : {get_eed_class(18.9)}")
    print(f"  EED class (+27.0)     : {get_eed_class(27.0)}")
    print(f"  cross_conf(0.07,0.90) : {get_cross_conf(0.07, 0.90):.4f}")
    print(f"  observational(0.126)  : {is_observational(0.126, 0.07)}")
    print(f"  tier_cap obs=True     : {get_tier_cap('RC-D3D4', observational=True)}")
    print(f"  tier_lang severa      : '{get_tier_language('severa')[:40]}...'")

    # Test human review
    needs, reason = needs_human_review(
        cross_pattern="CRISIS_DOBLE", cross_conf=0.45,
        observational=False, irs=88.0, eed=28.0,
        d4_overwhelm=True, d4_sat_codes=["SAT-D4-A","SAT-D4-B","SAT-D4-C"],
    )
    print(f"\n  Human review (CRISIS_DOBLE conf=0.45): {needs}")
    if reason:
        print(f"  Razon: {reason[:100]}")

    # Audit
    issues = audit_registry_consistency()
    print(f"\n── Audit de consistencia ──")
    if issues:
        for i in issues:
            print(f"  [INCONSISTENCIA] {i}")
    else:
        print("  Registro consistente — sin inconsistencias detectadas.")
