# -*- coding: utf-8 -*-
"""
scripts/enrich_rdc_docx.py — Cable Documental del MCD Rendición de Cuentas (serie 3 años)
═══════════════════════════════════════════════════════════════════════════════════════
Capa 2 del modelo 3-capas (Javo 2026-07-02): los informes oficiales de RDC son DOCUMENTOS.
Este cable EXTRAE la serie estructurada de los 3 informes CPCCS (2023-2025) y la MERGE al
bloque `rendicion` del snapshot (no toca fidelidad/cpccs que vienen del Excel).

Pipeline: enrich_rdc.py (Excel: fidelidad+cpccs) → enrich_rdc_docx.py (DOCX: serie+cumplimiento).
Fuente verificable: informes oficiales CPCCS (docx) · corte 2023-2025. Regla 3: no se inventa.
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
import re

from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")
DOCX = r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi\Rendición de cuentas 2023-2025\GAD Montecristi"
ARCHIVOS = {
    "2023": "GAD Monteristi Rendición de cuentas 2023.docx",
    "2024": "GAD Monteristi Rendición de cuentas 2024.docx",
    "2025": "GAD Monteristi Rendición de cuentas 2025.docx",
}


def _txt(cell) -> str:
    return re.sub(r"\s+", " ", (cell.text or "").strip())


def _blocks(doc: Document):
    """Itera párrafos y tablas EN ORDEN del cuerpo (para rastrear secciones)."""
    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield "p", Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield "t", Table(child, doc)


def _extract(doc: Document) -> tuple[dict, list]:
    serie = {"informe_n": "", "fecha_rdc": "", "lugar": "", "asistentes": None, "n_componentes": 0}
    cumpl: list[dict] = []
    section = ""
    for kind, blk in _blocks(doc):
        if kind == "p":
            tx = re.sub(r"\s+", " ", (blk.text or "").strip())
            up = tx.upper()
            if "RENDICIÓN DE CUENTAS N" in up and not serie["informe_n"]:
                m = re.search(r"N[°º]\s*(\d+)", tx)
                serie["informe_n"] = m.group(1) if m else ""
            if "CUMPLIMIENTO DEL PLAN DE TRABAJO" in up:
                section = "cumpl"
            elif "CUMPLIMIENTO DE OBLIGACIONES" in up:
                section = "trib"
            elif "MECANISMOS DE PARTICIPACIÓN" in up:
                section = "part"
            elif "APORTES CIUDADANOS" in up:
                section = "aportes"
            continue
        t = blk
        hdr = " ".join(_txt(c).upper() for c in t.rows[0].cells) if t.rows else ""
        if "FECHA DE LA RENDICI" in hdr and len(t.rows) > 1:
            vals = [_txt(c) for c in t.rows[1].cells]
            serie["fecha_rdc"] = vals[0] if len(vals) > 0 else ""
            serie["lugar"] = (vals[1] if len(vals) > 1 else "")[:42]
            try:
                serie["asistentes"] = int(re.sub(r"[^\d]", "", vals[2])) if len(vals) > 2 and vals[2] else None
            except ValueError:
                pass
        if section == "cumpl" and len(t.columns) == 4:
            c0 = _txt(t.rows[0].cells[0]).lower() if t.rows else ""
            if c0.startswith("plan de trabajo") or not c0:
                continue
            comp = _txt(t.rows[0].cells[0])
            res = " ".join(_txt(r.cells[2]) for r in t.rows
                           if len(r.cells) > 2 and _txt(r.cells[2]) and _txt(r.cells[2]) != "-")
            cumpl.append({"componente": comp[:95], "resultado": res[:230]})
    serie["n_componentes"] = len(cumpl)
    return serie, cumpl


def main() -> None:
    serie, cumpl_actual = [], []
    for anio, fname in ARCHIVOS.items():
        path = os.path.join(DOCX, fname)
        if not os.path.exists(path):
            print(f"[skip] no existe: {fname}")
            continue
        s, c = _extract(Document(path))
        s["periodo"] = anio
        serie.append(s)
        if anio == "2025":
            cumpl_actual = c

    snap = json.loads(open(SNAP, encoding="utf-8").read())
    rend = snap.get("rendicion") or {}
    rend["serie"] = serie
    rend["cumplimiento_actual"] = {"periodo": "2025", "componentes": cumpl_actual}
    snap["rendicion"] = rend
    open(SNAP, "w", encoding="utf-8").write(json.dumps(snap, ensure_ascii=False, indent=2))

    print("OK - serie RDC (docx) merge al snapshot")
    for s in serie:
        print(f"   {s['periodo']}: informe N°{s['informe_n']} · {s['fecha_rdc']} · {s['asistentes']} asistentes "
              f"· {s['n_componentes']} componentes")
    print(f"   cumplimiento 2025: {len(cumpl_actual)} componentes · ej: "
          f"{cumpl_actual[0]['componente'] if cumpl_actual else '—'}")


if __name__ == "__main__":
    main()
