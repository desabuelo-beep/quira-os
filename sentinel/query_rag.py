"""
SENTINEL RAG · query_rag.py
Motor de consulta RAG — recuperación + (opcional) LLM.
Fase 1: solo recuperación → valida calidad del vault.
Fase 2: recuperación + Claude API → respuesta citada.
La API key no es requerida para la fase de validación.
Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import re
from dataclasses import dataclass, field
from typing import Generator

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.rag_config import (
    CHROMA_DIR, EMBED_MODEL, CHROMA_COLLECTION,
    RAG_TOP_K, MIN_SCORE, ANTHROPIC_API_KEY,
    LLM_MODEL, LLM_MAX_TOKENS, SENTINEL_SYSTEM_PROMPT,
    IP_BLOCKED_TERMS,
)


# ── RESULTADO ESTRUCTURADO ─────────────────────────────────────────────────────
@dataclass
class ChunkResult:
    chunk_id:    str
    nota:        str
    section:     str
    tipo_nota:   str
    dimension:   str
    carpeta:     str
    score:       float
    text:        str


@dataclass
class SentinelResponse:
    pregunta:   str
    chunks:     list[ChunkResult] = field(default_factory=list)
    respuesta:  str = ""
    modo:       str = "retrieval"   # "retrieval" | "llm"
    confianza:  str = ""            # 🟢 Alta | 🟡 Media | 🔴 Baja
    error:      str = ""


# ── SINGLETON PARA MODELO Y CHROMA ────────────────────────────────────────────
_model    = None
_client   = None
_collection = None


def _init_rag():
    global _model, _client, _collection
    if _model is not None:
        return

    try:
        import chromadb
        from sentence_transformers import SentenceTransformer
    except ImportError as e:
        raise RuntimeError(
            f"Dependencia faltante: {e}. "
            "Instalar con: pip install chromadb sentence-transformers"
        )

    _model = SentenceTransformer(EMBED_MODEL)
    _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    _collection = _client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"}
    )


# ── FILTRO IP ─────────────────────────────────────────────────────────────────
def _filter_ip(text: str) -> str:
    """
    Elimina términos protegidos de IP del texto antes de enviarlo al LLM.
    Sentinel puede mostrar RESULTADOS del motor, no su ARQUITECTURA.
    """
    for term in IP_BLOCKED_TERMS:
        # Reemplazar término con [PROTEGIDO - IP Dylus Lab]
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub("[contenido protegido]", text)
    return text


# ── RECUPERACIÓN SEMÁNTICA ────────────────────────────────────────────────────
def retrieve(pregunta: str, k: int = RAG_TOP_K) -> list[ChunkResult]:
    """
    Convierte la pregunta en embedding y busca los k chunks más relevantes.
    """
    _init_rag()

    q_embedding = _model.encode(pregunta).tolist()

    results = _collection.query(
        query_embeddings=[q_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    if not results["ids"] or not results["ids"][0]:
        return chunks

    for chunk_id, doc, meta, dist in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        # ChromaDB cosine distance → similarity score
        score = 1.0 - dist
        if score < MIN_SCORE:
            continue

        chunks.append(ChunkResult(
            chunk_id  = chunk_id,
            nota      = meta.get("nota", ""),
            section   = meta.get("section", ""),
            tipo_nota = meta.get("tipo_nota", ""),
            dimension = meta.get("dimension_tgi", ""),
            carpeta   = meta.get("carpeta", ""),
            score     = round(score, 3),
            text      = _filter_ip(doc),
        ))

    return chunks


def _score_confianza(chunks: list[ChunkResult]) -> str:
    if not chunks:
        return "🔴 Sin resultados"
    avg = sum(c.score for c in chunks) / len(chunks)
    if avg >= 0.65:
        return "🟢 Alta"
    elif avg >= 0.40:
        return "🟡 Media"
    else:
        return "🔴 Baja — revisar vault"


# ── RESPUESTA SOLO RETRIEVAL (sin LLM, para validación Sprint 0) ──────────────
def query_retrieval_only(pregunta: str) -> SentinelResponse:
    """
    Retorna los chunks recuperados sin pasar por el LLM.
    Usar en Sprint 0/1 para validar que el vault está bien indexado.
    """
    chunks = retrieve(pregunta)
    confianza = _score_confianza(chunks)

    # Construir respuesta textual con los chunks
    if not chunks:
        respuesta = "No se encontraron fragmentos relevantes en el Knowledge Base."
    else:
        partes = []
        for i, c in enumerate(chunks, 1):
            partes.append(
                f"[{i}] {c.nota} · {c.section} (score: {c.score})\n"
                f"{c.text[:400]}..."
            )
        respuesta = "\n\n".join(partes)

    return SentinelResponse(
        pregunta  = pregunta,
        chunks    = chunks,
        respuesta = respuesta,
        modo      = "retrieval",
        confianza = confianza,
    )


# ── RESPUESTA CON LLM (streaming) ─────────────────────────────────────────────
def query_with_llm(pregunta: str) -> Generator[str, None, None]:
    """
    Pipeline RAG completo con streaming Claude API.
    Requiere ANTHROPIC_API_KEY en .env
    Uso: for token in query_with_llm(pregunta): print(token, end="", flush=True)
    """
    if not ANTHROPIC_API_KEY:
        yield "⚠️ No hay API key de Anthropic. "
        yield "Configurar ANTHROPIC_API_KEY en .env o variables de entorno.\n"
        yield "\n--- MODO RETRIEVAL (sin LLM) ---\n"
        resp = query_retrieval_only(pregunta)
        yield resp.respuesta
        return

    try:
        import anthropic
    except ImportError:
        yield "⚠️ Instalar: pip install anthropic\n"
        return

    # 1. Recuperar chunks relevantes
    chunks = retrieve(pregunta)
    confianza = _score_confianza(chunks)

    if not chunks:
        yield "No encontré información suficiente en el Knowledge Base para responder esto.\n"
        yield f"\n*Confianza: {confianza}*"
        return

    # 2. Construir contexto — solo texto filtrado por IP
    contexto = "\n\n---\n\n".join(
        f"Fuente: {c.nota} · {c.section}\n{c.text}" for c in chunks
    )

    fuentes_str = "\n".join(
        f"- {c.nota} ({c.tipo_nota}, score={c.score})" for c in chunks
    )

    # 3. Llamar Claude con streaming
    client_llm = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    user_message = (
        f"CONTEXTO RECUPERADO DEL KNOWLEDGE BASE:\n{contexto}\n\n"
        f"PREGUNTA: {pregunta}"
    )

    try:
        with client_llm.messages.stream(
            model=LLM_MODEL,
            max_tokens=LLM_MAX_TOKENS,
            system=SENTINEL_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            for text in stream.text_stream:
                yield text

        # Citas al final
        yield f"\n\n---\n**Fuentes recuperadas ({confianza}):**\n{fuentes_str}"

    except Exception as e:
        yield f"\n⚠️ Error LLM: {e}\n"
        yield "\n--- MODO RETRIEVAL (fallback) ---\n"
        resp = query_retrieval_only(pregunta)
        yield resp.respuesta


# ── FORMATO RESPUESTA CONSOLA ─────────────────────────────────────────────────
def format_retrieval_response(resp: SentinelResponse) -> str:
    """Formatea una SentinelResponse para display en consola."""
    sep = "═" * 62
    lines = [
        sep,
        f"  SENTINEL · Respuesta [{resp.modo.upper()}]",
        sep,
        f"  Pregunta: {resp.pregunta}",
        f"  Confianza: {resp.confianza}",
        "─" * 62,
    ]

    if resp.chunks:
        lines.append("  Fragmentos recuperados:")
        for i, c in enumerate(resp.chunks, 1):
            lines.append(f"  [{i}] {c.nota} · '{c.section}'  score={c.score}")
            lines.append(f"      tipo={c.tipo_nota}  dim={c.dimension}  carpeta={c.carpeta}")
        lines.append("─" * 62)

    lines.append("  Contenido:")
    for chunk in resp.chunks[:2]:  # mostrar primeros 2 chunks en consola
        preview = chunk.text[:300].replace("\n", " ")
        lines.append(f"  ···  {preview}...")
        lines.append("")

    if resp.error:
        lines.append(f"  ⚠️ Error: {resp.error}")

    lines.append(sep)
    return "\n".join(lines)


# ── SÍNTESIS LLM POR ROL (Sprint 2) ──────────────────────────────────────────
# Addendum al SENTINEL_SYSTEM_PROMPT según el perfil del usuario
_ROLE_ADDENDUM: dict[str, str] = {
    "analista": """
PERFIL ACTIVO: ANALISTA TÉCNICO
- Responde con detalle técnico completo
- Cita cada fuente como [nota_id] tras cada afirmación importante
- Incluye dimensiones TGI cubiertas cuando sea relevante
- Puedes usar términos técnicos: ICPI, TGI, IRS, COOTAD, COPFP, eSIGEF, SERCOP
- Formato: párrafos técnicos + listado de fuentes al final
- Máximo 450 palabras
""",
    "directivo": """
PERFIL ACTIVO: DIRECTIVO MUNICIPAL
- Sintetiza en máximo 3 párrafos ejecutivos concisos
- Párrafo 1: situación actual con semáforo institucional (🟢/🟡/🔴)
- Párrafo 2: causa raíz del problema o hallazgo principal
- Párrafo 3: UNA recomendación de acción concreta, factible y con plazo
- Cita fuentes de forma natural: "Según el PDOT cantonal..." o "De acuerdo con..."
- SIN scores numéricos, SIN siglas técnicas no explicadas
- Máximo 250 palabras
""",
    "politico": """
PERFIL ACTIVO: AUTORIDAD POLÍTICA (Alcalde / Concejal)
- Usa lenguaje ciudadano y político — CERO tecnicismos ni siglas
- Conecta la respuesta con el mandato 2023-2027 y el impacto en la ciudadanía
- Responde implícitamente: ¿qué significa esto para los habitantes de Montecristi?
- Si hay riesgo, explícalo en términos de servicios, obras e impacto social
- Máximo 2 párrafos. Sin scores. Sin dimensiones. Sin nombres de sistemas.
- Si no puedes recomendar, di por qué de forma comprensible para ciudadanos
""",
}


def synthesize_for_role(
    pregunta:          str,
    chunks:            list["ChunkResult"],
    dims_cubiertas:    list[str],
    guardrail_estado:  str,
    puede_recomendar:  bool,
    rol:               str = "analista",
) -> str:
    """
    Genera síntesis LLM adaptada al rol usando Claude Haiku.

    Sprint 2: llamada sincrónica (retorna string completo).
    El endpoint /sentinel/explain llama esto cuando ANTHROPIC_API_KEY está set.
    El endpoint /sentinel/stream sigue usando query_with_llm (streaming).

    Retorna "" si no hay API key o si hay error.
    """
    if not ANTHROPIC_API_KEY:
        return ""

    try:
        import anthropic
    except ImportError:
        return ""

    # Contexto rico: chunks con scores + cobertura dimensional
    contexto_chunks = "\n\n---\n\n".join(
        f"Fuente [{c.nota}] (score={c.score}, sección='{c.section}'):\n{c.text}"
        for c in chunks
    )
    dims_str = ", ".join(dims_cubiertas) if dims_cubiertas else "no determinadas"

    user_message = (
        f"CONTEXTO RECUPERADO DEL KNOWLEDGE BASE:\n"
        f"{contexto_chunks}\n\n"
        f"METADATOS DE CONFIANZA:\n"
        f"  · Dimensiones TGI cubiertas: {dims_str}\n"
        f"  · Estado guardrail:          {guardrail_estado}\n"
        f"  · Puede emitir recomendación: {'Sí' if puede_recomendar else 'No — solo informar'}\n\n"
        f"PREGUNTA DEL USUARIO:\n{pregunta}"
    )

    # Sistema base + addendum por rol
    rol_key    = rol if rol in _ROLE_ADDENDUM else "analista"
    system_msg = SENTINEL_SYSTEM_PROMPT.strip() + "\n\n" + _ROLE_ADDENDUM[rol_key].strip()

    client_llm = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    try:
        response = client_llm.messages.create(
            model      = LLM_MODEL,
            max_tokens = LLM_MAX_TOKENS,
            system     = system_msg,
            messages   = [{"role": "user", "content": user_message}],
        )
        return response.content[0].text
    except Exception as e:
        return f"[Error LLM: {e}]"


# ── CLI DE PRUEBA ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        pregunta = " ".join(sys.argv[1:])
    else:
        pregunta = "¿Por qué D3 ejecución presupuestaria está en rojo?"

    print(f"\nModo: {'LLM' if ANTHROPIC_API_KEY else 'RETRIEVAL ONLY'}")
    print(f"Pregunta: {pregunta}\n")

    if ANTHROPIC_API_KEY:
        for token in query_with_llm(pregunta):
            print(token, end="", flush=True)
        print()
    else:
        resp = query_retrieval_only(pregunta)
        print(format_retrieval_response(resp))
