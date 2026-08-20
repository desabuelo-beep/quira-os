"""
app/agents/d07/evidencia.py — Etapas de levantamiento de evidencia del pipeline d07
=========================================================================
Corrección (Javo + colega, 2026-07-22): esto NO es "una etapa de IA".
Son TRES responsabilidades cognitivas distintas, cada una con juicio real:

    1. Portal Navigator   — localizar la página/URL correcta del CD en el
                             portal (estructura cambia por GAD).
    2. Evidence Collector — descargar/leer el archivo real (PDF/CSV/HTML,
                             a veces escaneado, a veces enlace roto).
    3. Evidence Interpreter — juzgar lo recolectado: ¿está completo?
                             ¿es simulación o cumplimiento real? ¿el enlace
                             funciona? ¿hay inconsistencias internas?
                             (Instructivo Tabla 5 — vigencia/validez).

SEGUNDA CORRECCIÓN (Javo, 2026-08-17): *«Quira debe realizar todo esto de
manera independiente cuando se la manda a través de los comandos o botones
del sistema»*. Y resulta que para la fuente canónica **las tres etapas son
determinísticas**:

    OBS-QNKC-02 fijó el Portal de la DPE como fuente canónica de C5, y la DPE
    NO es un portal que haya que navegar: es una **API estructurada** que
    devuelve numeral, archivos, URL y fecha de publicación. No hay página que
    interpretar ni estructura que varíe por GAD.

Por eso `levantar_evidencia_local()` puebla `EvidenciaCD` **sin una sola
llamada a un modelo**, y d07 puede ejecutarse solo y sin costo de API. La vía
agéntica se conserva abajo para el caso que sí la necesita: un sujeto
obligado que publique fuera de la DPE.

DE DÓNDE SALE CADA CAMPO — todo con procedencia, nada inferido:

    existe          hay archivos del CD en ese período          índice DPE
    formato_archivo extensión del conjunto de datos             índice descargas
    campos_completos columnas útiles ≥ campos exigidos          catálogo v1.1.0
    fecha_dato      «FECHA ACTUALIZACIÓN DE LA INFORMACIÓN»     archivo de metadatos
    fecha_registro  `created_at` de la publicación              índice DPE
    enlaces_vivos   los enlaces del CSV resuelven               verificación de enlaces
    vigencia_ok     el dato corresponde al período              metadatos vs período
    validez_ok      el contenido es legible y estructurado      análisis de contenido
    url / sha256    la evidencia queda fijada                   índice descargas

LO QUE ESTE MÓDULO NO DECIDE: la **cobertura material** (¿el presupuesto trae
ingresos?) no se dobla dentro de `campos_completos`. Va por `componentes.py` y
produce hallazgos propios, porque SITA es la vara del órgano rector y la
cobertura material es una observación de QUIRA sobre la evidencia. Mezclarlas
haría que un hallazgo nuestro se presentara como calificación de la DPE.

Dylus Lab © 2026
"""
from __future__ import annotations

import csv
import datetime as _dt
import io
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

from .scoring import EvidenciaCD

RAIZ = Path(__file__).resolve().parents[3]

from app.agents import sujeto as _S            # noqa: E402
_INDICE = RAIZ / "data" / "lotaip" / "descargas_indice.json"
_CONTENIDO = RAIZ / "data" / "lotaip" / "contenido.json"
_ENLACES = RAIZ / "data" / "lotaip" / "enlaces.json"
_CATALOGO = RAIZ / "data" / "d07" / "catalogo_cd_d07_v1.1.0.yaml"

# (2026-08-18 · ADR-051) Aquí vivía una copia de los formatos de datos abiertos que
# ni siquiera se usaba: código muerto que además duplicaba un criterio normativo. Los
# formatos los declara `RO-VII-001` y los consume `reglas.formatos_datos_abiertos()`.
# Este módulo sólo nombra la extensión del archivo; calificar es de `scoring`.


def _norm(s: str) -> str:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").lower()
    return " ".join(s.split())


def _clave_numeral(etiqueta: str) -> str | None:
    """`Numeral 5-22` → `5`; `Art. 24 Gobiernos…` → `Art.24`.

    La DPE etiqueta los conjuntos igual que la guía los desarrolla, así que la
    correspondencia es directa y no hay que inventarla."""
    e = (etiqueta or "").strip()
    if _norm(e).startswith("art. 24") or _norm(e).startswith("art 24"):
        return "Art.24"
    if not _norm(e).startswith("numeral"):
        return None
    n = e.split(None, 1)[1].strip() if " " in e else ""
    return "5" if n == "5-22" else (n or None)


@lru_cache(maxsize=1)
def _catalogo() -> dict:
    import yaml
    cat = yaml.safe_load(_CATALOGO.read_text(encoding="utf-8"))
    porn: dict[str, dict] = {}
    for cd in cat["conjuntos_datos"]:
        num = str(cd.get("numeral_ley") or "")
        clave = "5" if num == "5+22" else ("Art.24" if num.startswith("Art") else num)
        porn[clave] = cd
        porn[cd["id"]] = cd
    return {"catalogo": cat, "por_clave": porn}


@lru_cache(maxsize=1)
def _datos() -> dict:
    def leer(p: Path, clave: str) -> list:
        if not p.exists():
            return []
        return json.loads(p.read_text(encoding="utf-8")).get(clave, [])
    return {
        "indice": leer(_INDICE, "archivos"),
        "contenido": leer(_CONTENIDO, "archivos"),
        "enlaces": {e["url"]: e for e in leer(_ENLACES, "enlaces")},
    }


def _fecha(txt: str) -> _dt.date | None:
    """La DPE mezcla `31/1/2025`, `2025-01-31` y `31-01-2025` en el mismo campo."""
    s = " ".join(str(txt or "").split())
    for pat, orden in ((r"(\d{4})-(\d{1,2})-(\d{1,2})", "ymd"),
                       (r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", "dmy")):
        m = re.search(pat, s)
        if m:
            a, b, c = m.groups()
            try:
                return (_dt.date(int(a), int(b), int(c)) if orden == "ymd"
                        else _dt.date(int(c), int(b), int(a)))
            except ValueError:
                return None
    return None


# Letras que el castellano sí usa. Cualquier otro carácter no-ASCII en un CSV
# administrativo ecuatoriano es, casi siempre, una decodificación equivocada.
_ESPERADAS = set("áéíóúüñÁÉÍÓÚÜÑ¿¡°ºª–—“”‘’…€$%/()·")


def _decodificar(crudo: bytes) -> str | None:
    """Elige la codificación por CALIDAD del resultado, no por orden de intento.

    `cp1252` y `latin-1` aceptan cualquier byte: nunca lanzan error, sólo
    devuelven texto equivocado. Probarlas antes que `cp850` fijaba la lectura
    corrupta —«Direcci¢n institucional»— como si fuera el texto real, y con ella
    se comparaban cabeceras y se buscaban términos. Es el mismo criterio que se
    aplicó al delimitador: gana el candidato que produce el resultado más
    coherente, no el primero que no falla."""
    mejor, mejor_txt = None, None
    for enc in ("utf-8-sig", "utf-8", "cp850", "cp1252", "latin-1"):
        try:
            t = crudo.decode(enc)
        except UnicodeDecodeError:
            continue
        raros = sum(1 for c in t if ord(c) > 127 and c not in _ESPERADAS)
        # UTF-8 es estricto: si decodifica sin error, es la respuesta. Para las
        # demás manda el recuento de caracteres imposibles en castellano.
        if enc.startswith("utf-8"):
            return t
        if mejor is None or raros < mejor:
            mejor, mejor_txt = raros, t
    return mejor_txt


def _leer_tabla(ruta: Path) -> list[list[str]]:
    """Lector tolerante. Las reglas vienen de la corrida del 2026-08-17:
    `cp850` antes que `latin-1` (hay exportaciones desde consola DOS) y el
    delimitador se elige por ESTABILIDAD de columnas, no por frecuencia —contar
    separadores partía una tabla de 9 columnas en 19 porque los textos llevan
    comas dentro."""
    if not ruta.exists():
        return []
    crudo = ruta.read_bytes()
    txt = _decodificar(crudo)
    if txt is None:
        return []
    mejor, filas_mejor = None, []
    for delim in (";", ",", "\t", "|"):
        try:
            filas = [f for f in csv.reader(io.StringIO(txt), delimiter=delim)
                     if any((c or "").strip() for c in f)]
        except csv.Error:
            continue
        if not filas:
            continue
        from collections import Counter
        anchos = Counter(len(f) for f in filas)
        ancho, veces = anchos.most_common(1)[0]
        if ancho < 2:
            continue
        p = (veces / len(filas), ancho)
        if mejor is None or p > mejor:
            mejor, filas_mejor = p, filas
    return filas_mejor


def _columnas_utiles(filas: list[list[str]]) -> int:
    """Las columnas vacías del final son artefacto de exportar desde Excel, no
    campos publicados: el directorio del numeral 2 trae 9 campos con nombre y 10
    columnas mudas detrás. Contarlas simulaba 19 campos donde la guía exige 9."""
    util = 0
    for f in filas:
        for j, c in enumerate(f):
            if (c or "").strip():
                util = max(util, j + 1)
    return util


def _tipo_archivo(nombre: str) -> str:
    """EL ORDEN IMPORTA: muchos archivos se llaman `…-datos-abiertos-metadatos.csv`
    y comprobar «datos abiertos» primero los clasificaba como conjunto de datos."""
    n = _norm(nombre)
    if "metadato" in n:
        return "metadatos"
    if "diccionario" in n:
        return "diccionario"
    if "conjunto" in n or "datos abiertos" in n:
        return "conjunto_de_datos"
    return "otro"


def levantar_evidencia_local(cd_id: str, anio: int, mes: int) -> EvidenciaCD:
    """Puebla `EvidenciaCD` desde la captura ya realizada. Determinístico, sin IA.

    Un CD sin archivos en el período devuelve `existe=False` — y eso significa
    **«no se halló publicación»**, nunca «no existe el hecho». La distinción es
    de ADR-042 §6 y la conserva el orquestador al redactar hallazgos."""
    cat = _catalogo()["por_clave"].get(cd_id) or {}
    d = _datos()

    archivos = [r for r in d["indice"]
                if r.get("anio") == str(anio) and r.get("mes") == mes
                and _clave_numeral(r.get("numeral", "")) ==
                ("Art.24" if cd_id == "CD-A24" else str(cat.get("numeral_ley", "")).replace("5+22", "5"))]
    if not archivos:
        return EvidenciaCD(existe=False, formato_archivo=None, campos_completos=False,
                           fecha_dato=None, fecha_registro=None)

    conjuntos = [r for r in archivos
                 if _tipo_archivo(r["archivo"]) == "conjunto_de_datos"]
    conjunto = conjuntos[0] if conjuntos else None
    metadato = next((r for r in archivos if _tipo_archivo(r["archivo"]) == "metadatos"), None)

    if conjunto is None:
        # La tríada existe a medias: hay metadatos y diccionario, falta lo que lleva
        # la información. No es lo mismo que no publicar nada, y se distingue.
        return EvidenciaCD(existe=False, formato_archivo=None, campos_completos=False,
                           fecha_dato=None, fecha_registro=None,
                           url=archivos[0].get("url"))

    fmt = Path(conjunto["archivo"]).suffix.lstrip(".").lower() or None
    filas = _leer_tabla(RAIZ / conjunto["ruta"]) if conjunto.get("ruta") else []

    # Un conjunto canónico puede publicarse en VARIOS archivos: el art. 24 reparte
    # sus dos secciones —resoluciones y actas— en ficheros distintos de 5 campos
    # cada uno. Medir un archivo suelto contra los 10 campos sumados marcaba
    # «integridad parcial» en una publicación que sí trae lo exigido.
    columnas = sum(_columnas_utiles(_leer_tabla(RAIZ / r["ruta"]))
                   for r in conjuntos if r.get("ruta")) if len(conjuntos) > 1 \
        else _columnas_utiles(filas)
    exigidos = len(cat.get("campos_exigidos") or [])
    # `campos_completos` compara CANTIDAD, que es lo verificable sin interpretar:
    # publicar más columnas no es defecto (el numeral 17 desglosa en dos lo que la
    # guía enuncia junto); publicar menos sí lo es.
    campos_completos = bool(exigidos) and columnas >= exigidos and len(filas) > 1

    fecha_dato = None
    if metadato and metadato.get("ruta"):
        for f in _leer_tabla(RAIZ / metadato["ruta"]):
            if f and "fecha actualizacion" in _norm(f[0]):
                fecha_dato = _fecha(f[1] if len(f) > 1 else "")
                break

    fecha_registro = None
    if conjunto.get("publicado"):
        fecha_registro = _fecha(str(conjunto["publicado"])[:10])

    # `enlaces_vivos`: los enlaces del CSV resuelven. Se cuenta como vivo el que
    # entrega el documento por CUALQUIER forma válida de pedirlo —un `/s/` de
    # Nextcloud devuelve el visor y el archivo cuelga de `/download`—, y NO se
    # penaliza lo que la captura no alcanzó a comprobar.
    urls = [u for f in filas[1:] for c in f
            for u in re.findall(r"https?://[^\s;,\"']+", c or "")]
    comprobados = [d["enlaces"].get(u.rstrip(".,;)")) for u in urls]
    comprobados = [e for e in comprobados if e]
    # ⚠️ SÓLO PENALIZA LO QUE ES DEL SUJETO OBLIGADO (2026-08-20). El cálculo
    # no miraba la procedencia: un enlace del GAD hacia SERCOP que devolviera
    # `acceso_restringido` le restaba calidad **al GAD**. Hoy sale bien por
    # casualidad —los 11 enlaces caídos son todos suyos— pero el día que una
    # fuente de tercero se degrade, Montecristi pagaría por ella.
    #
    # Es ADR-042 §6 aplicado al scoring: `fuente_no_disponible` habla de la
    # fuente, no del sujeto. La disponibilidad del portal de SERCOP no es un
    # hecho sobre la gestión de Montecristi.
    _dominios_propios = _S.dominios()
    rotos = [e for e in comprobados
             if e.get("estado") in ("enlace_roto", "acceso_restringido")
             and any(d in (e.get("url") or "") for d in _dominios_propios)]
    enlaces_vivos = not rotos

    # `vigencia_ok`: el dato declarado corresponde al período publicado. Sin fecha
    # declarada no se afirma lo contrario — se deja pasar y el hallazgo lo registra
    # el orquestador como «vigencia no declarada».
    vigencia_ok = True
    if fecha_dato:
        ref = _dt.date(anio, mes, 1)
        limite = (ref - _dt.timedelta(days=1)).replace(day=1)
        vigencia_ok = fecha_dato >= limite

    cont = next((r for r in d["contenido"]
                 if r.get("anio") == str(anio) and r.get("mes") == mes
                 and r.get("archivo") == conjunto["archivo"]), None)
    validez_ok = bool(cont) and cont.get("estado_contenido") in (
        "contenido_con_datos", "declaracion_de_ausencia")

    return EvidenciaCD(
        existe=True, formato_archivo=fmt, campos_completos=campos_completos,
        fecha_dato=fecha_dato, fecha_registro=fecha_registro,
        enlaces_vivos=enlaces_vivos, vigencia_ok=vigencia_ok, validez_ok=validez_ok,
        url=conjunto.get("url"), sha256=conjunto.get("sha256"))


def levantar_evidencia_portal(cd_id: str, municipio: str, anio: int, mes: int) -> EvidenciaCD:
    """Vía agéntica — para sujetos obligados que NO publican en la DPE.

    Sigue sin implementar y **no hace falta para el municipio 001**: su evidencia
    canónica está en la API de la DPE y se levanta con `levantar_evidencia_local`.
    Se conserva porque un GAD que publique sólo en su portal sí exigirá navegar e
    interpretar, y ahí las tres responsabilidades cognitivas vuelven a ser reales."""
    raise NotImplementedError(
        "Navigator + Collector + Interpreter — sólo para fuentes fuera de la DPE. "
        "Para la fuente canónica use levantar_evidencia_local(), que es determinística."
    )
