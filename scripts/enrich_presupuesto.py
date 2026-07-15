"""
QUIRA OS — Enriquecedor del snapshot · bloque `presupuesto_dom` (DOM d02)
═══════════════════════════════════════════════════════════════════════════════
Puente Excel→snapshot (Regla 1). Lee el Gold Master LOCAL (solo lectura · openpyxl
data_only · NO corrompe) y escribe el bloque `presupuesto_dom` en data/gm_snapshot.json.

VISIÓN d02 (corrección de Javo · 2026-07-14): la salud financiera del municipio COMO
BASE para captar financiamiento internacional (reembolsable y no reembolsable).
  ① La base financiera:  ejecución presupuestaria (H07 eSIGEF) · salud presup. (ISP · H19)
  ② La capacidad de captación:  eficiencia/fondos externos (IEF · H20c) + llaves de
     elegibilidad (alineación PND H11b · Agenda 2030) — consumidas, no propias.
  ③ Reporte de cooperación (H32) — a futuro.
"Qué fondo específico aplica" = QUIRA Cooperación (producto · ADR-024), NO este cajón.

Uso:  python scripts/enrich_presupuesto.py
Dylus Lab © 2026
"""
from __future__ import annotations

import json
import os
import re

import openpyxl

EXCEL = r"C:\Users\DELL\Desktop\Javo\Dylus Lab\ProyecT\SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx"
SNAP = os.path.join(os.path.dirname(__file__), "..", "data", "gm_snapshot.json")

_HCODE = re.compile(r"\bH\d{1,2}[a-z]?\b")


def _fw(s) -> bool:
    """Seguro para público: sin nomenclatura canónica (H01-H99) ni fila-nota (Firewall)."""
    s = str(s or "")
    return not _HCODE.search(s) and not s.strip().upper().startswith("NOTA")


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def build_block() -> dict:
    wb = openpyxl.load_workbook(EXCEL, read_only=True, data_only=True)

    def sh(prefix: str):
        return wb[next(s for s in wb.sheetnames if s.startswith(prefix))]

    def find(ws, etiqueta: str, col_val: int = 2, maxr: int = 60):
        """Busca una fila cuyo col 1 contenga `etiqueta` y devuelve el valor de col_val."""
        for r in ws.iter_rows(min_row=1, max_row=maxr, values_only=True):
            if r and r[0] and etiqueta.lower() in str(r[0]).lower():
                return r[col_val - 1] if len(r) >= col_val else None
        return None

    # ── ① SALUD PRESUPUESTARIA (ISP · H19) ────────────────────────────────────
    ws = sh("H19_ICS")
    isp_ref = str(find(ws, "ISP_Global", col_val=3) or "")     # "58.40% — Transición Crítica" (col 2 = Ti, no ISP)
    _m = re.search(r"([\d.]+)\s*%", isp_ref)
    isp_pct = round(float(_m.group(1)), 1) if _m else 0
    isp_clasif = str(find(ws, "Clasificación_ISP") or isp_ref).strip()
    isp = {
        "global_pct": isp_pct,
        "clasificacion": re.sub(r"[🔴🟡🟢🟠⚠️✅]", "", isp_clasif).strip(" —·"),
        "umbral_cootad": 65,  # COOTAD Art. 192 — mínimo de inversión
    }

    # ── ① EJECUCIÓN PRESUPUESTARIA (H07 eSIGEF) ───────────────────────────────
    ws = sh("H07_S5")
    cod = _num(find(ws, "Codificado_Total_Inversión")) or 0
    dev = _num(find(ws, "Devengado_Total_Inversión")) or 0
    ti = _num(find(ws, "Ti_Global_2026")) or 0
    corte = str(find(ws, "Fecha_Corte") or "").strip()
    ejecucion = {
        "codificado": round(cod), "devengado": round(dev),
        "ti_pct": round(ti * 100, 1) if ti <= 1 else round(ti, 1),
        "corte": corte,
    }
    # serie multi-año del Ti (2023-2026)
    serie = []
    for r in ws.iter_rows(min_row=24, max_row=32, values_only=True):
        if r and str(r[0]).strip().isdigit() and _num(r[1]) is not None:
            v = _num(r[1])
            serie.append({"anio": int(r[0]), "ti_pct": round(v * 100, 1) if v <= 1 else round(v, 1)})

    # ── ② CAPTACIÓN — FONDOS EXTERNOS (IEF · H20c) ────────────────────────────
    ws = sh("H20c")
    fondos, total_ext = [], 0.0
    for r in ws.iter_rows(min_row=14, max_row=60, values_only=True):
        if not r or not r[0]:
            continue
        mid = str(r[0]).strip()
        nombre = str(r[1] or "").strip()
        tipo = str(r[2] or "").strip()
        monto = _num(r[3]) or 0
        if not _fw(mid) or not _fw(nombre) or monto <= 0:
            continue
        # reembolsable vs no reembolsable (convenios/bonos = no reembolsable; crédito = reembolsable)
        reemb = "reembolsable" if any(k in (nombre + tipo).lower() for k in ("crédit", "credit", "préstamo", "prestamo", "banco")) else "no reembolsable"
        fondos.append({"meta": mid, "nombre": nombre[:70], "tipo": tipo.replace("_", " ").title(),
                       "monto": round(monto), "modalidad": reemb})
        total_ext += monto

    ief_umbral = {"alto": _num(find(ws, "Umbral_Alto")), "bueno": _num(find(ws, "Umbral_Bueno"))}
    captacion = {
        "total_externo": round(total_ext), "n_convenios": len(fondos),
        "detalle": fondos, "umbrales": ief_umbral,
    }

    # ── ② LLAVES DE ELEGIBILIDAD (consumidas · no propias) ────────────────────
    #  Alineación al Plan Nacional (H11b) — objeto compartido que nace en d01.
    try:
        _snap = json.load(open(SNAP, encoding="utf-8"))
        vm = ((_snap.get("planificacion", {}) or {}).get("alineacion_pnd", {}) or {}).get("vinculacion_media")
        alineacion_pnd = round(vm * 100) if vm else None
    except Exception:
        alineacion_pnd = None

    return {
        "_fuente": "Presupuesto (cédula eSIGEF) · Salud presupuestaria (ISP) · Eficiencia financiera / fondos "
                   "externos (IEF) · alineaciones consumidas · corte Abril 2026",
        "vision": "La salud financiera del municipio como base para captar financiamiento internacional "
                  "(reembolsable y no reembolsable).",
        "isp": isp,
        "ejecucion": ejecucion,
        "serie": serie,
        "captacion": captacion,
        "elegibilidad": {
            "alineacion_pnd_pct": alineacion_pnd,     # consumido de H11b (d01)
            "nota": "Qué fondo específico aplica lo resuelve QUIRA Cooperación (producto), no este dominio.",
        },
        "publicado": True,
    }


def main() -> None:
    block = build_block()
    snap = {}
    if os.path.exists(SNAP):
        with open(SNAP, encoding="utf-8") as f:
            snap = json.load(f)
    snap["presupuesto_dom"] = block
    with open(SNAP, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    print("OK - bloque 'presupuesto_dom' escrito en gm_snapshot.json")
    print(f"   ISP={block['isp']['global_pct']}% · ejecución Ti={block['ejecucion']['ti_pct']}% "
          f"· fondos externos ${block['captacion']['total_externo']:,} ({block['captacion']['n_convenios']} convenios)")


if __name__ == "__main__":
    main()
