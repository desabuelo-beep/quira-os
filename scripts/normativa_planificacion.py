# -*- coding: utf-8 -*-
"""
scripts/normativa_planificacion.py — Cable Normativo del MCD Planificación (Supabase)
═══════════════════════════════════════════════════════════════════════════════════
ADR-031 capacidad NORMATIVA · ADR-005 (Supabase = memoria documental verificable · pgvector).
"Cablear lo que existe": el corpus YA está poblado (normativa_corpus · 12,992 chunks). Este
cable NO ingiere nada — LEE la base legal del plan del corpus y la escribe al snapshot
(planificacion.base_normativa); el cajón la lee de ahí (Regla 1). Fallback elegante.

Verdad: el texto normativo viene del corpus verificado (sha256), no se inventa (Regla 3).
Uso:  python scripts/normativa_planificacion.py
Dylus Lab © 2026
"""
import json
import sys
import tomllib
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
SECRETS = REPO / ".streamlit" / "secrets.toml"

# Normas fundacionales del ciclo de planificación municipal (foco del dominio)
NORMAS_PLAN = ["CE", "COOTAD", "PDOT-MONTECRISTI", "PND-2025", "RLOSNCP"]
_NOMBRE = {"CE": "Constitución del Ecuador", "COOTAD": "Código Orgánico de Organización Territorial (COOTAD)",
           "PDOT-MONTECRISTI": "Plan de Desarrollo y Ordenamiento Territorial (PDOT)",
           "PND-2025": "Plan Nacional de Desarrollo", "RLOSNCP": "Reglamento a la Ley de Contratación Pública"}


def _uri() -> str:
    try:
        return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]
    except Exception:
        return ""


def main() -> int:
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    plan = snap.get("planificacion", {})
    if not plan:
        print("[ERR] sin bloque 'planificacion'"); return 1
    uri = _uri()
    if not uri:
        print("[skip] sin supabase_uri en secrets — el cajón omite la base normativa"); return 0
    try:
        import psycopg2
        conn = psycopg2.connect(uri, connect_timeout=20)
        cur = conn.cursor()

        # 1 · Cobertura: cuánto respaldo normativo verificado hay por norma fundacional
        cur.execute(
            "SELECT norma_sigla, count(*) FROM public.normativa_corpus "
            "WHERE norma_sigla = ANY(%s) GROUP BY norma_sigla", (NORMAS_PLAN,))
        cov = {r[0]: r[1] for r in cur.fetchall()}
        cobertura = [{"sigla": s, "nombre": _NOMBRE.get(s, s), "chunks": cov.get(s, 0)}
                     for s in NORMAS_PLAN if cov.get(s)]

        # 2 · Artículo ancla: la obligación COOTAD de planificar (verbatim del corpus · sha256)
        cur.execute(
            "SELECT articulo_num, sha256, contenido FROM public.normativa_corpus "
            "WHERE norma_sigla = 'COOTAD' AND contenido ILIKE %s "
            "ORDER BY length(contenido) DESC LIMIT 1", ("%plan de desarrollo y de ordenamiento territorial%",))
        row = cur.fetchone()
        ancla = None
        if row:
            ancla = {"norma": "COOTAD", "articulo": row[0], "sha256": (row[1] or "")[:12],
                     "texto": (row[2] or "").strip()[:420]}

        conn.close()
    except Exception as e:
        print(f"[skip] Supabase no disponible ({str(e)[:70]}) — el cajón omite la base normativa"); return 0

    total = sum(c["chunks"] for c in cobertura)
    plan["base_normativa"] = {
        "fuente": "Corpus normativo verificado (Supabase · pgvector · sha256)",
        "fecha": date.today().isoformat(),
        "total_chunks": total,
        "cobertura": cobertura,
        "articulo_ancla": ancla,
    }
    snap["planificacion"] = plan
    SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — base normativa escrita: {len(cobertura)} normas · {total} chunks verificados.")
    for c in cobertura:
        print(f"  {c['sigla']:<18} {c['chunks']:>5}  {c['nombre']}")
    if ancla:
        print(f"\n  Ancla COOTAD art.{ancla['articulo']} (sha {ancla['sha256']}): {ancla['texto'][:100]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
