# -*- coding: utf-8 -*-
"""
verificar_citas.py — ninguna cita normativa sin leer su fuente.

Nace de la falsación 43 (PANORAMA §5-duoquinquagies): se citó un artículo REAL
(COOTAD 266) como si fuera la norma que rige la rendición de cuentas, cuando la
cadena rectora (CNO-IX-001) ya estaba en el canon y no se leyó. Y de las citas del
QLEP y de los ACK que atribuían a un artículo lo que el artículo no dice.

ES UN MECANISMO DE INTEGRIDAD DOCUMENTAL, NO UNA AUTORIDAD NORMATIVA. Dice si una
cita corresponde a su fuente; no dice si una interpretación jurídica es verdadera.
La autoridad sigue siendo: norma/corpus → cadena canónica (BRN) → acto de autoridad.

LA REGLA (PANORAMA §5-quinquinquagies)
  Bloquea — hallazgo:
    1. HUELLA      la huella citada es de otro artículo, o no existe en el corpus.
    2. EXISTENCIA  el artículo citado no existe en el corpus (ni en una cadena CNO).
    3. LITERAL     un texto entre «» junto a su huella no está en el texto del artículo.
  Bloquea salvo declaración:
    4. CADENA      la línea trata la materia de una CNO y cita un artículo que ninguna
                   CNO encadena. Se resuelve DECLARANDO qué es: «concordancia»,
                   «eslabón faltante», «no encadenado», «fuera de la cadena». El gate
                   acepta además lo registrado en la línea base (historia anterior a este
                   mecanismo); todo lo nuevo debe declararse.
  Convención de escritura que la regla hace verificable:
    «»      sólo para texto de la ley (se contrasta con el artículo);
    “ ”     lo que otro afirma — un catálogo, una versión anterior, una persona;
    ~~ ~~   una cita retirada. Lo que va entre “ ” o tachado no se lee como cita propia.
  NO se verifica — y se dice:
    5. PARÁFRASIS  una cita con huella sin texto literal: la máquina prueba que el
                   artículo es el citado, NO que la paráfrasis diga lo que él dice. Se
                   cuenta como «contenido no verificado» y queda a validación humana.

Sólo lectura: la sesión con el corpus se abre read-only; la URI se resuelve con
brn_cno._uri y nunca se imprime. Sin corpus (CI) lo que exige el corpus (1, 2, 3) es
«no determinable»; la cadena (4) se determina igual con los YAML de la BRN.

Uso:
  python scripts/normativa/verificar_citas.py ARCHIVO [...]   # informe por archivo
  python scripts/normativa/verificar_citas.py --hook          # PostToolUse (Edit/Write)
  python scripts/normativa/verificar_citas.py --linea-base    # acto: registra la historia
Salida (convención de gates): 0 ok · 1 hallazgo · 2 no determinable.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import time
import unicodedata
from datetime import date
from pathlib import Path
from typing import NamedTuple

RAIZ = Path(__file__).resolve().parents[2]
BRN_DIR = RAIZ / "docs" / "brn"
LINEA_BASE = Path(__file__).with_name("citas_linea_base.json")
CACHE = Path(tempfile.gettempdir()) / "quira_verificar_citas_indice.json"
CACHE_TTL_S = 6 * 3600          # el corpus se reingiere rara vez; 6 h acotan la caducidad

# Siglas que otras capas usan para normas que el corpus nombra distinto.
ALIAS = {"LOAPAM": "LOPAM", "LOD": "LODISC", "LOMH": "LMH", "CPFP": "COPLAFIP"}

# Palabras de título de CNO demasiado generales para decidir la materia de una línea.
_VACIAS = {"obligacion", "sistema", "cantonal", "gobiernos", "autonomos", "descentralizados",
           "publica", "publico", "gestion", "ciudadana", "marco", "regla", "especifica",
           "derecho", "acceso", "informacion", "minima", "prioritaria", "articulacion",
           "traduccion"}

# Quien escribe declara qué es la cita que no está en la cadena rectora.
DECLARACIONES = ("concordancia", "eslabon faltante", "no encadenad", "sin encadenar",
                 "fuera de la cadena")

RX_HUELLA = re.compile(r"`([0-9a-f]{12})`")
_NUM = r"(\d+(?:\.\d+)?)(?!\d)(?!\s*%)"
RX_CONT = re.compile(
    r"^\s*(?:\*\*)?\s*(?:`[0-9a-f]{12}`)?\s*(?:\([^)]*\))?\s*(?:\*\*)?\s*"
    r"(?:,|·|\by\b|–|→)\s*(?:\*\*)?\s*" + _NUM)     # «LOSNCP 21 → 22»: la flecha renumera
RX_NUMERAL = re.compile(r"^\s*(?:\*\*)?\s*(?:n[úu]m\.|numeral|lit\.|literal|inciso)", re.I)
RX_BLOQUE = re.compile(r"^\s*$|^(\||#|>|```|[-*+] |\d+[.)] )")
RX_LITERAL = re.compile(r"«([^»]{12,})»")
RX_ELIPSIS = re.compile(r"\[\s*(?:…|\.\.\.)\s*\]|…|\.\.\.")
VENTANA_LITERAL = 60            # un «» cuenta como texto de la huella si abre a ≤60 caracteres de ella


def _plano(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _comparable(s: str) -> str:
    """Texto sin tildes, marcas ni puntuación: la forma en que se compara una cita literal."""
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", _plano(s)).split())


# ── Fuentes: corpus (lectura) y cadenas CNO ────────────────────────────────────
def _conectar():
    sys.path.insert(0, str(RAIZ / "scripts"))
    try:
        import brn_cno  # noqa: PLC0415  (se reutiliza _uri: no se reimplementa la lectura de secretos)
        import psycopg2  # noqa: PLC0415
        uri = brn_cno._uri()
        if not uri:
            return None
        conn = psycopg2.connect(uri, connect_timeout=25)
        conn.set_session(readonly=True, autocommit=True)
        return conn
    except Exception:  # noqa: BLE001 — sólo importa que no hubo corpus; nunca se imprime la URI
        return None


def cargar_indice(usar_cache: bool = True) -> dict | None:
    """{'huella': {h12: [sigla, art, texto]}, 'arts': {sigla: [art,...]}} o None."""
    if usar_cache and CACHE.exists() and time.time() - CACHE.stat().st_mtime < CACHE_TTL_S:
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    conn = _conectar()
    if conn is None:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT norma_sigla, articulo_num::text, left(sha256,12), "
                    "left(regexp_replace(contenido,'[[:space:]]+',' ','g'),180) "
                    "FROM public.normativa_corpus")
        filas = cur.fetchall()
    finally:
        conn.close()
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


def textos_de(huellas) -> dict[str, str]:
    """Texto completo del artículo al que pertenece cada huella (todas sus partes).
    Un fragmento sin número de artículo (tablas, NCI) aporta sólo su propio texto."""
    huellas = sorted(set(huellas))
    if not huellas:
        return {}
    conn = _conectar()
    if conn is None:
        return {}
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT left(a.sha256,12), string_agg(b.contenido, ' ' ORDER BY b.chunk_seq) "
            "FROM public.normativa_corpus a JOIN public.normativa_corpus b "
            "  ON b.norma_sigla = a.norma_sigla "
            " AND ((a.articulo_num IS NULL AND b.sha256 = a.sha256) "
            "      OR (a.articulo_num IS NOT NULL AND b.articulo_num = a.articulo_num)) "
            "WHERE left(a.sha256,12) = ANY(%s) GROUP BY 1", (huellas,))
        return {h: _comparable(t) for h, t in cur.fetchall()}
    finally:
        conn.close()


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


def siglas_sin_corpus(cnos: list[dict]) -> set[str]:
    """Sin corpus, las siglas salen de lo versionado: las cadenas CNO y el manifiesto."""
    siglas = {s for c in cnos for s, _ in c["cadena"]} | set(ALIAS)
    manifiesto = RAIZ / "scripts" / "normativa" / "manifest.py"
    if manifiesto.exists():
        siglas |= set(re.findall(r'"sigla":\s*"([^"]+)"', manifiesto.read_text(encoding="utf-8")))
    return siglas


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


RX_AJENO = re.compile(r"~~.+?~~|“[^”]*”")


def sin_citas_ajenas(linea: str) -> str:
    """Lo tachado (cita retirada) y lo que va entre “ ” (lo que otro afirma) no son citas
    de quien escribe: el registro tiene que poder nombrar una cita falsa para registrarla.
    Se borran conservando las posiciones."""
    return RX_AJENO.sub(lambda m: " " * len(m.group(0)), linea)


def huellas_en(texto: str) -> set[str]:
    return set(RX_HUELLA.findall(texto))


# ── La auditoría ───────────────────────────────────────────────────────────────
class Resultado(NamedTuple):
    hallazgos: list[str]                         # 1·2·3 — bloquean
    fuera_de_cadena: list[tuple[str, str]]       # 4 — (clave, mensaje): bloquean si no hay declaración
    literales: int                               # 3 — citas literales verificadas contra el artículo
    no_verificadas: int                          # 5 — con huella, sin texto literal: contenido NO verificado


def auditar(texto: str, *, idx: dict | None, cnos: list[dict], textos: dict | None = None,
            siglas=None, existencia: bool = True) -> Resultado:
    arts = {k: set(v) for k, v in idx["arts"].items()} if idx else {}
    huellas = idx["huella"] if idx else {}
    rx = rx_siglas(siglas if siglas is not None else arts.keys())
    en_cno = set().union(*(c["cadena"] for c in cnos)) if cnos else set()
    hallazgos, fuera, literales, no_verificadas = [], [], 0, 0

    def base(sig, art):
        """«CE 264.4» es el artículo 264, numeral 4 — salvo que el corpus numere así."""
        if art and "." in art and sig in arts and art not in arts[sig] and art.split(".")[0] in arts[sig]:
            return art.split(".")[0]
        return art

    for n, original in lineas_logicas(texto):
        linea = sin_citas_ajenas(original)
        crudas = citas_de(linea, rx)
        citas = [(s, base(s, a), i, f) for s, a, i, f in crudas]
        posiciones = [m for m in RX_HUELLA.finditer(linea)]
        desde = 0
        for k, m in enumerate(posiciones if idx else []):
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
                continue
            # 3 · ¿hay texto literal junto a la huella? Sólo el primer «» que abre cerca de
            # ella y antes de la huella siguiente: lo demás es de otra cita o de otra columna.
            hasta = posiciones[k + 1].start() if k + 1 < len(posiciones) else len(linea)
            lit = RX_LITERAL.search(linea, m.end(), hasta)
            if lit and lit.start() - m.end() <= VENTANA_LITERAL and textos is not None and h in textos:
                faltan = [p for p in (_comparable(x) for x in RX_ELIPSIS.split(lit.group(1)))
                          if len(p.split()) >= 3 and p not in textos[h]]
                if faltan:
                    hallazgos.append(f"L{n}: el texto entre «» junto a `{h}` ({c_sig} {c_art}) NO está "
                                     f"en el artículo: «{faltan[0][:90]}»")
                else:
                    literales += 1
            else:
                no_verificadas += 1
        # 2 · existencia
        citas = [c for c in citas if not re.fullmatch(r"\d\.0", c[1])]   # «LOTAIP 2.0» es versión
        crudas = [c for c in crudas if not re.fullmatch(r"\d\.0", c[1])]
        for sig, art, *_ in citas:
            if existencia and arts and sig in arts and art not in arts[sig] and (sig, art) not in en_cno:
                hallazgos.append(f"L{n}: {sig} {art} — el artículo no está en el corpus")
        # 4 · cadena rectora — se decide sobre la cita tal como se escribió, para que la
        # clave sea la misma con corpus o sin él
        if not cnos or not crudas or any(d in _plano(linea) for d in DECLARACIONES):
            continue
        palabras = set(re.findall(r"[a-z]{5,}", _plano(linea)))
        materias = [c for c in cnos if len(c["claves"] & palabras) >= min(2, len(c["claves"]))]
        if not materias:
            continue                  # la materia se reconoce por las palabras propias del título
        vistas = set()
        for s, a, *_ in crudas:
            a0 = a.split(".")[0]
            if f"{s} {a}" in vistas or (s, a) in en_cno or (s, a0) in en_cno:
                continue
            vistas.add(f"{s} {a}")
            cadenas = "; ".join(f"{c['id']}: " + " · ".join(f"{x} {y}" for x, y in sorted(c["cadena"]))
                                for c in materias)
            clave = f"{hashlib.sha1(original.strip().encode('utf-8')).hexdigest()[:12]}·{s} {a}"
            fuera.append((clave, f"L{n}: la línea trata «{materias[0]['titulo']}» y cita {s} {a}, que "
                                 f"ninguna CNO encadena. Cadena rectora — {cadenas}. Declara si es "
                                 "concordancia, eslabón faltante o no encadenado; o cita el rector."))
    return Resultado(hallazgos, fuera, literales, no_verificadas)


# ── El gate y su línea base ────────────────────────────────────────────────────
def universo_gate() -> list[Path]:
    """Lo que el gate [6/6] revisa. Una sola definición: la usan el gate y la línea base."""
    return [RAIZ / "docs" / "registry" / "PANORAMA_DOCUMENTAL_QUIRA.md",
            *sorted((RAIZ / "governance" / "qlep").glob("*.md")),
            *sorted((RAIZ / "data" / "acks").glob("*.yaml")),
            *sorted((RAIZ / "data" / "qtmp").glob("*.yaml")),
            *sorted(BRN_DIR.glob("*.yaml"))]


def leer_linea_base() -> set[str]:
    try:
        return set(json.loads(LINEA_BASE.read_text(encoding="utf-8"))["claves"])
    except Exception:  # noqa: BLE001
        return set()


def auditar_gate(con_corpus: bool = True) -> dict:
    """Lo que el gate certifica, separando lo que exige el corpus (1·2·3) de lo que se
    determina con lo versionado (4)."""
    try:
        cnos = cargar_cnos()
    except Exception:  # noqa: BLE001 — sin PyYAML la cadena no es determinable
        cnos = []
    idx = cargar_indice() if con_corpus else None
    rutas = universo_gate()
    textos = textos_de(set().union(*(huellas_en(r.read_text(encoding="utf-8")) for r in rutas))) if idx else None
    siglas = set(idx["arts"]) if idx else siglas_sin_corpus(cnos)
    base = leer_linea_base()
    out = {"corpus": idx is not None, "cadena": bool(cnos), "archivos": len(rutas), "hallazgos": [],
           "fuera_nuevas": [], "fuera_en_base": 0, "claves": [], "literales": 0, "no_verificadas": 0}
    for ruta in rutas:
        rel = ruta.relative_to(RAIZ).as_posix()
        r = auditar(ruta.read_text(encoding="utf-8"), idx=idx, cnos=cnos, textos=textos, siglas=siglas)
        out["hallazgos"] += [f"{rel} {h}" for h in r.hallazgos]
        for clave, msg in r.fuera_de_cadena:
            out["claves"].append(f"{rel}::{clave}")
            if f"{rel}::{clave}" in base:
                out["fuera_en_base"] += 1
            else:
                out["fuera_nuevas"].append(f"{rel} {msg}")
        out["literales"] += r.literales
        out["no_verificadas"] += r.no_verificadas
    return out


def registrar_linea_base() -> int:
    """ACTO, no rutina: registra como historia las citas fuera de cadena que ya existen.
    Quien lo corre debe justificarlo en el commit; el diff de este archivo lo deja a la vista."""
    g = auditar_gate()
    if not g["corpus"] or not g["cadena"]:
        print("  2 — no determinable: la línea base se registra con corpus y con la BRN")
        return 2
    LINEA_BASE.write_text(json.dumps({
        "registrada": date.today().isoformat(),
        "motivo": "citas fuera de la cadena rectora escritas ANTES del mecanismo (falsación 43). "
                  "Son historia registrada, no citas aprobadas: lo nuevo debe declararse.",
        "claves": sorted(set(g["claves"]))}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"  línea base: {len(set(g['claves']))} citas históricas fuera de cadena registradas")
    return 0


# ── Entradas ───────────────────────────────────────────────────────────────────
def _texto_del_hook(d: dict) -> tuple[str, str]:
    ti = d.get("tool_input", {}) or {}
    ruta = str(ti.get("file_path", ""))
    if "edits" in ti:
        return ruta, "\n".join(e.get("new_string", "") for e in ti["edits"])
    return ruta, str(ti.get("new_string", ti.get("content", "")))


def modo_hook() -> int:
    """El texto recién escrito no tiene historia: todo fuera de cadena debe declararse."""
    try:
        # En Windows la entrada llega con la página de códigos de la consola: se lee en
        # bytes y se decodifica UTF-8, o «·» y las tildes rompen la lectura de las citas.
        ruta, texto = _texto_del_hook(json.loads(sys.stdin.buffer.read().decode("utf-8", "replace")))
    except Exception:  # noqa: BLE001
        return 0
    if not re.search(r"\.(md|ya?ml)$", ruta, re.I) or not texto.strip():
        return 0
    try:
        cnos = cargar_cnos()
    except Exception:  # noqa: BLE001
        cnos = []
    idx = cargar_indice()
    siglas = set(idx["arts"]) if idx else siglas_sin_corpus(cnos)
    r = auditar(texto, idx=idx, cnos=cnos, textos=textos_de(huellas_en(texto)) if idx else None,
                siglas=siglas)
    if not r.hallazgos and not r.fuera_de_cadena:
        return 0
    cuerpo = "\n".join(["⛔ CITAS NORMATIVAS SIN VERIFICAR en lo recién escrito "
                        f"({Path(ruta).name}):"] + r.hallazgos + [m for _, m in r.fuera_de_cadena] +
                       ["Lee la cadena rectora (docs/brn CNO → data/acks → governance/qlep) y el "
                        "texto en el corpus ANTES de citar."])
    print(json.dumps({"decision": "block", "reason": cuerpo}, ensure_ascii=False))
    return 0


def main(argv: list[str]) -> int:
    if "--hook" in argv:
        return modo_hook()
    if "--linea-base" in argv:
        return registrar_linea_base()
    rutas = [Path(a) for a in argv if not a.startswith("--")]
    idx = cargar_indice(usar_cache="--sin-cache" not in argv)
    if idx is None:
        print("  2 — no determinable: sin acceso al corpus")
        return 2
    cnos = cargar_cnos()
    textos = textos_de(set().union(*(huellas_en(r.read_text(encoding="utf-8")) for r in rutas)))
    total = 0
    for ruta in rutas:
        r = auditar(ruta.read_text(encoding="utf-8"), idx=idx, cnos=cnos, textos=textos)
        total += len(r.hallazgos)
        print(f"  {ruta.as_posix()}: {'OK' if not r.hallazgos else f'{len(r.hallazgos)} hallazgo(s)'}"
              f" · {r.literales} literal(es) verificada(s) · {r.no_verificadas} sin texto literal"
              + (f" · {len(r.fuera_de_cadena)} fuera de cadena" if r.fuera_de_cadena else ""))
        for x in r.hallazgos + [m for _, m in r.fuera_de_cadena]:
            print(f"      {x}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main(sys.argv[1:]))
