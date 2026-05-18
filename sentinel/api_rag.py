"""
SENTINEL RAG · api_rag.py
FastAPI — puente entre Streamlit PMV, Next.js y el motor RAG.
Soporta: respuesta JSON (retrieval) y streaming SSE (LLM).
Ejecutar: uvicorn sentinel.api_rag:app --host 0.0.0.0 --port 8100 --reload
Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import time
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import StreamingResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
except ImportError:
    print("❌ Instalar: pip install fastapi uvicorn")
    sys.exit(1)

from sentinel.rag_config import ANTHROPIC_API_KEY, RAG_TOP_K, INDEX_VERSION, FUENTE_VERSION
from sentinel.query_rag import (
    retrieve, query_retrieval_only, query_with_llm,
    ChunkResult, SentinelResponse
)
from sentinel.explain       import explain_retrieval, to_dict as explain_to_dict
from sentinel.guardrails    import apply_guardrails,  to_dict as guardrail_to_dict
from sentinel.decision_log  import log_decision, read_recent, get_stats as log_stats
from sentinel.profiles      import (
    format_for_role, ROL_ANALISTA, ROL_DIRECTIVO, ROL_POLITICO, ROLES_VALIDOS
)
from sentinel.ingest_validator import (
    validate_document, to_dict as validation_to_dict, ValidationState
)
from sentinel.query_rag import synthesize_for_role
from sentinel.human_review import (
    ReviewStatus, submit_review, read_reviews,
    get_review_stats, get_pending_decisions, get_review_for_decision,
)
from sentinel.review_governance import (
    open_case, escalate, close_case,
    get_cases, get_case,
    calculate_trust_drift, to_dict as drift_to_dict,
    NivelRevision, CaseStatus,
)
from sentinel.sla_layer import (
    create_sla, close_sla, get_sla,
    get_all_slas, get_sla_summary,
    update_sla_owner, Priority,
)

# Importar LLM_MODEL para el log de decisiones
from sentinel.rag_config import LLM_MODEL

# ── APP ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="SENTINEL RAG API",
    description="Copiloto de inteligencia territorial — GAD Montecristi · Dylus Lab",
    version=f"{FUENTE_VERSION}-{INDEX_VERSION}",
    docs_url="/sentinel/docs",
    redoc_url="/sentinel/redoc",
)

# CORS — permite acceso desde Next.js (localhost:3000) y Streamlit (localhost:8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── SCHEMAS ───────────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    pregunta: str = Field(..., min_length=3, max_length=1000,
                          example="¿Por qué D3 ejecución presupuestaria está en rojo?")
    k:        int = Field(default=RAG_TOP_K, ge=1, le=10)
    modo:     str = Field(default="auto",
                          description="'retrieval' | 'llm' | 'auto' (llm si hay API key)")
    rol:      str = Field(default=ROL_ANALISTA,
                          description=f"Perfil de usuario: {', '.join(sorted(ROLES_VALIDOS))}")


class ChunkOut(BaseModel):
    nota:      str
    section:   str
    tipo_nota: str
    dimension: str
    score:     float
    preview:   str   # primeros 200 chars


class QueryResponse(BaseModel):
    pregunta:  str
    confianza: str
    modo:      str
    chunks:    list[ChunkOut]
    respuesta: str


# ── ENDPOINTS ─────────────────────────────────────────────────────────────────

@app.get("/sentinel/health")
def health():
    """Estado del sistema RAG."""
    chroma_ok = False
    total_chunks = 0
    try:
        import chromadb
        from sentinel.rag_config import CHROMA_DIR, CHROMA_COLLECTION
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        col = client.get_or_create_collection(CHROMA_COLLECTION)
        total_chunks = col.count()
        chroma_ok = True
    except Exception as e:
        pass

    return {
        "status":        "ok" if chroma_ok else "degraded",
        "chroma":        chroma_ok,
        "total_chunks":  total_chunks,
        "llm_disponible": bool(ANTHROPIC_API_KEY),
        "index_version": INDEX_VERSION,
        "fuente_version": FUENTE_VERSION,
        "timestamp":     time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


@app.post("/sentinel/query", response_model=QueryResponse)
def query_json(req: QueryRequest):
    """
    Consulta RAG — respuesta JSON completa con chunks y respuesta.
    Modo 'retrieval': solo recuperación (sin LLM, para validación).
    Modo 'llm': recuperación + LLM (requiere API key).
    Modo 'auto': LLM si hay key, retrieval si no.
    """
    modo_efectivo = req.modo
    if req.modo == "auto":
        modo_efectivo = "llm" if ANTHROPIC_API_KEY else "retrieval"

    chunks = retrieve(req.pregunta, k=req.k)

    if not chunks:
        return QueryResponse(
            pregunta  = req.pregunta,
            confianza = "🔴 Sin resultados",
            modo      = modo_efectivo,
            chunks    = [],
            respuesta = "No encontré información suficiente en el Knowledge Base.",
        )

    # Chunks para output
    chunks_out = [
        ChunkOut(
            nota      = c.nota,
            section   = c.section,
            tipo_nota = c.tipo_nota,
            dimension = c.dimension,
            score     = c.score,
            preview   = c.text[:200],
        )
        for c in chunks
    ]

    # Confianza promedio
    avg_score = sum(c.score for c in chunks) / len(chunks)
    confianza = "🟢 Alta" if avg_score >= 0.65 else "🟡 Media" if avg_score >= 0.40 else "🔴 Baja"

    if modo_efectivo == "retrieval":
        # Solo retrieval — juntar previews como respuesta
        previews = "\n\n".join(
            f"[{c.nota}] {c.section}:\n{c.text[:350]}" for c in chunks
        )
        return QueryResponse(
            pregunta  = req.pregunta,
            confianza = confianza,
            modo      = "retrieval",
            chunks    = chunks_out,
            respuesta = previews,
        )

    # LLM — acumular stream en respuesta JSON
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="API key de Anthropic no configurada. Usar modo='retrieval'."
        )

    full_response = ""
    for token in query_with_llm(req.pregunta):
        full_response += token

    return QueryResponse(
        pregunta  = req.pregunta,
        confianza = confianza,
        modo      = "llm",
        chunks    = chunks_out,
        respuesta = full_response,
    )


@app.post("/sentinel/stream")
def query_stream(req: QueryRequest):
    """
    Consulta RAG con streaming SSE (Server-Sent Events).
    Para uso desde Next.js / EventSource del browser.
    Requiere API key de Anthropic.
    """
    if not ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Streaming requiere ANTHROPIC_API_KEY configurada."
        )

    def event_stream():
        # Primero enviar los chunks recuperados como primer evento
        chunks = retrieve(req.pregunta, k=req.k)
        chunks_data = [
            {"nota": c.nota, "section": c.section, "score": c.score, "tipo": c.tipo_nota}
            for c in chunks
        ]
        yield f"event: chunks\ndata: {json.dumps(chunks_data, ensure_ascii=False)}\n\n"

        # Luego stream de tokens del LLM
        for token in query_with_llm(req.pregunta):
            # Escapar newlines para SSE
            escaped = token.replace("\n", "\\n")
            yield f"data: {escaped}\n\n"

        yield "event: done\ndata: [END]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/sentinel/explain")
def query_explain(req: QueryRequest):
    """
    Endpoint de producción (Sprint 1.5 + 1.6):
    - Trazabilidad auditable (explain_retrieval)
    - Guardrails institucionales (apply_guardrails)
    - Log auditado de decisiones (log_decision)
    - Respuesta adaptada al perfil de usuario (format_for_role)

    Roles: analista | directivo | politico
    """
    # 1. Trazabilidad auditable
    r = explain_retrieval(req.pregunta, k=req.k)

    # 2. Guardrails institucionales
    g = apply_guardrails(r)

    # 3. Sprint 2 — Síntesis LLM si hay API key y el guardrail permite responder
    llm_respuesta = ""
    llm_activado  = False
    if ANTHROPIC_API_KEY and g.puede_responder:
        llm_respuesta = synthesize_for_role(
            pregunta         = req.pregunta,
            chunks           = r.chunks,
            dims_cubiertas   = r.dims_cubiertas,
            guardrail_estado = g.estado.value,
            puede_recomendar = g.puede_recomendar,
            rol              = req.rol,
        )
        llm_activado = bool(llm_respuesta and not llm_respuesta.startswith("[Error"))

    # 4. Log auditado — siempre, independiente del estado
    log_decision(
        r=r, g=g, rol=req.rol,
        llm_activado=llm_activado,
        llm_modelo=LLM_MODEL if llm_activado else "",
    )

    # 5. Respuesta adaptada al rol
    resultado = format_for_role(
        r=r, g=g, rol=req.rol,
        llm_respuesta=llm_respuesta,
        llm_activado=llm_activado,
    )

    # 6. Trazabilidad raw (siempre en resp; solo analista recibe explain_raw completo)
    resultado["guardrail"]   = guardrail_to_dict(g)
    resultado["llm_modelo"]  = LLM_MODEL if llm_activado else ""
    if req.rol == ROL_ANALISTA:
        resultado["explain_raw"] = explain_to_dict(r)

    return resultado


@app.get("/sentinel/decisions")
def get_decisions(n: int = 50):
    """
    Log auditado de decisiones — Sprint 1.6.
    Retorna las últimas n consultas con su estado guardrail, confianza y fuentes.
    Permite auditoría institucional: 'por qué Sentinel sugirió esto'.
    """
    entries = read_recent(n)
    stats   = log_stats(min(n, 100))
    return {
        "entries": entries,
        "stats":   stats,
        "n":       n,
        "log_path": str(__import__("sentinel.decision_log", fromlist=["DECISIONS_LOG"]).DECISIONS_LOG),
    }


class ValidateRequest(BaseModel):
    texto:    str  = Field(..., min_length=10, description="Texto del documento a validar")
    filename: str  = Field(default="", description="Nombre del archivo (ayuda a clasificar el tipo)")


@app.post("/sentinel/validate")
def validate_doc(req: ValidateRequest):
    """
    Validador documental — Sprint 1.7.
    Aplica 5 guardrails antes de permitir la ingesta:
      G1. Texto ≥ 500 chars
      G2. Entidad institucional detectada
      G3. Fecha detectada
      G4. Tipo documental identificado
      G5. Score calidad textual ≥ 80%

    Estado APROBADO / ADVERTENCIA → puede ingestar
    Estado REQUIERE REVISIÓN / RECHAZADO → NO ingestar
    """
    result = validate_document(text=req.texto, filename=req.filename)
    return validation_to_dict(result)


class ReviewRequest(BaseModel):
    decision_ts: str = Field(
        ...,
        description="Timestamp de la decisión original (campo 'timestamp' en /sentinel/decisions)"
    )
    pregunta:    str = Field(..., min_length=3, max_length=1000,
                             description="Pregunta original (para trazabilidad del log)")
    status:      str = Field(
        ...,
        description="Estado de revisión: APROBAR | OBSERVAR | RECHAZAR"
    )
    reviewer:    str = Field(..., min_length=2, max_length=100,
                             description="Identificador del revisor (nombre/cargo)")
    comment:     str = Field(default="",
                             description="Justificación (obligatoria para OBSERVAR y RECHAZAR)")


@app.post("/sentinel/review")
def submit_human_review(req: ReviewRequest):
    """
    Human Override — Sprint 2.1.

    Registra una revisión humana sobre una decisión de Sentinel.
    Principio rector: SENTINEL recomienda. No gobierna.

    Estados:
      APROBAR  — El analista valida la recomendación.
      OBSERVAR — Acepta la información pero añade matiz o contexto.
      RECHAZAR — Descarta la recomendación (error, sesgo, contexto institucional).

    Nota: OBSERVAR y RECHAZAR requieren campo 'comment' con justificación.
    """
    try:
        review = submit_review(
            decision_ts = req.decision_ts,
            pregunta    = req.pregunta,
            status      = ReviewStatus(req.status.upper()),
            reviewer    = req.reviewer,
            comment     = req.comment,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return {
        "review_id":        review.review_id,
        "status":           review.status.value,
        "reviewer":         review.reviewer,
        "decision_ts":      review.decision_ts,
        "comment":          review.comment,
        "review_ts":        review.review_ts,
        "sentinel_version": review.sentinel_version,
        "mensaje":          f"✅ Revisión {review.status.value} registrada correctamente.",
    }


@app.get("/sentinel/reviews")
def get_reviews(n: int = 50):
    """
    Log de revisiones humanas — Sprint 2.1.
    Retorna las últimas n revisiones con estadísticas de aprobación/rechazo.
    """
    entries = read_reviews(n)
    summary = get_review_stats(min(n, 200))

    return {
        "entries": entries,
        "stats": {
            "total":           summary.total,
            "aprobadas":       summary.aprobadas,
            "observadas":      summary.observadas,
            "rechazadas":      summary.rechazadas,
            "tasa_aprobacion": summary.tasa_aprobacion,
            "tasa_rechazo":    summary.tasa_rechazo,
            "revisores":       summary.revisores,
        },
        "n": n,
    }


@app.get("/sentinel/reviews/pending")
def pending_reviews(n: int = 50):
    """
    Decisiones de Sentinel que aún no tienen revisión humana asociada.
    Útil para el panel de analistas — muestra la cola de revisión pendiente.
    """
    pending = get_pending_decisions(n_decisions=n)
    return {
        "pendientes": len(pending),
        "decisions":  pending,
    }


@app.get("/sentinel/reviews/lookup/{decision_ts}")
def lookup_review(decision_ts: str):
    """
    Busca si una decisión específica ya tiene revisión humana.
    Parámetro: decision_ts — campo 'timestamp' del log de decisiones.
    """
    review = get_review_for_decision(decision_ts)
    if review is None:
        return {"decision_ts": decision_ts, "revisado": False, "review": None}
    return {"decision_ts": decision_ts, "revisado": True, "review": review}


# ── GOVERNANCE — Sprint 2.2 ───────────────────────────────────────────────────

class EscalateRequest(BaseModel):
    decision_ts:   str = Field(..., description="Timestamp de la decisión a escalar")
    responsable:   str = Field(..., min_length=2, description="Responsable de la escalación")
    motivo:        str = Field(..., min_length=5, description="Motivo de la escalación")
    nivel_destino: str = Field(
        default="",
        description="Nivel destino: COORDINADOR | INSTITUCIONAL (vacío = automático)"
    )


class CloseRequest(BaseModel):
    decision_ts: str = Field(..., description="Timestamp de la decisión a cerrar")
    resolver:    str = Field(..., min_length=2, description="Responsable del cierre")
    resolucion:  str = Field(..., min_length=10, description="Resolución definitiva del caso")
    comment:     str = Field(default="", description="Comentario adicional (opcional)")


@app.post("/sentinel/governance/dispute")
def open_dispute(
    decision_ts: str,
    pregunta:    str,
):
    """
    Sprint 2.2 — Abre un caso de gobernanza para una decisión en conflicto.
    Detecta automáticamente el estado (EN_DISPUTA | PENDIENTE) según las revisiones existentes.

    Llama este endpoint cuando detectes que una decisión tiene revisiones contradictorias.
    """
    reviews = read_reviews(n=500)
    decision_reviews = [r for r in reviews if r.get("decision_ts") == decision_ts]

    if len(decision_reviews) < 2:
        raise HTTPException(
            status_code=422,
            detail=f"Se necesitan ≥2 revisiones para abrir un caso. Encontradas: {len(decision_reviews)}"
        )

    try:
        case = open_case(decision_ts, pregunta, decision_reviews)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Sprint 2.3 — Auto-crear SLA al abrir disputa
    _sla_priority = "alta" if case.estado.value == "EN_DISPUTA" else "media"
    _sla_info: dict = {}
    try:
        from sentinel.sla_layer import SLA_DEFAULT_OWNER as _SLA_OWNER
        _sla = create_sla(
            case_id     = case.case_id,
            decision_ts = case.decision_ts,
            pregunta    = case.pregunta,
            owner       = _SLA_OWNER,
            priority    = _sla_priority,
        )
        _sla_info = {
            "sla_owner":    _sla.owner,
            "sla_priority": _sla.priority,
            "sla_deadline": _sla.deadline,
            "sla_hours":    _sla.max_resolution_hours,
        }
    except Exception:
        pass  # SLA failure no bloquea apertura

    return {
        "case_id":      case.case_id,
        "decision_ts":  case.decision_ts,
        "estado":       case.estado.value,
        "nivel_actual": case.nivel_actual.value,
        "n_reviews":    len(case.reviews),
        "conflicto":    len({r.get("status") for r in case.reviews}) > 1,
        "sla":          _sla_info,
        "mensaje":      f"Caso {case.case_id} abierto — SLA {_sla_priority} ({_sla_info.get('sla_hours','?')}h) asignado.",
    }


@app.post("/sentinel/governance/escalate")
def escalate_case(req: EscalateRequest):
    """
    Sprint 2.2 — Escala un caso al siguiente nivel de revisión.
    ANALISTA → COORDINADOR → INSTITUCIONAL.
    """
    try:
        nivel = NivelRevision(req.nivel_destino.upper()) if req.nivel_destino else None
        result = escalate(
            decision_ts   = req.decision_ts,
            responsable   = req.responsable,
            motivo        = req.motivo,
            nivel_destino = nivel,
        )
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    return result


@app.post("/sentinel/governance/close")
def close_governance_case(req: CloseRequest):
    """
    Sprint 2.2 — Cierra un caso con resolución institucional definitiva.
    El cierre es irreversible.
    """
    try:
        result = close_case(
            decision_ts = req.decision_ts,
            resolver    = req.resolver,
            resolucion  = req.resolucion,
            comment     = req.comment,
        )
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    return result


@app.get("/sentinel/governance/cases")
def list_cases(estado: str = "", n: int = 50):
    """
    Sprint 2.2 — Lista casos de gobernanza, filtrados por estado opcional.
    Estados: PENDIENTE | EN_DISPUTA | ESCALADO | CERRADO
    """
    cases = get_cases(estado if estado else None)[:n]
    summary = {
        "total":      len(cases),
        "pendiente":  sum(1 for c in cases if c.get("estado") == "PENDIENTE"),
        "en_disputa": sum(1 for c in cases if c.get("estado") == "EN_DISPUTA"),
        "escalado":   sum(1 for c in cases if c.get("estado") == "ESCALADO"),
        "cerrado":    sum(1 for c in cases if c.get("estado") == "CERRADO"),
    }
    return {"cases": cases, "summary": summary}


@app.get("/sentinel/governance/case/{decision_ts}")
def get_governance_case(decision_ts: str):
    """Sprint 2.2 — Retorna el caso de gobernanza para una decisión específica."""
    case = get_case(decision_ts)
    if not case:
        raise HTTPException(status_code=404, detail=f"No existe caso para decision_ts='{decision_ts}'")
    return case


@app.get("/sentinel/trust-drift")
def trust_drift(n_weeks: int = 8):
    """
    Sprint 2.2 — Trust Drift Report.
    Mide la confianza institucional en Sentinel semana a semana.

    Alerta: si RECHAZAR >= 15% en cualquier semana, Sentinel está perdiendo
    alineación con la realidad institucional. Requiere revisión de prompts y vault.

    Tendencias: ESTABLE | DEGRADANDO | MEJORANDO
    """
    report = calculate_trust_drift(n_weeks=n_weeks)
    return drift_to_dict(report)


class SlaUpdateRequest(BaseModel):
    case_id:   str = Field(..., description="ID del caso de gobernanza")
    new_owner: str = Field(..., min_length=2, description="Nuevo responsable institucional")


@app.get("/sentinel/sla")
def list_sla(include_closed: bool = False):
    """
    Sprint 2.3 — Lista todos los SLAs activos con estado calculado en tiempo real.
    Estados: NORMAL 🟢 | SEGUIMIENTO 🟡 | CRITICO 🟠 | VENCIDO 🔴 | CUMPLIDO ✅

    Governance deadlock prevention: detecta SLAs vencidos automáticamente.
    """
    slas    = get_all_slas(include_closed=include_closed)
    summary = get_sla_summary()
    return {
        "slas":    slas,
        "summary": summary,
        "n":       len(slas),
    }


@app.get("/sentinel/sla/{case_id}")
def get_single_sla(case_id: str):
    """Sprint 2.3 — SLA de un caso específico con tiempo restante."""
    sla = get_sla(case_id)
    if not sla:
        raise HTTPException(status_code=404, detail=f"No existe SLA para case_id='{case_id}'")
    return sla


@app.post("/sentinel/sla/reassign")
def reassign_sla(req: SlaUpdateRequest):
    """Sprint 2.3 — Reasigna el owner de un SLA activo."""
    updated = update_sla_owner(req.case_id, req.new_owner)
    if not updated:
        raise HTTPException(status_code=404, detail=f"No existe SLA para case_id='{req.case_id}'")
    return {**updated, "mensaje": f"SLA reasignado a {req.new_owner}."}


@app.get("/sentinel/stats")
def stats():
    """Estadísticas del índice ChromaDB."""
    try:
        import chromadb
        from sentinel.rag_config import CHROMA_DIR, CHROMA_COLLECTION
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        col = client.get_or_create_collection(CHROMA_COLLECTION)

        # Sample de metadatos para distribución de tipos
        sample = col.get(limit=500, include=["metadatas"])
        tipo_dist: dict[str, int] = {}
        carpeta_dist: dict[str, int] = {}

        for meta in sample["metadatas"]:
            if not meta:
                continue
            t = meta.get("tipo_nota", "(sin tipo)")
            tipo_dist[t] = tipo_dist.get(t, 0) + 1
            c = meta.get("carpeta", "(raíz)")
            carpeta_dist[c] = carpeta_dist.get(c, 0) + 1

        return {
            "total_chunks":    col.count(),
            "index_version":   INDEX_VERSION,
            "fuente_canonica": __import__("sentinel.rag_config", fromlist=["FUENTE_CANONICA"]).FUENTE_CANONICA,
            "tipos":           tipo_dist,
            "carpetas":        carpeta_dist,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
