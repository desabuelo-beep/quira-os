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

try:
    from config import DATOS_DIR as _DATOS
except Exception:                                        # noqa: BLE001
    # ⚠️ LA CAUSA RAÍZ DEL BORRADO (2026-08-30). Ejecutado **como script**,
    # `sys.path[0]` es `scripts/`, no la raíz: `config` no es importable y este
    # bloque caía a `"."`, con lo que todas las rutas de datos apuntaban al
    # directorio de trabajo y los tres informes «no existían». La única puerta a
    # los datos es `config.DATOS_DIR` (gate REGLAS · 0 rutas fijas), así que
    # perderla en silencio no es un detalle de importación: **es quedarse sin
    # fuente creyendo que la fuente está vacía.**
    import os as _os
    import sys as _sys
    from pathlib import Path as _P
    _sys.path.insert(0, str(_P(__file__).resolve().parents[1]))
    try:
        from config import DATOS_DIR as _DATOS
    except Exception:                                    # noqa: BLE001
        if not _os.environ.get("QUIRA_DATOS"):
            raise SystemExit(
                "⛔ sin raíz de datos: `config` no es importable y QUIRA_DATOS "
                "no está definida. Se aborta en vez de asumir el directorio "
                "actual, porque asumirlo hace que toda fuente parezca ausente.")
        _DATOS = _P(_os.environ["QUIRA_DATOS"])

SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")
DOCX = str(_DATOS / "Holding_Municipal_Montecristi" / "Rendición de cuentas 2023-2025" / "GAD Montecristi")
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


def _sha(path: str) -> str:
    """La identidad del DOCX que se leyó, para que el derivado pueda señalarla.

    ESCALÓN 7 (2026-08-30). Hasta hoy este cable producía `serie` y
    `cumplimiento_actual` **sin decir de qué archivo salían**, y el único
    `_fuente` del bloque describía la otra mitad —la que viene del Excel—, así
    que quien lo leyera atribuía la serie al Gold Master. Un derivado que no
    puede señalar su origen acredita igual que una evidencia de primera mano, y
    esa diferencia es justamente la que QUIRA le mide al sujeto observado.

    La procedencia nace aquí, en el generador, y no se estampa después: añadirla
    a posteriori re-ejecutaría la cadena (lección de 2026-08-25)."""
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()[:16]


def main() -> None:
    serie, cumpl_actual, origen, faltan = [], [], {}, []
    for anio, fname in ARCHIVOS.items():
        path = os.path.join(DOCX, fname)
        if not os.path.exists(path):
            faltan.append(fname)
            continue
        s, c = _extract(Document(path))
        s["periodo"] = anio
        serie.append(s)
        # Relativo a la raíz de datos, NUNCA absoluto: una ruta con el disco de
        # una máquina dentro haría que el origen sólo se pudiera comprobar en
        # esa máquina, y el sistema tiene trinquete en 0 rutas fijas. Quien lea
        # el snapshot lo resuelve contra su propio `config.DATOS_DIR`.
        origen[anio] = {"archivo": os.path.relpath(path, str(_DATOS)).replace("\\", "/"),
                        "sha256": _sha(path)}
        if anio == "2025":
            cumpl_actual = c

    # ⛔ NO SE ESCRIBE SIN FUENTE (2026-08-30). Antes, cuando los DOCX no eran
    # accesibles, el cable seguía adelante y **guardaba listas vacías encima de
    # la serie ya extraída**: tres años de rendiciones desaparecían sin un solo
    # mensaje de error, porque «no encontré el archivo» se escribía en el
    # snapshot como si fuera «el GAD no rindió cuentas».
    #
    # Es el mismo colapso que QUIRA persigue afuera —«no lo encontré» ≠ «no
    # existe»— cometido adentro y contra nuestros propios datos. Costó los tres
    # años de la serie en una corrida real; se recuperaron del control de
    # versiones, que es la única razón por la que esto es una anécdota.
    if faltan:
        raise SystemExit(
            "⛔ ABORTA sin escribir · no se accede a "
            f"{len(faltan)} de {len(ARCHIVOS)} informes: {', '.join(faltan)}\n"
            f"   raíz esperada: {DOCX}\n"
            "   no encontrar la fuente NO es evidencia de que no haya serie: "
            "sobrescribir con vacío convertiría una falla de acceso en un "
            "hallazgo sobre el sujeto.")

    snap = json.loads(open(SNAP, encoding="utf-8").read())
    rend = snap.get("rendicion") or {}
    rend["serie"] = serie
    rend["cumplimiento_actual"] = {"periodo": "2025", "componentes": cumpl_actual}
    # SIN RELOJ, como toda procedencia del sistema: el *cuándo* pertenece al
    # sello de la cadena; el *de dónde*, al artefacto. Un reloj aquí volvería el
    # snapshot irreproducible y rompería la comprobación que lo acredita.
    rend["_origen_serie"] = origen
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
