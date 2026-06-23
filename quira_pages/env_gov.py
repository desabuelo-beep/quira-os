"""
QUIRA Intelligence — Ambiente 🏛 GOV  (Router v4 · Sprint A+ · 2026-05-27)
QUIRA Institucional — Monitoreo preventivo para GADs del Ecuador.

Regla doctrinal permanente:
  env_gov.py ES UN ROUTER. No contiene contenido ni lógica de negocio.
  El contenido vive en m1-m5 y p0-p19 y p_*.
  Módulos nuevos = archivo nuevo + una línea aquí.
  Nunca agregar HTML, métricas ni tabs directamente en este archivo.

━━━ MAPA COMPLETO DE MÓDULOS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  SECCIÓN EJECUTIVA — todos los roles GOV (Directivo, Técnico, Administrador)
  ─────────────────────────────────────────────────────────────────────────────
  inicio       → p0_inicio.py          Dashboard de entrada · ICPI · SAT · riesgo
  situacion    → m1_situacion.py       Vista Ejecutiva + Pulso + Brecha
  alertas      → m2_alertas.py         SAT Activas + Evolución Longitudinal
  municipal    → m3_municipal.py       Holding + Gobernanza + Transparencia + Inversión
  ods          → p11_ods.py            ODS Tracker · Agenda 2030 ↔ PDOT
  confianza    → p16_confianza.py      IGP · Participación parroquial · CPCCS
  rdc          → p17_rdc.py            Rendición de Cuentas · CPCCS · Checklist
  cooperacion  → p18_cooperacion.py    Fondos BID · CAF · PNUD · ONU Mujeres
  genero       → p19_genero.py         PSG 12.83% · ODS 5 · Ambiente · FA PDOT
  territorio   → p10_territorio.py     Dom10 · Cobertura agua potable · ADR-013 AGUA_POTABLE
  transparencia→ p07_transparencia.py  Dom07 · LOTAIP 21 numerales · C4×C5a×C5b×C5c · ADR-013

  SECCIÓN TÉCNICA — solo Técnico, Operador, Administrador (is_tecnico())
  ─────────────────────────────────────────────────────────────────────────────
  analisis     → m4_analisis.py        Tablero Técnico + Eficiencia + Metas + Cadena + Operación
  geotwin      → p4_geotwin.py         GeoTwin Territorio · Mapa Folium · Parroquias (Técnico)
  congruencias → p3_congruencias.py    Congruencias HPT-M · PDOT
  simulador    → p13_simulador.py      Simulador de Escenarios · Análisis de sensibilidad
  control      → m5_control.py         Centro de Control + Carga + Ingesta + Historial + Sentinel

━━━ ROLES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Directivo    → ve: SECCIÓN EJECUTIVA (11 módulos)
  Técnico      → ve: SECCIÓN EJECUTIVA + SECCIÓN TÉCNICA (16 módulos)
  Administrador→ ve: todo (igual que Técnico — verificación cruzada)

━━━ NAVEGACIÓN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  app.py llama render_sidebar_nav() para inyectar el menú en el sidebar.
  app.py llama render() para mostrar el contenido del módulo activo.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from utils.session import is_tecnico, is_admin, is_ejecutivo, get_rol
from utils.cache_quira import cargar_snapshot, cargar_gm_snapshot
from utils.css_tokens import C


# ══════════════════════════════════════════════════════════════════════════════
# KPI BAND PERSISTENTE — visible en drill-down del Ejecutivo
# Mantiene contexto de los 4 KPIs mientras el operador explora un dominio
# ══════════════════════════════════════════════════════════════════════════════

def _render_mini_kpi_band() -> None:
    """
    Banda compacta de 4 KPI tiles — persiste en drill-down del Ejecutivo.
    Misma fuente de datos que p_command_center.py · misma doctrina de labels.
    Regla: ningún nombre interno (ICPI, TGI, SAT, Ti) en labels públicos.
    """
    try:
        snap, _ = cargar_snapshot()
        gm      = cargar_gm_snapshot()

        icpi_pct    = None
        icpi_clasif = "—"
        n_alertas   = 0
        hold_avg    = None

        if snap:
            icpi_d      = snap.get("icpi", {})
            icpi_pct    = icpi_d.get("global_pct") or icpi_d.get("global")
            icpi_clasif = icpi_d.get("clasificacion", "—")
            sat_d       = snap.get("sat", {})
            n_alertas   = sat_d.get("total_activas", 0)

        if gm and gm.get("icpi"):
            icpi_gm     = gm.get("icpi", {})
            icpi_pct    = icpi_gm.get("global_pct") or icpi_gm.get("global")
            icpi_clasif = icpi_gm.get("clasificacion", "—")

        if gm:
            _h90 = gm.get("financiero", {}).get("h90_consolidado", {}) or {}
            if _h90.get("holding_ti_q1_pct") is not None:
                hold_avg = _h90["holding_ti_q1_pct"]            # consolidado real del motor

        _parcial    = any(t in str(icpi_clasif).lower() for t in ("parcial", "preliminar"))
        icpi_color  = "#F59E0B" if _parcial else (C.sem(icpi_pct) if icpi_pct is not None else "#EF4444")
        alert_color = "#EF4444" if n_alertas > 0 else "#22C55E"
        hold_color  = C.sem(hold_avg) if hold_avg is not None else "#EF4444"
        icpi_str    = f"{icpi_pct:.1f}%" if icpi_pct is not None else "—"
        hold_str    = f"{hold_avg:.1f}%" if hold_avg is not None else "—"

        def _t(label: str, val: str, color: str, sub: str) -> str:
            return f"""
<div style="flex:1;min-width:0;padding:8px 12px;
            background:rgba(8,13,24,.97);border:1px solid {color}22;
            border-top:2px solid {color};border-radius:8px">
  <div style="font-size:7px;font-weight:700;letter-spacing:.09em;
              text-transform:uppercase;color:rgba(255,255,255,.25);
              margin-bottom:5px">{label}</div>
  <div style="font-size:1.1rem;font-weight:900;color:{color};
              font-family:'JetBrains Mono',monospace;letter-spacing:-.03em;
              line-height:1;margin-bottom:4px">{val}</div>
  <div style="font-size:7.5px;color:rgba(255,255,255,.26);
              line-height:1.35">{sub}</div>
</div>"""

        tiles_html = (
            _t("Cumplimiento Institucional", icpi_str, icpi_color,
               icpi_clasif) +
            _t("Fondos en Riesgo", "$3.66M", "#7C5CFC",
               "3 fuentes condicionadas") +
            _t("Alertas Activas", str(n_alertas), alert_color,
               "Sistema activo") +
            _t("Holding Municipal", hold_str, hold_color,
               "Consolidado 4 entidades")
        )

        st.markdown(f"""
<div style="display:flex;gap:8px;margin-bottom:14px;padding:0 2px">
  {tiles_html}
</div>
""", unsafe_allow_html=True)

    except Exception:
        # Falla silenciosa — el KPI band es contextual, no bloquea el drill-down
        pass


# ── Catálogo de módulos GOV ───────────────────────────────────────────────────
# (key, icon, label, tecnico_only)
# tecnico_only=True → solo visible para Técnico, Operador, Administrador
_GOV_MODULES: list[tuple[str, str, str, bool]] = [
    # ── Sección Ejecutiva (todos los roles GOV) ────────────────────────────
    ("inicio",       "🏛",  "Centro de Inteligencia Territorial",               False),
    ("situacion",    "📊",  "Situación Institucional",      False),
    ("alertas",      "🚨",  "Alertas y Riesgos SAT",        False),
    ("municipal",    "🏛",  "Gestión Municipal",             False),
    ("ods",          "🌐",  "ODS y Metas PDOT",              False),
    ("confianza",    "🤝",  "Confianza Ciudadana",           False),
    ("rdc",          "📋",  "Rendición de Cuentas",          False),
    ("cooperacion",  "🌍",  "Cooperación Internacional",     False),
    ("genero",       "💜",  "Género y Ambiente",             False),
    ("territorio",   "🗺",  "Territorio & Cobertura",        False),   # Dom10 · ADR-013
    ("transparencia","👁",  "Transparencia Institucional",   False),   # Dom07 · ADR-013 Sprint 4
    # ── Sección Técnica (Técnico, Operador, Administrador) ─────────────────
    ("cadena",       "🔗",  "Cadena Institucional",          True),   # Sprint E.1
    ("analisis",     "📈",  "Análisis Estratégico",          True),
    ("geotwin",      "🗺",  "GeoTwin Territorio",            True),
    ("congruencias", "🔗",  "Congruencias PDOT",             True),
    ("simulador",    "🎮",  "Simulador de Escenarios",       True),
    ("control",      "⚙",  "Centro de Control",             True),
]

# Claves de módulos exclusivos de la sección técnica
_TECNICO_MODULES: frozenset[str] = frozenset(
    key for key, *_, tec_only in _GOV_MODULES if tec_only
)


def _can_see(module_key: str) -> bool:
    """Determina si el rol actual puede ver este módulo."""
    if module_key in _TECNICO_MODULES:
        return is_tecnico() or is_admin()
    return True  # todos los roles GOV ven la sección ejecutiva


def _current_module() -> str:
    """Módulo activo según session_state. Corrige si el rol no tiene acceso."""
    mod = st.session_state.get("gov_module", "inicio")
    if not _can_see(mod):
        st.session_state["gov_module"] = "inicio"
        return "inicio"
    return mod


# ══════════════════════════════════════════════════════════════════════════════
# Sidebar navigation — llamado desde app.py
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar_nav() -> None:
    """
    Inyecta la navegación modular de GOV en el sidebar.
    Solo se llama desde app.py cuando el ambiente activo es GOV.

    Ejecutivo (Sprint 1.2): sidebar ELIMINADO — navegación por HTML canvas.
    Técnico / Administrador: EJECUTIVO + TÉCNICO secciones.
    """
    # ── Ejecutivo: sin sidebar — el Centro de Inteligencia Territorial es el canvas completo ──────
    if is_ejecutivo():
        # El sidebar se oculta por CSS en p_command_center.py.
        # Aquí solo evitamos renderizar botones que aparecerían si el CSS falla.
        return

    current_mod = _current_module()
    tiene_tecnico = is_tecnico() or is_admin()

    def _btn(key: str, icon: str, label: str) -> None:
        is_active = (key == current_mod)
        if st.sidebar.button(
            f"{icon}  {label}",
            key=f"gov_mod_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            help=label,
        ):
            st.session_state["gov_module"] = key
            st.rerun()

    # ── Sección Ejecutiva ─────────────────────────────────────────────────
    st.sidebar.markdown(
        '<div style="font-size:9px;color:rgba(0,212,255,.35);letter-spacing:.1em;'
        'text-transform:uppercase;margin:12px 0 5px;font-weight:700">EJECUTIVO</div>',
        unsafe_allow_html=True,
    )
    for key, icon, label, tec_only in _GOV_MODULES:
        if tec_only:
            continue
        _btn(key, icon, label)

    # ── Sección Técnica (solo si el rol lo permite) ───────────────────────
    if tiene_tecnico:
        st.sidebar.markdown(
            '<div style="font-size:9px;color:rgba(34,197,94,.35);letter-spacing:.1em;'
            'text-transform:uppercase;margin:14px 0 5px;font-weight:700">TÉCNICO</div>',
            unsafe_allow_html=True,
        )
        for key, icon, label, tec_only in _GOV_MODULES:
            if not tec_only:
                continue
            _btn(key, icon, label)


# ══════════════════════════════════════════════════════════════════════════════
# Header GOV — identificador visual en el contenido
# ══════════════════════════════════════════════════════════════════════════════

def _render_gov_header(module_label: str) -> None:
    """Banda superior con identidad GOV y módulo activo."""
    rol = get_rol()
    rol_badge_color = {
        "Ejecutivo":     "#00D4FF",
        "Directivo":     "#22C55E",
        "Administrador": "#F97316",
    }.get(rol, "#64748B")

    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 16px;background:rgba(0,212,255,.04);
            border:1px solid rgba(0,212,255,.1);border-radius:10px;
            margin-bottom:16px">
    <div style="display:flex;align-items:center;gap:10px">
        <span style="font-size:18px">🏛</span>
        <div>
            <div style="font-size:13px;font-weight:800;color:#E2E8F0;
                        letter-spacing:-.01em">QUIRA Institucional</div>
            <div style="font-size:10px;color:rgba(255,255,255,.35);
                        letter-spacing:.04em">{module_label}</div>
        </div>
    </div>
    <span style="font-size:10px;font-weight:700;color:{rol_badge_color};
                 background:{rol_badge_color}1A;border:1px solid {rol_badge_color}33;
                 border-radius:6px;padding:3px 10px;letter-spacing:.04em">{rol}</span>
</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Renderers — uno por módulo, todos con try/except defensivo
# ══════════════════════════════════════════════════════════════════════════════

# ── Sección Ejecutiva ─────────────────────────────────────────────────────────

def _render_inicio() -> None:
    # v2 NATIVO (Sprint C 2026-06-11): cajones st.button reales — el v1
    # (iframe + puente postMessage) nunca navegó en Streamlit Cloud por
    # sandbox cross-origin. v1 queda como fallback de emergencia.
    try:
        from quira_pages.p_command_center_v2 import render as _r
        _r()
    except Exception as e:
        import traceback as _tb
        st.error(f"💥 CENTRO DE MANDO v2 FALLÓ EN RUNTIME — mostrando v1. Error: {e}")
        st.code(_tb.format_exc())
        try:
            from quira_pages.p_command_center import render as _r1
            _r1()
        except Exception as e1:
            st.error(f"Centro de Inteligencia Territorial no disponible: {e1}")


def _render_situacion() -> None:
    try:
        from quira_pages.m1_situacion import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Situación no disponible: {e}")


def _render_metas_d03() -> None:
    """
    Dom03 — Metas PDOT e Integridad del Mandato · p8_metas.py
    IFE-A: 48/66 promesas CNE vinculadas al PDOT (72.73% · auditado H73)
    IFE-E: trazabilidad POA→PAC→eSIGEF (pendiente Q2-2026)
    Wiring: ADR-026 D03 routing · 2026-06-09
    """
    try:
        from quira_pages.p8_metas import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Metas PDOT no disponible: {e}")


def _render_alertas() -> None:
    try:
        from quira_pages.m2_alertas import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Alertas no disponible: {e}")


def _render_municipal() -> None:
    try:
        from quira_pages.m3_municipal import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Municipal no disponible: {e}")


def _render_ods() -> None:
    try:
        from quira_pages.p11_ods import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo ODS no disponible: {e}")


def _render_confianza() -> None:
    try:
        from quira_pages.p16_confianza import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Confianza Ciudadana no disponible: {e}")


def _render_rdc() -> None:
    try:
        from quira_pages.p17_rdc import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Rendición de Cuentas no disponible: {e}")


def _render_cooperacion() -> None:
    try:
        from quira_pages.p18_cooperacion import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Cooperación Internacional no disponible: {e}")


def _render_genero() -> None:
    try:
        from quira_pages.p19_genero import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Género y Ambiente no disponible: {e}")


# ── Sección Técnica ───────────────────────────────────────────────────────────

def _render_cadena() -> None:
    try:
        from quira_pages.p_cadena_institucional import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Cadena Institucional no disponible: {e}")


def _render_analisis() -> None:
    try:
        from quira_pages.m4_analisis import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Análisis no disponible: {e}")


def _render_geotwin() -> None:
    try:
        from quira_pages.p4_geotwin import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo GeoTwin no disponible: {e}")


def _render_congruencias() -> None:
    try:
        from quira_pages.p3_congruencias import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Congruencias no disponible: {e}")


def _render_simulador() -> None:
    try:
        from quira_pages.p13_simulador import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Simulador no disponible: {e}")


def _render_control() -> None:
    try:
        from quira_pages.m5_control import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Centro de Control no disponible: {e}")


def _render_concejo() -> None:
    """Panel Estratégico — dominio político dentro del Centro de Inteligencia Territorial."""
    try:
        from quira_pages.p_concejo import render as _r
        _r()
    except Exception as e:
        st.error(f"Panel Estratégico no disponible: {e}")


def _render_territorio() -> None:
    """
    Dom10 — Territorio & Cobertura · Layer 2 para Ejecutivo.
    ADR-013: AGUA_POTABLE → Dom10 → p10_territorio.py
    Todos los roles pueden ver esta vista ejecutiva.
    El GeoTwin técnico (p4_geotwin.py) sigue siendo Técnico.
    """
    try:
        from quira_pages.p10_territorio import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Territorio & Cobertura no disponible: {e}")


def _render_transparencia_d07() -> None:
    """
    Dom07 — Transparencia e Información Pública · Layer 2 · Sprint 4.
    ADR-013: TRANSPARENCIA → Dom07 → p07_transparencia.py
    QNKC-P01 Dualidad Epistémica: C4 (Cumplimiento Formal) × C5 (Verificabilidad).
    OBS-QNKC-01: verificabilidad_efectiva = C5a × C5b × C5c.
    Todos los roles pueden ver esta vista ejecutiva.
    """
    try:
        from quira_pages.p07_transparencia import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Transparencia Institucional no disponible: {e}")


# ── Mapa key → (renderer, label) ─────────────────────────────────────────────
_MODULE_RENDER: dict[str, tuple] = {
    # Sección Ejecutiva
    "inicio":       (_render_inicio,       "Centro de Inteligencia Territorial"),
    "situacion":    (_render_situacion,    "Situación Institucional"),
    "metas":        (_render_metas_d03,   "Metas PDOT · IFE"),          # Dom03 · ADR-026
    "alertas":      (_render_alertas,      "Alertas y Riesgos SAT"),
    "municipal":    (_render_municipal,    "Gestión Municipal"),
    "ods":          (_render_ods,          "ODS y Metas PDOT"),
    "confianza":    (_render_confianza,    "Confianza Ciudadana"),
    "rdc":          (_render_rdc,          "Rendición de Cuentas"),
    "cooperacion":  (_render_cooperacion,  "Cooperación Internacional"),
    "genero":       (_render_genero,       "Género y Ambiente"),
    "territorio":   (_render_territorio,      "Territorio & Cobertura"),    # Dom10 · ADR-013
    "transparencia":(_render_transparencia_d07,"Transparencia Institucional"),# Dom07 · Sprint 4
    # Sección Técnica
    "cadena":       (_render_cadena,       "Cadena Institucional"),   # Sprint E.1
    "analisis":     (_render_analisis,     "Análisis Estratégico"),
    "geotwin":      (_render_geotwin,      "GeoTwin Territorio"),
    "congruencias": (_render_congruencias, "Congruencias PDOT"),
    "simulador":    (_render_simulador,    "Simulador de Escenarios"),
    "control":      (_render_control,      "Centro de Control"),
}


# ══════════════════════════════════════════════════════════════════════════════
# Entry point — llamado desde app.py
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """
    Renderiza el contenido GOV según el rol activo.

    Ejecutivo (Sprint 1.2):
      · Centro de Inteligencia Territorial único = pantalla principal (HTML canvas full)
      · Sidebar eliminado — navegación por tarjetas onclick
      · drill-in de dominio → módulo + banda de retorno "← Centro de Inteligencia Territorial"
      · 'concejo' = Panel Estratégico como dominio (no view separada)

    Directivo / Administrador → módulo activo con header de identidad GOV.
    """
    # ── Ejecutivo: teatro operacional único ──────────────────────────────────
    if is_ejecutivo():
        gov_mod = st.session_state.get("gov_module", "inicio")

        # drill-in — navegó a un dominio desde el Centro de Inteligencia Territorial
        # 'concejo' se maneja igual que cualquier módulo (Panel Estratégico)
        drill_targets = set(_MODULE_RENDER.keys()) | {"concejo"}
        is_qinv = gov_mod.startswith("qinv_")
        if gov_mod != "inicio" and (is_qinv or gov_mod in drill_targets):

            # Mostrar el módulo con banda de retorno
            if is_qinv:
                # Cajón → investigación sobre el kernel (qinv.render · UMI · Pasada 1)
                from quira_pages.qinv import render as _r_qinv, label_of as _label_qinv
                _qdom = gov_mod[len("qinv_"):]
                fn_drill = lambda d=_qdom: _r_qinv(d)
                label_drill = _label_qinv(_qdom)
            elif gov_mod == "concejo":
                fn_drill, label_drill = _render_concejo, "Panel Estratégico"
            else:
                fn_drill, label_drill = _MODULE_RENDER.get(
                    gov_mod, (_render_inicio, "Inicio"))

            # ── CSS: restablecer sidebar si el drill-down lo necesita ────────
            st.markdown("""
<style>
/* Drill-down: sidebar sigue oculto, área main permanece 100% */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
}
.main .block-container,
[data-testid="stMainBlockContainer"] {
  max-width: 100% !important;
  padding-left: 1rem !important;
  padding-right: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

            # Banda de retorno contextual
            st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;
            padding:8px 14px;background:rgba(0,212,255,.04);
            border:1px solid rgba(0,212,255,.10);border-radius:8px">
  <span style="font-size:9px;color:rgba(0,212,255,.55);font-weight:700;
               letter-spacing:.08em;text-transform:uppercase">⬡ QUIRA</span>
  <span style="font-size:9px;color:rgba(255,255,255,.20)">›</span>
  <span style="font-size:9px;color:rgba(255,255,255,.35);font-weight:700;
               letter-spacing:.06em;text-transform:uppercase">Centro de Inteligencia Territorial</span>
  <span style="font-size:9px;color:rgba(255,255,255,.20)">›</span>
  <span style="font-size:9px;color:#E2E8F0;font-weight:700;
               letter-spacing:.06em;text-transform:uppercase">{label_drill}</span>
  <div style="margin-left:auto">
    <span id="__back_hint__"
          style="font-size:9px;color:rgba(0,212,255,.45);cursor:default">
      ← volver</span>
  </div>
</div>
""", unsafe_allow_html=True)

            # Botón funcional de retorno
            if st.button("← Centro de Inteligencia Territorial", key="exec_back_centro",
                         use_container_width=False):
                st.session_state["gov_module"] = "inicio"
                st.session_state.pop("ejecutivo_modo", None)
                st.rerun()

            # KPI band: SOLO módulos legacy. Los cajones QINV van limpios, sin cromo viejo
            # (Javo 2026-06-23: las 4 tiles son de pantallas antiguas — eliminar del cajón).
            if not is_qinv:
                _render_mini_kpi_band()

            fn_drill()
            return

        # ── Landing Ejecutivo: Centro de Inteligencia Territorial v2 NATIVO ──────────────────────
        # FIX 2026-06-11: esta era la SEGUNDA ruta al Centro de Inteligencia Territorial (la del
        # rol ejecutivo) y seguía llamando al v1 — por eso Javo veía v1.1
        # aunque el v2 estuviera desplegado y sano. Ambas rutas ahora → v2.
        try:
            from quira_pages.p_command_center_v2 import render as _ve
            _ve()
        except Exception as e:
            import traceback as _tb
            st.error(f"💥 CENTRO DE MANDO v2 FALLÓ EN RUNTIME — mostrando v1. Error: {e}")
            st.code(_tb.format_exc())
            try:
                from quira_pages.p_command_center import render as _ve1
                _ve1()
            except Exception as e1:
                st.error(f"Centro de Inteligencia Territorial no disponible: {e1}")
        return

    # ── Directivo / Administrador: módulo activo con header GOV ──────────────
    module_key = _current_module()
    fn, label  = _MODULE_RENDER.get(module_key, (_render_inicio, "Inicio"))
    _render_gov_header(label)
    fn()
