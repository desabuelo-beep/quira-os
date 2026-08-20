# -*- coding: utf-8 -*-
"""
scripts/enriquecer_sercop_estado.py — el estado contractual, que es la variable
═══════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Javo: *«lo más importante de SERCOP es el monitoreo
del estado de la contratación en base al PAC: cuántos contratos están en fase
precontractual, contractual, adjudicados. Ésa es la variable que la fórmula
canónica establece»*.

La búsqueda (`search_ocds`) devuelve el proceso pero **no su trayectoria**: trae
método, tipo, proveedor y monto, y su campo `budget` es el IMPORTE, no la
partida. El estado vive en el expediente por proceso (`record`):

    tag                 planning → tender → award → contract
    planning.budget.id  la PARTIDA presupuestaria — cierra con el PAC
    tender.status       active · complete · cancelled · unsuccessful
    awards[]            adjudicaciones con proveedor

QUÉ NO HACE: no interpreta la trayectoria ni deriva variable alguna. Registra el
estado tal como SERCOP lo publica. **Que un proceso esté adjudicado no demuestra
que la meta se cumpliera** (ADR-049 §VIS-INV-003).

RITMO. Una pausa de 1,2 s entre peticiones y alto a los tres fallos seguidos. El
12-ago se dio por caída una fuente que respondía: la evidencia posterior mostró
que corta a los ~20 s de forma intermitente. **La fuente que se observa no se
castiga**, y una captura a medias se declara, no se disimula.

Uso:  python scripts/enriquecer_sercop_estado.py [--entidad "GAD Montecristi"] [--anios 2025,2026]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import subprocess
import sys
import time
import re
import urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FUENTE = RAIZ / "data" / "scouting" / "sercop_holding.json"
SALIDA = RAIZ / "data" / "scouting" / "sercop_estado_contractual.json"
API = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/record"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAUSA = 1.2
MAX_FALLOS = 3
_RED = {"intentos": 0, "fallos": 0, "seguidos": 0, "ultimo": ""}


def expediente(ocid: str, timeout: int = 45) -> dict | None:
    time.sleep(PAUSA)
    _RED["intentos"] += 1
    url = f"{API}?ocid={urllib.parse.quote(ocid)}"
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), "-A", UA, url],
                           capture_output=True, timeout=timeout + 15)
        if r.returncode != 0 or not r.stdout:
            raise RuntimeError("sin respuesta")
        d = json.loads(r.stdout.decode("utf-8", "replace"))
        _RED["seguidos"] = 0
        return d
    except Exception as e:
        _RED["fallos"] += 1
        _RED["seguidos"] += 1
        _RED["ultimo"] = f"{type(e).__name__}: {e}"
        return None


def _partida6(bruto) -> str:
    """La partida en 6 dígitos, también aquí.

    SERCOP publica `planning.budget.id` a veces corrido (`750105`) y a veces
    como código estructurado completo
    (`01.01.01.A100.110.2025.570201.000…`), donde los primeros seis dígitos son
    el programa. Tomarlo tal cual dejaba una partida sin normalizar entre 44 —y
    esa **no cruzaba con el PAC**, apareciendo como proceso fuera del plan
    cuando el defecto era del lector. La misma normalización que `extraer_pac`."""
    s = str(bruto or "").split("/")[0]
    m = re.search(r"20(?:2[3-6])\D{0,3}(\d{6})", s)
    if m:
        return m.group(1)
    d = re.sub(r"\D", "", s)
    return d[:6] if len(d) >= 6 else ""


def leer(rec: dict, ocid: str) -> dict:
    rels = (rec or {}).get("releases") or []
    if not rels:
        return {"ocid": ocid, "estado_captura": "expediente_vacio"}
    r = rels[-1]
    pl = r.get("planning") or {}
    bud = pl.get("budget") or {}
    t = r.get("tender") or {}
    aw = r.get("awards") or []
    prov = []
    for a in aw:
        for s in (a.get("suppliers") or []):
            if s.get("name"):
                prov.append(s["name"])
    return {
        "ocid": ocid,
        # La TRAYECTORIA, tal como la publica la fuente. No se resume ni se
        # traduce a una etiqueta propia: `planning` sin `award` significa algo
        # distinto de `award` sin `contract`, y colapsarlos perdería justo lo
        # que se quiere observar.
        "tag": r.get("tag") or [],
        "partida": _partida6(bud.get("id")),
        "partida_declarada": str(bud.get("id") or ""),
        "monto_planificado": (bud.get("amount") or {}).get("amount"),
        "tender_status": t.get("status"),
        "tender_titulo": t.get("title"),
        "n_adjudicaciones": len(aw),
        "proveedores": sorted(set(prov)),
        "fecha": r.get("date"),
        "estado_captura": "completa",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--entidad", help="restringe a una entidad del holding")
    ap.add_argument("--anios", default="2025,2026")
    args = ap.parse_args()

    base = json.loads(FUENTE.read_text(encoding="utf-8"))
    pendientes = []
    for a in args.anios.split(","):
        for p in base["anios"].get(a.strip(), {}).get("procesos", []):
            if args.entidad and p.get("_entidad_quira") != args.entidad:
                continue
            pendientes.append((a.strip(), p["ocid"], p.get("_entidad_quira")))

    print(f"ESTADO CONTRACTUAL · {len(pendientes)} expedientes"
          f"{' · ' + args.entidad if args.entidad else ''}\n")

    previo = {}
    if SALIDA.exists():
        previo = {r["ocid"]: r for r in
                  json.loads(SALIDA.read_text(encoding="utf-8"))["expedientes"]}

    out: list[dict] = []
    for i, (anio, ocid, ent) in enumerate(pendientes, 1):
        if ocid in previo and previo[ocid].get("estado_captura") == "completa":
            out.append(previo[ocid])
            continue
        if _RED["seguidos"] >= MAX_FALLOS:
            # Insistir contra una fuente que ya cortó tres veces no consigue el
            # dato y sí empeora el bloqueo. Lo que falta se declara.
            out.append({"ocid": ocid, "anio": anio, "entidad": ent,
                        "estado_captura": "no_alcanzada"})
            continue
        rec = expediente(ocid)
        r = (leer(rec, ocid) if rec else
             {"ocid": ocid, "estado_captura": "no_alcanzada"})
        r.update({"anio": anio, "entidad": ent})
        out.append(r)
        if i % 20 == 0:
            print(f"   {i}/{len(pendientes)} · fallos {_RED['fallos']}", flush=True)

    from collections import Counter
    comp = [r for r in out if r.get("estado_captura") == "completa"]
    print(f"\n  {len(comp)}/{len(out)} expedientes obtenidos")
    print("  trayectorias:",
          dict(Counter("→".join(r.get("tag") or []) for r in comp).most_common(6)))
    print("  con partida:", sum(1 for r in comp if r.get("partida")))
    print("  tender_status:", dict(Counter(r.get("tender_status") for r in comp)))

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(
        {"_meta": {"generado": _dt.date.today().isoformat(), "fuente": API,
                   "transporte": dict(_RED),
                   "regla": "trayectoria tal como la publica la fuente · "
                            "adjudicado ≠ meta cumplida (ADR-049 VIS-INV-003)"},
         "expedientes": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  → {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
