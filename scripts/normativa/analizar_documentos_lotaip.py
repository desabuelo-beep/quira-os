# -*- coding: utf-8 -*-
"""
scripts/normativa/analizar_documentos_lotaip.py — abrir los documentos, por fin
═══════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-18). Javo desarmó el monitoreo entero:

> *«Creo tu análisis sigue siendo ambiguo y general. […] Sabes que la norma manda
> a publicar las sesiones de concejo, no solo los resúmenes. […] Y con ello
> revisar todos los documentos del GAD —Excel, PDF, etc.— de los links para
> determinar su cumplimiento. Estás dejando de lado las normas, solo por encima,
> y eso es integral.»*

Tenía razón y el reparo es grave. Se descargaron 936 archivos, se comprobaron
417 enlaces… y **no se abrió un solo documento**. Se contaron columnas, fechas y
periodicidades: el envase. El cumplimiento vive dentro del PDF que cuelga del
enlace, y ahí no había mirado nadie.

LO QUE LA PRIMERA LECTURA YA DEMOSTRÓ, en el art. 24 (actas del Concejo):

  · La norma exige *«Enlace para ver y descargar **el acta**»*. Lo publicado es
    un **certificado de resoluciones** de una a cinco páginas: 16 de 16 empiezan
    por «RESOLUCIONES DE LA SESIÓN…». El acta íntegra no aparece nunca.
  · El propio documento **acredita que el acta existe**: una de sus resoluciones
    es «Aprobar el Acta de Sesión Ordinaria Nro. 099». Se publica la constancia
    de que el acta fue aprobada, no el acta.
  · El campo `Tipo` del conjunto de datos dice siempre «Resolución Legislativa»,
    cuando la guía exige **«Tipo de sesión: ordinaria o extraordinaria»**. El
    dato correcto está dentro del PDF, no en el metadato que se publica.
  · Las sesiones llevan **numeración correlativa** (112, 113, 114…), de modo que
    un salto en la serie señala una sesión cuya documentación no se publicó.

QUÉ HACE ESTE MÓDULO. Descarga el documento que cada fila enlaza, extrae su
texto y lo confronta con lo que la norma pide para ese numeral: clase de acto,
correlativo, correspondencia entre el metadato y el documento.

QUÉ NO HACE. No transcribe imágenes: un acta escaneada se declara
`no_procesable` —hay 123 así— porque el OCR exige presupuesto que este proyecto
no tiene, y **fingir que se leyó lo que no se leyó sería el peor error posible**.
Tampoco califica jurídicamente: produce hechos verificables y hallazgos.

Uso:  python scripts/normativa/analizar_documentos_lotaip.py [--numeral "Art. 24"] [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import io
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
DOCS = RAIZ / "data" / "lotaip" / "documentos"
SALIDA = RAIZ / "data" / "lotaip" / "documentos.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAUSA = 0.4
_RED = {"intentos": 0, "fallos": 0, "seguidos": 0}
MAX_FALLOS_SEGUIDOS = 8

# Clases de acto administrativo que la norma distingue. NO son sinónimos: el acta
# recoge el desarrollo íntegro de la sesión —debate, intervenciones, votación—;
# la resolución es sólo su producto. Publicar una en lugar de la otra cambia
# radicalmente lo que el ciudadano puede verificar.
_CLASES = [
    ("acta_de_sesion", r"^\s*ACTA\b|ACTA\s+DE\s+(LA\s+)?SESI[ÓO]N\s+N"),
    ("resoluciones_de_sesion", r"RESOLUCIONES\s+DE\s+LA\s+SESI[ÓO]N"),
    ("resolucion_administrativa", r"RESOLUCI[ÓO]N\s+ADMINISTRATIVA"),
    ("ordenanza", r"\bORDENANZA\b"),
    ("convocatoria", r"CONVOCATORIA\s+A\s+SESI[ÓO]N"),
]


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").upper()
    return " ".join(s.split())


def _descargar(url: str, destino: Path) -> str | None:
    """Nextcloud sirve el visor en `/s/XXXX` y el archivo en `/s/XXXX/download`.
    Pedir la primera forma y darla por documento fue el error del 17-ago."""
    if destino.exists() and destino.stat().st_size > 0:
        return "cache"
    time.sleep(PAUSA)
    _RED["intentos"] += 1
    u = url.rstrip("/")
    if "/index.php/s/" in u and not u.endswith("/download"):
        u += "/download"
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "45", "-A", UA,
             "--max-filesize", "40000000", "-o", str(destino),
             "-w", "%{http_code}|%{content_type}", u],
            capture_output=True, timeout=70)
        code, tipo = r.stdout.decode("utf-8", "replace").strip().split("|", 1)
        if code != "200":
            _RED["fallos"] += 1
            _RED["seguidos"] += 1
            destino.unlink(missing_ok=True)
            return None
        _RED["seguidos"] = 0
        return tipo.split(";")[0]
    except Exception:
        _RED["fallos"] += 1
        _RED["seguidos"] += 1
        destino.unlink(missing_ok=True)
        return None


def _texto_pdf(p: Path) -> tuple[str, int, bool]:
    """Devuelve (texto, páginas, es_imagen).

    `es_imagen` cuando el PDF apenas rinde texto por página: son escaneos. No se
    intenta OCR — se declara y punto."""
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            n = len(pdf.pages)
            t = "\n".join((pg.extract_text() or "") for pg in pdf.pages[:40])
    except Exception:
        return "", 0, False
    return t, n, (n > 0 and len(t.strip()) / n < 120)


def _clase(texto: str) -> str:
    t = _norm(texto)[:1200]
    for nombre, pat in _CLASES:
        if re.search(pat, t):
            return nombre
    return "no_identificado"


def _correlativo(texto: str) -> int | None:
    """Nro. de sesión. La serie es correlativa y sus saltos son verificables."""
    m = re.search(r"SESI[ÓO]N\s+(?:ORDINARIA|EXTRAORDINARIA)\s+N[roº°.\s]*(\d{1,4})",
                  _norm(texto)[:600])
    return int(m.group(1)) if m else None


def _tipo_sesion(texto: str) -> str | None:
    t = _norm(texto)[:600]
    if "SESION EXTRAORDINARIA" in t:
        return "extraordinaria"
    if "SESION ORDINARIA" in t:
        return "ordinaria"
    return None


def _filas_con_enlace(ruta: Path) -> tuple[list[str], list[tuple[list[str], str]]]:
    crudo = ruta.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1252", "cp850", "latin-1"):
        try:
            txt = crudo.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        return [], []
    filas = [f for f in csv.reader(io.StringIO(txt), delimiter=";")
             if any((c or "").strip() for c in f)]
    if not filas:
        return [], []
    fuera = []
    for f in filas[1:]:
        u = next((x for c in f for x in re.findall(r"https?://[^\s;,\"']+", c or "")), None)
        if u:
            fuera.append((f, u))
    return [c.strip() for c in filas[0]], fuera


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--numeral", default="Art. 24")
    ap.add_argument("--limite", type=int, default=0)
    ap.add_argument("--json", help="ruta donde volcar el análisis")
    args = ap.parse_args()

    DOCS.mkdir(parents=True, exist_ok=True)
    idx = json.loads(INDICE.read_text(encoding="utf-8"))["archivos"]
    # ⚠️ INSENSIBLE A CAJA (2026-08-18). El filtro decía `"onjunto" in archivo` y el
    # portal publica tanto `Conjunto de datos` como `CONJUNTO DE DATOS`: se perdían
    # 121 archivos de nueve numerales. El Art. 24 no se vio afectado —por eso su
    # análisis sigue siendo válido— pero el resto del universo quedaba invisible.
    objetivo = [r for r in idx
                if r["numeral"].startswith(args.numeral)
                and "onjunto" in r["archivo"].lower() and r.get("ruta")]

    print(f"DOCUMENTOS ENLAZADOS · {args.numeral} · {len(objetivo)} conjuntos de datos")
    print("se abre el documento, no sólo el registro que lo anuncia\n")

    registros: list[dict] = []
    for r in sorted(objetivo, key=lambda x: (x["anio"], x["mes"])):
        cab, filas = _filas_con_enlace(RAIZ / r["ruta"])
        # La sección se lee del nombre del archivo: el art. 24 reparte
        # resoluciones y actas en ficheros distintos.
        seccion = ("actas" if "cta" in _norm(r["archivo"]).lower()
                   else "resoluciones")
        for k, (f, u) in enumerate(filas, 1):
            if args.limite and len(registros) >= args.limite:
                break
            if _RED["seguidos"] >= MAX_FALLOS_SEGUIDOS:
                registros.append({"anio": r["anio"], "mes": r["mes"],
                                  "seccion": seccion, "url": u,
                                  "estado": "no_intentado_por_corte_de_fuente"})
                continue
            destino = DOCS / f"{_norm(args.numeral).replace(' ', '')}_{r['anio']}{r['mes']:02d}_{seccion}_{k}.bin"
            tipo = _descargar(u, destino)
            if tipo is None:
                registros.append({"anio": r["anio"], "mes": r["mes"],
                                  "seccion": seccion, "url": u,
                                  "estado": "no_accesible"})
                continue

            declarado = {cab[i]: (f[i] if i < len(f) else "")
                         for i in range(min(len(cab), len(f)))}
            reg = {"anio": r["anio"], "mes": r["mes"], "seccion": seccion,
                   "url": u, "content_type": tipo,
                   "bytes": destino.stat().st_size,
                   "declarado": declarado, "estado": "descargado"}

            if tipo == "application/pdf" or destino.read_bytes()[:4] == b"%PDF":
                texto, paginas, es_img = _texto_pdf(destino)
                reg.update({"paginas": paginas, "caracteres": len(texto.strip()),
                            "es_imagen": es_img,
                            "clase_documento": _clase(texto) if not es_img else "no_procesable",
                            "correlativo": _correlativo(texto),
                            "tipo_sesion_en_documento": _tipo_sesion(texto),
                            "primera_linea": " ".join(
                                (texto.strip().splitlines() or [""])[0].split())[:130]})
                if es_img:
                    reg["nota"] = ("el documento es un escaneo: no se transcribe. "
                                   "No se afirma nada sobre su contenido.")
            else:
                reg["clase_documento"] = "formato_no_analizado"
            registros.append(reg)

    # ── informe ───────────────────────────────────────────────────────────────
    ok = [x for x in registros if x.get("estado") == "descargado"]
    print(f"  {len(ok)}/{len(registros)} documentos descargados y abiertos\n")

    print("  CLASE DE ACTO PUBLICADO (lo que dice el documento, no el registro)")
    for k, v in Counter(x.get("clase_documento") for x in ok).most_common():
        print(f"     {str(k):32} {v:4}")

    # Acta vs resolución en la sección que la norma reserva a las actas.
    actas = [x for x in ok if x["seccion"] == "actas"]
    if actas:
        c = Counter(x.get("clase_documento") for x in actas)
        print(f"\n  SECCIÓN «ACTAS DE LAS SESIONES» · {len(actas)} documentos")
        print(f"     la guía exige: «Enlace para ver y descargar el acta»")
        for k, v in c.most_common():
            marca = "  ← es el acta" if k == "acta_de_sesion" else "  ← NO es el acta"
            print(f"     {str(k):32} {v:4}{marca}")

    # Correspondencia entre el metadato publicado y el documento.
    discrepan = [x for x in ok
                 if x.get("tipo_sesion_en_documento")
                 and _norm(json.dumps(x.get("declarado", {}), ensure_ascii=False))
                 and x["tipo_sesion_en_documento"] not in
                 _norm(json.dumps(x.get("declarado", {}), ensure_ascii=False)).lower()]
    if discrepan:
        print(f"\n  METADATO vs DOCUMENTO · {len(discrepan)} filas donde el conjunto de")
        print("     datos no declara el tipo de sesión que el documento acredita")
        for x in discrepan[:5]:
            dec = x["declarado"].get("Tipo") or "—"
            print(f"     {x['anio']}-{x['mes']:02d}  CSV «{dec[:28]}» · "
                  f"documento «sesión {x['tipo_sesion_en_documento']}»")

    # Serie correlativa: un salto es una sesión sin documentación publicada.
    nums = sorted(x["correlativo"] for x in ok if x.get("correlativo"))
    if len(nums) > 2:
        faltan = [n for n in range(nums[0], nums[-1] + 1) if n not in set(nums)]
        print(f"\n  SERIE DE SESIONES · de la {nums[0]} a la {nums[-1]} · "
              f"{len(set(nums))} publicadas")
        if faltan:
            print(f"     sin documentación publicada: {faltan}")
            print("     (la numeración es correlativa: el salto es verificable)")

    img = [x for x in ok if x.get("es_imagen")]
    if img:
        print(f"\n  ⚠ {len(img)} documentos son escaneos sin texto: no se transcriben "
              f"ni se afirma nada de su contenido")
    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} descargas no alcanzaron la fuente")

    if args.json:
        p = Path(args.json)
        # ⚠️ EL TOPE SE DECLARA (2026-08-19). Sin esta marca, un análisis cortado
        # por `--limite` produce un archivo idéntico a uno completo: mismo nombre,
        # misma forma, y el sistema lo daría por revisado. Este dominio ya pagó
        # ese error tres veces —«390 artefactos» era una resta, «24 escaneos» eran
        # referencias, «94 documentos» era un tope de tamaño—: un resultado
        # parcial que no se declara parcial es un resultado falso.
        p.write_text(json.dumps({"_meta": {
            "numeral": args.numeral, "transporte": dict(_RED),
            "generado": _dt.date.today().isoformat(),
            "conjuntos_de_datos": len(objetivo),
            "limite_aplicado": args.limite or None,
            # ⚠️ «Completo» tiene DOS enemigos, no uno. El tope pedido por quien
            # invoca, y el corte automático que se dispara cuando la fuente deja
            # de responder. La primera versión sólo miraba el primero: el
            # Numeral 10 salió con `completo: true` y 7 documentos jamás
            # intentados (2026-08-19). Un análisis que se detuvo solo no puede
            # declararse completo por no haber recibido la orden de detenerse.
            "completo": (not args.limite
                         and _RED["seguidos"] < MAX_FALLOS_SEGUIDOS),
            "no_intentados": sum(
                1 for r in registros
                if r.get("estado") == "no_intentado_por_corte_de_fuente"),
            "corte_por_fuente_caida": _RED["seguidos"] >= MAX_FALLOS_SEGUIDOS,
            "regla": "se abre el documento enlazado; un escaneo se declara "
                     "no_procesable en vez de suponer su contenido",
        }, "documentos": registros}, ensure_ascii=False, indent=1), encoding="utf-8")
        # Se acepta ruta relativa: el agente la invoca desde la raíz del
        # proyecto y `relative_to` reventaba el proceso DESPUÉS de haber escrito
        # el análisis — un fallo reportado sobre trabajo ya hecho (2026-08-19).
        print(f"\n  → {p.relative_to(RAIZ) if p.is_absolute() else p}")


if __name__ == "__main__":
    main()
