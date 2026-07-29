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


# ── HOMÓGRAFOS ADMINISTRATIVOS ────────────────────────────────────────────────
# Términos que CONTIENEN un rubro técnico como subcadena pero significan otra cosa.
# Detectado 2026-07-29 al aplicar REGLA T1: descartado correctamente el proyecto de
# "las Pampas", el siguiente candidato para "MEJORA DEL PARQUE (LAS PAOLAS)" fue
# "Parqueaderos, Casilleros Judiciales" — porque **"parqueadero" contiene "parque"**.
# Un estacionamiento no es un área verde. Se neutralizan ANTES de clasificar, con el
# mismo criterio de REGLA 0: el filtro debe leer significado, no coincidencia de letras.
HOMOGRAFOS = {
    "parqueaderos": " estacionamientos ", "parqueadero": " estacionamiento ",
    "plantas de tratamiento": " depuradoras ", "planta de tratamiento": " depuradora ",
    "socializacion": " difusion ", "socializar": " difundir ",
}


def _sin_unidad_ejecutora(p_norm: str) -> str:
    """Limpia el texto POA normalizado de ruido que no describe el objeto del gasto.

    Dos capas: (a) REGLA 0 — el nombre de la dirección responsable, porque si no todo
    proyecto hereda la afinidad temática de su unidad y el filtro clasifica por
    CONTINENTE en vez de por CONTENIDO; (b) homógrafos administrativos, porque
    coincidir letras no es reconocer un rubro.
    """
    for u in UNIDADES_EJECUTORAS:
        p_norm = p_norm.replace(u, " ")
    for h, neutro in HOMOGRAFOS.items():
        p_norm = p_norm.replace(h, neutro)
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

# ── REGLA 3 · Ancla territorial · REGLA T1 del canon ───────────────────────────
# NO se inventa: `docs/corpus_externo/QUIRA_TERRITORIAL_SEMANTICS_v1.0.md` §IX fija
#
#     "parroquia → parroquia: PROHIBIDO (territorios distintos, sin base empírica)"
#     "cantón → parroquia: PERMITIDO (con proxy_de explícito)"
#
# El caso que lo destapó (Javo · 2026-07-29): "MEJORA DEL PARQUE (LAS PAOLAS)" se
# emparejó con "parque las Pampas". **Las Paolas es zona urbana de la parroquia
# Colorado; Las Pampas es comuna rural.** Territorios distintos, niveles distintos.
# El emparejador los cruzó por la palabra "parque".
#
# La lista plana anterior no bastaba: ninguno de los dos topónimos estaba en ella, así
# que el ancla no disparaba. Ahora cada topónimo declara su NIVEL de la jerarquía
# canónica de 7 niveles (§I), que es lo que permite razonar sobre comparabilidad.
TOPONIMOS: dict[str, tuple[int, str]] = {
    # Nivel 2 · Cantón. NO es un ancla territorial: es el UNIVERSO del análisis.
    # En una fila del POA del GAD, "Montecristi" es el membrete institucional, no la
    # ubicación del proyecto — 769 de 1027 filas lo contienen. Tratarlo como ancla
    # producía descartes indebidos contra el propio canon, que fija
    # "cantón → parroquia: PERMITIDO (con proxy_de explícito)" (§IX Regla T1).
    "montecristi": (2, "cantón"),
    # Nivel 3a · Parroquias COOTAD (§I y §VIII del canon territorial)
    "colorado": (3, "parroquia"),
    "la pila": (3, "parroquia"), "isabel muentes": (3, "parroquia"),
    "leonidas proano": (3, "parroquia"), "anibal san andres": (3, "parroquia"),
    "eloy alfaro": (3, "parroquia"),
    # Nivel 6 · Comunas / comunidades (§VIII — unidad social, no COOTAD ni INEC)
    "el arroyo": (6, "comuna"), "el chorrillo": (6, "comuna"),
    "los 3 bajos": (6, "comuna"), "las toallas": (6, "comuna"),
    "las carceles": (6, "comuna"),
    "las pampas": (6, "comuna"),              # confirmado por Javo · 2026-07-29
    # Nivel 5/7 · Barrios, urbanizaciones y sectores
    "las paolas": (5, "zona urbana"),          # parroquia Colorado · confirmado por Javo
    "bajo de la palma": (5, "sector"), "bajo del pechiche": (5, "sector"),
    "monterrey": (5, "sector"), "las marias": (5, "sector"), "nuevo prado": (5, "sector"),
    "los espinos": (5, "sector"), "pepa de huso": (5, "sector"), "san eloy": (5, "sector"),
    "horizonte azul": (5, "sector"), "la silla": (5, "sector"), "vergeles": (5, "sector"),
    "tierrasanta": (5, "sector"), "nueva kenedy": (5, "sector"), "el secal": (5, "sector"),
    "club pichincha": (5, "sector"), "estancia las palmas": (5, "sector"),
    "santa ana": (5, "sector"), "manantiales": (5, "sector"),
}
RE_SECTOR = re.compile(r"\b(" + "|".join(sorted(TOPONIMOS, key=len, reverse=True)) + r")\b", re.I)


# ── Detección GENÉRICA de ancla territorial ───────────────────────────────────
# El registro de topónimos nunca estará completo, y menos para 222 GAD. Pero el
# territorio casi siempre viene marcado por PATRÓN, no por nombre conocido:
#   demanda: "NECESITAMOS PARQUE (SECTOR NUEVO MONTECRISTI)" · "... - BARRIO SAN JOSE"
#   POA:     "... Parroquia La Pila" · "... sector Los Bajos"
# Detectar el patrón permite aplicar REGLA T0 sin conocer el topónimo: basta saber
# que la demanda SÍ dice dónde y que el proyecto NO lo dice.
RE_ANCLA = re.compile(
    r"(?:sector|barrio|comunidad|comuna|parroquia|ciudadela|urbanizacion|recinto|sitio)\s+"
    r"([a-z0-9ñ][a-z0-9ñ\s]{2,28})", re.I)
RE_ANCLA_PAREN = re.compile(r"[(•\-]\s*([A-ZÑ][A-ZÑ0-9\s]{3,30})\s*[)•]?\s*$")


def _ancla_territorial(texto: str) -> str | None:
    """Lugar declarado en el texto, por topónimo conocido o por patrón. None si no lo declara."""
    t = _territorios(texto)
    if t:
        return sorted(t)[0]
    n = _norm(texto)
    m = RE_ANCLA.search(n)
    if m:
        return " ".join(m.group(1).split())[:28]
    m = RE_ANCLA_PAREN.search(str(texto).strip())
    if m:
        return _norm(m.group(1)).strip()[:28]
    return None


def _mismo_lugar(a: str, b: str) -> bool:
    """True si dos anclas nombran el mismo territorio (solapamiento de palabras significativas)."""
    pa = {w for w in _norm(a).split() if len(w) > 3}
    pb = {w for w in _norm(b).split() if len(w) > 3}
    return bool(pa & pb)


def _territorios(texto: str) -> set[str]:
    """Anclas territoriales SUB-CANTONALES del texto (nivel ≥ 3).

    El cantón se excluye deliberadamente: es el universo del análisis, no una
    ubicación. Un proyecto de alcance cantonal PUEDE satisfacer una demanda
    parroquial — lo dice Regla T1. Incluirlo bloqueaba correspondencias válidas.
    """
    return {m.group(0).lower() for m in RE_SECTOR.finditer(_norm(texto))
            if TOPONIMOS.get(m.group(0).lower(), (0, ""))[0] >= 3}


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
# ── MRSPP · Modelo de Relaciones de Satisfacción de Política Pública (v3) ──────
# La pregunta ya no es "¿se parecen estos textos?" ni siquiera "¿qué política satisface
# esta demanda?", sino: **¿QUÉ TIPO DE SATISFACCIÓN PÚBLICA DEMUESTRA LA EVIDENCIA
# DISPONIBLE entre esta demanda ciudadana y esta intervención institucional?**
#
# QUIRA por tanto NO responde "sí corresponde". Responde, por ejemplo: *"la demanda
# presenta satisfacción instrumental documentada mediante componente operativo de
# limpieza declarado en el expediente"* — una afirmación de naturaleza distinta.
RELACIONES = {
    "directa":       "el proyecto ejecuta exactamente la política solicitada, en el territorio solicitado",
    "funcional":     "la acción produce el efecto buscado aunque el objeto sea distinto — con respaldo técnico DECLARADO en la ficha",
    "instrumental":  "existe un componente operativo explícito que contribuye al resultado (declarado en el expediente)",
    "complementaria": "contribuye indirectamente a las condiciones del entorno de la demanda",
    "nula":          "no existe evidencia verificable de relación",
}

# ── SATISFACCIÓN FUNCIONAL ENTRE FAMILIAS · exige declaración técnica ──────────
# Un proyecto de OTRA familia satisface funcionalmente una demanda SOLO si su ficha
# DECLARA el propósito técnico. No se presume; se lee.
#
#   reforestación                                    ⇏ mitigación de riesgo
#   reforestación + "estabilización de taludes"      ⇒ mitigación de riesgo  (funcional)
#   reforestación + "embellecimiento / ornamental"   ⇒ complementaria o nula
#
# Es el mismo rigor que ya regía la relación instrumental, extendido al nivel funcional:
# la diferencia entre auditar y suponer está en si el expediente lo dice.
DECLARACIONES_TECNICAS = {
    "riesgos":      ["estabilizacion de talud", "estabilizacion de taludes", "control de erosion",
                     "erosion", "proteccion de quebrada", "proteccion de cuenca", "encauzamiento",
                     "mitigacion", "gestion de riesgo", "muro de contencion", "dragado"],
    "agua":         ["planta de tratamiento", "tratamiento de agua", "aguas servidas", "captacion",
                     "conduccion", "red de distribucion"],
    "residuos":     ["disposicion final", "ruta de recoleccion", "barrido", "relleno sanitario"],
    "vialidad":     ["capa de rodadura", "mejoramiento vial", "mantenimiento vial"],
    "seguridad":    ["videovigilancia", "luminaria", "sistema de alarma"],
    "areas_verdes": ["mantenimiento de areas verdes", "riego", "reforestacion urbana"],
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

# Medios por los que el GAD actúa SIN ejecutar el objeto demandado. Marcan la frontera
# entre satisfacción DIRECTA (ejecuta la obra) y FUNCIONAL (otro objeto, mismo efecto):
# "siembra de árboles" no es una obra de protección de quebradas, pero puede producir
# su efecto si la ficha declara el propósito técnico.
MEDIOS_NO_EJECUTORES = ["adquisicion", "compra", "suministro", "insumo", "dotacion",
                        "entrega", "siembra", "plantacion", "reforestacion", "arriendo"]

# Proyectos genéricos del POA: enunciados institucionales que no describen una obra ni
# un servicio concreto. Emparejan con todo y no satisfacen ninguna demanda específica.
PROYECTOS_GENERICOS = [
    "actividades que promueven la participacion", "fortalecimiento institucional",
    "desarrollo institucional", "gestion administrativa", "apoyo a la gestion",
    "coordinacion interinstitucional", "asistencia tecnica general",
]

# Rubros estructurales: no satisfacen directamente, pero mejoran condiciones.
RUBROS_ESTRUCTURALES = ["catastr", "planificacion", "ordenamiento", "estudio", "diagnostico",
                        "actualizacion", "sistema de informacion", "normativa"]


def evaluar_relacion(demanda: str, proyecto_poa: str) -> tuple[str, str]:
    """Clasifica el TIPO DE SATISFACCIÓN del proyecto respecto de la demanda (MRSPP).

    Devuelve (tipo, motivo) con tipo ∈ directa · funcional · instrumental ·
    complementaria · nula. Ningún nivel se presume: cada uno exige su evidencia.
    """
    # REGLA 0: se juzga el OBJETO del gasto, nunca la dirección que lo ejecuta.
    d, p = _norm(demanda), _sin_unidad_ejecutora(_norm(proyecto_poa))
    fam = _familia_de(d)

    # ── REGLA T0 · EL TERRITORIO ES CONSTITUTIVO DE LA DEMANDA ──────────────────
    # Validación de campo de Javo (2026-07-29, precisión 12%): el motor emparejaba
    # "parque en Nuevo Montecristi" con "parque las Pampas" y lo llamaba DIRECTA.
    #
    #   "la única relación es que en ambas se pide un parque. NO, eso no es incorporar
    #    las necesidades ciudadanas a la planificación: son distintos lugares."
    #
    # Una demanda ciudadana NO es "X": es **"X en el lugar Y"**. El lugar no es un
    # atributo secundario que refine el match — es parte del objeto demandado. Si el
    # proyecto ejecuta X en otro lugar, o no dice dónde, **no atendió esa demanda**.
    #
    # El contraste que lo prueba (caso 5, el único directo que Javo validó):
    #   "tapas de alcantarillado LA PILA" ↔ "alcantarillado Parroquia LA PILA"  → SÍ
    # Ambos lados declaran el MISMO territorio. Ésa es la condición.
    anc_d, anc_p = _ancla_territorial(demanda), _ancla_territorial(proyecto_poa)
    ter_d, ter_p = ({anc_d} if anc_d else set()), ({anc_p} if anc_p else set())
    if ter_d:
        if not ter_p:
            # No es incompatibilidad: es INDETERMINACIÓN. El POA no dice dónde ejecuta
            # (99% de las filas · OBS-020), así que la correspondencia no es verificable
            # ni afirmable. Javo: "esa opacidad hace que no se pueda determinar si las
            # peticiones fueron atendidas realmente en POA, PAC y presupuesto."
            return "nula", (f"inverificable_territorialmente: la demanda se ancla en "
                            f"'{sorted(ter_d)[0]}' y el proyecto NO declara territorio "
                            f"(alimenta el CVI · OBS-020)")
        if not _mismo_lugar(anc_d, anc_p):
            return "nula", (f"territorio_incompatible (REGLA T1): demanda en '{anc_d}' "
                            f"vs proyecto en '{anc_p}' — lugares distintos")

    # ── Proyectos genéricos institucionales: no satisfacen una demanda concreta ──
    # 6 de las 8 'complementarias' rechazadas por Javo emparejaban contra el mismo
    # proyecto: "Desarrollo de actividades que promueven la participación ciudadana".
    # Es el patrón del membrete y de la unidad ejecutora, por tercera vez: texto
    # institucional genérico que empareja con cualquier cosa.
    if any(g in p for g in PROYECTOS_GENERICOS):
        return "nula", ("proyecto_generico_institucional: no describe una obra o servicio "
                        "concreto que pueda satisfacer una demanda")

    # ── COMPLEMENTARIA se evalúa PRIMERO: un proyecto estructural (catastro,
    # planificación, ordenamiento) mejora las condiciones del entorno aunque no
    # satisfaga el objeto. Clasificarlo como administrativo-nulo perdería la relación.
    if any(e in p for e in RUBROS_ESTRUCTURALES):
        return "complementaria", "proyecto estructural: contribuye a las condiciones del entorno, no ejecuta el objeto"

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
            # ★ FUNCIONAL ENTRE FAMILIAS — el rubro es ajeno, PERO la ficha declara el
            #   propósito técnico que produce el efecto buscado. Se lee, no se deduce.
            #   (caso reforestación ↔ mitigación de riesgo · criterio de Javo 2026-07-29)
            decl = [t for t in DECLARACIONES_TECNICAS.get(fam, []) if t in p]
            if decl:
                return "funcional", (f"rubro ajeno, pero la ficha DECLARA '{decl[0]}': produce el "
                                     f"efecto buscado por la demanda '{fam}' (verificado, no presumido)")
            return "nula", f"demanda '{fam}' sin rubro afín ni propósito técnico declarado en la ficha"
        # partida de eventos pagando infraestructura → incompatible
        partidas = RE_PARTIDA.findall(p)
        if partidas and fam in ("areas_verdes", "vialidad", "agua", "riesgos"):
            planas = "".join(partidas).replace(".", "")
            if any(ev in planas for ev in PARTIDAS_EVENTOS):
                return "nula", "partida de eventos financiando infraestructura"
        # ── DIRECTA vs FUNCIONAL: la frontera es el OBJETO, no el efecto ──
        # DIRECTA   = el proyecto ejecuta el objeto demandado.
        # FUNCIONAL = el objeto es distinto pero produce el efecto buscado
        #             (adquisición, dotación, siembra… en vez de ejecutar la obra).
        medio = [k for k in MEDIOS_NO_EJECUTORES if k in p]
        if medio:
            return "funcional", (f"objeto distinto ('{medio[0]}') que produce el efecto buscado "
                                 f"por la demanda '{fam}'")
        return "directa", f"ejecuta el objeto de la demanda '{fam}' (rubro afín)"

    return "nula", "sin familia de demanda identificable — no se puede afirmar correspondencia"


def evaluar(demanda: str, proyecto_poa: str) -> tuple[bool, str]:
    """Compatibilidad con el cruce: pasa si la relación NO es nula."""
    tipo, motivo = evaluar_relacion(demanda, proyecto_poa)
    return tipo != "nula", f"{tipo}: {motivo}"
