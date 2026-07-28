# -*- coding: utf-8 -*-
"""
scripts/d08/cruzar_demandas.py — Fase 2 · Trazabilidad Biográfica de la demanda
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: MARCO-TEORICO-001
  constitution_articles: [1, 2, 3, 9]
  type: TECNICA

Implementa el POSTULADO I (Trazabilidad Biográfica del Dato) sobre las demandas
ciudadanas: reconstruye la historia de vida de cada demanda a través de la cadena

    demanda ciudadana → POA → PAC → presupuesto → ejecución

★ HORIZONTE DE VERDAD (marco_teorico · concepto 6) — TODO resultado declara su
  estado epistémico. Ésta es la frontera obligatoria de la Fase 2:

  · `confirmado`  → HECHO OBSERVABLE: existe la demanda · existe el proyecto ·
                    hay coincidencia semántica medible. QUIRA lo certifica.
  · `hipotesis`   → INFERENCIA ANALÍTICA: "esta demanda fue atendida". QUIRA la
                    PROPONE; el humano la valida (Constitución Art. 3).
  · `sin_correlato` → no se halló proyecto asociable en la evidencia disponible.
                    NO significa "no se atendió": significa que el expediente no
                    lo acredita (Principio de No-Inferencia).

NUNCA se afirma "la demanda fue satisfecha" como hecho. La prohibición de
alucinación es arquitectónica, no operacional.

MOTOR: embeddings locales (mismo modelo del corpus), SIN API y sin costo. Se reusa
la TÉCNICA de d09, no sus datos — la frontera d08/d09 es sobre el ORIGEN de los
aportes (DEC-0004), no sobre el método de cruce.

Uso:  python scripts/d08/cruzar_demandas.py [--anio 2025]
Salida: data/d08/trazabilidad_demandas.json
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import sys
import tomllib
from collections import Counter
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts" / "normativa"))
sys.path.insert(0, str(REPO / "scripts"))

DEMANDAS = REPO / "data" / "d08" / "demandas_ciudadanas.json"
SALIDA = REPO / "data" / "d08" / "trazabilidad_demandas.json"

# Umbrales calibrados y ya validados por Javo en el cruce de d09 (METODOLOGIA_TRAZABILIDAD_APORTES)
TH_FUERTE = 0.62      # candidato fuerte → hipótesis de correspondencia
TH_REVISAR = 0.52     # banda de validación experta obligatoria


def cargar_poa(anios: tuple[str, ...]) -> list[dict]:
    """Lee los proyectos POA del corpus verificado (Supabase). HECHO OBSERVABLE."""
    uri = tomllib.load(open(REPO / ".streamlit" / "secrets.toml", "rb"))["database"]["supabase_uri"]
    import psycopg2
    cur = psycopg2.connect(uri, connect_timeout=30).cursor()
    siglas = tuple(f"POA-GAD-{a}%" for a in anios)
    cur.execute("""SELECT norma_sigla, left(sha256,12), contenido
                   FROM public.normativa_corpus
                   WHERE norma_sigla LIKE ANY(%s) AND palabras > 8
                   ORDER BY norma_sigla, chunk_seq""", (list(siglas),))
    out = [{"fuente": s, "sha": h, "texto": " ".join(str(t).split())[:400]}
           for s, h, t in cur.fetchall()]
    cur.connection.close()
    return out


def main() -> int:
    if not DEMANDAS.exists():
        print("ERROR: falta data/d08/demandas_ciudadanas.json — ejecutar extraer_demandas.py")
        return 1
    d = json.loads(DEMANDAS.read_text(encoding="utf-8"))
    demandas = d["demandas"]
    print(f"=== FASE 2 · Trazabilidad Biográfica de {len(demandas)} demandas ===\n")

    poa = cargar_poa(("2025", "2026"))
    print(f"  POA cargado del corpus verificado: {len(poa)} registros")
    if not poa:
        print("  ERROR: sin POA — no se puede cruzar")
        return 1

    import numpy as np
    import ingest as ing
    model = ing._get_model()
    print("  modelo de embeddings local cargado (sin API)\n")

    def emb(txts):
        v = model.encode(txts, convert_to_numpy=True, show_progress_bar=False, batch_size=64)
        return v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-9)

    D = emb([x["demanda"][:300] for x in demandas])
    P = emb([x["texto"] for x in poa])

    resultados = []
    for i, dem in enumerate(demandas):
        sims = D[i] @ P.T
        j = int(sims.argmax())
        score = float(sims[j])

        # ★ ESTADO EPISTÉMICO — la frontera de la Fase 2
        if score >= TH_FUERTE:
            estado, naturaleza = "hipotesis", "INFERENCIA ANALÍTICA — correspondencia propuesta, requiere validación experta"
        elif score >= TH_REVISAR:
            estado, naturaleza = "pendiente_validacion", "banda de revisión — la máquina propone, el analista confirma"
        else:
            estado, naturaleza = "sin_correlato", "no se halló proyecto asociable en la evidencia disponible (NO significa que no se atendió)"

        resultados.append({
            # HECHOS OBSERVABLES (confirmados)
            "demanda": dem["demanda"][:220],
            "mecanismo": dem["mecanismo"],
            "naturaleza_juridica": dem["naturaleza_juridica"],
            "anio_demanda": dem["anio"],
            "fuente_demanda": dem["fuente"],
            "similitud": round(score, 3),
            "proyecto_poa_mas_proximo": poa[j]["texto"][:200] if score >= TH_REVISAR else "",
            "fuente_poa": poa[j]["fuente"] if score >= TH_REVISAR else "",
            "sha_poa": poa[j]["sha"] if score >= TH_REVISAR else "",
            # INFERENCIA (declarada como tal)
            "estado_epistemico": estado,
            "naturaleza_del_juicio": naturaleza,
        })

    est = Counter(r["estado_epistemico"] for r in resultados)
    vinc = [r for r in resultados if r["naturaleza_juridica"] == "vinculante"]
    est_vinc = Counter(r["estado_epistemico"] for r in vinc)

    salida = {
        "_fuente": "GENERADO por scripts/d08/cruzar_demandas.py — Fase 2",
        "_postulado": "I · Trazabilidad Biográfica del Dato (marco_teorico/MARCO_TEORICO_QUIRA.md)",
        "_horizonte_de_verdad": {
            "confirmado": "hechos observables: la demanda existe, el proyecto existe, hay similitud medible",
            "hipotesis": "INFERENCIA: correspondencia propuesta por la máquina — requiere validación experta",
            "pendiente_validacion": "banda de revisión obligatoria (0.52-0.62)",
            "sin_correlato": "el expediente no acredita correspondencia — NO afirma que no se atendió",
        },
        "_advertencia": "QUIRA NUNCA afirma 'la demanda fue satisfecha' como hecho. Propone; el humano valida (Constitución Art. 3).",
        "generado": date.today().isoformat(),
        "umbrales": {"fuerte": TH_FUERTE, "revisar": TH_REVISAR},
        "total_demandas": len(resultados),
        "registros_poa_contrastados": len(poa),
        "por_estado_epistemico": dict(est),
        "vinculantes_por_estado": dict(est_vinc),
        "trazabilidad": resultados,
    }
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  {'ESTADO EPISTÉMICO':<24} {'TODAS':>7}   {'VINCULANTES (COOTAD 238)':>26}")
    for e in ("hipotesis", "pendiente_validacion", "sin_correlato"):
        print(f"  {e:<24} {est.get(e,0):>7}   {est_vinc.get(e,0):>26}")
    print(f"\nOK — {SALIDA.relative_to(REPO)}")
    print("\n  RECORDATORIO: 'hipotesis' NO es 'atendida'. Requiere validación experta")
    print("  antes de cualquier afirmación pública (Horizonte de Verdad).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
