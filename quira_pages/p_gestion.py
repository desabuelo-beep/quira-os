"""
QUIRA OS · p_gestion.py
Ruta de Atención Institucional — Sprint 2.9A

Gobernanza operativa: estados formales, ownership, escalamiento,
circuito de revisión y bitácora inmutable por alerta.

Lenguaje institucional — sin terminología técnica.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st

from sentinel.governance_engine import (
    ESTADOS, TRANSITIONS, NIVELES,
    transition_alert, assign_alert, escalar_alert,
    get_gestion_kpis, get_alerts_for_gestion,
    get_alerts_summary_for_timeline, get_timeline,
)
from sentinel.alert_engine import ENTITY_LABELS

# ── CONSTANTES UI ─────────────────────────────────────────────────────────────
_TRANSITION_LABEL: dict[str, str] = {
    "en_revision": "Tomar en revisión",
    "derivada":    "Derivar a dirección",
    "resuelta":    "Registrar resolución",
    "observada":   "Observar — resolución insuficiente",
    "validada":    "Validar resolución",
    "archivada":   "Archivar — cierre institucional",
}

_NIVEL_OPTIONS = list(NIVELES.keys())
_NIVEL_LABELS  = list(NIVELES.values())


def _actor_from_session() -> str:
    return st.session_state.get("usuario", "analista")


def _badge(text: str, color: str = "#1A4A8C", text_color: str = "#FFF") -> str:
    return (
        f'<span style="background:{color};color:{text_color};padding:2px 8px;'
        f'border-radius:10px;font-size:0.77rem;font-weight:700">{text}</span>'
    )


# ── TAB 1 — GESTIÓN ACTIVA ────────────────────────────────────────────────────
def _tab_gestion(alertas: list[dict]) -> None:
    if not alertas:
        st.success("No hay alertas activas en seguimiento institucional.", icon="✅")
        return

    for a in alertas:
        meta   = a["estado_meta"]
        icon   = meta.get("icon", "•")
        color  = meta.get("color", "#666")
        label  = meta.get("label", a["estado"])
        dias   = a["dias_abierta"]
        titulo = a["titulo"]
        ent    = ENTITY_LABELS.get(a["entidad"], a["entidad"])

        dias_color = (
            "#8C1515" if dias >= 30 else
            "#8C5A00" if dias >= 15 else
            "#006B3C"
        )

        header = (
            f"{icon} **{titulo}** · `{a['entidad']}` · {a['periodo']} · "
            f"{label}"
        )
        if a.get("escalada"):
            header += f" · 🔺 Escalada"

        with st.expander(header, expanded=(a["estado"] in ("observada", "pendiente"))):
            c1, c2, c3 = st.columns(3)
            c1.markdown(
                f"**Responsable actual:**  \n"
                f"{a.get('owner_actual') or '_(sin asignar)_'}  \n"
                f"Nivel: {a['nivel_label']}"
            )
            c2.markdown(
                f"**Estado:**  \n"
                f"{icon} {label}"
            )
            c3.markdown(
                f"**Días abierta:**  \n"
                f"<span style='color:{dias_color};font-size:1.1rem;font-weight:700'>"
                f"{dias}d</span>",
                unsafe_allow_html=True,
            )

            if a.get("resolucion"):
                st.caption(f"Resolución registrada: _{a['resolucion'][:180]}_")

            st.markdown("---")

            # Asignación de responsable
            col_owner, col_nivel, col_asign = st.columns([2, 2, 1])
            with col_owner:
                owner_input = st.text_input(
                    "Asignar responsable",
                    value=a.get("owner_actual") or "",
                    key=f"owner_{a['id']}",
                    placeholder="Nombre del funcionario",
                    label_visibility="collapsed",
                )
            with col_nivel:
                nivel_idx = _NIVEL_OPTIONS.index(
                    a.get("nivel_escalamiento") or "analista"
                ) if (a.get("nivel_escalamiento") or "analista") in _NIVEL_OPTIONS else 0
                nivel_sel = st.selectbox(
                    "Nivel",
                    options=_NIVEL_OPTIONS,
                    format_func=lambda k: NIVELES[k],
                    index=nivel_idx,
                    key=f"nivel_{a['id']}",
                    label_visibility="collapsed",
                )
            with col_asign:
                if st.button("Asignar", key=f"asn_{a['id']}", use_container_width=True):
                    assign_alert(
                        a["id"], owner_input, nivel_sel,
                        actor=_actor_from_session(),
                        nota=f"Asignado a {owner_input} ({NIVELES[nivel_sel]})",
                    )
                    st.session_state.pop("gestion_cache", None)
                    st.success("Responsable actualizado.")
                    st.rerun()

            # Transiciones disponibles
            trans = a["transiciones"]
            if trans:
                nota_key = f"nota_{a['id']}"
                nota_val = st.text_area(
                    "Nota de la gestión",
                    key=nota_key,
                    placeholder="Justificación o contexto de la acción",
                    height=60,
                    label_visibility="collapsed",
                )

                btn_cols = st.columns(len(trans))
                for col_b, t in zip(btn_cols, trans):
                    t_label = _TRANSITION_LABEL.get(t["id"], t.get("label", t["id"]))
                    t_color = t.get("color", "#444")
                    with col_b:
                        if st.button(
                            f"{t.get('icon','•')} {t_label}",
                            key=f"tr_{a['id']}_{t['id']}",
                            use_container_width=True,
                        ):
                            ok = transition_alert(
                                a["id"], t["id"],
                                actor=_actor_from_session(),
                                nota=nota_val or None,
                                nivel=nivel_sel,
                            )
                            if ok:
                                st.session_state.pop("gestion_cache", None)
                                st.success(
                                    f"Estado actualizado a **{ESTADOS[t['id']]['label']}**. "
                                    f"Registrado en la bitácora institucional."
                                )
                                st.rerun()
                            else:
                                st.error("Transición no válida o alerta no encontrada.")

            # Escalamiento rápido
            if a["estado"] not in ("archivada",):
                with st.expander("🔺 Escalar a nivel superior", expanded=False):
                    esc_cols = st.columns([2, 1])
                    esc_nivel = esc_cols[0].selectbox(
                        "Nivel destino",
                        options=[k for k in _NIVEL_OPTIONS if k != "analista"],
                        format_func=lambda k: NIVELES[k],
                        key=f"esc_nivel_{a['id']}",
                        label_visibility="collapsed",
                    )
                    esc_nota = st.text_input(
                        "Motivo del escalamiento",
                        key=f"esc_nota_{a['id']}",
                        placeholder="Razón del escalamiento",
                        label_visibility="collapsed",
                    )
                    if esc_cols[1].button("Escalar", key=f"esc_{a['id']}", use_container_width=True):
                        escalar_alert(
                            a["id"], esc_nivel,
                            actor=_actor_from_session(),
                            nota=esc_nota or None,
                        )
                        st.session_state.pop("gestion_cache", None)
                        st.warning(f"Alerta escalada a {NIVELES[esc_nivel]}.")
                        st.rerun()


# ── TAB 2 — RUTA DE ATENCIÓN (TIMELINE) ──────────────────────────────────────
def _tab_timeline() -> None:
    alertas_lista = get_alerts_summary_for_timeline()
    if not alertas_lista:
        st.info("Sin alertas registradas aún.")
        return

    opciones = {
        a["id"]: (
            f"{ESTADOS.get(a['estado'],{}).get('icon','•')} "
            f"{a['titulo'][:55]} · {a['entidad']} · "
            f"{a.get('period_month','–')}/{a.get('period_year','–')}"
        )
        for a in alertas_lista
    }

    sel_id = st.selectbox(
        "Seleccionar alerta",
        options=list(opciones.keys()),
        format_func=lambda k: opciones[k],
    )

    if sel_id is None:
        return

    timeline = get_timeline(sel_id)
    if not timeline:
        st.caption("Sin eventos registrados para esta alerta.")
        return

    st.markdown("**Ruta de atención institucional:**")

    for i, ev in enumerate(timeline):
        ts         = ev.get("timestamp", "")[:16].replace("T", " ")
        actor      = ev.get("actor", "sistema")
        evento     = ev.get("evento", "")
        nota       = ev.get("nota", "")
        desde      = ev.get("estado_desde")
        hasta      = ev.get("estado_hasta")
        nivel      = ev.get("nivel", "")
        nivel_lbl  = NIVELES.get(nivel, nivel.title() if nivel else "")

        desde_meta = ESTADOS.get(desde or "", {})
        hasta_meta = ESTADOS.get(hasta or "", {})

        arrow = ""
        if desde and hasta:
            arrow = (
                f"{desde_meta.get('icon','•')} {desde_meta.get('label','–')} → "
                f"{hasta_meta.get('icon','•')} **{hasta_meta.get('label','–')}**"
            )
        elif hasta:
            arrow = f"{hasta_meta.get('icon','•')} **{hasta_meta.get('label','–')}**"

        is_last = (i == len(timeline) - 1)
        border  = "2px solid #1A4A8C" if is_last else "1px solid #DCE3F0"
        bg      = "#F0F4FF" if is_last else "#FAFBFF"

        _bloque_arrow = ("<div style='font-size:0.83rem;color:#555;"
                         "margin-top:2px'>" + arrow + "</div>") if arrow else ""
        _bloque_nota = ("<div style='font-size:0.82rem;color:#777;"
                        "font-style:italic;margin-top:4px'>› "
                        + nota + "</div>") if nota else ""
        st.markdown(
            f"<div style='border-left:{border};padding:8px 16px;margin-bottom:6px;"
            f"background:{bg};border-radius:0 6px 6px 0'>"
            f"<div style='font-size:0.78rem;color:#888;margin-bottom:2px'>"
            f"📅 {ts} &nbsp;·&nbsp; {nivel_lbl or actor}</div>"
            f"<div style='font-weight:700;color:#1A4A8C;font-size:0.92rem'>{evento}</div>"
            # ⚠️ El HTML se arma FUERA de la f-string. Python ≤3.11 prohíbe el
            # backslash dentro de la expresión (PEP 701 lo admite desde 3.12), y
            # el CI corre 3.11: aquí no compilaba, mientras el local con 3.13
            # decía que sí.
            f"{_bloque_arrow}"
            f"{_bloque_nota}"
            f"</div>",
            unsafe_allow_html=True,
        )


# ── TAB 3 — ESTADO GENERAL ────────────────────────────────────────────────────
def _tab_estado(kpis: dict) -> None:
    por_estado = kpis["por_estado"]

    st.markdown("**Distribución por estado institucional:**")
    rows_html = ""
    for estado_id, meta in ESTADOS.items():
        n = por_estado.get(estado_id, 0)
        if n == 0:
            continue
        rows_html += (
            f"<tr>"
            f"<td style='padding:8px 12px'>{meta['icon']} {meta['label']}</td>"
            f"<td style='padding:8px 12px;text-align:center;font-weight:700;"
            f"color:{meta['color']}'>{n}</td>"
            f"</tr>"
        )

    st.markdown(
        f"<table style='width:100%;border-collapse:collapse;font-size:0.9rem'>"
        f"<thead><tr style='background:#F0F4FF'>"
        f"<th style='padding:8px 12px;text-align:left;color:#444'>Estado</th>"
        f"<th style='padding:8px 12px;text-align:center;color:#444'>Alertas</th>"
        f"</tr></thead><tbody>{rows_html}</tbody></table>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.metric("🔺 Escaladas activas", kpis["escaladas"])
    c2.metric("⚠ Sin responsable asignado", kpis["sin_owner"])

    st.caption(
        "**Nota metodológica:** Los estados institucionales son gestionados exclusivamente "
        "por el equipo. El sistema registra cada acción en la bitácora pero no toma "
        "decisiones autónomas. Auditabilidad total — cada evento tiene actor y nota."
    )


# ── RENDER ────────────────────────────────────────────────────────────────────
def render() -> None:
    st.caption("**Ruta de Atención** · Seguimiento institucional de alertas")

    # ── Carga de datos ────────────────────────────────────────────────────────
    if "gestion_cache" not in st.session_state:
        kpis    = get_gestion_kpis()
        alertas = get_alerts_for_gestion(excluir_archivadas=True)
        st.session_state["gestion_cache"] = {"kpis": kpis, "alertas": alertas}

    cache   = st.session_state["gestion_cache"]
    kpis    = cache["kpis"]
    alertas = cache["alertas"]

    col_ref, _ = st.columns([1, 4])
    with col_ref:
        if st.button("↻ Actualizar", use_container_width=True):
            st.session_state.pop("gestion_cache", None)
            st.rerun()

    # ── KPI strip ─────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("🔴 Abiertas",         kpis["por_estado"].get("pendiente",   0))
    k2.metric("🟡 En Revisión",      kpis["por_estado"].get("en_revision", 0))
    k3.metric("🟠 Observadas",       kpis["por_estado"].get("observada",   0))
    k4.metric("🔹 En Validación",    kpis["en_validacion"])
    k5.metric("🟢 Archivadas",       kpis["archivadas"])

    st.markdown("---")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs([
        f"📋 Gestión Activa ({kpis['total_activas']})",
        "🗓 Ruta de Atención",
        "📊 Estado General",
    ])

    with tab1:
        _tab_gestion(alertas)

    with tab2:
        _tab_timeline()

    with tab3:
        _tab_estado(kpis)

    # ── Navegación ────────────────────────────────────────────────────────────
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔔 Ver Alertas", use_container_width=True):
            st.session_state["page"] = "alertas"
            st.rerun()
    with c2:
        if st.button("📊 Ver Seguimiento", use_container_width=True):
            st.session_state["page"] = "seguimiento"
            st.rerun()
