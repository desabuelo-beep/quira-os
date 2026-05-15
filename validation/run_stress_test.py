"""
QUIRA OS — Validación Fase 4
Stress Test Runner · Banco de Casos v1

Ejecutar desde la raíz del proyecto:
    python validation/run_stress_test.py

Salida:
    - Tabla de calibración por consola
    - validation/resultados_stress_test.json  (artefacto para el tester)

Doctrina: QUIRA fundamenta. La autoridad pública decide.
Dylus Lab © 2026
"""
from __future__ import annotations
import json
import sys
import io
import os
from pathlib import Path
from datetime import datetime

# ── Windows UTF-8 console fix ──────────────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── Path setup ─────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from data.loader import load_all
from sentinel.coherencia_engine import evaluate as coh_eval
from sentinel.legal_router import find_legal_refs
from sentinel.simulate_policy import simulate_policy

CASOS_PATH    = Path(__file__).parent / "banco_casos_v1.json"
RESULTADOS_PATH = Path(__file__).parent / "resultados_stress_test.json"

# ANSI colors for terminal
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def _ci_color(ci: int) -> str:
    if ci >= 80: return GREEN
    if ci >= 65: return CYAN
    if ci >= 50: return YELLOW
    return RED


def _in_range(ci: int, rng: list[int]) -> bool:
    return rng[0] <= ci <= rng[1]


def _run_caso(caso: dict, data: dict) -> dict:
    query     = caso["query"]
    territory = caso.get("territorio")
    sim_cfg   = caso.get("sim")

    # 1. Simulación (si aplica)
    sim_result = None
    if sim_cfg:
        sim_result = simulate_policy(
            policy_type = sim_cfg["policy_type"],
            territorio  = territory or "Montecristi",
            delta       = sim_cfg["delta"],
            quality     = sim_cfg.get("quality", "infraestructura"),
        )

    # 2. Referencias legales
    legal_refs = find_legal_refs(query, max_refs=3)

    # 3. Motor de Coherencia
    coh = coh_eval(
        query      = query,
        data       = data,
        sim_result = sim_result,
        legal_refs = legal_refs,
        territory  = territory,
    )

    ci         = coh["confianza_implementacion"]
    ci_label   = coh["confianza_label"]
    esperado   = caso["resultado_esperado"]
    en_rango   = _in_range(ci, esperado["ci_range"])
    desviacion = ci - sum(esperado["ci_range"]) / 2   # delta vs midpoint

    dimensiones_resumen = {
        d["dimension"]: {"score": d["score"], "nivel": d["nivel"]}
        for d in coh["dimensiones"]
    }

    return {
        "caso_id":            caso["caso_id"],
        "nombre":             caso["nombre"],
        "categoria":          caso["categoria"],
        "tipo_real":          caso["tipo_real"],
        "ci_calculado":       ci,
        "ci_label":           ci_label,
        "ci_rango_esperado":  esperado["ci_range"],
        "en_rango":           en_rango,
        "desviacion_midpoint": round(desviacion, 1),
        "dimensiones":        dimensiones_resumen,
        "issues_count":       coh["total_issues"],
        "recomendaciones":    coh["recomendaciones"],
        "legal_refs_count":   len(legal_refs),
        "legal_refs":         [f"{r['law']} {r['article']}" for r in legal_refs],
        "notas_calibracion":  caso.get("notas_calibracion", ""),
        "riesgo_principal":   caso.get("riesgo_principal", ""),
    }


def _print_header():
    print(f"\n{BOLD}{'='*72}{RESET}")
    print(f"{BOLD}  QUIRA OS · Stress Test Runner · Banco de Casos v1{RESET}")
    print(f"  Motor de Coherencia v1.0 · ICGI-T Q1-2026: 53.56")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{BOLD}{'='*72}{RESET}\n")


def _print_caso_result(r: dict, idx: int):
    ok      = "✓" if r["en_rango"] else "✗"
    color   = GREEN if r["en_rango"] else RED
    ci_col  = _ci_color(r["ci_calculado"])
    dev_str = f"{r['desviacion_midpoint']:+.1f}"

    print(f"{BOLD}[{idx:02d}] {r['caso_id']} · {r['nombre'][:50]}{RESET}")
    print(f"     CI Calculado: {ci_col}{BOLD}{r['ci_calculado']}%{RESET}"
          f"  |  Rango esperado: [{r['ci_rango_esperado'][0]}-{r['ci_rango_esperado'][1]}%]"
          f"  |  {color}{ok} desv={dev_str}{RESET}")

    for dim_name, dim_data in r["dimensiones"].items():
        nivel_sym = {"Alta": "▲", "Media": "◆", "Baja": "▼", "Insuficiente": "✗"}.get(dim_data["nivel"], "?")
        print(f"     {nivel_sym} {dim_name:<25} {dim_data['score']:3d}  ({dim_data['nivel']})")

    if r["legal_refs"]:
        print(f"     📋 Legal refs: {', '.join(r['legal_refs'])}")
    else:
        print(f"     {YELLOW}⚠ Sin referencias legales activas{RESET}")

    if r["recomendaciones"]:
        for rec in r["recomendaciones"][:2]:
            print(f"     → {rec[:80]}")

    print()


def _print_summary(resultados: list[dict]):
    en_rango   = sum(1 for r in resultados if r["en_rango"])
    total      = len(resultados)
    pct        = round(en_rango / total * 100)
    desv_media = round(sum(abs(r["desviacion_midpoint"]) for r in resultados) / total, 1)

    print(f"{BOLD}{'─'*72}{RESET}")
    print(f"{BOLD}  CALIBRACIÓN GLOBAL{RESET}")
    print(f"{'─'*72}")
    print(f"  Casos en rango esperado:   {GREEN if en_rango==total else YELLOW}{en_rango}/{total} ({pct}%){RESET}")
    print(f"  Desviación media (|Δ|):    {desv_media} pts vs midpoint del rango")
    print()

    # Casos fuera de rango
    fuera = [r for r in resultados if not r["en_rango"]]
    if fuera:
        print(f"  {RED}Casos que necesitan calibración:{RESET}")
        for r in fuera:
            direction = "ALTO" if r["desviacion_midpoint"] > 0 else "BAJO"
            print(f"  · {r['caso_id']}: CI={r['ci_calculado']}% "
                  f"({direction} {abs(r['desviacion_midpoint']):.0f} pts del midpoint)")
    else:
        print(f"  {GREEN}✓ Todos los casos dentro del rango esperado — motor calibrado.{RESET}")

    print(f"\n  Artefacto guardado: {RESULTADOS_PATH.relative_to(ROOT)}")
    print(f"{BOLD}{'='*72}{RESET}\n")


def main():
    _print_header()

    # Cargar datos y casos
    data  = load_all()
    banco = json.loads(CASOS_PATH.read_text(encoding="utf-8"))
    casos = banco["casos"]

    resultados = []
    for i, caso in enumerate(casos, 1):
        print(f"  Procesando {caso['caso_id']}... ", end="", flush=True)
        try:
            r = _run_caso(caso, data)
            resultados.append(r)
            status = f"{GREEN}OK{RESET}" if r["en_rango"] else f"{RED}FUERA{RESET}"
            print(f"{status} (CI={r['ci_calculado']}%)")
        except Exception as e:
            print(f"{RED}ERROR: {e}{RESET}")
            resultados.append({
                "caso_id": caso["caso_id"],
                "error":   str(e),
                "en_rango": False,
            })

    print()
    for i, r in enumerate(resultados, 1):
        if "error" in r:
            print(f"{RED}[{i:02d}] {r['caso_id']} — ERROR: {r['error']}{RESET}\n")
        else:
            _print_caso_result(r, i)

    _print_summary(resultados)

    # Guardar artefacto JSON para el tester
    artefacto = {
        "meta": {
            "version":      "v1.0",
            "fecha":        datetime.now().isoformat(),
            "icgit_q1":     53.56,
            "total_casos":  len(casos),
            "en_rango":     sum(1 for r in resultados if r.get("en_rango")),
        },
        "resultados": resultados,
    }
    RESULTADOS_PATH.write_text(
        json.dumps(artefacto, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()
