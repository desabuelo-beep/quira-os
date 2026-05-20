"""
QUIRA OS · p_ejecutivo.py
Vista Ejecutiva — Alcalde y Directivos RC-1

Responde solo las preguntas que le importan a la autoridad:
  ¿Cómo está el municipio hoy?
  ¿Qué requiere mi atención?
  ¿Qué está resuelto?

Sin terminología técnica. Sin tablas de datos. Solo semáforos y contexto.

Dylus Lab © 2026
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from sentinel.report_engine  import build_report_data
from sentinel.alert_engine   import get_alert_kpis, ENTITY_LABELS
from sentinel.sla_db         import get_sla_summary
from sentinel.db_config      import get_connection

_MESES = {
    1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril",
    5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto",
    9:"Septiembre", 10:"Octubre", 11:"Noviembre", 12:"Diciembre",
}

_STATUS_COLOR = {"ok": "#006B3C", "warning": "#8C5A00", "error": "#8C1515"}
_STATUS_BG    = {"ok": "#E6F4ED", "warning": "#FFF3CD", "error": "#FDECEA"}
_STATUS_ICON  = {"ok": "🟢", "warning": "🟡", "error": "🔴"}
_STATUS_LABEL = {"ok": "El municipio opera dentro de los parámetros normales.",
                 "warning": "Se detectan situaciones que requieren seguimiento.",
                 "error": "Hay indicadores críticos que requieren atención inmediata."}


def _semaforo_card(entidad: str, label: str, ti: float | None) -> str:
    if ti is None:
        status, valor = "error", "Sin datos"
    else:
        status = "ok" if ti >= 35 else ("warning" if ti >= 15 else "error")
        valor  = f"{ti:.1f}%"

    color = _STATUS_COLOR[status]
    bg    = _STATUS_BG[status]
    icon  = _STATUS_ICON[status]

    return f"""
<div style="border-radius:12px;background:{bg};border:2px solid {color}40;
            padding:18px 20px;text-align:center;height:100%">
  <div style="font-size:2rem;margin-bottom:6px">{icon}</div>
  <div style="font-weight:800;font-size:1rem;color:#1A1A1A;margin-bottom:4px">{label}</div>
  <div style="font-size:1.6rem;font-weight:900;color:{color};margin-bottom:4px">{valor}</div>
  <div style="font-size:0.78rem;color:#555">Ejecución de inversión</div>
</div>"""


def _atencion_card(titulo: str, entidad: str, periodo: str) -> str:
    return f"""
<div style="border-left:4px solid #8C1515;background:#FDECEA;border-radius:0 8px 8px 0;
            padding:10px 14px;margin-bottom:8px">
  <div style="font-weight:700;color:#8C1515;font-size:0.92rem">{titulo}</div>
  <div style="font-size:0.8rem;color:#666;margin-top:3px">{entidad} · {periodo}</div>
</div>"""


def render() -> None:
    today = date.today()
    year, month = today.year, today.month

    st.caption("**Vista Ejecutiva** · Estado institucional del Holding Municipal")

    # ── Selector de período ───────────────────────────────────────────────────
    c1, c2, _ = st.columns([1, 1, 3])
    year  = c1.number_input("Año", 2024, 2030, value=year, step=1)
    month = c2.number_input("Mes", 1, 12, value=month, step=1)
    mes_label = f"{_MESES.get(int(month), '')} {int(year)}"

    gen_key = f"ejecutivo_{int(year)}_{int(month)}"
    if st.button("Actualizar vista ejecutiva", type="primary") or gen_key not in st.session_state:
        with st.spinner(f"Cargando estado de {mes_label}…"):
            try:
                data = build_report_data(int(year), int(month))
                st.session_state[gen_key] = data
            except Exception as e:
                st.error(f"No se pudieron cargar los datos del período. Intentar con otro período.")
                return

    if gen_key not in st.session_state:
        st.info("Seleccione el período y presione **Actualizar vista ejecutiva**.")
        return

    data = st.session_state[gen_key]

    # ── Titular de estado ─────────────────────────────────────────────────────
    g_st  = data["global_status"]
    color = _STATUS_COLOR.get(g_st, "#333")
    bg    = _STATUS_BG.get(g_st, "#F5F5F5")
    icon  = _STATUS_ICON.get(g_st, "⬜")
    desc  = _STATUS_LABEL.get(g_st, "")

    st.markdown(
        f"<div style='background:{bg};border:2px solid {color}40;border-radius:16px;"
        f"padding:24px 28px;margin:12px 0 20px'>"
        f"<div style='font-size:2.5rem;margin-bottom:8px'>{icon}</div>"
        f"<div style='font-size:1.5rem;font-weight:900;color:{color};margin-bottom:6px'>"
        f"Estado — {mes_label}</div>"
        f"<div style='font-size:1rem;color:#444'>{desc}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Resumen ejecutivo Q&A ─────────────────────────────────────────────────
    sm = data["summary"]
    with st.expander("📋 Resumen para la autoridad", expanded=True):
        for pregunta, respuesta in [
            ("¿Cómo está el municipio?", sm["estado"]),
            ("¿Qué preocupa?",           sm["preocupa"]),
            ("¿Qué mejoró?",             sm["mejoro"]),
            ("¿Qué está pendiente?",     sm["pendiente"]),
        ]:
            st.markdown(f"**{pregunta}**  \n{respuesta}")
            st.markdown("---")

    # ── Semáforos por entidad ─────────────────────────────────────────────────
    st.markdown("### Estado por entidad del Holding Municipal")
    hkpis = data["holding_kpis"]
    ENTS  = ["GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"]
    cols  = st.columns(4)
    for i, ent in enumerate(ENTS):
        ti    = hkpis.get(ent)
        label = ENTITY_LABELS.get(ent, ent).split(" de ")[0]
        cols[i].markdown(
            _semaforo_card(ent, label, ti),
            unsafe_allow_html=True,
        )

    st.markdown("")

    # ── SLA Institucional (RC-2A) ─────────────────────────────────────────────
    try:
        _conn = get_connection()
        _sla  = get_sla_summary(_conn)
        _conn.close()

        _pct   = _sla["pct_cumplimiento"]
        _venc  = _sla["vencidas"]
        _esc   = _sla["escaladas"]
        _total = _sla["total_activas"]
        _alerta_global = _sla["alerta_global"]

        if _total > 0:
            _sla_clr  = "#8C1515" if _alerta_global else "#006B3C"
            _sla_bg   = "#FDECEA" if _alerta_global else "#E6F4ED"
            _sla_icon = "🔴" if _alerta_global else "🟢"
            _sla_lbl  = "Alertas fuera de plazo institucional" if _alerta_global else "Cumplimiento SLA dentro de parámetros"

            _detail_parts = []
            if _venc:
                _detail_parts.append(f"{_venc} vencida(s)")
            if _esc:
                _detail_parts.append(f"{_esc} escalada(s)")
            _en_t = _sla["en_tiempo"]
            _prox = _sla["proximo_vencer"]
            if _prox:
                _detail_parts.append(f"{_prox} próxima(s) a vencer")
            _detail_str = " · ".join(_detail_parts) if _detail_parts else f"{_en_t} dentro del plazo"

            st.markdown(
                f"<div style='background:{_sla_bg};border:2px solid {_sla_clr}40;"
                f"border-radius:12px;padding:16px 20px;margin:0 0 16px;"
                f"display:flex;align-items:center;gap:16px'>"
                f"<div style='font-size:1.8rem'>{_sla_icon}</div>"
                f"<div style='flex:1'>"
                f"<div style='font-weight:800;font-size:0.95rem;color:{_sla_clr}'>"
                f"SLA Institucional — {_pct:.0f}% de cumplimiento</div>"
                f"<div style='font-size:0.82rem;color:#555;margin-top:3px'>"
                f"{_sla_lbl} · {_detail_str}</div>"
                f"</div>"
                f"<div style='text-align:right'>"
                f"<div style='font-size:1.6rem;font-weight:900;color:{_sla_clr}'>{_pct:.0f}%</div>"
                f"<div style='font-size:0.72rem;color:#888'>{_total} alerta(s) activa(s)</div>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
    except Exception:
        pass  # SLA widget no bloquea la vista ejecutiva

    # ── Requiere atención (críticas activas) ──────────────────────────────────
    criticas = data.get("criticas", [])
    if criticas:
        st.markdown(f"### 🔴 Requiere atención — {len(criticas)} alerta(s) crítica(s)")
        for a in criticas:
            periodo = f"{a.get('period_month','–')}/{a.get('period_year','–')}"
            ent_lbl = ENTITY_LABELS.get(a.get('entidad',''), a.get('entidad',''))
            st.markdown(
                _atencion_card(
                    a.get("titulo", "Alerta institucional"),
                    ent_lbl.split(" de ")[0],
                    periodo,
                ),
                unsafe_allow_html=True,
            )
    else:
        st.success("Sin alertas críticas activas en el período. El municipio opera sin situaciones de urgencia.", icon="🟢")

    # ── Acción recomendada ────────────────────────────────────────────────────
    accion = sm.get("accion", "")
    if accion:
        st.info(f"**Acción recomendada por el equipo técnico:** {accion}", icon="📌")

    # ── Descarga PDF ejecutivo ────────────────────────────────────────────────
    st.markdown("---")
    col_pdf1, col_pdf2 = st.columns(2)

    # PDF del período activo (manual)
    with col_pdf1:
        try:
            from sentinel.report_engine import generate_pdf_bytes
            pdf = generate_pdf_bytes(data)
            if pdf:
                fname = f"estado_institucional_{int(year)}{int(month):02d}_{today.strftime('%Y%m%d')}.pdf"
                st.download_button(
                    label="📄 Informe Ejecutivo — Período seleccionado",
                    data=pdf,
                    file_name=fname,
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                )
        except Exception:
            pass

    # Digest automático del mes anterior (RC-2B)
    with col_pdf2:
        try:
            from sentinel.report_engine import build_report_data, generate_pdf_bytes
            # Calcular mes anterior automáticamente
            _mes_ant = today.month - 1 if today.month > 1 else 12
            _anio_ant = today.year if today.month > 1 else today.year - 1
            _mes_lbl  = _MESES.get(_mes_ant, str(_mes_ant))

            if st.button(
                f"📊 Digest Automático — {_mes_lbl} {_anio_ant}",
                use_container_width=True,
                help="Genera el informe del mes anterior automáticamente",
            ):
                with st.spinner(f"Generando digest de {_mes_lbl} {_anio_ant}…"):
                    try:
                        _data_ant = build_report_data(_anio_ant, _mes_ant)
                        _pdf_ant  = generate_pdf_bytes(_data_ant)
                        if _pdf_ant:
                            _fname_ant = (
                                f"digest_ejecutivo_{_anio_ant}{_mes_ant:02d}_"
                                f"{today.strftime('%Y%m%d')}.pdf"
                            )
                            st.download_button(
                                label=f"⬇ Descargar Digest {_mes_lbl} {_anio_ant}",
                                data=_pdf_ant,
                                file_name=_fname_ant,
                                mime="application/pdf",
                                use_container_width=True,
                            )
                        else:
                            st.info(f"No hay datos suficientes para {_mes_lbl} {_anio_ant}.")
                    except Exception:
                        st.info(f"Sin datos disponibles para {_mes_lbl} {_anio_ant}.")
        except Exception:
            pass

    # ── Navegación ────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔔 Ver gestión de alertas", use_container_width=True):
            st.session_state["page"] = "gestion"
            st.rerun()
    with c2:
        if st.button("📄 Ver reportes completos", use_container_width=True):
            st.session_state["page"] = "reportes"
            st.rerun()
