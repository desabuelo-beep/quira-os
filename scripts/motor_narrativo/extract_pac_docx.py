# -*- coding: utf-8 -*-
"""
Motor Narrativo — extractor del PAC (Plan Anual de Contratación) desde DOCX.
Dylus Lab © 2026 · doctrina PCD-MN01 §15 (capa R7: obra en contratación / "es paja").

Los PAC del GAD (2023-2026) vienen del portal SERCOP. El PDF sale con glyphs
scrambled (pdfplumber ilegible); el DOCX conserva el texto en runs <w:t>. Cada
proceso viene prefijado por su tipo de compra (Bien/Servicio/Obra/Consultoría) y
la descripción es legible (2024 con espacios; 2025 = print del portal, más ruido).

NO calcula nada (Regla 4). Solo lee evidencia documental para el cruce semántico:
¿la obra que la autoridad dice tener "en contratación" existe como proceso SERCOP?
Si NO está en el POA (ejecución) NI en el PAC (contratación) → candidata a "paja".
"""
from __future__ import annotations

import re
import zipfile
from functools import lru_cache
from pathlib import Path

_BASE = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi"
             r"\PAC 2023-2026\GAD Montecristi")

# cada proceso empieza en su tipo de compra (ancla robusta del PAC-SERCOP)
_TIPO = re.compile(r"(?=(?:Bien|Servicio|Obra|Consultor[ií]a))")
_TIPOWORD = re.compile(r"^(Bien|Servicio|Obra|Consultor[ií]a)\s*", re.I)
# fin de la descripción = cantidad seguida de unidad de medida
_MEDIDA = re.compile(r"\d[\d.,]*\s*(?:Unidad|Global|Metro|m2|Kg|Litro|Gal[oó]n|Mes|UNIDAD|GLOBAL)")
# líneas de cabecera / metadatos del portal (se descarta el segmento completo)
_HEADER = re.compile(r"Entidad:|Valor\s*Asignado|Nro\.?\s*Partida|Sistema Oficial|"
                     r"Consulta del Plan|Adquisici[oó]n:\d|Cat\.\s*Electr|T\.\s*R[eé]gimen|"
                     r"Tipo de Presupuesto|Fondo BID", re.I)
# vocabulario del portal SERCOP intercalado en el 2025/2026 (print de pantalla).
# se quita como FRASE (conservador: no toca palabras reales de la descripción).
_NOISE = re.compile(r"(R[eé]gimen\s*(Com[uú]n|Especial)|Proyecto\s*de\s*Inversi[oó]n|"
                    r"No\s*Aplica|Menor\s*cuant[ií]a|[IÍ]nfima\s*Cuant[ií]a|Cotizaci[oó]n|"
                    r"Licitaci[oó]n|Subasta\s*Inversa|Cat[aá]logo\s*Electr[oó]nico|Normalizad[oa])", re.I)
_NOSI = re.compile(r"(?<![A-Za-zÁÉÍÓÚÑ])(NO|SI)(?![A-Za-zÁÉÍÓÚÑ])")


def _texto(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    runs = [re.sub(r"<[^>]+>", "", t) for t in re.findall(r"<w:t[ >].*?>.*?</w:t>", xml, re.S)]
    return " ".join(r for r in runs if r.strip())


@lru_cache(maxsize=8)
def extract_pac(año: str) -> tuple:
    """Devuelve tupla de {tipo, desc} de los procesos del PAC del año. () si no existe."""
    path = _BASE / f"GAD_Montecristi_PAC_{año}.docx"
    if not path.exists():
        return ()
    t = _texto(path)
    procs, seen = [], set()
    for seg in _TIPO.split(t):
        tm = _TIPOWORD.match(seg)
        tipo = tm.group(1).capitalize() if tm else ""
        s = _TIPOWORD.sub("", seg)
        s = _MEDIDA.split(s)[0]                       # cortar en cantidad+medida
        s = re.sub(r"\s+", " ", s).strip()
        if _HEADER.search(s):                         # descartar cabecera/metadatos
            continue
        s = re.sub(r"^[^A-Za-zÁÉÍÓÚÑ]+", "", s).strip()   # limpiar códigos de partida al inicio
        if len(s) < 25 or not re.search(r"[A-Za-zÁÉÍÓÚÑ]{4,}", s):
            continue
        k = s[:60].lower()
        if k in seen:
            continue
        seen.add(k)
        procs.append({"tipo": tipo, "desc": s[:220]})
    return tuple(procs)


if __name__ == "__main__":
    import sys
    año = sys.argv[1] if len(sys.argv) > 1 else "2024"
    procs = extract_pac(año)
    print(f"PAC {año}: {len(procs)} procesos")
    for p in procs[:8]:
        print(f"  [{p['tipo'] or '?'}] {p['desc'][:100]}")
