"""
SENTINEL RAG · guardrails.py — Sprint 1.6
Política de fallback institucional — capa de seguridad antes de producción.

Evita "alucinaciones institucionales" aplicando 3 guardrails sobre ExplainResult:
  G1. chunks < 2          → RECHAZAR (respuesta imposible)
  G2. confianza < 40%     → RECHAZAR (señal demasiado débil)
  G3. confianza < 60%     → INFORMACIÓN INSUFICIENTE (puede mostrar, no recomendar)
  G4. dims_cubiertas < 2  → ADVERTENCIA (con cobertura parcial explícita)
  G5. Todo OK             → OK (responder y recomendar con trazabilidad)

Salida esperada cuando falla:
  Estado:          INFORMACIÓN INSUFICIENTE
  Motivo:          cobertura territorial incompleta
  Acción sugerida: cargar POA o PAC actualizado

Uso:
  from sentinel.guardrails import apply_guardrails
  result = apply_guardrails(explain_result)

Dylus Lab © 2026
"""
from __future__ import annotations
import sys
from dataclasses import dataclass, field
from enum import Enum

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.explain import ExplainResult

# ── UMBRALES DE PRODUCCIÓN ────────────────────────────────────────────────────
# Más estrictos que explain.py (que usa 25% y 40% para validación interna)
GUARDRAIL_CHUNKS_MIN      = 2      # menos de 2 chunks → RECHAZAR
GUARDRAIL_CONFIANZA_BAJA  = 40.0   # < 40% → RECHAZAR
GUARDRAIL_CONFIANZA_MEDIA = 60.0   # 40-60% → INSUFICIENTE (sin recomendación)
GUARDRAIL_DIMS_MIN        = 2      # < 2 dims → ADVERTENCIA con caveat


# ── ESTADOS ───────────────────────────────────────────────────────────────────
class Estado(str, Enum):
    OK           = "OK"
    ADVERTENCIA  = "ADVERTENCIA"
    INSUFICIENTE = "INFORMACIÓN INSUFICIENTE"
    RECHAZAR     = "RECHAZAR"


# ── RESULTADO ─────────────────────────────────────────────────────────────────
@dataclass
class GuardrailResult:
    estado:            Estado
    puede_responder:   bool
    puede_recomendar:  bool
    motivos:           list[str]   # razones específicas del estado
    accion_sugerida:   str         # qué debe hacer el operador / sistema
    nivel_riesgo:      str         # "🟢 Ninguno" | "🟡 Medio" | "🔴 Alto"


# ── APLICACIÓN DE GUARDRAILS ──────────────────────────────────────────────────
def apply_guardrails(r: ExplainResult) -> GuardrailResult:
    """
    Aplica política institucional de seguridad sobre ExplainResult.

    La lógica es lineal — el primer guardrail que dispara define el estado.
    Los guardrails posteriores son más permisivos (por eso el orden importa).
    """
    motivos: list[str] = []

    # ── G1: Chunks insuficientes → rechazo absoluto ───────────────────────────
    if len(r.chunks) < GUARDRAIL_CHUNKS_MIN:
        motivos.append(
            f"solo {len(r.chunks)} chunk(s) recuperados "
            f"(mínimo institucional: {GUARDRAIL_CHUNKS_MIN})"
        )
        return GuardrailResult(
            estado           = Estado.RECHAZAR,
            puede_responder  = False,
            puede_recomendar = False,
            motivos          = motivos,
            accion_sugerida  = (
                "Reformular la pregunta con términos más específicos, "
                "o cargar más notas relacionadas al tema en el Obsidian KB."
            ),
            nivel_riesgo     = "🔴 Alto",
        )

    # ── G2: Confianza muy baja → rechazo ─────────────────────────────────────
    if r.confianza_pct < GUARDRAIL_CONFIANZA_BAJA:
        motivos.append(
            f"confianza {r.confianza_pct:.0f}% < umbral mínimo "
            f"({GUARDRAIL_CONFIANZA_BAJA:.0f}%) — señal semántica insuficiente"
        )
        return GuardrailResult(
            estado           = Estado.RECHAZAR,
            puede_responder  = False,
            puede_recomendar = False,
            motivos          = motivos,
            accion_sugerida  = (
                "La pregunta no tiene cobertura semántica en el Knowledge Base. "
                "Verificar terminología institucional o enriquecer el vault con "
                "notas relacionadas al tema."
            ),
            nivel_riesgo     = "🔴 Alto",
        )

    # ── G3: Confianza media → puede mostrar fuentes, NO recomendar ────────────
    if r.confianza_pct < GUARDRAIL_CONFIANZA_MEDIA:
        motivos.append(
            f"confianza {r.confianza_pct:.0f}% no alcanza umbral de recomendación "
            f"({GUARDRAIL_CONFIANZA_MEDIA:.0f}%)"
        )
        if r.dims_faltantes:
            dims_str = ", ".join(
                f"{d} ({r.cobertura_dims[d].nombre})" for d in r.dims_faltantes
            )
            motivos.append(f"dimensiones sin cobertura: {dims_str}")
        return GuardrailResult(
            estado           = Estado.INSUFICIENTE,
            puede_responder  = True,   # puede mostrar fuentes
            puede_recomendar = False,  # NO puede emitir recomendación institucional
            motivos          = motivos,
            accion_sugerida  = (
                "Sentinel puede mostrar las fuentes encontradas pero no emitir "
                "recomendación institucional. Considerar cargar POA, PAC o "
                "informes sectoriales actualizados para enriquecer el contexto."
            ),
            nivel_riesgo     = "🟡 Medio",
        )

    # ── G4: Confianza OK pero cobertura dimensional baja → advertencia ────────
    if len(r.dims_cubiertas) < GUARDRAIL_DIMS_MIN:
        dims_faltantes_str = ", ".join(
            f"{d}={r.cobertura_dims[d].nombre}" for d in r.dims_faltantes
        )
        motivos.append(
            f"solo {len(r.dims_cubiertas)} dimensión(es) TGI cubiertas "
            f"(mínimo: {GUARDRAIL_DIMS_MIN})"
        )
        motivos.append(f"sin cobertura en: {dims_faltantes_str}")
        return GuardrailResult(
            estado           = Estado.ADVERTENCIA,
            puede_responder  = True,
            puede_recomendar = True,   # puede recomendar, pero con caveat obligatorio
            motivos          = motivos,
            accion_sugerida  = (
                "Respuesta parcial — citar explícitamente las dimensiones sin "
                "cobertura al presentar la recomendación. Marcar como análisis "
                "sectorial, no cantonal."
            ),
            nivel_riesgo     = "🟡 Medio",
        )

    # ── G5: Todo OK ───────────────────────────────────────────────────────────
    return GuardrailResult(
        estado           = Estado.OK,
        puede_responder  = True,
        puede_recomendar = True,
        motivos          = [],
        accion_sugerida  = (
            "Sentinel puede responder y recomendar con trazabilidad completa. "
            "Citar todas las fuentes recuperadas."
        ),
        nivel_riesgo     = "🟢 Ninguno",
    )


# ── FORMATEO ──────────────────────────────────────────────────────────────────
_ICON_MAP = {
    Estado.OK:           "🟢",
    Estado.ADVERTENCIA:  "🟡",
    Estado.INSUFICIENTE: "🟡",
    Estado.RECHAZAR:     "🔴",
}


def format_guardrail(g: GuardrailResult) -> str:
    """Formatea GuardrailResult para display en consola / log."""
    sep  = "─" * 64
    icon = _ICON_MAP.get(g.estado, "❓")

    lines = [
        sep,
        f"  GUARDRAIL  {icon} {g.estado.value}",
        f"  Riesgo institucional: {g.nivel_riesgo}",
    ]

    if g.motivos:
        lines.append("  Motivos:")
        for m in g.motivos:
            lines.append(f"    ⚠️  {m}")

    lines.append(f"  Acción sugerida:   {g.accion_sugerida}")
    lines.append(f"  Puede responder:   {'✅' if g.puede_responder  else '❌'}")
    lines.append(f"  Puede recomendar:  {'✅' if g.puede_recomendar else '❌'}")
    lines.append(sep)

    return "\n".join(lines)


def to_dict(g: GuardrailResult) -> dict:
    """JSON-serializable para API / logs."""
    return {
        "estado":           g.estado.value,
        "puede_responder":  g.puede_responder,
        "puede_recomendar": g.puede_recomendar,
        "motivos":          g.motivos,
        "accion_sugerida":  g.accion_sugerida,
        "nivel_riesgo":     g.nivel_riesgo,
    }


# ── CLI DE PRUEBA ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from sentinel.explain import explain_retrieval, format_explain

    pregunta = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "¿Cuál es el TGI score de Montecristi?"
    )

    r = explain_retrieval(pregunta)
    g = apply_guardrails(r)

    print(format_explain(r))
    print(format_guardrail(g))
