"""
QUIRA OS · p_alertas.py
Centro de Alertas de Cumplimiento — Sprint 2.6

Muestra alertas automáticas generadas por alert_engine:
  • Ejecución  — Ti inversión vs umbrales y trayectoria
  • Cobertura  — entidades sin evidencia mensual

Visible para analista, director y alcalde.
Lenguaje institucional — sin terminología técnica.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from quira_pages.html_engine import DEMO_CSS, page_frame, page_header
from sentinel.alert_engine import (
    run_alert_check, get_alerts_history, get_alert_kpis, get_tendencias,
    mark_en_revision, resolve_alert_with_comment,
    OK, WARNING, ERROR, ESTADO_ABIERTA, ESTADO_EN_REVISION, ESTADO_RESUELTA,
)
from sentinel.snapshot_engine import export_alerts_xlsx
from sentinel.learning_engine import get_context_for_alert, build_resolution_suggestion
from sentinel.sla_db import sla_badge_html, compute_sla_status

# ── CSS ───────────────────────────────────────────────────────────────────────
EXTRA_CSS = """
.alert-summary {
  display: flex; gap: 12px; justify-content: center;
  margin-bottom: 20px; flex-wrap: wrap;
}
.alert-chip {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 18px; border-radius: 20px;
  font-size: 13px; font-weight: 700;
}
.alert-card {
  background: var(--navy-card); border-radius: 12px;
  border: 1px solid var(--divider);
  margin-bottom: 10px; overflow: hidden;
  position: relative;
}
.alert-card-accent {
  position: absolute; top: 0; left: 0; bottom: 0;
  width: 4px; border-radius: 12px 0 0 12px;
}
.alert-card-body {
  padding: 14px 16px 14px 22px;
}
.alert-top {
  display: flex; align-items: flex-start; gap: 10px;
  margin-bottom: 6px;
}
.alert-sev-badge {
  font-size: 9px; font-weight: 800; letter-spacing: .06em;
  padding: 2px 8px; border-radius: 10px;
  white-space: nowrap; margin-top: 2px;
  text-transform: uppercase;
}
.alert-titulo {
  font-size: 13px; font-weight: 700; color: var(--white);
  flex: 1; line-height: 1.4;
}
.alert-meta {
  display: flex; gap: 14px; margin-bottom: 8px;
  font-size: 10px; color: var(--muted);
}
.alert-detalle {
  font-size: 11px; color: rgba(255,255,255,.65);
  line-height: 1.6; margin-bottom: 8px;
}
.alert-accion {
  font-size: 10px; font-weight: 700;
  padding: 6px 10px; border-radius: 6px;
  background: rgba(0,212,255,.06);
  border: 1px solid rgba(0,212,255,.15);
  color: var(--cyan);
  line-height: 1.5;
}
.alert-accion::before { content: "Acción recomendada: "; opacity: .6; }

.no-alerts {
  text-align: center; padding: 40px 20px;
}
.no-alerts-icon { font-size: 40px; margin-bottom: 12px; }
.no-alerts-label {
  font-size: 15px; font-weight: 700; color: var(--green);
  margin-bottom: 6px;
}
.no-alerts-sub {
  font-size: 11px; color: var(--muted);
}

.section-label {
  font-size: 10px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em;
  margin: 16px 0 8px;
}
.ts-footer {
  text-align: center; font-size: 9px; color: var(--muted);
  margin-top: 16px;
}

/* ── Tendencias ── */
.tend-grid {
  display: grid; grid-template-columns: repeat(2, 1fr);
  gap: 10px; margin-bottom: 14px;
}
@media (max-width: 600px) { .tend-grid { grid-template-columns: 1fr; } }
.tend-card {
  border-radius: 10px; padding: 12px 14px;
  font-size: 11px; border: 1px solid var(--divider);
}
.tend-ent { font-weight: 700; margin-bottom: 4px; }
.tend-msg { color: rgba(255,255,255,.65); }

/* ── Historial ── */
.hist-section-label {
  font-size: 10px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em;
  margin: 20px 0 10px;
  padding-top: 16px; border-top: 1px solid var(--divider);
}
.ah-row {
  display: grid;
  grid-template-columns: 90px 80px 90px 1fr 70px;
  gap: 8px; align-items: center;
  padding: 6px 4px; border-bottom: 1px solid rgba(255,255,255,.04);
  font-size: 10px;
}
.ah-row:last-child { border-bottom: none; }
.ah-head {
  font-size: 9px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .06em;
}
.ah-dot {
  width: 7px; height: 7px; border-radius: 50%;
  display: inline-block; margin-right: 5px;
}
.ah-estado-badge {
  font-size: 9px; font-weight: 700; padding: 2px 7px;
  border-radius: 8px; white-space: nowrap;
}
"""

# ── COLORES ───────────────────────────────────────────────────────────────────
_CLR = {OK: "var(--green)", WARNING: "var(--amber)", ERROR: "var(--red)"}
_BG  = {OK: "rgba(0,224,150,.08)", WARNING: "rgba(255,184,0,.08)", ERROR: "rgba(255,77,109,.08)"}
_BDR = {OK: "rgba(0,224,150,.25)", WARNING: "rgba(255,184,0,.25)", ERROR: "rgba(255,77,109,.25)"}
_ACCENT = {OK: "#00E096", WARNING: "#FFB800", ERROR: "#FF4D6D"}

_TIPO_ICON  = {"ejecucion": "📊", "cobertura": "📋"}
_TIPO_LABEL = {"ejecucion": "Ejecución", "cobertura": "Cobertura Documental"}


# ── HELPERS HTML ──────────────────────────────────────────────────────────────
def _chip(label: str, count: int, status: str) -> str:
    if count == 0:
        return ""
    clr = _CLR[status]
    bg  = _BG[status]
    bdr = _BDR[status]
    return (
        f'<div class="alert-chip" style="background:{bg};color:{clr};border:1px solid {bdr}">'
        f'{label}: {count}</div>'
    )


def _alert_card(alert: dict) -> str:
    st_  = alert["status"]
    clr  = _CLR.get(st_, "var(--white)")
    acc  = _ACCENT.get(st_, "#666")
    bg   = _BG.get(st_, "transparent")
    bdr  = _BDR.get(st_, "var(--divider)")
    sev  = alert["severidad"]
    tipo_icon  = _TIPO_ICON.get(alert["tipo"], "•")
    tipo_label = _TIPO_LABEL.get(alert["tipo"], alert["tipo"].title())

    sev_bg  = "rgba(255,77,109,.15)" if st_ == ERROR else "rgba(255,184,0,.12)"
    sev_clr = _CLR.get(st_, clr)

    valor_str = ""
    if alert.get("valor") is not None:
        v = alert["valor"]
        unit = "%" if alert["tipo"] == "ejecucion" else ""
        sign = "+" if v > 0 else ""
        valor_str = f'<span style="color:{clr};font-weight:700">{sign}{v:.2f}{unit}</span> · '

    # SLA badge — usa campos ya presentes en el dict si vienen de alerts_history
    sla_st  = alert.get("sla_status") or "EN_TIEMPO"
    sla_hrs = alert.get("sla_hours_remaining")
    if sla_hrs is None and alert.get("sla_target_hours") and alert.get("detected_at"):
        # Recalcular en tiempo real si no viene precalculado
        sla_st, sla_hrs = compute_sla_status(
            alert.get("detected_at", ""),
            int(alert.get("sla_target_hours") or 48),
            alert.get("estado", ""),
            int(alert.get("escalada") or 0),
        )
    sla_html = sla_badge_html(sla_st, sla_hrs)

    return f"""
<div class="alert-card" style="background:{bg};border-color:{bdr}">
  <div class="alert-card-accent" style="background:{acc}"></div>
  <div class="alert-card-body">
    <div class="alert-top">
      <div class="alert-sev-badge" style="background:{sev_bg};color:{sev_clr}">
        {sev}
      </div>
      <div class="alert-titulo">{alert['titulo']}</div>
    </div>
    <div class="alert-meta">
      <span>{tipo_icon} {tipo_label}</span>
      <span>📅 {alert['periodo']}</span>
      <span>🏛 {alert['entidad_label']}</span>
      {f'<span>{valor_str}</span>' if valor_str else ''}
      {sla_html}
    </div>
    <div class="alert-detalle">{alert['detalle']}</div>
    {f'<div class="alert-accion">{alert["accion"]}</div>' if alert.get("accion") else ''}
  </div>
</div>"""


_TIPO_LABEL_SHORT = {"ejecucion": "Ejecución", "cobertura": "Cobertura"}


def _tendencias_html(tendencias: list[dict]) -> str:
    if not tendencias:
        return ""
    _DOT = {"error": "#FF4D6D", "warning": "#FFB800", "ok": "#00E096"}
    cards = ""
    for t in tendencias:
        clr = _DOT.get(t.get("status", "ok"), "#666")
        bg  = {"error": "rgba(255,77,109,.07)", "warning": "rgba(255,184,0,.07)"}.get(
            t.get("status", ""), "rgba(0,224,150,.07)")
        cards += f"""
<div class="tend-card" style="background:{bg};border-color:{clr}40">
  <div class="tend-ent" style="color:{clr}">{t['entidad_label']}</div>
  <div class="tend-msg">{t['mensaje']}</div>
</div>"""
    return f"""
<div style="font-size:10px;font-weight:700;color:var(--muted);
            text-transform:uppercase;letter-spacing:.08em;margin:16px 0 8px;
            padding-top:14px;border-top:1px solid var(--divider)">
  Tendencias Detectadas
</div>
<div class="tend-grid">{cards}</div>"""


def _historial_section_html(history: list[dict]) -> str:
    if not history:
        return ""

    _DOT = {"error": "#FF4D6D", "warning": "#FFB800", "ok": "#00E096"}

    header = """
<div class="hist-section-label">Memoria de Alertas — Historial</div>
<div class="ah-row ah-head">
  <span>Período</span><span>Entidad</span><span>Tipo</span>
  <span>Alerta</span><span>Estado</span>
</div>"""

    rows = ""
    for h in history[:40]:
        dot_clr   = _DOT.get(h.get("status", ""), "#666")
        periodo   = f"{h.get('period_month', '–')}/{h.get('period_year', '–')}"
        tipo_lbl  = _TIPO_LABEL_SHORT.get(h.get("tipo", ""), h.get("tipo", "–"))
        titulo    = (h.get("titulo") or "")[:55]
        estado    = h.get("estado", "pendiente")

        if estado == "resuelta":
            est_bg  = "rgba(0,224,150,.12)"
            est_clr = "#00E096"
            est_lbl = "Resuelta"
        elif estado == "en_revision":
            est_bg  = "rgba(255,184,0,.12)"
            est_clr = "#FFB800"
            est_lbl = "En Revisión"
        else:
            est_bg  = "rgba(255,77,109,.10)"
            est_clr = "#FF4D6D"
            est_lbl = "Abierta"

        rows += f"""
<div class="ah-row">
  <span style="color:var(--muted)">{periodo}</span>
  <span style="font-weight:600">{h.get('entidad','–')}</span>
  <span style="color:var(--muted)">{tipo_lbl}</span>
  <span>
    <span class="ah-dot" style="background:{dot_clr}"></span>
    {titulo}
  </span>
  <span>
    <span class="ah-estado-badge" style="background:{est_bg};color:{est_clr}">
      {est_lbl}
    </span>
  </span>
</div>"""

    return header + rows


def _build_html(
    data: dict,
    history: list[dict] | None = None,
    tendencias: list[dict] | None = None,
) -> str:
    alerts = data["alerts"]
    ts     = data["ts_display"]

    # Header
    g_st   = data["status"]
    badge_clr = _CLR.get(g_st, "var(--white)")
    badge_bg  = _BG.get(g_st, "transparent")
    badge_bdr = _BDR.get(g_st, "var(--divider)")

    hdr = page_header(
        "🔔 ALERTAS",
        "Centro de Alertas de Cumplimiento",
        f"Verificación automática · {data['emoji']} {data['label']}",
        f'<span class="badge badge-{"red" if g_st == ERROR else ("amber" if g_st == WARNING else "green")}">Sprint 2.6</span>',
    )

    # Summary chips
    chips = (
        _chip("Críticas", data["n_error"], ERROR)
        + _chip("Advertencias", data["n_warning"], WARNING)
    )
    # ⚠️ El fallback sale de la f-string: Python ≤3.11 no admite backslash en la
    # expresión, y el CI corre 3.11. Nota para D-008: este texto usa
    # `var(--green)` —verde de «bien»— y esta página está fuera del universo del
    # gate visual. NO se cambia aquí: el color es decisión de curación, no de
    # compatibilidad, y mezclarlas escondería una en la otra.
    _sin_alertas = ('<span style="color:var(--green);font-size:13px;'
                    'font-weight:700">Sin alertas activas</span>')
    summary = f'<div class="alert-summary">{chips or _sin_alertas}</div>'

    # Empty state
    if not alerts:
        body = f"""
<div class="no-alerts">
  <div class="no-alerts-icon">✓</div>
  <div class="no-alerts-label">Sistema en buen estado</div>
  <div class="no-alerts-sub">
    No se detectaron alertas de ejecución ni cobertura documental<br>
    en el período más reciente.
  </div>
</div>"""
    else:
        # Agrupar por tipo
        por_tipo: dict[str, list] = {}
        for a in alerts:
            por_tipo.setdefault(a["tipo"], []).append(a)

        body = ""
        for tipo, tipo_alerts in por_tipo.items():
            icon  = _TIPO_ICON.get(tipo, "•")
            label = _TIPO_LABEL.get(tipo, tipo.title())
            n_err = sum(1 for a in tipo_alerts if a["status"] == ERROR)
            n_war = sum(1 for a in tipo_alerts if a["status"] == WARNING)
            count_str = " · ".join(filter(None, [
                f'{n_err} crítica{"s" if n_err != 1 else ""}' if n_err else "",
                f'{n_war} advertencia{"s" if n_war != 1 else ""}' if n_war else "",
            ]))
            body += f'<div class="section-label">{icon} {label} — {count_str}</div>'
            for a in tipo_alerts:
                body += _alert_card(a)

    tend_html = _tendencias_html(tendencias or [])
    hist_html = _historial_section_html(history or [])
    footer    = f'<div class="ts-footer">Última verificación: {ts} · Verificación institucional automática · Dylus Lab © 2026</div>'

    return hdr + summary + body + tend_html + hist_html + footer


# ── RENDER ────────────────────────────────────────────────────────────────────
def render() -> None:
    col_t, col_btn = st.columns([5, 1])
    with col_t:
        st.caption("**Alertas de Cumplimiento** · Ejecución y cobertura documental")
    with col_btn:
        recheck = st.button("↻ Verificar", use_container_width=True,
                            help="Re-verificar alertas del período más reciente")

    cache_key = "alertas_result"
    if recheck or cache_key not in st.session_state:
        with st.spinner("Analizando alertas institucionales…"):
            st.session_state[cache_key] = run_alert_check()

    data = st.session_state[cache_key]

    # ── KPIs nativos (fuera del iframe para mejor rendimiento) ────────────────
    kpis = get_alert_kpis()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("🔴 Críticas activas",     kpis["criticas_activas"])
    k2.metric("🟡 Advertencias activas", kpis["advertencias_activas"])
    k3.metric("🟢 Resueltas este mes",   kpis["resueltas_este_mes"])
    k4.metric("📅 Días sin resolver",    kpis["dias_abierta_max"],
              help="Alerta más antigua aún abierta")

    # ── Filtros ───────────────────────────────────────────────────────────────
    with st.expander("🔍 Filtrar historial", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        f_entidad = fc1.selectbox("Entidad", ["(todas)", "GAD", "BOMBEROS", "EMAI-EP", "PATRONATO"])
        f_tipo    = fc2.selectbox("Tipo", ["(todos)", "ejecucion", "cobertura"])
        f_estado  = fc3.selectbox("Estado", ["(todos)", "pendiente", "en_revision", "resuelta"])

    ent_filter  = "" if f_entidad == "(todas)"  else f_entidad
    tipo_filter = "" if f_tipo    == "(todos)"  else f_tipo
    est_filter  = "" if f_estado  == "(todos)"  else f_estado

    history    = get_alerts_history(limit=60,
                                    entidad=ent_filter,
                                    tipo=tipo_filter,
                                    estado=est_filter)
    tendencias = get_tendencias()

    # ── Iframe principal ──────────────────────────────────────────────────────
    html = _build_html(data, history, tendencias)
    full = page_frame(html, show_tech=False, extra_css=EXTRA_CSS)

    n_alerts = data["n_total"]
    n_hist   = min(len(history), 40)
    n_tend   = len(tendencias)
    height   = max(750, 300 + n_alerts * 140 + n_hist * 28 + n_tend * 60)
    components.html(full, height=height, scrolling=False)

    # ── Panel de resolución humana (NATIVO — no iframe) ───────────────────────
    pendientes = get_alerts_history(limit=20, estado="pendiente")
    en_rev     = get_alerts_history(limit=20, estado="en_revision")
    gestionables = pendientes + en_rev

    if gestionables:
        st.markdown("---")
        with st.expander(
            f"📋 Gestionar Alertas ({len(gestionables)} sin resolver)",
            expanded=False,
        ):
            st.caption(
                "Registra el estado y la justificación institucional de cada alerta. "
                "Este comentario queda en la **memoria permanente del sistema**."
            )
            for a in gestionables:
                estado_lbl = "🔴 Pendiente" if a["estado"] == ESTADO_ABIERTA else "🟡 En Revisión"
                with st.container():
                    ca, cb = st.columns([3, 1])
                    with ca:
                        st.markdown(
                            f"**{a['titulo']}** · `{a['entidad']}` · "
                            f"{a.get('period_month','')}/{a.get('period_year','')} · "
                            f"{estado_lbl}"
                        )
                    with cb:
                        if a["estado"] == ESTADO_ABIERTA:
                            if st.button("Tomar revisión", key=f"rev_{a['id']}",
                                         use_container_width=True):
                                mark_en_revision(a["id"])
                                st.session_state.pop("alertas_result", None)
                                st.rerun()

                    # ── 🧠 + 💡 Contexto y borrador (Sprint 2.8B/C) ──────────
                    ctx        = get_context_for_alert(a)
                    suggestion = build_resolution_suggestion(a, ctx=ctx)

                    if ctx and ctx["n_total"] > 0:
                        with st.expander(
                            f"🧠 Antecedentes comparables — {ctx['n_total']} caso(s) similar(es)",
                            expanded=False,
                        ):
                            st.caption(
                                "Casos similares resueltos por el equipo institucional. "
                                "No es una predicción — es memoria operativa trazable."
                            )
                            for caso in ctx["casos_similares"]:
                                dias = caso.get("dias_resolucion")
                                dias_str   = f"{dias}d" if dias is not None else "–"
                                reinc_icon = "🔁 Reincidió" if caso.get("reincidio") else "✓ Sin reincidencia"
                                st.markdown(
                                    f"**{caso['entidad']}** · {caso['periodo']} · "
                                    f"_{caso['categoria']}_ · {dias_str} · {reinc_icon}  \n"
                                    f"> *{caso['resolucion']}*"
                                )
                            st.info(
                                f"**Línea operativa:** {ctx['recomendacion_operativa']}",
                                icon="💡",
                            )
                    else:
                        st.caption(
                            "🧠 Sin antecedentes comparables registrados aún — "
                            "la memoria se construye con las resoluciones del equipo."
                        )

                    # ── 💡 Borrador institucional (Sprint 2.8C) ───────────────
                    if suggestion:
                        confianza_pct = suggestion["confianza_pct"]
                        if confianza_pct >= 70:
                            conf_color, conf_lbl = "#006B3C", "ALTA"
                        elif confianza_pct >= 50:
                            conf_color, conf_lbl = "#8C5A00", "MEDIA"
                        else:
                            conf_color, conf_lbl = "#555", "BAJA"

                        st.markdown(
                            f"**💡 Borrador institucional sugerido** &nbsp;"
                            f'<span style="background:{conf_color};color:#fff;padding:1px 7px;'
                            f'border-radius:8px;font-size:0.75rem;font-weight:700">'
                            f"{conf_lbl} {confianza_pct}%</span> &nbsp;"
                            f'<span style="color:#888;font-size:0.82rem">'
                            f"Categoría: {suggestion['label_probable']}</span>",
                            unsafe_allow_html=True,
                        )
                        _borrador = suggestion.get("borrador_resolucion", "")
                        borrador_preview = _borrador[:140] + ("…" if len(_borrador) > 140 else "")
                        st.caption(f"_{borrador_preview}_")

                        key_sug   = f"sug_used_{a['id']}"
                        key_bor   = f"sug_borrador_{a['id']}"
                        if st.button(
                            "📋 Insertar borrador institucional",
                            key=f"ins_{a['id']}",
                            help="Carga el borrador en el campo de justificación. Edítalo libremente antes de confirmar.",
                        ):
                            st.session_state[f"res_{a['id']}"] = _borrador
                            st.session_state[key_sug]  = True
                            st.session_state[key_bor]  = _borrador
                            st.session_state[f"sug_cat_{a['id']}"]  = suggestion.get("categoria_probable", "")
                            st.session_state[f"sug_conf_{a['id']}"] = suggestion.get("confianza", 0.0)
                            st.rerun()
                        st.caption(
                            "_Antecedente comparable — editable libremente — "
                            "la decisión final es siempre del funcionario responsable._"
                        )

                    comentario = st.text_area(
                        "Justificación / Resolución institucional",
                        key=f"res_{a['id']}",
                        placeholder='Ej: "Proceso detenido por reforma presupuestaria aprobada en sesión extraordinaria"',
                        height=90,
                        label_visibility="collapsed",
                    )
                    if st.button("✓ Marcar como resuelta", key=f"ok_{a['id']}",
                                 use_container_width=False,
                                 disabled=not comentario.strip()):
                        sug_used  = st.session_state.get(f"sug_used_{a['id']}", False)
                        sug_cat   = st.session_state.get(f"sug_cat_{a['id']}", None)
                        sug_conf  = st.session_state.get(f"sug_conf_{a['id']}", None)
                        orig_bor  = st.session_state.get(f"sug_borrador_{a['id']}", "")
                        edited    = sug_used and (comentario.strip() != orig_bor.strip())
                        resolve_alert_with_comment(
                            a["id"], comentario,
                            suggestion_used=sug_used,
                            suggestion_category=sug_cat,
                            suggestion_confidence=sug_conf,
                            edited_before_submit=edited,
                        )
                        st.session_state.pop("alertas_result", None)
                        st.success("Alerta resuelta y registrada en la memoria institucional.")
                        st.rerun()
                    st.markdown("---")

    # ── Export institucional ───────────────────────────────────────────────────
    st.markdown("---")
    all_history = get_alerts_history(limit=200)
    xlsx_bytes  = export_alerts_xlsx(all_history, kpis)
    if xlsx_bytes:
        from datetime import date as _date
        st.download_button(
            label="📊 Exportar Alertas a Excel (LOTAIP / Rendición de Cuentas)",
            data=xlsx_bytes,
            file_name=f"alertas_cumplimiento_{_date.today().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    # ── Navegación ────────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📥 Cargar cédula faltante", use_container_width=True):
            st.session_state["page"] = "ingesta"
            st.rerun()
    with c2:
        if st.button("⬡ Ver Congruencia Institucional", use_container_width=True):
            st.session_state["page"] = "congruencia"
            st.rerun()
