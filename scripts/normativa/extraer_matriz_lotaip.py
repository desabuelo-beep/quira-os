# -*- coding: utf-8 -*-
"""
scripts/normativa/extraer_matriz_lotaip.py — la vara con la que el Estado se mide
══════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Javo detuvo una captura que iba a contar archivos del
portal de transparencia:

> *«para trabajar este dominio está la guía metodológica de 2024; es la base del
> análisis. Todo lo que haga debe estar en base a la LOTAIP, el reglamento y la
> guía metodológica… Vamos a desnudar los niveles y vacíos de transparencia que
> tienen los GAD a nivel nacional.»*

Tenía razón y el reparo es de fondo: **contar archivos no es medir cumplimiento**.
Sin la exigencia normativa de cada numeral, un municipio que sube tres archivos
vacíos puntuaría igual que uno que publica lo debido. Es la Regla de Oro 3 en
este dominio — **sin la vara, no hay medición.**

LO QUE ESTE MÓDULO EXTRAE, y no es de QUIRA: es del órgano rector.

  · `Instructivo para evaluar el nivel de cumplimiento de los parámetros técnicos
    de la transparencia activa` · Versión 1.0, julio 2024 · Defensoría del Pueblo
  · 28 tablas: los criterios de calificación, la matriz del Art. 19 (obligaciones
    generales) y la de los Arts. 20-30 (obligaciones específicas)

Con esto QUIRA no evalúa con criterio propio: **evalúa con la misma vara que la
Defensoría aplica a los sujetos obligados**, que además fue aprobada por
resolución administrativa. Un hallazgo medido así no se discute con opiniones.

POR QUÉ SE LEE EL `.docx` Y NO EL CORPUS. El instructivo ya está ingerido (42
fragmentos), pero **sus tablas llegaron aplanadas**: el texto de cada celda
combinada aparece repetido tres veces y las columnas se mezclan. Lo que en el
corpus se lee como «Valor de la calificación… Valor de la calificación… Valor de
la calificación…» es, en el original, una fila con su valor. La estructura vive
en la correspondencia entre columnas, y el texto corrido la disuelve — el mismo
patrón de OBS-027.

QUÉ NO HACE: no evalúa a nadie. Extrae la norma para que la evaluación posterior
tenga contra qué medir.

Uso:  python scripts/normativa/extraer_matriz_lotaip.py [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    from config import DATOS_DIR as _DATOS
except Exception:                                        # noqa: BLE001
    import os as _os
    from pathlib import Path as _P
    _DATOS = _P(_os.environ.get("QUIRA_DATOS", "."))

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes                    # noqa: E402

FUENTE = Path(str(_DATOS / "Normativa_Word" / "LOTAIP - Instructivo-monitoreo-transparencia-activa-2024.docx"))

# Encabezado normalizado → campo. Los títulos traen tabulaciones y saltos dentro
# de la celda («Información completa\ty actualizada»), así que se comparan
# normalizados y por prefijo.
COLUMNAS = [
    ("articulo de la lotaip", "articulo"),
    ("numeral del articulo", "numeral"),
    ("numeral", "numeral"),
    ("descripcion del numeral", "descripcion"),
    ("descripcion del articulo", "descripcion"),
    ("descripcion", "descripcion"),
    ("formato para difusion", "formato_difusion"),
    ("informacion completa y actualizada", "completa_y_actualizada"),
    ("datos abiertos", "datos_abiertos"),
    ("registro dentro del plazo", "registro_en_plazo"),
    ("estado de verificables", "estado_verificables"),
    ("condicion", "condicion"),
    ("calificacion", "calificacion"),
    ("parametro", "parametro"),
]


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").lower()
    return " ".join(s.replace("\t", " ").replace("\n", " ").split())


def _txt(s) -> str:
    return " ".join(unicodedata.normalize("NFC", str(s or ""))
                    .replace("\t", " ").replace("\n", " ").split())


def _campo(titulo: str) -> str | None:
    t = _norm(titulo)
    for pref, campo in COLUMNAS:
        if t.startswith(pref):
            return campo
    return None


def _fila(fila) -> list[str]:
    """Word repite el contenido de una celda combinada en cada columna que ocupa.
    Sin colapsar esas repeticiones, una fila de 7 columnas se lee como 9."""
    out: list[str] = []
    for c in fila.cells:
        v = _txt(c.text)
        if not out or out[-1] != v:
            out.append(v)
    return out


def extraer() -> dict:
    import docx
    doc = docx.Document(str(FUENTE))

    criterios: list[dict] = []      # tablas de calificación
    obligaciones: list[dict] = []   # matriz por numeral

    for nt, tabla in enumerate(doc.tables, 1):
        filas = [_fila(f) for f in tabla.rows]
        if not filas:
            continue
        mapa = {j: c for j, celda in enumerate(filas[0]) if (c := _campo(celda))}
        if not mapa:
            continue

        for nf, f in enumerate(filas[1:], 2):
            reg = {mapa[j]: f[j] for j in mapa if j < len(f) and f[j]}
            if not reg:
                continue
            reg["_procedencia"] = {"tabla": nt, "fila": nf}
            # Una fila con `condicion`/`calificacion` define CÓMO se puntúa;
            # una con `numeral`/`descripcion` define QUÉ debe publicarse.
            if "calificacion" in reg and "numeral" not in reg:
                criterios.append(reg)
            elif reg.get("descripcion") or reg.get("numeral"):
                obligaciones.append(reg)

    return {"criterios": criterios, "obligaciones": obligaciones}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", help="ruta donde volcar la matriz")
    args = ap.parse_args()

    if not FUENTE.exists():
        print(f"[XX] no se halló el instructivo: {FUENTE.name}")
        sys.exit(2)

    print("MATRIZ NORMATIVA LOTAIP · Instructivo de monitoreo · DPE, julio 2024\n")
    d = extraer()
    sha = hashlib.sha256(FUENTE.read_bytes()).hexdigest()

    print(f"  CRITERIOS DE CALIFICACIÓN · {len(d['criterios'])}")
    for c in d["criterios"]:
        cond = c.get("condicion") or c.get("parametro") or "—"
        print(f"     {cond[:42]:44} → {c.get('calificacion','—')}")

    print(f"\n  OBLIGACIONES POR NUMERAL · {len(d['obligaciones'])}")
    from collections import Counter
    con_num = [o for o in d["obligaciones"] if o.get("numeral")]
    print(f"     con numeral declarado: {len(con_num)}")
    arts = Counter(o.get("articulo", "—") for o in d["obligaciones"] if o.get("articulo"))
    if arts:
        print(f"     artículos citados: {dict(arts)}")

    inv = Invariantes("matriz normativa LOTAIP")
    inv.cardinalidad("criterios", len(d["criterios"]), minimo=3)
    inv.cardinalidad("obligaciones", len(d["obligaciones"]), minimo=30)
    inv.texto_legible([o.get("descripcion", "") for o in d["obligaciones"]])
    print()
    inv.informe()

    if args.json:
        salida = {"_meta": {
            "fuente": FUENTE.name, "sha256": sha,
            "norma": "Instructivo para evaluar el nivel de cumplimiento de los "
                     "parámetros técnicos de la transparencia activa · v1.0 julio 2024",
            "emisor": "Defensoría del Pueblo de Ecuador",
            "alcance": "obligaciones generales art. 19 LOTAIP y específicas arts. 20-30",
            "nota": "vara del órgano rector · QUIRA no evalúa con criterio propio",
        }, **d}
        Path(args.json).write_text(json.dumps(salida, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
        print(f"  → {args.json}")
        print(f"  sha256 de la fuente: {sha[:32]}…")


if __name__ == "__main__":
    main()
