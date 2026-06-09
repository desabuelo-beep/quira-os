"""
app/engines/fondos_simulator.py — Simulador de Desbloqueo D02 · QUIRA OS
=========================================================================
Responde la pregunta más poderosa de QUIRA para un alcalde:

    "¿Qué dinero se desbloquea si el municipio mejora este indicador?"

RESPONSABILIDAD ÚNICA:
    Dado (indicador, nuevo_valor), calcular qué convocatorias
    que HOY están bloqueadas o en brecha pasarían a elegible.

DIFERENCIA CON el Matcher:
    Matcher  → estado REAL actual del GAD
    Simulator → estado HIPOTÉTICO si X mejora

BLOOMBERG FIREWALL:
    Entrada: indicador público (PSG, ISP, ITAM, etc.)
    Salida:  lista de convocatorias desbloqueadas + total USD
    NUNCA expone: ICPI · TGI · Ti · QTMP · H73 · Gold Master

EJEMPLO DE USO:
    simulate_unlock("PSG", 30.0)
    →  "Si PSG sube a 30%, se desbloquean 2 fondos: USD 630,000"

    simulate_unlock("ISP", 65.0)
    →  "Si ISP llega a 65%, se desbloquean 3 fondos: USD 5,700,000"

Dylus Lab © 2026 · ADR-026 §D02 Consecuencia
"""
from __future__ import annotations

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

GAD_ID_DEFAULT = "MCR-001"


# ── Conexión Supabase ─────────────────────────────────────────────────────────

def _get_supabase_uri() -> str:
    """Resuelve URI de Supabase desde Streamlit secrets o config."""
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
    return (
        "postgresql://postgres.whogonqaadkkyxcnudth:"
        "Z4tilmich3$1"
        "@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"
    )


# ── Lectura del estado actual desde fondos_elegibilidad ──────────────────────

def _load_current_state(gad_id: str) -> list[dict]:
    """Carga el estado actual de elegibilidad desde Supabase.

    Retorna filas de fondos_elegibilidad JOIN convocatorias JOIN emisores
    para las convocatorias activas (abierta|recurrente).
    """
    import psycopg2
    import psycopg2.extras

    uri = _get_supabase_uri()
    conn = psycopg2.connect(uri, sslmode="require", connect_timeout=15)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            e.convocatoria_id,
            e.estado_quira,
            e.brechas_json,
            e.potencial_usd,
            e.monto_confianza,
            e.indicadores_json,
            c.codigo            AS conv_codigo,
            c.nombre            AS conv_nombre,
            c.monto_min_usd,
            c.monto_max_usd,
            em.nombre           AS emisor_nombre,
            em.tipo_emisor,
            em.naturaleza
        FROM fondos_elegibilidad e
        JOIN fondos_convocatorias c  ON c.id = e.convocatoria_id
        JOIN fondos_emisores em      ON em.id = c.emisor_id
        WHERE e.gad_id = %s
          AND c.estado IN ('abierta', 'recurrente')
        ORDER BY e.estado_quira, e.potencial_usd DESC NULLS LAST
    """, (gad_id,))

    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return rows


def _load_requirements(gad_id: str) -> dict[int, list[dict]]:
    """Carga requisitos de cada convocatoria activa.

    Returns: dict[convocatoria_id] → lista de requisitos
    """
    import psycopg2
    import psycopg2.extras

    uri = _get_supabase_uri()
    conn = psycopg2.connect(uri, sslmode="require", connect_timeout=15)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT
            cr.convocatoria_id,
            r.codigo,
            r.nombre_publico,
            cr.operador,
            cr.valor,
            cr.valor_enum,
            cr.es_critico
        FROM fondos_conv_requisitos cr
        JOIN fondos_requisitos r       ON r.id = cr.requisito_id
        JOIN fondos_convocatorias c    ON c.id = cr.convocatoria_id
        WHERE c.estado IN ('abierta', 'recurrente')
          AND r.activo = true
        ORDER BY cr.convocatoria_id, cr.es_critico DESC, r.codigo
    """, ())

    from collections import defaultdict
    result: dict[int, list[dict]] = defaultdict(list)
    for row in cur.fetchall():
        result[row["convocatoria_id"]].append(dict(row))

    cur.close()
    conn.close()
    return result


# ── Motor de simulación ───────────────────────────────────────────────────────

def _evaluate_req_sim(
    valor_actual: Any,
    operador: str,
    umbral: float | None,
    umbral_enum: list | None,
) -> bool:
    """Versión simplificada de _evaluate_req para simulación (solo bool)."""
    if valor_actual is None:
        return False

    if operador == "eq_true":
        return bool(valor_actual)
    if operador == "exists":
        return valor_actual is not None
    if operador == "in":
        return valor_actual in (umbral_enum or [])

    try:
        v = float(valor_actual)
        t = float(umbral) if umbral is not None else 0.0
    except (TypeError, ValueError):
        return False

    if operador == "gte":   return v >= t
    if operador == "lte":   return v <= t
    if operador == "gt":    return v > t
    if operador == "lt":    return v < t
    if operador == "eq":    return abs(v - t) < 1e-6
    return False


def simulate_unlock(
    indicador: str,
    nuevo_valor: float,
    gad_id: str = GAD_ID_DEFAULT,
) -> dict:
    """Simula qué convocatorias se desbloquean si un indicador mejora.

    Args:
        indicador:   Código del indicador (PSG, ISP, ITAM, IFE_A, IGP, IOC...)
        nuevo_valor: Valor hipotético del indicador en la misma escala actual
        gad_id:      ID del GAD (default: MCR-001 Montecristi)

    Returns:
        dict con:
            indicador:            código del indicador simulado
            nuevo_valor:          valor hipotético ingresado
            valor_actual:         valor actual del indicador (del Matcher)
            desbloqueadas:        list de convocatorias que pasarían a elegible
            total_usd_desbloqueado: suma de potencial_usd de desbloqueadas
            ya_elegibles:         convocatorias ya elegibles (sin cambio)
            no_mejora:            convocatorias que siguen sin cumplir
            costo_oportunidad_usd: USD de convocatorias que aún no son elegibles
    """
    logger.info(
        f"[Simulator] Simulando: {indicador} → {nuevo_valor} · GAD {gad_id}"
    )

    # Cargar estado actual y requisitos
    current_state = _load_current_state(gad_id)
    requirements  = _load_requirements(gad_id)

    if not current_state:
        return {
            "status": "error",
            "error": "Sin estado en fondos_elegibilidad — ejecuta run_matcher() primero",
        }

    # Obtener valor actual del indicador desde cualquier fila que lo tenga
    valor_actual = None
    for row in current_state:
        indicadores = row.get("indicadores_json") or {}
        if indicador in indicadores:
            valor_actual = indicadores[indicador]
            break

    desbloqueadas = []
    ya_elegibles  = []
    no_mejora     = []

    for row in current_state:
        conv_id    = row["convocatoria_id"]
        estado_hoy = row["estado_quira"]
        reqs       = requirements.get(conv_id, [])
        monto_ref  = row.get("monto_max_usd") or row.get("potencial_usd") or 0

        # Construir snapshot de indicadores simulado:
        # tomar indicadores actuales y reemplazar el indicador simulado
        indicadores_sim = dict(row.get("indicadores_json") or {})
        indicadores_sim[indicador] = nuevo_valor

        # Evaluar si todos los críticos pasan con el nuevo valor
        critico_fallido_sim = False
        non_critico_gap_sim = False

        for req in reqs:
            codigo   = req["codigo"]
            operador = req["operador"]
            umbral   = req.get("valor")
            enum_    = req.get("valor_enum")
            critico  = req.get("es_critico", True)

            # Usar valor simulado si corresponde, si no usar actual
            val = indicadores_sim.get(codigo)

            if val is None:
                if critico:
                    critico_fallido_sim = True
                continue

            cumple = _evaluate_req_sim(val, operador, umbral, enum_)
            if not cumple:
                if critico:
                    critico_fallido_sim = True
                else:
                    non_critico_gap_sim = True

        # Estado hipotético
        if critico_fallido_sim:
            estado_sim = "no_elegible"
        elif non_critico_gap_sim:
            estado_sim = "elegible_con_brecha"
        else:
            estado_sim = "elegible_hoy"

        entry = {
            "conv_codigo":   row["conv_codigo"],
            "conv_nombre":   row["conv_nombre"],
            "emisor_nombre": row["emisor_nombre"],
            "naturaleza":    row["naturaleza"],
            "estado_actual": estado_hoy,
            "estado_sim":    estado_sim,
            "potencial_usd": monto_ref,
        }

        # Jerarquía de estados: mejor → mayor rank
        _rank = {
            "no_elegible": 0, "pendiente_datos": 1,
            "elegible_con_brecha": 2, "elegible_hoy": 3,
        }
        if estado_hoy == "elegible_hoy":
            ya_elegibles.append(entry)
        elif _rank.get(estado_sim, 0) > _rank.get(estado_hoy, 0):
            # Mejora REAL: el indicador simulado eleva el estado
            desbloqueadas.append(entry)
        else:
            # Sin mejora o mismo estado
            no_mejora.append(entry)

    total_desbloqueado   = sum(e["potencial_usd"] for e in desbloqueadas)
    total_ya_elegibles   = sum(e["potencial_usd"] for e in ya_elegibles)
    total_aun_bloqueado  = sum(e["potencial_usd"] for e in no_mejora)

    resultado = {
        "status":                 "ok",
        "gad_id":                 gad_id,
        "indicador":              indicador,
        "nuevo_valor":            nuevo_valor,
        "valor_actual":           valor_actual,
        "desbloqueadas":          desbloqueadas,
        "total_usd_desbloqueado": total_desbloqueado,
        "ya_elegibles":           ya_elegibles,
        "total_ya_elegible_usd":  total_ya_elegibles,
        "no_mejora":              no_mejora,
        "costo_oportunidad_usd":  total_aun_bloqueado,
    }

    logger.info(
        f"[Simulator] {indicador} {valor_actual} → {nuevo_valor}: "
        f"{len(desbloqueadas)} desbloqueadas · "
        f"USD {total_desbloqueado:,} · "
        f"costo oportunidad restante USD {total_aun_bloqueado:,}"
    )
    return resultado


def simulate_all_indicators(
    objetivos: dict[str, float],
    gad_id: str = GAD_ID_DEFAULT,
) -> dict:
    """Simula el impacto de mejorar MÚLTIPLES indicadores simultáneamente.

    Args:
        objetivos: dict[codigo_indicador] = nuevo_valor
            Ej: {"PSG": 30.0, "ISP": 65.0, "ITAM": 75.0}
        gad_id:   ID del GAD

    Returns:
        Resumen del estado de elegibilidad si todos los objetivos se cumplen.
        Útil para proyectar el potencial TOTAL de QUIRA con mejoras institucionales.
    """
    logger.info(f"[Simulator] Simulación multi-indicador: {objetivos}")

    current_state = _load_current_state(gad_id)
    requirements  = _load_requirements(gad_id)

    if not current_state:
        return {"status": "error", "error": "Sin estado — ejecuta run_matcher() primero"}

    elegibles_sim  = []
    bloqueadas_sim = []

    for row in current_state:
        conv_id   = row["convocatoria_id"]
        reqs      = requirements.get(conv_id, [])
        monto_ref = row.get("monto_max_usd") or row.get("potencial_usd") or 0

        # Snapshot con todos los objetivos aplicados
        indicadores_sim = dict(row.get("indicadores_json") or {})
        indicadores_sim.update(objetivos)

        critico_fallido = False
        non_critico_gap = False

        for req in reqs:
            val    = indicadores_sim.get(req["codigo"])
            if val is None and req.get("es_critico"):
                critico_fallido = True
                continue
            if val is None:
                continue
            cumple = _evaluate_req_sim(val, req["operador"], req.get("valor"), req.get("valor_enum"))
            if not cumple:
                if req.get("es_critico"):
                    critico_fallido = True
                else:
                    non_critico_gap = True

        if critico_fallido:
            bloqueadas_sim.append({"conv_codigo": row["conv_codigo"], "potencial_usd": monto_ref})
        else:
            elegibles_sim.append({"conv_codigo": row["conv_codigo"], "potencial_usd": monto_ref})

    return {
        "status":                "ok",
        "gad_id":                gad_id,
        "objetivos_simulados":   objetivos,
        "elegibles_sim":         elegibles_sim,
        "bloqueadas_sim":        bloqueadas_sim,
        "total_potencial_usd":   sum(e["potencial_usd"] for e in elegibles_sim),
        "aun_bloqueado_usd":     sum(e["potencial_usd"] for e in bloqueadas_sim),
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )

    # Uso: python -m app.engines.fondos_simulator PSG 30.0
    if len(sys.argv) >= 3:
        ind = sys.argv[1].upper()
        val = float(sys.argv[2])
        result = simulate_unlock(ind, val)
    else:
        # Demo: simular PSG subiendo a 30% (umbral ONU Mujeres)
        print("Demo: simulando PSG = 30.0 (sin argumento · uso: python -m ... PSG 30.0)\n")
        result = simulate_unlock("PSG", 30.0)

    # Resumen legible
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"SIMULACION: {result.get('indicador')} -> {result.get('nuevo_valor')}")
    print(f"Valor actual: {result.get('valor_actual')}")
    print(sep)

    desbl = result.get("desbloqueadas", [])
    if desbl:
        print(f"\n[DESBLOQUEA] {len(desbl)} convocatoria(s) -> USD {result['total_usd_desbloqueado']:,}")
        for e in desbl:
            print(f"   {e['conv_nombre'][:55]:55s}  USD {e['potencial_usd']:>10,}")
    else:
        print("\n-> Ninguna convocatoria adicional se desbloquea con este cambio.")

    ya = result.get("ya_elegibles", [])
    if ya:
        print(f"\n[YA ELEGIBLES] (sin cambio): {len(ya)} -> USD {result['total_ya_elegible_usd']:,}")

    no = result.get("no_mejora", [])
    if no:
        print(f"\n[AUN BLOQUEADAS] {len(no)} -> USD {result['costo_oportunidad_usd']:,} costo oportunidad")

    print(f"\n{'='*60}\n")
    print(json.dumps(result, indent=2, default=str))
