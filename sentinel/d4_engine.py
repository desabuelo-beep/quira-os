"""
sentinel/d4_engine.py
RC-D4 Territorial Equity Engine — QUIRA OS
Motor espacial PURO: baseline equitativo, brecha territorial, IRS, Gini, concentración.

NO interpreta. NO juzga. Calcula.
Trabaja con: poblacion · NBI · agua · inversión_percapita · tipo_parroquia.

API principal: analyze_territory(parishes) → D4Result
Doctrina: mismo input → mismo output (determinismo total).
Cada estadístico puede recomputarse frente a Contraloría con los datos crudos.

Pesos canónicos: alineados con Gold Master v5.5 H99_ENGINE_CORE
  w_NBI=50% · w_Agua=30% · w_Pop=20%

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional

# ── PESOS CANÓNICOS — Gold Master v5.5 H99_ENGINE_CORE ────────────────────────
_W_NBI  = 0.50   # Necesidades Básicas Insatisfechas
_W_AGUA = 0.30   # Déficit cobertura agua potable
_W_POP  = 0.20   # Peso poblacional (parroquias más grandes necesitan más total)

# ── UMBRALES ──────────────────────────────────────────────────────────────────
_IRS_CRITICO       = 70.0   # IRS > 70 → Ruptura Institucional
_IRS_ALTO          = 50.0   # IRS 50-70 → Ocurrencia Preocupante
_CR1_CONCENTRADO   = 0.65   # CR1 > 65% → alta concentración
_GAP_CRITICO       = -0.50  # gap_pct < -50% → rezago crítico
_CAPITAL_RATIO_ALT = 3.0    # urban/rural > 3x → captura capital
_AGUA_CRITICA      = 10.0   # cobertura agua < 10% → déficit hídrico severo


# ── TIPOS DE DATOS ─────────────────────────────────────────────────────────────

@dataclass
class ParishRecord:
    """
    Un registro parroquial de inversión y necesidad — corte transversal.

    id:                 str  — identificador canónico: 'P-01', 'P-06', etc.
    nombre:             str  — nombre de la parroquia
    tipo:               str  — 'Urbana' | 'Rural'
    poblacion:          int  — población censo 2022
    nbi_pct:            float — % NBI (0–100)
    cobertura_agua_pct: float — % cobertura agua potable (0–100)
    inv_percapita:      float — inversión por habitante USD (H99_ENGINE_CORE)
    iet_local_pct:      float — Índice de Equidad Territorial local (Gold Master output)
    """
    id:                  str
    nombre:              str
    tipo:                str
    poblacion:           int
    nbi_pct:             float
    cobertura_agua_pct:  float
    inv_percapita:       float
    iet_local_pct:       float
    metadatos:           Optional[dict] = None


@dataclass
class ParishAnalysis:
    """Análisis de equidad para una parroquia."""
    id:                       str
    nombre:                   str
    tipo:                     str
    composite_need:           float    # CN_i — score de necesidad compuesto (0–100)
    need_share:               float    # fracción esperada del presupuesto total (0–1)
    expected_inv_percapita:   float    # USD/hab equitativo según necesidad
    actual_inv_percapita:     float    # USD/hab real (input)
    gap_abs:                  float    # actual − expected (USD/hab)
    gap_pct:                  float    # (actual − expected) / expected (fracción)
    overfunded:               bool     # True si recibe más de lo equitativo
    raw_flags:                List[str] = field(default_factory=list)


@dataclass
class D4Result:
    """Salida completa del motor de equidad territorial D4."""

    # ── Métricas globales ──────────────────────────────────────────────────────
    irs:                    float    # Inverse Regresivity Score 0–100 (>60 = crítico)
    gini:                   float    # Gini de inversión per cápita ponderado por pop (0–1)
    cr1:                    float    # Concentración top-1 parroquia (fracción 0–1)
    cr2:                    float    # Concentración top-2 parroquias (fracción 0–1)
    capital_ratio:          float    # inv_percapita capital / media rural ponderada
    rural_mean_inv:         float    # USD/hab — media rural ponderada por población
    urban_inv:              float    # USD/hab — capital cantonal

    # ── Análisis parroquial ────────────────────────────────────────────────────
    parish_analyses:        List[ParishAnalysis]
    most_underfunded:       List[str]   # top-3 nombres por mayor brecha negativa
    most_overfunded:        List[str]   # top-3 nombres por mayor brecha positiva

    # ── Flags crudos (sin calibrar) ───────────────────────────────────────────
    raw_flags:              List[str]

    # ── Meta ──────────────────────────────────────────────────────────────────
    n_parishes:             int
    n_rural:                int
    n_urban:                int
    total_investment:       float   # USD totales en el cantón (Σ pop_i × inv_i)
    cantonal_inv_percapita: float   # USD/hab media cantonal ponderada

    # ── Contextual para calibración ───────────────────────────────────────────
    max_gap_pct:            float   # mayor brecha negativa (valor absoluto)
    n_critical_underfunded: int     # parroquias con gap < −50%
    n_hydric_deficit:       int     # parroquias con agua < 10% y gap negativo


# ── CÓMPUTOS MATEMÁTICOS ──────────────────────────────────────────────────────

def _composite_need(p: ParishRecord, pop_total: int) -> float:
    """
    CN_i = 0.5 × NBI_i + 0.3 × (100 − agua_i) + 0.2 × (pop_i / pop_total × 100)

    Pesos canónicos Gold Master v5.5 H99_ENGINE_CORE.
    Cuanto mayor el score, mayor la necesidad territorial.
    """
    pop_share_pct = (p.poblacion / pop_total * 100.0) if pop_total > 0 else 0.0
    return (
        _W_NBI  * p.nbi_pct +
        _W_AGUA * max(0.0, 100.0 - p.cobertura_agua_pct) +
        _W_POP  * pop_share_pct
    )


def _compute_irs(parishes: List[ParishRecord]) -> float:
    """
    IRS = −CORREL(NBI_pct, inv_percapita) × 100

    IRS > 0  → inversión regresiva (más NBI = menos inversión)
    IRS > 70 → Ruptura Institucional
    IRS = 0  → distribución neutral respecto a necesidad
    IRS < 0  → inversión progresiva (más NBI = más inversión) — ideal

    Fórmula canónica: Gold Master H99_ENGINE_CORE IRS formula.
    """
    n = len(parishes)
    if n < 2:
        return 0.0

    nbi = [p.nbi_pct      for p in parishes]
    inv = [p.inv_percapita for p in parishes]

    nbi_mean = sum(nbi) / n
    inv_mean = sum(inv) / n

    cov     = sum((nbi[i] - nbi_mean) * (inv[i] - inv_mean) for i in range(n)) / n
    std_nbi = math.sqrt(sum((x - nbi_mean) ** 2 for x in nbi) / n)
    std_inv = math.sqrt(sum((x - inv_mean) ** 2 for x in inv) / n)

    if std_nbi < 1e-9 or std_inv < 1e-9:
        return 0.0

    corr = cov / (std_nbi * std_inv)
    return max(-100.0, min(100.0, -corr * 100.0))


def _compute_gini(parishes: List[ParishRecord]) -> float:
    """
    Gini de inversión total por parroquia, ponderado por población (Lorenz trapezoidal).

    0 = perfecta igualdad per cápita
    1 = toda la inversión concentrada en una parroquia
    """
    pop_total = sum(p.poblacion for p in parishes)
    inv_total = sum(p.inv_percapita * p.poblacion for p in parishes)

    if inv_total < 1.0 or pop_total < 1:
        return 0.0

    sorted_p = sorted(parishes, key=lambda p: p.inv_percapita)

    cum_pop, cum_inv, area = 0.0, 0.0, 0.0
    prev_p, prev_l = 0.0, 0.0

    for p in sorted_p:
        this_pop = p.poblacion / pop_total
        this_inv = (p.inv_percapita * p.poblacion) / inv_total
        cum_pop += this_pop
        cum_inv += this_inv
        area    += (cum_pop - prev_p) * (prev_l + cum_inv) / 2.0
        prev_p, prev_l = cum_pop, cum_inv

    return max(0.0, min(1.0, 1.0 - 2.0 * area))


# ── API PRINCIPAL ──────────────────────────────────────────────────────────────

def analyze_territory(parishes: List[ParishRecord]) -> D4Result:
    """
    Analiza la equidad territorial de inversión pública.

    Computa: IRS · Gini · CR1/CR2 · baseline need-proporcional · brecha parroquial.

    Args:
        parishes: lista de ParishRecord (≥1, idealmente ≥4 para métricas significativas)

    Returns:
        D4Result — análisis completo, determinístico

    Raises:
        ValueError: si parishes está vacío
    """
    if not parishes:
        raise ValueError("analyze_territory requiere al menos una parroquia")

    pop_total = sum(p.poblacion for p in parishes)
    if pop_total == 0:
        raise ValueError("Población total es 0 — datos inválidos")

    # ── 1. Composite Need + Need-weighted shares ───────────────────────────────
    needs: dict[str, float] = {p.id: _composite_need(p, pop_total) for p in parishes}

    # NS_i = CN_i × pop_i — necesidad ponderada por población
    ns: dict[str, float] = {p.id: needs[p.id] * p.poblacion for p in parishes}
    ns_total = sum(ns.values())

    # Inversión total del cantón: Σ (inv_percapita_i × pop_i)
    total_inv = sum(p.inv_percapita * p.poblacion for p in parishes)
    cantonal_inv_percapita = total_inv / pop_total

    # ── 2. Análisis por parroquia ──────────────────────────────────────────────
    analyses: List[ParishAnalysis] = []

    for p in parishes:
        expected_share    = ns[p.id] / ns_total if ns_total > 1e-9 else 1.0 / len(parishes)
        expected_total    = total_inv * expected_share
        expected_percap   = expected_total / p.poblacion if p.poblacion > 0 else 0.0
        gap_abs           = p.inv_percapita - expected_percap
        gap_pct           = gap_abs / expected_percap if expected_percap > 1e-9 else 0.0

        flags: List[str] = []
        if gap_pct < _GAP_CRITICO and p.tipo == "Rural":
            flags.append(f"REZAGO_RURAL: gap={gap_pct:.0%} vs baseline")
        if p.cobertura_agua_pct < _AGUA_CRITICA and gap_abs < 0:
            flags.append(f"INEQUIDAD_HIDRICA: agua={p.cobertura_agua_pct:.1f}%, "
                         f"actual=${p.inv_percapita:.0f} vs esperado=${expected_percap:.0f}/hab")

        analyses.append(ParishAnalysis(
            id                     = p.id,
            nombre                 = p.nombre,
            tipo                   = p.tipo,
            composite_need         = needs[p.id],
            need_share             = expected_share,
            expected_inv_percapita = expected_percap,
            actual_inv_percapita   = p.inv_percapita,
            gap_abs                = gap_abs,
            gap_pct                = gap_pct,
            overfunded             = gap_abs > 0,
            raw_flags              = flags,
        ))

    # Ordenar por brecha (más negativa primero)
    sorted_by_gap  = sorted(analyses, key=lambda a: a.gap_pct)
    most_underfunded = [a.nombre for a in sorted_by_gap[:3]  if a.gap_pct < 0]
    most_overfunded  = [a.nombre for a in sorted_by_gap[::-1][:3] if a.gap_pct > 0]

    # ── 3. Métricas globales ───────────────────────────────────────────────────
    irs_val  = _compute_irs(parishes)
    gini_val = _compute_gini(parishes)

    # CR1 / CR2 — concentración por inversión total
    inv_by_parish = sorted(
        [(p.inv_percapita * p.poblacion, p) for p in parishes],
        key=lambda t: t[0],
        reverse=True,
    )
    cr1 = inv_by_parish[0][0] / total_inv if total_inv > 1e-9 else 0.0
    cr2 = sum(t[0] for t in inv_by_parish[:2]) / total_inv if total_inv > 1e-9 else 0.0

    # Capital ratio — urbana vs media rural ponderada
    urban  = [p for p in parishes if p.tipo == "Urbana"]
    rural  = [p for p in parishes if p.tipo == "Rural"]

    rural_pop   = sum(p.poblacion for p in rural)
    rural_inv_w = sum(p.inv_percapita * p.poblacion for p in rural)
    rural_mean  = rural_inv_w / rural_pop if rural_pop > 0 else 1.0

    urban_inv_pc  = urban[0].inv_percapita if urban else cantonal_inv_percapita
    capital_ratio = urban_inv_pc / rural_mean if rural_mean > 1e-9 else 1.0

    # ── 4. Flags crudos ───────────────────────────────────────────────────────
    raw_flags: List[str] = []

    if irs_val >= _IRS_CRITICO:
        raw_flags.append("CONCENTRACION_TERRITORIAL")
    elif irs_val >= _IRS_ALTO:
        raw_flags.append("SESGO_DISTRIBUTIVO_ALTO")

    if capital_ratio >= _CAPITAL_RATIO_ALT:
        raw_flags.append("CAPTURA_CAPITAL")

    if cr1 >= _CR1_CONCENTRADO:
        raw_flags.append("MONOEJECUCION_TERRITORIAL")

    n_critical = sum(1 for a in analyses if a.gap_pct < _GAP_CRITICO)
    if n_critical >= 2:
        raw_flags.append("REZAGO_PERSISTENTE")

    n_hydric = sum(
        1 for p in parishes
        if p.cobertura_agua_pct < _AGUA_CRITICA and
        next((a.gap_pct for a in analyses if a.id == p.id), 0.0) < 0
    )
    if n_hydric >= 1:
        raw_flags.append("INEQUIDAD_HIDRICA")

    max_gap_pct = abs(min((a.gap_pct for a in analyses), default=0.0))

    return D4Result(
        irs                    = irs_val,
        gini                   = gini_val,
        cr1                    = cr1,
        cr2                    = cr2,
        capital_ratio          = capital_ratio,
        rural_mean_inv         = rural_mean,
        urban_inv              = urban_inv_pc,
        parish_analyses        = analyses,
        most_underfunded       = most_underfunded,
        most_overfunded        = most_overfunded,
        raw_flags              = raw_flags,
        n_parishes             = len(parishes),
        n_rural                = len(rural),
        n_urban                = len(urban),
        total_investment       = total_inv,
        cantonal_inv_percapita = cantonal_inv_percapita,
        max_gap_pct            = max_gap_pct,
        n_critical_underfunded = n_critical,
        n_hydric_deficit       = n_hydric,
    )


def summarize_d4(result: D4Result) -> str:
    """Resumen textual compacto para logs y debug."""
    lines = [
        f"D4 Territory — IRS={result.irs:.1f} · Gini={result.gini:.3f} "
        f"· CR1={result.cr1:.0%} · CapRatio={result.capital_ratio:.1f}x",
        f"  Parroquias: {result.n_parishes} ({result.n_urban} urbana, {result.n_rural} rural)",
        f"  Rezago crítico (gap<-50%): {result.n_critical_underfunded} parroquias",
        f"  Más sub-financiadas: {', '.join(result.most_underfunded)}",
        f"  Flags: {result.raw_flags}",
    ]
    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    # Test con datos reales de Montecristi (Gold Master v5.5)
    _test_parishes = [
        ParishRecord("P-01", "Montecristi",     "Urbana", 39800, 38.4, 95.00, 217, 193.75),
        ParishRecord("P-02", "Anibal San Andres","Rural",  5200, 52.1, 67.01,  58,  51.79),
        ParishRecord("P-03", "Colorado",         "Rural",  3800, 58.7, 38.82,  32,  28.57),
        ParishRecord("P-04", "Leonidas Proano",  "Rural",  4100, 54.3,100.00,  48,  42.86),
        ParishRecord("P-05", "Gral. Alfaro",     "Rural",  6300, 49.8,100.00,  71,  63.39),
        ParishRecord("P-06", "Isabel Muentes",   "Rural",  5700, 61.2,  1.02,  40,  35.71),
        ParishRecord("P-07", "La Pila",          "Rural",  4600, 55.9, 50.00,  52,  46.43),
    ]

    r = analyze_territory(_test_parishes)
    print("=" * 65)
    print("D4 Engine — Montecristi (Gold Master v5.5 H99_ENGINE_CORE)")
    print("=" * 65)
    print(f"IRS            : {r.irs:.2f}  (Gold Master canonical: 79.7)")
    print(f"Gini           : {r.gini:.4f}")
    print(f"CR1            : {r.cr1:.2%}  (top-1 parroquia)")
    print(f"CR2            : {r.cr2:.2%}  (top-2 parroquias)")
    print(f"Capital ratio  : {r.capital_ratio:.2f}x  (urbana / media rural)")
    print(f"Rural mean inv : ${r.rural_mean_inv:.1f}/hab")
    print(f"Cantonal avg   : ${r.cantonal_inv_percapita:.1f}/hab")
    print(f"Flags          : {r.raw_flags}")
    print()
    print(f"{'Parroquia':<22} {'Tipo':<8} {'Actual':>8} {'Esperado':>9} {'Gap%':>7} {'Gap$':>8}")
    print("-" * 65)
    for a in sorted(r.parish_analyses, key=lambda a: a.gap_pct):
        sign = "+" if a.gap_abs >= 0 else ""
        print(f"{a.nombre:<22} {a.tipo:<8} ${a.actual_inv_percapita:>6.0f} "
              f"${a.expected_inv_percapita:>7.0f} "
              f"{a.gap_pct:>+6.0%}  {sign}${a.gap_abs:>6.0f}")
        for flag in a.raw_flags:
            print(f"  -> {flag}")
    print("=" * 65)
