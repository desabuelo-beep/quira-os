"""
app/fetchers/fondos_radar_runner.py — Orquestador /fondos-radar · QUIRA OS
===========================================================================
ADR-026 §D02.2 · Fetcher Layer · Dylus Lab © 2026

RESPONSABILIDAD ÚNICA:
    Orquestar el pipeline completo de descubrimiento de fondos.
    No fetcha, no normaliza — coordina.

PIPELINE (Colega v3 — con staging obligatorio):
    Adapter → Normalizer → Staging → Validator → Insert → Run Matcher

BLOOMBERG FIREWALL:
    Output público: convocatoria nombre, monto, emisor (lenguaje de gobernanza).
    NUNCA en output: ICPI · TGI · H73 · Gold Master · node IDs internos.

USO:
    CLI:        python -m app.fetchers.fondos_radar_runner [opciones]
    Skill:      invocado automáticamente por /fondos-radar
    Streamlit:  from app.fetchers.fondos_radar_runner import run_fondos_radar

OPCIONES CLI:
    --mode demo|live     (default: demo)
    --fuentes PNUD,BID   (default: todas las activas)
    --dry-run            (no hace INSERT, solo muestra qué insertaría)
    --no-haiku           (usa fallback heurístico en vez de Haiku)
    --gad-id MCR-001     (default: MCR-001)
"""
from __future__ import annotations

import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

GAD_ID_DEFAULT = "MCR-001"

# Registro de adaptadores disponibles
# Agregar aquí nuevos adaptadores sin tocar el runner
ADAPTERS_REGISTRY = {
    "PNUD":  "app.fetchers.adapter_pnud.AdapterPNUD",
    "BID":   "app.fetchers.adapter_bid.AdapterBID",
    "AECID": "app.fetchers.adapter_aecid.AdapterAECID",
}


# ── Pipeline principal ─────────────────────────────────────────────────────────

def run_fondos_radar(
    fuentes:    list[str]  = None,
    mode:       str        = "demo",
    dry_run:    bool       = False,
    use_haiku:  bool       = True,
    gad_id:     str        = GAD_ID_DEFAULT,
) -> dict:
    """
    Pipeline completo: Adapter → Normalizer → Staging → Validator → Insert
                       → Update fondos_fuentes → Run Matcher.

    Args:
        fuentes:   Lista de códigos de fuente ('PNUD', 'BID', 'AECID').
                   None = todas las registradas.
        mode:      'demo' (sin HTTP) | 'live' (fetch real).
        dry_run:   True = solo simula, no hace INSERT ni actualiza DB.
        use_haiku: True = usa Haiku para normalizar.
        gad_id:    ID del GAD para recalcular el Matcher.

    Returns:
        Resumen completo del pipeline con métricas por fuente.
    """
    t_inicio = time.time()
    fuentes  = fuentes or list(ADAPTERS_REGISTRY.keys())

    logger.info(
        f"[FondosRadar] Iniciando pipeline · fuentes={fuentes} "
        f"· mode={mode} · dry_run={dry_run}"
    )

    # Conexión Supabase (una sola para todo el pipeline)
    conn = None if dry_run else _get_db_connection()

    # Mapa de emisores para resolver emisor_codigo → id
    emisores_map = {} if dry_run else _load_emisores_map(conn)

    summary = {
        "fuentes_procesadas": [],
        "total_raw":          0,
        "total_normalizados": 0,
        "total_validos":      0,
        "total_insertados":   0,
        "total_duplicados":   0,
        "total_errores":      0,
        "convocatorias_nuevas": [],
        "dry_run":            dry_run,
        "mode":               mode,
        "duracion_s":         0,
    }

    for fuente_codigo in fuentes:
        fuente_summary = _process_fuente(
            fuente_codigo = fuente_codigo,
            mode          = mode,
            dry_run       = dry_run,
            use_haiku     = use_haiku,
            conn          = conn,
            emisores_map  = emisores_map,
            gad_id        = gad_id,
        )
        summary["fuentes_procesadas"].append(fuente_summary)
        summary["total_raw"]        += fuente_summary["raw"]
        summary["total_normalizados"]+= fuente_summary["normalizados"]
        summary["total_validos"]    += fuente_summary["validos"]
        summary["total_insertados"] += fuente_summary["insertados"]
        summary["total_duplicados"] += fuente_summary["duplicados"]
        summary["total_errores"]    += fuente_summary["errores"]
        summary["convocatorias_nuevas"].extend(fuente_summary["nuevas"])

    # Recalcular Matcher si hubo inserciones reales
    matcher_result = None
    if not dry_run and summary["total_insertados"] > 0:
        logger.info(
            f"[FondosRadar] {summary['total_insertados']} inserciones nuevas "
            f"→ recalculando Matcher para {gad_id}"
        )
        try:
            from app.engines.fondos_matcher import run_matcher
            matcher_result = run_matcher(gad_id)
            summary["matcher_recalculado"] = True
            summary["matcher_summary"] = {
                "elegible_hoy":        matcher_result["breakdown"].get("elegible_hoy", 0),
                "elegible_con_brecha": matcher_result["breakdown"].get("elegible_con_brecha", 0),
                "no_elegible":         matcher_result["breakdown"].get("no_elegible", 0),
                "total_potencial_usd": matcher_result.get("total_potencial_usd", 0),
            }
        except Exception as exc:
            logger.error(f"[FondosRadar] Error recalculando Matcher: {exc}")
            summary["matcher_error"] = str(exc)
    else:
        summary["matcher_recalculado"] = False

    if conn:
        conn.close()

    summary["duracion_s"] = round(time.time() - t_inicio, 2)
    logger.info(
        f"[FondosRadar] Pipeline completo · "
        f"{summary['total_insertados']} insertados · "
        f"{summary['total_duplicados']} duplicados · "
        f"{summary['duracion_s']}s"
    )
    return summary


# ── Procesar una fuente ────────────────────────────────────────────────────────

def _process_fuente(
    fuente_codigo: str,
    mode:          str,
    dry_run:       bool,
    use_haiku:     bool,
    conn,
    emisores_map:  dict,
    gad_id:        str,
) -> dict:
    """Ejecuta el pipeline completo para una sola fuente."""
    from app.fetchers.fondos_normalizer import normalize_raw_fund, validate_canonical

    result = {
        "fuente":       fuente_codigo,
        "raw":          0,
        "normalizados": 0,
        "validos":      0,
        "insertados":   0,
        "duplicados":   0,
        "errores":      0,
        "nuevas":       [],
        "error_msg":    None,
        "duracion_ms":  0,
    }

    t0 = time.time()

    # ── 1. Cargar adaptador ────────────────────────────────────────────────────
    adapter = _load_adapter(fuente_codigo)
    if adapter is None:
        result["error_msg"] = f"Adaptador '{fuente_codigo}' no encontrado"
        result["errores"] = 1
        return result

    # ── 2. Fetch raw ──────────────────────────────────────────────────────────
    raw_list = adapter.fetch(mode=mode)
    result["raw"] = len(raw_list)

    if not raw_list:
        result["error_msg"] = adapter.error_msg or "fetch retornó vacío"
        if not dry_run and conn:
            _update_fuente_status(conn, fuente_codigo, "error", 0, 0,
                                  result["error_msg"], adapter.duracion_ms)
        return result

    # ── 3. Normalizar (Staging en memoria) ────────────────────────────────────
    staging: list = []
    for raw in raw_list:
        try:
            canonical = normalize_raw_fund(raw, use_haiku=use_haiku)
            if canonical:
                staging.append(canonical)
                result["normalizados"] += 1
            else:
                logger.debug(f"[{fuente_codigo}] Normalizer descartó un item")
        except Exception as exc:
            logger.warning(f"[{fuente_codigo}] Error normalizando: {exc}")
            result["errores"] += 1

    # ── 4. Validar ─────────────────────────────────────────────────────────────
    validos: list = []
    for canonical in staging:
        ok, errs = validate_canonical(canonical)
        if ok:
            validos.append(canonical)
            result["validos"] += 1
        else:
            logger.warning(
                f"[{fuente_codigo}] Validación fallida para "
                f"'{canonical.nombre[:60]}': {errs}"
            )
            result["errores"] += 1

    # ── 5. Insert (deduplicado) ────────────────────────────────────────────────
    for canonical in validos:
        if dry_run:
            # Solo reportar qué se insertaría
            result["insertados"] += 1
            result["nuevas"].append({
                "nombre":        canonical.nombre,
                "emisor_codigo": canonical.emisor_codigo,
                "monto_max_usd": canonical.monto_max_usd,
                "confidence":    canonical.confidence,
            })
            continue

        insert_result = _insert_canonical(conn, canonical, emisores_map, fuente_codigo)
        if insert_result == "inserted":
            result["insertados"] += 1
            result["nuevas"].append({
                "nombre":        canonical.nombre,
                "emisor_codigo": canonical.emisor_codigo,
                "monto_max_usd": canonical.monto_max_usd,
                "confidence":    canonical.confidence,
            })
        elif insert_result == "duplicate":
            result["duplicados"] += 1
            # Registrar en historial que fue vista sin cambio
            _log_historial(conn, None, canonical.nombre, "detectada_sin_cambio",
                           fuente_codigo, canonical.confidence, canonical.raw_snippet)
        else:
            result["errores"] += 1

    # ── 6. Actualizar fondos_fuentes ──────────────────────────────────────────
    if not dry_run and conn:
        estado = "ok" if result["errores"] == 0 else (
            "parcial" if result["insertados"] > 0 else "error"
        )
        _update_fuente_status(
            conn, fuente_codigo, estado,
            result["raw"], result["insertados"],
            error_msg   = result["error_msg"],
            duracion_ms = int((time.time() - t0) * 1000),
        )

    result["duracion_ms"] = int((time.time() - t0) * 1000)
    return result


# ── Helpers DB ─────────────────────────────────────────────────────────────────

def _get_db_connection():
    """Resuelve URI de Supabase y retorna conexión psycopg2."""
    import psycopg2
    uri = ""
    try:
        import streamlit as st
        uri = st.secrets.get("database", {}).get("supabase_uri", "")
    except Exception:
        pass
    if not uri:
        try:
            import config as cfg
            uri = getattr(cfg, "SUPABASE_URI", "")
        except ImportError:
            pass
    conn = psycopg2.connect(uri, sslmode="require", connect_timeout=20)
    conn.autocommit = True
    return conn


def _load_emisores_map(conn) -> dict:
    """Carga mapping codigo → id de fondos_emisores."""
    import psycopg2.extras
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, codigo FROM fondos_emisores WHERE activo = TRUE")
    result = {r["codigo"]: r["id"] for r in cur.fetchall()}
    cur.close()
    return result


def _insert_canonical(conn, canonical, emisores_map: dict, fuente_codigo: str) -> str:
    """
    Inserta FondoCanonical en fondos_convocatorias si no existe duplicado.

    Deduplicación: nombre normalizado + emisor_id.
    Si ya existe → retorna 'duplicate'.
    Si insertó → retorna 'inserted'.
    Si error → retorna 'error'.
    """
    import psycopg2

    emisor_id = emisores_map.get(canonical.emisor_codigo)
    if not emisor_id:
        logger.warning(
            f"[Insert] emisor_codigo '{canonical.emisor_codigo}' no encontrado "
            f"en fondos_emisores. Skipping."
        )
        return "error"

    # Generar código único: EMISOR-HASH4-AÑO
    nombre_hash = hashlib.md5(
        canonical.nombre.lower().strip().encode()
    ).hexdigest()[:4].upper()
    año         = datetime.now().year
    codigo      = f"{canonical.emisor_codigo}-{nombre_hash}-{año}"

    cur = conn.cursor()
    try:
        # Verificar duplicado por código
        cur.execute(
            "SELECT id FROM fondos_convocatorias WHERE codigo = %s",
            (codigo,)
        )
        if cur.fetchone():
            cur.close()
            return "duplicate"

        # INSERT
        cur.execute("""
            INSERT INTO fondos_convocatorias
                (codigo, emisor_id, nombre, estado,
                 monto_min_usd, monto_max_usd, moneda,
                 elegibles, temas, url, descripcion,
                 fecha_cierre, fecha_apertura,
                 snapshot_date, proxima_revision)
            VALUES
                (%s, %s, %s, %s,
                 %s, %s, %s,
                 %s, %s, %s, %s,
                 %s, %s,
                 CURRENT_DATE, CURRENT_DATE + 30)
            RETURNING id
        """, (
            codigo,
            emisor_id,
            canonical.nombre,
            canonical.estado,
            canonical.monto_min_usd,
            canonical.monto_max_usd,
            canonical.moneda or "USD",
            canonical.elegibles or [],
            canonical.temas or [],
            canonical.url,
            canonical.descripcion,
            canonical.fecha_cierre,
            canonical.fecha_inicio,   # fecha_apertura en DB
        ))

        conv_id = cur.fetchone()[0]
        cur.close()

        # Registrar en historial
        _log_historial(
            conn, conv_id, canonical.nombre, "creada",
            fuente_codigo, canonical.confidence, canonical.raw_snippet
        )

        logger.info(
            f"[Insert] Nueva convocatoria: '{canonical.nombre[:60]}' "
            f"· {canonical.emisor_codigo} · confidence={canonical.confidence:.2f}"
        )
        return "inserted"

    except psycopg2.Error as e:
        logger.error(f"[Insert] DB error para '{canonical.nombre[:60]}': {e}")
        try:
            cur.close()
        except Exception:
            pass
        return "error"


def _update_fuente_status(
    conn,
    fuente_codigo: str,
    estado:        str,
    detectadas:    int,
    nuevas:        int,
    error_msg:     Optional[str] = None,
    duracion_ms:   Optional[int] = None,
) -> None:
    """Actualiza el registro de salud en fondos_fuentes."""
    cur = conn.cursor()
    cur.execute("""
        UPDATE fondos_fuentes
        SET
            ultimo_refresh           = NOW(),
            estado                   = %s,
            oportunidades_detectadas = %s,
            oportunidades_nuevas     = %s,
            error_msg                = %s,
            duracion_ms              = %s,
            updated_at               = NOW()
        WHERE codigo = %s
    """, (estado, detectadas, nuevas, error_msg, duracion_ms, fuente_codigo))
    cur.close()


def _log_historial(
    conn,
    conv_id:     Optional[int],
    conv_codigo: str,
    evento:      str,
    fuente:      str,
    confidence:  float,
    raw_snippet: Optional[str] = None,
) -> None:
    """Inserta un evento en fondos_historial."""
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fondos_historial
            (convocatoria_id, convocatoria_codigo, evento,
             fuente_codigo, normalizer_confidence, raw_snippet)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (conv_id, conv_codigo[:80], evento, fuente, confidence,
          (raw_snippet or "")[:400]))
    cur.close()


def _load_adapter(fuente_codigo: str):
    """Importa y retorna instancia del adaptador por código."""
    class_path = ADAPTERS_REGISTRY.get(fuente_codigo.upper())
    if not class_path:
        logger.error(f"[FondosRadar] Adaptador no registrado: {fuente_codigo}")
        return None
    try:
        module_path, class_name = class_path.rsplit(".", 1)
        import importlib
        module  = importlib.import_module(module_path)
        AdpCls  = getattr(module, class_name)
        return AdpCls()
    except Exception as exc:
        logger.error(f"[FondosRadar] Error cargando adaptador {fuente_codigo}: {exc}")
        return None


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level   = logging.INFO,
        format  = "%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt = "%H:%M:%S",
    )

    # Parsear argumentos simples
    mode     = "live"   if "--live"     in sys.argv else "demo"
    dry_run  = True     if "--dry-run"  in sys.argv else False
    use_haiku= False    if "--no-haiku" in sys.argv else True

    fuentes_arg = None
    for arg in sys.argv:
        if arg.startswith("--fuentes="):
            fuentes_arg = arg.split("=", 1)[1].split(",")

    gad_id = GAD_ID_DEFAULT
    for arg in sys.argv:
        if arg.startswith("--gad-id="):
            gad_id = arg.split("=", 1)[1]

    print(f"\nQUIRA /fondos-radar")
    print(f"  mode={mode}  dry_run={dry_run}  haiku={use_haiku}")
    print(f"  fuentes={fuentes_arg or 'todas'}  gad={gad_id}")
    print("=" * 60)

    result = run_fondos_radar(
        fuentes   = fuentes_arg,
        mode      = mode,
        dry_run   = dry_run,
        use_haiku = use_haiku,
        gad_id    = gad_id,
    )

    # Resumen
    print(f"\nRESUMEN PIPELINE:")
    print(f"  Raw:          {result['total_raw']}")
    print(f"  Normalizados: {result['total_normalizados']}")
    print(f"  Validos:      {result['total_validos']}")
    print(f"  Insertados:   {result['total_insertados']}")
    print(f"  Duplicados:   {result['total_duplicados']}")
    print(f"  Errores:      {result['total_errores']}")
    print(f"  Duracion:     {result['duracion_s']}s")

    if result["convocatorias_nuevas"]:
        print(f"\nCONVOCATORIAS NUEVAS ({len(result['convocatorias_nuevas'])}):")
        for c in result["convocatorias_nuevas"]:
            monto = c.get("monto_max_usd") or 0
            print(f"  [{c['emisor_codigo']:12s}]  {c['nombre'][:55]:55s}  "
                  f"${monto:>10,.0f}  conf={c['confidence']:.2f}")

    if result.get("matcher_recalculado"):
        ms = result["matcher_summary"]
        print(f"\nMATCHER (post-radar):")
        print(f"  Elegibles hoy:   {ms['elegible_hoy']}")
        print(f"  Con brecha:      {ms['elegible_con_brecha']}")
        print(f"  Bloqueadas:      {ms['no_elegible']}")
        print(f"  Potencial total: ${ms['total_potencial_usd']:,.0f}")

    print(f"\n{'=' * 60}")
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2, default=str))
