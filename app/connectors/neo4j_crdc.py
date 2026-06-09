"""
app/connectors/neo4j_crdc.py — Conector C-RDC · QUIRA OS
=========================================================
ADR-026 §C-RDC · Dylus Lab © 2026

Responsabilidad única:
    Retornar el estado actual del Circuito C-RDC para un GAD.
    Responde: "¿Está listo el municipio para presentar RDC ante el CPCCS?"

TOPOLOGÍA C-RDC (convergente — ≠ C01 que es causal):
    Dom07 (ITAM)  ──┐
    Dom08 (IGP)   ──┤
    Dom02 (ISP)   ──┼──► Dom09 (Checklist RDC) ──► CPCCS (V=0/V≥70)
    Dom04 (PDOT)  ──┤
    Dom10 (agua)  ──┤
    Dom19 (PSG)   ──┘

    C01: si Dom07 falla → colapsa Dom07→Dom09 (PROPAGACIÓN)
    C-RDC: si Dom07 falla → pct_ok baja pero el circuito sigue (ACUMULACIÓN)

CADENA CAUSAL CRUZADA CON D02 (el diferenciador QUIRA):
    PSG (C-RDC falla) → ONU Mujeres bloqueado ($300K)
    ISP (C-RDC falla) → BDE bloqueado ($5M)
    Esta cadena convierte una métrica de RDC en inteligencia financiera.

BLOOMBERG FIREWALL:
    Campos internos (circuit_id, nodo IDs, dominio IDs): NUNCA en UI.
    Campos públicos: nombre, estado, pct_ok, narrativa, brecha_pp, impacto_usd.

FALLBACK:
    Datos embebidos MCR-001 · 2026-06-09 · Gold Master v5.5
    Mismo patrón que neo4j_qtmp.py: Neo4j → fallback si no disponible.

ACTUALIZAR FALLBACK:
    Cuando lleguen datos D04 (Planificación) o cambie el Gold Master,
    actualizar _FALLBACK_CRDC y re-ejecutar 001_crdc_circuit.cypher.
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

GAD_MCR = "MCR-001"


# ══════════════════════════════════════════════════════════════════════════════
# FALLBACK — MCR-001 · 2026-06-09 · Gold Master v5.5 + QUIRA indicadores
# ══════════════════════════════════════════════════════════════════════════════
# Actualizar cuando cambien indicadores o lleguen datos D04.
# NO hardcodear sin snapshot — ver CLAUDE.md Regla 3.

_NODOS_FALLBACK: list[dict] = [
    {
        "nodo_id":      "DOM07_TRANS",       # INTERNO
        "dominio":      "Dom07",             # INTERNO
        "nombre":       "Transparencia y LOTAIP",
        "indicador":    "ITAM",
        "valor_actual": 56.0,
        "umbral":       80.0,
        "operador":     "gte",
        "pasa":         False,
        "brecha_pp":    -24.0,
        "es_critico":   True,
        "semaforo":     "ROJO",
        "fuente":       "QUIRA ITAM — Portal DPE · auditoría junio 2026",
        "narrativa":    (
            "La transparencia institucional está en 56.0 % — 24 puntos bajo el "
            "umbral de la Rendición de Cuentas (80 %). El atraso sistémico en "
            "publicación LOTAIP (0 de 16 meses en plazo legal) es la causa principal."
        ),
    },
    {
        "nodo_id":      "DOM08_PART",
        "dominio":      "Dom08",
        "nombre":       "Participación Ciudadana y Asambleas",
        "indicador":    "IGP",
        "valor_actual": 27.98,
        "umbral":       25.0,
        "operador":     "gte",
        "pasa":         True,
        "brecha_pp":    2.98,
        "es_critico":   True,
        "semaforo":     "VERDE",
        "fuente":       "QUIRA IGP — Gold Master v5.5",
        "narrativa":    (
            "La gestión participativa está en 27.98 % — 2.98 puntos sobre el umbral "
            "mínimo (25 %). El municipio cumple este requisito para la RDC."
        ),
    },
    {
        "nodo_id":      "DOM0203_FISCAL",
        "dominio":      "Dom02/Dom03",
        "nombre":       "Salud Presupuestaria",
        "indicador":    "ISP",
        "valor_actual": 14.58,
        "umbral":       25.0,
        "operador":     "gte",
        "pasa":         False,
        "brecha_pp":    -10.42,
        "es_critico":   True,
        "semaforo":     "ROJO",
        "fuente":       "QUIRA ISP — Gold Master v5.5 · SIGEF",
        "narrativa":    (
            "La salud presupuestaria es 14.58 % — 10.42 puntos bajo el umbral "
            "requerido (25 %). Impacto directo: bloquea acceso a crédito BDE "
            "($5M) y debilita el expediente de RDC ante el CPCCS."
        ),
    },
    {
        "nodo_id":      "DOM04_PDOT",
        "dominio":      "Dom04",
        "nombre":       "Planificación PDOT y Metas",
        "indicador":    "META_PDOT_ASOCIADA",
        "valor_actual": None,
        "umbral":       4.0,
        "operador":     "gte",
        "pasa":         False,
        "brecha_pp":    None,
        "es_critico":   False,
        "semaforo":     "PENDIENTE",
        "fuente":       "D04 pendiente — solicitar avance PDOT a Dirección de Planificación",
        "narrativa":    (
            "Datos de avance PDOT pendientes. Solicitar a la Dirección de Planificación "
            "el informe de avance de las 4 metas SAT-0 regularizadas."
        ),
    },
    {
        "nodo_id":      "DOM10_TERR",
        "dominio":      "Dom10",
        "nombre":       "Cobertura de Servicios Territoriales",
        "indicador":    "EVIDENCIA_EJECUCION",
        "valor_actual": 1.0,     # 1 = informe existe
        "umbral":       None,
        "operador":     "eq_true",
        "pasa":         True,
        "brecha_pp":    None,
        "es_critico":   False,
        "semaforo":     "VERDE",
        "fuente":       "INEC Censo 2022 · PDOT Bicentenario 2023",
        "narrativa":    (
            "Informe de cobertura de agua y servicios disponible y actualizado. "
            "Cobertura red pública: 34.9 % de viviendas (INEC 2022). "
            "El informe cumple el requisito documental de la RDC."
        ),
    },
    {
        "nodo_id":      "DOM19_PSG",
        "dominio":      "Dom19",
        "nombre":       "Presupuesto Sensible al Género",
        "indicador":    "PSG",
        "valor_actual": 12.83,
        "umbral":       20.0,
        "operador":     "gte",
        "pasa":         False,
        "brecha_pp":    -7.17,
        "es_critico":   True,
        "semaforo":     "ROJO",
        "fuente":       "QUIRA PSG — Gold Master v5.5 · cédula presupuestaria",
        "narrativa":    (
            "El presupuesto sensible al género es 12.83 % — 7.17 puntos bajo "
            "el umbral (20 %). Impacto cruzado: bloquea acceso al Fondo Mujeres "
            "Rurales ONU Mujeres ($300K) además de debilitar la RDC."
        ),
    },
]

def _calcular_estado(nodos: list[dict]) -> dict:
    """Calcula el estado del circuito a partir de los resultados de nodos."""
    n_total   = len(nodos)
    n_ok      = sum(1 for n in nodos if n["pasa"])
    n_falla   = sum(1 for n in nodos if not n["pasa"] and n["valor_actual"] is not None)
    n_pend    = sum(1 for n in nodos if n["valor_actual"] is None)
    criticos_fallan = any(n for n in nodos if not n["pasa"] and n["es_critico"])

    pct_ok = (n_ok / n_total * 100) if n_total else 0.0

    if pct_ok >= 100 and not criticos_fallan:
        estado = "PREPARADO"
    elif criticos_fallan:
        estado = "BLOQUEADO"
    else:
        estado = "CON_BRECHAS"

    return {
        "nodos_total":    n_total,
        "nodos_ok":       n_ok,
        "nodos_fallidos": n_falla,
        "nodos_pendientes": n_pend,
        "pct_ok":         round(pct_ok, 1),
        "estado":         estado,
        "criticos_fallan": criticos_fallan,
    }


_FALLBACK_CRDC: dict[str, Any] = {
    "circuit_id":   "C-RDC",              # INTERNO
    "gad_id":       GAD_MCR,              # INTERNO
    "circuito":     "C-RDC",             # INTERNO
    "nombre":       "Convergencia Anual — Rendición de Cuentas",
    "escala":       "Anual (Mayo–Septiembre)",
    "arbitro":      "CPCCS",
    "activacion":   "Mayo (preparación) → Agosto (ejecución) → Septiembre (calificación)",
    "nodos":        _NODOS_FALLBACK,
    **_calcular_estado(_NODOS_FALLBACK),
    "impacto_d02_usd": 5_300_000,
    # ISP falla → BDE $5M · PSG falla → ONU Mujeres $300K
    "impacto_descripcion": (
        "ISP bajo (14.58% < 25%) bloquea BDE Agua Potable $5M. "
        "PSG bajo (12.83% < 20%) bloquea ONU Mujeres Mujeres Rurales $300K. "
        "Cerrar estas brechas desbloquea $5.3M en financiamiento."
    ),
    "narrativa": (
        "El Circuito de Rendición de Cuentas evalúa 6 dominios que deben converger "
        "para que el municipio pueda presentar su RDC ante el CPCCS. "
        "Al 9 de junio de 2026: 2 de 6 nodos pasan (33.3 %). "
        "Los 3 nodos críticos que fallan son: "
        "ITAM (transparencia 56 % vs 80 % requerido), "
        "ISP (salud presupuestaria 14.58 % vs 25 % requerido), "
        "PSG (género 12.83 % vs 20 % requerido). "
        "Estos mismos fallos bloquean $5.3M en cooperación internacional (D02). "
        "Fuente: QUIRA · Gold Master v5.5 · Portal DPE · INEC Censo 2022."
    ),
    "fecha_corte": "2026-06-09",
    "estado_dato": "confirmado",
    "fuente_neo4j": False,
}


# ══════════════════════════════════════════════════════════════════════════════
# DRIVER (reutiliza el de neo4j_qtmp)
# ══════════════════════════════════════════════════════════════════════════════

def _get_driver():
    """Reutiliza el driver cache de neo4j_qtmp para no abrir dos conexiones."""
    try:
        from app.connectors.neo4j_qtmp import _get_driver as _qtmp_driver
        return _qtmp_driver()
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# CONSULTAS CYPHER
# ══════════════════════════════════════════════════════════════════════════════

def _query_crdc_from_neo4j(session, gad_id: str) -> dict | None:
    """
    Lee el estado C-RDC desde AuraDB.
    Consulta EvaluacionCircuito + C9ResultadoTerritorial por nodo.
    Retorna None si no existen datos para este gad_id.
    """
    eval_id = f"EVAL_CRDC_{gad_id.replace('-', '_')}_2026"

    # Evaluación general
    ev = session.run("""
        MATCH (ev:EvaluacionCircuito {id: $eval_id})
        RETURN ev.pct_ok        AS pct_ok,
               ev.estado        AS estado,
               ev.nodos_ok      AS nodos_ok,
               ev.nodos_total   AS nodos_total,
               ev.nodos_pendientes AS nodos_pendientes,
               ev.impacto_d02_usd  AS impacto_usd,
               ev.estado_desc      AS estado_desc,
               ev.updated_at       AS updated_at
    """, eval_id=eval_id).single()

    if not ev:
        return None

    # Resultados por nodo
    nodo_ids = [
        "RES_CRDC_DOM07_MCR", "RES_CRDC_DOM08_MCR", "RES_CRDC_DOM0203_MCR",
        "RES_CRDC_DOM04_MCR", "RES_CRDC_DOM10_MCR", "RES_CRDC_DOM19_MCR",
    ]
    nodos = []
    for nid in nodo_ids:
        r = session.run("""
            MATCH (r:C9ResultadoTerritorial {id: $nid})
            RETURN r.valor AS valor, r.semaforo AS semaforo, r.pasa AS pasa,
                   r.brecha_pp AS brecha_pp, r.indicador AS indicador,
                   r.dominio AS dominio, r.fuente_documental AS fuente,
                   r.periodo AS periodo, r.estado_dato AS estado_dato
        """, nid=nid).single()
        if r:
            # Enriquecer con datos estructurales del fallback
            fallback_nodo = next(
                (n for n in _NODOS_FALLBACK if n["indicador"] == r["indicador"]),
                {}
            )
            nodos.append({
                **fallback_nodo,
                "valor_actual": r["valor"],
                "semaforo":     r["semaforo"] or "PENDIENTE",
                "pasa":         bool(r["pasa"]),
                "brecha_pp":    r["brecha_pp"],
                "fuente":       _strip_internal(r["fuente"]),
                "fecha_corte":  r["periodo"] or "2026",
                "estado_dato":  r["estado_dato"] or "confirmado",
                "fuente_neo4j": True,
            })

    if not nodos:
        return None

    calc = _calcular_estado(nodos)
    return {
        **dict(_FALLBACK_CRDC),
        "nodos":         nodos,
        **calc,
        "impacto_d02_usd": ev["impacto_usd"] or _FALLBACK_CRDC["impacto_d02_usd"],
        "fecha_corte":   str(ev["updated_at"])[:10] if ev["updated_at"] else "2026-06-09",
        "fuente_neo4j":  True,
    }


def _strip_internal(text: str | None) -> str:
    """Elimina referencias internas — Bloomberg Model."""
    if not text:
        return ""
    for term in ["Gold Master", "H07b", "H73", "SIAP-ICPI", "_TGI", "v5.5"]:
        text = text.replace(term, "")
    return text.strip(" ·—-").strip()


# ══════════════════════════════════════════════════════════════════════════════
# API PÚBLICA
# ══════════════════════════════════════════════════════════════════════════════

def get_crdc_state(gad_id: str = GAD_MCR) -> dict[str, Any]:
    """
    Retorna el estado completo del Circuito C-RDC para un GAD.

    Output (lenguaje de gobernanza — Bloomberg-safe):
        circuito:         'C-RDC'
        nombre:           'Convergencia Anual — Rendición de Cuentas'
        estado:           'PREPARADO' | 'CON_BRECHAS' | 'BLOQUEADO'
        pct_ok:           float (0.0–100.0)
        nodos_ok:         int
        nodos_fallidos:   int
        nodos_total:      int
        nodos:            list[dict] — detalles por nodo (ver abajo)
        impacto_d02_usd:  float — USD bloqueados en D02 por culpa de gaps C-RDC
        narrativa:        str — texto completo gobernanza
        fecha_corte:      str
        fuente_neo4j:     bool

    Cada nodo incluye:
        nombre, indicador, valor_actual, umbral, pasa, brecha_pp,
        semaforo, es_critico, fuente, narrativa.
        (nodo_id y dominio son INTERNOS — no exponer en UI)

    Bloomberg: usar solo nombre/estado/pct_ok/narrativa/impacto_d02_usd en UI.
    NUNCA exponer: circuit_id, nodo_id, dominio, fuente_neo4j.
    """
    driver = _get_driver()

    if driver:
        try:
            with driver.session() as session:
                data = _query_crdc_from_neo4j(session, gad_id)
                if data:
                    logger.debug(f"get_crdc_state({gad_id}): desde Neo4j")
                    return data
                logger.debug(f"get_crdc_state({gad_id}): Neo4j sin datos → fallback")
        except Exception as exc:
            logger.warning(
                f"Error consultando C-RDC en Neo4j ({exc.__class__.__name__}) "
                f"— usando fallback."
            )

    logger.debug(f"get_crdc_state({gad_id}): fallback embebido")
    return dict(_FALLBACK_CRDC)


def get_crdc_nodo(nodo_indicador: str, gad_id: str = GAD_MCR) -> dict | None:
    """
    Retorna el estado de un nodo específico del C-RDC por su indicador.

    Args:
        nodo_indicador: 'ITAM' | 'IGP' | 'ISP' | 'META_PDOT_ASOCIADA'
                        | 'EVIDENCIA_EJECUCION' | 'PSG'

    Útil para el Simulador: "si ITAM sube a 80%, ¿el circuito se desbloquea?"
    """
    state = get_crdc_state(gad_id)
    for nodo in state.get("nodos", []):
        if nodo["indicador"] == nodo_indicador:
            return nodo
    return None


def simulate_crdc_mejora(
    indicador: str,
    nuevo_valor: float,
    gad_id: str = GAD_MCR,
) -> dict:
    """
    Simula cómo cambia el estado del C-RDC si un indicador mejora.

    Útil para: "Si PSG sube a 20%, ¿el circuito mejora?"
    Conecta con D02 Simulator para impacto financiero cruzado.

    Returns:
        dict con:
            estado_actual:   estado del circuito hoy
            estado_simulado: estado del circuito con nuevo valor
            pct_ok_actual:   porcentaje actual
            pct_ok_simulado: porcentaje simulado
            mejora:          True si el estado mejoró
            nodo_cambia:     True si el nodo específico cambia de estado
            narrativa_sim:   texto explicativo
    """
    state = get_crdc_state(gad_id)
    nodos_actuales = state.get("nodos", list(_NODOS_FALLBACK))

    # Simular cambio en el nodo específico
    nodos_simulados = []
    nodo_encontrado = False
    for nodo in nodos_actuales:
        if nodo["indicador"] == indicador:
            nodo_encontrado = True
            nodo_sim = dict(nodo)
            nodo_sim["valor_actual"] = nuevo_valor
            # Evaluar si pasa con el nuevo valor
            umbral = nodo.get("umbral")
            if umbral is not None:
                nodo_sim["pasa"]     = nuevo_valor >= umbral
                nodo_sim["brecha_pp"]= round(nuevo_valor - umbral, 2)
                nodo_sim["semaforo"] = "VERDE" if nodo_sim["pasa"] else "ROJO"
            nodos_simulados.append(nodo_sim)
        else:
            nodos_simulados.append(dict(nodo))

    if not nodo_encontrado:
        return {
            "error": f"Indicador '{indicador}' no encontrado en C-RDC",
            "indicadores_validos": [n["indicador"] for n in nodos_actuales],
        }

    calc_actual  = _calcular_estado(nodos_actuales)
    calc_sim     = _calcular_estado(nodos_simulados)
    mejora       = calc_sim["pct_ok"] > calc_actual["pct_ok"]
    estado_mejora= calc_sim["estado"] != calc_actual["estado"]

    nodo_antes  = next(n for n in nodos_actuales  if n["indicador"] == indicador)
    nodo_despues= next(n for n in nodos_simulados if n["indicador"] == indicador)

    return {
        "gad_id":          gad_id,
        "indicador":       indicador,
        "valor_actual":    nodo_antes["valor_actual"],
        "nuevo_valor":     nuevo_valor,
        "nodo_cambia":     nodo_antes["pasa"] != nodo_despues["pasa"],
        "estado_actual":   calc_actual["estado"],
        "estado_simulado": calc_sim["estado"],
        "pct_ok_actual":   calc_actual["pct_ok"],
        "pct_ok_simulado": calc_sim["pct_ok"],
        "mejora":          mejora,
        "mejora_estado":   estado_mejora,
        "narrativa_sim": (
            f"Si {nodo_antes['nombre']} sube de "
            f"{nodo_antes['valor_actual'] or '?'}% a {nuevo_valor}%: "
            f"el nodo {'pasa' if nodo_despues['pasa'] else 'sigue fallando'}. "
            f"C-RDC pasa de {calc_actual['pct_ok']}% a {calc_sim['pct_ok']}% "
            f"({calc_actual['estado']} -> {calc_sim['estado']})."
        ),
    }


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

    state = get_crdc_state()

    sep = "=" * 60
    print(f"\n{sep}")
    print(f"C-RDC — {state['nombre']}")
    print(f"GAD: {state.get('gad_id', GAD_MCR)}  |  "
          f"Estado: {state['estado']}  |  "
          f"Nodos OK: {state['nodos_ok']}/{state['nodos_total']} "
          f"({state['pct_ok']}%)")
    print(f"Impacto D02: ${state.get('impacto_d02_usd', 0):,.0f} bloqueados")
    print(f"Fuente Neo4j: {state.get('fuente_neo4j', False)}")
    print(sep)

    for nodo in state.get("nodos", []):
        icono = "OK" if nodo["pasa"] else ("??" if nodo["valor_actual"] is None else "NO")
        val   = f"{nodo['valor_actual']:.1f}%" if nodo["valor_actual"] is not None else "PENDIENTE"
        umb   = f"/{nodo['umbral']:.0f}%" if nodo["umbral"] else ""
        brecha= f" (brecha {nodo['brecha_pp']:+.1f}pp)" if nodo.get("brecha_pp") else ""
        crit  = " [CRITICO]" if nodo["es_critico"] and not nodo["pasa"] else ""
        print(f"  [{icono}] {nodo['nombre']:40s} {val}{umb}{brecha}{crit}")

    print(f"\n{sep}")

    # Test simulación
    if "--sim" in sys.argv:
        print("\nSIMULACION: PSG -> 20.0%")
        sim = simulate_crdc_mejora("PSG", 20.0)
        print(f"  {sim['narrativa_sim']}")
        print(f"  Impacto D02: nodo_cambia={sim['nodo_cambia']} "
              f"mejora_estado={sim['mejora_estado']}")
