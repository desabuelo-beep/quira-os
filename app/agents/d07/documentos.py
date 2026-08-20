"""
app/agents/d07/documentos.py — el universo documental (etapa 7 del pipeline d07)
=========================================================================
POR QUÉ EXISTE (2026-08-18). Javo:

> *«Sabes que la norma manda a publicar las sesiones de concejo, no solo los
> resúmenes. […] Revisar todos los documentos del GAD —Excel, PDF, etc.— de los
> links para determinar su cumplimiento. Estás dejando de lado las normas, solo
> por encima, y eso es integral.»*

Y sobre quién debe hacerlo:

> *«QUIRA debe hacer todo este trabajo; Claude solo supervisa cuando entremos a
> gestión del sistema. El de hoy es largo, pero los mensuales serán más cortos,
> progresivos para los 222 GAD del país.»*

Por eso esta capacidad vive en el agente y no en un script auxiliar: la carga
inicial es pesada, la corrida mensual es incremental, y ninguna de las dos puede
depender de que alguien esté mirando.

EL PROBLEMA QUE RESUELVE. El conjunto de datos casi nunca contiene el documento:
contiene **un enlace** a él. Verificar el CSV y detenerse ahí valida el envase.
La primera lectura de los documentos del art. 24 lo dejó claro:

    la guía exige   «Enlace para ver y descargar **el acta**»
    lo publicado    «RESOLUCIONES DE LA SESIÓN…» — un certificado de una a
                    cinco páginas, en 16 de 16 casos
    y el documento  acredita que el acta existe: una de sus resoluciones es
                    «Aprobar el Acta de Sesión Ordinaria Nro. 099»

Se publica la constancia de que el acta fue aprobada, no el acta.

QUÉ COMPRUEBA

    clase documental   ¿el documento es el acto que la norma pide?
    correspondencia    ¿el metadato del CSV coincide con el documento?
    serie correlativa  ¿falta alguna sesión de la numeración?
    procesabilidad     ¿es texto o un escaneo que nadie puede consultar?

DÓNDE VIVE LA EXIGENCIA. En el catálogo, no aquí: `clase_documental_exigida` se
deriva del texto literal de la obligación. Este módulo no decide qué debe
publicar un GAD — sólo comprueba lo que el canon ya declaró.

LÍMITE DECLARADO. Un PDF escaneado se marca `no_procesable` y **no se afirma
nada de su contenido**. Transcribirlo exige OCR y presupuesto; suponerlo sería
inventar evidencia, que es exactamente lo que QUIRA existe para no hacer.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import subprocess
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from . import reglas as R
from .evidencia import RAIZ, _catalogo, _clave_numeral, _datos, _norm, _tipo_archivo

DOCS = RAIZ / "data" / "lotaip" / "documentos"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")

PAUSA = 0.4
MAX_FALLOS_SEGUIDOS = 8

# ✅ DEUDA SALDADA (2026-08-18). Aquí vivía la lista de clases de acto como constante
# de módulo, y era criterio normativo puro: que un acta no sea una resolución lo decide
# la ley, no el lector. Estuvo declarada como deuda en ADR-051 porque su fundamento es
# el **art. 24** y ese artículo no tenía cadena; migrarla a `RO-VII-001` le habría
# atribuido al art. 19 una exigencia del 24.
#
# Con `CNO-VII-002` cerrada, las clases —y también los tipos de sesión admitidos, el
# patrón de la serie correlativa y qué hacer con un escaneo— se consumen de
# `RO-VII-003` a través de `reglas.py`. Si la norma reconociera mañana otra clase de
# acto, cambia la Regla Operativa; este archivo no se toca.


@dataclass
class Documento:
    url: str
    estado: str
    clase: str | None = None
    paginas: int = 0
    caracteres: int = 0
    es_imagen: bool = False
    correlativo: int | None = None
    tipo_sesion: str | None = None
    primera_linea: str = ""
    declarado: dict = field(default_factory=dict)
    sha256: str | None = None


@dataclass
class UniversoDocumental:
    cd_id: str
    anio: int
    seccion: str
    documentos: list[Documento] = field(default_factory=list)
    clase_exigida: str | None = None

    @property
    def conformes(self) -> list[Documento]:
        if not self.clase_exigida:
            return []
        return [d for d in self.documentos if d.clase == self.clase_exigida]

    @property
    def analizables(self) -> list[Documento]:
        return [d for d in self.documentos
                if d.estado == "descargado" and not d.es_imagen]

    @property
    def serie_faltante(self) -> list[int]:
        """Un salto en la numeración correlativa señala una sesión cuya
        documentación no se publicó. Es verificable sin interpretar nada."""
        nums = sorted({d.correlativo for d in self.documentos if d.correlativo})
        if len(nums) < 3:
            return []
        return [n for n in range(nums[0], nums[-1] + 1) if n not in set(nums)]


def _may(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").upper()
    return " ".join(s.split())


def clasificar(texto: str) -> str:
    """La clase de acto la reconoce el patrón que declara `RO-VII-003`, en el orden
    en que la regla los enumera — el orden importa: `resoluciones_de_sesion` debe
    evaluarse antes que `resolucion_legislativa`, o un certificado de sesión se
    clasificaría por su contenido en vez de por su naturaleza."""
    t = _may(texto)[:1500]
    for clase in R.clases_de_acto():
        if re.search(clase["patron"], t):
            return clase["id"]
    return "no_identificado"


def correlativo(texto: str) -> int | None:
    pat = (R.serie_correlativa() or {}).get("patron")
    if not pat:
        return None
    m = re.search(pat, _may(texto)[:800])
    return int(m.group(1)) if m else None


def tipo_sesion(texto: str) -> str | None:
    t = _may(texto)[:800]
    # Los tipos admitidos los declara la RO: el campo de la guía dice «ordinaria o
    # extraordinaria», y publicar otra cosa deja el dato sin declarar.
    for tipo in R.tipos_de_sesion_admitidos():
        if f"SESION {tipo.upper()}" in t:
            return tipo
    return None


def descargar(url: str, destino: Path, red: dict) -> str | None:
    """Nextcloud sirve el visor en `/s/XXXX` y el archivo en `/s/XXXX/download`.

    Pedir la primera forma y darla por documento produjo «0 de 430 enlaces
    accesibles» —falso—. Antes de dar por perdido un enlace se agota la forma
    válida de pedirlo."""
    if destino.exists() and destino.stat().st_size > 0:
        return "cache"
    time.sleep(PAUSA)
    red["intentos"] = red.get("intentos", 0) + 1
    u = url.rstrip("/")
    if "/index.php/s/" in u and not u.endswith("/download"):
        u += "/download"
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "45", "-A", UA,
             "--max-filesize", "40000000", "-o", str(destino),
             "-w", "%{http_code}|%{content_type}", u],
            capture_output=True, timeout=70)
        code, tipo = r.stdout.decode("utf-8", "replace").strip().split("|", 1)
        if code != "200":
            red["fallos"] = red.get("fallos", 0) + 1
            red["seguidos"] = red.get("seguidos", 0) + 1
            destino.unlink(missing_ok=True)
            return None
        red["seguidos"] = 0
        return tipo.split(";")[0]
    except Exception:
        red["fallos"] = red.get("fallos", 0) + 1
        red["seguidos"] = red.get("seguidos", 0) + 1
        destino.unlink(missing_ok=True)
        return None


def leer_pdf(p: Path) -> tuple[str, int, bool]:
    """(texto, páginas, es_escaneo). Un PDF que apenas rinde texto por página es
    una imagen: se declara y **no se transcribe**."""
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            n = len(pdf.pages)
            t = "\n".join((pg.extract_text() or "") for pg in pdf.pages[:40])
    except Exception:
        return "", 0, False
    return t, n, (n > 0 and len(t.strip()) / n < 120)


def analizar_documento(url: str, destino: Path, declarado: dict,
                       red: dict | None = None) -> Documento:
    red = red if red is not None else {}
    if red.get("seguidos", 0) >= MAX_FALLOS_SEGUIDOS:
        return Documento(url=url, estado="no_intentado_por_corte_de_fuente",
                         declarado=declarado)
    tipo = descargar(url, destino, red)
    if tipo is None:
        return Documento(url=url, estado="no_accesible", declarado=declarado)

    d = Documento(url=url, estado="descargado", declarado=declarado)
    crudo = destino.read_bytes()[:5]
    if crudo[:4] == b"%PDF":
        texto, paginas, escaneo = leer_pdf(destino)
        d.paginas, d.caracteres, d.es_imagen = paginas, len(texto.strip()), escaneo
        if escaneo:
            # No se afirma NADA sobre un documento que no se pudo leer.
            d.clase = "no_procesable"
        else:
            d.clase = clasificar(texto)
            d.correlativo = correlativo(texto)
            d.tipo_sesion = tipo_sesion(texto)
            lineas = texto.strip().splitlines()
            d.primera_linea = " ".join(lineas[0].split())[:150] if lineas else ""
    else:
        d.clase = "formato_no_analizado"
    return d


def verificar_universo(cd_id: str, anio: int, meses: list[int],
                       seccion: str | None = None,
                       limite: int = 0) -> list[UniversoDocumental]:
    """Abre los documentos que enlaza cada conjunto y los confronta con el canon."""
    import csv
    import io

    cat = _catalogo()["por_clave"].get(cd_id) or {}
    num = str(cat.get("numeral_ley") or "")
    clave = "Art.24" if num.startswith("Art") else num.replace("5+22", "5")
    d = _datos()
    red: dict = {"intentos": 0, "fallos": 0, "seguidos": 0}

    por_seccion: dict[str, UniversoDocumental] = {}
    for r in sorted(d["indice"], key=lambda x: (x.get("anio", ""), x.get("mes", 0))):
        if r.get("anio") != str(anio) or r.get("mes") not in meses:
            continue
        if _clave_numeral(r.get("numeral", "")) != clave:
            continue
        if _tipo_archivo(r["archivo"]) != "conjunto_de_datos" or not r.get("ruta"):
            continue

        sec = "actas" if "cta" in _norm(r["archivo"]) else "principal"
        if seccion and sec != seccion:
            continue
        u = por_seccion.setdefault(sec, UniversoDocumental(
            cd_id=cd_id, anio=anio, seccion=sec,
            clase_exigida=_clase_exigida(cat, sec)))

        crudo = (RAIZ / r["ruta"]).read_bytes()
        for enc in ("utf-8-sig", "utf-8", "cp1252", "cp850", "latin-1"):
            try:
                txt = crudo.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            continue
        filas = [f for f in csv.reader(io.StringIO(txt), delimiter=";")
                 if any((c or "").strip() for c in f)]
        if not filas:
            continue
        cab = [c.strip() for c in filas[0]]
        for k, f in enumerate(filas[1:], 1):
            url = next((x for c in f
                        for x in re.findall(r"https?://[^\s;,\"']+", c or "")), None)
            if not url:
                continue
            if limite and len(u.documentos) >= limite:
                break
            declarado = {cab[i]: (f[i] if i < len(f) else "")
                         for i in range(min(len(cab), len(f)))}
            destino = DOCS / cd_id / f"{anio}{r['mes']:02d}_{sec}_{k}.bin"
            u.documentos.append(analizar_documento(url, destino, declarado, red))
    return list(por_seccion.values())


def _clase_exigida(cat: dict, seccion: str) -> str | None:
    """Qué clase de acto exige la sección — lo declara `RO-VII-003`.

    Antes se deducía aquí recorriendo el catálogo y buscando la palabra «acta» en
    los campos. Funcionaba, pero era el módulo el que decidía qué constituye la
    exigencia; ahora la regla operativa lo dice, con el fundamento citado: el
    art. 24 §2 exige el acta porque su campo es «Enlace para ver y descargar **el
    acta**», y declara además qué NO la sustituye."""
    admite = R.clase_exigida("2" if seccion == "actas" else "1").get("admite") or []
    # Una sección con una sola clase admitida tiene exigencia inequívoca; si admite
    # varias (sección 1: resoluciones, ordenanzas, planes), no hay una única clase
    # que reclamar y la conformidad se evalúa contra el conjunto.
    return admite[0] if len(admite) == 1 else None


def clases_admitidas(seccion: str) -> list[str]:
    """Todas las clases que la sección admite. La sección 1 acepta varias —el
    literal habla de «resolución, ordenanza, reglamento, plan»—, así que un
    documento es conforme si pertenece a cualquiera de ellas."""
    return list(R.clase_exigida("2" if seccion == "actas" else "1").get("admite") or ())


def no_sustituible_por(seccion: str) -> list[str]:
    """Clases que NO satisfacen la exigencia aunque se les parezcan.

    Es el corazón del hallazgo del art. 24: un certificado de resoluciones no
    sustituye al acta, y la regla lo dice expresamente para que nadie tenga que
    argumentarlo caso por caso."""
    return list(R.clase_exigida("2" if seccion == "actas" else "1")
                .get("no_sustituible_por") or ())
