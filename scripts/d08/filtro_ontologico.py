# -*- coding: utf-8 -*-
"""
scripts/d08/filtro_ontologico.py — Filtro Ontológico QUIRA v1
═══════════════════════════════════════════════════════════════════════════════
authority:
  parent: MARCO-TEORICO-001
  constitution_articles: [1, 2, 3, 9]
  type: TECNICA

★ EL SALTO ONTOLÓGICO (validación experta de Javo · 2026-07-28)
La validación de 25 casos arrojó **13 falsos positivos**. El diagnóstico NO es que
el embedding esté mal calibrado: es que responde a la pregunta equivocada.

    El embedding pregunta:  "¿qué texto se parece?"
    QUIRA debe preguntar:   "¿qué política pública SATISFACE esta demanda?"

No es lo mismo. La palabra «parque» puede parecerse a otra palabra, pero una
política pública debe compartir **finalidad · competencia · territorio · objeto de
gasto · programa institucional**. Eso ya no es NLP: es conocimiento institucional.

    ANTES:  embedding DECIDE
    AHORA:  embedding PROPONE (top-N candidatos) · el filtro ontológico DECIDE

CASO PARADIGMÁTICO detectado por Javo: la partida recurrente "Feriado carnaval ·
Espectáculos Culturales" emparejaba con CUALQUIER demanda corta o con ruido OCR
(recolección de basura, parques, limpieza, quebradas). Un metadato presupuestario
genérico capturaba todo.

CONEXIÓN CON LOS POSTULADOS
  · I  Biografía        → impide que la historia del dato se contamine con
                          proyectos que nunca tuvieron relación con la demanda.
  · II Congruencia      → obliga a respetar la lógica del clasificador
                          presupuestario oficial y del COOTAD.
  · III Patrimonio      → cada validación de Javo se vuelve REGLA REUTILIZABLE
                          para los 222 GAD. La revisión manual no se repite.

Uso:  importado por scripts/d08/cruzar_demandas.py
Dylus Lab © 2026
"""
from __future__ import annotations

import re
import unicodedata


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.lower())


# ── REGLA 1 · Matriz de incompatibilidad temática (objeto de intervención) ──────
# Familias temáticas: qué pide la ciudadanía vs a qué rubro puede corresponder.
FAMILIAS = {
    "residuos":      ["desecho", "basura", "recoleccion", "limpieza", "maleza", "escombro", "aseo"],
    "areas_verdes":  ["parque", "area verde", "areas verdes", "arboriz", "planta", "ornamental",
                      "jardin", "espacio publico", "recreativ"],
    "vialidad":      ["calle", "via", "vial", "bacheo", "asfalt", "adoquin", "acera", "bordillo",
                      "camino", "ciclovia"],
    "agua":          ["agua potable", "alcantarillado", "saneamiento", "aguas servidas", "pozo"],
    "seguridad":     ["seguridad", "vigilancia", "iluminacion", "alumbrado", "camara"],
    "social":        ["salud", "brigada", "medic", "educacion", "capacitacion", "adulto mayor",
                      "discapacidad", "joven"],
    "riesgos":       ["riesgo", "quebrada", "deslave", "inundacion", "muro", "talud"],
}

# Rubros del POA que JAMÁS satisfacen una demanda de infraestructura o servicio.
# (El caso que destapó Javo: "Feriado carnaval · Espectáculos" capturaba todo.)
RUBROS_INCOMPATIBLES = {
    "eventos": ["carnaval", "concierto", "espectaculo", "festej", "feriado", "artistic",
                "agasajo", "aniversario", "desfile", "reina", "festival"],
    "administrativo": ["suministro de oficina", "material de oficina", "accesorios de oficina",
                       "viatico", "capacitacion del personal", "remuneracion", "catastr"],
}

# Qué rubro SÍ corresponde a cada familia (whitelist positiva)
RUBROS_COMPATIBLES = {
    "residuos":     ["aseo", "desecho", "recoleccion", "ambiental", "limpieza", "relleno"],
    "areas_verdes": ["parque", "area verde", "urbaniza", "embellecim", "planta", "arboriz",
                     "espacio publico", "ornamental", "obras publicas", "mantenimiento"],
    "vialidad":     ["vial", "via", "calle", "asfalt", "adoquin", "obras publicas", "infraestructura",
                     "mantenimiento", "maquinaria"],
    "agua":         ["agua", "alcantarillado", "saneamiento", "potable"],
    "seguridad":    ["seguridad", "iluminacion", "alumbrado", "camara", "vigilancia"],
    "social":       ["salud", "social", "educacion", "brigada", "patronato", "inclusion"],
    "riesgos":      ["riesgo", "quebrada", "muro", "gestion de riesgo", "mitigacion", "obras publicas"],
}

# ── REGLA 2 · Clasificador presupuestario (partidas del Ministerio de Finanzas) ──
# Las demandas de infraestructura NO pueden pagarse con partidas de festejos o
# servicios personales. Se detecta la partida en el texto del POA.
RE_PARTIDA = re.compile(r"\b(\d{2}\.\d{2}\.\d{2}[\.\w]*|\b7[35]\d{4}\b)")
PARTIDAS_INFRAESTRUCTURA = ("750104", "750105", "750107", "730402", "730404", "730811", "840")
PARTIDAS_EVENTOS = ("730205", "730207", "730209", "730802")

# ── REGLA 3 · Ancla territorial ────────────────────────────────────────────────
RE_SECTOR = re.compile(
    r"\b(bajo de la palma|bajo del pechiche|la pila|monterrey|el chorrillo|las marias|"
    r"nuevo prado|los espinos|pepa de huso|san eloy|isabel muentes|leonidas proano|"
    r"aníbal san andres|anibal san andres|colorado|horizonte azul|la silla|vergeles|"
    r"tierrasanta|nueva kenedy|club pichincha|estancia las palmas|eloy alfaro)\b", re.I)


# Una demanda SÍ puede corresponder a un rubro de eventos si es explícitamente cultural.
_CULTURAL = ["cultura", "cultural", "fiesta", "festiv", "artist", "deportiv", "recreac",
             "aniversario", "tradicion", "banda", "concierto", "evento"]


def _es_demanda_cultural(d_norm: str) -> bool:
    return any(k in d_norm for k in _CULTURAL)


def _familia_de(texto: str) -> str | None:
    t = _norm(texto)
    mejor, mx = None, 0
    for fam, claves in FAMILIAS.items():
        n = sum(1 for k in claves if k in t)
        if n > mx:
            mejor, mx = fam, n
    return mejor


def evaluar(demanda: str, proyecto_poa: str) -> tuple[bool, str]:
    """Aplica el Filtro Ontológico. Devuelve (pasa, motivo).

    El embedding ya propuso este candidato; aquí se decide si una POLÍTICA PÚBLICA
    puede realmente satisfacer esa demanda. Determinístico, sin IA, sin costo.
    """
    d, p = _norm(demanda), _norm(proyecto_poa)
    fam = _familia_de(d)

    # REGLA 1 · incompatibilidad temática — el filtro que mata los falsos positivos
    #
    # ★ CORRECCIÓN (test 2026-07-28): la primera versión solo descartaba `if fam`, y 30
    # falsos positivos con "Feriado carnaval · Conciertos" sobrevivieron porque la demanda
    # no tenía familia detectable ("PROYECTO REALIZADO-EL CHORILLO") o el OCR la rompía
    # ("PARQLIE" en vez de "parque"). La regla correcta es la inversa y más estricta:
    # un rubro de eventos/administrativo NUNCA satisface una demanda, SALVO que la propia
    # demanda sea explícitamente cultural o administrativa. Sin familia detectable no se
    # puede AFIRMAR correspondencia — y ante la duda, no se afirma (Horizonte de Verdad).
    for grupo, marcas in RUBROS_INCOMPATIBLES.items():
        if any(m in p for m in marcas):
            if grupo == "eventos" and _es_demanda_cultural(d):
                continue                                  # demanda cultural ↔ evento: sí procede
            return False, (f"incompatibilidad_tematica: demanda '{fam or 'sin_familia'}' "
                           f"vs rubro '{grupo}'")

    # REGLA 1b · si se identificó familia, el proyecto debe pertenecer a un rubro compatible
    if fam:
        compat = RUBROS_COMPATIBLES.get(fam, [])
        if compat and not any(c in p for c in compat):
            return False, f"sin_rubro_compatible: demanda '{fam}' no halla rubro afín en el proyecto"

    # REGLA 2 · clasificador presupuestario
    partidas = RE_PARTIDA.findall(p)
    if partidas and fam in ("areas_verdes", "vialidad", "agua", "riesgos"):
        planas = "".join(partidas).replace(".", "")
        if any(ev in planas for ev in PARTIDAS_EVENTOS):
            return False, "partida_incompatible: infraestructura pagada con partida de eventos"

    # REGLA 3 · ancla territorial (penaliza, no descarta: el POA suele ser cantonal)
    sec_d = {m.group(0).lower() for m in RE_SECTOR.finditer(demanda)}
    sec_p = {m.group(0).lower() for m in RE_SECTOR.finditer(proyecto_poa)}
    if sec_d and sec_p and not (sec_d & sec_p):
        return False, f"territorio_incompatible: demanda en {list(sec_d)[:1]} vs proyecto en {list(sec_p)[:1]}"

    return True, "pasa_filtro_ontologico"
