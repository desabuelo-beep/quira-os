# -*- coding: utf-8 -*-
"""
scripts/normativa/verificar_enlaces_lotaip.py — E5 · trazabilidad hasta la evidencia
════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Los conjuntos de datos LOTAIP casi nunca contienen el
documento: contienen **un enlace al documento**. El campo se llama, literalmente,
«Enlace para descargar el registro…», «Enlace para ver y descargar el acta». De modo
que un CSV impecable puede apuntar a mil enlaces rotos y el análisis de contenido lo
daría por bueno: **la fila existe, el respaldo no**.

LA REGLA DE JAVO, que aquí se vuelve operativa (2026-08-17):

> *«La información que esté linkeada y mande a revisar fuera de transparencia de la
> DPE, siempre y cuando esté alojada en la WEB del GAD, es información oficial.»*

Por eso un enlace no se clasifica como «externo» o «interno», sino por **procedencia
institucional**: el dominio del sujeto obligado y los portales del Estado son evidencia
oficial; un dominio privado o desconocido es otra cosa y se registra aparte. Los 629
enlaces que un informe anterior llamó «a terceros» eran, en su mayoría, SERCOP, la
Asamblea Nacional, el CPCCS y el Banco Central.

QUÉ REGISTRA. Por URL única —se deduplica, porque el mismo respaldo se enlaza en
muchos meses—: código HTTP, tipo de contenido, tamaño, procedencia institucional y si
lo que responde **es el documento o la aplicación web**, que no es lo mismo.

QUÉ NO HACE: no abre el documento ni juzga su contenido; no convierte un enlace roto
en incumplimiento. Un 404 de hoy no prueba que el documento nunca existió — prueba que
hoy no es verificable, que es justo lo que QUIRA certifica.

⚠️ Si esto falla en bloque, lo primero que se descarta es el instrumento, no la fuente
(OBS-030).

Uso:  python scripts/normativa/verificar_enlaces_lotaip.py [--limite 0] [--solo-gad]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

# ── El sujeto observado no vive aquí ────────────────────────────────────────────
# OBS-032: la identidad del GAD estaba escrita a mano en once puntos. Ahora se
# recibe; el instrumento no la contiene. Si mañana esto corre sobre el GAD 002,
# no se edita este archivo: se declara otro perfil.
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from app.agents import sujeto as _S                       # noqa: E402
INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
SALIDA = RAIZ / "data" / "lotaip" / "enlaces.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAUSA = 0.35
MAX_FALLOS_SEGUIDOS = 8
_TMP = str(RAIZ / "data" / "lotaip" / ".enlace.tmp")
_RED = {"intentos": 0, "fallos": 0, "seguidos": 0, "ultimo": ""}

# Taxonomía de procedencia. NO es «propio vs ajeno»: es qué institución respalda el
# documento. Un acta en el nube del GAD y un proceso en SERCOP son ambos evidencia
# oficial, de emisores distintos.
INSTITUCIONES = [
    (_S.dominio_web(), f"{_S.nombre_corto()} · sujeto obligado"),
    ("compraspublicas.gob.ec", "SERCOP"),
    ("dpe.gob.ec", "Defensoría del Pueblo"),
    ("cpccs.gob.ec", "CPCCS"),
    ("asambleanacional.gob.ec", "Asamblea Nacional"),
    ("bce.ec", "Banco Central"),
    ("finanzas.gob.ec", "Ministerio de Finanzas"),
    ("gob.ec", "otro portal del Estado"),
]


def procedencia(url: str) -> str:
    h = (url.split("/")[2].lower() if url.count("/") >= 2 else url.lower())
    for clave, nombre in INSTITUCIONES:
        if clave in h:
            return nombre
    return "dominio no estatal"


def forma_del_enlace(url: str) -> str:
    """Distingue el enlace que un ciudadano puede abrir del que exige sesión.

    El GAD publica sus respaldos en una nube Nextcloud, y no todas sus URLs son
    equivalentes: `/index.php/s/XXXX` es un enlace de **compartición pública**,
    mientras que `/index.php/f/NNN` y `/index.php/apps/files/…` son rutas **internas
    del gestor de archivos**, que devuelven 401 a quien no tiene cuenta.

    Publicar la segunda forma en transparencia activa cumple la apariencia —la celda
    trae un enlace al dominio oficial— pero **no entrega el documento a la persona que
    ejerce el derecho de acceso**. La distinción es del enlace, no del servidor: por
    eso se registra como forma, y el resultado HTTP se comprueba igual."""
    u = url.lower()
    if "/index.php/s/" in u or "/s/" in u.split("index.php")[-1][:4]:
        return "comparticion_publica"
    if "/index.php/f/" in u or "/apps/files" in u or "/remote.php" in u:
        return "ruta_interna_requiere_sesion"
    return "url_directa"


def comprobar(url: str, timeout: int = 30) -> dict:
    time.sleep(PAUSA)
    _RED["intentos"] += 1
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA,
             "--max-filesize", "3000000", "-o", _TMP,
             "-w", "%{http_code}|%{size_download}|%{content_type}|%{url_effective}",
             url],
            capture_output=True, timeout=timeout + 15)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or b"").decode("utf-8", "replace")[:80])
        code, size, tipo, final = (r.stdout.decode("utf-8", "replace")
                                   .strip().split("|", 3))
    except Exception as e:
        _RED["fallos"] += 1
        _RED["seguidos"] += 1
        _RED["ultimo"] = f"{type(e).__name__}: {e}"
        return {"estado": "no_verificable", "detalle": _RED["ultimo"],
                "nota": "no se alcanzó el servidor — NO significa que falte el documento"}

    _RED["seguidos"] = 0
    code = int(code or 0)
    d = {"http": code, "bytes": int(size or 0), "tipo": tipo.split(";")[0],
         "redirigido_a": final if final != url else None}
    if code != 200:
        d["estado"] = ("enlace_roto" if code in (404, 410)
                       else "acceso_restringido" if code in (401, 403)
                       else "respuesta_inesperada")
        return d
    try:
        ini = Path(_TMP).read_bytes()[:400].lstrip().lower()
        es_html = ini.startswith(b"<!doctype html") or b"<html" in ini[:200]
    except Exception:
        es_html = False

    if not es_html:
        d["estado"] = "accesible"
        return d

    # ⚠️ HTML NO significa «no hay documento». La nube del GAD es un Nextcloud: la URL
    # de compartición `/s/XXXX` devuelve **el visor** por diseño, y el archivo cuelga
    # de `/download`. Clasificar el visor como fallo daba «0 de 430 enlaces accesibles»
    # —falso, y del mismo linaje que OBS-030: culpar a la fuente por un defecto del
    # instrumento—. Antes de dar por perdido un enlace, se agota la forma de pedirlo.
    if forma_del_enlace(url) == "comparticion_publica":
        d2 = _pedir_crudo(url.rstrip("/") + "/download", timeout)
        if d2 and d2.get("http") == 200 and "html" not in d2.get("tipo", ""):
            d.update({"estado": "accesible", "via": "/download",
                      "tipo_documento": d2["tipo"], "bytes": d2.get("bytes", 0)})
            return d

    # Un enlace a la RAÍZ de un portal no permite llegar a la evidencia: manda al
    # ciudadano a buscarla. Es distinto de un enlace roto y se registra aparte.
    resto = url.split("//", 1)[-1]
    camino = resto.split("/", 1)[1] if "/" in resto else ""
    if len(camino.strip("/")) < 24 and not re.search(r"\d{4,}", camino):
        d["estado"] = "enlace_generico_al_portal"
        d["nota"] = "no apunta a un documento identificable, sino a la raíz del sitio"
        return d

    d["estado"] = "responde_pagina_no_documento"
    return d


def _pedir_crudo(url: str, timeout: int) -> dict | None:
    """Segundo intento con otra forma de la misma URL. No cuenta como fallo de red."""
    time.sleep(PAUSA)
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA,
             "--max-filesize", "3000000", "-o", _TMP,
             "-w", "%{http_code}|%{size_download}|%{content_type}", url],
            capture_output=True, timeout=timeout + 15)
        code, size, tipo = r.stdout.decode("utf-8", "replace").strip().split("|", 2)
        return {"http": int(code or 0), "bytes": int(size or 0),
                "tipo": tipo.split(";")[0]}
    except Exception:
        return None


def recolectar() -> dict[str, list]:
    """Junta las URLs de todos los conjuntos de datos, deduplicadas.

    El mismo respaldo se enlaza mes tras mes; comprobar cada repetición multiplicaría
    las peticiones sin añadir una sola prueba nueva."""
    idx = json.loads(INDICE.read_text(encoding="utf-8"))["archivos"]
    urls: dict[str, list] = defaultdict(list)
    for r in idx:
        if not r.get("ruta"):
            continue
        p = RAIZ / r["ruta"]
        if not p.exists():
            continue
        crudo = p.read_bytes()
        for enc in ("utf-8-sig", "utf-8", "cp1252", "cp850", "latin-1"):
            try:
                txt = crudo.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            continue
        for u in re.findall(r"https?://[^\s;,\"'<>\]\)]+", txt):
            u = u.rstrip(".,;)")
            urls[u].append({"anio": r["anio"], "mes": r["mes"],
                            "numeral": r["numeral"], "archivo": r["archivo"]})
    return urls


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limite", type=int, default=0, help="0 = todos")
    ap.add_argument("--solo-gad", action="store_true")
    args = ap.parse_args()

    urls = recolectar()
    if args.solo_gad:
        # Cualquier dominio del sujeto, no sólo el principal: su Nextcloud
        # también es publicación propia (OBS-032).
        urls = {u: v for u, v in urls.items()
                if any(d in u for d in _S.dominios())}
    claves = sorted(urls)
    if args.limite:
        claves = claves[:args.limite]

    total_ref = sum(len(v) for v in urls.values())
    print(f"ENLACES LOTAIP · {len(claves)} URLs únicas "
          f"({total_ref} referencias en los conjuntos de datos)\n")
    print("  procedencia institucional de las URLs únicas:")
    for k, v in Counter(procedencia(u) for u in claves).most_common():
        print(f"     {k:38} {v:5}")
    print()

    previo = {}
    if SALIDA.exists():
        previo = {e["url"]: e for e in
                  json.loads(SALIDA.read_text(encoding="utf-8"))["enlaces"]}

    out = []
    for i, u in enumerate(claves, 1):
        if u in previo and previo[u].get("estado") not in (None, "no_verificable"):
            out.append(previo[u])
            continue
        if _RED["seguidos"] >= MAX_FALLOS_SEGUIDOS:
            out.append({"url": u, "procedencia": procedencia(u),
                        "estado": "no_intentado_por_corte_de_fuente",
                        "referencias": len(urls[u])})
            continue
        d = comprobar(u)
        d.update({"url": u, "procedencia": procedencia(u),
                  "forma": forma_del_enlace(u),
                  "referencias": len(urls[u]),
                  "citado_en": urls[u][:4]})
        out.append(d)
        if i % 100 == 0:
            print(f"   {i}/{len(claves)} · fallos {_RED['fallos']}", flush=True)

    print("\n  RESULTADO por estado")
    for k, v in Counter(e.get("estado") for e in out).most_common():
        print(f"     {k:34} {v:5}")

    print("\n  RESULTADO por procedencia institucional")
    tabla: dict[str, Counter] = defaultdict(Counter)
    for e in out:
        tabla[e["procedencia"]][e.get("estado")] += 1
    for inst in sorted(tabla, key=lambda x: -sum(tabla[x].values())):
        c = tabla[inst]
        ok = c.get("accesible", 0)
        print(f"     {inst:38} {ok:4}/{sum(c.values()):4} accesibles"
              f"   {dict((k, v) for k, v in c.most_common() if k != 'accesible')}")

    gad = [e for e in out if "sujeto obligado" in e["procedencia"]]
    if gad:
        print("\n  FORMA DE LOS ENLACES DEL SUJETO OBLIGADO")
        print("     un enlace al dominio oficial que exige sesión no entrega el")
        print("     documento a quien ejerce el derecho de acceso")
        for f, n in Counter(e.get("forma") for e in gad).most_common():
            ok = sum(1 for e in gad if e.get("forma") == f
                     and e.get("estado") == "accesible")
            print(f"     {f:32} {n:5} URLs · {ok:5} accesibles")

    # C5c · inteligibilidad. Un acta escaneada como imagen es accesible y NO es
    # procesable: nadie puede buscar en ella, agregarla ni cruzarla. El Instructivo
    # sólo reconoce como datos abiertos los formatos no propietarios estructurados.
    docs = Counter(e.get("tipo_documento") or e.get("tipo")
                   for e in out if e.get("estado") == "accesible")
    if docs:
        print("\n  FORMATO DEL DOCUMENTO AL QUE SE LLEGA (C5c · inteligibilidad)")
        img = sum(v for k, v in docs.items() if str(k).startswith("image/"))
        for k, v in docs.most_common(8):
            marca = "  ← imagen: no procesable" if str(k).startswith("image/") else ""
            print(f"     {str(k):34} {v:5}{marca}")
        if img:
            print(f"     → {img} documentos llegan como imagen escaneada")

    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} no alcanzaron el servidor")
        print("    Antes de leerlo como enlace roto: descartar el instrumento (OBS-030).")

    SALIDA.write_text(json.dumps(
        {"_meta": {"generado": "2026-08-17", "transporte": dict(_RED),
                   "urls_unicas": len(claves), "referencias": total_ref,
                   "regla": "enlace alojado en el dominio del GAD = información "
                            "oficial (Javo, 2026-08-17)",
                   "limite": "un enlace roto hoy no prueba que el documento nunca "
                             "existió: prueba que hoy no es verificable"},
         "enlaces": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  → {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
