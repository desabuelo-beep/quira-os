# -*- coding: utf-8 -*-
"""
scripts/normativa/capturar_lotaip_dpe.py — la transparencia donde la norma la exige
════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). Javo: *«la evaluación de LOTAIP no se debe hacer desde
la web del GAD, sino desde transparencia de la DPE. Ése es el reporte que ellos
hacen con los filtros del Comité de Transparencia, que es quien avala la
información que se reporta mensualmente»*.

El repositorio del propio municipio sirve para **contrastar**; el acto sujeto a
control es el que se registra ante la Defensoría del Pueblo. Evaluar la copia en
lugar del acto era medir el lugar equivocado.

⚠️ SEIS DÍAS SE DIO POR CAÍDA ESTA FUENTE. No lo estaba: una VPN local con MTU
1420 sobre una ruta de ~1300 perdía el saludo TLS (OBS-030). Sin la VPN responde
en **0,4 s**. Queda como advertencia dentro del propio capturador: **si esto deja
de responder, lo primero que hay que descartar es el instrumento.**

QUÉ CAPTURA. Por entidad, año y mes: el numeral LOTAIP, sus archivos, la URL de
descarga y la fecha de publicación — con verificación real de accesibilidad,
porque **una URL listada no es una URL accesible** y el criterio del canon exige
documento verificable, no documento anunciado.

QUÉ NO HACE: no descarga los archivos, no juzga si el contenido cumple, no
convierte una ausencia en incumplimiento.

Uso:  python scripts/normativa/capturar_lotaip_dpe.py [--anios 2025,2026] [--verificar 40]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import unicodedata
import urllib.parse
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "data" / "lotaip" / "dpe_montecristi.json"

# ── El sujeto observado no vive aquí ────────────────────────────────────────────
# OBS-032: la identidad del GAD estaba escrita a mano en once puntos. Ahora se
# recibe; el instrumento no la contiene. Si mañana esto corre sobre el GAD 002,
# no se edita este archivo: se declara otro perfil.
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from app.agents import sujeto as _S                       # noqa: E402
BASE = "https://transparencia.dpe.gob.ec"
API = f"{BASE}/backend/v1/transparency/transparency/active/public"
# Los archivos NO cuelgan de la raíz: la ruta que devuelve el índice es relativa
# a `/backend/v1/transparency`. Resolverla contra la raíz devuelve **HTTP 200 con
# la página de la aplicación** —1.489 bytes de HTML idénticos para todos— y eso
# habría quedado registrado como «documento no accesible» siendo defecto del
# lector. Un 200 que no es el documento es peor que un 404: parece éxito.
BASE_ARCHIVOS = f"{BASE}/backend/v1/transparency"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# El holding en el registro de la Defensoría. `establishment_id` se lee del
# propio portal del sujeto obligado (`window.APP_CONFIG`).
ENTIDADES = {_S.entidad_dpe(): _S.cargar()["identidad_en_fuentes"]["dpe_entidad_nombre"]}

MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

_TMP = str(Path(__file__).resolve().parents[2] / "data" / "lotaip" / ".descarga.tmp")
PAUSA = 0.6
_RED = {"intentos": 0, "fallos": 0, "seguidos": 0, "ultimo": ""}


def _limpiar(s: str) -> str:
    """La API devuelve combinaciones Unicode descompuestas —«AutoÌ?nomos»—.
    Se normaliza a forma compuesta para que el texto sea legible y comparable."""
    return unicodedata.normalize("NFC", str(s or "")).strip()


def _pedir(url: str, timeout: int = 40, cabecera: bool = False):
    time.sleep(PAUSA)
    _RED["intentos"] += 1
    cmd = ["curl", "-sS", "--max-time", str(timeout), "-A", UA,
           "-H", f"Referer: {BASE}/"]
    if cabecera:
        # Ni `-I` ni `-o /dev/null`: en este entorno el combo devuelve rc=23
        # («client returned ERROR on write») aunque el servidor conteste 200 —
        # 120 verificaciones se registraron como fallo de red por eso. Se
        # descarga a un temporal y se leen los encabezados de la respuesta real.
        cmd += ["-L", "-o", _TMP, "-w", "%{http_code}|%{size_download}|%{content_type}"]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 15)
        if r.returncode != 0:
            raise RuntimeError((r.stderr or b"").decode("utf-8", "replace")[:90])
        _RED["seguidos"] = 0
        return r.stdout.decode("utf-8", "replace")
    except Exception as e:
        _RED["fallos"] += 1
        _RED["seguidos"] += 1
        _RED["ultimo"] = f"{type(e).__name__}: {e}"
        return None


def mes(est: int, anio: int, m: int) -> list | None:
    b = _pedir(f"{API}?month={m}&year={anio}&establishment_id={est}")
    if b is None:
        return None
    try:
        d = json.loads(b)
        return d if isinstance(d, list) else []
    except json.JSONDecodeError:
        return None


def estado_url(ruta: str) -> dict:
    """Comprueba de verdad. El criterio del canon distingue documento **en URL
    pública verificable** de URL meramente registrada: son estados distintos y
    sólo una comprobación real los separa."""
    url = ruta if ruta.startswith("http") else BASE_ARCHIVOS + ruta
    r = _pedir(url, timeout=30, cabecera=True)
    if r is None:
        return {"estado": "no_verificable",
                "nota": "no se alcanzó el servidor — NO significa que falte el documento"}
    try:
        code, size, tipo = r.strip().split("|")[:3]
        code = int(code)
    except Exception:
        return {"estado": "respuesta_no_interpretable"}
    if code == 200:
        tipo = tipo.split(";")[0]
        d = {"estado": "accesible", "http": 200, "bytes": int(size or 0), "tipo": tipo}
        # Un 200 que devuelve la aplicación web NO es el documento. Se distingue.
        try:
            ini = open(_TMP, "rb").read(2000)
            if ini.lstrip()[:15].lower().startswith(b"<!doctype html") or b"<html" in ini[:200].lower():
                return {"estado": "responde_pero_no_es_el_documento", "http": 200,
                        "nota": "la ruta devolvió la aplicación web, no el archivo"}
            texto = ini.decode("utf-8", "replace")
            d["primera_linea"] = " ".join(texto.splitlines()[0].split())[:120]
            import re as _re
            m = _re.search(r"(\d{2}/\d{2}/\d{4})", texto[:400])
            if m:
                d["fecha_declarada"] = m.group(1)
        except Exception:
            pass
        return d
    if code in (404, 410):
        return {"estado": "listado_pero_ausente", "http": code}
    return {"estado": "respuesta_inesperada", "http": code}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    # `2025` = los doce meses · `2026:5` = hasta mayo. El corte se declara, no
    # se supone: un año incompleto contado como completo bajaría el cumplimiento
    # de una entidad por meses que aún no debía publicar.
    ap.add_argument("--anios", default="2025,2026:5")
    ap.add_argument("--verificar", type=int, default=40,
                    help="URLs a comprobar por año; 0 = todas")
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args()

    print("REPOSITORIO LOTAIP · Defensoría del Pueblo\n")
    salida = {"_meta": {"generado": "2026-08-17", "fuente": API,
                        "regla": "URL listada ≠ URL accesible · "
                                 "ausencia ≠ incumplimiento"},
              "entidades": {}}

    for est, nombre in ENTIDADES.items():
        salida["entidades"][str(est)] = {"nombre": nombre, "anios": {}}
        for spec in args.anios.split(","):
            anio, _, tope = spec.strip().partition(":")
            anio = int(anio)
            ultimo = int(tope) if tope else 12
            registros: list[dict] = []
            meses_con_datos = []
            for m in range(1, ultimo + 1):
                d = mes(est, anio, m)
                if d is None:
                    continue
                if d:
                    meses_con_datos.append(m)
                for it in d:
                    num = (it.get("numeral") or {})
                    for f in (it.get("files") or []):
                        registros.append({
                            "anio": anio, "mes": m, "mes_nombre": MESES[m],
                            "numeral": _limpiar(num.get("name")),
                            "obligacion": _limpiar(num.get("description")),
                            "archivo": _limpiar(f.get("name")),
                            "descripcion": _limpiar(f.get("description")),
                            "url": f.get("url_download") or "",
                            "publicado": f.get("created_at"),
                        })

            n = len(registros) if args.verificar == 0 else min(args.verificar, len(registros))
            for i, r in enumerate(registros):
                r["verificacion"] = (estado_url(r["url"]) if i < n and r["url"]
                                     else {"estado": "no_comprobada"})

            from collections import Counter
            nums = sorted({r["numeral"] for r in registros if r["numeral"]})
            ver = Counter(r["verificacion"]["estado"] for r in registros)
            print(f"  {anio}: {len(registros):4} archivos · "
                  f"{len(meses_con_datos):2}/{ultimo} meses · {len(nums):2} numerales")
            for k, v in ver.most_common():
                print(f"         {k:24} {v:4}")
            salida["entidades"][str(est)]["anios"][str(anio)] = {
                "n_archivos": len(registros), "meses_evaluados": ultimo,
                "meses_con_datos": meses_con_datos,
                "numerales": nums, "registros": registros}

    salida["_meta"]["transporte"] = dict(_RED)
    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} peticiones no alcanzaron la fuente")
        print("    Antes de leerlo como falta de publicación: descartar el instrumento (OBS-030).")

    if args.escribir:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n  → {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
