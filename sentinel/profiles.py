"""
SENTINEL RAG · profiles.py — Sprint 1.6
Perfiles de usuario — adapta la respuesta de Sentinel según el rol institucional.

  ROL_ANALISTA:   chunks + scores + similitudes + dims (técnico completo)
  ROL_DIRECTIVO:  síntesis + semáforo de riesgo + recomendación ejecutiva
  ROL_POLITICO:   narrativa + impacto territorial + alineación al mandato

Diseño para crecer:
  - Los perfiles son metadata y formato hoy.
  - Los prompts LLM diferenciados por rol vienen en Sprint 2.
  - Los umbrales de alerta por rol pueden personalizarse por GAD.

Regla de oro: cada rol ve MENOS información técnica, pero MÁS contexto institucional.

Dylus Lab © 2026
"""
from __future__ import annotations
import sys

sys.stdout.reconfigure(encoding="utf-8")

from sentinel.explain import ExplainResult
from sentinel.guardrails import GuardrailResult, Estado

# ── CONSTANTES DE ROL ─────────────────────────────────────────────────────────
ROL_ANALISTA  = "analista"
ROL_DIRECTIVO = "directivo"
ROL_POLITICO  = "politico"

ROLES_VALIDOS = {ROL_ANALISTA, ROL_DIRECTIVO, ROL_POLITICO}

ROL_DESCRIPCION = {
    ROL_ANALISTA: (
        "Analista Técnico — acceso completo a chunks, scores y cobertura dimensional. "
        "Ve todo lo que Sentinel recuperó y cómo lo evaluó."
    ),
    ROL_DIRECTIVO: (
        "Directivo — síntesis ejecutiva con semáforo de riesgo y recomendación de acción. "
        "Sin tecnicismos, con impacto institucional claro."
    ),
    ROL_POLITICO: (
        "Autoridad Política — narrativa territorial con impacto ciudadano y alineación al mandato. "
        "Enfocado en decisión pública, no en datos técnicos."
    ),
}

# Dimensiones TGI críticas para alertas ejecutivas
DIMS_CRITICAS_DIRECTIVO = {"D3", "D4"}   # Ejecución y Equidad — más sensibles políticamente
DIMS_CRITICAS_POLITICO  = {"D4"}         # Equidad territorial — impacto ciudadano directo


# ── FUNCIÓN PRINCIPAL ─────────────────────────────────────────────────────────
def format_for_role(
    r:                        ExplainResult,
    g:                        GuardrailResult,
    rol:                      str = ROL_ANALISTA,
    llm_respuesta:            str = "",
    llm_activado:             bool = False,
) -> dict:
    """
    Adapta la respuesta de Sentinel al perfil del usuario.

    Args:
        r:             ExplainResult con toda la trazabilidad
        g:             GuardrailResult con el veredicto institucional
        rol:           "analista" | "directivo" | "politico"
        llm_respuesta: texto generado por LLM (vacío en Sprint 1.x)
        llm_activado:  True cuando Claude está conectado

    Returns:
        dict con los campos que el frontend debe mostrar para el rol dado
    """
    if rol not in ROLES_VALIDOS:
        rol = ROL_ANALISTA  # fallback seguro: siempre mostrar info técnica

    # Base común a todos los roles
    base = {
        "rol":                rol,
        "pregunta":           r.pregunta,
        "guardrail_estado":   g.estado.value,
        "nivel_riesgo":       g.nivel_riesgo,
        "puede_responder":    g.puede_responder,
        "puede_recomendar":   g.puede_recomendar,
        "accion_sentinel":    g.accion_sugerida,
        "confianza_pct":      r.confianza_pct,
        "nivel_confianza":    r.nivel_confianza,
        "dims_cubiertas":     r.dims_cubiertas,
        "dims_faltantes":     r.dims_faltantes,
        "territorios":        r.territorios,
        "vacios":             r.vacios,
        "llm_activado":       llm_activado,
    }

    if rol == ROL_ANALISTA:
        return _format_analista(r, g, base, llm_respuesta)
    elif rol == ROL_DIRECTIVO:
        return _format_directivo(r, g, base, llm_respuesta)
    else:  # ROL_POLITICO
        return _format_politico(r, g, base, llm_respuesta)


# ── ROL ANALISTA ──────────────────────────────────────────────────────────────
def _format_analista(
    r: ExplainResult, g: GuardrailResult, base: dict, llm_respuesta: str
) -> dict:
    """
    ROL_ANALISTA: Acceso completo a toda la información técnica.
    Ve chunks individuales, scores de similitud, cobertura dimensional y reglas.
    Diseñado para el equipo técnico de Dylus Lab y analistas del GAD.
    """
    return {
        **base,
        "vista": "técnica",

        # Chunks completos con todos los metadatos
        "chunks": [
            {
                "nota":      c.nota,
                "section":   c.section,
                "tipo_nota": c.tipo_nota,
                "dimension": c.dimension,
                "carpeta":   c.carpeta,
                "score":     c.score,
                "preview":   c.text[:400],
            }
            for c in r.chunks
        ],

        # Cobertura dimensional detallada
        "cobertura_dims": {
            dim_id: {
                "nombre":   cov.nombre,
                "cubierta": cov.cubierta,
                "score":    cov.score,
                "fuentes":  cov.fuentes,
            }
            for dim_id, cov in r.cobertura_dims.items()
        },

        # Métricas de recuperación completas
        "metricas": {
            "score_promedio":   r.score_promedio,
            "score_maximo":     r.score_maximo,
            "score_minimo":     r.score_minimo,
            "notas_distintas":  r.notas_distintas,
            "tipos_distintos":  r.tipos_distintos,
        },

        # Las 3 reglas institucionales
        "reglas": {
            "fuente":    r.regla_fuente,
            "confianza": r.regla_confianza,
            "cobertura": r.regla_cobertura,
        },

        # Guardrail completo
        "guardrail_motivos": g.motivos,

        # Respuesta LLM (si está activo)
        "llm_respuesta": llm_respuesta,
    }


# ── ROL DIRECTIVO ─────────────────────────────────────────────────────────────
def _semaforo_riesgo(r: ExplainResult, g: GuardrailResult) -> str:
    """Semáforo ejecutivo de riesgo institucional para directivos."""
    if g.estado == Estado.RECHAZAR:
        return "🔴 Riesgo Alto — información insuficiente para decidir"
    if g.estado == Estado.INSUFICIENTE:
        return "🟡 Riesgo Medio — cobertura parcial, revisar antes de actuar"
    if g.estado == Estado.ADVERTENCIA:
        return "🟡 Riesgo Medio — respuesta con cobertura dimensional incompleta"
    # Estado OK
    if r.confianza_pct >= 75:
        return "🟢 Confianza Alta — respuesta verificada y trazable"
    return "🟡 Confianza Media — respuesta válida con caveats menores"


def _format_directivo(
    r: ExplainResult, g: GuardrailResult, base: dict, llm_respuesta: str
) -> dict:
    """
    ROL_DIRECTIVO: Síntesis ejecutiva.
    Ve semáforo de riesgo, fuentes clave y recomendación de acción.
    Sin scores ni chunks individuales — solo lo que importa para decidir.
    """
    # Top 3 fuentes clave (por score)
    fuentes_ordenadas = sorted(r.chunks, key=lambda c: -c.score)
    fuentes_clave = list({c.nota: c for c in fuentes_ordenadas}.keys())[:3]

    # Alertas ejecutivas — dimensiones críticas faltantes
    alertas: list[str] = []
    for dim in DIMS_CRITICAS_DIRECTIVO:
        if dim in r.dims_faltantes:
            nombre = r.cobertura_dims[dim].nombre
            alertas.append(
                f"Sin cobertura en {dim} ({nombre}) — "
                f"la recomendación no incluye análisis de {nombre.lower()}."
            )
    if g.motivos:
        alertas.extend(g.motivos[:2])

    return {
        **base,
        "vista": "ejecutiva",

        # Semáforo principal
        "semaforo_riesgo":  _semaforo_riesgo(r, g),

        # Fuentes sin scores — solo nombres institucionales
        "fuentes_clave":    fuentes_clave,
        "num_fuentes":      r.notas_distintas,

        # Alertas ejecutivas
        "alertas_ejecutivas":      alertas,
        "dims_criticas_faltantes": [d for d in r.dims_faltantes if d in DIMS_CRITICAS_DIRECTIVO],

        # Sin chunks ni scores individuales
        # La síntesis viene del LLM en Sprint 2
        "llm_respuesta": llm_respuesta if llm_respuesta else (
            "ℹ️  Síntesis automática disponible al activar el módulo LLM (Sprint 2). "
            "Por ahora consultar las fuentes indicadas."
        ),
    }


# ── ROL POLÍTICO ──────────────────────────────────────────────────────────────
def _format_politico(
    r: ExplainResult, g: GuardrailResult, base: dict, llm_respuesta: str
) -> dict:
    """
    ROL_POLITICO: Narrativa territorial + impacto ciudadano.
    Sin tecnicismos. Enfocado en mandato, equidad y decisión pública.
    Diseñado para el Alcalde, Concejales y Asesores Políticos.
    """
    # Alineación al mandato 2023-2027
    # D2 (Planificación) + D3 (Ejecución) = ejes del mandato
    mandato_cubierto = "D2" in r.dims_cubiertas and "D3" in r.dims_cubiertas

    # Cobertura de equidad territorial (D4 = lo más sensible políticamente)
    equidad_cubierta = "D4" in r.dims_cubiertas

    # Narrativa de riesgo (sin números)
    if g.estado == Estado.RECHAZAR:
        narrativa_riesgo = (
            "No se encontró información suficiente en la base de conocimiento. "
            "Se requiere cargar documentos adicionales para emitir criterio."
        )
    elif g.estado in (Estado.INSUFICIENTE, Estado.ADVERTENCIA):
        motivo_simple = g.motivos[0] if g.motivos else "datos incompletos"
        narrativa_riesgo = (
            f"La información disponible es parcial ({motivo_simple}). "
            "El criterio debe tomarse con precaución."
        )
    else:
        narrativa_riesgo = (
            "La base de conocimiento tiene información suficiente y verificada "
            "para sustentar una decisión sobre este tema."
        )

    # Impacto territorial (con lenguaje ciudadano)
    parroquias_afectadas = [t for t in r.territorios if t != "Cantonal"]
    impacto = {
        "nivel_cantonal":         "Cantonal" in r.territorios,
        "parroquias_afectadas":   parroquias_afectadas,
        "num_parroquias":         len(parroquias_afectadas),
        "territorio_descripcion": (
            f"Afecta {len(parroquias_afectadas)} parroquia(s): {', '.join(parroquias_afectadas)}"
            if parroquias_afectadas
            else "Ámbito cantonal general"
        ),
    }

    return {
        **base,
        "vista": "narrativa",

        # Narrativa principal (sin tecnicismos)
        "narrativa_riesgo":    narrativa_riesgo,

        # Alineación al mandato
        "alineacion_mandato":  mandato_cubierto,
        "cobertura_equidad":   equidad_cubierta,

        # Impacto territorial
        "impacto_territorial": impacto,

        # Sin chunks, sin scores, sin dimensiones técnicas
        # La narrativa política viene del LLM en Sprint 2
        "llm_respuesta": llm_respuesta if llm_respuesta else (
            "ℹ️  Análisis narrativo automatizado disponible al activar el módulo de inteligencia (Sprint 2)."
        ),
    }
