# -*- coding: utf-8 -*-
"""
scripts/normativa/reingerir_instrumentos.py — sacar del corpus lo que no se puede leer
══════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-13). El gate de extracción halló **2.015 fragmentos
ilegibles** en el corpus, todos de instrumentos de planificación:

    POA-GAD-2025      1.434 fragmentos · 2,4 caracteres por palabra
    POA-GAD-2026-v2     349 fragmentos · 1,5
    PAI-GAD-2026        199 fragmentos · 1,1
    POA-BOMBEROS-2025    33 fragmentos · 2,1

Muestra real del PAI: «D O S E B O S J S A E T T R E I R V N O O IB L D L L E O».

LA CAUSA, corregida respecto de lo que se creía: **no se convirtieron a `.docx`,
se convirtieron a PDF**. El registro de ingesta lo dice —`archivo_nombre` termina
en `.pdf` en los cuatro—. Una hoja de cálculo ancha impresa a PDF se lee columna
por columna, y de ahí sale ese resultado. Los originales `.xlsx` estaban al lado,
intactos.

QUÉ HACE. Reingiere desde el original legible usando los extractores que
conservan la estructura tabular, **validando antes de escribir**: si un
instrumento no pasa el invariante de legibilidad, no entra. Es la diferencia
entre un pipeline que detecta basura y uno que no la produce.

COSTO: ninguno. El modelo de *embeddings* es local
(`paraphrase-multilingual-MiniLM-L12-v2`, 384 dim). Sólo CPU.

Uso:  python scripts/normativa/reingerir_instrumentos.py [--dry-run] [--sigla X]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(RAIZ))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes                            # noqa: E402

BASE_POA = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT"
                r"\Holding_Municipal_Montecristi\POA 2023-2026")


# ══════════════════════════════════════════════════════════════════════════════
# LOS CUATRO, CON SU ORIGINAL LEGIBLE
# Bomberos no tiene `.xlsx`; su original es `.docx` CON TABLAS —34×21, cabecera
# limpia—. El corpus lo había tomado igualmente de un PDF.
# ══════════════════════════════════════════════════════════════════════════════
FUENTES = {
    "POA-GAD-2025": {
        "archivo": BASE_POA / "GAD Montecristi" / "GAD Monteristi POA 2025.xlsx",
        "nombre": "Plan Operativo Anual 2025 — GAD Montecristi",
        "extractor": "poa", "anio": 2025, "dominios": "d01,d06"},
    "POA-GAD-2026-v2": {
        "archivo": BASE_POA / "GAD Montecristi" / "GAD Montecristi POA 2026.xlsx",
        "nombre": "Plan Operativo Anual 2026 — GAD Montecristi",
        "extractor": "poa", "anio": 2026, "dominios": "d01,d06"},
    "PAI-GAD-2026": {
        "archivo": BASE_POA / "GAD Montecristi" / "PAI GAD 2023-2026"
                   / "Plan Anual de inversion (PAI) 2026.xlsx",
        "nombre": "Plan Anual de Inversiones 2026 — GAD Montecristi",
        "extractor": "pai", "anio": 2026, "dominios": "d01,d06"},
    "POA-BOMBEROS-2025": {
        "archivo": BASE_POA / "Bomberos" / "Bomberos POA 2025.docx",
        "nombre": "Plan Operativo Anual 2025 — Cuerpo de Bomberos de Montecristi",
        "extractor": "docx_tabla", "anio": 2025, "dominios": "d01,d06"},
}


def _fragmentos_poa(cfg: dict) -> list[str]:
    from extraer_poa_xlsx import como_texto, extraer
    return [como_texto(r) for r in extraer(cfg["archivo"].name)]


def _fragmentos_pai(cfg: dict) -> list[str]:
    from extraer_pai import extraer
    out = []
    for r in extraer(cfg["anio"]):
        cab = f"PLAN ANUAL DE INVERSIONES {r['anio']} · {r['hoja']} · fila {r['fila']}"
        cuerpo = "\n".join(f"{k.upper().replace('_',' ')}: {v}"
                           for k, v in r["campos"].items())
        out.append(f"{cab}\n{cuerpo}")
    return out


def _fragmentos_docx_tabla(cfg: dict) -> list[str]:
    """Tablas de Word, fila a fila y con sus rótulos.

    Se lee la TABLA, no el texto corrido. Extraer un `.docx` tabular como prosa
    produce el mismo destrozo que el PDF: la estructura está en la
    correspondencia entre columnas, y leerla en línea la disuelve."""
    import docx
    doc = docx.Document(str(cfg["archivo"]))
    out: list[str] = []
    for nt, tabla in enumerate(doc.tables, 1):
        filas = [[c.text.strip() for c in f.cells] for f in tabla.rows]
        # la cabecera es la primera fila con al menos 4 rótulos distintos
        icab = next((i for i, f in enumerate(filas[:6])
                     if len({c for c in f if c}) >= 4), 0)
        cab = filas[icab]
        for n, f in enumerate(filas[icab + 1:], icab + 2):
            campos = [f"{cab[j] or f'COL{j}'}: {v}"
                      for j, v in enumerate(f) if v and j < len(cab)]
            # sin al menos tres campos con contenido no hay fila de datos
            if len(campos) < 3:
                continue
            out.append(f"{cfg['nombre']} · tabla {nt} · fila {n}\n" + "\n".join(campos))
    return out


EXTRACTORES = {"poa": _fragmentos_poa, "pai": _fragmentos_pai,
               "docx_tabla": _fragmentos_docx_tabla}


def _sha_archivo(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="extrae y valida; no toca el corpus")
    ap.add_argument("--sigla", help="reingerir sólo una")
    args = ap.parse_args()

    siglas = [args.sigla] if args.sigla else list(FUENTES)
    print("REINGESTA DE INSTRUMENTOS · desde el original legible\n")

    listos: dict[str, tuple] = {}
    for sig in siglas:
        cfg = FUENTES[sig]
        if not cfg["archivo"].exists():
            print(f"  ✗ {sig:20} original no hallado: {cfg['archivo'].name}")
            continue
        try:
            frags = EXTRACTORES[cfg["extractor"]](cfg)
        except Exception as e:
            print(f"  ✗ {sig:20} extracción falló · {type(e).__name__}: {e}")
            continue

        # ── EL GATE CORRE ANTES DE ESCRIBIR, no después.
        # Es toda la diferencia: un pipeline que detecta basura ya la tiene
        # dentro; uno que valida antes no llega a producirla.
        inv = Invariantes(sig)
        inv.texto_legible(frags)
        inv.cardinalidad("fragmentos", len(frags), minimo=10)
        if inv.rotos:
            inv.informe()
            print(f"     → NO se reingiere: entraría igual de ilegible.\n")
            continue
        print(f"  ✓ {sig:20} {len(frags):5} fragmentos · legible · "
              f"{cfg['archivo'].suffix} original")
        listos[sig] = (cfg, frags)

    if not listos:
        print("\n  nada que reingerir.")
        return
    if args.dry_run:
        print(f"\n  {len(listos)} instrumento(s) listos. "
              f"dry-run: no se tocó el corpus.")
        return

    # ── escritura
    import psycopg2
    import tomllib
    from ingest import _get_model                                # noqa: E402
    uri = tomllib.load(open(RAIZ / ".streamlit" / "secrets.toml", "rb")
                       )["database"]["supabase_uri"]
    cn = psycopg2.connect(uri)
    cn.autocommit = False
    modelo = _get_model()
    print(f"\n  modelo local listo · sin costo de API\n")

    for sig, (cfg, frags) in listos.items():
        cur = cn.cursor()
        cur.execute("SELECT count(*) FROM normativa_corpus WHERE norma_sigla=%s", (sig,))
        antes = cur.fetchone()[0]
        cur.execute("DELETE FROM normativa_corpus WHERE norma_sigla=%s", (sig,))

        sha_arch = _sha_archivo(cfg["archivo"])
        vecs = modelo.encode(frags, convert_to_numpy=True, show_progress_bar=False)
        nuevos = 0
        # `jerarquia` es ENTERO (0 = instrumento territorial, no norma con rango) y
        # el milestone de esta familia es `F1.0`. Ambos verificados contra las filas
        # ya existentes del mismo `tipo_documento`, no supuestos: el primer intento
        # pasó texto donde iba un entero y la transacción abortó — sin daño, porque
        # el `DELETE` iba dentro de la misma transacción y revirtió con ella.
        for i, (txt, v) in enumerate(zip(frags, vecs), 1):
            emb = "[" + ",".join(f"{x:.6f}" for x in v.tolist()) + "]"
            cur.execute("""
                INSERT INTO normativa_corpus
                    (norma_sigla, norma_nombre, jerarquia, milestone_qlep,
                     tipo_documento, chunk_seq, contenido, palabras,
                     dominios_quira, sha256, embedding, archivo_nombre,
                     archivo_sha256, ingestado_at, ingestado_por)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::vector,%s,%s,now(),%s)
                ON CONFLICT (sha256) DO NOTHING
            """, (sig, cfg["nombre"], 0, "F1.0",
                  "INSTRUMENTO_TERRITORIAL", i, txt, len(txt.split()),
                  cfg["dominios"],
                  hashlib.sha256(f"{sig}|{i}|{txt}".encode()).hexdigest(),
                  emb, cfg["archivo"].name, sha_arch,
                  "reingesta-desde-original-2026-08-13"))
            nuevos += cur.rowcount
        cn.commit()
        print(f"  {sig:20} {antes:5} rotos eliminados → {nuevos:5} legibles insertados")
        cur.close()
    cn.close()
    print("\n  Verificar con: python scripts/ci/check_extraccion.py")


if __name__ == "__main__":
    main()
