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
                       "viatico", "capacitacion del personal", "remuneracion"],
}

# ── REGLA 0 · LA UNIDAD EJECUTORA NO ACREDITA EL OBJETO DEL GASTO ──────────────
# Hallazgo 2026-07-29. La fila del POA concatena `partida · descripción · unidad
# responsable`. "Obras Públicas" figuraba como rubro compatible de TRES familias
# (áreas verdes · vialidad · riesgos) — y en un GAD esa dirección ejecuta parques,
# viales, muros Y arriendo de edificios. Resultado: la demanda "INUNDACIONES-
# MANANTIALES" se emparejó con "Edificios, Locales, Parqueaderos, Casilleros
# Judiciales (Arrendamientos)" como relación DIRECTA de riesgos.
#
# DOCTRINA: **quién ejecuta no dice qué se hace.** El nombre de la unidad es un
# atributo administrativo, no técnico. Se elimina del texto ANTES de clasificar.
# Es el mismo error que los membretes (es_encabezado), un nivel más adentro: metadato
# institucional leído como contenido. Vale para los 222 GAD — todos tienen estas
# direcciones, y todos las arrastran en la columna de responsable.
UNIDADES_EJECUTORAS = (
    "direccion de obras publicas", "obras publicas", "direccion de planificacion",
    "gestion ambiental", "direccion financiera", "direccion administrativa",
    "talento humano", "secretaria general", "direccion de avaluos y catastros",
    "procuraduria sindica", "alcaldia", "direccion de servicios publicos",
)


def _sin_unidad_ejecutora(p_norm: str) -> str:
    """Quita el nombre de la dirección responsable del texto POA ya normalizado.

    Sin esto, todo proyecto de una dirección hereda la afinidad temática de su
    nombre y el filtro clasifica por CONTINENTE en vez de por CONTENIDO.
    """
    for u in UNIDADES_EJECUTORAS:
        p_norm = p_norm.replace(u, " ")
    return p_norm


# Qué rubro SÍ corresponde a cada familia (whitelist positiva)
# ★ Ningún token nombra una unidad administrativa (ver REGLA 0): todos son rubros
#   técnicos que describen el OBJETO del gasto.
RUBROS_COMPATIBLES = {
    "residuos":     ["aseo", "desecho", "recoleccion", "ambiental", "limpieza", "relleno"],
    "areas_verdes": ["parque", "area verde", "urbaniza", "embellecim", "planta", "arboriz",
                     "espacio publico", "ornamental"],
    "vialidad":     ["vial", "via", "calle", "asfalt", "adoquin", "infraestructura",
                     "maquinaria"],
    "agua":         ["agua", "alcantarillado", "saneamiento", "potable"],
    "seguridad":    ["seguridad", "iluminacion", "alumbrado", "camara", "vigilancia"],
    "social":       ["salud", "social", "educacion", "brigada", "patronato", "inclusion"],
    "riesgos":      ["riesgo", "quebrada", "muro", "gestion de riesgo", "mitigacion"],
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


# ── TIPOLOGÍA RELACIONAL v2 (aporte de Javo · 2026-07-28) ──────────────────────
# Javo observó: "¿y si SÍ existe relación entre recolección de basura y carnaval?
# Es feriado, aumenta el trabajo de las EP de aseo, hay más gente, eventos públicos".
# TIENE RAZÓN — y revela que v1 asumía relación UNÍVOCA cuando la política pública
# es MULTINIVEL. Un evento genera obligación operativa de aseo: residuos extra,
# contratación temporal, barrido posterior, contenedores.
#
# La administración pública no opera en ceros y unos. QUIRA deja de preguntar
# "¿coincide?" y pasa a preguntar "¿QUÉ FUNCIÓN CUMPLE este proyecto respecto de la
# demanda?". Eso es razonar como un auditor público, no como un buscador de texto.
#
# ★ RIGOR OBLIGATORIO: la relación instrumental se VERIFICA EN LA EVIDENCIA, no se
# presume. No se infiere que "todo evento genera limpieza": se lee si el proyecto
# DECLARA el componente. Sin declaración → nula (Horizonte de Verdad · No-Inferencia).
RELACIONES = {
    "directa":      "satisface explícitamente el objeto de la demanda",
    "funcional":    "provee el insumo o recurso necesario para cumplirla",
    "instrumental": "el proyecto activa un operativo que atiende la demanda (declarado en el expediente)",
    "indirecta":    "mejora condiciones estructurales asociadas",
    "nula":         "no existe conexión técnica ni operativa defendible",
}

# Marcadores de que un proyecto de OTRO rubro incorpora componentes de una familia.
# Ej.: un evento cultural que declara limpieza/barrido → relación instrumental con residuos.
COMPONENTES_OPERATIVOS = {
    "residuos":     ["limpieza", "barrido", "recoleccion", "aseo", "contenedor", "desecho",
                     "residuo", "basura", "disposicion final"],
    "seguridad":    ["seguridad", "vigilancia", "policia", "control", "iluminacion"],
    "salud":        ["salud", "brigada", "atencion medica", "sanitari"],
    "vialidad":     ["cierre vial", "senalizacion", "movilidad", "transito"],
}

# Rubros estructurales: no satisfacen directamente, pero mejoran condiciones.
RUBROS_ESTRUCTURALES = ["catastr", "planificacion", "ordenamiento", "estudio", "diagnostico",
                        "actualizacion", "sistema de informacion", "normativa"]


def evaluar_relacion(demanda: str, proyecto_poa: str) -> tuple[str, str]:
    """Clasifica la FUNCIÓN del proyecto respecto de la demanda. Devuelve (tipo, motivo).

    Tipología de 5 niveles — la política pública no es binaria:
      directa · funcional · instrumental · indirecta · nula
    """
    # REGLA 0: se juzga el OBJETO del gasto, nunca la dirección que lo ejecuta.
    d, p = _norm(demanda), _sin_unidad_ejecutora(_norm(proyecto_poa))
    fam = _familia_de(d)

    # ── territorio incompatible descarta en cualquier nivel ──
    sec_d = {m.group(0).lower() for m in RE_SECTOR.finditer(demanda)}
    sec_p = {m.group(0).lower() for m in RE_SECTOR.finditer(proyecto_poa)}
    if sec_d and sec_p and not (sec_d & sec_p):
        return "nula", f"territorio_incompatible: {list(sec_d)[:1]} vs {list(sec_p)[:1]}"

    # ── NIVEL D · INDIRECTA se evalúa PRIMERO: un proyecto estructural (catastro,
    # planificación, ordenamiento) mejora condiciones aunque no satisfaga el objeto.
    # Clasificarlo como administrativo-nulo perdería una relación real.
    if any(e in p for e in RUBROS_ESTRUCTURALES):
        return "indirecta", "proyecto estructural: mejora condiciones asociadas, no satisface el objeto"

    es_evento = any(m in p for m in RUBROS_INCOMPATIBLES["eventos"])
    es_admin = any(m in p for m in RUBROS_INCOMPATIBLES["administrativo"])

    # ── NIVEL C · INSTRUMENTAL — el caso que Javo detectó ──
    # El rubro principal es otro (evento/administrativo), PERO el proyecto DECLARA
    # componentes operativos de la familia demandada. Se verifica, no se presume.
    if (es_evento or es_admin) and fam:
        comps = COMPONENTES_OPERATIVOS.get(fam, [])
        hallados = [c for c in comps if c in p]
        if hallados:
            return "instrumental", (f"el proyecto declara componente '{hallados[0]}' que atiende "
                                    f"la demanda '{fam}' (verificado en el texto, no presumido)")
        # rubro ajeno SIN componente declarado → nula
        return "nula", (f"rubro '{'eventos' if es_evento else 'administrativo'}' sin componente "
                        f"operativo de '{fam}' declarado en el expediente")

    if es_evento and _es_demanda_cultural(d):
        return "directa", "demanda cultural ↔ proyecto cultural"
    if es_evento or es_admin:
        return "nula", "rubro ajeno sin familia de demanda identificable"

    # ── NIVEL A/B · DIRECTA o FUNCIONAL ──
    if fam:
        compat = RUBROS_COMPATIBLES.get(fam, [])
        if not any(c in p for c in compat):
            return "nula", f"demanda '{fam}' sin rubro afín en el proyecto"
        # partida de eventos pagando infraestructura → incompatible
        partidas = RE_PARTIDA.findall(p)
        if partidas and fam in ("areas_verdes", "vialidad", "agua", "riesgos"):
            planas = "".join(partidas).replace(".", "")
            if any(ev in planas for ev in PARTIDAS_EVENTOS):
                return "nula", "partida de eventos financiando infraestructura"
        # FUNCIONAL: provee insumo (adquisición/compra) en vez de ejecutar la obra
        if any(k in p for k in ("adquisicion", "compra", "suministro de plantas", "insumo")):
            return "funcional", f"provee el insumo necesario para '{fam}'"
        return "directa", f"rubro afín a la demanda '{fam}'"

    return "nula", "sin familia de demanda identificable — no se puede afirmar correspondencia"


def evaluar(demanda: str, proyecto_poa: str) -> tuple[bool, str]:
    """Compatibilidad con el cruce: pasa si la relación NO es nula."""
    tipo, motivo = evaluar_relacion(demanda, proyecto_poa)
    return tipo != "nula", f"{tipo}: {motivo}"
