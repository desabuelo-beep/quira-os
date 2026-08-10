"""
QUIRA Intelligence — Ambiente ⚙ Ops
Infraestructura interna del equipo QUIRA. Nunca visible para el municipio.

5 tabs:
  Pipeline       → Ejecutar snapshot, ver logs, estado conectores
  Snapshots      → Registry, historial, validación
  Reliability    → Scores por fuente, trazabilidad longitudinal [Sprint 3 P3]
  Gold Master    → Estado v6.0, hojas implementadas, changelog [Sprint 3 P4]
  Configuración  → config.py, parámetros, conexiones

Acceso: Operator / Admin únicamente.
Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from utils.css_tokens import C


# ══════════════════════════════════════════════════════════════════════════════
# CARGA PEREZOSA — por qué existe (2026-08-07)
# ══════════════════════════════════════════════════════════════════════════════
# Abrir Operaciones costaba 326 segundos. La causa no era la red ni la base:
# `st.expander` NO es perezoso en Streamlit — el contenido de un expander se
# EJECUTA aunque esté cerrado— y `st.tabs` renderiza todas las pestañas, no solo
# la activa. Con cinco pestañas y siete expanders, cada uno montando una página
# entera, se ejecutaban doce páginas completas para mostrar una.
#
# Medido por pestaña antes del cambio:
#   Configuración 150 s · Cargas 113 s · Procesos 58 s · Confiabilidad 4 s
# El servicio local ausente aportaba solo 12 s de los 326: la sospecha inicial
# era la equivocada, y por eso se midió en vez de suponer.

def _perezosa(etiqueta: str, clave: str, cargar, ayuda: str = "") -> None:
    """Sección que se monta SOLO cuando se abre.

    Sustituye a `st.expander`, que ejecuta su contenido esté abierto o cerrado.
    El interruptor conserva su estado entre recargas, así que lo que el usuario
    dejó abierto sigue abierto."""
    if st.toggle(etiqueta, key=f"ops_ver_{clave}", help=ayuda or None):
        with st.container(border=True):
            try:
                cargar()
            except Exception as e:  # noqa: BLE001
                st.info(f"Sección no disponible: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# Tab 1 — Pipeline
# ══════════════════════════════════════════════════════════════════════════════

def _tab_pipeline() -> None:
    # ── Control de cache (Operator/Admin) ─────────────────────────────────────
    col_a, col_b = st.columns([3, 1])
    with col_b:
        if st.button("🔄 Refrescar datos", help="Invalida el cache y carga datos frescos desde Supabase/JSON", use_container_width=True):
            from utils.cache_quira import invalidar_todo
            invalidar_todo()
            st.success("Cache invalidado — recargando datos...")
            st.rerun()

    # El centro de control consulta un servicio local que normalmente no está
    # corriendo, y agota su espera en cada uno de tres extremos. Se carga bajo
    # demanda: son 12 s que no tiene sentido pagar al abrir la pantalla.
    def _sentinel():
        from quira_pages.p_sentinel_hub import render as r
        r()

    _perezosa("🛰 Centro de control", "sentinel", _sentinel,
              "Consulta el servicio local de vigilancia; tarda si no está activo")

    st.markdown("---")

    def _carga():
        from quira_pages.p_carga import render as r
        r()

    def _ingesta():
        from quira_pages.p_ingesta import render as r
        r()

    _perezosa("⬆️ Panel de carga manual", "carga", _carga)
    _perezosa("📥 Ingesta mensual", "ingesta", _ingesta)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 2 — Snapshots
# ══════════════════════════════════════════════════════════════════════════════

def _tab_snapshots() -> None:
    # Historial de snapshots
    try:
        from quira_pages.p_historico import render as _hist
        _hist()
    except Exception:
        pass

    st.markdown("---")

    def _seg():
        from quira_pages.p_seguimiento import render as r
        r()

    def _rep():
        from quira_pages.p_reportes import render as r
        r()

    _perezosa("📊 Seguimiento de cargas", "seguimiento", _seg)
    _perezosa("📄 Reportes", "reportes", _rep)


# ══════════════════════════════════════════════════════════════════════════════
# Tab 3 — Reliability  [Sprint 3 P3]
# ══════════════════════════════════════════════════════════════════════════════

def _tab_reliability() -> None:
    st.markdown("**📡 Source Reliability Governance**")
    st.caption("Sprint 3 · Prioridad 3 — Trazabilidad longitudinal de confiabilidad")

    # Tabla estática de confiabilidad actual
    fuentes = [
        ("Gold Master",     0.99, "Canónico",  "📋", "H73_OUTPUT_API v5.5+ · validación analítica Dylus Lab"),
        ("DPE API",         0.95, "Operativo", "📊", "API abierta eSIGEF · presupuesto y ejecución"),
        ("SERCOP OCDS",     0.95, "Operativo", "📝", "Portal contratación pública · OCDS estándar"),
        ("CPCCS RdC",       0.80, "Funcional", "🏛", "Rendición de cuentas ciudadana · portal CPCCS"),
        ("Evidencia social", 0.45, "Manual",   "👥", "Documentos ciudadanos · validación manual requerida"),
    ]

    for nombre, rel, estado, icon, desc in fuentes:
        # Era un semáforo hex a mano —verde/ámbar/rojo— y el sistema visual
        # prohíbe el verde: QUIRA mide verificabilidad, no bondad, y «bien» no
        # tiene color (utils/css_tokens · SIN_SENAL). Lo cazó el gate visual el
        # 2026-08-08, el mismo día que se amplió a los ambientes.
        r_color = C.atencion(rel * 100, umbral=90, alerta=70)
        e_color = C.SIN_SENAL if estado == "Operativo" else (
            C.OCRE if estado == "Canónico" else C.V_TX3)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;padding:10px 0;'
            f'border-bottom:1px solid rgba(255,255,255,.06)">'
            f'<span style="font-size:18px">{icon}</span>'
            f'<div style="flex:1">'
            f'<div style="font-size:13px;font-weight:600;color:#E2E8F0">{nombre}</div>'
            f'<div style="font-size:10px;color:rgba(255,255,255,.4)">{desc}</div>'
            f'</div>'
            f'<span style="font-size:10px;font-weight:700;color:{e_color};'
            f'background:{e_color}22;border:1px solid {e_color}44;'
            f'border-radius:4px;padding:2px 8px">{estado}</span>'
            f'<span style="font-size:14px;font-weight:800;color:{r_color};min-width:44px;'
            f'text-align:right">{rel:.0%}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("""
<div style="margin-top:16px;padding:10px 14px;background:rgba(245,158,11,.05);
            border-left:3px solid rgba(245,158,11,.4);border-radius:0 8px 8px 0;
            font-size:11px;color:rgba(255,255,255,.5)">
    <strong style="color:rgba(245,158,11,.8)">Sprint 3 P3 pendiente:</strong>
    <code>app/services/reliability_tracker.py</code> — evolución histórica de confiabilidad
    por fuente y trazabilidad longitudinal. Activado cuando se implemente.
</div>
    """, unsafe_allow_html=True)

    # Cargar reliability tracker con cache (10 min TTL)
    try:
        from utils.cache_quira import cargar_reliability_dashboard
        data = cargar_reliability_dashboard()
        if data:
            st.markdown("**Confiabilidad por Fuente**")
            import pandas as pd
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    except Exception as exc:
        st.warning(f"reliability_tracker: {exc}")


# ══════════════════════════════════════════════════════════════════════════════
# Tab 4 — Gold Master  [Sprint 3 P4]
# ══════════════════════════════════════════════════════════════════════════════

def _tab_gold_master() -> None:
    st.markdown("**📋 Gold Master Governance Layer**")
    st.caption("Motor metodológico TGI/ICPI/D1-D5 — Trazabilidad y versionado")

    # ── Estado Gold Master xlsx (con cache 10 min) ────────────────────────────
    from utils.cache_quira import cargar_estado_gold_master, cargar_gm_snapshot, cargar_changelog_gm

    estado_gm = cargar_estado_gold_master()
    gm_snap   = cargar_gm_snapshot()

    if estado_gm.get("disponible"):
        meta_snap = gm_snap.get("_meta", {})
        tgi_snap  = gm_snap.get("tgi", {})
        icpi_snap = gm_snap.get("icpi", {})

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Versión GM", estado_gm.get("version") or meta_snap.get("version_excel", "—"))
        with c2:
            st.metric("Fecha corte", estado_gm.get("fecha_corte") or meta_snap.get("fecha_corte", "—"))
        with c3:
            st.metric("TGI/ICPI", f"{icpi_snap.get('global_pct', tgi_snap.get('score', '—'))}%")
        with c4:
            n_err = estado_gm.get("n_errores_val", 0)
            color_v = "normal" if n_err == 0 else "inverse"
            st.metric("Errores validación", n_err, delta="OK" if n_err == 0 else "Revisar", delta_color=color_v)

        st.markdown(
            f"**Archivo:** `{estado_gm.get('nombre_archivo', '—')}` · "
            f"**Hojas:** {estado_gm.get('total_hojas', '—')} · "
            f"**Tamaño:** {estado_gm.get('tamano_mb', 0):.2f} MB"
        )
        if estado_gm.get("sha256"):
            st.caption(f"SHA-256: `{estado_gm['sha256'][:32]}...`")

        # Changelog
        changelog = cargar_changelog_gm()
        versiones  = changelog.get("versiones", [])
        if versiones:
            st.markdown("**Changelog de versiones:**")
            for v in versiones:
                estado_badge = "🟢" if v.get("estado") == "ACTIVO" else "⚪"
                st.markdown(
                    f"{estado_badge} **{v.get('version', '—')}** — {v.get('fecha', '—')} "
                    f"· `{v.get('estado', '—')}` · {v.get('hojas', '—')} hojas"
                )
                if v.get("notas"):
                    st.caption(v["notas"])
    elif gm_snap:
        # Fallback: leer solo desde gm_snapshot.json (modo Cloud)
        meta = gm_snap.get("_meta", {})
        tgi  = gm_snap.get("tgi", {})
        icpi = gm_snap.get("icpi", {})
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Versión (snapshot)", meta.get("version_excel", "—"))
        with c2:
            st.metric("Fecha corte", meta.get("fecha_corte", "—"))
        with c3:
            st.metric("ICPI", f"{icpi.get('global_pct', tgi.get('score', '—'))}%")
        st.info("Gold Master xlsx no disponible en este entorno — mostrando datos del snapshot JSON.")
    else:
        st.warning("Gold Master no disponible. Verifica que `data/gm_snapshot.json` esté en el repositorio.")

    st.markdown("---")

    # Estado hojas canónicas v5.5
    st.markdown("**Estado Gold Master v5.5 (canónico activo) — Hojas clave**")
    hojas_estado = [
        ("H73_OUTPUT_API",             "✅ Activa",    "64 métricas · reliability=0.99 · interfaz pública"),
        ("H82_CONFIG_PARAMS",          "✅ Activa",    "Configuración sistema — VERSION_SISTEMA"),
        ("H07_S5_FINANCIERO_eSIGEF",  "✅ Activa",    "Ti Holding 4 entes · datos reales Ene-Abr 2026"),
        ("H10_S8_PARTICIPACIÓN_CPCCS", "✅ Activa",    "25 metas PDOT · evidencia RDC 2023-2024 verificada"),
    ]
    for hoja, estado, nota in hojas_estado:
        color = C.SIN_SENAL if "✅" in estado else C.OCRE
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;'
            f'padding:6px 0;border-bottom:1px solid rgba(255,255,255,.06)">'
            f'<code style="font-size:11px;color:#00D4FF">{hoja}</code>'
            f'<span style="font-size:11px;font-weight:700;color:{color}">{estado}</span>'
            f'<span style="font-size:10px;color:rgba(255,255,255,.4)">{nota}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("""
<div style="margin-top:16px;padding:10px 14px;background:rgba(245,158,11,.05);
            border-left:3px solid rgba(245,158,11,.4);border-radius:0 8px 8px 0;
            font-size:11px;color:rgba(255,255,255,.5)">
    <strong style="color:rgba(245,158,11,.8)">Sprint 3 P4 pendiente:</strong>
    <code>app/services/gold_master_governance.py</code> — versionado, changelog,
    backup SHA-256, validación canónica. Activado cuando se implemente.
</div>
    """, unsafe_allow_html=True)

    # Intentar governance layer si existe
    try:
        from app.services.gold_master_governance import get_gm_changelog
        changelog = get_gm_changelog()
        if changelog:
            st.markdown("**Changelog Gold Master**")
            for entry in changelog[:5]:
                st.markdown(f"• `{entry.get('version')}` — {entry.get('descripcion', '')}")
    except ImportError:
        pass
    except Exception as exc:
        st.warning(f"gold_master_governance: {exc}")


# ══════════════════════════════════════════════════════════════════════════════
# Tab 5 — Configuración
# ══════════════════════════════════════════════════════════════════════════════

def _tab_config() -> None:
    st.markdown("**⚙ Configuración del Sistema**")

    try:
        import config as cfg

        params = [
            ("APP_NAME",         getattr(cfg, "APP_NAME", "—"),          "Nombre de la aplicación"),
            ("APP_VERSION",      getattr(cfg, "APP_VERSION", "—"),        "Versión actual"),
            ("GAD_NOMBRE",       getattr(cfg, "GAD_NOMBRE", "—"),         "Municipio primario"),
            ("GAD_PERIODO",      getattr(cfg, "GAD_PERIODO", "—"),        "Período de gobierno"),
            ("CORTE",            getattr(cfg, "CORTE", "—"),              "Corte de datos activo"),
            ("LOG_LEVEL",        getattr(cfg, "LOG_LEVEL", "INFO"),       "Nivel de logging"),
            ("SNAPSHOT_SCHEMA",  getattr(cfg, "SNAPSHOT_SCHEMA", "—"),   "Schema canónico"),
            ("PIPELINE_VERSION", getattr(cfg, "PIPELINE_VERSION", "—"),  "Versión del pipeline"),
        ]

        for key, val, desc in params:
            st.markdown(
                f'<div style="display:flex;align-items:center;justify-content:space-between;'
                f'padding:7px 0;border-bottom:1px solid rgba(255,255,255,.05)">'
                f'<div>'
                f'<span style="font-family:monospace;font-size:12px;color:#00D4FF">{key}</span>'
                f'<div style="font-size:10px;color:rgba(255,255,255,.35)">{desc}</div>'
                f'</div>'
                f'<span style="font-size:12px;color:#E2E8F0;font-weight:600">{val}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    except Exception as exc:
        st.error(f"No se pudo cargar config.py: {exc}")

    st.markdown("---")

    # Paths canónicos
    st.markdown("**Paths del sistema**")
    try:
        import config as cfg
        paths_map = [
            ("SNAPSHOTS_DIR", getattr(cfg, "SNAPSHOTS_DIR", "—")),
            ("DATA_DIR",      getattr(cfg, "DATA_DIR", "—")),
            ("GM_PATH",       getattr(cfg, "GM_PATH", "—")),
        ]
        for name, val in paths_map:
            st.code(f"{name} = {val}", language="text")
    except Exception:
        pass

    st.markdown("---")

    def _aprendizaje():
        from quira_pages.p_aprendizaje import render as r
        r()

    def _gestion():
        from quira_pages.p_gestion import render as r
        r()

    def _alertas():
        from quira_pages.p_alertas import render as r
        r()

    # Estas tres eran las más caras: montaban una página completa cada una
    # aunque el expander estuviera cerrado — 150 s de los 326 totales.
    _perezosa("🔮 Aprendizaje del sistema", "aprendizaje", _aprendizaje)
    _perezosa("🗓 Gestión", "gestion", _gestion)
    _perezosa("🔔 Monitor de señales", "alertas", _alertas)


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """OPERACIONES — mantenimiento técnico del sistema (Javo · 2026-08-06).

    NO es el Observatorio, y conviene dejarlo escrito porque el director los
    fusionó y estuvo mal: aquí vive el sostenimiento técnico que hace Dylus Lab
    cuando algo se rompe —cargas, conectores, cache, versiones del motor—. El
    Observatorio es otra cosa: un instrumento de administración pública cuyos
    interlocutores son el sector público y la cooperación internacional, y es el
    PRODUCTO PRINCIPAL (ADR-041 §5.1). Vive en `env_obs.py`.

    Las etiquetas sí salen de la jerga: este ambiente es interno pero sigue
    siendo una pantalla, y la Regla 2 no distingue."""
    from utils.css_tokens import C
    from utils.marca import logo

    st.markdown(f"""
<div style="display:flex;align-items:center;gap:11px;margin-bottom:6px">
    <span style="line-height:0">{logo("marfil", 22)}</span>
    <div>
      <div style="font-size:14px;font-weight:800;color:{C.V_TX}">Operaciones</div>
      <div style="font-size:10px;color:{C.V_TX2}">Mantenimiento técnico del
        sistema · equipo Dylus Lab</div>
    </div>
    <span style="margin-left:auto;font:700 9px/1 'JetBrains Mono',monospace;
                 color:{C.V_TX3};border:1px solid {C.V_BD_FUERTE};border-radius:6px;
                 padding:4px 9px;letter-spacing:.08em">USO INTERNO</span>
</div>
    """, unsafe_allow_html=True)

    # Un selector en vez de `st.tabs`: las pestañas de Streamlit renderizan su
    # contenido TODAS a la vez, esté visible o no. Con un selector se monta
    # únicamente la sección elegida, que es lo que el usuario está mirando.
    SECCIONES = {
        "⚡ Procesos":                 _tab_pipeline,
        "📦 Cargas":                   _tab_snapshots,
        "📡 Confiabilidad de fuentes": _tab_reliability,
        "📋 Motor de cálculo":         _tab_gold_master,
        "⚙ Configuración":             _tab_config,
    }
    elegida = st.radio("Sección", list(SECCIONES), horizontal=True,
                       key="ops_seccion", label_visibility="collapsed")
    st.markdown("---")
    SECCIONES[elegida]()
