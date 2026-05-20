"""
sentinel/normative_binding.py
RC-7.2 — Sub-motor 4: Cierre Normativo del Loop Longitudinal
QUIRA OS · Dylus Lab © 2026-05-20

Conecta: InstitutionalClass → SAT → vault_enricher → legal_router

Este es el verdadero cierre del loop:
  datos presupuestarios
    → análisis matemático (longitudinal_engine)
    → patrones institucionales (administrative_patterns)
    → clasificación ejecutiva (institutional_classifier)
    → ESTE MÓDULO: vinculación normativa (normative_binding)
    → bloque de contexto para Claude Haiku

Doctrina: ninguna interpretación sin norma. Ninguna norma sin evidencia.
Trazabilidad total: patrón → SAT → vault nota → artículo legal → cita.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from sentinel.institutional_classifier import InstitutionalClass
from sentinel.administrative_patterns import PatternSet
from sentinel.longitudinal_engine import LongitudinalResult


# ── TIPOS ─────────────────────────────────────────────────────────────────────

@dataclass
class NormativeBinding:
    """
    Resultado del cierre normativo para una situación de ejecución.

    clase:            clase institucional (del sub-motor 3)
    sat_codes:        SATs confirmados (de la clasificación)
    legal_block:      bloque normativo enriquecido para system prompt (legal_router)
    vault_block:      bloque vault para system prompt (vault_enricher)
    full_context:     bloque completo = legal + vault + diagnóstico RC-7.2
    provenance:       trazabilidad completa (SATs, notas vault, artículos)
    query_synthetic:  query sintética construida para activar routing correcto
    """
    clase:           str
    sat_codes:       list[str]        = field(default_factory=list)
    legal_block:     str              = ""
    vault_block:     str              = ""
    full_context:    str              = ""
    provenance:      dict             = field(default_factory=dict)
    query_synthetic: str              = ""


# ── QUERY SINTÉTICA POR SAT ───────────────────────────────────────────────────
# Genera una query que activa el routing correcto en vault_enricher y legal_router
# sin depender del lenguaje natural del usuario.

_SAT_TO_QUERY: dict[str, str] = {
    "SAT-IX":  (
        "legalidad normativa COOTAD copfp constitucion rendicion de cuentas "
        "transparencia institucional marco legal"
    ),
    "SAT-X-A": (
        "contratacion sercop compraspublicas adjudicar fraccionamiento "
        "infima cuantia menor cuantia proceso contractual losncp"
    ),
    "SAT-X-B": (
        "reforma presupuestaria modificacion presupuestaria reasignar "
        "reforma poa reforma al poa modificar presupuesto"
    ),
    "SAT-XI":  (
        "ejecucion presupuestaria devengado esigef tasa ejecucion "
        "infraejecucion fondos bloqueados inversion bloqueada grupos 7 grupos 8"
    ),
    "SAT-XII": (
        "equidad territorial iet brecha territorial inequidad per capita "
        "parroquia rural distribucion inequitativa nbi alto regresividad"
    ),
}

# Query complementaria por clase institucional
_CLASS_TO_QUERY: dict[str, str] = {
    "PARALISIS_ESTRUCTURAL":   "paralisis ejecucion presupuestaria devengado esigef fondon bloqueados",
    "INFRAEJECUCION_CRONICA":  "ejecucion presupuestaria devengado poa pac programacion anual",
    "MANIPULACION_TEMPORAL":   "contratacion sercop fraccionamiento pac adjudicacion",
    "EXPANSION_TARDIA":        "inversion transferencias recursos per capita distribucion fondos poa",
    "REFORMA_LEGITIMA":        "reforma presupuestaria reasignacion reforma poa modificar presupuesto",
    "DETERIORO_PROGRESIVO":    "ejecucion presupuestaria devengado sostenibilidad fiscal",
    "CIERRE_TARDIO":           "contratacion pac ejecucion presupuestaria programacion anual",
    "RECUPERACION_VERIFICADA": "presupuesto participativo poa plan operativo programacion",
    "SHOCK_EXTERNO":           "reforma presupuestaria modificacion presupuestaria reasignar",
    "SIN_PATRON_CLARO":        "presupuesto participativo poa programacion anual ejecucion",
}


def _build_synthetic_query(
    ic:          InstitutionalClass,
    ps:          PatternSet,
    result:      LongitudinalResult,
) -> str:
    """
    Construye query sintética combinando:
    1. Términos de los SAT codes implicados
    2. Términos adicionales de la clase institucional
    3. Términos contextuales del resultado matemático
    """
    parts: list[str] = []

    # Términos SAT (máximo 2 SATs para control de tokens)
    for sat in ic.sat_codes[:2]:
        if sat in _SAT_TO_QUERY:
            parts.append(_SAT_TO_QUERY[sat])

    # Términos de clase (si no ya cubiertos por SAT)
    class_query = _CLASS_TO_QUERY.get(ic.clase, "")
    if class_query and class_query not in " ".join(parts):
        parts.append(class_query)

    # Contexto matemático: añadir viabilidad si Ti muy baja
    if result.ti_series and result.ti_series[-1] < 10.0:
        parts.append("viable reasignar modificar presupuesto es posible")

    query = " ".join(parts)
    # Limitar longitud para no sobrecargar los routers
    return query[:600]


# ── ORQUESTADOR PRINCIPAL ─────────────────────────────────────────────────────

def bind(
    ic:     InstitutionalClass,
    ps:     PatternSet,
    result: LongitudinalResult,
) -> NormativeBinding:
    """
    Cierra el loop normativo:
    InstitutionalClass + PatternSet + LongitudinalResult → NormativeBinding

    Estrategia:
    1. Construye query sintética → activa vault_enricher + legal_router
    2. Recupera bloque vault (si disponible)
    3. Recupera bloque legal estático (COOTAD/COPLAFIP/CRE)
    4. Ensambla bloque completo para system prompt de Claude Haiku
    5. Captura provenance completo

    Returns:
        NormativeBinding listo para inyectar en sentinel.py
    """
    query_synthetic = _build_synthetic_query(ic, ps, result)

    # ── Capa 1: Bloque legal estático (COOTAD/COPLAFIP/CRE) ──────────────────
    legal_block = ""
    try:
        from sentinel.legal_router import find_legal_refs, build_legal_prompt_block
        legal_block = build_legal_prompt_block(query_synthetic)
    except Exception:
        pass  # legal_router no disponible → continúa sin bloque

    # ── Capa 2: Bloque vault (notas institucionales verificadas) ──────────────
    vault_block   = ""
    vault_ctx     = {}
    try:
        from sentinel.vault_enricher import get_vault_normative_context, build_vault_prompt_block
        vault_ctx   = get_vault_normative_context(query_synthetic)
        vault_block = build_vault_prompt_block(query_synthetic)
    except Exception:
        pass  # vault no disponible → continúa sin bloque

    # ── Capa 3: Diagnóstico RC-7.2 (bloque ejecutivo) ─────────────────────────
    from sentinel.institutional_classifier import describe_for_sentinel
    rc72_block = describe_for_sentinel(ic, result)

    # ── Ensamblar bloque completo ─────────────────────────────────────────────
    parts: list[str] = []
    if legal_block:
        parts.append(legal_block)
    if vault_block:
        parts.append(vault_block)
    if rc72_block:
        parts.append(rc72_block)

    full_context = "\n\n".join(parts) if parts else rc72_block

    # ── Provenance completo ───────────────────────────────────────────────────
    from sentinel.vault_enricher import provenance_to_dict
    vault_prov = provenance_to_dict(vault_ctx) if vault_ctx else {}

    provenance = {
        "clase":           ic.clase,
        "confianza":       ic.confianza,
        "sat_codes":       ic.sat_codes,
        "patterns":        [p.nombre for p in ps.patterns],
        "sat_implied":     ps.sat_implied,
        "avep_riesgo":     ic.avep_riesgo,
        "avep_score":      ic.avep_score,
        "flags":           ic.flags,
        "query_synthetic": query_synthetic[:200],
        "vault":           vault_prov,
        "longitudinal": {
            "n_periodos":    result.n_periodos,
            "ti_mean":       result.ti_mean,
            "ti_last":       result.ti_series[-1] if result.ti_series else None,
            "reforma_net":   result.reforma_net,
            "raw_flags":     result.raw_flags,
        },
    }

    return NormativeBinding(
        clase            = ic.clase,
        sat_codes        = ic.sat_codes,
        legal_block      = legal_block,
        vault_block      = vault_block,
        full_context     = full_context,
        provenance       = provenance,
        query_synthetic  = query_synthetic,
    )


# ── PIPELINE COMPLETO RC-7.2 ──────────────────────────────────────────────────

def run_rc72_pipeline(
    records: list,  # list[BudgetRecord]
) -> tuple[LongitudinalResult, PatternSet, InstitutionalClass, NormativeBinding]:
    """
    Pipeline completo RC-7.2:
    records → LongitudinalResult → PatternSet → InstitutionalClass → NormativeBinding

    Args:
        records: lista de BudgetRecord (del longitudinal_engine)

    Returns:
        Tupla (result, ps, ic, binding) — todos los artefactos del pipeline.
    """
    from sentinel.longitudinal_engine    import analyze_series
    from sentinel.administrative_patterns import detect_patterns
    from sentinel.institutional_classifier import classify

    result  = analyze_series(records)
    ps      = detect_patterns(result)
    ic      = classify(ps, result)
    binding = bind(ic, ps, result)

    return result, ps, ic, binding


def build_rc72_prompt_block(records: list) -> str:
    """
    Shortcut: ejecuta el pipeline y retorna solo el full_context para system prompt.
    Retorna "" si records está vacío.
    """
    if not records:
        return ""
    _, _, _, binding = run_rc72_pipeline(records)
    return binding.full_context


def summarize_binding(binding: NormativeBinding) -> dict:
    """Serializa NormativeBinding a dict compacto para logs y session_state."""
    return {
        "clase":           binding.clase,
        "sat_codes":       binding.sat_codes,
        "has_legal":       bool(binding.legal_block),
        "has_vault":       bool(binding.vault_block),
        "provenance":      binding.provenance,
    }


# ── INTEGRACIÓN DIRECTA CON SENTINEL ─────────────────────────────────────────

def get_rc72_context_for_query(
    query:   str,
    records: list | None = None,
) -> str:
    """
    Punto de entrada para sentinel.py.
    Si records está disponible: ejecuta pipeline completo.
    Si no: usa solo el routing normativo estático (fallback degradado).

    Args:
        query:   pregunta del usuario (para routing normativo)
        records: lista de BudgetRecord si el contexto presupuestario está disponible

    Returns:
        Bloque de contexto para system prompt. "" si nada aplica.
    """
    if records:
        try:
            return build_rc72_prompt_block(records)
        except Exception:
            pass  # fallback al routing estático

    # Fallback: solo legal_router sin datos longitudinales
    try:
        from sentinel.legal_router import build_legal_prompt_block
        return build_legal_prompt_block(query)
    except Exception:
        return ""
