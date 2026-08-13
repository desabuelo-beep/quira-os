# -*- coding: utf-8 -*-
"""
scripts/normativa/capturar_lotaip_portal.py — el repositorio LOTAIP del GAD, verificado
════════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). `V_LOTAIP` seguía en `sin_evidencia` porque el monitoreo
del portal no se había ejecutado nunca (OBS-029). Este guion lo ejecuta.

CÓMO SE HALLÓ LA FUENTE. El repositorio de `montecristi.gob.ec/transparencia/` se
arma en el navegador, así que no basta con leer el HTML. La configuración vive en
`window.APP_CONFIG` y declara **dos orígenes distintos**:

    years      2019-2026   · lo que el portal ofrece
    localYears 2019-2024   · servido por el propio GAD (`api/local-year.php`)
    2025-2026              · servido por la DPE (`transparencia.dpe.gob.ec`)

QUÉ VERIFICA. No basta con que el portal LISTE un archivo: `V_LOTAIP = 1,0` exige
**documento en URL pública verificable**. Por eso cada URL se comprueba de verdad
—código HTTP, tipo y tamaño— en vez de darla por buena porque aparece en el índice.
Un enlace listado y roto es precisamente el caso que el criterio `0,5` describe.

QUÉ NO HACE:
  · No descarga los documentos. Comprueba que existan y sean alcanzables.
  · No interpreta su contenido ni juzga si la publicación es completa.
  · No convierte un fallo de red en «no publicado» — ADR-042 §6.

Uso:  python scripts/normativa/capturar_lotaip_portal.py [--anios 2023,2024] [--verificar 0]
      (--verificar N comprueba N URLs por año; 0 = todas)
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "data" / "lotaip" / "portal_montecristi.json"

PORTAL = "https://montecristi.gob.ec"
API_LOCAL = f"{PORTAL}/transparencia/api/local-year.php"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

# Fallos de transporte, contados aparte de los resultados. Sin esta separación un
# portal caído se leería como un municipio que no publica.
_RED = {"intentos": 0, "fallos": 0, "ultimo_error": ""}


def _pedir(url: str, timeout: int = 45, solo_cabecera: bool = False):
    """Devuelve (status, cuerpo|None, longitud, tipo) o None si no se alcanzó la fuente."""
    _RED["intentos"] += 1
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        if solo_cabecera:
            req.get_method = lambda: "HEAD"
        with urllib.request.urlopen(req, timeout=timeout, context=_CTX) as r:
            cuerpo = None if solo_cabecera else r.read()
            return (r.status, cuerpo,
                    int(r.headers.get("Content-Length") or (len(cuerpo) if cuerpo else 0)),
                    (r.headers.get("Content-Type") or "").split(";")[0])
    except urllib.error.HTTPError as e:
        # Un 404 SÍ es respuesta del servidor: la fuente contestó, y contestó que no está.
        return (e.code, None, 0, "")
    except Exception as e:
        _RED["fallos"] += 1
        _RED["ultimo_error"] = f"{type(e).__name__}: {e}"
        return None


def indice_anual(anio: int) -> dict | None:
    r = _pedir(f"{API_LOCAL}?year={anio}")
    if r is None or r[0] != 200 or not r[1]:
        return None
    try:
        return json.loads(r[1].decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return None


def _url_absoluta(u: str) -> str:
    """Las rutas del índice son relativas a `/transparencia/`, NO a la raíz del sitio.

    Resolverlas contra la raíz devuelve 404 en todos los archivos, y eso habría
    producido el titular «el GAD publica enlaces rotos» siendo el defecto del
    capturador. Verificado: `…/transparencia/transparencia/2024/…` → HTTP 200,
    27.033 bytes. **Antes de atribuir una carencia a la fuente hay que descartar
    que sea propia** (ADR-042 §6; misma lección que OBS-027)."""
    return u if u.startswith("http") else f"{PORTAL}/transparencia/{u.lstrip('/')}"


def estado_url(url: str) -> dict:
    """El criterio de H13 distingue URL publicada de URL accesible. Aquí se comprueba.

    HEAD primero por cortesía con el servidor; si no lo admite, se reintenta con GET
    —hay servidores que responden 405 a HEAD y sirven el archivo sin problema—."""
    r = _pedir(url, timeout=30, solo_cabecera=True)
    if r is not None and r[0] in (405, 403, 501):
        r = _pedir(url, timeout=30)
    if r is None:
        return {"estado": "no_verificable", "detalle": "no se alcanzó el servidor",
                "advertencia": "fallo de transporte — NO significa que el documento falte"}
    codigo, _, tam, tipo = r
    if codigo == 200:
        return {"estado": "accesible", "http": 200, "bytes": tam, "tipo": tipo}
    if codigo in (404, 410):
        return {"estado": "listado_pero_ausente", "http": codigo}
    return {"estado": "respuesta_inesperada", "http": codigo}


def capturar(anio: int, verificar: int) -> dict:
    d = indice_anual(anio)
    if d is None:
        return {"anio": anio, "estado_captura": "captura_fallida",
                "razon": "el índice del año no se pudo obtener",
                "advertencia": "NO significa que el GAD no publique"}

    literales: list[dict] = []
    for mes in d.get("months", []):
        for it in mes.get("items", []):
            for f in it.get("files", []):
                literales.append({
                    "mes": mes.get("num"), "mes_nombre": mes.get("name"),
                    "literal": it.get("literal"), "descripcion": it.get("description"),
                    "publicado": it.get("published"),
                    "archivo": f.get("name"), "url": _url_absoluta(f.get("url", "")),
                })

    n = len(literales) if verificar == 0 else min(verificar, len(literales))
    for i, reg in enumerate(literales):
        if i < n:
            reg["verificacion"] = estado_url(reg["url"])
            time.sleep(0.08)                       # cortesía con el servidor
        else:
            reg["verificacion"] = {"estado": "no_comprobada",
                                   "detalle": "fuera de la muestra de esta corrida"}

    return {"anio": anio, "estado_captura":
            "parcial_con_fallos" if _RED["fallos"] else "completa",
            "n_archivos": len(literales), "n_verificados": n,
            "meses_con_publicacion": len({r["mes"] for r in literales}),
            "literales_distintos": sorted({r["literal"] for r in literales if r["literal"]}),
            "registros": literales}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anios", default="2023,2024",
                    help="años servidos por el portal del GAD (2019-2024)")
    ap.add_argument("--verificar", type=int, default=0,
                    help="cuántas URLs comprobar por año; 0 = todas")
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    print("REPOSITORIO LOTAIP · portal del GAD Montecristi\n")
    salida = {"_meta": {"generado": "2026-08-12", "fuente": API_LOCAL,
                        "regla": "URL listada ≠ URL accesible · fallo de red ≠ no publicado"},
              "anios": {}}

    for a in [int(x) for x in args.anios.split(",")]:
        r = capturar(a, args.verificar)
        salida["anios"][str(a)] = r
        if r["estado_captura"] == "captura_fallida":
            print(f"  {a}: ✗ CAPTURA FALLIDA — {r['razon']}")
            continue
        from collections import Counter
        c = Counter(x["verificacion"]["estado"] for x in r["registros"])
        print(f"  {a}: {r['n_archivos']:4} archivos · {r['meses_con_publicacion']:2}/12 meses "
              f"· {len(r['literales_distintos']):2} literales")
        for k, v in c.most_common():
            print(f"        {k:22} {v:4}")

    salida["_meta"]["transporte"] = dict(_RED)
    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} peticiones no alcanzaron la fuente "
              f"· último: {_RED['ultimo_error'][:80]}")

    if args.escribir:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  → {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
