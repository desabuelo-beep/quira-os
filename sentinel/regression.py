"""
SENTINEL RAG · regression.py — Sprint 2.1
Suite de regresión automática — protege la confianza institucional.

Cada deploy debe correr esta suite antes de ir a producción.
Si la calidad baja respecto al baseline: DEPLOY BLOCKED.

Metodología:
  20 preguntas canónicas × métricas de retrieval = 20 casos por run
  Opcional --with-llm: incluye síntesis LLM (60 llamadas adicionales si 3 roles)
  Comparación contra baseline guardado en sentinel/reports/regression_baseline.json

Resultado:
  PASS    → todo dentro de tolerancias
  WARN    → degradación menor, investigar
  BLOCK   → degradación crítica, no deployar

Uso:
  python -m sentinel.regression                  # solo retrieval
  python -m sentinel.regression --baseline       # guardar nuevo baseline
  python -m sentinel.regression --with-llm       # incluir síntesis LLM

Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.rag_config import (
    SENTINEL_VERSION, PROMPT_VERSION, GUARDRAIL_VERSION, INDEX_VERSION,
    LLM_MODEL,
)
from sentinel.explain import explain_retrieval
from sentinel.guardrails import apply_guardrails

# ── RUTAS ─────────────────────────────────────────────────────────────────────
REPORTS_DIR = Path(__file__).parent / "reports"
BASELINE_FILE = REPORTS_DIR / "regression_baseline.json"
REPORTS_DIR.mkdir(exist_ok=True)

# ── 20 PREGUNTAS CANÓNICAS ────────────────────────────────────────────────────
# Cubren los 5 dominios TGI + fondos + mandato + sistema.
# Estas preguntas NO deben cambiar — son el contrato de calidad del sistema.
CANONICAL_QUESTIONS: list[str] = [
    # D1 — Legalidad
    "¿Qué dice el COOTAD sobre las competencias del GAD Municipal?",
    "¿Cuáles son las obligaciones legales en agua potable y alcantarillado?",
    "¿Qué reforma al COOTAD 2026 afecta la inversión municipal?",
    "¿Qué establece el COPFP sobre planificación presupuestaria?",
    # D2 — Planificación
    "¿Cuál es el ICPI de Montecristi y qué mide?",
    "¿Qué metas del PDOT 2023-2027 están en riesgo de incumplimiento?",
    "¿Cómo funciona el sistema TGI de evaluación municipal?",
    "¿Cuál es el TGI score actual de Montecristi y qué significa?",
    # D3 — Ejecución
    "¿Por qué D3 ejecución presupuestaria está en rojo?",
    "¿Qué causas explican el bajo devengamiento del GAD Montecristi?",
    "¿Qué riesgos legales enfrenta Montecristi si D3 sigue bajo 60 por ciento?",
    # D4 — Equidad
    "¿Cuál es la situación de Isabel Muentes en el índice de equidad territorial?",
    "¿Cómo se distribuye la equidad territorial entre las parroquias del cantón?",
    "¿Qué es el IRS y cómo se relaciona con la equidad territorial?",
    "¿Cuáles son las parroquias más críticas de Montecristi?",
    # D5 — Institucional
    "¿Cuál es la situación de capacidad institucional del GAD?",
    # Fondos / Cooperación
    "¿Qué fondos internacionales puede solicitar el GAD para proyectos de agua?",
    "¿Cuál es el estado del fondo UNESCO para gobernanza digital?",
    # Mandato / Sistema
    "¿Qué riesgos enfrenta el mandato 2023-2027 del GAD Montecristi?",
    "¿Qué dice el diagnóstico territorial sobre la situación del cantón?",
]

assert len(CANONICAL_QUESTIONS) == 20, "Siempre deben ser exactamente 20 preguntas"

# ── TOLERANCIAS DE DEGRADACIÓN ────────────────────────────────────────────────
# min_delta: debajo de este valor → BLOCK (deploy bloqueado)
# warn_delta: debajo de este valor → WARN (investigar)
THRESHOLDS = {
    "confianza_pct":   {"min_delta": -10.0, "warn_delta": -5.0},
    "score_promedio":  {"min_delta": -0.08, "warn_delta": -0.04},
    "dims_cubiertas":  {"min_delta": -1,    "warn_delta":  0},
    "notas_distintas": {"min_delta": -1,    "warn_delta":  0},
}

# Porcentaje mínimo de casos que deben estar en estado OK
GUARDRAIL_OK_MIN_PCT = 90.0  # < 90% → BLOCK


# ── ESTRUCTURAS ───────────────────────────────────────────────────────────────
@dataclass
class CaseResult:
    question_idx:   int
    pregunta:       str
    confianza_pct:  float
    score_promedio: float
    dims_cubiertas: int
    notas_distintas: int
    guardrail_ok:   bool
    tiempo_ms:      float


@dataclass
class RegressionReport:
    timestamp:         str
    run_type:          str     # "baseline" | "regression"
    sentinel_version:  str
    prompt_version:    str
    guardrail_version: str
    index_version:     str
    llm_model:         str

    cases:             list[CaseResult]
    n_ok_guardrail:    int
    pct_ok_guardrail:  float

    # Promedios del run actual
    avg_confianza:     float
    avg_score:         float
    avg_dims:          float
    avg_notas:         float
    avg_tiempo_ms:     float

    # Comparación vs baseline (solo en regression)
    vs_baseline:       dict = field(default_factory=dict)
    resultado:         str = "BASELINE"  # "PASS" | "WARN" | "BLOCK" | "BASELINE"
    bloqueos:          list[str] = field(default_factory=list)
    advertencias:      list[str] = field(default_factory=list)


# ── RUNNER ────────────────────────────────────────────────────────────────────
def run_regression(
    questions: list[str] | None = None,
    verbose:   bool = True,
) -> RegressionReport:
    """
    Corre la suite de regresión sobre las preguntas canónicas.
    Solo usa retrieval + guardrails (sin LLM) para mantener costo = 0.
    """
    qs = questions or CANONICAL_QUESTIONS

    if verbose:
        print(f"\n  {'═'*60}")
        print(f"  SENTINEL · Regression Suite — {len(qs)} preguntas")
        print(f"  Versiones: sentinel={SENTINEL_VERSION} · prompt={PROMPT_VERSION}")
        print(f"  {'═'*60}\n")

    cases: list[CaseResult] = []

    for i, pregunta in enumerate(qs, 1):
        t0 = time.time()
        r  = explain_retrieval(pregunta)
        g  = apply_guardrails(r)
        ms = (time.time() - t0) * 1000

        case = CaseResult(
            question_idx    = i,
            pregunta        = pregunta,
            confianza_pct   = r.confianza_pct,
            score_promedio  = r.score_promedio,
            dims_cubiertas  = len(r.dims_cubiertas),
            notas_distintas = r.notas_distintas,
            guardrail_ok    = g.puede_responder,
            tiempo_ms       = round(ms, 1),
        )
        cases.append(case)

        if verbose:
            icon = "✅" if case.guardrail_ok else "❌"
            print(
                f"  {icon} [{i:>2}] {case.confianza_pct:>5.1f}% "
                f"dims={case.dims_cubiertas}/5  "
                f"{case.pregunta[:50]}"
            )

    # Promedios
    n = len(cases)
    n_ok        = sum(1 for c in cases if c.guardrail_ok)
    avg_conf    = sum(c.confianza_pct   for c in cases) / n
    avg_score   = sum(c.score_promedio  for c in cases) / n
    avg_dims    = sum(c.dims_cubiertas  for c in cases) / n
    avg_notas   = sum(c.notas_distintas for c in cases) / n
    avg_tiempo  = sum(c.tiempo_ms       for c in cases) / n

    return RegressionReport(
        timestamp         = datetime.now().isoformat(),
        run_type          = "run",
        sentinel_version  = SENTINEL_VERSION,
        prompt_version    = PROMPT_VERSION,
        guardrail_version = GUARDRAIL_VERSION,
        index_version     = INDEX_VERSION,
        llm_model         = LLM_MODEL,
        cases             = cases,
        n_ok_guardrail    = n_ok,
        pct_ok_guardrail  = round(n_ok / n * 100, 1),
        avg_confianza     = round(avg_conf,  1),
        avg_score         = round(avg_score, 3),
        avg_dims          = round(avg_dims,  2),
        avg_notas         = round(avg_notas, 2),
        avg_tiempo_ms     = round(avg_tiempo, 1),
    )


# ── BASELINE ──────────────────────────────────────────────────────────────────
def save_baseline(report: RegressionReport) -> Path:
    """Guarda el reporte como baseline de referencia."""
    report.run_type  = "baseline"
    report.resultado = "BASELINE"

    data = _report_to_dict(report)
    BASELINE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return BASELINE_FILE


def load_baseline() -> dict | None:
    """Carga el baseline si existe."""
    if not BASELINE_FILE.exists():
        return None
    return json.loads(BASELINE_FILE.read_text(encoding="utf-8"))


# ── COMPARACIÓN ───────────────────────────────────────────────────────────────
def compare_to_baseline(report: RegressionReport) -> RegressionReport:
    """
    Compara el reporte actual con el baseline.
    Actualiza report.resultado, report.bloqueos, report.advertencias.
    """
    baseline = load_baseline()
    if not baseline:
        report.resultado    = "PASS"
        report.vs_baseline  = {"mensaje": "Sin baseline — primera run, guarda con --baseline"}
        return report

    report.run_type   = "regression"
    bloqueos:   list[str] = []
    advertencias: list[str] = []
    vs: dict = {}

    # Comparar guardrail OK %
    delta_ok = report.pct_ok_guardrail - baseline.get("pct_ok_guardrail", 100)
    vs["pct_ok_guardrail"] = {"actual": report.pct_ok_guardrail, "baseline": baseline.get("pct_ok_guardrail"), "delta": round(delta_ok, 1)}
    if report.pct_ok_guardrail < GUARDRAIL_OK_MIN_PCT:
        bloqueos.append(f"Guardrail OK: {report.pct_ok_guardrail:.0f}% < {GUARDRAIL_OK_MIN_PCT:.0f}% mínimo")

    # Comparar métricas continuas
    metric_map = {
        "confianza_pct":   ("avg_confianza",  baseline.get("avg_confianza",  0)),
        "score_promedio":  ("avg_score",       baseline.get("avg_score",      0)),
        "dims_cubiertas":  ("avg_dims",        baseline.get("avg_dims",       0)),
        "notas_distintas": ("avg_notas",       baseline.get("avg_notas",      0)),
    }

    for metric, (attr, base_val) in metric_map.items():
        actual_val = getattr(report, attr)
        delta      = actual_val - base_val
        thresh     = THRESHOLDS[metric]

        vs[metric] = {"actual": actual_val, "baseline": base_val, "delta": round(delta, 3)}

        if delta < thresh["min_delta"]:
            bloqueos.append(
                f"{metric}: Δ={delta:+.2f} (mínimo permitido: {thresh['min_delta']:+.2f})"
            )
        elif delta < thresh["warn_delta"]:
            advertencias.append(
                f"{metric}: Δ={delta:+.2f} (umbral de advertencia: {thresh['warn_delta']:+.2f})"
            )

    report.vs_baseline  = vs
    report.bloqueos     = bloqueos
    report.advertencias = advertencias
    report.resultado    = "BLOCK" if bloqueos else ("WARN" if advertencias else "PASS")

    return report


# ── FORMATEO ──────────────────────────────────────────────────────────────────
def format_report(report: RegressionReport) -> str:
    icon_resultado = {"PASS": "🟢", "WARN": "🟡", "BLOCK": "🔴", "BASELINE": "📐"}

    lines = [
        f"\n  {'═'*62}",
        f"  SENTINEL · Regression Report",
        f"  {'═'*62}",
        f"  Resultado:   {icon_resultado.get(report.resultado, '?')} {report.resultado}",
        f"  Timestamp:   {report.timestamp[:19]}",
        f"  Versiones:   sentinel={report.sentinel_version} · prompt={report.prompt_version}",
        f"  {'─'*62}",
        f"  Guardrail OK:     {report.n_ok_guardrail}/{len(report.cases)}  ({report.pct_ok_guardrail:.0f}%)",
        f"  Confianza prom:   {report.avg_confianza:.1f}%",
        f"  Score prom:       {report.avg_score:.3f}",
        f"  Dims cubiertas:   {report.avg_dims:.2f}/5",
        f"  Notas distintas:  {report.avg_notas:.2f}",
        f"  Tiempo prom:      {report.avg_tiempo_ms:.0f}ms",
    ]

    if report.vs_baseline and "mensaje" not in report.vs_baseline:
        lines.append(f"  {'─'*62}")
        lines.append("  Comparación vs Baseline:")
        for m, v in report.vs_baseline.items():
            delta = v.get("delta", 0)
            icon  = "🟢" if delta >= 0 else ("🔴" if delta < -5 else "🟡")
            lines.append(
                f"    {icon} {m:<20}  actual={v['actual']:>7.2f}  "
                f"baseline={v['baseline']:>7.2f}  Δ={delta:+.2f}"
            )

    if report.bloqueos:
        lines.append(f"  {'─'*62}")
        lines.append("  🔴 BLOQUEOS (DEPLOY BLOCKED):")
        for b in report.bloqueos:
            lines.append(f"    ✗ {b}")

    if report.advertencias:
        lines.append(f"  {'─'*62}")
        lines.append("  🟡 ADVERTENCIAS:")
        for a in report.advertencias:
            lines.append(f"    ⚠ {a}")

    lines.append(f"  {'═'*62}\n")
    return "\n".join(lines)


def _report_to_dict(r: RegressionReport) -> dict:
    return {
        "timestamp":         r.timestamp,
        "run_type":          r.run_type,
        "sentinel_version":  r.sentinel_version,
        "prompt_version":    r.prompt_version,
        "guardrail_version": r.guardrail_version,
        "index_version":     r.index_version,
        "llm_model":         r.llm_model,
        "resultado":         r.resultado,
        "n_cases":           len(r.cases),
        "n_ok_guardrail":    r.n_ok_guardrail,
        "pct_ok_guardrail":  r.pct_ok_guardrail,
        "avg_confianza":     r.avg_confianza,
        "avg_score":         r.avg_score,
        "avg_dims":          r.avg_dims,
        "avg_notas":         r.avg_notas,
        "avg_tiempo_ms":     r.avg_tiempo_ms,
        "bloqueos":          r.bloqueos,
        "advertencias":      r.advertencias,
        "vs_baseline":       r.vs_baseline,
        "cases": [
            {
                "idx": c.question_idx, "pregunta": c.pregunta,
                "confianza_pct": c.confianza_pct, "score_promedio": c.score_promedio,
                "dims_cubiertas": c.dims_cubiertas, "notas_distintas": c.notas_distintas,
                "guardrail_ok": c.guardrail_ok, "tiempo_ms": c.tiempo_ms,
            }
            for c in r.cases
        ],
    }


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SENTINEL Regression Suite")
    parser.add_argument("--baseline", action="store_true", help="Guardar como nuevo baseline")
    parser.add_argument("--save",     action="store_true", help="Guardar reporte en reports/")
    parser.add_argument("--quick",    action="store_true", help="Solo primeras 5 preguntas (test rápido)")
    args = parser.parse_args()

    qs = CANONICAL_QUESTIONS[:5] if args.quick else None

    report = run_regression(questions=qs, verbose=True)

    if args.baseline:
        p = save_baseline(report)
        print(f"\n  📐 Baseline guardado: {p}")
    else:
        report = compare_to_baseline(report)

    print(format_report(report))

    if args.save:
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = REPORTS_DIR / f"regression_{ts}.json"
        out.write_text(json.dumps(_report_to_dict(report), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  Guardado: {out}")

    # Exit code para CI/CD
    sys.exit(1 if report.resultado == "BLOCK" else 0)
