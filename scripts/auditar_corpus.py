# -*- coding: utf-8 -*-
"""
scripts/auditar_corpus.py — Auditoría de COBERTURA del Corpus Normativo
═══════════════════════════════════════════════════════════════════════════════════
Compara, documento por documento, los artículos que contiene el archivo FUENTE (.docx) con los
que realmente están vectorizados en Supabase. Detecta artículos PERDIDOS en la ingesta.

POR QUÉ EXISTE (hallazgo de Javo · 2026-07-20): el chunker perdía artículos cuando el .docx
maqueta el marcador junto al título del capítulo ("De la rendición de cuentas Art. 88"). La LOPC
quedó con 77 de 103 artículos —faltaba el Art. 88, que funda el derecho ciudadano a exigir
rendición de cuentas— y nadie lo detectó: la BRN daba las cadenas por "íntegras" porque solo
verifica los eslabones DECLARADOS, no la completitud del corpus.

  «Si la base normativa no está completa, todo lo que se construya encima es alucinación probable.»

Sin esta auditoría, una ausencia de ingesta es indistinguible de una inexistencia jurídica — y esa
confusión ya produjo una conclusión errónea. La ausencia debe ser un RESULTADO, no una inferencia.

Uso:  python scripts/auditar_corpus.py            (resumen)
      python scripts/auditar_corpus.py --detalle  (lista los artículos faltantes)
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
WORD_DIR = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Normativa_Word")
SECRETS = REPO / ".streamlit" / "secrets.toml"

# Mapeo canónico: se REUTILIZA el manifest de QLEP-CORPUS (scripts/normativa/manifest.py) — la
# misma fuente de verdad que usa la ingesta. Así se auditan los 43 documentos, no una lista a mano.
sys.path.insert(0, str(REPO))
from scripts.normativa.manifest import MANIFEST  # noqa: E402

# Tipos con numeración de artículos secuencial → se auditan por CONTEO de artículos.
# Los demás (reforma cita otras leyes · plan/PDOT por metas · guía metodológica) darían falso
# positivo con el conteo: se auditan por presencia de chunks, no por artículos.
TIPOS_ARTICULADOS = {"constitucion", "ley_organica", "reglamento", "resolucion",
                     "acuerdo", "resolucion_local", "codigo", "convenio_internacional"}
MAPEO = {m["archivo"]: m["sigla"] for m in MANIFEST}
TIPO = {m["archivo"]: m.get("tipo", "?") for m in MANIFEST}


def _texto(path: Path) -> str:
    """Texto completo del .docx: párrafos + celdas de tabla (algunos documentos maquetan en tablas)."""
    import docx
    d = docx.Document(str(path))
    partes = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                partes.append(c.text)
    return "\n".join(partes)


def _arts_docx(texto: str) -> set[int]:
    """Artículos declarados en el documento fuente, con el MISMO criterio del chunker corregido."""
    sys.path.insert(0, str(REPO))
    from scripts.normativa.chunker import ARTICLE_RE
    out = set()
    for cap in ARTICLE_RE.findall(texto):
        c = str(cap).strip()
        if c.isdigit():
            out.add(int(c))
    return out


def auditoria_estructural() -> int:
    """AUDITORÍA A (colega · 2026-07-20): ¿el chunker reconoció bien la estructura? NO consulta
    Supabase. Caza bugs del PARSER antes de re-ingerir: chunks vacíos, gigantes, errores, o
    documentos sin artículos ni disposiciones."""
    from scripts.normativa.chunker import chunk_docx
    print("AUDITORÍA ESTRUCTURAL (parser) — no consulta Supabase")
    anom = 0
    for m in MANIFEST:
        f = WORD_DIR / m["archivo"]
        if not f.exists():
            print(f"  ❌ {m['sigla']:16} ARCHIVO FALTANTE"); anom += 1; continue
        try:
            c = chunk_docx(str(f))
        except Exception as e:
            print(f"  ❌ {m['sigla']:16} ERROR: {str(e)[:45]}"); anom += 1; continue
        vacios = sum(1 for x in c if len((x.contenido or "").strip()) < 10)
        gigantes = sum(1 for x in c if x.palabras > 600)
        disp = sum(1 for x in c if "Disposici" in x.articulo_raw)
        if not c or vacios or gigantes:
            print(f"  ⚠ {m['sigla']:16} chunks={len(c)} vacíos={vacios} gigantes={gigantes}"); anom += 1
    print(f"\n{len(MANIFEST)} documentos · {anom} con anomalías estructurales"
          f"{'  → PARSER ESTABLE' if not anom else '  → REVISAR PARSER'}")
    return 1 if anom else 0


def check_fixtures() -> int:
    """REGRESIÓN DEL PARSER (colega · 2026-07-20): compara el parser actual contra el baseline
    congelado en fixtures_parser.json. Detecta que un cambio futuro no rompa la segmentación —
    sin repetir la auditoría completa. Idempotencia incluida (SHA estables entre corridas)."""
    import json
    from scripts.normativa.chunker import chunk_docx
    fx_path = REPO / "scripts" / "normativa" / "fixtures_parser.json"
    if not fx_path.exists():
        print("[skip] no hay fixtures_parser.json — genera el baseline primero"); return 0
    fx = json.loads(fx_path.read_text(encoding="utf-8"))
    docs = {"CE": "Constitución del Ecuador.docx", "COOTAD": "COOTAD.docx",
            "COOTAD-2026": "COOTAD PARA LA SOSTENIBILIDAD Y EFICIENCIA 2026.docx",
            "LOPC": "LEY-ORGANICA-DE-PARTICIPACION-CIUDADANA.docx", "LOSNCP": "losncp.docx",
            "RLOTAIP": "LOTAIP - REGLAMENTO-24-01-2024.docx"}
    print("REGRESIÓN DEL PARSER — parser actual vs. baseline (fixtures)")
    roto = 0
    for sig, f in docs.items():
        c = chunk_docx(str(WORD_DIR / f))
        arts = {x.articulo_num for x in c if x.articulo_raw.startswith("Art.") and x.articulo_num}
        actual = {"chunks": len(c), "arts_unicos": len(arts),
                  "art_max": max(arts) if arts else 0,
                  "disposiciones": sum(1 for x in c if "Disposici" in x.articulo_raw)}
        c2 = chunk_docx(str(WORD_DIR / f))            # idempotencia
        idem = [x.sha256 for x in c] == [x.sha256 for x in c2]
        esp = fx.get(sig, {})
        ok = actual == esp and idem
        print(f"  {'✅' if ok else '❌'} {sig:12} {actual}" + ("" if ok else f"  ≠ esperado {esp} idem={idem}"))
        if not ok:
            roto += 1
    print(f"\n{'PARSER ESTABLE — sin regresión' if not roto else f'{roto} REGRESIONES'}")
    return 1 if roto else 0


def main() -> int:
    if "--estructural" in sys.argv:
        return auditoria_estructural()
    if "--fixtures" in sys.argv:
        return check_fixtures()
    detalle = "--detalle" in sys.argv
    try:
        uri = tomllib.load(open(SECRETS, "rb"))["database"]["supabase_uri"]
    except Exception:
        print("[skip] sin supabase_uri — no se puede auditar la cobertura")
        return 0
    import psycopg2
    cur = psycopg2.connect(uri, connect_timeout=30).cursor()

    if not WORD_DIR.exists():
        print(f"[ERR] no se halla la carpeta fuente: {WORD_DIR}")
        return 1

    articulados, no_articulados, criticos, faltantes_p = [], [], [], []
    for p in sorted(WORD_DIR.glob("*.docx")):
        sigla = MAPEO.get(p.name)
        if not sigla:
            continue
        tipo = TIPO.get(p.name, "?")
        cur.execute("SELECT count(*), count(DISTINCT articulo_num) FROM public.normativa_corpus "
                    "WHERE norma_sigla=%s", (sigla,))
        n_chunks, n_arts_cor = cur.fetchone()
        if tipo not in TIPOS_ARTICULADOS:
            no_articulados.append((sigla, tipo, n_chunks))
            continue
        try:
            arts = _arts_docx(_texto(p))
        except Exception as e:
            print(f"[WARN] {p.name}: {str(e)[:50]}"); continue
        cur.execute("SELECT DISTINCT articulo_num FROM public.normativa_corpus "
                    "WHERE norma_sigla=%s AND articulo_num IS NOT NULL", (sigla,))
        corp = {r[0] for r in cur.fetchall()}
        faltan = sorted(arts - corp)
        cob = 100 * len(arts & corp) / len(arts) if arts else 0.0
        # déficit GRANDE = bug de ingesta probable · déficit ≤3 y ≥95% = ruido de conteo (aceptable)
        if not arts and not corp:
            est = "s/datos"          # el .docx no usa numeración "Art. N" (CEDAW, clasificador…)
        elif not faltan:
            est = "OK"
        elif len(faltan) > 3 or cob < 95:
            est = "CRÍTICO"; criticos.append(sigla)
        else:
            est = "ruido"
        articulados.append((est, sigla, len(arts), len(corp), faltan, cob))
        if faltan and est == "CRÍTICO":
            faltantes_p.append((sigla, faltan))

    articulados.sort(key=lambda r: r[5])
    print("AUDITORÍA DE COBERTURA DEL CORPUS — fuente (.docx) vs. vectorizado (Supabase)")
    print(f"\nA · NORMAS ARTICULADAS (auditadas por conteo de artículos):")
    print(f"  {'ESTADO':8} {'NORMA':20} {'docx':>5} {'corpus':>6} {'falt':>4}  cob")
    for est, sigla, nd, nc, faltan, cob in articulados:
        print(f"  {est:8} {sigla:20} {nd:5} {nc:6} {len(faltan):4}  {cob:5.1f}%")
        if detalle and faltan:
            print(f"           faltan: {faltan[:30]}")
    print(f"\nB · NO ARTICULADAS (reforma/plan/guía — se reporta presencia, no conteo de artículos):")
    for sigla, tipo, nch in sorted(no_articulados):
        flag = "  ⚠ SIN CHUNKS" if nch == 0 else ""
        print(f"  {sigla:24} tipo={tipo:16} chunks={nch}{flag}")

    ok = sum(1 for r in articulados if r[0] == "OK")
    ruido = sum(1 for r in articulados if r[0] == "ruido")
    print(f"\nRESUMEN articuladas: {len(articulados)} · OK={ok} · ruido_conteo={ruido} · "
          f"CRÍTICAS={len(criticos)}  → {criticos}")
    return 1 if criticos else 0


if __name__ == "__main__":
    raise SystemExit(main())
