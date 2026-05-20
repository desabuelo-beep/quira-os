"""
sentinel/longitudinal_engine.py
RC-7.2 — Sub-motor 1: Análisis Longitudinal Matemático
QUIRA OS · Dylus Lab © 2026-05-20

Motor PURO. Sin semántica institucional. Sin interpretación.
Trabaja con: codificado · devengado · reformas · grupos_gasto · temporalidad · entidad

Doctrina: mismo input → mismo output (determinismo total).
Cada estadístico debe poder re-computarse frente a Contraloría con los datos crudos.

API principal: analyze_series(records) → LongitudinalResult
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ── TIPOS DE DATOS ─────────────────────────────────────────────────────────────

@dataclass
class BudgetRecord:
    """
    Un corte temporal de ejecución presupuestaria.

    periodo:      str  — identificador canónico: '2023', '2024Q1', '2025M03', etc.
    orden:        int  — posición en la serie (0-indexed, cronológico)
    codificado:   float — presupuesto codificado vigente (USD)
    devengado:    float — gasto devengado acumulado (USD)
    reformas:     float — monto acumulado de reformas presupuestarias (USD, puede ser negativo)
    grupo_gasto:  str  — grupo COPLAFIP/eSIGEF ('71','73','75','77','78','84' etc.)
    entidad:      str  — código entidad ('GAD','BOMB','PAT','EP_ASEO','HOLDING')
    """
    periodo:    str
    orden:      int
    codificado: float
    devengado:  float
    reformas:   float   = 0.0
    grupo_gasto: str    = ""
    entidad:    str     = "GAD"


@dataclass
class Slope:
    """Pendiente lineal entre dos puntos."""
    from_periodo: str
    to_periodo:   str
    variable:     str      # 'ti_pct' | 'codificado' | 'devengado' | 'reformas'
    value:        float    # USD/periodo o pct/periodo
    pct_change:   float    # cambio relativo (puede ser inf si base=0)


@dataclass
class Discontinuity:
    """Salto brusco detectado en una variable."""
    periodo:      str
    variable:     str
    magnitude:    float    # magnitud del salto (absoluta)
    direction:    str      # 'UP' | 'DOWN'
    z_score:      float    # desviación estándar del salto vs histórico


@dataclass
class SeasonalSignal:
    """Señal estacional detectada."""
    tipo:         str      # 'Q4_PUSH' | 'Q1_DIP' | 'MID_YEAR_FLAT' | 'YEAR_END_SPIKE'
    strength:     float    # 0.0–1.0 (ratio diferencia máx/mín normalizada)
    periodos:     list[str] = field(default_factory=list)


@dataclass
class Momentum:
    """Velocidad y aceleración de ejecución."""
    variable:       str
    velocidad:      float   # promedio de cambios periodo-a-periodo (USD o pct)
    aceleracion:    float   # segunda derivada (cambio en la velocidad)
    tendencia:      str     # 'ACELERANDO' | 'DESACELERANDO' | 'ESTABLE' | 'REVERTIENDO'


@dataclass
class LongitudinalResult:
    """Resultado completo del análisis longitudinal para una serie."""
    entidad:          str
    grupo_gasto:      str
    n_periodos:       int
    ti_series:        list[float]         # Ti% por periodo
    ti_mean:          float
    ti_std:           float
    ti_min:           float
    ti_max:           float
    ti_range:         float               # max - min
    slopes:           list[Slope]         = field(default_factory=list)
    discontinuities:  list[Discontinuity] = field(default_factory=list)
    seasonal_signals: list[SeasonalSignal]= field(default_factory=list)
    momentum:         Optional[Momentum]  = None
    codificado_drift: float               = 0.0  # cambio total codificado (USD)
    reforma_net:      float               = 0.0  # suma neta reformas
    raw_flags:        list[str]           = field(default_factory=list)


# ── CONSTANTES MATEMÁTICAS ─────────────────────────────────────────────────────

_DISCONTINUITY_Z_THRESHOLD  = 1.8   # z-score para declarar discontinuidad
_MIN_SERIES_LEN             = 2     # mínimo de puntos para calcular pendiente
_Q4_MONTHS                  = {"M10", "M11", "M12", "Q4"}
_Q1_MONTHS                  = {"M01", "M02", "M03", "Q1"}
_FREEZE_TI_THRESHOLD        = 2.0   # Ti% < 2% → ejecución congelada
_BURST_DELTA_THRESHOLD      = 20.0  # salto Ti% > 20 puntos en un periodo → burst


# ── HELPERS MATEMÁTICOS ────────────────────────────────────────────────────────

def _safe_ti(devengado: float, codificado: float) -> float:
    """Ti% = devengado / codificado * 100. Retorna 0.0 si codificado == 0."""
    if codificado == 0.0:
        return 0.0
    return round((devengado / codificado) * 100.0, 4)


def _safe_div(a: float, b: float) -> float:
    if b == 0.0:
        return float("inf") if a > 0 else (float("-inf") if a < 0 else 0.0)
    return a / b


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def _std(values: list[float], mean: Optional[float] = None) -> float:
    if len(values) < 2:
        return 0.0
    mu = mean if mean is not None else _mean(values)
    variance = sum((v - mu) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)


def _linear_slope(xs: list[float], ys: list[float]) -> float:
    """Pendiente OLS simple (β₁ de regresión y = β₀ + β₁·x)."""
    n = len(xs)
    if n < 2:
        return 0.0
    sum_x  = sum(xs)
    sum_y  = sum(ys)
    sum_xy = sum(x * y for x, y in zip(xs, ys))
    sum_x2 = sum(x ** 2 for x in xs)
    denom  = n * sum_x2 - sum_x ** 2
    if denom == 0.0:
        return 0.0
    return (n * sum_xy - sum_x * sum_y) / denom


# ── DETECTORES ────────────────────────────────────────────────────────────────

def _compute_slopes(records: list[BudgetRecord]) -> list[Slope]:
    """Pendientes periodo-a-periodo para ti_pct, codificado, devengado."""
    if len(records) < 2:
        return []
    slopes: list[Slope] = []
    variables = ["ti_pct", "codificado", "devengado", "reformas"]

    def _val(r: BudgetRecord, var: str) -> float:
        if var == "ti_pct":
            return _safe_ti(r.devengado, r.codificado)
        return getattr(r, var)

    for i in range(1, len(records)):
        prev, curr = records[i - 1], records[i]
        for var in variables:
            v0 = _val(prev, var)
            v1 = _val(curr, var)
            delta = v1 - v0
            pct   = _safe_div(delta, abs(v0)) if v0 != 0.0 else float("inf")
            slopes.append(Slope(
                from_periodo = prev.periodo,
                to_periodo   = curr.periodo,
                variable     = var,
                value        = round(delta, 4),
                pct_change   = round(pct, 6),
            ))
    return slopes


def _detect_discontinuities(
    records: list[BudgetRecord],
    slopes:  list[Slope],
) -> list[Discontinuity]:
    """
    Discontinuidad = salto cuyo z-score supera _DISCONTINUITY_Z_THRESHOLD
    relativo a la distribución de todos los saltos de esa variable.
    """
    if not slopes:
        return []

    # Agrupar deltas por variable
    from collections import defaultdict
    var_deltas: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for s in slopes:
        var_deltas[s.variable].append((s.to_periodo, s.value))

    discontinuities: list[Discontinuity] = []
    for var, delta_list in var_deltas.items():
        vals = [d for _, d in delta_list]
        mu   = _mean(vals)
        sd   = _std(vals)
        if sd == 0.0:
            continue
        for periodo, delta in delta_list:
            z = (delta - mu) / sd
            if abs(z) >= _DISCONTINUITY_Z_THRESHOLD:
                discontinuities.append(Discontinuity(
                    periodo   = periodo,
                    variable  = var,
                    magnitude = round(abs(delta), 2),
                    direction = "UP" if delta > 0 else "DOWN",
                    z_score   = round(z, 3),
                ))
    return discontinuities


def _detect_seasonal_signals(records: list[BudgetRecord]) -> list[SeasonalSignal]:
    """
    Detecta patrones estacionales conocidos en series temporales ecuatorianas.
    Requiere al menos 4 periodos con sufijo de mes/trimestre.
    """
    signals: list[SeasonalSignal] = []
    if len(records) < 4:
        return signals

    # Separar periodos Q4 vs Q1 si la serie los tiene
    q4_ti: list[float] = []
    q1_ti: list[float] = []
    for r in records:
        ti = _safe_ti(r.devengado, r.codificado)
        # Detectar si el periodo contiene marcadores Q4/Q1/mes
        p = r.periodo.upper()
        if any(tok in p for tok in _Q4_MONTHS):
            q4_ti.append(ti)
        elif any(tok in p for tok in _Q1_MONTHS):
            q1_ti.append(ti)

    if q4_ti and q1_ti:
        q4_mean = _mean(q4_ti)
        q1_mean = _mean(q1_ti)
        diff    = q4_mean - q1_mean
        # Normalizar sobre rango Ti de la serie completa
        all_ti = [_safe_ti(r.devengado, r.codificado) for r in records]
        ti_range = max(all_ti) - min(all_ti)
        strength = round(_safe_div(abs(diff), ti_range if ti_range > 0 else 1.0), 3)

        if q4_mean > q1_mean + 10.0:   # Q4 significativamente mayor → Q4_PUSH
            signals.append(SeasonalSignal(
                tipo     = "Q4_PUSH",
                strength = min(strength, 1.0),
                periodos = [r.periodo for r in records
                            if any(tok in r.periodo.upper() for tok in _Q4_MONTHS)],
            ))
        if q1_mean < 5.0:              # Q1 casi plano → Q1_DIP
            signals.append(SeasonalSignal(
                tipo     = "Q1_DIP",
                strength = round(1.0 - (q1_mean / 5.0), 3),
                periodos = [r.periodo for r in records
                            if any(tok in r.periodo.upper() for tok in _Q1_MONTHS)],
            ))

    # YEAR_END_SPIKE: último periodo tiene Ti mucho mayor que la media previa
    if len(records) >= 3:
        all_ti   = [_safe_ti(r.devengado, r.codificado) for r in records]
        last_ti  = all_ti[-1]
        prev_mean = _mean(all_ti[:-1])
        if last_ti > prev_mean + 25.0:
            signals.append(SeasonalSignal(
                tipo     = "YEAR_END_SPIKE",
                strength = round(_safe_div(last_ti - prev_mean, 100.0), 3),
                periodos = [records[-1].periodo],
            ))

    return signals


def _compute_momentum(records: list[BudgetRecord]) -> Optional[Momentum]:
    """
    Velocidad = promedio de cambios Ti% periodo-a-periodo.
    Aceleración = segunda derivada (cambio en velocidad).
    """
    if len(records) < 3:
        return None

    ti_series  = [_safe_ti(r.devengado, r.codificado) for r in records]
    deltas     = [ti_series[i] - ti_series[i-1] for i in range(1, len(ti_series))]
    velocidad  = _mean(deltas)

    if len(deltas) >= 2:
        acc_values   = [deltas[i] - deltas[i-1] for i in range(1, len(deltas))]
        aceleracion  = _mean(acc_values)
    else:
        aceleracion = 0.0

    # Clasificar tendencia
    if abs(velocidad) < 0.5:
        tendencia = "ESTABLE"
    elif velocidad > 0 and aceleracion >= 0:
        tendencia = "ACELERANDO"
    elif velocidad > 0 and aceleracion < 0:
        tendencia = "DESACELERANDO"
    elif velocidad < 0 and aceleracion <= 0:
        tendencia = "REVERTIENDO"
    else:
        tendencia = "DESACELERANDO"

    return Momentum(
        variable     = "ti_pct",
        velocidad    = round(velocidad, 4),
        aceleracion  = round(aceleracion, 4),
        tendencia    = tendencia,
    )


def _raw_flags(records: list[BudgetRecord]) -> list[str]:
    """
    Flags matemáticos puros — sin interpretación institucional.
    El sub-motor 2 (administrative_patterns) los interpretará.
    """
    flags: list[str] = []
    if not records:
        return flags

    ti_series = [_safe_ti(r.devengado, r.codificado) for r in records]

    # FREEZE: último Ti% muy bajo
    if ti_series[-1] < _FREEZE_TI_THRESHOLD:
        flags.append("FREEZE_LAST")

    # FREEZE_SUSTAINED: promedio de últimos 2 periodos < umbral
    if len(ti_series) >= 2 and _mean(ti_series[-2:]) < _FREEZE_TI_THRESHOLD:
        flags.append("FREEZE_SUSTAINED")

    # BURST: salto positivo > umbral en un periodo
    for i in range(1, len(ti_series)):
        if ti_series[i] - ti_series[i-1] > _BURST_DELTA_THRESHOLD:
            flags.append(f"BURST@{records[i].periodo}")

    # REFORMA_SIGNIFICATIVA: reforma > 10% del codificado inicial
    total_reforma = sum(r.reformas for r in records)
    if records and records[0].codificado > 0:
        reforma_ratio = abs(total_reforma) / records[0].codificado
        if reforma_ratio > 0.10:
            flags.append(f"REFORMA_NET_{'+' if total_reforma >= 0 else '-'}{round(reforma_ratio*100,1)}pct")

    # DECLINING_TREND: pendiente OLS negativa sobre Ti
    if len(ti_series) >= 3:
        xs     = list(range(len(ti_series)))
        slope  = _linear_slope(xs, ti_series)
        if slope < -2.0:
            flags.append("DECLINING_TREND")
        elif slope > 4.0:
            flags.append("ACCELERATING_TREND")

    # HIGH_VOLATILITY: std > 15 puntos porcentuales
    ti_std = _std(ti_series)
    if ti_std > 15.0:
        flags.append(f"HIGH_VOLATILITY_STD{round(ti_std,1)}")

    return flags


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def analyze_series(records: list[BudgetRecord]) -> LongitudinalResult:
    """
    Analiza una serie temporal de registros presupuestarios.

    Args:
        records: Lista de BudgetRecord, ordenada cronológicamente (orden asc).

    Returns:
        LongitudinalResult con todos los estadísticos matemáticos.
    """
    if not records:
        return LongitudinalResult(
            entidad="UNKNOWN", grupo_gasto="",
            n_periodos=0, ti_series=[], ti_mean=0.0, ti_std=0.0,
            ti_min=0.0, ti_max=0.0, ti_range=0.0,
        )

    # Ordenar por campo orden (garantiza determinismo)
    records = sorted(records, key=lambda r: r.orden)

    entidad     = records[-1].entidad
    grupo_gasto = records[-1].grupo_gasto

    ti_series = [_safe_ti(r.devengado, r.codificado) for r in records]
    ti_mean   = _mean(ti_series)
    ti_std    = _std(ti_series)
    ti_min    = min(ti_series)
    ti_max    = max(ti_series)

    slopes           = _compute_slopes(records)
    discontinuities  = _detect_discontinuities(records, slopes)
    seasonal_signals = _detect_seasonal_signals(records)
    momentum         = _compute_momentum(records)
    flags            = _raw_flags(records)

    # Drift codificado: cambio total de presupuesto codificado
    codificado_drift = records[-1].codificado - records[0].codificado
    reforma_net      = sum(r.reformas for r in records)

    return LongitudinalResult(
        entidad          = entidad,
        grupo_gasto      = grupo_gasto,
        n_periodos       = len(records),
        ti_series        = ti_series,
        ti_mean          = round(ti_mean, 4),
        ti_std           = round(ti_std, 4),
        ti_min           = round(ti_min, 4),
        ti_max           = round(ti_max, 4),
        ti_range         = round(ti_max - ti_min, 4),
        slopes           = slopes,
        discontinuities  = discontinuities,
        seasonal_signals = seasonal_signals,
        momentum         = momentum,
        codificado_drift = round(codificado_drift, 2),
        reforma_net      = round(reforma_net, 2),
        raw_flags        = flags,
    )


def analyze_multi_entity(
    series_map: dict[str, list[BudgetRecord]],
) -> dict[str, LongitudinalResult]:
    """
    Analiza múltiples entidades/grupos en paralelo.

    Args:
        series_map: {key → records}  donde key puede ser entidad, grupo_gasto, etc.

    Returns:
        {key → LongitudinalResult}
    """
    return {key: analyze_series(recs) for key, recs in series_map.items()}


def summarize_result(result: LongitudinalResult) -> dict:
    """
    Serializa LongitudinalResult a dict compacto para logs y provenance.
    """
    return {
        "entidad":         result.entidad,
        "grupo_gasto":     result.grupo_gasto,
        "n_periodos":      result.n_periodos,
        "ti_mean":         result.ti_mean,
        "ti_std":          result.ti_std,
        "ti_min":          result.ti_min,
        "ti_max":          result.ti_max,
        "ti_range":        result.ti_range,
        "momentum":        {
            "tendencia":    result.momentum.tendencia if result.momentum else "N/A",
            "velocidad":    result.momentum.velocidad if result.momentum else 0.0,
            "aceleracion":  result.momentum.aceleracion if result.momentum else 0.0,
        } if result.momentum else None,
        "n_discontinuities": len(result.discontinuities),
        "seasonal_signals":  [s.tipo for s in result.seasonal_signals],
        "codificado_drift":  result.codificado_drift,
        "reforma_net":       result.reforma_net,
        "raw_flags":         result.raw_flags,
    }
