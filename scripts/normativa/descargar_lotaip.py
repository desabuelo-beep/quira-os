# -*- coding: utf-8 -*-
"""
scripts/normativa/descargar_lotaip.py — traer la evidencia, sin juzgarla todavía
════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). La medición de periodicidad dejó a 2026 con 21 de 22
numerales cumpliendo. Ese resultado prueba **publicación**, no contenido: un numeral
puede figurar en verde con la tríada subida y hueca. El colega lo fijó así:

> *«Ahí sí vamos a saber si ese espectacular 21/22 de 2026 representa cumplimiento
> sustantivo o solamente cumplimiento de publicación.»*

Este módulo es el primer eslabón de esa segunda capa probatoria, y hace **una sola
cosa**: traer los 936 archivos y demostrar su integridad. No lee campos, no aplica la
regla de ausencia, no concluye. Separar la descarga del juicio es deliberado: si el
análisis se equivoca, se rehace sobre la misma evidencia sin volver a golpear la fuente.

LO QUE REGISTRA POR ARCHIVO

    sha256      la evidencia queda fijada: cualquier análisis posterior es auditable
    bytes       y se contrasta con los que declaró el índice del portal
    estado      descargado · no_alcanzado · no_es_el_documento · discrepancia_de_tamano

RITMO Y RESPETO A LA FUENTE. Pausa entre peticiones y alto a los fallos seguidos. Es
reanudable: lo ya descargado con SHA estable no se vuelve a pedir. **La fuente que se
observa no se castiga** — y una captura a medias se declara, nunca se disimula.

⚠️ Si esto empieza a fallar en bloque, lo primero que hay que descartar es el propio
instrumento, no la fuente (OBS-030: seis días declarando caído un portal que respondía).

QUÉ NO HACE: no interpreta el contenido, no puntúa, no toca la vara normativa
—`exigencias_por_numeral.json` queda congelada durante toda la descarga. Si aparece una
contradicción con la norma, se abre incidencia de corpus; **no se corrige la matriz en
silencio.**

Uso:  python scripts/normativa/descargar_lotaip.py [--anios 2025,2026] [--limite 0]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import datetime as _dt
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
EVIDENCIA = RAIZ / "data" / "lotaip" / "dpe_montecristi.json"

# ── El sujeto observado no vive aquí ────────────────────────────────────────────
# OBS-032: la identidad del GAD estaba escrita a mano en once puntos. Ahora se
# recibe; el instrumento no la contiene. Si mañana esto corre sobre el GAD 002,
# no se edita este archivo: se declara otro perfil.
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from app.agents import sujeto as _S                       # noqa: E402
DESTINO = RAIZ / "data" / "lotaip" / "descargas"
INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
BASE_ARCHIVOS = "https://transparencia.dpe.gob.ec/backend/v1/transparency"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAUSA = 0.5
MAX_FALLOS_SEGUIDOS = 5
PAUSA_TRAS_FALLO = 15.0
_RED = {"intentos": 0, "fallos": 0, "seguidos": 0, "ultimo": ""}


def _slug(s: str, n: int = 60) -> str:
    """Nombre de carpeta seguro en Windows conservando lo identificable.

    ⚠️ EL FINAL DEL NOMBRE ES LO QUE DISTINGUE. Los tres archivos de la tríada sólo se
    diferencian en su sufijo —`…febrero-2025(conjuntoDatos).csv`, `(metadatos).csv`,
    `(diccionario).csv`— y una versión previa truncaba por el principio: **29 archivos
    de contenido distinto se sobrescribieron entre sí**, con SHA y tamaños distintos.
    Por eso, al recortar, se conserva la cabeza Y la cola."""
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", s)
    s = re.sub(r"\s+", "_", s.strip())
    if len(s) <= n:
        return s or "sin_nombre"
    cola = 26
    return f"{s[:n - cola - 1]}~{s[-cola:]}"


def _descargar(url: str, destino: Path, timeout: int = 60) -> dict:
    """Trae un archivo y prueba que es el archivo.

    Un 200 que devuelve la aplicación web **parece éxito y no lo es**: son 1.489 bytes
    de HTML idénticos para cualquier ruta mal resuelta. Se distingue explícitamente,
    porque registrarlo como documento contaminaría todo el análisis posterior."""
    time.sleep(PAUSA)
    _RED["intentos"] += 1
    tmp = destino.with_suffix(destino.suffix + ".parcial")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA,
             "-H", "Referer: https://transparencia.dpe.gob.ec/",
             "-o", str(tmp), "-w", "%{http_code}", url],
            capture_output=True, timeout=timeout + 20)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or b"").decode("utf-8", "replace")[:90])
        code = int((r.stdout or b"0").decode().strip() or 0)
    except Exception as e:
        _RED["fallos"] += 1
        _RED["seguidos"] += 1
        _RED["ultimo"] = f"{type(e).__name__}: {e}"
        tmp.unlink(missing_ok=True)
        time.sleep(PAUSA_TRAS_FALLO)
        return {"estado": "no_alcanzado", "detalle": _RED["ultimo"]}

    _RED["seguidos"] = 0
    if code != 200:
        tmp.unlink(missing_ok=True)
        return {"estado": "listado_pero_ausente" if code in (404, 410)
                else "respuesta_inesperada", "http": code}

    crudo = tmp.read_bytes()
    cab = crudo.lstrip()[:200].lower()
    if cab.startswith(b"<!doctype html") or b"<html" in cab:
        tmp.unlink(missing_ok=True)
        return {"estado": "no_es_el_documento", "http": 200, "bytes": len(crudo),
                "detalle": "la ruta devolvió la aplicación web, no el archivo"}

    destino.unlink(missing_ok=True)
    tmp.rename(destino)
    return {"estado": "descargado", "http": 200, "bytes": len(crudo),
            "sha256": hashlib.sha256(crudo).hexdigest()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anios", default="2025,2026")
    ap.add_argument("--limite", type=int, default=0, help="0 = todos")
    args = ap.parse_args()

    ev = json.loads(EVIDENCIA.read_text(encoding="utf-8"))
    ent = ev["entidades"][str(_S.entidad_dpe())]

    previo: dict[str, dict] = {}
    if INDICE.exists():
        previo = {r["url"]: r for r in
                  json.loads(INDICE.read_text(encoding="utf-8"))["archivos"]}

    tareas = []
    for anio in [a.strip() for a in args.anios.split(",")]:
        for r in ent["anios"].get(anio, {}).get("registros", []):
            if r.get("url"):
                tareas.append((anio, r))
    if args.limite:
        tareas = tareas[:args.limite]

    print(f"DESCARGA LOTAIP · {len(tareas)} archivos · {ent['nombre']}")
    print("integridad y SHA256. El contenido NO se juzga aquí.\n")

    out: list[dict] = []
    nuevos = saltados = colisiones = 0
    tomadas: dict[str, str] = {}          # ruta → url que la ocupó
    for i, (anio, r) in enumerate(tareas, 1):
        url = r["url"] if r["url"].startswith("http") else BASE_ARCHIVOS + r["url"]
        carpeta = DESTINO / anio / f"{r['mes']:02d}_{_slug(r['numeral'], 34)}"
        ruta = carpeta / _slug(r["archivo"], 70)

        # Cinturón y tirantes: si dos URLs distintas caen en la misma ruta, se
        # desambigua. Una colisión silenciosa no produce un error — produce evidencia
        # equivocada, que es peor, porque el análisis posterior la da por buena.
        clave = str(ruta).lower()
        if tomadas.get(clave, url) != url:
            colisiones += 1
            marca = hashlib.sha256(url.encode()).hexdigest()[:6]
            ruta = ruta.with_name(f"{ruta.stem}__{marca}{ruta.suffix}")
            clave = str(ruta).lower()
        tomadas[clave] = url

        pre = previo.get(url)
        if pre and pre.get("estado") == "descargado" and ruta.exists():
            # Reanudable: se confía en el SHA ya calculado, no se vuelve a pedir.
            out.append(pre)
            saltados += 1
            continue

        if _RED["seguidos"] >= MAX_FALLOS_SEGUIDOS:
            # Insistir contra una fuente que ya cortó cinco veces no consigue el dato
            # y sí empeora el bloqueo. Lo que falta se declara, no se disimula.
            out.append({"url": url, "anio": anio, "mes": r["mes"],
                        "numeral": r["numeral"], "archivo": r["archivo"],
                        "estado": "no_intentado_por_corte_de_fuente"})
            continue

        d = _descargar(url, ruta)
        # Contraste con lo que el propio portal declaró en su índice: una diferencia
        # de tamaño no invalida el archivo, pero **debe quedar registrada**.
        declarados = (r.get("verificacion") or {}).get("bytes")
        if d.get("estado") == "descargado" and declarados and d["bytes"] != declarados:
            d["discrepancia_de_tamano"] = {"indice": declarados, "descargado": d["bytes"]}

        d.update({"url": url, "anio": anio, "mes": r["mes"], "numeral": r["numeral"],
                  "archivo": r["archivo"], "publicado": r.get("publicado"),
                  "ruta": str(ruta.relative_to(RAIZ)).replace("\\", "/")})
        out.append(d)
        nuevos += 1
        if nuevos % 50 == 0:
            print(f"   {i}/{len(tareas)} · nuevos {nuevos} · fallos {_RED['fallos']}",
                  flush=True)

    from collections import Counter
    est = Counter(r.get("estado") for r in out)
    print(f"\n  {nuevos} descargados en esta corrida · {saltados} ya estaban")
    for k, v in est.most_common():
        print(f"     {k:34} {v:4}")
    disc = [r for r in out if r.get("discrepancia_de_tamano")]
    if disc:
        print(f"\n  ⚠ {len(disc)} archivos difieren del tamaño que declaró el índice")
    if colisiones:
        print(f"  ⚠ {colisiones} nombres colisionaban y se desambiguaron por hash de URL")
    rutas = {r.get("ruta") for r in out if r.get("ruta")}
    if len(rutas) != len(out):
        print(f"  [XX] {len(out) - len(rutas)} registros comparten ruta: hay evidencia "
              f"sobrescrita. NO analizar sobre este índice.")
        sys.exit(4)
    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} peticiones no alcanzaron la fuente")
        print("    Antes de leerlo como falta de publicación: descartar el instrumento (OBS-030).")

    INDICE.write_text(json.dumps(
        {"_meta": {"generado": _dt.date.today().isoformat(), "fuente": BASE_ARCHIVOS,
                   "transporte": dict(_RED), "total": len(out),
                   "regla": "integridad y SHA256 · el contenido se juzga aparte",
                   "nota": "los binarios no van al repo: son públicos y reproducibles"},
         "archivos": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  → {INDICE.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
