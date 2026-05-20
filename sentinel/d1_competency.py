"""
sentinel/d1_competency.py
RC-D1.1 — Competency Graph (Grafo de Competencias Institucionales)
Dylus Lab © 2026-05-20

FUNCIÓN:
  Mapa computacional de "¿quién puede hacer qué, bajo qué norma y con qué evidencia?".
  Responde a la pregunta jurídica más básica antes de cualquier juicio normativo:
  ¿tenía la entidad la competencia formal para actuar así?

FUENTES (solo vault-verified):
  - COOTAD Art. 55  — competencias exclusivas GAD municipal
  - COOTAD Art. 238 — presupuesto participativo (7 parroquias)
  - COOTAD Art. 263 — clausura presupuestaria 31-dic
  - COOTAD Art. 265 — liquidación antes del 31-ene
  - COOTAD Art. 267 — cada EP aprueba su presupuesto con su propio Directorio
  - COOTAD Art. 272 — distribución de recursos parroquiales
  - COOTAD Art. 432 — facultades del Alcalde
  - CRE Art. 238   — autonomía GADs y equidad interterritorial
  - CRE Art. 264(4) — competencia municipal en agua potable
  - COPFP Art. 97  — umbral Alcalde: reforma <= 10% codificado sin Concejo
  - LOSNCP          — contratación pública (umbral genérico, PAC 15-ene)

DOCTRINA INMUTABLE:
  D1 no emite sentencias. Produce hipótesis de coherencia normativa.
  "El sistema informa — la autoridad pública decide."
  Nunca: "incumplió", "violó", "ilegal". Siempre: "genera indicadores de riesgo".

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ── ESTADOS D1 (6 niveles, no binario) ────────────────────────────────────────

class D1Status(str, Enum):
    """
    Estados de coherencia normativa — no son veredictos, son hipótesis institucionales.

    LEGAL                — competencia clara, canal correcto, evidencia suficiente
    OBSERVADO            — brecha menor; no bloquea; amerita seguimiento
    RIESGO_COMPETENCIA   — la entidad puede no tener facultad para el acto detectado
    RIESGO_PROCEDIMIENTO — canal aprobatorio incorrecto (ej: Concejo en vez de Directorio EP)
    RIESGO_EVIDENCIA     — la competencia existe pero falta documentación de respaldo
    REQUIERE_REVIEW      — señal demasiado compleja o grave para decisión automatizada
    """
    LEGAL                = "LEGAL"
    OBSERVADO            = "OBSERVADO"
    RIESGO_COMPETENCIA   = "RIESGO_DE_COMPETENCIA"
    RIESGO_PROCEDIMIENTO = "RIESGO_DE_PROCEDIMIENTO"
    RIESGO_EVIDENCIA     = "RIESGO_DE_EVIDENCIA"
    REQUIERE_REVIEW      = "REQUIERE_REVIEW"


# ── MAPA CANÓNICO DE COMPETENCIAS (solo art. vault-verified) ──────────────────

_COMPETENCY_MAP: Dict[str, Dict[str, Any]] = {

    # ── GAD Municipal de Montecristi ──────────────────────────────────────────
    "GAD": {

        "reforma_presupuestaria": {
            "approver_standard":  "Concejo Municipal",
            "approver_alcalde":   "Alcalde (si reforma <= 10% codificado)",
            "alcalde_threshold":  10.0,        # COPFP Art. 97
            "norms_verified":     ["COPFP Art. 97", "COOTAD Art. 432"],
            "evidence_required":  [
                "Informe técnico motivado (Dirección de Planificación o Financiera)",
                "Certificación presupuestaria de disponibilidad",
                "Resolución aprobatoria (Concejo o Alcalde según monto)",
            ],
            "sat_code":  "SAT-D1-A",
            "severity":  "alto",
            "nota": (
                "El Alcalde puede aprobar reformas <= 10% del codificado directamente "
                "(COPFP Art. 97). Reformas mayores requieren Concejo Municipal. "
                "El umbral del 10% se usa en RC-7.2 como 'reform_threshold' para "
                "clasificar REFORMA_LEGITIMA vs MANIPULACION_TEMPORAL."
            ),
        },

        "liquidacion_presupuesto": {
            "approver_standard":  "Alcalde + Director Financiero GADM",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 263", "COOTAD Art. 265"],
            "evidence_required":  [
                "Cédula presupuestaria de diciembre firmada y cerrada",
                "Liquidación presupuestaria formulada antes del 31 de enero del año siguiente",
            ],
            "time_window": {
                "deadline_month": 1, "deadline_day": 31,
                "description": "31 de enero del año siguiente al ejercicio fiscal",
            },
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },

        "presupuesto_participativo": {
            "approver_standard":  "Alcalde + participación ciudadana (7 parroquias)",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 238"],
            "evidence_required":  [
                "Actas de asamblea parroquial (al menos 1 por parroquia)",
                "Cobertura documentada de las 7 parroquias del cantón Montecristi",
                "Resolución de asignación participativa vinculante",
            ],
            "sat_code":  "SAT-D1-C",
            "severity":  "medio",
            "nota": (
                "Montecristi tiene 7 parroquias. COOTAD Art. 238 obliga PP. "
                "El D4 verifica si la distribución territorial resultante es equitativa."
            ),
        },

        "contratacion_publica": {
            "approver_standard":  "Alcalde o funcionario delegado",
            "alcalde_threshold":  None,
            "norms_verified":     ["LOSNCP", "COOTAD Art. 55"],
            "evidence_required":  [
                "Plan Anual de Contratación (PAC) publicado antes del 15 de enero",
                "Proceso registrado en portal ComprasPúblicas (SERCOP)",
                "Certificación presupuestaria para el proceso",
            ],
            "time_window": {
                "pac_deadline_month": 1, "pac_deadline_day": 15,
                "description": "PAC publicado antes del 15 de enero de cada año",
            },
            "sat_code":  "SAT-D1-C",
            "severity":  "medio",
        },

        "distribucion_parroquial": {
            "approver_standard":  "Alcalde + Concejo Municipal",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 272", "CRE Art. 238"],
            "evidence_required":  [
                "Ordenanza de distribución cantonal aprobada por Concejo",
                "Criterios de equidad interterritorial documentados",
            ],
            "sat_code":  "SAT-D1-C",
            "severity":  "medio",
        },
    },

    # ── EMAI-EP (Empresa Municipal de Aseo Integral Montecristi-EP) ───────────
    "EMAI-EP": {

        "reforma_presupuestaria": {
            "approver_standard":  "Directorio de EMAI-EP",
            "approver_alcalde":   None,  # CRÍTICO: el Alcalde NO puede aprobar reformas de la EP
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 267"],
            "evidence_required":  [
                "Solicitud formal del Gerente General de EMAI-EP",
                "Resolución aprobatoria del Directorio de EMAI-EP",
                "Registro en eSIGEF EP (partida EP identificada)",
            ],
            "sat_code":  "SAT-D1-A",
            "severity":  "alto",
            "nota": (
                "CRÍTICO — SAT-X-A: una reforma en EMAI-EP que sea aprobada por "
                "Concejo Municipal en lugar del Directorio de EMAI-EP constituye "
                "un riesgo procedimental de primer orden. El Directorio de EMAI-EP "
                "es el órgano competente exclusivo (COOTAD Art. 267)."
            ),
        },

        "aprobacion_presupuesto": {
            "approver_standard":  "Directorio de EMAI-EP",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 267"],
            "evidence_required":  [
                "Resolución de aprobación del Directorio de EMAI-EP",
                "Presupuesto EMAI-EP incorporado como anexo al presupuesto GADM",
            ],
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },

        "liquidacion_presupuesto": {
            "approver_standard":  "Gerente General EMAI-EP + Director Financiero EP",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 263", "COOTAD Art. 265"],
            "evidence_required":  [
                "Cédula presupuestaria de diciembre EMAI-EP cerrada",
                "Liquidación formulada antes del 31 de enero",
            ],
            "time_window": {
                "deadline_month": 1, "deadline_day": 31,
                "description": "31 de enero del año siguiente",
            },
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },

        "contratacion_publica": {
            "approver_standard":  "Gerente General EMAI-EP",
            "alcalde_threshold":  None,
            "norms_verified":     ["LOSNCP"],
            "evidence_required":  [
                "PAC de EMAI-EP publicado antes del 15 de enero",
                "Proceso registrado en ComprasPúblicas SERCOP",
            ],
            "time_window": {
                "pac_deadline_month": 1, "pac_deadline_day": 15,
                "description": "PAC EMAI-EP publicado antes del 15 de enero",
            },
            "sat_code":  "SAT-D1-C",
            "severity":  "medio",
        },
    },

    # ── Cuerpo de Bomberos ────────────────────────────────────────────────────
    "BOMBEROS": {

        "reforma_presupuestaria": {
            "approver_standard":  "Directorio del Cuerpo de Bomberos",
            "approver_alcalde":   None,
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 267"],
            "evidence_required":  [
                "Solicitud formal del Jefe del Cuerpo de Bomberos",
                "Resolución aprobatoria del Directorio",
            ],
            "sat_code":  "SAT-D1-A",
            "severity":  "alto",
        },

        "aprobacion_presupuesto": {
            "approver_standard":  "Directorio del Cuerpo de Bomberos",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 267"],
            "evidence_required":  ["Resolución de aprobación del Directorio"],
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },

        "liquidacion_presupuesto": {
            "approver_standard":  "Director Financiero Bomberos + Jefe de Bomberos",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 263"],
            "evidence_required":  ["Cédula presupuestaria de diciembre Bomberos"],
            "time_window": {"deadline_month": 1, "deadline_day": 31,
                            "description": "31 de enero del año siguiente"},
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },
    },

    # ── Patronato Municipal ───────────────────────────────────────────────────
    "PATRONATO": {

        "reforma_presupuestaria": {
            "approver_standard":  "Directorio del Patronato Municipal",
            "approver_alcalde":   None,
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 267"],
            "evidence_required":  [
                "Solicitud del Director del Patronato",
                "Resolución aprobatoria del Directorio del Patronato",
            ],
            "sat_code":  "SAT-D1-A",
            "severity":  "alto",
        },

        "aprobacion_presupuesto": {
            "approver_standard":  "Directorio del Patronato",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 267"],
            "evidence_required":  ["Resolución de aprobación del Directorio"],
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },

        "liquidacion_presupuesto": {
            "approver_standard":  "Director Financiero Patronato",
            "alcalde_threshold":  None,
            "norms_verified":     ["COOTAD Art. 263"],
            "evidence_required":  ["Cédula presupuestaria de diciembre Patronato"],
            "time_window": {"deadline_month": 1, "deadline_day": 31,
                            "description": "31 de enero del año siguiente"},
            "sat_code":  "SAT-D1-B",
            "severity":  "medio",
        },
    },
}

# ── MAPA D3 → D1 ACTION ───────────────────────────────────────────────────────
# Qué D3 pattern activa qué chequeo D1

D3_TO_D1_ACTION: Dict[str, Tuple[Optional[str], str]] = {
    "MANIPULACION_TEMPORAL":  (
        "reforma_presupuestaria",
        "Concentracion Q4 atipica detectada — verificar si reforma presupuestaria fue aprobada por canal correcto y organo competente",
    ),
    "CIERRE_TARDIO":          (
        "liquidacion_presupuesto",
        "Patron de concentracion en Q4 tardio — verificar cumplimiento del plazo 31 de enero para liquidacion",
    ),
    "REFORMA_LEGITIMA":       (
        "reforma_presupuestaria",
        "Reforma presupuestaria detectada dentro del umbral COPFP Art. 97 — confirmar que el canal aprobatorio fue correcto",
    ),
    "INFRAEJECUCION_CRONICA": (
        "contratacion_publica",
        "Subejecucion cronica sostenida — verificar si el PAC fue publicado en plazo y si los procesos de contratacion fueron iniciados",
    ),
    "EXPANSION_TARDIA":       (
        "reforma_presupuestaria",
        "Expansion presupuestaria tardia en Q3-Q4 — verificar si requirio suplemento de credito aprobado formalmente",
    ),
    "RECUPERACION_VERIFICADA":(
        "reforma_presupuestaria",
        "Recuperacion presupuestaria verificada — confirmar que las reformas intermedias siguieron el canal aprobatorio correcto",
    ),
    "DETERIORO_PROGRESIVO":   (
        "contratacion_publica",
        "Deterioro progresivo de ejecucion — verificar si contratos no fueron renovados o si PAC esta incompleto",
    ),
    "PARALISIS_ESTRUCTURAL":  (
        "contratacion_publica",
        "Paralisis estructural de ejecucion — posible bloqueo en contratacion publica; verificar PAC y procesos en SERCOP",
    ),
    "SHOCK_EXTERNO":          (
        "reforma_presupuestaria",
        "Shock externo reconocido — una reforma de emergencia requiere delegacion formal aunque sea urgente",
    ),
    "SIN_PATRON_CLARO":       (
        None,
        "Evidencia presupuestaria insuficiente para inferencia D1",
    ),
}

# ── MAPA D4 → D1 TERRITORIAL ACTION ──────────────────────────────────────────

D4_TO_D1_ACTION: Dict[str, Tuple[Optional[str], str]] = {
    "CONCENTRACION_TERRITORIAL": (
        "presupuesto_participativo",
        "Concentracion territorial extrema — verificar si el PP cubrio las 7 parroquias con equidad",
    ),
    "REZAGO_PERSISTENTE":        (
        "presupuesto_participativo",
        "Rezago persistente en parroquias perifericas — verificar si fueron incluidas con peso real en el PP",
    ),
    "CAPTURA_CAPITAL":           (
        "distribucion_parroquial",
        "Captura por cabecera cantonal — verificar si la ordenanza de distribucion respeta CRE Art. 238",
    ),
    "INEQUIDAD_HIDRICA":         (
        "contratacion_publica",
        "Inequidad hidrica en parroquias rurales — verificar contratos de agua ejecutados en zonas de NBI alto",
    ),
    "SESGO_DISTRIBUTIVO":        (
        "presupuesto_participativo",
        "Sesgo distributivo sistematico — verificar base normativa de la asignacion parroquial",
    ),
    "SIN_PATRON":                (None, "Sin patron territorial — D1 no se activa"),
}


# ── DATACLASSES ───────────────────────────────────────────────────────────────

@dataclass
class CompetencyContext:
    """
    Contexto para un chequeo de competencia.

    entity_id          — "GAD" | "EMAI-EP" | "BOMBEROS" | "PATRONATO"
    action_type        — clave del mapa de competencias
    reforma_pct        — porcentaje del codificado (para umbral Alcalde)
    d3_pattern         — patrón D3 que activó este chequeo (puede ser vacío)
    d4_pattern         — patrón D4 que activó este chequeo territorial
    n_parroquias_pp    — parroquias cubiertas en PP (para check COOTAD Art. 238)
    has_cedula_data    — si hay cédula disponible en el sistema
    evidence_confirmed — lista de evidencia que se puede confirmar desde los datos
    trigger_reason     — texto libre que explica por qué se activa el chequeo
    """
    entity_id:          str
    action_type:        str
    reforma_pct:        float        = 0.0
    d3_pattern:         str          = ""
    d4_pattern:         str          = ""
    n_parroquias_pp:    int          = 0
    n_parroquias_total: int          = 7       # Montecristi tiene 7 parroquias
    has_cedula_data:    bool         = False
    evidence_confirmed: List[str]    = field(default_factory=list)
    trigger_reason:     str          = ""


@dataclass
class D1CompetencyResult:
    """
    Resultado de un chequeo de competencia RC-D1.1.

    Campos clave:
      status            — D1Status (6 estados, no binario)
      confidence        — 0.0–1.0 (propaga desde D3/D4; < 0.25 → observational)
      observational     — True si confidence < 0.25 (no emite juicio sobre hechos)
      approver_required — quién debía autorizar el acto según la norma
      norm_refs         — artículos verificados aplicables
      evidence_required — documentos que deben existir
      evidence_gaps     — documentos no confirmados en datos disponibles
      counterfactual    — qué haría este resultado LEGAL (para guía institucional)
      sat_code          — código SAT asociado (si aplica)
      narrative         — texto explicativo tension-aware (no acusatorio)
    """
    entity_id:          str
    action_type:        str
    status:             D1Status
    confidence:         float
    observational:      bool
    approver_required:  str
    norm_refs:          List[str]
    evidence_required:  List[str]
    evidence_gaps:      List[str]
    evidence_confirmed: List[str]
    counterfactual:     str          # "Para que sea LEGAL se requiere: ..."
    sat_code:           str
    severity:           str          # "alto" | "medio" | "bajo"
    trigger_reason:     str
    narrative:          str
    d3_pattern:         str  = ""
    d4_pattern:         str  = ""


# ── MOTOR DE CHEQUEO ──────────────────────────────────────────────────────────

def check_competency(
    ctx: CompetencyContext,
    d3_confidence: float = 0.10,
    d4_confidence: float = 0.50,
) -> D1CompetencyResult:
    """
    Evalúa si una acción detectada es coherente con el marco competencial
    de la entidad, según normas vault-verified.

    Retorna D1CompetencyResult con status, gaps, narrative y counterfactual.

    Doctrina: no emite juicios de culpabilidad — produce hipótesis de coherencia.
    """
    entity_rules = _COMPETENCY_MAP.get(ctx.entity_id, {})
    action_rules  = entity_rules.get(ctx.action_type, {})

    # Si no hay regla para esta combinación → OBSERVADO (insuficiente para juicio)
    if not action_rules:
        return _make_no_rule_result(ctx, d3_confidence)

    # Confianza base: mínimo entre D3 y D4 (la cadena es tan fuerte como su eslabón más débil)
    base_conf = min(d3_confidence, d4_confidence) if d4_confidence > 0 else d3_confidence
    # Ajuste por disponibilidad de cédula
    if not ctx.has_cedula_data:
        base_conf *= 0.60
    conf = round(max(0.05, min(0.95, base_conf)), 4)
    obs  = conf < 0.25

    norms    = action_rules.get("norms_verified", [])
    evidence = action_rules.get("evidence_required", [])
    sat_code = action_rules.get("sat_code", "SAT-D1-X")
    severity = action_rules.get("severity", "medio")
    approver = action_rules.get("approver_standard", "Órgano competente no especificado")

    # Detectar gaps: qué evidencia requerida NO está confirmada
    gaps      = [e for e in evidence if e not in ctx.evidence_confirmed]
    confirmed = [e for e in evidence if e in ctx.evidence_confirmed]

    # ── Lógica de status ──────────────────────────────────────────────────────

    status = _compute_status(ctx, action_rules, gaps, conf, obs)

    # ── Narrativa tension-aware ───────────────────────────────────────────────
    narrative = _build_narrative(ctx, status, approver, norms, gaps, conf, obs)

    # ── Counterfactual ────────────────────────────────────────────────────────
    counterfactual = _build_counterfactual(ctx, action_rules, status)

    return D1CompetencyResult(
        entity_id          = ctx.entity_id,
        action_type        = ctx.action_type,
        status             = status,
        confidence         = conf,
        observational      = obs,
        approver_required  = approver,
        norm_refs          = norms,
        evidence_required  = evidence,
        evidence_gaps      = gaps,
        evidence_confirmed = confirmed,
        counterfactual     = counterfactual,
        sat_code           = sat_code if status not in (D1Status.LEGAL, D1Status.OBSERVADO) else "",
        severity           = severity,
        trigger_reason     = ctx.trigger_reason,
        narrative          = narrative,
        d3_pattern         = ctx.d3_pattern,
        d4_pattern         = ctx.d4_pattern,
    )


def _compute_status(
    ctx:          CompetencyContext,
    rules:        Dict[str, Any],
    gaps:         List[str],
    conf:         float,
    obs:          bool,
) -> D1Status:
    """Determina el D1Status según las reglas y el contexto."""

    # Insuficiente evidencia estructural → siempre OBSERVADO
    if not ctx.has_cedula_data:
        return D1Status.OBSERVADO

    # Reforma presupuestaria de EP → verificar que NO pasó por Concejo
    if ctx.action_type == "reforma_presupuestaria" and ctx.entity_id != "GAD":
        alcalde_th = rules.get("alcalde_threshold")
        if alcalde_th is not None:
            # Entidad no-GAD con umbral Alcalde: no debería existir
            return D1Status.RIESGO_COMPETENCIA
        # EP sin umbral Alcalde → el Directorio es el único órgano competente
        # Si hay gaps en evidencia del Directorio → riesgo procedimiento
        if any("Directorio" in g or "Resolución" in g for g in gaps):
            return D1Status.RIESGO_PROCEDIMIENTO if not obs else D1Status.OBSERVADO

    # GAD reforma: verificar umbral Alcalde
    if ctx.action_type == "reforma_presupuestaria" and ctx.entity_id == "GAD":
        alcalde_th = rules.get("alcalde_threshold", 10.0)
        if ctx.reforma_pct > alcalde_th:
            # Supera umbral → debió pasar por Concejo
            if any("Concejo" in g or "Resolución" in g for g in gaps):
                return D1Status.RIESGO_PROCEDIMIENTO if not obs else D1Status.OBSERVADO
        else:
            # Dentro del umbral Alcalde → LEGAL si hay evidencia suficiente
            if not gaps:
                return D1Status.LEGAL

    # PP: verificar cobertura parroquial
    if ctx.action_type == "presupuesto_participativo":
        if ctx.n_parroquias_pp > 0 and ctx.n_parroquias_pp < ctx.n_parroquias_total:
            return D1Status.RIESGO_EVIDENCIA
        if ctx.n_parroquias_pp == 0 and not obs:
            return D1Status.RIESGO_EVIDENCIA

    # Sin gaps → LEGAL (solo con conf suficiente)
    if not gaps and conf >= 0.40:
        return D1Status.LEGAL

    # Gaps pero baja confianza → OBSERVADO
    if obs:
        return D1Status.OBSERVADO

    # Gaps con confianza media → RIESGO_EVIDENCIA
    if gaps and conf >= 0.25:
        return D1Status.RIESGO_EVIDENCIA

    # Señal compleja → REQUIERE_REVIEW
    return D1Status.REQUIERE_REVIEW


def _build_narrative(
    ctx:      CompetencyContext,
    status:   D1Status,
    approver: str,
    norms:    List[str],
    gaps:     List[str],
    conf:     float,
    obs:      bool,
) -> str:
    """
    Texto explicativo tension-aware. Nunca acusatorio.
    Máximo ~300 caracteres para eficiencia en prompt.
    """
    obs_tag  = " [OBSERVACIONAL]" if obs else ""
    norm_str = " · ".join(norms[:2]) if norms else "normativa aplicable"

    status_phrases = {
        D1Status.LEGAL:                "La accion detectada presenta coherencia con el marco competencial",
        D1Status.OBSERVADO:            "La evidencia disponible es insuficiente para una valoracion definitiva",
        D1Status.RIESGO_COMPETENCIA:   "La accion detectada genera indicadores de potencial exceso de competencia",
        D1Status.RIESGO_PROCEDIMIENTO: "El canal aprobatorio requerido puede no haberse seguido",
        D1Status.RIESGO_EVIDENCIA:     "La competencia existe pero la documentacion de respaldo no es verificable",
        D1Status.REQUIERE_REVIEW:      "La complejidad de la señal supera el umbral de valoracion automatizada",
    }
    phrase = status_phrases.get(status, "Valoracion pendiente")
    gap_note = f" Brechas: {', '.join(gaps[:2])}." if gaps else ""

    return (
        f"[D1{obs_tag}] {ctx.entity_id} — {ctx.action_type}: "
        f"{phrase} (conf={conf:.0%}). "
        f"Aprobador requerido: {approver}. "
        f"Base normativa: {norm_str}.{gap_note}"
    )


def _build_counterfactual(
    ctx:    CompetencyContext,
    rules:  Dict[str, Any],
    status: D1Status,
) -> str:
    """
    Qué haría este resultado LEGAL — guía positiva para la autoridad institucional.
    Solo aplica cuando hay riesgo detectado.
    """
    if status == D1Status.LEGAL:
        return "La accion muestra coherencia con el marco normativo vigente."

    approver = rules.get("approver_standard", "órgano competente")
    evidence = rules.get("evidence_required", [])
    norms    = rules.get("norms_verified", [])

    evidence_list = "; ".join(f"({i+1}) {e}" for i, e in enumerate(evidence[:3]))
    norm_str = ", ".join(norms[:2])

    return (
        f"Para que la accion sea coherente con el marco normativo: "
        f"el aprobador formal debe ser {approver} "
        f"({norm_str}). "
        f"Documentacion requerida: {evidence_list}."
    )


def _make_no_rule_result(ctx: CompetencyContext, d3_conf: float) -> D1CompetencyResult:
    """Resultado cuando no hay regla para la combinación entidad+acción."""
    return D1CompetencyResult(
        entity_id          = ctx.entity_id,
        action_type        = ctx.action_type,
        status             = D1Status.OBSERVADO,
        confidence         = round(d3_conf * 0.5, 4),
        observational      = True,
        approver_required  = "No especificado en mapa RC-D1.1",
        norm_refs          = [],
        evidence_required  = [],
        evidence_gaps      = [],
        evidence_confirmed = [],
        counterfactual     = "Verificar en vault la regla competencial aplicable para esta combinación.",
        sat_code           = "",
        severity           = "bajo",
        trigger_reason     = ctx.trigger_reason,
        narrative          = (
            f"[D1-OBSERVACIONAL] {ctx.entity_id} — {ctx.action_type}: "
            f"combinación no registrada en mapa RC-D1.1. "
            f"Verificar en vault el artículo aplicable."
        ),
        d3_pattern         = ctx.d3_pattern,
        d4_pattern         = ctx.d4_pattern,
    )


# ── CONSULTA DIRECTA ──────────────────────────────────────────────────────────

def get_entity_competencies(entity_id: str) -> List[str]:
    """Lista de acciones reguladas para una entidad."""
    return list(_COMPETENCY_MAP.get(entity_id, {}).keys())


def get_approver(entity_id: str, action_type: str, reforma_pct: float = 0.0) -> str:
    """Quién debe aprobar una acción específica de una entidad."""
    rules = _COMPETENCY_MAP.get(entity_id, {}).get(action_type, {})
    if not rules:
        return "No registrado en RC-D1.1"

    alcalde_th = rules.get("alcalde_threshold")
    if alcalde_th is not None and reforma_pct <= alcalde_th and reforma_pct > 0:
        return rules.get("approver_alcalde", rules.get("approver_standard", ""))

    return rules.get("approver_standard", "Órgano competente")


def get_norm_refs(entity_id: str, action_type: str) -> List[str]:
    """Artículos verificados que rigen una acción."""
    return _COMPETENCY_MAP.get(entity_id, {}).get(action_type, {}).get("norms_verified", [])


def get_evidence_required(entity_id: str, action_type: str) -> List[str]:
    """Documentación requerida para una acción."""
    return _COMPETENCY_MAP.get(entity_id, {}).get(action_type, {}).get("evidence_required", [])


def get_d1_competency_block(entity_id: str) -> str:
    """
    Bloque compacto de contexto competencial para prompt injection.
    Describe qué puede hacer la entidad y bajo qué norma.
    Máx ~250 tokens.
    """
    rules = _COMPETENCY_MAP.get(entity_id)
    if not rules:
        return ""

    lines = [f"[D1-COMPETENCIAS:{entity_id}]"]
    for action, r in list(rules.items())[:4]:
        approver = r.get("approver_standard", "")
        norms    = ", ".join(r.get("norms_verified", [])[:2])
        lines.append(f"  {action}: aprobador={approver} [{norms}]")

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D1.1 Competency Graph — QUIRA OS")
    print("=" * 65)

    entities = list(_COMPETENCY_MAP.keys())
    for ent in entities:
        actions = get_entity_competencies(ent)
        print(f"\n  {ent}: {len(actions)} acciones reguladas")
        for act in actions:
            norms = get_norm_refs(ent, act)
            app   = get_approver(ent, act)
            print(f"    {act:<35} → {app[:40]} [{', '.join(norms[:2])}]")

    print("\n── Test: EMAI-EP reforma presupuestaria ──")
    ctx = CompetencyContext(
        entity_id    = "EMAI-EP",
        action_type  = "reforma_presupuestaria",
        d3_pattern   = "MANIPULACION_TEMPORAL",
        has_cedula_data = True,
        evidence_confirmed = [],  # sin evidencia del Directorio confirmada
        trigger_reason = "Concentracion Q4 atipica en EMAI-EP",
    )
    result = check_competency(ctx, d3_confidence=0.45)
    print(f"  Status    : {result.status.value}")
    print(f"  Confidence: {result.confidence:.0%}")
    print(f"  Approver  : {result.approver_required}")
    print(f"  SAT       : {result.sat_code}")
    print(f"  Gaps      : {result.evidence_gaps}")
    print(f"  Narrative : {result.narrative[:120]}...")

    print("\n── Test: GAD reforma dentro umbral Alcalde ──")
    ctx2 = CompetencyContext(
        entity_id    = "GAD",
        action_type  = "reforma_presupuestaria",
        d3_pattern   = "REFORMA_LEGITIMA",
        reforma_pct  = 7.5,    # < 10% → Alcalde puede aprobar
        has_cedula_data = True,
        evidence_confirmed = [
            "Informe técnico motivado (Dirección de Planificación o Financiera)",
            "Certificación presupuestaria de disponibilidad",
            "Resolución aprobatoria (Concejo o Alcalde según monto)",
        ],
        trigger_reason = "REFORMA_LEGITIMA detectada (7.5% codificado)",
    )
    result2 = check_competency(ctx2, d3_confidence=0.72)
    print(f"  Status    : {result2.status.value}")
    print(f"  Confidence: {result2.confidence:.0%}")
    print(f"  Counterfactual: {result2.counterfactual[:80]}...")

    print("\n── Test: GAD Presupuesto Participativo — parroquias incompletas ──")
    ctx3 = CompetencyContext(
        entity_id        = "GAD",
        action_type      = "presupuesto_participativo",
        d4_pattern       = "CONCENTRACION_TERRITORIAL",
        n_parroquias_pp  = 4,   # solo 4 de 7 parroquias
        n_parroquias_total = 7,
        has_cedula_data  = True,
        evidence_confirmed = [],
        trigger_reason   = "CONCENTRACION_TERRITORIAL — 4/7 parroquias en PP",
    )
    result3 = check_competency(ctx3, d3_confidence=0.70, d4_confidence=0.72)
    print(f"  Status    : {result3.status.value}")
    print(f"  Norm refs : {result3.norm_refs}")
    print(f"  Narrative : {result3.narrative[:100]}...")
