#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/fetch_sercop.py — QUIRA OS
Obtiene el estado vivo de los procesos de contratación pública (SERCOP) de una
entidad, vía la API de Contrataciones Abiertas (OCDS).

SUBSANADO 2026-06-24: la API real es `/PLATAFORMA/api/search_ocds` + `/record`
(la antigua `/api/v1/plannedprocurement|contracts` ya no existe). Validado en vivo.

Doctrina (Javo): el Excel es la base. Este conector trae el dato LIMPIO del SERCOP
para INGERIRLO al silo H06 del Canon; el cajón cablea desde el Excel, no desde la API.

Ciclo OCDS (tag): planning (PAC) → tender → award → contract.
  planning.budget.amount.amount = monto · .id = partida · planning.rationale = descripción
  tender.value/title/status · awards[].suppliers/status

Uso:
  python scripts/fetch_sercop.py --search montecristi --buyer "GOBIERNO AUTONOMO" --year 2026
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent))

# ── CONTADOR DE FALLOS DE TRANSPORTE (2026-08-12)
# Antes, un fallo de red y una respuesta «cero procesos» devolvían ambos `None`, y
# el llamador no podía distinguirlos: con la API caída el guion imprimía
# `[OK] 0 procesos` y guardaba el archivo como si fuera una captura válida.
# **«No existe» ≠ «no pude obtener»** (ADR-042 §6). Un cero así, ingerido al Canon,
# se vuelve indistinguible de una ausencia real de contratación.
_RED = {"fallos": 0, "intentos": 0, "ultimo_error": "", "via_curl": 0}


def _via_curl(url: str, params: dict | None = None, timeout: int = 45) -> Any:
    """Reintento con `curl` cuando el cliente de Python no logra el saludo TLS.

    NO es un parche cosmético. El 2026-08-12 se dio por caída la API de SERCOP
    —«connection reset» en `requests` y en `urllib`, con y sin verificación de
    certificado— y el mismo endpoint respondía **HTTP 200 con JSON** desde `curl`
    en la misma máquina y la misma red. La conclusión anterior era falsa: no
    estaba caída, era el cliente.

    Queda como recordatorio operativo: **antes de declarar una fuente
    inalcanzable hay que agotar los transportes**, o se registra como «el Estado
    no publica» lo que en realidad es «mi cliente no negoció»."""
    import shutil
    import subprocess
    import urllib.parse as _up
    if not shutil.which("curl"):
        return None
    if params:
        url = url + "?" + _up.urlencode(params)
    try:
        r = subprocess.run(
            ["curl", "-sS", "--max-time", str(timeout), "-A", USER_AGENT,
             "-H", "Accept: application/json", url],
            capture_output=True, timeout=timeout + 15)
        if r.returncode != 0 or not r.stdout:
            return None
        _RED["via_curl"] += 1
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception:
        return None


USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120 Safari/537.36")

try:
    import requests

    def api_get(url: str, params: dict | None = None, timeout: int = 30) -> Any:
        _RED["intentos"] += 1
        try:
            r = requests.get(url, params=params or {}, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            alt = _via_curl(url, params, timeout)
            if alt is not None:
                return alt
            _RED["fallos"] += 1
            _RED["ultimo_error"] = f"{type(e).__name__}: {e}"
            print(f"[WW] GET {url} {params} -> {e}")
            return None
except ImportError:
    import urllib.parse
    import urllib.request

    def api_get(url: str, params: dict | None = None, timeout: int = 30) -> Any:
        _RED["intentos"] += 1
        try:
            if params:
                url = url + "?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            alt = _via_curl(url, params, timeout)
            if alt is not None:
                return alt
            _RED["fallos"] += 1
            _RED["ultimo_error"] = f"{type(e).__name__}: {e}"
            print(f"[WW] GET {url} -> {e}")
            return None

OUT_DIR = Path(__file__).parent.parent / "data" / "scouting"
SERCOP_API = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api"

UMBRAL_DESIERTOS_PCT = 10.0     # > 10% desiertos → alerta
UMBRAL_CANCELADOS_PCT = 15.0    # > 15% cancelados → alerta

# Caché TTL (no saturar el servicio)
_TTL = 1800
_cache: dict = {}


def _get(endpoint: str, params: dict) -> dict | None:
    key = endpoint + "?" + "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    now = time.time()
    hit = _cache.get(key)
    if hit and now - hit[0] < _TTL:
        return hit[1]
    data = api_get(f"{SERCOP_API}/{endpoint}", params)
    if data is not None:
        _cache[key] = (now, data)
    return data


# ══════════════════════════════════════════════════════════════════════════════
# OBTENCIÓN (API actual: search_ocds + record)
# ══════════════════════════════════════════════════════════════════════════════
def buscar(year: int, search: str, buyer: str | None = None, max_pages: int = 25,
           passes: int = 3) -> list[dict]:
    """Lista de procesos ÚNICOS (ocid·buyer·date) por año + palabra clave (+ filtro buyer).

    El `search_ocds` es inestable: cada llamada puede omitir ±1 proceso en el borde de
    página (universo `total` estable, muestreo no). Para un corte DEFENDIBLE del Canon
    unimos `passes` recorridos FRESCOS (sin caché) → conjunto completo y reproducible.
    Orden determinista por ocid.
    """
    uniq: dict[str, dict] = {}
    for _ in range(max(1, passes)):
        page = 1
        while page <= max_pages:
            params: dict = {"year": year, "search": search, "page": page}
            if buyer:
                params["buyer"] = buyer
            d = api_get(f"{SERCOP_API}/search_ocds", params)  # fresco: capta la variación
            if not d:
                break
            for it in d.get("data", []):
                oc = it.get("ocid")
                if oc and oc not in uniq:
                    uniq[oc] = {"ocid": oc, "buyer": it.get("buyer"),
                                "date": it.get("date"), "locality": it.get("locality")}
            if page >= int(d.get("pages", 1) or 1):
                break
            page += 1
            time.sleep(0.2)
    return sorted(uniq.values(), key=lambda x: x["ocid"] or "")


def detalle(ocid: str) -> dict:
    """Detalle OCDS por proceso (estable: el `record` es por-ocid → reproducible).
    monto sigue jerarquía adjudicado > licitado > referencial; `monto_tipo` lo declara
    para no mezclar manzanas con naranjas en el Canon."""
    d = _get("record", {"ocid": ocid})
    rels = (d or {}).get("releases", [])
    if not rels:
        return {"ocid": ocid}
    rel = rels[-1]
    out: dict[str, Any] = {"ocid": ocid, "tag": rel.get("tag", []),
                           "fecha": rel.get("date"),
                           "buyer": (rel.get("buyer") or {}).get("name", "")}
    pl = rel.get("planning") or {}
    bud = pl.get("budget") or {}
    out["partida"] = bud.get("id")
    out["descripcion"] = pl.get("rationale") or ""
    monto, tipo = (bud.get("amount") or {}).get("amount"), "referencial"
    t = rel.get("tender") or {}
    if (t.get("value") or {}).get("amount") is not None:
        monto, tipo = t["value"]["amount"], "licitado"
    if t.get("title"):
        out["descripcion"] = t["title"]
    if t.get("procurementMethod"):
        out["metodo"] = t["procurementMethod"]
    if t.get("status"):
        out["estado"] = t["status"]
    aw = rel.get("awards") or []
    if aw:
        av = (aw[0].get("value") or {}).get("amount")
        if av is not None:
            monto, tipo = av, "adjudicado"
        sups = aw[0].get("suppliers") or []
        if sups:
            out["proveedor"] = sups[0].get("name")
        out["estado"] = aw[0].get("status", out.get("estado"))
    out["monto"] = monto
    out["monto_tipo"] = tipo if monto is not None else "sin_publicar"
    return out


# ══════════════════════════════════════════════════════════════════════════════
# BLOQUE CONTRATACIÓN (para el snapshot / silo H06)
# ══════════════════════════════════════════════════════════════════════════════
def build_contratacion_block(year: int, search: str, buyer_match: str = "") -> dict:
    """Construye el bloque 'contratacion' (procesos + conteos por etapa + alertas)
    de una entidad. `search` = palabra clave; `buyer_match` acota al comprador exacto."""
    lista = buscar(year, search)
    procesos, seen = [], set()
    for it in lista:
        if buyer_match and buyer_match.upper() not in (it.get("buyer") or "").upper():
            continue
        oc = it.get("ocid")
        if not oc or oc in seen:
            continue
        seen.add(oc)
        procesos.append(detalle(oc))
    procesos.sort(key=lambda p: p.get("ocid") or "")

    conteos: dict[str, int] = {}
    total_usd = 0.0
    alertas: list[str] = []
    for p in procesos:
        etapa = (p.get("estado") or (p.get("tag") or ["?"])[-1] or "?")
        conteos[etapa] = conteos.get(etapa, 0) + 1
        total_usd += p.get("monto") or 0

    n = len(procesos)
    if n:
        for key, umbral, msg in [
            ("cancelled", UMBRAL_CANCELADOS_PCT, "cancelados_excesivos"),
            ("unsuccessful", UMBRAL_DESIERTOS_PCT, "desiertos_excesivos"),
        ]:
            c = conteos.get(key, 0)
            if c and c / n * 100 > umbral:
                alertas.append(f"{msg}_{c/n*100:.0f}pct")

    return {
        "year": year,
        "fuente": f"SERCOP OCDS · {search}" + (f" · {buyer_match}" if buyer_match else ""),
        "fecha_corte": date.today().isoformat(),
        "n_procesos": n,
        "total_usd": round(total_usd, 2),
        "conteos_por_etapa": conteos,
        "procesos": procesos,
        "alertas": alertas,
        "via_api": "ocds_search_record_union",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Estado SERCOP (OCDS) de una entidad | QUIRA OS")
    parser.add_argument("--search", required=True, help="Palabra clave (p.ej. montecristi)")
    parser.add_argument("--buyer", default="", help="Filtro por nombre del comprador")
    parser.add_argument("--year", type=int, default=date.today().year)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    print(f"[>>] SERCOP OCDS: search='{args.search}' buyer='{args.buyer}' year={args.year}")
    block = build_contratacion_block(args.year, args.search, args.buyer)

    # ── UNA CAPTURA QUE NO ALCANZÓ LA FUENTE NO ES UNA CAPTURA DE CERO.
    # Se declara `captura_fallida`, se marca el bloque y se sale con código ≠ 0
    # para que ningún proceso aguas abajo lo confunda con evidencia de ausencia.
    fallida = _RED["fallos"] > 0 and block["n_procesos"] == 0
    block["transporte"] = {"intentos": _RED["intentos"], "fallos": _RED["fallos"],
                           "ultimo_error": _RED["ultimo_error"]}
    block["estado_captura"] = "captura_fallida" if fallida else (
        "parcial_con_fallos" if _RED["fallos"] else "completa")

    if fallida:
        print(f"[XX] CAPTURA FALLIDA — {_RED['fallos']}/{_RED['intentos']} peticiones no "
              f"alcanzaron la fuente. NO significa que no existan procesos.")
        print(f"     último error: {_RED['ultimo_error'][:120]}")
    else:
        print(f"[OK] {block['n_procesos']} procesos · ${block['total_usd']:,.2f}")
        print(f"     etapas: {block['conteos_por_etapa']}")
        if _RED["fallos"]:
            print(f"[!!] {_RED['fallos']} petición(es) fallaron: captura PARCIAL, no completa.")
    if block["alertas"]:
        print(f"[!!] Alertas: {', '.join(block['alertas'])}")

    out_path = Path(args.out) if args.out else OUT_DIR / f"sercop_{args.search}_{args.year}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(block, f, ensure_ascii=False, indent=2)
    print(f"[{'XX' if fallida else 'OK'}] Guardado: {out_path}")
    if fallida:
        sys.exit(2)


if __name__ == "__main__":
    main()
