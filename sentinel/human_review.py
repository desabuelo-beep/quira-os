"""
SENTINEL RAG · human_review.py
Sprint 2.1 — Human Override System.

Principio rector: SENTINEL recomienda. No gobierna.
Todo análisis puede ser revisado, observado o rechazado por un analista humano.

Estados: APROBAR | OBSERVAR | RECHAZAR
Log: sentinel/logs/human_reviews.jsonl (append-only)

Dylus Lab © 2026
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from typing import Optional

from sentinel.rag_config import LOGS_DIR, SENTINEL_VERSION, GUARDRAIL_VERSION

# ── RUTA DEL LOG ──────────────────────────────────────────────────────────────
REVIEWS_LOG = LOGS_DIR / "human_reviews.jsonl"
REVIEWS_LOG.parent.mkdir(parents=True, exist_ok=True)


# ── ENUM DE ESTADOS ───────────────────────────────────────────────────────────
class ReviewStatus(str, Enum):
    """
    Estado de revisión humana.

    APROBAR   — El analista valida la recomendación de Sentinel.
    OBSERVAR  — Acepta la información pero matiza o añade contexto.
    RECHAZAR  — Descarta la recomendación por error, sesgo u otro motivo institucional.
    """
    APROBAR  = "APROBAR"
    OBSERVAR = "OBSERVAR"
    RECHAZAR = "RECHAZAR"


# ── DATACLASSES ───────────────────────────────────────────────────────────────
@dataclass
class HumanReview:
    """
    Registro de una revisión humana sobre una decisión de Sentinel.

    Campos:
        review_id         — ID único de la revisión (timestamp ISO + revisor)
        decision_ts       — Timestamp de la decisión original en decisions.jsonl
        pregunta          — Pregunta original consultada
        status            — APROBAR | OBSERVAR | RECHAZAR
        reviewer          — Identificador del revisor (nombre/rol institucional)
        comment           — Justificación textual obligatoria para OBSERVAR/RECHAZAR
        sentinel_version  — Versión de Sentinel en el momento de la revisión
        guardrail_version — Versión de guardrails activa
        review_ts         — Timestamp ISO de la revisión
    """
    review_id:         str
    decision_ts:       str
    pregunta:          str
    status:            ReviewStatus
    reviewer:          str
    comment:           str
    sentinel_version:  str
    guardrail_version: str
    review_ts:         str


@dataclass
class ReviewSummary:
    """Resumen estadístico de las revisiones."""
    total:           int
    aprobadas:       int
    observadas:      int
    rechazadas:      int
    tasa_aprobacion: float   # % sobre total
    tasa_rechazo:    float   # % sobre total
    revisores:       list[str]
    ultimas_n:       int


# ── ESCRITURA ─────────────────────────────────────────────────────────────────
def submit_review(
    decision_ts: str,
    pregunta:    str,
    status:      ReviewStatus | str,
    reviewer:    str,
    comment:     str = "",
) -> HumanReview:
    """
    Registra una revisión humana sobre una decisión de Sentinel.

    Args:
        decision_ts  — Timestamp de la decisión original (campo 'timestamp' de decisions.jsonl)
        pregunta     — Pregunta consultada (para trazabilidad, sin necesidad de lookup)
        status       — ReviewStatus.APROBAR | OBSERVAR | RECHAZAR (o string equivalente)
        reviewer     — Identificador del revisor
        comment      — Comentario/justificación (obligatorio para OBSERVAR y RECHAZAR)

    Returns:
        HumanReview — registro persistido
    """
    if isinstance(status, str):
        try:
            status = ReviewStatus(status.upper())
        except ValueError:
            raise ValueError(
                f"Estado '{status}' inválido. Usar: APROBAR | OBSERVAR | RECHAZAR"
            )

    # Validar comentario obligatorio para OBSERVAR y RECHAZAR
    if status in (ReviewStatus.OBSERVAR, ReviewStatus.RECHAZAR) and not comment.strip():
        raise ValueError(
            f"El estado {status.value} requiere un comentario de justificación."
        )

    now_ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    review_id = f"{now_ts}_{reviewer[:12].replace(' ', '_')}"

    review = HumanReview(
        review_id         = review_id,
        decision_ts       = decision_ts,
        pregunta          = pregunta,
        status            = status,
        reviewer          = reviewer,
        comment           = comment.strip(),
        sentinel_version  = SENTINEL_VERSION,
        guardrail_version = GUARDRAIL_VERSION,
        review_ts         = now_ts,
    )

    # Persistir en JSONL (append-only)
    entry = asdict(review)
    entry["status"] = status.value  # guardar como string, no Enum

    with REVIEWS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return review


# ── LECTURA ───────────────────────────────────────────────────────────────────
def read_reviews(n: int = 50) -> list[dict]:
    """Retorna las últimas n revisiones, más recientes primero."""
    if not REVIEWS_LOG.exists():
        return []

    entries = []
    with REVIEWS_LOG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    return list(reversed(entries[-n:]))


def get_review_stats(n: int = 200) -> ReviewSummary:
    """Calcula estadísticas del log de revisiones (últimas n)."""
    entries = read_reviews(n)

    total     = len(entries)
    aprobadas = sum(1 for e in entries if e.get("status") == "APROBAR")
    observadas= sum(1 for e in entries if e.get("status") == "OBSERVAR")
    rechazadas= sum(1 for e in entries if e.get("status") == "RECHAZAR")
    revisores = sorted(set(e.get("reviewer", "") for e in entries if e.get("reviewer")))

    tasa_aprobacion = round(100 * aprobadas / total, 1) if total else 0.0
    tasa_rechazo    = round(100 * rechazadas / total, 1) if total else 0.0

    return ReviewSummary(
        total           = total,
        aprobadas       = aprobadas,
        observadas      = observadas,
        rechazadas      = rechazadas,
        tasa_aprobacion = tasa_aprobacion,
        tasa_rechazo    = tasa_rechazo,
        revisores       = revisores,
        ultimas_n       = n,
    )


def get_pending_decisions(n_decisions: int = 50) -> list[dict]:
    """
    Retorna decisiones de Sentinel que NO tienen revisión humana asociada.

    Implementación: lee decisions.jsonl y filtra fuera los decision_ts ya revisados.
    """
    from sentinel.decision_log import read_recent

    decisions = read_recent(n_decisions)
    reviewed_ts = {e.get("decision_ts") for e in read_reviews(n=500)}

    pending = [
        d for d in decisions
        if d.get("timestamp") not in reviewed_ts
    ]
    return pending


# ── LOOKUP: ¿tiene revisión? ──────────────────────────────────────────────────
def get_review_for_decision(decision_ts: str) -> Optional[dict]:
    """
    Busca la revisión más reciente para una decisión dada por su timestamp.
    Retorna None si no existe.
    """
    if not REVIEWS_LOG.exists():
        return None

    last_match = None
    with REVIEWS_LOG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("decision_ts") == decision_ts:
                    last_match = entry
            except json.JSONDecodeError:
                continue

    return last_match


# ── FORMATO CONSOLA ───────────────────────────────────────────────────────────
def format_review(review: HumanReview) -> str:
    """Formato de salida de una revisión para consola."""
    icon = {
        ReviewStatus.APROBAR:  "✅",
        ReviewStatus.OBSERVAR: "⚠️",
        ReviewStatus.RECHAZAR: "❌",
    }.get(review.status, "•")

    lines = [
        "─" * 60,
        f"  Revisión Humana  {icon} {review.status.value}",
        "─" * 60,
        f"  ID revisión : {review.review_id}",
        f"  Decisión ref: {review.decision_ts}",
        f"  Revisor     : {review.reviewer}",
        f"  Pregunta    : {review.pregunta[:80]}{'...' if len(review.pregunta) > 80 else ''}",
        f"  Comentario  : {review.comment or '(sin comentario)'}",
        f"  Timestamp   : {review.review_ts}",
        f"  Versiones   : SENTINEL={review.sentinel_version} · GR={review.guardrail_version}",
        "─" * 60,
    ]
    return "\n".join(lines)


def format_summary(s: ReviewSummary) -> str:
    """Formato de resumen estadístico."""
    lines = [
        "═" * 60,
        "  SENTINEL · Revisiones Humanas — Resumen",
        "═" * 60,
        f"  Total revisadas    : {s.total}",
        f"  Aprobadas ✅       : {s.aprobadas}  ({s.tasa_aprobacion}%)",
        f"  Observadas ⚠️      : {s.observadas}",
        f"  Rechazadas ❌      : {s.rechazadas}  ({s.tasa_rechazo}%)",
        f"  Revisores activos  : {', '.join(s.revisores) or '(ninguno)'}",
        f"  Últimas N analizadas: {s.ultimas_n}",
        "═" * 60,
    ]
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    if "--stats" in args:
        s = get_review_stats()
        print(format_summary(s))
        sys.exit(0)

    if "--pending" in args:
        pending = get_pending_decisions()
        if not pending:
            print("✅ No hay decisiones pendientes de revisión.")
        else:
            print(f"\n⏳ Decisiones sin revisión humana ({len(pending)}):\n")
            for d in pending[:10]:
                ts  = d.get("timestamp", "?")
                prg = d.get("pregunta", "")[:70]
                gst = d.get("guardrail_estado", "?")
                print(f"  [{ts}] {gst} — {prg}")
        sys.exit(0)

    if "--recent" in args:
        try:
            n = int(args[args.index("--recent") + 1])
        except (ValueError, IndexError):
            n = 10
        reviews = read_reviews(n)
        if not reviews:
            print("📭 Sin revisiones registradas aún.")
        else:
            for r in reviews:
                icon = {"APROBAR": "✅", "OBSERVAR": "⚠️", "RECHAZAR": "❌"}.get(r.get("status", ""), "•")
                ts   = r.get("review_ts", "?")
                rev  = r.get("reviewer", "?")
                prg  = r.get("pregunta", "")[:60]
                cmt  = r.get("comment", "")[:60]
                print(f"  {icon} [{ts}] {rev} → {prg}")
                if cmt:
                    print(f"     └─ {cmt}")
        sys.exit(0)

    # Demo: crear una revisión de prueba
    if "--demo" in args:
        print("\n── Demo: submit_review() ──")
        rev = submit_review(
            decision_ts = "2026-05-17T12:00:00",
            pregunta    = "¿Por qué D3 ejecución presupuestaria está en rojo?",
            status      = ReviewStatus.OBSERVAR,
            reviewer    = "Analista-TGI-01",
            comment     = "La fuente es correcta pero el contexto de la brecha 2023 no se refleja en el chunk.",
        )
        print(format_review(rev))
        print(f"\n✅ Revisión guardada en: {REVIEWS_LOG}")
        sys.exit(0)

    print("""
SENTINEL · Human Review CLI
Uso:
  python -m sentinel.human_review --stats          # Resumen estadístico
  python -m sentinel.human_review --pending        # Decisiones sin revisión
  python -m sentinel.human_review --recent 10      # Últimas 10 revisiones
  python -m sentinel.human_review --demo           # Crear revisión de prueba
""")
