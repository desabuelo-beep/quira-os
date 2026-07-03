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
             "desc_cols": [0], "partida": 2, "monto": 3},
    "2024": {"file": "GAD Montecristi POA 2024.pdf", "engine": "pdfplumber",
             "desc_cols": [1], "partida": 2, "monto": 3},
    # 2026: tabla de 30 col — descripción rica = proyecto(col9) + actividad(col17)
    "2026": {"file": "GAD Montecristi POA 2026.pdf", "engine": "pdfplumber",
             "desc_cols": [9, 17], "partida": 16, "monto": 20},
    # 2025: el PDF sale scrambled; el DOCX (convertido por Javo) trae la tabla de
    # 40 col limpia en el XML → col13 PROYECTO · col15 ACTIVIDAD · col18 DESCRIPCIÓN
    # · col16 PARTIDA · col36-39 MONTO I-IV.
    "2025": {"file": "GAD Monteristi POA 2025.docx", "engine": "docx_xml",
             "desc_cols": [13, 15, 18], "partida": 16, "monto_cols": [36, 37, 38, 39],
             "min_cols": 40, "key_col": 15},
}

_HDR_TOKENS = ("ACTIVIDAD", "ACTVIDAD", "DESCRIPCIÓN", "DESCRIPCION", "PROYECTO",
               "PARTIDA", "MONTO", "NO. DE", "RESPONSABLE", "META")


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
    cols = cfg["desc_cols"]
    rows: list[dict] = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            for tab in pg.extract_tables():
                for r in tab:
                    if not r or len(r) <= max(cols):
                        continue
                    parts = [_clean(r[ci]) for ci in cols if ci < len(r) and _clean(r[ci])]
                    desc = " · ".join(dict.fromkeys(parts))   # une columnas, sin repetir
                    if not desc or len(desc) < 6:
                        continue
                    up = desc.upper()
                    if any(up == t or up.startswith(t + " ") or up == t + ":" for t in _HDR_TOKENS):
                        continue
                    monto = _monto(r[cfg["monto"]]) if len(r) > cfg["monto"] else 0.0
                    partida = _clean(r[cfg["partida"]]) if cfg.get("partida") is not None and len(r) > cfg["partida"] else ""
                    rows.append({"desc": desc, "partida": partida, "monto": monto})
    return rows


def _extract_docx_xml(path: str, cfg: dict) -> list[dict]:
    """POA 2025 desde el DOCX (Javo): las tablas viven en el XML como <w:tr>/<w:tc>
    con 40 col limpias. Reconstruye filas y toma proyecto+actividad+descripción.
    """
    import zipfile
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    cols = cfg["desc_cols"]
    kc = cfg["key_col"]
    rows: list[dict] = []
    for tr in re.findall(r"<w:tr[ >].*?</w:tr>", xml, re.DOTALL):
        cells = []
        for tc in re.findall(r"<w:tc[ >].*?</w:tc>", tr, re.DOTALL):
            ts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", tc)
            cells.append(_clean(" ".join(ts)))
        if len(cells) < cfg["min_cols"]:
            continue
        key = cells[kc] if kc < len(cells) else ""
        if not key or key.upper() in ("ACTIVIDAD", "DESCRIPCIÓN", "DESCRIPCION"):
            continue                                   # encabezado de tabla
        parts = [cells[ci] for ci in cols if ci < len(cells) and cells[ci]]
        desc = " · ".join(dict.fromkeys(parts))
        if len(desc) < 8:
            continue
        monto = sum(_monto(cells[ci]) for ci in cfg.get("monto_cols", []) if ci < len(cells))
        partida = cells[cfg["partida"]] if cfg.get("partida") is not None and cfg["partida"] < len(cells) else ""
        rows.append({"desc": desc, "partida": partida, "monto": monto})
    return rows


def extract_poa(anio: str) -> list[dict]:
    cfg = POA_CFG.get(anio)
    if not cfg:
        return []
    path = os.path.join(POA_BASE, cfg["file"])
    if not os.path.exists(path):
        return []
    if cfg["engine"] == "docx_xml":
        rows = _extract_docx_xml(path, cfg)
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
