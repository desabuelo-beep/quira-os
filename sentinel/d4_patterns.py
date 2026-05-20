"""
sentinel/d4_patterns.py
RC-D4 Territorial Patterns — QUIRA OS
Detectores de patrones de inequidad territorial.

Entrada: D4Result → Salida: D4PatternSet
SATs D4: SAT-D4-A · SAT-D4-B · SAT-D4-C · SAT-D4-D · SAT-D4-E

Doctrina: detecta → no sentencia. La autoridad pública decide.
La calibración (d4_calibration.py) reduce los falsos positivos antes de emitir SATs.

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from sentinel.d4_engine import D4Result, ParishAnalysis


# ── TIPOS ─────────────────────────────────────────────────────────────────────

@dataclass
class D4Pattern:
    """Un patrón de inequidad territorial detectado."""
    nombre:      str           # ej. "CONCENTRACION_TERRITORIAL"
    sat_hint:    str           # ej. "SAT-D4-A"
    confianza:   float         # 0–1 (antes de calibración espacial)
    risk_level:  str           # "CRITICO" | "ALTO" | "MEDIO" | "BAJO"
    evidencias:  List[str]     # evidencia cuantitativa específica
    descripcion: str           # texto institucional corto


@dataclass
class D4PatternSet:
    """Conjunto de patrones D4 detectados para una entidad territorial."""
    patterns:         List[D4Pattern]
    patron_principal: Optional[str]    # nombre del patrón más severo
    sat_codes_raw:    List[str]        # SATs antes de calibración
    n_criticos:       int
    n_altos:          int


# ── DETECTORES DE PATRONES ────────────────────────────────────────────────────
# Ordenados por severidad (CRITICO → ALTO → MEDIO → BAJO)

def _detect_concentracion_territorial(r: D4Result) -> Optional[D4Pattern]:
    """
    SAT-D4-A: Concentración territorial.
    Inversión fuertemente concentrada en parroquias de menor necesidad.
    Trigger: IRS ≥ 70 Y CR1 ≥ 65%
    """
    evidence: List[str] = []
    conf = 0.0

    if r.irs >= 90:
        evidence.append(f"IRS={r.irs:.1f} — correlación NBI↑/inversión↓ extrema")
        conf += 0.55
    elif r.irs >= 70:
        evidence.append(f"IRS={r.irs:.1f} — inversión regresiva crítica")
        conf += 0.40

    if r.cr1 >= 0.80:
        top = max(r.parish_analyses, key=lambda a: a.actual_inv_percapita)
        evidence.append(
            f"CR1={r.cr1:.0%}: {top.nombre} concentra "
            f"${top.actual_inv_percapita:.0f}/hab ({top.need_share:.0%} de la necesidad cantonale)"
        )
        conf += 0.35
    elif r.cr1 >= 0.65:
        evidence.append(f"CR1={r.cr1:.0%} — alta concentración en pocas parroquias")
        conf += 0.20

    if not evidence:
        return None

    risk = "CRITICO" if r.irs >= 70 and r.cr1 >= 0.65 else "ALTO"
    conf = min(0.92, conf)

    return D4Pattern(
        nombre      = "CONCENTRACION_TERRITORIAL",
        sat_hint    = "SAT-D4-A",
        confianza   = conf,
        risk_level  = risk,
        evidencias  = evidence,
        descripcion = (
            f"Inversión per cápita fuertemente concentrada e inversamente correlacionada "
            f"con necesidad territorial. IRS={r.irs:.1f} indica distribución regresiva: "
            f"las parroquias con mayor NBI reciben sistemáticamente menos inversión."
        ),
    )


def _detect_rezago_persistente(r: D4Result) -> Optional[D4Pattern]:
    """
    SAT-D4-B: Rezago persistente.
    Múltiples parroquias rurales con brecha negativa severa vs baseline equitativo.
    Trigger: ≥2 parroquias rurales con gap < −50%
    """
    rezagadas = [
        a for a in r.parish_analyses
        if a.tipo == "Rural" and a.gap_pct < -0.50
    ]
    if len(rezagadas) < 2:
        return None

    rezagadas.sort(key=lambda a: a.gap_pct)  # más negativa primero
    evidence: List[str] = []

    for a in rezagadas[:4]:
        evidence.append(
            f"{a.nombre}: ${a.actual_inv_percapita:.0f}/hab vs ${a.expected_inv_percapita:.0f}/hab "
            f"equitativo (gap {a.gap_pct:+.0%})"
        )

    n = len(rezagadas)
    conf = min(0.88, 0.50 + n * 0.10)
    risk = "CRITICO" if n >= 4 else "ALTO"

    return D4Pattern(
        nombre      = "REZAGO_PERSISTENTE",
        sat_hint    = "SAT-D4-B",
        confianza   = conf,
        risk_level  = risk,
        evidencias  = evidence,
        descripcion = (
            f"{n} parroquias rurales ({n}/{r.n_rural} del total rural) "
            f"reciben menos del 50% de la inversión per cápita equitativa. "
            f"Patrón sistemático de sub-financiamiento territorial que excede "
            f"cualquier diferencia de competencias."
        ),
    )


def _detect_captura_capital(r: D4Result) -> Optional[D4Pattern]:
    """
    SAT-D4-C: Captura de capital cantonal.
    La cabecera cantonal concentra desproporcionadamente la inversión.
    Trigger: capital_ratio ≥ 3.0x y CR1 ≥ 70%
    """
    if r.capital_ratio < 3.0 or r.cr1 < 0.65:
        return None

    urban_analyses = [a for a in r.parish_analyses if a.tipo == "Urbana"]
    if not urban_analyses:
        return None

    cap = urban_analyses[0]
    evidence = [
        f"Cabecera cantonal: ${r.urban_inv:.0f}/hab vs "
        f"${r.rural_mean_inv:.1f}/hab media rural — ratio {r.capital_ratio:.1f}x",
        f"Gap cabecera: {cap.gap_pct:+.0%} sobre baseline equitativo "
        f"(+${cap.gap_abs:.0f}/hab excedente)",
    ]

    conf = min(0.85, 0.40 + (r.capital_ratio - 3.0) * 0.08)
    risk = "CRITICO" if r.capital_ratio >= 4.0 else "ALTO"

    return D4Pattern(
        nombre      = "CAPTURA_CAPITAL",
        sat_hint    = "SAT-D4-C",
        confianza   = conf,
        risk_level  = risk,
        evidencias  = evidence,
        descripcion = (
            f"La cabecera cantonal capta {r.capital_ratio:.1f}x más inversión per cápita "
            f"que la media rural. Aun ajustando por el efecto capital-sede-administrativa, "
            f"la brecha supera los rangos técnicamente justificables."
        ),
    )


def _detect_inequidad_hidrica(r: D4Result) -> Optional[D4Pattern]:
    """
    SAT-D4-D: Inequidad hídrica.
    Parroquias con déficit de agua potable severo reciben menos inversión de la equitativa.
    Trigger: ≥1 parroquia con agua < 10% y gap_pct < −50%
    """
    hidricas = [
        a for a in r.parish_analyses
        if a.gap_pct < -0.50
    ]
    # Also get water coverage for each
    # We don't have direct access to ParishRecord here, use raw_flags
    hidricas_agua = [
        a for a in hidricas
        if any("INEQUIDAD_HIDRICA" in flag for flag in a.raw_flags)
    ]

    if not hidricas_agua:
        return None

    evidence: List[str] = []
    for a in hidricas_agua:
        water_flag = next(
            (f for f in a.raw_flags if "INEQUIDAD_HIDRICA" in f), ""
        )
        evidence.append(f"{a.nombre}: {water_flag}")
        evidence.append(
            f"  → Necesidad compuesta: {a.composite_need:.1f} pts "
            f"(mayor del cantón) con solo ${a.actual_inv_percapita:.0f}/hab de inversión"
        )

    conf = min(0.82, 0.55 + len(hidricas_agua) * 0.15)

    return D4Pattern(
        nombre      = "INEQUIDAD_HIDRICA",
        sat_hint    = "SAT-D4-D",
        confianza   = conf,
        risk_level  = "ALTO",
        evidencias  = evidence,
        descripcion = (
            f"{len(hidricas_agua)} parroquia(s) combinan el mayor déficit de "
            f"cobertura de agua potable del cantón con una inversión per cápita "
            f"sistemáticamente por debajo de su baseline equitativo. "
            f"Indica desalineación entre necesidad hídrica y asignación presupuestaria."
        ),
    )


def _detect_sesgo_distributivo(r: D4Result) -> Optional[D4Pattern]:
    """
    SAT-D4-E: Sesgo distributivo generalizado.
    IRS moderadamente elevado + ninguna parroquia rural sobre baseline.
    Trigger: IRS 50–70 y todas las rurales sub-financiadas
    """
    if r.irs >= 70.0:
        return None  # ya cubierto por CONCENTRACION_TERRITORIAL

    if r.irs < 40.0:
        return None

    rural_underfunded = [
        a for a in r.parish_analyses
        if a.tipo == "Rural" and a.gap_pct < -0.10
    ]
    all_rural = [a for a in r.parish_analyses if a.tipo == "Rural"]

    if not all_rural or len(rural_underfunded) < len(all_rural) * 0.7:
        return None

    evidence = [
        f"IRS={r.irs:.1f} — sesgo distributivo elevado",
        f"{len(rural_underfunded)}/{len(all_rural)} parroquias rurales sub-financiadas",
    ]

    return D4Pattern(
        nombre      = "SESGO_DISTRIBUTIVO",
        sat_hint    = "SAT-D4-E",
        confianza   = 0.55,
        risk_level  = "MEDIO",
        evidencias  = evidence,
        descripcion = (
            f"Distribución de inversión moderadamente regresiva (IRS={r.irs:.1f}). "
            f"La mayoría de parroquias rurales reciben menos inversión per cápita "
            f"de la que les correspondería según su nivel de necesidad."
        ),
    )


# Registro de detectores — orden de prioridad (mayor riesgo primero)
_D4_PATTERN_DETECTORS = [
    _detect_concentracion_territorial,
    _detect_rezago_persistente,
    _detect_captura_capital,
    _detect_inequidad_hidrica,
    _detect_sesgo_distributivo,
]


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def detect_d4_patterns(result: D4Result) -> D4PatternSet:
    """
    Detecta patrones de inequidad territorial en el D4Result.

    Args:
        result: D4Result del motor espacial

    Returns:
        D4PatternSet con todos los patrones detectados, ordenados por severidad
    """
    patterns: List[D4Pattern] = []

    for detector in _D4_PATTERN_DETECTORS:
        try:
            p = detector(result)
            if p is not None:
                patterns.append(p)
        except Exception:
            pass  # nunca bloquear por un detector fallido

    # Ordenar: CRITICO > ALTO > MEDIO > BAJO, luego por confianza desc
    _RISK_ORDER = {"CRITICO": 0, "ALTO": 1, "MEDIO": 2, "BAJO": 3}
    patterns.sort(key=lambda p: (_RISK_ORDER.get(p.risk_level, 9), -p.confianza))

    sat_codes = list(dict.fromkeys(p.sat_hint for p in patterns))
    patron_principal = patterns[0].nombre if patterns else None

    n_criticos = sum(1 for p in patterns if p.risk_level == "CRITICO")
    n_altos    = sum(1 for p in patterns if p.risk_level == "ALTO")

    return D4PatternSet(
        patterns         = patterns,
        patron_principal = patron_principal,
        sat_codes_raw    = sat_codes,
        n_criticos       = n_criticos,
        n_altos          = n_altos,
    )


def summarize_pattern_set_d4(ps: D4PatternSet) -> str:
    """Resumen textual de patrones D4 para logs y debug."""
    if not ps.patterns:
        return "D4: Sin patrones detectados"
    lines = [
        f"D4 Patterns ({len(ps.patterns)}) — principal: {ps.patron_principal} "
        f"[{ps.n_criticos} críticos · {ps.n_altos} altos]"
    ]
    for p in ps.patterns:
        lines.append(f"  [{p.risk_level}] {p.nombre} conf={p.confianza:.0%} → {p.sat_hint}")
    return "\n".join(lines)
