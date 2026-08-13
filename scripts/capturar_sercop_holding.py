# -*- coding: utf-8 -*-
"""
scripts/capturar_sercop_holding.py — los procesos del holding, por COMPRADOR
════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). La captura vigente buscaba `search=montecristi` y
traía **menos de un tercio** de los procesos del holding. Medido el mismo día
contra la API, año 2025:

    search=montecristi ......................  97 procesos
    suma por comprador ...................... ~306 procesos
    lo que había ingerido en Supabase (GAD) ..  20 procesos

Aquello se había leído como «la contratación cayó de 121 a 20 procesos». **No
cayó: no la estábamos capturando.** Un cero derivado de ahí habría producido
falsos `V_SERCOP = 0` en masa — el mismo defecto que OBS-028 halló en H13.

TRES TRAMPAS DEL BUSCADOR, verificadas antes de escribir este guion:

1. **`search` no compara la cadena literal.** `search=GADMCM` devuelve 127
   procesos… de Muisne, Mera y Mejía. El código de la entidad no sirve como
   criterio de búsqueda.
2. **El comprador cambia de nombre entre años.** En 2025 el municipio aparece
   como «MUNICIPIO DE MONTECRISTI» (24) *y* como «GOBIERNO AUTONOMO
   DESCENTRALIZADO MUNICIPAL DEL CANTON MONTECRISTI» (56). Buscar por uno solo
   pierde el otro; hay que unir y deduplicar por `ocid`.
3. **El filtro `buyer` no es exacto.** Con el nombre del Patronato la API
   devuelve dos compradores distintos, así que **se vuelve a filtrar en casa**
   contra los nombres declarados.

Uso:  python scripts/capturar_sercop_holding.py --anios 2025,2026 [--escribir]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import unicodedata
import urllib.parse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "data" / "scouting" / "sercop_holding.json"
API = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

# Las cinco denominaciones bajo las que aparece el holding. `MUNICIPIO DE
# MONTECRISTI` es el nombre anterior del mismo GAD: se consulta igual porque los
# procesos viejos siguen registrados con él.
COMPRADORES = {
    "GAD Montecristi": ["GOBIERNO AUTONOMO DESCENTRALIZADO MUNICIPAL DEL CANTON MONTECRISTI",
                        "MUNICIPIO DE MONTECRISTI"],
    "Cuerpo de Bomberos": ["CUERPO DE BOMBEROS DE MONTECRISTI"],
    "Empresa Pública de Aseo": ["EMPRESA MUNICIPAL DE ASEO INTEGRAL MONTECRISTI-EP"],
    "Patronato": ["Patronato Municipal de Amparo Social de Montecristi",
                  "PATRONATO MUNICIPAL DE AMPARO SOCIAL DE MONTECRISTI"],
}

_RED = {"intentos": 0, "fallos": 0, "ultimo_error": ""}

# ══════════════════════════════════════════════════════════════════════════════
# CONTROL DE RITMO — no es cortesía, es método
#
# El 2026-08-12, tras ~60 peticiones en una hora (una captura anual, pruebas de
# cobertura y un proceso de fondo con tres pasadas), el servicio dejó de
# responder y empezó a cortar la conexión a los ~20 s. Lo más probable es que
# fuera límite de tasa, no caída: minutos antes contestaba con normalidad.
#
# Importa más allá de lo operativo. QUIRA observa servicios públicos del Estado;
# saturarlos degrada el acceso de terceros y contamina la propia medición —un
# portal que dejamos de alcanzar por nuestro volumen se registraría como portal
# que no publica. **La fuente que se observa no se castiga.**
# ══════════════════════════════════════════════════════════════════════════════
PAUSA_ENTRE_PETICIONES = 1.2      # segundos
PAUSA_TRAS_FALLO = 20.0           # ceder el paso si la fuente empieza a cortar
MAX_FALLOS_SEGUIDOS = 3           # y detenerse antes de insistir
_ULTIMA_PETICION = [0.0]


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s))
                if unicodedata.category(c) != "Mn").upper()
    return " ".join(s.split())


def _get(endpoint: str, params: dict, timeout: int = 45):
    """Transporte por `curl`: el cliente TLS de Python no logra el saludo con este
    host (verificado el 2026-08-12 — `requests` y `urllib` dan reset donde `curl`
    devuelve 200). Devuelve `None` SÓLO si no se alcanzó la fuente."""
    espera = PAUSA_ENTRE_PETICIONES - (time.time() - _ULTIMA_PETICION[0])
    if espera > 0:
        time.sleep(espera)
    _ULTIMA_PETICION[0] = time.time()

    _RED["intentos"] += 1
    url = f"{API}/{endpoint}?" + urllib.parse.urlencode(params)
    try:
        r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), "-A", UA,
                            "-H", "Accept: application/json", url],
                           capture_output=True, timeout=timeout + 15)
        if r.returncode != 0 or not r.stdout:
            raise RuntimeError((r.stderr or b"").decode("utf-8", "replace")[:120] or "vacío")
        _RED["seguidos"] = 0
        return json.loads(r.stdout.decode("utf-8", "replace"))
    except Exception as e:
        _RED["fallos"] += 1
        _RED["seguidos"] = _RED.get("seguidos", 0) + 1
        _RED["ultimo_error"] = f"{type(e).__name__}: {e}"
        if _RED["seguidos"] >= MAX_FALLOS_SEGUIDOS:
            # Insistir contra una fuente que ya cortó tres veces no consigue el
            # dato y sí empeora el bloqueo. Se cede el paso y se declara.
            _RED["detenido_por_ritmo"] = True
        else:
            time.sleep(PAUSA_TRAS_FALLO)
        return None


def por_comprador(anio: int, comprador: str, max_pag: int = 40) -> list[dict]:
    out, pag = [], 1
    while pag <= max_pag:
        if _RED.get("detenido_por_ritmo"):
            break
        d = _get("search_ocds", {"year": anio, "search": "", "buyer": comprador, "page": pag})
        if d is None:
            break
        out.extend(d.get("data", []))
        if pag >= int(d.get("pages", 1) or 1):
            break
        pag += 1
    return out


def capturar(anio: int) -> dict:
    unicos: dict[str, dict] = {}
    esperados = {_norm(n) for ns in COMPRADORES.values() for n in ns}
    descartados = 0

    for entidad, nombres in COMPRADORES.items():
        if _RED.get("detenido_por_ritmo"):
            break
        for nombre in nombres:
            for it in por_comprador(anio, nombre):
                # El filtro `buyer` de la API no es exacto: se revalida en casa.
                if _norm(it.get("buyer", "")) not in esperados:
                    descartados += 1
                    continue
                oc = it.get("ocid")
                if oc and oc not in unicos:
                    unicos[oc] = {**it, "_entidad_quira": entidad,
                                  "_consultado_como": nombre}
    regs = sorted(unicos.values(), key=lambda x: x.get("ocid") or "")
    estado = "captura_fallida" if (_RED["fallos"] and not regs) else (
        "parcial_con_fallos" if _RED["fallos"] else "completa")
    return {"anio": anio, "estado_captura": estado, "n_procesos": len(regs),
            "descartados_por_comprador_ajeno": descartados, "procesos": regs}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anios", default="2025,2026")
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    if not shutil.which("curl"):
        print("[XX] falta `curl`: es el único transporte que este host acepta.")
        sys.exit(2)

    print("SERCOP · HOLDING MUNICIPAL DE MONTECRISTI · captura por comprador\n")
    salida = {"_meta": {"generado": "2026-08-12", "fuente": API,
                        "metodo": "search_ocds por buyer · unión y deduplicación por ocid",
                        "advertencia": "`search` por palabra clave captura <1/3 — no usar"},
              "anios": {}}
    for a in [int(x) for x in args.anios.split(",")]:
        r = capturar(a)
        salida["anios"][str(a)] = r
        if r["estado_captura"] == "captura_fallida":
            print(f"  {a}: ✗ CAPTURA FALLIDA — no se alcanzó la fuente. "
                  f"NO significa que no existan procesos.")
            continue
        from collections import Counter
        ent = Counter(p["_entidad_quira"] for p in r["procesos"])
        con_part = sum(1 for p in r["procesos"] if p.get("partida"))
        print(f"  {a}: {r['n_procesos']:4} procesos únicos "
              f"({r['estado_captura']}) · descartados por comprador ajeno: "
              f"{r['descartados_por_comprador_ajeno']}")
        for e, n in ent.most_common():
            print(f"        {e:26} {n:4}")

    salida["_meta"]["transporte"] = dict(_RED)
    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} peticiones no alcanzaron la fuente")

    if args.escribir:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  → {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
