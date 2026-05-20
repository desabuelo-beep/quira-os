"""
sentinel/institutional_classifier.py
RC-7.2 — Sub-motor 3: Clasificación Institucional Ejecutiva
QUIRA OS · Dylus Lab © 2026-05-20

Convierte PatternSet → InstitutionalClass:
interpretación ejecutiva legible para Concejo, ciudadanía y Contraloría.

Taxonomía de clases (propiedades AVEP-compatibles):
  EXPANSION_TARDIA          — crecimiento presupuestario + ejecución rezagada
  REFORMA_LEGITIMA          — reforma presupuestaria con evidencia de viabilidad
  PARALISIS_ESTRUCTURAL     — freeze + decline + sin recuperación
  MANIPULACION_TEMPORAL     — Q4_PUSH + burst sin contexto normativo
  CIERRE_TARDIO             — Q4_PUSH aislado con métricas históricas razonables
  DETERIORO_PROGRESIVO      — gradual decline sin patrón de reforma
  RECUPERACION_VERIFICADA   — recovery con contexto positivo
  INFRAEJECUCION_CRONICA    — structural flat multi-periodo
  SHOCK_EXTERNO             — discontinuidad severa atribuible a factor externo
  SIN_PATRON_CLARO          — datos insuficientes o patrones contradictorios

Doctrina: la clase es un punto de partida para el análisis, no un veredicto.
Contraloría ve la evidencia, no la clase.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from sentinel.administrative_patterns import PatternSet, Pattern
from sentinel.longitudinal_engine import LongitudinalResult


# ── TIPOS ─────────────────────────────────────────────────────────────────────

@dataclass
class InstitutionalClass:
    """
    Clasificación ejecutiva de un patrón de ejecución presupuestaria.

    clase:         código canónico (ver taxonomía arriba)
    confianza:     0.0–1.0 (heredada del patrón dominante + reglas de composición)
    avep_riesgo:   nivel AVEP de riesgo institucional
    avep_score:    score AVEP aproximado (0–100) de la situación de ejecución
    sat_codes:     SAT codes confirmados (no solo hint)
    descripcion:   texto ejecutivo en español para informe
    recomendacion: acción inmediata recomendada (trazable a norma)
    flags:         lista de flags de diagnóstico adicionales
    """
    clase:         str
    confianza:     float
    avep_riesgo:   str              = "MEDIO"
    avep_score:    float            = 50.0
    sat_codes:     list[str]        = field(default_factory=list)
    descripcion:   str              = ""
    recomendacion: str              = ""
    flags:         list[str]        = field(default_factory=list)


# ── AVEP RISK MAPPING ─────────────────────────────────────────────────────────
# Compatible con escala AVEP: Excelencia≥90 | Mandato 70-90 | Transición 50-70
#                              Ocurrencia 30-50 | Ruptura<30

_AVEP_MAP: dict[str, tuple[str, float]] = {
    "PARALISIS_ESTRUCTURAL":    ("Ruptura Sistémica",     18.0),
    "INFRAEJECUCION_CRONICA":   ("Ruptura Sistémica",     22.0),
    "MANIPULACION_TEMPORAL":    ("Ocurrencia Crítica",    35.0),
    "DETERIORO_PROGRESIVO":     ("Ocurrencia Crítica",    38.0),
    "EXPANSION_TARDIA":         ("Transición Crítica",    48.0),
    "SHOCK_EXTERNO":            ("Transición Crítica",    50.0),
    "CIERRE_TARDIO":            ("Transición Crítica",    55.0),
    "REFORMA_LEGITIMA":         ("Gestión por Mandato",   72.0),
    "RECUPERACION_VERIFICADA":  ("Gestión por Mandato",   75.0),
    "SIN_PATRON_CLARO":         ("Transición Crítica",    52.0),
}


# ── REGLAS DE CLASIFICACIÓN ───────────────────────────────────────────────────

def _has(ps: PatternSet, nombre: str) -> bool:
    """True si el PatternSet contiene el patrón indicado."""
    return any(p.nombre == nombre for p in ps.patterns)


def _confidence(ps: PatternSet, nombre: str) -> float:
    """Confianza del patrón indicado, o 0.0 si no está."""
    for p in ps.patterns:
        if p.nombre == nombre:
            return p.confianza
    return 0.0


def _classify(
    ps:     PatternSet,
    result: LongitudinalResult,
) -> InstitutionalClass:
    """
    Motor de clasificación por reglas de composición de patrones.
    Orden de evaluación: mayor riesgo primero (fail-safe).
    """

    # ── PARALISIS_ESTRUCTURAL ─────────────────────────────────────────────────
    # FREEZE sostenido + GRADUAL_DECLINE + sin RECOVERY
    # Nota: ti_mean puede ser alto si la serie incluye años históricos buenos;
    # el ti del último periodo es el indicador determinante de parálisis.
    _ti_last = result.ti_series[-1] if result.ti_series else 100.0
    if (
        _has(ps, "FREEZE")
        and _has(ps, "GRADUAL_DECLINE")
        and not _has(ps, "RECOVERY")
        and (_ti_last < 10.0 or result.ti_mean < 15.0)
    ):
        conf = (_confidence(ps, "FREEZE") + _confidence(ps, "GRADUAL_DECLINE")) / 2
        return InstitutionalClass(
            clase          = "PARALISIS_ESTRUCTURAL",
            confianza      = round(conf, 3),
            avep_riesgo    = "Ruptura Sistémica",
            avep_score     = 18.0,
            sat_codes      = ["SAT-XI"],
            descripcion    = (
                f"Parálisis estructural de ejecución: Ti promedio {result.ti_mean:.1f}% "
                f"con tendencia negativa sostenida. No se detecta recuperación. "
                "Posible bloqueo eSIGEF o ausencia de proyectos ejecutables."
            ),
            recomendacion  = (
                "Activar revisión urgente de causales de bloqueo en eSIGEF. "
                "Convocar sesión técnica urgente Dirección Financiera + Planificación. "
                "Verificar vigencia del PAC y certificaciones presupuestarias."
            ),
            flags          = ["BLOQUEO_PROBABLE", "REQUIERE_INFORME_TECNICO"],
        )

    # ── INFRAEJECUCION_CRONICA ────────────────────────────────────────────────
    # STRUCTURAL_FLAT multi-periodo
    if _has(ps, "STRUCTURAL_FLAT") and result.n_periodos >= 3:
        conf = _confidence(ps, "STRUCTURAL_FLAT")
        return InstitutionalClass(
            clase          = "INFRAEJECUCION_CRONICA",
            confianza      = round(conf, 3),
            avep_riesgo    = "Ruptura Sistémica",
            avep_score     = 22.0,
            sat_codes      = ["SAT-XI", "SAT-IX"],
            descripcion    = (
                f"Infraejecución crónica confirmada: Ti promedio {result.ti_mean:.1f}% "
                f"con mínima varianza (σ={result.ti_std:.1f}%) en {result.n_periodos} períodos. "
                "Capacidad institucional de ejecución comprometida estructuralmente."
            ),
            recomendacion  = (
                "Solicitar informe técnico a Dirección de Planificación sobre causales. "
                "Revisar si proyectos tienen diseños definitivos y terrenos saneados. "
                "Considerar reforma al POA para reasignar a proyectos ejecutables."
            ),
            flags          = ["CAPACIDAD_INSTITUCIONAL_COMPROMETIDA"],
        )

    # ── MANIPULACION_TEMPORAL ─────────────────────────────────────────────────
    # Q4_PUSH + BURST (sin REFORM_SHOCK que lo justifique)
    if (
        _has(ps, "Q4_PUSH")
        and _has(ps, "BURST")
        and not _has(ps, "REFORM_SHOCK")
        and result.ti_mean < 40.0
    ):
        conf = (_confidence(ps, "Q4_PUSH") + _confidence(ps, "BURST")) / 2
        return InstitutionalClass(
            clase          = "MANIPULACION_TEMPORAL",
            confianza      = round(conf, 3),
            avep_riesgo    = "Ocurrencia Crítica",
            avep_score     = 35.0,
            sat_codes      = ["SAT-X-A", "SAT-XI"],
            descripcion    = (
                "Patrón de concentración temporal de gasto sin justificación normativa. "
                f"Historial de baja ejecución (Ti_media={result.ti_mean:.1f}%) "
                "con aceleraciones puntuales en Q4. Riesgo de fraccionamiento contractual."
            ),
            recomendacion  = (
                "Auditar procesos contractuales de Q4: verificar umbral LOSNCP, "
                "SHA-256 de documentos de soporte y cadena de aprobaciones. "
                "Confirmar inclusión en PAC previo a cada proceso."
            ),
            flags          = ["FRACCIONAMIENTO_SOSPECHOSO", "AUDITORIA_RECOMENDADA"],
        )

    # ── EXPANSION_TARDIA ─────────────────────────────────────────────────────
    # EXPANSION_BUDGET + (FREEZE o bajo Ti_last o bajo Ti_mean)
    _ti_last = result.ti_series[-1] if result.ti_series else 100.0
    if _has(ps, "EXPANSION_BUDGET") and (_ti_last < 30.0 or result.ti_mean < 40.0):
        conf = _confidence(ps, "EXPANSION_BUDGET")
        return InstitutionalClass(
            clase          = "EXPANSION_TARDIA",
            confianza      = round(conf, 3),
            avep_riesgo    = "Transición Crítica",
            avep_score     = 48.0,
            sat_codes      = ["SAT-XI"],
            descripcion    = (
                f"Expansión presupuestaria (Δcodificado=${result.codificado_drift:,.0f}) "
                f"sin capacidad de ejecución proporcional (Ti_media={result.ti_mean:.1f}%). "
                "Los recursos aprobados superan la capacidad operativa del GAD."
            ),
            recomendacion  = (
                "Revisar cartera de proyectos: identificar cuáles tienen expedientes completos. "
                "Activar refuerzo técnico en Unidad de Contratación Pública. "
                "Considerar reforma al PAC para redistribuir a proyectos maduros."
            ),
            flags          = ["CAPACIDAD_EJECUCION_INSUFICIENTE"],
        )

    # ── REFORMA_LEGITIMA ─────────────────────────────────────────────────────
    # REFORM_SHOCK + no BURST + no Q4_PUSH (reforma bien distribuida)
    if (
        _has(ps, "REFORM_SHOCK")
        and not _has(ps, "BURST")
        and not _has(ps, "Q4_PUSH")
    ):
        conf = _confidence(ps, "REFORM_SHOCK")
        return InstitutionalClass(
            clase          = "REFORMA_LEGITIMA",
            confianza      = round(conf * 0.8, 3),   # descuento: requiere verificación documental
            avep_riesgo    = "Gestión por Mandato",
            avep_score     = 72.0,
            sat_codes      = ["SAT-X-B"],
            descripcion    = (
                f"Reforma presupuestaria significativa detectada "
                f"(reforma_net=${result.reforma_net:,.0f}). "
                "Distribución temporal sin señales de aglomeración irregular. "
                "Requiere verificación: resolución del Alcalde/Concejo y consistencia PDOT."
            ),
            recomendacion  = (
                "Verificar informe técnico de Planificación que sustenta la reforma. "
                "Confirmar aprobación por el Alcalde (o Concejo si supera el 10%). "
                "Asegurar reforma al POA con metas PDOT actualizadas."
            ),
            flags          = ["VERIFICACION_DOCUMENTAL_REQUERIDA"],
        )

    # ── DETERIORO_PROGRESIVO ──────────────────────────────────────────────────
    # GRADUAL_DECLINE sin FREEZE ni RECOVERY
    if (
        _has(ps, "GRADUAL_DECLINE")
        and not _has(ps, "FREEZE")
        and not _has(ps, "RECOVERY")
    ):
        conf = _confidence(ps, "GRADUAL_DECLINE")
        return InstitutionalClass(
            clase          = "DETERIORO_PROGRESIVO",
            confianza      = round(conf, 3),
            avep_riesgo    = "Ocurrencia Crítica",
            avep_score     = 38.0,
            sat_codes      = ["SAT-XI"],
            descripcion    = (
                f"Deterioro progresivo de ejecución: Ti de {result.ti_series[0]:.1f}% "
                f"a {result.ti_series[-1]:.1f}% en {result.n_periodos} períodos. "
                "Sin señal de recuperación. Patrón de capacidad institucional en declive."
            ),
            recomendacion  = (
                "Solicitar informe de seguimiento al POA a la Dirección de Planificación. "
                "Identificar proyectos con baja ejecución y causas específicas. "
                "Evaluar necesidad de reforma presupuestaria con reasignación sectorial."
            ),
            flags          = ["TENDENCIA_NEGATIVA_CONFIRMADA"],
        )

    # ── CIERRE_TARDIO ────────────────────────────────────────────────────────
    # Q4_PUSH aislado, sin BURST intenso, con historial razonable
    if _has(ps, "Q4_PUSH") and not _has(ps, "BURST") and result.ti_mean > 40.0:
        conf = _confidence(ps, "Q4_PUSH")
        return InstitutionalClass(
            clase          = "CIERRE_TARDIO",
            confianza      = round(conf, 3),
            avep_riesgo    = "Transición Crítica",
            avep_score     = 55.0,
            sat_codes      = [],
            descripcion    = (
                "Patrón de cierre tardío: concentración de ejecución en Q4 "
                f"con historial razonable (Ti_media={result.ti_mean:.1f}%). "
                "Sin señal de fraccionamiento. Riesgo operativo moderado."
            ),
            recomendacion  = (
                "Adelantar planificación PAC a Q1. "
                "Revisar ciclo POA para distribuir ejecución a lo largo del año. "
                "Verificar que los procesos Q4 estén correctamente registrados en COMPRASPÚBLICAS."
            ),
            flags          = ["RIESGO_OPERATIVO_MODERADO"],
        )

    # ── RECUPERACION_VERIFICADA ───────────────────────────────────────────────
    # RECOVERY dominante
    if _has(ps, "RECOVERY") and ps.dominant == "RECOVERY":
        conf = _confidence(ps, "RECOVERY")
        return InstitutionalClass(
            clase          = "RECUPERACION_VERIFICADA",
            confianza      = round(conf * 0.85, 3),  # requiere sostenibilidad
            avep_riesgo    = "Gestión por Mandato",
            avep_score     = 75.0,
            sat_codes      = [],
            descripcion    = (
                f"Recuperación de ejecución: Ti pasó de {result.ti_series[-2]:.1f}% "
                f"a {result.ti_series[-1]:.1f}% en el último período. "
                "Señal positiva — monitorear sostenibilidad en próximo corte."
            ),
            recomendacion  = (
                "Mantener ritmo de ejecución. "
                "Verificar que la recuperación no corresponda a un spike puntual de Q4. "
                "Publicar reporte de avance de proyectos en portal de transparencia."
            ),
            flags          = ["MONITOREO_CONTINUADO_RECOMENDADO"],
        )

    # ── SHOCK_EXTERNO ─────────────────────────────────────────────────────────
    # DIP severo sin GRADUAL_DECLINE (evento puntual externo)
    if _has(ps, "DIP") and not _has(ps, "GRADUAL_DECLINE") and not _has(ps, "FREEZE"):
        conf = _confidence(ps, "DIP")
        dip_pat: Optional[Pattern] = next((p for p in ps.patterns if p.nombre == "DIP"), None)
        return InstitutionalClass(
            clase          = "SHOCK_EXTERNO",
            confianza      = round(conf * 0.7, 3),
            avep_riesgo    = "Transición Crítica",
            avep_score     = 50.0,
            sat_codes      = ["SAT-X-B"],
            descripcion    = (
                "Caída brusca puntual de ejecución sin tendencia de deterioro previa. "
                "Posible causa externa: reforma, bloqueo técnico o evento institucional. "
                + (dip_pat.descripcion if dip_pat else "")
            ),
            recomendacion  = (
                "Documentar causas específicas del período de caída. "
                "Si fue reforma presupuestaria: verificar resolución y consistencia PDOT. "
                "Si fue técnico: levantar informe de la Dirección Financiera."
            ),
            flags          = ["CAUSA_EXTERNA_PROBABLE"],
        )

    # ── SIN_PATRON_CLARO ─────────────────────────────────────────────────────
    return InstitutionalClass(
        clase          = "SIN_PATRON_CLARO",
        confianza      = 0.3,
        avep_riesgo    = "Transición Crítica",
        avep_score     = 52.0,
        sat_codes      = [],
        descripcion    = (
            f"Datos insuficientes o patrones contradictorios "
            f"(n={result.n_periodos} períodos, Ti_media={result.ti_mean:.1f}%). "
            "Se requieren más períodos o datos de grupos_gasto para clasificar."
        ),
        recomendacion  = (
            "Ampliar la serie temporal a mínimo 4 períodos comparables. "
            "Desagregar por grupo de gasto (G71–G78) para análisis específico."
        ),
        flags          = ["DATOS_INSUFICIENTES"],
    )


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def classify(
    ps:     PatternSet,
    result: LongitudinalResult,
) -> InstitutionalClass:
    """
    Clasifica el patrón de ejecución en una clase institucional ejecutiva.

    Args:
        ps:     PatternSet del sub-motor 2
        result: LongitudinalResult del sub-motor 1

    Returns:
        InstitutionalClass con clase, AVEP, SATs, descripción y recomendación.
    """
    ic = _classify(ps, result)

    # Enriquecer flags con señales longitudinales adicionales
    if result.momentum and result.momentum.tendencia == "REVERTIENDO":
        ic.flags.append("MOMENTUM_NEGATIVO")
    if result.ti_range > 40.0:
        ic.flags.append(f"ALTA_VOLATILIDAD_Ti_{result.ti_range:.0f}pts")
    if result.n_periodos < 3:
        ic.flags.append("SERIE_CORTA_VERIFICAR")

    return ic


def describe_for_sentinel(ic: InstitutionalClass, result: LongitudinalResult) -> str:
    """
    Genera bloque de texto listo para inyectar al system prompt de Sentinel.
    Máximo 400 caracteres — control de tokens.
    """
    lines = [
        f"DIAGNÓSTICO RC-7.2 ({ic.clase} | {ic.avep_riesgo}):",
        f"  {ic.descripcion[:200]}",
        f"  Acción: {ic.recomendacion[:150]}",
    ]
    if ic.sat_codes:
        lines.append(f"  SATs: {', '.join(ic.sat_codes)}")
    block = "\n".join(lines)
    if len(block) > 800:
        block = block[:797] + "..."
    return block


def summarize_class(ic: InstitutionalClass) -> dict:
    """Serializa InstitutionalClass a dict compacto para logs."""
    return {
        "clase":        ic.clase,
        "confianza":    ic.confianza,
        "avep_riesgo":  ic.avep_riesgo,
        "avep_score":   ic.avep_score,
        "sat_codes":    ic.sat_codes,
        "flags":        ic.flags,
    }
