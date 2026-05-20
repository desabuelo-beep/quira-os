"""
QUIRA OS · p_congruencia.py
Estado de Congruencia Institucional — Sprint 2.5C

Página visible para analista, director y alcalde.
El lenguaje es institucional — no técnico.
La arquitectura interna (Excel, Supabase, Obsidian) no se expone.

Dylus Lab © 2026
"""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from quira_pages.html_engine import DEMO_CSS, page_frame, page_header
from sentinel.parity_engine import (
    get_congruencia_status,
    get_historial_congruencia,
    OK, WARNING, ERROR,
)
from sentinel.integrity_engine import run_integrity_check

# ── CSS EXTRA ─────────────────────────────────────────────────────────────────
EXTRA_CSS = """
.par-header {
  text-align: center; padding: 22px 0 18px;
}
.par-badge {
  display: inline-block; padding: 7px 22px; border-radius: 30px;
  font-size: 14px; font-weight: 800; letter-spacing: 0.04em;
  margin-bottom: 6px;
}
.par-ts {
  font-size: 10px; color: var(--muted); margin-top: 4px;
}
.pillar-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;
  margin-bottom: 14px;
}
@media (max-width: 600px) {
  .pillar-grid { grid-template-columns: 1fr !important; }
}
.pillar-card {
  background: var(--navy-card); border-radius: 12px;
  padding: 18px 16px; border: 1px solid var(--divider);
  position: relative; overflow: hidden;
}
.pillar-icon {
  font-size: 26px; margin-bottom: 8px;
}
.pillar-name {
  font-size: 13px; font-weight: 700; color: var(--white);
  margin-bottom: 4px;
}
.pillar-desc {
  font-size: 10px; color: var(--muted); line-height: 1.5;
  margin-bottom: 12px;
}
.pillar-status {
  display: flex; align-items: center; gap: 7px;
  font-size: 12px; font-weight: 700;
}
.pillar-metric {
  font-size: 10px; color: var(--muted); margin-top: 8px;
  padding-top: 8px; border-top: 1px solid var(--divider);
  line-height: 1.7;
}
.pillar-accent {
  position: absolute; top: 0; left: 0; right: 0;
  height: 3px; border-radius: 12px 12px 0 0;
}
.issue-list {
  margin-top: 8px; padding-left: 0; list-style: none;
}
.issue-list li {
  font-size: 10px; color: var(--amber); padding: 2px 0;
}
.issue-list li::before { content: "⚠ "; }

.hist-row {
  display: flex; align-items: center; gap: 10px;
  padding: 7px 0; border-bottom: 1px solid var(--divider);
  font-size: 11px;
}
.hist-row:last-child { border-bottom: none; }
.hist-ts { color: var(--muted); font-size: 10px; min-width: 130px; }
.hist-label { flex: 1; font-weight: 600; }
.hist-capas { font-size: 9px; color: var(--muted); font-family: var(--mono); }

.sync-btn-area {
  text-align: center; margin: 16px 0 8px;
}

/* ── Integridad Semántica ── */
.integrity-header {
  font-size: 11px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: 12px;
}
.integrity-badge {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 16px; border-radius: 20px;
  font-size: 13px; font-weight: 700; margin-bottom: 12px;
}
.integrity-sublabel {
  font-size: 10px; color: var(--muted); margin-bottom: 14px;
}
.integrity-table {
  width: 100%; border-collapse: collapse; font-size: 11px;
}
.integrity-table th {
  font-size: 9px; font-weight: 700; color: var(--muted);
  text-transform: uppercase; letter-spacing: .06em;
  padding: 5px 8px; border-bottom: 1px solid var(--divider);
  text-align: left;
}
.integrity-table td {
  padding: 6px 8px; border-bottom: 1px solid rgba(255,255,255,.04);
  vertical-align: middle;
}
.int-dot {
  width: 8px; height: 8px; border-radius: 50%;
  display: inline-block; margin-right: 4px;
}
.int-val {
  font-family: var(--mono); font-size: 11px;
}
.int-delta {
  font-family: var(--mono); font-size: 10px; color: var(--muted);
}
"""

# ── COLOR MAP ─────────────────────────────────────────────────────────────────
_STATUS_COLOR = {OK: "var(--green)", WARNING: "var(--amber)", ERROR: "var(--red)"}
_STATUS_LABEL = {OK: "Operativo", WARNING: "Requiere Atención", ERROR: "Requiere Revisión"}
_STATUS_BG    = {OK: "rgba(0,224,150,.08)", WARNING: "rgba(255,184,0,.08)", ERROR: "rgba(255,77,109,.08)"}
_STATUS_BORDER= {OK: "rgba(0,224,150,.25)", WARNING: "rgba(255,184,0,.25)", ERROR: "rgba(255,77,109,.25)"}
_ICON_CAPA    = {OK: "✓", WARNING: "⚠", ERROR: "✗"}


# ── HELPERS HTML ──────────────────────────────────────────────────────────────
def _global_badge(label: str, color: str, emoji: str) -> str:
    bg  = color.replace(")", ",0.15)").replace("rgb", "rgba") if "rgb" in color else color + "26"
    return f"""
<div class="par-header">
  <div class="par-badge" style="background:{bg};color:{color};border:1px solid {color}40">
    {emoji} {label}
  </div>
</div>"""


def _pillar_card(
    icon: str, name: str, desc: str,
    status: str, metric_lines: list[str],
    issues: list[str], accent_color: str,
) -> str:
    clr       = _STATUS_COLOR.get(status, "var(--white)")
    bg        = _STATUS_BG.get(status, "transparent")
    border    = _STATUS_BORDER.get(status, "var(--divider)")
    s_label   = _STATUS_LABEL.get(status, status)
    s_icon    = _ICON_CAPA.get(status, "?")

    issues_html = ""
    if issues:
        li = "".join(f"<li>{i}</li>" for i in issues[:3])
        issues_html = f'<ul class="issue-list">{li}</ul>'

    metrics_html = "".join(f"{m}<br>" for m in metric_lines)

    return f"""
<div class="pillar-card" style="background:{bg};border-color:{border}">
  <div class="pillar-accent" style="background:{accent_color}"></div>
  <div class="pillar-icon">{icon}</div>
  <div class="pillar-name">{name}</div>
  <div class="pillar-desc">{desc}</div>
  <div class="pillar-status">
    <span style="color:{clr};font-size:16px">{s_icon}</span>
    <span style="color:{clr}">{s_label}</span>
  </div>
  <div class="pillar-metric">{metrics_html}</div>
  {issues_html}
</div>"""


def _hist_icon(status: str) -> str:
    return {"ok": "🟢", "warning": "🟡", "error": "🔴"}.get(status, "⬜")


def _integrity_html(integrity: dict | None) -> str:
    if integrity is None:
        return """
<div class="card" style="margin-bottom:14px">
  <div class="integrity-header">Integridad Semántica</div>
  <div style="font-size:11px;color:var(--muted);padding:8px 0">
    No se pudo ejecutar la verificación de integridad.
  </div>
</div>"""

    st    = integrity["status"]
    clr   = _STATUS_COLOR.get(st, "var(--white)")
    bg    = _STATUS_BG.get(st, "transparent")
    bdr   = _STATUS_BORDER.get(st, "var(--divider)")

    # Badge global
    badge = f"""
<div class="integrity-badge" style="background:{bg};color:{clr};border:1px solid {bdr}">
  {integrity['emoji']} {integrity['label']}
  <span style="font-size:10px;font-weight:400;margin-left:4px;opacity:.7">
    {integrity['n_ok']}/{integrity['n_total']}
  </span>
</div>
<div class="integrity-sublabel">{integrity['sublabel']}</div>"""

    # Tabla de checks
    _DOT_COLOR = {OK: "#00E096", WARNING: "#FFB800", ERROR: "#FF4D6D"}

    rows = ""
    for ch in integrity["checks"]:
        dot   = _DOT_COLOR.get(ch["status"], "#666")
        v_mot = f"{ch['motor']:.2f}{ch['unit']}" if ch["motor"] is not None else "–"
        v_mem = f"{ch['memoria']:.2f}{ch['unit']}" if ch["memoria"] is not None else "–"
        delta = ch.get("delta", "–")
        rows += f"""
<tr>
  <td>
    <span class="int-dot" style="background:{dot}"></span>
    {ch['label']}
  </td>
  <td class="int-val">{v_mot}</td>
  <td class="int-val">{v_mem}</td>
  <td class="int-delta">{delta}</td>
</tr>"""

    table = f"""
<table class="integrity-table">
  <thead>
    <tr>
      <th>Indicador</th>
      <th>Motor Analítico</th>
      <th>Memoria Inst.</th>
      <th>Δ</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>"""

    return f"""
<div class="card" style="margin-bottom:14px">
  <div class="integrity-header">Integridad Semántica — Coherencia de Valores</div>
  {badge}
  {table}
</div>"""


def _historial_html(historial: list[dict]) -> str:
    if not historial:
        return """
<div style="text-align:center;color:var(--muted);font-size:12px;padding:20px 0">
  Sin registros de sincronización anteriores
</div>"""

    rows = ""
    for h in historial[:12]:
        ts_raw = h.get("ts", "")
        try:
            from datetime import datetime
            ts_display = datetime.fromisoformat(ts_raw).strftime("%d %b %Y, %H:%M")
        except Exception:
            ts_display = ts_raw[:16] if ts_raw else "–"

        fi = _hist_icon(h.get("fuente", ""))
        mi = _hist_icon(h.get("memoria", ""))
        mo = _hist_icon(h.get("motor", ""))
        lbl = h.get("label", h.get("status", ""))
        clr = {"ok": "var(--green)", "warning": "var(--amber)", "error": "var(--red)"}.get(
            h.get("status", ""), "var(--muted)"
        )

        rows += f"""
<div class="hist-row">
  <span class="hist-ts">{ts_display}</span>
  <span class="hist-label" style="color:{clr}">{lbl}</span>
  <span class="hist-capas">{fi} Fuente · {mi} Memoria · {mo} Motor</span>
</div>"""
    return rows


# ── RENDER PRINCIPAL ──────────────────────────────────────────────────────────
def render() -> None:
    # Botón de refresco
    col_t, col_btn = st.columns([5, 1])
    with col_t:
        st.caption("**Congruencia Institucional** · Alineación del sistema QUIRA OS")
    with col_btn:
        recheck = st.button("↻ Verificar", use_container_width=True,
                            help="Re-verificar estado de las tres capas")

    cache_key   = "congruencia_result"
    int_cache   = "integrity_result"
    if recheck or cache_key not in st.session_state:
        with st.spinner("Verificando capas institucionales…"):
            st.session_state[cache_key] = get_congruencia_status()
            try:
                st.session_state[int_cache] = run_integrity_check()
            except Exception:
                st.session_state[int_cache] = None

    st_data   = st.session_state[cache_key]
    integrity = st.session_state.get(int_cache)

    g_label   = st_data["global_label"]
    g_color   = st_data["global_color"]
    g_emoji   = st_data["global_emoji"]
    g_ts      = st_data["checked_display"]
    fuente    = st_data["fuente"]
    memoria   = st_data["memoria"]
    motor     = st_data["motor"]

    # ── HTML ───────────────────────────────────────────────────────────────────
    hdr = page_header(
        "⬡ CONGRUENCIA",
        "Estado Institucional del Sistema",
        f"Verificación automática · {g_emoji} {g_label}",
        f'<span class="badge badge-{"green" if st_data["global_status"]==OK else ("amber" if st_data["global_status"]==WARNING else "red")}">Sprint 2.5C</span>',
    )

    # Badge global
    badge = _global_badge(g_label, g_color, g_emoji)
    ts_html = f'<div class="par-ts" style="text-align:center;margin-bottom:18px">Última verificación: {g_ts}</div>'

    # Tres pilares
    fuente_metrics = [
        f"Documentos cargados: <b style='color:var(--cyan)'>{fuente.get('total_uploads', 0)}</b>",
        f"Entidades activas: <b style='color:var(--cyan)'>{len(fuente.get('entidades_cargadas', []))}/4</b>",
        f"KPIs registrados: <b style='color:var(--cyan)'>{fuente.get('kpi_rows', 0)}</b>",
        f"Última actualización: <b>{fuente.get('last_upload_display', '–')}</b>",
    ]
    memoria_metrics = [
        f"Registros en vault: <b style='color:var(--cyan)'>{memoria.get('file_count', 0)}</b>",
        f"Última sincronización: <b>{memoria.get('last_updated', '–')}</b>",
    ]
    motor_metrics = [
        f"Entidades monitoreadas: <b style='color:var(--cyan)'>{len(motor.get('entidades_con_kpis', []))}/4</b>",
        f"Períodos históricos: <b style='color:var(--cyan)'>{motor.get('n_periodos', 0)}</b>",
        f"Reglas activas: <b style='color:var(--cyan)'>{motor.get('reglas_activas', 0)}</b>",
        f"Confiabilidad: <b style='color:var(--cyan)'>{motor.get('pct_cobertura', 0):.0f}%</b>",
    ]

    pilares_html = f"""
<div class="pillar-grid">
  {_pillar_card(
      "📄", "Fuente Operativa",
      "Documentos mensuales validados: cédulas presupuestarias, informes firmados y evidencias documentales.",
      fuente["status"], fuente_metrics, fuente.get("issues", []), "#00D4FF"
  )}
  {_pillar_card(
      "🧠", "Memoria Institucional",
      "Conocimiento histórico y normativo del municipio: planes, PDOT, POA, PAC, informes y alertas previas.",
      memoria["status"], memoria_metrics, memoria.get("issues", []), "#7C5CFC"
  )}
  {_pillar_card(
      "⚙", "Motor Analítico",
      "KPIs, alertas, tendencias y cruces automáticos de las 4 entidades del holding municipal.",
      motor["status"], motor_metrics, motor.get("issues", []), "#00E096"
  )}
</div>"""

    # Historial
    historial = get_historial_congruencia(limit=12)
    hist_html = f"""
<div class="card">
  <div style="font-size:11px;font-weight:700;color:var(--muted);
              text-transform:uppercase;letter-spacing:.08em;margin-bottom:12px">
    Historial de Sincronizaciones
  </div>
  {_historial_html(historial)}
</div>"""

    # Nota metodológica
    nota_html = f"""
<div style="background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.12);
            border-radius:10px;padding:12px 16px;font-size:10px;
            color:var(--muted);line-height:1.7;margin-bottom:12px">
  <b style="color:var(--cyan)">Metodología de verificación</b><br>
  El sistema verifica automáticamente la consistencia entre las tres capas
  institucionales. Una verificación <b style="color:var(--green)">verde</b> confirma que
  los documentos cargados, el conocimiento histórico y el motor de análisis están
  alineados. Un estado <b style="color:var(--amber)">amarillo</b> indica que algún
  elemento requiere atención del equipo técnico. Un estado
  <b style="color:var(--red)">rojo</b> indica una discrepancia que debe resolverse
  antes de generar informes oficiales.<br>
  <span style="color:rgba(255,255,255,.3)">Sentinel Sprint 2.5C · Dylus Lab © 2026</span>
</div>"""

    integrity_html = _integrity_html(integrity)

    html = hdr + badge + ts_html + pilares_html + integrity_html + hist_html + nota_html

    full = page_frame(html, show_tech=False, extra_css=EXTRA_CSS)
    components.html(full, height=1450, scrolling=False)

    # Botones de navegación
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📥 Actualizar Fuente Operativa", use_container_width=True):
            st.session_state["page"] = "ingesta"
            st.rerun()
    with c2:
        if st.button("📈 Ver Inteligencia Histórica", use_container_width=True):
            st.session_state["page"] = "historico"
            st.rerun()
