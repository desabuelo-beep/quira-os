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

  SECCIÓN TÉCNICA — solo Técnico, Operador, Administrador (is_tecnico())
  ─────────────────────────────────────────────────────────────────────────────
  analisis     → m4_analisis.py        Tablero Técnico + Eficiencia + Metas + Cadena + Operación
  geotwin      → p4_geotwin.py         GeoTwin Territorio · Mapa Folium · Parroquias
  congruencias → p3_congruencias.py    Congruencias HPT-M · PDOT
  simulador    → p13_simulador.py      Simulador de Escenarios · Análisis de sensibilidad
  control      → m5_control.py         Centro de Control + Carga + Ingesta + Historial + Sentinel

━━━ ROLES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Directivo    → ve: SECCIÓN EJECUTIVA (9 módulos)
  Técnico      → ve: SECCIÓN EJECUTIVA + SECCIÓN TÉCNICA (14 módulos)
  Administrador→ ve: todo (igual que Técnico — verificación cruzada)

━━━ NAVEGACIÓN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  app.py llama render_sidebar_nav() para inyectar el menú en el sidebar.
  app.py llama render() para mostrar el contenido del módulo activo.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from utils.session import is_tecnico, is_admin, is_ejecutivo, get_rol


# ── Catálogo de módulos GOV ───────────────────────────────────────────────────
# (key, icon, label, tecnico_only)
# tecnico_only=True → solo visible para Técnico, Operador, Administrador
_GOV_MODULES: list[tuple[str, str, str, bool]] = [
    # ── Sección Ejecutiva (todos los roles GOV) ────────────────────────────
    ("inicio",       "🏠",  "Inicio",                      False),
    ("situacion",    "📊",  "Situación Institucional",      False),
    ("alertas",      "🚨",  "Alertas y Riesgos SAT",        False),
    ("municipal",    "🏛",  "Gestión Municipal",             False),
    ("ods",          "🌐",  "ODS y Metas PDOT",              False),
    ("confianza",    "🤝",  "Confianza Ciudadana",           False),
    ("rdc",          "📋",  "Rendición de Cuentas",          False),
    ("cooperacion",  "🌍",  "Cooperación Internacional",     False),
    ("genero",       "💜",  "Género y Ambiente",             False),
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

    Ejecutivo: micro-switcher de 2 modos (Vista Ejecutiva / Concejo).
               No es navegación clásica — es cambio de modo de operación.
    Técnico / Administrador: EJECUTIVO + TÉCNICO secciones.
    """
    # ── Ejecutivo: micro-switcher modo (Sprint C.2) ───────────────────────────
    if is_ejecutivo():
        modo_actual = st.session_state.get("ejecutivo_modo", "vista")

        st.sidebar.markdown(
            '<div style="font-size:9px;color:rgba(245,158,11,.4);letter-spacing:.1em;'
            'text-transform:uppercase;margin:12px 0 8px;font-weight:800">MODO ACTIVO</div>',
            unsafe_allow_html=True,
        )

        if st.sidebar.button(
            "🏛  Vista Ejecutiva",
            key="modo_vista",
            use_container_width=True,
            type="primary" if modo_actual == "vista" else "secondary",
        ):
            st.session_state["ejecutivo_modo"] = "vista"
            st.rerun()

        if st.sidebar.button(
            "🏛  Panel Estratégico",
            key="modo_concejo",
            use_container_width=True,
            type="primary" if modo_actual == "concejo" else "secondary",
        ):
            st.session_state["ejecutivo_modo"] = "concejo"
            st.rerun()

        st.sidebar.markdown(
            '<div style="font-size:8px;color:rgba(255,255,255,.15);'
            'margin-top:8px;line-height:1.5">Sprint C.2 · QUIRA Intelligence</div>',
            unsafe_allow_html=True,
        )
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
    try:
        from quira_pages.p0_inicio import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Inicio no disponible: {e}")


def _render_situacion() -> None:
    try:
        from quira_pages.m1_situacion import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Situación no disponible: {e}")


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


# ── Mapa key → (renderer, label) ─────────────────────────────────────────────
_MODULE_RENDER: dict[str, tuple] = {
    # Sección Ejecutiva
    "inicio":       (_render_inicio,       "Inicio"),
    "situacion":    (_render_situacion,    "Situación Institucional"),
    "alertas":      (_render_alertas,      "Alertas y Riesgos SAT"),
    "municipal":    (_render_municipal,    "Gestión Municipal"),
    "ods":          (_render_ods,          "ODS y Metas PDOT"),
    "confianza":    (_render_confianza,    "Confianza Ciudadana"),
    "rdc":          (_render_rdc,          "Rendición de Cuentas"),
    "cooperacion":  (_render_cooperacion,  "Cooperación Internacional"),
    "genero":       (_render_genero,       "Género y Ambiente"),
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

    Ejecutivo → Vista Ejecutiva Bloomberg-style (pantalla única, sin header GOV).
    Directivo / Administrador → módulo activo con header de identidad GOV.
    """
    # ── Ejecutivo: Vista Ejecutiva o Panel Estratégico (Sprint C.2) ─────────
    if is_ejecutivo():
        modo = st.session_state.get("ejecutivo_modo", "vista")
        if modo == "concejo":
            try:
                from quira_pages.p_concejo import render as _c
                _c()
            except Exception as e:
                st.error(f"Panel Estratégico no disponible: {e}")
        else:
            try:
                from quira_pages.p_vista_ejecutiva import render as _ve
                _ve()
            except Exception as e:
                st.error(f"Vista Ejecutiva no disponible: {e}")
        return

    # ── Técnico / Administrador: módulo activo con header GOV ─────────────────
    module_key = _current_module()
    fn, label  = _MODULE_RENDER.get(module_key, (_render_inicio, "Inicio"))
    _render_gov_header(label)
    fn()
