"""
app/engines/fondos_matcher.py — Motor de Elegibilidad D02 · QUIRA OS
======================================================================
Conecta los 21 indicadores canónicos del GAD con el universo de
convocatorias activas en Supabase y determina el estado de elegibilidad
financiera de Montecristi (y cualquier GAD futuro).

RESPONSABILIDAD ÚNICA:
    Responder: "¿Qué dinero puede capturar el GAD con su estado actual?"

ARQUITECTURA:
    1. _read_gad_indicators()  → lee PSG/ISP/IGP/IOC/IET/IED/IFE_A/ITAM...
       Prioridad: Gold Master live → demo_data snapshot → None
    2. _evaluate_req()         → operador lógico sobre un indicador
    3. match_convocatoria()    → evalúa 1 convocatoria contra N requisitos
    4. run_matcher()           → entry point: lee, evalúa, UPSERT Supabase

BLOOMBERG FIREWALL:
    - Entrada: indicadores internos (PSG, ISP, etc.)
    - Salida: estado_quira, brechas_json — lenguaje de gobernanza
    - NUNCA expone: ICPI · TGI · Ti · QTMP · H73 · Gold Master en UI
    - Las brechas son "{codigo}: -17.17" no "H73.PSG_EJECUCION delta"

INVARIANTE (ADR-023 Regla 1):
    Los valores de indicadores vienen del Gold Master (Excel → Python).
    NUNCA se calculan aquí. NUNCA se recalculan. Solo se leen.

Dylus Lab © 2026 · ADR-026 §D02 Consecuencia
"""
from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

# ── Constantes ────────────────────────────────────────────────────────────────
GAD_ID_DEFAULT = "MCR-001"          # Montecristi · Municipio 001 QUIRA

# Estados de confianza del indicador (copiado a monto_confianza)
_CONF_ALTA     = "alta"             # Gold Master live
_CONF_MEDIA    = "media"            # demo_data snapshot (last known good)
_CONF_ESTIMADO = "estimado"         # histórico emisor sin convocatoria activa
_CONF_PEND     = "pendiente"        # fuente no disponible


# ── Lectura de indicadores ────────────────────────────────────────────────────

def _get_supabase_uri() -> str:
    """Resuelve la URI de Supabase desde Streamlit secrets o config."""
    try:
        import streamlit as st
        return st.secrets.get("database", {}).get("supabase_uri", "")
    except Exception:
        pass
    try:
        import config as cfg
        return getattr(cfg, "SUPABASE_URI", "")
    except ImportError:
        pass
    # Fallback directo (solo dev — en producción usar secrets.toml)
    return (
        "postgresql://postgres.whogonqaadkkyxcnudth:"
        "Z4tilmich3$1"
        "@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"
    )


def _read_gad_indicators() -> dict[str, tuple[Any, str, str]]:
    """Lee los 21 indicadores canónicos del GAD desde todas las fuentes.

    Prioridad por indicador:
        1. Gold Master live  (Gold Master H73_OUTPUT_API — confianza alta)
        2. demo_data.INDICES (último snapshot verificado — confianza media)
        3. None              (fuente no disponible — marcado pendiente_datos)

    Returns:
        dict[codigo] = (valor_actual, confianza, nota_fuente)
        donde confianza ∈ {"alta", "media", "estimado", "pendiente"}
    """
    # ── Intentar Gold Master live ──────────────────────────────────────────
    gm_fin  = {}
    gm_con  = {}
    gm_acc  = {}
    gm_raw  = {}

    try:
        from app.connectors.gold_master import fetch_gold_master_data
        gm_result = fetch_gold_master_data()
        if gm_result["status"] in ("ok", "partial"):
            gm_data = gm_result["data"]
            gm_fin  = gm_data.get("financiero", {})
            gm_con  = gm_data.get("contratacion", {})
            gm_acc  = gm_data.get("accountability", {})
            gm_raw  = gm_data.get("_raw_h73", {})
            logger.info("[Matcher] Gold Master live: OK")
        else:
            logger.warning(f"[Matcher] Gold Master parcial/falla: {gm_result.get('error')}")
    except Exception as exc:
        logger.warning(f"[Matcher] Gold Master no disponible: {exc}")

    # ── Cargar demo_data como fallback ─────────────────────────────────────
    _demo: dict = {}
    try:
        from data.demo_data import INDICES as _INDICES
        _demo = _INDICES
    except Exception as exc:
        logger.warning(f"[Matcher] demo_data no cargable: {exc}")

    def _demo_val(key: str):
        return _demo.get(key, {}).get("valor")

    def _demo_estado(key: str):
        return _demo.get(key, {}).get("estado", "snapshot")

    def _resolve(gm_val, demo_key: str, fuente_gm="Gold Master H73_OUTPUT_API"):
        """Retorna (valor, confianza, fuente) con prioridad GM → demo → None."""
        if gm_val is not None:
            return (gm_val, _CONF_ALTA, fuente_gm)
        dv = _demo_val(demo_key)
        if dv is not None:
            return (dv, _CONF_MEDIA, f"demo_data · {_demo_estado(demo_key)}")
        return (None, _CONF_PEND, "fuente no disponible")

    ind: dict[str, tuple] = {}

    # ── FAMILIA OPERACIONAL (6) — H73_OUTPUT_API ───────────────────────────
    # G-10 (Sprint B): el Gold Master almacena PSG/ISP como FRACCIÓN decimal
    # (0.028 = 2.8%) — regla documentada en BOOT. Los requisitos de fondos
    # están en escala porcentual. Sin esta normalización el matcher comparaba
    # 0.028 contra umbral 20 → brecha -19.97 (falsa). SOLO aplica a PSG/ISP
    # leídos del GM; demo_data ya viene en %.
    def _gm_pct(v):
        return v * 100 if v is not None else None

    # PSG: psg_ejecucion preferido, psg_fidelidad como backup
    # ⚠️ SEMÁNTICA PENDIENTE DE MESA (G-10b): psg_ejecucion (GM, ~2.8%) y
    # PSG display (demo_data, 12.83%) son VARIABLES DISTINTAS (ejecución vs
    # codificado). Decidir contra cuál se evalúan los requisitos de fondos.
    psg_gm = _gm_pct(gm_fin.get("psg_ejecucion") or gm_fin.get("psg_fidelidad"))
    ind["PSG"]  = _resolve(psg_gm, "PSG")

    # ISP: isp_salud_presup
    ind["ISP"]  = _resolve(_gm_pct(gm_fin.get("isp_salud_presup")), "ISP")

    # IGP, IOC, IET, IED: en _raw_h73 con claves a confirmar con Gold Master
    # Si las claves exactas no coinciden devuelven None → demo_data fallback
    igp_gm = (gm_raw.get("IGP_GESTION_PARTICIPATIVA")
               or gm_raw.get("IGP_PART")
               or gm_raw.get("IGP"))
    ind["IGP"]  = _resolve(igp_gm, "IGP")

    ioc_gm = (gm_raw.get("IOC_OBSERVANCIA_CONTRACTUAL")
               or gm_raw.get("IOC_OPACIDAD")
               or gm_raw.get("IOC"))
    ind["IOC"]  = _resolve(ioc_gm, "IOC")

    iet_gm = (gm_raw.get("IET_EQUIDAD_TERRITORIAL")
               or gm_raw.get("IET_INVERSION")
               or gm_raw.get("IET"))
    ind["IET"]  = _resolve(iet_gm, "IET")

    ied_gm = (gm_raw.get("IED_EFICIENCIA_DIRECCIONES")
               or gm_raw.get("IED_EFICIENCIA")
               or gm_raw.get("IED"))
    ind["IED"]  = _resolve(ied_gm, "IED")

    # ── FAMILIA INSTITUCIONAL (6) ──────────────────────────────────────────
    # PAC: Gold Master contratacion.pac_publicado (boolean)
    pac_gm = gm_con.get("pac_publicado")
    ind["PAC_APROBADO"] = (
        (pac_gm, _CONF_ALTA, "Gold Master H73 contratacion.pac_publicado")
        if pac_gm is not None
        else (True, _CONF_MEDIA, "demo_data · asumido vigente")
    )

    # POA: no en Gold Master normalizado — asumido vigente (demo nivel medio)
    ind["POA_APROBADO"] = (True, _CONF_MEDIA, "Asumido vigente · verificar D09")

    # RDC: rdc_score > 0 implica RDC presentada
    rdc_score = gm_acc.get("rdc_score")
    if rdc_score is not None:
        ind["RDC_PRESENTADA"] = (
            rdc_score > 0, _CONF_ALTA, "Gold Master H73 accountability.rdc_score"
        )
    else:
        # Conocimiento directo D09: CPCCS V=0 indica RDC con resultado adverso
        # pero fue presentada → True con confianza media
        ind["RDC_PRESENTADA"] = (True, _CONF_MEDIA, "D09 · CPCCS V=0 · RDC presentada")

    # CPCCS_SIN_OBS: CPCCS Valoración=0 en 2026 → False (tiene observación)
    ind["CPCCS_SIN_OBS"] = (False, _CONF_MEDIA, "CPCCS V=0 · H31_REPORTE_CPCCS · 2026")

    # LOTAIP_VIGENTE, PORTAL_OPERATIVO: D07/Neo4j/DPE — pendiente integración
    ind["LOTAIP_VIGENTE"]   = (None, _CONF_PEND, "D07/Neo4j QTMP — pendiente integración")
    ind["PORTAL_OPERATIVO"] = (None, _CONF_PEND, "DPE API transparencia.dpe.gob.ec — pendiente")

    # ── FAMILIA TERRITORIAL (4) — D05/Supabase + D10 ──────────────────────
    ind["META_PDOT_ASOCIADA"]    = (None, _CONF_PEND, "D05/Supabase corpus C1 — pendiente")
    ind["PDOT_ALINEADO"]         = (None, _CONF_PEND, "D05/Supabase corpus C1 — pendiente")
    ind["PRIORIDAD_TERRITORIAL"] = (None, _CONF_PEND, "D10 parroquias — pendiente")
    ind["PARROQUIA_PRIORIZADA"]  = (None, _CONF_PEND, "D10 parroquias — pendiente")

    # ── FAMILIA GOBERNANZA (5) — D03 + D07/Neo4j ──────────────────────────
    # IFE_A: H73_OUTPUT_API (clave exacta a confirmar) o demo_data
    ife_a_gm = (gm_raw.get("IFE_A_FIDELIDAD")
                or gm_raw.get("IFE_A_CNE")
                or gm_raw.get("H16_IFE")
                or gm_raw.get("IFE_A"))
    ind["IFE_A"] = _resolve(ife_a_gm, "IFE-A", "Gold Master H73 (IFE_A)")

    # ITAM: D07/Neo4j QTMP — demo_data como snapshot
    itam_gm = gm_raw.get("ITAM_TRANSPARENCIA") or gm_raw.get("ITAM")
    ind["ITAM"] = _resolve(itam_gm, "ITAM", "D07/Neo4j QTMP TRANSPARENCIA")

    # D03 gobernanza: IFE-E pendiente Q2-2026, promesas D03/Supabase
    ind["PROMESA_CNE"]           = (None, _CONF_PEND, "D03/Supabase IFE_CNE — pendiente")
    ind["META_INST_FORMALIZADA"] = (None, _CONF_PEND, "D03 MNT_UUID — pendiente")
    ind["EVIDENCIA_EJECUCION"]   = (None, _CONF_PEND, "D03/IFE-E POA→PAC→eSIGEF — Q2-2026")

    # Log resumen
    live   = sum(1 for v, c, _ in ind.values() if c in (_CONF_ALTA, _CONF_MEDIA))
    pend   = sum(1 for v, c, _ in ind.values() if c == _CONF_PEND)
    logger.info(f"[Matcher] Indicadores: {live} disponibles · {pend} pendientes")

    return ind


# ── Evaluación de requisitos ──────────────────────────────────────────────────

def _evaluate_req(
    valor_actual: Any,
    operador: str,
    umbral: float | None,
    umbral_enum: list | None,
) -> tuple[bool, float | None]:
    """Evalúa si valor_actual cumple el requisito.

    Returns:
        (cumple, gap)
        gap: float positivo = cuánto falta para cumplir. None si no aplica.
    """
    if valor_actual is None:
        return False, None      # pendiente_datos — manejado antes de llamar

    if operador == "eq_true":
        return bool(valor_actual), None

    if operador == "exists":
        return valor_actual is not None, None

    if operador == "in":
        return valor_actual in (umbral_enum or []), None

    # Operadores numéricos
    try:
        v = float(valor_actual)
        t = float(umbral) if umbral is not None else 0.0
    except (TypeError, ValueError):
        logger.warning(f"[Matcher] No se pudo convertir a float: val={valor_actual} umbral={umbral}")
        return False, None

    if operador == "gte":
        cumple = v >= t
        return cumple, round(max(0.0, t - v), 4)
    if operador == "lte":
        cumple = v <= t
        return cumple, round(max(0.0, v - t), 4)
    if operador == "gt":
        cumple = v > t
        return cumple, round(max(0.0, t - v), 4)
    if operador == "lt":
        cumple = v < t
        return cumple, round(max(0.0, v - t), 4)
    if operador == "eq":
        cumple = abs(v - t) < 1e-6
        return cumple, round(abs(v - t), 4)

    logger.warning(f"[Matcher] Operador desconocido: {operador}")
    return False, None


# ── Match de una convocatoria ─────────────────────────────────────────────────

def match_convocatoria(
    conv_id: int,
    requirements: list[dict],
    gad_indicators: dict[str, tuple],
    monto_ref_usd: int | None,
) -> dict:
    """Evalúa una convocatoria contra los indicadores actuales del GAD.

    Args:
        conv_id:       ID de la convocatoria en Supabase
        requirements:  filas de fondos_conv_requisitos JOIN fondos_requisitos
        gad_indicators: output de _read_gad_indicators()
        monto_ref_usd: monto_max_usd de la convocatoria (referencia)

    Returns:
        dict con estado_quira, brechas_json, potencial_usd, monto_confianza,
        indicadores_json para UPSERT en fondos_elegibilidad.
    """
    brechas: dict[str, float] = {}      # código → gap negativo (cuánto falta)
    pendientes: list[str] = []
    critico_fallido = False
    non_critico_gap = False
    snapshot: dict[str, Any] = {}

    for req in requirements:
        codigo   = req["codigo"]
        operador = req["operador"]
        umbral   = req.get("valor")
        enum_    = req.get("valor_enum")
        critico  = req.get("es_critico", True)

        ind_tuple = gad_indicators.get(codigo, (None, _CONF_PEND, "no mapeado"))
        valor_actual, confianza, fuente = ind_tuple
        snapshot[codigo] = valor_actual

        if valor_actual is None:
            pendientes.append(codigo)
            if critico:
                logger.debug(f"[Matcher] {codigo} pendiente (crítico) → pendiente_datos")
            continue

        cumple, gap = _evaluate_req(valor_actual, operador, umbral, enum_)

        if not cumple:
            if critico:
                critico_fallido = True
                logger.debug(f"[Matcher] {codigo} FALLA crítico: {valor_actual} {operador} {umbral}")
            else:
                non_critico_gap = True
                logger.debug(f"[Matcher] {codigo} brecha no crítica: {valor_actual} {operador} {umbral}")

            # Registrar brecha como valor negativo (cuánto falta)
            if gap is not None and gap > 0:
                brechas[codigo] = round(-gap, 4)

    # ── Determinar estado ──────────────────────────────────────────────────
    # Jerarquía: no_elegible > pendiente_datos > elegible_con_brecha > elegible_hoy
    if critico_fallido:
        estado = "no_elegible"
    elif pendientes:
        estado = "pendiente_datos"
    elif non_critico_gap:
        estado = "elegible_con_brecha"
    else:
        estado = "elegible_hoy"

    # ── Confianza del monto ────────────────────────────────────────────────
    if estado == "no_elegible":
        monto_pot  = None
        monto_conf = None
    elif estado == "elegible_hoy":
        monto_pot  = monto_ref_usd
        monto_conf = _CONF_ALTA if monto_ref_usd else _CONF_ESTIMADO
    else:
        monto_pot  = monto_ref_usd
        monto_conf = _CONF_MEDIA if monto_ref_usd else _CONF_ESTIMADO

    return {
        "convocatoria_id":  conv_id,
        "estado_quira":     estado,
        "brechas_json":     brechas,
        "potencial_usd":    monto_pot,
        "monto_confianza":  monto_conf,
        "indicadores_json": snapshot,
    }


# ── Entry point principal ─────────────────────────────────────────────────────

def run_matcher(gad_id: str = GAD_ID_DEFAULT) -> dict:
    """Motor de Elegibilidad D02 — entrada principal.

    1. Lee indicadores del GAD desde Gold Master + demo_data.
    2. Consulta convocatorias activas (abierta|recurrente) + sus requisitos.
    3. Evalúa cada convocatoria y calcula estado_quira, brechas, potencial_usd.
    4. Hace UPSERT en Supabase fondos_elegibilidad.

    Returns:
        summary dict:
            status, gad_id, matched, computed_at, breakdown, total_potencial_usd
    """
    import psycopg2
    import psycopg2.extras

    logger.info(f"[Matcher] ──── Inicio · GAD {gad_id} ────")

    # -- Leer indicadores --
    gad_indicators = _read_gad_indicators()

    # -- Conectar Supabase --
    uri = _get_supabase_uri()
    if not uri:
        return {"status": "error", "error": "SUPABASE_URI no disponible", "matched": 0}

    try:
        conn = psycopg2.connect(uri, sslmode="require", connect_timeout=15)
    except Exception as exc:
        return {"status": "error", "error": f"Conexión Supabase: {exc}", "matched": 0}

    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # -- Convocatorias activas + requisitos --
    cur.execute("""
        SELECT
            c.id              AS conv_id,
            c.codigo          AS conv_codigo,
            c.nombre          AS conv_nombre,
            c.monto_max_usd   AS monto_ref,
            r.codigo          AS codigo,
            r.nombre_publico  AS nombre_publico,
            r.familia         AS familia,
            cr.operador,
            cr.valor,
            cr.valor_enum,
            cr.es_critico
        FROM fondos_convocatorias c
        JOIN fondos_conv_requisitos cr ON cr.convocatoria_id = c.id
        JOIN fondos_requisitos r       ON r.id = cr.requisito_id
        WHERE c.estado IN ('abierta', 'recurrente')
        AND   r.activo = true
        ORDER BY c.id, r.familia, r.codigo
    """)
    rows = cur.fetchall()

    if not rows:
        logger.info("[Matcher] Sin convocatorias activas — nada que evaluar")
        conn.close()
        return {
            "status": "ok",
            "gad_id": gad_id,
            "matched": 0,
            "message": "Sin convocatorias activas en Supabase",
            "breakdown": {},
            "total_potencial_usd": 0,
        }

    # Agrupar por convocatoria
    conv_map: dict[int, dict] = defaultdict(lambda: {
        "nombre": "", "codigo": "", "monto_ref": None, "reqs": []
    })
    for row in rows:
        cid = row["conv_id"]
        conv_map[cid]["nombre"]    = row["conv_nombre"]
        conv_map[cid]["codigo"]    = row["conv_codigo"]
        conv_map[cid]["monto_ref"] = row["monto_ref"]
        conv_map[cid]["reqs"].append(dict(row))

    # -- Evaluar --
    results = []
    now = datetime.now(timezone.utc)

    for conv_id, conv_data in conv_map.items():
        result = match_convocatoria(
            conv_id       = conv_id,
            requirements  = conv_data["reqs"],
            gad_indicators= gad_indicators,
            monto_ref_usd = conv_data["monto_ref"],
        )
        result["gad_id"]      = gad_id
        result["computed_at"] = now
        results.append(result)

        pot = result["potencial_usd"] or 0
        logger.info(
            f"[Matcher]  {conv_data['codigo']:30s}  "
            f"{result['estado_quira']:22s}  "
            f"USD {pot:>12,}  "
            f"brechas={list(result['brechas_json'].keys())}"
        )

    # -- UPSERT fondos_elegibilidad --
    _UPSERT = """
        INSERT INTO fondos_elegibilidad
            (convocatoria_id, gad_id, estado_quira, brechas_json,
             potencial_usd, monto_confianza, indicadores_json, computed_at)
        VALUES
            (%(convocatoria_id)s, %(gad_id)s, %(estado_quira)s,
             %(brechas_json)s::jsonb, %(potencial_usd)s, %(monto_confianza)s,
             %(indicadores_json)s::jsonb, %(computed_at)s)
        ON CONFLICT (convocatoria_id, gad_id) DO UPDATE SET
            estado_quira     = EXCLUDED.estado_quira,
            brechas_json     = EXCLUDED.brechas_json,
            potencial_usd    = EXCLUDED.potencial_usd,
            monto_confianza  = EXCLUDED.monto_confianza,
            indicadores_json = EXCLUDED.indicadores_json,
            computed_at      = EXCLUDED.computed_at
    """
    for r in results:
        cur.execute(_UPSERT, {
            **r,
            "brechas_json":     json.dumps(r["brechas_json"]),
            "indicadores_json": json.dumps(r["indicadores_json"]),
        })

    conn.commit()
    cur.close()
    conn.close()

    # -- Summary --
    breakdown = {
        "elegible_hoy":        sum(1 for r in results if r["estado_quira"] == "elegible_hoy"),
        "elegible_con_brecha": sum(1 for r in results if r["estado_quira"] == "elegible_con_brecha"),
        "no_elegible":         sum(1 for r in results if r["estado_quira"] == "no_elegible"),
        "pendiente_datos":     sum(1 for r in results if r["estado_quira"] == "pendiente_datos"),
    }
    total_pot = sum(r["potencial_usd"] or 0 for r in results)

    summary = {
        "status":             "ok",
        "gad_id":             gad_id,
        "matched":            len(results),
        "computed_at":        now.isoformat(),
        "breakdown":          breakdown,
        "total_potencial_usd": total_pot,
    }

    logger.info(
        f"[Matcher] ──── FIN · {len(results)} convocatorias · "
        f"USD {total_pot:,} potencial · "
        f"elegible={breakdown['elegible_hoy']} · "
        f"brecha={breakdown['elegible_con_brecha']} · "
        f"no_elegible={breakdown['no_elegible']} ────"
    )
    return summary


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )
    gad = sys.argv[1] if len(sys.argv) > 1 else GAD_ID_DEFAULT
    result = run_matcher(gad)
    print(json.dumps(result, indent=2, default=str))
