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
BASE = "https://transparencia.dpe.gob.ec"
API = f"{BASE}/backend/v1/transparency/transparency/active/public"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# El holding en el registro de la Defensoría. `establishment_id` se lee del
# propio portal del sujeto obligado (`window.APP_CONFIG`).
ENTIDADES = {937: "GAD Montecristi"}

MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

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
        cmd += ["-o", "/dev/null", "-w", "%{http_code}|%{size_download}|%{content_type}",
                "-I", "-L"]
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
    url = ruta if ruta.startswith("http") else BASE + ruta
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
        return {"estado": "accesible", "http": 200,
                "bytes": int(size or 0), "tipo": tipo.split(";")[0]}
    if code in (404, 410):
        return {"estado": "listado_pero_ausente", "http": code}
    return {"estado": "respuesta_inesperada", "http": code}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--anios", default="2025,2026")
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
        for anio in [int(x) for x in args.anios.split(",")]:
            registros: list[dict] = []
            meses_con_datos = []
            for m in range(1, 13):
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
            print(f"  {anio}: {len(registros):4} archivos · {len(meses_con_datos):2}/12 meses "
                  f"· {len(nums):2} numerales")
            for k, v in ver.most_common():
                print(f"         {k:24} {v:4}")
            salida["entidades"][str(est)]["anios"][str(anio)] = {
                "n_archivos": len(registros), "meses_con_datos": meses_con_datos,
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
