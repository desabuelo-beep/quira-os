"""
sentinel/provenance_graph.py
Structured Provenance Graph — QUIRA OS
Dylus Lab © 2026-05-20

Grafo DAG de procedencia inferencial para todas las capas RC.
Traza la cadena: Gold Master Excel → Python → Silos → Prompt → Respuesta

PROPOSITO:
  Cada inferencia en QUIRA debe poder responder:
    ¿De dónde vino este dato?
    ¿Qué motor lo transformó?
    ¿Qué contratos RC lo gobiernan?
    ¿Qué confianza tiene cada nodo?

NODOS:
  SOURCE      → Fuente primaria (Gold Master Excel, Vault, JSON silo)
  TRANSFORM   → Motor RC que procesó la fuente (analyze_series, analyze_territory, etc.)
  INFERENCE   → Resultado inferencial (CalibratedResult, D4Result, D3D4CrossResult)
  NORMATIVE   → Binding normativo (D4NormativeBinding, D3D4NormativeBinding)
  PROMPT      → Bloque de contexto inyectado al LLM

ARISTAS:
  derives_from → X deriva_de Y
  governed_by  → X gobernado_por contract RC

POLITICA:
  - Inmutable: los nodos se agregan, nunca se modifican
  - Confianza propagada: nodo heredda min(conf_padres)
  - Sesión: el grafo es por sesión (no persiste entre recargas)

Dylus Lab © 2026-05-20
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ── TIPOS DE NODO ──────────────────────────────────────────────────────────────

NODE_TYPES = {"SOURCE", "TRANSFORM", "INFERENCE", "NORMATIVE", "PROMPT"}
EDGE_TYPES = {"derives_from", "governed_by", "injects_into"}


# ── DATACLASSES ────────────────────────────────────────────────────────────────

@dataclass
class ProvenanceNode:
    """Un nodo en el grafo de procedencia."""
    node_id:    str           # hash determinístico del contenido
    node_type:  str           # SOURCE | TRANSFORM | INFERENCE | NORMATIVE | PROMPT
    label:      str           # nombre legible (ej: "RC-D4 analyze_territory")
    engine:     str           # motor RC responsable (ej: "RC-D4", "RC-D3D4")
    confidence: float         # confianza asociada al nodo (0.0–1.0)
    payload:    Dict[str, Any] = field(default_factory=dict)  # metadatos clave
    timestamp:  float          = field(default_factory=time.time)
    parents:    List[str]      = field(default_factory=list)   # node_ids padres


@dataclass
class ProvenanceEdge:
    """Una arista dirigida en el grafo de procedencia."""
    source_id:  str   # node_id origen
    target_id:  str   # node_id destino
    edge_type:  str   # derives_from | governed_by | injects_into
    weight:     float = 1.0


@dataclass
class ProvenanceGraph:
    """
    Grafo DAG de procedencia para una sesión QUIRA.
    Crece durante la sesión; nunca modifica nodos existentes.
    """
    session_id: str
    nodes:      Dict[str, ProvenanceNode] = field(default_factory=dict)
    edges:      List[ProvenanceEdge]      = field(default_factory=list)
    created_at: float                     = field(default_factory=time.time)


# ── INSTANCIA DE SESIÓN (singleton por proceso) ────────────────────────────────

_GRAPH: Optional[ProvenanceGraph] = None


def get_graph(session_id: str = "default") -> ProvenanceGraph:
    """Retorna el grafo de sesión actual, creándolo si no existe."""
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = ProvenanceGraph(session_id=session_id)
    return _GRAPH


def reset_graph(session_id: str = "default") -> ProvenanceGraph:
    """Reinicia el grafo de sesión (típicamente al inicio de sesión Streamlit)."""
    global _GRAPH
    _GRAPH = ProvenanceGraph(session_id=session_id)
    return _GRAPH


# ── CONSTRUCCIÓN DE NODOS ──────────────────────────────────────────────────────

def _make_node_id(label: str, engine: str, payload_key: str = "") -> str:
    """Hash determinístico para un nodo. Mismo nodo = mismo ID."""
    raw = f"{label}|{engine}|{payload_key}"
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def add_source_node(
    label: str,
    engine: str,
    source_file: str,
    record_count: int = 0,
    confidence: float = 1.0,
) -> str:
    """
    Registra una fuente primaria (Gold Master Excel, JSON silo).

    Ejemplo:
        src_id = add_source_node(
            label="SIAP-ICPI Gold Master v5.5",
            engine="RC-7.4",
            source_file="SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx",
            record_count=48,
        )
    """
    g = get_graph()
    nid = _make_node_id(label, engine, source_file)
    if nid not in g.nodes:
        g.nodes[nid] = ProvenanceNode(
            node_id=nid,
            node_type="SOURCE",
            label=label,
            engine=engine,
            confidence=confidence,
            payload={"source_file": source_file, "record_count": record_count},
        )
    return nid


def add_transform_node(
    label: str,
    engine: str,
    function_name: str,
    confidence: float,
    parent_ids: List[str],
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Registra una transformación realizada por un motor RC.

    Ejemplo:
        tx_id = add_transform_node(
            label="D4 analyze_territory",
            engine="RC-D4",
            function_name="analyze_territory",
            confidence=0.72,
            parent_ids=[src_id],
        )
    """
    g = get_graph()
    nid = _make_node_id(label, engine, function_name)
    # Propagar confianza mínima de padres
    parent_confs = [g.nodes[p].confidence for p in parent_ids if p in g.nodes]
    effective_conf = min([confidence] + parent_confs) if parent_confs else confidence

    if nid not in g.nodes:
        payload = {"function_name": function_name, **(extra or {})}
        g.nodes[nid] = ProvenanceNode(
            node_id=nid,
            node_type="TRANSFORM",
            label=label,
            engine=engine,
            confidence=round(effective_conf, 4),
            payload=payload,
            parents=list(parent_ids),
        )
        for pid in parent_ids:
            g.edges.append(ProvenanceEdge(source_id=pid, target_id=nid, edge_type="derives_from"))
    return nid


def add_inference_node(
    label: str,
    engine: str,
    result_type: str,
    confidence: float,
    parent_ids: List[str],
    pattern: str = "",
    observational: bool = False,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Registra un resultado inferencial (patrón detectado, calibración).

    Ejemplo:
        inf_id = add_inference_node(
            label="D3xD4 CONVERGENCIA_CRITICA [OBS]",
            engine="RC-D3D4",
            result_type="D3D4CrossResult",
            confidence=0.1255,
            parent_ids=[d3_tx_id, d4_tx_id],
            pattern="CONVERGENCIA_CRITICA",
            observational=True,
        )
    """
    g = get_graph()
    key = f"{result_type}|{pattern}|{observational}"
    nid = _make_node_id(label, engine, key)
    parent_confs = [g.nodes[p].confidence for p in parent_ids if p in g.nodes]
    effective_conf = min([confidence] + parent_confs) if parent_confs else confidence

    if nid not in g.nodes:
        payload = {
            "result_type":   result_type,
            "pattern":       pattern,
            "observational": observational,
            **(extra or {}),
        }
        g.nodes[nid] = ProvenanceNode(
            node_id=nid,
            node_type="INFERENCE",
            label=label,
            engine=engine,
            confidence=round(effective_conf, 4),
            payload=payload,
            parents=list(parent_ids),
        )
        for pid in parent_ids:
            g.edges.append(ProvenanceEdge(source_id=pid, target_id=nid, edge_type="derives_from"))
    return nid


def add_normative_node(
    label: str,
    engine: str,
    tier: str,
    n_refs: int,
    parent_ids: List[str],
    confidence: float = 1.0,
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Registra un binding normativo.

    Ejemplo:
        norm_id = add_normative_node(
            label="D3xD4 Normative POTENCIAL",
            engine="RC-D3D4-Normative",
            tier="potencial",
            n_refs=2,
            parent_ids=[inf_id],
        )
    """
    g = get_graph()
    nid = _make_node_id(label, engine, tier)
    parent_confs = [g.nodes[p].confidence for p in parent_ids if p in g.nodes]
    effective_conf = min([confidence] + parent_confs) if parent_confs else confidence

    if nid not in g.nodes:
        payload = {"tier": tier, "n_refs": n_refs, **(extra or {})}
        g.nodes[nid] = ProvenanceNode(
            node_id=nid,
            node_type="NORMATIVE",
            label=label,
            engine=engine,
            confidence=round(effective_conf, 4),
            payload=payload,
            parents=list(parent_ids),
        )
        for pid in parent_ids:
            g.edges.append(ProvenanceEdge(source_id=pid, target_id=nid, edge_type="derives_from"))
    return nid


def add_governed_by(node_id: str, rc_contract: str) -> None:
    """Registra que un nodo está gobernado por un contrato RC."""
    g = get_graph()
    # El contrato es un meta-nodo virtual
    contract_id = _make_node_id(rc_contract, "RC-CORE", rc_contract)
    if contract_id not in g.nodes:
        g.nodes[contract_id] = ProvenanceNode(
            node_id=contract_id,
            node_type="SOURCE",
            label=f"Contrato {rc_contract}",
            engine="RC-CORE",
            confidence=1.0,
            payload={"contract": rc_contract},
        )
    g.edges.append(ProvenanceEdge(
        source_id=contract_id,
        target_id=node_id,
        edge_type="governed_by",
    ))


# ── CONSULTA ───────────────────────────────────────────────────────────────────

def get_ancestry(node_id: str) -> List[ProvenanceNode]:
    """
    Retorna todos los ancestros de un nodo en orden topológico.
    Útil para responder '¿de dónde viene esta inferencia?'
    """
    g = get_graph()
    visited: List[str] = []
    queue = [node_id]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.append(current)
        node = g.nodes.get(current)
        if node:
            queue.extend(node.parents)
    # Excluir el nodo raíz del resultado
    return [g.nodes[nid] for nid in visited[1:] if nid in g.nodes]


def get_confidence_chain(node_id: str) -> Dict[str, float]:
    """
    Retorna la cadena de confianza desde la fuente hasta el nodo.
    Dict[label → confidence]
    """
    ancestry = get_ancestry(node_id)
    chain = {n.label: n.confidence for n in ancestry}
    node = get_graph().nodes.get(node_id)
    if node:
        chain[node.label] = node.confidence
    return chain


def get_nodes_by_engine(engine: str) -> List[ProvenanceNode]:
    """Retorna todos los nodos de un motor RC específico."""
    return [n for n in get_graph().nodes.values() if n.engine == engine]


def summarize_graph() -> Dict[str, Any]:
    """Resumen compacto del grafo para prompt injection."""
    g = get_graph()
    by_type: Dict[str, int] = {}
    for n in g.nodes.values():
        by_type[n.node_type] = by_type.get(n.node_type, 0) + 1

    # Nodo de confianza mínima
    inference_nodes = [n for n in g.nodes.values() if n.node_type == "INFERENCE"]
    min_conf_node = min(inference_nodes, key=lambda n: n.confidence) if inference_nodes else None

    return {
        "total_nodes":  len(g.nodes),
        "total_edges":  len(g.edges),
        "by_type":      by_type,
        "session_id":   g.session_id,
        "min_conf_inference": {
            "label":      min_conf_node.label if min_conf_node else None,
            "engine":     min_conf_node.engine if min_conf_node else None,
            "confidence": min_conf_node.confidence if min_conf_node else None,
        },
    }


def get_provenance_block(node_id: str, max_ancestors: int = 5) -> str:
    """
    Bloque de texto de procedencia para incluir en prompt (máx ~100 tokens).
    Formato compacto para no saturar contexto Haiku.
    """
    g = get_graph()
    node = g.nodes.get(node_id)
    if not node:
        return ""

    ancestry = get_ancestry(node_id)[:max_ancestors]
    lines = [f"[PROVENANCE:{node.engine}]"]
    lines.append(f"  nodo: {node.label} (conf={node.confidence:.2f})")
    if ancestry:
        lines.append("  cadena:")
        for anc in ancestry:
            tp = anc.node_type[:3]
            lines.append(f"    ← [{tp}] {anc.label} (conf={anc.confidence:.2f})")

    # Patrón/tier clave
    if node.payload.get("pattern"):
        obs = " [OBS]" if node.payload.get("observational") else ""
        lines.append(f"  patron: {node.payload['pattern']}{obs}")
    if node.payload.get("tier"):
        lines.append(f"  tier: {node.payload['tier']}")

    return "\n".join(lines)


def export_graph_json() -> str:
    """Serializa el grafo completo a JSON (para debug / audit)."""
    g = get_graph()
    data = {
        "session_id": g.session_id,
        "created_at": g.created_at,
        "nodes": [
            {
                "id":         n.node_id,
                "type":       n.node_type,
                "label":      n.label,
                "engine":     n.engine,
                "confidence": n.confidence,
                "payload":    n.payload,
                "parents":    n.parents,
                "timestamp":  n.timestamp,
            }
            for n in g.nodes.values()
        ],
        "edges": [
            {
                "from":      e.source_id,
                "to":        e.target_id,
                "type":      e.edge_type,
                "weight":    e.weight,
            }
            for e in g.edges
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


# ── REGISTRO AUTOMÁTICO DESDE RESULTADOS RC ───────────────────────────────────

def register_d3_result(d3_dict: Optional[dict]) -> Optional[str]:
    """
    Registra automáticamente el resultado D3 (RC-7.2/7.3) en el grafo.
    Retorna node_id del nodo INFERENCE creado, o None si no hay datos.
    """
    if not d3_dict or not d3_dict.get("has_data"):
        return None

    # Nodo fuente: Gold Master Excel (RC-7.4)
    src_id = add_source_node(
        label="Gold Master Excel — Series Presupuestarias",
        engine="RC-7.4",
        source_file="SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx",
        confidence=1.0,
    )
    add_governed_by(src_id, "RC-7.4")

    # Nodo transform: analyze_series
    n_periods = d3_dict.get("n_periodos", 0)
    tx_id = add_transform_node(
        label=f"RC-7.2 analyze_series ({n_periods} periodos)",
        engine="RC-7.2",
        function_name="analyze_series",
        confidence=float(d3_dict.get("evidence_wt", 0.5)),
        parent_ids=[src_id],
        extra={"n_periodos": n_periods},
    )
    add_governed_by(tx_id, "RC-7.2")

    # Nodo INFERENCE: calibrated_result
    avep_class = d3_dict.get("avep_class", "SIN_PATRON_CLARO")
    conf = float(d3_dict.get("calibrated_confidence", 0.1))
    inf_id = add_inference_node(
        label=f"D3 CalibratedResult [{avep_class}]",
        engine="RC-7.3",
        result_type="CalibratedResult",
        confidence=conf,
        parent_ids=[tx_id],
        pattern=avep_class,
        observational=(conf < 0.25),
        extra={
            "avep_score": d3_dict.get("avep_score"),
            "avep_riesgo": d3_dict.get("avep_riesgo"),
        },
    )
    add_governed_by(inf_id, "RC-7.3")
    return inf_id


def register_d4_result(d4_dict: Optional[dict]) -> Optional[str]:
    """
    Registra automáticamente el resultado D4 (RC-D4) en el grafo.
    """
    if not d4_dict or not d4_dict.get("has_data"):
        return None

    src_id = add_source_node(
        label="Gold Master Excel — Datos Parroquiales",
        engine="RC-7.4",
        source_file="SIAP-ICPI_GOLD_MASTER_v5.5_TGI.xlsx",
        confidence=1.0,
    )
    add_governed_by(src_id, "RC-7.4")

    n_parishes = d4_dict.get("n_parroquias", 0)
    tx_id = add_transform_node(
        label=f"RC-D4 analyze_territory ({n_parishes} parroquias)",
        engine="RC-D4",
        function_name="analyze_territory",
        confidence=float(d4_dict.get("confidence", 0.5)),
        parent_ids=[src_id],
        extra={"n_parroquias": n_parishes, "irs": d4_dict.get("irs")},
    )
    add_governed_by(tx_id, "RC-D4")

    pattern = d4_dict.get("principal_pattern", "SIN_PATRON")
    conf = float(d4_dict.get("confidence", 0.5))
    irs = float(d4_dict.get("irs", 0.0))
    overwhelm = irs >= 85.0
    inf_id = add_inference_node(
        label=f"D4 Result [{pattern}] IRS={irs:.1f}",
        engine="RC-D4",
        result_type="D4Result",
        confidence=conf,
        parent_ids=[tx_id],
        pattern=pattern,
        observational=False,  # D4 no tiene flag observacional propio
        extra={"irs": irs, "overwhelm": overwhelm},
    )
    add_governed_by(inf_id, "RC-D4")
    return inf_id


def register_cross_result(
    cross_dict: Optional[dict],
    d3_node_id: Optional[str],
    d4_node_id: Optional[str],
) -> Optional[str]:
    """
    Registra el resultado D3xD4 (RC-D3D4) en el grafo.
    Depende de los nodos D3 y D4 ya registrados.
    """
    if not cross_dict:
        return None

    parents = [p for p in [d3_node_id, d4_node_id] if p]
    cross_pattern = cross_dict.get("cross_pattern", "SIN_CRUCE_CONFIRMADO")
    cross_conf    = float(cross_dict.get("cross_confidence", 0.0))
    obs           = bool(cross_dict.get("observational_only", True))
    eed           = float(cross_dict.get("eed_score", 0.0))

    inf_id = add_inference_node(
        label=f"D3xD4 [{cross_pattern}]{'[OBS]' if obs else ''}",
        engine="RC-D3D4",
        result_type="D3D4CrossResult",
        confidence=cross_conf,
        parent_ids=parents,
        pattern=cross_pattern,
        observational=obs,
        extra={"eed_score": eed, "eed_class": cross_dict.get("eed_class")},
    )
    add_governed_by(inf_id, "RC-D3D4")
    return inf_id


def register_cross_normative(
    normative_dict: Optional[dict],
    cross_node_id: Optional[str],
) -> Optional[str]:
    """
    Registra el binding normativo D3xD4 en el grafo.
    """
    if not normative_dict or not cross_node_id:
        return None

    tier   = normative_dict.get("overall_tier", "sin_tension")
    n_refs = len(normative_dict.get("references", []))
    obs    = normative_dict.get("observational_only", True)

    if tier == "sin_tension":
        return None

    norm_id = add_normative_node(
        label=f"D3xD4 Normative [{tier.upper()}]{'[OBS]' if obs else ''}",
        engine="RC-D3D4-Normative",
        tier=tier,
        n_refs=n_refs,
        parent_ids=[cross_node_id],
        extra={"pdot_brecha": normative_dict.get("pdot_brecha")},
    )
    add_governed_by(norm_id, "RC-D3D4-Normative")
    add_governed_by(norm_id, "PDOT")
    return norm_id


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    print("=" * 65)
    print("Provenance Graph — QUIRA OS  (demo con datos Montecristi)")
    print("=" * 65)

    # ── Datos mock Montecristi ─────────────────────────────────────
    d3_mock = {
        "has_data": True, "avep_class": "SIN_PATRON_CLARO",
        "avep_score": 72.3, "avep_riesgo": "Moderado",
        "calibrated_confidence": 0.07, "evidence_wt": 0.30,
        "n_periodos": 2,
    }
    d4_mock = {
        "has_data": True, "principal_pattern": "CONCENTRACION_TERRITORIAL",
        "irs": 93.1, "confidence": 0.72, "n_parroquias": 6,
    }
    cross_mock = {
        "cross_pattern": "CONVERGENCIA_CRITICA", "cross_confidence": 0.1255,
        "observational_only": True, "eed_score": 18.9, "eed_class": "expansion_concentrada",
    }
    norm_mock = {
        "overall_tier": "potencial", "observational_only": True,
        "references": [{"code": "PDOT-D4"}, {"code": "CRE-238"}],
        "pdot_brecha": 48.1,
    }

    # ── Registro ───────────────────────────────────────────────────
    d3_id   = register_d3_result(d3_mock)
    d4_id   = register_d4_result(d4_mock)
    cross_id = register_cross_result(cross_mock, d3_id, d4_id)
    norm_id  = register_cross_normative(norm_mock, cross_id)

    print(f"\n  Nodo D3  : {d3_id}")
    print(f"  Nodo D4  : {d4_id}")
    print(f"  Nodo Cross: {cross_id}")
    print(f"  Nodo Norm : {norm_id}")

    # ── Resumen ────────────────────────────────────────────────────
    summary = summarize_graph()
    print(f"\n── Resumen del grafo ──")
    print(f"  Total nodos : {summary['total_nodes']}")
    print(f"  Total aristas: {summary['total_edges']}")
    print(f"  Por tipo    : {summary['by_type']}")
    min_inf = summary['min_conf_inference']
    if min_inf['label']:
        print(f"  Confianza minima [INFERENCE]: {min_inf['confidence']:.4f} ({min_inf['label']})")

    # ── Bloque de proveniencia ─────────────────────────────────────
    if cross_id:
        print(f"\n── Bloque de proveniencia (para prompt) ──")
        block = get_provenance_block(cross_id)
        print(block)

    # ── Cadena de confianza ────────────────────────────────────────
    if cross_id:
        chain = get_confidence_chain(cross_id)
        print(f"\n── Cadena de confianza ──")
        for label, conf in chain.items():
            bar = "█" * int(conf * 20)
            print(f"  {conf:.2f} {bar:<20} {label[:50]}")
