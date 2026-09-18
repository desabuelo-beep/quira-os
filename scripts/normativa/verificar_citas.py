# -*- coding: utf-8 -*-
"""
verificar_citas.py — ninguna cita normativa sin leer su fuente.

Nace de la falsación 43 (PANORAMA §5-duoquinquagies): se citó un artículo REAL
(COOTAD 266) como si fuera la norma que rige la rendición de cuentas, cuando la
cadena rectora (CNO-IX-001) ya estaba en el canon y no se leyó. Y de las citas del
QLEP y de los ACK que atribuyen a un artículo lo que el artículo no dice.
Un ecosistema que se sustenta en la norma vigente no puede citarla de memoria.

Tres comprobaciones, SÓLO LECTURA (la sesión con el corpus se abre read-only; la
URI se resuelve con brn_cno._uri y nunca se imprime):

  1. HUELLA     · toda cita `SIGLA NUM` acompañada de una huella de 12 hex debe
                  corresponder, en el corpus, a ese mismo artículo.
  2. EXISTENCIA · todo `SIGLA NUM` citado debe existir en el corpus (o en una
                  cadena CNO, que la BRN ya verifica con su propia huella).
  3. RECTOR     · si la línea trata la materia de una CNO (por su título) y cita un
                  artículo que ninguna CNO encadena, se avisa: ¿rector o
                  concordancia? Es la comprobación que habría detenido la falsación 43.

Uso:
  python scripts/normativa/verificar_citas.py ARCHIVO [...] [--existencia] [--rector]
  python scripts/normativa/verificar_citas.py --hook     # PostToolUse (Edit/Write)
Salida (convención de gates): 0 ok · 1 hallazgo · 2 no determinable (sin corpus).
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
BRN_DIR = RAIZ / "docs" / "brn"
CACHE = Path(tempfile.gettempdir()) / "quira_verificar_citas_indice.json"
CACHE_TTL_S = 6 * 3600          # el corpus se reingiere rara vez; 6 h acotan la caducidad

# Siglas que otras capas usan para normas que el corpus nombra distinto.
ALIAS = {"LOAPAM": "LOPAM", "LOD": "LODISC", "LOMH": "LMH", "CPFP": "COPLAFIP"}

# Palabras de título de CNO demasiado generales para decidir la materia de una línea.
_VACIAS = {"obligacion", "sistema", "cantonal", "gobiernos", "autonomos", "descentralizados",
           "publica", "publico", "gestion", "ciudadana", "marco", "regla", "especifica",
           "derecho", "acceso", "informacion", "minima", "prioritaria", "articulacion",
           "traduccion"}

RX_HUELLA = re.compile(r"`([0-9a-f]{12})`")
_NUM = r"(\d+(?:\.\d+)?)(?!\d)(?!\s*%)"
RX_CONT = re.compile(
    r"^\s*(?:\*\*)?\s*(?:`[0-9a-f]{12}`)?\s*(?:\([^)]*\))?\s*(?:\*\*)?\s*"
    r"(?:,|·|\by\b|–|→)\s*(?:\*\*)?\s*" + _NUM)     # «LOSNCP 21 → 22»: la flecha renumera
RX_NUMERAL = re.compile(r"^\s*(?:\*\*)?\s*(?:n[úu]m\.|numeral|lit\.|literal|inciso)", re.I)


def _plano(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# ── Índice del corpus y cadenas CNO ────────────────────────────────────────────
def cargar_indice(usar_cache: bool = True) -> dict | None:
    """{'huella': {h12: [sigla, art, texto]}, 'arts': {sigla: [art,...]}} o None."""
    if usar_cache and CACHE.exists() and time.time() - CACHE.stat().st_mtime < CACHE_TTL_S:
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    sys.path.insert(0, str(RAIZ / "scripts"))
    try:
        import brn_cno  # noqa: PLC0415  (se reutiliza _uri: no se reimplementa la lectura de secretos)
        import psycopg2  # noqa: PLC0415
        uri = brn_cno._uri()
        if not uri:
            return None
        conn = psycopg2.connect(uri, connect_timeout=25)
        conn.set_session(readonly=True, autocommit=True)
        cur = conn.cursor()
        cur.execute("SELECT norma_sigla, articulo_num::text, left(sha256,12), "
                    "left(regexp_replace(contenido,'[[:space:]]+',' ','g'),180) "
                    "FROM public.normativa_corpus")
        filas = cur.fetchall()
        conn.close()
    except Exception:  # noqa: BLE001 — sólo el tipo importa; nunca se imprime la URI
        return None
    huella, arts = {}, {}
    for sig, art, h, txt in filas:
        huella[h] = [sig, art, txt]
        if art:
            arts.setdefault(sig, set()).add(art)
    idx = {"huella": huella, "arts": {k: sorted(v) for k, v in arts.items()}}
    try:
        CACHE.write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    return idx


def cargar_cnos() -> list[dict]:
    import yaml  # noqa: PLC0415
    out = []
    for p in sorted(BRN_DIR.glob("CNO-*.yaml")):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        cadena = {(str(e.get("norma")), str(e.get("articulo"))) for e in d.get("cadena", []) or []}
        claves = {w for w in re.findall(r"[a-z]{5,}", _plano(str(d.get("titulo", "")))) if w not in _VACIAS}
        out.append({"id": d.get("id"), "titulo": d.get("titulo"), "cadena": cadena, "claves": claves})
    return out


# ── Lectura de citas ───────────────────────────────────────────────────────────
def rx_siglas(siglas) -> re.Pattern:
    alt = "|".join(re.escape(s) for s in sorted(set(siglas) | set(ALIAS), key=len, reverse=True))
    return re.compile(rf"(?<![\w-])({alt})(?![\w-])\**\s*(?:Arts?(?:ículos?|\.)?\s*)?" + _NUM)


def citas_de(texto: str, rx: re.Pattern) -> list[tuple[str, str, int, int]]:
    """(sigla, artículo, inicio, fin) de cada cita, incluidas las continuaciones
    «LOPC 89 · 90 · 91». Tras «núm.», «lit.» o «inciso» lo que sigue son numerales
    del mismo artículo, no artículos nuevos."""
    out = []
    for m in rx.finditer(texto):
        sig, art, fin = ALIAS.get(m.group(1), m.group(1)), m.group(2), m.end()
        out.append((sig, art, m.start(), fin))
        if RX_NUMERAL.match(texto[fin:]):
            continue
        while (c := RX_CONT.match(texto[fin:])):
            out.append((sig, c.group(1), fin + c.start(1), fin + c.end()))
            fin += c.end()
    return out


def atribuir(linea: str, pos: int, desde: int, citas) -> tuple[str | None, str | None]:
    """A qué (sigla, artículo) se refiere la huella en `pos`: la última cita entre la
    huella anterior (`desde`) y ésta; si no hay, el último número suelto del tramo con
    la última sigla de la línea."""
    en_tramo = [c for c in citas if desde <= c[2] < pos]
    if en_tramo:
        return en_tramo[-1][0], en_tramo[-1][1]
    tramo = re.sub(r"\([^)]*\)", "", linea[desde:pos])
    nums = re.findall(_NUM, tramo)
    previas = [c for c in citas if c[2] < desde]
    return (previas[-1][0] if previas else None), (nums[-1] if nums else None)


RX_BLOQUE = re.compile(r"^\s*$|^(\||#|>|```|[-*+] |\d+[.)] )")


def lineas_logicas(texto: str) -> list[tuple[int, str]]:
    """Une las líneas que el markdown lee como un solo párrafo (una viñeta partida en
    dos sigue siendo la misma cita). Devuelve (nº de la primera línea física, texto)."""
    out: list[tuple[int, str]] = []
    for n, linea in enumerate(texto.splitlines(), 1):
        if out and linea.strip() and not RX_BLOQUE.match(linea) and out[-1][1].strip() \
                and not out[-1][1].lstrip().startswith(("|", "#", "```")):
            out[-1] = (out[-1][0], out[-1][1] + " " + linea.strip())
        else:
            out.append((n, linea))
    return out


def verificar_texto(texto: str, idx: dict, cnos: list[dict], *, existencia: bool,
                    rector: bool) -> tuple[list[str], list[str]]:
    """Devuelve (hallazgos, avisos) con número de línea."""
    rx = rx_siglas(idx["arts"].keys())
    huellas, arts = idx["huella"], {k: set(v) for k, v in idx["arts"].items()}
    en_cno = set().union(*(c["cadena"] for c in cnos)) if cnos else set()
    hallazgos, avisos = [], []
    def base(sig, art):
        """«CE 264.4» es el artículo 264, numeral 4 — salvo que el corpus numere así
        (COOTAD-2026 198.1)."""
        if art and "." in art and sig in arts and art not in arts[sig] and art.split(".")[0] in arts[sig]:
            return art.split(".")[0]
        return art

    for n, linea in lineas_logicas(texto):
        citas = [(s, base(s, a), i, f) for s, a, i, f in citas_de(linea, rx)]
        desde = 0
        for m in RX_HUELLA.finditer(linea):
            h = m.group(1)
            sig, art = atribuir(linea, m.start(), desde, citas)
            explicita = any(desde <= c[2] < m.start() for c in citas)
            desde = m.end()
            fila = huellas.get(h)
            if fila is None:
                if sig and art and explicita:
                    hallazgos.append(f"L{n}: {sig} {art} `{h}` — la huella NO existe en el corpus "
                                     "(¿obsoleta tras una reingesta o inventada?)")
                continue
            c_sig, c_art, c_txt = fila
            if art and c_art and art != c_art or (sig and art and c_sig != sig and art == c_art):
                hallazgos.append(f"L{n}: se cita {sig or '?'} {art} con `{h}`, pero esa huella es "
                                 f"{c_sig} {c_art}: «{c_txt[:110]}…»")
        citas = [c for c in citas if not re.fullmatch(r"\d\.0", c[1])]   # «LOTAIP 2.0» es versión
        for sig, art, *_ in citas:
            if existencia and sig in arts and art not in arts[sig] and (sig, art) not in en_cno:
                hallazgos.append(f"L{n}: {sig} {art} — el artículo no está en el corpus")
        if rector and citas and "concordancia" not in _plano(linea):
            palabras = set(re.findall(r"[a-z]{5,}", _plano(linea)))
            for cno in cnos:
                if len(cno["claves"] & palabras) < min(2, len(cno["claves"])):
                    continue          # la materia se decide por dos palabras propias del título
                fuera = sorted({f"{s} {a}" for s, a, *_ in citas
                                if (s, a) not in en_cno and (s, a) not in cno["cadena"]})
                if fuera:
                    cadena = " · ".join(f"{s} {a}" for s, a in sorted(cno["cadena"]))
                    avisos.append(f"L{n}: la línea trata «{cno['titulo']}» ({cno['id']}) y cita "
                                  f"{', '.join(fuera)}, que ninguna CNO encadena. Cadena rectora: "
                                  f"{cadena}. ¿Es rector, eslabón faltante o concordancia?")
    return hallazgos, avisos


# ── Entradas ───────────────────────────────────────────────────────────────────
def _texto_del_hook(d: dict) -> tuple[str, str]:
    ti = d.get("tool_input", {}) or {}
    ruta = str(ti.get("file_path", ""))
    if "edits" in ti:
        return ruta, "\n".join(e.get("new_string", "") for e in ti["edits"])
    return ruta, str(ti.get("new_string", ti.get("content", "")))


def modo_hook() -> int:
    try:
        # En Windows la entrada llega con la página de códigos de la consola: se lee en
        # bytes y se decodifica UTF-8, o «·» y las tildes rompen la lectura de las citas.
        ruta, texto = _texto_del_hook(json.loads(sys.stdin.buffer.read().decode("utf-8", "replace")))
    except Exception:  # noqa: BLE001
        return 0
    if not re.search(r"\.(md|ya?ml)$", ruta, re.I) or not texto.strip():
        return 0
    idx = cargar_indice()
    if idx is None:
        return 0                       # sin corpus el hook no bloquea: lo dice el gate
    hallazgos, avisos = verificar_texto(texto, idx, cargar_cnos(), existencia=True, rector=True)
    if not hallazgos and not avisos:
        return 0
    cuerpo = "\n".join(["⛔ CITAS NORMATIVAS SIN VERIFICAR en lo recién escrito "
                        f"({Path(ruta).name}):"] + hallazgos + avisos +
                       ["Lee la cadena rectora (docs/brn CNO → data/acks → governance/qlep) y el "
                        "texto en el corpus ANTES de citar. Corrige o declara la concordancia."])
    if hallazgos:
        print(json.dumps({"decision": "block", "reason": cuerpo}, ensure_ascii=False))
    else:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                 "additionalContext": cuerpo}}, ensure_ascii=False))
    return 0


def main(argv: list[str]) -> int:
    if "--hook" in argv:
        return modo_hook()
    rutas = [Path(a) for a in argv if not a.startswith("--")]
    idx = cargar_indice(usar_cache="--sin-cache" not in argv)
    if idx is None:
        print("  2 — no determinable: sin acceso al corpus (normal en CI)")
        return 2
    cnos = cargar_cnos()
    total = 0
    for ruta in rutas:
        h, a = verificar_texto(ruta.read_text(encoding="utf-8"), idx, cnos,
                               existencia="--existencia" in argv, rector="--rector" in argv)
        total += len(h)
        estado = "OK" if not h else f"{len(h)} hallazgo(s)"
        print(f"  {ruta.as_posix()}: {estado}" + (f" · {len(a)} aviso(s) de rector" if a else ""))
        for x in h + a:
            print(f"      {x}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
