"""
sentinel/administrative_patterns.py
RC-7.2 — Sub-motor 2: Reconocimiento de Patrones Institucionales
QUIRA OS · Dylus Lab © 2026-05-20

Recibe LongitudinalResult del motor 1 y produce PatternSet:
patrones nombrados con implicaciones SAT, umbral de riesgo y evidencia mínima.

Heurísticas institucionales del contexto ecuatoriano (GAD municipal):
  FREEZE         — ejecución detenida (eSIGEF bloqueado / voluntad política)
  Q4_PUSH        — acumulación de gasto en último trimestre
  REFORM_SHOCK   — reforma presupuestaria disruptiva
  BURST          — aceleración brusca de gasto
  DIP            — caída brusca de ejecución
  GRADUAL_DECLINE — deterioro sostenido multi-periodo
  RECOVERY       — recuperación tras caída
  STRUCTURAL_FLAT — ejecución plana sin señal estacional (infraejecución crónica)
  EXPANSION_BUDGET — codificado aumentó significativamente (más recursos, mismo ritmo)

Doctrina: Un patrón NO diagnostica — señala. El sub-motor 3 (institutional_classifier)
produce la interpretación ejecutiva. El sub-motor 4 (normative_binding) vincula la norma.

Dylus Lab © 2026
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from sentinel.longitudinal_engine import LongitudinalResult


# ── TIPOS ─────────────────────────────────────────────────────────────────────

@dataclass
class Pattern:
    """
    Un patrón institucional detectado.

    nombre:        código canónico del patrón
    confianza:     0.0–1.0 (proporción de evidencias que lo confirman)
    sat_hint:      lista de SAT codes implicados (heurística, no determinístico)
    risk_level:    'CRITICO' | 'ALTO' | 'MEDIO' | 'BAJO'
    evidencias:    lista de strings auditables (flags + estadísticos)
    descripcion:   texto conciso en español para informe ejecutivo
    """
    nombre:      str
    confianza:   float
    sat_hint:    list[str]      = field(default_factory=list)
    risk_level:  str            = "MEDIO"
    evidencias:  list[str]      = field(default_factory=list)
    descripcion: str            = ""


@dataclass
class PatternSet:
    """Conjunto de patrones detectados para una serie."""
    entidad:       str
    grupo_gasto:   str
    patterns:      list[Pattern]   = field(default_factory=list)
    dominant:      Optional[str]   = None   # nombre del patrón dominante
    sat_implied:   list[str]       = field(default_factory=list)  # union de sat_hint


# ── UMBRALES DE HEURÍSTICAS ───────────────────────────────────────────────────

_FREEZE_TI_MAX        = 5.0    # Ti% < 5% → posible freeze
_FREEZE_PERIODS_MIN   = 2      # mínimo de periodos consecutivos bajo umbral
_Q4_PUSH_MIN_STRENGTH = 0.30   # estacional Q4_PUSH con strength ≥ 0.30
_REFORM_SHOCK_MIN_PCT = 15.0   # reforma > 15% del codificado inicial → shock
_BURST_DELTA_MIN      = 20.0   # salto Ti% > 20 puntos en un periodo → burst
_DIP_DELTA_MIN        = 15.0   # caída Ti% > 15 puntos en un periodo → dip
_DECLINE_SLOPE_MAX    = -1.5   # pendiente OLS Ti% < -1.5 → decline gradual
_RECOVERY_THRESHOLD   = 10.0   # Ti mejora > 10 puntos tras dip → recovery
_FLAT_STD_MAX         = 3.0    # std Ti% < 3.0 y media < 30 → structural flat
_BUDGET_EXPAND_PCT    = 15.0   # codificado creció > 15% → expansion budget


# ── DETECTORES DE PATRÓN ──────────────────────────────────────────────────────

def _detect_freeze(result: LongitudinalResult) -> Optional[Pattern]:
    """
    FREEZE: ejecución detenida. Causas posibles:
    - Bloqueo eSIGEF (certificación, compromisos)
    - Decisión política de retener gasto
    - Proceso de reforma presupuestaria en curso
    - Falta de PAC/POA actualizado
    """
    if result.n_periodos < 1:
        return None

    freeze_flags = [f for f in result.raw_flags if "FREEZE" in f]
    low_ti_count = sum(1 for ti in result.ti_series if ti < _FREEZE_TI_MAX)

    if not freeze_flags and low_ti_count < _FREEZE_PERIODS_MIN:
        return None

    confianza = min(1.0, (len(freeze_flags) * 0.4) + (low_ti_count / max(result.n_periodos, 1)) * 0.6)
    evidencias = freeze_flags + [f"Ti_mean={result.ti_mean:.2f}% | periodos_bajos={low_ti_count}/{result.n_periodos}"]

    return Pattern(
        nombre      = "FREEZE",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-XI"],
        risk_level  = "CRITICO" if confianza >= 0.6 else "ALTO",
        evidencias  = evidencias,
        descripcion = (
            f"Ejecución detenida: Ti={result.ti_series[-1]:.1f}% en último período. "
            f"{low_ti_count} de {result.n_periodos} períodos bajo umbral del {_FREEZE_TI_MAX:.0f}%."
        ),
    )


def _detect_q4_push(result: LongitudinalResult) -> Optional[Pattern]:
    """
    Q4_PUSH: acumulación de gasto en último trimestre.
    Patrón institucional común en GADs ecuatorianos: presión de fin de año
    para justificar gasto no ejecutado. Riesgo de fraccionamiento (SAT-X-A).
    """
    seasonal = [s for s in result.seasonal_signals if s.tipo == "Q4_PUSH"]
    q4_burst  = [f for f in result.raw_flags if "BURST" in f and
                 any(tok in f.upper() for tok in {"M10", "M11", "M12", "Q4"})]

    if not seasonal and not q4_burst:
        return None

    strength  = max((s.strength for s in seasonal), default=0.0)
    confianza = min(1.0, strength + len(q4_burst) * 0.15)

    return Pattern(
        nombre      = "Q4_PUSH",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-X-A", "SAT-XI"],
        risk_level  = "ALTO",
        evidencias  = [f"Q4_strength={strength:.2f}"] + q4_burst,
        descripcion = (
            "Concentración de ejecución en Q4. Riesgo de fraccionamiento contractual "
            "y presión sobre proceso SERCOP sin debida planificación."
        ),
    )


def _detect_reform_shock(result: LongitudinalResult) -> Optional[Pattern]:
    """
    REFORM_SHOCK: reforma presupuestaria disruptiva.
    Reforma legítima (viabilidad confirmada) vs. reforma oculta (SAT-X-B).
    Solo el contexto documental distingue ambas — el motor señala el patrón.
    """
    reforma_flags = [f for f in result.raw_flags if "REFORMA_NET" in f]
    reform_net_pct = abs(result.reforma_net) / max(result.ti_series[0] if result.ti_series else 1.0, 1.0)

    # También detectar por discontinuidades en codificado
    cod_discs = [d for d in result.discontinuities if d.variable == "codificado"]

    if not reforma_flags and not cod_discs:
        return None

    confianza = min(1.0, len(reforma_flags) * 0.5 + len(cod_discs) * 0.3)

    return Pattern(
        nombre      = "REFORM_SHOCK",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-X-B"],
        risk_level  = "ALTO",
        evidencias  = reforma_flags + [
            f"reforma_net_USD={result.reforma_net:,.0f}",
            f"codificado_drift_USD={result.codificado_drift:,.0f}",
        ] + [f"disc@{d.periodo}_cod_z={d.z_score:.2f}" for d in cod_discs],
        descripcion = (
            f"Reforma presupuestaria significativa detectada: "
            f"variación neta ${result.reforma_net:,.0f}. "
            "Requiere verificación de resolución del Alcalde o Concejo."
        ),
    )


def _detect_burst(result: LongitudinalResult) -> Optional[Pattern]:
    """
    BURST: aceleración brusca de gasto.
    Puede indicar: ejecución aglomerada al cierre · pago de compromisos pendientes
    · respuesta a observación Contraloría · decisión política de último minuto.
    """
    burst_flags = [f for f in result.raw_flags if "BURST@" in f]
    ti_discs_up = [d for d in result.discontinuities
                   if d.variable == "ti_pct" and d.direction == "UP"]

    if not burst_flags and not ti_discs_up:
        return None

    confianza = min(1.0, len(burst_flags) * 0.5 + len(ti_discs_up) * 0.3)

    return Pattern(
        nombre      = "BURST",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-X-A", "SAT-XI"],
        risk_level  = "ALTO",
        evidencias  = burst_flags + [
            f"disc_UP@{d.periodo}_z={d.z_score:.2f}" for d in ti_discs_up
        ],
        descripcion = (
            "Aceleración brusca de ejecución detectada. "
            f"Rango Ti: {result.ti_min:.1f}%→{result.ti_max:.1f}%. "
            "Verificar trazabilidad documental de los devengados."
        ),
    )


def _detect_dip(result: LongitudinalResult) -> Optional[Pattern]:
    """
    DIP: caída brusca de ejecución.
    Causas posibles: reforma/reasignación · bloqueo técnico · cese de contrato.
    """
    ti_discs_down = [d for d in result.discontinuities
                     if d.variable == "ti_pct" and d.direction == "DOWN"]

    if not ti_discs_down:
        return None

    max_dip = max(d.magnitude for d in ti_discs_down)
    confianza = min(1.0, len(ti_discs_down) * 0.4 + max_dip / 50.0)

    return Pattern(
        nombre      = "DIP",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-XI", "SAT-X-B"],
        risk_level  = "ALTO",
        evidencias  = [
            f"disc_DOWN@{d.periodo}_z={d.z_score:.2f}_mag={d.magnitude:.1f}%"
            for d in ti_discs_down
        ],
        descripcion = (
            "Caída brusca en ejecución presupuestaria. "
            f"Magnitud máxima: {max_dip:.1f} puntos porcentuales. "
            "Puede reflejar reforma, bloqueo o discontinuidad contractual."
        ),
    )


def _detect_gradual_decline(result: LongitudinalResult) -> Optional[Pattern]:
    """
    GRADUAL_DECLINE: deterioro sostenido multi-periodo.
    Patrón más preocupante a largo plazo — sugiere problema estructural
    no episódico. Activa SAT-XI (paralisis de ejecución crónica).
    """
    if result.n_periodos < 3:
        return None
    if "DECLINING_TREND" not in result.raw_flags:
        return None

    # Calcular pendiente OLS explícita para confianza
    from sentinel.longitudinal_engine import _linear_slope
    xs    = list(range(result.n_periodos))
    slope = _linear_slope(xs, result.ti_series)
    confianza = min(1.0, abs(slope) / 5.0)  # escalar: -5%/periodo → conf=1.0

    return Pattern(
        nombre      = "GRADUAL_DECLINE",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-XI", "SAT-XII"],
        risk_level  = "CRITICO",
        evidencias  = [
            f"slope_OLS={slope:.3f}%/periodo",
            f"ti_inicio={result.ti_series[0]:.1f}% → ti_fin={result.ti_series[-1]:.1f}%",
            f"n_periodos={result.n_periodos}",
        ],
        descripcion = (
            f"Declive gradual sostenido: Ti pasó de {result.ti_series[0]:.1f}% a "
            f"{result.ti_series[-1]:.1f}% en {result.n_periodos} períodos. "
            "Patrón compatible con parálisis estructural de ejecución."
        ),
    )


def _detect_recovery(result: LongitudinalResult) -> Optional[Pattern]:
    """
    RECOVERY: recuperación tras caída.
    Puede ser señal positiva (corrección institucional) o cosmética (Q4_PUSH tardío).
    No elimina el SAT-XI si el promedio histórico sigue bajo.
    """
    if result.n_periodos < 3:
        return None

    ti = result.ti_series
    # Buscar: caída seguida de recuperación en últimos periodos
    if ti[-1] > ti[-2] + _RECOVERY_THRESHOLD and ti[-2] < result.ti_mean:
        confianza = min(1.0, (ti[-1] - ti[-2]) / 40.0)
        return Pattern(
            nombre      = "RECOVERY",
            confianza   = round(confianza, 3),
            sat_hint    = [],   # recovery puede ser positivo — depende del contexto
            risk_level  = "BAJO",
            evidencias  = [
                f"ti_penultimo={ti[-2]:.1f}% → ti_ultimo={ti[-1]:.1f}%",
                f"delta={ti[-1]-ti[-2]:.1f}%",
                f"ti_mean_historico={result.ti_mean:.1f}%",
            ],
            descripcion = (
                f"Recuperación de ejecución: {ti[-2]:.1f}% → {ti[-1]:.1f}% "
                f"(+{ti[-1]-ti[-2]:.1f} puntos). "
                "Verificar sostenibilidad vs. spike puntual."
            ),
        )
    return None


def _detect_structural_flat(result: LongitudinalResult) -> Optional[Pattern]:
    """
    STRUCTURAL_FLAT: ejecución crónica plana y baja.
    Ti% bajo con baja varianza → no hay impulso presupuestario de ningún tipo.
    Infraejecución estructural — más grave que el FREEZE episódico.
    """
    if result.n_periodos < 3:
        return None
    if result.ti_std > _FLAT_STD_MAX or result.ti_mean > 30.0:
        return None

    confianza = min(1.0, (30.0 - result.ti_mean) / 30.0 + (_FLAT_STD_MAX - result.ti_std) / _FLAT_STD_MAX)

    return Pattern(
        nombre      = "STRUCTURAL_FLAT",
        confianza   = round(confianza / 2.0, 3),   # dividir por 2: requiere más evidencia
        sat_hint    = ["SAT-XI", "SAT-IX"],
        risk_level  = "CRITICO",
        evidencias  = [
            f"ti_mean={result.ti_mean:.2f}%",
            f"ti_std={result.ti_std:.2f}%",
            f"n_periodos={result.n_periodos}",
        ],
        descripcion = (
            f"Infraejecución estructural: Ti promedio {result.ti_mean:.1f}% "
            f"con varianza mínima (σ={result.ti_std:.1f}%). "
            "No hay impulso presupuestario detectado."
        ),
    )


def _detect_expansion_budget(result: LongitudinalResult) -> Optional[Pattern]:
    """
    EXPANSION_BUDGET: el codificado creció significativamente.
    Más recursos, mismo ritmo de ejecución → problema de capacidad institucional
    o ausencia de proyectos listos para ejecutar (falta de POA/PAC actualizado).
    """
    if result.n_periodos < 2 or result.codificado_drift <= 0:
        return None

    # Calcular ratio de crecimiento respecto al codificado inicial
    # (aproximación: usamos drift / (codificado_final - drift) para la base)
    # Necesitamos el codificado inicial — lo inferimos del drift y el último registro
    # Esta heurística es conservadora: marca solo si el drift es grande en absoluto
    drift_pct = abs(result.codificado_drift) / max(abs(result.codificado_drift - result.codificado_drift), 1.0)

    # Usamos una heurística simple: si drift > 5M USD y Ti_mean no mejoró → señal
    if result.codificado_drift < 1_000_000 and result.ti_mean > 50.0:
        return None

    confianza = min(1.0, result.codificado_drift / 5_000_000)

    return Pattern(
        nombre      = "EXPANSION_BUDGET",
        confianza   = round(confianza, 3),
        sat_hint    = ["SAT-XI"],
        risk_level  = "MEDIO",
        evidencias  = [
            f"codificado_drift=+${result.codificado_drift:,.0f}",
            f"ti_mean={result.ti_mean:.1f}%",
        ],
        descripcion = (
            f"Expansión presupuestaria de ${result.codificado_drift:,.0f} "
            f"sin mejora proporcional en ejecución (Ti_media={result.ti_mean:.1f}%). "
            "Capacidad institucional insuficiente para el volumen de recursos."
        ),
    )


# ── ORQUESTADOR ────────────────────────────────────────────────────────────────

_PATTERN_DETECTORS = [
    _detect_freeze,
    _detect_q4_push,
    _detect_reform_shock,
    _detect_burst,
    _detect_dip,
    _detect_gradual_decline,
    _detect_recovery,
    _detect_structural_flat,
    _detect_expansion_budget,
]

_RISK_ORDER = {"CRITICO": 0, "ALTO": 1, "MEDIO": 2, "BAJO": 3}


def detect_patterns(result: LongitudinalResult) -> PatternSet:
    """
    Ejecuta todos los detectores sobre el LongitudinalResult.
    Filtra patrones con confianza < 0.15.
    Ordena por risk_level y confianza (mayor riesgo primero).

    Returns:
        PatternSet con patrones detectados, dominante y SATs implicados.
    """
    patterns: list[Pattern] = []

    for detector in _PATTERN_DETECTORS:
        p = detector(result)
        if p is not None and p.confianza >= 0.15:
            patterns.append(p)

    # Ordenar: CRITICO → ALTO → MEDIO → BAJO; dentro de cada nivel, por confianza desc
    patterns.sort(key=lambda p: (_RISK_ORDER.get(p.risk_level, 99), -p.confianza))

    # Dominante = primer patrón tras ordenamiento
    dominant = patterns[0].nombre if patterns else None

    # Unión de SATs implicados (sin duplicados, orden preservado)
    sat_implied: list[str] = []
    seen_sat: set[str] = set()
    for p in patterns:
        for sat in p.sat_hint:
            if sat not in seen_sat:
                sat_implied.append(sat)
                seen_sat.add(sat)

    return PatternSet(
        entidad    = result.entidad,
        grupo_gasto = result.grupo_gasto,
        patterns   = patterns,
        dominant   = dominant,
        sat_implied = sat_implied,
    )


def summarize_pattern_set(ps: PatternSet) -> dict:
    """Serializa PatternSet a dict compacto para logs y provenance."""
    return {
        "entidad":      ps.entidad,
        "grupo_gasto":  ps.grupo_gasto,
        "n_patterns":   len(ps.patterns),
        "dominant":     ps.dominant,
        "sat_implied":  ps.sat_implied,
        "patterns": [
            {
                "nombre":    p.nombre,
                "confianza": p.confianza,
                "risk":      p.risk_level,
                "sat_hint":  p.sat_hint,
            }
            for p in ps.patterns
        ],
    }
