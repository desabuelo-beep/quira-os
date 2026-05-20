"""
QUIRA OS · p_aprendizaje.py
Aprendizaje Institucional Trazable — Sprint 2.8A

Muestra cómo el sistema aprende de las resoluciones humanas:
categorías de resolución, frecuencias, tiempos y ejemplos auditables.

Lenguaje institucional — sin terminología técnica.

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from sentinel.learning_engine import (
    get_learning_stats,
    get_pattern_ranking,
    run_pattern_extraction,
    CATEGORIAS,
    _OTRO_LABEL,
)
from sentinel.alert_engine import ENTITY_LABELS

_CAT_ICON = {
    "reforma_presupuestaria":       "📋",
    "retraso_documental":           "📄",
    "proceso_contractual":          "🤝",
    "certificacion_presupuestaria": "✅",
    "decision_directiva":           "🏛",
    "ingesta_completada":           "📥",
    "automatico":                   "⚙",
    "otro":                         "❓",
}

_COL_HEADER  = "#F0F4FF"
_COL_ROW_A   = "#FFFFFF"
_COL_ROW_B   = "#F8F9FA"
_COL_ACCENT  = "#1A4A8C"


# ── HELPERS HTML ──────────────────────────────────────────────────────────────
def _badge(text: str, color: str = "#1A4A8C") -> str:
    return (
        f'<span style="background:{color};color:#FFF;padding:2px 8px;'
        f'border-radius:10px;font-size:0.78rem;font-weight:600">{text}</span>'
    )


def _patron_html(patrones: list[dict]) -> str:
    if not patrones:
        return "<p style='color:#888'>Sin patrones registrados aún. Ejecuta la extracción.</p>"

    rows = ""
    for i, p in enumerate(patrones):
        bg     = _COL_ROW_A if i % 2 == 0 else _COL_ROW_B
        icon   = _CAT_ICON.get(p["categoria"], "❓")
        label  = p["label_display"] or _OTRO_LABEL
        freq   = p["frecuencia"]
        dias   = p["tiempo_promedio_dias"]
        ents   = p.get("entidades_afectadas") or []
        ents_s = ", ".join(
            ENTITY_LABELS.get(e, e).split(" de ")[0] for e in ents
        ) if ents else "–"
        primera = (p.get("primera_vez") or "")[:10] or "–"
        ultima  = (p.get("ultima_vez")  or "")[:10] or "–"

        freq_badge = _badge(f"{freq} caso{'s' if freq != 1 else ''}")
        dias_badge = _badge(
            f"{dias}d prom.",
            "#006B3C" if dias <= 7 else ("#8C5A00" if dias <= 21 else "#8C1515"),
        )

        rows += f"""
        <tr style="background:{bg}">
            <td style="padding:10px 12px;font-size:1rem">{icon}</td>
            <td style="padding:10px 12px;font-weight:600;color:{_COL_ACCENT}">{label}</td>
            <td style="padding:10px 12px;text-align:center">{freq_badge}</td>
            <td style="padding:10px 12px;text-align:center">{dias_badge}</td>
            <td style="padding:10px 12px;font-size:0.85rem;color:#555">{ents_s}</td>
            <td style="padding:10px 12px;font-size:0.82rem;color:#777">{primera}</td>
            <td style="padding:10px 12px;font-size:0.82rem;color:#777">{ultima}</td>
        </tr>"""

    header_style = (
        f"background:{_COL_HEADER};font-size:0.8rem;text-transform:uppercase;"
        f"color:#444;letter-spacing:.05em;padding:8px 12px"
    )
    return f"""
    <div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse;font-family:sans-serif">
        <thead>
            <tr>
                <th style="{header_style}"></th>
                <th style="{header_style}">Categoría</th>
                <th style="{header_style};text-align:center">Frecuencia</th>
                <th style="{header_style};text-align:center">Tiempo Prom.</th>
                <th style="{header_style}">Entidades</th>
                <th style="{header_style}">Primera vez</th>
                <th style="{header_style}">Última vez</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    </div>"""


def _ejemplos_html(patrones: list[dict]) -> str:
    if not patrones:
        return ""

    cards = ""
    for p in patrones:
        ejemplos = p.get("ejemplos") or []
        if not ejemplos:
            continue
        icon  = _CAT_ICON.get(p["categoria"], "❓")
        label = p["label_display"] or _OTRO_LABEL
        items = "".join(
            f'<li style="margin:4px 0;color:#444;font-size:0.88rem">"{ej}"</li>'
            for ej in ejemplos
        )
        cards += f"""
        <div style="border:1px solid #DCE3F0;border-radius:8px;padding:14px 16px;
                    margin-bottom:12px;background:#FAFBFF">
            <div style="font-weight:700;color:{_COL_ACCENT};margin-bottom:8px">
                {icon} {label}
            </div>
            <ul style="margin:0;padding-left:18px">{items}</ul>
        </div>"""
    return cards or "<p style='color:#888'>Sin ejemplos disponibles.</p>"


# ── RENDER ────────────────────────────────────────────────────────────────────
def render() -> None:
    st.caption("**Aprendizaje Institucional** · Patrones de resolución trazables")

    # ── Extracción ────────────────────────────────────────────────────────────
    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        if st.button("🔄 Actualizar Aprendizaje", use_container_width=True, type="primary"):
            with st.spinner("Clasificando resoluciones institucionales…"):
                result = run_pattern_extraction()
            if result["procesadas"] == 0:
                st.info(
                    "No hay alertas resueltas con justificación registrada aún. "
                    "El aprendizaje se activa cuando el equipo registra resoluciones.",
                    icon="ℹ️",
                )
            else:
                st.success(
                    f"Aprendizaje actualizado: {result['procesadas']} resolución(es) "
                    f"clasificadas en {result['categorias_actualizadas']} categoría(s).",
                    icon="✅",
                )
            st.session_state["aprendizaje_cache"] = None  # invalidar caché

    with col_info:
        st.info(
            "El sistema clasifica automáticamente las justificaciones registradas por el equipo "
            "para detectar patrones recurrentes. **No toma decisiones — solo informa.**",
            icon="🤖",
        )

    st.markdown("---")

    # ── Cargar datos ──────────────────────────────────────────────────────────
    if st.session_state.get("aprendizaje_cache") is None:
        stats    = get_learning_stats()
        patrones = get_pattern_ranking()
        st.session_state["aprendizaje_cache"] = {"stats": stats, "patrones": patrones}
    else:
        stats    = st.session_state["aprendizaje_cache"]["stats"]
        patrones = st.session_state["aprendizaje_cache"]["patrones"]

    # ── KPIs ──────────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📋 Resoluciones clasificadas", stats["con_resolucion"])
    k2.metric("📂 Categorías identificadas",  stats["n_patrones"])
    k3.metric("📊 Cobertura",                 f"{stats['cobertura_pct']}%")
    k4.metric("❓ Sin justificación",         stats["sin_resolucion"])

    if stats["ultima_extraccion"]:
        ts = (stats["ultima_extraccion"] or "")[:19].replace("T", " ")
        st.caption(f"Última actualización: {ts} UTC")

    st.markdown("---")

    # ── Ranking de patrones ───────────────────────────────────────────────────
    with st.expander("📊 Ranking de Causas de Resolución", expanded=True):
        st.markdown(
            "Cómo resolvió el equipo institucional sus alertas — ordenado por frecuencia."
        )
        st.markdown(
            _patron_html(patrones),
            unsafe_allow_html=True,
        )

    # ── Ejemplos de resoluciones ──────────────────────────────────────────────
    with st.expander("📝 Ejemplos de Justificaciones Registradas", expanded=False):
        st.markdown(
            "Extractos literales de las justificaciones ingresadas, agrupados por categoría. "
            "Auditables en cualquier momento."
        )
        st.markdown(
            _ejemplos_html(patrones),
            unsafe_allow_html=True,
        )

    # ── Catálogo de categorías ────────────────────────────────────────────────
    with st.expander("🗂 Catálogo de Categorías del Sistema", expanded=False):
        st.markdown(
            "El sistema reconoce las siguientes categorías mediante palabras clave. "
            "Auditables y sin inteligencia artificial opaca."
        )
        for cat_id, meta in CATEGORIAS.items():
            icon  = _CAT_ICON.get(cat_id, "❓")
            kws   = " · ".join(f"`{k}`" for k in meta["keywords"][:6])
            st.markdown(f"**{icon} {meta['label']}** — {kws}")

    # ── Nota metodológica ─────────────────────────────────────────────────────
    st.markdown("---")
    st.caption(
        "**Nota metodológica:** El aprendizaje institucional clasifica solo justificaciones "
        "ingresadas manualmente por el equipo. No modifica alertas, no toma decisiones y no "
        "accede a información externa. Toda categorización es auditable y reversible."
    )

    # ── Navegación ────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔔 Ver Alertas", use_container_width=True):
            st.session_state["page"] = "alertas"
            st.rerun()
    with c2:
        if st.button("📊 Ver Seguimiento", use_container_width=True):
            st.session_state["page"] = "seguimiento"
            st.rerun()
