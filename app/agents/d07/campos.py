"""
app/agents/d07/campos.py — correspondencia campo por campo (etapa 5b del pipeline)
=========================================================================
POR QUÉ EXISTE (2026-08-18). Javo:

> *«Y así con todos los numerales: la revisión pormenorizada para contemplar todo
> lo que se exige a los GAD según la norma técnica.»*

Contar columnas no basta. Un conjunto puede publicar catorce columnas frente a
catorce campos exigidos y no traer los mismos catorce. La comprobación tiene que
ser **campo a campo**, y por eso no puede resolverse contando.

POR QUÉ ES DIFÍCIL, y por qué el primer intento se descartó. La guía enuncia
«Monto asignado» y el GAD publica `Asignado`; la guía pide «Código de la cuenta o
subcuenta contable» y el GAD escribe `Cuenta`. Son el mismo campo. Un comparador
por palabras compartidas produjo a la vez:

    falsos negativos  «Monto asignado» declarado ausente teniendo `Asignado`
    falsos positivos  «Fecha de recepción del donativo» emparejado con
                      `Enlace para descargar el documento`
    dobles            un solo `Fecha de inicio del viaje` cubriendo a la vez
                      «fecha de inicio» y «fecha de fin»

LAS TRES REGLAS QUE LO CORRIGEN

1. **Asignación 1:1.** Una columna publicada cubre como mucho un campo exigido.
   Sin esta regla, una tabla con la mitad de las columnas «cubría» todo.
2. **Similitud de secuencia sobre el núcleo léxico**, no intersección de
   palabras: descarta artículos y preposiciones y compara lo que queda.
3. **Tres estados, con umbral declarado.** `cubierto` · `revisar` ·
   `sin_correspondencia`. Lo dudoso no se resuelve a favor de nadie: se marca.

LÍMITE HONESTO. La correspondencia entre un enunciado normativo y un encabezado
de hoja de cálculo es **interpretación**, no medición. Por eso este módulo
produce una **señal de revisión**, no un incumplimiento: alimenta el criterio
`campos_completos` sólo cuando la ausencia es inequívoca, y en el resto marca
`revisar` para que un humano decida. Declararlo así es preferible a fabricar
hallazgos que no aguantan una discusión con el sujeto obligado.

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher

# Palabras que no discriminan: aparecen en casi todos los enunciados y, contadas
# como coincidencia, emparejan cualquier cosa con cualquier cosa.
_VACIAS = {
    "de", "del", "la", "el", "los", "las", "un", "una", "y", "o", "en", "para",
    "que", "se", "a", "con", "al", "su", "sus", "por", "lo", "the", "e",
    "correspondiente", "respectiva", "respectivas", "mediante", "cual", "cuales",
}

# ── PARÁMETROS TÉCNICOS DE LECTURA · NO son criterio normativo ──────────────────
# Declarado expresamente (ADR-051 §2): estos umbrales NO vienen de la RO y no deben
# venir de ella. La norma dice qué campos exige —eso lo declara `RO-VII-001` y lo
# consume `reglas.py`—; no dice con cuánto parecido léxico se reconoce un encabezado.
# Son de la misma familia que la detección de delimitador o de codificación: heurísticas
# de lectura de la evidencia, ajustables sin tocar el canon.
#
# La frontera importa. Si mañana alguien quisiera relajar el umbral para que un
# conjunto «cubra» más campos, estaría manipulando la LECTURA, no la exigencia — y por
# eso este módulo nunca declara un campo ausente: sólo `revisar`, que exige a un humano.
UMBRAL_CUBIERTO = 0.62
UMBRAL_REVISAR = 0.38


@dataclass
class Correspondencia:
    exigido: str
    publicado: str | None
    puntaje: float
    estado: str


@dataclass
class MapaCampos:
    cd_id: str
    correspondencias: list[Correspondencia] = field(default_factory=list)
    columnas_sin_usar: list[str] = field(default_factory=list)

    @property
    def cubiertos(self) -> int:
        return sum(1 for c in self.correspondencias if c.estado == "cubierto")

    @property
    def a_revisar(self) -> list[str]:
        return [c.exigido for c in self.correspondencias if c.estado == "revisar"]

    @property
    def sin_correspondencia(self) -> list[str]:
        return [c.exigido for c in self.correspondencias
                if c.estado == "sin_correspondencia"]


# Abreviaturas administrativas: el encabezado publica `No.` donde el enunciado
# normativo dice «Número secuencial». Sin resolverlas, dos numerales aparecían
# incumpliendo un campo que sí publican en su primera columna.
_ABREVIATURAS = {
    "no": "numero", "nro": "numero", "num": "numero", "n": "numero",
    "ruc": "ruc", "cod": "codigo", "dir": "direccion", "tel": "telefono",
    "ext": "extension", "art": "articulo", "usd": "monto",
}


def _raiz(t: str) -> str:
    """Plural → singular, de forma mínima y sin diccionario.

    La guía enuncia «Objetivo» y el GAD publica `Objetivos`; «Nombres y
    apellidos» frente a `Nombre y Apellido`. Son el mismo campo, y tratarlos
    como distintos produjo dos hallazgos falsos. Sólo se recorta la marca de
    plural: no se lematiza más, porque cada paso extra añade riesgo de unir
    palabras que la norma distingue."""
    if len(t) > 4 and t.endswith("es"):
        return t[:-2]
    if len(t) > 3 and t.endswith("s"):
        return t[:-1]
    return t


def _tokens(s: str) -> list[str]:
    s = "".join(c for c in unicodedata.normalize("NFD", str(s or ""))
                if unicodedata.category(c) != "Mn").lower()
    s = re.sub(r"[^\w\s]", " ", s)
    fuera = []
    for t in s.split():
        # Se recorta la nota al pie que la guía adhiere a algunos campos
        # («Lugar de la audiencia / reunión7»), ajena al enunciado.
        t = t.rstrip("0123456789") or t
        if t in _VACIAS:
            continue
        fuera.append(_raiz(_ABREVIATURAS.get(t, t)))
    return fuera


def _similitud(exigido: str, publicado: str) -> float:
    a, b = _tokens(exigido), _tokens(publicado)
    if not a or not b:
        return 0.0
    # Cobertura del campo PUBLICADO dentro del exigido: `Asignado` cubre por
    # completo el núcleo de «Monto asignado», y eso debe puntuar alto aunque el
    # enunciado normativo sea más largo. La media con la similitud de cadena
    # evita que una sola palabra común dispare la coincidencia.
    sa, sb = set(a), set(b)
    comunes = sa & sb
    cobertura = len(comunes) / min(len(sa), len(sb))
    cadena = SequenceMatcher(None, " ".join(a), " ".join(b)).ratio()
    return round(0.6 * cobertura + 0.4 * cadena, 4)


def emparejar(cd_id: str, exigidos: list[str],
              publicados: list[str]) -> MapaCampos:
    """Asignación 1:1 por mejor puntaje global, de mayor a menor.

    Se recorren todos los pares posibles y se toma el mejor disponible en cada
    paso: así una columna no puede reclamarse para dos campos, que era la falla
    del comparador anterior."""
    pares = sorted(
        ((_similitud(e, p), i, j) for i, e in enumerate(exigidos)
         for j, p in enumerate(publicados)),
        reverse=True)
    tomados_e: dict[int, tuple[int, float]] = {}
    tomados_p: set[int] = set()
    for punt, i, j in pares:
        if punt < UMBRAL_REVISAR:
            break
        if i in tomados_e or j in tomados_p:
            continue
        tomados_e[i] = (j, punt)
        tomados_p.add(j)

    m = MapaCampos(cd_id=cd_id)
    for i, e in enumerate(exigidos):
        if i not in tomados_e:
            m.correspondencias.append(
                Correspondencia(e, None, 0.0, "sin_correspondencia"))
            continue
        j, punt = tomados_e[i]
        m.correspondencias.append(Correspondencia(
            e, publicados[j], punt,
            "cubierto" if punt >= UMBRAL_CUBIERTO else "revisar"))
    m.columnas_sin_usar = [p for j, p in enumerate(publicados)
                           if j not in tomados_p]
    return m
