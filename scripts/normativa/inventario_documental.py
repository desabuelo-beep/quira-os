# -*- coding: utf-8 -*-
"""
scripts/normativa/inventario_documental.py — qué ES cada artefacto, materialmente
═════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-18). El dominio se declaró cerrado y hubo que reabrirlo el
mismo día. Javo:

> *«No se ha completado el trabajo en este DOM hasta que no se haga el análisis
> completo de todo el universo documental. Este DOM debe quedar impoluto e
> inexpugnable para que pueda nutrir a todo el sistema de QUIRA.»*

Y el colega formuló la regla que este módulo materializa:

> **La existencia de un enlace no acredita la existencia ni la naturaleza del
> documento exigido. La evidencia debe ser inspeccionada materialmente antes de
> ser considerada evidencia del cumplimiento.**

Es más fuerte que «el nombre del enlace no es evidencia», y en d07 quedó probada
tres veces: el campo decía «acta» y había un certificado de resoluciones; decía
«registro de asistencia» y había 260 fotografías de eventos; el banco de pruebas
eligió un corpus de OCR que no era un problema de OCR.

TRES NIVELES QUE NO PUEDEN CONTARSE JUNTOS. Decir «417 documentos» distorsiona,
porque trece de esos enlaces son contenedores con 260 objetos dentro:

    documento lógico publicado   lo que la fila del conjunto de datos declara
    contenedor publicado         el ZIP que el enlace entrega
    artefacto contenido          cada archivo real dentro del contenedor

QUÉ RESPONDE, y sólo esto: **¿qué es físicamente este artefacto?** Extensión real
—no la declarada—, SHA, tamaño, si rinde texto, si es imagen, cuántas páginas,
qué contiene si es contenedor.

QUÉ **NO** RESPONDE, y es la frontera que lo mantiene fuera del canon: si cumple.
La correspondencia entre naturaleza declarada y naturaleza material se registra
como observación; **decidir si eso constituye incumplimiento pertenece a la RO**,
nunca a un inventario. El OCR vive antes del canon, como herramienta de
extracción, y jamás decide la naturaleza jurídica de un documento.

Uso:  python scripts/normativa/inventario_documental.py [--limite 0] [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import datetime as _dt
import json
import subprocess
import sys
import time
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

def _procedencia(etapa: str) -> dict:
    """De quién es este artefacto. Se escribe AL GENERARLO, no después.

    Estamparlo más tarde —desde el sellador de la cadena— cambia el SHA del
    archivo ya medido y hace que las etapas siguientes crean que su insumo
    cambió: se re-ejecutan y la cadena entra en cascada. Costó una corrida
    colgada (2026-08-25). Aquí el archivo nace con su procedencia dentro."""
    try:
        from app.agents import procedencia as _P, sujeto as _S
        return _P.de_generacion(etapa, f"{_S.POR_DEFECTO} {_S.nombre_corto()}",
                                _S.huella())
    except Exception:                                        # noqa: BLE001
        return {"etapa": etapa, "estado": "sujeto_no_acreditado_por_la_cadena"}


RAIZ = Path(__file__).resolve().parents[2]
ENLACES = RAIZ / "data" / "lotaip" / "enlaces.json"
CACHE = RAIZ / "data" / "lotaip" / "artefactos"
SALIDA = RAIZ / "data" / "lotaip" / "inventario_documental.json"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAUSA = 0.35
MAX_FALLOS_SEGUIDOS = 8
_RED = {"intentos": 0, "fallos": 0, "seguidos": 0}

# Firma real del archivo. La extensión y el `content-type` los declara quien
# publica; los primeros bytes no mienten. En d07 apareció un `.zip` que traía
# imágenes y un numeral entero cuyos «documentos» eran fotografías.
_FIRMAS = [
    (b"%PDF", "pdf"),
    (b"\xff\xd8\xff", "jpeg"),
    (b"\x89PNG", "png"),
    (b"PK\x03\x04", "zip"),           # también .xlsx/.docx — se afina abriéndolo
    (b"\xd0\xcf\x11\xe0", "ole"),     # .doc/.xls antiguos
    (b"GIF8", "gif"),
    (b"\x00\x00\x00\x18ftyp", "mp4"),
    (b"\x00\x00\x00\x20ftyp", "mp4"),
]


def firma(datos: bytes) -> str:
    for pre, nombre in _FIRMAS:
        if datos.startswith(pre):
            return nombre
    if datos[4:12] in (b"ftypisom", b"ftypmp42"):
        return "mp4"
    return "desconocido"


def _afinar_zip(p: Path) -> str:
    """Un contenedor `PK` puede ser un ZIP, un .xlsx o un .docx. Se distingue por
    lo que lleva dentro, no por la extensión que le pusieron."""
    try:
        with zipfile.ZipFile(p) as z:
            n = z.namelist()
            if any(x.startswith("xl/") for x in n):
                return "xlsx"
            if any(x.startswith("word/") for x in n):
                return "docx"
            if any(x.startswith("ppt/") for x in n):
                return "pptx"
    except Exception:                                    # noqa: BLE001
        # Un ZIP que no abre puede estar corrupto en origen o TRUNCADO por un
        # límite de descarga nuestro. No es lo mismo: lo primero es un hallazgo
        # sobre el sujeto obligado; lo segundo, un defecto del instrumento.
        return "zip_ilegible"
    return "zip"


# Estados de captura. Todo límite operativo que pueda reducir el universo
# observado DEBE producir un estado explícito, nunca una ausencia silenciosa
# (regla del colega · 2026-08-18). El primer inventario devolvió 94 artefactos
# donde había 935: no mintió, midió un universo truncado por sus propios topes.
CAPTURA_OK = "descargado"
CAPTURA_TOPE = "cortado_por_tope_de_tamano"
CAPTURA_TIEMPO = "cortado_por_tiempo"
CAPTURA_HTTP = "respuesta_no_200"
CAPTURA_CORTE = "no_intentado_por_corte_de_fuente"
CAPTURA_FALLO = "no_alcanzado"

TOPE_BYTES = 500_000_000
TOPE_SEGUNDOS = 300


def descargar(url: str, destino: Path) -> str:
    """Devuelve el ESTADO de captura, no un booleano.

    Un `False` no distingue «el servidor no respondió» de «lo cortamos
    nosotros», y esa diferencia decide si el hallazgo es sobre el sujeto
    obligado o sobre el observador."""
    if destino.exists() and destino.stat().st_size > 0:
        return CAPTURA_OK
    if _RED["seguidos"] >= MAX_FALLOS_SEGUIDOS:
        return CAPTURA_CORTE
    time.sleep(PAUSA)
    _RED["intentos"] += 1
    u = url.rstrip("/")
    if "/index.php/s/" in u and not u.endswith("/download"):
        u += "/download"
    destino.parent.mkdir(parents=True, exist_ok=True)
    # ⚠️ LÍMITES QUE OCULTABAN EVIDENCIA (2026-08-18). La primera pasada usó
    # `--max-time 60` y `--max-filesize 80MB`: un contenedor de 73 MB con **194
    # archivos dentro** quedó fuera por tiempo, y cuatro ZIP mayores de 80 MB se
    # truncaron y se registraron como «zip_ilegible». El inventario reportó 63
    # artefactos internos donde había 260.
    #
    # Un límite del instrumento que reduce el universo observado es peor que un
    # error de lectura: no falla, sólo muestra menos. Se elevan y **el truncado
    # se detecta**, en vez de pasar por archivo corrupto.
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", str(TOPE_SEGUNDOS), "-A", UA,
             "--max-filesize", str(TOPE_BYTES), "-o", str(destino),
             "-w", "%{http_code}|%{size_download}", u],
            capture_output=True, timeout=TOPE_SEGUNDOS + 40)
        salida = r.stdout.decode("utf-8", "replace").strip()
        code, _, size = salida.partition("|")
        # curl 63 = superó --max-filesize · 28 = superó --max-time. Ambos son
        # límites NUESTROS y así se declaran: el universo quedó recortado por el
        # instrumento, no por la fuente.
        if r.returncode == 63:
            _RED["fallos"] += 1
            return CAPTURA_TOPE
        if r.returncode == 28:
            _RED["fallos"] += 1
            return CAPTURA_TIEMPO
        if code.strip() != "200":
            _RED["fallos"] += 1
            _RED["seguidos"] += 1
            destino.unlink(missing_ok=True)
            return CAPTURA_HTTP
        _RED["seguidos"] = 0
        return CAPTURA_OK
    except Exception:                                    # noqa: BLE001
        _RED["fallos"] += 1
        _RED["seguidos"] += 1
        destino.unlink(missing_ok=True)
        return CAPTURA_FALLO


def _texto_pdf(p: Path) -> tuple[int, int]:
    """(páginas, caracteres). Sin abrir más de 40 páginas: sólo hace falta saber
    si rinde texto, no leerlo entero."""
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            n = len(pdf.pages)
            t = "\n".join((pg.extract_text() or "") for pg in pdf.pages[:40])
        return n, len(t.strip())
    except Exception:                                    # noqa: BLE001
        return 0, 0


def inspeccionar(p: Path) -> dict:
    """Qué ES este archivo. Nada sobre si cumple."""
    datos = p.read_bytes()
    f = firma(datos[:16])
    d = {"sha256": hashlib.sha256(datos).hexdigest(),
         "bytes": len(datos), "firma": f}

    if f == "zip":
        f = _afinar_zip(p)
        d["firma"] = f
        if f == "zip_ilegible":
            # Si el tamaño coincide con un tope redondo, casi seguro lo cortamos
            # nosotros. Se declara la sospecha para no imputar al GAD un defecto
            # del instrumento (la lección de OBS-030).
            d["posible_truncado_por_limite"] = len(datos) in (
                40_000_000, 80_000_000, 500_000_000)

    if f == "pdf":
        paginas, caracteres = _texto_pdf(p)
        d.update({"paginas": paginas, "caracteres": caracteres,
                  "texto_extraible": caracteres > 0,
                  # Un PDF que apenas rinde texto por página es un escaneo: se
                  # declara, y es aquí donde el OCR tendría algo que aportar.
                  "es_escaneo": bool(paginas and caracteres / paginas < 120),
                  "naturaleza_material": "documento_pdf"})
    elif f in ("jpeg", "png", "gif"):
        d.update({"texto_extraible": False, "es_imagen": True,
                  "naturaleza_material": "imagen"})
    elif f == "mp4":
        d.update({"texto_extraible": False,
                  "naturaleza_material": "video"})
    elif f in ("xlsx", "docx", "pptx", "ole"):
        d.update({"texto_extraible": True,
                  "naturaleza_material": "documento_ofimatico"})
    elif f == "zip":
        d["naturaleza_material"] = "contenedor"
        try:
            with zipfile.ZipFile(p) as z:
                internos = [n for n in z.namelist() if not n.endswith("/")]
                ext = Counter(Path(n).suffix.lower() or "(sin extensión)"
                              for n in internos)
                d.update({
                    "contenedor": True,
                    "artefactos_internos": len(internos),
                    "extensiones_internas": dict(ext.most_common()),
                    # Un contenedor sin ningún documento ofimático ni PDF es un
                    # álbum, no un expediente. Se registra el hecho; el juicio
                    # normativo NO se emite aquí.
                    "internos_con_texto": sum(
                        v for k, v in ext.items()
                        if k in (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".csv")),
                    "carpetas": sorted({str(Path(n).parent) for n in internos
                                        if str(Path(n).parent) != "."})[:8],
                })
        except Exception as e:                           # noqa: BLE001
            d["error"] = f"zip ilegible: {type(e).__name__}"
    else:
        d["naturaleza_material"] = "no_identificado"
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limite", type=int, default=0, help="0 = todos")
    ap.add_argument("--solo-contenedores", action="store_true")
    ap.add_argument("--json", default=str(SALIDA))
    args = ap.parse_args()

    enlaces = json.loads(ENLACES.read_text(encoding="utf-8"))["enlaces"]
    objetivo = [e for e in enlaces if e.get("estado") == "accesible"]
    if args.solo_contenedores:
        objetivo = [e for e in objetivo
                    if str(e.get("tipo_documento", "")) == "application/zip"]
    if args.limite:
        objetivo = objetivo[:args.limite]

    CACHE.mkdir(parents=True, exist_ok=True)
    print(f"INVENTARIO FÍSICO · {len(objetivo)} enlaces accesibles")
    print("qué ES cada artefacto — no si cumple\n")

    registros: list[dict] = []
    for i, e in enumerate(objetivo, 1):
        cit = (e.get("citado_en") or [{}])[0]
        clave = hashlib.sha256(e["url"].encode()).hexdigest()[:16]
        destino = CACHE / f"{clave}.bin"
        reg = {"url": e["url"], "numeral": cit.get("numeral", "?"),
               "tipo_declarado": e.get("tipo_documento"),
               "referencias": e.get("referencias")}
        estado = descargar(e["url"], destino)
        reg["captura"] = estado
        if estado != CAPTURA_OK:
            reg["estado"] = "no_inspeccionado"
        else:
            reg["estado"] = "inspeccionado"
            reg.update(inspeccionar(destino))
            # La correspondencia entre lo declarado y lo material se REGISTRA;
            # calificarla es potestad de la Regla Operativa, no del inventario.
            dec = str(reg.get("tipo_declarado") or "")
            mat = reg.get("firma", "")
            reg["declarado_vs_material"] = (
                "coincide" if (mat in dec or dec.split("/")[-1] in mat) else "difiere")
        registros.append(reg)
        if i % 40 == 0:
            print(f"   {i}/{len(objetivo)} · fallos {_RED['fallos']}", flush=True)

    # ── informe ───────────────────────────────────────────────────────────────
    ok = [r for r in registros if r.get("estado") == "inspeccionado"]
    print(f"\n  {len(ok)}/{len(registros)} artefactos inspeccionados\n")

    print("  NATURALEZA MATERIAL (lo que el archivo ES)")
    for k, v in Counter(r.get("naturaleza_material", "—") for r in ok).most_common():
        print(f"     {str(k):24} {v:5}")

    cont = [r for r in ok if r.get("contenedor")]
    if cont:
        internos = sum(r.get("artefactos_internos", 0) for r in cont)
        con_texto = sum(r.get("internos_con_texto", 0) for r in cont)
        print(f"\n  CONTENEDORES · {len(cont)} ZIP → {internos} artefactos dentro")
        print(f"     de ellos con texto (pdf/doc/xls/csv): {con_texto}")
        ext = Counter()
        for r in cont:
            for k, v in (r.get("extensiones_internas") or {}).items():
                ext[k] += v
        print(f"     extensiones internas: {dict(ext.most_common(8))}")

    esc = [r for r in ok if r.get("es_escaneo")]
    if esc:
        print(f"\n  ESCANEOS · {len(esc)} PDF sin texto extraíble — aquí el OCR aporta")
        for k, v in Counter(r["numeral"] for r in esc).most_common(6):
            print(f"     {k[:34]:36} {v:4}")

    dif = [r for r in ok if r.get("declarado_vs_material") == "difiere"]
    if dif:
        print(f"\n  ⚠ {len(dif)} artefactos cuyo tipo material difiere del declarado")
        for r in dif[:5]:
            print(f"     {r['numeral'][:22]:24} declarado {str(r['tipo_declarado']):20} "
                  f"→ material {r.get('firma')}")

    # ── BALANCE DE CONSERVACIÓN ───────────────────────────────────────────────
    # Las magnitudes NO se suman entre sí: un ZIP no es «un documento más sus 35
    # documentos», es una capa distinta. Y el balance debe cuadrar, para que el
    # universo no pueda encogerse sin que nadie lo note — que fue exactamente lo
    # que pasó cuando los topes del instrumento devolvieron 94 en vez de 935.
    capturas = Counter(r.get("captura", "?") for r in registros)
    individuales = [r for r in ok if not r.get("contenedor")]
    internos = sum(r.get("artefactos_internos", 0) for r in cont)
    print("\n  BALANCE DE CONSERVACIÓN (las magnitudes no se suman entre sí)")
    print(f"     enlaces publicados accesibles   {len(registros):6}")
    print(f"       ├─ inspeccionados             {len(ok):6}")
    print(f"       │    ├─ archivos individuales {len(individuales):6}")
    print(f"       │    └─ contenedores          {len(cont):6}  → {internos} artefactos dentro")
    print(f"       └─ NO inspeccionados          {len(registros) - len(ok):6}")
    for k, v in capturas.most_common():
        if k != CAPTURA_OK:
            marca = ("  ← LÍMITE NUESTRO, no ausencia de la fuente"
                     if k in (CAPTURA_TOPE, CAPTURA_TIEMPO) else "")
            print(f"            {k:34} {v:4}{marca}")
    cuadra = len(ok) + (len(registros) - len(ok)) == len(registros)
    print(f"\n     balance {'cuadra' if cuadra else '⚠ NO CUADRA'} · "
          f"objetos físicos observados: {len(individuales) + internos}")

    truncados = [r for r in ok if r.get("posible_truncado_por_limite")]
    if truncados or capturas[CAPTURA_TOPE] or capturas[CAPTURA_TIEMPO]:
        print("\n  ⚠ HAY CAPTURA INCOMPLETA POR LÍMITES DEL INSTRUMENTO.")
        print("    Lo no capturado NO puede leerse como ausencia del sujeto obligado:")
        print("    quedó fuera del perímetro efectivo de observación (OBS-030).")

    if _RED["fallos"]:
        print(f"\n  ⚠ {_RED['fallos']}/{_RED['intentos']} peticiones con incidencia")

    p = Path(args.json)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"_meta": {
        "procedencia": _procedencia("inventario"),
        "generado": _dt.date.today().isoformat(),
        "regla": "la existencia de un enlace no acredita la existencia ni la "
                 "naturaleza del documento exigido",
        "limite": "este inventario responde QUÉ ES cada artefacto; si cumple lo "
                  "decide la Regla Operativa, no este módulo",
        "transporte": dict(_RED),
    }, "artefactos": registros}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  → {p.relative_to(RAIZ) if p.is_absolute() else p}")


if __name__ == "__main__":
    main()
