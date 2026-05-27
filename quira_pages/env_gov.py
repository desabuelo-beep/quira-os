"""
QUIRA Intelligence — Ambiente 🏛 GOV  (Router v3 · Sprint A · 2026-05-27)
QUIRA Institucional — Monitoreo preventivo para GADs del Ecuador.

Regla doctrinal permanente:
  env_gov.py ES UN ROUTER. No contiene contenido ni lógica de negocio.
  El contenido vive en m1-m4 y p0_inicio.
  Módulos nuevos = archivo nuevo + una línea aquí.
  Nunca agregar HTML, métricas ni tabs directamente en este archivo.

Módulos activos:
  inicio    → p0_inicio.py       (todos los roles GOV)
  situacion → m1_situacion.py    (todos los roles GOV)
  alertas   → m2_alertas.py      (todos los roles GOV)
  municipal → m3_municipal.py    (todos los roles GOV)
  analisis  → m4_analisis.py     (Técnico, Operador, Administrador)

Navegación:
  - app.py llama render_sidebar_nav() para inyectar el menú en el sidebar.
  - app.py llama render() para mostrar el contenido del módulo activo.

Roles GOV:
  Directivo    → ve: inicio, situacion, alertas, municipal
  Técnico      → ve: inicio, situacion, alertas, municipal, analisis
  Administrador→ ve: todo (verificación cruzada)

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
from utils.session import is_tecnico, is_admin, get_rol


# ── Catálogo de módulos GOV ──────────────────────────────────────────────────
# (key, icon, label, visible_para_tecnico+, visible_para_admin)
_GOV_MODULES: list[tuple[str, str, str]] = [
    ("inicio",     "🏠",  "Inicio"),
    ("situacion",  "📊",  "Situación Institucional"),
    ("alertas",    "🚨",  "Alertas y Riesgos"),
    ("municipal",  "🏛",  "Gestión Municipal"),
    ("analisis",   "📈",  "Análisis Estratégico"),   # solo Técnico+
]


def _can_see(module_key: str) -> bool:
    """Determina si el rol actual puede ver este módulo."""
    if module_key == "analisis":
        return is_tecnico() or is_admin()
    return True  # todos los roles GOV ven el resto


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
    """
    current_mod = _current_module()

    st.sidebar.markdown(
        '<div style="font-size:9px;color:rgba(255,255,255,.25);letter-spacing:.08em;'
        'text-transform:uppercase;margin:12px 0 6px">MÓDULOS GOV</div>',
        unsafe_allow_html=True,
    )

    for key, icon, label in _GOV_MODULES:
        if not _can_see(key):
            continue

        is_active = (key == current_mod)
        btn_style = ""
        if is_active:
            btn_style = (
                "background:rgba(0,212,255,.12)!important;"
                "border-color:rgba(0,212,255,.35)!important;"
                "color:#00D4FF!important;"
            )

        # Label con punto activo para el módulo seleccionado
        display = f"{icon}  {label}"

        if st.sidebar.button(
            display,
            key=f"gov_mod_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
            help=label,
        ):
            st.session_state["gov_module"] = key
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# Header GOV — identificador visual en el contenido
# ══════════════════════════════════════════════════════════════════════════════

def _render_gov_header(module_label: str) -> None:
    """Banda superior con identidad GOV y módulo activo."""
    rol = get_rol()
    rol_badge_color = {
        "Directivo":     "#00D4FF",
        "Técnico":       "#22C55E",
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
# Render de cada módulo
# ══════════════════════════════════════════════════════════════════════════════

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


def _render_analisis() -> None:
    try:
        from quira_pages.m4_analisis import render as _r
        _r()
    except Exception as e:
        st.error(f"Módulo Análisis no disponible: {e}")


# ── Mapa key → renderer ───────────────────────────────────────────────────────
_MODULE_RENDER = {
    "inicio":    (_render_inicio,    "Inicio"),
    "situacion": (_render_situacion, "Situación Institucional"),
    "alertas":   (_render_alertas,   "Alertas y Riesgos"),
    "municipal": (_render_municipal, "Gestión Municipal"),
    "analisis":  (_render_analisis,  "Análisis Estratégico"),
}


# ══════════════════════════════════════════════════════════════════════════════
# Entry point — llamado desde app.py
# ══════════════════════════════════════════════════════════════════════════════

def render() -> None:
    """Renderiza el módulo GOV activo."""
    module_key = _current_module()
    fn, label  = _MODULE_RENDER.get(module_key, (_render_inicio, "Inicio"))

    _render_gov_header(label)
    fn()
