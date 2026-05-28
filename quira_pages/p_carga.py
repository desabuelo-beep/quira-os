"""
QUIRA OS · p_carga.py
Panel de Carga Mensual — RC-CARGA

Permite al Técnico actualizar el snapshot maestro de indicadores institucionales
directamente desde el browser, sin tocar código ni Git.

Flujo:
  1. Analista descarga / actualiza el Gold Master Excel localmente
  2. Corre scripts/_update_snapshot.py → genera gm_snapshot.json actualizado
  3. Abre esta página → sube gm_snapshot.json → QUIRA valida y guarda en Supabase
  4. Todos los usuarios ven los datos actualizados de inmediato

Acceso: solo rol Técnico.

Dylus Lab © 2026
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone

import streamlit as st

from utils.page_guards  import auth_required_notice
from utils.snapshot_io  import validate_snapshot, save_snapshot, list_snapshots
from utils.display_names import FUENTE_CANONICA


# ── CSS interno ───────────────────────────────────────────────────────────────
_CSS = """
<style>
.carga-header {
  font-size: 11px; font-weight: 700; letter-spacing: 1.3px;
  text-transform: uppercase; color: #00D4FF;
  border-left: 3px solid #00D4FF; padding-left: 10px; margin-bottom: 12px;
}
.carga-card {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px; padding: 16px 20px; margin-bottom: 10px;
}
.snap-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
  font-size: 12px;
}
.snap-row:last-child { border-bottom: none; }
.snap-label { color: rgba(255,255,255,0.45); font-size: 10px; text-transform: uppercase; letter-spacing: .07em; }
.snap-value { color: #E2E8F0; font-weight: 600; }
.snap-ok    { color: #00E096; }
.snap-warn  { color: #FFB700; }
.snap-err   { color: #FF4D6D; }
.badge-active   { background: rgba(0,224,150,0.18); color: #00E096; border: 1px solid #00E096;
                  border-radius: 5px; padding: 1px 8px; font-size: 10px; font-weight: 700; }
.badge-inactive { background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.35);
                  border: 1px solid rgba(255,255,255,0.12); border-radius: 5px;
                  padding: 1px 8px; font-size: 10px; }
</style>
"""

_GUIDE = """
<div class="carga-card">
<div class="carga-header">Guía de carga — 3 pasos</div>
<div class="snap-row"><span class="snap-label">Paso 1</span>
  <span class="snap-value" style="font-size:11px">Actualiza el Gold Master Excel localmente con los datos del nuevo período</span></div>
<div class="snap-row"><span class="snap-label">Paso 2</span>
  <span class="snap-value" style="font-size:11px">Corre <code>python scripts/_update_snapshot.py</code> → genera <code>data/gm_snapshot.json</code></span></div>
<div class="snap-row"><span class="snap-label">Paso 3</span>
  <span class="snap-value" style="font-size:11px">Sube el JSON aquí → QUIRA valida y lo activa para todos los usuarios</span></div>
<div style="font-size:10px;color:rgba(255,255,255,0.3);margin-top:10px">
  El Gold Master Excel NUNCA sale de tu equipo · Solo el JSON procesado entra al sistema
</div>
</div>
"""


# ══════════════════════════════════════════════════════════════════════════════
# RENDER PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    # ── Gate: solo Técnico ────────────────────────────────────────────────────
    rol = st.session_state.get("rol", "")
    if rol not in ("Directivo", "Operador", "Administrador"):
        st.warning(
            "🔒 Acceso restringido — esta sección es exclusiva del rol **Directivo**.",
            icon="⚙️",
        )
        return

    st.markdown(_CSS, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        """<div style="font-size:1.3rem;font-weight:900;color:#00D4FF;margin-bottom:4px">
        ⚙️ Panel de Carga Mensual</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:20px">
        Actualiza el snapshot institucional · Solo rol Técnico</div>""",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs([
        "📤 Subir Snapshot",
        "📋 Historial de Cargas",
        "ℹ️ Estado Actual",
    ])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — Subir snapshot JSON
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown(_GUIDE, unsafe_allow_html=True)
        st.markdown("---")

        st.markdown('<div class="carga-header">Subir gm_snapshot.json</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Archivo JSON generado por scripts/_update_snapshot.py",
            type=["json"],
            help="Solo acepta archivos .json con la estructura canónica de QUIRA OS.",
            label_visibility="collapsed",
        )

        notas = st.text_input(
            "Notas del analista (opcional)",
            placeholder='Ej: "Carga Q1-2026 — cédula presupuestaria Marzo validada"',
            max_chars=200,
        )

        if uploaded is not None:
            # ── Parsear JSON ─────────────────────────────────────────────────
            try:
                raw_bytes = uploaded.read()
                data = json.loads(raw_bytes.decode("utf-8"))
            except Exception as exc:
                st.error(f"❌ El archivo no es JSON válido: {exc}")
                return

            # ── Validar estructura ────────────────────────────────────────────
            ok, errors = validate_snapshot(data)

            with st.expander("🔍 Resultado de validación", expanded=True):
                if ok:
                    st.success("✅ Estructura validada correctamente")
                    meta = data.get("_meta", {})
                    gad  = data.get("gad",  {})
                    tgi  = data.get("tgi",  {})
                    fin  = data.get("financiero", {})

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Municipio",    gad.get("nombre", "—")[:22])
                    col2.metric("Versión",      meta.get("version_excel", "—"))
                    col3.metric("Corte",        meta.get("fecha_corte", "—"))
                    col4.metric("TGI Score",    f"{tgi.get('score', 0):.2f}")

                    # Vista previa de indicadores clave
                    st.markdown(
                        f"""
<div class="carga-card" style="margin-top:12px">
<div class="carga-header">Vista previa — indicadores principales</div>
<div class="snap-row">
  <span class="snap-label">Clasificación TGI</span>
  <span class="snap-value">{tgi.get('clasificacion','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Parroquias</span>
  <span class="snap-value">{data.get('territorial',{{}}).get('parroquias_total','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Devengado Q1-2026</span>
  <span class="snap-value">${fin.get('devengado_q1_2026',0):,.0f}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Ti 2025</span>
  <span class="snap-value">{fin.get('ti_2025_pct',0):.2f}%</span>
</div>
</div>""",
                        unsafe_allow_html=True,
                    )
                else:
                    st.error("❌ Validación fallida — revisa los errores antes de continuar")
                    for err in errors:
                        st.caption(f"· {err}")

            # ── Confirmar y guardar ───────────────────────────────────────────
            if ok:
                st.markdown("---")
                usuario = st.session_state.get("usuario", "tecnico")

                if st.button(
                    "✅ Confirmar y activar snapshot",
                    type="primary",
                    use_container_width=True,
                    help="Guarda el snapshot en Supabase y lo activa para todos los usuarios.",
                ):
                    try:
                        from sentinel.db_config import get_connection, init_db
                        init_db()
                        conn = get_connection()
                        success, msg = save_snapshot(
                            conn, data, uploaded_by=usuario, notas=notas
                        )
                        conn.close()

                        if success:
                            st.success(f"🚀 Snapshot activado — {msg}")
                            # Invalidar caché de session_state para forzar recarga
                            for key in list(st.session_state.keys()):
                                if key.startswith(("gm_", "data_loaded", "rc7", "d3", "d4", "d1", "d5", "synth")):
                                    del st.session_state[key]
                            st.balloons()
                            st.info(
                                "💡 Los datos actualizados estarán disponibles en todas "
                                "las páginas al navegar. Si alguna página muestra datos "
                                "anteriores, recarga la sesión.",
                                icon="ℹ️",
                            )
                        else:
                            st.error(f"❌ {msg}")

                    except Exception as exc:
                        st.error(f"❌ Error de conexión a base de datos: {exc}")
                        st.caption(
                            "Verifica que Supabase esté configurado en "
                            "`.streamlit/secrets.toml` con `mode = 'supabase'`."
                        )

        else:
            st.caption(
                "📎 Arrastra el archivo JSON aquí, o haz clic para seleccionar. "
                "El archivo no sale de esta sesión — solo los indicadores extraídos se guardan."
            )

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — Historial de cargas
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<div class="carga-header">Historial de snapshots cargados</div>', unsafe_allow_html=True)

        try:
            from sentinel.db_config import get_connection
            conn = get_connection()
            rows = list_snapshots(conn)
            conn.close()
        except Exception:
            rows = []

        if not rows:
            st.info(
                "Aún no hay snapshots registrados en Supabase. "
                "Usa la pestaña **Subir Snapshot** para cargar el primero.",
                icon="📂",
            )
        else:
            st.caption(f"{len(rows)} snapshot(s) registrado(s) — mostrando más recientes primero")
            for row in rows:
                active_badge = (
                    '<span class="badge-active">ACTIVO</span>'
                    if row.get("is_active")
                    else '<span class="badge-inactive">inactivo</span>'
                )
                ts = (row.get("uploaded_at") or "")[:19].replace("T", " ")
                st.markdown(
                    f"""<div class="carga-card">
<div class="snap-row">
  <span class="snap-value">{row.get('municipio_name','—')}</span>
  {active_badge}
</div>
<div class="snap-row">
  <span class="snap-label">Versión</span>
  <span class="snap-value">{row.get('version','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Corte</span>
  <span class="snap-value">{row.get('fecha_corte','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Cargado por</span>
  <span class="snap-value">{row.get('uploaded_by','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Fecha carga</span>
  <span class="snap-value">{ts} UTC</span>
</div>
{f'<div class="snap-row"><span class="snap-label">Notas</span><span class="snap-value" style="font-size:11px">{row.get("notas","")}</span></div>' if row.get("notas") else ""}
<div class="snap-row">
  <span class="snap-label">SHA256</span>
  <span class="snap-value" style="font-family:monospace;font-size:10px">{row.get('checksum_sha256','—')}</span>
</div>
</div>""",
                    unsafe_allow_html=True,
                )

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — Estado actual del sistema
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown('<div class="carga-header">Estado actual del snapshot maestro</div>', unsafe_allow_html=True)

        from utils.snapshot_io import load_snapshot as _load
        snap, meta = _load(municipio_code="130801")

        if snap is None:
            st.warning("Sin snapshot maestro disponible.", icon="⚠️")
        else:
            source_label_map = {
                "supabase":  "🟢 Supabase (en vivo)",
                "json_file": "🟡 Archivo estático del repo (fallback)",
            }
            source_txt = source_label_map.get(meta.get("source", ""), "Desconocido")
            ts = (meta.get("uploaded_at") or "")[:19].replace("T", " ")

            gad = snap.get("gad", {})
            tgi = snap.get("tgi", {})
            fin = snap.get("financiero", {})
            ter = snap.get("territorial", {})

            st.markdown(
                f"""<div class="carga-card">
<div class="carga-header">Fuente de datos activa</div>
<div class="snap-row">
  <span class="snap-label">Fuente</span>
  <span class="snap-value">{source_txt}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Versión</span>
  <span class="snap-value">{meta.get('version','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Actualización</span>
  <span class="snap-value">{ts} UTC</span>
</div>
<div class="snap-row">
  <span class="snap-label">Municipio</span>
  <span class="snap-value">{gad.get('nombre','—')}</span>
</div>
</div>

<div class="carga-card" style="margin-top:8px">
<div class="carga-header">Indicadores clave activos</div>
<div class="snap-row">
  <span class="snap-label">TGI Score</span>
  <span class="snap-value snap-ok">{tgi.get('score',0):.2f} — {tgi.get('clasificacion','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Ti 2025</span>
  <span class="snap-value">{fin.get('ti_2025_pct',0):.2f}%</span>
</div>
<div class="snap-row">
  <span class="snap-label">Devengado Q1-2026</span>
  <span class="snap-value">${fin.get('devengado_q1_2026',0):,.0f}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Parroquias</span>
  <span class="snap-value">{ter.get('parroquias_total','—')}</span>
</div>
<div class="snap-row">
  <span class="snap-label">Población (INEC 2022)</span>
  <span class="snap-value">{ter.get('poblacion_census_2022',0):,}</span>
</div>
</div>""",
                unsafe_allow_html=True,
            )

            if meta.get("source") == "json_file":
                st.warning(
                    "El sistema está usando el archivo estático del repositorio. "
                    "Para activar datos en tiempo real, sube un snapshot en la pestaña **Subir Snapshot**.",
                    icon="⚠️",
                )

        st.markdown("---")
        st.caption(f"Sistema de Información Institucional QUIRA · {FUENTE_CANONICA}")
