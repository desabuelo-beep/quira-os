# -*- coding: utf-8 -*-
"""
Motor Narrativo de QUIRA — Etapa 6 · CRUCE DE 5 CAPAS
Dylus Lab © 2026 · doctrina: MOTOR_NARRATIVO_QUIRA.md §1 (asesor 2026-07-04).

El diferenciador REAL no es "discurso vs. evidencia": es la COHERENCIA entre las
capas de la realidad pública. Cada unidad narrativa del discurso se contrasta con:
  · PROMESA        — plan de gobierno (CNE) + PDOT   (corpus Supabase)
  · PLANIFICACIÓN  — POA del período                 (extract_poa)
  · EJECUCIÓN      — monto/actividad del POA ejecutado
(Presupuesto y Territorio quedan para la extensión con eSIGEF y geo.)

De ahí emergen las RELACIONES (asesor §5):
  · coherente          — se dijo, se prometió y se planificó/ejecutó
  · obra_sin_promesa    — está en el plan/ejecución pero no se prometió
  · promesa_sin_ejecucion — se prometió pero no hay correlato en el plan
  · solo_narrativa      — se dijo, sin correlato en ninguna capa (posible relleno)

Reusa el motor semántico local (embeddings) + corpus + POA. Salida: cruce.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))                 # scripts/
sys.path.insert(0, str(_HERE.parent / "normativa"))   # ingest
import identidad as _id
import ingest as _ing
from extract_poa_pdf import extract_poa

TH = 0.45                       # umbral de correlato (semiautomático, como aportes)
POA_AÑOS = (2024, 2025, 2026)
PROMESA_SIGLAS = ("PLAN-GOB-MCR", "PDOT-MONTECRISTI")   # plan de campaña + PDOT


def _embed(model, txts):
    v = model.encode(txts, convert_to_numpy=True, show_progress_bar=False, batch_size=64)
    return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)


def _promesa_corpus(conn):
    """Chunks del plan de gobierno + PDOT (la capa PROMESA)."""
    c = conn.cursor()
    c.execute("SELECT norma_sigla, contenido FROM normativa_corpus")
    def g(r, k, i):
        try: return r[k]
        except Exception: return r[i]
    out = []
    for row in c.fetchall():
        sig = g(row, "norma_sigla", 0)
        if sig in PROMESA_SIGLAS:
            out.append(" ".join(str(g(row, "contenido", 1)).split()))
    return out


def _clasificar(promesa: bool, plan: bool) -> str:
    if promesa and plan:
        return "coherente"
    if plan and not promesa:
        return "obra_sin_promesa"
    if promesa and not plan:
        return "promesa_sin_ejecucion"
    return "solo_narrativa"


def cruzar(video_id: str) -> dict:
    d = _id.BASE / video_id
    unidades = json.loads((d / "unidades.json").read_text(encoding="utf-8"))["unidades"]
    textos = [u.get("texto", "") for u in unidades]

    model = _ing._get_model()
    U = _embed(model, textos)

    # capa PLANIFICACIÓN/EJECUCIÓN — POA
    poa = {y: extract_poa(str(y)) for y in POA_AÑOS}
    P = {y: _embed(model, [p["desc"] for p in poa[y]]) for y in poa if poa[y]}

    # capa PROMESA — corpus
    conn = _ing.get_connection()
    prom_txt = _promesa_corpus(conn)
    conn.close()
    PR = _embed(model, prom_txt) if prom_txt else None

    detalle = []
    for i, u in enumerate(unidades):
        # plan/ejecución
        best_plan, plan_ev, plan_y, plan_monto = 0.0, "", None, 0.0
        for y in P:
            s = U[i] @ P[y].T
            j = int(s.argmax())
            if float(s[j]) > best_plan:
                best_plan = float(s[j]); plan_ev = poa[y][j]["desc"]; plan_y = y
                plan_monto = poa[y][j].get("monto", 0.0)
        # promesa
        best_prom = float((U[i] @ PR.T).max()) if PR is not None else 0.0

        plan_ok = best_plan >= TH
        prom_ok = best_prom >= TH
        detalle.append({
            "t": u.get("t"), "texto": u.get("texto"), "tipo": u.get("tipo"), "eje": u.get("eje"),
            "relacion": _clasificar(prom_ok, plan_ok),
            "promesa": {"correlato": prom_ok, "score": round(best_prom, 3)},
            "plan": {"correlato": plan_ok, "score": round(best_plan, 3),
                      "evidencia": plan_ev[:110] if plan_ok else "", "anio": plan_y if plan_ok else None,
                      "monto": round(plan_monto, 2) if plan_ok else 0.0},
        })

    from collections import Counter
    rel = Counter(x["relacion"] for x in detalle)
    out = {"video_id": video_id, "n_unidades": len(detalle), "umbral": TH,
           "por_relacion": dict(rel), "detalle": detalle}
    (d / "cruce.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    vid = _id._video_id(_id.PILOTO[año]["url"])
    res = cruzar(vid)
    print(f"CRUCE 5 CAPAS · {año}: {res['n_unidades']} unidades")
    for k, v in res["por_relacion"].items():
        print(f"   {v:3d}  {k}")
    print("\n  ejemplos:")
    for x in res["detalle"][:8]:
        print(f"   [{x['relacion']}] «{(x['texto'] or '')[:44]}» plan={x['plan']['score']} prom={x['promesa']['score']}")
