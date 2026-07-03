# -*- coding: utf-8 -*-
"""
extract_poa_pdf.py — Extractor de actividades POA desde los PDFs oficiales
QUIRA Gov · Dylus Lab © 2026

Los POA 2023-2026 del GAD están en PDF (Holding_Municipal_Montecristi). Su
vectorización en Supabase quedó corrupta (OCR fallido) — ver METODOLOGIA_
TRAZABILIDAD_APORTES.md §3. La fuente limpia es el PDF re-extraído.

Formatos heterogéneos por año (verificado 2026-07-03):
  2023: pdfplumber · tabla 6 col · desc=col0 · partida=col2 · monto=col3
  2024: pdfplumber · tabla 6 col · desc=col1 · partida=col2 · monto=col3
  2026: pdfplumber · tabla 30 col · desc=col17 · monto=col20
  2025: pymupdf (pdfplumber sale scrambled) — get_text por página

Salida por año: lista de {anio, desc, partida, monto} — insumo del cruce con
los aportes ciudadanos (H10c). No toca el canon; deriva de documento oficial.
"""
from __future__ import annotations

import os
import re

POA_BASE = (
    r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi"
    r"\POA 2023-2026\GAD Montecristi"
)

# Config por año. engine=pdfplumber usa columnas fijas; 2025 va aparte (pymupdf).
POA_CFG = {
    "2023": {"file": "GAD Montecristi POA 2023.pdf", "engine": "pdfplumber",
             "desc": 0, "partida": 2, "monto": 3, "hdr": "ACTVIDAD"},
    "2024": {"file": "GAD Montecristi POA 2024.pdf", "engine": "pdfplumber",
             "desc": 1, "partida": 2, "monto": 3, "hdr": "ACTIVIDAD"},
    "2026": {"file": "GAD Montecristi POA 2026.pdf", "engine": "pdfplumber",
             "desc": 17, "partida": 16, "monto": 20, "hdr": None},
    "2025": {"file": "GAD Monteristi POA 2025.pdf", "engine": "pymupdf"},
}


def _clean(s) -> str:
    if s is None:
        return ""
    return re.sub(r"\s+", " ", str(s)).strip()


def _monto(s) -> float:
    """'$ 35.920,00' / '$ 1 0,000.00' → float. Tolerante a ruido de extracción."""
    if s is None:
        return 0.0
    t = re.sub(r"[^\d.,]", "", str(s))
    if not t:
        return 0.0
    # heurística: si hay ',' y '.', el último separador es el decimal
    if "," in t and "." in t:
        if t.rfind(",") > t.rfind("."):      # formato 35.920,00
            t = t.replace(".", "").replace(",", ".")
        else:                                 # formato 10,000.00
            t = t.replace(",", "")
    elif "," in t:
        t = t.replace(".", "").replace(",", ".") if t.count(",") == 1 and len(t.split(",")[-1]) == 2 else t.replace(",", "")
    try:
        return round(float(t), 2)
    except ValueError:
        return 0.0


def _extract_pdfplumber(path: str, cfg: dict) -> list[dict]:
    import pdfplumber
    rows: list[dict] = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            for tab in pg.extract_tables():
                for r in tab:
                    if not r or len(r) <= cfg["desc"]:
                        continue
                    desc = _clean(r[cfg["desc"]])
                    # saltar encabezados / vacíos
                    if not desc or len(desc) < 6:
                        continue
                    up = desc.upper()
                    if up in ("ACTIVIDAD", "ACTVIDAD", "DESCRIPCIÓN DE LA ACTIVIDAD") or "NO. DE" in up:
                        continue
                    monto = _monto(r[cfg["monto"]]) if len(r) > cfg["monto"] else 0.0
                    partida = _clean(r[cfg["partida"]]) if cfg.get("partida") is not None and len(r) > cfg["partida"] else ""
                    rows.append({"desc": desc, "partida": partida, "monto": monto})
    return rows


def _extract_pymupdf_2025(path: str) -> list[dict]:
    """POA 2025: pdfplumber sale scrambled y find_tables cuelga (41 col × 12 pág).
    get_text() sí sale legible → se toman las líneas descriptivas como candidatos
    de ejecución (frases con verbo/objeto). Sin monto por-fila (se refina luego).
    """
    import fitz
    rows: list[dict] = []
    seen: set[str] = set()
    doc = fitz.open(path)
    for pg in doc:
        for line in pg.get_text().split("\n"):
            line = _clean(line)
            letras = sum(c.isalpha() for c in line)
            if len(line) >= 40 and letras >= 25 and len(line.split()) >= 6:
                low = line.lower()
                if low in seen:
                    continue
                seen.add(low)
                rows.append({"desc": line, "partida": "", "monto": 0.0})
    return rows


def extract_poa(anio: str) -> list[dict]:
    cfg = POA_CFG.get(anio)
    if not cfg:
        return []
    path = os.path.join(POA_BASE, cfg["file"])
    if not os.path.exists(path):
        return []
    if cfg["engine"] == "pymupdf":
        rows = _extract_pymupdf_2025(path)
    else:
        rows = _extract_pdfplumber(path, cfg)
    # dedup por (desc, monto) y etiqueta de año
    seen = set()
    out = []
    for r in rows:
        k = (r["desc"].lower(), r["monto"])
        if k in seen:
            continue
        seen.add(k)
        r["anio"] = anio
        out.append(r)
    return out


if __name__ == "__main__":
    import sys
    años = sys.argv[1:] or ["2023", "2024", "2025", "2026"]
    for a in años:
        acts = extract_poa(a)
        tot = sum(x["monto"] for x in acts)
        print(f"\n=== POA {a}: {len(acts)} actividades · monto sum ${tot:,.0f} ===")
        for x in acts[:5]:
            print(f"   ${x['monto']:>12,.0f}  {x['desc'][:60]}")
