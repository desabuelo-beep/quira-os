# -*- coding: utf-8 -*-
"""
scripts/normativa/extraer_pac.py — el Plan Anual de Contratación del holding
════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-13). Javo: *«todos los PAC del GAD están en la carpeta,
en word y pdf; el PAC lo puedo proveer yo. Lo más importante de SERCOP es el
monitoreo del estado de la contratación en base al PAC»*.

Eso corrige el foco: **el PAC no es lo que hay que ir a buscar a SERCOP.** Está
en disco, son trece documentos de las cuatro entidades, y es el insumo de
referencia. Lo que SERCOP debe aportar es otra cosa —el estado real de cada
proceso—, y eso no se sustituye con el PAC.

    PAC     → ¿qué previó contratar el GAD?      · insumo documental
    SERCOP  → ¿en qué estado está ese proceso?   · variable del cálculo canónico

POR QUÉ SE LEE EL `.docx` Y NO EL `.pdf`. El PAC del GAD existe en ambos
formatos. El `.docx` trae las tablas íntegras; **el `.pdf` es una impresión de la
pantalla del portal** —incluye «Buscar», «Limpiar», «Presione el botón»— y una
tabla ancha impresa a PDF se lee columna por columna. Es exactamente lo que
destrozó cuatro documentos del corpus (OBS-027). Entre un Word con tablas y un
PDF de tabla ancha, **el Word gana siempre**.

QUÉ NO HACE: no infiere estado de contratación. El PAC dice lo planificado; que
un ítem esté en el PAC **no demuestra que se contratara**.

Uso:  python scripts/normativa/extraer_pac.py [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes                       # noqa: E402

BASE = Path(r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT"
            r"\Holding_Municipal_Montecristi\PAC 2023-2026")

ENTIDADES = {"GAD Montecristi": "GAD Montecristi", "Aseo EP": "Empresa Pública de Aseo",
             "Bomberos": "Cuerpo de Bomberos", "Patronato": "Patronato"}

# Columnas del formulario oficial del PAC, por posición. El formato es el del
# portal y se repite en las cuatro entidades y los cuatro años.
CAMPOS = {0: "n_item", 1: "partida", 2: "cpc", 3: "tipo_compra",
          4: "descripcion", 5: "cantidad", 6: "unidad",
          7: "costo_unitario", 8: "total"}


def _txt(c) -> str:
    return " ".join(str(c).replace("\n", " ").split())


def _partida6(bruto: str) -> str:
    """El clasificador de 6 dígitos, venga como venga escrito.

    Cada entidad lo escribe distinto y **ninguna forma es incorrecta**: el GAD
    corrido (`750105`), Bomberos punteado (`84.02.02`), el Patronato con el
    código extendido partido por un salto de línea (`7.3.08.21\\n.000.00`), y a
    veces dos partidas en una misma celda (`84.01.03/53.14.03`).

    Exigir seis dígitos seguidos rechazaba **diez de los trece documentos**, y
    eso habría quedado registrado como «el holding no publica su PAC» cuando el
    defecto era del lector. Es el mismo error que OBS-027 corrigió en el POA.
    Y una trampa más: el GAD escribe a veces el CÓDIGO ESTRUCTURADO COMPLETO
    —`01.01.01.A100.110.2024.530255.000…`—, donde los primeros seis dígitos son
    `010101`, que no es ninguna partida sino el programa. La partida viene
    **después del año**. Sólo afectaba a 2 de 586 ítems, pero un lector que
    acierta el 99,7 % y falla en silencio es peor que uno que falla entero: los
    dos casos malos habrían entrado al Canon como partidas válidas."""
    s = _txt(bruto).split("/")[0]           # doble partida: manda la primera
    m = re.search(r"20(?:2[3-6])\D{0,3}(\d{6})", s)
    if m:
        return m.group(1)
    d = re.sub(r"\D", "", s)
    return d[:6] if len(d) >= 6 else ""


def _fila_unica(fila) -> list[str]:
    """Word repite el contenido de una celda combinada en cada columna que ocupa.
    Sin colapsar esas repeticiones, la columna 1 se leería nueve veces."""
    out: list[str] = []
    for c in fila.cells:
        v = _txt(c.text)
        if not out or out[-1] != v:
            out.append(v)
    return out


def extraer_archivo(ruta: Path, entidad: str, anio: int) -> tuple[list[dict], dict]:
    import docx
    doc = docx.Document(str(ruta))
    items: list[dict] = []
    cab: dict = {}
    direccion = ""

    for nt, tabla in enumerate(doc.tables, 1):
        for nf, fila in enumerate(tabla.rows, 1):
            vs = _fila_unica(fila)
            if len(vs) >= 2 and vs[0].endswith(":"):
                cab[vs[0].rstrip(":").strip()] = vs[1]
                continue
            # Encabezado de unidad administrativa: una sola celda con texto.
            # Se conserva porque atribuye los ítems que le siguen.
            if len([v for v in vs if v]) == 1 and len(vs[0] if vs else "") > 8:
                direccion = vs[0]
                continue
            if len(vs) < 8 or not vs[0].strip().isdigit():
                continue
            partida = _partida6(vs[1])
            if not partida:
                continue
            reg = {CAMPOS[i]: vs[i] for i in CAMPOS if i < len(vs)}
            reg["partida_declarada"] = _txt(vs[1])   # se conserva como la escribió la entidad
            reg["partida"] = partida
            reg.update({"entidad": entidad, "anio": anio, "unidad": direccion,
                        "_procedencia": {"archivo": ruta.name, "tabla": nt, "fila": nf}})
            items.append(reg)
    return items, cab


def como_texto(r: dict) -> str:
    cab = f"PLAN ANUAL DE CONTRATACIÓN {r['anio']} · {r['entidad']} · ítem {r['n_item']}"
    campos = [(k, v) for k, v in r.items()
              if k not in ("_procedencia", "entidad", "anio") and v]
    return cab + "\n" + "\n".join(f"{k.upper().replace('_',' ')}: {v}" for k, v in campos)


def extraer_todo() -> list[dict]:
    out: list[dict] = []
    for carpeta, entidad in ENTIDADES.items():
        d = BASE / carpeta
        if not d.is_dir():
            continue
        for ruta in sorted(d.glob("*.docx")):
            m = re.search(r"20(2[3-6])", ruta.name)
            if not m:
                continue
            try:
                items, _ = extraer_archivo(ruta, entidad, int(m.group(0)))
                out.extend(items)
            except Exception as e:
                print(f"  ⚠ {ruta.name}: {type(e).__name__}: {e}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", help="ruta donde volcar el resultado")
    args = ap.parse_args()

    print("PLAN ANUAL DE CONTRATACIÓN · holding municipal de Montecristi\n")
    regs = extraer_todo()

    from collections import Counter
    por = Counter((r["entidad"], r["anio"]) for r in regs)
    for (ent, a), n in sorted(por.items(), key=lambda x: (x[0][1], x[0][0])):
        sub = [r for r in regs if r["entidad"] == ent and r["anio"] == a]
        parts = len({r["partida"] for r in sub})
        tot = sum(float(r.get("total", "0").replace(",", "") or 0)
                  for r in sub if re.fullmatch(r"[\d,.]+", r.get("total", "")))
        print(f"  {a}  {ent:26} {n:4} ítems · {parts:3} partidas · ${tot:>14,.2f}")

    inv = Invariantes("PAC del holding")
    inv.columna_con_forma([r["partida"] for r in regs], "partida", r"\d{6}", minimo=0.99)
    inv.texto_legible([como_texto(r) for r in regs])
    inv.cardinalidad("ítems", len(regs), minimo=100)
    print()
    inv.informe()

    if args.json:
        Path(args.json).write_text(json.dumps(regs, ensure_ascii=False, indent=1),
                                   encoding="utf-8")
        print(f"  → {args.json}")


if __name__ == "__main__":
    main()
