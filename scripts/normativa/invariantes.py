# -*- coding: utf-8 -*-
"""
scripts/normativa/invariantes.py — que una extracción no pueda salir plausible y falsa
══════════════════════════════════════════════════════════════════════════════════════
POR QUÉ EXISTE (2026-08-12). En una sola jornada, tres extracciones produjeron
resultados **completos, coherentes y equivocados, sin lanzar un solo error**:

  · un capturador imprimió `0 procesos` con la fuente caída — fallo y vacío
    devolvían el mismo `None`;
  · un monitoreo dio «40 de 40 documentos rotos» porque resolvía las rutas contra
    la raíz del sitio y no contra su carpeta;
  · un extractor leyó el objetivo de desarrollo como objetivo estratégico porque
    heredó el mapa de columnas de otra hoja desplazada.

Los tres se detectaron **por casualidad**, al notar un valor raro. Eso no es un
método. Y el riesgo no es teórico: el segundo habría publicado una acusación
falsa contra el municipio.

⚠️ NINGUNA LIBRERÍA DE EXTRACCIÓN EVITA ESTO. `openpyxl` leyó las celdas
perfectamente en los tres casos. El fallo no está en leer el archivo sino en
**interpretar su estructura** — y eso sólo se ataja comprobando el resultado
contra algo que se sepa cierto de antemano.

QUÉ HACE. Da a cada extractor un modo de declarar qué debe cumplirse para que su
salida sea creíble, y de **fallar ruidosamente** cuando no se cumple. Un
invariante roto no se corrige solo: se declara.

QUÉ NO HACE. No promete cero errores —eso sería la promesa equivocada—. Promete
que ninguna extracción pase sin haber declarado qué la hace correcta.

Uso:
    inv = Invariantes("POA 2025")
    inv.columna_con_forma(filas, "partida", r"\\d{6}", minimo=0.95)
    inv.texto_legible(textos)
    inv.cardinalidad("filas", len(filas), minimo=100)
    inv.exigir()          # lanza si algo falló · `.informe()` para sólo reportar

Dylus Lab © 2026
"""
from __future__ import annotations

import re
import sys
import unicodedata

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


class InvarianteRoto(RuntimeError):
    """La extracción produjo algo que contradice lo que se sabe de la fuente."""


# ══════════════════════════════════════════════════════════════════════════════
# ESTADOS, NO APROBADO/REPROBADO
#
# La primera versión de este módulo devolvía booleanos, y ese era exactamente el
# defecto que existe para impedir: un `False` no distingue «el texto está
# corrupto» de «no pude mirar la fuente» de «se me fue la calibración». Colapsar
# esas tres cosas en un binario es lo mismo que colapsar `no_reconciliado` con
# `sin_partida` — un límite del observador disfrazado de defecto del observado.
#
# El orden importa: al agregar varios invariantes, **gobierna el peor estado**,
# y `NO_OBSERVABLE` nunca se degrada a `CORRUPTO`. No haber podido mirar no es
# un hallazgo sobre lo mirado.
# ══════════════════════════════════════════════════════════════════════════════
VALIDADO = "validado"
PARCIAL = "parcialmente_validado"
REVISION = "requiere_revision"
CORRUPTO = "extraccion_corrupta"
NO_OBSERVABLE = "no_observable"          # no había nada que mirar
FUENTE_NO_ACCESIBLE = "fuente_no_accesible"

_GRAVEDAD = {VALIDADO: 0, PARCIAL: 1, NO_OBSERVABLE: 2,
             FUENTE_NO_ACCESIBLE: 3, REVISION: 4, CORRUPTO: 5}


class Invariantes:
    def __init__(self, sujeto: str, estricto: bool = True) -> None:
        self.sujeto = sujeto
        self.estricto = estricto
        self.resultados: list[dict] = []

    # ── registro ──────────────────────────────────────────────────────────────
    def _anotar(self, nombre: str, ok: bool, detalle: str, medido: str = "",
                estado_si_falla: str = REVISION) -> bool:
        self.resultados.append({"invariante": nombre, "ok": ok,
                                "estado": VALIDADO if ok else estado_si_falla,
                                "detalle": detalle, "medido": medido})
        return ok

    @property
    def estado(self) -> str:
        """El peor estado de los observados. Sin invariantes, no hay veredicto."""
        if not self.resultados:
            return NO_OBSERVABLE
        peor = max((r["estado"] for r in self.resultados),
                   key=lambda e: _GRAVEDAD.get(e, 0))
        if peor == VALIDADO:
            return VALIDADO
        return PARCIAL if all(r["ok"] or r["estado"] in (NO_OBSERVABLE,)
                              for r in self.resultados) else peor

    # ── invariantes de forma ──────────────────────────────────────────────────
    def columna_con_forma(self, valores, nombre: str, patron: str,
                          minimo: float = 0.8) -> bool:
        """La columna que dice ser X tiene la forma de X.

        Es el invariante que habría atrapado la hoja desplazada: si `partida` no
        contiene mayoritariamente 6 dígitos, esa columna **no es la partida**,
        por más que el mapa de títulos diga lo contrario."""
        vs = [str(v).strip() for v in valores if v not in (None, "")]
        if not vs:
            return self._anotar(f"forma:{nombre}", False,
                                "la columna llegó vacía: no hay nada que validar",
                                estado_si_falla=NO_OBSERVABLE)
        rx = re.compile(patron)
        n = sum(1 for v in vs if rx.fullmatch(v.replace(" ", "")))
        r = n / len(vs)
        return self._anotar(
            f"forma:{nombre}", r >= minimo,
            f"se esperaba ≥{minimo:.0%} con forma /{patron}/ — probable columna equivocada",
            f"{r:.0%} ({n}/{len(vs)})", estado_si_falla=CORRUPTO)

    def numeros_parseables(self, valores, nombre: str, minimo: float = 0.8) -> bool:
        """Si una columna numérica devuelve nulos en masa, casi siempre es la
        convención y no el dato. En esta carpeta conviven `1.866.275,79` (Numeral
        6) y `23,327,341.51` (eSIGEF): fijar una habría vaciado un año entero en
        silencio."""
        total = sum(1 for v in valores if v not in (None, ""))
        if not total:
            return self._anotar(f"numerico:{nombre}", False, "columna vacía",
                                estado_si_falla=NO_OBSERVABLE)
        ok = sum(1 for v in valores if isinstance(v, (int, float)))
        r = ok / total
        return self._anotar(
            f"numerico:{nombre}", r >= minimo,
            "demasiados nulos: sospechar convención decimal, no dato faltante",
            f"{r:.0%} ({ok}/{total})")

    # ── invariantes de contenido ──────────────────────────────────────────────
    def texto_legible(self, textos, minimo: float = 0.85, muestra: int = 400) -> bool:
        """Detecta el texto destrozado por una conversión.

        El corpus llegó a tener el POA con **53 % de texto roto** —columnas de
        tabla leídas carácter a carácter: «ild,t o ifvo o sr: ot aM cliee acj»—
        y de ahí se concluyó que el POA no anclaba al PDOT. Era falso: el defecto
        era de la ingesta (OBS-027).

        Se mide la proporción de palabras que parecen palabras. Un texto sano en
        español supera holgadamente el 85 %; uno troceado se hunde."""
        muestras = [t for t in textos if t and len(str(t)) > 30][:muestra]
        if not muestras:
            return self._anotar("texto_legible", False, "sin texto que evaluar",
                                estado_si_falla=NO_OBSERVABLE)

        # La primera versión de este invariante exigía ≥3 caracteres y vocal por
        # palabra, y marcó como roto un texto perfectamente sano: el español
        # administrativo está lleno de «de», «la», «y», «en». **Un gate con
        # falsos positivos se acaba ignorando, y entonces no protege nada.**
        #
        # El discriminante bueno es la LONGITUD MEDIA DE PALABRA. Un texto en
        # español ronda 5-7 caracteres; uno troceado carácter a carácter —«ild,t
        # o ifvo o sr: ot aM cliee acj»— se hunde por debajo de 3,5 porque
        # fragmenta cada término en sílabas sueltas.
        largos = [len(p) for t in muestras for p in re.findall(r"\S+", str(t))]
        if not largos:
            return self._anotar("texto_legible", False, "sin palabras que medir",
                                estado_si_falla=NO_OBSERVABLE)
        media = sum(largos) / len(largos)
        cortas = sum(1 for L in largos if L <= 3) / len(largos)
        # Segunda calibración. Sólo con media y palabras cortas, el gate acusó a
        # `RC-ASEO-2023` —un formulario de rendición de cuentas perfectamente
        # legible— porque los formularios están llenos de siglas, RUC y campos
        # breves. **Acusar a un documento sano es el mismo error que dar por
        # bueno uno roto**, sólo que hacia el otro lado.
        #
        # Lo que ningún texto troceado conserva son las PALABRAS LARGAS: donde se
        # lee «RENDICIÓN», «INSTITUCIÓN», «MONTECRISTI», hubo lectura correcta.
        largas = sum(1 for L in largos if L >= 6) / len(largos)
        ok = (media >= 4.2 and cortas <= 0.55) or largas >= 0.15
        return self._anotar(
            "texto_legible", ok,
            "texto probablemente destrozado por la conversión — revisar el ORIGINAL",
            f"media {media:.1f} car/palabra · {cortas:.0%} de ≤3 car · "
            f"{largas:.0%} de ≥6 car ({len(largos)} palabras)",
            estado_si_falla=CORRUPTO)

    def sin_repeticion_sospechosa(self, valores, nombre: str, maximo: float = 0.9) -> bool:
        """Una columna donde casi todo es el mismo valor suele ser una etiqueta
        arrastrada por celdas combinadas, no un dato. El POA 2025 repite
        «INDICADOR ESTRATÉGICO PDOT» en cada fila de la columna 7."""
        vs = [str(v).strip() for v in valores if v not in (None, "")]
        if len(vs) < 10:
            return self._anotar(f"variedad:{nombre}", True, "muestra corta", f"{len(vs)}")
        top = max(vs.count(v) for v in set(vs)) / len(vs)
        return self._anotar(
            f"variedad:{nombre}", top <= maximo,
            "un solo valor domina la columna: probable etiqueta arrastrada",
            f"valor dominante {top:.0%}")

    # ── invariantes de volumen ────────────────────────────────────────────────
    def cardinalidad(self, nombre: str, n: int, minimo: int = 1,
                     maximo: int | None = None) -> bool:
        ok = n >= minimo and (maximo is None or n <= maximo)
        return self._anotar(f"cardinalidad:{nombre}", ok,
                            f"se esperaba entre {minimo} y {maximo or '∞'}", str(n))

    def transporte_limpio(self, intentos: int, fallos: int) -> bool:
        """Un resultado obtenido con fallos de red no es un resultado: es un
        resultado parcial que aún no sabe que lo es."""
        return self._anotar("transporte", fallos == 0,
                            "hubo fallos de red: el resultado NO puede leerse como ausencia",
                            f"{fallos}/{intentos} fallidos",
                            estado_si_falla=FUENTE_NO_ACCESIBLE)

    def coherencia(self, nombre: str, condicion: bool, detalle: str,
                   medido: str = "") -> bool:
        """Invariante libre, para lo que sólo el extractor sabe de su fuente."""
        return self._anotar(nombre, bool(condicion), detalle, medido)

    # ── cierre ────────────────────────────────────────────────────────────────
    @property
    def rotos(self) -> list[dict]:
        return [r for r in self.resultados if not r["ok"]]

    def informe(self, silencioso_si_ok: bool = False) -> bool:
        if not self.rotos and silencioso_si_ok:
            return True
        print(f"  [{self.estado}] invariantes · {self.sujeto} "
              f"({len(self.resultados) - len(self.rotos)}/{len(self.resultados)})")
        for r in self.rotos:
            print(f"      ✗ {r['invariante']} → {r['estado']}: {r['detalle']}")
            print(f"        medido: {r['medido']}")
        return not self.rotos

    def exigir(self) -> None:
        """Falla ruidosamente. Preferible a un dato plausible y falso: **el error
        silencioso se publica; el ruidoso se corrige.**"""
        self.informe()
        if self.rotos:
            raise InvarianteRoto(
                f"{self.sujeto}: {len(self.rotos)} invariante(s) roto(s) — "
                + "; ".join(r["invariante"] for r in self.rotos))


def _sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", str(s))
                   if unicodedata.category(c) != "Mn").lower()
