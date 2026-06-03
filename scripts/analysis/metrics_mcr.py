# -*- coding: utf-8 -*-
"""
metrics_mcr.py — Score Territorial MCR desde Gold Master Canonico
QUIRA Gov · Gate 5C (corregido) · Dylus Lab (c) 2026

DOCTRINA (regla de oro QUIRA):
  Excel Canon = fuente de verdad. Excel -> Python -> Supabase -> UI.
  Este script LEE las metricas calculadas por el Motor ICPI del Gold Master
  via app/connectors/gold_master.py (H73_OUTPUT_API).
  NO calcula nada por su cuenta. NO duplica logica del Excel.

El Motor ICPI del Excel ya calcula:
  ICPI     = Indice Compuesto de Progreso Institucional (17.45% Q1-2026 | 69.93% 2025)
  TGI      = TGI Score 5D (66.79%)
  D1-D5    = 5 dimensiones ponderadas
  ITAM     = Transparencia real (82.29%) / IOC opacidad (17.71%)
  IED      = Eficiencia Directiva (16.52%)
  SAT      = Alertas activas (2 activas, riesgo MEDIO)

El Gap A<>D real (desde el Excel):
  SIGAD declara ICM = 1.00 (100%)
  IOC_OPACIDAD = 17.71% (brecha de transparencia observable)
  D3 Ejecucion = 59.85% (dimension mas debil del TGI)

Uso:
  python -X utf8 scripts/analysis/metrics_mcr.py
  python -X utf8 scripts/analysis/metrics_mcr.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


def fetch() -> dict:
    """Lee metricas canonicas desde el Gold Master via conector oficial."""
    from app.connectors.gold_master import fetch_gold_master_data
    result = fetch_gold_master_data()
    if result["status"] == "failed":
        raise RuntimeError(f"Gold Master no disponible: {result['error']}")
    raw = result["data"].get("_raw_h73", {})
    tgi = result["data"].get("tgi", {})
    icpi = result["data"].get("icpi", {})
    sat = result["data"].get("sat_engine", {})
    return {
        "fuente":          "Gold Master v5.5 SIAP-ICPI (H73_OUTPUT_API)",
        "entidad":         raw.get("ENTIDAD", "GAD MCR"),
        "periodo_corte":   str(raw.get("PERIODO_CORTE", "")),
        # ICPI por ano (historico + actual)
        "icpi_2023":       round(icpi.get("historico", {}).get("2023", 0) * 100, 2),
        "icpi_2024":       round(icpi.get("historico", {}).get("2024", 0) * 100, 2),
        "icpi_2025":       round(icpi.get("historico", {}).get("2025", 0) * 100, 2),
        "icpi_q1_2026":    round((icpi.get("acumulado_q1") or 0) * 100, 2),
        "icpi_clasif":     icpi.get("clasificacion", ""),
        # TGI 5 dimensiones
        "tgi_score":       round(tgi.get("score", 0), 2),
        "tgi_d1_legalidad":     round(tgi.get("d1", 0), 2),
        "tgi_d2_planificacion": round(tgi.get("d2", 0), 2),
        "tgi_d3_ejecucion":     round(tgi.get("d3", 0), 2),
        "tgi_d4_equidad":       round(tgi.get("d4", 0), 2),
        "tgi_d5_capacidad":     round(tgi.get("d5", 0), 2),
        # Transparencia (ITAM) y Opacidad (IOC) — del Motor Excel
        "itam_transparencia": round((raw.get("ITAM_2025_REF") or 0) * 100, 2),
        "ioc_opacidad":       round((raw.get("IOC_OPACIDAD") or 0) * 100, 2),
        # Gap A<>D real: lo que el Excel calcula como opacidad observable
        "gap_a_d_ioc":        round((raw.get("IOC_OPACIDAD") or 0) * 100, 2),
        # SAT
        "sat_activas":     int(sat.get("activas_count") or 0),
        "sat_riesgo":      sat.get("clasif_riesgo", ""),
        # Financiero
        "presupuesto_total":  raw.get("PRESUPUESTO_TOTAL_4E"),
        "gad_devengado_q1":   raw.get("GAD_DEVENGADO_Q1"),
        "trust_score":        raw.get("TRUST_SCORE"),
    }


def print_report(d: dict) -> None:
    print("\n" + "=" * 62)
    print("  QUIRA -- Score Territorial Canonico")
    print(f"  {d['entidad']} -- Corte: {d['periodo_corte']}")
    print(f"  Fuente: {d['fuente']}")
    print("=" * 62)

    print("\n  ICPI -- Indice Compuesto de Progreso Institucional")
    print(f"    2023: {d['icpi_2023']:>6.2f}%  |  2024: {d['icpi_2024']:>6.2f}%"
          f"  |  2025: {d['icpi_2025']:>6.2f}%")
    print(f"    Q1-2026 (parcial): {d['icpi_q1_2026']:>6.2f}%   {d['icpi_clasif']}")
    print(f"    Meta PDOT 2027: 65.0%   Brecha: {65.0 - d['icpi_2025']:+.2f} pts")

    print("\n  TGI -- Score Territorial (5 Dimensiones)")
    print(f"    Score Global:  {d['tgi_score']:>6.2f}%")
    dims = [
        ("D1 Legalidad",     d["tgi_d1_legalidad"],     "#####....."),
        ("D2 Planificacion", d["tgi_d2_planificacion"],  "######...."),
        ("D3 Ejecucion",     d["tgi_d3_ejecucion"],      "#####....."),
        ("D4 Equidad",       d["tgi_d4_equidad"],        "####......"),
        ("D5 Capacidad",     d["tgi_d5_capacidad"],      "##########"),
    ]
    for name, val, _ in dims:
        bar = "#" * int(val / 10) + "." * (10 - int(val / 10))
        flag = " <-- gap critico" if val < 50 else (" <-- debil" if val < 65 else "")
        print(f"    {name:18s} [{bar}] {val:5.1f}%{flag}")

    print("\n  Transparencia (Motor ITAM del Excel):")
    print(f"    Transparencia observable: {d['itam_transparencia']:.2f}%")
    print(f"    Opacidad (IOC):           {d['ioc_opacidad']:.2f}%")
    print(f"    Gap A<>D real:            {d['gap_a_d_ioc']:.2f} pts de opacidad")

    print("\n  SAT -- Alertas Activas:")
    print(f"    {d['sat_activas']} alertas activas  --  Riesgo: {d['sat_riesgo']}")

    print("\n  Financiero:")
    if d.get("presupuesto_total"):
        print(f"    Presupuesto 4 entidades: ${d['presupuesto_total']:,.0f}")
    if d.get("gad_devengado_q1"):
        print(f"    GAD devengado Q1-2026:   ${d['gad_devengado_q1']:,.0f}")
    if d.get("trust_score"):
        print(f"    Trust Score: {d['trust_score']}  (modelo VALIDO)")

    print("\n" + "=" * 62 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    data = fetch()
    if args.as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        print_report(data)


if __name__ == "__main__":
    main()
