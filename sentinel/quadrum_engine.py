"""
SENTINEL · quadrum_engine.py
Motor de Coherencia Institucional QUADRUM — Sprint 6.
Evalúa la coherencia entre las 4 capas doctrinales de QUIRA OS:
  ENTENDER → GOBERNAR → SIMULAR → CONFIAR
Pregunta central: ¿Todo esto es coherente entre sí?
Doctrina: "La IA opera. La autoridad pública decide." — QUADRUM valida antes de recomendar.
Dylus Lab © 2026
"""
from __future__ import annotations
import unicodedata

# ── UMBRALES DOCTRINALES ───────────────────────────────────────────────────────
_UMBRAL_DATOS_CRITICOS = 50.0    # NBI / TPS por encima = emergencia territorial
_UMBRAL_INVERSION_MIN  = 60      # $/hab mínimo aceptable para no alertar inequidad
_UMBRAL_ICGIT_META     = 70.0    # meta mandato AVEP
_UMBRAL_ICGIT_CRITICO  = 50.0    # por debajo = Transición Crítica grave
_UMBRAL_TRUST_MIN      = 65      # score mínimo para recomendar sin advertencia


def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


# ── EVALUADORES POR CAPA ───────────────────────────────────────────────────────

def _eval_entender(data: dict, territory: str | None) -> dict:
    """
    ENTENDER — ¿Qué está pasando?
    Evalúa si los datos disponibles permiten un diagnóstico territorial confiable.
    """
    parroquias = data.get("parroquias", [])
    icgit      = data.get("icgit", {})
    sat        = data.get("sat", [])
    alertas    = [s for s in sat if s.get("nivel") == "CRÍTICO"]

    score    = 100
    issues   = []
    findings = []

    # ¿Hay datos de la parroquia objetivo?
    if territory:
        q  = _norm(territory)
        par = next((p for p in parroquias if _norm(p["nombre"]) in q or q in _norm(p["nombre"])), None)
        if par:
            findings.append(f"Datos disponibles para {par['nombre']}: NBI={par['nbi']}% · agua={par['agua']}%")
            if par["nbi"] >= _UMBRAL_DATOS_CRITICOS:
                issues.append(f"⚠️ {par['nombre']} en zona crítica NBI ({par['nbi']}%)")
                score -= 10
            if par["per_capita"] < _UMBRAL_INVERSION_MIN:
                issues.append(f"⚠️ Inversión insuficiente: ${par['per_capita']}/hab")
                score -= 8
        else:
            issues.append("Datos territoriales específicos no disponibles en H99")
            score -= 15

    # ¿SATs críticas activas?
    if alertas:
        issues.append(f"{len(alertas)} alerta(s) SAT crítica(s) activa(s)")
        score -= len(alertas) * 5

    # ¿ICGI-T en zona crítica?
    icgit_score = icgit.get("score", 53.56)
    if icgit_score < _UMBRAL_ICGIT_CRITICO:
        issues.append(f"ICGI-T Q1={icgit_score:.2f} — zona Transición Crítica")
        score -= 10

    findings.append(f"ICGI-T Global: {icgit_score:.2f} · Proyección 2026: {icgit.get('proyeccion', 65.77):.2f}")

    return {
        "capa":     "ENTENDER",
        "pregunta": "¿Qué está pasando?",
        "score":    max(30, score),
        "issues":   issues,
        "findings": findings,
        "estado":   "OK" if score >= 80 else "ALERTA" if score >= 60 else "CRÍTICO",
    }


def _eval_gobernar(data: dict, query: str) -> dict:
    """
    GOBERNAR — ¿Qué meta toca?
    Verifica si la decisión está alineada con el PDOT, POA y competencias legales.
    """
    q      = _norm(query)
    score  = 100
    issues = []
    findings = []

    # ¿Hay referencia a meta PDOT?
    pdot_terms = ["pdot", "meta", "planificacion", "2027", "objetivo"]
    if any(t in q for t in pdot_terms):
        findings.append("Consulta toca metas PDOT 2023-2027")
    else:
        issues.append("Sin referencia explícita a metas PDOT — verificar alineación")
        score -= 8

    # ¿Hay SATs que bloquean la decisión?
    sat = data.get("sat", [])
    criticas = [s for s in sat if s.get("nivel") == "CRÍTICO"]
    if criticas:
        for s in criticas[:2]:
            issues.append(f"SAT activa: {s['id']} — {s['nombre']}")
        score -= len(criticas) * 6

    # ¿Índices de gobernanza en ruptura?
    indices = data.get("indices", {})
    ruptura = {k: v for k, v in indices.items()
               if v.get("valor") is not None and v["valor"] < 30}
    if ruptura:
        nombres = ", ".join(f"{k}={v['valor']:.1f}" for k, v in ruptura.items())
        issues.append(f"Índices en Ruptura Sistémica: {nombres}")
        score -= len(ruptura) * 5

    iet = indices.get("IET", {}).get("valor", 44.80)
    findings.append(f"IET={iet:.2f} — Equidad Territorial ({('OK' if iet >= 50 else 'Transición Crítica')})")

    return {
        "capa":     "GOBERNAR",
        "pregunta": "¿Qué meta toca?",
        "score":    max(30, score),
        "issues":   issues,
        "findings": findings,
        "estado":   "OK" if score >= 80 else "ALERTA" if score >= 60 else "CRÍTICO",
    }


def _eval_simular(sim_result: dict | None) -> dict:
    """
    SIMULAR — ¿Qué pasa si actuamos?
    Verifica si existe modelo de simulación disponible y su confianza.
    """
    score  = 100
    issues = []
    findings = []

    if sim_result is None:
        issues.append("No hay simulación activa para esta consulta")
        score -= 30
        return {
            "capa":     "SIMULAR",
            "pregunta": "¿Qué pasa si actuamos?",
            "score":    score,
            "issues":   issues,
            "findings": ["Sin modelo de simulación — análisis solo descriptivo"],
            "estado":   "PENDIENTE",
        }

    conf = sim_result.get("confidence", 0)
    pol  = sim_result.get("policy_label", "")
    ter  = sim_result.get("territorio", "")
    d    = sim_result.get("delta_pct", 0)

    findings.append(f"Simulación activa: {pol} +{d}% en {ter}")
    findings.append(f"Confianza CBST v0.1: {conf}% ({sim_result.get('confidence_label','')})")

    if conf < _UMBRAL_TRUST_MIN:
        issues.append(f"Confianza del modelo ({conf}%) por debajo del umbral mínimo ({_UMBRAL_TRUST_MIN}%)")
        score -= 20

    # Delta muy agresivo
    if d > 40:
        issues.append(f"Delta de +{d}% es agresivo — revisar viabilidad presupuestaria")
        score -= 10

    icgit_d = sim_result.get("proyectado", {}).get("icgit_delta", 0)
    findings.append(f"Impacto proyectado ICGI-T cantonal: {icgit_d:+.3f} pts")

    return {
        "capa":     "SIMULAR",
        "pregunta": "¿Qué pasa si actuamos?",
        "score":    max(30, score),
        "issues":   issues,
        "findings": findings,
        "estado":   "OK" if score >= 80 else "ALERTA" if score >= 60 else "CRÍTICO",
    }


def _eval_confiar(trust_result: dict | None, legal_refs: list) -> dict:
    """
    CONFIAR — ¿Qué tan sólido es el dato?
    Consolida el trust score y verifica respaldo legal.
    """
    score  = 100
    issues = []
    findings = []

    if trust_result:
        ts = trust_result.get("score", 80)
        findings.append(
            f"Governance Confidence Index: {ts}% ({trust_result.get('label','')})"
        )
        desglose = trust_result.get("desglose", {})
        findings.append(
            f"Integridad {desglose.get('Integridad',0)}% · "
            f"Disponibilidad {desglose.get('Disponibilidad',0)}% · "
            f"Trazabilidad {desglose.get('Trazabilidad',0)}% · "
            f"Cumplimiento {desglose.get('Cumplimiento',0)}%"
        )
        if ts < _UMBRAL_TRUST_MIN:
            issues.append(f"Trust Score ({ts}%) insuficiente — revisar fuentes")
            score -= 20
    else:
        issues.append("Trust Score no calculado para esta respuesta")
        score -= 15

    if legal_refs:
        findings.append(f"{len(legal_refs)} referencia(s) legal(es) activa(s): " +
                         " · ".join(f"{r['law']} {r['article']}" for r in legal_refs))
        score += min(10, len(legal_refs) * 4)  # bonus por respaldo legal
    else:
        issues.append("Sin referencia legal activa — recomendación no fundamentada normativamente")
        score -= 12

    return {
        "capa":     "CONFIAR",
        "pregunta": "¿Qué tan sólido es el dato?",
        "score":    max(30, min(100, score)),
        "issues":   issues,
        "findings": findings,
        "estado":   "OK" if score >= 80 else "ALERTA" if score >= 60 else "CRÍTICO",
    }


# ── MOTOR CENTRAL ─────────────────────────────────────────────────────────────

def evaluate(
    query:        str,
    data:         dict,
    sim_result:   dict | None = None,
    trust_result: dict | None = None,
    legal_refs:   list        = None,
    territory:    str | None  = None,
) -> dict:
    """
    Evaluación QUADRUM completa — las 4 capas + coherencia cruzada.

    Args:
        query:        pregunta del usuario
        data:         load_all() — datos institucionales completos
        sim_result:   dict de simulate_policy() o None
        trust_result: dict de trust_engine.calculate_trust() o None
        legal_refs:   lista de chunks de legal_router.find_legal_refs() o []
        territory:    parroquia activa si la hay

    Returns:
        dict con evaluación por capa + coherencia global + recomendaciones
    """
    if legal_refs is None:
        legal_refs = []

    capas = [
        _eval_entender(data, territory),
        _eval_gobernar(data, query),
        _eval_simular(sim_result),
        _eval_confiar(trust_result, legal_refs),
    ]

    # ── Coherencia global ──────────────────────────────────────────────────────
    scores     = [c["score"] for c in capas]
    global_avg = sum(scores) / len(scores)
    all_issues = [i for c in capas for i in c["issues"]]
    criticos   = [c for c in capas if c["estado"] == "CRÍTICO"]

    # Calcular coherencia: penalizar si hay capas muy dispares
    dispersion = max(scores) - min(scores)
    coherencia = max(50, global_avg - (dispersion * 0.15))

    if criticos:
        coherencia -= len(criticos) * 8

    coherencia = round(min(99, max(30, coherencia)))

    coh_label = (
        "Alta coherencia"     if coherencia >= 80 else
        "Coherencia moderada" if coherencia >= 65 else
        "Coherencia baja — revisar antes de decidir"
    )

    # ── Recomendación ejecutiva ────────────────────────────────────────────────
    recomendaciones = []
    if criticos:
        recomendaciones.append(
            f"⚠️ {len(criticos)} capa(s) en estado CRÍTICO — no recomendar acción sin revisión."
        )
    if all_issues:
        recomendaciones.append(
            f"Resolver {len(all_issues)} observación(es) antes de elevar al Concejo."
        )
    if not legal_refs:
        recomendaciones.append(
            "Agregar fundamento normativo (COOTAD/COPLAFIP) a la recomendación."
        )
    if sim_result and sim_result.get("confidence", 0) < 75:
        recomendaciones.append(
            "Validar proyección de simulación con equipo técnico antes de incluir en POA."
        )
    if not recomendaciones:
        recomendaciones.append(
            "✅ Todas las capas coherentes — recomendación puede elevarse al decisor."
        )

    return {
        "capas":          capas,
        "global_avg":     round(global_avg),
        "coherencia":     coherencia,
        "coherencia_label": coh_label,
        "criticos":       len(criticos),
        "total_issues":   len(all_issues),
        "recomendaciones": recomendaciones,
        "doctrine":       "ENTENDER → GOBERNAR → SIMULAR → CONFIAR",
        "version":        "QUADRUM Engine v1.0 · Dylus Lab 2026",
    }
