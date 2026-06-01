"""
app/connectors/neo4j_qtmp.py — QUIRA OS · Sprint 3 Panel Estratégico
Conector Neo4j: cadena causal QTMP → datos listos para Layer 2.

ADR-013 (2026-05-31) — Mapeo canónico CONGELADO:
  GAP_10PCT     → Dom12 (Protección Social)      → p19_genero.py
  AGUA_POTABLE  → Dom10 (Territorio & Cobertura) → p10_territorio.py
  EQUIDAD       → Dom06 (Salud Institucional)    → m1_situacion.py
  TRANSPARENCIA → Dom07 (Transparencia)          → [Layer 2 pendiente] → municipal

Bloomberg Model — este módulo es INTERNO.
  ✓ Los campos 'narrativa' y 'fuente' siguen el lenguaje de gobernanza pública.
  ✗ Los IDs internos (circuit_id, indicador_ref, nodo IDs) NUNCA se exponen en UI.
  ✗ NUNCA mostrar: GAP_10PCT, SP_G10P_MCR, RES_G10P_04_MCR, IND_AGPT_01_MCR, etc.

Modo de operación:
  1. Intenta conectarse a Neo4j con credenciales de secrets.toml / env vars.
  2. Si Neo4j no disponible → fallback a datos confirmados del Gold Master v5.5.
  3. Todos los resultados fallback tienen estado_dato='confirmado' y fuente pública.

Dylus Lab © 2026 — DOCUMENTO INTERNO · QUIRA Operaciones
"""
from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# ── ADR-013: Mapeo canónico circuito → dominio — CONGELADO ───────────────────
# Fuente de verdad única en código. Cambiar requiere nuevo ADR.
CIRCUIT_DOMAIN_MAP: dict[str, dict[str, str]] = {
    "GAP_10PCT":     {"dominio": "Dom12", "modulo": "genero"},
    "AGUA_POTABLE":  {"dominio": "Dom10", "modulo": "territorio"},
    "EQUIDAD":       {"dominio": "Dom06", "modulo": "situacion"},
    "TRANSPARENCIA": {"dominio": "Dom07", "modulo": "municipal"},
}

# ── Circuitos disponibles ─────────────────────────────────────────────────────
CIRCUITS = list(CIRCUIT_DOMAIN_MAP.keys())

# ── Configuración conexión Neo4j ──────────────────────────────────────────────
_DEFAULT_URI  = "bolt://localhost:7687"
_DEFAULT_USER = "neo4j"


# ══════════════════════════════════════════════════════════════════════════════
# FALLBACK DATA — valores confirmados del Gold Master v5.5_TGI
# Estado: confirmado · Fuente: SIGEF / INEC / PDOT Bicentenario 2023
# Estos datos son la última línea de defensa cuando Neo4j no está disponible.
# Actualizar SOLO con nueva cédula presupuestaria o nuevo censo oficial.
# ══════════════════════════════════════════════════════════════════════════════

_FALLBACK: dict[str, dict[str, Any]] = {

    # ── GAP_10PCT → Dom12 ─────────────────────────────────────────────────────
    # Paradoja COOTAD_249: asignación VERDE, ejecución ROJO
    # Fuente: cédula presupuestaria GADMCM / Patronato nov-2025
    "GAP_10PCT": {
        "circuit_id":      "GAP_10PCT",           # INTERNO — no exponer en UI
        "dominio_id":      "Dom12",               # INTERNO
        "norma_sigla":     "COOTAD",              # INTERNO
        "norma_articulo":  "249",                 # INTERNO
        "norma_texto": (
            "Los gobiernos municipales asignarán al menos el 10 % de sus ingresos "
            "no tributarios para programas sociales dirigidos a grupos de "
            "atención prioritaria."
        ),
        "hallazgo": (
            "El municipio cumple el piso legal de asignación presupuestaria "
            "(20.84 % codificado — 2.08× el mínimo legal). Sin embargo, el "
            "Patronato Municipal ejecutó solo el 50 % de su presupuesto de "
            "inversión en 2025 — tercer año consecutivo por debajo del 85 % de umbral."
        ),
        "valor_principal":  50.0,
        "indicador_label": "Ejecución presupuestaria Patronato Municipal",
        "unidad":           "% ejecución",
        "semaforo":         "ROJO",
        "fuente":           "Sistema Integrado de Gestión Financiera (SIGEF) · noviembre 2025",
        "fecha_corte":      "noviembre 2025",
        "estado_dato":      "confirmado",
        "narrativa": (
            "El Art. 249 del COOTAD establece que el municipio debe asignar al menos el "
            "10 % de sus ingresos no tributarios a programas para grupos de atención "
            "prioritaria. Al corte noviembre 2025, el Patronato Municipal ejecutó el "
            "50 % de su presupuesto de inversión — 35 puntos bajo el umbral del 85 %. "
            "La asignación formal cumple la norma (20.84 %); la brecha es de ejecución "
            "institucional: aproximadamente $ 2 millones no llegaron a los grupos prioritarios. "
            "Serie histórica: 35 % (2023) → 54 % (2024) → 50 % (2025). "
            "Fuente: Sistema Integrado de Gestión Financiera · noviembre 2025."
        ),
        # Indicadores complementarios
        "asignacion_pct":   20.84,
        "asignacion_semaforo": "VERDE",
        "serie_historica":  {2023: 35.03, 2024: 53.77, 2025: 50.0},
        "umbral_verde":     85.0,
        "fuente_neo4j":     False,   # INTERNO — indica si dato viene de Neo4j o fallback
    },

    # ── AGUA_POTABLE → Dom10 ──────────────────────────────────────────────────
    # CE_264 (competencia exclusiva municipal) + CE_12 (derecho humano al agua)
    # Fuente: INEC Censo 2022 · PDOT Bicentenario 2023
    "AGUA_POTABLE": {
        "circuit_id":      "AGUA_POTABLE",        # INTERNO
        "dominio_id":      "Dom10",               # INTERNO
        "norma_sigla":     "CE",                  # INTERNO
        "norma_articulo":  "264",                 # INTERNO
        "norma_texto": (
            "Los gobiernos municipales tienen como competencia exclusiva la prestación "
            "de los servicios públicos de agua potable, alcantarillado y saneamiento "
            "ambiental en su circunscripción."
        ),
        "hallazgo": (
            "Solo el 34.9 % de las viviendas de Montecristi accede a la red pública de "
            "agua potable. El 60.19 % restante se abastece mediante tanqueros. "
            "Ninguna zona del cantón recibe servicio continuo (0 % continuidad 24/7)."
        ),
        "valor_principal":  34.9,
        "indicador_label": "Cobertura de agua potable por red pública",
        "unidad":           "% viviendas con acceso a red pública",
        "semaforo":         "ROJO",
        "fuente":           "INEC Censo de Población y Vivienda 2022",
        "fecha_corte":      "2022",
        "estado_dato":      "confirmado",
        "narrativa": (
            "El Art. 264 numeral 4 de la Constitución establece que el municipio es "
            "responsable exclusivo del servicio de agua potable. Al corte del Censo 2022, "
            "el 34.9 % de las viviendas de Montecristi accede a la red pública — "
            "55.1 puntos bajo el umbral de referencia del 90 %. El 60.19 % sin acceso "
            "a red pública depende de tanqueros para abastecerse. Ninguna zona del cantón "
            "recibe agua de forma continua: Montecristi y Aníbal San Andrés reciben "
            "servicio una vez por semana; Colorado, Leonidas Proaño y General Eloy Alfaro, "
            "una vez cada quince días. Meta PDOT Bicentenario 2027: 42.38 %. "
            "Fuente: INEC Censo 2022 · PDOT Bicentenario 2023."
        ),
        # Indicadores complementarios
        "continuidad_pct":   0.0,
        "continuidad_semaforo": "ROJO",
        "meta_pdot_2027":    42.38,
        "linea_base_pdot":   39.25,
        "umbral_verde":      90.0,
        "fuente_neo4j":      False,
    },

    # ── EQUIDAD → Dom06 ───────────────────────────────────────────────────────
    # COOTAD_228: criterios equidad territorial en distribución de inversión
    # Fuente: INEC Censo 2022 · SNP · PDOT Bicentenario 2023
    "EQUIDAD": {
        "circuit_id":      "EQUIDAD",             # INTERNO
        "dominio_id":      "Dom06",               # INTERNO
        "norma_sigla":     "COOTAD",              # INTERNO
        "norma_articulo":  "228",                 # INTERNO
        "norma_texto": (
            "Los presupuestos municipales se formularán aplicando criterios de equidad "
            "territorial: densidad poblacional, necesidades básicas insatisfechas, "
            "logros de desarrollo y brechas existentes."
        ),
        "hallazgo": (
            "La brecha de necesidades básicas insatisfechas entre zona urbana y rural "
            "es de 32 puntos porcentuales (21.3 % urbano vs 53.3 % rural). "
            "El indicador de redistribución social es del 79.7 % — 5.3 puntos bajo "
            "el umbral de referencia del 85 %."
        ),
        "valor_principal":  79.7,
        "indicador_label": "Redistribución de la inversión hacia sectores vulnerables",
        "unidad":           "% inversión hacia sectores vulnerables",
        "semaforo":         "AMARILLO",
        "fuente":           "INEC Censo 2022 · SNP · PDOT Bicentenario 2023",
        "fecha_corte":      "2022",
        "estado_dato":      "confirmado",
        "narrativa": (
            "El Art. 228 del COOTAD exige que la inversión municipal aplique criterios "
            "de equidad territorial, priorizando zonas con mayores necesidades básicas "
            "insatisfechas. Al corte del Censo 2022, la brecha entre zonas urbana y rural "
            "es de 32 puntos porcentuales: 21.3 % de NBI en zona urbana vs 53.3 % en zona "
            "rural (la zona rural multiplica por 2.5 la pobreza urbana). El 79.7 % de la "
            "inversión municipal llega a sectores vulnerables — 5.3 puntos bajo el umbral "
            "de referencia del 85 %. La pobreza multidimensional rural (67.9 %) casi "
            "triplica la urbana (23.0 %). "
            "Fuente: INEC Censo 2022 · SNP · PDOT Bicentenario 2023."
        ),
        # Indicadores complementarios
        "nbi_urbano":        21.3,
        "nbi_rural":         53.3,
        "brecha_nbi_pp":     32.0,
        "brecha_semaforo":   "ROJO",
        "pobreza_multi_urbana": 23.0,
        "pobreza_multi_rural":  67.9,
        "umbral_verde":      85.0,
        "fuente_neo4j":      False,
    },

    # ── TRANSPARENCIA → Dom07 ─────────────────────────────────────────────────
    # CE_18 (derecho a la información) + COOTAD_302 (rendición de cuentas)
    # Datos: pendiente verificación directa portal LOTAIP GADMCM
    # Nota interna: indicador central = H41_IOC (compuesto cumplimiento×actualización×comprensibilidad)
    "TRANSPARENCIA": {
        "circuit_id":      "TRANSPARENCIA",       # INTERNO — no exponer en UI
        "dominio_id":      "Dom07",               # INTERNO
        "norma_sigla":     "CE",                  # INTERNO
        "norma_articulo":  "18",                  # INTERNO
        "norma_texto": (
            "Todas las personas, en forma individual o colectiva, tienen derecho a "
            "buscar, recibir, intercambiar, producir y difundir información veraz, "
            "verificada, oportuna, contextualizada, plural, sin censura previa "
            "acerca de los hechos, acontecimientos y procesos de interés general."
        ),
        "hallazgo": (
            "El circuito de transparencia institucional del GADMCM requiere auditoría "
            "directa del portal LOTAIP. Los 21 numerales del Art. 19 de la Ley de "
            "Transparencia y Acceso a la Información Pública deben estar publicados, "
            "actualizados y ser comprensibles para el ciudadano. "
            "Datos pendientes de verificación directa en el portal institucional."
        ),
        "valor_principal":  None,
        "indicador_label": "Cumplimiento integral de publicación institucional",
        "unidad":           "% cumplimiento agregado (publicación × actualización × comprensibilidad)",
        "semaforo":         "PENDIENTE",
        "fuente":           "Portal LOTAIP GADMCM (montecristi.gob.ec) — verificación pendiente",
        "fecha_corte":      "pendiente",
        "estado_dato":      "pendiente_validacion",
        "narrativa": (
            "El Art. 18 de la Constitución establece el derecho fundamental a buscar "
            "y recibir información veraz y oportuna. El GADMCM tiene la obligación legal "
            "de publicar activamente los 21 numerales del Art. 19 de la Ley de Transparencia "
            "y Acceso a la Información Pública en su portal web. La capacidad efectiva de "
            "escrutinio ciudadano en Montecristi depende de que esa información esté "
            "disponible, actualizada y sea comprensible. El circuito está definido — "
            "los datos requieren verificación directa del portal institucional. "
            "Fuente: Portal LOTAIP GADMCM · verificación pendiente."
        ),
        # Indicadores complementarios
        "numerales_publicados": None,
        "numerales_total":      21,
        "tasa_respuesta_saip":  None,
        "umbral_verde":         80.0,
        "fuente_neo4j":         False,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# DRIVER FACTORY
# ══════════════════════════════════════════════════════════════════════════════

def _build_driver():
    """
    Intenta construir un driver Neo4j.
    Prioridad de credenciales:
      1. st.secrets["neo4j"] — secrets.toml (desarrollo) / Streamlit Cloud
      2. Variables de entorno NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD
      3. Defaults locales (bolt://localhost:7687 · user=neo4j)

    Retorna None si neo4j no está instalado o la conexión falla.
    """
    try:
        from neo4j import GraphDatabase  # optional dependency
    except ImportError:
        logger.debug("Paquete 'neo4j' no instalado — modo fallback.")
        return None

    # Leer credenciales
    try:
        import streamlit as st
        neo4j_cfg = st.secrets.get("neo4j", {})
        uri      = neo4j_cfg.get("uri",      os.getenv("NEO4J_URI",      _DEFAULT_URI))
        user     = neo4j_cfg.get("user",     os.getenv("NEO4J_USER",     _DEFAULT_USER))
        password = neo4j_cfg.get("password", os.getenv("NEO4J_PASSWORD", ""))
    except Exception:
        uri      = os.getenv("NEO4J_URI",      _DEFAULT_URI)
        user     = os.getenv("NEO4J_USER",     _DEFAULT_USER)
        password = os.getenv("NEO4J_PASSWORD", "")

    if not password:
        logger.debug("Neo4j: sin contraseña configurada — modo fallback.")
        return None

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        logger.info(f"Neo4j conectado: {uri}")
        return driver
    except Exception as exc:
        logger.warning(f"Neo4j no disponible ({exc.__class__.__name__}) — modo fallback.")
        return None


# ══════════════════════════════════════════════════════════════════════════════
# CONSULTAS CYPHER POR CIRCUITO
# ══════════════════════════════════════════════════════════════════════════════

def _query_gap_10pct(session) -> dict[str, Any]:
    """
    GAP_10PCT → Dom12
    Consulta principal: Ti_Patronato (RES_G10P_04_MCR — confirmado)
    Consulta complementaria: asignación GAP (RES_G10P_01_MCR — pendiente_validacion)
    """
    # Resultado principal: ejecución Patronato
    r = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_G10P_04_MCR'})
        RETURN r.valor       AS valor,
               r.semaforo    AS semaforo,
               r.fuente_documental AS fuente,
               r.interpretacion    AS interpretacion,
               r.periodo     AS periodo,
               r.estado_dato AS estado_dato,
               r.serie_2023  AS s2023,
               r.serie_2024  AS s2024,
               r.serie_2025  AS s2025
    """).single()

    if not r:
        return _FALLBACK["GAP_10PCT"]

    # Resultado complementario: asignación
    a = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_G10P_01_MCR'})
        RETURN r.valor AS asignacion, r.semaforo AS semaforo_a
    """).single()

    # Norma base
    norma = session.run("""
        MATCH (ack:Atom {id: 'COOTAD_249'})
        RETURN ack.obligacion AS texto, ack.sigla AS sigla, ack.articulo AS art
    """).single()

    base = dict(_FALLBACK["GAP_10PCT"])  # copia con todos los defaults
    base.update({
        "valor_principal":     r["valor"] or 50.0,
        "semaforo":            r["semaforo"] or "ROJO",
        "fuente":              _strip_internal(r["fuente"]),
        "fecha_corte":         r["periodo"] or "noviembre 2025",
        "estado_dato":         r["estado_dato"] or "confirmado",
        "asignacion_pct":      (a["asignacion"] if a else 20.84),
        "asignacion_semaforo": (a["semaforo_a"] if a else "VERDE"),
        "fuente_neo4j":        True,
    })
    if norma:
        base["norma_texto"] = norma["texto"]
    # Mantener narrativa del fallback (ya está en lenguaje gobernanza)
    return base


def _query_agua_potable(session) -> dict[str, Any]:
    """
    AGUA_POTABLE → Dom10
    Consultas: cobertura 34.9 % (RES_AGPT_01_MCR) + continuidad 0 % (RES_AGPT_02_MCR)
    """
    r = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_AGPT_01_MCR'})
        RETURN r.valor AS valor, r.semaforo AS semaforo,
               r.fuente_documental AS fuente,
               r.meta_pdot_2027   AS meta_pdot,
               r.periodo          AS periodo,
               r.estado_dato      AS estado_dato
    """).single()

    if not r:
        return _FALLBACK["AGUA_POTABLE"]

    cont = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_AGPT_02_MCR'})
        RETURN r.valor AS continuidad, r.semaforo AS sem_cont
    """).single()

    base = dict(_FALLBACK["AGUA_POTABLE"])
    base.update({
        "valor_principal":     r["valor"] or 34.9,
        "semaforo":            r["semaforo"] or "ROJO",
        "fuente":              _strip_internal(r["fuente"]) or "INEC Censo 2022",
        "fecha_corte":         r["periodo"] or "2022",
        "estado_dato":         r["estado_dato"] or "confirmado",
        "meta_pdot_2027":      r["meta_pdot"] or 42.38,
        "continuidad_pct":     (cont["continuidad"] if cont else 0.0),
        "continuidad_semaforo":(cont["sem_cont"]    if cont else "ROJO"),
        "fuente_neo4j":        True,
    })
    return base


def _query_transparencia(session) -> dict[str, Any]:
    """
    TRANSPARENCIA → Dom07
    Consulta principal: cumplimiento integral publicación (RES_TRANS_01_MCR)
    Consulta complementaria: cobertura numerales LOTAIP (RES_TRANS_02_MCR)
    """
    r = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_TRANS_01_MCR'})
        RETURN r.valor       AS valor,
               r.semaforo    AS semaforo,
               r.fuente_documental AS fuente,
               r.periodo     AS periodo,
               r.estado_dato AS estado_dato
    """).single()

    if not r:
        return _FALLBACK["TRANSPARENCIA"]

    cob = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_TRANS_02_MCR'})
        RETURN r.valor AS numerales, r.semaforo AS sem_cob
    """).single()

    sai = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_TRANS_04_MCR'})
        RETURN r.valor AS tasa_saip, r.semaforo AS sem_saip
    """).single()

    base = dict(_FALLBACK["TRANSPARENCIA"])
    base.update({
        "valor_principal":     r["valor"],
        "semaforo":            r["semaforo"] or "PENDIENTE",
        "fuente":              _strip_internal(r["fuente"]) or "Portal LOTAIP GADMCM",
        "fecha_corte":         r["periodo"] or "pendiente",
        "estado_dato":         r["estado_dato"] or "pendiente_validacion",
        "numerales_publicados": (cob["numerales"] if cob else None),
        "tasa_respuesta_saip":  (sai["tasa_saip"] if sai else None),
        "fuente_neo4j":         True,
    })
    return base


def _query_equidad(session) -> dict[str, Any]:
    """
    EQUIDAD → Dom06
    Consultas: IRS cantonal (RES_EQUD_01_MCR) + Brecha NBI (RES_EQUD_04_MCR)
    """
    irs = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_EQUD_01_MCR'})
        RETURN r.valor AS valor, r.semaforo AS semaforo,
               r.fuente_documental AS fuente,
               r.periodo AS periodo, r.estado_dato AS estado_dato
    """).single()

    if not irs:
        return _FALLBACK["EQUIDAD"]

    nbi = session.run("""
        MATCH (r:C9ResultadoTerritorial {id: 'RES_EQUD_04_MCR'})
        RETURN r.valor     AS brecha,
               r.nbi_urbano AS nbi_u,
               r.nbi_rural  AS nbi_r,
               r.semaforo   AS sem_nbi,
               r.pobreza_multidim_urbana AS pm_u,
               r.pobreza_multidim_rural  AS pm_r
    """).single()

    base = dict(_FALLBACK["EQUIDAD"])
    base.update({
        "valor_principal": irs["valor"] or 79.7,
        "semaforo":        irs["semaforo"] or "AMARILLO",
        "fuente":          _strip_internal(irs["fuente"]) or "INEC Censo 2022 · SNP",
        "fecha_corte":     irs["periodo"] or "2022",
        "estado_dato":     irs["estado_dato"] or "confirmado",
        "fuente_neo4j":    True,
    })
    if nbi:
        base.update({
            "brecha_nbi_pp":        nbi["brecha"]  or 32.0,
            "nbi_urbano":           nbi["nbi_u"]   or 21.3,
            "nbi_rural":            nbi["nbi_r"]   or 53.3,
            "brecha_semaforo":      nbi["sem_nbi"] or "ROJO",
            "pobreza_multi_urbana": nbi["pm_u"]    or 23.0,
            "pobreza_multi_rural":  nbi["pm_r"]    or 67.9,
        })
    return base


# ══════════════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ══════════════════════════════════════════════════════════════════════════════

# Intentar driver una sola vez por proceso (no por request)
_driver_cache: list = [None, False]   # [driver_obj, attempted]


def _get_driver():
    if not _driver_cache[1]:
        _driver_cache[0] = _build_driver()
        _driver_cache[1] = True
    return _driver_cache[0]


def _strip_internal(text: str | None) -> str:
    """
    Bloomberg Model: elimina referencias internas que pudieran filtrarse
    desde los campos de Neo4j hacia texto público.
    """
    if not text:
        return ""
    # Remover etiquetas internas que podrían estar en el campo fuente_documental
    _remove = [
        "Gold Master", "H07b", "H73", "SIAP-ICPI", "_TGI", "v5.5",
        "Ti_INVERSIÓN", "Ti_Patronato", "H41_IOC", "H41",
    ]
    for term in _remove:
        text = text.replace(term, "")
    return text.strip(" ·—-").strip()


def get_qtmp_chain(circuit_id: str) -> dict[str, Any] | None:
    """
    Retorna la cadena causal QTMP para un circuito dado.

    Parámetros:
        circuit_id: "GAP_10PCT" | "AGUA_POTABLE" | "EQUIDAD" | "TRANSPARENCIA"

    Retorna un dict con:
        circuit_id, dominio_id     — INTERNOS, no exponer en UI
        norma_texto                — lenguaje gobernanza público
        hallazgo                   — resumen del hallazgo
        valor_principal, unidad    — KPI principal
        semaforo                   — "VERDE" | "AMARILLO" | "ROJO" | "PENDIENTE"
        fuente                     — fuente pública (SIGEF, INEC, PDOT)
        fecha_corte                — periodo del dato
        estado_dato                — "confirmado" | "pendiente_validacion"
        narrativa                  — texto completo en lenguaje gobernanza
        fuente_neo4j               — True si viene del grafo, False si es fallback
        ...campos adicionales por circuito...

    Retorna None si circuit_id no es válido.

    Bloomberg Model: solo exponer 'narrativa', 'fuente', 'valor_principal',
    'indicador_label', 'semaforo', 'fecha_corte' en la UI.
    NUNCA exponer: circuit_id, dominio_id, norma_sigla, norma_articulo, fuente_neo4j.
    """
    if circuit_id not in CIRCUIT_DOMAIN_MAP:
        logger.error(f"circuit_id inválido: '{circuit_id}'. Válidos: {CIRCUITS}")
        return None

    _QUERY_MAP = {
        "GAP_10PCT":     _query_gap_10pct,
        "AGUA_POTABLE":  _query_agua_potable,
        "EQUIDAD":       _query_equidad,
        "TRANSPARENCIA": _query_transparencia,
    }

    driver = _get_driver()

    if driver:
        try:
            with driver.session() as session:
                data = _QUERY_MAP[circuit_id](session)
                logger.debug(f"get_qtmp_chain({circuit_id}): desde Neo4j")
                return data
        except Exception as exc:
            logger.warning(
                f"Error consultando Neo4j para {circuit_id} "
                f"({exc.__class__.__name__}) — usando fallback."
            )

    # Fallback: datos confirmados del Gold Master
    logger.debug(f"get_qtmp_chain({circuit_id}): fallback embebido")
    return dict(_FALLBACK[circuit_id])


def get_all_chains() -> dict[str, dict[str, Any]]:
    """
    Retorna las cadenas causales de los 3 circuitos QTMP.
    Útil para el Centro de Mando (Layer 1) si necesita datos de semáforo.

    Returns: {"GAP_10PCT": {...}, "AGUA_POTABLE": {...}, "EQUIDAD": {...}}
    """
    return {cid: get_qtmp_chain(cid) for cid in CIRCUITS}


def is_neo4j_available() -> bool:
    """
    Verifica si Neo4j está disponible en esta sesión.
    Útil para mostrar un badge "Datos en vivo" vs "Datos consolidados".
    """
    return _get_driver() is not None


def reset_driver_cache() -> None:
    """
    Fuerza reconexión al próximo get_qtmp_chain().
    Útil en desarrollo / después de reiniciar Neo4j Desktop.
    """
    _driver_cache[0] = None
    _driver_cache[1] = False
    logger.info("Cache del driver Neo4j reseteado.")
