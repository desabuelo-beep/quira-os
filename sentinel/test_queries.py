"""
SENTINEL RAG · test_queries.py
Las 11 preguntas de validación — Sprint 1.
Sentinel pasa el sprint cuando responde las 11 con al menos score 🟡 Media
y cita fuentes reales del vault.
Ejecutar: python -m sentinel.test_queries
Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import json
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.query_rag import query_retrieval_only, format_retrieval_response

# ── LAS 11 PREGUNTAS DE VALIDACIÓN ────────────────────────────────────────────
# Cubren todos los dominios del vault: TGI, PDOT, parroquias, fondos, normativa.
# La pregunta 11 (Colega 3) es la más exigente — requiere razonamiento cruzado.
PREGUNTAS = [
    # Dominio: TGI / Ejecución
    "¿Por qué D3 ejecución presupuestaria está en rojo?",

    # Dominio: UNESCO / Fondos
    "¿Cuál es la brecha de activación de la Ciudad Creativa UNESCO y qué fondos habilita?",

    # Dominio: Territorio / Equidad
    "¿Qué pasa con Isabel Muentes — cuáles son sus indicadores críticos?",

    # Dominio: Estrategia / TGI
    "¿Cuáles son las palancas más efectivas para cerrar el TGI en los próximos 365 días?",

    # Dominio: Parroquias / IRS
    "¿Qué significa el IRS=79.7 y por qué es un problema de equidad territorial?",

    # Dominio: PDOT / Metas
    "¿Qué metas del PDyOT 2023-2027 están en riesgo de no cumplirse al 2027?",

    # Dominio: ICPI / Planificación
    "¿Cómo se calcula el ICPI y qué explica la brecha de 30pp con el ICM del SNP?",

    # Dominio: Fondos / Financiamiento
    "¿Qué fuentes de financiamiento internacional aplican para las parroquias rurales de Montecristi?",

    # Dominio: Normativa / COOTAD
    "¿Qué dice el COOTAD sobre las competencias del GAD Municipal en agua potable y saneamiento?",

    # Dominio: D3 / Presupuesto
    "¿Cuánto vale en dólares cada punto porcentual de mejora en D3 ejecución presupuestaria?",

    # Dominio: CRUZADO — la más exigente (Colega 3)
    "¿Qué riesgos legales y financieros enfrenta Montecristi si D3 sigue bajo 60% hasta el cierre del mandato?",
]

# Criterios mínimos de éxito por pregunta
CRITERIOS = {
    "score_minimo":      0.35,    # score promedio de chunks recuperados
    "chunks_minimos":    2,       # al menos 2 chunks relevantes
    "fuentes_distintas": 1,       # al menos 1 nota distinta
}


def evaluar_respuesta(resp, pregunta_idx: int) -> dict:
    """Evalúa una SentinelResponse contra los criterios mínimos."""
    if not resp.chunks:
        return {"pasa": False, "razon": "Sin chunks recuperados", "score_avg": 0.0}

    score_avg = sum(c.score for c in resp.chunks) / len(resp.chunks)
    fuentes   = len({c.nota for c in resp.chunks})
    n_chunks  = len(resp.chunks)

    pasa = (
        score_avg >= CRITERIOS["score_minimo"] and
        n_chunks  >= CRITERIOS["chunks_minimos"] and
        fuentes   >= CRITERIOS["fuentes_distintas"]
    )

    return {
        "pasa":       pasa,
        "score_avg":  round(score_avg, 3),
        "n_chunks":   n_chunks,
        "fuentes":    fuentes,
        "confianza":  resp.confianza,
        "razon":      "OK" if pasa else f"score={score_avg:.2f}, chunks={n_chunks}, fuentes={fuentes}",
    }


def run_tests(verbose: bool = True) -> dict:
    """Ejecuta las 11 preguntas y retorna el informe."""
    print(f"\n{'═'*65}")
    print("  SENTINEL RAG · SUITE DE VALIDACIÓN — 11 PREGUNTAS")
    print("  Sprint 1 — Modo: RETRIEVAL ONLY (sin LLM)")
    print(f"{'═'*65}\n")

    resultados = []
    pasadas = 0

    for i, pregunta in enumerate(PREGUNTAS, 1):
        print(f"  [{i:02d}/11] {pregunta[:70]}...")
        t0 = time.time()

        resp = query_retrieval_only(pregunta)
        eval_r = evaluar_respuesta(resp, i)
        elapsed = round(time.time() - t0, 2)

        estado = "✅" if eval_r["pasa"] else "❌"
        if eval_r["pasa"]:
            pasadas += 1

        print(f"         {estado} {eval_r['confianza']}  "
              f"chunks={eval_r['n_chunks']}  "
              f"fuentes={eval_r['fuentes']}  "
              f"score={eval_r['score_avg']}  "
              f"{elapsed}s")

        if verbose and resp.chunks:
            for c in resp.chunks[:2]:
                print(f"           → {c.nota} · '{c.section}' ({c.score})")
        print()

        resultados.append({
            "idx":      i,
            "pregunta": pregunta,
            "elapsed":  elapsed,
            **eval_r,
            "chunks_detail": [
                {"nota": c.nota, "section": c.section, "score": c.score}
                for c in resp.chunks
            ],
        })

    # Resumen
    total = len(PREGUNTAS)
    pct   = pasadas / total * 100

    print(f"{'─'*65}")
    print(f"  RESULTADO: {pasadas}/{total} preguntas pasadas ({pct:.0f}%)")

    if pct >= 90:
        print("  🟢 SPRINT 1 COMPLETO — vault listo para integrar LLM")
    elif pct >= 60:
        print("  🟡 PARCIAL — revisar notas con score bajo antes de LLM")
    else:
        print("  🔴 REQUIERE WORK — normalizar YAML del vault (Sprint 0)")

    print(f"{'═'*65}\n")

    # Guardar reporte
    report = {
        "timestamp":    datetime.now().isoformat(),
        "total":        total,
        "pasadas":      pasadas,
        "porcentaje":   pct,
        "criterios":    CRITERIOS,
        "resultados":   resultados,
    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"test_queries_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  Reporte guardado: {report_path}")

    return report


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--quiet", action="store_true", help="Sin detalle de chunks")
    args = p.parse_args()
    run_tests(verbose=not args.quiet)
