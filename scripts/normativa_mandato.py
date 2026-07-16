# -*- coding: utf-8 -*-
"""
scripts/normativa_mandato.py — Cable Normativo del DOM d03 · Gobernanza del Mandato Electoral
═══════════════════════════════════════════════════════════════════════════════════
ADR-031 capacidad NORMATIVA · ADR-005 (Supabase = memoria documental verificable · pgvector).
Réplica exacta del molde de `normativa_planificacion.py` (d01): este cable NO ingiere nada —
LEE la base legal del mandato del corpus verificado y la escribe al snapshot
(mandato_dom.base_normativa); el cajón la lee de ahí vía `_ley_esl` (Regla 1).

Verdad: el texto normativo viene del corpus verificado (sha256), NO SE INVENTA (Regla 3).
  Lección 2026-07-16: la primera versión del marco legal de d03 hardcodeaba los artículos en
  el render. Eso violaba la Regla 9 (el dato nace en el canon, no en Python) y la Regla 3 (sin
  sha256 no hay norma). Este cable lo corrige: si el corpus no tiene el artículo, no se cita.

LA CADENA DEL MANDATO (marco aportado por Javo · 2026-07-16):
  Código de la Democracia Art. 97 → inscribe el Plan de Trabajo ante el CNE
  COOTAD Art. 58-60                → gana y toma posesión
  COPLAFIP Art. 34, 41-42          → DEBE traducir ese Plan al PDOT  ← lo que d03 verifica
  LOPC Art. 89-90                  → rinde cuentas anualmente sobre ese Plan
  Constitución Art. 105            → si incumple, el electorado puede revocarlo

Uso:  python scripts/normativa_mandato.py
Dylus Lab © 2026
"""
import json
import re as _re
import sys
import tomllib
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SNAP = REPO / "data" / "gm_snapshot.json"
SECRETS = REPO / ".streamlit" / "secrets.toml"

# Normas fundacionales del ciclo del mandato electoral (foco del dominio)
NORMAS_MANDATO = ["CE", "COD", "COPLAFIP", "LOPC", "COOTAD"]
_NOMBRE = {"CE": "Constitución del Ecuador", "COD": "Código de la Democracia",
           "COPLAFIP": "Código Orgánico de Planificación y Finanzas Públicas",
           "LOPC": "Ley Orgánica de Participación Ciudadana",
           "COOTAD": "Código Orgánico de Organización Territorial (COOTAD)"}

# Artículo ancla por eslabón: la disposición que sostiene cada fase (verbatim · sha256)
ESLABONES = {
    "compromiso":  [("COD", "97", None), ("COD", None, "%plan de trabajo%")],
    "investidura": [("COOTAD", "60", None), ("COOTAD", "58", None)],
    "traduccion":  [("COPLAFIP", "34", None), ("COPLAFIP", "41", None),
                    ("COPLAFIP", None, "%plan de desarrollo%")],
    "rendicion":   [("LOPC", "89", None), ("LOPC", None, "%rendición de cuentas%")],
    "consecuencia": [("CE", "105", None), ("LOPC", "25", None)],
}

# Marco AMPLIADO por eslabón — SELECTIVO (colega · 2026-07-16): solo la cadena que sostiene el
# índice. Fuera elegibilidad, edad mínima, prohibiciones y cómputo de votos: este dominio no
# trata de candidatura, trata de la TRANSFORMACIÓN JURÍDICA del Plan de Trabajo.
MARCO = {
    "compromiso":   [("COD", ["97"])],
    "investidura":  [("COOTAD", ["58", "59", "60"])],
    "traduccion":   [("COPLAFIP", ["12", "34", "41", "42", "44", "101", "103"])],
    "rendicion":    [("CE", ["100"]), ("LOPC", ["89", "90"])],
    "consecuencia": [("CE", ["105"]), ("LOPC", ["25"])],
}
_DISP = {"CE": "CE", "COD": "Cód. Democracia", "COPLAFIP": "COPLAFIP", "LOPC": "LOPC", "COOTAD": "COOTAD"}


def _uri() -> str:
    try:
        return tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]
    except Exception:
        return ""


def _compress(nums) -> str:
    ns = sorted({int(n) for n in nums})
    out, i = [], 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        out.append(str(ns[i]) if i == j else f"{ns[i]}-{ns[j]}")
        i = j + 1
    return ", ".join(out)


def main() -> int:
    snap = json.loads(SNAP.read_text(encoding="utf-8"))
    dom = snap.get("mandato_dom", {})
    if not dom:
        print("[ERR] sin bloque 'mandato_dom'")
        return 1
    uri = _uri()
    if not uri:
        print("[skip] sin supabase_uri en secrets — el cajón omite la base normativa")
        return 0
    try:
        import psycopg2
        conn = psycopg2.connect(uri, connect_timeout=20)
        cur = conn.cursor()

        # 1 · Cobertura verificada por norma fundacional
        cur.execute("SELECT norma_sigla, count(*) FROM public.normativa_corpus "
                    "WHERE norma_sigla = ANY(%s) GROUP BY norma_sigla", (NORMAS_MANDATO,))
        cov = {r[0]: r[1] for r in cur.fetchall()}
        cobertura = [{"sigla": s, "nombre": _NOMBRE.get(s, s), "chunks": cov.get(s, 0)}
                     for s in NORMAS_MANDATO if cov.get(s)]

        # 2 · Artículo ancla del dominio: la obligación de traducir el plan de campaña al PDOT
        cur.execute("SELECT articulo_num, sha256, contenido FROM public.normativa_corpus "
                    "WHERE norma_sigla='COPLAFIP' AND contenido ILIKE %s "
                    "ORDER BY length(contenido) DESC LIMIT 1", ("%plan de desarrollo%",))
        row = cur.fetchone()
        ancla = None
        if row:
            ancla = {"norma": "COPLAFIP", "articulo": row[0], "sha256": (row[1] or "")[:12],
                     "texto": (row[2] or "").strip()[:420]}

        def _fetch(sigla, num, kw):
            if num:
                cur.execute("SELECT articulo_num, sha256, contenido FROM public.normativa_corpus "
                            "WHERE norma_sigla=%s AND articulo_num=%s LIMIT 1", (sigla, num))
            else:
                cur.execute("SELECT articulo_num, sha256, contenido FROM public.normativa_corpus "
                            "WHERE norma_sigla=%s AND contenido ILIKE %s ORDER BY length(contenido) DESC LIMIT 1",
                            (sigla, kw))
            r = cur.fetchone()
            if not r or "derogado" in (r[2] or "")[:90].lower():
                return None
            cont = (r[2] or "").strip()
            m = _re.match(r"Art\.\s*[\d.]+\.-\s*([^.\-]{3,72})", cont)
            return {"norma": sigla, "articulo": r[0], "sha256": (r[1] or "")[:12],
                    "sumilla": (m.group(1).strip() if m else "")}

        por_eslabon = {}
        for k, cands in ESLABONES.items():
            for sigla, num, kw in cands:
                got = _fetch(sigla, num, kw)
                if got:
                    por_eslabon[k] = got
                    break

        # 3 · Marco ampliado — solo se cita lo que el corpus TIENE (Regla 3)
        for k, leyes in MARCO.items():
            parts = []
            for sigla, nums in leyes:
                cur.execute("SELECT DISTINCT articulo_num FROM public.normativa_corpus "
                            "WHERE norma_sigla=%s", (sigla,))
                have = {str(r[0]).strip() for r in cur.fetchall() if r[0] is not None}
                ok = [n for n in nums if n in have]
                if ok:
                    parts.append(f"{_DISP.get(sigla, sigla)} Art. {_compress(ok)}")
            if parts:
                por_eslabon.setdefault(k, {})["marco"] = parts

        conn.close()
    except Exception as e:
        print(f"[skip] Supabase no disponible ({str(e)[:70]}) — el cajón omite la base normativa")
        return 0

    total = sum(c["chunks"] for c in cobertura)
    dom["base_normativa"] = {
        "fuente": "Corpus normativo verificado (Supabase · pgvector · sha256)",
        "fecha": date.today().isoformat(),
        "total_chunks": total,
        "cobertura": cobertura,
        "articulo_ancla": ancla,
        "por_eslabon": por_eslabon,
    }
    snap["mandato_dom"] = dom
    SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK — base normativa del mandato: {len(cobertura)} normas · {total} chunks verificados.")
    for c in cobertura:
        print(f"   {c['sigla']:10} {c['chunks']:5,} chunks · {c['nombre']}")
    print("   eslabones:")
    for k, v in por_eslabon.items():
        print(f"     {k:13} {v.get('norma','?')} Art. {v.get('articulo','?')} "
              f"(sha {v.get('sha256','—')}) · marco: {' · '.join(v.get('marco', [])) or '—'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
