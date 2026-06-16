# -*- coding: utf-8 -*-
"""
scripts/_update_snapshot.py — Builder del fallback local data/gm_snapshot.json

RECREADO 2026-06-15 (Sprint D.1 Paso 3 · el original referenciado por p_carga había desaparecido).

QUÉ HACE: refresca los valores CANÓNICOS (ICPI, TGI, índices, _meta) en data/gm_snapshot.json
leyéndolos del motor vivo vía el conector canónico fetch_gold_master_data() (H73_OUTPUT_API).
PRESERVA lo curado (gad, parroquias, series_longitudinal, notas, etiquetas) — solo refresca .valor.

NO toca: Supabase · Neo4j · el Excel · B33. SOLO LECTURA del Excel + escritura del JSON LOCAL.
Idempotente. Respalda el JSON anterior antes de sobreescribir.

Uso: python scripts/_update_snapshot.py
Dylus Lab © 2026
"""
from __future__ import annotations
import sys, os, json, shutil
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass

_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_JSON = os.path.join(_RAIZ, "data", "gm_snapshot.json")


def _r(v, n=2):
    """round seguro (None-safe)."""
    return round(v, n) if isinstance(v, (int, float)) else v


def main() -> int:
    from app.connectors.gold_master import fetch_gold_master_data

    if not os.path.exists(_JSON):
        print(f"FALTA plantilla curada: {_JSON}"); return 1
    snap = json.loads(open(_JSON, encoding="utf-8").read())

    res = fetch_gold_master_data()
    if res.get("status") not in ("ok", "partial"):
        print(f"Conector falló: {res.get('error')}"); return 1
    d   = res["data"]
    icpi = d.get("icpi", {})
    tgi  = d.get("tgi", {})
    raw  = d.get("_raw_h73", {})

    icpi_pct_old = snap.get("icpi", {}).get("global_pct")

    # ── _meta ──────────────────────────────────────────────────────────────────
    m = snap.setdefault("_meta", {})
    m["fuente"]        = "SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx (slot vivo · CONTENIDO v6.0 corregido D.2A) — H73_OUTPUT_API"
    m["fecha_corte"]   = raw.get("PERIODO_CORTE", m.get("fecha_corte"))
    m["version_excel"] = "v6.0_D2A_20260615"
    m["sincronizado"]  = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} — refresco canónico desde el vivo corregido (cirugía D.2A · ICPI 27.46% · B33 intacta) vía _update_snapshot.py"
    m["nota_d2a"]      = "Refrescado tras cirugía D.2A (adscritas→SERCOP · semáforo escala+corte · FactorTemporal curva real). Valores curados (parroquias, series) preservados."

    # ── ICPI (headline) ──────────────────────────────────────────────────────────
    si = snap.setdefault("icpi", {})
    si["global"]       = _r(icpi.get("global"), 4)
    si["global_pct"]   = _r(icpi.get("global_pct"), 2)
    si["clasificacion"] = icpi.get("clasificacion", si.get("clasificacion"))
    si["acumulado_q1"] = _r(icpi.get("acumulado_q1"), 4)
    hist = icpi.get("historico", {})
    if hist:
        sh = si.setdefault("historico", {})
        for y in ("2023", "2024", "2025"):
            if y in hist: sh[y] = _r(hist[y] * 100, 2)   # contrato=fracción → snapshot=pct

    # ── TGI (titular explicador + D1-D5) ─────────────────────────────────────────
    st = snap.setdefault("tgi", {})
    if tgi.get("score") is not None: st["score"] = _r(tgi["score"], 2)
    for k in ("d1", "d2", "d3", "d4", "d5"):
        if tgi.get(k) is not None and isinstance(st.get(k), dict):
            st[k]["valor"] = _r(tgi[k], 2)
    if "IED_GLOBAL" in raw and isinstance(st.get("ied_global"), dict):
        st["ied_global"]["valor"] = _r(raw["IED_GLOBAL"] * 100, 2)
    if "BRECHA_RURAL_USD" in raw:
        st["brecha_rural_usd"] = raw["BRECHA_RURAL_USD"]
    if "IRS_GLOBAL" in raw and isinstance(st.get("irs"), dict):
        st["irs"]["valor"] = _r(raw["IRS_GLOBAL"], 2)

    # ── VECTORES causales (6 · alimentan d06 Brechas/Pulso · 'label' = etiqueta pública) ──
    def _pct(k):
        v = raw.get(k)
        return _r(v * 100, 2) if isinstance(v, (int, float)) else None
    snap["vectores"] = {
        "_nota": "6 vectores causales desde H73 (claves internas). Valores en %; 'label' = nombre PÚBLICO para la UI (frontera de lenguaje).",
        "isp": {"valor": _pct("ISP_SALUD_PRESUP"),   "label": "Salud presupuestaria"},
        "ied": {"valor": _pct("IED_GLOBAL"),          "label": "Eficiencia directiva"},
        "igp": {"valor": _pct("IGP_2026_ACTUAL"),     "label": "Participación ciudadana"},
        "ioc": {"valor": _pct("IOC_OPACIDAD"),        "label": "Opacidad informativa"},
        "iet": {"valor": _pct("IET_PERCAPITA_PEOR"),  "label": "Equidad territorial"},
        "psg": {"valor": _pct("PSG_EJECUCION"),       "label": "Presupuesto con enfoque de género"},
    }

    # ── Respaldo + escritura LOCAL (sin Supabase) ────────────────────────────────
    bak = _JSON + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(_JSON, bak)
    with open(_JSON, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"  gm_snapshot.json REFRESCADO (local · sin Supabase)")
    print(f"  respaldo: {os.path.basename(bak)}")
    print(f"  ICPI global_pct: {icpi_pct_old}  ->  {snap['icpi']['global_pct']}")
    print(f"  ICPI clasif:     {snap['icpi']['clasificacion']}")
    print(f"  TGI score:       {snap['tgi']['score']}  (D1-D5: "
          f"{[snap['tgi'].get(k,{}).get('valor') for k in ('d1','d2','d3','d4','d5')]})")
    print(f"  version_excel:   {snap['_meta']['version_excel']}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
