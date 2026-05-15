"""
SENTINEL · coherencia_engine.py
Motor de Coherencia Institucional — Fase 3.
Evalúa si una decisión de gestión pública puede implementarse con éxito
en 4 dimensiones institucionales:
  PLANIFICACIÓN → PRESUPUESTO → COMPETENCIA LEGAL → CAPACIDAD OPERATIVA
Resultado: Confianza de Implementación (0-100%)
Doctrina: QUIRA fundamenta. La autoridad pública decide.
Dylus Lab © 2026
"""
from __future__ import annotations
import unicodedata

# ── PESOS DE CADA DIMENSIÓN ────────────────────────────────────────────────────
_W_PLANIFICACION  = 0.30
_W_PRESUPUESTO    = 0.25
_W_LEGAL          = 0.25
_W_OPERATIVA      = 0.20

_ICGIT_BASE = 53.56   # score Q1-2026 para calibrar capacidad operativa


def _norm(text: str) -> str:
    nfkd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


# ── EVALUADORES POR DIMENSIÓN ──────────────────────────────────────────────────

def _eval_planificacion(data: dict, query: str, territory: str | None) -> dict:
    """
    PLANIFICACIÓN — ¿La acción está contemplada en el PDOT y POA vigente?
    """
    q      = _norm(query)
    score  = 65
    issues = []
    findings = []

    # Alineación PDOT explícita
    pdot_terms = [
        "pdot", "meta", "planificacion", "plan operativo", "poa", "2027", "objetivo estrategico",
        # Participación ciudadana — proceso PP es parte del ciclo de planificación
        "participativo", "pp 2026", "asamblea", "asamblea local",
        # Cumplimiento normativo — consultas de verificación implican proceso planificado
        "cumple", "cumplimiento", "conforme al cootad", "listo para elevar",
    ]
    if any(t in q for t in pdot_terms):
        score += 15
        findings.append("Consulta alineada con instrumentos de planificación PDOT/POA")
        # Bonus adicional: consulta de verificación de cumplimiento (proceso ya ejecutado)
        compliance_terms = ["cumple", "cumplimiento", "completado", "conforme", "listo para elevar"]
        if any(t in q for t in compliance_terms):
            score += 5
            findings.append("Consulta de verificación de cumplimiento — proceso institucional ejecutado")
    else:
        issues.append("Sin referencia explícita a PDOT o POA — validar alineación con Planificación")

    # Territorio con datos disponibles
    if territory:
        parroquias = data.get("parroquias", [])
        par = next(
            (p for p in parroquias if _norm(p["nombre"]) in _norm(territory)
             or _norm(territory) in _norm(p["nombre"])),
            None,
        )
        if par:
            findings.append(f"Territorio {par['nombre']} con datos PDOT verificados (NBI={par['nbi']}%)")
            if par.get("estado") == "EMERGENCIA":
                findings.append("⚠ Parroquia en estado EMERGENCIA — intervención urgente")
                score += 8   # emergencia = prioridad PDOT, facilita planificación
        else:
            issues.append("Territorio no identificado en el sistema — verificar con Planificación")
            score -= 8

    # SATs que bloquean planificación
    sat = data.get("sat", [])
    criticas = [s for s in sat if s.get("nivel") == "CRÍTICO"]
    if criticas:
        issues.append(f"{len(criticas)} señal(es) SAT crítica(s) activa(s) — requieren atención paralela")
        score -= len(criticas) * 4

    score = max(30, min(100, score))
    return {
        "dimension":  "Planificación",
        "pregunta":   "¿Está en el PDOT y POA vigente?",
        "score":      score,
        "nivel":      _nivel(score),
        "issues":     issues,
        "findings":   findings,
    }


def _eval_presupuesto(
    data:       dict,
    sim_result: dict | None,
    territory:  str | None,
    query:      str = "",
) -> dict:
    """
    PRESUPUESTO — ¿Existe margen presupuestario disponible?
    """
    q      = _norm(query)
    score  = 65
    issues = []
    findings = []
    hard_block = False

    icgit  = data.get("icgit", {})
    ejecucion = icgit.get("ti_raw", 0)

    # ── Check ISP: bloqueo formal por salud presupuestaria ─────────────────────
    # Se activa solo en consultas de crédito/financiamiento externo
    _credito_terms = ["bde", "credito", "prestamo", "financiamiento externo",
                      "perfil bde", "salud presupuestaria", "isp actual"]
    isp_val = data.get("indices", {}).get("ISP", {}).get("valor")
    if any(t in q for t in _credito_terms) and isp_val is not None and isp_val < 65:
        issues.append(
            f"⛔ ISP={isp_val:.2f}% bajo umbral COOTAD mínimo (65%) — "
            f"bloqueo formal de acceso a crédito BDE y transferencias condicionadas"
        )
        score = min(score, 35)
        hard_block = True

    # Ejecución presupuestaria como proxy de disponibilidad
    if ejecucion < 20:
        findings.append(f"Ejecución Q1 baja ({ejecucion:.1f}%) — existe margen presupuestario disponible")
        score += 12
    elif ejecucion < 40:
        findings.append(f"Ejecución Q1 moderada ({ejecucion:.1f}%) — margen ajustado")
        score += 4
    else:
        findings.append(f"Ejecución Q1 alta ({ejecucion:.1f}%) — margen presupuestario reducido")
        score -= 8
        issues.append("Ejecución avanzada — reasignación requiere reforma presupuestaria formal")

    # Simulación disponible: usa datos de inversión calculados
    if sim_result:
        inv_add = sim_result.get("inversion_adicional", 0)
        pc_nuevo = sim_result.get("per_capita_nuevo", 0)
        pc_base  = sim_result.get("baseline", {}).get("per_capita", 60)
        findings.append(
            f"Inversión adicional proyectada: ${inv_add:,} "
            f"(${pc_base}/hab → ${pc_nuevo}/hab)"
        )
        if pc_nuevo < 60:
            issues.append("Inversión per cápita proyectada sigue por debajo del umbral mínimo ($60/hab)")
            score -= 6
        elif pc_nuevo >= 80:
            score += 8

    # Parroquia sin inversión registrada
    if territory:
        parroquias = data.get("parroquias", [])
        par = next(
            (p for p in parroquias if _norm(p.get("nombre", "")) in _norm(territory)
             or _norm(territory) in _norm(p.get("nombre", ""))),
            None,
        )
        if par and par.get("per_capita", 0) == 0:
            issues.append(f"{par['nombre']}: sin inversión registrada Q1-2026 — prioridad de transferencia")
            score -= 10

    score = max(30, min(100, score))
    return {
        "dimension":  "Presupuesto",
        "pregunta":   "¿Existe margen presupuestario?",
        "score":      score,
        "nivel":      _nivel(score),
        "issues":     issues,
        "findings":   findings,
        "hard_block": hard_block,
    }


def _eval_legal(legal_refs: list[dict], query: str = "") -> dict:
    """
    COMPETENCIA LEGAL — ¿El GAD tiene autoridad legal para esta acción?
    """
    q      = _norm(query)
    score  = 55
    issues = []
    findings = []

    # ── Detección de bypass de proceso legal obligatorio ───────────────────────
    # Si la consulta propone omitir PAC/SERCOP/proceso formal, la acción es ilegal
    _bypass_terms = [
        "sin pac", "sin incluirla en el pac", "sin incluirlo en el pac",
        "sin incluir en el pac", "directamente sin", "sin proceso sercop",
        "evadir", "saltarnos el pac", "sin pasar por sercop",
    ]
    if any(t in q for t in _bypass_terms):
        score = min(40, score)   # bloqueo legal — acción propuesta viola LOSNCP
        issues.append(
            "⛔ Consulta plantea omitir proceso obligatorio (PAC/SERCOP) — "
            "acción ilegal conforme COPLAFIP Art.100 y LOSNCP Art.4 (prohibición de fraccionamiento)"
        )
        findings.append("Marco normativo violado: COPLAFIP Art.100 · COOTAD Art.432 · LOSNCP Art.4")
        return {
            "dimension":  "Competencia Legal",
            "pregunta":   "¿El GAD tiene autoridad legal?",
            "score":      score,
            "nivel":      _nivel(score),
            "issues":     issues,
            "findings":   findings,
        }

    if not legal_refs:
        issues.append("Sin fundamento normativo identificado — consultar con Asesoría Jurídica")
        return {
            "dimension":  "Competencia Legal",
            "pregunta":   "¿El GAD tiene autoridad legal?",
            "score":      score,
            "nivel":      _nivel(score),
            "issues":     issues,
            "findings":   ["Sin referencias legales activas para esta consulta"],
        }

    # Mapeo de intent → puntuación de autoridad legal
    _INTENT_SCORES = {
        "agua_potable":       88,  # competencia exclusiva CRE Art.264 + COOTAD Art.55
        "competencias":       92,  # competencias constitucionales directas
        "participacion":      85,  # obligatorio por COOTAD
        "equidad_territorial":80,
        "planificacion":      82,
        "reforma_poa":        72,  # viable con condiciones
        "contratacion":       75,  # requiere proceso SERCOP
        "presupuesto":        78,
        "gobernanza":         80,
        "finanzas":           70,
        "derechos":           85,  # CRE = norma suprema
    }

    intents   = list({r.get("intent", "general") for r in legal_refs})
    max_score = max(_INTENT_SCORES.get(i, 60) for i in intents)
    score     = max_score

    # Bonus por respaldo constitucional (CRE)
    has_cre = any(r["law"] == "CRE" for r in legal_refs)
    if has_cre:
        score = min(100, score + 6)
        findings.append("Respaldo constitucional (CRE) — jerarquía normativa máxima")

    for r in legal_refs:
        findings.append(f"{r['law']} {r['article']} — {r['topic']}")

    if score < 70:
        issues.append("Autoridad legal condicionada — verificar con Asesoría Jurídica antes de proceder")

    score = max(30, min(100, score))
    return {
        "dimension":  "Competencia Legal",
        "pregunta":   "¿El GAD tiene autoridad legal?",
        "score":      score,
        "nivel":      _nivel(score),
        "issues":     issues,
        "findings":   findings,
    }


def _eval_capacidad_operativa(
    data:       dict,
    sim_result: dict | None,
    territory:  str | None,
) -> dict:
    """
    CAPACIDAD OPERATIVA — ¿Puede el GAD ejecutar esta acción con su capacidad actual?
    Base neutral = 65; ICGI-T actúa como modificador, no como base directa
    (ICGI-T=53 en un GAD pequeño no impide ejecutar proyectos específicos).
    """
    icgit  = data.get("icgit", {})
    ic_val = icgit.get("score", _ICGIT_BASE)
    score  = 65   # base neutral
    issues = []
    findings = []

    findings.append(
        f"ICGI-T Q1-2026: {ic_val:.2f} pts ({icgit.get('avep', 'Transición Crítica')})"
    )

    # ICGI-T como modificador (±)
    if ic_val >= 70:
        score += 10
        findings.append("ICGI-T en Mandato — capacidad institucional favorable")
    elif ic_val < 50:
        score -= 10
        issues.append("ICGI-T en Ocurrencia/Ruptura — capacidad institucional limitada")

    # SATs críticas compiten por recursos operativos
    sat      = data.get("sat", [])
    criticas = [s for s in sat if s.get("nivel") == "CRÍTICO"]
    if criticas:
        penalidad = len(criticas) * 5
        score -= penalidad
        issues.append(
            f"{len(criticas)} señal(es) SAT crítica(s) compiten por capacidad operativa "
            f"(-{penalidad} pts)"
        )

    # Delta agresivo → mayor exigencia operativa
    if sim_result:
        delta = sim_result.get("delta_pct", 0)
        if delta > 40:
            score -= 10
            issues.append(
                f"Incremento del {delta}% es operativamente exigente — "
                f"verificar capacidad de ejecución y cronograma"
            )
        elif delta > 25:
            score -= 4

    # Parroquia en EMERGENCIA → contexto operativo más complejo
    if territory:
        parroquias = data.get("parroquias", [])
        par = next(
            (p for p in parroquias if _norm(p.get("nombre", "")) in _norm(territory)
             or _norm(territory) in _norm(p.get("nombre", ""))),
            None,
        )
        if par:
            if par.get("estado") == "EMERGENCIA":
                score -= 8
                issues.append(
                    f"{par['nombre']} en EMERGENCIA — logística de ejecución más compleja"
                )
            findings.append(
                f"Población: {par.get('habitantes', '?'):,} hab · Estado: {par.get('estado', '?')}"
            )

    score = max(30, min(100, score))
    return {
        "dimension":  "Capacidad Operativa",
        "pregunta":   "¿Puede el GAD ejecutar esta acción?",
        "score":      score,
        "nivel":      _nivel(score),
        "issues":     issues,
        "findings":   findings,
    }


# ── HELPERS ────────────────────────────────────────────────────────────────────

def _nivel(score: int) -> str:
    if score >= 80: return "Alta"
    if score >= 65: return "Media"
    if score >= 50: return "Baja"
    return "Insuficiente"


def _confianza_label(ci: int) -> str:
    if ci >= 80: return "Alta — lista para elevar al decisor"
    if ci >= 65: return "Moderada — resolver observaciones antes de comprometer recursos"
    if ci >= 50: return "Baja — requiere acciones previas"
    return "Insuficiente — no recomendado sin intervención correctiva"


# ── API PÚBLICA ────────────────────────────────────────────────────────────────

def evaluate(
    query:       str,
    data:        dict,
    sim_result:  dict | None = None,
    legal_refs:  list        = None,
    territory:   str | None  = None,
) -> dict:
    """
    Evaluación de Coherencia Institucional completa — las 4 dimensiones.

    Args:
        query:      pregunta o acción propuesta por el usuario
        data:       load_all() — datos institucionales
        sim_result: resultado de simulate_policy() si existe
        legal_refs: lista de find_legal_refs() si existe
        territory:  parroquia activa si hay

    Returns:
        dict con dimensiones, confianza_implementacion, label, recomendaciones
    """
    if legal_refs is None:
        legal_refs = []

    dimensiones = [
        _eval_planificacion(data, query, territory),
        _eval_presupuesto(data, sim_result, territory, query),
        _eval_legal(legal_refs, query),
        _eval_capacidad_operativa(data, sim_result, territory),
    ]

    # Confianza de implementación — promedio ponderado
    pesos = [_W_PLANIFICACION, _W_PRESUPUESTO, _W_LEGAL, _W_OPERATIVA]
    ci    = round(sum(d["score"] * w for d, w in zip(dimensiones, pesos)))
    ci    = max(30, min(99, ci))

    # Hard block: si Presupuesto detectó bloqueo fiscal formal, cap global
    hard_blocked = any(d.get("hard_block") for d in dimensiones)
    if hard_blocked:
        ci = min(ci, 45)

    # Recomendaciones ejecutivas
    all_issues  = [i for d in dimensiones for i in d["issues"]]
    criticas    = [d for d in dimensiones if d["nivel"] == "Insuficiente"]
    bajas       = [d for d in dimensiones if d["nivel"] == "Baja"]
    recomendaciones = []

    if criticas:
        recomendaciones.append(
            f"⛔ {', '.join(d['dimension'] for d in criticas)} en nivel Insuficiente — "
            f"bloquea implementación. Atender antes de proceder."
        )
    if bajas:
        recomendaciones.append(
            f"⚠ {', '.join(d['dimension'] for d in bajas)} requiere refuerzo "
            f"antes de comprometer recursos."
        )
    if not legal_refs:
        recomendaciones.append(
            "Agregar fundamento normativo (COOTAD/COPLAFIP/CRE) para respaldar la decisión."
        )
    if ci >= 80 and not criticas:
        recomendaciones.append(
            "✅ Coherencia suficiente — recomendación puede elevarse al decisor con el respaldo técnico generado."
        )
    elif ci >= 65 and not criticas:
        recomendaciones.append(
            "Subsanar las observaciones identificadas y validar con Planificación antes de elevar al Concejo."
        )

    return {
        "dimensiones":              dimensiones,
        "confianza_implementacion": ci,
        "confianza_label":          _confianza_label(ci),
        "total_issues":             len(all_issues),
        "recomendaciones":          recomendaciones,
        "doctrine":                 "PLANIFICACIÓN → PRESUPUESTO → COMPETENCIA LEGAL → CAPACIDAD OPERATIVA",
        "version":                  "Coherencia Engine v1.0 · Dylus Lab 2026",
    }


def detect_coherencia_intent(query: str) -> bool:
    """
    True si la query es de tipo: simulación de política, viabilidad normativa,
    o solicitud de evaluación de coherencia institucional.
    Determina cuándo mostrar el coherencia_card automáticamente.
    """
    q = _norm(query)
    triggers = [
        # Simulación / proyección
        "si subimos", "si aumentamos", "si invertimos", "simula", "proyecta",
        "que pasa si", "escenario", "impacto de",
        # Viabilidad normativa
        "puedo", "podemos", "es posible", "es viable", "esta permitido",
        "reasignar", "reformar", "modificar presupuesto",
        # Solicitud explícita
        "coherencia", "confianza de implementacion", "evalua", "diagnóstico",
        "puede el gad", "tiene capacidad",
    ]
    return any(t in q for t in triggers)
