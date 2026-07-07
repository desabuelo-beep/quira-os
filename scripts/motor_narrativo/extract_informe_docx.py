# -*- coding: utf-8 -*-
"""
Motor Narrativo — extractor del INFORME de rendición de cuentas (CPCCS) desde DOCX.
Dylus Lab © 2026 · doctrina PCD-MN01 §16 (capa CPCCS · Ambas: fuente + evidencia).

El informe CPCCS es el documento ESCRITO de la rendición (la matriz de compromisos/
gestión que el GAD sube al CPCCS). Sirve para dos cosas (aval de Javo · 2026-07-07):
  A) EVIDENCIA — corroborar el discurso del video contra lo que el GAD declaró por
     escrito (cifras, coberturas que el POA/PAC no capturan).
  B) FUENTE — cuando una rendición NO tiene video (ej. Aseo EP/Bomberos/Patronato
     2024), el informe escrito es la ENTRADA del motor.

El contenido vive en las TABLAS (la matriz de rendición), no en párrafos. Extrae
párrafos + celdas como segmentos de texto. NO calcula nada (Regla 4): solo lee la
declaración oficial para el cruce. Entidades del holding parametrizadas.
"""
from __future__ import annotations

import re
import zipfile
from functools import lru_cache
from pathlib import Path

_BASE = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi"
             r"\Rendición de cuentas 2023-2025")

# entidad -> plantilla de nombre de archivo (los nombres del holding no son uniformes)
_ARCHIVO = {
    "GAD": ("GAD Montecristi", "GAD Monteristi Rendición de cuentas {a}.docx"),
    "Aseo": ("Aseo EP", "Aseo EP - Rendición de cuentas  {a}.docx"),
    "Bomberos": ("Bomberos", "Bomberos Rendición de cuentas {a}.docx"),
    "Patronato": ("Patronato", "Patronato Rendición de cuentas {a}.docx"),
}
# ruido de plantilla/borrador que no es contenido de gestión
_RUIDO = re.compile(r"Borrador enviado|remitente|Correo Institucional|firmado\s*con\s*fecha|"
                    r"Verificable:https?|cloud\.montecristi|@montecristi\.gob\.ec", re.I)


_VENTANA, _OVERLAP = 55, 12  # palabras por chunk / solape (modo documento)


def _segmentos(path: Path) -> list[str]:
    """La matriz de rendición viene fragmentada en celdas diminutas → se une todo
    el texto y se corta en ventanas deslizantes (mismo criterio que la ingesta del
    corpus en modo documento). Robusto a la fragmentación en celdas del DOCX."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    runs = [re.sub(r"<[^>]+>", "", t) for t in re.findall(r"<w:t[ >].*?>(.*?)</w:t>", xml, re.S)]
    full = " ".join(r for r in runs if r.strip())
    full = re.sub(r"&quot;", '"', re.sub(r"&amp;", "&", full))
    full = re.sub(r"\s+", " ", full).strip()
    words = full.split()
    out, i = [], 0
    while i < len(words):
        chunk = " ".join(words[i:i + _VENTANA]).strip()
        if len(chunk) > 40 and not _RUIDO.search(chunk):
            out.append(chunk[:400])
        i += _VENTANA - _OVERLAP
    return out


@lru_cache(maxsize=16)
def extract_informe(año: str, entidad: str = "GAD") -> tuple:
    """Segmentos de texto del informe CPCCS de la entidad/año. () si no existe."""
    carpeta, patron = _ARCHIVO.get(entidad, _ARCHIVO["GAD"])
    path = _BASE / carpeta / patron.format(a=año)
    if not path.exists():
        return ()
    return tuple(_segmentos(path))


if __name__ == "__main__":
    import sys
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    ent = sys.argv[2] if len(sys.argv) > 2 else "GAD"
    segs = extract_informe(año, ent)
    print(f"INFORME CPCCS {ent} {año}: {len(segs)} segmentos")
    for s in segs[:8]:
        print(f"  • {s[:120]}")
