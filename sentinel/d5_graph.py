"""
sentinel/d5_graph.py
RC-D5 — Grafo de Propagacion de Tensiones Institucionales
Dylus Lab © 2026-05-20

FUNCION:
  Base de conocimiento estatica de los caminos de propagacion institucional.
  Define como las tensiones detectadas en D3/D4/D3xD4/D1/D1.3 se amplifican
  y transmiten entre dimensiones del sistema de gobernanza.

  El grafo NO es un modelo causal determinista.
  Es un grafo probabilistico de propagacion epistemologica:
    - Cada arista tiene un peso de amplificacion [0,1]
    - Solo se activa si la dimension fuente tiene confianza suficiente
    - La direccion refleja dependencias institucionales observadas

DOCTRINA:
  Una tension aislada puede ser una anomalia.
  Una tension que se propaga a otra dimension es una senal sistemica.
  Una cascada de 3+ dimensiones es evidencia de disfuncion estructural.

CONVENCION DE PESOS:
  0.85-1.00 — propagacion casi directa (evidencia muy fuerte)
  0.65-0.84 — propagacion fuerte (evidencia solida)
  0.45-0.64 — propagacion moderada (hipotesis plausible)
  0.25-0.44 — propagacion debil (senal emergente, observacional)

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── ARISTA DE PROPAGACION ─────────────────────────────────────────────────────

@dataclass(frozen=True)
class PropagationEdge:
    """
    Arista del grafo de propagacion de tensiones.

    source_dim      — dimension de origen: "D3" | "D4" | "D3xD4" | "D1" | "D1.3"
    source_state    — estado/patron que activa la arista
    target_dim      — dimension de destino
    target_state    — estado/patron que se amplifica en destino
    weight          — peso de amplificacion [0.0, 1.0]
    rationale       — hipotesis institucional de la propagacion
    norm_context    — contexto normativo vault-verificado (vacio si no aplica)
    min_source_conf — confianza minima en la dimension origen para activar
    feedback        — True si esta arista completa un ciclo de retroalimentacion
    """
    source_dim:      str
    source_state:    str
    target_dim:      str
    target_state:    str
    weight:          float
    rationale:       str
    norm_context:    str   = ""
    min_source_conf: float = 0.30
    feedback:        bool  = False


# ── GRAFO DE PROPAGACION ──────────────────────────────────────────────────────
#
# Cada arista refleja una hipotesis institucional sobre como las tensiones
# se transmiten entre dimensiones del gobierno local.
# Los pesos fueron calibrados a partir de la doctrina QUIRA y el corpus
# documental del Holding Municipal de Montecristi.

PROPAGATION_EDGES: List[PropagationEdge] = [

    # ── D3 -> D4 ─────────────────────────────────────────────────────────────
    # La dinamica temporal del presupuesto determina la distribucion territorial.

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "PARALISIS_ESTRUCTURAL",
        target_dim      = "D4",
        target_state    = "CONCENTRACION_TERRITORIAL",
        weight          = 0.75,
        rationale       = (
            "La paralisis ejecutiva concentra la ejecucion residual en parroquias "
            "con mayor capacidad de contratacion previa. Las zonas perifericas "
            "acumulan rezago cuando el flujo presupuestario se detiene."
        ),
        norm_context     = "COOTAD Art. 272 — distribucion equitativa cantonal",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "INFRAEJECUCION_CRONICA",
        target_dim      = "D4",
        target_state    = "CONCENTRACION_TERRITORIAL",
        weight          = 0.80,
        rationale       = (
            "La infraejecucion cronica beneficia desproporcionadamente a parroquias "
            "con contratos preexistentes. El gasto residual fluye hacia donde "
            "la burocracia local ya tiene capacidad de absorcion."
        ),
        norm_context     = "COOTAD Art. 272 — criterios de distribucion cantonal",
        min_source_conf  = 0.40,
    ),

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "EXPANSION_ACELERADA",
        target_dim      = "D4",
        target_state    = "CONCENTRACION_TERRITORIAL",
        weight          = 0.60,
        rationale       = (
            "La expansion presupuestaria acelerada tiende a beneficiar zonas "
            "con mayor capacidad de absorcion. Sin mecanismos distributivos "
            "explicitos, la inversion adicional reproduce concentracion preexistente."
        ),
        norm_context     = "COOTAD Art. 272 — criterios de distribucion cantonal",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "VOLATILIDAD_PROCESAL",
        target_dim      = "D4",
        target_state    = "EQUILIBRIO_FRAGMENTADO",
        weight          = 0.45,
        rationale       = (
            "La volatilidad en ejecucion genera fragmentacion territorial: "
            "algunas parroquias reciben inversion irregular mientras otras "
            "muestran rezago persistente por falta de continuidad."
        ),
        min_source_conf  = 0.30,
    ),

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "CIERRE_TARDIO",
        target_dim      = "D4",
        target_state    = "CONCENTRACION_TERRITORIAL",
        weight          = 0.50,
        rationale       = (
            "El cierre tardio concentra la ejecucion en Q4 en zonas con "
            "contratos avanzados. Las parroquias perifericas con proyectos "
            "menos maduros quedan subejecutadas al final del ciclo."
        ),
        norm_context     = "COOTAD Art. 272",
        min_source_conf  = 0.35,
    ),

    # ── D3 -> D1.3 ───────────────────────────────────────────────────────────
    # La dinamica temporal revela desacople respecto a compromisos PDOT.

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "PARALISIS_ESTRUCTURAL",
        target_dim      = "D1.3",
        target_state    = "DESVIACION_ESTRATEGICA",
        weight          = 0.55,
        rationale       = (
            "Cuando el patron temporal es paralisis, la ejecucion acumulada "
            "se aleja de las metas PDOT progresivamente. "
            "El desacople estrategico emerge de la inercia, no de decisiones explicitas."
        ),
        norm_context     = "PDOT 2023-2027 — compromisos de ejecucion territorial",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "INFRAEJECUCION_CRONICA",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.65,
        rationale       = (
            "La infraejecucion cronica genera contradiccion directa con metas PDOT: "
            "los compromisos de ejecucion territorial no pueden cumplirse si "
            "el presupuesto sistematicamente no se ejecuta."
        ),
        norm_context     = "PDOT 2023-2027 — metas de ejecucion territorial",
        min_source_conf  = 0.40,
    ),

    PropagationEdge(
        source_dim      = "D3",
        source_state    = "EXPANSION_ACELERADA",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.50,
        rationale       = (
            "La expansion sin correccion distributiva contradice la meta "
            "PDOT de IRS <= 45. El crecimiento del gasto amplifica la brecha "
            "territorial si no va acompanado de mecanismos de equidad expliciticos."
        ),
        norm_context     = "PDOT 2023-2027 — IRS meta <= 45",
        min_source_conf  = 0.40,
    ),

    # ── D4 -> D1.3 ───────────────────────────────────────────────────────────
    # La inequidad territorial contradice los compromisos estrategicos PDOT.

    PropagationEdge(
        source_dim      = "D4",
        source_state    = "CONCENTRACION_TERRITORIAL",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.82,
        rationale       = (
            "La concentracion territorial medida por IRS > meta PDOT "
            "constituye la evidencia directa de contradiccion con los compromisos "
            "estrategicos declarados en el PDOT 2023-2027."
        ),
        norm_context     = "PDOT 2023-2027 IRS<=45 + COOTAD Art. 272",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D4",
        source_state    = "PERIFERIA_EXCLUIDA",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.88,
        rationale       = (
            "La exclusion periferica sistematica contradice tanto el PDOT "
            "como la competencia municipal de agua potable (CRE Art. 264(4)) "
            "y la obligacion de distribucion equitativa (COOTAD Art. 272)."
        ),
        norm_context     = "CRE Art. 264(4) + COOTAD Art. 272",
        min_source_conf  = 0.40,
    ),

    PropagationEdge(
        source_dim      = "D4",
        source_state    = "INEQUIDAD_HIDRICA",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.90,
        rationale       = (
            "La inequidad hidrica rural sin correccion constituye la contradiccion "
            "mas directa con la competencia municipal exclusiva de agua potable "
            "establecida en CRE Art. 264(4). La planificacion PDOT no puede "
            "eludir esta responsabilidad constitucional."
        ),
        norm_context     = "CRE Art. 264(4) — competencia municipal exclusiva agua",
        min_source_conf  = 0.40,
    ),

    # ── D4 -> D1 ─────────────────────────────────────────────────────────────
    # La inequidad territorial puede indicar fallas procedimentales.

    PropagationEdge(
        source_dim      = "D4",
        source_state    = "CONCENTRACION_TERRITORIAL",
        target_dim      = "D1",
        target_state    = "RIESGO_DE_COMPETENCIA",
        weight          = 0.42,
        rationale       = (
            "La persistencia de concentracion territorial puede reflejar "
            "ausencia de mecanismos aprobatorios formales para distribucion "
            "de inversion. Sin ordenanza, la distribucion carece de respaldo competencial."
        ),
        norm_context     = "COOTAD Art. 238 + COOTAD Art. 267",
        min_source_conf  = 0.40,
    ),

    PropagationEdge(
        source_dim      = "D4",
        source_state    = "REZAGO_PERSISTENTE",
        target_dim      = "D1",
        target_state    = "RIESGO_DE_EVIDENCIA",
        weight          = 0.38,
        rationale       = (
            "El rezago territorial persistente sin documentacion de medidas correctivas "
            "genera riesgo de evidencia: no hay respaldo documental de que "
            "la entidad reconocio y respondio al desequilibrio."
        ),
        norm_context     = "COOTAD Art. 272 — obligacion de seguimiento",
        min_source_conf  = 0.35,
    ),

    # ── D3xD4 -> D1.3 ────────────────────────────────────────────────────────
    # El cruce dimensional produce la senal mas fuerte de contradiccion PDOT.

    PropagationEdge(
        source_dim      = "D3xD4",
        source_state    = "CRISIS_DOBLE",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.92,
        rationale       = (
            "La combinacion de subejecucion temporal y concentracion territorial "
            "constituye la senal de mayor probabilidad de contradiccion PDOT. "
            "Las dos dimensiones se refuerzan mutuamente para amplificar la brecha."
        ),
        norm_context     = "PDOT 2023-2027 + COOTAD Art. 272",
        min_source_conf  = 0.40,
    ),

    PropagationEdge(
        source_dim      = "D3xD4",
        source_state    = "EXCLUSION_PERIFERICA",
        target_dim      = "D1",
        target_state    = "RIESGO_DE_PROCEDIMIENTO",
        weight          = 0.58,
        rationale       = (
            "La exclusion periferica sostenida sugiere ausencia de mecanismos "
            "procedimentales para garantizar acceso territorial. "
            "Sin documentacion aprobatoria de distribucion, el procedimiento es opaco."
        ),
        norm_context     = "COOTAD Art. 238 + COPFP Art. 97",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D3xD4",
        source_state    = "EXCLUSION_PERIFERICA",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.85,
        rationale       = (
            "La exclusion periferica confirmada por ambas dimensiones "
            "es la contradiccion mas directa con los compromisos PDOT "
            "de equidad territorial y acceso a servicios basicos."
        ),
        norm_context     = "PDOT 2023-2027 + CRE Art. 264(4) + COOTAD Art. 272",
        min_source_conf  = 0.40,
    ),

    PropagationEdge(
        source_dim      = "D3xD4",
        source_state    = "EXPANSION_CONCENTRADA",
        target_dim      = "D1.3",
        target_state    = "DESVIACION_ESTRATEGICA",
        weight          = 0.70,
        rationale       = (
            "La expansion concentrada genera desacople estrategico: "
            "el gasto crece pero el territorio periferico no recibe el beneficio "
            "proporcional comprometido en el PDOT 2023-2027."
        ),
        norm_context     = "PDOT 2023-2027 — metas de equidad territorial",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D3xD4",
        source_state    = "VULNERABILIDAD_HIDRICA",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.88,
        rationale       = (
            "La vulnerabilidad hidrica cruzada (temporal y territorial) "
            "genera la contradiccion mas severa con CRE Art. 264(4): "
            "la competencia municipal exclusiva no se refleja en la distribucion "
            "presupuestaria ni en la cobertura territorial."
        ),
        norm_context     = "CRE Art. 264(4) + PDOT 2023-2027",
        min_source_conf  = 0.40,
    ),

    # ── D1 -> D1.3 ───────────────────────────────────────────────────────────
    # Las fallas procedimentales desconectan la ejecucion de los compromisos.

    PropagationEdge(
        source_dim      = "D1",
        source_state    = "RIESGO_DE_PROCEDIMIENTO",
        target_dim      = "D1.3",
        target_state    = "DESVIACION_ESTRATEGICA",
        weight          = 0.52,
        rationale       = (
            "Sin documentacion formal del proceso presupuestario, "
            "la verificacion de alineacion PDOT no es posible. "
            "La opacidad procedimental genera desacople estrategico por defecto."
        ),
        norm_context     = "COPFP Art. 97 — trazabilidad presupuestaria",
        min_source_conf  = 0.35,
    ),

    PropagationEdge(
        source_dim      = "D1",
        source_state    = "RIESGO_DE_COMPETENCIA",
        target_dim      = "D1.3",
        target_state    = "DESVIACION_ESTRATEGICA",
        weight          = 0.48,
        rationale       = (
            "La incertidumbre sobre que organo tiene competencia aprobatoria "
            "impide la correcta territorializacion del presupuesto, "
            "generando desacople progresivo respecto a las metas PDOT."
        ),
        norm_context     = "COOTAD Art. 267 — competencias EP municipales",
        min_source_conf  = 0.30,
    ),

    PropagationEdge(
        source_dim      = "D1",
        source_state    = "REQUIERE_REVIEW",
        target_dim      = "D1.3",
        target_state    = "CONTRADICCION_CRITICA",
        weight          = 0.62,
        rationale       = (
            "Cuando la coherencia juridica requiere revision institucional, "
            "la verificacion de alineacion PDOT es imposible. "
            "Este estado escala automaticamente a contradiccion estrategica critica."
        ),
        norm_context     = "COPFP Art. 97 + COOTAD Art. 238",
        min_source_conf  = 0.35,
    ),

    # ── D1.3 -> D4 (retroalimentacion) ───────────────────────────────────────
    # La contradiccion PDOT no resuelta refuerza la concentracion en el ciclo siguiente.

    PropagationEdge(
        source_dim      = "D1.3",
        source_state    = "CONTRADICCION_CRITICA",
        target_dim      = "D4",
        target_state    = "CONCENTRACION_TERRITORIAL",
        weight          = 0.35,
        rationale       = (
            "La contradiccion estrategica no resuelta implica que la asignacion "
            "presupuestaria del proximo ciclo replicara la distribucion inequitativa. "
            "Sin correccion del PDOT, la concentracion territorial se perpetua."
        ),
        norm_context     = "PDOT 2023-2027 — ciclo de planificacion 4 anos",
        min_source_conf  = 0.40,
        feedback         = True,
    ),

    PropagationEdge(
        source_dim      = "D1.3",
        source_state    = "DESVIACION_ESTRATEGICA",
        target_dim      = "D3",
        target_state    = "VOLATILIDAD_PROCESAL",
        weight          = 0.28,
        rationale       = (
            "La desviacion estrategica no corregida genera presion institucional "
            "para ajustar el presupuesto sin planificacion territorial, "
            "lo que introduce volatilidad en el patron temporal de ejecucion."
        ),
        norm_context     = "PDOT 2023-2027 — ciclo de seguimiento anual",
        min_source_conf  = 0.35,
        feedback         = True,
    ),

]


# ── INDICE POR DIMENSION ORIGEN ───────────────────────────────────────────────

def _build_index() -> Dict[str, List[PropagationEdge]]:
    idx: Dict[str, List[PropagationEdge]] = {}
    for edge in PROPAGATION_EDGES:
        idx.setdefault(edge.source_dim, []).append(edge)
    return idx


EDGES_BY_SOURCE: Dict[str, List[PropagationEdge]] = _build_index()


def get_edges_from(source_dim: str) -> List[PropagationEdge]:
    """Retorna todas las aristas que parten de una dimension dada."""
    return EDGES_BY_SOURCE.get(source_dim, [])


def get_edge(
    source_dim: str, source_state: str, target_dim: str
) -> Optional[PropagationEdge]:
    """Busca una arista especifica en el grafo (primera coincidencia)."""
    for edge in EDGES_BY_SOURCE.get(source_dim, []):
        if edge.source_state == source_state and edge.target_dim == target_dim:
            return edge
    return None


def get_all_source_dims() -> List[str]:
    """Retorna las dimensiones con aristas salientes."""
    return list(EDGES_BY_SOURCE.keys())


def count_edges() -> int:
    """Numero total de aristas en el grafo."""
    return len(PROPAGATION_EDGES)


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("RC-D5 Grafo de Propagacion — QUIRA OS")
    print("=" * 65)
    print(f"\n  Total aristas en el grafo: {count_edges()}")

    for src_dim in get_all_source_dims():
        edges = get_edges_from(src_dim)
        print(f"\n  {src_dim} ({len(edges)} aristas salientes):")
        for e in edges:
            fb = "[RETROALIM] " if e.feedback else ""
            print(f"    {fb}{e.source_state[:30]:<30} -> {e.target_dim}:{e.target_state}")
            print(f"      w={e.weight:.2f}  min_conf={e.min_source_conf:.2f}  "
                  f"norma={e.norm_context[:50]}")
