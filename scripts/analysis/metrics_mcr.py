# -*- coding: utf-8 -*-
"""
metrics_mcr.py — Primer Score Territorial Compuesto · GAD Montecristi
QUIRA Gov · Gate 5C · Dylus Lab © 2026

Calcula cuatro dimensiones del desempeño institucional a partir de los
datos ya ingresados en holding_structured_data y normativa_corpus.

Dimensiones:
  SIGAD_SCORE         — ICM reportado al SNP (evaluación externa)
  TRANSPARENCY_SCORE  — cobertura LOTAIP mensual publicada (%)
  TIMELINESS_SCORE    — puntualidad de envío de reportes (inverso de demora)
  COVERAGE_SCORE      — completitud del corpus documental del Holding

El gap observable A≠D es la distancia entre SIGAD_SCORE y TRANSPARENCY_SCORE.

Uso:
  python scripts/analysis/metrics_mcr.py
  python scripts/analysis/metrics_mcr.py --year 2024
  python scripts/analysis/metrics_mcr.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

import toml, streamlit as st
_raw = toml.load(str(ROOT / ".streamlit" / "secrets.toml"))
class _F:
    def get(self, k, d=None): return _raw.get(k, d)
    def __getitem__(self, k): return _raw[k]
st.secrets = _F()

from sentinel.db_config import get_connection


# ── CÁLCULO DE SCORES ─────────────────────────────────────────────────────────

def score_sigad(conn, entity: str = "GAD_MCR") -> dict:
    """ICM promedio de los años disponibles en SIGAD."""
    c = conn.cursor()
    c.execute("""
        SELECT periodo,
               (datos_json->>'icm')::float AS icm,
               (datos_json->>'demora_meses')::int AS demora
        FROM holding_structured_data
        WHERE evidence_type = 'SIGAD_ICM'
          AND source_entity = %s
        ORDER BY periodo
    """, (entity,))
    rows = c.fetchall()
    if not rows:
        return {"score": None, "detail": "sin datos SIGAD", "años": []}
    icms = [r["icm"] for r in rows if r["icm"] is not None]
    score = sum(icms) / len(icms) if icms else None
    return {
        "score": round(score * 100, 1) if score else None,
        "icm_promedio": score,
        "años": [{"periodo": r["periodo"], "icm": r["icm"],
                  "demora_meses": r["demora"]} for r in rows],
    }


def score_transparency(conn, entity: str = "GAD_MCR",
                       year: int | None = None) -> dict:
    """Cobertura LOTAIP: meses publicados / meses esperados (12 por año)."""
    c = conn.cursor()
    query = """
        SELECT periodo FROM holding_structured_data
        WHERE evidence_type = 'LOTAIP_DATOS'
          AND source_entity = %s
    """
    params = [entity]
    if year:
        query += " AND periodo LIKE %s"
        params.append(f"{year}-%")
    c.execute(query, params)
    rows = c.fetchall()

    by_year: dict[str, set] = {}
    for r in rows:
        p = r["periodo"]  # formato YYYY-MM
        yr = p[:4]
        by_year.setdefault(yr, set()).add(p[5:])  # mes MM

    detail = []
    total_expected = total_published = 0
    for yr in sorted(by_year):
        published = len(by_year[yr])
        expected = 12
        total_published += published
        total_expected += expected
        detail.append({"año": yr, "publicados": published,
                        "esperados": expected,
                        "cobertura_pct": round(published / expected * 100, 1)})

    score = (total_published / total_expected * 100) if total_expected else None
    return {
        "score": round(score, 1) if score else None,
        "meses_publicados": total_published,
        "meses_esperados": total_expected,
        "detalle_por_año": detail,
    }


def score_timeliness(conn, entity: str = "GAD_MCR") -> dict:
    """
    Puntualidad de envío SIGAD.
    Score = max(0, 100 - (demora_meses * 5))
    12 meses tarde → 40 pts | 6 meses → 70 pts | 0 meses → 100 pts
    """
    c = conn.cursor()
    c.execute("""
        SELECT periodo, (datos_json->>'demora_meses')::int AS demora
        FROM holding_structured_data
        WHERE evidence_type = 'SIGAD_ICM' AND source_entity = %s
        ORDER BY periodo
    """, (entity,))
    rows = c.fetchall()
    if not rows:
        return {"score": None, "detail": "sin datos SIGAD"}

    scores = []
    detail = []
    for r in rows:
        demora = r["demora"] or 0
        s = max(0, 100 - demora * 5)
        scores.append(s)
        detail.append({"periodo": r["periodo"], "demora_meses": demora,
                        "timeliness_score": s})

    return {
        "score": round(sum(scores) / len(scores), 1),
        "detalle": detail,
    }


def score_coverage(conn) -> dict:
    """
    Completitud del corpus documental del Holding MCR.
    Basado en siglas procesadas vs categorías esperadas.
    """
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT norma_sigla FROM normativa_corpus
        WHERE canton_id = 'MCR'
    """)
    siglas = {r["norma_sigla"] for r in c.fetchall()}

    # Categorías esperadas para circuito completo
    expected_categories = {
        "RC": ["RC-GAD-2023", "RC-GAD-2024"],
        "PP": ["PP-2023", "PP-2024", "PP-2025"],
        "POA-GAD": ["POA-GAD-2023", "POA-GAD-2024", "POA-GAD-2025", "POA-GAD-2026-v2"],
        "PAC-GAD": ["PAC-GAD-2023", "PAC-GAD-2024", "PAC-GAD-2025", "PAC-GAD-2026"],
        "SIGAD": ["SIGAD-GAD-2023-DOC", "SIGAD-GAD-2024-DOC"],
    }

    found = total = 0
    detail = {}
    for cat, expected_siglas in expected_categories.items():
        cat_found = [s for s in expected_siglas if s in siglas]
        found += len(cat_found)
        total += len(expected_siglas)
        detail[cat] = {
            "encontrados": len(cat_found),
            "esperados": len(expected_siglas),
            "siglas": cat_found,
        }

    score = found / total * 100 if total else 0
    return {
        "score": round(score, 1),
        "documentos_encontrados": found,
        "documentos_esperados": total,
        "detalle": detail,
    }


# ── REPORT ────────────────────────────────────────────────────────────────────

def compute_all(year: int | None = None) -> dict:
    conn = get_connection()

    s_sigad      = score_sigad(conn)
    s_transp     = score_transparency(conn, year=year)
    s_timeliness = score_timeliness(conn)
    s_coverage   = score_coverage(conn)
    conn.close()

    # Score compuesto ponderado
    weights = {"sigad": 0.30, "transparency": 0.30,
               "timeliness": 0.20, "coverage": 0.20}
    scores = {
        "sigad":        s_sigad["score"],
        "transparency": s_transp["score"],
        "timeliness":   s_timeliness["score"],
        "coverage":     s_coverage["score"],
    }
    valid = {k: v for k, v in scores.items() if v is not None}
    if valid:
        composite = sum(v * weights[k] for k, v in valid.items())
        composite /= sum(weights[k] for k in valid)
    else:
        composite = None

    # Gap A≠D: diferencia entre lo que el sistema dice y lo que publica
    gap_and = None
    if scores["sigad"] is not None and scores["transparency"] is not None:
        gap_and = round(scores["sigad"] - scores["transparency"], 1)

    return {
        "canton": "MCR — Montecristi",
        "entidad": "GAD_MCR",
        "fecha_calculo": "2026-06-03",
        "scores": scores,
        "composite_score": round(composite, 1) if composite else None,
        "gap_A_neq_D": gap_and,
        "detalle": {
            "sigad":        s_sigad,
            "transparency": s_transp,
            "timeliness":   s_timeliness,
            "coverage":     s_coverage,
        },
    }


def print_report(result: dict) -> None:
    print(f"\n{'='*60}")
    print(f"  QUIRA — Score Territorial Compuesto")
    print(f"  {result['canton']} · {result['entidad']}")
    print(f"  Calculado: {result['fecha_calculo']}")
    print(f"{'='*60}")

    s = result["scores"]
    print(f"\n  {'Dimensión':30s} {'Score':>8}  {'Peso':>6}")
    print(f"  {'-'*48}")
    dims = [
        ("SIGAD Score (evaluación externa)",  s["sigad"],        "30%"),
        ("Transparency Score (LOTAIP)",        s["transparency"], "30%"),
        ("Timeliness Score (puntualidad)",     s["timeliness"],   "20%"),
        ("Coverage Score (corpus docs)",       s["coverage"],     "20%"),
    ]
    for name, score, weight in dims:
        sc_str = f"{score:.1f}" if score is not None else "  n/d"
        print(f"  {name:30s} {sc_str:>8}  {weight:>6}")

    print(f"  {'-'*48}")
    cs = result["composite_score"]
    print(f"  {'Score Compuesto':30s} {cs:>8.1f}" if cs else "  Score Compuesto: n/d")

    gap = result["gap_A_neq_D"]
    if gap is not None:
        print(f"\n  [!] Gap A<>D (SIGAD - LOTAIP): {gap:+.1f} puntos")
        if gap > 50:
            print(f"      Divergencia ALTA: el GAD declara cumplimiento alto")
            print(f"      pero publica solo {s['transparency']:.0f}% de transparencia financiera.")

    # LOTAIP por año
    print(f"\n  Cobertura LOTAIP por año:")
    for d in result["detalle"]["transparency"].get("detalle_por_año", []):
        bar = "#" * int(d["cobertura_pct"] / 10) + "." * (10 - int(d["cobertura_pct"] / 10))
        print(f"    {d['año']}  [{bar}] {d['cobertura_pct']:5.1f}%  "
              f"({d['publicados']}/{d['esperados']} meses)")

    # SIGAD por año
    print(f"\n  SIGAD ICM por año:")
    for d in result["detalle"]["sigad"].get("años", []):
        print(f"    {d['periodo']}  ICM={d['icm']:.2f}  "
              f"(enviado con {d['demora_meses']} meses de retraso)")

    print(f"\n{'='*60}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    result = compute_all(year=args.year)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
