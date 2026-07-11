"""
QUIRA OS — Extractor POA MULTI-AÑO desde la FUENTE (Javo · 2026-07-11)
═══════════════════════════════════════════════════════════════════════════════
Re-vinculación meta↔actividad↔partida DESDE LA FUENTE (no inferida · Principio Rector:
la ausencia de evidencia es un RESULTADO, jamás una autorización a inferir). Los POA
oficiales del GAD por año (Excel) SÍ traen el vínculo — el 2025 tiene META·ACTIVIDAD·
PARTIDA explícitos. De ahí sale el mapa meta↔partida que ancla los años sin columna meta.

Fuente: Holding_Municipal_Montecristi\\POA 2023-2026\\GAD Montecristi\\*.xlsx
Salida: data/poa_multianio.json (artefacto curado · QUIRA lo lee · promoción candidata al canon).
Regla 1: la app lee el snapshot, no el Excel. Firewall: sin códigos internos en la salida pública.

Uso:  python scripts/enrich_poa_multianio.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
from collections import defaultdict

import openpyxl

POA_DIR = r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\Holding_Municipal_Montecristi\POA 2023-2026\GAD Montecristi"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "poa_multianio.json")

# esquema por año (col idx · descubierto por inspección de la fuente):
#   2025: META=9 · ACTIVIDAD=15 · PARTIDA=16 · MONTO=Σ(36..39) · header f4, data f5+
#   2024: ACTIVIDAD=1 · PARTIDA=2 · MONTO=3 (sin meta) · header f1, data f2+
#   2023: DESC=0 · PARTIDA=1 · MONTO=3 (sin meta · partida estructural) · data f6+
_ARCH = {
    2025: {"file": "GAD Monteristi POA 2025.xlsx", "data0": 5, "meta": 9, "act": 15, "part": 16, "monto": (36, 37, 38, 39)},
    2024: {"file": "GAD Montecristi POA 2024.xlsx", "data0": 2, "meta": None, "act": 1, "part": 2, "monto": (3,)},
    2023: {"file": "GAD Montecristi POA 2023.xlsx", "data0": 6, "meta": None, "act": 0, "part": 1, "monto": (3,)},
}


def _num(s) -> float:
    if isinstance(s, (int, float)):
        return float(s)
    try:
        return float(str(s).replace(".", "").replace(",", "."))
    except Exception:
        return 0.0


def _cell(row, i):
    return str(row[i]).strip() if (i is not None and i < len(row) and row[i] is not None) else ""


def _leer_anio(anio: int) -> list[dict]:
    a = _ARCH[anio]
    p = os.path.join(POA_DIR, a["file"])
    if not os.path.exists(p):
        return []
    ws = openpyxl.load_workbook(p, read_only=True, data_only=True)[
        openpyxl.load_workbook(p, read_only=True).sheetnames[0]]
    acts = []
    for row in list(ws.iter_rows(values_only=True))[a["data0"]:]:
        act = _cell(row, a["act"])
        part = _cell(row, a["part"])
        if not act and not part:
            continue
        monto = sum(_num(row[i]) for i in a["monto"] if i < len(row))
        acts.append({
            "meta": _cell(row, a["meta"]) if a["meta"] is not None else "",
            "actividad": act[:120],
            "partida": part,
            "monto": round(monto, 2),
        })
    return acts


def main() -> None:
    por_anio = {y: _leer_anio(y) for y in _ARCH}
    # mapa meta↔partida DESDE LA FUENTE (2025, único con META explícita): partida → metas
    p2m: dict[str, set] = defaultdict(set)
    for a in por_anio.get(2025, []):
        if a["meta"] and a["partida"]:
            p2m[a["partida"]].add(a["meta"])
    # solo las partidas DETERMINISTAS (una sola meta) sirven de ancla verificable
    ancla = {pt: next(iter(ms)) for pt, ms in p2m.items() if len(ms) == 1}

    salida = {
        "_fuente": "POA oficial GAD Montecristi por año (Excel) — vínculo meta↔actividad↔partida de la fuente",
        "_nota_metodologica": ("La 'meta' del POA es operativa (indicador). El mapa meta↔partida se toma del "
                               "2025 (único año con META explícita en la fuente); solo partidas DETERMINISTAS "
                               "(una sola meta) anclan otros años — la ausencia de vínculo NO se infiere."),
        "anios": {},
        "mapa_meta_partida_deterministas": len(ancla),
    }
    for y, acts in por_anio.items():
        con_meta = sum(1 for a in acts if a["meta"])
        # ancla los años sin meta por partida DETERMINISTA (de la fuente 2025)
        anclados = 0
        if con_meta == 0:
            for a in acts:
                if a["partida"] in ancla:
                    a["meta_ancla"] = ancla[a["partida"]]
                    anclados += 1
        salida["anios"][str(y)] = {
            "n_actividades": len(acts),
            "monto_total": round(sum(a["monto"] for a in acts), 2),
            "con_meta_fuente": con_meta,
            "anclados_por_partida": anclados,
            "actividades": acts,
        }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print("OK — data/poa_multianio.json")
    print(f"   mapa meta↔partida deterministas (de la fuente 2025): {len(ancla)} partidas")
    for y in sorted(salida["anios"]):
        d = salida["anios"][y]
        print(f"   {y}: {d['n_actividades']:>3} act · ${d['monto_total']/1e6:5.1f}M · "
              f"meta-fuente={d['con_meta_fuente']} · anclados={d['anclados_por_partida']}")


if __name__ == "__main__":
    main()
