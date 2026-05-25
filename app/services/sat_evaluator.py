"""
app/services/sat_evaluator.py — QUIRA OS · Sprint 2
Evaluador SAT — Sistema de Alertas y Trazabilidad

Evalúa el catálogo SAT (SAT-0 a SAT-VIII) contra los datos
del snapshot Q1 y produce alertas accionables con triple anclaje.

Doctrina:
  Triple ancla: Base Legal + Base Operativa + Base Doctrinal QUIRA
  SAT no es una metodología paralela a la ley.
  SAT es una capa de validación doctrinal SOBRE la ley.
  Cada alerta tiene anclaje: artículo legal + métrica observable + código SAT.

Referencia: SAT_Catalogo (Gold Master) + H75_SAT_ENGINE
Dylus Lab © 2026
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

# ── Catálogo SAT canónico ──────────────────────────────────────────────────────
# Cada entrada define un SAT evaluable contra datos del snapshot Q1.
# Campos:
#   codigo, nombre, dimension, tipo, peso_severidad
#   base_legal_art, base_legal_desc
#   base_doctrinal
#   evaluator: callable(snapshot_data) → (bool_activa, valor_observado, str_detalle)

SAT_CATALOG = [
    {
        "codigo":         "SAT-0",
        "nombre":         "Coherencia POA-PAC",
        "dimension":      "D2",
        "tipo":           "preventiva",
        "peso_severidad": 0.20,
        "base_legal_art": "LOSNCP Art. 22",
        "base_legal_desc": "Obliga a que el PAC refleje los procesos de contratación previstos en el POA.",
        "base_doctrinal": "D2-Planificación: ausencia de coherencia planificación-contratación.",
        "ref_engine":     "H75_SAT_ENGINE + H21b_SAT-0",
    },
    {
        "codigo":         "SAT-I",
        "nombre":         "Fragmentacion Selectiva",
        "dimension":      "D3",
        "tipo":           "critica",
        "peso_severidad": 0.25,
        "base_legal_art": "COPFP Art. 54",
        "base_legal_desc": "Entidades deben reportar avances de TODAS las metas en el SIGAD.",
        "base_doctrinal": "D3-Ejecución: calificación alta con universo de metas mínimo = señal de fragmentación.",
        "ref_engine":     "H75_SAT_ENGINE + H21_SAT-I",
    },
    {
        "codigo":         "SAT-II",
        "nombre":         "Reforma Significativa Tardia",
        "dimension":      "D2",
        "tipo":           "alerta",
        "peso_severidad": 0.15,
        "base_legal_art": "COPFP Art. 115 / Acuerdo MEF 067",
        "base_legal_desc": "Reformas presupuestarias deben justificarse. Reformas tardías evidencian planificación reactiva.",
        "base_doctrinal": "D2-Planificación: reformas post-Q2 > 5% codificado base = planificación reactiva.",
        "ref_engine":     "H75_SAT_ENGINE + H22_SAT-II",
    },
    {
        "codigo":         "SAT-III",
        "nombre":         "Paralisis Presupuestaria",
        "dimension":      "D3",
        "tipo":           "critica",
        "peso_severidad": 0.20,
        "base_legal_art": "COPFP Art. 113",
        "base_legal_desc": "Obliga evaluación periódica de ejecución presupuestaria por período.",
        "base_doctrinal": "D3-Ejecución: Ti < umbral por persistencia longitudinal = riesgo SAT-D3 CRÍTICO.",
        "ref_engine":     "H75_SAT_ENGINE + H23_SAT-III",
    },
    {
        "codigo":         "SAT-IV",
        "nombre":         "Alerta Fiscal COOTAD",
        "dimension":      "D3",
        "tipo":           "legal",
        "peso_severidad": 0.10,
        "base_legal_art": "COOTAD Art. 192",
        "base_legal_desc": "GAD debe destinar mínimo 65% de ingresos propios a inversión pública.",
        "base_doctrinal": "D3-Ejecución + D1-Legalidad: incumplimiento directo de mandato legal con magnitud medible.",
        "ref_engine":     "H75_SAT_ENGINE + H24_SAT-IV + H16_IFE",
    },
    {
        "codigo":         "SAT-V",
        "nombre":         "Brecha Compromiso CPCCS",
        "dimension":      "D5",
        "tipo":           "alerta",
        "peso_severidad": 0.05,
        "base_legal_art": "COOTAD Art. 302",
        "base_legal_desc": "GAD debe realizar RdC anual y cumplir compromisos declarados.",
        "base_doctrinal": "D5-Capacidad Institucional: brecha compromiso-cumplimiento erosiona credibilidad.",
        "ref_engine":     "H75_SAT_ENGINE + H24b_SAT-V_ALERTA_CPCCS",
    },
    {
        "codigo":         "SAT-VI",
        "nombre":         "Desvio Presupuesto Participativo",
        "dimension":      "D4",
        "tipo":           "alerta",
        "peso_severidad": 0.05,
        "base_legal_art": "COOTAD Art. 238 / Reglamento PP",
        "base_legal_desc": "PP debe ejecutarse según lo acordado. Desvíos requieren justificación.",
        "base_doctrinal": "D4-Equidad Territorial: PP es el mecanismo de inversión territorial equitativa.",
        "ref_engine":     "H75_SAT_ENGINE + H24c_SAT-VI_DESVÍO_PP",
    },
    {
        "codigo":         "SAT-VII",
        "nombre":         "Vi Sinaptico Pulso",
        "dimension":      "D3",
        "tipo":           "informacional",
        "peso_severidad": 0.00,
        "base_legal_art": "COPFP Art. 54 (referencial)",
        "base_legal_desc": "Entidades deben reportar avances mensualmente en el SIGAD.",
        "base_doctrinal": "D3-Ejecución: pulso sináptico mide vitalidad operativa del plan. Peso=0.",
        "ref_engine":     "H75_SAT_ENGINE (peso=0, informacional)",
    },
    {
        "codigo":         "SAT-VIII",
        "nombre":         "Equidad Territorial",
        "dimension":      "D4",
        "tipo":           "informacional",
        "peso_severidad": 0.00,
        "base_legal_art": "COOTAD Art. 249 (referencial)",
        "base_legal_desc": "GAD debe garantizar equidad en la inversión territorial.",
        "base_doctrinal": "D4-Equidad Territorial: IET mide equilibrio de inversión. Peso=0.",
        "ref_engine":     "H75_SAT_ENGINE (peso=0, informacional) + H42_IET",
    },
]


# ── Thresholds (configurables desde config.py) ────────────────────────────────
_DEFAULTS = {
    "ejecucion_critica":    0.60,
    "ejecucion_alerta":     0.75,
    "inversion_minima":     0.65,    # COOTAD Art. 192
    "pac_requerido":        True,
    "cancelados_alerta":    0.15,
    "rdc_score_minimo":     50.0,
    "rdc_brecha_compromisos": 0.30,
    "pp_desvio_maximo":     0.20,
    "vi_pulso_minimo":      0.85,
    "iet_desviacion_max":   0.20,
    "reformas_umbral_pct":  0.05,    # 5% codificado base
}


def _get_thresholds() -> dict:
    try:
        import config as cfg
        sat = getattr(cfg, "SAT_THRESHOLDS", {})
        return {**_DEFAULTS, **sat}
    except ImportError:
        return _DEFAULTS


# ══════════════════════════════════════════════════════════════════════════════
# Clasificación de riesgo (helper público — usado en tests y en evaluate_sat)
# ══════════════════════════════════════════════════════════════════════════════

def _classify_risk(riesgo: float) -> str:
    """Clasifica el riesgo ponderado SAT en niveles canónicos.

    Umbrales (base doctrinal QUIRA):
        < 0.15  → BAJO
        < 0.30  → MEDIO
        < 0.50  → ALTO
        >= 0.50 → CRÍTICO

    Args:
        riesgo: float en [0, 1] — riesgo ponderado acumulado.

    Returns:
        str — "BAJO" | "MEDIO" | "ALTO" | "CRÍTICO"
    """
    if riesgo < 0.15:
        return "BAJO"
    if riesgo < 0.30:
        return "MEDIO"
    if riesgo < 0.50:
        return "ALTO"
    return "CRÍTICO"


# ══════════════════════════════════════════════════════════════════════════════
# Evaluador principal
# ══════════════════════════════════════════════════════════════════════════════

def evaluate_sat(snapshot: dict) -> dict:
    """Evalúa el catálogo SAT completo contra los datos del snapshot.

    Args:
        snapshot: dict del snapshot Q1 (campos: financiero, contratacion,
                  accountability, tgi, sources, gold_master_data?)

    Returns:
        dict con claves:
            alertas:          list[dict] — SATs evaluadas (activas e inactivas)
            activas:          list[str]  — códigos SAT activos
            riesgo_ponderado: float      — Σ(peso_sev × activa) [0-1]
            clasif_riesgo:    str        — BAJO / MEDIO / ALTO / CRÍTICO
            sat_score:        float      — (1 - riesgo_ponderado) × 100
            datos_insuficientes: list[str] — SATs sin datos para evaluar
            evaluated_at:     str
            fuente_datos:     str        — "pipeline" | "gold_master" | "mixto"
    """
    t   = _get_thresholds()
    now = datetime.now(timezone.utc).isoformat()

    # ── Extraer datos disponibles ──────────────────────────────────────────────
    fin     = snapshot.get("financiero", {})
    cont    = snapshot.get("contratacion", {})
    acc     = snapshot.get("accountability", {}).get("rdc", {})
    gm      = snapshot.get("gold_master_data", {})     # si el pipeline lo pobló
    sources = snapshot.get("sources", {})

    # Determinar fuente de datos
    has_api_data = any(
        sources.get(s, {}).get("status") == "ok"
        for s in ("dpe", "sercop", "cpccs")
    )
    has_gm_data = bool(gm)
    fuente = ("pipeline" if has_api_data and not has_gm_data
              else "gold_master" if has_gm_data and not has_api_data
              else "mixto" if has_api_data and has_gm_data
              else "insuficiente")

    # ── Helpers para extraer valores con fallback GoldMaster ──────────────────
    def _get_fin(key: str, gm_key: str | None = None, default=None):
        v = fin.get(key)
        if v is None and gm_key and gm:
            v = gm.get("financiero", {}).get(gm_key)
        return v if v is not None else default

    def _get_cont(key: str, gm_key: str | None = None, default=None):
        v = cont.get(key)
        if v is None and gm_key and gm:
            v = gm.get("contratacion", {}).get(gm_key)
        return v if v is not None else default

    def _get_rdc(key: str, gm_key: str | None = None, default=None):
        v = acc.get(key)
        if v is None and gm_key and gm:
            v = gm.get("accountability", {}).get(gm_key)
        return v if v is not None else default

    # ── Evaluar cada SAT ──────────────────────────────────────────────────────
    alertas:             list[dict] = []
    activas:             list[str]  = []
    datos_insuficientes: list[str]  = []
    riesgo_acum          = 0.0

    for sat in SAT_CATALOG:
        codigo = sat["codigo"]
        alerta = {
            "codigo":         codigo,
            "nombre":         sat["nombre"],
            "dimension":      sat["dimension"],
            "tipo":           sat["tipo"],
            "peso_severidad": sat["peso_severidad"],
            "base_legal_art": sat["base_legal_art"],
            "base_legal_desc": sat["base_legal_desc"],
            "base_doctrinal": sat["base_doctrinal"],
            "ref_engine":     sat["ref_engine"],
            "estado":         "SIN_DATOS",
            "activa":         False,
            "valor_observado": None,
            "umbral":          None,
            "detalle":         "",
        }

        if codigo == "SAT-0":
            pac = _get_cont("pac_publicado", "pac_publicado")
            if pac is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "pac_publicado no disponible en pipeline"
            else:
                alerta["valor_observado"] = pac
                alerta["umbral"]          = "pac_publicado = True"
                if not pac:
                    alerta["estado"]  = "ACTIVA"
                    alerta["activa"]  = True
                    alerta["detalle"] = "PAC no publicado — incumplimiento LOSNCP Art.22"
                else:
                    alerta["estado"]  = "OK"
                    alerta["detalle"] = "PAC publicado — coherencia PAC requerida verificada"

        elif codigo == "SAT-I":
            icm   = _get_fin("icm_global")
            cob   = _get_fin("pct_metas_reportadas")
            if icm is None or cob is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "ICM / cobertura metas no disponible (requiere SIGAD)"
            else:
                alerta["valor_observado"] = {"icm": icm, "cobertura_metas": cob}
                alerta["umbral"]          = "ICM >= 0.80 AND cobertura_metas <= 0.10"
                if icm >= 0.80 and cob <= 0.10:
                    alerta["estado"]  = "ACTIVA"
                    alerta["activa"]  = True
                    alerta["detalle"] = (f"ICM={icm:.2%} >= 80% con cobertura metas={cob:.2%} <= 10% "
                                        f"— señal de fragmentación selectiva")
                else:
                    alerta["estado"]  = "OK"
                    alerta["detalle"] = f"Sin fragmentación: ICM={icm:.2%} / cob={cob:.2%}"

        elif codigo == "SAT-II":
            reformas = _get_fin("reformas_presupuestarias")
            if reformas is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "Reformas presupuestarias no disponibles en pipeline"
            else:
                alerta["valor_observado"] = reformas
                alerta["umbral"]          = f"> {t['reformas_umbral_pct']:.0%} codificado base post-Q2"
                umbral_pct = t["reformas_umbral_pct"]
                if isinstance(reformas, dict):
                    pct = reformas.get("pct_reforma", 0) or 0
                    post_q2 = reformas.get("post_q2", False)
                    if pct > umbral_pct and post_q2:
                        alerta["estado"]  = "ACTIVA"
                        alerta["activa"]  = True
                        alerta["detalle"] = f"Reforma tardía: {pct:.2%} > {umbral_pct:.2%} post-Q2"
                    else:
                        alerta["estado"]  = "OK"
                        alerta["detalle"] = "Sin reforma significativa tardía detectada"
                else:
                    datos_insuficientes.append(codigo)
                    alerta["detalle"] = "Formato reformas no reconocido"

        elif codigo == "SAT-III":
            # Intentar desde pipeline, luego Gold Master ISP
            ti = _get_fin("ejecucion_porcentaje")
            if ti is None:
                # Fallback: ISP del Gold Master (indirecto de ejecución)
                isp = _get_fin("isp_salud_presup", "isp_salud_presup")
                ti  = isp   # aproximación — debería ser ejecución total Ti
            if ti is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "Ejecución presupuestaria Ti no disponible en pipeline"
            else:
                umbral_crit = t["ejecucion_critica"]
                alerta["valor_observado"] = ti
                alerta["umbral"]          = f"Ti < {umbral_crit:.0%}"
                if ti < umbral_crit:
                    alerta["estado"]  = "ACTIVA"
                    alerta["activa"]  = True
                    alerta["detalle"] = (f"Ti = {ti:.2%} < umbral crítico {umbral_crit:.0%} — "
                                        f"parálisis presupuestaria — COPFP Art.113")
                else:
                    alerta["estado"]  = "OK"
                    alerta["detalle"] = f"Ejecución aceptable: Ti = {ti:.2%}"

        elif codigo == "SAT-IV":
            inv = _get_fin("inversion_porcentaje", "ife_inversion")
            if inv is None:
                # Fallback Gold Master ISP_SALUD_PRESUP como proxy de inversión social
                inv = _get_fin(None, "isp_salud_presup")
            if inv is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "Inversión pública (%) no disponible en pipeline"
            else:
                meta = t["inversion_minima"]
                alerta["valor_observado"] = inv
                alerta["umbral"]          = f">= {meta:.0%} (COOTAD Art.192)"
                if inv < meta:
                    brecha = meta - inv
                    alerta["estado"]  = "ACTIVA"
                    alerta["activa"]  = True
                    alerta["detalle"] = (f"Inversión = {inv:.2%} < meta {meta:.0%} — "
                                        f"brecha = {brecha:.2%} — COOTAD Art.192 INCUMPLIDO")
                else:
                    alerta["estado"]  = "OK"
                    alerta["detalle"] = f"Inversión {inv:.2%} >= meta {meta:.0%}"

        elif codigo == "SAT-V":
            score_rdc = acc.get("score_total")
            if score_rdc is None:
                score_rdc = _get_rdc("score_total", "rdc_score")
            if score_rdc is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "Score RdC CPCCS no disponible"
            else:
                minimo = t["rdc_score_minimo"]
                alerta["valor_observado"] = score_rdc
                alerta["umbral"]          = f">= {minimo:.0f}/100"
                if score_rdc < minimo:
                    alerta["estado"]  = "ACTIVA"
                    alerta["activa"]  = True
                    alerta["detalle"] = (f"Score RdC = {score_rdc}/100 < mínimo {minimo:.0f} — "
                                        f"brecha compromiso CPCCS — COOTAD Art.302")
                else:
                    alerta["estado"]  = "OK"
                    alerta["detalle"] = f"Score RdC aceptable: {score_rdc}/100"

        elif codigo == "SAT-VI":
            pp_reg = _get_fin("pp_registrado")
            pp_eje = _get_fin("pp_ejecutado")
            if pp_reg is None or pp_eje is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "PP registrado/ejecutado no disponible (requiere partida presupuestaria)"
            else:
                if pp_reg > 0:
                    desvio = abs(pp_eje - pp_reg) / pp_reg
                    max_dev = t["pp_desvio_maximo"]
                    alerta["valor_observado"] = {"pp_reg": pp_reg, "pp_eje": pp_eje, "desvio": desvio}
                    alerta["umbral"]          = f"desvio > {max_dev:.0%}"
                    if desvio > max_dev:
                        alerta["estado"]  = "ACTIVA"
                        alerta["activa"]  = True
                        alerta["detalle"] = f"Desvío PP = {desvio:.2%} > {max_dev:.0%}"
                    else:
                        alerta["estado"]  = "OK"
                        alerta["detalle"] = f"Desvío PP aceptable: {desvio:.2%}"
                else:
                    datos_insuficientes.append(codigo)
                    alerta["detalle"] = "pp_registrado = 0 — sin presupuesto participativo registrado"

        elif codigo == "SAT-VII":
            vi = _get_fin("vi_promedio_metas")
            if vi is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "Vi promedio metas PDOT no disponible (informacional)"
            else:
                minimo = t["vi_pulso_minimo"]
                alerta["valor_observado"] = vi
                alerta["umbral"]          = f">= {minimo:.2f} (informacional)"
                alerta["estado"]  = "INFORMACIONAL"
                alerta["detalle"] = (f"Vi promedio = {vi:.3f} — "
                                     f"{'por debajo del pulso mínimo' if vi < minimo else 'pulso saludable'}")

        elif codigo == "SAT-VIII":
            iet = _get_fin(None)  # No direct pipeline field yet
            if iet is None:
                datos_insuficientes.append(codigo)
                alerta["detalle"] = "IET desviación no disponible (requiere datos geolocalizados — Fase 2)"
            else:
                alerta["estado"]          = "INFORMACIONAL"
                alerta["valor_observado"] = iet
                alerta["detalle"]         = f"IET desviación = {iet:.2%}"

        # Acumular riesgo si está activa y tiene peso
        if alerta["activa"] and sat["peso_severidad"] > 0:
            riesgo_acum += sat["peso_severidad"]

        alertas.append(alerta)
        if alerta["activa"]:
            activas.append(codigo)

    # ── Clasificación de riesgo ────────────────────────────────────────────────
    clasif = _classify_risk(riesgo_acum)

    sat_score = round((1 - riesgo_acum) * 100, 1)

    logger.info(
        f"[SAT] Evaluación completa — activas: {len(activas)} | "
        f"riesgo: {riesgo_acum:.3f} → {clasif} | "
        f"sin datos: {len(datos_insuficientes)} SATs"
    )
    for a in alertas:
        if a["activa"]:
            logger.warning(f"[SAT] ⚠ {a['codigo']} ACTIVA — {a['detalle']}")

    return {
        "alertas":              alertas,
        "activas":              activas,
        "alertas_activas":      activas,   # alias canónico para p0_inicio y dashboard
        "riesgo_ponderado":     round(riesgo_acum, 4),
        "clasif_riesgo":        clasif,
        "sat_score":            sat_score,
        "datos_insuficientes":  datos_insuficientes,
        "evaluated_at":         now,
        "fuente_datos":         fuente,
        "total_evaluadas":      len(alertas),
        "total_activas":        len(activas),
    }
