"""
SENTINEL RAG · decision_log.py — Sprint 1.6
Log auditado de decisiones — trazabilidad institucional completa.

Cada consulta a Sentinel deja registro permanente y auditable.
Formato: append-only JSONL (una línea JSON por decisión).
Ruta:    sentinel/logs/decisions.jsonl

¿Por qué importa?
Cuando un director pregunte "¿por qué Sentinel sugirió esto?",
el log responde con timestamp, fuentes, confianza y estado del guardrail.

Uso:
  from sentinel.decision_log import log_decision, read_recent, get_stats
  entry = log_decision(explain_result, guardrail)

Dylus Lab © 2026
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.explain import ExplainResult
from sentinel.guardrails import GuardrailResult

# ── RUTAS ─────────────────────────────────────────────────────────────────────
LOGS_DIR      = Path(__file__).parent / "logs"
DECISIONS_LOG = LOGS_DIR / "decisions.jsonl"

# Crear directorio si no existe
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ── LOG DE DECISIÓN ───────────────────────────────────────────────────────────
def log_decision(
    r: ExplainResult,
    g: GuardrailResult,
    rol:          str  = "analista",
    llm_activado: bool = False,
    llm_modelo:   str  = "",
) -> dict:
    """
    Registra una decisión de Sentinel en el log auditado (JSONL).

    Cada entrada contiene:
    - Identificación: timestamp, pregunta, rol
    - Estado de decisión: guardrail_estado, puede_responder, puede_recomendar
    - Métricas de recuperación: confianza, score, num_chunks
    - Cobertura: dims_cubiertas, dims_faltantes
    - Trazabilidad: fuentes (notas Obsidian)
    - Vacíos detectados
    """
    entry = {
        # Identificación
        "timestamp":   datetime.now().isoformat(),
        "pregunta":    r.pregunta,
        "rol":         rol,

        # Estado de la decisión (guardrail)
        "guardrail_estado":     g.estado.value,
        "puede_responder":      g.puede_responder,
        "puede_recomendar":     g.puede_recomendar,
        "guardrail_motivos":    g.motivos,
        "nivel_riesgo":         g.nivel_riesgo,

        # LLM
        "llm_activado": llm_activado,
        "llm_modelo":   llm_modelo,

        # Métricas de recuperación
        "confianza_pct":   r.confianza_pct,
        "score_promedio":  r.score_promedio,
        "score_maximo":    r.score_maximo,
        "num_chunks":      len(r.chunks),
        "notas_distintas": r.notas_distintas,
        "tipos_distintos": r.tipos_distintos,

        # Cobertura dimensional
        "dims_cubiertas":     r.dims_cubiertas,
        "dims_faltantes":     r.dims_faltantes,
        "num_dims_cubiertas": len(r.dims_cubiertas),

        # Fuentes (notas Obsidian que sustentaron la respuesta)
        "fuentes": [c.nota for c in r.chunks],

        # Territorios cubiertos
        "territorios": r.territorios,

        # Vacíos detectados
        "vacios": r.vacios,
    }

    # Append al JSONL — operación atómica para thread-safety básica
    with open(DECISIONS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry


# ── LECTURA ───────────────────────────────────────────────────────────────────
def read_recent(n: int = 50) -> list[dict]:
    """Lee las últimas n decisiones del log. Las más recientes al final."""
    if not DECISIONS_LOG.exists():
        return []

    lines = DECISIONS_LOG.read_text(encoding="utf-8").strip().splitlines()
    entries = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            pass  # línea corrupta → ignorar

    return entries[-n:]


def get_stats(n: int = 100) -> dict:
    """
    Estadísticas agregadas de las últimas n decisiones.
    Útil para monitoreo y dashboards de calidad.
    """
    entries = read_recent(n)
    if not entries:
        return {"total": 0, "mensaje": "Sin decisiones registradas aún."}

    total = len(entries)
    confianzas = [e.get("confianza_pct", 0) for e in entries]

    # Distribución de estados guardrail
    estados: dict[str, int] = {}
    for e in entries:
        est = e.get("guardrail_estado", "desconocido")
        estados[est] = estados.get(est, 0) + 1

    # Distribución de roles
    roles: dict[str, int] = {}
    for e in entries:
        rol = e.get("rol", "desconocido")
        roles[rol] = roles.get(rol, 0) + 1

    # Dimensiones más faltantes
    dims_faltantes_count: dict[str, int] = {}
    for e in entries:
        for d in e.get("dims_faltantes", []):
            dims_faltantes_count[d] = dims_faltantes_count.get(d, 0) + 1

    # Notas más consultadas
    notas_count: dict[str, int] = {}
    for e in entries:
        for nota in e.get("fuentes", []):
            notas_count[nota] = notas_count.get(nota, 0) + 1
    top_notas = sorted(notas_count.items(), key=lambda x: -x[1])[:10]

    return {
        "total":              total,
        "confianza_promedio": round(sum(confianzas) / len(confianzas), 1),
        "confianza_maxima":   round(max(confianzas), 1),
        "confianza_minima":   round(min(confianzas), 1),
        "distribucion_estado": estados,
        "distribucion_rol":    roles,
        "dims_mas_faltantes":  dims_faltantes_count,
        "notas_mas_consultadas": [{"nota": n, "consultas": c} for n, c in top_notas],
        "llm_activaciones":    sum(1 for e in entries if e.get("llm_activado")),
        "periodo": {
            "desde": entries[0]["timestamp"]  if entries else None,
            "hasta": entries[-1]["timestamp"] if entries else None,
        },
    }


def clear_log() -> int:
    """
    Limpia el log de decisiones. CUIDADO: operación irreversible.
    Retorna el número de entradas eliminadas.
    """
    if not DECISIONS_LOG.exists():
        return 0
    count = len(read_recent(n=999999))
    DECISIONS_LOG.unlink()
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return count


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Audit log de decisiones Sentinel")
    parser.add_argument("--stats",  action="store_true", help="Mostrar estadísticas")
    parser.add_argument("--recent", type=int, default=10, help="Últimas N decisiones")
    args = parser.parse_args()

    if args.stats:
        stats = get_stats(100)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        entries = read_recent(args.recent)
        if not entries:
            print("  Sin decisiones registradas aún.")
        else:
            print(f"\n  Últimas {len(entries)} decisiones:\n")
            for e in entries:
                icon = "🟢" if e["guardrail_estado"] == "OK" else (
                       "🟡" if e["guardrail_estado"] in ("ADVERTENCIA", "INFORMACIÓN INSUFICIENTE")
                       else "🔴")
                ts   = e["timestamp"][:16].replace("T", " ")
                conf = e.get("confianza_pct", 0)
                rol  = e.get("rol", "?")
                print(f"  {icon} {ts}  {conf:>5.0f}%  [{rol:>9}]  {e['pregunta'][:60]}")
