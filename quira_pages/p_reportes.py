"""
QUIRA OS · p_reportes.py
Reportes Institucionales Mensuales — Sprint 2.6.3

Genera el PDF ejecutivo de corte mensual del Holding Municipal.
Artefacto oficial para: alcalde, concejales, dirección financiera,
auditoría interna, Contraloría, LOTAIP, rendición de cuentas.

Lenguaje institucional — sin terminología técnica.

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import date, datetime

import streamlit as st

from sentinel.report_engine import build_report_data, generate_pdf_bytes
from sentinel.alert_engine  import ENTITY_LABELS

MESES_ES = {
    1: "Enero",  2: "Febrero", 3: "Marzo",     4: "Abril",
    5: "Mayo",   6: "Junio",   7: "Julio",     8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

_STATUS_ICON  = {"ok": "🟢", "warning": "🟡", "error": "🔴"}
_STATUS_LABEL = {"ok": "Estable", "warning": "Requiere Atención", "error": "Crítico"}
_TIPO_LABEL   = {"ejecucion": "Ejecución", "cobertura": "Cobertura"}
_ESTADO_LABEL = {
    "pendiente":   "🔴 Abierta",
    "en_revision": "🟡 En Revisión",
    "resuelta":    "🟢 Resuelta",
}


# ── RENDER ────────────────────────────────────────────────────────────────────
def render() -> None:
    st.caption("**Reportes Institucionales** · PDF ejecutivo mensual")

    # ── Selector de período ───────────────────────────────────────────────────
    today = date.today()
    c1, c2, c3 = st.columns([2, 2, 3])
    year  = c1.number_input("Año", min_value=2024, max_value=2030,
                            value=today.year, step=1)
    month = c2.number_input("Mes", min_value=1,    max_value=12,
                            value=today.month, step=1)
    period_label = f"{MESES_ES.get(int(month), str(month))} {int(year)}"

    with c3:
        st.markdown(f"**Período seleccionado:** {period_label}")

    st.markdown("---")

    # ── Botón de generación ───────────────────────────────────────────────────
    col_gen, col_info = st.columns([1, 2])
    with col_gen:
        generate = st.button("📄 Generar Reporte Institucional",
                             use_container_width=True, type="primary")
    with col_info:
        st.info(
            "Genera el PDF ejecutivo oficial del período. Incluye: "
            "estado del Holding, alertas con resoluciones, congruencia e integridad. "
            "**Listo para auditoría y LOTAIP.**",
            icon="ℹ️",
        )

    # ── Generar / usar caché ──────────────────────────────────────────────────
    cache_key = f"reporte_{int(year)}_{int(month)}"
    if generate or cache_key not in st.session_state:
        with st.spinner(f"Consolidando estado institucional de {period_label}…"):
            data = build_report_data(int(year), int(month))
            st.session_state[cache_key]            = data
            st.session_state[f"{cache_key}_ready"] = True

    if f"{cache_key}_ready" not in st.session_state:
        st.markdown(
            "Selecciona el período y presiona **Generar Reporte Institucional**."
        )
        return

    data = st.session_state[cache_key]

    # ── Vista previa institucional (nativa Streamlit) ─────────────────────────
    g_st  = data["global_status"]
    g_lbl = _STATUS_LABEL.get(g_st, "–")
    icon  = _STATUS_ICON.get(g_st, "⬜")

    st.markdown(f"### {icon} {g_lbl} — {period_label}")

    # ── Resumen ejecutivo ─────────────────────────────────────────────────────
    with st.expander("📋 Resumen Ejecutivo", expanded=True):
        sm = data["summary"]
        for q, a in [
            ("¿Cómo está el municipio?", sm["estado"]),
            ("¿Qué preocupa?",           sm["preocupa"]),
            ("¿Qué mejoró?",             sm["mejoro"]),
            ("¿Qué está pendiente?",     sm["pendiente"]),
            ("Acción recomendada",       sm["accion"]),
        ]:
            st.markdown(f"**{q}**  \n{a}")
            st.markdown("---")

    # KPIs rápidos
    kpis = data["kpis"]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🔴 Críticas activas",      kpis["criticas_activas"])
    k2.metric("🟡 Advertencias activas",  kpis["advertencias_activas"])
    k3.metric("🟢 Resueltas",             kpis["resueltas_este_mes"])
    k4.metric("📅 Días sin resolver",     f"{kpis['dias_abierta_max']}d")

    # ── Estado del Holding ────────────────────────────────────────────────────
    with st.expander("🏛 Estado del Holding Municipal", expanded=True):
        hkpis  = data["holding_kpis"]
        ENTS   = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]
        cols   = st.columns(4)
        for i, ent in enumerate(ENTS):
            ti = hkpis.get(ent)
            if ti is None:
                st_v, ti_str = "error", "Sin datos"
            else:
                ti_str = f"{ti:.2f}%"
                st_v   = "ok" if ti >= 35 else ("warning" if ti >= 15 else "error")
            icn = _STATUS_ICON[st_v]
            cols[i].metric(
                ENTITY_LABELS.get(ent, ent).split(" de ")[0],
                ti_str,
                delta=f"{icn} {_STATUS_LABEL[st_v]}",
                delta_color="off",
            )

    # ── Alertas institucionales ───────────────────────────────────────────────
    with st.expander(
        f"🔔 Alertas Institucionales ({len(data['criticas'])} críticas · "
        f"{len(data['en_revision'])} en revisión · {len(data['resueltas'])} resueltas)",
        expanded=False,
    ):
        # Críticas
        if data["criticas"]:
            st.markdown("**🔴 Alertas Críticas**")
            for a in data["criticas"]:
                st.error(
                    f"**{a.get('titulo','')}** · `{a.get('entidad','')}` · "
                    f"Período: {a.get('period_month','')}/{a.get('period_year','')}"
                )
        else:
            st.success("Sin alertas críticas en el período.")

        # En revisión con resolución
        if data["en_revision"]:
            st.markdown("**🟡 Alertas en Revisión**")
            for a in data["en_revision"]:
                res = a.get("resolucion") or "_Sin justificación registrada_"
                st.warning(
                    f"**{a.get('titulo','')}** · `{a.get('entidad','')}` \n\n"
                    f"Justificación: *{res[:200]}*"
                )

        # Resueltas
        if data["resueltas"]:
            st.markdown("**🟢 Resueltas en el período**")
            for a in data["resueltas"]:
                res = a.get("resolucion") or "_Resuelta automáticamente_"
                st.success(
                    f"**{a.get('titulo','')}** · `{a.get('entidad','')}` \n\n"
                    f"Resolución: *{res[:200]}*"
                )

    # ── Congruencia e integridad ──────────────────────────────────────────────
    with st.expander("🔗 Congruencia e Integridad", expanded=False):
        cong  = data["congruencia"]
        integ = data["integridad"]

        co1, co2, co3 = st.columns(3)
        for col_w, key, lbl in [
            (co1, "fuente",  "Fuente Operativa"),
            (co2, "memoria", "Memoria Institucional"),
            (co3, "motor",   "Motor Analítico"),
        ]:
            st_val = (cong.get(key) or {}).get("status", "error")
            col_w.metric(lbl, _STATUS_ICON[st_val] + " " + _STATUS_LABEL[st_val])

        st.markdown(
            f"**Integridad semántica:** "
            f"{integ.get('n_ok', 0)}/{integ.get('n_total', 0)} indicadores correctos — "
            f"{integ.get('label', '–')}"
        )

    # ── Reincidencia ──────────────────────────────────────────────────────────
    reinc = data.get("reincidencia", [])
    if reinc:
        with st.expander(f"⚠ Reincidencia — {len(reinc)} patrón(es) detectado(s)", expanded=False):
            for r in reinc:
                tag = "🔴 Patrón estructural" if r["es_patron"] else "🟡 Repetido"
                st.markdown(
                    f"**{r['entidad_label']}** · {_TIPO_LABEL.get(r['tipo'], r['tipo'].title())} · "
                    f"{r['n_periodos']} períodos · {tag} · "
                    f"Primera vez: {r['primera_vez']} · Última: {r['ultima_vez']}"
                )

    st.markdown("---")

    # ── Descarga PDF ──────────────────────────────────────────────────────────
    with st.spinner("Preparando PDF institucional…"):
        pdf_bytes = generate_pdf_bytes(data)

    if pdf_bytes:
        file_name = (
            f"estado_institucional_{int(year)}{int(month):02d}_"
            f"{date.today().strftime('%Y%m%d')}.pdf"
        )
        st.download_button(
            label="📄 Descargar PDF Ejecutivo Institucional",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
        st.caption(
            f"PDF generado · {period_label} · "
            f"Listo para LOTAIP, auditoría y rendición de cuentas."
        )
    else:
        st.error(
            "No se pudo generar el PDF. Verifica que `reportlab` esté instalado: "
            "`pip install reportlab`"
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
