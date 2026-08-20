# -*- coding: utf-8 -*-
"""
scripts/normativa/inventario_contenido.py — qué hay DENTRO de los contenedores
══════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-18). El inventario de enlaces cerró con una cifra que
obliga a seguir: 26 de los 417 enlaces accesibles son contenedores, y guardan
**935 artefactos** que ningún análisis había tocado. Entre ellos, 671 PDF.

El colega puso la condición para abrirlos bien:

> *«Yo no avanzaría a "abrir los 672" como una masa única. Primero hay que fijar
> el inventario como una fotografía reproducible del universo.»*

DOS NIVELES QUE NO SE COLAPSAN, y es la aportación central de este módulo:

    publicación   cada aparición del documento en el portal (enlace × período)
    artefacto     el objeto físico único, identificado por su SHA-256

Deduplicar por SHA y quedarse sólo con el artefacto perdería la historia de
publicación; contar publicaciones y llamarlas documentos infla el universo. En
d07 pasó lo segundo: se dijo «15 escaneos del numeral 15» cuando era **un solo
archivo, mismo SHA, publicado quince meses seguidos**. Conservando ambos niveles
se puede afirmar a la vez:

    «el contrato colectivo se publicó 15 veces»   ← publicaciones
    «es un único artefacto físico»                ← artefacto

Ambas cosas son ciertas y ninguna sustituye a la otra.

QUÉ HACE. Abre los contenedores ya descargados —sin volver a la red—, y por cada
artefacto interno registra: SHA, tamaño, firma real (no la extensión), si rinde
texto, páginas, si es escaneo, su ruta dentro del contenedor y quién es su padre.

QUÉ NO HACE. No decide si cumple. La naturaleza material se registra; la
correspondencia con la obligación la evalúa la Regla Operativa, nunca este
módulo. Y no marca nada como candidato a OCR por su extensión: eso se deriva de
haberlo abierto, que es la lección del numeral 17.

Uso:  python scripts/normativa/inventario_contenido.py [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
INVENTARIO = RAIZ / "data" / "lotaip" / "inventario_documental.json"
CACHE = RAIZ / "data" / "lotaip" / "artefactos"
SALIDA = RAIZ / "data" / "lotaip" / "contenido_contenedores.json"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_FIRMAS = [
    (b"%PDF", "pdf"), (b"\xff\xd8\xff", "jpeg"), (b"\x89PNG", "png"),
    (b"PK\x03\x04", "zip"), (b"\xd0\xcf\x11\xe0", "ole"), (b"GIF8", "gif"),
]

# Límite de páginas al sondear un PDF: sólo hace falta saber si rinde texto, no
# leerlo entero. Con 935 artefactos, abrir todo completo costaría horas sin
# añadir una sola conclusión.
PAGINAS_SONDEO = 8


def firma(datos: bytes) -> str:
    for pre, nombre in _FIRMAS:
        if datos.startswith(pre):
            return nombre
    if datos[4:12] in (b"ftypisom", b"ftypmp42"):
        return "mp4"
    return "desconocido"


def _sondear_pdf(datos: bytes) -> dict:
    """Páginas y legibilidad, por estructura del archivo y no por extracción.

    ⚡ POR QUÉ ASÍ. La primera versión abría cada PDF con `pdfplumber` y extraía
    ocho páginas. Sobre 671 documentos eso tarda horas sin añadir una sola
    conclusión: para saber si un PDF **tiene capa de texto** basta con mirar su
    estructura. Un escaneo sin OCR no declara fuentes —no hay `/Font`— porque no
    contiene caracteres, sólo una imagen por página.

    La heurística es barata y directa: `/Font` presente ⇒ hay texto. Cuando el
    indicio es ambiguo se cae a la extracción real, que es cara pero exacta, y
    sólo para esos casos."""
    n = datos.count(b"/Type/Page") + datos.count(b"/Type /Page")
    tiene_fuentes = b"/Font" in datos
    imagenes = datos.count(b"/Image")
    d = {"paginas": max(n, 1) if n else 0,
         "declara_fuentes": tiene_fuentes,
         "objetos_imagen": imagenes}

    if tiene_fuentes:
        d.update({"texto_extraible": True, "es_escaneo": False,
                  "metodo_sondeo": "estructura"})
        return d
    if imagenes:
        # Sin fuentes y con imágenes: escaneo sin capa de texto. Es justo aquí
        # —y sólo aquí— donde un OCR tendría algo que aportar.
        d.update({"texto_extraible": False, "es_escaneo": True,
                  "metodo_sondeo": "estructura"})
        return d

    # Caso ambiguo: ni fuentes ni imágenes declaradas. Se paga la extracción.
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(datos)) as pdf:
            paginas = len(pdf.pages)
            t = "\n".join((pg.extract_text() or "")
                          for pg in pdf.pages[:PAGINAS_SONDEO])
        car = len(t.strip())
        vistas = min(paginas, PAGINAS_SONDEO) or 1
        d.update({"paginas": paginas, "caracteres_muestra": car,
                  "texto_extraible": car > 0,
                  "es_escaneo": car / vistas < 120,
                  "metodo_sondeo": "extraccion"})
    except Exception as e:                               # noqa: BLE001
        d.update({"texto_extraible": False,
                  "error_lectura": type(e).__name__,
                  "metodo_sondeo": "fallido"})
    return d


def clasificar(nombre: str, datos: bytes) -> dict:
    f = firma(datos[:16])
    d = {"firma": f, "bytes": len(datos),
         "sha256": hashlib.sha256(datos).hexdigest()}
    if f == "pdf":
        d.update(_sondear_pdf(datos))
        d["naturaleza_material"] = "documento_pdf"
    elif f in ("jpeg", "png", "gif"):
        d.update({"texto_extraible": False, "naturaleza_material": "imagen"})
    elif f == "mp4":
        d.update({"texto_extraible": False, "naturaleza_material": "video"})
    elif f in ("zip", "ole"):
        # Un contenedor dentro de un contenedor. Se declara y NO se abre en
        # cascada: primero hay que saber cuántos hay antes de decidir si el
        # universo tiene un nivel más de profundidad.
        d["naturaleza_material"] = ("documento_ofimatico" if f == "ole"
                                    else "contenedor_anidado")
    else:
        d["naturaleza_material"] = "no_identificado"
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", default=str(SALIDA))
    args = ap.parse_args()

    inv = json.loads(INVENTARIO.read_text(encoding="utf-8"))["artefactos"]
    contenedores = [r for r in inv if r.get("contenedor")]
    print(f"CONTENIDO DE CONTENEDORES · {len(contenedores)} ZIP ya descargados")
    print("se abre lo que hay dentro — sin volver a la red\n")

    internos: list[dict] = []
    fallos = 0
    for i, c in enumerate(contenedores, 1):
        clave = hashlib.sha256(c["url"].encode()).hexdigest()[:16]
        p = CACHE / f"{clave}.bin"
        if not p.exists():
            fallos += 1
            continue
        try:
            with zipfile.ZipFile(p) as z:
                for info in z.infolist():
                    if info.is_dir():
                        continue
                    try:
                        datos = z.read(info)
                    except Exception:                    # noqa: BLE001
                        internos.append({
                            "contenedor_url": c["url"], "numeral": c["numeral"],
                            "ruta_interna": info.filename,
                            "estado": "no_extraible"})
                        continue
                    reg = {
                        "contenedor_url": c["url"],
                        "contenedor_sha": c.get("sha256"),
                        "numeral": c["numeral"],
                        "ruta_interna": info.filename,
                        "carpeta": str(Path(info.filename).parent),
                        "extension_declarada": Path(info.filename).suffix.lower(),
                        "estado": "inspeccionado",
                    }
                    reg.update(clasificar(info.filename, datos))
                    internos.append(reg)
        except Exception as e:                           # noqa: BLE001
            fallos += 1
            print(f"   [XX] contenedor ilegible: {type(e).__name__}")
        if i % 8 == 0:
            print(f"   {i}/{len(contenedores)} contenedores · "
                  f"{len(internos)} artefactos", flush=True)

    ok = [r for r in internos if r.get("estado") == "inspeccionado"]
    print(f"\n  {len(ok)} artefactos internos inspeccionados"
          f"{f' · {fallos} contenedores ilegibles' if fallos else ''}\n")

    print("  NATURALEZA MATERIAL (lo que el archivo ES, por su firma)")
    for k, v in Counter(r.get("naturaleza_material") for r in ok).most_common():
        print(f"     {str(k):24} {v:5}")

    # ── La distinción que pidió el colega ─────────────────────────────────────
    # Publicaciones ≠ artefactos. Se conservan las dos, porque responden a
    # preguntas distintas y ninguna sustituye a la otra.
    por_sha = defaultdict(list)
    for r in ok:
        if r.get("sha256"):
            por_sha[r["sha256"]].append(r)
    unicos = len(por_sha)
    repetidos = {s: v for s, v in por_sha.items() if len(v) > 1}
    print(f"\n  PUBLICACIONES vs ARTEFACTOS FÍSICOS")
    print(f"     apariciones dentro de contenedores  {len(ok):5}")
    print(f"     artefactos físicos únicos (SHA)     {unicos:5}")
    print(f"     objetos publicados más de una vez   {len(repetidos):5}")
    if repetidos:
        top = sorted(repetidos.items(), key=lambda kv: -len(kv[1]))[:3]
        for s, v in top:
            print(f"        {s[:12]}… ×{len(v):3}  {Path(v[0]['ruta_interna']).name[:44]}")

    # ── Sólo lo abierto puede ser candidato a OCR ─────────────────────────────
    escaneos = [r for r in ok if r.get("es_escaneo")]
    con_texto = [r for r in ok if r.get("texto_extraible")]
    print(f"\n  LEGIBILIDAD")
    print(f"     PDF con texto extraíble             {len(con_texto):5}")
    print(f"     PDF escaneados (candidatos a OCR)   {len(escaneos):5}")
    if escaneos:
        for k, v in Counter(r["numeral"] for r in escaneos).most_common(6):
            print(f"        {k[:32]:34} {v:4}")
    sha_esc = {r["sha256"] for r in escaneos if r.get("sha256")}
    print(f"     → escaneos físicos ÚNICOS           {len(sha_esc):5}"
          "   ← el corpus real de OCR")

    anid = [r for r in ok if r.get("naturaleza_material") == "contenedor_anidado"]
    if anid:
        print(f"\n  ⚠ {len(anid)} contenedores ANIDADOS: el universo tiene un nivel más")

    print("\n  BALANCE")
    print(f"     contenedores abiertos               {len(contenedores) - fallos:5}")
    print(f"     apariciones internas                {len(internos):5}")
    print(f"     inspeccionadas                      {len(ok):5}")
    print(f"     no extraíbles                       {len(internos) - len(ok):5}")

    p = Path(args.json)
    # La naturaleza del artefacto viaja DENTRO de él (ADR-051 §10). Estos 636
    # objetos son correctos y sirven para construir el sistema; NO son todavía
    # una observación atribuible a QUIRA, y quien abra este JSON debe poder
    # saberlo sin haber leído el ADR.
    try:
        sys.path.insert(0, str(RAIZ))
        from app.agents.apropiacion import (MATERIAL_DE_INGENIERIA,
                                            clasificar_artefacto)
        _clase = clasificar_artefacto(
            MATERIAL_DE_INGENIERIA,
            "la cadena de adquisición que lo produjo aún no está acreditada como "
            "reproducible sobre este sujeto")
    except Exception:                                    # noqa: BLE001
        _clase = {"clase_epistemologica": "material_de_ingenieria"}

    p.write_text(json.dumps({"_meta": {
        **_clase,
        "generado": "2026-08-18",
        "regla": "publicación ≠ artefacto físico · ambos niveles se conservan",
        "limite": "registra QUÉ ES cada artefacto; si cumple lo decide la RO",
        "sondeo_paginas": PAGINAS_SONDEO,
        "apariciones": len(internos), "artefactos_unicos": unicos,
    }, "internos": internos}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n  → {p.relative_to(RAIZ) if p.is_absolute() else p}")


if __name__ == "__main__":
    main()
