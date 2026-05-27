"""
utils/cache_quira.py — QUIRA Intelligence · Sprint 3 Semana 4
Capa de cache centralizada para datos institucionales.

Problema que resuelve:
  Streamlit re-ejecuta el script completo en cada interacción del usuario.
  Sin cache: cada cambio de tab relanza load_snapshot() → Supabase/JSON.
  Con cache:  el snapshot se carga UNA vez y se reutiliza por TTL.

Estrategia de TTL (tiempo de vida del cache):
  · Snapshot activo    → 300s (5 min)  — operativamente estable por horas
  · Historial RC-M     → 300s (5 min)  — ídem
  · Reliability dash   → 600s (10 min) — cambia aún menos frecuente
  · Gold Master JSON   → 900s (15 min) — casi nunca cambia en runtime
  · Estado GM (xlsx)   → 600s (10 min) — solo cambia al actualizar Gold Master

Invalidación manual:
  En session_state usar `st.cache_data.clear()` tras ejecutar el pipeline
  para que el próximo render muestre datos frescos.

Doctrina:
  El cache está en tecnología (reemplazable).
  El dato canónico sigue siendo Gold Master + Supabase (permanentes).

Dylus Lab © 2026 — QUIRA Intelligence
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from utils.logger import get_logger

logger = get_logger(__name__)

_RAIZ = Path(__file__).parent.parent


# ══════════════════════════════════════════════════════════════════════════════
# Cache: Snapshot activo
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def cargar_snapshot(municipio_code: str = "130801") -> tuple[dict | None, dict | None]:
    """
    Carga el snapshot activo del municipio desde Supabase o JSON fallback.
    Cache TTL: 5 minutos. Misma interfaz que load_snapshot() de snapshot_io.
    Retorna: (snapshot_dict, meta_dict) o (None, None) si no hay datos.
    """
    try:
        from utils.snapshot_io import load_snapshot
        snap, meta = load_snapshot(municipio_code=municipio_code)
        if snap:
            logger.debug(f"[Cache] Snapshot {municipio_code} cargado — ICPI={snap.get('icpi', {}).get('global_pct', '—')}%")
        return snap, meta
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando snapshot {municipio_code}: {exc}")
        return None, None


# ══════════════════════════════════════════════════════════════════════════════
# Cache: Historial longitudinal RC-M
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def cargar_historial_snapshots(municipio_code: str = "130801", limite: int = 12) -> list[dict]:
    """
    Carga el historial de snapshots para la tabla RC-M longitudinal.
    Cache TTL: 5 minutos.
    Retorna: lista de snapshots ordenados por fecha (más reciente primero).
    """
    try:
        from app.services.longitudinal_engine import get_snapshot_history
        historia = get_snapshot_history(municipio_code, limit=limite)
        logger.debug(f"[Cache] Historial {municipio_code}: {len(historia)} períodos")
        return historia
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando historial {municipio_code}: {exc}")
        return []


@st.cache_data(ttl=300, show_spinner=False)
def cargar_datos_rcm(municipio_code: str = "130801") -> list[dict]:
    """
    Carga la tabla RC-M canónica (fecha, ICPI, D3, SAT-IV, Riesgo ponderado).
    Cache TTL: 5 minutos.
    """
    try:
        from app.services.longitudinal_engine import get_rc_m_data
        datos = get_rc_m_data(municipio_code)
        logger.debug(f"[Cache] RC-M {municipio_code}: {len(datos)} filas")
        return datos
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando RC-M {municipio_code}: {exc}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# Cache: Reliability Dashboard
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def cargar_reliability_dashboard() -> list[dict]:
    """
    Carga el dashboard de confiabilidad por fuente.
    Cache TTL: 10 minutos — cambia muy poco en runtime.
    Retorna: lista de dicts con {fuente, reliability, estado, ...}
    """
    try:
        from app.services.reliability_tracker import get_reliability_dashboard
        datos = get_reliability_dashboard()
        logger.debug(f"[Cache] Reliability dashboard: {len(datos)} fuentes")
        return datos or []
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando reliability dashboard: {exc}")
        return []


@st.cache_data(ttl=600, show_spinner=False)
def cargar_reliability_historial(municipio_code: str = "130801") -> list[dict]:
    """
    Carga el historial de confiabilidad por fuente para un municipio.
    Cache TTL: 10 minutos.
    """
    try:
        from app.services.reliability_tracker import get_reliability_history
        datos = get_reliability_history(municipio_code)
        logger.debug(f"[Cache] Reliability historial {municipio_code}: {len(datos)} registros")
        return datos or []
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando reliability historial: {exc}")
        return []


# ══════════════════════════════════════════════════════════════════════════════
# Cache: Gold Master JSON (fallback)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=900, show_spinner=False)
def cargar_gm_snapshot() -> dict:
    """
    Carga data/gm_snapshot.json — el fallback del Gold Master para Streamlit Cloud.
    Cache TTL: 15 minutos — prácticamente estático en runtime.
    Retorna: dict completo del snapshot o {} si no existe.
    """
    ruta = _RAIZ / "data" / "gm_snapshot.json"
    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
        meta  = datos.get("_meta", {})
        logger.debug(f"[Cache] gm_snapshot.json cargado — versión: {meta.get('version_excel', '—')}")
        return datos
    except FileNotFoundError:
        logger.warning("[Cache] gm_snapshot.json no encontrado")
        return {}
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando gm_snapshot.json: {exc}")
        return {}


# ══════════════════════════════════════════════════════════════════════════════
# Cache: Estado Gold Master (xlsx vivo)
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def cargar_estado_gold_master() -> dict:
    """
    Diagnóstico completo del Gold Master xlsx: disponibilidad, métricas,
    errores de validación, changelog, SHA-256.
    Cache TTL: 10 minutos — el Gold Master rara vez cambia en runtime.
    Retorna: dict de obtener_estado_gm() o {disponible: False} si falla.
    """
    try:
        from app.services.gold_master_governance import obtener_estado_gm
        estado = obtener_estado_gm()
        logger.debug(
            f"[Cache] Estado GM — disponible={estado.get('disponible')} "
            f"· versión={estado.get('version', '—')} "
            f"· errores={estado.get('n_errores_val', 0)}"
        )
        return estado
    except Exception as exc:
        logger.warning(f"[Cache] Error cargando estado Gold Master: {exc}")
        return {"disponible": False, "error": str(exc)}


@st.cache_data(ttl=600, show_spinner=False)
def cargar_changelog_gm() -> dict:
    """
    Historial de versiones del Gold Master desde gm_changelog.json.
    Cache TTL: 10 minutos.
    """
    try:
        from app.services.gold_master_governance import obtener_changelog_gm
        return obtener_changelog_gm()
    except Exception as exc:
        return {"versiones": [], "version_activa": None, "total_versiones": 0, "error": str(exc)}


# ══════════════════════════════════════════════════════════════════════════════
# Invalidación manual
# ══════════════════════════════════════════════════════════════════════════════

def invalidar_cache_snapshot() -> None:
    """
    Invalida el cache del snapshot activo e historial.
    Llamar después de ejecutar el pipeline para mostrar datos frescos.

    Uso típico (desde env_ops.py tras ejecutar pipeline):
        from utils.cache_quira import invalidar_cache_snapshot
        invalidar_cache_snapshot()
        st.rerun()
    """
    cargar_snapshot.clear()
    cargar_historial_snapshots.clear()
    cargar_datos_rcm.clear()
    logger.info("[Cache] Cache de snapshot invalidado — próximo render cargará datos frescos")


def invalidar_cache_gm() -> None:
    """
    Invalida el cache del Gold Master y reliability.
    Llamar después de actualizar el Gold Master.
    """
    cargar_gm_snapshot.clear()
    cargar_estado_gold_master.clear()
    cargar_changelog_gm.clear()
    cargar_reliability_dashboard.clear()
    logger.info("[Cache] Cache de Gold Master invalidado")


def invalidar_todo() -> None:
    """Invalida todos los caches de QUIRA. Usar con moderación."""
    st.cache_data.clear()
    logger.info("[Cache] Cache completo invalidado")
