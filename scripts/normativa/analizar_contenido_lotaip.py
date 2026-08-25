# -*- coding: utf-8 -*-
"""
scripts/normativa/analizar_contenido_lotaip.py — la segunda capa probatoria
════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-17). La medición de periodicidad dejó 2026 con 21 de 22
numerales en verde. Ese resultado prueba **publicación**, no contenido. El colega:

> *«Ahí sí vamos a saber si ese 21/22 de 2026 representa cumplimiento sustantivo o
> solamente cumplimiento de publicación.»*

LAS DOS REGLAS QUE GOBIERNAN ESTE MÓDULO

**1 · La forma de la ausencia no se interpreta** (colega, 2026-08-17). La norma fija
dos fórmulas —`NO APLICA` e `INFORMACIÓN NO DISPONIBLE`, sin comillas (Guía §VI)— y el
Instructivo manda *«verificar que en éste se encuentre colocado los textos»*: es una
comprobación de forma. Por eso `no disponible` **no se convierte** en `INFORMACIÓN NO
DISPONIBLE` por equivalencia semántica: se conserva el texto observado, se declara la
regla, y el resultado se gradúa —exacta · variante · no sustentada—. Traducir por
sentido reintroduciría justo la interpretación que QUIRA existe para evitar.

**2 · Un enlace al dominio del GAD es información oficial** (Javo, 2026-08-17):
*«La información que esté linkeada y mande a revisar fuera de transparencia de la DPE,
siempre y cuando esté alojada en la WEB del GAD, es información oficial.»* De modo que
una celda con enlace a `montecristi.gob.ec` **no es una ausencia**: es contenido que
remite a su respaldo. Contarla como vacía habría fabricado un incumplimiento.

LO QUE ESTE MÓDULO **NO** HACE

  · No verifica que el enlace resuelva. Eso es accesibilidad, prueba distinta y posterior.
  · No decide si un campo del CSV corresponde al campo exigido por la matriz. La guía
    describe los campos en prosa («Número secuencial de la información que se registra
    en cada celda…») y la cabecera dice `No.`. Casarlos exige interpretación, así que
    **se compara lo verificable —cuántas columnas— y lo demás queda `no_determinable`.**
  · No puntúa ni alimenta indicador alguno. La obligación determina qué puede medir el
    indicador, nunca al revés.

Uso:  python scripts/normativa/analizar_contenido_lotaip.py [--json salida.json]
Dylus Lab © 2026
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
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
sys.path.insert(0, str(Path(__file__).parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from invariantes import Invariantes                    # noqa: E402

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


INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
EXIGENCIAS = RAIZ / "data" / "lotaip" / "exigencias_por_numeral.json"
SELLO = RAIZ / "data" / "lotaip" / "VARA_SELLO.json"


def verificar_sello() -> str:
    """La vara está congelada durante la fase probatoria (colega, 2026-08-17).

    Sin esta comprobación, «no se corrige la matriz en silencio» sería una intención.
    Con ella, cualquier retoque a la exigencia normativa detiene el análisis: si la
    evidencia contradice la norma **se abre incidencia de corpus**, no se ablanda la
    vara para que el resultado encaje."""
    import hashlib
    if not SELLO.exists():
        return "sin sello — la vara no está congelada"
    s = json.loads(SELLO.read_text(encoding="utf-8"))
    actual = hashlib.sha256(EXIGENCIAS.read_bytes()).hexdigest()
    if actual != s["sha256"]:
        print("[XX] LA VARA NORMATIVA CAMBIÓ desde que fue sellada.")
        print(f"     sellada: {s['sha256'][:32]}…\n     actual : {actual[:32]}…")
        print("     El análisis se detiene. Abra incidencia de corpus o vuelva a sellar")
        print("     de forma explícita: no se mide con una vara movida a mitad de prueba.")
        sys.exit(3)
    return f"vara sellada {s['sha256'][:16]}… · {s['numerales']} numerales"

# El dominio del sujeto obligado. Un enlace aquí es respaldo oficial (regla de Javo);
# uno a otro host es contenido remitido a un tercero y se registra aparte, sin juzgarlo.
DOMINIO_GAD = _S.dominio_web()


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").lower()
    return " ".join(s.split())


def _clave(etiqueta: str) -> str | None:
    e = (etiqueta or "").strip()
    if not e.lower().startswith("numeral"):
        return None
    n = e.split(None, 1)[1].strip() if " " in e else ""
    return "5" if n == "5-22" else n or None


def _tipo(nombre: str) -> str:
    """La tríada que exige el anexo del cap. IX. Sólo el conjunto de datos lleva la
    información; metadatos y diccionario la describen."""
    n = _norm(nombre)
    # EL ORDEN IMPORTA. Muchos archivos se llaman «…-datos-abiertos-metadatos.csv»:
    # comprobar «datos abiertos» primero los clasificaba como conjunto de datos, y sus
    # ~25 columnas de metadatos aparecían como si el numeral publicara 25 campos donde
    # la guía exige 9. Los descriptores se descartan ANTES que el contenido.
    if "metadato" in n:
        return "metadatos"
    if "diccionario" in n:
        return "diccionario"
    if "conjunto" in n or "datos abiertos" in n:
        return "conjunto_de_datos"
    return "otro"


# ── regla de ausencia ───────────────────────────────────────────────────────────────
FORMULAS = ["NO APLICA", "INFORMACIÓN NO DISPONIBLE"]
_FORM_NORM = {_norm(f) for f in FORMULAS}

# Formas de declarar carencia que la norma NO admite, enumeradas a partir de lo
# realmente observado en los 936 archivos. La lista es cerrada a propósito: cualquier
# celda que no esté aquí ni sea una fórmula normativa **cuenta como dato**, no como
# ausencia. Ante la duda, el registro se lee a favor del sujeto obligado.
_NO_SUSTENTADAS = {
    "n/a", "na", "n.a.", "n/d", "nd", "noaplica",
    "no disponible", "sin informacion", "sin informacion disponible",
    "no existe", "ninguno", "ninguna",
    "-", "--", "---", ".", "..", "...", "s/n", "s/d", "*",
}
# Deliberadamente NO incluidos: `0` y `0,00`. Un cero puede ser el dato —un monto de
# cero es información, no su ausencia— y contarlo como carencia inventaría un vacío.


def _ausencia(celda: str) -> str | None:
    """Gradúa la forma sin traducirla.

    `exacta`         el texto literal que manda la norma
    `variante`       el mismo texto con otra caja o sin tildes — la norma no lo prevé
    `no_sustentada`  otra redacción («no disponible», «s/n», «-»): se conserva tal cual
    `None`           no es una declaración de ausencia
    """
    c = (celda or "").strip().strip('"').strip()
    if not c:
        return None
    if c in FORMULAS:
        return "exacta"
    n = " ".join(_norm(c).split())
    if n in _FORM_NORM:
        return "variante"
    # ENUMERADAS, NO ADIVINADAS. Un patrón abierto («empieza por no/sin/n/a…») marcó
    # como declaración de ausencia el nombre «NAPA MENDOZA GEOVER AUGUSTO» y el valor
    # numérico «-500». Detectar carencias donde hay datos es peor que no detectarlas:
    # infla el hallazgo con ruido y lo vuelve indefendible. Se listan las formas
    # realmente observadas y sólo se acepta coincidencia COMPLETA de la celda.
    if n in _NO_SUSTENTADAS:
        return "no_sustentada"
    return None


def _leer_csv(ruta: Path) -> tuple[list[list[str]], str | None]:
    """El portal publica con `;` y BOM, pero no siempre. Se prueban delimitadores y
    codificaciones antes de declarar ilegible: un archivo que el lector no supo abrir
    NO es un archivo sin contenido."""
    crudo = ruta.read_bytes()
    # `cp850` antes que `latin-1`: parte de los CSV se exportaron desde una consola DOS
    # y traen «Direcci¢n institucional». latin-1 nunca falla —acepta cualquier byte— y
    # habría fijado la lectura corrupta como si fuera el texto real.
    for enc in ("utf-8-sig", "utf-8", "cp1252", "cp850", "latin-1"):
        try:
            txt = crudo.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        return [], "no_decodificable"
    # Contar separadores NO basta: los campos de texto llevan comas dentro
    # («Dirección de Ambiente, Espacios públicos») y elegir `,` por mayoría partía una
    # tabla de 9 columnas en 19. Se prueban los candidatos y gana el que produce un
    # número de columnas ESTABLE entre filas, que es lo que define una tabla.
    mejor, mejores_filas = None, []
    for delim in (";", ",", "\t", "|"):
        try:
            filas = [f for f in csv.reader(io.StringIO(txt), delimiter=delim)
                     if any((c or "").strip() for c in f)]
        except csv.Error:
            continue
        if not filas:
            continue
        anchos = Counter(len(f) for f in filas)
        ancho, veces = anchos.most_common(1)[0]
        if ancho < 2:
            continue
        puntaje = (veces / len(filas), ancho)     # estabilidad primero, riqueza después
        if mejor is None or puntaje > mejor[0]:
            mejor, mejores_filas = (puntaje, delim), filas
    if mejor is None:
        return [], "sin_estructura_tabular"
    return mejores_filas, None


def analizar(reg: dict) -> dict:
    ruta = RAIZ / reg["ruta"]
    d = {"anio": reg["anio"], "mes": reg["mes"], "numeral": reg["numeral"],
         "clave": _clave(reg["numeral"]), "archivo": reg["archivo"],
         "tipo": _tipo(reg["archivo"]), "sha256": reg.get("sha256"),
         "bytes": reg.get("bytes")}

    if reg.get("estado") != "descargado" or not ruta.exists():
        d["estado_contenido"] = "recurso_no_accesible"
        d["razon"] = reg.get("estado", "sin ruta en disco")
        return d

    filas, err = _leer_csv(ruta)
    if err:
        d.update({"estado_contenido": "contenido_no_legible", "razon": err})
        return d
    if not filas:
        d.update({"estado_contenido": "contenido_sin_datos",
                  "razon": "el archivo no contiene ni cabecera"})
        return d

    cab, datos = filas[0], filas[1:]
    # Las columnas vacías del final son artefacto de exportar desde Excel, no campos
    # publicados: el directorio del numeral 2 trae sus 9 campos con nombre y 10
    # columnas mudas detrás. Contarlas hacía aparecer 19 campos donde la guía exige 9
    # —una discrepancia inventada por el lector—. Se recorta por la última columna con
    # contenido real en CUALQUIER fila, no sólo en la cabecera.
    util = 0
    for f in filas:
        for j, c in enumerate(f):
            if (c or "").strip():
                util = max(util, j + 1)
    d["columnas"] = util
    d["columnas_en_bruto"] = len(cab)
    if util != len(cab):
        d["columnas_vacias_al_final"] = len(cab) - util
    d["cabecera"] = [c.strip() for c in cab[:util]][:30]
    d["filas_datos"] = len(datos)

    enlaces = [u for f in datos for c in f
               for u in re.findall(r"https?://[^\s;,\"']+", c or "")]
    hosts = Counter(u.split("/")[2].lower() for u in enlaces if "/" in u[8:])
    d["enlaces"] = {
        "total": len(enlaces),
        # Regla de Javo: alojado en la web del GAD ⇒ información oficial.
        "al_dominio_del_gad": sum(v for h, v in hosts.items() if DOMINIO_GAD in h),
        "a_terceros": sum(v for h, v in hosts.items() if DOMINIO_GAD not in h),
        "hosts": dict(hosts.most_common(6)),
    }

    formas = Counter()
    celdas_vacias = celdas_tot = 0
    filas_solo_ausencia = 0
    literales: Counter = Counter()
    for f in datos:
        marcas = []
        for c in f:
            celdas_tot += 1
            v = (c or "").strip()
            if not v:
                celdas_vacias += 1
                marcas.append("vacia")
                continue
            a = _ausencia(v)
            if a:
                formas[a] += 1
                if a != "exacta":
                    literales[v] += 1
                marcas.append("ausencia")
            else:
                marcas.append("dato")
        if marcas and all(m != "dato" for m in marcas):
            filas_solo_ausencia += 1

    d["declaraciones_de_ausencia"] = {
        "por_forma": dict(formas),
        # El texto observado se conserva SIN traducir. Es la evidencia del hallazgo.
        "textos_no_normativos": dict(literales.most_common(8)),
        "regla_normativa": " | ".join(FORMULAS),
    }
    d["celdas_vacias"] = celdas_vacias
    d["celdas_totales"] = celdas_tot

    if not datos:
        d["estado_contenido"] = "contenido_sin_datos"
        d["razon"] = "sólo cabecera: ninguna fila de datos"
    elif filas_solo_ausencia == len(datos):
        d["estado_contenido"] = "declaracion_de_ausencia"
        d["razon"] = ("todas las filas declaran carencia — cumple si la fórmula es la "
                      "que manda la norma; el estado de forma se registra aparte")
    else:
        d["estado_contenido"] = "contenido_con_datos"
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", help="ruta donde volcar el análisis")
    args = ap.parse_args()

    print(f"[vara] {verificar_sello()}")
    idx = json.loads(INDICE.read_text(encoding="utf-8"))
    ex = json.loads(EXIGENCIAS.read_text(encoding="utf-8"))
    campos_exig = {n["numeral"]: len(n["campos_exigidos"]) for n in ex["numerales"]}

    regs = [analizar(r) for r in idx["archivos"]]
    cd = [r for r in regs if r["tipo"] == "conjunto_de_datos"]

    print(f"CONTENIDO LOTAIP · {len(regs)} archivos · "
          f"{len(cd)} son «conjunto de datos» (los que llevan la información)\n")

    est = Counter(r["estado_contenido"] for r in cd)
    print("  ESTADO DEL CONTENIDO (sólo conjuntos de datos)")
    for k, v in est.most_common():
        print(f"     {k:28} {v:4}")

    # ── la forma de la ausencia ────────────────────────────────────────────────────
    formas = Counter()
    textos: Counter = Counter()
    for r in cd:
        for k, v in (r.get("declaraciones_de_ausencia", {}).get("por_forma") or {}).items():
            formas[k] += v
        for t, v in (r.get("declaraciones_de_ausencia", {})
                     .get("textos_no_normativos") or {}).items():
            textos[t] += v
    print(f"\n  REGLA DE AUSENCIA · la norma manda: {' | '.join(FORMULAS)}")
    for k in ("exacta", "variante", "no_sustentada"):
        if formas.get(k):
            print(f"     forma {k:16} {formas[k]:6} celdas")
    if textos:
        print("     textos observados que la norma no prevé (sin traducir):")
        for t, v in textos.most_common(8):
            print(f"        «{t[:44]}» ×{v}")

    # ── enlaces al dominio del GAD ────────────────────────────────────────────────
    gad = sum(r.get("enlaces", {}).get("al_dominio_del_gad", 0) for r in cd)
    ter = sum(r.get("enlaces", {}).get("a_terceros", 0) for r in cd)
    print(f"\n  ENLACES DENTRO DE LOS CONJUNTOS DE DATOS")
    print(f"     al dominio del GAD ({DOMINIO_GAD}) {gad:6}  → información oficial")
    print(f"     a terceros                            {ter:6}  → se registra, no se juzga")
    print("     (no se comprueba aquí que resuelvan: eso es accesibilidad, prueba aparte)")

    # ── columnas contra campos exigidos ───────────────────────────────────────────
    print(f"\n  COLUMNAS PUBLICADAS vs CAMPOS EXIGIDOS POR LA GUÍA")
    print("     comparación de CANTIDAD, que es verificable. La correspondencia campo a")
    print("     campo exige interpretación → queda no_determinable.")
    porn: dict[str, set] = defaultdict(set)
    for r in cd:
        if r.get("clave") and r.get("columnas"):
            porn[r["clave"]].add(r["columnas"])
    print(f"     {'num':6}{'exige':>7}{'publica':>22}")
    faltantes = 0
    for k in sorted(porn, key=lambda x: (len(x), x)):
        e = campos_exig.get(k)
        obs = sorted(porn[k])
        # Publicar MÁS columnas no es incumplimiento: el numeral 17 desglosa en dos
        # columnas el campo que la guía enuncia junto («Nombres, apellidos y puesto
        # institucional»). Sólo se señala cuando se publica MENOS de lo exigido, que
        # es lo único que la cantidad puede probar por sí sola.
        marca = ""
        if e and min(obs) < e:
            marca, faltantes = "  ← publica MENOS de lo exigido", faltantes + 1
        elif e and e not in obs:
            marca = "  · desglosa campos enunciados juntos"
        print(f"     {k:6}{str(e or '—'):>7}{str(obs):>22}{marca}")
    print(f"     → {faltantes} numerales publican menos columnas que campos exige la guía")

    inv = Invariantes("contenido LOTAIP")
    inv.cardinalidad("conjuntos de datos analizados", len(cd), minimo=100)
    # `minimo=0`: que ningún archivo resulte ilegible es el resultado deseable, no una
    # anomalía. El valor por defecto (1) lo habría marcado como fallo.
    inv.cardinalidad("no legibles", sum(1 for r in cd
                                        if r["estado_contenido"] == "contenido_no_legible"),
                     minimo=0, maximo=5)
    print()
    inv.informe()

    if args.json:
        p = Path(args.json)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"_meta": {
            "procedencia": _procedencia("contenido"),
            "vara": "data/lotaip/exigencias_por_numeral.json (congelada)",
            "evidencia": "data/lotaip/descargas_indice.json",
            "reglas": [
                "la forma de la ausencia no se traduce por equivalencia semántica",
                f"enlace alojado en {DOMINIO_GAD} = información oficial del sujeto obligado",
                "correspondencia campo a campo = no_determinable sin interpretación",
            ],
        }, "archivos": regs}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  → {p}")


if __name__ == "__main__":
    main()
