"""
sentinel/synthesis_templates.py
RC-SYNTHESIS — Plantillas de Hipótesis Institucional
Dylus Lab © 2026-05-20

FUNCIÓN:
  Repositorio de plantillas para construir hipótesis institucionales interpretables
  a partir de la tensión dominante y las señales priorizadas.

  Una hipótesis institucional NO es:
    - Un score ("riesgo 87/100")
    - Una lista de KPIs
    - Una acusación
    - Un resumen de dashboards

  Una hipótesis institucional SÍ es:
    - Una lectura de la dinámica institucional observada
    - Una interpretación de por qué las tensiones coexisten
    - Una hipótesis plausible sobre el fenómeno subyacente
    - Una señal accionable para la autoridad competente

DOCTRINA:
  Las plantillas son marcos — no sentencias.
  La autoridad pública interpreta y decide.
  "El sistema informa — la autoridad pública decide."

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from sentinel.synthesis_prioritizer import Signal


# ── HIPÓTESIS POR TENSIÓN DOMINANTE ──────────────────────────────────────────

def build_hypothesis(
    dominant_tension: str,
    top_signals:      List["Signal"],
    entity_id:        str,
    context:          Dict[str, Any],
) -> str:
    """
    Construye la hipótesis institucional para la tensión dominante.

    Cada template produce texto de ~200-350 chars.
    La hipótesis menciona evidencia específica del contexto (IRS, patrón, entidad).
    Nunca acusatoria — siempre probabilística e interpretativa.
    """
    fn = _TEMPLATE_MAP.get(dominant_tension, _template_compuesta)
    return fn(top_signals, entity_id, context)[:400]


def _template_expansion_regresiva(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    irs     = ctx.get("irs_actual", 0.0)
    irs_m   = ctx.get("irs_meta",   45.0)
    d3_lbl  = next((s.label for s in signals if s.source == "D3"), "expansion presupuestaria")
    return (
        f"La expansión presupuestaria de {entity} no muestra indicadores de corrección "
        f"de las asimetrías territoriales. El IRS observado ({irs:.1f}) supera la meta "
        f"PDOT (≤{irs_m:.0f}). El patrón temporal '{d3_lbl}' coexiste con concentración "
        f"territorial, lo que sugiere que el incremento de gasto beneficia de manera "
        f"desproporcionada a las zonas con mayor capacidad de ejecución previa."
    )


def _template_bloqueo_institucional(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    d3_lbl = next((s.label for s in signals if s.source == "D3"), "contracción ejecutiva")
    d4_lbl = next((s.label for s in signals if s.source in ("D4", "D3xD4")), "concentración territorial")
    return (
        f"La paralización ejecutiva ({d3_lbl}) coexiste con persistencia de "
        f"concentración territorial ({d4_lbl}). La hipótesis institucional más plausible "
        f"es un bloqueo en el canal de contratación pública que afecta desproporcionadamente "
        f"a parroquias periféricas. Las zonas con menor capacidad institucional local "
        f"acumulan rezago cuando la ejecución central se contrae."
    )


def _template_desacople_estrategico(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    irs     = ctx.get("irs_actual", 0.0)
    irs_m   = ctx.get("irs_meta",   45.0)
    delta   = irs - irs_m
    d13_sig = next((s for s in signals if s.source == "D1.3"), None)
    d13_lbl = d13_sig.status if d13_sig else "desviación estratégica"
    return (
        f"El comportamiento material de {entity} presenta indicadores de divergencia "
        f"respecto a los compromisos estratégicos declarados en el PDOT 2023-2027. "
        f"La planificación definió IRS ≤ {irs_m:.0f} como meta territorial; "
        f"el valor observado ({irs:.1f}) implica una brecha de {delta:+.1f} puntos. "
        f"D1.3 clasifica esta situación como '{d13_lbl}': planificación y ejecución "
        f"territorial muestran trayectorias disociadas."
    )


def _template_crisis_territorial(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    cross = next((s for s in signals if s.source == "D3xD4"), None)
    c_lbl = cross.label if cross else "crisis combinada"
    irs   = ctx.get("irs_actual", 0.0)
    n_crit = ctx.get("n_critical", 0)
    return (
        f"Se detecta una combinación de subejecución y concentración territorial "
        f"({c_lbl}) que configura una señal de riesgo institucional de alta complejidad. "
        f"IRS territorial: {irs:.1f}. Parroquias con déficit crítico: {n_crit}. "
        f"El territorio periférico acumula rezago en múltiples dimensiones simultáneamente. "
        f"Esta señal requiere revisión institucional antes de ciclo presupuestario siguiente."
    )


def _template_vulnerabilidad_hidrica(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    return (
        f"La inequidad en el acceso a servicios de agua potable en zonas rurales de "
        f"{entity} no muestra señales de corrección sostenida. CRE Art. 264(4) establece "
        f"la competencia municipal exclusiva en agua potable, lo que genera una obligación "
        f"de cobertura territorial que no se refleja plenamente en la asignación presupuestaria. "
        f"Las parroquias rurales con mayor NBI concentran el déficit hídrico."
    )


def _template_maquillaje_institucional(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    return (
        f"La concentración de ejecución en Q4 terminal de {entity}, combinada con "
        f"persistencia de inequidad territorial, genera indicadores de posible concentración "
        f"formal de gasto sin corrección distributiva real. El cierre presupuestario acelerado "
        f"puede estar respondiendo a presiones de ejecución nominal sin territorializar "
        f"el beneficio hacia parroquias periféricas con mayor rezago."
    )


def _template_friccion_procedimental(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    d1_sig  = next((s for s in signals if s.source == "D1"), None)
    d1_lbl  = d1_sig.status if d1_sig else "riesgo procedimental"
    action  = ctx.get("top_action", "acto presupuestario")
    return (
        f"Se detectan indicadores de riesgo en el canal aprobatorio del proceso "
        f"presupuestario de {entity} ({d1_lbl} en '{action}'). "
        f"Sin documentación formal del órgano competente, la coherencia institucional "
        f"no es verificable. Esto no implica irregularidad — implica que la trazabilidad "
        f"procedimental requiere confirmación antes de elevar el nivel de señalización."
    )


def _template_compuesta(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    """Template genérico cuando no hay patrón dominante claro."""
    top_labels = ", ".join(s.label for s in signals[:3] if s.severity > 1)
    return (
        f"El análisis de {entity} detecta una combinación de tensiones institucionales "
        f"({top_labels}) que no se reducen a un patrón dominante único. "
        f"La complejidad de las señales simultáneas sugiere la necesidad de "
        f"revisión analítica integral antes de priorizar intervención específica."
    )


def _template_sin_tension(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    return (
        f"El análisis disponible de {entity} no detecta tensiones institucionales "
        f"de magnitud suficiente para señalización prioritaria. Los indicadores "
        f"disponibles muestran patrones dentro de rangos de variación normal. "
        f"Se mantiene monitoreo de rutina."
    )


def _template_coherencia_positiva(
    signals: List["Signal"], entity: str, ctx: Dict[str, Any]
) -> str:
    irs   = ctx.get("irs_actual", 0.0)
    irs_m = ctx.get("irs_meta",  45.0)
    return (
        f"Los indicadores disponibles de {entity} no muestran divergencias significativas "
        f"entre ejecución, territorio y compromisos normativos. "
        f"IRS actual ({irs:.1f}) dentro de rango compatible con la meta PDOT (≤{irs_m:.0f}). "
        f"El sistema mantiene monitoreo longitudinal para detectar tendencias emergentes."
    )


_TEMPLATE_MAP = {
    "EXPANSION_REGRESIVA":              _template_expansion_regresiva,
    "BLOQUEO_INSTITUCIONAL":            _template_bloqueo_institucional,
    "DESACOPLE_ESTRATEGICO":            _template_desacople_estrategico,
    "CRISIS_TERRITORIAL_CRITICA":       _template_crisis_territorial,
    "VULNERABILIDAD_HIDRICA_SISTEMICA": _template_vulnerabilidad_hidrica,
    "MAQUILLAJE_INSTITUCIONAL":         _template_maquillaje_institucional,
    "FRICCION_PROCEDIMENTAL":           _template_friccion_procedimental,
    "SIN_TENSION_DOMINANTE":            _template_sin_tension,
    "COHERENCIA_POSITIVA":              _template_coherencia_positiva,
    "TENSION_COMPUESTA":                _template_compuesta,
}


# ── RUTAS DE ACCIÓN ───────────────────────────────────────────────────────────

def build_action_route(
    dominant_tension: str,
    top_signals:      List["Signal"],
    entity_id:        str,
) -> List[str]:
    """
    Produce 2-3 pasos concretos de acción institucional.
    Siempre positivos — qué hacer, no qué no hacer.
    """
    routes = _ACTION_MAP.get(dominant_tension, _action_default)(top_signals, entity_id)
    return routes[:3]   # máximo 3 pasos


def _action_expansion(signals, entity):
    return [
        "Solicitar informe de territorialización de inversión adicional por parroquia",
        "Verificar cobertura real del PP en parroquias con bajo índice de recepción de inversión",
        "Revisar distribución de contratos adjudicados durante período de expansión presupuestaria",
    ]

def _action_bloqueo(signals, entity):
    return [
        "Verificar estado de procesos de contratación en portal SERCOP por entidad y período",
        "Solicitar PAC actualizado con estado de ejecución desglosado por parroquia",
        "Evaluar capacidad ejecutora del equipo técnico de contratación pública",
    ]

def _action_desacople(signals, entity):
    return [
        "Revisar trayectoria IRS respecto a meta PDOT 2027 en informe de seguimiento",
        "Actualizar asignación territorial del POA para próximo ciclo presupuestario",
        "Documentar criterios de distribución cantonal en ordenanza formal (COOTAD Art. 272)",
    ]

def _action_crisis(signals, entity):
    return [
        "Escalar señal a revisión institucional con Director de Planificación y Alcaldía",
        "Solicitar informe de parroquias con mayor déficit de ejecución y acceso territorial",
        "Revisar POA del próximo período incorporando corrección distributiva explícita",
    ]

def _action_hidrica(signals, entity):
    return [
        "Solicitar diagnóstico de cobertura de agua potable en parroquias rurales (NBI)",
        "Verificar asignación presupuestaria para proyectos de agua rural en PAI vigente",
        "Revisar estado de ejecución de contratos de agua potable en zonas de déficit",
    ]

def _action_maquillaje(signals, entity):
    return [
        "Revisar distribución territorial de contratos ejecutados en Q4 por parroquia",
        "Verificar que liquidación presupuestaria refleja territorialización real del gasto",
        "Solicitar informe de cierre por parroquia antes de liquidación definitiva",
    ]

def _action_friccion(signals, entity):
    return [
        "Verificar existencia de resolución aprobatoria del órgano competente",
        "Solicitar certificación presupuestaria y respaldo documental del proceso",
        "Confirmar canal aprobatorio según competencia de la entidad (COOTAD Art. 267 para EPs)",
    ]

def _action_default(signals, entity):
    return [
        "Revisar indicadores de desempeño institucional en informe de seguimiento",
        "Actualizar análisis con datos del próximo período para confirmar tendencias",
    ]

_ACTION_MAP = {
    "EXPANSION_REGRESIVA":              _action_expansion,
    "BLOQUEO_INSTITUCIONAL":            _action_bloqueo,
    "DESACOPLE_ESTRATEGICO":            _action_desacople,
    "CRISIS_TERRITORIAL_CRITICA":       _action_crisis,
    "VULNERABILIDAD_HIDRICA_SISTEMICA": _action_hidrica,
    "MAQUILLAJE_INSTITUCIONAL":         _action_maquillaje,
    "FRICCION_PROCEDIMENTAL":           _action_friccion,
}
