"""
QUIRA OS — Enriquecedor del snapshot · bloque `planificacion` (QINV-001)
═══════════════════════════════════════════════════════════════════════════════
Puente Excel→snapshot (Regla 1: la fuente alimenta al deploy, nunca al revés).
Lee el Gold Master LOCAL (solo lectura · openpyxl data_only · NO corrompe) y
escribe el bloque `planificacion` en data/gm_snapshot.json para que el cajón
QINV-001 renderice NATIVO (sin cosechar páginas viejas) con dato verificado.

Secciones: A·PDOT (H04 metas+competencia) · B·POA (H05 direcciones) ·
C·PAC (H05b contratación) · D·Coherencia (H21b SAT-0). Corte Q1-2026.

Reproducible: correr tras refrescar el Gold Master. NO toca H12!B33 ni el canon.
Uso:  python scripts/enrich_planificacion.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
from collections import Counter

import openpyxl

EXCEL = r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx"
SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")


def _temp(estado: str) -> str:
    """Traduce el estado del motor (con emoji) a temperatura del firewall."""
    e = estado or ""
    if "🔴" in e:
        return "critico"
    if "⚠️" in e or "🟠" in e:
        return "alerta"
    if "✅" in e or "🟢" in e or "🔵" in e:
        return "verde"
    return "dim"


def _clean(s: str) -> str:
    """Quita emojis/marcadores de estado para almacenar texto limpio (firewall)."""
    for mk in ("🔴", "⚠️", "✅", "🟢", "🔵", "🟠", "⏳", "❌", "★"):
        s = s.replace(mk, "")
    return s.strip(" ·—-")


def build_block() -> dict:
    wb = openpyxl.load_workbook(EXCEL, read_only=True, data_only=True)

    def sh(prefix: str):
        return wb[next(s for s in wb.sheetnames if s.startswith(prefix))]

    # ── A · PDOT — metas por competencia COOTAD (H04 col D) ──────────────────
    ws = sh("H04_S2_PLAN")
    comp = Counter()
    for r in range(15, 45):
        v = ws.cell(r, 4).value
        if v:
            comp[str(v).strip().replace("_", " ")] += 1
    metas_total = sum(comp.values())
    # orden canónico de severidad de competencia
    orden = ["Exclusiva Crítica", "Concurrente Crítica", "Exclusiva Importante", "Concurrente"]
    competencia = [{"label": k, "n": comp[k]} for k in orden if comp.get(k)]
    for k, n in comp.items():            # cualquier otra categoría no prevista
        if k not in orden:
            competencia.append({"label": k, "n": n})

    # ── B · POA — metas por dirección responsable (H05 col C) ────────────────
    ws = sh("H05_S3_OPER")
    dirs = Counter()
    for r in range(14, 45):
        v = ws.cell(r, 3).value
        if v:
            name = str(v).split("+")[0].strip()       # dirección primaria (antes de "+")
            if name.startswith("Dir."):
                name = name[4:].strip()
            dirs[name] += 1
    direcciones = [{"dir": k, "n": n} for k, n in dirs.most_common()]
    n_direcciones = len(direcciones)

    # ── C · PAC — contratación (H05b) ────────────────────────────────────────
    ws = sh("H05b_S3b")
    total_pac = ws["B11"].value or 0
    tipos = Counter()
    n_proc = 0
    gap_proc = None
    for r in range(15, 60):
        pid = ws.cell(r, 1).value
        if not pid:
            continue
        n_proc += 1
        tipo = ws.cell(r, 3).value
        if tipo:
            tipos[str(tipo).strip()] += 1
        desc = str(ws.cell(r, 2).value or "")
        if "grupos prio" in desc.lower() or "atenci" in desc.lower():
            gap_proc = desc[:60]
    pac = {
        "total_usd": total_pac,
        "n_procesos": n_proc,
        "tipos": [{"tipo": t, "n": n} for t, n in tipos.most_common()],
        "gap_proceso": gap_proc,
    }

    # ── D · Coherencia — SAT-0 (H21b) ────────────────────────────────────────
    ws = sh("H21b_SAT")
    def cell(addr):
        return str(ws[addr].value or "")
    sat0 = {
        "componentes": [
            {"label": "Brecha POA-PAC", "estado": _clean(cell("B14")), "temp": _temp(cell("B14"))},
            {"label": "Downcoding contractual", "estado": _clean(cell("B15")), "temp": _temp(cell("B15"))},
            {"label": "Monto mínimo", "estado": _clean(cell("B16")), "temp": _temp(cell("B16"))},
            {"label": "Reloj de evidencia", "estado": _clean(cell("B17")), "temp": _temp(cell("B17"))},
        ],
        "global": _clean(cell("B19")),
        "global_temp": _temp(cell("B19")),
        "diagnostico": _clean(cell("B21")),
    }

    return {
        "_fuente": "PDOT (planificación) · POA (operación) · PAC (contratación) · coherencia · corte Q1-2026",
        "metas_total": metas_total,
        "competencia": competencia,
        "direcciones": direcciones,
        "n_direcciones": n_direcciones,
        "pac": pac,
        "sat0": sat0,
    }


def main() -> None:
    block = build_block()
    with open(SNAP, encoding="utf-8") as f:
        snap = json.load(f)
    snap["planificacion"] = block
    with open(SNAP, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    print("OK - bloque 'planificacion' escrito en gm_snapshot.json")
    print(f"   metas={block['metas_total']} · direcciones={block['n_direcciones']} "
          f"· PAC=${block['pac']['total_usd']:,} ({block['pac']['n_procesos']} proc) "
          f"· SAT-0={block['sat0']['global']}")


if __name__ == "__main__":
    main()
